#!/usr/bin/env python3
"""
🎯 ULTIMATE FOLDER CLEANUP - Final Pass
=========================================
Analyze ALL remaining folders and consolidate everything

Features:
✨ Find all similar/duplicate folders
✨ Merge all variants/versions
✨ Remove empty folders
✨ Clean up numbered/generated folders
✨ Consolidate by theme
✨ CSV log only (no heavy backups needed)
"""

import os
import csv
import shutil
import re
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher
from collections import defaultdict

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    END = "\033[0m"

class UltimateFolderCleanup:
    """Final comprehensive folder cleanup"""
    
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.nocturne_dir = Path.home() / "Music" / "nocTurneMeLoDieS"
        self.log_file = self.nocturne_dir / f"ULTIMATE_CLEANUP_LOG_{self.timestamp}.csv"
        
        self.actions = []
        self.stats = {'merged': 0, 'removed': 0, 'space_mb': 0}
    
    def print_header(self, text: str, color=Colors.CYAN):
        print(f"\n{color}{Colors.BOLD}{'='*80}\n{text}\n{'='*80}{Colors.END}\n")
    
    def normalize(self, name: str) -> str:
        """Aggressive normalization"""
        name = name.lower()
        name = re.sub(r'[_-]+', ' ', name)
        name = re.sub(r'\d+$', '', name)  # trailing numbers
        name = re.sub(r'\s+', ' ', name)
        return name.strip()
    
    def should_skip(self, folder_name: str) -> bool:
        """Check if folder should be skipped"""
        skip_patterns = [
            'DATA', 'DOCS', 'SUNO', 'SCRIPTS', 'BACKUP', 'ARCHIVE',
            'CLEANUP', 'CONSOLIDATION', 'SCAN', 'EXTRACTION', 'LOG'
        ]
        
        return any(p in folder_name.upper() for p in skip_patterns)
    
    def get_folder_stats(self, folder: Path) -> dict:
        """Get folder info"""
        audio_count = len(list(folder.glob('files/*.mp3'))) + len(list(folder.glob('files/*.m4a')))
        total_files = sum(1 for _ in folder.rglob('*') if _.is_file())
        total_size = sum(f.stat().st_size for f in folder.rglob('*') if f.is_file())
        
        return {
            'audio': audio_count,
            'files': total_files,
            'size_mb': total_size / (1024**2)
        }
    
    def find_and_merge_all_variants(self):
        """Find all folder variants and merge"""
        self.print_header("🔍 FINDING ALL VARIANTS TO MERGE")
        
        folders = [f for f in self.nocturne_dir.iterdir() if f.is_dir() and not self.should_skip(f.name)]
        
        # Group by normalized name
        by_normalized = defaultdict(list)
        for folder in folders:
            norm = self.normalize(folder.name)
            by_normalized[norm].append(folder)
        
        # Find groups with multiple folders
        merge_groups = [(k, v) for k, v in by_normalized.items() if len(v) > 1]
        
        print(f"Found {len(merge_groups)} groups with variants:\n")
        
        for norm_name, variant_folders in sorted(merge_groups):
            # Get stats for each
            variants_with_stats = []
            for folder in variant_folders:
                stats = self.get_folder_stats(folder)
                variants_with_stats.append((folder, stats))
            
            # Choose primary (most audio, then most files)
            primary, primary_stats = sorted(variants_with_stats, 
                                          key=lambda x: (-x[1]['audio'], -x[1]['files']))[0]
            
            print(f"{Colors.BOLD}{norm_name}{Colors.END}")
            print(f"  {Colors.GREEN}PRIMARY:{Colors.END} {primary.name} ({primary_stats['audio']} audio, {primary_stats['files']} files)")
            
            # Merge others into primary
            for folder, stats in variants_with_stats:
                if folder == primary:
                    continue
                
                print(f"  {Colors.YELLOW}MERGE:{Colors.END} {folder.name} ({stats['audio']} audio, {stats['files']} files)")
                
                # Execute merge
                if not self.dry_run:
                    try:
                        for item in folder.rglob('*'):
                            if item.is_file():
                                rel = item.relative_to(folder)
                                target = primary / rel
                                target.parent.mkdir(parents=True, exist_ok=True)
                                
                                if not target.exists():
                                    shutil.copy2(item, target)
                        
                        shutil.rmtree(folder)
                        print(f"    {Colors.GREEN}✅ Merged{Colors.END}")
                        
                        self.stats['merged'] += 1
                        self.actions.append({
                            'action': 'MERGE',
                            'from': folder.name,
                            'to': primary.name,
                            'files': stats['files'],
                            'size_mb': stats['size_mb']
                        })
                        
                    except Exception as e:
                        print(f"    {Colors.RED}❌ {e}{Colors.END}")
                else:
                    print(f"    {Colors.YELLOW}[DRY RUN]{Colors.END}")
                    self.stats['merged'] += 1
            
            print()
    
    def remove_empty_folders(self):
        """Remove empty folders"""
        self.print_header("🗑️ REMOVING EMPTY FOLDERS")
        
        folders = [f for f in self.nocturne_dir.iterdir() if f.is_dir() and not self.should_skip(f.name)]
        
        removed = 0
        
        for folder in folders:
            stats = self.get_folder_stats(folder)
            
            if stats['files'] == 0 or (stats['audio'] == 0 and stats['files'] < 5):
                print(f"{Colors.YELLOW}{folder.name}{Colors.END} (0 audio, {stats['files']} files)")
                
                if not self.dry_run:
                    try:
                        shutil.rmtree(folder)
                        print(f"  {Colors.GREEN}✅ Removed{Colors.END}\n")
                        removed += 1
                        self.stats['removed'] += 1
                    except Exception as e:
                        print(f"  {Colors.RED}❌ {e}{Colors.END}\n")
                else:
                    print(f"  {Colors.YELLOW}[DRY RUN] Would remove{Colors.END}\n")
                    removed += 1
                    self.stats['removed'] += 1
        
        print(f"{Colors.BOLD}Empty folders removed: {removed}{Colors.END}\n")
    
    def save_log(self):
        """Save CSV log"""
        with open(self.log_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Action', 'From', 'To', 'Files', 'Size_MB', 'Timestamp'])
            
            for action in self.actions:
                writer.writerow([
                    action['action'],
                    action.get('from', ''),
                    action.get('to', ''),
                    action.get('files', 0),
                    f"{action.get('size_mb', 0):.2f}",
                    datetime.now().isoformat()
                ])
        
        print(f"{Colors.GREEN}✅ CSV log: {self.log_file.name}{Colors.END}\n")
    
    def run(self):
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║          🎯 ULTIMATE FOLDER CLEANUP - FINAL PASS 🎯                           ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        print(f"Mode: {Colors.YELLOW}{'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}\n")
        
        # 1. Merge all variants
        self.find_and_merge_all_variants()
        
        # 2. Remove empty folders
        self.remove_empty_folders()
        
        # 3. Save log
        if self.actions:
            self.save_log()
        
        # Summary
        self.print_header("✅ ULTIMATE CLEANUP COMPLETE!", Colors.GREEN)
        
        print(f"{Colors.BOLD}📊 Final Statistics:{Colors.END}\n")
        print(f"  Folders merged: {Colors.CYAN}{self.stats['merged']}{Colors.END}")
        print(f"  Empty folders removed: {Colors.CYAN}{self.stats['removed']}{Colors.END}\n")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}⚠️  DRY RUN - Run with --live{Colors.END}\n")
        else:
            print(f"{Colors.GREEN}✅ Cleanup complete!{Colors.END}\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="🎯 Ultimate Folder Cleanup")
    parser.add_argument('--dry-run', action='store_true', default=True)
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    
    cleanup = UltimateFolderCleanup(dry_run=not args.live)
    cleanup.run()


if __name__ == "__main__":
    main()
