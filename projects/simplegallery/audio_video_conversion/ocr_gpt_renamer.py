#!/usr/bin/env python3

"""Recursive OCR + GPT-4o Renamer & Prompt Generator (Noise-Resistant)

- Images: .jpg .jpeg .png .webp .tiff
- Videos: .mp4 .webm .mov .mkv
- Loads OPENAI_API_KEY from ~/env
- Preview mode by default (no changes). Use --apply / -a to rename.
- CSV (TAB-delimited): Old Path | New Path | Detected Title | File Type | Prompt

macOS setup:
  brew install tesseract
  pip install pillow pytesseract opencv-python python-dotenv openai

Run (preview):
  python ocr_gpt_renamer.py /path/to/folder

Apply:
  python ocr_gpt_renamer.py /path/to/folder --apply
"""

import os
import re
import csv
import sys
import argparse
from pathlib import Path

from PIL import Image, ImageOps
import pytesseract
import cv2

from dotenv import load_dotenv
import openai

# ------------------------- CONFIG -------------------------

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tiff"}
VIDEO_EXTS = {".mp4", ".webm", ".mov", ".mkv"}
CSV_HEADERS = ["Old Path", "New Path", "Detected Title", "File Type", "Prompt"]

# Words to ignore when building a title from OCR
BLACKLIST = {
    "filename",
    "file",
    "image",
    "photo",
    "picture",
    "design",
    "untitled",
    "screenshot",
    "img",
    "jpg",
    "jpeg",
    "png",
    "webp",
    "tiff",
    "video",
    "mov",
    "mp4",
    "webm",
    "mkv",
    "copy",
    "final",
    "draft",
    "edit",
    "v1",
    "v2",
    "v3",
}
# Skip very short junk/filler tokens except roman numerals or single letters like A, I
MIN_TOKEN_LEN = 2
OCR_CONF_THRESHOLD = 65  # pytesseract "conf" (0-100)
MIN_WORDS_FOR_TITLE = 2  # if only one decent token, we’ll still try, but prefer >=2
MAX_TITLE_WORDS = 5  # keep titles concise

# ------------------------- ENV / API -------------------------


def load_api_key_from_home_env() -> str:
    env_file = Path.home() / "env"
    if env_file.exists():
        load_dotenv(env_file)
    else:
        raise RuntimeError(f"Environment file not found: {env_file}")
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("Missing OPENAI_API_KEY in ~/env")
    return key


openai.api_key = load_api_key_from_home_env()

# ------------------------- OCR HELPERS -------------------------


def _preprocess_for_ocr(img: Image.Image) -> Image.Image:
    """Improve OCR reliability with simple preprocessing."""
    # Convert to grayscale and increase contrast
    g = ImageOps.grayscale(img)
    g = ImageOps.autocontrast(g)
    return g


def _ocr_data(img: Image.Image):
    """Get detailed OCR data (words, conf, boxes)."""
    img_prep = _preprocess_for_ocr(img)
    data = pytesseract.image_to_data(img_prep, output_type=pytesseract.Output.DICT)
    return data


def _clean_token(tok: str) -> str:
    tok = tok.strip()
    tok = re.sub(
        r"[^\w\.\-’'&]+",
        "",
        tok,
    )  # keep letters/numbers/&/apostrophes/dots (for L.A.)
    # collapse ellipses and dots like "E.W..." → "EW"
    tok = tok.replace("...", "").replace("..", ".")
    tok = tok.replace(".", "")  # after preserving acronyms, drop dots for filename
    return tok


def _good_token(tok: str) -> bool:
    if not tok:
        return False
    low = tok.lower()
    if low in BLACKLIST:
        return False
    if len(tok) < MIN_TOKEN_LEN and low not in {"a", "i"}:
        return False
    # reject random leftover digits-only tokens
    if tok.isdigit():
        return False
    return True


def _titlecase_join(tokens: list[str]) -> str:
    cased = []
    for t in tokens:
        if t.isupper() and len(t) <= 4:
            cased.append(t)  # keep short acronyms as upper (e.g., LA, NYC)
        else:
            cased.append(t.capitalize())
    return "".join(cased)  # no spaces/underscores


def ocr_detect_title(img: Image.Image) -> tuple[str, bool]:
    """Return (title, has_typography).
    We aggregate high-confidence, large-ish words in reading order into a clean TitleCase slug.
    """
    data = _ocr_data(img)
    n = len(data.get("text", []))
    words = []
    for i in range(n):
        text = data["text"][i]
        conf = data["conf"][i]
        if not text or text.strip() == "" or conf == "-1":
            continue
        try:
            conf_val = float(conf)
        except Exception:
            conf_val = 0.0
        if conf_val < OCR_CONF_THRESHOLD:
            continue

        # bounding box area heuristic: prefer larger words
        w = int(data["width"][i]) if "width" in data else 0
        h = int(data["height"][i]) if "height" in data else 0
        area = w * h

        tok = _clean_token(text)
        if not _good_token(tok):
            continue
        words.append((data["left"][i], data["top"][i], area, tok))

    if not words:
        return "", False

    # Sort by reading order: top then left
    words.sort(key=lambda x: (x[1], x[0]))

    # Prefer top N by area but still in reading order
    # Compute area threshold (e.g., top 60% area words)
    areas = [w[2] for w in words]
    if areas:
        cutoff = sorted(areas, reverse=True)[max(1, int(0.6 * len(areas))) - 1]
        selected = [w for w in words if w[2] >= cutoff]
        # keep reading order
        selected.sort(key=lambda x: (x[1], x[0]))
    else:
        selected = words

    tokens = [w[3] for w in selected][:MAX_TITLE_WORDS]

    # If we still have too few tokens, fall back to best high-conf words (top by area)
    if len(tokens) < MIN_WORDS_FOR_TITLE:
        tokens = [
            w[3]
            for w in sorted(words, key=lambda x: x[2], reverse=True)[:MAX_TITLE_WORDS]
        ]

    # Final cleanup & join
    tokens = [t for t in tokens if _good_token(t)]
    if not tokens:
        return "", False

    title = _titlecase_join(tokens)
    # final safety: only letters/digits in filename
    title = re.sub(r"[^\w]", "", title)
    return title, True


# ------------------------- VIDEO HELPERS -------------------------


def best_video_frame(:
    video_path: Path,
    sample_secs=(0.5, 1.0, 1.5, 2.0),
) -> Image.Image | None:
    """Grab multiple early frames and return the one with most OCRable text."""
    best_img = None
    best_score = -1
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return None
    try:
        for sec in sample_secs:
            cap.set(cv2.CAP_PROP_POS_MSEC, int(sec * 1000))
            ok, frame = cap.read()
            if not ok:
                continue
            pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            data = _ocr_data(pil)
            # score: count of high-conf tokens
            score = 0
            for i, text in enumerate(data.get("text", [])):
                if not text:
                    continue
                conf = data["conf"][i]
                try:
                    conf_val = float(conf)
                except Exception:
                    conf_val = 0.0
                if conf_val >= OCR_CONF_THRESHOLD:
                    tok = _clean_token(text)
                    if _good_token(tok):
                        score += 1
            if score > best_score:
                best_score = score
                best_img = pil
    finally:
        cap.release()
    return best_img


# ------------------------- GPT REFINEMENT -------------------------


def gpt_refine_and_describe(:
    raw_title: str,
    content_hint: str,
    need_typography: bool,
) -> tuple[str, str]:
    """Use GPT-4o to (1) sanitize/refine the title into TitleCase/no spaces; (2) generate a vivid description."""
    system_msg = (
        "You clean OCR-extracted titles and write vivid, concise visual descriptions for prompts. "
        "Return two lines:\n"
        "LINE1: Clean TitleCase filename-safe title (only letters/numbers, no spaces or underscores).\n"
        "LINE2: A short, concrete description of the visual style, subject, mood, setting, and notable elements."
    )
    user_msg = (
        f"OCR Title Candidate: {raw_title or 'NONE'}\n"
        f"Content Hint: {content_hint}\n"
        f"Typography Present: {need_typography!s}"
    )
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            max_tokens=220,
            temperature=0.3,
        )
        text = resp.choices[0].message.content.strip()
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        clean_title = re.sub(r"[^\w]", "", (lines[0] if lines else raw_title))
        description = (lines[1] if len(lines) > 1 else content_hint).rstrip(".")
    except Exception:
        # Fallback: trust OCR title and generic description
        clean_title = re.sub(r"[^\w]", "", raw_title) or "Image"
        description = content_hint.rstrip(".")

    # Build the final prompt
    if need_typography and clean_title:
        prompt = (
            f"Create a vibrant and alive typography cover image with a prompt that both spells out the '{clean_title}' "
            f"and reflects {description}, capturing the essence with an edgy and geeky style. "
            f"Bring to life through imagery that reflects the emotional and thematic content. "
            f"The aspect ratio of the generated image: 9:16. "
            f"The background setting of the image: solid color. "
            f"The resolution of the image: 1080x1920 pixels"
        )
    else:
        prompt = (
            f"Create a vibrant and alive cover image that reflects {description}, capturing the essence with an edgy and geeky style. "
            f"Bring to life through imagery that reflects the emotional and thematic content. "
            f"The aspect ratio of the generated image: 9:16. "
            f"The background setting of the image: solid color. "
            f"The resolution of the image: 1080x1920 pixels"
        )
    return clean_title or "Image", prompt


# ------------------------- CORE PROCESSING -------------------------


def process_media(path: Path) -> tuple[Path, Path, str, str, str, bool]:
    """Returns: old_path, new_path, detected_title, file_type, prompt, needs_rename"""
    ext = path.suffix.lower()
    file_type = "image" if ext in IMAGE_EXTS else "video"
    ocr_title = ""
    has_typography = False

    try:
        if file_type == "image":
            img = Image.open(path)
            ocr_title, has_typography = ocr_detect_title(img)
        else:
            frame = best_video_frame(path)
            if frame:
                ocr_title, has_typography = ocr_detect_title(frame)
    except Exception as e:
        print(f"[WARN] OCR failed on {path}: {e}")

    # Content hint can be basic—GPT will expand into rich description
    content_hint = "a bold graphic poster with festive colors and holiday elements"  # generic fallback
    clean_title, prompt = gpt_refine_and_describe(
        ocr_title,
        content_hint,
        has_typography,
    )

    current_stem = path.stem
    needs_rename = (
        has_typography and clean_title and (clean_title.lower() != current_stem.lower())
    )

    new_path = path
    if needs_rename:
        candidate = path.with_name(f"{clean_title}{path.suffix}")
        k = 2
        while candidate.exists():
            candidate = path.with_name(f"{clean_title}-{k}{path.suffix}")
            k += 1
        new_path = candidate

    return path, new_path, clean_title, file_type, prompt, needs_rename


def walk_and_process(root: Path, apply: bool, confirm: bool) -> list[list[str]]:
    rows: list[list[str]] = []
    # Confirmation if applying
    if apply and confirm:
        ans = input("Apply renaming to files? [y/N]: ").strip().lower()
        if ans not in {"y", "yes"}:
            print("Aborted.")
            sys.exit(0)

    for dirpath, _, files in os.walk(root):
        for fn in files:
            ext = Path(fn).suffix.lower()
            if ext not in IMAGE_EXTS and ext not in VIDEO_EXTS:
                continue
            fpath = Path(dirpath) / fn
            old_path, new_path, title, ftype, prompt, needs_rename = process_media(
                fpath,
            )
            rows.append([str(old_path), str(new_path), title, ftype, prompt])
            if apply and needs_rename:
                try:
                    os.rename(old_path, new_path)
                    print(f"[RENAMED] {old_path.name} -> {new_path.name}")
                except Exception as e:
                    print(f"[ERROR] Could not rename {old_path}: {e}")
    return rows


# ------------------------- CLI -------------------------


def main():
    ap = argparse.ArgumentParser(
        description="Noise-resistant OCR + GPT-4o renamer with prompt CSV.",
    )
    ap.add_argument("folder", help="Root folder to scan")
    ap.add_argument(
        "--apply",
        "-a",
        action="store_true",
        help="Apply renaming (default: preview only)",
    )
    ap.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="Skip confirmation when applying",
    )
    ap.add_argument(
        "--csv",
        default="output.csv",
        help="CSV output path (TAB-delimited)",
    )
    args = ap.parse_args()

    root = Path(args.folder).expanduser()
    if not root.exists():
        print(f"Path does not exist: {root}")
        sys.exit(1)

    rows = walk_and_process(root, apply=args.apply, confirm=not args.yes)

    # Write CSV
    outcsv = Path(args.csv).expanduser()
    outcsv.parent.mkdir(parents=True, exist_ok=True)
    with open(outcsv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(CSV_HEADERS)
        w.writerows(rows)

    print(f"\nProcessed {len(rows)} files.")
    print(f"CSV saved to: {outcsv}")
    if not args.apply:
        print("Preview mode only. Use --apply (or -a) to rename.")


if __name__ == "__main__":
    main()
