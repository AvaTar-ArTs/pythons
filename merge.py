#!/usr/bin/env python3
"""
Merge and deduplicate files from multiple zip archives into a target directory.
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
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        return extract_dir
    except Exception as e:
        print(f"  ⚠️  Error extracting {zip_path.name}: {e}")
        return None

def merge_and_dedupe(source_dirs, target_dir):
    """Merge files from multiple directories, deduplicating by content hash."""
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Track files by hash
    hash_to_path = defaultdict(list)
    files_processed = 0
    duplicates_skipped = 0
    
    # Process all source directories
    for source_dir in source_dirs:
        if source_dir is None or not source_dir.exists():
            continue
        print(f"\nProcessing {source_dir.name}...")
        for file_path in source_dir.rglob('*'):
            if file_path.is_file():
                files_processed += 1
                try:
                    file_hash = calculate_file_hash(file_path)
                    # Try to preserve relative path structure
                    # If all files are at root, use just filename
                    try:
                        relative_path = file_path.relative_to(source_dir)
                    except ValueError:
                        # If relative path fails, use filename
                        relative_path = Path(file_path.name)
                    hash_to_path[file_hash].append((relative_path, file_path))
                except Exception as e:
                    print(f"  ⚠️  Error processing {file_path}: {e}")
    
    # Copy unique files to target
    print(f"\nCopying unique files to {target_dir}...")
    for file_hash, paths in hash_to_path.items():
        # Use the first occurrence
        source_path = paths[0][1]
        relative_path = paths[0][0]
        
        # Flatten structure - put all files directly in target_dir
        # Use filename if there are conflicts
        target_path = target_dir / relative_path.name
        
        # If file already exists with same hash, skip
        if target_path.exists():
            try:
                existing_hash = calculate_file_hash(target_path)
                if existing_hash == file_hash:
                    duplicates_skipped += 1
                    if len(paths) > 1:
                        duplicates_skipped += len(paths) - 1
                    continue
                else:
                    # Different file with same name - add source identifier
                    target_path = target_dir / f"{relative_path.stem}_{source_path.parent.name}{relative_path.suffix}"
            except Exception:
                pass
        
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copy2(source_path, target_path)
            print(f"  ✓ Copied: {target_path.name}")
        except Exception as e:
            print(f"  ⚠️  Error copying {source_path}: {e}")
        
        # Report duplicates
        if len(paths) > 1:
            duplicates_skipped += len(paths) - 1
    
    return files_processed, duplicates_skipped, len(hash_to_path)

def main():
    if len(sys.argv) < 3:
        print("Usage: merge <target_dir> <zip1> [zip2] [zip3] ...")
        print("  target_dir: Directory to merge files into")
        print("  zip1, zip2, ...: Zip files to extract and merge")
        sys.exit(1)
    
    target_dir = Path(sys.argv[1])
    zip_paths = [Path(z) for z in sys.argv[2:]]
    
    # Validate inputs
    for zip_path in zip_paths:
        if not zip_path.exists():
            print(f"❌ Error: {zip_path} does not exist")
            sys.exit(1)
    
    # Determine target directory - if not specified, use parent of first zip
    if not target_dir.is_absolute() and len(zip_paths) > 0:
        # If relative path, make it relative to first zip's directory
        target_dir = zip_paths[0].parent / target_dir
    elif len(zip_paths) > 0 and not target_dir.exists():
        # If target is in same directory as zips, use that
        if all(z.parent == zip_paths[0].parent for z in zip_paths):
            target_dir = zip_paths[0].parent / target_dir
    
    # Create temporary extraction directory
    temp_dir = target_dir / ".temp_extraction"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Extract all zip files
        extract_dirs = []
        for zip_path in zip_paths:
            extract_dir = extract_zip(zip_path, temp_dir)
            if extract_dir:
                extract_dirs.append(extract_dir)
        
        if not extract_dirs:
            print("❌ Error: No zip files were successfully extracted")
            sys.exit(1)
        
        # Merge and deduplicate
        files_processed, duplicates_skipped, unique_files = merge_and_dedupe(
            extract_dirs, target_dir
        )
        
        print("\n" + "=" * 70)
        print("✅ MERGE AND DEDUPLICATION COMPLETE")
        print("=" * 70)
        print("📊 Summary:")
        print(f"   Zip files processed: {len(zip_paths)}")
        print(f"   Files processed: {files_processed}")
        print(f"   Unique files: {unique_files}")
        print(f"   Duplicates skipped: {duplicates_skipped}")
        print(f"   Target directory: {target_dir}")
        print("=" * 70)
        
    finally:
        # Clean up temporary extraction directory
        if temp_dir.exists():
            print("\nCleaning up temporary files...")
            shutil.rmtree(temp_dir)
            print("✓ Cleanup complete")

if __name__ == "__main__":
    main()
