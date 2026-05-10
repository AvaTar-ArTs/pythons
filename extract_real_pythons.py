"""
Summary of extract_real_pythons.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import csv
import os

# Define the "Safe Zones" where your real work lives
SAFE_ZONES = [
    './pythons',
    './AVATARARTS',
    './GitHub',
    './Documents',
    './scripts',
    './clean'
]

# Define specific noisy subdirectories to ignore even in safe zones (if any)
SPECIFIC_IGNORES = [
    'google-cloud-sdk',
    'pipreqs_env',
    'node_modules',
    '__pycache__',
    'venv',
    '.venv'
]

input_file = 'cleaned_python_inventory.csv'
output_file = 'real_python_scripts.csv'

real_scripts = []

if not os.path.exists(input_file):
    print(f"Error: {input_file} not found.")
    exit(1)

with open(input_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        path = row['Path']
        
        # 1. Check if it starts with a safe zone OR is a loose script in home (./filename.py)
        is_in_safe_zone = any(path.startswith(zone) for zone in SAFE_ZONES)
        is_loose_script = path.count('/') == 1 and path.startswith('./')
        
        if is_in_safe_zone or is_loose_script:
            # 2. Double check it's not in an ignored subdirectory
            if not any(ignore in path for ignore in SPECIFIC_IGNORES):
                # 3. Filter out boilerplate __init__.py if desired (optional, keeping for now as they show structure)
                real_scripts.append(row)

with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['Filename', 'Hash', 'Path']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in real_scripts:
        writer.writerow(row)

print(f"Successfully extracted {len(real_scripts)} 'Real' scripts into {output_file}")
