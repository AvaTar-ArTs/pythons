#!/usr/bin/env python3
"""
Music Track Selector for Licensing Platforms
Analyzes Suno database and selects best tracks for AudioJungle/Spotify

Usage: python3 track-selector.py
"""

import os
import csv
import json
from pathlib import Path
from collections import defaultdict, Counter
import shutil

# Configuration
MUSIC_DIR = Path.home() / "Music"
SUNO_CSV = MUSIC_DIR / "suno_merged_master_20250904-143205.csv"
OUTPUT_DIR = Path(__file__).parent / "selected-tracks"
METADATA_FILE = OUTPUT_DIR / "track-metadata.json"

# Commercial viability categories
CATEGORIES = {
    "background": ["ambient", "chill", "lo-fi", "calm", "peaceful", "relaxing"],
    "energetic": ["upbeat", "energetic", "happy", "positive", "motivational"],
    "corporate": ["corporate", "business", "professional", "inspiring", "success"],
    "cinematic": ["dramatic", "epic", "cinematic", "emotional", "powerful"],
    "electronic": ["electronic", "techno", "house", "synth", "edm"],
    "acoustic": ["acoustic", "guitar", "piano", "folk", "organic"],
}

def analyze_suno_database():
    """Analyze Suno master CSV and extract metadata"""
    print("🎵 Analyzing Suno Music Database...")
    print(f"📁 Location: {SUNO_CSV}")

    if not SUNO_CSV.exists():
        print(f"❌ CSV not found: {SUNO_CSV}")
        print("\n🔍 Searching for Suno CSV files...")
        suno_csvs = list(MUSIC_DIR.glob("**/*suno*.csv"))
        if suno_csvs:
            print(f"\n   Found {len(suno_csvs)} CSV files:")
            for csv_file in suno_csvs[:5]:
                print(f"   • {csv_file.name}")
            return None
        return None

    tracks = []
    genres = Counter()
    moods = Counter()

    try:
        with open(SUNO_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                track = {
                    'title': row.get('title', ''),
                    'genre': row.get('genre', row.get('style', '')),
                    'mood': row.get('mood', row.get('tags', '')),
                    'duration': row.get('duration', ''),
                    'created_date': row.get('created_at', row.get('date', '')),
                    'file_path': row.get('file_path', row.get('path', '')),
                }
                tracks.append(track)

                # Track statistics
                if track['genre']:
                    genres[track['genre'].lower()] += 1
                if track['mood']:
                    for mood in track['mood'].lower().split(','):
                        moods[mood.strip()] += 1

        print(f"\n📊 Database Analysis:")
        print(f"   Total tracks: {len(tracks):,}")
        print(f"   Unique genres: {len(genres)}")
        print(f"   Top 5 genres:")
        for genre, count in genres.most_common(5):
            print(f"      • {genre}: {count}")

        return {
            'tracks': tracks,
            'genres': genres,
            'moods': moods
        }

    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return None

def categorize_tracks(database):
    """Categorize tracks by commercial viability"""
    print("\n🎯 Categorizing tracks for commercial use...")

    if not database:
        return {}

    categorized = defaultdict(list)

    for track in database['tracks']:
        track_text = f"{track['title']} {track['genre']} {track['mood']}".lower()

        # Categorize
        matched = False
        for category, keywords in CATEGORIES.items():
            if any(keyword in track_text for keyword in keywords):
                categorized[category].append(track)
                matched = True
                break

        if not matched:
            categorized['other'].append(track)

    print("\n📂 Categorization Results:")
    for category in sorted(categorized.keys()):
        count = len(categorized[category])
        if count > 0:
            print(f"   {category}: {count} tracks")

    return categorized

def select_top_tracks(categorized, per_category=20):
    """Select top tracks from each category"""
    print(f"\n⭐ Selecting top {per_category} tracks per category...")

    selected = {}
    total = 0

    for category, tracks in categorized.items():
        if category == 'other':
            continue

        # Sort by most recent first (assuming more polished)
        sorted_tracks = sorted(
            tracks,
            key=lambda x: x.get('created_date', ''),
            reverse=True
        )[:per_category]

        selected[category] = sorted_tracks
        total += len(selected[category])
        print(f"   ✅ {category}: {len(selected[category])} tracks")

    print(f"\n   📦 Total selected: {total} tracks")
    return selected

def generate_audiojungle_metadata(selected):
    """Generate AudioJungle-optimized metadata"""
    print("\n📝 Generating AudioJungle metadata...")

    aj_metadata = []

    for category, tracks in selected.items():
        for track in tracks:
            metadata = {
                'title': track['title'],
                'category': category.title(),
                'description': f"{category.title()} music track perfect for {get_use_cases(category)}",
                'tags': generate_tags(track, category),
                'price_tier': suggest_price_tier(category),
                'file_path': track.get('file_path', ''),
            }
            aj_metadata.append(metadata)

    # Save metadata
    metadata_path = OUTPUT_DIR / "audiojungle-metadata.json"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(metadata_path, 'w') as f:
        json.dump(aj_metadata, f, indent=2)

    print(f"   ✅ Saved: {metadata_path}")
    return aj_metadata

def get_use_cases(category):
    """Get use cases for each category"""
    use_cases = {
        'background': "videos, podcasts, presentations, vlogs",
        'energetic': "ads, sports videos, workout content, upbeat projects",
        'corporate': "business presentations, explainer videos, corporate ads",
        'cinematic': "movie trailers, dramatic scenes, epic content",
        'electronic': "tech videos, gaming content, modern ads",
        'acoustic': "wedding videos, indie films, organic content",
    }
    return use_cases.get(category, "various projects")

def generate_tags(track, category):
    """Generate SEO-optimized tags for AudioJungle"""
    base_tags = {
        'background': ['ambient', 'background', 'chill', 'calm', 'relaxing', 'atmospheric'],
        'energetic': ['upbeat', 'energetic', 'positive', 'happy', 'motivational', 'inspiring'],
        'corporate': ['corporate', 'business', 'professional', 'success', 'technology'],
        'cinematic': ['cinematic', 'epic', 'dramatic', 'emotional', 'powerful', 'orchestral'],
        'electronic': ['electronic', 'modern', 'tech', 'futuristic', 'digital', 'synth'],
        'acoustic': ['acoustic', 'guitar', 'organic', 'natural', 'folk', 'indie'],
    }

    tags = base_tags.get(category, [])

    # Add generic commercial tags
    tags.extend(['royalty-free', 'commercial-use', 'background-music'])

    return tags[:15]  # AudioJungle limits tags

def suggest_price_tier(category):
    """Suggest pricing tier based on category"""
    tiers = {
        'background': '$19',
        'energetic': '$25',
        'corporate': '$35',
        'cinematic': '$49',
        'electronic': '$29',
        'acoustic': '$25',
    }
    return tiers.get(category, '$25')

def generate_spotify_strategy(selected):
    """Generate Spotify distribution strategy"""
    print("\n🎵 Generating Spotify strategy...")

    strategy = {
        'album_suggestions': [],
        'playlist_strategy': {},
        'release_schedule': []
    }

    # Suggest albums by category
    for category, tracks in selected.items():
        if len(tracks) >= 10:
            album = {
                'name': f"Focus {category.title()} - AvaTarArTs",
                'track_count': min(len(tracks), 15),
                'description': f"Collection of {category} music perfect for focus and productivity",
            }
            strategy['album_suggestions'].append(album)

    # Save strategy
    strategy_path = OUTPUT_DIR / "spotify-strategy.json"
    with open(strategy_path, 'w') as f:
        json.dump(strategy, f, indent=2)

    print(f"   ✅ Saved: {strategy_path}")
    return strategy

def print_next_steps(selected, aj_metadata):
    """Print actionable next steps"""
    print("\n" + "="*60)
    print("🚀 NEXT STEPS FOR MUSIC LICENSING")
    print("="*60)

    total_tracks = sum(len(tracks) for tracks in selected.values())

    print(f"\n📊 You have {total_tracks} tracks ready for licensing!")

    print("\n1️⃣  AudioJungle Setup:")
    print("   1. Go to https://audiojungle.net/")
    print("   2. Click 'Become an Author'")
    print("   3. Upload tracks from selected-tracks/")
    print("   4. Use metadata from audiojungle-metadata.json")
    print("   5. Price using suggested tiers")

    print("\n2️⃣  DistroKid Setup (Spotify/Apple Music):")
    print("   1. Go to https://distrokid.com/")
    print("   2. Sign up ($19.99/year for unlimited uploads)")
    print("   3. Create albums using spotify-strategy.json")
    print("   4. Upload 10-15 tracks per album")
    print("   5. Set up 'AvaTarArTs' as artist name")

    print("\n3️⃣  Pricing Strategy:")
    print("   AudioJungle:")
    print("   • Background/Ambient: $19-25")
    print("   • Corporate/Energetic: $29-35")
    print("   • Cinematic: $39-49")
    print("   You earn 50-70% depending on exclusivity")

    print("\n4️⃣  SEO Keywords for Titles:")
    keywords = [
        "Royalty Free Background Music",
        "Corporate Motivational",
        "Cinematic Epic Trailer",
        "Upbeat Energetic",
        "Ambient Chill Lo-Fi",
    ]
    for kw in keywords:
        print(f"   • {kw}")

    print("\n5️⃣  Revenue Projections:")
    print("   If 100 tracks average 5 sales/month at $25:")
    print("   100 tracks × 5 sales × $25 × 60% = $7,500/month")
    print("\n   Conservative (2 sales/month):")
    print("   100 tracks × 2 sales × $25 × 60% = $3,000/month")

    print("\n6️⃣  Marketing Strategy:")
    print("   • Create YouTube channel with free versions")
    print("   • Link to paid licenses")
    print("   • Build email list of video creators")
    print("   • Offer first track free to build reputation")

    print("\n7️⃣  Read complete guide:")
    guide_path = Path(__file__).parent / "audiojungle-setup.md"
    print(f"   open {guide_path}")

    print("\n" + "="*60)

def main():
    print("🎵 MUSIC LICENSING TRACK SELECTOR")
    print("="*60)

    # Step 1: Analyze Suno database
    database = analyze_suno_database()

    if not database:
        print("\n⚠️  Could not analyze Suno database.")
        print("   Please check the CSV file location.")
        return

    # Step 2: Categorize tracks
    categorized = categorize_tracks(database)

    # Step 3: Select top tracks
    selected = select_top_tracks(categorized, per_category=20)

    # Step 4: Generate AudioJungle metadata
    aj_metadata = generate_audiojungle_metadata(selected)

    # Step 5: Generate Spotify strategy
    spotify_strategy = generate_spotify_strategy(selected)

    # Step 6: Next steps
    print_next_steps(selected, aj_metadata)

    print("\n✅ Music licensing setup complete!")
    print(f"📁 Check output: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
