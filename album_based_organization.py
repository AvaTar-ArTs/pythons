#!/usr/bin/env python3
"""
Album-Based Organization for nocTurneMeLoDieS
Groups all versions of the same song into album directories
"""

import re
import shutil
from datetime import datetime
from pathlib import Path


def normalize_song_title(title):
    """Normalize song titles to identify the same song across different versions/remixes"""
    # Remove file extension
    name = Path(title).stem

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

    # Remove emoji prefixes
    name = re.sub(r"^[\U0001F300-\U0001F9FF\U00002600-\U000027BF🎵🔔⭐️✨💯🙂🇧🇷]+\s*", "", name)

    # Normalize apostrophes and special characters
    name = name.replace("’", "'").replace("‘", "'").replace("`", "'")

    # Replace common separators with spaces
    name = name.replace("_", " ").replace("-", " ").replace(".", " ")

    # Remove version indicators and numbers
    for indicator in version_indicators:
        # Use word boundaries to avoid partial matches
        name = re.sub(r"\b" + re.escape(indicator) + r"\b", "", name, flags=re.IGNORECASE)

    # Remove extra whitespace and digits
    name = re.sub(r"\s+", " ", name)
    name = re.sub(r"\d+", "", name)

    # Remove extra spaces again after digit removal
    name = name.strip()

    return name.strip()


def identify_albums():
    """Identify all unique albums based on normalized song titles"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")
    albums = {}

    # Find all MP3 files in the directory and subdirectories
    for mp3_file in base_path.rglob("*.mp3"):
        if "MUSIC_ALBUMS" in str(mp3_file):  # Skip if already in organized structure
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
    album_dir = base_path / "MUSIC_ALBUMS"
    album_dir.mkdir(exist_ok=True)

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


def organize_remaining_content():
    """Organize remaining content into appropriate categories"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")

    # Create supporting directories
    support_dirs = [
        "MUSIC_ALBUMS/COVER_ART",
        "MUSIC_ALBUMS/LYRICS",
        "MUSIC_ALBUMS/ANALYSIS",
        "MUSIC_ALBUMS/TRANSCRIPTS",
        "MUSIC_ALBUMS/OTHER_MISC",
    ]

    for dir_path in support_dirs:
        (base_path / dir_path).mkdir(parents=True, exist_ok=True)

    # Move non-MP3 files to appropriate locations
    moved_support = 0
    failed_support = 0

    # Find all non-MP3 files that are music-related
    for item in base_path.rglob("*"):
        if item.is_file() and item.parent.name != "MUSIC_ALBUMS":
            if item.suffix.lower() in [
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".svg",
                ".webp",
            ]:
                # Image files (likely cover art)
                target_dir = base_path / "MUSIC_ALBUMS" / "COVER_ART"
                target_file = target_dir / item.name
                counter = 1
                while target_file.exists():
                    stem = item.stem
                    suffix = item.suffix
                    target_file = target_dir / f"{stem}_{counter}{suffix}"
                    counter += 1
                try:
                    shutil.move(str(item), str(target_file))
                    print(f"  ✓ Moved image: {item.name}")
                    moved_support += 1
                except Exception as e:
                    print(f"  ✗ Failed to move image {item.name}: {str(e)}")
                    failed_support += 1

            elif item.suffix.lower() in [".txt", ".md"] and any(
                keyword in item.name.lower() for keyword in ["lyrics", "transcript", "analysis"]
            ):
                # Lyrics, transcripts, or analysis files
                if "lyrics" in item.name.lower():
                    target_dir = base_path / "MUSIC_ALBUMS" / "LYRICS"
                elif "transcript" in item.name.lower():
                    target_dir = base_path / "MUSIC_ALBUMS" / "TRANSCRIPTS"
                else:
                    target_dir = base_path / "MUSIC_ALBUMS" / "ANALYSIS"

                target_file = target_dir / item.name
                counter = 1
                while target_file.exists():
                    stem = item.stem
                    suffix = item.suffix
                    target_file = target_dir / f"{stem}_{counter}{suffix}"
                    counter += 1
                try:
                    shutil.move(str(item), str(target_file))
                    print(f"  ✓ Moved text: {item.name}")
                    moved_support += 1
                except Exception as e:
                    print(f"  ✗ Failed to move text {item.name}: {str(e)}")
                    failed_support += 1

    return moved_support, failed_support


def main():
    print("Starting album-based organization of nocTurneMeLoDieS music collection...")
    print("=" * 70)

    # Identify all albums
    print("Identifying albums from MP3 files...")
    albums = identify_albums()
    print(f"Found {len(albums)} unique albums")

    # Create album structure
    album_dir = create_album_structure(albums)

    # Move files to albums
    moved_files, failed_files = move_files_to_albums(albums, album_dir)

    # Organize remaining content
    moved_support, failed_support = organize_remaining_content()

    # Create summary
    summary_path = album_dir / "ORGANIZATION_SUMMARY.md"
    with open(summary_path, "w") as f:
        f.write("# nocTurneMeLoDieS - ALBUM-BASED ORGANIZATION SUMMARY\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"- **Albums created**: {len(albums)}\n")
        f.write(f"- **Music files moved**: {moved_files}\n")
        f.write(f"- **Supporting files moved**: {moved_support}\n")
        f.write(f"- **Failed operations**: {failed_files + failed_support}\n\n")

        f.write("## Top Albums by File Count\n\n")
        sorted_albums = sorted(albums.items(), key=lambda x: len(x[1]), reverse=True)
        for album_name, files in sorted_albums[:20]:  # Top 20 albums
            f.write(f"- **{album_name}**: {len(files)} versions\n")

        if len(sorted_albums) > 20:
            f.write(f"\n- ... and {len(sorted_albums) - 20} more albums\n\n")

        f.write("## New Structure\n\n")
        f.write("```\n")
        f.write("MUSIC_ALBUMS/\n")
        f.write("├── [Album Name 1]/          # All versions of Album 1\n")
        f.write("├── [Album Name 2]/          # All versions of Album 2\n")
        f.write("├── [Album Name 3]/          # All versions of Album 3\n")
        f.write("├── ...\n")
        f.write("├── COVER_ART/               # All cover art\n")
        f.write("├── LYRICS/                  # All lyrics files\n")
        f.write("├── ANALYSIS/                # All analysis files\n")
        f.write("├── TRANSCRIPTS/             # All transcript files\n")
        f.write("└── OTHER_MISC/              # Other miscellaneous files\n")
        f.write("```\n\n")

        f.write("## Benefits Achieved\n\n")
        f.write("- All versions of the same song are now in one album directory\n")
        f.write("- Easy to find all variations of a particular song\n")
        f.write("- Simplified navigation compared to scattered organization\n")
        f.write("- Clear separation of music content from supporting files\n")
        f.write("- Scalable structure that grows naturally with new content\n\n")

    print(f"\n{'=' * 70}")
    print("ALBUM-BASED ORGANIZATION COMPLETED!")
    print(f"{'=' * 70}")
    print(f"Albums created: {len(albums)}")
    print(f"Music files moved: {moved_files}")
    print(f"Supporting files moved: {moved_support}")
    print(f"Failed operations: {failed_files + failed_support}")
    print(f"Summary saved to: {summary_path}")

    return {
        "albums_created": len(albums),
        "music_files_moved": moved_files,
        "supporting_files_moved": moved_support,
        "failed_operations": failed_files + failed_support,
        "summary_path": str(summary_path),
    }


if __name__ == "__main__":
    results = main()
    print(f"\nFinal Results: {results}")
