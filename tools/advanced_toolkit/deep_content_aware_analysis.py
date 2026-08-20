#!/usr/bin/env python3
"""
DEEP CONTENT-AWARE ANALYSIS
Analyze all JSON metadata from SUNO + match with actual audio files
"""

import csv
import json
from pathlib import Path
import subprocess
from collections import defaultdict
from difflib import SequenceMatcher

def normalize_title(title: str) -> str:
    """Normalize title for matching"""
    if not title:
        return ""
    return title.lower().replace('_', ' ').replace('-', ' ').strip()

def load_all_json_metadata(suno_path: Path) -> list:
    """Load all JSON files from SUNO directory"""
    
    print("\n" + "=" * 80)
    print("  LOADING JSON METADATA")
    print("=" * 80 + "\n")
    
    json_files = list(suno_path.rglob('*.json'))
    print(f"Found {len(json_files)} JSON files\n")
    
    metadata = []
    
    for i, json_file in enumerate(json_files):
        if (i + 1) % 50 == 0:
            print(f"  Loading {i + 1}/{len(json_files)}...")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Handle different JSON structures
                if isinstance(data, dict):
                    metadata.append({
                        'source_file': str(json_file.relative_to(suno_path)),
                        'data': data
                    })
                elif isinstance(data, list):
                    for item in data:
                        metadata.append({
                            'source_file': str(json_file.relative_to(suno_path)),
                            'data': item
                        })
        except Exception as e:
            pass
    
    print(f"\n? Loaded {len(metadata)} metadata entries\n")
    
    return metadata

def extract_song_info(metadata_entry: dict) -> dict:
    """Extract song information from JSON metadata"""
    data = metadata_entry['data']
    
    # Try different JSON schema patterns
    return {
        'id': (data.get('id') or data.get('song_id') or 
               data.get('clip_id') or data.get('uuid') or ''),
        'title': (data.get('title') or data.get('name') or 
                 data.get('song_name') or data.get('display_name') or ''),
        'lyrics': (data.get('lyrics') or data.get('lyric') or 
                  data.get('prompt') or data.get('text') or ''),
        'style': (data.get('style') or data.get('genre') or 
                 data.get('tags') or data.get('metadata', {}).get('tags') or ''),
        'created': (data.get('created_at') or data.get('date') or 
                   data.get('timestamp') or ''),
        'duration': (data.get('duration') or data.get('length') or 
                    data.get('metadata', {}).get('duration') or 0),
        'audio_url': (data.get('audio_url') or data.get('url') or 
                     data.get('song_url') or data.get('media_url') or ''),
        'image_url': (data.get('image_url') or data.get('cover_url') or 
                     data.get('image_large_url') or ''),
        'model': (data.get('model_name') or data.get('model') or 
                 data.get('version') or ''),
        'source_file': metadata_entry['source_file'],
        'raw_data': data  # Keep raw data for deep analysis
    }

def find_all_audio_files(music_path: Path) -> list:
    """Find ALL audio files in Music directory"""
    
    print("=" * 80)
    print("  SCANNING FOR AUDIO FILES")
    print("=" * 80 + "\n")
    
    print(f"Scanning: {music_path}\n")
    
    audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac'}
    audio_files = []
    
    for ext in audio_extensions:
        files = list(music_path.rglob(f'*{ext}'))
        if files:
            print(f"  Found {len(files)} {ext} files")
            audio_files.extend(files)
    
    print(f"\n? Total audio files: {len(audio_files)}\n")
    
    return audio_files

def get_audio_metadata(filepath: Path) -> dict:
    """Get metadata from audio file"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-print_format', 'json',
             '-show_format', str(filepath)],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            tags = data.get('format', {}).get('tags', {})
            return {
                'title': tags.get('title', '') or tags.get('TITLE', ''),
                'artist': tags.get('artist', '') or tags.get('ARTIST', ''),
                'duration': float(data.get('format', {}).get('duration', 0)),
            }
    except Exception:
        pass
    
    return {}

def match_audio_with_metadata(audio_files: list, json_metadata: list, 
                               master_csv: dict) -> list:
    """Match audio files with JSON metadata and master CSV"""
    
    print("=" * 80)
    print("  MATCHING AUDIO WITH METADATA")
    print("=" * 80 + "\n")
    
    print("Processing audio files...\n")
    
    # Build metadata lookup
    metadata_by_title = defaultdict(list)
    for meta_entry in json_metadata:
        info = extract_song_info(meta_entry)
        if info['title']:
            metadata_by_title[normalize_title(info['title'])].append(info)
    
    matched = []
    
    for i, audio_file in enumerate(audio_files):
        if (i + 1) % 100 == 0:
            print(f"  Processing {i + 1}/{len(audio_files)}...")
        
        # Get audio metadata
        audio_meta = get_audio_metadata(audio_file)
        
        # Try to match
        title = audio_meta.get('title', '') or audio_file.stem
        title_norm = normalize_title(title)
        
        # Find matches
        json_matches = metadata_by_title.get(title_norm, [])
        master_match = master_csv.get(title_norm)
        
        matched.append({
            'filepath': str(audio_file),
            'filename': audio_file.name,
            'title': title,
            'title_normalized': title_norm,
            'audio_metadata': audio_meta,
            'json_metadata': json_matches,
            'master_metadata': master_match,
            'has_json': len(json_matches) > 0,
            'has_master': master_match is not None,
            'match_count': len(json_matches),
        })
    
    print(f"\n? Processed {len(matched)} audio files\n")
    
    return matched

def save_comprehensive_analysis(matched_data: list, output_path: Path):
    """Save comprehensive content-aware analysis"""
    
    print("=" * 80)
    print("  SAVING COMPREHENSIVE ANALYSIS")
    print("=" * 80 + "\n")
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Filename', 'Title', 'Artist',
            'Duration', 'Filepath',
            'Has_JSON_Metadata', 'JSON_Match_Count',
            'Has_Master_Entry',
            'JSON_Style', 'JSON_Model', 'JSON_Audio_URL',
            'JSON_Lyrics_Preview',
            'Master_Genre', 'Master_Status',
            'Content_Completeness', 'Recommendation'
        ])
        
        for item in matched_data:
            # Get first JSON match if available
            json_info = item['json_metadata'][0] if item['json_metadata'] else {}
            master_info = item['master_metadata'] or {}
            
            # Determine completeness
            if item['has_json'] and item['has_master']:
                completeness = 'COMPLETE'
                recommendation = 'Full metadata available'
            elif item['has_json']:
                completeness = 'HAS_JSON'
                recommendation = 'Add to master CSV'
            elif item['has_master']:
                completeness = 'HAS_MASTER'
                recommendation = 'Has master entry'
            else:
                completeness = 'MINIMAL'
                recommendation = 'Review - may need metadata'
            
            # Get lyrics preview
            lyrics = json_info.get('lyrics', '')
            lyrics_preview = lyrics[:100] + '...' if len(lyrics) > 100 else lyrics
            
            writer.writerow([
                item['filename'],
                item['title'],
                item['audio_metadata'].get('artist', ''),
                f"{item['audio_metadata'].get('duration', 0):.1f}",
                item['filepath'],
                'YES' if item['has_json'] else 'NO',
                item['match_count'],
                'YES' if item['has_master'] else 'NO',
                json_info.get('style', ''),
                json_info.get('model', ''),
                json_info.get('audio_url', ''),
                lyrics_preview,
                master_info.get('Genre', ''),
                master_info.get('Status', ''),
                completeness,
                recommendation
            ])
    
    print(f"? Saved to: {output_path}\n")

def main():
    print("\n" + "??" * 40)
    print("  DEEP CONTENT-AWARE ANALYSIS")
    print("  JSON Metadata + Audio Files + Master CSV")
    print("??" * 40)
    
    home = Path.home()
    suno_path = home / 'Music/nocTurneMeLoDieS/SUNO'
    music_path = home / 'Music/nocTurneMeLoDieS'
    master_path = home / 'Music/MASTER_COMPLETE_ALL_FIELDS.csv'
    
    # Load master CSV
    print("\nLoading master CSV...")
    master_csv = {}
    with open(master_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get('Title', '')
            if title:
                master_csv[normalize_title(title)] = row
    print(f"? Loaded {len(master_csv)} master entries\n")
    
    # Load all JSON metadata from SUNO
    json_metadata = load_all_json_metadata(suno_path)
    
    # Extract song info from JSON
    print("Extracting song information from JSON...")
    songs_from_json = []
    for meta in json_metadata:
        info = extract_song_info(meta)
        if info['title']:
            songs_from_json.append(info)
    print(f"? Extracted {len(songs_from_json)} songs from JSON\n")
    
    # Find all audio files
    audio_files = find_all_audio_files(music_path)
    
    # Sample first 1000 for speed
    if len(audio_files) > 1000:
        print(f"Analyzing first 1000 of {len(audio_files)} audio files for speed...\n")
        audio_files = audio_files[:1000]
    
    # Match everything
    matched = match_audio_with_metadata(audio_files, json_metadata, master_csv)
    
    # Save analysis
    output = home / 'Music/DEEP_CONTENT_AWARE_ANALYSIS.csv'
    save_comprehensive_analysis(matched, output)
    
    # Statistics
    print("=" * 80)
    print("  ?? CONTENT-AWARE STATISTICS")
    print("=" * 80 + "\n")
    
    with_json = sum(1 for m in matched if m['has_json'])
    with_master = sum(1 for m in matched if m['has_master'])
    complete = sum(1 for m in matched if m['has_json'] and m['has_master'])
    
    print(f"Audio files analyzed: {len(matched)}")
    print(f"JSON metadata entries: {len(json_metadata)}")
    print(f"Songs in JSON: {len(songs_from_json)}")
    print(f"Master CSV entries: {len(master_csv)}")
    print()
    print(f"Matches:")
    print(f"  ? Complete (audio + JSON + master): {complete}")
    print(f"  ?? Audio + JSON: {with_json}")
    print(f"  ?? Audio + master: {with_master}")
    print()
    
    print("=" * 80)
    print("  ? DEEP ANALYSIS COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"?? Report: {output}")
    print(f"\nFilter by 'Content_Completeness':")
    print(f"  COMPLETE ? Has audio + JSON + master")
    print(f"  HAS_JSON ? Has JSON metadata, add to master")
    print(f"  HAS_MASTER ? Has master entry")
    print(f"  MINIMAL ? Review metadata")
    print(f"\nOpen: open '{output}'")

if __name__ == '__main__':
    main()
