#!/usr/bin/env python3
"""
?? Compare & Cleanup Suno Folders
==================================

Compares and merges:
1. /Users/steven/Music/nocTurneMeLoDieS/SUNO
2. /Users/steven/Music/nocTurneMeLoDieS/FINAL_ORGANIZED/YOUR_SUNO_SONGS

Deduplicates, merges, and creates single clean folder.

Author: Steven Chaplinski
Date: November 4, 2025
"""

import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class SunoFolderCleaner:
    """Compare and cleanup Suno folders"""
    
    def __init__(self):
        self.music_dir = Path.home() / 'Music' / 'nocTurneMeLoDieS'
        
        self.folder1 = self.music_dir / 'SUNO'
        self.folder2 = self.music_dir / 'FINAL_ORGANIZED' / 'YOUR_SUNO_SONGS'
        
        # Target: keep everything in YOUR_SUNO_SONGS
        self.target = self.folder2
        
        self.audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg'}
        
        self.folder1_files = []
        self.folder2_files = []
        self.duplicates = []
        self.unique_to_folder1 = []
        
        self.stats = {
            'folder1_count': 0,
            'folder2_count': 0,
            'duplicates': 0,
            'moved': 0,
            'final_count': 0
        }
    
    def get_file_hash(self, filepath: Path) -> str:
        """Get file hash for comparison"""
        
        try:
            hash_md5 = hashlib.md5()
            with open(filepath, 'rb') as f:
                # Read first 1MB for speed
                chunk = f.read(1024 * 1024)
                hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return None
    
    def scan_folder(self, folder: Path, name: str):
        """Scan a folder"""
        
        print(f"?? Scanning: {name}")
        
        if not folder.exists():
            print(f"   ??  Folder not found\n")
            return []
        
        files = []
        
        for audio_file in folder.rglob('*'):
            if audio_file.suffix.lower() in self.audio_extensions and audio_file.is_file():
                try:
                    file_hash = self.get_file_hash(audio_file)
                    
                    files.append({
                        'path': audio_file,
                        'filename': audio_file.name,
                        'size_mb': round(audio_file.stat().st_size / (1024**2), 2),
                        'hash': file_hash
                    })
                except:
                    pass
        
        print(f"   ? Found {len(files)} files\n")
        return files
    
    def compare_folders(self):
        """Compare the two folders"""
        
        print("?? Comparing folders...\n")
        
        # Create hash maps
        folder2_hashes = {f['hash']: f for f in self.folder2_files if f['hash']}
        folder2_names = {f['filename'].lower(): f for f in self.folder2_files}
        
        for file1 in self.folder1_files:
            # Check if duplicate by hash
            if file1['hash'] and file1['hash'] in folder2_hashes:
                self.duplicates.append({
                    'file1': file1,
                    'file2': folder2_hashes[file1['hash']]
                })
                self.stats['duplicates'] += 1
            
            # Check if duplicate by name
            elif file1['filename'].lower() in folder2_names:
                self.duplicates.append({
                    'file1': file1,
                    'file2': folder2_names[file1['filename'].lower()]
                })
                self.stats['duplicates'] += 1
            
            else:
                # Unique to folder1
                self.unique_to_folder1.append(file1)
        
        print(f"   ? In both folders (duplicates): {len(self.duplicates)}")
        print(f"   ? Unique to SUNO folder: {len(self.unique_to_folder1)}\n")
    
    def merge_folders(self):
        """Merge SUNO into YOUR_SUNO_SONGS"""
        
        if not self.unique_to_folder1:
            print("   ??  No unique files to move\n")
            return
        
        print(f"?? Moving {len(self.unique_to_folder1)} unique files from SUNO folder...")
        print()
        
        for file_info in self.unique_to_folder1:
            try:
                source = file_info['path']
                target = self.target / source.name
                
                # Handle name conflicts
                if target.exists():
                    stem = source.stem
                    ext = source.suffix
                    counter = 1
                    while target.exists():
                        target = self.target / f"{stem}_{counter}{ext}"
                        counter += 1
                
                shutil.move(str(source), str(target))
                self.stats['moved'] += 1
                
                if self.stats['moved'] % 10 == 0:
                    print(f"   Moved {self.stats['moved']}/{len(self.unique_to_folder1)}...", end='\r')
            
            except Exception as e:
                print(f"   ? Error moving {source.name}: {e}")
        
        print(f"   ? Moved {self.stats['moved']} files" + " " * 20)
        print()
    
    def cleanup_empty_dirs(self):
        """Remove empty directories"""
        
        print("???  Cleaning up empty directories...")
        
        if self.folder1.exists():
            try:
                # Remove empty subdirectories
                for subdir in sorted(self.folder1.rglob('*'), reverse=True):
                    if subdir.is_dir() and not any(subdir.iterdir()):
                        subdir.rmdir()
                        print(f"   Removed: {subdir.relative_to(self.music_dir)}")
                
                # Remove main folder if empty
                if not any(self.folder1.iterdir()):
                    self.folder1.rmdir()
                    print(f"   Removed: {self.folder1.name}")
            except Exception as e:
                print(f"   ??  Could not remove all: {e}")
        
        print()
    
    def count_final(self):
        """Count final results"""
        
        print("?? Final count...")
        
        final_files = []
        for ext in self.audio_extensions:
            final_files.extend(self.target.glob(f'*{ext}'))
        
        self.stats['final_count'] = len(final_files)
        
        print(f"   ? YOUR_SUNO_SONGS now has {self.stats['final_count']} files\n")
    
    def generate_report(self):
        """Generate cleanup report"""
        
        report_file = Path.home() / 'workspace' / 'music-empire' / f'SUNO_FOLDERS_CLEANUP_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        
        with open(report_file, 'w') as f:
            f.write("?? SUNO FOLDERS CLEANUP REPORT\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"BEFORE:\n")
            f.write(f"  SUNO folder: {self.stats['folder1_count']} files\n")
            f.write(f"  YOUR_SUNO_SONGS: {self.stats['folder2_count']} files\n\n")
            
            f.write(f"CLEANUP:\n")
            f.write(f"  Duplicates found: {self.stats['duplicates']}\n")
            f.write(f"  Unique files moved: {self.stats['moved']}\n\n")
            
            f.write(f"AFTER:\n")
            f.write(f"  YOUR_SUNO_SONGS: {self.stats['final_count']} files\n\n")
            
            f.write("=" * 70 + "\n\n")
            
            if self.duplicates:
                f.write(f"DUPLICATES FOUND ({len(self.duplicates)}):\n\n")
                for dup in self.duplicates[:50]:
                    f.write(f"  ? {dup['file1']['filename']}\n")
                    f.write(f"    = {dup['file2']['filename']}\n\n")
                
                if len(self.duplicates) > 50:
                    f.write(f"... and {len(self.duplicates) - 50} more\n\n")
            
            if self.unique_to_folder1:
                f.write(f"\nMOVED FROM SUNO ({len(self.unique_to_folder1)}):\n\n")
                for file_info in self.unique_to_folder1:
                    f.write(f"  ? {file_info['filename']}\n")
        
        print(f"   ? Report: {report_file.name}\n")
    
    def run(self):
        """Run the cleanup"""
        
        print("?? SUNO FOLDERS CLEANUP")
        print("=" * 70)
        print()
        
        # Scan both folders
        self.folder1_files = self.scan_folder(self.folder1, "SUNO")
        self.folder2_files = self.scan_folder(self.folder2, "YOUR_SUNO_SONGS")
        
        self.stats['folder1_count'] = len(self.folder1_files)
        self.stats['folder2_count'] = len(self.folder2_files)
        
        # Compare
        self.compare_folders()
        
        # Merge
        self.merge_folders()
        
        # Cleanup
        self.cleanup_empty_dirs()
        
        # Count final
        self.count_final()
        
        # Report
        self.generate_report()
        
        # Summary
        print("=" * 70)
        print("?? CLEANUP COMPLETE!")
        print("=" * 70)
        
        print(f"\n?? Summary:")
        print(f"   Original SUNO: {self.stats['folder1_count']} files")
        print(f"   Original YOUR_SUNO_SONGS: {self.stats['folder2_count']} files")
        print(f"   Duplicates: {self.stats['duplicates']}")
        print(f"   Moved: {self.stats['moved']}")
        print(f"   Final total: {self.stats['final_count']} files")
        
        print(f"\n?? All YOUR Suno songs now in:")
        print(f"   {self.target}")
        
        print(f"\n?? Can create ~{self.stats['final_count'] // 24} albums!")


def main():
    cleaner = SunoFolderCleaner()
    cleaner.run()


if __name__ == '__main__':
    main()
