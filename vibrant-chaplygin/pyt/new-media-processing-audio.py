#!/usr/bin/env python3
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
env_dir = Path.home() / ".env.d"
if env_dir.exists():
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
logger = logging.getLogger(__name__)

# --- Check for API Key ---
if not OPENAI_API_KEY:
    logger.error(colored("❌ OPENAI_API_KEY missing. Ensure ~/.env or ~/.env.d/ has it.", "red"))
    sys.exit(1)

# Instantiate OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


# --- Utility Functions ---

def slugify(name: str) -> str:
    """Safe slugify for filenames."""
    name = name.strip().lower()
    name = re.sub(r"[\/\\]+", "-", name)  # replace slashes
    name = re.sub(r"[^\w\-_\.]+", "", name)  # remove unsafe chars
    name = re.sub(r"\s+", "_", name)
    return name[:200]  # cap length

def retry_with_backoff(func, *args, max_attempts=4, base_delay=1.0, cap=10.0, **kwargs):
    """Exponential backoff with full jitter for API calls."""
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
    
    if not file_path.is_file() or file_path.stat().st_size < 100:
        logger.warning(colored(f"Skipping empty or invalid file: {file_path.name}", "yellow"))
        return None

    def _call():
        with open(file_path, "rb") as media_file:
            # The method is .transcriptions.create(), not .transcribe()
            return client.audio.transcriptions.create(
                model="whisper-1", file=media_file, response_format="verbose_json"
            )

    try:
        transcript_data = retry_with_backoff(_call)
    except Exception as e:
        logger.error(f"Error transcribing {file_path.name}: {e}")
        return None

    # Build the transcript with timestamps
    transcript_with_timestamps = []
    for segment in transcript_data.get("segments", []):
        start_time = segment.get("start", 0)
        end_time = segment.get("end", 0)
        text = segment.get("text", "").strip()
        transcript_with_timestamps.append(
            f"{format_timestamp(start_time)}-{format_timestamp(end_time)}: {text}"
        )

    return "\n".join(transcript_with_timestamps)


def analyze_text(text: str, file_name: str) -> str | None:
    """Analyze the transcribed text using OpenAI GPT."""
    logger.info(colored(f"Analyzing {file_name}...", "cyan"))
    
    def _call():
        return client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert in multimedia analysis and storytelling. Your task is to provide a detailed and structured analysis "
                        "of video and audio content, focusing on themes, emotional tone, narrative structure, artistic intent, and audience impact. "
                        "Analyze how visual elements (e.g., imagery, colors, transitions) interact with audio elements (e.g., dialogue, music, sound effects) "
                        "to convey meaning and evoke emotions. Highlight storytelling techniques and assess their effectiveness in engaging viewers."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Analyze the following transcript from the file '{file_name}'. Provide a comprehensive analysis covering:\n\n"
                        "1. **Central Themes and Messages**: Identify the primary ideas or messages conveyed. How do they connect to the broader narrative?\n"
                        "2. **Emotional Tone**: What emotions are evoked, and how are they conveyed through the combination of audio and visuals?\n"
                        "3. **Narrative Arc**: Describe how this section contributes to the overall story or progression. Are there key turning points or developments?\n"
                        "4. **Creator's Intent**: What is the likely purpose or message the creator is trying to communicate? Is it to entertain, inform, inspire, or persuade?\n"
                        "5. **Significant Metaphors, Symbols, and Imagery**: Highlight notable metaphors, symbols, or visual/audio motifs that enhance the narrative or emotional impact.\n"
                        "6. **Storytelling Techniques**: Identify specific techniques used, such as pacing, transitions, visual effects, or sound design. How do they contribute to the overall experience?\n"
                        "7. **Interplay Between Visuals and Audio**: Analyze how visuals and audio work together to create meaning and impact. Are there any standout moments?\n"
                        "8. **Audience Engagement and Impact**: Evaluate how effectively the content captures and holds attention. How well does it resonate with its intended audience?\n"
                        "9. **Overall Effectiveness**: Summarize how these elements combine to create a cohesive, immersive, and impactful experience for the viewer.\n\n"
                        f"Transcript:\n{text}"
                    ),
                },
            ],
            max_tokens=CONSTANT_1500,
            temperature=0.7,
        )

    try:
        response = retry_with_backoff(_call)
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error analyzing {file_name}: {e}")
        return None


# --- Main Processing Functions ---

def process_media_file(
    media_file: Path, transcript_dir: Path, analysis_dir: Path, force: bool
):
    """
    Worker function to process a single media file.
    Transcribes, analyzes, and saves the output.
    """
    try:
        # Use a safe, slugified name for output files
        safe_name = slugify(media_file.stem)
        transcript_file_path = transcript_dir / f"{safe_name}_transcript.txt"
        analysis_file_path = analysis_dir / f"{safe_name}_analysis.txt"

        # Skip if already processed and --force is not used
        if (
            not force
            and transcript_file_path.exists()
            and analysis_file_path.exists()
        ):
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

        transcript_file_path.write_text(transcript, encoding="utf-8")
        logger.info(colored(f"✅ Transcript saved: {transcript_file_path.name}", "green"))

        # Step 2: Analyze the transcript
        analysis = analyze_text(transcript, media_file.name)
        if not analysis:
            logger.warning(colored(f"⚠️ Analysis failed for {media_file.name}.", "yellow"))
            return

        analysis_file_path.write_text(analysis, encoding="utf-8")
        logger.info(colored(f"✅ Analysis saved: {analysis_file_path.name}", "green"))

    except Exception as e:
        logger.error(f"Unhandled error processing {media_file.name}: {e}")


def process_media_directory(
    media_dir: Path, max_workers: int, force: bool
):
    """
    Finds all media files and processes them using a thread pool.
    """
    # Auto-create transcript and analysis folders within the source directory
    transcript_dir = media_dir / "transcript"
    analysis_dir = media_dir / "analysis"
    transcript_dir.mkdir(exist_ok=True)
    analysis_dir.mkdir(exist_ok=True)

    logger.info(f"Scanning for media in: {media_dir}")
    logger.info(f"Transcripts will be saved to: {transcript_dir}")
    logger.info(f"Analyses will be saved to: {analysis_dir}")

    # Find all .mp3 and .mp4 files recursively
    media_files = []
    for p in media_dir.rglob("*"):
        if p.suffix.lower() in [".mp3", ".mp4"]:
            # Ensure we don't re-process files already in our output dirs
            if p.parent.name not in ["transcript", "analysis"]:
                media_files.append(p)

    if not media_files:
        logger.warning(colored("⚠️ No .mp3 or .mp4 files found to process.", "red"))
        return

    logger.info(
        colored(f"Found {len(media_files)} media files. Starting processing...", "green")
    )

    # Use ThreadPoolExecutor for concurrent processing
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Create a list of futures
        futures = [
            executor.submit(
                process_media_file,
                media_file,
                transcript_dir,
                analysis_dir,
                force,
            )
            for media_file in media_files
        ]
        
        # Use tqdm to show progress
        for _ in tqdm(
            executor.map(
                lambda f: f.result(), futures
            ),  # Using map to process results as they complete
            total=len(media_files),
            desc="Processing Files",
        ):
            pass

    logger.info(colored("All processing complete!", "green"))


def setup_logging():
    """Configure root logger for console and file output."""
    log_file = "media_processing.log"
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.WARNING) # Log warnings and errors to file
    
    # Console handler for INFO
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO) # Show info-level messages on console
    
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


# --- Entrypoint ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transcribe and analyze all MP3/MP4 files in a directory."
    )
    parser.add_argument(
        "media_dir",
        type=str,
        help="Path to the directory containing MP3/MP4 files.",
    )
    parser.add_Ggument(
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
    args = parser.parse_args()

    setup_logging()

    media_dir_path = Path(args.media_dir).expanduser()
    if not media_dir_path.is_dir():
        logger.error(colored(f"❌ Invalid directory: {media_dir_path}", "red"))
        sys.exit(1)

    # Process the media files in the provided directory
    process_media_directory(
        media_dir_path, max_workers=args.max_workers, force=args.force
    )