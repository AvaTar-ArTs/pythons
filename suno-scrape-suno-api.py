#!/usr/bin/env python3
"""
?? SUNO AI SCRAPER - Complete CSV Exporter
==========================================
Scrapes Suno AI playlists and outputs to CSV

Usage:
    python suno_scraper_complete.py --url "https://suno.com/playlist/ID"
    python suno_scraper_complete.py --urls file_with_urls.txt
    python suno_scraper_complete.py --trending  # Scrape trending songs
"""

import argparse
import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urljoin

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("? Missing dependencies! Install with:")
    print("   pip install requests beautifulsoup4")
    sys.exit(1)


class SunoScraper:
    """Scrapes Suno AI playlists and songs"""
    
    BASE_URL = "https://suno.com"
    
    def __init__(self, max_songs: int = 100):
        self.max_songs = max_songs
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
    def scrape_playlist(self, playlist_url: str) -> List[Dict]:
        """Scrape a Suno playlist"""
        print(f"?? Scraping: {playlist_url}")
        
        try:
            response = self.session.get(playlist_url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"? Failed to fetch playlist: {e}")
            return []
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to extract data from script tags (Suno uses Next.js)
        songs = self._extract_from_nextjs(soup, playlist_url)
        
        if not songs:
            # Fallback: try parsing HTML directly
            songs = self._extract_from_html(soup, playlist_url)
        
        print(f"? Found {len(songs)} songs")
        return songs[:self.max_songs]
    
    def _extract_from_nextjs(self, soup: BeautifulSoup, playlist_url: str) -> List[Dict]:
        """Extract data from Next.js __NEXT_DATA__ script"""
        songs = []
        
        # Find Next.js data script
        script_tag = soup.find('script', id='__NEXT_DATA__')
        if not script_tag:
            return []
        
        try:
            data = json.loads(script_tag.string)
            
            # Navigate through Next.js data structure
            props = data.get('props', {}).get('pageProps', {})
            
            # Try different data paths
            clips_data = (
                props.get('clips') or 
                props.get('playlist', {}).get('clips') or
                props.get('songs') or
                []
            )
            
            for clip in clips_data:
                song = self._parse_song_data(clip, playlist_url)
                if song:
                    songs.append(song)
                    
        except (json.JSONDecodeError, KeyError) as e:
            print(f"??  Could not parse Next.js data: {e}")
        
        return songs
    
    def _extract_from_html(self, soup: BeautifulSoup, playlist_url: str) -> List[Dict]:
        """Fallback: Extract from HTML structure"""
        songs = []
        
        # Look for song links
        song_links = soup.find_all('a', href=re.compile(r'/song/[a-f0-9-]{36}'))
        
        for link in song_links[:self.max_songs]:
            song_url = urljoin(self.BASE_URL, link.get('href'))
            song_id = self._extract_song_id(song_url)
            
            if not song_id:
                continue
            
            # Try to extract song details
            parent = link.find_parent()
            title = link.get_text(strip=True) or link.get('title', '')
            
            song = {
                'songName': title,
                'songLink': song_url,
                'songId': song_id,
                'audioUrl': f"https://cdn1.suno.ai/{song_id}.mp3",
                'shareUrl': f"https://suno.com/s/{song_id.split('-')[0]}",
                'playlist': playlist_url,
                'scrapedAt': datetime.now().isoformat(),
            }
            
            songs.append(song)
        
        return songs
    
    def _parse_song_data(self, clip: Dict, playlist_url: str) -> Optional[Dict]:
        """Parse song data from API response"""
        try:
            song_id = clip.get('id', '')
            
            return {
                'songId': song_id,
                'songName': clip.get('title', ''),
                'songLink': f"{self.BASE_URL}/song/{song_id}",
                'shareUrl': f"{self.BASE_URL}/s/{song_id.split('-')[0] if song_id else ''}",
                'audioUrl': clip.get('audio_url') or f"https://cdn1.suno.ai/{song_id}.mp3",
                'imageUrl': clip.get('image_url') or clip.get('image_large_url', ''),
                'videoUrl': clip.get('video_url', ''),
                'length': self._format_duration(clip.get('duration', 0)),
                'author': clip.get('display_name', ''),
                'authorLink': f"{self.BASE_URL}/@{clip.get('handle', '')}" if clip.get('handle') else '',
                'published': clip.get('created_at', ''),
                'plays': clip.get('play_count', 0),
                'likes': clip.get('upvote_count', 0),
                'style': ', '.join(clip.get('metadata', {}).get('tags', [])),
                'lyrics': clip.get('metadata', {}).get('prompt', ''),
                'isPublic': clip.get('is_public', False),
                'modelVersion': clip.get('model_name', ''),
                'playlist': playlist_url,
                'scrapedAt': datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"??  Error parsing song: {e}")
            return None
    
    def _extract_song_id(self, url: str) -> Optional[str]:
        """Extract song ID from URL"""
        match = re.search(r'/song/([a-f0-9-]{36})', url)
        return match.group(1) if match else None
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in MM:SS"""
        if not seconds:
            return ''
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"


def save_to_csv(songs: List[Dict], output_file: str) -> None:
    """Save songs to CSV file"""
    if not songs:
        print("? No songs to save!")
        return
    
    # Get all unique keys
    fieldnames = set()
    for song in songs:
        fieldnames.update(song.keys())
    
    fieldnames = sorted(fieldnames)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(songs)
    
    print(f"\n? Saved {len(songs)} songs to: {output_file}")
    print(f"?? File size: {Path(output_file).stat().st_size / 1024:.1f} KB")


def save_to_json(songs: List[Dict], output_file: str) -> None:
    """Save songs to JSON file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(songs, f, indent=2, ensure_ascii=False)
    
    print(f"? Saved JSON to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='?? Suno AI Scraper - Export playlists to CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --url "https://suno.com/playlist/07653cdf-8f72-430e-847f-9ab8ac05af40"
  %(prog)s --url "https://suno.com/playlist/ID" --max-songs 50
  %(prog)s --urls playlists.txt --output my_songs.csv
  %(prog)s --trending --max-songs 100
        """
    )
    
    parser.add_argument('--url', help='Single playlist URL to scrape')
    parser.add_argument('--urls', help='File with playlist URLs (one per line)')
    parser.add_argument('--trending', action='store_true', help='Scrape trending songs')
    parser.add_argument('--max-songs', type=int, default=100, help='Max songs per playlist (default: 100)')
    parser.add_argument('--output', '-o', help='Output CSV file (default: auto-generated)')
    parser.add_argument('--json', action='store_true', help='Also save as JSON')
    
    args = parser.parse_args()
    
    # Validate input
    if not (args.url or args.urls or args.trending):
        parser.print_help()
        print("\n? Error: Provide --url, --urls, or --trending")
        sys.exit(1)
    
    # Initialize scraper
    scraper = SunoScraper(max_songs=args.max_songs)
    all_songs = []
    
    # Scrape URLs
    urls = []
    
    if args.url:
        urls.append(args.url)
    
    if args.urls:
        try:
            with open(args.urls) as f:
                urls.extend(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            print(f"? File not found: {args.urls}")
            sys.exit(1)
    
    if args.trending:
        urls.append("https://suno.com/")
    
    # Scrape each URL
    print(f"\n?? Scraping {len(urls)} playlist(s)...\n")
    
    for url in urls:
        songs = scraper.scrape_playlist(url)
        all_songs.extend(songs)
    
    if not all_songs:
        print("\n? No songs found!")
        sys.exit(1)
    
    # Generate output filename
    if not args.output:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        args.output = f"suno_songs_{timestamp}.csv"
    
    # Save to CSV
    save_to_csv(all_songs, args.output)
    
    # Save to JSON if requested
    if args.json:
        json_file = args.output.replace('.csv', '.json')
        save_to_json(all_songs, json_file)
    
    # Print summary
    print(f"\n{'='*70}")
    print(f"?? SCRAPING COMPLETE!")
    print(f"{'='*70}")
    print(f"   ?? Total songs: {len(all_songs)}")
    print(f"   ?? CSV file: {args.output}")
    if args.json:
        print(f"   ?? JSON file: {json_file}")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
