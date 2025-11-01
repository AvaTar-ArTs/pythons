"""
File Apps

This module provides functionality for file apps.

Author: Auto-generated
Date: 2025-11-01
"""

import os

from PIL import Image

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300


# Your messy, no-folder, unstructured digital wasteland
input_dir = "'/Users/steven/Pictures/etsy/PanoramicIndexJuice"

# Supported input formats because variety is the spice of life
input_formats = (".webp", ".tiff", ".tif")

# Go through all files, because why not?
for filename in os.listdir(input_dir):
    if filename.lower().endswith(input_formats):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.splitext(input_path)[0] + ".jpg"  # Keep same name, just betray the format

        # Open and mercilessly convert
        with Image.open(input_path) as img:
            rgb_img = img.convert("RGB")  # Because JPG hates transparency, much like your ex hates closure
            rgb_img.save(output_path, "JPEG", dpi=(CONSTANT_300, CONSTANT_300), quality=95)

        # Uncomment the line below to **obliterate** the original files, just for fun
        # os.remove(input_path)

        logger.info(f"Boom! {filename} → {output_path} (Enjoy your brand-new JPG!)")

logger.info("Congratulations, your files have been forcefully transformed. No take-backs.")
