#!/usr/bin/env python3
"""Preview-first image normalization with recoverable original backups."""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, UnidentifiedImageError

try:
    from exclude_patterns import FULL_EXCLUDED_PATTERNS
except ImportError:
    FULL_EXCLUDED_PATTERNS = []


MAX_WIDTH, MAX_HEIGHT = 4500, 5400
MIN_FILE_SIZE_BYTES = 8 * 1024 * 1024
SUPPORTED = {".jpg", ".jpeg", ".png"}


def excluded(path: Path) -> bool:
    text = str(path)
    return any(re.match(pattern, text) for pattern in FULL_EXCLUDED_PATTERNS)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def target_dimensions(width: int, height: int) -> tuple[int, int]:
    ratio = width / height
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        scale = min(MAX_WIDTH / width, MAX_HEIGHT / height)
        return max(1, int(width * scale)), max(1, int(height * scale))
    return width, height


def iter_candidates(root: Path):
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        dirs[:] = [d for d in dirs if not excluded(current_path / d)]
        for name in files:
            path = current_path / name
            if path.suffix.lower() in SUPPORTED and path.stat().st_size >= MIN_FILE_SIZE_BYTES and not excluded(path):
                yield path


def process(path: Path, backup_root: Path, apply: bool) -> dict[str, str]:
    before_size = path.stat().st_size
    before_hash = digest(path)
    row = {
        "before": str(path),
        "staging": str(path.with_name(f"300dpi_{path.name}")),
        "before_bytes": str(before_size),
        "before_sha256": before_hash,
        "after_bytes": "",
        "after_sha256": "",
        "backup": "",
        "status": "preview",
        "error": "",
    }
    staging = Path(row["staging"])
    try:
        with Image.open(path) as image:
            new_size = target_dimensions(*image.size)
            if staging.exists():
                row["status"] = "skipped-staging-exists"
                return row
            output = image.resize(new_size, Image.Resampling.LANCZOS) if new_size != image.size else image.copy()
            save_kwargs = {"dpi": (300, 300)}
            if path.suffix.lower() in {".jpg", ".jpeg"}:
                save_kwargs.update(quality=85, optimize=True)
            else:
                save_kwargs.update(optimize=True)
            output.save(staging, **save_kwargs)
            output.close()
        with Image.open(staging) as check:
            check.verify()
        if not apply:
            staging.unlink()
            return row
        backup_root.mkdir(parents=True, exist_ok=True)
        backup = backup_root / path.name
        counter = 1
        while backup.exists():
            backup = backup_root / f"{path.stem}-{counter}{path.suffix}"
            counter += 1
        shutil.copy2(path, backup)
        row["backup"] = str(backup)
        os.replace(staging, path)
        row["after_bytes"] = str(path.stat().st_size)
        row["after_sha256"] = digest(path)
        row["status"] = "applied"
    except (OSError, UnidentifiedImageError, ValueError) as exc:
        row["status"] = "error"
        row["error"] = str(exc)
        if staging.exists():
            staging.unlink(missing_ok=True)
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_directory", type=Path)
    parser.add_argument("--output", type=Path, default=Path(tempfile.gettempdir()) / "resize-preview.csv")
    parser.add_argument("--apply", action="store_true", help="Apply after preview review")
    parser.add_argument("--backup-dir", type=Path, help="Directory for recoverable originals")
    args = parser.parse_args()
    root = args.source_directory.expanduser().resolve()
    if not root.is_dir():
        parser.error(f"source directory does not exist: {root}")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    backup = (args.backup_dir or Path(tempfile.gettempdir()) / f"resize-originals-{stamp}").resolve()
    rows = [process(path, backup, args.apply) for path in iter_candidates(root)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = ["before", "staging", "before_bytes", "before_sha256", "after_bytes", "after_sha256", "backup", "status", "error"]
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Preview written: {args.output} | candidates: {len(rows)} | mode: {'apply' if args.apply else 'preview-only'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
