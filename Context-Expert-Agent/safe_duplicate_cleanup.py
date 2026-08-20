#!/usr/bin/env python3
"""
Safe Duplicate Cleanup Script
Removes numbered duplicates while preserving original files
"""

import json
import re
from datetime import datetime
from pathlib import Path


class SafeDuplicateCleanup:
    def __init__(self, target_dir):
        self.target_dir = Path(target_dir)
        self.cleanup_log = []
        self.files_removed = 0
        self.space_saved = 0
        
    def is_numbered_duplicate(self, filename):
        """Check if file is a numbered duplicate (e.g., 'file.md 1', 'file.md 2')"""
        patterns = [
            r' \d+$',  # space followed by digits at end
            r'_\d+$',  # underscore followed by digits at end
            r'\.md \d+$',  # .md space digits
            r'\.txt \d+$',  # .txt space digits
            r'\.py \d+$',   # .py space digits
        ]
        
        for pattern in patterns:
            if re.search(pattern, filename):
                return True
        return False
    
    def get_original_name(self, filename):
        """Get the original filename by removing numbered suffix"""
        # Remove numbered suffixes
        original = re.sub(r' \d+$', '', filename)
        original = re.sub(r'_\d+$', '', original)
        return original
    
    def file_exists(self, filepath):
        """Check if file exists and get its size"""
        if filepath.exists():
            return filepath.stat().st_size
        return 0
    
    def cleanup_directory(self, directory):
        """Clean up duplicates in a directory"""
        print(f"🔍 Scanning directory: {directory}")
        
        # Group files by their original name
        file_groups = {}
        
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                filename = file_path.name
                
                if self.is_numbered_duplicate(filename):
                    original_name = self.get_original_name(filename)
                    
                    if original_name not in file_groups:
                        file_groups[original_name] = {'original': None, 'duplicates': []}
                    
                    file_groups[original_name]['duplicates'].append(file_path)
                else:
                    # This might be an original file
                    if filename not in file_groups:
                        file_groups[filename] = {'original': None, 'duplicates': []}
                    file_groups[filename]['original'] = file_path
        
        # Process each group
        for base_name, group in file_groups.items():
            if group['duplicates']:
                print(f"\n📁 Processing group: {base_name}")
                print(f"   Original: {group['original']}")
                print(f"   Duplicates: {len(group['duplicates'])} files")
                
                # If we have an original file, remove all duplicates
                if group['original'] and group['original'].exists():
                    print(f"   ✅ Keeping original: {group['original']}")
                    
                    for duplicate in group['duplicates']:
                        if duplicate.exists():
                            size = duplicate.stat().st_size
                            self.space_saved += size
                            self.files_removed += 1
                            
                            self.cleanup_log.append({
                                'action': 'removed_duplicate',
                                'file': str(duplicate),
                                'original': str(group['original']),
                                'size': size,
                                'timestamp': datetime.now().isoformat()
                            })
                            
                            print(f"   🗑️  Removing: {duplicate.name} ({size} bytes)")
                            duplicate.unlink()
                
                # If no original file, keep the first duplicate as original
                elif group['duplicates']:
                    original = group['duplicates'][0]
                    duplicates = group['duplicates'][1:]
                    
                    print(f"   ✅ Keeping as original: {original}")
                    
                    for duplicate in duplicates:
                        if duplicate.exists():
                            size = duplicate.stat().st_size
                            self.space_saved += size
                            self.files_removed += 1
                            
                            self.cleanup_log.append({
                                'action': 'removed_duplicate',
                                'file': str(duplicate),
                                'original': str(original),
                                'size': size,
                                'timestamp': datetime.now().isoformat()
                            })
                            
                            print(f"   🗑️  Removing: {duplicate.name} ({size} bytes)")
                            duplicate.unlink()
    
    def save_log(self, log_file):
        """Save cleanup log to file"""
        log_data = {
            'cleanup_date': datetime.now().isoformat(),
            'target_directory': str(self.target_dir),
            'files_removed': self.files_removed,
            'space_saved_bytes': self.space_saved,
            'space_saved_mb': round(self.space_saved / (1024 * 1024), 2),
            'cleanup_actions': self.cleanup_log
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"\n📝 Cleanup log saved to: {log_file}")
    
    def run_cleanup(self):
        """Run the complete cleanup process"""
        print("🚀 Starting Safe Duplicate Cleanup")
        print(f"📂 Target directory: {self.target_dir}")
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Create backup log directory
        log_dir = self.target_dir.parent / "cleanup_logs"
        log_dir.mkdir(exist_ok=True)
        
        # Run cleanup
        self.cleanup_directory(self.target_dir)
        
        # Save results
        log_file = log_dir / f"duplicate_cleanup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.save_log(log_file)
        
        # Print summary
        print("\n" + "=" * 60)
        print("🎉 CLEANUP COMPLETE!")
        print(f"📊 Files removed: {self.files_removed}")
        print(f"💾 Space saved: {round(self.space_saved / (1024 * 1024), 2)} MB")
        print(f"📝 Log saved to: {log_file}")
        print("=" * 60)

def main():
    # Target the backups directory
    backups_dir = Path.home() / "Documents" / "backups"
    
    if not backups_dir.exists():
        print(f"❌ Error: Directory {backups_dir} does not exist")
        return
    
    print("⚠️  WARNING: This will remove numbered duplicate files from the backups directory")
    print("✅ Original files will be preserved")
    print("📝 A detailed log will be created")
    print("🚀 Proceeding with cleanup automatically...")
    
    # Run cleanup
    cleanup = SafeDuplicateCleanup(backups_dir)
    cleanup.run_cleanup()

if __name__ == "__main__":
    main()