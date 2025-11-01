"""
Manytran

This module provides functionality for manytran.

Author: Auto-generated
Date: 2025-11-01
"""

import os
import sys
import json
import argparse
import logging
import subprocess
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, List

import openai
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

# Constants
CONSTANT_300 = 300
CONSTANT_2048 = 2048


# --- CONFIGURATION ---
load_dotenv(Path.home() / ".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in environment.")
openai.api_key = OPENAI_API_KEY

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# --- DATA CLASSES ---
@dataclass
class TextAnalysis:
    central_themes: str
    hidden_meanings: str
    emotional_tone: str
    mood_shifts: str
    narrative_arc: str
    transitions: str
    creator_intent: str
    multimedia_support: str
    technical_elements: str
    production_techniques: str
    audience_engagement: str
    memorable_aspects: str

# --- CONSTANTS ---
VIDEO_EXTS = {".mp4"}
AUDIO_EXTS = {".mp3", ".wav"}

# --- UTILITIES ---
def format_timestamp(seconds: float) -> str:
    """format_timestamp function."""

    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes:02d}:{secs:02d}"

# --- MEDIA WORKFLOW (VIDEO/AUDIO) ---
@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    """split_video_to_segments function."""

def split_video_to_segments(video_path: Path, segment_length: int) -> List[Path]:
    base = video_path.stem
    seg_dir = video_path.parent / f"{base}_segments"
    seg_dir.mkdir(exist_ok=True)
    cmd = [
        "ffmpeg", "-i", str(video_path), "-c", "copy", "-map", "0",
        "-segment_time", str(segment_length), "-f", "segment", "-reset_timestamps", "1",
        str(seg_dir / f"{base}_%03d{video_path.suffix}")
    ]
    subprocess.run(cmd, check=True)
    return sorted(seg_dir.glob(f"*{video_path.suffix}"))

    """transcribe_audio function."""

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def transcribe_audio(file_path: Path, segment: Optional[Path] = None) -> str:
    target = segment or file_path
    with target.open('rb') as audio:
        result = openai.Audio.transcribe(
            model="whisper-1",
            file=audio,
            response_format="verbose_json"
        )
    lines = []
    for seg in result.get("segments", []):
        start = format_timestamp(seg["start"])
        end = format_timestamp(seg["end"])
        text = seg.get("text", "")
        lines.append(f"{start} --> {end}: {text}")
    return Path("\n").join(lines)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def analyze_text_for_section(transcript: str, section_number: int = 1) -> TextAnalysis:
    """Analyze a section of transcript with GPT-4o, returning structured insights with detailed breakdown."""
    system_prompt = (
        "You are an expert multimedia analyst and storyteller. Your analyses should cover thematic depth, "
        "emotional tone, narrative structure, artistic expression, technical execution, and audience engagement. "
        "Use vivid, descriptive language and reference specific moments when necessary."
    )
    user_prompt = (
        f"Analyze the following transcript and associated content for {section_name}. "
        "Provide a comprehensive analysis covering:\n"
        "1. Central Themes and Messages: Identify the primary ideas or messages conveyed. "
        "How do they connect to the broader narrative?\n"
        "2. Emotional Tone: What emotions are evoked, and how are they conveyed through the "
        "combination of audio and visuals?\n"
        "3. Narrative Arc: Describe how this section contributes to the overall story or progression. "
        "Are there key turning points or developments?\n"
        "4. Creator’s Intent: What is the likely purpose or message the creator is trying to communicate? "
        "Is it to entertain, inform, inspire, or persuade?\n"
        "5. Significant Metaphors, Symbols, and Imagery: Highlight notable metaphors, symbols, or "
        "visual/audio motifs that enhance the narrative or emotional impact.\n"
        "6. Storytelling Techniques: Identify specific techniques used, such as pacing, transitions, "
        "visual effects, or sound design. How do they contribute to the overall experience?\n"
        "7. Interplay Between Visuals and Audio: Analyze how visuals and audio work together to create "
        "meaning and impact. Are there any standout moments?\n"
        "8. Audience Engagement and Impact: Evaluate how effectively the content captures and holds attention. "
        "How well does it resonate with its intended audience?\n"
        "9. Overall Effectiveness: Summarize how these elements combine to create a cohesive, immersive, "
        "and impactful experience for the viewer.\n\n"
        f"Transcript:\n{text}"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=CONSTANT_2048,
    )
    content = response.choices[0].message.content
    # parse JSON output
    start = content.find("{")
    end = content.rfind("}") + 1
    data = json.loads(content[start:end])
    return TextAnalysis(
        central_themes=data.get("central_themes_and_messages", ""),
        hidden_meanings=data.get("hidden_or_layered_meanings", ""),
        emotional_tone=data.get("emotional_tone", ""),
        mood_shifts=data.get("mood_shifts", ""),
        narrative_arc=data.get("narrative_arc_and_structure", ""),
        transitions=data.get("transitions", ""),
        creator_intent=data.get("creators_intent_and_vision", ""),
        multimedia_support=data.get("multimedia_elements_support", ""),
        technical_elements=data.get("technical_and_artistic_elements", ""),
        production_techniques=data.get("production_techniques", ""),
        audience_engagement=data.get("audience_impact_and_engagement", ""),
        memorable_aspects=data.get("memorable_aspects", "")
    )
    """main function."""


# --- CLI ENTRYPOINT ---
def main():
    parser = argparse.ArgumentParser(prog="media_analyzer")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    media_parser = subparsers.add_parser(
        "media", help="Analyze media files (mp4, mp3, wav)"
    )
    media_parser.add_argument("file", type=Path, help="Path to media file")
    media_parser.add_argument("-l", "--length", type=int, default=CONSTANT_300, help="Video segment length in seconds")
    media_parser.add_argument("--transcript-dir", type=Path, default=Path("transcripts"), help="Folder to save transcripts")
    media_parser.add_argument("--analysis-dir", type=Path, default=Path("analysis"), help="Folder to save analysis JSONs")

    text_parser = subparsers.add_parser(
        "text", help="Analyze a text transcript file"
    )
    text_parser.add_argument("file", type=Path, help="Transcript text file")
    text_parser.add_argument("-s", "--section", type=int, default=1, help="Section number to analyze")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    if args.mode == "media":
        args.transcript_dir.mkdir(exist_ok=True)
        args.analysis_dir.mkdir(exist_ok=True)
        ext = args.file.suffix.lower()
        segments = split_video_to_segments(args.file, args.length) if ext in VIDEO_EXTS else [None] if ext in AUDIO_EXTS else []
        if not segments:
            logger.error("Unsupported media type: %s", ext)
            sys.exit(1)
        for idx, seg in enumerate(segments, start=1):
            logger.info("Processing section %d", idx)
            transcript = transcribe_audio(args.file, seg)
            tfile = args.transcript_dir / f"section_{idx}.txt"
            tfile.write_text(transcript)
            analysis = analyze_text_for_section(transcript, idx)
            afile = args.analysis_dir / f"section_{idx}_analysis.json"
            afile.write_text(json.dumps(asdict(analysis), indent=2))
        logger.info("Media analysis completed.")

    elif args.mode == "text":
        transcript = args.file.read_text()
        analysis = analyze_text_for_section(transcript, args.section)
        logger.info(json.dumps(asdict(analysis), indent=2))

if __name__ == "__main__":
    main()
