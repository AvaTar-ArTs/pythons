#!/usr/bin/env python3
"""
?? SUNO HTML BATCH EXTRACTOR
============================
Extracts song data from saved Suno HTML files and outputs to CSV

Usage:
    python suno_html_batch_extractor.py
    python suno_html_batch_extractor.py --dir ~/Documents/HTML
    python suno_html_batch_extractor.py --file specific_file.html
"""

import argparse
import csv
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set
from bs4 import BeautifulSoup

def extract_from_html(html_path: Path) -> List[Dict]:
    """Extract song data from a single HTML file"""
    print(f"?? Processing: {html_path.name}")
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"   ? Error reading file: {e}")
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    songs = []
    extracted_ids: Set[str] = set()
    
    # Method 1: Extract from Next.js data (best method)
    next_data = soup.find('script', id='__NEXT_DATA__')
    if next_data:
        try:
            data = json.loads(next_data.string)
            props = data.get('props', {}).get('pageProps', {})
            
            # Try different data paths
            clips = (
                props.get('clips') or 
                props.get('playlist', {}).get('clips') or
                props.get('songs') or
                props.get('library', {}).get('clips') or
                []
            )
            
            for clip in clips:
                song_id = clip.get('id', '')
                if not song_id or song_id in extracted_ids:
                    continue
                extracted_ids.add(song_id)
                
                songs.append({
                    'id': song_id,
                    'title': clip.get('title', ''),
                    'url': f"https://suno.com/song/{song_id}",
                    'shareUrl': f"https://suno.com/s/{song_id.split('-')[0]}",
                    'audioUrl': clip.get('audio_url') or f"https://cdn1.suno.ai/{song_id}.mp3",
                    'imageUrl': clip.get('image_url') or clip.get('image_large_url', ''),
                    'videoUrl': clip.get('video_url', ''),
                    'duration': format_duration(clip.get('duration', 0)),
                    'author': clip.get('display_name', ''),
                    'authorHandle': clip.get('handle', ''),
                    'authorLink': f"https://suno.com/@{clip.get('handle', '')}" if clip.get('handle') else '',
                    'published': clip.get('created_at', ''),
                    'plays': clip.get('play_count', 0),
                    'likes': clip.get('upvote_count', 0),
                    'tags': ', '.join(clip.get('metadata', {}).get('tags', [])),
                    'prompt': clip.get('metadata', {}).get('prompt', ''),
                    'lyrics': clip.get('metadata', {}).get('prompt', ''),  # Suno calls it prompt
                    'isPublic': clip.get('is_public', False),
                    'modelVersion': clip.get('model_name', ''),
                    'sourceFile': html_path.name,
                })
            
            if songs:
                print(f"   ? Found {len(songs)} songs via Next.js data")
                return songs
                
        except (json.JSONDecodeError, KeyError, AttributeError) as e:
            print(f"   ??  Could not parse Next.js data: {e}")
    
    # Method 2: Extract from HTML structure (fallback)
    song_links = soup.find_all('a', href=re.compile(r'/song/[a-f0-9-]{36}'))
    
    for link in song_links:
        href = link.get('href', '')
        match = re.search(r'/song/([a-f0-9-]{36})', href)
        
        if not match:
            continue
        
        song_id = match.group(1)
        if song_id in extracted_ids:
            continue
        extracted_ids.add(song_id)
        
        # Get title
        title = (
            link.get('title') or 
            link.get_text(strip=True) or
            'Untitled'
        )
        
        # Try to find container for more data
        container = link.find_parent()
        
        # Extract duration
        duration = ''
        if container:
            duration_el = container.find(class_=re.compile(r'font-mono'))
            if duration_el:
                time_match = re.search(r'\d+:\d+', duration_el.get_text())
                if time_match:
                    duration = time_match.group(0)
        
        # Extract image
        image_url = ''
        if container:
            img = container.find('img', src=re.compile(r'suno'))
            if img:
                image_url = img.get('src') or img.get('data-src', '')
        
        # Extract tags
        tags = ''
        if container:
            tag_links = container.find_all('a', href=re.compile(r'/style/'))
            if tag_links:
                tags = ', '.join(t.get_text(strip=True) for t in tag_links)
        
        # Extract author
        author = ''
        author_link = ''
        if container:
            author_el = container.find('a', href=re.compile(r'/@'))
            if author_el:
                author = author_el.get_text(strip=True)
                author_link = author_el.get('href', '')
        
        songs.append({
            'id': song_id,
            'title': title,
            'url': f"https://suno.com/song/{song_id}",
            'shareUrl': f"https://suno.com/s/{song_id.split('-')[0]}",
            'audioUrl': f"https://cdn1.suno.ai/{song_id}.mp3",
            'imageUrl': image_url,
            'videoUrl': '',
            'duration': duration,
            'author': author,
            'authorLink': author_link,
            'tags': tags,
            'sourceFile': html_path.name,
        })
    
    if songs:
        print(f"   ? Found {len(songs)} songs via HTML parsing")
    else:
        print(f"   ??  No songs found in this file")
    
    return songs


def format_duration(seconds: float) -> str:
    """Format duration as MM:SS"""
    if not seconds:
        return ''
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


def find_suno_html_files(directory: Path) -> List[Path]:
    """Find all Suno HTML files in directory"""
    patterns = ['*suno*.html', '*Suno*.html']
    files = []
    
    for pattern in patterns:
        files.extend(directory.rglob(pattern))
    
    # Remove duplicates
    return list(set(files))


def save_to_csv(songs: List[Dict], output_file: Path) -> None:
    """Save songs to CSV"""
    if not songs:
        print("? No songs to save!")
        return
    
    # Get all field names
    fieldnames = set()
    for song in songs:
        fieldnames.update(song.keys())
    fieldnames = sorted(fieldnames)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(songs)
    
    file_size = output_file.stat().st_size / 1024
    print(f"\n? Saved {len(songs)} songs to: {output_file}")
    print(f"?? File size: {file_size:.1f} KB")


def main():
    parser = argparse.ArgumentParser(
        description='?? Suno HTML Batch Extractor - Extract from saved HTML files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument('--dir', help='Directory to search for HTML files (default: ~/Documents/HTML)')
    parser.add_argument('--file', help='Single HTML file to process')
    parser.add_argument('--output', '-o', help='Output CSV file (default: auto-generated)')
    parser.add_argument('--recursive', '-r', action='store_true', help='Search directories recursively')
    
    args = parser.parse_args()
    
    # Determine files to process
    html_files = []
    
    if args.file:
        html_files = [Path(args.file)]
    else:
        search_dir = Path(args.dir) if args.dir else Path.home() / 'Documents' / 'HTML'
        if not search_dir.exists():
            print(f"? Directory not found: {search_dir}")
            return
        
        print(f"?? Searching for Suno HTML files in: {search_dir}")
        html_files = find_suno_html_files(search_dir)
    
    if not html_files:
        print("? No Suno HTML files found!")
        return
    
    print(f"?? Found {len(html_files)} HTML file(s)\n")
    
    # Extract from all files
    all_songs = []
    song_ids = set()
    
    for html_file in sorted(html_files):
        songs = extract_from_html(html_file)
        
        # Remove duplicates across files
        for song in songs:
            if song['id'] not in song_ids:
                song_ids.add(song['id'])
                all_songs.append(song)
    
    if not all_songs:
        print("\n? No songs extracted from any files!")
        return
    
    # Generate output filename
    if not args.output:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        args.output = f"suno_extracted_{timestamp}.csv"
    
    output_path = Path(args.output)
    
    # Save to CSV
    save_to_csv(all_songs, output_path)
    
    # Print summary
    print(f"\n{'='*70}")
    print(f"?? EXTRACTION COMPLETE!")
    print(f"{'='*70}")
    print(f"   ?? Files processed: {len(html_files)}")
    print(f"   ?? Total songs: {len(all_songs)}")
    print(f"   ?? Output file: {output_path}")
    print(f"{'='*70}\n")
    
    # Show sample
    if all_songs:
        print("?? First 5 songs:")
        for i, song in enumerate(all_songs[:5], 1):
            print(f"   {i}. {song['title']}")
            if song.get('author'):
                print(f"      By: {song['author']}")
            if song.get('duration'):
                print(f"      Duration: {song['duration']}")


if __name__ == '__main__':
    main()
