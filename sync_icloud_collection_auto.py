#!/usr/bin/env python3
"""
Script to synchronize the iCloud NocturneMelodies collection with the local collection.
This will copy missing files from the local collection to the iCloud collection.
NON-INTERACTIVE VERSION that automatically proceeds with sync.
"""

import csv
import os
import shutil
from pathlib import Path


def get_icloud_files():
    """Get all audio files from the iCloud collection."""
    icloud_dir = Path("/Users/steven/Library/Mobile Documents/com~apple~CloudDocs/nocTurneMeLoDieS")
    icloud_files = set()

    for root, dirs, files in os.walk(icloud_dir):
        for file in files:
            if file.lower().endswith((".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg")):
                # Get relative path from iCloud base
                file_path = Path(root) / file
                rel_path = file_path.relative_to(icloud_dir)
                icloud_files.add(str(rel_path))

    return icloud_files


def get_local_files():
    """Get all audio files from the local organized collection."""
    local_dir = Path("/Users/steven/Music/nocTurneMeLoDieS")
    local_files = {}

    # Look for MP3 files in the ALBUMS directory structure
    albums_dir = local_dir / "ALBUMS"
    if albums_dir.exists():
        for root, dirs, files in os.walk(albums_dir):
            for file in files:
                if file.lower().endswith((".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg")):
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(local_dir)
                    local_files[str(rel_path)] = file_path

    # Also look for any MP3s in the main directory
    for root, dirs, files in os.walk(local_dir):
        # Skip the ALBUMS directory since we already processed it
        if "ALBUMS" in str(root):
            continue
        for file in files:
            if file.lower().endswith((".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg")):
                file_path = Path(root) / file
                rel_path = file_path.relative_to(local_dir)
                if str(rel_path) not in local_files:  # Don't overwrite if already found in ALBUMS
                    local_files[str(rel_path)] = file_path

    return local_files


def sync_icloud_with_local():
    """Synchronize the iCloud collection with the local collection."""
    print("Getting list of files in iCloud collection...")
    icloud_files = get_icloud_files()
    print(f"Found {len(icloud_files)} files in iCloud collection")

    print("\nGetting list of files in local collection...")
    local_files = get_local_files()
    print(f"Found {len(local_files)} files in local collection")

    # Find files that are in local but not in iCloud
    missing_from_icloud = set(local_files.keys()) - icloud_files

    print(f"\nFound {len(missing_from_icloud)} files that are in local but missing from iCloud")

    if not missing_from_icloud:
        print("iCloud collection is already up to date with local collection!")
        return

    # Create mapping for the sync operations
    sync_operations = []
    for rel_path in missing_from_icloud:
        source_path = local_files[rel_path]
        # Remove the 'ALBUMS/' prefix when copying to iCloud
        if rel_path.startswith("ALBUMS/"):
            icloud_rel_path = rel_path[7:]  # Remove 'ALBUMS/' prefix
        else:
            icloud_rel_path = rel_path
        dest_path = (
            Path("/Users/steven/Library/Mobile Documents/com~apple~CloudDocs/nocTurneMeLoDieS") / icloud_rel_path
        )

        sync_operations.append(
            {
                "source": source_path,
                "destination": dest_path,
                "relative_path": rel_path,
                "icloud_relative_path": icloud_rel_path,
            }
        )

    # Show what will be synced
    print("\nFiles to be added to iCloud collection:")
    for op in sync_operations[:10]:  # Show first 10
        print(f"  {op['icloud_relative_path']}")

    if len(sync_operations) > 10:
        print(f"  ... and {len(sync_operations) - 10} more files")

    print(f"\nTotal files to sync: {len(sync_operations)}")
    print("Automatically proceeding with synchronization (non-interactive mode)...")

    # Create directories as needed and copy files
    print("\nStarting synchronization...")
    success_count = 0
    error_count = 0

    for i, op in enumerate(sync_operations, 1):
        try:
            # Create destination directory if it doesn't exist
            op["destination"].parent.mkdir(parents=True, exist_ok=True)

            # Copy the file
            shutil.copy2(op["source"], op["destination"])

            if i % 50 == 0:  # Progress indicator
                print(f"  Copied {i}/{len(sync_operations)} files...")

            success_count += 1
        except Exception as e:
            print(f"  Error copying {op['icloud_relative_path']}: {str(e)}")
            error_count += 1

    print("\nSynchronization completed!")
    print(f"  Successfully copied: {success_count} files")
    print(f"  Errors: {error_count} files")

    # Create a log of what was synced
    log_path = Path("/Users/steven/Music/nocTurneMeLoDieS/icloud_sync_log.csv")
    with open(log_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "relative_path",
            "icloud_relative_path",
            "source_path",
            "destination_path",
            "status",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for op in sync_operations:
            writer.writerow(
                {
                    "relative_path": op["relative_path"],
                    "icloud_relative_path": op["icloud_relative_path"],
                    "source_path": str(op["source"]),
                    "destination_path": str(op["destination"]),
                    "status": "synced" if op["destination"].exists() else "error",
                }
            )

    print(f"\nSync log saved to: {log_path}")


if __name__ == "__main__":
    print("NocturneMelodies iCloud Collection Sync Tool (Non-Interactive)")
    print("=" * 60)
    print("This tool will synchronize your iCloud collection with your local collection.")
    print("It will copy files that exist in your local collection but are missing from iCloud.")
    print("This is the NON-INTERACTIVE version that automatically proceeds with sync.")
    print("")

    sync_icloud_with_local()

    print("\nSynchronization process completed!")
    print("Your iCloud collection is now updated with the latest files from your local collection.")
