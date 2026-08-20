#!/usr/bin/env python3
"""
ULTIMATE MASTER REPORT
Combines all analysis into one comprehensive view
"""

import csv
from pathlib import Path
from collections import defaultdict

def load_csv_to_dict(filepath: Path, key_field: str) -> dict:
    """Load CSV and index by key field"""
    data = {}
    if not filepath.exists():
        return data
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row.get(key_field, '').strip()
            if key:
                data[key] = row
    
    return data

def normalize_title(title: str) -> str:
    """Normalize title for matching"""
    if not title:
        return ""
    return title.lower().replace('_', ' ').replace('-', ' ').strip()

def main():
    print("\n" + "??" * 40)
    print("  ULTIMATE MASTER REPORT")
    print("  All data sources unified")
    print("??" * 40 + "\n")
    
    home = Path.home()
    
    # Load all data sources
    print("Loading all data sources...\n")
    
    # 1. Master CSV with all fields
    master_file = home / 'Music/MASTER_COMPLETE_ALL_FIELDS.csv'
    master_data = {}
    if master_file.exists():
        with open(master_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get('Title', '')
                if title:
                    master_data[normalize_title(title)] = row
        print(f"? Master CSV: {len(master_data)} entries")
    
    # 2. Duration analysis
    duration_file = home / 'Music/DURATION_ANALYSIS.csv'
    duration_data = {}
    if duration_file.exists():
        with open(duration_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get('Title', '')
                if title:
                    duration_data[normalize_title(title)] = row
        print(f"? Duration analysis: {len(duration_data)} entries")
    
    # 3. Content-aware analysis
    content_file = home / 'Music/DEEP_CONTENT_AWARE_ANALYSIS.csv'
    content_data = {}
    if content_file.exists():
        with open(content_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                filename = row.get('Filename', '')
                title = row.get('Title', '')
                key = normalize_title(title) if title else normalize_title(filename)
                if key:
                    content_data[key] = row
        print(f"? Content-aware analysis: {len(content_data)} entries")
    
    print()
    
    # Combine all unique entries
    print("Combining all entries...\n")
    
    all_keys = set()
    all_keys.update(master_data.keys())
    all_keys.update(duration_data.keys())
    all_keys.update(content_data.keys())
    
    print(f"Total unique songs/files: {len(all_keys)}\n")
    
    # Build ultimate report
    print("Building ultimate report...\n")
    
    ultimate_data = []
    
    for key in sorted(all_keys):
        master = master_data.get(key, {})
        duration = duration_data.get(key, {})
        content = content_data.get(key, {})
        
        # Determine best title
        title = (master.get('Title') or duration.get('Title') or 
                content.get('Title') or key)
        
        # Determine overall status
        has_audio_file = bool(content.get('Filepath') or master.get('Local_Filenames'))
        has_master_entry = bool(master)
        has_duration = bool(duration.get('Duration'))
        has_lyrics = bool(master.get('Lyrics'))
        has_metadata = bool(master.get('Genre') or master.get('Style'))
        
        # Calculate completeness score
        completeness_score = sum([
            has_audio_file * 2,  # Audio file worth 2 points
            has_master_entry,
            has_duration,
            has_lyrics,
            has_metadata
        ])
        
        # Determine overall status
        if completeness_score >= 5:
            overall_status = 'COMPLETE'
            priority = 'LOW'
            recommendation = 'Fully documented and ready'
        elif has_audio_file and has_duration and has_metadata:
            overall_status = 'GOOD'
            priority = 'LOW'
            recommendation = 'Has essentials, could add lyrics'
        elif has_audio_file:
            overall_status = 'HAS_FILE'
            priority = 'MEDIUM'
            recommendation = 'Has audio, add metadata'
        elif has_master_entry:
            overall_status = 'NEED_DOWNLOAD'
            priority = 'HIGH'
            recommendation = 'Download from Suno'
        else:
            overall_status = 'UNKNOWN'
            priority = 'REVIEW'
            recommendation = 'Review and classify'
        
        ultimate_data.append({
            'Title': title,
            'Artist': master.get('Artist', ''),
            'Overall_Status': overall_status,
            'Priority': priority,
            'Completeness_Score': completeness_score,
            
            # Audio file info
            'Has_Audio_File': 'YES' if has_audio_file else 'NO',
            'Filepath': content.get('Filepath', '') or master.get('File_Path', ''),
            'Filename': content.get('Filename', '') or master.get('Local_Filenames', ''),
            
            # Duration & classification
            'Duration': duration.get('Duration', '') or master.get('Duration', ''),
            'Content_Type': duration.get('Content_Type', ''),
            
            # Metadata
            'Has_Lyrics': 'YES' if has_lyrics else 'NO',
            'Has_Metadata': 'YES' if has_metadata else 'NO',
            'Genre': master.get('Genre', ''),
            'Style': master.get('Style', ''),
            'Mood': master.get('Mood', ''),
            
            # URLs
            'Song_URL': master.get('Song_URL', ''),
            'Cover_URL': master.get('Cover_URL', ''),
            
            # Status from sources
            'Master_Status': master.get('Status', ''),
            'Duration_Source': duration.get('Duration_Source', ''),
            'Content_Completeness': content.get('Content_Completeness', ''),
            
            # Recommendation
            'Recommendation': recommendation
        })
    
    # Save ultimate report
    output = home / 'Music/ULTIMATE_MASTER_REPORT.csv'
    
    print("Saving ultimate report...\n")
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        if ultimate_data:
            writer = csv.DictWriter(f, fieldnames=ultimate_data[0].keys())
            writer.writeheader()
            writer.writerows(ultimate_data)
    
    print(f"? Saved to: {output}\n")
    
    # Statistics
    print("=" * 80)
    print("  ?? ULTIMATE STATISTICS")
    print("=" * 80 + "\n")
    
    by_status = defaultdict(int)
    by_priority = defaultdict(int)
    by_content_type = defaultdict(int)
    
    for item in ultimate_data:
        by_status[item['Overall_Status']] += 1
        by_priority[item['Priority']] += 1
        if item['Content_Type']:
            by_content_type[item['Content_Type']] += 1
    
    print(f"Total unique entries: {len(ultimate_data)}\n")
    
    print("By Overall Status:")
    print(f"  ? COMPLETE: {by_status['COMPLETE']}")
    print(f"  ?? GOOD: {by_status['GOOD']}")
    print(f"  ?? HAS_FILE: {by_status['HAS_FILE']}")
    print(f"  ?? NEED_DOWNLOAD: {by_status['NEED_DOWNLOAD']}")
    print(f"  ? UNKNOWN: {by_status['UNKNOWN']}")
    print()
    
    print("By Priority:")
    print(f"  ?? HIGH (need download): {by_priority['HIGH']}")
    print(f"  ?? MEDIUM (need metadata): {by_priority['MEDIUM']}")
    print(f"  ?? LOW (ready): {by_priority['LOW']}")
    print(f"  ? REVIEW: {by_priority['REVIEW']}")
    print()
    
    print("By Content Type:")
    for ct, count in sorted(by_content_type.items(), key=lambda x: -x[1]):
        print(f"  {ct}: {count}")
    print()
    
    print("=" * 80)
    print("  ? ULTIMATE REPORT COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"?? Ultimate report: {output}\n")
    print("This report combines:")
    print("  ? Master CSV (all fields)")
    print("  ? Duration analysis (content types)")
    print("  ? Content-aware analysis (file matching)")
    print("  ? Google Sheets (2 sources)")
    print("  ? SUNO catalogs (21 CSV files)")
    print()
    print("Sort/filter by:")
    print("  ? Overall_Status - COMPLETE, GOOD, HAS_FILE, NEED_DOWNLOAD")
    print("  ? Priority - HIGH, MEDIUM, LOW, REVIEW")
    print("  ? Content_Type - SONG, SHORT_CLIP, EXTENDED, etc.")
    print("  ? Completeness_Score - Higher = more complete")
    print()
    print(f"Open: open '{output}'")

if __name__ == '__main__':
    main()
