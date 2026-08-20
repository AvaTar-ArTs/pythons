#!/usr/bin/env python3
"""
Organize Root & Merge Script
Categorizes unique root HTML files and merges them into the 'organized' folder.
"""

from pathlib import Path
import shutil
import hashlib
from datetime import datetime
from collections import defaultdict
import csv

# Config
ROOT_DIR = Path(".")
ORGANIZED_DIR = ROOT_DIR / "organized"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = ROOT_DIR / f"HTML_ROOT_MERGE_LOG_{TIMESTAMP}.csv"

# Categories (Same as before for consistency)
CATEGORIES = {
    'ai-prompts': ['prompt', 'leonardo', 'dalle', 'suno', 'openai', 'claude', 'midjourney', 'artbreeder'],
    'galleries': ['gallery', 'image', 'photo', 'picture', 'album', 'lightbox'],
    'exports': ['export', 'backup', 'download', 'archive', 'copy', 'chat'],
    'templates': ['template', 'basic', 'test'],
    'articles': ['article', 'blog', 'post', 'story', 'narrative'],
    'projects': ['project', 'app', 'dashboard', 'admin'],
    'other': [] 
}

def get_category(filename, content):
    filename_lower = filename.lower()
    content_lower = content.lower()
    
    for cat, keywords in CATEGORIES.items():
        if cat == 'other': continue
        
        # Check filename
        if any(k in filename_lower for k in keywords):
            return cat
        
        # Check content (lighter check)
        if len(content_lower) > 0:
            if any(k in content_lower[:500] for k in keywords):
                return cat
                
    return 'other'

print("="*80)
print(f"🚀 ORGANIZE ROOT & MERGE: {ROOT_DIR.resolve()}")
print("="*80)

# 1. Identify Target Files
print("\n1. identifying Root Files...")
root_files = []
ignored_dirs = {'.git', '.gemini', 'organized', 'misc', 'Portfolio', 'trashcat-projects', 'SBHTML'}
for p in ROOT_DIR.iterdir():
    if p.is_file() and p.suffix.lower() == '.html':
        root_files.append(p)

print(f"   Found {len(root_files):,} HTML files to organize.")

if not root_files:
    print("   No files to organize. Exiting.")
    exit()

# 2. Process Files
print("\n2. Processing & Categorizing...")
moved_count = 0
errors = 0

with open(LOG_FILE, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['original_path', 'new_path', 'category', 'status'])

    for i, f in enumerate(root_files, 1):
        try:
            # Read content for categorization
            try:
                content = f.read_text(errors='ignore')[:1000]
            except:
                content = ""
            
            category = get_category(f.name, content)
            target_dir = ORGANIZED_DIR / category
            target_dir.mkdir(parents=True, exist_ok=True)
            
            new_path = target_dir / f.name
            
            # Handle Name Collisions
            counter = 1
            while new_path.exists():
                # Check if it's actually the exact same file (hash check)
                # But we did a dup check before and found 0, so these are likely name collisions only.
                stem = f.stem
                suffix = f.suffix
                new_path = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1
            
            # Move File
            shutil.move(str(f), str(new_path))
            writer.writerow([str(f), str(new_path), category, 'moved'])
            moved_count += 1
            
        except Exception as e:
            print(f"   Error processing {f.name}: {e}")
            writer.writerow([str(f), '', 'error', str(e)])
            errors += 1

        if i % 100 == 0:
            print(f"   Processed {i}/{len(root_files)}...")

print("\n" + "="*80)
print("✅ MERGE COMPLETE")
print("="*80)
print(f"   Files Moved: {moved_count:,}")
print(f"   Errors: {errors}")
print(f"   Log File: {LOG_FILE.name}")
print(f"   Target: {ORGANIZED_DIR}")
