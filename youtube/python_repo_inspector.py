"""
Python Repo Inspector

This module provides functionality for python repo inspector.

Author: Auto-generated
Date: 2025-11-01
"""

# Analyze the Python files you've uploaded here (a subset of your /Users/steven/Documents/python)
# and generate a compact report (CSV + simple HTML) along with an on-screen table.

import ast
import csv
import html
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple

import pandas as pd
from caas_jupyter_tools import display_dataframe_to_user

# Constants
CONSTANT_160 = 160
CONSTANT_555 = 555
CONSTANT_666 = 666


# Files visible in this workspace (mirror of some of your local files)
root = Path(Path("/Users/steven/Documents/python"))
py_files = sorted([p for p in root.iterdir() if p.suffix == ".py"])

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
        }),
    ("CLI/Automation", {"argparse", "subprocess", "pathlib", "shutil", "click"}),
    (
        "Networking/API",
        {"requests", "httpx", "fastapi", "flask", "boto3", "googleapiclient"}),
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
        }),
]


def analyze_ast(src: str) -> Tuple[List[str], List[str], List[str], str]:
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
    uniq_imports = list(dict.fromkeys([i.strip() for i in imports if i]))
    return funcs, classes, uniq_imports, mod_doc
def categorize_heuristic(imports: List[str]) -> str:
    s = {i.lower() for i in imports}
    for label, keys in HEURISTIC_RULES:
        if s & {k.lower() for k in keys}:
            return label
    return "Uncategorized"


rows = []
for p in py_files:
    try:
        src = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        src = ""
    loc = src.count(Path("\n")) + 1 if src else 0
    funcs, classes, imports, doc = analyze_ast(src)
    heur = categorize_heuristic(imports)
    rows.append(
        {
            "file": p.name,
            "path": str(p),
            "loc": loc,
            "heuristic_category": heur,
            "imports": ", ".join(imports),
            "functions": ", ".join(funcs[:20]) + (" …" if len(funcs) > 20 else ""),
            "classes": ", ".join(classes[:20]) + (" …" if len(classes) > 20 else ""),
            "docstring_preview": ((doc or "").strip().splitlines()[0][:CONSTANT_160] if doc else ""),
        }
    )

df = pd.DataFrame(rows).sort_values(["heuristic_category", "file"]).reset_index(drop=True)

# Save CSV and HTML
out_dir = Path(Path("/mnt/data/_mini_audit"))
out_dir.mkdir(exist_ok=True, parents=True)
csv_path = out_dir / "mini_index.csv"
html_path = out_dir / "mini_index.html"

df.to_csv(csv_path, index=False)
# simple HTML rendering
def esc(s):
    return html.escape(str(s) if s is not None else "")


items = []
for r in df.to_dict(orient="records"):
    items.append(
        f"""
<article style="border:1px solid #ddd;border-radius:12px;padding:12px;margin:10px 0;">
  <h3 style="margin:0 0 6px 0;">{esc(r['file'])}</h3>
  <div style="font-size:12px;color:#CONSTANT_666;margin-bottom:6px;">
    <b>Category:</b> {esc(r['heuristic_category'])}
    &nbsp;•&nbsp; <b>LOC:</b> {esc(r['loc'])}
    &nbsp;•&nbsp; <b>Imports:</b> {esc(r['imports'])}
  </div>
  <p style="margin:6px 0;"><b>Docstring:</b> {esc(r['docstring_preview'])}</p>
  <details>
    <summary style="cursor:pointer;">Functions / Classes</summary>
    <div style="font-size:13px;line-height:1.5;margin-top:6px;">
      <b>Functions</b>: {esc(r['functions'])}<br/>
      <b>Classes</b>: {esc(r['classes'])}<br/>
      <b>Path</b>: <code>{esc(r['path'])}</code>
    </div>
  </details>
</article>
"""
    )
html_doc = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Mini Python Audit</title>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<style>body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;max-width:960px;margin:40px auto;padding:0 16px;}}</style>
</head><body>
<h1>Mini Python Audit</h1>
<p style="color:#CONSTANT_555;">Files analyzed from the uploaded workspace.</p>
{''.join(items)}
</body></html>"""
html_path.write_text(html_doc, encoding="utf-8")

display_dataframe_to_user("Python files (uploaded subset) — analysis", df)

csv_path, html_path
