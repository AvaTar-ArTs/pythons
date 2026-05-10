"""
Summary of create_test_bed.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import os
import csv
import shutil
from pathlib import Path

csv_path = os.path.expanduser("~/reorganization_preview_2026_MASTER_V3.csv")
test_bed_root = os.path.expanduser("~/REORGANIZATION_TEST_BED")

if os.path.exists(test_bed_root):
    shutil.rmtree(test_bed_root)
os.makedirs(test_bed_root)

with open(csv_path, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        item_name = row['Item_Name']
        current_folder = os.path.expanduser(row['Current_Folder'])
        # Proposed folder is relative to home in the CSV (e.g., ~/automation/logs)
        # We want to mirror that inside the test_bed_root
        proposed_folder_rel = row['Proposed_Folder'].replace("~/", "")
        target_dir = os.path.join(test_bed_root, proposed_folder_rel)
        
        source_path = os.path.join(current_folder, item_name)
        target_path = os.path.join(target_dir, item_name)
        
        if not os.path.exists(source_path):
            continue
            
        os.makedirs(target_dir, exist_ok=True)
        
        try:
            if os.path.isdir(source_path):
                # Copying directory structure (shallow copy to avoid 850k file explosion)
                # We'll just create the folder in the test bed to show where it goes
                os.makedirs(target_path, exist_ok=True)
            else:
                shutil.copy2(source_path, target_path)
        except Exception as e:
            print(f"Error copying {item_name}: {e}")

print(f"✅ Test Bed created at: {test_bed_root}")
