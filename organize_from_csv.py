#!/usr/bin/env python3
"""
Organize & Deduplicate based on docs.csv analysis.
Scans the CSV, identifies duplicates, creates cleanup plan, and optionally applies fixes.

Usage:
    python organize_from_csv.py /path/to/docs.csv [--apply] [--dry-run]
"""

import csv
import os
import sys
import hashlib
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def load_csv(csv_path):
    """Load docs.csv and return list of dicts."""
    rows = []
    with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    print(f"📊 Loaded {len(rows):,} files from CSV")
    return rows

def find_name_duplicates(rows):
    """Find files with same name in different locations."""
    by_name = defaultdict(list)
    for row in rows:
        name = row.get('Filename', '').strip()
        path = row.get('Original Path', '').strip()
        if name and path:
            by_name[name].append(row)
    
    duplicates = {name: entries for name, entries in by_name.items() if len(entries) > 1}
    print(f"🔍 Found {len(duplicates):,} filenames with duplicates")
    return duplicates

def find_exact_content_duplicates(rows, sample_size=1000):
    """Use SHA256 to find true content duplicates."""
    by_hash = defaultdict(list)
    for row in rows:
        path = row.get('Original Path', '').strip()
        name = row.get('Filename', '').strip()
        if path and name:
            full_path = os.path.join(path, name)
            if os.path.exists(full_path):
                try:
                    with open(full_path, 'rb') as f:
                        content = f.read(sample_size)
                    h = hashlib.sha256(content).hexdigest()[:16]
                    by_hash[h].append(row)
                except (PermissionError, OSError):
                    pass
    
    exact_dups = {h: entries for h, entries in by_hash.items() if len(entries) > 1}
    print(f"🔒 Found {len(exact_dups):,} groups of exact content duplicates")
    return exact_dups

def generate_cleanup_plan(name_dups, exact_dups, output_path):
    """Create a CSV cleanup plan."""
    plan_rows = []
    
    # Exact duplicates - safe to remove
    for h, entries in exact_dups.items():
        # Keep the one in the most "important" location
        priority_dirs = [
            '10-gumroad-bundles',
            '04-codester-products',
            'TOOLS_UTILITIES',
            'tests',
            '13-launch-plan',
        ]
        
        def priority(row):
            path = row.get('Original Path', '')
            for i, pdir in enumerate(priority_dirs):
                if pdir in path:
                    return i
            return len(priority_dirs)
        
        entries_sorted = sorted(entries, key=priority)
        keeper = entries_sorted[0]
        
        for entry in entries_sorted[1:]:
            plan_rows.append({
                'Action': 'DELETE_EXACT_DUPLICATE',
                'File': entry.get('Filename', ''),
                'Path': entry.get('Original Path', ''),
                'Size': entry.get('File Size', ''),
                'Keep At': f"{keeper.get('Original Path', '')}/{keeper.get('Filename', '')}",
                'Reason': f'Exact content duplicate (hash {h})',
            })
    
    # Name duplicates (potential)
    for name, entries in sorted(name_dups.items(), key=lambda x: -len(x[1]))[:50]:
        for entry in entries:
            plan_rows.append({
                'Action': 'REVIEW_NAME_DUPLICATE',
                'File': entry.get('Filename', ''),
                'Path': entry.get('Original Path', ''),
                'Size': entry.get('File Size', ''),
                'Keep At': 'manual review needed',
                'Reason': f'{len(entries)} files named "{name}"',
            })
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Action', 'File', 'Path', 'Size', 'Keep At', 'Reason'])
        writer.writeheader()
        writer.writerows(plan_rows)
    
    print(f"📋 Cleanup plan saved to: {output_path}")
    print(f"   {sum(1 for r in plan_rows if r['Action'] == 'DELETE_EXACT_DUPLICATE')} exact duplicates to remove")
    print(f"   {sum(1 for r in plan_rows if r['Action'] == 'REVIEW_NAME_DUPLICATE')} name duplicates to review")

def apply_cleanup(plan_path, dry_run=True):
    """Execute the cleanup plan."""
    if not os.path.exists(plan_path):
        print(f"❌ Plan not found: {plan_path}")
        return
    
    with open(plan_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    deleted = 0
    errors = 0
    
    for row in rows:
        if row['Action'] == 'DELETE_EXACT_DUPLICATE':
            full_path = os.path.join(row['Path'], row['File'])
            if os.path.exists(full_path):
                if not dry_run:
                    try:
                        # Move to trash instead of delete
                        trash = os.path.join(os.path.dirname(full_path), '_TRASH')
                        os.makedirs(trash, exist_ok=True)
                        trash_path = os.path.join(trash, row['File'])
                        trash_path = get_unique_path(trash_path)
                        shutil.move(full_path, trash_path)
                        deleted += 1
                    except Exception as e:
                        print(f"  ❌ Error moving {full_path}: {e}")
                        errors += 1
                else:
                    deleted += 1
    
    action = "Would move to _TRASH" if dry_run else "Moved to _TRASH"
    print(f"\n✅ {action}: {deleted} files")
    if errors:
        print(f"   ❌ Errors: {errors}")

def get_unique_path(path):
    """Get unique path by appending counter if exists."""
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    counter = 1
    while True:
        new_path = f"{base}_{counter}{ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1

def main():
    if len(sys.argv) < 2:
        print("Usage: python organize_from_csv.py <docs.csv> [--apply] [--dry-run]")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    apply = '--apply' in sys.argv
    dry_run = '--dry-run' in sys.argv or not apply
    
    print(f"=== Organization & Dedup from CSV ===")
    print(f"Source: {csv_path}")
    print(f"Mode: {'DRY RUN' if dry_run else 'APPLY'}\n")
    
    rows = load_csv(csv_path)
    base_dir = os.path.dirname(csv_path)
    
    print(f"\n🔍 Finding duplicates...")
    name_dups = find_name_duplicates(rows)
    exact_dups = find_exact_content_duplicates(rows)
    
    plan_path = os.path.join(base_dir, 'dedup_cleanup_plan.csv')
    generate_cleanup_plan(name_dups, exact_dups, plan_path)
    
    if apply or dry_run:
        print(f"\n🧹 Applying cleanup ({'DRY RUN' if dry_run else 'LIVE'})...")
        apply_cleanup(plan_path, dry_run=dry_run)
    
    print(f"\n✅ Done!")

if __name__ == "__main__":
    main()
