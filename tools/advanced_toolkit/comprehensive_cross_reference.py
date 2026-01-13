#!/usr/bin/env python3
"""
Comprehensive Cross-Reference
Find ALL related content for each audio file:
- Lyrics, transcripts
- DALL-E prompts, Sora prompts, all prompts
- Videos (mp4, mov)
- PDFs
- HTMLs
- Markdown files
- Images
Everything!
"""

import csv
from pathlib import Path
from difflib import SequenceMatcher
import re

def normalize_for_matching(name: str) -> str:
    """Normalize filename for fuzzy matching"""
    name = Path(name).stem.lower()
    # Remove version numbers, dates
    name = re.sub(r'[-_]?v\d+', '', name)
    name = re.sub(r'\d{4}-\d{2}-\d{2}', '', name)
    name = re.sub(r'[-_]\d+$', '', name)
    # Normalize separators
    name = name.replace('_', ' ').replace('-', ' ')
    # Remove extra spaces
    name = re.sub(r'\s+', ' ', name)
    return name.strip()

def similarity_score(str1: str, str2: str) -> float:
    """Calculate similarity"""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def find_all_content():
    """Find ALL types of content across ~/"""
    
    print("\n" + "=" * 80)
    print("  COMPREHENSIVE CONTENT SCAN")
    print("  Finding EVERYTHING related to your audio")
    print("=" * 80 + "\n")
    
    home = Path.home()
    
    content = {
        'lyrics': [],
        'transcripts': [],
        'dalle_prompts': [],
        'sora_prompts': [],
        'other_prompts': [],
        'videos': [],
        'pdfs': [],
        'htmls': [],
        'markdowns': [],
        'images': [],
    }
    
    search_dirs = [
        home / 'Music/nocTurneMeLoDieS',
        home / 'Documents',
        home / 'Movies',
    ]
    
    print("Searching for all content types...\n")
    
    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        
        print(f"  ?? Scanning {search_dir.name}...")
        
        # Text files - lyrics, transcripts
        for txt_file in search_dir.rglob('*.txt'):
            name_lower = txt_file.name.lower()
            if 'lyric' in name_lower:
                content['lyrics'].append(txt_file)
            elif 'transcript' in name_lower:
                content['transcripts'].append(txt_file)
            elif 'prompt' in name_lower:
                if 'sora' in name_lower:
                    content['sora_prompts'].append(txt_file)
                elif 'dalle' in name_lower:
                    content['dalle_prompts'].append(txt_file)
                else:
                    content['other_prompts'].append(txt_file)
        
        # Markdown files
        for md_file in search_dir.rglob('*.md'):
            name_lower = md_file.name.lower()
            path_lower = str(md_file).lower()
            
            if 'lyric' in name_lower or 'transcript' in name_lower:
                content['transcripts'].append(md_file)
            elif 'prompt' in name_lower or 'prompt' in path_lower:
                if 'sora' in name_lower or 'sora' in path_lower:
                    content['sora_prompts'].append(md_file)
                elif 'dalle' in name_lower:
                    content['dalle_prompts'].append(md_file)
                else:
                    content['other_prompts'].append(md_file)
            else:
                content['markdowns'].append(md_file)
        
        # Videos
        for vid_ext in ['.mp4', '.mov', '.avi', '.mkv']:
            for vid_file in search_dir.rglob(f'*{vid_ext}'):
                content['videos'].append(vid_file)
        
        # PDFs
        for pdf_file in search_dir.rglob('*.pdf'):
            content['pdfs'].append(pdf_file)
        
        # HTMLs
        for html_file in search_dir.rglob('*.html'):
            name_lower = html_file.name.lower()
            path_lower = str(html_file).lower()
            
            if 'prompt' in name_lower or 'dalle' in path_lower or 'sora' in path_lower:
                if 'sora' in name_lower or 'sora' in path_lower:
                    content['sora_prompts'].append(html_file)
                else:
                    content['dalle_prompts'].append(html_file)
            else:
                content['htmls'].append(html_file)
        
        # Images (album art, cover art)
        for img_ext in ['.png', '.jpg', '.jpeg', '.webp']:
            for img_file in search_dir.rglob(f'*{img_ext}'):
                if any(keyword in img_file.name.lower() for keyword in ['cover', 'album', 'art', 'artwork']):
                    content['images'].append(img_file)
    
    print()
    print("? Content Found:")
    for content_type, files in content.items():
        print(f"  {content_type:20s} {len(files):5d} files")
    print()
    
    return content

def cross_reference_everything(audio_files: list, content: dict):
    """Match each audio file with ALL related content"""
    
    print("=" * 80)
    print("  CROSS-REFERENCING EVERYTHING")
    print("=" * 80 + "\n")
    
    matches = []
    
    print(f"Matching {len(audio_files)} audio files...\n")
    
    for i, audio_row in enumerate(audio_files, 1):
        if i % 50 == 0:
            print(f"  Processed {i}/{len(audio_files)}...")
        
        filename = audio_row.get('filename', '')
        title = audio_row.get('title', '')
        
        if not filename:
            continue
        
        audio_norm = normalize_for_matching(filename)
        title_norm = normalize_for_matching(title) if title else audio_norm
        
        match_info = {
            'audio_file': filename,
            'title': title,
            'duration': audio_row.get('duration', ''),
            'in_suno_catalog': audio_row.get('in_suno_catalog', 'NO'),
        }
        
        # Match with each content type
        for content_type, files in content.items():
            matches_found = []
            
            for related_file in files:
                related_norm = normalize_for_matching(related_file.name)
                
                # Calculate similarity
                sim_file = similarity_score(audio_norm, related_norm)
                sim_title = similarity_score(title_norm, related_norm) if title else 0
                
                # Match threshold
                if sim_file > 0.6 or sim_title > 0.6:
                    matches_found.append(str(related_file))
            
            match_info[content_type] = matches_found
        
        matches.append(match_info)
    
    print(f"\n? Cross-referenced {len(matches)} files\n")
    
    return matches

def save_comprehensive_reference(matches: list):
    """Save comprehensive cross-reference"""
    
    output = Path.home() / 'Music/COMPREHENSIVE_CROSS_REFERENCE.csv'
    
    print("=" * 80)
    print("  SAVING COMPREHENSIVE CROSS-REFERENCE")
    print("=" * 80 + "\n")
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow([
            'Audio File', 'Title', 'Duration', 'In Suno Catalog',
            'Has Lyrics', 'Has Transcripts', 'Has DALL-E Prompts', 'Has Sora Prompts',
            'Has Other Prompts', 'Has Videos', 'Has PDFs', 'Has HTMLs', 
            'Has Markdowns', 'Has Images',
            'Lyrics Files', 'Transcript Files', 'DALL-E Prompts', 'Sora Prompts',
            'Other Prompts', 'Videos', 'PDFs', 'HTMLs', 'Markdowns', 'Images'
        ])
        
        for match in matches:
            writer.writerow([
                match['audio_file'],
                match['title'],
                match['duration'],
                match['in_suno_catalog'],
                'YES' if match['lyrics'] else '',
                'YES' if match['transcripts'] else '',
                'YES' if match['dalle_prompts'] else '',
                'YES' if match['sora_prompts'] else '',
                'YES' if match['other_prompts'] else '',
                'YES' if match['videos'] else '',
                'YES' if match['pdfs'] else '',
                'YES' if match['htmls'] else '',
                'YES' if match['markdowns'] else '',
                'YES' if match['images'] else '',
                '; '.join(match['lyrics'][:3]) if match['lyrics'] else '',
                '; '.join(match['transcripts'][:3]) if match['transcripts'] else '',
                '; '.join(match['dalle_prompts'][:3]) if match['dalle_prompts'] else '',
                '; '.join(match['sora_prompts'][:3]) if match['sora_prompts'] else '',
                '; '.join(match['other_prompts'][:3]) if match['other_prompts'] else '',
                '; '.join(match['videos'][:3]) if match['videos'] else '',
                '; '.join(match['pdfs'][:3]) if match['pdfs'] else '',
                '; '.join(match['htmls'][:3]) if match['htmls'] else '',
                '; '.join(match['markdowns'][:3]) if match['markdowns'] else '',
                '; '.join(match['images'][:3]) if match['images'] else '',
            ])
    
    print(f"? Saved to: {output}\n")
    
    # Statistics
    stats = {}
    for content_type in ['lyrics', 'transcripts', 'dalle_prompts', 'sora_prompts', 
                        'other_prompts', 'videos', 'pdfs', 'htmls', 'markdowns', 'images']:
        count = sum(1 for m in matches if m.get(content_type))
        if count > 0:
            stats[content_type] = count
    
    print("Matching Statistics:")
    for content_type, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {content_type:20s} {count:3d} audio files have this")
    
    # Show complete matches
    complete_matches = [m for m in matches if 
                       (m.get('transcripts') or m.get('lyrics')) and 
                       (m.get('dalle_prompts') or m.get('sora_prompts') or m.get('images'))]
    
    print(f"\n? Complete matches (audio + text + visuals): {len(complete_matches)}")
    
    if complete_matches:
        print("\nSample complete sets:")
        for match in complete_matches[:5]:
            print(f"\n  ?? {match['audio_file']}")
            if match.get('transcripts'):
                print(f"    ?? Transcript: {len(match['transcripts'])} files")
            if match.get('dalle_prompts'):
                print(f"    ?? DALL-E: {len(match['dalle_prompts'])} prompts")
            if match.get('sora_prompts'):
                print(f"    ?? Sora: {len(match['sora_prompts'])} prompts")
            if match.get('videos'):
                print(f"    ?? Videos: {len(match['videos'])} files")
    
    return output

def main():
    print("\n" + "??" * 40)
    print("  COMPREHENSIVE CROSS-REFERENCE")
    print("  Audio + Lyrics + Transcripts + Prompts (DALL-E, Sora, etc)")
    print("  + Videos + PDFs + HTMLs + Markdown + Images")
    print("??" * 40)
    
    # Load audio files
    csv_path = Path.home() / 'Downloads/YOUR_SUNO_SONGS_COMPLETE - MASTER_MERGED_DATA (1).csv'
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        audio_files = [row for row in reader if row.get('filename')]
    
    print(f"\n? Loaded {len(audio_files)} audio files")
    
    # Find all content
    content = find_all_content()
    
    # Cross-reference
    matches = cross_reference_everything(audio_files, content)
    
    # Save
    output = save_comprehensive_reference(matches)
    
    print("\n" + "=" * 80)
    print("  ? COMPREHENSIVE CROSS-REFERENCE COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"Master file: {output}")
    print(f"\nThis shows ALL related content for each audio file!")
    print(f"\nOpen it: open {output}")

if __name__ == '__main__':
    main()
