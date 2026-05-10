#!/usr/bin/env python3
"""
Download missing audio and cover art from Suno export CSVs.
Skips files that already exist locally.
"""

import csv
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DATA_DIR = Path(__file__).parent / "AI_ENHANCED_ORGANIZATION" / "DATA"
OUT_AUDIO = Path(__file__).parent / "AI_ENHANCED_ORGANIZATION" / "DOWNLOADS" / "audio"
OUT_IMAGES = Path(__file__).parent / "AI_ENHANCED_ORGANIZATION" / "DOWNLOADS" / "images"

# Optional: set a different base dir for music organization
# OUT_AUDIO = Path(__file__).parent / "MUSIC_ORGANIZED" / "SUNO_DOWNLOADS"


def sanitize_filename(s: str) -> str:
    """Remove/replace chars unsafe for filenames; strip Markdown."""
    s = re.sub(r"^#+\s*", "", s)  # leading ###
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)  # **bold**
    s = re.sub(r"^🌀\s*", "", s)  # leading emoji
    s = re.sub(r'["\'\n\r\t]', "", s)
    s = re.sub(r"[<>:|?*\\/]", "-", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s or "Untitled"


def load_tracks_from_csv(csv_path: Path) -> list[dict]:
    """Load tracks from a Suno export CSV."""
    tracks = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("audioUrl") and row.get("id"):
                tracks.append(row)
    return tracks


def collect_unique_tracks() -> dict[str, dict]:
    """Collect unique tracks by id from all Suno export CSVs."""
    seen = {}
    for p in DATA_DIR.glob("suno-export-*.csv"):
        for t in load_tracks_from_csv(p):
            if t["id"] not in seen:
                seen[t["id"]] = t
    return seen


def download_file(url: str, out_path: Path, desc: str = "") -> bool:
    """Download URL to out_path. Return True on success."""
    try:
        req = Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; nocTurneMeLoDieS/1.0)"},
        )
        with urlopen(req, timeout=60) as resp:
            data = resp.read()
        out_path.write_bytes(data)
        return len(data) > 0
    except (URLError, HTTPError, OSError) as e:
        print(f"  Error: {e}", file=sys.stderr)
        return False


def main():
    OUT_AUDIO.mkdir(parents=True, exist_ok=True)
    OUT_IMAGES.mkdir(parents=True, exist_ok=True)

    tracks = collect_unique_tracks()
    print(f"Found {len(tracks)} unique tracks in Suno exports")

    downloaded_audio = 0
    skipped_audio = 0
    failed_audio = 0
    downloaded_images = 0
    skipped_images = 0
    failed_images = 0

    for tid, t in tracks.items():
        title = sanitize_filename(t.get("title", "Untitled"))
        audio_url = t.get("audioUrl", "").strip()
        image_url = t.get("imageUrl", "").strip()

        # Audio: {uuid}_{title}.mp3
        if audio_url:
            safe_title = re.sub(r"[<>:|?*\\/]", "-", title)[:80]
            audio_name = f"{tid}_{safe_title}.mp3"
            audio_path = OUT_AUDIO / audio_name
            if audio_path.exists():
                skipped_audio += 1
            else:
                print(f"Downloading audio: {title[:50]}...")
                if download_file(audio_url, audio_path, "audio"):
                    downloaded_audio += 1
                else:
                    failed_audio += 1
                    if audio_path.exists():
                        audio_path.unlink()

        # Image: {uuid}.jpeg (keep extension from URL or default)
        if image_url:
            ext = ".jpeg"
            if ".jpg" in image_url.lower():
                ext = ".jpg"
            elif ".png" in image_url.lower():
                ext = ".png"
            image_path = OUT_IMAGES / f"{tid}{ext}"
            if image_path.exists():
                skipped_images += 1
            else:
                print(f"Downloading image: {title[:50]}...")
                if download_file(image_url, image_path, "image"):
                    downloaded_images += 1
                else:
                    failed_images += 1
                    if image_path.exists():
                        image_path.unlink()

    print()
    print("Summary:")
    print(f"  Audio:  {downloaded_audio} downloaded, {skipped_audio} skipped, {failed_audio} failed")
    print(f"  Images: {downloaded_images} downloaded, {skipped_images} skipped, {failed_images} failed")
    print(f"  Output: {OUT_AUDIO} / {OUT_IMAGES}")


if __name__ == "__main__":
    main()
