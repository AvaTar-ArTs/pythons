"""
Dallecsv

This module provides functionality for dallecsv.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import csv

import logging

logger = logging.getLogger(__name__)


# Path to the input text file
input_file_path = Path("/Users/steven/Pictures/DaLL-E/dalle/dalle.txt")

# Path to the output CSV file
output_csv_path = Path("/Users/steven/Pictures/DaLL-E/dalle/dalle_output.csv")

# Read the content of the input file
with open(input_file_path, "r") as file:
    lines = file.readlines()

# Prepare the data for CSV
data = []
url = None
info = None

for line in lines:
    line = line.strip()
    if line.startswith("https://"):
        if url and info:
            data.append([url, info])
        url = line
        info = None
    else:
        if info:
            info += " " + line
        else:
            info = line

# Don't forget to add the last url-info pair
if url and info:
    data.append([url, info])

# Write the data to the CSV file
with open(output_csv_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["URL", "Info"])
    writer.writerows(data)

logger.info(f"CSV file has been generated: {output_csv_path}")
