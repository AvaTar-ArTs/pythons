#!/usr/bin/env python3
"""
Web Image Upscaler (v2)
Converts and upscales web images (WEBP, TIFF) to PNG/JPEG.
Uses core utilities for consistent processing.
"""

import os
from pathlib import Path
from typing import Optional

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from core import (
    UpscaleConfig,
    get_image_processor,
    optimize_file_size,
    get_file_size,
    ProcessorNotFoundError,
)


def convert_and_upscale_webp(
    input_path: str,
    output_path: str,
    target_format: str = 'JPEG',
    scale_factor: int = 2,
    target_dpi: int = 300,
    max_size_mb: float = 9.0
) -> dict:
    """
    Convert WEBP to target format and upscale.
    Ensures final file size is under max_size_mb.

    Args:
        input_path: Path to input WEBP file
        output_path: Path to save output file
        target_format: Target format ('JPEG' or 'PNG')
        scale_factor: Factor to upscale by (default: 2)
        target_dpi: Target DPI (default: 300)
        max_size_mb: Maximum file size in MB (default: 9.0)

    Returns:
        Dictionary with success status and details
    """
    if not PIL_AVAILABLE:
        return {
            'success': False,
            'error': 'PIL/Pillow is required for this operation'
        }

    try:
        with Image.open(input_path) as img:
            # Upscale by scale factor
            new_size = (img.width * scale_factor, img.height * scale_factor)
            img = img.resize(new_size, Image.Resampling.LANCZOS)

            # Convert to RGB if needed
            if img.mode != "RGB":
                img = img.convert("RGB")

            # Save in target format with DPI
            img.save(output_path, target_format, dpi=(target_dpi, target_dpi))

            # Optimize file size to ensure it's under max_size_mb
            opt_success, opt_message = optimize_file_size(
                output_path,
                max_size_mb,
                quality_range=(90, 20),
                quality_step=10
            )

            if not opt_success:
                print(f"Warning: {opt_message}")

            # Get final file size
            file_size = get_file_size(output_path)
            file_size_mb = file_size / (1024 * 1024)

            return {
                'success': True,
                'original_size': (img.width // scale_factor, img.height // scale_factor),
                'new_size': new_size,
                'format': target_format,
                'dpi': target_dpi,
                'file_size_mb': file_size_mb,
                'optimization': opt_message
            }

    except Exception as e:
        return {'success': False, 'error': str(e)}


def convert_and_upscale_tiff(
    input_path: str,
    output_path: str,
    target_format: str = 'PNG',
    scale_factor: int = 2,
    target_dpi: int = 300,
    remove_original: bool = False,
    max_size_mb: float = 9.0
) -> dict:
    """
    Convert TIFF to target format and upscale.
    Ensures final file size is under max_size_mb.

    Args:
        input_path: Path to input TIFF file
        output_path: Path to save output file
        target_format: Target format ('PNG' or 'JPEG')
        scale_factor: Factor to upscale by (default: 2)
        target_dpi: Target DPI (default: 300)
        remove_original: Whether to remove original file
        max_size_mb: Maximum file size in MB (default: 9.0)

    Returns:
        Dictionary with success status and details
    """
    if not PIL_AVAILABLE:
        return {
            'success': False,
            'error': 'PIL/Pillow is required for this operation'
        }

    try:
        with Image.open(input_path) as img:
            # Upscale by scale factor
            new_size = (img.width * scale_factor, img.height * scale_factor)
            img = img.resize(new_size, Image.Resampling.LANCZOS)

            # Convert to RGB if needed
            if img.mode != "RGB":
                img = img.convert("RGB")

            # Save in target format with DPI
            img.save(output_path, target_format, dpi=(target_dpi, target_dpi))

            # Optimize file size to ensure it's under max_size_mb
            opt_success, opt_message = optimize_file_size(
                output_path,
                max_size_mb,
                quality_range=(90, 20),
                quality_step=10
            )

            if not opt_success:
                print(f"Warning: {opt_message}")

            # Remove original if requested
            if remove_original:
                os.remove(input_path)

            # Get final file size
            file_size = get_file_size(output_path)
            file_size_mb = file_size / (1024 * 1024)

            return {
                'success': True,
                'original_size': (img.width // scale_factor, img.height // scale_factor),
                'new_size': new_size,
                'format': target_format,
                'dpi': target_dpi,
                'original_removed': remove_original,
                'file_size_mb': file_size_mb,
                'optimization': opt_message
            }

    except Exception as e:
        return {'success': False, 'error': str(e)}


def process_directory(
    directory: str,
    source_format: str = 'webp',
    target_format: str = 'JPEG',
    config: Optional[UpscaleConfig] = None,
    remove_original: bool = False
) -> None:
    """
    Process all images of source format in a directory.

    Args:
        directory: Directory to process
        source_format: Source format ('webp', 'tiff', 'tif')
        target_format: Target format ('JPEG' or 'PNG')
        config: UpscaleConfig instance (if None, uses defaults)
        remove_original: Whether to remove original files
    """
    if config is None:
        config = UpscaleConfig()

    if not PIL_AVAILABLE:
        print("❌ PIL/Pillow is required.")
        print("   Please install: pip install Pillow")
        return

    print(f"🖼️  WEB IMAGE UPSCALER v2")
    print("=" * 50)
    print(f"Processing {source_format.upper()} files in: {directory}")
    print(f"Converting to: {target_format}")
    print(f"Upscaling by 2x")
    print(f"Target DPI: {config.target_dpi}")
    print(f"Max file size: {config.max_file_size_mb}MB")
    print("=" * 50)

    successful = 0
    failed = 0

    # Walk through directory
    for root, _, files in os.walk(directory):
        for filename in files:
            source_ext = source_format.lower()
            if filename.lower().endswith(f".{source_ext}"):
                file_path = os.path.join(root, filename)

                # Determine output filename
                if source_format.lower() in ['tiff', 'tif']:
                    new_filename = os.path.splitext(filename)[0] + ".png"
                else:  # webp
                    new_filename = os.path.splitext(filename)[0] + (
                        ".jpg" if target_format == 'JPEG' else ".png"
                    )

                new_file_path = os.path.join(root, new_filename)

                print(f"Processing: {filename}...", end=" ")

                # Process based on source format
                if source_format.lower() in ['tiff', 'tif']:
                    result = convert_and_upscale_tiff(
                        file_path,
                        new_file_path,
                        target_format,
                        scale_factor=2,
                        target_dpi=config.target_dpi,
                        remove_original=remove_original,
                        max_size_mb=config.max_file_size_mb
                    )
                else:  # webp
                    result = convert_and_upscale_webp(
                        file_path,
                        new_file_path,
                        target_format,
                        scale_factor=2,
                        target_dpi=config.target_dpi,
                        max_size_mb=config.max_file_size_mb
                    )

                if result['success']:
                    successful += 1
                    size_info = f" {result['file_size_mb']:.2f}MB" if 'file_size_mb' in result else ""
                    print(f"✅ {result['new_size']}{size_info}")
                    if remove_original and source_format.lower() in ['tiff', 'tif']:
                        print(f"   Removed original: {filename}")
                else:
                    failed += 1
                    print(f"❌ {result['error']}")

    print("\n🎉 PROCESSING COMPLETE!")
    print("=" * 50)
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")


def main():
    """Main function - interactive web image processing."""
    print("🖼️  WEB IMAGE UPSCALER v2")
    print("=" * 50)
    print("Converts and upscales WEBP/TIFF images")
    print("=" * 50)

    # Check if PIL is available
    if not PIL_AVAILABLE:
        print("❌ PIL/Pillow is required.")
        print("   Please install: pip install Pillow")
        return

    # Get directory
    directory = input("Enter the directory path: ").strip()
    if not directory:
        directory = os.getcwd()

    # Get source format
    source_format = input(
        "Source format (webp/tiff) [webp]: "
    ).strip().lower()
    if not source_format:
        source_format = 'webp'

    # Get target format
    target_format = input(
        "Target format (JPEG/PNG) [JPEG]: "
    ).strip().upper()
    if not target_format:
        target_format = 'JPEG'

    # Get remove original option
    remove_original = input(
        "Remove original files? (y/N): "
    ).strip().lower() == 'y'

    # Create config
    config = UpscaleConfig()

    # Process images
    process_directory(directory, source_format, target_format, config, remove_original)


if __name__ == "__main__":
    main()

