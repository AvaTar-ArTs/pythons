"""
File Management Organize Tehsites 6

This module provides functionality for file management organize tehsites 6.

Author: Auto-generated
Date: 2025-11-01
"""


# Constants
CONSTANT_100 = 100
CONSTANT_200 = 200
CONSTANT_300 = 300
CONSTANT_400 = 400
CONSTANT_500 = 500
CONSTANT_600 = 600
CONSTANT_800 = 800
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024
CONSTANT_4096 = 4096

#!/usr/bin/env python3
"""
TehSiTes Targeted Directory Cleanup Script
Focuses on specific directories that need organization and cleanup
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

class TargetedTehSiTesCleanup:
    def __init__(self, target_directories):
        """__init__ function."""

        self.target_directories = [Path(d) for d in target_directories]
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
    
    def find_duplicates_in_targets(self):
        """Find duplicate files within target directories"""
        logger.info("Scanning target directories for duplicates...")
        
        total_files = 0
        for target_dir in self.target_directories:
            if not target_dir.exists():
                logger.warning(f"Directory does not exist: {target_dir}")
                continue
                
            logger.info(f"Scanning {target_dir.name}...")
            for root, dirs, files in os.walk(target_dir):
                # Skip certain directories
                if any(skip in root for skip in ['node_modules', '.git', '__pycache__', '.venv', 'ORGANIZED']):
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
    
    def remove_duplicates_with_priority(self):
        """Remove duplicate files with smart priority system"""
        logger.info("Removing duplicate files with priority system...")
        
        for file_hash, file_list in self.file_hashes.items():
            if len(file_list) > 1:
                # Sort files by priority
                    """file_priority function."""

                def file_priority(file_path):
                    path_str = str(file_path)
                    priority = 0
                    
                    # Highest priority for main project directories
                    if '03_Business_Platforms' in path_str:
                        priority += CONSTANT_1000
                    if 'Dr_Adu_GainesvillePFS_SEO_Project' in path_str:
                        priority += CONSTANT_800
                    if '15_Website_Hosting' in path_str:
                        priority += CONSTANT_600
                    if '05_Reports_Documentation' in path_str:
                        priority += CONSTANT_500
                    if 'avatararts.org' in path_str:
                        priority += CONSTANT_400
                    if 'DrAdu-SEO-OPTIMIZED' in path_str:
                        priority += CONSTANT_300
                    
                    # Medium priority for organized directories
                    if 'ORGANIZED' in path_str:
                        priority += CONSTANT_200
                    if '01_Core_AI_Development' in path_str:
                        priority += CONSTANT_100
                    if '02_Creative_Portfolio' in path_str:
                        priority += 50
                    
                    # Lower priority for messy directories
                    if 'New Folder With Items' in path_str:
                        priority -= CONSTANT_1000
                    if 'Archive' in path_str or 'Backup' in path_str:
                        priority -= CONSTANT_500
                    if '06_Archives_Backups' in path_str:
                        priority -= CONSTANT_300
                    
                    # Prefer shorter paths (less nested)
                    priority += (CONSTANT_100 - len(file_path.parts))
                    
                    # Prefer newer files
                    try:
                        priority += int(file_path.stat().st_mtime)
                    except (OSError, IOError, FileNotFoundError):
                        pass
                    
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
    
    def clean_new_folder_items(self):
        """Clean up the messy 'New Folder With Items' directories"""
        logger.info("Cleaning up 'New Folder With Items' directories...")
        
        new_folders = [d for d in self.target_directories if 'New Folder With Items' in str(d)]
        
        for folder in new_folders:
            if not folder.exists():
                continue
                
            logger.info(f"Processing {folder.name}...")
            
            # Move all files to a temporary organized structure
            temp_org_dir = folder.parent / f"{folder.name}_ORGANIZED"
            temp_org_dir.mkdir(exist_ok=True)
            
            # File type organization
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
                '.xml': 'data',
                '.zip': 'archives',
                '.tar': 'archives',
                '.gz': 'archives'
            }
            
            # Create organized subdirectories
            for subdir in ['html_files', 'css_files', 'js_files', 'images', 'documents', 'scripts', 'data', 'archives', 'other']:
                (temp_org_dir / subdir).mkdir(exist_ok=True)
            
            files_moved = 0
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = Path(root) / file
                    if file_path.is_file():
                        # Determine file type
                        file_ext = file_path.suffix.lower()
                        target_subdir = file_types.get(file_ext, 'other')
                        
                        # Move file to organized structure
                        try:
                            dest_path = temp_org_dir / target_subdir / file_path.name
                            if not dest_path.exists():
                                shutil.move(str(file_path), str(dest_path))
                                files_moved += 1
                                self.cleanup_log.append({
                                    'action': 'ORGANIZED_FROM_NEW_FOLDER',
                                    'file': str(file_path),
                                    'destination': str(dest_path)
                                })
                        except Exception as e:
                            logger.error(f"Error moving {file_path}: {e}")
            
            logger.info(f"Moved {files_moved} files from {folder.name}")
    
    def merge_similar_directories(self):
        """Merge similar directories and consolidate content"""
        logger.info("Merging similar directories...")
        
        # Group similar directories
        directory_groups = {
            'avatararts': [
                'avatararts-hub',
                'avatararts-gallery', 
                'avatararts-portfolio',
                'avatararts-tools',
                'avatararts.org'
            ],
            'dr_adu': [
                'DrAdu-SEO-OPTIMIZED',
                'Dr_Adu_GainesvillePFS_SEO_Project'
            ],
            'development': [
                '01_Core_AI_Development',
                '07_Active_Development'
            ]
        }
        
        for group_name, dirs in directory_groups.items():
            # Find existing directories
            existing_dirs = []
            for dir_name in dirs:
                for target_dir in self.target_directories:
                    if target_dir.name == dir_name and target_dir.exists():
                        existing_dirs.append(target_dir)
            
            if len(existing_dirs) > 1:
                logger.info(f"Merging {group_name} directories: {[d.name for d in existing_dirs]}")
                
                # Use the first directory as the main one
                main_dir = existing_dirs[0]
                merge_dirs = existing_dirs[1:]
                
                for merge_dir in merge_dirs:
                    try:
                        # Move contents to main directory
                        for item in merge_dir.iterdir():
                            dest_path = main_dir / item.name
                            if item.is_file():
                                if not dest_path.exists():
                                    shutil.move(str(item), str(dest_path))
                                    self.cleanup_log.append({
                                        'action': 'MERGED_FILE',
                                        'file': str(item),
                                        'destination': str(dest_path)
                                    })
                            elif item.is_dir():
                                if not dest_path.exists():
                                    shutil.move(str(item), str(dest_path))
                                    self.cleanup_log.append({
                                        'action': 'MERGED_DIRECTORY',
                                        'directory': str(item),
                                        'destination': str(dest_path)
                                    })
                        
                        # Remove empty directory
                        if not any(merge_dir.iterdir()):
                            merge_dir.rmdir()
                            self.cleanup_log.append({
                                'action': 'REMOVED_EMPTY_MERGED_DIR',
                                'directory': str(merge_dir)
                            })
                            
                    except Exception as e:
                        logger.error(f"Error merging {merge_dir}: {e}")
    
    def clean_empty_directories(self):
        """Remove empty directories"""
        logger.info("Cleaning empty directories...")
        
        empty_dirs_removed = 0
        for target_dir in self.target_directories:
            if not target_dir.exists():
                continue
                
            for root, dirs, files in os.walk(target_dir, topdown=False):
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
    
    def create_consolidation_report(self):
        """Create comprehensive consolidation report"""
        report_file = Path(Path("/Users/steven/tehSiTes")) / "TARGETED_CLEANUP_REPORT.txt"
        
        with open(report_file, 'w') as f:
            f.write("=== TEHSITES TARGETED CLEANUP REPORT ===\n\n")
            f.write(f"Cleanup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Time: {time.time() - self.start_time:.2f} seconds\n\n")
            
            f.write("=== TARGET DIRECTORIES ===\n")
            for target_dir in self.target_directories:
                f.write(f"- {target_dir}\n")
            f.write(Path("\n"))
            
            f.write("=== SUMMARY ===\n")
            f.write(f"Duplicate Files Found: {self.duplicates_found}\n")
            f.write(f"Files Removed: {self.files_removed}\n")
            f.write(f"Space Saved: {self.space_saved / (CONSTANT_1024*CONSTANT_1024):.2f} MB\n")
            f.write(f"Empty Directories Removed: {len([log for log in self.cleanup_log if log['action'] == 'REMOVED_EMPTY_DIR'])}\n")
            f.write(f"Files Organized: {len([log for log in self.cleanup_log if log['action'] == 'ORGANIZED_FROM_NEW_FOLDER'])}\n")
            f.write(f"Directories Merged: {len([log for log in self.cleanup_log if 'MERGED' in log['action']])}\n\n")
            
            f.write("=== CLEANUP ACTIONS ===\n")
            for log_entry in self.cleanup_log:
                f.write(f"{log_entry['action']}: {log_entry.get('file', log_entry.get('directory', log_entry.get('path', 'N/A')))}\n")
                if 'kept' in log_entry:
                    f.write(f"  Kept: {log_entry['kept']}\n")
                if 'destination' in log_entry:
                    f.write(f"  Destination: {log_entry['destination']}\n")
                if 'size' in log_entry:
                    f.write(f"  Size: {log_entry['size']} bytes\n")
                f.write(Path("\n"))
            
            f.write("=== RECOMMENDATIONS ===\n")
            f.write("1. Review merged directories for completeness\n")
            f.write("2. Consider archiving old 'New Folder With Items' directories\n")
            f.write("3. Set up regular cleanup schedules\n")
            f.write("4. Use version control for important projects\n")
            f.write("5. Implement consistent naming conventions\n")
        
        logger.info(f"Targeted cleanup report saved to {report_file}")
    
    def run_targeted_cleanup(self):
        """Run the complete targeted cleanup process"""
        logger.info("Starting targeted TehSiTes cleanup...")
        
        self.find_duplicates_in_targets()
        self.remove_duplicates_with_priority()
        self.clean_new_folder_items()
        self.merge_similar_directories()
        self.clean_empty_directories()
        self.create_consolidation_report()
        
        logger.info("Targeted cleanup completed!")
        logger.info(f"Total files removed: {self.files_removed}")
        logger.info(f"Total space saved: {self.space_saved / (CONSTANT_1024*CONSTANT_1024):.2f} MB")

if __name__ == "__main__":
    target_directories = [
        Path("/Users/steven/tehSiTes/avatararts-hub"),
        Path("/Users/steven/tehSiTes/01_Core_AI_Development"),
        Path("/Users/steven/tehSiTes/02_Business_and_Finance"),
        Path("/Users/steven/tehSiTes/02_Creative_Portfolio"),
        Path("/Users/steven/tehSiTes/03_Business_Platforms"),
        Path("/Users/steven/tehSiTes/04_Analysis_Documentation"),
        Path("/Users/steven/tehSiTes/05_Web_Assets"),
        Path("/Users/steven/tehSiTes/06_Archives_Backups"),
        Path("/Users/steven/tehSiTes/07_Active_Development"),
        Path("/Users/steven/tehSiTes/AvatarArts_MERGED"),
        Path("/Users/steven/tehSiTes/avatararts-gallery"),
        Path("/Users/steven/tehSiTes/avatararts-portfolio"),
        Path("/Users/steven/tehSiTes/avatararts-tools"),
        Path("/Users/steven/tehSiTes/avatararts.org"),
        Path("/Users/steven/tehSiTes/DrAdu-SEO-OPTIMIZED"),
        "/Users/steven/tehSiTes/New Folder With Items",
        "/Users/steven/tehSiTes/New Folder With Items 2",
        "/Users/steven/tehSiTes/New Folder With Items 3",
        "/Users/steven/tehSiTes/New Folder With Items 5",
        Path("/Users/steven/tehSiTes/ORGANIZED"),
        Path("/Users/steven/tehSiTes/QuantumForgeLabs_MERGED"),
        Path("/Users/steven/tehSiTes/src"),
        Path("/Users/steven/tehSiTes/static-projects"),
        Path("/Users/steven/tehSiTes/steven-chaplinski-artist")
    ]
    
    cleaner = TargetedTehSiTesCleanup(target_directories)
    cleaner.run_targeted_cleanup()