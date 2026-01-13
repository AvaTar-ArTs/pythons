#!/usr/bin/env python3
"""
Analyze ALL durations from master CSV + actual files
Sort out content types by duration
"""

import csv
from pathlib import Path
import subprocess
import json
from collections import defaultdict

def parse_duration(duration_str: str) -> float:
    """Parse duration string to seconds"""
    if not duration_str:
        return 0.0
    
    try:
        # Try direct float conversion
        return float(duration_str)
    except ValueError:
        pass
    
    # Try MM:SS or HH:MM:SS format
    parts = duration_str.split(':')
    try:
        if len(parts) == 2:  # MM:SS
            return int(parts[0]) * 60 + float(parts[1])
        elif len(parts) == 3:  # HH:MM:SS
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    except (ValueError, IndexError):
        pass
    
    return 0.0

def get_file_duration(filepath: str) -> float:
    """Get actual duration from audio file using ffprobe"""
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

def classify_by_duration(duration: float) -> str:
    """Classify content type by duration"""
    if duration == 0:
        return 'UNKNOWN'
    elif duration < 30:
        return 'SHORT_CLIP'  # UI sounds, jingles, clips
    elif 30 <= duration <= 360:  # 30s to 6 min
        return 'SONG'
    elif 360 < duration <= 900:  # 6-15 min
        return 'EXTENDED'  # Long songs, short podcasts/stories
    elif 900 < duration <= 1800:  # 15-30 min
        return 'PODCAST/STORY'
    else:  # > 30 min
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

def main():
    print("\n" + "?? " * 40)
    print("  DURATION ANALYSIS")
    print("  Classifying content by duration")
    print("?? " * 40 + "\n")
    
    home = Path.home()
    master_csv = home / 'Music/MASTER_COMPLETE_ALL_FIELDS.csv'
    
    print("Loading master CSV...")
    
    entries = []
    with open(master_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        entries = list(reader)
    
    print(f"? Loaded {len(entries)} entries\n")
    
    print("Analyzing durations...")
    print("(Reading actual file durations - this may take a moment)\n")
    
    analyzed = []
    
    for i, entry in enumerate(entries):
        if (i + 1) % 100 == 0:
            print(f"  Processing {i + 1}/{len(entries)}...")
        
        # Get duration from various sources
        duration = 0.0
        source = 'none'
        
        # 1. Try CSV Duration field
        csv_duration = parse_duration(entry.get('Duration', ''))
        if csv_duration > 0:
            duration = csv_duration
            source = 'csv_duration'
        
        # 2. Try CSV Length field
        if duration == 0:
            csv_length = parse_duration(entry.get('Length', ''))
            if csv_length > 0:
                duration = csv_length
                source = 'csv_length'
        
        # 3. Try File_Duration field
        if duration == 0:
            file_duration = parse_duration(entry.get('File_Duration', ''))
            if file_duration > 0:
                duration = file_duration
                source = 'file_duration_field'
        
        # 4. Try reading actual file
        if duration == 0 and entry.get('File_Path'):
            actual_duration = get_file_duration(entry.get('File_Path'))
            if actual_duration > 0:
                duration = actual_duration
                source = 'actual_file'
        
        # Classify
        content_type = classify_by_duration(duration)
        
        analyzed.append({
            'title': entry.get('Title', ''),
            'artist': entry.get('Artist', ''),
            'status': entry.get('Status', ''),
            'duration_seconds': duration,
            'duration_formatted': format_duration(duration),
            'content_type': content_type,
            'duration_source': source,
            'local_file': entry.get('Local_Filenames', ''),
            'file_path': entry.get('File_Path', ''),
            'genre': entry.get('Genre', ''),
            'style': entry.get('Style', ''),
        })
    
    print(f"? Analyzed {len(analyzed)} entries\n")
    
    # Save analysis
    print("Saving duration analysis...\n")
    
    output = home / 'Music/DURATION_ANALYSIS.csv'
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Title', 'Artist', 'Status',
            'Duration', 'Duration_Seconds', 
            'Content_Type', 'Duration_Source',
            'Genre', 'Style',
            'Local_File', 'File_Path'
        ])
        
        # Sort by duration
        for item in sorted(analyzed, key=lambda x: x['duration_seconds']):
            writer.writerow([
                item['title'],
                item['artist'],
                item['status'],
                item['duration_formatted'],
                f"{item['duration_seconds']:.1f}",
                item['content_type'],
                item['duration_source'],
                item['genre'],
                item['style'],
                item['local_file'],
                item['file_path'],
            ])
    
    print(f"? Saved to: {output}\n")
    
    # Statistics
    print("=" * 80)
    print("  ?? DURATION STATISTICS")
    print("=" * 80 + "\n")
    
    by_type = defaultdict(int)
    by_source = defaultdict(int)
    
    for item in analyzed:
        by_type[item['content_type']] += 1
        by_source[item['duration_source']] += 1
    
    print("Content Type Breakdown (by duration):")
    print(f"  ?? SONG (30s - 6min):         {by_type['SONG']}")
    print(f"  ?? SHORT_CLIP (< 30s):        {by_type['SHORT_CLIP']}")
    print(f"  ?? EXTENDED (6-15min):        {by_type['EXTENDED']}")
    print(f"  ???  PODCAST/STORY (15-30min):  {by_type['PODCAST/STORY']}")
    print(f"  ?? AUDIOBOOK/LONG (> 30min):  {by_type['AUDIOBOOK/LONG']}")
    print(f"  ? UNKNOWN (no duration):     {by_type['UNKNOWN']}")
    print()
    
    print("Duration Source Breakdown:")
    print(f"  ?? From CSV Duration field:   {by_source['csv_duration']}")
    print(f"  ?? From CSV Length field:     {by_source['csv_length']}")
    print(f"  ?? From File_Duration field:  {by_source['file_duration_field']}")
    print(f"  ?? From actual file read:     {by_source['actual_file']}")
    print(f"  ? No duration found:         {by_source['none']}")
    print()
    
    # Show examples from each category
    print("=" * 80)
    print("  ?? EXAMPLES BY CATEGORY")
    print("=" * 80 + "\n")
    
    for content_type in ['SHORT_CLIP', 'SONG', 'EXTENDED', 'PODCAST/STORY', 'AUDIOBOOK/LONG']:
        examples = [item for item in analyzed if item['content_type'] == content_type]
        if examples:
            print(f"\n{content_type} ({len(examples)} total):")
            for ex in examples[:5]:  # Show first 5
                print(f"  ? {ex['title'][:50]:50} {ex['duration_formatted']:>8}")
    
    print()
    print("=" * 80)
    print("  ? DURATION ANALYSIS COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"?? Full analysis: {output}")
    print(f"\nUse this to:")
    print(f"  ? Sort by Content_Type to group similar items")
    print(f"  ? Filter SHORT_CLIP to find UI sounds/jingles")
    print(f"  ? Filter SONG to find your music")
    print(f"  ? Filter PODCAST/STORY and AUDIOBOOK/LONG for spoken content")
    print(f"  ? Filter UNKNOWN to find items needing duration data")
    print(f"\nOpen: open '{output}'")

if __name__ == '__main__':
    main()
