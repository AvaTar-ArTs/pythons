#!/usr/bin/env python3
import csv
import os
import re
import shutil
import subprocess
from pathlib import Path

ROOT_DIR = "/Users/steven/Music/nocTurneMeLoDieS"
CSV_FILES = [
    "/Users/steven/Music/nocTurneMeLoDieS/suno_ultimate_master.csv",
    "/Users/steven/Music/nocTurneMeLoDieS/suno_ultimate_master_combined.csv",
]

# Directories to strictly ignore
EXCLUDE_DIRS = {
    "SCRIPTS",
    "DATA",
    "DOCS",
    "suno_backups",
    "suno_html_backups",
    "songs-metadata",
    "analysis",
    "transcripts",
    "test",
    ".git",
    ".DS_Store",
}


def get_duration_mmss(file_path):
    try:
        cmd = ["afinfo", str(file_path)]
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "duration" in line:
                seconds = float(line.split()[2])
                minutes = int(seconds // 60)
                secs = int(seconds % 60)
                return f"{minutes}{secs:02d}"
    except Exception:
        return "0000"
    return "0000"


def load_metadata(csv_files):
    metadata = {}
    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            continue
        with open(csv_file, encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                uuid = row.get("id") or row.get("idNumber")
                title = row.get("title") or row.get("Song Name")
                if uuid and title:
                    metadata[uuid.strip()] = title.strip()
    return metadata


def clean_title_string(title):
    # Basic cleanup
    title = re.sub(r"[^\x00-\x7F]+", "", title)  # ascii only
    title = re.sub(r"https?://\S+|www\.\S+", "", title)
    title = re.sub(r'[\\/?%*:|"<>]', "_"", title)
    title = title.replace(" ", "_").replace("-", "_")

    # Remove specific clutter
    title = re.sub(r"\(.*\)", "", title)  # remove parens
    title = re.sub(r"_dup\d*", "", title, flags=re.IGNORECASE)
    title = re.sub(r"_mix\d*", "", title, flags=re.IGNORECASE)
    title = re.sub(r"^root_", "", title, flags=re.IGNORECASE)

    # Remove existing duration suffix if it exists (3-4 digits at end)
    title = re.sub(r"\d{3,4}$", "", title)

    title = re.sub(r"_+", "_", title)
    return title.strip("_")


def get_unique_path(directory, filename):
    """Generates a unique filename if the target already exists.
    Appends _v2, _v3, etc.
    """
    base_name = Path(filename).stem
    extension = Path(filename).suffix
    counter = 2

    new_path = directory / filename
    while new_path.exists():
        new_filename = f"{base_name}_v{counter}{extension}"
        new_path = directory / new_filename
        counter += 1

    return new_path


def process_library():
    print("Loading metadata...")
    metadata = load_metadata(CSV_FILES)
    print(f"Loaded {len(metadata)} records.")

    print(f"\nScanning {ROOT_DIR}...")

    # Stats
    processed_count = 0
    renamed_count = 0
    skipped_count = 0
    error_count = 0

    for root, dirs, files in os.walk(ROOT_DIR):
        # Filter excluded directories in-place
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]

        current_dir = Path(root)

        # Filter for mp3s
        mp3_files = [f for f in files if f.lower().endswith(".mp3")]

        for filename in mp3_files:
            file_path = current_dir / filename
            processed_count += 1

            try:
                # Determine base title
                uuid = file_path.stem

                # Strategy 1: UUID match in CSV
                if uuid in metadata:
                    base_title = metadata[uuid]
                # Strategy 2: Clean the existing filename
                else:
                    base_title = filename

                clean_base = clean_title_string(base_title)

                # If title is empty after cleaning (edge case), skip or keep original
                if not clean_base:
                    clean_base = "Untitled"

                # Calculate duration
                mmss = get_duration_mmss(file_path)

                # Construct new name
                new_filename = f"{clean_base}{mmss}.mp3"

                # Check if rename is needed
                if filename != new_filename:
                    target_path = get_unique_path(current_dir, new_filename)

                    # Rename MP3
                    shutil.move(file_path, target_path)
                    print(f"RENAMED: {filename} -> {target_path.name}")
                    renamed_count += 1

                    # Rename associated meta files if they exist
                    # Try standard patterns
                    old_stem = file_path.stem
                    new_stem = target_path.stem

                    for ext in ["_transcript.txt", "_analysis.txt"]:
                        old_meta = current_dir / f"{old_stem}{ext}"
                        if old_meta.exists():
                            new_meta = current_dir / f"{new_stem}{ext}"
                            # Ensure unique meta name too (though usually syncs with mp3)
                            if new_meta.exists():
                                # This shouldn't happen if mp3 logic handled collision,
                                # but safe to overwrite or append? Let's move.
                                pass
                            shutil.move(old_meta, new_meta)
                            print(f"  -> Meta: {old_meta.name} -> {new_meta.name}")
                else:
                    # print(f"SKIPPED: {filename} (Already correct)")
                    skipped_count += 1

            except Exception as e:
                print(f"ERROR processing {filename}: {e}")
                error_count += 1

    print("-" * 50)
    print("SUMMARY")
    print(f"Processed: {processed_count}")
    print(f"Renamed:   {renamed_count}")
    print(f"Skipped:   {skipped_count}")
    print(f"Errors:    {error_count}")


if __name__ == "__main__":
    process_library()
