#!/usr/bin/env python3
"""
Move music-related files from /Volumes to appropriate album directories
"""

import shutil
from pathlib import Path


def move_volume_music():
    """Move music-related files from /Volumes to album directories"""
    volumes_path = Path("/Volumes")
    target_base = Path("/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED")

    # Find all music-related files in Volumes
    music_keywords = [
        "alley",
        "willow",
        "summer",
        "hero",
        "junkyard",
        "trashcat",
        "beautiful",
        "echoes",
        "heartbeats",
        "in.this.alley",
        "summer.love",
        "willow.whispers",
        "in_the_alley",
        "willow_whispers",
        "summer_love",
        "heroes",
        "villains",
        "junkyard",
        "raccoon",
        "trash",
        "beautiful_mess",
        "echoes_of",
        "heartbeats_in",
        "in.this.alley.where.i.hide",
        "in_this_alley_where_i_hide",
        "willow_whispers",
        "heroes_rise_villains_overthrow",
        "junkyard_symphony",
        "summer_love",
        "bite.in.the.night",
        "heavenly.hands",
        "dr.adu",
        "trashcats",
    ]

    # Find all audio files in Volumes
    audio_extensions = [".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg", ".opus"]
    all_audio = []

    for ext in audio_extensions:
        try:
            all_audio.extend(volumes_path.rglob(f"*{ext}"))
        except PermissionError:
            continue  # Skip directories we don't have permission to access

    # Filter for music-related audio files
    music_audio = []
    for audio_file in all_audio:
        audio_name = audio_file.name.lower()
        if any(keyword in audio_name for keyword in music_keywords):
            music_audio.append(audio_file)

    print(f"Found {len(music_audio)} music-related audio files in /Volumes")

    # Create mapping of files to appropriate album directories
    moved_count = 0
    failed_count = 0

    for audio_path in music_audio:
        audio_name = audio_path.name.lower()

        # Determine target album directory based on file name
        if any(
            kw in audio_name
            for kw in [
                "alley",
                "in.the.alley",
                "in_the_alley",
                "in.this.alley.where.i.hide",
                "in_this_alley_where_i_hide",
                "heartbreak.alley",
            ]
        ):
            target_dir = target_base / "ALBUMS" / "In_This_Alley_Where_I_Hide"
        elif any(
            kw in audio_name
            for kw in [
                "willow",
                "willow.whispers",
                "willow_whispers",
                "whisper.of.the.willow",
            ]
        ):
            target_dir = target_base / "ALBUMS" / "Willow_Whispers"
        elif any(kw in audio_name for kw in ["summer", "summer.love", "summer_love"]):
            target_dir = target_base / "ALBUMS" / "Summer_Love"
        elif any(kw in audio_name for kw in ["hero", "heroes", "villains", "heroes.rise"]):
            target_dir = target_base / "ALBUMS" / "Heroes_Rise_Villains_Overthrow"
        elif any(
            kw in audio_name
            for kw in [
                "junkyard",
                "trashcat",
                "raccoon",
                "trash",
                "junkyard.kings",
                "junkyard.symphony",
                "recycled.symphony",
            ]
        ):
            target_dir = target_base / "ALBUMS" / "Junkyard_Symphony"
        elif "beautiful" in audio_name and "mess" in audio_name:
            target_dir = target_base / "ALBUMS" / "Beautiful_Mess"
        elif "echoes" in audio_name and (
            "yesterday" in audio_name or "alley" in audio_name or "moonlight" in audio_name or "moonlit" in audio_name
        ):
            target_dir = target_base / "ALBUMS" / "Echoes_of_Yesterday"
        elif "heartbeats" in audio_name and "dark" in audio_name:
            target_dir = target_base / "ALBUMS" / "Heartbeats_in_the_Dark"
        elif "bite" in audio_name and "night" in audio_name:
            target_dir = target_base / "ALBUMS" / "Bite_In_The_Night"
        elif "trashcats" in audio_name:
            target_dir = target_base / "ALBUMS" / "Junkyard_Symphony"
        else:
            # For other music-related files, put in general singles
            target_dir = target_base / "ALBUMS" / "OTHER_THEMES"

        # Create target directory if it doesn't exist
        target_dir.mkdir(parents=True, exist_ok=True)

        # Handle potential filename conflicts
        target_file = target_dir / audio_path.name
        counter = 1
        while target_file.exists():
            stem = audio_path.stem
            suffix = audio_path.suffix
            target_file = target_dir / f"{stem}_{counter}{suffix}"
            counter += 1

        try:
            # Copy the audio file (since it might be on a mounted volume)
            shutil.copy2(str(audio_path), str(target_file))
            print(f"✓ Copied: {audio_path.name} -> {target_dir.name}/")
            moved_count += 1
        except Exception as e:
            print(f"✗ Failed to copy {audio_path.name}: {str(e)}")
            failed_count += 1

    # Also look for related image files in Volumes
    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"]
    all_images = []

    for ext in image_extensions:
        try:
            all_images.extend(volumes_path.rglob(f"*{ext}"))
        except PermissionError:
            continue

    # Filter for music-related images
    music_images = []
    for img in all_images:
        img_name = img.name.lower()
        if any(keyword in img_name for keyword in music_keywords):
            music_images.append(img)

    print(f"Found {len(music_images)} music-related images in /Volumes")

    # Move music-related images
    for img_path in music_images:
        img_name = img_path.name.lower()

        # Determine target album directory based on image name
        if any(
            kw in img_name
            for kw in [
                "alley",
                "in.the.alley",
                "in_the_alley",
                "in.this.alley.where.i.hide",
                "in_this_alley_where_i_hide",
            ]
        ):
            target_dir = target_base / "ALBUMS" / "In_This_Alley_Where_I_Hide"
        elif any(kw in img_name for kw in ["willow", "willow.whispers", "willow_whispers"]):
            target_dir = target_base / "ALBUMS" / "Willow_Whispers"
        elif any(kw in img_name for kw in ["summer", "summer.love", "summer_love"]):
            target_dir = target_base / "ALBUMS" / "Summer_Love"
        elif any(kw in img_name for kw in ["hero", "heroes", "villains"]):
            target_dir = target_base / "ALBUMS" / "Heroes_Rise_Villains_Overthrow"
        elif any(kw in img_name for kw in ["junkyard", "trashcat", "raccoon", "trash", "trashcats"]):
            target_dir = target_base / "ALBUMS" / "Junkyard_Symphony"
        elif "beautiful" in img_name and "mess" in img_name:
            target_dir = target_base / "ALBUMS" / "Beautiful_Mess"
        elif "echoes" in img_name and ("yesterday" in img_name or "alley" in img_name or "moonlight" in img_name):
            target_dir = target_base / "ALBUMS" / "Echoes_of_Yesterday"
        elif "heartbeats" in img_name and "dark" in img_name:
            target_dir = target_base / "ALBUMS" / "Heartbeats_in_the_Dark"
        elif "bite" in img_name and "night" in img_name:
            target_dir = target_base / "ALBUMS" / "Bite_In_The_Night"
        else:
            # For other music-related images, put in general cover art
            target_dir = target_base / "COVER_ART"

        # Create target directory if it doesn't exist
        target_dir.mkdir(parents=True, exist_ok=True)

        # Handle potential filename conflicts
        target_file = target_dir / img_path.name
        counter = 1
        while target_file.exists():
            stem = img_path.stem
            suffix = img_path.suffix
            target_file = target_dir / f"{stem}_{counter}{suffix}"
            counter += 1

        try:
            # Copy the image file
            shutil.copy2(str(img_path), str(target_file))
            print(f"✓ Copied: {img_path.name} -> {target_dir.name}/")
            moved_count += 1
        except Exception as e:
            print(f"✗ Failed to copy {img_path.name}: {str(e)}")
            failed_count += 1

    # Create summary
    summary_path = target_base / "COVER_ART" / "volume_music_moved_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    with open(summary_path, "w") as f:
        f.write("# Volume Music Moved Summary\n\n")
        f.write(f"**Date**: {Path(__file__).stat().st_mtime}\n\n")
        f.write(f"**Files moved**: {moved_count}\n")
        f.write(f"**Files failed**: {failed_count}\n\n")
        f.write("## Summary of Files Moved\n\n")
        f.write(
            "Music-related files from /Volumes have been moved to appropriate album directories based on their content:\n\n"
        )
        f.write("- Alley-themed files moved to: `ALBUMS/In_This_Alley_Where_I_Hide/`\n")
        f.write("- Willow-themed files moved to: `ALBUMS/Willow_Whispers/`\n")
        f.write("- Summer-themed files moved to: `ALBUMS/Summer_Love/`\n")
        f.write("- Hero-themed files moved to: `ALBUMS/Heroes_Rise_Villains_Overthrow/`\n")
        f.write("- Junkyard/TrashCat-themed files moved to: `ALBUMS/Junkyard_Symphony/`\n")
        f.write("- Beautiful Mess files moved to: `ALBUMS/Beautiful_Mess/`\n")
        f.write("- Echoes-themed files moved to: `ALBUMS/Echoes_of_Yesterday/`\n")
        f.write("- Heartbeats-themed files moved to: `ALBUMS/Heartbeats_in_the_Dark/`\n")
        f.write("- Bite in the Night files moved to: `ALBUMS/Bite_In_The_Night/`\n")
        f.write("- Other music files moved to: `ALBUMS/OTHER_THEMES/`\n\n")
        f.write(
            "This consolidation ensures all music-related content from external volumes is properly associated with their respective albums.\n"
        )

    print(f"\n{'=' * 50}")
    print("VOLUME MUSIC CONSOLIDATION COMPLETED!")
    print(f"{'=' * 50}")
    print(f"Files moved: {moved_count}")
    print(f"Files failed: {failed_count}")
    print(f"Summary saved to: {summary_path}")

    return {"moved": moved_count, "failed": failed_count, "summary": str(summary_path)}


if __name__ == "__main__":
    results = move_volume_music()
    print(f"\nFinal Results: {results}")
