#!/usr/bin/env python3
"""
Simple duplicate file detector for the current directory
"""
import os
import hashlib
from pathlib import Path

def get_file_hash(filepath):
    """Calculate SHA256 hash of a file"""
    hash_sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Read file in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception:
        return None

def find_duplicates(directory):
    """Find duplicate files in a directory"""
    print(f"Scanning {directory} for duplicates...")
    
    hash_dict = {}
    file_count = 0
    
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories and common cache directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.git', '.svn']]
        
        for file in files:
            filepath = Path(root) / file
            if filepath.is_file():
                file_hash = get_file_hash(filepath)
                if file_hash:
                    if file_hash in hash_dict:
                        hash_dict[file_hash].append(str(filepath))
                    else:
                        hash_dict[file_hash] = [str(filepath)]
                    file_count += 1
                    
                    if file_count % 100 == 0:
                        print(f"Processed {file_count} files...")
    
    print(f"Processed {file_count} files total.")
    
    # Find duplicates (hashes with more than one file)
    duplicates = {hash_val: paths for hash_val, paths in hash_dict.items() if len(paths) > 1}
    
    return duplicates

def main():
    directory = Path.cwd()  # Current directory
    print(f"Looking for duplicates in: {directory}")
    print("="*60)
    
    duplicates = find_duplicates(directory)
    
    if duplicates:
        print(f"\nFound {len(duplicates)} sets of duplicate files:\n")
        total_dupes = 0
        for hash_val, file_paths in duplicates.items():
            print(f"Duplicate set ({len(file_paths)} files):")
            for path in file_paths:
                file_size = Path(path).stat().st_size
                print(f"  - {path} ({file_size} bytes)")
            print()
            total_dupes += len(file_paths) - 1  # Count actual duplicate files (not the original)
        
        print(f"Total duplicate files: {total_dupes}")
    else:
        print("\nNo duplicates found!")

if __name__ == "__main__":
    main()