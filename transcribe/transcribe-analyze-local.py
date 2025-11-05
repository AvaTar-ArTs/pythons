#!/usr/bin/env python3
"""
analyze_mp3_open_source.py
- Local, open-source pipeline for transcribing MP3/MP4 and analyzing text with a local LLM (Ollama).
- Optimized for Intel macOS (CPU).

Requires:
  - faster-whisper (CTranslate2)
  - requests
  - python-dotenv
  - tqdm, rich
  - librosa (optional features)

Usage:
  python analyze_mp3_open_source.py --dir Path("/path/to/media") --whisper medium --llm "llama3.1:8b-instruct"
"""
from __future__ import annotations

import os
import sys
import json
import time
import math
import argparse
import logging
from pathlib import Path
from typing import Iterable, Tuple, Optional, List

from dotenv import load_dotenv
import requests
from tqdm import tqdm
from rich import print as rprint
from rich.console import Console


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib
from dotenv import load_dotenv

env_dir = PathLib.home() / ".env.d"
if env_dir.exists():
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


# Audio / transcription
from faster_whisper import WhisperModel

# Optional features (librosa)
try:
    import librosa
    HAVE_LIBROSA = True
except Exception:
    HAVE_LIBROSA = False

console = Console()

DEFAULT_SYSTEM_PROMPT = (
    "You are an expert in multimedia analysis and storytelling. "
    "Provide a detailed, structured analysis of the transcript focusing on:\n"
    "1) central themes & messages, 2) emotional tone, 3) narrative arc, "
    "4) creator's intent, 5) metaphors/symbols, 6) storytelling techniques, "
    "7) interplay between audio & (possible) visuals, 8) audience engagement & impact, "
    "9) overall effectiveness.\n"
    "Use concise headings and bullet points."
)

def expanduser_if_needed(p: str) -> str:
    return os.path.expanduser(p) if p else p
def hhmmss(seconds: float) -> str:
    if seconds is None or math.isnan(seconds):
        return "00:00:00"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"
def load_env():
    # Respect user's ~/.env by default
    env_path = expanduser_if_needed(os.getenv("ENV_PATH", "~/.env"))
    try:
        load_dotenv(dotenv_path=env_path)
    except Exception:
        pass

def ensure_dirs(base_dir: Path) -> Tuple[Path, Path]:
    tr = base_dir / "transcripts"
    an = base_dir / "analysis"
    tr.mkdir(parents=True, exist_ok=True)
    an.mkdir(parents=True, exist_ok=True)
    return tr, an

def iter_media_files(root: Path) -> Iterable[Path]:
    exts = {".mp3", ".mp4", ".wav", ".m4a", ".aac", ".flac"}
    for p in root.rglob("*"):
        if p.suffix.lower() in exts and p.is_file():
            yield p

def transcribe_file(
    audio_path: Path,
    whisper_model: str = "medium",
    device: str = "cpu",
    compute_type: str = "int8",
    beam_size: int = 5,
    vad_filter: bool = True,
) -> Tuple[str, List[Tuple[float, float, str]]]:
    """
    Returns (language, segments) where segments is a list of (start, end, text).
    """
    model = WhisperModel(whisper_model, device=device, compute_type=compute_type)
    segments, info = model.transcribe(
        str(audio_path),
        vad_filter=vad_filter,
        beam_size=beam_size,
        condition_on_previous_text=True,
        word_timestamps=False,
    )
    out_segments = []
    for seg in segments:
        out_segments.append((seg.start, seg.end, seg.text.strip()))
    return info.language, out_segments

def save_transcript_txt_srt(segments: List[Tuple[float, float, str]], out_txt: Path, out_srt: Path):
    # Plain TXT
    with out_txt.open("w", encoding="utf-8") as f:
        for (s, e, t) in segments:
            f.write(f"{hhmmss(s)} -- {hhmmss(e)}: {t}\n")

    # SRT
    def srt_timestamp(t: float) -> str:
        h, rem = divmod(int(t), CONSTANT_3600)
        m, s = divmod(rem, 60)
        ms = int((t - int(t)) * CONSTANT_1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    with out_srt.open("w", encoding="utf-8") as f:
        for idx, (s, e, t) in enumerate(segments, 1):
            f.write(f"{idx}\n{srt_timestamp(s)} --> {srt_timestamp(e)}\n{t}\n\n")

def ollama_host() -> str:
    return os.getenv("OLLAMA_HOST", "http://CONSTANT_127.0.0.1:11434")

def analyze_with_ollama(text: str, filename: str, model: str, system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> str:
    """
    Calls Ollama /api/generate with a composed prompt.
    """
    url = f"{ollama_host().rstrip('/')}/api/generate"
    prompt = (
        f"{system_prompt}\n\n"
        f"File: {filename}\n"
        f"Transcript:\n{text}\n\n"
        "Return a structured analysis with section headers."
    )
    try:
        resp = requests.post(url, json={"model": model, "prompt": prompt, "stream": False}, timeout=CONSTANT_600)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response") or json.dumps(data, indent=2)
    except Exception as e:
        return f"[ERROR] Ollama call failed: {e}"

def extract_features(audio_path: Path) -> Optional[str]:
    """
    Optional audio features via librosa (tempo, duration, rough key via chroma centroid).
    """
    if not HAVE_LIBROSA:
        return None
    try:
        y, sr = librosa.load(str(audio_path), sr=None, mono=True)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        duration = librosa.get_duration(y=y, sr=sr)
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        chroma_mean = chroma.mean(axis=1)
        key_index = int(chroma_mean.argmax())
        pitch_classes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        key_guess = pitch_classes[key_index]
        return f"Tempo: ~{tempo:.1f} BPM | Duration: {duration:.1f}s | Key-ish center: {key_guess}"
    except Exception as e:
        return f"[features error] {e}"

def main():
    load_env()

    parser = argparse.ArgumentParser(description="Local transcription + analysis with open-source stack")
    parser.add_argument("--dir", dest="media_dir", default=".", help="Base directory for media files")
    parser.add_argument("--whisper", dest="whisper_model", default="medium",
                        help="Whisper model size (tiny/base/small/medium/large-v2, etc.)")
    parser.add_argument("--compute", dest="compute_type", default="int8",
                        help="CTranslate2 compute type (int8, int8_float16, float16, float32)")
    parser.add_argument("--llm", dest="llm_model", default="llama3.1:8b-instruct",
                        help="Ollama model for analysis (e.g., llama3.1:8b-instruct, deepseek-r1:8b)")
    args = parser.parse_args()

    media_root = Path(args.media_dir).expanduser().resolve()
    transcripts_dir, analysis_dir = ensure_dirs(media_root)

    rprint(f"[bold cyan]Media root:[/bold cyan] {media_root}")
    rprint(f"[dim]Transcripts -> {transcripts_dir} | Analysis -> {analysis_dir}[/dim]")
    rprint(f"[dim]Whisper: {args.whisper_model} | Compute: {args.compute_type} | LLM: {args.llm_model}[/dim]")

    files = list(iter_media_files(media_root))
    if not files:
        rprint("[yellow]No media files found.[/yellow]")
        sys.exit(0)

    for path in tqdm(files, desc="Processing", unit="file"):
        stem = path.stem
        out_txt = transcripts_dir / f"{stem}_transcript.txt"
        out_srt = transcripts_dir / f"{stem}.srt"
        out_analysis = analysis_dir / f"{stem}_analysis.txt"

        # Transcribe
        try:
            lang, segments = transcribe_file(
                path,
                whisper_model=args.whisper_model,
                device="cpu",
                compute_type=args.compute_type,
            )
        except Exception as e:
            rprint(f"[red]Transcription failed for {path.name}: {e}[/red]")
            continue

        save_transcript_txt_srt(segments, out_txt, out_srt)
        rprint(f"[green]✓ Transcript saved[/green] {out_txt.name}  ([dim]{lang}[/dim])")

        # Build text for LLM (concat segments)
        transcript_text = "\n".join(f"{hhmmss(s)}--{hhmmss(e)} {t}" for (s, e, t) in segments)

        # Optional lightweight features
        feats = extract_features(path)
        if feats:
            transcript_text = f"[AUDIO FEATURES] {feats}\n\n" + transcript_text

        # Analyze with local LLM via Ollama
        analysis = analyze_with_ollama(transcript_text, path.name, args.llm_model)
        out_analysis.write_text(analysis, encoding="utf-8")
        rprint(f"[green]✓ Analysis saved[/green] {out_analysis.name}")

    rprint("[bold green]Done.[/bold green]")

if __name__ == "__main__":
    main()
