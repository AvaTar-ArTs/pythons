#!/usr/bin/env python3
"""
Script to create a backup mapping of the current iCloud NocturneMelodies collection.
This creates a CSV that can be used to restore files to their original locations if needed.
"""

import os
from datetime import datetime
from pathlib import Path


def get_file_metadata(file_path: Path) -> dict:
    """Extract metadata from a file."""
    file_stat = file_path.stat()
    return {
        "file_size": file_stat.st_size,
        "creation_date": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
        "modification_date": datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
    }


def create_icloud_backup_mapping():
    """Create a CSV mapping of the current iCloud collection."""

    # Source directory (iCloud collection)
    source_dir = Path("/Users/steven/Library/Mobile Documents/com~apple~CloudDocs/nocTurneMeLoDieS")

    # Output CSV file
    csv_file = Path("/Users/steven/Music/nocTurneMeLoDieS/icloud_collection_backup_mapping.csv")

    if not source_dir.exists():
        print(f"Error: Source directory does not exist: {source_dir}")
        return

    # Get current timestamp
    backup_timestamp = datetime.now().isoformat()

    # Count total files
    total_files = 0
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith((".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg")):
                total_files += 1

    print(f"Found {total_files} audio files in iCloud collection")

    # Open CSV file for appending (skip header since we already created it)
    with open(csv_file, "a", newline="", encoding="utf-8") as csvfile:
        file_count = 0
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.lower().endswith((".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg")):
                    original_path = Path(root) / file
                    if original_path.is_file():
                        # Get file metadata
                        metadata = get_file_metadata(original_path)

                        # Write to CSV
                        csvfile.write(
                            f'"{str(original_path.absolute())}","{str(original_path.absolute())}",{metadata["file_size"]},"{metadata["creation_date"]}","{metadata["modification_date"]}","{backup_timestamp}"\n'
                        )

                        file_count += 1
                        if file_count % 50 == 0:  # Progress indicator
                            print(f"Processed {file_count}/{total_files} files...")

    print(f"\nBackup mapping completed: {csv_file}")
    print(f"Total files mapped: {file_count}")
    print("CSV file can be used to restore files to their original locations if needed.")


if __name__ == "__main__":
    print("Creating backup mapping for iCloud NocturneMelodies collection...")
    print("This may take a few minutes depending on the number of files...")
    create_icloud_backup_mapping()
    print("Done! You can now proceed with the synchronization.")
