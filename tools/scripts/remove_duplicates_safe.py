#!/usr/bin/env python3
"""
Safe Duplicate Removal Script
Removes duplicates identified in dedupe_mapping.csv
"""

import shutil
from pathlib import Path
import sys

# Directories to remove (confirmed identical)
duplicates_to_remove = [
    "CONTENT_ASSETS/ai-sites/ai-sites/AvaTarArTs/avatararts.org",
    "ai-sites/AvaTarArTs/avatararts.org",
    "CONTENT_ASSETS/ai-sites/AvaTarArTs/avatararts.org"
]

root = Path(".")

print("="*80)
print("Safe Duplicate Removal")
print("="*80)
print(f"\nWill remove {len(duplicates_to_remove)} duplicate directories:")
print("(These are 100% identical to the version in ARCHIVES_BACKUPS)\n")

total_size = 0
for dup in duplicates_to_remove:
    path = root / dup
    if path.exists():
        # Calculate size
        size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
        size_mb = size / (1024**2)
        total_size += size_mb
        print(f"  - {dup} ({size_mb:.2f} MB)")

print(f"\nTotal space to recover: {total_size:.2f} MB ({total_size/1024:.2f} GB)")

# Check if --execute flag is provided
if '--execute' not in sys.argv:
    print("\n" + "="*80)
    print("DRY RUN - No files will be deleted")
    print("Run with --execute to actually remove duplicates")
    print("="*80)
    sys.exit(0)

print("\n" + "="*80)
print("EXECUTING - Removing duplicates...")
print("="*80)

removed = []
errors = []
saved_space = 0

for dup in duplicates_to_remove:
    path = root / dup
    if not path.exists():
        print(f"\n⚠️  {dup} (not found, skipping)")
        continue
    
    try:
        # Calculate size before removal
        size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
        size_mb = size / (1024**2)
        
        print(f"\n🗑️  Removing: {dup}")
        print(f"   Size: {size_mb:.2f} MB")
        
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        
        removed.append(dup)
        saved_space += size_mb
        print(f"   ✅ Removed successfully")
        
    except Exception as e:
        errors.append((dup, str(e)))
        print(f"   ❌ Error: {e}")

print("\n" + "="*80)
print("Summary")
print("="*80)
print(f"✅ Removed: {len(removed)} directories")
print(f"❌ Errors: {len(errors)}")
print(f"💾 Space saved: {saved_space:.2f} MB ({saved_space/1024:.2f} GB)")

if errors:
    print("\nErrors:")
    for path, error in errors:
        print(f"  {path}: {error}")

print("\n✅ Done!")
