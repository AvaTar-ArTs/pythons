#!/usr/bin/env python3
"""
?? Cleanup Duplicates & Compare Against Catalog
================================================

1. Removes duplicate files
2. Fixes permission errors
3. Compares organized files vs 636-song catalog
4. Shows what you have vs what to download

Author: Steven Chaplinski
Date: November 4, 2025
"""

import csv
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import hashlib

class CleanupAndCompare:
    """Cleanup and compare collection"""
    
    def __init__(self):
        self.home = Path.home()
        self.workspace = self.home / 'workspace' / 'music-empire'
        self.organized_dir = self.home / 'Music' / 'nocTurneMeLoDieS' / 'FINAL_ORGANIZED'
        
        self.catalog = {}  # 636 songs from catalog
        self.organized_files = []  # Files in FINAL_ORGANIZED
        self.duplicates_removed = []
        self.permission_fixes = []
        
        self.matches = []  # Files matching catalog
        self.have = set()  # Song IDs we have
        self.need = []  # Songs to download
        
        self.stats = {
            'duplicates_removed': 0,
            'permissions_fixed': 0,
            'catalog_matched': 0,
            'need_to_download': 0
        }
    
    def load_catalog(self):
        """Load 636-song catalog"""
        
        print("?? Loading catalog...\n")
        
        # Find downloaded CSVs (check both locations)
        csv_files = []
        
        # Check extracted-csvs folder
        extracted_dir = self.workspace / 'extracted-csvs'
        if extracted_dir.exists():
            csv_files.extend(extracted_dir.glob('suno-saved-html-*.csv'))
        
        # Check Downloads
        downloads = Path.home() / 'Downloads'
        if downloads.exists():
            csv_files.extend(downloads.glob('suno-saved-html-*.csv'))
        
        csv_files = sorted(csv_files)
        
        if not csv_files:
            print("   ??  No catalog CSVs in Downloads")
            return False
        
        print(f"   Found {len(csv_files)} CSV files")
        
        for csvfile in csv_files:
            with open(csvfile, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    song_id = row.get('id', '').strip()
                    if song_id and song_id not in self.catalog:
                        self.catalog[song_id] = {
                            'id': song_id,
                            'title': row.get('title', ''),
                            'tags': row.get('tags', ''),
                            'audio_url': row.get('audio_url', ''),
                            'url': row.get('url', '')
                        }
        
        print(f"   ? Loaded {len(self.catalog)} unique songs\n")
        return True
    
    def scan_organized_folder(self):
        """Scan the FINAL_ORGANIZED folder"""
        
        print("?? Scanning organized folder...\n")
        
        if not self.organized_dir.exists():
            print("   ??  FINAL_ORGANIZED folder not found\n")
            return False
        
        audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg'}
        
        for audio_file in self.organized_dir.rglob('*'):
            if audio_file.suffix.lower() in audio_extensions and audio_file.is_file():
                try:
                    self.organized_files.append({
                        'path': audio_file,
                        'filename': audio_file.name,
                        'stem': audio_file.stem,
                        'size_mb': round(audio_file.stat().st_size / (1024**2), 2),
                        'category': audio_file.parent.name
                    })
                except:
                    pass
        
        print(f"   ? Found {len(self.organized_files)} files in FINAL_ORGANIZED\n")
        return True
    
    def remove_duplicates(self):
        """Find and remove duplicate files"""
        
        print("?? Finding duplicates...\n")
        
        by_hash = defaultdict(list)
        
        for file_info in self.organized_files:
            try:
                # Quick hash based on size + filename
                filepath = file_info['path']
                size = filepath.stat().st_size
                file_hash = hashlib.md5(f"{size}:{filepath.name}".encode()).hexdigest()
                
                by_hash[file_hash].append(file_info)
            except:
                pass
        
        # Find duplicates
        for file_hash, files in by_hash.items():
            if len(files) > 1:
                # Keep first, remove others
                for duplicate in files[1:]:
                    try:
                        duplicate['path'].unlink()
                        self.duplicates_removed.append(duplicate)
                        self.stats['duplicates_removed'] += 1
                    except:
                        pass
        
        print(f"   ? Removed {self.stats['duplicates_removed']} duplicate files\n")
    
    def fix_permissions(self):
        """Fix file permissions"""
        
        print("?? Fixing permissions...\n")
        
        for file_info in self.organized_files:
            try:
                filepath = file_info['path']
                
                if filepath.exists():
                    # Set readable permissions
                    filepath.chmod(0o644)
                    self.stats['permissions_fixed'] += 1
            except:
                pass
        
        print(f"   ? Fixed {self.stats['permissions_fixed']} file permissions\n")
    
    def compare_to_catalog(self):
        """Compare organized files to catalog"""
        
        print("?? Comparing to catalog...\n")
        
        # Check each organized file against catalog
        for file_info in self.organized_files:
            filename = file_info['filename']
            stem = file_info['stem'].lower()
            
            matched = False
            
            # Check if song ID in filename
            for song_id, song in self.catalog.items():
                if song_id in filename:
                    self.matches.append({
                        'file': file_info,
                        'song': song
                    })
                    self.have.add(song_id)
                    matched = True
                    break
            
            if not matched:
                # Try title matching
                stem_norm = stem.replace(' ', '').replace('-', '').replace('_', '')
                
                for song_id, song in self.catalog.items():
                    title = song.get('title', '').lower()
                    title_norm = title.replace(' ', '').replace('-', '').replace('_', '')
                    
                    if title_norm and len(title_norm) > 5:
                        if title_norm in stem_norm or stem_norm in title_norm:
                            self.matches.append({
                                'file': file_info,
                                'song': song
                            })
                            self.have.add(song_id)
                            break
        
        # Find songs we still need
        for song_id, song in self.catalog.items():
            if song_id not in self.have:
                self.need.append(song)
        
        self.stats['catalog_matched'] = len(self.have)
        self.stats['need_to_download'] = len(self.need)
        
        print(f"   ? Matched to catalog: {len(self.have)} songs")
        print(f"   ? Still need: {len(self.need)} songs\n")
    
    def generate_comparison_report(self):
        """Generate comparison report"""
        
        report_file = self.workspace / f'CLEANUP_COMPARISON_REPORT_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# ?? Cleanup & Comparison Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            # Cleanup summary
            f.write("## ?? Cleanup Results\n\n")
            f.write(f"- **Duplicates removed:** {self.stats['duplicates_removed']}\n")
            f.write(f"- **Permissions fixed:** {self.stats['permissions_fixed']}\n\n")
            
            # Comparison summary
            f.write("## ?? Catalog Comparison\n\n")
            f.write(f"- **Catalog total:** {len(self.catalog)} songs\n")
            f.write(f"- **You already have:** {len(self.have)} songs ({len(self.have)/len(self.catalog)*100:.1f}%)\n")
            f.write(f"- **Need to download:** {len(self.need)} songs ({len(self.need)/len(self.catalog)*100:.1f}%)\n\n")
            
            # What you have
            f.write("## ? Songs You Already Have\n\n")
            f.write(f"**Total:** {len(self.have)} of {len(self.catalog)}\n\n")
            
            for i, match in enumerate(self.matches[:50], 1):
                f.write(f"{i}. **{match['song']['title']}**\n")
                f.write(f"   - File: `{match['file']['filename']}`\n")
                f.write(f"   - Location: `{match['file']['category']}`\n\n")
            
            if len(self.matches) > 50:
                f.write(f"... and {len(self.matches) - 50} more\n\n")
            
            # What you need
            f.write("---\n\n")
            f.write("## ? Songs to Download\n\n")
            f.write(f"**Total:** {len(self.need)}\n\n")
            
            for i, song in enumerate(self.need[:50], 1):
                f.write(f"{i}. **{song['title']}**\n")
                if song.get('tags'):
                    tags = song['tags'][:60] + '...' if len(song.get('tags', '')) > 60 else song.get('tags', '')
                    f.write(f"   - Style: {tags}\n")
                f.write(f"   - Download: {song['audio_url']}\n\n")
            
            if len(self.need) > 50:
                f.write(f"... and {len(self.need) - 50} more\n\n")
            
            # Next steps
            f.write("---\n\n")
            f.write("## ?? Next Steps\n\n")
            f.write(f"1. ? **{len(self.have)} songs organized** - ready to use!\n")
            f.write(f"2. ? **Download {len(self.need)} more songs** (optional)\n")
            f.write(f"3. ?? **Create albums** from your {len(self.have)} songs\n")
            f.write(f"4. ?? **Upload to DistroKid** and start earning!\n\n")
        
        print(f"   ? Report: {report_file.name}\n")
        return report_file
    
    def export_download_list(self):
        """Export list of songs to download"""
        
        if not self.need:
            return None
        
        download_file = self.workspace / 'SONGS_STILL_NEEDED.csv'
        
        with open(download_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'title', 'tags', 'audio_url', 'url'])
            writer.writeheader()
            
            for song in self.need:
                writer.writerow({
                    'id': song['id'],
                    'title': song['title'],
                    'tags': song.get('tags', ''),
                    'audio_url': song.get('audio_url', ''),
                    'url': song.get('url', '')
                })
        
        print(f"   ? Download list: {download_file.name}\n")
        return download_file
    
    def print_summary(self):
        """Print summary"""
        
        print("=" * 70)
        print("?? CLEANUP & COMPARISON COMPLETE!")
        print("=" * 70)
        
        print(f"\n?? Cleanup:")
        print(f"   Duplicates removed: {self.stats['duplicates_removed']}")
        print(f"   Permissions fixed: {self.stats['permissions_fixed']}")
        
        print(f"\n?? Comparison vs Catalog ({len(self.catalog)} songs):")
        print(f"   ? You have: {len(self.have)} songs ({len(self.have)/len(self.catalog)*100:.1f}%)")
        print(f"   ? Need: {len(self.need)} songs ({len(self.need)/len(self.catalog)*100:.1f}%)")
        
        print(f"\n?? Your collection:")
        print(f"   Suno songs organized: {len(self.organized_files)}")
        print(f"   Matched to catalog: {len(self.have)}")
        
        if len(self.have) >= len(self.catalog) * 0.5:
            print(f"\n?? You have over 50% of your catalog!")
        
        print(f"\n?? Can create ~{len(self.have) // 24} albums from what you have now!")
    
    def run(self):
        """Run cleanup and comparison"""
        
        print("?? CLEANUP & COMPARISON")
        print("=" * 70)
        print()
        
        # Load data
        if not self.load_catalog():
            print("? Could not load catalog")
            return
        
        if not self.scan_organized_folder():
            print("? Could not scan organized folder")
            return
        
        # Cleanup
        self.remove_duplicates()
        self.fix_permissions()
        
        # Compare
        self.compare_to_catalog()
        
        # Reports
        report_file = self.generate_comparison_report()
        download_file = self.export_download_list()
        
        # Summary
        self.print_summary()
        
        print(f"\n{'=' * 70}")
        print("? ALL DONE!")
        print("=" * 70)
        
        print(f"\n?? Files created:")
        print(f"   ? {report_file.name}")
        if download_file:
            print(f"   ? {download_file.name}")
        
        print(f"\n?? Your organized music:")
        print(f"   {self.organized_dir}")


def main():
    cleaner = CleanupAndCompare()
    cleaner.run()


if __name__ == '__main__':
    main()
