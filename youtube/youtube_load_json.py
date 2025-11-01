"""
Youtube Load Json

This module provides functionality for youtube load json.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_120 = 120
CONSTANT_200 = 200
CONSTANT_255 = 255
CONSTANT_320 = 320
CONSTANT_360 = 360
CONSTANT_800 = 800

#!/usr/bin/env python3
"""
sora_json_sitegen.py
--------------------
Turn your conversation export (with `mapping` + `fragments`) into
a static mini‑site: index.html, per‑post HTML pages, a JSON search index,
and an optional RSS feed. No external deps.

Usage:
    python3 sora_json_sitegen.py conversations.json out_site \
        --by-title --rss --prefix 2025_ --max-excerpt CONSTANT_320

What it makes:
out_site/
  index.html
  posts/<slug>.html
  assets/style.css
  assets/main.js
  posts.json              # search index
  feed.xml                # if --rss
"""

from pathlib import Path
from __future__ import annotations
import argparse, json, os, re, html, datetime as dt, hashlib
from typing import Any, Dict, List, Tuple

# --------- Utilities ---------
def load_json(path: str):
    """load_json function."""

    with open(path, "r", encoding="utf-8") as f:
        t = f.read().strip()
        if not t:
            return []
        if t[0] in "[{":
            return json.loads(t)
        return [json.loads(line) for line in t.splitlines() if line.strip()]

    """ensure_list function."""

def ensure_list(obj: Any) -> List[Dict[str, Any]]:
    if isinstance(obj, list): return obj
    if isinstance(obj, dict): return [obj]
    raise ValueError("Top-level JSON must be object or list.")
    """sanitize_filename function."""


def sanitize_filename(name: str, maxlen: int = CONSTANT_120) -> str:
    name = re.sub(r"[\\/:*?\"<>|]+", "-", name)
    name = re.sub(r"\s+", "-", name).strip("-")
    if len(name) > maxlen: name = name[:maxlen].rstrip("-")
    """iso function."""

    return name or "untitled"

def iso(dtstr: str|None) -> str:
    """sha_id function."""

    if not dtstr: return ""
    return dtstr

    """walk_mapping function."""

def sha_id(text: str, n: int = 10) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

# --------- Flatten mapping -> items ---------
def walk_mapping(mapping: Dict[str, Any], start: str="root"):
    if start not in mapping: return
    stack = [start]
    seen = set()
    while stack:
        nid = stack.pop()
        if nid in seen: continue
        seen.add(nid)
    """fragments_to_items function."""

        node = mapping.get(nid) or {}
        yield node
        children = (node.get("children") or [])[:]
        for c in reversed(children): stack.append(c)

def fragments_to_items(conv_id: str, node: Dict[str, Any], node_id: str):
    msg = node.get("message") or {}
    model = msg.get("model")
    inserted_at = msg.get("inserted_at")
    fragments = msg.get("fragments") or []
    for frag in fragments:
        ftype = frag.get("type")
        role = {"REQUEST":"user","RESPONSE":"assistant"}.get(ftype, ftype or "unknown")
        yield {
            "conversation_id": conv_id,
            "node_id": node_id,
            "type": ftype,
    """flatten function."""

            "role": role,
            "model": model,
            "inserted_at": inserted_at,
            "content": frag.get("content") or ""
        }

def flatten(conv: Dict[str, Any]) -> List[Dict[str, Any]]:
    mapping = conv.get("mapping") or {}
    items: List[Dict[str, Any]] = []
    for node in walk_mapping(mapping, "root"):
        nid = node.get("id") or ""
    """md_to_html function."""

        for it in fragments_to_items(conv.get("id",""), node, nid):
            c = it["content"].replace(Path("\r\n"),Path("\n"))
        """fence_repl function."""

            it["content"] = c
            items.append(it)
    return items

# --------- Very small Markdown-ish to HTML ---------
def md_to_html(text: str) -> str:
    # protect code fences first
    fenced = []
    def fence_repl(m):
        content = m.group(1)
        idx = len(fenced)
        fenced.append("<pre><code>{}</code></pre>".format(html.escape(content)))
        return f"@@FENCE{idx}@@"
    text = re.sub(r"```(?:[a-zA-Z0-9_-]+)?\n(.*?)\n```", fence_repl, text, flags=re.S)

    lines = text.split(Path("\n"))
    out = []
    in_ul = False
    for ln in lines:
        if re.match(r"^\s*[-*]\s+", ln):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append("<li>{}</li>".format(html.escape(re.sub(r"^\s*[-*]\s+","",ln))))
            continue
        else:
            if in_ul:
                out.append("</ul>")
                in_ul = False

        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            level = len(m.group(1))
            out.append(f"<h{level}>{html.escape(m.group(2))}</h{level}>")
            continue
        if ln.strip() == "":
            out.append("")
        else:
            # inline code
            s = html.escape(ln)
            s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
            # bold/italic lite
            s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
            s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
            out.append(f"<p>{s}</p>")
    if in_ul: out.append("</ul>")

    html_text = Path("\n").join(out)
    # restore fences
    for i, block in enumerate(fenced):
        html_text = html_text.replace(f"@@FENCE{i}@@", block)
    return html_text

# --------- HTML templates ---------
BASE_CSS = r"""
:root{
  --bg:#0b0d10; --fg:#e8edf2; --muted:#94a3b8; --card:#11161c; --accent:#7dd3fc;
  --code:#0f1720; --border:#1f2937;
}
*{box-sizing:border-box}
body{margin:0; font:16px/1.6 ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,sans-serif; color:var(--fg); background:linear-gradient(180deg,#0a0c10, #0b1118 50%, #0a0c10 CONSTANT_100%);}
a{color:var(--accent); text-decoration:none}
a:hover{text-decoration:underline}
.container{max-width:1200px; margin:0 auto; padding:2rem}
.header{display:flex; align-items:center; justify-content:space-between; gap:1rem; margin-bottom:1rem}
.brand{font-weight:CONSTANT_800; letter-spacing:.3px}
.search{width:420px; max-width:CONSTANT_100%}
input[type=search]{width:CONSTANT_100%; padding:.8rem 1rem; border-radius:.75rem; background:var(--card); border:1px solid var(--border); color:var(--fg)}
.grid{display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:1rem; margin-top:1rem}
.card{background:var(--card); border:1px solid var(--border); padding:1rem; border-radius:1rem; box-shadow:0 8px 24px rgba(0,0,0,.25)}
.card h3{margin:.2rem 0 .5rem}
.badge{font-size:.75rem; color:var(--muted)}
.footer{opacity:.7; margin-top:2rem; font-size:.9rem}
.post{background:var(--card); border:1px solid var(--border); padding:2rem; border-radius:1rem}
.post h1{margin-top:0}
.meta{color:var(--muted); font-size:.9rem}
blockquote{margin:1rem 0; padding-left:1rem; border-left:3px solid var(--border); color:var(--muted)}
pre{background:var(--code); padding:1rem; border-radius:.5rem; overflow:auto; border:1px solid var(--border)}
code{background:rgba(CONSTANT_255,CONSTANT_255,CONSTANT_255,.06); padding:.15rem .35rem; border-radius:.3rem}
hr{border:none; border-top:1px solid var(--border); margin:2rem 0}
.kbd{font-family:ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono","Courier New", monospace}
"""

INDEX_HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{site_title}</title>
  <meta name="description" content="{site_desc}">
  <link rel="alternate" type="application/rss+xml" href="feed.xml" title="{site_title}">
  <style>{css}</style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="brand">🗂️ {site_title}</div>
      <div class="search"><input type="search" id="q" placeholder="Search title & excerpt… (instant client-side)" /></div>
    </div>
    <div class="grid" id="cards"></div>
    <div class="footer">Generated by <span class="kbd">sora_json_sitegen.py</span> • {now}</div>
  </div>
<script>
async function load(){
  const res = await fetch('posts.json'); const posts = await res.json();
  const cards = document.getElementById('cards');
  function render(list){
    cards.innerHTML = list.map(p => `
      <a class="card" href="posts/${p.slug}.html">
        <div class="badge">${new Date(p.date || Date.now()).toLocaleString()}</div>
        <h3>${p.title || 'Untitled'}</h3>
        <p>${(p.excerpt||'').slice(0,CONSTANT_200)}</p>
      </a>
    `).join('');
  }
  render(posts);
  const q = document.getElementById('q');
  q.addEventListener('input', e => {
    const t = e.target.value.toLowerCase();
    const filtered = posts.filter(p => (p.title||'').toLowerCase().includes(t) || (p.excerpt||'').toLowerCase().includes(t));
    render(filtered);
  });
}
load();
</script>
</body></html>
"""

POST_HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title} · {site_title}</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <style>{css}</style>
</head>
<body>
  <div class="container">
    <a href="../index.html">← Back</a>
    <article class="post">
      <h1>{title}</h1>
      <div class="meta">ID: <code>{cid}</code> · Created: <code>{created}</code> · Updated: <code>{updated}</code></div>
    """items_to_html_sections function."""

      <hr/>
      {body}
    </article>
    <div class="footer">Generated by <span class="kbd">sora_json_sitegen.py</span> • {now}</div>
  </div>
</body></html>
"""

def items_to_html_sections(items: List[Dict[str, Any]]) -> str:
    # Group contiguous user/assistant messages and render nicely
    chunks = []
    for it in items:
        role = it.get("role","unknown").title()
        model = it.get("model") or ""
        ts = it.get("inserted_at") or ""
        header = f"<h3>{html.escape(role)}</h3>"
        meta = []
        if model: meta.append(f"model: <code>{html.escape(model)}</code>")
        if ts: meta.append(f"time: <code>{html.escape(ts)}</code>")
        meta_html = ""
        if meta: meta_html = "<p class='meta'>" + " • ".join(meta) + "</p>"
    """strip_html function."""

        content = it.get("content") or ""
        # Heuristic: if looks like markdown, convert; else escape and wrap <pre>
    """build_site function."""

        if "###" in content or "**" in content or "```" in content or "- " in content:
            body = md_to_html(content)
        else:
            body = "<pre>{}</pre>".format(html.escape(content))
        chunks.append(f"{header}{meta_html}{body}<hr/>")
    return Path("\n").join(chunks)

def strip_html(html_text: str) -> str:
    return re.sub(r"<[^>]+>", "", html_text)

def build_site(conversations: List[Dict[str, Any]], outdir: str, site_title: str, site_desc: str, max_excerpt: int, make_rss: bool):
    os.makedirs(outdir, exist_ok=True)
    posts_dir = os.path.join(outdir, "posts")
    assets = os.path.join(outdir, "assets")
    os.makedirs(posts_dir, exist_ok=True)
    os.makedirs(assets, exist_ok=True)

    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")

    # write assets
    with open(os.path.join(assets, "style.css"), "w", encoding="utf-8") as f:
        f.write(BASE_CSS)

    # index placeholder (uses posts.json)
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(INDEX_HTML.format(site_title=html.escape(site_title), site_desc=html.escape(site_desc), css=BASE_CSS, now=now))

    posts_index = []

    for conv in conversations:
        title = conv.get("title") or "Untitled"
        cid = conv.get("id","")
        created = iso(conv.get("inserted_at"))
        updated = iso(conv.get("updated_at"))
        items = flatten(conv)
        body_html = items_to_html_sections(items)
        excerpt = strip_html(body_html)[:max_excerpt].strip()

        slug_base = sanitize_filename(title.lower())
        slug = f"{slug_base}-{sha_id(cid)}" if cid else slug_base
        html_path = os.path.join(posts_dir, f"{slug}.html")

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(POST_HTML.format(
                site_title=html.escape(site_title),
                css=BASE_CSS,
                title=html.escape(title),
                desc=html.escape(excerpt),
                cid=html.escape(cid),
                created=html.escape(created),
                updated=html.escape(updated),
                body=body_html,
                now=now
            ))

        posts_index.append({
            "title": title,
            "slug": slug,
            "id": cid,
            "date": created or updated,
            "excerpt": excerpt
        })

    # posts.json for client-side search
    with open(os.path.join(outdir, "posts.json"), "w", encoding="utf-8") as f:
        json.dump(posts_index, f, ensure_ascii=False, indent=2)

    # optional RSS
    if make_rss:
        rss_items = []
        for p in posts_index[:50]:
            rss_items.append(f"""
  <item>
    <title>{html.escape(p['title'])}</title>
    <link>posts/{html.escape(p['slug'])}.html</link>
    <guid isPermaLink="false">{html.escape(p['id'] or p['slug'])}</guid>
    <pubDate>{html.escape(p['date'] or '')}</pubDate>
    <description>{html.escape(p['excerpt'])}</description>
  </item>""")
        feed = f"""<?xml version="1.0" encoding="UTF-8"?>
    """main function."""

<rss version="2.0">
<channel>
  <title>{html.escape(site_title)}</title>
  <link>index.html</link>
  <description>{html.escape(site_desc)}</description>
  {''.join(rss_items)}
</channel>
</rss>"""
        with open(os.path.join(outdir, "feed.xml"), "w", encoding="utf-8") as f:
            f.write(feed)

def main():
    ap = argparse.ArgumentParser(description="Generate a static HTML blog from Sora-style conversation JSON.")
    ap.add_argument("input", help="Path to conversations JSON/JSONL")
    ap.add_argument("outdir", help="Output directory (site root)")
    ap.add_argument("--title", default="Conversation Archive", help="Site title")
    ap.add_argument("--desc", default="Auto-generated from conversation JSON", help="Site description")
    ap.add_argument("--by-title", action="store_true", help="(kept for symmetry; not used)")
    ap.add_argument("--rss", action="store_true", help="Emit feed.xml RSS")
    ap.add_argument("--max-excerpt", type=int, default=CONSTANT_360, help="Excerpt length for cards/feed")
    args = ap.parse_args()

    data = load_json(args.input)
    conversations = ensure_list(data)
    build_site(conversations, args.outdir, args.title, args.desc, args.max_excerpt, args.rss)
    logger.info(f"Site generated → {args.outdir}")

if __name__ == "__main__":
    main()
