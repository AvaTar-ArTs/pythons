#!/usr/bin/env python3
"""
Deep dive analysis of folder depths across Documents directory
Identifies folders with excessive depth and calculates organization metrics
"""

from pathlib import Path
from collections import defaultdict
import json
from datetime import datetime

documents_dir = Path.home() / "Documents"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

print("=" * 100)
print("🔍 DEEP DIVE: FOLDER DEPTH ANALYSIS")
print("=" * 100)
print()

# Track depth statistics
depth_stats = defaultdict(lambda: {'folders': 0, 'files': 0, 'total_size': 0})
folder_details = []

# Folders to exclude from analysis (system/dependency folders)
EXCLUDE_PATTERNS = [
    'node_modules',
    '.git',
    '__pycache__',
    '.next',
    'dist',
    'build',
    '.venv',
    'venv',
    '.env',
    '.idea',
    '.vscode',
    'target',  # Rust
    'bin',
    'obj',  # .NET
]

def should_exclude(path):
    """Check if path should be excluded from analysis"""
    path_str = str(path)
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str:
            return True
    return False

def analyze_path(path, base_depth=0):
    """Recursively analyze folder structure"""
    try:
        if not path.exists() or not path.is_dir():
            return
        
        # Skip excluded folders
        if should_exclude(path):
            return
        
        # Calculate depth
        depth = len(path.relative_to(documents_dir).parts)
        
        # Count files in this directory
        files = list(path.iterdir())
        file_count = sum(1 for f in files if f.is_file())
        folder_count = sum(1 for f in files if f.is_dir())
        
        # Calculate total size of files in this directory (not recursive)
        total_size = sum(f.stat().st_size for f in files if f.is_file())
        
        # Update statistics
        depth_stats[depth]['folders'] += 1
        depth_stats[depth]['files'] += file_count
        depth_stats[depth]['total_size'] += total_size
        
        # Store folder details if depth > 2
        if depth > 2:
            folder_details.append({
                'path': str(path.relative_to(documents_dir)),
                'depth': depth,
                'files': file_count,
                'subfolders': folder_count,
                'size_bytes': total_size,
                'size_mb': round(total_size / (1024 * 1024), 2)
            })
        
        # Recurse into subdirectories
        for item in files:
            if item.is_dir():
                analyze_path(item, depth)
    
    except (PermissionError, OSError):
        pass

print("Analyzing folder structure...")
print("This may take a few minutes...")
print()

analyze_path(documents_dir)

print("=" * 100)
print("📊 DEPTH STATISTICS")
print("=" * 100)
print()

# Sort by depth
sorted_depths = sorted(depth_stats.items())

print(f"{'Depth':<8} {'Folders':<12} {'Files':<12} {'Size (MB)':<15} {'Severity':<12}")
print("-" * 100)

total_folders = 0
total_files = 0
total_size = 0

for depth, stats in sorted_depths:
    folders = stats['folders']
    files = stats['files']
    size_mb = stats['total_size'] / (1024 * 1024)
    severity = files * depth  # Files × depth
    
    total_folders += folders
    total_files += files
    total_size += stats['total_size']
    
    print(f"{depth:<8} {folders:<12,} {files:<12,} {size_mb:<15.2f} {severity:<12,}")

print("-" * 100)
print(f"{'TOTAL':<8} {total_folders:<12,} {total_files:<12,} {total_size/(1024*1024):<15.2f}")

print()
print("=" * 100)
print("🔴 PROBLEM FOLDERS (Depth > 3)")
print("=" * 100)
print()

# Sort folder details by severity (files × depth)
folder_details.sort(key=lambda x: x['files'] * x['depth'], reverse=True)

print(f"{'Depth':<8} {'Files':<10} {'Size (MB)':<12} {'Path':<60}")
print("-" * 100)

problem_folders = [f for f in folder_details if f['depth'] > 3]
for folder in problem_folders[:50]:  # Top 50
    path_display = folder['path'][:58] + ".." if len(folder['path']) > 60 else folder['path']
    print(f"{folder['depth']:<8} {folder['files']:<10,} {folder['size_mb']:<12.2f} {path_display:<60}")

print()
print(f"Total problem folders (depth > 3): {len(problem_folders):,}")

# Save detailed report
report_file = documents_dir / f"FOLDER_DEPTH_ANALYSIS_{timestamp}.json"
with open(report_file, 'w') as f:
    json.dump({
        'timestamp': timestamp,
        'depth_stats': {str(k): v for k, v in depth_stats.items()},
        'problem_folders': folder_details[:100],  # Top 100
        'summary': {
            'total_folders': total_folders,
            'total_files': total_files,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'problem_folders_count': len(problem_folders)
        }
    }, f, indent=2)

print()
print(f"📄 Detailed report saved: {report_file.name}")

# Identify top candidates for flattening
print()
print("=" * 100)
print("🎯 TOP CANDIDATES FOR FLATTENING (by severity)")
print("=" * 100)
print()

top_candidates = sorted(problem_folders, key=lambda x: x['files'] * x['depth'], reverse=True)[:20]

for i, folder in enumerate(top_candidates, 1):
    severity = folder['files'] * folder['depth']
    print(f"{i:2d}. Severity: {severity:,} | Depth: {folder['depth']} | Files: {folder['files']:,} | {folder['path']}")

print()
print("=" * 100)
print("✅ ANALYSIS COMPLETE")
print("=" * 100)

