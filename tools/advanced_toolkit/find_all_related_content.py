#!/usr/bin/env python3
"""
Find ALL related content for songs in master CSV
Searches entire ~/ for prompts, lyrics, images, videos, etc.
"""

import csv
from pathlib import Path
from difflib import SequenceMatcher
import re
from collections import defaultdict

def normalize_for_matching(text: str) -> str:
    """Normalize text for fuzzy matching"""
    if not text:
        return ""
    # Remove common prefixes/suffixes
    text = re.sub(r'(\.mp3|\.wav|\.txt|\.jpg|\.png|\.mp4|\.json|\.md|\.html)$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^(the|a|an)\s+', '', text, flags=re.IGNORECASE)
    # Remove special chars, normalize spaces
    text = re.sub(r'[_\-\(\)\[\]\{\}]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.lower().strip()

def similarity_score(s1: str, s2: str) -> float:
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, normalize_for_matching(s1), normalize_for_matching(s2)).ratio()

def find_content_files(base_dir: Path, patterns: list, max_depth: int = 5) -> list:
    """Find files matching patterns"""
    files = []
    
    def search_dir(path: Path, depth: int = 0):
        if depth > max_depth:
            return
        
        try:
            for item in path.iterdir():
                # Skip system/hidden dirs
                if item.name.startswith('.') or item.name in ['Library', 'Applications', 'System']:
                    continue
                
                if item.is_file():
                    # Check if matches any pattern
                    for pattern in patterns:
                        if pattern in item.name.lower() or item.suffix.lower() in pattern:
                            files.append(item)
                            break
                elif item.is_dir():
                    search_dir(item, depth + 1)
        except (PermissionError, OSError):
            pass
    
    search_dir(base_dir)
    return files

def main():
    print("\n" + "??" * 40)
    print("  FINDING ALL RELATED CONTENT")
    print("  Searching entire home directory")
    print("??" * 40 + "\n")
    
    home = Path.home()
    
    # Load master CSV
    print("Loading master CSV...")
    master_csv = home / 'Music/MASTER_COMPLETE_ALL_FIELDS.csv'
    
    songs = []
    with open(master_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        songs = list(reader)
    
    print(f"? Loaded {len(songs)} songs\n")
    
    # Define search locations (focused search for speed)
    search_dirs = [
        home / 'Music',
        home / 'Documents',
        home / 'Downloads',
        home / 'Desktop',
        home / 'Movies',
    ]
    
    # Find all content types
    print("Searching for related content...\n")
    
    print("  ?? Finding lyrics files...")
    lyrics_files = []
    for search_dir in search_dirs:
        if search_dir.exists():
            lyrics_files.extend(find_content_files(
                search_dir,
                ['.txt', '.lrc', '.srt', '.vtt', 'lyric', 'lyrics'],
                max_depth=4
            ))
    print(f"  ? Found {len(lyrics_files)} lyrics files")
    
    print("  ?? Finding prompt files...")
    prompt_files = []
    for search_dir in search_dirs:
        if search_dir.exists():
            prompt_files.extend(find_content_files(
                search_dir,
                ['prompt', 'dalle', 'sora', 'midjourney', 'chatgpt', '.json', 'gpt'],
                max_depth=4
            ))
    print(f"  ? Found {len(prompt_files)} prompt files")
    
    print("  ???  Finding image files...")
    image_files = []
    for search_dir in [home / 'Music', home / 'Documents', home / 'Downloads']:
        if search_dir.exists():
            image_files.extend(find_content_files(
                search_dir,
                ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
                max_depth=3
            ))
    print(f"  ? Found {len(image_files)} image files")
    
    print("  ?? Finding video files...")
    video_files = []
    for search_dir in [home / 'Music', home / 'Movies', home / 'Downloads']:
        if search_dir.exists():
            video_files.extend(find_content_files(
                search_dir,
                ['.mp4', '.mov', '.avi', '.mkv'],
                max_depth=3
            ))
    print(f"  ? Found {len(video_files)} video files")
    
    print("  ?? Finding document files...")
    doc_files = []
    for search_dir in [home / 'Documents', home / 'Music']:
        if search_dir.exists():
            doc_files.extend(find_content_files(
                search_dir,
                ['.md', '.html', '.pdf', '.doc', '.docx'],
                max_depth=3
            ))
    print(f"  ? Found {len(doc_files)} document files\n")
    
    # Match content to songs
    print("Matching content to songs...")
    print("(This may take a moment...)\n")
    
    matched_results = []
    
    for i, song in enumerate(songs):
        if (i + 1) % 50 == 0:
            print(f"  Processing song {i + 1}/{len(songs)}...")
        
        title = song.get('Title', '')
        if not title:
            continue
        
        result = {
            'title': title,
            'artist': song.get('Artist', ''),
            'status': song.get('Status', ''),
            'local_file': song.get('Local_Filenames', ''),
            'lyrics_in_csv': 'YES' if song.get('Lyrics') else 'NO',
            'lyrics_files': [],
            'prompt_files': [],
            'image_files': [],
            'video_files': [],
            'doc_files': [],
        }
        
        # Match lyrics
        for lf in lyrics_files:
            score = similarity_score(title, lf.stem)
            if score > 0.6:  # 60% match threshold
                result['lyrics_files'].append({
                    'path': str(lf),
                    'score': f"{score:.2f}"
                })
        
        # Match prompts
        for pf in prompt_files:
            score = similarity_score(title, pf.stem)
            if score > 0.6:
                result['prompt_files'].append({
                    'path': str(pf),
                    'score': f"{score:.2f}"
                })
        
        # Match images
        for img in image_files:
            score = similarity_score(title, img.stem)
            if score > 0.6:
                result['image_files'].append({
                    'path': str(img),
                    'score': f"{score:.2f}"
                })
        
        # Match videos
        for vid in video_files:
            score = similarity_score(title, vid.stem)
            if score > 0.6:
                result['video_files'].append({
                    'path': str(vid),
                    'score': f"{score:.2f}"
                })
        
        # Match documents
        for doc in doc_files:
            score = similarity_score(title, doc.stem)
            if score > 0.6:
                result['doc_files'].append({
                    'path': str(doc),
                    'score': f"{score:.2f}"
                })
        
        matched_results.append(result)
    
    print(f"? Matched content for {len(matched_results)} songs\n")
    
    # Save results
    print("Saving comprehensive cross-reference...\n")
    
    output = home / 'Music/COMPREHENSIVE_CONTENT_MAP.csv'
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Title', 'Artist', 'Status', 
            'Local_Audio_File',
            'Has_Lyrics_In_CSV',
            'Related_Lyrics_Files', 'Lyrics_Count',
            'Related_Prompt_Files', 'Prompt_Count',
            'Related_Image_Files', 'Image_Count',
            'Related_Video_Files', 'Video_Count',
            'Related_Doc_Files', 'Doc_Count',
            'Total_Related_Items'
        ])
        
        for result in matched_results:
            lyrics_count = len(result['lyrics_files'])
            prompt_count = len(result['prompt_files'])
            image_count = len(result['image_files'])
            video_count = len(result['video_files'])
            doc_count = len(result['doc_files'])
            total = lyrics_count + prompt_count + image_count + video_count + doc_count
            
            # Format file lists
            lyrics_str = ' | '.join([f"{m['path']} ({m['score']})" for m in result['lyrics_files']]) if result['lyrics_files'] else ''
            prompt_str = ' | '.join([f"{m['path']} ({m['score']})" for m in result['prompt_files']]) if result['prompt_files'] else ''
            image_str = ' | '.join([f"{m['path']} ({m['score']})" for m in result['image_files']]) if result['image_files'] else ''
            video_str = ' | '.join([f"{m['path']} ({m['score']})" for m in result['video_files']]) if result['video_files'] else ''
            doc_str = ' | '.join([f"{m['path']} ({m['score']})" for m in result['doc_files']]) if result['doc_files'] else ''
            
            writer.writerow([
                result['title'],
                result['artist'],
                result['status'],
                result['local_file'],
                result['lyrics_in_csv'],
                lyrics_str,
                lyrics_count,
                prompt_str,
                prompt_count,
                image_str,
                image_count,
                video_str,
                video_count,
                doc_str,
                doc_count,
                total
            ])
    
    print(f"? Saved to: {output}\n")
    
    # Statistics
    print("=" * 80)
    print("  ?? CONTENT MAPPING STATISTICS")
    print("=" * 80 + "\n")
    
    songs_with_lyrics = sum(1 for r in matched_results if r['lyrics_files'])
    songs_with_prompts = sum(1 for r in matched_results if r['prompt_files'])
    songs_with_images = sum(1 for r in matched_results if r['image_files'])
    songs_with_videos = sum(1 for r in matched_results if r['video_files'])
    songs_with_docs = sum(1 for r in matched_results if r['doc_files'])
    songs_with_any = sum(1 for r in matched_results if any([
        r['lyrics_files'], r['prompt_files'], r['image_files'], 
        r['video_files'], r['doc_files']
    ]))
    
    total_lyrics = sum(len(r['lyrics_files']) for r in matched_results)
    total_prompts = sum(len(r['prompt_files']) for r in matched_results)
    total_images = sum(len(r['image_files']) for r in matched_results)
    total_videos = sum(len(r['video_files']) for r in matched_results)
    total_docs = sum(len(r['doc_files']) for r in matched_results)
    
    print(f"Total songs analyzed: {len(matched_results)}")
    print(f"\nSongs with related content:")
    print(f"  ?? With lyrics files: {songs_with_lyrics}")
    print(f"  ?? With prompt files: {songs_with_prompts}")
    print(f"  ???  With image files: {songs_with_images}")
    print(f"  ?? With video files: {songs_with_videos}")
    print(f"  ?? With document files: {songs_with_docs}")
    print(f"  ? With any related content: {songs_with_any}")
    print(f"\nTotal related items found:")
    print(f"  ?? Lyrics files: {total_lyrics}")
    print(f"  ?? Prompt files: {total_prompts}")
    print(f"  ???  Image files: {total_images}")
    print(f"  ?? Video files: {total_videos}")
    print(f"  ?? Document files: {total_docs}")
    print(f"  ?? TOTAL: {total_lyrics + total_prompts + total_images + total_videos + total_docs}")
    print()
    
    print("=" * 80)
    print("  ? CONTENT MAPPING COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"?? Comprehensive map: {output}")
    print(f"\nSort by 'Total_Related_Items' to see songs with most content!")
    print(f"Filter by content type to find songs with prompts, images, etc.")
    print(f"\nOpen: open '{output}'")

if __name__ == '__main__':
    main()
