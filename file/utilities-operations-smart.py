"""
Utilities File Operations Smart 6

This module provides functionality for utilities file operations smart 6.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_1024 = 1024
CONSTANT_4096 = 4096
CONSTANT_10000 = 10000
CONSTANT_100000 = 100000

#!/usr/bin/env python3
"""
Smart Duplicate Cleaner for Documents
Safely removes duplicates while preserving the most recent and important files.
"""

import os
import json
import hashlib
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import re


class SmartDuplicateCleaner:
    def __init__(self, root_path, dry_run=True):
        """__init__ function."""

        self.root_path = Path(root_path)
        self.dry_run = dry_run
        self.duplicates = defaultdict(list)
        self.file_hashes = {}
        self.cleanup_log = []
        self.space_saved = 0
        self.files_removed = 0
        self.skipped_files = 0

        # Safety settings
        self.protected_dirs = {"Code", "python", "script", "Docs", "Media", "Archives"}
        self.protected_extensions = {".py", ".js", ".html", ".css", ".md", ".json"}

    def get_file_hash(self, filepath):
        """Get MD5 hash of file for duplicate detection"""
        try:
            hash_md5 = hashlib.md5()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(CONSTANT_4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except (OSError, UnicodeError, PermissionError):
            return None

    def is_protected_file(self, filepath):
        """Check if file should be protected from deletion"""
        path_str = str(filepath)

        # Check if in protected directory
        for protected_dir in self.protected_dirs:
            if protected_dir in path_str:
                return True

        # Check if important extension
        if filepath.suffix.lower() in self.protected_extensions:
            return True

        # Check if file has important keywords
        important_keywords = [
            "main",
            "config",
            "setup",
            "requirements",
            "readme",
            "index",
            "app",
            "server",
            "client",
            "utils",
            "helpers",
        ]

        filename_lower = filepath.name.lower()
        for keyword in important_keywords:
            if keyword in filename_lower:
                return True

        return False

    def find_duplicates(self, sample_size=CONSTANT_100000):
        """Find duplicate files using content hashing"""
        logger.info(f"🔍 Scanning for duplicates (sample of {sample_size:,} files)...")

        file_count = 0
        sample_files = []

        # Collect sample files
        for file_path in self.root_path.rglob("*"):
            if file_path.is_file():
                sample_files.append(file_path)
                if len(sample_files) >= sample_size:
                    break

        logger.info(f"📊 Analyzing {len(sample_files):,} files for duplicates...")

        for file_path in sample_files:
            file_count += 1
            if file_count % CONSTANT_10000 == 0:
                logger.info(f"   Processed {file_count:,} files...")

            try:
                file_hash = self.get_file_hash(file_path)
                if file_hash:
                    file_info = {
                        "path": str(file_path),
                        "size": file_path.stat().st_size,
                        "modified": file_path.stat().st_mtime,
                        "name": file_path.name,
                        "is_protected": self.is_protected_file(file_path),
                    }

                    if file_hash in self.file_hashes:
                        self.duplicates[file_hash].append(file_info)
                    else:
                        self.file_hashes[file_hash] = file_info
            except (OSError, IOError, FileNotFoundError):
                self.skipped_files += 1
                continue

        logger.info(
            f"✅ Found {len(self.duplicates)} duplicate groups affecting {sum(len(files) for files in self.duplicates.values())} files"
        )
        return self.duplicates

    def analyze_duplicate_groups(self):
        """Analyze duplicate groups to determine which files to keep/remove"""
        cleanup_plan = []

        logger.info("🧠 Analyzing duplicate groups for smart cleanup...")

        for hash_val, files in self.duplicates.items():
            if len(files) <= 1:
                continue

            # Sort files by priority (keep the best one)
            files_sorted = sorted(
                files,
                key=lambda x: (
                    not x["is_protected"],  # Protected files first
                    x["modified"],  # Newer files first
                    -x["size"],  # Larger files first (usually more complete)
                    x["path"],  # Alphabetical for consistency
                ),
            )

            # Keep the first file (highest priority)
            keep_file = files_sorted[0]
            remove_files = files_sorted[1:]

            # Calculate space savings
            space_saved = sum(f["size"] for f in remove_files)

            group_plan = {
                "hash": hash_val,
                "keep_file": keep_file,
                "remove_files": remove_files,
                "space_saved": space_saved,
                "file_count": len(files),
            }

            cleanup_plan.append(group_plan)

        # Sort by space savings (biggest wins first)
        cleanup_plan.sort(key=lambda x: x["space_saved"], reverse=True)

        return cleanup_plan

    def create_backup_plan(self, cleanup_plan):
        """Create a backup plan for important files"""
        backup_dir = self.root_path / "00_CLEANUP_BACKUP"

        if not self.dry_run:
            backup_dir.mkdir(exist_ok=True)

        backup_log = []

        logger.info("💾 Creating backup plan...")

        for group in cleanup_plan:
            for file_info in group["remove_files"]:
                if file_info["is_protected"]:
                    source_path = Path(file_info["path"])
                    backup_path = backup_dir / source_path.relative_to(self.root_path)

                    backup_log.append(
                        {"source": str(source_path), "backup": str(backup_path), "reason": "protected_file"}
                    )

                    if not self.dry_run:
                        backup_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source_path, backup_path)

        return backup_log

    def execute_cleanup(self, cleanup_plan):
        """Execute the cleanup plan"""
        logger.info(f"🚀 {'DRY RUN: ' if self.dry_run else ''}Executing cleanup plan...")

        total_space_saved = 0
        total_files_removed = 0

        for i, group in enumerate(cleanup_plan):
            if i % CONSTANT_100 == 0:
                logger.info(f"   Processing group {i+1}/{len(cleanup_plan)}...")

            for file_info in group["remove_files"]:
                file_path = Path(file_info["path"])

                # Log the action
                action = {
                    "action": "remove" if not self.dry_run else "would_remove",
                    "file": str(file_path),
                    "size": file_info["size"],
                    "reason": "duplicate",
                    "kept_file": group["keep_file"]["path"],
                }

                self.cleanup_log.append(action)

                if not self.dry_run:
                    try:
                        if file_path.exists():
                            file_path.unlink()
                            total_files_removed += 1
                            total_space_saved += file_info["size"]
                    except Exception as e:
                        action["error"] = str(e)
                        logger.info(f"   ⚠️  Error removing {file_path}: {e}")
                else:
                    total_files_removed += 1
                    total_space_saved += file_info["size"]

        self.space_saved = total_space_saved
        self.files_removed = total_files_removed

        return {
            "space_saved": total_space_saved,
            "space_saved_gb": total_space_saved / (CONSTANT_1024**3),
            "files_removed": total_files_removed,
        }

    def generate_cleanup_report(self, cleanup_plan, backup_log):
        """Generate detailed cleanup report"""
        report = f"""# Smart Duplicate Cleanup Report

## Summary
- **Mode:** {'DRY RUN' if self.dry_run else 'LIVE CLEANUP'}
- **Duplicate Groups:** {len(cleanup_plan)}
- **Files to Remove:** {self.files_removed:,}
- **Space to Save:** {self.space_saved / (CONSTANT_1024**3):.2f} GB
- **Backup Files:** {len(backup_log)}
- **Skipped Files:** {self.skipped_files:,}

## Top Space Savings by File Type
"""

        # Analyze by file extension
        extension_savings = defaultdict(int)
        for group in cleanup_plan:
            for file_info in group["remove_files"]:
                ext = Path(file_info["path"]).suffix.lower() or "no_extension"
                extension_savings[ext] += file_info["size"]

        sorted_extensions = sorted(extension_savings.items(), key=lambda x: x[1], reverse=True)

        for ext, size in sorted_extensions[:10]:
            report += f"- **{ext}:** {size / (CONSTANT_1024**2):.1f} MB\n"

        report += "\n## Protected Files Backed Up\n"

        for backup in backup_log[:20]:  # Show first 20
            report += f"- `{backup['source']}` → `{backup['backup']}`\n"

        if len(backup_log) > 20:
            report += f"... and {len(backup_log) - 20} more files\n"

        report += "\n## Cleanup Actions\n"

        # Group actions by type
        action_counts = defaultdict(int)
        for action in self.cleanup_log:
            action_counts[action["action"]] += 1

        for action_type, count in action_counts.items():
            report += f"- **{action_type.replace('_', ' ').title()}:** {count:,} files\n"

        return report

    def run_cleanup(self, dry_run=True):
        """Run the complete cleanup process"""
        logger.info("🧹 Starting Smart Duplicate Cleanup...")
        logger.info(f"Mode: {'DRY RUN' if dry_run else 'LIVE CLEANUP'}")

        # Find duplicates
        duplicates = self.find_duplicates()

        # Analyze for cleanup
        cleanup_plan = self.analyze_duplicate_groups()

        # Create backup plan
        backup_log = self.create_backup_plan(cleanup_plan)

        # Execute cleanup
        results = self.execute_cleanup(cleanup_plan)

        # Generate report
        report = self.generate_cleanup_report(cleanup_plan, backup_log)

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save JSON data
        cleanup_data = {
            "timestamp": timestamp,
            "dry_run": dry_run,
            "cleanup_plan": cleanup_plan,
            "backup_log": backup_log,
            "cleanup_log": self.cleanup_log,
            "results": results,
        }

        json_file = self.root_path / f"cleanup_report_{timestamp}.json"
        with open(json_file, "w") as f:
            json.dump(cleanup_data, f, indent=2)

        # Save markdown report
        report_file = self.root_path / f"cleanup_report_{timestamp}.md"
        with open(report_file, "w") as f:
            f.write(report)

        logger.info(f"\n✅ Cleanup {'simulation' if dry_run else 'execution'} complete!")
        logger.info(f"📊 Results:")
        logger.info(f"   - Files {'would be' if dry_run else ''} removed: {results['files_removed']:,}")
        logger.info(f"   - Space {'would be' if dry_run else ''} saved: {results['space_saved_gb']:.2f} GB")
        logger.info(f"   - Backup files: {len(backup_log)}")
        logger.info(f"   - Reports saved: {json_file.name}, {report_file.name}")

        return results


def main():
    """main function."""

    logger.info("🧹 Smart Duplicate Cleaner for Documents")
    logger.info("=" * 50)

    # First run: Dry run to show what would happen
    logger.info("\n🔍 STEP 1: DRY RUN - Analyzing what would be cleaned...")
    cleaner = SmartDuplicateCleaner(Path("/Users/steven/Documents"), dry_run=True)
    dry_results = cleaner.run_cleanup(dry_run=True)

    logger.info(f"\n📋 DRY RUN SUMMARY:")
    logger.info(f"   - {dry_results['files_removed']:,} files would be removed")
    logger.info(f"   - {dry_results['space_saved_gb']:.2f} GB would be saved")

    # Ask for confirmation
    logger.info(f"\n❓ Do you want to proceed with the actual cleanup?")
    logger.info("   This will remove the duplicate files and create backups.")
    logger.info("   Type 'YES' to proceed, anything else to cancel:")

    response = input().strip().upper()

    if response == "YES":
        logger.info("\n🚀 STEP 2: LIVE CLEANUP - Removing duplicates...")
        cleaner_live = SmartDuplicateCleaner(Path("/Users/steven/Documents"), dry_run=False)
        live_results = cleaner_live.run_cleanup(dry_run=False)

        logger.info(f"\n🎉 CLEANUP COMPLETE!")
        logger.info(f"   - {live_results['files_removed']:,} files removed")
        logger.info(f"   - {live_results['space_saved_gb']:.2f} GB saved")
    else:
        logger.info("\n❌ Cleanup cancelled. Dry run results saved for review.")


if __name__ == "__main__":
    main()
