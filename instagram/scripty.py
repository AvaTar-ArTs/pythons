"""
Scripty

This module provides functionality for scripty.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200
CONSTANT_250 = 250
CONSTANT_300 = 300
CONSTANT_320 = 320
CONSTANT_400 = 400
CONSTANT_500 = 500
CONSTANT_700 = 700
CONSTANT_1000 = 1000
CONSTANT_1200 = 1200
CONSTANT_1500 = 1500
CONSTANT_1600 = 1600
CONSTANT_1800 = 1800
CONSTANT_8192 = 8192

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripty_tts_unified_v2.py
All-in-one audiobook TTS engine with:
- Model auto-selection (prefers OpenAI gpt-4o-tts; falls back to other tts/audio; then HF Bark)
- Cheerful Guide persona with micro-pauses for imperative instructions
- Token-aware chunking, retries, resume, CONSTANT_320 kbps mastering
- Three modes: adaptive (chapter mp3s), asmr (single whisper master), cinematic (multi-voice + ambience)

Usage:
  python scripty_tts_unified_v2.py --source Path("/path/book.docx") --mode adaptive
  python scripty_tts_unified_v2.py --source Path("/path/book.docx") --mode asmr --voice cove
  python scripty_tts_unified_v2.py --source Path("/path/book.docx") --mode cinematic --bitrate 320k

Requires:
  pip install openai python-docx python-dotenv pydub requests
"""

import os, re, time, json, random, argparse, math
from pathlib import Path
from typing import List, Tuple, Optional

from dotenv import load_dotenv
from pydub import AudioSegment, effects

# lazy imports inside functions:
# from openai import OpenAI
# from docx import Document
# import requests

# =========================
# Env + constants
# =========================
load_dotenv(os.path.expanduser("~/.env"))

BITRATE_DEFAULT = "320k"
TARGET_DBFS_DEFAULT = -14.0

PREFERRED_MODELS = [
    "gpt-4o-tts",  # first choice if permitted
    "gpt-4o-audio",  # alt premium audio-capable
    "gpt-4o-mini-tts",  # last resort
]

CHEERFUL_GUIDE_PROMPT = (
    "Narration style: a cheerful guide. "
    "Tone: friendly, clear, and reassuring. "
    "Pronunciation: clear, articulate, steady. "
    "Pacing: brief, purposeful pauses after key instructions to allow processing. "
    "Emotion: warm and supportive, with empathy and care. "
    "Voice: warm, upbeat, and reassuring, steady, confident cadence. "
    "Dialect: neutral and professional, friendly and approachable. "
    "Be positive and solution-oriented, focusing on next steps. "
    "If imperatives appear (e.g., turn right, cross the street, continue straight), add a short pause right after."
)

PAUSE_KEYWORDS = [
    "turn right",
    "turn left",
    "continue straight",
    "cross the street",
    "merge right",
    "merge left",
    "take the exit",
    "keep right",
    "keep left",
    "stop here",
    "slow down",
    "look both ways",
    "proceed with caution",
]

AMBIENT_CHOICES = ["forest", "rain", "fire", "wind", "temple"]

CHAPTER_TO_AMBIENT = {
    "Foreword": "temple",
    "Thought And Character": "fire",
    "Effect Of Thought On Circumstances": "rain",
    "Effect Of Thought On Health And The Body": "forest",
    "Thought And Purpose": "wind",
    "The Thought-Factor In Achievement": "fire",
    "Visions And Ideals": "temple",
    "Serenity": "forest",
}


# =========================
# Helpers: text shaping
# =========================
def insert_guidance_pauses(text: str, pause_token: str = " … ") -> str:
    """insert_guidance_pauses function."""

    out = text
    for phrase in PAUSE_KEYWORDS:
        pattern = re.compile(rf"({re.escape(phrase)})(?![.,;:!?…])", re.IGNORECASE)
        out = pattern.sub(rf"\1{pause_token}", out)
    return out


    """apply_cheerful_guide_style function."""

def apply_cheerful_guide_style(text: str) -> str:
    content = insert_guidance_pauses(text)
    return f"{CHEERFUL_GUIDE_PROMPT}\n\n{content}"

    """split_sentences function."""


def split_sentences(text: str) -> List[str]:
    return re.split(r"(?<=[.!?])\s+", text.strip())
    """approx_token_count function."""



def approx_token_count(s: str) -> int:
    # crude but effective: ~4 chars/token
    return max(1, math.ceil(len(s) / 4))


def chunk_text(text: str, token_limit: int = CONSTANT_1800) -> List[str]:
    """Token-aware chunking. Keeps chunks under ~token_limit tokens."""
    sents = split_sentences(text)
    chunks, cur = [], ""
    cur_tokens = 0
    for s in sents:
        stoks = approx_token_count(s)
        if cur and (cur_tokens + stoks > token_limit):
            chunks.append(cur.strip())
            cur, cur_tokens = s, stoks
        else:
            cur = (cur + " " + s).strip() if cur else s
            cur_tokens += stoks
    if cur:
        chunks.append(cur.strip())
    """safe_name function."""

    return chunks


def safe_name(name: str) -> str:
    return re.sub(r"[^a-z0-9\-]+", "-", name.lower()).strip("-")

    """normalize_audio function."""


# =========================
# Helpers: audio shaping
# =========================
def normalize_audio(
    seg: AudioSegment, target_dbfs: float = TARGET_DBFS_DEFAULT
) -> AudioSegment:
    """overlay_ambience function."""

    seg = effects.normalize(seg)
    change = target_dbfs - seg.dBFS
    return seg.apply_gain(change)


def overlay_ambience(
    segment: AudioSegment,
    ambient_dir: Path,
    ambient_key: Optional[str],
    volume_db: int = -26,
) -> AudioSegment:
    if not ambient_key:
        return segment
    amb_path = ambient_dir / f"{ambient_key}.mp3"
    if not amb_path.exists():
        return segment
    amb = AudioSegment.from_mp3(amb_path) + volume_db
    if len(amb) < len(segment):
    """binauralize function."""

        loops = len(segment) // len(amb) + 1
        amb = amb * loops
    amb = amb[: len(segment)]
    return segment.overlay(amb)


def binauralize(
    """widen function."""

    seg: AudioSegment, pan_amount: float = 0.2, attenuate_db: float = -1.0
) -> AudioSegment:
    left = seg.pan(-abs(pan_amount))
    right = seg.pan(abs(pan_amount)).apply_gain(attenuate_db)
    return left.overlay(right)


def widen(seg: AudioSegment, pan_amount: float = 0.28) -> AudioSegment:
    return seg.pan(-abs(pan_amount)).overlay(seg.pan(abs(pan_amount)))


# =========================
# Model selection + TTS
# =========================
def choose_best_openai_tts():
    """Return (client, model) or (None, None)."""
    try:
        from openai import OpenAI
    except Exception:
        return None, None
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None, None
    client = OpenAI(api_key=key)
    try:
        available = [m.id for m in client.models.list().data]
        # Prefer explicit models
        for name in PREFERRED_MODELS:
            if name in available:
                return client, name
        # Otherwise grab any audio/tts-capable
        for m in available:
    """hf_fallback_available function."""

            mid = m.lower()
            if "tts" in mid or "audio" in mid:
                return client, m
    """hf_tts function."""

    except Exception:
        pass
    return None, None


def hf_fallback_available():
    return bool(os.getenv("HUGGINGFACE_API_KEY"))


def hf_tts(text: str, out_path: Path, model: Optional[str] = None):
    import requests

    key = os.getenv("HUGGINGFACE_API_KEY")
    model = model or os.getenv("HF_TTS_MODEL", "suno/bark-small")
    headers = {"Authorization": f"Bearer {key}"}
    resp = requests.post(
        f"https://api-inference.huggingface.co/models/{model}",
        headers=headers,
        json={"inputs": text},
    """_retry_backoff function."""

        stream=True,
        timeout=CONSTANT_300,
    )
    if resp.status_code != CONSTANT_200:
        raise RuntimeError(f"HF TTS error: {resp.text}")
    with open(out_path, "wb") as f:
        for chunk in resp.iter_content(CONSTANT_8192):
            f.write(chunk)


def _retry_backoff(attempt: int, base: float = 1.0, cap: float = 20.0):
    time.sleep(min(cap, base * (2 ** (attempt - 1))))


def openai_tts(
    client, model: str, voice: str, text: str, out_path: Path, max_retries: int = 5
):
    """Robust TTS with retries and response_format fallback."""
    styled = apply_cheerful_guide_style(text)
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            # Try modern param
            resp = client.audio.speech.create(
                model=model, voice=voice, input=styled, response_format="mp3"
            )
            out_path.write_bytes(resp.read())
            return
        except Exception as e1:
            last_err = e1
            # Try legacy param once per attempt
            try:
                resp = client.audio.speech.create(
                    model=model, voice=voice, input=styled, format="mp3"
                )
    """read_docx_chapters function."""

                out_path.write_bytes(resp.read())
                return
            except Exception as e2:
                last_err = e2
                _retry_backoff(attempt)
    raise RuntimeError(f"OpenAI TTS failed after {max_retries} attempts: {last_err}")


# =========================
# Source parsing
# =========================
def read_docx_chapters(path: Path) -> List[Tuple[str, str]]:
    from docx import Document

    doc = Document(str(path))
    chapters: List[Tuple[str, str]] = []
    cur_title, cur_body = None, []
    for p in doc.paragraphs:
        t = (p.text or "").strip()
        if not t:
    """read_txt function."""

            continue
        if t.isupper() and len(t.split()) < 10:
            if cur_title:
                chapters.append((cur_title.title(), Path("\n").join(cur_body)))
            cur_title, cur_body = t, []
        else:
    """synthesize_chunk function."""

            cur_body.append(t)
    if cur_title:
        chapters.append((cur_title.title(), Path("\n").join(cur_body)))
    return chapters


def read_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8")

    """render_adaptive function."""


# =========================
# Renderers
# =========================
def synthesize_chunk(text: str, tmp_path: Path, openai_pack, voice: str):
    client, model = openai_pack
    if client and model:
        openai_tts(client, model, voice, text, tmp_path)
    elif hf_fallback_available():
        hf_tts(text, tmp_path)
    else:
        raise RuntimeError("No TTS engine available (OpenAI or Hugging Face).")


def render_adaptive(
    source_text_or_chapters, out_dir: Path, voice: str, ambient_dir: Path, bitrate: str
):
    openai_pack = choose_best_openai_tts()
    out_dir.mkdir(parents=True, exist_ok=True)

    chapters = (
        source_text_or_chapters
        if isinstance(source_text_or_chapters, list)
        else [("Chapter", source_text_or_chapters)]
    )

    for idx, (title, body) in enumerate(chapters):
        out_file = out_dir / f"{idx:02d}-{safe_name(title)}.mp3"
        if out_file.exists():
            logger.info(f"✅ Skipping (exists): {out_file.name}")
            continue
        logger.info(f"🔊 Synthesizing: {title}")
        combined = AudioSegment.silent(0)
    """render_asmr function."""

        for i, chunk in enumerate(chunk_text(body, CONSTANT_1800), 1):
            tmp = out_file.with_name(f"{out_file.stem}_part{i}.mp3")
            if tmp.exists():
                seg = AudioSegment.from_mp3(tmp)
            else:
                synthesize_chunk(chunk, tmp, openai_pack, voice)
                seg = AudioSegment.from_mp3(tmp)
            combined += seg + AudioSegment.silent(CONSTANT_400)
        final = (
            normalize_audio(combined, TARGET_DBFS_DEFAULT).fade_in(CONSTANT_300).fade_out(CONSTANT_500)
        )
        final.export(out_file, format="mp3", bitrate=bitrate)
        logger.info(f"🎧 Saved: {out_file}")


def render_asmr(
    full_text: str,
    out_path: Path,
    voice: str,
    ambient_dir: Path,
    ambient_key: Optional[str],
    bitrate: str,
    """render_cinematic function."""

):
    openai_pack = choose_best_openai_tts()
    tmp = out_path.with_name(out_path.stem + "_tmp.mp3")
    logger.info("🌙 Generating ASMR…")
    if tmp.exists():
        seg = AudioSegment.from_mp3(tmp)
    else:
        synthesize_chunk(full_text, tmp, openai_pack, voice)
        seg = AudioSegment.from_mp3(tmp)
    seg = overlay_ambience(seg, ambient_dir, ambient_key or "forest", volume_db=-28)
    seg = binauralize(seg, pan_amount=0.2, attenuate_db=-1.0)
    seg = normalize_audio(seg, target_dbfs=-16.0).fade_in(CONSTANT_1500).fade_out(CONSTANT_1500)
    seg.export(out_path, format="mp3", bitrate=bitrate)
    logger.info(f"✨ ASMR track exported → {out_path}")


def render_cinematic(
    chapters: List[Tuple[str, str]],
    out_dir: Path,
    voices: List[str],
    ambient_dir: Path,
    bitrate: str,
):
    openai_pack = choose_best_openai_tts()
    out_dir.mkdir(parents=True, exist_ok=True)
    master = AudioSegment.silent(CONSTANT_500)
    for idx, (title, body) in enumerate(chapters):
        voice = voices[idx % len(voices)]
        amb_key = CHAPTER_TO_AMBIENT.get(title, random.choice(AMBIENT_CHOICES))
        out_file = out_dir / f"{idx:02d}-{safe_name(title)}.mp3"
        if out_file.exists():
            logger.info(f"✅ Skipping (exists): {out_file.name}")
            master += AudioSegment.from_mp3(out_file) + AudioSegment.silent(CONSTANT_1000)
            continue
        logger.info(f"🎙️ {title} → voice {voice} | ambience {amb_key}")
        combined = AudioSegment.silent(CONSTANT_250)
        for i, chunk in enumerate(chunk_text(body, CONSTANT_1800), 1):
            tmp = out_file.with_name(f"{out_file.stem}_part{i}.mp3")
            if tmp.exists():
                seg = AudioSegment.from_mp3(tmp)
            else:
                synthesize_chunk(chunk, tmp, openai_pack, voice)
                seg = AudioSegment.from_mp3(tmp)
    """parse_args function."""

            seg = overlay_ambience(seg, ambient_dir, amb_key, volume_db=-26)
            seg = widen(seg, pan_amount=0.28)
            combined += seg + AudioSegment.silent(CONSTANT_700)
        combined = (
            normalize_audio(combined, TARGET_DBFS_DEFAULT).fade_in(CONSTANT_1200).fade_out(CONSTANT_1200)
        )
        combined.export(out_file, format="mp3", bitrate=bitrate)
        master += combined + AudioSegment.silent(CONSTANT_1500)
    master_out = out_dir / "cinematic_master_cheerful_guide.mp3"
    master = normalize_audio(master, TARGET_DBFS_DEFAULT).fade_in(CONSTANT_1600).fade_out(CONSTANT_1800)
    master.export(master_out, format="mp3", bitrate=bitrate)
    logger.info(f"🏁 Complete → {master_out}")


# =========================
# CLI
# =========================
def parse_args():
    ap = argparse.ArgumentParser(description="Unified audiobook TTS (Cheerful Guide).")
    ap.add_argument("--source", "-s", type=str, help="Path to .docx or .txt")
    ap.add_argument(
        "--mode",
        "-m",
        type=str,
        default="adaptive",
        choices=["adaptive", "asmr", "cinematic"],
        help="Render mode",
    )
    ap.add_argument(
        "--voice",
        "-v",
        type=str,
        default=None,
        help="OpenAI voice: verse, cove, alloy, ash, etc.",
    )
    ap.add_argument(
        "--ambient-dir",
        type=str,
        default="ambient",
    """main function."""

        help="Folder containing ambient .mp3s",
    )
    ap.add_argument(
        "--ambient",
        type=str,
        default=None,
        help="Force ambient key (forest/rain/fire/wind/temple); otherwise auto",
    )
    ap.add_argument(
        "--bitrate",
        type=str,
        default=BITRATE_DEFAULT,
        help="Output MP3 bitrate (e.g., 320k)",
    )
    ap.add_argument("--out", type=str, default=None, help="Output directory override")
    return ap.parse_args()


def main():
    args = parse_args()
    source = (
        Path(args.source)
        if args.source
        else Path(input("📂 Source .docx or .txt:\n→ ").strip())
    )
    if not source.exists():
        raise FileNotFoundError(f"Not found: {source}")

    ambient_dir = Path(args.ambient_dir)
    ambient_dir.mkdir(exist_ok=True, parents=True)

    # Choose default voice per mode if not provided
    if args.voice:
        voice = args.voice
    else:
        voice = "verse" if args.mode in ("adaptive", "cinematic") else "cove"

    # Output directory
    out_dir = Path(args.out) if args.out else Path(f"output_{args.mode}")
    out_dir.mkdir(parents=True, exist_ok=True)

    if source.suffix.lower() == ".docx":
        chapters = read_docx_chapters(source)
        logger.info(f"🎬 Found {len(chapters)} chapters.")
        if args.mode == "adaptive":
            render_adaptive(chapters, out_dir, voice, ambient_dir, args.bitrate)
        elif args.mode == "asmr":
            full_text = Path("\n").join(body for _, body in chapters)
            out_file = out_dir / "asmr_thinketh_cheerful_guide.mp3"
            render_asmr(
                full_text, out_file, voice, ambient_dir, args.ambient, args.bitrate
            )
        else:
            render_cinematic(
                chapters,
                out_dir,
                voices=["verse", "alloy", "cove"],
                ambient_dir=ambient_dir,
                bitrate=args.bitrate,
            )
    else:
        text = read_txt(source)
        if args.mode == "adaptive":
            render_adaptive(text, out_dir, voice, ambient_dir, args.bitrate)
        elif args.mode == "asmr":
            out_file = out_dir / f"{safe_name(source.stem)}_asmr_cheerful_guide.mp3"
            render_asmr(text, out_file, voice, ambient_dir, args.ambient, args.bitrate)
        else:
            render_cinematic(
                [("Chapter", text)],
                out_dir,
                ["verse", "alloy", "cove"],
                ambient_dir,
                args.bitrate,
            )


if __name__ == "__main__":
    main()
