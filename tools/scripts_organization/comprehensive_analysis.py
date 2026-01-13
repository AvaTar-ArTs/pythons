#!/usr/bin/env python3
"""
Comprehensive analysis and cleanup recommendations for AVATARARTS project
"""
import os
import shutil
from pathlib import Path
import subprocess

def get_directory_size(directory):
    """Calculate total size of a directory"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            # Skip hidden directories and common cache directories
            dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.git', '.svn']]
            
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, FileNotFoundError):
                    # Skip files that can't be accessed
                    continue
    except Exception:
        pass
    return total_size

def format_size(size_bytes):
    """Format size in human readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def analyze_large_directories(directory, size_threshold_mb=10):
    """Find directories larger than the threshold"""
    directory = Path(directory)
    large_dirs = []
    
    for item in directory.iterdir():
        if item.is_dir():
            size = get_directory_size(item)
            if size > size_threshold_mb * 1024 * 1024:  # Convert MB to bytes
                large_dirs.append((size, item.name))
    
    # Sort by size (largest first)
    large_dirs.sort(key=lambda x: x[0], reverse=True)
    return large_dirs

def find_duplicate_directories(directory):
    """Find potentially duplicate directories based on name patterns"""
    directory = Path(directory)
    dir_names = {}
    
    for item in directory.iterdir():
        if item.is_dir():
            name = item.name.lower()
            # Normalize name by removing common suffixes/prefixes
            normalized = name.replace('-complete', '').replace('_complete', '').replace('-backup', '').replace('_backup', '')
            
            if normalized in dir_names:
                dir_names[normalized].append(item.name)
            else:
                dir_names[normalized] = [item.name]
    
    # Return groups of directories with similar names
    duplicates = [dirs for dirs in dir_names.values() if len(dirs) > 1]
    return duplicates

def find_large_files(directory, size_threshold_mb=50):
    """Find individual files larger than the threshold"""
    directory = Path(directory)
    large_files = []
    
    for file_path in directory.rglob('*'):
        if file_path.is_file():
            try:
                size = file_path.stat().st_size
                if size > size_threshold_mb * 1024 * 1024:  # Convert MB to bytes
                    large_files.append((size, str(file_path)))
            except (OSError, FileNotFoundError):
                continue
    
    # Sort by size (largest first)
    large_files.sort(key=lambda x: x[0], reverse=True)
    return large_files

def analyze_project_structure(directory):
    """Analyze the overall project structure"""
    directory = Path(directory)
    
    print("🔍 COMPREHENSIVE PROJECT ANALYSIS")
    print("="*60)
    
    # Get all directories
    all_dirs = [d for d in directory.iterdir() if d.is_dir()]
    total_dirs = len(all_dirs)
    
    # Get total size
    total_size = sum(get_directory_size(d) for d in all_dirs)
    
    print(f"Total directories: {total_dirs}")
    print(f"Total project size: {format_size(total_size)}")
    print()
    
    # Find large directories
    print("📁 LARGEST DIRECTORIES (>10MB):")
    large_dirs = analyze_large_directories(directory, 10)
    for size, name in large_dirs:
        print(f"  {format_size(size):>8} - {name}")
    print()
    
    # Find potentially duplicate directories
    print("🔍 POTENTIALLY DUPLICATE DIRECTORIES:")
    dup_dirs = find_duplicate_directories(directory)
    if dup_dirs:
        for group in dup_dirs:
            print(f"  Similar directories: {', '.join(group)}")
    else:
        print("  No potentially duplicate directories found")
    print()
    
    # Find large individual files
    print("💾 LARGE INDIVIDUAL FILES (>50MB):")
    large_files = find_large_files(directory, 50)
    for size, path in large_files[:10]:  # Show top 10
        print(f"  {format_size(size):>8} - {path}")
    if len(large_files) > 10:
        print(f"  ... and {len(large_files) - 10} more large files")
    print()
    
    # Cleanup recommendations
    print("🧹 CLEANUP RECOMMENDATIONS:")
    
    # Check for database files that might be redundant
    db_files = list(directory.rglob('*.db'))
    if len(db_files) > 3:  # If there are many DB files
        print(f"  • Found {len(db_files)} database files - consider consolidating or cleaning up old ones")
    
    # Check for log files
    log_files = list(directory.rglob('*.log'))
    if log_files:
        print(f"  • Found {len(log_files)} log files - consider archiving old logs")
    
    # Check for temporary/backup files
    temp_patterns = ['.DS_Store', '*.tmp', '*backup*', '*.bak', '*.old']
    temp_files = []
    for pattern in temp_patterns:
        temp_files.extend(directory.rglob(pattern))
    if temp_files:
        print(f"  • Found {len(temp_files)} temporary/backup files - consider cleanup")
    
    # Check for duplicate gitignore files
    gitignores = list(directory.rglob('.gitignore'))
    if len(gitignores) > 5:  # Arbitrary threshold
        print(f"  • Found {len(gitignores)} .gitignore files - consider standardizing")
    
    print()
    print("💡 OPTIMIZATION SUGGESTIONS:")
    print("  • Archive old/unused directories to reduce project size")
    print("  • Consolidate similar directories with redundant content")
    print("  • Remove or compress large files that are no longer needed")
    print("  • Implement a consistent directory naming convention")
    print("  • Consider using symbolic links for shared resources")
    print()
    
    return {
        'total_dirs': total_dirs,
        'total_size': total_size,
        'large_dirs': large_dirs,
        'duplicate_dirs': dup_dirs,
        'large_files': large_files
    }

def main():
    directory = Path.cwd()  # Current directory
    analysis = analyze_project_structure(directory)
    
    print("📊 ANALYSIS COMPLETE")
    print(f"   Directories analyzed: {analysis['total_dirs']}")
    print(f"   Total size: {format_size(analysis['total_size'])}")
    print(f"   Large directories found: {len(analysis['large_dirs'])}")
    print(f"   Potential duplicates: {len(analysis['duplicate_dirs'])}")
    print(f"   Large files found: {len(analysis['large_files'])}")

if __name__ == "__main__":
    main()