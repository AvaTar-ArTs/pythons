#!/usr/bin/env python3
"""
Rename Suno UUID zip files to their actual song titles using CSV data.
"""

import os
import csv
import re
from pathlib import Path

def load_suno_mappings(csv_path):
    """Load UUID to title mappings from Suno CSV."""
    mappings = {}
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                uuid = row.get('id', '').strip()
                title = row.get('title', '').strip()
                if uuid and title:
                    # Clean up the title (remove markdown formatting)
                    title = re.sub(r'[##*`"]', '', title).strip()
                    # Replace special characters with safe filename chars
                    title = re.sub(r'[<>:"/\\|?*]', '_', title)
                    mappings[uuid] = title
    except Exception as e:
        print(f"Error reading {csv_path}: {e}")
    return mappings

def rename_uuid_files(source_dir, mappings, dry_run=True):
    """Rename UUID files to song titles."""
    renamed = 0
    not_found = 0

    for filename in os.listdir(source_dir):
        if not filename.endswith('.zip'):
            continue

        # Extract UUID from filename (remove .zip extension)
        uuid = filename[:-4]  # Remove .zip

        if uuid in mappings:
            new_name = f"{mappings[uuid]}.zip"
            old_path = os.path.join(source_dir, filename)
            new_path = os.path.join(source_dir, new_name)

            if dry_run:
                print(f"WOULD RENAME: {filename} → {new_name}")
            else:
                try:
                    os.rename(old_path, new_path)
                    print(f"RENAMED: {filename} → {new_name}")
                    renamed += 1
                except Exception as e:
                    print(f"ERROR renaming {filename}: {e}")
        else:
            print(f"UUID not found in CSV: {filename}")
            not_found += 1

    if dry_run:
        print(f"\nDRY RUN COMPLETE: Would rename {len([f for f in os.listdir(source_dir) if f.endswith('.zip') and f[:-4] in mappings])} files")
    else:
        print(f"\nRENAMED: {renamed} files")

    if not_found > 0:
        print(f"NOT FOUND in CSV: {not_found} files")

def main():
    # Paths
    csv_path = "/Users/steven/Music/nocTurneMeLoDieS/AI_ENHANCED_ORGANIZATION/DATA/suno-export-2026-01-25T19-07-34.csv"
    uuid_dir = "/Volumes/2T-Xx/zip/non_etsy"

    print("Loading Suno mappings from CSV...")
    mappings = load_suno_mappings(csv_path)
    print(f"Loaded {len(mappings)} UUID → title mappings")

    print(f"\nChecking UUID files in {uuid_dir}...")
    uuid_files = [f for f in os.listdir(uuid_dir) if f.endswith('.zip') and re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\.zip$', f)]
    print(f"Found {len(uuid_files)} UUID zip files")

    print("\n=== DRY RUN (showing what would be renamed) ===")
    rename_uuid_files(uuid_dir, mappings, dry_run=True)

    print("\n=== READY TO RENAME ===")
    print("Run with dry_run=False to actually rename files")
    print("Command: python3 rename_suno_uuids.py  # then edit dry_run=False")

if __name__ == "__main__":
    main()