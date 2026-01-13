#!/usr/bin/env python3
"""
Aggressive directory consolidation - reduce directory count significantly
Flatten deep structures, merge small dirs, remove unnecessary nesting
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict

def analyze_and_flatten(root_dir, dry_run=True):
    """Aggressively flatten and consolidate directories"""
    root = Path(root_dir)

    print("🚀 AGGRESSIVE DIRECTORY CONSOLIDATION")
    print("=" * 70)
    print(f"Directory: {root_dir}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print()

    # Step 1: Find all directories at depth > 5 and flatten them
    print("📂 Step 1: Flattening Deep Structures (depth > 5)")
    print("-" * 70)

    deep_dirs = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ('.git', '__pycache__', '.vscode')]
        dir_path = Path(dirpath)
        rel_path = dir_path.relative_to(root)
        depth = len(rel_path.parts)

        if depth > 5:
            file_count = len([f for f in (dir_path / fn for fn in filenames) if Path(f).exists()])
            if file_count > 0:
                deep_dirs.append({
                    'path': dir_path,
                    'relative': str(rel_path),
                    'depth': depth,
                    'files': file_count
                })

    print(f"   Found {len(deep_dirs)} directories at depth > 5")

    # Flatten by moving to depth 3
    flattened = 0
    for dir_info in deep_dirs[:200]:  # Limit to 200
        source = dir_info['path']
        rel = Path(dir_info['relative'])

        # Create new path at depth 3
        parts = rel.parts
        if len(parts) > 3:
            # Keep first 2 levels, then combine rest into directory name
            new_parts = parts[:2] + ('_'.join(parts[2:]),)
            target = root / Path(*new_parts)

            if source.exists() and source != target and not target.exists():
                try:
                    if not dry_run:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(source), str(target))
                    flattened += 1
                    if flattened <= 20:
                        print(f"   ✅ {rel} → {Path(*new_parts)}")
                except Exception as e:
                    if flattened <= 5:
                        print(f"   ⚠️  Error: {e}")

    print(f"   Flattened: {flattened} directories")
    print()

    # Step 2: Merge small directories (< 3 files) into parent
    print("📦 Step 2: Merging Small Directories (< 3 files)")
    print("-" * 70)

    small_dirs = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ('.git', '__pycache__', '.vscode')]
        dir_path = Path(dirpath)
        rel_path = dir_path.relative_to(root)
        depth = len(rel_path.parts)

        # Count direct files only
        file_count = len(filenames)

        if file_count < 3 and file_count > 0 and depth > 1:
            small_dirs.append({
                'path': dir_path,
                'relative': str(rel_path),
                'files': file_count,
                'parent': dir_path.parent,
                'depth': depth
            })

    print(f"   Found {len(small_dirs)} small directories")

    # Group by parent
    by_parent = defaultdict(list)
    for dir_info in small_dirs:
        parent_str = str(dir_info['parent'].relative_to(root))
        by_parent[parent_str].append(dir_info)

    merged = 0
    for parent_str, dirs in list(by_parent.items())[:100]:  # Limit
        parent_path = root / parent_str
        if not parent_path.exists():
            continue

        for dir_info in dirs[:5]:  # Limit per parent
            source = dir_info['path']
            if not source.exists():
                continue

            try:
                moved = 0
                for item in source.iterdir():
                    if item.is_file():
                        dest = parent_path / item.name
                        if dest.exists():
                            # Skip if identical
                            if dest.stat().st_size == item.stat().st_size:
                                item.unlink()
                                continue
                            # Version the filename
                            base = dest.stem
                            ext = dest.suffix
                            counter = 1
                            while dest.exists():
                                dest = parent_path / f"{base}_{counter}{ext}"
                                counter += 1

                        if not dry_run:
                            shutil.move(str(item), str(dest))
                        moved += 1
                    elif item.is_dir():
                        # Move subdirectory
                        dest = parent_path / item.name
                        if not dest.exists():
                            if not dry_run:
                                shutil.move(str(item), str(dest))
                            moved += 1

                if moved > 0:
                    merged += 1
                    if merged <= 20:
                        print(f"   ✅ {dir_info['relative']} → {parent_str} ({moved} items)")

                    # Remove empty source
                    if not dry_run:
                        try:
                            source.rmdir()
                        except:
                            pass
            except Exception as e:
                if merged <= 5:
                    print(f"   ⚠️  Error: {e}")

    print(f"   Merged: {merged} directories")
    print()

    # Step 3: Remove empty directories
    print("🗑️  Step 3: Removing Empty Directories")
    print("-" * 70)

    removed = 0
    # Bottom-up traversal
    all_dirs = []
    for dirpath, dirnames, filenames in os.walk(root):
        dir_path = Path(dirpath)
        all_dirs.append(dir_path)

    # Sort by depth descending
    all_dirs.sort(key=lambda p: len(p.relative_to(root).parts), reverse=True)

    for dir_path in all_dirs:
        if dir_path == root:
            continue
        try:
            if not any(dir_path.iterdir()):  # Empty
                if not dry_run:
                    dir_path.rmdir()
                removed += 1
        except:
            pass

    print(f"   Removed: {removed} empty directories")
    print()

    # Final count
    if not dry_run:
        final_count = len([d for d in root.rglob("*") if d.is_dir()])
        print(f"📊 Final directory count: {final_count:,}")
    else:
        initial_count = len([d for d in root.rglob("*") if d.is_dir()])
        print(f"📊 Current directory count: {initial_count:,}")
        print(f"💡 Estimated reduction: {flattened + merged + removed} directories")

    print("\n✅ Consolidation complete!")

def main():
    """Main execution"""
    import sys

    root_dir = sys.argv[1] if len(sys.argv) > 1 else "/Users/steven/pythons"
    dry_run = "--execute" not in sys.argv

    analyze_and_flatten(root_dir, dry_run)

if __name__ == "__main__":
    main()

