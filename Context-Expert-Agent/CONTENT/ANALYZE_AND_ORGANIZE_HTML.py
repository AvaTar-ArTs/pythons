#!/usr/bin/env python3
"""
Analyze and organize Documents/HTML/misc/ folder
Categorizes HTML files by content type and purpose
"""

from pathlib import Path
import shutil
import hashlib
from datetime import datetime
from collections import defaultdict
import re

html_dir = Path.home() / "Documents" / "HTML"
misc_dir = html_dir / "misc"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

print("=" * 100)
print("🔍 ANALYZING & ORGANIZING Documents/HTML/misc/")
print("=" * 100)
print()

# Get all HTML files in misc/
all_files = list(misc_dir.rglob("*.html"))
print(f"Found {len(all_files):,} HTML files in misc/")
print()

# Categorization
categories = {
    'ai-prompts': [],      # AI prompt exports (Prompt, Leonardo, Dalle, etc.)
    'galleries': [],       # Image galleries, photo pages
    'exports': [],         # Exports, backups, downloads
    'templates': [],       # Basic templates, simple HTML
    'articles': [],        # Articles, blog posts, content pages
    'projects': [],        # Project-specific HTML
    'other': []            # Everything else
}

content_hashes = {}
duplicates = defaultdict(list)

print("Analyzing files...")
for i, f in enumerate(all_files, 1):
    try:
        # Read file content and hash in one pass
        with open(f, 'rb') as file:
            file_bytes = file.read()
            file_hash = hashlib.md5(file_bytes).hexdigest()
        
        # Check for duplicates
        if file_hash in content_hashes:
            duplicates[file_hash].append(f)
        else:
            content_hashes[file_hash] = f
        
        # Read text content for analysis
        try:
            content = file_bytes[:5000].decode('utf-8', errors='ignore')
        except:
            content = ""
        
        filename_lower = f.name.lower()
        content_lower = content.lower()
        
        # Categorize based on filename and content
        categorized = False
        
        # AI Prompts (Prompt files, AI service names)
        if (any(keyword in filename_lower for keyword in ['prompt', 'leonardo', 'dalle', 'suno', 'openai', 'claude', 'midjourney', 'artbreeder']) or
            any(keyword in content_lower[:1000] for keyword in ['prompt', 'leonardo.ai', 'dalle', 'openai', 'claude'])):
            categories['ai-prompts'].append(f)
            categorized = True
        
        # Galleries (image galleries, photo pages)
        elif (any(keyword in filename_lower for keyword in ['gallery', 'image', 'photo', 'picture', 'album']) or
              any(keyword in content_lower[:1000] for keyword in ['gallery', 'image-gallery', 'photo-gallery', 'lightbox'])):
            categories['galleries'].append(f)
            categorized = True
        
        # Exports (exports, backups, downloads)
        elif (any(keyword in filename_lower for keyword in ['export', 'backup', 'download', 'archive', 'copy']) or
              any(keyword in content_lower[:500] for keyword in ['exported', 'backup', 'downloaded'])):
            categories['exports'].append(f)
            categorized = True
        
        # Templates (basic HTML, simple templates)
        elif (filename_lower in ['basic.html', 'template.html', 'index.html', 'test.html'] or
              len(content.strip()) < 500 or
              'hello world' in content_lower or
              '<!doctype html><html><title>' in content_lower[:200]):
            categories['templates'].append(f)
            categorized = True
        
        # Articles (articles, blog posts, content)
        elif (any(keyword in filename_lower for keyword in ['article', 'blog', 'post', 'story', 'narrative']) or
              any(keyword in content_lower[:500] for keyword in ['article', 'blog-post', 'published'])):
            categories['articles'].append(f)
            categorized = True
        
        # Projects (project-specific files)
        elif (any(keyword in filename_lower for keyword in ['project', 'app', 'dashboard', 'admin']) or
              any(keyword in content_lower[:500] for keyword in ['project', 'application', 'dashboard'])):
            categories['projects'].append(f)
            categorized = True
        
        # Default to other
        if not categorized:
            categories['other'].append(f)
    
    except Exception as e:
        categories['other'].append(f)
        print(f"   ⚠️  Error reading {f.name}: {e}")
    
    if i % 500 == 0:
        print(f"   Progress: {i:,}/{len(all_files):,}...")

print()
print("=" * 100)
print("📊 ANALYSIS RESULTS:")
print("=" * 100)
for cat, files in categories.items():
    print(f"   {cat:15s}: {len(files):,} files")
print()

dup_count = sum(len(files) - 1 for files in duplicates.values() if len(files) > 1)
print(f"   🗑️  Duplicate files: {dup_count:,}")
print()

# Create organized structure
print("📁 Creating organized structure...")
organized_dir = html_dir / "organized"
organized_dir.mkdir(exist_ok=True)

# Create category folders
for cat in categories.keys():
    (organized_dir / cat).mkdir(exist_ok=True)

# Create backup log
backup_log = html_dir / f"HTML_ORGANIZATION_LOG_{timestamp}.csv"
with open(backup_log, 'w') as log:
    log.write("original_path,new_path,category,size_bytes,is_duplicate\n")

print()
print("🔄 Organizing files...")
print("-" * 100)

moved_count = 0
duplicate_count = 0

# Move files to categories
for cat, files in categories.items():
    if not files:
        continue
    
    target_dir = organized_dir / cat
    print(f"\n📂 {cat}/ ({len(files):,} files)")
    
    for f in files:
        try:
            # Check if duplicate
            with open(f, 'rb') as file:
                file_hash = hashlib.md5(file.read()).hexdigest()
            is_dup = file_hash in duplicates and len(duplicates[file_hash]) > 1 and f != content_hashes[file_hash]
            
            if is_dup:
                # Move duplicates to _duplicates subfolder
                dup_dir = target_dir / "_duplicates"
                dup_dir.mkdir(exist_ok=True)
                new_path = dup_dir / f.name
                duplicate_count += 1
            else:
                new_path = target_dir / f.name
            
            # Handle name conflicts
            counter = 1
            original_new_path = new_path
            while new_path.exists():
                stem = original_new_path.stem
                suffix = original_new_path.suffix
                new_path = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1
            
            # Move file
            shutil.move(str(f), str(new_path))
            
            # Log
            size = f.stat().st_size if f.exists() else 0
            with open(backup_log, 'a') as log:
                log.write(f"{f},{new_path},{cat},{size},{is_dup}\n")
            
            moved_count += 1
            
        except Exception as e:
            print(f"   ⚠️  Error moving {f.name}: {e}")

print()
print("=" * 100)
print("✅ ORGANIZATION COMPLETE!")
print("=" * 100)
print(f"   Files moved: {moved_count:,}")
print(f"   Duplicates: {duplicate_count:,}")
print(f"   Backup log: {backup_log.name}")
print()
print(f"📁 Organized files are in: {organized_dir}")
print()
print("Next steps:")
print("   1. Review organized/ folder structure")
print("   2. If satisfied, you can delete misc/ folder")
print("   3. Or move organized/ contents back to misc/ with new structure")

