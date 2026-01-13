#!/usr/bin/env python3
"""from collections import defaultdict
from datetime import datetime
from pathlib import Path
import csv
import json
import os

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from mutagen.mp3 import MP3
Enhanced Master Catalog - Deep scan incorporating all existing data sources.
Combines metadata from CSVs, JSON bundles, transcripts, and file analysis.
"""


# Configuration
MUSIC_DIR = Path("/Users/steven/Music/nocTurneMeLoDieS")
BUNDLES_DIR = MUSIC_DIR / "SONG_BUNDLES"
DATA_DIR = MUSIC_DIR / "DATA"
DOCS_DIR = MUSIC_DIR / "DOCS"

OUTPUT_CSV = DATA_DIR / "ENHANCED_MASTER_CATALOG.csv"
OUTPUT_SUMMARY = DATA_DIR / "CATALOG_SUMMARY_ENHANCED.txt"


def load_existing_metadata():
    """Load metadata from existing CSV files."""
    existing_data = {}

    # Try to load MUSIC_FOLDER_METADATA_COMPLETE.csv
    metadata_csv = DOCS_DIR / "MUSIC_FOLDER_METADATA_COMPLETE.csv"
    if metadata_csv.exists():
        try:
            with open(metadata_csv, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    filename = row.get("filename", "")
                    if filename:
                        existing_data[filename] = {
                            "genre": row.get("genre", ""),
                            "content_type": row.get("content_type", ""),
                            "bitrate": row.get("bitrate", ""),
                        }
        except Exception as e:
            print(f"Note: Could not load {metadata_csv}: {e}")

    return existing_data


def load_bundle_info():
    """Load song info from SONG_BUNDLES JSON files."""
    bundle_data = {}

    if not BUNDLES_DIR.exists():
        return bundle_data

    for json_file in BUNDLES_DIR.glob("*.json"):
        try:
            with open(json_file, encoding="utf-8") as f:
                data = json.load(f)
                song_info = data.get("song_info", {})
                title = song_info.get("title", "")
                if title:
                    bundle_data[title] = {
                        "genre": song_info.get("genre", ""),
                        "style": song_info.get("style", ""),
                        "mood": song_info.get("mood", ""),
                        "bundle_file": json_file.name,
                    }
        except Exception:
            pass

    return bundle_data


def get_mp3_info(mp3_file):
    """Get comprehensive MP3 metadata and file info."""
    info = {
        "duration_seconds": 0,
        "duration_formatted": "0:00",
        "file_size_mb": 0.0,
        "bitrate_kbps": 0,
        "sample_rate": 0,
    }

    try:
        audio = MP3(mp3_file)
        duration = int(audio.info.length)
        info["duration_seconds"] = duration
        info["duration_formatted"] = f"{duration // 60}:{duration % 60:02d}"
        info["bitrate_kbps"] = int(audio.info.bitrate / 1000)
        info["sample_rate"] = audio.info.sample_rate

        file_size_bytes = mp3_file.stat().st_size
        info["file_size_mb"] = round(file_size_bytes / (1024 * 1024), 2)
    except Exception:
        pass

    return info


def find_associated_files(mp3_file):
    """Find all files associated with an MP3 (transcripts, analysis, lyrics)."""
    mp3_dir = mp3_file.parent
    mp3_stem = mp3_file.stem.lower()

    associated = {
        "transcript_files": [],
        "analysis_files": [],
        "lyrics_files": [],
        "prompt_files": [],
        "has_transcript": False,
        "has_analysis": False,
        "has_lyrics": False,
        "has_prompt": False,
        "transcript_count": 0,
        "analysis_count": 0,
    }

    # Search for transcript files
    for txt_file in mp3_dir.glob("*.txt"):
        txt_stem = txt_file.stem.lower()

        # Check if related to this MP3
        if mp3_stem in txt_stem or txt_stem in mp3_stem:
            if "transcript" in txt_stem:
                associated["transcript_files"].append(txt_file.name)
                associated["has_transcript"] = True
            elif "analysis" in txt_stem:
                associated["analysis_files"].append(txt_file.name)
                associated["has_analysis"] = True
            elif "lyrics" in txt_stem:
                associated["lyrics_files"].append(txt_file.name)
                associated["has_lyrics"] = True

    # Check for prompts in prompts/ subdirectory
    prompts_dir = mp3_dir / "prompts"
    if prompts_dir.exists():
        prompt_files = list(prompts_dir.glob("*.txt"))
        if prompt_files:
            associated["has_prompt"] = True
            associated["prompt_files"] = [
                f.name for f in prompt_files[:3]
            ]  # Limit to 3

    associated["transcript_count"] = len(associated["transcript_files"])
    associated["analysis_count"] = len(associated["analysis_files"])

    return associated


def has_artwork(mp3_file):
    """Check if album has artwork/images."""
    album_dir = mp3_file.parent

    # Check for images in album directory
    image_exts = ["*.jpg", "*.jpeg", "*.png", "*.gif"]
    for ext in image_exts:
        if list(album_dir.glob(ext)):
            return True

    # Check images subdirectory
    images_dir = album_dir / "images"
    if images_dir.exists():
        for ext in image_exts:
            if list(images_dir.glob(ext)):
                return True

    return False


def get_album_from_path(mp3_path):
    """Extract album folder name from path."""
    parts = mp3_path.parts
    try:
        music_idx = parts.index("nocTurneMeLoDieS")
        if music_idx + 1 < len(parts):
            return parts[music_idx + 1]
    except ValueError:
        pass
    return "root"


def classify_content_type(duration_seconds):
    """Classify content based on duration."""
    if duration_seconds == 0:
        return "UNKNOWN"
    if duration_seconds < 30:
        return "SHORT_CLIP"
    if duration_seconds < 120:
        return "SHORT_SONG"
    if duration_seconds < 360:
        return "SONG"
    if duration_seconds < 600:
        return "EXTENDED"
    return "LONG_FORM"


def create_catalog_entry(mp3_file, existing_metadata, bundle_info):
    """Create comprehensive catalog entry for an MP3."""
    entry = {}

    # Basic file info
    filename = mp3_file.name
    entry["filename"] = filename
    entry["file_path"] = str(mp3_file.relative_to(MUSIC_DIR))
    entry["full_path"] = str(mp3_file)
    entry["album_folder"] = get_album_from_path(mp3_file)

    # Get MP3 metadata (ID3 tags)
    try:
        audio = EasyID3(mp3_file)
        entry["title"] = (
            audio.get("title", [""])[0] if "title" in audio else mp3_file.stem
        )
        entry["artist"] = audio.get("artist", [""])[0] if "artist" in audio else ""
        entry["album"] = (
            audio.get("album", [""])[0] if "album" in audio else entry["album_folder"]
        )
    except:
        entry["title"] = mp3_file.stem
        entry["artist"] = ""
        entry["album"] = entry["album_folder"]

    # Get file technical info
    mp3_info = get_mp3_info(mp3_file)
    entry.update(mp3_info)

    # Content classification
    entry["content_type"] = classify_content_type(mp3_info["duration_seconds"])

    # Check for associated files
    associated = find_associated_files(mp3_file)
    entry["has_transcript"] = "Y" if associated["has_transcript"] else "N"
    entry["has_analysis"] = "Y" if associated["has_analysis"] else "N"
    entry["has_lyrics"] = "Y" if associated["has_lyrics"] else "N"
    entry["has_prompt"] = "Y" if associated["has_prompt"] else "N"
    entry["transcript_count"] = associated["transcript_count"]
    entry["analysis_count"] = associated["analysis_count"]
    entry["transcript_files"] = "; ".join(
        associated["transcript_files"][:3],
    )  # Limit display
    entry["analysis_files"] = "; ".join(associated["analysis_files"][:3])

    # Check for artwork
    entry["has_artwork"] = "Y" if has_artwork(mp3_file) else "N"

    # Genre from existing metadata or bundle info
    entry["genre"] = ""
    entry["style"] = ""
    entry["mood"] = ""

    # Try existing metadata first
    if filename in existing_metadata:
        entry["genre"] = existing_metadata[filename].get("genre", "")

    # Try bundle info by title
    title = entry["title"]
    if title in bundle_info:
        if not entry["genre"]:
            entry["genre"] = bundle_info[title].get("genre", "")
        entry["style"] = bundle_info[title].get("style", "")
        entry["mood"] = bundle_info[title].get("mood", "")

    # Completeness score (0-100)
    score = 0
    if entry["artist"]:
        score += 15
    if entry["album"]:
        score += 15
    if entry["title"]:
        score += 10
    if entry["has_transcript"] == "Y":
        score += 20
    if entry["has_analysis"] == "Y":
        score += 10
    if entry["has_prompt"] == "Y":
        score += 15
    if entry["has_artwork"] == "Y":
        score += 10
    if entry["genre"]:
        score += 5
    entry["completeness_score"] = score

    # Status
    if score >= 85:
        entry["status"] = "COMPLETE"
    elif score >= 60:
        entry["status"] = "GOOD"
    elif score >= 40:
        entry["status"] = "PARTIAL"
    else:
        entry["status"] = "NEEDS_WORK"

    return entry


def main():
    print("=" * 80)
    print("ENHANCED MASTER CATALOG - DEEP SCAN")
    print("=" * 80)
    print("Loading existing data sources...\n")

    # Load existing metadata
    existing_metadata = load_existing_metadata()
    print(f"? Loaded metadata for {len(existing_metadata)} files from previous scans")

    # Load bundle info
    bundle_info = load_bundle_info()
    print(f"? Loaded {len(bundle_info)} song bundles")

    # Find all MP3 files
    mp3_files = list(MUSIC_DIR.glob("**/*.mp3")) + list(MUSIC_DIR.glob("**/*.MP3"))
    mp3_files = [f for f in mp3_files if "SONG_BUNDLES" not in f.parts]
    mp3_files.sort()

    print(f"? Found {len(mp3_files)} MP3 files\n")
    print("Processing files with deep scan...\n")

    # Create catalog entries
    catalog = []

    for i, mp3_file in enumerate(mp3_files, 1):
        entry = create_catalog_entry(mp3_file, existing_metadata, bundle_info)
        catalog.append(entry)

        if i % 50 == 0:
            print(f"  Processed {i}/{len(mp3_files)} files...")

    print(f"  Processed {len(mp3_files)}/{len(mp3_files)} files... Done!\n")

    # Write CSV
    fieldnames = [
        "filename",
        "file_path",
        "full_path",
        "album_folder",
        "title",
        "artist",
        "album",
        "genre",
        "style",
        "mood",
        "duration_formatted",
        "duration_seconds",
        "file_size_mb",
        "bitrate_kbps",
        "sample_rate",
        "content_type",
        "has_transcript",
        "has_analysis",
        "has_lyrics",
        "has_prompt",
        "has_artwork",
        "transcript_count",
        "analysis_count",
        "transcript_files",
        "analysis_files",
        "completeness_score",
        "status",
    ]

    DATA_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(catalog)

    # Generate statistics
    print("=" * 80)
    print("COMPREHENSIVE STATISTICS")
    print("=" * 80)

    total_duration = sum(e["duration_seconds"] for e in catalog)
    total_size = sum(e["file_size_mb"] for e in catalog)

    albums = defaultdict(int)
    for e in catalog:
        albums[e["album_folder"]] += 1

    with_transcripts = sum(1 for e in catalog if e["has_transcript"] == "Y")
    with_analysis = sum(1 for e in catalog if e["has_analysis"] == "Y")
    with_lyrics = sum(1 for e in catalog if e["has_lyrics"] == "Y")
    with_prompts = sum(1 for e in catalog if e["has_prompt"] == "Y")
    with_artwork = sum(1 for e in catalog if e["has_artwork"] == "Y")

    status_counts = defaultdict(int)
    for e in catalog:
        status_counts[e["status"]] += 1

    content_types = defaultdict(int)
    for e in catalog:
        content_types[e["content_type"]] += 1

    # Print summary
    print("\nCOLLECTION OVERVIEW:")
    print(f"  Total MP3 files: {len(catalog)}")
    print(f"  Total albums/folders: {len(albums)}")
    print(
        f"  Total duration: {total_duration // 3600}h {(total_duration % 3600) // 60}m {total_duration % 60}s",
    )
    print(f"  Total size: {total_size:.2f} MB ({total_size / 1024:.2f} GB)")

    print("\nCONTENT COVERAGE:")
    print(
        f"  Files with transcripts: {with_transcripts:3d} ({with_transcripts * 100 / len(catalog):5.1f}%)",
    )
    print(
        f"  Files with analysis: {with_analysis:3d} ({with_analysis * 100 / len(catalog):5.1f}%)",
    )
    print(
        f"  Files with lyrics: {with_lyrics:3d} ({with_lyrics * 100 / len(catalog):5.1f}%)",
    )
    print(
        f"  Files with prompts: {with_prompts:3d} ({with_prompts * 100 / len(catalog):5.1f}%)",
    )
    print(
        f"  Files with artwork: {with_artwork:3d} ({with_artwork * 100 / len(catalog):5.1f}%)",
    )

    print("\nCOMPLETENESS STATUS:")
    for status in ["COMPLETE", "GOOD", "PARTIAL", "NEEDS_WORK"]:
        count = status_counts[status]
        print(f"  {status:12s}: {count:3d} ({count * 100 / len(catalog):5.1f}%)")

    print("\nCONTENT TYPES:")
    for ctype in sorted(content_types.keys()):
        count = content_types[ctype]
        print(f"  {ctype:12s}: {count:3d} ({count * 100 / len(catalog):5.1f}%)")

    print("\nTOP 10 ALBUMS (by track count):")
    for album, count in sorted(albums.items(), key=lambda x: x[1], reverse=True)[:10]:
        album_tracks = [e for e in catalog if e["album_folder"] == album]
        album_duration = sum(e["duration_seconds"] for e in album_tracks)
        print(f"  {album:40s}: {count:3d} tracks, {album_duration // 60:3d}m")

    print(f"\n{'=' * 80}")
    print(f"? Enhanced master catalog saved to: {OUTPUT_CSV}")

    # Save summary to file
    with open(OUTPUT_SUMMARY, "w", encoding="utf-8") as f:
        f.write("nocTurneMeLoDieS - Enhanced Master Catalog Summary\n")
        f.write("=" * 80 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("COLLECTION OVERVIEW:\n")
        f.write(f"  Total MP3 files: {len(catalog)}\n")
        f.write(f"  Total albums/folders: {len(albums)}\n")
        f.write(
            f"  Total duration: {total_duration // 3600}h {(total_duration % 3600) // 60}m\n",
        )
        f.write(f"  Total size: {total_size:.2f} MB ({total_size / 1024:.2f} GB)\n\n")

        f.write("CONTENT COVERAGE:\n")
        f.write(
            f"  Files with transcripts: {with_transcripts} ({with_transcripts * 100 / len(catalog):.1f}%)\n",
        )
        f.write(
            f"  Files with analysis: {with_analysis} ({with_analysis * 100 / len(catalog):.1f}%)\n",
        )
        f.write(
            f"  Files with lyrics: {with_lyrics} ({with_lyrics * 100 / len(catalog):.1f}%)\n",
        )
        f.write(
            f"  Files with prompts: {with_prompts} ({with_prompts * 100 / len(catalog):.1f}%)\n",
        )
        f.write(
            f"  Files with artwork: {with_artwork} ({with_artwork * 100 / len(catalog):.1f}%)\n\n",
        )

        f.write("ALL ALBUMS:\n")
        for album, count in sorted(albums.items(), key=lambda x: x[1], reverse=True):
            album_tracks = [e for e in catalog if e["album_folder"] == album]
            album_duration = sum(e["duration_seconds"] for e in album_tracks)
            f.write(f"  ? {album} ({count} tracks, {album_duration // 60}m)\n")

    print(f"? Summary saved to: {OUTPUT_SUMMARY}\n")


if __name__ == "__main__":
    main()
