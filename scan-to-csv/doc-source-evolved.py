#!/usr/bin/env python3
"""
Document inventory scanner with flexible output and collision handling.

Scans directories for document-type files (.md, .csv, .py, etc.) and generates
CSV inventories with file metadata (size, creation date, path).

Features:
  - Numeric collision suffix strategy (_1, _2, _3) by default
  - CLI options for output directory, quiet mode, dry-run
  - Progress indicators for large scans
  - Summary statistics (file count, total size)
  - Regex-based exclusion patterns for common build/cache artifacts
  - Safe directory creation with fallback naming
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from datetime import datetime

from exclude_patterns import FULL_EXCLUDED_PATTERNS


# Configuration
LAST_DIRECTORY_FILE = "docs.txt"

DOC_EXTENSIONS = {
    ".pdf", ".csv", ".html", ".css", ".js", ".json", ".sh", ".md", ".txt",
    ".doc", ".docx", ".ppt", ".pptx", ".xlsx", ".py", ".xml",
}


def get_creation_date(filepath: str) -> str:
    """Get file creation date formatted as MM-DD-YY."""
    try:
        return datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%m-%d-%y")
    except Exception as e:
        if not QUIET_MODE:
            print(f"⚠ Error getting creation date for {filepath}: {e}", file=sys.stderr)
        return "Unknown"


def format_file_size(size_bytes: float) -> str:
    """Format file size into human-readable string (B, KB, MB, GB, TB)."""
    try:
        units = ["B", "KB", "MB", "GB", "TB"]
        size = float(size_bytes)

        for unit in units[:-1]:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024

        return f"{size:.2f} TB"
    except Exception as e:
        if not QUIET_MODE:
            print(f"⚠ Error formatting file size: {e}", file=sys.stderr)
        return "Unknown"


def is_excluded(path: str, patterns: list[str]) -> bool:
    """Check if path matches any exclusion pattern."""
    return any(re.match(pattern, path) for pattern in patterns)


def scan_directories(directories: list[str], dry_run: bool = False) -> list[list[str]]:
    """Scan directories and collect document file metadata."""
    rows = []
    file_count = 0
    total_size = 0

    for directory in directories:
        if not QUIET_MODE:
            print(f"📁 Scanning: {directory}")

        for root, dirs, files in os.walk(directory):
            # Filter out excluded directories
            dirs[:] = [
                d for d in dirs
                if not is_excluded(os.path.join(root, d), FULL_EXCLUDED_PATTERNS)
            ]

            for file in files:
                file_path = os.path.join(root, file)

                # Skip excluded files
                if is_excluded(file_path, FULL_EXCLUDED_PATTERNS):
                    continue

                # Only process document types
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext not in DOC_EXTENSIONS:
                    continue

                try:
                    file_size = os.path.getsize(file_path)
                    total_size += file_size
                    file_count += 1

                    size_str = format_file_size(file_size)
                    date_str = get_creation_date(file_path)

                    rows.append([file, size_str, date_str, root])

                    # Progress indicator for large scans
                    if not QUIET_MODE and file_count % 100 == 0:
                        print(f"  ✓ {file_count} files processed...", end="\r")

                except FileNotFoundError:
                    if not QUIET_MODE:
                        print(f"⚠ File not found during scan, skipping: {file_path}", file=sys.stderr)
                    continue

    if not QUIET_MODE and file_count > 0:
        print(f"\n✓ Scan complete: {file_count} files, {format_file_size(total_size)} total")

    return rows


def write_csv(csv_path: str, rows: list[list[str]]) -> None:
    """Write collected rows to CSV file."""
    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Filename", "File Size", "Creation Date", "Original Path"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow({
                    "Filename": row[0],
                    "File Size": row[1],
                    "Creation Date": row[2],
                    "Original Path": row[3],
                })
        if not QUIET_MODE:
            print(f"✓ CSV written: {csv_path}")
    except Exception as e:
        print(f"✗ Error writing CSV: {e}", file=sys.stderr)
        sys.exit(1)


def get_unique_file_path(base_path: str) -> str:
    """
    Return a unique file path by appending numeric suffix if needed.

    If base_path exists, tries: _1, _2, _3, ... until finding an available name.
    """
    if not os.path.exists(base_path):
        return base_path

    base, ext = os.path.splitext(base_path)
    counter = 1

    while True:
        new_path = f"{base}_{counter}{ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1


def sanitize_filename(name: str) -> str:
    """Convert folder name into safe filename by replacing invalid characters."""
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)


def save_last_directory(directory: str) -> None:
    """Save the last scanned directory for next run."""
    try:
        with open(LAST_DIRECTORY_FILE, "w", encoding="utf-8") as f:
            f.write(directory)
    except Exception as e:
        if not QUIET_MODE:
            print(f"⚠ Could not save last directory: {e}", file=sys.stderr)


def load_last_directory() -> str | None:
    """Load the last scanned directory if available."""
    if os.path.exists(LAST_DIRECTORY_FILE):
        try:
            with open(LAST_DIRECTORY_FILE, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            return None
    return None


def main():
    """Main entry point with CLI argument parsing."""
    global QUIET_MODE

    parser = argparse.ArgumentParser(
        description="Scan directories for document files and generate CSV inventory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan my-supremepowers directory, output to current directory
  %(prog)s /Users/steven/my-supremepowers

  # Scan multiple directories
  %(prog)s /Users/steven/my-supremepowers /Users/steven/iterm2

  # Specify output directory
  %(prog)s /Users/steven/my-supremepowers --output ~/csv-reports

  # Dry run (preview output filename without scanning)
  %(prog)s /Users/steven/my-supremepowers --dry-run

  # Quiet mode (no progress output)
  %(prog)s /Users/steven/my-supremepowers --quiet
        """
    )

    parser.add_argument(
        "directories",
        nargs="*",
        help="Directories to scan (default: prompt for input or use last directory)"
    )
    parser.add_argument(
        "-o", "--output",
        dest="output_dir",
        default=None,
        help="Output directory for CSV file (default: first scanned directory)"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress output"
    )
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help="Preview output filename without scanning"
    )

    args = parser.parse_args()
    QUIET_MODE = args.quiet

    directories = args.directories if args.directories else []

    # Interactive mode if no directories provided
    if not directories:
        last_dir = load_last_directory()

        while True:
            if last_dir:
                use_last = input(
                    f"Use last directory '{last_dir}'? (Y/N): "
                ).strip().lower()

                if use_last == "y":
                    directories.append(last_dir)
                    break
                else:
                    source = input("Enter new directory to scan: ").strip()
            else:
                source = input("Enter directory to scan: ").strip()

            if not source:
                print("No directory provided.", file=sys.stderr)
                sys.exit(1)

            if os.path.isdir(source):
                directories.append(source)
                save_last_directory(source)
                break
            else:
                print(f"✗ Not a valid directory: '{source}'", file=sys.stderr)

    if not directories:
        print("✗ No directories to scan.", file=sys.stderr)
        sys.exit(1)

    # Generate output filename
    folder_names = [
        sanitize_filename(os.path.basename(os.path.normpath(d)))
        for d in directories
    ]
    joined_names = "_".join(folder_names) or "root"
    csv_filename = f"docs-{joined_names}.csv"

    # Determine output path
    output_base = args.output_dir or directories[0]
    csv_output_path = os.path.join(output_base, csv_filename)
    csv_output_path = get_unique_file_path(csv_output_path)

    if not QUIET_MODE:
        print(f"📄 Output: {csv_output_path}")

    if args.dry_run:
        print("(Dry run - no scan performed)")
        return

    # Perform scan and write results
    rows = scan_directories(directories, dry_run=args.dry_run)

    if rows:
        write_csv(csv_output_path, rows)
    else:
        print("⚠ No document files found.", file=sys.stderr)


if __name__ == "__main__":
    QUIET_MODE = False
    main()
