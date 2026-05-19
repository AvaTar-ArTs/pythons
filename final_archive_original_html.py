#!/usr/bin/env python3
"""
Final archival script for original HTML files to external drive
This script moves the original HTML files to the external drive while preserving
the mobile-optimized and consolidated versions in the main directory.
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path


def create_final_archive():
    """Create a final archive of original HTML files to external drive"""

    # Define source and destination
    source_dir = Path("/Users/steven/Music/nocTurneMeLoDieS")
    dest_dir = Path("/Volumes/2T-Xx/nocTurneMeLoDieS_ORIGINAL_HTML_ARCHIVE_20260129_142113")

    # Create archive directory with timestamp
    dest_dir.mkdir(parents=True, exist_ok=True)

    print(f"Starting archival of original HTML files to: {dest_dir}")

    # Find all original HTML files (excluding the consolidated and mobile versions)
    original_html_files = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".html") and not any(
                exclude in root
                for exclude in [
                    "CONSOLIDATED_HTML",
                    "NOCTURNEMELODIES_WEB_STRUCTURE_V2",
                    "NOCTURNEMELODIES_WEB_STRUCTURE_V3",
                    "NOCTURNEMELODIES_FINAL_ORGANIZATION",
                ]
            ):
                if not file.endswith("_mobile.html"):
                    original_html_files.append(Path(root) / file)

    print(f"Found {len(original_html_files)} original HTML files to archive")

    # Track archived files
    archive_mapping = {}

    # Move files to external drive
    for i, file_path in enumerate(original_html_files):
        try:
            # Create relative path to preserve directory structure
            rel_path = file_path.relative_to(source_dir)
            dest_file_path = dest_dir / rel_path

            # Create destination directory if it doesn't exist
            dest_file_path.parent.mkdir(parents=True, exist_ok=True)

            # Move the file
            shutil.move(str(file_path), str(dest_file_path))

            # Record in mapping
            archive_mapping[str(rel_path)] = {
                "original_location": str(file_path),
                "archived_location": str(dest_file_path),
                "timestamp": datetime.now().isoformat(),
            }

            print(f"Archived ({i + 1}/{len(original_html_files)}): {rel_path}")

        except Exception as e:
            print(f"Error archiving {file_path}: {str(e)}")
            continue

    # Save mapping file
    mapping_file = dest_dir / "archive_mapping.json"
    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump(archive_mapping, f, indent=2)

    # Create summary file
    summary_file = dest_dir / "archive_summary.txt"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("Original HTML Files Archive Summary\n")
        f.write("=" * 40 + "\n")
        f.write(f"Total files archived: {len(archive_mapping)}\n")
        f.write(f"Archive date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Archive location: {dest_dir}\n\n")
        f.write("Original files have been moved to the external drive.\n")
        f.write("Mobile-optimized and consolidated versions remain in the main directory.\n")

    print("\nArchival completed successfully!")
    print(f"Total files archived: {len(archive_mapping)}")
    print(f"Archive location: {dest_dir}")
    print(f"Mapping file saved: {mapping_file}")
    print(f"Summary file saved: {summary_file}")

    return archive_mapping


def main():
    print("Starting final archival of original HTML files to external drive...")
    print("This will move original HTML files to /Volumes/2T-Xx while preserving")
    print("mobile-optimized and consolidated versions in the main directory.\n")

    # Create the final archive
    create_final_archive()

    print("\nFinal archival completed!")
    print("All original HTML files have been moved to your external drive")
    print("Mobile-optimized and consolidated versions remain accessible in the main directory")
    print("Archive mapping preserved for reference purposes")


if __name__ == "__main__":
    main()
