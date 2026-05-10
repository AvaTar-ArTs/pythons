import csv
import os
import re

import pandas as pd


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
        csv_input = input(
            "Enter the path to the duplicate report CSV file (or 'N' to finish): "
        ).strip()
        if csv_input.lower() == "n":
            print("No CSV file provided. Exiting.")
            return None
        if os.path.isfile(csv_input):
            print(f"Added: {csv_input}")
            return csv_input
        else:
            print(
                f"Invalid file path: {csv_input}. Please enter a valid CSV file path."
            )


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
            print("Invalid input. Please enter 'D' for Dry run or 'C' for Cleanup.")


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

    # Filter to show only duplicates (where Duplicate Count > 1)
    duplicates = duplicate_report[duplicate_report["Duplicate Count"] > 1]

    # Group by MD5 Hash and get file paths for duplicates
    duplicate_groups = (
        duplicates.groupby("MD5 Hash")["File Path"].apply(list).reset_index()
    )

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
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

    print(f"CSV of duplicates created at {output_csv_path}")


# Prompt user for the duplicate report CSV file
duplicate_report_path = prompt_for_csv_file()

# Check if a valid file was provided before proceeding
if duplicate_report_path:
    # Prompt user for the action: dry run or cleanup
    delete_files = prompt_for_action()
    output_csv_path = (
        "duplicates_to_delete.csv"  # Path to save the CSV with duplicate file paths
    )
    remove_duplicates(duplicate_report_path, output_csv_path, delete_files=delete_files)
else:
    print("No valid CSV file provided. Exiting.")
