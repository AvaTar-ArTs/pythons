#!/usr/bin/env python3
"""
Reanalyze ALL Metadata in ~/music
Deep scan of lowercase music folder for complete understanding
"""

import csv
from pathlib import Path
import subprocess
import json
from collections import defaultdict
import hashlib

def get_file_hash(filepath: Path) -> str:
    """Get MD5 hash"""
    try:
        md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            md5.update(f.read(8192))
        return md5.hexdigest()[:8]
    except Exception:
        return ""

def extract_full_metadata(filepath: Path) -> dict:
    """Extract complete metadata from audio file"""
    if not filepath.exists():
        return {}
    
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-print_format', 'json',
             '-show_format', '-show_streams', str(filepath)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            format_info = data.get('format', {})
            tags = format_info.get('tags', {})
            
            return {
                'duration': float(format_info.get('duration', 0)),
                'size': int(format_info.get('size', 0)),
                'bitrate': int(format_info.get('bit_rate', 0)),
                'format': format_info.get('format_name', ''),
                'title': tags.get('title', '') or tags.get('TITLE', ''),
                'artist': tags.get('artist', '') or tags.get('ARTIST', ''),
                'album': tags.get('album', '') or tags.get('ALBUM', ''),
                'album_artist': tags.get('album_artist', '') or tags.get('ALBUM_ARTIST', ''),
                'genre': tags.get('genre', '') or tags.get('GENRE', ''),
                'date': tags.get('date', '') or tags.get('DATE', ''),
                'comment': tags.get('comment', '') or tags.get('COMMENT', ''),
                'track': tags.get('track', '') or tags.get('TRACK', ''),
            }
    except Exception as e:
        return {}

def format_duration(seconds: float) -> str:
    """Format duration"""
    if seconds == 0:
        return "0:00"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"

def classify_content_type(duration: float) -> str:
    """Classify by duration"""
    if duration == 0:
        return 'UNKNOWN'
    elif duration < 30:
        return 'SHORT_CLIP'
    elif 30 <= duration <= 360:
        return 'SONG'
    elif 360 < duration <= 900:
        return 'EXTENDED'
    elif 900 < duration <= 1800:
        return 'PODCAST/STORY'
    else:
        return 'AUDIOBOOK/LONG'

def is_your_music(artist: str, album: str, filepath: str) -> bool:
    """Determine if this is YOUR music"""
    
    # Check path
    if any(term in filepath for term in ['YOUR_SUNO', 'avatararts', 'AvaTar']):
        return True
    
    # Check artist
    if artist:
        artist_lower = artist.lower()
        if any(term in artist_lower for term in ['avatar', 'avatararts', 'steven chaplinski', 'ava tar']):
            return True
        if artist.strip() in ['1', '2', '3', 'Ai', 'Music', 'Meeso']:
            return True
    
    # Check album
    if album:
        album_lower = album.lower()
        if any(term in album_lower for term in ['steven chaplinski', 'avatar', 'suno']):
            return True
    
    return False

def main():
    print("\n" + "??" * 40)
    print("  REANALYZE ALL METADATA IN ~/music")
    print("  Complete deep scan")
    print("??" * 40 + "\n")
    
    home = Path.home()
    music_dir = home / 'music'
    
    if not music_dir.exists():
        print(f"? ~/music not found")
        return
    
    # Find all audio files
    print("Finding all audio files...\n")
    
    audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac', '.m4r'}
    audio_files = []
    
    for ext in audio_extensions:
        files = list(music_dir.rglob(f'*{ext}'))
        if files:
            print(f"  Found {len(files)} {ext} files")
            audio_files.extend(files)
    
    print(f"\n? Total audio files: {len(audio_files)}\n")
    
    # Analyze each file
    print("Analyzing metadata...\n")
    
    analyzed = []
    
    for i, audio_file in enumerate(audio_files):
        if (i + 1) % 100 == 0:
            print(f"  Processing {i + 1}/{len(audio_files)}...")
        
        metadata = extract_full_metadata(audio_file)
        
        # Determine location type
        rel_path = str(audio_file.relative_to(music_dir))
        
        if 'nocTurneMeLoDieS' in rel_path:
            location = 'nocTurneMeLoDieS'
        elif 'Other_Content' in rel_path:
            location = 'Other_Content'
        elif '_OLD_' in rel_path or '_ARCHIVED_' in rel_path:
            location = 'ARCHIVED'
        else:
            location = 'ROOT'
        
        analyzed.append({
            'filepath': str(audio_file),
            'filename': audio_file.name,
            'relative_path': rel_path,
            'location': location,
            'parent_folder': audio_file.parent.name,
            'metadata': metadata,
            'file_hash': get_file_hash(audio_file),
            'is_yours': is_your_music(
                metadata.get('artist', ''),
                metadata.get('album', ''),
                str(audio_file)
            ),
            'content_type': classify_content_type(metadata.get('duration', 0))
        })
    
    print(f"\n? Analyzed {len(analyzed)} files\n")
    
    # Save comprehensive report
    print("Saving metadata analysis...\n")
    
    output = home / 'Music/nocTurneMeLoDieS/DATA/MUSIC_FOLDER_METADATA_COMPLETE.csv'
    output.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Filename', 'Filepath', 'Location', 'Parent_Folder',
            'Title', 'Artist', 'Album', 'Album_Artist', 'Genre', 'Track',
            'Duration', 'Duration_Formatted', 'Size_MB', 'Bitrate_kbps',
            'Format', 'File_Hash',
            'Content_Type', 'Is_Your_Music',
            'Has_Title', 'Has_Artist', 'Has_Album', 'Has_Genre',
            'Metadata_Quality', 'Relative_Path'
        ])
        
        for item in analyzed:
            meta = item['metadata']
            duration = meta.get('duration', 0)
            
            # Calculate metadata quality
            has_title = bool(meta.get('title'))
            has_artist = bool(meta.get('artist'))
            has_album = bool(meta.get('album'))
            has_genre = bool(meta.get('genre'))
            
            quality_score = sum([has_title, has_artist, has_album, has_genre])
            
            if quality_score == 4:
                metadata_quality = 'COMPLETE'
            elif quality_score >= 2:
                metadata_quality = 'GOOD'
            elif quality_score == 1:
                metadata_quality = 'BASIC'
            else:
                metadata_quality = 'NONE'
            
            writer.writerow([
                item['filename'],
                item['filepath'],
                item['location'],
                item['parent_folder'],
                meta.get('title', ''),
                meta.get('artist', ''),
                meta.get('album', ''),
                meta.get('album_artist', ''),
                meta.get('genre', ''),
                meta.get('track', ''),
                f"{duration:.1f}",
                format_duration(duration),
                f"{meta.get('size', 0) / 1024 / 1024:.2f}",
                f"{meta.get('bitrate', 0) / 1000:.0f}",
                meta.get('format', ''),
                item['file_hash'],
                item['content_type'],
                'YES' if item['is_yours'] else 'NO',
                'YES' if has_title else 'NO',
                'YES' if has_artist else 'NO',
                'YES' if has_album else 'NO',
                'YES' if has_genre else 'NO',
                metadata_quality,
                item['relative_path']
            ])
    
    print(f"? Saved to: {output}\n")
    
    # Statistics
    print("=" * 80)
    print("  ?? METADATA ANALYSIS STATISTICS")
    print("=" * 80 + "\n")
    
    by_location = defaultdict(int)
    by_content_type = defaultdict(int)
    by_metadata_quality = defaultdict(int)
    your_music = 0
    others_music = 0
    
    for item in analyzed:
        by_location[item['location']] += 1
        by_content_type[item['content_type']] += 1
        
        meta = item['metadata']
        quality_score = sum([
            bool(meta.get('title')),
            bool(meta.get('artist')),
            bool(meta.get('album')),
            bool(meta.get('genre'))
        ])
        
        if quality_score == 4:
            by_metadata_quality['COMPLETE'] += 1
        elif quality_score >= 2:
            by_metadata_quality['GOOD'] += 1
        elif quality_score == 1:
            by_metadata_quality['BASIC'] += 1
        else:
            by_metadata_quality['NONE'] += 1
        
        if item['is_yours']:
            your_music += 1
        else:
            others_music += 1
    
    print(f"Total files: {len(analyzed)}\n")
    
    print("By location:")
    for loc, count in sorted(by_location.items(), key=lambda x: -x[1]):
        print(f"  {loc}: {count}")
    print()
    
    print("By content type:")
    for ct, count in sorted(by_content_type.items(), key=lambda x: -x[1]):
        print(f"  {ct}: {count}")
    print()
    
    print("By metadata quality:")
    for qual, count in sorted(by_metadata_quality.items()):
        print(f"  {qual}: {count}")
    print()
    
    print("Ownership:")
    print(f"  YOUR music (AvaTar ArTs): {your_music}")
    print(f"  OTHERS' music: {others_music}")
    print()
    
    print("=" * 80)
    print("  ? METADATA REANALYSIS COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"?? Complete metadata: {output}\n")
    
    print("Filter by:")
    print("  ? Location - nocTurneMeLoDieS, Other_Content, ARCHIVED, ROOT")
    print("  ? Is_Your_Music - YES/NO")
    print("  ? Content_Type - SONG, SHORT_CLIP, EXTENDED, etc.")
    print("  ? Metadata_Quality - COMPLETE, GOOD, BASIC, NONE")
    print()
    
    print(f"Open: open '{output}'")

if __name__ == '__main__':
    main()
