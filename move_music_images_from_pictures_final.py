#!/usr/bin/env python3
"""
Move music-related images from ~/Pictures to appropriate album directories
"""

import shutil
from pathlib import Path


def move_music_images():
    """Move music-related images from ~/Pictures to album directories"""
    pictures_path = Path("~/Pictures").expanduser()
    target_base = Path("/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED")

    # Find all music-related images in Pictures
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
    ]

    # Find all image files in Pictures
    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"]
    all_images = []

    for ext in image_extensions:
        all_images.extend(pictures_path.rglob(f"*{ext}"))

    # Filter for music-related images
    music_images = []
    for img in all_images:
        img_name = img.name.lower()
        if any(keyword in img_name for keyword in music_keywords):
            music_images.append(img)

    print(f"Found {len(music_images)} music-related images in ~/Pictures")

    # Create mapping of images to appropriate album directories
    moved_count = 0
    failed_count = 0

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
        elif any(kw in img_name for kw in ["junkyard", "trashcat", "raccoon", "trash"]):
            target_dir = target_base / "ALBUMS" / "Junkyard_Symphony"
        elif "beautiful" in img_name and "mess" in img_name:
            target_dir = target_base / "ALBUMS" / "Beautiful_Mess"
        elif "echoes" in img_name and ("yesterday" in img_name or "alley" in img_name or "moonlight" in img_name):
            target_dir = target_base / "ALBUMS" / "Echoes_of_Yesterday"
        elif "heartbeats" in img_name and "dark" in img_name:
            target_dir = target_base / "ALBUMS" / "Heartbeats_in_the_Dark"
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
            # Move the image file
            shutil.move(str(img_path), str(target_file))
            print(f"✓ Moved: {img_path.name} -> {target_dir.name}/")
            moved_count += 1
        except Exception as e:
            print(f"✗ Failed to move {img_path.name}: {str(e)}")
            failed_count += 1

    # Create summary
    summary_path = target_base / "COVER_ART" / "music_images_moved_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    with open(summary_path, "w") as f:
        f.write("# Music Images Moved Summary\n\n")
        f.write(f"**Date**: {Path(__file__).stat().st_mtime}\n\n")
        f.write(f"**Images moved**: {moved_count}\n")
        f.write(f"**Images failed**: {failed_count}\n\n")
        f.write("## Summary of Images Moved\n\n")
        f.write(
            "Music-related images from ~/Pictures have been moved to appropriate album directories based on their content:\n\n"
        )
        f.write("- Alley-themed images moved to: `ALBUMS/In_This_Alley_Where_I_Hide/`\n")
        f.write("- Willow-themed images moved to: `ALBUMS/Willow_Whispers/`\n")
        f.write("- Summer-themed images moved to: `ALBUMS/Summer_Love/`\n")
        f.write("- Hero-themed images moved to: `ALBUMS/Heroes_Rise_Villains_Overthrow/`\n")
        f.write("- Junkyard/TrashCat-themed images moved to: `ALBUMS/Junkyard_Symphony/`\n")
        f.write("- Beautiful Mess images moved to: `ALBUMS/Beautiful_Mess/`\n")
        f.write("- Echoes-themed images moved to: `ALBUMS/Echoes_of_Yesterday/`\n")
        f.write("- Heartbeats-themed images moved to: `ALBUMS/Heartbeats_in_the_Dark/`\n")
        f.write("- Other music images moved to: `COVER_ART/`\n\n")
        f.write(
            "This consolidation ensures all music-related visual assets are properly associated with their respective albums.\n"
        )

    print(f"\n{'=' * 50}")
    print("MUSIC IMAGE CONSOLIDATION COMPLETED!")
    print(f"{'=' * 50}")
    print(f"Images moved: {moved_count}")
    print(f"Images failed: {failed_count}")
    print(f"Summary saved to: {summary_path}")

    return {"moved": moved_count, "failed": failed_count, "summary": str(summary_path)}


if __name__ == "__main__":
    results = move_music_images()
    print(f"\nFinal Results: {results}")
