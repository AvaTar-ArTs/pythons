#!/usr/bin/env python3
"""
Main entry point for the Transcription Analyzer example usage
"""

# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)
from pathlib import Path as PathLib


def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip("'").strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")


load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    from dotenv import load_dotenv

    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass

import logging
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Tuple

try:
    from transcription_analyzer import TranscriptionAnalyzer
except ImportError:
    logger.error(
        "transcription_analyzer module not found. Please install required dependencies."
    )
    sys.exit(1)

# Load environment variables from ~/.env.dv/
env_path = Path.home() / ".env.dv" / ".env"
load_dotenv(env_path)

# Configure logging with enhanced formatting
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("transcription_processor.log", mode="a"),
    ],
)
logger = logging.getLogger(__name__)


def check_api_key() -> Optional[str]:
    """Check if OpenAI API key is available and return it.

    Returns:
        Optional[str]: API key if found, None otherwise
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error(
            "OPENAI_API_KEY not found. Please set your API key in ~/.env.dv/.env file"
        )
        logger.info("Format: OPENAI_API_KEY=your_actual_api_key_here")
        return None
    return api_key


def validate_file_path(file_path: str) -> Tuple[bool, str]:
    """Validate if the given path exists and is a file.

    Args:
        file_path (str): Path to validate

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    path = Path(file_path)
    if not path.exists():
        return False, f"File '{file_path}' does not exist"
    if not path.is_file():
        return False, f"'{file_path}' is not a file"
    return True, ""


def validate_directory_path(dir_path: str) -> Tuple[bool, str]:
    """Validate if the given path exists and is a directory.

    Args:
        dir_path (str): Path to validate

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    path = Path(dir_path)
    if not path.exists():
        return False, f"Directory '{dir_path}' does not exist"
    if not path.is_dir():
        return False, f"'{dir_path}' is not a directory"
    return True, ""


def example_batch_processing() -> bool:
    """Example of batch processing multiple files with improved error handling.

    Returns:
        bool: True if batch processing example was successful, False otherwise
    """
    logger.info("\n📦 Example: Batch Processing")
    logger.info("=" * 40)

    api_key = check_api_key()
    if not api_key:
        return False

    try:
        TranscriptionAnalyzer(api_key)
        example_dir = "sample_files"

        is_valid, error_msg = validate_directory_path(example_dir)
        if is_valid:
            logger.info(f"✅ Found directory: {example_dir}")
            logger.info(f"Processing all files in: {example_dir}")
            logger.info("To process this directory, run:")
            logger.info("python batch_process.py sample_files/")
            return True
        else:
            logger.warning(f"❌ {error_msg}")
            logger.info(
                "💡 Create a 'sample_files' directory with MP3/MP4 files to test batch processing"
            )
            return False

    except Exception as e:
        logger.error(f"🚨 Error initializing TranscriptionAnalyzer: {e}")
        logger.debug("Stack trace:", exc_info=True)
        return False


def example_single_file() -> bool:
    """Example of processing a single file with enhanced validation.

    Returns:
        bool: True if single file processing was successful, False otherwise
    """
    logger.info("\n🎵 Example: Single File Processing")
    logger.info("=" * 40)

    api_key = check_api_key()
    if not api_key:
        return False

    try:
        analyzer = TranscriptionAnalyzer(api_key)
        example_file = "example_audio.mp3"

        is_valid, error_msg = validate_file_path(example_file)
        if is_valid:
            logger.info(f"🔍 Processing: {example_file}")
            success = analyzer.process_file(example_file)

            if success:
                logger.info("✅ File processed successfully!")
                logger.info(
                    f"📁 Output saved to: {analyzer.get_output_directory(example_file)}"
                )
                return True
            else:
                logger.error("❌ Failed to process file")
                return False
        else:
            logger.warning(f"⚠️  {error_msg}")
            logger.info(
                "💡 Please add a sample MP3 or MP4 file named 'example_audio.mp3' to test"
            )
            return False

    except Exception as e:
        logger.error(f"🚨 Error processing file: {e}")
        logger.debug("Stack trace:", exc_info=True)
        return False


def show_output_structure() -> None:
    """Display the expected output directory structure with clear formatting."""
    logger.info("\n📁 Expected Output Structure:")
    logger.info("=" * 40)
    logger.info(
        """
    filename_analysis_YYYYMMDD_HHMMSS/
    ├── transcripts/
    │   ├── filename_transcript.txt          # Plain text transcript
    │   └── filename_timestamped.txt         # Transcript with timestamps
    ├── analysis/
    │   └── filename_analysis.json           # GPT-4o analysis results
    ├── audio/
    │   └── filename.mp3                     # Converted audio (for MP4 files)
    └── filename_summary.txt                 # Processing summary and metadata
    """
    )


def display_setup_instructions() -> None:
    """Display comprehensive setup instructions for users."""
    logger.info("\n🚀 Setup Instructions:")
    logger.info("=" * 40)
    logger.info("1. 📋 Add your OpenAI API key:")
    logger.info("   echo 'OPENAI_API_KEY=your_key_here' > ~/.env.dv/.env")
    logger.info("2. ⚙️  Install dependencies:")
    logger.info("   pip install -r requirements.txt")
    logger.info("3. 📂 Add sample files:")
    logger.info("   mkdir sample_files && cp your_file.mp4 sample_files/")
    logger.info("4. 🎯 Process files:")
    logger.info("   python transcription_analyzer.py your_file.mp4")
    logger.info("   python batch_process.py sample_files/")


def main() -> None:
    """Main function to run example usage with improved user experience."""
    logger.info("🎯 Transcription Analyzer - Example Usage")
    logger.info("=" * 50)
    logger.info(
        "This script demonstrates basic functionality of the transcription processor"
    )

    # Run examples and track success
    single_file_success = example_single_file()
    batch_success = example_batch_processing()
    show_output_structure()
    display_setup_instructions()

    # Summary of execution with clear feedback
    logger.info("\n📊 Execution Summary:")
    logger.info("=" * 30)
    if single_file_success:
        logger.info("✅ Single file example: SUCCESS")
    else:
        logger.info("❌ Single file example: FAILED")

    if batch_success:
        logger.info("✅ Batch processing example: SUCCESS")
    else:
        logger.info("❌ Batch processing example: FAILED")

    if not single_file_success and not batch_success:
        logger.warning("\n⚠️  No examples were successful. Please check:")
        logger.warning("   - API key configuration")
        logger.warning("   - File/directory existence")
        logger.warning("   - Dependencies installation")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n👋 Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        sys.exit(1)
