#!/usr/bin/env python3
"""
Focused analysis of MP3 collection, discography, prompts, lyrics, and duplicates
"""

from pathlib import Path
import csv
from datetime import datetime
from collections import defaultdict
import os

home_dir = Path.home()
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

print("=" * 100)
print("📊 FOCUSED ANALYSIS: MP3 COLLECTION")
print("=" * 100)
print()

# Search patterns
search_patterns = {
    'mp3': ['*.mp3'],
    'discography': ['*discography*', '*disc*', '*album*', '*collection*'],
    'prompts': ['*prompt*', '*prompts*'],
    'lyrics': ['*lyric*', '*lyrics*', '*transcript*', '*transcription*'],
}

results = {
    'mp3': [],
    'discography': [],
    'prompts': [],
    'lyrics': []
}

def get_depth(path, base_path):
    """Calculate depth of path relative to base path"""
    try:
        relative = path.relative_to(base_path)
        return len(relative.parts)
    except:
        return 0

# Search MP3s
print("🔍 Searching MP3s...")
for mp3 in home_dir.rglob("*.mp3"):
    try:
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
    except:
        pass
print(f"   ✅ Found {len(results['mp3']):,} MP3 files")
print()

# Search discography
print("🔍 Searching discography...")
for pattern in search_patterns['discography']:
    for item in home_dir.rglob(pattern):
        try:
            if item.is_file() or item.is_dir():
                depth = get_depth(item, home_dir)
                results['discography'].append({
                    'path': str(item),
                    'name': item.name,
                    'type': 'file' if item.is_file() else 'folder',
                    'depth': depth
                })
        except:
            pass
print(f"   ✅ Found {len(results['discography']):,} discography items")
print()

# Search prompts
print("🔍 Searching prompts...")
for pattern in search_patterns['prompts']:
    for item in home_dir.rglob(pattern):
        try:
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
        except:
            pass
print(f"   ✅ Found {len(results['prompts']):,} prompt files")
print()

# Search lyrics
print("🔍 Searching lyrics...")
for pattern in search_patterns['lyrics']:
    for item in home_dir.rglob(pattern):
        try:
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
        except:
            pass
print(f"   ✅ Found {len(results['lyrics']):,} lyric/transcript files")
print()

# ============================================================================
# MP3 ANALYSIS
# ============================================================================
print("=" * 100)
print("🎵 MP3 FILES ANALYSIS")
print("=" * 100)
print()

mp3_count = len(results['mp3'])
mp3_total_size = sum(f['size'] for f in results['mp3'])
mp3_size_gb = mp3_total_size / (1024*1024*1024)
mp3_size_mb = mp3_total_size / (1024*1024)

print(f"Total: {mp3_count:,} files, {mp3_size_gb:.2f} GB ({mp3_size_mb:.2f} MB)")
print()

# By directory
print("📁 Top 20 Directories by File Count:")
mp3_by_dir = defaultdict(lambda: {'count': 0, 'size': 0})
for mp3 in results['mp3']:
    mp3_by_dir[mp3['directory']]['count'] += 1
    mp3_by_dir[mp3['directory']]['size'] += mp3['size']

sorted_dirs = sorted(mp3_by_dir.items(), key=lambda x: x[1]['count'], reverse=True)
print(f"{'Count':<8} {'Size (GB)':<12} {'Directory':<70}")
print("-" * 100)
for dir_path, data in sorted_dirs[:20]:
    size_gb = data['size'] / (1024*1024*1024)
    dir_display = dir_path[:68] + ".." if len(dir_path) > 70 else dir_path
    print(f"{data['count']:<8,} {size_gb:<12.2f} {dir_display:<70}")
print()

# By depth
print("📏 Distribution by Folder Depth:")
depth_stats = defaultdict(lambda: {'count': 0, 'size': 0})
for mp3 in results['mp3']:
    depth_stats[mp3['depth']]['count'] += 1
    depth_stats[mp3['depth']]['size'] += mp3['size']

print(f"{'Depth':<8} {'Count':<12} {'Size (GB)':<12} {'Avg Size (MB)':<15}")
print("-" * 100)
for depth in sorted(depth_stats.keys()):
    stats = depth_stats[depth]
    size_gb = stats['size'] / (1024*1024*1024)
    avg_mb = (stats['size'] / stats['count']) / (1024*1024) if stats['count'] > 0 else 0
    print(f"{depth:<8} {stats['count']:<12,} {size_gb:<12.2f} {avg_mb:<15.2f}")
print()

# Size distribution
print("📊 Size Distribution:")
size_ranges = {
    'Tiny (< 1 MB)': 0,
    'Small (1-5 MB)': 0,
    'Medium (5-10 MB)': 0,
    'Large (10-20 MB)': 0,
    'Very Large (20-50 MB)': 0,
    'Huge (> 50 MB)': 0
}
for mp3 in results['mp3']:
    size_mb = mp3['size_mb']
    if size_mb < 1:
        size_ranges['Tiny (< 1 MB)'] += 1
    elif size_mb < 5:
        size_ranges['Small (1-5 MB)'] += 1
    elif size_mb < 10:
        size_ranges['Medium (5-10 MB)'] += 1
    elif size_mb < 20:
        size_ranges['Large (10-20 MB)'] += 1
    elif size_mb < 50:
        size_ranges['Very Large (20-50 MB)'] += 1
    else:
        size_ranges['Huge (> 50 MB)'] += 1

for range_name, count in size_ranges.items():
    pct = (count / mp3_count * 100) if mp3_count > 0 else 0
    print(f"   {range_name:<25} {count:>6,} files ({pct:>5.1f}%)")
print()

# ============================================================================
# DUPLICATE ANALYSIS
# ============================================================================
print("=" * 100)
print("🔄 DUPLICATE ANALYSIS")
print("=" * 100)
print()

filename_to_paths = defaultdict(list)
for mp3 in results['mp3']:
    filename = mp3['name']
    filename_to_paths[filename].append(mp3)

duplicates = {k: v for k, v in filename_to_paths.items() if len(v) > 1}
unique_files = {k: v[0] for k, v in filename_to_paths.items() if len(v) == 1}

print(f"Total MP3 files: {mp3_count:,}")
print(f"Unique filenames: {len(filename_to_paths):,}")
print(f"Files with duplicate names: {len(duplicates):,}")
print(f"Total duplicate instances: {sum(len(v) for v in duplicates.values()):,}")
print()

# Top duplicates
print("🔝 Top 20 Most Duplicated Files:")
duplicate_counts = [(k, len(v)) for k, v in duplicates.items()]
duplicate_counts.sort(key=lambda x: x[1], reverse=True)

print(f"{'Copies':<8} {'Filename':<70}")
print("-" * 100)
for filename, count in duplicate_counts[:20]:
    filename_display = filename[:68] + ".." if len(filename) > 70 else filename
    print(f"{count:<8} {filename_display:<70}")
print()

# Duplicates by location
print("📍 Duplicate Locations Analysis:")
dup_locations = defaultdict(int)
for filename, paths_list in duplicates.items():
    for mp3 in paths_list:
        dup_locations[mp3['directory']] += 1

sorted_dup_locs = sorted(dup_locations.items(), key=lambda x: x[1], reverse=True)
print(f"{'Count':<8} {'Directory':<70}")
print("-" * 100)
for dir_path, count in sorted_dup_locs[:15]:
    dir_display = dir_path[:68] + ".." if len(dir_path) > 70 else dir_path
    print(f"{count:<8,} {dir_display:<70}")
print()

# ============================================================================
# DISCOGRAPHY ANALYSIS
# ============================================================================
print("=" * 100)
print("💿 DISCOGRAPHY ANALYSIS")
print("=" * 100)
print()

disc_count = len(results['discography'])
disc_files = [d for d in results['discography'] if d['type'] == 'file']
disc_folders = [d for d in results['discography'] if d['type'] == 'folder']

print(f"Total items: {disc_count:,}")
print(f"   Files: {len(disc_files):,}")
print(f"   Folders: {len(disc_folders):,}")
print()

# By depth
print("📏 Distribution by Folder Depth:")
disc_depth_stats = defaultdict(int)
for item in results['discography']:
    disc_depth_stats[item['depth']] += 1

print(f"{'Depth':<8} {'Count':<12}")
print("-" * 100)
for depth in sorted(disc_depth_stats.keys()):
    print(f"{depth:<8} {disc_depth_stats[depth]:<12,}")
print()

# Top directories
print("📁 Top 15 Discography Locations:")
disc_by_dir = defaultdict(int)
for item in results['discography']:
    if item['type'] == 'file':
        disc_by_dir[os.path.dirname(item['path'])] += 1
    else:
        disc_by_dir[item['path']] += 1

sorted_disc_dirs = sorted(disc_by_dir.items(), key=lambda x: x[1], reverse=True)
print(f"{'Count':<8} {'Location':<70}")
print("-" * 100)
for dir_path, count in sorted_disc_dirs[:15]:
    dir_display = dir_path[:68] + ".." if len(dir_path) > 70 else dir_path
    print(f"{count:<8,} {dir_display:<70}")
print()

# ============================================================================
# PROMPTS ANALYSIS
# ============================================================================
print("=" * 100)
print("📝 PROMPTS ANALYSIS")
print("=" * 100)
print()

prompt_count = len(results['prompts'])
prompt_total_size = sum(f['size'] for f in results['prompts'])
prompt_size_mb = prompt_total_size / (1024*1024)

print(f"Total: {prompt_count:,} files, {prompt_size_mb:.2f} MB")
print()

# By depth
print("📏 Distribution by Folder Depth:")
prompt_depth_stats = defaultdict(lambda: {'count': 0, 'size': 0})
for prompt in results['prompts']:
    prompt_depth_stats[prompt['depth']]['count'] += 1
    prompt_depth_stats[prompt['depth']]['size'] += prompt['size']

print(f"{'Depth':<8} {'Count':<12} {'Size (MB)':<12}")
print("-" * 100)
for depth in sorted(prompt_depth_stats.keys()):
    stats = prompt_depth_stats[depth]
    size_mb = stats['size'] / (1024*1024)
    print(f"{depth:<8} {stats['count']:<12,} {size_mb:<12.2f}")
print()

# Top directories
print("📁 Top 15 Prompt Locations:")
prompt_by_dir = defaultdict(lambda: {'count': 0, 'size': 0})
for prompt in results['prompts']:
    dir_path = os.path.dirname(prompt['path'])
    prompt_by_dir[dir_path]['count'] += 1
    prompt_by_dir[dir_path]['size'] += prompt['size']

sorted_prompt_dirs = sorted(prompt_by_dir.items(), key=lambda x: x[1]['count'], reverse=True)
print(f"{'Count':<8} {'Size (MB)':<12} {'Directory':<70}")
print("-" * 100)
for dir_path, data in sorted_prompt_dirs[:15]:
    size_mb = data['size'] / (1024*1024)
    dir_display = dir_path[:68] + ".." if len(dir_path) > 70 else dir_path
    print(f"{data['count']:<8,} {size_mb:<12.2f} {dir_display:<70}")
print()

# ============================================================================
# LYRICS/TRANSCRIPTS ANALYSIS
# ============================================================================
print("=" * 100)
print("🎤 LYRICS/TRANSCRIPTS ANALYSIS")
print("=" * 100)
print()

lyric_count = len(results['lyrics'])
lyric_total_size = sum(f['size'] for f in results['lyrics'])
lyric_size_mb = lyric_total_size / (1024*1024)

print(f"Total: {lyric_count:,} files, {lyric_size_mb:.2f} MB")
print()

# By depth
print("📏 Distribution by Folder Depth:")
lyric_depth_stats = defaultdict(lambda: {'count': 0, 'size': 0})
for lyric in results['lyrics']:
    lyric_depth_stats[lyric['depth']]['count'] += 1
    lyric_depth_stats[lyric['depth']]['size'] += lyric['size']

print(f"{'Depth':<8} {'Count':<12} {'Size (MB)':<12}")
print("-" * 100)
for depth in sorted(lyric_depth_stats.keys()):
    stats = lyric_depth_stats[depth]
    size_mb = stats['size'] / (1024*1024)
    print(f"{depth:<8} {stats['count']:<12,} {size_mb:<12.2f}")
print()

# Top directories
print("📁 Top 15 Lyrics/Transcript Locations:")
lyric_by_dir = defaultdict(lambda: {'count': 0, 'size': 0})
for lyric in results['lyrics']:
    dir_path = os.path.dirname(lyric['path'])
    lyric_by_dir[dir_path]['count'] += 1
    lyric_by_dir[dir_path]['size'] += lyric['size']

sorted_lyric_dirs = sorted(lyric_by_dir.items(), key=lambda x: x[1]['count'], reverse=True)
print(f"{'Count':<8} {'Size (MB)':<12} {'Directory':<70}")
print("-" * 100)
for dir_path, data in sorted_lyric_dirs[:15]:
    size_mb = data['size'] / (1024*1024)
    dir_display = dir_path[:68] + ".." if len(dir_path) > 70 else dir_path
    print(f"{data['count']:<8,} {size_mb:<12.2f} {dir_display:<70}")
print()

# ============================================================================
# EXPORT CSV FILES
# ============================================================================
print("=" * 100)
print("💾 EXPORTING CSV FILES")
print("=" * 100)
print()

# MP3s with duplicates
csv_mp3 = Path.home() / "Documents" / f"ANALYSIS_MP3_{timestamp}.csv"
with open(csv_mp3, 'w', newline='', encoding='utf-8') as f:
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
            filename, mp3['path'], mp3['directory'], mp3['depth'],
            mp3['size'], mp3['size_mb'], is_duplicate, duplicate_count
        ])

print(f"✅ MP3 Analysis: {csv_mp3.name}")

# Duplicates detailed
csv_dupes = Path.home() / "Documents" / f"ANALYSIS_DUPLICATES_{timestamp}.csv"
with open(csv_dupes, 'w', newline='', encoding='utf-8') as f:
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
                filename, i, mp3['path'], mp3['directory'],
                mp3['depth'], mp3['size'], mp3['size_mb'], total_copies
            ])

print(f"✅ Duplicates: {csv_dupes.name}")

# Discography
csv_disc = Path.home() / "Documents" / f"ANALYSIS_DISCOGRAPHY_{timestamp}.csv"
with open(csv_disc, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'path', 'type', 'depth'])
    
    for item in results['discography']:
        writer.writerow([
            item['name'], item['path'], item['type'], item['depth']
        ])

print(f"✅ Discography: {csv_disc.name}")

# Prompts
csv_prompts = Path.home() / "Documents" / f"ANALYSIS_PROMPTS_{timestamp}.csv"
with open(csv_prompts, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'path', 'depth', 'size_bytes', 'size_mb'])
    
    for prompt in results['prompts']:
        writer.writerow([
            prompt['name'], prompt['path'], prompt['depth'],
            prompt['size'], prompt['size_mb']
        ])

print(f"✅ Prompts: {csv_prompts.name}")

# Lyrics
csv_lyrics = Path.home() / "Documents" / f"ANALYSIS_LYRICS_{timestamp}.csv"
with open(csv_lyrics, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'path', 'depth', 'size_bytes', 'size_mb'])
    
    for lyric in results['lyrics']:
        writer.writerow([
            lyric['name'], lyric['path'], lyric['depth'],
            lyric['size'], lyric['size_mb']
        ])

print(f"✅ Lyrics/Transcripts: {csv_lyrics.name}")

# Summary
csv_summary = Path.home() / "Documents" / f"ANALYSIS_SUMMARY_{timestamp}.csv"
with open(csv_summary, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['category', 'count', 'size_mb', 'size_gb'])
    
    writer.writerow(['MP3', mp3_count, round(mp3_size_mb, 2), round(mp3_size_gb, 2)])
    writer.writerow(['Prompts', prompt_count, round(prompt_size_mb, 2), 0])
    writer.writerow(['Lyrics/Transcripts', lyric_count, round(lyric_size_mb, 2), 0])
    writer.writerow(['Discography', disc_count, 0, 0])
    writer.writerow(['Duplicates (unique)', len(duplicates), 0, 0])
    writer.writerow(['Duplicate instances', sum(len(v) for v in duplicates.values()), 0, 0])

print(f"✅ Summary: {csv_summary.name}")
print()

print("=" * 100)
print("✅ ANALYSIS COMPLETE")
print("=" * 100)
print()
print(f"📁 All CSV files saved to: {Path.home() / 'Documents'}")
print()
