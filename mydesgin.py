"""
Csv Mydesgin 1

This module provides functionality for csv mydesgin 1.

Author: Auto-generated
Date: 2025-11-01
"""

import csv
import os

import logging

logger = logging.getLogger(__name__)


# Parent directory containing all the subdirectories
parent_directory = str(Path.home()) + "/Pictures/V-Day CFab/tumnMuG/"

# The CSV file you want to create
csv_file = "print_on_demand_data.csv"

# Define the fields for the CSV
fields = ["File Path"]

# List to store file details
file_details = []

# Traverse through the parent directory and all its subdirectories
for subdir, dirs, files in os.walk(parent_directory):
    for file in files:
        if file.endswith(("png", "svg", "dxf", "eps")):
            file_path = os.path.join(subdir, file)
            file_name, file_extension = os.path.splitext(file)
            file_details.append([file_name, file_extension.strip("."), file_path])

# Write to CSV
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(fields)
    writer.writerows(file_details)

logger.info(f"CSV file '{csv_file}' has been created with image file details.")
