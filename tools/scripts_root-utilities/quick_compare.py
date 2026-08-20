#!/usr/bin/env python3
import os
import zipfile
from pathlib import Path

# Paths
ZIP1 = Path("/Users/steven/Documents/Archives/gallery-projects/simplegallery_template.zip")
ZIP2 = Path("/Users/steven/Documents/Archives/gallery-projects/simplegallery-Perfect.zip")
DIR1 = Path("/Users/steven/simplegallery")
DIR2 = Path("/Users/steven/simples/simplegallery")

OUTPUT = Path("/Users/steven/Documents/Archives/duplicate_analysis/simplegallery_comparison.txt")

def get_zip_files(zip_path):
    """Get file list from zip"""
    if not zip_path.exists():
        return None, f"File not found: {zip_path}"
    try:
        files = set()
        with zipfile.ZipFile(zip_path, 'r') as z:
            for name in z.namelist():
                if not name.endswith('/'):
                    files.add(name)
        return files, None
    except Exception as e:
        return None, str(e)

def get_dir_files(dir_path):
    """Get file list from directory"""
    if not dir_path.exists():
        return None, f"Directory not found: {dir_path}"
    try:
        files = set()
        for root, dirs, filenames in os.walk(dir_path):
            for f in filenames:
                filepath = Path(root) / f
                rel = filepath.relative_to(dir_path)
                files.add(str(rel).replace('\\', '/'))
        return files, None
    except Exception as e:
        return None, str(e)

# Get all file sets
zip1_files, zip1_err = get_zip_files(ZIP1)
zip2_files, zip2_err = get_zip_files(ZIP2)
dir1_files, dir1_err = get_dir_files(DIR1)
dir2_files, dir2_err = get_dir_files(DIR2)

# Write report
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT, 'w') as f:
    f.write("=" * 70 + "\n")
    f.write("SIMPLEGALLERY COMPARISON REPORT\n")
    f.write("=" * 70 + "\n\n")
    
    f.write("FILES CHECKED:\n")
    f.write(f"  1. {ZIP1} - {'EXISTS' if ZIP1.exists() else 'NOT FOUND'}\n")
    if ZIP1.exists():
        f.write(f"     Size: {ZIP1.stat().st_size / (1024*1024):.2f} MB\n")
    f.write(f"  2. {ZIP2} - {'EXISTS' if ZIP2.exists() else 'NOT FOUND'}\n")
    if ZIP2.exists():
        f.write(f"     Size: {ZIP2.stat().st_size / (1024*1024):.2f} MB\n")
    f.write(f"  3. {DIR1} - {'EXISTS' if DIR1.exists() else 'NOT FOUND'}\n")
    f.write(f"  4. {DIR2} - {'EXISTS' if DIR2.exists() else 'NOT FOUND'}\n")
    f.write("\n")
    
    # Compare zip1 with dir2
    if zip1_files and dir2_files:
        common = zip1_files & dir2_files
        only_zip = zip1_files - dir2_files
        only_dir = dir2_files - zip1_files
        f.write(f"\n{'='*70}\n")
        f.write(f"COMPARISON: simplegallery_template.zip vs ~/simples/simplegallery\n")
        f.write(f"{'='*70}\n")
        f.write(f"Files in zip: {len(zip1_files)}\n")
        f.write(f"Files in dir: {len(dir2_files)}\n")
        f.write(f"Common files: {len(common)}\n")
        f.write(f"Only in zip: {len(only_zip)}\n")
        f.write(f"Only in dir: {len(only_dir)}\n")
        if only_zip:
            f.write(f"\nFiles ONLY in zip (first 20):\n")
            for x in sorted(list(only_zip))[:20]:
                f.write(f"  + {x}\n")
        if only_dir:
            f.write(f"\nFiles ONLY in directory (first 20):\n")
            for x in sorted(list(only_dir))[:20]:
                f.write(f"  + {x}\n")
    
    # Compare zip2 with dir2
    if zip2_files and dir2_files:
        common = zip2_files & dir2_files
        only_zip = zip2_files - dir2_files
        only_dir = dir2_files - zip2_files
        f.write(f"\n{'='*70}\n")
        f.write(f"COMPARISON: simplegallery-Perfect.zip vs ~/simples/simplegallery\n")
        f.write(f"{'='*70}\n")
        f.write(f"Files in zip: {len(zip2_files)}\n")
        f.write(f"Files in dir: {len(dir2_files)}\n")
        f.write(f"Common files: {len(common)}\n")
        f.write(f"Only in zip: {len(only_zip)}\n")
        f.write(f"Only in dir: {len(only_dir)}\n")
        if only_zip:
            f.write(f"\nFiles ONLY in zip (first 20):\n")
            for x in sorted(list(only_zip))[:20]:
                f.write(f"  + {x}\n")
        if only_dir:
            f.write(f"\nFiles ONLY in directory (first 20):\n")
            for x in sorted(list(only_dir))[:20]:
                f.write(f"  + {x}\n")
    
    # Compare zip1 vs zip2
    if zip1_files and zip2_files:
        common = zip1_files & zip2_files
        only_zip1 = zip1_files - zip2_files
        only_zip2 = zip2_files - zip1_files
        f.write(f"\n{'='*70}\n")
        f.write(f"COMPARISON: simplegallery_template.zip vs simplegallery-Perfect.zip\n")
        f.write(f"{'='*70}\n")
        f.write(f"Files in template.zip: {len(zip1_files)}\n")
        f.write(f"Files in Perfect.zip: {len(zip2_files)}\n")
        f.write(f"Common files: {len(common)}\n")
        f.write(f"Only in template.zip: {len(only_zip1)}\n")
        f.write(f"Only in Perfect.zip: {len(only_zip2)}\n")
        if only_zip1:
            f.write(f"\nFiles ONLY in template.zip (first 20):\n")
            for x in sorted(list(only_zip1))[:20]:
                f.write(f"  + {x}\n")
        if only_zip2:
            f.write(f"\nFiles ONLY in Perfect.zip (first 20):\n")
            for x in sorted(list(only_zip2))[:20]:
                f.write(f"  + {x}\n")
    
    # Errors
    if zip1_err:
        f.write(f"\nERROR with zip1: {zip1_err}\n")
    if zip2_err:
        f.write(f"\nERROR with zip2: {zip2_err}\n")
    if dir1_err:
        f.write(f"\nERROR with dir1: {dir1_err}\n")
    if dir2_err:
        f.write(f"\nERROR with dir2: {dir2_err}\n")

print(f"Report written to: {OUTPUT}")
