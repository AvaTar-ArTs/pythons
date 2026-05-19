#!/usr/bin/env python3
"""Scan for Python projects and .py files under /Users/steven.
Outputs:
- projects.csv: project roots (marker dirs) with metadata
- pyfiles.csv: all .py files with size/mtime
Excludes system + non-project heavy dirs.
"""
from __future__ import annotations

import csv
import os
from pathlib import Path
from datetime import datetime

ROOT = Path('/Users/steven')
OUT_DIR = Path('/Users/steven/python-inventory')
PROJECTS_CSV = OUT_DIR / 'projects.csv'
PYFILES_CSV = OUT_DIR / 'pyfiles.csv'

MARKERS = {
    'pyproject.toml','requirements.txt','setup.py','Pipfile','environment.yml',
    'setup.cfg','requirements.in','poetry.lock'
}
README_NAMES = {'README','README.md','README.txt','README.rst'}
LICENSE_NAMES = {'LICENSE','LICENSE.md','LICENSE.txt','COPYING'}

# System folders + excluded non-project areas
EXCLUDE_PREFIXES = [
    '/System/', '/Applications/', '/usr/', '/bin/', '/sbin/',
    '/opt/', '/private/', '/var/', '/etc/', '/tmp/',
    '/Users/steven/Library/',
    '/Users/steven/.local/',
    '/Users/steven/.cache/',
    '/Users/steven/.venv',
    '/Users/steven/.venv_dev',
    '/Users/steven/google-cloud-sdk/',
    '/Users/steven/Downloads/',
    '/Users/steven/iterm2/',
    '/Users/steven/.vscode/',
    '/Users/steven/.cursor/',
    '/Users/steven/.gemini/',
]


def excluded(path: Path) -> bool:
    p = str(path)
    return any(p.startswith(prefix) for prefix in EXCLUDE_PREFIXES)


def iter_tree(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirpath = Path(dirpath)
        if excluded(dirpath):
            dirnames[:] = []
            continue
        yield dirpath, dirnames, filenames


def nearest_repo_root(p: Path) -> Path:
    for parent in [p] + list(p.parents):
        if (parent / '.git').exists():
            return parent
    return p


def main():
    projects = {}
    pyfiles = []

    for dirpath, _, filenames in iter_tree(ROOT):
        # project markers
        marker_hits = sorted([f for f in filenames if f in MARKERS])
        if marker_hits:
            projects.setdefault(dirpath, set()).update(marker_hits)

        # .py files inventory
        for f in filenames:
            if f.endswith('.py'):
                p = dirpath / f
                if excluded(p):
                    continue
                try:
                    st = p.stat()
                    pyfiles.append((
                        str(p),
                        st.st_size,
                        datetime.fromtimestamp(st.st_mtime).isoformat(timespec='seconds'),
                    ))
                except OSError:
                    continue

    # write projects.csv
    with PROJECTS_CSV.open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['project_path','repo_root','markers','has_readme','has_license','py_files_in_dir'])
        for p, markers in sorted(projects.items(), key=lambda x: str(x[0]).lower()):
            try:
                files = set(os.listdir(p))
            except OSError:
                files = set()
            has_readme = any(name in files for name in README_NAMES)
            has_license = any(name in files for name in LICENSE_NAMES)
            py_here = len([name for name in files if name.endswith('.py')])
            w.writerow([
                str(p),
                str(nearest_repo_root(p)),
                ';'.join(sorted(markers)),
                str(has_readme),
                str(has_license),
                str(py_here),
            ])

    # write pyfiles.csv
    with PYFILES_CSV.open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['file_path','size_bytes','mtime'])
        for row in sorted(pyfiles, key=lambda x: x[0].lower()):
            w.writerow(row)


if __name__ == '__main__':
    main()
