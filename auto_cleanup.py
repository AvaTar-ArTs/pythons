#!/usr/bin/env python3
"""
Automatic Duplicate Cleanup Script
Removes duplicates with backup automatically
"""

import json
import os
import shutil


def load_analysis_results():
    """Load the duplicate analysis results"""
    with open('duplicate_analysis.json', 'r') as f:
        return json.load(f)

def create_backup():
    """Create a backup of files before cleanup"""
    backup_dir = "duplicate_backup"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"✅ Created backup directory: {backup_dir}")
    return backup_dir

def cleanup_duplicates():
    """Remove duplicate files with backup"""
    print("🧹 AUTOMATIC DUPLICATE CLEANUP")
    print("=" * 50)
    
    # Load analysis results
    try:
        results = load_analysis_results()
    except FileNotFoundError:
        print("❌ Error: duplicate_analysis.json not found!")
        return
    
    # Create backup
    backup_dir = create_backup()
    
    exact_duplicates = results['exact_duplicates']
    removed_count = 0
    saved_space = 0
    
    print(f"Processing {len(exact_duplicates)} duplicate groups...")
    print("=" * 50)
    
    for i, (file_hash, files) in enumerate(exact_duplicates.items(), 1):
        if len(files) > 1:
            # Keep the first file, remove the rest
            keep_file = files[0]
            remove_files = files[1:]
            
            if i <= 10:  # Show first 10 groups
                print(f"\nGroup {i}: Keeping {keep_file['filename']}")
            
            for file_info in remove_files:
                file_path = file_info['path']
                filename = file_info['filename']
                file_size = file_info['size']
                
                try:
                    # Create backup
                    backup_path = os.path.join(backup_dir, filename)
                    shutil.copy2(file_path, backup_path)
                    
                    # Remove the duplicate file
                    os.remove(file_path)
                    
                    if i <= 10:  # Show details for first 10 groups
                        print(f"  ✅ Removed: {filename} ({file_size/1024:.1f} KB)")
                    
                    removed_count += 1
                    saved_space += file_size
                    
                except Exception as e:
                    print(f"  ❌ Error removing {filename}: {e}")
        
        # Progress indicator
        if i % 100 == 0:
            print(f"Processed {i}/{len(exact_duplicates)} groups...")
    
    print("\n🎉 CLEANUP COMPLETE!")
    print(f"  • Files removed: {removed_count}")
    print(f"  • Space saved: {saved_space / (1024*1024):.2f} MB")
    print(f"  • Backup created in: {backup_dir}/")
    
    # Show final count
    remaining_files = len([f for f in os.listdir('.') if f.endswith('.jpg')])
    print(f"  • Files remaining: {remaining_files}")

if __name__ == "__main__":
    cleanup_duplicates()