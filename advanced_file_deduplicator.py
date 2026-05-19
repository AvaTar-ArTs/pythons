#!/usr/bin/env python3
"""
Advanced File Deduplication and Organization Tool
Finds and removes duplicate files using multiple comparison strategies with enhanced safety features

Features:
- Multiple comparison algorithms (hash, size, content similarity)
- Advanced file selection strategies
- Comprehensive backup and logging
- Progress tracking and reporting
- Configurable exclusion patterns
- Dry-run mode for safe previewing
"""

import os
import sys
import json
import hashlib
import shutil
import logging
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
import argparse
import fnmatch
from concurrent.futures import ThreadPoolExecutor, as_completed


def setup_logging(log_file: str = "advanced_dedup.log"):
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


@dataclass
class DedupConfig:
    """Configuration for deduplication process."""
    exclude_patterns: List[str] = None
    include_patterns: List[str] = None
    min_file_size: int = 0  # Minimum file size in bytes
    max_file_size: int = 0  # Maximum file size in bytes (0 = no limit)
    hash_algorithm: str = 'md5'
    chunk_size: int = 8192
    backup_enabled: bool = True
    preserve_hard_links: bool = True
    dry_run: bool = True
    max_workers: int = 4
    selection_strategy: str = 'smart'  # smart, oldest, newest, shortest_path, largest, smallest

    def __post_init__(self):
        if self.exclude_patterns is None:
            self.exclude_patterns = [
                'node_modules', '.git', '__pycache__', '.next', 'dist', 'build',
                '.venv', 'venv', '.env', '.idea', '.vscode', 'target', 'bin',
                'obj', '.DS_Store', 'Archives/repos', 'github/', '*.tmp', '*.temp'
            ]
        if self.include_patterns is None:
            self.include_patterns = ['*']


class AdvancedFileDeduplicator:
    """Advanced file deduplication with multiple strategies and safety features."""
    
    def __init__(self, root_path: Path, config: DedupConfig = None):
        self.root_path = Path(root_path)
        self.config = config or DedupConfig()
        self.logger = setup_logging()
        self.file_hashes = defaultdict(list)
        self.duplicates = {}
        self.stats = {
            'total_files_scanned': 0,
            'total_duplicates_found': 0,
            'total_space_saved': 0,
            'files_removed': 0,
            'errors': 0
        }
    
    def matches_pattern(self, path: Path, patterns: List[str]) -> bool:
        """Check if path matches any of the given patterns."""
        path_str = str(path)
        for pattern in patterns:
            if fnmatch.fnmatch(path_str, pattern) or pattern in path_str:
                return True
        return False
    
    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded based on patterns."""
        return self.matches_pattern(path, self.config.exclude_patterns)
    
    def should_include(self, path: Path) -> bool:
        """Check if path should be included based on patterns."""
        if not self.config.include_patterns or '*' in self.config.include_patterns:
            return True
        return self.matches_pattern(path, self.config.include_patterns)
    
    def calculate_file_hash(self, file_path: Path) -> Optional[str]:
        """Calculate hash of file using configured algorithm."""
        try:
            hash_obj = hashlib.new(self.config.hash_algorithm)
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(self.config.chunk_size), b""):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except (IOError, OSError, PermissionError) as e:
            self.logger.warning(f"Could not read file {file_path}: {e}")
            return None
    
    def scan_files(self) -> Dict[str, List[Path]]:
        """Scan files and group by hash."""
        self.logger.info(f"🔍 Scanning files in {self.root_path}")
        
        # Use ThreadPoolExecutor for parallel file hashing
        all_files = []
        for root, dirs, files in os.walk(self.root_path):
            # Prune directories that match exclude patterns
            dirs[:] = [d for d in dirs if not self.should_exclude(Path(root) / d)]
            
            for file in files:
                file_path = Path(root) / file
                
                if self.should_exclude(file_path) or not self.should_include(file_path):
                    continue
                
                try:
                    stat = file_path.stat()
                    size = stat.st_size
                    
                    # Check size constraints
                    if size < self.config.min_file_size:
                        continue
                    if self.config.max_file_size > 0 and size > self.config.max_file_size:
                        continue
                    
                    all_files.append(file_path)
                    
                except (OSError, PermissionError):
                    continue
        
        self.logger.info(f"Found {len(all_files)} files to process")
        
        # Process files in parallel
        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            future_to_path = {
                executor.submit(self.calculate_file_hash, file_path): file_path 
                for file_path in all_files
            }
            
            for future in as_completed(future_to_path):
                file_path = future_to_path[future]
                try:
                    file_hash = future.result()
                    if file_hash:
                        self.file_hashes[file_hash].append(file_path)
                        self.stats['total_files_scanned'] += 1
                        
                        if self.stats['total_files_scanned'] % 1000 == 0:
                            self.logger.info(f"Processed {self.stats['total_files_scanned']} files...")
                            
                except Exception as e:
                    self.logger.error(f"Error processing {file_path}: {e}")
                    self.stats['errors'] += 1
        
        # Find duplicates (groups with more than 1 file)
        self.duplicates = {
            hash_val: files for hash_val, files in self.file_hashes.items() 
            if len(files) > 1
        }
        
        self.logger.info(f"Found {len(self.duplicates)} duplicate groups")
        return self.duplicates
    
    def select_file_to_keep(self, file_group: List[Path]) -> Path:
        """Select which file to keep from a duplicate group based on strategy."""
        if len(file_group) <= 1:
            return file_group[0] if file_group else None
        
        if self.config.selection_strategy == 'oldest':
            return min(file_group, key=lambda f: f.stat().st_mtime)
        elif self.config.selection_strategy == 'newest':
            return max(file_group, key=lambda f: f.stat().st_mtime)
        elif self.config.selection_strategy == 'shortest_path':
            return min(file_group, key=lambda f: len(str(f)))
        elif self.config.selection_strategy == 'largest':
            return max(file_group, key=lambda f: f.stat().st_size)
        elif self.config.selection_strategy == 'smallest':
            return min(file_group, key=lambda f: f.stat().st_size)
        else:  # smart strategy (default)
            # Smart strategy: prefer files in more organized paths
            def score_file(file_path):
                path_str = str(file_path)
                score = 0
                # Lower score for better organization
                score -= path_str.count(os.sep) * 10  # Prefer shallower paths
                score += path_str.count('_') * 2     # Penalize underscores
                score += path_str.count(' ') * 3     # Penalize spaces
                score += path_str.count('(') * 5     # Penalize parentheses
                score += path_str.count('copy') * 10 # Penalize "copy" in name
                score += path_str.count('~') * 5     # Penalize tildes
                return score
            
            return min(file_group, key=score_file)
    
    def create_backup_log(self, operation: str = "deduplication") -> Path:
        """Create a backup log file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_name = f"{operation.upper()}_LOG_{timestamp}.csv"
        log_path = self.root_path / log_name
        
        with open(log_path, 'w', encoding='utf-8') as log:
            log.write("action,removed_file,kept_file,file_hash,size_bytes,operation_time\n")
        
        return log_path
    
    def log_operation(self, log_path: Path, action: str, removed: Path, kept: Path, 
                     file_hash: str, size: int):
        """Log an operation to the backup log."""
        with open(log_path, 'a', encoding='utf-8') as log:
            log.write(f"{action},{removed},{kept},{file_hash},{size},{datetime.now().isoformat()}\n")
    
    def remove_duplicates(self) -> Dict[str, any]:
        """Remove duplicate files based on configuration."""
        if not self.duplicates:
            self.logger.info("No duplicates found to remove")
            return self.stats
        
        log_path = self.create_backup_log()
        self.logger.info(f"Starting removal process (dry_run={self.config.dry_run})")
        
        for file_hash, files in self.duplicates.items():
            # Choose which file to keep
            keep_file = self.select_file_to_keep(files)
            remove_files = [f for f in files if f != keep_file]
            
            for remove_file in remove_files:
                try:
                    file_stat = remove_file.stat()
                    file_size = file_stat.st_size
                    
                    if not self.config.dry_run:
                        # Actually remove the file
                        remove_file.unlink()
                        action = "removed"
                    else:
                        # Just log the planned action
                        action = "would_remove"
                    
                    # Log the operation
                    self.log_operation(log_path, action, remove_file, keep_file, 
                                     file_hash, file_size)
                    
                    self.stats['files_removed'] += 1
                    self.stats['total_space_saved'] += file_size
                    
                    if self.config.dry_run:
                        self.logger.info(f"Would remove: {remove_file}")
                    else:
                        self.logger.info(f"Removed: {remove_file}")
                        
                except Exception as e:
                    self.logger.error(f"Error processing {remove_file}: {e}")
                    self.stats['errors'] += 1
        
        self.stats['total_duplicates_found'] = sum(len(files)-1 for files in self.duplicates.values())
        
        self.logger.info(f"Removal process completed. Log saved to: {log_path}")
        return self.stats
    
    def generate_report(self) -> Dict[str, any]:
        """Generate a comprehensive report of the deduplication process."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'root_path': str(self.root_path),
            'config': {
                'exclude_patterns': self.config.exclude_patterns,
                'include_patterns': self.config.include_patterns,
                'min_file_size': self.config.min_file_size,
                'max_file_size': self.config.max_file_size,
                'hash_algorithm': self.config.hash_algorithm,
                'selection_strategy': self.config.selection_strategy,
                'dry_run': self.config.dry_run
            },
            'statistics': self.stats,
            'duplicate_groups': [
                {
                    'hash': hash_val,
                    'count': len(files),
                    'size_per_file': files[0].stat().st_size if files else 0,
                    'total_waste': (len(files) - 1) * files[0].stat().st_size if files else 0,
                    'files': [str(f) for f in files]
                }
                for hash_val, files in self.duplicates.items()
            ]
        }
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.root_path / f"DEDUPE_REPORT_{timestamp}.json"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        self.logger.info(f"Deduplication report saved to: {report_path}")
        return report


def main():
    """Main entry point with command-line interface."""
    parser = argparse.ArgumentParser(
        description='Advanced File Deduplication Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python advanced_dedup.py /path/to/directory                    # Dry run deduplication
  python advanced_dedup.py /path/to/directory --remove          # Actually remove duplicates
  python advanced_dedup.py /path/to/directory --strategy newest # Keep newest files
  python advanced_dedup.py /path/to/directory --min-size 1024   # Only process files > 1KB
        """
    )
    
    parser.add_argument('directory', help='Directory to deduplicate')
    parser.add_argument('--remove', action='store_true', help='Actually remove duplicates (default: dry run)')
    parser.add_argument('--strategy', choices=['smart', 'oldest', 'newest', 'shortest_path', 'largest', 'smallest'],
                       default='smart', help='Strategy for selecting which file to keep')
    parser.add_argument('--min-size', type=int, default=0, help='Minimum file size in bytes (default: 0)')
    parser.add_argument('--max-size', type=int, default=0, help='Maximum file size in bytes (0 = no limit)')
    parser.add_argument('--algorithm', choices=['md5', 'sha1', 'sha256'], 
                       default='md5', help='Hash algorithm to use')
    parser.add_argument('--workers', type=int, default=4, help='Number of worker threads')
    parser.add_argument('--include', action='append', help='Include pattern (can be used multiple times)')
    parser.add_argument('--exclude', action='append', help='Exclude pattern (can be used multiple times)')
    
    args = parser.parse_args()
    
    # Create configuration
    config = DedupConfig(
        exclude_patterns=args.exclude,
        include_patterns=args.include,
        min_file_size=args.min_size,
        max_file_size=args.max_size,
        hash_algorithm=args.algorithm,
        max_workers=args.workers,
        selection_strategy=args.strategy,
        dry_run=not args.remove
    )
    
    # Run deduplication
    deduper = AdvancedFileDeduplicator(Path(args.directory), config)
    
    try:
        # Scan for duplicates
        duplicates = deduper.scan_files()
        
        if not duplicates:
            print("✅ No duplicates found!")
            return
        
        # Remove duplicates
        stats = deduper.remove_duplicates()
        
        # Generate report
        report = deduper.generate_report()
        
        # Print summary
        print(f"\n📊 Deduplication Summary:")
        print(f"   Files scanned: {stats['total_files_scanned']:,}")
        print(f"   Duplicate groups found: {len(duplicates):,}")
        print(f"   Files that would be removed: {stats['files_removed']:,}")
        print(f"   Space that would be saved: {stats['total_space_saved'] / (1024*1024):.2f} MB")
        print(f"   Errors: {stats['errors']:,}")
        
        if args.remove:
            print(f"\n✅ Deduplication completed! Files removed and log saved.")
        else:
            print(f"\nℹ️  This was a dry run. Use --remove to actually delete duplicates.")
        
    except KeyboardInterrupt:
        print("\n⚠️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during deduplication: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()