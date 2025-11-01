"""
Media Processing Image Get 77

This module provides functionality for media processing image get 77.

Author: Auto-generated
Date: 2025-11-01
"""

import csv
import os
from datetime import datetime

from PIL import Image, UnidentifiedImageError
from tqdm import tqdm

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_1024 = 1024


# Constants
TARGET_DPI = CONSTANT_300
TARGET_MIN_FILE_SIZE_MB = 5  # Minimum file size in MB
TARGET_MAX_FILE_SIZE_MB = 9  # Maximum file size in MB
ASPECT_RATIOS = [
    (9, 16),
    (16, 9),
    (1, 1),
    (2, 3),
    (3, 2),
    (4, 5),
    (5, 4),
    (1, 2),
    (2, 1),
]  # Supported aspect ratios

# Initialize log data
log_data = []


# Function to dynamically calculate the closest aspect ratio
def get_closest_aspect_ratio(width, height):
    """get_closest_aspect_ratio function."""

    current_ratio = width / height
    closest_ratio = min(ASPECT_RATIOS, key=lambda r: abs(current_ratio - (r[0] / r[1])))
    return closest_ratio


# Function to resize images while maintaining file size and aspect ratio
    """resize_image_to_target_size function."""

def resize_image_to_target_size(im, output_path):
    width, height = im.size
    closest_ratio = get_closest_aspect_ratio(width, height)
    aspect_ratio = closest_ratio[0] / closest_ratio[1]

    print(
        f"🔍 Closest aspect ratio: {closest_ratio[0]}:{closest_ratio[1]} (Current ratio: {width}:{height})"
    )

    # Adjust dimensions to enforce the closest aspect ratio
    if width / height > aspect_ratio:
        new_width = width
        new_height = int(width / aspect_ratio)
    else:
        new_height = height
        new_width = int(height * aspect_ratio)

    print(
        f"🔄 Adjusting dimensions to: {new_width}x{new_height} with ratio {closest_ratio[0]}:{closest_ratio[1]}"
    )
    im = im.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Save image iteratively to achieve the target file size
    quality = 95  # Start with high quality
    while quality > 10:  # Minimum quality threshold
        im.save(output_path, dpi=(TARGET_DPI, TARGET_DPI), quality=quality)
        file_size_mb = os.path.getsize(output_path) / (CONSTANT_1024**2)
        if TARGET_MIN_FILE_SIZE_MB <= file_size_mb <= TARGET_MAX_FILE_SIZE_MB:
            logger.info(f"✅ File size optimized: {file_size_mb:.2f} MB (Quality: {quality})")
            return True, file_size_mb, (new_width, new_height)
        quality -= 5  # Reduce quality incrementally if size doesn't fit

    print(
        f"⚠️ Unable to resize {output_path} to target size range. Final file size: {file_size_mb:.2f} MB"
    )
    return False, file_size_mb, (new_width, new_height)


    """process_image function."""

# Function to process a single image
def process_image(file_path):
    file_ext = file_path.lower().split(".")[-1]
    entry = {
        "File Name": os.path.basename(file_path),
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Skip unsupported file formats
    if file_ext not in ("jpg", "jpeg", "png", "webp"):
        logger.info(f"⚠️ Skipping {file_path}: Unsupported file format.")
        entry["Status"] = "Skipped - Unsupported Format"
        log_data.append(entry)
        return

    # Open image
    try:
        im = Image.open(file_path)
        width, height = im.size
        file_size_mb = os.path.getsize(file_path) / (CONSTANT_1024**2)
        entry["Original Dimensions"] = f"{width}x{height}"
        entry["Original Size (MB)"] = round(file_size_mb, 2)

        # Skip files smaller than the target minimum size
        if file_size_mb < TARGET_MIN_FILE_SIZE_MB:
            logger.info(f"⚠️ Skipping {file_path}: File size below {TARGET_MIN_FILE_SIZE_MB} MB.")
            entry["Status"] = "Skipped - File Too Small"
            log_data.append(entry)
            return

        print(
            f"\n🖼️ Processing {os.path.basename(file_path)}: {width}x{height}, {file_size_mb:.2f} MB"
        )

        # Resize and overwrite the original file
        success, new_file_size_mb, new_dimensions = resize_image_to_target_size(im, file_path)

        entry["New Dimensions"] = f"{new_dimensions[0]}x{new_dimensions[1]}"
        entry["New Size (MB)"] = round(new_file_size_mb, 2)
        entry["Status"] = "Resized" if success else "Error - Size Not Achieved"

    except UnidentifiedImageError:
        logger.info(f"⚠️ Skipping {file_path}: Cannot identify image.")
        entry["Status"] = "Error - Unidentified Image"
    except Exception as e:
        logger.info(f"⚠️ Error processing {file_path}: {e}")
        entry["Status"] = f"Error - {str(e)}"

    log_data.append(entry)

    """process_images_in_directory function."""


# Function to process images in a directory
def process_images_in_directory(source_directory):
    for root, _, files in os.walk(source_directory):
        batch = [os.path.join(root, file) for file in files]
        if batch:
            logger.info(f"🔄 Processing {len(batch)} images in {root}...")
            for file in tqdm(batch, desc="Processing images", unit="file"):
                process_image(file)
    """write_log_to_csv function."""



# Write log to CSV
def write_log_to_csv(output_file):
    fieldnames = [
        "File Name",
        "Timestamp",
        "Original Dimensions",
        "Original Size (MB)",
        "New Dimensions",
        "New Size (MB)",
        "Status",
    ]
    with open(output_file, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(log_data)
    """display_summary function."""

    logger.info(f"📄 Log saved to {output_file}")


# Display summary
def display_summary():
    resized_count = sum(1 for entry in log_data if entry["Status"] == "Resized")
    skipped_count = len(log_data) - resized_count
    logger.info("\n📊 Processing Summary:")
    logger.info(f"   ✅ Resized: {resized_count}")
    logger.info(f"   ⚠️ Skipped: {skipped_count}")
    for reason in set(entry["Status"] for entry in log_data if "Skipped" in entry["Status"]):
    """main function."""

        count = sum(1 for entry in log_data if entry["Status"] == reason)
        logger.info(f"      - {reason}: {count}")


# Main function
def main():
    logger.info("✨ Welcome to the Advanced Image Resizer ✨")
    source_directory = input("Enter the path to the source directory containing images: ").strip()
    if not os.path.isdir(source_directory):
        logger.info("❌ Source directory does not exist.")
        return

    process_images_in_directory(source_directory)

    # Write log to CSV
    timestamp = datetime.now().strftime("%m%d%Y_%H%M%S")
    csv_output_path = os.path.join(source_directory, f"image_processing_log_{timestamp}.csv")
    write_log_to_csv(csv_output_path)

    # Display summary
    display_summary()
    logger.info("🎉 All images processed successfully!")


if __name__ == "__main__":
    main()
