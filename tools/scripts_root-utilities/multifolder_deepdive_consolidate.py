#!/usr/bin/env python3
"""
Multifolder Deep Dive & Consolidation Analyzer
Scans multiple folders at unlimited depth, identifies duplicates, scattered files,
and provides consolidation recommendations with actionable plans.
"""

import os
import hashlib
import csv
import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Tuple, Set
import subprocess

class MultifolderDeepDive:
    """Deep dive analysis across multiple folders with consolidation recommendations."""
    
    def __init__(self, target_dirs: List[str] = None, max_depth: int = None):
        """
        Initialize deep dive analyzer.
        
        Args:
            target_dirs: List of directories to scan (defaults to AVATARARTS workspace)
            max_depth: Maximum depth to scan (None = unlimited)
        """
        self.workspace_root = Path("/Users/steven/AVATARARTS")
        self.target_dirs = target_dirs or [str(self.workspace_root)]
        self.max_depth = max_depth  # None = unlimited depth
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Statistics
        self.stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_size': 0,
            'by_extension': Counter(),
            'by_directory': defaultdict(lambda: {'count': 0, 'size': 0, 'depth': 0}),
            'duplicates': defaultdict(list),  # hash -> [filepaths]
            'scattered_files': defaultdict(list),  # filename -> [filepaths]
            'large_files': [],
            'empty_dirs': [],
            'nested_projects': [],
            'consolidation_opportunities': []
        }
        
        # Exclude patterns
        self.exclude_patterns = [
            'node_modules', '.git', '__pycache__', '.venv', 'venv',
            '.next', 'dist', 'build', '.cache', 'Library', 'System',
            '.DS_Store', '.pytest_cache', '.mypy_cache', '.tox',
            '*.pyc', '*.pyo', '*.egg-info'
        ]
    
    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded from analysis."""
        path_str = str(path)
        path_parts = path.parts
        
        # Check exclude patterns
        for pattern in self.exclude_patterns:
            if pattern in path_str or any(pattern in part for part in path_parts):
                return True
        
        # Exclude hidden files/dirs (except .env files which might be important)
        if path.name.startswith('.') and path.name not in ['.env', '.env.d']:
            return True
        
        return False
    
    def calculate_file_hash(self, filepath: Path, max_size: int = 50 * 1024 * 1024) -> str:
        """Calculate MD5 hash for file (skip very large files)."""
        try:
            size = filepath.stat().st_size
            if size > max_size:
                return f"LARGE_{size}"  # Use size as identifier for large files
            
            # For smaller files, calculate hash
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return None
    
    def get_dir_size(self, path: Path) -> int:
        """Get directory size using du command (faster for large dirs)."""
        try:
            result = subprocess.run(
                ['du', '-sk', str(path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return int(result.stdout.split()[0]) * 1024
        except:
            pass
        
        # Fallback: manual calculation
        total = 0
        try:
            for item in path.rglob('*'):
                if item.is_file():
                    total += item.stat().st_size
        except:
            pass
        return total
    
    def scan_directory(self, path: Path, current_depth: int = 0, parent_path: str = ""):
        """
        Recursively scan directory at unlimited depth.
        
        Args:
            path: Directory to scan
            current_depth: Current depth level
            parent_path: Parent directory path for tracking
        """
        if self.should_exclude(path):
            return
        
        # Check depth limit
        if self.max_depth is not None and current_depth > self.max_depth:
            return
        
        try:
            # Process directory
            if path.is_dir():
                self.stats['total_dirs'] += 1
                
                # Calculate depth
                rel_path = str(path.relative_to(self.workspace_root)) if path.is_relative_to(self.workspace_root) else str(path)
                depth = len(Path(rel_path).parts)
                
                # Track directory stats
                dir_key = str(path.relative_to(self.workspace_root)) if path.is_relative_to(self.workspace_root) else str(path)
                if dir_key not in self.stats['by_directory']:
                    self.stats['by_directory'][dir_key] = {'count': 0, 'size': 0, 'depth': depth}
                
                # Check for empty directory
                try:
                    if not any(path.iterdir()):
                        self.stats['empty_dirs'].append({
                            'path': str(path.relative_to(self.workspace_root)) if path.is_relative_to(self.workspace_root) else str(path),
                            'depth': depth
                        })
                except:
                    pass
                
                # Detect nested projects
                project_indicators = ['.git', 'package.json', 'setup.py', 'pyproject.toml', 'requirements.txt']
                has_project = any((path / indicator).exists() for indicator in project_indicators)
                if has_project and depth > 2:
                    self.stats['nested_projects'].append({
                        'path': str(path.relative_to(self.workspace_root)) if path.is_relative_to(self.workspace_root) else str(path),
                        'depth': depth
                    })
            
            # Process files
            for item in path.iterdir():
                if self.should_exclude(item):
                    continue
                
                try:
                    if item.is_file():
                        self._process_file(item, current_depth)
                    elif item.is_dir() and (self.max_depth is None or current_depth < self.max_depth):
                        # Recurse into subdirectories
                        self.scan_directory(item, current_depth + 1, str(path))
                
                except (PermissionError, OSError):
                    continue
                except Exception as e:
                    continue
        
        except (PermissionError, OSError):
            pass
        except Exception as e:
            pass
    
    def _process_file(self, filepath: Path, depth: int):
        """Process a single file and collect statistics."""
        try:
            stat = filepath.stat()
            size = stat.st_size
            
            self.stats['total_files'] += 1
            self.stats['total_size'] += size
            
            # Extension tracking
            ext = filepath.suffix.lower() or '(no extension)'
            self.stats['by_extension'][ext] += 1
            
            # Directory tracking
            rel_path = str(filepath.relative_to(self.workspace_root)) if filepath.is_relative_to(self.workspace_root) else str(filepath)
            dir_key = str(filepath.parent.relative_to(self.workspace_root)) if filepath.is_relative_to(self.workspace_root) else str(filepath.parent)
            
            if dir_key not in self.stats['by_directory']:
                self.stats['by_directory'][dir_key] = {'count': 0, 'size': 0, 'depth': depth}
            
            self.stats['by_directory'][dir_key]['count'] += 1
            self.stats['by_directory'][dir_key]['size'] += size
            
            # Large files
            if size > 100 * 1024 * 1024:  # > 100MB
                self.stats['large_files'].append({
                    'path': rel_path,
                    'size': size,
                    'size_mb': size / (1024 * 1024),
                    'depth': depth
                })
            
            # Duplicate detection (hash-based)
            file_hash = self.calculate_file_hash(filepath)
            if file_hash:
                self.stats['duplicates'][file_hash].append({
                    'path': rel_path,
                    'full_path': str(filepath),
                    'size': size,
                    'depth': depth,
                    'modified': stat.st_mtime
                })
            
            # Scattered files (same filename in different locations)
            filename = filepath.name
            self.stats['scattered_files'][filename].append({
                'path': rel_path,
                'full_path': str(filepath),
                'size': size,
                'depth': depth,
                'directory': dir_key,
                'modified': stat.st_mtime
            })
        
        except Exception:
            pass
    
    def analyze_duplicates(self) -> Dict:
        """Analyze duplicate files and create consolidation plan."""
        duplicate_groups = {}
        total_waste = 0
        
        for file_hash, files in self.stats['duplicates'].items():
            if len(files) > 1:
                # Sort by path (prefer files in main workspace root)
                files_sorted = sorted(files, key=lambda x: (
                    not x['path'].startswith('AVATARARTS/'),
                    x['depth'],
                    x['modified']
                ))
                
                keep_file = files_sorted[0]
                duplicates = files_sorted[1:]
                
                waste_size = sum(f['size'] for f in duplicates)
                total_waste += waste_size
                
                duplicate_groups[file_hash] = {
                    'keep': keep_file,
                    'duplicates': duplicates,
                    'count': len(duplicates),
                    'waste_mb': waste_size / (1024 * 1024),
                    'filename': Path(keep_file['path']).name
                }
        
        return {
            'groups': duplicate_groups,
            'total_groups': len(duplicate_groups),
            'total_duplicates': sum(g['count'] for g in duplicate_groups.values()),
            'total_waste_mb': total_waste / (1024 * 1024),
            'total_waste_gb': total_waste / (1024 * 1024 * 1024)
        }
    
    def analyze_scattered_files(self) -> Dict:
        """Analyze scattered files (same filename in multiple locations)."""
        scattered_groups = {}
        
        for filename, files in self.stats['scattered_files'].items():
            if len(files) > 1:
                # Group by directory to find patterns
                dir_groups = defaultdict(list)
                for f in files:
                    dir_groups[f['directory']].append(f)
                
                # Determine if files are truly scattered or just in subdirs
                unique_dirs = len(dir_groups)
                if unique_dirs > 1:
                    # Sort by depth and modification time
                    files_sorted = sorted(files, key=lambda x: (x['depth'], -x['modified']))
                    
                    scattered_groups[filename] = {
                        'locations': files,
                        'unique_directories': unique_dirs,
                        'count': len(files),
                        'total_size_mb': sum(f['size'] for f in files) / (1024 * 1024),
                        'recommended_location': files_sorted[0]['directory'],
                        'scatter_score': unique_dirs * len(files)  # Higher = more scattered
                    }
        
        # Sort by scatter score
        sorted_scattered = sorted(
            scattered_groups.items(),
            key=lambda x: x[1]['scatter_score'],
            reverse=True
        )
        
        return {
            'groups': dict(sorted_scattered),
            'total_files': len(scattered_groups),
            'total_locations': sum(g['count'] for g in scattered_groups.values())
        }
    
    def identify_consolidation_opportunities(self) -> List[Dict]:
        """Identify folders and files that should be consolidated."""
        opportunities = []
        
        # 1. Deep nested directories that could be flattened
        deep_dirs = [
            (dir_path, stats) for dir_path, stats in self.stats['by_directory'].items()
            if stats['depth'] > 5 and stats['count'] < 10
        ]
        
        for dir_path, stats in sorted(deep_dirs, key=lambda x: x[1]['depth'], reverse=True)[:20]:
            opportunities.append({
                'type': 'Deep Nested Directory',
                'path': dir_path,
                'depth': stats['depth'],
                'file_count': stats['count'],
                'recommendation': f"Consider flattening: {dir_path} (depth {stats['depth']}, only {stats['count']} files)"
            })
        
        # 2. Directories with many small files that could be consolidated
        small_file_dirs = [
            (dir_path, stats) for dir_path, stats in self.stats['by_directory'].items()
            if stats['count'] > 20 and (stats['size'] / stats['count']) < 10 * 1024  # Avg < 10KB per file
        ]
        
        for dir_path, stats in sorted(small_file_dirs, key=lambda x: x[1]['count'], reverse=True)[:10]:
            opportunities.append({
                'type': 'Many Small Files',
                'path': dir_path,
                'file_count': stats['count'],
                'avg_size_kb': (stats['size'] / stats['count']) / 1024,
                'recommendation': f"Consider consolidating {stats['count']} small files in {dir_path}"
            })
        
        # 3. Empty directories
        if self.stats['empty_dirs']:
            opportunities.append({
                'type': 'Empty Directories',
                'count': len(self.stats['empty_dirs']),
                'paths': [d['path'] for d in self.stats['empty_dirs'][:10]],
                'recommendation': f"Remove {len(self.stats['empty_dirs'])} empty directories"
            })
        
        # 4. Nested projects that could be moved
        if self.stats['nested_projects']:
            opportunities.append({
                'type': 'Nested Projects',
                'count': len(self.stats['nested_projects']),
                'paths': [p['path'] for p in self.stats['nested_projects'][:10]],
                'recommendation': f"Consider moving {len(self.stats['nested_projects'])} nested projects to root level"
            })
        
        return opportunities
    
    def run_analysis(self):
        """Run comprehensive deep dive analysis."""
        print("=" * 80)
        print("MULTIFOLDER DEEP DIVE & CONSOLIDATION ANALYSIS")
        print("=" * 80)
        print(f"Target directories: {', '.join(self.target_dirs)}")
        print(f"Max depth: {'Unlimited' if self.max_depth is None else self.max_depth}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Scan all target directories
        for target_dir in self.target_dirs:
            target_path = Path(target_dir)
            if not target_path.exists():
                print(f"⚠️  Skipping non-existent directory: {target_dir}")
                continue
            
            print(f"📂 Scanning: {target_dir}")
            self.scan_directory(target_path, current_depth=0)
        
        # Filter duplicates (only groups with 2+ files)
        self.stats['duplicates'] = {
            k: v for k, v in self.stats['duplicates'].items() if len(v) > 1
        }
        
        # Filter scattered files (only files with 2+ locations)
        self.stats['scattered_files'] = {
            k: v for k, v in self.stats['scattered_files'].items() if len(v) > 1
        }
        
        # Sort large files
        self.stats['large_files'].sort(key=lambda x: x['size'], reverse=True)
        
        print(f"\n✅ Scan complete!")
        print(f"   Files: {self.stats['total_files']:,}")
        print(f"   Directories: {self.stats['total_dirs']:,}")
        print(f"   Total size: {self.stats['total_size'] / (1024**3):.2f} GB")
        print(f"   Duplicate groups: {len(self.stats['duplicates'])}")
        print(f"   Scattered files: {len(self.stats['scattered_files'])}")
    
    def generate_reports(self):
        """Generate comprehensive CSV and markdown reports."""
        print("\n📝 Generating reports...")
        
        # Analyze duplicates
        duplicate_analysis = self.analyze_duplicates()
        
        # Analyze scattered files
        scattered_analysis = self.analyze_scattered_files()
        
        # Identify consolidation opportunities
        consolidation_ops = self.identify_consolidation_opportunities()
        
        # Generate CSV reports
        self._generate_csv_reports(duplicate_analysis, scattered_analysis, consolidation_ops)
        
        # Generate markdown report
        self._generate_markdown_report(duplicate_analysis, scattered_analysis, consolidation_ops)
        
        print("✅ Reports generated!")
    
    def _generate_csv_reports(self, duplicate_analysis, scattered_analysis, consolidation_ops):
        """Generate CSV reports."""
        base_name = f"MULTIFOLDER_DEEPDIVE_{self.timestamp}"
        
        # 1. Main inventory CSV
        inventory_csv = self.workspace_root / f"{base_name}_INVENTORY.csv"
        with open(inventory_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Directory', 'File Count', 'Size (bytes)', 'Size (GB)', 'Depth'])
            
            for dir_path, stats in sorted(
                self.stats['by_directory'].items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )[:1000]:  # Top 1000 directories
                writer.writerow([
                    dir_path,
                    stats['count'],
                    stats['size'],
                    f"{stats['size'] / (1024**3):.2f}",
                    stats['depth']
                ])
        
        print(f"   📄 Inventory CSV: {inventory_csv}")
        
        # 2. Duplicates CSV
        if duplicate_analysis['groups']:
            duplicates_csv = self.workspace_root / f"{base_name}_DUPLICATES.csv"
            with open(duplicates_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Filename', 'Keep Path', 'Duplicate Path', 'Size (MB)',
                    'Depth', 'Waste (MB)', 'Action'
                ])
                
                for file_hash, group in duplicate_analysis['groups'].items():
                    keep = group['keep']
                    for dup in group['duplicates']:
                        writer.writerow([
                            group['filename'],
                            keep['path'],
                            dup['path'],
                            f"{dup['size'] / (1024*1024):.2f}",
                            dup['depth'],
                            f"{group['waste_mb']:.2f}",
                            'DELETE'
                        ])
            
            print(f"   📄 Duplicates CSV: {duplicates_csv}")
        
        # 3. Scattered files CSV
        if scattered_analysis['groups']:
            scattered_csv = self.workspace_root / f"{base_name}_SCATTERED.csv"
            with open(scattered_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Filename', 'Location Path', 'Directory', 'Size (MB)',
                    'Depth', 'Scatter Score', 'Recommended Location'
                ])
                
                for filename, group in list(scattered_analysis['groups'].items())[:500]:
                    for location in group['locations']:
                        writer.writerow([
                            filename,
                            location['path'],
                            location['directory'],
                            f"{location['size'] / (1024*1024):.2f}",
                            location['depth'],
                            group['scatter_score'],
                            group['recommended_location']
                        ])
            
            print(f"   📄 Scattered Files CSV: {scattered_csv}")
        
        # 4. Consolidation opportunities CSV
        if consolidation_ops:
            consolidation_csv = self.workspace_root / f"{base_name}_CONSOLIDATION.csv"
            with open(consolidation_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Type', 'Path/Details', 'Recommendation'])
                
                for opp in consolidation_ops:
                    if opp['type'] == 'Empty Directories':
                        writer.writerow([
                            opp['type'],
                            f"{opp['count']} directories",
                            opp['recommendation']
                        ])
                    elif opp['type'] == 'Nested Projects':
                        writer.writerow([
                            opp['type'],
                            f"{opp['count']} projects",
                            opp['recommendation']
                        ])
                    else:
                        writer.writerow([
                            opp['type'],
                            opp['path'],
                            opp['recommendation']
                        ])
            
            print(f"   📄 Consolidation CSV: {consolidation_csv}")
    
    def _generate_markdown_report(self, duplicate_analysis, scattered_analysis, consolidation_ops):
        """Generate comprehensive markdown report."""
        report_path = self.workspace_root / f"MULTIFOLDER_DEEPDIVE_REPORT_{self.timestamp}.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Multifolder Deep Dive & Consolidation Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Target Directories:** {', '.join(self.target_dirs)}\n")
            f.write(f"**Max Depth:** {'Unlimited' if self.max_depth is None else self.max_depth}\n\n")
            f.write("---\n\n")
            
            # Executive Summary
            f.write("## 📊 Executive Summary\n\n")
            f.write(f"- **Total Files:** {self.stats['total_files']:,}\n")
            f.write(f"- **Total Directories:** {self.stats['total_dirs']:,}\n")
            f.write(f"- **Total Size:** {self.stats['total_size'] / (1024**3):.2f} GB\n")
            f.write(f"- **Duplicate Groups:** {duplicate_analysis['total_groups']}\n")
            f.write(f"- **Total Duplicates:** {duplicate_analysis['total_duplicates']}\n")
            f.write(f"- **Potential Space Savings:** {duplicate_analysis['total_waste_gb']:.2f} GB\n")
            f.write(f"- **Scattered Files:** {scattered_analysis['total_files']}\n")
            f.write(f"- **Consolidation Opportunities:** {len(consolidation_ops)}\n\n")
            
            # Top File Types
            f.write("## 📁 Top File Types\n\n")
            f.write("| Extension | Count | Percentage |\n")
            f.write("|-----------|------:|----------:|\n")
            total_files = self.stats['total_files']
            for ext, count in self.stats['by_extension'].most_common(20):
                pct = (count / total_files) * 100 if total_files > 0 else 0
                f.write(f"| `{ext}` | {count:,} | {pct:.1f}% |\n")
            f.write("\n")
            
            # Duplicates Section
            if duplicate_analysis['groups']:
                f.write("## 🔄 Duplicate Files Analysis\n\n")
                f.write(f"Found **{duplicate_analysis['total_groups']}** groups of duplicate files.\n\n")
                f.write(f"**Total waste:** {duplicate_analysis['total_waste_gb']:.2f} GB\n\n")
                
                # Top duplicates
                sorted_dupes = sorted(
                    duplicate_analysis['groups'].items(),
                    key=lambda x: x[1]['waste_mb'],
                    reverse=True
                )[:30]
                
                for i, (file_hash, group) in enumerate(sorted_dupes, 1):
                    f.write(f"### Duplicate Group {i}: {group['filename']}\n\n")
                    f.write(f"- **Keep:** `{group['keep']['path']}`\n")
                    f.write(f"- **Duplicates:** {group['count']}\n")
                    f.write(f"- **Waste:** {group['waste_mb']:.2f} MB\n")
                    f.write(f"- **Locations:**\n")
                    for dup in group['duplicates'][:5]:
                        f.write(f"  - `{dup['path']}`\n")
                    if len(group['duplicates']) > 5:
                        f.write(f"  - ... and {len(group['duplicates']) - 5} more\n")
                    f.write("\n")
            
            # Scattered Files Section
            if scattered_analysis['groups']:
                f.write("## 📂 Scattered Files Analysis\n\n")
                f.write(f"Found **{scattered_analysis['total_files']}** files with the same name in multiple locations.\n\n")
                
                sorted_scattered = sorted(
                    scattered_analysis['groups'].items(),
                    key=lambda x: x[1]['scatter_score'],
                    reverse=True
                )[:30]
                
                for i, (filename, group) in enumerate(sorted_scattered, 1):
                    f.write(f"### {i}. {filename}\n\n")
                    f.write(f"- **Locations:** {group['count']}\n")
                    f.write(f"- **Unique Directories:** {group['unique_directories']}\n")
                    f.write(f"- **Scatter Score:** {group['scatter_score']}\n")
                    f.write(f"- **Recommended Location:** `{group['recommended_location']}`\n")
                    f.write(f"- **All Locations:**\n")
                    for loc in group['locations'][:5]:
                        f.write(f"  - `{loc['path']}` (depth: {loc['depth']})\n")
                    if len(group['locations']) > 5:
                        f.write(f"  - ... and {len(group['locations']) - 5} more\n")
                    f.write("\n")
            
            # Consolidation Opportunities
            if consolidation_ops:
                f.write("## 🎯 Consolidation Opportunities\n\n")
                for i, opp in enumerate(consolidation_ops, 1):
                    f.write(f"### {i}. {opp['type']}\n\n")
                    f.write(f"{opp['recommendation']}\n\n")
                    if 'paths' in opp:
                        f.write("**Affected paths:**\n")
                        for path in opp['paths'][:10]:
                            f.write(f"- `{path}`\n")
                        if len(opp['paths']) > 10:
                            f.write(f"- ... and {len(opp['paths']) - 10} more\n")
                    f.write("\n")
            
            # Largest Directories
            f.write("## 📂 Largest Directories (by file count)\n\n")
            sorted_dirs = sorted(
                self.stats['by_directory'].items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )[:30]
            
            f.write("| Directory | Files | Size (GB) | Depth |\n")
            f.write("|-----------|------:|----------:|------:|\n")
            for dir_name, stats in sorted_dirs:
                size_gb = stats['size'] / (1024**3)
                f.write(f"| `{dir_name}` | {stats['count']:,} | {size_gb:.2f} | {stats['depth']} |\n")
            f.write("\n")
            
            # Large Files
            if self.stats['large_files']:
                f.write("## 💾 Large Files (>100 MB)\n\n")
                f.write("| File | Size (MB) | Depth |\n")
                f.write("|------|----------:|------:|\n")
                for file in self.stats['large_files'][:50]:
                    f.write(f"| `{file['path']}` | {file['size_mb']:.1f} | {file['depth']} |\n")
                f.write("\n")
        
        print(f"   📄 Markdown Report: {report_path}")
        return report_path

def main():
    """Main execution function."""
    # Initialize analyzer with AVATARARTS workspace
    analyzer = MultifolderDeepDive(
        target_dirs=[str(Path("/Users/steven/AVATARARTS"))],
        max_depth=None  # Unlimited depth
    )
    
    # Run analysis
    analyzer.run_analysis()
    
    # Generate reports
    analyzer.generate_reports()
    
    print("\n" + "=" * 80)
    print("✅ DEEP DIVE COMPLETE!")
    print("=" * 80)
    print(f"\n📊 Check the generated CSV and Markdown reports in:")
    print(f"   {analyzer.workspace_root}")
    print()

if __name__ == "__main__":
    main()
