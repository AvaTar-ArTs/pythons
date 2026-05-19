#!/usr/bin/env python3
"""
Version Sprawl Cleaner for ~/pythons/
Intelligently consolidates version variants:
1. Exact duplicates -> keep newest, stage rest
2. Version variants (v1, v2, _final) -> keep latest modified, stage rest
3. Syntax errors -> flagged for review
"""
import os
import re
import shutil
import json
import time
import hashlib
from collections import defaultdict
from pathlib import Path

BASE_DIR = '/Users/steven/pythons'
STAGING_DIR = '/Users/steven/pythons/_VERSION_STAGING'
LOG_FILE = '/Users/steven/pythons_consolidation.log'

def sha256_file(filepath, chunk_size=65536):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    except:
        return None

def normalize_filename(filename):
    """Strip version indicators from filename"""
    name = filename.replace('.py', '')
    patterns = [
        r'_v\d+$', r'_ver\d+$', r'_version\d*$', r'_\d+$',
        r'[-_]?final[-_]?$', r'[-_]?latest[-_]?$', r'[-_]?backup\d*$',
        r'[-_]?old[-_]?\d*$', r'[-_]?copy\d*$', r'[-_]?orig.*$',
        r'[-_]?new\d*$', r'[-_]?updated$', r'[-_]?improved$',
        r'[-_]?fixed$', r'[-_]?v?\d+\.\d+\.\d+$',
        r'[-_]?\d{8}$', r'[-_]?\d{6}$', r'_f\d+$', r'_F\d+$',
        r'[-_]?\d{4}[-_]?\d{2}[-_]?\d{2}$',  # _2026-01-01
        r'[-_]?\d{14}$',  # timestamp like 20250607125040
    ]
    base = name
    for pattern in patterns:
        base = re.sub(pattern, '', base, flags=re.IGNORECASE)
    base = base.rstrip('_- ')
    return base.lower() if base else name.lower()

def check_syntax(filepath):
    """Check for actual syntax errors (not warnings)"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            source = f.read()
        compile(source, filepath, 'exec')
        return None
    except SyntaxError as e:
        return {'line': e.lineno, 'msg': e.msg}
    except:
        return None

def consolidate_sprawl():
    print("=" * 70)
    print("🐍 ~/pythons/ Version Sprawl Consolidator")
    print("=" * 70)
    
    os.makedirs(STAGING_DIR, exist_ok=True)
    
    # Index all files
    all_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '_VERSION_STAGING']
        for fname in files:
            if fname.endswith('.py'):
                fpath = os.path.join(root, fname)
                try:
                    size = os.path.getsize(fpath)
                    mtime = os.path.getmtime(fpath)
                    all_files.append({
                        'path': fpath,
                        'name': fname,
                        'size': size,
                        'mtime': mtime,
                        'base': normalize_filename(fname),
                        'dir': root
                    })
                except:
                    pass
    
    print(f"Total files: {len(all_files):,}")
    
    # Group by (directory, base_name) - only consolidate within same directory
    dir_families = defaultdict(list)
    for f in all_files:
        key = f"{f['dir']}|{f['base']}"
        dir_families[key].append(f)
    
    # Filter to families with multiple files
    sprawl_families = {k: v for k, v in dir_families.items() if len(v) > 1}
    print(f"Families with sprawl (same dir): {len(sprawl_families):,}")
    
    # Stats
    stats = {
        'families_processed': 0,
        'exact_dups_removed': 0,
        'old_versions_staged': 0,
        'syntax_errors_found': 0,
        'files_staged': 0,
        'bytes_saved': 0,
        'errors': 0
    }
    
    syntax_errors = []
    
    print("\nConsolidating version sprawl...")
    
    for key, files in sorted(sprawl_families.items(), key=lambda x: len(x[1]), reverse=True):
        stats['families_processed'] += 1
        
        if stats['families_processed'] % 50 == 0:
            print(f"  Processed {stats['families_processed']}/{len(sprawl_families)} families...")
        
        # Find latest modified file
        files_sorted = sorted(files, key=lambda x: x['mtime'], reverse=True)
        canonical = files_sorted[0]
        
        # Check for syntax errors in all variants
        for f in files:
            err = check_syntax(f['path'])
            if err:
                syntax_errors.append({'path': f['path'], 'name': f['name'], 'error': err})
                stats['syntax_errors_found'] += 1
        
        # Compare with canonical
        canonical_hash = sha256_file(canonical['path'])
        
        for f in files_sorted[1:]:  # Skip the canonical
            try:
                file_hash = sha256_file(f['path'])
                
                if file_hash == canonical_hash:
                    # Exact duplicate - stage it
                    stats['exact_dups_removed'] += 1
                    stats['bytes_saved'] += f['size']
                else:
                    # Different version - stage older ones, keep newest
                    stats['old_versions_staged'] += 1
                    stats['bytes_saved'] += f['size']
                
                # Move to staging
                rel_path = os.path.relpath(f['path'], BASE_DIR)
                staging_path = os.path.join(STAGING_DIR, rel_path)
                os.makedirs(os.path.dirname(staging_path), exist_ok=True)
                
                shutil.move(f['path'], staging_path)
                stats['files_staged'] += 1
                
                action = 'EXACT_DUP' if file_hash == canonical_hash else 'OLD_VERSION'
                with open(LOG_FILE, 'a') as log:
                    log.write(f"{action}|{f['path']}|{staging_path}|{f['size']}|"
                             f"canonical={canonical['name']}|{time.strftime('%Y-%m-%d', time.localtime(f['mtime']))}\n")
                
            except Exception as e:
                stats['errors'] += 1
    
    # Clean empty directories
    print("\nCleaning empty directories...")
    removed = 0
    for root, dirs, files in os.walk(BASE_DIR, topdown=False):
        if '_VERSION_STAGING' in root:
            continue
        if not dirs and not files:
            try:
                os.rmdir(root)
                removed += 1
            except:
                pass
    
    # Print syntax errors
    if syntax_errors:
        print(f"\n{'='*70}")
        print(f"❌ SYNTAX ERRORS ({len(syntax_errors)} files)")
        print(f"{'='*70}")
        for err in syntax_errors[:30]:
            print(f"  {err['name']}: Line {err['error']['line']} - {err['error']['msg']}")
    
    # Results
    print(f"\n{'='*70}")
    print("📊 CONSOLIDATION RESULTS")
    print(f"{'='*70}")
    print(f"Families processed: {stats['families_processed']:,}")
    print(f"Exact duplicates staged: {stats['exact_dups_removed']:,}")
    print(f"Old versions staged: {stats['old_versions_staged']:,}")
    print(f"Total files staged: {stats['files_staged']:,}")
    print(f"Syntax errors found: {stats['syntax_errors_found']}")
    print(f"Space saved: {stats['bytes_saved'] / (1024**2):.1f} MB")
    print(f"Empty dirs removed: {removed}")
    print(f"\nStaging: {STAGING_DIR}")
    print(f"Log: {LOG_FILE}")
    
    # Save syntax errors report
    if syntax_errors:
        error_report = {
            'total_errors': len(syntax_errors),
            'errors': syntax_errors
        }
        error_path = '/Users/steven/pythons_syntax_errors.json'
        with open(error_path, 'w') as f:
            json.dump(error_report, f, indent=2)
        print(f"Syntax error report: {error_path}")
    
    print(f"\n⚠️  Verify pythons/ works, then: rm -rf {STAGING_DIR}")

if __name__ == '__main__':
    consolidate_sprawl()
