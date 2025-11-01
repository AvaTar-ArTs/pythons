
# Constants
CONSTANT_300 = 300
CONSTANT_500 = 500

#!/usr/bin/env python3
"""
Merged Content Analysis Tool

This file was automatically merged from the following source files:
- /Users/steven/Music/nocTurneMeLoDieS/python/FINAL_ORGANIZED/generation/advanced_content_generator.py
- /Users/steven/Music/nocTurneMeLoDieS/python/CLEAN_ORGANIZED/generation/advanced_content_generator.py

Combines the best features and functionality from multiple similar files.
"""

# Imports from all source files
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
from typing import Dict, List, Optional, Union
import argparse
import csv
import json
import logging
import os
import pandas as pd
import sys

# Documentation from source files
        """Generate description for image using GPT-4 Vision."""
        """Generate descriptions for multiple images."""
"""
    """Main function for command-line usage."""
        """Generate HTML album pages from song data."""
                html_content = f"""
        """Generate video content description."""
        """Generate CSV from HTML song data."""
    """Comprehensive content generation tool with multiple generation modes."""

Advanced Content Generator - Consolidated Generation Script

This script consolidates all content generation functionality from multiple generation scripts
into a comprehensive, feature-rich content generation tool.
"""

import os
import sys
import logging
import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List, Optional, Union
import pandas as pd
from bs4 import BeautifulSoup

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("content_generation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AdvancedContentGenerator:
    """Comprehensive content generation tool with multiple generation modes."""
    
    def __init__(self):
        self.client = client
    
    def generate_song_csv(self, html_files: List[Path], output_path: Path) -> bool:
        """Generate CSV from HTML song data."""
        try:
            song_details = []
            
            for html_file in html_files:
                with open(html_file, "r", encoding="utf-8") as f:
                    html_content = f.read()
                
                soup = BeautifulSoup(html_content, "html.parser")
                for item in soup.find_all("div", class_="css-79jxux"):
                    title_element = item.find("span", class_="text-primary")
                    song_url_element = item.find("a", href=True)
                    cover_url_element = item.find_previous_sibling("img", src=True)
                    genre_element = item.find("a", class_="hover:underline", href=True)
                    time_element = item.find("span", class_="text-mono")
                    
                    song_details.append({
                        "Song Title": title_element["title"] if title_element else "",
                        "Time": time_element.text.strip() if time_element else "",
                        "Genre": genre_element.text.strip() if genre_element else "",
                        "Song URL": song_url_element["href"] if song_url_element else "",
                        "Cover URL": cover_url_element["src"] if cover_url_element else "",
                        "Lyrics": "",
                        "Info": "",
                        "Keys": ""
                    })
            
            df = pd.DataFrame(song_details)
            df.to_csv(output_path, index=False)
            logger.info(f"Generated CSV with {len(song_details)} songs: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating song CSV: {e}")
            return False
    
    def generate_album_pages(self, song_data: List[Dict], output_dir: Path) -> bool:
        """Generate HTML album pages from song data."""
        try:
            output_dir.mkdir(exist_ok=True)
            
            for i, song in enumerate(song_data):
                html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{song.get('Song Title', 'Unknown')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .song-info {{ background: #f5f5f5; padding: 20px; border-radius: 8px; }}
        .cover {{ max-width: 300px; height: auto; }}
    </style>
</head>
<body>
    <div class="song-info">
        <h1>{song.get('Song Title', 'Unknown')}</h1>
        <img src="{song.get('Cover URL', '')}" alt="Cover" class="cover">
        <p><strong>Genre:</strong> {song.get('Genre', 'Unknown')}</p>
        <p><strong>Duration:</strong> {song.get('Time', 'Unknown')}</p>
        <p><strong>URL:</strong> <a href="{song.get('Song URL', '')}">Listen</a></p>
        <p><strong>Lyrics:</strong> {song.get('Lyrics', 'Not available')}</p>
    </div>
</body>
</html>
"""
                output_file = output_dir / f"song_{i+1:03d}.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            
            logger.info(f"Generated {len(song_data)} album pages in {output_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating album pages: {e}")
            return False
    
    def generate_image_description(self, image_url: str) -> str:
        """Generate description for image using GPT-4 Vision."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Create a detailed and descriptive image prompt for this image as if you were to recreate it."
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url}
                            }
                        ]
                    }
                ],
                max_tokens=CONSTANT_300
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating image description: {e}")
            return f"Description generation failed: {str(e)}"
    
    def generate_video_content(self, prompt: str, duration: int = 30) -> str:
        """Generate video content description."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a video content creator. Generate detailed video content based on the given prompt."
                    },
                    {
                        "role": "user",
                        "content": f"Create video content for: {prompt}\nDuration: {duration} seconds"
                    }
                ],
                max_tokens=CONSTANT_500,
                temperature=0.8
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating video content: {e}")
            return f"Video generation failed: {str(e)}"
    
    def batch_generate_descriptions(self, image_urls: List[str], output_file: Path) -> bool:
        """Generate descriptions for multiple images."""
        try:
            descriptions = []
            
            for url in image_urls:
                description = self.generate_image_description(url)
                descriptions.append({"url": url, "description": description})
            
            df = pd.DataFrame(descriptions)
            df.to_csv(output_file, index=False)
            logger.info(f"Generated descriptions for {len(descriptions)} images: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error batch generating descriptions: {e}")
            return False

def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Advanced Content Generator")
    parser.add_argument("--mode", choices=["csv", "html", "image", "video"], required=True,
                       help="Generation mode")
    parser.add_argument("--input", help="Input file or directory")
    parser.add_argument("--output", help="Output file or directory")
    parser.add_argument("--urls", nargs="+", help="Image URLs for description generation")
    parser.add_argument("--prompt", help="Content prompt")
    
    args = parser.parse_args()
    
    generator = AdvancedContentGenerator()
    
    if args.mode == "csv" and args.input and args.output:
        html_files = [Path(f) for f in args.input.split(",")]
        generator.generate_song_csv(html_files, Path(args.output))
    
    elif args.mode == "html" and args.input and args.output:
        # Load song data from CSV
        df = pd.read_csv(args.input)
        song_data = df.to_dict('records')
        generator.generate_album_pages(song_data, Path(args.output))
    
    elif args.mode == "image" and args.urls and args.output:
        generator.batch_generate_descriptions(args.urls, Path(args.output))
    
    elif args.mode == "video" and args.prompt and args.output:
        content = generator.generate_video_content(args.prompt)
        with open(args.output, 'w') as f:
            f.write(content)
        logger.info(f"Video content generated: {args.output}")
    
    else:
        logger.info("Invalid arguments. Use --help for usage information.")

if __name__ == "__main__":
    main()
