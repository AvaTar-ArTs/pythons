#!/usr/bin/env python3
"""
🔄 UNDO COLLECTION FIX & MERGE INTO NOCTURNE
=============================================
1. Move all songs back from albums to Steven_Chaplinski_Collection
2. Distribute ALL songs from collection into nocTurneMeLoDieS structure
3. Remove Steven_Chaplinski_Collection folder completely
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

class UndoAndMergeCollection:
    """Undo collection fix and merge everything into nocturne"""
    
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.nocturne_dir = Path.home() / "Music" / "nocTurneMeLoDieS"
        self.collection_dir = self.nocturne_dir / "Steven_Chaplinski_Collection"
        
        self.stats = {
            'moved_back': 0,
            'distributed': 0,
            'total_files': 0
        }
    
    def print_header(self, text: str, color=Colors.CYAN):
        print(f"\n{color}{Colors.BOLD}{'='*80}\n{text}\n{'='*80}{Colors.END}\n")
    
    def step1_move_all_mp3s_to_collection(self):
        """Move all MP3s from albums back to collection first"""
        self.print_header("🔄 STEP 1: GATHERING ALL MP3s TO COLLECTION")
        
        collection_files = self.collection_dir / "files"
        collection_files.mkdir(parents=True, exist_ok=True)
        
        # Find all MP3s that were recently moved (they're in album/files/ folders)
        # We'll just move ALL MP3s from ALL albums to collection temporarily
        
        print(f"Scanning all albums for MP3s...\n")
        
        for album_folder in self.nocturne_dir.iterdir():
            if not album_folder.is_dir():
                continue
            
            if album_folder.name == "Steven_Chaplinski_Collection":
                continue
            
            # Skip analysis folders
            if any(skip in album_folder.name.upper() for skip in ['ANALYSIS', 'LOG', 'SCAN', 'BACKUP']):
                continue
            
            album_files = album_folder / "files"
            
            if not album_files.exists():
                continue
            
            mp3_files = list(album_files.glob("*.mp3"))
            
            if mp3_files:
                print(f"{Colors.CYAN}{album_folder.name}{Colors.END}: {len(mp3_files)} MP3s")
                
                for mp3 in mp3_files:
                    target = collection_files / mp3.name
                    
                    # Skip if already exists in collection
                    if target.exists():
                        continue
                    
                    if not self.dry_run:
                        shutil.move(str(mp3), str(target))
                        self.stats['moved_back'] += 1
                    else:
                        self.stats['moved_back'] += 1
        
        print(f"\n{Colors.BOLD}Total MP3s gathered to collection: {self.stats['moved_back']}{Colors.END}")
    
    def step2_distribute_all_to_nocturne(self):
        """Distribute all MP3s from collection into nocturne root"""
        self.print_header("📤 STEP 2: DISTRIBUTING ALL MP3s TO NOCTURNE ROOT")
        
        collection_files = self.collection_dir / "files"
        
        if not collection_files.exists():
            print(f"{Colors.YELLOW}No files to distribute{Colors.END}")
            return
        
        mp3_files = list(collection_files.glob("*.mp3"))
        
        print(f"Found {len(mp3_files)} MP3s to distribute\n")
        
        self.stats['total_files'] = len(mp3_files)
        
        # Move all MP3s directly to nocturne root
        for mp3 in mp3_files:
            target = self.nocturne_dir / mp3.name
            
            # Skip if file already exists
            if target.exists():
                print(f"{Colors.YELLOW}⚠️  Skip (exists):{Colors.END} {mp3.name}")
                continue
            
            if not self.dry_run:
                shutil.move(str(mp3), str(target))
                self.stats['distributed'] += 1
                
                if self.stats['distributed'] % 100 == 0:
                    print(f"{Colors.GREEN}✅ Moved {self.stats['distributed']} files...{Colors.END}")
            else:
                self.stats['distributed'] += 1
        
        print(f"\n{Colors.BOLD}Total files distributed: {self.stats['distributed']}{Colors.END}")
    
    def step3_remove_collection_folder(self):
        """Remove Steven_Chaplinski_Collection folder"""
        self.print_header("🗑️ STEP 3: REMOVING COLLECTION FOLDER")
        
        if not self.collection_dir.exists():
            print(f"{Colors.YELLOW}Collection folder already removed{Colors.END}")
            return
        
        print(f"Removing: {self.collection_dir.name}\n")
        
        if not self.dry_run:
            try:
                shutil.rmtree(self.collection_dir)
                print(f"{Colors.GREEN}✅ Removed Steven_Chaplinski_Collection folder{Colors.END}")
            except Exception as e:
                print(f"{Colors.RED}❌ Error: {e}{Colors.END}")
        else:
            print(f"{Colors.YELLOW}[DRY RUN] Would remove folder{Colors.END}")
    
    def run(self):
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║         🔄 UNDO COLLECTION & MERGE INTO NOCTURNE 🔄                           ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        print(f"Mode: {Colors.YELLOW}{'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}\n")
        
        # Step 1: Gather all MP3s
        self.step1_move_all_mp3s_to_collection()
        
        # Step 2: Distribute to nocturne
        self.step2_distribute_all_to_nocturne()
        
        # Step 3: Remove collection folder
        self.step3_remove_collection_folder()
        
        # Summary
        self.print_header("✅ UNDO & MERGE COMPLETE!", Colors.GREEN)
        
        print(f"{Colors.BOLD}📊 Summary:{Colors.END}\n")
        print(f"  Files moved back to collection: {Colors.CYAN}{self.stats['moved_back']}{Colors.END}")
        print(f"  Files distributed to nocturne: {Colors.CYAN}{self.stats['distributed']}{Colors.END}")
        print(f"  Total processed: {Colors.CYAN}{self.stats['total_files']}{Colors.END}\n")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}⚠️  DRY RUN - Run with --live to execute{Colors.END}\n")
        else:
            print(f"{Colors.GREEN}✅ All songs merged into nocturne root!{Colors.END}")
            print(f"{Colors.GREEN}✅ Steven_Chaplinski_Collection removed!{Colors.END}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="🔄 Undo Collection & Merge")
    parser.add_argument('--dry-run', action='store_true', default=True)
    parser.add_argument('--live', action='store_true')
    
    args = parser.parse_args()
    
    merger = UndoAndMergeCollection(dry_run=not args.live)
    merger.run()


if __name__ == "__main__":
    main()
