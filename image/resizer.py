"""
Img Resizer

This module provides functionality for img resizer.

Author: Auto-generated
Date: 2025-11-01
"""

#!/usr/bin/env python3
import os
import csv
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, UnidentifiedImageError
from tqdm import tqdm

# Constants
CONSTANT_300 = 300
CONSTANT_1024 = 1024


# Configure logging
def setup_logging(log_file=None, verbose=False):
    """setup_logging function."""

    level = logging.DEBUG if verbose else logging.INFO
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(message)s", handlers=handlers)

    """process_image function."""


def process_image(path, threshold_mb, max_mb, upscale_factor, dpi):
    try:
        size_mb = os.path.getsize(path) / (CONSTANT_1024**2)
        with Image.open(path) as img:
            if size_mb >= threshold_mb:
                # reduce quality
                for quality in range(95, 19, -5):
                    img.save(path, dpi=(dpi, dpi), quality=quality)
                    size_mb = os.path.getsize(path) / (CONSTANT_1024**2)
                    if size_mb <= max_mb:
                        logging.info(f"Resized {os.path.basename(path)} -> {size_mb:.2f}MB at Q={quality}")
                        return
                logging.warning(f"Could not reduce {os.path.basename(path)} below {max_mb}MB")
            else:
                # upscale small images
                w, h = img.size
                new_size = (int(w * upscale_factor), int(h * upscale_factor))
                img2 = img.resize(new_size, Image.LANCZOS)
                img2.save(path, dpi=(dpi, dpi), quality=95)
                logging.info(f"Upscaled {os.path.basename(path)} -> {new_size[0]}x{new_size[1]}")
    except UnidentifiedImageError:
        logging.debug(f"Skipped non-image: {path}")
    except Exception as e:
        logging.error(f"Error processing {path}: {e}")

    """load_paths_from_csv function."""


def load_paths_from_csv(csv_file, column_name):
    paths = []
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            p = row.get(column_name) or row.get("path") or row.get("file")
            if p and os.path.isfile(p):
                paths.append(p)
            else:
                logging.warning(f"Invalid or missing path: {p}")
    return paths
    """main function."""


def main():
    parser = argparse.ArgumentParser(description="Batch Image Resize/Upscale Tool")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--directory", help="Directory of images to scan")
    group.add_argument("-c", "--csv", help="CSV file listing image paths")
    parser.add_argument("-n", "--column", default="path", help="CSV column name for file paths")
    parser.add_argument("-t", "--threshold", type=float, default=8, help="MB threshold to decide resize vs upscale")
    parser.add_argument("-m", "--max", type=float, default=10, help="Max MB after resizing")
    parser.add_argument("-u", "--upscale", type=float, default=2, help="Upscale factor for small images")
    parser.add_argument("--dpi", type=int, default=CONSTANT_300, help="DPI for saved images")
    parser.add_argument("-w", "--workers", type=int, default=4, help="Number of parallel workers")
    parser.add_argument("-l", "--log", help="Log file path")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose (debug) logging")
    args = parser.parse_args()

    setup_logging(args.log, args.verbose)

    # Gather image paths
    if args.directory:
        exts = (".jpg", ".jpeg", ".png", ".webp", ".tiff")
        paths = []
        for root, _, files in os.walk(args.directory):
            for fn in files:
                if fn.lower().endswith(exts):
                    paths.append(os.path.join(root, fn))
    else:
        paths = load_paths_from_csv(args.csv, args.column)

    if not paths:
        logging.error("No valid images found.")
        return

    # Process in parallel with progress
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        for _ in tqdm(
            executor.map(lambda p: process_image(p, args.threshold, args.max, args.upscale, args.dpi), paths),
            total=len(paths),
            desc="Processing images",
        ):
            pass


if __name__ == "__main__":
    main()
