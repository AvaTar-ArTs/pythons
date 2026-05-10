from pathlib import Path
import json
import os
import shutil

import logging

logger = logging.getLogger(__name__)


# Paths configuration
backup_file_path = Path("/Volumes/iMac/15days/file_order_backup.json")


def move_files_back(backup_path):
    """Move files back to their original locations."""
    # Load the backup file to get the file metadata
    with open(backup_path, "r") as backup_file:
        files_metadata = json.load(backup_file)

    for file in files_metadata:
        original_path = file["original_path"]
        destination_path = file["destination_path"]

        # Ensure the original directory exists
        if not os.path.exists(os.path.dirname(original_path)):
            os.makedirs(os.path.dirname(original_path))

        # Move the file back to its original location
        shutil.move(destination_path, original_path)
        logger.info(f"Moved file: {destination_path} to {original_path}")


# Execute the function to move files back
move_files_back(backup_file_path)

logger.info("All files have been moved back to their original locations.")
