#!/usr/bin/env python3
"""
Execute Consolidation - Auto Version
Deletes duplicate files based on consolidation mapping CSV.
Runs automatically without prompts.
"""

import csv
from pathlib import Path
from datetime import datetime

def execute_consolidation(mapping_csv: Path, workspace_root: Path, limit: int = None):
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
        print(f"⚠️  Limited to first {limit} files")
    else:
        print(f"   Processing all {len(files_to_delete):,} files")
    
    print(f"\n{'='*80}")
    print(f"🗑️  EXECUTING CONSOLIDATION")
    print(f"{'='*80}\n")
    
    deleted_count = 0
    not_found_count = 0
    error_count = 0
    
    for i, file_info in enumerate(files_to_delete, 1):
        file_path = file_info['full_path']
        
        if not file_path.exists():
            not_found_count += 1
            continue
        
        try:
            file_path.unlink()
            deleted_count += 1
            
            if deleted_count % 1000 == 0:
                print(f"   Deleted {deleted_count:,}/{len(files_to_delete):,} files...")
        
        except Exception as e:
            error_count += 1
            if error_count <= 10:
                print(f"   ⚠️  Error deleting {file_info['original_path']}: {e}")
    
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
    print("SIMPLE CONSOLIDATION EXECUTOR - AUTO MODE")
    print("=" * 80)
    print()
    
    workspace_root = Path("/Users/steven/AVATARARTS")
    
    # Find latest mapping CSV (prefer COMPLETE_DUPLICATES_MAPPING.csv)
    complete_mapping = workspace_root / "COMPLETE_DUPLICATES_MAPPING.csv"
    if complete_mapping.exists():
        mapping_files = [complete_mapping]
    else:
        mapping_files = sorted(
            workspace_root.glob("CONSOLIDATION_MAPPING_*.csv"),
            reverse=True
        )
    
    if not mapping_files:
        print("❌ No consolidation mapping CSV found!")
        return
    
    mapping_csv = mapping_files[0]
    print(f"📄 Using: {mapping_csv.name}\n")
    
    # Execute (start with 10000 files for safety, remove limit for full run)
    print("Starting consolidation...")
    deleted, not_found, errors = execute_consolidation(
        mapping_csv, 
        workspace_root, 
        limit=None  # Set to a number like 10000 for testing, None for full run
    )
    
    print(f"\n{'='*80}")
    print("✅ CONSOLIDATION COMPLETE")
    print(f"{'='*80}")
    print(f"\n📊 Final Results:")
    print(f"   Files deleted: {deleted:,}")
    print(f"   Files not found: {not_found:,}")
    print(f"   Errors: {errors:,}")
    print()

if __name__ == "__main__":
    main()
