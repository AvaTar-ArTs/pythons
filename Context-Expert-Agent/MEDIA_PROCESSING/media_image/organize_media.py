# TODO: Resolve circular dependencies by restructuring imports

# String constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"


# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_PORT = 8080


import asyncio
import aiohttp

async def async_request(url: str, session: aiohttp.ClientSession) -> str:
    """Async HTTP request."""
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        logger.error(f"Async request failed: {e}")
        return None

async def process_urls(urls: List[str]) -> List[str]:
    """Process multiple URLs asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [async_request(url, session) for url in urls]
        return await asyncio.gather(*tasks)


def batch_processor(items: List[Any], batch_size: int = 100):
    """Generator to process items in batches."""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

def file_line_reader(file_path: str):
    """Generator to read file line by line."""
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()


from functools import wraps

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def retry_decorator(max_retries = 3):
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


from abc import ABC, abstractmethod

@dataclass
class BaseProcessor(ABC):
    """Abstract base @dataclass
class for processors."""

    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process data."""
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate data."""
        pass


@dataclass
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

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio
import logging
import os
import shutil
import sys

@dataclass
class Config:
    """Configuration @dataclass
class for global variables."""
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
    cache = {}
    key = str(args) + str(kwargs)
    cache[key] = func(*args, **kwargs)
    logger = logging.getLogger(__name__)
    DEFAULT_BASE_DIR = Path("~/Music/nocTurneMeLoDieS/MP3")
    SUFFIXES = ("_analysis", "_transcript")
    MEDIA_EXTS = {".mp3", ".m4a", ".mp4", ".wav"}
    TEXT_EXTS = {".txt"}
    IMAGE_EXTS = {".png"}  # cover image
    ext_lower = ext.lower()
    entries = [e for e in base_dir.iterdir() if e.is_file()]
    moved = 0
    skipped = 0
    stem = f.stem
    ext = f.suffix  # includes the dot
    ext_lower = ext.lower()
    album_name = normalized_album_name(stem)
    album_folder = base_dir / album_name
    dest_name = canonical_dest_name(album_name, ext_lower, stem)
    dest_path = album_folder / dest_name
    base_dir = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_BASE_DIR
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    skipped + = 1
    album_folder.mkdir(parents = True, exist_ok
    skipped + = 1
    moved + = 1
    skipped + = 1


# Constants



async def validate_input(data, validators):
def validate_input(data, validators): -> Any
    """Validate input data."""
    for field, validator in validators.items():
        if field in data:
            if not validator(data[field]):
                raise ValueError(f"Invalid {field}: {data[field]}")
    return True


async def memoize(func):
def memoize(func): -> Any
    """Memoization decorator."""

    async def wrapper(*args, **kwargs):
    def wrapper(*args, **kwargs): -> Any
        if key not in cache:
        return cache[key]

    return wrapper


@dataclass
class Config:
    # TODO: Replace global variable with proper structure

#!/usr/bin/env python3
"""
Organize media and related text files by album base name.

- Scans a single-level directory (no recursion) for files.
- Derives an album_name from the filename by removing the extension and
  stripping known suffixes like "_analysis" and "_transcript".
- Creates a folder named after that album_name.
- Moves any of these files into that folder, renaming them to a canonical pattern:
    * {album_name}.mp3
    * {album_name}.m4a
    * {album_name}.mp4
    * {album_name}_analysis.txt
    * {album_name}_transcript.txt
    * {album_name}.png    (cover image if present in the base directory)
- Skips moving if the destination already exists (to avoid overwriting).

Usage:
    python organize_media.py [BASE_DIR]

If BASE_DIR is not provided, defaults to:
    ~/Music/nocTurneMeLoDieS/MP3

Notes:
- This script is macOS-friendly and uses only the standard library.
"""



# Known suffixes to normalize album base names

# Extensions we manage (case-insensitive)


async def normalized_album_name(stem: str) -> str:
def normalized_album_name(stem: str) -> str:
    """Strip known suffixes from a filename stem to yield the album name."""
    for suf in SUFFIXES:
        if stem.endswith(suf):
            return stem[: -len(suf)]
    return stem


async def canonical_dest_name(album: str, ext: str, original_stem: str) -> str:
def canonical_dest_name(album: str, ext: str, original_stem: str) -> str:
    """Return canonical destination filename for a given extension.
    - For analysis/transcript text, keep the suffix in the filename.
    - For media and cover image, use {album}{ext}.
    """
    if ext_lower == ".txt":
        # Preserve whether it was analysis or transcript by examining the original stem
        if original_stem.endswith("_analysis"):
            return f"{album}_analysis.txt"
        elif original_stem.endswith("_transcript"):
            return f"{album}_transcript.txt"
        # Fallback: generic text alongside album
        return f"{album}.txt"
    else:
        # Media or image: canonicalized to album name + ext
        return f"{album}{ext_lower}"


async def organize_files(base_dir: Path) -> None:
def organize_files(base_dir: Path) -> None:
    if not base_dir.exists() or not base_dir.is_dir():
        logger.info(f"Base directory does not exist or is not a directory: {base_dir}")
        sys.exit(1)

    if not entries:
        logger.info("No files found to organize.")
        return


    # First pass: compute album folders and move items
    for f in entries:

        # We only care about our known sets
        if ext_lower not in MEDIA_EXTS | TEXT_EXTS | IMAGE_EXTS:
            continue

        if not album_name:
            # Safety: if stripping left empty (shouldn't happen), skip
            continue

        # Make the album folder


        # If destination already exists, skip to avoid overwrite
        if dest_path.exists():
            logger.info(f"Skip (exists): {f.name} -> {dest_path}")
            continue

        # Move the file
        try:
            shutil.move(str(f), str(dest_path))
            logger.info(f"Moved: {f.name} -> {dest_path}")
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            logger.info(f"ERROR moving {f.name} -> {dest_path}: {e}")

    logger.info(f"Done. Moved: {moved}, Skipped: {skipped}")


if __name__ == "__main__":
    organize_files(base_dir)
    logger.info("All files have been organized successfully.")
