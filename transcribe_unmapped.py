#!/usr/bin/env python3
"""
Advanced transcription and analysis for ALBUMS/Unmapped_UUIDs.

Uses high-quality settings from ~/pythons research:
- Priority: OpenAI Whisper API (verbose_json) → faster-whisper (medium) → openai-whisper (word_timestamps)
- Parameters: beam_size=5, vad_filter, condition_on_previous_text, medium model
- Output: transcripts/ with timestamps, analysis/ with GPT music-style analysis

Usage:
  python transcribe_unmapped.py [--force] [--no-analysis] [--provider openai|local]
"""

import os
from pathlib import Path


# Load env from ~/.env.d and ~/.env
def load_env():
    env_d = Path.home() / ".env.d"
    if env_d.exists():
        for f in env_d.glob("*.env"):
            try:
                for line in f.read_text().splitlines():
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        if line.startswith("export "):
                            line = line[7:]
                        parts = line.split("=", 1)
                        if len(parts) == 2 and not parts[0].strip().startswith("source"):
                            k, v = parts[0].strip(), parts[1].strip().strip("'\"")
                            os.environ[k] = v
            except Exception:
                pass
    try:
        from dotenv import load_dotenv

        load_dotenv(Path.home() / ".env")
    except ImportError:
        pass


load_env()

UNMAPPED = Path(__file__).parent / "ALBUMS" / "Unmapped_UUIDs"
TRANSCRIPTS_DIR = UNMAPPED / "transcripts"
ANALYSIS_DIR = UNMAPPED / "analysis"

MUSIC_ANALYSIS_PROMPT = """Analyze the following song transcript:
1. **Central Themes and Meaning**: Main themes and message
2. **Emotional Tone**: Emotional tone and shifts
3. **Artist's Intent**: What the artist aims to express
4. **Metaphors, Symbols, and Imagery**: Notable metaphors and their significance
5. **Overall Emotional and Narrative Experience**: How elements create impact
6. **Suggested Title**: If the transcript has no known title, suggest one based on lyrics

Transcript:
{transcript}"""


def fmt_ts(s: float) -> str:
    m, sec = divmod(int(s), 60)
    return f"{m:02d}:{sec:02d}"


def transcribe_openai(
    audio_path: Path,
) -> tuple[str, list[tuple[float, float, str]]] | None:
    """OpenAI Whisper API – verbose_json for rich segments."""
    try:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        if not client.api_key:
            return None
        with open(audio_path, "rb") as f:
            r = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="verbose_json",
                timestamp_granularities=["segment"],
            )
        lang = getattr(r, "language", None) or "en"
        segs = getattr(r, "segments", None) or []
        out = [
            (
                float(getattr(s, "start", 0)),
                float(getattr(s, "end", 0)),
                (getattr(s, "text", None) or "").strip(),
            )
            for s in segs
        ]
        if not out and getattr(r, "text", None):
            out = [(0.0, 0.0, r.text.strip())]
        return (lang, out)
    except Exception as e:
        print(f"  OpenAI failed: {e}")
        return None


def transcribe_faster_whisper(
    audio_path: Path,
    model: str = "medium",
    device: str = "cpu",
    compute_type: str = "int8",
    beam_size: int = 5,
    vad_filter: bool = True,
) -> tuple[str, list[tuple[float, float, str]]] | None:
    """faster-whisper – medium model, beam_size=5, condition_on_previous_text."""
    try:
        from faster_whisper import WhisperModel

        m = WhisperModel(model, device=device, compute_type=compute_type)
        segments, info = m.transcribe(
            str(audio_path),
            vad_filter=vad_filter,
            beam_size=beam_size,
            condition_on_previous_text=True,
        )
        out = [(s.start, s.end, s.text.strip()) for s in segments]
        return (info.language or "en", out)
    except Exception as e:
        print(f"  faster-whisper failed: {e}")
        return None


def transcribe_openai_whisper(
    audio_path: Path,
    model: str = "medium",
    word_timestamps: bool = True,
    beam_size: int = 5,
    temperature: tuple = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
    best_of: int = 5,
    patience: float = 1.0,
) -> tuple[str, list[tuple[float, float, str]]] | None:
    """openai-whisper – word_timestamps, beam_size, temperature fallback."""
    try:
        import whisper

        m = whisper.load_model(model, device="cpu")
        r = m.transcribe(
            str(audio_path),
            language=None,
            task="transcribe",
            beam_size=beam_size,
            best_of=best_of,
            temperature=temperature,
            patience=patience,
            condition_on_previous_text=True,
            word_timestamps=word_timestamps,
        )
        lang = r.get("language", "en")
        segs = r.get("segments", [])
        out = [(s["start"], s["end"], (s.get("text") or "").strip()) for s in segs]
        return (lang, out)
    except Exception as e:
        print(f"  openai-whisper failed: {e}")
        return None


def analyze_transcript_gpt(transcript_text: str, model: str = "gpt-4o-mini") -> str | None:
    """GPT music-style analysis."""
    try:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        if not client.api_key:
            return None
        prompt = MUSIC_ANALYSIS_PROMPT.format(transcript=transcript_text)
        r = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an experienced language and music expert. Provide in-depth analysis of song lyrics.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return (r.choices[0].message.content or "").strip()
    except Exception as e:
        print(f"  GPT analysis failed: {e}")
        return None


def save_transcript(segments: list[tuple[float, float, str]], out_path: Path) -> str:
    """Save segment-level transcript. Returns full text for analysis."""
    lines = [f"{fmt_ts(s)}--{fmt_ts(e)} {t}" for s, e, t in segments]
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return " ".join(t for _, _, t in segments).strip()


def main():
    import argparse

    p = argparse.ArgumentParser(description="Advanced transcription + analysis for Unmapped_UUIDs")
    p.add_argument("--force", action="store_true", help="Overwrite existing transcripts")
    p.add_argument("--no-analysis", action="store_true", help="Skip GPT analysis")
    p.add_argument(
        "--provider",
        choices=["openai", "local"],
        default=None,
        help="Force provider (default: try openai then local)",
    )
    args = p.parse_args()

    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

    mp3s = sorted(UNMAPPED.rglob("*.mp3"))
    if not mp3s:
        print("No MP3s found in Unmapped_UUIDs")
        return

    print(f"Found {len(mp3s)} MP3(s). Using advanced settings (medium model, beam_size=5, etc.)\n")

    use_openai = args.provider != "local" and os.getenv("OPENAI_API_KEY")
    transcribe = None
    backend = ""

    if use_openai:

        def _transcribe_openai(p):
            return transcribe_openai(p)

        transcribe = _transcribe_openai
        backend = "OpenAI Whisper API"
    if transcribe is None or args.provider == "local":

        def _transcribe_local(p):
            return transcribe_faster_whisper(p) or transcribe_openai_whisper(p)

        transcribe = _transcribe_local
        backend = "faster-whisper (medium) / openai-whisper (medium)"

    print(f"Transcription backend: {backend}\n")

    for audio_path in mp3s:
        stem = audio_path.stem
        out_txt = TRANSCRIPTS_DIR / f"{stem}_transcript.txt"
        out_analysis = ANALYSIS_DIR / f"{stem}_analysis.txt"

        if out_txt.exists() and not args.force:
            print(f"Skipping {audio_path.name} (transcript exists, use --force to overwrite)")
            transcript_text = out_txt.read_text(encoding="utf-8")
            full_text = " ".join(
                (p[1] if len(p := line.split(" ", 1)) > 1 else "") for line in transcript_text.splitlines()
            ).strip()
        else:
            print(f"Transcribing {audio_path.name}...", end=" ", flush=True)
            result = transcribe(audio_path)
            if not result:
                print("FAILED")
                continue
            lang, segments = result
            full_text = save_transcript(segments, out_txt)
            preview = (full_text[:140] + "…") if len(full_text) > 140 else full_text
            print(f"✓ [{lang}]")
            if preview:
                print(f"  Preview: {preview}")

        if not args.no_analysis and full_text:
            if out_analysis.exists() and not args.force:
                print("  Analysis exists (use --force to overwrite)")
            else:
                print("  Analyzing...", end=" ", flush=True)
                analysis = analyze_transcript_gpt(full_text)
                if analysis:
                    out_analysis.write_text(analysis, encoding="utf-8")
                    print("✓")
                else:
                    print("(skipped – no API key or error)")

    print(f"\nTranscripts: {TRANSCRIPTS_DIR}/")
    print(f"Analysis:    {ANALYSIS_DIR}/")


if __name__ == "__main__":
    main()
