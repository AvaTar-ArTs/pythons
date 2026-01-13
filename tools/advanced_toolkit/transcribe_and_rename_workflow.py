#!/usr/bin/env python3
"""
Transcribe and Rename Workflow
Step 1: Transcribe files with bad names
Step 2: Use transcription to generate proper names
Step 3: Rename files intelligently
"""

import csv
from pathlib import Path
import subprocess
import json
import re
from datetime import datetime

def transcribe_file(audio_path: Path, model: str = 'base') -> dict:
    """Transcribe audio file using Whisper"""
    
    print(f"  Transcribing: {audio_path.name}")
    
    try:
        # Run whisper
        result = subprocess.run(
            ['whisper', str(audio_path),
             '--model', model,
             '--output_format', 'json',
             '--output_dir', str(audio_path.parent),
             '--language', 'en'],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            # Load JSON output
            json_path = audio_path.with_suffix('.json')
            if json_path.exists():
                with open(json_path, 'r') as f:
                    data = json.load(f)
                    return {
                        'success': True,
                        'text': data.get('text', ''),
                        'segments': data.get('segments', []),
                        'json_path': str(json_path)
                    }
        
        return {'success': False, 'error': 'Whisper failed'}
        
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'Timeout'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def extract_title_from_transcription(text: str, lyrics_patterns: list = None) -> str:
    """Extract likely song title from transcription"""
    
    if not text:
        return ""
    
    # Clean text
    text = text.strip()
    
    # Common patterns for song titles in transcriptions
    # Look for phrases that might be titles
    
    # Remove common music notation
    text = re.sub(r'\[.*?\]', '', text)  # Remove [Music], [Verse], etc.
    
    # Get first meaningful line (often the hook/chorus)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    if not lines:
        return ""
    
    # Look for repeated phrases (likely chorus/hook)
    phrases = {}
    for line in lines:
        if len(line) > 10 and len(line) < 100:  # Reasonable title length
            phrases[line] = phrases.get(line, 0) + 1
    
    # Get most repeated phrase
    if phrases:
        most_common = max(phrases.items(), key=lambda x: x[1])
        if most_common[1] > 1:  # Appears more than once
            return most_common[0][:80]  # Limit length
    
    # Otherwise, use first line
    first_line = lines[0]
    
    # Clean up first line
    first_line = re.sub(r'^(music|song|audio|recording)\s*', '', first_line, flags=re.IGNORECASE)
    first_line = first_line[:80]  # Limit length
    
    return first_line

def generate_proper_filename(title: str, artist: str, original_filename: str) -> str:
    """Generate proper filename from title and artist"""
    
    # Use title if available
    if title and len(title) > 3:
        # Clean title for filename
        clean_title = re.sub(r'[<>:"/\\|?*]', '', title)
        clean_title = re.sub(r'\s+', ' ', clean_title).strip()
        
        if artist and artist not in ['Unknown', '']:
            # Clean artist
            clean_artist = re.sub(r'[<>:"/\\|?*]', '', artist)
            clean_artist = re.sub(r'\s+', ' ', clean_artist).strip()
            
            new_name = f"{clean_artist} - {clean_title}"
        else:
            new_name = clean_title
        
        # Limit length
        if len(new_name) > 150:
            new_name = new_name[:150]
        
        return new_name
    
    # Fallback to original
    return Path(original_filename).stem

def main():
    print("\n" + "??" * 40)
    print("  TRANSCRIBE AND RENAME WORKFLOW")
    print("  Step-by-step process for fixing bad filenames")
    print("??" * 40 + "\n")
    
    home = Path.home()
    needs_work_csv = home / 'Music/FILES_NEEDING_TRANSCRIPTION_TO_RENAME.csv'
    
    if not needs_work_csv.exists():
        print("? FILES_NEEDING_TRANSCRIPTION_TO_RENAME.csv not found")
        print("Run identify_files_needing_transcription.py first")
        return
    
    # Load files that need work
    print("Loading files that need transcription...\n")
    
    files_to_process = []
    with open(needs_work_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only HIGH priority + your music
            if (row.get('Priority') == 'HIGH' and 
                row.get('Is_Your_Music') in ['YES', 'True', 'TRUE'] and
                row.get('Content_Type') == 'SONG'):
                files_to_process.append(row)
    
    print(f"? Found {len(files_to_process)} HIGH priority songs (your music only)\n")
    
    if len(files_to_process) == 0:
        print("No HIGH priority files to process!")
        return
    
    # Limit to reasonable batch
    batch_size = 10
    if len(files_to_process) > batch_size:
        print(f"Processing first {batch_size} files as a test batch...\n")
        files_to_process = files_to_process[:batch_size]
    
    print("=" * 80)
    print("  BATCH TRANSCRIPTION")
    print("=" * 80 + "\n")
    
    results = []
    
    for i, file_info in enumerate(files_to_process, 1):
        filepath = file_info.get('Filepath', '')
        
        if not filepath or not Path(filepath).exists():
            print(f"[{i}/{len(files_to_process)}] ??  File not found: {file_info.get('Filename')}\n")
            continue
        
        audio_path = Path(filepath)
        
        print(f"[{i}/{len(files_to_process)}] {audio_path.name}")
        print(f"  Current title: {file_info.get('Current_Title') or 'None'}")
        print(f"  Issues: {file_info.get('Issues')}")
        
        # Transcribe
        transcription = transcribe_file(audio_path, model='base')
        
        if transcription['success']:
            # Extract title from transcription
            extracted_title = extract_title_from_transcription(transcription['text'])
            
            # Generate proper filename
            new_filename = generate_proper_filename(
                extracted_title,
                file_info.get('Artist', ''),
                audio_path.name
            )
            
            print(f"  ? Transcribed successfully")
            print(f"  ?? Detected content: {transcription['text'][:100]}...")
            print(f"  ?? Suggested title: {extracted_title}")
            print(f"  ?? Suggested filename: {new_filename}.mp3")
            
            results.append({
                'original_filename': audio_path.name,
                'original_path': filepath,
                'current_title': file_info.get('Current_Title', ''),
                'artist': file_info.get('Artist', ''),
                'transcription_text': transcription['text'],
                'extracted_title': extracted_title,
                'suggested_filename': new_filename + '.mp3',
                'suggested_new_path': str(audio_path.parent / f"{new_filename}.mp3"),
                'transcription_json': transcription.get('json_path', ''),
                'status': 'READY_TO_RENAME'
            })
        else:
            print(f"  ? Transcription failed: {transcription.get('error')}")
            
            results.append({
                'original_filename': audio_path.name,
                'original_path': filepath,
                'current_title': file_info.get('Current_Title', ''),
                'artist': file_info.get('Artist', ''),
                'transcription_text': '',
                'extracted_title': '',
                'suggested_filename': '',
                'suggested_new_path': '',
                'transcription_json': '',
                'status': f"FAILED: {transcription.get('error')}"
            })
        
        print()
    
    # Save results
    print("=" * 80)
    print("  SAVING RESULTS")
    print("=" * 80 + "\n")
    
    output = home / 'Music/TRANSCRIPTION_AND_RENAME_RESULTS.csv'
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        if results:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
    
    print(f"? Saved to: {output}\n")
    
    # Summary
    success = sum(1 for r in results if r['status'] == 'READY_TO_RENAME')
    failed = sum(1 for r in results if r['status'].startswith('FAILED'))
    
    print(f"Successfully transcribed: {success}")
    print(f"Failed: {failed}")
    print()
    
    if success > 0:
        print("=" * 80)
        print("  ?? RENAME RECOMMENDATIONS")
        print("=" * 80 + "\n")
        
        for i, result in enumerate([r for r in results if r['status'] == 'READY_TO_RENAME'], 1):
            print(f"{i}. OLD: {result['original_filename']}")
            print(f"   NEW: {result['suggested_filename']}")
            print(f"   Based on: \"{result['extracted_title']}\"")
            print()
        
        print("Review these suggestions, then:")
        print("  1. Edit TRANSCRIPTION_AND_RENAME_RESULTS.csv if needed")
        print("  2. Run the rename script (I'll create it)")
        print()
    
    print(f"Open: open '{output}'")

if __name__ == '__main__':
    main()
