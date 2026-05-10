#!/usr/bin/env python3
"""
Comprehensive analysis and organization plan for 70 directories
Creates categorization, grouping suggestions, and reorganization plan
"""

from pathlib import Path
from collections import defaultdict
import json
from datetime import datetime

def analyze_all_directories(root_dir):
    """Comprehensive analysis of all directories"""
    root = Path(root_dir)
    directories = [d for d in root.iterdir() if d.is_dir() and not d.name.startswith('.')]

    print("📊 COMPREHENSIVE 70 DIRECTORY ANALYSIS")
    print("=" * 70)

    # Get stats
    dir_stats = {}
    for d in directories:
        try:
            files = list(d.rglob("*"))
            file_count = len([f for f in files if f.is_file()])
            dir_count = len([f for f in files if f.is_dir()])
            size = sum(f.stat().st_size for f in files if f.is_file())

            dir_stats[d.name] = {
                'name': d.name,
                'files': file_count,
                'subdirs': dir_count,
                'size_mb': size / (1024*1024),
                'path': str(d)
            }
        except Exception:
            dir_stats[d.name] = {
                'name': d.name,
                'files': 0,
                'subdirs': 0,
                'size_mb': 0,
                'path': str(d)
            }

    # Categorize
    categories = categorize_directories(dir_stats)

    # Print analysis
    print(f"\n📁 Total Directories: {len(directories)}")
    print(f"📄 Total Files: {sum(s['files'] for s in dir_stats.values()):,}")
    print()

    print("📂 CATEGORIZATION:")
    print("-" * 70)
    for category, dirs in sorted(categories.items(), key=lambda x: -len(x[1])):
        if dirs:
            total_files = sum(dir_stats[d]['files'] for d in dirs)
            total_size = sum(dir_stats[d]['size_mb'] for d in dirs)
            print(f"\n{category} ({len(dirs)} directories, {total_files:,} files, {total_size:.1f} MB):")
            for d in sorted(dirs, key=lambda x: -dir_stats[x]['files'])[:15]:
                stat = dir_stats[d]
                print(f"  • {d:40} {stat['files']:5} files  {stat['size_mb']:6.1f} MB")
            if len(dirs) > 15:
                print(f"  ... and {len(dirs) - 15} more")

    # Size distribution
    print("\n" + "=" * 70)
    print("📊 SIZE DISTRIBUTION:")
    print("-" * 70)
    empty = [d for d, s in dir_stats.items() if s['files'] == 0]
    small = [d for d, s in dir_stats.items() if 1 <= s['files'] < 10]
    medium = [d for d, s in dir_stats.items() if 10 <= s['files'] < 50]
    large = [d for d, s in dir_stats.items() if 50 <= s['files'] < 200]
    xlarge = [d for d, s in dir_stats.items() if s['files'] >= 200]

    print(f"  Empty (0 files):         {len(empty):3} directories")
    print(f"  Small (1-9 files):       {len(small):3} directories")
    print(f"  Medium (10-49 files):    {len(medium):3} directories")
    print(f"  Large (50-199 files):    {len(large):3} directories")
    print(f"  Extra Large (200+ files): {len(xlarge):3} directories")

    # Organization suggestions
    print("\n" + "=" * 70)
    print("💡 ORGANIZATION SUGGESTIONS:")
    print("-" * 70)

    suggestions = []

    # Merge small directories
    if len(small) > 10:
        suggestions.append({
            'action': 'merge',
            'target': 'misc',
            'sources': small[:10],
            'reason': f'Merge {len(small[:10])} small directories into misc/'
        })
        print(f"\n1. Merge {len(small)} small directories:")
        print(f"   Consider creating 'misc/' or 'small-tools/' category")
        for d in small[:10]:
            print(f"      - {d} ({dir_stats[d]['files']} files)")
        if len(small) > 10:
            print(f"      ... and {len(small) - 10} more")

    # Consolidate by category
    for category, dirs in categories.items():
        if len(dirs) > 3 and category != 'Other':
            target = find_best_target(dir_stats, dirs)
            sources = [d for d in dirs if d != target]
            if sources:
                suggestions.append({
                    'action': 'consolidate',
                    'target': target,
                    'sources': sources[:5],
                    'reason': f'Consolidate {category} directories into {target}'
                })
                print(f"\n2. Consolidate {category} directories:")
                print(f"   Target: {target}")
                for d in sources[:5]:
                    print(f"      - {d} ({dir_stats[d]['files']} files) → {target}")
                if len(sources) > 5:
                    print(f"      ... and {len(sources) - 5} more")

    # Remove empty
    if empty:
        suggestions.append({
            'action': 'remove',
            'sources': empty,
            'reason': f'Remove {len(empty)} empty directories'
        })
        print(f"\n3. Remove empty directories ({len(empty)}):")
        for d in empty[:10]:
            print(f"      - {d}")
        if len(empty) > 10:
            print(f"      ... and {len(empty) - 10} more")

    # Save analysis
    output_file = Path.home() / "70_directories_analysis.json"
    analysis_data = {
        'timestamp': datetime.now().isoformat(),
        'total_directories': len(directories),
        'total_files': sum(s['files'] for s in dir_stats.values()),
        'categories': {k: list(v) for k, v in categories.items()},
        'size_distribution': {
            'empty': len(empty),
            'small': len(small),
            'medium': len(medium),
            'large': len(large),
            'xlarge': len(xlarge)
        },
        'directory_stats': dir_stats,
        'suggestions': suggestions
    }

    with open(output_file, 'w') as f:
        json.dump(analysis_data, f, indent=2, default=str)

    print(f"\n💾 Analysis saved to: {output_file}")

    return categories, dir_stats, suggestions

def categorize_directories(dir_stats):
    """Categorize directories by name and content"""
    categories = defaultdict(list)

    for name, stats in dir_stats.items():
        name_lower = name.lower()
        categorized = False

        # Tools/Utilities
        if any(word in name_lower for word in ['tool', 'util', 'script', 'automation']):
            categories['Tools/Utilities'].append(name)
            categorized = True

        # Data/Analytics
        if any(word in name_lower for word in ['data', 'analytics', 'analysis']):
            categories['Data/Analytics'].append(name)
            categorized = True

        # Documentation
        if any(word in name_lower for word in ['doc', 'documentation', 'readme']):
            categories['Documentation'].append(name)
            categorized = True

        # Media
        if any(word in name_lower for word in ['audio', 'video', 'image', 'media', 'gallery']):
            categories['Media'].append(name)
            categorized = True

        # Web/API
        if any(word in name_lower for word in ['web', 'site', 'api', 'server', 'http']):
            categories['Web/API'].append(name)
            categorized = True

        # AI/ML
        if any(word in name_lower for word in ['ai', 'ml', 'gpt', 'llm', 'neural', 'comic', 'axolotl']):
            categories['AI/ML'].append(name)
            categorized = True

        # Projects/Business
        if any(word in name_lower for word in ['project', 'client', 'business', 'portfolio']):
            categories['Projects/Business'].append(name)
            categorized = True

        # Archive/Legacy
        if any(word in name_lower for word in ['archive', 'legacy', 'old', 'backup']):
            categories['Archive/Legacy'].append(name)
            categorized = True

        # Configuration
        if any(word in name_lower for word in ['config', 'setup', 'install', 'requirement']):
            categories['Configuration'].append(name)
            categorized = True

        # Code/Development
        if any(word in name_lower for word in ['code', 'src', 'dev', 'framework']):
            categories['Code/Development'].append(name)
            categorized = True

        # Platforms
        if any(word in name_lower for word in ['platform', 'twitter', 'instagram', 'youtube']):
            categories['Platforms'].append(name)
            categorized = True

        if not categorized:
            categories['Other'].append(name)

    return categories

def find_best_target(dir_stats, dirs):
    """Find the best target directory (largest, most relevant name)"""
    if not dirs:
        return None

    # Sort by file count
    sorted_dirs = sorted(dirs, key=lambda x: -dir_stats[x]['files'])

    # Prefer directories with common names
    preferred_names = ['tools', 'data', 'docs', 'media', 'scripts']
    for name in preferred_names:
        if name in sorted_dirs:
            return name

    # Return largest
    return sorted_dirs[0]

if __name__ == "__main__":
    import sys
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "/Users/steven/pythons"
    analyze_all_directories(root_dir)

