#!/usr/bin/env python3
"""
Home Directory Cleanup Utility
Automatically organizes files in the home directory
"""

import hashlib
import json
import os
import shutil
from datetime import datetime
from pathlib import Path


class HomeCleanup:
    def __init__(self, home_dir=None):
        self.home = Path(home_dir or os.path.expanduser("~"))
        self.backup_dir = self.home / "Documents" / "archives" / "cleanup_backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Create organized directory structure
        self.directories = {
            'python_production': self.home / "Documents" / "python" / "00_production",
            'python_utilities': self.home / "Documents" / "python" / "03_utilities", 
            'python_experiments': self.home / "Documents" / "python" / "01_experiments",
            'python_archived': self.home / "Documents" / "python" / "02_archived",
            'reports': self.home / "Documents" / "reports",
            'env_backups': self.home / "Documents" / "archives" / "env_backups",
            'old_backups': self.home / "Documents" / "archives" / "old_backups"
        }
        
        # Create all directories
        for dir_path in self.directories.values():
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def get_file_hash(self, file_path):
        """Get MD5 hash of file for duplicate detection"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return None
    
    def categorize_python_file(self, file_path):
        """Categorize Python files based on name and content"""
        name = file_path.name.lower()
        
        # Production scripts (commonly used)
        production_keywords = [
            'complete_file_processor', 'comprehensive_file_processor',
            'final_consolidation', 'consolidate_to_dradu',
            'file_merge', 'file_summary', 'comprehensive_file_report'
        ]
        
        # Utility scripts
        utility_keywords = [
            'cleanup', 'organize', 'backup', 'archive', 'utility',
            'helper', 'tool', 'maintenance'
        ]
        
        # Experimental scripts
        experimental_keywords = [
            'test', 'experiment', 'trial', 'debug', 'temp',
            'draft', 'v1', 'v2', 'beta', 'alpha'
        ]
        
        # Check for production scripts
        if any(keyword in name for keyword in production_keywords):
            return 'python_production'
        
        # Check for utility scripts
        if any(keyword in name for keyword in utility_keywords):
            return 'python_utilities'
        
        # Check for experimental scripts
        if any(keyword in name for keyword in experimental_keywords):
            return 'python_experiments'
        
        # Check for duplicate indicators
        if '_1' in name or '_2' in name or 'copy' in name:
            return 'python_archived'
        
        # Default to experiments for unknown files
        return 'python_experiments'
    
    def cleanup_python_files(self):
        """Clean up Python files in home directory"""
        print("🐍 Cleaning up Python files...")
        
        python_files = list(self.home.glob("*.py"))
        moved_count = 0
        
        for file_path in python_files:
            try:
                category = self.categorize_python_file(file_path)
                dest_dir = self.directories[category]
                
                # Check for duplicates
                dest_file = dest_dir / file_path.name
                if dest_file.exists():
                    # Create backup of existing file
                    backup_file = self.backup_dir / f"{file_path.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
                    shutil.move(str(dest_file), str(backup_file))
                    print(f"  📦 Backed up existing: {dest_file.name}")
                
                # Move file
                shutil.move(str(file_path), str(dest_file))
                print(f"  ✅ Moved {file_path.name} to {category}")
                moved_count += 1
                
            except Exception as e:
                print(f"  ❌ Error moving {file_path.name}: {e}")
        
        print(f"📊 Moved {moved_count} Python files")
        return moved_count
    
    def cleanup_json_reports(self):
        """Clean up JSON report files"""
        print("📊 Cleaning up JSON reports...")
        
        json_files = list(self.home.glob("*_report.json"))
        moved_count = 0
        
        for file_path in json_files:
            try:
                dest_file = self.directories['reports'] / file_path.name
                shutil.move(str(file_path), str(dest_file))
                print(f"  ✅ Moved {file_path.name} to reports")
                moved_count += 1
            except Exception as e:
                print(f"  ❌ Error moving {file_path.name}: {e}")
        
        print(f"📊 Moved {moved_count} JSON reports")
        return moved_count
    
    def cleanup_env_files(self):
        """Clean up environment files"""
        print("🔧 Cleaning up environment files...")
        
        env_files = list(self.home.glob(".env*"))
        moved_count = 0
        
        for file_path in env_files:
            # Skip the main .env and .env.d directory
            if file_path.name in ['.env', '.env.d']:
                continue
            
            try:
                # Determine if it's a backup or old file
                if 'backup' in file_path.name or file_path.suffix in ['.bak', '.zip']:
                    dest_file = self.directories['env_backups'] / file_path.name
                else:
                    dest_file = self.directories['old_backups'] / file_path.name
                
                shutil.move(str(file_path), str(dest_file))
                print(f"  ✅ Moved {file_path.name} to archives")
                moved_count += 1
            except Exception as e:
                print(f"  ❌ Error moving {file_path.name}: {e}")
        
        print(f"📊 Moved {moved_count} environment files")
        return moved_count
    
    def cleanup_installer_files(self):
        """Clean up installer and temporary files"""
        print("🗑️ Cleaning up installer files...")
        
        installer_patterns = [
            "*.dmg", "*.pkg", "*.zip", "*.tar.gz", "*.sh"
        ]
        
        moved_count = 0
        for pattern in installer_patterns:
            files = list(self.home.glob(pattern))
            for file_path in files:
                # Skip important files
                if file_path.name in ['.zshrc', '.bashrc']:
                    continue
                
                try:
                    dest_file = self.directories['old_backups'] / file_path.name
                    shutil.move(str(file_path), str(dest_file))
                    print(f"  ✅ Moved {file_path.name} to archives")
                    moved_count += 1
                except Exception as e:
                    print(f"  ❌ Error moving {file_path.name}: {e}")
        
        print(f"📊 Moved {moved_count} installer files")
        return moved_count
    
    def generate_cleanup_report(self, stats):
        """Generate a cleanup report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'python_files_moved': stats.get('python_files', 0),
            'json_reports_moved': stats.get('json_reports', 0),
            'env_files_moved': stats.get('env_files', 0),
            'installer_files_moved': stats.get('installer_files', 0),
            'total_files_moved': sum(stats.values()),
            'directories_created': list(self.directories.keys())
        }
        
        report_file = self.directories['reports'] / f"cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📋 Cleanup report saved to: {report_file}")
        return report
    
    def run_cleanup(self):
        """Run the complete cleanup process"""
        print("🚀 Starting Home Directory Cleanup")
        print("=" * 50)
        
        stats = {}
        
        # Run cleanup tasks
        stats['python_files'] = self.cleanup_python_files()
        stats['json_reports'] = self.cleanup_json_reports()
        stats['env_files'] = self.cleanup_env_files()
        stats['installer_files'] = self.cleanup_installer_files()
        
        # Generate report
        report = self.generate_cleanup_report(stats)
        
        print("=" * 50)
        print("🎉 Cleanup Complete!")
        print(f"📊 Total files moved: {report['total_files_moved']}")
        print(f"📁 Directories created: {len(report['directories_created'])}")
        print(f"📋 Report saved to: {self.directories['reports']}")
        
        return report

if __name__ == "__main__":
    cleanup = HomeCleanup()
    cleanup.run_cleanup()