#!/usr/bin/env python3
"""Preview-first cleanup inventory for the local clean tool directory.

The default command only writes a before/after CSV.  ``--apply`` moves
selected candidates into a recoverable quarantine directory; it never deletes
files and it never rewrites README files or shell configuration.
"""

from __future__ import annotations

import argparse
import csv
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_NAMES = {"audio.py-bak", "docs.py-bak", "sorts.py-bak", "cleanup.py"}


def candidates(clean_dir: Path, include_zshrc: bool) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for name in sorted(DEFAULT_NAMES):
        path = clean_dir / name
        if path.is_file():
            rows.append({
                "before": str(path),
                "after": "",
                "reason": "legacy cleanup candidate",
                "status": "planned",
            })

    if include_zshrc:
        home = Path.home()
        backups = sorted(home.glob(".zshrc.backup*")) + sorted(home.glob(".zshrc.bak*"))
        backups.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        for path in backups[2:]:
            rows.append({
                "before": str(path),
                "after": "",
                "reason": "older shell backup; review explicitly",
                "status": "planned",
            })
    return rows


def write_preview(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["before", "after", "reason", "status"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def apply_quarantine(rows: list[dict[str, str]], quarantine: Path) -> None:
    quarantine.mkdir(parents=True, exist_ok=True)
    for row in rows:
        source = Path(row["before"])
        if not source.is_file():
            row["status"] = "missing"
            continue
        target = quarantine / source.name
        counter = 1
        while target.exists():
            target = quarantine / f"{source.stem}-{counter}{source.suffix}"
            counter += 1
        shutil.move(str(source), str(target))
        row["after"] = str(target)
        row["status"] = "quarantined"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.home() / "clean")
    parser.add_argument("--output", type=Path, help="Preview CSV path")
    parser.add_argument("--include-zshrc-backups", action="store_true")
    parser.add_argument("--apply", action="store_true", help="Move planned files to quarantine")
    parser.add_argument("--quarantine", type=Path, help="Recoverable quarantine directory")
    args = parser.parse_args()

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    output = args.output or Path(tempfile.gettempdir()) / f"clean-preview-{stamp}.csv"
    rows = candidates(args.root.expanduser().resolve(), args.include_zshrc_backups)
    quarantine = args.quarantine or Path(tempfile.gettempdir()) / f"clean-quarantine-{stamp}"
    if args.apply:
        apply_quarantine(rows, quarantine)
    write_preview(output, rows)
    print(f"Preview written: {output}")
    print(f"Candidates: {len(rows)} | mode: {'quarantine' if args.apply else 'preview-only'}")
    if args.apply:
        print(f"Recoverable quarantine: {quarantine}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
