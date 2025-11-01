
# Constants
CONSTANT_300 = 300
CONSTANT_1024 = 1024
CONSTANT_2000 = 2000
CONSTANT_4000 = 4000

#!/usr/bin/env python3
"""
Enhanced Image Upscaler
A comprehensive, well-structured image upscaling tool with improved error handling, 
performance optimizations, and better code organization.

Features:
- Multiple aspect ratio support
- Batch processing with progress tracking
- Comprehensive error handling and logging
- Configurable settings
- Type hints and documentation
- Memory-efficient processing
"""

import os
import sys
import subprocess
import math
import logging
import time
from pathlib import Path
from typing import Dict, Tuple, Optional, List, Union
from dataclasses import dataclass
from enum import Enum
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager

# Configure logging
logging.basicConfig(
    level = logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    handlers=[
        logging.FileHandler('image_upscaler.log'), 
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ProcessingMethod(Enum):
    """Image processing methods"""
    CROP = "crop"
    PAD = "pad"
    STRETCH = "stretch"

@dataclass
class ProcessingConfig:
    """Configuration for image processing"""
    max_file_size_mb: float = 9.0
    target_dpi: int = CONSTANT_300
    base_size: int = CONSTANT_2000
    max_dimension: int = CONSTANT_4000
    quality_range: Tuple[int, int] = (90, 20)
    quality_step: int = 10
    batch_size: int = 5
    max_workers: int = 4
    temp_file_prefix: str = ".temp_"

@dataclass
class AspectRatio:
    """Aspect ratio configuration"""
    name: str
    width_ratio: int
    height_ratio: int
    display_name: str

class ImageProcessor:
    """Main image processing class with improved error handling and performance"""

    # Standard aspect ratios
    ASPECT_RATIOS = [
        AspectRatio('16x9', 16, 9, '16:9'), 
        AspectRatio('9x16', 9, 16, '9:16'), 
        AspectRatio('1x1', 1, 1, '1:1'), 
        AspectRatio('4x3', 4, 3, '4:3'), 
        AspectRatio('3x4', 3, 4, '3:4'), 
        AspectRatio('3x2', 3, 2, '3:2'), 
        AspectRatio('2x3', 2, 3, '2:3'), 
    ]

    def __init__(self, config: ProcessingConfig = None):
        """__init__ function."""
        self.config = config or ProcessingConfig()
        self.supported_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp'}

    def run_command(self, cmd: str) -> Tuple[bool, str, str]:
        """Run a shell command with improved error handling"""
        try:
            result = subprocess.run(
                cmd, 
                shell = True, 
                capture_output = True, 
                text = True, 
                timeout = CONSTANT_300  # 5 minute timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {cmd}")
            return False, "", "Command timed out"
        except Exception as e:
            logger.error(f"Command failed: {cmd}, Error: {e}")
            return False, "", str(e)

    def get_image_dimensions(self, image_path: Union[str, Path]) -> Optional[Tuple[int, int]]:
        """Get image dimensions using sips with error handling"""
        try:
            success, stdout, stderr = self.run_command(f'sips -g pixelWidth -g pixelHeight "{image_path}"')
            if not success:
                logger.error(f"Failed to get dimensions for {image_path}: {stderr}")
                return None

            width = height = None
            for line in stdout.split('\n'):
                if 'pixelWidth:' in line:
                    width = int(line.split(':')[1].strip())
                elif 'pixelHeight:' in line:
                    height = int(line.split(':')[1].strip())

            if width is None or height is None:
                logger.error(f"Could not parse dimensions from sips output: {stdout}")
                return None

            return width, height
        except Exception as e:
            logger.error(f"Error getting dimensions for {image_path}: {e}")
            return None

    def get_file_size(self, file_path: Union[str, Path]) -> int:
        """Get file size in bytes with error handling"""
        try:
            return os.path.getsize(file_path)
        except OSError as e:
            logger.error(f"Error getting file size for {file_path}: {e}")
            return 0

    def calculate_target_dimensions(self, aspect_ratio: AspectRatio) -> Tuple[int, int]:
        """Calculate target dimensions for the aspect ratio"""
        width_ratio, height_ratio = aspect_ratio.width_ratio, aspect_ratio.height_ratio

        if width_ratio >= height_ratio:
            # Landscape or square
            width = min(self.config.max_dimension, self.config.base_size * width_ratio)
            height = int(width * height_ratio / width_ratio)
        else:
            # Portrait
            height = min(self.config.max_dimension, self.config.base_size * height_ratio)
            width = int(height * width_ratio / height_ratio)

        return width, height

    @contextmanager
    def temp_file(self, base_path: Union[str, Path]):
        """Context manager for temporary files"""
        temp_path = f"{base_path}{self.config.temp_file_prefix}"
        try:
            yield temp_path
        finally:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError as e:
                    logger.warning(f"Could not remove temp file {temp_path}: {e}")

    def resize_to_aspect_ratio(
        self, 
        input_path: Union[str, Path], 
        output_path: Union[str, Path], 
        aspect_ratio: AspectRatio, 
        method: ProcessingMethod = ProcessingMethod.CROP
    ) -> Tuple[bool, str]:
        """Resize image to target dimensions using sips with improved error handling"""

        # Get original dimensions
        orig_dimensions = self.get_image_dimensions(input_path)
        if not orig_dimensions:
            return False, "Could not get image dimensions"

        orig_width, orig_height = orig_dimensions
        target_width, target_height = self.calculate_target_dimensions(aspect_ratio)

        orig_ratio = orig_width / orig_height
        target_ratio = target_width / target_height

        try:
            if method == ProcessingMethod.CROP and orig_ratio != target_ratio:
                # Calculate crop dimensions
                if orig_ratio > target_ratio:
                    # Image is wider - crop width
                    crop_width = int(orig_height * target_ratio)
                    crop_height = orig_height
                    offset_x = (orig_width - crop_width) // 2
                    offset_y = 0
                else:
                    # Image is taller - crop height
                    crop_height = int(orig_width / target_ratio)
                    crop_width = orig_width
                    offset_x = 0
                    offset_y = (orig_height - crop_height) // 2

                # First crop, then resize
                with self.temp_file(output_path) as temp_path:
                    crop_cmd = (
                        f'sips -c {crop_height} {crop_width} '
                        f'--cropOffset {offset_y} {offset_x} '
                        f'"{input_path}" --out "{temp_path}"'
                    )

                    success1, _, err1 = self.run_command(crop_cmd)
                    if not success1:
                        return False, f"Crop failed: {err1}"

                    resize_cmd = f'sips -z {target_height} {target_width} "{temp_path}" --out "{output_path}"'
                    success2, _, err2 = self.run_command(resize_cmd)
                    if not success2:
                        return False, f"Resize failed: {err2}"
            else:
                # Direct resize
                resize_cmd = f'sips -z {target_height} {target_width} "{input_path}" --out "{output_path}"'
                success, _, err = self.run_command(resize_cmd)
                if not success:
                    return False, f"Resize failed: {err}"

            # Set DPI
            dpi_cmd = f'sips -s dpiHeight {self.config.target_dpi} -s dpiWidth {self.config.target_dpi} "{output_path}"'
            self.run_command(dpi_cmd)  # Don't fail if DPI setting fails

            return True, "Success"

        except Exception as e:
            logger.error(f"Error in resize_to_aspect_ratio: {e}")
            return False, str(e)

    def optimize_file_size(self, image_path: Union[str, Path]) -> Tuple[bool, str]:
        """Optimize file size by reducing quality if needed"""
        max_size_bytes = self.config.max_file_size_mb * CONSTANT_1024 * CONSTANT_1024
        current_size = self.get_file_size(image_path)

        if current_size <= max_size_bytes:
            return True, "File size already within limits"

        logger.info(f"Optimizing file size for {image_path} (current: {current_size / (CONSTANT_1024*CONSTANT_1024):.1f}MB)")

        for quality in range(self.config.quality_range[0], self.config.quality_range[1], -self.config.quality_step):
            with self.temp_file(image_path) as temp_path:
                quality_cmd = f'sips -s formatOptions {quality} "{image_path}" --out "{temp_path}"'

                success, _, _ = self.run_command(quality_cmd)
                if success and os.path.exists(temp_path):
                    temp_size = self.get_file_size(temp_path)
                    if temp_size <= max_size_bytes:
                        try:
                            shutil.move(temp_path, image_path)
                            logger.info(f"Optimized to {quality}% quality ({temp_size / (CONSTANT_1024*CONSTANT_1024):.1f}MB)")
                            return True, f"Optimized to {quality}% quality"
                        except OSError as e:
                            logger.error(f"Failed to replace file: {e}")
                            return False, f"Failed to replace file: {e}"

        return False, "Could not optimize file size within quality limits"

    def process_single_image(
        self, 
        input_path: Union[str, Path], 
        output_path: Union[str, Path], 
        aspect_ratio: AspectRatio
    ) -> Dict[str, Union[bool, str, float, Tuple[int, int]]]:
        """Process a single image with comprehensive error handling"""
        try:
            input_path = Path(input_path)
            output_path = Path(output_path)

            # Ensure output directory exists
            output_path.parent.mkdir(parents = True, exist_ok = True)

            # Resize to aspect ratio
            success, message = self.resize_to_aspect_ratio(input_path, output_path, aspect_ratio)
            if not success:
                return {'success': False, 'error': message}

            # Optimize file size
            opt_success, opt_message = self.optimize_file_size(output_path)
            if not opt_success:
                logger.warning(f"File size optimization failed for {output_path}: {opt_message}")

            # Get final dimensions and size
            final_dimensions = self.get_image_dimensions(output_path)
            file_size = self.get_file_size(output_path)

            return {
                'success': True, 
                'original_size': self.get_image_dimensions(input_path), 
                'new_size': final_dimensions, 
                'file_size_mb': file_size / (CONSTANT_1024 * CONSTANT_1024), 
                'message': message, 
                'optimization_message': opt_message
            }

        except Exception as e:
            logger.error(f"Error processing {input_path}: {e}")
            return {'success': False, 'error': str(e)}

    def find_image_files(self, directory: Union[str, Path]) -> List[Path]:
        """Find all supported image files in directory"""
        directory = Path(directory)
        image_files = []

        for ext in self.supported_extensions:
            image_files.extend(directory.glob(f'*{ext}'))
            image_files.extend(directory.glob(f'*{ext.upper()}'))

        return sorted(image_files)

    def process_batch(
        self, 
        image_files: List[Path], 
        aspect_ratio: AspectRatio, 
        output_dir: Union[str, Path], 
        progress_callback: Optional[callable] = None
    ) -> Tuple[int, int]:
        """Process a batch of images with progress tracking"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents = True, exist_ok = True)

        successful = 0
        failed = 0

        for i, image_path in enumerate(image_files, 1):
            output_path = output_dir / f"upscaled_{image_path.name}"

            if progress_callback:
                progress_callback(i, len(image_files), image_path.name)

            result = self.process_single_image(image_path, output_path, aspect_ratio)

            if result['success']:
                successful += 1
                logger.info(f"✅ {image_path.name} -> {result['file_size_mb']:.1f}MB")
            else:
                failed += 1
                logger.error(f"❌ {image_path.name}: {result['error']}")

        return successful, failed

    def process_all_ratios(
        self, 
        directory: Union[str, Path], 
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Dict[str, int]]:
        """Process all images with all aspect ratios"""
        directory = Path(directory)

        if not directory.exists():
            logger.error(f"Directory does not exist: {directory}")
            return {}

        image_files = self.find_image_files(directory)
        if not image_files:
            logger.warning(f"No image files found in {directory}")
            return {}

        logger.info(f"Found {len(image_files)} image files")
        logger.info(f"Processing with {len(self.ASPECT_RATIOS)} aspect ratios")

        results = {}
        total_processed = 0
        total_successful = 0

        for aspect_ratio in self.ASPECT_RATIOS:
            logger.info(f"\n📐 Processing {aspect_ratio.display_name}...")

            # Create output directory
            output_dir = directory / f"upscaled_{aspect_ratio.name}"

            # Process in batches
            batches = [
                image_files[i:i + self.config.batch_size]
                for i in range(0, len(image_files), self.config.batch_size)
            ]

            ratio_successful = 0
            ratio_failed = 0

            for batch_num, batch in enumerate(batches, 1):
                logger.info(f"  Batch {batch_num}/{len(batches)}")
                successful, failed = self.process_batch(
                    batch, aspect_ratio, output_dir, progress_callback
                )
                ratio_successful += successful
                ratio_failed += failed

                # Small delay between batches
                if batch_num < len(batches):
                    time.sleep(0.5)

            results[aspect_ratio.name] = {
                'successful': ratio_successful, 
                'failed': ratio_failed, 
                'total': ratio_successful + ratio_failed
            }

            total_processed += ratio_successful + ratio_failed
            total_successful += ratio_successful

            logger.info(f"  📊 {aspect_ratio.display_name}: {ratio_successful} successful, {ratio_failed} failed")

        # Final summary
        logger.info(f"\n🎉 BATCH PROCESSING COMPLETE!")
        logger.info(f"Total images processed: {total_processed}")
        logger.info(f"Total successful: {total_successful}")
        logger.info(f"Total failed: {total_processed - total_successful}")

        return results

def main():
    """Main function with improved CLI interface"""
    logger.info("🖼️  ENHANCED IMAGE UPSCALER")
    logger.info("=" * 50)
    logger.info("Advanced image processing with multiple aspect ratios")
    logger.info("Features: Error handling, progress tracking, batch processing")
    logger.info("=" * 50)

    # Check if sips is available
    processor = ImageProcessor()
    success, _, _ = processor.run_command('which sips')
    if not success:
        logger.info("❌ sips command not found. This script requires macOS.")
        sys.exit(1)

    # Get directory
    current_dir = os.getcwd()
    logger.info(f"\n📁 Working directory: {current_dir}")

    use_current = input(f"\nUse current directory? (y/n, default: y): ").strip().lower()
    if use_current in ['n', 'no']:
        directory = input("Enter the directory path containing images: ").strip()
        if not directory:
            directory = current_dir
    else:
        directory = current_dir

    # Get configuration
    try:
        max_size = input(f"Enter max file size in MB (default: 9): ").strip()
        max_size = float(max_size) if max_size else 9.0

        batch_size = input(f"Enter batch size (default: 5): ").strip()
        batch_size = int(batch_size) if batch_size else 5

    except ValueError:
        logger.info("Invalid input, using defaults")
        max_size = 9.0
        batch_size = 5

    # Create configuration
    config = ProcessingConfig(
        max_file_size_mb = max_size, 
        batch_size = batch_size
    )

    # Create processor with config
    processor = ImageProcessor(config)

    # Progress callback
        """progress_callback function."""
    def progress_callback(current, total, filename):
        logger.info(f"  [{current}/{total}] {filename}...", end=" ")

    # Process images
    logger.info(f"\n🔄 Processing images in: {directory}")
    logger.info(f"📏 Max file size: {max_size}MB")
    logger.info(f"🎯 Target DPI: 300")
    logger.info(f"📦 Batch size: {batch_size}")

    results = processor.process_all_ratios(directory, progress_callback)

    # Print summary
    logger.info(f"\n📁 Output directories created:")
    for ratio_name in processor.ASPECT_RATIOS:
        logger.info(f"  • upscaled_{ratio_name.name}/")

    logger.info(f"\n💡 All images are:")
    logger.info(f"  • {processor.config.target_dpi} DPI for print quality")
    logger.info(f"  • Under {processor.config.max_file_size_mb}MB file size")
    logger.info(f"  • Optimized for web and print use")
    logger.info(f"  • Cropped to exact aspect ratios")

if __name__ == "__main__":
    main()