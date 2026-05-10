#!/usr/bin/env python3
"""
NocturneMelodies Collection Backup Script
Creates a CSV mapping of original file paths to new locations with metadata
and includes a restore function for the NocturneMelodies collection.
"""

import argparse
import csv
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


def get_file_metadata(file_path: Path) -> dict:
    """Extract metadata from a file."""
    stat = file_path.stat()
    return {
        "file_size": stat.st_size,
        "creation_date": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modification_date": datetime.fromtimestamp(stat.st_mtime).isoformat(),
    }


def create_backup_mapping(source_dir: str, destination_dir: str, csv_output: str):
    """
    Create a CSV file mapping original file paths to new locations with metadata.

    Args:
        source_dir: Source directory to scan
        destination_dir: Destination directory for organized files
        csv_output: Path to output CSV file
    """
    source_path = Path(source_dir)
    dest_path = Path(destination_dir)

    if not source_path.exists():
        print(f"Error: Source directory does not exist: {source_dir}")
        return False

    # Create destination directory if it doesn't exist
    dest_path.mkdir(parents=True, exist_ok=True)

    backup_timestamp = datetime.now().isoformat()

    with open(csv_output, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "original_path",
            "new_path",
            "file_size",
            "creation_date",
            "modification_date",
            "backup_timestamp",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        file_count = 0
        for root, dirs, files in os.walk(source_path):
            for file in files:
                original_path = Path(root) / file
                if original_path.is_file():
                    # Calculate relative path from source to determine new location
                    rel_path = original_path.relative_to(source_path)
                    new_path = dest_path / rel_path

                    # Get file metadata
                    metadata = get_file_metadata(original_path)

                    # Write to CSV
                    writer.writerow(
                        {
                            "original_path": str(original_path.absolute()),
                            "new_path": str(new_path.absolute()),
                            "file_size": metadata["file_size"],
                            "creation_date": metadata["creation_date"],
                            "modification_date": metadata["modification_date"],
                            "backup_timestamp": backup_timestamp,
                        }
                    )

                    file_count += 1

        print(f"Backup mapping created: {csv_output}")
        print(f"Total files mapped: {file_count}")

    return True


def create_icloud_collection_backup(source_dirs: list, backup_name: str = None):
    """
    Create a timestamped backup of the iCloud collection.

    Args:
        source_dirs: List of source directories to backup
        backup_name: Optional custom name for the backup
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = backup_name or f"icloud_collection_backup_{timestamp}"

    backup_dir = Path.home() / "Music" / "nocTurneMeLoDieS" / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)

    backup_path = backup_dir / backup_name
    backup_path.mkdir(parents=True, exist_ok=True)

    print(f"Creating iCloud collection backup: {backup_path}")

    for source_dir in source_dirs:
        source_path = Path(source_dir)
        if not source_path.exists():
            print(f"Warning: Source directory does not exist: {source_dir}")
            continue

        dest_path = backup_path / source_path.name
        print(f"Copying: {source_path} -> {dest_path}")
        shutil.copytree(source_path, dest_path, dirs_exist_ok=True)

    print(f"iCloud collection backup completed: {backup_path}")
    return str(backup_path)


def restore_from_csv(csv_path: str, dry_run: bool = False):
    """
    Restore files to their original locations using the CSV mapping.

    Args:
        csv_path: Path to the CSV backup file
        dry_run: If True, only show what would be restored without actually restoring
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        print(f"Error: CSV file does not exist: {csv_path}")
        return

    print(f"Restoring from CSV: {csv_path}")
    if dry_run:
        print("(Dry run mode - no actual files will be moved)")

    restored_count = 0
    skipped_count = 0
    error_count = 0

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            original_path = Path(row["original_path"])
            new_path = Path(row["new_path"])

            # Check if the new file exists
            if not new_path.exists():
                print(f"Missing file: {new_path}")
                error_count += 1
                continue

            # Check if original path exists
            if original_path.exists():
                print(f"File already exists at original location: {original_path}")
                skipped_count += 1
                continue

            # Create parent directories if they don't exist
            original_path.parent.mkdir(parents=True, exist_ok=True)

            if not dry_run:
                try:
                    shutil.copy2(new_path, original_path)  # Copy with metadata
                    print(f"Restored: {new_path} -> {original_path}")
                    restored_count += 1
                except Exception as e:
                    print(f"Error restoring {new_path}: {str(e)}")
                    error_count += 1
            else:
                print(f"Would restore: {new_path} -> {original_path}")
                restored_count += 1

    print("\nRestore Summary:")
    print(f"  Files restored: {restored_count}")
    print(f"  Files skipped: {skipped_count}")
    print(f"  Errors: {error_count}")


def main():
    parser = argparse.ArgumentParser(description="NocturneMelodies Collection Backup Script")
    parser.add_argument(
        "--action",
        choices=["backup", "restore", "both"],
        default="both",
        help="Action to perform",
    )
    parser.add_argument("--source", help="Source directory to backup")
    parser.add_argument("--destination", help="Destination directory for organized files")
    parser.add_argument("--csv", help="Path to CSV mapping file")
    parser.add_argument("--restore-csv", help="Path to CSV file for restoration")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually doing it",
    )

    args = parser.parse_args()

    if args.action in ["backup", "both"]:
        if not args.source or not args.destination or not args.csv:
            print("For backup action, please provide --source, --destination, and --csv arguments")
            sys.exit(1)

        print("Creating backup mapping...")
        success = create_backup_mapping(args.source, args.destination, args.csv)
        if not success:
            sys.exit(1)

        # Also create a full backup of the source directory
        print("Creating full backup of source directory...")
        create_icloud_collection_backup([args.source])

    if args.action in ["restore", "both"]:
        if not args.restore_csv:
            if args.csv:
                args.restore_csv = args.csv
            else:
                print("For restore action, please provide --restore-csv argument")
                sys.exit(1)

        restore_from_csv(args.restore_csv, dry_run=args.dry_run)


if __name__ == "__main__":
    # If no arguments provided, run in interactive mode
    if len(sys.argv) == 1:
        print("NocturneMelodies Collection Backup Script")
        print("=" * 50)

        # Default directories for NocturneMelodies collection
        source_dir = (
            input("Enter source directory (default: /Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED): ")
            or "/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED"
        )
        destination_dir = (
            input(
                "Enter destination directory (default: /Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED_BACKUP): "
            )
            or "/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED_BACKUP"
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"nocturnemelodies_backup_{timestamp}.csv"
        csv_path = f"/Users/steven/Music/nocTurneMeLoDieS/backups/{csv_filename}"

        print("\nCreating backup mapping...")
        success = create_backup_mapping(source_dir, destination_dir, csv_path)

        if success:
            print(f"\nBackup mapping created: {csv_path}")

            # Create full backup of source directories
            source_dirs = [source_dir]
            print("\nCreating full backup of source directories...")
            create_icloud_collection_backup(source_dirs)

            print("\nBackup completed successfully!")
            print(f"CSV mapping file: {csv_path}")

            # Ask if user wants to see restore instructions
            restore_help = input("\nWould you like to see restore instructions? (y/n): ")
            if restore_help.lower() == "y":
                print("\nTo restore files from the backup, use:")
                print(f"python {__file__} --action restore --restore-csv {csv_path}")
                print("For a dry run (to see what would be restored):")
                print(f"python {__file__} --action restore --restore-csv {csv_path} --dry-run")
    else:
        main()
