"""
Core image processing utilities shared across all upscaling scripts.

This module provides platform-agnostic utilities for image processing,
automatically detecting and using the best available image processor
(sips on macOS, PIL/Pillow as fallback).
"""

import functools
import platform
import shutil
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Literal, Optional, Tuple

try:
    from PIL import Image, ImageOps

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from .exceptions import (
    DimensionError,
    ImageFileNotFoundError,
    ProcessorNotFoundError,
)


# Platform detection
@functools.lru_cache(maxsize=1)
def get_image_processor() -> Literal["sips", "pil", None]:
    '\''
    Detect available image processor.

    Returns:
        'sips' if macOS sips is available
        'pil' if PIL/Pillow is available
        None if no processor is available

    Raises:
        ProcessorNotFoundError: If no image processor is available
    """
    # Check for sips (macOS)
    if platform.system() == "Darwin":
        try:
            result = subprocess.run(
                ["which", "sips"], capture_output=True, text=True, check=False
            )
            if result.returncode == 0:
                return "sips"
        except Exception:
            pass

    # Check for PIL/Pillow
    if PIL_AVAILABLE:
        return "pil"

    return None


@contextmanager
def temp_file(base_path: str):
    """
    Context manager for temporary files with automatic cleanup.

    Args:
        base_path: Base path for the temporary file

    Yields:
        Path to temporary file
    """
    temp_path = f"{base_path}.temp"
    try:
        yield temp_path
    finally:
        temp_path_obj = Path(temp_path)
        if temp_path_obj.exists():
            temp_path_obj.unlink()


def supports_webp() -> bool:
    """
    Check if WebP format is supported.

    Returns:
        True if WebP is supported, False otherwise
    """
    if PIL_AVAILABLE:
        try:
            return "WEBP" in Image.SUPPORTED
        except AttributeError:
            # Older PIL versions
            return hasattr(Image, "WEBP")
    return False


def run_command(cmd: str) -> Tuple[bool, str, str]:
    """
    Run a shell command and return the result.

    Args:
        cmd: Shell command to execute

    Returns:
        Tuple of (success, stdout, stderr)
    """
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def get_image_dimensions(:
    image_path: str, processor: Optional[str] = None
) -> Tuple[int, int]:
    """
    Get image dimensions (width, height).

    Args:
        image_path: Path to the image file
        processor: Image processor to use ('sips' or 'pil').
                   If None, auto-detects.

    Returns:
        Tuple of (width, height) in pixels

    Raises:
        ImageFileNotFoundError: If image file doesn't exist
        DimensionError: If dimensions cannot be determined
    '\''
    image_path_obj = Path(image_path)
    if not image_path_obj.exists():
        raise ImageFileNotFoundError(f"Image file not found: {image_path}")

    if processor is None:
        processor = get_image_processor()

    if processor == "sips":
        success, stdout, stderr = run_command(
            f'sips -g pixelWidth -g pixelHeight "{image_path}"'
        )
        if not success:
            raise DimensionError(f"Failed to get dimensions: {stderr}")

        width = None
        height = None

        for line in stdout.split("\n"):
            if "pixelWidth:" in line:
                width = int(line.split(":")[1].strip())
            elif "pixelHeight:" in line:
                height = int(line.split(":")[1].strip())

        if width is None or height is None:
            raise DimensionError("Could not parse dimensions from sips output")

        return width, height

    elif processor == "pil":
        if not PIL_AVAILABLE:
            raise ProcessorNotFoundError("PIL/Pillow is not available")

        try:
            with Image.open(image_path) as img:
                return img.size  # Returns (width, height)
        except Exception as e:
            raise DimensionError(f"Failed to get dimensions with PIL: {e}") from e

    else:
        raise ProcessorNotFoundError("No image processor available")


def get_file_size(image_path: str) -> int:
    '\''
    Get file size in bytes.

    Args:
        image_path: Path to the file

    Returns:
        File size in bytes (0 if file doesn't exist)
    """
    try:
        return Path(image_path).stat().st_size
    except OSError:
        return 0


def calculate_target_dimensions(:
    width_ratio: int,
    height_ratio: int,
    base_size: int = 2000,
    max_dimension: int = 4000,
) -> Tuple[int, int]:
    """
    Calculate target dimensions for the given aspect ratio.

    Args:
        width_ratio: Width component of aspect ratio
        height_ratio: Height component of aspect ratio
        base_size: Base size for calculations
        max_dimension: Maximum dimension (width or height)

    Returns:
        Tuple of (target_width, target_height)
    """
    if width_ratio >= height_ratio:
        # Landscape or square
        width = min(max_dimension, base_size * width_ratio)
        height = int(width * height_ratio / width_ratio)
    else:
        # Portrait
        height = min(max_dimension, base_size * height_ratio)
        width = int(height * width_ratio / height_ratio)

    return width, height


def resize_to_aspect_ratio(:
    input_path: str,
    output_path: str,
    target_width: int,
    target_height: int,
    processor: Optional[str] = None,
    method: str = "crop",
) -> Tuple[bool, str]:
    """
    Resize image to target dimensions with aspect ratio handling.

    Args:
        input_path: Path to input image
        output_path: Path to save output image
        target_width: Target width in pixels
        target_height: Target height in pixels
        processor: Image processor to use ('sips' or 'pil').
                   If None, auto-detects.
        method: Resize method ('crop', 'pad', or 'stretch').
                Default: 'crop'

    Returns:
        Tuple of (success, message)

    Raises:
        ResizeError: If resize operation fails
    """
    if processor is None:
        processor = get_image_processor()

    if processor == "sips":
        return _resize_with_sips(
            input_path, output_path, target_width, target_height, method
        )
    elif processor == "pil":
        return _resize_with_pil(
            input_path, output_path, target_width, target_height, method
        )
    else:
        raise ProcessorNotFoundError("No image processor available")


def _resize_with_sips(:
    input_path: str,
    output_path: str,
    target_width: int,
    target_height: int,
    method: str,
) -> Tuple[bool, str]:
    """Resize image using macOS sips command.'\''
    # Get original dimensions
    try:
        orig_width, orig_height = get_image_dimensions(input_path, "sips")
    except Exception as e:
        return False, f"Could not get image dimensions: {e}"

    orig_ratio = orig_width / orig_height
    target_ratio = target_width / target_height

    # Calculate crop dimensions
    if method == "crop":
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
        with temp_file(output_path) as temp_path:
            crop_cmd = (
                f"sips -c {crop_height_final} {crop_width_final} "
                f'-cOffset {crop_y} {crop_x} "{input_path}" '
                f'--out "{temp_path}"'
            )
            resize_cmd = (
                f'sips -z {target_height} {target_width} "{temp_path}" '
                f'--out "{output_path}"'
            )

            # Execute crop
            success1, _, err1 = run_command(crop_cmd)
            if not success1:
                return False, f"Crop failed: {err1}"

            # Execute resize
            success2, _, err2 = run_command(resize_cmd)
            if not success2:
                return False, f"Resize failed: {err2}"

    elif method == "stretch":
        # Direct resize without cropping
        resize_cmd = (
            f'sips -z {target_height} {target_width} "{input_path}" '
            f'--out "{output_path}"'
        )
        success, _, err = run_command(resize_cmd)
        if not success:
            return False, f"Resize failed: {err}"

    else:  # pad method not easily supported with sips
        # Fallback to stretch for sips
        resize_cmd = (
            f'sips -z {target_height} {target_width} "{input_path}" '
            f'--out "{output_path}"'
        )
        success, _, err = run_command(resize_cmd)
        if not success:
            return False, f"Resize failed: {err}"

    # Set DPI to 300
    dpi_cmd = f'sips -s dpiHeight 300 -s dpiWidth 300 "{output_path}"'
    run_command(dpi_cmd)

    return True, "Success"


def _resize_with_pil(:
    input_path: str,
    output_path: str,
    target_width: int,
    target_height: int,
    method: str,
) -> Tuple[bool, str]:
    """Resize image using PIL/Pillow."""
    if not PIL_AVAILABLE:
        return False, "PIL/Pillow is not available"

    try:
        with Image.open(input_path) as image:
            # Convert to RGB if needed
            if image.mode in ("RGBA", "LA", "P"):
                image = image.convert("RGB")

            original_width, original_height = image.size
            original_ratio = original_width / original_height
            target_ratio = target_width / target_height

            if method == "crop":
                # Crop to fit target ratio
                if original_ratio > target_ratio:
                    # Image is wider - crop width
                    new_width = int(original_height * target_ratio)
                    left = (original_width - new_width) // 2
                    image = image.crop((left, 0, left + new_width, original_height))
                elif original_ratio < target_ratio:
                    # Image is taller - crop height
                    new_height = int(original_width / target_ratio)
                    top = (original_height - new_height) // 2
                    image = image.crop((0, top, original_width, top + new_height))

                resized = image.resize(
                    (target_width, target_height), Image.Resampling.LANCZOS
                )

            elif method == "pad":
                # Pad to fit target ratio
                if original_ratio > target_ratio:
                    # Image is wider - pad height
                    new_height = int(original_width / target_ratio)
                    padding = (new_height - original_height) // 2
                    image = ImageOps.expand(
                        image, (0, padding, 0, padding), fill="white"
                    )
                elif original_ratio < target_ratio:
                    # Image is taller - pad width
                    new_width = int(original_height * target_ratio)
                    padding = (new_width - original_width) // 2
                    image = ImageOps.expand(
                        image, (padding, 0, padding, 0), fill="white"
                    )

                resized = image.resize(
                    (target_width, target_height), Image.Resampling.LANCZOS
                )

            else:  # stretch
                resized = image.resize(
                    (target_width, target_height), Image.Resampling.LANCZOS
                )

            # Save with 300 DPI
            resized.save(output_path, dpi=(300, 300))
            return True, "Success"

    except Exception as e:
        return False, f"PIL resize failed: {e}"


def optimize_file_size(:
    image_path: str,
    max_size_mb: float = 9.0,
    processor: Optional[str] = None,
    quality_range: Tuple[int, int] = (90, 20),
    quality_step: int = 10,
) -> Tuple[bool, str]:
    '\''
    Optimize file size by reducing quality if needed.

    Args:
        image_path: Path to the image file
        max_size_mb: Maximum file size in megabytes
        processor: Image processor to use ('sips' or 'pil').
                   If None, auto-detects.
        quality_range: Tuple of (max_quality, min_quality)
        quality_step: Step size for quality reduction

    Returns:
        Tuple of (success, message)
    '\''
    max_size_bytes = max_size_mb * 1024 * 1024

    # Check current file size
    if current_size <= max_size_bytes:
        return True, "File size already within limits"

    if processor is None:
        processor = get_image_processor()

    if processor == "sips":
        # Try different quality levels
        max_quality, min_quality = quality_range
        with temp_file(image_path) as temp_path:
            for quality in range(max_quality, min_quality - 1, -quality_step):
                quality_cmd = (
                    f'sips -s formatOptions {quality} "{image_path}" '
                    f'--out "{temp_path}"'
                )

                success, _, _ = run_command(quality_cmd)
                temp_path_obj = Path(temp_path)
                if success and temp_path_obj.exists():
                    temp_size = get_file_size(temp_path)
                    if temp_size <= max_size_bytes:
                        # Replace original with optimized version
                        shutil.move(temp_path, image_path)
                        return True, f"Optimized to {quality}% quality"

        return False, "Could not optimize file size"

    elif processor == "pil":
        if not PIL_AVAILABLE:
            return False, "PIL/Pillow is not available"

        try:
            with Image.open(image_path) as image:
                # Convert to RGB if needed
                if image.mode in ("RGBA", "LA", "P"):
                    image = image.convert("RGB")

                max_quality, min_quality = quality_range
                with temp_file(image_path) as temp_path:
                    for quality in range(max_quality, min_quality - 1, -quality_step):
                        image.save(
                            temp_path, format="JPEG", quality=quality, optimize=True
                        )
                        temp_size = get_file_size(temp_path)

                        if temp_size <= max_size_bytes:
                            # Replace original with optimized version
                            shutil.move(temp_path, image_path)
                            return True, f"Optimized to {quality}% quality"

                return False, "Could not optimize file size"

        except Exception as e:
            return False, f"PIL optimization failed: {e}"

    else:
        return False, "No image processor available"
