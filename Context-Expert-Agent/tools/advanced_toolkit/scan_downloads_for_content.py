#!/usr/bin/env python3
"""
Scan Downloads for Music Content
Find all audio files, CSVs, lyrics, prompts in ~/Downloads
Match with existing songs and add to bundles
"""

import csv
from pathlib import Path
from difflib import SequenceMatcher
import subprocess
import json
from collections import defaultdict

def normalize_for_matching(text: str) -> str:
    """Normalize text for fuzzy matching"""
    if not text:
        return ""
    import re
    text = re.sub(r'\.(mp3|wav|txt|jpg|png|json|md|html|csv)$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(the|a|an|by|suno|avatararts?|avatar|arts?)\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'[_\-\(\)\[\]\{\}]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.lower().strip()

def similarity_score(s1: str, s2: str) -> float:
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, normalize_for_matching(s1), normalize_for_matching(s2)).ratio()

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
            format_info = data.get('format', {})
            tags = format_info.get('tags', {})
            return {
                'duration': float(format_info.get('duration', 0)),
                'title': tags.get('title', '') or tags.get('TITLE', ''),
                'artist': tags.get('artist', '') or tags.get('ARTIST', ''),
            }
    except Exception:
        pass
    return {}

def scan_downloads(downloads_path: Path) -> dict:
    """Scan Downloads directory for all content types"""
    
    print("\n" + "=" * 80)
    print("  SCANNING DOWNLOADS DIRECTORY")
    print("=" * 80 + "\n")
    
    print(f"Scanning: {downloads_path}\n")
    
    content = {
        'audio': [],
        'csv': [],
        'lyrics': [],
        'prompts': [],
        'images': [],
        'docs': [],
        'other': []
    }
    
    # Scan all files
    for item in downloads_path.rglob('*'):
        if not item.is_file():
            continue
        
        ext = item.suffix.lower()
        
        if ext in ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac']:
            content['audio'].append(item)
        elif ext == '.csv':
            content['csv'].append(item)
        elif ext in ['.txt', '.lrc', '.srt', '.vtt'] or 'lyric' in item.name.lower():
            content['lyrics'].append(item)
        elif 'prompt' in item.name.lower() or 'dalle' in item.name.lower() or 'sora' in item.name.lower():
            content['prompts'].append(item)
        elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            content['images'].append(item)
        elif ext in ['.md', '.html', '.pdf', '.json']:
            content['docs'].append(item)
        else:
            content['other'].append(item)
    
    print(f"? Audio files: {len(content['audio'])}")
    print(f"? CSV files: {len(content['csv'])}")
    print(f"? Lyrics files: {len(content['lyrics'])}")
    print(f"? Prompt files: {len(content['prompts'])}")
    print(f"? Image files: {len(content['images'])}")
    print(f"? Document files: {len(content['docs'])}")
    print(f"? Other files: {len(content['other'])}")
    print()
    
    return content

def load_existing_songs(master_csv: Path) -> dict:
    """Load existing songs from master CSV"""
    
    songs = {}
    
    if master_csv.exists():
        with open(master_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get('Title', '')
                if title:
                    songs[normalize_for_matching(title)] = row
    
    return songs

def match_downloads_to_songs(downloads_content: dict, existing_songs: dict) -> dict:
    """Match downloads content to existing songs"""
    
    print("=" * 80)
    print("  MATCHING DOWNLOADS TO EXISTING SONGS")
    print("=" * 80 + "\n")
    
    matches = defaultdict(lambda: {
        'audio': [],
        'lyrics': [],
        'prompts': [],
        'images': [],
        'docs': [],
        'csv': []
    })
    
    unmatched = defaultdict(list)
    
    # Match audio files
    print("Matching audio files...")
    for audio_file in downloads_content['audio']:
        metadata = get_audio_metadata(audio_file)
        title = metadata.get('title', '') or audio_file.stem
        
        best_match = None
        best_score = 0
        
        for song_key, song_data in existing_songs.items():
            score = similarity_score(title, song_data.get('Title', ''))
            if score > best_score:
                best_score = score
                best_match = song_data.get('Title', '')
        
        if best_score > 0.6:
            matches[best_match]['audio'].append({
                'path': audio_file,
                'score': best_score,
                'metadata': metadata
            })
        else:
            unmatched['audio'].append({
                'path': audio_file,
                'title': title,
                'metadata': metadata
            })
    
    print(f"  ? Matched {sum(len(m['audio']) for m in matches.values())} audio files")
    print(f"  ??  Unmatched: {len(unmatched['audio'])} audio files")
    print()
    
    # Match lyrics
    print("Matching lyrics files...")
    for lyrics_file in downloads_content['lyrics']:
        title = lyrics_file.stem
        
        best_match = None
        best_score = 0
        
        for song_key, song_data in existing_songs.items():
            score = similarity_score(title, song_data.get('Title', ''))
            if score > best_score:
                best_score = score
                best_match = song_data.get('Title', '')
        
        if best_score > 0.6:
            matches[best_match]['lyrics'].append({
                'path': lyrics_file,
                'score': best_score
            })
        else:
            unmatched['lyrics'].append({
                'path': lyrics_file,
                'title': title
            })
    
    print(f"  ? Matched {sum(len(m['lyrics']) for m in matches.values())} lyrics files")
    print(f"  ??  Unmatched: {len(unmatched['lyrics'])} lyrics files")
    print()
    
    # Match prompts
    print("Matching prompt files...")
    for prompt_file in downloads_content['prompts']:
        title = prompt_file.stem
        
        best_match = None
        best_score = 0
        
        for song_key, song_data in existing_songs.items():
            score = similarity_score(title, song_data.get('Title', ''))
            if score > best_score:
                best_score = score
                best_match = song_data.get('Title', '')
        
        if best_score > 0.6:
            matches[best_match]['prompts'].append({
                'path': prompt_file,
                'score': best_score
            })
        else:
            unmatched['prompts'].append({
                'path': prompt_file,
                'title': title
            })
    
    print(f"  ? Matched {sum(len(m['prompts']) for m in matches.values())} prompt files")
    print(f"  ??  Unmatched: {len(unmatched['prompts'])} prompt files")
    print()
    
    # Match images
    print("Matching image files...")
    for image_file in downloads_content['images']:
        title = image_file.stem
        
        best_match = None
        best_score = 0
        
        for song_key, song_data in existing_songs.items():
            score = similarity_score(title, song_data.get('Title', ''))
            if score > best_score:
                best_score = score
                best_match = song_data.get('Title', '')
        
        if best_score > 0.6:
            matches[best_match]['images'].append({
                'path': image_file,
                'score': best_score
            })
        else:
            unmatched['images'].append({
                'path': image_file,
                'title': title
            })
    
    print(f"  ? Matched {sum(len(m['images']) for m in matches.values())} image files")
    print(f"  ??  Unmatched: {len(unmatched['images'])} image files")
    print()
    
    return dict(matches), dict(unmatched)

def save_reports(matches: dict, unmatched: dict, output_dir: Path):
    """Save matching and unmatched reports"""
    
    print("=" * 80)
    print("  SAVING REPORTS")
    print("=" * 80 + "\n")
    
    # Matched content report
    matched_report = output_dir / 'DOWNLOADS_MATCHED_CONTENT.csv'
    
    with open(matched_report, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Song_Title', 'Content_Type', 'Filename', 
            'Filepath', 'Match_Score', 'Recommendation'
        ])
        
        for song_title, content in sorted(matches.items()):
            for audio in content['audio']:
                writer.writerow([
                    song_title, 'AUDIO', audio['path'].name,
                    str(audio['path']), f"{audio['score']:.2f}",
                    'Add to song bundle'
                ])
            
            for lyrics in content['lyrics']:
                writer.writerow([
                    song_title, 'LYRICS', lyrics['path'].name,
                    str(lyrics['path']), f"{lyrics['score']:.2f}",
                    'Add to song bundle'
                ])
            
            for prompt in content['prompts']:
                writer.writerow([
                    song_title, 'PROMPT', prompt['path'].name,
                    str(prompt['path']), f"{prompt['score']:.2f}",
                    'Add to song bundle'
                ])
            
            for image in content['images']:
                writer.writerow([
                    song_title, 'IMAGE', image['path'].name,
                    str(image['path']), f"{image['score']:.2f}",
                    'Add to song bundle'
                ])
    
    print(f"? Matched content: {matched_report}")
    
    # Unmatched content report
    unmatched_report = output_dir / 'DOWNLOADS_UNMATCHED_CONTENT.csv'
    
    with open(unmatched_report, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Content_Type', 'Filename', 'Title_Extracted',
            'Filepath', 'Recommendation'
        ])
        
        for audio in unmatched.get('audio', []):
            writer.writerow([
                'AUDIO', audio['path'].name, audio['title'],
                str(audio['path']), 'Review - may be new song or duplicate'
            ])
        
        for lyrics in unmatched.get('lyrics', []):
            writer.writerow([
                'LYRICS', lyrics['path'].name, lyrics['title'],
                str(lyrics['path']), 'Review - may need manual matching'
            ])
        
        for prompt in unmatched.get('prompts', []):
            writer.writerow([
                'PROMPT', prompt['path'].name, prompt['title'],
                str(prompt['path']), 'Review - may need manual matching'
            ])
        
        for image in unmatched.get('images', []):
            writer.writerow([
                'IMAGE', image['path'].name, image['title'],
                str(image['path']), 'Review - may need manual matching'
            ])
    
    print(f"? Unmatched content: {unmatched_report}")
    print()

def main():
    print("\n" + "??" * 40)
    print("  SCAN DOWNLOADS FOR MUSIC CONTENT")
    print("  Find audio, lyrics, prompts, images in Downloads")
    print("??" * 40)
    
    home = Path.home()
    downloads_path = home / 'Downloads'
    master_csv = home / 'Music/ULTIMATE_MASTER_REPORT.csv'
    output_dir = home / 'Music'
    
    # Scan Downloads
    downloads_content = scan_downloads(downloads_path)
    
    # Load existing songs
    print("Loading existing songs database...")
    existing_songs = load_existing_songs(master_csv)
    print(f"? Loaded {len(existing_songs)} existing songs\n")
    
    # Match content
    matches, unmatched = match_downloads_to_songs(downloads_content, existing_songs)
    
    # Save reports
    save_reports(matches, unmatched, output_dir)
    
    # Statistics
    print("=" * 80)
    print("  ?? DOWNLOADS SCAN SUMMARY")
    print("=" * 80 + "\n")
    
    total_matched = sum(
        len(content['audio']) + len(content['lyrics']) + 
        len(content['prompts']) + len(content['images'])
        for content in matches.values()
    )
    
    total_unmatched = sum(
        len(files) for files in unmatched.values()
    )
    
    print(f"Songs with matched content: {len(matches)}")
    print(f"Total matched items: {total_matched}")
    print(f"Total unmatched items: {total_unmatched}")
    print()
    
    # Show top matches
    if matches:
        print("Top 10 songs with Downloads content:")
        sorted_matches = sorted(
            matches.items(),
            key=lambda x: len(x[1]['audio']) + len(x[1]['lyrics']) + 
                         len(x[1]['prompts']) + len(x[1]['images']),
            reverse=True
        )
        
        for i, (song_title, content) in enumerate(sorted_matches[:10], 1):
            total = (len(content['audio']) + len(content['lyrics']) + 
                    len(content['prompts']) + len(content['images']))
            print(f"  {i}. {song_title} - {total} items")
    
    print()
    print("=" * 80)
    print("  ? DOWNLOADS SCAN COMPLETE")
    print("=" * 80 + "\n")
    
    print("Reports created:")
    print(f"  ?? Matched: {output_dir}/DOWNLOADS_MATCHED_CONTENT.csv")
    print(f"  ?? Unmatched: {output_dir}/DOWNLOADS_UNMATCHED_CONTENT.csv")
    print()
    
    print("Next steps:")
    print("  1. Review matched content and add to song bundles")
    print("  2. Review unmatched content for new songs or manual matching")
    print()
    
    print("Open reports:")
    print(f"  open '{output_dir}/DOWNLOADS_MATCHED_CONTENT.csv'")
    print(f"  open '{output_dir}/DOWNLOADS_UNMATCHED_CONTENT.csv'")

if __name__ == '__main__':
    main()
