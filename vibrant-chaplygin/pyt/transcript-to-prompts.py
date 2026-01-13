#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate detailed, descriptive image prompts from a timestamped transcript.

Input:
  A transcript text file with lines like:
    [HH:MM:SS] some narrative text...
Output:
  - <base>_prompts.jsonl  (one JSON per prompt item)
  - <base>_prompts.md     (nicely formatted, ready to paste into your generator)
Design:
  For each line, we infer mood, setting, and symbolism, then produce a trio:
    - Transition image (connective visual)
    - Main image (cinematic narrative focus)
    - Filler/typography (graphic/overlay for pacing)
The script uses lightweight heuristics and word-shape detection to avoid
heavy dependencies while still yielding rich, cinematic prompts.
"""
import argparse, sys, json, re
from pathlib import Path

MOOD_WORDS = {
    "dark": ["dark", "night", "shadow", "void", "ruin", "storm", "grave", "mourning", "peril", "fear"],
    "luminous": ["light", "dawn", "gold", "sun", "shine", "halo", "spark", "glow", "hope", "rescue"],
    "electric": ["neon", "signal", "circuit", "electric", "wired", "static", "satellite", "pulse"],
    "organic": ["forest", "river", "rain", "leaf", "roots", "soil", "breath", "heart"],
    "ritual": ["ritual", "altar", "veil", "incantation", "circle", "choir", "bells", "torch"],
    "conflict": ["war", "battle", "clash", "riot", "rage", "flee", "strike", "siren"]
}

STYLE_HINTS = {
    "cinematic": ["ultra-detailed", "cinematic lighting", "volumetric fog", "wide-angle", "high dynamic range"],
    "typography": ["bold serif", "engraved lettering", "glowing glyphs", "kerning tight", "letterforms textured"],
    "surreal": ["surreal symbolism", "double exposure", "scale-shifted architecture", "dreamlike haze"],
    "documentary": ["handheld framing", "grain", "ambient realism", "muted palette"]
}

COLOR_THEMES = {
    "noir": ["deep blacks", "steel blues", "dim tungsten highlights"],
    "ember": ["volcanic orange", "charcoal", "cinder glow"],
    "aether": ["lunar silver", "cool violets", "teal highlights"],
    "civic_peril": ["alarm red", "ashen gray", "midnight blue"]
}

def parse_transcript_lines(text):
    items = []
    for raw in text.splitlines():
        raw = raw.strip()
        if not raw:
            continue
        m = re.match(r"\[(\d{2}:\d{2}:\d{2})\]\s*(.*)", raw)
        if m:
            ts, line = m.group(1), m.group(2).strip()
        else:
            ts, line = None, raw
        items.append({"ts": ts, "text": line})
    return items
def pick_tags(txt):
    txt_low = txt.lower()
    moods = [k for k, words in MOOD_WORDS.items() if any(w in txt_low for w in words)]
    styles = ["cinematic"]
    if any(w in txt_low for w in ("dream", "veil", "vision", "siren", "phantom", "myth")):
        styles.append("surreal")
    if any(w in txt_low for w in ("crowd", "protest", "city", "street", "sirens")):
        styles.append("documentary")
    colors = []
    if any(w in txt_low for w in ("fire", "ember", "lava", "ash", "burn")):
        colors.append("ember")
    if any(w in txt_low for w in ("night", "shadow", "noir", "moon")):
        colors.append("noir")
    if any(w in txt_low for w in ("signal", "neon", "pulse", "wires")):
        colors.append("aether")
    if any(w in txt_low for w in ("america", "nation", "civic", "republic", "flag", "liberty", "peril")):
        colors.append("civic_peril")
    return moods or ["luminous"], styles, colors or ["aether"]

def enrich_prompt(base_desc, moods, styles, colors):
    parts = []
    parts.append(base_desc)
    for tag in styles:
        parts += STYLE_HINTS.get(tag, [])
    if moods:
        mood_tag = moods[0]
        parts.append(f"mood: {mood_tag}")
    for c in colors:
        parts += COLOR_THEMES.get(c, [])
    parts += [
        "shallow depth of field, precise focus on subject",
        "subtle film grain, 4k detail",
        "composition balanced with leading lines"
    ]
    return ", ".join(parts)

def make_triplet(item, idx):
    ts = item["ts"] or f"{idx:02d}:00:00"
    text = item["text"]
    moods, styles, colors = pick_tags(text)
    transition = enrich_prompt(
        f"Transition scene at {ts}: symbolic connective imagery echoing the line meaning; motion blur trails, scene morphing to next context",
        moods, styles, colors
    )
    main = enrich_prompt(
        f"Main image at {ts}: cinematic narration distilled into a single decisive tableau that visualizes: {text}",
        moods, styles, colors
    )
    filler = enrich_prompt(
        f"Filler/typography card at {ts}: minimal graphic interlude; integrate a succinct phrase extracted from the line; letterforms textured, subtle glow; negative space for pacing",
        moods, styles + ['typography'], colors
    )
    return {
        "timestamp": ts,
        "source_line": text,
        "transition_prompt": transition,
        "main_image_prompt": main,
        "filler_prompt": filler
    }

def write_jsonl_md(base_path: Path, triplets):
    jsonl = base_path.with_suffix("_prompts.jsonl")
    md = base_path.with_suffix("_prompts.md")
    with open(jsonl, "w", encoding="utf-8") as jf:
        for t in triplets:
            jf.write(json.dumps(t, ensure_ascii=False) + Path("\n"))
    with open(md, "w", encoding="utf-8") as mf:
        mf.write(f"# Prompt Suite for {base_path.name}\n\n")
        for i, t in enumerate(triplets, 1):
            mf.write(f"## Line {i} — [{t['timestamp']}]\n")
            mf.write(f"**Source:** {t['source_line']}\n\n")
            mf.write(f"**Transition:** {t['transition_prompt']}\n\n")
            mf.write(f"**Main Image:** {t['main_image_prompt']}\n\n")
            mf.write(f"**Filler/Typo:** {t['filler_prompt']}\n\n---\n\n")
    return str(jsonl), str(md)

def main():
    ap = argparse.ArgumentParser(description="Generate detailed image prompts from a transcript with timestamps.")
    ap.add_argument("transcripts", nargs="+", help="Path(s) to transcript .txt files with [HH:MM:SS] lines")
    args = ap.parse_args()

    for path in args.transcripts:
        p = Path(path).expanduser().resolve()
        text = p.read_text(encoding="utf-8", errors="ignore")
        items = parse_transcript_lines(text)
        if not items:
            logger.info(f"[skip] empty transcript: {p}")
            continue
        triplets = [make_triplet(it, i) for i, it in enumerate(items, 1)]
        j, m = write_jsonl_md(p, triplets)
        logger.info(f"[ok] wrote:\n  {j}\n  {m}")

if __name__ == "__main__":
    main()
