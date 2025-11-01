"""
1500 Cutout Orn Process

This module provides functionality for 1500 cutout orn process.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os

import cv2
import numpy as np

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_255 = 255


def apply_circular_mask(image_path, output_path):
    """
    Applies a circular mask to the input image and saves it with transparency.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path to save the masked image.
    """
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # If the image is not loaded correctly, skip it
    if image is None:
        logger.info(f"Failed to load image: {image_path}")
        return

    # Create a blank mask with the same size and 4 channels (for transparency)
    mask = np.zeros(image.shape, dtype=np.uint8)

    # Define the center and radius for the circular mask
    height, width = image.shape[:2]
    center = (width // 2, height // 2)  # Assuming the circle is centered
    radius = min(center[0], center[1])  # Radius to fit the circle inside the image

    # Draw a white circle on the mask
    cv2.circle(mask, center, radius, (CONSTANT_255, CONSTANT_255, CONSTANT_255, CONSTANT_255), -1)

    # Apply the mask to the image
    masked_image = cv2.bitwise_and(image, mask)

    # Save the masked image with alpha channel (transparency)
    cv2.imwrite(output_path, masked_image)
    logger.info(f"Saved masked image to {output_path}")


def process_images_in_directory(input_directory, output_directory):
    """
    Processes all images in a directory, applying a circular mask to each image.

    Args:
        input_directory (str): Directory containing images to process.
        output_directory (str): Directory to save the masked images.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Loop through all files in the input directory
    for filename in os.listdir(input_directory):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, filename)

            # Apply the circular mask to the image and save it
            apply_circular_mask(input_path, output_path)
        else:
            logger.info(f"Skipping non-image file: {filename}")


# Example usage
input_directory = Path("/Users/steven/Pictures/orn/Dream/all_images")
output_directory = Path("/Users/steven/Pictures/orn/Dream/all_images/masked_output")

process_images_in_directory(input_directory, output_directory)
