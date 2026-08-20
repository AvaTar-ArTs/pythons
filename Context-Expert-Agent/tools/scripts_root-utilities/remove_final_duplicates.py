#!/usr/bin/env python3
"""
Remove Final Duplicates
Removes the 7 duplicate files identified by comprehensive content-aware analysis.
"""

import csv
from pathlib import Path
from datetime import datetime

def remove_duplicates(mapping_csv: Path, workspace_root: Path):
    """Remove duplicate files based on mapping CSV."""
    
    print("🗑️  REMOVING FINAL DUPLICATES")
    print("=" * 80)
    print()
    
    files_to_delete = []
    
    # Read mapping CSV
    with open(mapping_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            original_path = workspace_root / row['original_path']
            if original_path.exists():
                files_to_delete.append({
                    'path': original_path,
                    'original_path': row['original_path'],
                    'new_path': row['new_path'],
                    'filename': row['filename'],
                    'size_mb': row['size_mb'],
                    'reason': row['keep_reason']
                })
    
    if not files_to_delete:
        print("✅ No duplicate files to remove!")
        return
    
    print(f"Found {len(files_to_delete)} duplicate files to remove:\n")
    
    # Show what will be deleted
    for i, file_info in enumerate(files_to_delete, 1):
        print(f"{i}. {file_info['original_path']}")
        print(f"   Size: {file_info['size_mb']} MB")
        print(f"   Reason: {file_info['reason']}")
        print(f"   Keep: {file_info['new_path']}")
        print()
    
    # Confirm
    print(f"{'='*80}")
    response = input(f"Remove {len(files_to_delete)} duplicate files? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("\n❌ Removal cancelled")
        return
    
    # Delete files
    print(f"\n🗑️  Removing files...\n")
    deleted_count = 0
    errors = []
    
    for file_info in files_to_delete:
        try:
            file_info['path'].unlink()
            deleted_count += 1
            print(f"   ✅ Deleted: {file_info['original_path']}")
        except Exception as e:
            errors.append(f"{file_info['original_path']}: {e}")
            print(f"   ⚠️  Error: {file_info['original_path']} - {e}")
    
    print(f"\n{'='*80}")
    print("✅ REMOVAL COMPLETE")
    print(f"{'='*80}")
    print(f"\n📊 Results:")
    print(f"   Files deleted: {deleted_count}/{len(files_to_delete)}")
    if errors:
        print(f"   Errors: {len(errors)}")
        for error in errors:
            print(f"      - {error}")
    print()

if __name__ == "__main__":
    workspace_root = Path("/Users/steven/AVATARARTS")
    
    # Find latest comprehensive mapping
    mapping_files = sorted(
        workspace_root.glob("COMPREHENSIVE_DUPLICATES_MAPPING_*.csv"),
        reverse=True
    )
    
    if not mapping_files:
        print("❌ No comprehensive duplicates mapping found!")
        print("   Run: python3 comprehensive_content_duplicate_finder.py first")
        exit(1)
    
    mapping_csv = mapping_files[0]
    print(f"📄 Using: {mapping_csv.name}\n")
    
    remove_duplicates(mapping_csv, workspace_root)
