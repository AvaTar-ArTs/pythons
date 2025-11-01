"""
Ai Tools Gpt Vision 2

This module provides functionality for ai tools gpt vision 2.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import csv

from openai import OpenAI

# Constants
CONSTANT_300 = 300


# Initialize the OpenAI client
client = OpenAI()


def generate_description(image_url):
    """generate_description function."""

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Can you create a detailed and descriptive image prompt for the image as if you were to recreate it?",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=CONSTANT_300,
    )
    return response.choices[0].content


# Specify the input and output file paths
input_file_path = "input.csv"
output_file_path = "output.csv"  # Change to 'output.txt' for a TXT file

# Read the input CSV, generate descriptions, and write to the output CSV or TXT
with open(input_file_path, mode="r") as infile, open(
    output_file_path, mode="w", newline=""
) as outfile:
    reader = csv.reader(infile)
    if output_file_path.endswith(".csv"):
        writer = csv.writer(outfile)
    else:
        writer = None  # For TXT file, we'll write directly without a CSV writer

    for row in reader:
        image_url = row[0]  # Adjust if the URL is in a different column
        description = generate_description(image_url)

        if writer:
            # For CSV, write each row with the original data and the new
            # description
            writer.writerow(row + [description])
        else:
            # For TXT, write the description directly, followed by a newline
            outfile.write(description + Path("\n"))
