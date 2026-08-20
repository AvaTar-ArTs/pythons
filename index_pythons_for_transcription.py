#!/usr/bin/env python3
"""
Index Python Files from pythons-files.txt for Transcription and Analysis
Scans the pythons-files.txt file for Python scripts and creates an index
of files that need transcription and analysis.
"""

import os
import csv
import re
import json
from pathlib import Path
from datetime import datetime

# Output directories for transcripts and analysis
OUTPUT_DIRS = {
    "transcripts": Path("/Users/steven/pythons/python_transcripts"),
    "analysis": Path("/Users/steven/pythons/python_analysis"),
}

# File containing the list of Python files
PYTHONS_FILES_TXT = Path("/Users/steven/pythons/pythons-files.txt")

def parse_pythons_files_txt(file_path):
    """Parse the pythons-files.txt file to extract all file paths."""
    print(f"Reading {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Better parsing: handle both quoted and unquoted paths
    # First, extract quoted paths (single or double quotes)
    quoted_paths = re.findall(r"['\"]([^'\"]+)['\"]", content)
    
    # Remove quoted paths from content to avoid double matching
    content_no_quotes = content
    for qp in quoted_paths:
        content_no_quotes = content_no_quotes.replace(f"'{qp}'", "").replace(f'"{qp}"', "")
    
    # Now extract unquoted paths (starting with /Users/steven/pythons)
    unquoted_paths = re.findall(r'(/Users/steven/pythons/[^\s]+)', content_no_quotes)
    
    # Combine all paths
    all_paths = quoted_paths + unquoted_paths
    
    # Filter for Python files
    python_files = []
    for path_str in all_paths:
        path = Path(path_str)
        # Check if it's a Python file
        if path.suffix in {'.py', '.pyw'}:
            # Only include files that exist
            if path.exists() and path.is_file():
                python_files.append(path)
    
    return python_files

def check_transcript_exists(python_path):
    """Check if transcript exists for Python file."""
    file_stem = python_path.stem
    # Use relative path from pythons dir to create unique name
    try:
        rel_path = python_path.relative_to(Path("/Users/steven/pythons"))
        # Replace / with _ for filename
        safe_name = str(rel_path).replace('/', '_').replace('\\', '_')
    except ValueError:
        # If not relative, use full path hash or name
        safe_name = f"{python_path.parent.name}_{file_stem}"
    
    transcript_path = OUTPUT_DIRS["transcripts"] / f"{safe_name}_transcript.txt"
    return transcript_path.exists(), transcript_path

def check_analysis_exists(python_path):
    """Check if analysis exists for Python file."""
    file_stem = python_path.stem
    try:
        rel_path = python_path.relative_to(Path("/Users/steven/pythons"))
        safe_name = str(rel_path).replace('/', '_').replace('\\', '_')
    except ValueError:
        safe_name = f"{python_path.parent.name}_{file_stem}"
    
    analysis_path = OUTPUT_DIRS["analysis"] / f"{safe_name}_analysis.txt"
    return analysis_path.exists(), analysis_path

def get_file_size_kb(file_path):
    """Get file size in KB."""
    try:
        return file_path.stat().st_size / 1024
    except:
        return 0

def count_lines(file_path):
    """Count lines in Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return len(f.readlines())
    except:
        return 0

def get_file_info(python_path):
    """Get comprehensive info about a Python file."""
    size_kb = get_file_size_kb(python_path)
    line_count = count_lines(python_path)
    
    has_transcript, transcript_path = check_transcript_exists(python_path)
    has_analysis, analysis_path = check_analysis_exists(python_path)
    
    # Determine status
    if has_transcript and has_analysis:
        status = "COMPLETE"
        needs_work = False
    elif has_transcript:
        status = "NEEDS_ANALYSIS"
        needs_work = True
    else:
        status = "NEEDS_TRANSCRIPTION"
        needs_work = True
    
    # Get relative path
    try:
        rel_path = str(python_path.relative_to(Path("/Users/steven/pythons")))
    except ValueError:
        rel_path = str(python_path)
    
    return {
        'filepath': str(python_path),
        'filename': python_path.name,
        'directory': str(python_path.parent),
        'relative_path': rel_path,
        'size_kb': round(size_kb, 2),
        'line_count': line_count,
        'has_transcript': has_transcript,
        'has_analysis': has_analysis,
        'transcript_path': str(transcript_path) if has_transcript else '',
        'analysis_path': str(analysis_path) if has_analysis else '',
        'status': status,
        'needs_work': needs_work,
    }

def main():
    print("=" * 80)
    print("INDEXING PYTHON FILES FOR TRANSCRIPTION AND ANALYSIS")
    print("=" * 80)
    print()
    
    if not PYTHONS_FILES_TXT.exists():
        print(f"Error: {PYTHONS_FILES_TXT} not found!")
        return
    
    # Parse Python files from the text file
    python_files = parse_pythons_files_txt(PYTHONS_FILES_TXT)
    
    print(f"Found {len(python_files)} Python files")
    print()
    
    if len(python_files) == 0:
        print("No Python files found in pythons-files.txt")
        return
    
    # Create output directories
    for dir_path in OUTPUT_DIRS.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Process each Python file
    print("Analyzing Python files...")
    indexed_files = []
    
    for i, python_path in enumerate(python_files, 1):
        if i % 100 == 0:
            print(f"  Processed {i}/{len(python_files)}...")
        
        file_info = get_file_info(python_path)
        indexed_files.append(file_info)
    
    print(f"Analysis complete!\n")
    
    # Create output directory
    output_dir = Path("/Users/steven/pythons/python_index")
    output_dir.mkdir(exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save CSV index
    csv_path = output_dir / f"python_index_{timestamp}.csv"
    
    fieldnames = [
        'filepath', 'filename', 'directory', 'relative_path',
        'size_kb', 'line_count', 'has_transcript', 'has_analysis',
        'transcript_path', 'analysis_path', 'status', 'needs_work'
    ]
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(indexed_files)
    
    print(f"CSV index saved: {csv_path}")
    
    # Save JSON index (for programmatic access)
    json_path = output_dir / f"python_index_{timestamp}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(indexed_files, f, indent=2)
    
    print(f"JSON index saved: {json_path}\n")
    
    # Generate summary
    total = len(indexed_files)
    complete = sum(1 for f in indexed_files if f['status'] == 'COMPLETE')
    needs_transcription = sum(1 for f in indexed_files if f['status'] == 'NEEDS_TRANSCRIPTION')
    needs_analysis = sum(1 for f in indexed_files if f['status'] == 'NEEDS_ANALYSIS')
    needs_work = sum(1 for f in indexed_files if f['needs_work'])
    
    total_size = sum(f['size_kb'] for f in indexed_files)
    total_lines = sum(f['line_count'] for f in indexed_files)
    needs_work_size = sum(f['size_kb'] for f in indexed_files if f['needs_work'])
    needs_work_lines = sum(f['line_count'] for f in indexed_files if f['needs_work'])
    
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Python files found: {total}")
    print(f"Total size: {total_size:.2f} KB ({total_size/1024:.2f} MB)")
    print(f"Total lines of code: {total_lines:,}")
    print()
    print(f"✅ Complete (transcript + analysis): {complete} ({complete/total*100:.1f}%)")
    print(f"📝 Needs transcription: {needs_transcription} ({needs_transcription/total*100:.1f}%)")
    print(f"🔍 Needs analysis: {needs_analysis} ({needs_analysis/total*100:.1f}%)")
    print()
    print(f"⚠️  Files needing work: {needs_work} ({needs_work/total*100:.1f}%)")
    print(f"   Total size needing work: {needs_work_size:.2f} KB ({needs_work_size/1024:.2f} MB)")
    print(f"   Total lines needing work: {needs_work_lines:,}")
    print()
    
    # Show examples of files needing work
    if needs_work > 0:
        print("=" * 80)
        print("FILES NEEDING WORK (first 10)")
        print("=" * 80)
        
        needs_work_files = [f for f in indexed_files if f['needs_work']]
        # Sort by size (largest first) or line count
        needs_work_files.sort(key=lambda x: x['line_count'], reverse=True)
        
        for i, file_info in enumerate(needs_work_files[:10], 1):
            print(f"{i}. {file_info['filename']}")
            print(f"   Path: {file_info['relative_path']}")
            print(f"   Size: {file_info['size_kb']:.2f} KB")
            print(f"   Lines: {file_info['line_count']:,}")
            print(f"   Status: {file_info['status']}")
            print()
        
        if len(needs_work_files) > 10:
            print(f"... and {len(needs_work_files) - 10} more files")
            print()
    
    # Create filtered CSV for files needing work
    if needs_work > 0:
        needs_work_csv = output_dir / f"pythons_needing_work_{timestamp}.csv"
        with open(needs_work_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows([f for f in indexed_files if f['needs_work']])
        
        print(f"Filtered CSV (needs work only): {needs_work_csv}")
        print()
    
    # Statistics by directory
    print("=" * 80)
    print("TOP DIRECTORIES (by file count)")
    print("=" * 80)
    
    dir_counts = {}
    for file_info in indexed_files:
        dir_path = file_info['directory']
        dir_counts[dir_path] = dir_counts.get(dir_path, 0) + 1
    
    top_dirs = sorted(dir_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for dir_path, count in top_dirs:
        rel_dir = dir_path.replace(str(Path("/Users/steven/pythons")), "").lstrip("/") or "root"
        print(f"  {rel_dir}: {count} files")
    print()
    
    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("1. Review the CSV index to see all Python files")
    print("2. Use pythons_needing_work CSV to process files")
    print("3. Create transcription/analysis scripts for Python files")
    print()
    print(f"Open CSV: open '{csv_path}'")

if __name__ == '__main__':
    main()
