# Create a corrected drop-in script (argparse-based), a batch runner, and zip them for the user.
from pathlib import Path
import textwrap, zipfile, os

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_2000 = 2000


# Define the directory to store the fixed CLI bundle
bundle_dir = Path(Path("/Users/steven/Downloads/Compressed/analyzer_prompt_cli_fix_v2"))
bundle_dir.mkdir(parents=True, exist_ok=True)

# Define paths for the script, batch runners, and README
script_path = bundle_dir / "analyzer_prompt_cli.py"
runner_all = bundle_dir / "run_all_in_dir.sh"
runner_one = bundle_dir / "run_one_file.sh"
readme = bundle_dir / "README_FIX.md"

# Script code with argparse-based CLI fix
script_code = textwrap.dedent(r'''
#!/usr/bin/env python3
"""
analyzer_prompt_cli.py
- Fixes the IndexError/sys.arg bug.
- Replaces interactive input() with argparse flags.
- Supports processing a single MP4 (--video) or all MP4s in a directory (--video-dir).
- Splits with ffmpeg -> transcribes (OpenAI Whisper API) -> analyzes with GPT.
Intel macOS compatible (Miniforge/Mamba).
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

from dotenv import load_dotenv

try:
    import openai
except Exception as e:
    logger.info(f"[import-error] openai: {e}", file=sys.stderr)
    raise

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Helper function to format timestamps
def format_timestamp(seconds: float) -> str:
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

# Function to split video into segments
def split_video_to_segments(video_path: Path, output_root: Path, segment_length: int = CONSTANT_300) -> list[Path]:
    """Split the video into smaller segments using ffmpeg -c copy segmentation."""
    video_name = video_path.stem
    out_dir = output_root / f"{video_name}_segments"
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-i", str(video_path),
        "-c", "copy",
        "-map", "0",
        "-segment_time", str(segment_length),
        "-f", "segment",
        "-reset_timestamps", "1",
        str(out_dir / f"{video_name}_%03d.mp4"),
    ]
    logger.info("• ffmpeg split:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    return sorted(p for p in out_dir.glob("*.mp4"))

# Function to transcribe video segments
def transcribe_video_segment(file_path: Path) -> str:
    """Transcribe a segment with OpenAI Whisper API, returning a string with timestamps."""
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in env or .env")

    with open(file_path, "rb") as video_file:
        transcript_data = openai.Audio.transcribe(
            "whisper-1", video_file, response_format="verbose_json"
        )

    lines = []
    for seg in transcript_data.get("segments", []):
        start_time = seg.get("start", 0.0)
        end_time = seg.get("end", 0.0)
        text = seg.get("text", "").strip()
        lines.append(f"{format_timestamp(start_time)} -- {format_timestamp(end_time)}: {text}")
    return Path("\n").join(lines)

# Function to analyze text for each section
def analyze_text_for_section(transcript: str, section_number: int = 1) -> str:
    """Analyze transcript with GPT (Chat Completions)."""
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in env or .env")

    system_msg = (
        "You are an expert in multimedia analysis and storytelling. Your task is to provide a detailed and structured analysis "
        "of video and audio content, focusing on themes, emotional tone, narrative structure, artistic intent, and audience impact. "
        "Analyze how visual elements (e.g., imagery, colors, transitions) interact with audio elements (e.g., dialogue, music, sound effects) "
        "to convey meaning and evoke emotions. Highlight storytelling techniques and assess their effectiveness in engaging viewers."
    )

    user_msg = (
        f"Analyze the following transcript for Section {section_number}. Provide a comprehensive analysis covering:\n\n"
        "1. **Central Themes and Messages**\n"
        "2. **Emotional Tone**\n"
        "3. **Narrative Arc**\n"
        "4. **Creator's Intent**\n"
        "5. **Significant Metaphors, Symbols, and Imagery**\n"
        "6. **Storytelling Techniques**\n"
        "7. **Interplay Between Visuals and Audio**\n"
        "8. **Audience Engagement and Impact**\n"
        "9. **Overall Effectiveness**\n\n"
        f"Transcript:\n{transcript}"
    )

    try:
        resp = openai.ChatCompletion.create(
            model=os.getenv("ANALYZER_MODEL", "gpt-4o"),
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            max_tokens=CONSTANT_2000,
            temperature=0.7,
        )
        return resp.choices[0].message["content"].strip()
    except Exception as e:
        return f"[analysis-error] {e}"

# Function to process video by section
def process_video_by_section(video_file: Path, base_dir: Path, segment_length: int = CONSTANT_300):
    """Split -> transcribe -> analyze; writes outputs under base_dir/transcript and base_dir/analysis."""
    transcript_dir = base_dir / "transcript"
    analysis_dir = base_dir / "analysis"
    transcript_dir.mkdir(parents=True, exist_ok=True)
    analysis_dir.mkdir(parents=True, exist_ok=True)

    segments = split_video_to_segments(video_file, base_dir, segment_length)
    for index, segment in enumerate(segments, start=1):
        logger.info(f"== Section {index}: {segment.name} ==")
        transcript = transcribe_video_segment(segment)
        tpath = transcript_dir / f"section_{index:03d}_transcript.txt"
        tpath.write_text(transcript, encoding="utf-8")
        logger.info("   transcript ->", tpath)

        analysis = analyze_text_for_section(transcript, index)
        apath = analysis_dir / f"section_{index:03d}_analysis.txt"
        apath.write_text(analysis, encoding="utf-8")
        logger.info("   analysis   ->", apath)

# Main function to handle argument parsing and processing
def main():
    ap = argparse.ArgumentParser(description="Split, transcribe, and analyze MP4s by sections (CLI fix).")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--video", type=str, help="Path to a single MP4 file")
    g.add_argument("--video-dir", type=str, help="Directory containing MP4 files to process")

    ap.add_argument("--outdir", type=str, help="Output directory (default: alongside input)")
    ap.add_argument("--segment-seconds", type=int, default=CONSTANT_300, help="Length of each segment in seconds (default: CONSTANT_300)")

    args = ap.parse_args()

    if args.video:
        vf = Path(args.video).expanduser().resolve()
        if not vf.exists():
            ap.error(f"Video not found: {vf}")
        outdir = Path(args.outdir).expanduser().resolve() if args.outdir else vf.parent
        process_video_by_section(vf, outdir, args.segment_seconds)
    else:
        vd = Path(args.video_dir).expanduser().resolve()
        if not vd.is_dir():
            ap.error(f"Not a directory: {vd}")
        mp4s = sorted(vd.glob("*.mp4"))
        if not mp4s:
            logger.info(f"[warn] No MP4 files found in: {vd}")
        for vf in mp4s:
            outdir = Path(args.outdir).expanduser().resolve() if args.outdir else vf.parent
            process_video_by_section(vf, outdir, args.segment_seconds)

if __name__ == "__main__":
    main()
''').strip())

# Write the script code to the script path and set executable permissions
script_path.write_text(script_code)
script_path.chmod(0o755)

# Create a README file with usage instructions
readme_text = textwrap.dedent('''
# analyzer_prompt_cli.py (Fix)

This fixes your errors:
- `IndexError: list index out of range` (no more `sys.argv[1]` without args)
- `AttributeError: module 'sys' has no attribute 'arg'` (typo)
- Replaces interactive `input()` with `--video` or `--video-dir` flags.

## Usage

### Single file
```bash
conda activate hekate
python analyzer_prompt_cli.py \
  --video Path("/Users/steven/Movies/HeKaTe-saLome/input.mp4") \
  --outdir Path("/Users/steven/Movies/HeKaTe-saLome") \
  --segment-seconds CONSTANT_300
