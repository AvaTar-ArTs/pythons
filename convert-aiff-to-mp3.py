"""
Convert Mp

This module provides functionality for convert mp.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Convert AIFF files to MP3 format
"""

import os
import subprocess
from pathlib import Path


def convert_aiff_to_mp3(input_file: str, output_file: str) -> bool:
    """Convert AIFF file to MP3 using ffmpeg"""
    try:
        cmd = [
            "ffmpeg",
            "-i",
            input_file,
            "-acodec",
            "libmp3lame",
            "-ab",
            "128k",
            output_file,
            "-y",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0

    except Exception as e:
        logger.info(f"Conversion error: {e}")
        return False


def convert_all_aiff_files():
    """Convert all AIFF files in the audio directory to MP3"""
    audio_dir = Path("as_a_man_thinketh_audio_system")
    mp3_dir = Path("as_a_man_thinketh_audio_mp3")
    mp3_dir.mkdir(exist_ok=True)

    logger.info("Converting AIFF files to MP3...")

    # Find all AIFF files
    aiff_files = list(audio_dir.rglob("*.aiff"))
    logger.info(f"Found {len(aiff_files)} AIFF files")

    converted_count = 0

    for aiff_file in aiff_files:
        # Create corresponding MP3 path
        relative_path = aiff_file.relative_to(audio_dir)
        mp3_file = mp3_dir / relative_path.with_suffix(".mp3")

        # Create directory if needed
        mp3_file.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Converting {aiff_file.name}...", end=" ")

        if convert_aiff_to_mp3(str(aiff_file), str(mp3_file)):
            logger.info("✓")
            converted_count += 1
        else:
            logger.info("✗")

    logger.info(f"\n✅ Converted {converted_count}/{len(aiff_files)} files to MP3")
    logger.info(f"MP3 files saved to: {mp3_dir}")


if __name__ == "__main__":
    convert_all_aiff_files()
