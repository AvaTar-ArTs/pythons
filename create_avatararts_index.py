#!/usr/bin/env python3
"""
AVATARARTS Ecosystem Indexer
Creates comprehensive indexes and CSV files for organizing the AVATARARTS ecosystem
"""

import os
import csv
import json
from pathlib import Path
from datetime import datetime
import pandas as pd
from typing import List, Dict, Any
import hashlib

def get_file_hash(filepath: str) -> str:
    """Generate a hash for file deduplication"""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def analyze_avatararts_ecosystem():
    """Analyze the AVATARARTS ecosystem and create comprehensive indexes"""
    
    base_path = Path("/Users/steven/AVATARARTS")
    if not base_path.exists():
        print("AVATARARTS directory not found at /Users/steven/AVATARARTS")
        return
    
    print("Analyzing AVATARARTS ecosystem...")
    
    # Collect all files with metadata
    files_data = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            filepath = Path(root) / file
            try:
                stat = filepath.stat()
                file_ext = filepath.suffix.lower()
                
                # Determine file type based on content and extension
                file_type = classify_file_type(filepath, file_ext)
                
                # Get file hash for deduplication
                file_hash = get_file_hash(str(filepath)) if stat.st_size < 10*1024*1024 else "large_file"  # Skip very large files
                
                files_data.append({
                    'path': str(filepath),
                    'relative_path': str(filepath.relative_to(base_path)),
                    'filename': file,
                    'extension': file_ext,
                    'size_bytes': stat.st_size,
                    'size_mb': round(stat.st_size / (1024*1024), 2),
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'file_type': file_type,
                    'directory': str(filepath.parent.relative_to(base_path)),
                    'hash': file_hash,
                    'function_classification': classify_function(filepath)
                })
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
    
    print(f"Collected data for {len(files_data)} files")
    
    # Create main index CSV
    create_main_index(files_data)
    
    # Create function-based classification CSV
    create_function_index(files_data)
    
    # Create duplicate detection CSV
    create_duplicates_index(files_data)
    
    # Create directory structure analysis
    create_directory_analysis(files_data)
    
    print("Indexing complete!")

def classify_file_type(filepath: Path, ext: str) -> str:
    """Classify file type based on extension and content"""
    ext_classifications = {
        '.py': 'Python Script',
        '.sh': 'Shell Script',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.json': 'JSON Data',
        '.csv': 'CSV Data',
        '.md': 'Markdown Documentation',
        '.html': 'HTML Document',
        '.css': 'CSS Stylesheet',
        '.sql': 'SQL Script',
        '.txt': 'Text File',
        '.log': 'Log File',
        '.yaml': 'YAML Configuration',
        '.yml': 'YAML Configuration',
        '.xml': 'XML Document',
        '.pdf': 'PDF Document',
        '.doc': 'Word Document',
        '.docx': 'Word Document',
        '.xls': 'Excel Spreadsheet',
        '.xlsx': 'Excel Spreadsheet',
        '.png': 'Image File',
        '.jpg': 'Image File',
        '.jpeg': 'Image File',
        '.gif': 'Image File',
        '.svg': 'Vector Image',
        '.mp3': 'Audio File',
        '.wav': 'Audio File',
        '.mp4': 'Video File',
        '.avi': 'Video File',
        '.zip': 'Archive File',
        '.tar': 'Archive File',
        '.gz': 'Archive File',
        '.db': 'Database File',
        '.sqlite': 'SQLite Database',
    }
    
    return ext_classifications.get(ext, 'Other')

def classify_function(filepath: Path) -> str:
    """Classify file function based on path and content"""
    path_str = str(filepath).lower()
    
    # Check for keywords in path that indicate function
    if 'revenue' in path_str or 'launch' in path_str:
        return 'Revenue Automation'
    elif 'dashboard' in path_str or 'analytics' in path_str or 'intelligence' in path_str:
        return 'Business Intelligence'
    elif 'api' in path_str or 'endpoint' in path_str:
        return 'API Integration'
    elif 'data' in path_str or 'csv' in path_str:
        return 'Data Processing'
    elif 'automation' in path_str or 'suite' in path_str:
        return 'Automation Suite'
    elif 'portfolio' in path_str:
        return 'Portfolio Management'
    elif 'documentation' in path_str or 'doc' in path_str:
        return 'Documentation'
    elif 'script' in path_str or 'tool' in path_str:
        return 'Utility Tool'
    elif 'config' in path_str or 'setting' in path_str:
        return 'Configuration'
    elif 'test' in path_str:
        return 'Testing'
    elif 'model' in path_str:
        return 'Machine Learning Model'
    elif 'ai' in path_str or 'ml' in path_str:
        return 'AI/ML Component'
    else:
        # Try to infer from file content if path doesn't indicate function
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(1000).lower()  # Read first 1000 chars
                
                if any(keyword in content for keyword in ['revenue', 'launch', 'profit', 'income']):
                    return 'Revenue Automation'
                elif any(keyword in content for keyword in ['dashboard', 'analytics', 'metric', 'report']):
                    return 'Business Intelligence'
                elif any(keyword in content for keyword in ['api', 'request', 'endpoint', 'client']):
                    return 'API Integration'
                elif any(keyword in content for keyword in ['data', 'pandas', 'csv', 'json', 'process']):
                    return 'Data Processing'
                elif any(keyword in content for keyword in ['automation', 'schedule', 'workflow']):
                    return 'Automation Suite'
                elif any(keyword in content for keyword in ['portfolio', 'investment', 'finance']):
                    return 'Portfolio Management'
                elif any(keyword in content for keyword in ['ai', 'ml', 'neural', 'model', 'predict']):
                    return 'AI/ML Component'
                else:
                    return 'General Purpose'
        except:
            return 'Unknown'

def create_main_index(files_data: List[Dict[str, Any]]):
    """Create the main index CSV file"""
    output_file = "/Users/steven/AVATARARTS_MAIN_INDEX.csv"
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'path', 'relative_path', 'filename', 'extension', 'size_bytes', 
            'size_mb', 'created', 'modified', 'file_type', 'directory', 
            'hash', 'function_classification'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for file_data in files_data:
            writer.writerow(file_data)
    
    print(f"Main index created: {output_file}")

def create_function_index(files_data: List[Dict[str, Any]]):
    """Create a function-based classification index"""
    output_file = "/Users/steven/AVATARARTS_FUNCTION_INDEX.csv"
    
    # Group by function classification
    function_groups = {}
    for file_data in files_data:
        func_class = file_data['function_classification']
        if func_class not in function_groups:
            function_groups[func_class] = []
        function_groups[func_class].append(file_data)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'function_classification', 'count', 'total_size_mb', 
            'avg_size_mb', 'file_extensions', 'sample_paths'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for func_class, files in function_groups.items():
            extensions = list(set([f['extension'] for f in files]))
            total_size = sum([f['size_mb'] for f in files])
            avg_size = total_size / len(files) if files else 0
            
            writer.writerow({
                'function_classification': func_class,
                'count': len(files),
                'total_size_mb': round(total_size, 2),
                'avg_size_mb': round(avg_size, 2),
                'file_extensions': ', '.join(extensions),
                'sample_paths': '; '.join([f['relative_path'] for f in files[:3]])  # First 3 paths
            })
    
    print(f"Function index created: {output_file}")

def create_duplicates_index(files_data: List[Dict[str, Any]]):
    """Create a duplicates detection index"""
    output_file = "/Users/steven/AVATARARTS_DUPLICATES_INDEX.csv"
    
    # Group by hash to find duplicates
    hash_groups = {}
    for file_data in files_data:
        file_hash = file_data['hash']
        if file_hash not in hash_groups:
            hash_groups[file_hash] = []
        hash_groups[file_hash].append(file_data)
    
    duplicates = [group for group in hash_groups.values() if len(group) > 1]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'hash', 'duplicate_count', 'total_size_saved_mb', 
            'duplicate_paths'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for dup_group in duplicates:
            total_size = sum([f['size_mb'] for f in dup_group]) - dup_group[0]['size_mb']  # Subtract one since we keep one copy
            writer.writerow({
                'hash': dup_group[0]['hash'],
                'duplicate_count': len(dup_group),
                'total_size_saved_mb': round(total_size, 2),
                'duplicate_paths': '; '.join([f['relative_path'] for f in dup_group])
            })
    
    print(f"Duplicates index created: {output_file}")

def create_directory_analysis(files_data: List[Dict[str, Any]]):
    """Create directory structure analysis"""
    output_file = "/Users/steven/AVATARARTS_DIRECTORY_ANALYSIS.csv"
    
    # Group by directory
    dir_groups = {}
    for file_data in files_data:
        directory = file_data['directory']
        if directory not in dir_groups:
            dir_groups[directory] = []
        dir_groups[directory].append(file_data)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'directory', 'file_count', 'total_size_mb', 'avg_file_size_mb',
            'extensions', 'function_diversity', 'path_depth'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for directory, files in dir_groups.items():
            extensions = list(set([f['extension'] for f in files]))
            functions = list(set([f['function_classification'] for f in files]))
            total_size = sum([f['size_mb'] for f in files])
            avg_size = total_size / len(files) if files else 0
            path_depth = len(directory.split('/')) if directory else 0
            
            writer.writerow({
                'directory': directory,
                'file_count': len(files),
                'total_size_mb': round(total_size, 2),
                'avg_file_size_mb': round(avg_size, 2),
                'extensions': ', '.join(extensions),
                'function_diversity': len(functions),
                'path_depth': path_depth
            })
    
    print(f"Directory analysis created: {output_file}")

if __name__ == "__main__":
    analyze_avatararts_ecosystem()