
import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOCX -> per-chapter MP3s using OpenAI TTS.
- Keys from ~/.env  (OPENAI_API_KEY=sk-...)
- Chapter detection via docx heading styles OR fallback regex for known titles
- Voices: alloy, ash, ballad, coral, echo, fable, nova, onyx, sage, shimmer
- Alias: cove -> sage
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import List, Tuple, Iterable, Dict

# -------- env loader (quiet) --------
def load_home_env():
    try:
        from dotenv import load_dotenv
        load_dotenv(Path.home() / ".env", override=False)
    except Exception:
        pass

# -------- voices / model --------
VALID_VOICES = ["alloy","ash","ballad","coral","echo","fable","nova","onyx","sage","shimmer"]
VOICE_ALIASES: Dict[str, str] = {"cove":"sage"}
DEFAULT_MODEL = "gpt-4o-mini-tts"

# -------- docx reader --------
def read_docx_text(docx_path: Path) -> List[Tuple[str, str]]:
    """
    Return a list of (style_name, text) per paragraph.
    """
    from docx import Document
    doc = Document(docx_path)
    out = []
    for p in doc.paragraphs:
        txt = p.text.strip()
        if not txt:
            continue
        style = getattr(p.style, "name", "") or ""
        out.append((style, txt))
    return out

# -------- chapter detection --------
CHAPTER_TITLES = [
    "Foreword",
    "Thought and Character",
    "Effect of Thought on Circumstances",
    "Effect of Thought on Health and the Body",
    "Thought and Purpose",
    "The Thought-Factor in Achievement",
    "Visions and Ideals",
    "Serenity",
]

def make_heading_regex(title: str) -> re.Pattern:
    safe = re.escape(title)
    # Match either pure line or markdown-like heading text
    return re.compile(rf"^\s*(?:#+\s*)?{safe}\s*$", flags=re.I)

def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^\w\s-]+", "", s)
    s = re.sub(r"\s+", "-", s)
    return s.strip("-")

def normalize_body(t: str) -> str:
    t = t.replace(Path("\r\n"),Path("\n")).replace(Path("\r"),Path("\n"))
    t = re.sub(r"[ \t]+"," ",t)
    t = re.sub(r"\n{3,}",Path("\n\n"),t)
    t = t.replace("[PAUSE=short]", ".")
    return t.strip()

def extract_chapters(paragraphs: List[Tuple[str,str]]) -> List[Tuple[str,str]]:
    """
    Try headings first. If none, fall back to regex matching titles within body lines.
    """
    # 1) Build a plain text with markers so we can split
    lines = []
    for style, txt in paragraphs:
        # Treat styles named like Heading 1/2/etc as headings
        is_heading_style = bool(re.search(r"\bHeading\b|\bTitle\b", style, flags=re.I))
        if is_heading_style:
            lines.append(f"@@H@@ {txt.strip()}")
        else:
            lines.append(txt.strip())
    joined = Path("\n").join(lines)

    # 2) First pass: split on actual heading markers
    parts = []
    indices = []
    for m in re.finditer(r"^@@H@@\s+(.*)$", joined, flags=re.M):
        indices.append((m.start(), m.end(), m.group(1).strip()))
    if indices:
        # Section spans
        for i, (s, e, title) in enumerate(indices):
            start = e
            end = indices[i+1][0] if i+1 < len(indices) else len(joined)
            body = joined[start:end].strip()
            parts.append((title, body))
    else:
        # 3) Fallback: find canonical titles by regex in raw lines
        # build doc as lines and mark matches
        all_lines = joined.splitlines()
        hits = []
        regs = [(t, make_heading_regex(t)) for t in CHAPTER_TITLES]
        for i, ln in enumerate(all_lines):
            for t, rgx in regs:
                if rgx.match(ln):
                    hits.append((i, t))
        hits.sort(key=lambda x: x[0])
        if hits:
            for i, (line_idx, title) in enumerate(hits):
                start = line_idx + 1
                end = hits[i+1][0] if i+1 < len(hits) else len(all_lines)
                body = Path("\n").join(all_lines[start:end]).strip()
                parts.append((title, body))
        else:
            # 4) If still nothing, shrug and dump everything as one section
            whole = normalize_body(joined)
            return [("Full Text", whole)]

    # Optional epigraph: capture preface text before first known chapter if present
    # Not strictly needed for TTS; keeping only canonical chapters is fine.
    final = []
    title_set = set(t.lower() for t in CHAPTER_TITLES)
    for title, body in parts:
        if title.lower() in title_set:
            final.append((title, normalize_body(body)))
    if not final:
        return [("Full Text", normalize_body(joined))]
    return final

# -------- OpenAI TTS --------
def ensure_voice(v: str) -> str:
    key = (v or "").strip().lower()
    if key in VOICE_ALIASES:
        key = VOICE_ALIASES[key]
    if key not in VALID_VOICES:
        raise SystemExit(f"Invalid voice: {v}\nValid: {', '.join(VALID_VOICES)}\nAliases: cove->sage")
    return key

def openai_client():
    load_home_env()
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY not found in ~/.env. Put it there, like an adult.")
    from openai import OpenAI
    return OpenAI()

def synth_mp3_bytes(client, text: str, model: str, voice: str) -> bytes:
    resp = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        format="mp3"
    )
    return resp.read()

# -------- I/O helpers --------
def write_jsonl(chapters: List[Tuple[str,str]], out_jsonl: Path):
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with out_jsonl.open("w", encoding="utf-8") as f:
        for i, (title, body) in enumerate(chapters):
            rec = {
                "order": i,
                "slug": f"{i:02d}-{slugify(title)}",
                "title": title,
                "text": body
            }
            f.write(json.dumps(rec, ensure_ascii=False) + Path("\n"))

def render_chapters_to_mp3s(chapters: List[Tuple[str,str]], out_dir: Path, voice: str, model: str):
    out_dir.mkdir(parents=True, exist_ok=True)
    client = openai_client()
    for i, (title, body) in enumerate(chapters):
        text = body.strip()
        if not text:
            continue
        slug = f"{i:02d}-{slugify(title)}"
        audio = synth_mp3_bytes(client, text, model, voice)
        (out_dir / f"{slug}.mp3").write_bytes(audio)
        logger.info(f"wrote {out_dir / (slug + '.mp3')}")

# -------- CLI --------
def parse_args():
    p = argparse.ArgumentParser(description="DOCX -> OpenAI TTS (per chapter).")
    p.add_argument("-i","--input", type=str,
                   default=Path("/Users/steven/Documents/AS-A-MAN-THINKETH-nonformat.docx"),
                   help="Path to input .docx")
    p.add_argument("-o","--outdir", type=str, default="thinketh_mp3",
                   help="Output root directory (default: thinketh_mp3)")
    p.add_argument("-v","--voice", type=str, default="cove",
                   help="Voice or alias (cove|alloy|ash|ballad|coral|echo|fable|nova|onyx|sage|shimmer)")
    p.add_argument("-m","--model", type=str, default=DEFAULT_MODEL,
                   help=f"TTS model (default: {DEFAULT_MODEL})")
    p.add_argument("--emit-jsonl", action="store_true",
                   help="Also write chapters.jsonl next to MP3s.")
    return p.parse_args()

def main():
    args = parse_args()
    docx_path = Path(args.input).expanduser()
    if not docx_path.exists():
        raise SystemExit(f"Input not found: {docx_path}")
    voice = ensure_voice(args.voice)
    out_root = Path(args.outdir)
    voice_dir = out_root / voice

    # Parse chapters
    paragraphs = read_docx_text(docx_path)
    chapters = extract_chapters(paragraphs)

    # Optional JSONL export
    if args.emit_jsonl:
        write_jsonl(ch_

