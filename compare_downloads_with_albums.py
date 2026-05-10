#!/usr/bin/env python3
"""
Compare AI_ENHANCED_ORGANIZATION/DOWNLOADS with ALBUMS.
Shows which downloaded tracks exist in ALBUMS (by title/folder) and which are new.
"""

import re
from collections import defaultdict
from pathlib import Path

ALBUMS_DIR = Path(__file__).parent / "ALBUMS"
DOWNLOADS_AUDIO = Path(__file__).parent / "AI_ENHANCED_ORGANIZATION" / "DOWNLOADS" / "audio"


def normalize(s: str) -> str:
    """Normalize for comparison: lowercase, collapse spaces/underscores."""
    s = re.sub(r"[_\-]+", " ", s.lower())
    s = re.sub(r"\s+", " ", s.strip())
    s = re.sub(r"[^\w\s]", "", s)  # remove punctuation
    return s


def get_album_bases() -> dict[str, list[str]]:
    """Map normalized name -> original folder names in ALBUMS."""
    bases = defaultdict(list)
    for d in ALBUMS_DIR.iterdir():
        if d.is_dir():
            name = d.name
            key = normalize(name)
            bases[key].append(name)
    return bases


def get_download_bases() -> dict[str, list[str]]:
    """Map normalized name -> original filenames in DOWNLOADS."""
    bases = defaultdict(list)
    if not DOWNLOADS_AUDIO.exists():
        return bases
    for f in DOWNLOADS_AUDIO.iterdir():
        if f.is_file() and f.suffix.lower() in (".mp3", ".wav", ".flac", ".m4a"):
            stem = f.stem
            base = re.sub(r"_\d+$", "", stem)
            key = normalize(base)
            bases[key].append(stem)
    return bases


def main():
    albums = get_album_bases()
    downloads = get_download_bases()

    album_keys = set(albums.keys())
    download_keys = set(downloads.keys())

    in_both = album_keys & download_keys
    only_downloads = download_keys - album_keys
    only_albums = album_keys - download_keys

    print("=" * 60)
    print("DOWNLOADS vs ALBUMS Comparison")
    print("=" * 60)
    print(f"\nALBUMS:        {len(albums)} unique album folders, {sum(len(v) for v in albums.values())} names")
    print(f"DOWNLOADS:     {len(downloads)} unique titles, {sum(len(v) for v in downloads.values())} files")

    print("\n--- IN BOTH (downloaded track has matching album folder) ---")
    print(f"Count: {len(in_both)}")
    for k in sorted(in_both)[:25]:
        orig_album = albums[k][0]
        orig_dl = downloads[k][0]
        print(f"  {orig_dl}  <->  {orig_album}/")
    if len(in_both) > 25:
        print(f"  ... and {len(in_both) - 25} more")

    print("\n--- ONLY IN DOWNLOADS (new, not in ALBUMS) ---")
    print(f"Count: {len(only_downloads)}")
    for k in sorted(only_downloads):
        print(f"  {downloads[k][0]}")
    if not only_downloads:
        print("  (none)")

    print("\n--- SUMMARY ---")
    print(f"  Matching albums:     {len(in_both)}")
    print(f"  New (only in DOWNLOADS): {len(only_downloads)}")
    print(f"  Album folders with no recent download: {len(only_albums)} (albums not in Suno exports)")


if __name__ == "__main__":
    main()
