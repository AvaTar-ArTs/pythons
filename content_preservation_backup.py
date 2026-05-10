#!/usr/bin/env python3
"""
Content Preservation and Backup Script for NocturneMelodies

This script creates a comprehensive backup of all organized content
and ensures preservation of the work done across all versions.
"""

import hashlib
import json
import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path


def create_preservation_backup():
    """Create a comprehensive backup of all organized content"""

    print("Creating comprehensive preservation backup of all NocturneMelodies content...")

    # Define source directories (all the organized content)
    source_dirs = [
        "/Users/steven/Music/nocTurneMeLoDieS/CONSOLIDATED_HTML",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_WEB_STRUCTURE_V2",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_WEB_STRUCTURE_V3",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_FINAL_ORGANIZATION",
    ]

    # Create backup directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"/Users/steven/Music/nocTurneMeLoDieS/BACKUPS/NOCTURNEMELODIES_PRESERVATION_BACKUP_{timestamp}")
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Create a mapping of all organized content
    content_map = {}

    for source_dir in source_dirs:
        source_path = Path(source_dir)
        if source_path.exists():
            print(f"Backing up: {source_dir}")

            # Get the directory name for the backup structure
            dir_name = source_path.name

            # Copy the entire directory to backup location
            dest_path = backup_dir / dir_name
            if source_path.is_dir():
                shutil.copytree(source_path, dest_path, dirs_exist_ok=True)

            # Create content inventory for this directory
            inventory = []
            for root, dirs, files in os.walk(source_path):
                for file in files:
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(source_path)
                    file_stat = file_path.stat()

                    inventory.append(
                        {
                            "relative_path": str(rel_path),
                            "size_bytes": file_stat.st_size,
                            "modified": datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                            "checksum": calculate_file_checksum(file_path),
                        }
                    )

            content_map[dir_name] = inventory
            print(f"  - {len(inventory)} files inventoried")

    # Save the content map
    map_file = backup_dir / "content_preservation_map.json"
    with open(map_file, "w", encoding="utf-8") as f:
        json.dump(content_map, f, indent=2)

    # Create a summary file
    summary_file = backup_dir / "preservation_summary.txt"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("NocturneMelodies Content Preservation Summary\n")
        f.write("=" * 50 + "\n")
        f.write(f"Backup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Source Directories: {len(source_dirs)}\n\n")

        total_files = 0
        for dir_name, inventory in content_map.items():
            f.write(f"{dir_name}:\n")
            f.write(f"  - Files: {len(inventory)}\n")
            total_files += len(inventory)

        f.write(f"\nTotal Files Preserved: {total_files}\n")
        f.write(f"Backup Location: {backup_dir}\n")
        f.write("\nThis backup preserves all organized and mobile-optimized content.\n")

    # Create a ZIP archive for portability
    zip_path = Path(
        f"/Users/steven/Music/nocTurneMeLoDieS/BACKUPS/NOCTURNEMELODIES_COMPLETE_ORGANIZATION_{timestamp}.zip"
    )
    print(f"Creating ZIP archive: {zip_path}")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(backup_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(backup_dir.parent.parent)
                zipf.write(file_path, arc_path)

    print("\nContent preservation completed successfully!")
    print(f"Backup location: {backup_dir}")
    print(f"ZIP archive: {zip_path}")
    print(f"Total files preserved: {total_files}")
    print(f"Content map saved to: {map_file}")

    return backup_dir, zip_path, content_map


def calculate_file_checksum(file_path):
    """Calculate SHA256 checksum of a file"""
    try:
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read file in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except OSError:
        return "checksum_error"


def main():
    print("Starting comprehensive content preservation process...")
    print("This will create a complete backup of all organized NocturneMelodies content")

    # Create preservation backup
    backup_dir, zip_path, content_map = create_preservation_backup()

    print("\nPreservation process completed!")
    print(f"Backup directory: {backup_dir}")
    print(f"ZIP archive: {zip_path}")
    print(f"Content preservation map: {backup_dir}/content_preservation_map.json")
    print(f"Summary report: {backup_dir}/preservation_summary.txt")

    print("\nAll NocturneMelodies content has been preserved in an organized, mobile-optimized structure.")
    print("The backup includes all three versions (V1, V2, V3) plus the final organization.")


if __name__ == "__main__":
    main()
