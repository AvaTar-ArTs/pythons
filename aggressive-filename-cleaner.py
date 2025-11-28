#!/usr/bin/env python3
"""
Aggressive Filename Cleaner - Fix the filename insanity
Removes duplicate numbers, redundant suffixes, and generic words
"""

import os
import re
import csv
from pathlib import Path
from datetime import datetime


class AggressiveFilenameCleaner:
    """Clean up terrible filename patterns aggressively."""

    def __init__(self, target_dir: str = Path(str(Path.home()) + "/Documents/python")):
        """__init__ function."""

        self.target_dir = Path(target_dir)
        self.changes = []

        # Patterns to remove aggressively
        self.junk_patterns = [
            # Duplicate numbers and copies
            r"\s+copy\s*(\d+)?\.py$",
            r"\s+copy\s*\.py$",
            r"\s+\(\d+\)\.py$",
            r"\s+\d+\s+copy\.py$",
            r"\s+copy\s+\d+\.py$",
            # Redundant suffixes
            r"_from_[^_]+\.py$",
            r"_from_[^_]+_from_[^_]+\.py$",
            r"_from_[^_]+_from_[^_]+_from_[^_]+\.py$",
            # Generic words and numbers
            r"_\d+_\d+_\d+\.py$",
            r"_\d+_\d+\.py$",
            r"_\d+\.py$",
            r"\s+\d+\s+\d+\s+\d+\.py$",
            r"\s+\d+\s+\d+\.py$",
            r"\s+\d+\.py$",
            # Common generic patterns
            r"_1_1_1\.py$",
            r"_1_1\.py$",
            r"_1\.py$",
            r"\s+1\s+1\s+1\.py$",
            r"\s+1\s+1\.py$",
            r"\s+1\.py$",
            # File type indicators
            r"_from_csv-processor\.py$",
            r"_from_ai-image-generator\.py$",
            r"_from_backup-tool\.py$",
            r"_from_utilities\.py$",
            r"_from_bot-automation\.py$",
            r"_from_api-development\.py$",
            r"_from_video-downloader\.py$",
            r"_from_image-converter\.py$",
            # Generic prefixes
            r"^\d+mb_from_",
            r"^\d+dpi_from_",
            r"^\d+_from_",
            r"^\d+mb_",
            r"^\d+dpi_",
            r"^\d+_",
            # Multiple spaces and underscores
            r"\s+",
            r"_{2,}",
            r"__+",
        ]

        # Words to remove
        self.generic_words = [
            "copy",
            "duplicate",
            "backup",
            "old",
            "new",
            "temp",
            "tmp",
            "version",
            "v1",
            "v2",
            "v3",
            "final",
            "draft",
            "test",
            "from",
            "the",
            "and",
            "or",
            "of",
            "in",
            "on",
            "at",
            "to",
            "for",
            "with",
            "by",
            "from",
            "generated",
            "auto",
            "bot",
        ]

    def clean_filename(self, filename: str) -> str:
        """Clean a filename aggressively."""
        original = filename
        cleaned = filename

        # Remove .py extension temporarily
        if cleaned.endswith(".py"):
            cleaned = cleaned[:-3]

        # Apply junk patterns
        for pattern in self.junk_patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

        # Remove generic words
        words = cleaned.split("_")
        filtered_words = []

        for word in words:
            # Clean each word
            word = word.strip()
            if not word:
                continue

            # Remove numbers at the end
            word = re.sub(r"\d+$", "", word)

            # Skip generic words
            if word.lower() in self.generic_words:
                continue

            # Skip single characters or numbers
            if len(word) <= 1 or word.isdigit():
                continue

            filtered_words.append(word)

        # Join words with underscores
        if filtered_words:
            cleaned = "_".join(filtered_words)
        else:
            # If nothing left, use a generic name
            cleaned = "cleaned_file"

        # Clean up multiple underscores
        cleaned = re.sub(r"_{2,}", "_", cleaned)
        cleaned = re.sub(r"^_|_$", "", cleaned)

        # Add .py extension back
        cleaned += ".py"

        # Ensure it's different from original
        if cleaned == original:
            cleaned = cleaned.replace(".py", "_cleaned.py")

        return cleaned

    def find_files_to_clean(self) -> list:
        """Find Python files that need cleaning."""
        files_to_clean = []

        for file_path in self.target_dir.glob("*.py"):
            filename = file_path.name
            cleaned_name = self.clean_filename(filename)

            # Check if cleaning would change the name
            if cleaned_name != filename:
                files_to_clean.append(
                    {
                        "original_path": str(file_path),
                        "original_name": filename,
                        "cleaned_name": cleaned_name,
                        "new_path": str(file_path.parent / cleaned_name),
                    }
                )

        return files_to_clean

    def clean_files(self, dry_run: bool = True) -> dict:
        """Clean the files (dry run by default)."""
        logger.info("🧹 AGGRESSIVE FILENAME CLEANER")
        logger.info("=" * 50)
        logger.info("Fixing the filename insanity!")
        print()

        files_to_clean = self.find_files_to_clean()

        if not files_to_clean:
            logger.info("✅ No files need cleaning!")
            return {"cleaned": 0, "errors": 0}

        logger.info(f"📄 Found {len(files_to_clean)} files to clean:")
        print()

        cleaned_count = 0
        error_count = 0

        for file_info in files_to_clean:
            original_name = file_info["original_name"]
            cleaned_name = file_info["cleaned_name"]
            original_path = Path(file_info["original_path"])
            new_path = Path(file_info["new_path"])

            logger.info(f"   {original_name}")
            logger.info(f"   → {cleaned_name}")

            if not dry_run:
                try:
                    # Check if target already exists
                    if new_path.exists():
                        # Add number suffix
                        counter = 1
                        while new_path.exists():
                            name_parts = cleaned_name.rsplit(".", 1)
                            if len(name_parts) == 2:
                                new_name = f"{name_parts[0]}_{counter}.{name_parts[1]}"
                            else:
                                new_name = f"{cleaned_name}_{counter}"
                            new_path = original_path.parent / new_name
                            counter += 1

                    # Rename the file
                    original_path.rename(new_path)
                    logger.info(f"   ✅ Renamed successfully")
                    cleaned_count += 1

                    # Record the change
                    self.changes.append(
                        {
                            "original_path": str(original_path),
                            "new_path": str(new_path),
                            "original_name": original_name,
                            "new_name": new_path.name,
                            "status": "success",
                        }
                    )

                except Exception as e:
                    logger.info(f"   ❌ Error: {e}")
                    error_count += 1

                    self.changes.append(
                        {
                            "original_path": str(original_path),
                            "new_path": str(new_path),
                            "original_name": original_name,
                            "new_name": cleaned_name,
                            "status": f"error: {e}",
                        }
                    )
            else:
                logger.info(f"   🔍 Dry run - would rename")
                cleaned_count += 1

                self.changes.append(
                    {
                        "original_path": str(original_path),
                        "new_path": str(new_path),
                        "original_name": original_name,
                        "new_name": cleaned_name,
                        "status": "dry_run",
                    }
                )

            print()

        return {"cleaned": cleaned_count, "errors": error_count}

    def save_changes_csv(self) -> str:
        """Save changes to CSV for rollback."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = fstr(Path.home()) + "/Documents/python/filename_cleanup_{timestamp}.csv"

        with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "original_path",
                "new_path",
                "original_name",
                "new_name",
                "status",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for change in self.changes:
                writer.writerow(change)

        return csv_file


def main():
    """Run the aggressive filename cleaner."""
    cleaner = AggressiveFilenameCleaner()

    # First, show what would be cleaned (dry run)
    logger.info("🔍 DRY RUN - Showing what would be cleaned:")
    logger.info("=" * 60)
    results = cleaner.clean_files(dry_run=True)

    logger.info(f"\n📊 DRY RUN RESULTS:")
    logger.info(f"   Files to clean: {results['cleaned']}")
    logger.info(f"   Errors: {results['errors']}")

    # Save dry run results
    csv_file = cleaner.save_changes_csv()
    logger.info(f"\n📄 Dry run results saved to: {csv_file}")

    logger.info(f"\n💡 To execute the cleaning, run:")
    logger.info(f"   python3 aggressive_filename_cleaner.py --execute")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        cleaner = AggressiveFilenameCleaner()
        logger.info("🚀 EXECUTING FILENAME CLEANUP")
        logger.info("=" * 50)
        results = cleaner.clean_files(dry_run=False)
        csv_file = cleaner.save_changes_csv()

        logger.info(f"\n🎯 CLEANUP COMPLETE!")
        logger.info(f"   Files cleaned: {results['cleaned']}")
        logger.info(f"   Errors: {results['errors']}")
        logger.info(f"   Changes saved to: {csv_file}")
    else:
        main()
