#!/usr/bin/env python3
"""
Content-based duplicate finder: group files by content hash, output CSV for consolidation.

Only files with identical contents (byte-for-byte) are reported as duplicates.
Output CSV: Hash, Size, Occurrences, Paths — compatible with Phase 1 when used as DUPLICATE_FILE.

Usage:
  python3 content_based_dedupe_report.py [--root PATH] [--max-depth N] [--out CSV] [--same-dir-only]
  python3 content_based_dedupe_report.py --root ~/REORGANIZATION_TEST_BED --out content_dedupe_report.csv
"""

import argparse
import csv
import hashlib
import os
from pathlib import Path
from collections import defaultdict

HOME = Path.home()
SKIP_DIRS = {
    ".venv", "venv", "__pycache__", ".git", "node_modules",
    "site-packages", ".Trash", ".cache", "Library", ".npm", ".cargo", ".bun",
}


def content_hash(filepath: Path, chunk_size: int = 65536) -> str:
    """SHA256 of file contents. Empty string on read error."""
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, PermissionError):
        return ""


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def scan_by_content(root: Path, max_depth: int) -> dict[str, list[Path]]:
    """Walk root and group file paths by content hash. Returns hash -> [paths]."""
    groups: dict[str, list[Path]] = defaultdict(list)
    root = Path(root).resolve()

    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        depth = len(current.relative_to(root).parts)
        if depth > max_depth:
            dirnames.clear()
            continue
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for name in filenames:
            fp = current / name
            if not fp.is_file():
                continue
            if should_skip(fp):
                continue
            h = content_hash(fp)
            if h:
                groups[h].append(fp)

    return groups


def main():
    ap = argparse.ArgumentParser(description="Content-based duplicate report (compare contents)")
    ap.add_argument("--root", type=Path, default=HOME / "REORGANIZATION_TEST_BED",
                    help="Root to scan")
    ap.add_argument("--max-depth", type=int, default=10, help="Max directory depth")
    ap.add_argument("--out", type=Path,
                    default=HOME / "REORGANIZATION_TEST_BED/data/inventory/content_dedupe_report.csv",
                    help="Output CSV path")
    ap.add_argument("--same-dir-only", action="store_true",
                    help="Only output groups where all paths are in the same directory (Phase 1 safe)")
    args = ap.parse_args()

    root = Path(args.root).expanduser()
    if not root.exists():
        print("Root does not exist:", root)
        return

    print("Scanning by content hash:", root)
    groups = scan_by_content(root, args.max_depth)

    # Only duplicate groups (2+ paths)
    dup_groups = {h: paths for h, paths in groups.items() if len(paths) > 1}
    print("Duplicate groups (same content):", len(dup_groups))

    out_path = Path(args.out).expanduser()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Hash", "Size", "Occurrences", "Paths"])
        for h, paths in dup_groups.items():
            if args.same_dir_only:
                dirs = set(p.parent for p in paths)
                if len(dirs) > 1:
                    continue
            size = paths[0].stat().st_size if paths else 0
            paths_str = ";".join(str(p) for p in sorted(paths))
            w.writerow([h, size, len(paths), paths_str])

    print("Wrote:", out_path)


if __name__ == "__main__":
    main()
