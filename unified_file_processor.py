
#!/usr/bin/env python3
"""
Unified File Processor
Consolidates file processing functionality from multiple scripts into one system.
"""

import os
import shutil
import hashlib
from pathlib import Path
from typing import List, Dict, Callable, Optional
from datetime import datetime
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed


class FileProcessor:
    """Unified file processing system."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
    
    def calculate_file_hash(self, file_path: Path, algorithm: str = "md5") -> str:
        """Calculate hash of file."""
        hash_func = hashlib.new(algorithm)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    
    def find_duplicates_by_hash(self, directory: Path, extensions: List[str] = None) -> Dict[str, List[Path]]:
        """Find duplicate files by hash."""
        hash_to_files = {}
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if extensions and Path(file).suffix.lower() not in extensions:
                    continue
                
                file_path = Path(root) / file
                try:
                    file_hash = self.calculate_file_hash(file_path)
                    if file_hash not in hash_to_files:
                        hash_to_files[file_hash] = []
                    hash_to_files[file_hash].append(file_path)
                except Exception as e:
                    self.logger.warning(f"Could not hash {file_path}: {e}")
        
        # Filter to only include hashes with multiple files (duplicates)
        duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}
        return duplicates
    
    def organize_by_extension(self, source_dir: Path, dest_dir: Path) -> Dict[str, int]:
        """Organize files by extension."""
        results = {"organized": 0, "errors": 0}
        
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = Path(root) / file
                ext = file_path.suffix.lower()
                
                if ext:
                    ext_dir = dest_dir / ext[1:]  # Remove the dot
                else:
                    ext_dir = dest_dir / "no_extension"
                
                ext_dir.mkdir(parents=True, exist_ok=True)
                
                try:
                    dest_path = ext_dir / file_path.name
                    # Handle name conflicts
                    counter = 1
                    original_dest_path = dest_path
                    while dest_path.exists():
                        stem = original_dest_path.stem
                        suffix = original_dest_path.suffix
                        dest_path = original_dest_path.parent / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    shutil.move(str(file_path), str(dest_path))
                    results["organized"] += 1
                    self.logger.info(f"Moved {file_path} -> {dest_path}")
                except Exception as e:
                    self.logger.error(f"Error moving {file_path}: {e}")
                    results["errors"] += 1
        
        return results
    
    def organize_by_size(self, source_dir: Path, dest_dir: Path) -> Dict[str, int]:
        """Organize files by size."""
        size_categories = {
            "tiny": (0, 1024),  # < 1KB
            "small": (1024, 1024*100),  # 1KB - 100KB
            "medium": (1024*100, 1024*1024),  # 100KB - 1MB
            "large": (1024*1024, 1024*1024*10),  # 1MB - 10MB
            "huge": (1024*1024*10, float("inf"))  # > 10MB
        }
        
        results = {"organized": 0, "errors": 0}
        
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = Path(root) / file
                try:
                    size = file_path.stat().st_size
                    
                    # Determine size category
                    category = "unknown"
                    for cat, (min_size, max_size) in size_categories.items():
                        if min_size <= size < max_size:
                            category = cat
                            break
                    
                    cat_dir = dest_dir / category
                    cat_dir.mkdir(parents=True, exist_ok=True)
                    
                    dest_path = cat_dir / file_path.name
                    # Handle name conflicts
                    counter = 1
                    original_dest_path = dest_path
                    while dest_path.exists():
                        stem = original_dest_path.stem
                        suffix = original_dest_path.suffix
                        dest_path = original_dest_path.parent / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    shutil.move(str(file_path), str(dest_path))
                    results["organized"] += 1
                    self.logger.info(f"Moved {file_path} -> {dest_path}")
                except Exception as e:
                    self.logger.error(f"Error moving {file_path}: {e}")
                    results["errors"] += 1
        
        return results
    
    def batch_rename(self, directory: Path, rename_function: Callable[[Path], str]) -> Dict[str, int]:
        """Batch rename files using a custom function."""
        results = {"renamed": 0, "errors": 0}
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                old_path = Path(root) / file
                try:
                    new_name = rename_function(old_path)
                    if new_name != file:
                        new_path = old_path.parent / new_name
                        if not new_path.exists():
                            old_path.rename(new_path)
                            results["renamed"] += 1
                            self.logger.info(f"Renamed {old_path} -> {new_path}")
                        else:
                            self.logger.warning(f"Target name already exists: {new_path}")
                except Exception as e:
                    self.logger.error(f"Error renaming {old_path}: {e}")
                    results["errors"] += 1
        
        return results
    
    def remove_duplicates(self, directory: Path, strategy: str = "keep_first") -> Dict[str, int]:
        """Remove duplicate files."""
        duplicates = self.find_duplicates_by_hash(directory)
        
        results = {"removed": 0, "errors": 0, "duplicates_found": 0}
        
        for file_hash, files in duplicates.items():
            results["duplicates_found"] += len(files) - 1  # Count extra copies
            
            if strategy == "keep_first":
                # Keep the first file, remove the rest
                files_to_remove = files[1:]
            elif strategy == "keep_last":
                # Keep the last file, remove the rest
                files_to_remove = files[:-1]
            else:
                # Default to keep_first
                files_to_remove = files[1:]
            
            for file_path in files_to_remove:
                try:
                    file_path.unlink()
                    results["removed"] += 1
                    self.logger.info(f"Removed duplicate: {file_path}")
                except Exception as e:
                    self.logger.error(f"Error removing {file_path}: {e}")
                    results["errors"] += 1
        
        return results


class FileOrganizer:
    """Higher-level file organization tools."""
    
    def __init__(self):
        self.processor = FileProcessor()
    
    def smart_organize(self, source_dir: Path, dest_dir: Path, strategy: str = "extension") -> Dict[str, Any]:
        """Perform smart organization based on strategy."""
        if strategy == "extension":
            return self.processor.organize_by_extension(source_dir, dest_dir)
        elif strategy == "size":
            return self.processor.organize_by_size(source_dir, dest_dir)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
    
    def analyze_directory(self, directory: Path) -> Dict[str, Any]:
        """Analyze directory structure and content."""
        stats = {
            "total_files": 0,
            "total_size": 0,
            "extensions": {},
            "size_distribution": {},
            "duplicate_sets": 0
        }
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = Path(root) / file
                try:
                    stat = file_path.stat()
                    stats["total_files"] += 1
                    stats["total_size"] += stat.st_size
                    
                    # Extension stats
                    ext = file_path.suffix.lower()
                    stats["extensions"][ext] = stats["extensions"].get(ext, 0) + 1
                    
                    # Size distribution
                    size = stat.st_size
                    if size < 1024:
                        bucket = "under_1kb"
                    elif size < 1024 * 100:
                        bucket = "1kb_to_100kb"
                    elif size < 1024 * 1024:
                        bucket = "100kb_to_1mb"
                    elif size < 1024 * 1024 * 10:
                        bucket = "1mb_to_10mb"
                    else:
                        bucket = "over_10mb"
                    
                    stats["size_distribution"][bucket] = stats["size_distribution"].get(bucket, 0) + 1
                    
                except Exception as e:
                    self.processor.logger.error(f"Error analyzing {file_path}: {e}")
        
        # Find duplicates
        duplicates = self.processor.find_duplicates_by_hash(directory)
        stats["duplicate_sets"] = len(duplicates)
        
        return stats


# Example usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Unified File Processor")
    parser.add_argument("command", choices=["organize", "dedupe", "analyze", "rename"], 
                       help="Command to execute")
    parser.add_argument("directory", help="Directory to process")
    parser.add_argument("--strategy", choices=["extension", "size"], default="extension",
                       help="Organization strategy")
    parser.add_argument("--dest", help="Destination directory for organization")
    
    args = parser.parse_args()
    
    organizer = FileOrganizer()
    
    if args.command == "organize":
        if not args.dest:
            print("Error: --dest required for organize command")
            exit(1)
        result = organizer.smart_organize(Path(args.directory), Path(args.dest), args.strategy)
        print(f"Organization completed: {result}")
    
    elif args.command == "analyze":
        result = organizer.analyze_directory(Path(args.directory))
        print(json.dumps(result, indent=2, default=str))
    
    elif args.command == "dedupe":
        processor = FileProcessor()
        result = processor.remove_duplicates(Path(args.directory))
        print(f"De-duplication completed: {result}")
    
    else:
        print(f"Unknown command: {args.command}")
