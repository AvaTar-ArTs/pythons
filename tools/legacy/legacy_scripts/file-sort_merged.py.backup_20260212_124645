#!/usr/bin/env python3
"""
Merged Content Analysis Tool

This file was automatically merged from the following source files:
- /Users/steven/Music/nocTurneMeLoDieS/python/FINAL_ORGANIZED/core_analysis/file-sort.py
- /Users/steven/Music/nocTurneMeLoDieS/python/CLEAN_ORGANIZED/core_analysis/file-sort.py

Combines the best features and functionality from multiple similar files.
"""

# Imports from all source files
import csv
import os
from collections import defaultdict

output_csv = "/Users/steven/Music/NocTurnE-meLoDieS/v4/song-info.csv"

# Step 1: Group files by song title (ignoring version indicators)
file_groups = defaultdict(list)

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        # Group by the base title, ignoring version-specific suffixes
        base_title = filename.split("_analysis")[0].split("-analysis")[0].split("(")[0]
        file_groups[base_title.strip()].append(os.path.join(directory, filename))

# Step 2: Write grouped files to CSV
with open(output_csv, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Song Title", "File Paths"])

    for title, files in file_groups.items():
        # Write each group to the CSV with title and all associated file paths
        writer.writerow([title, ", ".join(files)])

print(f"Organized file list has been written to {output_csv}")
