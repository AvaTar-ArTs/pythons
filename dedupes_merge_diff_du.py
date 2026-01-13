#!/usr/bin/env python3
"""
Comprehensive analysis: Deduplication, Merge, Diff, and Disk Usage
"""
import os
import hashlib
import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime

downloads_path = Path.home() / 'Downloads'
output_dir = Path('/Users/steven/Downloads_Analysis')

# Create output directory
output_dir.mkdir(exist_ok=True)

dedupes_file = output_dir / 'deduplicates.csv'
merge_file = output_dir / 'merge_analysis.csv'
diff_file = output_dir / 'diff_analysis.csv'
du_file = output_dir / 'disk_usage.csv'
summary_file = output_dir / 'comprehensive_summary.md'

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
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

print("="*70)
print("COMPREHENSIVE ANALYSIS: DEDUPES, MERGE, DIFF, DU")
print("="*70)
print(f"Scanning: {downloads_path}\n")

# Data structures
all_files = []
file_hashes = defaultdict(list)
file_sizes = defaultdict(list)
file_names = defaultdict(list)
folder_sizes = defaultdict(int)
folder_counts = defaultdict(int)

print("Step 1: Scanning files and calculating hashes...")
count = 0
hash_count = 0

for root, dirs, files in os.walk(downloads_path):
    rel_root = str(Path(root).relative_to(downloads_path))
    
    for file in files:
        file_path = Path(root) / file
        try:
            stat = file_path.stat()
            size = stat.st_size
            rel_path = str(file_path.relative_to(downloads_path))
            
            # Calculate hash for files > 0 bytes
            file_hash = None
            if size > 0:
                file_hash = calculate_hash(file_path)
                if file_hash:
                    file_hashes[file_hash].append((rel_path, file, size))
                    hash_count += 1
            
            # Track by size
            file_sizes[size].append((rel_path, file))
            
            # Track by name
            file_names[file].append((rel_path, size))
            
            # Track folder usage
            folder_sizes[rel_root] += size
            folder_counts[rel_root] += 1
            
            all_files.append({
                'path': rel_path,
                'name': file,
                'size': size,
                'hash': file_hash,
                'folder': rel_root
            })
            
            count += 1
            if count % 5000 == 0:
                print(f"  Processed {count} files, hashed {hash_count}...")
        except Exception as e:
            continue

print(f"\nTotal files: {count:,}")
print(f"Files hashed: {hash_count:,}")

# 1. DEDUPLICATION ANALYSIS
print("\n" + "="*70)
print("STEP 2: DEDUPLICATION ANALYSIS")
print("="*70)

duplicates = {h: files for h, files in file_hashes.items() if len(files) > 1}
duplicate_count = sum(len(files) - 1 for files in duplicates.values())
duplicate_size = 0

for file_hash, files in duplicates.items():
    # Size of duplicates (excluding first occurrence)
    for rel_path, name, size in files[1:]:
        duplicate_size += size

print(f"Duplicate groups found: {len(duplicates):,}")
print(f"Duplicate files: {duplicate_count:,}")
print(f"Wasted space: {format_size(duplicate_size)}")

# Write deduplicates CSV
with open(dedupes_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Hash', 'File_Path', 'File_Name', 'Size', 'Size_Formatted', 'Group_Size', 'Keep_File'])
    
    for file_hash, files in sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True):
        sorted_files = sorted(files, key=lambda x: x[0])  # Sort by path
        keep_file = sorted_files[0][0]
        
        for rel_path, name, size in sorted_files:
            writer.writerow([
                file_hash[:16],
                rel_path,
                name,
                size,
                format_size(size),
                len(files),
                'YES' if rel_path == keep_file else 'NO'
            ])

print(f"Saved: {dedupes_file}")

# 2. MERGE ANALYSIS (files that could be merged/consolidated)
print("\n" + "="*70)
print("STEP 3: MERGE ANALYSIS (Similar files that could be consolidated)")
print("="*70)

# Find files with same name but different locations
merge_candidates = {name: files for name, files in file_names.items() if len(files) > 1}
merge_count = sum(len(files) - 1 for files in merge_candidates.values())
merge_size = 0

for name, files in merge_candidates.items():
    # Group by size (same name + same size = likely duplicates)
    size_groups = defaultdict(list)
    for rel_path, size in files:
        size_groups[size].append(rel_path)
    
    # For each size group with multiple files
    for size, paths in size_groups.items():
        if len(paths) > 1:
            merge_size += size * (len(paths) - 1)

print(f"Files with duplicate names: {len(merge_candidates):,}")
print(f"Potential merge candidates: {merge_count:,}")
print(f"Potential space savings: {format_size(merge_size)}")

# Write merge analysis CSV
with open(merge_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['File_Name', 'File_Path', 'Size', 'Size_Formatted', 'Occurrences', 'Same_Size_Count'])
    
    for name, files in sorted(merge_candidates.items(), key=lambda x: len(x[1]), reverse=True):
        size_groups = defaultdict(list)
        for rel_path, size in files:
            size_groups[size].append(rel_path)
        
        for size, paths in size_groups.items():
            for rel_path in paths:
                writer.writerow([
                    name,
                    rel_path,
                    size,
                    format_size(size),
                    len(files),
                    len(paths)
                ])

print(f"Saved: {merge_file}")

# 3. DIFF ANALYSIS (files with same name but different content)
print("\n" + "="*70)
print("STEP 4: DIFF ANALYSIS (Same name, different content)")
print("="*70)

diff_candidates = []
for name, files in merge_candidates.items():
    if len(files) > 1:
        # Group by hash if available
        hash_groups = defaultdict(list)
        size_groups = defaultdict(list)
        
        for rel_path, size in files:
            # Find hash for this file
            file_path = downloads_path / rel_path
            file_hash = None
            if size > 0:
                file_hash = calculate_hash(file_path)
            
            if file_hash:
                hash_groups[file_hash].append((rel_path, size))
            size_groups[size].append(rel_path)
        
        # If same name but different hashes, they're different
        if len(hash_groups) > 1:
            for file_hash, file_list in hash_groups.items():
                for rel_path, size in file_list:
                    diff_candidates.append({
                        'name': name,
                        'path': rel_path,
                        'size': size,
                        'hash': file_hash[:16],
                        'variants': len(hash_groups)
                    })

print(f"Files with same name but different content: {len(diff_candidates):,}")

# Write diff analysis CSV
with open(diff_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['File_Name', 'File_Path', 'Size', 'Size_Formatted', 'Hash', 'Variants'])
    
    for item in sorted(diff_candidates, key=lambda x: x['variants'], reverse=True):
        writer.writerow([
            item['name'],
            item['path'],
            item['size'],
            format_size(item['size']),
            item['hash'],
            item['variants']
        ])

print(f"Saved: {diff_file}")

# 4. DISK USAGE (DU) ANALYSIS
print("\n" + "="*70)
print("STEP 5: DISK USAGE (DU) ANALYSIS")
print("="*70)

# Sort folders by size
sorted_folders = sorted(folder_sizes.items(), key=lambda x: x[1], reverse=True)
total_size = sum(folder_sizes.values())

print(f"Total folders analyzed: {len(sorted_folders):,}")
print(f"Total size: {format_size(total_size)}")

# Write disk usage CSV
with open(du_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Folder', 'Size', 'Size_Formatted', 'File_Count', 'Percent_Of_Total'])
    
    for folder, size in sorted_folders:
        pct = (size / total_size * 100) if total_size > 0 else 0
        folder_display = folder if folder != '.' else '(root)'
        writer.writerow([
            folder_display,
            size,
            format_size(size),
            folder_counts[folder],
            f"{pct:.2f}%"
        ])

print(f"Saved: {du_file}")

# Generate comprehensive summary
print("\n" + "="*70)
print("STEP 6: GENERATING SUMMARY REPORT")
print("="*70)

with open(summary_file, 'w', encoding='utf-8') as f:
    f.write("# Comprehensive Downloads Analysis Report\n\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"**Location:** {downloads_path}\n\n")
    
    f.write("## Executive Summary\n\n")
    f.write(f"- **Total Files:** {count:,}\n")
    f.write(f"- **Total Size:** {format_size(total_size)}\n")
    f.write(f"- **Total Folders:** {len(sorted_folders):,}\n\n")
    
    f.write("## 1. Deduplication Analysis\n\n")
    f.write(f"- **Duplicate Groups:** {len(duplicates):,}\n")
    f.write(f"- **Duplicate Files:** {duplicate_count:,}\n")
    f.write(f"- **Wasted Space:** {format_size(duplicate_size)}\n")
    f.write(f"- **Potential Savings:** {format_size(duplicate_size)}\n\n")
    
    f.write("### Top 20 Largest Duplicate Groups\n\n")
    f.write("| Hash | Files | Total Size | Wasted Space |\n")
    f.write("|------|-------|------------|--------------|\n")
    sorted_dups = sorted(duplicates.items(), key=lambda x: len(x[1]) * x[1][0][2], reverse=True)
    for file_hash, files in sorted_dups[:20]:
        total_sz = sum(size for _, _, size in files)
        wasted = total_sz - files[0][2]  # Size minus one copy
        f.write(f"| `{file_hash[:16]}...` | {len(files)} | {format_size(total_sz)} | {format_size(wasted)} |\n")
    f.write("\n")
    
    f.write("## 2. Merge Analysis\n\n")
    f.write(f"- **Files with Duplicate Names:** {len(merge_candidates):,}\n")
    f.write(f"- **Potential Merge Candidates:** {merge_count:,}\n")
    f.write(f"- **Potential Space Savings:** {format_size(merge_size)}\n\n")
    
    f.write("### Top 20 Most Duplicated Filenames\n\n")
    f.write("| Filename | Occurrences | Total Size |\n")
    f.write("|----------|-------------|------------|\n")
    sorted_merge = sorted(merge_candidates.items(), key=lambda x: len(x[1]), reverse=True)
    for name, files in sorted_merge[:20]:
        total_sz = sum(size for _, size in files)
        f.write(f"| `{name}` | {len(files)} | {format_size(total_sz)} |\n")
    f.write("\n")
    
    f.write("## 3. Diff Analysis\n\n")
    f.write(f"- **Files with Same Name, Different Content:** {len(diff_candidates):,}\n")
    f.write("These files have the same name but different content (different hashes).\n\n")
    
    f.write("## 4. Disk Usage (DU) Analysis\n\n")
    f.write("### Top 20 Largest Folders\n\n")
    f.write("| Folder | Size | File Count | % of Total |\n")
    f.write("|--------|------|------------|------------|\n")
    for folder, size in sorted_folders[:20]:
        pct = (size / total_size * 100) if total_size > 0 else 0
        folder_display = folder if folder != '.' else '(root)'
        f.write(f"| `{folder_display}` | {format_size(size)} | {folder_counts[folder]:,} | {pct:.2f}% |\n")
    f.write("\n")
    
    f.write("## Recommendations\n\n")
    f.write("1. **Remove Duplicates:** Free up {format_size(duplicate_size)} by removing duplicate files\n")
    f.write("2. **Consolidate Files:** Review merge candidates to consolidate similar files\n")
    f.write("3. **Review Large Folders:** Focus cleanup efforts on largest folders\n")
    f.write("4. **Archive Old Files:** Consider archiving files in largest folders\n\n")
    
    f.write("## Files Generated\n\n")
    f.write(f"- `deduplicates.csv` - Complete duplicate file analysis\n")
    f.write(f"- `merge_analysis.csv` - Files that could be merged/consolidated\n")
    f.write(f"- `diff_analysis.csv` - Files with same name but different content\n")
    f.write(f"- `disk_usage.csv` - Folder-by-folder disk usage\n")
    f.write(f"- `comprehensive_summary.md` - This summary report\n\n")

print(f"Saved: {summary_file}")

print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)
print(f"\nFiles generated in: {output_dir}")
print(f"  - deduplicates.csv ({len(duplicates):,} duplicate groups)")
print(f"  - merge_analysis.csv ({len(merge_candidates):,} merge candidates)")
print(f"  - diff_analysis.csv ({len(diff_candidates):,} diff candidates)")
print(f"  - disk_usage.csv ({len(sorted_folders):,} folders)")
print(f"  - comprehensive_summary.md")
print("\n" + "="*70)
