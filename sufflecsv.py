"""
Sufflecsv

This module provides functionality for sufflecsv.

Author: Auto-generated
Date: 2025-11-01
"""

import csv
import random
from io import StringIO

import requests


def shuffle_csv(url):
    """shuffle_csv function."""

    # Download the CSV data from the URL
    response = requests.get(url)
    response.raise_for_status()  # Check for errors
    csv_data = response.text

    # Read the CSV data
    csv_file = StringIO(csv_data)
    reader = csv.reader(csv_file)
    data = list(reader)

    # Shuffle the data
    random.shuffle(data)

    # Prompt the user for the destination file path
    destination_file_path = input("Enter the path to save the shuffled CSV file: ")

    # Write the shuffled data to the specified file
    with open(destination_file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)


# Prompt the user for the CSV file URL
csv_url = input("Enter the URL of the CSV file: ")
shuffle_csv(csv_url)
