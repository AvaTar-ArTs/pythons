#!/usr/bin/env python3
"""
Advanced File Processor - Consolidated Processing Script

This script consolidates all file processing functionality from multiple processing scripts
into a comprehensive, feature-rich file processing tool.
"""

import os
import sys
import logging
import argparse
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Union
from concurrent.futures import ThreadPoolExecutor
import time

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("file_processing.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class AdvancedFileProcessor:
    """Comprehensive file processing tool with multiple processing modes."""

    def __init__(self):
        """__init__ function."""

        self.client = client
        self.supported_audio_formats = [".mp3", ".mp4", ".wav", ".m4a", ".flac"]
        self.supported_image_formats = [
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".bmp",
            ".tiff",
        ]

    def convert_mp4_to_mp3(self, mp4_path: Path, quality: str = "0") -> Optional[Path]:
        """Convert MP4 to MP3 using ffmpeg."""
        mp3_path = mp4_path.with_suffix(".mp3")
        if mp3_path.exists():
            logger.info(f"MP3 already exists: {mp3_path}")
            return mp3_path

        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    str(mp4_path),
                    "-q:a",
                    quality,
                    "-map",
                    "a",
                    str(mp3_path),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            logger.info(f"Converted {mp4_path.name} to MP3")
            return mp3_path
        except Exception as e:
            logger.error(f"Error converting {mp4_path}: {e}")
            return None

    def convert_mp3_to_mp4(
        self, mp3_path: Path, image_path: Optional[Path] = None
    ) -> Optional[Path]:
        """Convert MP3 to MP4 with optional cover image."""
        mp4_path = mp3_path.with_suffix(".mp4")
        if mp4_path.exists():
            logger.info(f"MP4 already exists: {mp4_path}")
            return mp4_path

        try:
            if image_path and image_path.exists():
                # Convert with cover image
                subprocess.run(
                    [
                        "ffmpeg",
                        "-loop",
                        "1",
                        "-i",
                        str(image_path),
                        "-i",
                        str(mp3_path),
                        "-c:v",
                        "libx264",
                        "-tune",
                        "stillimage",
                        "-c:a",
                        "aac",
                        "-b:a",
                        "192k",
                        "-pix_fmt",
                        "yuv420p",
                        "-shortest",
                        str(mp4_path),
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            else:
                # Convert without image (black screen)
                subprocess.run(
                    [
                        "ffmpeg",
                        "-f",
                        "lavfi",
                        "-i",
                        "color=c=black:s=1280x720:r=1",
                        "-i",
                        str(mp3_path),
                        "-c:v",
                        "libx264",
                        "-c:a",
                        "aac",
                        "-b:a",
                        "192k",
                        "-shortest",
                        str(mp4_path),
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

            logger.info(f"Converted {mp3_path.name} to MP4")
            return mp4_path
        except Exception as e:
            logger.error(f"Error converting {mp3_path}: {e}")
            return None

    def split_audio(
        self, file_path: Path, segment_length: int = CONSTANT_300
    ) -> List[Path]:
        """Split audio into smaller segments."""
        output_dir = file_path.parent / "segments"
        output_dir.mkdir(exist_ok=True)

        file_name_no_ext = file_path.stem
        command = [
            "ffmpeg",
            "-i",
            str(file_path),
            "-f",
            "segment",
            "-segment_time",
            str(segment_length),
            "-c",
            "copy",
            str(output_dir / f"{file_name_no_ext}_%03d.mp3"),
        ]

        try:
            subprocess.run(command, check=True)
            segments = sorted(list(output_dir.glob("*.mp3")))
            logger.info(f"Split {file_path.name} into {len(segments)} segments")
            return segments
        except Exception as e:
            logger.error(f"Error splitting {file_path}: {e}")
            return []

    def upscale_image(self, image_path: Path, scale_factor: int = 2) -> Optional[Path]:
        """Upscale image using ffmpeg."""
        output_path = (
            image_path.parent / f"{image_path.stem}_upscaled{image_path.suffix}"
        )

        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    str(image_path),
                    "-vf",
                    f"scale=iw*{scale_factor}:ih*{scale_factor}",
                    str(output_path),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            logger.info(f"Upscaled {image_path.name} by {scale_factor}x")
            return output_path
        except Exception as e:
            logger.error(f"Error upscaling {image_path}: {e}")
            return None

    def extract_metadata(self, file_path: Path) -> Dict:
        """Extract metadata from media file using ffprobe."""
        try:
            result = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "quiet",
                    "-print_format",
                    "json",
                    "-show_format",
                    "-show_streams",
                    str(file_path),
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            import json

            metadata = json.loads(result.stdout)

            # Extract useful information
            format_info = metadata.get("format", {})
            streams = metadata.get("streams", [])

            return {
                "filename": file_path.name,
                "duration": format_info.get("duration", "0"),
                "size": format_info.get("size", "0"),
                "bitrate": format_info.get("bit_rate", "0"),
                "format_name": format_info.get("format_name", "unknown"),
                "streams": len(streams),
            }
        except Exception as e:
            logger.error(f"Error extracting metadata from {file_path}: {e}")
            return {}

    def batch_convert(
        self,
        input_dir: Path,
        output_dir: Optional[Path] = None,
        conversion_type: str = "mp4_to_mp3",
    ) -> Dict[Path, Optional[Path]]:
        """Batch convert files in a directory."""
        if not output_dir:
            output_dir = input_dir / "converted"
        output_dir.mkdir(exist_ok=True)

        results = {}
        files_to_process = []

        # Find files to process
        if conversion_type == "mp4_to_mp3":
            files_to_process = list(input_dir.rglob("*.mp4"))
        elif conversion_type == "mp3_to_mp4":
            files_to_process = list(input_dir.rglob("*.mp3"))

        for file_path in files_to_process:
            try:
                if conversion_type == "mp4_to_mp3":
                    result = self.convert_mp4_to_mp3(file_path)
                elif conversion_type == "mp3_to_mp4":
                    result = self.convert_mp3_to_mp4(file_path)
                else:
                    result = None

                results[file_path] = result

            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                results[file_path] = None

        logger.info(f"Processed {len(files_to_process)} files")
        return results

    def organize_music_library(
        self, music_dir: Path, organize_by: str = "artist"
    ) -> bool:
        """Organize music library by specified criteria."""
        try:
            if organize_by == "artist":
                # Group by artist (extract from filename or metadata)
                for file_path in music_dir.rglob("*.mp3"):
                    # Simple organization by first part of filename
                    artist = file_path.stem.split(" - ")[0].strip()
                    artist_dir = music_dir / artist
                    artist_dir.mkdir(exist_ok=True)

                    new_path = artist_dir / file_path.name
                    if not new_path.exists():
                        shutil.move(str(file_path), str(new_path))
                        logger.info(f"Moved {file_path.name} to {artist}")

            elif organize_by == "genre":
                # Group by genre (would need metadata extraction)
                logger.info(
                    "Genre organization requires metadata extraction - not implemented"
                )
                return False

            logger.info(f"Organized music library by {organize_by}")
            return True

        except Exception as e:
            logger.error(f"Error organizing music library: {e}")
            return False


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Advanced File Processor")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument(
        "--mode",
        choices=["convert", "split", "upscale", "metadata", "organize"],
        required=True,
        help="Processing mode",
    )
    parser.add_argument("-o", "--output", help="Output file or directory")
    parser.add_argument(
        "--conversion",
        choices=["mp4_to_mp3", "mp3_to_mp4"],
        help="Conversion type for convert mode",
    )
    parser.add_argument(
        "--segment-length",
        type=int,
        default=CONSTANT_300,
        help="Segment length in seconds for split mode",
    )
    parser.add_argument(
        "--scale-factor", type=int, default=2, help="Scale factor for upscale mode"
    )
    parser.add_argument(
        "--organize-by",
        choices=["artist", "genre"],
        default="artist",
        help="Organization criteria for organize mode",
    )

    args = parser.parse_args()

    processor = AdvancedFileProcessor()
    input_path = Path(args.input)

    if args.mode == "convert" and args.conversion:
        if input_path.is_file():
            if args.conversion == "mp4_to_mp3":
                result = processor.convert_mp4_to_mp3(input_path)
            elif args.conversion == "mp3_to_mp4":
                result = processor.convert_mp3_to_mp4(input_path)

            if result:
                logger.info(f"Converted: {result}")
        elif input_path.is_dir():
            output_dir = Path(args.output) if args.output else input_path / "converted"
            results = processor.batch_convert(input_path, output_dir, args.conversion)
            logger.info(f"Converted {len([r for r in results.values() if r])} files")

    elif args.mode == "split" and input_path.is_file():
        segments = processor.split_audio(input_path, args.segment_length)
        logger.info(f"Split into {len(segments)} segments")
        for segment in segments:
            logger.info(f"  {segment}")

    elif args.mode == "upscale" and input_path.is_file():
        result = processor.upscale_image(input_path, args.scale_factor)
        if result:
            logger.info(f"Upscaled: {result}")

    elif args.mode == "metadata" and input_path.is_file():
        metadata = processor.extract_metadata(input_path)
        logger.info("Metadata:")
        for key, value in metadata.items():
            logger.info(f"  {key}: {value}")

    elif args.mode == "organize" and input_path.is_dir():
        success = processor.organize_music_library(input_path, args.organize_by)
        if success:
            logger.info(f"Organized music library by {args.organize_by}")

    else:
        logger.info("Invalid arguments. Use --help for usage information.")


if __name__ == "__main__":
    main()
