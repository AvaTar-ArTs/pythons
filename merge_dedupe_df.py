#!/usr/bin/env python3
"""
Merge and deduplicate files from two zip archives into a target directory.
"""
import zipfile
import shutil
from pathlib import Path
import hashlib
import sys
from collections import defaultdict

def calculate_file_hash(file_path):
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def extract_zip(zip_path, extract_to):
    """Extract zip file to a temporary directory."""
    extract_dir = extract_to / f"temp_{zip_path.stem}"
    extract_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Extracting {zip_path.name}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    
    return extract_dir

def merge_and_dedupe(source_dir1, source_dir2, target_dir):
    """Merge files from two directories, deduplicating by content hash."""
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Track files by hash
    hash_to_path = defaultdict(list)
    files_processed = 0
    duplicates_skipped = 0
    
    # Process first directory
    print(f"\nProcessing {source_dir1}...")
    for file_path in source_dir1.rglob('*'):
        if file_path.is_file():
            files_processed += 1
            try:
                file_hash = calculate_file_hash(file_path)
                relative_path = file_path.relative_to(source_dir1)
                hash_to_path[file_hash].append((relative_path, file_path))
            except Exception as e:
                print(f"  ⚠️  Error processing {file_path}: {e}")
    
    # Process second directory
    print(f"\nProcessing {source_dir2}...")
    for file_path in source_dir2.rglob('*'):
        if file_path.is_file():
            files_processed += 1
            try:
                file_hash = calculate_file_hash(file_path)
                relative_path = file_path.relative_to(source_dir2)
                hash_to_path[file_hash].append((relative_path, file_path))
            except Exception as e:
                print(f"  ⚠️  Error processing {file_path}: {e}")
    
    # Copy unique files to target
    print(f"\nCopying unique files to {target_dir}...")
    for file_hash, paths in hash_to_path.items():
        # Use the first occurrence (prefer from first zip if both exist)
        source_path = paths[0][1]
        relative_path = paths[0][0]
        
        target_path = target_dir / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Only copy if target doesn't exist or is different
        if not target_path.exists() or calculate_file_hash(target_path) != file_hash:
            shutil.copy2(source_path, target_path)
            print(f"  ✓ Copied: {relative_path}")
        else:
            duplicates_skipped += 1
            print(f"  ⊘ Skipped (already exists): {relative_path}")
        
        # Report duplicates
        if len(paths) > 1:
            duplicates_skipped += len(paths) - 1
            print(f"  ⊘ Skipped {len(paths) - 1} duplicate(s) of: {relative_path}")
    
    return files_processed, duplicates_skipped, len(hash_to_path)

def main():
    if len(sys.argv) != 4:
        print("Usage: merge dedupe df <target_dir> <zip1> <zip2>")
        print("  target_dir: Directory to merge files into")
        print("  zip1: First zip file to extract and merge")
        print("  zip2: Second zip file to extract and merge")
        sys.exit(1)
    
    target_dir = Path(sys.argv[1])
    zip1_path = Path(sys.argv[2])
    zip2_path = Path(sys.argv[3])
    
    # Validate inputs
    if not zip1_path.exists():
        print(f"❌ Error: {zip1_path} does not exist")
        sys.exit(1)
    
    if not zip2_path.exists():
        print(f"❌ Error: {zip2_path} does not exist")
        sys.exit(1)
    
    # Create temporary extraction directory
    temp_dir = target_dir / ".temp_extraction"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Extract both zip files
        extract1 = extract_zip(zip1_path, temp_dir)
        extract2 = extract_zip(zip2_path, temp_dir)
        
        # Merge and deduplicate
        files_processed, duplicates_skipped, unique_files = merge_and_dedupe(
            extract1, extract2, target_dir
        )
        
        print("\n" + "=" * 70)
        print("✅ MERGE AND DEDUPLICATION COMPLETE")
        print("=" * 70)
        print(f"📊 Summary:")
        print(f"   Files processed: {files_processed}")
        print(f"   Unique files: {unique_files}")
        print(f"   Duplicates skipped: {duplicates_skipped}")
        print(f"   Target directory: {target_dir}")
        print("=" * 70)
        
    finally:
        # Clean up temporary extraction directory
        if temp_dir.exists():
            print(f"\nCleaning up temporary files...")
            shutil.rmtree(temp_dir)
            print("✓ Cleanup complete")

if __name__ == "__main__":
    main()
