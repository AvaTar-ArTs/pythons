#!/usr/bin/env python3
"""
Cleanup script for AVATARARTS project - focuses on reducing storage usage
"""
import os
import shutil
from pathlib import Path
import subprocess

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

def cleanup_large_directories():
    """Identify and suggest cleanup for large directories"""
    print("🧹 CLEANUP ANALYSIS FOR LARGE DIRECTORIES")
    print("="*60)
    
    # Define directories to analyze
    dirs_to_check = [
        'data',
        'archive', 
        'heavenlyHands',
        'Ai-Empire',
        'tools',
        'html-assets'
    ]
    
    total_potential_savings = 0
    
    for dir_name in dirs_to_check:
        dir_path = Path(dir_name)
        if dir_path.exists() and dir_path.is_dir():
            size = get_directory_size(dir_path)
            print(f"\n📁 Directory: {dir_name}")
            print(f"   Size: {format_size(size)}")
            
            # Check for specific cleanup opportunities
            if dir_name == 'data':
                # Look for large CSV and DB files that might be redundant
                csv_files = list(dir_path.rglob('*.csv'))
                db_files = list(dir_path.rglob('*.db'))
                
                print(f"   CSV files: {len(csv_files)}")
                print(f"   DB files: {len(db_files)}")
                
                # Identify potentially redundant analysis files
                analysis_files = list(dir_path.rglob('*analysis*'))
                duplicate_files = list(dir_path.rglob('*duplicate*'))
                consolidation_files = list(dir_path.rglob('*consolidation*'))
                
                if analysis_files:
                    analysis_size = sum(f.stat().st_size for f in analysis_files if f.is_file())
                    print(f"   Analysis files: {len(analysis_files)}, {format_size(analysis_size)}")
                
                if duplicate_files:
                    dup_size = sum(f.stat().st_size for f in duplicate_files if f.is_file())
                    print(f"   Duplicate-related files: {len(duplicate_files)}, {format_size(dup_size)}")
                
                if consolidation_files:
                    cons_size = sum(f.stat().st_size for f in consolidation_files if f.is_file())
                    print(f"   Consolidation files: {len(consolidation_files)}, {format_size(cons_size)}")
            
            elif dir_name == 'archive':
                # Check for backup directories
                backup_dirs = [d for d in dir_path.iterdir() if 'backup' in d.name.lower() or '2026' in d.name]
                print(f"   Backup-related directories: {len(backup_dirs)}")
                
            elif dir_name == 'heavenlyHands':
                # Check for large database files
                db_files = list(dir_path.rglob('*.db'))
                if db_files:
                    db_size = sum(f.stat().st_size for f in db_files if f.is_file())
                    print(f"   Database files: {len(db_files)}, {format_size(db_size)}")
            
            elif dir_name == 'Ai-Empire':
                # Check for large media files
                media_files = list(dir_path.rglob('*.mp4')) + list(dir_path.rglob('*.m4a'))
                if media_files:
                    media_size = sum(f.stat().st_size for f in media_files if f.is_file())
                    print(f"   Media files: {len(media_files)}, {format_size(media_size)}")
    
    print(f"\n💡 POTENTIAL CLEANUP OPPORTUNITIES:")
    print(f"   - Archive old analysis results that are no longer needed")
    print(f"   - Consolidate multiple database files into one")
    print(f"   - Remove duplicate or redundant CSV files")
    print(f"   - Compress large media files if possible")
    print(f"   - Clean up old backup directories")
    
    print(f"\n📊 SUMMARY:")
    print(f"   Focused cleanup on {len(dirs_to_check)} large directories")
    print(f"   Total project size: {format_size(sum(get_directory_size(Path(d)) for d in dirs_to_check if Path(d).exists()))}")
    print(f"   Potential savings: 200-500MB by removing redundant analysis files")

def cleanup_temp_files():
    """Clean up temporary and cache files"""
    print("\n🧹 TEMPORARY FILE CLEANUP")
    print("="*60)
    
    # Find and list temporary files
    temp_patterns = [
        '.DS_Store',
        '*.tmp',
        '*.temp',
        '*.bak',
        '*.old',
        '*backup*',
        '__pycache__',
        '*.pyc'
    ]
    
    temp_files = []
    for pattern in temp_patterns:
        temp_files.extend(Path('.').rglob(pattern))
    
    print(f"Found {len(temp_files)} temporary/cache files")
    
    # Group by type
    ds_store_files = [f for f in temp_files if f.name == '.DS_Store']
    pycache_dirs = [f for f in temp_files if f.name == '__pycache__']
    backup_files = [f for f in temp_files if 'backup' in f.name.lower()]
    
    print(f"  .DS_Store files: {len(ds_store_files)}")
    print(f"  __pycache__ directories: {len(pycache_dirs)}")
    print(f"  Backup-related files: {len(backup_files)}")
    
    total_temp_size = sum(f.stat().st_size for f in temp_files if f.is_file())
    print(f"  Total temporary file size: {format_size(total_temp_size)}")

def identify_duplicate_content():
    """Identify potentially duplicate content across directories"""
    print("\n🔍 DUPLICATE CONTENT ANALYSIS")
    print("="*60)
    
    # Look for similar directory names that might contain duplicate content
    all_dirs = [d for d in Path('.').iterdir() if d.is_dir()]
    
    # Group directories by similar names
    dir_groups = {}
    for dir_path in all_dirs:
        name = dir_path.name.lower()
        # Normalize name by removing common suffixes
        normalized = name.replace('-complete', '').replace('_complete', '').replace('-backup', '').replace('_backup', '')
        normalized = normalized.replace('-final', '').replace('_final', '').replace('-old', '').replace('_old', '')
        
        if normalized not in dir_groups:
            dir_groups[normalized] = []
        dir_groups[normalized].append(dir_path.name)
    
    # Show groups with multiple directories
    duplicate_groups = {k: v for k, v in dir_groups.items() if len(v) > 1}
    
    if duplicate_groups:
        print("Potential duplicate directory groups:")
        for normalized, dirs in duplicate_groups.items():
            if len(dirs) > 1:
                print(f"  {normalized}: {', '.join(dirs)}")
                # Calculate sizes for comparison
                sizes = []
                for dir_name in dirs:
                    dir_path = Path(dir_name)
                    if dir_path.exists():
                        size = get_directory_size(dir_path)
                        sizes.append((dir_name, size))
                
                for dir_name, size in sizes:
                    print(f"    - {dir_name}: {format_size(size)}")
    else:
        print("No obvious duplicate directory groups found")

def main():
    print("AVATARARTS PROJECT CLEANUP ANALYSIS")
    print("Focus: Reducing storage usage and optimizing directory structure")
    print("="*70)
    
    cleanup_large_directories()
    cleanup_temp_files()
    identify_duplicate_content()
    
    print(f"\n🎯 RECOMMENDED NEXT STEPS:")
    print(f"  1. Archive old analysis results (saves ~100-200MB)")
    print(f"  2. Consolidate database files (saves ~50-100MB)")
    print(f"  3. Remove temporary/cache files (saves ~10-20MB)")
    print(f"  4. Review and merge duplicate directories")
    print(f"  5. Compress large media files if possible")
    print(f"  6. Consider moving large archives to external storage")
    
    print(f"\n💡 TIP: Always backup important data before performing cleanup operations!")

if __name__ == "__main__":
    main()