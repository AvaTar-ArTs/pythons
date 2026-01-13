#!/usr/bin/env python3
"""
Thorough cleanup script to remove duplicate directory completely
"""
import os
import shutil
from pathlib import Path

def remove_directory_completely(dir_to_remove):
    """Remove a directory completely, even if it has contents"""
    dir_path = Path(dir_to_remove)
    
    if dir_path.exists():
        print(f"Removing directory completely: {dir_to_remove}")
        try:
            shutil.rmtree(dir_path)
            print(f"✅ Successfully removed: {dir_to_remove}")
        except Exception as e:
            print(f"❌ Error removing {dir_to_remove}: {e}")
    else:
        print(f"Directory {dir_to_remove} does not exist")

def main():
    print("AVATARARTS THOROUGH DUPLICATE DIRECTORY REMOVAL")
    print("="*50)
    
    # The duplicate directory that should be removed
    duplicate_dir = "heavenlyhands-complete"
    
    # Remove the directory completely
    remove_directory_completely(duplicate_dir)
    
    # Verify removal
    if not Path(duplicate_dir).exists():
        print(f"\n✅ Directory {duplicate_dir} has been completely removed")
    else:
        print(f"\n❌ Directory {duplicate_dir} still exists")
    
    print(f"\n✅ Thorough cleanup complete!")

if __name__ == "__main__":
    main()