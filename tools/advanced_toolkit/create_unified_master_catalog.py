#!/usr/bin/env python3
"""
Create Unified Master Catalog
Merge existing COMPLETE_METADATA_CATALOG with comprehensive reanalysis
"""

import csv
from pathlib import Path
from collections import defaultdict

def normalize_path(path: str) -> str:
    """Normalize path for matching"""
    return str(Path(path).resolve())

def main():
    print("\n" + "??" * 40)
    print("  CREATING UNIFIED MASTER CATALOG")
    print("  Merging existing catalog + new analysis")
    print("??" * 40 + "\n")
    
    home = Path.home()
    
    # Load existing catalog
    existing_catalog = home / 'Music/COMPLETE_METADATA_CATALOG.csv'
    new_analysis = home / 'Music/COMPREHENSIVE_MP3_REANALYSIS.csv'
    deep_scan_audio = home / 'Music/DEEP_SCAN_AUDIO.csv'
    
    print("Loading data sources...\n")
    
    # Load existing catalog (525 songs with transcription data)
    existing_data = {}
    if existing_catalog.exists():
        with open(existing_catalog, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                filepath = row.get('filepath', '')
                if filepath:
                    existing_data[normalize_path(filepath)] = row
        print(f"? Existing catalog: {len(existing_data)} songs")
    
    # Load new comprehensive analysis (1,256 files)
    new_data = {}
    if new_analysis.exists():
        with open(new_analysis, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                filepath = row.get('Filepath', '')
                if filepath:
                    new_data[normalize_path(filepath)] = row
        print(f"? Comprehensive reanalysis: {len(new_data)} files")
    
    # Load deep scan (6,068 audio files)
    deep_scan_data = {}
    if deep_scan_audio.exists():
        with open(deep_scan_audio, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                filepath = row.get('Path', '')
                if filepath:
                    deep_scan_data[normalize_path(filepath)] = row
        print(f"? Deep scan: {len(deep_scan_data)} audio files")
    
    print()
    
    # Merge all data
    print("Merging all data sources...\n")
    
    # Get all unique paths
    all_paths = set()
    all_paths.update(existing_data.keys())
    all_paths.update(new_data.keys())
    all_paths.update(deep_scan_data.keys())
    
    print(f"Total unique audio files: {len(all_paths)}\n")
    
    # Build unified catalog
    unified = []
    
    for filepath in sorted(all_paths):
        existing = existing_data.get(filepath, {})
        new = new_data.get(filepath, {})
        deep = deep_scan_data.get(filepath, {})
        
        # Determine best values (prefer existing catalog for established data)
        entry = {
            # Core identification
            'filepath': filepath,
            'filename': existing.get('filename') or new.get('Filename') or Path(filepath).name,
            
            # Metadata (prefer existing catalog)
            'title': existing.get('title') or new.get('Title') or Path(filepath).stem,
            'artist': existing.get('artist') or new.get('Artist') or '',
            'album': existing.get('album') or new.get('Album') or '',
            'genre': existing.get('genre') or new.get('Genre') or '',
            
            # File info
            'duration_seconds': existing.get('duration_seconds') or new.get('Duration') or '',
            'duration_formatted': existing.get('duration_formatted') or '',
            'file_size_mb': existing.get('file_size_mb') or new.get('Size_MB') or deep.get('Size_MB') or '',
            'bitrate_kbps': existing.get('bitrate') or new.get('Bitrate_kbps') or '',
            'file_hash': existing.get('file_hash') or new.get('File_Hash') or deep.get('Hash') or '',
            
            # Classification
            'content_type': existing.get('content_type') or new.get('Content_Type') or '',
            'is_your_music': new.get('Is_Your_Music') or ('YES' if 'Steven Chaplinski' in existing.get('artist', '') else 'NO'),
            
            # Organization
            'album_folder': existing.get('album_folder') or '',
            'has_bundle': new.get('Has_Bundle') or 'NO',
            'bundle_path': '',  # Will populate if has bundle
            
            # Knowledge base matches
            'in_google_sheet_1': new.get('In_Google_Sheet_1') or 'NO',
            'in_google_sheet_2': new.get('In_Google_Sheet_2') or 'NO',
            'in_suno_catalog': new.get('In_SUNO_Catalog') or 'NO',
            'in_master_csv': new.get('In_Master_CSV') or 'NO',
            
            # Content availability
            'has_lyrics': new.get('Has_Lyrics') or 'NO',
            'has_metadata_tags': existing.get('has_metadata') or new.get('Has_Metadata_Tags') or 'NO',
            
            # Transcription (from existing catalog)
            'should_transcribe': existing.get('should_transcribe') or ('YES' if existing else 'REVIEW'),
            'transcribed': existing.get('transcribed') or 'NO',
            
            # Quality
            'completeness_score': new.get('Completeness_Score') or '0',
            'status': new.get('Status') or existing.get('status') or 'UNKNOWN',
            'recommendation': new.get('Recommendation') or '',
            
            # Notes
            'notes': existing.get('notes') or '',
            
            # Source tracking
            'in_existing_catalog': 'YES' if existing else 'NO',
            'in_new_analysis': 'YES' if new else 'NO',
            'in_deep_scan': 'YES' if deep else 'NO',
            'scan_depth': deep.get('Depth') or '',
            'scan_location': deep.get('Location') or '',
        }
        
        unified.append(entry)
    
    print("Building unified catalog...\n")
    
    # Save unified catalog
    output = home / 'Music/UNIFIED_MASTER_CATALOG.csv'
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        if unified:
            writer = csv.DictWriter(f, fieldnames=unified[0].keys())
            writer.writeheader()
            writer.writerows(unified)
    
    print(f"? Saved to: {output}\n")
    
    # Statistics
    print("=" * 80)
    print("  ?? UNIFIED CATALOG STATISTICS")
    print("=" * 80 + "\n")
    
    total = len(unified)
    in_existing = sum(1 for e in unified if e['in_existing_catalog'] == 'YES')
    in_new = sum(1 for e in unified if e['in_new_analysis'] == 'YES')
    in_deep = sum(1 for e in unified if e['in_deep_scan'] == 'YES')
    in_all_three = sum(1 for e in unified if e['in_existing_catalog'] == 'YES' and e['in_new_analysis'] == 'YES' and e['in_deep_scan'] == 'YES')
    
    your_music = sum(1 for e in unified if e['is_your_music'] == 'YES')
    complete = sum(1 for e in unified if e['status'] == 'COMPLETE')
    has_lyrics = sum(1 for e in unified if e['has_lyrics'] == 'YES')
    has_bundles = sum(1 for e in unified if e['has_bundle'] == 'YES')
    should_transcribe = sum(1 for e in unified if e['should_transcribe'] == 'YES')
    already_transcribed = sum(1 for e in unified if e['transcribed'] not in ['NO', ''])
    
    print(f"Total unique audio files: {total}\n")
    
    print("Source coverage:")
    print(f"  In existing catalog: {in_existing}")
    print(f"  In new analysis: {in_new}")
    print(f"  In deep scan: {in_deep}")
    print(f"  In all three sources: {in_all_three}")
    print()
    
    print("Your music:")
    print(f"  Your original songs: {your_music}")
    print(f"  Fully complete: {complete}")
    print(f"  With lyrics: {has_lyrics}")
    print(f"  In bundles: {has_bundles}")
    print()
    
    print("Transcription status:")
    print(f"  Should transcribe: {should_transcribe}")
    print(f"  Already transcribed: {already_transcribed}")
    print(f"  Need to transcribe: {should_transcribe - already_transcribed}")
    print()
    
    # Content type breakdown
    by_type = defaultdict(int)
    for e in unified:
        if e['content_type']:
            by_type[e['content_type']] += 1
    
    print("By content type:")
    for ct, count in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"  {ct}: {count}")
    
    print()
    print("=" * 80)
    print("  ? UNIFIED CATALOG COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"?? Unified catalog: {output}\n")
    
    print("This catalog combines:")
    print("  ? Existing metadata catalog (525 songs)")
    print("  ? Comprehensive reanalysis (1,256 files)")
    print("  ? Deep scan results (6,068 files)")
    print("  ? Google Sheets matches")
    print("  ? SUNO catalog verification")
    print("  ? Song bundle status")
    print()
    
    print("Use this as your ONE source of truth!")
    print()
    print(f"Open: open '{output}'")

if __name__ == '__main__':
    main()
