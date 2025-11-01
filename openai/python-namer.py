"""
Gpt Python Namer

This module provides functionality for gpt python namer.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os

from openai import OpenAI

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_1000 = 1000


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from the environment variable


def get_openai_batch_titles(script_contents):
    """
    Prepare a batch request to OpenAI for suggesting appropriate titles for scripts.

    Args:
        script_contents (list): List of script contents as strings.

    Returns:
        list: List of suggested titles for each script.
    """
    # Check if the API key is loaded properly
    if not openai.api_key:
        raise ValueError(
            "OpenAI API key is missing. Make sure it's set in the .env file."
        )

    # Prepare messages for the batch request
    messages = [
        {
            "role": "system",
            "content": "You are an expert Python programmer. Suggest appropriate titles for the following scripts.",
        },
        {
            "role": "user",
            "content": Path("\n\n").join(
                f"Script {i+1}:\n{content[:CONSTANT_1000]}"
                for i, content in enumerate(script_contents)
            ),
        },
    ]

    try:
        # Make the batch request to OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages, max_tokens=CONSTANT_300
        )

        # Parse the response to extract the titles for each script
        response_text = response.choices[0].message.content.strip()
        titles = response_text.split(Path("\n"))
        return [title.strip() for title in titles if title.strip()]
    except Exception as e:
        logger.info(f"Error during batch processing: {e}")
        return ["Untitled"] * len(script_contents)


def suggest_script_titles_batch(file_paths, batch_size=10):
    """
    Suggest titles for scripts in batches to optimize the process.

    Args:
        file_paths (list): List of file paths to process.
        batch_size (int): Number of scripts to process in each batch.

    Returns:
        list: List of dictionaries with file names, suggested titles, and file paths.
    """
    results = []

    # Process the files in batches
    for i in range(0, len(file_paths), batch_size):
        batch_paths = file_paths[i : i + batch_size]
        batch_contents = []

        # Read the contents of each file in the batch
        for file_path in batch_paths:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                batch_contents.append(content)
            except FileNotFoundError:
                logger.info(f"File not found: {file_path}")
                batch_contents.append("")
            except Exception as e:
                logger.info(f"Error reading {file_path}: {e}")
                batch_contents.append("")

        # Get the suggested titles from the OpenAI API
        batch_titles = get_openai_batch_titles(batch_contents)

        # Store the results
        for file_path, title in zip(batch_paths, batch_titles):
            results.append(
                {
                    "File Name": os.path.basename(file_path),
                    "Suggested Title": title,
                    "Path": file_path,
                }
            )
            logger.info(f"Suggested title for {os.path.basename(file_path)}: {title}")

    return results


def process_directory_with_batching(directory_path, batch_size=10):
    """
    Process a directory of Python scripts, suggesting titles for each script in batches.

    Args:
        directory_path (str): The path of the directory containing Python scripts.
        batch_size (int): Number of scripts to process in each batch.

    Returns:
        list: List of dictionaries with suggested titles and file paths.
    """
    # Gather all Python files from the directory and subdirectories
    file_paths = [
        os.path.join(root, file)
        for root, _, files in os.walk(directory_path)
        for file in files
        if file.endswith(".py")
    ]

    # Ensure there are Python files to process
    if not file_paths:
        logger.info("No Python files found in the specified directory.")
        return []

    # Process the files in batches
    return suggest_script_titles_batch(file_paths, batch_size=batch_size)


# Example usage
if __name__ == "__main__":
    directory_path = Path(
        str(Path.home()) + "/Documents/python"
    )  # Update this to your target directory
    batch_size = 10  # Number of scripts to process at a time

    # Get the results
    results = process_directory_with_batching(directory_path, batch_size=batch_size)

    # Print the results
    for result in results:
        print(
            f"File: {result['File Name']}, Suggested Title: {result['Suggested Title']}, Path: {result['Path']}"
        )
