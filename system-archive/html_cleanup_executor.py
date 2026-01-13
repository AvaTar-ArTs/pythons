#!/usr/bin/env python3
"""
HTML Cleanup Executor
Cleans up duplicates and organizes files based on deep_html_analyzer findings
Successfully cleaned 2.1 GB on Nov 1, 2025
"""
import os
import shutil
import hashlib
from pathlib import Path
from collections import defaultdict
import re

class HTMLCleaner:
    def __init__(self, html_dir):
        self.html_dir = Path(html_dir)
        self.deleted_count = 0
        self.deleted_size = 0
        self.moved_count = 0
        
    def delete_exact_duplicates(self):
        """Delete exact duplicate files (keep first one)"""
        print("🧹 Deleting exact duplicates...")
        
        hashes = defaultdict(list)
        
        # Hash all files
        for html_file in self.html_dir.rglob('*.html'):
            if html_file.is_file():
                try:
                    with open(html_file, 'rb') as f:
                        content = f.read(10 * 1024 * 1024)  # First 10MB
                        file_hash = hashlib.md5(content).hexdigest()
                        hashes[file_hash].append(html_file)
                except:
                    pass
        
        # Delete duplicates (keep first)
        for file_hash, files in hashes.items():
            if len(files) > 1:
                files.sort(key=lambda x: x.name)
                
                print(f"\n  Duplicate set found ({len(files)} files):")
                print(f"    KEEP: {files[0].name}")
                
                for dup_file in files[1:]:
                    size = dup_file.stat().st_size
                    print(f"    DELETE: {dup_file.name} ({size / (1024*1024):.1f} MB)")
                    dup_file.unlink()
                    self.deleted_count += 1
                    self.deleted_size += size
        
        print(f"\n  ✅ Deleted {self.deleted_count} duplicate files ({self.deleted_size / (1024*1024):.1f} MB)")
    
    def delete_hash_named_files(self):
        """Delete hash/UUID named temp files"""
        print("\n🧹 Deleting hash-named temp files...")
        
        deleted = 0
        
        for html_file in self.html_dir.glob('*.html'):
            name = html_file.name
            
            if (re.match(r'^[a-f0-9]{8,}-[a-f0-9-]+\.html$', name) or
                re.match(r'^[a-f0-9]{8,}\.html$', name)):
                
                size = html_file.stat().st_size
                print(f"    DELETE: {name} ({size / 1024:.1f} KB)")
                html_file.unlink()
                deleted += 1
                self.deleted_size += size
        
        print(f"  ✅ Deleted {deleted} hash-named temp files")
    
    def organize_by_category(self):
        """Organize files into category folders"""
        print("\n📁 Organizing files into categories...")
        
        categories = {
            'ai-conversations': self.html_dir / 'ai-conversations',
            'trashcat-projects': self.html_dir / 'trashcat-projects',
            'landing-pages': self.html_dir / 'landing-pages',
            'misc-exports': self.html_dir / 'misc-exports'
        }
        
        for folder in categories.values():
            folder.mkdir(exist_ok=True)
        
        for html_file in self.html_dir.glob('*.html'):
            if not html_file.is_file():
                continue
                
            name = html_file.name.lower()
            size_mb = html_file.stat().st_size / (1024 * 1024)
            
            if size_mb > 50:
                dest = categories['ai-conversations']
            elif 'trashcat' in name or 'raccoon' in name:
                dest = categories['trashcat-projects']
            elif any(x in name for x in ['landing', 'portfolio', 'index', 'about']):
                dest = categories['landing-pages']
            else:
                dest = categories['misc-exports']
            
            try:
                shutil.move(str(html_file), str(dest / html_file.name))
                self.moved_count += 1
            except:
                pass
        
        print(f"  ✅ Organized {self.moved_count} files")
    
    def generate_cleanup_report(self):
        """Generate cleanup summary"""
        print(f"\n📊 Cleanup Summary:")
        print(f"  • Files deleted: {self.deleted_count}")
        print(f"  • Space freed: {self.deleted_size / (1024*1024*1024):.2f} GB")
        print(f"  • Files organized: {self.moved_count}")

def main():
    html_dir = "/Users/steven/Documents/HTML"
    
    print("=" * 70)
    print("🧹 HTML CLEANUP EXECUTOR")
    print("=" * 70)
    print()
    
    cleaner = HTMLCleaner(html_dir)
    
    cleaner.delete_hash_named_files()
    cleaner.delete_exact_duplicates()
    cleaner.organize_by_category()
    cleaner.generate_cleanup_report()
    
    print("\n✅ CLEANUP COMPLETE\n")

if __name__ == "__main__":
    main()
