#!/usr/bin/env python3
"""
nocturneMelodies — CSV-Driven Dedup, Merge & Organize (v2)
suno-937.csv = THE SOURCE OF TRUTH — what tracks exist
DISCO/ = target (new refined structure) — organize TO this
Discography0g/ = source (old messy) — pull content FROM this

Match CSV tracks to actual MP3s by album name + title similarity (not UUID).
Organize DISCO to match CSV. Pull missing from Discography0g. Report orphans.
"""

import csv
import os
import json
import re
import shutil
from pathlib import Path
from collections import defaultdict

SUNO_CSV = "/Users/steven/Music/nocturneMelodies/suno-937.csv"
DISCO_DIR = Path("/Users/steven/Music/nocturneMelodies/DISCO")
DISCOG_DIR = Path("/Users/steven/Music/nocturneMelodies/Discography0g")
REPORT_DIR = Path("/Users/steven/Music/nocturneMelodies")


def normalize(s):
    """Normalize string for matching."""
    s = s.lower().strip()
    s = re.sub(r'[##*"\']', '', s)
    s = re.sub(r'[\s_\-]+', ' ', s)
    s = re.sub(r'[^a-z0-9 ]', '', s)
    return s


def load_csv():
    """Load THE SOURCE OF TRUTH."""
    tracks = []
    with open(SUNO_CSV, "r", encoding="utf-8", errors="ignore") as f:
        for row in csv.DictReader(f):
            uid = row.get("ID", "").strip()
            if not uid:
                continue
            title = row.get("Title", "").strip().strip('"').strip("'")
            title = title.replace("## ", "").replace("### ", "").replace("**", "").strip()
            # Album = text before first comma, or full title
            album = title.split(",")[0].strip() if "," in title else title
            if not album:
                album = "Misc"
            tracks.append({
                "id": uid,
                "title": title,
                "album": album,
                "safe_album": re.sub(r'[^a-zA-Z0-9 _-]', '', album)[:80],
                "duration": row.get("Duration", "0:00"),
                "tags": row.get("Tags", "")[:200],
                "norm_title": normalize(title),
                "norm_album": normalize(album),
            })
    print(f"📊 CSV loaded: {len(tracks)} tracks, {len(set(t['album'] for t in tracks))} albums")
    return tracks


def scan_mp3s(base_dir):
    """Scan directory: return {album_dir: [mp3_files]}."""
    result = defaultdict(list)
    base_dir = Path(base_dir)
    if not base_dir.exists():
        return result
    for root, dirs, files in os.walk(base_dir):
        rel = Path(root).relative_to(base_dir)
        album_name = rel.parts[0] if rel.parts else "_root"
        for f in files:
            if f.endswith(".mp3"):
                result[album_name].append({
                    "path": os.path.join(root, f),
                    "filename": f,
                    "norm": normalize(f),
                    "size": os.path.getsize(os.path.join(root, f)),
                })
    total = sum(len(v) for v in result.values())
    print(f"🔍 {base_dir.name}: {total} MP3s in {len(result)} album dirs")
    return result


def match_tracks_to_mp3s(csv_tracks, disco_albums, discog_albums):
    """Match each CSV track to actual MP3 files by album + title similarity."""
    stats = {
        "csv_tracks": len(csv_tracks),
        "matched_in_disco": 0,
        "matched_in_discog": 0,
        "unmatched": 0,
        "matched_details": [],
        "unmatched_details": [],
        "album_map": defaultdict(set),
    }

    # Index all MP3s by normalized album name
    disco_by_album = {}
    for album, files in disco_albums.items():
        disco_by_album[normalize(album)] = files

    discog_by_album = {}
    for album, files in discog_albums.items():
        discog_by_album[normalize(album)] = files

    for track in csv_tracks:
        norm_album = track["norm_album"]
        norm_title = track["norm_title"]

        # Find best album match
        best_album_match = None
        best_album_score = 0
        for candidate in list(disco_by_album.keys()) + list(discog_by_album.keys()):
            # Score: how much of the CSV album name matches the candidate
            parts = norm_album.split()
            if not parts:
                continue
            matches = sum(1 for p in parts if p in candidate)
            score = matches / len(parts)
            if score > best_album_score:
                best_album_score = score
                best_album_match = candidate

        if best_album_score < 0.3:
            stats["unmatched"] += 1
            stats["unmatched_details"].append(f"{track['album']} / {track['title'][:40]}")
            continue

        # Search for matching MP3 in the best album
        found = None
        found_in = None

        # Try DISCO first
        if best_album_match in disco_by_album:
            for mp3 in disco_by_album[best_album_match]:
                # Check if any part of the CSV title matches the filename
                title_parts = norm_title.split()
                if len(title_parts) >= 2:
                    match_count = sum(1 for p in title_parts[:3] if p in mp3["norm"])
                    if match_count >= 1:
                        found = mp3
                        found_in = "DISCO"
                        break

        # Try Discography0g
        if not found and best_album_match in discog_by_album:
            for mp3 in discog_by_album[best_album_match]:
                title_parts = norm_title.split()
                if len(title_parts) >= 2:
                    match_count = sum(1 for p in title_parts[:3] if p in mp3["norm"])
                    if match_count >= 1:
                        found = mp3
                        found_in = "Discography0g"
                        break

        if found:
            if found_in == "DISCO":
                stats["matched_in_disco"] += 1
            else:
                stats["matched_in_discog"] += 1
            stats["matched_details"].append({
                "track": track["title"][:60],
                "album": track["album"][:50],
                "mp3": found["filename"],
                "source": found_in,
                "from_album": best_album_match,
            })
            stats["album_map"][track["safe_album"]].add(found["filename"])
        else:
            stats["unmatched"] += 1
            stats["unmatched_details"].append(f"{track['album'][:40]} / {track['title'][:40]}")

    return stats


def organize_disco(stats, disco_albums, discog_albums, csv_tracks):
    """Organize DISCO to match CSV: create proper album folders, copy MP3s."""
    organized = 0

    # Build lookup: norm_album -> {norm_filename: full_path}
    disco_lookup = {}
    for album, files in disco_albums.items():
        na = normalize(album)
        for f in files:
            disco_lookup[(na, f["norm"])] = f["path"]

    discog_lookup = {}
    for album, files in discog_albums.items():
        na = normalize(album)
        for f in files:
            discog_lookup[(na, f["norm"])] = f["path"]

    for detail in stats["matched_details"]:
        if detail["source"] == "Discography0g":
            # Copy from Discography0g to DISCO/<album>/
            target_album = detail.get("from_album", detail["album"])
            target_dir = DISCO_DIR / re.sub(r'[^a-zA-Z0-9 _-]', '', target_album)[:80]
            target_dir.mkdir(parents=True, exist_ok=True)
            target_path = target_dir / detail["mp3"]
            src = detail.get("path")
            if src and os.path.exists(src):
                if not target_path.exists():
                    shutil.copy2(src, target_path)
                    organized += 1
            elif detail["from_album"] in discog_lookup:
                key = (normalize(detail["from_album"]), normalize(detail["mp3"]))
                src = discog_lookup.get(key)
                if src and os.path.exists(src) and not target_path.exists():
                    shutil.copy2(src, target_path)
                    organized += 1

    # Find orphans in DISCO (MP3s not matched to any CSV track)
    csv_mp3s = set()
    for detail in stats["matched_details"]:
        if detail["source"] == "DISCO":
            csv_mp3s.add(detail["mp3"])

    orphans = []
    for album, files in disco_albums.items():
        for f in files:
            if f["filename"] not in csv_mp3s:
                orphans.append(f["path"])

    return organized, orphans


def main():
    print("=== nocturneMelodies — CSV-Driven Dedup, Merge & Organize ===\n")
    print("📖 suno-937.csv = SOURCE OF TRUTH (WHAT EXISTS)")
    print("📂 DISCO/ = target (new refined)")
    print("📂 Discography0g/ = source (old messy)\n")

    csv_tracks = load_csv()
    disco_albums = scan_mp3s(DISCO_DIR)
    discog_albums = scan_mp3s(DISCOG_DIR)

    stats = match_tracks_to_mp3s(csv_tracks, disco_albums, discog_albums)

    organized, orphans = organize_disco(stats, disco_albums, discog_albums, csv_tracks)

    # Print report
    print(f"\n{'='*60}")
    print("📊 MATCH REPORT")
    print(f"{'='*60}\n")
    print(f"  CSV tracks (source of truth):  {stats['csv_tracks']:>6}")
    print(f"  Matched in DISCO:              {stats['matched_in_disco']:>6}")
    print(f"  Matched in Discography0g:      {stats['matched_in_discog']:>6}")
    print(f"  Unmatched (no MP3 found):      {stats['unmatched']:>6}")
    print(f"  Organized into DISCO:          {organized:>6}")
    print(f"  Orphaned in DISCO:             {len(orphans):>6}")

    matched_pct = (stats['matched_in_disco'] + stats['matched_in_discog']) / stats['csv_tracks'] * 100
    print(f"\n  Match rate: {matched_pct:.1f}%\n")

    if stats['unmatched_details']:
        print(f"⚠️  Top 10 unmatched:")
        for d in stats['unmatched_details'][:10]:
            print(f"  • {d}")

    if orphans:
        print(f"\n🗑️  Top 10 orphaned (in DISCO but not in CSV):")
        for o in orphans[:10]:
            print(f"  • {o}")

    if organized:
        print(f"\n✅ {organized} files organized into DISCO/<album>/")

    # Save detailed report
    report = {
        "summary": {
            "csv_tracks": stats["csv_tracks"],
            "matched_disco": stats["matched_in_disco"],
            "matched_discog": stats["matched_in_discog"],
            "unmatched": stats["unmatched"],
            "organized": organized,
            "orphaned": len(orphans),
            "match_rate_pct": round(matched_pct, 1),
        },
        "unmatched": stats["unmatched_details"][:50],
        "orphans_sample": orphans[:50],
        "matched_sample": stats["matched_details"][:20],
    }
    report_path = REPORT_DIR / "csv_match_report.json"
    report_path.write_text(json.dumps(report, indent=2))
    print(f"\n📋 Full report: {report_path}")


if __name__ == "__main__":
    main()
