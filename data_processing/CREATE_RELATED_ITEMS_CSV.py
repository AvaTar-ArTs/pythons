#!/usr/bin/env python3
"""
Create CSV with related items grouped together
Groups MP3s with their associated lyrics, prompts, and discography items
"""

from pathlib import Path
import json
import csv
from datetime import datetime
from collections import defaultdict

documents_dir = Path.home() / "Documents"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Find the most recent search JSON
json_files = sorted(documents_dir.glob("MP3_SEARCH_*.json"), reverse=True)
if not json_files:
    print("❌ No MP3_SEARCH JSON file found. Run SEARCH_AND_ORGANIZE_MP3S.py first.")
    exit(1)

json_file = json_files[0]
print(f"📄 Loading data from: {json_file.name}")
print()

# Load data
with open(json_file, "r") as f:
    data = json.load(f)

# Load all items (not just the limited samples in details)
# The JSON might have limited samples, so we need to search again or load from CSV
# For now, use what's available in details, but note it might be limited
mp3s = data["details"].get("mp3", [])
discography = data["details"].get("discography", [])
prompts = data["details"].get("prompts", [])
lyrics = data["details"].get("lyrics", [])

# Try to load from CSV if available (has all data)
csv_files = sorted(documents_dir.glob("MP3_ALL_FILES_*.csv"), reverse=True)
if csv_files:
    print(f"📄 Also loading from CSV: {csv_files[0].name}")
    import csv as csv_module

    with open(csv_files[0], "r", encoding="utf-8") as f:
        reader = csv_module.DictReader(f)
        mp3s_from_csv = []
        for row in reader:
            mp3s_from_csv.append(
                {
                    "path": row["full_path"],
                    "name": row["filename"],
                    "size_mb": float(row.get("size_mb", 0)),
                    "size": int(float(row.get("size_bytes", 0))),
                    "depth": int(row.get("depth", 0)),
                    "directory": row.get("directory", ""),
                }
            )
        if len(mp3s_from_csv) > len(mp3s):
            print(f"   Using {len(mp3s_from_csv)} MP3s from CSV (more complete)")
            mp3s = mp3s_from_csv

print(
    f"Loaded: {len(mp3s)} MP3s, {len(discography)} discography, {len(prompts)} prompts, {len(lyrics)} lyrics"
)
print()

# Group items by directory/project
related_groups = defaultdict(
    lambda: {
        "mp3s": [],
        "lyrics": [],
        "prompts": [],
        "discography": [],
        "base_path": None,
    }
)


def normalize_path(path_str):
    """Normalize path for grouping"""
    path = Path(path_str)
    # Get parent directory (project/album folder)
    return str(path.parent)


def get_base_name(name):
    """Extract base name without extension and numbers"""
    base = Path(name).stem
    # Remove common suffixes like " 1", " 2", " (1)", etc.
    import re

    base = re.sub(r"\s*\(\d+\)\s*$", "", base)
    base = re.sub(r"\s+\d+\s*$", "", base)
    return base.lower().strip()


# Group MP3s by directory
print("Grouping MP3s by directory...")
for mp3 in mp3s:
    directory = mp3.get("directory", normalize_path(mp3["path"]))
    related_groups[directory]["mp3s"].append(mp3)
    if not related_groups[directory]["base_path"]:
        related_groups[directory]["base_path"] = directory

# Group lyrics by directory and match to MP3s
print("Grouping lyrics...")
for lyric in lyrics:
    directory = lyric.get("directory", normalize_path(lyric["path"]))
    related_groups[directory]["lyrics"].append(lyric)

    # Also try to match by filename similarity
    lyric_base = get_base_name(lyric["name"])
    for group_dir, group_data in related_groups.items():
        for mp3 in group_data["mp3s"]:
            mp3_base = get_base_name(mp3["name"])
            if lyric_base in mp3_base or mp3_base in lyric_base:
                if directory != group_dir:  # Only add if not already in same directory
                    related_groups[group_dir]["lyrics"].append(lyric)
                break

# Group prompts by directory
print("Grouping prompts...")
for prompt in prompts:
    directory = prompt.get("directory", normalize_path(prompt["path"]))
    related_groups[directory]["prompts"].append(prompt)

# Group discography by directory
print("Grouping discography...")
for disc in discography:
    directory = disc.get("directory", normalize_path(disc["path"]))
    related_groups[directory]["discography"].append(disc)

print(f"Created {len(related_groups)} related groups")
print()

# Create CSV with related items
csv_file = documents_dir / f"RELATED_ITEMS_{timestamp}.csv"

print("Creating CSV with related items...")
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # Header
    writer.writerow(
        [
            "group_id",
            "base_directory",
            "mp3_count",
            "mp3_files",
            "mp3_total_size_mb",
            "lyric_count",
            "lyric_files",
            "lyric_total_size_mb",
            "prompt_count",
            "prompt_files",
            "prompt_total_size_mb",
            "discography_count",
            "discography_items",
            "total_items",
            "total_size_mb",
        ]
    )

    # Sort groups by total items (most related first)
    sorted_groups = sorted(
        related_groups.items(),
        key=lambda x: len(x[1]["mp3s"])
        + len(x[1]["lyrics"])
        + len(x[1]["prompts"])
        + len(x[1]["discography"]),
        reverse=True,
    )

    group_id = 0
    for directory, group_data in sorted_groups:
        group_id += 1

        mp3s_list = group_data["mp3s"]
        lyrics_list = group_data["lyrics"]
        prompts_list = group_data["prompts"]
        discography_list = group_data["discography"]

        # Calculate totals
        mp3_size = sum(m["size_mb"] for m in mp3s_list)
        lyric_size = sum(l["size_mb"] for l in lyrics_list)
        prompt_size = sum(p["size_mb"] for p in prompts_list)
        total_size = mp3_size + lyric_size + prompt_size
        total_items = (
            len(mp3s_list)
            + len(lyrics_list)
            + len(prompts_list)
            + len(discography_list)
        )

        # Create file lists (truncated if too long)
        mp3_files = " | ".join([m["name"] for m in mp3s_list[:10]])
        if len(mp3s_list) > 10:
            mp3_files += f" ... (+{len(mp3s_list) - 10} more)"

        lyric_files = " | ".join([l["name"] for l in lyrics_list[:10]])
        if len(lyrics_list) > 10:
            lyric_files += f" ... (+{len(lyrics_list) - 10} more)"

        prompt_files = " | ".join([p["name"] for p in prompts_list[:10]])
        if len(prompts_list) > 10:
            prompt_files += f" ... (+{len(prompts_list) - 10} more)"

        discography_items = " | ".join([d["name"] for d in discography_list[:10]])
        if len(discography_list) > 10:
            discography_items += f" ... (+{len(discography_list) - 10} more)"

        writer.writerow(
            [
                group_id,
                directory,
                len(mp3s_list),
                mp3_files,
                round(mp3_size, 2),
                len(lyrics_list),
                lyric_files,
                round(lyric_size, 2),
                len(prompts_list),
                prompt_files,
                round(prompt_size, 2),
                len(discography_list),
                discography_items,
                total_items,
                round(total_size, 2),
            ]
        )

print(f"✅ CSV created: {csv_file.name}")
print()

# Also create detailed version with one item per row
detailed_csv = documents_dir / f"RELATED_ITEMS_DETAILED_{timestamp}.csv"

print("Creating detailed CSV (one item per row)...")
with open(detailed_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # Header
    writer.writerow(
        [
            "group_id",
            "base_directory",
            "item_type",
            "item_name",
            "item_path",
            "item_size_mb",
            "item_depth",
            "related_mp3s",
            "related_lyrics",
            "related_prompts",
            "related_discography",
        ]
    )

    group_id = 0
    for directory, group_data in sorted_groups:
        group_id += 1

        mp3s_list = group_data["mp3s"]
        lyrics_list = group_data["lyrics"]
        prompts_list = group_data["prompts"]
        discography_list = group_data["discography"]

        # Create related items strings
        related_mp3s = " | ".join([m["name"] for m in mp3s_list[:5]])
        related_lyrics = " | ".join([l["name"] for l in lyrics_list[:5]])
        related_prompts = " | ".join([p["name"] for p in prompts_list[:5]])
        related_discography = " | ".join([d["name"] for d in discography_list[:5]])

        # Write MP3s
        for mp3 in mp3s_list:
            writer.writerow(
                [
                    group_id,
                    directory,
                    "MP3",
                    mp3["name"],
                    mp3["path"],
                    mp3["size_mb"],
                    mp3.get("depth", ""),
                    related_mp3s,
                    related_lyrics,
                    related_prompts,
                    related_discography,
                ]
            )

        # Write Lyrics
        for lyric in lyrics_list:
            writer.writerow(
                [
                    group_id,
                    directory,
                    "Lyric",
                    lyric["name"],
                    lyric["path"],
                    lyric["size_mb"],
                    lyric.get("depth", ""),
                    related_mp3s,
                    related_lyrics,
                    related_prompts,
                    related_discography,
                ]
            )

        # Write Prompts
        for prompt in prompts_list:
            writer.writerow(
                [
                    group_id,
                    directory,
                    "Prompt",
                    prompt["name"],
                    prompt["path"],
                    prompt["size_mb"],
                    prompt.get("depth", ""),
                    related_mp3s,
                    related_lyrics,
                    related_prompts,
                    related_discography,
                ]
            )

        # Write Discography
        for disc in discography_list:
            writer.writerow(
                [
                    group_id,
                    directory,
                    "Discography",
                    disc["name"],
                    disc["path"],
                    "",
                    disc.get("depth", ""),
                    related_mp3s,
                    related_lyrics,
                    related_prompts,
                    related_discography,
                ]
            )

print(f"✅ Detailed CSV created: {detailed_csv.name}")
print()

# Statistics
print("=" * 100)
print("📊 STATISTICS")
print("=" * 100)
print()

total_groups = len(related_groups)
groups_with_mp3s = sum(1 for g in related_groups.values() if g["mp3s"])
groups_with_lyrics = sum(1 for g in related_groups.values() if g["lyrics"])
groups_with_prompts = sum(1 for g in related_groups.values() if g["prompts"])
groups_with_discography = sum(1 for g in related_groups.values() if g["discography"])

print(f"Total groups: {total_groups:,}")
print(f"Groups with MP3s: {groups_with_mp3s:,}")
print(f"Groups with Lyrics: {groups_with_lyrics:,}")
print(f"Groups with Prompts: {groups_with_prompts:,}")
print(f"Groups with Discography: {groups_with_discography:,}")
print()

# Top groups
print("Top 10 groups by total items:")
print("-" * 100)
for i, (directory, group_data) in enumerate(sorted_groups[:10], 1):
    total = (
        len(group_data["mp3s"])
        + len(group_data["lyrics"])
        + len(group_data["prompts"])
        + len(group_data["discography"])
    )
    print(
        f"{i:2d}. {total:3d} items | {len(group_data['mp3s'])} MP3s, {len(group_data['lyrics'])} lyrics, "
        f"{len(group_data['prompts'])} prompts, {len(group_data['discography'])} discography"
    )
    print(f"    {directory[:80]}")

print()
print("=" * 100)
print("✅ CSV FILES CREATED")
print("=" * 100)
print(f"📊 Summary CSV: {csv_file.name}")
print(f"📋 Detailed CSV: {detailed_csv.name}")
print()
