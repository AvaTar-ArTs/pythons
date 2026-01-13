#!/usr/bin/env python3
"""
Comprehensive Dedupe, Merge, Diff, and Du Tool
Unified tool for duplicate detection, file merging, diffing, and disk usage analysis
"""

import os
import hashlib
import shutil
import difflib
import subprocess
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import argparse
import json
import csv

class DedupeMergeDiffTool:
    def __init__(self, root_dir=None, dry_run=True):
        self.root = Path(root_dir) if root_dir else Path.cwd()
        self.dry_run = dry_run
        self.duplicates = defaultdict(list)
        self.file_hashes = {}
        self.stats = {
            'total_files': 0,
            'duplicate_groups': 0,
            'potential_savings': 0,
            'merged_files': 0,
            'diff_results': []
        }
    
    # ==================== DEDUPE FUNCTIONS ====================
    
    def calculate_hash(self, filepath, algorithm='md5', chunk_size=8192):
        """Calculate file hash with optional chunking for large files"""
        hash_obj = hashlib.new(algorithm)
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(chunk_size):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except Exception as e:
            print(f"⚠️  Error hashing {filepath}: {e}")
            return None
    
    def find_duplicates(self, max_size_mb=50, algorithm='md5'):
        """Find duplicate files by content hash"""
        print("🔍 Scanning for duplicates...")
        print(f"   Max file size: {max_size_mb} MB")
        print(f"   Algorithm: {algorithm}\n")
        
        max_size = max_size_mb * 1024 * 1024
        file_count = 0
        
        for root, dirs, files in os.walk(self.root):
            # Skip common exclusions
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}]
            
            for file in files:
                filepath = Path(root) / file
                
                try:
                    if filepath.stat().st_size > max_size:
                        continue
                    
                    file_hash = self.calculate_hash(filepath, algorithm)
                    if file_hash:
                        rel_path = filepath.relative_to(self.root)
                        self.duplicates[file_hash].append({
                            'path': filepath,
                            'rel_path': str(rel_path),
                            'size': filepath.stat().st_size,
                            'mtime': filepath.stat().st_mtime,
                            'name': filepath.name
                        })
                        self.file_hashes[str(rel_path)] = file_hash
                        file_count += 1
                        
                        if file_count % 1000 == 0:
                            print(f"   ... {file_count:,} files scanned")
                
                except (PermissionError, OSError):
                    continue
        
        # Filter to only groups with 2+ files
        self.duplicates = {k: v for k, v in self.duplicates.items() if len(v) > 1}
        self.stats['duplicate_groups'] = len(self.duplicates)
        
        # Calculate potential savings
        for files in self.duplicates.values():
            # Keep one, delete rest
            duplicate_size = files[0]['size'] * (len(files) - 1)
            self.stats['potential_savings'] += duplicate_size
        
        print(f"\n✅ Found {len(self.duplicates)} duplicate groups")
        print(f"   Potential savings: {self.stats['potential_savings'] / (1024**2):.2f} MB")
        return self.duplicates
    
    def dedupe(self, strategy='newest', keep_paths=None):
        """Remove duplicate files based on strategy"""
        if not self.duplicates:
            print("No duplicates found. Run find_duplicates() first.")
            return
        
        print(f"\n🗑️  Deduplicating files (strategy: {strategy})...")
        print(f"{'DRY RUN - ' if self.dry_run else ''}Removing duplicates...\n")
        
        deleted = []
        saved_space = 0
        
        for hash_val, files in sorted(
            self.duplicates.items(),
            key=lambda x: x[1][0]['size'] * len(x[1]),
            reverse=True
        ):
            # Determine which file to keep
            if strategy == 'newest':
                files.sort(key=lambda x: x['mtime'], reverse=True)
                keep_file = files[0]
            elif strategy == 'oldest':
                files.sort(key=lambda x: x['mtime'])
                keep_file = files[0]
            elif strategy == 'largest':
                files.sort(key=lambda x: x['size'], reverse=True)
                keep_file = files[0]
            elif strategy == 'smallest':
                files.sort(key=lambda x: x['size'])
                keep_file = files[0]
            elif strategy == 'shortest_path':
                files.sort(key=lambda x: len(x['rel_path']))
                keep_file = files[0]
            elif keep_paths:
                # Keep file matching preferred path pattern
                keep_file = None
                for file in files:
                    if any(pattern in file['rel_path'] for pattern in keep_paths):
                        keep_file = file
                        break
                if not keep_file:
                    keep_file = files[0]  # Fallback to first
            else:
                keep_file = files[0]
            
            delete_files = [f for f in files if f['path'] != keep_file['path']]
            
            print(f"📁 {keep_file['name']} ({keep_file['size'] / 1024:.1f} KB)")
            print(f"   ✅ KEEP: {keep_file['rel_path']}")
            
            for file_to_delete in delete_files:
                print(f"   🗑️  DELETE: {file_to_delete['rel_path']}")
                
                if not self.dry_run:
                    try:
                        file_to_delete['path'].unlink()
                        deleted.append(file_to_delete['rel_path'])
                        saved_space += file_to_delete['size']
                    except Exception as e:
                        print(f"   ⚠️  ERROR: {e}")
            
            print()
        
        if not self.dry_run:
            print(f"✅ Deleted {len(deleted)} duplicate files")
            print(f"   Space saved: {saved_space / (1024**2):.2f} MB")
        
        return deleted, saved_space
    
    # ==================== MERGE FUNCTIONS ====================
    
    def merge_files(self, file_paths, output_path, merge_strategy='concatenate'):
        """Merge multiple files into one"""
        if len(file_paths) < 2:
            print("Need at least 2 files to merge")
            return False
        
        print(f"\n🔀 Merging {len(file_paths)} files...")
        print(f"   Strategy: {merge_strategy}")
        print(f"   Output: {output_path}\n")
        
        if not self.dry_run:
            try:
                with open(output_path, 'w', encoding='utf-8') as outfile:
                    for i, file_path in enumerate(file_paths):
                        path = Path(file_path)
                        if not path.exists():
                            print(f"   ⚠️  Skipping {path} (not found)")
                            continue
                        
                        print(f"   📄 Merging: {path.name}")
                        
                        if merge_strategy == 'concatenate':
                            with open(path, 'r', encoding='utf-8', errors='ignore') as infile:
                                if i > 0:
                                    outfile.write('\n' + '='*80 + '\n')
                                    outfile.write(f"# From: {path.name}\n")
                                    outfile.write('='*80 + '\n\n')
                                outfile.write(infile.read())
                        
                        elif merge_strategy == 'unique_lines':
                            with open(path, 'r', encoding='utf-8', errors='ignore') as infile:
                                seen = set()
                                for line in infile:
                                    if line not in seen:
                                        seen.add(line)
                                        outfile.write(line)
                
                self.stats['merged_files'] += 1
                print(f"\n✅ Merged files saved to: {output_path}")
                return True
            
            except Exception as e:
                print(f"   ⚠️  Error merging: {e}")
                return False
        else:
            print("   [DRY RUN] Would merge files")
            return True
    
    def merge_directories(self, dir_paths, output_dir, merge_strategy='copy_all'):
        """Merge multiple directories into one"""
        if len(dir_paths) < 2:
            print("Need at least 2 directories to merge")
            return False
        
        print(f"\n🔀 Merging {len(dir_paths)} directories...")
        print(f"   Strategy: {merge_strategy}")
        print(f"   Output: {output_dir}\n")
        
        output_path = Path(output_dir)
        if not self.dry_run:
            output_path.mkdir(parents=True, exist_ok=True)
        
        file_conflicts = []
        files_copied = 0
        
        for dir_path in dir_paths:
            source = Path(dir_path)
            if not source.exists() or not source.is_dir():
                print(f"   ⚠️  Skipping {source} (not a directory)")
                continue
            
            print(f"   📂 Processing: {source.name}")
            
            for item in source.rglob('*'):
                if item.is_file():
                    rel_path = item.relative_to(source)
                    dest = output_path / rel_path
                    
                    if dest.exists():
                        file_conflicts.append({
                            'source': str(item),
                            'dest': str(dest),
                            'size': item.stat().st_size
                        })
                        print(f"      ⚠️  Conflict: {rel_path}")
                        
                        if merge_strategy == 'overwrite':
                            if not self.dry_run:
                                shutil.copy2(item, dest)
                            files_copied += 1
                        elif merge_strategy == 'rename':
                            counter = 1
                            while dest.exists():
                                stem = dest.stem
                                suffix = dest.suffix
                                dest = dest.parent / f"{stem}_{counter}{suffix}"
                                counter += 1
                            if not self.dry_run:
                                shutil.copy2(item, dest)
                            files_copied += 1
                        # skip strategy: do nothing
                    else:
                        if not self.dry_run:
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(item, dest)
                        files_copied += 1
        
        print(f"\n✅ Merged directories")
        print(f"   Files copied: {files_copied}")
        print(f"   Conflicts: {len(file_conflicts)}")
        
        if file_conflicts:
            print("\n   Conflict details:")
            for conflict in file_conflicts[:10]:
                print(f"      {Path(conflict['source']).name}")
        
        return True
    
    # ==================== DIFF FUNCTIONS ====================
    
    def diff_files(self, file1, file2, output_format='unified'):
        """Compare two files and show differences"""
        path1 = Path(file1)
        path2 = Path(file2)
        
        if not path1.exists() or not path2.exists():
            print(f"⚠️  One or both files don't exist")
            return None
        
        print(f"\n🔍 Comparing files...")
        print(f"   File 1: {path1}")
        print(f"   File 2: {path2}\n")
        
        try:
            with open(path1, 'r', encoding='utf-8', errors='ignore') as f1:
                lines1 = f1.readlines()
            with open(path2, 'r', encoding='utf-8', errors='ignore') as f2:
                lines2 = f2.readlines()
            
            if output_format == 'unified':
                diff = list(difflib.unified_diff(
                    lines1, lines2,
                    fromfile=str(path1),
                    tofile=str(path2),
                    lineterm=''
                ))
            elif output_format == 'context':
                diff = list(difflib.context_diff(
                    lines1, lines2,
                    fromfile=str(path1),
                    tofile=str(path2),
                    lineterm=''
                ))
            elif output_format == 'html':
                diff = difflib.HtmlDiff().make_file(
                    lines1, lines2,
                    fromdesc=str(path1),
                    todesc=str(path2)
                )
                return diff
            else:
                diff = list(difflib.ndiff(lines1, lines2))
            
            if diff:
                print("   Differences found:")
                for line in diff[:50]:  # Show first 50 lines
                    print(f"   {line}")
                if len(diff) > 50:
                    print(f"   ... ({len(diff) - 50} more lines)")
            else:
                print("   ✅ Files are identical")
            
            self.stats['diff_results'].append({
                'file1': str(path1),
                'file2': str(path2),
                'diff_lines': len(diff),
                'identical': len(diff) == 0
            })
            
            return diff
        
        except Exception as e:
            print(f"   ⚠️  Error comparing files: {e}")
            return None
    
    def diff_directories(self, dir1, dir2, output_file=None):
        """Compare two directories and show differences"""
        path1 = Path(dir1)
        path2 = Path(dir2)
        
        if not path1.exists() or not path2.exists():
            print(f"⚠️  One or both directories don't exist")
            return None
        
        print(f"\n🔍 Comparing directories...")
        print(f"   Dir 1: {path1}")
        print(f"   Dir 2: {path2}\n")
        
        files1 = {f.relative_to(path1): f for f in path1.rglob('*') if f.is_file()}
        files2 = {f.relative_to(path2): f for f in path2.rglob('*') if f.is_file()}
        
        only_in_1 = set(files1.keys()) - set(files2.keys())
        only_in_2 = set(files2.keys()) - set(files1.keys())
        in_both = set(files1.keys()) & set(files2.keys())
        
        different = []
        identical = []
        
        for rel_path in in_both:
            hash1 = self.calculate_hash(files1[rel_path])
            hash2 = self.calculate_hash(files2[rel_path])
            
            if hash1 == hash2:
                identical.append(rel_path)
            else:
                different.append(rel_path)
        
        print(f"📊 Comparison Results:")
        print(f"   Files only in {path1.name}: {len(only_in_1)}")
        print(f"   Files only in {path2.name}: {len(only_in_2)}")
        print(f"   Files in both (identical): {len(identical)}")
        print(f"   Files in both (different): {len(different)}")
        
        if only_in_1:
            print(f"\n   Only in {path1.name}:")
            for f in list(only_in_1)[:10]:
                print(f"      {f}")
            if len(only_in_1) > 10:
                print(f"      ... ({len(only_in_1) - 10} more)")
        
        if only_in_2:
            print(f"\n   Only in {path2.name}:")
            for f in list(only_in_2)[:10]:
                print(f"      {f}")
            if len(only_in_2) > 10:
                print(f"      ... ({len(only_in_2) - 10} more)")
        
        if different:
            print(f"\n   Different files:")
            for f in different[:10]:
                print(f"      {f}")
            if len(different) > 10:
                print(f"      ... ({len(different) - 10} more)")
        
        result = {
            'only_in_1': [str(f) for f in only_in_1],
            'only_in_2': [str(f) for f in only_in_2],
            'identical': [str(f) for f in identical],
            'different': [str(f) for f in different]
        }
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n✅ Results saved to: {output_file}")
        
        return result
    
    # ==================== DU (DISK USAGE) FUNCTIONS ====================
    
    def du(self, path=None, max_depth=3, sort_by='size'):
        """Show disk usage for directory"""
        target = Path(path) if path else self.root
        
        if not target.exists():
            print(f"⚠️  Path doesn't exist: {target}")
            return None
        
        print(f"\n💾 Disk Usage Analysis: {target}")
        print(f"   Max depth: {max_depth}\n")
        
        usage = []
        
        def get_size(path_obj, depth=0):
            if depth > max_depth:
                return 0, 0
            
            total_size = 0
            file_count = 0
            
            try:
                if path_obj.is_file():
                    return path_obj.stat().st_size, 1
                
                for item in path_obj.iterdir():
                    try:
                        if item.is_file():
                            size = item.stat().st_size
                            total_size += size
                            file_count += 1
                        elif item.is_dir():
                            sub_size, sub_count = get_size(item, depth + 1)
                            total_size += sub_size
                            file_count += sub_count
                    except (PermissionError, OSError):
                        continue
                
                if total_size > 0 and depth <= max_depth:
                    rel_path = path_obj.relative_to(target) if path_obj != target else Path('.')
                    usage.append({
                        'path': str(rel_path),
                        'size': total_size,
                        'size_mb': total_size / (1024**2),
                        'size_gb': total_size / (1024**3),
                        'files': file_count
                    })
            
            except (PermissionError, OSError):
                pass
            
            return total_size, file_count
        
        get_size(target)
        
        # Sort results
        if sort_by == 'size':
            usage.sort(key=lambda x: x['size'], reverse=True)
        elif sort_by == 'files':
            usage.sort(key=lambda x: x['files'], reverse=True)
        elif sort_by == 'path':
            usage.sort(key=lambda x: x['path'])
        
        # Display results
        print(f"{'Path':<50} {'Size':>12} {'Files':>10}")
        print("-" * 75)
        
        for item in usage[:50]:  # Top 50
            size_str = f"{item['size_mb']:.1f} MB" if item['size_mb'] < 1024 else f"{item['size_gb']:.2f} GB"
            path_str = item['path'][:48] + '..' if len(item['path']) > 50 else item['path']
            print(f"{path_str:<50} {size_str:>12} {item['files']:>10,}")
        
        if len(usage) > 50:
            print(f"\n   ... ({len(usage) - 50} more directories)")
        
        total_size = sum(item['size'] for item in usage)
        total_files = sum(item['files'] for item in usage)
        
        print("-" * 75)
        print(f"{'TOTAL':<50} {total_size/(1024**3):.2f} GB {total_files:>10,}")
        
        return usage
    
    # ==================== REPORT GENERATION ====================
    
    def generate_report(self, output_file=None):
        """Generate comprehensive report"""
        if output_file is None:
            output_file = self.root / f"DEDUPE_MERGE_DIFF_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(output_file, 'w') as f:
            f.write("# Dedupe, Merge, Diff, and Du Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Root Directory:** `{self.root}`\n\n")
            f.write("---\n\n")
            
            f.write("## 📊 Statistics\n\n")
            f.write(f"- **Duplicate Groups:** {self.stats['duplicate_groups']}\n")
            f.write(f"- **Potential Savings:** {self.stats['potential_savings'] / (1024**2):.2f} MB\n")
            f.write(f"- **Merged Files:** {self.stats['merged_files']}\n")
            f.write(f"- **Diff Comparisons:** {len(self.stats['diff_results'])}\n\n")
            
            if self.duplicates:
                f.write("## 🔄 Duplicate Files\n\n")
                sorted_dupes = sorted(
                    self.duplicates.items(),
                    key=lambda x: x[1][0]['size'] * len(x[1]),
                    reverse=True
                )[:50]
                
                for i, (hash_val, files) in enumerate(sorted_dupes, 1):
                    f.write(f"### Group {i}: {files[0]['name']}\n\n")
                    f.write(f"- **Size:** {files[0]['size'] / 1024:.1f} KB\n")
                    f.write(f"- **Copies:** {len(files)}\n")
                    f.write(f"- **Locations:**\n")
                    for file in files:
                        f.write(f"  - `{file['rel_path']}`\n")
                    f.write("\n")
        
        print(f"✅ Report saved: {output_file}")
        return output_file

def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive dedupe, merge, diff, and du tool"
    )
    parser.add_argument('--root', default='.', help='Root directory to analyze')
    parser.add_argument('--execute', action='store_true', help='Actually perform operations (default is dry-run)')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Dedupe command
    dedupe_parser = subparsers.add_parser('dedupe', help='Find and remove duplicates')
    dedupe_parser.add_argument('--strategy', choices=['newest', 'oldest', 'largest', 'smallest', 'shortest_path'],
                              default='newest', help='Strategy for choosing which file to keep')
    dedupe_parser.add_argument('--max-size', type=int, default=50, help='Max file size in MB to check')
    dedupe_parser.add_argument('--keep-paths', nargs='+', help='Path patterns to prefer keeping')
    dedupe_parser.add_argument('--execute', action='store_true', help='Actually delete files (default is dry-run)')
    
    # Merge command
    merge_parser = subparsers.add_parser('merge', help='Merge files or directories')
    merge_parser.add_argument('--files', nargs='+', help='Files to merge')
    merge_parser.add_argument('--dirs', nargs='+', help='Directories to merge')
    merge_parser.add_argument('--output', required=True, help='Output path')
    merge_parser.add_argument('--strategy', choices=['concatenate', 'unique_lines', 'overwrite', 'rename'],
                              default='concatenate', help='Merge strategy')
    
    # Diff command
    diff_parser = subparsers.add_parser('diff', help='Compare files or directories')
    diff_parser.add_argument('--files', nargs=2, help='Two files to compare')
    diff_parser.add_argument('--dirs', nargs=2, help='Two directories to compare')
    diff_parser.add_argument('--format', choices=['unified', 'context', 'html'], default='unified')
    diff_parser.add_argument('--output', help='Output file for diff results')
    
    # Du command
    du_parser = subparsers.add_parser('du', help='Show disk usage')
    du_parser.add_argument('--path', help='Path to analyze (default: root)')
    du_parser.add_argument('--depth', type=int, default=3, help='Max depth')
    du_parser.add_argument('--sort', choices=['size', 'files', 'path'], default='size')
    
    # Find duplicates command
    find_parser = subparsers.add_parser('find', help='Find duplicates without removing')
    find_parser.add_argument('--max-size', type=int, default=50, help='Max file size in MB')
    find_parser.add_argument('--report', help='Output report file')
    
    args = parser.parse_args()
    
    # Get root from args or use current directory
    root_dir = getattr(args, 'root', None) or '.'
    tool = DedupeMergeDiffTool(root_dir=root_dir, dry_run=not args.execute)
    
    if args.command == 'dedupe':
        tool.dry_run = not (getattr(args, 'execute', False) or args.execute)
        tool.find_duplicates(max_size_mb=args.max_size)
        tool.dedupe(strategy=args.strategy, keep_paths=getattr(args, 'keep_paths', None))
        tool.generate_report()
    
    elif args.command == 'merge':
        if args.files:
            tool.merge_files(args.files, args.output, args.strategy)
        elif args.dirs:
            tool.merge_directories(args.dirs, args.output, args.strategy)
        else:
            print("Error: Need --files or --dirs")
    
    elif args.command == 'diff':
        if args.files:
            tool.diff_files(args.files[0], args.files[1], args.format)
        elif args.dirs:
            tool.diff_directories(args.dirs[0], args.dirs[1], args.output)
        else:
            print("Error: Need --files or --dirs")
    
    elif args.command == 'du':
        tool.du(path=args.path, max_depth=args.depth, sort_by=args.sort)
    
    elif args.command == 'find':
        tool.find_duplicates(max_size_mb=args.max_size)
        if args.report:
            tool.generate_report(args.report)
        else:
            tool.generate_report()
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
