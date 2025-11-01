"""
Directoryorganizer

This module provides functionality for directoryorganizer.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Directory Organizer
Organizes all directories at depth 6+ and moves them to ~/Documents/python
"""

import os
import re
import shutil
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class DirectoryOrganizer:
    """Organizes directories and moves them to proper locations."""

    def __init__(self):
        """__init__ function."""

        self.root_path = Path(Path("/Users/steven/Documents/python")).expanduser()
        self.max_depth = 10
        self.target_python_dir = Path(Path("/Users/steven/Documents/python"))

        # File type organization
        self.file_type_dirs = {
            ".html": Path(Path("/Users/steven/Documents/html")),
            ".md": Path(Path("/Users/steven/Documents/markdown")),
            ".csv": Path(Path("/Users/steven/Documents/csv")),
            ".pdf": Path(Path("/Users/steven/Documents/pdf")),
            ".json": Path(Path("/Users/steven/Documents/json")),
            ".txt": Path(Path("/Users/steven/Documents/text")),
            ".log": Path(Path("/Users/steven/Documents/logs")),
            ".png": Path(Path("/Users/steven/Documents/images")),
            ".jpg": Path(Path("/Users/steven/Documents/images")),
            ".jpeg": Path(Path("/Users/steven/Documents/images")),
            ".gif": Path(Path("/Users/steven/Documents/images")),
            ".svg": Path(Path("/Users/steven/Documents/images")),
            ".mp4": Path(Path("/Users/steven/Documents/videos")),
            ".mov": Path(Path("/Users/steven/Documents/videos")),
            ".avi": Path(Path("/Users/steven/Documents/videos")),
            ".zip": Path(Path("/Users/steven/Documents/archives")),
            ".tar": Path(Path("/Users/steven/Documents/archives")),
            ".gz": Path(Path("/Users/steven/Documents/archives")),
            ".exe": Path(Path("/Users/steven/Documents/executables")),
            ".dmg": Path(Path("/Users/steven/Documents/executables")),
            ".pkg": Path(Path("/Users/steven/Documents/executables")),
        }

        # Track all changes for CSV
        self.changes = []

    def clean_directory_name(self, dir_name):
        """Clean directory name by removing junk patterns."""
        # Remove common junk patterns
        junk_patterns = [
            r"_\d{8}_\d{6}",  # _20251028_021746
            r"_\d{8}",  # _20251028
            r"_\d{6}",  # _021746
            r"_\d{4}-\d{2}-\d{2}",  # _2025-10-28
            r"^documentation_documentation_documentation_",
            r"^documentation_documentation_",
            r"^documentation_",
            r"^web_resources_",
            r"^pydoc_html_",
            r"^html-generator_",
            r"^doc-generator_output_",
            r"^legacy_categories_",
            r"^archived_",
            r"^backups_",
            r"^carbons_",
            r"_[a-f0-9]{8,}$",  # _a1a7b7066bc54
            r"_from_\w+$",  # _from_csv-processor
            r"_from_\w+_\d+$",  # _from_csv-processor_1
            r"_temp$",
            r"_tmp$",
            r"_backup$",
            r"_old$",
            r"_copy$",
        ]

        cleaned_name = dir_name
        for pattern in junk_patterns:
            cleaned_name = re.sub(pattern, "", cleaned_name)

        # Clean up spaces and special chars
        cleaned_name = re.sub(r"[^a-zA-Z0-9._-]", "_", cleaned_name)
        cleaned_name = re.sub(r"_{2,}", "_", cleaned_name)  # Multiple underscores
        cleaned_name = cleaned_name.strip("_")

        # If we removed too much, keep original
        if len(cleaned_name) < 3:
            return dir_name

        return cleaned_name

    def clean_filename(self, filename):
        """Clean filename by removing junk patterns."""
        name, ext = os.path.splitext(filename)

        # Remove junk patterns
        junk_patterns = [
            r"_\d{8}_\d{6}",  # _20251028_021746
            r"_\d{8}",  # _20251028
            r"_\d{6}",  # _021746
            r"_\d{4}-\d{2}-\d{2}",  # _2025-10-28
            r"^documentation_documentation_documentation_",
            r"^documentation_documentation_",
            r"^documentation_",
            r"^web_resources_",
            r"^pydoc_html_",
            r"^html-generator_",
            r"^doc-generator_output_",
            r"^legacy_categories_",
            r"^archived_",
            r"^backups_",
            r"^carbons_",
            r"_[a-f0-9]{8,}$",  # _a1a7b7066bc54
            r"_from_\w+$",  # _from_csv-processor
            r"_from_\w+_\d+$",  # _from_csv-processor_1
            r"_temp$",
            r"_tmp$",
            r"_backup$",
            r"_old$",
            r"_copy$",
        ]

        for pattern in junk_patterns:
            name = re.sub(pattern, "", name)

        # Clean up
        name = re.sub(r"[^a-zA-Z0-9._-]", "_", name)
        name = re.sub(r"_{2,}", "_", name)
        name = name.strip("_")

        if len(name) < 3:
            return filename

        return name + ext

    def create_rollback_csv(self, changes, output_file):
        """Create CSV rollback file."""
        logger.info(f"📊 Creating rollback CSV: {output_file}")

        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "operation_type",
                "original_path",
                "original_name",
                "new_path",
                "new_name",
                "file_extension",
                "file_size",
                "depth_level",
                "change_reason",
                "timestamp",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for change in changes:
                writer.writerow(change)

        logger.info(f"   ✅ CSV rollback created with {len(changes)} changes")

    def execute_directory_organization(self):
        """Execute directory organization."""
        logger.info("🎯 DIRECTORY ORGANIZER")
        logger.info("=" * 60)
        logger.info("Organizing directories at depth 6+ and moving to ~/Documents/python")
        print()

        # Create target directories
        for target_dir in self.file_type_dirs.values():
            target_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"📁 Created directory: {target_dir}")

        # Find ALL files and directories
        all_items = []
        depth_counts = defaultdict(int)

        for item_path in self.root_path.rglob("*"):
            try:
                depth = len(item_path.relative_to(self.root_path).parts)
                if depth > self.max_depth:
                    continue
            except ValueError:
                continue

            all_items.append(item_path)
            depth_counts[depth] += 1

        logger.info(f"\n📊 Found {len(all_items)} items to process")
        logger.info(f"   Depth distribution:")
        for depth in sorted(depth_counts.keys()):
            logger.info(f"     Level {depth}: {depth_counts[depth]} items")

        # Process items
        directories_moved = 0
        files_moved = 0
        files_renamed = 0

        for item_path in all_items:
            try:
                if item_path.is_file():
                    # Process files
                    original_name = item_path.name
                    cleaned_name = self.clean_filename(original_name)
                    ext = item_path.suffix.lower()

                    if ext == ".py":
                        # Rename Python files in place
                        if cleaned_name != original_name:
                            new_path = item_path.parent / cleaned_name
                            item_path.rename(new_path)

                            self.changes.append(
                                {
                                    "operation_type": "python_rename",
                                    "original_path": str(item_path),
                                    "original_name": original_name,
                                    "new_path": str(new_path),
                                    "new_name": cleaned_name,
                                    "file_extension": ext,
                                    "file_size": new_path.stat().st_size,
                                    "depth_level": len(item_path.relative_to(self.root_path).parts),
                                    "change_reason": f"Cleaned filename - removed junk patterns",
                                    "timestamp": datetime.now().isoformat(),
                                }
                            )

                            logger.info(f"🐍 {original_name} → {cleaned_name}")
                            files_renamed += 1
                    else:
                        # Move other files to appropriate directories
                        if ext in self.file_type_dirs:
                            target_dir = self.file_type_dirs[ext]
                            new_path = target_dir / cleaned_name
                            shutil.move(str(item_path), str(new_path))

                            self.changes.append(
                                {
                                    "operation_type": "file_move",
                                    "original_path": str(item_path),
                                    "original_name": original_name,
                                    "new_path": str(new_path),
                                    "new_name": cleaned_name,
                                    "file_extension": ext,
                                    "file_size": new_path.stat().st_size,
                                    "depth_level": len(item_path.relative_to(self.root_path).parts),
                                    "change_reason": f"Moved {ext} file to {target_dir.name} directory",
                                    "timestamp": datetime.now().isoformat(),
                                }
                            )

                            logger.info(f"📁 {original_name} → {ext} directory")
                            files_moved += 1

                elif item_path.is_dir():
                    # Process directories - move deep ones to python root
                    depth = len(item_path.relative_to(self.root_path).parts)
                    if depth >= 6:  # Move directories at depth 6+
                        original_name = item_path.name
                        cleaned_name = self.clean_directory_name(original_name)

                        # Move to python root
                        new_path = self.target_python_dir / cleaned_name

                        # Handle name conflicts
                        counter = 1
                        while new_path.exists():
                            new_path = self.target_python_dir / f"{cleaned_name}_{counter}"
                            counter += 1

                        shutil.move(str(item_path), str(new_path))

                        self.changes.append(
                            {
                                "operation_type": "directory_move",
                                "original_path": str(item_path),
                                "original_name": original_name,
                                "new_path": str(new_path),
                                "new_name": new_path.name,
                                "file_extension": "",
                                "file_size": 0,
                                "depth_level": depth,
                                "change_reason": f"Moved directory from depth {depth} to python root",
                                "timestamp": datetime.now().isoformat(),
                            }
                        )

                        logger.info(f"📂 {original_name} → {new_path.name} (depth {depth})")
                        directories_moved += 1

            except Exception as e:
                logger.info(f"❌ Error processing {item_path.name}: {e}")

        # Create CSV rollback
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = f"/Users/steven/Documents/python/directory_rollback_{timestamp}.csv"
        self.create_rollback_csv(self.changes, csv_file)

        logger.info(f"\n✅ Directory organization complete!")
        logger.info(f"📂 Directories moved: {directories_moved}")
        logger.info(f"🐍 Python files renamed: {files_renamed}")
        logger.info(f"📁 Files moved: {files_moved}")
        logger.info(f"📊 CSV rollback: {csv_file}")
        logger.info(f"\n💡 All deep directories moved to ~/Documents/python")


def main():
    """Main execution function."""
    organizer = DirectoryOrganizer()
    organizer.execute_directory_organization()


if __name__ == "__main__":
    main()
