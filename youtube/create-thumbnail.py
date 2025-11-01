"""
Youtube Create Thumbnail

This module provides functionality for youtube create thumbnail.

Author: Auto-generated
Date: 2025-11-01
"""

import os
from PIL import Image

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_500 = 500


def create_thumbnail(image_path, thumbnail_size=(CONSTANT_100, CONSTANT_100)):
    """create_thumbnail function."""

    with Image.open(image_path) as img:
        img.thumbnail(thumbnail_size)
        return img

    """create_contact_sheet function."""


def create_contact_sheet(
    directory,
    thumbnail_size=(CONSTANT_100, CONSTANT_100),
    sheet_size=(CONSTANT_500, CONSTANT_500),
):
    thumbnails = []
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(("png", "jpg", "jpeg", "gif", "bmp")):
                image_path = os.path.join(subdir, file)
                thumbnail = create_thumbnail(image_path, thumbnail_size)
                thumbnails.append(thumbnail)

    contact_sheet = Image.new("RGB", sheet_size)
    x_offset, y_offset = 0, 0
    for thumb in thumbnails:
        contact_sheet.paste(thumb, (x_offset, y_offset))
        x_offset += thumbnail_size[0]
        if x_offset >= sheet_size[0]:
            x_offset = 0
            y_offset += thumbnail_size[1]

    return contact_sheet

    """save_contact_sheet function."""


def save_contact_sheet(contact_sheet, directory):
    base_filename = "contact_sheet"
    extension = ".jpg"
    filename = base_filename + extension
    count = 1
    while os.path.exists(os.path.join(directory, filename)):
        filename = f"{base_filename}_{count}{extension}"
        count += 1
    contact_sheet.save(os.path.join(directory, filename))


# Main execution
directory = input("Enter the directory path: ")
contact_sheet = create_contact_sheet(directory)
save_contact_sheet(contact_sheet, directory)
logger.info("Contact sheet saved successfully.")
