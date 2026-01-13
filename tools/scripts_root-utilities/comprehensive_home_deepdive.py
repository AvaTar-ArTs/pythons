#!/usr/bin/env python3
"""
Comprehensive Home Directory Deep Dive
Enhanced analysis with hidden folders, duplicates, and detailed insights
"""

import os
import hashlib
import subprocess
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import csv
import json

class ComprehensiveHomeDeepDive:
    def __init__(self, home_dir=None):
        self.home = Path(home_dir or Path.home())
        self.stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_size': 0,
            'by_extension': Counter(),
            'by_directory': defaultdict(lambda: {'count': 0, 'size': 0}),
            'hidden_dirs': defaultdict(lambda: {'count': 0, 'size': 0}),
            'large_files': [],
            'duplicates': defaultdict(list),
            'python_projects': [],
            'node_projects': [],
            'git_repos': [],
            'file_types': Counter(),
        }
        
    def get_dir_size(self, path):
        """Get directory size using du command"""
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
        return 0
    
    def calculate_hash(self, filepath, max_size=10*1024*1024):
        """Calculate MD5 hash for duplicate detection"""
        try:
            size = filepath.stat().st_size
            if size > max_size:
                return None
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def detect_project_type(self, path):
        """Detect project type from directory contents"""
        indicators = {
            'Python': ['setup.py', 'pyproject.toml', 'requirements.txt', 'Pipfile', '__init__.py'],
            'Node.js': ['package.json', 'package-lock.json', 'yarn.lock', 'node_modules'],
            'Git': ['.git'],
            'Docker': ['Dockerfile', 'docker-compose.yml'],
            'React': ['react', 'next.config.js', 'vite.config.js'],
        }
        
        detected = []
        try:
            for item in path.iterdir():
                if item.is_file() or item.is_dir():
                    for proj_type, files in indicators.items():
                        if item.name in files:
                            if proj_type not in detected:
                                detected.append(proj_type)
        except:
            pass
        return detected
    
    def scan_directory(self, path, max_depth=3, current_depth=0, exclude_patterns=None):
        """Recursively scan directory"""
        if exclude_patterns is None:
            exclude_patterns = [
                'node_modules', '.git', '__pycache__', '.venv', 'venv',
                '.next', 'dist', 'build', '.cache', 'Library', 'System',
            ]
        
        try:
            # Skip excluded directories
            if any(pattern in str(path) for pattern in exclude_patterns):
                return
            
            # Limit depth for performance
            if current_depth > max_depth:
                return
            
            for item in path.iterdir():
                try:
                    # Skip if excluded
                    if any(pattern in str(item) for pattern in exclude_patterns):
                        continue
                    
                    if item.is_file():
                        self.stats['total_files'] += 1
                        size = item.stat().st_size
                        self.stats['total_size'] += size
                        
                        # Extension analysis
                        ext = item.suffix.lower()
                        self.stats['by_extension'][ext] += 1
                        self.stats['file_types'][ext] += 1
                        
                        # Directory tracking
                        rel_dir = str(item.parent.relative_to(self.home))
                        self.stats['by_directory'][rel_dir]['count'] += 1
                        self.stats['by_directory'][rel_dir]['size'] += size
                        
                        # Hidden directory tracking
                        if item.parent.name.startswith('.'):
                            hidden_name = item.parent.name
                            self.stats['hidden_dirs'][hidden_name]['count'] += 1
                            self.stats['hidden_dirs'][hidden_name]['size'] += size
                        
                        # Large files
                        if size > 100 * 1024 * 1024:  # > 100MB
                            self.stats['large_files'].append({
                                'path': str(item.relative_to(self.home)),
                                'size': size,
                                'size_mb': size / (1024 * 1024)
                            })
                        
                        # Duplicate detection (small files only)
                        if size < 5 * 1024 * 1024:  # < 5MB
                            file_hash = self.calculate_hash(item)
                            if file_hash:
                                self.stats['duplicates'][file_hash].append({
                                    'path': str(item.relative_to(self.home)),
                                    'size': size,
                                    'name': item.name
                                })
                    
                    elif item.is_dir() and current_depth < max_depth:
                        self.stats['total_dirs'] += 1
                        
                        # Detect projects
                        project_types = self.detect_project_type(item)
                        if project_types:
                            size = self.get_dir_size(item)
                            if 'Python' in project_types:
                                self.stats['python_projects'].append({
                                    'path': str(item.relative_to(self.home)),
                                    'types': project_types,
                                    'size_mb': size / (1024 * 1024)
                                })
                            if 'Node.js' in project_types:
                                self.stats['node_projects'].append({
                                    'path': str(item.relative_to(self.home)),
                                    'types': project_types,
                                    'size_mb': size / (1024 * 1024)
                                })
                            if 'Git' in project_types:
                                self.stats['git_repos'].append({
                                    'path': str(item.relative_to(self.home)),
                                    'types': project_types,
                                    'size_mb': size / (1024 * 1024)
                                })
                        
                        # Recurse into subdirectories
                        self.scan_directory(item, max_depth, current_depth + 1, exclude_patterns)
                
                except (PermissionError, OSError):
                    continue
                except Exception as e:
                    continue
        
        except (PermissionError, OSError):
            pass
        except Exception as e:
            pass
    
    def analyze_major_directories(self):
        """Analyze major visible directories"""
        print("📂 Analyzing major directories...")
        
        major_dirs = [
            'AVATARARTS', 'GitHub', 'pythons', 'scripts', 'Documents',
            'Downloads', 'Desktop', 'Music', 'Pictures', 'Movies',
            'Library', 'claude-Convos', 'analysis'
        ]
        
        results = []
        for dir_name in major_dirs:
            dir_path = self.home / dir_name
            if dir_path.exists():
                size = self.get_dir_size(dir_path)
                results.append({
                    'name': dir_name,
                    'path': str(dir_path),
                    'size': size,
                    'size_gb': size / (1024**3)
                })
                print(f"   ✓ {dir_name}: {size/(1024**3):.2f} GB")
        
        return results
    
    def analyze_hidden_directories(self):
        """Analyze hidden configuration directories"""
        print("\n🔍 Analyzing hidden directories...")
        
        hidden_dirs = [
            '.env.d', '.claude', '.config', '.cache', '.local',
            '.npm', '.yarn', '.git', '.ssh', '.zsh', '.oh-my-zsh'
        ]
        
        results = []
        for dir_name in hidden_dirs:
            dir_path = self.home / dir_name
            if dir_path.exists():
                size = self.get_dir_size(dir_path)
                results.append({
                    'name': dir_name,
                    'path': str(dir_path),
                    'size': size,
                    'size_mb': size / (1024**2)
                })
                print(f"   ✓ {dir_name}: {size/(1024**2):.1f} MB")
        
        return results
    
    def run_analysis(self):
        """Run comprehensive analysis"""
        print("=" * 80)
        print("COMPREHENSIVE HOME DIRECTORY DEEP DIVE")
        print("=" * 80)
        print(f"Home: {self.home}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Analyze major directories first
        major_dirs = self.analyze_major_directories()
        hidden_dirs = self.analyze_hidden_directories()
        
        print("\n🔍 Scanning files (this may take a while)...")
        print("   Limiting depth to 3 levels for performance...")
        
        # Scan major directories
        for dir_info in major_dirs:
            dir_path = Path(dir_info['path'])
            print(f"   Scanning {dir_info['name']}...")
            self.scan_directory(dir_path, max_depth=3)
        
        # Filter duplicates (keep only groups with 2+ files)
        self.stats['duplicates'] = {
            k: v for k, v in self.stats['duplicates'].items() if len(v) > 1
        }
        
        # Sort large files
        self.stats['large_files'].sort(key=lambda x: x['size'], reverse=True)
        
        print(f"\n✅ Scan complete!")
        print(f"   Files: {self.stats['total_files']:,}")
        print(f"   Directories: {self.stats['total_dirs']:,}")
        print(f"   Total size: {self.stats['total_size'] / (1024**3):.2f} GB")
    
    def generate_report(self):
        """Generate comprehensive markdown report"""
        report_path = self.home / 'AVATARARTS' / 'HOME_DEEPDIVE_REPORT.md'
        
        with open(report_path, 'w') as f:
            f.write("# Home Directory Deep Dive Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Home Directory:** `{self.home}`\n\n")
            f.write("---\n\n")
            
            # Executive Summary
            f.write("## 📊 Executive Summary\n\n")
            f.write(f"- **Total Files:** {self.stats['total_files']:,}\n")
            f.write(f"- **Total Directories:** {self.stats['total_dirs']:,}\n")
            f.write(f"- **Total Size:** {self.stats['total_size'] / (1024**3):.2f} GB\n")
            f.write(f"- **Python Projects:** {len(self.stats['python_projects'])}\n")
            f.write(f"- **Node.js Projects:** {len(self.stats['node_projects'])}\n")
            f.write(f"- **Git Repositories:** {len(self.stats['git_repos'])}\n")
            f.write(f"- **Duplicate Groups:** {len(self.stats['duplicates'])}\n")
            f.write(f"- **Large Files (>100MB):** {len(self.stats['large_files'])}\n\n")
            
            # File Types
            f.write("## 📁 Top File Types\n\n")
            f.write("| Extension | Count | Percentage |\n")
            f.write("|-----------|------:|----------:|\n")
            for ext, count in self.stats['by_extension'].most_common(30):
                pct = (count / self.stats['total_files']) * 100 if self.stats['total_files'] > 0 else 0
                ext_display = ext if ext else "(no extension)"
                f.write(f"| `{ext_display}` | {count:,} | {pct:.1f}% |\n")
            f.write("\n")
            
            # Largest Directories
            f.write("## 📂 Largest Directories (by file count)\n\n")
            sorted_dirs = sorted(
                self.stats['by_directory'].items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )[:30]
            
            f.write("| Directory | Files | Size (GB) |\n")
            f.write("|-----------|------:|----------:|\n")
            for dir_name, stats in sorted_dirs:
                size_gb = stats['size'] / (1024**3)
                f.write(f"| `{dir_name}` | {stats['count']:,} | {size_gb:.2f} |\n")
            f.write("\n")
            
            # Hidden Directories
            if self.stats['hidden_dirs']:
                f.write("## 🔍 Hidden Directories Analysis\n\n")
                sorted_hidden = sorted(
                    self.stats['hidden_dirs'].items(),
                    key=lambda x: x[1]['size'],
                    reverse=True
                )[:20]
                
                f.write("| Directory | Files | Size (MB) |\n")
                f.write("|-----------|------:|----------:|\n")
                for dir_name, stats in sorted_hidden:
                    size_mb = stats['size'] / (1024**2)
                    f.write(f"| `.{dir_name}` | {stats['count']:,} | {size_mb:.1f} |\n")
                f.write("\n")
            
            # Projects
            if self.stats['python_projects']:
                f.write("## 🐍 Python Projects\n\n")
                f.write("| Path | Types | Size (MB) |\n")
                f.write("|------|-------|----------:|\n")
                for proj in sorted(self.stats['python_projects'], key=lambda x: x['size_mb'], reverse=True)[:20]:
                    types = ', '.join(proj['types'])
                    f.write(f"| `{proj['path']}` | {types} | {proj['size_mb']:.1f} |\n")
                f.write("\n")
            
            if self.stats['node_projects']:
                f.write("## 📦 Node.js Projects\n\n")
                f.write("| Path | Types | Size (MB) |\n")
                f.write("|------|-------|----------:|\n")
                for proj in sorted(self.stats['node_projects'], key=lambda x: x['size_mb'], reverse=True)[:20]:
                    types = ', '.join(proj['types'])
                    f.write(f"| `{proj['path']}` | {types} | {proj['size_mb']:.1f} |\n")
                f.write("\n")
            
            # Large Files
            if self.stats['large_files']:
                f.write("## 💾 Large Files (>100 MB)\n\n")
                f.write("| File | Size (MB) |\n")
                f.write("|------|----------:|\n")
                for file in self.stats['large_files'][:50]:
                    f.write(f"| `{file['path']}` | {file['size_mb']:.1f} |\n")
                f.write("\n")
            
            # Duplicates
            if self.stats['duplicates']:
                f.write("## 🔄 Duplicate Files\n\n")
                f.write(f"Found **{len(self.stats['duplicates'])}** groups of duplicate files.\n\n")
                
                # Calculate potential savings
                total_duplicate_size = 0
                for files in self.stats['duplicates'].values():
                    duplicate_size = files[0]['size'] * (len(files) - 1)
                    total_duplicate_size += duplicate_size
                
                f.write(f"**Potential space savings:** {total_duplicate_size / (1024**2):.1f} MB\n\n")
                
                # Top duplicates
                sorted_dupes = sorted(
                    self.stats['duplicates'].items(),
                    key=lambda x: x[1][0]['size'] * len(x[1]),
                    reverse=True
                )[:20]
                
                for i, (hash_val, files) in enumerate(sorted_dupes, 1):
                    f.write(f"### Duplicate Group {i}\n\n")
                    f.write(f"- **File:** `{files[0]['name']}`\n")
                    f.write(f"- **Size:** {files[0]['size'] / 1024:.1f} KB\n")
                    f.write(f"- **Copies:** {len(files)}\n")
                    f.write(f"- **Locations:**\n")
                    for file in files:
                        f.write(f"  - `{file['path']}`\n")
                    f.write("\n")
        
        print(f"✅ Report saved: {report_path}")
        return report_path
    
    def export_csv(self):
        """Export detailed CSV inventory"""
        csv_path = self.home / 'AVATARARTS' / f'HOME_DEEPDIVE_INVENTORY_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Category', 'Path', 'Count', 'Size (bytes)', 'Size (GB)'])
            
            # Directory summary
            for dir_name, stats in sorted(
                self.stats['by_directory'].items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )[:1000]:
                writer.writerow([
                    'Directory',
                    dir_name,
                    stats['count'],
                    stats['size'],
                    f"{stats['size'] / (1024**3):.2f}"
                ])
        
        print(f"✅ CSV inventory saved: {csv_path}")
        return csv_path

def main():
    analyzer = ComprehensiveHomeDeepDive()
    analyzer.run_analysis()
    
    print("\n📝 Generating reports...")
    report_path = analyzer.generate_report()
    csv_path = analyzer.export_csv()
    
    print("\n" + "=" * 80)
    print("✅ DEEP DIVE COMPLETE!")
    print("=" * 80)
    print(f"\n📊 Report: {report_path}")
    print(f"📁 CSV: {csv_path}")
    print()

if __name__ == "__main__":
    main()
