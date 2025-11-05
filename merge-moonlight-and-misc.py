#!/usr/bin/env python3
"""
🌙 MERGE MOONLIGHT FOLDERS & ORGANIZE MISCELLANEOUS
====================================================
Specific consolidation for moonlight-themed and misc folders

Merges:
✨ Moonlight_Night → Moonlight_Serenade
✨ moonly-alley--howling-banjo239 → Moonlight_Serenade  
✨ Moonly_Alley_1_1 → Moonlight_Serenade
✨ Midnight_Reckoning + sammy_Midnight_Reckoning → Midnight_Reckoning
✨ Miscellaneous (25 MP3s) → Categorize and distribute
"""

import os
import csv
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

class MoonlightMiscMerger:
    """Merge moonlight folders and organize miscellaneous"""
    
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.nocturne_dir = Path.home() / "Music" / "nocTurneMeLoDieS"
        self.log_file = self.nocturne_dir / f"MOONLIGHT_MISC_MERGE_LOG_{self.timestamp}.csv"
        
        self.actions = []
        
        self.stats = {
            'folders_merged': 0,
            'files_moved': 0,
            'space_freed_mb': 0
        }
    
    def print_header(self, text: str, color=Colors.CYAN):
        """Print fancy header"""
        print(f"\n{color}{Colors.BOLD}{'='*80}")
        print(f"{text}")
        print(f"{'='*80}{Colors.END}\n")
    
    def merge_folder(self, from_folder: str, to_folder: str, description: str):
        """Merge one folder into another"""
        from_path = self.nocturne_dir / from_folder
        to_path = self.nocturne_dir / to_folder
        
        if not from_path.exists():
            print(f"{Colors.YELLOW}⚠️  {from_folder} doesn't exist - already merged?{Colors.END}\n")
            return
        
        print(f"{Colors.BOLD}{from_folder}{Colors.END}")
        print(f"  → Into: {to_folder}")
        print(f"  Reason: {description}")
        
        # Get file count
        file_count = sum(1 for _ in from_path.rglob('*') if _.is_file())
        folder_size = sum(f.stat().st_size for f in from_path.rglob('*') if f.is_file())
        
        print(f"  Files: {file_count} ({folder_size / (1024**2):.2f} MB)")
        
        if not self.dry_run:
            try:
                # Ensure target exists
                to_path.mkdir(parents=True, exist_ok=True)
                
                # Merge all contents
                for item in from_path.rglob('*'):
                    if item.is_file():
                        rel_path = item.relative_to(from_path)
                        target = to_path / rel_path
                        target.parent.mkdir(parents=True, exist_ok=True)
                        
                        # Skip if exists
                        if not target.exists():
                            shutil.copy2(item, target)
                            self.stats['files_moved'] += 1
                
                # Remove old folder
                shutil.rmtree(from_path)
                
                print(f"  {Colors.GREEN}✅ Merged and removed{Colors.END}")
                self.stats['folders_merged'] += 1
                self.stats['space_freed_mb'] += folder_size / (1024**2)
                
                self.actions.append({
                    'action': 'MERGE',
                    'from': from_folder,
                    'to': to_folder,
                    'files': file_count,
                    'size_mb': folder_size / (1024**2)
                })
                
            except Exception as e:
                print(f"  {Colors.RED}❌ Error: {e}{Colors.END}")
        else:
            print(f"  {Colors.YELLOW}[DRY RUN] Would merge{Colors.END}")
        
        print()
    
    def merge_moonlight_folders(self):
        """Merge all moonlight-themed folders"""
        self.print_header("🌙 MERGING MOONLIGHT-THEMED FOLDERS")
        
        merges = [
            ('Moonlight_Night', 'Moonlight_Serenade', 'Same moonlight theme'),
            ('moonly-alley--howling-banjo239', 'Moonlight_Serenade', 'Moonly Alley song variant'),
            ('Moonly_Alley_1_1', 'Moonlight_Serenade', 'Moonly Alley numbered version'),
        ]
        
        for from_folder, to_folder, description in merges:
            self.merge_folder(from_folder, to_folder, description)
    
    def merge_midnight_folders(self):
        """Merge midnight reckoning folders"""
        self.print_header("🌃 MERGING MIDNIGHT_RECKONING FOLDERS")
        
        self.merge_folder(
            'sammy_Midnight_Reckoning_by_DarkSoundEffect3495___Suno_Remix',
            'Midnight_Reckoning',
            'Sammy variant of Midnight Reckoning'
        )
    
    def organize_miscellaneous(self):
        """Organize miscellaneous folder"""
        self.print_header("📦 ORGANIZING MISCELLANEOUS FOLDER")
        
        misc_path = self.nocturne_dir / "Miscellaneous"
        
        if not misc_path.exists():
            print(f"{Colors.YELLOW}⚠️  Miscellaneous folder doesn't exist{Colors.END}\n")
            return
        
        # Get all MP3s
        mp3_files = list(misc_path.glob('files/*.mp3'))
        
        print(f"Found {len(mp3_files)} MP3 files in Miscellaneous\n")
        
        if not mp3_files:
            print(f"{Colors.GREEN}✅ No files to organize{Colors.END}\n")
            return
        
        # Show sample files
        print(f"{Colors.BOLD}Sample files to organize:{Colors.END}\n")
        for mp3 in mp3_files[:10]:
            print(f"  • {mp3.name}")
        
        if len(mp3_files) > 10:
            print(f"  ... and {len(mp3_files) - 10} more")
        
        print(f"\n{Colors.CYAN}💡 Recommendation: Move to Steven_Chaplinski_Collection/{Colors.END}")
        print(f"{Colors.CYAN}These appear to be uncategorized songs{Colors.END}\n")
        
        # Merge into collection
        target = self.nocturne_dir / "Steven_Chaplinski_Collection"
        target.mkdir(parents=True, exist_ok=True)
        
        if not self.dry_run:
            try:
                # Merge
                for item in misc_path.rglob('*'):
                    if item.is_file():
                        rel_path = item.relative_to(misc_path)
                        target_file = target / rel_path
                        target_file.parent.mkdir(parents=True, exist_ok=True)
                        
                        if not target_file.exists():
                            shutil.copy2(item, target_file)
                
                # Remove misc folder
                shutil.rmtree(misc_path)
                
                print(f"{Colors.GREEN}✅ Merged Miscellaneous → Steven_Chaplinski_Collection{Colors.END}\n")
                self.stats['folders_merged'] += 1
                
                self.actions.append({
                    'action': 'MERGE',
                    'from': 'Miscellaneous',
                    'to': 'Steven_Chaplinski_Collection',
                    'files': len(mp3_files),
                    'size_mb': sum(f.stat().st_size for f in mp3_files) / (1024**2)
                })
                
            except Exception as e:
                print(f"{Colors.RED}❌ Error: {e}{Colors.END}\n")
        else:
            print(f"{Colors.YELLOW}[DRY RUN] Would merge Miscellaneous → Steven_Chaplinski_Collection{Colors.END}\n")
    
    def save_log(self):
        """Save CSV log"""
        with open(self.log_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Action', 'From', 'To', 'Files', 'Size_MB'])
            
            for action in self.actions:
                writer.writerow([
                    action['action'],
                    action['from'],
                    action['to'],
                    action['files'],
                    f"{action['size_mb']:.2f}"
                ])
        
        print(f"{Colors.GREEN}✅ Log: {self.log_file.name}{Colors.END}\n")
    
    def run(self):
        """Run targeted merges"""
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║     🌙 MERGE MOONLIGHT & ORGANIZE MISCELLANEOUS 🌙                            ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        print(f"Mode: {Colors.YELLOW}{'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}\n")
        
        # 1. Merge moonlight folders
        self.merge_moonlight_folders()
        
        # 2. Merge midnight folders
        self.merge_midnight_folders()
        
        # 3. Organize miscellaneous
        self.organize_miscellaneous()
        
        # 4. Save log
        if self.actions:
            self.save_log()
        
        # Summary
        self.print_header("✅ TARGETED CONSOLIDATION COMPLETE!", Colors.GREEN)
        
        print(f"{Colors.BOLD}📊 Statistics:{Colors.END}\n")
        print(f"  Folders merged: {Colors.CYAN}{self.stats['folders_merged']}{Colors.END}")
        print(f"  Files moved: {Colors.CYAN}{self.stats['files_moved']}{Colors.END}\n")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}⚠️  DRY RUN - Run with --live to execute{Colors.END}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="🌙 Merge Moonlight & Misc")
    parser.add_argument('--dry-run', action='store_true', default=True)
    parser.add_argument('--live', action='store_true')
    
    args = parser.parse_args()
    
    merger = MoonlightMiscMerger(dry_run=not args.live)
    merger.run()


if __name__ == "__main__":
    main()
