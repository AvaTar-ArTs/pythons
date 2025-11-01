"""
Upscale 6

This module provides functionality for upscale 6.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_1024 = 1024
CONSTANT_2000 = 2000
CONSTANT_4000 = 4000

#!/usr/bin/env python3
"""
Automatic Image Upscaler
Processes all images with multiple aspect ratios automatically
"""

import os
import sys
import subprocess
import math
from pathlib import Path
import shutil


def run_command(cmd):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def get_image_dimensions(image_path):
    """Get image dimensions using sips"""
    success, stdout, stderr = run_command(f'sips -g pixelWidth -g pixelHeight "{image_path}"')
    if not success:
        return None, None

    width = None
    height = None

    for line in stdout.split("\n"):
        if "pixelWidth:" in line:
            width = int(line.split(":")[1].strip())
        elif "pixelHeight:" in line:
            height = int(line.split(":")[1].strip())

    return width, height


def calculate_target_dimensions(width_ratio, height_ratio, target_dpi=CONSTANT_300):
    """Calculate target dimensions for the aspect ratio"""
    base_size = CONSTANT_2000

    if width_ratio >= height_ratio:
        # Landscape or square
        width = min(CONSTANT_4000, base_size * width_ratio)
        height = int(width * height_ratio / width_ratio)
    else:
        # Portrait
        height = min(CONSTANT_4000, base_size * height_ratio)
        width = int(height * width_ratio / height_ratio)

    return width, height


def resize_with_sips(input_path, output_path, target_width, target_height):
    """Resize image using sips with aspect ratio handling"""

    # Get original dimensions
    orig_width, orig_height = get_image_dimensions(input_path)
    if not orig_width or not orig_height:
        return False, "Could not get image dimensions"

    orig_ratio = orig_width / orig_height
    target_ratio = target_width / target_height

    # Calculate crop dimensions
    if orig_ratio > target_ratio:
        # Image is wider - crop width
        crop_width = int(orig_height * target_ratio)
        crop_x = (orig_width - crop_width) // 2
        crop_y = 0
        crop_width_final = crop_width
        crop_height_final = orig_height
    elif orig_ratio < target_ratio:
        # Image is taller - crop height
        crop_height = int(orig_width / target_ratio)
        crop_x = 0
        crop_y = (orig_height - crop_height) // 2
        crop_width_final = orig_width
        crop_height_final = crop_height
    else:
        # Already correct ratio
        crop_x = 0
        crop_y = 0
        crop_width_final = orig_width
        crop_height_final = orig_height

    # First crop, then resize
    temp_path = f"{output_path}.temp"
    crop_cmd = (
        f'sips -c {crop_height_final} {crop_width_final} -cOffset {crop_y} {crop_x} "{input_path}" --out "{temp_path}"'
    )
    resize_cmd = f'sips -z {target_height} {target_width} "{temp_path}" --out "{output_path}"'

    # Execute crop
    success1, _, err1 = run_command(crop_cmd)
    if not success1:
        return False, f"Crop failed: {err1}"

    # Execute resize
    success2, _, err2 = run_command(resize_cmd)
    if not success2:
        return False, f"Resize failed: {err2}"

    # Clean up temp file
    if os.path.exists(temp_path):
        os.remove(temp_path)

    # Set DPI to CONSTANT_300
    dpi_cmd = f'sips -s dpiHeight CONSTANT_300 -s dpiWidth CONSTANT_300 "{output_path}"'
    run_command(dpi_cmd)

    return True, "Success"


def optimize_file_size(image_path, max_size_mb=9.0):
    """Optimize file size by reducing quality if needed"""
    max_size_bytes = max_size_mb * CONSTANT_1024 * CONSTANT_1024

    # Check current file size
    current_size = os.path.getsize(image_path)
    if current_size <= max_size_bytes:
        return True, "File size already within limits"

    # Try different quality levels
    for quality in range(90, 20, -10):
        temp_path = f"{image_path}.temp"
        quality_cmd = f'sips -s formatOptions {quality} "{image_path}" --out "{temp_path}"'

        success, _, _ = run_command(quality_cmd)
        if success and os.path.exists(temp_path):
            temp_size = os.path.getsize(temp_path)
            if temp_size <= max_size_bytes:
                # Replace original with optimized version
                shutil.move(temp_path, image_path)
                return True, f"Optimized to {quality}% quality"
            else:
                os.remove(temp_path)

    return False, "Could not optimize file size"


def upscale_image(input_path, output_path, width_ratio, height_ratio):
    """Upscale a single image"""
    try:
        # Calculate target dimensions
        target_width, target_height = calculate_target_dimensions(width_ratio, height_ratio)

        # Resize image
        success, message = resize_with_sips(input_path, output_path, target_width, target_height)
        if not success:
            return {"success": False, "error": message}

        # Optimize file size
        opt_success, opt_message = optimize_file_size(output_path)
        if not opt_success:
            logger.info(f"Warning: {opt_message}")

        # Get final dimensions and size
        final_width, final_height = get_image_dimensions(output_path)
        file_size = os.path.getsize(output_path)

        return {
            "success": True,
            "original_size": get_image_dimensions(input_path),
            "new_size": (final_width, final_height),
            "file_size_mb": file_size / (CONSTANT_1024 * CONSTANT_1024),
            "message": message,
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def process_all_ratios():
    """Process all images with multiple aspect ratios"""

    # Define aspect ratios to process
    ratios = {
        "16x9": (16, 9, "16:9"),
        "9x16": (9, 16, "9:16"),
        "1x1": (1, 1, "1:1"),
        "4x3": (4, 3, "4:3"),
        "3x4": (3, 4, "3:4"),
        "3x2": (3, 2, "3:2"),
        "2x3": (2, 3, "2:3"),
    }

    # Check if sips is available
    success, _, _ = run_command("which sips")
    if not success:
        logger.info("❌ sips command not found. This script requires macOS.")
        return

    # Find all JPG files
    current_dir = Path(".")
    image_files = list(current_dir.glob("*.jpg"))

    if not image_files:
        logger.info("❌ No JPG files found in current directory")
        return

    logger.info(f"🖼️  AUTOMATIC IMAGE UPSCALER")
    logger.info("=" * 50)
    logger.info(f"Found {len(image_files)} JPG files")
    logger.info(f"Processing with {len(ratios)} aspect ratios")
    logger.info("=" * 50)

    total_processed = 0
    total_successful = 0

    for ratio_name, (width_ratio, height_ratio, display_name) in ratios.items():
        logger.info(f"\n📐 Processing {display_name}...")

        # Create output directory
        output_dir = f"upscaled_{ratio_name}"
        os.makedirs(output_dir, exist_ok=True)

        successful = 0
        failed = 0

        for i, file_path in enumerate(image_files, 1):
            output_path = Path(output_dir) / f"upscaled_{file_path.name}"

            logger.info(f"  [{i}/{len(image_files)}] {file_path.name}...", end=" ")

            result = upscale_image(file_path, output_path, width_ratio, height_ratio)

            if result["success"]:
                successful += 1
                total_successful += 1
                logger.info(f"✅ {result['file_size_mb']:.1f}MB")
            else:
                failed += 1
                logger.info(f"❌ {result['error']}")

            total_processed += 1

        logger.info(f"  📊 {display_name}: {successful} successful, {failed} failed")

    # Final summary
    logger.info(f"\n🎉 BATCH PROCESSING COMPLETE!")
    logger.info("=" * 50)
    logger.info(f"Total images processed: {total_processed}")
    logger.info(f"Total successful: {total_successful}")
    logger.info(f"Total failed: {total_processed - total_successful}")
    logger.info(f"\n📁 Output directories created:")
    for ratio_name in ratios.keys():
        logger.info(f"  • upscaled_{ratio_name}/")

    logger.info(f"\n💡 All images are:")
    logger.info(f"  • CONSTANT_300 DPI for print quality")
    logger.info(f"  • Under 9MB file size")
    logger.info(f"  • Optimized for web and print use")
    logger.info(f"  • Cropped to exact aspect ratios")


if __name__ == "__main__":
    process_all_ratios()
