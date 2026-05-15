#!/usr/bin/env python3
"""
Merge multiple CSV files with optional deduplication on a key column.
Fills the gap: many search results show snippets; few ship as a CLI product.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Merge CSV files. Optionally drop duplicate rows by column."
    )
    p.add_argument(
        "inputs",
        nargs="+",
        type=Path,
        help="Input CSV paths (order preserved)",
    )
    p.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        help="Output CSV path",
    )
    p.add_argument(
        "--dedupe-column",
        metavar="COL",
        help="If set, drop duplicate rows keeping first, based on this column",
    )
    p.add_argument(
        "--encoding",
        default="utf-8",
        help="File encoding (default utf-8)",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    frames = []
    for path in args.inputs:
        if not path.is_file():
            print(f"Missing file: {path}", file=sys.stderr)
            return 1
        frames.append(pd.read_csv(path, encoding=args.encoding))
    merged = pd.concat(frames, ignore_index=True)
    if args.dedupe_column:
        if args.dedupe_column not in merged.columns:
            print(
                f"Column {args.dedupe_column!r} not in columns: {list(merged.columns)}",
                file=sys.stderr,
            )
            return 2
        merged = merged.drop_duplicates(subset=[args.dedupe_column], keep="first")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(args.output, index=False, encoding=args.encoding)
    print(f"Wrote {len(merged)} rows -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
