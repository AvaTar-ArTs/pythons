"""
Resize Img

This module provides functionality for resize img.

Author: Auto-generated
Date: 2025-11-01
"""

import csv
import os
import re
import time
from datetime import datetime

from PIL import Image, UnidentifiedImageError
from tqdm import tqdm

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_1024 = 1024
CONSTANT_4550 = 4550
CONSTANT_5400 = 5400


# 🌟 Constants
MAX_WIDTH, MAX_HEIGHT = CONSTANT_4550, CONSTANT_5400
TARGET_DPI = CONSTANT_300
UPSCALE_MULTIPLIER = 2
BATCH_SIZE = 50
PAUSE_DURATION = 3
SIZE_THRESHOLD_MB = 9
TARGET_MAX_FILE_SIZE_MB = 10
LAST_DIRECTORY_FILE = "image_data.txt"

# 📊 Common Aspect Ratios
ASPECT_RATIOS = {
    "16:9": (16, 9),
    "9:16": (9, 16),
    "1:1": (1, 1),
    "2:3": (2, 3),
}

# 📜 Log Data
log_data = []


# 🎯 Get closest aspect ratio
def get_closest_aspect_ratio(width, height):
    """get_closest_aspect_ratio function."""

    current_ratio = width / height
    closest_ratio = min(
        ASPECT_RATIOS,
        key=lambda ar: abs(
            current_ratio - (ASPECT_RATIOS[ar][0] / ASPECT_RATIOS[ar][1])
        ),
    )
    return closest_ratio, ASPECT_RATIOS[closest_ratio]


# 🕒 Get file creation date
    """get_creation_date function."""

def get_creation_date(filepath):
    try:
        return datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%m-%d-%y")
    except Exception as e:
        logger.info(f"Error getting creation date for {filepath}: {e}")
        return "Unknown"


    """optimize_file_size function."""

# 📉 Reduce file size to fit 9MB-10MB range
def optimize_file_size(im, output_path):
    quality = 95
    while quality > 10:
        im.save(output_path, dpi=(TARGET_DPI, TARGET_DPI), quality=quality)
        file_size_mb = os.path.getsize(output_path) / (CONSTANT_1024**2)
        if SIZE_THRESHOLD_MB <= file_size_mb <= TARGET_MAX_FILE_SIZE_MB:
            return True
        quality -= 5
    return False

    """upscale_image function."""


# 🔺 Upscale smaller images
def upscale_image(im, output_path):
    new_width, new_height = (
        im.width * UPSCALE_MULTIPLIER,
        im.height * UPSCALE_MULTIPLIER,
    )
    im = im.resize((new_width, new_height), Image.LANCZOS)
    im.save(output_path, dpi=(TARGET_DPI, TARGET_DPI), quality=95)
    """get_image_metadata function."""



# 📜 Extract metadata from an image file
def get_image_metadata(filepath):
    try:
        with Image.open(filepath) as img:
            width, height = img.size
            dpi = img.info.get("dpi", (None, None))
            dpi_x = dpi[0] if dpi and len(dpi) > 0 else None
            dpi_y = dpi[1] if dpi and len(dpi) > 1 else None
            file_size = os.path.getsize(filepath)
            return width, height, dpi_x, dpi_y, file_size
    except Exception as e:
        logger.info(f"Error getting image metadata for {filepath}: {e}")
    """process_image function."""

        return None, None, None, None, None


# 🖼️ Process images
def process_image(file_path):
    file_ext = file_path.lower().split(".")[-1]
    entry = {
        "File": os.path.basename(file_path),
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    if file_ext not in ("jpg", "jpeg", "png", "webp", "tiff"):
        entry["Status"] = "Skipped - Unsupported Format"
        log_data.append(entry)
        return

    try:
        im = Image.open(file_path)
        width, height = im.size
        file_size_mb = os.path.getsize(file_path) / (CONSTANT_1024**2)
        creation_date = get_creation_date(file_path)

        entry["Original Size (MB)"] = round(file_size_mb, 2)
        entry["Creation Date"] = creation_date
        entry["Original Dimensions"] = f"{width}x{height}"

        if file_size_mb >= SIZE_THRESHOLD_MB:
            optimize_file_size(im, file_path)
        else:
            upscale_image(im, file_path)

        entry["New Size (MB)"] = round(os.path.getsize(file_path) / (CONSTANT_1024**2), 2)
        entry["Status"] = "Processed ✅"

    except UnidentifiedImageError:
        entry["Status"] = "Error - Unidentified Image"
    except Exception as e:
        entry["Status"] = f"Error - {str(e)}"
    """process_images function."""


    log_data.append(entry)


# 📦 Process all images in a directory
def process_images(source_directory):
    batch = []
    for root, _, files in os.walk(source_directory):
        for file in files:
            batch.append(os.path.join(root, file))
            if len(batch) >= BATCH_SIZE:
                for img_file in tqdm(batch, desc="✨ Processing batch"):
                    process_image(img_file)
                batch = []
                time.sleep(PAUSE_DURATION)

    """save_log function."""

        if batch:
            for img_file in tqdm(batch, desc="✨ Final batch"):
                process_image(img_file)


# 📜 Save log to CSV
def save_log(source_directory):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    output_file = os.path.join(
        source_directory, f"image_processing_log_{timestamp}.csv"
    )

    fieldnames = [
        "File",
        "Timestamp",
        "Creation Date",
        "Original Size (MB)",
        "New Size (MB)",
        "Status",
    ]
    with open(output_file, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    """save_last_directory function."""

        writer.writeheader()
        writer.writerows(log_data)

    logger.info(f"📄 Log saved to: {output_file}")
    """load_last_directory function."""



# 🏆 Remember last used directory
def save_last_directory(directory):
    with open(LAST_DIRECTORY_FILE, "w") as file:
        file.write(directory)

    """main function."""


def load_last_directory():
    if os.path.exists(LAST_DIRECTORY_FILE):
        with open(LAST_DIRECTORY_FILE, "r") as file:
            return file.read().strip()
    return None


# 🚀 Main Function
def main():
    logger.info("🔥 Welcome to the AI-Powered Image Processor 🔥")

    last_directory = load_last_directory()
    if last_directory:
        source_directory = last_directory
    else:
        source_directory = input("📂 Enter the source directory: ").strip()
        if not os.path.isdir(source_directory):
            logger.info("❌ ERROR: Source directory does not exist!")
            return
        save_last_directory(source_directory)

    process_images(source_directory)
    save_log(source_directory)

    logger.info("\n🎉 All images processed successfully! 🎊")
    logger.info("📜 A detailed log has been saved.")


if __name__ == "__main__":
    main()
