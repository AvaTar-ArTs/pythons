#!/usr/bin/env python3
"""
Option C - Batch 2 moves (core structure).

Moves or merges selected directories based on the Option C CSV:
  - MOVE entries with current_depth <= 2
  - Source/target paths are relative to /Users/steven/AVATARARTS

Behavior:
  - If destination does not exist: move source directory
  - If destination exists: merge contents
    - File conflicts resolved by content hash:
      - Same content: skip duplicate
      - Different content: rename with hash suffix
  - Logs all actions to CSV
"""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path("/Users/steven/AVATARARTS")
CSV_PATH = ROOT / "content/documentation/analysis/ACTIVE/OPTION_C_BEFORE_AFTER.csv"
LOG_PATH = ROOT / "content/documentation/analysis/ACTIVE/OPTION_C_BATCH2_MOVE_LOG.csv"


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def unique_name(dest: Path, suffix: str) -> Path:
    if dest.suffix:
        return dest.with_name(f"{dest.stem}{suffix}{dest.suffix}")
    return dest.with_name(f"{dest.name}{suffix}")


def merge_dir(src: Path, dest: Path, log_rows: list[dict]) -> None:
    ensure_dir(dest)
    for item in src.iterdir():
        target = dest / item.name
        try:
            if item.is_dir():
                if target.exists() and target.is_dir():
                    merge_dir(item, target, log_rows)
                    if not any(item.iterdir()):
                        item.rmdir()
                        log_rows.append({
                            "action": "REMOVE_EMPTY_DIR",
                            "src": str(item),
                            "dest": str(target),
                            "detail": "merged_dir",
                        })
                else:
                    item.rename(target)
                    log_rows.append({
                        "action": "MOVE_DIR",
                        "src": str(item),
                        "dest": str(target),
                        "detail": "moved_dir",
                    })
            else:
                if not target.exists():
                    item.rename(target)
                    log_rows.append({
                        "action": "MOVE_FILE",
                        "src": str(item),
                        "dest": str(target),
                        "detail": "moved_file",
                    })
                else:
                    src_hash = sha256_file(item)
                    dest_hash = sha256_file(target)
                    if src_hash == dest_hash:
                        item.unlink()
                        log_rows.append({
                            "action": "DUPLICATE_SKIPPED",
                            "src": str(item),
                            "dest": str(target),
                            "detail": "same_hash",
                        })
                    else:
                        suffix = f"__conflict_{src_hash[:8]}"
                        new_target = unique_name(target, suffix)
                        item.rename(new_target)
                        log_rows.append({
                            "action": "RENAME_CONFLICT",
                            "src": str(item),
                            "dest": str(new_target),
                            "detail": "different_hash",
                        })
        except OSError as exc:
            log_rows.append({
                "action": "ERROR",
                "src": str(item),
                "dest": str(target),
                "detail": f"{type(exc).__name__}: {exc}",
            })


def move_or_merge(src: Path, dest: Path, log_rows: list[dict]) -> None:
    if not src.exists():
        log_rows.append({
            "action": "SKIP_MISSING",
            "src": str(src),
            "dest": str(dest),
            "detail": "source_missing",
        })
        return

    if not dest.exists():
        ensure_dir(dest.parent)
        try:
            src.rename(dest)
            log_rows.append({
                "action": "MOVE_DIR",
                "src": str(src),
                "dest": str(dest),
                "detail": "moved_root_dir",
            })
        except OSError as exc:
            log_rows.append({
                "action": "ERROR",
                "src": str(src),
                "dest": str(dest),
                "detail": f"{type(exc).__name__}: {exc}",
            })
        return

    if dest.is_dir():
        merge_dir(src, dest, log_rows)
        if src.exists() and src.is_dir() and not any(src.iterdir()):
            try:
                src.rmdir()
                log_rows.append({
                    "action": "REMOVE_EMPTY_DIR",
                    "src": str(src),
                    "dest": str(dest),
                    "detail": "source_empty_after_merge",
                })
            except OSError as exc:
                log_rows.append({
                    "action": "ERROR",
                    "src": str(src),
                    "dest": str(dest),
                    "detail": f"{type(exc).__name__}: {exc}",
                })
    else:
        log_rows.append({
            "action": "ERROR",
            "src": str(src),
            "dest": str(dest),
            "detail": "destination_is_file",
        })


def main() -> None:
    if not CSV_PATH.exists():
        raise SystemExit(f"Missing CSV: {CSV_PATH}")

    log_rows: list[dict] = []
    with CSV_PATH.open("r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("change_type") != "MOVE":
                continue
            try:
                depth = int(row.get("current_depth", "999"))
            except ValueError:
                continue
            if depth > 2:
                continue

            src_rel = row.get("current_path", "").strip()
            dest_rel = row.get("proposed_path", "").strip()
            if not src_rel or not dest_rel:
                continue
            if src_rel == dest_rel:
                continue

            src = ROOT / src_rel
            dest = ROOT / dest_rel
            move_or_merge(src, dest, log_rows)

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["action", "src", "dest", "detail"],
        )
        writer.writeheader()
        writer.writerows(log_rows)

    moved = sum(1 for r in log_rows if r["action"] in {"MOVE_DIR", "MOVE_FILE"})
    merged = sum(1 for r in log_rows if r["action"] == "REMOVE_EMPTY_DIR")
    dupes = sum(1 for r in log_rows if r["action"] == "DUPLICATE_SKIPPED")
    conflicts = sum(1 for r in log_rows if r["action"] == "RENAME_CONFLICT")
    errors = sum(1 for r in log_rows if r["action"] == "ERROR")
    skipped = sum(1 for r in log_rows if r["action"] == "SKIP_MISSING")

    print("✅ Option C Batch 2 move complete")
    print(f"Moved items: {moved}")
    print(f"Removed empty dirs: {merged}")
    print(f"Duplicates skipped: {dupes}")
    print(f"Conflicts renamed: {conflicts}")
    print(f"Skipped (missing): {skipped}")
    print(f"Errors: {errors}")
    print(f"Log: {LOG_PATH}")


if __name__ == "__main__":
    main()
