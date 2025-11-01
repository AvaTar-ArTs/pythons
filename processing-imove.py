"""
Data Processing Csv Imove 3

This module provides functionality for data processing csv imove 3.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import csv
import os
import shutil

import logging

logger = logging.getLogger(__name__)


# Define the path to the CSV file
csv_file_path = str(Path.home()) + "/Downloads/ogPic6-21 - image_paths2.csv"
# Define the destination directory based on your specification
destination_dir = Path("/Volumes/iMac/4-4-2024")

# Ensure the destination directory exists
os.makedirs(destination_dir, exist_ok=True)

# Open the CSV file and read its contents
with open(csv_file_path, newline="") as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)  # Skip the header row if your CSV has one
    for row in reader:
        # Assuming the file paths are in the first column
        # Strip to remove any leading/trailing whitespace
        file_path = row[0].strip()
        # Define the destination path for the file
        dest_path = os.path.join(destination_dir, os.path.basename(file_path))
        # Check if the source file exists before attempting to copy
        if os.path.exists(file_path):
            # Copy the file to the destination directory
            shutil.copy(file_path, dest_path)
        else:
            logger.info(f"File does not exist: {file_path}")
