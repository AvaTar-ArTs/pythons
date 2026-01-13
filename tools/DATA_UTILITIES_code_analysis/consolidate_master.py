#!/usr/bin/env python3
"""from collections import defaultdict
from datetime import datetime
from pathlib import Path
import csv
import json
import re

from difflib import SequenceMatcher
Intelligent CSV Consolidation for nocturnemelodies Music Catalog
Combines multiple Suno CSV exports with MP3 file inventory
"""

# Configuration
PRIMARY_SOURCE = "suno_ultimate_master.csv"
SECONDARY_SOURCES = [
    "suno-9-2025 - songs_master_combined_data.csv",
    "suno_ultimate_master_combined.csv",
    "Discography ALL.csv",
]
MP3_INVENTORY = "/Users/steven/clean/audio-11-29-08:26.csv"
OUTPUT_FILE = "NOCTURNEMELODIES_MASTER_CATALOG.csv"
REPORT_FILE = "consolidation_report.json"


def extract_song_id(url_or_id):
    """Extract song ID from URL or return as-is"""
    if not url_or_id:
        return None
    if "suno.com/song/" in url_or_id or "suno.ai/song/" in url_or_id:
        return url_or_id.split("/song/")[-1].split("?")[0].strip()
    return url_or_id.strip()


def normalize_title(title):
    """Normalize song title for matching"""
    if not title:
        return ""
    # Remove special characters, lowercase, strip whitespace
    normalized = re.sub(r"[^\w\s-]", "", title.lower())
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def similarity_score(str1, str2):
    """Calculate similarity between two strings (0-1)"""
    return SequenceMatcher(None, str1, str2).ratio()


def parse_duration(duration_str):
    """Parse duration string to seconds"""
    if not duration_str:
        return None
    try:
        # Handle formats like "3:45" or "4:27"
        parts = str(duration_str).split(":")
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        return int(duration_str)
    except:
        return None


def load_mp3_inventory(filepath):
    """Load MP3 file inventory"""
    mp3_files = {}
    if not Path(filepath).exists():
        print(f"⚠️  MP3 inventory not found: {filepath}")
        return mp3_files

    with open(filepath, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row.get("Filename", "")
            normalized_name = normalize_title(filename.replace(".mp3", ""))
            mp3_files[normalized_name] = {
                "filename": filename,
                "duration": row.get("Duration", ""),
                "file_size": row.get("File Size", ""),
                "creation_date": row.get("Creation Date", ""),
                "path": row.get("Original Path", ""),
            }
    return mp3_files


def load_primary_source():
    """Load the primary master CSV"""
    songs = {}
    with open(PRIMARY_SOURCE, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song_id = extract_song_id(row.get("id") or row.get("url", ""))
            if song_id:
                songs[song_id] = {
                    "id": song_id,
                    "title": row.get("title", ""),
                    "url": row.get("url", ""),
                    "audio_url": row.get("audioUrl", ""),
                    "image_url": row.get("imageUrl", ""),
                    "duration": row.get("duration", ""),
                    "artist": row.get("author", ""),
                    "artist_link": row.get("authorLink", ""),
                    "published": row.get("published", ""),
                    "plays": row.get("plays", ""),
                    "likes": row.get("likes", ""),
                    "style": row.get("style", ""),
                    "lyrics": row.get("lyrics", ""),
                    "version": row.get("version", ""),
                    "playlist": row.get("playlist", ""),
                    "source_files": row.get("sourceFiles", ""),
                    "analysis": "",
                    "keys": "",
                    "mp3_filename": "",
                    "mp3_path": "",
                    "mp3_file_size": "",
                    "source": "master",
                }
    return songs


def merge_secondary_sources(songs):
    """Merge data from secondary sources"""
    stats = {"songs_added": 0, "fields_enriched": 0, "duplicates_skipped": 0}

    # Load songs_master for additional songs
    filepath = Path("suno-9-2025 - songs_master_combined_data.csv")
    if filepath.exists():
        with open(filepath, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                song_id = extract_song_id(row.get("SongURL", ""))
                if not song_id:
                    continue

                if song_id not in songs:
                    # New song, add it
                    songs[song_id] = {
                        "id": song_id,
                        "title": row.get("SongTitle", ""),
                        "url": row.get("SongURL", ""),
                        "audio_url": "",
                        "image_url": row.get("CoverUrl", ""),
                        "duration": row.get("Time", ""),
                        "artist": "",
                        "artist_link": "",
                        "published": "",
                        "plays": "",
                        "likes": "",
                        "style": "",
                        "lyrics": "",
                        "version": row.get("Version", ""),
                        "playlist": "",
                        "source_files": "",
                        "analysis": "",
                        "keys": row.get("Keys", ""),
                        "mp3_filename": "",
                        "mp3_path": "",
                        "mp3_file_size": "",
                        "source": "songs_master",
                    }
                    stats["songs_added"] += 1
                # Enrich existing song with keys if not present
                elif not songs[song_id]["keys"] and row.get("Keys"):
                    songs[song_id]["keys"] = row.get("Keys", "")
                    stats["fields_enriched"] += 1

    # Load Discography for analysis data
    filepath = Path("Discography ALL.csv")
    if filepath.exists():
        with open(filepath, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                song_id = extract_song_id(row.get("Song URL", ""))
                title_key = normalize_title(row.get("Song Title", ""))

                # Try to match by ID first, then by title
                matched_id = None
                if song_id and song_id in songs:
                    matched_id = song_id
                else:
                    # Try title matching
                    for sid, song in songs.items():
                        if (
                            similarity_score(normalize_title(song["title"]), title_key)
                            > 0.85
                        ):
                            matched_id = sid
                            break

                if matched_id:
                    # Merge analysis data
                    if row.get("Analysis"):
                        songs[matched_id]["analysis"] = row.get("Analysis", "")
                        stats["fields_enriched"] += 1
                    if row.get("Keys") and not songs[matched_id]["keys"]:
                        songs[matched_id]["keys"] = row.get("Keys", "")
                        stats["fields_enriched"] += 1

    return songs, stats


def match_mp3_files(songs, mp3_files):
    """Match MP3 files to songs in catalog"""
    stats = {
        "exact_matches": 0,
        "fuzzy_matches": 0,
        "unmatched_songs": 0,
        "unmatched_files": 0,
    }

    unmatched_files = set(mp3_files.keys())

    for song_id, song in songs.items():
        title_normalized = normalize_title(song["title"])

        # Try exact match first
        if title_normalized in mp3_files:
            mp3_data = mp3_files[title_normalized]
            song["mp3_filename"] = mp3_data["filename"]
            song["mp3_path"] = mp3_data["path"]
            song["mp3_file_size"] = mp3_data["file_size"]
            stats["exact_matches"] += 1
            unmatched_files.discard(title_normalized)
            continue

        # Try fuzzy matching
        best_match = None
        best_score = 0.75  # Minimum similarity threshold

        for mp3_key in mp3_files.keys():
            score = similarity_score(title_normalized, mp3_key)
            if score > best_score:
                best_score = score
                best_match = mp3_key

        if best_match:
            mp3_data = mp3_files[best_match]
            song["mp3_filename"] = mp3_data["filename"]
            song["mp3_path"] = mp3_data["path"]
            song["mp3_file_size"] = mp3_data["file_size"]
            stats["fuzzy_matches"] += 1
            unmatched_files.discard(best_match)
        else:
            stats["unmatched_songs"] += 1

    stats["unmatched_files"] = len(unmatched_files)

    return songs, stats, unmatched_files


def write_master_catalog(songs, output_file):
    """Write consolidated master catalog"""
    fieldnames = [
        "id",
        "title",
        "url",
        "audio_url",
        "image_url",
        "duration",
        "artist",
        "artist_link",
        "published",
        "plays",
        "likes",
        "style",
        "lyrics",
        "version",
        "playlist",
        "source_files",
        "keys",
        "analysis",
        "mp3_filename",
        "mp3_path",
        "mp3_file_size",
        "source",
    ]

    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        # Sort by title
        sorted_songs = sorted(songs.values(), key=lambda x: x["title"].lower())
        writer.writerows(sorted_songs)


def main():
    print("=" * 80)
    print("NOCTURNEMELODIES MASTER CATALOG CONSOLIDATION")
    print("=" * 80)

    # Load data sources
    print("\n📥 Loading primary source...")
    songs = load_primary_source()
    print(f"   ✓ Loaded {len(songs)} songs from {PRIMARY_SOURCE}")

    print("\n📥 Loading MP3 inventory...")
    mp3_files = load_mp3_inventory(MP3_INVENTORY)
    print(f"   ✓ Loaded {len(mp3_files)} MP3 files")

    print("\n🔄 Merging secondary sources...")
    songs, merge_stats = merge_secondary_sources(songs)
    print(f"   ✓ Added {merge_stats['songs_added']} new songs")
    print(f"   ✓ Enriched {merge_stats['fields_enriched']} fields")

    print("\n🔗 Matching MP3 files to catalog...")
    songs, match_stats, unmatched_files = match_mp3_files(songs, mp3_files)
    print(f"   ✓ Exact matches: {match_stats['exact_matches']}")
    print(f"   ✓ Fuzzy matches: {match_stats['fuzzy_matches']}")
    print(f"   ⚠ Unmatched songs: {match_stats['unmatched_songs']}")
    print(f"   ⚠ Unmatched files: {match_stats['unmatched_files']}")

    print("\n💾 Writing master catalog...")
    write_master_catalog(songs, OUTPUT_FILE)
    print(f"   ✓ Saved to: {OUTPUT_FILE}")

    # Generate report
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_songs": len(songs),
        "total_mp3_files": len(mp3_files),
        "merge_stats": merge_stats,
        "match_stats": match_stats,
        "unmatched_files": list(unmatched_files)[:50],  # Limit to 50 for readability
    }

    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)

    print("\n📊 Consolidation Report:")
    print(f"   • Total songs in catalog: {len(songs)}")
    print(
        f"   • Songs with MP3 files: {match_stats['exact_matches'] + match_stats['fuzzy_matches']}",
    )
    print(f"   • Songs without MP3 files: {match_stats['unmatched_songs']}")
    print(f"   • Orphaned MP3 files: {match_stats['unmatched_files']}")
    print(f"\n✅ Complete! Report saved to: {REPORT_FILE}")
    print("=" * 80)


if __name__ == "__main__":
    main()
