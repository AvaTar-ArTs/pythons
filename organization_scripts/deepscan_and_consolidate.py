#!/usr/bin/env python3
"""
Deep scan all folders at unlimited depth
Analyze structure and consolidate/merge while maintaining parent folder context
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict
import json
import hashlib

def get_file_hash(filepath):
    """Calculate MD5 hash of file"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return None

def analyze_directory_structure(root_dir):
    """Deep scan and analyze directory structure"""
    root = Path(root_dir)

    print("🔍 DEEP SCAN - Unlimited Depth Analysis")
    print("=" * 70)
    print(f"Scanning: {root}")
    print()

    file_map = defaultdict(list)  # hash -> list of files
    dir_structure = defaultdict(list)  # parent_dir -> list of subdirs
    file_stats = defaultdict(int)  # extension -> count

    total_files = 0
    total_dirs = 0

    print("📊 Scanning all directories and files...")

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip .git and __pycache__
        dirnames[:] = [d for d in dirnames if d not in ('.git', '__pycache__')]

        dir_path = Path(dirpath)
        total_dirs += 1

        for filename in filenames:
            if filename.startswith('.'):
                continue

            file_path = dir_path / filename
            total_files += 1

            # Get file info
            try:
                stat = file_path.stat()
                size = stat.st_size
                ext = file_path.suffix.lower()

                file_stats[ext] += 1

                # Calculate hash for duplicate detection
                file_hash = get_file_hash(file_path)
                if file_hash:
                    rel_path = file_path.relative_to(root)
                    file_map[file_hash].append({
                        'path': file_path,
                        'relative': str(rel_path),
                        'size': size,
                        'ext': ext,
                        'parent': str(rel_path.parent)
                    })

                # Track directory structure
                parent = str(rel_path.parent)
                dir_structure[parent].append(str(rel_path))

            except Exception:
                continue

        if total_files % 1000 == 0:
            print(f"   Scanned {total_files:,} files, {total_dirs:,} directories...")

    print(f"\n✅ Scan complete!")
    print(f"   Total files: {total_files:,}")
    print(f"   Total directories: {total_dirs:,}")
    print(f"   Unique file hashes: {len(file_map):,}")

    # Find duplicates
    duplicates = {h: files for h, files in file_map.items() if len(files) > 1}

    print(f"   Duplicate files: {sum(len(files) - 1 for files in duplicates.values())}")
    print()

    return {
        'file_map': dict(file_map),
        'duplicates': dict(duplicates),
        'dir_structure': dict(dir_structure),
        'file_stats': dict(file_stats),
        'total_files': total_files,
        'total_dirs': total_dirs
    }

def find_consolidation_opportunities(analysis, root_dir):
    """Find opportunities to consolidate directories"""
    root = Path(root_dir)

    print("💡 CONSOLIDATION OPPORTUNITIES")
    print("=" * 70)

    opportunities = []

    # 1. Find duplicate files (keep one, remove others)
    duplicates = analysis['duplicates']
    if duplicates:
        print(f"\n📋 Duplicate Files: {len(duplicates)} sets")
        duplicate_ops = []
        for file_hash, files in list(duplicates.items())[:20]:
            # Keep the one with shortest path
            files_sorted = sorted(files, key=lambda x: (len(x['relative'].split(os.sep)), x['relative']))
            keep = files_sorted[0]
            remove = files_sorted[1:]

            duplicate_ops.append({
                'type': 'remove_duplicate',
                'keep': keep['path'],
                'remove': [f['path'] for f in remove],
                'count': len(remove)
            })

        opportunities.extend(duplicate_ops)
        print(f"   Found {len(duplicate_ops)} duplicate sets to consolidate")

    # 2. Find similar directory names that could be merged
    dir_structure = analysis['dir_structure']
    dir_names = defaultdict(list)

    for parent_dir in dir_structure.keys():
        if parent_dir == '.':
            continue

        # Extract directory names
        parts = parent_dir.split(os.sep)
        for part in parts:
            dir_names[part.lower()].append(parent_dir)

    # Find directories with similar names
    similar_dirs = {name: dirs for name, dirs in dir_names.items() if len(dirs) > 1 and len(name) > 3}

    if similar_dirs:
        print(f"\n📁 Similar Directory Names: {len(similar_dirs)} groups")
        for name, dirs in list(similar_dirs.items())[:10]:
            print(f"   '{name}': {len(dirs)} directories")
            for d in dirs[:3]:
                print(f"      - {d}")
            if len(dirs) > 3:
                print(f"      ... and {len(dirs) - 3} more")

    return opportunities

def consolidate_duplicates(root_dir, duplicates, dry_run=True):
    """Remove duplicate files, keeping the best version"""
    root = Path(root_dir)

    print("\n🗑️  REMOVING DUPLICATE FILES")
    print("-" * 70)

    removed_count = 0
    space_freed = 0
    errors = 0

    for file_hash, files in list(duplicates.items())[:100]:  # Limit to 100 sets for performance
        # Sort by path length (prefer shorter, simpler paths)
        files_sorted = sorted(files, key=lambda x: (len(x['relative'].split(os.sep)), x['relative']))
        keep = files_sorted[0]
        remove = files_sorted[1:]

        for file_info in remove:
            file_path = file_info['path']

            if file_path.exists():
                try:
                    size = file_info['size']
                    if not dry_run:
                        file_path.unlink()
                    removed_count += 1
                    space_freed += size
                    if removed_count <= 20:
                        print(f"   ❌ Removed: {file_info['relative']}")
                except Exception as e:
                    errors += 1
                    if errors <= 5:
                        print(f"   ⚠️  Error removing {file_info['relative']}: {e}")

    print(f"\n   Removed: {removed_count} duplicate files")
    print(f"   Space freed: {space_freed / (1024*1024):.2f} MB")
    print(f"   Errors: {errors}")

    return removed_count, space_freed

def generate_report(analysis, output_file):
    """Generate analysis report"""
    report_file = Path(output_file)

    report_data = {
        'summary': {
            'total_files': analysis['total_files'],
            'total_directories': analysis['total_dirs'],
            'unique_files': len(analysis['file_map']),
            'duplicate_sets': len(analysis['duplicates']),
            'total_duplicates': sum(len(files) - 1 for files in analysis['duplicates'].values())
        },
        'file_statistics': analysis['file_stats'],
        'top_duplicates': {
            h: [f['relative'] for f in files[:5]]
            for h, files in list(analysis['duplicates'].items())[:50]
        }
    }

    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2, default=str)

    print(f"\n💾 Report saved to: {report_file}")

def main():
    """Main execution"""
    import sys

    root_dir = sys.argv[1] if len(sys.argv) > 1 else "/Users/steven/pythons"
    dry_run = "--execute" not in sys.argv

    print("🚀 DEEP SCAN & CONSOLIDATION")
    print("=" * 70)
    print(f"Directory: {root_dir}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print()

    # Analyze structure
    analysis = analyze_directory_structure(root_dir)

    # Find opportunities
    opportunities = find_consolidation_opportunities(analysis, root_dir)

    # Remove duplicates
    if analysis['duplicates']:
        consolidate_duplicates(root_dir, analysis['duplicates'], dry_run)

    # Generate report
    report_file = Path.home() / "deepscan_analysis.json"
    generate_report(analysis, report_file)

    print("\n" + "=" * 70)
    print("✅ Analysis Complete!")

    if dry_run:
        print("\n💡 Run with --execute to perform consolidation")
    else:
        print("\n✅ Consolidation complete!")

if __name__ == "__main__":
    main()

