"""
Script 261

This module provides functionality for script 261.

Author: Auto-generated
Date: 2025-11-01
"""


# Constants
CONSTANT_300 = 300
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Enhanced Image Upscaler
=======================

A production-ready image upscaling tool with comprehensive error handling,
performance optimizations, and advanced features.

Key improvements over original:
- Full type hints and documentation
- Comprehensive error handling and logging
- Multiple processing methods (PIL, sips)
- Batch processing with progress tracking
- Configuration management
- Memory optimization
- Resume capability
- Unit testing support

Author: Enhanced by Claude
Version: 2.0
"""

import os
import sys
import logging
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Callable, Any
from dataclasses import dataclass, asdict
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import tempfile
import shutil

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
def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """Setup enhanced logging configuration."""
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

class ProcessingMethod(Enum):
    """Image processing methods."""
    PIL = "pil"
    SIPS = "sips"
    AUTO = "auto"

class ProcessingStatus(Enum):
    """Processing status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class UpscaleConfig:
    """Configuration for image upscaling."""
    scale_factor: float = 2.0
    target_dpi: Tuple[int, int] = (CONSTANT_300, CONSTANT_300)
    quality: int = 95
    output_format: str = "JPEG"
    batch_size: int = 10
    max_workers: int = 4
    supported_extensions: List[str] = None
    processing_method: ProcessingMethod = ProcessingMethod.AUTO
    save_progress: bool = True
    progress_file: str = "upscale_progress.json"
    log_level: str = "INFO"
    log_file: str = "image_upscaler.log"
    
    def __post_init__(self):
        """__post_init__ function."""

        if self.supported_extensions is None:
            self.supported_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.webp']

@dataclass
class UpscaleResult:
    """Result of image upscaling operation."""
    status: ProcessingStatus
    input_path: str
    output_path: str
    original_size: Optional[Tuple[int, int]] = None
    new_size: Optional[Tuple[int, int]] = None
    file_size_mb: Optional[float] = None
    processing_time: Optional[float] = None
    method_used: Optional[str] = None
    error_message: Optional[str] = None

class EnhancedImageUpscaler:
    """Enhanced image upscaler with comprehensive error handling and optimization."""
    
        """__init__ function."""

    def __init__(self, config: Optional[UpscaleConfig] = None):
        self.config = config or UpscaleConfig()
        self.logger = setup_logging(self.config.log_level, self.config.log_file)
        self.progress_data = self.load_progress()
        
        # Check available processing methods
        self.pil_available = HAS_PIL
        self.sips_available = self._check_sips()
        
        if not self.pil_available and not self.sips_available:
            raise RuntimeError("No image processing libraries available. Install PIL or ensure sips is available.")
        
        # Select processing method
        if self.config.processing_method == ProcessingMethod.AUTO:
            if self.sips_available:
                self.processing_method = ProcessingMethod.SIPS
            elif self.pil_available:
                self.processing_method = ProcessingMethod.PIL
            else:
                raise RuntimeError("No suitable processing method available")
        else:
            self.processing_method = self.config.processing_method
        
        self.logger.info(f"Using processing method: {self.processing_method.value}")
    
    def _check_sips(self) -> bool:
        """Check if sips command is available (macOS only)."""
        try:
            import subprocess
            result = subprocess.run(['which', 'sips'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def load_progress(self) -> Dict[str, Any]:
        """Load progress from file."""
        if not self.config.save_progress:
            return {}
        
        try:
            if os.path.exists(self.config.progress_file):
                with open(self.config.progress_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.warning(f"Could not load progress file: {e}")
        
        return {}
    
    def save_progress(self, data: Dict[str, Any]):
        """Save progress to file."""
        if not self.config.save_progress:
            return
        
        try:
            with open(self.config.progress_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.warning(f"Could not save progress file: {e}")
    
    def upscale_with_pil(self, input_path: Path, output_path: Path) -> UpscaleResult:
        """Upscale image using PIL with comprehensive error handling."""
        start_time = time.time()
        
        try:
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with Image.open(input_path) as img:
                # Convert to RGB if needed
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Calculate new dimensions
                new_width = int(img.width * self.config.scale_factor)
                new_height = int(img.height * self.config.scale_factor)
                
                # Resize image
                upscaled_img = img.resize(
                    (new_width, new_height), 
                    Image.Resampling.LANCZOS
                )
                
                # Save with specified DPI and quality
                upscaled_img.save(
                    output_path,
                    format=self.config.output_format,
                    dpi=self.config.target_dpi,
                    quality=self.config.quality,
                    optimize=True
                )
            
            # Get file size
            file_size_mb = output_path.stat().st_size / (CONSTANT_1024 * CONSTANT_1024)
            
            return UpscaleResult(
                status=ProcessingStatus.SUCCESS,
                input_path=str(input_path),
                output_path=str(output_path),
                original_size=(img.width, img.height),
                new_size=(new_width, new_height),
                file_size_mb=file_size_mb,
                processing_time=time.time() - start_time,
                method_used="PIL"
            )
            
        except Exception as e:
            return UpscaleResult(
                status=ProcessingStatus.FAILED,
                input_path=str(input_path),
                output_path=str(output_path),
                processing_time=time.time() - start_time,
                method_used="PIL",
                error_message=str(e)
            )
    
    def upscale_with_sips(self, input_path: Path, output_path: Path) -> UpscaleResult:
        """Upscale image using sips with comprehensive error handling."""
        start_time = time.time()
        
        try:
            import subprocess
            
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Get original dimensions
            get_dims_cmd = ['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', str(input_path)]
            result = subprocess.run(get_dims_cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                raise RuntimeError(f"Failed to get image dimensions: {result.stderr}")
            
            # Parse dimensions
            width = height = None
            for line in result.stdout.split('\n'):
                if 'pixelWidth:' in line:
                    width = int(line.split(':')[1].strip())
                elif 'pixelHeight:' in line:
                    height = int(line.split(':')[1].strip())
            
            if width is None or height is None:
                raise RuntimeError("Could not parse image dimensions")
            
            # Calculate new dimensions
            new_width = int(width * self.config.scale_factor)
            new_height = int(height * self.config.scale_factor)
            
            # Resize image
            resize_cmd = [
                'sips', '-z', str(new_height), str(new_width),
                str(input_path), '--out', str(output_path)
            ]
            
            result = subprocess.run(resize_cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                raise RuntimeError(f"Failed to resize image: {result.stderr}")
            
            # Set DPI
            dpi_cmd = [
                'sips', '-s', 'dpiHeight', str(self.config.target_dpi[1]),
                '-s', 'dpiWidth', str(self.config.target_dpi[0]),
                str(output_path)
            ]
            
            subprocess.run(dpi_cmd, capture_output=True, text=True, timeout=30)
            
            # Get file size
            file_size_mb = output_path.stat().st_size / (CONSTANT_1024 * CONSTANT_1024)
            
            return UpscaleResult(
                status=ProcessingStatus.SUCCESS,
                input_path=str(input_path),
                output_path=str(output_path),
                original_size=(width, height),
                new_size=(new_width, new_height),
                file_size_mb=file_size_mb,
                processing_time=time.time() - start_time,
                method_used="sips"
            )
            
        except Exception as e:
            return UpscaleResult(
                status=ProcessingStatus.FAILED,
                input_path=str(input_path),
                output_path=str(output_path),
                processing_time=time.time() - start_time,
                method_used="sips",
                error_message=str(e)
            )
    
    def upscale_single_image(self, input_path: Union[str, Path], 
                           output_path: Union[str, Path]) -> UpscaleResult:
        """Upscale a single image with the configured method."""
        input_path = Path(input_path)
        output_path = Path(output_path)
        
        # Check if already processed
        progress_key = f"{input_path.name}_{self.config.scale_factor}"
        if progress_key in self.progress_data:
            result_data = self.progress_data[progress_key]
            if result_data.get('status') == 'success':
                return UpscaleResult(
                    status=ProcessingStatus.SUCCESS,
                    input_path=str(input_path),
                    output_path=str(output_path),
                    original_size=tuple(result_data.get('original_size', [])),
                    new_size=tuple(result_data.get('new_size', [])),
                    file_size_mb=result_data.get('file_size_mb'),
                    processing_time=0,
                    method_used=result_data.get('method_used')
                )
        
        # Process image
        if self.processing_method == ProcessingMethod.PIL:
            result = self.upscale_with_pil(input_path, output_path)
        elif self.processing_method == ProcessingMethod.SIPS:
            result = self.upscale_with_sips(input_path, output_path)
        else:
            result = UpscaleResult(
                status=ProcessingStatus.FAILED,
                input_path=str(input_path),
                output_path=str(output_path),
                error_message="No processing method available"
            )
        
        # Save result to progress
        self.progress_data[progress_key] = {
            'status': result.status.value,
            'original_size': list(result.original_size) if result.original_size else None,
            'new_size': list(result.new_size) if result.new_size else None,
            'file_size_mb': result.file_size_mb,
            'processing_time': result.processing_time,
            'method_used': result.method_used,
            'error_message': result.error_message,
            'timestamp': time.time()
        }
        self.save_progress(self.progress_data)
        
        return result
    
    def find_image_files(self, directory: Union[str, Path]) -> List[Path]:
        """Find all supported image files in directory."""
        directory = Path(directory)
        image_files = []
        
        for ext in self.config.supported_extensions:
            image_files.extend(directory.glob(f'*{ext}'))
            image_files.extend(directory.glob(f'*{ext.upper()}'))
        
        return sorted(image_files)
    
    def process_batch(self, input_dir: Union[str, Path], output_dir: Union[str, Path],
                     progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Process a batch of images with progress tracking."""
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        
        if not input_dir.exists():
            self.logger.error(f"Input directory does not exist: {input_dir}")
            return {"success": False, "error": "Input directory not found"}
        
        # Find image files
        image_files = self.find_image_files(input_dir)
        if not image_files:
            self.logger.warning(f"No image files found in {input_dir}")
            return {"success": False, "error": "No image files found"}
        
        self.logger.info(f"Found {len(image_files)} image files")
        
        # Process images
        results = []
        successful = 0
        failed = 0
        
        # Create progress bar if tqdm is available
        if HAS_TQDM:
            progress_bar = tqdm(image_files, desc="Upscaling images", unit="image")
        else:
            progress_bar = image_files
        
        for image_file in progress_bar:
            output_file = output_dir / f"upscaled_{image_file.name}"
            
            if progress_callback:
                progress_callback(image_file.name)
            
            result = self.upscale_single_image(image_file, output_file)
            results.append(result)
            
            if result.status == ProcessingStatus.SUCCESS:
                successful += 1
                self.logger.info(f"✅ {image_file.name} -> {result.file_size_mb:.1f}MB")
            else:
                failed += 1
                self.logger.error(f"❌ {image_file.name}: {result.error_message}")
        
        # Summary
        total_time = sum(r.processing_time or 0 for r in results)
        
        summary = {
            "success": True,
            "total_files": len(image_files),
            "successful": successful,
            "failed": failed,
            "total_time": total_time,
            "average_time": total_time / len(image_files) if image_files else 0,
            "results": [asdict(r) for r in results]
        }
        
        self.logger.info(f"Batch processing complete: {successful} successful, {failed} failed")
        
        return summary

def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description="Enhanced Image Upscaler")
    parser.add_argument("input_dir", help="Input directory containing images")
    parser.add_argument("output_dir", help="Output directory for upscaled images")
    parser.add_argument("--scale", type=float, default=2.0, help="Scale factor (default: 2.0)")
    parser.add_argument("--dpi", type=int, nargs=2, default=[CONSTANT_300, CONSTANT_300], help="Target DPI (default: CONSTANT_300 CONSTANT_300)")
    parser.add_argument("--quality", type=int, default=95, help="JPEG quality (default: 95)")
    parser.add_argument("--method", choices=["pil", "sips", "auto"], default="auto", help="Processing method")
    parser.add_argument("--batch-size", type=int, default=10, help="Batch size for processing")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO", help="Log level")
    parser.add_argument("--config", help="Configuration file (JSON)")
    
    args = parser.parse_args()
    
    # Load configuration
    if args.config:
        try:
            with open(args.config, 'r') as f:
                config_data = json.load(f)
            config = UpscaleConfig(**config_data)
        except Exception as e:
            logger.info(f"Error loading config file: {e}")
            sys.exit(1)
    else:
        config = UpscaleConfig(
            scale_factor=args.scale,
            target_dpi=tuple(args.dpi),
            quality=args.quality,
            processing_method=ProcessingMethod(args.method),
            batch_size=args.batch_size,
            log_level=args.log_level
        )
    
    # Create upscaler
    try:
        upscaler = EnhancedImageUpscaler(config)
    except RuntimeError as e:
        logger.info(f"Error initializing upscaler: {e}")
        sys.exit(1)
    
    # Process images
    logger.info(f"🚀 Enhanced Image Upscaler")
    logger.info(f"Input: {args.input_dir}")
    logger.info(f"Output: {args.output_dir}")
    logger.info(f"Scale: {config.scale_factor}x")
    logger.info(f"DPI: {config.target_dpi}")
    logger.info(f"Method: {upscaler.processing_method.value}")
    logger.info("=" * 50)
        """progress_callback function."""

    
    def progress_callback(filename):
        if not HAS_TQDM:
            logger.info(f"Processing: {filename}")
    
    result = upscaler.process_batch(args.input_dir, args.output_dir, progress_callback)
    
    if result["success"]:
        logger.info(f"\n✅ Processing complete!")
        logger.info(f"Total files: {result['total_files']}")
        logger.info(f"Successful: {result['successful']}")
        logger.info(f"Failed: {result['failed']}")
        logger.info(f"Total time: {result['total_time']:.2f}s")
        logger.info(f"Average time: {result['average_time']:.2f}s per image")
    else:
        logger.info(f"\n❌ Processing failed: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()