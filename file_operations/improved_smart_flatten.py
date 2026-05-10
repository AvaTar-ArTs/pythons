#!/usr/bin/env python3
"""
Improved Smart Directory Flattening
Implements intelligent strategies based on analysis
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict


def smart_flatten(root_dir, dry_run=True):
    """Improved smart flattening with better strategies"""
    root = Path(root_dir)

    print("🚀 IMPROVED SMART FLATTENING")
    print("=" * 70)
    print(f"Directory: {root_dir}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print()

    total_reduced = 0

    # Step 1: Category-priority deep flattening (depth > 3 → depth 3)
    print("📂 Step 1: Category-Priority Deep Flattening")
    print("-" * 70)

    deep_dirs_by_cat = defaultdict(list)

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
            category = rel_path.parts[0] if rel_path.parts else "root"
            has_content = len(filenames) > 0 or len(dirnames) > 0
            if has_content:
                deep_dirs_by_cat[category].append(
                    {"path": dir_path, "relative": str(rel_path), "depth": depth}
                )

    # Process by category, prioritizing high-impact
    cat_priority = sorted(deep_dirs_by_cat.items(), key=lambda x: -len(x[1]))

    flattened = 0
    for cat, dirs in cat_priority[:10]:  # Top 10 categories
        print(f"\n   📁 {cat}: {len(dirs)} deep directories")
        cat_flattened = 0

        for dir_info in dirs[:100]:  # Limit per category
            source = dir_info["path"]
            rel = Path(dir_info["relative"])
            parts = rel.parts

            if len(parts) > 3:
                base_path = Path(*parts[:2])
                combined_name = "_".join(parts[2:])
                target_rel = base_path / combined_name
                target = root / target_rel

                if source.exists() and source != target:
                    try:
                        if not target.exists():
                            if not dry_run:
                                target.mkdir(parents=True, exist_ok=True)

                        moved = 0
                        for item in source.iterdir():
                            dest = target / item.name

                            if dest.exists():
                                if item.is_file() and dest.is_file():
                                    if item.stat().st_size == dest.stat().st_size:
                                        if not dry_run:
                                            item.unlink()
                                        continue
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
                            cat_flattened += 1
                            if cat_flattened <= 5:
                                print(f"      ✅ {rel.name}")

                            if not dry_run:
                                try:
                                    source.rmdir()
                                except:
                                    pass
                    except Exception:
                        pass

        flattened += cat_flattened
        if cat_flattened > 0:
            print(f"      💰 Flattened: {cat_flattened} directories")

    print(f"\n   Total flattened: {flattened} directories")
    total_reduced += flattened
    print()

    # Step 2: Intelligent small directory merging (group by parent, merge intelligently)
    print("📦 Step 2: Intelligent Small Directory Merging")
    print("-" * 70)

    small_dirs_by_parent = defaultdict(list)

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames if d not in (".git", "__pycache__", ".vscode")
        ]
        dir_path = Path(dirpath)
        rel_path = dir_path.relative_to(root)
        depth = len(rel_path.parts)

        file_count = len([f for f in filenames if not f.startswith(".")])

        if file_count < 5 and file_count > 0 and depth > 2:
            parent = dir_path.parent
            parent_str = str(parent.relative_to(root))
            small_dirs_by_parent[parent_str].append(
                {"path": dir_path, "relative": str(rel_path), "files": file_count}
            )

    # Merge groups with 2+ small directories
    merged = 0
    for parent_str, dirs in list(small_dirs_by_parent.items()):
        if len(dirs) < 2:  # Only merge if 2+ small dirs
            continue

        parent_path = root / parent_str
        if not parent_path.exists():
            continue

        # Merge all small dirs into parent
        for dir_info in dirs[:10]:
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
                    merged += 1
                    if merged <= 20:
                        print(
                            f"   ✅ {dir_info['relative']} → {parent_str} ({moved} items)"
                        )

                    if not dry_run:
                        try:
                            source.rmdir()
                        except:
                            pass
            except Exception:
                pass

    print(f"\n   Total merged: {merged} directories")
    total_reduced += merged
    print()

    # Step 3: Consolidate duplicate directory names
    print("🔄 Step 3: Duplicate Name Consolidation")
    print("-" * 70)

    name_groups = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(root):
        dir_path = Path(dirpath)
        rel_path = dir_path.relative_to(root)
        depth = len(rel_path.parts)

        if 2 <= depth <= 3:
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

    duplicates = {name: dirs for name, dirs in name_groups.items() if len(dirs) > 1}

    consolidated = 0
    for name, dirs in list(duplicates.items())[:50]:
        by_depth = defaultdict(list)
        for d in dirs:
            by_depth[d["depth"]].append(d)

        for depth, depth_dirs in by_depth.items():
            if len(depth_dirs) > 1:
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

                for source_info in sources[:3]:
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
                            if consolidated <= 15:
                                print(
                                    f"   ✅ {source_info['relative']} → {target_info['relative']} ({moved} items)"
                                )

                            if not dry_run:
                                try:
                                    shutil.rmtree(source)
                                except:
                                    pass
                    except Exception:
                        pass

    print(f"\n   Total consolidated: {consolidated} directories")
    total_reduced += consolidated
    print()

    # Step 4: Remove empty directories
    print("🗑️  Step 4: Empty Directory Cleanup")
    print("-" * 70)

    removed = 0
    all_dirs = []
    for dirpath, dirnames, filenames in os.walk(root):
        all_dirs.append(Path(dirpath))

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
    total_reduced += removed
    print()

    # Final count
    if not dry_run:
        final_count = len([d for d in root.rglob("*") if d.is_dir()])
        print(f"📊 Final directory count: {final_count:,}")
        print(f"💰 Total reduction: {total_reduced} directories")
    else:
        initial_count = len([d for d in root.rglob("*") if d.is_dir()])
        print(f"📊 Current directory count: {initial_count:,}")
        print(f"💡 Estimated reduction: ~{total_reduced} directories")
        print(f"💡 Estimated final count: ~{initial_count - total_reduced:,}")

    print("\n✅ Improved smart flattening complete!")


def main():
    """Main execution"""
    import sys

    root_dir = sys.argv[1] if len(sys.argv) > 1 else "/Users/steven/pythons"
    dry_run = "--execute" not in sys.argv

    smart_flatten(root_dir, dry_run)


if __name__ == "__main__":
    main()
