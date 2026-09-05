#!/usr/bin/env python3
"""V2 normalized report writer using the existing enrichment engine.

No repeated duplicate path lists. Output is a new directory outside scan roots.
The legacy scanner and its heuristics remain unchanged; see README-enriched-v2.md.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import os
import re
import shutil
import tempfile
from collections import Counter
from pathlib import Path


def valid_sha256(value: object) -> bool:
    """Return whether value is a complete hexadecimal SHA-256 digest."""
    return isinstance(value, str) and bool(re.fullmatch(r'[0-9a-fA-F]{64}', value))


def build_report(directories, output, *, absolute_paths=False):
    roots = []
    for raw in directories:
        path = Path(raw).expanduser()
        # Reject symlinks in any supplied root component before resolving.
        path = Path(os.path.abspath(path))
        if any(p.is_symlink() for p in (path, *path.parents)):
            raise ValueError('symlinked root or ancestor is not supported')
        path = path.resolve()
        if not path.is_dir():
            raise ValueError('scan root must be a directory')
        roots.append(path)
    roots = sorted(set(roots), key=lambda p: (len(p.parts), str(p)))
    roots = [p for p in roots if not any(q in p.parents for q in roots)]
    if not roots:
        raise ValueError('at least one root is required')
    output = Path(output).expanduser()
    if output.exists() or output.is_symlink():
        raise ValueError('output already exists; select a new report directory')
    output = output.resolve()
    if any(output == p or p in output.parents for p in roots):
        raise ValueError('output must be outside every scan root')

    source = Path(__file__).with_name('doc-source-enriched.py')
    spec = importlib.util.spec_from_file_location('enriched_v1_engine', source)
    if spec is None or spec.loader is None:
        raise ValueError('cannot load sibling enrichment engine')
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    setattr(engine, 'QUIET_MODE', True)
    rows = engine.scan_and_enrich([str(p) for p in roots])
    # Do NOT call annotate_duplicates: it creates the quadratic path-list payload.
    counts = Counter(r['content_hash'].lower() for r in rows
                     if valid_sha256(r.get('content_hash')))
    for row in rows:
        path = Path(row.pop('full_path'))
        index = next(i for i, root in enumerate(roots) if root in path.parents)
        row.pop('original_path', None)
        for field in ('duplicate_paths', 'duplicate_group', 'duplicate_count',
                      'duplicate_basis', 'same_filename_in_group'):
            row.pop(field, None)
        row['schema_version'] = '2.0'
        row['root_id'] = f'root-{index + 1}'
        row['relative_path'] = str(path.relative_to(roots[index]))
        digest = row.get('content_hash', '')
        if valid_sha256(digest):
            digest = digest.lower()
            row['content_hash'] = digest
        else:
            digest = ''
        row['duplicate_group_id'] = (
            'sha256:' + digest if digest and counts[digest] > 1 else ''
        )
        if absolute_paths:
            row['absolute_path'] = str(path)
    rows.sort(key=lambda r: (r['root_id'], r['relative_path']))
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.enriched-v2-', dir=output.parent))
    try:
        columns = list(rows[0]) if rows else [
            'schema_version', 'root_id', 'relative_path', 'content_hash',
            'duplicate_group_id',
        ]
        with (staging / 'inventory.csv').open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            for row in rows:
                writer.writerow({k: ("'" + v if isinstance(v, str) and
                                     v.startswith(('=', '+', '-', '@')) else v)
                                 for k, v in row.items()})
            f.flush()
            os.fsync(f.fileno())
        member_count = 0
        with (staging / 'duplicate-members.csv').open('w', newline='', encoding='utf-8') as f:
            fields = ['duplicate_group_id', 'content_hash', 'duplicate_count',
                      'root_id', 'relative_path', 'filename', 'file_size_bytes']
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for row in rows:
                if row['duplicate_group_id']:
                    values = {
                        'duplicate_group_id': row['duplicate_group_id'],
                        'content_hash': row.get('content_hash', ''),
                        'duplicate_count': counts[row['content_hash']],
                        'root_id': row['root_id'],
                        'relative_path': row['relative_path'],
                        'filename': row.get('filename', ''),
                        'file_size_bytes': row.get('file_size_bytes', ''),
                    }
                    writer.writerow({k: ("'" + str(v) if isinstance(v, str) and
                                         v.startswith(('=', '+', '-', '@')) else v)
                                     for k, v in values.items()})
                    member_count += 1
            f.flush()
            os.fsync(f.fileno())
        summary = {
            'schema_version': '2.0', 'file_count': len(rows),
            'duplicate_group_count': sum(v > 1 for v in counts.values()),
            'duplicate_member_count': member_count,
            'path_encoding': 'CSV formula-leading strings prefixed with apostrophe',
            'roots': [{'root_id': f'root-{i + 1}', **(
                {'absolute_path': str(p)} if absolute_paths else {})}
                for i, p in enumerate(roots)],
            'limitations': ['Legacy enrichment and exclusion policy retained',
                           'Full hashing and in-memory rows; not a bounded metadata-only scan',
                           'Live tree is not an atomic filesystem snapshot',
                           'No cleanup or canonical-copy selection'],
        }
        with (staging / 'summary.json').open('w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
            f.write('\n')
            f.flush()
            os.fsync(f.fileno())
        if output.exists() or output.is_symlink():
            raise ValueError('output appeared during scan; refusing replacement')
        staging.rename(output)
        return summary
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directories', nargs='+')
    parser.add_argument('-o', '--output', required=True, type=Path,
                        help='New report directory OUTSIDE all scanned roots')
    parser.add_argument('--absolute-paths', action='store_true',
                        help='Include private absolute paths explicitly')
    args = parser.parse_args()
    try:
        result = build_report(args.directories, args.output,
                              absolute_paths=args.absolute_paths)
    except (OSError, ValueError) as exc:
        parser.exit(2, f'error: {exc}\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
