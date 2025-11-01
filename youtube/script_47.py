"""
Script 47

This module provides functionality for script 47.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_120 = 120
CONSTANT_200 = 200
CONSTANT_400 = 400
CONSTANT_12000 = 12000

#!/usr/bin/env python3
"""
script_cataloger.py — Safe cataloger/organizer for Python projects.

Key features
- DRY-RUN by default (no file changes unless --apply)
- Modes: index (no changes), move, copy, link (symlink)
- Rules-based categorization (imports + keywords)
- Optional LLM assist if --use-llm and OPENAI_API_KEY present
- Outputs CSV + Markdown portfolio grouped by category
- Ignores common junk: .git, __pycache__, venvs, .ipynb_checkpoints

Usage
  python script_cataloger.py --root ~/Documents/Python \
      --dest ~/Documents/Categorized \
      --mode link --apply \
      --out-csv catalog.csv --out-md PORTFOLIO.md \
      --github-root https://github.com/ichoake/python/tree/main \
      --use-llm

"""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import os
import re
import shutil
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

# --------- Heuristic rules (augmented by categories.json if provided) ---------
DEFAULT_RULES = {
    "AI / LLM": {
        "imports": ["openai", "transformers", "torch", "langchain", "llama_index", "vertexai"],
        "keywords": ["gpt", "whisper", "tts", "embed", "inference", "llm"],
    },
    "Video / Audio": {
        "imports": ["ffmpeg", "moviepy", "librosa", "pydub", "cv2", "yt_dlp", "pytube"],
        "keywords": ["mp3", "mp4", "wav", "video", "subtitle", "caption", "b-roll", "codec"],
    },
    "Images / Graphics / POD": {
        "imports": ["PIL", "pil", "pillow", "opencv", "cv2"],
        "keywords": ["resize", "upscale", "thumbnail", "mockup", "jpeg", "png", "psd", "redbubble", "printify"],
    },
    "Web / APIs": {
        "imports": ["requests", "flask", "fastapi", "httpx", "boto3"],
        "keywords": ["endpoint", "oauth", "api", "webhook"],
    },
    "Automation / Selenium": {
        "imports": ["selenium", "playwright"],
        "keywords": ["browser", "automation", "scrape", "headless"],
    },
    "Data / CSV": {
        "imports": ["pandas", "numpy", "polars", "csv"],
        "keywords": ["dataset", "dataframe", "csv", "etl", "merge"],
    },
    "YouTube / Streaming": {
        "imports": ["googleapiclient", "twitch", "pytube"],
        "keywords": ["youtube", "shorts", "twitch", "vod", "channel", "playlist"],
    },
    "File Utilities": {
        "imports": ["pathlib", "shutil", "zipfile", "glob"],
        "keywords": ["rename", "organize", "dedupe", "scan", "move", "copy"],
    },
}

IGNORE_DIRS = {".git", "__pycache__", ".ipynb_checkpoints", "venv", ".venv", "env", ".history"}
PY_EXT = {".py"}

@dataclass
class Record:
    path: str
    rel_path: str
    category: str
    title: str
    description: str
    imports: str
    mode_planned: str
    dest_path: str

def read_text_safe(p: Path, limit_bytes: int = 800_000) -> str:
    """read_text_safe function."""

    try:
        if p.stat().st_size > limit_bytes:
            return ""
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

    """ast_imports function."""

def ast_imports(src: str) -> List[str]:
    out = []
    if not src:
        return out
    try:
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    out.append(n.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    out.append(node.module.split(".")[0])
    except Exception:
        pass
    return sorted(set(out))
    """sniff_title_description function."""


def sniff_title_description(src: str) -> Tuple[str, str]:
    title = ""
    desc = ""
    if not src:
        return title, desc
    # Module docstring
    try:
        tree = ast.parse(src)
        doc = ast.get_docstring(tree) or ""
    except Exception:
        doc = ""
    # Title from first line / filename will be set elsewhere; here we try docstring first line
    if doc:
        lines = [l.strip() for l in doc.splitlines() if l.strip()]
        if lines:
            title = lines[0][:CONSTANT_120]
            desc = " ".join(lines[1:])[:CONSTANT_400]
    # Fallback: comments at top
    if not title:
        for line in src.splitlines()[:15]:
            if line.strip().startswith("#"):
                t = line.lstrip("# ").strip()
                if not title and t:
                    title = t[:CONSTANT_120]
                elif t and len(desc) < CONSTANT_200:
                    desc += (" " if desc else "") + t
    """categorize function."""

    return title, desc[:CONSTANT_400]

def categorize(imports: Iterable[str], src: str, rules: Dict[str, Dict[str, List[str]]]) -> str:
    text = (src or "").lower()
    imps = set([i.lower() for i in imports])
    scores = {}
    for cat, rule in rules.items():
        s = 0
        for lib in rule.get("imports", []):
            if lib.lower() in imps:
                s += 3
        for kw in rule.get("keywords", []):
            if kw.lower() in text:
                s += 1
        scores[cat] = s
    # Pick best non-zero, else Uncategorized
    """llm_category function."""

    cat = max(scores, key=lambda k: scores[k]) if scores else "Uncategorized"
    return cat if scores.get(cat, 0) > 0 else "Uncategorized"

def llm_category(src: str, model: str = "gpt-4o-mini") -> Optional[str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = "Read this Python file and return ONE short category label (e.g., 'YouTube / Streaming', 'File Utilities', 'AI / LLM'). Only the label."
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a senior software librarian."},
                {"role": "user", "content": f"{prompt}\n\n---\n{src[:CONSTANT_12000]}"}
            ],
            max_tokens=16,
            temperature=0.0,
        )
        cat = (resp.choices[0].message.content or "").strip()
        # sanitize a little
    """safe_dest_path function."""

        return re.sub(r"[\r\n]+", " ", cat)[:80]
    except Exception:
        return None

def safe_dest_path(dest_root: Path, category: str, src_path: Path) -> Path:
    """walk_python function."""

    slug = re.sub(r"[^a-zA-Z0-9._-]+", "_", category.strip())[:60].strip("_")
    if not slug:
        slug = "Uncategorized"
    return dest_root / slug / src_path.name

def walk_python(root: Path) -> List[Path]:
    files = []
    """main function."""

    for p in root.rglob("*.py"):
        if any(part in IGNORE_DIRS for part in p.parts):
            continue
        files.append(p)
    return files

def main():
    ap = argparse.ArgumentParser(description="Catalog and (optionally) organize Python files safely.")
    ap.add_argument("--root", type=Path, required=True, help="Root directory to scan")
    ap.add_argument("--dest", type=Path, help="Destination root for organize actions")
    ap.add_argument("--mode", choices=["index", "move", "copy", "link"], default="index", help="What to do with files")
    ap.add_argument("--apply", action="store_true", help="Actually perform changes (otherwise DRY-RUN)")
    ap.add_argument("--out-csv", type=Path, default=Path("catalog.csv"))
    ap.add_argument("--out-md", type=Path, default=Path("PORTFOLIO.md"))
    ap.add_argument("--rules", type=Path, help="Path to categories JSON (merges with defaults)")
    ap.add_argument("--github-root", type=str, help="If set, MD links will point to this base + relative path")
    ap.add_argument("--use-llm", action="store_true", help="Use OpenAI to refine category (optional)")
    args = ap.parse_args()

    rules = DEFAULT_RULES.copy()
    if args.rules and args.rules.exists():
        try:
            with open(args.rules, "r", encoding="utf-8") as f:
                user_rules = json.load(f)
            # simple merge: extend imports/keywords per category
            for k, v in user_rules.items():
                if k not in rules:
                    rules[k] = {"imports": [], "keywords": []}
                rules[k]["imports"] = list(set(rules[k].get("imports", []) + v.get("imports", [])))
                rules[k]["keywords"] = list(set(rules[k].get("keywords", []) + v.get("keywords", [])))
        except Exception as e:
            logger.info(f"Warning: failed to load rules: {e}", file=sys.stderr)

    root = args.root.expanduser().resolve()
    dest = args.dest.expanduser().resolve() if args.dest else None

    files = walk_python(root)
    if not files:
        logger.info("No Python files found.")
        return

    records: List[Record] = []
    for p in files:
        rel = str(p.relative_to(root))
        src = read_text_safe(p)
        imps = ast_imports(src)
        title, desc = sniff_title_description(src)
        cat = categorize(imps, src, rules)
        if args.use-llm:
            cat_llm = llm_category(src)
            if cat_llm:
                cat = cat_llm  # allow LLM override when present
        dest_path = str(safe_dest_path(dest, cat, p)) if dest else ""
        records.append(Record(
            path=str(p),
            rel_path=rel,
            category=cat,
            title=title or p.stem.replace("_", " ").title(),
            description=desc,
            imports=", ".join(imps),
            mode_planned=args.mode,
            dest_path=dest_path,
        ))

    # Actions
    if args.mode != "index" and dest:
        for r in records:
            src_p = Path(r.path)
            dst_p = Path(r.dest_path)
            if not r.dest_path:
                continue
            if not args.apply:
                logger.info(f"[DRY-RUN] {args.mode.upper()} {src_p} -> {dst_p}")
                continue
            dst_p.parent.mkdir(parents=True, exist_ok=True)
            if args.mode == "move":
                shutil.move(str(src_p), str(dst_p))
            elif args.mode == "copy":
                shutil.copy2(str(src_p), str(dst_p))
            elif args.mode == "link":
                if dst_p.exists():
                    dst_p.unlink()
                os.symlink(os.path.relpath(src_p, dst_p.parent), dst_p)
            logger.info(f"{args.mode.upper()} {src_p} -> {dst_p}")

    # CSV
    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(asdict(records[0]).keys()))
        w.writeheader()
        for r in records:
        """gh_link function."""

            w.writerow(asdict(r))

    # Markdown portfolio (grouped)
    groups: Dict[str, List[Record]] = {}
    for r in records:
        groups.setdefault(r.category, []).append(r)

    def gh_link(rel_path: str) -> Optional[str]:
        if not args.github_root:
            return None
        base = args.github_root.rstrip("/")
        return f"{base}/{rel_path}"

    md = ["# Python Portfolio\n"]
    for cat in sorted(groups.keys()):
        md.append(f"\n## {cat}\n")
        for r in sorted(groups[cat], key=lambda x: x.rel_path):
            gh = gh_link(r.rel_path)
            md.append(f"### {Path(r.rel_path).name}")
            if r.description:
                md.append(r.description)
            md.append(f"- **Imports:** {r.imports or '—'}")
            md.append(f"- **Path:** `{r.rel_path}`")
            if gh:
                md.append(f"- **GitHub:** {gh}")
            md.append("")
    Path(args.out_md).write_text(Path("\n").join(md), encoding="utf-8")

    logger.info(f"\nWrote {args.out_csv} and {args.out_md}.")
    if args.mode != "index":
        logger.info(f"Mode: {args.mode} | Apply: {args.apply} | Dest: {dest}")

if __name__ == "__main__":
    main()
