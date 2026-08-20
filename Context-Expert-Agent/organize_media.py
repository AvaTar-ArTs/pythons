#!/usr/bin/env python3
"""
Organize media and related text files by album base name.

- Scans a single-level directory (no recursion) for files.
- Derives an album_name from the filename by removing the extension and
  stripping known suffixes like "_analysis" and "_transcript".
- Creates a folder named after that album_name.
- Moves any of these files into that folder, renaming them to a canonical pattern:
    * {album_name}.mp3
    * {album_name}.m4a
    * {album_name}.mp4
    * {album_name}_analysis.txt
    * {album_name}_transcript.txt
    * {album_name}.png    (cover image if present in the base directory)
- Skips moving if the destination already exists (to avoid overwriting).

Usage:
    python organize_media.py [BASE_DIR]

If BASE_DIR is not provided, defaults to:
    /Users/steven/Music/nocTurneMeLoDieS/MP3

Notes:
- This script is macOS-friendly and uses only the standard library.
- File extensions are matched case-insensitively (.MP3 == .mp3).
"""

import shutil
import sys
from pathlib import Path

DEFAULT_BASE_DIR = Path("/Users/steven/Music/nocTurneMeLoDieS/MP3")

# Known suffixes to normalize album base names
SUFFIXES = ("_analysis", "_transcript")

# Extensions we manage (case-insensitive)
MEDIA_EXTS = {".mp3", ".m4a", ".mp4", ".wav"}
TEXT_EXTS = {".txt"}
IMAGE_EXTS = {".png"}  # cover image


def normalized_album_name(stem: str) -> str:
    """Strip known suffixes from a filename stem to yield the album name."""
    for suf in SUFFIXES:
        if stem.endswith(suf):
            return stem[: -len(suf)]
    return stem


def canonical_dest_name(album: str, ext: str, original_stem: str) -> str:
    """Return canonical destination filename for a given extension.
    - For analysis/transcript text, keep the suffix in the filename.
    - For media and cover image, use {album}{ext}.
    """
    ext_lower = ext.lower()
    if ext_lower == ".txt":
        # Preserve whether it was analysis or transcript by examining the original stem
        if original_stem.endswith("_analysis"):
            return f"{album}_analysis.txt"
        elif original_stem.endswith("_transcript"):
            return f"{album}_transcript.txt"
        # Fallback: generic text alongside album
        return f"{album}.txt"
    else:
        # Media or image: canonicalized to album name + ext
        return f"{album}{ext_lower}"


def organize_files(base_dir: Path) -> None:
    if not base_dir.exists() or not base_dir.is_dir():
        print(f"Base directory does not exist or is not a directory: {base_dir}")
        sys.exit(1)

    entries = [e for e in base_dir.iterdir() if e.is_file()]
    if not entries:
        print("No files found to organize.")
        return

    moved = 0
    skipped = 0

    # First pass: compute album folders and move items
    for f in entries:
        stem = f.stem
        ext = f.suffix  # includes the dot
        ext_lower = ext.lower()

        # We only care about our known sets
        if ext_lower not in MEDIA_EXTS | TEXT_EXTS | IMAGE_EXTS:
            continue

        album_name = normalized_album_name(stem)
        if not album_name:
            # Safety: if stripping left empty (shouldn't happen), skip
            skipped += 1
            continue

        # Make the album folder
        album_folder = base_dir / album_name
        album_folder.mkdir(parents=True, exist_ok=True)

        dest_name = canonical_dest_name(album_name, ext_lower, stem)
        dest_path = album_folder / dest_name

        # If destination already exists, skip to avoid overwrite
        if dest_path.exists():
            print(f"Skip (exists): {f.name} -> {dest_path}")
            skipped += 1
            continue

        # Move the file
        try:
            shutil.move(str(f), str(dest_path))
            print(f"Moved: {f.name} -> {dest_path}")
            moved += 1
        except Exception as e:
            print(f"ERROR moving {f.name} -> {dest_path}: {e}")
            skipped += 1

    print(f"Done. Moved: {moved}, Skipped: {skipped}")


if __name__ == "__main__":
    base_dir = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_BASE_DIR
    organize_files(base_dir)
    print("All files have been organized successfully.")
