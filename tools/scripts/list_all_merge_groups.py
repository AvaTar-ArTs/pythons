#!/usr/bin/env python3
"""
List all merge groups identified
"""

import csv
from collections import defaultdict
from pathlib import Path

mapping_file = 'dedupe_mapping.csv'
merge_groups = defaultdict(list)

print("="*80)
print("ALL 257 MERGE GROUPS IDENTIFIED")
print("="*80)
print()

with open(mapping_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if 'MERGE' in row['action']:
            reason = row['reason']
            if 'Similar to' in reason:
                target = reason.split('Similar to ')[1].split(' (')[0]
                merge_groups[target].append({
                    'source': row['old_path'],
                    'size_mb': float(row.get('size_mb', 0)),
                    'similarity': row.get('similarity', 'N/A')
                })

# Sort by total size
sorted_groups = sorted(
    merge_groups.items(),
    key=lambda x: sum(item['size_mb'] for item in x[1]),
    reverse=True
)

print(f"Total Merge Groups: {len(sorted_groups)}\n")
print("="*80)
print()

for i, (target, items) in enumerate(sorted_groups, 1):
    total_size = sum(item['size_mb'] for item in items)
    print(f"{i}. TARGET: {target}")
    print(f"   Size: {total_size:.2f} MB")
    print(f"   Sources to merge: {len(items)}")
    print(f"   Sources:")
    for item in items:
        print(f"      - {item['source']} ({item['size_mb']:.2f} MB, {item['similarity']})")
    print()

print("="*80)
print(f"Total: {len(sorted_groups)} merge groups")
total_merge_size = sum(sum(item['size_mb'] for item in items) for _, items in sorted_groups)
print(f"Total merge size: {total_merge_size:.2f} MB ({total_merge_size/1024:.2f} GB)")
print("="*80)
