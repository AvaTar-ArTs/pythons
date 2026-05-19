#!/usr/bin/env python3
"""
Focused Etsy Cleanup Tool
Efficient cleanup for large-scale duplicate and archive management
"""

import json
import os
import re
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path


class FocusedEtsyCleanup:
    def __init__(self, etsy_dir=None):
        self.etsy_dir = Path(etsy_dir or os.path.expanduser("~/Pictures/etsy"))
        self.backup_dir = self.etsy_dir / "00_archives" / "cleanup_backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Target directories
        self.zip_dir = self.etsy_dir / "02_zip_archives"
        self.duplicates_dir = self.etsy_dir / "11_duplicates"
        self.archived_dir = self.etsy_dir / "12_archived"

        # Results
        self.results = {
            "duplicates_processed": 0,
            "duplicates_removed": 0,
            "archived_processed": 0,
            "archived_removed": 0,
            "space_saved": 0,
            "errors": 0,
        }

    def quick_duplicate_cleanup(self, dry_run=True):
        """Quick cleanup of obvious duplicates based on filename patterns"""
        print("🔄 Quick Duplicate Cleanup")
        print("=" * 50)

        # Get all files recursively
        all_files = list(self.duplicates_dir.rglob("*"))
        files_only = [f for f in all_files if f.is_file()]

        print(f"📁 Found {len(files_only)} files to analyze")

        # Group by obvious patterns
        pattern_groups = defaultdict(list)

        for file_path in files_only:
            name = file_path.name

            # Pattern 1: Files with _1, _2, etc. suffixes
            base_name = re.sub(r"_\d+$", "", name)
            if base_name != name:
                pattern_groups[f"numbered_{base_name}"].append(file_path)
                continue

            # Pattern 2: Files with (1), (2), etc. suffixes
            base_name = re.sub(r"\(\d+\)$", "", name)
            if base_name != name:
                pattern_groups[f"parentheses_{base_name}"].append(file_path)
                continue

            # Pattern 3: Files with "copy" in name
            if "copy" in name.lower():
                base_name = re.sub(r"\s*copy.*$", "", name, flags=re.IGNORECASE)
                pattern_groups[f"copy_{base_name}"].append(file_path)
                continue

            # Pattern 4: Files with "duplicate" in name
            if "duplicate" in name.lower():
                base_name = re.sub(r"\s*duplicate.*$", "", name, flags=re.IGNORECASE)
                pattern_groups[f"duplicate_{base_name}"].append(file_path)
                continue

        # Process each group
        removal_candidates = []
        keep_candidates = []

        for group_name, files in pattern_groups.items():
            if len(files) <= 1:
                keep_candidates.extend(files)
                continue

            # Sort by file size and modification time
            files_with_info = []
            for file_path in files:
                try:
                    stat = file_path.stat()
                    files_with_info.append(
                        {
                            "path": file_path,
                            "size": stat.st_size,
                            "mtime": stat.st_mtime,
                            "name": file_path.name,
                        }
                    )
                except:
                    continue

            if not files_with_info:
                continue

            # Sort by size (descending) then by modification time (descending)
            files_with_info.sort(key=lambda x: (x["size"], x["mtime"]), reverse=True)

            # Keep the first (largest/newest), mark others for removal
            keep_candidates.append(files_with_info[0]["path"])
            for file_info in files_with_info[1:]:
                removal_candidates.append(
                    {
                        "path": file_info["path"],
                        "size": file_info["size"],
                        "reason": f"Duplicate of {files_with_info[0]['name']} (kept larger/newer version)",
                    }
                )

        print("📊 Quick Analysis Complete:")
        print(
            f"  🔄 Duplicate groups found: {len([g for g in pattern_groups.values() if len(g) > 1])}"
        )
        print(f"  ✅ Files to keep: {len(keep_candidates)}")
        print(f"  🗑️  Files to remove: {len(removal_candidates)}")

        # Calculate potential space savings
        total_size = sum(c["size"] for c in removal_candidates)
        print(f"  💾 Potential space saved: {self.format_size(total_size)}")

        if not dry_run and removal_candidates:
            print(f"\n🗑️  Removing {len(removal_candidates)} duplicate files...")
            removed_count = 0
            for candidate in removal_candidates:
                try:
                    # Create backup
                    backup_path = self.backup_dir / candidate["path"].name
                    shutil.copy2(str(candidate["path"]), str(backup_path))

                    # Remove file
                    candidate["path"].unlink()
                    removed_count += 1
                    self.results["space_saved"] += candidate["size"]

                except Exception as e:
                    print(f"  ❌ Error removing {candidate['path'].name}: {e}")
                    self.results["errors"] += 1

            print(f"✅ Removed {removed_count} duplicate files")
            self.results["duplicates_removed"] = removed_count

        return removal_candidates, keep_candidates

    def quick_archive_cleanup(self, dry_run=True):
        """Quick cleanup of obvious archive files"""
        print("\n📁 Quick Archive Cleanup")
        print("=" * 50)

        # Get all files recursively
        all_files = list(self.archived_dir.rglob("*"))
        files_only = [f for f in all_files if f.is_file()]

        print(f"📁 Found {len(files_only)} archived files to analyze")

        # Categorize files for removal
        removal_candidates = []
        current_time = datetime.now().timestamp()
        current_time - (365 * 24 * 60 * 60)
        two_years_ago = current_time - (2 * 365 * 24 * 60 * 60)

        for file_path in files_only:
            try:
                stat = file_path.stat()
                file_age = current_time - stat.st_mtime
                file_size = stat.st_size
                name_lower = file_path.name.lower()

                # Very old files (2+ years)
                if file_age > two_years_ago:
                    removal_candidates.append(
                        {
                            "path": file_path,
                            "size": file_size,
                            "reason": "Very old file (2+ years)",
                            "priority": "high",
                        }
                    )
                    continue

                # Very small files (<1KB)
                if file_size < 1024:
                    removal_candidates.append(
                        {
                            "path": file_path,
                            "size": file_size,
                            "reason": "Very small file (<1KB)",
                            "priority": "medium",
                        }
                    )
                    continue

                # System files
                if any(
                    pattern in name_lower
                    for pattern in [".ds_store", "thumbs.db", ".tmp", "~"]
                ):
                    removal_candidates.append(
                        {
                            "path": file_path,
                            "size": file_size,
                            "reason": "System file",
                            "priority": "high",
                        }
                    )
                    continue

                # Temporary files
                if any(
                    pattern in name_lower for pattern in [".tmp", ".temp", ".bak", "~"]
                ):
                    removal_candidates.append(
                        {
                            "path": file_path,
                            "size": file_size,
                            "reason": "Temporary file",
                            "priority": "high",
                        }
                    )
                    continue

            except Exception as e:
                print(f"  ⚠️  Could not process {file_path.name}: {e}")
                continue

        # Sort by priority
        high_priority = [c for c in removal_candidates if c["priority"] == "high"]
        medium_priority = [c for c in removal_candidates if c["priority"] == "medium"]

        print("📊 Archive Analysis Complete:")
        print(f"  🗑️  High priority removals: {len(high_priority)}")
        print(f"  🗑️  Medium priority removals: {len(medium_priority)}")
        print(
            f"  💾 Total potential space saved: {self.format_size(sum(c['size'] for c in removal_candidates))}"
        )

        if not dry_run and removal_candidates:
            print(f"\n🗑️  Removing {len(removal_candidates)} archive files...")
            removed_count = 0
            for candidate in removal_candidates:
                try:
                    # Create backup
                    backup_path = self.backup_dir / candidate["path"].name
                    shutil.copy2(str(candidate["path"]), str(backup_path))

                    # Remove file
                    candidate["path"].unlink()
                    removed_count += 1
                    self.results["space_saved"] += candidate["size"]

                except Exception as e:
                    print(f"  ❌ Error removing {candidate['path'].name}: {e}")
                    self.results["errors"] += 1

            print(f"✅ Removed {removed_count} archive files")
            self.results["archived_removed"] = removed_count

        return removal_candidates

    def format_size(self, size_bytes):
        """Format size in human readable format"""
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def generate_cleanup_report(self):
        """Generate cleanup report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "results": self.results,
            "summary": {
                "duplicates_removed": self.results["duplicates_removed"],
                "archived_removed": self.results["archived_removed"],
                "total_space_saved": self.results["space_saved"],
                "formatted_space_saved": self.format_size(self.results["space_saved"]),
                "errors": self.results["errors"],
            },
        }

        report_file = (
            self.etsy_dir
            / "00_archives"
            / f"focused_cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"📋 Cleanup report saved to: {report_file}")
        return report

    def run_focused_cleanup(self, dry_run=True):
        """Run focused cleanup on duplicates and archives"""
        print("🎯 Focused Etsy Cleanup")
        print("=" * 60)
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE CLEANUP'}")
        print("=" * 60)

        # Quick duplicate cleanup
        duplicate_removals, duplicate_keeps = self.quick_duplicate_cleanup(dry_run)

        # Quick archive cleanup
        archive_removals = self.quick_archive_cleanup(dry_run)

        # Generate report
        report = self.generate_cleanup_report()

        # Summary
        total_removals = len(duplicate_removals) + len(archive_removals)
        total_space = sum(c["size"] for c in duplicate_removals) + sum(
            c["size"] for c in archive_removals
        )

        print("\n🎉 Focused Cleanup Complete!")
        print(f"📊 Total files to remove: {total_removals}")
        print(f"💾 Total space to save: {self.format_size(total_space)}")
        print(f"🔄 Duplicates: {len(duplicate_removals)} files")
        print(f"📁 Archives: {len(archive_removals)} files")

        if dry_run:
            print("\n💡 To execute cleanup, run with dry_run=False")
        else:
            print("\n✅ Cleanup executed successfully!")
            print(f"📁 Backups saved to: {self.backup_dir}")

        return report


if __name__ == "__main__":
    cleanup = FocusedEtsyCleanup()

    # Run dry run first
    print("🔍 Running DRY RUN analysis...")
    cleanup.run_focused_cleanup(dry_run=True)

    print("\n" + "=" * 60)
    print("🚀 Executing LIVE CLEANUP...")
    cleanup.run_focused_cleanup(dry_run=False)
