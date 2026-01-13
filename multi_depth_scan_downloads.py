#!/usr/bin/env python3
"""
Multi-depth folder scan of Downloads directory.
Analyzes structure, sizes, file types, and organization at multiple depth levels.
"""
import os
import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime

downloads_path = Path.home() / 'Downloads'
output_file = Path('/Users/steven/Downloads_MultiDepth_Analysis.csv')
summary_file = Path('/Users/steven/Downloads_MultiDepth_Summary.md')

def format_size(size_bytes):
    """Format bytes to human readable size"""
    if size_bytes == 0:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def get_file_extension(filename):
    """Get file extension"""
    if '.' in filename:
        return filename.split('.')[-1].lower()
    return 'no-ext'

print("="*60)
print("MULTI-DEPTH FOLDER SCAN - DOWNLOADS")
print("="*60)
print(f"Scanning: {downloads_path}\n")

# Data structures
depth_stats = defaultdict(lambda: {'files': 0, 'size': 0, 'dirs': 0})
folder_stats = {}
file_type_stats = defaultdict(lambda: {'count': 0, 'size': 0})
all_files = []
max_depth = 0

# Scan files
print("Step 1: Scanning all files...")
count = 0
for root, dirs, files in os.walk(downloads_path):
    rel_root = str(Path(root).relative_to(downloads_path))
    depth = len(Path(rel_root).parts) if rel_root != '.' else 0
    max_depth = max(max_depth, depth)
    
    # Track directory
    if rel_root not in folder_stats:
        folder_stats[rel_root] = {'files': 0, 'size': 0, 'depth': depth}
    
    for file in files:
        file_path = Path(root) / file
        try:
            size = file_path.stat().st_size
            rel_path = str(file_path.relative_to(downloads_path))
            ext = get_file_extension(file)
            
            # Update stats
            depth_stats[depth]['files'] += 1
            depth_stats[depth]['size'] += size
            folder_stats[rel_root]['files'] += 1
            folder_stats[rel_root]['size'] += size
            file_type_stats[ext]['count'] += 1
            file_type_stats[ext]['size'] += size
            
            all_files.append({
                'path': rel_path,
                'name': file,
                'size': size,
                'depth': depth,
                'folder': rel_root,
                'extension': ext
            })
            
            count += 1
            if count % 5000 == 0:
                print(f"  Processed {count} files...")
        except Exception as e:
            continue
    
    # Count directories at this depth
    depth_stats[depth]['dirs'] += len(dirs)

print(f"\nTotal files scanned: {count}")
print(f"Maximum depth: {max_depth}")

# Count directories
print("\nStep 2: Counting directories...")
total_dirs = 0
for root, dirs, files in os.walk(downloads_path):
    total_dirs += len(dirs)

print(f"Total directories: {total_dirs}")

# Calculate folder sizes
print("\nStep 3: Calculating folder sizes...")
for folder_path, stats in folder_stats.items():
    if folder_path != '.':
        # Calculate total size including subdirectories
        full_path = downloads_path / folder_path
        if full_path.exists():
            try:
                total_size = sum(f.stat().st_size for f in full_path.rglob('*') if f.is_file())
                stats['total_size'] = total_size
            except:
                stats['total_size'] = stats['size']

# Write CSV with all file details
print("\nStep 4: Writing detailed CSV...")
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['File_Path', 'File_Name', 'Size', 'Size_Formatted', 'Depth', 'Folder', 'Extension'])
    writer.writeheader()
    for item in sorted(all_files, key=lambda x: x['size'], reverse=True):
        writer.writerow({
            'File_Path': item['path'],
            'File_Name': item['name'],
            'Size': item['size'],
            'Size_Formatted': format_size(item['size']),
            'Depth': item['depth'],
            'Folder': item['folder'],
            'Extension': item['extension']
        })

# Generate summary report
print("\nStep 5: Generating summary report...")
with open(summary_file, 'w', encoding='utf-8') as f:
    f.write("# Downloads Multi-Depth Analysis Report\n\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"**Location:** {downloads_path}\n\n")
    
    f.write("## Executive Summary\n\n")
    f.write(f"- **Total Files:** {count:,}\n")
    f.write(f"- **Total Directories:** {total_dirs:,}\n")
    f.write(f"- **Maximum Depth:** {max_depth} levels\n")
    total_size = sum(item['size'] for item in all_files)
    f.write(f"- **Total Size:** {format_size(total_size)}\n\n")
    
    f.write("## Files by Depth Level\n\n")
    f.write("| Depth | Files | Size | Directories |\n")
    f.write("|-------|-------|------|-------------|\n")
    for depth in sorted(depth_stats.keys()):
        stats = depth_stats[depth]
        f.write(f"| {depth} | {stats['files']:,} | {format_size(stats['size'])} | {stats['dirs']:,} |\n")
    f.write("\n")
    
    f.write("## Top 20 Largest Folders\n\n")
    f.write("| Folder | Files | Size | Total Size (with subdirs) | Depth |\n")
    f.write("|--------|-------|------|---------------------------|-------|\n")
    sorted_folders = sorted(folder_stats.items(), key=lambda x: x[1].get('total_size', x[1]['size']), reverse=True)
    for folder, stats in sorted_folders[:20]:
        folder_display = folder if folder != '.' else '(root)'
        total_sz = stats.get('total_size', stats['size'])
        f.write(f"| `{folder_display}` | {stats['files']:,} | {format_size(stats['size'])} | {format_size(total_sz)} | {stats['depth']} |\n")
    f.write("\n")
    
    f.write("## File Types (Top 30)\n\n")
    f.write("| Extension | Count | Size | Avg Size |\n")
    f.write("|-----------|-------|------|----------|\n")
    sorted_types = sorted(file_type_stats.items(), key=lambda x: x[1]['size'], reverse=True)
    for ext, stats in sorted_types[:30]:
        avg = stats['size'] / stats['count'] if stats['count'] > 0 else 0
        f.write(f"| `.{ext}` | {stats['count']:,} | {format_size(stats['size'])} | {format_size(avg)} |\n")
    f.write("\n")
    
    f.write("## Largest Files (Top 20)\n\n")
    f.write("| File | Size | Depth | Folder |\n")
    f.write("|------|------|-------|--------|\n")
    sorted_files = sorted(all_files, key=lambda x: x['size'], reverse=True)
    for item in sorted_files[:20]:
        f.write(f"| `{item['name']}` | {format_size(item['size'])} | {item['depth']} | `{item['folder']}` |\n")
    f.write("\n")
    
    f.write("## Depth Distribution\n\n")
    f.write("Files are distributed across depth levels as follows:\n\n")
    for depth in sorted(depth_stats.keys()):
        stats = depth_stats[depth]
        pct = (stats['files'] / count * 100) if count > 0 else 0
        f.write(f"- **Depth {depth}:** {stats['files']:,} files ({pct:.1f}%) - {format_size(stats['size'])}\n")
    f.write("\n")
    
    f.write("## Folder Structure Analysis\n\n")
    f.write(f"Total folders analyzed: {len(folder_stats)}\n")
    f.write(f"Average files per folder: {count / len(folder_stats):.1f}\n")
    f.write(f"Average folder depth: {sum(s['depth'] for s in folder_stats.values()) / len(folder_stats):.1f}\n\n")

print(f"\n{'='*60}")
print("ANALYSIS COMPLETE")
print(f"{'='*60}")
print(f"Files analyzed: {count:,}")
print(f"Directories: {total_dirs:,}")
print(f"Maximum depth: {max_depth}")
print(f"\nReports generated:")
print(f"  - {output_file}")
print(f"  - {summary_file}")
print(f"{'='*60}\n")
