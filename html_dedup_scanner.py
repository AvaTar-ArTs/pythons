#!/usr/bin/env python3
"""
Scanner for Documents/HTML/organized_intelligent/
Find duplicate HTML files using SHA256 hashing
"""
import os
import sys
import hashlib
import json
import time
from collections import defaultdict

def sha256_file(filepath, chunk_size=65536):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    except:
        return None

def scan_html_directory(base_dir):
    """Scan HTML directory and find duplicates"""
    print(f"Scanning: {base_dir}")
    
    hash_index = defaultdict(list)
    count = 0
    
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for fname in files:
            fpath = os.path.join(root, fname)
            if not os.path.isfile(fpath):
                continue
            
            try:
                size = os.path.getsize(fpath)
            except:
                continue
            
            file_hash = sha256_file(fpath)
            if file_hash:
                hash_index[file_hash].append({
                    'path': fpath,
                    'rel_path': os.path.relpath(fpath, base_dir),
                    'size': size,
                    'name': fname
                })
            
            count += 1
            if count % 500 == 0:
                print(f"  Scanned {count} files...")
    
    # Find duplicates
    duplicates = {h: paths for h, paths in hash_index.items() if len(paths) > 1}
    
    # Stats
    total_files = count
    unique_hashes = len(hash_index)
    dup_groups = len(duplicates)
    dup_files = sum(len(paths) - 1 for paths in duplicates.values())
    
    wasted = 0
    for h, paths in duplicates.items():
        if paths:
            wasted += paths[0]['size'] * (len(paths) - 1)
    
    print(f"\n{'='*60}")
    print(f"HTML DEDUPLICATION RESULTS")
    print(f"{'='*60}")
    print(f"Total files: {total_files:,}")
    print(f"Unique hashes: {unique_hashes:,}")
    print(f"Duplicate groups: {dup_groups:,}")
    print(f"Redundant files: {dup_files:,}")
    print(f"Wasted space: {wasted / (1024**2):.1f} MB")
    
    # Save report
    report = {
        'summary': {
            'total_files': total_files,
            'unique_hashes': unique_hashes,
            'duplicate_groups': dup_groups,
            'redundant_files': dup_files,
            'wasted_bytes': wasted
        },
        'duplicates': []
    }
    
    for h, paths in sorted(duplicates.items(), key=lambda x: x[1][0]['size'], reverse=True):
        report['duplicates'].append({
            'hash': h,
            'count': len(paths),
            'size': paths[0]['size'],
            'paths': [p['rel_path'] for p in paths]
        })
    
    report_path = '/Users/steven/html_dedup_report.json'
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nReport: {report_path}")
    
    # Print top duplicates
    print(f"\nTOP DUPLICATE GROUPS:")
    for dup in report['duplicates'][:20]:
        print(f"\n  [{dup['size']/1024:.0f} KB] {dup['count']} copies:")
        for p in dup['paths']:
            print(f"    - {p}")
    
    return report

if __name__ == '__main__':
    base_dir = '/Users/steven/Documents/HTML/organized_intelligent'
    if os.path.isdir(base_dir):
        scan_html_directory(base_dir)
    else:
        print(f"Directory not found: {base_dir}")
