#!/usr/bin/env python3
"""
Simple disk usage analyzer for the current directory
"""
import os
from pathlib import Path

def get_directory_size(directory):
    """Calculate total size of a directory"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            # Skip hidden directories and common cache directories
            dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.git', '.svn']]
            
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, FileNotFoundError):
                    # Skip files that can't be accessed
                    continue
    except Exception:
        pass
    return total_size

def format_size(size_bytes):
    """Format size in human readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def analyze_disk_usage(directory, top_n=20):
    """Analyze disk usage of subdirectories"""
    print(f"Analyzing disk usage in: {directory}")
    print("="*60)
    
    directory = Path(directory)
    subdirs = []
    
    # Get all immediate subdirectories
    for item in directory.iterdir():
        if item.is_dir():
            size = get_directory_size(item)
            subdirs.append((size, item.name))
    
    # Sort by size (largest first)
    subdirs.sort(key=lambda x: x[0], reverse=True)
    
    print(f"\nTop {min(top_n, len(subdirs))} largest directories:\n")
    print(f"{'Size':<10} {'Directory':<50}")
    print("-" * 60)
    
    for size, name in subdirs[:top_n]:
        formatted_size = format_size(size)
        print(f"{formatted_size:<10} {name:<50}")
    
    # Also analyze file types
    print("\n" + "="*60)
    print("File type analysis:\n")
    
    file_types = {}
    total_files = 0
    
    for dirpath, dirnames, filenames in os.walk(directory):
        # Skip hidden directories and common cache directories
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.git', '.svn']]
        
        for filename in filenames:
            total_files += 1
            ext = Path(filename).suffix.lower()
            if ext:
                file_types[ext] = file_types.get(ext, 0) + 1
            else:
                file_types['(no extension)'] = file_types.get('(no extension)', 0) + 1
    
    # Sort file types by count
    sorted_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)
    
    print(f"{'Extension':<15} {'Count':<10}")
    print("-" * 25)
    
    for ext, count in sorted_types[:15]:  # Top 15 file types
        print(f"{ext:<15} {count:<10}")
    
    print(f"\nTotal files analyzed: {total_files}")
    print(f"Total directories: {len(subdirs)}")
    
    # Calculate total size
    total_size = sum(size for size, _ in subdirs)
    print(f"Total size: {format_size(total_size)}")

def main():
    directory = Path.cwd()  # Current directory
    analyze_disk_usage(directory)

if __name__ == "__main__":
    main()