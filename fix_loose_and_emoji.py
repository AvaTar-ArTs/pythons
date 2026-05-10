#!/usr/bin/env python3
"""
1. Move loose MP3s from ALBUMS root into appropriate album folders.
2. Merge emoji-prefixed folders into canonical folder names.

Usage:
  python3 fix_loose_and_emoji.py          # dry run
  python3 fix_loose_and_emoji.py --apply  # execute
"""

import re
import shutil
import sys
from pathlib import Path

ALBUMS_DIR = Path(__file__).parent / "ALBUMS"

# Loose MP3 filename prefix/suffix -> target folder
LOOSE_MAPPING = [
    (r"^Heavenlyhands_Jingle", "HEAVENLYHANDS_JINGLE"),
    (r"^Summer_Love", "Summer_Love"),
    (r"^Junkyard_Symphony", "Junkyard_Symphony"),
    (r"^Love_is_rubbish", "Rubbish_Love"),
]

# Emoji folder -> canonical folder (merge contents, then remove emoji folder)
EMOJI_MERGES = [
    ("🎵_THE_PATCHWORK_PROPHECY", "The_Patchwork_Prophecy"),
    ("️_StarLit_Void", "StarLit_Void"),
]


def move_loose_mp3s(dry_run: bool) -> int:
    """Move loose MP3s from ALBUMS root into folders."""
    moved = 0
    for f in ALBUMS_DIR.iterdir():
        if not f.is_file() or f.suffix.lower() != ".mp3":
            continue
        name = f.name
        target_folder = None
        for pattern, folder in LOOSE_MAPPING:
            if re.search(pattern, name, re.I):
                target_folder = folder
                break
        if not target_folder:
            continue
        dest_dir = ALBUMS_DIR / target_folder
        if not dest_dir.exists():
            dest_dir.mkdir(parents=True)
        dest = dest_dir / name
        if dest.exists():
            stem, ext = dest.stem, dest.suffix
            i = 1
            while dest.exists():
                dest = dest_dir / f"{stem}_{i}{ext}"
                i += 1
        if dry_run:
            print(f"  [loose] {name} -> {target_folder}/")
        else:
            shutil.move(str(f), str(dest))
            print(f"  Moved {name} -> {target_folder}/")
        moved += 1
    return moved


def merge_emoji_folders(dry_run: bool) -> int:
    """Merge emoji-prefixed folders into canonical folders."""
    merged = 0
    for emoji_name, canonical_name in EMOJI_MERGES:
        src = ALBUMS_DIR / emoji_name
        dst = ALBUMS_DIR / canonical_name
        if not src.exists() or not src.is_dir():
            continue
        if not dst.exists():
            if dry_run:
                print(f"  [emoji] Would rename {emoji_name} -> {canonical_name}/")
            else:
                shutil.move(str(src), str(dst))
                print(f"  Renamed {emoji_name} -> {canonical_name}/")
            merged += 1
            continue
        # Merge: move contents from emoji folder into canonical
        if dry_run:
            count = sum(1 for _ in src.rglob("*") if _.is_file())
            print(f"  [emoji] Would merge {emoji_name}/ ({count} items) -> {canonical_name}/")
        else:
            for item in src.rglob("*"):
                if not item.is_file():
                    continue
                rel = item.relative_to(src)
                dest_file = dst / rel
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                if dest_file.exists():
                    stem, ext = dest_file.stem, dest_file.suffix
                    i = 1
                    while dest_file.exists():
                        dest_file = dest_file.parent / f"{stem}_{i}{ext}"
                        i += 1
                shutil.move(str(item), str(dest_file))
            # Remove empty subdirs and the emoji folder
            for d in sorted(src.rglob("*"), key=lambda x: -len(x.parts)):
                if d.is_dir() and not any(d.iterdir()):
                    d.rmdir()
            if not any(src.iterdir()):
                src.rmdir()
            print(f"  Merged {emoji_name}/ -> {canonical_name}/")
        merged += 1
    return merged


def main():
    dry_run = "--apply" not in sys.argv
    mode = "DRY RUN - " if dry_run else ""
    print(f"{mode}Fix loose MP3s and emoji folders in {ALBUMS_DIR}\n")

    print("--- Loose MP3s ---")
    n1 = move_loose_mp3s(dry_run)
    print(f"  {n1} files\n")

    print("--- Emoji folders ---")
    n2 = merge_emoji_folders(dry_run)
    print(f"  {n2} folders\n")

    print(f"--- Summary ---\n  Loose moved: {n1}\n  Emoji merged: {n2}")
    if dry_run:
        print("\nRun with --apply to execute.")


if __name__ == "__main__":
    main()
