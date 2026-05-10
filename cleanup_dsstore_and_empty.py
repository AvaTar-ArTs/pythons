#!/usr/bin/env python3
"""
Remove .DS_Store files and clean empty directories.

- Deletes .DS_Store everywhere under the target root
  (default: /Users/steven).
  - Skips .git/.svn directories for safety.
  - Removes empty directories after cleanup (excluding root).
  - Logs actions to CSV under AVATARARTS analysis docs.
"""

from __future__ import annotations

import csv
from pathlib import Path
from datetime import datetime

ROOT = Path("/Users/steven")
LOG_PATH = Path("/Users/steven/AVATARARTS/content/documentation/analysis/ACTIVE/DSSTORE_EMPTYDIR_CLEANUP_LOG.csv")

SKIP_DIRS = {".git", ".svn"}


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def delete_dsstore(root: Path) -> list[dict]:
    log_rows = []
    for path in root.rglob(".DS_Store"):
        if not path.is_file():
            continue
        if is_skipped(path):
            log_rows.append({
                "action": "SKIP",
                "path": str(path),
                "reason": "inside .git/.svn",
            })
            continue
        try:
            path.unlink()
            log_rows.append({
                "action": "DELETE_DSSTORE",
                "path": str(path),
                "reason": "removed",
            })
        except OSError as exc:
            log_rows.append({
                "action": "ERROR",
                "path": str(path),
                "reason": f"unlink failed: {exc}",
            })
    return log_rows


def remove_empty_dirs(root: Path) -> list[dict]:
    log_rows = []
    # Bottom-up traversal
    for path in sorted(root.rglob("*"), reverse=True):
        if not path.is_dir():
            continue
        if path == root:
            continue
        if is_skipped(path):
            continue
        try:
            if not any(path.iterdir()):
                path.rmdir()
                log_rows.append({
                    "action": "REMOVE_EMPTY_DIR",
                    "path": str(path),
                    "reason": "empty",
                })
        except OSError as exc:
            log_rows.append({
                "action": "ERROR",
                "path": str(path),
                "reason": f"rmdir failed: {exc}",
            })
    return log_rows


def main() -> None:
    log_rows = []
    log_rows.extend(delete_dsstore(ROOT))
    log_rows.extend(remove_empty_dirs(ROOT))

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["action", "path", "reason"],
        )
        writer.writeheader()
        writer.writerows(log_rows)

    deleted = sum(1 for r in log_rows if r["action"] == "DELETE_DSSTORE")
    removed_dirs = sum(1 for r in log_rows if r["action"] == "REMOVE_EMPTY_DIR")
    errors = sum(1 for r in log_rows if r["action"] == "ERROR")

    print("✅ Cleanup complete")
    print(f".DS_Store removed: {deleted}")
    print(f"Empty dirs removed: {removed_dirs}")
    print(f"Errors: {errors}")
    print(f"Log: {LOG_PATH}")
    print(f"Timestamp: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
