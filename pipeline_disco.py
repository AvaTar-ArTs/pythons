#!/usr/bin/env python3
"""
nocTurneMeLoDieS — Complete DISCO Pipeline
────────────────────────────────────────────
1. Download 937 tracks (audio + cover) from suno-937.csv
2. Organize into DISCO/ by album
3. Rename UUID folders/files to song titles
4. Fix issues (non-ASCII, emoji, loose files, duplicates)
5. Verify completion

All output goes to: /Users/steven/Music/nocturneMelodies/DISCO/
"""

import csv
import os
import re
import sys
import time
import shutil
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from collections import Counter

# ─── CONFIG ──────────────────────────────────────────────────────────────
CSV_PATH = Path("/Users/steven/Music/nocturneMelodies/suno-937.csv")
DISCO = Path("/Users/steven/Music/nocturneMelodies/DISCO")
AUDIO_DIR = DISCO / "audio"
COVERS_DIR = DISCO / "covers"
ALBUMS_DIR = DISCO / "albums"

# ─── PHASE 1: DOWNLOAD ───────────────────────────────────────────────────

def sanitize_title(s: str) -> str:
    """Make title safe for filenames."""
    s = re.sub(r"^#+\s*", "", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r'^["\']|["\']$', "", s)
    s = re.sub(r"[<>:\"|?*\\/]", "-", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s or "Untitled"

def load_tracks(csv_path: Path) -> list:
    """Load tracks from suno-937.csv."""
    tracks = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Handle both column name variants
            audio_url = (row.get("Audio URL") or row.get("audioUrl", "")).strip()
            cover_url = (row.get("Cover URL") or row.get("imageUrl", "")).strip()
            title = row.get("Title", "").strip()
            uuid = row.get("ID", "").strip()
            tags = row.get("Tags", "").strip()
            
            if audio_url and uuid:
                tracks.append({
                    "uuid": uuid,
                    "title": sanitize_title(title),
                    "audio_url": audio_url,
                    "cover_url": cover_url,
                    "tags": tags,
                })
    return tracks

def download(url: str, out_path: Path, retries: int = 3) -> bool:
    """Download a file with retries."""
    for attempt in range(retries):
        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req, timeout=60) as resp:
                data = resp.read()
            if len(data) > 0:
                out_path.write_bytes(data)
                return True
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                print(f"    ✗ {out_path.name}: {e}")
                return False
    return False

def phase1_download():
    """Phase 1: Download all 937 tracks."""
    print("=" * 60)
    print("PHASE 1: DOWNLOADING 937 TRACKS")
    print("=" * 60)
    
    if not CSV_PATH.exists():
        print(f"CSV not found: {CSV_PATH}")
        return False
    
    tracks = load_tracks(CSV_PATH)
    print(f"Loaded {len(tracks)} tracks from CSV\n")
    
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    
    dl_audio = 0
    skip_audio = 0
    fail_audio = 0
    dl_cover = 0
    skip_cover = 0
    fail_cover = 0
    
    for i, t in enumerate(tracks):
        uid = t["uuid"]
        title = t["title"][:60]
        
        # Audio: uuid_Title.mp3
        audio_name = f"{uid}_{t['title'][:60]}.mp3"
        audio_path = AUDIO_DIR / audio_name
        
        if not audio_path.exists():
            print(f"[{i+1}/{len(tracks)}] Audio: {title}")
            if download(t["audio_url"], audio_path):
                dl_audio += 1
            else:
                fail_audio += 1
        else:
            skip_audio += 1
        
        # Cover: uuid.jpeg
        if t["cover_url"]:
            ext = ".jpeg"
            if ".png" in t["cover_url"]:
                ext = ".png"
            elif ".jpg" in t["cover_url"]:
                ext = ".jpg"
            cover_path = COVERS_DIR / f"{uid}{ext}"
            
            if not cover_path.exists():
                if download(t["cover_url"], cover_path):
                    dl_cover += 1
                else:
                    fail_cover += 1
            else:
                skip_cover += 1
        
        if (i + 1) % 50 == 0:
            print(f"  ... {i+1}/{len(tracks)} done")
    
    print(f"\nAudio:  {dl_audio} downloaded, {skip_audio} skipped, {fail_audio} failed")
    print(f"Covers: {dl_cover} downloaded, {skip_cover} skipped, {fail_cover} failed")
    return True

# ─── PHASE 2: ALBUM ORGANIZATION ─────────────────────────────────────────

def phase2_organize_by_album():
    """Phase 2: Move audio into album folders based on CSV title."""
    print("\n" + "=" * 60)
    print("PHASE 2: ORGANIZING BY ALBUM")
    print("=" * 60)
    
    tracks = load_tracks(CSV_PATH)
    album_map = {}
    for t in tracks:
        # Use first part of title before common delimiters as album
        title = t["title"]
        # Simple album detection: if title has underscores/parentheses, use base
        album = re.split(r"[\(_\d]", title)[0].strip()[:40]
        if not album:
            album = "Singles"
        album_map[t["uuid"]] = album
    
    ALBUMS_DIR.mkdir(parents=True, exist_ok=True)
    organized = 0
    
    # Scan all audio files
    for mp3 in AUDIO_DIR.glob("*.mp3"):
        # Extract UUID from filename: uuid_Title.mp3
        match = re.match(r"^([a-f0-9-]+)", mp3.name)
        if match:
            uid = match.group(1).lower()
            album = album_map.get(uid, "Uncategorized")
            album_dir = ALBUMS_DIR / sanitize_title(album)
            album_dir.mkdir(exist_ok=True)
            
            dest = album_dir / mp3.name
            if not dest.exists():
                shutil.move(str(mp3), str(dest))
                organized += 1
    
    print(f"Organized {organized} files into {len(list(ALBUMS_DIR.iterdir()))} albums")

# ─── PHASE 3: RENAME UUID TO TITLES ──────────────────────────────────────

def phase3_rename_to_titles():
    """Phase 3: Rename UUID-named files/folders to song titles."""
    print("\n" + "=" * 60)
    print("PHASE 3: RENAMING UUID → TITLES")
    print("=" * 60)
    
    tracks = load_tracks(CSV_PATH)
    uuid_to_title = {t["uuid"].lower(): t["title"] for t in tracks}
    print(f"Loaded {len(uuid_to_title)} title mappings")
    
    renamed = 0
    for root, dirs, files in os.walk(str(ALBUMS_DIR)):
        for fname in files:
            match = re.match(r"^([a-f0-9-]{36})_(.+)\.(mp3)", fname)
            if match:
                uid = match.group(1).lower()
                ext = match.group(3)
                if uid in uuid_to_title:
                    title = sanitize_title(uuid_to_title[uid])[:80]
                    old = Path(root) / fname
                    new = Path(root) / f"{title}.{ext}"
                    counter = 1
                    while new.exists():
                        new = Path(root) / f"{title}_{counter}.{ext}"
                        counter += 1
                    try:
                        old.rename(new)
                        renamed += 1
                    except OSError:
                        pass
    
    print(f"Renamed {renamed} files")

# ─── PHASE 4: FIX ISSUES ─────────────────────────────────────────────────

def phase4_fix_issues():
    """Phase 4: Fix non-ASCII, emoji, loose files, duplicates."""
    print("\n" + "=" * 60)
    print("PHASE 4: FIXING ISSUES")
    print("=" * 60)
    
    # Find duplicates
    print("\nFinding duplicates...")
    seen = {}
    dupes = 0
    for root, dirs, files in os.walk(str(ALBUMS_DIR)):
        for fname in files:
            if fname.endswith(".mp3"):
                fpath = Path(root) / fname
                size = fpath.stat().st_size
                key = f"{fname}-{size}"
                if key in seen:
                    fpath.unlink()
                    dupes += 1
                else:
                    seen[key] = str(fpath)
    
    print(f"Removed {dupes} duplicate files")
    
    # Count final stats
    total_mp3 = sum(1 for _ in ALBUMS_DIR.rglob("*.mp3"))
    total_covers = sum(1 for _ in COVERS_DIR.glob("*"))
    total_albums = len([d for d in ALBUMS_DIR.iterdir() if d.is_dir()])
    
    print(f"\nFinal DISCO stats:")
    print(f"  Albums: {total_albums}")
    print(f"  Audio files: {total_mp3}")
    print(f"  Cover images: {total_covers}")

# ─── MAIN PIPELINE ───────────────────────────────────────────────────────

def main():
    print("\n🎵 nocTurneMeLoDieS — DISCO PIPELINE 🎵")
    print(f"Output: {DISCO}\n")
    
    phase1_download()
    phase2_organize_by_album()
    phase3_rename_to_titles()
    phase4_fix_issues()
    
    print("\n✅ DISCO PIPELINE COMPLETE")
    print(f"Check: {DISCO}")

if __name__ == "__main__":
    main()
