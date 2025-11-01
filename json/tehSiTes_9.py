"""
Tehsites 9

This module provides functionality for tehsites 9.

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
CONSTANT_700 = 700
CONSTANT_800 = 800
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024
CONSTANT_1200 = 1200
CONSTANT_1500 = 1500
CONSTANT_2000 = 2000
CONSTANT_4096 = 4096
CONSTANT_5000 = 5000

#!/usr/bin/env python3
"""
TehSiTes Deep Cleanup Script - 16+ Levels Deep
Comprehensive cleanup that goes deep into all folder structures
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
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DeepTehSiTesCleanup:
    def __init__(self, tehSiTes_dir):
        """__init__ function."""

        self.tehSiTes_dir = Path(tehSiTes_dir)
        self.file_hashes = defaultdict(list)
        self.duplicates_found = 0
        self.files_removed = 0
        self.space_saved = 0
        self.cleanup_log = []
        self.start_time = time.time()
        self.max_depth = 0
        self.deep_paths = []
        
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
    
    def find_deep_duplicates(self, max_depth=20):
        """Find duplicate files going 16+ levels deep"""
        logger.info(f"Scanning for duplicates up to {max_depth} levels deep...")
        
        total_files = 0
        deep_files = 0
        
        for root, dirs, files in os.walk(self.tehSiTes_dir):
            # Calculate current depth
            current_depth = len(Path(root).parts) - len(self.tehSiTes_dir.parts)
            self.max_depth = max(self.max_depth, current_depth)
            
            # Skip certain directories
            if any(skip in root for skip in ['node_modules', '.git', '__pycache__', '.venv']):
                continue
            
            # Track deep paths
            if current_depth >= 10:
                deep_files += 1
                if deep_files % CONSTANT_100 == 0:
                    logger.info(f"Found {deep_files} files at depth {current_depth}+")
                self.deep_paths.append((current_depth, root))
            
            for file in files:
                file_path = Path(root) / file
                if file_path.is_file():
                    total_files += 1
                    if total_files % CONSTANT_5000 == 0:
                        logger.info(f"Processed {total_files} files (max depth: {self.max_depth})...")
                    
                    file_hash = self.calculate_file_hash(file_path)
                    if file_hash:
                        self.file_hashes[file_hash].append(file_path)
        
        # Count duplicates
        for file_hash, file_list in self.file_hashes.items():
            if len(file_list) > 1:
                self.duplicates_found += len(file_list) - 1
        
        logger.info(f"Found {self.duplicates_found} duplicate files out of {total_files} total files")
        logger.info(f"Maximum depth reached: {self.max_depth}")
        logger.info(f"Files at depth 10+: {deep_files}")
    
    def remove_deep_duplicates(self):
        """Remove duplicate files with deep structure awareness"""
        logger.info("Removing duplicate files with deep structure priority...")
        
        for file_hash, file_list in self.file_hashes.items():
            if len(file_list) > 1:
                # Sort files by priority with deep structure awareness
                    """file_priority function."""

                def file_priority(file_path):
                    path_str = str(file_path)
                    priority = 0
                    
                    # Calculate depth penalty (shallow is better)
                    depth = len(file_path.parts) - len(self.tehSiTes_dir.parts)
                    depth_penalty = depth * 10  # Penalty for deep nesting
                    
                    # Highest priority for main project directories
                    if '03_Business_Platforms' in path_str:
                        priority += CONSTANT_2000
                    if 'Dr_Adu_GainesvillePFS_SEO_Project' in path_str:
                        priority += CONSTANT_1500
                    if '15_Website_Hosting' in path_str:
                        priority += CONSTANT_1200
                    if '05_Reports_Documentation' in path_str:
                        priority += CONSTANT_1000
                    if 'avatararts.org' in path_str:
                        priority += CONSTANT_800
                    if 'DrAdu-SEO-OPTIMIZED' in path_str:
                        priority += CONSTANT_700
                    
                    # Medium priority for organized directories
                    if 'ORGANIZED' in path_str:
                        priority += CONSTANT_600
                    if '01_Core_AI_Development' in path_str:
                        priority += CONSTANT_500
                    if '02_Creative_Portfolio' in path_str:
                        priority += CONSTANT_400
                    if 'avatararts' in path_str:
                        priority += CONSTANT_300
                    
                    # Lower priority for messy directories
                    if 'New Folder With Items' in path_str:
                        priority -= CONSTANT_2000
                    if 'Archive' in path_str or 'Backup' in path_str:
                        priority -= CONSTANT_1000
                    if '06_Archives_Backups' in path_str:
                        priority -= CONSTANT_800
                    
                    # Prefer shorter paths (less nested)
                    priority += (CONSTANT_200 - len(file_path.parts))
                    
                    # Prefer newer files
                    try:
                        priority += int(file_path.stat().st_mtime)
                    except (OSError, IOError, FileNotFoundError):
                        pass
                    
                    # Apply depth penalty
                    priority -= depth_penalty
                    
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
                            'action': 'REMOVED_DEEP_DUPLICATE',
                            'file': str(file_to_remove),
                            'kept': str(keep_file),
                            'size': file_size,
                            'depth': len(file_to_remove.parts) - len(self.tehSiTes_dir.parts)
                        })
                        logger.info(f"Removed duplicate: {file_to_remove.name} (depth: {len(file_to_remove.parts) - len(self.tehSiTes_dir.parts)})")
                    except Exception as e:
                        logger.error(f"Error removing {file_to_remove}: {e}")
    
    def clean_numbered_duplicates_deep(self):
        """Remove numbered duplicate files going deep"""
        logger.info("Cleaning numbered duplicate files at all depths...")
        
        numbered_files_removed = 0
        for root, dirs, files in os.walk(self.tehSiTes_dir):
            # Skip certain directories
            if any(skip in root for skip in ['node_modules', '.git', '__pycache__', '.venv', 'ORGANIZED']):
                continue
            
            # Group files by base name
            file_groups = defaultdict(list)
            for file in files:
                file_path = Path(root) / file
                if file_path.is_file():
                    # Extract base name (remove numbers and extensions)
                    base_name = file
                    # Remove common numbered patterns
                    base_name = re.sub(r'\s+\d+$', '', base_name)  # Remove trailing numbers
                    base_name = re.sub(r'\s+\(\d+\)$', '', base_name)  # Remove (1), (2), etc.
                    base_name = re.sub(r'\s+\d+\s*$', '', base_name)  # Remove trailing numbers with spaces
                    base_name = re.sub(r'_\d+$', '', base_name)  # Remove trailing _1, _2, etc.
                    base_name = re.sub(r'-\d+$', '', base_name)  # Remove trailing -1, -2, etc.
                    
                    file_groups[base_name].append(file_path)
            
            # For each group, keep the original and remove numbered versions
            for base_name, file_list in file_groups.items():
                if len(file_list) > 1:
                    # Sort by modification time and path length
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
                                'size': file_size,
                                'depth': len(file_to_remove.parts) - len(self.tehSiTes_dir.parts)
                            })
                        except Exception as e:
                            logger.error(f"Error removing numbered duplicate {file_to_remove}: {e}")
        
        logger.info(f"Removed {numbered_files_removed} numbered duplicate files")
    
    def flatten_deep_structures(self):
        """Flatten overly deep directory structures"""
        logger.info("Flattening deep directory structures...")
        
        # Find directories that are too deep
        deep_dirs = []
        for root, dirs, files in os.walk(self.tehSiTes_dir):
            current_depth = len(Path(root).parts) - len(self.tehSiTes_dir.parts)
            if current_depth > 12:  # Flatten directories deeper than 12 levels
                deep_dirs.append((current_depth, root))
        
        # Sort by depth (deepest first)
        deep_dirs.sort(key=lambda x: x[0], reverse=True)
        
        flattened_count = 0
        for depth, dir_path in deep_dirs:
            try:
                dir_path = Path(dir_path)
                if not dir_path.exists():
                    continue
                
                # Find a suitable parent directory to move files to
                parent_depth = 8  # Target depth
                current_path = dir_path
                target_path = None
                
                # Walk up the directory tree to find a suitable parent
                for _ in range(depth - parent_depth):
                    current_path = current_path.parent
                    if len(current_path.parts) - len(self.tehSiTes_dir.parts) <= parent_depth:
                        target_path = current_path
                        break
                
                if target_path and target_path != dir_path:
                    # Move files from deep directory to shallower location
                    for item in dir_path.iterdir():
                        if item.is_file():
                            dest_path = target_path / item.name
                            if not dest_path.exists():
                                shutil.move(str(item), str(dest_path))
                                flattened_count += 1
                                self.cleanup_log.append({
                                    'action': 'FLATTENED_DEEP_FILE',
                                    'file': str(item),
                                    'destination': str(dest_path),
                                    'original_depth': depth
                                })
                
                # Remove empty deep directory
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    self.cleanup_log.append({
                        'action': 'REMOVED_EMPTY_DEEP_DIR',
                        'directory': str(dir_path),
                        'depth': depth
                    })
                    
            except Exception as e:
                logger.error(f"Error flattening {dir_path}: {e}")
        
        logger.info(f"Flattened {flattened_count} files from deep structures")
    
    def clean_empty_directories_deep(self):
        """Remove empty directories at all depths"""
        logger.info("Cleaning empty directories at all depths...")
        
        empty_dirs_removed = 0
        for root, dirs, files in os.walk(self.tehSiTes_dir, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                try:
                    if not any(dir_path.iterdir()):  # Directory is empty
                        depth = len(dir_path.parts) - len(self.tehSiTes_dir.parts)
                        dir_path.rmdir()
                        empty_dirs_removed += 1
                        self.cleanup_log.append({
                            'action': 'REMOVED_EMPTY_DIR',
                            'path': str(dir_path),
                            'depth': depth
                        })
                except Exception as e:
                    logger.error(f"Error removing empty directory {dir_path}: {e}")
        
        logger.info(f"Removed {empty_dirs_removed} empty directories")
    
    def organize_remaining_files_deep(self):
        """Organize remaining files into a clean structure"""
        logger.info("Organizing remaining files into clean structure...")
        
        # Create main organization directories
        org_dirs = {
            'html_files': self.tehSiTes_dir / 'ORGANIZED_DEEP' / 'html_files',
            'css_files': self.tehSiTes_dir / 'ORGANIZED_DEEP' / 'css_files',
            'js_files': self.tehSiTes_dir / 'ORGANIZED_DEEP' / 'js_files',
            'images': self.tehSiTes_dir / 'ORGANIZED_DEEP' / 'images',
            'documents': self.tehSiTes_dir / 'ORGANIZED_DEEP' / 'documents',
            'scripts': self.tehSiTes_dir / 'ORGANIZED_DEEP' / 'scripts',
            'data': self.tehSiTes_dir / 'ORGANIZED_DEEP' / 'data',
            'archives': self.tehSiTes_dir / 'ORGANIZED_DEEP' / 'archives',
            'other': self.tehSiTes_dir / 'ORGANIZED_DEEP' / 'other'
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
            '.xml': 'data',
            '.zip': 'archives',
            '.tar': 'archives',
            '.gz': 'archives'
        }
        
        files_organized = 0
        for root, dirs, files in os.walk(self.tehSiTes_dir):
            # Skip organized directories
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
                                'action': 'ORGANIZED_DEEP_FILE',
                                'file': str(file_path),
                                'destination': str(dest_path),
                                'depth': len(file_path.parts) - len(self.tehSiTes_dir.parts)
                            })
                    except Exception as e:
                        logger.error(f"Error organizing {file_path}: {e}")
        
        logger.info(f"Organized {files_organized} files into clean structure")
    
    def create_deep_cleanup_report(self):
        """Create comprehensive deep cleanup report"""
        report_file = self.tehSiTes_dir / "DEEP_CLEANUP_REPORT.txt"
        
        with open(report_file, 'w') as f:
            f.write("=== TEHSITES DEEP CLEANUP REPORT ===\n\n")
            f.write(f"Cleanup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Time: {time.time() - self.start_time:.2f} seconds\n\n")
            
            f.write("=== DEPTH ANALYSIS ===\n")
            f.write(f"Maximum Depth Reached: {self.max_depth}\n")
            f.write(f"Files at Depth 10+: {len(self.deep_paths)}\n")
            f.write(f"Deepest Paths Found:\n")
            for depth, path in sorted(self.deep_paths, key=lambda x: x[0], reverse=True)[:20]:
                f.write(f"  Depth {depth}: {path}\n")
            f.write(Path("\n"))
            
            f.write("=== SUMMARY ===\n")
            f.write(f"Duplicate Files Found: {self.duplicates_found}\n")
            f.write(f"Files Removed: {self.files_removed}\n")
            f.write(f"Space Saved: {self.space_saved / (CONSTANT_1024*CONSTANT_1024):.2f} MB\n")
            f.write(f"Empty Directories Removed: {len([log for log in self.cleanup_log if log['action'] == 'REMOVED_EMPTY_DIR'])}\n")
            f.write(f"Files Organized: {len([log for log in self.cleanup_log if log['action'] == 'ORGANIZED_DEEP_FILE'])}\n")
            f.write(f"Deep Files Flattened: {len([log for log in self.cleanup_log if log['action'] == 'FLATTENED_DEEP_FILE'])}\n\n")
            
            f.write("=== CLEANUP ACTIONS ===\n")
            for log_entry in self.cleanup_log:
                f.write(f"{log_entry['action']}: {log_entry.get('file', log_entry.get('directory', log_entry.get('path', 'N/A')))}\n")
                if 'kept' in log_entry:
                    f.write(f"  Kept: {log_entry['kept']}\n")
                if 'destination' in log_entry:
                    f.write(f"  Destination: {log_entry['destination']}\n")
                if 'size' in log_entry:
                    f.write(f"  Size: {log_entry['size']} bytes\n")
                if 'depth' in log_entry:
                    f.write(f"  Depth: {log_entry['depth']}\n")
                f.write(Path("\n"))
            
            f.write("=== RECOMMENDATIONS ===\n")
            f.write("1. Review the ORGANIZED_DEEP directory structure\n")
            f.write("2. Consider archiving very deep directory structures\n")
            f.write("3. Set up regular deep cleanup schedules\n")
            f.write("4. Use version control for important projects\n")
            f.write("5. Implement consistent directory depth limits\n")
            f.write("6. Consider using symbolic links for deep structures\n")
        
        logger.info(f"Deep cleanup report saved to {report_file}")
    
    def run_deep_cleanup(self):
        """Run the complete deep cleanup process"""
        logger.info("Starting deep TehSiTes cleanup (16+ levels)...")
        
        self.find_deep_duplicates(max_depth=20)
        self.remove_deep_duplicates()
        self.clean_numbered_duplicates_deep()
        self.flatten_deep_structures()
        self.clean_empty_directories_deep()
        self.organize_remaining_files_deep()
        self.create_deep_cleanup_report()
        
        logger.info("Deep cleanup completed!")
        logger.info(f"Total files removed: {self.files_removed}")
        logger.info(f"Total space saved: {self.space_saved / (CONSTANT_1024*CONSTANT_1024):.2f} MB")
        logger.info(f"Maximum depth reached: {self.max_depth}")

if __name__ == "__main__":
    tehSiTes_dir = Path("/Users/steven/tehSiTes")
    cleaner = DeepTehSiTesCleanup(tehSiTes_dir)
    cleaner.run_deep_cleanup()