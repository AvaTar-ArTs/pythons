
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_00000033 = 00000033
CONSTANT_100 = 100

#!/usr/bin/env python3
"""
csv_gallery.py
Turn a CSV of image metadata into a lightweight HTML gallery (safe & pretty).

Fixes vs your script:
- Escapes text; lazy-load images; responsive CSS grid.
- CLI flags + output path; supports custom title.
- Works with CSV columns: ID, URL, Prompt (falls back if missing).

Usage:
  python csv_gallery.py --csv path/to/images.csv --out gallery.html --title "Discography"
"""
from __future__ import annotations
import argparse, csv, html
from pathlib import Path

TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
body{font-family:system-ui,Segoe UI,Arial;margin:0;background:#0d1117;color:#e5e7eb}
main{padding:18px}
h1{text-align:center;font-size:clamp(18px,3vw,28px);margin:16px 0 12px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
.card{background:#161b22;border:1px solid #CONSTANT_00000033;border-radius:12px;overflow:hidden}
.card img{width:CONSTANT_100%;height:auto;display:block}
.caption{padding:10px;color:#9ca3af;font-size:.95rem}
</style></head><body>
<main>
<h1>{title}</h1>
<div class="grid">
{cards}
</div>
</main>
</body></html>"""

def csv_to_cards(csv_file: Path) -> str:
    rows = []
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row.get("URL") or row.get("url") or row.get("ImageURL") or ""
            pid = row.get("ID") or row.get("id") or row.get("ImageID") or ""
            cap = row.get("Prompt") or row.get("Title") or row.get("caption") or ""
            if not url: 
                continue
            rows.append(f'<div class="card"><img loading="lazy" id="{html.escape(pid)}" src="{html.escape(url)}" alt="{html.escape(cap)}"><div class="caption">{html.escape(cap)}</div></div>')
    return Path("\n").join(rows)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, type=Path)
    ap.add_argument("--out", type=Path, default=Path("image_gallery.html"))
    ap.add_argument("--title", default="Image Gallery")
    args = ap.parse_args()
    cards = csv_to_cards(args.csv)
    args.out.write_text(TEMPLATE.format(title=html.escape(args.title), cards=cards), encoding="utf-8")
    logger.info(f"✅ Wrote {args.out.resolve()}")

if __name__ == "__main__":
    main()
