#!/usr/bin/env python3
"""
Unlimited Depth Folder Search Tool
===================================
Searches through all directories at unlimited depth with various filters and criteria.

Features:
- Search by name pattern (regex supported)
- Search by file type/extension
- Search by size (min/max)
- Search by content (text search in files)
- Search by date (modified/created)
- Search by purpose/category
- Export results to CSV/JSON
- Interactive filtering

Usage:
    python3 unlimited_depth_search.py [options]

Examples:
    # Find all Python files
    python3 unlimited_depth_search.py --type py

    # Find large files (>100MB)
    python3 unlimited_depth_search.py --min-size 100MB

    # Find files containing "revenue"
    python3 unlimited_depth_search.py --content "revenue"

    # Find duplicate directories
    python3 unlimited_depth_search.py --duplicates

    # Find all README files
    python3 unlimited_depth_search.py --pattern "README"

    # Find empty directories
    python3 unlimited_depth_search.py --empty-dirs
"""

import os
import sys
import json
import csv
import re
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Optional, Set, Tuple
import hashlib


class Colors:
    """Terminal colors"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class UnlimitedDepthSearch:
    """Unlimited depth folder search engine"""
    
    def __init__(self, root_path: Path = None, exclude_dirs: Set[str] = None):
        self.root_path = root_path or Path.cwd()
        self.exclude_dirs = exclude_dirs or {
            '.git', '.github', '.history', '__pycache__', 
            'node_modules', '.next', '.venv', 'venv', 'env'
        }
        self.results = []
        self.stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_size': 0,
            'files_by_type': defaultdict(int),
            'dirs_by_depth': defaultdict(int),
            'largest_files': [],
            'largest_dirs': []
        }
    
    def format_size(self, size_bytes: int) -> str:
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    def parse_size(self, size_str: str) -> int:
        """Parse size string (e.g., '100MB') to bytes"""
        size_str = size_str.upper().strip()
        multipliers = {'B': 1, 'KB': 1024, 'MB': 1024**2, 'GB': 1024**3, 'TB': 1024**4}
        
        for unit, multiplier in multipliers.items():
            if size_str.endswith(unit):
                try:
                    return int(float(size_str[:-len(unit)]) * multiplier)
                except ValueError:
                    pass
        # Try parsing as number
        try:
            return int(size_str)
        except ValueError:
            return 0
    
    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded"""
        parts = path.parts
        return any(part in self.exclude_dirs for part in parts)
    
    def get_file_info(self, file_path: Path) -> Dict:
        """Get comprehensive file information"""
        try:
            stat = file_path.stat()
            ext = file_path.suffix.lower()
            
            return {
                'path': str(file_path),
                'name': file_path.name,
                'type': 'file',
                'size': stat.st_size,
                'extension': ext or 'no-ext',
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'depth': len(file_path.parts) - len(self.root_path.parts),
                'parent': str(file_path.parent),
            }
        except (OSError, PermissionError) as e:
            return {
                'path': str(file_path),
                'name': file_path.name,
                'type': 'file',
                'error': str(e)
            }
    
    def get_dir_info(self, dir_path: Path) -> Dict:
        """Get comprehensive directory information"""
        try:
            # Count files and get size
            file_count = 0
            dir_count = 0
            total_size = 0
            
            try:
                for item in dir_path.iterdir():
                    if item.is_file():
                        file_count += 1
                        try:
                            total_size += item.stat().st_size
                        except:
                            pass
                    elif item.is_dir():
                        dir_count += 1
            except (PermissionError, OSError):
                pass
            
            return {
                'path': str(dir_path),
                'name': dir_path.name,
                'type': 'directory',
                'size': total_size,
                'file_count': file_count,
                'dir_count': dir_count,
                'depth': len(dir_path.parts) - len(self.root_path.parts),
                'parent': str(dir_path.parent),
            }
        except (OSError, PermissionError) as e:
            return {
                'path': str(dir_path),
                'name': dir_path.name,
                'type': 'directory',
                'error': str(e)
            }
    
    def search_by_pattern(self, pattern: str, case_sensitive: bool = False) -> List[Dict]:
        """Search files/directories by name pattern (regex)"""
        results = []
        regex = re.compile(pattern, 0 if case_sensitive else re.IGNORECASE)
        
        print(f"{Colors.CYAN}Searching for pattern: {pattern}{Colors.ENDC}")
        
        for root, dirs, files in os.walk(self.root_path):
            root_path = Path(root)
            
            if self.should_exclude(root_path):
                continue
            
            # Search in directory name
            if regex.search(root_path.name):
                dir_info = self.get_dir_info(root_path)
                dir_info['match_type'] = 'directory_name'
                results.append(dir_info)
            
            # Search in file names
            for file in files:
                file_path = root_path / file
                if regex.search(file):
                    file_info = self.get_file_info(file_path)
                    file_info['match_type'] = 'filename'
                    results.append(file_info)
        
        return results
    
    def search_by_type(self, extensions: List[str]) -> List[Dict]:
        """Search files by extension"""
        results = []
        ext_set = {ext.lower().lstrip('.') for ext in extensions}
        
        print(f"{Colors.CYAN}Searching for file types: {', '.join(extensions)}{Colors.ENDC}")
        
        for root, dirs, files in os.walk(self.root_path):
            root_path = Path(root)
            
            if self.should_exclude(root_path):
                continue
            
            for file in files:
                file_path = root_path / file
                ext = file_path.suffix.lower().lstrip('.')
                
                if ext in ext_set or (not ext and 'no-ext' in ext_set):
                    file_info = self.get_file_info(file_path)
                    results.append(file_info)
        
        return results
    
    def search_by_size(self, min_size: Optional[int] = None, max_size: Optional[int] = None) -> List[Dict]:
        """Search files by size range"""
        results = []
        
        size_range = ""
        if min_size:
            size_range += f"min: {self.format_size(min_size)}"
        if max_size:
            if size_range:
                size_range += ", "
            size_range += f"max: {self.format_size(max_size)}"
        
        print(f"{Colors.CYAN}Searching by size: {size_range}{Colors.ENDC}")
        
        for root, dirs, files in os.walk(self.root_path):
            root_path = Path(root)
            
            if self.should_exclude(root_path):
                continue
            
            for file in files:
                file_path = root_path / file
                try:
                    size = file_path.stat().st_size
                    
                    if min_size and size < min_size:
                        continue
                    if max_size and size > max_size:
                        continue
                    
                    file_info = self.get_file_info(file_path)
                    file_info['size_formatted'] = self.format_size(size)
                    results.append(file_info)
                except (OSError, PermissionError):
                    pass
        
        return results
    
    def search_by_content(self, search_text: str, file_extensions: Optional[List[str]] = None, case_sensitive: bool = False) -> List[Dict]:
        """Search for text content in files"""
        results = []
        search_lower = search_text.lower() if not case_sensitive else search_text
        
        print(f"{Colors.CYAN}Searching for content: '{search_text}'{Colors.ENDC}")
        
        for root, dirs, files in os.walk(self.root_path):
            root_path = Path(root)
            
            if self.should_exclude(root_path):
                continue
            
            for file in files:
                file_path = root_path / file
                
                # Filter by extension if specified
                if file_extensions:
                    ext = file_path.suffix.lower().lstrip('.')
                    if ext not in file_extensions and (ext or 'no-ext') not in file_extensions:
                        continue
                
                try:
                    # Try to read as text
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if not case_sensitive:
                            content = content.lower()
                        
                        if search_text in content if case_sensitive else search_lower in content:
                            file_info = self.get_file_info(file_path)
                            # Count occurrences
                            matches = content.count(search_lower)
                            file_info['content_matches'] = matches
                            file_info['search_text'] = search_text
                            results.append(file_info)
                except (UnicodeDecodeError, PermissionError, OSError):
                    # Skip binary files or permission errors
                    pass
        
        return results
    
    def find_duplicates(self, by_name: bool = False, by_content: bool = False) -> Dict[str, List[Dict]]:
        """Find duplicate files (by name or content hash)"""
        duplicates = defaultdict(list)
        
        if by_name:
            print(f"{Colors.CYAN}Finding duplicate file names...{Colors.ENDC}")
            for root, dirs, files in os.walk(self.root_path):
                root_path = Path(root)
                if self.should_exclude(root_path):
                    continue
                
                for file in files:
                    file_path = root_path / file
                    file_info = self.get_file_info(file_path)
                    duplicates[file.lower()].append(file_info)
        
        if by_content:
            print(f"{Colors.CYAN}Finding duplicate file content (hashing)...{Colors.ENDC}")
            content_hashes = defaultdict(list)
            
            for root, dirs, files in os.walk(self.root_path):
                root_path = Path(root)
                if self.should_exclude(root_path):
                    continue
                
                for file in files:
                    file_path = root_path / file
                    try:
                        # Calculate hash for small-medium files only
                        size = file_path.stat().st_size
                        if size > 100 * 1024 * 1024:  # Skip files > 100MB
                            continue
                        
                        with open(file_path, 'rb') as f:
                            file_hash = hashlib.md5(f.read()).hexdigest()
                        
                        file_info = self.get_file_info(file_path)
                        content_hashes[file_hash].append(file_info)
                    except (OSError, PermissionError, MemoryError):
                        pass
            
            # Filter to only duplicates
            for file_hash, files in content_hashes.items():
                if len(files) > 1:
                    duplicates[f"hash_{file_hash[:8]}"] = files
        
        # Filter to only actual duplicates
        return {k: v for k, v in duplicates.items() if len(v) > 1}
    
    def find_empty_dirs(self) -> List[Dict]:
        """Find empty directories"""
        results = []
        
        print(f"{Colors.CYAN}Finding empty directories...{Colors.ENDC}")
        
        for root, dirs, files in os.walk(self.root_path, topdown=False):
            root_path = Path(root)
            
            if self.should_exclude(root_path):
                continue
            
            try:
                items = list(root_path.iterdir())
                if not items:  # Empty directory
                    dir_info = self.get_dir_info(root_path)
                    results.append(dir_info)
            except (PermissionError, OSError):
                pass
        
        return results
    
    def find_large_dirs(self, min_size: int = 100 * 1024 * 1024) -> List[Dict]:
        """Find large directories"""
        results = []
        dir_sizes = {}
        
        print(f"{Colors.CYAN}Finding large directories (> {self.format_size(min_size)})...{Colors.ENDC}")
        
        for root, dirs, files in os.walk(self.root_path):
            root_path = Path(root)
            
            if self.should_exclude(root_path):
                continue
            
            total_size = 0
            try:
                for file in files:
                    file_path = root_path / file
                    try:
                        total_size += file_path.stat().st_size
                    except:
                        pass
            except:
                pass
            
            if total_size >= min_size:
                dir_info = self.get_dir_info(root_path)
                dir_info['size'] = total_size
                dir_info['size_formatted'] = self.format_size(total_size)
                results.append(dir_info)
        
        return sorted(results, key=lambda x: x.get('size', 0), reverse=True)
    
    def analyze_structure(self) -> Dict:
        """Complete structure analysis"""
        print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}Unlimited Depth Structure Analysis{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}\n")
        
        print(f"{Colors.CYAN}Analyzing: {self.root_path}{Colors.ENDC}\n")
        
        max_depth = 0
        depth_stats = defaultdict(int)
        type_stats = defaultdict(int)
        size_stats = defaultdict(int)
        largest_files = []
        largest_dirs = []
        
        for root, dirs, files in os.walk(self.root_path):
            root_path = Path(root)
            
            if self.should_exclude(root_path):
                continue
            
            depth = len(root_path.parts) - len(self.root_path.parts)
            max_depth = max(max_depth, depth)
            depth_stats[depth] += 1
            
            # Analyze files
            for file in files:
                file_path = root_path / file
                try:
                    size = file_path.stat().st_size
                    ext = file_path.suffix.lower().lstrip('.') or 'no-ext'
                    
                    type_stats[ext] += 1
                    size_stats[ext] += size
                    
                    largest_files.append({
                        'path': str(file_path),
                        'size': size,
                        'ext': ext
                    })
                except:
                    pass
            
            # Analyze directories
            try:
                dir_size = sum(
                    (root_path / f).stat().st_size 
                    for f in files 
                    if (root_path / f).is_file()
                )
                if dir_size > 0:
                    largest_dirs.append({
                        'path': str(root_path),
                        'size': dir_size,
                        'file_count': len(files)
                    })
            except:
                pass
        
        # Sort largest
        largest_files.sort(key=lambda x: x['size'], reverse=True)
        largest_dirs.sort(key=lambda x: x['size'], reverse=True)
        
        return {
            'max_depth': max_depth,
            'depth_distribution': dict(depth_stats),
            'file_types': dict(type_stats),
            'type_sizes': {k: self.format_size(v) for k, v in size_stats.items()},
            'largest_files': largest_files[:50],
            'largest_dirs': largest_dirs[:50],
            'total_files': sum(type_stats.values()),
            'total_dirs': sum(depth_stats.values())
        }
    
    def export_results(self, results: List[Dict], output_file: str, format: str = 'json'):
        """Export results to file"""
        if format.lower() == 'json':
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
        elif format.lower() == 'csv':
            if results:
                with open(output_file, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=results[0].keys())
                    writer.writeheader()
                    writer.writerows(results)
        
        print(f"{Colors.GREEN}✅ Results exported to: {output_file}{Colors.ENDC}")
    
    def print_results(self, results: List[Dict], limit: int = 50):
        """Print search results"""
        if not results:
            print(f"{Colors.YELLOW}No results found.{Colors.ENDC}")
            return
        
        print(f"\n{Colors.BOLD}Found {len(results)} results{Colors.ENDC}")
        if len(results) > limit:
            print(f"{Colors.YELLOW}Showing first {limit} results...{Colors.ENDC}\n")
        
        for i, result in enumerate(results[:limit], 1):
            print(f"{Colors.CYAN}[{i}]{Colors.ENDC} {result.get('path', 'N/A')}")
            if 'size' in result:
                size_str = result.get('size_formatted', self.format_size(result['size']))
                print(f"      Size: {size_str}")
            if 'match_type' in result:
                print(f"      Match: {result['match_type']}")
            if 'content_matches' in result:
                print(f"      Matches: {result['content_matches']}")
            print()


def main():
    parser = argparse.ArgumentParser(
        description='Unlimited Depth Folder Search Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('--root', type=str, default='.', help='Root directory to search (default: current directory)')
    parser.add_argument('--pattern', type=str, help='Search pattern (regex) for file/directory names')
    parser.add_argument('--type', type=str, nargs='+', help='File extensions to search (e.g., py js md)')
    parser.add_argument('--min-size', type=str, help='Minimum file size (e.g., 100MB, 1GB)')
    parser.add_argument('--max-size', type=str, help='Maximum file size (e.g., 100MB, 1GB)')
    parser.add_argument('--content', type=str, help='Search for text content in files')
    parser.add_argument('--content-ext', type=str, nargs='+', help='File extensions to search content in')
    parser.add_argument('--duplicates', action='store_true', help='Find duplicate files')
    parser.add_argument('--duplicates-by-content', action='store_true', help='Find duplicate files by content hash')
    parser.add_argument('--empty-dirs', action='store_true', help='Find empty directories')
    parser.add_argument('--large-dirs', type=str, help='Find large directories (min size, e.g., 100MB)')
    parser.add_argument('--analyze', action='store_true', help='Complete structure analysis')
    parser.add_argument('--export', type=str, help='Export results to file')
    parser.add_argument('--format', type=str, choices=['json', 'csv'], default='json', help='Export format')
    parser.add_argument('--limit', type=int, default=50, help='Limit number of results to display')
    parser.add_argument('--case-sensitive', action='store_true', help='Case sensitive search')
    
    args = parser.parse_args()
    
    # Initialize search
    searcher = UnlimitedDepthSearch(root_path=Path(args.root).resolve())
    
    results = []
    
    # Execute searches
    if args.analyze:
        analysis = searcher.analyze_structure()
        print(f"\n{Colors.BOLD}Structure Analysis Results:{Colors.ENDC}\n")
        print(f"Max Depth: {analysis['max_depth']}")
        print(f"Total Files: {analysis['total_files']:,}")
        print(f"Total Directories: {analysis['total_dirs']:,}")
        print(f"\n{Colors.BOLD}Top 10 File Types:{Colors.ENDC}")
        for ext, count in sorted(analysis['file_types'].items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  .{ext}: {count:,} files ({analysis['type_sizes'].get(ext, '0 B')})")
        print(f"\n{Colors.BOLD}Top 10 Largest Files:{Colors.ENDC}")
        for item in analysis['largest_files'][:10]:
            print(f"  {searcher.format_size(item['size']):>12} - {item['path']}")
        print(f"\n{Colors.BOLD}Top 10 Largest Directories:{Colors.ENDC}")
        for item in analysis['largest_dirs'][:10]:
            print(f"  {searcher.format_size(item['size']):>12} - {item['path']} ({item['file_count']} files)")
        
        if args.export:
            searcher.export_results([analysis], args.export, args.format)
        return
    
    if args.pattern:
        results = searcher.search_by_pattern(args.pattern, args.case_sensitive)
    
    if args.type:
        results = searcher.search_by_type(args.type)
    
    if args.min_size or args.max_size:
        min_size = searcher.parse_size(args.min_size) if args.min_size else None
        max_size = searcher.parse_size(args.max_size) if args.max_size else None
        results = searcher.search_by_size(min_size, max_size)
    
    if args.content:
        content_ext = args.content_ext if args.content_ext else None
        results = searcher.search_by_content(args.content, content_ext, args.case_sensitive)
    
    if args.duplicates:
        dupes = searcher.find_duplicates(by_name=True)
        print(f"\n{Colors.BOLD}Found {len(dupes)} duplicate file names:{Colors.ENDC}\n")
        for name, files in list(dupes.items())[:args.limit]:
            print(f"{Colors.YELLOW}{name}{Colors.ENDC} ({len(files)} copies):")
            for f in files[:5]:
                print(f"  - {f['path']}")
            if len(files) > 5:
                print(f"  ... and {len(files) - 5} more")
            print()
        results = [{'name': k, 'copies': len(v), 'files': v} for k, v in dupes.items()]
    
    if args.duplicates_by_content:
        dupes = searcher.find_duplicates(by_content=True)
        print(f"\n{Colors.BOLD}Found {len(dupes)} duplicate content groups:{Colors.ENDC}\n")
        for hash_key, files in list(dupes.items())[:args.limit]:
            print(f"{Colors.YELLOW}{hash_key}{Colors.ENDC} ({len(files)} identical files):")
            for f in files[:5]:
                print(f"  - {f['path']} ({searcher.format_size(f.get('size', 0))})")
            if len(files) > 5:
                print(f"  ... and {len(files) - 5} more")
            print()
        results = [{'hash': k, 'copies': len(v), 'files': v} for k, v in dupes.items()]
    
    if args.empty_dirs:
        results = searcher.find_empty_dirs()
    
    if args.large_dirs:
        min_size = searcher.parse_size(args.large_dirs)
        results = searcher.find_large_dirs(min_size)
    
    # Print results
    if results:
        searcher.print_results(results, args.limit)
        
        # Export if requested
        if args.export:
            searcher.export_results(results, args.export, args.format)
    else:
        print(f"{Colors.YELLOW}No search criteria specified. Use --help for options.{Colors.ENDC}")
        print(f"\n{Colors.CYAN}Quick examples:{Colors.ENDC}")
        print("  python3 unlimited_depth_search.py --analyze")
        print("  python3 unlimited_depth_search.py --type py --limit 20")
        print("  python3 unlimited_depth_search.py --pattern README")
        print("  python3 unlimited_depth_search.py --min-size 100MB")
        print("  python3 unlimited_depth_search.py --content 'revenue' --content-ext py md")
        print("  python3 unlimited_depth_search.py --duplicates")


if __name__ == '__main__':
    main()
