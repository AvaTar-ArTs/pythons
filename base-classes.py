"""
Utilities File Operations Documents 1

This module provides functionality for utilities file operations documents 1.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_200 = 200
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024
CONSTANT_4096 = 4096
CONSTANT_5000 = 5000
CONSTANT_10000 = 10000
CONSTANT_50000 = 50000

#!/usr/bin/env python3
"""
Robust Documents Analyzer
Handles extremely long file paths and other edge cases.
"""

import os
import json
import hashlib
from pathlib import Path
from collections import defaultdict, Counter
import re
from datetime import datetime

class RobustDocumentsAnalyzer:
    def __init__(self, root_path):
        self.root_path = Path(root_path)
        self.analysis = {}
        self.duplicates = defaultdict(list)
        self.file_hashes = {}
        self.skipped_files = 0
        self.error_files = 0
        
    def safe_file_operation(self, file_path, operation):
        """Safely perform file operations with error handling"""
        try:
            return operation(file_path)
        except (OSError, UnicodeError, PermissionError) as e:
            self.error_files += 1
            if self.error_files % CONSTANT_1000 == 0:
                logger.info(f"Skipped {self.error_files} files due to errors...")
            return None
    
    def get_file_hash(self, filepath):
        """Get MD5 hash of file for duplicate detection"""
        def _hash_file(fp):
            hash_md5 = hashlib.md5()
            with open(fp, "rb") as f:
                for chunk in iter(lambda: f.read(CONSTANT_4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        
        return self.safe_file_operation(filepath, _hash_file)
    
    def analyze_file_types(self):
        """Analyze file types and their distribution"""
        file_types = Counter()
        total_size = 0
        file_count = 0
        
        logger.info("Analyzing file types...")
        
        for file_path in self.root_path.rglob('*'):
            if self.safe_file_operation(file_path, lambda x: x.is_file()):
                file_count += 1
                if file_count % CONSTANT_10000 == 0:
                    logger.info(f"Processed {file_count:,} files...")
                
                def _analyze_file(fp):
                    file_size = fp.stat().st_size
                    
                    # Get file extension
                    ext = fp.suffix.lower()
                    if not ext:
                        ext = 'no_extension'
                    
                    file_types[ext] += 1
                    return file_size
                
                result = self.safe_file_operation(file_path, _analyze_file)
                if result:
                    total_size += result
        
        return {
            'file_types': dict(file_types.most_common()),
            'total_files': file_count,
            'total_size': total_size,
            'total_size_gb': total_size / (CONSTANT_1024**3),
            'skipped_files': self.error_files
        }
    
    def find_duplicates_sample(self, sample_size=CONSTANT_50000):
        """Find duplicates using a sample of files to avoid memory issues"""
        logger.info(f"Scanning for duplicates (sample of {sample_size:,} files)...")
        
        file_count = 0
        duplicate_count = 0
        sample_files = []
        
        def _analyze_file(fp):
            nonlocal duplicate_count
            file_hash = self.get_file_hash(fp)
            if file_hash:
                file_info = {
                    'path': str(fp),
                    'size': fp.stat().st_size,
                    'modified': fp.stat().st_mtime,
                    'name': fp.name
                }
                
                if file_hash in self.file_hashes:
                    self.duplicates[file_hash].append(file_info)
                    duplicate_count += 1
                else:
                    self.file_hashes[file_hash] = file_info
            return True
        
        # First, collect a sample of files
        for file_path in self.root_path.rglob('*'):
            if self.safe_file_operation(file_path, lambda x: x.is_file()):
                sample_files.append(file_path)
                if len(sample_files) >= sample_size:
                    break
        
        logger.info(f"Analyzing {len(sample_files):,} files for duplicates...")
        
        for file_path in sample_files:
            file_count += 1
            if file_count % CONSTANT_5000 == 0:
                logger.info(f"Processed {file_count:,} files...")
            
            self.safe_file_operation(file_path, _analyze_file)
        
        logger.info(f"Found {len(self.duplicates)} duplicate groups affecting {duplicate_count} files")
        return self.duplicates
    
    def analyze_python_duplicates(self):
        """Specifically analyze Python file duplicates"""
        python_files = []
        
        logger.info("Collecting Python files...")
        
        for file_path in self.root_path.rglob('*.py'):
            if self.safe_file_operation(file_path, lambda x: x.is_file()):
                python_files.append(file_path)
                if len(python_files) % CONSTANT_1000 == 0:
                    logger.info(f"Found {len(python_files):,} Python files...")
        
        logger.info(f"Analyzing {len(python_files)} Python files...")
        
        # Group by base name patterns
        python_patterns = defaultdict(list)
        
        for py_file in python_files:
            name = py_file.name
            # Extract base name
            base_name = re.sub(r'_\d+(_\d+)*', '', name)
            base_name = re.sub(r'\(\d+\)', '', base_name)
            base_name = re.sub(r'\s+\d+$', '', base_name)
            base_name = re.sub(r'\.py$', '', base_name)
            
            def _analyze_python_file(fp):
                python_patterns[base_name].append({
                    'path': str(fp),
                    'name': name,
                    'size': fp.stat().st_size,
                    'modified': fp.stat().st_mtime
                })
            
            self.safe_file_operation(py_file, _analyze_python_file)
        
        # Find patterns with multiple files
        duplicate_patterns = {k: v for k, v in python_patterns.items() if len(v) > 1}
        
        # Sort by number of duplicates
        sorted_duplicates = sorted(duplicate_patterns.items(), key=lambda x: len(x[1]), reverse=True)
        
        return {
            'total_python_files': len(python_files),
            'duplicate_patterns': dict(sorted_duplicates[:CONSTANT_100]),  # Top CONSTANT_100 patterns
            'pattern_count': len(duplicate_patterns),
            'total_duplicate_files': sum(len(files) for files in duplicate_patterns.values())
        }
    
    def analyze_directory_structure(self):
        """Analyze directory structure and identify organization issues"""
        directories = []
        large_dirs = []
        logger.info("Analyzing directory structure...")
        
        for dir_path in self.root_path.rglob('*'):
            if self.safe_file_operation(dir_path, lambda x: x.is_dir()):
                def _analyze_directory(dp):
                    try:
                        file_count = len(list(dp.iterdir()))
                        dir_size = 0
                        
                        # Calculate size safely
                        for f in dp.rglob('*'):
                            if self.safe_file_operation(f, lambda x: x.is_file()):
                                size_result = self.safe_file_operation(f, lambda x: x.stat().st_size)
                                if size_result:
                                    dir_size += size_result
                        
                        dir_info = {
                            'path': str(dp),
                            'name': dp.name,
                            'file_count': file_count,
                            'size': dir_size,
                            'size_gb': dir_size / (CONSTANT_1024**3),
                            'depth': len(dp.parts) - len(self.root_path.parts)
                        }
                        
                        directories.append(dir_info)
                        
                        if file_count > CONSTANT_1000 or dir_size > CONSTANT_100 * CONSTANT_1024 * CONSTANT_1024:  # 100MB
                            large_dirs.append(dir_info)
                    except (OSError, IOError, FileNotFoundError):
                        pass
                
                self.safe_file_operation(dir_path, _analyze_directory)
        
        # Sort by size and file count
        large_dirs.sort(key=lambda x: x['size'], reverse=True)
        
        return {
            'total_directories': len(directories),
            'large_directories': large_dirs[:20],  # Top 20 largest
            'deepest_directory': max(directories, key=lambda x: x['depth']) if directories else None
        }
    
    def analyze_specific_problem_areas(self):
        """Analyze specific problem areas identified"""
        problem_areas = {
            'very_long_paths': 0,
            'nested_duplicates': 0,
            'versioned_files': 0,
            'temp_files': 0
        }
        
        logger.info("Analyzing specific problem areas...")
        
        for file_path in self.root_path.rglob('*'):
            if self.safe_file_operation(file_path, lambda x: x.is_file()):
                # Check for very long paths
                if len(str(file_path)) > CONSTANT_200:
                    problem_areas['very_long_paths'] += 1
                
                # Check for versioned files
                name = file_path.name
                if re.search(r'_\d+(_\d+)*', name) or re.search(r'\(\d+\)', name):
                    problem_areas['versioned_files'] += 1
                
                # Check for temp files
                if 'temp' in str(file_path).lower() or 'tmp' in str(file_path).lower():
                    problem_areas['temp_files'] += 1
        
        return problem_areas
    
    def generate_cleanup_recommendations(self):
        """Generate specific cleanup recommendations"""
        recommendations = []
        
        # Analyze Python duplicates
        python_analysis = self.analyze_python_duplicates()
        
        if python_analysis['pattern_count'] > 50:
            recommendations.append({
                'type': 'python_cleanup',
                'priority': 'high',
                'title': 'Clean Up Python File Duplicates',
                'description': f"Found {python_analysis['pattern_count']} Python file patterns with duplicates",
                'action': 'Review and consolidate similar Python files',
                'potential_savings': f"~{python_analysis['total_duplicate_files']} duplicate files"
            })
        
        # Analyze problem areas
        problem_areas = self.analyze_specific_problem_areas()
        
        if problem_areas['very_long_paths'] > CONSTANT_100:
            recommendations.append({
                'type': 'path_cleanup',
                'priority': 'high',
                'title': 'Fix Very Long File Paths',
                'description': f"Found {problem_areas['very_long_paths']} files with extremely long paths",
                'action': 'Rename or move files to shorter paths',
                'potential_savings': 'Improved system performance'
            })
        
        if problem_areas['versioned_files'] > CONSTANT_1000:
            recommendations.append({
                'type': 'version_cleanup',
                'priority': 'medium',
                'title': 'Consolidate Versioned Files',
                'description': f"Found {problem_areas['versioned_files']} files with version numbers",
                'action': 'Review and keep only the latest versions',
                'potential_savings': 'Reduced clutter and confusion'
            })
        
        return recommendations
    
    def run_complete_analysis(self):
        """Run complete analysis of Documents folder"""
        logger.info("Starting comprehensive Documents analysis...")
        
        # Analyze file types
        file_analysis = self.analyze_file_types()
        logger.info("✓ File type analysis complete")
        
        # Find duplicates (sample)
        duplicates = self.find_duplicates_sample()
        logger.info("✓ Duplicate analysis complete")
        
        # Analyze Python duplicates
        python_analysis = self.analyze_python_duplicates()
        logger.info("✓ Python duplicate analysis complete")
        
        # Analyze directory structure
        dir_analysis = self.analyze_directory_structure()
        logger.info("✓ Directory structure analysis complete")
        
        # Analyze problem areas
        problem_areas = self.analyze_specific_problem_areas()
        logger.info("✓ Problem areas analysis complete")
        
        # Generate recommendations
        recommendations = self.generate_cleanup_recommendations()
        logger.info("✓ Cleanup recommendations generated")
        
        # Compile complete analysis
        self.analysis = {
            'summary': {
                'total_files': file_analysis['total_files'],
                'total_size_gb': file_analysis['total_size_gb'],
                'total_directories': dir_analysis['total_directories'],
                'duplicate_groups': len(duplicates),
                'duplicate_files': sum(len(files) for files in duplicates.values()),
                'python_duplicate_patterns': python_analysis['pattern_count'],
                'skipped_files': file_analysis['skipped_files'],
                'analysis_date': datetime.now().isoformat()
            },
            'file_analysis': file_analysis,
            'duplicate_analysis': {
                'duplicates': dict(duplicates),
                'total_groups': len(duplicates),
                'total_files': sum(len(files) for files in duplicates.values())
            },
            'python_analysis': python_analysis,
            'directory_analysis': dir_analysis,
            'problem_areas': problem_areas,
            'recommendations': recommendations
        }
        
        return self.analysis
    
    def save_analysis(self):
        """Save analysis results to files"""
        # Save JSON analysis
        with open(self.root_path / 'documents_analysis_robust.json', 'w') as f:
            json.dump(self.analysis, f, indent=2)
        
        # Create human-readable report
        report = f"""# Documents Folder Deep Dive Analysis (Robust)

## Summary
- **Total Files:** {self.analysis['summary']['total_files']:,}
- **Total Size:** {self.analysis['summary']['total_size_gb']:.2f} GB
- **Total Directories:** {self.analysis['summary']['total_directories']:,}
- **Duplicate Groups:** {self.analysis['summary']['duplicate_groups']:,}
- **Duplicate Files:** {self.analysis['summary']['duplicate_files']:,}
- **Python Duplicate Patterns:** {self.analysis['summary']['python_duplicate_patterns']:,}
- **Skipped Files (Errors):** {self.analysis['summary']['skipped_files']:,}

## File Type Distribution
"""
        
        for ext, count in list(self.analysis['file_analysis']['file_types'].items())[:20]:
            report += f"- **{ext}:** {count:,} files\n"
        
        report += "\n## Top Python Duplicate Patterns\n"
        
        for pattern, files in list(self.analysis['python_analysis']['duplicate_patterns'].items())[:20]:
            report += f"- **{pattern}:** {len(files)} files\n"
        
        report += "\n## Large Directories\n"
        
        for dir_info in self.analysis['directory_analysis']['large_directories'][:10]:
            report += f"- **{dir_info['name']}:** {dir_info['file_count']:,} files, {dir_info['size_gb']:.2f} GB\n"
        
        report += "\n## Problem Areas\n"
        
        for area, count in self.analysis['problem_areas'].items():
            report += f"- **{area.replace('_', ' ').title()}:** {count:,} files\n"
        
        report += "\n## Cleanup Recommendations\n"
        
        for i, rec in enumerate(self.analysis['recommendations'], 1):
            report += f"### {i}. {rec['title']} ({rec['priority'].upper()} PRIORITY)\n"
            report += f"**Description:** {rec['description']}\n\n"
            report += f"**Action:** {rec['action']}\n\n"
            if 'potential_savings' in rec:
                report += f"**Potential Savings:** {rec['potential_savings']}\n\n"
        
        with open(self.root_path / 'documents_analysis_report_robust.md', 'w') as f:
            f.write(report)
        
        logger.info(f"Analysis saved to:")
        logger.info(f"- documents_analysis_robust.json")
        logger.info(f"- documents_analysis_report_robust.md")

def main():
    analyzer = RobustDocumentsAnalyzer(Path("/Users/steven/Documents"))
    analysis = analyzer.run_complete_analysis()
    analyzer.save_analysis()
    
    logger.info(f"\nAnalysis Complete!")
    logger.info(f"Found {analysis['summary']['total_files']:,} files in {analysis['summary']['total_directories']:,} directories")
    logger.info(f"Total size: {analysis['summary']['total_size_gb']:.2f} GB")
    logger.info(f"Duplicate groups: {analysis['summary']['duplicate_groups']:,}")
    logger.info(f"Python duplicate patterns: {analysis['summary']['python_duplicate_patterns']:,}")
    logger.info(f"Skipped files due to errors: {analysis['summary']['skipped_files']:,}")

if __name__ == "__main__":
    main()