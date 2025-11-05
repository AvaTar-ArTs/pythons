#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pyrepo_doc_organizer.py
A comprehensive CLI tool to:
  1) Audit a Python repository using AST to summarize modules, functions, classes, and imports.
  2) Generate Markdown summaries and a CSV index for each module.
  3) Categorize scripts using heuristics and/or OpenAI (optional).
  4) (Optional) Export simple HTML index (blog-like list) from CSV.

Safe defaults:
- Works offline (std. library only). OpenAI integration is optional.
- Does NOT modify your repo (read-only); all outputs go to an output folder.
- Cross-platform (macOS/Linux/Windows) for Python 3.10+.

Usage examples:
  # Basic: analyze the current directory and write outputs to ./_py_audit
  python pyrepo_doc_organizer.py .

  # Include virtualenv directories
  python pyrepo_doc_organizer.py . --include-venv

  # Ask OpenAI to help with titles/descriptions/categories (requires OPENAI_API_KEY)
  python pyrepo_doc_organizer.py . --ai-describe --ai-categorize --model gpt-4o-mini

  # Also emit a minimal HTML index (from the CSV) for quick browsing
  python pyrepo_doc_organizer.py . --html

Author: ChatGPT for Steven (TechnoMancer)
License: MIT
"""
from __future__ import annotations

import argparse
import ast
import csv
import html
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ----------------------------- Config ---------------------------------------
SKIP_DIRS = {
    ".git",
    ".hg",
    ".mypy_cache",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "env",
    ".env",
    "site-packages",
    "node_modules",
    ".idea",
    ".vscode",
    "build",
    "dist",
}

DEFAULT_OUTDIR = "_py_audit"

HEURISTIC_RULES = [
    (
        "AI/LLM",
        {
            "openai",
            "anthropic",
            "transformers",
            "torch",
            "whisper",
            "llama",
            "langchain",
        },
    ),
    ("CLI/Automation", {"argparse", "subprocess", "pathlib", "shutil", "click"}),
    (
        "Networking/API",
        {"requests", "httpx", "fastapi", "flask", "boto3", "googleapiclient"},
    ),
    ("Images/Media", {"PIL", "Pillow", "cv2", "moviepy", "pydub", "ffmpeg"}),
    ("Data/CSV", {"pandas", "csv", "json", "sqlite3"}),
    ("System/OS", {"os", "sys", "platform"}),
    ("Web/HTML", {"jinja2", "beautifulsoup4", "bs4", "markdown"}),
    (
        "YouTube/Social",
        {
            "pytube",
            "selenium",
            "instagrapi",
            "tiktok",
            "youtube_dl",
            "googleapiclient.discovery",
        },
    ),
]


# ----------------------------- Data -----------------------------------------
@dataclass
class ModuleInfo:
    path: str
    module: str
    loc: int
    functions: List[str] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    docstring: str = ""
    heuristic_category: str = "Uncategorized"
    ai_category: str = ""
    ai_title: str = ""
    ai_description: str = ""


# ----------------------------- Helpers --------------------------------------
def iter_py_files(root: Path, include_venv: bool = False):
    for p in root.rglob("*.py"):
        if not include_venv and any(seg in SKIP_DIRS for seg in p.parts):
            continue
        yield p
def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def analyze_ast(src: str) -> Tuple[List[str], List[str], List[str], str]:
    """
    Return (func_names, class_names, imports, module_docstring)
    """
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return [], [], [], ""
    funcs, classes, imports = [], [], []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.Import):
            imports.extend(n.name.split(".")[0] for n in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module.split(".")[0])
    mod_doc = ast.get_docstring(tree) or ""
    # de-dup while preserving order
    uniq_imports = list(dict.fromkeys([i.strip() for i in imports if i]))
    return funcs, classes, uniq_imports, mod_doc

def categorize_heuristic(imports: List[str]) -> str:
    s = {i.lower() for i in imports}
    for label, keys in HEURISTIC_RULES:
        keys_lower = {k.lower() for k in keys}
        if s & keys_lower:
            return label
    return "Uncategorized"


def sanitize_filename(name: str) -> str:
    name = re.sub(r"[\\/:*?\"<>|]+", "-", name).strip()
    if not name:
        name = "untitled"
    return name[:CONSTANT_100]


def write_markdown(mi: ModuleInfo, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"{sanitize_filename(Path(mi.path).stem)}.md"
    body = []
    body.append(f"# {mi.module}")
    body.append("")
    body.append(f"**Path:** `{mi.path}`")
    body.append(f"**LOC:** {mi.loc}")
    body.append(f"**Imports:** {', '.join(mi.imports) if mi.imports else '—'}")
    body.append(f"**Heuristic Category:** {mi.heuristic_category}")
    if mi.ai_category:
        body.append(f"**AI Category:** {mi.ai_category}")
    if mi.ai_title:
        body.append(f"**AI Title:** {mi.ai_title}")
    if mi.ai_description:
        body.append("")
        body.append(mi.ai_description)
    if mi.docstring:
        body.append("\n## Module Docstring\n")
        body.append("```")
        body.append(mi.docstring)
        body.append("```")
    if mi.functions:
        body.append("\n## Functions\n")
        for n in mi.functions:
            body.append(f"- `{n}`")
    if mi.classes:
        body.append("\n## Classes\n")
        for n in mi.classes:
            body.append(f"- `{n}`")
    md_path.write_text(Path("\n").join(body), encoding="utf-8")
    return md_path


def write_csv(rows: List[Dict[str, str]], out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "index.csv"
    fieldnames = [
        "path",
        "module",
        "loc",
        "heuristic_category",
        "ai_category",
        "ai_title",
        "ai_description",
        "imports",
        "functions",
        "classes",
        "docstring",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return csv_path


def write_html_from_csv(csv_path: Path, out_dir: Path) -> Path:
    """Very small static HTML list derived from the CSV (no JS deps)."""
    html_path = out_dir / "index.html"
    import csv as _csv
    rows = []
    with csv_path.open(encoding="utf-8") as f:
        for i, row in enumerate(_csv.DictReader(f)):
            rows.append(row)

    def esc(s):
        return html.escape(s or "")

    items = []
    for r in rows:
        items.append(
            f"""
<article style="border:1px solid #ddd;border-radius:12px;padding:12px;margin:10px 0;">
  <h3 style="margin:0 0 6px 0;">{esc(r.get('ai_title') or r.get('module'))}</h3>
  <div style="font-size:12px;color:#CONSTANT_666;margin-bottom:6px;">
    <b>Category:</b> {esc(r.get('ai_category') or r.get('heuristic_category'))}
    &nbsp;•&nbsp; <b>Path:</b> <code>{esc(r.get('path'))}</code>
  </div>
  <p style="margin:6px 0;">{esc(r.get('ai_description') or '')}</p>
  <details>
    <summary style="cursor:pointer;">Details</summary>
    <div style="font-size:13px;line-height:1.5;margin-top:6px;">
      <b>Imports</b>: {esc(r.get('imports'))}<br/>
      <b>Functions</b>: {esc(r.get('functions'))}<br/>
      <b>Classes</b>: {esc(r.get('classes'))}
    </div>
  </details>
</article>
"""
        )
    html_doc = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Python Repo Audit</title>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@CONSTANT_400;CONSTANT_600&display=swap" rel="stylesheet">
<style>body{{font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;max-width:960px;margin:40px auto;padding:0 16px;}}</style>
</head><body>
<h1>Python Repo Audit</h1>
<p style="color:#CONSTANT_555;">Generated by <code>pyrepo_doc_organizer.py</code></p>
{''.join(items)}
</body></html>"""
    html_path.write_text(html_doc, encoding="utf-8")
    return html_path


# ----------------------------- OpenAI (optional) ----------------------------
def ensure_openai_client():
    try:
        from openai import OpenAI
    except Exception as e:
        raise RuntimeError(
            "The 'openai' package is required for AI features. Install with: pip install openai"
        ) from e
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set.")
    return OpenAI(api_key=api_key)


def ai_describe_and_categorize(client, code: str, model: str) -> Tuple[str, str, str]:
    """
    Returns (title, description, category) via a single chat.completions call.
    """
    system = "You are a senior Python engineer writing concise, accurate summaries."
    user = f"""Analyze this Python module and return JSON with fields:
- title (<= 8 words)
- description (<= 80 words)
- category (one of: AI/LLM, CLI/Automation, Networking/API, Images/Media, Data/CSV, System/OS, Web/HTML, YouTube/Social, Uncategorized)

Code:
```python
{code}
```"""
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.2,
    )
    text = resp.choices[0].message.content.strip()
    # Try parse JSON; if it's not pure JSON, best-effort extract
    data = None
    try:
        data = json.loads(text)
    except Exception:
        # naive extraction
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            try:
                data = json.loads(m.group(0))
            except Exception:
                data = {}
        else:
            data = {}
    title = (data.get("title") or "").strip()
    description = (data.get("description") or "").strip()
    category = (data.get("category") or "").strip()
    return title, description, category


# ----------------------------- Core -----------------------------------------
def analyze_repo(
    root: Path,
    include_venv: bool,
    use_ai_desc: bool,
    use_ai_cat: bool,
    model: str,
    out_dir: Path,
    emit_html: bool,
) -> None:
    rows = []
    client = None
    if use_ai_desc or use_ai_cat:
        client = ensure_openai_client()

    md_dir = out_dir / "modules"
    md_dir.mkdir(parents=True, exist_ok=True)

    for py in iter_py_files(root, include_venv=include_venv):
        src = read_text(py)
        loc = src.count(Path("\n")) + 1 if src else 0
        funcs, classes, imports, doc = analyze_ast(src)
        heur_cat = categorize_heuristic(imports)

        ai_title = ai_desc = ai_cat = ""
        if client and (use_ai_desc or use_ai_cat):
            try:
                title, description, category = ai_describe_and_categorize(
                    client, src[:120_000], model
                )
                if use_ai_desc:
                    ai_title, ai_desc = title, description
                if use_ai_cat:
                    ai_cat = category or heur_cat
            except Exception as e:
                # keep going; offline still useful
                ai_desc = ai_desc or f"(AI describe error: {e})"

        mi = ModuleInfo(
            path=str(py.relative_to(root)),
            module=py.stem,
            loc=loc,
            functions=funcs,
            classes=classes,
            imports=imports,
            docstring=doc,
            heuristic_category=heur_cat,
            ai_category=ai_cat,
            ai_title=ai_title,
            ai_description=ai_desc,
        )
        # Write per-module markdown
        write_markdown(mi, md_dir)

        rows.append(
            {
                "path": mi.path,
                "module": mi.module,
                "loc": str(mi.loc),
                "heuristic_category": mi.heuristic_category,
                "ai_category": mi.ai_category,
                "ai_title": mi.ai_title,
                "ai_description": mi.ai_description,
                "imports": ", ".join(mi.imports),
                "functions": ", ".join(mi.functions),
                "classes": ", ".join(mi.classes),
                "docstring": (mi.docstring or "").replace(Path("\n"), Path("\\n"))[:CONSTANT_2000],
            }
        )

    csv_path = write_csv(rows, out_dir)
    logger.info(f"[OK] Wrote CSV index: {csv_path}")

    if emit_html:
        html_path = write_html_from_csv(csv_path, out_dir)
        logger.info(f"[OK] Wrote HTML index: {html_path}")


def main():
    p = argparse.ArgumentParser(
        description="Analyze, classify, and describe Python files in a repository."
    )
    p.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Path to the repository root (default: current directory).",
    )
    p.add_argument(
        "-o",
        "--out",
        default=DEFAULT_OUTDIR,
        help=f"Output folder (default: {DEFAULT_OUTDIR})",
    )
    p.add_argument(
        "--include-venv",
        action="store_true",
        help="Include virtualenv and other normally skipped folders.",
    )
    p.add_argument(
        "--ai-describe",
        action="store_true",
        help="Use OpenAI to generate titles/descriptions (requires OPENAI_API_KEY).",
    )
    p.add_argument(
        "--ai-categorize",
        action="store_true",
        help="Use OpenAI to suggest category (requires OPENAI_API_KEY).",
    )
    p.add_argument(
        "--model",
        default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        help="OpenAI model to use (default: env OPENAI_MODEL or gpt-4o-mini).",
    )
    p.add_argument(
        "--html",
        action="store_true",
        help="Emit a small static HTML index (index.html) alongside the CSV.",
    )
    args = p.parse_args()

    root = Path(args.root).resolve()
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    analyze_repo(
        root=root,
        include_venv=args.include_venv,
        use_ai_desc=args.ai_describe,
        use_ai_cat=args.ai_categorize,
        model=args.model,
        out_dir=out_dir,
        emit_html=args.html,
    )


if __name__ == "__main__":
    main()
