#!/usr/bin/env python3
import csv
import os
import shutil
from pathlib import Path

def restore_from_mapping(mapping_file):
    """Restore files from mapping CSV"""
    if not os.path.exists(mapping_file):
        print(f"Mapping file not found: {mapping_file}")
        return
    
    restored = 0
    with open(mapping_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            original = row.get('original_location', '')
            consolidated = row.get('consolidated_location', '') or row.get('active_location', '')
            
            if not original or not consolidated:
                continue
            
            # Create directory if needed
            os.makedirs(os.path.dirname(consolidated), exist_ok=True)
            
            # Copy original to consolidated location
            if os.path.exists(original):
                shutil.copy2(original, consolidated)
                print(f"Restored: {consolidated}")
                restored += 1
            else:
                print(f"Warning: Original not found: {original}")
    
    print(f"\nRestored {restored} files from {mapping_file}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        restore_from_mapping(sys.argv[1])
    else:
        print("Usage: python restore_files.py <mapping_file.csv>")
