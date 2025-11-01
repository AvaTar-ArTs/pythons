"""
Data Processing Csv Fdupes 1

This module provides functionality for data processing csv fdupes 1.

Author: Auto-generated
Date: 2025-11-01
"""

import csv

# Read the output from the fdupes results
with open("duplicates.txt", "r") as infile, open(
    "duplicates.csv", "w", newline=""
) as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["File1", "File2"])  # Write the CSV header

    files = []
    for line in infile:
        line = line.strip()
        if line:
            files.append(line)
        else:
            # Write pairs of duplicate files
            for i in range(1, len(files)):
                writer.writerow([files[0], files[i]])
            files = []
