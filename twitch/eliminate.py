"""
Eliminate

This module provides functionality for eliminate.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Eliminate Archive Directories
Move all items from _archived_cleanup and _organized_root_files
into proper context-fluid categories
"""

import shutil
from pathlib import Path
from collections import defaultdict


class ArchiveEliminator:
    """Eliminate archive directories by properly categorizing contents"""

    def __init__(self, base_dir: Path):
        """__init__ function."""

        self.base_dir = base_dir
        self.archive_dirs = ["_archived_cleanup", "_organized_root_files"]

    def analyze_item(self, item_path: Path):
        """Intelligently categorize an item based on name and content"""

        name_lower = item_path.name.lower()

        # Bot/Automation patterns
        if any(
            word in name_lower
            for word in [
                "bot",
                "automation",
                "scraper",
                "scrape",
                "instagram",
                "reddit",
                "twitter",
                "telegram",
                "youtube",
                "tiktok",
                "twitch",
                "whatsapp",
            ]
        ):
            return "AUTOMATION_BOTS/legacy_categories"

        # Media processing patterns
        if any(
            word in name_lower
            for word in [
                "video",
                "audio",
                "image",
                "mp3",
                "mp4",
                "media",
                "music",
                "spotify",
                "voice",
                "sound",
                "transcribe",
                "subtitle",
                "ocr",
            ]
        ):
            return "MEDIA_PROCESSING/legacy_categories"

        # AI/ML patterns
        if any(
            word in name_lower
            for word in [
                "ai",
                "ml",
                "machine-learning",
                "chatbot",
                "gpt",
                "llm",
                "neural",
                "model",
                "train",
            ]
        ):
            return "AI_CONTENT/legacy_categories"

        # Data/Utility patterns
        if any(
            word in name_lower
            for word in [
                "csv",
                "json",
                "excel",
                "pdf",
                "data",
                "database",
                "sql",
                "file",
                "backup",
                "monitor",
                "tool",
                "utility",
                "converter",
                "processor",
                "analyzer",
                "extractor",
                "downloader",
                "organizer",
            ]
        ):
            return "DATA_UTILITIES/legacy_categories"

        # Documentation patterns
        if any(
            word in name_lower
            for word in [
                "doc",
                "docs",
                "documentation",
                "readme",
                "guide",
                "tutorial",
                "example",
                "article",
                "notes",
            ]
        ):
            return "DOCUMENTATION/legacy_categories"

        # Development/Test patterns
        if any(
            word in name_lower
            for word in ["test", "example", "experimental", "temp", "tmp"]
        ):
            return "experiments/archived_items"

        # Default to DATA_UTILITIES for unclear items
        return "DATA_UTILITIES/legacy_categories"

    def get_all_items_from_archives(self):
        """Get all items from archive directories"""
        items = []

        for archive_dir in self.archive_dirs:
            archive_path = self.base_dir / archive_dir
            if not archive_path.exists():
                continue

            # Get all top-level items in archive
            for item in archive_path.iterdir():
                if not item.name.startswith("."):
                    items.append((archive_dir, item))

        return items

    def execute(self, dry_run=True):
        """Execute archive elimination"""

        logger.info("=" * 70)
        logger.info(f"🗑️  ELIMINATE ARCHIVES {'(DRY RUN)' if dry_run else '(LIVE)'}")
        logger.info("=" * 70)
        print()

        items = self.get_all_items_from_archives()

        if not items:
            logger.info("✅ No archive directories found or they're already empty!")
            return

        logger.info(f"Found {len(items)} items in archive directories")
        print()

        moved_count = 0
        error_count = 0

        # Group by destination
        by_destination = defaultdict(list)
        for archive_name, item_path in items:
            destination = self.analyze_item(item_path)
            by_destination[destination].append((archive_name, item_path))

        for dest, item_list in sorted(by_destination.items()):
            logger.info(f"📂 {dest}/")

            for archive_name, item_path in item_list:
                # Get size info
                try:
                    if item_path.is_file():
                        size_kb = item_path.stat().st_size / CONSTANT_1024
                        size_str = f"{size_kb:.1f} KB"
                    else:
                        try:
                            file_count = len(list(item_path.rglob("*")))
                            size_str = f"{file_count} items"
                        except (OSError, IOError, FileNotFoundError):
                            size_str = "dir"
                except (OSError, IOError, FileNotFoundError):
                    size_str = "unknown"

                target_dir = self.base_dir / dest
                target = target_dir / item_path.name

                if dry_run:
                    logger.info(f"   [DRY RUN] {item_path.name:<45} ({size_str})")
                else:
                    # Create target directory
                    target_dir.mkdir(parents=True, exist_ok=True)

                    # Handle conflicts
                    if target.exists():
                        from datetime import datetime

                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        if item_path.is_file():
                            new_name = f"{item_path.stem}_{timestamp}{item_path.suffix}"
                        else:
                            new_name = f"{item_path.name}_{timestamp}"
                        target = target_dir / new_name

                    # Move
                    try:
                        shutil.move(str(item_path), str(target))
                        logger.info(f"   ✅ {item_path.name:<45} ({size_str})")
                        moved_count += 1
                    except Exception as e:
                        logger.info(f"   ❌ {item_path.name:<45} ERROR: {str(e)[:30]}")
                        error_count += 1

            print()

        logger.info("=" * 70)
        logger.info(f"{'Simulation' if dry_run else 'Elimination'} complete!")
        logger.info(f"   Items {'would be' if dry_run else ''} moved: {moved_count}")
        if error_count > 0:
            logger.info(f"   Errors: {error_count}")
        logger.info("=" * 70)

        if not dry_run:
            # Remove empty archive directories
            print()
            logger.info("🗑️  Removing empty archive directories...")
            for archive_dir in self.archive_dirs:
                archive_path = self.base_dir / archive_dir
                if archive_path.exists():
                    try:
                        # Remove empty subdirectories
                        for item in sorted(archive_path.rglob("*"), reverse=True):
                            if item.is_dir() and not any(item.iterdir()):
                                item.rmdir()

                        # Remove archive directory if empty
                        if not any(archive_path.iterdir()):
                            archive_path.rmdir()
                            logger.info(f"   ✅ Removed: {archive_dir}/")
                        else:
                            remaining = len(list(archive_path.rglob("*")))
                            logger.info(
                                f"   ⚠️  {archive_dir}/ still has {remaining} items"
                            )
                    except Exception as e:
                        logger.info(f"   ❌ Error removing {archive_dir}/: {e}")

            print()
            logger.info("✨ Archives eliminated! All items properly categorized.")

        if dry_run:
            logger.info("\n💡 To execute, run:")
            logger.info("   python3 eliminate_archives.py --execute")


def main():
    """main function."""

    import sys

    base_dir = Path(Path(str(Path.home()) + "/Documents/python"))
    dry_run = "--execute" not in sys.argv

    eliminator = ArchiveEliminator(base_dir)
    eliminator.execute(dry_run=dry_run)


if __name__ == "__main__":
    main()
