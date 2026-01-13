#!/usr/bin/env python3
"""
Duplicate Cleanup Script
Provides options to safely remove duplicate files
"""

import json
import os
import shutil


def load_analysis_results():
    """Load the duplicate analysis results"""
    with open('duplicate_analysis.json', 'r') as f:
        return json.load(f)

def preview_cleanup(results):
    """Show what files would be removed"""
    print("🧹 DUPLICATE CLEANUP PREVIEW")
    print("=" * 50)
    
    exact_duplicates = results['exact_duplicates']
    total_files_to_remove = 0
    total_space_to_save = 0
    
    print(f"Found {len(exact_duplicates)} groups of exact duplicates")
    print("\nFiles that would be removed (keeping the first file in each group):")
    print("-" * 50)
    
    for i, (file_hash, files) in enumerate(exact_duplicates.items(), 1):
        if len(files) > 1:
            print(f"\nGroup {i}:")
            print(f"  KEEP: {files[0]['filename']} ({files[0]['size']/1024:.1f} KB)")
            
            for file_info in files[1:]:  # Skip the first file (keep this one)
                print(f"  REMOVE: {file_info['filename']} ({file_info['size']/1024:.1f} KB)")
                total_files_to_remove += 1
                total_space_to_save += file_info['size']
    
    print("\n📊 CLEANUP SUMMARY:")
    print(f"  • Files to remove: {total_files_to_remove}")
    print(f"  • Space to save: {total_space_to_save / (1024*1024):.2f} MB")
    
    return total_files_to_remove, total_space_to_save

def create_backup():
    """Create a backup of files before cleanup"""
    backup_dir = "duplicate_backup"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"✅ Created backup directory: {backup_dir}")
    return backup_dir

def cleanup_duplicates(results, create_backup_flag=True, dry_run=True):
    """Remove duplicate files"""
    exact_duplicates = results['exact_duplicates']
    
    if create_backup_flag:
        backup_dir = create_backup()
    
    removed_count = 0
    saved_space = 0
    
    print(f"\n{'DRY RUN: ' if dry_run else ''}CLEANING DUPLICATES...")
    print("=" * 50)
    
    for file_hash, files in exact_duplicates.items():
        if len(files) > 1:
            # Keep the first file, remove the rest
            keep_file = files[0]
            remove_files = files[1:]
            
            print(f"\nGroup: {keep_file['filename']}")
            print(f"  Keeping: {keep_file['filename']}")
            
            for file_info in remove_files:
                file_path = file_info['path']
                filename = file_info['filename']
                file_size = file_info['size']
                
                if dry_run:
                    print(f"  Would remove: {filename} ({file_size/1024:.1f} KB)")
                else:
                    try:
                        # Create backup if requested
                        if create_backup_flag:
                            backup_path = os.path.join(backup_dir, filename)
                            shutil.copy2(file_path, backup_path)
                        
                        # Remove the duplicate file
                        os.remove(file_path)
                        print(f"  ✅ Removed: {filename} ({file_size/1024:.1f} KB)")
                        removed_count += 1
                        saved_space += file_size
                        
                    except Exception as e:
                        print(f"  ❌ Error removing {filename}: {e}")
    
    if not dry_run:
        print("\n🎉 CLEANUP COMPLETE!")
        print(f"  • Files removed: {removed_count}")
        print(f"  • Space saved: {saved_space / (1024*1024):.2f} MB")
        if create_backup_flag:
            print(f"  • Backup created in: {backup_dir}/")
    else:
        print("\n📋 DRY RUN COMPLETE!")
        print(f"  • Files that would be removed: {removed_count}")
        print(f"  • Space that would be saved: {saved_space / (1024*1024):.2f} MB")

def interactive_cleanup():
    """Interactive cleanup with user choices"""
    print("🔍 DUPLICATE FILE CLEANUP TOOL")
    print("=" * 50)
    
    # Load analysis results
    try:
        results = load_analysis_results()
    except FileNotFoundError:
        print("❌ Error: duplicate_analysis.json not found!")
        print("Please run the duplicate_finder.py script first.")
        return
    
    # Show summary
    summary = results['summary']
    print("\n📊 ANALYSIS SUMMARY:")
    print(f"  • Total files: {summary['total_files']}")
    print(f"  • Duplicate groups: {summary['exact_duplicate_groups']}")
    print(f"  • Space that can be saved: {summary['space_savings_mb']:.2f} MB")
    
    # Preview cleanup
    print("\n" + "="*50)
    preview_cleanup(results)
    
    # Ask user what to do
    print("\n" + "="*50)
    print("What would you like to do?")
    print("1. Preview cleanup (dry run)")
    print("2. Clean up duplicates (with backup)")
    print("3. Clean up duplicates (no backup)")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            cleanup_duplicates(results, create_backup_flag=False, dry_run=True)
            break
        elif choice == "2":
            confirm = input("This will create a backup and remove duplicate files. Continue? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                cleanup_duplicates(results, create_backup_flag=True, dry_run=False)
            else:
                print("Cleanup cancelled.")
            break
        elif choice == "3":
            confirm = input("This will permanently remove duplicate files (NO BACKUP). Continue? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                cleanup_duplicates(results, create_backup_flag=False, dry_run=False)
            else:
                print("Cleanup cancelled.")
            break
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    interactive_cleanup()