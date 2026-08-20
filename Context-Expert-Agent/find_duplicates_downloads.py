#!/usr/bin/env python3
"""
Find and remove duplicate files in Downloads directory.
"""
import os
import hashlib
import csv
from pathlib import Path
from collections import defaultdict

downloads_path = Path.home() / 'Downloads'
output_file = Path('/Users/steven/downloads_duplicates_report.csv')
duplicates_file = Path('/Users/steven/downloads_duplicates_to_remove.csv')

def calculate_hash(file_path, chunk_size=8192):
    """Calculate MD5 hash of file content"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        return None

def format_size(size_bytes):
    """Format bytes to human readable size"""
    if size_bytes == 0:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

print(f"Scanning Downloads directory: {downloads_path}")
print("Step 1: Finding files...")

all_files = []
content_hashes = defaultdict(list)
name_duplicates = defaultdict(list)

count = 0
for root, dirs, files in os.walk(downloads_path):
    for file in files:
        file_path = Path(root) / file
        try:
            size = file_path.stat().st_size
            rel_path = str(file_path.relative_to(downloads_path))
            all_files.append((rel_path, file, size))
            name_duplicates[file].append((rel_path, size))
            count += 1
            if count % 100 == 0:
                print(f"  Processed {count} files...")
        except:
            continue

print(f"\nTotal files found: {count}")

# Calculate hashes for files to find content duplicates
print("\nStep 2: Calculating content hashes for duplicate detection...")
hash_count = 0
for rel_path, filename, size in all_files:
    if size > 0:  # Skip empty files
        full_path = downloads_path / rel_path
        file_hash = calculate_hash(full_path)
        if file_hash:
            content_hashes[file_hash].append((rel_path, filename, size))
            hash_count += 1
            if hash_count % 50 == 0:
                print(f"  Hashed {hash_count} files...")

print(f"\nHashed {hash_count} files")

# Find duplicates
print("\nStep 3: Identifying duplicates...")
exact_name_dups = {name: paths for name, paths in name_duplicates.items() if len(paths) > 1}
content_dups = {h: files for h, files in content_hashes.items() if len(files) > 1}

print(f"Files with duplicate names: {len(exact_name_dups)}")
print(f"Content duplicates (same hash): {len(content_dups)}")

# Generate removal list
print("\nStep 4: Generating removal list...")
files_to_remove = []
total_size = 0

# Content duplicates - keep first, remove rest
for file_hash, files in content_dups.items():
    if len(files) > 1:
        sorted_files = sorted(files, key=lambda x: x[0])  # Sort by path
        keep_path = sorted_files[0][0]
        for rel_path, filename, size in sorted_files[1:]:
            files_to_remove.append({
                'path': rel_path,
                'name': filename,
                'size': size,
                'type': 'Content_Hash',
                'keep_path': keep_path,
                'reason': f'Identical content to {keep_path}'
            })
            total_size += size

# Exact name duplicates (only if same size - likely same file)
for name, paths in exact_name_dups.items():
    if len(paths) > 1:
        # Group by size
        size_groups = defaultdict(list)
        for rel_path, size in paths:
            size_groups[size].append(rel_path)
        
        # For each size group with multiple files, keep first
        for size, path_list in size_groups.items():
            if len(path_list) > 1:
                sorted_paths = sorted(path_list)
                keep_path = sorted_paths[0]
                for rel_path in sorted_paths[1:]:
                    # Only add if not already in content duplicates
                    if not any(f['path'] == rel_path for f in files_to_remove):
                        files_to_remove.append({
                            'path': rel_path,
                            'name': name,
                            'size': size,
                            'type': 'Exact_Name_Same_Size',
                            'keep_path': keep_path,
                            'reason': f'Same name and size as {keep_path}'
                        })
                        total_size += size

print(f"\nFiles to remove: {len(files_to_remove)}")
print(f"Total size: {format_size(total_size)}")

# Write CSV
with open(duplicates_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['File_Path', 'File_Name', 'Size', 'Size_Formatted', 'Duplicate_Type', 'Keep_Path', 'Reason'])
    writer.writeheader()
    for item in files_to_remove:
        writer.writerow({
            'File_Path': item['path'],
            'File_Name': item['name'],
            'Size': item['size'],
            'Size_Formatted': format_size(item['size']),
            'Duplicate_Type': item['type'],
            'Keep_Path': item['keep_path'],
            'Reason': item['reason']
        })

print(f"\n{'='*60}")
print(f"DUPLICATE ANALYSIS COMPLETE")
print(f"{'='*60}")
print(f"Files to remove: {len(files_to_remove)}")
print(f"Space savings: {format_size(total_size)}")
print(f"\nReport saved: {duplicates_file}")
print(f"{'='*60}\n")
