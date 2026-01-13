#!/usr/bin/env python3
"""
Deep SUNO Directory Analysis
Content-aware analysis comparing SUNO directory with master CSV
"""

import csv
import json
from pathlib import Path
import subprocess
from collections import defaultdict
from difflib import SequenceMatcher
import hashlib

def normalize_title(title: str) -> str:
    """Normalize title for matching"""
    if not title:
        return ""
    return title.lower().replace('_', ' ').replace('-', ' ').strip()

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

def extract_audio_metadata(filepath: Path) -> dict:
    """Extract metadata from audio file"""
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
                'title': tags.get('title', '') or tags.get('TITLE', ''),
                'artist': tags.get('artist', '') or tags.get('ARTIST', ''),
                'album': tags.get('album', '') or tags.get('ALBUM', ''),
                'genre': tags.get('genre', '') or tags.get('GENRE', ''),
                'comment': tags.get('comment', '') or tags.get('COMMENT', ''),
            }
    except Exception as e:
        pass
    
    return {}

def scan_suno_directory(suno_path: Path) -> dict:
    """Deep scan of SUNO directory"""
    
    print("\n" + "=" * 80)
    print("  SCANNING SUNO DIRECTORY")
    print("=" * 80 + "\n")
    
    results = {
        'audio_files': [],
        'csv_files': [],
        'json_files': [],
        'txt_files': [],
        'other_files': [],
        'directories': [],
    }
    
    print(f"Scanning: {suno_path}\n")
    
    # Scan all files
    for item in suno_path.rglob('*'):
        if item.is_file():
            ext = item.suffix.lower()
            
            if ext in ['.mp3', '.wav', '.m4a', '.flac', '.ogg']:
                results['audio_files'].append(item)
            elif ext == '.csv':
                results['csv_files'].append(item)
            elif ext == '.json':
                results['json_files'].append(item)
            elif ext == '.txt':
                results['txt_files'].append(item)
            else:
                results['other_files'].append(item)
        elif item.is_dir():
            results['directories'].append(item)
    
    print(f"? Found {len(results['audio_files'])} audio files")
    print(f"? Found {len(results['csv_files'])} CSV files")
    print(f"? Found {len(results['json_files'])} JSON files")
    print(f"? Found {len(results['txt_files'])} text files")
    print(f"? Found {len(results['other_files'])} other files")
    print(f"? Found {len(results['directories'])} directories\n")
    
    return results

def load_suno_csvs(csv_files: list) -> dict:
    """Load all CSV files from SUNO directory"""
    
    print("=" * 80)
    print("  LOADING SUNO CSV FILES")
    print("=" * 80 + "\n")
    
    all_songs = {}
    
    for csv_file in csv_files:
        print(f"Loading: {csv_file.name}")
        
        try:
            with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
                print(f"  ? {len(rows)} rows")
                
                for row in rows:
                    # Try different title column names
                    title = (row.get('SongTitle') or row.get('Title') or 
                            row.get('title') or row.get('songName') or '')
                    
                    if title:
                        key = normalize_title(title)
                        if key not in all_songs:
                            all_songs[key] = {
                                'title': title,
                                'sources': [],
                                'data': []
                            }
                        
                        all_songs[key]['sources'].append(csv_file.name)
                        all_songs[key]['data'].append(row)
        except Exception as e:
            print(f"  ? Error: {e}")
    
    print(f"\n? Total unique songs in CSVs: {len(all_songs)}\n")
    
    return all_songs

def analyze_audio_files(audio_files: list, max_files: int = None) -> list:
    """Deep analysis of audio files"""
    
    print("=" * 80)
    print("  ANALYZING AUDIO FILES")
    print("=" * 80 + "\n")
    
    if max_files:
        print(f"Analyzing first {max_files} files for speed...\n")
        audio_files = audio_files[:max_files]
    else:
        print(f"Analyzing all {len(audio_files)} files...\n")
    
    analyzed = []
    
    for i, audio_file in enumerate(audio_files):
        if (i + 1) % 50 == 0:
            print(f"  Processing {i + 1}/{len(audio_files)}...")
        
        metadata = extract_audio_metadata(audio_file)
        
        analyzed.append({
            'filepath': str(audio_file),
            'filename': audio_file.name,
            'stem': audio_file.stem,
            'extension': audio_file.suffix,
            'size': audio_file.stat().st_size,
            'hash': get_file_hash(audio_file),
            'metadata': metadata,
            'relative_path': str(audio_file.relative_to(audio_file.parents[2])),
        })
    
    print(f"\n? Analyzed {len(analyzed)} audio files\n")
    
    return analyzed

def load_master_csv(master_path: Path) -> dict:
    """Load master CSV for comparison"""
    
    print("=" * 80)
    print("  LOADING MASTER CSV")
    print("=" * 80 + "\n")
    
    master_songs = {}
    
    with open(master_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get('Title', '')
            if title:
                key = normalize_title(title)
                master_songs[key] = row
    
    print(f"? Loaded {len(master_songs)} songs from master CSV\n")
    
    return master_songs

def compare_datasets(suno_audio: list, suno_csvs: dict, master_csv: dict) -> dict:
    """Deep comparison of all datasets"""
    
    print("=" * 80)
    print("  COMPARING DATASETS")
    print("=" * 80 + "\n")
    
    comparison = {
        'in_all_three': [],          # In audio files, SUNO CSVs, and master CSV
        'in_audio_and_suno_csv': [], # In audio files and SUNO CSVs, not in master
        'in_audio_and_master': [],   # In audio files and master, not in SUNO CSVs
        'audio_only': [],            # Only in audio files
        'suno_csv_only': [],         # Only in SUNO CSVs
        'master_only': [],           # Only in master CSV
        'duplicates': [],            # Same audio file appears multiple times
    }
    
    # Index audio files by title/filename
    audio_by_title = defaultdict(list)
    for audio in suno_audio:
        # Try metadata title first
        title = audio['metadata'].get('title', '')
        if title:
            audio_by_title[normalize_title(title)].append(audio)
        
        # Also index by filename
        audio_by_title[normalize_title(audio['stem'])].append(audio)
    
    # Find duplicates
    for title, files in audio_by_title.items():
        if len(files) > 1:
            comparison['duplicates'].append({
                'title': title,
                'count': len(files),
                'files': files
            })
    
    # Compare audio files
    for title, files in audio_by_title.items():
        in_suno_csv = title in suno_csvs
        in_master = title in master_csv
        
        if in_suno_csv and in_master:
            comparison['in_all_three'].extend(files)
        elif in_suno_csv:
            comparison['in_audio_and_suno_csv'].extend(files)
        elif in_master:
            comparison['in_audio_and_master'].extend(files)
        else:
            comparison['audio_only'].extend(files)
    
    # Find SUNO CSV entries not in audio files
    for title in suno_csvs:
        if title not in audio_by_title:
            comparison['suno_csv_only'].append(suno_csvs[title])
    
    # Find master CSV entries not in audio files
    for title in master_csv:
        if title not in audio_by_title:
            comparison['master_only'].append(master_csv[title])
    
    print("Comparison Results:")
    print(f"  ? In all three (audio + SUNO CSV + master): {len(comparison['in_all_three'])}")
    print(f"  ?? In audio + SUNO CSV (not master): {len(comparison['in_audio_and_suno_csv'])}")
    print(f"  ?? In audio + master (not SUNO CSV): {len(comparison['in_audio_and_master'])}")
    print(f"  ?? Audio files only: {len(comparison['audio_only'])}")
    print(f"  ?? SUNO CSV only (no audio): {len(comparison['suno_csv_only'])}")
    print(f"  ?? Master CSV only (no audio): {len(comparison['master_only'])}")
    print(f"  ??  Duplicate audio files: {len(comparison['duplicates'])}")
    print()
    
    return comparison

def save_comprehensive_report(suno_audio: list, suno_csvs: dict, 
                              master_csv: dict, comparison: dict, output_path: Path):
    """Save comprehensive analysis report"""
    
    print("=" * 80)
    print("  SAVING COMPREHENSIVE REPORT")
    print("=" * 80 + "\n")
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Title', 'Filename', 'Filepath',
            'Duration', 'Size_MB', 'Hash',
            'In_SUNO_Audio', 'In_SUNO_CSV', 'In_Master_CSV',
            'Metadata_Title', 'Metadata_Artist', 'Metadata_Genre',
            'SUNO_CSV_Sources', 'Status', 'Recommendation'
        ])
        
        # Process all audio files
        for audio in suno_audio:
            title = audio['metadata'].get('title', '') or audio['stem']
            title_norm = normalize_title(title)
            
            in_suno_csv = 'YES' if title_norm in suno_csvs else 'NO'
            in_master = 'YES' if title_norm in master_csv else 'NO'
            
            suno_sources = ''
            if title_norm in suno_csvs:
                suno_sources = ', '.join(suno_csvs[title_norm]['sources'])
            
            # Determine status
            if in_suno_csv == 'YES' and in_master == 'YES':
                status = 'COMPLETE'
                recommendation = 'Verified in all sources'
            elif in_suno_csv == 'YES':
                status = 'NEED_MASTER_UPDATE'
                recommendation = 'Add to master CSV'
            elif in_master == 'YES':
                status = 'SUNO_VERIFIED'
                recommendation = 'Has master entry'
            else:
                status = 'UNVERIFIED'
                recommendation = 'Review - may be duplicate or misnamed'
            
            writer.writerow([
                title,
                audio['filename'],
                audio['relative_path'],
                f"{audio['metadata'].get('duration', 0):.1f}",
                f"{audio['size'] / 1024 / 1024:.2f}",
                audio['hash'][:8],
                'YES',
                in_suno_csv,
                in_master,
                audio['metadata'].get('title', ''),
                audio['metadata'].get('artist', ''),
                audio['metadata'].get('genre', ''),
                suno_sources,
                status,
                recommendation
            ])
    
    print(f"? Saved to: {output_path}\n")

def main():
    print("\n" + "??" * 40)
    print("  DEEP SUNO CONTENT-AWARE ANALYSIS")
    print("  Comparing SUNO directory with master CSV")
    print("??" * 40)
    
    home = Path.home()
    suno_path = home / 'Music/nocTurneMeLoDieS/SUNO'
    master_path = home / 'Music/MASTER_COMPLETE_ALL_FIELDS.csv'
    
    if not suno_path.exists():
        print(f"\n? SUNO directory not found: {suno_path}")
        return
    
    # Step 1: Scan SUNO directory
    suno_scan = scan_suno_directory(suno_path)
    
    # Step 2: Load SUNO CSVs
    suno_csvs = load_suno_csvs(suno_scan['csv_files'])
    
    # Step 3: Analyze audio files (limit to 500 for speed, or None for all)
    suno_audio = analyze_audio_files(suno_scan['audio_files'], max_files=500)
    
    # Step 4: Load master CSV
    master_csv = load_master_csv(master_path)
    
    # Step 5: Compare everything
    comparison = compare_datasets(suno_audio, suno_csvs, master_csv)
    
    # Step 6: Save comprehensive report
    output = home / 'Music/SUNO_DEEP_ANALYSIS.csv'
    save_comprehensive_report(suno_audio, suno_csvs, master_csv, comparison, output)
    
    # Summary
    print("=" * 80)
    print("  ? DEEP ANALYSIS COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"?? SUNO Directory:")
    print(f"  Audio files: {len(suno_scan['audio_files'])}")
    print(f"  CSV files: {len(suno_scan['csv_files'])}")
    print(f"  Unique songs in CSVs: {len(suno_csvs)}")
    print()
    
    print(f"?? Comparison:")
    print(f"  ? Complete (in all sources): {len(comparison['in_all_three'])}")
    print(f"  ??  Duplicates found: {len(comparison['duplicates'])}")
    print(f"  ?? Need to add to master: {len(comparison['in_audio_and_suno_csv'])}")
    print(f"  ?? In master but not SUNO: {len(comparison['master_only'])}")
    print()
    
    print(f"?? Report saved: {output}")
    print(f"\nFilter by 'Status' column:")
    print(f"  COMPLETE ? Verified everywhere")
    print(f"  NEED_MASTER_UPDATE ? In SUNO, add to master")
    print(f"  SUNO_VERIFIED ? Has master entry")
    print(f"  UNVERIFIED ? Review for duplicates/issues")
    print(f"\nOpen: open '{output}'")

if __name__ == '__main__':
    main()
