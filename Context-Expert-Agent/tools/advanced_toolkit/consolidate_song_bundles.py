#!/usr/bin/env python3
"""
Consolidate Song Bundles
Move all related content (audio, lyrics, prompts, images) into organized folders
Instead of scattered everywhere, each song gets its own complete bundle
"""

import csv
from pathlib import Path
import shutil
import json

def sanitize_folder_name(name: str) -> str:
    """Sanitize folder name"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    name = name.strip('. ')
    if len(name) > 100:
        name = name[:100]
    return name

def copy_file_safely(src: Path, dst: Path) -> bool:
    """Copy file with conflict handling"""
    try:
        # If destination exists, add number
        if dst.exists():
            stem = dst.stem
            suffix = dst.suffix
            counter = 1
            while dst.exists():
                dst = dst.parent / f"{stem}_{counter}{suffix}"
                counter += 1
        
        shutil.copy2(src, dst)
        return True
    except Exception as e:
        print(f"    ? Error copying: {e}")
        return False

def create_bundle_metadata(song: dict, bundle_path: Path, files_copied: dict):
    """Create metadata file for the bundle"""
    
    metadata = {
        'song_info': {
            'title': song.get('Title', ''),
            'artist': song.get('Artist', ''),
            'genre': song.get('Genre', ''),
            'style': song.get('Style', ''),
            'mood': song.get('Mood', ''),
            'duration': song.get('Duration', ''),
            'content_type': song.get('Content_Type', ''),
        },
        'bundle_contents': {
            'audio_files': len(files_copied.get('audio', [])),
            'lyrics_files': len(files_copied.get('lyrics', [])),
            'prompt_files': len(files_copied.get('prompts', [])),
            'image_files': len(files_copied.get('images', [])),
            'document_files': len(files_copied.get('docs', [])),
        },
        'files': files_copied,
        'original_locations': {
            'audio': song.get('Filepath', ''),
            'cover_url': song.get('Cover_URL', ''),
            'song_url': song.get('Song_URL', ''),
        }
    }
    
    metadata_file = bundle_path / '_bundle_info.json'
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    # Also create a readable README
    readme_file = bundle_path / 'README.txt'
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(f"{'=' * 80}\n")
        f.write(f"  {song.get('Title', 'Unknown')}\n")
        f.write(f"{'=' * 80}\n\n")
        f.write(f"Artist: {song.get('Artist', 'Unknown')}\n")
        f.write(f"Genre: {song.get('Genre', 'Unknown')}\n")
        f.write(f"Style: {song.get('Style', 'Unknown')}\n")
        f.write(f"Duration: {song.get('Duration', 'Unknown')}\n\n")
        
        f.write(f"Bundle Contents:\n")
        f.write(f"  Audio files: {len(files_copied.get('audio', []))}\n")
        f.write(f"  Lyrics files: {len(files_copied.get('lyrics', []))}\n")
        f.write(f"  Prompt files: {len(files_copied.get('prompts', []))}\n")
        f.write(f"  Images: {len(files_copied.get('images', []))}\n")
        f.write(f"  Documents: {len(files_copied.get('docs', []))}\n\n")
        
        if song.get('Cover_URL'):
            f.write(f"Cover Art URL: {song.get('Cover_URL')}\n")
        if song.get('Song_URL'):
            f.write(f"Song URL: {song.get('Song_URL')}\n")

def main():
    print("\n" + "??" * 40)
    print("  CONSOLIDATE SONG BUNDLES")
    print("  Organize all related content together")
    print("??" * 40 + "\n")
    
    home = Path.home()
    
    # Load content matches
    matches_csv = home / 'Music/DEEP_CONTENT_MATCHES.csv'
    
    if not matches_csv.exists():
        print("? DEEP_CONTENT_MATCHES.csv not found")
        print("Run deep_content_matching.py first")
        return
    
    # Load bundles details
    bundles_txt = home / 'Music/SONG_CONTENT_BUNDLES.txt'
    
    print("Loading matched content...\n")
    
    songs_data = []
    with open(matches_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only process songs with matched content
            if int(row.get('Total_Matches', 0)) > 0:
                songs_data.append(row)
    
    print(f"? Found {len(songs_data)} songs with related content\n")
    
    # Create bundles directory
    bundles_root = home / 'Music/nocTurneMeLoDieS/SONG_BUNDLES'
    bundles_root.mkdir(parents=True, exist_ok=True)
    
    print(f"Bundles location: {bundles_root}\n")
    print("=" * 80)
    print("  CREATING CONSOLIDATED BUNDLES")
    print("=" * 80 + "\n")
    
    # Process each song
    results = []
    
    for i, song in enumerate(songs_data):
        title = song.get('Title', f'Unknown_{i}')
        artist = song.get('Artist', 'Unknown')
        
        print(f"[{i+1}/{len(songs_data)}] {title}")
        
        # Create bundle folder
        folder_name = sanitize_folder_name(f"{artist} - {title}")
        bundle_path = bundles_root / folder_name
        bundle_path.mkdir(exist_ok=True)
        
        files_copied = {
            'audio': [],
            'lyrics': [],
            'prompts': [],
            'images': [],
            'docs': []
        }
        
        # Copy audio file
        audio_path = song.get('Audio_Filepath', '').strip()
        if audio_path and Path(audio_path).exists():
            src = Path(audio_path)
            dst = bundle_path / f"AUDIO - {src.name}"
            if copy_file_safely(src, dst):
                files_copied['audio'].append(dst.name)
                print(f"  ? Audio: {src.name}")
        
        # Copy lyrics files
        lyrics_files = song.get('Matched_Lyrics_Files', '').split(' | ')
        lyrics_count = 0
        for lf in lyrics_files:
            if not lf.strip():
                continue
            # Extract filename (before the score)
            filename = lf.split(' (')[0].strip()
            # Try to find the file
            for search_dir in [home / 'Music', home / 'Documents', home / 'Downloads']:
                matches = list(search_dir.rglob(filename))
                if matches:
                    src = matches[0]
                    dst = bundle_path / f"LYRICS - {src.name}"
                    if copy_file_safely(src, dst):
                        files_copied['lyrics'].append(dst.name)
                        lyrics_count += 1
                    break
        
        if lyrics_count > 0:
            print(f"  ? Lyrics: {lyrics_count} files")
        
        # Copy prompt files
        prompt_files = song.get('Matched_Prompt_Files', '').split(' | ')
        prompt_count = 0
        for pf in prompt_files:
            if not pf.strip():
                continue
            filename = pf.split(' (')[0].strip()
            for search_dir in [home / 'Music', home / 'Documents', home / 'Downloads']:
                matches = list(search_dir.rglob(filename))
                if matches:
                    src = matches[0]
                    dst = bundle_path / f"PROMPT - {src.name}"
                    if copy_file_safely(src, dst):
                        files_copied['prompts'].append(dst.name)
                        prompt_count += 1
                    break
        
        if prompt_count > 0:
            print(f"  ? Prompts: {prompt_count} files")
        
        # Copy image files
        image_files = song.get('Matched_Images', '').split(' | ')
        image_count = 0
        for img in image_files:
            if not img.strip():
                continue
            filename = img.split(' (')[0].strip()
            for search_dir in [home / 'Music', home / 'Documents', home / 'Downloads']:
                matches = list(search_dir.rglob(filename))
                if matches:
                    src = matches[0]
                    dst = bundle_path / f"IMAGE - {src.name}"
                    if copy_file_safely(src, dst):
                        files_copied['images'].append(dst.name)
                        image_count += 1
                    break
        
        if image_count > 0:
            print(f"  ? Images: {image_count} files")
        
        # Copy document files
        doc_files = song.get('Matched_Docs', '').split(' | ')
        doc_count = 0
        for doc in doc_files:
            if not doc.strip():
                continue
            filename = doc.split(' (')[0].strip()
            for search_dir in [home / 'Music', home / 'Documents']:
                matches = list(search_dir.rglob(filename))
                if matches:
                    src = matches[0]
                    dst = bundle_path / f"DOC - {src.name}"
                    if copy_file_safely(src, dst):
                        files_copied['docs'].append(dst.name)
                        doc_count += 1
                    break
        
        if doc_count > 0:
            print(f"  ? Docs: {doc_count} files")
        
        # Create bundle metadata
        create_bundle_metadata(song, bundle_path, files_copied)
        
        # Track results
        total_files = (len(files_copied['audio']) + len(files_copied['lyrics']) + 
                      len(files_copied['prompts']) + len(files_copied['images']) + 
                      len(files_copied['docs']))
        
        results.append({
            'title': title,
            'folder': folder_name,
            'total_files': total_files,
            'files_copied': files_copied
        })
        
        print(f"  ? Bundle created: {total_files} files total\n")
    
    # Summary
    print("=" * 80)
    print("  ? CONSOLIDATION COMPLETE")
    print("=" * 80 + "\n")
    
    total_bundles = len(results)
    total_audio = sum(len(r['files_copied']['audio']) for r in results)
    total_lyrics = sum(len(r['files_copied']['lyrics']) for r in results)
    total_prompts = sum(len(r['files_copied']['prompts']) for r in results)
    total_images = sum(len(r['files_copied']['images']) for r in results)
    total_docs = sum(len(r['files_copied']['docs']) for r in results)
    total_files = total_audio + total_lyrics + total_prompts + total_images + total_docs
    
    print(f"Created {total_bundles} complete song bundles\n")
    print(f"Total files organized:")
    print(f"  ?? Audio files: {total_audio}")
    print(f"  ?? Lyrics files: {total_lyrics}")
    print(f"  ?? Prompt files: {total_prompts}")
    print(f"  ???  Image files: {total_images}")
    print(f"  ?? Document files: {total_docs}")
    print(f"  ?? TOTAL: {total_files}")
    print()
    
    print(f"All bundles are in: {bundles_root}\n")
    
    # Create index
    index_file = bundles_root / '_BUNDLES_INDEX.txt'
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("  SONG BUNDLES INDEX\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total bundles: {total_bundles}\n")
        f.write(f"Total files: {total_files}\n\n")
        f.write("=" * 80 + "\n\n")
        
        for i, result in enumerate(sorted(results, key=lambda x: x['title']), 1):
            f.write(f"{i}. {result['title']}\n")
            f.write(f"   Folder: {result['folder']}\n")
            f.write(f"   Files: {result['total_files']} (")
            parts = []
            if result['files_copied']['audio']:
                parts.append(f"{len(result['files_copied']['audio'])} audio")
            if result['files_copied']['lyrics']:
                parts.append(f"{len(result['files_copied']['lyrics'])} lyrics")
            if result['files_copied']['prompts']:
                parts.append(f"{len(result['files_copied']['prompts'])} prompts")
            if result['files_copied']['images']:
                parts.append(f"{len(result['files_copied']['images'])} images")
            if result['files_copied']['docs']:
                parts.append(f"{len(result['files_copied']['docs'])} docs")
            f.write(", ".join(parts))
            f.write(")\n\n")
    
    print(f"? Index created: {index_file}\n")
    
    print("Each bundle contains:")
    print("  ? Audio file(s)")
    print("  ? Related lyrics")
    print("  ? Related prompts")
    print("  ? Related images")
    print("  ? Related documents")
    print("  ? _bundle_info.json (metadata)")
    print("  ? README.txt (human-readable info)")
    print()
    
    print("=" * 80)
    print(f"\n?? All content consolidated!\n")
    print(f"Open: open '{bundles_root}'")
    print(f"Index: open '{index_file}'")

if __name__ == '__main__':
    main()
