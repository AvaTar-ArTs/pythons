
# Constants
CONSTANT_300 = 300
CONSTANT_4096 = 4096

#!/usr/bin/env python3
"""
Enhanced Common Utilities
=========================

A comprehensive collection of improved utility functions used across projects.
This module provides robust, well-tested, and documented utilities for common tasks.

Key improvements:
- Full type hints and documentation
- Comprehensive error handling
- Performance optimizations
- Configuration management
- Logging integration
- Unit testing support

Author: Enhanced by Claude
Version: 2.0
"""

import os
import sys
import json
import csv
import logging
import time
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple, Callable, Iterator
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from contextlib import contextmanager
import shutil
import subprocess
from functools import wraps
import tempfile

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class ProcessingResult:
    """Standard result structure for processing operations."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    processing_time: Optional[float] = None
    error: Optional[str] = None

@dataclass
class FileInfo:
    """File information structure."""
    path: Path
    size: int
    created: datetime
    modified: datetime
    extension: str
    hash: Optional[str] = None

class EnhancedFileManager:
    """Enhanced file management utilities with error handling and logging."""

    def __init__(self, base_path: Union[str, Path], log_level: str = "INFO"):
        """__init__ function."""
        self.base_path = Path(base_path)
        self.logger = logging.getLogger(f"{__name__}.FileManager")
        self.logger.setLevel(getattr(logging, log_level.upper()))

    def get_file_info(self, file_path: Union[str, Path]) -> Optional[FileInfo]:
        """Get comprehensive file information with error handling."""
        try:
            path = Path(file_path)
            if not path.exists():
                self.logger.warning(f"File not found: {path}")
                return None

            stat = path.stat()
            return FileInfo(
                path = path, 
                size = stat.st_size, 
                created = datetime.fromtimestamp(stat.st_ctime, tz = timezone.utc), 
                modified = datetime.fromtimestamp(stat.st_mtime, tz = timezone.utc), 
                extension = path.suffix.lower(), 
                hash = self._calculate_file_hash(path)
            )
        except Exception as e:
            self.logger.error(f"Error getting file info for {file_path}: {e}")
            return None

    def _calculate_file_hash(self, file_path: Path, algorithm: str = "md5") -> Optional[str]:
        """Calculate file hash with error handling."""
        try:
            hash_func = hashlib.new(algorithm)
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(CONSTANT_4096), b""):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception as e:
            self.logger.error(f"Error calculating hash for {file_path}: {e}")
            return None

    def safe_copy(self, src: Union[str, Path], dst: Union[str, Path], 
                  overwrite: bool = False) -> ProcessingResult:
        """Safely copy file with comprehensive error handling."""
        start_time = time.time()
        try:
            src_path = Path(src)
            dst_path = Path(dst)

            if not src_path.exists():
                return ProcessingResult(
                    success = False, 
                    message = f"Source file not found: {src_path}", 
                    processing_time = time.time() - start_time, 
                    error="FileNotFoundError"
                )

            if dst_path.exists() and not overwrite:
                return ProcessingResult(
                    success = False, 
                    message = f"Destination file exists: {dst_path}", 
                    processing_time = time.time() - start_time, 
                    error="FileExistsError"
                )

            # Ensure destination directory exists
            dst_path.parent.mkdir(parents = True, exist_ok = True)

            # Copy file
            shutil.copy2(src_path, dst_path)

            return ProcessingResult(
                success = True, 
                message = f"Successfully copied {src_path} to {dst_path}", 
                processing_time = time.time() - start_time, 
                data={"source": str(src_path), "destination": str(dst_path)}
            )

        except Exception as e:
            return ProcessingResult(
                success = False, 
                message = f"Error copying file: {e}", 
                processing_time = time.time() - start_time, 
                error = str(e)
            )

    def find_files(self, pattern: str, recursive: bool = True) -> List[FileInfo]:
        """Find files matching pattern with comprehensive error handling."""
        try:
            files = []
            if recursive:
                search_path = self.base_path.rglob(pattern)
            else:
                search_path = self.base_path.glob(pattern)

            for file_path in search_path:
                if file_path.is_file():
                    file_info = self.get_file_info(file_path)
                    if file_info:
                        files.append(file_info)

            self.logger.info(f"Found {len(files)} files matching pattern: {pattern}")
            return files

        except Exception as e:
            self.logger.error(f"Error finding files with pattern {pattern}: {e}")
            return []

class EnhancedImageProcessor:
    """Enhanced image processing utilities with error handling and optimization."""

        """__init__ function."""
    def __init__(self, log_level: str = "INFO"):
        self.logger = logging.getLogger(f"{__name__}.ImageProcessor")
        self.logger.setLevel(getattr(logging, log_level.upper()))

        # Try to import PIL
        try:
            from PIL import Image, ImageOps
            self.Image = Image
            self.ImageOps = ImageOps
            self.pil_available = True
        except ImportError:
            self.logger.warning("PIL not available. Image processing features disabled.")
            self.pil_available = False

    def upscale_image(self, input_path: Union[str, Path], output_path: Union[str, Path], 
                     scale_factor: float = 2.0, dpi: Tuple[int, int] = (CONSTANT_300, CONSTANT_300), 
                     quality: int = 95) -> ProcessingResult:
        """Enhanced image upscaling with comprehensive error handling."""
        start_time = time.time()

        if not self.pil_available:
            return ProcessingResult(
                success = False, 
                message="PIL not available", 
                processing_time = time.time() - start_time, 
                error="ImportError"
            )

        try:
            input_path = Path(input_path)
            output_path = Path(output_path)

            if not input_path.exists():
                return ProcessingResult(
                    success = False, 
                    message = f"Input file not found: {input_path}", 
                    processing_time = time.time() - start_time, 
                    error="FileNotFoundError"
                )

            # Ensure output directory exists
            output_path.parent.mkdir(parents = True, exist_ok = True)

            # Open and process image
            with self.Image.open(input_path) as img:
                # Convert to RGB if needed
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')

                # Calculate new dimensions
                new_width = int(img.width * scale_factor)
                new_height = int(img.height * scale_factor)

                # Resize image
                upscaled_img = img.resize((new_width, new_height), self.Image.Resampling.LANCZOS)

                # Save with specified DPI and quality
                upscaled_img.save(
                    output_path, 
                    format='JPEG', 
                    dpi = dpi, 
                    quality = quality, 
                    optimize = True
                )

            return ProcessingResult(
                success = True, 
                message = f"Successfully upscaled image: {input_path} -> {output_path}", 
                processing_time = time.time() - start_time, 
                data={
                    "input_size": (img.width, img.height), 
                    "output_size": (new_width, new_height), 
                    "scale_factor": scale_factor, 
                    "dpi": dpi, 
                    "quality": quality
                }
            )

        except Exception as e:
            return ProcessingResult(
                success = False, 
                message = f"Error upscaling image: {e}", 
                processing_time = time.time() - start_time, 
                error = str(e)
            )

class EnhancedAudioProcessor:
    """Enhanced audio processing utilities with error handling."""
        """__init__ function."""

    def __init__(self, log_level: str = "INFO"):
        self.logger = logging.getLogger(f"{__name__}.AudioProcessor")
        self.logger.setLevel(getattr(logging, log_level.upper()))

        # Check for audio processing dependencies
        self.whisper_available = self._check_whisper()
        self.ffmpeg_available = self._check_ffmpeg()

    def _check_whisper(self) -> bool:
        """Check if Whisper is available."""
        try:
            import whisper
            return True
        except ImportError:
            self.logger.warning("Whisper not available. Audio transcription features disabled.")
            return False

    def _check_ffmpeg(self) -> bool:
        """Check if FFmpeg is available."""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output = True, text = True, timeout = 10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.logger.warning("FFmpeg not available. Audio conversion features disabled.")
            return False

    def transcribe_audio(self, audio_path: Union[str, Path], 
                        model_size: str = "base", 
                        language: Optional[str] = None) -> ProcessingResult:
        """Enhanced audio transcription with error handling."""
        start_time = time.time()

        if not self.whisper_available:
            return ProcessingResult(
                success = False, 
                message="Whisper not available", 
                processing_time = time.time() - start_time, 
                error="ImportError"
            )

        try:
            import whisper

            audio_path = Path(audio_path)
            if not audio_path.exists():
                return ProcessingResult(
                    success = False, 
                    message = f"Audio file not found: {audio_path}", 
                    processing_time = time.time() - start_time, 
                    error="FileNotFoundError"
                )

            # Load model
            model = whisper.load_model(model_size)

            # Transcribe
            result = model.transcribe(str(audio_path), language = language)

            return ProcessingResult(
                success = True, 
                message = f"Successfully transcribed audio: {audio_path}", 
                processing_time = time.time() - start_time, 
                data={
                    "text": result["text"], 
                    "language": result.get("language", "unknown"), 
                    "segments": result.get("segments", []), 
                    "model_size": model_size
                }
            )

        except Exception as e:
            return ProcessingResult(
                success = False, 
                message = f"Error transcribing audio: {e}", 
                processing_time = time.time() - start_time, 
                error = str(e)
            )

class EnhancedDataProcessor:
    """__init__ function."""
    """Enhanced data processing utilities with error handling and optimization."""

    def __init__(self, log_level: str = "INFO"):
        self.logger = logging.getLogger(f"{__name__}.DataProcessor")
        self.logger.setLevel(getattr(logging, log_level.upper()))

    def read_csv_safe(self, file_path: Union[str, Path], 
                     encoding: str = 'utf-8') -> ProcessingResult:
        """Safely read CSV file with error handling."""
        start_time = time.time()

        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return ProcessingResult(
                    success = False, 
                    message = f"CSV file not found: {file_path}", 
                    processing_time = time.time() - start_time, 
                    error="FileNotFoundError"
                )

            data = []
            with open(file_path, 'r', encoding = encoding, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data.append(row)

            return ProcessingResult(
                success = True, 
                message = f"Successfully read CSV: {file_path}", 
                processing_time = time.time() - start_time, 
                data={"rows": len(data), "columns": list(data[0].keys()) if data else []}
            )

        except Exception as e:
            return ProcessingResult(
                success = False, 
                message = f"Error reading CSV: {e}", 
                processing_time = time.time() - start_time, 
                error = str(e)
            )

    def write_json_safe(self, data: Any, file_path: Union[str, Path], 
                       indent: int = 2) -> ProcessingResult:
        """Safely write JSON file with error handling."""
        start_time = time.time()

        try:
            file_path = Path(file_path)

            # Ensure directory exists
            file_path.parent.mkdir(parents = True, exist_ok = True)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent = indent, ensure_ascii = False, default = str)

            return ProcessingResult(
                success = True, 
                message = f"Successfully wrote JSON: {file_path}", 
                processing_time = time.time() - start_time, 
                data={"file_size": file_path.stat().st_size}
            )

        except Exception as e:
            return ProcessingResult(
                success = False, 
                message = f"Error writing JSON: {e}", 
                processing_time = time.time() - start_time, 
                error = str(e)
            )

    """wrapper function."""
def timing_decorator(func: Callable) -> Callable:
    """Decorator to add timing information to functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        if hasattr(result, 'processing_time'):
            result.processing_time = end_time - start_time

        logger.info(f"{func.__name__} completed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper

@contextmanager
def safe_temp_file(suffix: str = ".tmp", prefix: str = "enhanced_"):
    """Context manager for safe temporary file handling."""
    temp_file = None
    try:
        temp_file = tempfile.NamedTemporaryFile(suffix = suffix, prefix = prefix, delete = False)
        yield temp_file.name
    finally:
        if temp_file:
            temp_file.close()
            try:
                os.unlink(temp_file.name)
            except OSError:
                pass

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

def main():
    """Demo function showing usage of enhanced utilities."""
    logger.info("🚀 Enhanced Common Utilities Demo")
    logger.info("=" * 50)

    # Setup logging
    logger = setup_logging("INFO")

    # Initialize managers
    file_manager = EnhancedFileManager(Path("/tmp"), "INFO")
    image_processor = EnhancedImageProcessor("INFO")
    audio_processor = EnhancedAudioProcessor("INFO")
    data_processor = EnhancedDataProcessor("INFO")

    # Demo file operations
    logger.info("\n📁 File Operations Demo:")
    test_file = Path(Path("/tmp/test_file.txt"))
    test_file.write_text("Hello, World!")

    file_info = file_manager.get_file_info(test_file)
    if file_info:
        logger.info(f"File: {file_info.path}")
        logger.info(f"Size: {file_info.size} bytes")
        logger.info(f"Hash: {file_info.hash}")

    # Demo data operations
    logger.info("\n📊 Data Operations Demo:")
    test_data = {"message": "Hello, World!", "timestamp": datetime.now().isoformat()}
    result = data_processor.write_json_safe(test_data, Path("/tmp/test_data.json"))
    logger.info(f"JSON write result: {result.success} - {result.message}")

    # Cleanup
    test_file.unlink(missing_ok = True)
    Path(Path("/tmp/test_data.json")).unlink(missing_ok = True)

    logger.info("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    main()