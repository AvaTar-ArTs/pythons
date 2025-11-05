#!/usr/bin/env python3
"""
🔍 BATCH TRANSCRIPT FINDER
===========================
Search for transcripts/lyrics one folder at a time
Compile results into CSV
"""

import os
import csv
from pathlib import Path
from datetime import datetime

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"

class BatchTranscriptFinder:
    """Find transcripts in batches"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_file = Path.home() / "Documents" / f"TRANSCRIPT_INVENTORY_{self.timestamp}.csv"
        
        self.results = []
        self.stats = {'total_files': 0, 'total_size_mb': 0}
    
    def search_folder(self, folder_path: Path, max_depth: int = 5):
        """Search one folder for transcripts/lyrics"""
        
        if not folder_path.exists():
            print(f"{Colors.YELLOW}⚠️  {folder_path} doesn't exist{Colors.END}")
            return 0
        
        print(f"{Colors.CYAN}Searching: {folder_path}{Colors.END}")
        
        found = 0
        patterns = ['*transcript*', '*lyrics*', '*lyric*']
        
        for pattern in patterns:
            try:
                # Use rglob with try/except for each file
                for file in folder_path.rglob(pattern):
                    if file.is_file():
                        try:
                            size = file.stat().st_size
                            
                            self.results.append({
                                'path': str(file),
                                'name': file.name,
                                'parent': file.parent.name,
                                'size_kb': size / 1024,
                                'location': str(folder_path.name)
                            })
                            
                            found += 1
                            self.stats['total_files'] += 1
                            self.stats['total_size_mb'] += size / (1024**2)
                            
                        except Exception:
                            pass
                            
            except Exception as e:
                print(f"  {Colors.RED}Error with {pattern}: {e}{Colors.END}")
        
        print(f"  {Colors.GREEN}✅ Found {found} files{Colors.END}\n")
        return found
    
    def save_csv(self):
        """Save results to CSV"""
        
        with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Path', 'Filename', 'Parent_Folder', 'Size_KB', 'Location'])
            
            for item in sorted(self.results, key=lambda x: x['size_kb'], reverse=True):
                writer.writerow([
                    item['path'],
                    item['name'],
                    item['parent'],
                    f"{item['size_kb']:.2f}",
                    item['location']
                ])
        
        print(f"\n{Colors.GREEN}✅ CSV saved: {self.output_file}{Colors.END}")
        print(f"{Colors.GREEN}✅ Total files: {self.stats['total_files']}{Colors.END}")
        print(f"{Colors.GREEN}✅ Total size: {self.stats['total_size_mb']:.2f} MB{Colors.END}\n")
    
    def run(self):
        """Run batch search"""
        
        print(f"{Colors.BOLD}")
        print("="*80)
        print("🔍 BATCH TRANSCRIPT FINDER")
        print("="*80)
        print(f"{Colors.END}\n")
        
        # List of folders to search
        folders_to_search = [
            # Home directories
            Path.home() / "Music" / "nocTurneMeLoDieS",
            Path.home() / "Documents" / "MUSIC_ARCHIVE_PRESERVATION_20251104_175831",
            Path.home() / "Documents" / "PRESERVED_ARCHIVES",
            
            # Volumes
            Path("/Volumes/2T-Xx"),
            Path("/Volumes/DeVonDaTa"),
        ]
        
        for folder in folders_to_search:
            self.search_folder(folder)
        
        # Save CSV
        self.save_csv()


def main():
    finder = BatchTranscriptFinder()
    finder.run()


if __name__ == "__main__":
    main()
