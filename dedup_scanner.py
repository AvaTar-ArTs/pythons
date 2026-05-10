#!/usr/bin/env python3
"""
Comprehensive SHA256-based deduplication scanner
Scans multiple directories, finds exact and near-duplicates
"""
import os
import sys
import hashlib
import csv
import json
import time
from collections import defaultdict
from pathlib import Path

def sha256_file(filepath, chunk_size=65536):
    """Calculate SHA256 hash of a file"""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (PermissionError, OSError):
        return None

def scan_directory(base_dir, extensions=None):
    """Scan directory and return file info dict"""
    files = {}
    base = Path(base_dir)
    count = 0
    
    for root, dirs, filenames in os.walk(base):
        # Skip hidden dirs and .git
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '.git']
        
        for fname in filenames:
            if fname.startswith('.') or fname == '.DS_Store':
                continue
            
            fpath = os.path.join(root, fname)
            if not os.path.isfile(fpath):
                continue
            
            try:
                size = os.path.getsize(fpath)
            except OSError:
                continue
                
            # Get relative path from base
            rel_path = os.path.relpath(fpath, base_dir)
            
            files[rel_path] = {
                'abs_path': fpath,
                'size': size,
                'rel_path': rel_path,
                'name': fname,
                'ext': Path(fname).suffix.lower(),
            }
            count += 1
            if count % 1000 == 0:
                print(f"  Scanned {count} files...", file=sys.stderr)
    
    return files

def build_hash_index(files_dict):
    """Build SHA256 hash index for all files"""
    hash_index = defaultdict(list)
    
    for i, (rel_path, info) in enumerate(files_dict.items()):
        if i % 1000 == 0:
            print(f"  Hashing {i}/{len(files_dict)} files...", file=sys.stderr)
        
        file_hash = sha256_file(info['abs_path'])
        if file_hash:
            info['hash'] = file_hash
            hash_index[file_hash].append(rel_path)
    
    return hash_index

def find_duplicates(hash_index):
    """Find files with identical hashes"""
    duplicates = {}
    for file_hash, paths in hash_index.items():
        if len(paths) > 1:
            duplicates[file_hash] = paths
    return duplicates

def analyze_cross_directory(hash_index, dir_list):
    """Analyze which duplicates span multiple directories"""
    cross_dir_dups = []
    
    for file_hash, paths in hash_index.items():
        dirs_found = set()
        for p in paths:
            for d in dir_list:
                if p.startswith(d + '/') or p.startswith(d + os.sep):
                    dirs_found.add(d)
        
        if len(dirs_found) > 1:
            # This file exists in multiple directories
            first_file = None
            for p in paths:
                for d in dir_list:
                    if p.startswith(d + '/') or p.startswith(d + os.sep):
                        full_path = os.path.join('/Users/steven/diGiTaLdiVe', d, p[len(d)+1:])
                        if first_file is None:
                            first_file = full_path
                        break
            
            total_size = 0
            for p in paths:
                try:
                    # Find the actual file
                    for d in dir_list:
                        if p.startswith(d + '/') or p.startswith(d + os.sep):
                            full_path = os.path.join('/Users/steven/diGiTaLdiVe', d, p[len(d)+1:])
                            if os.path.exists(full_path):
                                total_size += os.path.getsize(full_path)
                            break
                except:
                    pass
            
            cross_dir_dups.append({
                'hash': file_hash,
                'paths': paths,
                'dirs': list(dirs_found),
                'count': len(paths),
                'wasted_space': total_size  # approximate
            })
    
    return cross_dir_dups

def main():
    base_dir = '/Users/steven/diGiTaLdiVe'
    target_dirs = ['p-market', 'MarketMaster', 'MasterxEo', 'PYTHON_MARKETPLACE_MASTER']
    
    print("=" * 80)
    print("DEDUPLICATION SCANNER - diGiTaLdiVe/")
    print("=" * 80)
    
    all_files = {}
    total_start = time.time()
    
    for target in target_dirs:
        target_path = os.path.join(base_dir, target)
        if not os.path.isdir(target_path):
            print(f"SKIP: {target} (not found)")
            continue
        
        print(f"\nScanning: {target}/")
        files = scan_directory(target_path)
        print(f"  Found {len(files)} files")
        
        # Add directory prefix to keys
        for rel_path, info in files.items():
            prefixed_key = f"{target}/{rel_path}"
            info['source_dir'] = target
            all_files[prefixed_key] = info
    
    print(f"\nTotal files indexed: {len(all_files)}")
    print(f"Building hash index...")
    
    hash_index = build_hash_index(all_files)
    
    print(f"\nFinding duplicates...")
    duplicates = find_duplicates(hash_index)
    
    # Analyze cross-directory duplicates
    print(f"\nAnalyzing cross-directory duplicates...")
    cross_dir = analyze_cross_directory(hash_index, target_dirs)
    
    # Calculate stats
    total_dup_groups = len(duplicates)
    total_dup_files = sum(len(paths) - 1 for paths in duplicates.values())
    
    # Calculate wasted space
    wasted_space = 0
    for file_hash, paths in duplicates.items():
        if paths:
            # Find size of one copy
            sample_path = paths[0]
            if sample_path in all_files:
                file_size = all_files[sample_path]['size']
                wasted_space += file_size * (len(paths) - 1)
    
    elapsed = time.time() - total_start
    
    # Output results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    print(f"Total unique hashes: {len(hash_index)}")
    print(f"Duplicate groups: {total_dup_groups}")
    print(f"Redundant files: {total_dup_files}")
    print(f"Wasted space: {wasted_space / (1024**3):.2f} GB")
    print(f"Cross-directory duplicates: {len(cross_dir)}")
    print(f"Time: {elapsed:.1f}s")
    
    # Save detailed report to JSON
    report = {
        'summary': {
            'total_files': len(all_files),
            'unique_hashes': len(hash_index),
            'duplicate_groups': total_dup_groups,
            'redundant_files': total_dup_files,
            'wasted_space_bytes': wasted_space,
            'wasted_space_gb': round(wasted_space / (1024**3), 2),
            'cross_directory_duplicates': len(cross_dir),
            'scan_time_seconds': round(elapsed, 1)
        },
        'cross_directory_duplicates': sorted(cross_dir, key=lambda x: x['wasted_space'], reverse=True)[:200],
        'duplicate_groups_by_dir': {}
    }
    
    # Group duplicates by which directories they span
    for dup in cross_dir:
        dir_key = '-'.join(sorted(dup['dirs']))
        if dir_key not in report['duplicate_groups_by_dir']:
            report['duplicate_groups_by_dir'][dir_key] = {
                'count': 0,
                'files': []
            }
        report['duplicate_groups_by_dir'][dir_key]['count'] += 1
        report['duplicate_groups_by_dir'][dir_key]['files'].append({
            'hash': dup['hash'],
            'paths': dup['paths'],
            'count': dup['count']
        })
    
    # Save report
    report_path = '/Users/steven/dedup_scan_results.json'
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\nDetailed report saved to: {report_path}")
    
    # Print top cross-directory duplicates
    print("\n" + "=" * 80)
    print("TOP CROSS-DIRECTORY DUPLICATES (by wasted space)")
    print("=" * 80)
    
    for dup in sorted(cross_dir, key=lambda x: x['wasted_space'], reverse=True)[:30]:
        wasted_gb = dup['wasted_space'] / (1024**2)
        print(f"\n  Hash: {dup['hash'][:12]}... | {dup['count']} copies | {wasted_gb:.1f} MB wasted")
        print(f"  Dirs: {', '.join(dup['dirs'])}")
        for p in dup['paths'][:5]:  # Show first 5 paths
            print(f"    - {p[:80]}")
    
    # Save CSV of all duplicates for further processing
    csv_path = '/Users/steven/dedup_duplicates.csv'
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['hash', 'file_count', 'dirs', 'paths', 'sample_size_bytes'])
        
        for dup in sorted(cross_dir, key=lambda x: x['wasted_space'], reverse=True):
            sample_size = 0
            for p in dup['paths']:
                if p in all_files:
                    sample_size = all_files[p]['size']
                    break
            
            writer.writerow([
                dup['hash'],
                dup['count'],
                '|'.join(dup['dirs']),
                '|'.join(dup['paths']),
                sample_size
            ])
    
    print(f"\nDuplicate list saved to: {csv_path}")
    
    return report

if __name__ == '__main__':
    main()
