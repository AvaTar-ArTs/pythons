#!/usr/bin/env python3
"""
Test script for NocturneMelodies Collection Backup Script
"""

import csv
import sys
import tempfile
from pathlib import Path


def test_backup_script():
    """Test the backup script functionality."""
    print("Testing NocturneMelodies Collection Backup Script...")

    # Create temporary directories for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create test source directory with some sample files
        source_dir = temp_path / "test_source"
        source_dir.mkdir()

        # Create some test files
        test_files = ["test1.mp3", "test2.wav", "test3.flac"]
        for filename in test_files:
            test_file = source_dir / filename
            with open(test_file, "w") as f:
                f.write(f"This is a test file: {filename}")

        # Create destination directory
        dest_dir = temp_path / "test_destination"

        # Create backup directory
        backup_dir = temp_path / "backups"
        backup_dir.mkdir()

        # Test CSV path
        csv_path = backup_dir / "test_backup.csv"

        print("Created test environment:")
        print(f"  Source: {source_dir}")
        print(f"  Destination: {dest_dir}")
        print(f"  CSV: {csv_path}")

        # Import the backup script functions
        sys.path.insert(0, "/Users/steven/Music/nocTurneMeLoDieS")
        from nocturnemelodies_collection_backup import create_backup_mapping

        # Test the backup mapping function
        print("\nTesting backup mapping creation...")
        success = create_backup_mapping(str(source_dir), str(dest_dir), str(csv_path))

        if success:
            print("✓ Backup mapping created successfully")

            # Verify CSV file exists and has correct structure
            if csv_path.exists():
                print("✓ CSV file created")

                # Read and verify CSV structure
                with open(csv_path, newline="") as csvfile:
                    reader = csv.DictReader(csvfile)
                    headers = reader.fieldnames

                    expected_headers = [
                        "original_path",
                        "new_path",
                        "file_size",
                        "creation_date",
                        "modification_date",
                        "backup_timestamp",
                    ]

                    if set(headers) == set(expected_headers):
                        print("✓ CSV headers are correct")
                    else:
                        print(f"✗ CSV headers mismatch. Expected: {expected_headers}, Got: {headers}")
                        return False

                    # Count rows
                    rows = list(reader)
                    print(f"✓ Found {len(rows)} rows in CSV")

                    # Verify each row has all required fields
                    for i, row in enumerate(rows):
                        missing_fields = [field for field in expected_headers if not row.get(field)]
                        if missing_fields:
                            print(f"✗ Row {i} missing fields: {missing_fields}")
                            return False

                    print("✓ All rows have required fields")

                    # Verify file paths exist in the original source
                    for row in rows:
                        orig_path = Path(row["original_path"])
                        if not orig_path.exists():
                            print(f"✗ Original path does not exist: {orig_path}")
                            return False

                    print("✓ All original paths exist")

            else:
                print("✗ CSV file was not created")
                return False

        else:
            print("✗ Failed to create backup mapping")
            return False

    print("\n✓ All tests passed!")
    return True


def run_example_usage():
    """Run an example usage of the backup script."""
    print("\nExample usage:")
    print("-------------")
    print("# Create a backup of your music collection")
    print("python nocturnemelodies_collection_backup.py --action backup \\")
    print('  --source "/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED" \\')
    print('  --destination "/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED_BACKUP" \\')
    print('  --csv "/Users/steven/Music/nocTurneMeLoDieS/backups/my_backup.csv"')
    print()
    print("# Later, restore files from the backup")
    print("python nocturnemelodies_collection_backup.py --action restore \\")
    print('  --restore-csv "/Users/steven/Music/nocTurneMeLoDieS/backups/my_backup.csv"')


if __name__ == "__main__":
    success = test_backup_script()
    if success:
        run_example_usage()
    else:
        print("\nTests failed!")
        sys.exit(1)
