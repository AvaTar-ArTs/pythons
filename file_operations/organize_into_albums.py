#!/usr/bin/env python3
"""from collections import defaultdict
from pathlib import Path
import csv
import re
import shutil
?? ORGANIZE SUNO COLLECTION INTO ALBUMS
Analyze content, rename, and sort 349 MP3s into proper album folders
"""


def extract_base_title(filename: str) -> str:
    """Extract base song title from filename"""
    # Remove common patterns
    name = filename

    # Remove duration codes (_234, _359)
    name = re.sub(r"_\d{3}(?:$|[^0-9])", "", name)

    # Remove version numbers
    name = re.sub(
        r"[_-]?(Remastered|Remix|Edit|Cover|Live|Extended?)",
        "",
        name,
        flags=re.IGNORECASE,
    )
    name = re.sub(r"[_\(]\d+[_\)]", "", name)  # (_1), _2, etc
    name = re.sub(r"\d+$", "", name)  # Trailing numbers

    # Remove tags in brackets/parens
    name = re.sub(r"\[.*?\]", "", name)
    name = re.sub(r"\(.*?\)", "", name)

    # Clean up
    name = name.replace("_", " ").replace("-", " ")
    name = re.sub(r"\s+", " ", name).strip()

    return name


def classify_song(filename: str, metadata: dict) -> dict:
    """Classify song into album/series"""
    base_title = extract_base_title(filename)

    # Define album patterns
    albums = {
        "In_This_Alley": [
            r"in\s*this\s*alley",
            r"alley\s*songs",
            r"alley\s*king",
            r"moonly.*alley",
        ],
        "Love_Is_Rubbish": [
            r"love.*rubbish",
            r"rubbish.*love",
            r"trash.*revolution",
            r"trashy",
            r"get\s*trashy",
        ],
        "Heartbeats": [
            r"heartbeat",
            r"heart.*dark",
        ],
        "Bite_In_The_Night": [
            r"bite.*night",
        ],
        "Junkyard_Symphony": [
            r"junkyard",
        ],
        "Willow_Whispers": [
            r"willow\s*whisper",
        ],
        "Feather_Fang": [
            r"feather\s*fang",
            r"spirit\s*sang",
            r"spirits.*near",
            r"vine.*void",
            r"i\s*became",
        ],
        "PeTals_FaLL": [
            r"petals?\s*fall",
            r"roots?\s*remain",
        ],
        "Summer_Love": [
            r"summer\s*love",
        ],
        "Heroes_Rise": [
            r"heroes?\s*rise",
            r"villains?\s*overthrow",
        ],
        "Kings_And_Queens": [
            r"kings?\s*(and|&)\s*queens?",
            r"litter",
        ],
        "Book_Of_Memory": [
            r"book.*memory",
            r"heartland",
            r"forgotten.*hearts",
        ],
        "Blues_Collection": [
            r"blues.*alley",
            r"blues.*moonlit",
            r"midnight.*reckoning",
            r"sammy.*blues",
            r"sammys.*serenade",
        ],
        "Echoes_And_Shadows": [
            r"echoes?.*moonlight",
            r"echoes?.*yesterday",
            r"shadows?.*horizon",
            r"shadows?.*messages",
            r"shadows?.*purge",
        ],
        "Heavenly_Hands": [
            r"heavenly.*hands",
        ],
        "Workshop_Series": [
            r"workshop.*worries",
            r"tapestry.*tyranny",
        ],
        "Covers": [
            r"rocket\s*man",
            r"adele",
            r"billie",
            r"cover",
        ],
        "Rituals_And_Mystical": [
            r"threaded.*veil",
            r"enchanted.*",
            r"witches?\s*road",
            r"chamber.*silence",
            r"drink.*me",
            r"ritual",
            r"mystic",
        ],
        "Dance_And_Movement": [
            r"dance.*like",
            r"dancing.*veil",
        ],
        "Nature_Themes": [
            r"desert",
            r"garden",
            r"golden\s*roots",
        ],
        "Philosophical": [
            r"as\s*a\s*man\s*thinketh",
            r"descriptive.*origins",
        ],
    }

    filename_lower = filename.lower()

    # Check each album pattern
    for album, patterns in albums.items():
        for pattern in patterns:
            if re.search(pattern, filename_lower):
                return {
                    "album": album,
                    "base_title": base_title,
                    "pattern_matched": pattern,
                }

    # Default to Singles
    return {"album": "Singles", "base_title": base_title, "pattern_matched": "none"}


def organize_collection():
    """Organize MP3s into album folders"""
    print("\n" + "=" * 80)
    print("  ?? ORGANIZE SUNO COLLECTION INTO ALBUMS")
    print("=" * 80 + "\n")

    base_dir = Path("/Users/steven/Music/nocTurneMeLoDieS")
    mp3_dir = base_dir / "mp3s"
    csv_file = base_dir / "suno-merged-20251105_010216.csv"

    # Load metadata
    metadata = {}
    if csv_file.exists():
        with open(csv_file, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get("title", "")
                metadata[title] = row

    print(f"?? Loaded metadata for {len(metadata)} songs\n")

    # Find all MP3s
    mp3_files = list(mp3_dir.glob("*.mp3"))
    print(f"?? Found {len(mp3_files)} MP3s to organize\n")

    # Classify each song
    classifications = defaultdict(list)

    for mp3_file in mp3_files:
        classification = classify_song(mp3_file.stem, metadata.get(mp3_file.stem, {}))
        classification["file"] = mp3_file
        classifications[classification["album"]].append(classification)

    # Show classification summary
    print("?? ALBUM CLASSIFICATION:\n")
    for album in sorted(classifications.keys()):
        count = len(classifications[album])
        print(f"   {album:30s}: {count:3d} songs")

    print(f"\n{'=' * 80}\n")

    # Create organization plan
    moves = []

    for album, songs in classifications.items():
        album_dir = base_dir / album

        for song in songs:
            source = song["file"]

            # Create clean filename
            clean_name = song["base_title"].strip()
            if not clean_name:
                clean_name = source.stem

            # Replace spaces with underscores for consistency
            clean_name = clean_name.replace(" ", "_")

            destination = album_dir / f"{clean_name}.mp3"

            # Handle duplicates
            counter = 1
            while destination in [m["dest"] for m in moves]:
                counter += 1
                destination = album_dir / f"{clean_name}_v{counter}.mp3"

            moves.append(
                {
                    "source": source,
                    "dest": destination,
                    "album": album,
                    "old_name": source.name,
                    "new_name": destination.name,
                },
            )

    print(f"?? Organization plan created: {len(moves)} files\n")

    # Preview some moves
    print("?? Sample organization (first 10):\n")
    for move in moves[:10]:
        print(f"   {move['old_name']}")
        print(f"   ? {move['album']}/{move['new_name']}\n")

    # Save plan
    plan_file = base_dir / "ALBUM_ORGANIZATION_PLAN.csv"
    with open(plan_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["album", "old_name", "new_name", "source", "dest"],
        )
        writer.writeheader()
        writer.writerows(moves)

    print(f"?? Plan saved: {plan_file.name}\n")

    # Execute?
    print("=" * 80)
    print("??  Ready to organize 349 MP3s into album folders")
    print("Press Ctrl+C to cancel, or Enter to execute...")

    try:
        input()
    except KeyboardInterrupt:
        print("\n\n? Cancelled - Plan saved for review")
        return

    # Execute organization
    print("\n?? Organizing files...\n")

    success = 0
    failed = []

    for i, move in enumerate(moves, 1):
        # Create album directory
        move["dest"].parent.mkdir(exist_ok=True)

        try:
            # Move file
            shutil.move(str(move["source"]), str(move["dest"]))
            success += 1

            if i % 50 == 0:
                print(f"? Progress: {i}/{len(moves)} ({success} moved)")

        except Exception as e:
            print(f"? Failed: {move['old_name']} - {e}")
            failed.append(move["old_name"])

    print("\n" + "=" * 80)
    print("  ? ORGANIZATION COMPLETE!")
    print("=" * 80 + "\n")

    print(f"? Successfully organized: {success}/{len(moves)}")
    print(f"? Failed: {len(failed)}")

    # Show album summary
    print("\n?? ALBUMS CREATED:\n")
    for album in sorted(classifications.keys()):
        album_dir = base_dir / album
        if album_dir.exists():
            mp3_count = len(list(album_dir.glob("*.mp3")))
            print(f"   {album:30s}: {mp3_count:3d} MP3s")

    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    organize_collection()
