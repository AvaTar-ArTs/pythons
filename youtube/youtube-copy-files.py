"""
Youtube Copy Files

This module provides functionality for youtube copy files.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import csv
import os
import shutil

import logging

logger = logging.getLogger(__name__)



# Function to copy files while preserving folder structure and logging each copied file
def copy_files_with_logging(csv_file, destination_root):
    """copy_files_with_logging function."""

    log_file = "copy_log.txt"
    with open(csv_file, newline="") as csvfile, open(
        log_file, "a"
    ) as log:  # Use 'a' to append to the log file
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Ensuring the row is not empty
                src_file_path = row[0]
                try:
                    # Check if the source file exists
                    if not os.path.exists(src_file_path):
                        error_message = f"Source file does not exist: {src_file_path}"
                        log.write(error_message + Path("\n"))
                        logger.info(error_message)
                        continue

                    relative_path = os.path.relpath(
                        src_file_path, Path("/Users/steven/Documents/Python/Sort/tagg")
                    )
                    dest_file_path = os.path.join(destination_root, relative_path)

                    # Create directories if they do not exist
                    os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)

                    # Copy the file
                    shutil.copy2(src_file_path, dest_file_path)
                    log.write(f"Copied {src_file_path} to {dest_file_path}\n")
                    logger.info(f"Copied {src_file_path} to {dest_file_path}")
                except PermissionError as e:
                    error_message = f"Permission denied: {e}"
                    log.write(error_message + Path("\n"))
                    logger.info(error_message)
                except Exception as e:
                    error_message = (
                        f"Error copying {src_file_path} to {dest_file_path}: {e}"
                    )
                    log.write(error_message + Path("\n"))
                    logger.info(error_message)


if __name__ == "__main__":
    csv_files = ["/Users/steven/Documents/Python/Sort/tagg/vids-07-11-12:31.csv"]
    destination_base_path = Path("/Volumes/oG-bAk/organized")

    # Process each CSV file
    for csv_file in csv_files:
        copy_files_with_logging(csv_file, destination_base_path)
