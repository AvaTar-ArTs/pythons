#!/usr/bin/env python3
"""
PDF File Path Analysis, Deduplication, and Management Tool

This script processes the pdfs.txt file to:
1. Parse the file paths
2. Identify duplicates
3. Provide analysis of the PDF collection
4. Generate cleaned/deduplicated versions
"""

import os
import re
from pathlib import Path
from collections import Counter, defaultdict
import hashlib
import json
from datetime import datetime


def parse_pdf_file_paths(file_path):
    """
    Parse the pdfs.txt file to extract individual file paths.
    The file contains space-separated paths, some with quotes.
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Handle both quoted and unquoted paths
    # This pattern matches quoted strings or sequences of non-whitespace characters
    pattern = r'"([^"]*)"|\'([^\']*)\'|(\S+)'
    matches = re.findall(pattern, content)
    
    # Extract the matched paths (the non-empty group from each match)
    paths = []
    for match in matches:
        path = next((m for m in match if m), None)
        if path:
            # Clean up the path (remove any remaining quotes or extra spaces)
            path = path.strip().strip('\'"')
            if path:  # Only add non-empty paths
                paths.append(path)
    
    return paths


def get_file_stats(file_path):
    """Get basic statistics about a file."""
    try:
        stat = os.stat(file_path)
        return {
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'exists': True
        }
    except:
        return {
            'size': 0,
            'modified': 'N/A',
            'exists': False
        }


def calculate_file_hash(file_path, chunk_size=8192):
    """Calculate MD5 hash of file content."""
    if not os.path.exists(file_path):
        return None
        
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return None


def analyze_pdf_paths(paths):
    """Analyze the collection of PDF paths."""
    analysis = {
        'total_paths': len(paths),
        'unique_paths': set(),
        'duplicates': [],
        'missing_files': [],
        'existing_files': [],
        'path_stats': defaultdict(int),  # Count by directory
        'extension_analysis': defaultdict(int),  # Count by extension
        'size_distribution': [],
        'hashes': {}  # path -> hash mapping
    }
    
    path_counts = Counter(paths)
    
    for path in paths:
        analysis['unique_paths'].add(path)
        
        # Count duplicates (paths that appear more than once)
        if path_counts[path] > 1:
            analysis['duplicates'].append(path)
    
    # Analyze directories and file stats
    for path in set(paths):
        path_obj = Path(path)
        
        # Count by directory
        parent_dir = str(path_obj.parent)
        analysis['path_stats'][parent_dir] += 1
        
        # Count by extension
        ext = path_obj.suffix.lower()
        analysis['extension_analysis'][ext] += 1
        
        # Check if file exists and get stats
        stats = get_file_stats(path)
        if stats['exists']:
            analysis['existing_files'].append({
                'path': path,
                'size': stats['size'],
                'modified': stats['modified']
            })
            
            # Calculate hash for existing files
            file_hash = calculate_file_hash(path)
            if file_hash:
                analysis['hashes'][path] = file_hash
        else:
            analysis['missing_files'].append(path)
    
    # Sort files by size for distribution analysis
    analysis['existing_files'].sort(key=lambda x: x['size'], reverse=True)
    
    return analysis


def find_content_duplicates(hashes):
    """Find files that have the same content (based on hash)."""
    hash_to_paths = defaultdict(list)
    
    for path, hash_value in hashes.items():
        hash_to_paths[hash_value].append(path)
    
    content_duplicates = {
        hash_val: paths 
        for hash_val, paths in hash_to_paths.items() 
        if len(paths) > 1
    }
    
    return content_duplicates


def generate_deduplicated_list(paths):
    """Generate a list with duplicates removed (keeping unique paths)."""
    return list(set(paths))


def generate_report(analysis):
    """Generate a comprehensive report of the analysis."""
    report = []
    report.append("PDF Collection Analysis Report")
    report.append("=" * 50)
    report.append(f"Analysis Date: {datetime.now().isoformat()}")
    report.append("")
    
    report.append("Basic Statistics:")
    report.append(f"  Total paths in file: {analysis['total_paths']}")
    report.append(f"  Unique paths: {len(analysis['unique_paths'])}")
    report.append(f"  Duplicate paths: {len(analysis['duplicates'])}")
    report.append(f"  Missing files: {len(analysis['missing_files'])}")
    report.append(f"  Existing files: {len(analysis['existing_files'])}")
    report.append("")
    
    if analysis['duplicates']:
        report.append("Duplicate Path Details:")
        path_counts = Counter(analysis['duplicates'])
        for path, count in list(path_counts.items())[:10]:  # Top 10 duplicates
            report.append(f"  {path[:60]}... ({count} times)")
        if len(path_counts) > 10:
            report.append(f"  ... and {len(path_counts) - 10} more duplicate paths")
        report.append("")
    
    top_dirs = sorted(analysis['path_stats'].items(), key=lambda x: x[1], reverse=True)[:10]
    report.append("Top 10 Directory Locations:")
    for directory, count in top_dirs:
        report.append(f"  {directory} ({count} files)")
    report.append("")
    
    ext_counts = sorted(analysis['extension_analysis'].items(), key=lambda x: x[1], reverse=True)
    report.append("File Extensions:")
    for ext, count in ext_counts:
        report.append(f"  {ext}: {count} files")
    report.append("")
    
    if analysis['existing_files']:
        report.append("File Size Statistics:")
        sizes = [f['size'] for f in analysis['existing_files']]
        if sizes:
            report.append(f"  Total size: {sum(sizes) / (1024*1024):.2f} MB")
            report.append(f"  Average size: {sum(sizes) / len(sizes) / 1024:.2f} KB")
            report.append(f"  Largest file: {max(sizes) / 1024:.2f} KB")
            report.append(f"  Smallest file: {min(sizes) / 1024:.2f} KB")
        report.append("")
    
    return "\n".join(report)


def save_results(analysis, output_dir):
    """Save analysis results to files."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Generate report
    report = generate_report(analysis)
    with open(output_path / "pdf_analysis_report.txt", 'w') as f:
        f.write(report)
    
    # Save unique paths
    unique_paths = generate_deduplicated_list(list(analysis['unique_paths']))
    with open(output_path / "unique_pdf_paths.txt", 'w') as f:
        f.write('\n'.join(sorted(unique_paths)) + '\n')
    
    # Save missing files
    with open(output_path / "missing_pdf_files.txt", 'w') as f:
        f.write('\n'.join(sorted(analysis['missing_files'])) + '\n')
    
    # Save content duplicates (if any)
    content_duplicates = find_content_duplicates(analysis['hashes'])
    if content_duplicates:
        with open(output_path / "content_duplicates.json", 'w') as f:
            json.dump(content_duplicates, f, indent=2)
    
    # Save full analysis as JSON
    analysis_copy = analysis.copy()
    analysis_copy['unique_paths'] = list(analysis_copy['unique_paths'])
    with open(output_path / "full_analysis.json", 'w') as f:
        json.dump(analysis_copy, f, indent=2, default=str)


def main():
    input_file = "/Users/steven/Documents/pdfs.txt"
    output_dir = "/Users/steven/pythons-sort/pdf_analysis_results"
    
    print(f"Analyzing PDF paths from: {input_file}")
    
    # Parse the file
    paths = parse_pdf_file_paths(input_file)
    print(f"Found {len(paths)} total paths")
    
    # Analyze the paths
    analysis = analyze_pdf_paths(paths)
    
    # Print summary
    print(f"Unique paths: {len(analysis['unique_paths'])}")
    print(f"Duplicates: {len(analysis['duplicates'])}")
    print(f"Missing files: {len(analysis['missing_files'])}")
    print(f"Existing files: {len(analysis['existing_files'])}")
    
    # Save results
    save_results(analysis, output_dir)
    print(f"Analysis results saved to: {output_dir}")
    
    # Summary
    print(f"\nDetailed analysis report generated at: {output_dir}/pdf_analysis_report.txt")
    print(f"Deduplicated paths saved to: {output_dir}/unique_pdf_paths.txt")
    print(f"Missing files listed at: {output_dir}/missing_pdf_files.txt")
    
    return analysis


if __name__ == "__main__":
    main()