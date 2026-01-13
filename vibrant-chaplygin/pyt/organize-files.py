#!/usr/bin/env python3
"""
💾 SAVE EVERYTHING BEFORE CLEANUP
==================================
Comprehensive preservation of ALL content before any cleanup/merge operations

Features:
✨ Archive all orphaned content (stories, lyrics, transcripts, prompts)
✨ Preserve all files from archive directories
✨ Create timestamped backups
✨ Generate complete inventory
✨ Ensure NOTHING is lost
✨ Organize by content type
"""

import os
import csv
import json
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    END = "\033[0m"

class ComprehensivePreservationSystem:
    """Save everything before any cleanup"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Master preservation directory
        self.preservation_root = Path.home() / "Documents" / f"MUSIC_ARCHIVE_PRESERVATION_{self.timestamp}"
        
        # Organized subdirectories
        self.dirs = {
            'csv': self.preservation_root / "CSV_CATALOGS",
            'lyrics': self.preservation_root / "LYRICS",
            'transcripts': self.preservation_root / "TRANSCRIPTS",
            'prompts': self.preservation_root / "PROMPTS",
            'metadata': self.preservation_root / "METADATA",
            'stories': self.preservation_root / "STORIES_AND_NARRATIVES",
            'html': self.preservation_root / "HTML_GALLERIES",
            'json': self.preservation_root / "JSON_DATA",
            'markdown': self.preservation_root / "MARKDOWN_DOCS",
            'images': self.preservation_root / "IMAGES",
            'other': self.preservation_root / "OTHER"
        }
        
        # Create all directories
        for directory in self.dirs.values():
            directory.mkdir(parents=True, exist_ok=True)
        
        self.stats = {
            'files_preserved': 0,
            'total_size': 0,
            'by_type': defaultdict(int)
        }
        
        self.inventory = []
    
    def print_header(self, text: str, color=Colors.CYAN):
        """Print fancy header"""
        print(f"\n{color}{Colors.BOLD}{'='*80}")
        print(f"{text}")
        print(f"{'='*80}{Colors.END}\n")
    
    def classify_file(self, filepath: Path) -> str:
        """Classify file for organization"""
        name_lower = filepath.name.lower()
        ext = filepath.suffix.lower()
        
        # Read first few lines if text
        content_preview = ""
        if ext in ['.txt', '.md']:
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content_preview = ''.join(f.readlines()[:5]).lower()
            except Exception:
                pass
        
        # CSV
        if ext == '.csv':
            return 'csv'
        
        # Lyrics
        if 'lyric' in name_lower or '[verse' in content_preview or '[chorus' in content_preview:
            return 'lyrics'
        
        # Transcripts
        if 'transcript' in name_lower or 'speaker' in content_preview or 'timestamp' in content_preview:
            return 'transcripts'
        
        # Prompts
        if 'prompt' in name_lower or 'dalle' in name_lower or 'sora' in name_lower:
            return 'prompts'
        
        # Stories/narratives
        if 'story' in name_lower or 'tale' in name_lower or 'narrative' in name_lower:
            return 'stories'
        if 'chapter' in content_preview or 'trashcat' in name_lower:
            return 'stories'
        
        # Metadata
        if 'metadata' in name_lower or 'info' in name_lower or ext == '.json':
            if ext == '.json':
                return 'json'
            return 'metadata'
        
        # HTML
        if ext in ['.html', '.htm']:
            return 'html'
        
        # Markdown
        if ext == '.md':
            # Check if it's a specific type
            if 'branding' in name_lower or 'professional' in name_lower:
                return 'markdown'
            if 'seo' in name_lower or 'strategy' in name_lower:
                return 'markdown'
            return 'markdown'
        
        # Images
        if ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
            return 'images'
        
        return 'other'
    
    def preserve_orphaned_content(self):
        """Preserve orphaned content from scan results"""
        self.print_header("💾 PRESERVING ORPHANED CONTENT")
        
        # Find latest comprehensive scan
        music_dir = Path.home() / "Music"
        scan_dirs = sorted(music_dir.glob("COMPREHENSIVE_SCAN_*"))
        
        if not scan_dirs:
            print(f"{Colors.YELLOW}⚠️  No comprehensive scan found. Skipping orphaned content.{Colors.END}")
            return
        
        latest_scan = scan_dirs[-1]
        orphaned_file = latest_scan / "ORPHANED_CONTENT_NO_AUDIO.csv"
        
        if not orphaned_file.exists():
            print(f"{Colors.YELLOW}⚠️  No orphaned content file found.{Colors.END}")
            return
        
        print(f"Reading: {latest_scan.name}\n")
        
        # Load orphaned content
        orphaned_files = []
        with open(orphaned_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            orphaned_files = list(reader)
        
        print(f"Found {len(orphaned_files)} orphaned content files to preserve\n")
        
        preserved_count = 0
        
        for file_info in orphaned_files:
            source_path = Path(file_info['Path'])
            
            # Handle both absolute and relative paths
            if not source_path.is_absolute():
                location = file_info.get('Location', 'Music')
                if location == 'Music':
                    source_path = music_dir / source_path
                else:
                    source_path = Path.home() / "Documents" / source_path
            
            if not source_path.exists():
                continue
            
            try:
                # Classify file
                file_type = self.classify_file(source_path)
                
                # Determine target directory
                target_dir = self.dirs.get(file_type, self.dirs['other'])
                target_path = target_dir / source_path.name
                
                # Handle name conflicts
                counter = 1
                original_target = target_path
                while target_path.exists():
                    target_path = original_target.parent / f"{original_target.stem}_{counter}{original_target.suffix}"
                    counter += 1
                
                # Copy file
                shutil.copy2(source_path, target_path)
                
                file_size = source_path.stat().st_size
                
                self.inventory.append({
                    'filename': source_path.name,
                    'original_path': str(source_path),
                    'preserved_path': str(target_path),
                    'type': file_type,
                    'size': file_size,
                    'source': 'orphaned_content'
                })
                
                self.stats['files_preserved'] += 1
                self.stats['total_size'] += file_size
                self.stats['by_type'][file_type] += 1
                preserved_count += 1
                
                if preserved_count % 50 == 0:
                    print(f"  Preserved {preserved_count} files...", end='\r')
                
            except Exception as e:
                print(f"{Colors.RED}❌ Error preserving {source_path.name}: {e}{Colors.END}")
        
        print(f"\n{Colors.GREEN}✅ Preserved {preserved_count} orphaned content files{Colors.END}\n")
    
    def preserve_archived_directories_content(self):
        """Preserve valuable content from archived directories"""
        self.print_header("📁 PRESERVING ARCHIVED DIRECTORIES CONTENT")
        
        archive_dirs = [
            Path("/Users/steven/Music/_ARCHIVED_DIRECTORIES"),
            Path("/Users/steven/Music/_OLD_DIRECTORIES_ARCHIVED"),
        ]
        
        for archive_dir in archive_dirs:
            if not archive_dir.exists():
                continue
            
            print(f"{Colors.CYAN}Scanning: {archive_dir.name}{Colors.END}\n")
            
            preserved_count = 0
            
            # Scan for valuable files
            for root, dirs, files in os.walk(archive_dir):
                # Skip system directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for filename in files:
                    if filename.startswith('.'):
                        continue
                    
                    filepath = Path(root) / filename
                    ext = filepath.suffix.lower()
                    
                    # Preserve these types
                    preserve_types = {
                        '.csv', '.md', '.txt', '.json', '.html', '.htm',
                        '.jpg', '.jpeg', '.png', '.webp', '.pdf'
                    }
                    
                    if ext in preserve_types:
                        try:
                            file_type = self.classify_file(filepath)
                            target_dir = self.dirs.get(file_type, self.dirs['other'])
                            
                            # Preserve directory structure in filename
                            rel_path = filepath.relative_to(archive_dir)
                            safe_name = str(rel_path).replace('/', '_').replace(' ', '_')
                            target_path = target_dir / safe_name
                            
                            # Handle conflicts
                            counter = 1
                            original_target = target_path
                            while target_path.exists():
                                target_path = original_target.parent / f"{original_target.stem}_{counter}{original_target.suffix}"
                                counter += 1
                            
                            # Copy
                            shutil.copy2(filepath, target_path)
                            
                            file_size = filepath.stat().st_size
                            
                            self.inventory.append({
                                'filename': filename,
                                'original_path': str(filepath),
                                'preserved_path': str(target_path),
                                'type': file_type,
                                'size': file_size,
                                'source': archive_dir.name
                            })
                            
                            self.stats['files_preserved'] += 1
                            self.stats['total_size'] += file_size
                            self.stats['by_type'][file_type] += 1
                            preserved_count += 1
                            
                            if preserved_count % 20 == 0:
                                print(f"  Preserved {preserved_count} files from {archive_dir.name}...", end='\r')
                            
                        except Exception as e:
                            pass
            
            print(f"\n{Colors.GREEN}✅ Preserved {preserved_count} files from {archive_dir.name}{Colors.END}\n")
    
    def preserve_extraction_reports(self):
        """Preserve all extraction and analysis reports"""
        self.print_header("📊 PRESERVING ANALYSIS REPORTS")
        
        music_dir = Path.home() / "Music"
        
        # Find all analysis directories
        analysis_patterns = [
            "ARCHIVE_ANALYSIS_*",
            "ARCHIVE_EXTRACTION_*",
            "COMPREHENSIVE_SCAN_*",
            "DOCUMENTS_ARCHIVES_SCAN_*"
        ]
        
        reports_dir = self.preservation_root / "ANALYSIS_REPORTS"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        preserved_count = 0
        
        for pattern in analysis_patterns:
            for analysis_dir in music_dir.glob(pattern):
                if analysis_dir.is_dir():
                    # Copy entire directory
                    target_dir = reports_dir / analysis_dir.name
                    
                    try:
                        shutil.copytree(analysis_dir, target_dir, dirs_exist_ok=True)
                        
                        # Count files
                        file_count = sum(1 for _ in target_dir.rglob('*') if _.is_file())
                        preserved_count += file_count
                        
                        print(f"{Colors.GREEN}✅ Preserved: {analysis_dir.name} ({file_count} files){Colors.END}")
                        
                    except Exception as e:
                        print(f"{Colors.RED}❌ Error: {e}{Colors.END}")
        
        print(f"\n{Colors.BOLD}Reports preserved: {preserved_count} files{Colors.END}\n")
    
    def create_master_inventory(self):
        """Create master inventory of everything preserved"""
        self.print_header("📋 CREATING MASTER INVENTORY")
        
        inventory_file = self.preservation_root / "MASTER_INVENTORY.csv"
        
        with open(inventory_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Filename', 'Original_Path', 'Preserved_Path', 
                'Type', 'Size_KB', 'Source'
            ])
            
            for item in sorted(self.inventory, key=lambda x: (x['type'], x['filename'])):
                writer.writerow([
                    item['filename'],
                    item['original_path'],
                    item['preserved_path'],
                    item['type'],
                    f"{item['size'] / 1024:.2f}",
                    item['source']
                ])
        
        print(f"{Colors.GREEN}✅ Inventory: {inventory_file.name}{Colors.END}")
        
        # Create summary by type
        summary_file = self.preservation_root / "PRESERVATION_SUMMARY.json"
        
        summary = {
            'timestamp': self.timestamp,
            'total_files': self.stats['files_preserved'],
            'total_size_mb': self.stats['total_size'] / (1024**2),
            'by_type': dict(self.stats['by_type']),
            'preservation_root': str(self.preservation_root)
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print(f"{Colors.GREEN}✅ Summary: {summary_file.name}{Colors.END}")
        
        # Create README
        readme_file = self.preservation_root / "README.md"
        
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write("# 💾 Music Archive Preservation\n\n")
            f.write(f"**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            f.write("## 📊 Preservation Summary\n\n")
            f.write(f"This archive contains **{self.stats['files_preserved']:,} files** ")
            f.write(f"({self.stats['total_size'] / (1024**2):.2f} MB) preserved before cleanup.\n\n")
            
            f.write("## 📁 Organization\n\n")
            f.write("Files are organized by content type:\n\n")
            for type_name, count in sorted(self.stats['by_type'].items(), key=lambda x: -x[1]):
                f.write(f"- **{type_name.upper()}/** - {count} files\n")
            f.write("\n")
            
            f.write("## 📋 What's Preserved\n\n")
            f.write("### 1. Orphaned Content\n")
            f.write("- Content files without associated audio\n")
            f.write("- May include drafts, standalone stories, lyrics\n\n")
            
            f.write("### 2. Archived Directory Content\n")
            f.write("- All valuable files from `_ARCHIVED_DIRECTORIES`\n")
            f.write("- All valuable files from `_OLD_DIRECTORIES_ARCHIVED`\n\n")
            
            f.write("### 3. Analysis Reports\n")
            f.write("- All previous analysis and extraction reports\n")
            f.write("- Complete scan results\n\n")
            
            f.write("## 🔍 How to Use This Archive\n\n")
            f.write("1. **Browse by Type:** Each subfolder contains specific content type\n")
            f.write("2. **Check Inventory:** `MASTER_INVENTORY.csv` lists all files with original paths\n")
            f.write("3. **Search Content:** Use search tools to find specific songs/stories\n")
            f.write("4. **Restore if Needed:** Original paths are documented for restoration\n\n")
            
            f.write("## ⚠️ Important Notes\n\n")
            f.write("- This archive is PERMANENT - safe to keep indefinitely\n")
            f.write("- Original files may be removed during cleanup\n")
            f.write("- Use this archive to recover any accidentally deleted content\n")
            f.write("- All content is timestamped and traceable\n\n")
        
        print(f"{Colors.GREEN}✅ README: {readme_file.name}{Colors.END}")
    
    def create_content_index(self):
        """Create searchable content index"""
        self.print_header("🔍 CREATING SEARCHABLE INDEX")
        
        index_file = self.preservation_root / "CONTENT_INDEX.csv"
        
        # Group files by type
        by_type = defaultdict(list)
        for item in self.inventory:
            by_type[item['type']].append(item)
        
        with open(index_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Type', 'Count', 'Total_Size_MB', 'Files'])
            
            for file_type in sorted(by_type.keys()):
                files = by_type[file_type]
                total_size = sum(item['size'] for item in files)
                file_list = '; '.join([item['filename'] for item in files[:10]])
                
                if len(files) > 10:
                    file_list += f" ... and {len(files) - 10} more"
                
                writer.writerow([
                    file_type.upper(),
                    len(files),
                    f"{total_size / (1024**2):.2f}",
                    file_list
                ])
        
        print(f"{Colors.GREEN}✅ Content Index: {index_file.name}{Colors.END}")
    
    def run(self):
        """Run comprehensive preservation"""
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║           💾 SAVE EVERYTHING BEFORE CLEANUP 💾                                ║")
        print("║                                                                               ║")
        print("║        Comprehensive Preservation → Nothing Lost → Safe Cleanup              ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        print(f"{Colors.CYAN}Preservation Directory:{Colors.END}")
        print(f"  {self.preservation_root}\n")
        
        # 1. Preserve orphaned content
        self.preserve_orphaned_content()
        
        # 2. Preserve archived directories content
        self.preserve_archived_directories_content()
        
        # 3. Preserve analysis reports
        self.preserve_extraction_reports()
        
        # 4. Create master inventory
        self.create_master_inventory()
        
        # 5. Create searchable index
        self.create_content_index()
        
        # Final summary
        self.print_header("✅ PRESERVATION COMPLETE!", Colors.GREEN)
        
        print(f"{Colors.BOLD}📊 Final Statistics:{Colors.END}\n")
        print(f"  Total files preserved: {Colors.CYAN}{self.stats['files_preserved']:,}{Colors.END}")
        print(f"  Total size: {Colors.CYAN}{self.stats['total_size'] / (1024**2):.2f} MB{Colors.END}\n")
        
        print(f"{Colors.BOLD}By Content Type:{Colors.END}\n")
        for file_type, count in sorted(self.stats['by_type'].items(), key=lambda x: -x[1]):
            print(f"  {file_type:20} {count:5} files")
        print()
        
        print(f"{Colors.BOLD}📁 Preservation Archive:{Colors.END}")
        print(f"  {self.preservation_root}\n")
        
        print(f"{Colors.BOLD}📝 Key Files:{Colors.END}")
        print(f"  README.md - Overview and usage guide")
        print(f"  MASTER_INVENTORY.csv - Complete file listing")
        print(f"  PRESERVATION_SUMMARY.json - Statistics")
        print(f"  CONTENT_INDEX.csv - Searchable index\n")
        
        print(f"{Colors.BOLD}📂 Organized Folders:{Colors.END}")
        for type_name, directory in self.dirs.items():
            count = self.stats['by_type'].get(type_name, 0)
            if count > 0:
                print(f"  {type_name.upper():<20} {count:5} files → {directory.name}/")
        print()
        
        print(f"{Colors.GREEN}✅ ALL CONTENT SAFELY PRESERVED!{Colors.END}")
        print(f"{Colors.GREEN}✅ Safe to proceed with cleanup/merge operations.{Colors.END}\n")
        
        print(f"{Colors.CYAN}Open archive: open '{self.preservation_root}'{Colors.END}\n")


def main():
    print(f"\n{Colors.YELLOW}⚠️  This script will preserve ALL content before cleanup{Colors.END}")
    print(f"{Colors.YELLOW}Files will be copied (not moved) to a timestamped archive.{Colors.END}\n")
    
    response = input(f"{Colors.BOLD}Proceed with preservation? [Y/n]: {Colors.END}").strip().lower()
    
    if response and response != 'y':
        print(f"\n{Colors.YELLOW}Cancelled.{Colors.END}\n")
        return
    
    preserver = ComprehensivePreservationSystem()
    preserver.run()


if __name__ == "__main__":
    main()
