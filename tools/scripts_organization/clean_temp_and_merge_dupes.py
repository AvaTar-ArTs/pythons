#!/usr/bin/env python3
"""
Script to clean temporary files and identify duplicate directories
"""
import os
import shutil
from pathlib import Path

def clean_temp_files():
    """Clean temporary files like .DS_Store, __pycache__, etc."""
    print("🧹 CLEANING TEMPORARY FILES")
    print("="*50)
    
    temp_patterns = [
        '.DS_Store',
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '*.tmp',
        '*.temp',
        '*.bak',
        '*.old',
        '*backup*',
        '.coverage',
        'coverage.xml',
        'htmlcov/',
        '.pytest_cache/',
        '.mypy_cache/',
        '.tox/',
        '*.log'  # Only if they're old logs
    ]
    
    cleaned_files = 0
    cleaned_size = 0
    
    for pattern in temp_patterns:
        if pattern in ['.DS_Store', '*.pyc', '*.pyo', '*.tmp', '*.temp', '*.bak', '*.old', '*backup*', '*.log']:
            for file_path in Path('.').rglob(pattern):
                if file_path.is_file():
                    try:
                        size = file_path.stat().st_size
                        file_path.unlink()
                        print(f"  Removed: {file_path} ({size} bytes)")
                        cleaned_files += 1
                        cleaned_size += size
                    except Exception as e:
                        print(f"  Error removing {file_path}: {e}")
        elif pattern in ['__pycache__']:
            for dir_path in Path('.').rglob(pattern):
                if dir_path.is_dir():
                    try:
                        size = sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())
                        shutil.rmtree(dir_path)
                        print(f"  Removed directory: {dir_path} (~{size} bytes)")
                        cleaned_files += 1
                        cleaned_size += size
                    except Exception as e:
                        print(f"  Error removing directory {dir_path}: {e}")
    
    print(f"\n✅ Cleaned {cleaned_files} temporary files/directories")
    print(f"✅ Freed up {cleaned_size:,} bytes ({cleaned_size/1024/1024:.2f} MB)")
    return cleaned_files, cleaned_size

def find_duplicate_directories():
    """Find potentially duplicate directories based on name patterns"""
    print("\n🔍 FINDING POTENTIAL DUPLICATE DIRECTORIES")
    print("="*50)
    
    all_dirs = [d for d in Path('.').iterdir() if d.is_dir()]
    dir_names = {}
    
    for item in all_dirs:
        name = item.name.lower()
        # Normalize name by removing common suffixes/prefixes
        normalized = name.replace('-complete', '').replace('_complete', '').replace('-backup', '').replace('_backup', '')
        normalized = normalized.replace('-final', '').replace('_final', '').replace('-old', '').replace('_old', '')
        normalized = normalized.replace('-v1', '').replace('-v2', '').replace('-v3', '').replace('-v4', '').replace('-v5', '')
        normalized = normalized.replace('_v1', '').replace('_v2', '').replace('_v3', '').replace('_v4', '').replace('_v5', '')
        
        if normalized in dir_names:
            dir_names[normalized].append(item.name)
        else:
            dir_names[normalized] = [item.name]
    
    # Return groups of directories with similar names
    duplicates = [dirs for dirs in dir_names.values() if len(dirs) > 1]
    
    if duplicates:
        print("Potential duplicate directory groups found:")
        for group in duplicates:
            print(f"  {group}")
            
            # Show sizes for comparison
            sizes = []
            for dir_name in group:
                dir_path = Path(dir_name)
                if dir_path.exists():
                    size = sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())
                    sizes.append((dir_name, size))
            
            for dir_name, size in sizes:
                print(f"    - {dir_name}: {size/1024/1024:.2f} MB")
    else:
        print("No potential duplicate directories found")
    
    return duplicates

def main():
    print("AVATARARTS TEMPORARY FILE CLEANUP & DUPLICATE DIRECTORY ANALYSIS")
    print("="*70)
    
    # Clean temporary files
    cleaned_files, cleaned_size = clean_temp_files()
    
    # Find duplicate directories
    dup_dirs = find_duplicate_directories()
    
    print(f"\n📊 SUMMARY:")
    print(f"  • Temporary files cleaned: {cleaned_files}")
    print(f"  • Storage freed: {cleaned_size/1024/1024:.2f} MB")
    print(f"  • Potential duplicate directory groups: {len(dup_dirs)}")
    
    if dup_dirs:
        print(f"\n💡 NEXT STEPS:")
        print(f"  • Review the duplicate directory groups above")
        print(f"  • Determine which directories to merge/consolidate")
        print(f"  • Consider keeping the most recent/complete version")
        print(f"  • Archive or remove redundant directories")
    
    print(f"\n✅ Analysis complete!")

if __name__ == "__main__":
    main()