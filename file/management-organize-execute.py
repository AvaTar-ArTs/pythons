"""
File Management Organize Execute 7

This module provides functionality for file management organize execute 7.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Execute Ultra-Specific Functional Reorganization
Move files from broad categories to ultra-specific action-based categories
"""

import json
import shutil
from pathlib import Path
from datetime import datetime


def execute_reorganization(analysis_file: Path, dry_run: bool = True):
    """Execute the ultra-specific reorganization"""

    with open(analysis_file) as f:
        analysis = json.load(f)

    base_dir = Path(analysis["directory"])

    logger.info(f"🚀 Ultra-Specific Functional Reorganization")
    logger.info(f"   Mode: {'DRY RUN' if dry_run else 'LIVE EXECUTION'}")
    logger.info(f"   Categories: {analysis['total_categories']}")
    logger.info(f"   Files to move: {analysis['total_files_categorized']}")
    print()

    moved_count = 0
    skipped_count = 0
    error_count = 0

    for category_name, category_data in analysis["categories"].items():
        category_path = base_dir / category_name

        # Create category directory
        if not dry_run:
            category_path.mkdir(parents=True, exist_ok=True)

        logger.info(f"📁 {category_name}/ ({category_data['count']} files)")

        for file_rel_path in category_data["files"]:
            source_path = base_dir / file_rel_path
            dest_path = category_path / source_path.name

            if not source_path.exists():
                logger.info(f"   ⚠️  Source not found: {source_path.name}")
                skipped_count += 1
                continue

            if dest_path.exists():
                logger.info(f"   ⏭️  Already exists: {source_path.name}")
                skipped_count += 1
                continue

            if dry_run:
                logger.info(f"   [DRY RUN] Would move: {source_path.name}")
            else:
                try:
                    shutil.move(str(source_path), str(dest_path))
                    logger.info(f"   ✅ Moved: {source_path.name}")
                except Exception as e:
                    logger.info(f"   ❌ Error: {source_path.name} - {e}")
                    error_count += 1
                    continue

            moved_count += 1

    print()
    logger.info("=" * 60)
    logger.info(f"{'DRY RUN ' if dry_run else ''}Complete!")
    logger.info(f"   Files {'would be ' if dry_run else ''}moved: {moved_count}")
    logger.info(f"   Skipped: {skipped_count}")
    if error_count > 0:
        logger.info(f"   Errors: {error_count}")

    if dry_run:
        logger.info("\n💡 To execute for real, run:")
        logger.info(f"   python3 execute_ultra_specific_reorg.py --execute")


def main():
    """main function."""

    import sys

    base_dir = Path.cwd()

    # Find most recent analysis file
    analyses = list(base_dir.glob("ultra_specific_analysis_*.json"))
    if not analyses:
        logger.info("❌ No ultra_specific_analysis_*.json file found")
        logger.info("   Run ultra_specific_categorizer.py first")
        return

    analysis_file = max(analyses, key=lambda p: p.stat().st_mtime)
    logger.info(f"📄 Using analysis: {analysis_file.name}\n")

    # Check if --execute flag provided
    dry_run = "--execute" not in sys.argv

    execute_reorganization(analysis_file, dry_run=dry_run)


if __name__ == "__main__":
    main()
