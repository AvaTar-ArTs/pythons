#!/usr/bin/env python3
"""
Duplicate Removal Analyzer
==========================
Basic filename-based duplicate detection using pattern matching.
Simple and fast for initial analysis.

Features:
- Pattern matching for common duplicate indicators
- Basic filename comparison
- Removal recommendations
"""

import os
import sys
import csv
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List


class DuplicateRemovalAnalyzer:
    def __init__(self, root_dir: str = None, max_files: int = None):
        self.root_dir = Path(root_dir) if root_dir else Path.home()
        self.max_files = max_files
        
    def find_python_files(self) -> List[Path]:
        """Find all Python files in the codebase."""
        python_files = []
        count = 0
        
        print(f"🔍 Scanning for Python files in {self.root_dir}...")
        
        for root, dirs, files in os.walk(self.root_dir):
            # Skip common directories
            dirs[:] = [d for d in dirs if d not in {
                '.git', '.venv', 'venv', '__pycache__', 'node_modules',
                '.pytest_cache', '.mypy_cache', 'dist', 'build', '.eggs'
            }]
            
            for file in files:
                if file.endswith('.py'):
                    filepath = Path(root) / file
                    try:
                        if filepath.is_file() and filepath.stat().st_size > 0:
                            python_files.append(filepath)
                            count += 1
                            if self.max_files and count >= self.max_files:
                                break
                    except (OSError, PermissionError):
                        continue
            
            if self.max_files and count >= self.max_files:
                break
        
        print(f"✅ Found {len(python_files)} Python files")
        return python_files
    
    def is_duplicate_pattern(self, filename1: str, filename2: str) -> bool:
        """Check if two filenames match duplicate patterns."""
        name1 = filename1.lower().replace('.py', '')
        name2 = filename2.lower().replace('.py', '')
        
        # Exact match
        if name1 == name2:
            return True
        
        # Copy patterns
        copy_patterns = [
            (r'(.+?)(?:\s*\(copy\)|\s*copy\s*\d*|\s*-\s*copy)$', r'\1'),
            (r'(.+?)(?:_copy\d*|_\d+)$', r'\1'),
        ]
        
        for pattern, replacement in copy_patterns:
            base1 = re.sub(pattern, replacement, name1)
            base2 = re.sub(pattern, replacement, name2)
            if base1 == base2 and base1:
                return True
        
        # Version patterns
        version_patterns = [
            (r'(.+?)(?:v\d+|_v\d+|version\s*\d+)$', r'\1'),
        ]
        
        for pattern, replacement in version_patterns:
            base1 = re.sub(pattern, replacement, name1)
            base2 = re.sub(pattern, replacement, name2)
            if base1 == base2 and base1:
                return True
        
        return False
    
    def find_duplicates(self) -> List[List[Path]]:
        """Find duplicate files using pattern matching."""
        print("\n📊 Analyzing filenames for duplicates...")
        python_files = self.find_python_files()
        
        duplicate_groups = []
        processed = set()
        
        for i, file1 in enumerate(python_files):
            if file1 in processed:
                continue
            
            group = [file1]
            
            for file2 in python_files[i+1:]:
                if file2 in processed:
                    continue
                
                if self.is_duplicate_pattern(file1.name, file2.name):
                    group.append(file2)
                    processed.add(file2)
            
            if len(group) > 1:
                duplicate_groups.append(group)
                processed.add(file1)
        
        print(f"✅ Found {len(duplicate_groups)} duplicate groups")
        return duplicate_groups
    
    def generate_removal_recommendations(self, duplicate_groups: List[List[Path]]) -> List[Dict]:
        """Generate recommendations for which files to remove."""
        recommendations = []
        
        for group in duplicate_groups:
            # Sort by path (prefer keeping files in standard locations)
            def sort_key(f: Path):
                path_str = str(f)
                score = 0
                # Penalize temp/backup directories
                if any(x in path_str.lower() for x in ['temp', 'backup', 'old', 'archive']):
                    score += 1000
                # Prefer shorter paths
                score += len(path_str)
                # Penalize files with copy indicators
                if any(re.search(p, f.stem, re.IGNORECASE) for p in [
                    r'copy', r'_\d+$', r'v\d+$'
                ]):
                    score += 100
                return score
            
            group_sorted = sorted(group, key=sort_key)
            keep_file = group_sorted[0]
            
            for remove_file in group_sorted[1:]:
                # Determine reason
                name1 = keep_file.stem.lower()
                name2 = remove_file.stem.lower()
                
                if name1 == name2:
                    reason = "Exact filename match"
                elif 'copy' in name2:
                    reason = "Copy indicator detected"
                elif re.search(r'_\d+$|v\d+$', name2):
                    reason = "Version/copy number detected"
                else:
                    reason = "Pattern match"
                
                # Get file size
                try:
                    file_size = remove_file.stat().st_size
                except:
                    file_size = 0
                
                recommendations.append({
                    'file_to_remove': str(remove_file),
                    'keep_file': str(keep_file),
                    'reason': reason,
                    'file_size': file_size
                })
        
        return recommendations
    
    def save_results(self, output_file: str = "files_to_remove.csv"):
        """Save analysis results to CSV."""
        duplicate_groups = self.find_duplicates()
        recommendations = self.generate_removal_recommendations(duplicate_groups)
        
        if not recommendations:
            print("\n✅ No duplicates found!")
            return
        
        print(f"\n📝 Saving {len(recommendations)} recommendations to {output_file}...")
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'file_to_remove', 'keep_file', 'reason', 'file_size'
            ])
            writer.writeheader()
            writer.writerows(recommendations)
        
        print(f"✅ Results saved to {output_file}")
        print(f"\n📊 Summary:")
        print(f"   - Total duplicate groups: {len(duplicate_groups)}")
        print(f"   - Files recommended for removal: {len(recommendations)}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Basic duplicate removal analyzer for Python codebase"
    )
    parser.add_argument(
        '--root', 
        type=str, 
        default=None,
        help='Root directory to analyze (default: home directory)'
    )
    parser.add_argument(
        '--max-files',
        type=int,
        default=None,
        help='Maximum number of files to analyze (default: all)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='files_to_remove.csv',
        help='Output CSV file (default: files_to_remove.csv)'
    )
    
    args = parser.parse_args()
    
    analyzer = DuplicateRemovalAnalyzer(
        root_dir=args.root,
        max_files=args.max_files
    )
    
    analyzer.save_results(output_file=args.output)


if __name__ == '__main__':
    main()
