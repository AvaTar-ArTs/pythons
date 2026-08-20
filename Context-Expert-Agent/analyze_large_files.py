#!/usr/bin/env python3
"""
Analyze large ZIP backup files and large HTML/MD files.
Compare contents, find duplicates, and recommend cleanup.
"""

import sys
import zipfile
import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime


def analyze_zip_file(zip_path):
    """Analyze a ZIP file."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            files = zf.namelist()
            total_size = sum(info.file_size for info in zf.infolist())
            total_compressed = sum(info.compress_size for info in zf.infolist())
            
            # Get date from filename if possible
            date_str = "unknown"
            name = zip_path.name
            if '2025' in name or '2024' in name:
                # Try to extract date
                import re
                date_match = re.search(r'(\d{4})(\d{2})(\d{2})', name)
                if date_match:
                    date_str = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
            
            return {
                'name': zip_path.name,
                'path': str(zip_path),
                'size': zip_path.stat().st_size,
                'file_count': len(files),
                'total_uncompressed': total_size,
                'total_compressed': total_compressed,
                'date': date_str,
                'files': files[:100]  # First 100 files for comparison
            }
    except Exception as e:
        return {'name': zip_path.name, 'error': str(e)}


def compare_zip_contents(zip1_info, zip2_info):
    """Compare contents of two ZIP files."""
    if 'error' in zip1_info or 'error' in zip2_info:
        return None
    
    files1 = set(zip1_info['files'])
    files2 = set(zip2_info['files'])
    
    common = files1 & files2
    only_in_1 = files1 - files2
    only_in_2 = files2 - files1
    
    similarity = len(common) / max(len(files1), len(files2)) if max(len(files1), len(files2)) > 0 else 0
    
    return {
        'similarity': similarity,
        'common_files': len(common),
        'only_in_1': len(only_in_1),
        'only_in_2': len(only_in_2),
        'total_files_1': len(files1),
        'total_files_2': len(files2)
    }


def analyze_large_html_md(root_path):
    """Find and analyze large HTML/MD files."""
    large_files = []
    
    for file_path in root_path.rglob('*'):
        if file_path.is_file():
            try:
                size = file_path.stat().st_size
                if size > 50 * 1024 * 1024:  # > 50MB
                    ext = file_path.suffix.lower()
                    if ext in ['.html', '.md', '.htm']:
                        large_files.append({
                            'path': file_path,
                            'rel_path': str(file_path.relative_to(root_path)),
                            'size': size,
                            'name': file_path.name
                        })
            except:
                pass
    
    return large_files


def compare_large_files(file1_path, file2_path):
    """Compare two large files for similarity."""
    try:
        # Quick comparison: first 1MB and size
        with open(file1_path, 'rb') as f1:
            chunk1 = f1.read(1024 * 1024)
        with open(file2_path, 'rb') as f2:
            chunk2 = f2.read(1024 * 1024)
        
        size1 = file1_path.stat().st_size
        size2 = file2_path.stat().st_size
        
        # Compare first chunk
        if chunk1 == chunk2 and size1 == size2:
            return {'identical': True, 'similarity': 1.0}
        elif chunk1 == chunk2:
            return {'identical_start': True, 'size_diff': abs(size1 - size2)}
        else:
            return {'different': True}
    except:
        return None


print("=" * 80)
print("LARGE FILES ANALYSIS")
print("=" * 80)

if len(sys.argv) < 2:
    print("Usage: python analyze_large_files.py <directory>")
    sys.exit(1)

root_path = Path(sys.argv[1])
if not root_path.exists():
    print(f"Error: Directory not found: {root_path}")
    sys.exit(1)

print(f"\n📂 Analyzing: {root_path}")

# Find ZIP files
print(f"\n📦 Finding ZIP backup files...")
zip_files = list(root_path.rglob('*.zip'))
zip_files = [f for f in zip_files if f.is_file() and f.stat().st_size > 100 * 1024 * 1024]  # > 100MB

print(f"   Found {len(zip_files)} large ZIP files")

# Analyze ZIP files
zip_infos = []
for zip_file in zip_files:
    info = analyze_zip_file(zip_file)
    zip_infos.append(info)
    if 'error' not in info:
        print(f"   - {info['name']}: {info['size']/1024/1024/1024:.2f} GB, {info['file_count']} files, date: {info['date']}")

# Compare ZIP files
print(f"\n🔍 Comparing ZIP files...")
zip_comparisons = []
for i, zip1 in enumerate(zip_infos):
    if 'error' in zip1:
        continue
    for zip2 in zip_infos[i+1:]:
        if 'error' in zip2:
            continue
        comparison = compare_zip_contents(zip1, zip2)
        if comparison and comparison['similarity'] > 0.5:
            zip_comparisons.append({
                'zip1': zip1['name'],
                'zip2': zip2['name'],
                'comparison': comparison
            })

if zip_comparisons:
    print(f"   Found {len(zip_comparisons)} pairs with >50% similarity")
    for comp in zip_comparisons[:10]:
        print(f"     {comp['zip1']} <-> {comp['zip2']}")
        print(f"       Similarity: {comp['comparison']['similarity']*100:.1f}%")
        print(f"       Common files: {comp['comparison']['common_files']}")

# Find large HTML/MD files
print(f"\n📄 Finding large HTML/MD files...")
large_html_md = analyze_large_html_md(root_path)

print(f"   Found {len(large_html_md)} large HTML/MD files (>50MB)")
for file_info in large_html_md:
    print(f"   - {file_info['rel_path']}: {file_info['size']/1024/1024:.2f} MB")

# Compare large HTML/MD files
print(f"\n🔍 Comparing large HTML/MD files...")
html_comparisons = []
for i, file1 in enumerate(large_html_md):
    for file2 in large_html_md[i+1:]:
        if file1['name'] == file2['name'] or 'ChatGPT' in file1['name']:
            comparison = compare_large_files(file1['path'], file2['path'])
            if comparison and comparison.get('identical'):
                html_comparisons.append({
                    'file1': file1['rel_path'],
                    'file2': file2['rel_path'],
                    'size': file1['size']
                })

if html_comparisons:
    print(f"   Found {len(html_comparisons)} pairs of identical large files")
    for comp in html_comparisons:
        print(f"     {comp['file1']} <-> {comp['file2']} ({comp['size']/1024/1024:.2f} MB each)")

# Summary and recommendations
print(f"\n" + "=" * 80)
print("SUMMARY & RECOMMENDATIONS")
print("=" * 80)

total_zip_size = sum(z['size'] for z in zip_infos if 'error' not in z)
total_html_size = sum(f['size'] for f in large_html_md)

print(f"\n📦 ZIP BACKUP FILES:")
print(f"   Total ZIP files: {len(zip_files)}")
print(f"   Total size: {total_zip_size/1024/1024/1024:.2f} GB")
print(f"   Recommendations:")
print(f"     - Review ZIP files - many appear to be backups of the same content")
print(f"     - Consider keeping only the most recent backup")
print(f"     - Archive old backups to external storage if needed")

print(f"\n📄 LARGE HTML/MD FILES:")
print(f"   Total large files: {len(large_html_md)}")
print(f"   Total size: {total_html_size/1024/1024/1024:.2f} GB")
if html_comparisons:
    potential_savings = sum(c['size'] for c in html_comparisons)
    print(f"   Identical duplicates found: {len(html_comparisons)}")
    print(f"   Potential space savings: {potential_savings/1024/1024/1024:.2f} GB")
    print(f"   Recommendations:")
    print(f"     - Remove duplicate large HTML/MD files")
    print(f"     - Keep only one copy (preferably in organized subdirectory)")

print(f"\n💾 TOTAL POTENTIAL SAVINGS:")
potential = total_zip_size * 0.5  # Assume 50% of ZIPs are redundant
if html_comparisons:
    potential += sum(c['size'] for c in html_comparisons)
print(f"   Estimated: {potential/1024/1024/1024:.2f} GB")

print("\n" + "=" * 80)
