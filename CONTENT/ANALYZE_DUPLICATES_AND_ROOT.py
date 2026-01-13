#!/usr/bin/env python3
"""
Deep Dive Analysis & Duplicate Detector
Scans root and organized/ folders to find duplicates and unorganized files.
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict

ROOT_DIR = Path(".")
ORGANIZED_DIR = ROOT_DIR / "organized"

def calculate_hash(filepath):
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        return None

def get_file_info(filepath):
    stat = filepath.stat()
    return {
        'path': str(filepath),
        'name': filepath.name,
        'size': stat.st_size,
        'mtime': stat.st_mtime,
        'parent': filepath.parent.name
    }

print("="*80)
print(f"🔍 DEEP DIVE ANALYSIS: {ROOT_DIR.resolve()}")
print("="*80)

# 1. Scan Root Files (excluding directories and known subdirs)
print("\n1. Scanning Root Directory...")
root_files = []
ignored_dirs = {'.git', '.gemini', 'organized', 'misc', 'Portfolio', 'trashcat-projects', 'SBHTML'}
for p in ROOT_DIR.iterdir():
    if p.is_file() and p.suffix.lower() == '.html':
        root_files.append(p)

print(f"   Found {len(root_files):,} HTML files in root.")

# 2. Scan Organized Files
print("\n2. Scanning Organized Directory...")
organized_files = list(ORGANIZED_DIR.rglob("*.html"))
print(f"   Found {len(organized_files):,} HTML files in organized/.")

# 3. Hash & Compare
print("\n3. Analyzing Duplicates & Content...")
# Map hash -> list of files
hash_map = defaultdict(list)
all_scanned = root_files + organized_files
total = len(all_scanned)

for i, f in enumerate(all_scanned):
    h = calculate_hash(f)
    if h:
        hash_map[h].append(f)
    if i % 500 == 0:
        print(f"   Processed {i}/{total}...")

# Analyze Results
duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}
unique_files = len(hash_map)

root_dupes = 0      # Root files that exist in organized
root_unique = 0     # Root files that are NOT in organized
internal_dupes = 0  # Duplicates strictly within organized

print("\n" + "="*80)
print("📊 ANALYSIS REPORT")
print("="*80)

print(f"Total Unique Content (by hash): {unique_files:,}")
print(f"Total Duplicates Sets: {len(duplicates):,}")

print("\n--- Duplicate Breakdown ---")
for h, paths in duplicates.items():
    # Check if this set involves root and organized
    has_root = any(p in root_files for p in paths)
    has_organized = any(p in organized_files for p in paths)
    
    if has_root and has_organized:
        # Root file is already organized!
        root_dupes += sum(1 for p in paths if p in root_files)
    elif has_root and not has_organized:
        # Duplicates within root itself
        pass 
    elif not has_root and has_organized:
        # Duplicates inside organized
        internal_dupes += 1

print(f"1. Root files already present in 'organized': {root_dupes:,}")
print(f"   (Safe to delete these root files)")

print(f"2. Duplicates strictly within 'organized': {internal_dupes:,}")
print(f"   (These might need manual review)")

# Calculate root unique
root_hashes = {calculate_hash(f) for f in root_files}
organized_hashes = {calculate_hash(f) for f in organized_files}
unique_root_hashes = root_hashes - organized_hashes
print(f"3. Unique Root files (New content to organize): {len(unique_root_hashes):,}")

print("\n" + "="*80)
print("💡 RECOMMENDATIONS")
print("="*80)

if root_dupes > 0:
    print(f"[ACTION] Delete {root_dupes} duplicate files from root.")

if len(unique_root_hashes) > 0:
    print(f"[ACTION] Organize {len(unique_root_hashes)} unique root files into 'organized/'.")

if internal_dupes > 0:
    print(f"[ACTION] Deduplicate {internal_dupes} sets within 'organized/'.")

print("\nTo execute these actions, run the clean-up script (to be created).")
