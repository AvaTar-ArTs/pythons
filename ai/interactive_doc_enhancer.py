"""
Interactive Doc Enhancer

This module provides functionality for interactive doc enhancer.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import subprocess

import openai

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1000 = 1000



# Prompt the user to input the OpenAI API key if it's not found in environment variables
def get_openai_api_key():
    """get_openai_api_key function."""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = input("Enter your OpenAI API key: ").strip()
    return api_key


# Prompt the user for directory paths if not provided
    """get_directory_path function."""

def get_directory_path(prompt_message, default_path):
    directory = input(f"{prompt_message} (default: {default_path}): ").strip()
    return directory if directory else default_path


    """get_pydocgen_paths function."""

# Prompt the user for pydocgen input and output paths
def get_pydocgen_paths():
    python_directory = get_directory_path(
        "Enter the directory where Python scripts are located",
        Path("/Users/steven/Documents/python"),
    )
    docs_directory = get_directory_path(
        "Enter the directory where documentation should be saved",
        Path("/Users/steven/Documents/python/docs"),
    )
    return python_directory, docs_directory


# Set OpenAI API key
openai.api_key = get_openai_api_key()

    """generate_docs function."""


# Step 1: Run pydocgen to generate documentation
def generate_docs():
    python_directory, docs_directory = get_pydocgen_paths()

    # Ensure the docs directory exists; if not, create it
    if not os.path.exists(docs_directory):
        os.makedirs(docs_directory)
        logger.info(f"Created missing directory: {docs_directory}")

    try:
        subprocess.run(
            ["pydocgen", "-i", python_directory, "-o", docs_directory], check=True
        )
        logger.info(f"Documentation generated in {docs_directory}")
    except subprocess.CalledProcessError as e:
        logger.info(f"Error running pydocgen: {e}")
    """enhance_docs function."""



# Step 2: Enhance the generated documentation with OpenAI
def enhance_docs():
    python_directory, docs_directory = get_pydocgen_paths()

    for filename in os.listdir(docs_directory):
        if filename.endswith(".md") or filename.endswith(".rst"):
            file_path = os.path.join(docs_directory, filename)
            enhanced_file_path = os.path.join(docs_directory, f"enhanced_{filename}")

            # Skip enhancement if the enhanced file already exists
            if os.path.exists(enhanced_file_path):
                logger.info(f"Enhanced file already exists: {enhanced_file_path}")
                continue

            with open(file_path, "r") as doc_file:
                content = doc_file.read()

                # Use OpenAI to enhance the documentation
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Enhance the following Python code documentation for better readability and detail:\n\n{content}",
                    max_tokens=CONSTANT_1000,
                )

                enhanced_content = response.choices[0].text.strip()

            # Write the enhanced documentation to a new file
            with open(enhanced_file_path, "w") as enhanced_doc_file:
                enhanced_doc_file.write(enhanced_content)

    """run_flake8 function."""

            logger.info(f"Enhanced documentation saved to: {enhanced_file_path}")


# Step 3: Run flake8 to check code quality and compliance with PEP 8 and PEP 257
def run_flake8():
    python_directory, docs_directory = get_pydocgen_paths()

    flake8_report_file = os.path.join(docs_directory, "flake8_report.txt")

    # Skip flake8 if the report already exists
    if os.path.exists(flake8_report_file):
        logger.info(f"flake8 report already exists: {flake8_report_file}")
        return

    try:
        result = subprocess.run(
            ["flake8", python_directory, "--max-line-length=88"],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            logger.info("All files passed flake8 checks.")
        else:
            logger.info("flake8 found issues:")
            with open(flake8_report_file, "w") as report_file:
                report_file.write(result.stdout)
            logger.info(f"flake8 issues saved to: {flake8_report_file}")
    except subprocess.CalledProcessError as e:
        logger.info(f"Error running flake8: {e}")


# Run the entire workflow
generate_docs()
enhance_docs()
run_flake8()
