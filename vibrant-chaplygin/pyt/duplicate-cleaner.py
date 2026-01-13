#!/usr/bin/env python3
"""
Duplicate Cleaner - Remove duplicate files and consolidate naming
"""

import os
import csv
import hashlib
from pathlib import Path
from datetime import datetime


class DuplicateCleaner:
    """Clean up duplicate files and consolidate naming."""

    def __init__(self, target_dir: str = Path(str(Path.home()) + "/Documents/python")):
        """__init__ function."""

        self.target_dir = Path(target_dir)
        self.changes = []

    def find_duplicate_groups(self) -> dict:
        """Find files that are duplicates or variations of the same name."""
        duplicate_groups = {}

        # Group files by base name patterns
        name_groups = {}

        for file_path in self.target_dir.glob("*.py"):
            filename = file_path.name
            base_name = self.get_base_name(filename)

            if base_name not in name_groups:
                name_groups[base_name] = []
            name_groups[base_name].append(file_path)

        # Find groups with multiple files
        for base_name, files in name_groups.items():
            if len(files) > 1:
                duplicate_groups[base_name] = files

        return duplicate_groups

    def get_base_name(self, filename: str) -> str:
        """Extract base name from filename."""
        # Remove .py extension
        name = filename.replace(".py", "")

        # Remove common suffixes
        suffixes_to_remove = [
            "_1",
            "_2",
            "_3",
            "_4",
            "_5",
            "_copy",
            "_duplicate",
            "_backup",
            "_old",
            "_new",
            "_temp",
            "_tmp",
            "_final",
            "_draft",
            "_test",
        ]

        for suffix in suffixes_to_remove:
            if name.endswith(suffix):
                name = name[: -len(suffix)]
                break

        return name

    def get_file_hash(self, file_path: Path) -> str:
        """Get MD5 hash of file content."""
        try:
            with open(file_path, "rb") as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()
        except Exception:
            return ""

    def analyze_duplicates(self) -> dict:
        """Analyze duplicate groups and recommend actions."""
        duplicate_groups = self.find_duplicate_groups()
        analysis = {
            "groups": {},
            "total_files": 0,
            "duplicates_found": 0,
            "recommendations": [],
        }

        for base_name, files in duplicate_groups.items():
            analysis["total_files"] += len(files)
            analysis["duplicates_found"] += len(files) - 1

            # Get file info
            file_info = []
            for file_path in files:
                try:
                    stat = file_path.stat()
                    file_info.append(
                        {
                            "path": str(file_path),
                            "name": file_path.name,
                            "size": stat.st_size,
                            "modified": stat.st_mtime,
                            "hash": self.get_file_hash(file_path),
                        }
                    )
                except Exception as e:
                    logger.info(f"Error analyzing {file_path}: {e}")

            # Sort by size (largest first) and modification time (newest first)
            file_info.sort(key=lambda x: (-x["size"], -x["modified"]))

            # Find unique files by hash
            unique_files = {}
            for info in file_info:
                if info["hash"] not in unique_files:
                    unique_files[info["hash"]] = info

            analysis["groups"][base_name] = {
                "files": file_info,
                "unique_files": list(unique_files.values()),
                "duplicates": [f for f in file_info if f not in unique_files.values()],
                "keep": file_info[0] if file_info else None,  # Keep the largest/newest
                "remove": file_info[1:] if len(file_info) > 1 else [],
            }

            # Add recommendation
            if len(file_info) > 1:
                keep_file = file_info[0]["name"]
                remove_files = [f["name"] for f in file_info[1:]]
                analysis["recommendations"].append(
                    {
                        "base_name": base_name,
                        "keep": keep_file,
                        "remove": remove_files,
                        "reason": f"Keep {keep_file} (largest/newest), remove {len(remove_files)} duplicates",
                    }
                )

        return analysis

    def clean_duplicates(self, dry_run: bool = True) -> dict:
        """Clean up duplicate files."""
        logger.info("🧹 DUPLICATE CLEANER")
        logger.info("=" * 50)
        logger.info("Removing duplicate files and consolidating names")
        print()

        analysis = self.analyze_duplicates()

        if not analysis["groups"]:
            logger.info("✅ No duplicate groups found!")
            return {"cleaned": 0, "errors": 0}

        logger.info(f"📄 Found {len(analysis['groups'])} duplicate groups:")
        logger.info(f"   Total files: {analysis['total_files']}")
        logger.info(f"   Duplicates: {analysis['duplicates_found']}")
        print()

        cleaned_count = 0
        error_count = 0

        for base_name, group_info in analysis["groups"].items():
            logger.info(f"🔍 Group: {base_name}")
            logger.info(f"   Files: {len(group_info['files'])}")
            logger.info(f"   Unique: {len(group_info['unique_files'])}")

            if group_info["keep"]:
                logger.info(f"   ✅ Keep: {group_info['keep']['name']}")

                for file_info in group_info["remove"]:
                    logger.info(f"   🗑️ Remove: {file_info['name']}")

                    if not dry_run:
                        try:
                            file_path = Path(file_info["path"])
                            file_path.unlink()  # Delete the file
                            logger.info(f"      ✅ Deleted successfully")
                            cleaned_count += 1

                            self.changes.append(
                                {
                                    "action": "deleted",
                                    "file_path": file_info["path"],
                                    "file_name": file_info["name"],
                                    "reason": f"Duplicate of {group_info['keep']['name']}",
                                    "status": "success",
                                }
                            )

                        except Exception as e:
                            logger.info(f"      ❌ Error: {e}")
                            error_count += 1

                            self.changes.append(
                                {
                                    "action": "deleted",
                                    "file_path": file_info["path"],
                                    "file_name": file_info["name"],
                                    "reason": f"Duplicate of {group_info['keep']['name']}",
                                    "status": f"error: {e}",
                                }
                            )
                    else:
                        logger.info(f"      🔍 Dry run - would delete")
                        cleaned_count += 1

                        self.changes.append(
                            {
                                "action": "deleted",
                                "file_path": file_info["path"],
                                "file_name": file_info["name"],
                                "reason": f"Duplicate of {group_info['keep']['name']}",
                                "status": "dry_run",
                            }
                        )

            print()

        return {"cleaned": cleaned_count, "errors": error_count}

    def save_changes_csv(self) -> str:
        """Save changes to CSV for rollback."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = fstr(Path.home()) + "/Documents/python/duplicate_cleanup_{timestamp}.csv"

        with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["action", "file_path", "file_name", "reason", "status"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for change in self.changes:
                writer.writerow(change)

        return csv_file


def main():
    """Run the duplicate cleaner."""
    cleaner = DuplicateCleaner()

    # First, show what would be cleaned (dry run)
    logger.info("🔍 DRY RUN - Showing what duplicates would be cleaned:")
    logger.info("=" * 70)
    results = cleaner.clean_duplicates(dry_run=True)

    logger.info(f"\n📊 DRY RUN RESULTS:")
    logger.info(f"   Files to clean: {results['cleaned']}")
    logger.info(f"   Errors: {results['errors']}")

    # Save dry run results
    csv_file = cleaner.save_changes_csv()
    logger.info(f"\n📄 Dry run results saved to: {csv_file}")

    logger.info(f"\n💡 To execute the duplicate cleaning, run:")
    logger.info(f"   python3 duplicate_cleaner.py --execute")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        cleaner = DuplicateCleaner()
        logger.info("🚀 EXECUTING DUPLICATE CLEANUP")
        logger.info("=" * 50)
        results = cleaner.clean_duplicates(dry_run=False)
        csv_file = cleaner.save_changes_csv()

        logger.info(f"\n🎯 DUPLICATE CLEANUP COMPLETE!")
        logger.info(f"   Files cleaned: {results['cleaned']}")
        logger.info(f"   Errors: {results['errors']}")
        logger.info(f"   Changes saved to: {csv_file}")
    else:
        main()
