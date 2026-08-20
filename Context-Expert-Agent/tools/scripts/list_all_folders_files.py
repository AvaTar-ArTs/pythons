#!/usr/bin/env python3
"""
List All Folders and Files
==========================
Comprehensive listing of all directories and files in the project
"""

import os
from pathlib import Path
from collections import defaultdict
import json
import argparse
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


class FolderFileLister:
    def __init__(self, root_dir=None, max_depth=None):
        self.root = Path(root_dir) if root_dir else Path.cwd()
        self.max_depth = max_depth
        self.exclude_dirs = {
            '.git', '.github', '.history', '__pycache__', 
            'node_modules', '.next', '.venv', 'venv', 'env',
            '.DS_Store'
        }
        self.stats = {
            'total_dirs': 0,
            'total_files': 0,
            'total_size': 0,
            'dirs_by_depth': defaultdict(int),
            'files_by_type': defaultdict(int),
            'dirs_by_name': defaultdict(list)
        }
    
    def format_size(self, size_bytes):
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    def should_exclude(self, path):
        """Check if path should be excluded"""
        parts = path.parts
        return any(part in self.exclude_dirs for part in parts)
    
    def list_all(self, output_format='tree', output_file=None):
        """List all folders and files"""
        print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}Listing All Folders and Files{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}\n")
        print(f"{Colors.CYAN}Root: {self.root}{Colors.ENDC}\n")
        
        if output_format == 'tree':
            return self._list_tree(output_file)
        elif output_format == 'flat':
            return self._list_flat(output_file)
        elif output_format == 'json':
            return self._list_json(output_file)
        elif output_format == 'csv':
            return self._list_csv(output_file)
    
    def _list_tree(self, output_file=None):
        """List in tree format"""
        lines = []
        lines.append(f"📁 {self.root.name}/")
        lines.append("")
        
        def walk_tree(path, prefix="", depth=0):
            if self.max_depth and depth > self.max_depth:
                return
            
            if self.should_exclude(path):
                return
            
            try:
                items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
                
                for i, item in enumerate(items):
                    is_last = i == len(items) - 1
                    current_prefix = "└── " if is_last else "├── "
                    next_prefix = "    " if is_last else "│   "
                    
                    if item.is_dir():
                        self.stats['total_dirs'] += 1
                        self.stats['dirs_by_depth'][depth] += 1
                        dir_size = self._get_dir_size(item)
                        size_str = self.format_size(dir_size)
                        
                        lines.append(f"{prefix}{current_prefix}{Colors.BLUE}📁 {item.name}/{Colors.ENDC} ({size_str})")
                        walk_tree(item, prefix + next_prefix, depth + 1)
                    else:
                        self.stats['total_files'] += 1
                        try:
                            file_size = item.stat().st_size
                            self.stats['total_size'] += file_size
                            ext = item.suffix.lower() or 'no-ext'
                            self.stats['files_by_type'][ext] += 1
                            size_str = self.format_size(file_size)
                            lines.append(f"{prefix}{current_prefix}{Colors.CYAN}{item.name}{Colors.ENDC} ({size_str})")
                        except:
                            lines.append(f"{prefix}{current_prefix}{item.name}")
            except (PermissionError, OSError):
                pass
        
        walk_tree(self.root)
        
        # Print summary
        lines.append("")
        lines.append(f"{Colors.HEADER}{'='*80}{Colors.ENDC}")
        lines.append(f"{Colors.BOLD}Summary{Colors.ENDC}")
        lines.append(f"{Colors.HEADER}{'='*80}{Colors.ENDC}")
        lines.append(f"Total Directories: {self.stats['total_dirs']}")
        lines.append(f"Total Files: {self.stats['total_files']}")
        lines.append(f"Total Size: {self.format_size(self.stats['total_size'])}")
        lines.append("")
        lines.append(f"{Colors.BOLD}Top 10 File Types:{Colors.ENDC}")
        for ext, count in sorted(self.stats['files_by_type'].items(), key=lambda x: x[1], reverse=True)[:10]:
            lines.append(f"  .{ext}: {count:,} files")
        
        output = '\n'.join(lines)
        print(output)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"\n{Colors.GREEN}✅ Saved to: {output_file}{Colors.ENDC}")
        
        return output
    
    def _list_flat(self, output_file=None):
        """List in flat format (all paths)"""
        all_items = []
        
        def collect_items(path, depth=0):
            if self.max_depth and depth > self.max_depth:
                return
            
            if self.should_exclude(path):
                return
            
            try:
                for item in path.iterdir():
                    if self.should_exclude(item):
                        continue
                    
                    rel_path = item.relative_to(self.root)
                    
                    if item.is_dir():
                        self.stats['total_dirs'] += 1
                        all_items.append({
                            'type': 'directory',
                            'path': str(rel_path),
                            'depth': depth
                        })
                        collect_items(item, depth + 1)
                    else:
                        self.stats['total_files'] += 1
                        try:
                            size = item.stat().st_size
                            self.stats['total_size'] += size
                            ext = item.suffix.lower() or 'no-ext'
                            self.stats['files_by_type'][ext] += 1
                            all_items.append({
                                'type': 'file',
                                'path': str(rel_path),
                                'size': size,
                                'ext': ext,
                                'depth': depth
                            })
                        except:
                            pass
            except (PermissionError, OSError):
                pass
        
        collect_items(self.root)
        
        # Sort by path
        all_items.sort(key=lambda x: x['path'])
        
        # Print
        lines = []
        lines.append(f"{Colors.BOLD}All Folders and Files (Flat List){Colors.ENDC}\n")
        
        for item in all_items:
            if item['type'] == 'directory':
                lines.append(f"{Colors.BLUE}📁 {item['path']}/{Colors.ENDC}")
            else:
                size_str = self.format_size(item['size'])
                lines.append(f"{Colors.CYAN}{item['path']}{Colors.ENDC} ({size_str})")
        
        lines.append("")
        lines.append(f"{Colors.HEADER}{'='*80}{Colors.ENDC}")
        lines.append(f"{Colors.BOLD}Summary{Colors.ENDC}")
        lines.append(f"{Colors.HEADER}{'='*80}{Colors.ENDC}")
        lines.append(f"Total Directories: {self.stats['total_dirs']}")
        lines.append(f"Total Files: {self.stats['total_files']}")
        lines.append(f"Total Size: {self.format_size(self.stats['total_size'])}")
        
        output = '\n'.join(lines)
        print(output)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"\n{Colors.GREEN}✅ Saved to: {output_file}{Colors.ENDC}")
        
        return output
    
    def _list_json(self, output_file=None):
        """List in JSON format"""
        data = {
            'root': str(self.root),
            'generated': datetime.now().isoformat(),
            'directories': [],
            'files': []
        }
        
        def collect_data(path, depth=0):
            if self.max_depth and depth > self.max_depth:
                return
            
            if self.should_exclude(path):
                return
            
            try:
                for item in path.iterdir():
                    if self.should_exclude(item):
                        continue
                    
                    rel_path = item.relative_to(self.root)
                    
                    if item.is_dir():
                        self.stats['total_dirs'] += 1
                        dir_size = self._get_dir_size(item)
                        data['directories'].append({
                            'path': str(rel_path),
                            'depth': depth,
                            'size': dir_size
                        })
                        collect_data(item, depth + 1)
                    else:
                        self.stats['total_files'] += 1
                        try:
                            size = item.stat().st_size
                            self.stats['total_size'] += size
                            ext = item.suffix.lower() or 'no-ext'
                            self.stats['files_by_type'][ext] += 1
                            data['files'].append({
                                'path': str(rel_path),
                                'size': size,
                                'ext': ext,
                                'depth': depth
                            })
                        except:
                            pass
            except (PermissionError, OSError):
                pass
        
        collect_data(self.root)
        
        data['stats'] = {
            'total_dirs': self.stats['total_dirs'],
            'total_files': self.stats['total_files'],
            'total_size': self.stats['total_size'],
            'files_by_type': dict(self.stats['files_by_type'])
        }
        
        output_file = output_file or f"all_folders_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"{Colors.GREEN}✅ JSON saved to: {output_file}{Colors.ENDC}")
        print(f"   Directories: {len(data['directories'])}")
        print(f"   Files: {len(data['files'])}")
        
        return data
    
    def _list_csv(self, output_file=None):
        """List in CSV format"""
        import csv
        
        all_items = []
        
        def collect_items(path, depth=0):
            if self.max_depth and depth > self.max_depth:
                return
            
            if self.should_exclude(path):
                return
            
            try:
                for item in path.iterdir():
                    if self.should_exclude(item):
                        continue
                    
                    rel_path = item.relative_to(self.root)
                    
                    if item.is_dir():
                        self.stats['total_dirs'] += 1
                        dir_size = self._get_dir_size(item)
                        all_items.append({
                            'type': 'directory',
                            'path': str(rel_path),
                            'name': item.name,
                            'size': dir_size,
                            'depth': depth
                        })
                        collect_items(item, depth + 1)
                    else:
                        self.stats['total_files'] += 1
                        try:
                            size = item.stat().st_size
                            self.stats['total_size'] += size
                            ext = item.suffix.lower() or 'no-ext'
                            self.stats['files_by_type'][ext] += 1
                            all_items.append({
                                'type': 'file',
                                'path': str(rel_path),
                                'name': item.name,
                                'size': size,
                                'ext': ext,
                                'depth': depth
                            })
                        except:
                            pass
            except (PermissionError, OSError):
                pass
        
        collect_items(self.root)
        
        output_file = output_file or f"all_folders_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['type', 'path', 'name', 'size', 'ext', 'depth'])
            writer.writeheader()
            for item in sorted(all_items, key=lambda x: x['path']):
                row = item.copy()
                if row['type'] == 'directory':
                    row['ext'] = ''
                writer.writerow(row)
        
        print(f"{Colors.GREEN}✅ CSV saved to: {output_file}{Colors.ENDC}")
        print(f"   Total items: {len(all_items)}")
        
        return all_items
    
    def _get_dir_size(self, path):
        """Get directory size"""
        total = 0
        try:
            for item in path.rglob('*'):
                if item.is_file():
                    try:
                        total += item.stat().st_size
                    except:
                        pass
        except:
            pass
        return total


def main():
    parser = argparse.ArgumentParser(
        description='List all folders and files in the project',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Tree format (default)
  python3 list_all_folders_files.py

  # Flat list
  python3 list_all_folders_files.py --format flat

  # JSON export
  python3 list_all_folders_files.py --format json

  # CSV export
  python3 list_all_folders_files.py --format csv

  # Limit depth
  python3 list_all_folders_files.py --max-depth 3

  # Save to file
  python3 list_all_folders_files.py --output listing.txt
        """
    )
    
    parser.add_argument('--root', default='.', help='Root directory to list')
    parser.add_argument('--format', choices=['tree', 'flat', 'json', 'csv'], 
                       default='tree', help='Output format')
    parser.add_argument('--output', help='Output file')
    parser.add_argument('--max-depth', type=int, help='Maximum depth to traverse')
    
    args = parser.parse_args()
    
    lister = FolderFileLister(root_dir=args.root, max_depth=args.max_depth)
    lister.list_all(output_format=args.format, output_file=args.output)


if __name__ == '__main__':
    main()
