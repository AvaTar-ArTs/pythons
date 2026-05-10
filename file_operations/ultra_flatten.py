#!/usr/bin/env python3
"""
Ultra-aggressive directory flattening - reduce directory count significantly
Flatten all structures to max depth 3, merge aggressively
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict


def ultra_flatten(root_dir, dry_run=True):
    """Ultra-aggressive flattening"""
    root = Path(root_dir)

    print("🔥 ULTRA-AGGRESSIVE FLATTENING")
    print("=" * 70)
    print(f"Directory: {root_dir}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print()

    # Step 1: Flatten everything at depth > 3 to depth 3
    print("📂 Step 1: Flattening All Structures (depth > 3 → depth 3)")
    print("-" * 70)

    deep_dirs = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d
            for d in dirnames
            if d not in (".git", "__pycache__", ".vscode", ".github")
        ]
        dir_path = Path(dirpath)
        rel_path = dir_path.relative_to(root)
        depth = len(rel_path.parts)

        if depth > 3:
            # Check if has files or subdirs
            has_content = len(filenames) > 0 or len(dirnames) > 0
            if has_content:
                deep_dirs.append(
                    {
                        "path": dir_path,
                        "relative": str(rel_path),
                        "depth": depth,
                        "files": len(filenames),
                        "subdirs": len(dirnames),
                    }
                )

    print(f"   Found {len(deep_dirs)} directories at depth > 3")

    # Group by top 3 levels for flattening
    flattened = 0
    moved_files = 0

    for dir_info in deep_dirs[:500]:  # Process more
        source = dir_info["path"]
        rel = Path(dir_info["relative"])
        parts = rel.parts

        if len(parts) > 3:
            # Keep first 2 levels, combine rest
            base_path = Path(*parts[:2])
            combined_name = "_".join(parts[2:])
            target_rel = base_path / combined_name
            target = root / target_rel

            if source.exists() and source != target:
                try:
                    # Move all content to target
                    if not target.exists():
                        if not dry_run:
                            target.mkdir(parents=True, exist_ok=True)

                    # Move files and subdirs
                    moved = 0
                    for item in source.iterdir():
                        dest = target / item.name

                        # Handle conflicts
                        if dest.exists():
                            if item.is_file() and dest.is_file():
                                # Skip if identical
                                if item.stat().st_size == dest.stat().st_size:
                                    if not dry_run:
                                        item.unlink()
                                    continue
                            # Version the name
                            base_name = dest.stem
                            ext = dest.suffix if item.is_file() else ""
                            counter = 1
                            while dest.exists():
                                if item.is_file():
                                    dest = target / f"{base_name}_{counter}{ext}"
                                else:
                                    dest = target / f"{item.name}_{counter}"
                                counter += 1

                        if not dry_run:
                            shutil.move(str(item), str(dest))
                        moved += 1

                    if moved > 0:
                        moved_files += moved
                        flattened += 1
                        if flattened <= 30:
                            print(f"   ✅ {rel} → {target_rel} ({moved} items)")

                        # Remove source if empty
                        if not dry_run:
                            try:
                                source.rmdir()
                            except:
                                pass

                except Exception as e:
                    if flattened <= 5:
                        print(f"   ⚠️  Error: {e}")

    print(f"   Flattened: {flattened} directories")
    print(f"   Items moved: {moved_files}")
    print()

    # Step 2: Merge small directories (< 5 files) into parent more aggressively
    print("📦 Step 2: Aggressive Small Directory Merging (< 5 files)")
    print("-" * 70)

    small_dirs = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames if d not in (".git", "__pycache__", ".vscode")
        ]
        dir_path = Path(dirpath)
        rel_path = dir_path.relative_to(root)
        depth = len(rel_path.parts)

        # Count files in this directory only
        file_count = len(filenames)

        if file_count < 5 and file_count > 0 and depth > 2:
            small_dirs.append(
                {
                    "path": dir_path,
                    "relative": str(rel_path),
                    "files": file_count,
                    "parent": dir_path.parent,
                    "depth": depth,
                }
            )

    print(f"   Found {len(small_dirs)} small directories")

    # Group by parent and merge
    by_parent = defaultdict(list)
    for dir_info in small_dirs:
        parent_str = str(dir_info["parent"].relative_to(root))
        by_parent[parent_str].append(dir_info)

    merged = 0
    files_moved = 0

    for parent_str, dirs in list(by_parent.items())[:200]:  # More aggressive
        parent_path = root / parent_str
        if not parent_path.exists():
            continue

        for dir_info in dirs[:10]:  # More per parent
            source = dir_info["path"]
            if not source.exists() or source == parent_path:
                continue

            try:
                moved = 0
                for item in source.iterdir():
                    dest = parent_path / item.name

                    if dest.exists():
                        if item.is_file() and dest.is_file():
                            if item.stat().st_size == dest.stat().st_size:
                                if not dry_run:
                                    item.unlink()
                                continue
                        # Version
                        base = dest.stem
                        ext = dest.suffix if item.is_file() else ""
                        counter = 1
                        while dest.exists():
                            if item.is_file():
                                dest = parent_path / f"{base}_{counter}{ext}"
                            else:
                                dest = parent_path / f"{item.name}_{counter}"
                            counter += 1

                    if not dry_run:
                        shutil.move(str(item), str(dest))
                    moved += 1

                if moved > 0:
                    files_moved += moved
                    merged += 1
                    if merged <= 30:
                        print(
                            f"   ✅ {dir_info['relative']} → {parent_str} ({moved} items)"
                        )

                    # Remove source
                    if not dry_run:
                        try:
                            source.rmdir()
                        except:
                            pass
            except Exception as e:
                if merged <= 5:
                    print(f"   ⚠️  Error: {e}")

    print(f"   Merged: {merged} directories")
    print(f"   Items moved: {files_moved}")
    print()

    # Step 3: Consolidate duplicate directory names at same level
    print("🔄 Step 3: Consolidating Duplicate Directory Names")
    print("-" * 70)

    # Find directories with same name at similar depths
    name_groups = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(root):
        dir_path = Path(dirpath)
        rel_path = dir_path.relative_to(root)
        depth = len(rel_path.parts)

        if depth >= 2 and depth <= 3:  # Focus on level 2-3
            for dirname in dirnames:
                if dirname not in (".git", "__pycache__", ".vscode", ".github"):
                    name_groups[dirname.lower()].append(
                        {
                            "path": dir_path / dirname,
                            "relative": str((dir_path / dirname).relative_to(root)),
                            "parent": dir_path,
                            "depth": depth,
                        }
                    )

    # Find duplicates
    duplicates = {name: dirs for name, dirs in name_groups.items() if len(dirs) > 1}

    print(f"   Found {len(duplicates)} duplicate directory names")

    consolidated = 0
    for name, dirs in list(duplicates.items())[:100]:
        # Group by depth
        by_depth = defaultdict(list)
        for d in dirs:
            by_depth[d["depth"]].append(d)

        # Merge at same depth
        for depth, depth_dirs in by_depth.items():
            if len(depth_dirs) > 1:
                # Pick the one with most content as target
                target_info = max(
                    depth_dirs,
                    key=lambda x: len(list(x["path"].iterdir()))
                    if x["path"].exists()
                    else 0,
                )
                sources = [d for d in depth_dirs if d != target_info]

                target = target_info["path"]
                if not target.exists():
                    continue

                for source_info in sources[:5]:  # Limit per group
                    source = source_info["path"]
                    if not source.exists() or source == target:
                        continue

                    try:
                        moved = 0
                        for item in source.iterdir():
                            dest = target / item.name

                            if dest.exists():
                                if item.is_file() and dest.is_file():
                                    if item.stat().st_size == dest.stat().st_size:
                                        if not dry_run:
                                            item.unlink()
                                        continue
                                base = dest.stem
                                ext = dest.suffix if item.is_file() else ""
                                counter = 1
                                while dest.exists():
                                    if item.is_file():
                                        dest = target / f"{base}_{counter}{ext}"
                                    else:
                                        dest = target / f"{item.name}_{counter}"
                                    counter += 1

                            if not dry_run:
                                shutil.move(str(item), str(dest))
                            moved += 1

                        if moved > 0:
                            consolidated += 1
                            if consolidated <= 20:
                                print(
                                    f"   ✅ {source_info['relative']} → {target_info['relative']} ({moved} items)"
                                )

                            if not dry_run:
                                try:
                                    shutil.rmtree(source)
                                except:
                                    pass
                    except Exception as e:
                        if consolidated <= 3:
                            print(f"   ⚠️  Error: {e}")

    print(f"   Consolidated: {consolidated} directories")
    print()

    # Step 4: Remove all empty directories
    print("🗑️  Step 4: Removing All Empty Directories")
    print("-" * 70)

    removed = 0
    # Bottom-up traversal
    all_dirs = []
    for dirpath, dirnames, filenames in os.walk(root):
        dir_path = Path(dirpath)
        all_dirs.append(dir_path)

    all_dirs.sort(key=lambda p: len(p.relative_to(root).parts), reverse=True)

    for dir_path in all_dirs:
        if dir_path == root:
            continue
        try:
            if not any(dir_path.iterdir()):
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
        estimated_reduction = flattened + merged + consolidated + removed
        print(f"📊 Current directory count: {initial_count:,}")
        print(f"💡 Estimated reduction: ~{estimated_reduction} directories")
        print(f"💡 Estimated final count: ~{initial_count - estimated_reduction:,}")

    print("\n✅ Ultra-flattening complete!")


def main():
    """Main execution"""
    import sys

    root_dir = sys.argv[1] if len(sys.argv) > 1 else "/Users/steven/pythons"
    dry_run = "--execute" not in sys.argv

    ultra_flatten(root_dir, dry_run)


if __name__ == "__main__":
    main()
