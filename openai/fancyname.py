"""
Ai Tools Gpt Fancyname 3

This module provides functionality for ai tools gpt fancyname 3.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import csv
import os
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI

import logging

logger = logging.getLogger(__name__)


# Load environment variables from the specified .env file
env_path = Path("/Users/steven/.env")
load_dotenv(dotenv_path=env_path)

# Initialize OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# Error checking for OpenAI API key
if not api_key:
    raise EnvironmentError("OpenAI API key not found. Please check your .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)


# Function to generate creative filenames using GPT
def generate_creative_filename(prompt):
    """generate_creative_filename function."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a witty and imaginative assistant. Generate playful, creative, and descriptive filenames "
                    "for digital products based on provided prompts."
                ),
            },
            {
                "role": "user",
                "content": f"Create a unique filename for this design prompt: '{prompt}'",
            },
        ],
        max_tokens=20,
        temperature=0.7,
    )
    filename = response.choices[0].message.content.strip()
    return filename.replace(" ", "_").replace("/", "_")  # Replace spaces and slashes

    # Function to process images and rename them
    """process_images function."""


def process_images(directory):
    # Generate output CSV filename with folder name and current date
    folder_name = os.path.basename(os.path.normpath(directory))
    current_date = datetime.now().strftime("%m-%d-%y")
    output_csv = os.path.join(directory, f"{folder_name}-{current_date}.csv")

    image_extensions = [".jpeg", ".jpg", ".png"]
    image_files = [
        f
        for f in os.listdir(directory)
        if os.path.splitext(f)[1].lower() in image_extensions
    ]

    with open(output_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Old File Path", "New File Path", "Prompt"])

        for image_file in image_files:
            image_path = os.path.join(directory, image_file)
            base_name, ext = os.path.splitext(image_file)

            # Use the base name of the image as the default prompt
            prompt = f"Generate a filename for an image based on '{base_name}' with a theme of Christmas and wood art."

            # Generate new filename
            new_filename = generate_creative_filename(prompt)
            new_file_path = os.path.join(directory, f"{new_filename}{ext}")

            # Rename the file
            os.rename(image_path, new_file_path)

            # Log the renaming to CSV
            writer.writerow([image_path, new_file_path, prompt])
            logger.info(f"Renamed: {image_path} -> {new_file_path}")

    logger.info(f"\nOutput CSV saved to: {output_csv}")

    """main function."""


# Main function to run the process
def main():
    logger.info("Welcome to the Creative Filename Generator!")
    directory = input("Enter the directory path containing your files: ").strip()

    if not os.path.exists(directory):
        logger.info("Error: The specified directory does not exist.")
        return

    logger.info("\nStarting the renaming process...")
    process_images(directory)
    logger.info("\nProcess completed!")


# Run the main function
if __name__ == "__main__":
    main()
