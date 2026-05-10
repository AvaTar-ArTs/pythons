#!/usr/bin/env python3
"""
Backup and Archival Script for NocturneMelodies Content Organization Project

This script creates a comprehensive backup of all the work done on organizing
and optimizing HTML content in the NocturneMelodies project.
"""

import json
import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path


def create_backup():
    """Create a comprehensive backup of all NocturneMelodies organization work"""

    print("Creating comprehensive backup of NocturneMelodies organization project...")

    # Define source directories (all the work we've done)
    source_dirs = [
        "/Users/steven/Music/nocTurneMeLoDieS/CONSOLIDATED_HTML",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_WEB_STRUCTURE_V2",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_WEB_STRUCTURE_V3",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_FINAL_ORGANIZATION",
        "/Users/steven/Music/nocTurneMeLoDieS/AVATARARTS_CONSOLIDATION_PROJECT",
    ]

    # Create backup directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"/Users/steven/Music/nocTurneMeLoDieS/BACKUPS/NOCTURNEMELODIES_ORGANIZATION_BACKUP_{timestamp}")
    backup_dir.mkdir(parents=True, exist_ok=True)

    print(f"Backup directory created: {backup_dir}")

    # Create a backup manifest
    manifest = {
        "backup_timestamp": datetime.now().isoformat(),
        "project": "NocturneMelodies Content Organization",
        "description": "Complete backup of HTML content organization and mobile optimization work",
        "directories_backed_up": [],
        "files_count": {},
        "backup_size": 0,
    }

    # Copy each directory to the backup location
    for source_dir in source_dirs:
        source_path = Path(source_dir)
        if source_path.exists():
            dest_path = backup_dir / source_path.name
            print(f"Backing up: {source_dir} -> {dest_path}")

            # Copy the directory
            if source_path.is_dir():
                shutil.copytree(source_path, dest_path, dirs_exist_ok=True)

                # Count files in directory
                file_count = sum([len(files) for _, _, files in os.walk(source_path)])
                manifest["files_count"][source_path.name] = file_count
                manifest["directories_backed_up"].append(str(source_path))

                # Calculate directory size
                dir_size = sum(f.stat().st_size for f in source_path.rglob("*") if f.is_file())
                manifest["backup_size"] += dir_size

    # Save manifest
    manifest_path = backup_dir / "backup_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Backup manifest saved: {manifest_path}")

    # Create a summary file
    summary_path = backup_dir / "backup_summary.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("NocturneMelodies Content Organization Backup Summary\n")
        f.write("=" * 50 + "\n")
        f.write(f"Backup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Directories backed up: {len(manifest['directories_backed_up'])}\n")
        f.write(f"Total files: {sum(manifest['files_count'].values())}\n")
        f.write(f"Total size: {manifest['backup_size'] / (1024 * 1024):.2f} MB\n\n")

        f.write("Directory details:\n")
        for dir_name, count in manifest["files_count"].items():
            f.write(f"  {dir_name}: {count} files\n")

    print(f"Backup summary saved: {summary_path}")

    # Create a compressed archive as well
    archive_path = backup_dir.parent / f"NOCTURNEMELODIES_ORGANIZATION_ARCHIVE_{timestamp}.zip"
    print(f"Creating compressed archive: {archive_path}")

    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(backup_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(backup_dir.parent.parent)
                zipf.write(file_path, arc_path)

    print(f"Compressed archive created: {archive_path}")

    print("\nBackup completed successfully!")
    print(f"Backup location: {backup_dir}")
    print(f"Archive location: {archive_path}")
    print(f"Directories backed up: {len(manifest['directories_backed_up'])}")
    print(f"Total files: {sum(manifest['files_count'].values())}")
    print(f"Total size: {manifest['backup_size'] / (1024 * 1024):.2f} MB")


if __name__ == "__main__":
    create_backup()
