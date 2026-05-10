#!/usr/bin/env python3
"""
Fix Untitled_* and Unmapped_UUIDs: map UUIDs to titles from Suno exports,
move files to correct album folders, consolidate unknowns.

Usage:
  python3 fix_untitled_uuid_folders.py          # dry run
  python3 fix_untitled_uuid_folders.py --apply  # execute
"""

import csv
import re
import shutil
import sys
from pathlib import Path

PROJECT = Path(__file__).parent
DATA_DIR = PROJECT / "AI_ENHANCED_ORGANIZATION" / "DATA"
ALBUMS_DIR = PROJECT / "ALBUMS"

# Match Untitled_XXXXXXXX (8 hex) or full UUID with underscores
UNTITLED_PREFIX = re.compile(r"^Untitled_([a-f0-9]{8})$", re.I)
FULL_UUID_UNDERSCORE = re.compile(r"^([a-f0-9]{8}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{12})$", re.I)


def sanitize_title(s: str) -> str:
    s = re.sub(r"^#+\s*", "", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"[\u2600-\u27BF\U0001F300-\U0001F9FF\uFE0F⭐️🌀]+", "", s)  # emoji
    s = re.sub(r'["\'\n\r\t<>:|?*\\/]', "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:120] if s else "Untitled"


def title_to_folder(title: str) -> str:
    # Strip emoji and other non-ASCII that could create weird folder names
    s = re.sub(r"[\u2600-\u27BF\U0001F300-\U0001F9FF]", "", title)
    s = re.sub(r'[<>:"/\\|?*]', "", s)
    s = re.sub(r"\s+", "_", s.strip().strip("_"))
    return s or "Untitled"


def load_uuid_mapping() -> dict[str, str]:
    """UUID (lower, with - or _) -> sanitized title. Also 8-char prefix -> title."""
    mapping: dict[str, str] = {}
    for p in sorted(DATA_DIR.glob("suno-export-*.csv")):
        with open(p, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                uid = (row.get("id") or "").strip()
                title = (row.get("title") or "").strip()
                if not uid or not title:
                    continue
                clean = sanitize_title(title)
                # Full UUID (hyphens)
                mapping[uid.lower()] = clean
                # Full UUID with underscores
                mapping[uid.lower().replace("-", "_")] = clean
                # 8-char prefix for Untitled_XXXXXXXX
                prefix = uid[:8].lower()
                mapping[prefix] = clean
    return mapping


def get_target_folder(title: str) -> Path:
    """Resolve target album folder, creating if needed."""
    folder_name = title_to_folder(title)
    return ALBUMS_DIR / folder_name


def move_to_album(src_dir: Path, target_dir: Path, dry_run: bool, used: dict[str, int]) -> int:
    """Move all media files from src_dir to target_dir. Returns count moved."""
    moved = 0
    for f in src_dir.iterdir():
        if not f.is_file():
            continue
        ext = f.suffix.lower()
        if ext not in (".mp3", ".m4a", ".wav", ".jpg", ".jpeg", ".png", ".flac"):
            continue
        base = f.stem
        # Avoid overwrite: use base or base_N
        key = base
        idx = used.get(key, 0)
        used[key] = idx + 1
        dest_name = f"{base}_{idx}{ext}" if idx else f"{base}{ext}"
        dest = target_dir / dest_name
        if dest.exists():
            while dest.exists():
                idx += 1
                used[key] = idx
                dest = target_dir / f"{base}_{idx}{ext}"
        if dry_run:
            print(f"  [would move] {src_dir.name}/{f.name} -> {target_dir.name}/{dest.name}")
        else:
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), str(dest))
            print(f"  Moved {src_dir.name}/{f.name} -> {target_dir.name}/{dest.name}")
        moved += 1
    return moved


def main():
    dry_run = "--apply" not in sys.argv
    mode = "DRY RUN - " if dry_run else ""
    print(f"{mode}Fixing Untitled_* and Unmapped_UUIDs\n")

    mapping = load_uuid_mapping()
    print(f"Loaded {len(mapping)} UUID->title mappings from Suno exports\n")

    # Folders to process: Untitled_*, full UUID folders, Unmapped_UUIDs subdirs
    to_process: list[tuple[Path, str | None]] = []  # (folder_path, title or None)

    for d in ALBUMS_DIR.iterdir():
        if not d.is_dir() or d.name.startswith("."):
            continue
        name = d.name

        # Skip main Untitled for now - we'll handle its subdirs and direct files
        if name == "Untitled":
            continue
        if name == "Unmapped_UUIDs":
            # Process subdirs inside Unmapped_UUIDs
            for sub in d.iterdir():
                if sub.is_dir():
                    sub_name = sub.name
                    if FULL_UUID_UNDERSCORE.match(sub_name):
                        uid = sub_name.replace("_", "-").lower()
                        title = mapping.get(uid) or mapping.get(sub_name.lower())
                        to_process.append((sub, title))
                    else:
                        to_process.append((sub, None))
            continue

        # Untitled_XXXXXXXX
        m = UNTITLED_PREFIX.match(name)
        if m:
            prefix = m.group(1).lower()
            title = mapping.get(prefix)
            to_process.append((d, title))
            continue

        # Full UUID with underscores (standalone folder)
        if FULL_UUID_UNDERSCORE.match(name):
            uid = name.replace("_", "-").lower()
            title = mapping.get(uid) or mapping.get(name.lower())
            to_process.append((d, title))
            continue

    # Process main Untitled folder: subdirs and loose files
    untitled_dir = ALBUMS_DIR / "Untitled"
    if untitled_dir.exists():
        for item in untitled_dir.iterdir():
            if item.is_dir():
                sub_name = item.name
                m = UNTITLED_PREFIX.match(sub_name)
                if m:
                    prefix = m.group(1).lower()
                    title = mapping.get(prefix)
                    to_process.append((item, title))
                elif FULL_UUID_UNDERSCORE.match(sub_name):
                    uid = sub_name.replace("_", "-").lower()
                    title = mapping.get(uid) or mapping.get(sub_name.lower())
                    to_process.append((item, title))
                else:
                    to_process.append((item, None))

    # Execute: move mapped to albums, consolidate unmapped
    moved_total = 0
    used_per_album: dict[str, dict[str, int]] = {}
    unknown_dir = ALBUMS_DIR / "Unmapped_UUIDs"
    if not dry_run:
        unknown_dir.mkdir(exist_ok=True)

    for folder, title in to_process:
        if title:
            target = get_target_folder(title)
            used = used_per_album.setdefault(str(target), {})
            n = move_to_album(folder, target, dry_run, used)
            if n:
                print(f"\n[{folder.name}] -> {target.name}/ ({n} files)")
                moved_total += n
        else:
            # Unknown: move contents to Unmapped_UUIDs (flatten)
            for f in folder.iterdir():
                if not f.is_file():
                    continue
                ext = f.suffix.lower()
                if ext not in (".mp3", ".m4a", ".wav", ".jpg", ".jpeg", ".png"):
                    continue
                dest = unknown_dir / f.name
                if dest.exists():
                    stem, suf = dest.stem, dest.suffix
                    i = 1
                    while dest.exists():
                        dest = unknown_dir / f"{stem}_{i}{suf}"
                        i += 1
                if dry_run:
                    print(f"  [would move] {folder.name}/{f.name} -> Unmapped_UUIDs/")
                else:
                    shutil.move(str(f), str(dest))
                    print(f"  Moved {folder.name}/{f.name} -> Unmapped_UUIDs/")
                moved_total += 1

        # Remove empty folder
        if not dry_run and folder.exists() and folder.is_dir():
            try:
                if not any(folder.iterdir()):
                    folder.rmdir()
                    print(f"  Removed empty {folder.name}/")
            except OSError:
                pass

    # Consolidate main Untitled folder: move known UUID files to albums, rest to Unmapped
    if untitled_dir.exists():
        for f in list(untitled_dir.iterdir()):
            if not f.is_file():
                continue
            stem = f.stem
            ext = f.suffix.lower()
            if ext not in (".mp3", ".m4a", ".wav", ".jpg", ".jpeg", ".png"):
                continue
            # Check for UUID in filename: Untitled_XXXXXXXX_1 or similar
            m = re.search(r"([a-f0-9]{8})", stem, re.I)
            title = None
            if m:
                prefix = m.group(1).lower()
                title = mapping.get(prefix)
            if title:
                target = get_target_folder(title)
                used = used_per_album.setdefault(str(target), {})
                base = f.stem
                key = base
                idx = used.get(key, 0)
                used[key] = idx + 1
                dest_name = f"{base}_{idx}{ext}" if idx else f.name
                dest = target / dest_name
                if dest.exists():
                    while dest.exists():
                        idx += 1
                        dest = target / f"{base}_{idx}{ext}"
                if dry_run:
                    print(f"  [would move] Untitled/{f.name} -> {target.name}/")
                else:
                    target.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(f), str(dest))
                    print(f"  Moved Untitled/{f.name} -> {target.name}/")
                moved_total += 1
            else:
                dest = unknown_dir / f.name
                if dest.exists():
                    stem2, suf = dest.stem, dest.suffix
                    i = 1
                    while dest.exists():
                        dest = unknown_dir / f"{stem2}_{i}{suf}"
                        i += 1
                if dry_run:
                    print(f"  [would move] Untitled/{f.name} -> Unmapped_UUIDs/")
                else:
                    shutil.move(str(f), str(dest))
                    print(f"  Moved Untitled/{f.name} -> Unmapped_UUIDs/")
                moved_total += 1

        if not dry_run:
            try:
                remaining = list(untitled_dir.iterdir())
                if not remaining:
                    untitled_dir.rmdir()
                    print("  Removed empty Untitled/")
                else:
                    for r in remaining:
                        if r.is_dir():
                            shutil.rmtree(r)
                    if not any(untitled_dir.iterdir()):
                        untitled_dir.rmdir()
            except OSError:
                pass

    print("\n--- Summary ---")
    print(f"  Files moved: {moved_total}")
    if dry_run:
        print("  Run with --apply to execute.")


if __name__ == "__main__":
    main()
