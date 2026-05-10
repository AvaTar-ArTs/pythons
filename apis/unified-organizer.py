#!/usr/bin/env python3
"""
?? UNIFIED FILE ORGANIZER
Consolidated organizer combining functionality from 115+ scattered organize scripts

Features:
- File type-based organization
- CSV-based structured moves
- Music album organization
- Content-based classification
- Dry-run and preview modes
"""

import os
import csv
import re
import shutil
from pathlib import Path
from collections import defaultdict


class UnifiedOrganizer:
    def __init__(self, dry_run=False, verbose=True):
        self.dry_run = dry_run
        self.verbose = verbose
        self.moves = []

    def log(self, message):
        if self.verbose:
            print(f"?? {message}")

    def organize_by_filetype(self, directory, custom_rules=None):
        """
        Organize files by extension and content analysis
        Based on organize_files.py functionality
        """
        directory = Path(directory)

        file_types = {
            # Documents
            ".pdf": "documents/pdf",
            ".doc": "documents/word",
            ".docx": "documents/word",
            ".txt": "documents/text",
            ".md": "documents/markdown",
            ".rtf": "documents/text",
            # Code
            ".py": "code/python",
            ".js": "code/javascript",
            ".ts": "code/typescript",
            ".html": "code/web",
            ".css": "code/web",
            ".json": "code/data",
            ".xml": "code/data",
            ".sql": "code/database",
            ".sh": "code/shell",
            # Data
            ".csv": "data/csv",
            ".xlsx": "data/excel",
            ".xls": "data/excel",
            ".db": "data/databases",
            ".sqlite": "data/databases",
            # Images
            ".jpg": "media/images",
            ".jpeg": "media/images",
            ".png": "media/images",
            ".gif": "media/images",
            ".svg": "media/images",
            ".webp": "media/images",
            # Audio
            ".mp3": "media/audio",
            ".wav": "media/audio",
            ".m4a": "media/audio",
            ".flac": "media/audio",
            # Video
            ".mp4": "media/video",
            ".mov": "media/video",
            ".avi": "media/video",
            ".webm": "media/video",
            # Archives
            ".zip": "archives",
            ".tar": "archives",
            ".gz": "archives",
            ".7z": "archives",
        }

        # Add custom rules if provided
        if custom_rules:
            file_types.update(custom_rules)

        for file_path in directory.iterdir():
            if file_path.is_file():
                file_ext = file_path.suffix.lower()
                tag = file_types.get(file_ext, "misc/other")

                # Apply content-based tagging for Python files
                if file_ext == ".py":
                    tag = self._analyze_python_file(file_path, tag)

                dest_dir = directory / tag
                dest_path = dest_dir / file_path.name

                self._queue_move(file_path, dest_path, f"filetype: {tag}")

        self._execute_moves("File type organization")

    def _analyze_python_file(self, file_path, default_tag):
        """Analyze Python file content for better categorization"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

                if "import pandas" in content or "import numpy" in content:
                    return "code/python/data-analysis"
                elif "import tensorflow" in content or "import torch" in content:
                    return "code/python/ml"
                elif "import requests" in content or "import httpx" in content:
                    return "code/python/web"
                elif "import sqlite3" in content or "import psycopg2" in content:
                    return "code/python/database"
                elif "class " in content and "def " in content:
                    return "code/python/libraries"
                else:
                    return "code/python/scripts"
        except:
            return default_tag

    def organize_by_csv(self, csv_file, destination_base):
        """
        Organize files based on CSV mapping
        Based on organize.py functionality
        """
        destination_base = Path(destination_base)

        with open(csv_file, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                original_path = (
                    row.get("Original Path") or row.get("source") or row.get("filepath")
                )
                if not original_path:
                    continue

                # Support multiple CSV formats
                destination_path = (
                    row.get("Destination Path") or row.get("dest") or row.get("target")
                )
                if destination_path:
                    # Use explicit destination from CSV
                    dest_path = destination_base / destination_path.lstrip(os.sep)
                else:
                    # Recreate structure from original path
                    dest_path = destination_base / Path(original_path).relative_to(
                        Path(original_path).anchor
                    )

                source_path = Path(original_path)
                if source_path.exists():
                    self._queue_move(source_path, dest_path, "CSV mapping")

        self._execute_moves("CSV-based organization")

    def organize_music_by_albums(:
        self, music_dir, strategy="filename", metadata_csv=None
    ):
        """
        Organize music files into albums
        Based on organize_into_albums.py and smart_organize_with_metadata.py
        """
        music_dir = Path(music_dir)

        # Load metadata if available
        metadata = {}
        if metadata_csv and Path(metadata_csv).exists():
            metadata = self._load_music_metadata(metadata_csv)

        # Find audio files
        audio_extensions = {".mp3", ".wav", ".m4a", ".flac", ".aac"}
        audio_files = []
        for ext in audio_extensions:
            audio_files.extend(music_dir.glob(f"**/*{ext}"))

        self.log(f"Found {len(audio_files)} audio files")

        # Classify files
        classifications = defaultdict(list)

        for audio_file in audio_files:
            if strategy == "filename":
                album = self._classify_by_filename(audio_file.stem)
            elif strategy == "metadata" and metadata:
                album = self._classify_with_metadata(audio_file.stem, metadata)
            else:
                album = "Singles"

            classifications[album].append(audio_file)

        # Create organization plan
        for album, files in classifications.items():
            album_dir = music_dir / album

            for audio_file in files:
                # Create clean filename
                clean_name = self._clean_music_filename(audio_file.stem)
                dest_path = album_dir / f"{clean_name}{audio_file.suffix}"

                # Handle duplicates
                counter = 1
                original_dest = dest_path
                while dest_path in [m["dest"] for m in self.moves]:
                    counter += 1
                    dest_path = (
                        album_dir / f"{clean_name}_v{counter}{audio_file.suffix}"
                    )

                self._queue_move(audio_file, dest_path, f"Music album: {album}")

        self._execute_moves(f"Music organization ({strategy} strategy)")

    def _load_music_metadata(self, csv_file):
        """Load music metadata from CSV"""
        metadata = {}
        try:
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    title = row.get("title") or row.get("songName") or ""
                    if title:
                        metadata[title] = row
        except Exception as e:
            self.log(f"Error loading metadata: {e}")
        return metadata

    def _classify_by_filename(self, filename):
        """Classify music by filename patterns"""
        filename_lower = filename.lower()

        album_patterns = {
            "In_This_Alley": [r"in\s*this\s*alley", r"alley"],
            "Love_Is_Rubbish": [r"love.*rubbish", r"rubbish", r"trash"],
            "Junkyard_Symphony": [r"junkyard"],
            "Heartbeats": [r"heartbeat"],
            "Blues_Alley": [r"blues"],
            "Echoes_Moonlight": [r"echoes", r"moonlight"],
            "Singles": [],  # Default
        }

        for album, patterns in album_patterns.items():
            for pattern in patterns:
                if re.search(pattern, filename_lower):
                    return album

        return "Singles"

    def _classify_with_metadata(self, filename, metadata):
        """Classify music using metadata"""
        # Simplified metadata classification
        # Full version in smart_organize_with_metadata.py
        return self._classify_by_filename(filename)  # Fallback to filename

    def _clean_music_filename(self, filename):
        """Clean music filename"""
        # Remove common patterns
        name = filename

        # Remove duration codes (_234, _359)
        name = re.sub(r"_\d{3}(?:$|[^0-9])", "", name)

        # Remove version numbers
        name = re.sub(
            r"[_-]?(Remastered|Remix|Edit|Cover|Live|Extended?)",
            "",
            name,
            flags=re.IGNORECASE,
        )
        name = re.sub(r"[_\\(]\\d+[_\\)]", "", name)
        name = re.sub(r"\\d+$", "", name)

        # Remove tags in brackets/parens
        name = re.sub(r"\\[.*?\\]", "", name)
        name = re.sub(r"\\(.*?\\)", "", name)

        # Clean up
        name = name.replace("_", " ").replace("-", " ")
        name = re.sub(r"\\s+", " ", name).strip()
        name = name.replace(" ", "_")

        return name

    def _queue_move(self, source, dest, reason):
        """Queue a file move operation"""
        self.moves.append({"source": source, "dest": dest, "reason": reason})

    def _execute_moves(self, operation_name):
        """Execute all queued moves"""
        if not self.moves:
            self.log(f"No moves to execute for {operation_name}")
            return

        self.log(f"Executing {len(self.moves)} moves for {operation_name}")

        if self.dry_run:
            self.log("DRY RUN MODE - No files will be moved")
            for move in self.moves:
                print(
                    f"  ? {move['source'].name} -> {move['dest'].relative_to(move['dest'].parent.parent)}"
                )
            return

        # Create directories and move files
        success = 0
        failed = []

        for move in self.moves:
            try:
                # Create destination directory
                move["dest"].parent.mkdir(parents=True, exist_ok=True)

                # Move file
                shutil.move(str(move["source"]), str(move["dest"]))
                success += 1

                if self.verbose and success % 10 == 0:
                    self.log(f"Progress: {success}/{len(self.moves)}")

            except Exception as e:
                failed.append(f"{move['source'].name}: {e}")

        # Report results
        self.log(f"Operation complete: {success} successful, {len(failed)} failed")
        if failed:
            self.log("Failed moves:")
            for fail in failed:
                print(f"  ? {fail}")

        # Clear moves for next operation
        self.moves.clear()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Unified File Organizer")
    parser.add_argument("directory", help="Directory to organize")
    parser.add_argument(
        "--mode",
        choices=["filetype", "csv", "music"],
        default="filetype",
        help="Organization mode",
    )
    parser.add_argument("--csv-file", help="CSV file for CSV mode")
    parser.add_argument("--destination", help="Destination for CSV mode")
    parser.add_argument(
        "--music-strategy",
        choices=["filename", "metadata"],
        default="filename",
        help="Music organization strategy",
    )
    parser.add_argument("--metadata-csv", help="Metadata CSV for music organization")
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview without moving files"
    )
    parser.add_argument("--quiet", action="store_true", help="Reduce output")

    args = parser.parse_args()

    organizer = UnifiedOrganizer(dry_run=args.dry_run, verbose=not args.quiet)

    if args.mode == "filetype":
        organizer.organize_by_filetype(args.directory)
    elif args.mode == "csv":
        if not args.csv_file or not args.destination:
            print("Error: --csv-file and --destination required for CSV mode")
            return
        organizer.organize_by_csv(args.csv_file, args.destination)
    elif args.mode == "music":
        organizer.organize_music_by_albums(
            args.directory, strategy=args.music_strategy, metadata_csv=args.metadata_csv
        )


if __name__ == "__main__":
    main()
