"""
Batch 15

This module provides functionality for batch 15.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Batch processing script for multiple audio/video files
"""

import os
import sys
import glob
from pathlib import Path
from transcription_analyzer import TranscriptionAnalyzer
from dotenv import load_dotenv
import os

# Load environment variables from ~/.env
load_dotenv(os.path.expanduser("~/.env"))


def main():
    """Process multiple files in a directory."""
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.info("ERROR: OPENAI_API_KEY not found in environment variables")
        logger.info("Please set your OpenAI API key in a .env file or environment variable")
        return

    # Initialize analyzer
    analyzer = TranscriptionAnalyzer(api_key)

    # Get input directory from command line argument
    if len(sys.argv) != 2:
        logger.info("Usage: python batch_process.py <input_directory>")
        logger.info("Will process all MP3 and MP4 files in the directory")
        return

    input_dir = Path(sys.argv[1])

    if not input_dir.exists():
        logger.info(f"ERROR: Directory {input_dir} does not exist")
        return

    # Find all supported files
    supported_files = []
    for pattern in ["*.mp3", "*.mp4", "*.MP3", "*.MP4"]:
        supported_files.extend(input_dir.glob(pattern))

    if not supported_files:
        logger.info(f"No MP3 or MP4 files found in {input_dir}")
        return

    logger.info(f"Found {len(supported_files)} files to process:")
    for file in supported_files:
        logger.info(f"  - {file.name}")

    # Process each file
    successful = 0
    failed = 0

    for file_path in supported_files:
        logger.info(f"\n{'='*50}")
        logger.info(f"Processing: {file_path.name}")
        logger.info(f"{'='*50}")

        if analyzer.process_file(str(file_path)):
            successful += 1
            logger.info(f"✅ Successfully processed {file_path.name}")
        else:
            failed += 1
            logger.info(f"❌ Failed to process {file_path.name}")

    logger.info(f"\n{'='*50}")
    logger.info(f"BATCH PROCESSING COMPLETE")
    logger.info(f"{'='*50}")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {failed}")
    logger.info(f"Total: {len(supported_files)}")


if __name__ == "__main__":
    main()
