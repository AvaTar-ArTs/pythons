"""
Utilities File Operations Remove 1

This module provides functionality for utilities file operations remove 1.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Remove timestamp suffixes from filenames
Pattern: filename_YYYYMMDD_HHMMSS.ext -> filename.ext
"""

import os
import re
import subprocess
from pathlib import Path
from collections import defaultdict


def is_git_tracked(filepath):
    """Check if file is tracked by git"""
    try:
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", filepath], capture_output=True, text=True, cwd=Path(filepath).parent
        )
        return result.returncode == 0
    except (OSError, IOError, FileNotFoundError):
        return False


def get_timestamp_from_filename(filename):
    """Extract timestamp from filename for comparison"""
    match = re.search(r"_(\d{8}_\d{6})", filename)
    if match:
        return match.group(1)
    return None


def remove_timestamp_suffix(filepath):
    """Remove _YYYYMMDD_HHMMSS pattern from filename"""
    path = Path(filepath)
    filename = path.name

    # Pattern: _YYYYMMDD_HHMMSS before extension
    pattern = r"_\d{8}_\d{6}"
    new_filename = re.sub(pattern, "", filename)

    if new_filename != filename:
        new_path = path.parent / new_filename
        return new_path
    return None


def main():
    """main function."""

    # Find all files with timestamp pattern
    project_root = Path("/Users/steven/Documents/python")
    pattern = re.compile(r".*_\d{8}_\d{6}.*")

    timestamped_files = []
    for filepath in project_root.rglob("*"):
        if filepath.is_file() and pattern.match(filepath.name):
            # Skip .git directory
            if ".git" in filepath.parts:
                continue
            timestamped_files.append(filepath)

    logger.info(f"Found {len(timestamped_files)} files with timestamps")

    # Group files by their base name (without timestamp)
    grouped = defaultdict(list)
    for filepath in timestamped_files:
        base_path = remove_timestamp_suffix(filepath)
        if base_path:
            grouped[str(base_path)].append(filepath)

    logger.info(f"\nWill consolidate to {len(grouped)} unique filenames\n")

    renamed_count = 0
    for target_path_str, source_files in grouped.items():
        if not source_files:
            continue

        # Sort by timestamp to keep the most recent
        source_files.sort(key=lambda p: get_timestamp_from_filename(p.name) or "", reverse=True)
        most_recent = source_files[0]
        target_path = Path(target_path_str)

        # Check if target already exists and is not one of our source files
        if target_path.exists() and target_path not in source_files:
            logger.info(f"⚠️  Skipping {most_recent.name} -> {target_path.name} (target exists)")
            continue

        # Delete older versions
        for old_file in source_files[1:]:
            try:
                if is_git_tracked(str(old_file)):
                    subprocess.run(["git", "rm", "-f", str(old_file)], check=True)
                    logger.info(f"🗑️  Deleted old: {old_file.name}")
                else:
                    old_file.unlink()
                    logger.info(f"🗑️  Deleted old: {old_file.name}")
            except Exception as e:
                logger.info(f"❌ Error deleting {old_file}: {e}")

        # Rename the most recent file
        try:
            if most_recent == target_path:
                logger.info(f"✓  Already named correctly: {target_path.name}")
                continue

            if is_git_tracked(str(most_recent)):
                subprocess.run(["git", "mv", str(most_recent), str(target_path)], check=True)
                logger.info(f"✅ Renamed (git): {most_recent.name} -> {target_path.name}")
            else:
                most_recent.rename(target_path)
                logger.info(f"✅ Renamed: {most_recent.name} -> {target_path.name}")
            renamed_count += 1
        except Exception as e:
            logger.info(f"❌ Error renaming {most_recent}: {e}")

    logger.info(f"\n✅ Successfully renamed {renamed_count} files")


if __name__ == "__main__":
    main()
