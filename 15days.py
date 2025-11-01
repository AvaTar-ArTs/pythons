"""
15Days

This module provides functionality for 15days.

Author: Auto-generated
Date: 2025-11-01
"""

import os
import shutil
import csv
import json

import logging

logger = logging.getLogger(__name__)


# Paths configuration
csv_file_path = str(Path.home()) + "/15days.csv"
destination_root = "/Users/steven"
backup_file_path = os.path.join(destination_root, "file_order_backup.json")


def ensure_dir(directory):
    """Ensure the directory exists. If not, create it."""
    if not os.path.exists(directory):
        os.makedirs(directory)


# Prepare a list to hold file metadata for backup
files_metadata = []

with open(csv_file_path, newline="") as csvfile:
    filereader = csv.reader(csvfile)
    for row in filereader:
        # Assuming each row has one column with the file path
        file_path = row[0].strip()  # Remove any leading/trailing whitespaces
        if file_path.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
            # Construct the destination path
            destination_path = os.path.join(
                destination_root, os.path.basename(file_path)
            )

            # Record file metadata
            files_metadata.append(
                {
                    "original_path": file_path,
                    "name": os.path.basename(file_path),
                    "destination_path": destination_path,
                }
            )

            # Ensure the destination directory exists
            ensure_dir(os.path.dirname(destination_path))

            # Move the file to the destination
            shutil.move(file_path, destination_path)
            logger.info(f"Moved file: {file_path} to {destination_path}")

# Backup the file metadata
with open(backup_file_path, "w") as backup_file:
    json.dump(files_metadata, backup_file, indent=4)

logger.info(f"Backup of file metadata created at {backup_file_path}")
