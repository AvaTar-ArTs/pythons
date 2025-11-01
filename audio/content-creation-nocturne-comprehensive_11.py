#!/usr/bin/env python3
"""
Merged Content Analysis Tool

This file was automatically merged from the following source files:
- /Users/steven/Music/nocTurneMeLoDieS/python/comprehensive_merge.py
- /Users/steven/Music/nocTurneMeLoDieS/python/FINAL_ORGANIZED/core_analysis/comprehensive_merge.py

Combines the best features and functionality from multiple similar files.
"""

# Imports from all source files
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import hashlib
import json
import logging
import os
import re
import shutil
import sys
import zipfile

# Documentation from source files
        """Determine file category based on content, filename, and extension."""
            has_docstring = '"""' in content or "'''" in content
        """Clean up temporary files."""
"""
        """Create a clean filename based on analysis."""
        """Collect all files from all sources."""
        """Find duplicates and select the best version of each file."""
        """Organize files into the final structure."""
        """Run the complete merge and consolidation process."""
        """Extract Archive.zip contents to temp directory."""
    """Main function."""
        """Create the final organized directory structure."""
        """Generate comprehensive merge report."""
        """Analyze file content to determine category and quality."""
        """Calculate MD5 hash of file content."""

Comprehensive Merge and Consolidation Tool

This script merges and combines all Python directories and files from multiple sources:
- Main directory files
- Archive directory
- Archive.zip contents
- CLEAN_ORGANIZED directory
- Consolidated directory
- DUPLICATES_ARCHIVE
- Sorted directory
- transcribe-keywords directory
- Various documentation and log files

It creates a single, unified, organized structure with all the best features.
"""

import os
import sys
import logging
import shutil
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import re
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('comprehensive_merge.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ComprehensiveMerger:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.merged_dir = self.base_dir / "MERGED_UNIFIED"
        self.temp_dir = self.base_dir / "TEMP_EXTRACTION"
        self.final_dir = self.base_dir / "FINAL_ORGANIZED"
        
        # Source directories to merge
        self.sources = {
            'main': self.base_dir,
            'archive': self.base_dir / "Archive",
            'archive_zip': self.base_dir / "Archive.zip",
            'clean_organized': self.base_dir / "CLEAN_ORGANIZED",
            'consolidated': self.base_dir / "Consolidated",
            'duplicates_archive': self.base_dir / "DUPLICATES_ARCHIVE",
            'sorted': self.base_dir / "Sorted",
            'transcribe_keywords': self.base_dir / "transcribe-keywords",
            'reports': self.base_dir / "REPORTS"
        }
        
        # File categories for final organization
        self.categories = {
            'core_analysis': 'Core Analysis & Processing Scripts',
            'transcription': 'Transcription & Speech Processing',
            'generation': 'Content Generation & Creation',
            'processing': 'File Processing & Conversion',
            'web_scraping': 'Web Scraping & Data Extraction',
            'organization': 'File Organization & Management',
            'utilities': 'Utility Scripts & Tools',
            'documentation': 'Documentation & Reports',
            'scripts': 'Shell Scripts & Automation',
            'config': 'Configuration & Requirements',
            'logs': 'Log Files & Debugging',
            'experimental': 'Experimental & Test Scripts',
            'archived': 'Archived & Legacy Scripts'
        }
        
        # File hash cache for duplicate detection
        self.file_hashes = {}
        self.processed_files = set()
        self.merge_stats = {
            'total_files_found': 0,
            'unique_files_kept': 0,
            'duplicates_merged': 0,
            'files_organized': 0,
            'categories_created': 0
        }

    def extract_archive_zip(self):
        """Extract Archive.zip contents to temp directory."""
        logger.info("Extracting Archive.zip...")
        
        self.temp_dir.mkdir(exist_ok=True)
        
        try:
            with zipfile.ZipFile(self.sources['archive_zip'], 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
            logger.info(f"Archive.zip extracted to {self.temp_dir}")
            return True
        except Exception as e:
            logger.error(f"Error extracting Archive.zip: {e}")
            return False

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content."""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            return hashlib.md5(content).hexdigest()
        except Exception as e:
            logger.warning(f"Could not calculate hash for {file_path}: {e}")
            return ""

    def analyze_file_content(self, file_path: Path) -> Dict:
        """Analyze file content to determine category and quality."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic content analysis
            lines = content.split('\n')
            non_empty_lines = [line for line in lines if line.strip()]
            
            # Quality indicators
            has_docstring = '"""' in content or "'''" in content
            has_logging = 'logging' in content.lower()
            has_error_handling = 'try:' in content and 'except' in content
            has_main_function = 'if __name__ == "__main__":' in content
            has_imports = len([line for line in lines if line.strip().startswith('import') or line.strip().startswith('from')])
            
            # Determine category based on content and filename
            category = self._determine_category(content, file_path.name, file_path.suffix)
            
            # Calculate quality score
            quality_score = 0
            if has_docstring: quality_score += 2
            if has_logging: quality_score += 1
            if has_error_handling: quality_score += 2
            if has_main_function: quality_score += 1
            if has_imports > 5: quality_score += 1
            
            return {
                'file_path': file_path,
                'category': category,
                'quality_score': quality_score,
                'lines': len(lines),
                'non_empty_lines': len(non_empty_lines),
                'has_docstring': has_docstring,
                'has_logging': has_logging,
                'has_error_handling': has_error_handling,
                'has_main_function': has_main_function,
                'imports_count': has_imports,
                'size': file_path.stat().st_size,
                'modified': file_path.stat().st_mtime
            }
            
        except Exception as e:
            logger.warning(f"Could not analyze {file_path}: {e}")
            return {
                'file_path': file_path,
                'category': 'utilities',
                'quality_score': 0,
                'lines': 0,
                'non_empty_lines': 0,
                'has_docstring': False,
                'has_logging': False,
                'has_error_handling': False,
                'has_main_function': False,
                'imports_count': 0,
                'size': 0,
                'modified': 0
            }

    def _determine_category(self, content: str, filename: str, extension: str) -> str:
        """Determine file category based on content, filename, and extension."""
        content_lower = content.lower()
        filename_lower = filename.lower()
        
        # Shell scripts
        if extension in ['.sh', '.bash'] or filename_lower.endswith('.sh'):
            return 'scripts'
        
        # Configuration files
        if extension in ['.txt', '.md', '.log'] or 'requirements' in filename_lower or 'config' in filename_lower:
            if 'requirements' in filename_lower:
                return 'config'
            elif 'log' in filename_lower:
                return 'logs'
            else:
                return 'documentation'
        
        # Python files - analyze content
        if extension == '.py':
            # Analysis scripts
            if any(keyword in content_lower for keyword in ['analyze', 'analysis', 'analyzer']):
                return 'core_analysis'
            
            # Transcription scripts
            if any(keyword in content_lower for keyword in ['transcribe', 'transcript', 'whisper', 'speech']):
                return 'transcription'
            
            # Generation scripts
            if any(keyword in content_lower for keyword in ['generate', 'create', 'build', 'html', 'csv']):
                return 'generation'
            
            # Processing scripts
            if any(keyword in content_lower for keyword in ['process', 'convert', 'mp3', 'mp4', 'ffmpeg']):
                return 'processing'
            
            # Web scraping scripts
            if any(keyword in content_lower for keyword in ['scrape', 'suno', 'beautifulsoup', 'requests']):
                return 'web_scraping'
            
            # Organization scripts
            if any(keyword in content_lower for keyword in ['organize', 'sort', 'manage', 'file']):
                return 'organization'
            
            # Experimental/test scripts
            if any(keyword in filename_lower for keyword in ['test', 'experimental', 'untitled', 'copy']):
                return 'experimental'
            
            return 'utilities'
        
        # Default category
        return 'utilities'

    def collect_all_files(self) -> Dict[str, List[Path]]:
        """Collect all files from all sources."""
        logger.info("Collecting files from all sources...")
        
        all_files = defaultdict(list)
        
        for source_name, source_path in self.sources.items():
            if not source_path.exists():
                logger.warning(f"Source not found: {source_path}")
                continue
            
            logger.info(f"Scanning {source_name}: {source_path}")
            
            if source_path.is_file() and source_path.suffix == '.zip':
                # Handle zip files
                continue  # Will be handled separately
            
            # Collect files from directory
            for file_path in source_path.rglob("*"):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    all_files[source_name].append(file_path)
                    self.merge_stats['total_files_found'] += 1
        
        # Handle extracted zip contents
        if self.temp_dir.exists():
            for file_path in self.temp_dir.rglob("*"):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    all_files['archive_extracted'].append(file_path)
                    self.merge_stats['total_files_found'] += 1
        
        logger.info(f"Collected {self.merge_stats['total_files_found']} files from all sources")
        return all_files

    def find_and_merge_duplicates(self, all_files: Dict[str, List[Path]]) -> Dict[str, Path]:
        """Find duplicates and select the best version of each file."""
        logger.info("Finding and merging duplicates...")
        
        # Group files by content hash
        hash_to_files = defaultdict(list)
        
        for source_name, files in all_files.items():
            for file_path in files:
                if file_path.exists():
                    file_hash = self.calculate_file_hash(file_path)
                    if file_hash:
                        hash_to_files[file_hash].append((file_path, source_name))
        
        # Select best file from each group
        best_files = {}
        duplicate_groups = {}
        
        for file_hash, file_list in hash_to_files.items():
            if len(file_list) == 1:
                # Unique file
                file_path, source = file_list[0]
                best_files[file_hash] = file_path
            else:
                # Duplicate group - select best
                file_analyses = []
                for file_path, source in file_list:
                    analysis = self.analyze_file_content(file_path)
                    analysis['source'] = source
                    file_analyses.append(analysis)
                
                # Sort by quality score, then by size, then by modification time
                file_analyses.sort(key=lambda x: (x['quality_score'], x['size'], x['modified']), reverse=True)
                
                best_file = file_analyses[0]['file_path']
                best_files[file_hash] = best_file
                duplicate_groups[file_hash] = file_analyses
                
                self.merge_stats['duplicates_merged'] += len(file_list) - 1
                logger.info(f"Selected best from {len(file_list)} duplicates: {best_file.name}")
        
        self.merge_stats['unique_files_kept'] = len(best_files)
        logger.info(f"Selected {len(best_files)} unique files from {self.merge_stats['total_files_found']} total files")
        
        return best_files, duplicate_groups

    def create_final_structure(self):
        """Create the final organized directory structure."""
        logger.info("Creating final organized structure...")
        
        # Create main directories
        self.final_dir.mkdir(exist_ok=True)
        
        # Create category directories
        for category, description in self.categories.items():
            category_dir = self.final_dir / category
            category_dir.mkdir(exist_ok=True)
            
            # Create README for each category
            readme_path = category_dir / "README.md"
            with open(readme_path, 'w') as f:
                f.write(f"# {description}\n\n")
                f.write(f"This directory contains {description.lower()}.\n\n")
                f.write("## Files in this category:\n")
            
            self.merge_stats['categories_created'] += 1
        
        logger.info("Final structure created")

    def organize_files(self, best_files: Dict[str, Path]):
        """Organize files into the final structure."""
        logger.info("Organizing files into final structure...")
        
        for file_hash, file_path in best_files.items():
            try:
                # Analyze file
                analysis = self.analyze_file_content(file_path)
                category = analysis['category']
                
                # Determine target directory
                target_dir = self.final_dir / category
                
                # Create clean filename
                new_filename = self._create_clean_filename(file_path.name, analysis)
                target_path = target_dir / new_filename
                
                # Handle filename conflicts
                counter = 1
                original_target = target_path
                while target_path.exists():
                    stem = original_target.stem
                    suffix = original_target.suffix
                    target_path = target_dir / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                # Copy file
                shutil.copy2(str(file_path), str(target_path))
                self.processed_files.add(str(file_path))
                self.merge_stats['files_organized'] += 1
                
                logger.info(f"Organized {file_path.name} -> {category}/{target_path.name}")
                
            except Exception as e:
                logger.error(f"Error organizing {file_path}: {e}")

    def _create_clean_filename(self, filename: str, analysis: Dict) -> str:
        """Create a clean filename based on analysis."""
        # Remove common suffixes and clean up
        clean_name = filename
        
        # Remove common patterns
        patterns_to_remove = [
            r'\(\d+\)',  # (1), (2), etc.
            r'_\d+$',    # _1, _2, etc.
            r'\s+\d+$',  # space + number
            r'copy',     # copy
            r'backup',   # backup
            r'variants_', # variants_ prefix
        ]
        
        for pattern in patterns_to_remove:
            clean_name = re.sub(pattern, '', clean_name, flags=re.IGNORECASE)
        
        # Clean up extra spaces and underscores
        clean_name = re.sub(r'[_\s]+', '_', clean_name)
        clean_name = clean_name.strip('_')
        
        return clean_name

    def generate_merge_report(self, duplicate_groups: Dict[str, List[Dict]]):
        """Generate comprehensive merge report."""
        logger.info("Generating merge report...")
        
        report_path = self.final_dir / "MERGE_REPORT.md"
        with open(report_path, 'w') as f:
            f.write("# Comprehensive Merge and Consolidation Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Overview\n\n")
            f.write(f"- **Total files found:** {self.merge_stats['total_files_found']}\n")
            f.write(f"- **Unique files kept:** {self.merge_stats['unique_files_kept']}\n")
            f.write(f"- **Duplicates merged:** {self.merge_stats['duplicates_merged']}\n")
            f.write(f"- **Files organized:** {self.merge_stats['files_organized']}\n")
            f.write(f"- **Categories created:** {self.merge_stats['categories_created']}\n\n")
            
            f.write("## Sources Merged\n\n")
            for source_name, source_path in self.sources.items():
                f.write(f"- **{source_name}:** {source_path}\n")
            f.write("- **archive_extracted:** Extracted from Archive.zip\n\n")
            
            f.write("## Duplicate Groups Processed\n\n")
            for file_hash, file_list in duplicate_groups.items():
                f.write(f"### Group {file_hash[:8]}...\n")
                f.write(f"Files: {len(file_list)}\n")
                for i, file_analysis in enumerate(file_list):
                    status = "✓ KEPT" if i == 0 else "✗ MERGED"
                    f.write(f"- {status} {file_analysis['file_path']} (Quality: {file_analysis['quality_score']})\n")
                f.write(Path("\n"))
            
            f.write("## Final Directory Structure\n\n")
            f.write("```\n")
            f.write("FINAL_ORGANIZED/\n")
            for category in self.categories.keys():
                f.write(f"├── {category}/\n")
                f.write(f"│   ├── README.md\n")
                category_files = list((self.final_dir / category).glob("*"))
                category_files = [f for f in category_files if f.name != "README.md"]
                for i, file_path in enumerate(category_files[:5]):  # Show first 5 files
                    f.write(f"│   ├── {file_path.name}\n")
                if len(category_files) > 5:
                    f.write(f"│   └── ... ({len(category_files) - 5} more files)\n")
                else:
                    f.write(f"│   └── (empty)\n")
            f.write("```\n")
        
        # Generate JSON report
        json_report = self.final_dir / "MERGE_ANALYSIS.json"
        analysis_data = {
            'merge_stats': self.merge_stats,
            'sources': {k: str(v) for k, v in self.sources.items()},
            'duplicate_groups': {h: [{'path': str(f['file_path']), 'quality': f['quality_score']} for f in files] for h, files in duplicate_groups.items()},
            'categories': {cat: len(list((self.final_dir / cat).glob("*"))) - 1 for cat in self.categories.keys()},  # -1 for README.md
            'timestamp': datetime.now().isoformat()
        }
        
        with open(json_report, 'w') as f:
            json.dump(analysis_data, f, indent=2)
        
        logger.info(f"Merge report generated: {report_path}")

    def cleanup_temp_files(self):
        """Clean up temporary files."""
        logger.info("Cleaning up temporary files...")
        
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            logger.info("Temporary files cleaned up")

    def run_comprehensive_merge(self):
        """Run the complete merge and consolidation process."""
        logger.info("Starting comprehensive merge and consolidation process...")
        
        try:
            # Step 1: Extract archive
            self.extract_archive_zip()
            
            # Step 2: Collect all files
            all_files = self.collect_all_files()
            
            # Step 3: Find and merge duplicates
            best_files, duplicate_groups = self.find_and_merge_duplicates(all_files)
            
            # Step 4: Create final structure
            self.create_final_structure()
            
            # Step 5: Organize files
            self.organize_files(best_files)
            
            # Step 6: Generate reports
            self.generate_merge_report(duplicate_groups)
            
            # Step 7: Cleanup
            self.cleanup_temp_files()
            
            logger.info("Comprehensive merge and consolidation process completed!")
            
            # Print summary
            logger.info(f"\n✅ Comprehensive Merge Complete!")
            logger.info(f"📊 Total files found: {self.merge_stats['total_files_found']}")
            logger.info(f"🗂️  Unique files kept: {self.merge_stats['unique_files_kept']}")
            logger.info(f"🔄 Duplicates merged: {self.merge_stats['duplicates_merged']}")
            logger.info(f"📁 Files organized: {self.merge_stats['files_organized']}")
            logger.info(f"📂 Categories created: {self.merge_stats['categories_created']}")
            logger.info(f"📁 Final directory: {self.final_dir}")
            logger.info(f"📋 Merge report: {self.final_dir}/MERGE_REPORT.md")
            
        except Exception as e:
            logger.error(f"Error during merge process: {e}")
            raise

def main():
    """Main function."""
    base_dir = Path("/Users/steven/Music/nocTurneMeLoDieS/python")
    
    if not os.path.exists(base_dir):
        logger.error(f"Base directory not found: {base_dir}")
        return
    
    merger = ComprehensiveMerger(base_dir)
    merger.run_comprehensive_merge()

if __name__ == "__main__":
    main()