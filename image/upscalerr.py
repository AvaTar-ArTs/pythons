"""
Upscalerr

This module provides functionality for upscalerr.

Author: Auto-generated
Date: 2025-11-01
"""

import os
import time
from datetime import datetime
from PIL import Image, UnidentifiedImageError
import csv
from tqdm import tqdm

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_1024 = 1024


# 🚀 Constants
TARGET_DPI = CONSTANT_300
UPSCALE_MULTIPLIER = 2  # How much to enlarge small images
BATCH_SIZE = 50
PAUSE_DURATION = 3  # Just for dramatic effect 🎭
SIZE_THRESHOLD_MB = 9  # The Holy Grail of size rules

# 📜 Log Data
log_data = []

# 🏆 Ask the user for the processing mode
def get_user_choice():
    """get_user_choice function."""

    logger.info("\n🎯 Choose Processing Mode:")
    logger.info("1️⃣ Only resize images 9MB+ (Skip smaller ones)")
    logger.info("2️⃣ Resize 9MB+ & upscale anything smaller")
    logger.info("3️⃣ Only upscale images below 9MB (Ignore large ones)")
    
    while True:
        choice = input("\n🔹 Enter 1, 2, or 3: ").strip()
        if choice in ("1", "2", "3"):
            return int(choice)
        logger.info("❌ Invalid choice! Please enter 1, 2, or 3.")

# 🖨️ Apply CONSTANT_300 DPI
    """apply_dpi function."""

def apply_dpi(im, output_path):
    im.save(output_path, dpi=(TARGET_DPI, TARGET_DPI), quality=95)

    """resize_image function."""

# 🔻 Resize images larger than 9MB
def resize_image(im, output_path):
    logger.info(f"📉 Resizing image to reduce file size...")

    quality = 95  # Start with high quality
    while quality > 10:  # Don't go below 10, because nobody likes pixel soup
        im.save(output_path, dpi=(TARGET_DPI, TARGET_DPI), quality=quality)
        file_size_mb = os.path.getsize(output_path) / (CONSTANT_1024 ** 2)
        if file_size_mb <= SIZE_THRESHOLD_MB:
            logger.info(f"✅ Resized successfully! New Size: {file_size_mb:.2f} MB")
            return
        quality -= 5  # Reduce quality until it fits

    logger.info(f"⚠️ Could not shrink below {file_size_mb:.2f} MB, keeping best effort.")
    """upscale_image function."""


# 🔺 Upscale images smaller than 9MB
def upscale_image(im, output_path):
    logger.info(f"📈 Upscaling image to meet quality standards...")

    new_width = im.width * UPSCALE_MULTIPLIER
    new_height = im.height * UPSCALE_MULTIPLIER

    im = im.resize((new_width, new_height), Image.LANCZOS)
    im.save(output_path, dpi=(TARGET_DPI, TARGET_DPI), quality=95)
    """process_batch function."""

    logger.info(f"✅ Upscaled successfully to {new_width}x{new_height}!")

# 🖼️ Process a batch of images based on user choice
def process_batch(batch, root, mode):
    for file in tqdm(batch, desc="✨ Processing images ✨", unit="file"):
        file_path = os.path.join(root, file)
        file_ext = file.lower().split('.')[-1]

        if file_ext not in ('jpg', 'jpeg', 'png', 'webp'):
            logger.info(f"⚠️ Skipping {file}: Unsupported format.")
            continue  

        try:
            im = Image.open(file_path)
            file_size_mb = os.path.getsize(file_path) / (CONSTANT_1024 ** 2)

            temp_file = os.path.join(root, f"processed_{file}")

            logger.info(f"\n📂 Processing: {file} ({file_size_mb:.2f} MB)")

            if mode == 1 and file_size_mb < SIZE_THRESHOLD_MB:
                logger.info(f"⏭️ Skipping {file} (Too small for resizing)")
                continue

            # Resize if it's 9MB+ and user chose mode 1 or 2
            if file_size_mb >= SIZE_THRESHOLD_MB and mode in (1, 2):
                logger.info(f"🔻 Shrinking file (TOO BIG!)...")
                resize_image(im, temp_file)

            # Upscale if it's below 9MB and user chose mode 2 or 3
            elif file_size_mb < SIZE_THRESHOLD_MB and mode in (2, 3):
                logger.info(f"🔺 Enlarging file (TOO SMALL!)...")
                upscale_image(im, temp_file)

            os.replace(temp_file, file_path)  # Overwrite original

            log_data.append({
                "File": file,
                "Original Size (MB)": round(file_size_mb, 2),
                "Final Size (MB)": round(os.path.getsize(file_path) / (CONSTANT_1024 ** 2), 2),
                "Status": "Processed ✅"
            })

        except UnidentifiedImageError:
            logger.info(f"❌ ERROR: Cannot process {file}. Unrecognized format!")
            log_data.append({"File": file, "Status": "Error - Unidentified Image"})
        except Exception as e:
    """process_images function."""

            logger.info(f"❌ ERROR processing {file}: {str(e)}")
            log_data.append({"File": file, "Status": f"Error - {str(e)}"})

# 📦 Process all images in a directory
def process_images(source_directory, mode):
    batch = []
    for root, _, files in os.walk(source_directory):
        for file in files:
            batch.append(file)
            if len(batch) >= BATCH_SIZE:
                process_batch(batch, root, mode)
                batch = []
                time.sleep(PAUSE_DURATION)  # ⏳ Adds suspense
    """write_log function."""


        if batch:
            process_batch(batch, root, mode)

# 📜 Write log to CSV with Auto-Generated Name
def write_log(source_directory):
    folder_name = os.path.basename(os.path.normpath(source_directory))  # Get the folder name
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')  # Format: YYYY-MM-DD_HHMM
    output_file = os.path.join(source_directory, f"{folder_name}_{timestamp}.csv")

    fieldnames = ["File", "Original Size (MB)", "Final Size (MB)", "Status"]
    
    with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    """main function."""

        writer.writeheader()
        writer.writerows(log_data)

    logger.info(f"📜 Log saved as: {output_file}")

# 🚀 Main function
def main():
    logger.info("🔥 Welcome to the Ultimate Image Resizer & Upscaler 🔥")
    source_directory = input("📂 Enter the path to the source directory: ").strip()

    if not os.path.isdir(source_directory):
        logger.info("🚨 ERROR: Source directory does not exist!")
        return

    mode = get_user_choice()  # Ask the user for mode selection
    process_images(source_directory, mode)
    write_log(source_directory)

    logger.info("\n🎉 All images processed successfully! 🎊")
    logger.info("📜 A detailed log has been saved.")

if __name__ == "__main__":
    main()
