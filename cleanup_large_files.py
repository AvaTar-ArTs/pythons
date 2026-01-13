#!/usr/bin/env python3
"""
Cleanup large ZIP backup files and duplicate large HTML/MD files.
"""

import sys
import zipfile
import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import re


def compare_zip_files_detailed(zip1_path, zip2_path):
    """Detailed comparison of two ZIP files."""
    try:
        with zipfile.ZipFile(zip1_path, 'r') as zf1:
            files1 = set(zf1.namelist())
            size1 = zip1_path.stat().st_size
        
        with zipfile.ZipFile(zip2_path, 'r') as zf2:
            files2 = set(zf2.namelist())
            size2 = zip2_path.stat().st_size
        
        common = files1 & files2
        only1 = files1 - files2
        only2 = files2 - files1
        
        similarity = len(common) / max(len(files1), len(files2)) if max(len(files1), len(files2)) > 0 else 0
        
        return {
            'similarity': similarity,
            'common_files': len(common),
            'only_in_1': len(only1),
            'only_in_2': len(only2),
            'size1': size1,
            'size2': size2,
            'size_diff': abs(size1 - size2)
        }
    except Exception as e:
        return {'error': str(e)}


def compare_large_files_hash(file1_path, file2_path):
    """Compare two files by hash."""
    def quick_hash(path):
        md5 = hashlib.md5()
        try:
            with open(path, 'rb') as f:
                # Hash first 10MB + size
                chunk = f.read(10 * 1024 * 1024)
                md5.update(chunk)
                md5.update(str(path.stat().st_size).encode())
            return md5.hexdigest()
        except:
            return None
    
    hash1 = quick_hash(file1_path)
    hash2 = quick_hash(file2_path)
    
    if hash1 and hash2:
        return hash1 == hash2
    return False


def cleanup_large_files(root_path, dry_run=True):
    """Clean up large ZIP and HTML/MD files."""
    print("=" * 80)
    print("LARGE FILES CLEANUP")
    print("=" * 80)
    print(f"\n📂 Directory: {root_path}")
    print(f"Mode: {'DRY RUN' if dry_run else 'EXECUTE'}")
    
    root_path = Path(root_path)
    
    # Find large ZIP files
    print(f"\n📦 Analyzing ZIP backup files...")
    zip_files = []
    for zip_file in root_path.rglob('*.zip'):
        if zip_file.is_file() and zip_file.stat().st_size > 100 * 1024 * 1024:  # > 100MB
            zip_files.append(zip_file)
    
    zip_files.sort(key=lambda f: f.stat().st_size, reverse=True)
    
    print(f"   Found {len(zip_files)} large ZIP files")
    for zip_file in zip_files:
        size_gb = zip_file.stat().st_size / 1024 / 1024 / 1024
        print(f"     - {zip_file.name}: {size_gb:.2f} GB")
    
    # Compare ZIP files to find duplicates/redundant backups
    print(f"\n🔍 Comparing ZIP files for duplicates...")
    zip_to_remove = []
    zip_groups = []
    
    # Group by date and similar names
    date_groups = defaultdict(list)
    for zip_file in zip_files:
        name = zip_file.name
        # Extract date
        date_match = re.search(r'(\d{4})(\d{2})(\d{2})', name)
        if date_match:
            date_key = date_match.group(0)
            date_groups[date_key].append(zip_file)
        else:
            date_groups['unknown'].append(zip_file)
    
    # For each date group, compare files
    for date_key, files in date_groups.items():
        if len(files) > 1:
            print(f"\n   Date group {date_key}: {len(files)} files")
            # Compare all pairs
            compared = set()
            for i, zip1 in enumerate(files):
                for zip2 in files[i+1:]:
                    pair_key = tuple(sorted([zip1.name, zip2.name]))
                    if pair_key in compared:
                        continue
                    compared.add(pair_key)
                    
                    comparison = compare_zip_files_detailed(zip1, zip2)
                    if comparison and 'error' not in comparison:
                        if comparison['similarity'] > 0.7:  # Lower threshold
                            # Similar - check if one is subset
                            print(f"     ⚠️  {zip1.name} <-> {zip2.name}")
                            print(f"        Similarity: {comparison['similarity']*100:.1f}%")
                            print(f"        Common files: {comparison['common_files']}")
                            print(f"        Only in {zip1.name}: {comparison['only_in_1']}")
                            print(f"        Only in {zip2.name}: {comparison['only_in_2']}")
                            
                            # If one has significantly more files, keep that one
                            if comparison['only_in_2'] == 0 and comparison['only_in_1'] > 0:
                                # zip2 is subset of zip1
                                zip_to_remove.append(zip2)
                                print(f"        → {zip2.name} is subset of {zip1.name}, removing {zip2.name}")
                            elif comparison['only_in_1'] == 0 and comparison['only_in_2'] > 0:
                                # zip1 is subset of zip2
                                zip_to_remove.append(zip1)
                                print(f"        → {zip1.name} is subset of {zip2.name}, removing {zip1.name}")
                            elif comparison['similarity'] > 0.95:
                                # Very similar - keep larger/newer one
                                if zip1.stat().st_size >= zip2.stat().st_size:
                                    zip_to_remove.append(zip2)
                                    print(f"        → Keep: {zip1.name}, Remove: {zip2.name}")
                                else:
                                    zip_to_remove.append(zip1)
                                    print(f"        → Keep: {zip2.name}, Remove: {zip1.name}")
    
    # Also check for ZIP files that might be redundant backups
    # If we have multiple backups from same date, keep the largest/most complete
    print(f"\n   Checking for redundant backups...")
    for date_key, files in date_groups.items():
        if date_key == '20251225' and len(files) > 1:
            # Multiple backups from same day - likely redundant
            files_sorted = sorted(files, key=lambda f: f.stat().st_size, reverse=True)
            print(f"     Found {len(files)} backups from {date_key}")
            print(f"     Keeping largest: {files_sorted[0].name} ({files_sorted[0].stat().st_size/1024/1024/1024:.2f} GB)")
            # Mark smaller ones for potential removal (but be conservative)
            for smaller_zip in files_sorted[1:]:
                size_diff = (files_sorted[0].stat().st_size - smaller_zip.stat().st_size) / files_sorted[0].stat().st_size
                if size_diff < 0.1:  # Less than 10% difference - likely same content
                    if smaller_zip not in zip_to_remove:
                        zip_to_remove.append(smaller_zip)
                        print(f"     → Marking for removal: {smaller_zip.name} (similar size, likely duplicate)")
    
    # Find large HTML/MD files
    print(f"\n📄 Finding large HTML/MD files...")
    large_files = []
    for file_path in root_path.rglob('*'):
        if file_path.is_file():
            try:
                size = file_path.stat().st_size
                if size > 50 * 1024 * 1024:  # > 50MB
                    ext = file_path.suffix.lower()
                    if ext in ['.html', '.md', '.htm']:
                        large_files.append(file_path)
            except:
                pass
    
    print(f"   Found {len(large_files)} large HTML/MD files")
    
    # Find duplicate large HTML/MD files
    print(f"\n🔍 Finding duplicate large HTML/MD files...")
    html_to_remove = []
    compared = set()
    
    for i, file1 in enumerate(large_files):
        for file2 in large_files[i+1:]:
            # Check if same name or ChatGPT files
            if file1.name == file2.name or ('ChatGPT' in file1.name and 'ChatGPT' in file2.name):
                pair_key = tuple(sorted([str(file1), str(file2)]))
                if pair_key in compared:
                    continue
                compared.add(pair_key)
                
                # Compare files
                if compare_large_files_hash(file1, file2):
                    # Prefer file in organized subdirectory
                    rel1 = str(file1.relative_to(root_path))
                    rel2 = str(file2.relative_to(root_path))
                    
                    # Prefer html/ or TrashCaTs/ subdirectories over root
                    if 'html/' in rel1 or 'TrashCaTs/' in rel1:
                        html_to_remove.append(file2)
                        print(f"     - Keep: {rel1}")
                        print(f"       Remove: {rel2}")
                    elif 'html/' in rel2 or 'TrashCaTs/' in rel2:
                        html_to_remove.append(file1)
                        print(f"     - Keep: {rel2}")
                        print(f"       Remove: {rel1}")
                    else:
                        # Keep the one in a subdirectory
                        if '/' in rel1 and '/' not in rel2:
                            html_to_remove.append(file2)
                            print(f"     - Keep: {rel1} (in subdirectory)")
                            print(f"       Remove: {rel2}")
                        elif '/' in rel2 and '/' not in rel1:
                            html_to_remove.append(file1)
                            print(f"     - Keep: {rel2} (in subdirectory)")
                            print(f"       Remove: {rel1}")
                        else:
                            # Keep first one
                            html_to_remove.append(file2)
                            print(f"     - Keep: {rel1}")
                            print(f"       Remove: {rel2}")
    
    # Summary
    print(f"\n" + "=" * 80)
    print("CLEANUP SUMMARY")
    print("=" * 80)
    
    total_zip_size = sum(f.stat().st_size for f in zip_to_remove)
    total_html_size = sum(f.stat().st_size for f in html_to_remove)
    
    print(f"\n📦 ZIP FILES TO REMOVE: {len(zip_to_remove)}")
    if zip_to_remove:
        for zip_file in zip_to_remove:
            size_gb = zip_file.stat().st_size / 1024 / 1024 / 1024
            print(f"     - {zip_file.name}: {size_gb:.2f} GB")
        print(f"   Total ZIP size to remove: {total_zip_size/1024/1024/1024:.2f} GB")
    else:
        print("   ✅ No redundant ZIP files found")
    
    print(f"\n📄 HTML/MD FILES TO REMOVE: {len(html_to_remove)}")
    if html_to_remove:
        for html_file in html_to_remove:
            size_mb = html_file.stat().st_size / 1024 / 1024
            rel_path = html_file.relative_to(root_path)
            print(f"     - {rel_path}: {size_mb:.2f} MB")
        print(f"   Total HTML/MD size to remove: {total_html_size/1024/1024/1024:.2f} GB")
    else:
        print("   ✅ No duplicate large HTML/MD files found")
    
    total_savings = total_zip_size + total_html_size
    print(f"\n💾 TOTAL POTENTIAL SAVINGS: {total_savings/1024/1024/1024:.2f} GB")
    
    # Execute removal
    if not dry_run:
        print(f"\n🗑️  Removing files...")
        
        removed_zips = 0
        removed_html = 0
        
        for zip_file in zip_to_remove:
            try:
                zip_file.unlink()
                removed_zips += 1
            except Exception as e:
                print(f"     ⚠️  Error removing {zip_file.name}: {e}")
        
        for html_file in html_to_remove:
            try:
                html_file.unlink()
                removed_html += 1
            except Exception as e:
                print(f"     ⚠️  Error removing {html_file.relative_to(root_path)}: {e}")
        
        print(f"\n✅ Removed {removed_zips} ZIP files and {removed_html} HTML/MD files")
    else:
        print(f"\n💡 Run with --execute to actually remove files")
    
    return {
        'zip_to_remove': zip_to_remove,
        'html_to_remove': html_to_remove,
        'total_savings': total_savings
    }


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python cleanup_large_files.py <directory> [--execute]")
        print("\nExample:")
        print("  python cleanup_large_files.py /path/to/dir          # Dry run")
        print("  python cleanup_large_files.py /path/to/dir --execute # Actually remove")
        sys.exit(1)
    
    root_path = sys.argv[1]
    dry_run = '--execute' not in sys.argv
    
    cleanup_large_files(root_path, dry_run)
