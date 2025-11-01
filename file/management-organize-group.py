"""
File Management Organize Group 1

This module provides functionality for file management organize group 1.

Author: Auto-generated
Date: 2025-11-01
"""

import csv
import os
from collections import defaultdict
from datetime import datetime

import logging

logger = logging.getLogger(__name__)


# Prompt the user for the directory
directory = input("Enter the directory containing the files: ").strip()

# Get the root folder name
root_folder = os.path.basename(os.path.normpath(directory))
current_date = datetime.now().strftime("%m%d%y")
output_csv = os.path.join(directory, f"{root_folder}-{current_date}.csv")

# Step 1: Group files by song title (ignoring version indicators)
file_groups = defaultdict(list)

try:
    # Check if the directory exists
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")

    for subdir, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".txt"):
                # Group by the base title, ignoring version-specific suffixes
                base_title = filename.split("_analysis")[0].split("-analysis")[0].split("(")[0].strip()
                file_groups[base_title].append(os.path.join(subdir, filename))

    # Step 2: Write grouped files to CSV
    with open(output_csv, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Song Title", "File Paths"])

        for title, files in file_groups.items():
            # Write each group to the CSV with title and all associated file paths
            writer.writerow([title, ", ".join(files)])

    logger.info(f"Organized file list has been written to {output_csv}")
except Exception as e:
    logger.info(f"An error occurred: {e}")
