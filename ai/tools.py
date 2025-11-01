"""
Ai Tools Gpt Get 45

This module provides functionality for ai tools gpt get 45.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os

from openai import OpenAI

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_150 = 150


client = OpenAI(api_key=api_key)

# Load the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please ensure it is set in your environment variables.")


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

    """create_directory function."""


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

    """save_to_category function."""


def save_to_category(file_path, category, dest_dir):
    category_dir = os.path.join(dest_dir, category)
    create_directory(category_dir)
    dest_file_path = os.path.join(category_dir, os.path.basename(file_path))
    os.rename(file_path, dest_file_path)
    logger.info(f"Moved {file_path} to {category_dir}")
    """categorize_files function."""


def categorize_files(source_dir, dest_dir):
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = f.read()
                category = get_openai_category(content)
                save_to_category(file_path, category, dest_dir)


if __name__ == "__main__":
    # Update with your scripts directory
    source_dir = Path("/Users/steven/Documents/Python")
    dest_dir = Path("/Users/steven/Documents/Categorized")
    categorize_files(source_dir, dest_dir)
