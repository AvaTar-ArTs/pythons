"""
Organizer 1

This module provides functionality for organizer 1.

Author: Auto-generated
Date: 2025-11-01
"""

import csv
import logging
import os
import re
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv
from mutagen import File  # For handling .webm files
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from openai import OpenAI
from PIL import Image
from tenacity import retry, stop_after_attempt, wait_exponential

# Constants
CONSTANT_3600 = 3600
CONSTANT_15000 = 15000


# Load environment variables
load_dotenv(Path("/Users/steven/.env"))

# Initialize OpenAI
try:
    openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    logging.error(f"OpenAI initialization failed: {str(e)}")
    openai = None

# Configuration
CONFIG_DIR = Path(Path("/Users/steven/.config/file_organizer"))
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

# Logging setup
LOG_FILE = CONFIG_DIR / "file_organizer.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)

# File type mappings
FILE_TYPES = {
    "audio": {".mp3", ".wav", ".flac", ".aac", ".m4a"},
    "image": {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"},
    "video": {".mp4", ".mkv", ".mov", ".avi", ".wmv", ".webm"},
    "scripts": {".py"},
}

# Regex patterns for exclusions
EXCLUDED_PATTERNS = [
    re.compile(r"^\..*"),  # Hidden files/dirs (starting with dot)
    re.compile(r".*/(?:venv|env|\.venv|\.env)/.*"),  # Python virtual environments
    re.compile(r".*/(?:my_global_venv|\.my_global_venv)/.*"),  # Global venv
    re.compile(
        r".*/(?:simplegallery|avatararts|github)/.*"
    ),  # Specific excluded directories
    re.compile(r".*/Documents/gitHub/.*"),  # GitHub folder inside Documents
    re.compile(r".*/node/.*"),  # Node-related directories
    re.compile(r".*/Movies/(?:CapCut|movavi)/.*"),  # Video editing software
    re.compile(r".*/miniconda3/.*"),  # Conda environments
    re.compile(r".*/Library/.*"),  # macOS Library folder
    re.compile(r".*/\.(?:config|spicetify|gem|zprofile)/.*"),  # Hidden config folders
    re.compile(r".*/\..*"),  # General hidden directories
]


def prompt_for_directory() -> Path:
    """Prompt the user to input a directory path."""
    while True:
        directory = input("Enter the directory to scan (or 'q' to quit): ").strip()
        if directory.lower() == "q":
            logging.info("Exiting as requested by user.")
            exit(0)

        path = Path(directory)
        if path.is_dir():
            return path
        logging.error(f"Invalid directory: {directory}. Please try again.")


@contextmanager
def safe_file_access(filepath: Path):
    """Context manager for safe file handling with error logging."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            yield f
    except Exception as e:
        logging.error(f"Failed to access {filepath}: {str(e)}")
        yield None


def should_exclude(path: Path) -> bool:
    """Check if a path matches any exclusion pattern."""
    return any(pattern.search(str(path)) for pattern in EXCLUDED_PATTERNS)


class FileProcessor:
    """Base class for file processing operations."""

    @staticmethod
    def get_creation_date(filepath: Path) -> str:
        """get_creation_date function."""

        try:
            return datetime.fromtimestamp(filepath.stat().st_ctime).strftime("%m-%d-%y")
        except Exception as e:
            logging.error(f"Creation date error for {filepath}: {str(e)}")
            return "Unknown"

    @staticmethod
        """format_file_size function."""

    def format_file_size(size_in_bytes: int) -> str:
        thresholds = [
            (1 << 40, "TB"),
            (1 << 30, "GB"),
            (1 << 20, "MB"),
            (1 << 10, "KB"),
            (1, "B"),
        ]
        for factor, suffix in thresholds:
            if size_in_bytes >= factor:
                return f"{size_in_bytes / factor:.2f} {suffix}"
        return "Unknown"

        """format_duration function."""

    @staticmethod
    def format_duration(seconds: Optional[float]) -> str:
        if seconds is None:
            return "Unknown"
        try:
            hours, remainder = divmod(seconds, CONSTANT_3600)
            minutes, seconds = divmod(remainder, 60)
            return (
                f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
                if hours
                else f"{int(minutes):02}:{int(seconds):02}"
            )
        except Exception as e:
            logging.error(f"Duration formatting error: {str(e)}")
            return "Unknown"


class MediaProcessor(FileProcessor):
    """Handles media file processing with metadata extraction."""
        """process_audio function."""


    @classmethod
    def process_audio(cls, filepath: Path) -> Optional[Dict]:
        try:
            audio = MP3(filepath, ID3=EasyID3)
            return {
                "type": "audio",
                "path": str(filepath),
                "duration": cls.format_duration(audio.info.length),
                "size": cls.format_file_size(filepath.stat().st_size),
                "created": cls.get_creation_date(filepath),
            }
        except Exception as e:
            logging.error(f"Audio processing failed for {filepath}: {str(e)}")
        """process_image function."""

            return None

    @classmethod
    def process_image(cls, filepath: Path) -> Optional[Dict]:
        try:
            with Image.open(filepath) as img:
                return {
                    "type": "image",
                    "path": str(filepath),
                    "dimensions": f"{img.width}x{img.height}",
                    "dpi": img.info.get("dpi", (None, None)),
                    "size": cls.format_file_size(filepath.stat().st_size),
                    "created": cls.get_creation_date(filepath),
                }
        except Exception as e:
        """process_video function."""

            logging.error(f"Image processing failed for {filepath}: {str(e)}")
            return None

    @classmethod
    def process_video(cls, filepath: Path) -> Optional[Dict]:
        try:
            if filepath.suffix.lower() == ".webm":
                # Use mutagen.File for .webm files
                video = File(filepath)
                duration = video.info.length
            else:
                # Use MP4 for other video formats
                video = MP4(filepath)
                duration = video.info.length

            return {
                "type": "video",
                "path": str(filepath),
                "duration": cls.format_duration(duration),
                "size": cls.format_file_size(filepath.stat().st_size),
                "created": cls.get_creation_date(filepath),
            }
        except Exception as e:
            logging.error(f"Video processing failed for {filepath}: {str(e)}")
            return None


class ScriptAnalyzer:
    """Handles script analysis using OpenAI."""

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def analyze_scripts_batch(self, scripts: List[Dict]) -> List[Dict]:
        """Analyze multiple scripts in a single API request."""
        if not openai:
            return [{"error": "OpenAI client not initialized"}] * len(scripts)

        try:
            messages = [
                {
                    "role": "user",
                    "content": f"Analyze this script:\n{script['content'][:CONSTANT_15000]}\n\nReturn categories and a title suggestion.",
                }
                for script in scripts
            ]

            response = openai.chat.completions.create(model="gpt-4", messages=messages)
            return [
                self._parse_response(choice.message.content, script["path"])
                for choice, script in zip(response.choices, scripts)
        """_parse_response function."""

            ]
        except Exception as e:
            logging.error(f"AI analysis failed: {str(e)}")
            return [{"error": str(e)}] * len(scripts)

    def _parse_response(self, response: str, filepath: Path) -> Dict:
        # Add your custom response parsing logic here
        return {
            "path": str(filepath),
            "name": filepath.name,
            "categories": "Uncategorized",
            "title": "Untitled",
            "analysis": response,
        }


def process_directory(
    root_dir: Path, processor: MediaProcessor, file_type: str
) -> List[Dict]:
    """Process all files in directory with appropriate handlers."""
    results = []
    for item in root_dir.rglob("*"):
        if should_exclude(item):
            continue

        if item.is_file() and item.suffix.lower() in FILE_TYPES[file_type]:
            handler = {
                "audio": processor.process_audio,
                "image": processor.process_image,
                "video": processor.process_video,
            }.get(file_type)

            if handler:
                result = handler(item)
                if result:
                    results.append(result)
    return results


def write_results(results: List[Dict], output_path: Path):
    """Write processed results to CSV."""
    if not results:
        logging.warning("No results to write")
        return

    fieldnames = list(results[0].keys())
    try:
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        logging.info(f"Successfully wrote {len(results)} records to {output_path}")
    except Exception as e:
        logging.error(f"Failed to write CSV: {str(e)}")


def main():
    """main function."""

    # Initialize processors
    media_processor = MediaProcessor()
    script_analyzer = ScriptAnalyzer()

    # Prompt for directory
    directory = prompt_for_directory()

    # Process media files
    for file_type in ["audio", "image", "video"]:
        results = process_directory(directory, media_processor, file_type)
        if results:
            output_path = CONFIG_DIR / f"{file_type}_analysis.csv"
            write_results(results, output_path)

    # Process scripts
    script_results = []
    scripts_to_analyze = []
    for script_path in directory.rglob("*.py"):
        if should_exclude(script_path):
            continue

        with safe_file_access(script_path) as f:
            if f:
                scripts_to_analyze.append({"path": script_path, "content": f.read()})

    # Batch analyze scripts
    if scripts_to_analyze:
        script_results = script_analyzer.analyze_scripts_batch(scripts_to_analyze)
        output_path = CONFIG_DIR / "script_analysis.csv"
        write_results(script_results, output_path)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Operation cancelled by user")
    except Exception as e:
        logging.error(f"Critical failure: {str(e)}", exc_info=True)
