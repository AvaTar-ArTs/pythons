#!/usr/bin/env python3
"""
Deep Multi-Level Scan
Search ~/Music and ~/ at any depth for ALL content that could help
"""

import csv
from pathlib import Path
from collections import defaultdict
import hashlib

def get_file_hash(filepath: Path) -> str:
    """Get quick hash of file"""
    try:
        md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            # Just hash first 8KB for speed
            md5.update(f.read(8192))
        return md5.hexdigest()[:8]
    except Exception:
        return ""

def deep_scan_directory(base_path: Path, max_depth: int = None) -> dict:
    """Deep scan directory for all content types"""
    
    print(f"\nScanning: {base_path}")
    if max_depth:
        print(f"Max depth: {max_depth} levels")
    else:
        print("Max depth: unlimited")
    
    results = {
        'audio': [],
        'lyrics': [],
        'prompts': [],
        'images': [],
        'videos': [],
        'documents': [],
        'json': [],
        'csv': [],
        'archives': [],
        'other': []
    }
    
    # Skip these directories (system/cache)
    skip_dirs = {
        '.Trash', 'Library', 'Applications', 'System', '.cache', 
        'node_modules', '__pycache__', '.git', '.lh',
        'Cache', 'Caches', 'cache', 'caches'
    }
    
    def scan_recursive(path: Path, depth: int = 0):
        if max_depth and depth > max_depth:
            return
        
        try:
            for item in path.iterdir():
                # Skip hidden and system
                if item.name.startswith('.') and item.name not in ['.env.d']:
                    continue
                
                if item.is_dir():
                    # Skip certain directories
                    if item.name in skip_dirs:
                        continue
                    scan_recursive(item, depth + 1)
                    
                elif item.is_file():
                    ext = item.suffix.lower()
                    size = item.stat().st_size
                    
                    # Categorize by extension
                    if ext in ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac']:
                        results['audio'].append({
                            'path': str(item),
                            'name': item.name,
                            'size': size,
                            'depth': depth,
                            'hash': get_file_hash(item)
                        })
                    
                    elif ext in ['.txt', '.lrc', '.srt', '.vtt'] or 'lyric' in item.name.lower():
                        results['lyrics'].append({
                            'path': str(item),
                            'name': item.name,
                            'size': size,
                            'depth': depth
                        })
                    
                    elif 'prompt' in item.name.lower() or 'dalle' in item.name.lower() or 'sora' in item.name.lower() or 'gpt' in item.name.lower():
                        results['prompts'].append({
                            'path': str(item),
                            'name': item.name,
                            'size': size,
                            'depth': depth
                        })
                    
                    elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']:
                        results['images'].append({
                            'path': str(item),
                            'name': item.name,
                            'size': size,
                            'depth': depth
                        })
                    
                    elif ext in ['.mp4', '.mov', '.avi', '.mkv', '.webm']:
                        results['videos'].append({
                            'path': str(item),
                            'name': item.name,
                            'size': size,
                            'depth': depth
                        })
                    
                    elif ext in ['.md', '.html', '.pdf', '.doc', '.docx']:
                        results['documents'].append({
                            'path': str(item),
                            'name': item.name,
                            'size': size,
                            'depth': depth
                        })
                    
                    elif ext == '.json':
                        results['json'].append({
                            'path': str(item),
                            'name': item.name,
                            'size': size,
                            'depth': depth
                        })
                    
                    elif ext == '.csv':
                        results['csv'].append({
                            'path': str(item),
                            'name': item.name,
                            'size': size,
                            'depth': depth
                        })
                    
                    elif ext in ['.zip', '.tar', '.gz', '.7z', '.rar']:
                        results['archives'].append({
                            'path': str(item),
                            'name': item.name,
                            'size': size,
                            'depth': depth
                        })
                    
        except (PermissionError, OSError):
            pass
    
    scan_recursive(base_path)
    
    return results

def main():
    print("\n" + "??" * 40)
    print("  DEEP MULTI-LEVEL CONTENT SCAN")
    print("  Finding ALL content at any depth")
    print("??" * 40)
    
    home = Path.home()
    
    # Scan locations
    scans = []
    
    print("\n" + "=" * 80)
    print("  DEEP SCANNING")
    print("=" * 80)
    
    # Deep scan ~/Music (unlimited depth)
    print("\n1. Scanning ~/Music (unlimited depth)...")
    music_results = deep_scan_directory(home / 'Music', max_depth=None)
    scans.append(('Music', music_results))
    
    # Deep scan ~/Documents (unlimited depth)
    print("\n2. Scanning ~/Documents (unlimited depth)...")
    docs_results = deep_scan_directory(home / 'Documents', max_depth=None)
    scans.append(('Documents', docs_results))
    
    # Deep scan ~/Downloads (max 5 levels)
    print("\n3. Scanning ~/Downloads (max 5 levels)...")
    downloads_results = deep_scan_directory(home / 'Downloads', max_depth=5)
    scans.append(('Downloads', downloads_results))
    
    # Scan specific directories in home
    print("\n4. Scanning ~/Desktop (max 3 levels)...")
    if (home / 'Desktop').exists():
        desktop_results = deep_scan_directory(home / 'Desktop', max_depth=3)
        scans.append(('Desktop', desktop_results))
    
    print("\n5. Scanning ~/Movies (max 3 levels)...")
    if (home / 'Movies').exists():
        movies_results = deep_scan_directory(home / 'Movies', max_depth=3)
        scans.append(('Movies', movies_results))
    
    # Aggregate all results
    print("\n" + "=" * 80)
    print("  AGGREGATING RESULTS")
    print("=" * 80 + "\n")
    
    totals = defaultdict(int)
    all_results = defaultdict(list)
    
    for location, results in scans:
        print(f"{location}:")
        for category, items in results.items():
            count = len(items)
            totals[category] += count
            all_results[category].extend(items)
            if count > 0:
                print(f"  {category}: {count}")
        print()
    
    # Find duplicates
    print("=" * 80)
    print("  FINDING DUPLICATES")
    print("=" * 80 + "\n")
    
    audio_by_hash = defaultdict(list)
    for audio in all_results['audio']:
        if audio['hash']:
            audio_by_hash[audio['hash']].append(audio)
    
    duplicates = {h: files for h, files in audio_by_hash.items() if len(files) > 1}
    
    print(f"Found {len(duplicates)} duplicate audio files (by hash)\n")
    
    # Save comprehensive report
    print("=" * 80)
    print("  SAVING COMPREHENSIVE REPORTS")
    print("=" * 80 + "\n")
    
    output_dir = home / 'Music'
    
    # 1. Audio files report
    audio_output = output_dir / 'DEEP_SCAN_AUDIO.csv'
    with open(audio_output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Filename', 'Path', 'Size_MB', 'Depth', 'Hash', 'Location'])
        
        for audio in sorted(all_results['audio'], key=lambda x: x['depth']):
            location = 'Music' if '/Music/' in audio['path'] else \
                      'Documents' if '/Documents/' in audio['path'] else \
                      'Downloads' if '/Downloads/' in audio['path'] else 'Other'
            
            writer.writerow([
                audio['name'],
                audio['path'],
                f"{audio['size'] / 1024 / 1024:.2f}",
                audio['depth'],
                audio['hash'],
                location
            ])
    
    print(f"? Audio files: {audio_output}")
    
    # 2. Lyrics files report
    lyrics_output = output_dir / 'DEEP_SCAN_LYRICS.csv'
    with open(lyrics_output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Filename', 'Path', 'Size_KB', 'Depth', 'Location'])
        
        for lyrics in sorted(all_results['lyrics'], key=lambda x: x['size'], reverse=True):
            location = 'Music' if '/Music/' in lyrics['path'] else \
                      'Documents' if '/Documents/' in lyrics['path'] else 'Other'
            
            writer.writerow([
                lyrics['name'],
                lyrics['path'],
                f"{lyrics['size'] / 1024:.2f}",
                lyrics['depth'],
                location
            ])
    
    print(f"? Lyrics files: {lyrics_output}")
    
    # 3. Prompts files report
    prompts_output = output_dir / 'DEEP_SCAN_PROMPTS.csv'
    with open(prompts_output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Filename', 'Path', 'Size_KB', 'Depth', 'Location'])
        
        for prompt in sorted(all_results['prompts'], key=lambda x: x['name']):
            location = 'Music' if '/Music/' in prompt['path'] else \
                      'Documents' if '/Documents/' in prompt['path'] else 'Other'
            
            writer.writerow([
                prompt['name'],
                prompt['path'],
                f"{prompt['size'] / 1024:.2f}",
                prompt['depth'],
                location
            ])
    
    print(f"? Prompt files: {prompts_output}")
    
    # 4. Images report
    images_output = output_dir / 'DEEP_SCAN_IMAGES.csv'
    with open(images_output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Filename', 'Path', 'Size_KB', 'Depth', 'Location'])
        
        for img in sorted(all_results['images'], key=lambda x: x['size'], reverse=True)[:1000]:  # Top 1000
            location = 'Music' if '/Music/' in img['path'] else \
                      'Documents' if '/Documents/' in img['path'] else \
                      'Downloads' if '/Downloads/' in img['path'] else 'Other'
            
            writer.writerow([
                img['name'],
                img['path'],
                f"{img['size'] / 1024:.2f}",
                img['depth'],
                location
            ])
    
    print(f"? Images (top 1000): {images_output}")
    
    # 5. Duplicates report
    if duplicates:
        dup_output = output_dir / 'DEEP_SCAN_DUPLICATES.csv'
        with open(dup_output, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Hash', 'Count', 'Filename', 'Paths'])
            
            for hash_val, files in sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True):
                paths = ' | '.join([f['path'] for f in files])
                writer.writerow([
                    hash_val,
                    len(files),
                    files[0]['name'],
                    paths
                ])
        
        print(f"? Duplicates: {dup_output}")
    
    # 6. Summary report
    summary_output = output_dir / 'DEEP_SCAN_SUMMARY.csv'
    with open(summary_output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Category', 'Count', 'Total_Size_MB'])
        
        for category, items in sorted(all_results.items(), key=lambda x: len(x[1]), reverse=True):
            total_size = sum(item['size'] for item in items) / 1024 / 1024
            writer.writerow([
                category,
                len(items),
                f"{total_size:.2f}"
            ])
    
    print(f"? Summary: {summary_output}")
    
    # Statistics
    print("\n" + "=" * 80)
    print("  ?? DEEP SCAN STATISTICS")
    print("=" * 80 + "\n")
    
    print("Total files found:")
    for category, count in sorted(totals.items(), key=lambda x: -x[1]):
        if count > 0:
            total_size = sum(item['size'] for item in all_results[category]) / 1024 / 1024
            print(f"  {category:12} {count:6} files  ({total_size:8.2f} MB)")
    
    print()
    print(f"Total files scanned: {sum(totals.values())}")
    print(f"Duplicate audio files: {len(duplicates)}")
    print()
    
    # Show depth distribution for audio
    depth_dist = defaultdict(int)
    for audio in all_results['audio']:
        depth_dist[audio['depth']] += 1
    
    print("Audio files by depth:")
    for depth in sorted(depth_dist.keys()):
        print(f"  Level {depth}: {depth_dist[depth]} files")
    
    print()
    print("=" * 80)
    print("  ? DEEP SCAN COMPLETE")
    print("=" * 80 + "\n")
    
    print("Reports created:")
    print(f"  1. {audio_output}")
    print(f"  2. {lyrics_output}")
    print(f"  3. {prompts_output}")
    print(f"  4. {images_output}")
    if duplicates:
        print(f"  5. {dup_output}")
    print(f"  6. {summary_output}")
    print()
    
    print("Next steps:")
    print("  ? Review DEEP_SCAN_AUDIO.csv for all audio files")
    print("  ? Review DEEP_SCAN_LYRICS.csv for lyrics to match")
    print("  ? Review DEEP_SCAN_PROMPTS.csv for creation info")
    print("  ? Review DEEP_SCAN_DUPLICATES.csv to remove duplicates")
    print()
    
    print(f"Open: open '{output_dir}'")

if __name__ == '__main__':
    main()
