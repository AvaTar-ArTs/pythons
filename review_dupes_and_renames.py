#!/usr/bin/env python3
"""
Safe duplicate + rename review helper.

What it does:
1) Finds exact content duplicates using SHA-256.
2) Proposes normalized filenames for common copy suffix patterns.
3) Writes CSV reports and supports optional apply mode for safe renames.

No deletions are performed.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


COPY_SUFFIX_PATTERNS = [
    re.compile(r"^(?P<base>.+?)__(?P<num>\d+)$"),   # foo__2
    re.compile(r"^(?P<base>.+?)\s(?P<num>\d+)$"),   # foo 2
]


@dataclass
class FileMeta:
    path: Path
    relpath: str
    size: int
    sha256: str


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def iter_files(root: Path, max_depth: int) -> list[Path]:
    files: list[Path] = []
    root_depth = len(root.parts)
    for dirpath, _, filenames in os.walk(root):
        current_depth = len(Path(dirpath).parts) - root_depth
        if current_depth > max_depth:
            continue
        for name in filenames:
            p = Path(dirpath) / name
            if p.is_file():
                files.append(p)
    return files


def strip_copy_suffix(stem: str) -> str:
    """
    Repeatedly strip known copy suffixes to get a canonical stem.
    e.g. "file__2" -> "file", "name 3" -> "name", "script_4" -> "script".
    """
    current = stem
    changed = True
    while changed:
        changed = False
        for pat in COPY_SUFFIX_PATTERNS:
            m = pat.match(current)
            if m:
                current = m.group("base")
                changed = True
                break
    return current


def build_rename_target(path: Path) -> str | None:
    stem = path.stem
    clean = strip_copy_suffix(stem)
    if clean == stem:
        return None
    return f"{clean}{path.suffix}"


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser(description="Review duplicates and rename candidates.")
    parser.add_argument("--root", default=".", help="Root directory to scan.")
    parser.add_argument("--max-depth", type=int, default=1, help="Max directory depth from root (default: 1).")
    parser.add_argument(
        "--report-dir",
        default="reports/dupe_rename_review",
        help="Directory to write CSV reports.",
    )
    parser.add_argument(
        "--apply-renames",
        action="store_true",
        help="Apply only 'ready' rename candidates.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    report_dir = (root / args.report_dir).resolve()

    files = iter_files(root, args.max_depth)
    metas: list[FileMeta] = []
    for p in files:
        rel = str(p.relative_to(root))
        size = p.stat().st_size
        sha = sha256_file(p)
        metas.append(FileMeta(path=p, relpath=rel, size=size, sha256=sha))

    # Duplicate report by hash
    by_hash: dict[str, list[FileMeta]] = defaultdict(list)
    for m in metas:
        by_hash[m.sha256].append(m)

    dup_rows: list[dict] = []
    for sha, group in sorted(by_hash.items(), key=lambda kv: (len(kv[1]) * -1, kv[0])):
        if len(group) < 2:
            continue
        keep = sorted(group, key=lambda x: x.relpath)[0].relpath
        for m in sorted(group, key=lambda x: x.relpath):
            dup_rows.append(
                {
                    "sha256": sha,
                    "size_bytes": m.size,
                    "group_size": len(group),
                    "path": m.relpath,
                    "keep_path": keep,
                    "is_keep": "yes" if m.relpath == keep else "no",
                }
            )

    # Rename candidates
    existing_rel = {m.relpath for m in metas}
    hash_by_rel = {m.relpath: m.sha256 for m in metas}
    rename_rows: list[dict] = []
    ready_moves: list[tuple[Path, Path]] = []

    for m in sorted(metas, key=lambda x: x.relpath):
        target_name = build_rename_target(m.path)
        if not target_name:
            continue
        target_rel = str((Path(m.relpath).parent / target_name).as_posix())
        status = "ready"
        note = ""

        if target_rel == m.relpath:
            status = "skip_no_change"
        elif target_rel in existing_rel:
            # If target exists with same hash, this source is a duplicate name variant.
            if hash_by_rel[target_rel] == m.sha256:
                status = "duplicate_of_existing_target"
                note = "target exists with identical content"
            else:
                status = "collision_target_exists"
                note = "target exists with different content"

        rename_rows.append(
            {
                "old_path": m.relpath,
                "proposed_new_path": target_rel,
                "status": status,
                "note": note,
            }
        )

        if status == "ready":
            ready_moves.append((m.path, root / target_rel))

    # Write reports
    write_csv(
        report_dir / "hash_duplicates.csv",
        dup_rows,
        ["sha256", "size_bytes", "group_size", "path", "keep_path", "is_keep"],
    )
    write_csv(
        report_dir / "rename_candidates.csv",
        rename_rows,
        ["old_path", "proposed_new_path", "status", "note"],
    )

    applied = 0
    if args.apply_renames:
        for src, dst in ready_moves:
            dst.parent.mkdir(parents=True, exist_ok=True)
            src.rename(dst)
            applied += 1

    print(f"Scanned files: {len(metas)}")
    print(f"Duplicate groups: {len({r['sha256'] for r in dup_rows})}")
    print(f"Duplicate file rows: {len(dup_rows)}")
    print(f"Rename candidates: {len(rename_rows)}")
    print(f"Ready renames: {sum(1 for r in rename_rows if r['status'] == 'ready')}")
    print(f"Applied renames: {applied}")
    print(f"Reports: {report_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
