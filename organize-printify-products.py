from pathlib import Path
import csv
import os
import time
from datetime import datetime

import cv2
import numpy as np
import pytesseract
from PIL import Image, UnidentifiedImageError
from tqdm import tqdm

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200


# Configure Tesseract for OCR
pytesseract.pytesseract.tesseract_cmd = Path(
    "/usr/local/bin/tesseract"
)  # Adjust path as needed

# Constants
BATCH_SIZE = 50
PAUSE_DURATION = 2  # Pause between batches for readability
CSV_FIELDS = [
    "Platform",
    "File",
    "Product",
    "Category",
    "Features",
    "Mockup Recommendation",
]

# Platforms with product and mockup recommendations
PLATFORMS = {
    "tiktok": {
        "hoodie": ["bold colors", "dark tones", "statement text"],
        "t-shirt": ["minimalist", "memes", "high contrast"],
        "tote bag": ["artistic", "neutral tones", "simple graphics"],
        "phone case": ["vibrant", "pop culture", "sharp details"],
        "sticker": ["high contrast", "small details", "text-heavy"],
        "candle": ["aesthetic", "soft colors", "cozy themes"],
        "plush blanket": ["soft tones", "cozy aesthetics", "neutral patterns"],
    },
    "etsy": {
        "ceramic mug": ["custom text", "personalized gifts", "vintage aesthetics"],
        "cotton tee": ["affordable", "durable", "versatile for daily wear"],
        "crewneck sweatshirt": [
            "classic style",
            "warmth",
            "perfect for custom designs",
        ],
        "jersey tee": ["soft material", "stylish", "great for casual fashion"],
        "garment-dyed t-shirt": ["premium look", "trendy", "youth appeal"],
        "hooded sweatshirt": ["cozy", "seasonal favorite", "customizable"],
        "scented candle": ["relaxation", "premium home decor", "giftable"],
        "tote bag": ["eco-friendly", "practical", "ideal for custom graphics"],
        "matte canvas": ["artistic", "premium home decor", "custom prints"],
        "plush blanket": ["soft tones", "comfort", "perfect for gifts"],
    },
}

# Mockup recommendations
MOCKUP_GUIDE = {
    "hoodie": "4-6 (front, back, lifestyle shots, close-ups)",
    "t-shirt": "4-6 (front, back, lifestyle shots, close-ups)",
    "tote bag": "3-5 (both sides, lifestyle shots)",
    "phone case": "3-4 (front, angled, lifestyle shots)",
    "sticker": "2-3 (detailed, lifestyle, on products)",
    "candle": "3-4 (top, side, lifestyle shots)",
    "plush blanket": "3-5 (folded, spread out, lifestyle shots)",
    "ceramic mug": "3-5 (both sides, top view, lifestyle shots)",
    "matte canvas": "3-5 (angled, wall-mounted, close-ups)",
}


# Get dominant color from image
def get_dominant_color(image_path):
    """get_dominant_color function."""

    img = Image.open(image_path).resize((50, 50))  # Downsample for faster processing
    img_array = np.array(img).reshape(-1, 3)
    unique, counts = np.unique(img_array, axis=0, return_counts=True)
    dominant_color = unique[counts.argmax()]  # Most common color
    return tuple(dominant_color)

    # Detect text from image using OCR
    """detect_text function."""


def detect_text(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text.strip() if text else None

    """suggest_product function."""


# Suggest product type based on platform, colors, and text
def suggest_product(platform, dominant_color, text):
    r, g, b = dominant_color
    category = "unknown"

    if text:
        category = (
            "sticker"
            if len(text) < 50
            else "t-shirt" if platform == "tiktok" else "ceramic mug"
        )

    elif r > g and r > b:
        category = "hoodie" if platform == "tiktok" else "tote bag"

    elif g > r and g > b:
        category = "candle"

    elif b > r and b > g:
        category = "phone case"

    elif r > CONSTANT_200 and g > CONSTANT_200 and b > CONSTANT_200:
        category = "plush blanket"

    return category

    """process_batch function."""


# Process batch of images
def process_batch(batch, root, platform):
    csv_data = []
    for file in tqdm(batch, desc="✨ Processing Files ✨", unit="file"):
        file_path = os.path.join(root, file)
        file_ext = file.lower().split(".")[-1]

        if file_ext not in ("jpg", "jpeg", "png", "webp"):
            logger.info(f"⚠️ Skipping {file}: Unsupported format.")
            continue

        try:
            dominant_color = get_dominant_color(file_path)
            text_detected = detect_text(file_path)
            product_category = suggest_product(platform, dominant_color, text_detected)

            csv_data.append(
                {
                    "Platform": platform.capitalize(),
                    "File": file,
                    "Product": product_category,
                    "Category": product_category,
                    "Features": ", ".join(
                        PLATFORMS[platform].get(product_category, [])
                    ),
                    "Mockup Recommendation": MOCKUP_GUIDE.get(product_category, "N/A"),
                }
            )
        except UnidentifiedImageError:
            logger.info(f"❌ Skipping {file}: Unidentified Image Format!")
        except Exception as e:
            logger.info(f"❌ Error processing {file}: {e}")

    return csv_data
    """process_images function."""


# Process images in directory
def process_images(source_directory, platform):
    csv_rows = []
    batch = []
    for root, _, files in os.walk(source_directory):
        for file in files:
            batch.append(file)
            if len(batch) >= BATCH_SIZE:
                csv_rows.extend(process_batch(batch, root, platform))
                batch = []
                time.sleep(PAUSE_DURATION)

        if batch:
            csv_rows.extend(process_batch(batch, root, platform))

    """write_csv function."""

    return csv_rows


# Write processed data to CSV
def write_csv(source_directory, csv_rows):
    folder_name = os.path.basename(os.path.normpath(source_directory))
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    output_file = os.path.join(
        source_directory, f"{folder_name}_organized_{timestamp}.csv"
    )

    with open(output_file, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(csv_rows)
    """main function."""

    logger.info(f"📜 CSV saved as: {output_file}")


# Main Function
def main():
    logger.info("🔥 Welcome to the Printify Organizer 🔥")
    source_directory = input("📂 Enter the path to the source directory: ").strip()

    logger.info("\n🎯 Choose Platform:")
    logger.info("1️⃣ Etsy")
    logger.info("2️⃣ TikTok")
    platform_choice = input("\n🔹 Enter 1 or 2: ").strip()
    platform = (
        "etsy"
        if platform_choice == "1"
        else "tiktok" if platform_choice == "2" else None
    )

    if not platform:
        logger.info("❌ Invalid platform choice! Exiting.")
        return

    if not os.path.isdir(source_directory):
        logger.info("🚨 ERROR: Source directory does not exist!")
        return

    csv_rows = process_images(source_directory, platform)
    write_csv(source_directory, csv_rows)

    logger.info("\n🎉 All files processed and organized successfully! 🎊")


if __name__ == "__main__":
    main()
