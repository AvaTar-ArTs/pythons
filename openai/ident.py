"""
Ai Tools Gpt Ident 1

This module provides functionality for ai tools gpt ident 1.

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
import csv

from dotenv import load_dotenv

# Load environment variables from the specified .env file
load_dotenv(Path("/Users/steven/Documents/python/.env"))

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
        titles = []

        # Process each line of the response text to extract titles
        for i, line in enumerate(response_text.split(Path("\n"))):
            line = line.strip()
            if line and "Script" in line:  # Look for lines that contain "Script"
                # Extract the part after the script number
                title = line.split(":", 1)[-1].strip().strip('"')
                titles.append(title if title else f"Script {i+1}: Untitled")
            else:
                titles.append(f"Script {i+1}: Untitled")

        # Ensure the list matches the number of script contents provided
        if len(titles) < len(script_contents):
            titles.extend(
                [
                    f"Script {i+1}: Untitled"
                    for i in range(len(titles), len(script_contents))
                ]
            )

        return titles
    except Exception as e:
        logger.info(f"Error during batch processing: {e}")
        return [f"Script {i+1}: Untitled" for i in range(len(script_contents))]


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


def process_directory_with_batching(
    directory_path, batch_size=10, output_csv="output.csv"
):
    """
    Process a directory of Python scripts, suggesting titles for each script in batches.

    Args:
        directory_path (str): The path of the directory containing Python scripts.
        batch_size (int): Number of scripts to process in each batch.
        output_csv (str): The path of the output CSV file.

    Returns:
        None
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
        return

    # Process the files in batches and get the results
    results = suggest_script_titles_batch(file_paths, batch_size=batch_size)

    # Write the results to a CSV file
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["File Name", "Suggested Title", "Path"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)

    logger.info(f"Results have been written to {output_csv}")


# Example usage
if __name__ == "__main__":
    directory_path = Path("/Users/steven/Documents/python")  # Your target directory
    batch_size = 10  # Number of scripts to process at a time
    output_csv = Path(
        "/Users/steven/Documents/python/output.csv"
    )  # Output CSV file path

    # Process the directory and output the results to a CSV file
    process_directory_with_batching(
        directory_path, batch_size=batch_size, output_csv=output_csv
    )
