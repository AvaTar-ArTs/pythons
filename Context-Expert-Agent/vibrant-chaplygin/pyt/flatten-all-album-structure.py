#!/usr/bin/env python3
"""
🎵 FLATTEN ALL ALBUM STRUCTURES
================================
Remove files/, lyrics/, metadata/ subfolders
Move all content directly into album folders

Structure:
  Before: Bite_in_the_Night/files/song.mp3
  After:  Bite_in_the_Night/song.mp3
  
  Before: Bite_in_the_Night/lyrics/transcript.txt
  After:  Bite_in_the_Night/transcript.txt
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

class FlattenAlbumStructure:
    """Flatten all album folder structures"""
    
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.nocturne_dir = Path.home() / "Music" / "nocTurneMeLoDieS"
        
        self.stats = {
            'albums_flattened': 0,
            'files_moved': 0,
            'folders_removed': 0
        }
        
        # Subfolders to flatten
        self.subfolders_to_flatten = ['files', 'lyrics', 'analysis', 'metadata', 'images', 'prompts']
    
    def print_header(self, text: str, color=Colors.CYAN):
        print(f"\n{color}{Colors.BOLD}{'='*80}\n{text}\n{'='*80}{Colors.END}\n")
    
    def flatten_album(self, album_path: Path):
        """Flatten single album folder"""
        flattened_any = False
        
        for subfolder_name in self.subfolders_to_flatten:
            subfolder = album_path / subfolder_name
            
            if not subfolder.exists() or not subfolder.is_dir():
                continue
            
            # Get all files in subfolder
            files = list(subfolder.rglob('*'))
            files = [f for f in files if f.is_file()]
            
            if not files:
                # Empty folder, remove it
                if not self.dry_run:
                    try:
                        shutil.rmtree(subfolder)
                        self.stats['folders_removed'] += 1
                    except Exception:
                        pass
                continue
            
            # Move all files up to parent
            for file in files:
                target = album_path / file.name
                
                # Handle duplicates by adding number
                if target.exists():
                    base = target.stem
                    ext = target.suffix
                    counter = 1
                    while target.exists():
                        target = album_path / f"{base}_{counter}{ext}"
                        counter += 1
                
                if not self.dry_run:
                    try:
                        shutil.move(str(file), str(target))
                        self.stats['files_moved'] += 1
                        flattened_any = True
                    except Exception as e:
                        print(f"  {Colors.RED}Error moving {file.name}: {e}{Colors.END}")
                else:
                    self.stats['files_moved'] += 1
                    flattened_any = True
            
            # Remove empty subfolder
            if not self.dry_run:
                try:
                    shutil.rmtree(subfolder)
                    self.stats['folders_removed'] += 1
                except Exception:
                    pass
        
        return flattened_any
    
    def flatten_all_albums(self):
        """Flatten all album folders"""
        self.print_header("📦 FLATTENING ALL ALBUM STRUCTURES")
        
        print("Processing albums...\n")
        
        for item in sorted(self.nocturne_dir.iterdir()):
            if not item.is_dir():
                continue
            
            # Skip system/analysis folders
            if any(skip in item.name.upper() for skip in 
                   ['ANALYSIS', 'LOG', 'SCAN', 'BACKUP', 'CONSOLIDATION', 'EXTRACTION']):
                continue
            
            # Skip if it's just a file container (no nested structure)
            has_subfolders = any(
                (item / subfolder).exists() 
                for subfolder in self.subfolders_to_flatten
            )
            
            if not has_subfolders:
                continue
            
            # Check what's in there
            file_count = sum(1 for _ in item.rglob('*') if _.is_file())
            
            if file_count == 0:
                continue
            
            print(f"{Colors.CYAN}{item.name}{Colors.END}")
            
            flattened = self.flatten_album(item)
            
            if flattened:
                print(f"  {Colors.GREEN}✅ Flattened{Colors.END}\n")
                self.stats['albums_flattened'] += 1
            else:
                print(f"  {Colors.YELLOW}⚠️ No changes needed{Colors.END}\n")
    
    def distribute_collection_and_remove(self):
        """Distribute Steven_Chaplinski_Collection and remove it"""
        self.print_header("📤 DISTRIBUTING COLLECTION TO NOCTURNE ROOT")
        
        collection_dir = self.nocturne_dir / "Steven_Chaplinski_Collection"
        
        if not collection_dir.exists():
            print(f"{Colors.YELLOW}Collection folder not found{Colors.END}")
            return
        
        # Get all MP3s from collection
        collection_files = collection_dir / "files"
        
        if collection_files.exists():
            mp3_files = list(collection_files.glob("*.mp3"))
            
            print(f"Found {len(mp3_files)} MP3s in collection\n")
            
            # Move to nocturne root
            for mp3 in mp3_files:
                target = self.nocturne_dir / mp3.name
                
                # Skip if exists
                if target.exists():
                    continue
                
                if not self.dry_run:
                    shutil.move(str(mp3), str(target))
                    self.stats['files_moved'] += 1
                    
                    if self.stats['files_moved'] % 100 == 0:
                        print(f"{Colors.GREEN}✅ Moved {self.stats['files_moved']} files...{Colors.END}")
                else:
                    self.stats['files_moved'] += 1
        
        # Remove collection folder
        if not self.dry_run:
            try:
                shutil.rmtree(collection_dir)
                print(f"\n{Colors.GREEN}✅ Removed Steven_Chaplinski_Collection{Colors.END}")
            except Exception as e:
                print(f"\n{Colors.RED}❌ Error removing collection: {e}{Colors.END}")
        else:
            print(f"\n{Colors.YELLOW}[DRY RUN] Would remove Steven_Chaplinski_Collection{Colors.END}")
    
    def run(self):
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║              🎵 FLATTEN ALL ALBUM STRUCTURES 🎵                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        print(f"Mode: {Colors.YELLOW}{'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}\n")
        
        # Step 1: Flatten all albums
        self.flatten_all_albums()
        
        # Step 2: Distribute collection
        self.distribute_collection_and_remove()
        
        # Summary
        self.print_header("✅ FLATTENING COMPLETE!", Colors.GREEN)
        
        print(f"{Colors.BOLD}📊 Summary:{Colors.END}\n")
        print(f"  Albums flattened: {Colors.CYAN}{self.stats['albums_flattened']}{Colors.END}")
        print(f"  Files moved: {Colors.CYAN}{self.stats['files_moved']}{Colors.END}")
        print(f"  Folders removed: {Colors.CYAN}{self.stats['folders_removed']}{Colors.END}\n")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}⚠️  DRY RUN - Run with --live to execute{Colors.END}\n")
        else:
            print(f"{Colors.GREEN}✅ All albums now have flat structure!{Colors.END}")
            print(f"{Colors.GREEN}✅ No more files/, lyrics/ subfolders!{Colors.END}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="🎵 Flatten Album Structures")
    parser.add_argument('--dry-run', action='store_true', default=True)
    parser.add_argument('--live', action='store_true')
    
    args = parser.parse_args()
    
    flattener = FlattenAlbumStructure(dry_run=not args.live)
    flattener.run()


if __name__ == "__main__":
    main()
