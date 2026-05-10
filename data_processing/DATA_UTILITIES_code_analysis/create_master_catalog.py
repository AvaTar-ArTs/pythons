#!/usr/bin/env python3
"""from datetime import datetime
from pathlib import Path
import csv
import os

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from mutagen.mp3 import MP3
Create a comprehensive master catalog of all nocTurneMeLoDieS music.
Includes: album, song title, duration, file path, transcript status, prompt status, image status.
"""

# Configuration
MUSIC_DIR = Path("/Users/steven/Music/nocTurneMeLoDieS")
OUTPUT_CSV = MUSIC_DIR / "DATA" / "MASTER_CATALOG_COMPLETE.csv"


def get_mp3_duration(mp3_file):
    """Get duration of MP3 file in seconds."""
    try:
        audio = MP3(mp3_file)
        return int(audio.info.length)
    except:
        return 0


def format_duration(seconds):
    """Format duration as MM:SS."""
    if seconds == 0:
        return "0:00"
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"


def has_transcript(mp3_file):
    """Check if an MP3 has associated transcript files."""
    mp3_dir = mp3_file.parent
    mp3_stem = mp3_file.stem

    # Look for transcript files in same directory
    patterns = [
        f"{mp3_stem}_transcript.txt",
        f"{mp3_stem}_analysis.txt",
        f"{mp3_stem.lower()}_transcript.txt",
        f"{mp3_stem.lower()}_analysis.txt",
    ]

    for pattern in patterns:
        if (mp3_dir / pattern).exists():
            return "Y"

    # Check for any txt files with similar names
    for txt_file in mp3_dir.glob("*.txt"):
        if mp3_stem.lower() in txt_file.stem.lower():
            return "Y"

    return "N"


def has_prompt(mp3_file):
    """Check if album has prompts directory."""
    album_dir = mp3_file.parent
    prompts_dir = album_dir / "prompts"

    if prompts_dir.exists() and prompts_dir.is_dir():
        # Check if there are any prompt files
        if list(prompts_dir.glob("*.txt")):
            return "Y"

    return "N"


def has_artwork(mp3_file):
    """Check if album has images/artwork."""
    album_dir = mp3_file.parent

    # Check for common image extensions
    image_patterns = ["*.jpg", "*.jpeg", "*.png", "*.gif"]

    for pattern in image_patterns:
        if list(album_dir.glob(pattern)):
            return "Y"

        # Check images subdirectory
        images_dir = album_dir / "images"
        if images_dir.exists() and list(images_dir.glob(pattern)):
            return "Y"

    return "N"


def get_album_from_path(mp3_path):
    """Extract album name from path."""
    parts = mp3_path.parts
    try:
        music_idx = parts.index("nocTurneMeLoDieS")
        if music_idx + 1 < len(parts):
            album = parts[music_idx + 1]
            # Clean up album name
            return album.replace("_", " ").replace("-", " ")
    except ValueError:
        pass
    return "Unknown"


def catalog_mp3(mp3_file):
    """Create catalog entry for an MP3 file."""
    entry = {
        "Album": "",
        "Title": "",
        "Artist": "",
        "Duration": "",
        "Duration_Seconds": 0,
        "File_Path": str(mp3_file.relative_to(MUSIC_DIR)),
        "Full_Path": str(mp3_file),
        "Has_Transcript": "N",
        "Has_Prompt": "N",
        "Has_Artwork": "N",
        "File_Size_MB": 0,
    }

    # Get metadata
    try:
        try:
            audio = EasyID3(mp3_file)
            entry["Title"] = (
                audio.get("title", [""])[0] if "title" in audio else mp3_file.stem
            )
            entry["Artist"] = audio.get("artist", [""])[0] if "artist" in audio else ""
            entry["Album"] = (
                audio.get("album", [""])[0]
                if "album" in audio
                else get_album_from_path(mp3_file)
            )
        except ID3NoHeaderError:
            entry["Title"] = mp3_file.stem
            entry["Album"] = get_album_from_path(mp3_file)
    except Exception:
        entry["Title"] = mp3_file.stem
        entry["Album"] = get_album_from_path(mp3_file)

    # Get duration
    duration_seconds = get_mp3_duration(mp3_file)
    entry["Duration_Seconds"] = duration_seconds
    entry["Duration"] = format_duration(duration_seconds)

    # Get file size
    try:
        file_size_bytes = mp3_file.stat().st_size
        entry["File_Size_MB"] = round(file_size_bytes / (1024 * 1024), 2)
    except:
        pass

    # Check for associated files
    entry["Has_Transcript"] = has_transcript(mp3_file)
    entry["Has_Prompt"] = has_prompt(mp3_file)
    entry["Has_Artwork"] = has_artwork(mp3_file)

    return entry


def main():
    print("=" * 80)
    print("CREATING MASTER CATALOG")
    print("=" * 80)
    print(f"Output: {OUTPUT_CSV}\n")

    # Find all MP3 files
    mp3_files = list(MUSIC_DIR.glob("**/*.mp3")) + list(MUSIC_DIR.glob("**/*.MP3"))

    # Exclude SONG_BUNDLES
    mp3_files = [f for f in mp3_files if "SONG_BUNDLES" not in f.parts]

    # Sort by path
    mp3_files.sort()

    print(f"Found {len(mp3_files)} MP3 files\n")
    print("Processing files...")

    # Catalog all files
    catalog_entries = []

    for i, mp3_file in enumerate(mp3_files, 1):
        entry = catalog_mp3(mp3_file)
        catalog_entries.append(entry)

        if i % 50 == 0:
            print(f"  Processed {i}/{len(mp3_files)} files...")

    print(f"  Processed {len(mp3_files)}/{len(mp3_files)} files... Done!\n")

    # Write CSV
    OUTPUT_CSV.parent.mkdir(exist_ok=True)

    fieldnames = [
        "Album",
        "Title",
        "Artist",
        "Duration",
        "Duration_Seconds",
        "File_Path",
        "Full_Path",
        "Has_Transcript",
        "Has_Prompt",
        "Has_Artwork",
        "File_Size_MB",
    ]

    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(catalog_entries)

    # Generate statistics
    total_duration = sum(e["Duration_Seconds"] for e in catalog_entries)
    total_size = sum(e["File_Size_MB"] for e in catalog_entries)

    albums = set(e["Album"] for e in catalog_entries)
    with_transcripts = sum(1 for e in catalog_entries if e["Has_Transcript"] == "Y")
    with_prompts = sum(1 for e in catalog_entries if e["Has_Prompt"] == "Y")
    with_artwork = sum(1 for e in catalog_entries if e["Has_Artwork"] == "Y")

    # Print summary
    print("=" * 80)
    print("CATALOG SUMMARY")
    print("=" * 80)
    print(f"Total MP3 files: {len(catalog_entries)}")
    print(f"Unique albums: {len(albums)}")
    print(
        f"Total duration: {format_duration(total_duration)} ({total_duration // 3600}h {(total_duration % 3600) // 60}m)",
    )
    print(f"Total size: {total_size:.2f} MB ({total_size / 1024:.2f} GB)")
    print()
    print("Content Coverage:")
    print(
        f"  Files with transcripts: {with_transcripts} ({with_transcripts * 100 / len(catalog_entries):.1f}%)",
    )
    print(
        f"  Files with prompts: {with_prompts} ({with_prompts * 100 / len(catalog_entries):.1f}%)",
    )
    print(
        f"  Files with artwork: {with_artwork} ({with_artwork * 100 / len(catalog_entries):.1f}%)",
    )
    print()
    print(f"Catalog saved to: {OUTPUT_CSV}")
    print("\n? Master catalog complete!")

    # Create summary file
    summary_file = MUSIC_DIR / "DATA" / "CATALOG_SUMMARY.txt"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("nocTurneMeLoDieS - Master Catalog Summary\n")
        f.write("=" * 80 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total MP3 files: {len(catalog_entries)}\n")
        f.write(f"Unique albums: {len(albums)}\n")
        f.write(
            f"Total duration: {format_duration(total_duration)} ({total_duration // 3600}h {(total_duration % 3600) // 60}m)\n",
        )
        f.write(f"Total size: {total_size:.2f} MB ({total_size / 1024:.2f} GB)\n\n")
        f.write("Content Coverage:\n")
        f.write(
            f"  Files with transcripts: {with_transcripts} ({with_transcripts * 100 / len(catalog_entries):.1f}%)\n",
        )
        f.write(
            f"  Files with prompts: {with_prompts} ({with_prompts * 100 / len(catalog_entries):.1f}%)\n",
        )
        f.write(
            f"  Files with artwork: {with_artwork} ({with_artwork * 100 / len(catalog_entries):.1f}%)\n\n",
        )
        f.write("Album List:\n")
        for album in sorted(albums):
            album_files = [e for e in catalog_entries if e["Album"] == album]
            album_duration = sum(e["Duration_Seconds"] for e in album_files)
            f.write(
                f"  ? {album} ({len(album_files)} tracks, {format_duration(album_duration)})\n",
            )

    print(f"\nSummary also saved to: {summary_file}")


if __name__ == "__main__":
    main()
