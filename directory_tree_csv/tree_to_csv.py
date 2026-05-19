#!/usr/bin/env python3
"""
Export a directory tree to CSV (path, depth, name, is_file, size_bytes).
Gap: PMs/SEOs search 'folder structure csv' — few tiny dedicated OSS products.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Export directory listing to CSV.")
    p.add_argument("root", type=Path, help="Root directory to walk")
    p.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("directory_tree.csv"),
        help="Output CSV",
    )
    p.add_argument(
        "--max-depth",
        type=int,
        default=0,
        help="0 = unlimited depth",
    )
    return p.parse_args()


def depth_under(root: Path, path: Path) -> int:
    rel = path.relative_to(root)
    return len(rel.parts)


def main() -> int:
    args = parse_args()
    if not args.root.is_dir():
        print(f"Not a directory: {args.root}", file=sys.stderr)
        return 1

    root = args.root.resolve()
    rows: list[dict[str, str | int]] = []

    for path in root.rglob("*"):
        d = depth_under(root, path)
        if args.max_depth and d > args.max_depth:
            continue
        is_file = path.is_file()
        size = path.stat().st_size if is_file else 0
        rows.append(
            {
                "path": str(path),
                "depth": d,
                "name": path.name,
                "is_file": int(is_file),
                "size_bytes": size,
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(
            fh, fieldnames=["path", "depth", "name", "is_file", "size_bytes"]
        )
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote {len(rows)} entries -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
