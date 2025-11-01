"""
Pyorganize 2

This module provides functionality for pyorganize 2.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
from openai import OpenAI

import logging

logger = logging.getLogger(__name__)


client = OpenAI(api_key=api_key)
import os
import re

# Load the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        "API key not found. Please ensure it is set in your environment variables."
    )


def extract_functions_and_classes(content):
    """
    Extracts top-level functions and classes from the script content.
    """
    pattern = re.compile(r"^\s*(def|class)\s+\w+\s*\(.*?\):", re.MULTILINE)
    matches = pattern.findall(content)
    headers = pattern.findall(content)
    functions_and_classes = []
    for header, body in zip(headers, matches):
        functions_and_classes.append(header + body)
    return functions_and_classes


def get_script_description(content):
    """
    Gets the description of the script content using OpenAI API.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert Python programmer."},
            {
                "role": "user",
                "content": f"Analyze the following Python code and describe its functionality:\n\n{content}",
            },
        ],
    )

    # Extract and return the description from the response
    description = response.choices[0].message.content.strip()
    return description


def categorize_scripts(directory):
    """
    Analyzes and categorizes all Python scripts in the specified directory.
    """
    descriptions = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".py"):
                file_path = os.path.join(root, filename)
                with open(file_path, "r") as file:
                    script_content = file.read()

                # Get the description for the entire script
                description = get_script_description(script_content)
                descriptions[file_path] = description

    return descriptions


if __name__ == "__main__":
    # Update with your scripts directory
    scripts_directory = Path(str(Path.home()) + "/Documents/Python/")
    descriptions = categorize_scripts(scripts_directory)

    # Print out the categorized descriptions
    for script, description in descriptions.items():
        logger.info(f"Script: {script}\nDescription: {description}\n{'-'*60}\n")
