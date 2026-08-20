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
    from openai import OpenAI
except Exception as e:
    print(f"[import-error] openai: {e}", file=sys.stderr)
    raise

# ---------- Env ----------
load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "placeholder"))

# ---------- Helpers ----------
def format_timestamp(seconds: float) -> str:
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def split_video_to_segments(video_path: Path, output_root: Path, segment_length: int = 300) -> list[Path]:
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
    print("• ffmpeg split:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    return sorted(p for p in out_dir.glob("*.mp4"))

def transcribe_video_segment(file_path: Path) -> str:
    """Transcribe a segment with OpenAI Whisper API, returning a string with timestamps."""
    with open(file_path, "rb") as video_file:
        transcript_data = client.audio.transcriptions.create(
            model="whisper-1", file=video_file, response_format="verbose_json"
        )

    lines = []
    for seg in transcript_data.segments:
        lines.append(
            f"{format_timestamp(seg.start)} -- {format_timestamp(seg.end)}: {seg.text.strip()}"
        )
    return "\n".join(lines)

def analyze_text_for_section(transcript: str, section_number: int = 1) -> str:
    """Analyze transcript with GPT (Chat Completions)."""
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
        resp = client.chat.completions.create(
            model=os.getenv("ANALYZER_MODEL", "gpt-4o"),
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            max_tokens=2000,
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[analysis-error] {e}"

def transcribe_segment(file_path: str) -> str:
    """Public alias for integration with digital_dive."""
    return transcribe_video_segment(Path(file_path))


def analyze_transcript(transcript: str) -> str:
    """Public alias for integration with digital_dive."""
    return analyze_text_for_section(transcript)


def process_video_by_section(video_file: Path, base_dir: Path, segment_length: int = 300):
    """Split -> transcribe -> analyze; writes outputs under base_dir/transcript and base_dir/analysis."""
    transcript_dir = base_dir / "transcript"
    analysis_dir = base_dir / "analysis"
    transcript_dir.mkdir(parents=True, exist_ok=True)
    analysis_dir.mkdir(parents=True, exist_ok=True)

    segments = split_video_to_segments(video_file, base_dir, segment_length)
    for index, segment in enumerate(segments, start=1):
        print(f"== Section {index}: {segment.name} ==")
        transcript = transcribe_video_segment(segment)
        tpath = transcript_dir / f"section_{index:03d}_transcript.txt"
        tpath.write_text(transcript, encoding="utf-8")
        print("   transcript ->", tpath)

        analysis = analyze_text_for_section(transcript, index)
        apath = analysis_dir / f"section_{index:03d}_analysis.txt"
        apath.write_text(analysis, encoding="utf-8")
        print("   analysis   ->", apath)

def main():
    ap = argparse.ArgumentParser(description="Split, transcribe, and analyze MP4s by sections (CLI fix).")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--video", type=str, help="Path to a single MP4 file")
    g.add_argument("--video-dir", type=str, help="Directory containing MP4 files to process")

    ap.add_argument("--outdir", type=str, help="Output directory (default: alongside input)")
    ap.add_argument("--segment-seconds", type=int, default=300, help="Length of each segment in seconds (default: 300)")

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
            print(f"[warn] No MP4 files found in: {vd}")
        for vf in mp4s:
            outdir = Path(args.outdir).expanduser().resolve() if args.outdir else vf.parent
            process_video_by_section(vf, outdir, args.segment_seconds)

if __name__ == "__main__":
    main()
