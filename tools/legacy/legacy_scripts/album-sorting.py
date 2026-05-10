#!/usr/bin/env python3
'\''
🎵 ADVANCED ALBUM SORTING & RENAMING TOOL (Unified Version)
=========================================================
Automates the organization of your music library by:
1. Recursively scanning for MP3s in 'nocTurneMeLoDieS'.
2. Leveraging 'audio-11-28-21:09.csv' for precise metadata.
3. Parsing ID3 tags and associated text files.
4. Standardizing filenames to 'Title_of_SongMMSS.mp3'.
5. Organizing files into an 'Artist/Album/' directory structure.

Features:
- CSV Metadata Integration
- ID3 Tag Parsing (Mutagen)
- Text File Parsing (_analysis.txt, _transcript.txt)
- Robust Renaming (Title_MMSS)
- Dry Run Mode (Safety First)
- Detailed Logging
"""

import sys
import csv
import re
import shutil
import argparse
import logging
from pathlib import Path
from collections import defaultdict

# Try to import mutagen for ID3 tags
try:
    from mutagen.easyid3 import EasyID3
    from mutagen.mp3 import MP3

    HAS_MUTAGEN = True
except ImportError:
    HAS_MUTAGEN = False

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"


METADATA_CSV_PATH = Path("/Users/steven/clean/audio-11-29-08:26.csv")


class AlbumSorter:
    def __init__(self, root_dir, dry_run=True):
        self.root_dir = Path(root_dir).resolve()
        self.dry_run = dry_run
        self.stats = defaultdict(int)
        self.csv_metadata = self.load_csv_metadata()

        if not self.root_dir.exists():
            logger.error(
                f"{Colors.RED}Error: Directory not found: {self.root_dir}{Colors.END}"
            )
            sys.exit(1)

    def load_csv_metadata(self):
        """Load metadata from the provided CSV file"""
        meta_map = {}
        if not METADATA_CSV_PATH.exists():
            logger.warning(
                f"{Colors.YELLOW}Warning: Metadata CSV not found at {METADATA_CSV_PATH}{Colors.END}"
            )
            return meta_map

        try:
            with open(METADATA_CSV_PATH, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Index by Filename AND Original Path for robust matching
                    filename = row.get("Filename", "").strip()
                    path = row.get("Original Path", "").strip()

                    if filename:
                        meta_map[filename] = row
                    if path:
                        meta_map[path] = row
            logger.info(
                f"{Colors.CYAN}Loaded metadata for {len(meta_map)} items from CSV.{Colors.END}"
            )
        except Exception as e:
            logger.error(f"{Colors.RED}Error loading CSV: {e}{Colors.END}")

        return meta_map

    def get_duration_mmss(self, file_path):
        """Get duration in M(M)SS format"""
        # 1. Try CSV
        if file_path.name in self.csv_metadata:
            dur_str = self.csv_metadata[file_path.name].get("Duration", "").strip()
            if dur_str and ":" in dur_str:
                try:
                    parts = dur_str.split(":")
                    minutes = int(parts[0])
                    seconds = int(parts[1])
                    if minutes == 0:
                        return f"{seconds:02d}"
                    else:
                        return f"{minutes}{seconds:02d}"
                except:
                    pass

        # 2. Try Mutagen
        try:
            if HAS_MUTAGEN:
                audio = MP3(file_path)
                total_seconds = int(audio.info.length)
                minutes = total_seconds // 60
                seconds = total_seconds % 60

                if total_seconds == 0:
                    return "00"
                elif minutes == 0:
                    return f"{seconds:02d}"  # e.g. "05" for 0:05
                else:
                    return f"{minutes}{seconds:02d}"  # e.g. "123" for 1:23, "1005" for 10:05
        except Exception:
            pass
        return "0000"  # Fallback to a consistent "0000" if duration cannot be determined or is 0.

    def standardize_filename(self, title, mmss):
        """Convert title to Title_of_SongMMSS.mp3 format"""
        # Remove existing MMSS if present at end of title
        clean_title = re.sub(r"\d{4}$", "", title).strip()

        # Replace non-alphanumeric with underscores
        clean_title = re.sub(r"[^a-zA-Z0-9]", "_", clean_title)

        # Remove multiple underscores
        clean_title = re.sub(r"_+", "_", clean_title)

        # Ensure no leading/trailing underscores
        clean_title = clean_title.strip("_")

        return f"{clean_title}{mmss}.mp3"

    def get_metadata(self, file_path):
        """Extract metadata from CSV, ID3, and text files"""
        meta = {
            "artist": "Unknown Artist",
            "album": "Unknown Album",
            "title": file_path.stem,
        }

        # 1. CSV Metadata (Highest Priority for some fields?)
        # Actually, ID3 tags might be more accurate for Artist/Album if manually set.
        # But CSV gives us "Creation Date" which might be useful.

        # 2. ID3 Tags
        if HAS_MUTAGEN:
            try:
                tags = EasyID3(file_path)
                if "artist" in tags:
                    meta["artist"] = tags["artist"][0]
                if "album" in tags:
                    meta["album"] = tags["album"][0]
                if "title" in tags:
                    meta["title"] = tags["title"][0]
            except Exception:
                pass

        # 3. Text File Parsing (Analysis/Transcript)
        base_name = file_path.stem
        clean_stem = re.sub(r"\d{4}$", "", base_name)

        for suffix in ["_analysis.txt", "_transcript.txt"]:
            for stem in [base_name, clean_stem]:
                txt_path = file_path.parent / f"{stem}{suffix}"
                if txt_path.exists():
                    try:
                        content = txt_path.read_text(encoding="utf-8")
                        artist_match = re.search(
                            r"Artist:\s*(.+)", content, re.IGNORECASE
                        )
                        if artist_match and meta["artist"] == "Unknown Artist":
                            meta["artist"] = artist_match.group(1).strip()

                        title_match = re.search(
                            r"Title:\s*(.+)", content, re.IGNORECASE
                        )
                        if (
                            title_match and meta["title"] == base_name
                        ):  # Only override if generic
                            meta["title"] = title_match.group(1).strip()
                    except Exception:
                        pass

        # Fallback: If still unknown, maybe use parent folder name as Album?
        if meta["album"] == "Unknown Album":
            parent_name = file_path.parent.name
            if parent_name not in ["nocTurneMeLoDieS", "Music", "mp3"]:
                meta["album"] = parent_name

        return meta

    def organize_library(self):
        """Main execution loop'\''
        logger.info(
            f"{Colors.BOLD}Starting Album Sorting & Organization...{Colors.END}"
        )
        logger.info(f"Root: {self.root_dir}")
        logger.info("Mode: {'DRY RUN' if self.dry_run else 'LIVE'}\n")

        files_processed = 0

        # recursive scan
        for file_path in self.root_dir.rglob("*.mp3"):
            # Skip hidden files
            if file_path.name.startswith("."):
                continue

            files_processed += 1

            # Gather Info
            meta = self.get_metadata(file_path)
            duration = self.get_duration_mmss(file_path)

            # Determine New Filename
            new_filename = self.standardize_filename(meta["title"], duration)

            # Determine Target Directory: Root/Artist/Album/
            safe_artist = re.sub(r'[<>:"/\\|?*]', "_", meta["artist""])
            safe_album = re.sub(r'[<>:"/\\|?*]', "_", meta["album""])

            # Avoid creating deep nests if Artist/Album are unknown or generic
            if safe_artist == "Unknown_Artist":
                safe_artist = "Misc"

            target_dir = self.root_dir / safe_artist / safe_album
            target_path = target_dir / new_filename

            # Check if move/rename is needed
            if target_path.resolve() != file_path.resolve():
                self.move_file(file_path, target_path)
                self.move_associated_files(file_path, target_path)
            else:
                pass

        logger.info(
            f"\n{Colors.BOLD}Processed {files_processed} MP3 files.{Colors.END}"
        )
        logger.info(f"Moved/Renamed: {self.stats['moved']}")
        logger.info(f"Errors: {self.stats['errors']}")

    def move_file(self, src, dst):
        """Handle file movement with logging"""
        try:
            if self.dry_run:
                logger.info(
                    f"  {Colors.YELLOW}[DRY RUN] Would move:{Colors.END} {src.name}"
                )
                logger.info(f"       -> {dst.relative_to(self.root_dir)}")
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
                logger.info(
                    f"  {Colors.GREEN}Moved:{Colors.END} {src.name} -> {dst.name}"
                )

            self.stats["moved"] += 1

        except Exception as e:
            logger.error(f"  {Colors.RED}Error moving {src.name}: {e}{Colors.END}")
            self.stats["errors"] += 1

    def move_associated_files(self, audio_src, audio_dst):
        """Find and move sibling text files"""
        base_name = audio_src.stem
        for sibling in audio_src.parent.glob(f"{re.escape(base_name)}*"):
            if sibling == audio_src:
                continue
            if sibling.suffix.lower() == ".mp3":
                continue  # Don't move other mp3s, let the loop handle them

            new_sibling_name = audio_dst.stem + sibling.suffix
            sibling_dst = audio_dst.parent / new_sibling_name

            if sibling.resolve() != sibling_dst.resolve():
                if self.dry_run:
                    logger.info(
                        f"    {Colors.YELLOW}[DRY RUN] Would move sibling:{Colors.END} {sibling.name}"
                    )
                else:
                    try:
                        shutil.move(str(sibling), str(sibling_dst))
                        logger.info(
                            f"    {Colors.GREEN}Moved sibling:{Colors.END} {sibling.name}"
                        )
                    except Exception as e:
                        logger.error(
                            f"    {Colors.RED}Error moving sibling: {e}{Colors.END}"
                        )


def main():
    parser = argparse.ArgumentParser(
        description="Organize Music Library by Artist/Album"
    )
    parser.add_argument(
        "--live", action="store_true", help="Execute changes (default is dry-run)"
    )
    parser.add_argument(
        "--dir",
        type=str,
        default="/Users/steven/Music/nocTurneMeLoDieS",
        help="Root directory to process",
    )

    args = parser.parse_args()

    if not HAS_MUTAGEN:
        logger.warning(
            f"{Colors.YELLOW}Warning: 'mutagen' library not found. ID3 tag parsing will be disabled.{Colors.END}"
        )

    sorter = AlbumSorter(args.dir, dry_run=not args.live)
    sorter.organize_library()


if __name__ == "__main__":
    main()
