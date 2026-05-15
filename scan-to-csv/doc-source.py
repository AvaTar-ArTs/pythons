import csv
import os
import re
import sys
from datetime import datetime

from exclude_patterns import FULL_EXCLUDED_PATTERNS


# Constants
LAST_DIRECTORY_FILE = "docs.txt"


def get_creation_date(filepath):
    """Get the creation date of a file formatted as MM-DD-YY."""
    try:
        return datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%m-%d-%y")
    except Exception as e:
        print(f"Error getting creation date for {filepath}: {e}")
        return "Unknown"


def format_file_size(size_in_bytes):
    """Format file size into human-readable string with appropriate units."""
    try:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} B"
        size_in_bytes /= 1024
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} KB"
        size_in_bytes /= 1024
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} MB"
        size_in_bytes /= 1024
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} GB"
        size_in_bytes /= 1024
        return f"{size_in_bytes:.2f} TB"
    except Exception as e:
        print(f"Error formatting file size: {e}")
        return "Unknown"


def generate_dry_run_csv(directories, csv_path):
    """
    Scan the given directories for document files and write their details to a CSV file.
    """
    rows = []

    excluded_patterns = FULL_EXCLUDED_PATTERNS

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
    }

    for directory in directories:
        for root, dirs, files in os.walk(directory):
            # Filter out excluded directories using regex patterns
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

                # Skip files matching excluded patterns
                if any(re.match(pattern, file_path) for pattern in excluded_patterns):
                    continue

                file_ext = os.path.splitext(file)[1].lower()

                if file_ext in file_types:
                    try:
                        file_size = format_file_size(os.path.getsize(file_path))
                        creation_date = get_creation_date(file_path)
                        rows.append([file, file_size, creation_date, root])
                    except FileNotFoundError:
                        print(f"File not found during scan, skipping: {file_path}")
                        continue

    write_csv(csv_path, rows)


def write_csv(csv_path, rows):
    """Write the collected file information to a CSV file."""
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
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


def get_unique_file_path(base_path):
    """
    If the base_path exists, append a counter suffix to create a unique file path.
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


def save_last_directory(directory):
    """Save the last scanned directory to a file."""
    with open(LAST_DIRECTORY_FILE, "w", encoding="utf-8") as file:
        file.write(directory)


def load_last_directory():
    """Load the last scanned directory from a file, if it exists."""
    if os.path.exists(LAST_DIRECTORY_FILE):
        with open(LAST_DIRECTORY_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    return None


def sanitize_filename(name):
    """
    Sanitize a string to be safe for use as a filename by replacing invalid characters with underscores.
    """
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)


if __name__ == "__main__":
    # Accept command line arguments for directories
    if len(sys.argv) > 1:
        directories = sys.argv[1:]
    else:
        # Interactive mode fallback
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
                break
            else:
                print(f"'{source_directory}' is not a valid directory. Please try again.")

    if directories:
        print(f"Scanning directories: {directories}")

        # Generate CSV filename based on scanned folder names
        folder_names = [sanitize_filename(os.path.basename(os.path.normpath(d))) for d in directories]
        joined_folder_names = "_".join(folder_names)
        if not joined_folder_names:
            joined_folder_names = "root"

        csv_filename = f"docs-{joined_folder_names}.csv"
        csv_output_path = os.path.join(os.getcwd(), csv_filename)
        csv_output_path = get_unique_file_path(csv_output_path)

        generate_dry_run_csv(directories, csv_output_path)
        print(f"Document scan completed. Output saved to {csv_output_path}")
    else:
        print("No directories were provided to scan.")

