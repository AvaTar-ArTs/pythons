from pathlib import Path
import os

from openai import OpenAI

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_150 = 150


client = OpenAI(api_key=api_key)
import hashlib
import re
import shutil

# Load the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        "API key not found. Please ensure it is set in your environment variables."
    )


SOURCE_DIR = Path(str(Path.home()) + "/Documents/Python")
DEST_DIR = Path(str(Path.home()) + "/Documents/Categorized")


def get_openai_category(script_content):
    """get_openai_category function."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert Python programmer."},
                {
                    "role": "user",
                    "content": f"Based on the content of the script, suggest an appropriate category:\n\n{script_content}",
                },
            ],
            max_tokens=CONSTANT_150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.info(f"Error categorizing script: {e}")
        return "Uncategorized"


def sanitize_category(category, max_length=CONSTANT_100):
    """Sanitize and truncate the category name to be a valid directory name."""
    sanitized = re.sub(r"[^a-zA-Z0-9_\- ]", "", category)  # Remove invalid characters
    sanitized = sanitized.strip().replace(" ", "_")  # Replace spaces with underscores
    truncated = sanitized[:max_length]  # Truncate to max length

    # Ensure uniqueness by appending a hash if the name was truncated
    if len(sanitized) > max_length:
        hash_suffix = hashlib.md5(sanitized.encode()).hexdigest()[:8]
        truncated += "_" + hash_suffix

    return truncated.lower()

    """create_directory function."""


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

    """save_to_category function."""


def save_to_category(file_path, category, dest_dir):
    category_dir = os.path.join(dest_dir, category)
    create_directory(category_dir)
    dest_file_path = os.path.join(category_dir, os.path.basename(file_path))
    shutil.move(file_path, dest_file_path)
    logger.info(f"Moved {file_path} to {category_dir}")
    """categorize_files function."""


def categorize_files(source_dir, dest_dir):
    for root, _, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension == ".py":
                with open(file_path, "r") as f:
                    content = f.read()
                category = get_openai_category(content)
                sanitized_category = sanitize_category(category)
                save_to_category(file_path, sanitized_category, dest_dir)
            else:
                # For non-Python files, categorize them as 'miscellaneous'
                save_to_category(file_path, "miscellaneous", dest_dir)


if __name__ == "__main__":
    source_dir = Path(
        str(Path.home()) + "/Documents/Python"
    )  # Update with your scripts directory
    dest_dir = Path(str(Path.home()) + "/Documents/Categorized")
    categorize_files(source_dir, dest_dir)
