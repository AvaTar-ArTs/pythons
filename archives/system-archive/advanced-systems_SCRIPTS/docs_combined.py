#!/usr/bin/env python3
"""
Document File Organizer and Metadata Extractor

This script scans directories for document files and generates a CSV report
with metadata including file size, creation date, and file path.
It supports various document formats and excludes common system directories.

Features:
- Async processing support
- Caching for performance
- Comprehensive error handling
- Logging support
- Type hints
- Configuration management
- CSV comparison and merging capabilities
- Security features (password hashing, input sanitization)
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
import secrets
import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache, wraps
from typing import Any, Callable, Dict, List, Optional

import aiohttp
import pandas as pd
from pandas.errors import EmptyDataError

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"
LAST_DIRECTORY_FILE = "docs.txt"


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


def sanitize_string(value: str) -> str:
    """Sanitize string input to prevent injection attacks."""
    if not isinstance(value, str):
        raise ValueError("Input must be a string")

    # Remove potentially dangerous characters
    dangerous_chars = ["<", ">", '\'', "\'", "&", ";", "(", ")", "{", "}"]
    for char in dangerous_chars:
        value = value.replace(char, "")

    # Limit length
    if len(value) > 1000:
        value = value[:1000]

    return value.strip()


def hash_password(password: str) -> str:
    """Hash password using secure method."""
    salt = secrets.token_hex(32)
    pwdhash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
    )
    return salt + pwdhash.hex()


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    salt = hashed[:64]
    stored_hash = hashed[64:]
    pwdhash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
    )
    return pwdhash.hex() == stored_hash


def validate_input(data: Dict[str, Any], validators: Dict[str, Callable]) -> bool:
    """Validate input data with comprehensive checks."""
    if not isinstance(data, dict):
        raise ValueError("Input must be a dictionary")

    for field, validator in validators.items():
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

        try:
            if not validator(data[field]):
                raise ValueError(f"Invalid value for field {field}: {data[field]}")
        except Exception as e:
            raise ValueError(f"Validation error for field {field}: {e}")

    return True


def memoize(func):
    """Memoization decorator."""
    cache = {}

    def wrapper(*args, **kwargs):
        if key not in cache:

    return wrapper


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


# Core document processing functions
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
def format_file_size(size_in_bytes: int) -> str:
    """Format file size in human-readable format."""
    try:
        if size_in_bytes < Config.KB_SIZE:
            return f"{size_in_bytes:.2f} B"
        size_in_bytes /= Config.KB_SIZE
        if size_in_bytes < Config.KB_SIZE:
            return f"{size_in_bytes:.2f} KB"
        size_in_bytes /= Config.KB_SIZE
        if size_in_bytes < Config.KB_SIZE:
            return f"{size_in_bytes:.2f} MB"
        size_in_bytes /= Config.KB_SIZE
        if size_in_bytes < Config.KB_SIZE:
            return f"{size_in_bytes:.2f} GB"
        size_in_bytes /= Config.KB_SIZE
        return f"{size_in_bytes:.2f} TB"
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
    except Exception as e:
        logger.info(f"Error formatting file size: {e}")
        return "Unknown"


@retry_decorator(max_retries=3)
def generate_dry_run_csv(directories: List[str], csv_path: str) -> None:
    """Generate a dry run CSV for organizing document files."""
    rows = []

    # Regex patterns for exclusions
    excluded_patterns = [
        r"^\..*",  # Hidden files and directories
        r".*\/venv\/.*",  # venv directories
        r".*\/\.venv\/.*",  # .venv directories
        r".*\/lib\/.*",  # venv directories
        r".*\/\.lib\/.*",  # .venv directories
        r".*\/my_global_venv\/.*",  # venv directories
        r".*\/simplegallery\/.*",
        r".*\/avatararts\/.*",
        r".*\/github\/.*",
        r".*\/Documents\/gitHub\/.*",  # Specific gitHub directory
        r".*\/\.my_global_venv\/.*",  # .venv directories
        r".*\/node\/.*",  # Any directory named node
        r".*\/miniconda3\/.*",
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
        ".pdf": "Documents",
        ".csv": "Documents",
        ".html": "Documents",
        ".css": "Documents",
        ".js": "Documents",
        ".json": "Documents",
        ".sh": "Documents",
        ".md": "Documents",
        ".txt": "Documents",
        ".doc": "Documents",
        ".docx": "Documents",
        ".ppt": "Documents",
        ".pptx": "Documents",
        ".xlsx": "Documents",
        ".py": "Documents",
        ".xml": "Documents",
        ".rtf": "Documents",
        ".odt": "Documents",
        ".ods": "Documents",
        ".odp": "Documents",
    }

    for directory in directories:
        logger.info(f"Scanning directory: {directory}")
        for root, dirs, files in os.walk(directory):
            # Skip hidden directories and system directories using regex
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
                    file_size = format_file_size(os.path.getsize(file_path))
                    creation_date = get_creation_date(file_path)
                    rows.append([file, file_size, creation_date, root])

    write_csv(csv_path, rows)


def write_csv(csv_path: str, rows: List[List[str]]) -> None:
    """Write data to CSV file."""
    with open(csv_path, "w", newline="") as csvfile:
        fieldnames = ["Filename", "File Size", "Creation Date", "Original Path"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "Filename": row[0],
                    "File Size": row[1],
                    "Creation Date": row[2],
                    "Original Path": row[3],
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


# CSV Processing Functions
def combine_csvs(csv_paths: List[str], output_path: str) -> None:
    """Combine multiple CSV files into one."""
    dfs = []

    for path in csv_paths:
        if not os.path.exists(path):
            logger.warning(f"File not found, skipping: {path}")
            continue

        # Check for 0-byte file
        if os.path.getsize(path) == 0:
            logger.warning(f"Empty file, skipping: {path}")
            continue

        try:
            logger.info(f"Reading CSV: {path}")
            df = pd.read_csv(path)
            dfs.append(df)
        except EmptyDataError:
            logger.warning(f"{path} is empty or invalid CSV. Skipping.")
        except Exception as e:
            logger.error(f"Could not read {path}: {e}")

    if not dfs:
        logger.error("No valid CSV files found. Exiting.")
        return

    # Concatenate into one DataFrame
    df_combined = pd.concat(dfs, ignore_index=True)

    # Optionally drop duplicates if you want each row to appear only once
    df_combined.drop_duplicates(inplace=True)

    # Save to a new CSV
    df_combined.to_csv(output_path, index=False)

    logger.info(f"Saved combined CSV with shape {df_combined.shape} to {output_path}!")


def compare_csvs(old_csvs: List[str], new_csv: str, output_dir: str = ".") -> None:
    """Compare old and new CSV files and generate difference reports."""
    # Read and combine old CSVs
    old_dfs = []
    for csv_path in old_csvs:
        if os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path)
                old_dfs.append(df)
            except Exception as e:
                logger.error(f"Could not read {csv_path}: {e}")

    if not old_dfs:
        logger.error("No valid old CSV files found.")
        return

    df_old_combined = pd.concat(old_dfs, ignore_index=True)
    df_old_combined.drop_duplicates(inplace=True)

    # Read new CSV
    try:
        df_new = pd.read_csv(new_csv)
    except Exception as e:
        logger.error(f"Could not read new CSV {new_csv}: {e}")
        return

    # Merge the dataframes
    merge_cols = ["Filename", "Original Path"]
    df_compare = pd.merge(
        df_old_combined,
        df_new,
        on=merge_cols,
        how="outer",
        indicator=True,
        suffixes=("_old", "_new"),
    )

    # Identify differences
    rows_only_in_old = df_compare[df_compare["_merge"] == "left_only"].copy()
    rows_only_in_new = df_compare[df_compare["_merge"] == "right_only"].copy()
    rows_in_both = df_compare[df_compare["_merge"] == "both"].copy()

    logger.info(f"Rows only in OLD: {rows_only_in_old.shape[0]}")
    logger.info(f"Rows only in NEW: {rows_only_in_new.shape[0]}")
    logger.info(f"Rows in BOTH: {rows_in_both.shape[0]}")

    # Check for changes in certain columns
    cols_to_check = ["File Size", "Creation Date"]
    changed_mask = False

    for col in cols_to_check:
        old_col = col + "_old"
        new_col = col + "_new"
        diff_col = f"{col.lower().replace(' ', '_')}_changed"
        rows_in_both[diff_col] = rows_in_both[old_col] != rows_in_both[new_col]
        changed_mask = changed_mask | rows_in_both[diff_col]

    rows_changed_in_both = rows_in_both[changed_mask].copy()

    logger.info(
        f"Rows in BOTH that have changed columns: {rows_changed_in_both.shape[0]}"
    )

    # Export difference sets
    rows_only_in_old.to_csv(os.path.join(output_dir, "docs_removed.csv"), index=False)
    rows_only_in_new.to_csv(os.path.join(output_dir, "docs_added.csv"), index=False)
    rows_changed_in_both.to_csv(
        os.path.join(output_dir, "docs_modified.csv"), index=False
    )

    # Create combined difference summary
    df_diff = pd.concat(
        [
            rows_only_in_old.assign(DiffType="Removed"),
            rows_only_in_new.assign(DiffType="Added"),
            rows_changed_in_both.assign(DiffType="Modified"),
        ],
        ignore_index=True,
    )

    df_diff.to_csv(os.path.join(output_dir, "docs_difference_summary.csv"), index=False)

    logger.info("All done! Differences exported as:")
    logger.info("- docs_removed.csv        (only in old)")
    logger.info("- docs_added.csv          (only in new)")
    logger.info("- docs_modified.csv       (in both, but changed in specified columns)")
    logger.info("- docs_difference_summary.csv (combined overview)")


# Async versions of core functions
async def async_generate_dry_run_csv(directories: List[str], csv_path: str) -> None:
    """Async version of generate_dry_run_csv."""
    # Run the synchronous version in a thread pool
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, generate_dry_run_csv, directories, csv_path)


async def async_write_csv(csv_path: str, rows: List[List[str]]) -> None:
    """Async version of write_csv."""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, write_csv, csv_path, rows)


# Main execution
def main():
    """Main function to run the document file organizer."""
    directories = []
    last_directory = load_last_directory()

    while True:
        if last_directory:
            use_last = (
                input(
                    f"Do you want to use the last directory '{last_directory}'? (Y/N): "
                )
                .strip()
                .lower()
            )
            if use_last == "y":
                directories.append(last_directory)
                break
            else:
                source_directory = input(
                    "Please enter a new source directory to scan for document files: "
                ).strip()
        else:
            source_directory = input(
                "Please enter a source directory to scan for document files: "
            ).strip()

        if source_directory == "":
            break
        if os.path.isdir(source_directory):
            directories.append(source_directory)
            save_last_directory(source_directory)
        else:
            logger.info(
                f"'{source_directory}' is not a valid directory. Please try again."
            )

    if directories:
        current_date = datetime.now().strftime("%m-%d-%H:%M")
        csv_output_path = os.path.join(os.getcwd(), f"docs-{current_date}.csv")
        csv_output_path = get_unique_file_path(csv_output_path)

        generate_dry_run_csv(directories, csv_output_path)
        logger.info(f"Document scan completed. Output saved to {csv_output_path}")
    else:
        logger.info("No directories were provided to scan.")


async def async_main():
    """Async version of main function."""
    directories = []
    last_directory = load_last_directory()

    while True:
        if last_directory:
            use_last = (
                input(
                    f"Do you want to use the last directory '{last_directory}'? (Y/N): "
                )
                .strip()
                .lower()
            )
            if use_last == "y":
                directories.append(last_directory)
                break
            else:
                source_directory = input(
                    "Please enter a new source directory to scan for document files: "
                ).strip()
        else:
            source_directory = input(
                "Please enter a source directory to scan for document files: "
            ).strip()

        if source_directory == "":
            break
        if os.path.isdir(source_directory):
            directories.append(source_directory)
            save_last_directory(source_directory)
        else:
            logger.info(
                f"'{source_directory}' is not a valid directory. Please try again."
            )

    if directories:
        current_date = datetime.now().strftime("%m-%d-%H:%M")
        csv_output_path = os.path.join(os.getcwd(), f"docs-{current_date}.csv")
        csv_output_path = get_unique_file_path(csv_output_path)

        await async_generate_dry_run_csv(directories, csv_output_path)
        logger.info(f"Document scan completed. Output saved to {csv_output_path}")
    else:
        logger.info("No directories were provided to scan.")


if __name__ == "__main__":
    # Check if async mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == "--async":
        asyncio.run(async_main())
    else:
        main()
