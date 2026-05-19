#!/usr/bin/env python3
"""
Rename UUID-prefixed files in AI_ENHANCED_ORGANIZATION/DOWNLOADS to use song titles.
Uses Suno export CSVs for UUID->title mapping.
"""

import csv
import re
import sys
from pathlib import Path

DATA_DIR = Path(__file__).parent / "AI_ENHANCED_ORGANIZATION" / "DATA"
AUDIO_DIR = Path(__file__).parent / "AI_ENHANCED_ORGANIZATION" / "DOWNLOADS" / "audio"
IMAGES_DIR = Path(__file__).parent / "AI_ENHANCED_ORGANIZATION" / "DOWNLOADS" / "images"
UUID_PATTERN = re.compile(r"^([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})", re.I)


def sanitize_title(s: str) -> str:
    """Clean title for filename: strip Markdown, unsafe chars."""
    s = re.sub(r"^#+\s*", "", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"^[🌀⭐️]\s*", "", s)
    s = re.sub(r'["\'\n\r\t<>:|?*\\/]', "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:120] if s else "Untitled"


def load_uuid_mapping() -> dict[str, str]:
    """Load UUID->title from all suno-export-*.csv in DATA_DIR."""
    mapping = {}
    for p in sorted(DATA_DIR.glob("suno-export-*.csv")):
        with open(p, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                uid = row.get("id", "").strip()
                title = row.get("title", "").strip()
                if uid and title:
                    mapping[uid.lower()] = sanitize_title(title)
    return mapping


def rename_dir(dir_path: Path, mapping: dict, extensions: tuple) -> tuple[int, int]:
    """Rename files in dir_path. Returns (renamed, skipped)."""
    renamed, skipped = 0, 0
    used_titles: dict[str, int] = {}

    for f in dir_path.iterdir():
        if not f.is_file():
            continue
        if not f.name.lower().endswith(extensions):
            continue

        m = UUID_PATTERN.match(f.name)
        if not m:
            skipped += 1
            continue

        uuid_part = m.group(1).lower()
        title = mapping.get(uuid_part)
        if not title:
            print(f"  No mapping for {f.name}", file=sys.stderr)
            skipped += 1
            continue

        ext = f.suffix
        base = title
        idx = used_titles.get(base, 0)
        used_titles[base] = idx + 1
        new_name = f"{base}_{idx}{ext}" if idx else f"{base}{ext}"
        new_path = dir_path / new_name

        if new_path == f:
            continue
        if new_path.exists():
            while new_path.exists():
                idx += 1
                used_titles[base] = idx
                new_path = dir_path / f"{base}_{idx}{ext}"

        try:
            f.rename(new_path)
            print(f"  {f.name} -> {new_path.name}")
            renamed += 1
        except OSError as e:
            print(f"  Error renaming {f.name}: {e}", file=sys.stderr)
            skipped += 1

    return renamed, skipped


def main():
    print("Loading UUID->title mapping from Suno exports...")
    mapping = load_uuid_mapping()
    print(f"Loaded {len(mapping)} mappings")

    total_r, total_s = 0, 0

    if AUDIO_DIR.exists():
        print(f"\nProcessing audio: {AUDIO_DIR}")
        r, s = rename_dir(AUDIO_DIR, mapping, (".mp3", ".wav", ".flac", ".m4a"))
        total_r += r
        total_s += s
        print(f"  Renamed: {r}, Skipped: {s}")

    if IMAGES_DIR.exists():
        print(f"\nProcessing images: {IMAGES_DIR}")
        r, s = rename_dir(IMAGES_DIR, mapping, (".jpeg", ".jpg", ".png"))
        total_r += r
        total_s += s
        print(f"  Renamed: {r}, Skipped: {s}")

    print(f"\nTotal: {total_r} renamed, {total_s} skipped")


if __name__ == "__main__":
    main()
