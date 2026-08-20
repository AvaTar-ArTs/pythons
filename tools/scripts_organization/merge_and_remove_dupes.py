#!/usr/bin/env python3
"""
Script to merge duplicate directories and remove duplicates
"""
import os
import shutil
from pathlib import Path

def merge_directories(src_dir, dest_dir):
    """Merge contents of src_dir into dest_dir, handling conflicts"""
    print(f"Merging {src_dir} -> {dest_dir}")
    
    src_path = Path(src_dir)
    dest_path = Path(dest_dir)
    
    if not src_path.exists() or not dest_path.exists():
        print(f"  Error: One or both directories don't exist")
        return False
    
    conflicts = []
    moved_count = 0
    
    # Create a list of items to move first to avoid issues with modifying directory during iteration
    items_to_move = []
    for src_item in src_path.rglob('*'):
        if src_item.is_file():
            items_to_move.append(src_item)
    
    for src_item in items_to_move:
        # Calculate relative path from source directory
        rel_path = src_item.relative_to(src_path)
        dest_item = dest_path / rel_path
        
        # Check if destination file already exists
        if dest_item.exists():
            # Skip .DS_Store files as they're system files
            if rel_path.name == '.DS_Store':
                print(f"  Skipping duplicate .DS_Store: {rel_path}")
                continue
            else:
                conflicts.append((src_item, dest_item))
                print(f"  CONFLICT: {rel_path} exists in both directories")
        else:
            # Create parent directories if they don't exist
            dest_item.parent.mkdir(parents=True, exist_ok=True)
            
            # Move the file
            shutil.move(str(src_item), str(dest_item))
            print(f"  Moved: {rel_path}")
            
            moved_count += 1
    
    print(f"  Summary: {moved_count} items moved")
    if conflicts:
        print(f"  Conflicts not resolved: {len(conflicts)} files")
    
    return True

def remove_duplicate_directory(dir_to_remove):
    """Remove the now-empty or nearly empty duplicate directory"""
    dir_path = Path(dir_to_remove)
    
    if dir_path.exists():
        # Check if directory is empty or nearly empty
        items = list(dir_path.rglob('*'))
        non_ds_store_items = [item for item in items if item.name != '.DS_Store']
        
        if len(non_ds_store_items) == 0:
            # Directory is empty (or only has .DS_Store), safe to remove
            shutil.rmtree(dir_path)
            print(f"  Removed empty directory: {dir_to_remove}")
        else:
            print(f"  Directory {dir_to_remove} still has {len(non_ds_store_items)} items, not removing")
            for item in non_ds_store_items[:5]:  # Show first 5 items
                print(f"    - {item}")
            if len(non_ds_store_items) > 5:
                print(f"    ... and {len(non_ds_store_items) - 5} more")
    else:
        print(f"  Directory {dir_to_remove} does not exist")

def main():
    print("AVATARARTS MERGE DUPLICATE DIRECTORIES")
    print("="*50)
    
    # The duplicate directories we identified
    primary_dir = "heavenlyHands"
    duplicate_dir = "heavenlyhands-complete"
    
    primary_path = Path(primary_dir)
    duplicate_path = Path(duplicate_dir)
    
    if duplicate_path.exists() and primary_path.exists():
        print(f"Starting merge of {duplicate_dir} into {primary_dir}")
        
        # Perform the merge
        success = merge_directories(duplicate_dir, primary_dir)
        
        if success:
            # After successful merge, remove the now-empty duplicate directory
            print(f"\nRemoving duplicate directory: {duplicate_dir}")
            remove_duplicate_directory(duplicate_dir)
            
            # Verify the merge
            primary_size = sum(f.stat().st_size for f in primary_path.rglob('*') if f.is_file())
            print(f"\n✅ Merge completed!")
            print(f"Primary directory ({primary_dir}) size: {primary_size/1024/1024:.2f} MB")
            print(f"Duplicate directory ({duplicate_dir}) removed")
        else:
            print("❌ Merge failed")
    else:
        print(f"One or both directories don't exist: {primary_dir}, {duplicate_dir}")
    
    print(f"\n✅ Operation complete!")

if __name__ == "__main__":
    main()