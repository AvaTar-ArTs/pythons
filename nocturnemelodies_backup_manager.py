#!/usr/bin/env python3
"""
NocturneMelodies Backup Manager
A comprehensive backup solution that creates CSV mappings of file locations with metadata
and provides restoration capabilities for the NocturneMelodies collection.
"""

import csv
import json
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path


class NocturneBackupManager:
    def __init__(self, base_path: str = "/Users/steven/Music/nocTurneMeLoDieS"):
        self.base_path = Path(base_path)
        self.backup_dir = self.base_path / "backups"
        self.backup_dir.mkdir(exist_ok=True)

    def get_file_metadata(self, file_path: Path) -> dict[str, str]:
        """Extract metadata from a file."""
        stat = file_path.stat()
        return {
            "file_size": str(stat.st_size),
            "creation_date": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modification_date": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        }

    def generate_backup_mapping(
        self,
        source_dirs: list[str],
        destination_dir: str,
        backup_name: str | None = None,
    ) -> str:
        """
        Generate a CSV file mapping original file paths to new locations with metadata.

        Args:
            source_dirs: List of source directories to scan
            destination_dir: Destination directory for the organized files
            backup_name: Optional custom name for the backup

        Returns:
            Path to the generated CSV file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_id = backup_name or f"nocturnemelodies_backup_{timestamp}_{uuid.uuid4().hex[:8]}"

        csv_path = self.backup_dir / f"{backup_id}.csv"

        backup_data = []
        backup_timestamp = datetime.now().isoformat()

        for source_dir in source_dirs:
            source_path = Path(source_dir)
            if not source_path.exists():
                print(f"Warning: Source directory does not exist: {source_dir}")
                continue

            print(f"Scanning: {source_dir}")

            for root, dirs, files in os.walk(source_path):
                for file in files:
                    original_path = Path(root) / file
                    if original_path.is_file():
                        # Calculate relative path from source to determine new location
                        rel_path = original_path.relative_to(source_path)
                        new_path = Path(destination_dir) / rel_path

                        # Get file metadata
                        metadata = self.get_file_metadata(original_path)

                        # Create backup record
                        record = {
                            "original_path": str(original_path.absolute()),
                            "new_path": str(new_path.absolute()),
                            "file_size": metadata["file_size"],
                            "creation_date": metadata["creation_date"],
                            "modification_date": metadata["modification_date"],
                            "backup_timestamp": backup_timestamp,
                        }

                        backup_data.append(record)

        # Write CSV file
        with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
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
            for record in backup_data:
                writer.writerow(record)

        print(f"Backup mapping created: {csv_path}")
        print(f"Total files mapped: {len(backup_data)}")

        # Also create a summary JSON file
        summary_path = self.backup_dir / f"{backup_id}_summary.json"
        summary = {
            "backup_id": backup_id,
            "timestamp": backup_timestamp,
            "source_directories": source_dirs,
            "destination_directory": destination_dir,
            "total_files": len(backup_data),
            "csv_file": str(csv_path.name),
        }

        with open(summary_path, "w", encoding="utf-8") as jsonfile:
            json.dump(summary, jsonfile, indent=2)

        print(f"Summary created: {summary_path}")

        return str(csv_path)

    def create_icloud_collection_backup(self, source_dirs: list[str], backup_name: str | None = None) -> str:
        """
        Create a timestamped backup of the iCloud collection.

        Args:
            source_dirs: List of source directories to backup
            backup_name: Optional custom name for the backup

        Returns:
            Path to the backup directory
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_id = backup_name or f"icloud_collection_backup_{timestamp}_{uuid.uuid4().hex[:8]}"
        backup_path = self.backup_dir / backup_id

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

    def restore_from_csv(self, csv_path: str, dry_run: bool = True) -> list[dict[str, str]]:
        """
        Restore files to their original locations using the CSV mapping.

        Args:
            csv_path: Path to the CSV backup file
            dry_run: If True, only show what would be restored without actually restoring

        Returns:
            List of restoration records with status
        """
        csv_path = Path(csv_path)
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file does not exist: {csv_path}")

        print(f"Restoring from CSV: {csv_path}")
        if dry_run:
            print("(Dry run mode - no actual files will be moved)")

        restoration_results = []

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                original_path = Path(row["original_path"])
                new_path = Path(row["new_path"])

                result = {
                    "original_path": str(original_path),
                    "new_path": str(new_path),
                    "status": "",
                    "message": "",
                }

                # Check if the new file exists
                if not new_path.exists():
                    result["status"] = "missing"
                    result["message"] = "New file does not exist"
                    restoration_results.append(result)
                    continue

                # Check if original path exists
                if original_path.exists():
                    result["status"] = "exists"
                    result["message"] = "Original file already exists"
                    restoration_results.append(result)
                    continue

                # Create parent directories if they don't exist
                original_path.parent.mkdir(parents=True, exist_ok=True)

                if not dry_run:
                    try:
                        shutil.copy2(new_path, original_path)  # Copy with metadata
                        result["status"] = "restored"
                        result["message"] = "File restored successfully"
                    except Exception as e:
                        result["status"] = "error"
                        result["message"] = f"Restore failed: {str(e)}"
                else:
                    result["status"] = "would_restore"
                    result["message"] = "Would restore file (dry run)"

                restoration_results.append(result)

        # Print summary
        statuses = [r["status"] for r in restoration_results]
        print("\nRestoration Summary:")
        print(f"  Total files processed: {len(restoration_results)}")
        print(f"  Files restored: {statuses.count('restored')}")
        print(f"  Files would be restored: {statuses.count('would_restore')}")
        print(f"  Original files already existed: {statuses.count('exists')}")
        print(f"  Missing new files: {statuses.count('missing')}")
        print(f"  Errors: {statuses.count('error')}")

        return restoration_results

    def validate_backup_integrity(self, csv_path: str) -> dict[str, int]:
        """
        Validate the integrity of the backup by checking file existence and sizes.

        Args:
            csv_path: Path to the CSV backup file

        Returns:
            Dictionary with validation statistics
        """
        csv_path = Path(csv_path)
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file does not exist: {csv_path}")

        stats = {
            "total_files": 0,
            "original_exists": 0,
            "new_exists": 0,
            "size_matches": 0,
            "size_mismatches": 0,
        }

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                stats["total_files"] += 1

                original_path = Path(row["original_path"])
                new_path = Path(row["new_path"])
                expected_size = int(row["file_size"])

                if original_path.exists():
                    stats["original_exists"] += 1
                    actual_size = original_path.stat().st_size
                    if actual_size == expected_size:
                        stats["size_matches"] += 1
                    else:
                        stats["size_mismatches"] += 1

                if new_path.exists():
                    stats["new_exists"] += 1
                    actual_size = new_path.stat().st_size
                    if actual_size == expected_size:
                        stats["size_matches"] += 1
                    else:
                        stats["size_mismatches"] += 1

        print("\nIntegrity Validation Results:")
        print(f"  Total files checked: {stats['total_files']}")
        print(f"  Original files exist: {stats['original_exists']}")
        print(f"  New files exist: {stats['new_exists']}")
        print(f"  Size matches: {stats['size_matches']}")
        print(f"  Size mismatches: {stats['size_mismatches']}")

        return stats


def main():
    """Main function demonstrating the backup manager functionality."""
    manager = NocturneBackupManager()

    # Define source directories (you can customize these based on your collection)
    source_directories = [
        "/Users/steven/AVATARARTS/HEAVENLY_HANDS_PROJECT",
        "/Users/steven/AVATARARTS/DR_ADU_PROJECT",
        "/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED",
    ]

    destination_directory = "/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED_BACKUP"

    print("=== NocturneMelodies Backup Manager ===\n")

    # Create iCloud collection backup
    print("1. Creating iCloud collection backup...")
    backup_path = manager.create_icloud_collection_backup(source_directories)

    # Generate backup mapping CSV
    print("\n2. Generating backup mapping CSV...")
    csv_path = manager.generate_backup_mapping(
        source_directories,
        destination_directory,
        backup_name="nocturnemelodies_collection",
    )

    print("\nBackup completed!")
    print(f"  - Backup directory: {backup_path}")
    print(f"  - CSV mapping: {csv_path}")

    # Example of how to restore (in dry-run mode)
    print("\n3. Example restore operation (dry-run)...")
    manager.restore_from_csv(csv_path, dry_run=True)

    # Example of integrity validation
    print("\n4. Validating backup integrity...")
    manager.validate_backup_integrity(csv_path)


if __name__ == "__main__":
    main()
