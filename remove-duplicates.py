#!/usr/bin/env python3
"""
Advanced Duplicate Remover - Multiple detection methods
Uses content hashing, similarity analysis, and pattern matching
"""

import os
import csv
import hashlib
import difflib
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class AdvancedDuplicateRemover:
    """Advanced duplicate detection and removal using multiple methods."""

    def __init__(self, target_dir: str = Path(str(Path.home()) + "/Documents/python")):
        """__init__ function."""

        self.target_dir = Path(target_dir)
        self.changes = []

    def get_file_hash(self, file_path: Path) -> str:
        """Get MD5 hash of file content."""
        try:
            with open(file_path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""

    def get_file_content(self, file_path: Path) -> str:
        """Get file content as string."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception:
            return ""

    def calculate_similarity(self, content1: str, content2: str) -> float:
        """Calculate similarity between two file contents."""
        if not content1 or not content2:
            return 0.0

        # Use difflib to calculate similarity
        similarity = difflib.SequenceMatcher(None, content1, content2).ratio()
        return similarity

    def find_exact_duplicates(self) -> dict:
        """Find files with identical content (exact duplicates)."""
        logger.info("🔍 Finding exact duplicates by content hash...")

        hash_groups = defaultdict(list)

        for file_path in self.target_dir.glob("*.py"):
            file_hash = self.get_file_hash(file_path)
            if file_hash:
                hash_groups[file_hash].append(file_path)

        # Filter groups with duplicates
        exact_duplicates = {
            hash_val: files for hash_val, files in hash_groups.items() if len(files) > 1
        }

        logger.info(f"   Found {len(exact_duplicates)} groups of exact duplicates")
        return exact_duplicates

    def find_similar_files(self, similarity_threshold: float = 0.8) -> dict:
        """Find files with similar content."""
        logger.info(f"🔍 Finding similar files (threshold: {similarity_threshold})...")

        files = list(self.target_dir.glob("*.py"))
        similar_groups = []
        processed = set()

        for i, file1 in enumerate(files):
            if file1 in processed:
                continue

            content1 = self.get_file_content(file1)
            if not content1:
                continue

            similar_files = [file1]

            for j, file2 in enumerate(files[i + 1 :], i + 1):
                if file2 in processed:
                    continue

                content2 = self.get_file_content(file2)
                if not content2:
                    continue

                similarity = self.calculate_similarity(content1, content2)
                if similarity >= similarity_threshold:
                    similar_files.append(file2)
                    processed.add(file2)

            if len(similar_files) > 1:
                similar_groups.append(similar_files)
                processed.update(similar_files)

        logger.info(f"   Found {len(similar_groups)} groups of similar files")
        return similar_groups

    def find_name_pattern_duplicates(self) -> dict:
        """Find files with similar naming patterns."""
        logger.info("🔍 Finding name pattern duplicates...")

        name_groups = defaultdict(list)

        for file_path in self.target_dir.glob("*.py"):
            name = file_path.stem  # filename without extension

            # Extract base name (remove numbers, common suffixes)
            base_name = self.extract_base_name(name)

            if base_name and len(base_name) > 2:  # Ignore very short names
                name_groups[base_name].append(file_path)

        # Filter groups with multiple files
        pattern_duplicates = {
            base: files for base, files in name_groups.items() if len(files) > 1
        }

        logger.info(
            f"   Found {len(pattern_duplicates)} groups of name pattern duplicates"
        )
        return pattern_duplicates

    def extract_base_name(self, filename: str) -> str:
        """Extract base name from filename."""
        # Remove common suffixes and numbers
        import re

        # Remove numbers at the end
        name = re.sub(r"\d+$", "", filename)

        # Remove common suffixes
        suffixes = ["_copy", "_duplicate", "_backup", "_old", "_new", "_temp", "_tmp"]
        for suffix in suffixes:
            if name.endswith(suffix):
                name = name[: -len(suffix)]
                break

        # Remove multiple underscores
        name = re.sub(r"_{2,}", "_", name)
        name = name.strip("_")

        return name if len(name) > 2 else ""

    def select_best_file(self, file_group: list) -> Path:
        """Select the best file from a group of duplicates."""
        if not file_group:
            return None

        # Sort by file size (largest first), then by modification time (newest first)
        file_group.sort(key=lambda f: (-f.stat().st_size, -f.stat().st_mtime))
        return file_group[0]

    def remove_duplicates(self, dry_run: bool = True) -> dict:
        """Remove duplicates using all methods."""
        logger.info("🧹 ADVANCED DUPLICATE REMOVER")
        logger.info("=" * 60)
        logger.info("Using multiple detection methods")
        print()

        # Find all types of duplicates
        exact_duplicates = self.find_exact_duplicates()
        similar_files = self.find_similar_files()
        pattern_duplicates = self.find_name_pattern_duplicates()

        total_duplicates = 0
        total_files_to_remove = 0

        # Process exact duplicates
        logger.info(
            f"\n📄 Processing {len(exact_duplicates)} exact duplicate groups..."
        )
        for hash_val, files in exact_duplicates.items():
            best_file = self.select_best_file(files)
            files_to_remove = [f for f in files if f != best_file]

            logger.info(f"   Group: {best_file.name} (keeping best of {len(files)})")
            for file_to_remove in files_to_remove:
                logger.info(f"      🗑️ Remove: {file_to_remove.name}")

                if not dry_run:
                    try:
                        file_to_remove.unlink()
                        logger.info(f"         ✅ Deleted successfully")
                        total_files_to_remove += 1

                        self.changes.append(
                            {
                                "type": "exact_duplicate",
                                "kept": str(best_file),
                                "removed": str(file_to_remove),
                                "reason": f"Exact duplicate of {best_file.name}",
                                "status": "success",
                            }
                        )
                    except Exception as e:
                        logger.info(f"         ❌ Error: {e}")
                        self.changes.append(
                            {
                                "type": "exact_duplicate",
                                "kept": str(best_file),
                                "removed": str(file_to_remove),
                                "reason": f"Exact duplicate of {best_file.name}",
                                "status": f"error: {e}",
                            }
                        )
                else:
                    logger.info(f"         🔍 Dry run - would delete")
                    total_files_to_remove += 1
                    self.changes.append(
                        {
                            "type": "exact_duplicate",
                            "kept": str(best_file),
                            "removed": str(file_to_remove),
                            "reason": f"Exact duplicate of {best_file.name}",
                            "status": "dry_run",
                        }
                    )

            total_duplicates += len(files) - 1

        # Process similar files
        logger.info(f"\n📄 Processing {len(similar_files)} similar file groups...")
        for file_group in similar_files:
            best_file = self.select_best_file(file_group)
            files_to_remove = [f for f in file_group if f != best_file]

            logger.info(
                f"   Group: {best_file.name} (keeping best of {len(file_group)})"
            )
            for file_to_remove in files_to_remove:
                logger.info(f"      🗑️ Remove: {file_to_remove.name}")

                if not dry_run:
                    try:
                        file_to_remove.unlink()
                        logger.info(f"         ✅ Deleted successfully")
                        total_files_to_remove += 1

                        self.changes.append(
                            {
                                "type": "similar_file",
                                "kept": str(best_file),
                                "removed": str(file_to_remove),
                                "reason": f"Similar to {best_file.name}",
                                "status": "success",
                            }
                        )
                    except Exception as e:
                        logger.info(f"         ❌ Error: {e}")
                        self.changes.append(
                            {
                                "type": "similar_file",
                                "kept": str(best_file),
                                "removed": str(file_to_remove),
                                "reason": f"Similar to {best_file.name}",
                                "status": f"error: {e}",
                            }
                        )
                else:
                    logger.info(f"         🔍 Dry run - would delete")
                    total_files_to_remove += 1
                    self.changes.append(
                        {
                            "type": "similar_file",
                            "kept": str(best_file),
                            "removed": str(file_to_remove),
                            "reason": f"Similar to {best_file.name}",
                            "status": "dry_run",
                        }
                    )

            total_duplicates += len(file_group) - 1

        # Process pattern duplicates
        logger.info(f"\n📄 Processing {len(pattern_duplicates)} name pattern groups...")
        for base_name, files in pattern_duplicates.items():
            best_file = self.select_best_file(files)
            files_to_remove = [f for f in files if f != best_file]

            logger.info(f"   Group: {base_name} (keeping best of {len(files)})")
            for file_to_remove in files_to_remove:
                logger.info(f"      🗑️ Remove: {file_to_remove.name}")

                if not dry_run:
                    try:
                        file_to_remove.unlink()
                        logger.info(f"         ✅ Deleted successfully")
                        total_files_to_remove += 1

                        self.changes.append(
                            {
                                "type": "pattern_duplicate",
                                "kept": str(best_file),
                                "removed": str(file_to_remove),
                                "reason": f"Pattern duplicate of {base_name}",
                                "status": "success",
                            }
                        )
                    except Exception as e:
                        logger.info(f"         ❌ Error: {e}")
                        self.changes.append(
                            {
                                "type": "pattern_duplicate",
                                "kept": str(best_file),
                                "removed": str(file_to_remove),
                                "reason": f"Pattern duplicate of {base_name}",
                                "status": f"error: {e}",
                            }
                        )
                else:
                    logger.info(f"         🔍 Dry run - would delete")
                    total_files_to_remove += 1
                    self.changes.append(
                        {
                            "type": "pattern_duplicate",
                            "kept": str(best_file),
                            "removed": str(file_to_remove),
                            "reason": f"Pattern duplicate of {base_name}",
                            "status": "dry_run",
                        }
                    )

            total_duplicates += len(files) - 1

        return {
            "exact_groups": len(exact_duplicates),
            "similar_groups": len(similar_files),
            "pattern_groups": len(pattern_duplicates),
            "total_duplicates": total_duplicates,
            "files_to_remove": total_files_to_remove,
        }

    def save_changes_csv(self) -> str:
        """Save changes to CSV for rollback."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = (
            fstr(Path.home()) + "/Documents/python/advanced_duplicate_cleanup_{timestamp}.csv"
        )

        with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["type", "kept", "removed", "reason", "status"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for change in self.changes:
                writer.writerow(change)

        return csv_file


def main():
    """Run the advanced duplicate remover."""
    remover = AdvancedDuplicateRemover()

    # First, show what would be cleaned (dry run)
    logger.info("🔍 DRY RUN - Showing what duplicates would be removed:")
    logger.info("=" * 70)
    results = remover.remove_duplicates(dry_run=True)

    logger.info(f"\n📊 DRY RUN RESULTS:")
    logger.info(f"   Exact duplicate groups: {results['exact_groups']}")
    logger.info(f"   Similar file groups: {results['similar_groups']}")
    logger.info(f"   Pattern duplicate groups: {results['pattern_groups']}")
    logger.info(f"   Total duplicates: {results['total_duplicates']}")
    logger.info(f"   Files to remove: {results['files_to_remove']}")

    # Save dry run results
    csv_file = remover.save_changes_csv()
    logger.info(f"\n📄 Dry run results saved to: {csv_file}")

    logger.info(f"\n💡 To execute the advanced duplicate removal, run:")
    logger.info(f"   python3 advanced_duplicate_remover.py --execute")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        remover = AdvancedDuplicateRemover()
        logger.info("🚀 EXECUTING ADVANCED DUPLICATE REMOVAL")
        logger.info("=" * 60)
        results = remover.remove_duplicates(dry_run=False)
        csv_file = remover.save_changes_csv()

        logger.info(f"\n🎯 ADVANCED DUPLICATE REMOVAL COMPLETE!")
        logger.info(f"   Exact duplicate groups: {results['exact_groups']}")
        logger.info(f"   Similar file groups: {results['similar_groups']}")
        logger.info(f"   Pattern duplicate groups: {results['pattern_groups']}")
        logger.info(f"   Total duplicates: {results['total_duplicates']}")
        logger.info(f"   Files removed: {results['files_to_remove']}")
        logger.info(f"   Changes saved to: {csv_file}")
    else:
        main()
