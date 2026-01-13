#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
thinketh_tts.py
Text-to-Speech generator for 'As A Man Thinketh' (James Allen)

Features:
 - Reads DOCX
 - Splits into chapters automatically
 - Handles token limits by chunking text
 - Merges all chunks into one MP3 per chapter
 - Skips already completed files
"""

import os
import re
from pathlib import Path
from docx import Document
from dotenv import load_dotenv
from openai import OpenAI
from pydub import AudioSegment


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib
from dotenv import load_dotenv

env_dir = PathLib.home() / ".env.d"
if env_dir.exists():
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


# ---------------- CONFIG ---------------- #
DOCX_PATH = Path("/Users/steven/Downloads/Compressed/thinketh_tts_package/AS-A-MAN-THINKETH-nonformat.docx")
OUT_DIR = Path("/Users/steven/Downloads/Compressed/thinketh_tts_package/output_mp3")
MODEL = "gpt-4o-mini-tts"
VOICE = "sage"   # try "alloy", "verse", or "cove" if you like different timbres
CHAPTERS = [
    "Foreword",
    "Thought and Character",
    "Effect of Thought on Circumstances",
    "Effect of Thought on Health and the Body",
    "Thought and Purpose",
    "The Thought-Factor in Achievement",
    "Visions and Ideals",
    "Serenity",
]
CHUNK_SIZE = 6000  # ~1500 tokens (safe)
# ---------------------------------------- #


def load_env():
    load_dotenv(Path.home() / ".env", override=False)
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Missing OPENAI_API_KEY in ~/.env")


def read_docx_text(docx_path: Path):
    doc = Document(docx_path)
    return [p.text.strip() for p in doc.paragraphs if p.text.strip()]


def normalize_text(t: str) -> str:
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def slugify(s: str) -> str:
    return re.sub(r"[^\w\-]+", "-", s.strip().lower()).strip("-")


def extract_chapters(paragraphs):
    """Divide text by known chapter titles."""
    joined = "\n".join(paragraphs)
    parts = []
    for i, title in enumerate(CHAPTERS):
        pattern = re.compile(rf"\b{re.escape(title)}\b", re.I)
        match = pattern.search(joined)
        if not match:
            continue
        start = match.end()
        end = None
        for next_title in CHAPTERS[i + 1:]:
            nxt = re.search(rf"\b{re.escape(next_title)}\b", joined[start:], re.I)
            if nxt:
                end = start + nxt.start()
                break
        body = joined[start:end].strip() if end else joined[start:].strip()
        parts.append((title, normalize_text(body)))
    if not parts:
        return [("Full Text", normalize_text(joined))]
    return parts


def synthesize_to_mp3(client, text: str, out_path: Path, model: str, voice: str):
    """
    Split long text into chunks, synthesize each, then merge into one MP3.
    """
    paragraphs = re.split(r'(?<=[.!?])\s+', text)
    chunks, current = [], ""

    for para in paragraphs:
        if len(current) + len(para) > CHUNK_SIZE:
            chunks.append(current.strip())
            current = para
        else:
            current += " " + para
    if current.strip():
        chunks.append(current.strip())

    print(f"    ↳ Splitting into {len(chunks)} chunks")

    full_audio = AudioSegment.empty()

    for i, chunk in enumerate(chunks, start=1):
        print(f"      🗣️ Chunk {i}/{len(chunks)} ({len(chunk)} chars)")
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=chunk,
            response_format="mp3"
        )
        temp_chunk_path = out_path.parent / f"{out_path.stem}_part{i}.mp3"
        temp_chunk_path.write_bytes(response.read())

        segment = AudioSegment.from_mp3(temp_chunk_path)
        full_audio += segment
        os.remove(temp_chunk_path)

    full_audio.export(out_path, format="mp3")


def main():
    load_env()
    client = OpenAI()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"📖 Reading {DOCX_PATH.name}...")
    paragraphs = read_docx_text(DOCX_PATH)
    chapters = extract_chapters(paragraphs)
    print(f"🎬 Found {len(chapters)} chapters.")

    for idx, (title, text) in enumerate(chapters):
        slug = f"{idx:02d}-{slugify(title)}"
        mp3_path = OUT_DIR / f"{slug}.mp3"

        if mp3_path.exists():
            print(f"✅ Skipping already done: {mp3_path.name}")
            continue

        print(f"🔊 Synthesizing: {title} → {mp3_path.name}")
        try:
            synthesize_to_mp3(client, text, mp3_path, MODEL, VOICE)
            print(f"🎧 Saved: {mp3_path.name}")
        except Exception as e:
            print(f"⚠️ Error while processing {title}: {e}")
            break

    print(f"\n✅ All done! Files saved in: {OUT_DIR}")


if __name__ == "__main__":
    main()
