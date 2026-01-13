#!/usr/bin/env python3
"""
Batch Volume Cleanup - Process Large Volumes in Chunks
Smart batching to handle 65K+ files without timeouts
"""

import hashlib
import json
import csv
from pathlib import Path
from datetime import datetime

class BatchVolumeCleanup:
    """Process volumes in small, manageable batches"""
    
    def __init__(self):
        self.master_dir = Path.home() / 'Documents' / 'pythons'
        self.analysis_dir = self.master_dir / '_analysis'
        self.analysis_dir.mkdir(exist_ok=True)
        self.master_index = None
        
    def quick_hash(self, filepath):
        """Super fast hash: filename + size + first 1KB"""
        try:
            stat = filepath.stat()
            with open(filepath, 'rb') as f:
                chunk = f.read(1024)
            return hashlib.md5(f"{filepath.name}{stat.st_size}{chunk}".encode()).hexdigest()
        except:
            return None
    
    def step1_index_master(self):
        """Step 1: Index master directory only (fast)"""
        print("?? STEP 1: Index Master Directory")
        print("=" * 80)
        
        index_file = self.analysis_dir / 'master_index.json'
        
        if index_file.exists():
            print(f"  ? Loading existing index")
            with open(index_file) as f:
                self.master_index = json.load(f)
            print(f"  ? Loaded {len(self.master_index)} master files")
            return
        
        self.master_index = {}
        
        # Only index main scripts, skip backups/analysis
        exclude = ['_backups', '_analysis', '_archives', '__pycache__']
        py_files = [
            f for f in self.master_dir.rglob('*.py')
            if not any(ex in str(f) for ex in exclude)
        ]
        
        print(f"  Indexing {len(py_files)} Python files...")
        
        for i, fp in enumerate(py_files, 1):
            if i % 100 == 0:
                print(f"    {i}/{len(py_files)}")
            
            h = self.quick_hash(fp)
            if h:
                self.master_index[h] = {
                    'name': fp.name,
                    'path': str(fp.relative_to(self.master_dir)),
                    'size': fp.stat().st_size
                }
        
        with open(index_file, 'w') as f:
            json.dump(self.master_index, f, indent=2)
        
        print(f"  ? Indexed {len(self.master_index)} files ? {index_file.name}")
    
    def step2_scan_volume_sample(self, volume_name, sample_size=5000):
        """Step 2: Scan SAMPLE of external volume"""
        print(f"\n?? STEP 2: Sample Scan of {volume_name} ({sample_size} files)")
        print("=" * 80)
        
        vol_path = Path(f'/Volumes/{volume_name}')
        if not vol_path.exists():
            print(f"  ??  Volume not mounted")
            return
        
        print(f"  Finding Python files...")
        
        # Get iterator to avoid loading all into memory
        all_py_files = vol_path.rglob('*.py')
        
        sample = []
        dupes = []
        unique = []
        
        count = 0
        for fp in all_py_files:
            count += 1
            
            if count % 500 == 0:
                print(f"    Processed: {count} ({len(dupes)} dupes, {len(unique)} unique)")
            
            if count > sample_size:
                print(f"    ? Sample limit reached ({sample_size})")
                break
            
            h = self.quick_hash(fp)
            if not h:
                continue
            
            info = {
                'path': str(fp),
                'name': fp.name,
                'hash': h,
                'size': fp.stat().st_size,
                'parent': str(fp.parent)
            }
            
            if h in self.master_index:
                dupes.append({
                    **info,
                    'master_path': self.master_index[h]['path'],
                    'action': 'SAFE_TO_REMOVE'
                })
            else:
                unique.append(info)
            
            sample.append(info)
        
        # Save results
        sample_file = self.analysis_dir / f'{volume_name}_sample_{sample_size}.json'
        with open(sample_file, 'w') as f:
            json.dump({'sample': sample, 'duplicates': dupes, 'unique': unique}, f, indent=2)
        
        # Generate CSV
        csv_path = self.analysis_dir / f'{volume_name}_duplicates_SAMPLE.csv'
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['External_Path', 'Master_Path', 'Size_KB', 'Filename', 'Parent_Dir', 'Action'])
            
            for d in dupes:
                writer.writerow([
                    d['path'],
                    f"~/Documents/pythons/{d['master_path']}",
                    f"{d['size']/1024:.1f}",
                    d['name'],
                    d['parent'],
                    d['action']
                ])
        
        dup_size = sum(d['size'] for d in dupes) / (1024**3)
        
        print(f"\n  ?? Sample Results ({count} files processed):")
        print(f"    ? Duplicates: {len(dupes)} ({dup_size:.2f} GB)")
        print(f"    ? Unique files: {len(unique)}")
        print(f"\n  ? CSV: {csv_path.name}")
        print(f"  ? JSON: {sample_file.name}")
        
        return dupes, unique
    
    def step3_summarize_findings(self):
        """Step 3: Create summary report"""
        print(f"\n?? STEP 3: Generate Summary Report")
        print("=" * 80)
        
        # Find all scan results
        devon_results = self.analysis_dir / 'DeVonDaTa_sample_5000.json'
        
        report_lines = [
            "# ?? External Volume Cleanup Summary\n",
            f"\n> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
            "\n## ?? Analysis Results\n\n"
        ]
        
        volumes_analyzed = {}
        
        # Check DeVonDaTa
        if devon_results.exists():
            with open(devon_results) as f:
                data = json.load(f)
            
            volumes_analyzed['DeVonDaTa'] = {
                'scanned': len(data['sample']),
                'duplicates': len(data['duplicates']),
                'unique': len(data['unique']),
                'size_gb': sum(d['size'] for d in data['duplicates']) / (1024**3)
            }
        
        for vol_name, stats in volumes_analyzed.items():
            report_lines.append(f"### {vol_name}\n")
            report_lines.append(f"- **Files Scanned**: {stats['scanned']:,}\n")
            report_lines.append(f"- **Duplicates Found**: {stats['duplicates']:,}\n")
            report_lines.append(f"- **Unique Files**: {stats['unique']:,}\n")
            report_lines.append(f"- **Space Reclaimable**: {stats['size_gb']:.2f} GB\n\n")
        
        report_lines.append("\n## ?? Next Steps\n\n")
        report_lines.append("1. Review CSV files in `_analysis/`\n")
        report_lines.append("2. Edit CSV to change Action column if needed\n")
        report_lines.append("3. Run: `python batch-volume-cleanup.py execute <volume> --dry-run`\n")
        report_lines.append("4. If satisfied: `python batch-volume-cleanup.py execute <volume> --live`\n")
        
        report_path = self.analysis_dir / 'CLEANUP_SUMMARY.md'
        with open(report_path, 'w') as f:
            f.writelines(report_lines)
        
        print(f"  ? Report: {report_path}")
        
        # Print summary
        print("\n" + "".join(report_lines))

def main():
    import sys
    
    cleanup = BatchVolumeCleanup()
    
    # Step 1: Index master
    cleanup.step1_index_master()
    
    # Step 2: Scan volumes (sample)
    print("\n" + "="*80)
    cleanup.step2_scan_volume_sample('DeVonDaTa', sample_size=5000)
    
    # Step 3: Summary
    print("\n" + "="*80)
    cleanup.step3_summarize_findings()
    
    print("\n" + "="*80)
    print("? BATCH ANALYSIS COMPLETE")
    print("="*80)
    print("\n?? Check _analysis/ folder for:")
    print("  ? DeVonDaTa_duplicates_SAMPLE.csv")
    print("  ? CLEANUP_SUMMARY.md")
    print("\n??  Next: Scan 2T-Xx (65K files) - run separately")

if __name__ == "__main__":
    main()
