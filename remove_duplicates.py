#!/usr/bin/env python3
"""
Safely remove duplicate files from Google Drive.
Includes dry-run mode and backup options.
"""
import os
import csv
import shutil
from pathlib import Path
from datetime import datetime

base_path = Path('/Users/steven/Library/CloudStorage/GoogleDrive-sjchaplinski@gmail.com')
duplicates_file = Path('/Users/steven/duplicate_files_to_remove.csv')
log_file = Path('/Users/steven/duplicate_removal_log.txt')

def format_size(size_bytes):
    """Format bytes to human readable size"""
    if size_bytes == 0:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def remove_duplicates(dry_run=True, backup=True, confirm_each=False):
    """Remove duplicate files based on the CSV report"""
    
    if not duplicates_file.exists():
        print(f"Error: {duplicates_file} not found!")
        print("Please run find_duplicates.py first.")
        return
    
    # Read duplicates to remove
    files_to_remove = []
    total_size = 0
    
    with open(duplicates_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            file_path = base_path / row['File_Path']
            if file_path.exists():
                files_to_remove.append({
                    'path': file_path,
                    'rel_path': row['File_Path'],
                    'name': row['File_Name'],
                    'size': int(row['Size']),
                    'type': row['Duplicate_Type'],
                    'keep_path': row['Keep_Path'],
                    'reason': row['Reason']
                })
                total_size += int(row['Size'])
    
    print(f"\n{'='*60}")
    print(f"DUPLICATE FILE REMOVAL")
    print(f"{'='*60}")
    print(f"Mode: {'DRY RUN (no files will be deleted)' if dry_run else 'LIVE (files will be deleted)'}")
    print(f"Files to process: {len(files_to_remove)}")
    print(f"Total size: {format_size(total_size)}")
    print(f"{'='*60}\n")
    
    if not files_to_remove:
        print("No duplicate files found to remove.")
        return
    
    # Create backup directory if needed
    backup_dir = None
    if backup and not dry_run:
        backup_dir = Path(f'/Users/steven/Google_Drive_Duplicates_Backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        backup_dir.mkdir(exist_ok=True)
        print(f"Backup directory: {backup_dir}\n")
    
    # Process files
    removed_count = 0
    error_count = 0
    saved_size = 0
    
    log_entries = []
    log_entries.append(f"Duplicate Removal Log - {datetime.now()}")
    log_entries.append(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log_entries.append(f"Total files: {len(files_to_remove)}")
    log_entries.append(f"Total size: {format_size(total_size)}")
    log_entries.append("")
    
    for i, file_info in enumerate(files_to_remove, 1):
        file_path = file_info['path']
        rel_path = file_info['rel_path']
        
        if not file_path.exists():
            log_entries.append(f"[{i}/{len(files_to_remove)}] SKIP: {rel_path} (file not found)")
            continue
        
        if confirm_each and not dry_run:
            response = input(f"\nRemove {rel_path}? (y/n/q): ").strip().lower()
            if response == 'q':
                print("Aborted by user.")
                break
            if response != 'y':
                log_entries.append(f"[{i}/{len(files_to_remove)}] SKIP: {rel_path} (user declined)")
                continue
        
        try:
            if dry_run:
                print(f"[{i}/{len(files_to_remove)}] WOULD REMOVE: {rel_path} ({format_size(file_info['size'])})")
                log_entries.append(f"[{i}/{len(files_to_remove)}] DRY RUN: {rel_path} ({format_size(file_info['size'])})")
                removed_count += 1
                saved_size += file_info['size']
            else:
                # Backup if requested
                if backup and backup_dir:
                    backup_path = backup_dir / rel_path.replace('/', '_')
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, backup_path)
                    log_entries.append(f"[{i}/{len(files_to_remove)}] BACKED UP: {backup_path}")
                
                # Remove file
                file_path.unlink()
                print(f"[{i}/{len(files_to_remove)}] REMOVED: {rel_path} ({format_size(file_info['size'])})")
                log_entries.append(f"[{i}/{len(files_to_remove)}] REMOVED: {rel_path} ({format_size(file_info['size'])})")
                removed_count += 1
                saved_size += file_info['size']
                
        except Exception as e:
            error_count += 1
            error_msg = f"ERROR removing {rel_path}: {str(e)}"
            print(f"[{i}/{len(files_to_remove)}] {error_msg}")
            log_entries.append(f"[{i}/{len(files_to_remove)}] {error_msg}")
    
    # Write log
    log_entries.append("")
    log_entries.append(f"Summary:")
    log_entries.append(f"  Files processed: {removed_count}")
    log_entries.append(f"  Errors: {error_count}")
    log_entries.append(f"  Space saved: {format_size(saved_size)}")
    if backup_dir:
        log_entries.append(f"  Backup location: {backup_dir}")
    
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_entries))
    
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Files processed: {removed_count}")
    print(f"Errors: {error_count}")
    print(f"Space saved: {format_size(saved_size)}")
    if backup_dir:
        print(f"Backup location: {backup_dir}")
    print(f"Log file: {log_file}")
    print(f"{'='*60}\n")
    
    if dry_run:
        print("This was a DRY RUN. No files were actually deleted.")
        print("To actually remove files, run with dry_run=False")

if __name__ == '__main__':
    import sys
    
    dry_run = True
    backup = True
    confirm_each = False
    
    if len(sys.argv) > 1:
        if '--live' in sys.argv or '--remove' in sys.argv:
            dry_run = False
            print("WARNING: This will DELETE files!")
            response = input("Are you sure? Type 'yes' to continue: ")
            if response.lower() != 'yes':
                print("Aborted.")
                sys.exit(0)
        if '--no-backup' in sys.argv:
            backup = False
        if '--confirm' in sys.argv:
            confirm_each = True
    
    remove_duplicates(dry_run=dry_run, backup=backup, confirm_each=confirm_each)
