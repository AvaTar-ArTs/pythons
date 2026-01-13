#!/usr/bin/env python3
"""
Deep dive analysis of directory structure, duplicates, and file statistics.
"""

import sys
import hashlib
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import json


class DeepDiveAnalyzer:
    def __init__(self, root_path, batch_size=50):
        self.root_path = Path(root_path)
        self.batch_size = max(50, min(200, batch_size))
        self.stats = {
            'total_files': 0,
            'total_size': 0,
            'files_by_type': Counter(),
            'files_by_size_range': Counter(),
            'duplicates_by_hash': defaultdict(list),
            'duplicates_by_name': defaultdict(list),
            'duplicates_by_size': defaultdict(list),
            'largest_files': [],
            'oldest_files': [],
            'newest_files': [],
            'directory_depth': defaultdict(int),
            'empty_directories': [],
            'errors': []
        }
    
    def calculate_hash(self, file_path, chunk_size=8192):
        """Calculate MD5 hash of file using chunks."""
        md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                while chunk := f.read(chunk_size):
                    md5.update(chunk)
            return md5.hexdigest()
        except Exception as e:
            self.stats['errors'].append(f"Hash error for {file_path}: {e}")
            return None
    
    def analyze(self):
        """Perform deep dive analysis."""
        print("=" * 80)
        print("DEEP DIVE ANALYSIS")
        print("=" * 80)
        print(f"\n📂 Analyzing: {self.root_path}")
        print(f"   Batch size: {self.batch_size} files")
        
        if not self.root_path.exists():
            print(f"\n❌ Error: Directory not found: {self.root_path}")
            return False
        
        # Collect all files
        print(f"\n📋 Scanning directory structure...")
        all_files = []
        for file_path in self.root_path.rglob('*'):
            if file_path.is_file():
                try:
                    stat = file_path.stat()
                    rel_path = str(file_path.relative_to(self.root_path))
                    depth = len(rel_path.split('/')) - 1
                    
                    all_files.append({
                        'path': file_path,
                        'rel_path': rel_path,
                        'size': stat.st_size,
                        'mtime': stat.st_mtime,
                        'depth': depth,
                        'extension': file_path.suffix.lower() or '(no extension)',
                        'name': file_path.name
                    })
                    
                    self.stats['directory_depth'][depth] += 1
                    self.stats['total_files'] += 1
                    self.stats['total_size'] += stat.st_size
                    self.stats['files_by_type'][file_path.suffix.lower() or '(no extension)'] += 1
                    
                except Exception as e:
                    self.stats['errors'].append(f"Error accessing {file_path}: {e}")
        
        print(f"   Found {len(all_files):,} files")
        
        # Group by name and size for duplicate detection
        print(f"\n🔍 Analyzing for duplicates...")
        by_name = defaultdict(list)
        by_size = defaultdict(list)
        
        for file_info in all_files:
            by_name[file_info['name']].append(file_info)
            by_size[file_info['size']].append(file_info)
        
        # Find duplicates by name
        for name, files in by_name.items():
            if len(files) > 1:
                sizes = [f['size'] for f in files]
                if len(set(sizes)) == 1:
                    # Same name, same size - likely duplicates
                    self.stats['duplicates_by_name'][name] = [f['rel_path'] for f in files]
        
        # Find potential duplicates by size
        for size, files in by_size.items():
            if len(files) > 1 and size > 0:  # Ignore empty files
                self.stats['duplicates_by_size'][size] = [f['rel_path'] for f in files]
        
        # Hash-based duplicate detection (sample)
        print(f"   Calculating file hashes (sampling large groups)...")
        hash_groups = defaultdict(list)
        
        # Only hash files that appear in size-based duplicate groups
        files_to_hash = []
        for size, file_list in self.stats['duplicates_by_size'].items():
            if len(file_list) > 1 and size < 100 * 1024 * 1024:  # Only hash files < 100MB
                for rel_path in file_list[:5]:  # Limit to first 5 per group
                    file_path = self.root_path / rel_path
                    if file_path.exists():
                        files_to_hash.append((rel_path, file_path, size))
        
        print(f"   Hashing {len(files_to_hash)} potential duplicate files...")
        for idx, (rel_path, file_path, size) in enumerate(files_to_hash, 1):
            if idx % 50 == 0:
                print(f"     Processed {idx}/{len(files_to_hash)} files...", end='\r')
            
            file_hash = self.calculate_hash(file_path)
            if file_hash:
                hash_groups[file_hash].append(rel_path)
        
        print(f"     Processed {len(files_to_hash)} files")
        
        # Find exact duplicates by hash
        for file_hash, file_list in hash_groups.items():
            if len(file_list) > 1:
                self.stats['duplicates_by_hash'][file_hash] = file_list
        
        # Find largest files
        print(f"\n📊 Collecting statistics...")
        sorted_by_size = sorted(all_files, key=lambda x: x['size'], reverse=True)
        self.stats['largest_files'] = [
            {'path': f['rel_path'], 'size': f['size']} 
            for f in sorted_by_size[:20]
        ]
        
        # Find oldest/newest files
        sorted_by_time = sorted(all_files, key=lambda x: x['mtime'])
        self.stats['oldest_files'] = [
            {'path': f['rel_path'], 'date': datetime.fromtimestamp(f['mtime']).strftime('%Y-%m-%d %H:%M:%S')}
            for f in sorted_by_time[:10]
        ]
        self.stats['newest_files'] = [
            {'path': f['rel_path'], 'date': datetime.fromtimestamp(f['mtime']).strftime('%Y-%m-%d %H:%M:%S')}
            for f in sorted_by_time[-10:]
        ]
        
        # Find empty directories
        for dir_path in self.root_path.rglob('*'):
            if dir_path.is_dir():
                try:
                    if not any(dir_path.iterdir()):
                        self.stats['empty_directories'].append(str(dir_path.relative_to(self.root_path)))
                except:
                    pass
        
        # Size ranges
        for file_info in all_files:
            size = file_info['size']
            if size == 0:
                self.stats['files_by_size_range']['0 bytes'] += 1
            elif size < 1024:
                self.stats['files_by_size_range']['< 1 KB'] += 1
            elif size < 1024 * 1024:
                self.stats['files_by_size_range']['1 KB - 1 MB'] += 1
            elif size < 10 * 1024 * 1024:
                self.stats['files_by_size_range']['1 MB - 10 MB'] += 1
            elif size < 100 * 1024 * 1024:
                self.stats['files_by_size_range']['10 MB - 100 MB'] += 1
            else:
                self.stats['files_by_size_range']['> 100 MB'] += 1
        
        return True
    
    def print_report(self):
        """Print comprehensive analysis report."""
        print("\n" + "=" * 80)
        print("ANALYSIS REPORT")
        print("=" * 80)
        
        # Basic statistics
        print(f"\n📊 BASIC STATISTICS")
        print(f"   Total files: {self.stats['total_files']:,}")
        print(f"   Total size: {self.stats['total_size']/1024/1024/1024:.2f} GB")
        print(f"   Average file size: {self.stats['total_size']/self.stats['total_files']/1024/1024:.2f} MB" if self.stats['total_files'] > 0 else "   N/A")
        
        # File types
        print(f"\n📁 FILE TYPES (Top 20)")
        for ext, count in self.stats['files_by_type'].most_common(20):
            print(f"   {ext:20s} {count:6,} files")
        
        # Size distribution
        print(f"\n📏 SIZE DISTRIBUTION")
        for size_range in ['0 bytes', '< 1 KB', '1 KB - 1 MB', '1 MB - 10 MB', '10 MB - 100 MB', '> 100 MB']:
            count = self.stats['files_by_size_range'][size_range]
            if count > 0:
                print(f"   {size_range:20s} {count:6,} files")
        
        # Duplicates by hash (exact duplicates)
        print(f"\n🔍 EXACT DUPLICATES (Same Hash)")
        hash_dupes = len(self.stats['duplicates_by_hash'])
        if hash_dupes > 0:
            total_dupe_files = sum(len(files) for files in self.stats['duplicates_by_hash'].values())
            wasted_space = 0
            for file_hash, file_list in list(self.stats['duplicates_by_hash'].items())[:10]:
                if file_list:
                    file_path = self.root_path / file_list[0]
                    if file_path.exists():
                        size = file_path.stat().st_size
                        wasted_space += size * (len(file_list) - 1)
                        print(f"   Hash: {file_hash[:16]}... ({len(file_list)} copies)")
                        for rel_path in file_list[:3]:
                            print(f"     - {rel_path}")
                        if len(file_list) > 3:
                            print(f"     ... and {len(file_list) - 3} more")
            
            print(f"\n   Total duplicate groups: {hash_dupes}")
            print(f"   Total duplicate files: {total_dupe_files}")
            print(f"   Wasted space: {wasted_space/1024/1024/1024:.2f} GB")
        else:
            print("   ✅ No exact duplicates found")
        
        # Duplicates by name
        print(f"\n📝 DUPLICATES BY NAME (Same filename, same size)")
        name_dupes = len(self.stats['duplicates_by_name'])
        if name_dupes > 0:
            for name, file_list in list(self.stats['duplicates_by_name'].items())[:20]:
                print(f"   {name} ({len(file_list)} copies)")
                for rel_path in file_list[:2]:
                    print(f"     - {rel_path}")
                if len(file_list) > 2:
                    print(f"     ... and {len(file_list) - 2} more")
            if name_dupes > 20:
                print(f"   ... and {name_dupes - 20} more duplicate names")
        else:
            print("   ✅ No duplicate filenames found")
        
        # Potential duplicates by size
        print(f"\n⚖️  POTENTIAL DUPLICATES BY SIZE")
        size_dupes = {k: v for k, v in self.stats['duplicates_by_size'].items() if len(v) > 1}
        if size_dupes:
            large_groups = sorted(size_dupes.items(), key=lambda x: (len(x[1]), x[0]), reverse=True)[:10]
            for size, file_list in large_groups:
                if len(file_list) > 1:
                    print(f"   Size: {size/1024/1024:.2f} MB ({len(file_list)} files)")
                    for rel_path in file_list[:3]:
                        print(f"     - {rel_path}")
                    if len(file_list) > 3:
                        print(f"     ... and {len(file_list) - 3} more")
        else:
            print("   ✅ No size-based duplicates found")
        
        # Largest files
        print(f"\n📦 LARGEST FILES (Top 20)")
        for idx, file_info in enumerate(self.stats['largest_files'], 1):
            size_mb = file_info['size'] / 1024 / 1024
            size_gb = file_info['size'] / 1024 / 1024 / 1024
            size_str = f"{size_gb:.2f} GB" if size_gb >= 1 else f"{size_mb:.2f} MB"
            print(f"   {idx:2d}. {file_info['path'][:60]}")
            print(f"       {size_str}")
        
        # Directory depth
        print(f"\n📂 DIRECTORY DEPTH ANALYSIS")
        if self.stats['directory_depth']:
            max_depth = max(self.stats['directory_depth'].keys())
            print(f"   Maximum depth: {max_depth} levels")
            for depth in sorted(self.stats['directory_depth'].keys())[:10]:
                print(f"   Depth {depth}: {self.stats['directory_depth'][depth]:,} files")
        
        # Empty directories
        if self.stats['empty_directories']:
            print(f"\n📁 EMPTY DIRECTORIES ({len(self.stats['empty_directories'])} found)")
            for empty_dir in self.stats['empty_directories'][:20]:
                print(f"   - {empty_dir}")
            if len(self.stats['empty_directories']) > 20:
                print(f"   ... and {len(self.stats['empty_directories']) - 20} more")
        
        # Errors
        if self.stats['errors']:
            print(f"\n⚠️  ERRORS ({len(self.stats['errors'])} found)")
            for error in self.stats['errors'][:10]:
                print(f"   - {error}")
            if len(self.stats['errors']) > 10:
                print(f"   ... and {len(self.stats['errors']) - 10} more")
        
        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
    
    def export_json(self, output_file):
        """Export results to JSON."""
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            # Convert defaultdict to dict for JSON serialization
            json_stats = {
                'total_files': self.stats['total_files'],
                'total_size': self.stats['total_size'],
                'files_by_type': dict(self.stats['files_by_type']),
                'duplicates_by_hash': {k: v for k, v in list(self.stats['duplicates_by_hash'].items())[:100]},
                'duplicates_by_name': dict(list(self.stats['duplicates_by_name'].items())[:100]),
                'largest_files': self.stats['largest_files'],
            }
            json.dump(json_stats, f, indent=2)
        print(f"\n💾 Results exported to: {output_file}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python deepdive_analysis.py <directory> [--batch-size N] [--export json_file]")
        print("\nExample:")
        print("  python deepdive_analysis.py /path/to/dir")
        print("  python deepdive_analysis.py /path/to/dir --batch-size 100")
        print("  python deepdive_analysis.py /path/to/dir --export results.json")
        sys.exit(1)
    
    root_path = sys.argv[1]
    batch_size = 50
    export_file = None
    
    # Parse arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--batch-size' and i + 1 < len(sys.argv):
            batch_size = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--export' and i + 1 < len(sys.argv):
            export_file = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    analyzer = DeepDiveAnalyzer(root_path, batch_size)
    if analyzer.analyze():
        analyzer.print_report()
        if export_file:
            analyzer.export_json(export_file)
