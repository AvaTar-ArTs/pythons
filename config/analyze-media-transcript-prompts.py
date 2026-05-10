#!/usr/bin/env python3
"""
Media Transcription and Analysis Tool
======================================
Transcribes audio/video files using OpenAI Whisper and analyzes content using GPT.
Supports MP3, MP4, and other media formats.
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
                            value = value.strip().strip('\'').strip("\'")
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

import argparse
import logging
import logging.handlers
import os
import random
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from termcolor import colored
from tqdm import tqdm

# --- Load API Keys ---
# Load from ~/.env.d/ first
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)

# Load from ~/.env as a fallback
env_path = Path.home() / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# --- Constants & Globals ---
CONSTANT_1500 = 1500
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup a logger for the module
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

if not OPENAI_API_KEY:
    logger.error(colored("❌ OPENAI_API_KEY missing. Ensure ~/.env.d/ or ~/.env has it.", "red"))
    sys.exit(1)

# Instantiate OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Supported media extensions
MEDIA_EXTENSIONS = {".mp3", ".mp4", ".m4a", ".wav", ".flac", ".webm", ".ogg", ".mov", ".avi"}


# --- Utility Functions ---

def slugify(name: str) -> str:
    """Create a safe filename from a string."""
    name = name.strip().lower()
    name = re.sub(r"[\/\\]+", "-", name)  # replace slashes
    name = re.sub(r"[^\w\-_\. ]+", "", name)  # allow word chars, dash, underscore, dot, space
    name = re.sub(r"\s+", "_", name)
    return name[:200]  # cap length


def retry_with_backoff(func, *args, max_attempts=4, base_delay=1.0, cap=10.0, **kwargs):
    """Retry a function with exponential backoff and full jitter."""
    for attempt in range(1, max_attempts + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt == max_attempts:
                logger.error(f"Final attempt failed for {func.__name__}: {e}")
                raise
            sleep_time = min(cap, base_delay * (2 ** (attempt - 1)))
            sleep_time = random.uniform(0, sleep_time)  # Full jitter
            logger.warning(
                f"Attempt {attempt} failed with {e!r}; waiting {sleep_time:.2f}s before retry."
            )
            time.sleep(sleep_time)


def format_timestamp(seconds: float) -> str:
    """Convert seconds into the format MM:SS."""
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes:02d}:{sec:02d}"


# --- Core API Functions ---

def transcribe_file(file_path: Path) -> str | None:
    """Transcribe audio or video using OpenAI Whisper."""
    logger.info(colored(f"Transcribing {file_path.name}...", "cyan"))
    
    if not file_path.is_file() or file_path.stat().st_size == 0:
        logger.error(colored(f"❌ Invalid or empty file: {file_path.name}", "red"))
        return None

    def _call():
        with open(file_path, "rb") as f:
            return client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="verbose_json"
            )

    try:
        transcript_data = retry_with_backoff(_call, max_attempts=4)
    except Exception as e:
        logger.error(f"Failed to transcribe {file_path.name}: {e}")
        return None

    # Format transcript with timestamps
    segments = transcript_data.get("segments", [])
    transcript_lines = []
    for seg in segments:
        start = seg.get("start", 0)
        end = seg.get("end", 0)
        text = seg.get("text", "").strip()
        transcript_lines.append(
            f"{format_timestamp(start)} -- {format_timestamp(end)}: {text}"
        )
    
    return "\n".join(transcript_lines)


def analyze_text(text: str, file_name: str, model: str = "gpt-4o") -> str | None:
    """Analyze the transcribed text using OpenAI GPT."""
    logger.info(colored(f"Analyzing {file_name}...", "cyan"))
    
    system_prompt = (
        "You are an expert in multimedia analysis and storytelling. Your task is to provide a detailed and structured analysis "
        "of video and audio content, focusing on themes, emotional tone, narrative structure, artistic intent, and audience impact. "
        "Analyze how visual elements (e.g., imagery, colors, transitions) interact with audio elements (e.g., dialogue, music, sound effects) "
        "to convey meaning and evoke emotions. Highlight storytelling techniques and assess their effectiveness in engaging the audience."
    )
    
    user_prompt = (
        "Please provide a comprehensive analysis of the following transcript, structured as follows:\n\n"
        "1. **Central Themes and Core Message**: Identify the main themes and the primary message or story being conveyed.\n"
        "2. **Emotional Tone and Atmosphere**: Describe the emotional tone, mood, and atmosphere throughout the content. Note any shifts or transitions.\n"
        "3. **Narrative Structure**: Analyze the narrative arc, pacing, and how the story unfolds. Are there distinct acts or sections?\n"
        "4. **Artistic and Creative Intent**: Discuss what the creator(s) might be aiming to express, communicate, or achieve with this content.\n"
        "5. **Metaphors, Symbols, and Motifs**: Identify and explain notable metaphors, symbols, or visual/audio motifs that enhance the narrative or emotional impact.\n"
        "6. **Storytelling Techniques**: Identify specific techniques used, such as pacing, transitions, visual effects, or sound design. How do they contribute to the overall experience?\n"
        "7. **Interplay Between Visuals and Audio**: Analyze how visuals and audio work together to create meaning and impact. Are there any standout moments?\n"
        "8. **Audience Engagement and Impact**: Evaluate how effectively the content captures and holds attention. How well does it resonate with its intended audience?\n"
        "9. **Overall Effectiveness**: Summarize how these elements combine to create a cohesive, immersive, and impactful experience for the viewer.\n\n"
        f"Transcript:\n{text}"
    )

    def _call():
        return client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=CONSTANT_1500,
            temperature=0.7,
        )

    try:
        response = retry_with_backoff(_call, max_attempts=3)
    except Exception as e:
        logger.error(f"Analysis failed for {file_name}: {e}")
        return None

    choice = response.choices[0]
    content = getattr(choice.message, "content", None) if hasattr(choice, "message") else getattr(choice, "text", None)
    return content.strip() if content else None


# --- Processing Functions ---

def process_media_file(:
    media_file: Path,
    transcript_dir: Path,
    analysis_dir: Path,
    force: bool = False,
    analysis_model: str = "gpt-4o",
):
    """Process a single media file: transcribe and analyze."""
    try:
        safe_name = slugify(media_file.stem)
        transcript_file_path = transcript_dir / f"{safe_name}_transcript.txt"
        analysis_file_path = analysis_dir / f"{safe_name}_analysis.txt"

        logger.info(colored(f"🎬 Processing {media_file.name}", "cyan"))

        # Check if already processed
        if transcript_file_path.exists() and analysis_file_path.exists() and not force:
            logger.info(
                colored(f"✔ Skipping {media_file.name} (already processed)", "green")
            )
            return

        # Step 1: Transcribe the media file
        transcript = transcribe_file(media_file)
        if not transcript:
            logger.warning(
                colored(f"⚠️ Transcription failed for {media_file.name}, skipping analysis.", "yellow")
            )
            return

        transcript_dir.mkdir(parents=True, exist_ok=True)
        transcript_file_path.write_text(transcript, encoding="utf-8")
        logger.info(colored(f"✅ Transcript saved: {transcript_file_path.name}", "green"))

        # Step 2: Analyze the transcript
        analysis = analyze_text(transcript, media_file.name, model=analysis_model)
        if not analysis:
            logger.warning(colored(f"⚠️ Analysis failed for {media_file.name}.", "yellow"))
            return

        analysis_dir.mkdir(parents=True, exist_ok=True)
        analysis_file_path.write_text(analysis, encoding="utf-8")
        logger.info(colored(f"✅ Analysis saved: {analysis_file_path.name}", "green"))

    except Exception as e:
        logger.error(f"Unhandled error processing {media_file.name}: {e}")


def process_media_directory(:
    media_dir: Path, max_workers: int = 4, force: bool = False, analysis_model: str = "gpt-4o"
):
    """Process all media files in a directory recursively."""
    transcript_dir = media_dir / "transcript"
    analysis_dir = media_dir / "analysis"
    transcript_dir.mkdir(parents=True, exist_ok=True)
    analysis_dir.mkdir(parents=True, exist_ok=True)

    # Find all media files
    media_files = []
    for ext in MEDIA_EXTENSIONS:
        media_files.extend(media_dir.rglob(f"*{ext}"))
    
    media_files = sorted([p for p in media_files if p.is_file()])
    
    if not media_files:
        logger.error(colored("❌ No media files found in the directory.", "red"))
        return

    logger.info(
        colored(f"Found {len(media_files)} media files. Starting processing...", "green")
    )

    # Use ThreadPoolExecutor for concurrent processing
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                process_media_file,
                media_file,
                transcript_dir,
                analysis_dir,
                force,
                analysis_model,
            )
            for media_file in media_files
        ]
        
        # Use tqdm to show progress
        for future in tqdm(futures, desc="Processing Files", total=len(media_files)):
            future.result()  # Wait for completion and handle any exceptions

    logger.info(colored("All processing complete!", "green"))


def setup_logging():
    """Configure root logger for console and file output."""
    log_file = "media_transcription_analysis.log"
    log_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    log_handler.setFormatter(formatter)
    
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(log_handler)
    
    # Also echo to console
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    root.addHandler(console)


# --- Entry Point ---

def main():
    parser = argparse.ArgumentParser(
        description="Transcribe and analyze media files (MP3, MP4, etc.) using OpenAI Whisper and GPT."
    )
    parser.add_argument(
        "media_dir",
        type=str,
        nargs="?",
        default=str(Path.home() / "Music" / "nocTurneMeLoDieS"),
        help="Path to the directory containing MP3/MP4 files. Default: ~/Music/nocTurneMeLoDieS",
    )
    parser.add_argument(
        "-w",
        "--max-workers",
        type=int,
        default=4,
        help="Number of concurrent workers. Default: 4",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force reprocessing of files even if output already exists.",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="gpt-4o",
        help="OpenAI model to use for analysis (e.g., gpt-3.5-turbo, gpt-4o). Default: gpt-4o",
    )
    args = parser.parse_args()

    setup_logging()

    media_dir_path = Path(args.media_dir).expanduser()
    if not media_dir_path.is_dir():
        logger.error(colored(f"❌ Invalid directory: {media_dir_path}", "red"))
        sys.exit(1)

    # Process the media files in the provided directory
    process_media_directory(
        media_dir_path, max_workers=args.max_workers, force=args.force, analysis_model=args.model
    )


if __name__ == "__main__":
    main()
