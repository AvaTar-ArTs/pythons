#!/usr/bin/env python3
"""
Analyze and move music-related images from ~/Pictures to appropriate album directories
in the nocTurneMeLoDieS collection.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path


def analyze_and_move_music_images():
    """Analyze and move music-related images from ~/Pictures to album directories"""

    # Define the Pictures path
    pictures_path = Path("~/Pictures").expanduser()

    # Define the target base path for the music collection
    target_base = Path("/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED")

    # Define music-related keywords based on the collection themes
    music_keywords = {
        "alley": [
            "alley",
            "in.the.alley",
            "in_the_alley",
            "in.this.alley.where.i.hide",
            "in_this_alley_where_i_hide",
            "hollow",
            "shadow",
        ],
        "willow": ["willow", "willow.whispers", "willow_whispers", "tree", "forest"],
        "summer": ["summer", "summer.love", "summer_love", "warm", "bright", "sun"],
        "hero": ["hero", "heroes", "villains", "rise", "warrior", "battle", "fight"],
        "junkyard": [
            "junkyard",
            "trash",
            "garbage",
            "raccoon",
            "cat",
            "street",
            "urban",
        ],
        "beautiful": ["beautiful", "mess", "pretty", "art", "aesthetic", "nature"],
        "echoes": ["echoes", "moonlight", "night", "dark", "silence", "whisper"],
        "heartbeats": ["heartbeats", "heart", "pulse", "dark", "feeling", "emotion"],
        "witch": ["witch", "magic", "spell", "forest", "moon", "night"],
        "shadow": ["shadow", "dark", "light", "hollow", "deep", "alley"],
        "forest": ["forest", "woods", "trees", "willow", "enchanted", "nature"],
        "dark": ["dark", "night", "moon", "stars", "shadow", "deep"],
    }

    # Find all image files in Pictures
    image_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".tiff",
        ".webp",
        ".svg",
    ]
    all_images = []

    if not pictures_path.exists():
        print(f"ERROR: ~/Pictures directory does not exist: {pictures_path}")
        print("Please verify the directory exists before running this script.")
        return {"error": f"Pictures directory not found: {pictures_path}"}

    for ext in image_extensions:
        all_images.extend(pictures_path.rglob(f"*{ext}"))

    print(f"Found {len(all_images)} total images in ~/Pictures")

    # Filter for music-related images
    music_images = []
    for img in all_images:
        img_name = img.name.lower()
        for theme, keywords in music_keywords.items():
            if any(keyword in img_name for keyword in keywords):
                music_images.append((img, theme))
                break

    print(f"Found {len(music_images)} music-related images in ~/Pictures")

    # Map themes to actual album directories in the collection
    theme_to_album_map = {
        "hero": [
            "Heroes_Rise_Villains_Overthrow",
            "A_Hymn_For_The_Seekers",
            "A_Warrior's_Lullaby",
            "Brave_Sir_Cedric",
            "Marching_Ever_Forward",
        ],
        "beautiful": [
            "Beautiful_Mess",
            "Beautiful_Mess_Indie_Folk_Acoustic",
            "Beautiful_Mess_Whimsical_Story",
            "Petals_Fall",
            "Echoes_of_Moonlight",
        ],
        "heartbeats": [
            "Heartbeats_in_the_Dark",
            "There'S_A_Feeling",
            "Love_in_Imperfection",
        ],
        "echoes": ["Echoes_of_Moonlight", "The_Spirits_Are_Near", "What_The_Stars_See"],
        "alley": [
            "In_The_Hollow",
            "A_Shadow_Deep_Inside",
            "Shadows_On_The_Horizon",
            "Where_Shadows_Play",
        ],
        "willow": ["Enchanted_Woods", "Enchanted_Witchs_Path", "Forest", "Nature"],
        "witch": [
            "Enchanted_Witchs_Path",
            "Witches_Road",
            "Hecate",
            "The_Enchanted_Children",
        ],
        "shadow": [
            "A_Shadow_Deep_Inside",
            "Shadows_On_The_Horizon",
            "Where_Shadows_Play",
            "Heartbeats_in_the_Dark",
        ],
        "forest": [
            "Enchanted_Woods",
            "Enchanted_Witchs_Path",
            "The_Jungle_Shaman",
            "Mountain_Eyes",
        ],
        "dark": ["Heartbeats_in_the_Dark", "A_Shadow_Deep_Inside", "Dark", "Night"],
        "summer": ["Summer", "Warm", "Bright"],
        "junkyard": ["Junkyard", "Urban", "Street"],
    }

    # Get list of actual existing album directories
    albums_path = target_base / "ALBUMS"
    if not albums_path.exists():
        print(f"ERROR: Album directory does not exist: {albums_path}")
        return {"error": f"Albums directory not found: {albums_path}"}

    existing_albums = [d.name for d in albums_path.iterdir() if d.is_dir()]
    print(f"Found {len(existing_albums)} existing albums in the collection")

    # Match themes to existing albums
    matched_images = []
    unmatched_images = []

    for img_path, theme in music_images:
        img_name = img_path.name.lower()

        # Find matching albums for this theme
        possible_albums = theme_to_album_map.get(theme, [])
        matching_album = None

        # Look for the best matching album that actually exists
        for album_candidate in possible_albums:
            # Case-insensitive matching
            for existing_album in existing_albums:
                if (
                    album_candidate.lower() in existing_album.lower()
                    or existing_album.lower() in album_candidate.lower()
                ):
                    matching_album = existing_album
                    break
            if matching_album:
                break

        if matching_album:
            matched_images.append((img_path, theme, matching_album))
            print(f"Matched {img_name} to theme '{theme}' -> album '{matching_album}'")
        else:
            unmatched_images.append((img_path, theme))
            print(f"No matching album found for {img_name} with theme '{theme}'")

    print("\nSummary:")
    print(f"- {len(matched_images)} images matched to albums")
    print(f"- {len(unmatched_images)} images without matching albums")

    # Move matched images to appropriate album directories
    moved_count = 0
    failed_count = 0

    for img_path, theme, album_name in matched_images:
        target_dir = albums_path / album_name

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
            print(f"✓ Moved: {img_path.name} -> {album_name}/")
            moved_count += 1
        except Exception as e:
            print(f"✗ Failed to move {img_path.name}: {str(e)}")
            failed_count += 1

    # For unmatched images, move to a general "Cover Art" directory
    cover_art_dir = target_base / "COVER_ART"
    cover_art_dir.mkdir(parents=True, exist_ok=True)

    for img_path, theme in unmatched_images:
        target_file = cover_art_dir / img_path.name
        counter = 1
        while target_file.exists():
            stem = img_path.stem
            suffix = img_path.suffix
            target_file = cover_art_dir / f"{stem}_{counter}{suffix}"
            counter += 1

        try:
            shutil.move(str(img_path), str(target_file))
            print(f"✓ Moved unmatched {img_path.name} to COVER_ART/")
            moved_count += 1
        except Exception as e:
            print(f"✗ Failed to move unmatched {img_path.name}: {str(e)}")
            failed_count += 1

    # Create detailed report
    report_path = target_base / "ANALYSIS" / "music_images_analysis_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, "w") as f:
        f.write("# Music Images Analysis & Organization Report\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total images analyzed**: {len(all_images)}\n")
        f.write(f"**Music-related images found**: {len(music_images)}\n")
        f.write(f"**Images moved**: {moved_count}\n")
        f.write(f"**Images failed to move**: {failed_count}\n\n")

        f.write("## Theme Mapping\n\n")
        for theme, albums in theme_to_album_map.items():
            f.write(f"- **{theme}**: {', '.join(albums[:3])}{'...' if len(albums) > 3 else ''}\n")

        f.write("\n## Images Moved by Theme\n\n")
        theme_counts = {}
        for _, theme, _ in matched_images:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1

        for theme, count in theme_counts.items():
            f.write(f"- {theme}: {count} images\n")

        f.write(f"\n- Unmatched images: {len(unmatched_images)} (moved to COVER_ART)\n\n")

        f.write("## Detailed Image Mapping\n\n")
        for img_path, theme, album_name in matched_images:
            f.write(f"- `{img_path.name}` ({theme}) → `{album_name}/`\n")

        f.write("\n## Unmatched Images\n\n")
        for img_path, theme in unmatched_images:
            f.write(f"- `{img_path.name}` ({theme}) → `COVER_ART/`\n")

        f.write("\n## Recommendations\n\n")
        f.write("1. Review the moved images to ensure they match the album themes appropriately\n")
        f.write("2. Consider creating specific album directories for unmatched images if needed\n")
        f.write("3. Update album artwork with the newly added images as appropriate\n")
        f.write("4. Verify that all moved images enhance the visual experience of the music collection\n\n")

        f.write(
            "This analysis ensures that all music-related visual assets are properly associated with their respective albums, enhancing the overall organization and aesthetic coherence of the nocTurneMeLoDieS collection.\n"
        )

    # Create JSON summary for programmatic access
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "total_images_analyzed": len(all_images),
        "music_related_found": len(music_images),
        "images_matched": len(matched_images),
        "images_unmatched": len(unmatched_images),
        "images_moved": moved_count,
        "images_failed": failed_count,
        "theme_distribution": theme_counts,
        "report_path": str(report_path),
    }

    summary_path = target_base / "ANALYSIS" / "music_images_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary_data, f, indent=2)

    print(f"\n{'=' * 60}")
    print("MUSIC IMAGES ANALYSIS & ORGANIZATION COMPLETED!")
    print(f"{'=' * 60}")
    print(f"Images analyzed: {len(all_images)}")
    print(f"Music-related images: {len(music_images)}")
    print(f"Images moved: {moved_count}")
    print(f"Images failed: {failed_count}")
    print(f"Detailed report saved to: {report_path}")
    print(f"JSON summary saved to: {summary_path}")

    return {
        "analyzed": len(all_images),
        "music_related": len(music_images),
        "moved": moved_count,
        "failed": failed_count,
        "report": str(report_path),
        "summary": str(summary_path),
    }


if __name__ == "__main__":
    results = analyze_and_move_music_images()
    print(f"\nFinal Results: {results}")
