#!/usr/bin/env python3
"""from collections import defaultdict
from pathlib import Path
import csv
import re
Clean up messy MP3 filenames and create mapping CSV with Suno backup data
Maps mp3s folder files to proper album folders, avoiding duplicates
"""

BASE_DIR = Path("/Users/steven/Music/nocTurneMeLoDieS")
CSV_FILE = BASE_DIR / "suno-merged-20251105_010216.csv"
OUTPUT_CSV = BASE_DIR / "FILENAME_CLEANUP_MAPPING.csv"

# Album folders (excluding system folders)
EXCLUDE_FOLDERS = {
    "TRANSCRIPT_ANALYSIS_20251105_034630",
    "DATA",
    "DOCS",
    "SCRIPTS",
    "SONG_BUNDLES",
    "DEDUP_BACKUP",
    "TRANSCRIPT_MATCHING",
}


def normalize_for_matching(text):
    """Normalize text for fuzzy matching"""
    # Remove special chars, lowercase, collapse spaces
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text.lower())
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_filename(filename):
    '\''Clean up messy filename patterns
    Examples:
        'Witches Road Song Lyrics_255.mp3' -> 'Witches_Road_Song_255.mp3'
        'Witches Road_(Remastered)_256.mp3' -> 'Witches_Road_(Remastered)_256.mp3'
    """
    name = filename.rsplit(".", 1)[0]  # Remove extension

    # Remove redundant words (case insensitive)
    redundant_words = [
        "Lyrics",
        "Song Lyrics",
        "Audio",
        "AUDIO",
        "Official",
        "Track",
        "Full Song",
    ]

    for word in redundant_words:
        # Remove at end or before underscore/duration
        name = re.sub(rf"\s+{word}\b", "", name, flags=re.IGNORECASE)
        name = re.sub(rf"\b{word}\s+", "", name, flags=re.IGNORECASE)

    # Clean up multiple underscores/spaces
    name = re.sub(r"_+", "_", name)
    name = re.sub(r"\s+", "_", name)

    # Remove leading/trailing underscores
    name = name.strip("_")

    # Ensure proper spacing around parentheses
    name = re.sub(r"_\(", "_(", name)
    name = re.sub(r"\)_", ")_", name)

    return name + ".mp3"


def extract_base_title(filename):
    """Extract the base song title (without duration, version markers)
    For matching with Suno CSV and detecting duplicates
    """
    name = filename.rsplit(".", 1)[0]

    # Remove duration patterns: _### or (M:SS)
    name = re.sub(r"_\d{3,4}$", "", name)
    name = re.sub(r"_?\(\d:\d{2}\)$", "", name)

    # Remove version markers
    name = re.sub(r"_\(Remastered\).*$", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_\(Remix\).*$", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_\(Edit\).*$", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_\[Live\].*$", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_Remastered.*$", "", name, flags=re.IGNORECASE)

    # Remove sequence numbers _1, _2, etc at end
    name = re.sub(r"_\d{1,2}$", "", name)
    name = re.sub(r"-\d{1,2}$", "", name)

    return normalize_for_matching(name)


def load_suno_data():
    """Load Suno CSV data for matching"""
    print("?? Loading Suno CSV data...")

    suno_data = {}

    try:
        with open(CSV_FILE, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get("title", "")
                if title:
                    normalized = normalize_for_matching(title)
                    # Store multiple matches if needed
                    if normalized not in suno_data:
                        suno_data[normalized] = []
                    suno_data[normalized].append(row)

        total_songs = sum(len(v) for v in suno_data.values())
        print(f"   Loaded {total_songs} Suno songs ({len(suno_data)} unique titles)\n")
    except Exception as e:
        print(f"   ??  Could not load Suno CSV: {e}\n")

    return suno_data


def scan_album_folders():
    """Scan all album folders (excluding mp3s folder) to find existing files"""
    print("?? Scanning album folders for existing MP3s...")

    album_files = {}  # base_title -> [list of files]

    for mp3_file in BASE_DIR.rglob("*.mp3"):
        # Get folder name
        try:
            rel_path = mp3_file.relative_to(BASE_DIR)
            folder = rel_path.parts[0] if len(rel_path.parts) > 1 else "."
        except ValueError:
            continue

        # Exclude mp3s folder and system folders
        if folder == "mp3s" or folder in EXCLUDE_FOLDERS:
            continue

        # Get base title for duplicate detection
        base_title = extract_base_title(mp3_file.name)

        if base_title not in album_files:
            album_files[base_title] = []

        album_files[base_title].append(
            {"file": mp3_file, "folder": folder, "filename": mp3_file.name},
        )

    total_files = sum(len(v) for v in album_files.values())
    print(f"   Found {total_files} MP3s in {len(album_files)} unique songs\n")

    return album_files


def scan_mp3s_folder():
    """Scan the mp3s download folder"""
    print("?? Scanning mp3s download folder...")

    mp3s_dir = BASE_DIR / "mp3s"
    mp3_files = []

    if mp3s_dir.exists():
        mp3_files = list(mp3s_dir.glob("*.mp3"))

    print(f"   Found {len(mp3_files)} MP3s in download folder\n")

    return mp3_files


def create_comprehensive_mapping(mp3s_files, album_files, suno_data):
    """Create comprehensive mapping for all files"""
    print("???  Creating comprehensive mapping...")

    mappings = []

    # 1. Process files in album folders (cleanup only)
    print("   Processing album folder files...")
    for base_title, files in album_files.items():
        for file_info in files:
            mp3_file = file_info["file"]
            original_filename = mp3_file.name
            cleaned_filename = clean_filename(original_filename)

            # Match with Suno data
            suno_matches = suno_data.get(base_title, [])
            suno_match = suno_matches[0] if suno_matches else {}

            mapping = {
                "location": "ALBUM_FOLDER",
                "current_folder": file_info["folder"],
                "target_folder": file_info["folder"],  # Stay in same folder
                "original_filename": original_filename,
                "cleaned_filename": cleaned_filename,
                "needs_rename": (
                    "YES" if original_filename != cleaned_filename else "NO"
                ),
                "action": "RENAME" if original_filename != cleaned_filename else "KEEP",
                "duplicate_status": "UNIQUE",
                "suno_id": suno_match.get("id", ""),
                "suno_title": suno_match.get("title", ""),
                "suno_url": suno_match.get("url", ""),
                "suno_audio_url": suno_match.get("audioUrl", ""),
                "suno_image_url": suno_match.get("imageUrl", ""),
                "full_path": str(mp3_file),
            }

            mappings.append(mapping)

    # 2. Process files in mp3s folder (move or mark as duplicate)
    print("   Processing mp3s folder files...")
    for mp3_file in mp3s_files:
        original_filename = mp3_file.name
        cleaned_filename = clean_filename(original_filename)
        base_title = extract_base_title(original_filename)

        # Check if this file already exists in album folders
        is_duplicate = base_title in album_files

        # Match with Suno data
        suno_matches = suno_data.get(base_title, [])
        suno_match = suno_matches[0] if suno_matches else {}

        # Determine target folder based on Suno title or existing location
        target_folder = "Singles"  # Default
        if is_duplicate:
            # Use folder where it already exists
            target_folder = album_files[base_title][0]["folder"]

        mapping = {
            "location": "MP3S_FOLDER",
            "current_folder": "mp3s",
            "target_folder": target_folder,
            "original_filename": original_filename,
            "cleaned_filename": cleaned_filename,
            "needs_rename": "YES" if original_filename != cleaned_filename else "NO",
            "action": "DUPLICATE_DELETE" if is_duplicate else "MOVE_AND_RENAME",
            "duplicate_status": "DUPLICATE" if is_duplicate else "NEW",
            "suno_id": suno_match.get("id", ""),
            "suno_title": suno_match.get("title", ""),
            "suno_url": suno_match.get("url", ""),
            "suno_audio_url": suno_match.get("audioUrl", ""),
            "suno_image_url": suno_match.get("imageUrl", ""),
            "full_path": str(mp3_file),
        }

        mappings.append(mapping)

    print(f"   Created {len(mappings)} total mappings\n")

    return mappings


def write_csv(mappings):
    """Write mapping CSV"""
    print(f"?? Writing mapping CSV: {OUTPUT_CSV.name}")

    # Sort: duplicates first, then by action, then by folder
    mappings.sort(
        key=lambda x: (
            x["location"],
            x["action"] != "DUPLICATE_DELETE",
            x["current_folder"],
            x["original_filename"],
        ),
    )

    fieldnames = [
        "location",
        "action",
        "duplicate_status",
        "current_folder",
        "target_folder",
        "original_filename",
        "cleaned_filename",
        "needs_rename",
        "suno_id",
        "suno_title",
        "suno_url",
        "suno_audio_url",
        "suno_image_url",
        "full_path",
    ]

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(mappings)

    print(f"   ? Saved {len(mappings)} mappings\n")


def print_summary(mappings):
    """Print summary statistics'\''
    # Count by location
    album_files = [m for m in mappings if m["location"] == "ALBUM_FOLDER"]
    mp3s_files = [m for m in mappings if m["location"] == "MP3S_FOLDER"]

    # Count by action
    to_rename = sum(1 for m in mappings if m["needs_rename"] == "YES")
    duplicates = sum(1 for m in mappings if m["duplicate_status"] == "DUPLICATE")
    new_files = sum(1 for m in mappings if m["duplicate_status"] == "NEW")
    with_suno = sum(1 for m in mappings if m["suno_id"])

    print("=" * 70)
    print("?? COMPREHENSIVE SUMMARY")
    print("=" * 70)
    print(f"Total MP3 files scanned: {len(mappings)}")
    print(f"  ? In album folders: {len(album_files)}")
    print(f"  ? In mp3s folder: {len(mp3s_files)}")
    print()
    print(f"Files needing cleanup rename: {to_rename}")
    print(f"Duplicates to delete: {duplicates}")
    print(f"New files to organize: {new_files}")
    print(f"Files with Suno backup data: {with_suno}")
    print()
    print(f"?? Mapping CSV: {OUTPUT_CSV}")
    print()

    # Show some examples
    if duplicates > 0:
        print("???  Example duplicates (in mp3s folder):")
        examples = [m for m in mp3s_files if m["duplicate_status"] == "DUPLICATE"][:5]
        for ex in examples:
            print(f"   ? {ex['original_filename']}")
            print(f"     Already in: {ex['target_folder']}")
        print()

    if new_files > 0:
        print("?? Example new files to organize:")
        examples = [m for m in mp3s_files if m["duplicate_status"] == "NEW"][:5]
        for ex in examples:
            print(f"   ? {ex['original_filename']}")
            print(f"     ? Move to: {ex['target_folder']}")
        print()

    rename_examples = [m for m in album_files if m["needs_rename"] == "YES"][:5]
    if rename_examples:
        print("?? Example cleanups (in album folders):")
        for ex in rename_examples:
            print(f"   ? {ex['original_filename']}")
            print(f"     ? {ex['cleaned_filename']}")
        print()

    print("=" * 70)
    print("Next steps:")
    print("1. Review FILENAME_CLEANUP_MAPPING.csv")
    print("2. Delete duplicates from mp3s folder")
    print("3. Move new files to proper album folders")
    print("4. Rename files in album folders for consistency")
    print("=" * 70)


def main():
    print("=" * 70)
    print("???  COMPREHENSIVE FILENAME CLEANUP MAPPER")
    print("=" * 70)
    print()

    # Load Suno data
    suno_data = load_suno_data()

    # Scan album folders
    album_files = scan_album_folders()

    # Scan mp3s folder
    mp3s_files = scan_mp3s_folder()

    # Create comprehensive mapping
    mappings = create_comprehensive_mapping(mp3s_files, album_files, suno_data)

    # Write CSV
    write_csv(mappings)

    # Print summary
    print_summary(mappings)


if __name__ == "__main__":
    main()
