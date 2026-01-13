#!/usr/bin/env python3
"""
AVATARARTS Organization Suite - Unified Management Tool
========================================================

A comprehensive workspace organization system that combines:
- Context-aware file organization
- Intelligent duplicate detection
- Automated archival of old files
- Storage analysis and cleanup
- Parent-folder content awareness

Commands:
  analyze     - Deep analysis of directory structure and storage
  organize    - Context-aware file organization
  cleanup     - Remove temporary files and optimize storage
  dedupe      - Find and handle duplicate files
  archive     - Auto-archive old analysis files
  fix-paths   - Update hardcoded paths in scripts

Author: AVATARARTS Organization Suite
Version: 2.0.0
Date: 2026-01-02
"""

import os
import sys
import shutil
import argparse
import json
import hashlib
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Set, Optional
from collections import defaultdict
import re


class Colors:
    """Terminal colors for better output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class AvatarArtsOrganizer:
    """Main organization system"""

    def __init__(self, workspace_root: Path = None):
        self.workspace_root = workspace_root or Path.cwd()
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load configuration with smart defaults"""
        return {
            'archive_age_days': 90,  # Archive files older than this
            'temp_patterns': ['.DS_Store', '*.tmp', '*.temp', '*.bak', '__pycache__'],
            'skip_dirs': {'.git', '.github', '.history', 'node_modules', '__pycache__'},
            'context_keywords': {
                'ai_ml': ['ai', 'ml', 'machine', 'learning', 'neural', 'model'],
                'seo_marketing': ['seo', 'marketing', 'campaign', 'keyword'],
                'automation': ['automation', 'workflow', 'script', 'bot'],
                'music_audio': ['music', 'audio', 'suno', 'track', 'song'],
                'content': ['content', 'creation', 'video', 'image'],
                'development': ['code', 'dev', 'develop', 'programming'],
                'analysis': ['analysis', 'data', 'report', 'analytics']
            },
            'file_categories': {
                'documents': {'.txt', '.pdf', '.doc', '.docx', '.md'},
                'images': {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'},
                'videos': {'.mp4', '.avi', '.mov', '.mkv', '.webm'},
                'audio': {'.mp3', '.wav', '.flac', '.aac', '.m4a'},
                'data': {'.csv', '.json', '.xml', '.yaml', '.yml', '.db'},
                'scripts': {'.py', '.js', '.sh', '.bash', '.rb'},
                'archives': {'.zip', '.tar', '.gz', '.rar', '.7z'},
                'configs': {'.env', '.ini', '.cfg', '.conf', '.toml'}
            }
        }

    def analyze(self, directory: Path = None) -> Dict:
        """Deep analysis of directory structure"""
        target = directory or self.workspace_root

        print(f"{Colors.HEADER}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}AVATARARTS Workspace Analysis{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*70}{Colors.ENDC}\n")

        stats = {
            'total_size': 0,
            'total_files': 0,
            'total_dirs': 0,
            'file_types': defaultdict(int),
            'large_dirs': [],
            'temp_files': [],
            'old_files': [],
            'duplicates': defaultdict(list)
        }

        # Walk directory tree
        for root, dirs, files in os.walk(target):
            # Skip hidden and excluded directories
            dirs[:] = [d for d in dirs if d not in self.config['skip_dirs'] and not d.startswith('.')]

            stats['total_dirs'] += len(dirs)

            for file in files:
                if file.startswith('.'):
                    continue

                filepath = Path(root) / file
                try:
                    file_size = filepath.stat().st_size
                    file_mtime = datetime.fromtimestamp(filepath.stat().st_mtime)

                    stats['total_files'] += 1
                    stats['total_size'] += file_size

                    # Track file types
                    ext = filepath.suffix.lower()
                    stats['file_types'][ext] += 1

                    # Find temp files
                    if any(file.endswith(p.replace('*', '')) for p in self.config['temp_patterns'] if '*' in p) or \
                       file in self.config['temp_patterns']:
                        stats['temp_files'].append(filepath)

                    # Find old files (for potential archival)
                    age_threshold = datetime.now() - timedelta(days=self.config['archive_age_days'])
                    if file_mtime < age_threshold and any(x in str(filepath) for x in ['analysis', 'report', 'summary']):
                        stats['old_files'].append((filepath, file_mtime))

                    # Find duplicates by content hash (for files < 10MB)
                    if file_size < 10 * 1024 * 1024:
                        file_hash = self._hash_file(filepath)
                        stats['duplicates'][file_hash].append(filepath)

                except (OSError, PermissionError):
                    continue

        # Find large directories
        for item in target.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                size = self._get_dir_size(item)
                stats['large_dirs'].append((item.name, size))

        stats['large_dirs'].sort(key=lambda x: x[1], reverse=True)

        self._print_analysis(stats)
        return stats

    def _hash_file(self, filepath: Path, chunk_size: int = 8192) -> str:
        """Calculate file hash"""
        hasher = hashlib.md5()
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(chunk_size):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except:
            return ""

    def _get_dir_size(self, directory: Path) -> int:
        """Calculate directory size"""
        total = 0
        try:
            for item in directory.rglob('*'):
                if item.is_file():
                    total += item.stat().st_size
        except:
            pass
        return total

    def _format_size(self, size_bytes: int) -> str:
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def _print_analysis(self, stats: Dict):
        """Print formatted analysis results"""
        print(f"{Colors.CYAN}📊 Workspace Overview{Colors.ENDC}")
        print(f"   Total Size: {Colors.BOLD}{self._format_size(stats['total_size'])}{Colors.ENDC}")
        print(f"   Total Files: {Colors.BOLD}{stats['total_files']:,}{Colors.ENDC}")
        print(f"   Total Directories: {Colors.BOLD}{stats['total_dirs']:,}{Colors.ENDC}\n")

        print(f"{Colors.CYAN}📁 Largest Directories (Top 10){Colors.ENDC}")
        for name, size in stats['large_dirs'][:10]:
            print(f"   {name:40s} {self._format_size(size):>12s}")
        print()

        print(f"{Colors.CYAN}📝 File Types (Top 10){Colors.ENDC}")
        sorted_types = sorted(stats['file_types'].items(), key=lambda x: x[1], reverse=True)[:10]
        for ext, count in sorted_types:
            ext_display = ext if ext else '[no extension]'
            print(f"   {ext_display:20s} {count:>8,} files")
        print()

        # Duplicates
        duplicate_groups = {k: v for k, v in stats['duplicates'].items() if len(v) > 1}
        if duplicate_groups:
            total_dup_size = sum(
                v[0].stat().st_size * (len(v) - 1)
                for v in duplicate_groups.values()
                if v and v[0].exists()
            )
            print(f"{Colors.YELLOW}🔄 Duplicate Files Found{Colors.ENDC}")
            print(f"   Duplicate groups: {len(duplicate_groups)}")
            print(f"   Potential savings: {self._format_size(total_dup_size)}")
            print(f"   Run 'avatararts_organize.py dedupe' for details\n")

        # Temp files
        if stats['temp_files']:
            temp_size = sum(f.stat().st_size for f in stats['temp_files'] if f.exists())
            print(f"{Colors.YELLOW}🧹 Temporary Files{Colors.ENDC}")
            print(f"   Count: {len(stats['temp_files'])}")
            print(f"   Size: {self._format_size(temp_size)}")
            print(f"   Run 'avatararts_organize.py cleanup' to remove\n")

        # Old files
        if stats['old_files']:
            print(f"{Colors.YELLOW}📦 Old Files (>90 days){Colors.ENDC}")
            print(f"   Count: {len(stats['old_files'])}")
            print(f"   Run 'avatararts_organize.py archive' to archive\n")

    def cleanup(self, dry_run: bool = False):
        """Remove temporary and cache files"""
        print(f"{Colors.HEADER}🧹 Cleanup Mode{Colors.ENDC}\n")

        removed_count = 0
        freed_space = 0

        for root, dirs, files in os.walk(self.workspace_root):
            dirs[:] = [d for d in dirs if d not in self.config['skip_dirs']]

            for file in files:
                filepath = Path(root) / file

                # Check if it matches temp patterns
                should_remove = False
                if file in self.config['temp_patterns']:
                    should_remove = True
                else:
                    for pattern in self.config['temp_patterns']:
                        if '*' in pattern and file.endswith(pattern.replace('*', '')):
                            should_remove = True
                            break

                if should_remove:
                    try:
                        size = filepath.stat().st_size
                        if dry_run:
                            print(f"   Would remove: {filepath}")
                        else:
                            filepath.unlink()
                            print(f"   {Colors.GREEN}✓{Colors.ENDC} Removed: {filepath.name}")
                        removed_count += 1
                        freed_space += size
                    except Exception as e:
                        print(f"   {Colors.RED}✗{Colors.ENDC} Error removing {filepath}: {e}")

        # Remove __pycache__ directories
        for root, dirs, files in os.walk(self.workspace_root):
            if '__pycache__' in dirs:
                pycache_path = Path(root) / '__pycache__'
                try:
                    if dry_run:
                        print(f"   Would remove: {pycache_path}")
                    else:
                        shutil.rmtree(pycache_path)
                        print(f"   {Colors.GREEN}✓{Colors.ENDC} Removed: {pycache_path}")
                    removed_count += 1
                except Exception as e:
                    print(f"   {Colors.RED}✗{Colors.ENDC} Error: {e}")

        print(f"\n{Colors.CYAN}Summary:{Colors.ENDC}")
        print(f"   Items removed: {removed_count}")
        print(f"   Space freed: {self._format_size(freed_space)}")
        if dry_run:
            print(f"\n   {Colors.YELLOW}DRY RUN - No files were actually removed{Colors.ENDC}")
            print(f"   Run without --dry-run to actually remove files")

    def dedupe(self, interactive: bool = True):
        """Find and handle duplicate files"""
        print(f"{Colors.HEADER}🔄 Duplicate Detection{Colors.ENDC}\n")

        duplicates = defaultdict(list)

        for root, dirs, files in os.walk(self.workspace_root):
            dirs[:] = [d for d in dirs if d not in self.config['skip_dirs']]

            for file in files:
                if file.startswith('.'):
                    continue

                filepath = Path(root) / file
                try:
                    # Only hash files < 10MB
                    if filepath.stat().st_size < 10 * 1024 * 1024:
                        file_hash = self._hash_file(filepath)
                        if file_hash:
                            duplicates[file_hash].append(filepath)
                except:
                    continue

        # Filter to only groups with duplicates
        duplicate_groups = {k: v for k, v in duplicates.items() if len(v) > 1}

        if not duplicate_groups:
            print(f"   {Colors.GREEN}No duplicates found!{Colors.ENDC}")
            return

        print(f"Found {len(duplicate_groups)} duplicate file groups\n")

        total_savings = 0
        for hash_val, files in duplicate_groups.items():
            file_size = files[0].stat().st_size
            savings = file_size * (len(files) - 1)
            total_savings += savings

            print(f"{Colors.CYAN}Duplicate group ({len(files)} files, {self._format_size(file_size)} each):{Colors.ENDC}")
            for f in files:
                print(f"   - {f.relative_to(self.workspace_root)}")
            print(f"   Potential savings: {Colors.YELLOW}{self._format_size(savings)}{Colors.ENDC}\n")

        print(f"{Colors.BOLD}Total potential savings: {self._format_size(total_savings)}{Colors.ENDC}\n")

        if interactive:
            print(f"{Colors.YELLOW}💡 Tip: Review duplicates manually before deleting{Colors.ENDC}")
            print(f"   Consider keeping files in different locations if they serve different purposes")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description='AVATARARTS Organization Suite - Unified workspace management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s analyze              # Analyze workspace structure
  %(prog)s cleanup              # Remove temp files (dry run)
  %(prog)s cleanup --execute    # Actually remove temp files
  %(prog)s dedupe               # Find duplicate files
  %(prog)s organize             # Context-aware organization
        """
    )

    parser.add_argument('command',
                       choices=['analyze', 'cleanup', 'dedupe', 'organize', 'archive'],
                       help='Command to execute')
    parser.add_argument('--execute', action='store_true',
                       help='Execute changes (default is dry run for cleanup)')
    parser.add_argument('--dir', type=Path,
                       help='Directory to operate on (default: current)')

    args = parser.parse_args()

    # Initialize organizer
    workspace = args.dir or Path.cwd()
    organizer = AvatarArtsOrganizer(workspace)

    # Execute command
    if args.command == 'analyze':
        organizer.analyze()
    elif args.command == 'cleanup':
        organizer.cleanup(dry_run=not args.execute)
    elif args.command == 'dedupe':
        organizer.dedupe()
    elif args.command == 'organize':
        print(f"{Colors.YELLOW}Organization mode coming soon!{Colors.ENDC}")
        print("Will implement context-aware file organization based on your existing scripts")
    elif args.command == 'archive':
        print(f"{Colors.YELLOW}Archive mode coming soon!{Colors.ENDC}")
        print("Will auto-archive old analysis files")


if __name__ == '__main__':
    main()
