"""
Openai Image Generater

This module provides functionality for openai image generater.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os

from openai import OpenAI

import logging

logger = logging.getLogger(__name__)


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import csv

from dotenv import load_dotenv

# Load API key from .env file
load_dotenv(Path(str(Path.home()) + "/.env"))


# Function to generate a filename using GPT based on the prompt
def generate_filename_with_gpt(prompt):
    """generate_filename_with_gpt function."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that generates descriptive filenames.",
            },
            {
                "role": "user",
                "content": f"Generate a concise, descriptive filename for this design prompt: '{prompt}'",
            },
        ],
        max_tokens=20,
    )
    filename = response.choices[0].message.content.strip()
    return filename.replace(" ", "_")  # Replace spaces with underscores

    # Function to pair .jpeg and .txt files, generate filenames, and save to CSV
    """pair_and_rename_images function."""


def pair_and_rename_images(directory, output_csv):
    text_files = {}
    image_extensions = [".jpeg", ".jpg", ".png"]

    # Scan the directory for text and image files
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_id, ext = os.path.splitext(file)

            if ext == ".txt":
                text_files[file_id] = {"text_path": os.path.join(root, file)}
            elif ext in image_extensions:
                if file_id in text_files:
                    text_files[file_id]["image_path"] = os.path.join(root, file)
                else:
                    text_files[file_id] = {"image_path": os.path.join(root, file)}

    # Write results to CSV
    with open(output_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Original Image Path", "New Filename", "Prompt"])

        for file_id, paths in text_files.items():
            if "text_path" in paths and "image_path" in paths:
                text_path = paths["text_path"]
                image_path = paths["image_path"]

                # Read the prompt from the .txt file
                with open(text_path, "r") as f:
                    prompt = f.read().strip()

                # Generate new filename using GPT
                new_filename = generate_filename_with_gpt(prompt)

                # Form the new filename with extension from the original image
                new_image_filename = f"{new_filename}{os.path.splitext(image_path)[1]}"

                # Log to CSV
                writer.writerow([image_path, new_image_filename, prompt])
                logger.info(f"Paired: {image_path} -> {new_image_filename}")

            else:
                logger.info(f"Warning: Missing image or text file for {file_id}")


# Example usage
directory = str(Path.home()) + "/Music/TraShCaTs/witches Road/Witches_Road_Covers"
output_csv = (
    str(Path.home()) + "/Music/TraShCaTs/witches Road/Witches_Road_Covers/paired_output.csv"
)
pair_and_rename_images(directory, output_csv)
