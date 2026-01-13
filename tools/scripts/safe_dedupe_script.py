#!/usr/bin/env python3
"""
Safe Deduplication Script with Dry-Run Mode
Removes duplicates identified in dedupe_mapping.csv
"""

import csv
import os
import shutil
from pathlib import Path
import sys

def safe_remove(path, dry_run=True):
    """Safely remove file or directory"""
    path_obj = Path(path)

    if not path_obj.exists():
        return False, "Not found"

    try:
        if path_obj.is_dir():
            if dry_run:
                size = get_dir_size(str(path_obj))
                return True, f"Would remove directory ({size / (1024*1024):.1f} MB)"
            else:
                size = get_dir_size(str(path_obj))
                shutil.rmtree(str(path_obj))
                return True, f"Removed directory ({size / (1024*1024):.1f} MB)"
        else:
            size = path_obj.stat().st_size
            if dry_run:
                return True, f"Would remove file ({size / (1024*1024):.2f} MB)"
            else:
                path_obj.unlink()
                return True, f"Removed file ({size / (1024*1024):.2f} MB)"
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_dir_size(path):
    """Get directory size"""
    total = 0
    try:
        for entry in Path(path).rglob('*'):
            if entry.is_file():
                total += entry.stat().st_size
    except:
        pass
    return total

def main():
    # Check for dry-run flag
    dry_run = '--execute' not in sys.argv

    if dry_run:
        print("="*80)
        print("🔍 DRY-RUN MODE - No files will be deleted")
        print("="*80)
        print("Run with --execute to actually remove duplicates")
        print()
    else:
        print("="*80)
        print("⚠️  EXECUTION MODE - Files WILL be deleted")
        print("="*80)
        response = input("Are you sure? Type 'yes' to continue: ")
        if response.lower() != 'yes':
            print("Aborted.")
            return
        print()

    # Load dedupe mapping
    mapping_file = 'dedupe_mapping.csv'
    if not os.path.exists(mapping_file):
        print(f"❌ {mapping_file} not found. Run create_dedupe_mapping.py first.")
        return

    print(f"Loading {mapping_file}...")
    items_to_remove = []

    with open(mapping_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Include all duplicates (including archives)
            # Only process REMOVE and MERGE_REMOVE actions
            if 'REMOVE' in row['action']:
                items_to_remove.append({
                    'path': row['old_path'],
                    'reason': row['reason'],
                    'size_mb': float(row['size_mb']),
                    'similarity': row.get('similarity', 'N/A')
                })

    print(f"Found {len(items_to_remove)} items to remove (excluding archives)")
    print()

    # Sort by size (largest first)
    items_to_remove.sort(key=lambda x: x['size_mb'], reverse=True)

    # Process removals
    removed_count = 0
    error_count = 0
    total_size = 0

    print("Processing removals...")
    print("-" * 80)

    for i, item in enumerate(items_to_remove, 1):
        path = item['path']
        size_mb = item['size_mb']

        # Check if path exists
        full_path = Path('.') / path
        if not full_path.exists():
            print(f"[{i}/{len(items_to_remove)}] ⚠️  {path} - Not found (may already be removed)")
            continue

        success, message = safe_remove(str(full_path), dry_run=dry_run)

        if success:
            removed_count += 1
            total_size += size_mb
            status = "✅" if not dry_run else "🔍"
            print(f"[{i}/{len(items_to_remove)}] {status} {path[:60]:60} {message}")
        else:
            error_count += 1
            print(f"[{i}/{len(items_to_remove)}] ❌ {path[:60]:60} {message}")

        # Show progress every 50 items
        if i % 50 == 0:
            print(f"... processed {i}/{len(items_to_remove)} items ...")

    print()
    print("="*80)
    print("SUMMARY")
    print("="*80)
    if dry_run:
        print(f"🔍 DRY-RUN: Would remove {removed_count} items")
        print(f"   Space to recover: {total_size:.1f} MB")
        print(f"   Errors: {error_count}")
        print()
        print("Run with --execute to actually perform removals")
    else:
        print(f"✅ Removed {removed_count} items")
        print(f"   Space recovered: {total_size:.1f} MB")
        print(f"   Errors: {error_count}")
    print("="*80)

if __name__ == "__main__":
    main()

