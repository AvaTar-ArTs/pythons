"""
Pdf2Img

This module provides functionality for pdf2img.

Author: Auto-generated
Date: 2025-11-01
"""

from pdf2image import convert_from_path
import os

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300


# Path to your PDF file
pdf_path = str(Path.home()) + "/Documents/tesla/1-ocr.pdf"

# Output directory for images
output_dir = str(Path.home()) + "/Documents/tesla/output_images"
os.makedirs(output_dir, exist_ok=True)

# Convert PDF to images
images = convert_from_path(pdf_path, dpi=CONSTANT_300)

# Save images to the output directory
for i, image in enumerate(images):
    image_path = os.path.join(output_dir, f"page_{i+1}.png")
    image.save(image_path, "PNG")
    logger.info(f"Saved {image_path}")
