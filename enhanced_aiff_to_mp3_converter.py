#!/usr/bin/env python3
"""
Enhanced AIFF to MP3 Converter
Convert AIFF files to MP3 format with improved error handling and functionality.

Features:
- Proper error handling and logging
- Progress tracking
- Configurable bitrates
- Batch processing
- File validation
"""

import os
import sys
import logging
import subprocess
from pathlib import Path
from typing import Optional, List
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed


def setup_logging(log_file: str = "aiff_to_mp3_converter.log"):
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


logger = setup_logging()


def convert_aiff_to_mp3(input_file: str, output_file: str, bitrate: str = "128k", 
                       sample_rate: Optional[int] = None) -> bool:
    """Convert AIFF file to MP3 using ffmpeg with enhanced error handling."""
    try:
        # Ensure output directory exists
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            "ffmpeg",
            "-i", input_file,
            "-acodec", "libmp3lame",
            "-ab", bitrate,
        ]
        
        # Add sample rate if specified
        if sample_rate:
            cmd.extend(["-ar", str(sample_rate)])
        
        # Add output file and overwrite flag
        cmd.extend([output_file, "-y"])
        
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True,
            check=False  # Don't raise exception on non-zero exit
        )
        
        if result.returncode == 0:
            logger.info(f"✓ Successfully converted: {Path(input_file).name}")
            return True
        else:
            logger.error(f"✗ Conversion failed for {input_file}: {result.stderr}")
            return False

    except Exception as e:
        logger.error(f"✗ Conversion error for {input_file}: {e}")
        return False


def validate_aiff_file(file_path: Path) -> bool:
    """Validate that the file is a proper AIFF file."""
    try:
        # Check file extension
        if file_path.suffix.lower() not in ['.aiff', '.aif']:
            return False
        
        # Check if file exists and has content
        if not file_path.exists() or file_path.stat().st_size == 0:
            return False
        
        # Optional: Use ffprobe to validate file integrity
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-select_streams", "a:0", 
             "-show_entries", "stream=codec_name", "-of", "csv=p=0", str(file_path)],
            capture_output=True,
            text=True
        )
        
        # If ffprobe succeeds and detects audio, it's likely valid
        return result.returncode == 0
    
    except Exception:
        # If ffprobe isn't available or fails, just check basic file properties
        return file_path.exists() and file_path.suffix.lower() in ['.aiff', '.aif']


def convert_all_aiff_files(
    source_dir: Path, 
    output_dir: Path, 
    bitrate: str = "128k", 
    sample_rate: Optional[int] = None,
    max_workers: int = 4
) -> int:
    """Convert all AIFF files in the source directory to MP3 with enhanced functionality."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Scanning for AIFF files in: {source_dir}")
    
    # Find all AIFF files
    aiff_files = []
    for aiff_file in source_dir.rglob("*.aiff"):
        if validate_aiff_file(aiff_file):
            aiff_files.append(aiff_file)
        else:
            logger.warning(f"Skipping invalid file: {aiff_file}")
    
    for aiff_file in source_dir.rglob("*.aif"):
        if validate_aiff_file(aiff_file):
            aiff_files.append(aiff_file)
        else:
            logger.warning(f"Skipping invalid file: {aiff_file}")
    
    logger.info(f"Found {len(aiff_files)} valid AIFF files")
    
    if not aiff_files:
        logger.info("No valid AIFF files found to convert")
        return 0
    
    converted_count = 0
    
    # Process files in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all conversion tasks
        future_to_file = {
            executor.submit(
                convert_aiff_to_mp3, 
                str(aiff_file), 
                str(output_dir / aiff_file.with_suffix('.mp3').name),
                bitrate,
                sample_rate
            ): aiff_file 
            for aiff_file in aiff_files
        }
        
        # Process completed tasks
        for future in as_completed(future_to_file):
            aiff_file = future_to_file[future]
            try:
                success = future.result()
                if success:
                    converted_count += 1
            except Exception as e:
                logger.error(f"✗ Unexpected error converting {aiff_file}: {e}")
    
    logger.info(f"\n✅ Converted {converted_count}/{len(aiff_files)} files to MP3")
    logger.info(f"MP3 files saved to: {output_dir}")
    
    return converted_count


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(
        description='Enhanced AIFF to MP3 Converter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python enhanced_aiff_to_mp3.py /path/to/aiff/files /output/mp3/dir
  python enhanced_aiff_to_mp3.py /path/to/aiff/files /output/mp3/dir --bitrate 192k
  python enhanced_aiff_to_mp3.py /path/to/aiff/files /output/mp3/dir --sample-rate 44100
        """
    )
    
    parser.add_argument('source_dir', help='Source directory containing AIFF files')
    parser.add_argument('output_dir', help='Output directory for MP3 files')
    parser.add_argument('--bitrate', default='128k', help='MP3 bitrate (default: 128k)')
    parser.add_argument('--sample-rate', type=int, help='Sample rate in Hz (e.g., 44100)')
    parser.add_argument('--workers', type=int, default=4, help='Number of parallel workers')
    
    args = parser.parse_args()
    
    try:
        source_path = Path(args.source_dir)
        output_path = Path(args.output_dir)
        
        if not source_path.exists():
            logger.error(f"Source directory does not exist: {source_path}")
            sys.exit(1)
        
        convert_count = convert_all_aiff_files(
            source_path, 
            output_path, 
            args.bitrate, 
            args.sample_rate,
            args.workers
        )
        
        logger.info(f"Conversion completed. {convert_count} files processed.")
        
    except KeyboardInterrupt:
        logger.info("Conversion interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error during conversion: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()