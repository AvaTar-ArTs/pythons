#!/usr/bin/env python3
"""
Create deduplication mapping CSV
Shows what to keep, what to remove, what to merge
"""

import json
import csv
from pathlib import Path

# Load deduplication analysis
try:
    with open('dedupe_analysis.json') as f:
        data = json.load(f)
except:
    print("Running dedupe_analysis.py first...")
    import subprocess
    subprocess.run(['python3', 'dedupe_analysis.py'])
    with open('dedupe_analysis.json') as f:
        data = json.load(f)

# Create mapping
mapping = []

# Process duplicate directories
for dup_group in data.get('duplicate_directories', []):
    dirs = sorted(dup_group['directories'], key=lambda x: x['size_bytes'], reverse=True)
    keep = dirs[0]
    for remove in dirs[1:]:
        mapping.append({
            'old_path': remove['path'],
            'action': 'REMOVE',
            'reason': f'Duplicate of {keep["path"]}',
            'size_mb': remove['size_bytes'] / (1024*1024),
            'similarity': f"{dup_group['similarity']*100:.1f}%"
        })

# Process similar folders
for group in data.get('similar_folders', []):
    items = sorted(group['items'], key=lambda x: x['size_bytes'], reverse=True)
    keep = items[0]
    for remove in items[1:]:
        mapping.append({
            'old_path': remove['path'],
            'action': 'MERGE_REMOVE',
            'reason': f'Similar to {keep["path"]} ({group["similarity"]*100:.1f}% similar)',
            'size_mb': remove['size_bytes'] / (1024*1024),
            'similarity': f"{group['similarity']*100:.1f}%"
        })

# Process duplicate files
for file_hash, files in data.get('duplicate_files', {}).items():
    if len(files) > 1:
        files_sorted = sorted(files, key=lambda x: x['size'])
        keep = files_sorted[0]
        for remove in files_sorted[1:]:
            mapping.append({
                'old_path': remove['path'],
                'action': 'REMOVE',
                'reason': f'Duplicate file of {keep["path"]}',
                'size_mb': remove['size'] / (1024*1024),
                'similarity': '100%'
            })

# Sort by size (largest waste first)
mapping.sort(key=lambda x: x['size_mb'], reverse=True)

# Write CSV
with open('dedupe_mapping.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['old_path', 'action', 'reason', 'size_mb', 'similarity'])
    writer.writeheader()
    writer.writerows(mapping)

print(f"✅ Created deduplication mapping with {len(mapping)} items to remove/merge")
print(f"Total waste: {sum(m['size_mb'] for m in mapping):.1f} MB")

