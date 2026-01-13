#!/usr/bin/env python3
"""
Home Directory Deep Dive Analyzer
Comprehensive analysis of entire home directory ecosystem
"""
import os
import subprocess
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import csv

def get_dir_size(path):
    """Get directory size in bytes"""
    try:
        result = subprocess.run(['du', '-sk', path],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL,
                              text=True, timeout=60)
        if result.returncode == 0:
            return int(result.stdout.split()[0]) * 1024  # Convert KB to bytes
    except:
        pass
    return 0

def format_size(bytes_size):
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f}{unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f}PB"

def count_files_by_extension(directory, extensions):
    """Count files by extension in directory"""
    counts = defaultdict(int)
    try:
        for ext in extensions:
            result = subprocess.run(
                ['find', directory, '-name', f'*.{ext}', '-type', 'f'],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=120
            )
            if result.returncode == 0 and result.stdout.strip():
                counts[ext] = len(result.stdout.strip().split('\n'))
    except:
        pass
    return counts

def analyze_home_directory():
    """Perform comprehensive home directory analysis"""

    home = Path.home()

    print("=" * 80)
    print("HOME DIRECTORY DEEP DIVE ANALYSIS")
    print("=" * 80)
    print(f"Home: {home}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Define major directories to analyze
    major_dirs = [
        'AVATARARTS', 'GitHub', 'pythons', 'pythons-sort', 'scripts',
        'Documents', 'Downloads', 'Desktop',
        'Pictures', 'Music', 'Movies',
        'Library', 'claude-Convos', 'analysis',
        '.env.d', '.claude', '.config'
    ]

    # Extensions to track
    extensions = {
        'code': ['py', 'js', 'ts', 'jsx', 'tsx', 'sh', 'bash', 'zsh'],
        'data': ['csv', 'json', 'db', 'sqlite', 'sqlite3', 'xml'],
        'docs': ['md', 'txt', 'pdf', 'doc', 'docx'],
        'media': ['jpg', 'jpeg', 'png', 'gif', 'mp3', 'wav', 'mp4', 'mov'],
        'config': ['yml', 'yaml', 'toml', 'ini', 'conf', 'env']
    }

    results = []

    print("Analyzing directories...")
    print("-" * 80)

    for dir_name in major_dirs:
        dir_path = home / dir_name
        if not dir_path.exists():
            continue

        print(f"  Analyzing: {dir_name}...", end=' ')

        # Get size
        size_bytes = get_dir_size(str(dir_path))

        # Count files by category
        file_counts = {
            'code': 0,
            'data': 0,
            'docs': 0,
            'media': 0,
            'config': 0
        }

        for category, exts in extensions.items():
            counts = count_files_by_extension(str(dir_path), exts)
            file_counts[category] = sum(counts.values())

        # Get Python files specifically
        py_result = subprocess.run(
            ['find', str(dir_path), '-name', '*.py', '-type', 'f'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=120
        )
        py_count = len(py_result.stdout.strip().split('\n')) if py_result.stdout.strip() else 0

        results.append({
            'directory': dir_name,
            'path': str(dir_path),
            'size_bytes': size_bytes,
            'size_formatted': format_size(size_bytes),
            'python_files': py_count,
            **file_counts
        })

        print(f"✓ ({format_size(size_bytes)}, {py_count} .py)")

    # Sort by size
    results.sort(key=lambda x: x['size_bytes'], reverse=True)

    # Print summary table
    print("\n" + "=" * 80)
    print("SUMMARY BY SIZE")
    print("=" * 80)
    print(f"{'Directory':<20} {'Size':>10} {'Python':>8} {'Code':>8} {'Data':>8} {'Docs':>8} {'Media':>8}")
    print("-" * 80)

    for r in results:
        print(f"{r['directory']:<20} {r['size_formatted']:>10} {r['python_files']:>8,} "
              f"{r['code']:>8,} {r['data']:>8,} {r['docs']:>8,} {r['media']:>8,}")

    # Totals
    total_size = sum(r['size_bytes'] for r in results)
    total_py = sum(r['python_files'] for r in results)
    total_code = sum(r['code'] for r in results)
    total_data = sum(r['data'] for r in results)
    total_docs = sum(r['docs'] for r in results)
    total_media = sum(r['media'] for r in results)

    print("-" * 80)
    print(f"{'TOTAL':<20} {format_size(total_size):>10} {total_py:>8,} "
          f"{total_code:>8,} {total_data:>8,} {total_docs:>8,} {total_media:>8,}")
    print("=" * 80)

    # Top Python directories
    print("\n" + "=" * 80)
    print("TOP PYTHON FILE LOCATIONS")
    print("=" * 80)

    py_sorted = sorted(results, key=lambda x: x['python_files'], reverse=True)
    for r in py_sorted[:10]:
        if r['python_files'] > 0:
            print(f"  {r['directory']:<25} {r['python_files']:>8,} Python files")

    # Save detailed CSV
    output_file = home / 'AVATARARTS' / f'HOME_DIRECTORY_ANALYSIS_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

    with open(output_file, 'w', newline='') as f:
        fieldnames = ['directory', 'path', 'size_bytes', 'size_formatted',
                      'python_files', 'code', 'data', 'docs', 'media', 'config']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ Detailed CSV saved to: {output_file}")

    # Key findings
    print("\n" + "=" * 80)
    print("KEY FINDINGS")
    print("=" * 80)

    # Media vs code ratio
    media_dirs = ['Pictures', 'Music', 'Movies', 'Downloads']
    media_size = sum(r['size_bytes'] for r in results if r['directory'] in media_dirs)

    code_dirs = ['AVATARARTS', 'GitHub', 'pythons', 'pythons-sort']
    code_size = sum(r['size_bytes'] for r in results if r['directory'] in code_dirs)

    print(f"  Media Storage:     {format_size(media_size)} ({media_size/total_size*100:.1f}%)")
    print(f"  Code Storage:      {format_size(code_size)} ({code_size/total_size*100:.1f}%)")
    print(f"  Python Files:      {total_py:,} total")
    print(f"  Data Files (CSV):  {total_data:,} total")

    # Check for databases
    print("\n  Database Files:")
    for r in results:
        if r['data'] > 0:
            db_count = subprocess.run(
                ['find', r['path'], '-name', '*.db', '-o', '-name', '*.sqlite', '-type', 'f'],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True
            )
            if db_count.stdout.strip():
                db_files = len(db_count.stdout.strip().split('\n'))
                print(f"    {r['directory']}: {db_files} database files")

    print("\n" + "=" * 80)
    print(f"Analysis complete: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

if __name__ == '__main__':
    analyze_home_directory()
