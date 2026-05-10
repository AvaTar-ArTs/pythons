#!/usr/bin/env python3
"""
Organize ALBUMS: flatten nested structures, move scripts out, merge project folders,
consolidate song variations, fix loose/emoji.

Usage:
  python3 organize_albums.py          # dry run
  python3 organize_albums.py --apply  # execute
"""

import shutil
import sys
from pathlib import Path

ALBUMS_DIR = Path(__file__).parent / "ALBUMS"
PROJECT = Path(__file__).parent

# Folders that are project structure, not albums - move out of ALBUMS
MOVE_OUT_FOLDERS = ["MUSIC_ORGANIZED", "CONSOLIDATED_CONTENT", "MUSIC"]

# Files to move out of ALBUMS
MOVE_OUT_FILES = ["consolidate_nested_albums.py", "CONSOLIDATION_SUMMARY.json"]

ARCHIVE_DIR = PROJECT / "_ARCHIVED_FROM_ALBUMS"


def flatten_album(album_path: Path, dry_run: bool) -> int:
    """Move files from nested subdirs into album root. Returns count moved."""
    moved = 0
    for f in list(album_path.rglob("*")):
        if not f.is_file():
            continue
        if f.parent == album_path:
            continue
        rel = f.relative_to(album_path)
        dest = album_path / f.name
        if dest.exists():
            stem, ext = dest.stem, dest.suffix
            i = 1
            while dest.exists():
                dest = album_path / f"{stem}_{i}{ext}"
                i += 1
        if dry_run:
            print(f"  [flatten] {rel} -> {dest.name}")
        else:
            shutil.move(str(f), str(dest))
            print(f"  Flattened {rel} -> {dest.name}")
        moved += 1
    # Remove empty subdirs
    if not dry_run and moved:
        for d in sorted(album_path.rglob("*"), key=lambda x: -len(x.parts)):
            if d.is_dir() and not any(d.iterdir()):
                d.rmdir()
    return moved


def flatten_all(dry_run: bool) -> int:
    """Flatten all albums with nested subdirs."""
    total = 0
    for d in ALBUMS_DIR.iterdir():
        if not d.is_dir() or d.name.startswith("."):
            continue
        subdirs = [x for x in d.iterdir() if x.is_dir()]
        if not subdirs:
            continue
        # Skip MOVE_OUT_FOLDERS - handled separately
        if d.name in MOVE_OUT_FOLDERS:
            continue
        n = flatten_album(d, dry_run)
        if n:
            print(f"\n[{d.name}] {n} files flattened")
            total += n
    return total


def move_scripts_out(dry_run: bool) -> int:
    """Move scripts and config out of ALBUMS."""
    moved = 0
    for name in MOVE_OUT_FILES:
        src = ALBUMS_DIR / name
        if not src.exists():
            continue
        dest = PROJECT / name
        if dry_run:
            print(f"  [move out] {name} -> {PROJECT}/")
        else:
            if dest.exists() and dest.is_file():
                dest.unlink()
            shutil.move(str(src), str(dest))
            print(f"  Moved {name} -> project root")
        moved += 1
    return moved


def move_project_folders_out(dry_run: bool) -> int:
    """Move MUSIC_ORGANIZED, CONSOLIDATED_CONTENT, MUSIC to archive (project structure, not albums)."""
    moved = 0
    if not dry_run:
        ARCHIVE_DIR.mkdir(exist_ok=True)
    for name in MOVE_OUT_FOLDERS:
        src = ALBUMS_DIR / name
        if not src.exists() or not src.is_dir():
            continue
        dest = ARCHIVE_DIR / name
        if dry_run:
            print(f"  [move out] {name}/ -> {ARCHIVE_DIR}/")
        else:
            if dest.exists():
                shutil.rmtree(dest)
            shutil.move(str(src), str(dest))
            print(f"  Moved {name}/ -> _ARCHIVED_FROM_ALBUMS/")
        moved += 1
    return moved


def main():
    dry_run = "--apply" not in sys.argv
    mode = "DRY RUN - " if dry_run else ""
    print(f"{mode}Organizing ALBUMS\n")
    print("=" * 50)

    print("\n--- 1. Move scripts/config out ---")
    n = move_scripts_out(dry_run)
    print(f"  {n} items")

    print("\n--- 2. Flatten nested album subdirs ---")
    n = flatten_all(dry_run)
    print(f"  Total: {n} files flattened")

    print("\n--- 3. Move project folders out (MUSIC_ORGANIZED, CONSOLIDATED_CONTENT, MUSIC) ---")
    n = move_project_folders_out(dry_run)
    print(f"  {n} folders moved to _ARCHIVED_FROM_ALBUMS/")

    print("\n--- 4. Consolidate song variations (CSV-based) ---")
    if not dry_run:
        from consolidate_song_variations import main as consolidate_main

        consolidate_main()
    else:
        print("  (run with --apply)")

    print("\n--- 5. Fix loose MP3s and emoji folders ---")
    if not dry_run:
        from fix_loose_and_emoji import main as fix_main

        fix_main()
    else:
        print("  (run with --apply)")

    print("\n" + "=" * 50)
    print("Done.")
    if dry_run:
        print("Run with --apply to execute.")


if __name__ == "__main__":
    main()
