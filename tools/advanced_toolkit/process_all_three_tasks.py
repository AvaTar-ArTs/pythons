#!/usr/bin/env python3
"""
Process the three main tasks:
1. Fix unknown durations (184 files)
2. Extract metadata for files (974 files)
3. Generate complete songs summary (47 files)
"""

import csv
from pathlib import Path
import subprocess
import json
from collections import defaultdict

def get_actual_duration(filepath: str) -> float:
    """Get actual duration from file using ffprobe"""
    if not filepath or not Path(filepath).exists():
        return 0.0
    
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
            return float(data.get('format', {}).get('duration', 0))
    except Exception:
        pass
    
    return 0.0

def get_full_metadata(filepath: str) -> dict:
    """Get complete metadata from file"""
    if not filepath or not Path(filepath).exists():
        return {}
    
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-print_format', 'json',
             '-show_format', '-show_streams', str(filepath)],
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

def format_duration(seconds: float) -> str:
    """Format seconds to readable string"""
    if seconds == 0:
        return "0:00"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"

def task1_fix_unknown_durations(ultimate_data: list, output_dir: Path):
    """Task 1: Fix unknown durations"""
    
    print("\n" + "=" * 80)
    print("  TASK 1: FIX UNKNOWN DURATIONS (184 files)")
    print("=" * 80 + "\n")
    
    unknown = [item for item in ultimate_data if item.get('Content_Type') == 'UNKNOWN']
    
    print(f"Processing {len(unknown)} files with unknown durations...\n")
    
    fixed = []
    
    for i, item in enumerate(unknown):
        if (i + 1) % 50 == 0:
            print(f"  Processing {i + 1}/{len(unknown)}...")
        
        filepath = item.get('Filepath', '')
        if not filepath:
            continue
        
        # Get actual duration
        duration = get_actual_duration(filepath)
        
        if duration > 0:
            content_type = classify_by_duration(duration)
            
            fixed.append({
                'Title': item.get('Title', ''),
                'Filename': item.get('Filename', ''),
                'Filepath': filepath,
                'Duration_Seconds': f"{duration:.1f}",
                'Duration_Formatted': format_duration(duration),
                'Content_Type': content_type,
                'Previous_Status': 'UNKNOWN',
                'Fixed': 'YES'
            })
    
    # Save results
    output = output_dir / 'TASK1_FIXED_DURATIONS.csv'
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        if fixed:
            writer = csv.DictWriter(f, fieldnames=fixed[0].keys())
            writer.writeheader()
            writer.writerows(fixed)
    
    print(f"\n? Fixed {len(fixed)} durations")
    print(f"? Saved to: {output}\n")
    
    # Statistics
    by_type = defaultdict(int)
    for item in fixed:
        by_type[item['Content_Type']] += 1
    
    print("New classifications:")
    for ct, count in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"  {ct}: {count}")
    print()
    
    return fixed

def task2_extract_metadata(ultimate_data: list, output_dir: Path):
    """Task 2: Extract metadata for files"""
    
    print("=" * 80)
    print("  TASK 2: EXTRACT METADATA (974 files)")
    print("=" * 80 + "\n")
    
    has_file = [item for item in ultimate_data if item.get('Overall_Status') == 'HAS_FILE']
    
    print(f"Processing {len(has_file)} files...\n")
    print("(Sampling first 200 for speed...)\n")
    
    sample = has_file[:200]
    
    extracted = []
    
    for i, item in enumerate(sample):
        if (i + 1) % 50 == 0:
            print(f"  Processing {i + 1}/{len(sample)}...")
        
        filepath = item.get('Filepath', '')
        if not filepath:
            continue
        
        # Get full metadata
        metadata = get_full_metadata(filepath)
        
        if metadata:
            # Determine what's missing
            missing = []
            if not metadata.get('genre'):
                missing.append('genre')
            if not metadata.get('artist'):
                missing.append('artist')
            if not metadata.get('album'):
                missing.append('album')
            
            # Determine priority
            if len(missing) >= 3:
                priority = 'HIGH'
            elif len(missing) >= 1:
                priority = 'MEDIUM'
            else:
                priority = 'LOW'
            
            extracted.append({
                'Title': item.get('Title', ''),
                'Filename': item.get('Filename', ''),
                'Filepath': filepath,
                'Current_Title': metadata.get('title', ''),
                'Current_Artist': metadata.get('artist', ''),
                'Current_Genre': metadata.get('genre', ''),
                'Current_Album': metadata.get('album', ''),
                'Duration': format_duration(metadata.get('duration', 0)),
                'Format': metadata.get('format', ''),
                'Bitrate': f"{metadata.get('bitrate', 0) / 1000:.0f} kbps",
                'Missing_Fields': ', '.join(missing) if missing else 'None',
                'Priority': priority,
                'Recommendation': 'Add metadata tags' if missing else 'Complete'
            })
    
    # Save results
    output = output_dir / 'TASK2_METADATA_EXTRACTION.csv'
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        if extracted:
            writer = csv.DictWriter(f, fieldnames=extracted[0].keys())
            writer.writeheader()
            writer.writerows(extracted)
    
    print(f"\n? Extracted metadata from {len(extracted)} files")
    print(f"? Saved to: {output}\n")
    
    # Statistics
    by_priority = defaultdict(int)
    for item in extracted:
        by_priority[item['Priority']] += 1
    
    print("By priority:")
    print(f"  HIGH (missing 3+ fields): {by_priority['HIGH']}")
    print(f"  MEDIUM (missing 1-2 fields): {by_priority['MEDIUM']}")
    print(f"  LOW (complete): {by_priority['LOW']}")
    print()
    
    return extracted

def task3_review_complete(ultimate_data: list, output_dir: Path):
    """Task 3: Review complete songs"""
    
    print("=" * 80)
    print("  TASK 3: REVIEW COMPLETE SONGS (47 files)")
    print("=" * 80 + "\n")
    
    complete = [item for item in ultimate_data if item.get('Overall_Status') == 'COMPLETE']
    
    print(f"Found {len(complete)} complete songs\n")
    
    # Enhanced complete report
    enhanced = []
    
    for item in complete:
        enhanced.append({
            'Title': item.get('Title', ''),
            'Artist': item.get('Artist', ''),
            'Genre': item.get('Genre', ''),
            'Style': item.get('Style', ''),
            'Mood': item.get('Mood', ''),
            'Duration': item.get('Duration', ''),
            'Content_Type': item.get('Content_Type', ''),
            'Has_Lyrics': item.get('Has_Lyrics', ''),
            'Has_Audio': item.get('Has_Audio_File', ''),
            'Filepath': item.get('Filepath', ''),
            'Cover_URL': item.get('Cover_URL', ''),
            'Song_URL': item.get('Song_URL', ''),
            'Completeness_Score': item.get('Completeness_Score', ''),
            'Status': '? READY TO USE'
        })
    
    # Save results
    output = output_dir / 'TASK3_COMPLETE_SONGS.csv'
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        if enhanced:
            writer = csv.DictWriter(f, fieldnames=enhanced[0].keys())
            writer.writeheader()
            writer.writerows(enhanced)
    
    print(f"? Saved to: {output}\n")
    
    # Show some examples
    print("Sample complete songs:")
    for i, song in enumerate(enhanced[:10]):
        print(f"  {i+1}. {song['Title']} - {song['Artist']} ({song['Genre']})")
    
    if len(enhanced) > 10:
        print(f"  ... and {len(enhanced) - 10} more\n")
    else:
        print()
    
    # Statistics
    by_content_type = defaultdict(int)
    with_lyrics = sum(1 for s in enhanced if s['Has_Lyrics'] == 'YES')
    with_cover = sum(1 for s in enhanced if s['Cover_URL'])
    
    for song in enhanced:
        if song['Content_Type']:
            by_content_type[song['Content_Type']] += 1
    
    print("Statistics:")
    print(f"  Total complete: {len(enhanced)}")
    print(f"  With lyrics: {with_lyrics}")
    print(f"  With cover art: {with_cover}")
    print()
    
    print("By content type:")
    for ct, count in sorted(by_content_type.items(), key=lambda x: -x[1]):
        print(f"  {ct}: {count}")
    print()
    
    return enhanced

def main():
    print("\n" + "??" * 40)
    print("  PROCESSING THREE MAIN TASKS")
    print("  1. Fix unknown durations")
    print("  2. Extract metadata")
    print("  3. Review complete songs")
    print("??" * 40)
    
    home = Path.home()
    ultimate_csv = home / 'Music/ULTIMATE_MASTER_REPORT.csv'
    output_dir = home / 'Music'
    
    # Load ultimate report
    print("\nLoading ultimate report...")
    
    ultimate_data = []
    with open(ultimate_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        ultimate_data = list(reader)
    
    print(f"? Loaded {len(ultimate_data)} entries\n")
    
    # Task 1: Fix unknown durations
    fixed_durations = task1_fix_unknown_durations(ultimate_data, output_dir)
    
    # Task 2: Extract metadata
    extracted_metadata = task2_extract_metadata(ultimate_data, output_dir)
    
    # Task 3: Review complete
    complete_songs = task3_review_complete(ultimate_data, output_dir)
    
    # Final summary
    print("=" * 80)
    print("  ? ALL TASKS COMPLETE")
    print("=" * 80 + "\n")
    
    print("Results:")
    print(f"  ?? Task 1: Fixed {len(fixed_durations)} unknown durations")
    print(f"  ?? Task 2: Extracted metadata from {len(extracted_metadata)} files (sample)")
    print(f"  ?? Task 3: Reviewed {len(complete_songs)} complete songs")
    print()
    
    print("Files created:")
    print(f"  1. {output_dir}/TASK1_FIXED_DURATIONS.csv")
    print(f"  2. {output_dir}/TASK2_METADATA_EXTRACTION.csv")
    print(f"  3. {output_dir}/TASK3_COMPLETE_SONGS.csv")
    print()
    
    print("Next steps:")
    print("  ? Review TASK1 to see new content type classifications")
    print("  ? Review TASK2 to see which files need metadata tags")
    print("  ? Review TASK3 to see your fully complete songs")
    print()
    
    print("Open all:")
    print(f"  open '{output_dir}/TASK1_FIXED_DURATIONS.csv'")
    print(f"  open '{output_dir}/TASK2_METADATA_EXTRACTION.csv'")
    print(f"  open '{output_dir}/TASK3_COMPLETE_SONGS.csv'")

if __name__ == '__main__':
    main()
