#!/usr/bin/env python3
"""
Analyze and suggest organization for 70 directories in ~/pythons
"""

from pathlib import Path
from collections import defaultdict
import json

def analyze_directories(root_dir):
    """Analyze directory structure and provide recommendations"""
    root = Path(root_dir)
    directories = [d for d in root.iterdir() if d.is_dir() and not d.name.startswith('.')]

    print("📊 COMPREHENSIVE DIRECTORY ANALYSIS")
    print("=" * 70)
    print(f"\nTotal directories: {len(directories)}")
    print()

    # Collect statistics
    dir_stats = []
    for d in directories:
        try:
            files = list(d.rglob("*"))
            file_count = len([f for f in files if f.is_file()])
            dir_count = len([f for f in files if f.is_dir()])
            size = sum(f.stat().st_size for f in files if f.is_file())

            dir_stats.append({
                'name': d.name,
                'files': file_count,
                'subdirs': dir_count,
                'size_mb': size / (1024*1024),
                'depth': len(d.parts) - len(root.parts)
            })
        except Exception as e:
            dir_stats.append({
                'name': d.name,
                'files': 0,
                'subdirs': 0,
                'size_mb': 0,
                'depth': 0
            })

    # Sort by file count
    dir_stats.sort(key=lambda x: -x['files'])

    print("📁 TOP DIRECTORIES (by file count):")
    print("-" * 70)
    for i, stat in enumerate(dir_stats[:15], 1):
        size_str = f"{stat['size_mb']:.1f}MB" if stat['size_mb'] > 0.1 else "<0.1MB"
        print(f"  {i:2}. {stat['name']:35} {stat['files']:5} files  {stat['subdirs']:3} subdirs  {size_str:>8}")
    print()

    print("📁 SMALLEST DIRECTORIES (merge candidates):")
    print("-" * 70)
    small = [s for s in dir_stats if s['files'] < 10 and s['subdirs'] < 5]
    small.sort(key=lambda x: x['files'])
    for i, stat in enumerate(small[:20], 1):
        size_str = f"{stat['size_mb']:.1f}MB" if stat['size_mb'] > 0.1 else "<0.1MB"
        print(f"  {i:2}. {stat['name']:35} {stat['files']:3} files  {stat['subdirs']:2} subdirs  {size_str:>8}")
    print()

    print("📊 STATISTICS:")
    print("-" * 70)
    print(f"  Total directories:        {len(dir_stats)}")
    print(f"  Total files:              {sum(s['files'] for s in dir_stats):,}")
    print(f"  Directories with < 5 files:    {len([s for s in dir_stats if s['files'] < 5])}")
    print(f"  Directories with < 10 files:   {len([s for s in dir_stats if s['files'] < 10])}")
    print(f"  Directories with 10-50 files:  {len([s for s in dir_stats if 10 <= s['files'] < 50])}")
    print(f"  Directories with 50-100 files: {len([s for s in dir_stats if 50 <= s['files'] < 100])}")
    print(f"  Directories with > 100 files:  {len([s for s in dir_stats if s['files'] >= 100])}")
    print()

    # Categorize
    categories = defaultdict(list)
    for stat in dir_stats:
        name = stat['name'].lower()
        categorized = False

        for pattern, cat in [
            (['tool', 'util', 'script', 'automation'], 'Tools/Utilities'),
            (['data', 'analytics', 'analysis'], 'Data/Analytics'),
            (['doc', 'readme', 'guide'], 'Documentation'),
            (['web', 'site', 'api', 'server'], 'Web/API'),
            (['ai', 'ml', 'model', 'neural', 'llm'], 'AI/ML'),
            (['media', 'audio', 'video', 'image', 'photo'], 'Media'),
            (['archive', 'old', 'legacy', 'backup'], 'Archive/Legacy'),
            (['project', 'client', 'business'], 'Projects/Business'),
            (['test', 'testing'], 'Testing'),
            (['config', 'setup', 'install'], 'Configuration'),
            (['platform', 'twitter', 'instagram', 'youtube'], 'Platforms'),
        ]:
            if any(p in name for p in pattern):
                categories[cat].append(stat)
                categorized = True
                break

        if not categorized:
            categories['Other'].append(stat)

    print("📂 CATEGORIZATION:")
    print("-" * 70)
    for category, dirs in sorted(categories.items(), key=lambda x: -len(x[1])):
        if dirs:
            total_files = sum(d['files'] for d in dirs)
            print(f"\n{category} ({len(dirs)} directories, {total_files:,} files):")
            for d in sorted(dirs, key=lambda x: -x['files'])[:10]:
                print(f"  • {d['name']:35} {d['files']:4} files")
            if len(dirs) > 10:
                print(f"  ... and {len(dirs) - 10} more")
    print()

    # Recommendations
    print("💡 RECOMMENDATIONS:")
    print("-" * 70)
    print()

    small_dirs = [s for s in dir_stats if s['files'] < 5]
    if small_dirs:
        print(f"1. Merge small directories ({len(small_dirs)} with < 5 files):")
        print("   Consider consolidating these into broader categories")
        print()

    similar_names = defaultdict(list)
    for stat in dir_stats:
        # Find similar names (simple prefix matching)
        prefix = stat['name'].split('_')[0].split('-')[0]
        if len(prefix) > 3:
            similar_names[prefix].append(stat['name'])

    duplicates = {k: v for k, v in similar_names.items() if len(v) > 1}
    if duplicates:
        print(f"2. Similar/duplicate names found ({len(duplicates)} groups):")
        for prefix, names in list(duplicates.items())[:5]:
            print(f"   '{prefix}': {', '.join(names[:5])}")
        print()

    print("3. Suggested organization:")
    print("   • Consolidate small directories into categories")
    print("   • Merge duplicate/similar directories")
    print("   • Create category-based structure (e.g., tools/, data/, media/)")
    print("   • Move single-purpose directories into appropriate categories")
    print()

    return dir_stats, categories

if __name__ == "__main__":
    import sys
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "/Users/steven/pythons"
    analyze_directories(root_dir)

