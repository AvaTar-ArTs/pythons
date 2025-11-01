"""
Youtube Find Out Of Place Files

This module provides functionality for youtube find out of place files.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Out of Place Files Analysis
==========================
Scans Documents directory for files that are in the wrong locations
based on their file extensions and creates a comprehensive CSV report.
"""

import os
import csv
from pathlib import Path
from datetime import datetime


def find_out_of_place_files():
    """Find all files that are in the wrong directories based on their extensions"""

    # Define the correct directories for each file type
    correct_dirs = {
        ".py": "python",
        ".md": "markD",
        ".csv": "CsV",
        ".html": "HTML",
        ".json": "json",
        ".txt": "txt",
        ".zip": "Archives",
    }

    # Define file extensions to check
    extensions = [".py", ".md", ".csv", ".html", ".json", ".txt", ".zip"]

    out_of_place_files = []
    documents_path = Path("/Users/steven/Documents")

    logger.info("🔍 Scanning Documents directory for out-of-place files...")

    for ext in extensions:
        correct_dir = correct_dirs[ext]
        logger.info(f"  Checking {ext} files (should be in {correct_dir}/)...")

        # Find all files with this extension
        for file_path in documents_path.rglob(f"*{ext}"):
            # Skip if it's already in the correct directory
            if f"/{correct_dir}/" in str(file_path):
                continue

            # Skip if it's in a subdirectory of the correct directory
            if f"/{correct_dir}/" in str(file_path.parent):
                continue

            # Get file info
            try:
                stat = file_path.stat()
                file_size = stat.st_size
                modified_time = datetime.fromtimestamp(stat.st_mtime)

                # Determine current location category
                current_location = "Root Documents"
                if "As-a-man-thinketh" in str(file_path):
                    current_location = "As-a-man-thinketh Project"
                elif "Obsidian Vault" in str(file_path):
                    current_location = "Obsidian Vault"
                elif "python" in str(file_path) and ext != ".py":
                    current_location = "Python Directory (Wrong Type)"
                elif "script" in str(file_path):
                    current_location = "Script Directory"
                elif "claude" in str(file_path):
                    current_location = "Claude Projects"
                elif "creative-asset-orchestrator" in str(file_path):
                    current_location = "Creative Asset Project"
                else:
                    # Check parent directory
                    parent_name = file_path.parent.name
                    if parent_name != "Documents":
                        current_location = f"Other: {parent_name}"

                out_of_place_files.append(
                    {
                        "file_path": str(file_path),
                        "file_name": file_path.name,
                        "file_extension": ext,
                        "correct_directory": correct_dir,
                        "current_location": current_location,
                        "file_size_bytes": file_size,
                        "file_size_mb": round(
                            file_size / (CONSTANT_1024 * CONSTANT_1024), 2
                        ),
                        "modified_date": modified_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "relative_path": str(file_path.relative_to(documents_path)),
                    }
                )

            except (OSError, PermissionError) as e:
                logger.info(f"    ⚠️  Could not access {file_path}: {e}")
                continue

    return out_of_place_files


def create_csv_report(out_of_place_files):
    """Create a CSV report of out-of-place files"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = (
        f"/Users/steven/Documents/python/out_of_place_files_report_{timestamp}.csv"
    )

    logger.info(f"\n📊 Creating CSV report: {csv_filename}")

    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "file_name",
            "file_extension",
            "correct_directory",
            "current_location",
            "file_size_mb",
            "modified_date",
            "relative_path",
            "full_path",
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Sort by file extension, then by current location
        sorted_files = sorted(
            out_of_place_files,
            key=lambda x: (x["file_extension"], x["current_location"]),
        )

        for file_info in sorted_files:
            writer.writerow(
                {
                    "file_name": file_info["file_name"],
                    "file_extension": file_info["file_extension"],
                    "correct_directory": file_info["correct_directory"],
                    "current_location": file_info["current_location"],
                    "file_size_mb": file_info["file_size_mb"],
                    "modified_date": file_info["modified_date"],
                    "relative_path": file_info["relative_path"],
                    "full_path": file_info["file_path"],
                }
            )

    return csv_filename


def print_summary(out_of_place_files):
    """Print a summary of the analysis"""

    logger.info(f"\n📈 SUMMARY")
    logger.info("=" * 50)
    logger.info(f"Total out-of-place files found: {len(out_of_place_files)}")

    # Count by file type
    by_extension = {}
    by_location = {}
    total_size = 0

    for file_info in out_of_place_files:
        ext = file_info["file_extension"]
        loc = file_info["current_location"]
        size = file_info["file_size_bytes"]

        by_extension[ext] = by_extension.get(ext, 0) + 1
        by_location[loc] = by_location.get(loc, 0) + 1
        total_size += size

    logger.info(f"\n📁 By File Type:")
    for ext, count in sorted(by_extension.items()):
        logger.info(f"  {ext}: {count} files")

    logger.info(f"\n📍 By Current Location:")
    for loc, count in sorted(by_location.items()):
        logger.info(f"  {loc}: {count} files")

    logger.info(
        f"\n💾 Total Size: {total_size / (CONSTANT_1024 * CONSTANT_1024):.2f} MB"
    )

    # Show top 10 largest files
    logger.info(f"\n🔝 Top 10 Largest Files:")
    largest_files = sorted(
        out_of_place_files, key=lambda x: x["file_size_bytes"], reverse=True
    )[:10]
    for i, file_info in enumerate(largest_files, 1):
        logger.info(
            f"  {i:2d}. {file_info['file_name']} ({file_info['file_size_mb']} MB) - {file_info['current_location']}"
        )


def main():
    """Main function"""
    logger.info("🚀 Out of Place Files Analysis")
    logger.info("=" * 50)

    # Find out-of-place files
    out_of_place_files = find_out_of_place_files()

    if not out_of_place_files:
        logger.info(
            "✅ No out-of-place files found! Your Documents directory is well organized."
        )
        return

    # Create CSV report
    csv_filename = create_csv_report(out_of_place_files)

    # Print summary
    print_summary(out_of_place_files)

    logger.info(f"\n✅ Analysis complete! CSV report saved to: {csv_filename}")
    logger.info("\n💡 Next steps:")
    logger.info("  1. Review the CSV report")
    logger.info("  2. Decide which files to move")
    logger.info("  3. Use the file paths to organize files properly")


if __name__ == "__main__":
    main()
