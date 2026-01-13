#!/usr/bin/env python3
"""
Auto Cleanup Extra Files
Automatically removes extra files identified by cleanup analysis.
"""

import csv
from pathlib import Path

def cleanup_extra_files(cleanup_csv: Path, workspace_root: Path, dry_run: bool = True):
    """Clean up extra files."""
    
    print("🗑️  CLEANUP EXTRA FILES")
    print("=" * 80)
    print()
    
    mode = "DRY RUN" if dry_run else "EXECUTING"
    print(f"Mode: {mode}\n")
    
    files_to_delete = []
    
    with open(cleanup_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            file_path = workspace_root / row['path']
            if file_path.exists():
                files_to_delete.append({
                    'path': file_path,
                    'category': row['category'],
                    'size_mb': float(row['size_mb']),
                    'reason': row['reason']
                })
    
    print(f"Found {len(files_to_delete)} files to clean up")
    print(f"Total size: {sum(f['size_mb'] for f in files_to_delete):.2f} MB\n")
    
    deleted_count = 0
    deleted_size = 0
    
    for i, file_info in enumerate(files_to_delete, 1):
        file_path = file_info['path']
        
        if dry_run:
            if i <= 20:
                print(f"   Would delete: {file_info['path'].name} ({file_info['size_mb']:.2f} MB) - {file_info['reason']}")
            elif i == 21:
                print(f"   ... and {len(files_to_delete) - 20} more files")
        else:
            try:
                size = file_path.stat().st_size
                file_path.unlink()
                deleted_count += 1
                deleted_size += size
                
                if deleted_count % 10 == 0:
                    print(f"   Deleted {deleted_count}/{len(files_to_delete)}...")
            except Exception as e:
                print(f"   ⚠️  Error deleting {file_path.name}: {e}")
    
    if not dry_run:
        print(f"\n✅ Cleanup complete!")
        print(f"   Deleted: {deleted_count} files")
        print(f"   Freed: {deleted_size / (1024 * 1024):.2f} MB")
    
    return deleted_count, deleted_size

def main():
    """Main execution."""
    workspace_root = Path("/Users/steven/AVATARARTS")
    
    # Find latest cleanup CSV
    cleanup_files = sorted(
        workspace_root.glob("CLEANUP_EXTRA_FILES_*.csv"),
        reverse=True
    )
    
    if not cleanup_files:
        print("❌ No cleanup CSV found!")
        print("   Run: python3 cleanup_extra_files.py first")
        return
    
    cleanup_csv = cleanup_files[0]
    print(f"📄 Using: {cleanup_csv.name}\n")
    
    # Dry run
    print("STEP 1: DRY RUN")
    print("-" * 80)
    cleanup_extra_files(cleanup_csv, workspace_root, dry_run=True)
    
    # Confirm
    print(f"\n{'='*80}")
    response = input(f"\nProceed with cleanup? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("\n❌ Cleanup cancelled")
        return
    
    # Execute
    print(f"\n{'='*80}")
    print("STEP 2: EXECUTING CLEANUP")
    print("-" * 80)
    deleted, freed = cleanup_extra_files(cleanup_csv, workspace_root, dry_run=False)
    
    print(f"\n{'='*80}")
    print("✅ CLEANUP COMPLETE")
    print(f"{'='*80}")
    print(f"\n📊 Results:")
    print(f"   Files deleted: {deleted}")
    print(f"   Space freed: {freed / (1024 * 1024):.2f} MB")
    print()

if __name__ == "__main__":
    main()
