"""Behavioral coverage for the repository launcher; fixtures never touch user data."""
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]


def cli(*args):
    return subprocess.run(
        [sys.executable, str(ROOT / "pythons_sort.py"), *map(str, args)],
        text=True, capture_output=True, timeout=10,
    )


def test_info_lists_complete_script_names():
    result = cli("info", "--category", "scanners")
    assert result.returncode == 0, result.stderr
    assert "function_scanner.py" in result.stdout


def test_run_executes_main_and_forwards_arguments(tmp_path):
    script = tmp_path / "sample tool.py"
    script.write_text("import sys\nif __name__ == '__main__':\n    print(repr(sys.argv[1:]))\n")
    result = cli("--repository", tmp_path, "run", script.name, "--", "a b", "--flag")
    assert result.returncode == 0, result.stderr
    assert "['a b', '--flag']" in result.stdout


def test_run_propagates_exit_status(tmp_path):
    (tmp_path / "fail.py").write_text("raise SystemExit(7)\n")
    result = cli("--repository", tmp_path, "run", "fail.py")
    assert result.returncode == 7


def test_dry_run_never_executes_legacy_top_level_code(tmp_path):
    marker = tmp_path / "changed"
    (tmp_path / "unsafe.py").write_text(f"from pathlib import Path\nPath({str(marker)!r}).touch()\n")
    result = cli("--repository", tmp_path, "run", "--dry-run", "unsafe.py")
    assert result.returncode == 0, result.stderr
    assert "Preview" in result.stdout
    assert not marker.exists()


def test_missing_tool_does_not_fall_back_to_prefix(tmp_path):
    (tmp_path / "tool_old.py").write_text("raise SystemExit(99)\n")
    result = cli("--repository", tmp_path, "run", "tool.py")
    assert result.returncode == 2
    assert "not found" in result.stderr


def test_external_symlink_is_rejected(tmp_path):
    (tmp_path / "external.py").symlink_to(ROOT / "pythons_sort.py")
    result = cli("--repository", tmp_path, "run", "external.py")
    assert result.returncode == 2
    assert "outside" in result.stderr


@pytest.mark.parametrize("command", ["analyze", "cleanup", "dedup", "organize", "scan", "rename", "pdf"])
def test_legacy_dispatch_reports_migration(command):
    result = cli(command, "/does/not/exist", "--dry-run")
    assert result.returncode == 2
    assert "run" in result.stderr


def test_legacy_entrypoint_delegates():
    result = subprocess.run(
        [sys.executable, str(ROOT / "file_operations/pythons_sort.py"), "info", "--category", "scanners"],
        cwd=ROOT.parent, text=True, capture_output=True, timeout=10,
    )
    assert result.returncode == 0, result.stderr
    assert "function_scanner.py" in result.stdout
