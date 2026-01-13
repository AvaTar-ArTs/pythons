#!/usr/bin/env python3
"""from pathlib import Path
import shutil
Undo the cleanup - return folders to original locations
"""


def undo_cleanup():
    """Return folders to original state"""
    nocturne = Path.home() / "Music" / "nocTurneMeLoDieS"
    workspace = Path.home() / "workspace" / "music-empire"

    print("\n" + "=" * 80)
    print("  UNDO CLEANUP - Returning Folders")
    print("=" * 80 + "\n")

    moves = []

    # From MUSIC/ back to root
    music_dir = nocturne / "MUSIC"
    if music_dir.exists():
        for item in music_dir.iterdir():
            if item.is_dir() or item.is_file():
                moves.append((item, nocturne / item.name))

    # From TOOLS/ back to root
    tools_dir = nocturne / "TOOLS"
    if tools_dir.exists():
        for item in tools_dir.iterdir():
            if item.is_dir() or item.is_file():
                moves.append((item, nocturne / item.name))

    # From DOCS/ back to root
    docs_dir = nocturne / "DOCS"
    if docs_dir.exists():
        for item in docs_dir.iterdir():
            if item.is_dir() or item.is_file():
                moves.append((item, nocturne / item.name))

    # From DATA/ back to root
    data_dir = nocturne / "DATA"
    if data_dir.exists():
        for item in data_dir.iterdir():
            if item.is_dir() or item.is_file():
                moves.append((item, nocturne / item.name))

    # From MEDIA/ back to root
    media_dir = nocturne / "MEDIA"
    if media_dir.exists():
        for item in media_dir.iterdir():
            if item.is_dir() or item.is_file():
                moves.append((item, nocturne / item.name))

    # From ARCHIVES/ back to root
    archives_dir = nocturne / "ARCHIVES"
    if archives_dir.exists():
        for item in archives_dir.iterdir():
            if item.is_dir() or item.is_file():
                if item.name != "old_files_20251104":  # Keep this archived
                    moves.append((item, nocturne / item.name))

    # From workspace back to nocturne
    if workspace.exists():
        for item in workspace.iterdir():
            if item.is_dir():
                moves.append((item, nocturne / item.name))

    print(f"Will return {len(moves)} items to original locations\n")

    response = input("Proceed? (yes/no): ").strip().lower()

    if response != "yes":
        print("\nCancelled.")
        return

    print("\n" + "=" * 80)
    print("  RETURNING FOLDERS")
    print("=" * 80 + "\n")

    moved = 0
    errors = 0

    for source, target in moves:
        if not source.exists():
            continue

        if target.exists():
            print(f"??  Skip: {source.name} (already exists)")
            errors += 1
            continue

        try:
            shutil.move(str(source), str(target))
            print(f"? {source.name}")
            moved += 1
        except Exception as e:
            print(f"? Error: {source.name} - {e}")
            errors += 1

    print("\n" + "=" * 80)
    print("  ? COMPLETE!")
    print("=" * 80 + "\n")

    print(f"? Returned {moved} items")
    print(f"??  Skipped {errors} items")
    print()

    # Remove empty organizational folders
    print("Cleaning up empty folders...")
    for folder in [music_dir, tools_dir, docs_dir, data_dir, media_dir]:
        if folder.exists() and not any(folder.iterdir()):
            folder.rmdir()
            print(f"  ? Removed empty: {folder.name}/")

    print("\n? Folders returned to original state!")


if __name__ == "__main__":
    undo_cleanup()
