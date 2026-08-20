#!/usr/bin/env python3
"""
Etsy Design Collection Organizer
Organizes the massive Etsy design collection in ~/Pictures/etsy/
"""

import hashlib
import json
import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path


class EtsyOrganizer:
    def __init__(self, etsy_dir=None):
        self.etsy_dir = Path(etsy_dir or os.path.expanduser("~/Pictures/etsy"))
        self.backup_dir = self.etsy_dir / "00_archives" / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Create organized directory structure
        self.categories = {
            '00_production': 'Production-ready designs',
            '01_ideogram_designs': 'Ideogram AI generated designs',
            '02_zip_archives': 'ZIP file archives',
            '03_t_shirt_designs': 'T-shirt and apparel designs',
            '04_halloween_designs': 'Halloween themed designs',
            '05_raccoon_designs': 'Raccoon themed designs',
            '06_funny_quotes': 'Funny quotes and text designs',
            '07_animal_designs': 'Animal themed designs',
            '08_holiday_designs': 'Holiday and seasonal designs',
            '09_mockups_templates': 'Mockups and design templates',
            '10_ai_generated': 'AI generated images and designs',
            '11_duplicates': 'Duplicate files',
            '12_archived': 'Archived and old designs'
        }
        
        # Create all category directories
        for category in self.categories.keys():
            (self.etsy_dir / category).mkdir(exist_ok=True)
    
    def get_file_hash(self, file_path):
        """Get MD5 hash of file for duplicate detection"""
        try:
            with open(file_path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def analyze_filename(self, file_path):
        """Analyze filename to determine category"""
        name = file_path.name.lower()
        
        # Ideogram designs
        if 'ideo' in name or 'ideogram' in name:
            return '01_ideogram_designs'
        
        # T-shirt designs
        if any(keyword in name for keyword in ['tshirt', 't-shirt', 'shirt', 'apparel']):
            return '03_t_shirt_designs'
        
        # Halloween designs
        if any(keyword in name for keyword in ['halloween', 'spooky', 'skeleton', 'ghost', 'witch']):
            return '04_halloween_designs'
        
        # Raccoon designs
        if any(keyword in name for keyword in ['raccoon', 'racoon', 'trash', 'panda']):
            return '05_raccoon_designs'
        
        # Funny quotes
        if any(keyword in name for keyword in ['funny', 'quote', 'sarcastic', 'pun', 'joke']):
            return '06_funny_quotes'
        
        # Animal designs
        if any(keyword in name for keyword in ['cat', 'dog', 'animal', 'pet', 'cute']):
            return '07_animal_designs'
        
        # Holiday designs
        if any(keyword in name for keyword in ['christmas', 'valentine', 'easter', 'thanksgiving', 'holiday']):
            return '08_holiday_designs'
        
        # Mockups and templates
        if any(keyword in name for keyword in ['mockup', 'template', 'psd', 'ai', 'svg']):
            return '09_mockups_templates'
        
        # AI generated
        if any(keyword in name for keyword in ['dalle', 'midjourney', 'stable', 'ai-generated', 'generated']):
            return '10_ai_generated'
        
        # Duplicates (version numbers, copies)
        if any(pattern in name for pattern in ['_1', '_2', '_3', 'copy', 'duplicate', 'backup']):
            return '11_duplicates'
        
        return None
    
    def analyze_zip_content(self, zip_path):
        """Analyze ZIP file content to determine category"""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                file_list = zip_file.namelist()
                
                # Count different file types
                png_count = len([f for f in file_list if f.lower().endswith('.png')])
                jpg_count = len([f for f in file_list if f.lower().endswith(('.jpg', '.jpeg'))])
                svg_count = len([f for f in file_list if f.lower().endswith('.svg')])
                psd_count = len([f for f in file_list if f.lower().endswith('.psd')])
                
                # Analyze filenames in ZIP
                all_names = ' '.join(file_list).lower()
                
                if 'halloween' in all_names or 'skeleton' in all_names:
                    return '04_halloween_designs'
                elif 'raccoon' in all_names or 'racoon' in all_names:
                    return '05_raccoon_designs'
                elif 'funny' in all_names or 'quote' in all_names:
                    return '06_funny_quotes'
                elif 'tshirt' in all_names or 'shirt' in all_names:
                    return '03_t_shirt_designs'
                elif 'animal' in all_names or 'cat' in all_names or 'dog' in all_names:
                    return '07_animal_designs'
                elif 'holiday' in all_names or 'christmas' in all_names:
                    return '08_holiday_designs'
                elif svg_count > png_count and svg_count > jpg_count:
                    return '09_mockups_templates'
                else:
                    return '02_zip_archives'
                    
        except:
            return '02_zip_archives'
    
    def is_duplicate(self, file_path, existing_files):
        """Check if file is a duplicate"""
        file_hash = self.get_file_hash(file_path)
        if not file_hash:
            return False
        
        for existing_file in existing_files:
            if self.get_file_hash(existing_file) == file_hash:
                return existing_file
        return False
    
    def organize_files(self):
        """Organize all files in the Etsy directory"""
        print("🎨 Organizing Etsy Design Collection")
        print("=" * 50)
        
        # Get all files (excluding already organized directories)
        all_files = []
        organized_dirs = set(self.categories.keys())
        
        for root, dirs, files in os.walk(self.etsy_dir):
            # Skip already organized directories
            if any(part in organized_dirs for part in Path(root).parts):
                continue
            
            for file in files:
                file_path = Path(root) / file
                all_files.append(file_path)
        
        print(f"📊 Found {len(all_files)} files to organize")
        
        # Statistics
        stats = {
            'total_files': len(all_files),
            'moved_files': 0,
            'duplicates_found': 0,
            'errors': 0,
            'categories': {cat: 0 for cat in self.categories.keys()}
        }
        
        # Track files by hash to detect duplicates
        file_hashes = {}
        duplicates = []
        
        for file_path in all_files:
            try:
                # Check for duplicates first
                file_hash = self.get_file_hash(file_path)
                if file_hash and file_hash in file_hashes:
                    # This is a duplicate
                    duplicates.append((file_path, file_hashes[file_hash]))
                    stats['duplicates_found'] += 1
                    continue
                
                if file_hash:
                    file_hashes[file_hash] = file_path
                
                # Categorize the file
                category = self.analyze_filename(file_path)
                
                # Special handling for ZIP files
                if file_path.suffix.lower() == '.zip' and not category:
                    category = self.analyze_zip_content(file_path)
                
                # Default category if none found
                if not category:
                    category = '12_archived'
                
                # Move file to appropriate category
                dest_dir = self.etsy_dir / category
                dest_file = dest_dir / file_path.name
                
                # Handle name conflicts
                counter = 1
                original_name = file_path.name
                while dest_file.exists():
                    name_parts = original_name.rsplit('.', 1)
                    if len(name_parts) == 2:
                        new_name = f"{name_parts[0]}_{counter}.{name_parts[1]}"
                    else:
                        new_name = f"{original_name}_{counter}"
                    dest_file = dest_dir / new_name
                    counter += 1
                
                # Move the file
                shutil.move(str(file_path), str(dest_file))
                relative_path = file_path.relative_to(self.etsy_dir)
                print(f"  ✅ Moved {relative_path} to {category}")
                stats['moved_files'] += 1
                stats['categories'][category] += 1
                
            except Exception as e:
                print(f"  ❌ Error processing {file_path.name}: {e}")
                stats['errors'] += 1
        
        # Handle duplicates
        if duplicates:
            print(f"\n🔄 Processing {len(duplicates)} duplicate files...")
            for duplicate_file, original_file in duplicates:
                try:
                    # Move duplicate to duplicates folder
                    dest_file = self.etsy_dir / '11_duplicates' / f"duplicate_{duplicate_file.name}"
                    shutil.move(str(duplicate_file), str(dest_file))
                    print(f"  📦 Archived duplicate: {duplicate_file.name}")
                except Exception as e:
                    print(f"  ❌ Error archiving duplicate {duplicate_file.name}: {e}")
        
        return stats
    
    def cleanup_empty_directories(self):
        """Remove empty directories after organizing files"""
        print("\n🧹 Cleaning up empty directories...")
        
        removed_dirs = 0
        for root, dirs, files in os.walk(self.etsy_dir, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                # Skip organized category directories
                if dir_name in self.categories:
                    continue
                
                try:
                    # Check if directory is empty
                    if not any(dir_path.iterdir()):
                        dir_path.rmdir()
                        relative_path = dir_path.relative_to(self.etsy_dir)
                        print(f"  🗑️  Removed empty directory: {relative_path}")
                        removed_dirs += 1
                except OSError:
                    # Directory not empty or permission error
                    pass
        
        print(f"📊 Removed {removed_dirs} empty directories")
        return removed_dirs
    
    def create_readme_files(self):
        """Create README files for each category"""
        print("\n📝 Creating README files for each category...")
        
        for category, description in self.categories.items():
            readme_path = self.etsy_dir / category / "README.md"
            
            # Count files in category
            file_count = len(list((self.etsy_dir / category).glob("*")))
            
            readme_content = f"""# {description}

## Overview
This directory contains {file_count} files related to {description.lower()}.

## Categories
- **Production Designs**: Ready-to-use, high-quality designs
- **Ideogram Designs**: AI-generated designs from Ideogram
- **ZIP Archives**: Compressed design bundles
- **T-shirt Designs**: Apparel and clothing designs
- **Halloween Designs**: Spooky and Halloween-themed designs
- **Raccoon Designs**: Raccoon and trash panda themed designs
- **Funny Quotes**: Humorous text and quote designs
- **Animal Designs**: Cute animal themed designs
- **Holiday Designs**: Seasonal and holiday themed designs
- **Mockups & Templates**: Design templates and mockups
- **AI Generated**: AI-generated images and designs
- **Duplicates**: Duplicate files found during organization
- **Archived**: Old and archived designs

## File Organization
Files are organized by theme and type. Use the naming convention:
- `design_name.png` - Main design file
- `design_name_v2.png` - Updated version
- `design_name_mockup.psd` - Mockup template

## Usage
Most design files can be opened with:
- **PNG/JPG**: Any image viewer or editor
- **PSD**: Adobe Photoshop
- **SVG**: Vector graphics editor
- **ZIP**: Extract to access multiple files

## Design Guidelines
- Keep original high-resolution files
- Maintain consistent naming conventions
- Use appropriate file formats for different purposes
- Archive old versions instead of deleting
"""
            
            with open(readme_path, 'w') as f:
                f.write(readme_content)
            
            print(f"  ✅ Created README for {category}")
    
    def generate_organization_report(self, stats):
        """Generate a detailed organization report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_files_processed': stats['total_files'],
            'files_moved': stats['moved_files'],
            'duplicates_found': stats['duplicates_found'],
            'errors': stats['errors'],
            'category_distribution': stats['categories'],
            'space_saved_estimate': f"{stats['duplicates_found'] * 0.1:.1f}GB (estimated)"
        }
        
        report_file = self.etsy_dir / "00_archives" / f"etsy_organization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📋 Organization report saved to: {report_file}")
        return report
    
    def run_organization(self):
        """Run the complete organization process"""
        print("🚀 Starting Etsy Design Collection Organization")
        print("=" * 50)
        
        # Show current structure
        print(f"📁 Current directory: {self.etsy_dir}")
        print(f"📊 Total size: {self.get_directory_size()}")
        
        # Organize files
        stats = self.organize_files()
        
        # Create README files
        self.create_readme_files()
        
        # Clean up empty directories
        empty_dirs_removed = self.cleanup_empty_directories()
        
        # Generate report
        report = self.generate_organization_report(stats)
        report['empty_directories_removed'] = empty_dirs_removed
        
        print("\n" + "=" * 50)
        print("🎉 Organization Complete!")
        print(f"📊 Total files processed: {report['total_files_processed']}")
        print(f"📁 Files moved: {report['files_moved']}")
        print(f"🔄 Duplicates found: {report['duplicates_found']}")
        print(f"❌ Errors: {report['errors']}")
        print(f"🗑️  Empty directories removed: {report.get('empty_directories_removed', 0)}")
        print(f"💾 Estimated space saved: {report['space_saved_estimate']}")
        
        print("\n📂 Category Distribution:")
        for category, count in report['category_distribution'].items():
            if count > 0:
                print(f"  {category}: {count} files")
        
        return report
    
    def get_directory_size(self):
        """Get directory size in human readable format"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(self.etsy_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except OSError:
                    pass
        
        # Convert to human readable format
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if total_size < 1024.0:
                return f"{total_size:.1f} {unit}"
            total_size /= 1024.0
        return f"{total_size:.1f} PB"

if __name__ == "__main__":
    organizer = EtsyOrganizer()
    organizer.run_organization()