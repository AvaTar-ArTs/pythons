#!/usr/bin/env python3
"""
Enhanced duplicate finder: Direct scanning with MD5 hashing across directories.
Designed for comparative analysis of two directories (e.g., pythons/ vs Web-Archives/)

Usage:
    python3 tools/find_duplicates_enhanced.py \
      --source1 ~/pythons \
      --source2 ~/Documents/Web-Archives/QuantumForgeLabs/python \
      --format both \
      --output ~/Documents/duplicates_report
"""
import json
import csv
import os
import hashlib
import sys
from pathlib import Path
from collections import defaultdict
import argparse
from datetime import datetime


def md5_file(filepath, chunk_size=8192):
    """Calculate MD5 hash of a file."""
    md5_hash = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
    except (IOError, OSError) as e:
        return None


def scan_directory(directory, source_label=None, exclude_patterns=None):
    """Scan directory and return {md5: [files]} mapping."""
    if exclude_patterns is None:
        exclude_patterns = ['.git', '__pycache__', 'node_modules', '.env', '.DS_Store', 
                           '.venv', '.pytest_cache', '.mypy_cache', 'dist', 'build', 
                           '.egg-info', '.tox', 'venv', 'env']
    
    file_map = defaultdict(list)
    file_count = 0
    skipped = 0
    errors = 0
    
    directory = os.path.expanduser(directory)
    
    if not os.path.isdir(directory):
        print(f"❌ Directory not found: {directory}", file=sys.stderr)
        sys.exit(1)
    
    try:
        for root, dirs, files in os.walk(directory):
            # Filter out excluded directories in-place
            dirs[:] = [d for d in dirs if not any(excl in d for excl in exclude_patterns) and not d.startswith('.')]
            
            for filename in files:
                filepath = os.path.join(root, filename)
                
                # Skip hidden files and excluded patterns
                if filename.startswith('.') or any(pattern in filepath for pattern in exclude_patterns):
                    skipped += 1
                    continue
                
                try:
                    md5 = md5_file(filepath)
                    if md5:
                        file_map[md5].append({
                            'path': filepath,
                            'size': os.path.getsize(filepath),
                            'name': filename,
                            'mtime': os.path.getmtime(filepath),
                            'source': source_label or 'source1'
                        })
                        file_count += 1
                except Exception as e:
                    errors += 1
    except Exception as e:
        print(f"❌ Error scanning {directory}: {e}", file=sys.stderr)
        sys.exit(1)
    
    print(f"  ✓ {file_count} files scanned, {skipped} skipped, {errors} errors", file=sys.stderr)
    return file_map


def find_duplicates(file_map):
    """Find duplicate files from map."""
    duplicates = {}
    for md5, files in file_map.items():
        if len(files) > 1:
            duplicates[md5] = files
    return duplicates


def output_csv(duplicates, output_file):
    """Output duplicates as CSV."""
    filepath = os.path.expanduser(output_file) if not output_file.endswith('.csv') else os.path.expanduser(output_file)
    if not filepath.endswith('.csv'):
        filepath += '.csv'
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['MD5', 'Size (bytes)', 'File Path', 'Filename', 'Source', 'Mod Time', 
                        'Total Copies', 'Wasted Space (bytes)', 'Keep/Delete?'])
        
        for md5, files in sorted(duplicates.items()):
            total_copies = len(files)
            wasted = files[0]['size'] * (total_copies - 1)
            
            # Sort by modification time (newest first)
            sorted_files = sorted(files, key=lambda x: x['mtime'], reverse=True)
            
            for idx, file_info in enumerate(sorted_files):
                writer.writerow([
                    md5,
                    file_info['size'],
                    file_info['path'],
                    file_info['name'],
                    file_info.get('source', ''),
                    datetime.fromtimestamp(file_info['mtime']).isoformat(),
                    total_copies if idx == 0 else '',
                    wasted if idx == 0 else '',
                    'KEEP' if idx == 0 else 'DELETE'
                ])
    
    print(f"✅ CSV report written to {filepath}")
    return filepath


def output_json(duplicates, output_file):
    """Output duplicates as JSON."""
    filepath = os.path.expanduser(output_file) if not output_file.endswith('.json') else os.path.expanduser(output_file)
    if not filepath.endswith('.json'):
        filepath += '.json'
    
    json_output = {
        'scan_date': datetime.now().isoformat(),
        'total_duplicate_groups': len(duplicates),
        'total_duplicate_files': sum(len(files) - 1 for files in duplicates.values()),
        'total_wasted_space_bytes': sum(files[0]['size'] * (len(files) - 1) for files in duplicates.values()),
        'total_wasted_space_gb': round(sum(files[0]['size'] * (len(files) - 1) for files in duplicates.values()) / (1024**3), 2),
        'duplicates': {}
    }
    
    for md5, files in duplicates.items():
        sorted_files = sorted(files, key=lambda x: x['mtime'], reverse=True)
        json_output['duplicates'][md5] = {
            'count': len(files),
            'size_per_file_bytes': files[0]['size'],
            'total_wasted_bytes': files[0]['size'] * (len(files) - 1),
            'files': [
                {
                    'path': f['path'],
                    'source': f.get('source', ''),
                    'mtime': datetime.fromtimestamp(f['mtime']).isoformat(),
                    'recommendation': 'KEEP' if idx == 0 else 'DELETE'
                }
                for idx, f in enumerate(sorted_files)
            ]
        }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(json_output, f, indent=2)
    
    print(f"✅ JSON report written to {filepath}")
    return filepath


def print_summary(duplicates):
    """Print summary statistics."""
    total_dupes = sum(len(files) - 1 for files in duplicates.values())
    total_wasted = sum(files[0]['size'] * (len(files) - 1) for files in duplicates.values())
    
    print(f"\n📊 Duplicate Summary:", file=sys.stderr)
    print(f"  Duplicate groups: {len(duplicates)}", file=sys.stderr)
    print(f"  Total duplicate files: {total_dupes}", file=sys.stderr)
    print(f"  Wasted space: {total_wasted / (1024**3):.3f} GB ({total_wasted / (1024**2):.1f} MB)", file=sys.stderr)
    
    # Show top 10 largest wastes
    print(f"\n  Top 10 largest wastes:", file=sys.stderr)
    sorted_dupes = sorted(duplicates.items(), 
                         key=lambda x: x[1][0]['size'] * (len(x[1]) - 1), 
                         reverse=True)[:10]
    for idx, (md5, files) in enumerate(sorted_dupes, 1):
        waste = files[0]['size'] * (len(files) - 1)
        print(f"    {idx}. {files[0]['name']}: {waste / (1024**2):.1f} MB ({len(files)} copies)", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description='Find duplicate files across directories using MD5 hashing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compare two directories
  python3 find_duplicates_enhanced.py \\
    --source1 ~/pythons \\
    --source2 ~/Documents/Web-Archives/QuantumForgeLabs/python \\
    --format both \\
    --output ~/Documents/pythons_dedup_report

  # Single directory
  python3 find_duplicates_enhanced.py \\
    --source1 ~/GitHub \\
    --output ~/Documents/github_dupes
        """
    )
    parser.add_argument('--source1', required=True, help='Primary directory to scan')
    parser.add_argument('--source2', help='Secondary directory to scan (optional)')
    parser.add_argument('--format', choices=['csv', 'json', 'both'], default='both', 
                       help='Output format (default: both)')
    parser.add_argument('--output', required=True, help='Output file path (extension added automatically)')
    
    args = parser.parse_args()
    
    print(f"🔍 Starting duplicate analysis...\n", file=sys.stderr)
    
    print(f"📁 Scanning source1: {args.source1}", file=sys.stderr)
    file_map = scan_directory(args.source1, source_label='source1')
    
    if args.source2:
        print(f"📁 Scanning source2: {args.source2}", file=sys.stderr)
        file_map2 = scan_directory(args.source2, source_label='source2')
        # Merge maps
        for md5, files in file_map2.items():
            file_map[md5].extend(files)
    
    duplicates = find_duplicates(file_map)
    
    if not duplicates:
        print("\n✅ No duplicates found!", file=sys.stderr)
        return
    
    print_summary(duplicates)
    
    output_dir = os.path.dirname(os.path.expanduser(args.output))
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if args.format in ('csv', 'both'):
        output_csv(duplicates, args.output)
    if args.format in ('json', 'both'):
        output_json(duplicates, args.output)
    
    print("\n✨ Analysis complete!", file=sys.stderr)


if __name__ == "__main__":
    main()
