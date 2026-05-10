#!/usr/bin/env python3
"""Final aggressive flattening to maximize reduction"""

import os
import shutil
from pathlib import Path


def final_flatten(root_dir, dry_run=True):
    """Final aggressive flattening"""
    root = Path(root_dir)

    print("🔥 FINAL AGGRESSIVE FLATTENING")
    print("=" * 70)
    print(f"Directory: {root_dir}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print()

    total_reduced = 0

    # Step 1: Flatten ALL depth > 2 to depth 2 (very aggressive)
    print("📂 Step 1: Ultra-Flatten (depth > 2 → depth 2)")
    print("-" * 70)

    deep_dirs = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames if d not in (".git", "__pycache__", ".vscode")
        ]
        dir_path = Path(dirpath)
        rel_path = dir_path.relative_to(root)
        depth = len(rel_path.parts)

        if depth > 2:
            has_content = len(filenames) > 0 or len(dirnames) > 0
            if has_content:
                deep_dirs.append(
                    {"path": dir_path, "relative": str(rel_path), "depth": depth}
                )

    print(f"   Found {len(deep_dirs)} directories at depth > 2")

    flattened = 0
    for dir_info in deep_dirs[:300]:  # Process many
        source = dir_info["path"]
        rel = Path(dir_info["relative"])
        parts = rel.parts

        if len(parts) > 2:
            # Keep only first level, combine rest
            base_path = Path(parts[0])
            combined_name = "_".join(parts[1:])
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
                        flattened += 1
                        if flattened <= 15:
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

    # Step 2: Merge ALL small directories (< 10 files) into parents
    print("📦 Step 2: Aggressive Small Directory Merging (< 10 files)")
    print("-" * 70)

    small_dirs = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames if d not in (".git", "__pycache__", ".vscode")
        ]
        dir_path = Path(dirpath)
        rel_path = dir_path.relative_to(root)
        depth = len(rel_path.parts)

        file_count = len([f for f in filenames if not f.startswith(".")])

        if file_count < 10 and file_count > 0 and depth > 1:
            small_dirs.append(
                {
                    "path": dir_path,
                    "relative": str(rel_path),
                    "files": file_count,
                    "parent": dir_path.parent,
                }
            )

    print(f"   Found {len(small_dirs)} small directories")

    merged = 0
    for dir_info in small_dirs[:200]:
        source = dir_info["path"]
        parent = dir_info["parent"]

        if not source.exists() or source == parent or parent == root:
            continue

        try:
            moved = 0
            for item in source.iterdir():
                dest = parent / item.name

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
                            dest = parent / f"{base}_{counter}{ext}"
                        else:
                            dest = parent / f"{item.name}_{counter}"
                        counter += 1

                if not dry_run:
                    shutil.move(str(item), str(dest))
                moved += 1

            if moved > 0:
                merged += 1
                if merged <= 20:
                    print(
                        f"   ✅ {dir_info['relative']} → {parent.relative_to(root)} ({moved} items)"
                    )

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

    # Step 3: Remove all empty directories
    print("🗑️  Step 3: Remove All Empty Directories")
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

    print("\n✅ Final aggressive flattening complete!")


if __name__ == "__main__":
    import sys

    root_dir = sys.argv[1] if len(sys.argv) > 1 else "/Users/steven/pythons"
    dry_run = "--execute" not in sys.argv
    final_flatten(root_dir, dry_run)
