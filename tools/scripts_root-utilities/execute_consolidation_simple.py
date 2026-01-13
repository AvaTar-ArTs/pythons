#!/usr/bin/env python3
"""
Execute Consolidation - Simple Version
Deletes duplicate files based on consolidation mapping CSV.
No backup needed - folder-folder-folder type duplicates.
"""

import csv
from pathlib import Path
from datetime import datetime

def execute_consolidation(mapping_csv: Path, workspace_root: Path, dry_run: bool = False, limit: int = None):
    """Execute consolidation by deleting duplicate files."""
    
    print(f"📄 Reading mapping CSV: {mapping_csv.name}")
    
    files_to_delete = []
    
    with open(mapping_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            original_path = workspace_root / row['original_path']
            files_to_delete.append({
                'original_path': row['original_path'],
                'full_path': original_path,
                'new_path': row['new_path']
            })
    
    if limit:
        files_to_delete = files_to_delete[:limit]
        print(f"⚠️  Limited to first {limit} files for testing")
    
    print(f"   Found {len(files_to_delete):,} files to delete\n")
    
    mode = "DRY RUN" if dry_run else "EXECUTING"
    print(f"{'='*80}")
    print(f"🗑️  {mode} CONSOLIDATION")
    print(f"{'='*80}\n")
    
    deleted_count = 0
    not_found_count = 0
    error_count = 0
    
    for i, file_info in enumerate(files_to_delete, 1):
        file_path = file_info['full_path']
        
        if not file_path.exists():
            not_found_count += 1
            continue
        
        if dry_run:
            if i <= 20:
                print(f"   Would delete: {file_info['original_path']}")
            elif i == 21:
                print(f"   ... and {len(files_to_delete) - 20} more files")
        else:
            try:
                file_path.unlink()
                deleted_count += 1
                
                if deleted_count % 1000 == 0:
                    print(f"   Deleted {deleted_count:,}/{len(files_to_delete):,} files...")
            
            except Exception as e:
                error_count += 1
                if error_count <= 10:
                    print(f"   ⚠️  Error deleting {file_info['original_path']}: {e}")
    
    if not dry_run:
        print(f"\n✅ Consolidation complete!")
        print(f"   Deleted: {deleted_count:,} files")
        if not_found_count > 0:
            print(f"   Not found: {not_found_count:,} files")
        if error_count > 0:
            print(f"   Errors: {error_count:,} files")
    
    return deleted_count, not_found_count, error_count

def main():
    """Main execution."""
    print("=" * 80)
    print("SIMPLE CONSOLIDATION EXECUTOR")
    print("=" * 80)
    print()
    
    workspace_root = Path("/Users/steven/AVATARARTS")
    
    # Find latest mapping CSV
    mapping_files = sorted(
        workspace_root.glob("CONSOLIDATION_MAPPING_*.csv"),
        reverse=True
    )
    
    if not mapping_files:
        print("❌ No consolidation mapping CSV found!")
        print("   Run: python3 generate_simple_mapping.py first")
        return
    
    mapping_csv = mapping_files[0]
    print(f"📄 Using: {mapping_csv.name}\n")
    
    # Dry run first
    print("STEP 1: DRY RUN (first 100 files)")
    print("-" * 80)
    execute_consolidation(mapping_csv, workspace_root, dry_run=True, limit=100)
    
    # Confirm
    print(f"\n{'='*80}")
    response = input(f"\nProceed with full consolidation? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("\n❌ Consolidation cancelled")
        return
    
    # Execute
    print(f"\n{'='*80}")
    print("STEP 2: EXECUTING CONSOLIDATION")
    print("-" * 80)
    
    deleted, not_found, errors = execute_consolidation(
        mapping_csv, 
        workspace_root, 
        dry_run=False
    )
    
    print(f"\n{'='*80}")
    print("✅ CONSOLIDATION COMPLETE")
    print(f"{'='*80}")
    print(f"\n📊 Results:")
    print(f"   Files deleted: {deleted:,}")
    print(f"   Files not found: {not_found:,}")
    print(f"   Errors: {errors:,}")
    print()

if __name__ == "__main__":
    main()
