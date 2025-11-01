
# Constants
CONSTANT_300 = 300
CONSTANT_1024 = 1024
CONSTANT_2000 = 2000
CONSTANT_4000 = 4000

#!/usr/bin/env python3
"""
Improved Batch Image Upscaler
Enhanced version with better error handling, progress tracking, and performance optimizations.

Key improvements:
- Comprehensive error handling and logging
- Progress tracking with tqdm
- Memory-efficient processing
- Configurable settings
- Better code organization
- Type hints and documentation
"""

import os
import sys
import subprocess
import math
import logging
import time
from pathlib import Path
from typing import Dict, Tuple, Optional, List, Union, Callable
from dataclasses import dataclass
from enum import Enum
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from datetime import datetime

# Try to import tqdm for progress bars
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    logger.info("Install tqdm for progress bars: pip install tqdm")

# Configure logging
logging.basicConfig(
    level = logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    handlers=[
        logging.FileHandler('batch_upscaler.log'), 
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ProcessingStatus(Enum):
    """Processing status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class ProcessingResult:
    """Result of image processing"""
    status: ProcessingStatus
    input_path: str
    output_path: str
    original_size: Optional[Tuple[int, int]] = None
    new_size: Optional[Tuple[int, int]] = None
    file_size_mb: Optional[float] = None
    error_message: Optional[str] = None
    processing_time: Optional[float] = None

@dataclass
class BatchConfig:
    """Configuration for batch processing"""
    max_file_size_mb: float = 9.0
    target_dpi: int = CONSTANT_300
    base_size: int = CONSTANT_2000
    max_dimension: int = CONSTANT_4000
    quality_range: Tuple[int, int] = (90, 20)
    quality_step: int = 10
    batch_size: int = 5
    max_workers: int = 2  # Conservative for sips
    temp_file_prefix: str = ".temp_"
    save_progress: bool = True
    progress_file: str = "batch_progress.json"

class ImprovedBatchUpscaler:
    """Improved batch upscaler with better error handling and performance"""

    # Standard aspect ratios
    ASPECT_RATIOS = {
        '16x9': (16, 9, '16:9'), 
        '9x16': (9, 16, '9:16'), 
        '1x1': (1, 1, '1:1'), 
        '4x3': (4, 3, '4:3'), 
        '3x4': (3, 4, '3:4'), 
        '3x2': (3, 2, '3:2'), 
        '2x3': (2, 3, '2:3'), 
    }

    def __init__(self, config: BatchConfig = None):
        """__init__ function."""
        self.config = config or BatchConfig()
        self.supported_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp'}
        self.progress_data = self.load_progress()

    def load_progress(self) -> Dict:
        """Load progress from file"""
        if not self.config.save_progress:
            return {}

        try:
            if os.path.exists(self.config.progress_file):
                with open(self.config.progress_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load progress file: {e}")

        return {}

    def save_progress(self, data: Dict):
        """Save progress to file"""
        if not self.config.save_progress:
            return

        try:
            with open(self.config.progress_file, 'w') as f:
                json.dump(data, f, indent = 2)
        except Exception as e:
            logger.warning(f"Could not save progress file: {e}")

    def run_command(self, cmd: str, timeout: int = CONSTANT_300) -> Tuple[bool, str, str]:
        """Run a shell command with improved error handling and timeout"""
        try:
            result = subprocess.run(
                cmd, 
                shell = True, 
                capture_output = True, 
                text = True, 
                timeout = timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out after {timeout}s: {cmd}")
            return False, "", f"Command timed out after {timeout}s"
        except Exception as e:
            logger.error(f"Command failed: {cmd}, Error: {e}")
            return False, "", str(e)

    def get_image_dimensions(self, image_path: Union[str, Path]) -> Optional[Tuple[int, int]]:
        """Get image dimensions using sips with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                success, stdout, stderr = self.run_command(f'sips -g pixelWidth -g pixelHeight "{image_path}"')
                if not success:
                    if attempt < max_retries - 1:
                        time.sleep(1)  # Wait before retry
                        continue
                    logger.error(f"Failed to get dimensions for {image_path}: {stderr}")
                    return None

                width = height = None
                for line in stdout.split('\n'):
                    if 'pixelWidth:' in line:
                        width = int(line.split(':')[1].strip())
                    elif 'pixelHeight:' in line:
                        height = int(line.split(':')[1].strip())

                if width is None or height is None:
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                    logger.error(f"Could not parse dimensions from sips output: {stdout}")
                    return None

                return width, height
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                logger.error(f"Error getting dimensions for {image_path}: {e}")
                return None

        return None

    def get_file_size(self, file_path: Union[str, Path]) -> int:
        """Get file size in bytes with error handling"""
        try:
            return os.path.getsize(file_path)
        except OSError as e:
            logger.error(f"Error getting file size for {file_path}: {e}")
            return 0

    def calculate_target_dimensions(self, width_ratio: int, height_ratio: int) -> Tuple[int, int]:
        """Calculate target dimensions for the aspect ratio"""
        if width_ratio >= height_ratio:
            # Landscape or square
            width = min(self.config.max_dimension, self.config.base_size * width_ratio)
            height = int(width * height_ratio / width_ratio)
        else:
            # Portrait
            height = min(self.config.max_dimension, self.config.base_size * height_ratio)
            width = int(height * width_ratio / height_ratio)

        return width, height

    def resize_to_aspect_ratio(
        self, 
        input_path: Union[str, Path], 
        output_path: Union[str, Path], 
        target_width: int, 
        target_height: int
    ) -> Tuple[bool, str]:
        """Resize image to target dimensions using sips with improved error handling"""

        # Get original dimensions
        orig_dimensions = self.get_image_dimensions(input_path)
        if not orig_dimensions:
            return False, "Could not get image dimensions"

        orig_width, orig_height = orig_dimensions
        orig_ratio = orig_width / orig_height
        target_ratio = target_width / target_height

        try:
            if orig_ratio != target_ratio:
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
                temp_path = f"{output_path}{self.config.temp_file_prefix}"
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

                # Clean up temp file
                try:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                except OSError as e:
                    logger.warning(f"Could not remove temp file {temp_path}: {e}")
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

        logger.debug(f"Optimizing file size for {image_path} (current: {current_size / (CONSTANT_1024*CONSTANT_1024):.1f}MB)")

        for quality in range(self.config.quality_range[0], self.config.quality_range[1], -self.config.quality_step):
            temp_path = f"{image_path}{self.config.temp_file_prefix}"
            quality_cmd = f'sips -s formatOptions {quality} "{image_path}" --out "{temp_path}"'

            success, _, _ = self.run_command(quality_cmd)
            if success and os.path.exists(temp_path):
                temp_size = self.get_file_size(temp_path)
                if temp_size <= max_size_bytes:
                    try:
                        shutil.move(temp_path, image_path)
                        logger.debug(f"Optimized to {quality}% quality ({temp_size / (CONSTANT_1024*CONSTANT_1024):.1f}MB)")
                        return True, f"Optimized to {quality}% quality"
                    except OSError as e:
                        logger.error(f"Failed to replace file: {e}")
                        return False, f"Failed to replace file: {e}"
                else:
                    try:
                        os.remove(temp_path)
                    except OSError:
                        pass

        return False, "Could not optimize file size within quality limits"

    def process_single_image(
        self, 
        input_path: Union[str, Path], 
        output_path: Union[str, Path], 
        aspect_ratio: Tuple[int, int, str]
    ) -> ProcessingResult:
        """Process a single image with comprehensive error handling and timing"""
        start_time = time.time()
        input_path = Path(input_path)
        output_path = Path(output_path)

        # Check if already processed
        progress_key = f"{input_path.name}_{aspect_ratio[2]}"
        if progress_key in self.progress_data:
            result_data = self.progress_data[progress_key]
            if result_data.get('status') == 'success':
                return ProcessingResult(
                    status = ProcessingStatus.SUCCESS, 
                    input_path = str(input_path), 
                    output_path = str(output_path), 
                    original_size = tuple(result_data.get('original_size', [])), 
                    new_size = tuple(result_data.get('new_size', [])), 
                    file_size_mb = result_data.get('file_size_mb'), 
                    processing_time = 0
                )

        try:
            # Ensure output directory exists
            output_path.parent.mkdir(parents = True, exist_ok = True)

            width_ratio, height_ratio, display_name = aspect_ratio
            target_width, target_height = self.calculate_target_dimensions(width_ratio, height_ratio)

            # Resize to aspect ratio
            success, message = self.resize_to_aspect_ratio(input_path, output_path, target_width, target_height)
            if not success:
                result = ProcessingResult(
                    status = ProcessingStatus.FAILED, 
                    input_path = str(input_path), 
                    output_path = str(output_path), 
                    error_message = message, 
                    processing_time = time.time() - start_time
                )
                self.save_result_to_progress(progress_key, result)
                return result

            # Optimize file size
            opt_success, opt_message = self.optimize_file_size(output_path)
            if not opt_success:
                logger.warning(f"File size optimization failed for {output_path}: {opt_message}")

            # Get final dimensions and size
            final_dimensions = self.get_image_dimensions(output_path)
            file_size = self.get_file_size(output_path)

            result = ProcessingResult(
                status = ProcessingStatus.SUCCESS, 
                input_path = str(input_path), 
                output_path = str(output_path), 
                original_size = self.get_image_dimensions(input_path), 
                new_size = final_dimensions, 
                file_size_mb = file_size / (CONSTANT_1024 * CONSTANT_1024), 
                processing_time = time.time() - start_time
            )

            self.save_result_to_progress(progress_key, result)
            return result

        except Exception as e:
            logger.error(f"Error processing {input_path}: {e}")
            result = ProcessingResult(
                status = ProcessingStatus.FAILED, 
                input_path = str(input_path), 
                output_path = str(output_path), 
                error_message = str(e), 
                processing_time = time.time() - start_time
            )
            self.save_result_to_progress(progress_key, result)
            return result

    def save_result_to_progress(self, key: str, result: ProcessingResult):
        """Save result to progress data"""
        self.progress_data[key] = {
            'status': result.status.value, 
            'original_size': list(result.original_size) if result.original_size else None, 
            'new_size': list(result.new_size) if result.new_size else None, 
            'file_size_mb': result.file_size_mb, 
            'error_message': result.error_message, 
            'processing_time': result.processing_time, 
            'timestamp': datetime.now().isoformat()
        }
        self.save_progress(self.progress_data)

    def find_image_files(self, directory: Union[str, Path]) -> List[Path]:
        """Find all supported image files in directory"""
        directory = Path(directory)
        image_files = []

        for ext in self.supported_extensions:
            image_files.extend(directory.glob(f'*{ext}'))
            image_files.extend(directory.glob(f'*{ext.upper()}'))

        return sorted(image_files)

    def process_batch_with_progress(
        self, 
        image_files: List[Path], 
        aspect_ratio: Tuple[int, int, str], 
        output_dir: Union[str, Path], 
        progress_callback: Optional[Callable] = None
    ) -> Tuple[int, int, List[ProcessingResult]]:
        """Process a batch of images with progress tracking"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents = True, exist_ok = True)

        results = []
        successful = 0
        failed = 0

        # Create progress bar if tqdm is available
        if HAS_TQDM:
            progress_bar = tqdm(
                image_files, 
                desc = f"Processing {aspect_ratio[2]}", 
                unit="image"
            )
        else:
            progress_bar = image_files

        for image_path in progress_bar:
            output_path = output_dir / f"upscaled_{image_path.name}"

            if progress_callback:
                progress_callback(image_path.name)

            result = self.process_single_image(image_path, output_path, aspect_ratio)
            results.append(result)

            if result.status == ProcessingStatus.SUCCESS:
                successful += 1
                if HAS_TQDM:
                    progress_bar.set_postfix({
                        'Success': successful, 
                        'Failed': failed, 
                        'Size': f"{result.file_size_mb:.1f}MB" if result.file_size_mb else "N/A"
                    })
                else:
                    logger.info(f"✅ {image_path.name} -> {result.file_size_mb:.1f}MB" if result.file_size_mb else f"✅ {image_path.name}")
            else:
                failed += 1
                if HAS_TQDM:
                    progress_bar.set_postfix({
                        'Success': successful, 
                        'Failed': failed, 
                        'Error': result.error_message[:20] + "..." if result.error_message and len(result.error_message) > 20 else result.error_message
                    })
                else:
                    logger.info(f"❌ {image_path.name}: {result.error_message}")

        return successful, failed, results

    def process_all_ratios(
        self, 
        directory: Union[str, Path], 
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Dict[str, Union[int, List[ProcessingResult]]]]:
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
        logger.info(f"Batch size: {self.config.batch_size}")
        logger.info(f"Max workers: {self.config.max_workers}")

        results = {}
        total_processed = 0
        total_successful = 0

        for ratio_name, aspect_ratio in self.ASPECT_RATIOS.items():
            logger.info(f"\n📐 Processing {aspect_ratio[2]}...")

            # Create output directory
            output_dir = directory / f"upscaled_{ratio_name}"

            # Process in batches
            batches = [
                image_files[i:i + self.config.batch_size]
                for i in range(0, len(image_files), self.config.batch_size)
            ]

            ratio_successful = 0
            ratio_failed = 0
            ratio_results = []

            for batch_num, batch in enumerate(batches, 1):
                logger.info(f"  Batch {batch_num}/{len(batches)} ({len(batch)} images)")

                successful, failed, batch_results = self.process_batch_with_progress(
                    batch, aspect_ratio, output_dir, progress_callback
                )

                ratio_successful += successful
                ratio_failed += failed
                ratio_results.extend(batch_results)

                # Pause between batches to prevent system overload
                if batch_num < len(batches):
                    logger.info(f"  ⏸️  Pausing between batches...")
                    time.sleep(2)

            results[ratio_name] = {
                'successful': ratio_successful, 
                'failed': ratio_failed, 
                'total': ratio_successful + ratio_failed, 
                'results': ratio_results
            }

            total_processed += ratio_successful + ratio_failed
            total_successful += ratio_successful

            logger.info(f"  📊 {aspect_ratio[2]}: {ratio_successful} successful, {ratio_failed} failed")

        # Final summary
        logger.info(f"\n🎉 BATCH PROCESSING COMPLETE!")
        logger.info(f"Total images processed: {total_processed}")
        logger.info(f"Total successful: {total_successful}")
        logger.info(f"Total failed: {total_processed - total_successful}")

        # Save final results
        self.save_progress(self.progress_data)

        return results

def main():
    """Main function with improved CLI interface"""
    logger.info("🖼️  IMPROVED BATCH IMAGE UPSCALER")
    logger.info("=" * 50)
    logger.info("Enhanced batch processing with progress tracking")
    logger.info("Features: Error handling, progress bars, resume capability")
    logger.info("=" * 50)

    # Check if sips is available
    upscaler = ImprovedBatchUpscaler()
    success, _, _ = upscaler.run_command('which sips')
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

        max_workers = input(f"Enter max workers (default: 2): ").strip()
        max_workers = int(max_workers) if max_workers else 2

    except ValueError:
        logger.info("Invalid input, using defaults")
        max_size = 9.0
        batch_size = 5
        max_workers = 2

    # Create configuration
    config = BatchConfig(
        max_file_size_mb = max_size, 
        batch_size = batch_size, 
        max_workers = max_workers
    )

    # Create upscaler with config
    upscaler = ImprovedBatchUpscaler(config)

    # Progress callback
        """progress_callback function."""
    def progress_callback(filename):
        if not HAS_TQDM:
            logger.info(f"Processing {filename}...")

    # Process images
    logger.info(f"\n🔄 Processing images in: {directory}")
    logger.info(f"📏 Max file size: {max_size}MB")
    logger.info(f"🎯 Target DPI: 300")
    logger.info(f"📦 Batch size: {batch_size}")
    logger.info(f"👥 Max workers: {max_workers}")

    results = upscaler.process_all_ratios(directory, progress_callback)

    # Print summary
    logger.info(f"\n📁 Output directories created:")
    for ratio_name in upscaler.ASPECT_RATIOS.keys():
        logger.info(f"  • upscaled_{ratio_name}/")

    logger.info(f"\n💡 All images are:")
    logger.info(f"  • {upscaler.config.target_dpi} DPI for print quality")
    logger.info(f"  • Under {upscaler.config.max_file_size_mb}MB file size")
    logger.info(f"  • Optimized for web and print use")
    logger.info(f"  • Cropped to exact aspect ratios")

    if upscaler.config.save_progress:
        logger.info(f"\n📊 Progress saved to: {upscaler.config.progress_file}")

if __name__ == "__main__":
    main()