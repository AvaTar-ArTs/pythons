#!/usr/bin/env python3
"""
Analyze which directories can be safely merged
Identifies safe merge candidates based on size, naming, and content
"""

from pathlib import Path
from collections import defaultdict
import json

def analyze_directory(dir_path):
    """Get stats for a directory"""
    try:
        files = list(dir_path.rglob("*"))
        file_count = len([f for f in files if f.is_file()])
        dir_count = len([f for f in files if f.is_dir()])
        size = sum(f.stat().st_size for f in files if f.is_file())
        return {
            'files': file_count,
            'subdirs': dir_count,
            'size_mb': size / (1024*1024),
            'exists': True
        }
    except Exception:
        return {'files': 0, 'subdirs': 0, 'size_mb': 0, 'exists': False}

def analyze_merge_candidates(root_dir):
    """Analyze which directories can be safely merged"""
    root = Path(root_dir)
    directories = [d for d in root.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    print("🔍 ANALYZING MERGE CANDIDATES")
    print("=" * 70)
    print()
    
    # Get stats for all directories
    dir_stats = {}
    for d in directories:
        dir_stats[d.name] = analyze_directory(d)
        dir_stats[d.name]['path'] = d
    
    # Find merge groups
    merge_groups = []
    
    # 1. Small directories that can be merged into larger ones
    small_dirs = [(name, stats) for name, stats in dir_stats.items() if stats['files'] < 10]
    large_dirs = [(name, stats) for name, stats in dir_stats.items() if stats['files'] >= 50]
    
    print("📊 SMALL DIRECTORIES (< 10 files) - Merge Candidates:")
    print("-" * 70)
    small_by_category = defaultdict(list)
    
    for name, stats in sorted(small_dirs, key=lambda x: x[1]['files']):
        name_lower = name.lower()
        category = "Other"
        
        # Categorize for potential merge target
        if any(word in name_lower for word in ['tool', 'util', 'script']):
            category = "Tools"
        elif any(word in name_lower for word in ['data', 'analytics']):
            category = "Data"
        elif any(word in name_lower for word in ['doc', 'documentation']):
            category = "Documentation"
        elif any(word in name_lower for word in ['audio', 'video', 'media']):
            category = "Media"
        elif any(word in name_lower for word in ['content', 'creation']):
            category = "Content"
        elif any(word in name_lower for word in ['archive', 'legacy']):
            category = "Archive"
        elif any(word in name_lower for word in ['config', 'setup']):
            category = "Config"
        
        small_by_category[category].append((name, stats))
        print(f"  {name:35} {stats['files']:3} files  → Suggested category: {category}")
    
    print()
    
    # 2. Find duplicate/similar names that should merge
    print("🔗 SIMILAR/DUPLICATE NAMES - Merge Groups:")
    print("-" * 70)
    
    name_groups = defaultdict(list)
    for name in dir_stats.keys():
        # Extract base name (remove prefixes/suffixes)
        base = name.lower()
        base = base.replace('_', ' ').replace('-', ' ').split()
        
        # Find common prefixes
        if len(base) > 0:
            key = base[0] if len(base[0]) > 3 else ' '.join(base[:2])
            name_groups[key].append(name)
    
    # Find groups with multiple entries
    duplicate_groups = {k: v for k, v in name_groups.items() if len(v) > 1}
    
    merge_suggestions = []
    
    for key, names in sorted(duplicate_groups.items(), key=lambda x: -len(x[1])):
        if len(names) > 1:
            # Find the largest directory (likely the merge target)
            names_with_stats = [(n, dir_stats[n]) for n in names]
            names_with_stats.sort(key=lambda x: -x[1]['files'])
            
            target = names_with_stats[0][0]
            sources = [n for n, _ in names_with_stats[1:]]
            
            merge_suggestions.append({
                'type': 'duplicate_names',
                'target': target,
                'sources': sources,
                'reason': f"Similar names (base: {key})"
            })
            
            print(f"\n  {key.upper()}:")
            print(f"    Target: {target:35} {dir_stats[target]['files']:4} files")
            for source in sources:
                print(f"    Merge:  {source:35} {dir_stats[source]['files']:4} files → {target}")
    
    print()
    
    # 3. Empty directories
    print("🗑️  EMPTY DIRECTORIES (can be removed or merged):")
    print("-" * 70)
    empty_dirs = [(name, stats) for name, stats in dir_stats.items() if stats['files'] == 0]
    for name, stats in sorted(empty_dirs):
        print(f"  {name:35} {stats['files']} files  {stats['subdirs']} subdirs")
    print()
    
    # 4. Create specific merge recommendations
    print("💡 SPECIFIC MERGE RECOMMENDATIONS:")
    print("-" * 70)
    
    recommendations = []
    
    # Data directories
    if 'DATA_UTILITIES' in dir_stats and 'DATA_ANALYTICS' in dir_stats:
        target = 'DATA_UTILITIES' if dir_stats['DATA_UTILITIES']['files'] > dir_stats['DATA_ANALYTICS']['files'] else 'DATA_ANALYTICS'
        source = 'DATA_ANALYTICS' if target == 'DATA_UTILITIES' else 'DATA_UTILITIES'
        recommendations.append({
            'type': 'merge',
            'target': target,
            'source': source,
            'reason': 'Duplicate DATA directories',
            'safe': dir_stats[source]['files'] < 10
        })
        print(f"  ✅ {source} → {target} (DATA consolidation)")
    
    # Audio directories
    audio_dirs = [n for n in dir_stats.keys() if 'audio' in n.lower()]
    if len(audio_dirs) > 1:
        audio_with_stats = [(n, dir_stats[n]) for n in audio_dirs]
        audio_with_stats.sort(key=lambda x: -x[1]['files'])
        target = audio_with_stats[0][0]
        for source, stats in audio_with_stats[1:]:
            recommendations.append({
                'type': 'merge',
                'target': target,
                'source': source,
                'reason': 'Audio-related directories',
                'safe': stats['files'] < 50
            })
            print(f"  ✅ {source} → {target} (Audio consolidation)")
    
    # Documentation directories
    doc_dirs = [n for n in dir_stats.keys() if any(word in n.lower() for word in ['doc', 'documentation']) and n != 'documentation']
    if doc_dirs and 'documentation' in dir_stats:
        for source in doc_dirs:
            recommendations.append({
                'type': 'merge',
                'target': 'documentation',
                'source': source,
                'reason': 'Documentation consolidation',
                'safe': dir_stats[source]['files'] < 20
            })
            print(f"  ✅ {source} → documentation (Docs consolidation)")
    
    # Content directories
    content_dirs = [n for n in dir_stats.keys() if 'content' in n.lower() and n != 'CONTENT']
    if len(content_dirs) > 1:
        content_with_stats = [(n, dir_stats[n]) for n in content_dirs]
        content_with_stats.sort(key=lambda x: -x[1]['files'])
        target = content_with_stats[0][0] if content_with_stats[0][1]['files'] > 0 else 'CONTENT'
        for source, stats in content_with_stats:
            if source != target:
                recommendations.append({
                    'type': 'merge',
                    'target': target if target in dir_stats else 'CONTENT',
                    'source': source,
                    'reason': 'Content directories consolidation',
                    'safe': stats['files'] < 10
                })
                print(f"  ✅ {source} → {target} (Content consolidation)")
    
    # Small directories into tools
    if 'tools' in dir_stats:
        small_tool_dirs = [
            n for n, stats in small_dirs 
            if any(word in n.lower() for word in ['tool', 'util', 'script', 'automation'])
            and n not in ['tools', 'AUTOMATION_BOTS']
        ]
        for source in small_tool_dirs[:5]:  # Limit to top 5
            recommendations.append({
                'type': 'merge',
                'target': 'tools',
                'source': source,
                'reason': 'Small tool/utility into tools',
                'safe': dir_stats[source]['files'] < 10
            })
            print(f"  ✅ {source} → tools (Small tool consolidation)")
    
    print()
    print("=" * 70)
    print(f"📊 SUMMARY:")
    print(f"   Total directories: {len(dir_stats)}")
    print(f"   Small directories (< 10 files): {len(small_dirs)}")
    print(f"   Empty directories: {len(empty_dirs)}")
    print(f"   Merge recommendations: {len(recommendations)}")
    print(f"   Safe merges (small sources): {sum(1 for r in recommendations if r['safe'])}")
    print()
    
    # Save recommendations to JSON
    output_file = Path.home() / "merge_recommendations.json"
    with open(output_file, 'w') as f:
        json.dump({
            'total_directories': len(dir_stats),
            'small_directories': len(small_dirs),
            'empty_directories': len(empty_dirs),
            'recommendations': recommendations,
            'directory_stats': {k: {'files': v['files'], 'subdirs': v['subdirs'], 'size_mb': v['size_mb']} 
                               for k, v in dir_stats.items()}
        }, f, indent=2)
    
    print(f"💾 Recommendations saved to: {output_file}")
    
    return recommendations, dir_stats

if __name__ == "__main__":
    import sys
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "/Users/steven/pythons"
    analyze_merge_candidates(root_dir)

