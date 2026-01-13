#!/usr/bin/env python3
"""
Generate CSV file with all duplicate files from deep dive analysis
"""
import os
import hashlib
import subprocess
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import csv

class DuplicateCSVGenerator:
    """
    Content-Based Duplicate File Detector
    
    This tool identifies duplicate files by comparing their ACTUAL CONTENT
    (using MD5 hashes), not just filenames. Files with identical content
    but different names will be detected as duplicates.
    """
    def __init__(self, home_dir=None):
        self.home = Path(home_dir or Path.home())
        self.duplicates = defaultdict(list)  # Key: content hash, Value: list of files
        self.max_file_size = 10 * 1024 * 1024  # 10MB - files larger use sampling
        
    def calculate_hash(self, filepath):
        """
        Calculate MD5 hash based on FILE CONTENT (not filename).
        This ensures true duplicate detection based on actual file contents.
        """
        try:
            size = filepath.stat().st_size
            
            if size == 0:
                # Empty files get same hash
                return hashlib.md5(b'').hexdigest()
            
            if size > self.max_file_size:
                # For large files (>10MB), use content sampling:
                # - First 2KB (header/metadata)
                # - Middle 2KB (content sample)
                # - Last 2KB (footer/metadata)
                # - File size
                # This catches duplicates even if filenames differ
                with open(filepath, 'rb') as f:
                    first = f.read(2048)  # First 2KB
                    middle_pos = size // 2
                    f.seek(max(0, middle_pos - 1024))
                    middle = f.read(2048)  # Middle 2KB
                    f.seek(max(0, size - 2048))
                    last = f.read(2048)  # Last 2KB
                    # Combine with size for uniqueness
                    content = first + middle + last + str(size).encode()
                    return hashlib.md5(content).hexdigest()
            else:
                # For smaller files, hash entire content
                # This is the most accurate method
                with open(filepath, 'rb') as f:
                    file_content = f.read()
                    return hashlib.md5(file_content).hexdigest()
        except (IOError, OSError, PermissionError) as e:
            # Skip files we can't read
            return None
        except Exception as e:
            return None
    
    def get_file_size(self, filepath):
        """Get file size in bytes"""
        try:
            return filepath.stat().st_size
        except:
            return 0
    
    def format_size(self, bytes_size):
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f}{unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f}PB"
    
    def scan_for_duplicates(self, target_dir, max_depth=3, current_depth=0):
        """Scan directory for duplicate files"""
        exclude_patterns = [
            'node_modules', '.git', '__pycache__', '.venv', 'venv',
            '.next', 'dist', 'build', '.cache', 'Library', 'System',
            '.Trash', '.DS_Store'
        ]
        
        try:
            # Skip excluded directories
            if any(pattern in str(target_dir) for pattern in exclude_patterns):
                return
            
            # Limit depth
            if current_depth > max_depth:
                return
            
            if not target_dir.is_dir():
                return
            
            for item in target_dir.iterdir():
                try:
                    if item.is_file():
                        # Calculate content-based hash (not filename-based)
                        # Files with same content but different names will match
                        file_hash = self.calculate_hash(item)
                        if file_hash:
                            file_size = self.get_file_size(item)
                            self.duplicates[file_hash].append({
                                'path': str(item),
                                'size': file_size,
                                'name': item.name,  # Name stored for reference only
                                'parent': str(item.parent),
                                'hash': file_hash  # Content hash for verification
                            })
                    elif item.is_dir():
                        # Recurse into subdirectories
                        self.scan_for_duplicates(item, max_depth, current_depth + 1)
                except (PermissionError, OSError):
                    continue
        except (PermissionError, OSError):
            pass
    
    def generate_csv(self, output_path=None):
        """Generate CSV file with duplicate information"""
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = self.home / 'AVATARARTS' / f'DUPLICATES_{timestamp}.csv'
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Filter to only groups with 2+ files
        duplicate_groups = {k: v for k, v in self.duplicates.items() if len(v) > 1}
        
        # Sort by total size (largest first)
        sorted_groups = sorted(
            duplicate_groups.items(),
            key=lambda x: sum(f['size'] for f in x[1]),
            reverse=True
        )
        
        # Write CSV
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Group_ID',
                'File_Name',
                'Full_Path',
                'Parent_Directory',
                'Size_Bytes',
                'Size_Human',
                'Content_Hash',
                'File_Count_In_Group',
                'Total_Group_Size_Bytes',
                'Total_Group_Size_Human',
                'Potential_Savings_Bytes',
                'Potential_Savings_Human',
                'Keep_File',
                'Action',
                'Note'
            ])
            
            group_id = 1
            for file_hash, files in sorted_groups:
                # Sort files by path (keep first as primary)
                files_sorted = sorted(files, key=lambda x: x['path'])
                
                total_size = sum(f['size'] for f in files)
                # Potential savings = (count - 1) * size of one file
                file_size = files[0]['size']
                potential_savings = file_size * (len(files) - 1)
                
                # Mark first file as "KEEP", others as "REVIEW"
                # Note: Files are grouped by CONTENT HASH, not filename
                for idx, file_info in enumerate(files_sorted):
                    keep = "YES" if idx == 0 else "NO"
                    action = "KEEP" if idx == 0 else "DELETE (if identical)"
                    
                    # Check if filenames differ (content-based duplicate)
                    names_match = all(f['name'] == files_sorted[0]['name'] for f in files_sorted)
                    note = "Content-identical" if names_match else "Content-identical, different names"
                    
                    writer.writerow([
                        group_id,
                        file_info['name'],
                        file_info['path'],
                        file_info['parent'],
                        file_info['size'],
                        self.format_size(file_info['size']),
                        file_info.get('hash', 'N/A'),  # Content hash for verification
                        len(files),
                        total_size,
                        self.format_size(total_size),
                        potential_savings if idx > 0 else 0,
                        self.format_size(potential_savings) if idx > 0 else "0B",
                        keep,
                        action,
                        note
                    ])
                
                group_id += 1
        
        return output_path, len(duplicate_groups), sum(
            files[0]['size'] * (len(files) - 1)
            for files in duplicate_groups.values()
        )

def main():
    print("=" * 80)
    print("CONTENT-BASED DUPLICATE FILES CSV GENERATOR")
    print("=" * 80)
    print("⚠️  IMPORTANT: This tool compares FILE CONTENT, not filenames")
    print("    Files with identical content but different names will be detected")
    print("=" * 80)
    
    home = Path.home()
    print(f"Home directory: {home}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Major directories to scan
    major_dirs = [
        home / 'AVATARARTS',
        home / 'pythons',
        home / 'pythons-sort',
        home / 'Documents',
        home / 'Downloads',
        home / 'Pictures',
        home / 'Music',
        home / 'GitHub',
        home / 'scripts'
    ]
    
    generator = DuplicateCSVGenerator(home)
    
    print("Scanning for duplicates (this may take a while)...")
    print("Limiting depth to 3 levels for performance...\n")
    
    for dir_path in major_dirs:
        if dir_path.exists():
            print(f"  Scanning: {dir_path.name}...")
            generator.scan_for_duplicates(dir_path, max_depth=3)
    
    print("\nGenerating CSV file...")
    output_path, group_count, total_savings = generator.generate_csv()
    
    print("\n" + "=" * 80)
    print("✅ CSV GENERATION COMPLETE")
    print("=" * 80)
    print(f"Output file: {output_path}")
    print(f"Duplicate groups found: {group_count:,}")
    print(f"Potential space savings: {generator.format_size(total_savings)}")
    print(f"Total files in duplicates: {sum(len(files) for files in generator.duplicates.values() if len(files) > 1):,}")
    print("=" * 80)
    
    return output_path

if __name__ == "__main__":
    main()
