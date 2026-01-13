#!/usr/bin/env python3
"""Fix and organize tools directory based on analysis"""

import os
import shutil
from pathlib import Path
from collections import defaultdict

def fix_tools(root_dir, dry_run=True):
    """Fix tools directory structure"""
    tools_dir = Path(root_dir) / "tools"

    if not tools_dir.exists():
        print(f"❌ tools directory not found at {tools_dir}")
        return

    print("🔧 FIXING TOOLS DIRECTORY")
    print("=" * 70)
    print(f"Directory: {tools_dir}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print()

    total_reduced = 0

    # Step 1: Flatten deep nesting (depth > 2 → depth 2)
    print("📂 Step 1: Flatten Deep Nesting (depth > 2 → depth 2)")
    print("-" * 70)

    deep_dirs = []
    for dirpath, dirnames, filenames in os.walk(tools_dir):
        dirnames[:] = [d for d in dirnames if d not in ('.git', '__pycache__', '.vscode')]
        dir_path = Path(dirpath)
        rel_path = dir_path.relative_to(tools_dir)
        depth = len(rel_path.parts)

        if depth > 2:
            has_content = len(filenames) > 0 or len(dirnames) > 0
            if has_content:
                deep_dirs.append({
                    'path': dir_path,
                    'relative': str(rel_path),
                    'depth': depth
                })

    print(f"   Found {len(deep_dirs)} directories at depth > 2")

    flattened = 0
    for dir_info in deep_dirs[:200]:
        source = dir_info['path']
        rel = Path(dir_info['relative'])
        parts = rel.parts

        if len(parts) > 2:
            # Keep first level, combine rest
            base_path = Path(parts[0])
            combined_name = '_'.join(parts[1:])
            target_rel = base_path / combined_name
            target = tools_dir / target_rel

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
                            ext = dest.suffix if item.is_file() else ''
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
                        flattened += 1
                        if flattened <= 20:
                            print(f"   ✅ {rel} → {target_rel}")

                        if not dry_run:
                            try:
                                source.rmdir()
                            except:
                                pass
                except Exception:
                    pass

    print(f"   Flattened: {flattened} directories")
    total_reduced += flattened
    print()

    # Step 2: Merge small directories (< 5 files)
    print("📦 Step 2: Merge Small Directories (< 5 files)")
    print("-" * 70)

    small_dirs = []
    for dirpath, dirnames, filenames in os.walk(tools_dir):
        dirnames[:] = [d for d in dirnames if d not in ('.git', '__pycache__', '.vscode')]
        dir_path = Path(dirpath)
        rel_path = dir_path.relative_to(tools_dir)
        depth = len(rel_path.parts)

        file_count = len([f for f in filenames if not f.startswith('.')])

        if file_count < 5 and file_count > 0 and depth > 1:
            small_dirs.append({
                'path': dir_path,
                'relative': str(rel_path),
                'files': file_count,
                'parent': dir_path.parent
            })

    print(f"   Found {len(small_dirs)} small directories")

    # Group by parent
    by_parent = defaultdict(list)
    for dir_info in small_dirs:
        parent_str = str(dir_info['parent'].relative_to(tools_dir))
        by_parent[parent_str].append(dir_info)

    merged = 0
    for parent_str, dirs in list(by_parent.items())[:100]:
        parent_path = tools_dir / parent_str
        if not parent_path.exists():
            continue

        for dir_info in dirs[:10]:
            source = dir_info['path']
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
                        ext = dest.suffix if item.is_file() else ''
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
                        print(f"   ✅ {dir_info['relative']} → {parent_str} ({moved} items)")

                    if not dry_run:
                        try:
                            source.rmdir()
                        except:
                            pass
            except Exception:
                pass

    print(f"   Merged: {merged} directories")
    total_reduced += merged
    print()

    # Step 3: Consolidate duplicate directory names
    print("🔄 Step 3: Consolidate Duplicate Directory Names")
    print("-" * 70)

    name_groups = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(tools_dir):
        dir_path = Path(dirpath)
        rel_path = dir_path.relative_to(tools_dir)
        depth = len(rel_path.parts)

        if depth >= 1 and depth <= 2:
            for dirname in dirnames:
                if dirname not in ('.git', '__pycache__', '.vscode'):
                    name_groups[dirname.lower()].append({
                        'path': dir_path / dirname,
                        'relative': str((dir_path / dirname).relative_to(tools_dir)),
                        'parent': dir_path,
                        'depth': depth
                    })

    duplicates = {name: dirs for name, dirs in name_groups.items() if len(dirs) > 1}

    consolidated = 0
    for name, dirs in list(duplicates.items())[:50]:
        by_depth = defaultdict(list)
        for d in dirs:
            by_depth[d['depth']].append(d)

        for depth, depth_dirs in by_depth.items():
            if len(depth_dirs) > 1:
                target_info = max(depth_dirs, key=lambda x: len(list(x['path'].iterdir())) if x['path'].exists() else 0)
                sources = [d for d in depth_dirs if d != target_info]

                target = target_info['path']
                if not target.exists():
                    continue

                for source_info in sources[:3]:
                    source = source_info['path']
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
                                ext = dest.suffix if item.is_file() else ''
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
                                print(f"   ✅ {source_info['relative']} → {target_info['relative']} ({moved} items)")

                            if not dry_run:
                                try:
                                    shutil.rmtree(source)
                                except:
                                    pass
                    except Exception:
                        pass

    print(f"   Consolidated: {consolidated} directories")
    total_reduced += consolidated
    print()

    # Step 4: Remove empty directories
    print("🗑️  Step 4: Remove Empty Directories")
    print("-" * 70)

    removed = 0
    all_dirs = []
    for dirpath, dirnames, filenames in os.walk(tools_dir):
        all_dirs.append(Path(dirpath))

    all_dirs.sort(key=lambda p: len(p.relative_to(tools_dir).parts), reverse=True)

    for dir_path in all_dirs:
        if dir_path == tools_dir:
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
        final_count = len([d for d in tools_dir.rglob("*") if d.is_dir()])
        print(f"📊 Final directory count in tools/: {final_count:,}")
        print(f"💰 Total reduction: {total_reduced} directories")
    else:
        initial_count = len([d for d in tools_dir.rglob("*") if d.is_dir()])
        print(f"📊 Current directory count in tools/: {initial_count:,}")
        print(f"💡 Estimated reduction: ~{total_reduced} directories")
        print(f"💡 Estimated final count: ~{initial_count - total_reduced:,}")

    print("\n✅ Tools directory fix complete!")

if __name__ == "__main__":
    import sys
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "/Users/steven/pythons"
    dry_run = "--execute" not in sys.argv
    fix_tools(root_dir, dry_run)

