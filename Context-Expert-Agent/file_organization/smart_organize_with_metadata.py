#!/usr/bin/env python3
"""from collections import defaultdict
from pathlib import Path
import csv
import re
import shutil
?? SMART ORGANIZER WITH METADATA
Use CSV metadata (lyrics, tags, style) to intelligently organize 349 MP3s
"""


def load_all_metadata():
    """Load metadata from multiple CSV sources"""
    csv_sources = [
        Path("/Users/steven/Music/nocTurneMeLoDieS/suno-merged-20251105_010216.csv"),
        Path("/Users/steven/Documents/CsV/dataset_suno-ai-scraper_21-09-00-670.csv"),
        Path(
            "/Users/steven/Documents/pythons/suno_tools/suno-sept/suno_merged_master_20250904-143205.csv",
        ),
    ]

    metadata_by_title = {}

    for csv_file in csv_sources:
        if not csv_file.exists():
            continue

        try:
            with open(csv_file, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Get title from various column names
                    title = (
                        (
                            row.get("title")
                            or row.get("songName")
                            or row.get("songtitle")
                            or row.get("songname")
                            or ""
                        )
                        .strip()
                        .strip('"')
                    )

                    if title:
                        # Merge metadata, preferring non-empty values
                        if title not in metadata_by_title:
                            metadata_by_title[title] = row
                        else:
                            # Merge - prefer non-empty values
                            for key, value in row.items():
                                if value and not metadata_by_title[title].get(key):
                                    metadata_by_title[title][key] = value
        except Exception as e:
            print(f"  ??  Error loading {csv_file.name}: {e}")

    return metadata_by_title


def get_metadata_for_file(filename: str, metadata_lookup: dict) -> dict:
    """Find metadata for a given MP3 filename"""
    # Try exact match first
    for title in metadata_lookup:
        clean_title = title.replace(" ", "_").replace("-", "_")
        if clean_title.lower() in filename.lower():
            return metadata_lookup[title]

    # Try fuzzy match
    filename_words = set(re.findall(r"\w+", filename.lower()))
    best_match = None
    best_score = 0

    for title in metadata_lookup:
        title_words = set(re.findall(r"\w+", title.lower()))
        common = len(filename_words & title_words)
        score = common / max(len(filename_words), len(title_words))

        if score > best_score and score > 0.5:
            best_score = score
            best_match = title

    if best_match:
        return metadata_lookup[best_match]

    return {}


def classify_with_metadata(filename: str, metadata: dict) -> str:
    """Classify using metadata (lyrics, style, tags)"""
    filename_lower = filename.lower()

    # Get metadata fields
    style = (
        metadata.get("style")
        or metadata.get("tags")
        or metadata.get("source_labels")
        or ""
    ).lower()

    # Define album patterns with metadata hints
    classifications = {
        "In_This_Alley": {
            "filename": [r"alley", r"in\s*this.*alley"],
            "style": [r"grunge", r"indie.*folk", r"acoustic.*indie"],
        },
        "Love_Is_Rubbish": {
            "filename": [r"love.*rubbish", r"rubbish", r"trash", r"trashy"],
            "style": [r"trash", r"rubbish"],
        },
        "Junkyard_Symphony": {
            "filename": [r"junkyard"],
            "style": [r"junkyard"],
        },
        "Heartbeats": {
            "filename": [r"heartbeat"],
            "style": [r"heartbeat"],
        },
        "Bite_in_the_Night": {
            "filename": [r"bite.*night"],
            "style": [r"night.*bite"],
        },
        "Willow_Whispers": {
            "filename": [r"willow"],
            "style": [r"willow", r"whisper"],
        },
        "Feather_Fang": {
            "filename": [
                r"feather",
                r"spirit",
                r"vine",
                r"became",
                r"mother.*no.*name",
            ],
            "style": [r"ritual", r"tribal", r"shaman", r"native", r"drum.*ceremony"],
        },
        "PeTals_FaLL": {
            "filename": [r"petals", r"roots"],
            "style": [r"petal", r"root"],
        },
        "Summer_Love": {
            "filename": [r"summer.*love"],
            "style": [],
        },
        "Heroes_Rise": {
            "filename": [r"heroes", r"villains"],
            "style": [r"hero", r"villain"],
        },
        "Kings_and_Queens": {
            "filename": [r"kings", r"queens", r"litter", r"royal", r"succession"],
            "style": [r"royal"],
        },
        "Book_of_Memory": {
            "filename": [r"book.*memory", r"heartland", r"forgotten"],
            "style": [r"memory", r"heartland"],
        },
        "Blues_Alley": {
            "filename": [r"blues", r"midnight", r"sammy", r"moonly"],
            "style": [r"blues"],
        },
        "Echoes_Moonlight": {
            "filename": [r"echoes", r"moonlight", r"yesterday"],
            "style": [r"echo", r"moonlight"],
        },
        "Shadow_Messages": {
            "filename": [r"shadow"],
            "style": [r"shadow", r"dark"],
        },
        "Heavenly_Hands": {
            "filename": [r"heavenly.*hands"],
            "style": [],
        },
        "Workshop_Series": {
            "filename": [r"workshop", r"tapestry", r"tyranny"],
            "style": [r"workshop", r"tapestry"],
        },
        "Covers": {
            "filename": [
                r"rocket\s*man",
                r"adele",
                r"billie",
                r"murray",
                r"angie.*rocket",
                r"cover",
            ],
            "style": [r"cover"],
        },
        "Rituals": {
            "filename": [
                r"threaded",
                r"enchanted",
                r"witches",
                r"chamber",
                r"drink.*me",
            ],
            "style": [r"ritual", r"mystic", r"witch", r"enchant"],
        },
        "Dance": {
            "filename": [r"dance", r"dancing"],
            "style": [r"dance", r"disco"],
        },
        "Nature": {
            "filename": [r"desert", r"garden", r"golden\s*roots"],
            "style": [r"nature", r"garden"],
        },
        "Philosophical": {
            "filename": [r"thinketh", r"descriptive.*origins"],
            "style": [],
        },
        "Stormchild": {
            "filename": [r"storm", r"unbroken.*stars"],
            "style": [r"storm"],
        },
    }

    # Check filename patterns
    for album, patterns in classifications.items():
        for pattern in patterns["filename"]:
            if re.search(pattern, filename_lower):
                return album

    # Check style/tags patterns if we have metadata
    if style:
        for album, patterns in classifications.items():
            for pattern in patterns["style"]:
                if re.search(pattern, style):
                    return album

    return "Singles"


print("\n" + "=" * 80)
print("  ?? SMART ORGANIZE WITH METADATA")
print("=" * 80 + "\n")

# Load all metadata
print("?? Loading metadata from multiple sources...")
metadata = load_all_metadata()
print(f"? Loaded metadata for {len(metadata)} songs\n")

# Find root MP3s
base_dir = Path("/Users/steven/Music/nocTurneMeLoDieS")
root_mp3s = [f for f in base_dir.glob("*.mp3") if f.is_file()]

print(f"?? Found {len(root_mp3s)} MP3s in root directory\n")

# Classify each
classifications = defaultdict(list)

for mp3_file in root_mp3s:
    # Get metadata
    meta = get_metadata_for_file(mp3_file.stem, metadata)

    # Classify
    album = classify_with_metadata(mp3_file.stem, meta)

    classifications[album].append({"file": mp3_file, "metadata": meta})

# Show classification
print("?? ALBUM CLASSIFICATION SUMMARY:\n")
total_classified = 0
for album in sorted(classifications.keys()):
    count = len(classifications[album])
    total_classified += count
    print(f"   {album:30s}: {count:3d} songs")

print(f"\n   TOTAL: {total_classified} songs")
print(f"\n{'='*80}\n")

# Create move plan
moves = []

for album, songs in classifications.items():
    album_dir = base_dir / album

    for item in songs:
        mp3_file = item["file"]

        # Keep original filename (just move to folder)
        destination = album_dir / mp3_file.name

        moves.append(
            {
                "source": str(mp3_file),
                "dest": str(destination),
                "album": album,
                "filename": mp3_file.name,
                "has_metadata": bool(item["metadata"]),
            },
        )

# Save plan
plan_file = base_dir / "SMART_ORGANIZATION_PLAN.csv"
with open(plan_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["album", "filename", "source", "dest", "has_metadata"],
    )
    writer.writeheader()
    writer.writerows(moves)

print(f"?? Organization plan saved: {plan_file.name}")
print(
    f"?? Files with metadata: {sum(1 for m in moves if m['has_metadata'])}/{len(moves)}",
)
print(
    f"\n? Ready to organize {len(moves)} files into {len(classifications)} album folders",
)
print("\n?? Review SMART_ORGANIZATION_PLAN.csv before executing")

if __name__ == "__main__":
    pass  # Run as script
