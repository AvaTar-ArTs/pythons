#!/usr/bin/env python3
"""
Image Upscaler using macOS sips command
Upscales images to 300 DPI with various aspect ratios using built-in macOS tools
"""

import os
import shutil
import subprocess
from pathlib import Path


def run_command(cmd):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def get_image_dimensions(image_path):
    """Get image dimensions using sips"""
    success, stdout, stderr = run_command(
        f'sips -g pixelWidth -g pixelHeight "{image_path}"'
    )
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


def calculate_target_dimensions(width_ratio, height_ratio, target_dpi=300):
    """Calculate target dimensions for the aspect ratio"""
    # Base size for calculations
    base_size = 2000

    if width_ratio >= height_ratio:
        # Landscape or square
        width = min(4000, base_size * width_ratio)
        height = int(width * height_ratio / width_ratio)
    else:
        # Portrait
        height = min(4000, base_size * height_ratio)
        width = int(height * width_ratio / height_ratio)

    return width, height


def resize_with_sips(:
    input_path, output_path, target_width, target_height, method="crop"
):
    """Resize image using sips with aspect ratio handling"""

    # Get original dimensions
    orig_width, orig_height = get_image_dimensions(input_path)
    if not orig_width or not orig_height:
        return False, "Could not get image dimensions"

    orig_ratio = orig_width / orig_height
    target_ratio = target_width / target_height

    if method == "crop":
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
        crop_cmd = f'sips -c {crop_height_final} {crop_width_final} -cOffset {crop_y} {crop_x} "{input_path}" --out "{temp_path}"'
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

    else:
        # Direct resize (may distort)
        resize_cmd = f'sips -z {target_height} {target_width} "{input_path}" --out "{output_path}"'
        success, _, err = run_command(resize_cmd)
        if not success:
            return False, f"Resize failed: {err}"

    # Set DPI to 300
    dpi_cmd = f'sips -s dpiHeight 300 -s dpiWidth 300 "{output_path}"'
    run_command(dpi_cmd)

    return True, "Success"


def optimize_file_size(image_path, max_size_mb=9.0):
    """Optimize file size by reducing quality if needed"""
    max_size_bytes = max_size_mb * 1024 * 1024

    # Check current file size
    current_size = os.path.getsize(image_path)
    if current_size <= max_size_bytes:
        return True, "File size already within limits"

    # Try different quality levels
    for quality in range(90, 20, -10):
        temp_path = f"{image_path}.temp"
        quality_cmd = (
            f'sips -s formatOptions {quality} "{image_path}" --out "{temp_path}"'
        )

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


def upscale_image(input_path, output_path, width_ratio, height_ratio, method="crop"):
    """Upscale a single image"""
    try:
        # Calculate target dimensions
        target_width, target_height = calculate_target_dimensions(
            width_ratio, height_ratio
        )

        # Resize image
        success, message = resize_with_sips(
            input_path, output_path, target_width, target_height, method
        )
        if not success:
            return {"success": False, "error": message}

        # Optimize file size
        opt_success, opt_message = optimize_file_size(output_path)
        if not opt_success:
            print(f"Warning: {opt_message}")

        # Get final dimensions and size
        final_width, final_height = get_image_dimensions(output_path)
        file_size = os.path.getsize(output_path)

        return {
            "success": True,
            "original_size": get_image_dimensions(input_path),
            "new_size": (final_width, final_height),
            "file_size_mb": file_size / (1024 * 1024),
            "message": message,
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    print("🖼️  IMAGE UPSCALER (macOS sips)")
    print("=" * 50)
    print("Upscales images to 300 DPI with various aspect ratios")
    print("Uses built-in macOS sips command")

    # Get current directory
    current_dir = os.getcwd()
    print(f"\n📁 Working directory: {current_dir}")

    # Check if sips is available
    success, _, _ = run_command("which sips")
    if not success:
        print("❌ sips command not found. This script requires macOS.")
        return

    # Define aspect ratios
    ratios = {
        "1": (16, 9, "16:9"),
        "2": (9, 16, "9:16"),
        "3": (1, 1, "1:1"),
        "4": (4, 3, "4:3"),
        "5": (3, 4, "3:4"),
        "6": (3, 2, "3:2"),
        "7": (2, 3, "2:3"),
    }

    print("\n📐 Choose aspect ratio:")
    for key, (w, h, name) in ratios.items():
        print(f"{key}. {name}")

    while True:
        choice = input("\nEnter choice (1-7): ").strip()
        if choice in ratios:
            width_ratio, height_ratio, ratio_name = ratios[choice]
            break
        print("Invalid choice. Please enter 1-7.")

    print(f"Selected: {ratio_name}")

    # Find JPG files
    image_files = list(Path(current_dir).glob("*.jpg"))

    if not image_files:
        print("❌ No JPG files found in current directory")
        return

    print(f"\n📊 Found {len(image_files)} JPG files")

    # Create output directory
    output_dir = f"upscaled_{ratio_name.replace(':', 'x')}"
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Output directory: {output_dir}")

    # Process files
    successful = 0
    failed = 0

    print("\n🔄 Processing files...")
    print("=" * 50)

    for i, file_path in enumerate(image_files, 1):
        output_path = Path(output_dir) / f"upscaled_{file_path.name}"

        print(f"[{i}/{len(image_files)}] {file_path.name}...")

        result = upscale_image(
            file_path, output_path, width_ratio, height_ratio, "crop"
        )

        if result["success"]:
            successful += 1
            print(f"  ✅ {result['new_size']} @ {result['file_size_mb']:.2f}MB")
        else:
            failed += 1
            print(f"  ❌ Error: {result['error']}")

    # Summary
    print("\n🎉 PROCESSING COMPLETE!")
    print("=" * 50)
    print(f"Total files: {len(image_files)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Output directory: {output_dir}")

    if successful > 0:
        print("\n💡 Tips:")
        print("  • Images are saved at 300 DPI for print quality")
        print("  • File sizes are optimized to stay under 9MB")
        print("  • Original files are preserved")
        print(f"  • Check the '{output_dir}' folder for results")


if __name__ == "__main__":
    main()
