#!/usr/bin/env python3
"""
nocturneMelodies — CSV-Enforced Cleanup
CSV rows = EXACT number of tracks allowed in DISCO.
Move all extras to DISCO/_EXTRAS/. Keep only CSV-matched MP3s.
"""

import csv
import os
import json
import re
import shutil
from pathlib import Path

SUNO_CSV = "/Users/steven/Music/nocturneMelodies/suno-937.csv"
DISCO_DIR = Path("/Users/steven/Music/nocturneMelodies/DISCO")
EXTRAS_DIR = DISCO_DIR / "_EXTRAS"
REPORT_DIR = Path("/Users/steven/Music/nocturneMelodies")


def normalize(s):
    s = s.lower().strip()
    s = re.sub(r'[##*"\']', '', s)
    s = re.sub(r'[\s_\-]+', ' ', s)
    s = re.sub(r'[^a-z0-9 ]', '', s)
    return s


def load_csv():
    """Load THE authoritative catalog."""
    tracks = {}
    with open(SUNO_CSV, "r", encoding="utf-8", errors="ignore") as f:
        for row in csv.DictReader(f):
            uid = row.get("ID", "").strip()
            if not uid:
                continue
            title = row.get("Title", "").strip().strip('"').strip("'")
            title = title.replace("## ", "").replace("### ", "").replace("**", "").strip()
            album = title.split(",")[0].strip() if "," in title else title
            if not album:
                album = "Misc"
            safe_album = re.sub(r'[^a-zA-Z0-9 _-]', '', album)[:80]
            tracks[uid] = {
                "title": title,
                "album": album,
                "safe_album": safe_album,
                "norm_title": normalize(title),
                "norm_album": normalize(album),
                "duration": row.get("Duration", "0:00"),
            }
    print(f"📖 CSV loaded: {len(tracks)} authoritative tracks")
    return tracks


def scan_all_mp3s(base_dir):
    """Scan all MP3s, return list of {path, filename, parent_album_dir}."""
    files = []
    for root, dirs, fnames in os.walk(base_dir):
        if "_EXTRAS" in root:
            continue
        for f in fnames:
            if f.endswith(".mp3"):
                files.append({
                    "path": os.path.join(root, f),
                    "filename": f,
                    "norm": normalize(f),
                    "parent": os.path.basename(root),
                })
    print(f"🔍 Found {len(files)} MP3s in DISCO")
    return files


def match_mp3_to_csv(mp3, csv_tracks):
    """Try to match an MP3 file to a CSV track."""
    fn_norm = mp3["norm"]
    parent_norm = normalize(mp3["parent"])

    # Strategy 1: Extract potential UUID from filename
    uuid_match = re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', mp3["filename"])
    if uuid_match:
        for uid in uuid_match:
            if uid in csv_tracks:
                return uid

    # Strategy 2: Match by album + title words
    for uid, track in csv_tracks.items():
        # Check if track's title words appear in the filename
        title_words = track["norm_title"].split()
        if len(title_words) >= 2:
            # Check if first 2-3 meaningful words of title are in the filename
            match_count = sum(1 for w in title_words[:4] if len(w) > 3 and w in fn_norm)
            if match_count >= 2:
                # Also check album match
                if track["norm_album"] in parent_norm or parent_norm in track["norm_album"]:
                    return uid

    return None


def enforce_csv(csv_tracks, all_mp3s):
    """Keep only CSV-matched MP3s. Move everything else to _EXTRAS/."""
    stats = {
        "total_mp3s": len(all_mp3s),
        "csv_matched": 0,
        "moved_to_extras": 0,
        "missing_from_csv": 0,
        "matched_details": [],
        "moved_files": [],
    }

    # Match all MP3s
    matched_mp3s = set()
    for mp3 in all_mp3s:
        uid = match_mp3_to_csv(mp3, csv_tracks)
        if uid:
            stats["csv_matched"] += 1
            matched_mp3s.add(mp3["path"])
            stats["matched_details"].append({
                "mp3": mp3["filename"],
                "csv_track": csv_tracks[uid]["title"][:50],
                "album": csv_tracks[uid]["safe_album"],
            })

    # Move unmatched to _EXTRAS
    EXTRAS_DIR.mkdir(parents=True, exist_ok=True)
    for mp3 in all_mp3s:
        if mp3["path"] not in matched_mp3s:
            target = EXTRAS_DIR / mp3["filename"]
            # Handle filename conflicts
            counter = 1
            while target.exists():
                stem = Path(mp3["filename"]).stem
                ext = Path(mp3["filename"]).suffix
                target = EXTRAS_DIR / f"{stem}_{counter}{ext}"
                counter += 1
            shutil.move(mp3["path"], target)
            stats["moved_to_extras"] += 1
            stats["moved_files"].append(mp3["filename"])

    # Check which CSV tracks are missing MP3s
    matched_csv_uids = set()
    for detail in stats["matched_details"]:
        for uid, track in csv_tracks.items():
            if detail["csv_track"].startswith(track["title"][:30]):
                matched_csv_uids.add(uid)

    stats["missing_from_csv"] = len(csv_tracks) - len(matched_csv_uids)

    return stats


def print_report(stats):
    print(f"\n{'='*60}")
    print("📊 CSV-Enforced Cleanup Report")
    print(f"{'='*60}\n")
    print(f"  Total MP3s in DISCO:           {stats['total_mp3s']:>6}")
    print(f"  Matched to CSV (kept):          {stats['csv_matched']:>6}")
    print(f"  Moved to _EXTRAS/:              {stats['moved_to_extras']:>6}")
    print(f"  CSV tracks missing MP3s:        {stats['missing_from_csv']:>6}")
    print(f"\n  DISCO now contains exactly:     {stats['csv_matched']} / {stats['total_mp3s']} original MP3s")
    print(f"  _EXTRAS/ contains:               {stats['moved_to_extras']} files\n")

    if stats['moved_files']:
        print(f"📦 Moved to _EXTRAS/ (first 10):")
        for f in stats['moved_files'][:10]:
            print(f"  → {f}")
        if len(stats['moved_files']) > 10:
            print(f"  ... and {len(stats['moved_files']) - 10} more")


def save_report(stats):
    report = {
        "summary": {
            "total_mp3s": stats["total_mp3s"],
            "csv_matched": stats["csv_matched"],
            "moved_to_extras": stats["moved_to_extras"],
            "missing_from_csv": stats["missing_from_csv"],
        },
        "moved_files": stats["moved_files"][:100],
        "matched_sample": stats["matched_details"][:50],
    }
    path = REPORT_DIR / "csv_enforced_report.json"
    path.write_text(json.dumps(report, indent=2))
    print(f"📋 Full report: {path}")


def main():
    print("=== nocturneMelodies — CSV-Enforced Cleanup ===\n")
    print("📖 suno-937.csv = AUTHORITY (exact row count = exact tracks allowed)")
    print("📂 DISCO/ = keep only CSV-matched MP3s\n")

    csv_tracks = load_csv()
    all_mp3s = scan_all_mp3s(DISCO_DIR)

    stats = enforce_csv(csv_tracks, all_mp3s)
    print_report(stats)
    save_report(stats)


if __name__ == "__main__":
    main()
