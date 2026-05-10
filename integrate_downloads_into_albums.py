#!/usr/bin/env python3
"""
Integrate AI_ENHANCED_ORGANIZATION/DOWNLOADS (audio + images) into ALBUMS.
- Copies or moves tracks and cover art into matching album folders (by title)
- Creates new album folders for items that don't have a match
- Handles filename conflicts

Usage:
  python3 integrate_downloads_into_albums.py          # dry run, audio only
  python3 integrate_downloads_into_albums.py --apply  # copy audio
  python3 integrate_downloads_into_albums.py --apply --images  # audio + images
  python3 integrate_downloads_into_albums.py --apply --images --move  # move (consolidate, empty DOWNLOADS)
"""

import re
import shutil
import sys
from pathlib import Path

ALBUMS_DIR = Path(__file__).parent / "ALBUMS"
DOWNLOADS = Path(__file__).parent / "AI_ENHANCED_ORGANIZATION" / "DOWNLOADS"
DOWNLOADS_AUDIO = DOWNLOADS / "audio"
DOWNLOADS_IMAGES = DOWNLOADS / "images"


def normalize(s: str) -> str:
    """Normalize for comparison."""
    s = re.sub(r"[_\-]+", " ", s.lower())
    s = re.sub(r"\s+", " ", s.strip())
    s = re.sub(r"[^\w\s]", "", s)
    return s


def title_to_folder_name(title: str) -> str:
    """Convert 'The Patchwork Prophecy' -> 'The_Patchwork_Prophecy'."""
    s = re.sub(r'[<>:"/\\|?*]', "", title)
    s = re.sub(r"\s+", "_", s.strip())
    return s or "Untitled"


def get_album_map() -> dict[str, Path]:
    """Map normalized title -> album folder path."""
    m = {}
    for d in ALBUMS_DIR.iterdir():
        if d.is_dir() and not d.name.startswith("."):
            key = normalize(d.name)
            if key not in m:
                m[key] = d
    return m


def integrate_dir(
    src_dir: Path,
    extensions: tuple,
    dry_run: bool,
    album_map: dict,
    mode: str,
    move: bool = False,
) -> tuple:
    """Copy or move files from src_dir into ALBUMS. Returns (copied, created, skipped, consolidated, errors)."""
    copied = created = skipped = consolidated = 0
    errors = []

    for f in sorted(src_dir.iterdir()):
        if not f.is_file() or f.suffix.lower() not in extensions:
            continue

        stem = f.stem
        base = re.sub(r"_\d+$", "", stem)
        key = normalize(base)

        target_dir = album_map.get(key)
        if target_dir is None:
            folder_name = title_to_folder_name(base)
            target_dir = ALBUMS_DIR / folder_name
            if not target_dir.exists():
                if not dry_run:
                    target_dir.mkdir(parents=True)
                print(f"  [NEW] {target_dir.name}/")
                created += 1
            album_map[key] = target_dir  # cache for same-title files

        target_file = target_dir / f.name
        if target_file.exists() and target_file.stat().st_size == f.stat().st_size:
            if move and not dry_run:
                f.unlink()  # remove duplicate from source
                consolidated += 1
            else:
                skipped += 1
            continue

        if target_file.exists():
            i = 1
            while target_file.exists():
                target_file = target_dir / f"{f.stem}_{i}{f.suffix}"
                i += 1

        try:
            if not dry_run:
                if move:
                    shutil.move(str(f), str(target_file))
                else:
                    shutil.copy2(str(f), str(target_file))
            print(f"  {'Moved' if move else 'Copied'} {f.name} -> {target_dir.name}/")
            copied += 1
        except OSError as e:
            errors.append(f"{f.name}: {e}")

    return copied, created, skipped, consolidated, errors


def integrate(dry_run: bool = True, include_images: bool = False, move: bool = False):
    """Copy or move DOWNLOADS audio (and optionally images) into ALBUMS."""
    album_map = get_album_map()
    mode = "DRY RUN - " if dry_run else ""
    total_copied = total_created = total_skipped = total_consolidated = 0
    all_errors = []

    if DOWNLOADS_AUDIO.exists():
        print(f"{mode}Integrating {DOWNLOADS_AUDIO} into {ALBUMS_DIR} ({'move' if move else 'copy'})\n")
        c, cr, s, co, e = integrate_dir(
            DOWNLOADS_AUDIO,
            (".mp3", ".wav", ".flac", ".m4a"),
            dry_run,
            album_map,
            mode,
            move,
        )
        total_copied += c
        total_created += cr
        total_skipped += s
        total_consolidated += co
        all_errors.extend(e)
        print(f"\n  Audio: copied={c}, created={cr}, skipped={s}" + (f", consolidated={co}" if co else ""))
    else:
        print(f"DOWNLOADS audio not found: {DOWNLOADS_AUDIO}")

    if include_images and DOWNLOADS_IMAGES.exists():
        print(f"\n{mode}Integrating {DOWNLOADS_IMAGES} into {ALBUMS_DIR} ({'move' if move else 'copy'})\n")
        c, cr, s, co, e = integrate_dir(
            DOWNLOADS_IMAGES,
            (".jpeg", ".jpg", ".png", ".webp"),
            dry_run,
            album_map,
            mode,
            move,
        )
        total_copied += c
        total_created += cr
        total_skipped += s
        total_consolidated += co
        all_errors.extend(e)
        print(f"\n  Images: copied={c}, created={cr}, skipped={s}" + (f", consolidated={co}" if co else ""))
    elif include_images:
        print(f"DOWNLOADS images not found: {DOWNLOADS_IMAGES}")

    print("\n--- Summary ---")
    print(f"  Moved/copied: {total_copied}")
    print(f"  New folders: {total_created}")
    print(f"  Skipped (existing): {total_skipped}")
    if total_consolidated:
        print(f"  Consolidated (removed dupes from DOWNLOADS): {total_consolidated}")
    if all_errors:
        print(f"  Errors: {len(all_errors)}")
        for err in all_errors[:5]:
            print(f"    {err}")
    if dry_run:
        print("\nRun with --apply to execute. Add --images for cover art.")


if __name__ == "__main__":
    dry_run = "--apply" not in sys.argv
    include_images = "--images" in sys.argv
    move = "--move" in sys.argv
    integrate(dry_run=dry_run, include_images=include_images, move=move)
