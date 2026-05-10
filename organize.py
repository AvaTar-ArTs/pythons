import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
Summary of organize.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import csv
import os
import shutil


def copy_files_with_structure(csv_file_path, destination_base_path):
    with open(csv_file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            original_path = row["Original Path"]
            destination_path = os.path.join(
                destination_base_path, original_path.lstrip(os.sep)
            )

            # Create the destination directory if it doesn't exist
            destination_dir = os.path.dirname(destination_path)
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)

            # Copy the file to the destination
            shutil.copy2(original_path, destination_path)
            print(f"Copied {original_path} to {destination_path}")


try:
        csv_file_path = "/Users/steven/Documents/Python/Sort/tagg/audio-07-11-14:39.csv"
        destination_base_path = "/Volumes/oG-bAk/organized"
        copy_files_with_structure(csv_file_path, destination_base_path)
        print("All files have been copied successfully.")
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)