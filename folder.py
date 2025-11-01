"""
Img To Pdf Folder

This module provides functionality for img to pdf folder.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os

from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import logging

logger = logging.getLogger(__name__)


# Function to convert an image to PDF
def image_to_pdf(image_path, pdf_path):
    """image_to_pdf function."""

    c = canvas.Canvas(pdf_path, pagesize=letter)
    img = Image.open(image_path)
    width, height = img.size
    c.setPageSize((width, height))
    c.drawImage(image_path, 0, 0, width, height)
    c.showPage()
    c.save()

    # Function to traverse the directory and convert images to PDFs
    """convert_images_to_pdf function."""


def convert_images_to_pdf(root_dir):
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif")):
                image_path = os.path.join(root, file)
                pdf_path = os.path.splitext(image_path)[0] + ".pdf"
                image_to_pdf(image_path, pdf_path)
                logger.info(f"Converted {image_path} to {pdf_path}")


if __name__ == "__main__":
    source_directory = Path("/Users/steven/Pictures/Move")
    convert_images_to_pdf(source_directory)
