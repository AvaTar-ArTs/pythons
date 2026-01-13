#!/usr/bin/env python3
"""
Split large INTELLIGENT_HOME_ANALYSIS.json into manageable chunks
"""
import json
import os
from pathlib import Path

SOURCE_FILE = "/Users/steven/INTELLIGENT_HOME_ANALYSIS.json"
OUTPUT_DIR = "/Users/steven/home_analysis_split"

def split_analysis():
    print(f"Loading {SOURCE_FILE}...")
    print("This may take a minute due to file size...")

    with open(SOURCE_FILE, 'r') as f:
        data = json.load(f)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"\nTop-level keys: {list(data.keys())}")

    # Split into separate files by category
    files_created = []

    # 1. Summary statistics (small)
    if 'statistics' in data:
        summary_file = f"{OUTPUT_DIR}/01_statistics.json"
        with open(summary_file, 'w') as f:
            json.dump({
                'analysis_date': data.get('analysis_date'),
                'root_path': data.get('root_path'),
                'statistics': data['statistics']
            }, f, indent=2)
        files_created.append(('Statistics', summary_file, os.path.getsize(summary_file)))

    # 2. Split other top-level keys into separate files
    for key in data.keys():
        if key in ['analysis_date', 'root_path', 'statistics']:
            continue

        output_file = f"{OUTPUT_DIR}/02_{key}.json"
        with open(output_file, 'w') as f:
            json.dump({key: data[key]}, f, indent=2)
        files_created.append((key, output_file, os.path.getsize(output_file)))

    # Create index file
    index_file = f"{OUTPUT_DIR}/00_INDEX.txt"
    with open(index_file, 'w') as f:
        f.write("INTELLIGENT HOME ANALYSIS - SPLIT FILES\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Original file: {SOURCE_FILE}\n")
        f.write(f"Original size: {os.path.getsize(SOURCE_FILE) / (1024**3):.2f} GB\n\n")
        f.write("Split files:\n")
        f.write("-" * 50 + "\n")

        total_size = 0
        for name, path, size in sorted(files_created, key=lambda x: x[2], reverse=True):
            size_mb = size / (1024**2)
            f.write(f"{name:30s} {size_mb:>8.2f} MB  {Path(path).name}\n")
            total_size += size

        f.write("-" * 50 + "\n")
        f.write(f"Total: {total_size / (1024**2):.2f} MB\n")

    print(f"\n✅ Split complete! Files saved to: {OUTPUT_DIR}")
    print(f"\nCreated {len(files_created)} files:")
    for name, path, size in sorted(files_created, key=lambda x: x[2], reverse=True):
        print(f"  {name:30s} {size/(1024**2):>8.2f} MB")

    print(f"\nOriginal: {os.path.getsize(SOURCE_FILE)/(1024**3):.2f} GB")
    print(f"Split:    {sum(s for _,_,s in files_created)/(1024**2):.2f} MB")
    print(f"\nYou can now delete the original file to save space:")
    print(f"  rm {SOURCE_FILE}")

if __name__ == "__main__":
    split_analysis()
