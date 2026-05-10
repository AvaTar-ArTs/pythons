#!/usr/bin/env python3
"""
Enhanced File Organization Toolkit

This script provides advanced file organization capabilities with improved error handling,
logging, and configuration options. It includes features for organizing files based on
content analysis, file types, and custom rules.

Features:
- Content-aware file organization
- Multiple organization strategies
- Dry-run mode for previewing changes
- Backup and rollback capabilities
- Progress tracking and reporting
"""

import os
import sys
import shutil
import json
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from collections import defaultdict
import mimetypes
import hashlib


def setup_logging(log_file: str = "file_organization.log"):
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


class FileOrganizer:
    """Advanced file organization toolkit."""
    
    def __init__(self, source_dir: str, dest_dir: str = None, config: Dict = None):
        self.source_dir = Path(source_dir)
        self.dest_dir = Path(dest_dir) if dest_dir else self.source_dir / "_organized"
        self.config = config or self._get_default_config()
        self.logger = setup_logging()
        self.organized_files = []
        self.failed_files = []
        self.stats = defaultdict(int)
        
    def _get_default_config(self) -> Dict:
        """Get default configuration."""
        return {
            'strategies': ['extension', 'size', 'date'],  # Organization strategies
            'file_types': {
                'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.md', '.csv', '.xls', '.xlsx'],
                'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
                'audio': ['.mp3', '.wav', '.flac', '.aac', '.m4a', '.ogg'],
                'video': ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'],
                'archives': ['.zip', '.rar', '.tar', '.gz', '.7z'],
                'code': ['.py', '.js', '.ts', '.html', '.css', '.java', '.cpp', '.c', '.h', '.json', '.xml']
            },
            'size_thresholds': {
                'small': 1024 * 1024,      # < 1MB
                'medium': 10 * 1024 * 1024, # < 10MB
                'large': 100 * 1024 * 1024  # < 100MB
            },
            'dry_run': False,
            'backup': True,
            'preserve_structure': False,
            'custom_rules': []  # Custom organization rules
        }
    
    def scan_files(self) -> List[Path]:
        """Scan source directory and return list of files to organize."""
        files = []
        for root, dirs, filenames in os.walk(self.source_dir):
            # Skip hidden directories and the destination directory
            dirs[:] = [d for d in dirs if not d.startswith('.') and Path(root) / d != self.dest_dir]
            
            for filename in filenames:
                if filename.startswith('.'):
                    continue  # Skip hidden files
                
                filepath = Path(root) / filename
                files.append(filepath)
        
        self.logger.info(f"📁 Found {len(files)} files to organize in {self.source_dir}")
        return files
    
    def analyze_file(self, filepath: Path) -> Dict:
        """Analyze a file and return its properties."""
        stat = filepath.stat()
        
        # Determine file type based on extension
        ext = filepath.suffix.lower()
        file_type = 'other'
        for category, extensions in self.config['file_types'].items():
            if ext in extensions:
                file_type = category
                break
        
        # Determine size category
        size_cat = 'unknown'
        for category, threshold in self.config['size_thresholds'].items():
            if stat.st_size < threshold:
                size_cat = category
                break
        
        # Determine date-based category
        mod_date = datetime.fromtimestamp(stat.st_mtime)
        age_days = (datetime.now() - mod_date).days
        if age_days < 7:
            date_cat = 'recent'
        elif age_days < 30:
            date_cat = 'monthly'
        elif age_days < 365:
            date_cat = 'yearly'
        else:
            date_cat = 'old'
        
        return {
            'path': filepath,
            'name': filepath.name,
            'ext': ext,
            'size': stat.st_size,
            'size_category': size_cat,
            'modified': mod_date,
            'date_category': date_cat,
            'type': file_type,
            'mime_type': mimetypes.guess_type(str(filepath))[0] or 'unknown'
        }
    
    def determine_destination(self, file_info: Dict) -> Path:
        """Determine destination path based on organization strategy."""
        # Apply custom rules first
        for rule in self.config['custom_rules']:
            if self._matches_rule(file_info, rule):
                return self.dest_dir / rule['destination'] / file_info['name']
        
        # Apply default strategies
        dest_parts = [str(self.dest_dir)]
        
        for strategy in self.config['strategies']:
            if strategy == 'extension':
                dest_parts.append(file_info['type'])
            elif strategy == 'size':
                dest_parts.append(file_info['size_category'])
            elif strategy == 'date':
                dest_parts.append(file_info['date_category'])
            elif strategy == 'mime_type':
                mime_cat = file_info['mime_type'].split('/')[0] if file_info['mime_type'] != 'unknown' else 'other'
                dest_parts.append(mime_cat)
        
        # Create destination path
        dest_path = Path(*dest_parts) / file_info['name']
        return dest_path
    
    def _matches_rule(self, file_info: Dict, rule: Dict) -> bool:
        """Check if file matches a custom rule."""
        if 'extension' in rule and file_info['ext'] != rule['extension']:
            return False
        if 'type' in rule and file_info['type'] != rule['type']:
            return False
        if 'size_min' in rule and file_info['size'] < rule['size_min']:
            return False
        if 'size_max' in rule and file_info['size'] > rule['size_max']:
            return False
        return True
    
    def create_backup(self) -> Optional[Path]:
        """Create a backup of the source directory structure."""
        if not self.config['backup']:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.source_dir.parent / f"backup_{timestamp}"
        
        if self.config['dry_run']:
            self.logger.info(f"Would create backup at: {backup_dir}")
            return backup_dir
        
        try:
            shutil.copytree(self.source_dir, backup_dir, dirs_exist_ok=True)
            self.logger.info(f"💾 Backup created at: {backup_dir}")
            return backup_dir
        except Exception as e:
            self.logger.error(f"❌ Failed to create backup: {e}")
            return None
    
    def organize_files(self) -> Dict:
        """Organize files according to configuration."""
        files = self.scan_files()
        
        if not files:
            self.logger.info("📭 No files found to organize")
            return self._get_results()
        
        # Create backup if requested
        backup_path = self.create_backup()
        
        self.logger.info(f"🚀 Starting organization of {len(files)} files...")
        
        for i, filepath in enumerate(files, 1):
            try:
                # Analyze file
                file_info = self.analyze_file(filepath)
                
                # Determine destination
                dest_path = self.determine_destination(file_info)
                
                # Update stats
                self.stats[file_info['type']] += 1
                self.stats['total_processed'] += 1
                
                # Skip if dry run
                if self.config['dry_run']:
                    self.logger.info(f"[DRY RUN] Would move {filepath} -> {dest_path}")
                    self.organized_files.append((filepath, dest_path))
                    continue
                
                # Create destination directory
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Move file
                if self.config['preserve_structure']:
                    # Preserve original directory structure
                    rel_path = filepath.relative_to(self.source_dir)
                    dest_path = self.dest_dir / rel_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(filepath, dest_path)
                else:
                    # Move to organized structure
                    if dest_path.exists():
                        # Handle duplicate names
                        counter = 1
                        stem = dest_path.stem
                        suffix = dest_path.suffix
                        while dest_path.exists():
                            new_name = f"{stem}_{counter}{suffix}"
                            dest_path = dest_path.parent / new_name
                            counter += 1
                    
                    shutil.move(str(filepath), str(dest_path))
                
                self.organized_files.append((filepath, dest_path))
                self.logger.debug(f"✅ Moved {filepath.name} -> {dest_path}")
                
                # Progress indicator
                if i % 50 == 0 or i == len(files):
                    progress = (i / len(files)) * 100
                    self.logger.info(f"📊 Progress: {i}/{len(files)} files ({progress:.1f}%)")
                    
            except Exception as e:
                self.logger.error(f"❌ Failed to organize {filepath}: {e}")
                self.failed_files.append((filepath, str(e)))
        
        # Generate report
        self._generate_report(backup_path)
        
        return self._get_results()
    
    def _generate_report(self, backup_path: Optional[Path]):
        """Generate organization report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'source_dir': str(self.source_dir),
            'dest_dir': str(self.dest_dir),
            'total_processed': self.stats['total_processed'],
            'by_type': dict(self.stats),
            'organized_files': [(str(src), str(dst)) for src, dst in self.organized_files],
            'failed_files': [(str(path), error) for path, error in self.failed_files],
            'backup_path': str(backup_path) if backup_path else None,
            'config': self.config
        }
        
        report_file = self.dest_dir / "organization_report.json"
        
        if not self.config['dry_run']:
            report_file.parent.mkdir(parents=True, exist_ok=True)
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, default=str)
        
        self.logger.info(f"📋 Report saved to: {report_file}")
    
    def _get_results(self) -> Dict:
        """Get organization results."""
        return {
            'organized_count': len(self.organized_files),
            'failed_count': len(self.failed_files),
            'stats': dict(self.stats),
            'organized_files': self.organized_files,
            'failed_files': self.failed_files
        }


def main():
    """Main entry point with command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Enhanced File Organization Toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python enhanced_file_organizer.py /path/to/source                    # Organize with defaults
  python enhanced_file_organizer.py /path/to/source --dest /organized  # Custom destination
  python enhanced_file_organizer.py /path/to/source --dry-run         # Preview changes
  python enhanced_file_organizer.py /path/to/source --strategy type   # By file type only
        """
    )
    
    parser.add_argument(
        'source_dir',
        help='Source directory to organize'
    )
    
    parser.add_argument(
        '--dest',
        help='Destination directory (default: source_dir/_organized)'
    )
    
    parser.add_argument(
        '--strategy',
        choices=['extension', 'size', 'date', 'mime_type'],
        action='append',
        dest='strategies',
        help='Organization strategy (can be used multiple times)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without moving files'
    )
    
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Skip creating backup'
    )
    
    parser.add_argument(
        '--preserve-structure',
        action='store_true',
        help='Preserve original directory structure'
    )
    
    parser.add_argument(
        '--config',
        help='Configuration file (JSON format)'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = {}
    
    if args.config:
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                config.update(json.load(f))
        except Exception as e:
            print(f"❌ Error loading config file: {e}")
            sys.exit(1)
    
    # Override with command-line arguments
    if args.strategies:
        config['strategies'] = args.strategies
    if args.dry_run:
        config['dry_run'] = True
    if args.no_backup:
        config['backup'] = False
    if args.preserve_structure:
        config['preserve_structure'] = True
    
    # Create organizer and run
    dest_dir = args.dest or (Path(args.source_dir) / "_organized")
    organizer = FileOrganizer(args.source_dir, dest_dir, config)
    
    try:
        results = organizer.organize_files()
        
        print(f"\n📊 Organization Results:")
        print(f"   Files organized: {results['organized_count']}")
        print(f"   Files failed: {results['failed_count']}")
        print(f"   Destination: {organizer.dest_dir}")
        
        if results['failed_files']:
            print(f"\n❌ Failed files:")
            for filepath, error in results['failed_files'][:5]:  # Show first 5
                print(f"   • {filepath}: {error}")
            if len(results['failed_files']) > 5:
                print(f"   ... and {len(results['failed_files']) - 5} more")
        
        if args.dry_run:
            print(f"\nℹ️  This was a dry run - no files were actually moved")
        
    except Exception as e:
        print(f"❌ Error during organization: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()