"""
Upscale

This module provides functionality for upscale.

Author: Auto-generated
Date: 2025-11-01
"""

import os

from PIL import Image
from tqdm import tqdm

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300



# Function to upscale an image by 2x and set resolution to CONSTANT_300 DPI
def upscale_image(input_path, output_path):
    """
    Upscale an image by 2x and set resolution to CONSTANT_300 DPI.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the upscaled image.

    Returns:
        None
    """
    image = Image.open(input_path)
    upscaled_image = image.resize((image.width * 2, image.height * 2), Image.BICUBIC)
    upscaled_image = upscaled_image.convert("RGB")  # Ensure the image is in RGB mode
    upscaled_image.save(output_path, dpi=(CONSTANT_300, CONSTANT_300))  # Set resolution to CONSTANT_300 DPI


# Ask for input and output directories
input_dir = input("Enter the path to the input directory: ")
output_dir = input("Enter the path to the output directory: ")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# List all files in the input directory
input_files = os.listdir(input_dir)

# Define a list of ANSI color codes (you can customize this list)
color_codes = ["\x1b[31m", "\x1b[32m", "\x1b[33m", "\x1b[34m", "\x1b[35m"]

# Initialize tqdm with the total number of files for the progress bar
with tqdm(total=len(input_files)) as pbar:
    # Iterate through input files and upscale them
    for index, input_file in enumerate(input_files):
        if input_file.endswith((".jpg", ".jpeg", ".png")):
            input_path = os.path.join(input_dir, input_file)
            output_path = os.path.join(output_dir, input_file)
            upscale_image(input_path, output_path)

            # Get the color code for this file (cycling through the list)
            color_code = color_codes[index % len(color_codes)]

            # Update the progress bar with the file's color code
            pbar.set_description(color_code + f"Processing: {input_file}" + "\x1b[0m")
            pbar.update(1)  # Update the progress bar

logger.info("Images upscaled by 2x and set to CONSTANT_300 DPI successfully.")
