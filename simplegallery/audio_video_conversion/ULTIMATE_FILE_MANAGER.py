#!/usr/bin/env python3
"""Ultimate File Manager - Comprehensive File Processing, Organization, and Deduplication Tool

This script combines the best features from:
- Advanced File Processor (file conversion, processing, metadata extraction)
- Advanced Organizer (file organization, music library management, duplicate detection)
- Robust Sort and Dedupe (intelligent sorting, content analysis, quality scoring)

Provides a unified interface for all file management operations.
"""

import os
import sys
import logging
import argparse
import subprocess
import shutil
import hashlib
import json
import re
import time
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Union
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("ultimate_file_manager.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class UltimateFileManager:
    """Comprehensive file management tool combining processing, organization, and deduplication."""

    def __init__(self):
        self.client = client

        # File type categories for organization
        self.file_type_categories = {
            "audio": [".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"],
            "video": [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv"],
            "image": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"],
            "document": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
            "archive": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c"],
            "data": [".csv", ".json", ".xml", ".yaml", ".yml"],
        }

        # Music organization patterns
        self.music_organize_patterns = {
            "artist_album": r"^(.+?)\s*-\s*(.+?)\s*-\s*(.+?)$",
            "artist_title": r"^(.+?)\s*-\s*(.+?)$",
            "album_track": r"^(\d+)\s*-\s*(.+?)$",
            "date_title": r"^(\d{4}-\d{2}-\d{2})\s*-\s*(.+?)$",
        }

        # Content similarity patterns for deduplication
        self.similarity_patterns = {
            "analyze_variants": [
                r"analyze.*\.py$",
                r"analyzer.*\.py$",
                r".*analysis.*\.py$",
            ],
            "transcribe_variants": [
                r"trans.*\.py$",
                r"transcript.*\.py$",
                r".*transcribe.*\.py$",
            ],
            "generate_variants": [
                r"generate.*\.py$",
                r"gen.*\.py$",
                r".*create.*\.py$",
            ],
            "process_variants": [
                r"process.*\.py$",
                r"mp3.*\.py$",
                r"mp4.*\.py$",
                r"convert.*\.py$",
            ],
            "suno_variants": [r"suno.*\.py$", r".*scrape.*\.py$", r".*extract.*\.py$"],
        }

        # File categories for organization
        self.categories = {
            "core_analysis": "Core Analysis Scripts",
            "transcription": "Transcription & Speech Processing",
            "generation": "Content Generation",
            "processing": "File Processing & Conversion",
            "web_scraping": "Web Scraping & Data Extraction",
            "organization": "File Organization & Management",
            "utilities": "Utility Scripts",
            "experimental": "Experimental & Test Scripts",
            "archived": "Archived Scripts",
        }

        # File hash cache for duplicate detection
        self.file_hashes = {}
        self.duplicate_groups = defaultdict(list)
        self.processed_files = set()

    # ============================================================================
    # FILE PROCESSING METHODS (from Advanced File Processor)
    # ============================================================================

    def convert_mp4_to_mp3(self, mp4_path: Path, quality: str = "0") -> Path | None:
        """Convert MP4 to MP3 using ffmpeg."""
        mp3_path = mp4_path.with_suffix(".mp3")
        if mp3_path.exists():
            logger.info(f"MP3 already exists: {mp3_path}")
            return mp3_path

        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    str(mp4_path),
                    "-q:a",
                    quality,
                    "-map",
                    "a",
                    str(mp3_path),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            logger.info(f"Converted {mp4_path.name} to MP3")
            return mp3_path
        except Exception as e:
            logger.error(f"Error converting {mp4_path}: {e}")
            return None

    def convert_mp3_to_mp4(
        self, mp3_path: Path, image_path: Path | None = None,
    ) -> Path | None:
        """Convert MP3 to MP4 with optional cover image."""
        mp4_path = mp3_path.with_suffix(".mp4")
        if mp4_path.exists():
            logger.info(f"MP4 already exists: {mp4_path}")
            return mp4_path

        try:
            if image_path and image_path.exists():
                # Convert with cover image
                subprocess.run(
                    [
                        "ffmpeg",
                        "-loop",
                        "1",
                        "-i",
                        str(image_path),
                        "-i",
                        str(mp3_path),
                        "-c:v",
                        "libx264",
                        "-tune",
                        "stillimage",
                        "-c:a",
                        "aac",
                        "-b:a",
                        "192k",
                        "-pix_fmt",
                        "yuv420p",
                        "-shortest",
                        str(mp4_path),
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            else:
                # Convert without image (black screen)
                subprocess.run(
                    [
                        "ffmpeg",
                        "-f",
                        "lavfi",
                        "-i",
                        "color=c=black:s=1280x720:r=1",
                        "-i",
                        str(mp3_path),
                        "-c:v",
                        "libx264",
                        "-c:a",
                        "aac",
                        "-b:a",
                        "192k",
                        "-shortest",
                        str(mp4_path),
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

            logger.info(f"Converted {mp3_path.name} to MP4")
            return mp4_path
        except Exception as e:
            logger.error(f"Error converting {mp3_path}: {e}")
            return None

    def split_audio(self, file_path: Path, segment_length: int = 300) -> list[Path]:
        """Split audio into smaller segments."""
        output_dir = file_path.parent / "segments"
        output_dir.mkdir(exist_ok=True)

        file_name_no_ext = file_path.stem
        command = [
            "ffmpeg",
            "-i",
            str(file_path),
            "-f",
            "segment",
            "-segment_time",
            str(segment_length),
            "-c",
            "copy",
            str(output_dir / f"{file_name_no_ext}_%03d.mp3"),
        ]

        try:
            subprocess.run(command, check=True)
            segments = sorted(list(output_dir.glob("*.mp3")))
            logger.info(f"Split {file_path.name} into {len(segments)} segments")
            return segments
        except Exception as e:
            logger.error(f"Error splitting {file_path}: {e}")
            return []

    def upscale_image(self, image_path: Path, scale_factor: int = 2) -> Path | None:
        """Upscale image using ffmpeg."""
        output_path = (
            image_path.parent / f"{image_path.stem}_upscaled{image_path.suffix}"
        )

        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    str(image_path),
                    "-vf",
                    f"scale=iw*{scale_factor}:ih*{scale_factor}",
                    str(output_path),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            logger.info(f"Upscaled {image_path.name} by {scale_factor}x")
            return output_path
        except Exception as e:
            logger.error(f"Error upscaling {image_path}: {e}")
            return None

    def extract_metadata(self, file_path: Path) -> dict:
        """Extract metadata from media file using ffprobe."""
        try:
            result = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "quiet",
                    "-print_format",
                    "json",
                    "-show_format",
                    "-show_streams",
                    str(file_path),
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            metadata = json.loads(result.stdout)

            # Extract useful information
            format_info = metadata.get("format", {})
            streams = metadata.get("streams", [])

            return {
                "filename": file_path.name,
                "duration": format_info.get("duration", "0"),
                "size": format_info.get("size", "0"),
                "bitrate": format_info.get("bit_rate", "0"),
                "format_name": format_info.get("format_name", "unknown"),
                "streams": len(streams),
            }
        except Exception as e:
            logger.error(f"Error extracting metadata from {file_path}: {e}")
            return {}

    def batch_convert(
        self,
        input_dir: Path,
        output_dir: Path | None = None,
        conversion_type: str = "mp4_to_mp3",
    ) -> dict[Path, Path | None]:
        """Batch convert files in a directory."""
        if not output_dir:
            output_dir = input_dir / "converted"
        output_dir.mkdir(exist_ok=True)

        results = {}
        files_to_process = []

        # Find files to process
        if conversion_type == "mp4_to_mp3":
            files_to_process = list(input_dir.rglob("*.mp4"))
        elif conversion_type == "mp3_to_mp4":
            files_to_process = list(input_dir.rglob("*.mp3"))

        for file_path in files_to_process:
            try:
                if conversion_type == "mp4_to_mp3":
                    result = self.convert_mp4_to_mp3(file_path)
                elif conversion_type == "mp3_to_mp4":
                    result = self.convert_mp3_to_mp4(file_path)
                else:
                    result = None

                results[file_path] = result

            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                results[file_path] = None

        logger.info(f"Processed {len(files_to_process)} files")
        return results

    # ============================================================================
    # FILE ORGANIZATION METHODS (from Advanced Organizer)
    # ============================================================================

    def organize_by_file_type(
        self, source_dir: Path, target_dir: Path | None = None,
    ) -> dict[str, int]:
        """Organize files by their type/extension."""
        if not target_dir:
            target_dir = source_dir / "organized_by_type"

        target_dir.mkdir(exist_ok=True)

        # Create category directories
        for category in self.file_type_categories.keys():
            (target_dir / category).mkdir(exist_ok=True)

        # Create "other" directory for unrecognized types
        (target_dir / "other").mkdir(exist_ok=True)

        file_counts = defaultdict(int)

        for file_path in source_dir.rglob("*"):
            if file_path.is_file():
                extension = file_path.suffix.lower()
                category = self._get_file_category(extension)

                target_category_dir = target_dir / category
                target_file_path = target_category_dir / file_path.name

                # Handle duplicate names
                counter = 1
                original_target = target_file_path
                while target_file_path.exists():
                    stem = original_target.stem
                    suffix = original_target.suffix
                    target_file_path = target_category_dir / f"{stem}_{counter}{suffix}"
                    counter += 1

                try:
                    shutil.move(str(file_path), str(target_file_path))
                    file_counts[category] += 1
                    logger.info(f"Moved {file_path.name} to {category}/")
                except Exception as e:
                    logger.error(f"Error moving {file_path}: {e}")

        logger.info(f"Organized {sum(file_counts.values())} files by type")
        return dict(file_counts)

    def organize_music_library(
        self,
        music_dir: Path,
        organize_by: str = "artist",
        target_dir: Path | None = None,
    ) -> dict[str, int]:
        """Organize music library by artist, album, or genre."""
        if not target_dir:
            target_dir = music_dir / "organized_music"

        target_dir.mkdir(exist_ok=True)

        file_counts = defaultdict(int)

        for file_path in music_dir.rglob("*.mp3"):
            try:
                if organize_by == "artist":
                    artist = self._extract_artist_from_filename(file_path.name)
                    artist_dir = target_dir / self._sanitize_filename(artist)
                    artist_dir.mkdir(exist_ok=True)

                    target_file_path = artist_dir / file_path.name
                    self._handle_duplicate_file(file_path, target_file_path)
                    file_counts[artist] += 1

                elif organize_by == "album":
                    artist, album = self._extract_artist_album_from_filename(
                        file_path.name,
                    )
                    album_dir = (
                        target_dir
                        / self._sanitize_filename(artist)
                        / self._sanitize_filename(album)
                    )
                    album_dir.mkdir(parents=True, exist_ok=True)

                    target_file_path = album_dir / file_path.name
                    self._handle_duplicate_file(file_path, target_file_path)
                    file_counts[f"{artist}/{album}"] += 1

                elif organize_by == "genre":
                    # This would require metadata extraction
                    logger.warning(
                        "Genre organization requires metadata extraction - not implemented",
                    )
                    continue

            except Exception as e:
                logger.error(f"Error organizing {file_path}: {e}")

        logger.info(
            f"Organized {sum(file_counts.values())} music files by {organize_by}",
        )
        return dict(file_counts)

    def organize_by_date(
        self,
        source_dir: Path,
        target_dir: Path | None = None,
        date_format: str = "year_month",
    ) -> dict[str, int]:
        """Organize files by their creation or modification date."""
        if not target_dir:
            target_dir = source_dir / "organized_by_date"

        target_dir.mkdir(exist_ok=True)

        file_counts = defaultdict(int)

        for file_path in source_dir.rglob("*"):
            if file_path.is_file():
                try:
                    stat = file_path.stat()
                    mtime = stat.st_mtime

                    if date_format == "year_month":
                        date_str = time.strftime("%Y-%m", time.localtime(mtime))
                    elif date_format == "year":
                        date_str = time.strftime("%Y", time.localtime(mtime))
                    elif date_format == "year_month_day":
                        date_str = time.strftime("%Y-%m-%d", time.localtime(mtime))
                    else:
                        date_str = "unknown"

                    date_dir = target_dir / date_str
                    date_dir.mkdir(exist_ok=True)

                    target_file_path = date_dir / file_path.name
                    self._handle_duplicate_file(file_path, target_file_path)
                    file_counts[date_str] += 1

                except Exception as e:
                    logger.error(f"Error organizing {file_path} by date: {e}")

        logger.info(f"Organized {sum(file_counts.values())} files by date")
        return dict(file_counts)

    def organize_by_size(
        self, source_dir: Path, target_dir: Path | None = None,
    ) -> dict[str, int]:
        """Organize files by their size ranges."""
        if not target_dir:
            target_dir = source_dir / "organized_by_size"

        target_dir.mkdir(exist_ok=True)

        size_categories = {
            "tiny": (0, 1024),  # < 1KB
            "small": (1024, 1024 * 1024),  # 1KB - 1MB
            "medium": (1024 * 1024, 10 * 1024 * 1024),  # 1MB - 10MB
            "large": (10 * 1024 * 1024, 100 * 1024 * 1024),  # 10MB - 100MB
            "huge": (100 * 1024 * 1024, float("inf")),  # > 100MB
        }

        # Create size category directories
        for category in size_categories:
            (target_dir / category).mkdir(exist_ok=True)

        file_counts = defaultdict(int)

        for file_path in source_dir.rglob("*"):
            if file_path.is_file():
                try:
                    size = file_path.stat().st_size
                    category = self._get_size_category(size, size_categories)

                    category_dir = target_dir / category
                    target_file_path = category_dir / file_path.name
                    self._handle_duplicate_file(file_path, target_file_path)
                    file_counts[category] += 1

                except Exception as e:
                    logger.error(f"Error organizing {file_path} by size: {e}")

        logger.info(f"Organized {sum(file_counts.values())} files by size")
        return dict(file_counts)

    # ============================================================================
    # DEDUPLICATION METHODS (from Robust Sort and Dedupe)
    # ============================================================================

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content."""
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            return hashlib.md5(content).hexdigest()
        except Exception as e:
            logger.warning(f"Could not calculate hash for {file_path}: {e}")
            return ""

    def find_exact_duplicates(self, source_dir: Path) -> dict[str, list[Path]]:
        """Find files with identical content."""
        logger.info("Scanning for exact duplicates...")

        file_hashes = defaultdict(list)

        for file_path in source_dir.rglob("*"):
            if file_path.is_file():
                file_hash = self.calculate_file_hash(file_path)
                if file_hash:
                    file_hashes[file_hash].append(file_path)

        # Return only groups with duplicates
        duplicates = {h: files for h, files in file_hashes.items() if len(files) > 1}
        logger.info(f"Found {len(duplicates)} groups of exact duplicates")
        return duplicates

    def find_similar_files(self, source_dir: Path) -> dict[str, list[Path]]:
        """Find files with similar names and purposes."""
        logger.info("Scanning for similar files...")

        similar_groups = defaultdict(list)

        for file_path in source_dir.rglob("*.py"):
            if file_path.is_file():
                filename = file_path.name.lower()

                for pattern_name, patterns in self.similarity_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, filename):
                            similar_groups[pattern_name].append(file_path)
                            break

        # Filter out single-file groups
        similar_groups = {k: v for k, v in similar_groups.items() if len(v) > 1}
        logger.info(f"Found {len(similar_groups)} groups of similar files")
        return similar_groups

    def analyze_file_content(self, file_path: Path) -> dict:
        """Analyze file content to determine category and quality."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Basic content analysis
            lines = content.split("\n")
            non_empty_lines = [line for line in lines if line.strip()]

            # Quality indicators
            has_docstring = '"""' in content or "'''" in content
            has_logging = "logging" in content.lower()
            has_error_handling = "try:" in content and "except" in content
            has_main_function = 'if __name__ == "__main__":' in content
            has_imports = len(
                [
                    line
                    for line in lines
                    if line.strip().startswith("import")
                    or line.strip().startswith("from")
                ],
            )

            # Determine category based on content
            category = self._determine_category(content, file_path.name)

            # Calculate quality score
            quality_score = 0
            if has_docstring:
                quality_score += 2
            if has_logging:
                quality_score += 1
            if has_error_handling:
                quality_score += 2
            if has_main_function:
                quality_score += 1
            if has_imports > 5:
                quality_score += 1

            return {
                "file_path": file_path,
                "category": category,
                "quality_score": quality_score,
                "lines": len(lines),
                "non_empty_lines": len(non_empty_lines),
                "has_docstring": has_docstring,
                "has_logging": has_logging,
                "has_error_handling": has_error_handling,
                "has_main_function": has_main_function,
                "imports_count": has_imports,
                "size": file_path.stat().st_size,
                "modified": file_path.stat().st_mtime,
            }

        except Exception as e:
            logger.warning(f"Could not analyze {file_path}: {e}")
            return {
                "file_path": file_path,
                "category": "utilities",
                "quality_score": 0,
                "lines": 0,
                "non_empty_lines": 0,
                "has_docstring": False,
                "has_logging": False,
                "has_error_handling": False,
                "has_main_function": False,
                "imports_count": 0,
                "size": 0,
                "modified": 0,
            }

    def clean_duplicates(
        self,
        duplicates: dict[str, list[Path]],
        keep_strategy: str = "largest",
        archive_dir: Path | None = None,
    ) -> int:
        """Clean duplicate files using specified strategy."""
        if not archive_dir:
            archive_dir = Path("DUPLICATES_ARCHIVE")
        archive_dir.mkdir(exist_ok=True)

        removed_count = 0

        for file_hash, files in duplicates.items():
            if len(files) > 1:
                if keep_strategy == "largest":
                    files.sort(key=lambda x: x.stat().st_size, reverse=True)
                elif keep_strategy == "newest":
                    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                elif keep_strategy == "shortest_path":
                    files.sort(key=lambda x: len(x.parts))
                elif keep_strategy == "highest_quality":
                    file_analyses = [self.analyze_file_content(f) for f in files]
                    file_analyses.sort(key=lambda x: x["quality_score"], reverse=True)
                    files = [f["file_path"] for f in file_analyses]

                keep_file = files[0]
                duplicates_to_remove = files[1:]

                logger.info(f"Keeping: {keep_file}")
                logger.info(f"Archiving {len(duplicates_to_remove)} duplicates")

                for duplicate in duplicates_to_remove:
                    try:
                        archive_path = archive_dir / duplicate.name
                        # Handle duplicate names in archive
                        counter = 1
                        original_archive = archive_path
                        while archive_path.exists():
                            stem = original_archive.stem
                            suffix = original_archive.suffix
                            archive_path = (
                                original_archive.parent / f"{stem}_{counter}{suffix}"
                            )
                            counter += 1

                        shutil.move(str(duplicate), str(archive_path))
                        removed_count += 1
                        logger.info(f"Archived: {duplicate}")
                    except Exception as e:
                        logger.error(f"Error archiving {duplicate}: {e}")

        logger.info(f"Archived {removed_count} duplicate files")
        return removed_count

    # ============================================================================
    # COMPREHENSIVE WORKFLOW METHODS
    # ============================================================================

    def comprehensive_cleanup(
        self, source_dir: Path, target_dir: Path | None = None,
    ) -> dict:
        """Perform comprehensive cleanup: deduplicate, organize, and process files."""
        if not target_dir:
            target_dir = source_dir / "CLEANED_ORGANIZED"

        target_dir.mkdir(exist_ok=True)

        logger.info("Starting comprehensive cleanup...")

        # Step 1: Find and clean duplicates
        duplicates = self.find_exact_duplicates(source_dir)
        similar_files = self.find_similar_files(source_dir)

        # Clean duplicates
        archived_duplicates = self.clean_duplicates(
            duplicates, "highest_quality", target_dir / "DUPLICATES_ARCHIVE",
        )

        # Step 2: Organize by file type
        type_organization = self.organize_by_file_type(
            source_dir, target_dir / "by_type",
        )

        # Step 3: Organize music files specifically
        music_files = list(source_dir.rglob("*.mp3"))
        if music_files:
            music_organization = self.organize_music_library(
                source_dir, "artist", target_dir / "music_by_artist",
            )
        else:
            music_organization = {}

        # Step 4: Generate comprehensive report
        report = {
            "timestamp": datetime.now().isoformat(),
            "source_directory": str(source_dir),
            "target_directory": str(target_dir),
            "duplicates_found": len(duplicates),
            "duplicates_archived": archived_duplicates,
            "similar_groups": len(similar_files),
            "type_organization": type_organization,
            "music_organization": music_organization,
            "total_files_processed": sum(type_organization.values())
            + sum(music_organization.values()),
        }

        # Save report
        report_path = target_dir / "CLEANUP_REPORT.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        logger.info("Comprehensive cleanup completed!")
        return report

    # ============================================================================
    # UTILITY METHODS
    # ============================================================================

    def _get_file_category(self, extension: str) -> str:
        """Get category for file extension."""
        for category, extensions in self.file_type_categories.items():
            if extension in extensions:
                return category
        return "other"

    def _get_size_category(self, size: int, size_categories: dict) -> str:
        """Get size category for file size."""
        for category, (min_size, max_size) in size_categories.items():
            if min_size <= size < max_size:
                return category
        return "huge"

    def _extract_artist_from_filename(self, filename: str) -> str:
        """Extract artist name from filename."""
        # Try different patterns
        for pattern_name, pattern in self.music_organize_patterns.items():
            match = re.match(pattern, filename)
            if match:
                return match.group(1).strip()

        # Fallback: use first part before any separator
        separators = [" - ", " _ ", " -", "_"]
        for sep in separators:
            if sep in filename:
                return filename.split(sep)[0].strip()

        return "Unknown Artist"

    def _extract_artist_album_from_filename(self, filename: str) -> tuple[str, str]:
        """Extract artist and album from filename."""
        # Try artist - album - title pattern
        match = re.match(self.music_organize_patterns["artist_album"], filename)
        if match:
            return match.group(1).strip(), match.group(2).strip()

        # Fallback
        return self._extract_artist_from_filename(filename), "Unknown Album"

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for filesystem use."""
        # Remove invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, "_")

        # Remove extra spaces and dots
        filename = re.sub(r"\s+", " ", filename).strip()
        filename = filename.strip(".")

        return filename

    def _handle_duplicate_file(self, source: Path, target: Path):
        """Handle duplicate file names when moving."""
        counter = 1
        original_target = target
        while target.exists():
            stem = original_target.stem
            suffix = original_target.suffix
            target = original_target.parent / f"{stem}_{counter}{suffix}"
            counter += 1

        shutil.move(str(source), str(target))

    def _determine_category(self, content: str, filename: str) -> str:
        """Determine file category based on content and filename."""
        content_lower = content.lower()
        filename_lower = filename.lower()

        # Analysis scripts
        if any(
            keyword in content_lower for keyword in ["analyze", "analysis", "analyzer"]
        ):
            return "core_analysis"

        # Transcription scripts
        if any(
            keyword in content_lower
            for keyword in ["transcribe", "transcript", "whisper", "speech"]
        ):
            return "transcription"

        # Generation scripts
        if any(
            keyword in content_lower
            for keyword in ["generate", "create", "build", "html", "csv"]
        ):
            return "generation"

        # Processing scripts
        if any(
            keyword in content_lower
            for keyword in ["process", "convert", "mp3", "mp4", "ffmpeg"]
        ):
            return "processing"

        # Web scraping scripts
        if any(
            keyword in content_lower
            for keyword in ["scrape", "suno", "beautifulsoup", "requests"]
        ):
            return "web_scraping"

        # Organization scripts
        if any(
            keyword in content_lower
            for keyword in ["organize", "sort", "manage", "file"]
        ):
            return "organization"

        # Experimental/test scripts
        if any(
            keyword in filename_lower
            for keyword in ["test", "experimental", "untitled", "copy"]
        ):
            return "experimental"

        return "utilities"


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Ultimate File Manager")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument(
        "--mode",
        choices=[
            "convert",
            "split",
            "upscale",
            "metadata",
            "organize",
            "dedupe",
            "cleanup",
        ],
        required=True,
        help="Operation mode",
    )
    parser.add_argument("-o", "--output", help="Output file or directory")
    parser.add_argument(
        "--conversion",
        choices=["mp4_to_mp3", "mp3_to_mp4"],
        help="Conversion type for convert mode",
    )
    parser.add_argument(
        "--organize-by",
        choices=["type", "music", "date", "size"],
        help="Organization criteria",
    )
    parser.add_argument(
        "--music-by",
        choices=["artist", "album", "genre"],
        default="artist",
        help="Music organization criteria",
    )
    parser.add_argument(
        "--keep-strategy",
        choices=["largest", "newest", "shortest_path", "highest_quality"],
        default="highest_quality",
        help="Strategy for keeping duplicates",
    )
    parser.add_argument(
        "--segment-length",
        type=int,
        default=300,
        help="Segment length in seconds for split mode",
    )
    parser.add_argument(
        "--scale-factor", type=int, default=2, help="Scale factor for upscale mode",
    )

    args = parser.parse_args()

    manager = UltimateFileManager()
    input_path = Path(args.input)

    if args.mode == "convert" and args.conversion:
        if input_path.is_file():
            if args.conversion == "mp4_to_mp3":
                result = manager.convert_mp4_to_mp3(input_path)
            elif args.conversion == "mp3_to_mp4":
                result = manager.convert_mp3_to_mp4(input_path)

            if result:
                print(f"Converted: {result}")
        elif input_path.is_dir():
            output_dir = Path(args.output) if args.output else input_path / "converted"
            results = manager.batch_convert(input_path, output_dir, args.conversion)
            print(f"Converted {len([r for r in results.values() if r])} files")

    elif args.mode == "split" and input_path.is_file():
        segments = manager.split_audio(input_path, args.segment_length)
        print(f"Split into {len(segments)} segments")
        for segment in segments:
            print(f"  {segment}")

    elif args.mode == "upscale" and input_path.is_file():
        result = manager.upscale_image(input_path, args.scale_factor)
        if result:
            print(f"Upscaled: {result}")

    elif args.mode == "metadata" and input_path.is_file():
        metadata = manager.extract_metadata(input_path)
        print("Metadata:")
        for key, value in metadata.items():
            print(f"  {key}: {value}")

    elif args.mode == "organize" and input_path.is_dir() and args.organize_by:
        output_dir = Path(args.output) if args.output else None

        if args.organize_by == "type":
            results = manager.organize_by_file_type(input_path, output_dir)
            print("Files organized by type:")
            for category, count in results.items():
                print(f"  {category}: {count} files")

        elif args.organize_by == "music":
            results = manager.organize_music_library(
                input_path, args.music_by, output_dir,
            )
            print(f"Music files organized by {args.music_by}:")
            for category, count in results.items():
                print(f"  {category}: {count} files")

        elif args.organize_by == "date":
            results = manager.organize_by_date(input_path, output_dir)
            print("Files organized by date:")
            for category, count in results.items():
                print(f"  {category}: {count} files")

        elif args.organize_by == "size":
            results = manager.organize_by_size(input_path, output_dir)
            print("Files organized by size:")
            for category, count in results.items():
                print(f"  {category}: {count} files")

    elif args.mode == "dedupe" and input_path.is_dir():
        duplicates = manager.find_exact_duplicates(input_path)
        print(f"Found {len(duplicates)} groups of duplicate files")

        total_duplicates = sum(len(files) - 1 for files in duplicates.values())
        print(f"Total duplicate files: {total_duplicates}")

        if args.output:
            removed = manager.clean_duplicates(
                duplicates, args.keep_strategy, Path(args.output),
            )
            print(f"Archived {removed} duplicate files to {args.output}")

    elif args.mode == "cleanup" and input_path.is_dir():
        output_dir = Path(args.output) if args.output else None
        report = manager.comprehensive_cleanup(input_path, output_dir)
        print("Comprehensive cleanup completed!")
        print(f"Processed {report['total_files_processed']} files")
        print(f"Archived {report['duplicates_archived']} duplicates")
        print(f"Report saved to: {output_dir}/CLEANUP_REPORT.json")

    else:
        print("Invalid arguments. Use --help for usage information.")


if __name__ == "__main__":
    main()
