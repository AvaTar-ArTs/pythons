#!/usr/bin/env python3
"""
Comprehensive MP3 Reanalysis
Using ALL gathered intelligence to deeply analyze every MP3
"""

import csv
from pathlib import Path
import subprocess
import json
import hashlib
from difflib import SequenceMatcher
from collections import defaultdict
import re

def normalize_title(title: str) -> str:
    """Normalize title for matching"""
    if not title:
        return ""
    return title.lower().replace('_', ' ').replace('-', ' ').strip()

def similarity_score(s1: str, s2: str) -> float:
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, normalize_title(s1), normalize_title(s2)).ratio()

def get_file_hash(filepath: Path) -> str:
    """Get MD5 hash of file"""
    try:
        md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                md5.update(chunk)
        return md5.hexdigest()
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
                'genre': tags.get('genre', '') or tags.get('GENRE', ''),
                'date': tags.get('date', '') or tags.get('DATE', ''),
                'comment': tags.get('comment', '') or tags.get('COMMENT', ''),
            }
    except Exception:
        pass
    
    return {}

def classify_by_duration(duration: float) -> str:
    """Classify content type by duration"""
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

def is_your_music(artist: str, title: str, filename: str, filepath: str) -> bool:
    """Determine if this is the user's original music"""
    
    # Check file path - if in YOUR_SUNO_SONGS, it's yours!
    if 'YOUR_SUNO_SONGS' in filepath:
        return True
    
    # Check if in SONG_BUNDLES
    if 'SONG_BUNDLES' in filepath:
        return True
    
    # Check artist
    if artist:
        artist_lower = artist.lower()
        if any(term in artist_lower for term in ['avatar', 'avatararts', 'ava tar', 'steven chaplinski']):
            return True
        if artist.strip() in ['1', '2', '3', 'Ai', 'Ai-Art', 'AI', 'Music', 'Meeso']:
            return True
    
    # Check filename patterns
    filename_lower = filename.lower()
    if any(term in filename_lower for term in ['avatar', 'suno', 'remastered', 'blues', 'heartbeats', 'alley', 'junkyard', 'petals', 'kings', 'queens', 'bite', 'bookOmemory', 'feather fang']):
        return True
    
    # Check for video indicators (likely not music)
    video_terms = ['eso', 'gameplay', 'political', 'tutorial', 'episode', 'chapter']
    if any(term in filename_lower for term in video_terms):
        return False
    
    return False

def load_all_knowledge_bases(home: Path) -> dict:
    """Load all gathered intelligence"""
    
    print("\n" + "=" * 80)
    print("  LOADING ALL KNOWLEDGE BASES")
    print("=" * 80 + "\n")
    
    knowledge = {
        'google_sheet_1': {},
        'google_sheet_2': {},
        'suno_catalogs': {},
        'master_csv': {},
        'bundles': {},
        'downloads_matched': set()
    }
    
    # Google Sheet 1
    gs1 = home / 'Music/GOOGLE_SHEET_SUNO_DATA.csv'
    if gs1.exists():
        with open(gs1, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get('SongTitle', '') or row.get('Title', '')
                if title:
                    knowledge['google_sheet_1'][normalize_title(title)] = row
        print(f"? Google Sheet 1: {len(knowledge['google_sheet_1'])} songs")
    
    # Google Sheet 2 (with lyrics)
    gs2 = home / 'Music/GOOGLE_SHEET_2_SUNO_DATA.csv'
    if gs2.exists():
        with open(gs2, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get('songName', '') or row.get('SongTitle', '')
                if title:
                    knowledge['google_sheet_2'][normalize_title(title)] = row
        print(f"? Google Sheet 2: {len(knowledge['google_sheet_2'])} songs (with lyrics)")
    
    # SUNO master catalog
    suno_master = home / 'Music/nocTurneMeLoDieS/SUNO/suno-sept/songs_master_combined.csv'
    if suno_master.exists():
        with open(suno_master, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get('SongTitle', '')
                if title:
                    knowledge['suno_catalogs'][normalize_title(title)] = row
        print(f"? SUNO catalog: {len(knowledge['suno_catalogs'])} songs")
    
    # Master CSV
    master = home / 'Music/MASTER_COMPLETE_ALL_FIELDS.csv'
    if master.exists():
        with open(master, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get('Title', '')
                if title:
                    knowledge['master_csv'][normalize_title(title)] = row
        print(f"? Master CSV: {len(knowledge['master_csv'])} entries")
    
    # Song bundles
    bundles_dir = home / 'Music/nocTurneMeLoDieS/SONG_BUNDLES'
    if bundles_dir.exists():
        for bundle in bundles_dir.iterdir():
            if bundle.is_dir():
                # Extract song title from folder name
                folder_name = bundle.name
                # Remove artist prefix
                if ' - ' in folder_name:
                    title = folder_name.split(' - ', 1)[1]
                else:
                    title = folder_name
                knowledge['bundles'][normalize_title(title)] = str(bundle)
        print(f"? Song bundles: {len(knowledge['bundles'])} bundles")
    
    # Downloads matched
    downloads_matched = home / 'Music/DOWNLOADS_MATCHED_CONTENT.csv'
    if downloads_matched.exists():
        with open(downloads_matched, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get('Song_Title', '')
                if title:
                    knowledge['downloads_matched'].add(normalize_title(title))
        print(f"? Downloads matches: {len(knowledge['downloads_matched'])} songs")
    
    print()
    return knowledge

def find_all_mp3s(search_paths: list) -> list:
    """Find all MP3 files in search paths"""
    
    print("=" * 80)
    print("  FINDING ALL MP3 FILES")
    print("=" * 80 + "\n")
    
    all_mp3s = []
    
    for search_path in search_paths:
        if not search_path.exists():
            continue
        
        print(f"Scanning: {search_path}")
        mp3s = list(search_path.rglob('*.mp3'))
        all_mp3s.extend(mp3s)
        print(f"  ? Found {len(mp3s)} MP3s")
    
    print(f"\n? Total MP3s found: {len(all_mp3s)}\n")
    
    return all_mp3s

def comprehensive_analysis(mp3_file: Path, knowledge: dict) -> dict:
    """Perform comprehensive analysis using all knowledge"""
    
    # Extract metadata
    metadata = extract_full_metadata(mp3_file)
    
    # Get title for matching
    title = metadata.get('title', '') or mp3_file.stem
    artist = metadata.get('artist', '')
    title_norm = normalize_title(title)
    
    # Calculate hash
    file_hash = get_file_hash(mp3_file)
    
    # Classify
    duration = metadata.get('duration', 0)
    content_type = classify_by_duration(duration)
    
    # Check ownership
    is_yours = is_your_music(artist, title, mp3_file.name, str(mp3_file))
    
    # Match against knowledge bases
    matches = {
        'google_sheet_1': None,
        'google_sheet_2': None,
        'suno_catalog': None,
        'master_csv': None,
        'bundle': None,
        'downloads': False
    }
    
    best_scores = {}
    
    # Match Google Sheet 1
    for gs_title, gs_data in knowledge['google_sheet_1'].items():
        score = similarity_score(title, gs_data.get('SongTitle', ''))
        if score > 0.7:
            if 'google_sheet_1' not in best_scores or score > best_scores['google_sheet_1']:
                matches['google_sheet_1'] = gs_data
                best_scores['google_sheet_1'] = score
    
    # Match Google Sheet 2 (lyrics)
    for gs_title, gs_data in knowledge['google_sheet_2'].items():
        score = similarity_score(title, gs_data.get('songName', ''))
        if score > 0.7:
            if 'google_sheet_2' not in best_scores or score > best_scores['google_sheet_2']:
                matches['google_sheet_2'] = gs_data
                best_scores['google_sheet_2'] = score
    
    # Match SUNO catalog
    for suno_title, suno_data in knowledge['suno_catalogs'].items():
        score = similarity_score(title, suno_data.get('SongTitle', ''))
        if score > 0.7:
            if 'suno_catalog' not in best_scores or score > best_scores['suno_catalog']:
                matches['suno_catalog'] = suno_data
                best_scores['suno_catalog'] = score
    
    # Match master CSV
    matches['master_csv'] = knowledge['master_csv'].get(title_norm)
    
    # Match bundle
    matches['bundle'] = knowledge['bundles'].get(title_norm)
    
    # Check downloads
    matches['downloads'] = title_norm in knowledge['downloads_matched']
    
    # Determine completeness
    completeness_score = 0
    completeness_details = []
    
    if metadata.get('title'):
        completeness_score += 1
        completeness_details.append('Has title tag')
    if metadata.get('artist'):
        completeness_score += 1
        completeness_details.append('Has artist tag')
    if metadata.get('genre'):
        completeness_score += 1
        completeness_details.append('Has genre tag')
    if matches['google_sheet_2']:
        completeness_score += 2
        completeness_details.append('Has lyrics in Google Sheet')
    if matches['google_sheet_1']:
        completeness_score += 1
        completeness_details.append('In Google Sheet (metadata)')
    if matches['suno_catalog']:
        completeness_score += 1
        completeness_details.append('In SUNO catalog')
    if matches['bundle']:
        completeness_score += 2
        completeness_details.append('Has song bundle')
    if matches['downloads']:
        completeness_score += 1
        completeness_details.append('Has Downloads content')
    
    # Determine overall status
    if completeness_score >= 8:
        status = 'COMPLETE'
        recommendation = 'Fully documented and bundled'
    elif completeness_score >= 5:
        status = 'VERY_GOOD'
        recommendation = 'Has good metadata, could add to bundle'
    elif completeness_score >= 3:
        status = 'GOOD'
        recommendation = 'Has some metadata, needs enrichment'
    elif completeness_score >= 1:
        status = 'BASIC'
        recommendation = 'Minimal metadata, needs analysis'
    else:
        status = 'UNKNOWN'
        recommendation = 'No metadata, needs full analysis'
    
    return {
        'filepath': str(mp3_file),
        'filename': mp3_file.name,
        'title': title,
        'artist': artist,
        'metadata': metadata,
        'file_hash': file_hash,
        'content_type': content_type,
        'is_yours': is_yours,
        'matches': matches,
        'match_scores': best_scores,
        'completeness_score': completeness_score,
        'completeness_details': completeness_details,
        'status': status,
        'recommendation': recommendation
    }

def main():
    print("\n" + "??" * 40)
    print("  COMPREHENSIVE MP3 REANALYSIS")
    print("  Using ALL gathered intelligence")
    print("??" * 40)
    
    home = Path.home()
    
    # Load all knowledge
    knowledge = load_all_knowledge_bases(home)
    
    # Find all MP3s
    search_paths = [
        home / 'Music',
        home / 'Downloads',
        home / 'Documents'
    ]
    
    all_mp3s = find_all_mp3s(search_paths)
    
    # Analyze each MP3
    print("=" * 80)
    print("  ANALYZING ALL MP3S")
    print("=" * 80 + "\n")
    
    print(f"Analyzing {len(all_mp3s)} MP3 files with complete intelligence...\n")
    
    analyses = []
    
    for i, mp3_file in enumerate(all_mp3s):
        if (i + 1) % 100 == 0:
            print(f"  Processing {i + 1}/{len(all_mp3s)}...")
        
        analysis = comprehensive_analysis(mp3_file, knowledge)
        analyses.append(analysis)
    
    print(f"\n? Analyzed {len(analyses)} MP3s\n")
    
    # Save comprehensive report
    print("=" * 80)
    print("  SAVING COMPREHENSIVE REPORT")
    print("=" * 80 + "\n")
    
    output = home / 'Music/COMPREHENSIVE_MP3_REANALYSIS.csv'
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Filename', 'Title', 'Artist', 'Filepath',
            'Duration', 'Size_MB', 'Bitrate_kbps', 'File_Hash',
            'Content_Type', 'Is_Your_Music',
            'In_Google_Sheet_1', 'In_Google_Sheet_2', 'In_SUNO_Catalog',
            'In_Master_CSV', 'Has_Bundle', 'Has_Downloads_Content',
            'Has_Lyrics', 'Has_Metadata_Tags',
            'Completeness_Score', 'Status', 'Recommendation',
            'Google_Sheet_1_Match_Score', 'Google_Sheet_2_Match_Score',
            'Genre', 'Album', 'Comment'
        ])
        
        for analysis in analyses:
            metadata = analysis['metadata']
            matches = analysis['matches']
            scores = analysis['match_scores']
            
            writer.writerow([
                analysis['filename'],
                analysis['title'],
                analysis['artist'],
                analysis['filepath'],
                f"{metadata.get('duration', 0):.1f}",
                f"{metadata.get('size', 0) / 1024 / 1024:.2f}",
                f"{metadata.get('bitrate', 0) / 1000:.0f}",
                analysis['file_hash'][:8],
                analysis['content_type'],
                'YES' if analysis['is_yours'] else 'NO',
                'YES' if matches['google_sheet_1'] else 'NO',
                'YES' if matches['google_sheet_2'] else 'NO',
                'YES' if matches['suno_catalog'] else 'NO',
                'YES' if matches['master_csv'] else 'NO',
                'YES' if matches['bundle'] else 'NO',
                'YES' if matches['downloads'] else 'NO',
                'YES' if matches['google_sheet_2'] else 'NO',
                'YES' if any([metadata.get('title'), metadata.get('artist'), metadata.get('genre')]) else 'NO',
                analysis['completeness_score'],
                analysis['status'],
                analysis['recommendation'],
                f"{scores.get('google_sheet_1', 0):.2f}",
                f"{scores.get('google_sheet_2', 0):.2f}",
                metadata.get('genre', ''),
                metadata.get('album', ''),
                metadata.get('comment', '')
            ])
    
    print(f"? Saved to: {output}\n")
    
    # Statistics
    print("=" * 80)
    print("  ?? COMPREHENSIVE ANALYSIS STATISTICS")
    print("=" * 80 + "\n")
    
    by_status = defaultdict(int)
    by_content_type = defaultdict(int)
    your_music = 0
    others_music = 0
    
    in_google_1 = 0
    in_google_2 = 0
    in_suno = 0
    in_master = 0
    has_bundle = 0
    has_lyrics = 0
    
    for analysis in analyses:
        by_status[analysis['status']] += 1
        by_content_type[analysis['content_type']] += 1
        
        if analysis['is_yours']:
            your_music += 1
        else:
            others_music += 1
        
        if analysis['matches']['google_sheet_1']:
            in_google_1 += 1
        if analysis['matches']['google_sheet_2']:
            in_google_2 += 1
            has_lyrics += 1
        if analysis['matches']['suno_catalog']:
            in_suno += 1
        if analysis['matches']['master_csv']:
            in_master += 1
        if analysis['matches']['bundle']:
            has_bundle += 1
    
    print(f"Total MP3s analyzed: {len(analyses)}\n")
    
    print("Ownership:")
    print(f"  ?? Your music: {your_music}")
    print(f"  ?? Others' music: {others_music}\n")
    
    print("Content Types:")
    for ct, count in sorted(by_content_type.items(), key=lambda x: -x[1]):
        print(f"  {ct}: {count}")
    print()
    
    print("Completeness Status:")
    print(f"  ? COMPLETE: {by_status['COMPLETE']}")
    print(f"  ?? VERY_GOOD: {by_status['VERY_GOOD']}")
    print(f"  ?? GOOD: {by_status['GOOD']}")
    print(f"  ?? BASIC: {by_status['BASIC']}")
    print(f"  ? UNKNOWN: {by_status['UNKNOWN']}\n")
    
    print("Knowledge Base Matches:")
    print(f"  ?? In Google Sheet 1: {in_google_1}")
    print(f"  ?? In Google Sheet 2 (with lyrics): {in_google_2}")
    print(f"  ?? In SUNO catalog: {in_suno}")
    print(f"  ?? In Master CSV: {in_master}")
    print(f"  ?? Has song bundle: {has_bundle}")
    print(f"  ?? Has lyrics: {has_lyrics}\n")
    
    print("=" * 80)
    print("  ? COMPREHENSIVE REANALYSIS COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"?? Full report: {output}\n")
    
    print("Sort/filter by:")
    print("  ? Status - COMPLETE, VERY_GOOD, GOOD, BASIC, UNKNOWN")
    print("  ? Is_Your_Music - YES/NO")
    print("  ? Content_Type - SONG, SHORT_CLIP, EXTENDED, etc.")
    print("  ? Completeness_Score - Higher = more complete (0-10)")
    print("  ? Has_Lyrics - YES/NO")
    print("  ? Has_Bundle - YES/NO")
    print()
    
    print(f"Open: open '{output}'")

if __name__ == '__main__':
    main()
