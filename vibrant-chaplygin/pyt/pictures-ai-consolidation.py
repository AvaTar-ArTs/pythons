#!/usr/bin/env python3
"""
📸 PICTURES AI FOLDERS CONSOLIDATION
=====================================
Intelligently consolidate AI-generated image folders in ~/Pictures

Features:
✨ Merge Ideogram-related folders (ideo, ideo-ALL, ideo-notion, ideogram)
✨ Organize by aspect ratio (1:1, 9:16, 16:9) within each AI tool folder
✨ Clean up filenames (remove duplicates, normalize)
✨ Delete duplicate extracted archives
✨ CSV log for all operations
✨ Dry-run mode for safety
"""

import os
import re
import csv
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from PIL import Image


class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    END = "\033[0m"


class PicturesAIConsolidation:
    """Consolidate AI-generated image folders with aspect ratio organization"""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.pictures_dir = Path.home() / "Pictures"
        self.ai_images_dir = self.pictures_dir / "AI-Images"
        self.log_file = Path.home() / f"pictures_ai_consolidation_{self.timestamp}.csv"
        
        # AI folders to consolidate
        self.ideogram_folders = ['ideo', 'ideo-ALL', 'ideo-notion', 'ideogram']
        self.ai_tools = {
            'Ideogram': self.ideogram_folders,
            'DaLLe': ['DaLLe'],
            'Sora': ['sora'],
            'Grok': ['grok'],
            'DreamLab': ['DreamLab']
        }
        
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
        self.operations = []
        self.stats = {
            'images_organized': 0,
            'archives_deleted': 0,
            'space_saved_mb': 0,
            'duplicates_skipped': 0
        }

    def print_header(self, text: str, color=Colors.CYAN):
        """Print fancy header"""
        print(f"\n{color}{Colors.BOLD}{'='*80}")
        print(f"{text}")
        print(f"{'='*80}{Colors.END}\n")

    def clean_filename(self, filename: str) -> str:
        """Clean and normalize filename"""
        name = filename
        
        # Remove common problematic patterns
        name = re.sub(r'_\d{13}', '', name)  # Unix timestamps
        name = re.sub(r'\s+\(\d+\)', '', name)  # (1), (2) duplicates
        name = re.sub(r'[-_]+copy[-_]*\d*', '', name, flags=re.IGNORECASE)
        name = re.sub(r'[-_]+duplicate[-_]*\d*', '', name, flags=re.IGNORECASE)
        
        # Clean up separators
        name = re.sub(r'[-_]+', '-', name)
        name = re.sub(r'^-+|-+$', '', name)
        
        return name

    def get_aspect_ratio_folder(self, image_path: Path) -> str:
        """Determine aspect ratio folder for image"""
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                
                # Calculate aspect ratio
                ratio = width / height
                
                # Categorize (with tolerance)
                if 0.95 <= ratio <= 1.05:  # Square (1:1)
                    return "1-1"
                elif ratio < 0.95:  # Portrait
                    if 0.5 <= ratio <= 0.6:  # 9:16
                        return "9-16"
                    else:
                        return "9-16"  # Default portrait to 9:16
                else:  # Landscape
                    if 1.7 <= ratio <= 1.8:  # 16:9
                        return "16-9"
                    else:
                        return "16-9"  # Default landscape to 16:9
        except Exception as e:
            # If can't read image, use default
            return "unknown"

    def collect_all_images(self, source_folders: list) -> dict:
        """Collect all images from source folders"""
        images_by_ratio = defaultdict(list)
        other_files = []
        
        for folder_name in source_folders:
            folder_path = self.pictures_dir / folder_name
            if not folder_path.exists():
                continue
            
            for item in folder_path.rglob('*'):
                if not item.is_file():
                    continue
                
                if item.suffix.lower() in self.image_extensions:
                    ratio_folder = self.get_aspect_ratio_folder(item)
                    cleaned_name = self.clean_filename(item.name)
                    
                    images_by_ratio[ratio_folder].append({
                        'source': item,
                        'original_name': item.name,
                        'cleaned_name': cleaned_name,
                        'size': item.stat().st_size
                    })
                else:
                    # Non-image files (txt, html, json, etc.)
                    other_files.append(item)
        
        return images_by_ratio, other_files

    def plan_ai_tool_consolidation(self):
        """Create consolidation plan for all AI tools"""
        self.print_header("📋 CREATING AI CONSOLIDATION PLAN")
        
        for tool_name, source_folders in self.ai_tools.items():
            print(f"{Colors.BOLD}{tool_name}:{Colors.END}")
            
            # Check if any source folders exist
            existing_folders = [f for f in source_folders if (self.pictures_dir / f).exists()]
            if not existing_folders:
                print(f"  {Colors.YELLOW}No folders found{Colors.END}\n")
                continue
            
            # Collect images
            images_by_ratio, other_files = self.collect_all_images(source_folders)
            
            # Show breakdown
            total_images = sum(len(images) for images in images_by_ratio.values())
            print(f"  Source folders: {', '.join(existing_folders)}")
            print(f"  Total images: {total_images:,}")
            
            for ratio, images in sorted(images_by_ratio.items()):
                if images:
                    print(f"    {ratio:10s} → {len(images):,} images")
            
            if other_files:
                print(f"  Other files: {len(other_files):,} (txt, html, json, etc.)")
            
            # Create operations
            for ratio, images in images_by_ratio.items():
                for img_info in images:
                    target_dir = self.ai_images_dir / tool_name / ratio
                    target_path = target_dir / img_info['cleaned_name']
                    
                    self.operations.append({
                        'action': 'ORGANIZE_IMAGE',
                        'tool': tool_name,
                        'ratio': ratio,
                        'source': img_info['source'],
                        'target': target_path,
                        'size_mb': img_info['size'] / (1024**2)
                    })
            
            # Handle other files (put in root of tool folder)
            for file in other_files[:100]:  # Limit to avoid too many
                target_dir = self.ai_images_dir / tool_name / '_metadata'
                target_path = target_dir / file.name
                
                self.operations.append({
                    'action': 'MOVE_METADATA',
                    'tool': tool_name,
                    'ratio': '_metadata',
                    'source': file,
                    'target': target_path,
                    'size_mb': file.stat().st_size / (1024**2)
                })
            
            print()

    def find_duplicate_archives(self):
        """Find extracted archives to delete"""
        self.print_header("🗑️ FINDING DUPLICATE EXTRACTED ARCHIVES")
        
        duplicates = [
            {
                'path': self.pictures_dir / 'Adobe' / 'AutoMated-Mockups' / '280 ml can animated mockup.zip',
                'folder': self.pictures_dir / 'Adobe' / 'AutoMated-Mockups' / '280 ml can animated mockup',
                'size_mb': 665
            },
            {
                'path': self.pictures_dir / 'Adobe' / 'magic mug animated mockup.zip',
                'folder': self.pictures_dir / 'Adobe' / 'magic mug animated mockup',
                'size_mb': 360
            },
            {
                'path': self.pictures_dir / 'zip' / 'Onest.zip',
                'folder': self.pictures_dir / 'zip' / 'Onest',
                'size_mb': 0.7
            }
        ]
        
        found_duplicates = []
        for dup in duplicates:
            if dup['path'].exists() and dup['folder'].exists():
                found_duplicates.append(dup)
                self.operations.append({
                    'action': 'DELETE_ARCHIVE',
                    'tool': 'Archive Cleanup',
                    'ratio': 'N/A',
                    'source': dup['path'],
                    'target': None,
                    'size_mb': dup['size_mb']
                })
                print(f"{Colors.YELLOW}Delete:{Colors.END} {dup['path'].relative_to(self.pictures_dir)}")
                print(f"  Savings: {dup['size_mb']:.1f} MB\n")
        
        total_savings = sum(d['size_mb'] for d in found_duplicates)
        print(f"{Colors.GREEN}Total archive savings: {total_savings:.1f} MB{Colors.END}\n")

    def execute_operations(self):
        """Execute all planned operations"""
        self.print_header("⚡ EXECUTING OPERATIONS")
        
        print(f"Mode: {Colors.YELLOW}{'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}")
        print(f"Total operations: {len(self.operations):,}\n")
        
        # Group by action for cleaner output
        by_action = defaultdict(list)
        for op in self.operations:
            by_action[op['action']].append(op)
        
        for action, ops in by_action.items():
            print(f"{Colors.BOLD}{action}: {len(ops):,} operations{Colors.END}")
        
        print()
        
        # Execute with progress
        processed = 0
        for op in self.operations:
            processed += 1
            
            if processed % 500 == 0 or processed <= 10:
                print(f"Processing {processed:,}/{len(self.operations):,}...", end='\r')
            
            if not self.dry_run:
                try:
                    if op['action'] == 'DELETE_ARCHIVE':
                        op['source'].unlink()
                        self.stats['archives_deleted'] += 1
                        self.stats['space_saved_mb'] += op['size_mb']
                    
                    elif op['action'] in ['ORGANIZE_IMAGE', 'MOVE_METADATA']:
                        op['target'].parent.mkdir(parents=True, exist_ok=True)
                        
                        # Check for duplicates
                        if op['target'].exists():
                            self.stats['duplicates_skipped'] += 1
                            continue
                        
                        shutil.copy2(op['source'], op['target'])
                        self.stats['images_organized'] += 1
                    
                    op['status'] = 'COMPLETED'
                    
                except Exception as e:
                    op['status'] = f'FAILED: {e}'
            else:
                op['status'] = 'DRY_RUN'
                if op['action'] == 'DELETE_ARCHIVE':
                    self.stats['archives_deleted'] += 1
                    self.stats['space_saved_mb'] += op['size_mb']
                elif op['action'] in ['ORGANIZE_IMAGE', 'MOVE_METADATA']:
                    self.stats['images_organized'] += 1
        
        print(f"{Colors.GREEN}✅ Processed {processed:,} operations{Colors.END}\n")

    def save_log(self):
        """Save CSV log of all operations"""
        self.print_header("💾 SAVING LOG")
        
        with open(self.log_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Action', 'AI_Tool', 'Aspect_Ratio', 'Source', 'Target', 'Size_MB', 'Status'])
            
            for op in self.operations:
                writer.writerow([
                    op['action'],
                    op['tool'],
                    op['ratio'],
                    str(op['source']) if op['source'] else 'N/A',
                    str(op['target']) if op['target'] else 'N/A',
                    f"{op['size_mb']:.2f}",
                    op.get('status', 'PENDING')
                ])
        
        print(f"{Colors.GREEN}✅ Log saved: {self.log_file}{Colors.END}\n")

    def run(self):
        """Run complete consolidation"""
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║     📸 PICTURES AI FOLDERS CONSOLIDATION 📸                                   ║")
        print("║                                                                               ║")
        print("║     Merge → Clean → Organize by Aspect Ratio → Execute                       ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        # 1. Plan AI consolidation
        self.plan_ai_tool_consolidation()
        
        # 2. Find duplicates
        self.find_duplicate_archives()
        
        # 3. Execute
        self.execute_operations()
        
        # 4. Save log
        self.save_log()
        
        # Final summary
        self.print_header("✅ CONSOLIDATION COMPLETE!", Colors.GREEN)
        
        print(f"{Colors.BOLD}📊 Summary:{Colors.END}\n")
        print(f"  Images organized: {Colors.CYAN}{self.stats['images_organized']:,}{Colors.END}")
        print(f"  Duplicates skipped: {Colors.CYAN}{self.stats['duplicates_skipped']:,}{Colors.END}")
        print(f"  Archives deleted: {Colors.CYAN}{self.stats['archives_deleted']}{Colors.END}")
        print(f"  Space saved: {Colors.GREEN}{self.stats['space_saved_mb']:.2f} MB{Colors.END}\n")
        
        print(f"{Colors.BOLD}📝 New Structure:{Colors.END}")
        print(f"  ~/Pictures/AI-Images/")
        print(f"    ├── Ideogram/")
        print(f"    │   ├── 1-1/          [square images]")
        print(f"    │   ├── 9-16/         [portrait/vertical]")
        print(f"    │   ├── 16-9/         [landscape/horizontal]")
        print(f"    │   └── _metadata/    [txt, html, json files]")
        print(f"    ├── DaLLe/")
        print(f"    │   ├── 1-1/")
        print(f"    │   ├── 9-16/")
        print(f"    │   └── 16-9/")
        print(f"    ├── Sora/")
        print(f"    ├── Grok/")
        print(f"    └── DreamLab/\n")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}⚠️  This was a DRY RUN. Run with --live to execute.{Colors.END}\n")
            print(f"{Colors.CYAN}💡 Review the log file before running --live{Colors.END}\n")
        else:
            print(f"{Colors.GREEN}✅ AI folders consolidated successfully!{Colors.END}\n")
            print(f"{Colors.YELLOW}⚠️  Remember to delete original folders after verifying!{Colors.END}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="📸 Pictures AI Folders Consolidation")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Dry run mode (default)")
    parser.add_argument("--live", action="store_true", help="Live mode (execute consolidation)")
    
    args = parser.parse_args()
    
    consolidator = PicturesAIConsolidation(dry_run=not args.live)
    consolidator.run()


if __name__ == "__main__":
    main()
