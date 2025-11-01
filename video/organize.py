"""
Organize 6

This module provides functionality for organize 6.

Author: Auto-generated
Date: 2025-11-01
"""

#!/usr/bin/env python3
from pathlib import Path
import os
import shutil
import argparse

import logging

logger = logging.getLogger(__name__)


# ── CONFIG ─────────────────────────────────────────────────────────────────────

# Project root (where mp3/, mp4/, txt/ live, plus other folders we ignore)
PROJECT_ROOT = Path("/Users/steven/Movies/project2025/Media")

# Relative subdirectories to scan (ignore everything else):
SCAN_DIRS = {
    ".mp4": "mp4",
    ".mp3": "mp3",
    "_analysis.txt": "txt",
    "_transcript.txt": "txt",
}


# ── HELPERS ─────────────────────────────────────────────────────────────────────


def find_all_candidates(root: str):
    """
    Walk through each SCAN_DIRS[subdir], find files whose name ends with
    any of the keys in SCAN_DIRS. Return a list of tuples:
      (absolute_path, base_name, suffix)
    """
    candidates = []
    for suffix, subdir in SCAN_DIRS.items():
        folder = os.path.join(root, subdir)
        if not os.path.isdir(folder):
            # If mp4/ or mp3/ or txt/ doesn’t exist, skip
            continue

        for fname in os.listdir(folder):
            if not fname.endswith(suffix):
                continue
            fullpath = os.path.join(folder, fname)

            if not os.path.isfile(fullpath):
                continue

            base = fname[: -len(suffix)]
            # If stripping leaves an empty string, skip it
            if base.strip() == "":
                continue

            candidates.append((fullpath, base, suffix))
    return candidates


def ensure_folder(path: str):
    """Create path if it doesn’t exist."""
    os.makedirs(path, exist_ok=True)


def move_file(src: str, dst: str, dry_run: bool):
    """
    Create parent folder for dst if needed. Then:
      • If dst already exists: print “skipped” and return False
      • If dry_run: just print what would move, return True
      • Else: actually move src→dst, return True or False if error
    """
    ensure_folder(os.path.dirname(dst))
    if os.path.exists(dst):
        logger.info(f"    ⚠️ Skipped (already in place): {dst}")
        return False

    if dry_run:
        logger.info(f"    [DRY RUN] Would move: {src} → {dst}")
        return True

    try:
        shutil.move(src, dst)
        logger.info(f"    ✅ Moved: {src} → {dst}")
        return True
    except Exception as e:
        logger.info(f"    ❌ Error moving '{src}' → '{dst}': {e}")
        return False


# ── MAIN ORGANIZATION ───────────────────────────────────────────────────────────


def organize_subdirs(root: str, dry_run: bool):
    """
    1) Gather all .mp4/.mp3/_analysis.txt/_transcript.txt from their
       respective subfolders (mp4/, mp3/, txt/).
    2) Group by base name.
    3) For each base, create PROJECT_ROOT/<base>/ if missing.
    4) Move each matching file into that new folder.
    """
    candidates = find_all_candidates(root)
    if not candidates:
        logger.info(f"⚠️ No matching files found under {root}/{{mp4,mp3,txt}}")
        return

    # Group by base_name
    albums = {}
    for fullpath, base, suffix in candidates:
        albums.setdefault(base, []).append((fullpath, suffix))

    total_albums = len(albums)
    total_files = len(candidates)
    logger.info(f"🔍 Found {total_albums} unique base(s) and {total_files} total file(s).\n")

    moved = 0
    skipped = 0

    for idx, (base, items) in enumerate(albums.items(), start=1):
        target_folder = os.path.join(root, base)
        logger.info(f"[{idx}/{total_albums}] Base: '{base}' → Folder: '{base}/'")

        # 1) Create folder for this base if missing
        if not os.path.isdir(target_folder):
            try:
                os.makedirs(target_folder)
                logger.info(f"    ✅ Created folder: {target_folder}")
            except Exception as e:
                logger.info(f"    ❌ Could not create {target_folder}: {e}")
                continue
        else:
            logger.info(f"    ℹ️ Folder already exists: {target_folder}")

        # 2) Move each matched file into that folder
        for src_path, suffix in items:
            fname = os.path.basename(src_path)
            dst_path = os.path.join(target_folder, fname)

            # If the file is already in the correct folder, skip
            if os.path.abspath(src_path) == os.path.abspath(dst_path):
                logger.info(f"    ⚠️ Already in place: {fname}")
                skipped += 1
                continue

            ok = move_file(src_path, dst_path, dry_run)
            if ok:
                moved += 1
            else:
                skipped += 1

        logger.info("")  # blank line between bases

    # Summary
    logger.info("────────────────────────────────────────")
    logger.info(f"✅ Done. Files moved: {moved}, skipped: {skipped}")
    if dry_run:
        logger.info("    (dry-run: no actual moves performed)")
    logger.info("────────────────────────────────────────\n")


# ── ENTRY POINT ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scan mp4/, mp3/, and txt/ subfolders under project2025, "
        "then group each set of files sharing the same base name "
        "into project2025/<BaseName>/."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without moving any files.",
    )
    args = parser.parse_args()

    organize_subdirs(PROJECT_ROOT, dry_run=args.dry_run)
