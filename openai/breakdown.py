"""
Ai Tools Gpt Breakdown 3

This module provides functionality for ai tools gpt breakdown 3.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
from openai import OpenAI

import logging

logger = logging.getLogger(__name__)


client = OpenAI(api_key=api_key)
import os

# Load the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        "API key not found. Please ensure it is set in your environment variables."
    )


def get_script_description(file_path):
    """get_script_description function."""

    with open(file_path, "r") as file:
        script_content = file.read()

    # OpenAI API call to get the script description
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert Python programmer."},
            {
                "role": "user",
                "content": f"Analyze the following Python script and describe its functionality:\n\n{script_content}",
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
                description = get_script_description(file_path)
                descriptions[file_path] = description
    return descriptions


if __name__ == "__main__":
    scripts_directory = Path(
        "/Users/steven/Documents/Python"
    )  # Update with your scripts directory
    descriptions = analyze_scripts(scripts_directory)

    # Print out the descriptions
    for script, description in descriptions.items():
        logger.info(f"Script: {script}\nDescription: {description}\n{'-'*60}\n")
