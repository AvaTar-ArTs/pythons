#!/usr/bin/env python3
"""
Backup File Cleaner
Removes backup files (*.bak, *.backup, *_backup*) from project directories
while preserving system files and intentional backups.
"""

import os
import sys
from pathlib import Path
from collections import defaultdict
import argparse

# Directories to exclude (system files, intentional backups)
EXCLUDE_DIRS = {
    'Library',
    'Movies',
    'Downloads',
    '.cache',
    '.npm',
    '.m2',
    '.gradle',
    '.gem',
    '.bundle',
    '.composer',
    '.local',
    '.oh-my-zsh',
    '.nvm',
    '.rustup',
    '.dotnet',
    '.aspnet',
    '.x-cmd.root',
    '.cursor',
    '.claude',
    '.gemini',
    '.grok',
    '.qwen',
    '.apify',
    '.boltai',
    '.iterm2',
    '.jupyter',
    '.ipython',
    '.mplayer',
    '.putty',
    '.raycast',
    '.spicetify',
    '.spotdl',
    '.ssh',
    '.streamlit',
    '.u2net',
    '.warp',
    '.zsh',
    '.zsh_sessions',
    '.zshrc',
    '.zshrc_archive',
    '.zshrc_env_perm_check',
    '.zshrcd',
    '.zshrce',
    'node_modules',
    '__pycache__',
    '.git',
    '.venv',
    'venv',
    '.env',
}

# Directories that contain intentional backups (keep these)
INTENTIONAL_BACKUP_DIRS = {
    '.env.d/backups',
    '.env.d/archived',
    'AVATARARTS/archive/backups',
    '.package_manager_backup',
    'Library/Mobile Documents',  # iCloud backups
}

# File patterns to remove
BACKUP_PATTERNS = [
    '*.bak',
    '*.bak*',  # .bak1, .bak2, etc.
    '*.backup',
    '*.backup*',
    '*_backup',
    '*_backup*',
    '*.bak_*',  # .bak_20251125 format
]

def should_exclude_path(path: Path) -> bool:
    """Check if a path should be excluded from cleanup."""
    path_str = str(path)
    
    # Check if in exclude directory
    for exclude_dir in EXCLUDE_DIRS:
        if exclude_dir in path.parts:
            return True
    
    # Check if in intentional backup directory
    for backup_dir in INTENTIONAL_BACKUP_DIRS:
        if backup_dir in path_str:
            return True
    
    # Exclude hidden files in home directory root
    if path.parent == Path.home() and path.name.startswith('.'):
        # But allow project backup files
        if any(pattern.replace('*', '') in path.name for pattern in BACKUP_PATTERNS):
            return False
        return True
    
    return False

def is_backup_file(path: Path) -> bool:
    """Check if a file matches backup patterns."""
    name = path.name.lower()
    
    # Check patterns
    if name.endswith('.bak'):
        return True
    if '.bak' in name and any(char.isdigit() for char in name.split('.bak')[-1].split('.')[0][:5]):
        return True  # .bak1, .bak2, .bak2025, etc.
    if name.endswith('.backup'):
        return True
    if name.endswith('_backup'):
        return True
    if '_backup' in name:
        return True
    if '.backup.' in name:
        return True
    
    return False

def find_backup_files(root_dir: Path, dry_run: bool = True) -> list:
    """Find all backup files in project directories."""
    backup_files = []
    stats = defaultdict(int)
    
    print(f"Scanning for backup files in: {root_dir}")
    print(f"Excluding: {', '.join(sorted(EXCLUDE_DIRS))[:100]}...")
    print()
    
    for root, dirs, files in os.walk(root_dir):
        # Skip excluded directories
        root_path = Path(root)
        if should_exclude_path(root_path):
            dirs[:] = []  # Don't descend into excluded dirs
            continue
        
        # Remove excluded dirs from dirs list to avoid descending
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.') or d in ['.git', '.venv']]
        
        for file in files:
            file_path = root_path / file
            
            # Skip excluded paths
            if should_exclude_path(file_path):
                continue
            
            # Check if it's a backup file
            if is_backup_file(file_path):
                backup_files.append(file_path)
                stats[file_path.suffix or 'no_ext'] += 1
    
    return backup_files, stats

def remove_backup_files(backup_files: list, dry_run: bool = True) -> dict:
    """Remove backup files."""
    results = {
        'removed': 0,
        'failed': 0,
        'total_size': 0,
        'errors': []
    }
    
    for file_path in backup_files:
        try:
            file_size = file_path.stat().st_size
            results['total_size'] += file_size
            
            if not dry_run:
                file_path.unlink()
                results['removed'] += 1
                print(f"  ✓ Removed: {file_path}")
            else:
                results['removed'] += 1
                print(f"  [DRY RUN] Would remove: {file_path} ({file_size:,} bytes)")
        except Exception as e:
            results['failed'] += 1
            results['errors'].append((str(file_path), str(e)))
            print(f"  ✗ Error removing {file_path}: {e}")
    
    return results

def format_size(size: int) -> str:
    """Format bytes to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"

def main():
    parser = argparse.ArgumentParser(
        description='Remove backup files from project directories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (preview what would be removed)
  python cleanup_backup_files.py --dry-run
  
  # Actually remove backup files
  python cleanup_backup_files.py
  
  # Scan specific directory
  python cleanup_backup_files.py --dir pythons --dry-run
        """
    )
    parser.add_argument('--dir', type=Path, default=Path.home(),
                       help='Directory to scan (default: home directory)')
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Preview changes without removing files (default: True)')
    parser.add_argument('--execute', action='store_true',
                       help='Actually remove files (overrides --dry-run)')
    
    args = parser.parse_args()
    
    dry_run = not args.execute if args.execute else args.dry_run
    
    if not dry_run:
        response = input("⚠️  This will permanently delete backup files. Continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled.")
            return
    
    print("=" * 70)
    print("BACKUP FILE CLEANER")
    print("=" * 70)
    print(f"Mode: {'DRY RUN (preview only)' if dry_run else 'EXECUTE (will delete files)'}")
    print()
    
    # Find backup files
    backup_files, stats = find_backup_files(args.dir, dry_run)
    
    if not backup_files:
        print("✓ No backup files found in project directories.")
        return
    
    print(f"\nFound {len(backup_files)} backup files to remove:")
    print("\nBreakdown by extension:")
    for ext, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {ext:20s}: {count:4d} files")
    
    print(f"\n{'Preview:' if dry_run else 'Removing files...'}")
    print("-" * 70)
    
    # Remove files
    results = remove_backup_files(backup_files, dry_run)
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Files {'would be' if dry_run else ''} removed: {results['removed']}")
    print(f"Failed: {results['failed']}")
    print(f"Total size: {format_size(results['total_size'])}")
    
    if results['errors']:
        print(f"\nErrors ({len(results['errors'])}):")
        for path, error in results['errors'][:10]:
            print(f"  {path}: {error}")
        if len(results['errors']) > 10:
            print(f"  ... and {len(results['errors']) - 10} more errors")
    
    if dry_run:
        print("\n💡 Run with --execute to actually remove these files")
    else:
        print("\n✅ Cleanup complete!")

if __name__ == '__main__':
    main()
