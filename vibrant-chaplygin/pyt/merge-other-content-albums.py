#!/usr/bin/env python3
"""
🔀 MERGE OTHER_CONTENT/ALBUMS INTO NOCTURNE
============================================
Move all albums from Other_Content/Albums into nocTurneMeLoDieS
with flat structure
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    END = "\033[0m"

class MergeOtherContentAlbums:
    """Merge Other_Content/Albums into nocturne"""
    
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        
        self.other_albums = Path.home() / "Music" / "Other_Content" / "Albums"
        self.nocturne_dir = Path.home() / "Music" / "nocTurneMeLoDieS"
        
        self.stats = {
            'albums_moved': 0,
            'files_moved': 0
        }
    
    def print_header(self, text: str, color=Colors.CYAN):
        print(f"\n{color}{Colors.BOLD}{'='*80}\n{text}\n{'='*80}{Colors.END}\n")
    
    def merge_album_folder(self, album_path: Path):
        """Merge one album folder into nocturne"""
        
        # Target in nocturne
        target_album = self.nocturne_dir / album_path.name
        target_album.mkdir(parents=True, exist_ok=True)
        
        # Get all files (recursively)
        all_files = [f for f in album_path.rglob('*') if f.is_file()]
        
        if not all_files:
            return 0
        
        print(f"{Colors.CYAN}{album_path.name}{Colors.END}")
        print(f"  Files: {len(all_files)}")
        
        moved = 0
        
        for file in all_files:
            target = target_album / file.name
            
            # Handle duplicates
            if target.exists():
                base = target.stem
                ext = target.suffix
                counter = 1
                while target.exists():
                    target = target_album / f"{base}_{counter}{ext}"
                    counter += 1
            
            if not self.dry_run:
                try:
                    shutil.copy2(file, target)
                    moved += 1
                except Exception as e:
                    print(f"  {Colors.RED}Error: {e}{Colors.END}")
            else:
                moved += 1
        
        print(f"  {Colors.GREEN}✅ Moved {moved} files{Colors.END}\n")
        
        return moved
    
    def merge_all_albums(self):
        """Merge all album folders"""
        self.print_header("🔀 MERGING OTHER_CONTENT/ALBUMS → NOCTURNE")
        
        if not self.other_albums.exists():
            print(f"{Colors.YELLOW}Other_Content/Albums not found{Colors.END}")
            return
        
        # Get all folders
        folders = [f for f in self.other_albums.iterdir() if f.is_dir()]
        
        # Skip empty/system folders
        skip = ['img', 'web', 'zip', 'scripts', 'Discography-HTML', 'enhancements', 
                'Needs_Review', 'suno-tools', 'transcripts', 'Txt']
        
        for folder in sorted(folders):
            if folder.name in skip:
                continue
            
            # Check if it has content
            file_count = sum(1 for _ in folder.rglob('*') if _.is_file())
            
            if file_count == 0:
                continue
            
            moved = self.merge_album_folder(folder)
            
            if moved > 0:
                self.stats['albums_moved'] += 1
                self.stats['files_moved'] += moved
                
                # Remove original folder
                if not self.dry_run:
                    try:
                        shutil.rmtree(folder)
                    except Exception:
                        pass
    
    def run(self):
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║        🔀 MERGE OTHER_CONTENT/ALBUMS → NOCTURNE 🔀                           ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        print(f"Mode: {Colors.YELLOW}{'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}\n")
        
        self.merge_all_albums()
        
        self.print_header("✅ MERGE COMPLETE!", Colors.GREEN)
        
        print(f"{Colors.BOLD}📊 Summary:{Colors.END}\n")
        print(f"  Albums merged: {Colors.CYAN}{self.stats['albums_moved']}{Colors.END}")
        print(f"  Files moved: {Colors.CYAN}{self.stats['files_moved']}{Colors.END}\n")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}⚠️  DRY RUN - Run with --live{Colors.END}\n")
        else:
            print(f"{Colors.GREEN}✅ All albums merged into nocturne!{Colors.END}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="🔀 Merge Other_Content/Albums")
    parser.add_argument('--dry-run', action='store_true', default=True)
    parser.add_argument('--live', action='store_true')
    
    args = parser.parse_args()
    
    merger = MergeOtherContentAlbums(dry_run=not args.live)
    merger.run()


if __name__ == "__main__":
    main()
