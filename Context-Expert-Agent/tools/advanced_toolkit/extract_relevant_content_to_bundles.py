#!/usr/bin/env python3
"""
Extract Relevant Content to Bundles
Instead of copying entire files, read and extract only the relevant parts
"""

import csv
from pathlib import Path
from difflib import SequenceMatcher
import re
import json

def normalize_for_matching(text: str) -> str:
    """Normalize text for matching"""
    if not text:
        return ""
    text = re.sub(r'\.(mp3|wav|txt|jpg|png|json|md|html|pdf)$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'[_\-\(\)\[\]\{\}]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.lower().strip()

def similarity_score(s1: str, s2: str) -> float:
    """Calculate similarity"""
    return SequenceMatcher(None, normalize_for_matching(s1), normalize_for_matching(s2)).ratio()

def read_text_file(filepath: Path) -> str:
    """Read text content from file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return ""

def extract_relevant_sections(content: str, song_title: str) -> list:
    """Extract sections of content relevant to the song"""
    if not content:
        return []
    
    relevant_sections = []
    lines = content.split('\n')
    
    # Look for sections mentioning the song
    in_relevant_section = False
    current_section = []
    context_lines = 5  # Lines before/after match
    
    for i, line in enumerate(lines):
        # Check if this line mentions the song
        if similarity_score(song_title, line) > 0.5:
            # Get context before
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)
            
            section = '\n'.join(lines[start:end])
            relevant_sections.append(section)
    
    # If no specific matches, try to find sections with keywords
    if not relevant_sections:
        # Look for common section headers
        keywords = normalize_for_matching(song_title).split()
        for i, line in enumerate(lines):
            line_norm = normalize_for_matching(line)
            if any(keyword in line_norm for keyword in keywords if len(keyword) > 3):
                start = max(0, i - 2)
                end = min(len(lines), i + 10)
                section = '\n'.join(lines[start:end])
                if section not in [s for s in relevant_sections]:
                    relevant_sections.append(section)
    
    return relevant_sections

def extract_from_json(filepath: Path, song_title: str) -> dict:
    """Extract relevant data from JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # If it's a dict, look for song-related fields
        if isinstance(data, dict):
            relevant = {}
            for key, value in data.items():
                key_lower = str(key).lower()
                # Check if key or value relates to the song
                if (similarity_score(song_title, str(key)) > 0.5 or 
                    similarity_score(song_title, str(value)) > 0.5):
                    relevant[key] = value
                # Common metadata fields
                elif key_lower in ['title', 'lyrics', 'prompt', 'description', 'tags', 'genre', 'style']:
                    relevant[key] = value
            return relevant
        
        return {'data': data}
    except Exception:
        return {}

def create_extracted_content_file(bundle_path: Path, song_title: str, 
                                  lyrics_files: list, prompt_files: list, 
                                  doc_files: list) -> int:
    """Create a single extracted content file in the bundle"""
    
    content_parts = []
    files_processed = 0
    
    # Header
    content_parts.append("=" * 80)
    content_parts.append(f"  EXTRACTED CONTENT FOR: {song_title}")
    content_parts.append("=" * 80)
    content_parts.append("")
    
    # Extract from lyrics files
    if lyrics_files:
        content_parts.append("\n" + "=" * 80)
        content_parts.append("  LYRICS")
        content_parts.append("=" * 80 + "\n")
        
        for lf_path in lyrics_files:
            if not Path(lf_path).exists():
                continue
            
            content = read_text_file(Path(lf_path))
            if content:
                content_parts.append(f"Source: {Path(lf_path).name}")
                content_parts.append("-" * 80)
                # If it's a full lyrics file, include it all (they're usually short)
                if len(content) < 5000:
                    content_parts.append(content)
                else:
                    # Extract relevant parts
                    sections = extract_relevant_sections(content, song_title)
                    if sections:
                        content_parts.append('\n\n[...]\n\n'.join(sections))
                    else:
                        content_parts.append(content[:2000] + "\n\n[...truncated...]")
                content_parts.append("")
                files_processed += 1
    
    # Extract from prompt files
    if prompt_files:
        content_parts.append("\n" + "=" * 80)
        content_parts.append("  PROMPTS & GENERATION INFO")
        content_parts.append("=" * 80 + "\n")
        
        for pf_path in prompt_files:
            if not Path(pf_path).exists():
                continue
            
            pf = Path(pf_path)
            content_parts.append(f"Source: {pf.name}")
            content_parts.append("-" * 80)
            
            if pf.suffix == '.json':
                data = extract_from_json(pf, song_title)
                if data:
                    content_parts.append(json.dumps(data, indent=2))
            else:
                content = read_text_file(pf)
                sections = extract_relevant_sections(content, song_title)
                if sections:
                    content_parts.append('\n\n[...]\n\n'.join(sections))
                elif content:
                    content_parts.append(content[:1000] + "\n\n[...truncated...]")
            
            content_parts.append("")
            files_processed += 1
    
    # Extract from document files
    if doc_files:
        content_parts.append("\n" + "=" * 80)
        content_parts.append("  RELATED DOCUMENTS")
        content_parts.append("=" * 80 + "\n")
        
        for df_path in doc_files:
            if not Path(df_path).exists():
                continue
            
            df = Path(df_path)
            
            # Skip PDFs (would need special handling)
            if df.suffix == '.pdf':
                content_parts.append(f"Source: {df.name} [PDF - not extracted]")
                content_parts.append("-" * 80)
                content_parts.append(f"Full file at: {df_path}")
                content_parts.append("")
                continue
            
            content_parts.append(f"Source: {df.name}")
            content_parts.append("-" * 80)
            
            if df.suffix == '.json':
                data = extract_from_json(df, song_title)
                if data:
                    content_parts.append(json.dumps(data, indent=2))
            else:
                content = read_text_file(df)
                sections = extract_relevant_sections(content, song_title)
                if sections:
                    content_parts.append('\n\n[...]\n\n'.join(sections))
                elif content:
                    # Show first part
                    content_parts.append(content[:1500] + "\n\n[...truncated...]")
            
            content_parts.append("")
            files_processed += 1
    
    # Save extracted content
    if files_processed > 0:
        output_file = bundle_path / 'EXTRACTED_CONTENT.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content_parts))
        return files_processed
    
    return 0

def main():
    print("\n" + "??" * 40)
    print("  EXTRACT RELEVANT CONTENT TO BUNDLES")
    print("  Smart extraction instead of full file copies")
    print("??" * 40 + "\n")
    
    home = Path.home()
    bundles_root = home / 'Music/nocTurneMeLoDieS/SONG_BUNDLES'
    matches_csv = home / 'Music/DEEP_CONTENT_MATCHES.csv'
    
    if not matches_csv.exists():
        print("? DEEP_CONTENT_MATCHES.csv not found")
        return
    
    if not bundles_root.exists():
        print("? SONG_BUNDLES directory not found")
        return
    
    # Load matched content
    print("Loading content matches...\n")
    
    songs_data = []
    with open(matches_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row.get('Total_Matches', 0)) > 0:
                songs_data.append(row)
    
    print(f"? Found {len(songs_data)} songs with related content\n")
    
    print("=" * 80)
    print("  EXTRACTING RELEVANT CONTENT")
    print("=" * 80 + "\n")
    
    results = {
        'processed': 0,
        'files_extracted': 0,
        'bundles_updated': 0
    }
    
    for i, song in enumerate(songs_data):
        title = song.get('Title', f'Unknown_{i}')
        artist = song.get('Artist', 'AvaTar ArTs')
        
        print(f"[{i+1}/{len(songs_data)}] {title}")
        
        # Find bundle
        bundle_name = f"{artist} - {title}"
        # Try to find existing bundle (fuzzy match)
        bundle_path = None
        for bundle_dir in bundles_root.iterdir():
            if bundle_dir.is_dir() and similarity_score(title, bundle_dir.name) > 0.7:
                bundle_path = bundle_dir
                break
        
        if not bundle_path:
            print(f"  ??  Bundle not found, skipping\n")
            continue
        
        # Parse file lists
        lyrics_files = []
        prompt_files = []
        doc_files = []
        
        # Get lyrics files
        lyrics_str = song.get('Matched_Lyrics_Files', '')
        if lyrics_str:
            for item in lyrics_str.split(' | '):
                if item.strip():
                    filename = item.split(' (')[0].strip()
                    # Try to find the file
                    for search_dir in [home / 'Music', home / 'Documents', home / 'Downloads']:
                        matches = list(search_dir.rglob(filename))
                        if matches:
                            lyrics_files.append(str(matches[0]))
                            break
        
        # Get prompt files
        prompt_str = song.get('Matched_Prompt_Files', '')
        if prompt_str:
            for item in prompt_str.split(' | '):
                if item.strip():
                    filename = item.split(' (')[0].strip()
                    for search_dir in [home / 'Music', home / 'Documents', home / 'Downloads']:
                        matches = list(search_dir.rglob(filename))
                        if matches:
                            prompt_files.append(str(matches[0]))
                            break
        
        # Get doc files
        doc_str = song.get('Matched_Docs', '')
        if doc_str:
            for item in doc_str.split(' | '):
                if item.strip():
                    filename = item.split(' (')[0].strip()
                    for search_dir in [home / 'Music', home / 'Documents']:
                        matches = list(search_dir.rglob(filename))
                        if matches:
                            doc_files.append(str(matches[0]))
                            break
        
        # Extract relevant content
        files_extracted = create_extracted_content_file(
            bundle_path, title, lyrics_files, prompt_files, doc_files
        )
        
        if files_extracted > 0:
            print(f"  ? Extracted from {files_extracted} files")
            results['bundles_updated'] += 1
            results['files_extracted'] += files_extracted
        else:
            print(f"  - No content to extract")
        
        results['processed'] += 1
        print()
    
    # Summary
    print("=" * 80)
    print("  ? CONTENT EXTRACTION COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"Bundles processed: {results['processed']}")
    print(f"Bundles updated: {results['bundles_updated']}")
    print(f"Source files extracted from: {results['files_extracted']}")
    print()
    
    print("Benefits:")
    print("  ? Only relevant content extracted (not entire files)")
    print("  ? Clean, readable format in EXTRACTED_CONTENT.txt")
    print("  ? Smaller bundle sizes")
    print("  ? No duplicate large files")
    print("  ? All related content in one readable file per song")
    print()
    
    print(f"All bundles: open '{bundles_root}'")
    print()
    print("Each bundle now has:")
    print("  ? AUDIO - [song].mp3")
    print("  ? EXTRACTED_CONTENT.txt  ? Smart extraction!")
    print("  ? _bundle_info.json")
    print("  ? README.txt")

if __name__ == '__main__':
    main()
