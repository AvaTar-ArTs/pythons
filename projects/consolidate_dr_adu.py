#!/usr/bin/env python3
"""
Dr_Adu_Gainesville Consolidation Script
Consolidates all Dr_Adu_Gainesville related files into a single organized directory
"""

import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json

class DrAduConsolidator:
    def __init__(self, target_dir="/Users/steven/Documents/Dr_Adu_GainesvillePFS_SEO_Project_CONSOLIDATED"):
        self.target_dir = Path(target_dir)
        self.source_locations = [
            "/Users/steven/Documents/Dr_Adu_GainesvillePFS_SEO_Project",
            "/Users/steven/Downloads/Dr_Adu_GainesvillePFS_SEO_Project",
            "/Users/steven/Library/Mobile Documents/com~apple~CloudDocs/Downloads/Dr_Adu_GainesvillePFS_SEO_Project",
            "/Users/steven/Documents/DrAdu",
            "/Users/steven/csv_outputs",
            "/Users/steven/claude_export_all_2025-11-28-csv",
        ]
        self.file_registry = {}
        self.duplicates = defaultdict(list)
        self.consolidation_log = []
        self.stats = {
            'files_processed': 0,
            'files_moved': 0,
            'duplicates_found': 0,
            'directories_created': 0,
            'errors': 0
        }
        
    def get_file_hash(self, file_path):
        """Calculate MD5 hash of file"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            return None
    
    def get_file_info(self, file_path):
        """Get file metadata"""
        try:
            stat = file_path.stat()
            return {
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'created': stat.st_ctime,
                'path': str(file_path)
            }
        except:
            return None
    
    def find_all_files(self):
        """Find all Dr_Adu/Gainesville related files"""
        print("🔍 Scanning for all Dr_Adu/Gainesville files...")
        all_files = []
        
        # Directories to scan
        directories = [
            "/Users/steven/Documents/Dr_Adu_GainesvillePFS_SEO_Project",
            "/Users/steven/Downloads/Dr_Adu_GainesvillePFS_SEO_Project",
            "/Users/steven/Library/Mobile Documents/com~apple~CloudDocs/Downloads/Dr_Adu_GainesvillePFS_SEO_Project",
            "/Users/steven/Documents/DrAdu",
        ]
        
        # Individual files
        individual_files = [
            "/Users/steven/move_dr_adu.py",
            "/Users/steven/analyze_dr_adu.py",
            "/Users/steven/pythons/DR_ADU_PYTHON_content_aware_analyzer_1.py",
            "/Users/steven/Documents/organized/reports/FINAL_DR_ADU_ORGANIZATION_SUMMARY.md",
        ]
        
        # CSV files
        csv_patterns = [
            "/Users/steven/csv_outputs/*Dr_Adu*.csv",
            "/Users/steven/csv_outputs/*Gainesville*.csv",
            "/Users/steven/claude_export_all_2025-11-28-csv/*Gainesville*.csv",
        ]
        
        # Scan directories
        for directory in directories:
            dir_path = Path(directory)
            if dir_path.exists():
                for file_path in dir_path.rglob('*'):
                    if file_path.is_file():
                        all_files.append(file_path)
        
        # Add individual files
        for file_path in individual_files:
            path = Path(file_path)
            if path.exists():
                all_files.append(path)
        
        # Add CSV files
        import glob
        for pattern in csv_patterns:
            for file_path in glob.glob(pattern):
                all_files.append(Path(file_path))
        
        print(f"   Found {len(all_files)} files")
        return all_files
    
    def determine_best_file(self, file_list):
        """Determine which file to keep from duplicates"""
        if not file_list:
            return None
        
        # Score files: prefer larger, newer files from Documents
        best_file = None
        best_score = -1
        
        for file_path in file_list:
            info = self.get_file_info(file_path)
            if not info:
                continue
            
            score = 0
            path_str = str(file_path)
            
            # Prefer Documents over Downloads/iCloud
            if '/Documents/' in path_str:
                score += 100
            elif '/Downloads/' in path_str:
                score += 50
            elif 'iCloud' in path_str:
                score += 25
            
            # Prefer larger files (more complete)
            score += info['size'] / 1000
            
            # Prefer newer files
            score += info['modified'] / 1000000
            
            # Prefer files not in DrAdu duplicates folder
            if '/DrAdu/' in path_str and 'copy' in file_path.name.lower():
                score -= 50
            
            if score > best_score:
                best_score = score
                best_file = file_path
        
        return best_file
    
    def create_target_structure(self):
        """Create organized directory structure"""
        print("🏗️  Creating consolidated directory structure...")
        
        structure = [
            "01_Project_Files",
            "02_Analysis_Research",
            "03_Content_Development",
            "04_Technical_Implementation",
            "05_Reports_Documentation",
            "06_Tools_Scripts",
            "07_Archive_Backup",
            "08_CSV_Data",
            "09_Duplicates_Archive",
            "10_Website_Hosting",
            "11_Python_Scripts",
            "12_Related_Files"
        ]
        
        for dir_name in structure:
            (self.target_dir / dir_name).mkdir(parents=True, exist_ok=True)
            self.stats['directories_created'] += 1
        
        # Create subdirectories
        (self.target_dir / "02_Analysis_Research" / "01_Content_Analysis").mkdir(exist_ok=True)
        (self.target_dir / "02_Analysis_Research" / "02_SEO_Analysis").mkdir(exist_ok=True)
        (self.target_dir / "05_Reports_Documentation" / "01_Summaries").mkdir(exist_ok=True)
        (self.target_dir / "05_Reports_Documentation" / "02_Comprehensive_Analysis").mkdir(exist_ok=True)
        (self.target_dir / "07_Archive_Backup" / "01_Original_Files").mkdir(exist_ok=True)
        (self.target_dir / "07_Archive_Backup" / "02_Duplicates").mkdir(exist_ok=True)
    
    def get_target_path(self, source_file, file_hash=None):
        """Determine target path for a file"""
        source_str = str(source_file)
        file_name = source_file.name
        
        # Python scripts
        if source_file.suffix == '.py' and ('dr_adu' in file_name.lower() or 'gainesville' in file_name.lower()):
            return self.target_dir / "11_Python_Scripts" / file_name
        
        # CSV files
        if source_file.suffix == '.csv' and ('dr_adu' in file_name.lower() or 'gainesville' in file_name.lower()):
            return self.target_dir / "08_CSV_Data" / file_name
        
        # HTML files
        if source_file.suffix == '.html' and 'gainesville' in file_name.lower():
            return self.target_dir / "10_Website_Hosting" / file_name
        
        # Shell scripts
        if source_file.suffix == '.sh' and 'gainesville' in file_name.lower():
            return self.target_dir / "06_Tools_Scripts" / file_name
        
        # Markdown files - categorize by content
        if source_file.suffix == '.md':
            if 'FINAL_DR_ADU_ORGANIZATION_SUMMARY' in file_name:
                return self.target_dir / "05_Reports_Documentation" / "01_Summaries" / file_name
            elif 'DR_ADU_COMPREHENSIVE_ANALYSIS' in file_name:
                return self.target_dir / "02_Analysis_Research" / "02_SEO_Analysis" / file_name
            elif 'GAINESVILLE_PFS_WEBSITE_ANALYSIS' in file_name:
                return self.target_dir / "02_Analysis_Research" / "01_Content_Analysis" / file_name
            elif 'gainesville' in file_name.lower() or 'dr_adu' in file_name.lower():
                return self.target_dir / "05_Reports_Documentation" / "02_Comprehensive_Analysis" / file_name
        
        # Files from main project structure - preserve structure
        for source_loc in self.source_locations:
            if source_str.startswith(source_loc):
                relative = os.path.relpath(source_str, source_loc)
                rel_path = Path(relative)
                
                # Map to new structure
                if str(rel_path).startswith('02_Analysis_Research/'):
                    return self.target_dir / "02_Analysis_Research" / Path(*rel_path.parts[1:])
                elif str(rel_path).startswith('03_Content_Development/'):
                    return self.target_dir / "03_Content_Development" / Path(*rel_path.parts[1:])
                elif str(rel_path).startswith('04_Technical_Implementation/'):
                    return self.target_dir / "04_Technical_Implementation" / Path(*rel_path.parts[1:])
                elif str(rel_path).startswith('05_Reports_Documentation/'):
                    return self.target_dir / "05_Reports_Documentation" / Path(*rel_path.parts[1:])
                elif str(rel_path).startswith('06_Tools_Scripts/'):
                    return self.target_dir / "06_Tools_Scripts" / Path(*rel_path.parts[1:])
                elif str(rel_path).startswith('07_Archive_Backup/'):
                    return self.target_dir / "07_Archive_Backup" / Path(*rel_path.parts[1:])
                elif str(rel_path).startswith('15_Website_Hosting/'):
                    return self.target_dir / "10_Website_Hosting" / Path(*rel_path.parts[1:])
                elif rel_path.parts and rel_path.parts[0] in ['02_Analysis_Research', '03_Content_Development', '04_Technical_Implementation', 
                                                               '05_Reports_Documentation', '06_Tools_Scripts', '07_Archive_Backup', '15_Website_Hosting']:
                    # Handle case where it's a direct child
                    if rel_path.parts[0] == '15_Website_Hosting':
                        return self.target_dir / "10_Website_Hosting" / Path(*rel_path.parts[1:]) if len(rel_path.parts) > 1 else self.target_dir / "10_Website_Hosting" / file_name
                    else:
                        return self.target_dir / rel_path.parts[0] / Path(*rel_path.parts[1:]) if len(rel_path.parts) > 1 else self.target_dir / rel_path.parts[0] / file_name
                else:
                    return self.target_dir / "01_Project_Files" / relative
        
        # Default location
        return self.target_dir / "12_Related_Files" / file_name
    
    def consolidate_files(self):
        """Main consolidation process"""
        print("\n🚀 Starting consolidation process...")
        
        # Create target structure
        self.create_target_structure()
        
        # Find all files
        all_files = self.find_all_files()
        
        # Group files by hash to find duplicates
        print("\n📊 Analyzing files for duplicates...")
        hash_groups = defaultdict(list)
        
        for file_path in all_files:
            self.stats['files_processed'] += 1
            file_hash = self.get_file_hash(file_path)
            if file_hash:
                hash_groups[file_hash].append(file_path)
        
        # Process files
        print("\n📦 Moving files to consolidated location...")
        moved_files = set()
        
        for file_hash, file_list in hash_groups.items():
            if len(file_list) > 1:
                self.stats['duplicates_found'] += len(file_list) - 1
                best_file = self.determine_best_file(file_list)
                
                # Move best file
                if best_file:
                    target_path = self.get_target_path(best_file, file_hash)
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    if target_path not in moved_files:
                        try:
                            if target_path.exists():
                                # If target exists, check if source is better
                                source_info = self.get_file_info(best_file)
                                target_info = self.get_file_info(target_path)
                                
                                if source_info and target_info:
                                    if source_info['size'] > target_info['size'] or source_info['modified'] > target_info['modified']:
                                        shutil.copy2(best_file, target_path)
                                        self.consolidation_log.append(f"Updated: {best_file} -> {target_path}")
                                    else:
                                        # Keep existing, archive source
                                        archive_path = self.target_dir / "09_Duplicates_Archive" / f"{best_file.parent.name}_{best_file.name}"
                                        shutil.copy2(best_file, archive_path)
                                        self.consolidation_log.append(f"Archived (duplicate): {best_file} -> {archive_path}")
                                else:
                                    shutil.copy2(best_file, target_path)
                                    self.consolidation_log.append(f"Copied: {best_file} -> {target_path}")
                            else:
                                shutil.copy2(best_file, target_path)
                                self.consolidation_log.append(f"Copied: {best_file} -> {target_path}")
                            
                            moved_files.add(target_path)
                            self.stats['files_moved'] += 1
                        except Exception as e:
                            print(f"   ❌ Error moving {best_file}: {e}")
                            self.stats['errors'] += 1
                            self.consolidation_log.append(f"ERROR: {best_file} - {e}")
                    
                    # Archive other duplicates
                    for duplicate_file in file_list:
                        if duplicate_file != best_file:
                            archive_path = self.target_dir / "09_Duplicates_Archive" / f"{duplicate_file.parent.name}_{duplicate_file.name}"
                            archive_path.parent.mkdir(parents=True, exist_ok=True)
                            try:
                                if not archive_path.exists():
                                    shutil.copy2(duplicate_file, archive_path)
                                    self.consolidation_log.append(f"Archived duplicate: {duplicate_file} -> {archive_path}")
                            except Exception as e:
                                print(f"   ⚠️  Could not archive {duplicate_file}: {e}")
            else:
                # Single file, no duplicates
                file_path = file_list[0]
                target_path = self.get_target_path(file_path)
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                if target_path not in moved_files:
                    try:
                        if target_path.exists():
                            # Check if source is newer/larger
                            source_info = self.get_file_info(file_path)
                            target_info = self.get_file_info(target_path)
                            
                            if source_info and target_info:
                                if source_info['size'] > target_info['size'] or source_info['modified'] > target_info['modified']:
                                    shutil.copy2(file_path, target_path)
                                    self.consolidation_log.append(f"Updated: {file_path} -> {target_path}")
                                else:
                                    archive_path = self.target_dir / "09_Duplicates_Archive" / f"{file_path.parent.name}_{file_path.name}"
                                    shutil.copy2(file_path, archive_path)
                                    self.consolidation_log.append(f"Archived: {file_path} -> {archive_path}")
                            else:
                                shutil.copy2(file_path, target_path)
                                self.consolidation_log.append(f"Copied: {file_path} -> {target_path}")
                        else:
                            shutil.copy2(file_path, target_path)
                            self.consolidation_log.append(f"Copied: {file_path} -> {target_path}")
                        
                        moved_files.add(target_path)
                        self.stats['files_moved'] += 1
                    except Exception as e:
                        print(f"   ❌ Error moving {file_path}: {e}")
                        self.stats['errors'] += 1
                        self.consolidation_log.append(f"ERROR: {file_path} - {e}")
        
        print(f"\n✅ Consolidation complete!")
    
    def generate_report(self):
        """Generate consolidation report"""
        report_path = self.target_dir / "CONSOLIDATION_REPORT.md"
        
        with open(report_path, 'w') as f:
            f.write("# Dr_Adu_Gainesville Consolidation Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Statistics\n\n")
            f.write(f"- **Files Processed:** {self.stats['files_processed']}\n")
            f.write(f"- **Files Moved:** {self.stats['files_moved']}\n")
            f.write(f"- **Duplicates Found:** {self.stats['duplicates_found']}\n")
            f.write(f"- **Directories Created:** {self.stats['directories_created']}\n")
            f.write(f"- **Errors:** {self.stats['errors']}\n\n")
            
            f.write("## Directory Structure\n\n")
            f.write("```\n")
            for item in sorted(self.target_dir.rglob('*')):
                if item.is_dir():
                    rel_path = item.relative_to(self.target_dir)
                    f.write(f"{rel_path}/\n")
            f.write("```\n\n")
            
            f.write("## Consolidation Log\n\n")
            f.write(f"Total operations: {len(self.consolidation_log)}\n\n")
            f.write("### Recent Operations\n\n")
            for log_entry in self.consolidation_log[-100:]:  # Last 100 entries
                f.write(f"- {log_entry}\n")
        
        print(f"\n📋 Report saved to: {report_path}")
    
    def run(self):
        """Run complete consolidation"""
        print("=" * 60)
        print("Dr_Adu_Gainesville Consolidation")
        print("=" * 60)
        
        self.consolidate_files()
        self.generate_report()
        
        print("\n" + "=" * 60)
        print(f"✅ Consolidation complete!")
        print(f"📁 Consolidated location: {self.target_dir}")
        print("=" * 60)

if __name__ == "__main__":
    consolidator = DrAduConsolidator()
    consolidator.run()
