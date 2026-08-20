"""
nocTurneMeLoDieS V1 - Basic Album-Based Organization
Foundation version: Basic album organization where each song becomes its own album
"""

import logging
import re
import shutil
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def normalize_song_title(title):
    """Normalize song titles to identify the same song across different versions/remixes"""
    # Remove file extension
    name = Path(title).stem

    # Remove emoji prefixes
    name = re.sub(r"^[\U0001F300-\U0001F9FF\U00002600-\U000027BF🎵🔔⭐️✨💯🙂🇧🇷]+\s*", "", name)

    # Normalize apostrophes and special characters
    name = name.replace("’", "'").replace("‘", "'").replace("`", "'")

    # Replace common separators with spaces
    name = name.replace("_", " ").replace("-", " ").replace(".", " ")

    # Remove common suffixes/prefixes that indicate versions
    version_indicators = [
        "remix",
        "remastered",
        "live",
        "acoustic",
        "instrumental",
        "duo",
        "v4",
        "v3",
        "v2",
        "v1",
        "edit",
        "extended",
        "short",
        "long",
        "original",
        "cover",
        "acapella",
        "remix",
        "remixes",
        "remixing",
        "version",
        "alt",
        "alternative",
        "demo",
        "studio",
        "radio",
        "extended",
        "extended_mix",
        "radio_edit",
        "album_version",
        "single_version",
        "feat",
        "ft",
        "with",
        "prod",
        "producer",
        "original_mix",
        "radio_cut",
        "club_mix",
        "unplugged",
        "reprise",
        "reprise_version",
        "acoustic_version",
        "live_version",
        "studio_version",
        "orchestral",
        "symphonic",
        "piano",
        "guitar",
        "vocal",
        "vocal_version",
        "clean",
        "clean_version",
        "dirty",
        "explicit",
        "explicit_version",
        "clean_radio",
        "radio_version",
        "master",
        "mastered",
        "mastered_version",
        "master_version",
        "re_mastered",
        "re_master",
        "master_remix",
        "master_version",
        "re_mastered_version",
        "re_master_version",
        "mastered_version",
        "master_version",
        "master_remix",
        "re_mastered_remix",
        "re_master_remix",
        "mastered_remix",
        "master_remix_version",
        "re_mastered_remix_version",
        "re_master_remix_version",
        "mastered_remix_version",
        "master_remix_version",
    ]

    # Remove version indicators
    for indicator in version_indicators:
        # Use word boundaries to avoid partial matches
        name = re.sub(r"\b" + re.escape(indicator) + r"\b", "", name, flags=re.IGNORECASE)

    # Remove extra whitespace and digits
    name = re.sub(r"\s+", " ", name)
    name = re.sub(r"\d+", "", name)

    return name.strip()


def identify_albums():
    """Identify all unique albums based on normalized song titles"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")
    albums = {}

    # Find all MP3 files in the directory and subdirectories
    for mp3_file in base_path.rglob("*.mp3"):
        if "MUSIC_ORGANIZED" in str(mp3_file):  # Skip if already in organized structure
            continue

        original_name = mp3_file.name
        normalized_title = normalize_song_title(original_name).lower()

        # Create album directory name
        album_name = (
            normalized_title.replace(" ", "_")
            .replace("'", "")
            .replace('"', "")
            .replace("(", "")
            .replace(")", "")
            .replace("[", "")
            .replace("]", "")
            .replace(",", "")
            .replace("&", "and")
            .strip("_")
        )

        if album_name not in albums:
            albums[album_name] = []
        albums[album_name].append(mp3_file)

    return albums


def create_album_structure(albums):
    """Create the album-based directory structure"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")
    album_dir = base_path / "MUSIC_ORGANIZED" / "ALBUMS"
    album_dir.mkdir(parents=True, exist_ok=True)

    print(f"Creating album structure for {len(albums)} unique albums...")

    for album_name, files in albums.items():
        album_path = album_dir / album_name
        album_path.mkdir(exist_ok=True)
        print(f"  Created album: {album_name} ({len(files)} files)")

    return album_dir


def move_files_to_albums(albums, album_dir):
    """Move files to their respective album directories"""
    moved_count = 0
    failed_count = 0

    print("\nMoving files to album directories...")

    for album_name, files in albums.items():
        album_path = album_dir / album_name

        for file_path in files:
            target_file = album_path / file_path.name

            # Handle potential naming conflicts
            counter = 1
            while target_file.exists():
                stem = file_path.stem
                suffix = file_path.suffix
                target_file = album_path / f"{stem}_{counter}{suffix}"
                counter += 1

            try:
                shutil.move(str(file_path), str(target_file))
                print(f"    ✓ Moved: {file_path.name}")
                moved_count += 1
            except Exception as e:
                print(f"    ✗ Failed to move {file_path.name}: {str(e)}")
                failed_count += 1

    return moved_count, failed_count


def organize_music_collection():
    """Main function to organize the music collection"""
    print("nocTurneMeLoDieS V1 - Basic Album-Based Organization")
    print("=" * 55)

    start_time = datetime.now()

    # Identify albums
    print("\nStep 1: Identifying albums from MP3 files...")
    albums = identify_albums()
    print(f"Found {len(albums)} unique albums")

    # Create album structure
    print("\nStep 2: Creating album directory structure...")
    album_dir = create_album_structure(albums)

    # Move files to albums
    print("\nStep 3: Moving files to album directories...")
    moved_files, failed_files = move_files_to_albums(albums, album_dir)

    # Create summary
    end_time = datetime.now()
    duration = end_time - start_time

    summary = {
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "duration_seconds": duration.total_seconds(),
        "albums_created": len(albums),
        "files_moved": moved_files,
        "files_failed": failed_files,
        "success_rate": ((moved_files / (moved_files + failed_files)) * 100 if (moved_files + failed_files) > 0 else 0),
    }

    # Save summary to file
    summary_path = album_dir / "ORGANIZATION_SUMMARY_V1.json"
    import json

    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n{'=' * 55}")
    print("BASIC ALBUM-BASED ORGANIZATION COMPLETED!")
    print(f"{'=' * 55}")
    print(f"Albums created: {summary['albums_created']}")
    print(f"Files moved: {summary['files_moved']}")
    print(f"Failed operations: {summary['files_failed']}")
    print(f"Success rate: {summary['success_rate']:.1f}%")
    print(f"Duration: {summary['duration_seconds']:.1f} seconds")
    print(f"Summary saved to: {summary_path}")

    return summary


if __name__ == "__main__":
    results = organize_music_collection()
    print(f"\nFinal Results: {results}")
