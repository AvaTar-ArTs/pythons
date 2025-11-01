"""
Proc Vid

This module provides functionality for proc vid.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Example usage of the Transcription Analyzer
"""

import os
from transcription_analyzer import TranscriptionAnalyzer
from dotenv import load_dotenv

# Load environment variables from ~/.env
load_dotenv(os.path.expanduser("~/.env"))


def example_single_file():
    """Example of processing a single file."""
    logger.info("Example: Processing a single file")
    logger.info("-" * 40)

    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.info("Please set your OPENAI_API_KEY in the .env file")
        return

    # Initialize analyzer
    analyzer = TranscriptionAnalyzer(api_key)

    # Example file path (replace with your actual file)
    example_file = "example_audio.mp3"

    if os.path.exists(example_file):
        logger.info(f"Processing: {example_file}")
        success = analyzer.process_file(example_file)
        if success:
            logger.info("✅ File processed successfully!")
        else:
            logger.info("❌ Failed to process file")
    else:
        logger.info(f"Example file {example_file} not found")
        logger.info("Please add a sample MP3 or MP4 file to test with")


def example_batch_processing():
    """Example of batch processing multiple files."""
    logger.info("\nExample: Batch processing")
    logger.info("-" * 40)

    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.info("Please set your OPENAI_API_KEY in the .env file")
        return

    # Initialize analyzer
    analyzer = TranscriptionAnalyzer(api_key)

    # Example directory (replace with your actual directory)
    example_dir = "sample_files"

    if os.path.exists(example_dir):
        logger.info(f"Processing all files in: {example_dir}")
        # This would be called from batch_process.py
        logger.info("Run: python batch_process.py sample_files/")
    else:
        logger.info(f"Example directory {example_dir} not found")
        logger.info("Create a directory with sample MP3/MP4 files to test batch processing")


def show_output_structure():
    """Show the expected output structure."""
    logger.info("\nOutput Structure:")
    logger.info("-" * 40)
    print(
        """
    filename_analysis_YYYYMMDD_HHMMSS/
    ├── transcripts/
    │   ├── filename_transcript.txt          # Plain transcript
    │   └── filename_timestamped.txt         # Transcript with timestamps
    ├── analysis/
    │   └── filename_analysis.json           # GPT-4o analysis
    ├── audio/
    │   └── filename.mp3                     # Converted audio (MP4 files only)
    └── filename_summary.txt                 # Processing summary
    """
    )


def main():
    """Run example usage."""
    logger.info("🎯 Transcription Analyzer - Example Usage")
    logger.info("=" * 50)

    example_single_file()
    example_batch_processing()
    show_output_structure()

    logger.info("\n📝 Next Steps:")
    logger.info("1. Add your OpenAI API key to ~/.env file")
    logger.info("2. Run: python setup.py")
    logger.info("3. Add some MP3/MP4 files to test with")
    logger.info("4. Run: python transcription_analyzer.py your_file.mp4")


if __name__ == "__main__":
    main()
