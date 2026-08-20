#!/usr/bin/env python3
"""
Unified Merge, Diff, and Dedupe Tool
====================================
Works with existing dedupe_mapping.csv to merge, diff, and remove duplicates
"""

import os
import sys
import csv
import json
import shutil
import hashlib
import difflib
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class MergeDiffDedupe:
    def __init__(self, root_dir=None, dry_run=True):
        self.root = Path(root_dir) if root_dir else Path.cwd()
        self.dry_run = dry_run
        self.duplicates = []
        self.merge_opportunities = []
        
    def load_dedupe_mapping(self, mapping_file='dedupe_mapping.csv'):
        """Load existing dedupe mapping"""
        if not Path(mapping_file).exists():
            print(f"{Colors.RED}❌ {mapping_file} not found{Colors.ENDC}")
            print(f"   Run dedupe_analysis.py first to generate mapping")
            return False
        
        print(f"{Colors.CYAN}📂 Loading {mapping_file}...{Colors.ENDC}")
        
        with open(mapping_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'REMOVE' in row['action']:
                    self.duplicates.append({
                        'path': row['old_path'],
                        'action': row['action'],
                        'reason': row['reason'],
                        'size_mb': float(row.get('size_mb', 0)),
                        'similarity': row.get('similarity', 'N/A')
                    })
                elif 'MERGE' in row['action']:
                    self.merge_opportunities.append(row)
        
        print(f"   ✅ Found {len(self.duplicates)} items to remove")
        print(f"   ✅ Found {len(self.merge_opportunities)} merge opportunities")
        return True
    
    def show_summary(self):
        """Show summary of duplicates and merge opportunities"""
        if not self.duplicates and not self.merge_opportunities:
            print(f"{Colors.YELLOW}No duplicates or merge opportunities found{Colors.ENDC}")
            return
        
        total_size = sum(d['size_mb'] for d in self.duplicates)
        
        print(f"\n{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}Summary{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}\n")
        
        print(f"{Colors.CYAN}Duplicates to Remove:{Colors.ENDC}")
        print(f"   Count: {len(self.duplicates)}")
        print(f"   Total Size: {total_size:.2f} MB ({total_size/1024:.2f} GB)")
        print(f"   Top 10 by size:")
        
        sorted_dupes = sorted(self.duplicates, key=lambda x: x['size_mb'], reverse=True)
        for i, dup in enumerate(sorted_dupes[:10], 1):
            print(f"      {i}. {dup['path']} ({dup['size_mb']:.2f} MB)")
        
        if self.merge_opportunities:
            print(f"\n{Colors.CYAN}Merge Opportunities:{Colors.ENDC}")
            print(f"   Count: {len(self.merge_opportunities)}")
            print(f"   Top 10:")
            for i, merge in enumerate(self.merge_opportunities[:10], 1):
                print(f"      {i}. {merge['old_path']}")
                print(f"         → {merge.get('reason', 'N/A')}")
    
    def diff_files(self, file1, file2, output_file=None):
        """Compare two files and show differences"""
        path1 = self.root / file1
        path2 = self.root / file2
        
        if not path1.exists():
            print(f"{Colors.RED}❌ File not found: {path1}{Colors.ENDC}")
            return None
        if not path2.exists():
            print(f"{Colors.RED}❌ File not found: {path2}{Colors.ENDC}")
            return None
        
        print(f"\n{Colors.CYAN}🔍 Comparing files...{Colors.ENDC}")
        print(f"   File 1: {path1}")
        print(f"   File 2: {path2}\n")
        
        try:
            with open(path1, 'r', encoding='utf-8', errors='ignore') as f1:
                lines1 = f1.readlines()
            with open(path2, 'r', encoding='utf-8', errors='ignore') as f2:
                lines2 = f2.readlines()
            
            # Check if identical
            if lines1 == lines2:
                print(f"{Colors.GREEN}✅ Files are identical{Colors.ENDC}")
                return {'identical': True, 'diff_lines': 0}
            
            # Generate unified diff
            diff = list(difflib.unified_diff(
                lines1, lines2,
                fromfile=str(path1),
                tofile=str(path2),
                lineterm=''
            ))
            
            print(f"{Colors.YELLOW}⚠️  Files differ ({len(diff)} diff lines){Colors.ENDC}")
            print(f"\n{Colors.BOLD}First 30 differences:{Colors.ENDC}\n")
            
            for line in diff[:30]:
                if line.startswith('+'):
                    print(f"{Colors.GREEN}{line}{Colors.ENDC}")
                elif line.startswith('-'):
                    print(f"{Colors.RED}{line}{Colors.ENDC}")
                elif line.startswith('@'):
                    print(f"{Colors.CYAN}{line}{Colors.ENDC}")
                else:
                    print(line)
            
            if len(diff) > 30:
                print(f"\n{Colors.YELLOW}... ({len(diff) - 30} more lines){Colors.ENDC}")
            
            result = {
                'identical': False,
                'diff_lines': len(diff),
                'diff': diff
            }
            
            if output_file:
                with open(output_file, 'w') as f:
                    f.write('\n'.join(diff))
                print(f"\n{Colors.GREEN}✅ Diff saved to: {output_file}{Colors.ENDC}")
            
            return result
            
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.ENDC}")
            return None
    
    def diff_directories(self, dir1, dir2, output_file=None):
        """Compare two directories with content and parent folder awareness"""
        path1 = self.root / dir1
        path2 = self.root / dir2
        
        if not path1.exists() or not path1.is_dir():
            print(f"{Colors.RED}❌ Directory not found: {path1}{Colors.ENDC}")
            return None
        if not path2.exists() or not path2.is_dir():
            print(f"{Colors.RED}❌ Directory not found: {path2}{Colors.ENDC}")
            return None
        
        print(f"\n{Colors.CYAN}🔍 Comparing directories (Content & Parent Folder Aware)...{Colors.ENDC}")
        print(f"   Dir 1: {path1}")
        print(f"   Dir 2: {path2}")
        
        # Parent folder context
        parent1 = path1.parent.name if path1.parent != self.root else "root"
        parent2 = path2.parent.name if path2.parent != self.root else "root"
        print(f"   Parent 1: {parent1}")
        print(f"   Parent 2: {parent2}\n")
        
        # Get all files with full context
        files1 = {}
        files2 = {}
        
        for f in path1.rglob('*'):
            if f.is_file():
                rel_path = f.relative_to(path1)
                files1[rel_path] = {
                    'path': f,
                    'full_path': str(f),
                    'parent': f.parent.name,
                    'size': f.stat().st_size,
                    'mtime': f.stat().st_mtime
                }
        
        for f in path2.rglob('*'):
            if f.is_file():
                rel_path = f.relative_to(path2)
                files2[rel_path] = {
                    'path': f,
                    'full_path': str(f),
                    'parent': f.parent.name,
                    'size': f.stat().st_size,
                    'mtime': f.stat().st_mtime
                }
        
        only_in_1 = set(files1.keys()) - set(files2.keys())
        only_in_2 = set(files2.keys()) - set(files1.keys())
        in_both = set(files1.keys()) & set(files2.keys())
        
        # Content-aware comparison
        identical = []
        different = []
        different_by_size = []
        different_by_content = []
        similar_content = []
        
        print(f"{Colors.CYAN}Analyzing file contents...{Colors.ENDC}\n")
        
        for rel_path in in_both:
            file1_info = files1[rel_path]
            file2_info = files2[rel_path]
            
            # Size comparison
            size_diff = abs(file1_info['size'] - file2_info['size'])
            
            # Content hash comparison
            hash1 = self._file_hash(file1_info['path'])
            hash2 = self._file_hash(file2_info['path'])
            
            if hash1 == hash2 and hash1 is not None:
                identical.append({
                    'path': str(rel_path),
                    'size': file1_info['size'],
                    'parent': file1_info['parent']
                })
            elif hash1 is None or hash2 is None:
                # Binary or unreadable files - compare by size
                if size_diff == 0:
                    identical.append({
                        'path': str(rel_path),
                        'size': file1_info['size'],
                        'parent': file1_info['parent'],
                        'note': 'binary/identical size'
                    })
                else:
                    different_by_size.append({
                        'path': str(rel_path),
                        'size1': file1_info['size'],
                        'size2': file2_info['size'],
                        'diff': size_diff,
                        'parent': file1_info['parent']
                    })
            else:
                # Different content - analyze similarity
                similarity = self._content_similarity(file1_info['path'], file2_info['path'])
                if similarity > 0.8:
                    similar_content.append({
                        'path': str(rel_path),
                        'similarity': similarity,
                        'parent': file1_info['parent']
                    })
                else:
                    different_by_content.append({
                        'path': str(rel_path),
                        'similarity': similarity,
                        'parent': file1_info['parent']
                    })
                different.append(str(rel_path))
        
        # Group files by parent folder for context
        only_in_1_by_parent = defaultdict(list)
        only_in_2_by_parent = defaultdict(list)
        
        for rel_path in only_in_1:
            parent = files1[rel_path]['parent']
            only_in_1_by_parent[parent].append({
                'path': str(rel_path),
                'size': files1[rel_path]['size']
            })
        
        for rel_path in only_in_2:
            parent = files2[rel_path]['parent']
            only_in_2_by_parent[parent].append({
                'path': str(rel_path),
                'size': files2[rel_path]['size']
            })
        
        # Print comprehensive results
        print(f"{Colors.BOLD}{'='*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}Comparison Results:{Colors.ENDC}")
        print(f"{Colors.BOLD}{'='*80}{Colors.ENDC}\n")
        
        print(f"{Colors.GREEN}✅ Files in both (identical): {len(identical)}{Colors.ENDC}")
        print(f"{Colors.YELLOW}⚠️  Files only in {path1.name}: {len(only_in_1)}{Colors.ENDC}")
        print(f"{Colors.YELLOW}⚠️  Files only in {path2.name}: {len(only_in_2)}{Colors.ENDC}")
        print(f"{Colors.RED}❌ Files in both (different): {len(different)}{Colors.ENDC}")
        if similar_content:
            print(f"{Colors.CYAN}📊 Files with similar content (>80%): {len(similar_content)}{Colors.ENDC}")
        if different_by_size:
            print(f"{Colors.YELLOW}📏 Files different by size only: {len(different_by_size)}{Colors.ENDC}")
        
        # Show identical files summary
        if identical:
            total_identical_size = sum(f['size'] for f in identical) / (1024**2)
            print(f"\n{Colors.GREEN}Identical Files Summary:{Colors.ENDC}")
            print(f"   Total size: {total_identical_size:.2f} MB")
            print(f"   Sample files:")
            for f in identical[:5]:
                print(f"      {f['path']} ({f['size']/1024:.1f} KB) [parent: {f['parent']}]")
            if len(identical) > 5:
                print(f"      ... ({len(identical) - 5} more)")
        
        # Show files only in dir1 (grouped by parent)
        if only_in_1_by_parent:
            print(f"\n{Colors.YELLOW}Files only in {path1.name} (by parent folder):{Colors.ENDC}")
            for parent, files in sorted(only_in_1_by_parent.items()):
                total_size = sum(f['size'] for f in files) / (1024**2)
                print(f"   📁 {parent}/ ({len(files)} files, {total_size:.2f} MB):")
                for f in files[:3]:
                    print(f"      {f['path']} ({f['size']/1024:.1f} KB)")
                if len(files) > 3:
                    print(f"      ... ({len(files) - 3} more)")
        
        # Show files only in dir2 (grouped by parent)
        if only_in_2_by_parent:
            print(f"\n{Colors.YELLOW}Files only in {path2.name} (by parent folder):{Colors.ENDC}")
            for parent, files in sorted(only_in_2_by_parent.items()):
                total_size = sum(f['size'] for f in files) / (1024**2)
                print(f"   📁 {parent}/ ({len(files)} files, {total_size:.2f} MB):")
                for f in files[:3]:
                    print(f"      {f['path']} ({f['size']/1024:.1f} KB)")
                if len(files) > 3:
                    print(f"      ... ({len(files) - 3} more)")
        
        # Show similar content files
        if similar_content:
            print(f"\n{Colors.CYAN}Files with similar content (>80% match):{Colors.ENDC}")
            for f in sorted(similar_content, key=lambda x: x['similarity'], reverse=True)[:10]:
                print(f"   {f['path']} ({f['similarity']*100:.1f}% similar) [parent: {f['parent']}]")
            if len(similar_content) > 10:
                print(f"   ... ({len(similar_content) - 10} more)")
        
        # Show different files
        if different_by_content:
            print(f"\n{Colors.RED}Files with different content:{Colors.ENDC}")
            for f in different_by_content[:10]:
                print(f"   {f['path']} ({f['similarity']*100:.1f}% similar) [parent: {f['parent']}]")
            if len(different_by_content) > 10:
                print(f"   ... ({len(different_by_content) - 10} more)")
        
        if different_by_size:
            print(f"\n{Colors.YELLOW}Files different by size:{Colors.ENDC}")
            for f in sorted(different_by_size, key=lambda x: x['diff'], reverse=True)[:10]:
                size_diff_mb = f['diff'] / (1024**2)
                print(f"   {f['path']} (diff: {size_diff_mb:.2f} MB) [parent: {f['parent']}]")
            if len(different_by_size) > 10:
                print(f"   ... ({len(different_by_size) - 10} more)")
        
        # Summary statistics
        total_size1 = sum(f['size'] for f in files1.values()) / (1024**2)
        total_size2 = sum(f['size'] for f in files2.values()) / (1024**2)
        
        print(f"\n{Colors.BOLD}{'='*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}Summary Statistics:{Colors.ENDC}")
        print(f"{Colors.BOLD}{'='*80}{Colors.ENDC}")
        print(f"   {path1.name}: {len(files1)} files, {total_size1:.2f} MB")
        print(f"   {path2.name}: {len(files2)} files, {total_size2:.2f} MB")
        print(f"   Size difference: {abs(total_size1 - total_size2):.2f} MB")
        print(f"   Identical content: {len(identical)} files")
        print(f"   Merge potential: {len(only_in_1) + len(only_in_2)} unique files could be merged")
        
        result = {
            'only_in_1': [str(f) for f in only_in_1],
            'only_in_2': [str(f) for f in only_in_2],
            'identical': [f['path'] for f in identical],
            'different': different,
            'similar_content': [f['path'] for f in similar_content],
            'different_by_size': [f['path'] for f in different_by_size],
            'only_in_1_by_parent': {k: [f['path'] for f in v] for k, v in only_in_1_by_parent.items()},
            'only_in_2_by_parent': {k: [f['path'] for f in v] for k, v in only_in_2_by_parent.items()},
            'stats': {
                'total_files_1': len(files1),
                'total_files_2': len(files2),
                'total_size_1_mb': total_size1,
                'total_size_2_mb': total_size2,
                'identical_count': len(identical),
                'different_count': len(different),
                'similar_count': len(similar_content)
            }
        }
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n{Colors.GREEN}✅ Results saved to: {output_file}{Colors.ENDC}")
        
        return result
    
    def _content_similarity(self, file1, file2):
        """Calculate content similarity between two text files"""
        try:
            with open(file1, 'r', encoding='utf-8', errors='ignore') as f1:
                content1 = f1.read()
            with open(file2, 'r', encoding='utf-8', errors='ignore') as f2:
                content2 = f2.read()
            
            # Use SequenceMatcher for similarity
            from difflib import SequenceMatcher
            return SequenceMatcher(None, content1, content2).ratio()
        except:
            return 0.0
    
    def _file_hash(self, filepath):
        """Calculate file hash"""
        try:
            hash_md5 = hashlib.md5()
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return None
    
    def merge_files(self, files, output_path, strategy='concatenate'):
        """Merge multiple files into one"""
        if len(files) < 2:
            print(f"{Colors.RED}❌ Need at least 2 files to merge{Colors.ENDC}")
            return False
        
        print(f"\n{Colors.CYAN}🔀 Merging {len(files)} files...{Colors.ENDC}")
        print(f"   Strategy: {strategy}")
        print(f"   Output: {output_path}\n")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}[DRY RUN] Would merge:{Colors.ENDC}")
            for f in files:
                print(f"   - {f}")
            return True
        
        try:
            output = self.root / output_path
            output.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output, 'w', encoding='utf-8') as outfile:
                for i, file_path in enumerate(files):
                    path = self.root / file_path
                    if not path.exists():
                        print(f"{Colors.YELLOW}⚠️  Skipping {path} (not found){Colors.ENDC}")
                        continue
                    
                    print(f"   📄 Merging: {path.name}")
                    
                    if strategy == 'concatenate':
                        with open(path, 'r', encoding='utf-8', errors='ignore') as infile:
                            if i > 0:
                                outfile.write('\n' + '='*80 + '\n')
                                outfile.write(f"# From: {path.name}\n")
                                outfile.write('='*80 + '\n\n')
                            outfile.write(infile.read())
                    
                    elif strategy == 'unique_lines':
                        seen = set()
                        with open(path, 'r', encoding='utf-8', errors='ignore') as infile:
                            for line in infile:
                                if line not in seen:
                                    seen.add(line)
                                    outfile.write(line)
            
            print(f"\n{Colors.GREEN}✅ Merged files saved to: {output}{Colors.ENDC}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.ENDC}")
            return False
    
    def dedupe(self, limit=None, min_size_mb=0):
        """Remove duplicate files based on dedupe_mapping.csv"""
        if not self.duplicates:
            print(f"{Colors.YELLOW}No duplicates found. Load dedupe_mapping.csv first.{Colors.ENDC}")
            return
        
        # Filter by size
        filtered = [d for d in self.duplicates if d['size_mb'] >= min_size_mb]
        
        if limit:
            filtered = filtered[:limit]
        
        total_size = sum(d['size_mb'] for d in filtered)
        
        print(f"\n{Colors.CYAN}🗑️  Deduplicating...{Colors.ENDC}")
        print(f"   Items to remove: {len(filtered)}")
        print(f"   Total size: {total_size:.2f} MB ({total_size/1024:.2f} GB)")
        print(f"   Mode: {'DRY RUN' if self.dry_run else 'EXECUTE'}\n")
        
        if not self.dry_run:
            response = input(f"{Colors.RED}⚠️  Are you sure? Type 'yes' to continue: {Colors.ENDC}")
            if response.lower() != 'yes':
                print(f"{Colors.YELLOW}Aborted.{Colors.ENDC}")
                return
        
        removed = []
        errors = []
        saved_space = 0
        
        for dup in sorted(filtered, key=lambda x: x['size_mb'], reverse=True):
            path = self.root / dup['path']
            
            if not path.exists():
                print(f"{Colors.YELLOW}⚠️  {dup['path']} (not found, skipping){Colors.ENDC}")
                continue
            
            print(f"   🗑️  {dup['path']} ({dup['size_mb']:.2f} MB)")
            
            if not self.dry_run:
                try:
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
                    removed.append(dup['path'])
                    saved_space += dup['size_mb']
                except Exception as e:
                    errors.append((dup['path'], str(e)))
                    print(f"      {Colors.RED}❌ Error: {e}{Colors.ENDC}")
        
        print(f"\n{Colors.GREEN}✅ Summary:{Colors.ENDC}")
        print(f"   Removed: {len(removed)}")
        print(f"   Errors: {len(errors)}")
        if not self.dry_run:
            print(f"   Space saved: {saved_space:.2f} MB ({saved_space/1024:.2f} GB)")
        
        if errors:
            print(f"\n{Colors.RED}Errors:{Colors.ENDC}")
            for path, error in errors:
                print(f"   {path}: {error}")
        
        return removed, saved_space


def main():
    parser = argparse.ArgumentParser(
        description='Unified Merge, Diff, and Dedupe Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show summary of duplicates
  python3 merge_diff_dedupe.py summary

  # Diff two files
  python3 merge_diff_dedupe.py diff --files file1.py file2.py

  # Diff two directories
  python3 merge_diff_dedupe.py diff --dirs dir1/ dir2/

  # Merge files
  python3 merge_diff_dedupe.py merge --files file1.txt file2.txt --output merged.txt

  # Remove duplicates (dry run)
  python3 merge_diff_dedupe.py dedupe

  # Remove duplicates (execute)
  python3 merge_diff_dedupe.py dedupe --execute

  # Remove only large duplicates (>10MB)
  python3 merge_diff_dedupe.py dedupe --min-size 10 --execute
        """
    )
    
    parser.add_argument('--root', default='.', help='Root directory')
    parser.add_argument('--mapping', default='dedupe_mapping.csv', help='Dedupe mapping file')
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Show summary of duplicates')
    
    # Diff command
    diff_parser = subparsers.add_parser('diff', help='Compare files or directories')
    diff_parser.add_argument('--files', nargs=2, help='Two files to compare')
    diff_parser.add_argument('--dirs', nargs=2, help='Two directories to compare')
    diff_parser.add_argument('--output', help='Output file for diff results')
    
    # Merge command
    merge_parser = subparsers.add_parser('merge', help='Merge files')
    merge_parser.add_argument('--files', nargs='+', required=True, help='Files to merge')
    merge_parser.add_argument('--output', required=True, help='Output file')
    merge_parser.add_argument('--strategy', choices=['concatenate', 'unique_lines'], default='concatenate')
    
    # Dedupe command
    dedupe_parser = subparsers.add_parser('dedupe', help='Remove duplicates')
    dedupe_parser.add_argument('--execute', action='store_true', help='Actually remove (default is dry-run)')
    dedupe_parser.add_argument('--limit', type=int, help='Limit number of items to remove')
    dedupe_parser.add_argument('--min-size', type=float, default=0, help='Minimum size in MB')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Determine dry_run based on command
    execute = getattr(args, 'execute', False)
    tool = MergeDiffDedupe(root_dir=args.root, dry_run=not execute)
    
    if args.command == 'summary':
        if tool.load_dedupe_mapping(args.mapping):
            tool.show_summary()
    
    elif args.command == 'diff':
        if args.files:
            tool.diff_files(args.files[0], args.files[1], args.output)
        elif args.dirs:
            tool.diff_directories(args.dirs[0], args.dirs[1], args.output)
        else:
            print(f"{Colors.RED}Error: Need --files or --dirs{Colors.ENDC}")
    
    elif args.command == 'merge':
        tool.merge_files(args.files, args.output, args.strategy)
    
    elif args.command == 'dedupe':
        tool.dry_run = not args.execute
        if tool.load_dedupe_mapping(args.mapping):
            tool.dedupe(limit=args.limit, min_size_mb=args.min_size)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
