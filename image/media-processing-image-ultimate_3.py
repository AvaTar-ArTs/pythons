"""
Media Processing Image Ultimate 3

This module provides functionality for media processing image ultimate 3.

Author: Auto-generated
Date: 2025-11-01
"""


# Constants
CONSTANT_100 = 100
CONSTANT_250 = 250
CONSTANT_300 = 300
CONSTANT_360 = 360
CONSTANT_720 = 720
CONSTANT_768 = 768
CONSTANT_1024 = 1024
CONSTANT_1080 = 1080
CONSTANT_1200 = 1200
CONSTANT_1280 = 1280
CONSTANT_1440 = 1440
CONSTANT_1600 = 1600
CONSTANT_1920 = 1920
CONSTANT_4500 = 4500

#!/usr/bin/env python3
"""
Ultimate Image Processor V2
==========================

Enhanced version that:
- Resizes images larger than 9MB
- Upscales images that don't have CONSTANT_300 DPI
- Maintains aspect ratios and quality
- Provides detailed DPI analysis

Author: AI Assistant
Version: 2.0
"""

import os
import sys
import argparse
import logging
import csv
import math
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum

from PIL import Image, ImageFile, UnidentifiedImageError
from tqdm import tqdm

# Allow PIL to load truncated/corrupted images
ImageFile.LOAD_TRUNCATED_IMAGES = True

class ProcessingMode(Enum):
    """Processing modes for the image processor."""
    RESIZE_ONLY = "resize_only"      # Only resize large images
    UPSCALE_ONLY = "upscale_only"    # Only upscale small images
    DPI_ONLY = "dpi_only"            # Only fix DPI issues
    BOTH = "both"                    # Resize large and upscale small images
    SMART = "smart"                  # Smart processing based on image characteristics
    COMPREHENSIVE = "comprehensive"  # Resize large + upscale small + fix DPI

@dataclass
class ImageConfig:
    """Configuration for image processing."""
    # File size limits
    max_file_size_mb: float = 9.0
    max_file_size_bytes: int = 9 * CONSTANT_1024 * CONSTANT_1024
    
    # Image dimensions
    max_width: int = CONSTANT_4500
    max_height: int = CONSTANT_4500
    
    # DPI settings
    target_dpi: int = CONSTANT_300
    min_dpi_threshold: int = CONSTANT_250  # Consider DPI too low if below this
    
    # Quality settings
    default_quality: int = 85
    min_quality: int = 20
    quality_step: int = 5
    
    # Upscaling
    upscale_multiplier: float = 2.0
    
    # Batch processing
    batch_size: int = 50
    pause_duration: float = 3.0
    
    # Supported formats
    supported_formats: Tuple[str, ...] = (".jpg", ".jpeg", ".png", ".tiff", ".bmp")
    
    # Aspect ratio minimums
    aspect_ratio_minimums: Dict[str, Tuple[int, int]] = None
    
    def __post_init__(self):
        """__post_init__ function."""

        if self.aspect_ratio_minimums is None:
            self.aspect_ratio_minimums = {
                "16:9": (CONSTANT_720, CONSTANT_1280),    # Landscape
                "9:16": (CONSTANT_1080, CONSTANT_1920),   # Portrait
                "1:1": (CONSTANT_1024, CONSTANT_1024),    # Square
                "3:4": (CONSTANT_768, CONSTANT_1024),     # Portrait photography
                "4:3": (CONSTANT_1200, CONSTANT_1600),    # Common screen ratio
                "2:1": (CONSTANT_720, CONSTANT_1440),     # Wide aspect ratio
                "1:2": (CONSTANT_720, CONSTANT_360),      # Tall aspect ratio
            }

class ImageProcessor:
    """Main image processing class."""
    
        """__init__ function."""

    def __init__(self, config: ImageConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.stats = {
            'processed': 0,
            'resized': 0,
            'upscaled': 0,
            'dpi_fixed': 0,
            'skipped': 0,
            'errors': 0
        }
    
    def get_image_dpi(self, image: Image.Image) -> Tuple[float, float]:
        """Get the DPI of an image."""
        dpi = image.info.get('dpi', (72, 72))
        if isinstance(dpi, (int, float)):
            return (float(dpi), float(dpi))
        return (float(dpi[0]), float(dpi[1]))
    
    def needs_dpi_fix(self, image: Image.Image) -> bool:
        """Check if image needs DPI adjustment."""
        dpi_x, dpi_y = self.get_image_dpi(image)
        return dpi_x < self.config.min_dpi_threshold or dpi_y < self.config.min_dpi_threshold
    
    def get_closest_aspect_ratio(self, width: int, height: int) -> Tuple[str, Tuple[int, int]]:
        """Get the closest aspect ratio for given dimensions."""
        aspect_ratios = {
            "16:9": 16 / 9,
            "9:16": 9 / 16,
            "1:1": 1 / 1,
            "3:4": 3 / 4,
            "4:3": 4 / 3,
            "2:1": 2 / 1,
            "1:2": 1 / 2,
        }
        
        current_ratio = width / height
        closest_ratio = min(aspect_ratios, key=lambda ar: abs(current_ratio - aspect_ratios[ar]))
        return closest_ratio, self.config.aspect_ratio_minimums[closest_ratio]
    
    def calculate_new_dimensions(self, width: int, height: int, target_size_mb: float) -> Tuple[int, int]:
        """Calculate new dimensions to achieve target file size."""
        current_ratio = width / height
        target_bytes = target_size_mb * CONSTANT_1024 * CONSTANT_1024
        
        # Estimate compression ratio (rough approximation)
        estimated_compression_ratio = 0.1  # 10% of original size for high quality
        
        # Calculate target pixel count
        target_pixels = target_bytes / estimated_compression_ratio
        
        # Calculate new dimensions maintaining aspect ratio
        new_width = int(math.sqrt(target_pixels * current_ratio))
        new_height = int(new_width / current_ratio)
        
        # Ensure minimum dimensions
        new_width = max(new_width, CONSTANT_100)
        new_height = max(new_height, CONSTANT_100)
        
        return new_width, new_height
    
    def resize_image(self, image: Image.Image, output_path: str, target_size_mb: float = None) -> bool:
        """Resize image to meet size requirements."""
        if target_size_mb is None:
            target_size_mb = self.config.max_file_size_mb
            
        width, height = image.size
        original_size_mb = os.path.getsize(output_path) / (CONSTANT_1024 * CONSTANT_1024) if os.path.exists(output_path) else 0
        
        if original_size_mb <= target_size_mb:
            return True
        
        # Calculate new dimensions
        new_width, new_height = self.calculate_new_dimensions(width, height, target_size_mb)
        
        # Ensure we don't exceed maximum dimensions
        if new_width > self.config.max_width or new_height > self.config.max_height:
            scale_factor = min(self.config.max_width / new_width, self.config.max_height / new_height)
            new_width = int(new_width * scale_factor)
            new_height = int(new_height * scale_factor)
        
        self.logger.info(f"Resizing from {width}x{height} to {new_width}x{new_height}")
        
        # Resize image
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Try different quality levels to achieve target size
        for quality in range(self.config.default_quality, self.config.min_quality - 1, -self.config.quality_step):
            resized_image.save(output_path, dpi=(self.config.target_dpi, self.config.target_dpi), 
                             quality=quality, optimize=True)
            
            current_size_mb = os.path.getsize(output_path) / (CONSTANT_1024 * CONSTANT_1024)
            if current_size_mb <= target_size_mb:
                self.logger.info(f"Successfully resized to {current_size_mb:.2f}MB at quality {quality}")
                return True
        
        self.logger.warning(f"Could not resize below {target_size_mb}MB")
        return False
    
    def upscale_image(self, image: Image.Image, output_path: str) -> bool:
        """Upscale image by the configured multiplier."""
        width, height = image.size
        new_width = int(width * self.config.upscale_multiplier)
        new_height = int(height * self.config.upscale_multiplier)
        
        self.logger.info(f"Upscaling from {width}x{height} to {new_width}x{new_height}")
        
        # Upscale image
        upscaled_image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Convert to RGB if needed for JPEG
        if output_path.lower().endswith(('.jpg', '.jpeg')) and upscaled_image.mode != 'RGB':
            upscaled_image = upscaled_image.convert('RGB')
        
        # Save with high quality and target DPI
        upscaled_image.save(output_path, dpi=(self.config.target_dpi, self.config.target_dpi), 
                           quality=95, optimize=True)
        
        return True
    
    def fix_dpi(self, image: Image.Image, output_path: str) -> bool:
        """Fix DPI without changing image dimensions."""
        dpi_x, dpi_y = self.get_image_dpi(image)
        self.logger.info(f"Fixing DPI from ({dpi_x:.1f}, {dpi_y:.1f}) to ({self.config.target_dpi}, {self.config.target_dpi})")
        
        # Convert to RGB if needed for JPEG
        if output_path.lower().endswith(('.jpg', '.jpeg')) and image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save with target DPI
        image.save(output_path, dpi=(self.config.target_dpi, self.config.target_dpi), 
                  quality=self.config.default_quality, optimize=True)
        
        return True
    
    def process_single_image(self, input_path: str, output_path: str, mode: ProcessingMode) -> Dict:
        """Process a single image based on the specified mode."""
        result = {
            'file': os.path.basename(input_path),
            'status': 'skipped',
            'original_size_mb': 0,
            'final_size_mb': 0,
            'original_dimensions': (0, 0),
            'final_dimensions': (0, 0),
            'original_dpi': (0, 0),
            'final_dpi': (0, 0),
            'error': None
        }
        
        try:
            # Get file size
            original_size_mb = os.path.getsize(input_path) / (CONSTANT_1024 * CONSTANT_1024)
            result['original_size_mb'] = original_size_mb
            
            # Open image
            with Image.open(input_path) as image:
                width, height = image.size
                result['original_dimensions'] = (width, height)
                
                # Get current DPI
                dpi_x, dpi_y = self.get_image_dpi(image)
                result['original_dpi'] = (dpi_x, dpi_y)
                
                # Determine what needs to be done
                needs_resize = original_size_mb > self.config.max_file_size_mb
                needs_dpi_fix = self.needs_dpi_fix(image)
                needs_upscale = False
                
                # Check if upscaling is needed based on mode
                if mode in [ProcessingMode.UPSCALE_ONLY, ProcessingMode.BOTH, ProcessingMode.SMART, ProcessingMode.COMPREHENSIVE]:
                    closest_ratio, (min_width, min_height) = self.get_closest_aspect_ratio(width, height)
                    needs_upscale = width < min_width or height < min_height
                
                # Process based on mode
                if mode == ProcessingMode.RESIZE_ONLY and needs_resize:
                    success = self.resize_image(image, output_path)
                    result['status'] = 'resized' if success else 'error'
                    if success:
                        self.stats['resized'] += 1
                    else:
                        self.stats['errors'] += 1
                        result['error'] = 'Failed to resize'
                        
                elif mode == ProcessingMode.UPSCALE_ONLY and needs_upscale:
                    success = self.upscale_image(image, output_path)
                    result['status'] = 'upscaled' if success else 'error'
                    if success:
                        self.stats['upscaled'] += 1
                    else:
                        self.stats['errors'] += 1
                        result['error'] = 'Failed to upscale'
                        
                elif mode == ProcessingMode.DPI_ONLY and needs_dpi_fix:
                    success = self.fix_dpi(image, output_path)
                    result['status'] = 'dpi_fixed' if success else 'error'
                    if success:
                        self.stats['dpi_fixed'] += 1
                    else:
                        self.stats['errors'] += 1
                        result['error'] = 'Failed to fix DPI'
                        
                elif mode == ProcessingMode.BOTH:
                    if needs_resize:
                        success = self.resize_image(image, output_path)
                        result['status'] = 'resized' if success else 'error'
                        if success:
                            self.stats['resized'] += 1
                        else:
                            self.stats['errors'] += 1
                            result['error'] = 'Failed to resize'
                    elif needs_upscale:
                        success = self.upscale_image(image, output_path)
                        result['status'] = 'upscaled' if success else 'error'
                        if success:
                            self.stats['upscaled'] += 1
                        else:
                            self.stats['errors'] += 1
                            result['error'] = 'Failed to upscale'
                    else:
                        # Just fix DPI if needed
                        if needs_dpi_fix:
                            success = self.fix_dpi(image, output_path)
                            result['status'] = 'dpi_fixed' if success else 'error'
                            if success:
                                self.stats['dpi_fixed'] += 1
                            else:
                                self.stats['errors'] += 1
                                result['error'] = 'Failed to fix DPI'
                        else:
                            # Just copy with DPI setting
                            image.save(output_path, dpi=(self.config.target_dpi, self.config.target_dpi), 
                                      quality=self.config.default_quality, optimize=True)
                            result['status'] = 'processed'
                            self.stats['processed'] += 1
                            
                elif mode == ProcessingMode.SMART:
                    # Smart processing: resize if too large, upscale if too small, fix DPI
                    if needs_resize:
                        success = self.resize_image(image, output_path)
                        result['status'] = 'resized' if success else 'error'
                        if success:
                            self.stats['resized'] += 1
                        else:
                            self.stats['errors'] += 1
                            result['error'] = 'Failed to resize'
                    elif needs_upscale:
                        success = self.upscale_image(image, output_path)
                        result['status'] = 'upscaled' if success else 'error'
                        if success:
                            self.stats['upscaled'] += 1
                        else:
                            self.stats['errors'] += 1
                            result['error'] = 'Failed to upscale'
                    elif needs_dpi_fix:
                        success = self.fix_dpi(image, output_path)
                        result['status'] = 'dpi_fixed' if success else 'error'
                        if success:
                            self.stats['dpi_fixed'] += 1
                        else:
                            self.stats['errors'] += 1
                            result['error'] = 'Failed to fix DPI'
                    else:
                        # Just copy with DPI setting
                        image.save(output_path, dpi=(self.config.target_dpi, self.config.target_dpi), 
                                  quality=self.config.default_quality, optimize=True)
                        result['status'] = 'processed'
                        self.stats['processed'] += 1
                        
                elif mode == ProcessingMode.COMPREHENSIVE:
                    # Comprehensive: do everything needed
                    if needs_resize:
                        success = self.resize_image(image, output_path)
                        if success:
                            result['status'] = 'resized'
                            self.stats['resized'] += 1
                        else:
                            result['status'] = 'error'
                            result['error'] = 'Failed to resize'
                            self.stats['errors'] += 1
                    elif needs_upscale:
                        success = self.upscale_image(image, output_path)
                        if success:
                            result['status'] = 'upscaled'
                            self.stats['upscaled'] += 1
                        else:
                            result['status'] = 'error'
                            result['error'] = 'Failed to upscale'
                            self.stats['errors'] += 1
                    elif needs_dpi_fix:
                        success = self.fix_dpi(image, output_path)
                        if success:
                            result['status'] = 'dpi_fixed'
                            self.stats['dpi_fixed'] += 1
                        else:
                            result['status'] = 'error'
                            result['error'] = 'Failed to fix DPI'
                            self.stats['errors'] += 1
                    else:
                        # Just copy with DPI setting
                        image.save(output_path, dpi=(self.config.target_dpi, self.config.target_dpi), 
                                  quality=self.config.default_quality, optimize=True)
                        result['status'] = 'processed'
                        self.stats['processed'] += 1
                else:
                    # Just copy with DPI setting
                    image.save(output_path, dpi=(self.config.target_dpi, self.config.target_dpi), 
                              quality=self.config.default_quality, optimize=True)
                    result['status'] = 'processed'
                    self.stats['processed'] += 1
                
                # Get final size, dimensions, and DPI
                if os.path.exists(output_path):
                    final_size_mb = os.path.getsize(output_path) / (CONSTANT_1024 * CONSTANT_1024)
                    result['final_size_mb'] = final_size_mb
                    
                    with Image.open(output_path) as final_image:
                        result['final_dimensions'] = final_image.size
                        final_dpi_x, final_dpi_y = self.get_image_dpi(final_image)
                        result['final_dpi'] = (final_dpi_x, final_dpi_y)
                
        except UnidentifiedImageError:
            result['status'] = 'error'
            result['error'] = 'Cannot identify image format'
            self.stats['errors'] += 1
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
            self.stats['errors'] += 1
            self.logger.error(f"Error processing {input_path}: {e}")
        
        if result['status'] == 'skipped':
            self.stats['skipped'] += 1
        
        return result
    
    def process_directory(self, input_dir: str, output_dir: str, mode: ProcessingMode) -> List[Dict]:
        """Process all images in a directory."""
        results = []
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        if not input_path.exists():
            self.logger.error(f"Input directory does not exist: {input_dir}")
            return results
        
        # Create output directory
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Find all image files
        image_files = []
        for ext in self.config.supported_formats:
            image_files.extend(input_path.rglob(f"*{ext}"))
            image_files.extend(input_path.rglob(f"*{ext.upper()}"))
        
        if not image_files:
            self.logger.warning(f"No supported image files found in {input_dir}")
            return results
        
        self.logger.info(f"Found {len(image_files)} image files to process")
        
        # Process images in batches
        for i in range(0, len(image_files), self.config.batch_size):
            batch = image_files[i:i + self.config.batch_size]
            
            for image_file in tqdm(batch, desc=f"Processing batch {i//self.config.batch_size + 1}"):
                # Calculate relative path and create output subdirectory
                rel_path = image_file.relative_to(input_path)
                output_file = output_path / rel_path
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Process the image
                result = self.process_single_image(str(image_file), str(output_file), mode)
                results.append(result)
            
            # Pause between batches
            if i + self.config.batch_size < len(image_files):
                time.sleep(self.config.pause_duration)
        
        return results

def setup_logging(log_file: Optional[str] = None, verbose: bool = False) -> logging.Logger:
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    
    # Create logger
    logger = logging.getLogger('image_processor')
    logger.setLevel(level)
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def save_results_csv(results: List[Dict], output_file: str):
    """Save processing results to CSV file."""
    if not results:
        return
    
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['file', 'status', 'original_size_mb', 'final_size_mb', 
                     'original_dimensions', 'final_dimensions', 'original_dpi', 'final_dpi', 'error']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Ultimate Image Processor V2 - Resize, upscale, and fix DPI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Comprehensive processing (resize large + upscale small + fix DPI)
  python ultimate_image_processor_v2.py input_dir output_dir --mode comprehensive
  
  # Resize large images only
  python ultimate_image_processor_v2.py input_dir output_dir --mode resize_only
  
  # Fix DPI issues only
  python ultimate_image_processor_v2.py input_dir output_dir --mode dpi_only
  
  # Smart processing based on image characteristics
  python ultimate_image_processor_v2.py input_dir output_dir --mode smart
        """
    )
    
    parser.add_argument('input_dir', help='Input directory containing images')
    parser.add_argument('output_dir', help='Output directory for processed images')
    parser.add_argument('--mode', choices=[m.value for m in ProcessingMode], 
                       default=ProcessingMode.COMPREHENSIVE.value,
                       help='Processing mode (default: comprehensive)')
    parser.add_argument('--max-size', type=float, default=9.0,
                       help='Maximum file size in MB (default: 9.0)')
    parser.add_argument('--upscale-factor', type=float, default=2.0,
                       help='Upscale multiplier (default: 2.0)')
    parser.add_argument('--batch-size', type=int, default=50,
                       help='Batch size for processing (default: 50)')
    parser.add_argument('--dpi', type=int, default=CONSTANT_300,
                       help='Target DPI (default: CONSTANT_300)')
    parser.add_argument('--min-dpi', type=int, default=CONSTANT_250,
                       help='Minimum DPI threshold (default: CONSTANT_250)')
    parser.add_argument('--log-file', help='Log file path')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--csv-output', help='Save results to CSV file')
    
    args = parser.parse_args()
    
    # Set up logging
    logger = setup_logging(args.log_file, args.verbose)
    
    # Create configuration
    config = ImageConfig(
        max_file_size_mb=args.max_size,
        max_file_size_bytes=int(args.max_size * CONSTANT_1024 * CONSTANT_1024),
        upscale_multiplier=args.upscale_factor,
        batch_size=args.batch_size,
        target_dpi=args.dpi,
        min_dpi_threshold=args.min_dpi
    )
    
    # Create processor
    processor = ImageProcessor(config, logger)
    
    # Process images
    logger.info(f"Starting image processing: {args.input_dir} -> {args.output_dir}")
    logger.info(f"Mode: {args.mode}, Max size: {args.max_size}MB, Upscale: {args.upscale_factor}x, Target DPI: {args.dpi}")
    
    mode = ProcessingMode(args.mode)
    results = processor.process_directory(args.input_dir, args.output_dir, mode)
    
    # Print statistics
    logger.info("Processing complete!")
    logger.info(f"Processed: {processor.stats['processed']}")
    logger.info(f"Resized: {processor.stats['resized']}")
    logger.info(f"Upscaled: {processor.stats['upscaled']}")
    logger.info(f"DPI Fixed: {processor.stats['dpi_fixed']}")
    logger.info(f"Skipped: {processor.stats['skipped']}")
    logger.info(f"Errors: {processor.stats['errors']}")
    
    # Save results to CSV if requested
    if args.csv_output:
        save_results_csv(results, args.csv_output)
        logger.info(f"Results saved to: {args.csv_output}")

if __name__ == '__main__':
    main()