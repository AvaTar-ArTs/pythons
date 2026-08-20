#!/usr/bin/env python3
"""
nocTurneMeLoDies Music Data Generator

This script reads from the consolidated music database CSV and generates
JavaScript data files for the music gallery web interface.
"""

import csv
import json
import re
from pathlib import Path
from collections import defaultdict

class MusicDataGenerator:
    def __init__(self, csv_path, output_dir):
        self.csv_path = Path(csv_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Genre mapping based on song titles and tags
        self.genre_keywords = {
            'electronic': ['electronic', 'dance', 'remix', 'mixd', 'edm', 'techno', 'synth'],
            'classical': ['classical', 'orchestral', 'symphony', 'piano', 'violin', 'orchestra'],
            'jazz': ['jazz', 'blues', 'swing', 'bebop'],
            'rock': ['rock', 'metal', 'punk', 'grunge', 'alternative'],
            'pop': ['pop', 'summer', 'lover', 'love', 'boy', 'girl'],
            'ambient': ['ambient', 'atmospheric', 'void', 'veil', 'mystical', 'ethereal'],
            'hip-hop': ['hip-hop', 'rap', 'beats', 'flow'],
            'country': ['country', 'folk', 'americana'],
            'reggae': ['reggae', 'dub', 'roots'],
            'world': ['world', 'ethnic', 'traditional', 'cultural'],
            'soundtrack': ['soundtrack', 'score', 'cinematic', 'film'],
            'experimental': ['experimental', 'avant-garde', 'noise', 'abstract']
        }

    def clean_title(self, title):
        """Clean and normalize song titles"""
        if not title:
            return "Untitled AI Composition"

        # Remove extra quotes and formatting
        title = title.strip('"')

        # Remove (Remastered), (Remix) suffixes for cleaner display
        title = re.sub(r'\s*\([^)]*(?:remaster|remix)[^)]*\)', '', title, flags=re.IGNORECASE)

        # Remove numbers at the end
        title = re.sub(r'\d+$', '', title).strip()

        # Clean up extra spaces
        title = re.sub(r'\s+', ' ', title)

        return title or "Untitled AI Composition"

    def detect_genre(self, title, tags=""):
        """Detect genre based on title and tags"""
        text = f"{title} {tags}".lower()

        for genre, keywords in self.genre_keywords.items():
            if any(keyword in text for keyword in keywords):
                return genre

        # Default genres based on common patterns
        if any(word in text for word in ['night', 'dark', 'shadow', 'storm']):
            return 'ambient'
        if any(word in text for word in ['hero', 'villain', 'rise', 'overthrow']):
            return 'rock'
        if any(word in text for word in ['love', 'heart', 'summer']):
            return 'pop'

        return 'electronic'  # Default genre

    def extract_tags(self, title, tags_string=""):
        """Extract meaningful tags from title and tags"""
        tags = []

        # Add genre-based tags
        genre = self.detect_genre(title, tags_string)
        tags.append(genre)

        # Extract specific keywords
        text = f"{title} {tags_string}".lower()

        if 'remix' in text or 'mixd' in text:
            tags.append('remix')
        if 'night' in text or 'dark' in text:
            tags.append('dark')
        if 'love' in text or 'lover' in text:
            tags.append('romantic')
        if 'hero' in text or 'villain' in text:
            tags.append('epic')
        if 'void' in text or 'veil' in text:
            tags.append('atmospheric')
        if '🐍' in title:
            tags.append('snake')
        if '🎵' in title:
            tags.append('music')

        return tags

    def process_csv(self):
        """Process the CSV file and generate music data"""
        songs = []

        try:
            with open(self.csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    # Skip entries without audio URLs
                    if not row.get('audio_url'):
                        continue

                    song = {
                        'id': row.get('song_id', ''),
                        'title': self.clean_title(row.get('title', '')),
                        'url': row.get('audio_url', ''),
                        'image_url': row.get('image_url', '') or 'images/default-album.svg',
                        'duration': row.get('duration', '3:00'),
                        'genre': self.detect_genre(row.get('title', ''), row.get('tags', '')),
                        'tags': self.extract_tags(row.get('title', ''), row.get('tags', '')),
                        'date_added': row.get('consolidated_at', '').split('T')[0] if row.get('consolidated_at') else '2026-01-23'
                    }

                    # Ensure duration format
                    if ':' not in song['duration']:
                        song['duration'] = '3:00'

                    songs.append(song)

        except FileNotFoundError:
            print(f"Error: CSV file not found at {self.csv_path}")
            return []
        except Exception as e:
            print(f"Error processing CSV: {e}")
            return []

        return songs

    def generate_js_data(self, songs):
        """Generate JavaScript data file"""
        js_content = f"""// nocTurneMeLoDies Music Data
// Generated from {self.csv_path}
// Total songs: {len(songs)}

const musicData = {json.dumps(songs, indent=2)};

// Export for Node.js environments
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = musicData;
}}
"""

        output_path = self.output_dir / 'music-data.js'
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(js_content)

        print(f"Generated JavaScript data file: {output_path}")
        print(f"Total songs processed: {len(songs)}")

    def generate_genre_stats(self, songs):
        """Generate genre statistics"""
        genre_counts = defaultdict(int)

        for song in songs:
            genre_counts[song['genre']] += 1

        stats = {
            'total_songs': len(songs),
            'genres': dict(sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)),
            'generated_at': '2026-01-23'
        }

        output_path = self.output_dir / 'music-stats.json'
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(stats, file, indent=2)

        print(f"Generated statistics file: {output_path}")
        return stats

    def generate_html_preview(self, songs, limit=50):
        """Generate a simple HTML preview of the music data"""
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>nocTurneMeLoDies Data Preview</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .song {{ margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
        .genre {{ color: #666; font-style: italic; }}
        .tags {{ margin-top: 5px; }}
        .tag {{ display: inline-block; background: #f0f0f0; padding: 2px 6px; margin: 2px; border-radius: 3px; font-size: 0.8em; }}
        .stats {{ background: #f9f9f9; padding: 15px; margin: 20px 0; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>nocTurneMeLoDies Music Data Preview</h1>
    <div class="stats">
        <h2>Statistics</h2>
        <p><strong>Total Songs:</strong> {len(songs)}</p>
        <p><strong>Sample Songs Shown:</strong> {min(limit, len(songs))}</p>
    </div>

    <h2>Music Library</h2>
"""

        for i, song in enumerate(songs[:limit]):
            html_content += f"""
    <div class="song">
        <h3>{i+1}. {song['title']}</h3>
        <p class="genre">Genre: {song['genre']} | Duration: {song['duration']}</p>
        <div class="tags">
            {' '.join(f'<span class="tag">{tag}</span>' for tag in song['tags'])}
        </div>
        <p><small>ID: {song['id']}</small></p>
    </div>
"""

        html_content += """
</body>
</html>
"""

        output_path = self.output_dir / 'music-data-preview.html'
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(html_content)

        print(f"Generated HTML preview: {output_path}")

def main():
    # Configuration
    csv_path = "/Users/steven/Music/nocTurneMeLoDies/consolidated_music_database_20260123_072130.csv"
    output_dir = "/Users/steven/avatararts.org"

    # Generate music data
    generator = MusicDataGenerator(csv_path, output_dir)
    songs = generator.process_csv()

    if songs:
        generator.generate_js_data(songs)
        stats = generator.generate_genre_stats(songs)
        generator.generate_html_preview(songs)

        print(f"\nSuccess! Processed {len(songs)} songs")
        print("Top genres:", list(stats['genres'].keys())[:5])
    else:
        print("No songs found to process")

if __name__ == "__main__":
    main()