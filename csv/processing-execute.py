"""
Data Processing Csv Execute 5

This module provides functionality for data processing csv execute 5.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Execute Smart Organization Plan
==============================
Executes the organization plan based on the CSV recommendations.
"""

import os
import csv
import shutil
from pathlib import Path
from datetime import datetime
import subprocess


class OrganizationExecutor:
    def __init__(self, csv_file_path):
        """__init__ function."""

        self.csv_file_path = csv_file_path
        self.organization_plan = []
        self.moved_files = []
        self.errors = []
        self.stats = {"total_files": 0, "moved_files": 0, "skipped_files": 0, "error_files": 0, "space_freed_mb": 0}

    def load_organization_plan(self):
        """Load the organization plan from CSV"""
        logger.info("📊 Loading organization plan...")

        with open(self.csv_file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.organization_plan.append(row)

        self.stats["total_files"] = len(self.organization_plan)
        logger.info(f"✅ Loaded {self.stats['total_files']} files for organization")

    def create_directories(self, destination_path):
        """Create necessary directories"""
        try:
            Path(destination_path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.info(f"❌ Error creating directory {destination_path}: {e}")
            return False

    def move_file(self, file_info):
        """Move a single file according to the plan"""
        source_path = file_info["full_path"]
        destination = file_info["suggested_destination"]
        file_name = file_info["file_name"]

        # Expand ~ to home directory
        if destination.startswith("~/"):
            destination = destination.replace("~", str(Path.home()))

        destination_path = Path(destination) / file_name

        try:
            # Check if source file exists
            if not os.path.exists(source_path):
                logger.info(f"⚠️  Source file not found: {source_path}")
                self.stats["skipped_files"] += 1
                return False

            # Create destination directory
            if not self.create_directories(destination_path.parent):
                return False

            # Check if destination already exists
            if os.path.exists(destination_path):
                logger.info(f"⚠️  Destination already exists: {destination_path}")
                # Add timestamp to avoid conflict
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                name_parts = file_name.rsplit(".", 1)
                if len(name_parts) == 2:
                    new_name = f"{name_parts[0]}_{timestamp}.{name_parts[1]}"
                else:
                    new_name = f"{file_name}_{timestamp}"
                destination_path = Path(destination) / new_name

            # Move the file
            shutil.move(source_path, destination_path)

            # Record the move
            move_record = {
                "file_name": file_name,
                "source_path": source_path,
                "destination_path": str(destination_path),
                "file_size_mb": float(file_info["file_size_mb"]),
                "moved_at": datetime.now().isoformat(),
                "restore_path": file_info["restore_path"],
            }
            self.moved_files.append(move_record)

            self.stats["moved_files"] += 1
            self.stats["space_freed_mb"] += float(file_info["file_size_mb"])

            logger.info(f"✅ Moved: {file_name} → {destination_path}")
            return True

        except Exception as e:
            error_record = {
                "file_name": file_name,
                "source_path": source_path,
                "destination_path": destination,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }
            self.errors.append(error_record)
            self.stats["error_files"] += 1
            logger.info(f"❌ Error moving {file_name}: {e}")
            return False

    def execute_organization(self, start_with_immediate=True, max_files=None):
        """Execute the organization plan"""
        logger.info("🚀 Starting organization execution...")

        # Filter files based on criteria
        files_to_move = []

        if start_with_immediate:
            # Start with immediate action files
            files_to_move = [f for f in self.organization_plan if f["immediate_action"] == "True"]
            logger.info(f"🎯 Starting with {len(files_to_move)} immediate action files")
        else:
            # Process all files
            files_to_move = self.organization_plan
            logger.info(f"📁 Processing all {len(files_to_move)} files")

        # Limit number of files if specified
        if max_files:
            files_to_move = files_to_move[:max_files]
            logger.info(f"🔢 Limited to first {max_files} files")

        # Sort by priority (highest first)
        files_to_move.sort(key=lambda x: int(x["priority"]), reverse=True)

        logger.info(f"\n📋 EXECUTION PLAN:")
        logger.info(f"   Files to process: {len(files_to_move)}")
        logger.info(f"   Starting with: {files_to_move[0]['file_name'] if files_to_move else 'None'}")
        logger.info(
            f"   Priority range: {files_to_move[0]['priority'] if files_to_move else 'N/A'} to {files_to_move[-1]['priority'] if files_to_move else 'N/A'}"
        )

        # Execute moves
        for i, file_info in enumerate(files_to_move, 1):
            logger.info(f"\n[{i}/{len(files_to_move)}] Processing: {file_info['file_name']}")
            logger.info(f"   Priority: {file_info['priority']}")
            logger.info(f"   Size: {file_info['file_size_mb']} MB")
            logger.info(f"   Destination: {file_info['suggested_destination']}")

            self.move_file(file_info)

            # Progress update every 10 files
            if i % 10 == 0:
                logger.info(f"\n📊 Progress: {i}/{len(files_to_move)} files processed")
                logger.info(f"   Moved: {self.stats['moved_files']}")
                logger.info(f"   Errors: {self.stats['error_files']}")
                logger.info(f"   Space freed: {self.stats['space_freed_mb']:.1f} MB")

    def save_execution_report(self):
        """Save execution report"""
        logger.info("💾 Saving execution report...")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save moved files log
        moved_csv = f"/Users/steven/Documents/python/moved_files_{timestamp}.csv"
        if self.moved_files:
            with open(moved_csv, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = [
                    "file_name",
                    "source_path",
                    "destination_path",
                    "file_size_mb",
                    "moved_at",
                    "restore_path",
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.moved_files)

        # Save errors log
        errors_csv = f"/Users/steven/Documents/python/organization_errors_{timestamp}.csv"
        if self.errors:
            with open(errors_csv, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["file_name", "source_path", "destination_path", "error", "timestamp"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.errors)

        # Save summary report
        summary_file = f"/Users/steven/Documents/python/organization_summary_{timestamp}.txt"
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write("ORGANIZATION EXECUTION SUMMARY\n")
            f.write("=" * 50 + Path("\n\n"))
            f.write(f"Execution Time: {datetime.now().isoformat()}\n")
            f.write(f"Total Files Processed: {self.stats['total_files']}\n")
            f.write(f"Files Moved Successfully: {self.stats['moved_files']}\n")
            f.write(f"Files Skipped: {self.stats['skipped_files']}\n")
            f.write(f"Files with Errors: {self.stats['error_files']}\n")
            f.write(f"Space Freed: {self.stats['space_freed_mb']:.2f} MB\n")
            f.write(f"Space Freed: {self.stats['space_freed_mb']/CONSTANT_1024:.2f} GB\n\n")

            if self.moved_files:
                f.write("MOVED FILES:\n")
                f.write("-" * 30 + Path("\n"))
                for file_info in self.moved_files[:10]:  # First 10
                    f.write(f"{file_info['file_name']} → {file_info['destination_path']}\n")
                if len(self.moved_files) > 10:
                    f.write(f"... and {len(self.moved_files) - 10} more files\n")

            if self.errors:
                f.write("\nERRORS:\n")
                f.write("-" * 30 + Path("\n"))
                for error in self.errors[:10]:  # First 10
                    f.write(f"{error['file_name']}: {error['error']}\n")
                if len(self.errors) > 10:
                    f.write(f"... and {len(self.errors) - 10} more errors\n")

        logger.info(f"✅ Reports saved:")
        if self.moved_files:
            logger.info(f"   📋 Moved files: {moved_csv}")
        if self.errors:
            logger.info(f"   ❌ Errors: {errors_csv}")
        logger.info(f"   📊 Summary: {summary_file}")

        return moved_csv, errors_csv, summary_file

    def print_summary(self):
        """Print execution summary"""
        logger.info(Path("\n") + "=" * 80)
        logger.info("🎯 ORGANIZATION EXECUTION SUMMARY")
        logger.info("=" * 80)

        logger.info(f"\n📊 STATISTICS:")
        logger.info(f"   Total files processed: {self.stats['total_files']:,}")
        logger.info(f"   Files moved successfully: {self.stats['moved_files']:,}")
        logger.info(f"   Files skipped: {self.stats['skipped_files']:,}")
        logger.info(f"   Files with errors: {self.stats['error_files']:,}")
        logger.info(
            f"   Space freed: {self.stats['space_freed_mb']:.2f} MB ({self.stats['space_freed_mb']/CONSTANT_1024:.2f} GB)"
        )

        if self.moved_files:
            logger.info(f"\n✅ TOP MOVED FILES:")
            for i, file_info in enumerate(self.moved_files[:5], 1):
                logger.info(f"   {i}. {file_info['file_name']} ({file_info['file_size_mb']:.1f} MB)")
                logger.info(f"      → {file_info['destination_path']}")

        if self.errors:
            logger.info(f"\n❌ ERRORS ENCOUNTERED:")
            for i, error in enumerate(self.errors[:5], 1):
                logger.info(f"   {i}. {error['file_name']}: {error['error']}")

        logger.info(f"\n💡 NEXT STEPS:")
        logger.info(f"   1. Review the execution reports")
        logger.info(f"   2. Check moved files in their new locations")
        logger.info(f"   3. Use restore information if needed")
        logger.info(f"   4. Continue with remaining files if desired")


def main():
    """Main function"""
    logger.info("🚀 Execute Smart Organization Plan")
    logger.info("=" * 50)

    # Find the most recent organization plan CSV
    csv_files = list(Path("/Users/steven/Documents/python").glob("smart_organization_plan_*.csv"))
    if not csv_files:
        logger.info("❌ No organization plan CSV found. Please run smart_organization_plan.py first.")
        return

    latest_csv = max(csv_files, key=lambda x: x.stat().st_mtime)
    logger.info(f"📁 Using organization plan: {latest_csv}")

    # Initialize executor
    executor = OrganizationExecutor(str(latest_csv))

    # Load plan
    executor.load_organization_plan()

    # Execute with immediate action files only (automated)
    logger.info(f"\n🎯 EXECUTING: Starting with immediate action files only")
    logger.info(f"   This will process the highest priority files first")

    # Process immediate action files only
    executor.execute_organization(start_with_immediate=True)

    # Save reports
    executor.save_execution_report()

    # Print summary
    executor.print_summary()

    logger.info(f"\n✅ Organization execution complete!")


if __name__ == "__main__":
    main()
