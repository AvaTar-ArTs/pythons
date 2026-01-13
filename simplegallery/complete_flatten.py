#!/usr/bin/env python3
"""
Complete Directory Flattening Script
Moves ALL files from subdirectories to the root level with descriptive prefixes
"""

import os
import re
import shutil
from collections import defaultdict
from pathlib import Path


def sanitize_filename(filename):
    """Sanitize filename to be filesystem-safe"""
    # Remove or replace problematic characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove multiple underscores
    filename = re.sub(r'_+', '_', filename)
    # Remove leading/trailing underscores
    filename = filename.strip('_')
    return filename

def get_file_type_prefix(file_path):
    """Get appropriate prefix based on file type and content"""
    ext = Path(file_path).suffix.lower()
    
    if ext == '.py':
        return 'PY_'
    elif ext == '.md':
        return 'DOC_'
    elif ext in ['.txt', '.log']:
        return 'TXT_'
    elif ext in ['.json', '.yaml', '.yml']:
        return 'CFG_'
    elif ext in ['.sh', '.bash']:
        return 'SH_'
    elif ext in ['.html', '.htm']:
        return 'WEB_'
    elif ext in ['.csv', '.xlsx', '.xls']:
        return 'DATA_'
    elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg']:
        return 'IMG_'
    elif ext in ['.zip', '.tar', '.gz']:
        return 'ARCH_'
    else:
        return 'FILE_'

def flatten_all_files(root_dir):
    """Flatten ALL files from subdirectories to root level"""
    root_path = Path(root_dir)
    moved_files = []
    conflicts = []
    
    # Get all files in subdirectories (not in root)
    all_files = []
    for file_path in root_path.rglob('*'):
        if file_path.is_file() and file_path.parent != root_path:
            # Skip certain files
            if any(skip in str(file_path) for skip in ['__pycache__', '.git', '.DS_Store']):
                continue
            all_files.append(file_path)
    
    print(f"Found {len(all_files)} files to move")
    
    # Process each file
    for file_path in all_files:
        try:
            # Create new filename with prefix
            relative_path = file_path.relative_to(root_path)
            path_parts = relative_path.parts[:-1]  # All parts except filename
            
            # Create descriptive prefix from directory structure
            if path_parts:
                dir_prefix = '_'.join(path_parts[:2])  # Use first 2 directory levels
                dir_prefix = sanitize_filename(dir_prefix)
                dir_prefix = f"{dir_prefix}_"
            else:
                dir_prefix = ""
            
            # Get file type prefix
            type_prefix = get_file_type_prefix(file_path)
            
            # Create new filename
            original_name = file_path.name
            new_name = f"{type_prefix}{dir_prefix}{original_name}"
            new_name = sanitize_filename(new_name)
            
            # Handle conflicts
            target_path = root_path / new_name
            counter = 1
            while target_path.exists():
                name_parts = new_name.rsplit('.', 1)
                if len(name_parts) == 2:
                    new_name = f"{name_parts[0]}_{counter}.{name_parts[1]}"
                else:
                    new_name = f"{new_name}_{counter}"
                target_path = root_path / new_name
                counter += 1
            
            # Move the file
            shutil.move(str(file_path), str(target_path))
            moved_files.append((str(file_path), str(target_path)))
            print(f"Moved: {file_path.name} -> {target_path.name}")
            
        except Exception as e:
            conflicts.append((str(file_path), str(e)))
            print(f"Error moving {file_path}: {e}")
    
    return moved_files, conflicts

def remove_empty_directories(root_dir):
    """Remove empty directories after flattening"""
    root_path = Path(root_dir)
    removed_dirs = []
    
    # Walk from bottom up to remove empty directories
    for dir_path in sorted(root_path.rglob('*'), key=lambda p: len(p.parts), reverse=True):
        if dir_path.is_dir() and dir_path != root_path:
            try:
                if not any(dir_path.iterdir()):  # Directory is empty
                    dir_path.rmdir()
                    removed_dirs.append(str(dir_path))
                    print(f"Removed empty directory: {dir_path}")
            except OSError:
                pass  # Directory not empty or permission error
    
    return removed_dirs

def create_file_index(root_dir):
    """Create an index file listing all organized files"""
    root_path = Path(root_dir)
    index_content = []
    
    # Group files by type
    files_by_type = defaultdict(list)
    
    for file_path in root_path.iterdir():
        if file_path.is_file():
            ext = file_path.suffix.lower()
            files_by_type[ext].append(file_path.name)
    
    # Create index content
    index_content.append("# Python Directory - Complete Flattened File Index\n")
    index_content.append(f"Generated: {os.popen('date').read().strip()}\n")
    index_content.append(f"Total files: {sum(len(files) for files in files_by_type.values())}\n\n")
    
    for ext, files in sorted(files_by_type.items()):
        if not ext:
            ext = "no extension"
        index_content.append(f"## {ext.upper()} Files ({len(files)})\n")
        for file_name in sorted(files):
            index_content.append(f"- {file_name}\n")
        index_content.append("\n")
    
    # Write index file
    index_path = root_path / "COMPLETE_FILE_INDEX.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.writelines(index_content)
    
    print(f"Created file index: {index_path}")
    return index_path

if __name__ == "__main__":
    root_directory = "/Users/steven/AvaTarArTs/python"
    
    print("Starting complete directory flattening process...")
    print(f"Root directory: {root_directory}")
    
    # Flatten all files
    moved_files, conflicts = flatten_all_files(root_directory)
    print(f"\nMoved {len(moved_files)} files")
    if conflicts:
        print(f"Encountered {len(conflicts)} conflicts")
        for source, error in conflicts:
            print(f"  {source}: {error}")
    
    # Remove empty directories
    print("\nRemoving empty directories...")
    removed_dirs = remove_empty_directories(root_directory)
    print(f"Removed {len(removed_dirs)} empty directories")
    
    # Create file index
    print("\nCreating file index...")
    index_path = create_file_index(root_directory)
    
    print("\nComplete directory flattening finished!")
    print(f"File index created at: {index_path}")