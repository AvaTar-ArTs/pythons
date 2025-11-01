
# Constants
CONSTANT_100 = 100
CONSTANT_124 = 124
CONSTANT_537 = 537
CONSTANT_666 = 666
CONSTANT_4472 = 4472

#!/usr/bin/env python3
"""
Merged Content Analysis Tool

This file was automatically merged from the following source files:
- /Users/steven/Music/nocTurneMeLoDieS/python/FINAL_ORGANIZED/generation/advanced_web_scraper.py
- /Users/steven/Music/nocTurneMeLoDieS/python/CLEAN_ORGANIZED/generation/advanced_web_scraper.py

Combines the best features and functionality from multiple similar files.
"""

# Imports from all source files
from bs4 import BeautifulSoup
from pathlib import Path
from typing import Dict, List, Optional, Union
from urllib.parse import urljoin, urlparse
import argparse
import csv
import json
import logging
import os
import pandas as pd
import re
import requests
import sys

# Documentation from source files
        """Scrape song information from Suno HTML file."""
        """Extract song information from URL."""
        """Scrape data using regex patterns."""
"""
        """Generate HTML image gallery."""
        """Generate Markdown image gallery."""
        """Batch scrape songs from multiple HTML files."""
        html_template += """
                seo_text = f"""
        """Generate image gallery from URLs."""
        html_template = """
            html_template += f"""
        """Generate SEO-optimized content from song data."""
    """Comprehensive web scraping tool with multiple scraping modes."""
    """Main function for command-line usage."""

Advanced Web Scraper - Consolidated Web Scraping Script

This script consolidates all web scraping functionality from multiple scraping scripts
into a comprehensive, feature-rich web scraping tool.
"""

import os
import sys
import logging
import argparse
import re
import csv
import json
from pathlib import Path
from typing import Dict, List, Optional, Union
import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("web_scraping.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AdvancedWebScraper:
    """Comprehensive web scraping tool with multiple scraping modes."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/CONSTANT_537.36 (KHTML, like Gecko) Chrome/91.0.CONSTANT_4472.CONSTANT_124 Safari/CONSTANT_537.36'
        })
    
    def scrape_suno_songs(self, html_file: Path) -> List[Dict]:
        """Scrape song information from Suno HTML file."""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            songs = []
            
            # Multiple patterns to try for different HTML structures
            patterns = [
                {'div_class': 'css-79jxux', 'title_class': 'text-primary', 'time_class': 'text-mono'},
                {'div_class': 'song-item', 'title_class': 'song-title', 'time_class': 'duration'},
                {'div_class': 'track', 'title_class': 'name', 'time_class': 'length'}
            ]
            
            for pattern in patterns:
                items = soup.find_all('div', class_=pattern['div_class'])
                if items:
                    for item in items:
                        title_element = item.find('span', class_=pattern['title_class'])
                        song_url_element = item.find('a', href=True)
                        cover_url_element = item.find_previous_sibling('img', src=True)
                        genre_element = item.find('a', class_='hover:underline', href=True)
                        time_element = item.find('span', class_=pattern['time_class'])
                        
                        song_data = {
                            'title': title_element.get('title', '') if title_element else '',
                            'url': song_url_element.get('href', '') if song_url_element else '',
                            'cover_url': cover_url_element.get('src', '') if cover_url_element else '',
                            'genre': genre_element.text.strip() if genre_element else '',
                            'duration': time_element.text.strip() if time_element else '',
                            'lyrics': '',
                            'info': '',
                            'keys': ''
                        }
                        songs.append(song_data)
                    break
            
            logger.info(f"Scraped {len(songs)} songs from {html_file.name}")
            return songs
            
        except Exception as e:
            logger.error(f"Error scraping Suno songs from {html_file}: {e}")
            return []
    
    def scrape_with_regex(self, html_file: Path, pattern: str) -> List[Dict]:
        """Scrape data using regex patterns."""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            matches = re.findall(pattern, html_content)
            results = []
            
            for match in matches:
                if isinstance(match, tuple):
                    result = {}
                    for i, field in enumerate(['src', 'title', 'song_href', 'style_href', 'style']):
                        if i < len(match):
                            result[field] = match[i]
                    results.append(result)
                else:
                    results.append({'match': match})
            
            logger.info(f"Found {len(results)} matches with regex")
            return results
            
        except Exception as e:
            logger.error(f"Error with regex scraping: {e}")
            return []
    
    def generate_image_gallery(self, image_urls: List[str], output_file: Path, 
                              gallery_type: str = "html") -> bool:
        """Generate image gallery from URLs."""
        try:
            if gallery_type == "html":
                html_content = self._generate_html_gallery(image_urls)
            elif gallery_type == "markdown":
                html_content = self._generate_markdown_gallery(image_urls)
            else:
                logger.error(f"Unsupported gallery type: {gallery_type}")
                return False
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Generated {gallery_type} gallery: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating image gallery: {e}")
            return False
    
    def _generate_html_gallery(self, image_urls: List[str]) -> str:
        """Generate HTML image gallery."""
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Gallery</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .gallery-item { text-align: center; }
        .gallery-item img { max-width: CONSTANT_100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .gallery-item p { margin-top: 10px; color: #CONSTANT_666; }
    </style>
</head>
<body>
    <h1>Image Gallery</h1>
    <div class="gallery">
"""
        
        for i, url in enumerate(image_urls):
            html_template += f"""
        <div class="gallery-item">
            <img src="{url}" alt="Image {i+1}" loading="lazy">
            <p>Image {i+1}</p>
        </div>
"""
        
        html_template += """
    </div>
</body>
</html>
"""
        return html_template
    
    def _generate_markdown_gallery(self, image_urls: List[str]) -> str:
        """Generate Markdown image gallery."""
        markdown = "# Image Gallery\n\n"
        
        for i, url in enumerate(image_urls):
            markdown += f"![Image {i+1}]({url})\n\n"
        
        return markdown
    
    def extract_song_info(self, url: str) -> Dict:
        """Extract song information from URL."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic information
            title = soup.find('title')
            title_text = title.text.strip() if title else 'Unknown'
            
            # Look for meta tags
            description = soup.find('meta', attrs={'name': 'description'})
            description_text = description.get('content', '') if description else ''
            
            # Look for Open Graph tags
            og_title = soup.find('meta', property='og:title')
            og_description = soup.find('meta', property='og:description')
            og_image = soup.find('meta', property='og:image')
            
            return {
                'url': url,
                'title': title_text,
                'description': description_text,
                'og_title': og_title.get('content', '') if og_title else '',
                'og_description': og_description.get('content', '') if og_description else '',
                'og_image': og_image.get('content', '') if og_image else ''
            }
            
        except Exception as e:
            logger.error(f"Error extracting song info from {url}: {e}")
            return {'url': url, 'error': str(e)}
    
    def batch_scrape_songs(self, html_files: List[Path], output_file: Path) -> bool:
        """Batch scrape songs from multiple HTML files."""
        try:
            all_songs = []
            
            for html_file in html_files:
                songs = self.scrape_suno_songs(html_file)
                all_songs.extend(songs)
            
            # Save to CSV
            df = pd.DataFrame(all_songs)
            df.to_csv(output_file, index=False)
            
            logger.info(f"Scraped {len(all_songs)} songs total, saved to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error in batch scraping: {e}")
            return False
    
    def generate_seo_content(self, song_data: List[Dict], output_file: Path) -> bool:
        """Generate SEO-optimized content from song data."""
        try:
            seo_content = []
            
            for song in song_data:
                title = song.get('title', 'Unknown Song')
                genre = song.get('genre', 'Unknown Genre')
                duration = song.get('duration', 'Unknown Duration')
                
                # Generate SEO-friendly content
                seo_text = f"""
# {title}

**Genre:** {genre}  
**Duration:** {duration}

## About This Song

{title} is a {genre.lower()} track with a duration of {duration}. This song showcases the artist's unique style and musical creativity.

## Key Features

- **Genre:** {genre}
- **Duration:** {duration}
- **Style:** Contemporary {genre.lower()}

## Listen Now

[Play {title}]({song.get('url', '#')})

---
"""
                seo_content.append(seo_text)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\\n'.join(seo_content))
            
            logger.info(f"Generated SEO content for {len(song_data)} songs: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating SEO content: {e}")
            return False

def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Advanced Web Scraper")
    parser.add_argument("--mode", choices=["suno", "regex", "gallery", "song-info", "batch", "seo"], 
                       required=True, help="Scraping mode")
    parser.add_argument("--input", help="Input file or directory")
    parser.add_argument("--output", help="Output file")
    parser.add_argument("--pattern", help="Regex pattern for regex mode")
    parser.add_argument("--urls", nargs="+", help="URLs for gallery or song-info mode")
    parser.add_argument("--gallery-type", choices=["html", "markdown"], default="html",
                       help="Gallery type for gallery mode")
    
    args = parser.parse_args()
    
    scraper = AdvancedWebScraper()
    
    if args.mode == "suno" and args.input and args.output:
        songs = scraper.scrape_suno_songs(Path(args.input))
        if songs:
            df = pd.DataFrame(songs)
            df.to_csv(args.output, index=False)
            logger.info(f"Scraped {len(songs)} songs, saved to {args.output}")
    
    elif args.mode == "regex" and args.input and args.pattern and args.output:
        results = scraper.scrape_with_regex(Path(args.input), args.pattern)
        if results:
            df = pd.DataFrame(results)
            df.to_csv(args.output, index=False)
            logger.info(f"Found {len(results)} matches, saved to {args.output}")
    
    elif args.mode == "gallery" and args.urls and args.output:
        success = scraper.generate_image_gallery(args.urls, Path(args.output), args.gallery_type)
        if success:
            logger.info(f"Generated {args.gallery_type} gallery: {args.output}")
    
    elif args.mode == "song-info" and args.urls:
        for url in args.urls:
            info = scraper.extract_song_info(url)
            logger.info(f"URL: {url}")
            for key, value in info.items():
                logger.info(f"  {key}: {value}")
            print()
    
    elif args.mode == "batch" and args.input and args.output:
        html_files = list(Path(args.input).glob("*.html"))
        success = scraper.batch_scrape_songs(html_files, Path(args.output))
        if success:
            logger.info(f"Batch scraping completed: {args.output}")
    
    elif args.mode == "seo" and args.input and args.output:
        # Load song data from CSV
        df = pd.read_csv(args.input)
        song_data = df.to_dict('records')
        success = scraper.generate_seo_content(song_data, Path(args.output))
        if success:
            logger.info(f"SEO content generated: {args.output}")
    
    else:
        logger.info("Invalid arguments. Use --help for usage information.")

if __name__ == "__main__":
    main()