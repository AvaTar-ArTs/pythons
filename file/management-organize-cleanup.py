"""
File Management Organize Cleanup 14

This module provides functionality for file management organize cleanup 14.

Author: Auto-generated
Date: 2025-11-01
"""

import csv
import os
import re
from datetime import datetime

import pandas as pd

import logging

logger = logging.getLogger(__name__)


def is_excluded(path, patterns):
    """
    Check if a given path matches any of the exclusion patterns.

    Parameters:
    path (str): The path to check.
    patterns (list): A list of regex patterns for exclusion.

    Returns:
    bool: True if path matches any pattern, False otherwise.
    """
    for pattern in patterns:
        if re.search(pattern, path):
            return True
    return False


def prompt_for_csv_file():
    """
    Prompt user for a CSV file path.

    Returns:
    str: The CSV file path provided by the user.
    """
    while True:
        csv_input = input("Enter the path to the duplicate report CSV file (or 'N' to finish): ").strip()
        if csv_input.lower() == "n":
            logger.info("No CSV file provided. Exiting.")
            return None
        if os.path.isfile(csv_input):
            logger.info(f"Added: {csv_input}")
            return csv_input
        else:
            logger.info(f"Invalid file path: {csv_input}. Please enter a valid CSV file path.")


def prompt_for_output_directory():
    """
    Prompt user for the output directory.

    Returns:
    str: The output directory provided by the user.
    """
    while True:
        dir_output = input("Enter the path to save the output CSV file: ").strip()
        if os.path.isdir(dir_output):
            logger.info(f"Output CSV will be saved in: {dir_output}")
            return dir_output
        else:
            logger.info(f"Invalid directory path: {dir_output}. Please enter a valid directory path.")


def prompt_for_action():
    """
    Prompt user for the action: dry run or cleanup.

    Returns:
    bool: True if cleanup is chosen, False if dry run is chosen.
    """
    while True:
        action = input("Choose action - Dry run (D) or Cleanup (C): ").strip().lower()
        if action == "d":
            return False
        elif action == "c":
            return True
        else:
            logger.info("Invalid input. Please enter 'D' for Dry run or 'C' for Cleanup.")


def remove_duplicates(duplicate_report_path, output_csv_path, delete_files=False):
    """
    Identify and handle duplicate files based on the detailed duplicate report.

    Parameters:
    duplicate_report_path (str): Path to the detailed duplicate report CSV.
    output_csv_path (str): Path to save the CSV with duplicate file paths.
    delete_files (bool): Whether to delete duplicate files, keeping one instance.

    Returns:
    None
    """
    # Load the detailed duplicate report CSV file
    duplicate_report = pd.read_csv(duplicate_report_path)

    # Determine the correct column name for the duplicate count
    possible_count_columns = ["Duplicate Count", "Count", "Duplicates"]
    count_column = next((col for col in possible_count_columns if col in duplicate_report.columns), None)

    if count_column is None:
        logger.info("No suitable column found for duplicate count.")
        return

    # Filter to show only duplicates (where Duplicate Count > 1)
    duplicates = duplicate_report[duplicate_report[count_column] > 1]

    # Group by MD5 Hash and get file paths for duplicates
    duplicate_groups = duplicates.groupby("MD5 Hash")["File Path"].apply(list).reset_index()

    # Create a list to store paths of files to be deleted
    files_to_delete = []

    # Iterate over duplicate groups to determine which files to keep/delete
    for _, row in duplicate_groups.iterrows():
        file_paths = row["File Path"]
        # Keep the first file, mark the rest for deletion
        files_to_delete.extend(file_paths[1:])

    # Log the duplicate file paths to another CSV
    with open(output_csv_path, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["File Path"])
        for file_path in files_to_delete:
            csv_writer.writerow([file_path])

    # Optionally delete the duplicate files
    if delete_files:
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                logger.info(f"Deleted: {file_path}")
            except Exception as e:
                logger.info(f"Error deleting {file_path}: {e}")

    logger.info(f"CSV of duplicates created at {output_csv_path}")


# Prompt user for the action: dry run or cleanup
delete_files = prompt_for_action()

# Prompt user for the duplicate report CSV file
duplicate_report_path = prompt_for_csv_file()

# Check if a valid file was provided before proceeding
if duplicate_report_path:
    # Prompt user for the output directory
    output_dir = prompt_for_output_directory()

    # Generate a timestamped filename for the output CSV
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_csv_path = os.path.join(output_dir, f"duplicates_to_delete_{timestamp}.csv")

    remove_duplicates(duplicate_report_path, output_csv_path, delete_files=delete_files)
else:
    logger.info("No valid CSV file provided. Exiting.")
