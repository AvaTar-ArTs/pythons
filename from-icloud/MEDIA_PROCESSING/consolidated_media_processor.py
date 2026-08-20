#!/usr/bin/env python3
"""
Consolidated Media Processor
A comprehensive tool for processing images, audio, and video files with unified interfaces.

Features:
- Image processing (resizing, upscaling, format conversion)
- Audio processing (text-to-speech, format conversion)
- Video processing (download, format conversion)
- Batch processing with progress tracking
- Comprehensive error handling and logging
- Configurable settings
- Type hints and documentation
"""

import os
import sys
import subprocess
import math
import logging
import time
from pathlib import Path
from typing import Dict, Tuple, Optional, List, Union, Any
from dataclasses import dataclass
from enum import Enum
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
import argparse
from PIL import Image, ImageOps
import requests
from gtts import gTTS
from mutagen import File as MutagenFile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('media_processor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MediaType(Enum):
    """Supported media types"""
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"


class ProcessingMethod(Enum):
    """Image processing methods"""
    CROP = "crop"
    PAD = "pad"
    STRETCH = "stretch"


@dataclass
class ProcessingConfig:
    """Configuration for media processing"""
    max_file_size_mb: float = 9.0
    target_dpi: int = 300
    base_size: int = 2000
    max_dimension: int = 4000
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


class MediaProcessor:
    """Main media processing class with improved error handling and performance"""

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
        self.config = config or ProcessingConfig()
        self.supported_image_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.webp'}
        self.supported_audio_extensions = {'.mp3', '.wav', '.flac', '.aac', '.m4a', '.ogg'}
        self.supported_video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}

    def run_command(self, cmd: str) -> Tuple[bool, str, str]:
        """Run a shell command with improved error handling"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
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
        max_size_bytes = self.config.max_file_size_mb * 1024 * 1024
        current_size = self.get_file_size(image_path)

        if current_size <= max_size_bytes:
            return True, "File size already within limits"

        logger.info(f"Optimizing file size for {image_path} (current: {current_size / (1024*1024):.1f}MB)")

        for quality in range(self.config.quality_range[0], self.config.quality_range[1], -self.config.quality_step):
            with self.temp_file(image_path) as temp_path:
                quality_cmd = f'sips -s formatOptions {quality} "{image_path}" --out "{temp_path}"'

                success, _, _ = self.run_command(quality_cmd)
                if success and os.path.exists(temp_path):
                    temp_size = self.get_file_size(temp_path)
                    if temp_size <= max_size_bytes:
                        try:
                            shutil.move(temp_path, image_path)
                            logger.info(f"Optimized to {quality}% quality ({temp_size / (1024*1024):.1f}MB)")
                            return True, f"Optimized to {quality}% quality"
                        except OSError as e:
                            logger.error(f"Failed to replace file: {e}")
                            return False, f"Failed to replace file: {e}"

        return False, "Could not optimize file size within quality limits"

    def upscale_image(self, input_path: Union[str, Path], output_path: Union[str, Path]) -> Tuple[bool, str]:
        """Upscale an image by 2x and set resolution to 300 DPI"""
        try:
            with Image.open(input_path) as image:
                # Convert to RGB if needed
                if image.mode in ('RGBA', 'LA', 'P'):
                    image = image.convert('RGB')

                # Upscale by 2x
                upscaled_image = image.resize(
                    (image.width * 2, image.height * 2),
                    Image.Resampling.LANCZOS
                )

                # Save with 300 DPI
                upscaled_image.save(output_path, dpi=(300, 300))
                return True, "Image upscaled successfully"
        except Exception as e:
            logger.error(f"Error upscaling image {input_path}: {e}")
            return False, str(e)

    def convert_image_format(self, input_path: Union[str, Path], output_path: Union[str, Path], format_ext: str) -> Tuple[bool, str]:
        """Convert image to a different format"""
        try:
            with Image.open(input_path) as image:
                # Convert to RGB if needed for certain formats
                if format_ext.lower() in ['.jpg', '.jpeg'] and image.mode in ('RGBA', 'LA', 'P'):
                    image = image.convert('RGB')

                # Determine PIL format from extension
                format_map = {
                    '.jpg': 'JPEG', '.jpeg': 'JPEG',
                    '.png': 'PNG', '.bmp': 'BMP',
                    '.tiff': 'TIFF', '.webp': 'WEBP'
                }
                
                pil_format = format_map.get(format_ext.lower(), 'JPEG')
                
                image.save(output_path, format=pil_format, dpi=(300, 300))
                return True, f"Image converted to {format_ext} successfully"
        except Exception as e:
            logger.error(f"Error converting image {input_path} to {format_ext}: {e}")
            return False, str(e)

    def text_to_speech(self, text: str, output_path: Union[str, Path], lang: str = 'en') -> Tuple[bool, str]:
        """Convert text to speech and save as audio file"""
        try:
            tts = gTTS(text=text, lang=lang)
            tts.save(output_path)
            return True, "Text converted to speech successfully"
        except Exception as e:
            logger.error(f"Error converting text to speech: {e}")
            return False, str(e)

    def convert_audio_format(self, input_path: Union[str, Path], output_path: Union[str, Path], target_format: str) -> Tuple[bool, str]:
        """Convert audio to a different format using ffmpeg"""
        try:
            # Check if ffmpeg is available
            success, _, _ = self.run_command('which ffmpeg')
            if not success:
                return False, "ffmpeg not found. Please install ffmpeg."

            # Determine codec based on target format
            codec_map = {
                '.mp3': 'mp3',
                '.wav': 'pcm_s16le',
                '.flac': 'flac',
                '.aac': 'aac',
                '.m4a': 'aac',
                '.ogg': 'libvorbis'
            }
            
            codec = codec_map.get(target_format.lower(), 'mp3')
            
            # Build ffmpeg command
            cmd = f'ffmpeg -i "{input_path}" -c:a {codec} "{output_path}" -y'
            success, stdout, stderr = self.run_command(cmd)
            
            if success:
                return True, f"Audio converted to {target_format} successfully"
            else:
                return False, f"Audio conversion failed: {stderr}"
        except Exception as e:
            logger.error(f"Error converting audio {input_path} to {target_format}: {e}")
            return False, str(e)

    def download_video(self, url: str, output_path: Union[str, Path]) -> Tuple[bool, str]:
        """Download video from URL using requests (basic implementation)"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            return True, f"Video downloaded successfully to {output_path}"
        except Exception as e:
            logger.error(f"Error downloading video from {url}: {e}")
            return False, str(e)

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
            output_path.parent.mkdir(parents=True, exist_ok=True)

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
                'file_size_mb': file_size / (1024 * 1024),
                'message': message,
                'optimization_message': opt_message
            }

        except Exception as e:
            logger.error(f"Error processing {input_path}: {e}")
            return {'success': False, 'error': str(e)}

    def find_media_files(self, directory: Union[str, Path], media_type: MediaType) -> List[Path]:
        """Find all supported media files in directory based on type"""
        directory = Path(directory)
        media_files = []

        if media_type == MediaType.IMAGE:
            extensions = self.supported_image_extensions
        elif media_type == MediaType.AUDIO:
            extensions = self.supported_audio_extensions
        elif media_type == MediaType.VIDEO:
            extensions = self.supported_video_extensions
        else:
            extensions = set()

        for ext in extensions:
            media_files.extend(directory.glob(f'*{ext}'))
            media_files.extend(directory.glob(f'*{ext.upper()}'))

        return sorted(media_files)

    def process_batch(
        self,
        media_files: List[Path],
        aspect_ratio: AspectRatio,
        output_dir: Union[str, Path],
        progress_callback: Optional[callable] = None
    ) -> Tuple[int, int]:
        """Process a batch of media files with progress tracking"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        successful = 0
        failed = 0

        for i, media_path in enumerate(media_files, 1):
            output_path = output_dir / f"processed_{media_path.name}"

            if progress_callback:
                progress_callback(i, len(media_files), media_path.name)

            result = self.process_single_image(media_path, output_path, aspect_ratio)

            if result['success']:
                successful += 1
                logger.info(f"✅ {media_path.name} -> {result['file_size_mb']:.1f}MB")
            else:
                failed += 1
                logger.error(f"❌ {media_path.name}: {result['error']}")

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

        image_files = self.find_media_files(directory, MediaType.IMAGE)
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
            output_dir = directory / f"processed_{aspect_ratio.name}"

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
    """Main function with CLI interface"""
    parser = argparse.ArgumentParser(description='Consolidated Media Processor')
    parser.add_argument('action', choices=['process-images', 'upscale', 'convert-format', 'text-to-speech', 'convert-audio', 'download-video'], 
                       help='Action to perform')
    parser.add_argument('--input', '-i', required=True, help='Input file or directory')
    parser.add_argument('--output', '-o', required=True, help='Output file or directory')
    parser.add_argument('--format', '-f', help='Target format for conversion')
    parser.add_argument('--text', help='Text for text-to-speech')
    parser.add_argument('--lang', default='en', help='Language for text-to-speech')
    
    args = parser.parse_args()

    print("🖼️  CONSOLIDATED MEDIA PROCESSOR")
    print("=" * 50)
    print("Comprehensive media processing with multiple capabilities")
    print("Features: Error handling, progress tracking, batch processing")
    print("=" * 50)

    processor = MediaProcessor()

    if args.action == 'process-images':
        # Check if sips is available
        success, _, _ = processor.run_command('which sips')
        if not success:
            print("❌ sips command not found. This script requires macOS.")
            sys.exit(1)

        directory = Path(args.input)
        print(f"\n📁 Processing images in: {directory}")

        # Progress callback
        def progress_callback(current, total, filename):
            print(f"  [{current}/{total}] {filename}...", end=" ")

        # Process images
        results = processor.process_all_ratios(directory, progress_callback)

        # Print summary
        print(f"\n📁 Output directories created:")
        for ratio_name in processor.ASPECT_RATIOS:
            print(f"  • processed_{ratio_name.name}/")

    elif args.action == 'upscale':
        input_path = Path(args.input)
        output_path = Path(args.output)
        
        success, message = processor.upscale_image(input_path, output_path)
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")

    elif args.action == 'convert-format':
        input_path = Path(args.input)
        output_path = Path(args.output)
        
        if not args.format:
            print("❌ Format required for conversion")
            sys.exit(1)
        
        success, message = processor.convert_image_format(input_path, output_path, args.format)
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")

    elif args.action == 'text-to-speech':
        if not args.text:
            print("❌ Text required for text-to-speech")
            sys.exit(1)
        
        output_path = Path(args.output)
        success, message = processor.text_to_speech(args.text, output_path, args.lang)
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")

    elif args.action == 'convert-audio':
        input_path = Path(args.input)
        output_path = Path(args.output)
        
        if not args.format:
            print("❌ Format required for audio conversion")
            sys.exit(1)
        
        success, message = processor.convert_audio_format(input_path, output_path, args.format)
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")

    elif args.action == 'download-video':
        output_path = Path(args.output)
        success, message = processor.download_video(args.input, output_path)
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")


if __name__ == "__main__":
    main()