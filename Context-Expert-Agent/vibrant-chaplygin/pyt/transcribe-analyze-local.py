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
from datetime import datetime
from pathlib import Path
from typing import Iterable, Tuple, Optional, List

# Fix OpenMP duplicate library issue (faster-whisper + numpy on macOS)
os.environ.setdefault('KMP_DUPLICATE_LIB_OK', 'TRUE')

def auto_install_package(package_name: str, import_name: str = None) -> bool:
    """
    Automatically install a missing package.
    Returns True if successful, False otherwise.
    """
    import_name = import_name or package_name
    try:
        __import__(import_name)
        return True
    except ImportError:
        print(f"?? Installing missing package: {package_name}")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package_name])
            print(f"? Successfully installed {package_name}")
            return True
        except Exception as e:
            print(f"? Failed to install {package_name}: {e}")
            return False

# Auto-install core dependencies
CORE_PACKAGES = {
    'python-dotenv': 'dotenv',
    'requests': 'requests',
    'tqdm': 'tqdm',
    'rich': 'rich',
    'faster-whisper': 'faster_whisper',
    'groq': 'groq',
}

for pkg, import_name in CORE_PACKAGES.items():
    auto_install_package(pkg, import_name)

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
def mmss(seconds: float) -> str:
    """Format as MM:SS"""
    if seconds is None or math.isnan(seconds):
        return "00:00"
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"
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
            f.write(f"{mmss(s)}-{mmss(e)}: {t}\n")

    # SRT
    def srt_timestamp(t: float) -> str:
        h, rem = divmod(int(t), 3600)
        m, s = divmod(rem, 60)
        ms = int((t - int(t)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    with out_srt.open("w", encoding="utf-8") as f:
        for idx, (s, e, t) in enumerate(segments, 1):
            f.write(f"{idx}\n{srt_timestamp(s)} --> {srt_timestamp(e)}\n{t}\n\n")

def analyze_with_llm(text: str, filename: str, backend: str = "groq", model: str = None, system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> str:
    """
    Universal LLM analysis function that routes to different backends.
    Supports: groq, openai, anthropic, gemini, deepseek, ollama
    Auto-installs backend-specific packages as needed.
    """
    # Default models per backend
    DEFAULT_MODELS = {
        "groq": "llama-3.3-70b-versatile",  # Fast, free, high quality
        "openai": "gpt-4o-mini",  # Cost-effective
        "anthropic": "claude-3-5-sonnet-20241022",  # Best quality
        "gemini": "gemini-2.0-flash-exp",  # Free tier
        "deepseek": "deepseek-chat",  # Cost-effective
        "ollama": "llama3.2:1b"  # Local
    }
    
    # Backend-specific package requirements
    BACKEND_PACKAGES = {
        "groq": ("groq", "groq"),
        "openai": ("openai", "openai"),
        "anthropic": ("anthropic", "anthropic"),
        "gemini": ("google-generativeai", "google.generativeai"),
        "deepseek": ("openai", "openai"),
    }
    
    # Auto-install backend package if needed
    if backend in BACKEND_PACKAGES:
        pkg, import_name = BACKEND_PACKAGES[backend]
        auto_install_package(pkg, import_name)
    
    model = model or DEFAULT_MODELS.get(backend, "gpt-4o-mini")
    user_prompt = f"File: {filename}\nTranscript:\n{text}\n\nReturn a structured analysis with section headers."
    
    try:
        if backend == "groq":
            from groq import Groq
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
            )
            return completion.choices[0].message.content
            
        elif backend == "openai":
            import openai
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
            )
            return completion.choices[0].message.content
            
        elif backend == "anthropic":
            import anthropic
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            message = client.messages.create(
                model=model,
                max_tokens=2000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return message.content[0].text
            
        elif backend == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model_obj = genai.GenerativeModel(model)
            response = model_obj.generate_content(f"{system_prompt}\n\n{user_prompt}")
            return response.text
            
        elif backend == "deepseek":
            import openai
            client = openai.OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com"
            )
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
            )
            return completion.choices[0].message.content
            
        elif backend == "ollama":
            return analyze_with_ollama(text, filename, model, system_prompt)
            
        else:
            return f"[ERROR] Unknown backend: {backend}"
            
    except Exception as e:
        return f"[ERROR] {backend.upper()} API call failed: {e}\nCheck API key in ~/.env.d/llm-apis.env"

def analyze_with_groq(text: str, filename: str, model: str = "llama-3.3-70b-versatile", system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> str:
    """DEPRECATED: Use analyze_with_llm() instead."""
    return analyze_with_llm(text, filename, "groq", model, system_prompt)

def ollama_host() -> str:
    return os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")

def analyze_with_ollama(text: str, filename: str, model: str, system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> str:
    """
    Calls Ollama /api/generate with a composed prompt (DEPRECATED: Use Groq instead).
    """
    url = f"{ollama_host().rstrip('/')}/api/generate"
    prompt = (
        f"{system_prompt}\n\n"
        f"File: {filename}\n"
        f"Transcript:\n{text}\n\n"
        "Return a structured analysis with section headers."
    )
    try:
        resp = requests.post(url, json={"model": model, "prompt": prompt, "stream": False}, timeout=600)
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
    parser.add_argument("--backend", dest="backend", default="groq", 
                        choices=["groq", "openai", "anthropic", "gemini", "deepseek", "ollama"],
                        help="LLM backend (default: groq - fastest & free)")
    parser.add_argument("--llm", dest="llm_model", default=None,
                        help="Model name (optional - uses best default per backend)")
    args = parser.parse_args()

    media_root = Path(args.media_dir).expanduser().resolve()
    transcripts_dir, analysis_dir = ensure_dirs(media_root)

    rprint(f"[bold cyan]Media root:[/bold cyan] {media_root}")
    rprint(f"[dim]Transcripts -> {transcripts_dir} | Analysis -> {analysis_dir}[/dim]")
    rprint(f"[dim]Whisper: {args.whisper_model} | Compute: {args.compute_type} | Backend: {args.backend} | Model: {args.llm_model}[/dim]")

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
        rprint(f"[green]? Transcript saved[/green] {out_txt.name}  ([dim]{lang}[/dim])")

        # Build text for LLM (concat segments)
        transcript_text = "\n".join(f"{mmss(s)}-{mmss(e)} {t}" for (s, e, t) in segments)

        # Optional lightweight features
        feats = extract_features(path)
        if feats:
            transcript_text = f"[AUDIO FEATURES] {feats}\n\n" + transcript_text

        # Analyze with LLM (auto-select backend)
        analysis = analyze_with_llm(
            transcript_text, 
            path.name, 
            backend=args.backend,
            model=args.llm_model
        )
        
        # Add header to analysis
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"""MUSIC ANALYSIS FOR: {stem}
{'=' * 60}
Analysis timestamp: {timestamp}
Transcription method: Whisper AI ({args.whisper_model} model)
LLM Backend: {args.backend}
LLM Model: {args.llm_model}
Detected language: {lang}
{'=' * 60}

"""
        full_analysis = header + analysis
        out_analysis.write_text(full_analysis, encoding="utf-8")
        rprint(f"[green]? Analysis saved[/green] {out_analysis.name}")

    rprint("[bold green]Done.[/bold green]")

if __name__ == "__main__":
    main()
