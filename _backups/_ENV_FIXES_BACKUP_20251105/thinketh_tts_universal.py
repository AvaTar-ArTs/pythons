import os, tempfile, json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from pydub import AudioSegment
import requests
import subprocess

load_dotenv(os.path.expanduser("~/.env"))

# ============ CONFIG ============ #
OUTPUT_DIR = Path("output_universal")
OUTPUT_DIR.mkdir(exist_ok=True)
BITRATE = "320k"

VOICE = "verse"
MODEL_PRIORITY = [
    "gpt-4o-tts",             # best OpenAI voice synthesis
    "gpt-4o-audio-preview",   # fallback premium
    "gpt-4o-mini-tts"         # lowest fallback
]
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Open-source backup (Coqui / Bark via HuggingFace)
HF_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
HF_MODEL = "suno/bark-small"

# ================================= #

def best_openai_tts_model(client):
    """Return best available OpenAI model for TTS."""
    try:
        models = [m.id for m in client.models.list().data]
        for name in MODEL_PRIORITY:
            if name in models:
                return name
    except Exception as e:
        print("⚠️ Could not query OpenAI models:", e)
    return None

def synthesize_openai(client, text, out_path, model, voice):
    print(f"🔊 Synthesizing with {model} / voice={voice}")
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        format="mp3"
    )
    with open(out_path, "wb") as f:
        f.write(response.read())

def synthesize_huggingface(text, out_path):
    """Fallback open-source TTS using Bark (via HF API)."""
    print("🦜 Using Hugging Face Bark TTS fallback...")
    headers = {"Authorization": f"Bearer {HF_KEY}"}
    payload = {"inputs": text}
    resp = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers=headers, json=payload, stream=True
    )
    if resp.status_code != 200:
        raise RuntimeError(f"HuggingFace API error: {resp.text}")
    with open(out_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

def add_ambient(mp3_path, ambient_path=None):
    """Mix narration with ambient background (if provided)."""
    base = AudioSegment.from_file(mp3_path)
    if ambient_path and Path(ambient_path).exists():
        amb = AudioSegment.from_file(ambient_path)
        amb = amb - 24  # lower background volume
        mixed = base.overlay(amb.loop(duration=len(base)))
    else:
        mixed = base
    out = mp3_path.replace(".mp3", "_mixed.mp3")
    mixed.export(out, format="mp3", bitrate=BITRATE)
    print(f"🎧 Mixed version exported → {out}")

def main():
    print("📂 Please enter the path to your .docx or .txt source file:")
    src = input("→ ").strip().strip('"')
    text = Path(src).read_text(encoding="utf-8") if src.endswith(".txt") else None
    if not text:
        from docx import Document
        doc = Document(src)
        text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    out_file = OUTPUT_DIR / f"{Path(src).stem}_tts.mp3"
    client = OpenAI(api_key=OPENAI_KEY)
    model = best_openai_tts_model(client)

    try:
        if model:
            synthesize_openai(client, text, out_file, model, VOICE)
        elif HF_KEY:
            synthesize_huggingface(text, out_file)
        else:
            raise RuntimeError("No TTS model or API available.")
        add_ambient(out_file, "ambient/thoughts.mp3")  # optional
        print("✅ Done.")
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    main()
