#!/usr/bin/env python3
"""
SUPER CLEAR FILE PATHS:
========================
SCRIPT LOCATION: /Users/steven/pythons/transcribe/analyze-mp3-transcript-prompts.py

OUTPUT DIRECTORIES (DO NOT CHANGE):
- TRANSCRIPTS: /Users/steven/Music/nocTurneMeLoDieS/transcript
- ANALYSIS:    /Users/steven/Music/nocTurneMeLoDieS/analysis

INPUT: Scans /Users/steven/Music/nocTurneMeLoDieS recursively for MP3 files
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
import json
import logging
import logging.handlers
import os
import random
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from termcolor import colored
from tqdm import tqdm


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib
from dotenv import load_dotenv

    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


# Constants


# ---------- CONFIG & UTILITIES ----------

# Setup logging first (before using logger)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load .env first
load_dotenv(os.path.expanduser("~/.env"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.info(colored("❌ OPENAI_API_KEY missing. Ensure ~/.env or environment has it.", "red"))
    sys.exit(1)

# Instantiate OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Safe slugify for filenames
def slugify(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[\/\\]+", "-", name)  # replace slashes
    name = re.sub(r"[^\w\-_\. ]+", "", name)  # allow word chars, dash, underscore, dot, space
    name = re.sub(r"\s+", "_", name)
    return name[:200]  # cap length

# Exponential backoff with full jitter
def retry_with_backoff(func, *args, max_attempts=4, base_delay=1.0, cap=10.0, **kwargs):
    for attempt in range(1, max_attempts + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt == max_attempts:
                raise
            sleep_time = min(cap, base_delay * (2 ** (attempt - 1)))
            # full jitter
            sleep_time = random.uniform(0, sleep_time)
            logging.warning(f"Attempt {attempt} failed with {e!r}; waiting {sleep_time:.2f}s before retry.")
            time.sleep(sleep_time)
def format_timestamp(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes:02d}:{sec:02d}"

def parse_transcript(transcript_text):
    segments = []
    for line in transcript_text.splitlines():
        if "--" in line:
            try:
                timestamp_part, text = line.split(": ", 1)
                segments.append({"timestamp": timestamp_part.strip(), "text": text.strip()})
            except ValueError:
                continue
    return segments
# ---------- TRANSCRIPTION & ANALYSIS ----------

def transcribe_audio(file_path: Path, model="whisper-1") -> str | None:
    if not file_path.is_file() or file_path.stat().st_size == 0:
        logging.error(f"Invalid or empty file: {file_path}")
        logger.info(colored(f"❌ {file_path.name} invalid/empty.", "red"))
        return None

    def _call():
        with open(file_path, "rb") as f:
            return client.audio.transcriptions.create(model=model, file=f, response_format="verbose_json")

    try:
        transcript_data = retry_with_backoff(_call, max_attempts=4)
    except Exception as e:
        logging.error(f"Failed to transcribe {file_path.name}: {e}")
        logger.info(colored(f"❌ Failed to transcribe {file_path.name}: {e}", "red"))
        return None

    segments = transcript_data.get("segments", [])
    lines = []
    for seg in segments:
        start = seg.get("start", 0)
        end = seg.get("end", 0)
        text = seg.get("text", "").strip()
        lines.append(f"{format_timestamp(start)} -- {format_timestamp(end)}: {text}")
    return "\n".join(lines)

def analyze_text_for_section(text: str, model="gpt-3.5-turbo") -> str | None:
    system_prompt = (
        "You are an experienced language and music expert. Your role is to provide an in-depth, structured analysis of song lyrics. "
        "Focus on uncovering the central context, emotional nuances, narrative arc, and deeper meanings. Analyze the emotional tone, "
        "narrative journey, and underlying themes, while highlighting any significant metaphors, symbols, and imagery. "
        "Explain how these elements interconnect and contribute to the overall emotional and narrative impact."
    )
    user_prompt = (
        "Please provide a thorough analysis of the following song transcript, structured as follows:\n"
        "(1) **Central Themes and Meaning**: Describe the main themes and the message conveyed by the song.\n"
        "(2) **Emotional Tone**: Highlight the emotional tone and any shifts throughout the lyrics.\n"
        "(3) **Artist's Intent**: Discuss what the artist might be aiming to express or achieve with these lyrics.\n"
        "(4) **Metaphors, Symbols, and Imagery**: Identify and explain notable metaphors, symbols, or imagery, and their significance.\n"
        "(5) **Overall Emotional and Narrative Experience**: Summarize how these elements create an impactful experience for the listener.\n"
        f"Transcript:\n{text}"
    )

    def _call():
        return client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1500,
            temperature=0.7)

    try:
        response = retry_with_backoff(_call, max_attempts=3)
    except Exception as e:
        logging.error(f"Analysis failed: {e}")
        logger.info(colored(f"⚠️ Analysis error: {e}", "yellow"))
        return None
    choice = response.choices[0]
    # Depending on API version, adjust access
    content = getattr(choice.message, "content", None) if hasattr(choice, "message") else choice.text
    return content.strip() if content else None

def link_timestamps_to_analysis(transcript_segments, analysis_text):
    linked = analysis_text
    for seg in transcript_segments:
        piece = seg["text"]
        if piece and piece in linked:
            linked = linked.replace(piece, f"{piece} [{seg['timestamp']}]")
    return linked

# ---------- MAIN PROCESSING ----------

def process_audio_file(:
    audio_file: Path,
    transcript_dir: Path,
    analysis_dir: Path,
    force: bool = False,
):
    safe_name = slugify(audio_file.stem)
    transcript_path = transcript_dir / f"{safe_name}_transcript.txt"
    analysis_path = analysis_dir / f"{safe_name}_analysis.txt"

    logger.info(colored(f"🎧 Processing {audio_file.name}", "cyan"))

    if transcript_path.exists() and analysis_path.exists() and not force:
        logger.info(colored(f"✔ Skipping {audio_file.name} (already done). Use --force to reprocess.", "green"))
        return

    transcript = transcribe_audio(audio_file)
    if not transcript:
        logger.info(colored(f"⚠️ Skipping {audio_file.name} due to transcription failure.", "yellow"))
        return

    transcript_dir.mkdir(parents=True, exist_ok=True)
    transcript_path.write_text(transcript, encoding="utf-8")
    logger.info(colored(f"✅ Transcript saved: {transcript_path.name}", "green"))

    transcript_segments = parse_transcript(transcript)

    analysis = analyze_text_for_section(transcript)
    if not analysis:
        logger.info(colored(f"⚠️ Skipping analysis for {audio_file.name}.", "yellow"))
        return

    linked = link_timestamps_to_analysis(transcript_segments, analysis)
    analysis_dir.mkdir(parents=True, exist_ok=True)
    analysis_path.write_text(f"# Analysis of {audio_file.name}\n\n{linked}", encoding="utf-8")
    logger.info(colored(f"📝 Analysis saved: {analysis_path.name}", "green"))

def check_conda_env(expected="ai-media"):
    current = os.environ.get("CONDA_DEFAULT_ENV", "")
    if expected and expected not in current:
        logger.info(colored(f"⚠️ You are in conda env '{current or 'none'}'; expected '{expected}'. Activate with: conda activate {expected}", "yellow"))
def load_progress_cache(cache_file: Path):
    try:
        if cache_file.exists():
            return json.loads(cache_file.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}

def save_progress_cache(cache_file: Path, data):
    try:
        cache_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception as e:
        logging.warning(f"Failed saving cache: {e}")

def process_audio_directory(audio_dir: Path, max_workers: int, force: bool, limit: int = None):
    # SUPER CLEAR: Output directories - DO NOT CHANGE THESE PATHS
    # Transcripts go to: /Users/steven/Music/nocTurneMeLoDieS/transcript
    # Analysis goes to: /Users/steven/Music/nocTurneMeLoDieS/analysis
    transcript_dir = Path("/Users/steven/Music/nocTurneMeLoDieS/transcript")
    analysis_dir = Path("/Users/steven/Music/nocTurneMeLoDieS/analysis")
    transcript_dir.mkdir(parents=True, exist_ok=True)
    analysis_dir.mkdir(parents=True, exist_ok=True)

    audio_files = sorted([p for p in audio_dir.rglob("*.mp3") if p.is_file()])
    if not audio_files:
        logger.info(colored("⚠️ No MP3s found in the directory.", "red"))
        return
    
    # Limit files for testing
    if limit:
        audio_files = audio_files[:limit]
        logger.info(colored(f"🧪 TEST MODE: Processing only {len(audio_files)} files", "yellow"))

    logger.info(colored(f"🗂 Found {len(audio_files)} MP3 files. Starting...", "green"))

    cache_file = audio_dir / ".processing_cache.json"
    cache = load_progress_cache(cache_file)

    def worker(path: Path):
        try:
            process_audio_file(path, transcript_dir, analysis_dir, force=force)
            cache_key = slugify(path.stem)
            cache[cache_key] = {"processed_at": time.time()}
            save_progress_cache(cache_file, cache)
        except Exception as e:
            logging.error(f"Unhandled error on {path.name}: {e}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        list(tqdm(executor.map(worker, audio_files), total=len(audio_files), desc="Files"))

# ---------- ENTRYPOINT ----------

def main():
    parser = argparse.ArgumentParser(description="Transcribe and analyze MP3 library.")
    parser.add_argument(
        "-d",
        "--audio-dir",
        type=str,
        default=Path(str(Path.home()) + "/Music/nocTurneMeLoDieS/MP3/"),
        help="Directory containing MP3s (recursive).")
    parser.add_argument(
        "-w", "--max-workers", type=int, default=4, help="Number of concurrent transcription workers."
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="Reprocess even if transcript+analysis exist."
    )
    parser.add_argument(
        "-l", "--limit", type=int, default=None, help="Limit number of files to process (for testing)."
    )
    args = parser.parse_args()

    check_conda_env("ai-media")

    audio_dir = Path(args.audio_dir).expanduser()
    if not audio_dir.is_dir():
        logger.info(colored(f"❌ Audio directory invalid: {audio_dir}", "red"))
        sys.exit(1)

    # Setup logging with rotation
    log_handler = logging.handlers.RotatingFileHandler(
        "transcription_analysis_errors.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    log_handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(log_handler)

    # Also echo warnings/errors to console
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    root.addHandler(console)

    process_audio_directory(audio_dir, max_workers=args.max_workers, force=args.force, limit=args.limit)


if __name__ == "__main__":
    main()
