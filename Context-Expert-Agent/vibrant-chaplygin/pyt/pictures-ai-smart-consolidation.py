#!/usr/bin/env python3
"""
📸 SMART PICTURES AI CONSOLIDATION
===================================
Intelligently merge, deduplicate, and organize AI images

Features:
✨ Detect duplicate/similar images using perceptual hashing
✨ Group variations of same image together
✨ Organize by aspect ratio (1:1, 9:16, 16:9)
✨ Clean filenames and remove duplicates
✨ Smart merging of related content
✨ Keep best quality version of duplicates
"""

import os
import re
import csv
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from PIL import Image
import imagehash


class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    END = "\033[0m"


class SmartAIConsolidation:
    """Smart AI image consolidation with deduplication"""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.pictures_dir = Path.home() / "Pictures"
        self.ai_images_dir = self.pictures_dir / "AI-Images"
        self.log_file = Path.home() / f"smart_ai_consolidation_{self.timestamp}.csv"
        
        # AI tools configuration
        self.ai_tools = {
            'Ideogram': ['ideo', 'ideo-ALL', 'ideo-notion', 'ideogram'],
            'DaLLe': ['DaLLe'],
            'Sora': ['sora'],
            'Grok': ['grok'],
            'DreamLab': ['DreamLab']
        }
        
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
        
        # Tracking
        self.image_hashes = {}  # hash -> best image info
        self.operations = []
        self.stats = {
            'total_images': 0,
            'duplicates_found': 0,
            'variations_found': 0,
            'images_kept': 0,
            'space_saved_mb': 0,
            'archives_deleted': 0
        }

    def print_header(self, text: str, color=Colors.CYAN):
        """Print header"""
        print(f"\n{color}{Colors.BOLD}{'='*80}")
        print(f"{text}")
        print(f"{'='*80}{Colors.END}\n")

    def get_image_hash(self, image_path: Path) -> tuple:
        """Get perceptual hash of image"""
        try:
            with Image.open(image_path) as img:
                # Perceptual hash (detects similar images)
                phash = str(imagehash.phash(img))
                # Average hash (faster, for exact duplicates)
                ahash = str(imagehash.average_hash(img))
                return (phash, ahash)
        except Exception as e:
            return (None, None)

    def get_aspect_ratio_category(self, width: int, height: int) -> str:
        """Categorize aspect ratio"""
        ratio = width / height
        
        if 0.95 <= ratio <= 1.05:
            return "1-1"
        elif ratio < 0.95:
            return "9-16"
        else:
            return "16-9"

    def get_image_quality_score(self, image_path: Path) -> int:
        """Calculate quality score for choosing best version"""
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                # Higher resolution = better
                pixels = width * height
                # Prefer original filenames over numbered variations
                filename_score = 100 if not re.search(r'\(\d+\)|-\d+\.', image_path.name) else 0
                return pixels + filename_score
        except:
            return 0

    def clean_filename(self, filename: str) -> str:
        """Clean filename"""
        name, ext = os.path.splitext(filename)
        
        # Remove common patterns
        name = re.sub(r'_\d{13}', '', name)  # Timestamps
        name = re.sub(r'\s*\(\d+\)', '', name)  # (1), (2)
        name = re.sub(r'[-_]copy[-_]*\d*', '', name, flags=re.IGNORECASE)
        name = re.sub(r'[-_]duplicate', '', name, flags=re.IGNORECASE)
        name = re.sub(r'[-_]variation[-_]*\d*', '', name, flags=re.IGNORECASE)
        name = re.sub(r'[-_]v\d+', '', name)
        
        # Clean separators
        name = re.sub(r'[-_]+', '-', name)
        name = re.sub(r'^-+|-+$', '', name)
        
        return name + ext

    def scan_and_deduplicate(self, tool_name: str, source_folders: list):
        """Scan images and detect duplicates"""
        print(f"{Colors.BOLD}Scanning {tool_name}...{Colors.END}")
        
        images_by_hash = defaultdict(list)
        images_by_ratio = defaultdict(list)
        
        for folder_name in source_folders:
            folder_path = self.pictures_dir / folder_name
            if not folder_path.exists():
                continue
            
            for item in folder_path.rglob('*'):
                if not item.is_file() or item.suffix.lower() not in self.image_extensions:
                    continue
                
                self.stats['total_images'] += 1
                
                # Get hashes
                phash, ahash = self.get_image_hash(item)
                if not phash:
                    continue
                
                # Get metadata
                try:
                    with Image.open(item) as img:
                        width, height = img.size
                        ratio_cat = self.get_aspect_ratio_category(width, height)
                except:
                    continue
                
                quality_score = self.get_image_quality_score(item)
                
                image_info = {
                    'path': item,
                    'phash': phash,
                    'ahash': ahash,
                    'ratio': ratio_cat,
                    'quality': quality_score,
                    'size': item.stat().st_size,
                    'width': width,
                    'height': height,
                    'cleaned_name': self.clean_filename(item.name)
                }
                
                # Group by perceptual hash (finds variations)
                images_by_hash[phash].append(image_info)
        
        # Process hash groups
        kept_images = []
        for phash, images in images_by_hash.items():
            if len(images) > 1:
                # Multiple images with same perceptual hash = variations
                self.stats['variations_found'] += len(images) - 1
                # Keep highest quality
                best = max(images, key=lambda x: x['quality'])
                kept_images.append(best)
                
                print(f"  Found {len(images)} variations, keeping best: {best['path'].name}")
            else:
                kept_images.append(images[0])
        
        # Further check for exact duplicates by file content
        content_hashes = {}
        final_images = []
        
        for img_info in kept_images:
            # Calculate file hash
            with open(img_info['path'], 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            
            if file_hash in content_hashes:
                self.stats['duplicates_found'] += 1
                self.stats['space_saved_mb'] += img_info['size'] / (1024**2)
                print(f"  Duplicate: {img_info['path'].name}")
            else:
                content_hashes[file_hash] = img_info
                final_images.append(img_info)
                images_by_ratio[img_info['ratio']].append(img_info)
        
        self.stats['images_kept'] += len(final_images)
        
        # Show breakdown
        print(f"  Total found: {self.stats['total_images']:,}")
        print(f"  After dedup: {len(final_images):,}")
        for ratio in ['1-1', '9-16', '16-9']:
            if ratio in images_by_ratio:
                print(f"    {ratio:10s} {len(images_by_ratio[ratio]):,} images")
        print()
        
        return images_by_ratio

    def create_consolidation_plan(self):
        """Create smart consolidation plan"""
        self.print_header("📋 SMART CONSOLIDATION PLAN")
        
        for tool_name, source_folders in self.ai_tools.items():
            images_by_ratio = self.scan_and_deduplicate(tool_name, source_folders)
            
            # Create operations
            for ratio, images in images_by_ratio.items():
                for img_info in images:
                    target_dir = self.ai_images_dir / tool_name / ratio
                    target_path = target_dir / img_info['cleaned_name']
                    
                    # Handle name collisions
                    counter = 1
                    while target_path in [op['target'] for op in self.operations]:
                        name, ext = os.path.splitext(img_info['cleaned_name'])
                        target_path = target_dir / f"{name}-{counter}{ext}"
                        counter += 1
                    
                    self.operations.append({
                        'action': 'COPY_BEST',
                        'tool': tool_name,
                        'ratio': ratio,
                        'source': img_info['path'],
                        'target': target_path,
                        'size_mb': img_info['size'] / (1024**2),
                        'dimensions': f"{img_info['width']}x{img_info['height']}"
                    })

    def add_archive_deletions(self):
        """Add duplicate archive deletions"""
        self.print_header("🗑️ DUPLICATE ARCHIVES")
        
        duplicates = [
            ('Adobe/AutoMated-Mockups/280 ml can animated mockup.zip', 665),
            ('Adobe/magic mug animated mockup.zip', 360),
            ('zip/Onest.zip', 0.7)
        ]
        
        for path_str, size_mb in duplicates:
            archive_path = self.pictures_dir / path_str
            if archive_path.exists():
                self.operations.append({
                    'action': 'DELETE_ARCHIVE',
                    'tool': 'Archive',
                    'ratio': 'N/A',
                    'source': archive_path,
                    'target': None,
                    'size_mb': size_mb,
                    'dimensions': 'N/A'
                })
                self.stats['archives_deleted'] += 1
                self.stats['space_saved_mb'] += size_mb
                print(f"  {path_str} ({size_mb} MB)")
        
        print()

    def execute_operations(self):
        """Execute operations"""
        self.print_header("⚡ EXECUTING")
        
        print(f"Mode: {Colors.YELLOW}{'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}")
        print(f"Operations: {len(self.operations):,}\n")
        
        for i, op in enumerate(self.operations, 1):
            if i % 500 == 0:
                print(f"Progress: {i:,}/{len(self.operations):,}", end='\r')
            
            if not self.dry_run:
                try:
                    if op['action'] == 'COPY_BEST':
                        op['target'].parent.mkdir(parents=True, exist_ok=True)
                        if not op['target'].exists():
                            shutil.copy2(op['source'], op['target'])
                    elif op['action'] == 'DELETE_ARCHIVE':
                        op['source'].unlink()
                    op['status'] = 'OK'
                except Exception as e:
                    op['status'] = str(e)
            else:
                op['status'] = 'DRY_RUN'
        
        print(f"{Colors.GREEN}✅ Complete{Colors.END}\n")

    def save_log(self):
        """Save log"""
        with open(self.log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Action', 'Tool', 'Ratio', 'Source', 'Target', 'Size_MB', 'Dimensions', 'Status'])
            for op in self.operations:
                writer.writerow([
                    op['action'], op['tool'], op['ratio'],
                    str(op['source']), str(op.get('target', '')),
                    f"{op['size_mb']:.2f}", op.get('dimensions', ''),
                    op.get('status', 'PENDING')
                ])
        print(f"{Colors.GREEN}✅ Log: {self.log_file}{Colors.END}\n")

    def run(self):
        """Run consolidation"""
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔════════════════════════════════════════════════════════════════════════╗")
        print("║         📸 SMART AI CONSOLIDATION 📸                                   ║")
        print("║  Scan → Deduplicate → Organize → Clean → Execute                      ║")
        print("╚════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")
        
        self.create_consolidation_plan()
        self.add_archive_deletions()
        self.execute_operations()
        self.save_log()
        
        # Summary
        self.print_header("✅ COMPLETE", Colors.GREEN)
        print(f"  Total images scanned: {Colors.CYAN}{self.stats['total_images']:,}{Colors.END}")
        print(f"  Duplicates removed: {Colors.CYAN}{self.stats['duplicates_found']:,}{Colors.END}")
        print(f"  Variations merged: {Colors.CYAN}{self.stats['variations_found']:,}{Colors.END}")
        print(f"  Images kept: {Colors.GREEN}{self.stats['images_kept']:,}{Colors.END}")
        print(f"  Archives deleted: {Colors.CYAN}{self.stats['archives_deleted']}{Colors.END}")
        print(f"  Space saved: {Colors.GREEN}{self.stats['space_saved_mb']:.2f} MB{Colors.END}\n")
        
        print(f"{Colors.BOLD}Structure:{Colors.END}")
        print("  ~/Pictures/AI-Images/")
        print("    ├── Ideogram/  {1-1, 9-16, 16-9}")
        print("    ├── DaLLe/     {1-1, 9-16, 16-9}")
        print("    └── [others]/\n")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}⚠️  DRY RUN - use --live to execute{Colors.END}\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Smart AI Consolidation")
    parser.add_argument("--live", action="store_true", help="Execute (default: dry-run)")
    args = parser.parse_args()
    
    consolidator = SmartAIConsolidation(dry_run=not args.live)
    consolidator.run()


if __name__ == "__main__":
    main()
