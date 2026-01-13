#!/usr/bin/env python3
import csv
import logging
import os
import time
from datetime import datetime

from PIL import Image, UnidentifiedImageError
from tqdm import tqdm

# Constants
CONSTANT_300 = 300
CONSTANT_1024 = 1024


# 🚀 Constants
TARGET_DPI = CONSTANT_300
UPSCALE_MULTIPLIER = 2  # How much to enlarge small images
BATCH_SIZE = 50
PAUSE_DURATION = 3  # Seconds between batches
SIZE_THRESHOLD_MB = 9  # Max image size threshold
MAX_IMAGE_SIZE_MB = 9  # Holy grail max size


# Configure logging
def setup_logging(log_file=None, verbose=False):
    level = logging.DEBUG if verbose else logging.INFO
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    logging.basicConfig(
        level=level, format="%(asctime)s [%(levelname)s] %(message)s", handlers=handlers
    )


# 🏆 Ask user for processing mode
def get_user_choice():
    logger.info("\nChoose Processing Mode:")
    logger.info("1. Resize images >= 9MB only (skip smaller ones)")
    logger.info("2. Resize >=9MB & upscale <9MB")
    logger.info("3. Upscale <9MB only (skip larger ones)")
    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice in ("1", "2", "3"):
            return int(choice)
        logger.info("Invalid. Please enter 1, 2, or 3.")
# 🔻 Resize large images
def resize_image(im, output_path):
    quality = 95
    while quality >= 20:
        im.save(output_path, dpi=(TARGET_DPI, TARGET_DPI), quality=quality)
        size_mb = os.path.getsize(output_path) / (CONSTANT_1024**2)
        if size_mb <= MAX_IMAGE_SIZE_MB:
            logging.info(
                f"Resized {os.path.basename(output_path)} -> {size_mb:.2f}MB at Q={quality}"
            )
            return True
        quality -= 5
    logging.warning(f"Could not shrink {os.path.basename(output_path)} below {MAX_IMAGE_SIZE_MB}MB")
    return False

# 🔺 Upscale small images
def upscale_image(im, output_path):
    w, h = im.size
    new_size = (int(w * UPSCALE_MULTIPLIER), int(h * UPSCALE_MULTIPLIER))
    im2 = im.resize(new_size, Image.LANCZOS)
    im2.save(output_path, dpi=(TARGET_DPI, TARGET_DPI), quality=95)
    logging.info(f"Upscaled {os.path.basename(output_path)} -> {new_size[0]}x{new_size[1]}")


# 🖼️ Process a batch
def process_batch(batch, root, mode, log_data):
    for file in tqdm(batch, desc="Processing batch", unit="file"):
        path = os.path.join(root, file)
        try:
            im = Image.open(path)
            size_mb = os.path.getsize(path) / (CONSTANT_1024**2)
            temp = os.path.join(root, f"tmp_{file}")

            # Mode 1: Resize only
            if mode == 1 and size_mb >= SIZE_THRESHOLD_MB:
                resize_image(im, temp)

            # Mode 2: Resize + Upscale
            elif mode == 2:
                if size_mb >= SIZE_THRESHOLD_MB:
                    resize_image(im, temp)
                else:
                    upscale_image(im, temp)

            # Mode 3: Upscale only
            elif mode == 3 and size_mb < SIZE_THRESHOLD_MB:
                upscale_image(im, temp)

            else:
                if os.path.exists(temp):
                    os.remove(temp)
                continue

            os.replace(temp, path)
            new_size_mb = os.path.getsize(path) / (CONSTANT_1024**2)
            log_data.append(
                {
                    "File": file,
                    "Orig MB": round(size_mb, 2),
                    "Final MB": round(new_size_mb, 2),
                    "Status": "OK",
                }
            )
        except UnidentifiedImageError:
            logging.debug(f"Skipped non-image: {file}")
            log_data.append({"File": file, "Status": "Skipped"})
        except Exception as e:
            logging.error(f"Error {file}: {e}")
            log_data.append({"File": file, "Status": f"Error: {e}"})


# 📦 Main processing
def process_images(source, mode, from_csv=False, column="path", log_file=None, verbose=False):
    setup_logging(log_file, verbose)
    log_data = []
    paths = []

    if from_csv:
        with open(source, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                p = row.get(column)
                if p and os.path.isfile(p):
                    paths.append(p)
    else:
        for root, _, files in os.walk(source):
            batch = []
            for file in files:
                batch.append(file)
                if len(batch) >= BATCH_SIZE:
                    process_batch(batch, root, mode, log_data)
                    batch = []
                    time.sleep(PAUSE_DURATION)
            if batch:
                process_batch(batch, root, mode, log_data)
    return log_data


# 📜 Write log
def write_log(log_data, source):
    base = os.path.basename(os.path.normpath(source))
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = f"{base}_{ts}.csv"
    keys = log_data[0].keys() if log_data else []
    with open(out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(log_data)
    logger.info(f"Log saved: {out}")


# 🎬 Entry point
def main():
    logger.info("Ultimate Batch Image Resizer & Upscaler")
    src = input("Enter folder or CSV path: ").strip()
    if not os.path.exists(src):
        logger.info("Invalid path!")
        return
    use_csv = src.lower().endswith(".csv")
    mode = get_user_choice()
    log_data = process_images(src, mode, from_csv=use_csv)
    write_log(log_data, src)
    logger.info("Done!")


if __name__ == "__main__":
    main()
