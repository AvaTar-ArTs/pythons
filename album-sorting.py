"""
Album Sorting

This module provides functionality for album sorting.

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


# ── CONFIGURATION ──────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(str(Path.home()) + "/Movies/PROJECt2025-DoMinIon/Media")
DIRECTORIES = {
    ".mp4": os.path.join(PROJECT_ROOT, "mp4"),
    ".mp3": os.path.join(PROJECT_ROOT, "mp3"),
    "_analysis.txt": os.path.join(PROJECT_ROOT, "txt"),
    "_transcript.txt": os.path.join(PROJECT_ROOT, "txt"),
}

# ── HELPER FUNCTIONS ───────────────────────────────────────────────────────────


def list_bases(directory, suffix):
    """Return a sorted list of base names for files with the given suffix in the directory."""
    if not os.path.isdir(directory):
        logger.info(f"❌ Directory not found: {directory!r}")
        return []
    return sorted(
        fname[: -len(suffix)]
        for fname in os.listdir(directory)
        if fname.lower().endswith(suffix) and fname[: -len(suffix)].strip()
    )


def ensure_folder(path):
    """Create the folder (and any parents) if it doesn’t exist."""
    os.makedirs(path, exist_ok=True)


def move_if_exists(src, dst, dry_run=False):
    """Move src to dst if it exists, creating parent folders as needed."""
    if not os.path.isfile(src):
        return False

    ensure_folder(os.path.dirname(dst))
    if os.path.exists(dst):
        logger.info(f"    ⚠️  Skipped (already exists): {dst}")
        return False

    if dry_run:
        logger.info(f"    [DRY RUN] Would move: {src} → {dst}")
        return True

    try:
        shutil.move(src, dst)
        logger.info(f"    ✅ Moved: {src} → {dst}")
        return True
    except Exception as e:
        logger.info(f"    ❌ Error moving {src!r} → {dst!r}: {e}")
        return False


# ── MAIN LOGIC ─────────────────────────────────────────────────────────────────


def analyze_organization(dry_run=False):
    """analyze_organization function."""

    bases = list_bases(DIRECTORIES[".mp4"], ".mp4")
    if not bases:
        logger.info("⚠️  No .mp4 files found in 'mp4/'. Nothing to do.")
        return

    total_bases = len(bases)
    logger.info(f"🔍 Found {total_bases} .mp4 base(s) in '{DIRECTORIES['.mp4']}'.\n")

    moved_files, skipped_files = 0, 0

    for idx, base in enumerate(bases, start=1):
        folder_path = os.path.join(PROJECT_ROOT, base)
        logger.info(
            f"[{idx}/{total_bases}] Analyzing base: '{base}' → folder: '{base}/'"
        )

        if not os.path.isdir(folder_path):
            try:
                os.makedirs(folder_path)
                logger.info(f"    ✅ Created folder: {folder_path}")
            except Exception as e:
                logger.info(f"    ❌ Could not create '{folder_path}': {e}")
                continue
        else:
            logger.info(f"    ℹ️  Folder already exists: {folder_path}")

        for ext in DIRECTORIES.keys():
            src = os.path.join(DIRECTORIES[ext], base + ext)
            dst = os.path.join(folder_path, base + ext)
            if os.path.abspath(src) == os.path.abspath(dst):
                logger.info(f"    ⚠️  Already in place: {src}")
                skipped_files += 1
            else:
                if move_if_exists(src, dst, dry_run):
                    moved_files += 1
                else:
                    skipped_files += 1

        logger.info("")  # blank line between bases

    logger.info("────────────────────────────────────────")
    print(
        f"✅ Analysis completed. Files moved: {moved_files}, skipped/missing: {skipped_files}"
    )
    if dry_run:
        logger.info("    (dry-run mode: no files were actually moved)")
    logger.info("────────────────────────────────────────")


# ── ENTRY POINT ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze file organization by moving each .mp4 and its related files into a dedicated folder."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the file organization without making any changes.",
    )
    args = parser.parse_args()

    analyze_organization(dry_run=args.dry_run)
