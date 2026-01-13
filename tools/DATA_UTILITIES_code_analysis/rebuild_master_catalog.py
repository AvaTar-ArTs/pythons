#!/usr/bin/env python3
"""from datetime import datetime
from pathlib import Path
import csv
import os
Rebuild ENHANCED_MASTER_CATALOG.csv from scratch by scanning current filesystem.
This ensures all paths match actual files on disk.
"""

BASE_DIR = Path("/Users/steven/Music/nocTurneMeLoDieS")
OUTPUT_CSV = BASE_DIR / "DATA" / "ENHANCED_MASTER_CATALOG.csv"

# Folders to skip
SKIP_FOLDERS = {
    "DATA",
    "DOCS",
    "SCRIPTS",
    "analysis",
    "transcripts",
    "suno_backups",
    "suno_html_backups",
}


def scan_all_audio_files():
    """Scan and catalog all audio files."""
    audio_files = []

    print("?? Scanning for audio files...")

    for root, dirs, files in os.walk(BASE_DIR):
        # Skip unwanted directories
        dirs[:] = [d for d in dirs if d not in SKIP_FOLDERS and not d.startswith(".")]

        root_path = Path(root)

        for file in files:
            if file.lower().endswith((".mp3", ".mp4", ".wav", ".m4a", ".flac", ".m4r")):
                full_path = root_path / file
                relative_path = full_path.relative_to(BASE_DIR)

                # Get folder name (album)
                if len(relative_path.parts) > 1:
                    album_folder = relative_path.parts[0]
                else:
                    album_folder = "Singles"

                # Check for related files
                stem = full_path.stem
                has_transcript = (
                    any((root_path / "transcripts").glob(f"{stem}*.txt"))
                    if (root_path / "transcripts").exists()
                    else False
                )
                has_analysis = (
                    any((root_path / "analysis").glob(f"{stem}*_analysis.txt"))
                    if (root_path / "analysis").exists()
                    else False
                )

                audio_files.append(
                    {
                        "filename": file,
                        "file_path": str(relative_path),
                        "full_path": str(full_path),
                        "album_folder": album_folder,
                        "has_transcript": "Y" if has_transcript else "N",
                        "has_analysis": "Y" if has_analysis else "N",
                    },
                )

    return audio_files


def main():
    print(f"?? Scanning: {BASE_DIR}")

    audio_files = scan_all_audio_files()

    print(f"   Found {len(audio_files)} audio files")

    if audio_files:
        # Backup old catalog
        if OUTPUT_CSV.exists():
            backup = OUTPUT_CSV.with_suffix(
                f'.csv.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            )
            OUTPUT_CSV.rename(backup)
            print(f"?? Backed up old catalog: {backup.name}")

        # Write new catalog
        fieldnames = [
            "filename",
            "file_path",
            "full_path",
            "album_folder",
            "has_transcript",
            "has_analysis",
        ]

        with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(audio_files)

        print(f"? Created new catalog: {OUTPUT_CSV.name}")
        print(f"   {len(audio_files)} files cataloged")
    else:
        print("??  No audio files found!")


if __name__ == "__main__":
    main()
