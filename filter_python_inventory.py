"""
Summary of filter_python_inventory.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import re
import csv
import os

# Import patterns from the config file
# Since we are in the home dir, and config is in clean/config.py
import sys
sys.path.append(os.path.join(os.getcwd(), 'clean'))
try:
    from config import EXCLUDED_PATTERNS
except ImportError:
    print("Could not import EXCLUDED_PATTERNS from clean/config.py")
    EXCLUDED_PATTERNS = []

inventory_file = 'all_python_scripts_inventory.txt'
output_file = 'cleaned_python_inventory.csv'

compiled_patterns = [re.compile(p) for p in EXCLUDED_PATTERNS]

cleaned_data = []

if not os.path.exists(inventory_file):
    print(f"Error: {inventory_file} not found.")
    exit(1)

with open(inventory_file, 'r') as f:
    for line in f:
        parts = line.strip().split('  ', 1)
        if len(parts) < 2:
            continue
        
        sha_hash = parts[0]
        full_path = parts[1]
        
        # Check against exclusions
        is_excluded = False
        for pattern in compiled_patterns:
            if pattern.match(full_path):
                is_excluded = True
                break
        
        if not is_excluded:
            filename = os.path.basename(full_path)
            cleaned_data.append({
                'Filename': filename,
                'Hash': sha_hash,
                'Path': full_path
            })

with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['Filename', 'Hash', 'Path']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in cleaned_data:
        writer.writerow(row)

print(f"Filtered {len(cleaned_data)} scripts into {output_file}")
