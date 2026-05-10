#!/usr/bin/env python3
"""
🎧 Adaptive Emotional Audiobook Generator (Cheerful Guide Style) 🎧
✨ Prefers OpenAI gpt-4o-tts, with a fallback to HF Bark if needed. ✨
"""

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
                            value = value.strip().strip('\'').strip("\'")
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

import os
from pathlib import Path
from dotenv import load_dotenv
from docx import Document
from pydub import AudioSegment
from utils.splitter import split_text
from utils.mixer import normalize_audio
from utils.styles import apply_cheerful_guide_style
from utils.model_select import choose_best_openai_model, can_use_hf, hf_params
import requests


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib

    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


# 🌿 Load environment variables
load_dotenv(os.path.expanduser("~/.env"))

# 🎤 Voice and Output Configuration
VOICE = os.getenv("OPENAI_TTS_VOICE", "verse")
OUT_DIR = Path("output_adaptive")
OUT_DIR.mkdir(exist_ok=True)
BITRATE = "320k"

def get_source():
    """📂 Prompt user for the path to the .docx source file."""
    path = input("📂 Please enter the path to your .docx source file:\n→ ").strip()
    if not os.path.exists(path):
        raise FileNotFoundError("❌ Source file not found.")
    return path

def read_chapters(docx_path: str):
    """📖 Read and parse chapters from the .docx file."""
    doc = Document(docx_path)
    chapters, cur_t, cur_b = [], None, []
    for p in doc.paragraphs:
        t = p.text.strip()
        if not t:
            continue
        if t.isupper() and len(t.split()) < 10:
            if cur_t:
                chapters.append((cur_t.title(), "\n".join(cur_b)))
            cur_t, cur_b = t, []
        else:
            cur_b.append(t)
    if cur_t:
        chapters.append((cur_t.title(), "\n".join(cur_b)))
    print(f"🎬 Found {len(chapters)} chapters.")
    return chapters

def openai_tts(client, model, text, voice, out_path: Path):
    """🔊 Synthesize text to speech using OpenAI."""
    styled = apply_cheerful_guide_style(text)
    resp = client.audio.speech.create(
        model=model, voice=voice, input=styled, response_format="mp3"
    )
    out_path.write_bytes(resp.read())

def hf_bark_tts(text, out_path: Path):
    """🦜 Synthesize text to speech using Hugging Face Bark."""
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
    """🔄 Synthesize a chunk of text using the best available TTS model."""
    client, model = choose_best_openai_model()
    if client and model:
        openai_tts(client, model, text, VOICE, tmp_path)
    elif can_use_hf():
        hf_bark_tts(text, tmp_path)
    else:
        raise RuntimeError("No TTS model available (OpenAI or HF).")

def main():
    """🚀 Main function to process the source file and generate audio."""
    src = get_source()
    chapters = read_chapters(src)
    for idx, (title, body) in enumerate(chapters):
        out_file = OUT_DIR / f"{idx:02d}-{title.lower().replace(' ','-')}.mp3"
        if out_file.exists():
            print(f"✅ Skipping: {out_file.name}")
            continue

        print(f"🔊 Synthesizing: {title}")
        combined = AudioSegment.silent(0)
        chunks = split_text(body, 6000)  # safe chunking
        for i, chunk in enumerate(chunks, 1):
            tmp = out_file.with_name(f"{out_file.stem}_part{i}.mp3")
            synthesize_chunk(chunk, tmp)
            combined += AudioSegment.from_mp3(tmp) + AudioSegment.silent(400)

        combined = (
            normalize_audio(combined, target_dbfs=-14.0).fade_in(300).fade_out(500)
        )
        combined.export(out_file, format="mp3", bitrate=BITRATE)
        print(f"🎧 Saved: {out_file}")

    print(f"\n✅ All done → {OUT_DIR}")

if __name__ == "__main__":
    main()
