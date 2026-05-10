#!/usr/bin/env python3
"""
Backup and Archival Script for NocturneMelodies Content Organization Project

This script creates a comprehensive backup of all the work done on the NocturneMelodies
content organization project, including all versions and documentation.
"""

import json
import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path


def create_comprehensive_backup():
    """Create a comprehensive backup of the entire NocturneMelodies organization project"""

    # Define source directories to backup
    source_dirs = [
        "/Users/steven/Music/nocTurneMeLoDieS/CONSOLIDATED_HTML",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_WEB_STRUCTURE_V2",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_WEB_STRUCTURE_V3",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_FINAL_ORGANIZATION",
        "/Users/steven/Music/nocTurneMeLoDieS/AVATARARTS_CONSOLIDATION_PROJECT",
        "/Users/steven/Music/nocTurneMeLoDieS/MOBILE_TEMPLATES",
        "/Users/steven/Music/nocTurneMeLoDieS/CONSOLIDATED_CONTENT_STEVEN",
    ]

    # Create backup directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"/Users/steven/Music/nocTurneMeLoDieS/BACKUPS/NOCTURNEMELODIES_ORGANIZATION_BACKUP_{timestamp}")
    backup_dir.mkdir(parents=True, exist_ok=True)

    print(f"Creating comprehensive backup at: {backup_dir}")

    # Create backup of each directory
    backup_info = {}
    for source_dir in source_dirs:
        source_path = Path(source_dir)
        if source_path.exists():
            dest_path = backup_dir / source_path.name
            print(f"Backing up: {source_dir}")

            # Use shutil.copytree for directories
            if source_path.is_dir():
                shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
                file_count = sum([len(files) for _, _, files in os.walk(dest_path)])
                backup_info[source_path.name] = {
                    "source": str(source_path),
                    "destination": str(dest_path),
                    "file_count": file_count,
                    "size": get_directory_size(dest_path),
                }
            else:
                # For files, just copy
                shutil.copy2(source_path, dest_path)
                backup_info[source_path.name] = {
                    "source": str(source_path),
                    "destination": str(dest_path),
                    "file_count": 1,
                    "size": source_path.stat().st_size,
                }

    # Create backup of all related scripts and documentation
    scripts_and_docs = [
        "/Users/steven/Music/nocTurneMeLoDieS/consolidate_make_mobile.py",
        "/Users/steven/Music/nocTurneMeLoDieS/consolidate_all_steven_content.py",
        "/Users/steven/Music/nocTurneMeLoDieS/create_avatararts_website.py",
        "/Users/steven/Music/nocTurneMeLoDieS/create_nocturnemelodies_v2.py",
        "/Users/steven/Music/nocTurneMeLoDieS/create_nocturnemelodies_v3.py",
        "/Users/steven/Music/nocTurneMeLoDieS/create_final_nocturnemelodies_organization.py",
        "/Users/steven/Music/nocTurneMeLoDieS/CONTENT_REVIEW_SUMMARY.md",
        "/Users/steven/Music/nocTurneMeLoDieS/COMPREHENSIVE_CONTENT_CONSOLIDATION_ALL_VERSIONS.md",
        "/Users/steven/Music/nocTurneMeLoDieS/AVATARARTS_CONTENT_REVIEW.md",
        "/Users/steven/Music/nocTurneMeLoDieS/FINAL_PROJECT_REVIEW_AND_SUMMARY.md",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_CONTENT_ORGANIZATION_COMPLETE.md",
        "/Users/steven/Music/nocTurneMeLoDieS/COMPREHENSIVE_PROJECT_SUMMARY_WITH_COMPARISON.md",
        "/Users/steven/Music/nocTurneMeLoDieS/DIRECTORY_COMPARISON_REPORT.md",
        "/Users/steven/Music/nocTurneMeLoDieS/HTML_CONSOLIDATION_MOBILE_OPTIMIZATION_COMPLETED.md",
        "/Users/steven/Music/nocTurneMeLoDieS/CONTENT_ORGANIZATION_SUGGESTIONS.html",
        "/Users/steven/Music/nocTurneMeLoDieS/CONTENT_ORGANIZATION_SUGGESTIONS.csv",
    ]

    scripts_backup_dir = backup_dir / "scripts_and_documentation"
    scripts_backup_dir.mkdir(exist_ok=True)

    for script_path in scripts_and_docs:
        script_file = Path(script_path)
        if script_file.exists():
            dest_file = scripts_backup_dir / script_file.name
            shutil.copy2(script_file, dest_file)
            backup_info[f"script_{script_file.name}"] = {
                "source": str(script_file),
                "destination": str(dest_file),
                "file_count": 1,
                "size": script_file.stat().st_size,
            }

    # Create a backup manifest
    manifest_path = backup_dir / "backup_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(backup_info, f, indent=2)

    # Create a summary file
    summary_path = backup_dir / "backup_summary.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("NocturneMelodies Content Organization Project - Backup Summary\n")
        f.write("=" * 60 + "\n")
        f.write(f"Backup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Backup Location: {backup_dir}\n\n")
        f.write("Directories Backed Up:\n")
        for name, info in backup_info.items():
            if "size" in info:
                size_mb = info["size"] / (1024 * 1024)
                f.write(f"  {name}: {info['file_count']} files ({size_mb:.2f} MB)\n")

    # Create a ZIP archive for portability
    zip_path = Path(
        f"/Users/steven/Music/nocTurneMeLoDieS/BACKUPS/NOCTURNEMELODIES_ORGANIZATION_BACKUP_{timestamp}.zip"
    )
    print(f"Creating ZIP archive: {zip_path}")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(backup_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(backup_dir.parent)
                zipf.write(file_path, arc_path)

    print("\nComprehensive backup completed successfully!")
    print(f"Backup location: {backup_dir}")
    print(f"ZIP archive: {zip_path}")
    print(f"Manifest file: {manifest_path}")
    print(f"Summary file: {summary_path}")

    return backup_dir, zip_path


def get_directory_size(path):
    """Get the total size of a directory in bytes"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(file_path)
            except OSError:
                continue  # Skip if file is inaccessible
    return total_size


def main():
    print("Starting comprehensive backup of NocturneMelodies content organization project...")

    backup_dir, zip_path = create_comprehensive_backup()

    print("\nBackup completed successfully!")
    print(f"Directory backup: {backup_dir}")
    print(f"ZIP archive: {zip_path}")
    print("Backup includes all versions (V1, V2, V3, Final) of the HTML organization system")
    print("Backup includes all scripts, documentation, and mobile optimization templates")


if __name__ == "__main__":
    main()
