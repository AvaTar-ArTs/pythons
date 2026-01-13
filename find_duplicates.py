#!/usr/bin/env python3
"""
Find duplicate files in Google Drive directories.
Identifies duplicates by name, size, and content hash.
"""
import os
import hashlib
import csv
from pathlib import Path
from collections import defaultdict

base_path = Path('/Users/steven/Library/CloudStorage/GoogleDrive-sjchaplinski@gmail.com')
output_file = Path('/Users/steven/duplicate_files_report.csv')
duplicates_file = Path('/Users/steven/duplicate_files_to_remove.csv')

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

print("Step 1: Finding files with duplicate names...")
name_duplicates = defaultdict(list)
size_duplicates = defaultdict(list)
all_files = []

count = 0
for root, dirs, files in os.walk(base_path / 'My Drive'):
    for file in files:
        file_path = Path(root) / file
        try:
            size = file_path.stat().st_size
            rel_path = str(file_path.relative_to(base_path))
            name_duplicates[file].append((rel_path, size))
            size_duplicates[size].append((rel_path, file))
            all_files.append((rel_path, file, size))
            count += 1
            if count % 1000 == 0:
                print(f"  Processed {count} files...")
        except:
            continue

for root, dirs, files in os.walk(base_path / 'Other computers'):
    for file in files:
        file_path = Path(root) / file
        try:
            size = file_path.stat().st_size
            rel_path = str(file_path.relative_to(base_path))
            name_duplicates[file].append((rel_path, size))
            size_duplicates[size].append((rel_path, file))
            all_files.append((rel_path, file, size))
            count += 1
            if count % 1000 == 0:
                print(f"  Processed {count} files...")
        except:
            continue

print(f"\nTotal files scanned: {count}")

# Find exact name duplicates
print("\nStep 2: Identifying exact name duplicates...")
exact_name_dups = {name: paths for name, paths in name_duplicates.items() if len(paths) > 1}

print(f"Found {len(exact_name_dups)} files with duplicate names")

# Find same-size duplicates (potential content duplicates)
print("\nStep 3: Identifying same-size duplicates (potential content duplicates)...")
same_size_dups = {size: paths for size, paths in size_duplicates.items() 
                  if len(paths) > 1 and size > 1000}  # Only files > 1KB

print(f"Found {len(same_size_dups)} file sizes with multiple files")

# For large same-size files, calculate hashes to confirm duplicates
print("\nStep 4: Calculating content hashes for large same-size files...")
content_duplicates = defaultdict(list)
hash_count = 0

for size, paths in list(same_size_dups.items())[:100]:  # Limit to first 100 size groups
    if size > 100000:  # Only hash files > 100KB
        for rel_path, filename in paths:
            full_path = base_path / rel_path
            file_hash = calculate_hash(full_path)
            if file_hash:
                content_duplicates[file_hash].append((rel_path, filename, size))
                hash_count += 1
                if hash_count % 50 == 0:
                    print(f"  Hashed {hash_count} files...")

print(f"\nHashed {hash_count} files for content comparison")

# Generate reports
print("\nStep 5: Generating reports...")

# Report 1: All duplicate groups
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Type', 'Key', 'File_Path', 'File_Name', 'Size', 'Size_Formatted'])
    
    # Exact name duplicates
    for name, paths in sorted(exact_name_dups.items(), key=lambda x: len(x[1]), reverse=True):
        for rel_path, size in paths:
            writer.writerow(['Exact_Name', name, rel_path, os.path.basename(rel_path), size, format_size(size)])
    
    # Content duplicates (same hash)
    for file_hash, files in content_duplicates.items():
        if len(files) > 1:
            for rel_path, filename, size in files:
                writer.writerow(['Content_Hash', file_hash[:16], rel_path, filename, size, format_size(size)])

# Report 2: Files to remove (keeping first occurrence)
with open(duplicates_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['File_Path', 'File_Name', 'Size', 'Size_Formatted', 'Duplicate_Type', 'Keep_Path', 'Reason'])
    
    removed_count = 0
    total_size = 0
    
    # Exact name duplicates - keep first, remove rest
    for name, paths in sorted(exact_name_dups.items(), key=lambda x: len(x[1]), reverse=True):
        if len(paths) > 1:
            # Sort by path (prefer "My Drive" over "Other computers")
            sorted_paths = sorted(paths, key=lambda x: (x[0].startswith('Other computers'), x[0]))
            keep_path = sorted_paths[0][0]
            
            for rel_path, size in sorted_paths[1:]:
                writer.writerow([
                    rel_path,
                    name,
                    size,
                    format_size(size),
                    'Exact_Name',
                    keep_path,
                    f'Duplicate of {keep_path}'
                ])
                removed_count += 1
                total_size += size
    
    # Content duplicates - keep first, remove rest
    for file_hash, files in content_duplicates.items():
        if len(files) > 1:
            # Sort by path
            sorted_files = sorted(files, key=lambda x: (x[0].startswith('Other computers'), x[0]))
            keep_path = sorted_files[0][0]
            
            for rel_path, filename, size in sorted_files[1:]:
                writer.writerow([
                    rel_path,
                    filename,
                    size,
                    format_size(size),
                    'Content_Hash',
                    keep_path,
                    f'Identical content to {keep_path}'
                ])
                removed_count += 1
                total_size += size

print(f"\n{'='*60}")
print(f"DUPLICATE ANALYSIS COMPLETE")
print(f"{'='*60}")
print(f"Files with duplicate names: {len(exact_name_dups)}")
print(f"Potential content duplicates: {len([g for g in content_duplicates.values() if len(g) > 1])}")
print(f"\nFiles recommended for removal: {removed_count}")
print(f"Potential space savings: {format_size(total_size)}")
print(f"\nReports saved:")
print(f"  - {output_file}")
print(f"  - {duplicates_file}")
