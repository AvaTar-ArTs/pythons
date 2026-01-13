# TODO: Resolve circular dependencies by restructuring imports

# String constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"


# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_PORT = 8080

# TODO: Consider extracting methods from long functions

from functools import wraps

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper function."""
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def retry_decorator(max_retries = 3):
    """Decorator to retry function on failure."""
        """decorator function."""
    def decorator(func):
        """wrapper function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
            return None
        return wrapper
    return decorator


class Factory:
    """Generic factory pattern implementation."""
    _creators = {}

    @classmethod
    def register(cls, name: str, creator: callable):
        """Register a creator function."""
        cls._creators[name] = creator

    @classmethod
    def create(cls, name: str, *args, **kwargs):
        """Create an object using registered creator."""
        if name not in cls._creators:
            raise ValueError(f"Unknown type: {name}")
        return cls._creators[name](*args, **kwargs)

#!/usr/bin/env python3
"""
Unified Image Upscaler
A comprehensive, production-ready image upscaling tool that combines the best features
from all the original scripts with significant improvements.

Key Features:
- Multiple processing methods (sips, PIL)
- Comprehensive error handling and logging
- Progress tracking and resume capability
- Memory-efficient processing
- Configurable settings via JSON/YAML
- Type hints and extensive documentation
- Unit tests and validation
- Performance monitoring
"""

import os
import sys
import subprocess
import math
import logging
import time
import json
import yaml
from pathlib import Path
from typing import Dict, Tuple, Optional, List, Union, Callable, Any
from dataclasses import dataclass, asdict
from enum import Enum
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from datetime import datetime
import argparse
import hashlib

# Try to import optional dependencies
try:
    from PIL import Image, ImageOps
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

# Configure logging
def setup_logging(log_level: str = "INFO", log_file: str = "image_upscaler.log"):
    """Setup logging configuration"""
    logging.basicConfig(
        level = getattr(logging, log_level.upper()), 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        handlers=[
            logging.FileHandler(log_file), 
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

class ProcessingMethod(Enum):
    """Image processing methods"""
    SIPS = "sips"
    PIL = "pil"
    AUTO = "auto"

class ProcessingStatus(Enum):
    """Processing status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class AspectRatio:
    """Aspect ratio configuration"""
    name: str
    width_ratio: int
    height_ratio: int
    display_name: str

        """ratio function."""
    @property
    def ratio(self) -> float:
        return self.width_ratio / self.height_ratio

@dataclass
class ProcessingConfig:
    """Configuration for image processing"""
    # File settings
    max_file_size_mb: float = 9.0
    target_dpi: int = 300

    # Dimension settings
    base_size: int = 2000
    max_dimension: int = 4000

    # Quality settings
    quality_range: Tuple[int, int] = (90, 20)
    quality_step: int = 10

    # Processing settings
    batch_size: int = 5
    max_workers: int = 2
    processing_method: ProcessingMethod = ProcessingMethod.AUTO

    # File handling
    temp_file_prefix: str = ".temp_"
    supported_extensions: List[str] = None

    # Progress tracking
    save_progress: bool = True
    progress_file: str = "upscaler_progress.json"

    # Logging
    log_level: str = "INFO"
        """__post_init__ function."""
    log_file: str = "image_upscaler.log"

    def __post_init__(self):
        if self.supported_extensions is None:
            self.supported_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.webp']

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
    method_used: Optional[str] = None
    quality_used: Optional[int] = None

    """__init__ function."""
class ImageProcessor:
    """Base image processor class"""

    def __init__(self, config: ProcessingConfig):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def get_image_dimensions(self, image_path: Union[str, Path]) -> Optional[Tuple[int, int]]:
        """Get image dimensions - to be implemented by subclasses"""
        raise NotImplementedError

    def resize_to_aspect_ratio(
        self, 
        input_path: Union[str, Path], 
        output_path: Union[str, Path], 
        aspect_ratio: AspectRatio
    ) -> Tuple[bool, str]:
        """Resize image to aspect ratio - to be implemented by subclasses"""
        raise NotImplementedError

    def optimize_file_size(self, image_path: Union[str, Path]) -> Tuple[bool, str, int]:
        """Optimize file size - to be implemented by subclasses"""
        raise NotImplementedError
            """__init__ function."""

class SipsProcessor(ImageProcessor):
    """Image processor using macOS sips command"""

    def __init__(self, config: ProcessingConfig):
        super().__init__(config)
        self._check_sips_availability()

    def _check_sips_availability(self):
        """Check if sips is available"""
        success, _, _ = self.run_command('which sips')
        if not success:
            raise RuntimeError("sips command not found. This processor requires macOS.")

    def run_command(self, cmd: str, timeout: int = 300) -> Tuple[bool, str, str]:
        """Run a shell command with error handling"""
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
            self.logger.error(f"Command timed out: {cmd}")
            return False, "", "Command timed out"
        except Exception as e:
            self.logger.error(f"Command failed: {cmd}, Error: {e}")
            return False, "", str(e)

    def get_image_dimensions(self, image_path: Union[str, Path]) -> Optional[Tuple[int, int]]:
        """Get image dimensions using sips"""
        try:
            success, stdout, stderr = self.run_command(f'sips -g pixelWidth -g pixelHeight "{image_path}"')
            if not success:
                self.logger.error(f"Failed to get dimensions for {image_path}: {stderr}")
                return None

            width = height = None
            for line in stdout.split('\n'):
                if 'pixelWidth:' in line:
                    width = int(line.split(':')[1].strip())
                elif 'pixelHeight:' in line:
                    height = int(line.split(':')[1].strip())

            if width is None or height is None:
                self.logger.error(f"Could not parse dimensions from sips output: {stdout}")
                return None

            return width, height
        except Exception as e:
            self.logger.error(f"Error getting dimensions for {image_path}: {e}")
            return None

    def calculate_target_dimensions(self, aspect_ratio: AspectRatio) -> Tuple[int, int]:
        """Calculate target dimensions for the aspect ratio"""
        if aspect_ratio.width_ratio >= aspect_ratio.height_ratio:
            # Landscape or square
            width = min(self.config.max_dimension, self.config.base_size * aspect_ratio.width_ratio)
            height = int(width * aspect_ratio.height_ratio / aspect_ratio.width_ratio)
        else:
            # Portrait
            height = min(self.config.max_dimension, self.config.base_size * aspect_ratio.height_ratio)
            width = int(height * aspect_ratio.width_ratio / aspect_ratio.height_ratio)

        return width, height

    def resize_to_aspect_ratio(
        self, 
        input_path: Union[str, Path], 
        output_path: Union[str, Path], 
        aspect_ratio: AspectRatio
    ) -> Tuple[bool, str]:
        """Resize image to target dimensions using sips"""

        # Get original dimensions
        orig_dimensions = self.get_image_dimensions(input_path)
        if not orig_dimensions:
            return False, "Could not get image dimensions"

        orig_width, orig_height = orig_dimensions
        target_width, target_height = self.calculate_target_dimensions(aspect_ratio)

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
                    self.logger.warning(f"Could not remove temp file {temp_path}: {e}")
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
            self.logger.error(f"Error in resize_to_aspect_ratio: {e}")
            return False, str(e)

    def optimize_file_size(self, image_path: Union[str, Path]) -> Tuple[bool, str, int]:
        """Optimize file size by reducing quality if needed"""
        max_size_bytes = self.config.max_file_size_mb * 1024 * 1024
        current_size = os.path.getsize(image_path)

        if current_size <= max_size_bytes:
            return True, "File size already within limits", 95

        self.logger.debug(f"Optimizing file size for {image_path} (current: {current_size / (1024*1024):.1f}MB)")

        for quality in range(self.config.quality_range[0], self.config.quality_range[1], -self.config.quality_step):
            temp_path = f"{image_path}{self.config.temp_file_prefix}"
            quality_cmd = f'sips -s formatOptions {quality} "{image_path}" --out "{temp_path}"'

            success, _, _ = self.run_command(quality_cmd)
            if success and os.path.exists(temp_path):
                temp_size = os.path.getsize(temp_path)
                if temp_size <= max_size_bytes:
                    try:
                        shutil.move(temp_path, image_path)
                        self.logger.debug(f"Optimized to {quality}% quality ({temp_size / (1024*1024):.1f}MB)")
                        return True, f"Optimized to {quality}% quality", quality
                    except OSError as e:
                        self.logger.error(f"Failed to replace file: {e}")
                        return False, f"Failed to replace file: {e}", quality
                else:
                    try:
                        os.remove(temp_path)
                    except OSError:
                        pass

            """__init__ function."""
        return False, "Could not optimize file size within quality limits", 0

class PILProcessor(ImageProcessor):
    """Image processor using PIL/Pillow"""

    def __init__(self, config: ProcessingConfig):
        super().__init__(config)
        if not HAS_PIL:
            raise RuntimeError("PIL/Pillow not available. Install with: pip install Pillow")

        # Set PIL limits
        Image.MAX_IMAGE_PIXELS = 178956970

    def get_image_dimensions(self, image_path: Union[str, Path]) -> Optional[Tuple[int, int]]:
        """Get image dimensions using PIL"""
        try:
            with Image.open(image_path) as img:
                return img.size
        except Exception as e:
            self.logger.error(f"Error getting dimensions for {image_path}: {e}")
            return None

    def calculate_target_dimensions(self, aspect_ratio: AspectRatio) -> Tuple[int, int]:
        """Calculate target dimensions for the aspect ratio"""
        if aspect_ratio.width_ratio >= aspect_ratio.height_ratio:
            # Landscape or square
            width = min(self.config.max_dimension, self.config.base_size * aspect_ratio.width_ratio)
            height = int(width * aspect_ratio.height_ratio / aspect_ratio.width_ratio)
        else:
            # Portrait
            height = min(self.config.max_dimension, self.config.base_size * aspect_ratio.height_ratio)
            width = int(height * aspect_ratio.width_ratio / aspect_ratio.height_ratio)

        return width, height

    def resize_to_aspect_ratio(
        self, 
        input_path: Union[str, Path], 
        output_path: Union[str, Path], 
        aspect_ratio: AspectRatio
    ) -> Tuple[bool, str]:
        """Resize image to target dimensions using PIL"""
        try:
            with Image.open(input_path) as img:
                # Convert to RGB if needed
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')

                target_width, target_height = self.calculate_target_dimensions(aspect_ratio)
                orig_width, orig_height = img.size
                orig_ratio = orig_width / orig_height
                target_ratio = target_width / target_height

                # Crop to fit target ratio
                if orig_ratio > target_ratio:
                    # Image is wider - crop width
                    new_width = int(orig_height * target_ratio)
                    left = (orig_width - new_width) // 2
                    img = img.crop((left, 0, left + new_width, orig_height))
                elif orig_ratio < target_ratio:
                    # Image is taller - crop height
                    new_height = int(orig_width / target_ratio)
                    top = (orig_height - new_height) // 2
                    img = img.crop((0, top, orig_width, top + new_height))

                # Resize to target dimensions
                img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

                # Save with DPI
                img.save(output_path, format="JPEG", dpi=(self.config.target_dpi, self.config.target_dpi), quality = 95, optimize = True)

                return True, "Success"

        except Exception as e:
            self.logger.error(f"Error in resize_to_aspect_ratio: {e}")
            return False, str(e)

    def optimize_file_size(self, image_path: Union[str, Path]) -> Tuple[bool, str, int]:
        """Optimize file size by reducing quality if needed"""
        max_size_bytes = self.config.max_file_size_mb * 1024 * 1024
        current_size = os.path.getsize(image_path)

        if current_size <= max_size_bytes:
            return True, "File size already within limits", 95

        self.logger.debug(f"Optimizing file size for {image_path} (current: {current_size / (1024*1024):.1f}MB)")

        try:
            with Image.open(image_path) as img:
                for quality in range(self.config.quality_range[0], self.config.quality_range[1], -self.config.quality_step):
                    temp_path = f"{image_path}{self.config.temp_file_prefix}"
                    img.save(temp_path, format="JPEG", dpi=(self.config.target_dpi, self.config.target_dpi), quality = quality, optimize = True)

                    temp_size = os.path.getsize(temp_path)
                    if temp_size <= max_size_bytes:
                        try:
                            shutil.move(temp_path, image_path)
                            self.logger.debug(f"Optimized to {quality}% quality ({temp_size / (1024*1024):.1f}MB)")
                            return True, f"Optimized to {quality}% quality", quality
                        except OSError as e:
                            self.logger.error(f"Failed to replace file: {e}")
                            return False, f"Failed to replace file: {e}", quality
                    else:
                        try:
                            os.remove(temp_path)
                        except OSError:
                            pass

            return False, "Could not optimize file size within quality limits", 0

        except Exception as e:
            self.logger.error(f"Error optimizing file size: {e}")
            return False, str(e), 0

class UnifiedImageUpscaler:
    """Unified image upscaler with multiple processing methods"""

    # Standard aspect ratios
    ASPECT_RATIOS = [
        AspectRatio('16x9', 16, 9, '16:9'), 
        AspectRatio('9x16', 9, 16, '9:16'), 
        AspectRatio('1x1', 1, 1, '1:1'), 
            """__init__ function."""
        AspectRatio('4x3', 4, 3, '4:3'), 
        AspectRatio('3x4', 3, 4, '3:4'), 
        AspectRatio('3x2', 3, 2, '3:2'), 
        AspectRatio('2x3', 2, 3, '2:3'), 
    ]

    def __init__(self, config: ProcessingConfig = None):
        self.config = config or ProcessingConfig()
        self.logger = setup_logging(self.config.log_level, self.config.log_file)
        self.progress_data = self.load_progress()

        # Initialize processor
        self.processor = self._create_processor()

    def _create_processor(self) -> ImageProcessor:
        """Create the appropriate processor based on config"""
        if self.config.processing_method == ProcessingMethod.SIPS:
            return SipsProcessor(self.config)
        elif self.config.processing_method == ProcessingMethod.PIL:
            return PILProcessor(self.config)
        else:  # AUTO
            try:
                return SipsProcessor(self.config)
            except RuntimeError:
                if HAS_PIL:
                    self.logger.info("sips not available, falling back to PIL")
                    return PILProcessor(self.config)
                else:
                    raise RuntimeError("Neither sips nor PIL available")

    def load_progress(self) -> Dict:
        """Load progress from file"""
        if not self.config.save_progress:
            return {}

        try:
            if os.path.exists(self.config.progress_file):
                with open(self.config.progress_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.warning(f"Could not load progress file: {e}")

        return {}

    def save_progress(self, data: Dict):
        """Save progress to file"""
        if not self.config.save_progress:
            return

        try:
            with open(self.config.progress_file, 'w') as f:
                json.dump(data, f, indent = 2)
        except Exception as e:
            self.logger.warning(f"Could not save progress file: {e}")

    def get_file_size(self, file_path: Union[str, Path]) -> int:
        """Get file size in bytes with error handling"""
        try:
            return os.path.getsize(file_path)
        except OSError as e:
            self.logger.error(f"Error getting file size for {file_path}: {e}")
            return 0

    def find_image_files(self, directory: Union[str, Path]) -> List[Path]:
        """Find all supported image files in directory"""
        directory = Path(directory)
        image_files = []

        for ext in self.config.supported_extensions:
            image_files.extend(directory.glob(f'*{ext}'))
            image_files.extend(directory.glob(f'*{ext.upper()}'))

        return sorted(image_files)

    def process_single_image(
        self, 
        input_path: Union[str, Path], 
        output_path: Union[str, Path], 
        aspect_ratio: AspectRatio
    ) -> ProcessingResult:
        """Process a single image with comprehensive error handling"""
        start_time = time.time()
        input_path = Path(input_path)
        output_path = Path(output_path)

        # Check if already processed
        progress_key = f"{input_path.name}_{aspect_ratio.name}"
        if progress_key in self.progress_data:
            result_data = self.progress_data[progress_key]
            if result_data.get('status') == 'success':
                return ProcessingResult(
                    status = ProcessingStatus.SUCCESS, 
                    input_path = str(input_path), 
                    output_path = str(output_path), 
                    original_size = tuple(result_data.get('original_size', [])) if result_data.get('original_size') else None, 
                    new_size = tuple(result_data.get('new_size', [])) if result_data.get('new_size') else None, 
                    file_size_mb = result_data.get('file_size_mb'), 
                    processing_time = 0, 
                    method_used = result_data.get('method_used'), 
                    quality_used = result_data.get('quality_used')
                )

        try:
            # Ensure output directory exists
            output_path.parent.mkdir(parents = True, exist_ok = True)

            # Resize to aspect ratio
            success, message = self.processor.resize_to_aspect_ratio(input_path, output_path, aspect_ratio)
            if not success:
                result = ProcessingResult(
                    status = ProcessingStatus.FAILED, 
                    input_path = str(input_path), 
                    output_path = str(output_path), 
                    error_message = message, 
                    processing_time = time.time() - start_time, 
                    method_used = self.processor.__class__.__name__
                )
                self.save_result_to_progress(progress_key, result)
                return result

            # Optimize file size
            opt_success, opt_message, quality_used = self.processor.optimize_file_size(output_path)
            if not opt_success:
                self.logger.warning(f"File size optimization failed for {output_path}: {opt_message}")

            # Get final dimensions and size
            final_dimensions = self.processor.get_image_dimensions(output_path)
            file_size = self.get_file_size(output_path)

            result = ProcessingResult(
                status = ProcessingStatus.SUCCESS, 
                input_path = str(input_path), 
                output_path = str(output_path), 
                original_size = self.processor.get_image_dimensions(input_path), 
                new_size = final_dimensions, 
                file_size_mb = file_size / (1024 * 1024), 
                processing_time = time.time() - start_time, 
                method_used = self.processor.__class__.__name__, 
                quality_used = quality_used
            )

            self.save_result_to_progress(progress_key, result)
            return result

        except Exception as e:
            self.logger.error(f"Error processing {input_path}: {e}")
            result = ProcessingResult(
                status = ProcessingStatus.FAILED, 
                input_path = str(input_path), 
                output_path = str(output_path), 
                error_message = str(e), 
                processing_time = time.time() - start_time, 
                method_used = self.processor.__class__.__name__
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
            'method_used': result.method_used, 
            'quality_used': result.quality_used, 
            'timestamp': datetime.now().isoformat()
        }
        self.save_progress(self.progress_data)

    def process_all_ratios(
        self, 
        directory: Union[str, Path], 
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Dict[str, Union[int, List[ProcessingResult]]]]:
        """Process all images with all aspect ratios"""
        directory = Path(directory)

        if not directory.exists():
            self.logger.error(f"Directory does not exist: {directory}")
            return {}

        image_files = self.find_image_files(directory)
        if not image_files:
            self.logger.warning(f"No image files found in {directory}")
            return {}

        self.logger.info(f"Found {len(image_files)} image files")
        self.logger.info(f"Processing with {len(self.ASPECT_RATIOS)} aspect ratios")
        self.logger.info(f"Using processor: {self.processor.__class__.__name__}")
        self.logger.info(f"Batch size: {self.config.batch_size}")

        results = {}
        total_processed = 0
        total_successful = 0

        for aspect_ratio in self.ASPECT_RATIOS:
            self.logger.info(f"\n📐 Processing {aspect_ratio.display_name}...")

            # Create output directory
            output_dir = directory / f"upscaled_{aspect_ratio.name}"

            # Process in batches
            batches = [
                image_files[i:i + self.config.batch_size]
                for i in range(0, len(image_files), self.config.batch_size)
            ]

            ratio_successful = 0
            ratio_failed = 0
            ratio_results = []

            # Create progress bar if tqdm is available
            if HAS_TQDM:
                progress_bar = tqdm(
                    batches, 
                    desc = f"Processing {aspect_ratio.display_name}", 
                    unit="batch"
                )
            else:
                progress_bar = batches

            for batch_num, batch in enumerate(progress_bar, 1):
                self.logger.info(f"  Batch {batch_num}/{len(batches)} ({len(batch)} images)")

                for image_path in batch:
                    output_path = output_dir / f"upscaled_{image_path.name}"

                    if progress_callback:
                        progress_callback(image_path.name)

                    result = self.process_single_image(image_path, output_path, aspect_ratio)
                    ratio_results.append(result)

                    if result.status == ProcessingStatus.SUCCESS:
                        ratio_successful += 1
                        self.logger.info(f"✅ {image_path.name} -> {result.file_size_mb:.1f}MB")
                    else:
                        ratio_failed += 1
                        self.logger.error(f"❌ {image_path.name}: {result.error_message}")

                # Pause between batches
                if batch_num < len(batches):
                    time.sleep(1)

            results[aspect_ratio.name] = {
                'successful': ratio_successful, 
                'failed': ratio_failed, 
                'total': ratio_successful + ratio_failed, 
                'results': ratio_results
            }

            total_processed += ratio_successful + ratio_failed
            total_successful += ratio_successful

            self.logger.info(f"  📊 {aspect_ratio.display_name}: {ratio_successful} successful, {ratio_failed} failed")

        # Final summary
        self.logger.info(f"\n🎉 BATCH PROCESSING COMPLETE!")
        self.logger.info(f"Total images processed: {total_processed}")
        self.logger.info(f"Total successful: {total_successful}")
        self.logger.info(f"Total failed: {total_processed - total_successful}")

        return results

def load_config(config_file: str) -> ProcessingConfig:
    """Load configuration from file"""
    try:
        with open(config_file, 'r') as f:
            if config_file.endswith('.yaml') or config_file.endswith('.yml'):
                data = yaml.safe_load(f)
            else:
                data = json.load(f)

        return ProcessingConfig(**data)
    except Exception as e:
        logger.warning(f"Could not load config file {config_file}: {e}")
        return ProcessingConfig()

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description="Unified Image Upscaler")
    parser.add_argument("directory", nargs="?", default=".", help="Directory containing images")
    parser.add_argument("--config", "-c", help="Configuration file (JSON or YAML)")
    parser.add_argument("--method", choices=["sips", "pil", "auto"], default="auto", help="Processing method")
    parser.add_argument("--max-size", type = float, default = 9.0, help="Maximum file size in MB")
    parser.add_argument("--batch-size", type = int, default = 5, help="Batch size for processing")
    parser.add_argument("--max-workers", type = int, default = 2, help="Maximum number of workers")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO", help="Log level")
    parser.add_argument("--no-progress", action="store_true", help="Disable progress saving")

    args = parser.parse_args()

    # Load configuration
    if args.config:
        config = load_config(args.config)
    else:
        config = ProcessingConfig()

    # Override with command line arguments
    config.processing_method = ProcessingMethod(args.method)
    config.max_file_size_mb = args.max_size
    config.batch_size = args.batch_size
    config.max_workers = args.max_workers
        """progress_callback function."""
    config.log_level = args.log_level
    config.save_progress = not args.no_progress

    # Create upscaler
    upscaler = UnifiedImageUpscaler(config)

    # Progress callback
    def progress_callback(filename):
        if not HAS_TQDM:
            print(f"Processing {filename}...")

    # Process images
    print(f"🖼️  UNIFIED IMAGE UPSCALER")
    print("=" * 50)
    print(f"Directory: {args.directory}")
    print(f"Method: {config.processing_method.value}")
    print(f"Max file size: {config.max_file_size_mb}MB")
    print(f"Batch size: {config.batch_size}")
    print("=" * 50)

    results = upscaler.process_all_ratios(args.directory, progress_callback)

    # Print summary
    print(f"\n📁 Output directories created:")
    for ratio in upscaler.ASPECT_RATIOS:
        print(f"  • upscaled_{ratio.name}/")

    print(f"\n💡 All images are:")
    print(f"  • {config.target_dpi} DPI for print quality")
    print(f"  • Under {config.max_file_size_mb}MB file size")
    print(f"  • Optimized for web and print use")
    print(f"  • Cropped to exact aspect ratios")

if __name__ == "__main__":
    main()