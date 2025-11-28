#!/usr/bin/env python3
"""
Search and organize MP3s, discography, prompts, lyrics across ~/ with configurable depth
"""

from pathlib import Path
import json
import csv
from datetime import datetime
from collections import defaultdict
import os

home_dir = Path.home()
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Configuration
MAX_DEPTH = 10  # Set to None for unlimited depth, or an integer to limit depth
SHOW_DEPTH_INFO = True  # Show depth information in output
# Exclude system directories to speed up search
EXCLUDE_DIRS = {'.git', 'node_modules', '__pycache__', '.next', 'dist', 'build', '.venv', 'venv', 'Library', 'System', 'Applications', 'opt', 'private', 'usr', 'bin', 'sbin', 'etc', 'var', 'tmp'}

print("=" * 100)
print("🔍 SEARCHING FOR MP3s, DISCOGRAPHY, PROMPTS, LYRICS")
print(f"📍 Location: {home_dir}")
if MAX_DEPTH:
    print(f"📏 Max Depth: {MAX_DEPTH} levels")
else:
    print(f"📏 Max Depth: Unlimited")
print("=" * 100)
print()

# Search patterns
search_patterns = {
    'mp3': ['*.mp3'],
    'discography': ['*discography*', '*disc*', '*album*', '*collection*'],
    'prompts': ['*prompt*', '*prompts*'],
    'lyrics': ['*lyric*', '*lyrics*', '*transcript*', '*transcription*'],
}

results = defaultdict(list)

def get_depth(path, base_path):
    """Calculate depth of path relative to base path"""
    try:
        relative = path.relative_to(base_path)
        return len(relative.parts)
    except:
        return 0

def should_include_path(path, base_path):
    """Check if path should be included based on depth limit and exclusions"""
    # Check if any part of path is in exclude list
    path_parts = Path(path).parts
    for part in path_parts:
        if part in EXCLUDE_DIRS:
            return False
    
    if MAX_DEPTH is None:
        return True
    depth = get_depth(path, base_path)
    return depth <= MAX_DEPTH

def search_files(base_path, file_type, patterns):
    """Search for files matching patterns"""
    found_files = []
    for pattern in patterns:
        for item in base_path.rglob(pattern):
            try:
                if not should_include_path(item, base_path):
                    continue
                    
                if item.is_file():
                    size = item.stat().st_size
                    depth = get_depth(item, base_path)
                    found_files.append({
                        'path': str(item),
                        'size': size,
                        'size_mb': round(size / (1024*1024), 2),
                        'name': item.name,
                        'depth': depth,
                        'directory': str(item.parent)
                    })
            except Exception as e:
                pass
    return found_files

def search_directories(base_path, patterns):
    """Search for directories matching patterns"""
    found_items = []
    for pattern in patterns:
        for item in base_path.rglob(pattern):
            try:
                if not should_include_path(item, base_path):
                    continue
                    
                if item.is_dir():
                    depth = get_depth(item, base_path)
                    found_items.append({
                        'path': str(item),
                        'name': item.name,
                        'type': 'folder',
                        'depth': depth
                    })
            except Exception as e:
                pass
    return found_items

# Search MP3s
print("   Searching MP3s...")
mp3_count = 0
for mp3 in home_dir.rglob("*.mp3"):
    try:
        if not should_include_path(mp3, home_dir):
            continue
        size = mp3.stat().st_size
        depth = get_depth(mp3, home_dir)
        results['mp3'].append({
            'path': str(mp3),
            'size': size,
            'size_mb': round(size / (1024*1024), 2),
            'name': mp3.name,
            'depth': depth,
            'directory': str(mp3.parent)
        })
        mp3_count += 1
        if mp3_count % 100 == 0:
            print(f"      Found {mp3_count} MP3s...")
    except:
        pass
print(f"   ✅ Found {mp3_count} MP3 files")
print()

# Search discography
print("   Searching discography...")
disc_count = 0
for pattern in search_patterns['discography']:
    for item in home_dir.rglob(pattern):
        try:
            if not should_include_path(item, home_dir):
                continue
            if item.is_file() or item.is_dir():
                depth = get_depth(item, home_dir)
                results['discography'].append({
                    'path': str(item),
                    'name': item.name,
                    'type': 'file' if item.is_file() else 'folder',
                    'depth': depth
                })
                disc_count += 1
        except:
            pass
print(f"   ✅ Found {disc_count} discography items")
print()

# Search prompts
print("   Searching prompts...")
prompt_count = 0
for pattern in search_patterns['prompts']:
    for item in home_dir.rglob(pattern):
        try:
            if not should_include_path(item, home_dir):
                continue
            if item.is_file():
                size = item.stat().st_size
                depth = get_depth(item, home_dir)
                results['prompts'].append({
                    'path': str(item),
                    'name': item.name,
                    'size': size,
                    'size_mb': round(size / (1024*1024), 2),
                    'depth': depth
                })
                prompt_count += 1
        except:
            pass
print(f"   ✅ Found {prompt_count} prompt files")
print()

# Search lyrics
print("   Searching lyrics...")
lyric_count = 0
for pattern in search_patterns['lyrics']:
    for item in home_dir.rglob(pattern):
        try:
            if not should_include_path(item, home_dir):
                continue
            if item.is_file():
                size = item.stat().st_size
                depth = get_depth(item, home_dir)
                results['lyrics'].append({
                    'path': str(item),
                    'name': item.name,
                    'size': size,
                    'size_mb': round(size / (1024*1024), 2),
                    'depth': depth
                })
                lyric_count += 1
        except:
            pass
print(f"   ✅ Found {lyric_count} lyric files")
print()

# Duplicate detection for MP3s
print("=" * 100)
print("🔍 DETECTING DUPLICATES")
print("=" * 100)
print()

filename_to_paths = defaultdict(list)
for mp3 in results['mp3']:
    filename = mp3['name']
    filename_to_paths[filename].append(mp3)

duplicates = {k: v for k, v in filename_to_paths.items() if len(v) > 1}
unique_files = {k: v[0] for k, v in filename_to_paths.items() if len(v) == 1}

print(f"   Total MP3 files: {len(results['mp3']):,}")
print(f"   Unique filenames: {len(filename_to_paths):,}")
print(f"   Files with duplicate names: {len(duplicates):,}")
print(f"   Total duplicate instances: {sum(len(v) for v in duplicates.values()):,}")
print()

# Generate report
print("=" * 100)
print("📊 SEARCH RESULTS SUMMARY")
print("=" * 100)
print()

# MP3s
mp3_count = len(results['mp3'])
mp3_size = sum(f['size'] for f in results['mp3']) / (1024*1024*1024)
mp3_size_mb = sum(f['size'] for f in results['mp3']) / (1024*1024)

print("🎵 MP3 FILES:")
print(f"   Count: {mp3_count:,} files")
print(f"   Size:  {mp3_size:.2f} GB ({mp3_size_mb:.2f} MB)")
if SHOW_DEPTH_INFO:
    depth_stats = defaultdict(int)
    for mp3 in results['mp3']:
        depth_stats[mp3['depth']] += 1
    print(f"   Depth distribution:")
    for depth in sorted(depth_stats.keys()):
        print(f"      Level {depth}: {depth_stats[depth]:,} files")
print()

# Discography
disc_count = len(results['discography'])

print("💿 DISCOGRAPHY:")
print(f"   Count: {disc_count:,} items")
if SHOW_DEPTH_INFO:
    depth_stats = defaultdict(int)
    for item in results['discography']:
        depth_stats[item['depth']] += 1
    print(f"   Depth distribution:")
    for depth in sorted(depth_stats.keys()):
        print(f"      Level {depth}: {depth_stats[depth]:,} items")
print()

# Prompts
prompt_count = len(results['prompts'])
prompt_size = sum(f['size'] for f in results['prompts']) / (1024*1024)

print("📝 PROMPTS:")
print(f"   Count: {prompt_count:,} files")
print(f"   Size:  {prompt_size:.2f} MB")
if SHOW_DEPTH_INFO:
    depth_stats = defaultdict(int)
    for prompt in results['prompts']:
        depth_stats[prompt['depth']] += 1
    print(f"   Depth distribution:")
    for depth in sorted(depth_stats.keys()):
        print(f"      Level {depth}: {depth_stats[depth]:,} files")
print()

# Lyrics
lyric_count = len(results['lyrics'])
lyric_size = sum(f['size'] for f in results['lyrics']) / (1024*1024)

print("🎤 LYRICS:")
print(f"   Count: {lyric_count:,} files")
print(f"   Size:  {lyric_size:.2f} MB")
if SHOW_DEPTH_INFO:
    depth_stats = defaultdict(int)
    for lyric in results['lyrics']:
        depth_stats[lyric['depth']] += 1
    print(f"   Depth distribution:")
    for depth in sorted(depth_stats.keys()):
        print(f"      Level {depth}: {depth_stats[depth]:,} files")
print()

# Save detailed JSON report
report_file = Path.home() / "Documents" / f"MP3_SEARCH_{timestamp}.json"
with open(report_file, 'w') as f:
    json.dump({
        'timestamp': timestamp,
        'base_path': str(home_dir),
        'max_depth': MAX_DEPTH,
        'summary': {
            'mp3': {
                'count': mp3_count,
                'size_gb': round(mp3_size, 2),
                'size_mb': round(mp3_size_mb, 2)
            },
            'discography': {
                'count': disc_count
            },
            'prompts': {
                'count': prompt_count,
                'size_mb': round(prompt_size, 2)
            },
            'lyrics': {
                'count': lyric_count,
                'size_mb': round(lyric_size, 2)
            },
            'duplicates': {
                'files_with_duplicates': len(duplicates),
                'total_duplicate_instances': sum(len(v) for v in duplicates.values())
            }
        },
        'details': {
            'mp3': results['mp3'][:500],  # Top 500
            'discography': results['discography'][:200],
            'prompts': results['prompts'][:200],
            'lyrics': results['lyrics'][:200]
        }
    }, f, indent=2)

print(f"📄 Detailed JSON report saved: {report_file.name}")
print()

# CSV Export - All MP3s
csv_file_all = Path.home() / "Documents" / f"MP3_ALL_FILES_{timestamp}.csv"
with open(csv_file_all, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'filename', 'full_path', 'directory', 'depth', 
        'size_bytes', 'size_mb', 'is_duplicate', 'duplicate_count'
    ])
    
    for mp3 in results['mp3']:
        filename = mp3['name']
        is_duplicate = len(filename_to_paths[filename]) > 1
        duplicate_count = len(filename_to_paths[filename]) if is_duplicate else 1
        
        writer.writerow([
            filename,
            mp3['path'],
            mp3['directory'],
            mp3['depth'],
            mp3['size'],
            mp3['size_mb'],
            is_duplicate,
            duplicate_count
        ])

print(f"📊 CSV (All MP3s) saved: {csv_file_all.name}")
print()

# CSV Export - Duplicates Only
if duplicates:
    csv_file_dupes = Path.home() / "Documents" / f"MP3_DUPLICATES_{timestamp}.csv"
    with open(csv_file_dupes, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'filename', 'copy_number', 'full_path', 'directory', 
            'depth', 'size_bytes', 'size_mb', 'total_copies'
        ])
        
        for filename in sorted(duplicates.keys()):
            paths_list = sorted(duplicates[filename], key=lambda x: x['path'])
            total_copies = len(paths_list)
            
            for i, mp3 in enumerate(paths_list, 1):
                writer.writerow([
                    filename,
                    i,
                    mp3['path'],
                    mp3['directory'],
                    mp3['depth'],
                    mp3['size'],
                    mp3['size_mb'],
                    total_copies
                ])
    
    print(f"📊 CSV (Duplicates Only) saved: {csv_file_dupes.name}")
    print()

# CSV Export - By Depth
csv_file_depth = Path.home() / "Documents" / f"MP3_BY_DEPTH_{timestamp}.csv"
with open(csv_file_depth, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'depth', 'file_type', 'count', 'total_size_mb', 'total_size_gb'
    ])
    
    # Group by depth
    depth_stats = defaultdict(lambda: defaultdict(lambda: {'count': 0, 'size': 0}))
    
    for mp3 in results['mp3']:
        depth = mp3['depth']
        depth_stats[depth]['mp3']['count'] += 1
        depth_stats[depth]['mp3']['size'] += mp3['size']
    
    for prompt in results['prompts']:
        depth = prompt['depth']
        depth_stats[depth]['prompts']['count'] += 1
        depth_stats[depth]['prompts']['size'] += prompt['size']
    
    for lyric in results['lyrics']:
        depth = lyric['depth']
        depth_stats[depth]['lyrics']['count'] += 1
        depth_stats[depth]['lyrics']['size'] += lyric['size']
    
    for depth in sorted(depth_stats.keys()):
        for file_type in ['mp3', 'prompts', 'lyrics']:
            if file_type in depth_stats[depth]:
                stats = depth_stats[depth][file_type]
                size_mb = stats['size'] / (1024*1024)
                size_gb = size_mb / 1024
                writer.writerow([
                    depth,
                    file_type,
                    stats['count'],
                    round(size_mb, 2),
                    round(size_gb, 2)
                ])

print(f"📊 CSV (By Depth) saved: {csv_file_depth.name}")
print()

# Show top locations
print("=" * 100)
print("📍 TOP MP3 LOCATIONS")
print("=" * 100)
print()

# Group MP3s by directory
mp3_locations = defaultdict(lambda: {'count': 0, 'size': 0, 'avg_depth': []})

for mp3 in results['mp3']:
    directory = mp3['directory']
    mp3_locations[directory]['count'] += 1
    mp3_locations[directory]['size'] += mp3['size']
    mp3_locations[directory]['avg_depth'].append(mp3['depth'])

# Sort by count
sorted_locations = sorted(mp3_locations.items(), key=lambda x: x[1]['count'], reverse=True)

print(f"{'Count':<10} {'Size (GB)':<12} {'Avg Depth':<12} {'Location':<60}")
print("-" * 100)
for loc, data in sorted_locations[:20]:
    size_gb = data['size'] / (1024*1024*1024)
    avg_depth = sum(data['avg_depth']) / len(data['avg_depth']) if data['avg_depth'] else 0
    loc_display = loc[:58] + ".." if len(loc) > 60 else loc
    print(f"{data['count']:<10,} {size_gb:<12.2f} {avg_depth:<12.1f} {loc_display:<60}")

print()
print("=" * 100)
print("✅ SEARCH COMPLETE")
print("=" * 100)
print()
print(f"📁 All reports saved to: {Path.home() / 'Documents'}")
print()
