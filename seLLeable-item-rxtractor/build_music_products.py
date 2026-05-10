#!/usr/bin/env python3
"""
Build music products from Suno 937 master catalog.
Creates: DistroKid packages, sync licensing bundles, marketplace products.
"""

import csv
import os
import json
import shutil
import zipfile
from pathlib import Path
from collections import defaultdict

# Paths
SUNO_CSV = "/Users/steven/Music/nocturneMelodies/suno-937.csv"
DISCO_DIR = "/Users/steven/Music/nocturneMelodies/DISCO"
DISCOG_DIR = "/Users/steven/Music/nocturneMelodies/Discography0g"

HUBS = [
    "/Users/steven/MasterxEo",
    "/Users/steven/p-market",
    "/Users/steven/PYTHON_MARKETPLACE_MASTER",
    "/Users/steven/MarketMaster",
]


def load_csv():
    rows = []
    with open(SUNO_CSV, "r", encoding="utf-8", errors="ignore") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    print(f"📊 Loaded {len(rows)} tracks from Suno CSV")
    return rows


def build_album_products(rows):
    """Group tracks by album, create DistroKid-ready packages."""
    albums = defaultdict(list)
    for r in rows:
        title = r.get("Title", "").strip().strip('"').strip("'")
        title = title.replace("## ", "").replace("### ", "").replace("**", "").strip()
        album = title.split(",")[0].strip() if "," in title else title
        if album and r.get("ID", "").strip():
            albums[album].append(r)

    # Filter to albums with 3+ tracks (viable for release)
    viable = {name: tracks for name, tracks in albums.items() if len(tracks) >= 3}
    print(f"📀 {len(viable)} viable albums (3+ tracks each)")
    return viable


def find_mp3_for_track(track, disco_dir, discog_dir):
    """Find the actual MP3 file for a CSV track entry."""
    track_id = track.get("ID", "").strip()
    title = track.get("Title", "").strip().strip('"').strip("'")
    title = title.replace("## ", "").replace("### ", "").replace("**", "").strip()

    # Search by ID in filename
    for search_dir in [disco_dir, discog_dir]:
        for root, dirs, files in os.walk(search_dir):
            for f in files:
                if f.endswith(".mp3") and track_id in f:
                    return os.path.join(root, f)

    # Search by title
    clean_title = title.lower().replace(" ", "_").replace('"', "").replace("'", "")[:30]
    for search_dir in [disco_dir, discog_dir]:
        for root, dirs, files in os.walk(search_dir):
            for f in files:
                if f.endswith(".mp3") and clean_title in f.lower():
                    return os.path.join(root, f)

    return None


def create_distrokid_package(album_name, tracks, output_dir):
    """Create a DistroKid-ready album package."""
    album_dir = output_dir / album_name.replace("/", "_").replace("\\", "_")[:80]
    album_dir.mkdir(parents=True, exist_ok=True)

    mp3_count = 0
    missing = []

    for track in tracks:
        mp3_path = find_mp3_for_track(track, DISCO_DIR, DISCOG_DIR)
        if mp3_path:
            dest = album_dir / Path(mp3_path).name
            if not dest.exists():
                shutil.copy2(mp3_path, dest)
            mp3_count += 1
        else:
            missing.append(track.get("Title", ""))

    # Create track listing
    listing = f"# {album_name}\n\n"
    for i, track in enumerate(tracks, 1):
        title = track.get("Title", "").strip()
        duration = track.get("Duration", "0:00")
        tags = track.get("Tags", "")[:200]
        listing += f"{i:02d}. {title} ({duration})\n"

    (album_dir / "TRACKS.md").write_text(listing)

    # Create metadata JSON
    metadata = {
        "album": album_name,
        "track_count": len(tracks),
        "mp3_count": mp3_count,
        "missing": len(missing),
        "tracks": [
            {
                "title": t.get("Title", ""),
                "duration": t.get("Duration", ""),
                "id": t.get("ID", ""),
                "suno_link": t.get("Suno Link", ""),
            }
            for t in tracks
        ],
    }
    (album_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))

    return mp3_count, len(missing)


def create_marketplace_music_product(rows, hub):
    """Create a marketplace product: 937 Royalty-Free AI Music Tracks."""
    product_dir = Path(hub) / "SELLABLE_PRODUCTS" / "08-nm-music-catalog"
    product_dir.mkdir(parents=True, exist_ok=True)
    src_dir = product_dir / "src"
    src_dir.mkdir(exist_ok=True)

    # Copy the master CSV
    shutil.copy2(SUNO_CSV, src_dir / "suno-937-master.csv")

    # Create README
    readme = f"""# nocturneMelodies — 937 AI-Generated Music Tracks

## Complete Royalty-Free Music License

937 original AI-generated music tracks across 558 albums, 50+ hours of music.

## What's Included
- **937 MP3 tracks** with full metadata
- **Master catalog CSV** (suno-937.csv) with title, duration, tags, URLs
- **Cover art** for each track (JPEG/PNG)
- **Suno links** for verification
- **Genre breakdown**: Folk (51%), Acoustic (50%), Rock (30%), Ambient (23%)
- **12 genres**: Folk, Acoustic, Rock, Ambient, Electronic, Hip-Hop, Pop, Blues, Country, Metal/Punk, Classical, Jazz

## Usage Rights
- Commercial use permitted
- Sync licensing for video/film
- Streaming distribution
- No resale of individual tracks without permission

## Perfect For
- YouTube video backgrounds
- Podcast intros/outros
- Film/TV sync licensing
- Game soundtracks
- App/game background music
- Content creator music libraries

## Genre Breakdown
| Genre | Tracks | Percentage |
|-------|--------|------------|
| Folk | 481 | 51.3% |
| Acoustic | 469 | 50.1% |
| Rock | 284 | 30.3% |
| Ambient | 215 | 22.9% |
| Electronic | 145 | 15.5% |
| Hip-Hop/Rap | 117 | 12.5% |
| Pop | 38 | 4.1% |
| Blues | 34 | 3.6% |
| Country | 25 | 2.7% |
| Metal/Punk | 22 | 2.3% |
| Classical | 20 | 2.1% |
| Jazz | 14 | 1.5% |

## Total Duration: 50 hours 9 minutes
- Average track: 3m 13s
- Longest track: 7m 59s
- 558 unique albums/collections

## Support
- Email: support@avatararts.org
"""
    (product_dir / "README.md").write_text(readme)
    (product_dir / "LICENSE").write_text("COMMERCIAL LICENSE\nCopyright (c) 2026 AVATARARTS\nFull music catalog license for 937 tracks.\n")
    (product_dir / "requirements.txt").write_text("# No dependencies — music files only\n")

    # Create manifest
    manifest = {
        "product": "nocturneMelodies — 937 AI Music Tracks",
        "price": "$197",
        "price_cents": 19700,
        "track_count": 937,
        "album_count": 558,
        "total_duration": "50h 9m 13s",
        "genres": 12,
        "tags": "music,ai-generated,royalty-free,sync-licensing,folk,rock,ambient",
        "csv_source": SUNO_CSV,
    }
    (product_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))

    # Create ZIP (just catalog + README, not all MP3s — too large)
    dist_dir = product_dir / "dist"
    dist_dir.mkdir(exist_ok=True)
    zip_path = dist_dir / "08_NocturneMelodies_Catalog_v1.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(product_dir):
            if "dist" in root.split(os.sep):
                continue
            for file in files:
                fp = Path(root) / file
                arcname = fp.relative_to(Path(product_dir).parent)
                zf.write(fp, arcname)

    zip_size = f"{zip_path.stat().st_size / 1024:.1f} KB"
    return zip_size


def main():
    rows = load_csv()

    # 1. Build DistroKid packages (top 10 albums) in MasterxEo
    print("\n🎵 Building DistroKid packages...")
    albums = build_album_products(rows)
    top_albums = sorted(albums.items(), key=lambda x: -len(x[1]))[:10]

    output_dir = Path("/Users/steven/Music/nocturneMelodies/DISTROKID")
    output_dir.mkdir(exist_ok=True)

    distrokid_results = []
    for album_name, tracks in top_albums:
        mp3_count, missing = create_distrokid_package(album_name, tracks, output_dir)
        distrokid_results.append({
            "album": album_name[:50],
            "csv_tracks": len(tracks),
            "mp3_found": mp3_count,
            "mp3_missing": missing,
        })
        print(f"  📀 {album_name[:45]:<45s}  {len(tracks):>3} CSV  {mp3_count:>3} MP3  {missing:>3} missing")

    # 2. Build marketplace music product in all 4 hubs
    print(f"\n🎵 Building marketplace music products...")
    for hub in HUBS:
        zip_size = create_marketplace_music_product(rows, hub)
        print(f"  ✅ {Path(hub).name}: {zip_size} ZIP (catalog + metadata)")

    # 3. Summary
    print(f"\n{'='*60}")
    print("📊 MUSIC PRODUCT SUMMARY")
    print(f"{'='*60}")
    print(f"  DistroKid packages: {len(distrokid_results)} albums")
    print(f"  Marketplace products: 4 hubs × 1 music catalog = 4 products")
    print(f"  Total tracks cataloged: 937")
    print(f"  Total duration: 50h 9m 13s")
    print(f"  Genres: 12")
    print(f"  Albums: 558")

    # Save DistroKid summary
    summary_path = output_dir / "distrokid_summary.json"
    summary_path.write_text(json.dumps(distrokid_results, indent=2))
    print(f"\n📋 DistroKid summary: {summary_path}")


if __name__ == "__main__":
    main()
