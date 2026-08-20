#!/usr/bin/env python3
"""
Download missing songs from Suno
Uses Song URLs from the master CSV
"""

import csv
from pathlib import Path
import subprocess
import json
import time
from urllib.parse import urlparse

def load_env_config():
    """Load Suno credentials from ~/.env.d/"""
    home = Path.home()
    env_dir = home / '.env.d'
    
    config = {}
    
    if not env_dir.exists():
        return config
    
    # Look for Suno-related config files
    for env_file in env_dir.glob('*'):
        if 'suno' in env_file.name.lower():
            try:
                if env_file.suffix == '.json':
                    with open(env_file, 'r') as f:
                        data = json.load(f)
                        config.update(data)
                elif env_file.suffix in ['.env', '.txt', '']:
                    with open(env_file, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if '=' in line and not line.startswith('#'):
                                key, value = line.split('=', 1)
                                config[key.strip()] = value.strip()
            except Exception:
                pass
    
    return config

def download_with_curl(url: str, output_path: Path, cookie: str = None) -> bool:
    """Download file using curl"""
    
    cmd = ['curl', '-L', '-o', str(output_path), url]
    
    # Add cookie if available
    if cookie:
        cmd.extend(['-H', f'Cookie: {cookie}'])
    
    # Add user agent
    cmd.extend(['-A', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Check if file was created and has content
        if output_path.exists() and output_path.stat().st_size > 1000:
            return True
        else:
            # Clean up failed download
            if output_path.exists():
                output_path.unlink()
            return False
    except Exception as e:
        # Clean up failed download
        if output_path.exists():
            output_path.unlink()
        return False

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for filesystem"""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > 200:
        filename = filename[:200]
    
    return filename

def main():
    print("\n" + "??" * 40)
    print("  DOWNLOAD MISSING SONGS FROM SUNO")
    print("??" * 40 + "\n")
    
    home = Path.home()
    ultimate_csv = home / 'Music/ULTIMATE_MASTER_REPORT.csv'
    download_dir = home / 'Music/nocTurneMeLoDieS/FINAL_ORGANIZED/YOUR_SUNO_SONGS/DOWNLOADED'
    
    # Create download directory
    download_dir.mkdir(parents=True, exist_ok=True)
    
    # Load config
    print("Loading Suno credentials...")
    config = load_env_config()
    
    suno_cookie = config.get('SUNO_COOKIE') or config.get('suno_cookie') or config.get('cookie')
    
    if suno_cookie:
        print("? Found Suno cookie\n")
    else:
        print("??  No Suno cookie found in ~/.env.d/\n")
        print("  Downloads may fail for private/authenticated content\n")
    
    # Load songs that need downloading
    print("Loading songs that need downloading...\n")
    
    need_download = []
    
    with open(ultimate_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Overall_Status') == 'NEED_DOWNLOAD':
                song_url = row.get('Song_URL', '').strip()
                if song_url and song_url.startswith('http'):
                    need_download.append(row)
    
    print(f"Found {len(need_download)} songs with download URLs\n")
    
    if len(need_download) == 0:
        print("No songs to download!")
        return
    
    # Show sample
    print("Sample of songs to download:")
    for i, song in enumerate(need_download[:10]):
        print(f"  {i+1}. {song.get('Title', 'Unknown')} - {song.get('Artist', 'Unknown')}")
    
    if len(need_download) > 10:
        print(f"  ... and {len(need_download) - 10} more\n")
    else:
        print()
    
    # Ask for confirmation
    print("=" * 80)
    print("  DOWNLOAD PLAN")
    print("=" * 80 + "\n")
    
    print(f"Will attempt to download {len(need_download)} songs")
    print(f"Download directory: {download_dir}\n")
    
    # Limit to reasonable batch for testing
    max_downloads = 50
    if len(need_download) > max_downloads:
        print(f"??  Limiting to first {max_downloads} songs for safety\n")
        need_download = need_download[:max_downloads]
    
    print(f"Attempting to download {len(need_download)} songs...\n")
    
    # Download
    results = {
        'success': [],
        'failed': [],
        'skipped': []
    }
    
    for i, song in enumerate(need_download):
        title = song.get('Title', 'Unknown')
        artist = song.get('Artist', 'Unknown')
        song_url = song.get('Song_URL', '')
        
        print(f"[{i+1}/{len(need_download)}] {title} - {artist}")
        
        # Parse URL to determine file extension
        parsed_url = urlparse(song_url)
        
        # Suno URLs typically point to the song page, not direct MP3
        # We need to extract the actual audio URL
        if 'suno.com/song/' in song_url:
            # This is a Suno song page URL, not a direct download
            # We'd need to scrape the page or use the API
            print(f"  ??  Suno song page URL - need API/scraping")
            results['skipped'].append({
                'title': title,
                'url': song_url,
                'reason': 'Need Suno API or scraping'
            })
            continue
        
        # Try to download if it's a direct URL
        filename = sanitize_filename(f"{artist} - {title}.mp3")
        output_path = download_dir / filename
        
        # Skip if already exists
        if output_path.exists():
            print(f"  ? Already exists")
            results['success'].append({
                'title': title,
                'path': str(output_path)
            })
            continue
        
        # Attempt download
        print(f"  Downloading...")
        
        if download_with_curl(song_url, output_path, suno_cookie):
            print(f"  ? Success")
            results['success'].append({
                'title': title,
                'path': str(output_path)
            })
        else:
            print(f"  ? Failed")
            results['failed'].append({
                'title': title,
                'url': song_url,
                'reason': 'Download failed'
            })
        
        # Rate limiting
        time.sleep(1)
    
    # Save results
    print("\n" + "=" * 80)
    print("  DOWNLOAD RESULTS")
    print("=" * 80 + "\n")
    
    print(f"? Successful: {len(results['success'])}")
    print(f"? Failed: {len(results['failed'])}")
    print(f"??  Skipped: {len(results['skipped'])}")
    print()
    
    # Save detailed report
    report_path = home / 'Music/DOWNLOAD_REPORT.csv'
    
    with open(report_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Status', 'Details'])
        
        for item in results['success']:
            writer.writerow([item['title'], 'SUCCESS', item['path']])
        
        for item in results['failed']:
            writer.writerow([item['title'], 'FAILED', f"{item['reason']}: {item['url']}"])
        
        for item in results['skipped']:
            writer.writerow([item['title'], 'SKIPPED', f"{item['reason']}: {item['url']}"])
    
    print(f"? Report saved to: {report_path}\n")
    
    # Next steps
    print("=" * 80)
    print("  NEXT STEPS")
    print("=" * 80 + "\n")
    
    if results['skipped']:
        print(f"??  {len(results['skipped'])} songs need Suno API/scraping")
        print("   Most Song URLs point to Suno song pages, not direct MP3 files")
        print("   Need to:")
        print("     1. Use Suno API to get direct download URLs")
        print("     2. Or scrape the page to extract audio URLs")
        print()
    
    if results['success']:
        print(f"? {len(results['success'])} songs downloaded to:")
        print(f"  {download_dir}")
        print()
    
    print(f"Full report: open '{report_path}'")

if __name__ == '__main__':
    main()
