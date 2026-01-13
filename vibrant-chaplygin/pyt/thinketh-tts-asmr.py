#!/usr/bin/env python3
"""
ASMR whisper edition with cheerful-guide affect,
ambient option, binaural widening, 320 kbps mastering.
"""

import os, random
from pathlib import Path
from dotenv import load_dotenv
from docx import Document
from pydub import AudioSegment, effects
from utils.splitter import split_text
from utils.mixer import overlay_ambience, binauralize, normalize_audio
from utils.styles import apply_cheerful_guide_style
from utils.model_select import choose_best_openai_model, can_use_hf, hf_params
import requests


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib
from dotenv import load_dotenv

env_dir = PathLib.home() / ".env.d"
if env_dir.exists():
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


load_dotenv(os.path.expanduser("~/.env"))

VOICE = os.getenv("OPENAI_TTS_VOICE_ASMR", "cove")
OUT_DIR = Path("output_asmr")
OUT_DIR.mkdir(exist_ok=True)
BITRATE = "320k"
AMBIENTS = ["forest", "rain", "wind", "fire", "temple"]


def get_source():
    path = input("📂 Please enter the path to your .docx source file:\n→ ").strip()
    if not os.path.exists(path):
        raise FileNotFoundError("Source file not found.")
    return path


def openai_tts(client, model, text, voice, out_path: Path):
    styled = apply_cheerful_guide_style(text)
    resp = client.audio.speech.create(
        model=model, voice=voice, input=styled, response_format="mp3"
    )
    out_path.write_bytes(resp.read())


def hf_bark_tts(text, out_path: Path):
    key, model = hf_params()
    headers = {"Authorization": f"Bearer {key}"}
    resp = requests.post(
        f"https://api-inference.huggingface.co/models/{model}",
        headers=headers,
        json={"inputs": text},
        stream=True,
        timeout=300,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"HF TTS error: {resp.text}")
    with open(out_path, "wb") as f:
        for chunk in resp.iter_content(8192):
            f.write(chunk)


def synthesize_chunk(text, tmp_path: Path):
    client, model = choose_best_openai_model()
    if client and model:
        openai_tts(client, model, text, VOICE, tmp_path)
    elif can_use_hf():
        hf_bark_tts(text, tmp_path)
    else:
        raise RuntimeError("No TTS model available (OpenAI or HF).")


def main():
    src = get_source()
    doc = Document(src)
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    chunks = split_text(text, 6000)

    print("🌙 Generating ASMR edition…")
    amb_key = random.choice(AMBIENTS)
    combined = AudioSegment.silent(500)

    for i, chunk in enumerate(chunks, 1):
        tmp = OUT_DIR / f"asmr_part{i}.mp3"
        synthesize_chunk(chunk, tmp)
        seg = AudioSegment.from_mp3(tmp)
        seg = overlay_ambience(seg, amb_key, volume_db=-28)
        seg = binauralize(seg)
        combined += seg + AudioSegment.silent(500)

    combined = normalize_audio(combined, target_dbfs=-16.0).fade_in(1500).fade_out(1500)
    out_mp3 = OUT_DIR / "asmr_thinketh_cheerful_guide.mp3"
    combined.export(out_mp3, format="mp3", bitrate=BITRATE)
    print(f"✨ ASMR track exported → {out_mp3}")


if __name__ == "__main__":
    main()
