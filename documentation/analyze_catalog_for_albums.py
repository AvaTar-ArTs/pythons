import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""from collections import Counter
import re

import pandas as pd
Analyze Full Catalog and Suggest Album Compilations
Creates a strategic release plan for all 590 songs
"""

# Configuration
CSV_FILE = "/Users/steven/Downloads/Misc/suno_ultimate_master - suno_ultimate_master_combined(1).csv"
OUTPUT_DIR = "/Users/steven/Music/nocTurneMeLoDieS/RELEASES"


def clean_genre(genre_str):
    """Extract and clean genre information"""
    if pd.isna(genre_str):
        return []
    genres = [g.strip().lower() for g in str(genre_str).split(",")]
    return genres


def suggest_themed_albums(df):
    """Suggest album compilations based on themes, genres, and titles"""
    print("=" * 80)
    print("ALBUM COMPILATION SUGGESTIONS")
    print("=" * 80)
    print()

    albums = []

    # Album 1: Already completed
    albums.append(
        {
            "name": "Best of AvaTar ArTs - Vol 1",
            "status": "✓ COMPLETED",
            "tracks": 20,
            "theme": "Greatest hits compilation",
        },
    )

    # Album 2: Moonlit & Mystical themes
    moonlit_keywords = [
        "moon",
        "night",
        "dark",
        "shadow",
        "midnight",
        "twilight",
        "echo",
    ]
    moonlit_songs = []
    for idx, row in df.iterrows():
        title = str(row["Song Name"]).lower()
        if any(kw in title for kw in moonlit_keywords):
            moonlit_songs.append(row["Song Name"])

    if len(moonlit_songs) >= 12:
        albums.append(
            {
                "name": "Moonlit Echoes",
                "status": "READY TO CURATE",
                "tracks": min(20, len(moonlit_songs)),
                "theme": "Nighttime, moonlit, mystical atmosphere",
                "sample_tracks": moonlit_songs[:5],
            },
        )

    # Album 3: Love & Romance (or Anti-Love)
    love_keywords = ["love", "heart", "kiss", "romance", "valentine", "crush", "trashy"]
    love_songs = []
    for idx, row in df.iterrows():
        title = str(row["Song Name"]).lower()
        if any(kw in title for kw in love_keywords):
            love_songs.append(row["Song Name"])

    if len(love_songs) >= 12:
        albums.append(
            {
                "name": "Love is Rubbish: The Anti-Valentine Collection",
                "status": "READY TO CURATE",
                "tracks": min(20, len(love_songs)),
                "theme": "Love, heartbreak, anti-romance",
                "sample_tracks": love_songs[:5],
            },
        )

    # Album 4: Alley & Urban themes
    alley_keywords = ["alley", "street", "city", "urban", "road", "town"]
    alley_songs = []
    for idx, row in df.iterrows():
        title = str(row["Song Name"]).lower()
        if any(kw in title for kw in alley_keywords):
            alley_songs.append(row["Song Name"])

    if len(alley_songs) >= 12:
        albums.append(
            {
                "name": "Tales from the Alley",
                "status": "READY TO CURATE",
                "tracks": min(20, len(alley_songs)),
                "theme": "Urban street life, alley stories",
                "sample_tracks": alley_songs[:5],
            },
        )

    # Album 5: Blues collection
    blues_songs = []
    for idx, row in df.iterrows():
        genres = clean_genre(row.get("genres", ""))
        title = str(row["Song Name"]).lower()
        if "blues" in genres or "blues" in title:
            blues_songs.append(row["Song Name"])

    if len(blues_songs) >= 12:
        albums.append(
            {
                "name": "Sammy's Blues Collection",
                "status": "READY TO CURATE",
                "tracks": min(20, len(blues_songs)),
                "theme": "Blues, soulful, melancholic",
                "sample_tracks": blues_songs[:5],
            },
        )

    # Album 6: Spirits & Supernatural
    supernatural_keywords = [
        "spirit",
        "ghost",
        "witch",
        "magic",
        "spell",
        "haunt",
        "mystic",
    ]
    supernatural_songs = []
    for idx, row in df.iterrows():
        title = str(row["Song Name"]).lower()
        if any(kw in title for kw in supernatural_keywords):
            supernatural_songs.append(row["Song Name"])

    if len(supernatural_songs) >= 12:
        albums.append(
            {
                "name": "Spirits & Shadows",
                "status": "READY TO CURATE",
                "tracks": min(20, len(supernatural_songs)),
                "theme": "Supernatural, witches, spirits",
                "sample_tracks": supernatural_songs[:5],
            },
        )

    # Album 7: Dance & Upbeat
    dance_keywords = ["dance", "party", "celebration", "joy", "happy", "groove"]
    dance_songs = []
    for idx, row in df.iterrows():
        title = str(row["Song Name"]).lower()
        genres = clean_genre(row.get("genres", ""))
        if any(kw in title for kw in dance_keywords) or "dance" in genres:
            dance_songs.append(row["Song Name"])

    if len(dance_songs) >= 12:
        albums.append(
            {
                "name": "Dance Like Nobody's Watching",
                "status": "READY TO CURATE",
                "tracks": min(20, len(dance_songs)),
                "theme": "Upbeat, danceable, celebratory",
                "sample_tracks": dance_songs[:5],
            },
        )

    # Print suggestions
    for i, album in enumerate(albums, 1):
        print(f"ALBUM {i}: {album['name']}")
        print(f"Status: {album['status']}")
        print(f"Tracks: {album['tracks']}")
        print(f"Theme: {album['theme']}")
        if album.get("sample_tracks"):
            print("Sample tracks:")
            for track in album["sample_tracks"]:
                print(f"  - {track}")
        print()

    return albums


def calculate_release_strategy(df, num_albums=12):
    """Calculate how many albums can be created from catalog"""
    print("=" * 80)
    print("RELEASE STRATEGY CALCULATOR")
    print("=" * 80)
    print()

    total_songs = len(df)
    songs_per_album = 20

    # Calculate maximum possible albums
    max_albums = total_songs // songs_per_album

    print(f"Total songs in catalog: {total_songs}")
    print(f"Songs per album: {songs_per_album}")
    print(f"Maximum possible albums: {max_albums}")
    print()

    # Monthly release schedule
    print("SUGGESTED RELEASE SCHEDULE:")
    print("-" * 80)
    print()

    schedules = [
        {
            "name": "Conservative (Quarterly)",
            "frequency": "1 album every 3 months",
            "albums_per_year": 4,
            "years_to_complete": num_albums / 4,
        },
        {
            "name": "Moderate (Bi-Monthly)",
            "frequency": "1 album every 2 months",
            "albums_per_year": 6,
            "years_to_complete": num_albums / 6,
        },
        {
            "name": "Aggressive (Monthly)",
            "frequency": "1 album per month",
            "albums_per_year": 12,
            "years_to_complete": num_albums / 12,
        },
    ]

    for schedule in schedules:
        print(f"{schedule['name']}")
        print(f"  Frequency: {schedule['frequency']}")
        print(f"  Albums/year: {schedule['albums_per_year']}")
        print(
            f"  Time to release {num_albums} albums: {schedule['years_to_complete']:.1f} years",
        )
        print()

    # Revenue projections
    print("REVENUE PROJECTIONS (Conservative estimates):")
    print("-" * 80)
    print()

    streams_per_album = [10000, 50000, 100000]  # Conservative, Moderate, Optimistic
    revenue_per_1k = 4  # $4 per 1000 streams average

    for i, streams in enumerate(streams_per_album, 1):
        scenario = ["Conservative", "Moderate", "Optimistic"][i - 1]
        revenue_per_album = (streams / 1000) * revenue_per_1k
        total_revenue = revenue_per_album * num_albums

        print(f"{scenario}: {streams:,} streams per album")
        print(f"  Revenue per album: ${revenue_per_album:,.0f}")
        print(f"  Total from {num_albums} albums: ${total_revenue:,.0f}")
        print()


def main():
    print("=" * 80)
    print("AVATARARTS CATALOG ANALYSIS & RELEASE PLANNING")
    print("=" * 80)
    print()

    # Load CSV
    print(f"Loading: {CSV_FILE}")
    df = pd.read_csv(CSV_FILE)
    print(f"✓ Loaded {len(df)} songs")
    print()

    # Suggest themed albums
    albums = suggest_themed_albums(df)

    # Calculate release strategy
    calculate_release_strategy(df, num_albums=len(albums))

    # Summary
    print("=" * 80)
    print("RECOMMENDED NEXT STEPS")
    print("=" * 80)
    print()
    print("1. ✓ Album 1 completed: 'Best of AvaTar ArTs - Vol 1'")
    print("2. Choose Album 2 theme from suggestions above")
    print("3. Create curation script for Album 2")
    print("4. Set up monthly release calendar")
    print("5. Start building social media presence")
    print("6. Submit Album 1 to playlists while working on Album 2")
    print()
    print(f"Potential: {len(albums)} themed albums from your {len(df)} song catalog!")
    print()


try:
        main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)