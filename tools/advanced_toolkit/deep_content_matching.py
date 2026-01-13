#!/usr/bin/env python3
"""
Deep Content Matching
Match complete songs with their lyrics, prompts, images, and related content
"""

import csv
from pathlib import Path
from difflib import SequenceMatcher
import re

def normalize_for_matching(text: str) -> str:
    """Normalize text for fuzzy matching"""
    if not text:
        return ""
    # Remove file extensions
    text = re.sub(r'\.(mp3|wav|txt|jpg|png|json|md|html)$', '', text, flags=re.IGNORECASE)
    # Remove common words
    text = re.sub(r'\b(the|a|an|by|suno|avatararts?|avatar|arts?)\b', '', text, flags=re.IGNORECASE)
    # Remove special chars, normalize spaces
    text = re.sub(r'[_\-\(\)\[\]\{\}]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.lower().strip()

def similarity_score(s1: str, s2: str) -> float:
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, normalize_for_matching(s1), normalize_for_matching(s2)).ratio()

def find_content_in_directory(search_dir: Path, patterns: list, max_depth: int = 4) -> list:
    """Find files matching patterns"""
    files = []
    
    def search_recursive(path: Path, depth: int = 0):
        if depth > max_depth:
            return
        
        try:
            for item in path.iterdir():
                # Skip system/hidden
                if item.name.startswith('.'):
                    continue
                
                if item.is_file():
                    # Check patterns
                    name_lower = item.name.lower()
                    for pattern in patterns:
                        if pattern in name_lower or item.suffix.lower() == pattern:
                            files.append(item)
                            break
                elif item.is_dir():
                    # Skip certain directories
                    if item.name not in ['Library', 'Applications', 'node_modules', '__pycache__']:
                        search_recursive(item, depth + 1)
        except (PermissionError, OSError):
            pass
    
    search_recursive(search_dir)
    return files

def read_text_file(filepath: Path, max_chars: int = 500) -> str:
    """Read text file content (preview)"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(max_chars)
            if len(content) == max_chars:
                content += '...'
            return content
    except Exception:
        return ""

def main():
    print("\n" + "??" * 40)
    print("  DEEP CONTENT MATCHING")
    print("  Matching songs with lyrics, prompts, images")
    print("??" * 40 + "\n")
    
    home = Path.home()
    
    # Load complete songs
    complete_songs_csv = home / 'Music/TASK3_COMPLETE_SONGS.csv'
    
    if not complete_songs_csv.exists():
        print("? TASK3_COMPLETE_SONGS.csv not found")
        print("Run process_all_three_tasks.py first")
        return
    
    print("Loading complete songs...\n")
    
    songs = []
    with open(complete_songs_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        songs = list(reader)
    
    print(f"? Loaded {len(songs)} complete songs\n")
    
    # Search locations
    search_dirs = {
        'Music': home / 'Music',
        'Documents': home / 'Documents',
        'Downloads': home / 'Downloads',
    }
    
    # Find all content types
    print("Searching for related content...\n")
    
    content_files = {
        'lyrics': [],
        'prompts': [],
        'images': [],
        'docs': []
    }
    
    for dir_name, dir_path in search_dirs.items():
        if not dir_path.exists():
            continue
        
        print(f"  Scanning {dir_name}...")
        
        # Lyrics
        lyrics = find_content_in_directory(
            dir_path,
            ['.txt', '.lrc', '.srt', '.vtt', 'lyric', 'lyrics'],
            max_depth=3
        )
        content_files['lyrics'].extend(lyrics)
        
        # Prompts (JSON, specific keywords)
        prompts = find_content_in_directory(
            dir_path,
            ['prompt', 'dalle', 'sora', 'chatgpt', 'gpt', '.json'],
            max_depth=3
        )
        content_files['prompts'].extend(prompts)
        
        # Images
        images = find_content_in_directory(
            dir_path,
            ['.jpg', '.jpeg', '.png', '.webp'],
            max_depth=3
        )
        content_files['images'].extend(images)
        
        # Docs
        docs = find_content_in_directory(
            dir_path,
            ['.md', '.html', '.pdf'],
            max_depth=3
        )
        content_files['docs'].extend(docs)
    
    print()
    print(f"? Found {len(content_files['lyrics'])} lyrics files")
    print(f"? Found {len(content_files['prompts'])} prompt files")
    print(f"? Found {len(content_files['images'])} image files")
    print(f"? Found {len(content_files['docs'])} document files")
    print()
    
    # Match each song with content
    print("Matching songs with content...\n")
    
    matched_songs = []
    
    for i, song in enumerate(songs):
        if (i + 1) % 10 == 0:
            print(f"  Processing {i + 1}/{len(songs)}...")
        
        title = song.get('Title', '')
        
        matches = {
            'song': song,
            'lyrics_files': [],
            'prompt_files': [],
            'image_files': [],
            'doc_files': [],
        }
        
        # Match lyrics
        for lf in content_files['lyrics']:
            score = similarity_score(title, lf.stem)
            if score > 0.6:  # 60% match threshold
                content_preview = read_text_file(lf, 200)
                matches['lyrics_files'].append({
                    'path': str(lf),
                    'name': lf.name,
                    'score': score,
                    'preview': content_preview
                })
        
        # Match prompts
        for pf in content_files['prompts']:
            score = similarity_score(title, pf.stem)
            if score > 0.6:
                content_preview = read_text_file(pf, 200)
                matches['prompt_files'].append({
                    'path': str(pf),
                    'name': pf.name,
                    'score': score,
                    'preview': content_preview
                })
        
        # Match images
        for img in content_files['images']:
            score = similarity_score(title, img.stem)
            if score > 0.6:
                matches['image_files'].append({
                    'path': str(img),
                    'name': img.name,
                    'score': score
                })
        
        # Match docs
        for doc in content_files['docs']:
            score = similarity_score(title, doc.stem)
            if score > 0.6:
                matches['doc_files'].append({
                    'path': str(doc),
                    'name': doc.name,
                    'score': score
                })
        
        matched_songs.append(matches)
    
    print(f"\n? Matched content for {len(matched_songs)} songs\n")
    
    # Save detailed report
    print("Saving content matching report...\n")
    
    output = home / 'Music/DEEP_CONTENT_MATCHES.csv'
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Title', 'Artist', 'Genre', 'Style',
            'Has_Lyrics_In_CSV', 'Audio_Filepath',
            'Matched_Lyrics_Files', 'Lyrics_Count',
            'Matched_Prompt_Files', 'Prompt_Count',
            'Matched_Images', 'Image_Count',
            'Matched_Docs', 'Doc_Count',
            'Total_Matches', 'Completeness'
        ])
        
        for match in matched_songs:
            song = match['song']
            
            lyrics_count = len(match['lyrics_files'])
            prompt_count = len(match['prompt_files'])
            image_count = len(match['image_files'])
            doc_count = len(match['doc_files'])
            total = lyrics_count + prompt_count + image_count + doc_count
            
            # Determine completeness
            has_csv_lyrics = song.get('Has_Lyrics') == 'YES'
            
            if has_csv_lyrics and lyrics_count > 0 and prompt_count > 0 and image_count > 0:
                completeness = 'COMPLETE'
            elif (has_csv_lyrics or lyrics_count > 0) and prompt_count > 0:
                completeness = 'VERY_GOOD'
            elif has_csv_lyrics or lyrics_count > 0 or prompt_count > 0:
                completeness = 'GOOD'
            else:
                completeness = 'BASIC'
            
            # Format file lists
            lyrics_str = ' | '.join([f"{m['name']} ({m['score']:.2f})" for m in match['lyrics_files']])
            prompt_str = ' | '.join([f"{m['name']} ({m['score']:.2f})" for m in match['prompt_files']])
            image_str = ' | '.join([f"{m['name']} ({m['score']:.2f})" for m in match['image_files']])
            doc_str = ' | '.join([f"{m['name']} ({m['score']:.2f})" for m in match['doc_files']])
            
            writer.writerow([
                song.get('Title', ''),
                song.get('Artist', ''),
                song.get('Genre', ''),
                song.get('Style', ''),
                song.get('Has_Lyrics', ''),
                song.get('Filepath', ''),
                lyrics_str,
                lyrics_count,
                prompt_str,
                prompt_count,
                image_str,
                image_count,
                doc_str,
                doc_count,
                total,
                completeness
            ])
    
    print(f"? Saved to: {output}\n")
    
    # Create detailed bundles report
    print("Creating content bundles report...\n")
    
    bundles_output = home / 'Music/SONG_CONTENT_BUNDLES.txt'
    
    with open(bundles_output, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("  COMPLETE SONG CONTENT BUNDLES\n")
        f.write("  Everything we have for each song\n")
        f.write("=" * 80 + "\n\n")
        
        for match in matched_songs:
            song = match['song']
            title = song.get('Title', 'Unknown')
            
            # Skip songs with no matches
            if not any([match['lyrics_files'], match['prompt_files'], 
                       match['image_files'], match['doc_files']]):
                continue
            
            f.write(f"\n{'=' * 80}\n")
            f.write(f"?? {title}\n")
            f.write(f"{'=' * 80}\n\n")
            
            f.write(f"Artist: {song.get('Artist', 'Unknown')}\n")
            f.write(f"Genre: {song.get('Genre', 'Unknown')}\n")
            f.write(f"Style: {song.get('Style', 'Unknown')}\n")
            f.write(f"Duration: {song.get('Duration', 'Unknown')}\n")
            f.write(f"\nAudio File: {song.get('Filepath', 'N/A')}\n")
            
            if song.get('Cover_URL'):
                f.write(f"Cover Art: {song.get('Cover_URL')}\n")
            
            # Lyrics
            if match['lyrics_files']:
                f.write(f"\n?? LYRICS FILES ({len(match['lyrics_files'])}):\n")
                for lf in match['lyrics_files']:
                    f.write(f"  ? {lf['name']} (match: {lf['score']:.0%})\n")
                    f.write(f"    Path: {lf['path']}\n")
                    if lf['preview']:
                        f.write(f"    Preview: {lf['preview'][:150]}...\n")
            
            # Prompts
            if match['prompt_files']:
                f.write(f"\n?? PROMPT FILES ({len(match['prompt_files'])}):\n")
                for pf in match['prompt_files']:
                    f.write(f"  ? {pf['name']} (match: {pf['score']:.0%})\n")
                    f.write(f"    Path: {pf['path']}\n")
                    if pf['preview']:
                        f.write(f"    Preview: {pf['preview'][:150]}...\n")
            
            # Images
            if match['image_files']:
                f.write(f"\n???  IMAGE FILES ({len(match['image_files'])}):\n")
                for img in match['image_files']:
                    f.write(f"  ? {img['name']} (match: {img['score']:.0%})\n")
                    f.write(f"    Path: {img['path']}\n")
            
            # Docs
            if match['doc_files']:
                f.write(f"\n?? DOCUMENT FILES ({len(match['doc_files'])}):\n")
                for doc in match['doc_files']:
                    f.write(f"  ? {doc['name']} (match: {doc['score']:.0%})\n")
                    f.write(f"    Path: {doc['path']}\n")
            
            f.write("\n")
    
    print(f"? Saved to: {bundles_output}\n")
    
    # Statistics
    print("=" * 80)
    print("  ?? CONTENT MATCHING STATISTICS")
    print("=" * 80 + "\n")
    
    songs_with_lyrics = sum(1 for m in matched_songs if m['lyrics_files'])
    songs_with_prompts = sum(1 for m in matched_songs if m['prompt_files'])
    songs_with_images = sum(1 for m in matched_songs if m['image_files'])
    songs_with_docs = sum(1 for m in matched_songs if m['doc_files'])
    songs_with_any = sum(1 for m in matched_songs if any([
        m['lyrics_files'], m['prompt_files'], m['image_files'], m['doc_files']
    ]))
    
    total_lyrics = sum(len(m['lyrics_files']) for m in matched_songs)
    total_prompts = sum(len(m['prompt_files']) for m in matched_songs)
    total_images = sum(len(m['image_files']) for m in matched_songs)
    total_docs = sum(len(m['doc_files']) for m in matched_songs)
    
    print(f"Songs analyzed: {len(songs)}")
    print(f"\nSongs with matched content:")
    print(f"  ?? With lyrics files: {songs_with_lyrics}")
    print(f"  ?? With prompt files: {songs_with_prompts}")
    print(f"  ???  With image files: {songs_with_images}")
    print(f"  ?? With document files: {songs_with_docs}")
    print(f"  ? With any related content: {songs_with_any}")
    print(f"\nTotal matched items:")
    print(f"  ?? Lyrics files: {total_lyrics}")
    print(f"  ?? Prompt files: {total_prompts}")
    print(f"  ???  Image files: {total_images}")
    print(f"  ?? Document files: {total_docs}")
    print(f"  ?? TOTAL: {total_lyrics + total_prompts + total_images + total_docs}")
    print()
    
    # Show examples
    print("=" * 80)
    print("  ?? BEST CONTENT BUNDLES")
    print("=" * 80 + "\n")
    
    # Sort by total matches
    best_bundles = sorted(matched_songs, 
                         key=lambda x: len(x['lyrics_files']) + len(x['prompt_files']) + 
                                     len(x['image_files']) + len(x['doc_files']),
                         reverse=True)
    
    for i, match in enumerate(best_bundles[:10]):
        song = match['song']
        total = (len(match['lyrics_files']) + len(match['prompt_files']) + 
                len(match['image_files']) + len(match['doc_files']))
        
        if total == 0:
            break
        
        print(f"{i+1}. {song.get('Title', 'Unknown')}")
        print(f"   {len(match['lyrics_files'])} lyrics, {len(match['prompt_files'])} prompts, " +
              f"{len(match['image_files'])} images, {len(match['doc_files'])} docs")
    
    print()
    print("=" * 80)
    print("  ? DEEP CONTENT MATCHING COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"?? CSV Report: {output}")
    print(f"?? Detailed Bundles: {bundles_output}")
    print()
    print("Open reports:")
    print(f"  open '{output}'")
    print(f"  open '{bundles_output}'")

if __name__ == '__main__':
    main()
