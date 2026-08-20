#!/usr/bin/env python3
"""
Identify Files Needing Transcription for Proper Naming
Many files have bad names (UUIDs, numbers, etc.) that can only be fixed 
after we listen/transcribe them
"""

import csv
from pathlib import Path
import re

def is_bad_filename(filename: str, title: str) -> tuple:
    """Determine if filename is poor quality and needs transcription to fix"""
    
    stem = Path(filename).stem
    reasons = []
    priority = 'LOW'
    
    # Check for UUID/hash patterns
    if re.match(r'^[a-f0-9]{8,}', stem):
        reasons.append('UUID/hash filename')
        priority = 'HIGH'
    
    # Check for just numbers
    if re.match(r'^\d+$', stem) or re.match(r'^\d+[-_]\d+', stem):
        reasons.append('Numeric only filename')
        priority = 'HIGH'
    
    # Check for very short names (< 3 chars)
    if len(stem) < 3:
        reasons.append('Very short filename')
        priority = 'HIGH'
    
    # Check for generic names
    generic_names = ['audio', 'track', 'song', 'untitled', 'recording', 'new recording', 'voice memo']
    if any(g in stem.lower() for g in generic_names):
        reasons.append('Generic filename')
        priority = 'MEDIUM'
    
    # Check for confusing patterns
    if re.search(r'[\(\)\[\]]{3,}', stem):
        reasons.append('Too many brackets/parentheses')
        priority = 'MEDIUM'
    
    # Check for very long names
    if len(stem) > 100:
        reasons.append('Filename too long')
        priority = 'LOW'
    
    # Check if title is empty or same as filename
    if not title or title.strip() == '' or title == stem:
        reasons.append('No title metadata')
        if priority == 'LOW':
            priority = 'MEDIUM'
    
    # Check for underscore/dash only separators (not human readable)
    if re.match(r'^[a-zA-Z0-9_\-]+$', stem) and ('_' in stem or '-' in stem):
        if len(stem.split('_')) > 5 or len(stem.split('-')) > 5:
            reasons.append('Machine-generated name pattern')
            if priority == 'LOW':
                priority = 'MEDIUM'
    
    return (len(reasons) > 0, priority, reasons)

def main():
    print("\n" + "??" * 40)
    print("  IDENTIFY FILES NEEDING TRANSCRIPTION")
    print("  Find files with bad names that need listening")
    print("??" * 40 + "\n")
    
    home = Path.home()
    catalog = home / 'Music/UNIFIED_MASTER_CATALOG.csv'
    
    if not catalog.exists():
        print(f"? Unified catalog not found: {catalog}")
        return
    
    print("Loading unified catalog...\n")
    
    entries = []
    with open(catalog, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        entries = list(reader)
    
    print(f"? Loaded {len(entries)} entries\n")
    
    print("Analyzing filenames...\n")
    
    needs_work = []
    
    for i, entry in enumerate(entries):
        if (i + 1) % 1000 == 0:
            print(f"  Processing {i + 1}/{len(entries)}...")
        
        filename = entry.get('filename') or entry.get('current_filename') or ''
        title = entry.get('title') or ''
        filepath = entry.get('filepath') or entry.get('current_path') or ''
        is_yours = entry.get('is_your_music') or entry.get('is_music') or ''
        content_type = entry.get('content_type') or ''
        
        # Skip non-music content
        if content_type in ['SHORT_CLIP', 'FRAGMENT']:
            continue
        
        # Check if filename is bad
        needs_fix, priority, reasons = is_bad_filename(filename, title)
        
        if needs_fix:
            needs_work.append({
                'filename': filename,
                'current_title': title,
                'filepath': filepath,
                'artist': entry.get('artist', ''),
                'album': entry.get('album') or entry.get('current_album') or '',
                'duration': entry.get('duration_seconds') or entry.get('duration') or '',
                'content_type': content_type,
                'is_your_music': is_yours,
                'priority': priority,
                'issues': ' | '.join(reasons),
                'should_transcribe': entry.get('should_transcribe', 'YES'),
                'transcribed': entry.get('transcribed', 'NO'),
                'completeness_score': entry.get('completeness_score', '0'),
            })
    
    print(f"\n? Found {len(needs_work)} files with naming issues\n")
    
    # Save report
    output = home / 'Music/FILES_NEEDING_TRANSCRIPTION_TO_RENAME.csv'
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Filename', 'Current_Title', 'Artist', 'Album',
            'Duration', 'Content_Type', 'Is_Your_Music',
            'Priority', 'Issues', 'Filepath',
            'Should_Transcribe', 'Transcribed',
            'Completeness_Score', 'Workflow_Step'
        ])
        
        for item in sorted(needs_work, key=lambda x: (x['priority'], x['filename'])):
            # Determine workflow step
            if item['transcribed'] not in ['NO', '']:
                workflow = '3. RENAME (transcription done)'
            elif item['should_transcribe'] == 'YES':
                workflow = '1. TRANSCRIBE FIRST'
            else:
                workflow = '2. SET should_transcribe=YES'
            
            writer.writerow([
                item['filename'],
                item['current_title'],
                item['artist'],
                item['album'],
                item['duration'],
                item['content_type'],
                item['is_your_music'],
                item['priority'],
                item['issues'],
                item['filepath'],
                item['should_transcribe'],
                item['transcribed'],
                item['completeness_score'],
                workflow
            ])
    
    print(f"? Saved to: {output}\n")
    
    # Statistics
    print("=" * 80)
    print("  ?? NAMING ISSUES ANALYSIS")
    print("=" * 80 + "\n")
    
    by_priority = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
    by_workflow = {
        '1. TRANSCRIBE FIRST': 0,
        '2. SET should_transcribe=YES': 0,
        '3. RENAME (transcription done)': 0
    }
    
    your_music_bad_names = 0
    
    for item in needs_work:
        by_priority[item['priority']] += 1
        
        if item['transcribed'] not in ['NO', '']:
            by_workflow['3. RENAME (transcription done)'] += 1
        elif item['should_transcribe'] == 'YES':
            by_workflow['1. TRANSCRIBE FIRST'] += 1
        else:
            by_workflow['2. SET should_transcribe=YES'] += 1
        
        if item['is_your_music'] in ['YES', 'True', 'TRUE']:
            your_music_bad_names += 1
    
    print(f"Total files with naming issues: {len(needs_work)}\n")
    
    print("By priority:")
    print(f"  ?? HIGH: {by_priority['HIGH']} (UUIDs, numbers, very short)")
    print(f"  ?? MEDIUM: {by_priority['MEDIUM']} (generic, confusing)")
    print(f"  ?? LOW: {by_priority['LOW']} (minor issues)")
    print()
    
    print("By workflow:")
    for workflow, count in sorted(by_workflow.items()):
        print(f"  {workflow}: {count}")
    print()
    
    print(f"Your music with bad names: {your_music_bad_names}\n")
    
    # Show examples
    print("=" * 80)
    print("  EXAMPLES OF NAMING ISSUES")
    print("=" * 80 + "\n")
    
    print("HIGH Priority (need transcription urgently):")
    high_priority = [n for n in needs_work if n['priority'] == 'HIGH'][:10]
    for i, item in enumerate(high_priority, 1):
        print(f"  {i}. {item['filename']}")
        print(f"     Issues: {item['issues']}")
        print(f"     Path: {item['filepath']}")
    
    print()
    print("=" * 80)
    print("  ? ANALYSIS COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"?? Full report: {output}\n")
    
    print("Recommended workflow:")
    print("  1. Filter by Priority = HIGH")
    print("  2. Filter by Workflow_Step = '1. TRANSCRIBE FIRST'")
    print("  3. Transcribe those files")
    print("  4. Use transcription to determine proper song title")
    print("  5. Rename file based on actual content")
    print()
    
    print("Ready to transcribe? I can create:")
    print("  ? Batch transcription script for priority files")
    print("  ? Auto-rename script (uses transcription results)")
    print("  ? Quality check script (verify transcriptions)")
    print()
    
    print(f"Open: open '{output}'")

if __name__ == '__main__':
    main()
