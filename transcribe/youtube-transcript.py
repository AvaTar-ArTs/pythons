#!/usr/bin/env python3
"""
youtube-transcript.py  —  fetch YouTube auto-captions and save as clean text
Usage: python3 youtube-transcript.py <youtube_url> [output_dir]
"""

import sys
import re
import subprocess
import tempfile
import os
from pathlib import Path


def download_vtt(url: str, tmp_dir: str) -> tuple[str, str]:
    """Download auto-captions via yt-dlp, return (vtt_path, video_title)."""
    result = subprocess.run(
        [
            "yt-dlp",
            "--write-auto-subs",
            "--sub-lang",
            "en",
            "--sub-format",
            "vtt",
            "--skip-download",
            "--print",
            "title",
            "-o",
            os.path.join(tmp_dir, "%(title)s.%(ext)s"),
            url,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(1)

    title = result.stdout.strip().splitlines()[0]
    vtt_files = list(Path(tmp_dir).glob("*.vtt"))
    if not vtt_files:
        print("No captions found for this video.")
        sys.exit(1)

    return str(vtt_files[0]), title


def clean_vtt(vtt_path: str) -> str:
    """
    Convert raw VTT subtitle file into clean readable text.
    TODO(human): implement this function

    The VTT file contains lines like:
      00:00:00.000 --> 00:00:04.000
      Hello and welcome to <00:00:01.500><c>this</c> video

      00:00:02.000 --> 00:00:06.000
      Hello and welcome to this video today

    Problems to solve:
      1. Lines repeat with overlapping timestamps (sliding window captions)
      2. Inline tags like <00:00:01.500><c>word</c> need stripping
      3. Header lines (WEBVTT, Kind:, Language:) should be excluded
      4. Result should be flowing readable text, not one line per caption

    Return the cleaned text as a single string.
    """
    with open(vtt_path, encoding="utf-8") as f:
        raw = f.read()

    # Your implementation here
    pass


def save_transcript(text: str, title: str, output_dir: str) -> str:
    """Write cleaned text to output_dir/<title>.txt, return the path."""
    safe_title = re.sub(r'[<>:"/\\|?*]', "", title).strip()
    out_path = os.path.join(output_dir, f"{safe_title}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    return out_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 youtube-transcript.py <youtube_url> [output_dir]")
        sys.exit(1)

    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else str(Path.home() / "Music")

    print(f"Fetching captions for: {url}")
    with tempfile.TemporaryDirectory() as tmp:
        vtt_path, title = download_vtt(url, tmp)
        print(f"Title: {title}")
        print("Cleaning transcript...")
        text = clean_vtt(vtt_path)
        if not text:
            print("clean_vtt returned empty — check your implementation.")
            sys.exit(1)
        out = save_transcript(text, title, output_dir)

    print(f"\nSaved to: {out}")
    print(f"Length: {len(text):,} characters")


if __name__ == "__main__":
    main()
