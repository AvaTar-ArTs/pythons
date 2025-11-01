#!/usr/bin/env python3
"""
Final Root Directory Organizer

Organizes all remaining loose files in root directory into proper structure.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import re

class FinalRootOrganizer:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Target directories
        self.structure = {
            'REPORTS': self.target_dir / '_reports',
            'DATA': self.target_dir / '_data',
            'BACKUPS': self.target_dir / '_backups',
            'SCRIPTS': self.target_dir / '_scripts',
            'DOCS': self.target_dir / '_docs',
            'TEMP': self.target_dir / '_temp',
            'MEDIA': self.target_dir / '_media'
        }
        
        self.stats = {
            'files_moved': 0,
            'folders_merged': 0,
            'errors': 0
        }
    
    def categorize_file(self, file_path: Path) -> str:
        """Determine where a file should go."""
        name = file_path.name.lower()
        suffix = file_path.suffix.lower()
        
        # Reports (MD files)
        if suffix == '.md' and any(x in name for x in ['report', 'summary', 'analysis', 'complete', 'plan']):
            return 'REPORTS'
        
        # Data files
        if suffix in ['.csv', '.json']:
            return 'DATA'
        
        # Backups
        if any(x in name for x in ['.bak', '.backup', 'backup_', 'undo_']):
            return 'BACKUPS'
        
        # Scripts
        if suffix in ['.sh']:
            return 'SCRIPTS'
        
        # Documentation
        if suffix in ['.md', '.txt', '.html'] and 'report' not in name:
            return 'DOCS'
        
        # Media
        if suffix in ['.png', '.jpg', '.jpeg', '.gif', '.zip']:
            return 'MEDIA'
        
        # Temp/miscellaneous
        if any(x in name for x in ['test', 'temp', 'tmp', 'unnamed']):
            return 'TEMP'
        
        return None  # Keep in root if important
    
    def should_keep_in_root(self, file_name: str) -> bool:
        """Determine if file should stay in root."""
        keep_patterns = [
            'README.md',
            'requirements.txt',
            'setup.py',
            'main.py',
            'config.json',
            '.gitignore'
        ]
        
        return any(pattern.lower() in file_name.lower() for pattern in keep_patterns)
    
    def create_structure(self):
        """Create the target directory structure."""
        print("\n📁 Creating organization structure...\n")
        
        for name, path in self.structure.items():
            path.mkdir(exist_ok=True)
            print(f"✅ Created: {path.name}/")
    
    def organize_files(self, dry_run=True):
        """Organize all loose files in root."""
        print(f"\n📊 Organizing root directory files...\n")
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}\n")
        
        # Get all files in root
        root_files = [f for f in self.target_dir.iterdir() if f.is_file()]
        
        moved_count = {'REPORTS': 0, 'DATA': 0, 'BACKUPS': 0, 'SCRIPTS': 0, 'DOCS': 0, 'TEMP': 0, 'MEDIA': 0}
        
        for file_path in sorted(root_files):
            # Skip important files
            if self.should_keep_in_root(file_path.name):
                continue
            
            # Categorize
            category = self.categorize_file(file_path)
            
            if category:
                target_dir = self.structure[category]
                target_path = target_dir / file_path.name
                
                # Handle duplicates
                counter = 1
                original_target = target_path
                while target_path.exists():
                    stem = original_target.stem
                    suffix = original_target.suffix
                    target_path = target_dir / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                if not dry_run:
                    try:
                        shutil.move(str(file_path), str(target_path))
                        moved_count[category] += 1
                        self.stats['files_moved'] += 1
                    except Exception as e:
                        print(f"❌ Error moving {file_path.name}: {e}")
                        self.stats['errors'] += 1
                else:
                    moved_count[category] += 1
                    if moved_count[category] <= 5:
                        print(f"  {category}: {file_path.name}")
        
        print(f"\n📊 Files to move by category:")
        for category, count in moved_count.items():
            if count > 0:
                print(f"  {category}: {count} files")
        
        return moved_count
    
    def merge_duplicate_folders(self, dry_run=True):
        """Merge duplicate category folders."""
        print(f"\n🔄 Checking for duplicate folders...\n")
        
        # Check for duplicates like 04_web_scraping and 04-web-scraping
        folders = [f for f in self.target_dir.iterdir() if f.is_dir()]
        
        # Find pairs
        duplicates = []
        for folder in folders:
            name_dash = folder.name.replace('_', '-')
            name_under = folder.name.replace('-', '_')
            
            for other in folders:
                if folder != other and (other.name == name_dash or other.name == name_under):
                    duplicates.append((folder, other))
        
        if duplicates:
            print(f"Found {len(duplicates)} duplicate pairs\n")
            
            for src, dst in duplicates:
                if src.exists() and dst.exists():
                    print(f"  Merging: {src.name} → {dst.name}")
                    
                    if not dry_run:
                        try:
                            # Move contents
                            for item in src.iterdir():
                                target = dst / item.name
                                if not target.exists():
                                    shutil.move(str(item), str(target))
                            
                            # Remove empty directory
                            if not list(src.iterdir()):
                                src.rmdir()
                            
                            self.stats['folders_merged'] += 1
                        except Exception as e:
                            print(f"❌ Error: {e}")
                            self.stats['errors'] += 1
        else:
            print("No duplicate folders found")
    
    def generate_final_report(self, moved_count, dry_run):
        """Generate final organization report."""
        report_path = self.target_dir / f"FINAL_ROOT_ORGANIZATION_{self.timestamp}.md"
        
        with open(report_path, 'w') as f:
            f.write("# 📁 Final Root Directory Organization\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mode:** {'DRY RUN' if dry_run else 'LIVE'}\n\n")
            
            f.write("## Statistics\n\n")
            f.write(f"- **Files Moved:** {self.stats['files_moved']}\n")
            f.write(f"- **Folders Merged:** {self.stats['folders_merged']}\n")
            f.write(f"- **Errors:** {self.stats['errors']}\n\n")
            
            f.write("## Files Organized by Category\n\n")
            for category, count in sorted(moved_count.items()):
                if count > 0:
                    f.write(f"- **{category}:** {count} files\n")
            
            f.write("\n## Final Structure\n\n")
            f.write("```\n")
            f.write("/Users/steven/Documents/python/\n")
            f.write("├── 01-core-tools/\n")
            f.write("├── 02-youtube-automation/\n")
            f.write("├── 03-ai-creative-tools/\n")
            f.write("├── 04-web-scraping/\n")
            f.write("├── 05-social-media/\n")
            f.write("├── 06-media-processing/\n")
            f.write("├── 07-utilities/\n")
            f.write("├── 08-analysis-tools/\n")
            f.write("├── 09-documentation/\n")
            f.write("├── 10-archived-projects/\n")
            f.write("├── scripts/ (14 production tools)\n")
            f.write("├── _reports/ (all analysis reports)\n")
            f.write("├── _data/ (CSV & JSON files)\n")
            f.write("├── _backups/ (backup files)\n")
            f.write("├── _scripts/ (shell scripts)\n")
            f.write("├── _docs/ (documentation)\n")
            f.write("├── _media/ (images, zips)\n")
            f.write("├── _ARCHIVED_BACKUPS_*/\n")
            f.write("└── [Important root files only]\n")
            f.write("```\n")
        
        print(f"\n✅ Report: {report_path}")
    
    def run(self, dry_run=True):
        """Run complete root organization."""
        print(f"\n{'='*80}")
        print("📁 FINAL ROOT DIRECTORY ORGANIZER")
        print(f"{'='*80}\n")
        
        # Step 1: Create structure
        self.create_structure()
        
        # Step 2: Merge duplicate folders
        self.merge_duplicate_folders(dry_run)
        
        # Step 3: Organize files
        moved_count = self.organize_files(dry_run)
        
        # Step 4: Generate report
        self.generate_final_report(moved_count, dry_run)
        
        print(f"\n{'='*80}")
        print("✅ ROOT ORGANIZATION COMPLETE!")
        print(f"{'='*80}\n")
        print(f"Files Moved: {self.stats['files_moved']}")
        print(f"Folders Merged: {self.stats['folders_merged']}")
        if self.stats['errors'] > 0:
            print(f"⚠️  Errors: {self.stats['errors']}")
        print()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Final Root Organizer')
    parser.add_argument('--target', default='.', help='Target directory')
    parser.add_argument('--live', action='store_true', help='Execute moves')
    
    args = parser.parse_args()
    
    organizer = FinalRootOrganizer(args.target)
    organizer.run(dry_run=not args.live)

if __name__ == "__main__":
    main()

