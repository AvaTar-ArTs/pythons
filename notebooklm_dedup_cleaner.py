#!/usr/bin/env python3
"""
NotebookLM (1) (2) Suffix Duplicate Cleaner
Finds files with (1) or (2) suffixes, compares with originals,
moves duplicates to staging area
"""
import os
import re
import shutil
import hashlib
import time
from pathlib import Path

STAGING_DIR = '/Users/steven/NotebookLM/_DUPLICATES_STAGING'
LOG_FILE = '/Users/steven/notebooklm_dedup.log'

def sha256_file(filepath, chunk_size=65536):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    except:
        return None

def strip_suffix(filename):
    """Remove (1), (2) etc suffix from filename"""
    # Match patterns like file(1).ext, file (1).ext, file(1)_metadata.ext
    pattern = r'(\(1\)|\(2\)|\(3\)|\(4\)|\(5\))'
    cleaned = re.sub(pattern, '', filename)
    # Clean up double spaces or trailing underscores
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    cleaned = re.sub(r'_+', '_', cleaned).strip()
    # Remove trailing space before extension
    cleaned = re.sub(r'\s+(\.\w+)$', r'\1', cleaned)
    return cleaned.strip()

def find_suffix_duplicates(base_dir):
    """Find all files with (1) (2) suffixes"""
    suffix_files = []
    
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '_DUPLICATES_STAGING']
        
        for fname in files:
            if '(1)' in fname or '(2)' in fname or '(3)' in fname:
                fpath = os.path.join(root, fname)
                suffix_files.append({
                    'path': fpath,
                    'name': fname,
                    'clean_name': strip_suffix(fname),
                    'dir': root
                })
    
    return suffix_files

def main():
    base_dir = '/Users/steven/NotebookLM'
    
    print("=" * 70)
    print("📓 NotebookLM (1)/(2) Suffix Duplicate Cleaner")
    print("=" * 70)
    
    os.makedirs(STAGING_DIR, exist_ok=True)
    
    # Find all suffix files
    print("\nFinding suffix duplicates...")
    suffix_files = find_suffix_duplicates(base_dir)
    print(f"Found {len(suffix_files)} files with suffixes")
    
    # Build lookup of original files
    print("Building original file index...")
    originals = {}
    count = 0
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '_DUPLICATES_STAGING']
        for fname in files:
            if '(1)' not in fname and '(2)' not in fname and '(3)' not in fname:
                fpath = os.path.join(root, fname)
                key = f"{root}|{fname}"
                originals[key] = fpath
        count += len(files)
        if count % 1000 == 0:
            print(f"  Indexed {count} files...")
    
    print(f"Total originals indexed: {len(originals):,}")
    
    # Process suffix files
    stats = {
        'total_suffix_files': len(suffix_files),
        'exact_duplicates': 0,
        'unique_different': 0,
        'no_original_found': 0,
        'moved_to_staging': 0,
        'errors': 0,
        'bytes_saved': 0
    }
    
    print("\nProcessing suffix duplicates...")
    for i, sf in enumerate(suffix_files):
        if i % 50 == 0:
            print(f"  Processing {i}/{len(suffix_files)}...")
        
        suffix_path = sf['path']
        clean_name = sf['clean_name']
        parent_dir = sf['dir']
        
        try:
            suffix_hash = sha256_file(suffix_path)
            suffix_size = os.path.getsize(suffix_path)
        except:
            stats['errors'] += 1
            continue
        
        # Look for original in same directory
        original_path = os.path.join(parent_dir, clean_name)
        
        if os.path.exists(original_path):
            # Compare hashes
            original_hash = sha256_file(original_path)
            
            if suffix_hash == original_hash:
                # Exact duplicate - move to staging
                stats['exact_duplicates'] += 1
                stats['bytes_saved'] += suffix_size
                
                rel_path = os.path.relpath(suffix_path, base_dir)
                staging_path = os.path.join(STAGING_DIR, rel_path)
                os.makedirs(os.path.dirname(staging_path), exist_ok=True)
                
                try:
                    shutil.move(suffix_path, staging_path)
                    stats['moved_to_staging'] += 1
                    
                    with open(LOG_FILE, 'a') as f:
                        f.write(f"MOVED|{suffix_path}|{staging_path}|{suffix_size}|exact_duplicate_of_{clean_name}\n")
                except Exception as e:
                    stats['errors'] += 1
            else:
                # Different content - keep both but log
                stats['unique_different'] += 1
                with open(LOG_FILE, 'a') as f:
                    f.write(f"KEPT|{suffix_path}|{suffix_size}|different_content_from_{clean_name}\n")
        else:
            # No original found in same directory - search broader
            stats['no_original_found'] += 1
            # Still move to staging since it has a suffix
            rel_path = os.path.relpath(suffix_path, base_dir)
            staging_path = os.path.join(STAGING_DIR, rel_path)
            os.makedirs(os.path.dirname(staging_path), exist_ok=True)
            
            try:
                shutil.move(suffix_path, staging_path)
                stats['moved_to_staging'] += 1
                stats['bytes_saved'] += suffix_size
                
                with open(LOG_FILE, 'a') as f:
                    f.write(f"MOVED_NO_ORIGINAL|{suffix_path}|{staging_path}|{suffix_size}|no_original_found_{clean_name}\n")
            except Exception as e:
                stats['errors'] += 1
    
    # Clean empty dirs
    print("\nCleaning empty directories...")
    removed = 0
    for root, dirs, files in os.walk(base_dir, topdown=False):
        if '_DUPLICATES_STAGING' in root:
            continue
        if not dirs and not files:
            try:
                os.rmdir(root)
                removed += 1
            except:
                pass
    
    print(f"\n{'='*70}")
    print("📊 RESULTS")
    print(f"{'='*70}")
    print(f"Total suffix files found: {stats['total_suffix_files']}")
    print(f"Exact duplicates moved: {stats['moved_to_staging']}")
    print(f"  - With original in same dir: {stats['exact_duplicates']}")
    print(f"  - No original found: {stats['no_original_found']}")
    print(f"Unique different content kept: {stats['unique_different']}")
    print(f"Errors: {stats['errors']}")
    print(f"Space saved: {stats['bytes_saved'] / (1024**2):.1f} MB")
    print(f"Empty dirs removed: {removed}")
    print(f"\nStaging: {STAGING_DIR}")
    print(f"Log: {LOG_FILE}")
    print(f"\n⚠️  Verify NotebookLM/ works, then: rm -rf {STAGING_DIR}")

if __name__ == '__main__':
    main()
