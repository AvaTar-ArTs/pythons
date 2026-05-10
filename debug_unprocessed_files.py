"""
Summary of debug_unprocessed_files.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""


import sys
import os
import csv
import io
from pathlib import Path

# Get all Python files
all_files_list = [str(f) for f in Path('/Users/steven/pythons/').rglob('*.py')]
all_files = set(all_files_list)

# Read processed files from stdin (comprehensive_meta.csv)
processed_files_raw = sys.stdin.read()
processed_files = set()

# Process CSV data
csv_file_like = io.StringIO(processed_files_raw)
reader = csv.reader(csv_file_like)

# Attempt to skip header, handle empty file gracefully
try:
    next(reader) # Skip header
except StopIteration:
    pass

for row in reader:
    if row and len(row) > 0:
        path_from_csv = row[0].strip()
        if path_from_csv:
            processed_files.add(path_from_csv)

# Output all_files to one file
with open('/Users/steven/pythons/all_python_files_from_rglob.txt', 'w') as f:
    for f_path in sorted(list(all_files)):
        f.write(f_path + '\n')

# Output processed_files to another file
with open('/Users/steven/pythons/processed_files_from_csv.txt', 'w') as f:
    for p_path in sorted(list(processed_files)):
        f.write(p_path + '\n')

sys.stderr.write("--- DEBUG INFO ---\n")
sys.stderr.write(f"Total Python files found by rglob: {len(all_files)}\n")
sys.stderr.write(f"Number of files in processed_files set: {len(processed_files)}\n")
sys.stderr.write("all_python_files_from_rglob.txt and processed_files_from_csv.txt generated for comparison.\n")
sys.stderr.write("--- END DEBUG INFO ---\n")

# This script will not print unprocessed_files to stdout anymore, as we are generating full lists.
# The next step will be to compare these generated files.
