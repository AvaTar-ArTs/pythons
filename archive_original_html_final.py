#!/usr/bin/env python3
"""
Final archival script for NocturneMelodies HTML files to external drive
This script archives the original HTML files to /Volumes/2T-Xx as requested
"""

import shutil
from datetime import datetime
from pathlib import Path


def archive_original_html_files():
    """Archive original HTML files to external drive"""

    # Define source and destination
    source_dir = Path("/Users/steven/Music/nocTurneMeLoDieS")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_dir = Path(f"/Volumes/2T-Xx/nocTurneMeLoDieS_HTML_Archive_{timestamp}")

    # Create archive directory
    archive_dir.mkdir(parents=True, exist_ok=True)

    print("Starting archival of original HTML files...")
    print(f"Source: {source_dir}")
    print(f"Destination: {archive_dir}")

    # Find all original HTML files (excluding the newly created mobile versions and consolidated versions)
    html_files = list(source_dir.rglob("*.html"))
    original_html_files = []

    for file_path in html_files:
        # Skip files that are already in consolidated or mobile-optimized directories
        if (
            "CONSOLIDATED_CONTENT" not in str(file_path)
            and "NOCTURNEMELODIES_WEB_STRUCTURE" not in str(file_path)
            and "FINAL_ORGANIZATION" not in str(file_path)
            and "_mobile.html" not in str(file_path)
        ):
            original_html_files.append(file_path)

    print(f"Found {len(original_html_files)} original HTML files to archive")

    # Copy files to archive
    for i, file_path in enumerate(original_html_files, 1):
        try:
            # Create relative path to preserve directory structure
            rel_path = file_path.relative_to(source_dir)
            archive_path = archive_dir / rel_path

            # Create parent directories if they don't exist
            archive_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy the file
            shutil.copy2(file_path, archive_path)

            if i % 50 == 0:
                print(f"Archived {i}/{len(original_html_files)} files...")

        except Exception as e:
            print(f"Error archiving {file_path}: {str(e)}")
            continue

    print("\nArchival completed!")
    print(f"Total files archived: {len(original_html_files)}")
    print(f"Archive location: {archive_dir}")

    # Create a summary file
    summary_path = archive_dir / "ARCHIVE_SUMMARY.txt"
    with open(summary_path, "w") as f:
        f.write("NocturneMelodies HTML Archive Summary\n")
        f.write(f"Archive Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Files Archived: {len(original_html_files)}\n\n")
        f.write("Archived Files:\n")
        for file_path in original_html_files:
            rel_path = file_path.relative_to(source_dir)
            f.write(f"- {rel_path}\n")

    print(f"Archive summary created: {summary_path}")


if __name__ == "__main__":
    archive_original_html_files()
