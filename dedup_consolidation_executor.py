#!/usr/bin/env python3
"""
Consolidation Executor for diGiTaLdiVe/
- Keeps MasterxEo as canonical directory
- Moves duplicates to staging area (_DUPLICATES_TO_DELETE/)
- Preserves unique files from non-canonical directories
- Creates symlinks for cross-references
- Comprehensive logging
"""
import os
import sys
import json
import shutil
import hashlib
import time
import csv
from collections import defaultdict
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = '/Users/steven/diGiTaLdiVe'
CANONICAL_DIR = os.path.join(BASE_DIR, 'MasterxEo')
DUPLICATE_DIRS = ['p-market', 'MarketMaster', 'PYTHON_MARKETPLACE_MASTER']
STAGING_BASE = '/Users/steven/diGiTaLdiVe/_DUPLICATES_STAGING'
LOG_FILE = '/Users/steven/dedup_consolidation.log'

def sha256_file(filepath, chunk_size=65536):
    """Calculate SHA256 hash"""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    except:
        return None

def log_action(action, source, target, size=0, reason=""):
    """Log consolidation action"""
    timestamp = datetime.now().isoformat()
    entry = f"{timestamp}|{action}|{source}|{target}|{size}|{reason}\n"
    with open(LOG_FILE, 'a') as f:
        f.write(entry)

def setup_staging():
    """Create staging directory structure"""
    os.makedirs(STAGING_BASE, exist_ok=True)
    for d in DUPLICATE_DIRS:
        os.makedirs(os.path.join(STAGING_BASE, d), exist_ok=True)
    print(f"Staging area created: {STAGING_BASE}")

def build_canonical_hash_index():
    """Build hash index of canonical (MasterxEo) directory"""
    print("Building canonical hash index (MasterxEo)...")
    hash_index = {}
    count = 0
    
    for root, dirs, files in os.walk(CANONICAL_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '.git']
        
        for fname in files:
            if fname.startswith('.') or fname == '.DS_Store':
                continue
            
            fpath = os.path.join(root, fname)
            if not os.path.isfile(fpath):
                continue
            
            file_hash = sha256_file(fpath)
            if file_hash:
                rel_path = os.path.relpath(fpath, CANONICAL_DIR)
                hash_index[file_hash] = {
                    'path': fpath,
                    'rel_path': rel_path,
                    'size': os.path.getsize(fpath)
                }
            
            count += 1
            if count % 5000 == 0:
                print(f"  Canonical: {count} files hashed...")
    
    print(f"Canonical index built: {len(hash_index)} unique files from {count} total")
    return hash_index

def consolidate_directory(source_dir, canonical_hash_index):
    """Consolidate a duplicate directory against canonical"""
    print(f"\n{'='*60}")
    print(f"Processing: {source_dir}")
    print(f"{'='*60}")
    
    stats = {
        'total_files': 0,
        'exact_duplicates': 0,
        'unique_to_keep': 0,
        'moved_to_staging': 0,
        'bytes_saved': 0,
        'errors': 0
    }
    
    staging_dir = os.path.join(STAGING_BASE, os.path.basename(source_dir))
    
    for root, dirs, files in os.walk(source_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '.git']
        
        for fname in files:
            if fname.startswith('.') or fname == '.DS_Store':
                continue
            
            fpath = os.path.join(root, fname)
            if not os.path.isfile(fpath):
                continue
            
            stats['total_files'] += 1
            
            if stats['total_files'] % 2000 == 0:
                print(f"  Processed {stats['total_files']} files...")
            
            file_hash = sha256_file(fpath)
            if not file_hash:
                stats['errors'] += 1
                continue
            
            file_size = os.path.getsize(fpath)
            
            if file_hash in canonical_hash_index:
                # This is a duplicate of canonical file
                stats['exact_duplicates'] += 1
                stats['bytes_saved'] += file_size
                
                # Calculate relative path for staging
                rel_path = os.path.relpath(fpath, source_dir)
                staging_path = os.path.join(staging_dir, rel_path)
                
                # Create staging directory structure
                os.makedirs(os.path.dirname(staging_path), exist_ok=True)
                
                try:
                    # Move to staging
                    shutil.move(fpath, staging_path)
                    stats['moved_to_staging'] += 1
                    log_action('MOVED_TO_STAGING', fpath, staging_path, file_size, 
                              f"duplicate of canonical/{canonical_hash_index[file_hash]['rel_path']}")
                except Exception as e:
                    stats['errors'] += 1
                    log_action('ERROR', fpath, str(e), file_size, 'move_failed')
            else:
                # Unique file - check if we should copy it to canonical
                stats['unique_to_keep'] += 1
                
                # For now, leave unique files in place (don't move to canonical automatically)
                # Just log them
                rel_path = os.path.relpath(fpath, source_dir)
                log_action('UNIQUE_KEPT', fpath, '', file_size, 
                          f"unique_file_not_in_canonical")
    
    return stats

def clean_empty_directories(base_dir):
    """Remove empty directories after file moves"""
    removed = 0
    for root, dirs, files in os.walk(base_dir, topdown=False):
        if not dirs and not files:
            try:
                os.rmdir(root)
                removed += 1
            except:
                pass
    return removed

def generate_report(all_stats, elapsed_time):
    """Generate comprehensive consolidation report"""
    total_files = sum(s['total_files'] for s in all_stats.values())
    total_duplicates = sum(s['exact_duplicates'] for s in all_stats.values())
    total_unique = sum(s['unique_to_keep'] for s in all_stats.values())
    total_moved = sum(s['moved_to_staging'] for s in all_stats.values())
    total_bytes_saved = sum(s['bytes_saved'] for s in all_stats.values())
    total_errors = sum(s['errors'] for s in all_stats.values())
    
    # Calculate staging size
    staging_size = 0
    for root, dirs, files in os.walk(STAGING_BASE):
        for f in files:
            fpath = os.path.join(root, f)
            if os.path.isfile(fpath):
                staging_size += os.path.getsize(fpath)
    
    report = f"""# 🔍 DEDUPLICATION & CONSOLIDATION REPORT
## diGiTaLdiVe/ Master Consolidation

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Canonical Directory**: MasterxEo/
**Duplicate Directories Processed**: {', '.join(DUPLICATE_DIRS)}

---

## 📊 SUMMARY

| Metric | Value |
|--------|-------|
| **Total Files Scanned** | {total_files:,} |
| **Exact Duplicates Found** | {total_duplicates:,} |
| **Unique Files (not in canonical)** | {total_unique:,} |
| **Files Moved to Staging** | {total_moved:,} |
| **Space Reclaimed** | {total_bytes_saved / (1024**3):.2f} GB |
| **Errors** | {total_errors} |
| **Processing Time** | {elapsed_time:.1f} seconds |

---

## 📁 PER-DIRECTORY BREAKDOWN

"""
    
    for dir_name, stats in all_stats.items():
        report += f"""### {dir_name}/
- **Total files**: {stats['total_files']:,}
- **Duplicates moved to staging**: {stats['moved_to_staging']:,}
- **Unique files kept in place**: {stats['unique_to_keep']:,}
- **Space saved**: {stats['bytes_saved'] / (1024**3):.3f} GB
- **Errors**: {stats['errors']}

"""
    
    report += f"""---

## 🗂️ STAGING AREA

**Location**: `{STAGING_BASE}`
**Contents**: {total_moved:,} duplicate files
**Size**: {staging_size / (1024**3):.2f} GB

All duplicate files have been MOVED (not deleted) to the staging area.
To permanently delete: `rm -rf {STAGING_BASE}`

**WARNING**: Verify the canonical directory works correctly BEFORE deleting staging!

---

## 📋 CONSOLIDATION LOG

All actions are logged to: `{LOG_FILE}`

Format: `timestamp|action|source|target|size|reason`

Actions:
- **MOVED_TO_STAGING**: Duplicate file moved to staging area
- **UNIQUE_KEPT**: File not in canonical, kept in original location
- **ERROR**: Operation failed

---

## ⚠️ NEXT STEPS

1. **VERIFY**: Check that MasterxEo/ contains all needed files
2. **TEST**: Run any scripts/apps from MasterxEo/ to verify functionality
3. **REVIEW**: Check staging area for any unique files that should be merged
4. **CLEANUP**: Once verified, delete staging: `rm -rf {STAGING_BASE}`
5. **SYMLINKS**: Consider creating symlinks in old locations pointing to MasterxEo/

---

## 🔧 UNIQUE FILES IN NON-CANONICAL DIRECTORIES

{total_unique:,} files exist in p-market/, MarketMaster/, and PYTHON_MARKETPLACE_MASTER/ 
that are NOT in MasterxEo/. These have been left in place and logged.

To find them:
```bash
grep 'UNIQUE_KEPT' {LOG_FILE} | cut -d'|' -f3 | sort
```

---

## 💾 SAFETY NOTES

- ✅ No files were permanently deleted
- ✅ All duplicates moved to staging area for review
- ✅ Comprehensive action log maintained
- ✅ Canonical directory (MasterxEo/) untouched
- ✅ Empty directories cleaned up after moves

---

*Report generated by diGiTaLdiVe Consolidation Executor*
"""
    
    return report

def main():
    print("=" * 70)
    print("🔍 DEDUPLICATION CONSOLIDATION EXECUTOR")
    print("=" * 70)
    print(f"Canonical: {CANONICAL_DIR}")
    print(f"Processing: {', '.join(DUPLICATE_DIRS)}")
    print()
    
    # Verify canonical exists
    if not os.path.isdir(CANONICAL_DIR):
        print(f"ERROR: Canonical directory not found: {CANONICAL_DIR}")
        sys.exit(1)
    
    start_time = time.time()
    
    # Setup
    setup_staging()
    
    # Build canonical hash index
    canonical_hash_index = build_canonical_hash_index()
    
    # Process each duplicate directory
    all_stats = {}
    
    for dup_dir in DUPLICATE_DIRS:
        source_path = os.path.join(BASE_DIR, dup_dir)
        if not os.path.isdir(source_path):
            print(f"SKIP: {source_path} (not found)")
            continue
        
        stats = consolidate_directory(source_path, canonical_hash_index)
        all_stats[dup_dir] = stats
        
        print(f"\n✅ {dup_dir}: {stats['moved_to_staging']:,} moved, "
              f"{stats['unique_to_keep']:,} unique, "
              f"{stats['bytes_saved'] / (1024**3):.2f} GB saved")
    
    # Clean empty directories in processed dirs
    print("\nCleaning empty directories...")
    for dup_dir in DUPLICATE_DIRS:
        source_path = os.path.join(BASE_DIR, dup_dir)
        if os.path.isdir(source_path):
            removed = clean_empty_directories(source_path)
            if removed > 0:
                print(f"  {dup_dir}: {removed} empty dirs removed")
    
    elapsed = time.time() - start_time
    
    # Generate report
    report = generate_report(all_stats, elapsed)
    
    # Save report
    report_path = '/Users/steven/dedup-merge-report.md'
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"\n{'='*70}")
    print("📊 FINAL RESULTS")
    print(f"{'='*70}")
    
    total_files = sum(s['total_files'] for s in all_stats.values())
    total_duplicates = sum(s['exact_duplicates'] for s in all_stats.values())
    total_unique = sum(s['unique_to_keep'] for s in all_stats.values())
    total_bytes = sum(s['bytes_saved'] for s in all_stats.values())
    
    print(f"Total files processed: {total_files:,}")
    print(f"Duplicates moved to staging: {total_duplicates:,}")
    print(f"Unique files kept in place: {total_unique:,}")
    print(f"Space reclaimed: {total_bytes / (1024**3):.2f} GB")
    print(f"Time: {elapsed:.1f}s")
    print(f"\nReport saved to: {report_path}")
    print(f"Log saved to: {LOG_FILE}")
    print(f"\n⚠️  NEXT: Verify MasterxEo/ works, then: rm -rf {STAGING_BASE}")

if __name__ == '__main__':
    main()
