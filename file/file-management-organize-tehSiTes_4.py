"""
File Management Organize Tehsites 4

This module provides functionality for file management organize tehsites 4.

Author: Auto-generated
Date: 2025-11-01
"""


# Constants
CONSTANT_100 = 100
CONSTANT_300 = 300
CONSTANT_400 = 400
CONSTANT_500 = 500
CONSTANT_600 = 600
CONSTANT_800 = 800
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024
CONSTANT_4096 = 4096
CONSTANT_5000 = 5000

#!/usr/bin/env python3
"""
TehSiTes Ultimate Deep Research & Content-Aware Cleanup
Combines all analysis techniques: merge, diff, remove, organize with deep intelligence
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
import difflib
from typing import Dict, List, Tuple, Set

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UltimateTehSiTesCleanup:
    def __init__(self, tehSiTes_dir):
        """__init__ function."""

        self.tehSiTes_dir = Path(tehSiTes_dir)
        self.file_hashes = defaultdict(list)
        self.content_analysis = {}
        self.similar_files = defaultdict(list)
        self.duplicates_found = 0
        self.files_removed = 0
        self.space_saved = 0
        self.merge_log = []
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
    
    def deep_content_analysis(self, file_path):
        """Perform deep content analysis on a file"""
        analysis = {
            'path': str(file_path),
            'name': file_path.name,
            'size': file_path.stat().st_size,
            'extension': file_path.suffix.lower(),
            'keywords': set(),
            'content_type': 'unknown',
            'has_avatararts': False,
            'has_quantumforgelabs': False,
            'has_dr_adu': False,
            'has_seo': False,
            'has_portfolio': False,
            'has_gallery': False,
            'has_tools': False,
            'has_react': False,
            'has_nextjs': False,
            'has_python': False,
            'has_node': False,
            'is_duplicate': False,
            'is_similar': False,
            'similar_files': [],
            'depth': len(file_path.parts) - len(self.tehSiTes_dir.parts)
        }
        
        try:
            # Analyze file content
            if file_path.suffix.lower() in ['.md', '.txt', '.html', '.js', '.py', '.json', '.jsx', '.tsx', '.ts', '.css']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                    
                    # Keyword analysis
                    keywords = {
                        'avatararts': ['avatararts', 'avatar arts'],
                        'quantumforgelabs': ['quantumforgelabs', 'quantum forge labs'],
                        'dr_adu': ['dr.adu', 'dr adu', 'gainesville', 'pfs'],
                        'seo': ['seo', 'search engine', 'optimization'],
                        'portfolio': ['portfolio', 'showcase'],
                        'gallery': ['gallery', 'gallery'],
                        'tools': ['tools', 'utilities', 'utilities'],
                        'react': ['react', 'jsx', 'component'],
                        'nextjs': ['next', 'nextjs', 'next.js'],
                        'python': ['python', 'import ', 'def ', 'class '],
                        'node': ['node', 'npm', 'package.json']
                    }
                    
                    for category, terms in keywords.items():
                        if any(term in content for term in terms):
                            analysis[f'has_{category}'] = True
                            analysis['keywords'].add(category)
            
            # Determine content type
            analysis['content_type'] = self.determine_content_type(analysis)
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            
        return analysis
    
    def determine_content_type(self, analysis):
        """Determine content type based on analysis"""
        if analysis['has_avatararts']:
            if analysis['has_gallery']:
                return 'avatararts_gallery'
            elif analysis['has_portfolio']:
                return 'avatararts_portfolio'
            elif analysis['has_tools']:
                return 'avatararts_tools'
            else:
                return 'avatararts_general'
        elif analysis['has_quantumforgelabs']:
            return 'quantumforgelabs'
        elif analysis['has_dr_adu']:
            return 'dr_adu'
        elif analysis['has_seo']:
            return 'seo'
        elif analysis['has_react'] or analysis['has_nextjs']:
            return 'web_development'
        elif analysis['has_python']:
            return 'python_development'
        elif analysis['has_node']:
            return 'node_development'
        elif analysis['extension'] in ['.html', '.htm']:
            return 'html'
        elif analysis['extension'] in ['.css']:
            return 'css'
        elif analysis['extension'] in ['.js', '.jsx', '.ts', '.tsx']:
            return 'javascript'
        elif analysis['extension'] in ['.py']:
            return 'python'
        elif analysis['extension'] in ['.md', '.txt']:
            return 'documentation'
        elif analysis['extension'] in ['.json', '.xml', '.csv']:
            return 'data'
        else:
            return 'other'
    
    def find_similar_files(self, file_path, analysis):
        """Find files similar to the given file"""
        similar_files = []
        
        try:
            # Find files with similar names
            name_parts = re.split(r'[_\-\s]+', analysis['name'].lower())
            name_parts = [part for part in name_parts if len(part) > 2]
            
            for other_path, other_analysis in self.content_analysis.items():
                if other_path == file_path:
                    continue
                
                # Check if files are similar
                similarity_score = 0
                
                # Name similarity
                other_name_parts = re.split(r'[_\-\s]+', other_analysis['name'].lower())
                other_name_parts = [part for part in other_name_parts if len(part) > 2]
                
                common_parts = set(name_parts) & set(other_name_parts)
                if common_parts:
                    similarity_score += len(common_parts) * 10
                
                # Content type similarity
                if analysis['content_type'] == other_analysis['content_type']:
                    similarity_score += 20
                
                # Keyword similarity
                common_keywords = analysis['keywords'] & other_analysis['keywords']
                if common_keywords:
                    similarity_score += len(common_keywords) * 15
                
                # Size similarity (within 10%)
                size_diff = abs(analysis['size'] - other_analysis['size'])
                if analysis['size'] > 0:
                    size_ratio = size_diff / analysis['size']
                    if size_ratio < 0.1:
                        similarity_score += 10
                
                # If similarity score is high enough, consider them similar
                if similarity_score >= 30:
                    similar_files.append((other_path, similarity_score))
            
            # Sort by similarity score
            similar_files.sort(key=lambda x: x[1], reverse=True)
            
        except Exception as e:
            logger.error(f"Error finding similar files for {file_path}: {e}")
        
        return similar_files
    
    def compare_files(self, file1_path, file2_path):
        """Compare two files and determine if they're duplicates or similar"""
        try:
            # Check if files are identical
            if file1_path.stat().st_size == file2_path.stat().st_size:
                hash1 = self.calculate_file_hash(file1_path)
                hash2 = self.calculate_file_hash(file2_path)
                if hash1 and hash2 and hash1 == hash2:
                    return 'identical'
            
            # Check if files are similar (for text files)
            if file1_path.suffix.lower() in ['.md', '.txt', '.html', '.js', '.py', '.json']:
                with open(file1_path, 'r', encoding='utf-8', errors='ignore') as f1:
                    content1 = f1.read()
                with open(file2_path, 'r', encoding='utf-8', errors='ignore') as f2:
                    content2 = f2.read()
                
                # Calculate similarity ratio
                similarity = difflib.SequenceMatcher(None, content1, content2).ratio()
                if similarity > 0.9:
                    return 'very_similar'
                elif similarity > 0.7:
                    return 'similar'
            
            return 'different'
            
        except Exception as e:
            logger.error(f"Error comparing files {file1_path} and {file2_path}: {e}")
            return 'different'
    
    def analyze_all_files(self):
        """Analyze all files in the directory"""
        logger.info("Performing deep content analysis on all files...")
        
        total_files = 0
        for root, dirs, files in os.walk(self.tehSiTes_dir):
            # Skip certain directories
            if any(skip in root for skip in ['node_modules', '.git', '__pycache__', '.venv', 'DEEP_ORGANIZED']):
                continue
            
            current_depth = len(Path(root).parts) - len(self.tehSiTes_dir.parts)
            self.max_depth = max(self.max_depth, current_depth)
            
            for file in files:
                file_path = Path(root) / file
                if file_path.is_file():
                    total_files += 1
                    if total_files % CONSTANT_5000 == 0:
                        logger.info(f"Analyzed {total_files} files...")
                    
                    analysis = self.deep_content_analysis(file_path)
                    self.content_analysis[file_path] = analysis
                    
                    # Track deep paths
                    if current_depth >= 8:
                        self.deep_paths.append(analysis)
        
        logger.info(f"Analysis complete: {total_files} files analyzed, max depth: {self.max_depth}")
    
    def find_duplicates_and_similar(self):
        """Find duplicate and similar files"""
        logger.info("Finding duplicates and similar files...")
        
        # Group files by hash for exact duplicates
        for file_path, analysis in self.content_analysis.items():
            file_hash = self.calculate_file_hash(file_path)
            if file_hash:
                self.file_hashes[file_hash].append(file_path)
        
        # Find exact duplicates
        for file_hash, file_list in self.file_hashes.items():
            if len(file_list) > 1:
                self.duplicates_found += len(file_list) - 1
                # Mark all but the first as duplicates
                for file_path in file_list[1:]:
                    self.content_analysis[file_path]['is_duplicate'] = True
        
        # Find similar files
        for file_path, analysis in self.content_analysis.items():
            if analysis['is_duplicate']:
                continue
            
            similar_files = self.find_similar_files(file_path, analysis)
            if similar_files:
                analysis['is_similar'] = True
                analysis['similar_files'] = similar_files[:5]  # Keep top 5 similar files
                
                # Mark similar files
                for similar_path, score in similar_files[:3]:  # Mark top 3 as similar
                    if similar_path in self.content_analysis:
                        self.content_analysis[similar_path]['is_similar'] = True
        
        logger.info(f"Found {self.duplicates_found} exact duplicates and {sum(1 for a in self.content_analysis.values() if a['is_similar'])} similar files")
    
    def remove_duplicates(self):
        """Remove duplicate files, keeping the best version"""
        logger.info("Removing duplicate files...")
        
        for file_hash, file_list in self.file_hashes.items():
            if len(file_list) > 1:
                # Sort by priority (best file first)
                    """file_priority function."""

                def file_priority(file_path):
                    analysis = self.content_analysis[file_path]
                    priority = 0
                    
                    # Prefer files with more content
                    priority += analysis['size'] // CONSTANT_1000
                    
                    # Prefer files with more keywords
                    priority += len(analysis['keywords']) * CONSTANT_100
                    
                    # Prefer files in main directories
                    path_str = str(file_path)
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
                    
                    # Prefer shorter paths
                    priority += (CONSTANT_100 - len(file_path.parts))
                    
                    # Prefer newer files
                    try:
                        priority += int(file_path.stat().st_mtime)
                    except (OSError, IOError, FileNotFoundError):
                        pass
                    
                    return priority
                
                # Sort by priority
                file_list.sort(key=file_priority, reverse=True)
                
                # Keep the first (best) file, remove the rest
                keep_file = file_list[0]
                remove_files = file_list[1:]
                
                for file_to_remove in remove_files:
                    try:
                        file_size = file_to_remove.stat().st_size
                        file_to_remove.unlink()
                        self.files_removed += 1
                        self.space_saved += file_size
                        self.merge_log.append({
                            'action': 'REMOVED_DUPLICATE',
                            'file': str(file_to_remove),
                            'kept': str(keep_file),
                            'size': file_size
                        })
                        logger.info(f"Removed duplicate: {file_to_remove.name}")
                    except Exception as e:
                        logger.error(f"Error removing {file_to_remove}: {e}")
    
    def merge_similar_files(self):
        """Merge similar files intelligently"""
        logger.info("Merging similar files...")
        
        merged_count = 0
        for file_path, analysis in self.content_analysis.items():
            if not analysis['is_similar'] or analysis['is_duplicate']:
                continue
            
            similar_files = analysis['similar_files']
            if not similar_files:
                continue
            
            # Find the best similar file to merge with
            best_similar = None
            best_score = 0
            
            for similar_path, score in similar_files:
                if similar_path in self.content_analysis and not self.content_analysis[similar_path]['is_duplicate']:
                    if score > best_score:
                        best_score = score
                        best_similar = similar_path
            
            if best_similar and best_similar.exists():
                try:
                    # Compare files to determine merge strategy
                    comparison = self.compare_files(file_path, best_similar)
                    
                    if comparison == 'identical':
                        # Remove duplicate
                        file_size = file_path.stat().st_size
                        file_path.unlink()
                        self.files_removed += 1
                        self.space_saved += file_size
                        self.merge_log.append({
                            'action': 'REMOVED_IDENTICAL_SIMILAR',
                            'file': str(file_path),
                            'kept': str(best_similar),
                            'size': file_size
                        })
                        merged_count += 1
                        
                    elif comparison in ['very_similar', 'similar']:
                        # Create a merged version
                        merged_name = f"{file_path.stem}_merged{file_path.suffix}"
                        merged_path = file_path.parent / merged_name
                        
                        # For now, just keep the better file
                        if analysis['size'] > self.content_analysis[best_similar]['size']:
                            shutil.move(str(file_path), str(merged_path))
                            self.merge_log.append({
                                'action': 'MERGED_SIMILAR',
                                'file': str(file_path),
                                'destination': str(merged_path),
                                'similar_to': str(best_similar)
                            })
                        else:
                            shutil.move(str(best_similar), str(merged_path))
                            self.merge_log.append({
                                'action': 'MERGED_SIMILAR',
                                'file': str(best_similar),
                                'destination': str(merged_path),
                                'similar_to': str(file_path)
                            })
                        merged_count += 1
                        
                except Exception as e:
                    logger.error(f"Error merging {file_path} with {best_similar}: {e}")
        
        logger.info(f"Merged {merged_count} similar files")
    
    def organize_by_content_type(self):
        """Organize files by content type"""
        logger.info("Organizing files by content type...")
        
        # Create organized directories
        organized_base = self.tehSiTes_dir / "ULTIMATE_ORGANIZED"
        organized_base.mkdir(exist_ok=True)
        
        content_type_dirs = {}
        for analysis in self.content_analysis.values():
            content_type = analysis['content_type']
            if content_type not in content_type_dirs:
                content_type_dirs[content_type] = organized_base / content_type
                content_type_dirs[content_type].mkdir(exist_ok=True)
        
        # Move files to appropriate directories
        moved_count = 0
        for file_path, analysis in self.content_analysis.items():
            if not file_path.exists():
                continue
            
            content_type = analysis['content_type']
            target_dir = content_type_dirs[content_type]
            
            try:
                # Create a unique name if file already exists
                target_path = target_dir / file_path.name
                counter = 1
                while target_path.exists():
                    stem = file_path.stem
                    suffix = file_path.suffix
                    target_path = target_dir / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                shutil.move(str(file_path), str(target_path))
                self.merge_log.append({
                    'action': 'ORGANIZED_BY_TYPE',
                    'file': str(file_path),
                    'destination': str(target_path),
                    'content_type': content_type
                })
                moved_count += 1
                
            except Exception as e:
                logger.error(f"Error organizing {file_path}: {e}")
        
        logger.info(f"Organized {moved_count} files by content type")
    
    def create_ultimate_report(self):
        """Create comprehensive ultimate cleanup report"""
        report_file = self.tehSiTes_dir / "ULTIMATE_CLEANUP_REPORT.txt"
        
        with open(report_file, 'w') as f:
            f.write("=== TEHSITES ULTIMATE CLEANUP REPORT ===\n\n")
            f.write(f"Cleanup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Time: {time.time() - self.start_time:.2f} seconds\n\n")
            
            f.write("=== ANALYSIS SUMMARY ===\n")
            f.write(f"Files Analyzed: {len(self.content_analysis)}\n")
            f.write(f"Maximum Depth: {self.max_depth}\n")
            f.write(f"Deep Paths Found: {len(self.deep_paths)}\n")
            f.write(f"Exact Duplicates Found: {self.duplicates_found}\n")
            f.write(f"Similar Files Found: {sum(1 for a in self.content_analysis.values() if a['is_similar'])}\n\n")
            
            f.write("=== CONTENT TYPE BREAKDOWN ===\n")
            content_types = defaultdict(int)
            for analysis in self.content_analysis.values():
                content_types[analysis['content_type']] += 1
            
            for content_type, count in sorted(content_types.items()):
                f.write(f"{content_type}: {count} files\n")
            f.write(Path("\n"))
            
            f.write("=== CLEANUP SUMMARY ===\n")
            f.write(f"Files Removed: {self.files_removed}\n")
            f.write(f"Space Saved: {self.space_saved / (CONSTANT_1024*CONSTANT_1024):.2f} MB\n")
            f.write(f"Cleanup Actions: {len(self.merge_log)}\n\n")
            
            f.write("=== CLEANUP ACTIONS ===\n")
            for log_entry in self.merge_log:
                f.write(f"{log_entry['action']}: {log_entry.get('file', 'N/A')}\n")
                if 'kept' in log_entry:
                    f.write(f"  Kept: {log_entry['kept']}\n")
                if 'destination' in log_entry:
                    f.write(f"  Destination: {log_entry['destination']}\n")
                if 'size' in log_entry:
                    f.write(f"  Size: {log_entry['size']} bytes\n")
                if 'content_type' in log_entry:
                    f.write(f"  Content Type: {log_entry['content_type']}\n")
                f.write(Path("\n"))
            
            f.write("=== RECOMMENDATIONS ===\n")
            f.write("1. Review the ULTIMATE_ORGANIZED directory structure\n")
            f.write("2. Test merged files to ensure functionality\n")
            f.write("3. Update any hardcoded paths in projects\n")
            f.write("4. Consider archiving old backup directories\n")
            f.write("5. Implement regular cleanup schedules\n")
            f.write("6. Use version control for important projects\n")
        
        logger.info(f"Ultimate cleanup report saved to {report_file}")
    
    def run_ultimate_cleanup(self):
        """Run the complete ultimate cleanup process"""
        logger.info("Starting ultimate TehSiTes cleanup with deep research...")
        
        # Step 1: Analyze all files
        self.analyze_all_files()
        
        # Step 2: Find duplicates and similar files
        self.find_duplicates_and_similar()
        
        # Step 3: Remove duplicates
        self.remove_duplicates()
        
        # Step 4: Merge similar files
        self.merge_similar_files()
        
        # Step 5: Organize by content type
        self.organize_by_content_type()
        
        # Step 6: Create comprehensive report
        self.create_ultimate_report()
        
        logger.info("Ultimate cleanup completed!")
        logger.info(f"Total files removed: {self.files_removed}")
        logger.info(f"Total space saved: {self.space_saved / (CONSTANT_1024*CONSTANT_1024):.2f} MB")

if __name__ == "__main__":
    tehSiTes_dir = Path("/Users/steven/tehSiTes")
    cleaner = UltimateTehSiTesCleanup(tehSiTes_dir)
    cleaner.run_ultimate_cleanup()