"""
Utilities File Operations Check 7

This module provides functionality for utilities file operations check 7.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import subprocess

import logging

logger = logging.getLogger(__name__)


def check_with_pylint(file_path, log_file):
    """
    Run pylint on the given Python file to check for errors and style issues.

    :param file_path: Path to the Python file.
    :param log_file: File object to log the errors.
    :return: None
    """
    result = subprocess.run(["pylint", file_path], capture_output=True, text=True)
    if result.returncode != 0:
        log_file.write(f"Pylint issues in {file_path}:\n")
        log_file.write(result.stdout + Path("\n"))
        logger.info(f"Pylint issues in {file_path}:\n{result.stdout}")
    else:
        log_file.write(f"No pylint issues found in {file_path}\n")
        logger.info(f"No pylint issues found in {file_path}")


def check_with_flake8(file_path, log_file):
    """
    Run flake8 on the given Python file to check for style issues.

    :param file_path: Path to the Python file.
    :param log_file: File object to log the errors.
    :return: None
    """
    result = subprocess.run(["flake8", file_path], capture_output=True, text=True)
    if result.returncode != 0:
        log_file.write(f"Flake8 issues in {file_path}:\n")
        log_file.write(result.stdout + Path("\n"))
        logger.info(f"Flake8 issues in {file_path}:\n{result.stdout}")
    else:
        log_file.write(f"No flake8 issues found in {file_path}\n")
        logger.info(f"No flake8 issues found in {file_path}")


def process_directory(input_dir, log_file_path):
    """
    Recursively process all Python files in the input directory and check for errors.

    :param input_dir: Path to the input directory.
    :param log_file_path: Path to the log file.
    :return: None
    """
    with open(log_file_path, "w") as log_file:
        for root, _, files in os.walk(input_dir):
            for filename in files:
                if filename.lower().endswith(".py"):
                    file_path = os.path.join(root, filename)
                    check_with_pylint(file_path, log_file)
                    check_with_flake8(file_path, log_file)


if __name__ == "__main__":
    # Define the base input directory and log file path
    # Update to your actual input directory
    input_dir = Path("/Users/steven/Documents/Python")
    # Path to save the error log
    log_file_path = Path("/Users/steven/Documents/Python/error_log.txt")

    # Process the directory and check Python files for errors
    process_directory(input_dir, log_file_path)
