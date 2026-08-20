#!/usr/bin/env python3
"""
Create combined reorganization + deduplication plan
Excludes archives from deduplication
"""

import json
import csv
from pathlib import Path
from collections import defaultdict

# Load deduplication analysis
print("Loading deduplication analysis...")
try:
    with open('dedupe_analysis.json') as f:
        dedupe_data = json.load(f)
except FileNotFoundError:
    print("❌ dedupe_analysis.json not found. Run dedupe_analysis.py first.")
    exit(1)

# Load dedupe mapping
print("Loading dedupe mapping...")
duplicates_to_remove = set()
with open('dedupe_mapping.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Include all duplicates (including archives)
        duplicates_to_remove.add(row['old_path'])

print(f"Found {len(duplicates_to_remove)} duplicates to remove")

# Map to existing structure (don't create new directories)
def determine_new_path(old_path):
    """Determine new simplified path"""
    old_path_lower = old_path.lower()

    # Skip duplicates
    if old_path in duplicates_to_remove:
        return None, "REMOVE_DUPLICATE"

    path_parts = old_path.split('/')

    # Root level files
    if '/' not in old_path:
        if old_path.endswith(('.md', '.txt', '.html')):
            return f"docs/{old_path}", "documentation"
        elif old_path.endswith(('.py', '.sh', '.csv')):
            return f"projects/{old_path}", "project"
        else:
            return f"projects/{old_path}", "project"

    # Categorize by folder name/path
    if any(x in old_path_lower for x in ['client', 'joseph', 'customer']):
        return f"projects/{path_parts[-1] if path_parts else old_path}", "client_project"

    if any(x in old_path_lower for x in ['business', 'monet', 'income', 'revenue', 'agency']):
        return f"projects/{path_parts[-1] if path_parts else old_path}", "business"

    if any(x in old_path_lower for x in ['dev', 'code', 'tool', 'script', 'automation', 'utility']):
        return f"projects/{path_parts[-1] if path_parts else old_path}", "development"

    if any(x in old_path_lower for x in ['content', 'asset', 'image', 'audio', 'video', 'music', 'gallery', 'media', 'ai-sites']):
        return f"content/{path_parts[-1] if path_parts else old_path}", "content"

    if any(x in old_path_lower for x in ['doc', 'guide', 'manual', 'analysis', 'report', 'plan', 'index', 'documentation']):
        return f"docs/{path_parts[-1] if path_parts else old_path}", "documentation"

    if any(x in old_path_lower for x in ['website', 'site', 'github', 'html', 'web']):
        return f"projects/{path_parts[-1] if path_parts else old_path}", "website"

    if any(x in old_path_lower for x in ['data', 'analytics', 'csv', 'json']):
        return f"projects/{path_parts[-1] if path_parts else old_path}", "data"

    # Default to projects
    return f"projects/{path_parts[-1] if path_parts else old_path}", "project"

# Get all directories and files from directory analysis
print("Loading directory structure...")
try:
    with open('directory_analysis.json') as f:
        dir_data = json.load(f)
except FileNotFoundError:
    print("⚠️  directory_analysis.json not found. Using basic structure.")
    dir_data = {'flat_structure': [], 'root_files': []}

# Build mapping
mapping = []
seen_new_paths = defaultdict(int)

# Process directories from flat structure
for item in dir_data.get('flat_structure', []):
    old_path = item['path']
    new_path, category = determine_new_path(old_path)

    if new_path is None:  # Skip or remove
        mapping.append({
            'old_path': old_path,
            'new_path': '',
            'action': category,
            'category': '',
            'size_mb': item.get('size_bytes', 0) / (1024*1024),
            'file_count': item.get('file_count', 0)
        })
    else:
        # Handle name conflicts
        base_new_path = new_path
        conflict_count = seen_new_paths[new_path]
        if conflict_count > 0:
            # Add parent context to avoid conflicts
            path_parts = old_path.split('/')
            if len(path_parts) > 1:
                new_path = f"{base_new_path.rsplit('/', 1)[0]}/{path_parts[-2]}_{path_parts[-1]}"
            else:
                new_path = f"{base_new_path}_{conflict_count}"
        seen_new_paths[base_new_path] += 1

        mapping.append({
            'old_path': old_path,
            'new_path': new_path,
            'action': 'MOVE',
            'category': category,
            'size_mb': item.get('size_bytes', 0) / (1024*1024),
            'file_count': item.get('file_count', 0)
        })

# Process root files
for root_file in dir_data.get('root_files', []):
    root_file_str = str(root_file)
    if '/' in root_file_str:
        root_file_str = root_file_str.split('/', 1)[-1]

    new_path, category = determine_new_path(root_file_str)

    if new_path is None:
        mapping.append({
            'old_path': root_file_str,
            'new_path': '',
            'action': category,
            'category': '',
            'size_mb': 0,
            'file_count': 1
        })
    else:
        mapping.append({
            'old_path': root_file_str,
            'new_path': new_path,
            'action': 'MOVE',
            'category': category,
            'size_mb': 0,
            'file_count': 1
        })

# Sort by action (REMOVE first, then MOVE)
mapping.sort(key=lambda x: (
    0 if x['action'] in ['REMOVE_DUPLICATE', 'SKIP_ARCHIVE'] else 1,
    -x['size_mb']  # Largest first
))

# Write CSV
print(f"\nCreating combined reorganization plan...")
print(f"Total items: {len(mapping)}")

with open('combined_reorganization_plan.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['old_path', 'new_path', 'action', 'category', 'size_mb', 'file_count'])
    writer.writeheader()
    writer.writerows(mapping)

# Summary
remove_count = sum(1 for m in mapping if 'REMOVE' in m['action'])
move_count = sum(1 for m in mapping if m['action'] == 'MOVE')
skip_count = sum(1 for m in mapping if 'SKIP' in m['action'])
remove_size = sum(m['size_mb'] for m in mapping if 'REMOVE' in m['action'])

print("\n" + "="*80)
print("COMBINED REORGANIZATION PLAN SUMMARY")
print("="*80)
print(f"Total items: {len(mapping)}")
print(f"  - To MOVE: {move_count}")
print(f"  - To REMOVE (duplicates): {remove_count}")
print(f"  - To SKIP (archives): {skip_count}")
print(f"Space to recover: {remove_size:.1f} MB")
print(f"\n✅ Plan saved to: combined_reorganization_plan.csv")
print("="*80)

