#!/usr/bin/env python3
"""
Pythons Consolidation Script
Analyzes and consolidates pythons and pythons-sort directories.

This script:
1. Analyzes the relationship between pythons and pythons-sort
2. Identifies unique files in pythons-sort
3. Provides options to merge or archive pythons-sort
"""

import os
import json
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import argparse

def get_file_hash(file_path: Path, sample_size: int = 8192) -> str:
    """Compute file hash (first 8KB for speed)."""
    try:
        import hashlib
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            hasher.update(f.read(sample_size))
        return hasher.hexdigest()
    except:
        return 'error'

def scan_directory(directory: Path) -> dict:
    """Scan a directory and return file information."""
    files = {}
    stats = {
        'total_files': 0,
        'total_size': 0,
        'by_extension': defaultdict(int),
        'python_files': 0,
    }
    
    if not directory.exists():
        return {'error': 'Directory not found', 'files': {}, 'stats': stats}
    
    for root, dirs, filenames in os.walk(directory):
        # Skip hidden and cache directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and
                  d not in ['__pycache__', 'node_modules', 'venv', '.venv']]
        
        for filename in filenames:
            if filename.startswith('.'):
                continue
            
            file_path = Path(root) / filename
            try:
                file_stat = file_path.stat()
                file_size = file_stat.st_size
                rel_path = file_path.relative_to(directory)
                
                file_hash = get_file_hash(file_path)
                
                file_info = {
                    'path': str(file_path),
                    'rel_path': str(rel_path),
                    'name': filename,
                    'size': file_size,
                    'hash': file_hash,
                    'extension': file_path.suffix.lower() or 'no_ext',
                }
                
                files[str(rel_path)] = file_info
                stats['total_files'] += 1
                stats['total_size'] += file_size
                stats['by_extension'][file_info['extension']] += 1
                
                if file_info['extension'] == '.py':
                    stats['python_files'] += 1
                    
            except (PermissionError, OSError) as e:
                print(f"  ⚠️  Error accessing {file_path}: {e}")
    
    return {'files': files, 'stats': stats}

def compare_directories(pythons_dir: Path, pythons_sort_dir: Path) -> dict:
    """Compare two directories and find differences."""
    print("Scanning pythons directory...")
    pythons_data = scan_directory(pythons_dir)
    
    print("Scanning pythons-sort directory...")
    pythons_sort_data = scan_directory(pythons_sort_dir)
    
    if 'error' in pythons_data or 'error' in pythons_sort_data:
        return {'error': 'One or both directories not found'}
    
    pythons_files = pythons_data['files']
    pythons_sort_files = pythons_sort_data['files']
    
    # Find files by hash
    pythons_hashes = {info['hash']: info for info in pythons_files.values() if info['hash'] != 'error'}
    pythons_sort_hashes = {info['hash']: info for info in pythons_sort_files.values() if info['hash'] != 'error'}
    
    # Find common files (same hash)
    common_hashes = set(pythons_hashes.keys()) & set(pythons_sort_hashes.keys())
    
    # Find unique files in pythons-sort
    unique_pythons_sort_hashes = set(pythons_sort_hashes.keys()) - set(pythons_hashes.keys())
    unique_pythons_sort_files = [pythons_sort_hashes[h] for h in unique_pythons_sort_hashes]
    
    # Find unique files in pythons
    unique_pythons_hashes = set(pythons_hashes.keys()) - set(pythons_sort_hashes.keys())
    
    comparison = {
        'pythons': {
            'stats': pythons_data['stats'],
            'total_files': len(pythons_files),
            'unique_files': len(unique_pythons_hashes),
        },
        'pythons_sort': {
            'stats': pythons_sort_data['stats'],
            'total_files': len(pythons_sort_files),
            'unique_files': len(unique_pythons_sort_hashes),
        },
        'common': {
            'count': len(common_hashes),
            'files': [pythons_sort_hashes[h]['rel_path'] for h in list(common_hashes)[:20]]
        },
        'unique_in_pythons_sort': {
            'count': len(unique_pythons_sort_files),
            'files': [f['rel_path'] for f in unique_pythons_sort_files[:50]]
        }
    }
    
    return comparison

def format_size(size: int) -> str:
    """Format bytes to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def archive_pythons_sort(pythons_sort_dir: Path, archive_dir: Path) -> bool:
    """Archive pythons-sort directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = archive_dir / f"pythons-sort_archived_{timestamp}"
    
    try:
        print(f"Archiving {pythons_sort_dir} to {archive_path}...")
        shutil.move(str(pythons_sort_dir), str(archive_path))
        print(f"✓ Archived to: {archive_path}")
        return True
    except Exception as e:
        print(f"✗ Error archiving: {e}")
        return False

def merge_unique_files(pythons_sort_dir: Path, pythons_dir: Path, unique_files: list, dry_run: bool = True) -> dict:
    """Merge unique files from pythons-sort into pythons."""
    results = {
        'copied': 0,
        'failed': 0,
        'skipped': 0,
        'errors': []
    }
    
    merge_dir = pythons_dir / 'from_pythons_sort'
    if not dry_run:
        merge_dir.mkdir(exist_ok=True)
    
    for file_info in unique_files:
        source_path = Path(file_info['path'])
        rel_path = file_info['rel_path']
        
        # Determine destination
        dest_path = merge_dir / rel_path
        
        try:
            if not dry_run:
                # Create parent directories
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                # Copy file
                shutil.copy2(source_path, dest_path)
                results['copied'] += 1
                print(f"  ✓ Copied: {rel_path}")
            else:
                results['copied'] += 1
                print(f"  [DRY RUN] Would copy: {rel_path} -> {dest_path}")
        except Exception as e:
            results['failed'] += 1
            results['errors'].append((rel_path, str(e)))
            print(f"  ✗ Error copying {rel_path}: {e}")
    
    return results

def main():
    parser = argparse.ArgumentParser(
        description='Analyze and consolidate pythons and pythons-sort directories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze the relationship
  python consolidate_pythons.py --analyze
  
  # Preview merge of unique files
  python consolidate_pythons.py --merge --dry-run
  
  # Actually merge unique files
  python consolidate_pythons.py --merge
  
  # Archive pythons-sort
  python consolidate_pythons.py --archive
        """
    )
    parser.add_argument('--analyze', action='store_true',
                       help='Analyze relationship between directories')
    parser.add_argument('--merge', action='store_true',
                       help='Merge unique files from pythons-sort into pythons')
    parser.add_argument('--archive', action='store_true',
                       help='Archive pythons-sort directory')
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Preview changes without making them (default: True)')
    parser.add_argument('--execute', action='store_true',
                       help='Actually perform operations (overrides --dry-run)')
    parser.add_argument('--pythons-dir', type=Path, default=Path.home() / 'pythons',
                       help='Path to pythons directory')
    parser.add_argument('--pythons-sort-dir', type=Path, default=Path.home() / 'pythons-sort',
                       help='Path to pythons-sort directory')
    parser.add_argument('--archive-dir', type=Path, default=Path.home() / 'archive',
                       help='Path to archive directory')
    
    args = parser.parse_args()
    
    dry_run = not args.execute if args.execute else args.dry_run
    
    # Default to analyze if no action specified
    if not any([args.analyze, args.merge, args.archive]):
        args.analyze = True
    
    print("=" * 70)
    print("PYTHONS CONSOLIDATION TOOL")
    print("=" * 70)
    print()
    
    # Analyze
    if args.analyze:
        print("Analyzing directories...")
        print("-" * 70)
        
        comparison = compare_directories(args.pythons_dir, args.pythons_sort_dir)
        
        if 'error' in comparison:
            print(f"❌ Error: {comparison['error']}")
            return
        
        print("\nCOMPARISON RESULTS:")
        print("=" * 70)
        
        print(f"\n📁 PYTHONS:")
        print(f"  Total files: {comparison['pythons']['total_files']:,}")
        print(f"  Python files: {comparison['pythons']['stats']['python_files']:,}")
        print(f"  Total size: {format_size(comparison['pythons']['stats']['total_size'])}")
        print(f"  Unique files: {comparison['pythons']['unique_files']:,}")
        
        print(f"\n📁 PYTHONS-SORT:")
        print(f"  Total files: {comparison['pythons_sort']['total_files']:,}")
        print(f"  Python files: {comparison['pythons_sort']['stats']['python_files']:,}")
        print(f"  Total size: {format_size(comparison['pythons_sort']['stats']['total_size'])}")
        print(f"  Unique files: {comparison['pythons_sort']['unique_files']:,}")
        
        print(f"\n🔄 COMMON FILES:")
        print(f"  Files with same content: {comparison['common']['count']:,}")
        if comparison['common']['files']:
            print(f"  Examples:")
            for f in comparison['common']['files'][:10]:
                print(f"    - {f}")
        
        print(f"\n✨ UNIQUE IN PYTHONS-SORT:")
        print(f"  Unique files: {comparison['unique_in_pythons_sort']['count']:,}")
        if comparison['unique_in_pythons_sort']['files']:
            print(f"  Examples:")
            for f in comparison['unique_in_pythons_sort']['files'][:20]:
                print(f"    - {f}")
        
        # Save comparison
        output_file = Path.home() / 'analysis' / 'pythons_consolidation_analysis.json'
        output_file.parent.mkdir(exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(comparison, f, indent=2)
        print(f"\n💾 Analysis saved to: {output_file}")
    
    # Merge
    if args.merge:
        print("\n" + "=" * 70)
        print("MERGING UNIQUE FILES")
        print("=" * 70)
        
        # Load comparison if available
        comparison_file = Path.home() / 'analysis' / 'pythons_consolidation_analysis.json'
        if comparison_file.exists():
            with open(comparison_file, 'r') as f:
                comparison = json.load(f)
        else:
            print("Running analysis first...")
            comparison = compare_directories(args.pythons_dir, args.pythons_sort_dir)
        
        unique_files = comparison.get('unique_in_pythons_sort', {}).get('files', [])
        
        if not unique_files:
            print("No unique files to merge.")
            return
        
        # Get full file info for unique files
        pythons_sort_data = scan_directory(args.pythons_sort_dir)
        unique_file_infos = []
        for rel_path in unique_files:
            if rel_path in pythons_sort_data.get('files', {}):
                unique_file_infos.append(pythons_sort_data['files'][rel_path])
        
        print(f"\nFound {len(unique_file_infos)} unique files to merge")
        print(f"Mode: {'DRY RUN (preview only)' if dry_run else 'EXECUTE (will copy files)'}")
        
        if not dry_run:
            response = input("\n⚠️  This will copy files. Continue? (yes/no): ")
            if response.lower() != 'yes':
                print("Cancelled.")
                return
        
        results = merge_unique_files(args.pythons_sort_dir, args.pythons_dir, unique_file_infos, dry_run)
        
        print(f"\n✓ Merged {results['copied']} files")
        if results['failed'] > 0:
            print(f"✗ Failed: {results['failed']} files")
    
    # Archive
    if args.archive:
        print("\n" + "=" * 70)
        print("ARCHIVING PYTHONS-SORT")
        print("=" * 70)
        
        if not dry_run:
            response = input(f"⚠️  This will move {args.pythons_sort_dir} to archive. Continue? (yes/no): ")
            if response.lower() != 'yes':
                print("Cancelled.")
                return
        
        args.archive_dir.mkdir(exist_ok=True)
        success = archive_pythons_sort(args.pythons_sort_dir, args.archive_dir)
        
        if success:
            print("\n✅ Archive complete!")
        else:
            print("\n❌ Archive failed!")

if __name__ == '__main__':
    main()
