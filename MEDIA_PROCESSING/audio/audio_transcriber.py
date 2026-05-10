#!/usr/bin/env python3
"""
Unified Audio Transcriber
Supports both OpenAI Whisper (cloud) and faster-whisper (local)

Usage:
    # OpenAI Whisper (cloud)
    python audio_transcriber.py audio.mp3 --provider openai

    # Local faster-whisper
    python audio_transcriber.py audio.mp3 --provider local --model medium

    # Batch process directory
    python audio_transcriber.py /path/to/audio --batch
"""

import os
import logging
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from enum import Enum

from dotenv import load_dotenv
from tqdm import tqdm

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
                            value = value.strip().strip('\'').strip("\'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")


load_env_d()

# Also load from ~/.env as fallback using dotenv
load_dotenv(os.path.expanduser("~/.env"))

# Optional imports
try:
    from openai import OpenAI

    HAVE_OPENAI = True
except ImportError:
    HAVE_OPENAI = False

try:
    from faster_whisper import WhisperModel

    HAVE_FASTER_WHISPER = True
except ImportError:
    HAVE_FASTER_WHISPER = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("transcription.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class TranscriptionProvider(Enum):
    OPENAI = "openai"
    LOCAL = "local"


class AudioTranscriber:
    """Unified transcription tool supporting multiple backends."""

    def __init__(self, provider: TranscriptionProvider = TranscriptionProvider.OPENAI):
        self.provider = provider
        self.supported_formats = [".mp3", ".mp4", ".wav", ".m4a", ".flac", ".aac"]

        if provider == TranscriptionProvider.OPENAI:
            if not HAVE_OPENAI:
                raise ImportError("openai package required for OpenAI provider")
            if not api_key:
                raise ValueError(
                    "OPENAI_API_KEY not found in environment. "
                    "Ensure it's set in ~/.env.d/*.env or ~/.env"
                )
            self.client = OpenAI(api_key=api_key)
        elif provider == TranscriptionProvider.LOCAL:
            if not HAVE_FASTER_WHISPER:
                raise ImportError("faster-whisper package required for local provider")

    def format_timestamp(self, seconds: float) -> str:
        """Convert seconds to MM:SS format."""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

    def format_timestamp_srt(self, seconds: float) -> str:
        """Convert seconds to SRT format (HH:MM:SS,mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

    def transcribe_openai(:
        self,
        file_path: Path,
        model: str = "whisper-1",
        response_format: str = "verbose_json",
    ) -> Optional[Dict]:
        """Transcribe using OpenAI Whisper."""
        try:
            with open(file_path, "rb") as audio_file:
                logger.info(f"Transcribing {file_path.name} with OpenAI Whisper...")
                transcript_data = self.client.audio.transcriptions.create(
                    model=model, file=audio_file, response_format=response_format
                )
                return transcript_data
        except Exception as e:
            logger.error(f"Error transcribing {file_path}: {e}")
            return None

    def transcribe_local(:
        self,
        file_path: Path,
        model: str = "medium",
        device: str = "cpu",
        compute_type: str = "int8",
        beam_size: int = 5,
        vad_filter: bool = True,
    ) -> Optional[Tuple[str, List[Tuple[float, float, str]]]]:
        """Transcribe using faster-whisper (local)."""
        try:
            logger.info(
                f"Transcribing {file_path.name} with local Whisper ({model})..."
            )
            whisper_model = WhisperModel(
                model, device=device, compute_type=compute_type
            )
            segments, info = whisper_model.transcribe(
                str(file_path),
                vad_filter=vad_filter,
                beam_size=beam_size,
                condition_on_previous_text=True,
                word_timestamps=False,
            )

            out_segments = []
            for seg in segments:
                out_segments.append((seg.start, seg.end, seg.text.strip()))

            return info.language, out_segments
        except Exception as e:
            logger.error(f"Error transcribing {file_path}: {e}")
            return None

    def transcribe(:
        self, file_path: Path, model: Optional[str] = None, **kwargs
    ) -> Optional[Union[Dict, Tuple[str, List[Tuple[float, float, str]]]]]:
        """Transcribe audio file using configured provider."""
        if self.provider == TranscriptionProvider.OPENAI:
            return self.transcribe_openai(
                file_path, model=model or "whisper-1", **kwargs
            )
        else:
            return self.transcribe_local(file_path, model=model or "medium", **kwargs)

    def transcribe_with_timestamps(self, file_path: Path, **kwargs) -> Optional[str]:
        """Transcribe audio and return formatted text with timestamps."""
        result = self.transcribe(file_path, **kwargs)

        if not result:
            return None

        transcript_lines = []

        if self.provider == TranscriptionProvider.OPENAI:
            # OpenAI returns dict with segments
            if isinstance(result, dict) and "segments" in result:
                for segment in result.segments:
                    start = segment["start"]
                    end = segment["end"]
                    text = segment["text"]
                    transcript_lines.append(
                        f"{self.format_timestamp(start)} -- {self.format_timestamp(end)}: {text}"
                    )
        else:
            # Local returns (language, segments)
            if isinstance(result, tuple):
                _, segments = result
                for start, end, text in segments:
                    transcript_lines.append(
                        f"{self.format_timestamp(start)} -- {self.format_timestamp(end)}: {text}"
                    )

        return "\n".join(transcript_lines)

    def save_transcript_srt(:
        self, segments: List[Tuple[float, float, str]], output_path: Path
    ) -> None:
        """Save transcript in SRT subtitle format."""
        with open(output_path, "w", encoding="utf-8") as f:
            for idx, (start, end, text) in enumerate(segments, 1):
                f.write(f"{idx}\n")
                f.write(
                    f"{self.format_timestamp_srt(start)} --> {self.format_timestamp_srt(end)}\n"
                )
                f.write(f"{text}\n\n")

    def convert_mp4_to_mp3(self, mp4_path: Path) -> Optional[Path]:
        """Convert MP4 to MP3 using ffmpeg."""
        mp3_path = mp4_path.with_suffix(".mp3")
        if mp3_path.exists():
            logger.info(f"MP3 already exists: {mp3_path.name}")
            return mp3_path

        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    str(mp4_path),
                    "-q:a",
                    "0",
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

    def split_audio(self, file_path: Path, segment_length: int = 300) -> List[Path]:
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
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            segments = sorted(list(output_dir.glob("*.mp3")))
            logger.info(f"Split into {len(segments)} segments")
            return segments
        except Exception as e:
            logger.error(f"Error splitting {file_path}: {e}")
            return []

    def batch_transcribe(:
        self,
        input_dir: Path,
        output_dir: Optional[Path] = None,
        force: bool = False,
    ) -> Dict[Path, str]:
        """Transcribe all audio files in a directory."""
        if not output_dir:
            output_dir = input_dir / "transcripts"
        output_dir.mkdir(exist_ok=True)

        results = {}
        audio_files = []

        # Find all audio files
        for ext in self.supported_formats:
            audio_files.extend(input_dir.rglob(f"*{ext}"))

        logger.info(f"Found {len(audio_files)} audio files")

        for file_path in tqdm(audio_files, desc="Transcribing files"):
            try:
                # Check if already processed
                output_file = output_dir / f"{file_path.stem}_transcript.txt"
                if output_file.exists() and not force:
                    logger.info(f"Skipping {file_path.name} (already exists)")
                    continue

                # Convert MP4 to MP3 if needed
                if file_path.suffix.lower() == ".mp4":
                    mp3_path = self.convert_mp4_to_mp3(file_path)
                    if mp3_path:

                # Transcribe
                transcript = self.transcribe_with_timestamps(file_path)
                if transcript:
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(transcript)
                    results[file_path] = transcript
                    logger.info(f"✓ Transcribed {file_path.name}")

            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                results[file_path] = f"Error: {str(e)}"

        return results


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Unified Audio Transcriber")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("-o", "--output", help="Output directory (for batch mode)")
    parser.add_argument(
        "--provider",
        choices=["openai", "local"],
        default="openai",
        help="Transcription provider (default: openai)",
    )
    parser.add_argument(
        "--model",
        help="Model name (whisper-1 for OpenAI, tiny/base/small/medium/large-v2 for local)",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process directory in batch mode",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reprocess existing transcripts",
    )
    parser.add_argument(
        "--convert",
        action="store_true",
        help="Convert MP4 to MP3 first",
    )
    parser.add_argument(
        "--split",
        type=int,
        help="Split audio into segments of specified length (seconds)",
    )

    args = parser.parse_args()

    try:
        provider = TranscriptionProvider(args.provider)
        transcriber = AudioTranscriber(provider=provider)
    except (ImportError, ValueError) as e:
        logger.error(f"Failed to initialize transcriber: {e}")
        return

    input_path = Path(args.input)

    if input_path.is_file():
        if args.convert and input_path.suffix.lower() == ".mp4":
            mp3_path = transcriber.convert_mp4_to_mp3(input_path)
            if mp3_path:
                input_path = mp3_path

        if args.split:
            segments = transcriber.split_audio(input_path, args.split)
            logger.info(f"Split into {len(segments)} segments")
            for segment in segments:
                logger.info(f"  {segment}")

        transcript = transcriber.transcribe_with_timestamps(
            input_path, model=args.model
        )
        if transcript:
            print(transcript)

    elif input_path.is_dir() or args.batch:
        output_dir = Path(args.output) if args.output else input_path / "transcripts"
        results = transcriber.batch_transcribe(input_path, output_dir, force=args.force)
        logger.info(f"Transcribed {len(results)} files. Results saved to {output_dir}")

    else:
        logger.error(f"Invalid input: {input_path}")


if __name__ == "__main__":
    main()
