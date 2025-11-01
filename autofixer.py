"""
Autofixer

This module provides functionality for autofixer.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import shutil
import subprocess
from datetime import datetime
import csv

import logging

logger = logging.getLogger(__name__)


def create_backup(file_path, backup_dir):
    """
    Create a backup of the given file in the specified backup directory.

    :param file_path: Path to the original file.
    :param backup_dir: Path to the backup directory.
    :return: None
    """
    os.makedirs(backup_dir, exist_ok=True)
    file_name = os.path.basename(file_path)
    backup_path = os.path.join(backup_dir, file_name)
    shutil.copy(file_path, backup_path)
    logger.info(f"Backup created for {file_path} at {backup_path}")


def apply_autopep8(file_path):
    """
    Apply autopep8 to the given Python file to fix formatting issues.

    :param file_path: Path to the Python file.
    :return: None
    """
    result = subprocess.run(
        ["autopep8", "--in-place", "--aggressive", "--aggressive", file_path]
    )
    if result.returncode == 0:
        logger.info(f"Formatted {file_path} with autopep8")
        return "Formatted with autopep8"
    else:
        logger.info(f"Failed to format {file_path} with autopep8")
        return "Failed to format with autopep8"


def run_pylint(file_path):
    """
    Run pylint on the given Python file to check for issues.

    :param file_path: Path to the Python file.
    :return: None
    """
    result = subprocess.run(["pylint", file_path], capture_output=True, text=True)
    if result.returncode != 0:
        logger.info(f"Issues found in {file_path}:")
        logger.info(result.stdout)
        return result.stdout.strip()
    else:
        logger.info(f"No issues found in {file_path}")
        return "No issues found"


def process_directory(input_dir, backup_base_dir, output_file):
    """
    Recursively process all Python files in the input directory, create backups,
    apply autopep8 and run pylint, and write the results to a CSV or TXT file.

    :param input_dir: Path to the input directory.
    :param backup_base_dir: Path to the base backup directory.
    :param output_file: Path to the output CSV or TXT file.
    :return: None
    """
    results = []
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if filename.lower().endswith(".py"):
                file_path = os.path.join(root, filename)

                # Create backup
                relative_path = os.path.relpath(root, input_dir)
                backup_dir = os.path.join(backup_base_dir, relative_path)
                create_backup(file_path, backup_dir)

                # Apply autopep8
                autopep8_result = apply_autopep8(file_path)

                # Run pylint
                pylint_result = run_pylint(file_path)

                # Append results
                results.append([file_path, autopep8_result, pylint_result])

    # Write results to CSV or TXT file
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["File Path", "autopep8 Result", "pylint Result"])
        writer.writerows(results)


if __name__ == "__main__":
    # Define the base input directory
    # Update to your actual input directory
    input_dir = Path(str(Path.home()) + "/Documents/Python")

    # Define the base backup directory with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Update to your preferred backup location
    backup_base_dir = fstr(Path.home()) + "/Documents/Python_backup_{timestamp}"

    # Define the output file path
    # Change to .txt if needed
    output_file = Path(str(Path.home()) + "/Documents/formatting_report.csv")

    # Process the directory and fix Python files
    process_directory(input_dir, backup_base_dir, output_file)
