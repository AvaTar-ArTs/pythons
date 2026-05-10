#!/usr/bin/env python3
"""
Remove duplicate MP3s from ALBUMS (by content hash).
Keeps one copy per duplicate set, removes the rest.

Usage:
  python3 remove_duplicate_mp3s.py          # dry run
  python3 remove_duplicate_mp3s.py --apply  # delete duplicates
"""

import hashlib
import sys
from pathlib import Path

ALBUMS_DIR = Path(__file__).parent / "ALBUMS"
CHUNK = 64 * 1024  # 64KB for hashing


def file_hash(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(CHUNK):
            h.update(chunk)
    return h.hexdigest()


def find_duplicates() -> dict[str, list[Path]]:
    """Group MP3s by content hash. Returns {hash: [paths]}."""
    groups = {}
    for f in ALBUMS_DIR.rglob("*.mp3"):
        if not f.is_file():
            continue
        try:
            h = file_hash(f)
            groups.setdefault(h, []).append(f)
        except OSError:
            pass
    return {h: sorted(paths) for h, paths in groups.items() if len(paths) >= 2}


def main():
    dry_run = "--apply" not in sys.argv
    mode = "DRY RUN - " if dry_run else ""
    print(f"{mode}Finding duplicate MP3s in {ALBUMS_DIR}\n")

    groups = find_duplicates()
    total_dupes = sum(len(paths) - 1 for paths in groups.values())
    total_bytes = 0

    print(f"Found {len(groups)} duplicate sets ({total_dupes} files to remove)\n")

    removed = 0
    for h, paths in sorted(groups.items(), key=lambda x: -len(x[1])):
        paths[0]
        delete = paths[1:]
        for p in delete:
            size = p.stat().st_size
            total_bytes += size
            if dry_run:
                print(f"  [would remove] {p.relative_to(ALBUMS_DIR)} ({size // 1024} KB)")
            else:
                try:
                    p.unlink()
                    print(f"  Removed {p.relative_to(ALBUMS_DIR)}")
                    removed += 1
                except OSError as e:
                    print(f"  Error: {p.name}: {e}")

    print("\n--- Summary ---")
    print(f"  Duplicate sets: {len(groups)}")
    print(f"  Files {'to remove' if dry_run else 'removed'}: {total_dupes}")
    print(f"  Space freed: {total_bytes / (1024 * 1024):.1f} MB")
    if dry_run:
        print("\nRun with --apply to delete duplicates.")


if __name__ == "__main__":
    main()
