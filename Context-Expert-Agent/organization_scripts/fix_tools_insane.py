#!/usr/bin/env python3
"""
Fix the insane tools directory structure
Clean up git artifacts, merge scattered directories, organize properly
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict

def fix_insane_tools(root_dir, dry_run=True):
    """Fix the insane tools directory"""
    tools_dir = Path(root_dir) / "tools"

    if not tools_dir.exists():
        print(f"❌ tools directory not found at {tools_dir}")
        return

    print("🔧 FIXING INSANE TOOLS DIRECTORY")
    print("=" * 70)
    print(f"Directory: {tools_dir}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print()

    total_reduced = 0

    # Step 1: Remove git artifact directories (refs_*, objects_*, etc.)
    print("🗑️  Step 1: Remove Git Artifact Directories")
    print("-" * 70)

    git_artifacts = []
    for item in tools_dir.iterdir():
        if item.is_dir():
            name = item.name
            # Identify git artifacts
            if (name.startswith('refs_') or
                name.startswith('objects_') or
                name.startswith('logs_') or
                name.startswith('hooks_') or
                name.startswith('info_') or
                name.startswith('AUTOMATION_BOTS_logs')):
                git_artifacts.append(item)

    print(f"   Found {len(git_artifacts)} git artifact directories")

    removed = 0
    space_freed = 0
    for artifact in git_artifacts:
        try:
            # Calculate size
            size = sum(f.stat().st_size for f in artifact.rglob('*') if f.is_file())
            space_freed += size

            if not dry_run:
                shutil.rmtree(artifact)

            removed += 1
            if removed <= 20:
                size_mb = size / (1024 * 1024)
                print(f"   {'Would remove' if dry_run else 'Removed'}: {artifact.name} ({size_mb:.2f} MB)")
        except Exception as e:
            if removed <= 5:
                print(f"   ⚠️  Error: {e}")

    print(f"\n   {'Would remove' if dry_run else 'Removed'}: {removed} directories")
    print(f"   Space freed: {space_freed / (1024 * 1024):.2f} MB")
    total_reduced += removed
    print()

    # Step 2: Consolidate AUTOMATION_BOTS scattered directories
    print("📦 Step 2: Consolidate AUTOMATION_BOTS Directories")
    print("-" * 70)

    # Find all AUTOMATION_BOTS* directories
    automation_dirs = []
    for item in tools_dir.iterdir():
        if item.is_dir() and item.name.startswith('AUTOMATION_BOTS'):
            automation_dirs.append(item)

    if automation_dirs:
        # Create or use main AUTOMATION_BOTS directory
        main_auto = tools_dir / "AUTOMATION_BOTS"
        if not main_auto.exists():
            if not dry_run:
                main_auto.mkdir(exist_ok=True)

        consolidated = 0
        for auto_dir in automation_dirs:
            if auto_dir == main_auto:
                continue

            try:
                moved = 0
                for item in auto_dir.iterdir():
                    dest = main_auto / item.name

                    # Handle conflicts
                    if dest.exists():
                        if item.is_file() and dest.is_file():
                            if item.stat().st_size == dest.stat().st_size:
                                if not dry_run:
                                    item.unlink()
                                continue
                        base = dest.stem if item.is_file() else dest.name
                        ext = dest.suffix if item.is_file() else ''
                        counter = 1
                        while dest.exists():
                            if item.is_file():
                                dest = main_auto / f"{base}_{counter}{ext}"
                            else:
                                dest = main_auto / f"{item.name}_{counter}"
                            counter += 1

                    if not dry_run:
                        shutil.move(str(item), str(dest))
                    moved += 1

                if moved > 0:
                    consolidated += 1
                    if consolidated <= 20:
                        print(f"   ✅ {auto_dir.name} → AUTOMATION_BOTS ({moved} items)")

                    if not dry_run:
                        try:
                            shutil.rmtree(auto_dir)
                        except:
                            pass
            except Exception as e:
                if consolidated <= 5:
                    print(f"   ⚠️  Error: {e}")

        print(f"\n   Consolidated: {consolidated} directories")
        total_reduced += consolidated
    else:
        print("   No AUTOMATION_BOTS directories to consolidate")

    print()

    # Step 3: Flatten overly long directory names
    print("📂 Step 3: Flatten Long Directory Names")
    print("-" * 70)

    long_dirs = []
    for item in tools_dir.iterdir():
        if item.is_dir():
            name = item.name
            # Find directories with very long names (likely flattened incorrectly)
            if len(name) > 60 or name.count('_') > 8:
                long_dirs.append(item)

    print(f"   Found {len(long_dirs)} overly long directory names")

    flattened = 0
    for long_dir in long_dirs[:30]:  # Limit processing
        # Create a shorter, more reasonable name
        name_parts = long_dir.name.split('_')

        # Keep first 2-3 meaningful parts
        if len(name_parts) > 5:
            new_name = '_'.join(name_parts[:3])
            if new_name.endswith('_'):
                new_name = new_name[:-1]
        else:
            new_name = long_dir.name[:40]  # Truncate if needed

        target = tools_dir / new_name

        if target.exists() and target != long_dir:
            # Merge into existing
            try:
                moved = 0
                for item in long_dir.iterdir():
                    dest = target / item.name
                    if dest.exists():
                        if item.is_file() and dest.is_file():
                            if item.stat().st_size == dest.stat().st_size:
                                if not dry_run:
                                    item.unlink()
                                continue
                        base = dest.stem if item.is_file() else dest.name
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
                    flattened += 1
                    if flattened <= 15:
                        print(f"   ✅ {long_dir.name[:50]}... → {new_name} ({moved} items)")

                    if not dry_run:
                        try:
                            shutil.rmtree(long_dir)
                        except:
                            pass
            except Exception:
                pass
        else:
            # Rename
            if not dry_run:
                try:
                    long_dir.rename(target)
                    flattened += 1
                    if flattened <= 15:
                        print(f"   ✅ {long_dir.name[:50]}... → {new_name}")
                except Exception:
                    pass

    print(f"\n   Flattened/renamed: {flattened} directories")
    total_reduced += flattened
    print()

    # Step 4: Merge small directories into logical groups
    print("📦 Step 4: Merge Small Directories")
    print("-" * 70)

    small_dirs = []
    for item in tools_dir.iterdir():
        if item.is_dir():
            file_count = len(list(item.rglob("*.*")))
            if file_count < 10 and file_count > 0:
                small_dirs.append((item, file_count))

    print(f"   Found {len(small_dirs)} small directories (< 10 files)")

    # Group by prefix/keyword
    groups = defaultdict(list)
    for item, count in small_dirs:
        name = item.name.lower()
        # Categorize
        if 'social' in name or 'instagram' in name or 'twitter' in name:
            groups['social_media'].append(item)
        elif 'youtube' in name or 'yt' in name:
            groups['youtube'].append(item)
        elif 'reddit' in name:
            groups['reddit'].append(item)
        elif 'automation' in name or 'bot' in name:
            groups['automation'].append(item)
        elif 'data' in name or 'util' in name:
            groups['utilities'].append(item)
        else:
            groups['misc'].append(item)

    merged = 0
    for group_name, dirs in groups.items():
        if len(dirs) <= 1:
            continue

        # Create group directory
        group_dir = tools_dir / group_name
        if not group_dir.exists():
            if not dry_run:
                group_dir.mkdir(exist_ok=True)

        # Merge directories into group
        for dir_item in dirs[:10]:  # Limit per group
            try:
                moved = 0
                for item in dir_item.iterdir():
                    dest = group_dir / item.name
                    if dest.exists():
                        if item.is_file() and dest.is_file():
                            if item.stat().st_size == dest.stat().st_size:
                                if not dry_run:
                                    item.unlink()
                                continue
                        base = dest.stem if item.is_file() else dest.name
                        ext = dest.suffix if item.is_file() else ''
                        counter = 1
                        while dest.exists():
                            if item.is_file():
                                dest = group_dir / f"{base}_{counter}{ext}"
                            else:
                                dest = group_dir / f"{item.name}_{counter}"
                            counter += 1

                    if not dry_run:
                        shutil.move(str(item), str(dest))
                    moved += 1

                if moved > 0:
                    merged += 1
                    if merged <= 20:
                        print(f"   ✅ {dir_item.name} → {group_name}/ ({moved} items)")

                    if not dry_run:
                        try:
                            shutil.rmtree(dir_item)
                        except:
                            pass
            except Exception:
                pass

    print(f"\n   Merged: {merged} directories")
    total_reduced += merged
    print()

    # Step 5: Remove empty directories
    print("🗑️  Step 5: Remove Empty Directories")
    print("-" * 70)

    removed = 0
    all_dirs = list(tools_dir.rglob("*"))
    all_dirs.sort(key=lambda p: len(p.relative_to(tools_dir).parts), reverse=True)

    for dir_path in all_dirs:
        if dir_path == tools_dir:
            continue
        try:
            if dir_path.is_dir() and not any(dir_path.iterdir()):
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
    fix_insane_tools(root_dir, dry_run)

