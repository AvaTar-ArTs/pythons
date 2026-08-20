#!/usr/bin/env python3
"""
Cross-Reference Everything
Compare 430 audio files with:
- Lyrics files
- Transcripts
- Image prompts (album art)
- DALL-E prompts
Match them all together
"""

import csv
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher
import re

def normalize_name(name: str) -> str:
    """Normalize filename for matching"""
    # Remove extension
    name = Path(name).stem
    # Remove common suffixes
    name = re.sub(r'[-_](v\d+|part\d+|\d+)$', '', name, flags=re.IGNORECASE)
    # Normalize separators
    name = name.replace('_', ' ').replace('-', ' ')
    # Remove numbers at end
    name = re.sub(r'\s+\d+$', '', name)
    # Lowercase
    return name.lower().strip()

def similarity_score(str1: str, str2: str) -> float:
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def find_all_related_files():
    """Find all lyrics, transcripts, and prompts"""
    
    print("\n" + "=" * 80)
    print("  FINDING ALL RELATED CONTENT")
    print("=" * 80 + "\n")
    
    home = Path.home()
    
    related = {
        'lyrics': [],
        'transcripts': [],
        'prompts': [],
        'images': []
    }
    
    # Search locations
    search_dirs = [
        home / 'Music/nocTurneMeLoDieS',
        home / 'Documents',
    ]
    
    print("Searching for related content...\n")
    
    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        
        print(f"  Scanning {search_dir.name}...")
        
        # Lyrics and transcripts
        for txt_file in search_dir.rglob('*.txt'):
            name_lower = txt_file.name.lower()
            if 'lyric' in name_lower:
                related['lyrics'].append(txt_file)
            elif 'transcript' in name_lower:
                related['transcripts'].append(txt_file)
        
        for md_file in search_dir.rglob('*.md'):
            name_lower = md_file.name.lower()
            if 'lyric' in name_lower or 'transcript' in name_lower:
                related['transcripts'].append(md_file)
        
        # Prompts
        for prompt_file in search_dir.rglob('*prompt*.txt'):
            related['prompts'].append(prompt_file)
        
        for prompt_file in search_dir.rglob('*prompt*.md'):
            related['prompts'].append(prompt_file)
        
        # Images (album art, etc.)
        for img_ext in ['.png', '.jpg', '.jpeg']:
            for img_file in search_dir.rglob(f'*{img_ext}'):
                if 'cover' in img_file.name.lower() or 'album' in img_file.name.lower():
                    related['images'].append(img_file)
    
    print()
    print("Found:")
    print(f"  Lyrics: {len(related['lyrics'])} files")
    print(f"  Transcripts: {len(related['transcripts'])} files")
    print(f"  Prompts: {len(related['prompts'])} files")
    print(f"  Images: {len(related['images'])} files")
    print()
    
    return related

def cross_reference(audio_files: list, related: dict):
    """Cross-reference audio with related content"""
    
    print("=" * 80)
    print("  CROSS-REFERENCING")
    print("=" * 80 + "\n")
    
    matches = []
    
    print(f"Matching {len(audio_files)} audio files with related content...\n")
    
    for audio_row in audio_files:
        filename = audio_row.get('filename', '')
        title = audio_row.get('title', '')
        
        if not filename:
            continue
        
        # Normalize for matching
        audio_name_norm = normalize_name(filename)
        title_norm = normalize_name(title) if title else audio_name_norm
        
        match_info = {
            'audio_file': filename,
            'title': title,
            'duration': audio_row.get('duration', ''),
            'in_suno_catalog': audio_row.get('in_suno_catalog', 'NO'),
            'lyrics': [],
            'transcripts': [],
            'prompts': [],
            'images': []
        }
        
        # Match with lyrics
        for lyrics_file in related['lyrics']:
            lyrics_norm = normalize_name(lyrics_file.name)
            
            if similarity_score(audio_name_norm, lyrics_norm) > 0.7 or \
               (title_norm and similarity_score(title_norm, lyrics_norm) > 0.7):
                match_info['lyrics'].append(str(lyrics_file))
        
        # Match with transcripts
        for transcript_file in related['transcripts']:
            transcript_norm = normalize_name(transcript_file.name)
            
            if similarity_score(audio_name_norm, transcript_norm) > 0.7 or \
               (title_norm and similarity_score(title_norm, transcript_norm) > 0.7):
                match_info['transcripts'].append(str(transcript_file))
        
        # Match with prompts
        for prompt_file in related['prompts']:
            prompt_norm = normalize_name(prompt_file.name)
            
            if similarity_score(audio_name_norm, prompt_norm) > 0.6 or \
               (title_norm and similarity_score(title_norm, prompt_norm) > 0.6):
                match_info['prompts'].append(str(prompt_file))
        
        # Match with images
        for img_file in related['images']:
            img_norm = normalize_name(img_file.name)
            
            if similarity_score(audio_name_norm, img_norm) > 0.6 or \
               (title_norm and similarity_score(title_norm, img_norm) > 0.6):
                match_info['images'].append(str(img_file))
        
        matches.append(match_info)
    
    return matches

def save_cross_reference(matches: list):
    """Save cross-reference data"""
    
    output = Path.home() / 'Music/CROSS_REFERENCED_COMPLETE.csv'
    
    print("=" * 80)
    print("  SAVING CROSS-REFERENCE")
    print("=" * 80 + "\n")
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Audio File', 'Title', 'Duration', 'In Suno Catalog',
            'Has Lyrics', 'Has Transcript', 'Has Prompts', 'Has Images',
            'Lyrics Files', 'Transcript Files', 'Prompt Files', 'Image Files'
        ])
        
        for match in matches:
            writer.writerow([
                match['audio_file'],
                match['title'],
                match['duration'],
                match['in_suno_catalog'],
                'YES' if match['lyrics'] else 'NO',
                'YES' if match['transcripts'] else 'NO',
                'YES' if match['prompts'] else 'NO',
                'YES' if match['images'] else 'NO',
                '; '.join(match['lyrics']) if match['lyrics'] else '',
                '; '.join(match['transcripts']) if match['transcripts'] else '',
                '; '.join(match['prompts']) if match['prompts'] else '',
                '; '.join(match['images']) if match['images'] else '',
            ])
    
    print(f"? Saved to: {output}\n")
    
    # Show statistics
    with_lyrics = sum(1 for m in matches if m['lyrics'])
    with_transcripts = sum(1 for m in matches if m['transcripts'])
    with_prompts = sum(1 for m in matches if m['prompts'])
    with_images = sum(1 for m in matches if m['images'])
    
    print("Matching Statistics:")
    print(f"  Audio files with lyrics: {with_lyrics}")
    print(f"  Audio files with transcripts: {with_transcripts}")
    print(f"  Audio files with prompts: {with_prompts}")
    print(f"  Audio files with images: {with_images}")
    
    # Show samples
    if with_lyrics > 0:
        print("\nSample matches with lyrics:")
        count = 0
        for match in matches:
            if match['lyrics'] and count < 5:
                print(f"  ? {match['audio_file']}")
                for lyrics_file in match['lyrics'][:1]:
                    print(f"    ? {Path(lyrics_file).name}")
                count += 1
    
    return output

def main():
    print("\n" + "??" * 40)
    print("  CROSS-REFERENCE ALL CONTENT")
    print("  Audio + Lyrics + Transcripts + Prompts + Images")
    print("??" * 40)
    
    # Load the final CSV
    csv_path = Path.home() / 'Downloads/YOUR_SUNO_SONGS_COMPLETE - MASTER_MERGED_DATA (1).csv'
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        audio_files = [row for row in reader if row.get('filename')]
    
    print(f"\n? Loaded {len(audio_files)} audio files from CSV")
    
    # Find all related content
    related = find_all_related_files()
    
    # Cross-reference everything
    matches = cross_reference(audio_files, related)
    
    # Save results
    output = save_cross_reference(matches)
    
    print("\n" + "=" * 80)
    print("  ? CROSS-REFERENCE COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"Master cross-reference: {output}")
    print(f"\nThis shows which audio files have:")
    print(f"  ? Lyrics/transcripts")
    print(f"  ? Image prompts")
    print(f"  ? Album art")
    print(f"\nAll matched together!")

if __name__ == '__main__':
    main()
