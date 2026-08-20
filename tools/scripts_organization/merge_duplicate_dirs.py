#!/usr/bin/env python3
"""
Script to help merge duplicate directories
"""
import os
import shutil
from pathlib import Path

def merge_directories(src_dir, dest_dir, dry_run=True):
    """Merge contents of src_dir into dest_dir, handling conflicts"""
    print(f"{'DRY RUN - ' if dry_run else ''}Merging {src_dir} -> {dest_dir}")
    
    src_path = Path(src_dir)
    dest_path = Path(dest_dir)
    
    if not src_path.exists() or not dest_path.exists():
        print(f"  Error: One or both directories don't exist")
        return False
    
    conflicts = []
    moved_count = 0
    
    for src_item in src_path.rglob('*'):
        if src_item.is_file():
            # Calculate relative path from source directory
            rel_path = src_item.relative_to(src_path)
            dest_item = dest_path / rel_path
            
            # Check if destination file already exists
            if dest_item.exists():
                conflicts.append((src_item, dest_item))
                print(f"  CONFLICT: {rel_path} exists in both directories")
            else:
                # Create parent directories if they don't exist
                dest_item.parent.mkdir(parents=True, exist_ok=True)
                
                if not dry_run:
                    # Move the file
                    shutil.move(str(src_item), str(dest_item))
                    print(f"  Moved: {rel_path}")
                else:
                    print(f"  Would move: {rel_path}")
                
                moved_count += 1
        elif src_item.is_dir():
            # For directories, just ensure they exist in destination
            rel_path = src_item.relative_to(src_path)
            dest_item = dest_path / rel_path
            if not dry_run:
                dest_item.mkdir(parents=True, exist_ok=True)
    
    print(f"  Summary: {moved_count} items to move")
    if conflicts:
        print(f"  Conflicts: {len(conflicts)} files exist in both directories")
    
    return True

def analyze_duplicate_directories():
    """Analyze the duplicate directories we found"""
    print("🔍 ANALYZING DUPLICATE DIRECTORIES")
    print("="*50)
    
    # The duplicate directories we found
    dir1 = "heavenlyHands"
    dir2 = "heavenlyhands-complete"
    
    dir1_path = Path(dir1)
    dir2_path = Path(dir2)
    
    if dir1_path.exists() and dir2_path.exists():
        # Get sizes
        size1 = sum(f.stat().st_size for f in dir1_path.rglob('*') if f.is_file())
        size2 = sum(f.stat().st_size for f in dir2_path.rglob('*') if f.is_file())
        
        print(f"Directory 1: {dir1} ({size1/1024/1024:.2f} MB)")
        print(f"Directory 2: {dir2} ({size2/1024/1024:.2f} MB)")
        
        # Count files
        files1 = len([f for f in dir1_path.rglob('*') if f.is_file()])
        files2 = len([f for f in dir2_path.rglob('*') if f.is_file()])
        
        print(f"  Files in {dir1}: {files1}")
        print(f"  Files in {dir2}: {files2}")
        
        # Check for common file patterns
        files1_set = {f.name for f in dir1_path.rglob('*') if f.is_file()}
        files2_set = {f.name for f in dir2_path.rglob('*') if f.is_file()}
        
        common_files = files1_set.intersection(files2_set)
        if common_files:
            print(f"  Common file names: {len(common_files)}")
            for f in list(common_files)[:5]:  # Show first 5
                print(f"    - {f}")
            if len(common_files) > 5:
                print(f"    ... and {len(common_files) - 5} more")
        else:
            print("  No common file names found")
        
        print(f"\n💡 RECOMMENDATION:")
        print(f"  Since {dir1} is significantly larger ({size1/1024/1024:.2f} MB vs {size2/1024/1024:.2f} MB),")
        print(f"  consider merging {dir2} into {dir1}")
        
        return dir1, dir2
    else:
        print("One or both directories don't exist")
        return None, None

def main():
    print("AVATARARTS DUPLICATE DIRECTORY MERGE ANALYSIS")
    print("="*70)
    
    dir1, dir2 = analyze_duplicate_directories()
    
    if dir1 and dir2:
        print(f"\n📋 MERGE OPTIONS:")
        print(f"  Option 1: Merge {dir2} into {dir1}")
        print(f"  Option 2: Merge {dir1} into {dir2}")
        print(f"  Option 3: Create new combined directory")
        
        print(f"\n🧪 DRY RUN - Testing merge of {dir2} into {dir1}:")
        merge_directories(dir2, dir1, dry_run=True)
        
        print(f"\n⚠️  IMPORTANT:")
        print(f"  • Always backup before merging directories")
        print(f"  • Review conflicts before proceeding")
        print(f"  • Consider if you want to keep both directories")
        
        print(f"\n🎯 NEXT STEPS:")
        print(f"  1. Review the conflicts identified above")
        print(f"  2. Decide which directory to keep as primary")
        print(f"  3. Manually resolve any conflicts if needed")
        print(f"  4. Run the merge with dry_run=False when ready")
    
    print(f"\n✅ Analysis complete!")

if __name__ == "__main__":
    main()