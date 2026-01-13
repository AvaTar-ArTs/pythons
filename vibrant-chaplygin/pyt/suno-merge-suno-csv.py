#!/usr/bin/env python3
"""
?? SUNO CSV COMPARATOR & MERGER
================================
Compares and merges all Suno CSV files to find unique songs

Usage:
    python suno_csv_comparator.py
    python suno_csv_comparator.py --output master_suno_collection.csv
"""

import argparse
import csv
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set
from collections import defaultdict

def extract_song_id(url: str) -> str:
    """Extract song ID from various URL formats"""
    if not url:
        return ''
    
    # Try to extract UUID from URL
    patterns = [
        r'/song/([a-f0-9-]{36})',
        r'/s/([a-f0-9]+)',
        r'cdn1\.suno\.ai/([a-f0-9-]{36})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, str(url))
        if match:
            return match.group(1)
    
    return ''

def read_csv_file(filepath: Path) -> List[Dict]:
    """Read CSV file and return list of songs"""
    songs = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Try to detect if first char is BOM
            first_char = f.read(1)
            if first_char != '\ufeff':
                f.seek(0)
            
            reader = csv.DictReader(f)
            for row in reader:
                # Clean up keys (remove quotes, BOM, etc)
                cleaned_row = {}
                for key, value in row.items():
                    clean_key = key.strip().strip('"').strip('\ufeff')
                    cleaned_row[clean_key] = value
                
                # Add source file
                cleaned_row['_source_file'] = filepath.name
                songs.append(cleaned_row)
                
    except Exception as e:
        print(f"   ??  Error reading {filepath.name}: {e}")
    
    return songs

def normalize_song_data(song: Dict) -> Dict:
    """Normalize song data with standard field names"""
    normalized = {
        'id': '',
        'title': '',
        'url': '',
        'audioUrl': '',
        'imageUrl': '',
        'duration': '',
        'author': '',
        'authorLink': '',
        'published': '',
        'plays': '',
        'likes': '',
        'style': '',
        'lyrics': '',
        'version': '',
        'playlist': '',
        'sourceFiles': song.get('_source_file', ''),
    }
    
    # Map various field names to standard names
    field_mappings = {
        'id': ['id', 'songId'],
        'title': ['title', 'songName', 'songtitle', 'songname'],
        'url': ['url', 'songLink', 'songlink', 'songurl'],
        'audioUrl': ['audioUrl', 'audio_url'],
        'imageUrl': ['imageUrl', 'image_url', 'coverurl'],
        'duration': ['duration', 'length'],
        'author': ['author', 'artist', 'display_name'],
        'authorLink': ['authorLink', 'authorlink'],
        'published': ['published', 'created_at'],
        'plays': ['plays', 'views', 'play_count'],
        'likes': ['likes', 'upvote_count'],
        'style': ['style', 'tags', 'source_labels'],
        'lyrics': ['lyrics', 'prompt'],
        'version': ['version', 'modelVersion', 'model_name'],
        'playlist': ['playlist'],
    }
    
    for std_field, variants in field_mappings.items():
        for variant in variants:
            if variant in song and song[variant]:
                normalized[std_field] = song[variant]
                break
    
    # Try to extract ID from URL if not present
    if not normalized['id']:
        normalized['id'] = extract_song_id(normalized['url'])
    
    return normalized

def find_suno_csvs() -> List[Path]:
    """Find all Suno CSV files"""
    search_paths = [
        Path.home() / 'Documents' / 'CsV',
        Path.home() / 'Documents' / 'pythons' / 'suno_tools',
        Path.home() / 'Documents' / 'pythons',
        Path.home() / 'Downloads',
    ]
    
    csv_files = []
    
    for search_path in search_paths:
        if search_path.exists():
            csv_files.extend(search_path.rglob('*suno*.csv'))
            csv_files.extend(search_path.rglob('*Suno*.csv'))
    
    # Remove duplicates
    return list(set(csv_files))

def main():
    parser = argparse.ArgumentParser(
        description='?? Compare and merge all Suno CSV files',
    )
    
    parser.add_argument('--output', '-o', default='suno_master_collection.csv',
                       help='Output CSV file (default: suno_master_collection.csv)')
    parser.add_argument('--report', action='store_true',
                       help='Generate detailed comparison report')
    
    args = parser.parse_args()
    
    print("?? Finding all Suno CSV files...\n")
    
    csv_files = find_suno_csvs()
    
    if not csv_files:
        print("? No Suno CSV files found!")
        return
    
    print(f"?? Found {len(csv_files)} CSV files:\n")
    
    # Read all CSV files
    all_songs = []
    file_stats = {}
    
    for csv_file in sorted(csv_files):
        print(f"?? {csv_file.name}")
        songs = read_csv_file(csv_file)
        
        file_stats[csv_file.name] = {
            'songs': len(songs),
            'size': csv_file.stat().st_size / 1024,
        }
        
        print(f"   Songs: {len(songs)}")
        print(f"   Size: {csv_file.stat().st_size / 1024:.1f} KB\n")
        
        all_songs.extend(songs)
    
    print(f"?? Total songs loaded: {len(all_songs)}\n")
    
    # Normalize all songs
    print("?? Normalizing song data...")
    normalized_songs = [normalize_song_data(song) for song in all_songs]
    
    # Deduplicate by ID
    print("?? Deduplicating songs...")
    
    unique_songs = {}
    id_sources = defaultdict(list)
    
    for song in normalized_songs:
        song_id = song['id']
        
        if not song_id:
            continue
        
        id_sources[song_id].append(song['sourceFiles'])
        
        if song_id not in unique_songs:
            unique_songs[song_id] = song
        else:
            # Merge: prefer non-empty fields
            existing = unique_songs[song_id]
            for key, value in song.items():
                if value and not existing.get(key):
                    existing[key] = value
            
            # Combine source files
            sources = set(existing['sourceFiles'].split(', '))
            sources.add(song['sourceFiles'])
            existing['sourceFiles'] = ', '.join(sorted(sources))
    
    unique_list = list(unique_songs.values())
    
    print(f"? Unique songs: {len(unique_list)}")
    print(f"?? Duplicates removed: {len(normalized_songs) - len(unique_list)}\n")
    
    # Save to CSV
    output_path = Path(args.output)
    
    if unique_list:
        fieldnames = list(unique_list[0].keys())
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(unique_list)
        
        print(f"? Saved {len(unique_list)} unique songs to: {output_path}")
        print(f"?? File size: {output_path.stat().st_size / 1024:.1f} KB\n")
    
    # Generate report
    print("="*70)
    print("?? COMPARISON SUMMARY")
    print("="*70)
    print(f"\n?? Files analyzed: {len(csv_files)}")
    print(f"?? Total songs (all files): {len(all_songs)}")
    print(f"?? Unique songs: {len(unique_list)}")
    print(f"??  Duplicates: {len(all_songs) - len(unique_list)}")
    print(f"?? Output file: {output_path}")
    
    # Show top source files
    source_counts = defaultdict(int)
    for sources_list in id_sources.values():
        for source in sources_list:
            source_counts[source] += 1
    
    print(f"\n?? Top 10 source files by song count:")
    for i, (source, count) in enumerate(sorted(source_counts.items(), 
                                               key=lambda x: x[1], 
                                               reverse=True)[:10], 1):
        print(f"   {i:2d}. {source}: {count} songs")
    
    # Show songs found in multiple files
    multi_source = {k: v for k, v in id_sources.items() if len(v) > 1}
    if multi_source:
        print(f"\n?? Songs found in multiple files: {len(multi_source)}")
        print(f"   Example: {list(multi_source.keys())[0]}")
        print(f"   Found in: {len(list(multi_source.values())[0])} files")
    
    # Show sample songs
    print(f"\n?? Sample of unique songs:")
    for i, song in enumerate(unique_list[:5], 1):
        print(f"\n   {i}. {song['title']}")
        if song['author']:
            print(f"      By: {song['author']}")
        if song['duration']:
            print(f"      Duration: {song['duration']}")
        if song['style']:
            style_preview = song['style'][:50] + '...' if len(song['style']) > 50 else song['style']
            print(f"      Style: {style_preview}")
        print(f"      Sources: {song['sourceFiles']}")
    
    print(f"\n{'='*70}\n")
    
    # Detailed report if requested
    if args.report:
        report_path = output_path.with_suffix('.report.txt')
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("?? SUNO CSV COMPARISON REPORT\n")
            f.write("="*70 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"FILES ANALYZED ({len(csv_files)}):\n")
            f.write("-"*70 + "\n")
            for filename, stats in sorted(file_stats.items()):
                f.write(f"\n{filename}\n")
                f.write(f"  Songs: {stats['songs']}\n")
                f.write(f"  Size: {stats['size']:.1f} KB\n")
            
            f.write(f"\n\nSUMMARY:\n")
            f.write("-"*70 + "\n")
            f.write(f"Total songs (all files): {len(all_songs)}\n")
            f.write(f"Unique songs: {len(unique_list)}\n")
            f.write(f"Duplicates: {len(all_songs) - len(unique_list)}\n")
            
            f.write(f"\n\nDUPLICATE ANALYSIS:\n")
            f.write("-"*70 + "\n")
            for song_id, sources in sorted(multi_source.items(), 
                                          key=lambda x: len(x[1]), 
                                          reverse=True)[:20]:
                song_title = unique_songs[song_id]['title']
                f.write(f"\n{song_title}\n")
                f.write(f"  ID: {song_id}\n")
                f.write(f"  Found in {len(sources)} files:\n")
                for source in sources:
                    f.write(f"    - {source}\n")
        
        print(f"?? Detailed report saved to: {report_path}\n")

if __name__ == '__main__':
    main()
