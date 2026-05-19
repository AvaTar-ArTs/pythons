#!/usr/bin/env python3
"""
Universal File Management Toolkit
Consolidates multiple file management functions into a single, comprehensive tool

Features:
- File organization and categorization
- Deduplication with multiple algorithms
- Content-aware renaming
- Batch processing with preview
- Backup and restore capabilities
- Progress tracking and reporting
"""

import os
import sys
import json
import hashlib
import shutil
import logging
import argparse
import fnmatch
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional, Callable
from datetime import datetime
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import ast
import mimetypes


def setup_logging(log_file: str = "file_management_toolkit.log"):
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


class FileHasher:
    """Handles file hashing for deduplication."""
    
    @staticmethod
    def calculate_file_hash(file_path: Path, algorithm: str = 'md5', chunk_size: int = 8192) -> str:
        """Calculate hash of file using specified algorithm."""
        hash_obj = hashlib.new(algorithm)
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except Exception as e:
            logging.error(f"Error calculating hash for {file_path}: {e}")
            return ""
    
    @staticmethod
    def calculate_content_hash(content: bytes, algorithm: str = 'md5') -> str:
        """Calculate hash of content."""
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(content)
        return hash_obj.hexdigest()


class ContentAnalyzer:
    """Analyzes file content to determine purpose and category."""
    
    @staticmethod
    def analyze_python_file(file_path: Path) -> Dict[str, any]:
        """Analyze Python file to determine its purpose."""
        analysis = {
            'imports': [],
            'functions': [],
            'classes': [],
            'docstring': '',
            'purpose': 'unknown',
            'category': 'utilities'
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Parse AST to extract structure
            try:
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            analysis['imports'].append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        analysis['imports'].append(node.module or '')
                    elif isinstance(node, ast.FunctionDef):
                        analysis['functions'].append(node.name)
                    elif isinstance(node, ast.ClassDef):
                        analysis['classes'].append(node.name)
                    elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and analysis['docstring'] == '':
                        if isinstance(node.value.value, str):
                            analysis['docstring'] = node.value.value
            
            except SyntaxError:
                # If syntax error, skip AST analysis
                pass
            
            # Determine purpose based on content
            content_lower = content.lower()
            
            # Determine category based on keywords
            if any(keyword in content_lower for keyword in ['api', 'client', 'request', 'http']):
                analysis['category'] = 'api_clients'
            elif any(keyword in content_lower for keyword in ['organize', 'rename', 'move', 'file', 'directory']):
                analysis['category'] = 'file_management'
            elif any(keyword in content_lower for keyword in ['dedup', 'duplicate', 'hash', 'md5']):
                analysis['category'] = 'deduplication'
            elif any(keyword in content_lower for keyword in ['youtube', 'video', 'download', 'scrap']):
                analysis['category'] = 'video_tools'
            elif any(keyword in content_lower for keyword in ['image', 'resize', 'crop', 'convert']):
                analysis['category'] = 'image_tools'
            elif any(keyword in content_lower for keyword in ['audio', 'mp3', 'wav', 'sound']):
                analysis['category'] = 'audio_tools'
            elif any(keyword in content_lower for keyword in ['ai', 'ml', 'model', 'predict']):
                analysis['category'] = 'ai_tools'
            elif any(keyword in content_lower for keyword in ['data', 'csv', 'json', 'parse']):
                analysis['category'] = 'data_utils'
            elif any(keyword in content_lower for keyword in ['social', 'twitter', 'instagram', 'facebook']):
                analysis['category'] = 'social_automation'
            elif any(keyword in content_lower for keyword in ['music', 'album', 'playlist', 'song']):
                analysis['category'] = 'music_tools'
            elif any(keyword in content_lower for keyword in ['test', 'unittest', 'pytest']):
                analysis['category'] = 'testing_debug'
            
            # Determine purpose
            if any(func in analysis['functions'] for func in ['organize', 'rename', 'move']):
                analysis['purpose'] = 'file_organizer'
            elif any(func in analysis['functions'] for func in ['dedup', 'remove_duplicates']):
                analysis['purpose'] = 'deduplicator'
            elif any(func in analysis['functions'] for func in ['download', 'fetch', 'get']):
                analysis['purpose'] = 'downloader'
            elif any(func in analysis['functions'] for func in ['process', 'transform', 'convert']):
                analysis['purpose'] = 'processor'
            elif any(func in analysis['functions'] for func in ['analyze', 'scan', 'detect']):
                analysis['purpose'] = 'analyzer'
            
        except Exception as e:
            logging.error(f"Error analyzing Python file {file_path}: {e}")
        
        return analysis


class FileOrganizer:
    """Handles file organization based on content analysis."""
    
    CATEGORIES = {
        '01_core_tools': ['manager', 'organizer', 'analyzer', 'explorer', 'consolidator'],
        '02_youtube_automation': ['youtube', 'video', 'shorts', 'reddit', 'tiktok'],
        '03_ai_creative_tools': ['ai', 'image', 'leonardo', 'dalle', 'comic', 'generator'],
        '04_web_scraping': ['scraper', 'crawler', 'downloader', 'api_client'],
        '05_automation': ['bot', 'automation', 'scheduler', 'workflow'],
        '06_data_processing': ['processor', 'converter', 'transformer', 'parser'],
        '07_media_tools': ['audio', 'video', 'image', 'upscaler', 'converter'],
        '08_utilities': ['utility', 'helper', 'tool', 'script'],
    }
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def suggest_category(self, file_path: Path) -> str:
        """Suggest a category for a file based on its content and name."""
        # First try content analysis for Python files
        if file_path.suffix.lower() == '.py':
            analysis = ContentAnalyzer.analyze_python_file(file_path)
            return analysis['category']
        
        # Otherwise use filename analysis
        name_lower = file_path.name.lower()
        
        for category, keywords in self.CATEGORIES.items():
            if any(keyword in name_lower for keyword in keywords):
                return category
        
        # Default to utilities if no match found
        return '08_utilities'


class Deduplicator:
    """Handles file deduplication."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def find_duplicates_by_hash(self, file_paths: List[Path], algorithm: str = 'md5') -> Dict[str, List[Path]]:
        """Find duplicate files using hash comparison."""
        hash_to_files = defaultdict(list)
        
        for file_path in file_paths:
            if not file_path.is_file():
                continue
                
            file_hash = FileHasher.calculate_file_hash(file_path, algorithm)
            if file_hash:
                hash_to_files[file_hash].append(file_path)
        
        # Filter to only include hashes with multiple files (duplicates)
        duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}
        
        return duplicates
    
    def find_duplicates_by_size(self, file_paths: List[Path]) -> Dict[int, List[Path]]:
        """Find potential duplicates by file size."""
        size_to_files = defaultdict(list)
        
        for file_path in file_paths:
            if not file_path.is_file():
                continue
                
            size = file_path.stat().st_size
            size_to_files[size].append(file_path)
        
        # Filter to only include sizes with multiple files
        potential_duplicates = {s: files for s, files in size_to_files.items() if len(files) > 1}
        
        return potential_duplicates


class UniversalFileToolkit:
    """Main class that consolidates all file management functionality."""
    
    def __init__(self):
        self.logger = setup_logging()
        self.organizer = FileOrganizer(self.logger)
        self.deduplicator = Deduplicator(self.logger)
        self.backup_locations = []
    
    def scan_directory(self, 
                      directory: Path, 
                      include_patterns: List[str] = None,
                      exclude_patterns: List[str] = None,
                      max_depth: int = None) -> List[Path]:
        """Scan directory for files with filtering options."""
        if include_patterns is None:
            include_patterns = ['*']
        if exclude_patterns is None:
            exclude_patterns = [
                'node_modules', '.git', '__pycache__', '.next', 'dist', 'build', 
                '.venv', 'venv', '.env', '.idea', '.vscode', 'target', 'bin', 
                'obj', '.DS_Store', 'Archives/repos', 'github/'
            ]
        
        files = []
        directory = Path(directory)
        
        # Convert patterns to compiled regex for faster matching
        exclude_regexes = [re.compile(fnmatch.translate(pattern)) for pattern in exclude_patterns]
        
        for root, dirs, filenames in os.walk(directory):
            # Prune directories that match exclude patterns
            dirs[:] = [d for d in dirs if not any(regex.match(d) for regex in exclude_regexes)]
            
            # Check depth if specified
            if max_depth is not None:
                current_depth = len(Path(root).relative_to(directory).parts)
                if current_depth > max_depth:
                    continue
            
            for filename in filenames:
                file_path = Path(root) / filename
                
                # Check if file matches include patterns
                if any(self._match_pattern(filename, pattern) for pattern in include_patterns):
                    # Check if file path contains excluded patterns
                    path_str = str(file_path)
                    if not any(pattern in path_str for pattern in exclude_patterns):
                        files.append(file_path)
        
        self.logger.info(f"📁 Found {len(files)} files in {directory}")
        return files
    
    def _match_pattern(self, filename: str, pattern: str) -> bool:
        """Match filename against pattern (supports wildcards)."""
        import fnmatch
        return fnmatch.fnmatch(filename, pattern)
    
    def organize_files(self, 
                      source_dir: Path, 
                      dest_dir: Path = None,
                      strategy: str = 'content_analysis',
                      dry_run: bool = True) -> Dict[str, any]:
        """Organize files using specified strategy."""
        if dest_dir is None:
            dest_dir = Path(source_dir) / "_organized"
        
        files = self.scan_directory(source_dir)
        results = {
            'organized': [],
            'failed': [],
            'strategy': strategy,
            'dry_run': dry_run
        }
        
        self.logger.info(f"🚀 Organizing {len(files)} files using '{strategy}' strategy")
        
        for file_path in files:
            try:
                if strategy == 'content_analysis':
                    category = self.organizer.suggest_category(file_path)
                elif strategy == 'extension':
                    category = file_path.suffix.lower().strip('.') or 'no_ext'
                elif strategy == 'size':
                    size = file_path.stat().st_size
                    if size < 1024 * 1024:  # < 1MB
                        category = 'small'
                    elif size < 10 * 1024 * 1024:  # < 10MB
                        category = 'medium'
                    else:
                        category = 'large'
                else:
                    category = 'misc'
                
                # Create destination path
                dest_path = dest_dir / category / file_path.name
                
                # Handle duplicate names
                counter = 1
                original_dest_path = dest_path
                while dest_path.exists() and not dry_run:
                    stem = original_dest_path.stem
                    suffix = original_dest_path.suffix
                    dest_path = original_dest_path.parent / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                if not dry_run:
                    # Create destination directory
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Move file
                    shutil.move(str(file_path), str(dest_path))
                else:
                    self.logger.info(f"[DRY RUN] Would move {file_path} -> {dest_path}")
                
                results['organized'].append({
                    'source': str(file_path),
                    'destination': str(dest_path),
                    'category': category
                })
                
            except Exception as e:
                self.logger.error(f"❌ Failed to organize {file_path}: {e}")
                results['failed'].append({
                    'file': str(file_path),
                    'error': str(e)
                })
        
        self.logger.info(f"✅ Organized {len(results['organized'])} files, {len(results['failed'])} failed")
        return results
    
    def deduplicate_files(self, 
                         directory: Path, 
                         algorithm: str = 'md5',
                         strategy: str = 'move_to_duplicates',
                         dry_run: bool = True) -> Dict[str, any]:
        """Find and handle duplicate files."""
        files = self.scan_directory(directory)
        duplicates = self.deduplicator.find_duplicates_by_hash(files, algorithm)
        
        results = {
            'duplicates_found': 0,
            'files_removed': 0,
            'duplicates': [],
            'dry_run': dry_run
        }
        
        self.logger.info(f"🔍 Found {len(duplicates)} sets of duplicate files")
        
        for file_hash, file_list in duplicates.items():
            results['duplicates_found'] += len(file_list) - 1  # Count extra copies
            
            # Keep the first file, process the rest
            kept_file = file_list[0]
            duplicate_files = file_list[1:]
            
            for dup_file in duplicate_files:
                try:
                    if not dry_run:
                        if strategy == 'move_to_duplicates':
                            # Move to duplicates folder
                            dup_dir = directory / "_duplicates"
                            dup_dir.mkdir(exist_ok=True)
                            new_path = dup_dir / dup_file.name
                            
                            # Handle name conflicts
                            counter = 1
                            original_new_path = new_path
                            while new_path.exists():
                                stem = original_new_path.stem
                                suffix = original_new_path.suffix
                                new_path = original_new_path.parent / f"{stem}_{counter}{suffix}"
                                counter += 1
                            
                            shutil.move(str(dup_file), str(new_path))
                        elif strategy == 'delete':
                            # Delete the duplicate
                            os.remove(dup_file)
                        elif strategy == 'hardlink':
                            # Create hard link to save space
                            os.remove(dup_file)
                            os.link(str(kept_file), str(dup_file))
                    
                    results['duplicates'].append({
                        'kept': str(kept_file),
                        'removed': str(dup_file),
                        'strategy': strategy
                    })
                    
                    results['files_removed'] += 1
                    
                except Exception as e:
                    self.logger.error(f"❌ Failed to handle duplicate {dup_file}: {e}")
        
        self.logger.info(f"✅ Processed {results['files_removed']} duplicate files")
        return results
    
    def rename_files_intelligently(self, 
                                  directory: Path,
                                  strategy: str = 'content_analysis',
                                  dry_run: bool = True) -> Dict[str, any]:
        """Rename files based on content analysis."""
        files = self.scan_directory(directory, include_patterns=['*.py', '*.js', '*.ts', '*.txt', '*.md'])
        
        results = {
            'renamed': [],
            'failed': [],
            'dry_run': dry_run
        }
        
        self.logger.info(f"🏷️  Renaming {len(files)} files using '{strategy}' strategy")
        
        for file_path in files:
            try:
                if strategy == 'content_analysis' and file_path.suffix.lower() == '.py':
                    analysis = ContentAnalyzer.analyze_python_file(file_path)
                    purpose = analysis['purpose']
                    category = analysis['category']
                    
                    # Create new name based on analysis
                    stem = file_path.stem
                    if purpose != 'unknown':
                        new_stem = f"{category}_{purpose}_{stem}"
                    else:
                        new_stem = f"{category}_{stem}"
                    
                    new_name = f"{new_stem}{file_path.suffix}"
                    new_path = file_path.parent / new_name
                else:
                    # Fallback to basic analysis
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    if len(content) > 100:
                        preview = content[:100].replace('\n', '_').replace(' ', '_')
                        new_name = f"{file_path.stem}_analyzed_{preview[:30]}{file_path.suffix}"
                        new_path = file_path.parent / new_name
                    else:
                        continue  # Skip very short files
                
                # Handle name conflicts
                counter = 1
                original_new_path = new_path
                while new_path.exists() and new_path != file_path and not dry_run:
                    stem = original_new_path.stem
                    suffix = original_new_path.suffix
                    new_path = original_new_path.parent / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                if not dry_run and new_path != file_path:
                    file_path.rename(new_path)
                
                if new_path != file_path:
                    results['renamed'].append({
                        'old_name': str(file_path),
                        'new_name': str(new_path),
                        'strategy': strategy
                    })
                
                if dry_run and new_path != file_path:
                    self.logger.info(f"[DRY RUN] Would rename {file_path} -> {new_path}")
                
            except Exception as e:
                self.logger.error(f"❌ Failed to rename {file_path}: {e}")
                results['failed'].append({
                    'file': str(file_path),
                    'error': str(e)
                })
        
        self.logger.info(f"✅ Renamed {len(results['renamed'])} files, {len(results['failed'])} failed")
        return results
    
    def create_backup(self, source_dir: Path, backup_dir: Path = None) -> Path:
        """Create a backup of a directory."""
        if backup_dir is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = source_dir.parent / f"backup_{timestamp}"
        
        self.logger.info(f"💾 Creating backup of {source_dir} to {backup_dir}")
        
        shutil.copytree(source_dir, backup_dir, dirs_exist_ok=True)
        self.backup_locations.append(str(backup_dir))
        
        self.logger.info(f"✅ Backup created at {backup_dir}")
        return backup_dir
    
    def generate_report(self, results: Dict[str, any], output_file: Path = None) -> str:
        """Generate a report of operations."""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = Path.cwd() / f"file_management_report_{timestamp}.json"
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'tool': 'Universal File Management Toolkit',
            'results': results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        self.logger.info(f"📋 Report saved to {output_file}")
        return str(output_file)


def main():
    """Main entry point with command-line interface."""
    parser = argparse.ArgumentParser(
        description='Universal File Management Toolkit - Consolidates file management operations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python universal_file_toolkit.py organize /path/to/files                    # Organize files
  python universal_file_toolkit.py dedupe /path/to/files                     # Remove duplicates  
  python universal_file_toolkit.py rename /path/to/files                     # Rename intelligently
  python universal_file_toolkit.py scan /path/to/files                       # Just scan files
  python universal_file_toolkit.py organize /path/to/files --strategy content_analysis --dry-run  # Preview organization
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Organize command
    organize_parser = subparsers.add_parser('organize', help='Organize files')
    organize_parser.add_argument('directory', help='Directory to organize')
    organize_parser.add_argument('--strategy', choices=['content_analysis', 'extension', 'size'], 
                                default='content_analysis', help='Organization strategy')
    organize_parser.add_argument('--dest', help='Destination directory')
    organize_parser.add_argument('--dry-run', action='store_true', help='Preview changes only')
    
    # Deduplicate command
    dedupe_parser = subparsers.add_parser('dedupe', help='Find and remove duplicates')
    dedupe_parser.add_argument('directory', help='Directory to deduplicate')
    dedupe_parser.add_argument('--algorithm', choices=['md5', 'sha1', 'sha256'], 
                              default='md5', help='Hash algorithm to use')
    dedupe_parser.add_argument('--strategy', choices=['move_to_duplicates', 'delete', 'hardlink'], 
                              default='move_to_duplicates', help='What to do with duplicates')
    dedupe_parser.add_argument('--dry-run', action='store_true', help='Preview changes only')
    
    # Rename command
    rename_parser = subparsers.add_parser('rename', help='Rename files intelligently')
    rename_parser.add_argument('directory', help='Directory to rename files in')
    rename_parser.add_argument('--strategy', choices=['content_analysis'], 
                              default='content_analysis', help='Rename strategy')
    rename_parser.add_argument('--dry-run', action='store_true', help='Preview changes only')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Just scan directory')
    scan_parser.add_argument('directory', help='Directory to scan')
    scan_parser.add_argument('--pattern', action='append', default=['*'], help='Include patterns')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    toolkit = UniversalFileToolkit()
    
    try:
        if args.command == 'organize':
            dest_dir = Path(args.dest) if args.dest else None
            results = toolkit.organize_files(
                Path(args.directory), 
                dest_dir=dest_dir,
                strategy=args.strategy,
                dry_run=args.dry_run
            )
            toolkit.generate_report(results)
            
        elif args.command == 'dedupe':
            results = toolkit.deduplicate_files(
                Path(args.directory),
                algorithm=args.algorithm,
                strategy=args.strategy,
                dry_run=args.dry_run
            )
            toolkit.generate_report(results)
            
        elif args.command == 'rename':
            results = toolkit.rename_files_intelligently(
                Path(args.directory),
                strategy=args.strategy,
                dry_run=args.dry_run
            )
            toolkit.generate_report(results)
            
        elif args.command == 'scan':
            files = toolkit.scan_directory(
                Path(args.directory),
                include_patterns=args.pattern
            )
            print(f"Found {len(files)} files:")
            for f in files[:10]:  # Show first 10
                print(f"  {f}")
            if len(files) > 10:
                print(f"  ... and {len(files) - 10} more")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()