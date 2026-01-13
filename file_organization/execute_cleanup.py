#!/usr/bin/env python3
"""from pathlib import Path
import csv
import shutil
Execute the cleanup plan from FILENAME_CLEANUP_MAPPING.csv
1. Delete duplicates from mp3s folder
2. Rename files in album folders
"""


BASE_DIR = Path("/Users/steven/Music/nocTurneMeLoDieS")
MAPPING_CSV = BASE_DIR / "FILENAME_CLEANUP_MAPPING.csv"
BACKUP_DIR = BASE_DIR / "CLEANUP_BACKUP"


def read_mapping():
    """Read the mapping CSV"""
    print(f"?? Reading mapping: {MAPPING_CSV.name}\n")

    mappings = []
    with open(MAPPING_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        mappings = list(reader)

    return mappings


def delete_duplicates(mappings):
    """Delete duplicate files from mp3s folder"""
    duplicates = [m for m in mappings if m["action"] == "DUPLICATE_DELETE"]

    if not duplicates:
        print("? No duplicates to delete\n")
        return 0

    print(f"???  Deleting {len(duplicates)} duplicates from mp3s folder...")
    print()

    deleted = 0
    errors = []

    for dup in duplicates:
        file_path = Path(dup["full_path"])

        if not file_path.exists():
            print(f"  ??  Not found: {file_path.name}")
            continue

        try:
            file_path.unlink()
            deleted += 1
            if deleted <= 10 or deleted % 50 == 0:
                print(f"  ? [{deleted}/{len(duplicates)}] Deleted: {file_path.name}")
        except Exception as e:
            errors.append(f"{file_path.name}: {e}")
            print(f"  ? Error deleting {file_path.name}: {e}")

    print(f"\n  Deleted {deleted} duplicates\n")

    if errors:
        print(f"  ??  {len(errors)} errors occurred")

    return deleted


def rename_files(mappings):
    """Rename files in album folders"""
    to_rename = [
        m
        for m in mappings
        if m["needs_rename"] == "YES" and m["location"] == "ALBUM_FOLDER"
    ]

    if not to_rename:
        print("? No files need renaming\n")
        return 0

    print(f"???  Renaming {len(to_rename)} files in album folders...")
    print()

    renamed = 0
    errors = []

    for item in to_rename:
        old_path = Path(item["full_path"])

        if not old_path.exists():
            print(f"  ??  Not found: {old_path.name}")
            continue

        new_path = old_path.parent / item["cleaned_filename"]

        # Skip if target already exists
        if new_path.exists():
            print(f"  ??  Target exists: {new_path.name}")
            continue

        try:
            old_path.rename(new_path)
            renamed += 1
            if renamed <= 10 or renamed % 50 == 0:
                print(f"  ? [{renamed}/{len(to_rename)}] {old_path.name}")
                print(f"     ? {new_path.name}")
        except Exception as e:
            errors.append(f"{old_path.name}: {e}")
            print(f"  ? Error renaming {old_path.name}: {e}")

    print(f"\n  Renamed {renamed} files\n")

    if errors:
        print(f"  ??  {len(errors)} errors occurred")

    return renamed


def main():
    print("=" * 70)
    print("?? EXECUTE FILENAME CLEANUP")
    print("=" * 70)
    print()

    # Read mapping
    mappings = read_mapping()

    # Count actions
    duplicates = sum(1 for m in mappings if m["action"] == "DUPLICATE_DELETE")
    renames = sum(
        1
        for m in mappings
        if m["needs_rename"] == "YES" and m["location"] == "ALBUM_FOLDER"
    )

    print("?? Planned actions:")
    print(f"   ? Delete duplicates from mp3s: {duplicates}")
    print(f"   ? Rename files in albums: {renames}")
    print()

    # Confirm
    response = input("Proceed? (yes/no): ").strip().lower()
    if response != "yes":
        print("\n? Cancelled")
        return

    print()
    print("=" * 70)
    print()

    # Delete duplicates
    deleted = delete_duplicates(mappings)

    print("=" * 70)
    print()

    # Rename files
    renamed = rename_files(mappings)

    print("=" * 70)
    print("? CLEANUP COMPLETE")
    print("=" * 70)
    print(f"Duplicates deleted: {deleted}")
    print(f"Files renamed: {renamed}")
    print("=" * 70)


if __name__ == "__main__":
    main()
