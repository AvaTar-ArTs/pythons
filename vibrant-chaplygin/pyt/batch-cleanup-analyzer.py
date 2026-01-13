#!/usr/bin/env python3
"""
Batch-Based External Volume Cleanup Analyzer
Process volumes incrementally to avoid timeouts
"""

import hashlib
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import csv

class BatchCleanupAnalyzer:
    """Process external volumes in manageable batches"""
    
    def __init__(self):
        self.master_dir = Path.home() / 'Documents' / 'pythons'
        self.output_dir = self.master_dir / '_analysis'
        self.output_dir.mkdir(exist_ok=True)
        
        self.master_index_file = self.output_dir / 'master_hashes.json'
        
    def hash_file_fast(self, filepath):
        """Fast hash using first 8KB + size"""
        try:
            size = filepath.stat().st_size
            with open(filepath, 'rb') as f:
                sample = f.read(8192)  # First 8KB
            return hashlib.md5(f"{size}:{sample}".encode()).hexdigest()
        except:
            return None
    
    def build_master_index(self):
        """Build hash index of master directory"""
        print("?? Building Master Index...")
        
        if self.master_index_file.exists():
            print(f"  ? Loading existing index: {self.master_index_file}")
            with open(self.master_index_file) as f:
                return json.load(f)
        
        master_index = {}
        py_files = list(self.master_dir.rglob('*.py'))
        
        print(f"  Found {len(py_files)} files in master directory")
        
        for i, filepath in enumerate(py_files, 1):
            if i % 100 == 0:
                print(f"    Progress: {i}/{len(py_files)}")
            
            # Skip backups and analysis dirs
            if any(x in str(filepath) for x in ['_backups', '_analysis', '_archives']):
                continue
            
            file_hash = self.hash_file_fast(filepath)
            if file_hash:
                master_index[file_hash] = {
                    'path': str(filepath),
                    'name': filepath.name,
                    'size': filepath.stat().st_size
                }
        
        # Save index
        with open(self.master_index_file, 'w') as f:
            json.dump(master_index, f, indent=2)
        
        print(f"  ? Indexed {len(master_index)} unique files")
        return master_index
    
    def scan_volume_batch(self, volume_path, batch_size=1000):
        """Scan a volume in batches"""
        print(f"\n?? Scanning {volume_path.name} in batches of {batch_size}...")
        
        if not volume_path.exists():
            print(f"  ??  Volume not mounted")
            return []
        
        # Get all Python files
        print("  Finding Python files...")
        py_files = list(volume_path.rglob('*.py'))
        total = len(py_files)
        
        print(f"  Found {total:,} Python files")
        
        results = []
        
        for batch_num, start_idx in enumerate(range(0, total, batch_size), 1):
            end_idx = min(start_idx + batch_size, total)
            batch = py_files[start_idx:end_idx]
            
            print(f"\n  Batch {batch_num}: Processing files {start_idx+1}-{end_idx} of {total}")
            
            for i, filepath in enumerate(batch, 1):
                if i % 100 == 0:
                    print(f"    Progress: {i}/{len(batch)}")
                
                try:
                    file_hash = self.hash_file_fast(filepath)
                    results.append({
                        'path': str(filepath),
                        'name': filepath.name,
                        'hash': file_hash,
                        'size': filepath.stat().st_size,
                        'parent': str(filepath.parent)
                    })
                except Exception as e:
                    pass
            
            # Save batch results
            batch_file = self.output_dir / f'{volume_path.name}_batch_{batch_num}.json'
            with open(batch_file, 'w') as f:
                json.dump(results[-len(batch):], f, indent=2)
            
            print(f"    ? Saved batch to: {batch_file.name}")
        
        return results
    
    def find_duplicates_in_batch(self, volume_name, master_index):
        """Find duplicates in saved batch files"""
        print(f"\n?? Finding Duplicates in {volume_name}...")
        
        batch_files = sorted(self.output_dir.glob(f'{volume_name}_batch_*.json'))
        
        if not batch_files:
            print("  No batch files found. Run scan first.")
            return []
        
        duplicates = []
        unique_external = []
        
        for batch_file in batch_files:
            with open(batch_file) as f:
                batch_data = json.load(f)
            
            for item in batch_data:
                if item['hash'] in master_index:
                    duplicates.append({
                        'external_path': item['path'],
                        'master_path': master_index[item['hash']]['path'],
                        'size': item['size'],
                        'name': item['name']
                    })
                else:
                    unique_external.append(item)
        
        print(f"  Found {len(duplicates)} duplicates")
        print(f"  Found {len(unique_external)} unique external files")
        
        return duplicates, unique_external
    
    def generate_cleanup_csv(self, volume_name, duplicates):
        """Generate CSV for easy review and batch processing"""
        csv_path = self.output_dir / f'{volume_name}_duplicates_to_remove.csv'
        
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['External_Path', 'Master_Path', 'Size_KB', 'Filename', 'Action'])
            
            for dup in duplicates:
                writer.writerow([
                    dup['external_path'],
                    dup['master_path'],
                    f"{dup['size'] / 1024:.1f}",
                    dup['name'],
                    'REMOVE'  # Default action
                ])
        
        print(f"  ? CSV saved: {csv_path}")
        return csv_path
    
    def execute_from_csv(self, csv_path, dry_run=True):
        """Execute cleanup from CSV file"""
        print(f"\n???  Executing Cleanup from CSV...")
        print(f"  CSV: {csv_path}")
        print(f"  Mode: {'DRY RUN' if dry_run else 'LIVE DELETION'}")
        
        removed_count = 0
        removed_size = 0
        
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        print(f"  Total files to process: {len(rows)}")
        
        for i, row in enumerate(rows, 1):
            if row['Action'].upper() != 'REMOVE':
                continue
            
            filepath = Path(row['External_Path'])
            
            if not filepath.exists():
                continue
            
            if dry_run:
                print(f"  [{i}/{len(rows)}] Would remove: {filepath.name}")
            else:
                try:
                    filepath.unlink()
                    removed_count += 1
                    removed_size += int(float(row['Size_KB']) * 1024)
                    if i % 100 == 0:
                        print(f"  [{i}/{len(rows)}] Removed {removed_count} files ({removed_size/(1024**2):.1f} MB)")
                except Exception as e:
                    print(f"  Error removing {filepath.name}: {e}")
        
        if dry_run:
            print(f"\n  DRY RUN: Would remove {len(rows)} files")
        else:
            print(f"\n  ? Removed {removed_count} files ({removed_size/(1024**3):.2f} GB)")

def main():
    import sys
    
    analyzer = BatchCleanupAnalyzer()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python batch-cleanup-analyzer.py index                    # Build master index")
        print("  python batch-cleanup-analyzer.py scan <volume>            # Scan volume (2T-Xx or DeVonDaTa)")
        print("  python batch-cleanup-analyzer.py find <volume>            # Find duplicates")
        print("  python batch-cleanup-analyzer.py execute <csv> [--live]   # Execute cleanup")
        print()
        print("Example workflow:")
        print("  1. python batch-cleanup-analyzer.py index")
        print("  2. python batch-cleanup-analyzer.py scan 2T-Xx")
        print("  3. python batch-cleanup-analyzer.py find 2T-Xx")
        print("  4. Review CSV, then:")
        print("  5. python batch-cleanup-analyzer.py execute 2T-Xx_duplicates_to_remove.csv --live")
        return
    
    command = sys.argv[1]
    
    if command == 'index':
        master_index = analyzer.build_master_index()
        print(f"\n? Master index built with {len(master_index)} files")
    
    elif command == 'scan':
        if len(sys.argv) < 3:
            print("Error: Specify volume (2T-Xx or DeVonDaTa)")
            return
        
        volume_name = sys.argv[2]
        volume_path = Path(f'/Volumes/{volume_name}')
        
        results = analyzer.scan_volume_batch(volume_path, batch_size=1000)
        print(f"\n? Scanned {len(results)} files")
    
    elif command == 'find':
        if len(sys.argv) < 3:
            print("Error: Specify volume (2T-Xx or DeVonDaTa)")
            return
        
        volume_name = sys.argv[2]
        
        # Load master index
        with open(analyzer.master_index_file) as f:
            master_index = json.load(f)
        
        # Find duplicates
        duplicates, unique = analyzer.find_duplicates_in_batch(volume_name, master_index)
        
        # Generate CSV
        csv_path = analyzer.generate_cleanup_csv(volume_name, duplicates)
        
        total_size = sum(d['size'] for d in duplicates)
        print(f"\n?? Summary:")
        print(f"  Duplicates: {len(duplicates)} files")
        print(f"  Space to reclaim: {total_size / (1024**3):.2f} GB")
        print(f"  Unique external files: {len(unique)}")
        print(f"\n? Review CSV: {csv_path}")
    
    elif command == 'execute':
        if len(sys.argv) < 3:
            print("Error: Specify CSV file")
            return
        
        csv_file = analyzer.output_dir / sys.argv[2]
        dry_run = '--live' not in sys.argv
        
        if not csv_file.exists():
            print(f"Error: CSV not found: {csv_file}")
            return
        
        analyzer.execute_from_csv(csv_file, dry_run=dry_run)
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
