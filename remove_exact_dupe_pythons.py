#!/usr/bin/env python3
"""
remove_exact_dupe_pythons.py
Finds and removes exact duplicate .py files across the home directory.

Keeps the file in the "best" location (priority: ~/pythons > ~/AVATARARTS > other)
and removes identical copies elsewhere.

Usage:
    python remove_exact_dupe_pythons.py                 # Dry run (report only)
    python remove_exact_dupe_pythons.py --execute       # Actually delete dupes
    python remove_exact_dupe_pythons.py --backup-dirs   # Focus on backup dirs only
"""

import argparse
import hashlib
import os
from pathlib import Path
from collections import defaultdict

HOME = Path.home()

# Skip patterns (framework/venv/system files)
SKIP_DIRS = {
    ".venv", "venv", "__pycache__", ".git", "node_modules",
    "site-packages", "google-cloud-sdk", ".local", ".pyenv",
    ".Trash", ".cache", "Library", ".npm", ".cargo", ".bun",
}

# Priority order for keeping files (higher = prefer to keep)
LOCATION_PRIORITY = {
    "pythons": 100,
    "AutoTagger": 90,
    "AVATARARTS": 80,
    "IntelliHub": 70,
    ".env.d": 60,
    "clean": 50,
    "Documents": 40,
    "Downloads": 30,
    "Pictures": 20,
    "Movies": 20,
    "Music": 20,
}


def file_hash(filepath: Path) -> str:
    """SHA256 hash of file contents."""
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, PermissionError):
        return ""


def should_skip(path: Path) -> bool:
    """Check if path contains a skip directory."""
    return any(part in SKIP_DIRS for part in path.parts)


def get_priority(filepath: Path) -> int:
    """Get location priority for a file."""
    try:
        rel = filepath.relative_to(HOME)
        top = rel.parts[0] if rel.parts else ""

        # Backup directories get lowest priority
        if top.startswith("AVATARARTS_BACKUP"):
            return 0
        if top.startswith("AVATARARTS_DIABLO"):
            return 5

        return LOCATION_PRIORITY.get(top, 10)
    except ValueError:
        return 10


def scan_and_hash(
    root: Path,
    max_depth: int = 8,
    backup_only: bool = False
) -> dict[str, list[Path]]:
    """Scan directory tree and group files by content hash."""
    hash_groups: dict[str, list[Path]] = defaultdict(list)

    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)

        depth = len(current.relative_to(root).parts)
        if depth > max_depth:
            dirnames.clear()
            continue

        # Prune skip dirs
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        # If backup-only mode, skip non-backup directories at depth 1
        if backup_only and depth == 0:
            dirnames[:] = [d for d in dirnames
                           if d.startswith("AVATARARTS_BACKUP")
                           or d == "AVATARARTS"
                           or d == "pythons"]

        for fname in filenames:
            if not fname.endswith(".py"):
                continue

            filepath = current / fname
            if should_skip(filepath):
                continue

            h = file_hash(filepath)
            if h:
                hash_groups[h].append(filepath)

    return hash_groups


def find_duplicates(hash_groups: dict[str, list[Path]]) -> list[tuple[Path, list[Path]]]:
    """Determine which files to keep and which to remove."""
    results = []

    for h, files in hash_groups.items():
        if len(files) < 2:
            continue

        # Sort by priority (highest first), then by path length (shorter preferred)
        files.sort(key=lambda f: (-get_priority(f), len(str(f))))

        keep = files[0]
        remove = files[1:]

        results.append((keep, remove))

    return results


def main():
    parser = argparse.ArgumentParser(description="Remove exact duplicate Python files")
    parser.add_argument("--execute", action="store_true",
                        help="Actually delete files (default is dry run)")
    parser.add_argument("--backup-dirs", action="store_true",
                        help="Only scan backup directories + primary locations")
    parser.add_argument("--max-depth", type=int, default=8,
                        help="Max scan depth (default: 8)")
    args = parser.parse_args()

    mode = "EXECUTE" if args.execute else "DRY RUN"
    print(f"=== Duplicate Python File Removal ({mode}) ===")
    print(f"Scanning {HOME}...")
    print()

    hash_groups = scan_and_hash(HOME, max_depth=args.max_depth,
                                backup_only=args.backup_dirs)

    duplicates = find_duplicates(hash_groups)

    if not duplicates:
        print("No exact duplicates found.")
        return

    total_remove = 0
    total_bytes = 0

    for keep, removes in sorted(duplicates, key=lambda x: len(x[1]), reverse=True):
        rel_keep = keep.relative_to(HOME)
        print(f"KEEP: {rel_keep}")
        for r in removes:
            rel_r = r.relative_to(HOME)
            size = r.stat().st_size
            total_bytes += size
            total_remove += 1
            print(f"  DEL: {rel_r} ({size/1024:.0f}KB)")

            if args.execute:
                try:
                    r.unlink()
                except OSError as e:
                    print(f"  ERROR: {e}")
        print()

    print("=" * 60)
    print(f"Duplicate groups: {len(duplicates)}")
    print(f"Files to remove: {total_remove}")
    print(f"Space to reclaim: {total_bytes / 1024 / 1024:.1f} MB")

    if not args.execute:
        print("\nThis was a DRY RUN. Use --execute to actually delete files.")
    else:
        print(f"\nRemoved {total_remove} duplicate files.")


if __name__ == "__main__":
    main()
