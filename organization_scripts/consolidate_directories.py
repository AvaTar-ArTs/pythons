#!/usr/bin/env python3
"""
Analyze and consolidate directories to reduce directory count
Identify merge opportunities and flatten structure where possible
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict
import json

def analyze_directories(root_dir):
    """Analyze directory structure and find consolidation opportunities"""
    root = Path(root_dir)

    print("🔍 ANALYZING DIRECTORY STRUCTURE")
    print("=" * 70)

    dir_info = {}
    file_counts = {}
    small_dirs = []
    nested_dirs = []
    similar_names = defaultdict(list)

    # Walk through all directories
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip .git and __pycache__
        dirnames[:] = [d for d in dirnames if d not in ('.git', '__pycache__', '.vscode', '.github')]

        dir_path = Path(dirpath)
        rel_path = dir_path.relative_to(root)
        depth = len(rel_path.parts)

        # Count files in this directory (direct children only)
        file_count = len(filenames)

        # Count total files in subtree
        total_files = 0
        for subdir, _, subfiles in os.walk(dir_path):
            total_files += len(subfiles)

        dir_info[str(rel_path)] = {
            'path': dir_path,
            'relative': str(rel_path),
            'depth': depth,
            'direct_files': file_count,
            'total_files': total_files,
            'subdirs': len(dirnames)
        }

        file_counts[str(rel_path)] = total_files

        # Identify small directories (< 10 files)
        if total_files < 10 and depth > 0:
            small_dirs.append({
                'path': dir_path,
                'relative': str(rel_path),
                'files': total_files,
                'depth': depth,
                'parent': str(rel_path.parent)
            })

        # Track nested directories (depth > 3)
        if depth > 3:
            nested_dirs.append({
                'path': dir_path,
                'relative': str(rel_path),
                'depth': depth,
                'files': total_files
            })

        # Track similar directory names
        if dir_path.name:
            similar_names[dir_path.name.lower()].append({
                'path': dir_path,
                'relative': str(rel_path),
                'files': total_files,
                'depth': depth
            })

    # Find similar names with multiple occurrences
    similar_groups = {name: dirs for name, dirs in similar_names.items()
                     if len(dirs) > 1 and len(name) > 2}

    return {
        'dir_info': dir_info,
        'file_counts': file_counts,
        'small_dirs': small_dirs,
        'nested_dirs': nested_dirs,
        'similar_groups': similar_groups,
        'total_dirs': len(dir_info)
    }

def find_consolidation_opportunities(analysis, root_dir):
    """Find specific consolidation opportunities"""
    root = Path(root_dir)

    print("\n💡 CONSOLIDATION OPPORTUNITIES")
    print("=" * 70)

    opportunities = []

    # 1. Small directories (< 5 files) that could be merged into parent
    small_dirs = analysis['small_dirs']
    small_mergeable = [d for d in small_dirs if d['files'] < 5 and d['depth'] > 1]

    print(f"\n📁 Small Directories (< 5 files): {len(small_mergeable)}")

    # Group by parent
    by_parent = defaultdict(list)
    for dir_info in small_mergeable:
        parent = dir_info['parent']
        if parent != '.':
            by_parent[parent].append(dir_info)

    # Suggest merging small dirs into their parent
    merge_into_parent = []
    for parent, dirs in by_parent.items():
        total_files = sum(d['files'] for d in dirs)
        if total_files < 20:  # If combined would still be manageable
            merge_into_parent.append({
                'type': 'merge_into_parent',
                'parent': parent,
                'dirs': dirs,
                'total_files': total_files
            })

    opportunities.extend(merge_into_parent)

    # 2. Similar-named directories that could be merged
    similar_groups = analysis['similar_groups']
    merge_similar = []

    for name, dirs in list(similar_groups.items())[:50]:
        if len(dirs) > 1:
            # Filter to directories at similar depth levels
            dirs_by_depth = defaultdict(list)
            for d in dirs:
                dirs_by_depth[d['depth']].append(d)

            # Merge directories at the same depth level
            for depth, depth_dirs in dirs_by_depth.items():
                if len(depth_dirs) > 1:
                    total_files = sum(d['files'] for d in depth_dirs)
                    if total_files < 100:  # Reasonable merge size
                        # Pick the one with most files as target
                        target = max(depth_dirs, key=lambda x: x['files'])
                        sources = [d for d in depth_dirs if d != target]

                        merge_similar.append({
                            'type': 'merge_similar_names',
                            'target': target,
                            'sources': sources,
                            'name': name,
                            'total_files': total_files
                        })

    opportunities.extend(merge_similar)

    # 3. Deeply nested directories that could be flattened
    nested_dirs = analysis['nested_dirs']
    flatten_candidates = [d for d in nested_dirs if d['depth'] > 4 and d['files'] < 20]

    print(f"\n📂 Deeply Nested Directories (depth > 4, < 20 files): {len(flatten_candidates)}")

    # Group by root-level ancestor
    flatten_ops = []
    for dir_info in flatten_candidates[:50]:  # Limit to 50
        parts = Path(dir_info['relative']).parts
        if len(parts) > 4:
            # Suggest moving to depth 2-3
            new_parts = parts[:2] + parts[-2:]  # Keep first 2 and last 2
            flatten_ops.append({
                'type': 'flatten',
                'current': dir_info,
                'suggested': '/'.join(new_parts)
            })

    return opportunities + flatten_ops

def consolidate_small_dirs(root_dir, opportunities, dry_run=True):
    """Consolidate small directories into their parents"""
    root = Path(root_dir)

    print("\n📦 CONSOLIDATING SMALL DIRECTORIES")
    print("-" * 70)

    merged_count = 0
    files_moved = 0
    errors = 0

    for opp in opportunities:
        if opp['type'] != 'merge_into_parent':
            continue

        parent_path = root / opp['parent']
        if not parent_path.exists():
            continue

        print(f"\n📁 Merging into {opp['parent']}/")

        for dir_info in opp['dirs'][:10]:  # Limit per parent
            source_dir = dir_info['path']
            if not source_dir.exists():
                continue

            try:
                # Move all files from source to parent
                moved = 0
                for item in source_dir.rglob("*"):
                    if item.is_file():
                        rel_to_source = item.relative_to(source_dir)
                        dest = parent_path / rel_to_source

                        # Handle name conflicts
                        if dest.exists():
                            # Skip if identical, otherwise version
                            if dest.stat().st_size == item.stat().st_size:
                                continue
                            base = dest.stem
                            ext = dest.suffix
                            counter = 1
                            while dest.exists():
                                dest = parent_path / f"{base}_{counter}{ext}"
                                counter += 1

                        dest.parent.mkdir(parents=True, exist_ok=True)

                        if not dry_run:
                            shutil.move(str(item), str(dest))
                        moved += 1

                if moved > 0:
                    files_moved += moved
                    print(f"   ✅ {source_dir.name}/ → {moved} files moved")

                    # Remove empty source directory
                    if not dry_run:
                        try:
                            source_dir.rmdir()
                        except:
                            # Not empty yet, try to remove files first
                            for item in source_dir.rglob("*"):
                                if item.is_file():
                                    item.unlink()
                            # Try again
                            for item in reversed(list(source_dir.rglob("*"))):
                                if item.is_dir():
                                    try:
                                        item.rmdir()
                                    except:
                                        pass
                            try:
                                source_dir.rmdir()
                            except:
                                pass

                    merged_count += 1

            except Exception as e:
                errors += 1
                if errors <= 5:
                    print(f"   ⚠️  Error: {e}")

    print(f"\n   Merged: {merged_count} directories")
    print(f"   Files moved: {files_moved}")
    print(f"   Errors: {errors}")

    return merged_count, files_moved

def consolidate_similar_names(root_dir, opportunities, dry_run=True):
    """Consolidate directories with similar names"""
    root = Path(root_dir)

    print("\n🔄 CONSOLIDATING SIMILAR-NAMED DIRECTORIES")
    print("-" * 70)

    merged_count = 0
    errors = 0

    for opp in opportunities:
        if opp['type'] != 'merge_similar_names':
            continue

        target_dir = root / Path(opp['target']['relative'])
        if not target_dir.exists():
            target_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n📁 Merging into {opp['target']['relative']}/")

        for source_info in opp['sources'][:5]:  # Limit per group
            source_dir = root / Path(source_info['relative'])
            if not source_dir.exists() or source_dir == target_dir:
                continue

            try:
                # Move all files
                moved = 0
                for item in source_dir.rglob("*"):
                    if item.is_file():
                        rel_to_source = item.relative_to(source_dir)
                        dest = target_dir / rel_to_source

                        if dest.exists():
                            if dest.stat().st_size == item.stat().st_size:
                                continue
                            base = dest.stem
                            ext = dest.suffix
                            counter = 1
                            while dest.exists():
                                dest = target_dir / f"{base}_{counter}{ext}"
                                counter += 1

                        dest.parent.mkdir(parents=True, exist_ok=True)

                        if not dry_run:
                            shutil.move(str(item), str(dest))
                        moved += 1

                if moved > 0:
                    print(f"   ✅ {source_info['relative']} → {moved} files")
                    merged_count += 1

                    # Remove source
                    if not dry_run:
                        try:
                            shutil.rmtree(source_dir)
                        except:
                            pass

            except Exception as e:
                errors += 1
                if errors <= 5:
                    print(f"   ⚠️  Error: {e}")

    print(f"\n   Merged: {merged_count} directories")
    print(f"   Errors: {errors}")

    return merged_count

def main():
    """Main execution"""
    import sys

    root_dir = sys.argv[1] if len(sys.argv) > 1 else "/Users/steven/pythons"
    dry_run = "--execute" not in sys.argv

    print("🚀 DIRECTORY CONSOLIDATION")
    print("=" * 70)
    print(f"Directory: {root_dir}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print()

    # Analyze
    analysis = analyze_directories(root_dir)

    print(f"\n📊 Current State:")
    print(f"   Total directories: {analysis['total_dirs']:,}")
    print(f"   Small directories (< 5 files): {len(analysis['small_dirs']):,}")
    print(f"   Deeply nested (depth > 4): {len(analysis['nested_dirs']):,}")
    print(f"   Similar-named groups: {len(analysis['similar_groups'])}")

    # Find opportunities
    opportunities = find_consolidation_opportunities(analysis, root_dir)

    print(f"\n💡 Found {len(opportunities)} consolidation opportunities")

    # Consolidate small dirs
    merge_parent_ops = [o for o in opportunities if o['type'] == 'merge_into_parent']
    if merge_parent_ops:
        consolidate_small_dirs(root_dir, merge_parent_ops, dry_run)

    # Consolidate similar names
    merge_similar_ops = [o for o in opportunities if o['type'] == 'merge_similar_names']
    if merge_similar_ops:
        consolidate_similar_names(root_dir, merge_similar_ops, dry_run)

    # Count final directories
    if not dry_run:
        final_count = len([d for d in Path(root_dir).rglob("*") if d.is_dir()])
        print(f"\n📊 Final directory count: {final_count:,}")
    else:
        print(f"\n💡 Run with --execute to perform consolidation")

    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()

