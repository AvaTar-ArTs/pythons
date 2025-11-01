"""
Pydescribe

This module provides functionality for pydescribe.

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
    matches = pattern.split(content)
    headers = pattern.findall(content)
    functions_and_classes = []
    for header, body in zip(headers, matches[1:]):
        functions_and_classes.append(header + body)
    return functions_and_classes


def save_to_text_files(directory, script_name, functions_and_classes):
    """
    Save each function or class to a separate text file in a common directory.
    """
    base_path = os.path.join(directory, "extracted_parts")
    os.makedirs(base_path, exist_ok=True)
    file_paths = []

    for i, item in enumerate(functions_and_classes):
        sanitized_script_name = script_name.replace("/", "_").replace(Path("\\"), "_")
        file_path = os.path.join(base_path, f"{sanitized_script_name}_part_{i}.txt")
        with open(file_path, "w") as file:
            file.write(item)
        file_paths.append(file_path)

    return file_paths


def get_description_from_file(file_path):
    """get_description_from_file function."""

    with open(file_path, "r") as file:
        content = file.read()

    # OpenAI API call to get the description
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

    """analyze_scripts function."""


def analyze_scripts(directory):
    descriptions = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".py"):
                file_path = os.path.join(root, filename)
                with open(file_path, "r") as file:
                    script_content = file.read()

                functions_and_classes = extract_functions_and_classes(script_content)
                text_files = save_to_text_files(
                    directory, os.path.splitext(filename)[0], functions_and_classes
                )

                # Get descriptions for each text file
                file_descriptions = [get_description_from_file(f) for f in text_files]
                combined_description = Path("\n").join(file_descriptions)

                descriptions[file_path] = combined_description

    return descriptions


if __name__ == "__main__":
    # Update with your scripts directory
    scripts_directory = Path("/Users/steven/Documents/Python/")
    descriptions = analyze_scripts(scripts_directory)

    # Print out the descriptions
    for script, description in descriptions.items():
        logger.info(f"Script: {script}\nDescription: {description}\n{'-'*60}\n")
