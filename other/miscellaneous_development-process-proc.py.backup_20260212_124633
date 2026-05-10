import csv
import os
from datetime import datetime

from PIL import Image, UnidentifiedImageError

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024
CONSTANT_1500 = 1500
CONSTANT_2000 = 2000
CONSTANT_2500 = 2500
CONSTANT_3000 = 3000
CONSTANT_4000 = 4000


# 🎯 Bestselling Product Categories for Etsy & TikTok
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


# 🎨 Function to Determine Printify Product Category
def categorize_image(image_width, image_height):
    """categorize_image function."""

    if image_width >= CONSTANT_4000 or image_height >= CONSTANT_4000:
        return "matte canvas"
    elif image_width >= CONSTANT_3000 and image_height >= CONSTANT_3000:
        return "plush blanket"
    elif image_width >= CONSTANT_2500 and image_height >= CONSTANT_2500:
        return "hoodie"
    elif image_width >= CONSTANT_2000 and image_height >= CONSTANT_2000:
        return "t-shirt"
    elif image_width >= CONSTANT_1500 and image_height >= CONSTANT_1500:
        return "tote bag"
    elif image_width >= CONSTANT_1000 and image_height >= CONSTANT_1000:
        return "ceramic mug"
    else:
        return "sticker"

    # 📜 Process Images & Generate CSV
    """process_images function."""


def process_images(source_directory, platform):
    logger.info(
        f"\n📂 Scanning Directory: {source_directory} for {platform.upper()} products"
    )

    output_data = []
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    output_filename = os.path.join(
        source_directory, f"{platform}_organized_{timestamp}.csv"
    )

    for root, _, files in os.walk(source_directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = file.lower().split(".")[-1]

            if file_ext not in ("jpg", "jpeg", "png", "webp"):
                logger.info(f"⚠️ Skipping {file}: Unsupported format.")
                continue

            try:
                im = Image.open(file_path)
                width, height = im.size
                file_size = round(os.path.getsize(file_path) / (CONSTANT_1024**2), 2)

                category = categorize_image(width, height)
                best_selling_keywords = ", ".join(
                    PLATFORMS[platform].get(category, ["general use"])
                )

                output_data.append(
                    {
                        "Filename": file,
                        "File Size (MB)": file_size,
                        "Width": width,
                        "Height": height,
                        "Suggested Category": category,
                        "Best Selling Keywords": best_selling_keywords,
                    }
                )

            except UnidentifiedImageError:
                logger.info(f"❌ ERROR: Cannot process {file}. Unrecognized format!")

    # Save to CSV
    with open(output_filename, mode="w", newline="", encoding="utf-8") as csv_file:
        fieldnames = [
            "Filename",
            "File Size (MB)",
            "Width",
            "Height",
            "Suggested Category",
            "Best Selling Keywords",
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_data)

    logger.info(f"\n✅ CSV file saved: {output_filename}")

    """main function."""


# 🚀 Main Function
def main():
    logger.info("🔥 Welcome to the Printify Image Organizer 🔥")
    source_directory = input("📂 Enter the path to the source directory: ").strip()

    if not os.path.isdir(source_directory):
        logger.info("🚨 ERROR: Source directory does not exist!")
        return

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
        logger.info("❌ Invalid choice! Exiting...")
        return

    process_images(source_directory, platform)
    logger.info("\n🎉 All images processed successfully! 🎊")


if __name__ == "__main__":
    main()
