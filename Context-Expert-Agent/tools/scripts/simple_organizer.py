#!/usr/bin/env python3
"""
Simple file sorter and organizer for the current directory
"""
import os
import shutil
from pathlib import Path

def organize_files_by_type(directory):
    """Organize files in the current directory by type into subdirectories"""
    directory = Path(directory)
    
    # Define file type categories
    file_categories = {
        'documents': {'.txt', '.pdf', '.doc', '.docx', '.rtf', '.odt', '.md'},
        'images': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'},
        'videos': {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'},
        'audio': {'.mp3', '.wav', '.flac', '.aac', '.m4a', '.ogg', '.wma'},
        'data': {'.csv', '.json', '.xml', '.yaml', '.yml', '.sql', '.db'},
        'scripts': {'.py', '.js', '.sh', '.bash', '.pl', '.rb', '.php', '.html', '.css'},
        'archives': {'.zip', '.tar', '.gz', '.rar', '.7z', '.bz2', '.xz'},
        'configs': {'.env', '.ini', '.cfg', '.conf', '.toml', '.gitignore', '.dockerignore'}
    }
    
    # Counters
    organized_count = 0
    skipped_count = 0
    
    print(f"Organizing files in: {directory}")
    print("="*60)
    
    # Get all files in the current directory (not subdirectories)
    files = [f for f in directory.iterdir() if f.is_file()]
    
    for file_path in files:
        if file_path.name == os.path.basename(__file__):  # Skip this script
            continue
            
        file_ext = file_path.suffix.lower()
        
        # Determine category for the file
        category = 'other'  # Default category
        for cat_name, extensions in file_categories.items():
            if file_ext in extensions:
                category = cat_name
                break
        
        # Create category directory if it doesn't exist
        cat_dir = directory / category
        cat_dir.mkdir(exist_ok=True)
        
        # Move the file to its category directory
        target_path = cat_dir / file_path.name
        
        # Handle potential name conflicts
        counter = 1
        original_target = target_path
        while target_path.exists():
            stem = original_target.stem
            suffix = original_target.suffix
            target_path = cat_dir / f"{stem}_{counter}{suffix}"
            counter += 1
        
        try:
            shutil.move(str(file_path), str(target_path))
            print(f"Moved: {file_path.name} -> {category}/")
            organized_count += 1
        except Exception as e:
            print(f"Skipped: {file_path.name} (reason: {e})")
            skipped_count += 1
    
    print("="*60)
    print(f"Organization complete!")
    print(f"Files organized: {organized_count}")
    print(f"Files skipped: {skipped_count}")

def main():
    directory = Path.cwd()  # Current directory
    organize_files_by_type(directory)

if __name__ == "__main__":
    print("This script will organize files in the current directory by type.")
    print("It will create subdirectories for each file type and move files accordingly.")
    response = input("Do you want to continue? (y/N): ")
    if response.lower() == 'y':
        main()
    else:
        print("Operation cancelled.")