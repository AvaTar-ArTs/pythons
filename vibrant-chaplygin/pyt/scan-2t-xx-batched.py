#!/usr/bin/env python3
"""
Scan 2T-Xx in Small Batches
Process 65K+ files in manageable 1000-file chunks with progress saving
"""

import hashlib
import json
import csv
from pathlib import Path
from datetime import datetime

def quick_hash(filepath):
    """Fast hash for duplicate detection"""
    try:
        stat = filepath.stat()
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
        return hashlib.md5(f"{filepath.name}{stat.st_size}{chunk}".encode()).hexdigest()
    except:
        return None

def scan_batch(volume_path, master_index, batch_num, start_idx, batch_size):
    """Scan one batch"""
    analysis_dir = Path.home() / 'Documents' / 'pythons' / '_analysis'
    
    print(f"\n?? Batch {batch_num}: Files {start_idx+1} to {start_idx+batch_size}")
    
    # Get all Python files (generator to save memory)
    all_files = list(volume_path.rglob('*.py'))
    total = len(all_files)
    
    if start_idx >= total:
        print(f"  ? All files processed (total: {total})")
        return None, None
    
    batch = all_files[start_idx:start_idx + batch_size]
    
    print(f"  Processing {len(batch)} files...")
    
    duplicates = []
    unique = []
    
    for i, fp in enumerate(batch, 1):
        if i % 200 == 0:
            print(f"    {i}/{len(batch)} ({len(duplicates)} dupes)")
        
        h = quick_hash(fp)
        if not h:
            continue
        
        info = {
            'path': str(fp),
            'name': fp.name,
            'size': fp.stat().st_size,
            'parent': str(fp.parent)
        }
        
        if h in master_index:
            duplicates.append({
                **info,
                'master_path': master_index[h]['path']
            })
        else:
            unique.append(info)
    
    # Save batch results
    batch_file = analysis_dir / f'2T-Xx_batch_{batch_num:03d}_duplicates.csv'
    
    with open(batch_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['External_Path', 'Master_Path', 'Size_KB', 'Filename', 'Action'])
        
        for d in duplicates:
            writer.writerow([
                d['path'],
                f"~/Documents/pythons/{d['master_path']}",
                f"{d['size']/1024:.1f}",
                d['name'],
                'SAFE_TO_REMOVE'
            ])
    
    dup_size_mb = sum(d['size'] for d in duplicates) / (1024**2)
    
    print(f"  ? Batch {batch_num} complete:")
    print(f"    ? Duplicates: {len(duplicates)} ({dup_size_mb:.1f} MB)")
    print(f"    ? Unique: {len(unique)}")
    print(f"    ? Saved: {batch_file.name}")
    
    # Save progress
    progress_file = analysis_dir / '2T-Xx_scan_progress.json'
    progress = {
        'last_batch': batch_num,
        'last_index': start_idx + batch_size,
        'total_files': total,
        'timestamp': datetime.now().isoformat()
    }
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=2)
    
    return len(duplicates), len(unique)

def main():
    import sys
    
    analysis_dir = Path.home() / 'Documents' / 'pythons' / '_analysis'
    
    # Load master index
    index_file = analysis_dir / 'master_index.json'
    if not index_file.exists():
        print("? Run batch-volume-cleanup.py first to create master index")
        return
    
    with open(index_file) as f:
        master_index = json.load(f)
    
    print("?? 2T-Xx Batch Scanner")
    print("=" * 80)
    print(f"Master index: {len(master_index)} files")
    
    # Get batch number from command line or use 1
    start_batch = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    num_batches = int(sys.argv[2]) if len(sys.argv) > 2 else 5  # Process 5 batches by default
    
    volume_path = Path('/Volumes/2T-Xx')
    batch_size = 1000
    
    print(f"Processing {num_batches} batches starting from batch {start_batch}")
    print(f"Batch size: {batch_size} files per batch")
    
    total_dupes = 0
    total_unique = 0
    
    for batch_offset in range(num_batches):
        batch_num = start_batch + batch_offset
        start_idx = (batch_num - 1) * batch_size
        
        dupes, unique = scan_batch(volume_path, master_index, batch_num, start_idx, batch_size)
        
        if dupes is None:
            print("\n? All files processed!")
            break
        
        total_dupes += dupes
        total_unique += unique
    
    print("\n" + "=" * 80)
    print("? BATCH SCAN COMPLETE")
    print("=" * 80)
    print(f"\n?? Totals for this run:")
    print(f"  ? Batches processed: {num_batches}")
    print(f"  ? Duplicates found: {total_dupes}")
    print(f"  ? Unique files: {total_unique}")
    print(f"\n?? Results in: _analysis/2T-Xx_batch_*.csv")
    print(f"\n??  Next: python scan-2t-xx-batched.py {start_batch + num_batches} 5")

if __name__ == "__main__":
    main()
