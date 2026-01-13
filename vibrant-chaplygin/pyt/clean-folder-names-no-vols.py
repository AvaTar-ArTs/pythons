#!/usr/bin/env python3
"""
📂 CLEAN FOLDER NAMES - Remove Vol Numbers
============================================
Rename folders to remove Vol._1, Vol_2, Vol_3 etc.

Features:
✨ Remove all "Vol" and version numbers from folder names
✨ Merge contents if clean name already exists
✨ Safe renaming with CSV log
✨ Handle all edge cases
"""

import os
import csv
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    END = "\033[0m"

class CleanFolderNames:
    """Remove Vol numbers from folder names"""
    
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.nocturne_dir = Path.home() / "Music" / "nocTurneMeLoDieS"
        self.log_file = self.nocturne_dir / f"FOLDER_RENAME_LOG_{self.timestamp}.csv"
        
        self.renames = []
        
        self.stats = {
            'folders_renamed': 0,
            'folders_merged': 0
        }
    
    def print_header(self, text: str, color=Colors.CYAN):
        """Print fancy header"""
        print(f"\n{color}{Colors.BOLD}{'='*80}")
        print(f"{text}")
        print(f"{'='*80}{Colors.END}\n")
    
    def clean_folder_name(self, name: str) -> str:
        """Remove Vol and version numbers from folder name"""
        import re
        
        # Remove patterns like "Vol._1", "Vol_2", "Vol._3", "Vol 1", etc.
        patterns = [
            r'_Vol\._\d+',
            r'_Vol_\d+',
            r'_Vol\d+',
            r' Vol\._\d+',
            r' Vol_\d+',
            r' Vol\d+',
            r'_v\d+',
            r' v\d+',
        ]
        
        cleaned = name
        for pattern in patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        # Clean up any trailing underscores or spaces
        cleaned = cleaned.rstrip('_').rstrip(' ')
        
        return cleaned
    
    def scan_and_rename_folders(self):
        """Scan for folders with Vol numbers and rename"""
        self.print_header("📂 SCANNING FOR FOLDERS WITH VOL NUMBERS")
        
        # Get all directories in nocTurneMeLoDieS
        all_dirs = [d for d in self.nocturne_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        
        folders_to_rename = []
        
        for folder in all_dirs:
            cleaned_name = self.clean_folder_name(folder.name)
            
            if cleaned_name != folder.name:
                folders_to_rename.append({
                    'old_path': folder,
                    'old_name': folder.name,
                    'new_name': cleaned_name,
                    'new_path': self.nocturne_dir / cleaned_name
                })
        
        print(f"Found {len(folders_to_rename)} folder(s) with Vol numbers\n")
        
        if not folders_to_rename:
            print(f"{Colors.GREEN}✅ All folders already have clean names!{Colors.END}")
            return
        
        # Show what will be renamed
        print(f"{Colors.BOLD}Folders to rename:{Colors.END}\n")
        
        for item in folders_to_rename:
            print(f"{Colors.YELLOW}Old:{Colors.END} {item['old_name']}")
            print(f"{Colors.GREEN}New:{Colors.END} {item['new_name']}")
            
            # Check if target already exists
            if item['new_path'].exists():
                print(f"{Colors.CYAN}→ Will merge into existing folder{Colors.END}")
                item['action'] = 'MERGE'
            else:
                print(f"{Colors.CYAN}→ Simple rename{Colors.END}")
                item['action'] = 'RENAME'
            
            print()
        
        # Execute renames/merges
        self.execute_renames(folders_to_rename)
    
    def execute_renames(self, folders_to_rename):
        """Execute folder renames and merges"""
        self.print_header("✏️ EXECUTING FOLDER RENAMES")
        
        print(f"Mode: {Colors.YELLOW}{'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}\n")
        
        for item in folders_to_rename:
            old_path = item['old_path']
            new_path = item['new_path']
            action = item['action']
            
            print(f"{Colors.BOLD}{item['old_name']}{Colors.END}")
            
            if action == 'MERGE':
                # Merge contents into existing folder
                print(f"  {Colors.CYAN}Merging into: {item['new_name']}{Colors.END}")
                
                if not self.dry_run:
                    try:
                        # Move all contents
                        for item_in_old in old_path.iterdir():
                            target = new_path / item_in_old.name
                            
                            if target.exists():
                                # If subfolder exists, merge recursively
                                if item_in_old.is_dir() and target.is_dir():
                                    # Copy contents
                                    for sub_item in item_in_old.rglob('*'):
                                        if sub_item.is_file():
                                            rel_path = sub_item.relative_to(item_in_old)
                                            target_file = target / rel_path
                                            target_file.parent.mkdir(parents=True, exist_ok=True)
                                            
                                            if not target_file.exists():
                                                shutil.copy2(sub_item, target_file)
                                else:
                                    # File conflict - skip or rename
                                    counter = 1
                                    while target.exists():
                                        target = new_path / f"{item_in_old.stem}_{counter}{item_in_old.suffix}"
                                        counter += 1
                                    shutil.move(str(item_in_old), target)
                            else:
                                shutil.move(str(item_in_old), target)
                        
                        # Remove old empty directory
                        old_path.rmdir()
                        
                        print(f"  {Colors.GREEN}✅ Merged and removed old folder{Colors.END}")
                        self.stats['folders_merged'] += 1
                        
                    except Exception as e:
                        print(f"  {Colors.RED}❌ Error: {e}{Colors.END}")
                else:
                    print(f"  {Colors.YELLOW}[DRY RUN] Would merge contents{Colors.END}")
                    self.stats['folders_merged'] += 1
            
            else:
                # Simple rename
                print(f"  {Colors.CYAN}Renaming to: {item['new_name']}{Colors.END}")
                
                if not self.dry_run:
                    try:
                        old_path.rename(new_path)
                        print(f"  {Colors.GREEN}✅ Renamed{Colors.END}")
                        self.stats['folders_renamed'] += 1
                        
                    except Exception as e:
                        print(f"  {Colors.RED}❌ Error: {e}{Colors.END}")
                else:
                    print(f"  {Colors.YELLOW}[DRY RUN] Would rename{Colors.END}")
                    self.stats['folders_renamed'] += 1
            
            # Log rename
            self.renames.append({
                'old_path': str(old_path),
                'new_path': str(new_path),
                'old_name': item['old_name'],
                'new_name': item['new_name'],
                'action': action,
                'status': 'COMPLETED' if not self.dry_run else 'DRY_RUN'
            })
            
            print()
    
    def save_log(self):
        """Save CSV log for revert"""
        self.print_header("💾 SAVING CSV LOG (For Revert)")
        
        with open(self.log_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Old_Path', 'New_Path', 'Old_Name', 'New_Name', 'Action', 'Status'
            ])
            
            for rename in self.renames:
                writer.writerow([
                    rename['old_path'],
                    rename['new_path'],
                    rename['old_name'],
                    rename['new_name'],
                    rename['action'],
                    rename['status']
                ])
        
        print(f"{Colors.GREEN}✅ CSV log: {self.log_file.name}{Colors.END}")
        print(f"{Colors.CYAN}💡 Contains old_path & new_path - use to revert if needed{Colors.END}\n")
    
    def run(self):
        """Run folder name cleaning"""
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║        📂 CLEAN FOLDER NAMES - REMOVE VOL NUMBERS 📂                          ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        print(f"Mode: {Colors.YELLOW}{'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}\n")
        
        # 1. Scan and rename
        self.scan_and_rename_folders()
        
        # 2. Save log
        if self.renames:
            self.save_log()
        
        # Final summary
        if self.renames:
            self.print_header("✅ FOLDER RENAMING COMPLETE!", Colors.GREEN)
            
            print(f"{Colors.BOLD}📊 Statistics:{Colors.END}\n")
            print(f"  Folders renamed: {Colors.CYAN}{self.stats['folders_renamed']}{Colors.END}")
            print(f"  Folders merged: {Colors.CYAN}{self.stats['folders_merged']}{Colors.END}\n")
            
            print(f"{Colors.BOLD}📝 CSV Log:{Colors.END}")
            print(f"  {self.log_file}\n")
            
            if self.dry_run:
                print(f"{Colors.YELLOW}⚠️  This was a DRY RUN. Run with --live to execute.{Colors.END}\n")
            else:
                print(f"{Colors.GREEN}✅ All folder names cleaned! No more Vol numbers.{Colors.END}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="📂 Clean Folder Names")
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Dry run mode (default)')
    parser.add_argument('--live', action='store_true',
                       help='Live mode (execute renames)')
    
    args = parser.parse_args()
    
    cleaner = CleanFolderNames(dry_run=not args.live)
    cleaner.run()


if __name__ == "__main__":
    main()
