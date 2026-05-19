#!/usr/bin/env python3
"""
Comprehensive organization of 70 directories
- Removes empty directories
- Merges small directories
- Consolidates by category
- Creates clean structure
"""

import os
import shutil
import json
from pathlib import Path
from collections import defaultdict

def load_analysis():
    """Load directory analysis"""
    analysis_file = Path.home() / "70_directories_analysis.json"
    if analysis_file.exists():
        with open(analysis_file, 'r') as f:
            return json.load(f)
    return None

def remove_empty_directories(root_dir, empty_dirs, dry_run=True):
    """Remove empty directories"""
    root = Path(root_dir)
    removed = 0
    errors = 0

    print("🗑️  STEP 1: Remove Empty Directories")
    print("-" * 70)

    for dir_name in empty_dirs:
        dir_path = root / dir_name
        if dir_path.exists():
            try:
                # Double check it's actually empty
                files = list(dir_path.rglob("*"))
                file_count = len([f for f in files if f.is_file()])

                if file_count == 0:
                    if not dry_run:
                        shutil.rmtree(dir_path)
                    print(f"   ✅ Removed: {dir_name}")
                    removed += 1
                else:
                    print(f"   ⚠️  Skipped {dir_name} (has {file_count} files)")
            except Exception as e:
                print(f"   ❌ Error removing {dir_name}: {e}")
                errors += 1

    print(f"\n   Removed: {removed}, Errors: {errors}\n")
    return removed, errors

def merge_small_directories(root_dir, small_dirs, target_dir, dry_run=True):
    """Merge small directories into target"""
    root = Path(root_dir)
    target = root / target_dir

    if not dry_run:
        target.mkdir(parents=True, exist_ok=True)

    merged = 0
    errors = 0

    print(f"📦 STEP 2: Merge Small Directories into {target_dir}/")
    print("-" * 70)

    for dir_name in small_dirs:
        source = root / dir_name
        if not source.exists():
            continue

        try:
            files = list(source.rglob("*"))
            file_count = len([f for f in files if f.is_file() and not f.name.startswith('.')])

            if file_count == 0:
                continue

            # Copy files
            for item in source.rglob("*"):
                if item.is_file() and not item.name.startswith('.'):
                    rel_path = item.relative_to(source)
                    dst = target / dir_name / rel_path

                    if not dry_run:
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        if not dst.exists():
                            shutil.copy2(item, dst)

                    merged += 1

            print(f"   ✅ Merged {dir_name} ({file_count} files)")

            if not dry_run and merged > 0:
                shutil.rmtree(source)

        except Exception as e:
            print(f"   ❌ Error merging {dir_name}: {e}")
            errors += 1

    print(f"\n   Files merged: {merged}, Errors: {errors}\n")
    return merged, errors

def consolidate_by_category(root_dir, categories_map, dry_run=True):
    """Consolidate directories by category"""
    root = Path(root_dir)
    consolidated = 0
    errors = 0

    print("📂 STEP 3: Consolidate by Category")
    print("-" * 70)

    # Define target directories for each category
    category_targets = {
        'Tools/Utilities': 'tools',
        'Data/Analytics': 'data',
        'Documentation': 'documentation',
        'Media': 'media',
        'AI/ML': 'ai-ml',
        'Archive/Legacy': 'archives',
        'Projects/Business': 'projects',
        'Code/Development': 'code',
        'Web/API': 'web',
        'Configuration': 'config',
        'Platforms': 'platforms'
    }

    for category, dirs in categories_map.items():
        if category not in category_targets or len(dirs) <= 1:
            continue

        target_name = category_targets[category]
        target = root / target_name

        # Find best target (largest existing directory in category)
        existing_dirs = [d for d in dirs if (root / d).exists()]
        if existing_dirs:
            # Use existing directory as target if it's large
            analysis_file = Path.home() / "70_directories_analysis.json"
            if analysis_file.exists():
                with open(analysis_file, 'r') as f:
                    analysis = json.load(f)
                    stats = analysis.get('directory_stats', {})
                    existing_dirs.sort(key=lambda x: stats.get(x, {}).get('files', 0), reverse=True)
                    if stats.get(existing_dirs[0], {}).get('files', 0) > 50:
                        target = root / existing_dirs[0]
                        target_name = existing_dirs[0]

        if not dry_run:
            target.mkdir(parents=True, exist_ok=True)

        sources = [d for d in dirs if d != target_name and (root / d).exists()]

        if not sources:
            continue

        print(f"\n   Category: {category}")
        print(f"   Target: {target_name}")

        for source_name in sources[:10]:  # Limit to 10 per category
            source = root / source_name
            try:
                files = list(source.rglob("*"))
                file_count = len([f for f in files if f.is_file() and not f.name.startswith('.')])

                if file_count == 0:
                    continue

                # Copy files
                for item in source.rglob("*"):
                    if item.is_file() and not item.name.startswith('.'):
                        rel_path = item.relative_to(source)
                        dst = target / source_name / rel_path  # Keep source name as subdirectory

                        if not dry_run:
                            dst.parent.mkdir(parents=True, exist_ok=True)
                            if not dst.exists():
                                shutil.copy2(item, dst)

                        consolidated += 1

                print(f"      ✅ {source_name} → {target_name}/ ({file_count} files)")

                if not dry_run and consolidated > 0:
                    shutil.rmtree(source)

            except Exception as e:
                print(f"      ❌ Error: {source_name}: {e}")
                errors += 1

    print(f"\n   Files consolidated: {consolidated}, Errors: {errors}\n")
    return consolidated, errors

def generate_summary(root_dir, dry_run=True):
    """Generate final summary"""
    root = Path(root_dir)
    directories = [d for d in root.iterdir() if d.is_dir() and not d.name.startswith('.')]

    print("📊 FINAL SUMMARY")
    print("=" * 70)
    print(f"Total directories: {len(directories)}")
    print(f"Mode: {'DRY RUN' if dry_run else 'COMPLETED'}")
    print()

    # Count files
    total_files = 0
    for d in directories:
        try:
            files = list(d.rglob("*"))
            file_count = len([f for f in files if f.is_file()])
            total_files += file_count
        except:
            pass

    print(f"Total files: {total_files:,}")
    print()
    print("Top directories:")
    dir_counts = []
    for d in directories:
        try:
            files = list(d.rglob("*"))
            file_count = len([f for f in files if f.is_file()])
            dir_counts.append((d.name, file_count))
        except:
            pass

    dir_counts.sort(key=lambda x: -x[1])
    for name, count in dir_counts[:10]:
        print(f"  {name:40} {count:5} files")

def main():
    """Main execution"""
    import sys

    root_dir = "/Users/steven/pythons"
    dry_run = "--execute" not in sys.argv

    print("🚀 COMPREHENSIVE DIRECTORY ORGANIZATION")
    print("=" * 70)
    print(f"Directory: {root_dir}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print()

    # Load analysis
    analysis = load_analysis()
    if not analysis:
        print("❌ Analysis file not found. Run organize_70_directories.py first.")
        return

    # Step 1: Remove empty directories
    empty_dirs = []
    stats = analysis.get('directory_stats', {})
    for name, stat in stats.items():
        if stat.get('files', 0) == 0:
            empty_dirs.append(name)

    remove_empty_directories(root_dir, empty_dirs, dry_run)

    # Step 2: Merge small directories (only if dry_run, or user confirms)
    # Skip for now - let's see results first

    # Step 3: Consolidate by category
    categories = analysis.get('categories', {})
    consolidate_by_category(root_dir, categories, dry_run)

    # Final summary
    generate_summary(root_dir, dry_run)

    if dry_run:
        print("\n💡 Run with --execute to perform actual organization")
    else:
        print("\n✅ Organization complete!")

if __name__ == "__main__":
    main()

