#!/usr/bin/env python3
"""
Enhanced Image Resizer and Processor
Resize images with improved error handling, batch processing, and metadata generation.

Features:
- Dynamic resizing based on aspect ratio
- Batch processing with progress tracking
- Metadata CSV generation
- Proper error handling and logging
- Configurable parameters
"""

import os
import sys
import logging
import csv
import time
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional
from PIL import Image, UnidentifiedImageError
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed


def setup_logging(log_file: str = "image_resizer.log"):
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


def load_env_d():
    """Load all .env files from ~/.env.d directory with proper error handling."""
    logger = setup_logging()
    env_d_path = Path.home() / ".env.d"
    
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
                                
            except Exception as e:
                logger.warning(f"Warning: Error loading {env_file} at line {line_num}: {e}")
    else:
        logger.debug(f"Env directory does not exist: {env_d_path}")


logger = setup_logging()


def sanitize_filename(filename: str, file_ext: str) -> str:
    """
    Sanitize the filename to ensure:
    - Quotes are removed.
    - Extra periods in the name are replaced with underscores.
    - A single extension is maintained.
    """
    # Remove path separators and special characters
    filename = filename.strip('"').replace(" ", "_").replace("/", "_").replace(":", "_")
    # Remove any existing extension and ensure a single valid extension
    filename = Path(filename).stem
    return f"{filename}.{file_ext}"


def resize_image(
    input_path: Path, 
    output_path: Path, 
    max_width: int = 4500, 
    max_height: int = 5400,
    min_width: int = 6,
    min_height: int = 720,
    target_dpi: int = 300
) -> bool:
    """
    Resize image to meet dynamic target dimensions based on aspect ratio.
    """
    try:
        with Image.open(input_path) as im:
            width, height = im.size
            aspect_ratio = width / height

            # Calculate new dimensions based on constraints
            new_width, new_height = width, height
            
            # Downscale if too large
            if width > max_width or height > max_height:
                if width / max_width > height / max_height:
                    new_width = max_width
                    new_height = int(new_width / aspect_ratio)
                else:
                    new_height = max_height
                    new_width = int(new_height * aspect_ratio)
            # Upscale if too small
            elif width < min_width or height < min_height:
                if width / min_width < height / min_height:
                    new_width = min_width
                    new_height = int(new_width / aspect_ratio)
                else:
                    new_height = min_height
                    new_width = int(new_height * aspect_ratio)

            # Only resize if dimensions changed
            if (new_width, new_height) != (width, height):
                logger.info(f"🔄 Resizing {input_path.name}: {width}x{height} → {new_width}x{new_height}")
                
                # Convert to RGB if needed (for JPEG compatibility)
                if output_path.suffix.lower() in ['.jpg', '.jpeg'] and im.mode != "RGB":
                    im = im.convert("RGB")
                
                # Resize the image
                resized_im = im.resize((new_width, new_height), Image.LANCZOS)
                
                # Save with DPI information
                resized_im.save(
                    output_path, 
                    dpi=(target_dpi, target_dpi), 
                    quality=85,
                    format=output_path.suffix[1:].upper()  # Remove the dot
                )
            else:
                # Just copy if no resizing needed
                im.save(output_path, dpi=(target_dpi, target_dpi), quality=85)
        
        return True
    
    except UnidentifiedImageError:
        logger.error(f"❌ Cannot identify image: {input_path}")
        return False
    except Exception as e:
        logger.error(f"❌ Error resizing {input_path}: {e}")
        return False


def process_single_image(
    file_path: Path,
    output_dir: Path,
    max_width: int,
    max_height: int,
    min_width: int,
    min_height: int,
    target_dpi: int
) -> Optional[Tuple[str, str, str, int, int, int, int, str]]:
    """
    Process a single image and return metadata for CSV.
    """
    try:
        file_ext = file_path.suffix.lower()[1:]  # Remove the dot
        
        # Process only supported formats
        if file_ext not in ("jpg", "jpeg", "png", "bmp", "tiff", "webp"):
            logger.warning(f"⚠️ Skipping {file_path.name}: Unsupported file format.")
            return None

        # Open and analyze image
        with Image.open(file_path) as im:
            width, height = im.size
            logger.info(f"🖼️ Processing {file_path.name}: Original size: {width}x{height}")

            # Sanitize filename
            sanitized_filename = sanitize_filename(file_path.stem, file_ext)

            # Create output path
            output_file_path = output_dir / sanitized_filename
            
            # Resize image
            success = resize_image(
                file_path, 
                output_file_path, 
                max_width, max_height, 
                min_width, min_height, 
                target_dpi
            )
            
            if success:
                # Get file size after processing
                resized_size = output_file_path.stat().st_size
                creation_date = datetime.fromtimestamp(output_file_path.stat().st_ctime).strftime("%m-%d-%y")
                
                # Return metadata for CSV
                return (
                    sanitized_filename,
                    f"{resized_size / (1024 ** 2):.2f} MB",
                    creation_date,
                    width,
                    height,
                    target_dpi,
                    target_dpi,
                    str(output_file_path)
                )
            else:
                return None
                
    except Exception as e:
        logger.error(f"❌ Error processing {file_path}: {e}")
        return None


def process_images_and_generate_csv(
    source_directory: Path, 
    output_directory: Path,
    max_width: int = 4500,
    max_height: int = 5400,
    min_width: int = 6,
    min_height: int = 720,
    target_dpi: int = 300,
    max_workers: int = 4
) -> int:
    """Process images and generate metadata CSV."""
    output_directory.mkdir(parents=True, exist_ok=True)
    
    # Find all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    image_files = []
    
    for root, _, files in os.walk(source_directory):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in image_extensions:
                image_files.append(file_path)
    
    logger.info(f"Found {len(image_files)} image files to process")
    
    if not image_files:
        logger.info("No image files found to process")
        return 0
    
    # Process images in parallel
    metadata_rows = []
    processed_count = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all processing tasks
        future_to_file = {
            executor.submit(
                process_single_image,
                file_path,
                output_directory,
                max_width, max_height,
                min_width, min_height,
                target_dpi
            ): file_path
            for file_path in image_files
        }
        
        # Process completed tasks
        for future in as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                metadata = future.result()
                if metadata:
                    metadata_rows.append(metadata)
                    processed_count += 1
            except Exception as e:
                logger.error(f"❌ Unexpected error processing {file_path}: {e}")
    
    # Generate CSV with metadata
    current_date = datetime.now().strftime("%m-%d-%y")
    csv_output_path = output_directory / f"image_data-{current_date}.csv"
    
    with open(csv_output_path, "w", newline="", encoding='utf-8') as csvfile:
        fieldnames = [
            "Filename",
            "File Size",
            "Creation Date",
            "Original Width",
            "Original Height",
            "DPI_X",
            "DPI_Y",
            "Output Path",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in metadata_rows:
            writer.writerow({
                "Filename": row[0],
                "File Size": row[1],
                "Creation Date": row[2],
                "Original Width": row[3],
                "Original Height": row[4],
                "DPI_X": row[5],
                "DPI_Y": row[6],
                "Output Path": row[7],
            })
    
    logger.info(f"✅ Processed {processed_count}/{len(image_files)} images")
    logger.info(f"📄 CSV metadata saved to: {csv_output_path}")
    
    return processed_count


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(
        description='Enhanced Image Resizer and Processor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python enhanced_image_resizer.py /path/to/images /output/dir
  python enhanced_image_resizer.py /path/to/images /output/dir --max-width 1920 --max-height 1080
  python enhanced_image_resizer.py /path/to/images /output/dir --dpi 300 --workers 8
        """
    )
    
    parser.add_argument('source_dir', help='Source directory containing images')
    parser.add_argument('output_dir', help='Output directory for processed images')
    parser.add_argument('--max-width', type=int, default=4500, help='Maximum width (default: 4500)')
    parser.add_argument('--max-height', type=int, default=5400, help='Maximum height (default: 5400)')
    parser.add_argument('--min-width', type=int, default=6, help='Minimum width (default: 6)')
    parser.add_argument('--min-height', type=int, default=720, help='Minimum height (default: 720)')
    parser.add_argument('--dpi', type=int, default=300, help='Target DPI (default: 300)')
    parser.add_argument('--workers', type=int, default=4, help='Number of parallel workers')
    
    args = parser.parse_args()
    
    try:
        source_path = Path(args.source_dir)
        output_path = Path(args.output_dir)
        
        if not source_path.exists():
            logger.error(f"❌ Source directory does not exist: {source_path}")
            sys.exit(1)
        
        processed_count = process_images_and_generate_csv(
            source_path,
            output_path,
            args.max_width,
            args.max_height,
            args.min_width,
            args.min_height,
            args.dpi,
            args.workers
        )
        
        logger.info(f"✅ Image processing completed. {processed_count} files processed.")
        
    except KeyboardInterrupt:
        logger.info("⚠️ Processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error during processing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()