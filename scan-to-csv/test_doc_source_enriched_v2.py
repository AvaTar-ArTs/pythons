import csv
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).with_name('doc-source-enriched-v2.py')


def test_only_complete_sha256_values_can_form_duplicate_groups():
    spec = importlib.util.spec_from_file_location('v2_hash_validation_test', SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.valid_sha256('a' * 64)
    assert module.valid_sha256('A' * 64)
    assert not module.valid_sha256('unknown')
    assert not module.valid_sha256('a' * 63)
    assert not module.valid_sha256('g' * 64)


def run_scan(root, out):
    return subprocess.run([sys.executable, str(SCRIPT), str(root), '-o', str(out)], capture_output=True, text=True, timeout=30)


def test_nested_duplicates_are_normalized(tmp_path):
    root = tmp_path / 'input'
    for branch in ['left/shared', 'right/shared']:
        folder = root / branch
        folder.mkdir(parents=True)
        (folder / 'same.md').write_text('identical fixture\n')
    out = tmp_path / 'report'
    result = run_scan(root, out)
    assert result.returncode == 0, result.stderr
    with (out / 'inventory.csv').open() as f:
        rows = list(csv.DictReader(f))
    assert {r['relative_path'] for r in rows} == {'left/shared/same.md', 'right/shared/same.md'}
    assert all('duplicate_paths' not in r for r in rows)
    with (out / 'duplicate-members.csv').open() as f:
        members = list(csv.DictReader(f))
    assert len(members) == 2
    assert len({r['duplicate_group_id'] for r in members}) == 1
    assert len(members[0]['duplicate_group_id']) == len('sha256:') + 64
    assert json.loads((out / 'summary.json').read_text())['file_count'] == 2
    assert str(root) not in (out / 'inventory.csv').read_text()


def test_duplicate_output_grows_linearly(tmp_path):
    sizes = []
    for count in [40, 80]:
        root = tmp_path / str(count)
        root.mkdir()
        for i in range(count):
            (root / f'file-{i:03}.md').write_text('same\n')
        out = tmp_path / f'report-{count}'
        result = run_scan(root, out)
        assert result.returncode == 0, result.stderr
        sizes.append(sum(p.stat().st_size for p in out.iterdir()))
        with (out / 'duplicate-members.csv').open() as f:
            assert len(list(csv.DictReader(f))) == count
    assert sizes[1] < sizes[0] * 2.2


def test_existing_output_and_in_tree_output_rejected(tmp_path):
    root = tmp_path / 'input'
    root.mkdir()
    out = tmp_path / 'report'
    out.mkdir()
    marker = out / 'keep'
    marker.write_text('preserve')
    assert run_scan(root, out).returncode == 2
    assert marker.read_text() == 'preserve'
    assert run_scan(root, root / 'report').returncode == 2
    assert not (root / 'report').exists()


def test_symlink_root_rejected(tmp_path):
    root = tmp_path / 'input'
    root.mkdir()
    link = tmp_path / 'link'
    link.symlink_to(root)
    assert run_scan(link, tmp_path / 'report').returncode == 2
    assert not (tmp_path / 'report').exists()


def test_empty_report_and_explicit_absolute_paths(tmp_path):
    root = tmp_path / 'input'
    root.mkdir()
    result = run_scan(root, tmp_path / 'empty')
    assert result.returncode == 0, result.stderr
    assert json.loads((tmp_path / 'empty/summary.json').read_text())['file_count'] == 0
    (root / 'file.md').write_text('fixture')
    out = tmp_path / 'private'
    result = subprocess.run([sys.executable, str(SCRIPT), str(root), '-o',
                             str(out), '--absolute-paths'], capture_output=True,
                            text=True, timeout=30)
    assert result.returncode == 0, result.stderr
    with (out / 'inventory.csv').open() as f:
        row = next(csv.DictReader(f))
    assert row['absolute_path'] == str(root / 'file.md')


def test_failed_write_does_not_publish_report(tmp_path, monkeypatch):
    import pytest

    sys.path.insert(0, str(SCRIPT.parent))
    spec = importlib.util.spec_from_file_location('v2_failure_test', SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    root = tmp_path / 'input'
    root.mkdir()
    (root / 'one.md').write_text('fixture')
    out = tmp_path / 'report'

    def fail(*args, **kwargs):
        raise OSError('simulated disk write failure')

    monkeypatch.setattr(module.os, 'fsync', fail)
    with pytest.raises(OSError, match='simulated'):
        module.build_report([root], out)
    assert not out.exists()
    assert not list(tmp_path.glob('.enriched-v2-*'))
