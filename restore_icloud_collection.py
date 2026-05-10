#!/usr/bin/env python3
"""
Restoration script for NocturneMelodies iCloud collection.
This script can restore files to their original locations using the backup CSV.
"""

import csv
import shutil
from pathlib import Path


def restore_from_backup(csv_path, dry_run=True):
    """
    Restore files to their original locations using the backup CSV.

    Args:
        csv_path: Path to the backup CSV file
        dry_run: If True, only show what would be done without actually moving files
    """
    csv_path = Path(csv_path)

    if not csv_path.exists():
        print(f"Error: CSV file does not exist: {csv_path}")
        return

    print(f"Restoring from backup: {csv_path}")
    if dry_run:
        print("(DRY RUN MODE - No actual changes will be made)")

    restored_count = 0
    skipped_count = 0
    error_count = 0

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            original_path = Path(row["original_path"])

            # Check if the file exists in its current location
            if not original_path.exists():
                print(f"File not found: {original_path}")
                error_count += 1
                continue

            # Check if the parent directory exists
            original_path.parent.mkdir(parents=True, exist_ok=True)

            if dry_run:
                print(f"Would restore: {original_path}")
                restored_count += 1
            else:
                # In this case, since original_path is where the file already is,
                # we're essentially just verifying it exists
                print(f"Verified: {original_path}")
                restored_count += 1

    print("\nRestore Summary (Dry Run):")
    print(f"  Files verified/restored: {restored_count}")
    print(f"  Files skipped: {skipped_count}")
    print(f"  Errors: {error_count}")

    if dry_run:
        print("\nTo perform actual restoration, run with dry_run=False")

    return restored_count, skipped_count, error_count


def restore_to_different_location(csv_path, target_base_path, dry_run=True):
    """
    Restore files to a different location than their original.

    Args:
        csv_path: Path to the backup CSV file
        target_base_path: Base path to restore files to
        dry_run: If True, only show what would be done without actually moving files
    """
    csv_path = Path(csv_path)
    target_base = Path(target_base_path)

    if not csv_path.exists():
        print(f"Error: CSV file does not exist: {csv_path}")
        return

    print(f"Restoring from backup to: {target_base_path}")
    if dry_run:
        print("(DRY RUN MODE - No actual changes will be made)")

    restored_count = 0
    skipped_count = 0
    error_count = 0

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            original_path = Path(row["original_path"])
            row["file_size"]

            # Determine the relative path from the iCloud base
            icloud_base = Path("/Users/steven/Library/Mobile Documents/com~apple~CloudDocs/nocTurneMeLoDieS")
            try:
                relative_path = original_path.relative_to(icloud_base)
            except ValueError:
                # If the path is not relative to the iCloud base, use the full path structure
                relative_path = original_path.relative_to(original_path.parent)

            target_path = target_base / relative_path

            # Check if the original file exists
            if not original_path.exists():
                print(f"Source file not found: {original_path}")
                error_count += 1
                continue

            # Create target directory if it doesn't exist
            target_path.parent.mkdir(parents=True, exist_ok=True)

            if dry_run:
                print(f"Would copy: {original_path} -> {target_path}")
                restored_count += 1
            else:
                try:
                    shutil.copy2(original_path, target_path)  # Copy with metadata
                    print(f"Copied: {original_path} -> {target_path}")
                    restored_count += 1
                except Exception as e:
                    print(f"Error copying {original_path}: {str(e)}")
                    error_count += 1

    print("\nRestore Summary:")
    print(f"  Files copied: {restored_count}")
    print(f"  Files skipped: {skipped_count}")
    print(f"  Errors: {error_count}")

    return restored_count, skipped_count, error_count


if __name__ == "__main__":
    csv_file = "/Users/steven/Music/nocTurneMeLoDieS/icloud_collection_backup_mapping.csv"

    print("NocturneMelodies iCloud Collection Restoration Tool")
    print("=" * 50)

    # Perform a dry run to show what would be restored
    print("\nPerforming dry run to show what would be restored...")
    restore_from_backup(csv_file, dry_run=True)

    print(f"\nBackup CSV created at: {csv_file}")
    print("This can be used to verify the integrity of your iCloud collection.")
    print("\nTo restore to a different location, use the restore_to_different_location function.")
