"""
Finalrootcleanup

This module provides functionality for finalrootcleanup.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Final Root Directory Cleanup
Organize remaining loose items into context-fluid structure
"""

import shutil
from pathlib import Path
from collections import defaultdict


class FinalRootCleanup:
    """Clean up remaining root directory items"""

    def __init__(self, base_dir: Path):
        """__init__ function."""

        self.base_dir = base_dir

        # Map remaining items to their context-fluid destinations
        self.cleanup_map = {
            # Analysis and mapping files → experiments/analysis_artifacts
            "context_fluid_analysis_20251026_040815.json": "experiments/analysis_artifacts",
            "context_fluid_map_20251026_041243.csv": "experiments/analysis_artifacts",
            "reorganization_map_20251026_035729.csv": "experiments/analysis_artifacts",
            "reorganization_directory_map_20251026_035729.csv": "experiments/analysis_artifacts",
            # Reorganization scripts → experiments/reorganization_tools
            "context_fluid_reorganizer.py": "experiments/reorganization_tools",
            "execute_context_fluid_reorg.py": "experiments/reorganization_tools",
            "create_context_fluid_map.py": "experiments/reorganization_tools",
            "migrate_old_dirs.py": "experiments/reorganization_tools",
            "final_root_cleanup.py": "experiments/reorganization_tools",
            "advanced_directory_consolidation.py": "experiments/reorganization_tools",
            "analyze_claude_dir.py": "experiments/reorganization_tools",
            "categorize_and_reorganize.py": "experiments/reorganization_tools",
            "comprehensive_directory_consolidation.py": "experiments/reorganization_tools",
            "consolidate_directories.py": "experiments/reorganization_tools",
            "create_reorganization_map.py": "experiments/reorganization_tools",
            "enhanced_directory_consolidation.py": "experiments/reorganization_tools",
            "execute_reorganization.py": "experiments/reorganization_tools",
            "intelligent_directory_consolidation.py": "experiments/reorganization_tools",
            "smart_directory_consolidation.py": "experiments/reorganization_tools",
            # Documentation files → DOCUMENTATION/project_docs
            "COMPLETE_TRANSFORMATION_SUMMARY.md": "DOCUMENTATION/project_docs",
            "CONVERSATION_EXPORTER_README.md": "DOCUMENTATION/project_docs",
            "REORGANIZATION_COMPLETE.md": "DOCUMENTATION/project_docs",
            "REORGANIZATION_PHASE_2_COMPLETE.md": "DOCUMENTATION/project_docs",
            "ULTRA_SPECIFIC_REORGANIZATION_COMPLETE.md": "DOCUMENTATION/project_docs",
            # Old directories → _archived_cleanup
            "heads": "_archived_cleanup/old_dirs",
            "info": "_archived_cleanup/old_dirs",
            "installation": "_archived_cleanup/old_dirs",
            "intelligent_articles": "_archived_cleanup/old_dirs",
            "ISSUE_TEMPLATE": "_archived_cleanup/old_dirs",
            "learning": "_archived_cleanup/old_dirs",
            "logs": "_archived_cleanup/old_dirs",
            "mac": "_archived_cleanup/old_dirs",
            "MDs": "_archived_cleanup/old_dirs",
            "medium_articles": "_archived_cleanup/old_dirs",
            "MIGRATION_BACKUP": "_archived_cleanup/old_dirs",
            "photoshop-mockup-automation": "_archived_cleanup/old_dirs",
            "reddit-text-extract": "_archived_cleanup/old_dirs",
            "Reddit-Tiktok-Video-Bot": "_archived_cleanup/old_dirs",
            "selenium_browser_automation": "_archived_cleanup/old_dirs",
            "simple_scraper": "_archived_cleanup/old_dirs",
            "sms": "_archived_cleanup/old_dirs",
            "system_scripts": "_archived_cleanup/old_dirs",
            "test-python-audio": "_archived_cleanup/old_dirs",
            "text-extractor": "_archived_cleanup/old_dirs",
            "tiktok-video-bot": "_archived_cleanup/old_dirs",
            "twitter-scraper": "_archived_cleanup/old_dirs",
            "ui-tools": "_archived_cleanup/old_dirs",
            "uipath-tools": "_archived_cleanup/old_dirs",
            "unique_files": "_archived_cleanup/old_dirs",
            "UserID_scraper": "_archived_cleanup/old_dirs",
            "vin_decoder": "_archived_cleanup/old_dirs",
            "watchdog-automation": "_archived_cleanup/old_dirs",
            "web-tools": "_archived_cleanup/old_dirs",
            "website_downloader": "_archived_cleanup/old_dirs",
            "Whatsapp": "_archived_cleanup/old_dirs",
            "workflow-automation": "_archived_cleanup/old_dirs",
            "youtube-bot": "_archived_cleanup/old_dirs",
            "youtube-generator": "_archived_cleanup/old_dirs",
            "yt_audio_processing": "_archived_cleanup/old_dirs",
            "zoom-background": "_archived_cleanup/old_dirs",
            # Misc files → appropriate locations
            "Claude Conversations.alfredworkflow": "DATA_UTILITIES/legacy_categories/alfred_workflow",
            "test_transcript.json": "experiments/test_data",
            "__init__.py": "_archived_cleanup/misc_files",
        }

    def execute(self, dry_run=True):
        """Execute final cleanup"""

        logger.info("=" * 70)
        logger.info(f"🧹 FINAL ROOT CLEANUP {'(DRY RUN)' if dry_run else '(LIVE)'}")
        logger.info("=" * 70)
        print()

        moved_count = 0
        skipped_count = 0
        error_count = 0

        # Group by destination for cleaner output
        by_destination = defaultdict(list)
        for item, dest in self.cleanup_map.items():
            source = self.base_dir / item
            if source.exists():
                by_destination[dest].append(item)

        for dest, items in sorted(by_destination.items()):
            logger.info(f"📂 {dest}/")

            for item in items:
                source = self.base_dir / item
                target_dir = self.base_dir / dest
                target = target_dir / source.name

                if not source.exists():
                    skipped_count += 1
                    continue

                # Get size info
                try:
                    if source.is_file():
                        size_kb = source.stat().st_size / CONSTANT_1024
                        size_str = f"{size_kb:.1f} KB"
                    else:
                        file_count = len(list(source.rglob("*")))
                        size_str = f"{file_count} items"
                except (OSError, IOError, FileNotFoundError):
                    size_str = "unknown size"

                if dry_run:
                    logger.info(f"   [DRY RUN] {source.name:<50} ({size_str})")
                else:
                    # Create target directory
                    target_dir.mkdir(parents=True, exist_ok=True)

                    # Handle conflicts
                    if target.exists():
                        # Add timestamp to name
                        from datetime import datetime

                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        if source.is_file():
                            new_name = f"{source.stem}_{timestamp}{source.suffix}"
                        else:
                            new_name = f"{source.name}_{timestamp}"
                        target = target_dir / new_name

                    # Move
                    try:
                        shutil.move(str(source), str(target))
                        logger.info(f"   ✅ {source.name:<50} ({size_str})")
                        moved_count += 1
                    except Exception as e:
                        logger.info(f"   ❌ {source.name:<50} ERROR: {e}")
                        error_count += 1

            print()

        logger.info("=" * 70)
        logger.info(f"{'Simulation' if dry_run else 'Cleanup'} complete!")
        logger.info(f"   Items {'would be' if dry_run else ''} moved: {moved_count}")
        if skipped_count > 0:
            logger.info(f"   Already organized: {skipped_count}")
        if error_count > 0:
            logger.info(f"   Errors: {error_count}")
        logger.info("=" * 70)

        if dry_run:
            logger.info("\n💡 To execute, run:")
            logger.info("   python3 final_root_cleanup.py --execute")
        else:
            logger.info("\n✨ Root directory cleanup complete!")
            logger.info(f"   Check: ls -la {self.base_dir}/")


def main():
    """main function."""

    import sys

    base_dir = Path(Path("/Users/steven/Documents/python"))
    dry_run = "--execute" not in sys.argv

    cleanup = FinalRootCleanup(base_dir)
    cleanup.execute(dry_run=dry_run)


if __name__ == "__main__":
    main()
