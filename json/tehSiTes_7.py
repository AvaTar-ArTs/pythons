"""
Tehsites 7

This module provides functionality for tehsites 7.

Author: Auto-generated
Date: 2025-11-01
"""


# Constants
CONSTANT_100 = 100
CONSTANT_200 = 200
CONSTANT_300 = 300
CONSTANT_500 = 500
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024
CONSTANT_4096 = 4096

#!/usr/bin/env python3
"""
TehSiTes Comprehensive Cleanup Script
Merges, sorts, and deduplicates files across the entire tehSiTes directory structure
"""

import os
import shutil
import hashlib
from pathlib import Path
import logging
from collections import defaultdict
import json
import time
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TehSiTesCleanup:
    def __init__(self, tehSiTes_dir):
        """__init__ function."""

        self.tehSiTes_dir = Path(tehSiTes_dir)
        self.file_hashes = defaultdict(list)
        self.duplicates_found = 0
        self.files_removed = 0
        self.space_saved = 0
        self.cleanup_log = []
        self.start_time = time.time()
        
    def calculate_file_hash(self, file_path):
        """Calculate MD5 hash of a file"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(CONSTANT_4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating hash for {file_path}: {e}")
            return None
    
    def find_duplicates(self):
        """Find all duplicate files by hash"""
        logger.info("Scanning for duplicate files...")
        
        total_files = 0
        for root, dirs, files in os.walk(self.tehSiTes_dir):
            # Skip certain directories
            if any(skip in root for skip in ['node_modules', '.git', '__pycache__', '.venv']):
                continue
                
            for file in files:
                file_path = Path(root) / file
                if file_path.is_file():
                    total_files += 1
                    if total_files % CONSTANT_1000 == 0:
                        logger.info(f"Processed {total_files} files...")
                    
                    file_hash = self.calculate_file_hash(file_path)
                    if file_hash:
                        self.file_hashes[file_hash].append(file_path)
        
        # Count duplicates
        for file_hash, file_list in self.file_hashes.items():
            if len(file_list) > 1:
                self.duplicates_found += len(file_list) - 1
        
        logger.info(f"Found {self.duplicates_found} duplicate files out of {total_files} total files")
    
    def remove_duplicates(self):
        """Remove duplicate files, keeping the best version"""
        logger.info("Removing duplicate files...")
        
        for file_hash, file_list in self.file_hashes.items():
            if len(file_list) > 1:
                # Sort files by priority (prefer certain locations)
                    """file_priority function."""

                def file_priority(file_path):
                    path_str = str(file_path)
                    priority = 0
                    
                    # Higher priority for main project directories
                    if '03_Business_Platforms' in path_str:
                        priority += CONSTANT_1000
                    if 'Dr_Adu_GainesvillePFS_SEO_Project' in path_str:
                        priority += CONSTANT_500
                    if '15_Website_Hosting' in path_str:
                        priority += CONSTANT_300
                    if '05_Reports_Documentation' in path_str:
                        priority += CONSTANT_200
                    
                    # Lower priority for backup/archive directories
                    if 'New Folder With Items' in path_str:
                        priority -= CONSTANT_1000
                    if 'Archive' in path_str or 'Backup' in path_str:
                        priority -= CONSTANT_500
                    if '06_Archives_Backups' in path_str:
                        priority -= CONSTANT_300
                    
                    # Prefer shorter paths (less nested)
                    priority += (CONSTANT_100 - len(file_path.parts))
                    
                    return priority
                
                # Sort by priority (highest first)
                file_list.sort(key=file_priority, reverse=True)
                
                # Keep the first (highest priority) file, remove the rest
                keep_file = file_list[0]
                remove_files = file_list[1:]
                
                for file_to_remove in remove_files:
                    try:
                        file_size = file_to_remove.stat().st_size
                        file_to_remove.unlink()
                        self.files_removed += 1
                        self.space_saved += file_size
                        self.cleanup_log.append({
                            'action': 'REMOVED_DUPLICATE',
                            'file': str(file_to_remove),
                            'kept': str(keep_file),
                            'size': file_size
                        })
                        logger.info(f"Removed duplicate: {file_to_remove.name}")
                    except Exception as e:
                        logger.error(f"Error removing {file_to_remove}: {e}")
    
    def clean_empty_directories(self):
        """Remove empty directories"""
        logger.info("Cleaning empty directories...")
        
        empty_dirs_removed = 0
        for root, dirs, files in os.walk(self.tehSiTes_dir, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                try:
                    if not any(dir_path.iterdir()):  # Directory is empty
                        dir_path.rmdir()
                        empty_dirs_removed += 1
                        self.cleanup_log.append({
                            'action': 'REMOVED_EMPTY_DIR',
                            'path': str(dir_path)
                        })
                except Exception as e:
                    logger.error(f"Error removing empty directory {dir_path}: {e}")
        
        logger.info(f"Removed {empty_dirs_removed} empty directories")
    
    def clean_numbered_duplicates(self):
        """Remove files with numbered suffixes (2, 3, 4, etc.)"""
        logger.info("Cleaning numbered duplicate files...")
        
        numbered_files_removed = 0
        for root, dirs, files in os.walk(self.tehSiTes_dir):
            # Skip certain directories
            if any(skip in root for skip in ['node_modules', '.git', '__pycache__', '.venv']):
                continue
            
            # Group files by base name
            file_groups = defaultdict(list)
            for file in files:
                file_path = Path(root) / file
                if file_path.is_file():
                    # Extract base name (remove numbers and extensions)
                    base_name = file
                    # Remove common numbered patterns
                    import re
                    base_name = re.sub(r'\s+\d+$', '', base_name)  # Remove trailing numbers
                    base_name = re.sub(r'\s+\(\d+\)$', '', base_name)  # Remove (1), (2), etc.
                    base_name = re.sub(r'\s+\d+\s*$', '', base_name)  # Remove trailing numbers with spaces
                    
                    file_groups[base_name].append(file_path)
            
            # For each group, keep the original and remove numbered versions
            for base_name, file_list in file_groups.items():
                if len(file_list) > 1:
                    # Sort by modification time (keep newest) or by name (keep shortest)
                    file_list.sort(key=lambda x: (x.stat().st_mtime, len(x.name)), reverse=True)
                    
                    keep_file = file_list[0]
                    remove_files = file_list[1:]
                    
                    for file_to_remove in remove_files:
                        try:
                            file_size = file_to_remove.stat().st_size
                            file_to_remove.unlink()
                            numbered_files_removed += 1
                            self.files_removed += 1
                            self.space_saved += file_size
                            self.cleanup_log.append({
                                'action': 'REMOVED_NUMBERED_DUPLICATE',
                                'file': str(file_to_remove),
                                'kept': str(keep_file),
                                'size': file_size
                            })
                        except Exception as e:
                            logger.error(f"Error removing numbered duplicate {file_to_remove}: {e}")
        
        logger.info(f"Removed {numbered_files_removed} numbered duplicate files")
    
    def organize_remaining_files(self):
        """Organize remaining files into a clean structure"""
        logger.info("Organizing remaining files...")
        
        # Create main organization directories
        org_dirs = {
            'html_files': self.tehSiTes_dir / 'ORGANIZED' / 'html_files',
            'css_files': self.tehSiTes_dir / 'ORGANIZED' / 'css_files',
            'js_files': self.tehSiTes_dir / 'ORGANIZED' / 'js_files',
            'images': self.tehSiTes_dir / 'ORGANIZED' / 'images',
            'documents': self.tehSiTes_dir / 'ORGANIZED' / 'documents',
            'scripts': self.tehSiTes_dir / 'ORGANIZED' / 'scripts',
            'data': self.tehSiTes_dir / 'ORGANIZED' / 'data',
            'other': self.tehSiTes_dir / 'ORGANIZED' / 'other'
        }
        
        for dir_path in org_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # File type mappings
        file_types = {
            '.html': 'html_files',
            '.htm': 'html_files',
            '.css': 'css_files',
            '.js': 'js_files',
            '.png': 'images',
            '.jpg': 'images',
            '.jpeg': 'images',
            '.gif': 'images',
            '.svg': 'images',
            '.md': 'documents',
            '.txt': 'documents',
            '.pdf': 'documents',
            '.py': 'scripts',
            '.sh': 'scripts',
            '.json': 'data',
            '.csv': 'data',
            '.xml': 'data'
        }
        
        files_organized = 0
        for root, dirs, files in os.walk(self.tehSiTes_dir):
            # Skip organized directory and certain others
            if 'ORGANIZED' in root or any(skip in root for skip in ['node_modules', '.git', '__pycache__', '.venv']):
                continue
            
            for file in files:
                file_path = Path(root) / file
                if file_path.is_file():
                    # Determine file type
                    file_ext = file_path.suffix.lower()
                    target_dir = file_types.get(file_ext, 'other')
                    
                    # Move file to organized directory
                    try:
                        dest_path = org_dirs[target_dir] / file_path.name
                        if not dest_path.exists():
                            shutil.move(str(file_path), str(dest_path))
                            files_organized += 1
                            self.cleanup_log.append({
                                'action': 'ORGANIZED_FILE',
                                'file': str(file_path),
                                'destination': str(dest_path)
                            })
                    except Exception as e:
                        logger.error(f"Error organizing {file_path}: {e}")
        
        logger.info(f"Organized {files_organized} files into clean structure")
    
    def create_cleanup_report(self):
        """Create comprehensive cleanup report"""
        report_file = self.tehSiTes_dir / "TEHSITES_CLEANUP_REPORT.txt"
        
        with open(report_file, 'w') as f:
            f.write("=== TEHSITES COMPREHENSIVE CLEANUP REPORT ===\n\n")
            f.write(f"Cleanup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Time: {time.time() - self.start_time:.2f} seconds\n\n")
            
            f.write("=== SUMMARY ===\n")
            f.write(f"Duplicate Files Found: {self.duplicates_found}\n")
            f.write(f"Files Removed: {self.files_removed}\n")
            f.write(f"Space Saved: {self.space_saved / (CONSTANT_1024*CONSTANT_1024):.2f} MB\n")
            f.write(f"Directories Cleaned: {len([log for log in self.cleanup_log if log['action'] == 'REMOVED_EMPTY_DIR'])}\n")
            f.write(f"Files Organized: {len([log for log in self.cleanup_log if log['action'] == 'ORGANIZED_FILE'])}\n\n")
            
            f.write("=== CLEANUP ACTIONS ===\n")
            for log_entry in self.cleanup_log:
                f.write(f"{log_entry['action']}: {log_entry.get('file', log_entry.get('path', 'N/A'))}\n")
                if 'kept' in log_entry:
                    f.write(f"  Kept: {log_entry['kept']}\n")
                if 'size' in log_entry:
                    f.write(f"  Size: {log_entry['size']} bytes\n")
                f.write(Path("\n"))
            
            f.write("=== RECOMMENDATIONS ===\n")
            f.write("1. Review the ORGANIZED directory structure\n")
            f.write("2. Move important files to appropriate project directories\n")
            f.write("3. Consider archiving old backup directories\n")
            f.write("4. Set up regular cleanup to prevent future duplication\n")
            f.write("5. Use version control (git) to track file changes\n")
        
        logger.info(f"Cleanup report saved to {report_file}")
    
    def run_cleanup(self):
        """Run the complete cleanup process"""
        logger.info("Starting TehSiTes comprehensive cleanup...")
        
        self.find_duplicates()
        self.remove_duplicates()
        self.clean_numbered_duplicates()
        self.clean_empty_directories()
        self.organize_remaining_files()
        self.create_cleanup_report()
        
        logger.info("TehSiTes cleanup completed!")
        logger.info(f"Total files removed: {self.files_removed}")
        logger.info(f"Total space saved: {self.space_saved / (CONSTANT_1024*CONSTANT_1024):.2f} MB")

if __name__ == "__main__":
    tehSiTes_dir = Path("/Users/steven/tehSiTes")
    cleaner = TehSiTesCleanup(tehSiTes_dir)
    cleaner.run_cleanup()