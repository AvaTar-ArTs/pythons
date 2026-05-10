#!/usr/bin/env python3
"""
Analyze related items CSV and suggest organizational improvements
"""

from pathlib import Path
import csv
from datetime import datetime

documents_dir = Path.home() / "Documents"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Find most recent related items CSV
csv_files = sorted(documents_dir.glob("RELATED_ITEMS_20251126_*.csv"), reverse=True)
if not csv_files:
    print("❌ No RELATED_ITEMS CSV file found.")
    exit(1)

csv_file = csv_files[0]
print("=" * 100)
print("📊 ANALYZING RELATED ITEMS AND SUGGESTING IMPROVEMENTS")
print("=" * 100)
print(f"📄 Analyzing: {csv_file.name}")
print()

# Load data
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Loaded {len(rows)} groups")
print()

# Analysis
analysis = {
    'total_groups': len(rows),
    'groups_with_mp3s': 0,
    'groups_with_lyrics': 0,
    'groups_with_prompts': 0,
    'groups_with_discography': 0,
    'groups_with_multiple_types': 0,
    'mp3s_no_lyrics': [],
    'lyrics_no_mp3s': [],
    'orphaned_lyrics': [],
    'orphaned_prompts': [],
    'large_mp3_collections': [],
    'well_organized': []
}

for row in rows:
    mp3_count = int(row['mp3_count'])
    lyric_count = int(row['lyric_count'])
    prompt_count = int(row['prompt_count'])
    discography_count = int(row['discography_count'])
    total_items = int(row['total_items'])
    
    # Count types
    type_count = sum([
        mp3_count > 0,
        lyric_count > 0,
        prompt_count > 0,
        discography_count > 0
    ])
    
    if mp3_count > 0:
        analysis['groups_with_mp3s'] += 1
    if lyric_count > 0:
        analysis['groups_with_lyrics'] += 1
    if prompt_count > 0:
        analysis['groups_with_prompts'] += 1
    if discography_count > 0:
        analysis['groups_with_discography'] += 1
    if type_count > 1:
        analysis['groups_with_multiple_types'] += 1
    
    # Identify issues
    if mp3_count > 0 and lyric_count == 0:
        analysis['mp3s_no_lyrics'].append(row)
    if lyric_count > 0 and mp3_count == 0:
        analysis['lyrics_no_mp3s'].append(row)
    if lyric_count > 5 and mp3_count == 0:
        analysis['orphaned_lyrics'].append(row)
    if prompt_count > 5 and mp3_count == 0:
        analysis['orphaned_prompts'].append(row)
    if mp3_count > 50:
        analysis['large_mp3_collections'].append(row)
    if mp3_count > 0 and lyric_count > 0 and type_count >= 2:
        analysis['well_organized'].append(row)

# Print analysis
print("=" * 100)
print("📊 ANALYSIS RESULTS")
print("=" * 100)
print()

print(f"Total groups: {analysis['total_groups']:,}")
print(f"Groups with MP3s: {analysis['groups_with_mp3s']:,}")
print(f"Groups with Lyrics: {analysis['groups_with_lyrics']:,}")
print(f"Groups with Prompts: {analysis['groups_with_prompts']:,}")
print(f"Groups with Discography: {analysis['groups_with_discography']:,}")
print(f"Groups with multiple types: {analysis['groups_with_multiple_types']:,}")
print()

print("=" * 100)
print("🔍 IDENTIFIED ISSUES")
print("=" * 100)
print()

print(f"1. MP3s without lyrics: {len(analysis['mp3s_no_lyrics']):,} groups")
print("   These MP3s might benefit from lyric files")
print()

print(f"2. Lyrics without MP3s: {len(analysis['lyrics_no_mp3s']):,} groups")
print("   These lyrics might be orphaned or MP3s are elsewhere")
print()

print(f"3. Large orphaned lyric collections: {len(analysis['orphaned_lyrics']):,} groups")
print("   These have 5+ lyrics but no MP3s")
print()

print(f"4. Large orphaned prompt collections: {len(analysis['orphaned_prompts']):,} groups")
print("   These have 5+ prompts but no MP3s")
print()

print(f"5. Large MP3 collections: {len(analysis['large_mp3_collections']):,} groups")
print("   These have 50+ MP3s and might need sub-organization")
print()

print(f"6. Well-organized groups: {len(analysis['well_organized']):,} groups")
print("   These have MP3s + lyrics + other content")
print()

# Detailed suggestions
print("=" * 100)
print("💡 SUGGESTIONS")
print("=" * 100)
print()

# Suggestion 1: Large MP3 collections
if analysis['large_mp3_collections']:
    print("1. 📁 LARGE MP3 COLLECTIONS (Consider sub-organization):")
    print("-" * 100)
    for i, row in enumerate(sorted(analysis['large_mp3_collections'], 
                                   key=lambda x: int(x['mp3_count']), reverse=True)[:10], 1):
        print(f"   {i}. {row['base_directory']}")
        print(f"      {row['mp3_count']} MP3s, {row['total_size_mb']} MB")
        print("      💡 Consider organizing by artist, album, or genre")
    print()

# Suggestion 2: Orphaned lyrics
if analysis['orphaned_lyrics']:
    print("2. 🎤 ORPHANED LYRICS (MP3s might be elsewhere):")
    print("-" * 100)
    for i, row in enumerate(sorted(analysis['orphaned_lyrics'], 
                                   key=lambda x: int(x['lyric_count']), reverse=True)[:10], 1):
        print(f"   {i}. {row['base_directory']}")
        print(f"      {row['lyric_count']} lyrics, no MP3s")
        print("      💡 Search for matching MP3s or move lyrics to MP3 location")
    print()

# Suggestion 3: MP3s without lyrics
if analysis['mp3s_no_lyrics']:
    print("3. 🎵 MP3s WITHOUT LYRICS (Consider adding lyrics):")
    print("-" * 100)
    top_mp3s_no_lyrics = sorted(analysis['mp3s_no_lyrics'], 
                               key=lambda x: int(x['mp3_count']), reverse=True)[:10]
    for i, row in enumerate(top_mp3s_no_lyrics, 1):
        print(f"   {i}. {row['base_directory']}")
        print(f"      {row['mp3_count']} MP3s, 0 lyrics")
        if int(row['mp3_count']) > 10:
            print("      💡 Large collection - consider transcribing or finding lyrics")
    print()

# Suggestion 4: Well-organized examples
if analysis['well_organized']:
    print("4. ✅ WELL-ORGANIZED GROUPS (Good examples to follow):")
    print("-" * 100)
    for i, row in enumerate(sorted(analysis['well_organized'], 
                                   key=lambda x: int(x['total_items']), reverse=True)[:10], 1):
        print(f"   {i}. {row['base_directory']}")
        print(f"      {row['mp3_count']} MP3s, {row['lyric_count']} lyrics, "
              f"{row['prompt_count']} prompts, {row['discography_count']} discography")
        print("      ✅ Good organization - all related content together")
    print()

# Create suggestions CSV
suggestions_file = documents_dir / f"ORGANIZATION_SUGGESTIONS_{timestamp}.csv"
with open(suggestions_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'suggestion_type', 'priority', 'base_directory', 'mp3_count', 'lyric_count',
        'prompt_count', 'discography_count', 'total_items', 'total_size_mb', 'suggestion'
    ])
    
    # Large collections
    for row in sorted(analysis['large_mp3_collections'], 
                     key=lambda x: int(x['mp3_count']), reverse=True):
        writer.writerow([
            'Large MP3 Collection',
            'Medium',
            row['base_directory'],
            row['mp3_count'],
            row['lyric_count'],
            row['prompt_count'],
            row['discography_count'],
            row['total_items'],
            row['total_size_mb'],
            'Consider organizing by artist/album/genre into subfolders'
        ])
    
    # Orphaned lyrics
    for row in sorted(analysis['orphaned_lyrics'], 
                     key=lambda x: int(x['lyric_count']), reverse=True):
        writer.writerow([
            'Orphaned Lyrics',
            'High',
            row['base_directory'],
            row['mp3_count'],
            row['lyric_count'],
            row['prompt_count'],
            row['discography_count'],
            row['total_items'],
            row['total_size_mb'],
            'Search for matching MP3s or move lyrics to MP3 location'
        ])
    
    # MP3s without lyrics
    for row in sorted(analysis['mp3s_no_lyrics'], 
                     key=lambda x: int(x['mp3_count']), reverse=True)[:50]:
        if int(row['mp3_count']) > 5:
            writer.writerow([
                'MP3s Without Lyrics',
                'Low',
                row['base_directory'],
                row['mp3_count'],
                row['lyric_count'],
                row['prompt_count'],
                row['discography_count'],
                row['total_items'],
                row['total_size_mb'],
                'Consider adding lyrics or transcriptions'
            ])

print(f"📄 Suggestions CSV saved: {suggestions_file.name}")
print()

# Summary recommendations
print("=" * 100)
print("🎯 SUMMARY RECOMMENDATIONS")
print("=" * 100)
print()

recommendations = []

if len(analysis['large_mp3_collections']) > 0:
    recommendations.append(f"• Organize {len(analysis['large_mp3_collections'])} large MP3 collections into subfolders")

if len(analysis['orphaned_lyrics']) > 0:
    recommendations.append(f"• Investigate {len(analysis['orphaned_lyrics'])} orphaned lyric collections - find matching MP3s")

if len(analysis['mp3s_no_lyrics']) > 10:
    recommendations.append(f"• Consider adding lyrics to {len(analysis['mp3s_no_lyrics'])} MP3 collections without lyrics")

if len(analysis['well_organized']) > 0:
    recommendations.append(f"• {len(analysis['well_organized'])} groups are well-organized - use as examples")

if not recommendations:
    recommendations.append("• Your collection is already well-organized! ✅")

for rec in recommendations:
    print(rec)

print()
print("=" * 100)
print("✅ ANALYSIS COMPLETE")
print("=" * 100)

