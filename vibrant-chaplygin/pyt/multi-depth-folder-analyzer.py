#!/usr/bin/env python3
"""
🔍 MULTI-DEPTH FOLDER ANALYZER & CONSOLIDATOR
==============================================
Deep recursive analysis and consolidation at ALL folder levels

Features:
✨ Scan recursively to all depths
✨ Find duplicates/variants at every level
✨ Merge nested folders intelligently
✨ Remove empty nested directories
✨ Consolidate by theme across depths
✨ CSV log for all operations
"""

import os
import csv
import shutil
import re
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher
from collections import defaultdict
from typing import Dict, List, Tuple

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    END = "\033[0m"

class MultiDepthFolderAnalyzer:
    """Analyze and consolidate at all folder depths"""
    
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.nocturne_dir = Path.home() / "Music" / "nocTurneMeLoDieS"
        self.output_dir = self.nocturne_dir / f"MULTI_DEPTH_ANALYSIS_{self.timestamp}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.all_folders = []  # All folders at all depths
        self.by_depth = defaultdict(list)
        self.duplicates_by_depth = defaultdict(list)
        
        self.actions = []
        
        self.stats = {
            'total_folders': 0,
            'max_depth': 0,
            'merged': 0,
            'removed': 0,
            'space_freed_mb': 0
        }
    
    def print_header(self, text: str, color=Colors.CYAN):
        """Print fancy header"""
        print(f"\n{color}{Colors.BOLD}{'='*80}")
        print(f"{text}")
        print(f"{'='*80}{Colors.END}\n")
    
    def normalize_name(self, name: str) -> str:
        """Aggressive normalization"""
        name = name.lower()
        
        # Remove numbers, underscores, dashes
        name = re.sub(r'[_-]+', ' ', name)
        name = re.sub(r'\s*\(\d+\)\s*', '', name)  # (1), (2), etc.
        name = re.sub(r'\s+\d+$', '', name)  # trailing numbers
        name = re.sub(r'\s+', ' ', name)
        
        return name.strip()
    
    def should_skip(self, folder_name: str) -> bool:
        """Skip system/analysis folders"""
        skip_patterns = [
            'ARCHIVE_', 'BACKUP_', 'CLEANUP_', 'LOG_', 'SCAN_',
            'CONSOLIDATION', 'EXTRACTION', 'VERIFICATION',
            'ANALYSIS', 'MULTI_DEPTH'
        ]
        
        return any(p in folder_name.upper() for p in skip_patterns)
    
    def get_folder_info(self, folder_path: Path, depth: int) -> Dict:
        """Get comprehensive folder info"""
        audio_exts = {'.mp3', '.m4a', '.wav', '.flac'}
        
        audio_count = 0
        file_count = 0
        total_size = 0
        has_subfolders = False
        
        # Check immediate children
        try:
            items = list(folder_path.iterdir())
            has_subfolders = any(i.is_dir() for i in items)
        except Exception:
            pass
        
        # Count files recursively
        try:
            for item in folder_path.rglob('*'):
                if item.is_file():
                    file_count += 1
                    size = item.stat().st_size
                    total_size += size
                    
                    if item.suffix.lower() in audio_exts:
                        audio_count += 1
        except Exception:
            pass
        
        return {
            'audio_count': audio_count,
            'file_count': file_count,
            'total_size_mb': total_size / (1024**2),
            'has_subfolders': has_subfolders,
            'depth': depth
        }
    
    def scan_all_depths(self):
        """Recursively scan all folder depths"""
        self.print_header("🔍 SCANNING ALL FOLDER DEPTHS")
        
        print(f"Scanning: {self.nocturne_dir}\n")
        
        for root, dirs, files in os.walk(self.nocturne_dir):
            # Skip hidden and system folders
            dirs[:] = [d for d in dirs if not d.startswith('.') and not self.should_skip(d)]
            
            current_path = Path(root)
            
            try:
                depth = len(current_path.relative_to(self.nocturne_dir).parts)
            except ValueError:
                continue
            
            if depth > self.stats['max_depth']:
                self.stats['max_depth'] = depth
            
            for dir_name in dirs:
                folder_path = current_path / dir_name
                
                if self.should_skip(dir_name):
                    continue
                
                info = self.get_folder_info(folder_path, depth + 1)
                
                folder_data = {
                    'path': folder_path,
                    'name': dir_name,
                    'full_path': str(folder_path),
                    'relative_path': str(folder_path.relative_to(self.nocturne_dir)),
                    'normalized': self.normalize_name(dir_name),
                    'depth': depth + 1,
                    **info
                }
                
                self.all_folders.append(folder_data)
                self.by_depth[depth + 1].append(folder_data)
                self.stats['total_folders'] += 1
        
        print(f"{Colors.GREEN}✅ Found {self.stats['total_folders']} folders{Colors.END}")
        print(f"{Colors.CYAN}Max depth: {self.stats['max_depth']} levels{Colors.END}\n")
        
        # Show depth distribution
        print(f"{Colors.BOLD}Folders by depth:{Colors.END}\n")
        for depth in sorted(self.by_depth.keys()):
            print(f"  Level {depth}: {len(self.by_depth[depth])} folders")
        print()
    
    def find_duplicates_at_each_depth(self):
        """Find duplicate folders at each depth"""
        self.print_header("🔍 FINDING DUPLICATES BY DEPTH")
        
        for depth in sorted(self.by_depth.keys()):
            folders = self.by_depth[depth]
            
            # Group by normalized name
            by_normalized = defaultdict(list)
            for folder in folders:
                by_normalized[folder['normalized']].append(folder)
            
            # Find groups with multiple folders
            duplicates = [(k, v) for k, v in by_normalized.items() if len(v) > 1]
            
            if duplicates:
                print(f"{Colors.BOLD}Level {depth}:{Colors.END} {len(duplicates)} duplicate groups\n")
                
                for norm_name, variants in duplicates[:5]:  # Show first 5 per level
                    print(f"  '{norm_name}':")
                    for v in variants:
                        print(f"    • {v['relative_path']} ({v['audio_count']} audio, {v['file_count']} files)")
                    print()
                
                if len(duplicates) > 5:
                    print(f"  ... and {len(duplicates) - 5} more groups\n")
                
                self.duplicates_by_depth[depth] = duplicates
    
    def consolidate_from_bottom_up(self):
        """Consolidate folders from deepest to shallowest"""
        self.print_header("🔀 CONSOLIDATING (Bottom-Up)")
        
        print(f"Processing from depth {self.stats['max_depth']} to 1\n")
        
        # Process from deepest to shallowest
        for depth in sorted(self.by_depth.keys(), reverse=True):
            if depth not in self.duplicates_by_depth:
                continue
            
            duplicates = self.duplicates_by_depth[depth]
            
            print(f"{Colors.BOLD}=== Level {depth} ==={Colors.END}\n")
            
            for norm_name, variants in duplicates:
                # Sort by file count (keep the one with most content)
                variants_sorted = sorted(variants, key=lambda x: (-x['audio_count'], -x['file_count']))
                
                primary = variants_sorted[0]
                merge_into_primary = variants_sorted[1:]
                
                if not merge_into_primary:
                    continue
                
                print(f"{norm_name}:")
                print(f"  {Colors.GREEN}KEEP:{Colors.END} {primary['relative_path']}")
                
                for variant in merge_into_primary:
                    print(f"  {Colors.YELLOW}MERGE:{Colors.END} {variant['relative_path']}")
                    
                    # Execute merge
                    if not self.dry_run:
                        try:
                            # Copy all files
                            for item in variant['path'].rglob('*'):
                                if item.is_file():
                                    rel = item.relative_to(variant['path'])
                                    target = primary['path'] / rel
                                    target.parent.mkdir(parents=True, exist_ok=True)
                                    
                                    if not target.exists():
                                        shutil.copy2(item, target)
                            
                            # Remove old folder
                            shutil.rmtree(variant['path'])
                            
                            print(f"    {Colors.GREEN}✅ Merged{Colors.END}")
                            
                            self.stats['merged'] += 1
                            self.stats['space_freed_mb'] += variant['total_size_mb']
                            
                            self.actions.append({
                                'depth': depth,
                                'action': 'MERGE',
                                'from': variant['relative_path'],
                                'to': primary['relative_path'],
                                'files': variant['file_count'],
                                'size_mb': variant['total_size_mb']
                            })
                            
                        except Exception as e:
                            print(f"    {Colors.RED}❌ {e}{Colors.END}")
                    else:
                        print(f"    {Colors.YELLOW}[DRY RUN]{Colors.END}")
                        self.stats['merged'] += 1
                
                print()
    
    def remove_empty_at_all_depths(self):
        """Remove empty folders at all depths (bottom-up)"""
        self.print_header("🗑️ REMOVING EMPTY FOLDERS (All Depths)")
        
        removed_count = 0
        
        # Process from deepest to shallowest
        for depth in sorted(self.by_depth.keys(), reverse=True):
            folders = self.by_depth[depth]
            
            for folder in folders:
                # Re-check if empty (might have been emptied by previous operations)
                try:
                    items = list(folder['path'].iterdir())
                    non_hidden = [i for i in items if not i.name.startswith('.')]
                    
                    is_empty = len(non_hidden) == 0 or folder['file_count'] == 0
                    
                    if is_empty and folder['path'].exists():
                        if not self.dry_run:
                            try:
                                shutil.rmtree(folder['path'])
                                print(f"{Colors.GREEN}✅ Removed empty:{Colors.END} {folder['relative_path']}")
                                removed_count += 1
                                self.stats['removed'] += 1
                            except Exception:
                                pass
                        else:
                            print(f"{Colors.YELLOW}[DRY RUN] Remove empty:{Colors.END} {folder['relative_path']}")
                            removed_count += 1
                            self.stats['removed'] += 1
                
                except Exception:
                    pass
        
        print(f"\n{Colors.BOLD}Empty folders removed: {removed_count}{Colors.END}\n")
    
    def save_comprehensive_report(self):
        """Save detailed CSV report"""
        self.print_header("💾 SAVING COMPREHENSIVE REPORT")
        
        # CSV log
        log_file = self.output_dir / "MULTI_DEPTH_CLEANUP_LOG.csv"
        
        with open(log_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Depth', 'Action', 'From_Path', 'To_Path', 'Files', 'Size_MB'])
            
            for action in self.actions:
                writer.writerow([
                    action['depth'],
                    action['action'],
                    action['from'],
                    action.get('to', ''),
                    action['files'],
                    f"{action['size_mb']:.2f}"
                ])
        
        print(f"{Colors.GREEN}✅ CSV log: {log_file.name}{Colors.END}")
        
        # Summary by depth
        summary_file = self.output_dir / "DEPTH_ANALYSIS_SUMMARY.csv"
        
        with open(summary_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Depth', 'Total_Folders', 'Duplicate_Groups', 'Action_Taken'])
            
            for depth in sorted(self.by_depth.keys()):
                dup_count = len(self.duplicates_by_depth.get(depth, []))
                actions_at_depth = [a for a in self.actions if a.get('depth') == depth]
                
                writer.writerow([
                    depth,
                    len(self.by_depth[depth]),
                    dup_count,
                    len(actions_at_depth)
                ])
        
        print(f"{Colors.GREEN}✅ Summary: {summary_file.name}{Colors.END}\n")
    
    def run(self):
        """Run multi-depth analysis and consolidation"""
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║        🔍 MULTI-DEPTH FOLDER ANALYZER & CONSOLIDATOR 🔍                       ║")
        print("║                                                                               ║")
        print("║     Scan All Depths → Find Variants → Merge → Clean                          ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        print(f"Mode: {Colors.YELLOW}{'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}\n")
        
        # 1. Scan all depths
        self.scan_all_depths()
        
        # 2. Find duplicates by depth
        self.find_duplicates_at_each_depth()
        
        # 3. Consolidate bottom-up
        self.consolidate_from_bottom_up()
        
        # 4. Remove empty folders
        self.remove_empty_at_all_depths()
        
        # 5. Save reports
        self.save_comprehensive_report()
        
        # Final summary
        self.print_header("✅ MULTI-DEPTH CONSOLIDATION COMPLETE!", Colors.GREEN)
        
        print(f"{Colors.BOLD}📊 Final Statistics:{Colors.END}\n")
        print(f"  Total folders analyzed: {Colors.CYAN}{self.stats['total_folders']}{Colors.END}")
        print(f"  Maximum depth found: {Colors.CYAN}{self.stats['max_depth']}{Colors.END}")
        print(f"  Folders merged: {Colors.CYAN}{self.stats['merged']}{Colors.END}")
        print(f"  Empty folders removed: {Colors.CYAN}{self.stats['removed']}{Colors.END}")
        print(f"  Space freed: {Colors.GREEN}{self.stats['space_freed_mb']:.2f} MB{Colors.END}\n")
        
        print(f"{Colors.BOLD}📁 Reports:{Colors.END}")
        print(f"  {self.output_dir}\n")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}⚠️  This was a DRY RUN. Run with --live to execute.{Colors.END}\n")
        else:
            print(f"{Colors.GREEN}✅ All depths consolidated! Structure is clean.{Colors.END}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="🔍 Multi-Depth Folder Analyzer")
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Dry run mode (default)')
    parser.add_argument('--live', action='store_true',
                       help='Live mode (execute consolidation)')
    
    args = parser.parse_args()
    
    analyzer = MultiDepthFolderAnalyzer(dry_run=not args.live)
    analyzer.run()


if __name__ == "__main__":
    main()
