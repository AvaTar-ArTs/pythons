"""
Scancsv

This module provides functionality for scancsv.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import csv
import os

import logging

logger = logging.getLogger(__name__)


# List of drives to scan
drives = [
    Path("/Users/steven/Documents"),
    Path("/Users/steven/Music"),
    Path("/Users/steven/Movies/mine"),
    Path("/Users/steven/Pictures"),
]

# File types to look for
file_types = (".jpg", ".jpeg", ".png", ".gif", "webp")


# Function to scan a directory for image files
def scan_directory(directory):
    """scan_directory function."""

    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(file_types):
                yield os.path.join(root, file)


# Output CSV file path
output_csv = "image_paths.csv"

# Open a file to write the paths
with open(output_csv, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["image_path"])  # Write the header
    for drive in drives:
        for image_path in scan_directory(drive):
            csv_writer.writerow([image_path])

logger.info(f"Scan complete. Image paths saved to {output_csv}")
