#!/usr/bin/env python3
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
                            value = value.strip().strip('"').strip("'")
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
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, APIConnectionError, RateLimitError, APIStatusError, AuthenticationError
from termcolor import colored
from tqdm import tqdm


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib

    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


# Constants
CONSTANT_200 = 200
CONSTANT_1500 = 1500


# ---------- CONFIG & UTILITIES ----------

# Setup logging first
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
    name = re.sub(r"[\/\\\\]+", "-", name)  # replace slashes
    name = re.sub(r"[^\w\-_\. ]+", "", name)  # allow word chars, dash, underscore, dot, space
    name = re.sub(r"\s+", "_", name)
    return name[:CONSTANT_200]  # cap length

# Enhanced Retry Logic
def retry_with_backoff(func, *args, max_attempts=3, base_delay=5.0, backoff_type="linear", **kwargs):
    """
    Retry logic with specific handling for OpenAI errors.
    - max_attempts: 3 (default)
    - base_delay: 5s (default)
    - backoff_type: "linear" or "exponential"
    """
    for attempt in range(1, max_attempts + 1):
        try:
            return func(*args, **kwargs)
        except RateLimitError as e:
            # Check if it's a quota issue (insufficient_quota) vs rate limit
            if e.code == 'insufficient_quota':
                logger.error(colored("❌ CRITICAL: OpenAI Quota Exceeded. Please check billing.", "red"))
                raise e # Do not retry quota errors, they won't fix themselves quickly
            
            if attempt == max_attempts:
                logger.error(f"Rate limit hit. Max retries ({max_attempts}) exceeded.")
                raise
            
            sleep_time = base_delay * attempt if backoff_type == "linear" else base_delay * (2 ** (attempt - 1))
            # Add jitter
            sleep_time += random.uniform(0, 1)
            
            logger.warning(colored(f"⚠️ Rate limit hit. Retrying in {sleep_time:.2f}s (Attempt {attempt}/{max_attempts})...", "yellow"))
            time.sleep(sleep_time)
            
        except (APIConnectionError, APIStatusError) as e:
            if attempt == max_attempts:
                logger.error(f"API Error: {e}. Max retries exceeded.")
                raise
            
            sleep_time = base_delay * attempt if backoff_type == "linear" else base_delay * (2 ** (attempt - 1))
            logger.warning(colored(f"⚠️ API Error: {e}. Retrying in {sleep_time:.2f}s...", "yellow"))
            time.sleep(sleep_time)
            
        except AuthenticationError as e:
            logger.error(colored(f"❌ Authentication Error: {e}. Check your API key.", "red"))
            raise # Do not retry auth errors
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

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
            # UPDATED METHOD: client.audio.transcriptions.create
            return client.audio.transcriptions.create(model=model, file=f, response_format="verbose_json")

    try:
        transcript_data = retry_with_backoff(_call, max_attempts=3, base_delay=5.0, backoff_type="linear")
    except RateLimitError:
        return None # Skip this file if rate limited/quota exceeded
    except Exception as e:
        logging.error(f"Failed to transcribe {file_path.name}: {e}")
        logger.info(colored(f"❌ Failed to transcribe {file_path.name}: {e}", "red"))
        return None

    segments = transcript_data.segments
    lines = []
    for seg in segments:
        start = seg['start']
        end = seg['end']
        text = seg['text'].strip()
        lines.append(f"{format_timestamp(start)} -- {format_timestamp(end)}: {text}")
    return "\n".join(lines)

def analyze_text_for_section(text: str, model="gpt-4o") -> str | None:
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
            max_tokens=CONSTANT_1500,
            temperature=0.7)

    try:
        response = retry_with_backoff(_call, max_attempts=3, base_delay=5.0, backoff_type="linear")
    except RateLimitError:
        return None
    except Exception as e:
        logging.error(f"Analysis failed: {e}")
        logger.info(colored(f"⚠️ Analysis error: {e}", "yellow"))
        return None
    
    choice = response.choices[0]
    content = choice.message.content
    return content.strip() if content else None

def link_timestamps_to_analysis(transcript_segments, analysis_text):
    linked = analysis_text
    for seg in transcript_segments:
        piece = seg["text"]
        if piece and piece in linked:
            linked = linked.replace(piece, f"{piece} [{seg['timestamp']}]")
    return linked

# ---------- MAIN PROCESSING ----------

def process_audio_file(
    audio_file: Path,
    transcript_dir: Path,
    analysis_dir: Path,
    force: bool = False,
    analysis_model: str = "gpt-4o",
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

    analysis = analyze_text_for_section(transcript, model=analysis_model)
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

def process_audio_directory(audio_dir: Path, max_workers: int, force: bool, analysis_model: str):
    transcript_dir = audio_dir / "transcript"
    analysis_dir = audio_dir / "analysis"
    transcript_dir.mkdir(parents=True, exist_ok=True)
    analysis_dir.mkdir(parents=True, exist_ok=True)

    audio_files = sorted([p for p in audio_dir.rglob("*.mp3") if p.is_file()])
    if not audio_files:
        logger.info(colored("⚠️ No MP3s found in the directory.", "red"))
        return

    logger.info(colored(f"🗂 Found {len(audio_files)} MP3 files. Starting...", "green"))

    cache_file = audio_dir / ".processing_cache.json"
    cache = load_progress_cache(cache_file)

    def worker(path: Path):
        try:
            process_audio_file(path, transcript_dir, analysis_dir, force=force, analysis_model=analysis_model)
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
        default=Path(str(Path.home()) + "/Music/nocTurneMeLoDieS"),
        help="Directory containing MP3s (recursive).")
    parser.add_argument(
        "-w", "--max-workers", type=int, default=4, help="Number of concurrent transcription workers."
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="Reprocess even if transcript+analysis exist."
    )
    parser.add_argument(
        "-m", "--model", type=str, default="gpt-4o", help="OpenAI model to use for analysis (e.g., gpt-3.5-turbo, gpt-4o)."
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

    # Pass the model argument to the processing function
    process_audio_directory(audio_dir, max_workers=args.max_workers, force=args.force, analysis_model=args.model)


if __name__ == "__main__":
    main()