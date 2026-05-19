#!/usr/bin/env python3
"""
Option C - Batch 3 moves (depth > 2) with relocation awareness.

Reads OPTION_C_BEFORE_AFTER.csv and applies:
  - MOVE entries with current_depth > 2
  - ARCHIVE entries with current_depth > 2

Advanced behavior:
  - If source path no longer exists, attempt to resolve it from
    known relocation roots (e.g., super-flat -> archives/migration-staging/super-flat).
  - When destination exists, merge with content-hash conflict handling.
  - Logs all actions to CSV.
"""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path("/Users/steven/AVATARARTS")
CSV_PATH = ROOT / "content/documentation/analysis/ACTIVE/OPTION_C_BEFORE_AFTER.csv"
LOG_PATH = ROOT / "content/documentation/analysis/ACTIVE/OPTION_C_BATCH3_MOVE_LOG.csv"

RELOCATION_MAP = {
    "super-flat": "archives/migration-staging/super-flat",
    "consolidation": "archives/migration-staging/consolidation",
}


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


def resolve_src(rel: str) -> tuple[Path, str]:
    src = ROOT / rel
    if src.exists():
        return src, rel
    for prefix, mapped in RELOCATION_MAP.items():
        if rel == prefix or rel.startswith(f"{prefix}/"):
            remainder = Path(rel).relative_to(prefix)
            alt_rel = Path(mapped) / remainder
            alt_src = ROOT / alt_rel
            if alt_src.exists():
                return alt_src, alt_rel.as_posix()
    return src, rel


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

    if src == dest:
        log_rows.append({
            "action": "SKIP_SAME_PATH",
            "src": str(src),
            "dest": str(dest),
            "detail": "already_in_place",
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
            change_type = row.get("change_type")
            if change_type not in {"MOVE", "ARCHIVE"}:
                continue
            try:
                depth = int(row.get("current_depth", "999"))
            except ValueError:
                continue
            if depth <= 2:
                continue

            src_rel = (row.get("current_path") or "").strip()
            dest_rel = (row.get("proposed_path") or "").strip()
            if not src_rel or not dest_rel:
                continue
            if src_rel == dest_rel:
                continue

            resolved_src, resolved_rel = resolve_src(src_rel)
            if not resolved_src.exists():
                log_rows.append({
                    "action": "SKIP_MISSING",
                    "src": str(ROOT / src_rel),
                    "dest": str(ROOT / dest_rel),
                    "detail": "source_missing_after_relocation",
                })
                continue

            dest = ROOT / dest_rel
            move_or_merge(resolved_src, dest, log_rows)

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
    skipped = sum(1 for r in log_rows if r["action"].startswith("SKIP"))

    print("✅ Option C Batch 3 move complete")
    print(f"Moved items: {moved}")
    print(f"Removed empty dirs: {merged}")
    print(f"Duplicates skipped: {dupes}")
    print(f"Conflicts renamed: {conflicts}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")
    print(f"Log: {LOG_PATH}")


if __name__ == "__main__":
    main()
