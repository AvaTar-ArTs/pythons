"""
Simple Photo Gallery Logic

This module provides functionality for simple photo gallery logic.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import shutil
import sqlite3
from datetime import datetime

import logging

logger = logging.getLogger(__name__)


def get_creation_date(filepath):
    """Get the creation date of the file."""
    return datetime.fromtimestamp(os.path.getctime(filepath)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def custom_tags(filename, filepath):
    """Determine custom tags based on file content or filename patterns."""
    custom_tag = None
    if filename.endswith(".py"):
        with open(filepath, "r") as file:
            content = file.read()
            if "import pandas" in content:
                custom_tag = "python_data_analysis"
            elif "import tensorflow" in content:
                custom_tag = "python_ml"
            else:
                custom_tag = "python_misc"
    elif filename.endswith(".txt"):
        with open(filepath, "r") as file:
            content = file.read()
            if "project" in content:
                custom_tag = "text_project"
            else:
                custom_tag = "text_misc"
    # Add more custom rules as needed
    return custom_tag


def organize_files(directory):
    """organize_files function."""

    file_types = {
        ".pdf": "pdf_files",
        ".csv": "csv_files",
        ".py": "python_files",
        ".html": "web_project_files",
        ".css": "web_project_files",
        ".js": "web_project_files",
        ".json": "web_project_files",
        ".sh": "shell_files",
        ".md": "markdown_files",
        ".txt": "text_files",
        ".svg": "svg_files",
        ".png": "image_files",
        ".jpg": "image_files",
        ".jpeg": "image_files",
        ".webm": "video_files",
        ".zip": "zip_files",
    }

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        file_ext = os.path.splitext(filename)[1].lower()
        tag = file_types.get(file_ext, "other_files")

        custom_tag = custom_tags(filename, file_path)
        if custom_tag:
            tag = custom_tag

        dest_dir = os.path.join(directory, tag)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        shutil.move(file_path, os.path.join(dest_dir, filename))
        logger.info(f"Moved {filename} to {dest_dir}")
        insert_metadata(filename, tag, get_creation_date(file_path))

    """tag_files function."""


def tag_files(directory):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(os.path.join(directory, "tags.txt"), "a") as tag_file:
        for tag_dir in os.listdir(directory):
            tag_file.write(f"{tag_dir}: {timestamp}\n")

    """create_database function."""


def create_database():
    conn = sqlite3.connect("file_metadata.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS files
                 (filename TEXT, tag TEXT, creation_date TEXT, timestamp TEXT)"""
    )
    conn.commit()
    conn.close()
    """insert_metadata function."""


def insert_metadata(filename, tag, creation_date):
    conn = sqlite3.connect("file_metadata.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO files (filename, tag, creation_date, timestamp) VALUES (?, ?, ?, ?)",
        (filename, tag, creation_date, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    project_directory = Path(str(Path.home()) + "/Pictures/Bcovers")
    create_database()
    organize_files(project_directory)
    tag_files(project_directory)
