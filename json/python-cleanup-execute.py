"""
Python Cleanup Execute

This module provides functionality for python cleanup execute.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Python Directory Cleanup - Auto Execution
Automatically removes identified duplicate and unnecessary files.
"""

import os
import shutil
import re
from pathlib import Path
from collections import defaultdict
import json
from datetime import datetime

def create_backup_log():
    """Create a backup log file for tracking deletions."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"/Users/steven/python_cleanup_log_{timestamp}.json"
    return log_file

def log_deletion(log_file, file_path, reason, file_size):
    """Log a file deletion."""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'file': str(file_path),
        'reason': reason,
        'size_bytes': file_size,
        'size_mb': round(file_size / (CONSTANT_1024 * CONSTANT_1024), 2)
    }
    
    # Append to log file
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def analyze_files_to_remove():
    """Analyze files that should be removed."""
    python_path = Path(Path("/Users/steven/Documents/python"))
    
    files_to_remove = {
        'cache_files': [],
        'temp_files': [],
        'empty_files': [],
        'duplicate_files': [],
        'numbered_files': [],
        'auto_generated_files': []
    }
    
    logger.info("🔍 Analyzing files for removal...")
    
    # 1. Find cache files
    logger.info("   - Finding cache files...")
    for file_path in python_path.rglob('*'):
        if file_path.is_file():
            if any(pattern in file_path.name.lower() for pattern in ['__pycache__', '.pyc', '.pyo', '.pyd']):
                files_to_remove['cache_files'].append({
                    'path': str(file_path),
                    'size': file_path.stat().st_size,
                    'reason': 'Cache file'
                })
    
    # 2. Find temp files
    logger.info("   - Finding temp files...")
    for file_path in python_path.rglob('*'):
        if file_path.is_file():
            if any(pattern in file_path.name.lower() for pattern in ['.tmp', '.temp', '~', '.bak', '.backup']):
                files_to_remove['temp_files'].append({
                    'path': str(file_path),
                    'size': file_path.stat().st_size,
                    'reason': 'Temporary file'
                })
    
    # 3. Find empty files
    logger.info("   - Finding empty files...")
    for file_path in python_path.rglob('*'):
        if file_path.is_file() and file_path.stat().st_size == 0:
            files_to_remove['empty_files'].append({
                'path': str(file_path),
                'size': 0,
                'reason': 'Empty file'
            })
    
    # 4. Find numbered files (be selective)
    logger.info("   - Finding numbered files...")
    numbered_groups = defaultdict(list)
    
    for file_path in python_path.rglob('*.py'):
        if file_path.is_file() and re.search(r'\(\d+\)|_\d+\.|copy|duplicate', file_path.name.lower()):
            base_name = re.sub(r'[_\-\s]*\(\d+\)[_\-\s]*', '', file_path.name.lower())
            base_name = re.sub(r'[_\-\s]*copy[_\-\s]*', '', base_name)
            base_name = re.sub(r'[_\-\s]*duplicate[_\-\s]*', '', base_name)
            base_name = re.sub(r'\.py$', '', base_name)
            numbered_groups[base_name].append({
                'path': str(file_path),
                'size': file_path.stat().st_size,
                'name': file_path.name
            })
    
    # For each group, keep the first file and mark others for removal
    for base_name, files in numbered_groups.items():
        if len(files) > 1:
            # Sort by name to keep the first one
            files.sort(key=lambda x: x['name'])
            # Keep the first file, remove the rest
            for file_info in files[1:]:
                files_to_remove['numbered_files'].append({
                    'path': file_info['path'],
                    'size': file_info['size'],
                    'reason': f'Numbered file - keeping first in group: {base_name}'
                })
    
    # 5. Find auto-generated files
    logger.info("   - Finding auto-generated files...")
    for file_path in python_path.rglob('*'):
        if file_path.is_file():
            if any(pattern in file_path.name.lower() for pattern in ['auto_', 'generated', 'temp_', 'tmp_']):
                files_to_remove['auto_generated_files'].append({
                    'path': str(file_path),
                    'size': file_path.stat().st_size,
                    'reason': 'Auto-generated file'
                })
    
    # 6. Find exact duplicates by hash
    logger.info("   - Finding exact duplicates...")
    file_hashes = defaultdict(list)
    
    for file_path in python_path.rglob('*'):
        if file_path.is_file() and file_path.stat().st_size < 50 * CONSTANT_1024 * CONSTANT_1024:  # Only files < 50MB
            try:
                with open(file_path, 'rb') as f:
                    file_hash = hash(f.read())
                file_hashes[file_hash].append({
                    'path': str(file_path),
                    'size': file_path.stat().st_size,
                    'name': file_path.name
                })
            except (IOError, OSError):
                continue
    
    # Find duplicates
    for file_hash, files in file_hashes.items():
        if len(files) > 1:
            # Sort by name to keep the first one
            files.sort(key=lambda x: x['name'])
            # Keep the first file, remove the rest
            for file_info in files[1:]:
                files_to_remove['duplicate_files'].append({
                    'path': file_info['path'],
                    'size': file_info['size'],
                    'reason': f'Exact duplicate - keeping first in group'
                })
    
    return files_to_remove

def remove_files_safely(files_to_remove, log_file):
    """Safely remove files with logging."""
    total_size = 0
    total_files = 0
    removed_count = 0
    error_count = 0
    
    logger.info(f"\n🗑️  REMOVING FILES")
    logger.info("=" * 60)
    
    for category, files in files_to_remove.items():
        if not files:
            continue
            
        logger.info(f"\n📁 {category.upper().replace('_', ' ')}")
        logger.info("-" * 40)
        logger.info(f"Files to remove: {len(files)}")
        
        category_size = sum(f['size'] for f in files)
        category_mb = category_size / (CONSTANT_1024 * CONSTANT_1024)
        logger.info(f"Total size: {category_mb:.2f} MB")
        
        total_size += category_size
        total_files += len(files)
        
        # Show first few files
        for i, file_info in enumerate(files[:3]):
            size_mb = file_info['size'] / (CONSTANT_1024 * CONSTANT_1024)
            logger.info(f"  {i+1}. {Path(file_info['path']).name} ({size_mb:.2f} MB)")
        
        if len(files) > 3:
            logger.info(f"  ... and {len(files) - 3} more files")
        
        # Actually remove files
        logger.info(f"\n   Removing {len(files)} files...")
        for i, file_info in enumerate(files):
            try:
                file_path = Path(file_info['path'])
                if file_path.exists():
                    file_path.unlink()
                    log_deletion(log_file, file_path, file_info['reason'], file_info['size'])
                    removed_count += 1
                    if (i + 1) % CONSTANT_100 == 0:
                        logger.info(f"   Progress: {i + 1}/{len(files)} files removed...")
                else:
                    logger.info(f"   ⚠ File not found: {file_path.name}")
            except Exception as e:
                logger.info(f"   ❌ Error removing {file_path.name}: {e}")
                error_count += 1
        
        logger.info(f"   ✅ Completed: {removed_count} files removed, {error_count} errors")
    
    total_mb = total_size / (CONSTANT_1024 * CONSTANT_1024)
    total_gb = total_mb / CONSTANT_1024
    
    logger.info(f"\n📊 CLEANUP SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Total files processed: {total_files:,}")
    logger.info(f"Files successfully removed: {removed_count:,}")
    logger.info(f"Errors encountered: {error_count:,}")
    logger.info(f"Total space freed: {total_mb:.2f} MB ({total_gb:.2f} GB)")
    logger.info(f"Log file: {log_file}")
    
    return removed_count, total_size

def main():
    """Main cleanup execution."""
    logger.info("🐍 PYTHON CLEANUP - AUTO EXECUTION")
    logger.info("=" * 60)
    
    # Create backup log
    log_file = create_backup_log()
    logger.info(f"📝 Log file: {log_file}")
    
    # Analyze files
    files_to_remove = analyze_files_to_remove()
    
    # Show summary
    total_files = sum(len(files) for files in files_to_remove.values())
    total_size = sum(sum(f['size'] for f in files) for files in files_to_remove.values())
    total_mb = total_size / (CONSTANT_1024 * CONSTANT_1024)
    total_gb = total_mb / CONSTANT_1024
    
    logger.info(f"\n📊 CLEANUP PLAN")
    logger.info("=" * 60)
    logger.info(f"Cache files: {len(files_to_remove['cache_files'])}")
    logger.info(f"Temp files: {len(files_to_remove['temp_files'])}")
    logger.info(f"Empty files: {len(files_to_remove['empty_files'])}")
    logger.info(f"Duplicate files: {len(files_to_remove['duplicate_files'])}")
    logger.info(f"Numbered files: {len(files_to_remove['numbered_files'])}")
    logger.info(f"Auto-generated files: {len(files_to_remove['auto_generated_files'])}")
    logger.info(f"Total files to remove: {total_files:,}")
    logger.info(f"Total space to free: {total_mb:.2f} MB ({total_gb:.2f} GB)")
    
    logger.info(f"\n🚀 Starting cleanup...")
    removed_count, freed_size = remove_files_safely(files_to_remove, log_file)
    
    logger.info(f"\n✅ Cleanup completed!")
    logger.info(f"   Removed: {removed_count:,} files")
    logger.info(f"   Freed: {freed_size / (CONSTANT_1024**3):.2f} GB")
    logger.info(f"   Log: {log_file}")

if __name__ == "__main__":
    main()