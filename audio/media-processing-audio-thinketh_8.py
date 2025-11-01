"""
Media Processing Audio Thinketh 8

This module provides functionality for media processing audio thinketh 8.

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
CONSTANT_500 = 500
CONSTANT_700 = 700
CONSTANT_1200 = 1200
CONSTANT_1500 = 1500
CONSTANT_1600 = 1600
CONSTANT_1800 = 1800
CONSTANT_6000 = 6000
CONSTANT_8192 = 8192

#!/usr/bin/env python3
"""
Cinematic hybrid edition:
- cheerful-guide affect baked in
- dynamic voice rotation
- ambient overlays per chapter
- widening, fades, -14 LUFS target, CONSTANT_320 kbps mastering
"""

import os, random
from pathlib import Path
from dotenv import load_dotenv
from docx import Document
from pydub import AudioSegment
from utils.splitter import split_text
from utils.mixer import overlay_ambience, widen, normalize_audio
from utils.styles import apply_cheerful_guide_style
from utils.model_select import choose_best_openai_model, can_use_hf, hf_params
import requests

load_dotenv(os.path.expanduser("~/.env"))

VOICES_ROTATION = ["verse", "alloy", "cove"]
OUT_DIR = Path("output_scripty")
OUT_DIR.mkdir(exist_ok=True)
BITRATE = "320k"

CHAPTER_AMBIENT = {
    "Foreword": "temple",
    "Thought And Character": "fire",
    "Effect Of Thought On Circumstances": "rain",
    "Effect Of Thought On Health And The Body": "forest",
    "Thought And Purpose": "wind",
    "The Thought-Factor In Achievement": "fire",
    "Visions And Ideals": "temple",
    "Serenity": "forest",
}


def get_source():
    """get_source function."""

    path = input("📂 Please enter the path to your .docx source file:\n→ ").strip()
    if not os.path.exists(path):
        raise FileNotFoundError("Source file not found.")
    return path


    """openai_tts function."""

def openai_tts(client, model, text, voice, out_path: Path):
    styled = apply_cheerful_guide_style(text)
    resp = client.audio.speech.create(
        model=model, voice=voice, input=styled, response_format="mp3"
    )
    out_path.write_bytes(resp.read())

    """hf_bark_tts function."""


def hf_bark_tts(text, out_path: Path):
    key, model = hf_params()
    headers = {"Authorization": f"Bearer {key}"}
    resp = requests.post(
        f"https://api-inference.huggingface.co/models/{model}",
        headers=headers,
        json={"inputs": text},
        stream=True,
        timeout=CONSTANT_300,
    )
    if resp.status_code != CONSTANT_200:
        raise RuntimeError(f"HF TTS error: {resp.text}")
    with open(out_path, "wb") as f:
        for chunk in resp.iter_content(CONSTANT_8192):
            f.write(chunk)
    """synthesize_chunk function."""



def synthesize_chunk(text, tmp_path: Path, voice: str):
    client, model = choose_best_openai_model()
    if client and model:
        openai_tts(client, model, text, voice, tmp_path)
    elif can_use_hf():
        hf_bark_tts(text, tmp_path)
    else:
    """parse_chapters function."""

        raise RuntimeError("No TTS model available (OpenAI or HF).")


def parse_chapters(docx_path: str):
    doc = Document(docx_path)
    chapters, cur_t, cur_b = [], None, []
    for p in doc.paragraphs:
        t = p.text.strip()
        if not t:
            continue
        if t.isupper() and len(t.split()) < 10:
            if cur_t:
                chapters.append((cur_t.title(), Path("\n").join(cur_b)))
            cur_t, cur_b = t, []
        else:
            cur_b.append(t)
    if cur_t:
        chapters.append((cur_t.title(), Path("\n").join(cur_b)))
    """main function."""

    logger.info(f"🎬 Found {len(chapters)} chapters.")
    return chapters


def main():
    src = get_source()
    chapters = parse_chapters(src)

    master = AudioSegment.silent(CONSTANT_500)
    for i, (title, body) in enumerate(chapters):
        voice = VOICES_ROTATION[i % len(VOICES_ROTATION)]
        amb_key = CHAPTER_AMBIENT.get(
            title, random.choice(list(CHAPTER_AMBIENT.values()))
        )
        out_ch = OUT_DIR / f"{i:02d}-{title.lower().replace(' ','-')}.mp3"
        if out_ch.exists():
            logger.info(f"✅ Skipping: {out_ch.name}")
            continue

        logger.info(f"🎙️ {title} → voice {voice} | ambience {amb_key}")
        combined = AudioSegment.silent(CONSTANT_250)
        for j, chunk in enumerate(split_text(body, CONSTANT_6000), 1):
            tmp = OUT_DIR / f"{i:02d}_part{j}.mp3"
            synthesize_chunk(chunk, tmp, voice)
            seg = AudioSegment.from_mp3(tmp)
            seg = overlay_ambience(seg, amb_key, volume_db=-26)
            seg = widen(seg, pan_amount=0.28)
            combined += seg + AudioSegment.silent(CONSTANT_700)

        combined = (
            normalize_audio(combined, target_dbfs=-14.0).fade_in(CONSTANT_1200).fade_out(CONSTANT_1200)
        )
        combined.export(out_ch, format="mp3", bitrate=BITRATE)
        master += combined + AudioSegment.silent(CONSTANT_1500)

    master_out = OUT_DIR / "cinematic_master_cheerful_guide.mp3"
    master = normalize_audio(master, target_dbfs=-14.0).fade_in(CONSTANT_1600).fade_out(CONSTANT_1800)
    master.export(master_out, format="mp3", bitrate=BITRATE)
    logger.info(f"🏁 Complete → {master_out}")


if __name__ == "__main__":
    main()
