from pathlib import Path
import ast
import os

from openai import OpenAI

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import csv
from datetime import datetime

from dotenv import load_dotenv

# Load environment variables from .env
env_path = Path(str(Path.home()) + "/.env")
load_dotenv(dotenv_path=env_path)

# Initialize OpenAI API key

# Error checking for OpenAI API key
if not openai.api_key:
    raise EnvironmentError("OpenAI API key not found. Please check your .env file.")


# Function to send batch content to OpenAI for better classification and generating category names
def generate_category_with_openai(content):
    """generate_category_with_openai function."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Updated to use ChatCompletion
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Python script categorizer.",
                },
                {
                    "role": "user",
                    "content": f"Classify the following Python script and generate a category name:\n{content}\n",
                },
            ],
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0,
        )
        category = response.choices[0].message.content.strip()
        return category
    except Exception as e:
        logger.info(f"Error with OpenAI API: {e}")
        return "Unknown Category"


def classify_script(filepath, file_size):
    """Classify a Python script by generating automatic category names based on file heuristics and OpenAI's API."""
    try:
        with open(filepath, "r") as file:
            content = file.read()
    except Exception as e:
        logger.info(f"Error reading file {filepath}: {e}")
        return "Unknown Category"

    # Metadata classification based on file size
    if file_size < 1 * CONSTANT_1024:  # Files smaller than 1KB
        return "Small Utility Script"
    elif (
        1 * CONSTANT_1024 <= file_size <= 10 * CONSTANT_1024
    ):  # Files between 1KB and 10KB
        return "Medium-Sized Script"

    # If the file size is large, check for selective keywords and imports
    imports = []
    try:
        tree = ast.parse(content, filename=filepath)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append(alias.name)
    except SyntaxError:
        return "Syntax Error Script"

    # Generate descriptive category names based on detected imports
    if "requests" in imports or "openai" in imports:
        return "API Interaction Script"
    elif "pandas" in imports or "numpy" in imports:
        return "Data Processing Script"
    elif "flask" in imports or "django" in imports:
        return "Web Application Script"
    elif "matplotlib" in imports or "seaborn" in imports:
        return "Data Visualization Script"

    # If no specific import matches, use OpenAI for generating the category
    if file_size > 10 * CONSTANT_1024:  # Larger files trigger OpenAI classification
        openai_category = generate_category_with_openai(content)
        return openai_category

    return "General Script"


def scan_directory(directory):
    """Scan a directory, classify files, and output the results."""
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory {directory} not found.")
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"{directory} is not a valid directory.")

    results = []
    errors = []
    file_count = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(filepath)
                    category = classify_script(filepath, file_size)
                    results.append((file, category))
                    file_count += 1
                except Exception as e:
                    errors.append(f"Error processing file {file}: {e}")

    return results, errors, file_count


def save_classification_to_csv(results, output_file):
    """Save classification results to a CSV file."""
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Filename", "Category"])
        writer.writerows(results)


if __name__ == "__main__":
    # Prompt the user for the directory
    directory = input("Enter the directory path to scan for Python scripts: ")

    try:
        # Log start time
        start_time = datetime.now()
        logger.info(f"Classification started at {start_time}")

        # Scan the directory and classify the scripts
        classification_results, errors, file_count = scan_directory(directory)

        # Define the output CSV file path (in the same directory)
        output_file = os.path.join(
            directory, "script_classifications_with_auto_categories.csv"
        )

        # Save the classification results to the CSV file
        save_classification_to_csv(classification_results, output_file)

        # Log end time
        end_time = datetime.now()
        duration = end_time - start_time

        # Summary details
        logger.info(f"\nClassification completed at {end_time}")
        logger.info(f"Total files processed: {file_count}")
        logger.info(f"Time taken: {duration}")
        logger.info(f"CSV saved to: {output_file}")

        # Display errors if any
        if errors:
            logger.info("\nErrors encountered during classification:")
            for error in errors:
                logger.info(error)
        else:
            logger.info("\nNo errors encountered during classification.")

    except Exception as e:
        logger.info(f"An error occurred: {e}")
