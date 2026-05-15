#!/usr/bin/env python3
"""
Compare two CSVs: columns, dtypes (inferred), row counts, optional key overlap.
Unique SKU: 'merge' tools abound; 'did my export break?' needs schema diff.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Compare schema and shape of two CSV files."
    )
    p.add_argument("csv_a", type=Path, help="First CSV (e.g. yesterday)")
    p.add_argument("csv_b", type=Path, help="Second CSV (e.g. today)")
    p.add_argument(
        "--key",
        metavar="COL",
        help="If set, report key-only overlap counts (inner join size)",
    )
    p.add_argument("--encoding", default="utf-8")
    p.add_argument("-o", "--report", type=Path, help="Write markdown report file")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    for path in (args.csv_a, args.csv_b):
        if not path.is_file():
            print(f"Missing: {path}", file=sys.stderr)
            return 1

    a = pd.read_csv(args.csv_a, encoding=args.encoding)
    b = pd.read_csv(args.csv_b, encoding=args.encoding)

    cols_a = set(a.columns)
    cols_b = set(b.columns)
    only_a = sorted(cols_a - cols_b)
    only_b = sorted(cols_b - cols_a)
    common = sorted(cols_a & cols_b)

    lines: list[str] = []
    lines.append("# CSV schema diff\n")
    lines.append(f"- **A:** `{args.csv_a}` → rows **{len(a)}**, cols **{len(cols_a)}**\n")
    lines.append(f"- **B:** `{args.csv_b}` → rows **{len(b)}**, cols **{len(cols_b)}**\n")
    lines.append("\n## Column set\n")
    lines.append(f"- Only in A: {only_a or '—'}\n")
    lines.append(f"- Only in B: {only_b or '—'}\n")
    lines.append(f"- Common: {len(common)} columns\n")

    lines.append("\n## Dtype pairs (common columns)\n")
    for c in common:
        da = a[c].dtype
        db = b[c].dtype
        mark = "" if da == db else " **(mismatch)**"
        lines.append(f"- `{c}`: A={da} | B={db}{mark}\n")

    if args.key:
        if args.key not in common:
            print(f"Key {args.key!r} not in both files' columns.", file=sys.stderr)
            return 2
        inner = pd.merge(
            a[[args.key]], b[[args.key]], on=args.key, how="inner"
        )
        lines.append("\n## Key overlap\n")
        lines.append(f"- Key `{args.key}`: inner rows **{len(inner)}**\n")

    text = "".join(lines)
    print(text)
    if args.report:
        args.report.write_text(text, encoding="utf-8")
        print(f"Wrote {args.report}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
