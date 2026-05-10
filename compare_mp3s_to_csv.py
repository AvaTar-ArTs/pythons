#!/usr/bin/env python3
"""
Compare ALBUMS MP3s to CSV inventory and metadata.
Reports: in both, only in ALBUMS (not in CSV), only in CSV (missing from ALBUMS).
"""

import csv
import re
from pathlib import Path

ALBUMS_DIR = Path(__file__).parent / "ALBUMS"
DATA_DIR = Path(__file__).parent / "AI_ENHANCED_ORGANIZATION" / "DATA"
OUTPUT_JSON = DATA_DIR / "mp3_csv_comparison.json"


def normalize_rel(p: Path) -> str:
    """Normalize path for comparison: Folder/file.mp3"""
    s = str(p).replace("\\", "/")
    if s.startswith("./"):
        s = s[2:]
    return s


def get_albums_mp3s() -> set[str]:
    """All MP3s in ALBUMS as relative paths (folder/file.mp3)."""
    rel = set()
    for f in ALBUMS_DIR.rglob("*.mp3"):
        if f.is_file():
            r = f.relative_to(ALBUMS_DIR)
            rel.add(normalize_rel(r))
    return rel


def get_csv_mp3_paths() -> set[str]:
    """MP3 paths from COMPLETE_MUSIC_COLLECTION_INVENTORY (relative to ALBUMS)."""
    path = DATA_DIR / "COMPLETE_MUSIC_COLLECTION_INVENTORY.csv"
    if not path.exists():
        return set()
    rel = set()
    prefix = str(ALBUMS_DIR) + "/"
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            fp = (row.get("File Path") or "").strip()
            if not fp.endswith(".mp3"):
                continue
            if fp.startswith(prefix):
                r = fp[len(prefix) :]
                rel.add(normalize_rel(Path(r)))
            elif "/ALBUMS/" in fp:
                parts = fp.split("/ALBUMS/", 1)
                if len(parts) == 2:
                    rel.add(normalize_rel(Path(parts[1])))
    return rel


def get_albums_metadata_folders() -> set[str]:
    """Folder names from albums-metadata (Album Name + Related Tracks)."""
    path = DATA_DIR / "albums-metadata.csv"
    if not path.exists():
        return set()
    folders = set()
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            album = (row.get("Album Name") or "").strip()
            if album:
                folders.add(re.sub(r"\s+", "_", album))
            related = (row.get("Related Tracks") or "").strip()
            for part in re.split(r"[,;]+", related):
                part = part.strip().strip("_")
                if part:
                    folders.add(part)
    return folders


def get_suno_titles() -> set[str]:
    """Song titles from Suno exports (normalized to folder-style)."""
    titles = set()
    for p in DATA_DIR.glob("suno-export-*.csv"):
        try:
            with open(p, encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    t = (row.get("title") or "").strip()
                    t = re.sub(r"^#+\s*|\*\*|🌀|" "", "", t).strip()
                    if t:
                        titles.add(re.sub(r"\s+", "_", re.sub(r'[<>:"/\\|?*]', "", t)))
        except Exception:
            pass
    return titles


def main():
    mp3s = get_albums_mp3s()
    csv_paths = get_csv_mp3_paths()
    meta_folders = get_albums_metadata_folders()
    suno = get_suno_titles()

    in_both = mp3s & csv_paths
    only_mp3s = mp3s - csv_paths
    only_csv = csv_paths - mp3s

    # Album folders that have MP3s
    mp3_folders = {str(Path(p).parent) for p in mp3s}
    in_metadata = mp3_folders & meta_folders
    mp3_folders & suno

    print("=" * 60)
    print("MP3 vs CSV Comparison")
    print("=" * 60)
    print(f"\nALBUMS MP3s:        {len(mp3s)}")
    print(f"CSV (inventory):    {len(csv_paths)}")
    print(f"albums-metadata:    {len(meta_folders)} folders")
    print(f"Suno titles:        {len(suno)}")

    print("\n--- IN BOTH (MP3 in inventory CSV) ---")
    print(f"Count: {len(in_both)}")

    print("\n--- ONLY IN ALBUMS (not in inventory CSV) ---")
    print(f"Count: {len(only_mp3s)}")
    for p in sorted(only_mp3s)[:30]:
        print(f"  {p}")
    if len(only_mp3s) > 30:
        print(f"  ... and {len(only_mp3s) - 30} more")

    print("\n--- ONLY IN CSV (missing from ALBUMS) ---")
    print(f"Count: {len(only_csv)}")
    for p in sorted(only_csv)[:30]:
        print(f"  {p}")
    if len(only_csv) > 30:
        print(f"  ... and {len(only_csv) - 30} more")

    print("\n--- SUMMARY ---")
    print(f"  In both:           {len(in_both)}")
    print(f"  Only in ALBUMS:    {len(only_mp3s)} (not catalogued)")
    print(f"  Only in CSV:       {len(only_csv)} (missing/deleted)")
    print(f"  Album folders in metadata: {len(in_metadata)} of {len(mp3_folders)}")

    # Write JSON for programmatic use
    import json

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "summary": {
            "mp3_count": len(mp3s),
            "csv_count": len(csv_paths),
            "in_both": len(in_both),
            "only_in_albums": len(only_mp3s),
            "only_in_csv": len(only_csv),
        },
        "only_in_albums": sorted(only_mp3s),
        "only_in_csv": sorted(only_csv),
    }
    with open(OUTPUT_JSON, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nReport saved to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
