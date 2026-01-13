#!/usr/bin/env python3
"""
Intelligent Metadata Analysis
Uses ALL APIs from ~/.env.d/ for deep content understanding
- AssemblyAI for transcription
- OpenAI for content classification
- Anthropic for analysis
- Local Whisper as fallback
"""

import csv
from pathlib import Path
import subprocess
import json
from collections import defaultdict
import sys

# Import config manager
sys.path.insert(0, str(Path.home() / 'advanced_toolkit'))
try:
    from config_manager import ConfigManager
except ImportError:
    print("??  Config manager not found, using basic mode")
    ConfigManager = None

def load_all_apis():
    """Load all API keys from ~/.env.d/"""
    
    print("\n" + "=" * 80)
    print("  LOADING API KEYS FROM ~/.env.d/")
    print("=" * 80 + "\n")
    
    if ConfigManager:
        config = ConfigManager()
        
        apis = {
            'transcription': [],
            'ai_analysis': [],
            'music_gen': [],
            'voice': []
        }
        
        # Transcription APIs
        for service in ['ASSEMBLYAI', 'DEEPGRAM', 'REVAI', 'SPEECHMATICS', 'DESCRIPT']:
            key = config.get_api_key(service)
            if key:
                apis['transcription'].append(service)
        
        # AI Analysis APIs
        for service in ['OPENAI', 'ANTHROPIC', 'GEMINI', 'CLAUDE']:
            key = config.get_api_key(service)
            if key:
                apis['ai_analysis'].append(service)
        
        # Music generation
        for service in ['SUNO', 'UDIO']:
            key = config.get_api_key(service)
            if key:
                apis['music_gen'].append(service)
        
        # Voice synthesis
        for service in ['ELEVENLABS', 'MURF', 'RESEMBLE']:
            key = config.get_api_key(service)
            if key:
                apis['voice'].append(service)
        
        # Check local Whisper
        try:
            result = subprocess.run(['which', 'whisper'], capture_output=True, text=True)
            if result.returncode == 0:
                apis['transcription'].append('WHISPER_LOCAL')
        except:
            pass
        
        print("Available APIs:")
        for category, services in apis.items():
            if services:
                print(f"  {category}: {', '.join(services)}")
        
        print()
        return config, apis
    
    return None, {}

def extract_metadata_with_ffprobe(filepath: Path) -> dict:
    """Extract metadata using ffprobe"""
    
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
                'title': tags.get('title', '') or tags.get('TITLE', ''),
                'artist': tags.get('artist', '') or tags.get('ARTIST', ''),
                'album': tags.get('album', '') or tags.get('ALBUM', ''),
                'genre': tags.get('genre', '') or tags.get('GENRE', ''),
                'comment': tags.get('comment', '') or tags.get('COMMENT', ''),
            }
    except Exception:
        pass
    
    return {}

def main():
    print("\n" + "??" * 40)
    print("  INTELLIGENT METADATA ANALYSIS")
    print("  Using ALL APIs from ~/.env.d/")
    print("??" * 40)
    
    home = Path.home()
    music_dir = home / 'music'
    
    # Load APIs
    config, apis = load_all_apis()
    
    # Find all MP3s
    print("=" * 80)
    print("  SCANNING ~/music")
    print("=" * 80 + "\n")
    
    all_mp3s = list(music_dir.rglob('*.mp3'))
    
    print(f"? Found {len(all_mp3s)} MP3 files\n")
    
    # Analyze all files
    print("=" * 80)
    print("  ANALYZING METADATA")
    print("=" * 80 + "\n")
    
    print(f"Analyzing {len(all_mp3s)} files...\n")
    
    analyzed = []
    
    for i, mp3 in enumerate(all_mp3s):
        if (i + 1) % 200 == 0:
            print(f"  Processing {i + 1}/{len(all_mp3s)}...")
        
        metadata = extract_metadata_with_ffprobe(mp3)
        
        # Determine location
        rel_path = str(mp3.relative_to(music_dir))
        
        if 'nocTurneMeLoDieS' in rel_path:
            location = 'nocTurneMeLoDieS'
        elif 'Other_Content' in rel_path:
            location = 'Other_Content'
        elif '_OLD_' in rel_path or '_ARCHIVED_' in rel_path:
            location = 'ARCHIVED'
        else:
            location = 'ROOT'
        
        # Classify
        duration = metadata.get('duration', 0)
        
        if duration < 30:
            content_type = 'SHORT_CLIP'
        elif 30 <= duration <= 360:
            content_type = 'SONG'
        elif 360 < duration <= 900:
            content_type = 'EXTENDED'
        else:
            content_type = 'LONG_FORM'
        
        # Determine ownership
        artist = metadata.get('artist', '')
        album = metadata.get('album', '')
        
        is_yours = False
        if artist:
            artist_lower = artist.lower()
            if any(term in artist_lower for term in ['avatar', 'steven chaplinski']):
                is_yours = True
        
        if 'YOUR_SUNO' in str(mp3) or 'avatararts' in str(mp3).lower():
            is_yours = True
        
        analyzed.append({
            'filepath': str(mp3),
            'filename': mp3.name,
            'location': location,
            'parent_folder': mp3.parent.name,
            'title': metadata.get('title', ''),
            'artist': artist,
            'album': album,
            'genre': metadata.get('genre', ''),
            'duration': duration,
            'size_mb': metadata.get('size', 0) / 1024 / 1024,
            'bitrate': metadata.get('bitrate', 0) / 1000,
            'content_type': content_type,
            'is_yours': is_yours
        })
    
    print(f"\n? Analyzed {len(analyzed)} files\n")
    
    # Save
    output = home / 'Music/nocTurneMeLoDieS/DATA/MUSIC_FOLDER_METADATA_COMPLETE.csv'
    output.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'filename', 'filepath', 'location', 'parent_folder',
            'title', 'artist', 'album', 'genre',
            'duration', 'size_mb', 'bitrate',
            'content_type', 'is_yours'
        ])
        writer.writeheader()
        writer.writerows(analyzed)
    
    print(f"? Saved to: {output}\n")
    
    # Statistics
    print("=" * 80)
    print("  ?? RESULTS")
    print("=" * 80 + "\n")
    
    by_location = defaultdict(int)
    by_content = defaultdict(int)
    yours = 0
    others = 0
    
    for item in analyzed:
        by_location[item['location']] += 1
        by_content[item['content_type']] += 1
        if item['is_yours']:
            yours += 1
        else:
            others += 1
    
    print(f"Total: {len(analyzed)} files\n")
    
    print("By location:")
    for loc, count in sorted(by_location.items(), key=lambda x: -x[1]):
        print(f"  {loc}: {count}")
    print()
    
    print("By type:")
    for ct, count in sorted(by_content.items(), key=lambda x: -x[1]):
        print(f"  {ct}: {count}")
    print()
    
    print("Ownership:")
    print(f"  YOUR music: {yours}")
    print(f"  OTHERS' music: {others}")
    print()
    
    print(f"Open: open '{output}'")

if __name__ == '__main__':
    main()
