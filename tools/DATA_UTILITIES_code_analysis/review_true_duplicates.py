#!/usr/bin/env python3
"""from pathlib import Path
import csv
import hashlib

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
Review True Duplicates
Identify and prepare cleanup for the 8 true duplicate groups
"""


DATA_DIR = Path(__file__).parent.parent / "DATA"
ANALYSIS_DIR = DATA_DIR / "INTELLIGENT_ANALYSIS"


def get_file_hash(filepath):
    """Calculate MD5 hash of file"""
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_mp3_info(filepath):
    """Extract MP3 metadata"""
    try:
        audio = MP3(filepath, ID3=EasyID3)
        return {
            "duration": audio.info.length,
            "bitrate": audio.info.bitrate,
            "size_mb": filepath.stat().st_size / (1024 * 1024),
            "title": audio.get("title", [""])[0],
            "artist": audio.get("artist", [""])[0],
        }
    except:
        return {
            "duration": 0,
            "bitrate": 0,
            "size_mb": filepath.stat().st_size / (1024 * 1024),
            "title": "",
            "artist": "",
        }


def review_duplicates():
    """Review the 8 true duplicate groups"""
    print("=" * 80)
    print("🔍 REVIEWING 8 TRUE DUPLICATE GROUPS")
    print("=" * 80)

    # Load the true duplicates CSV
    dup_csv = ANALYSIS_DIR / "true_duplicates_to_delete.csv"
    if not dup_csv.exists():
        print("❌ No true duplicates file found")
        return

    # Read duplicate groups
    groups = {}
    with open(dup_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row["Title"]
            if title not in groups:
                groups[title] = row

    print(f"\n📊 Found {len(groups)} duplicate groups to review\n")

    # Find and analyze each group
    base_dir = Path("/Users/steven/Music/nocTurneMeLoDieS")
    cleanup_plan = []

    for i, (title, info) in enumerate(groups.items(), 1):
        print(f"\n{'='*80}")
        print(f"GROUP {i}: {title}")
        print(f"{'='*80}")
        print(f"Files found: {info['Total_Files']}")
        print(f"Reason: {info['Reason']}")
        print(f"Action: {info['Action']}")

        # Search for these files
        files_found = list(base_dir.rglob(f"*{title}*.mp3"))

        if not files_found:
            print(f"⚠️  No files found for '{title}'")
            continue

        print(f"\n📁 Found {len(files_found)} matching files:")

        # Analyze each file
        file_data = []
        for f in files_found:
            hash_val = get_file_hash(f)
            info = get_mp3_info(f)
            file_data.append({"path": f, "hash": hash_val, **info})
            print(f"\n  📄 {f.name}")
            print(f"     Path: {f.parent.name}/")
            print(f"     Size: {info['size_mb']:.2f} MB")
            print(f"     Duration: {info['duration']:.0f}s")
            print(f"     Hash: {hash_val[:12]}...")

        # Group by hash
        hash_groups = {}
        for fd in file_data:
            h = fd["hash"]
            if h not in hash_groups:
                hash_groups[h] = []
            hash_groups[h].append(fd)

        print(f"\n🔑 Unique hashes: {len(hash_groups)}")

        # Identify duplicates
        for hash_val, files in hash_groups.items():
            if len(files) > 1:
                print(f"\n  ⚠️  EXACT DUPLICATES (hash {hash_val[:12]}...):")
                # Keep the first one (usually in the main album folder)
                keep = files[0]
                delete = files[1:]

                print(f"     ✅ KEEP: {keep['path']}")
                for d in delete:
                    print(f"     🗑️  DELETE: {d['path']}")
                    cleanup_plan.append(
                        {
                            "title": title,
                            "keep": str(keep["path"]),
                            "delete": str(d["path"]),
                            "hash": hash_val,
                            "size_mb": d["size_mb"],
                        },
                    )

        if len(hash_groups) == len(file_data):
            print("\n  ✅ All files are unique (different versions - KEEP ALL)")

    # Save cleanup plan
    if cleanup_plan:
        plan_file = DATA_DIR / "TRUE_DUPLICATES_CLEANUP_PLAN.csv"
        with open(plan_file, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["title", "keep", "delete", "hash", "size_mb"],
            )
            writer.writeheader()
            writer.writerows(cleanup_plan)

        total_size = sum(p["size_mb"] for p in cleanup_plan)

        print("\n" + "=" * 80)
        print("✅ CLEANUP PLAN CREATED")
        print("=" * 80)
        print(f"\n📁 Saved to: {plan_file}")
        print("\n📊 Summary:")
        print(f"   • Files to delete: {len(cleanup_plan)}")
        print(f"   • Space to save: {total_size:.2f} MB")
    else:
        print("\n" + "=" * 80)
        print("✅ NO EXACT DUPLICATES FOUND")
        print("=" * 80)
        print("\nAll files appear to be different versions - keeping all!")


if __name__ == "__main__":
    review_duplicates()
