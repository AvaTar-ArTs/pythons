#!/usr/bin/env python3
"""
Image File Organizer and Metadata Extractor

This script scans directories for image files and generates a CSV report
with metadata including file size, dimensions, DPI, creation date, and file path.
It supports various image formats and excludes common system directories.

Features:
- Async processing support
- Caching for performance
- Comprehensive error handling
- Logging support
- Type hints
- Configuration management
- PIL-based image metadata extraction
"""

import asyncio
import csv
import html
import logging
import os
import re
import sys
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache, wraps
from typing import Any, Callable, Dict, List, Optional, Tuple

import aiohttp
from PIL import Image

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"
LAST_DIRECTORY_FILE = "image_data.txt"


@dataclass
class Config:
    """Configuration class for global variables."""

    DPI_300 = 300
    DPI_72 = 72
    KB_SIZE = 1024
    MB_SIZE = 1024 * 1024
    GB_SIZE = 1024 * 1024 * 1024
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = 100
    MAX_FILE_SIZE = 9 * 1024 * 1024  # 9MB
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = 1920
    DEFAULT_HEIGHT = 1080


# Decorators
def timing_decorator(func):
    """Decorator to measure function execution time."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result

    return wrapper


def retry_decorator(max_retries=3):
    """Decorator to retry function on failure."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
            return None

        return wrapper

    return decorator


# Abstract base classes
@dataclass
class BaseProcessor(ABC):
    """Abstract base class for processors."""

    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process data."""
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate data."""
        pass


# Singleton metaclass
class SingletonMeta(type):
    """Thread-safe singleton metaclass."""

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# Utility functions
def sanitize_html(html_content: str) -> str:
    """Sanitize HTML content to prevent XSS."""
    return html.escape(html_content)


def validate_input(data: Dict[str, Any], validators: Dict[str, Callable]) -> bool:
    """Validate input data."""
    for field, validator in validators.items():
        if field in data:
            if not validator(data[field]):
                raise ValueError(f"Invalid {field}: {data[field]}")
    return True


def memoize(func):
    """Memoization decorator."""
    cache = {}

    def wrapper(*args, **kwargs):
        if key not in cache:

    return wrapper


def is_system_path(path: str) -> bool:
    """Check if a path is a system directory that should be excluded."""
    system_paths = [
        "~/Desktop",
        "/System",
        "/Applications",
        "/Library",
        "/usr",
        "/bin",
        "/sbin",
        "/var",
        "/private",
        "/etc",
        "/tmp",
        "/.",
        "/Python",
        "/Documents/Git",
    ]
    return any(path.startswith(system_path) for system_path in system_paths)


# Async utility functions
async def async_request(url: str, session: aiohttp.ClientSession) -> Optional[str]:
    """Async HTTP request."""
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        logger.error(f"Async request failed: {e}")
        return None


async def process_urls(urls: List[str]) -> List[Optional[str]]:
    """Process multiple URLs asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [async_request(url, session) for url in urls]
        return await asyncio.gather(*tasks)


# Core image processing functions
@timing_decorator
def get_creation_date(filepath: str) -> str:
    """Get the creation date of a file."""
    try:
        return datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%m-%d-%y")
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
    except Exception as e:
        logger.info(f"Error getting creation date for {filepath}: {e}")
        return "Unknown"


@timing_decorator
def get_image_metadata(:
    filepath: str,
) -> Tuple[
    Optional[int], Optional[int], Optional[float], Optional[float], Optional[int]
]:
    """Extract metadata from an image file using PIL."""
    try:
        with Image.open(filepath) as img:
            width, height = img.size
            dpi = img.info.get("dpi", (None, None))  # Extract DPI if available
            dpi_x = dpi[0] if dpi and len(dpi) > 0 else None
            dpi_y = dpi[1] if dpi and len(dpi) > 1 else None
            file_size = os.path.getsize(filepath)
            return width, height, dpi_x, dpi_y, file_size
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
    except Exception as e:
        logger.info(f"Error getting image metadata for {filepath}: {e}")
        return None, None, None, None, None


@timing_decorator
def format_file_size(size_in_bytes: int) -> str:
    """Format file size in human-readable format."""
    try:
        thresholds = [
            (Config.KB_SIZE**4, "TB"),
            (Config.KB_SIZE**3, "GB"),
            (Config.KB_SIZE**2, "MB"),
            (Config.KB_SIZE**1, "KB"),
            (Config.KB_SIZE**0, "B"),
        ]
        for factor, suffix in thresholds:
            if size_in_bytes >= factor:
                break
        return f"{size_in_bytes / factor:.2f} {suffix}"
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
    except Exception as e:
        logger.info(f"Error formatting file size: {e}")
        return "Unknown"


@retry_decorator(max_retries=3)
def generate_csv(directories: List[str], csv_path: str) -> None:
    """Generate a CSV for organizing image files."""
    rows = []

    # Regex patterns for exclusions
    excluded_patterns = [
        r"^\..*",  # Hidden files and directories
        r".*\/venv\/.*",  # venv directories
        r".*\/\.venv\/.*",  # .venv directories
        r".*\/my_global_venv\/.*",  # venv directories
        r".*\/simplegallery\/.*",
        r".*\/avatararts\/.*",
        r".*\/github\/.*",
        r".*\/Documents\/gitHub\/.*",  # Specific gitHub directory
        r".*\/\.my_global_venv\/.*",  # .venv directories
        r".*\/node\/.*",  # Any directory named node
        r".*\/Movies\/capcut\/.*",
        r".*\/miniconda3\/.*",
        r".*\/Movies\/movavi\/.*",
        r".*\/env\/.*",  # env directories
        r".*\/\.env\/.*",  # .env directories
        r".*\/Library\/.*",  # Library directories
        r".*\/\.config\/.*",  # .config directories
        r".*\/\.spicetify\/.*",  # .spicetify directories
        r".*\/\.gem\/.*",  # .gem directories
        r".*\/\.zprofile\/.*",  # .zprofile directories
        r"^.*\/\..*",  # Any file or directory starting with a dot
    ]

    file_types = {
        ".jpg": "Image",
        ".jpeg": "Image",
        ".png": "Image",
        ".bmp": "Image",
        ".gif": "Image",
        ".tiff": "Image",
        ".webp": "Image",
        ".svg": "Image",
    }

    for directory in directories:
        logger.info(f"Scanning directory: {directory}")
        for root, dirs, files in os.walk(directory):
            # Skip hidden directories and venv directories using regex
            dirs[:] = [
                d
                for d in dirs
                if not any(
                    re.match(pattern, os.path.join(root, d))
                    for pattern in excluded_patterns
                )
            ]

            for file in files:
                file_path = os.path.join(root, file)

                # Skip files that match the excluded patterns
                if any(re.match(pattern, file_path) for pattern in excluded_patterns):
                    continue

                file_ext = os.path.splitext(file)[1].lower()

                # Add file to rows if it matches the logical file types
                if file_ext in file_types:
                    creation_date = get_creation_date(file_path)
                    width, height, dpi_x, dpi_y, file_size = get_image_metadata(
                        file_path
                    )
                    if width is None or height is None:
                        formatted_size = "Unknown"
                    else:
                        formatted_size = format_file_size(file_size)
                    rows.append(
                        [
                            file,
                            formatted_size,
                            creation_date,
                            width,
                            height,
                            dpi_x,
                            dpi_y,
                            file_path,
                        ]
                    )

    write_csv(csv_path, rows)


def write_csv(csv_path: str, rows: List[List[str]]) -> None:
    """Write data to CSV file."""
    with open(csv_path, "w", newline="") as csvfile:
        fieldnames = [
            "Filename",
            "File Size",
            "Creation Date",
            "Width",
            "Height",
            "DPI_X",
            "DPI_Y",
            "Original Path",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "Filename": row[0],
                    "File Size": row[1],
                    "Creation Date": row[2],
                    "Width": row[3],
                    "Height": row[4],
                    "DPI_X": row[5],
                    "DPI_Y": row[6],
                    "Original Path": row[7],
                }
            )


def get_unique_file_path(base_path: str) -> str:
    """Get a unique file path by appending a counter if file exists."""
    if not os.path.exists(base_path):
        return base_path

    base, ext = os.path.splitext(base_path)
    counter = 1
    while True:
        new_path = f"{base}_{counter}{ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1


def save_last_directory(directory: str) -> None:
    """Save the last used directory to file."""
    with open(LAST_DIRECTORY_FILE, "w") as file:
        file.write(directory)


def load_last_directory() -> Optional[str]:
    """Load the last used directory from file."""
    if os.path.exists(LAST_DIRECTORY_FILE):
        with open(LAST_DIRECTORY_FILE, "r") as file:
            return file.read().strip()
    return None


# Async versions of core functions
async def async_generate_csv(directories: List[str], csv_path: str) -> None:
    """Async version of generate_csv."""
    # Run the synchronous version in a thread pool
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, generate_csv, directories, csv_path)


async def async_write_csv(csv_path: str, rows: List[List[str]]) -> None:
    """Async version of write_csv."""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, write_csv, csv_path, rows)


# Main execution
def main():
    """Main function to run the image file organizer."""
    last_directory = load_last_directory()

    if last_directory:
        directories = [last_directory]
        logger.info(f"Using last directory: {last_directory}")
    else:
        logger.info(
            "No last directory found. Please enter a source directory to scan for image files."
        )
        source_directory = input(
            "Please enter a source directory to scan for image files: "
        ).strip()
        if os.path.isdir(source_directory):
            directories = [source_directory]
            save_last_directory(source_directory)
        else:
            logger.info(f"'{source_directory}' is not a valid directory. Exiting.")
            sys.exit(1)

    if directories:
        current_date = datetime.now().strftime("%m-%d-%H-%M")
        csv_output_path = os.path.join(os.getcwd(), f"image_data-{current_date}.csv")
        csv_output_path = get_unique_file_path(csv_output_path)

        generate_csv(directories, csv_output_path)
        logger.info(f"Image scan completed. Output saved to {csv_output_path}")
    else:
        logger.info("No directories were provided to scan.")


async def async_main():
    """Async version of main function."""
    last_directory = load_last_directory()

    if last_directory:
        directories = [last_directory]
        logger.info(f"Using last directory: {last_directory}")
    else:
        logger.info(
            "No last directory found. Please enter a source directory to scan for image files."
        )
        source_directory = input(
            "Please enter a source directory to scan for image files: "
        ).strip()
        if os.path.isdir(source_directory):
            directories = [source_directory]
            save_last_directory(source_directory)
        else:
            logger.info(f"'{source_directory}' is not a valid directory. Exiting.")
            sys.exit(1)

    if directories:
        current_date = datetime.now().strftime("%m-%d-%H-%M")
        csv_output_path = os.path.join(os.getcwd(), f"image_data-{current_date}.csv")
        csv_output_path = get_unique_file_path(csv_output_path)

        await async_generate_csv(directories, csv_output_path)
        logger.info(f"Image scan completed. Output saved to {csv_output_path}")
    else:
        logger.info("No directories were provided to scan.")


if __name__ == "__main__":
    # Check if async mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == "--async":
        asyncio.run(async_main())
    else:
        main()
