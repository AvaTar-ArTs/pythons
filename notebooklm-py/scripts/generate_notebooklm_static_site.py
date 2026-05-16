#!/usr/bin/env python3
"""Generate a static HTML mini-site for NotebookLM notebooks (Artifacts-first).

Writes a **new versioned build** under ``site/versions/<NNNN>/`` each run (0001, 0002, …)
without overwriting previous builds or legacy files at ``site/index.html`` etc.

Updates ``site/latest`` symlink to the newest build (macOS/Linux). Use ``site/latest/…``
in your hub links.

Paths to media/docs are relative so opening HTML via file:// works locally.

Usage:
  python3 scripts/generate_notebooklm_artifacts_site.py
"""

from __future__ import annotations

import html
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = ROOT / "site"
VERSIONS_ROOT = SITE_ROOT / "versions"

SKIP_DIR_NAMES = {".git", ".qwen", "site", "scripts"}


def next_build_id(versions_root: Path) -> str:
    """Return next zero-padded build id (e.g. 0007) based on existing numeric dirs."""
    versions_root.mkdir(parents=True, exist_ok=True)
    max_n = 0
    for p in versions_root.iterdir():
        if p.is_dir() and re.fullmatch(r"\d{4}", p.name):
            max_n = max(max_n, int(p.name))
    return f"{max_n + 1:04d}"


def update_latest_symlink(site_dir: Path, build_id: str) -> None:
    """Point site/latest at versions/NNNN (relative symlink)."""
    link = site_dir / "latest"
    target = Path("versions") / build_id
    if link.is_symlink():
        link.unlink()
    elif link.exists():
        if link.is_dir():
            print(
                f"Warning: {link} exists and is not a symlink; leaving it untouched. "
                "Remove or rename it to enable site/latest.",
                file=sys.stderr,
            )
            return
        link.unlink()
    try:
        link.symlink_to(target, target_is_directory=True)
    except OSError as e:
        print(f"Warning: could not create symlink {link} -> {target}: {e}", file=sys.stderr)


def write_versions_catalog(versions_root: Path, current_id: str) -> None:
    """Overwrite site/versions/index.html with links to all numeric builds."""
    rows: list[str] = []
    for p in sorted(versions_root.iterdir(), key=lambda x: x.name):
        if not p.is_dir() or not re.fullmatch(r"\d{4}", p.name):
            continue
        bid = p.name
        cur = " — latest" if bid == current_id else ""
        rows.append(
            f'<li class="ver-li"><span class="ver-id">{bid}</span>{cur} · '
            f'<a href="{bid}/index.html">grid</a> · '
            f'<a href="{bid}/index-compact.html">list</a></li>'
        )
    body = "\n".join(rows) if rows else "<li>No builds yet.</li>"
    catalog = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>NotebookLM — Build versions</title>
  <style>
    body {{ font-family: ui-monospace, monospace; background: #0a0a0c; color: #e8e6e3; padding: 2rem; }}
    a {{ color: #00ff9d; }}
    ul {{ list-style: none; padding: 0; }}
    li {{ margin: 0.5rem 0; }}
    .ver-id {{ color: #ffd700; }}
  </style>
</head>
<body>
  <h1>site/versions</h1>
  <p>Each run creates a new folder. <code>site/latest</code> points at the most recent build.</p>
  <ul>
{body}
  </ul>
</body>
</html>
"""
    write_text(versions_root / "index.html", catalog)

AUDIO_EXT = {".wav", ".mp3", ".m4a", ".aac", ".ogg", ".flac"}
VIDEO_EXT = {".mp4", ".webm", ".mov", ".mkv"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
TEXT_EXT = {".md", ".txt", ".csv", ".xml"}
JSON_EXT = {".json"}
HTML_EXT = {".html"}
PDF_EXT = {".pdf"}


def iter_notebook_dirs(only_names: set[str] | None = None) -> list[Path]:
    out: list[Path] = []
    for p in sorted(ROOT.iterdir(), key=lambda x: x.name.lower()):
        if not p.is_dir():
            continue
        if p.name.startswith("."):
            continue
        if p.name in SKIP_DIR_NAMES:
            continue
        if only_names is not None and p.name not in only_names:
            continue
        out.append(p)
    return out


def slugify(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s[:72] or "notebook"


def ensure_unique_slugs(names: list[str]) -> dict[str, str]:
    """Map folder name -> slug (add -2, -3 on collision)."""
    used: dict[str, int] = {}
    mapping: dict[str, str] = {}
    for name in names:
        base = slugify(name)
        n = used.get(base, 0)
        slug = base if n == 0 else f"{base}-{n+1}"
        used[base] = n + 1
        mapping[name] = slug
    return mapping


def normalize_pair_stem(stem: str) -> str:
    """Strip NotebookLM-style suffixes so 'Foo metadata' pairs with 'Foo'."""
    s = stem.strip()
    for suf in (
        " metadata",
        " metada",
        " metad",
        " me",
        " m",
    ):
        low = s.lower()
        if low.endswith(suf):
            s = s[: -len(suf)]
            break
    return s.strip()


def os_path_relpath(target: Path, start: Path) -> str:
    import os

    return os.path.relpath(target, start)


def read_json_meta(path: Path) -> dict | None:
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
        return json.loads(raw)
    except (OSError, json.JSONDecodeError):
        return None


def classify(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in AUDIO_EXT:
        return "audio"
    if ext in VIDEO_EXT:
        return "video"
    if ext in IMAGE_EXT:
        return "image"
    if ext in PDF_EXT:
        return "pdf"
    if ext in HTML_EXT:
        return "html"
    if ext in TEXT_EXT or ext in JSON_EXT or ext == "":
        return "text"
    return "other"


def walk_artifacts(artifacts_root: Path) -> list[Path]:
    if not artifacts_root.is_dir():
        return []
    files: list[Path] = []
    for p in artifacts_root.rglob("*"):
        if p.is_file():
            # Skip junk
            if p.name.startswith(".") or p.name == ".DS_Store":
                continue
            files.append(p)
    return sorted(files, key=lambda x: str(x).lower())


def group_episodes(files: list[Path], notebook_root: Path) -> list[dict]:
    """Group artifact files into 'episodes' by normalized stem within each parent folder."""
    by_key: dict[tuple[str, str], list[Path]] = defaultdict(list)
    for f in files:
        rel = f.relative_to(notebook_root)
        parent = str(rel.parent)
        stem = normalize_pair_stem(f.stem)
        key = (parent, stem)
        by_key[key].append(f)

    episodes: list[dict] = []
    for (parent, stem), group in sorted(by_key.items(), key=lambda x: (x[0][0], x[0][1].lower())):
        meta: dict | None = None
        meta_path: Path | None = None
        title = stem
        for f in group:
            if f.suffix.lower() == ".json":
                data = read_json_meta(f)
                if isinstance(data, dict) and data.get("title"):
                    meta = data
                    meta_path = f
                    title = str(data.get("title") or title)
                    break
        if meta is None:
            for f in group:
                if f.suffix.lower() == ".json":
                    data = read_json_meta(f)
                    if isinstance(data, dict):
                        meta = data
                        meta_path = f
                        title = str(data.get("title") or stem)
                        break

        episodes.append(
            {
                "title": title,
                "parent": parent,
                "stem": stem,
                "files": sorted(group, key=lambda p: str(p)),
                "meta": meta,
                "meta_path": meta_path,
            }
        )
    return episodes


def render_episode(page_path: Path, ep: dict) -> str:
    parts: list[str] = []
    eid = slugify(f'{ep["parent"]}/{ep["stem"]}')
    parts.append(f'<article class="episode" id="{html.escape(eid)}">')
    parts.append(f'<h3 class="episode-title">{html.escape(ep["title"])}</h3>')
    if ep["parent"] and ep["parent"] != ".":
        parts.append(
            f'<p class="muted path-hint">{html.escape(ep["parent"])}</p>'
        )

    # Media first
    for f in ep["files"]:
        kind = classify(f)
        rel = os_path_relpath(f, page_path.parent)
        u = html.escape(Path(rel).as_posix())
        name = html.escape(f.name)
        if kind == "audio":
            parts.append('<div class="media audio">')
            parts.append(f'<audio controls preload="metadata" src="{u}"></audio>')
            parts.append(f'<p class="muted"><a href="{u}">Open audio file ({name})</a></p>')
            parts.append("</div>")
        elif kind == "video":
            parts.append('<div class="media video">')
            parts.append(
                f'<video controls preload="metadata" src="{u}"></video>'
                f'<p class="muted"><a href="{u}">Open {name}</a></p>'
            )
            parts.append("</div>")
        elif kind == "image":
            parts.append('<div class="media image">')
            parts.append(f'<img loading="lazy" alt="{name}" src="{u}" />')
            parts.append(f'<p class="muted"><a href="{u}">{name}</a></p>')
            parts.append("</div>")
        elif kind == "pdf":
            parts.append('<div class="media pdf">')
            parts.append(
                f'<object data="{u}" type="application/pdf" class="pdf-frame">'
                f'<p><a href="{u}">Download PDF: {name}</a></p></object>'
            )
            parts.append("</div>")
        elif kind == "html":
            parts.append('<div class="media html">')
            parts.append(
                f'<p><a class="button" href="{u}">Open HTML: {name}</a></p>'
            )
            parts.append("</div>")

    # Text / json / md / remaining
    for f in ep["files"]:
        kind = classify(f)
        if kind in {"audio", "video", "image", "pdf", "html"}:
            continue
        rel = os_path_relpath(f, page_path.parent)
        u = html.escape(Path(rel).as_posix())
        name = html.escape(f.name)
        ext = f.suffix.lower()

        if ext == ".json" and f == ep.get("meta_path"):
            parts.append('<details class="json-meta"><summary>Artifact metadata (JSON)</summary>')
            raw = f.read_text(encoding="utf-8", errors="replace")
            parts.append(f'<pre class="code"><code>{html.escape(raw)}</code></pre>')
            parts.append("</details>")
        elif ext in {".md", ".txt", ".csv", ".xml"} or ext == "":
            try:
                raw = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                raw = ""
            if len(raw) > 120_000:
                raw = raw[:120_000] + "\n\n… (truncated for browser performance) …\n"
            parts.append(f'<details class="text-doc"><summary>{name}</summary>')
            parts.append(f'<pre class="code md"><code>{html.escape(raw)}</code></pre>')
            parts.append("</details>")
        elif ext == ".json":
            parts.append('<details class="json-meta"><summary>')
            parts.append(name)
            parts.append("</summary>")
            try:
                raw = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                raw = ""
            parts.append(f'<pre class="code"><code>{html.escape(raw)}</code></pre>')
            parts.append("</details>")
        else:
            parts.append(f'<p class="download"><a href="{u}">File: {name}</a></p>')

    parts.append("</article>")
    return "\n".join(parts)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def page_shell(
    title: str,
    body: str,
    back_href: str,
    back_label: str,
    body_class: str = "gptj page",
    extra_top_html: str = "",
) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#0a0a0c" />
  <title>{html.escape(title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="stylesheet" href="../styles.css" />
</head>
<body class="{html.escape(body_class)}">
  {extra_top_html}
  <header class="page-head">
    <p class="crumb"><a href="{html.escape(back_href)}">{html.escape(back_label)}</a></p>
    <h1 class="page-title">{html.escape(title)}</h1>
  </header>
  <main class="wrap">
{body}
  </main>
  <footer class="footer">
    <p class="footer-text">Generated locally from your NotebookLM export. Paths are relative for offline viewing.</p>
  </footer>
</body>
</html>
"""


def main() -> None:
    selected = [arg for arg in sys.argv[1:] if arg.strip()]
    only_names = set(selected) if selected else None
    notebook_dirs = iter_notebook_dirs(only_names=only_names)
    if only_names:
        matched = {p.name for p in notebook_dirs}
        missing = sorted(only_names - matched)
        if missing:
            print(
                "Warning: these requested notebook folders were not found and were skipped:\n"
                + "\n".join(f"  - {name}" for name in missing),
                file=sys.stderr,
            )
    if not notebook_dirs:
        print("No notebook folders selected. Nothing to build.", file=sys.stderr)
        sys.exit(1)
    names = [p.name for p in notebook_dirs]
    slug_map = ensure_unique_slugs(names)

    build_id = next_build_id(VERSIONS_ROOT)
    SITE = VERSIONS_ROOT / build_id
    PAGES = SITE / "notebooks"

    VERSIONS_ROOT.mkdir(parents=True, exist_ok=True)
    SITE.mkdir(parents=True, exist_ok=True)
    PAGES.mkdir(parents=True, exist_ok=True)

    index_rows: list[str] = []
    compact_rows: list[str] = []
    total_episodes = 0
    themes = ("ai", "biz", "creative")

    for i, nb in enumerate(notebook_dirs):
        name = nb.name
        slug = slug_map[name]
        artifacts = nb / "Artifacts"
        files = walk_artifacts(artifacts)
        episodes = group_episodes(files, nb) if files else []
        total_episodes += len(episodes)

        page_path = PAGES / f"{slug}.html"
        page_v2_path = PAGES / f"{slug}-v2.html"
        page_v3_path = PAGES / f"{slug}-v3.html"
        if episodes:
            body_parts = [
                '<p class="lede">Primary focus: <strong>Artifacts</strong> grouped into episodes (paired metadata + media where possible).</p>',
                '<section class="episode-grid">',
            ]
            for ep in episodes:
                body_parts.append(render_episode(page_path, ep))
            body_parts.append("</section>")
        else:
            body_parts = [
                "<p><strong>No <code>Artifacts</code> folder</strong> (or it is empty). "
                "This notebook may still have <code>Sources/</code>, notes, or chat exports.</p>"
            ]
            # Optional: surface notebook-level json
            for candidate in sorted(nb.glob("*.json")):
                rel = os_path_relpath(candidate, page_path.parent)
                u = html.escape(Path(rel).as_posix())
                body_parts.append(
                    f'<p class="notebook-meta"><a href="{u}">{html.escape(candidate.name)}</a></p>'
                )

        base_body = "\n".join(body_parts)
        notebook_variant_nav = (
            '<nav class="variant-nav" aria-label="Notebook page variants">'
            '<a href="../../../index.html">Hub</a>'
            '<span class="variant-sep" aria-hidden="true">·</span>'
            f'<span class="variant-current" aria-current="page">Notebook v1</span>'
            '<span class="variant-sep" aria-hidden="true">·</span>'
            f'<a href="{html.escape(page_v2_path.name)}">Notebook v2</a>'
            '<span class="variant-sep" aria-hidden="true">·</span>'
            f'<a href="{html.escape(page_v3_path.name)}">Notebook v3</a>'
            "</nav>"
        )
        notebook_variant_nav_v2 = (
            '<nav class="variant-nav" aria-label="Notebook page variants">'
            '<a href="../../../index.html">Hub</a>'
            '<span class="variant-sep" aria-hidden="true">·</span>'
            f'<a href="{html.escape(page_path.name)}">Notebook v1</a>'
            '<span class="variant-sep" aria-hidden="true">·</span>'
            f'<span class="variant-current" aria-current="page">Notebook v2</span>'
            '<span class="variant-sep" aria-hidden="true">·</span>'
            f'<a href="{html.escape(page_v3_path.name)}">Notebook v3</a>'
            "</nav>"
        )
        notebook_variant_nav_v3 = (
            '<nav class="variant-nav" aria-label="Notebook page variants">'
            '<a href="../../../index.html">Hub</a>'
            '<span class="variant-sep" aria-hidden="true">·</span>'
            f'<a href="{html.escape(page_path.name)}">Notebook v1</a>'
            '<span class="variant-sep" aria-hidden="true">·</span>'
            f'<a href="{html.escape(page_v2_path.name)}">Notebook v2</a>'
            '<span class="variant-sep" aria-hidden="true">·</span>'
            f'<span class="variant-current" aria-current="page">Notebook v3</span>'
            "</nav>"
        )

        write_text(
            page_path,
            page_shell(
                title=f"{name} — Artifacts",
                body=base_body,
                back_href="../index.html",
                back_label="All notebooks",
                body_class="gptj page page-v1",
                extra_top_html=notebook_variant_nav,
            ),
        )
        write_text(
            page_v2_path,
            page_shell(
                title=f"{name} — Artifacts (v2 compact)",
                body='<p class="lede">Variation 2: compact reading layout with tighter spacing for long scans.</p>\n'
                + base_body,
                back_href="../index.html",
                back_label="All notebooks",
                body_class="gptj page page-v2",
                extra_top_html=notebook_variant_nav_v2,
            ),
        )
        write_text(
            page_v3_path,
            page_shell(
                title=f"{name} — Artifacts (v3 showcase)",
                body='<p class="lede">Variation 3: showcase mode with larger visual hierarchy for media-heavy browsing.</p>\n'
                + base_body,
                back_href="../index.html",
                back_label="All notebooks",
                body_class="gptj page page-v3",
                extra_top_html=notebook_variant_nav_v3,
            ),
        )

        # Index card (single description line — no duplicate counts)
        href = f"notebooks/{slug}.html"
        acount = len(episodes)
        if acount:
            subtitle = (
                f"{acount} episode{'s' if acount != 1 else ''} · audio, video, JSON, and docs"
            )
        else:
            subtitle = "No Artifacts folder yet — Sources / chat may still exist"
        th = themes[i % len(themes)]
        search_val = html.escape(name.lower(), quote=True)
        index_rows.append(
            f'<a class="repo-card {th}" href="{html.escape(href)}" data-search="{search_val}">'
            f'<div class="card-name">{html.escape(name)}</div>'
            f'<div class="card-desc">{html.escape(subtitle)}</div>'
            f"</a>"
        )
        ep_label = f"{acount} ep." if acount else "—"
        compact_rows.append(
            f'<li class="dir-row" data-search="{search_val}">'
            f'<a class="dir-link" href="{html.escape(href)}">{html.escape(name)}</a>'
            f'<span class="dir-meta">{html.escape(ep_label)}</span>'
            f"</li>"
        )

    n_notebooks = len(notebook_dirs)
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#0a0a0c" />
  <title>NotebookLM — Artifacts</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="stylesheet" href="styles.css" />
</head>
<body class="gptj home">
  <nav class="variant-nav" aria-label="View variants">
    <a href="../../../index.html">Hub</a>
    <span class="variant-sep" aria-hidden="true">·</span>
    <span class="variant-current" aria-current="page">Grid</span>
    <span class="variant-sep" aria-hidden="true">·</span>
    <a href="index-compact.html">List</a>
  </nav>
  <header class="hero">
    <p class="terminal-prefix">notebooklm · build {build_id}</p>
    <h1 aria-label="NotebookLM Artifacts">
      <span class="brand-line">NotebookLM</span>
      <span class="junkie">Artifacts</span>
    </h1>
    <p class="hero-sub">Podcast-style index inspired by <a class="inline-link" href="https://gptjunkie.com/" rel="noopener noreferrer">gptjunkie.com</a>. Open a notebook to browse <strong>Artifacts</strong> as episodes (audio, video, docs).</p>
    <div class="stats-bar" role="presentation">
      <div class="stat">
        <div class="stat-num green">{n_notebooks}</div>
        <div class="stat-label">Notebooks</div>
      </div>
      <div class="stat">
        <div class="stat-num gold">{total_episodes}</div>
        <div class="stat-label">Artifact episodes</div>
      </div>
      <div class="stat">
        <div class="stat-num pink">3</div>
        <div class="stat-label">Accent themes</div>
      </div>
    </div>
    <p class="scroll-hint">Scroll to explore</p>
  </header>

  <section class="theme-section">
    <div class="section-header">
      <span class="section-num">01</span>
      <h2 class="section-title">Notebook index</h2>
      <span class="section-count">{n_notebooks} notebooks</span>
    </div>
    <div class="index-toolbar">
      <label class="sr-only" for="nb-search">Filter notebooks by name</label>
      <input type="search" id="nb-search" class="search-input" placeholder="Filter notebooks…" autocomplete="off" />
      <span class="filter-count" id="nb-filter-count" aria-live="polite"></span>
    </div>
    <div class="repo-grid" id="repo-grid">
{chr(10).join(index_rows)}
    </div>
  </section>

  <footer class="footer">
    <p class="footer-text">
      <a class="inline-link" href="index-compact.html">Compact list view</a>
      ·
      <a class="inline-link" href="../../../index.html">Export hub</a>
      ·
      New builds go to <code>site/versions/</code> (this is build <strong>{build_id}</strong>).
      Regenerate with <code>python3 scripts/generate_notebooklm_artifacts_site.py</code>
    </p>
  </footer>
  <script>
(function () {{
  var input = document.getElementById("nb-search");
  var grid = document.getElementById("repo-grid");
  var countEl = document.getElementById("nb-filter-count");
  if (!input || !grid) return;
  var cards = grid.querySelectorAll("a.repo-card");
  function apply() {{
    var q = (input.value || "").trim().toLowerCase();
    var n = 0;
    for (var i = 0; i < cards.length; i++) {{
      var a = cards[i];
      var hay = (a.getAttribute("data-search") || "").toLowerCase();
      var show = !q || hay.indexOf(q) !== -1;
      a.style.display = show ? "" : "none";
      if (show) n++;
    }}
    if (countEl) {{
      if (!q) countEl.textContent = "";
      else countEl.textContent = n + (n === 1 ? " match" : " matches");
    }}
  }}
  input.addEventListener("input", apply);
  input.addEventListener("search", apply);
}})();
  </script>
</body>
</html>
"""
    write_text(SITE / "index.html", index_html)

    index_compact_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#0a0a0c" />
  <title>NotebookLM — Compact index</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="stylesheet" href="styles.css" />
</head>
<body class="gptj compact-variant">
  <nav class="variant-nav" aria-label="View variants">
    <a href="../../../index.html">Hub</a>
    <span class="variant-sep" aria-hidden="true">·</span>
    <a href="index.html">Grid</a>
    <span class="variant-sep" aria-hidden="true">·</span>
    <span class="variant-current" aria-current="page">List</span>
  </nav>

  <header class="hero hero-compact">
    <p class="terminal-prefix">notebooklm · build {build_id} · list</p>
    <h1 aria-label="NotebookLM compact index">
      <span class="brand-line">NotebookLM</span>
      <span class="junkie">List</span>
    </h1>
    <p class="hero-sub">Dense directory view — same links as the grid, faster to scan. <strong>{n_notebooks}</strong> notebooks · <strong>{total_episodes}</strong> artifact episodes.</p>
  </header>

  <section class="theme-section compact-section">
    <div class="section-header">
      <span class="section-num">03</span>
      <h2 class="section-title">Notebook directory</h2>
      <span class="section-count">{n_notebooks} notebooks</span>
    </div>
    <div class="index-toolbar">
      <label class="sr-only" for="nb-search-compact">Filter notebooks by name</label>
      <input type="search" id="nb-search-compact" class="search-input" placeholder="Filter notebooks…" autocomplete="off" />
      <span class="filter-count" id="nb-filter-count-compact" aria-live="polite"></span>
    </div>
    <ol class="compact-list" id="compact-list">
{chr(10).join(compact_rows)}
    </ol>
  </section>

  <footer class="footer">
    <p class="footer-text">Build <strong>{build_id}</strong> · Regenerate with <code>python3 scripts/generate_notebooklm_artifacts_site.py</code></p>
  </footer>
  <script>
(function () {{
  var input = document.getElementById("nb-search-compact");
  var list = document.getElementById("compact-list");
  var countEl = document.getElementById("nb-filter-count-compact");
  if (!input || !list) return;
  var rows = list.querySelectorAll("li.dir-row");
  function apply() {{
    var q = (input.value || "").trim().toLowerCase();
    var n = 0;
    for (var i = 0; i < rows.length; i++) {{
      var row = rows[i];
      var hay = (row.getAttribute("data-search") || "").toLowerCase();
      var show = !q || hay.indexOf(q) !== -1;
      row.style.display = show ? "" : "none";
      if (show) n++;
    }}
    if (countEl) {{
      if (!q) countEl.textContent = "";
      else countEl.textContent = n + (n === 1 ? " match" : " matches");
    }}
  }}
  input.addEventListener("input", apply);
  input.addEventListener("search", apply);
}})();
  </script>
</body>
</html>
"""
    write_text(SITE / "index-compact.html", index_compact_html)

    css = """/* NotebookLM static site — visual language aligned with https://gptjunkie.com/ */
@import url("https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&family=IBM+Plex+Mono:wght@300;400&display=swap");

*, *::before, *::after { box-sizing: border-box; }

:root {
  color-scheme: dark;
  --bg: #0a0a0c;
  --surface: #111115;
  --surface-hover: #16161b;
  --border: #1e1e24;
  --text: #e8e6e3;
  --text-dim: #7a7874;
  --accent-ai: #00ff9d;
  --accent-biz: #ffd700;
  --accent-creative: #ff6bcb;
  --mono: "Space Mono", ui-monospace, monospace;
  --display: "Syne", system-ui, sans-serif;
  --body-mono: "IBM Plex Mono", ui-monospace, monospace;
}

html { scroll-behavior: smooth; }

body.gptj {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: var(--body-mono);
  line-height: 1.6;
  overflow-x: hidden;
}

/* Scanline overlay (gptjunkie.com) */
body.gptj::after {
  content: "";
  position: fixed;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0, 0, 0, 0.03) 2px,
    rgba(0, 0, 0, 0.03) 4px
  );
  pointer-events: none;
  z-index: 9999;
}

/* --- Home hero --- */
body.home .hero {
  min-height: 72vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  padding: 2rem;
  border-bottom: 1px solid var(--border);
}

body.home .hero::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 60% 40% at 20% 80%, rgba(0, 255, 157, 0.07), transparent),
    radial-gradient(ellipse 50% 50% at 80% 20%, rgba(255, 107, 203, 0.07), transparent),
    radial-gradient(ellipse 40% 30% at 50% 50%, rgba(255, 215, 0, 0.05), transparent);
  pointer-events: none;
}

.terminal-prefix {
  font-family: var(--mono);
  font-size: 0.75rem;
  color: var(--accent-ai);
  letter-spacing: 0.15em;
  text-transform: uppercase;
  margin-bottom: 1.5rem;
}

.terminal-prefix::before {
  content: "$ ";
  opacity: 0.5;
}

body.home .hero h1 {
  font-family: var(--display);
  font-size: clamp(2.2rem, 8vw, 5rem);
  font-weight: 800;
  letter-spacing: -0.04em;
  line-height: 0.95;
  text-align: center;
  margin: 0;
}

.brand-line {
  display: block;
  color: var(--text);
}

.junkie {
  display: block;
  background: linear-gradient(135deg, var(--accent-ai), var(--accent-biz), var(--accent-creative));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-sub {
  font-family: var(--body-mono);
  font-size: 0.9rem;
  color: var(--text-dim);
  margin-top: 2rem;
  text-align: center;
  max-width: 520px;
}

.hero-sub strong { color: var(--text); }

.inline-link {
  color: var(--accent-ai);
  text-decoration: none;
  border-bottom: 1px solid rgba(0, 255, 157, 0.35);
}

.inline-link:hover {
  color: var(--text);
  border-bottom-color: var(--text-dim);
}

.stats-bar {
  display: flex;
  justify-content: center;
  gap: 3rem;
  margin-top: 3rem;
  flex-wrap: wrap;
}

.stat { text-align: center; }

.stat-num {
  font-family: var(--display);
  font-size: 2rem;
  font-weight: 700;
}

.stat-num.green { color: var(--accent-ai); }
.stat-num.gold { color: var(--accent-biz); }
.stat-num.pink { color: var(--accent-creative); }
.stat-num.white { color: var(--text); }

.stat-label {
  font-size: 0.65rem;
  color: var(--text-dim);
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-top: 0.25rem;
}

.scroll-hint {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.7rem;
  color: var(--text-dim);
  letter-spacing: 0.2em;
  text-transform: uppercase;
}

/* --- Index section + repo grid --- */
.theme-section {
  padding: 3rem 1.5rem 4rem;
  max-width: 1200px;
  margin: 0 auto;
  border-bottom: 1px solid var(--border);
}

.section-header {
  display: flex;
  align-items: baseline;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.section-num {
  font-family: var(--display);
  font-size: 0.8rem;
  color: var(--text-dim);
}

.section-title {
  font-family: var(--display);
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
  color: var(--text);
}

.section-count {
  font-family: var(--mono);
  font-size: 0.7rem;
  color: var(--text-dim);
  margin-left: auto;
}

.index-toolbar {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1.25rem;
}

.search-input {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  font-family: var(--body-mono);
  font-size: 0.75rem;
  padding: 0.55rem 0.85rem;
  min-width: 220px;
  max-width: 100%;
  outline: none;
  transition: border-color 0.2s;
  border-radius: 2px;
}

.search-input:focus {
  border-color: var(--accent-ai);
}

.search-input::placeholder {
  color: var(--text-dim);
}

.filter-count {
  font-family: var(--mono);
  font-size: 0.65rem;
  color: var(--accent-ai);
  letter-spacing: 0.06em;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.repo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
}

a.repo-card {
  background: var(--surface);
  padding: 1.5rem;
  transition: background 0.3s;
  position: relative;
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  display: block;
}

.repo-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 3px;
  height: 100%;
  background: var(--card-accent, var(--text-dim));
  opacity: 0;
  transition: opacity 0.3s;
}

.repo-card:hover::before { opacity: 1; }
.repo-card:hover { background: var(--surface-hover); }

.repo-card.ai { --card-accent: var(--accent-ai); }
.repo-card.biz { --card-accent: var(--accent-biz); }
.repo-card.creative { --card-accent: var(--accent-creative); }

.card-name {
  font-family: var(--display);
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: var(--text);
}

.card-desc {
  font-size: 0.75rem;
  color: var(--text-dim);
  line-height: 1.5;
  margin-bottom: 0.75rem;
}

.card-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.6rem;
  color: var(--text-dim);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.card-files { color: var(--card-accent, var(--text-dim)); }

/* --- Inner pages --- */
.page-head {
  padding: 2rem 1.5rem 1rem;
  max-width: 1200px;
  margin: 0 auto;
  border-bottom: 1px solid var(--border);
}

.page-title {
  font-family: var(--display);
  font-size: clamp(1.4rem, 4vw, 2.2rem);
  font-weight: 800;
  letter-spacing: -0.03em;
  margin: 0.5rem 0 0;
  line-height: 1.1;
}

.crumb a {
  font-family: var(--mono);
  font-size: 0.7rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent-ai);
  text-decoration: none;
}

.crumb a:hover { color: var(--text); }

.wrap {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem 1.5rem 3rem;
}

.lede {
  font-size: 0.9rem;
  color: var(--text-dim);
  max-width: 80ch;
  margin-bottom: 1.25rem;
}

.lede strong { color: var(--text); }

.episode-grid {
  display: grid;
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
  margin-top: 0.5rem;
}

.episode {
  background: var(--surface);
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
}

.episode:nth-child(3n + 1) { --ep-accent: var(--accent-ai); }
.episode:nth-child(3n + 2) { --ep-accent: var(--accent-biz); }
.episode:nth-child(3n) { --ep-accent: var(--accent-creative); }

.episode::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 3px;
  height: 100%;
  background: var(--ep-accent);
  opacity: 0.85;
}

.episode-title {
  font-family: var(--display);
  margin: 0 0 0.35rem;
  font-size: 1.1rem;
  font-weight: 700;
}

.path-hint {
  margin: 0 0 1rem;
  font-size: 0.75rem;
  color: var(--text-dim);
}

.muted { color: var(--text-dim); }

.media { margin: 10px 0; }
.audio audio,
.video video {
  width: 100%;
  max-height: 520px;
  border-radius: 4px;
  border: 1px solid var(--border);
}
.image img {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  border: 1px solid var(--border);
}
.pdf-frame {
  width: 100%;
  height: min(70vh, 720px);
  border: 1px solid var(--border);
  border-radius: 4px;
  background: #050506;
}

details {
  margin: 10px 0;
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 0.5rem 0.75rem;
  background: rgba(0, 0, 0, 0.2);
}

summary {
  cursor: pointer;
  font-family: var(--mono);
  font-size: 0.7rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--accent-ai);
  font-weight: 700;
}

summary:hover { color: var(--text); }

.code {
  white-space: pre-wrap;
  word-break: break-word;
  overflow: auto;
  max-height: 420px;
  padding: 12px;
  border-radius: 4px;
  border: 1px solid var(--border);
  background: #050506;
  color: #c8f7e4;
  font-size: 0.78rem;
  font-family: var(--body-mono);
}

.button {
  display: inline-block;
  padding: 10px 12px;
  border-radius: 4px;
  border: 1px solid var(--border);
  background: rgba(0, 255, 157, 0.06);
  color: var(--accent-ai);
  text-decoration: none;
  font-family: var(--mono);
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.button:hover {
  background: rgba(0, 255, 157, 0.12);
  color: var(--text);
}

.download a {
  color: var(--accent-creative);
  text-decoration: none;
  border-bottom: 1px solid rgba(255, 107, 203, 0.35);
}

.download a:hover { color: var(--text); }

.notebook-meta a { color: var(--accent-biz); text-decoration: none; }
.notebook-meta a:hover { color: var(--text); }

.footer {
  padding: 2.5rem 1.5rem;
  text-align: center;
  border-top: 1px solid var(--border);
}

.footer-text {
  font-size: 0.7rem;
  color: var(--text-dim);
  margin: 0;
}

.footer-text code {
  font-family: var(--mono);
  font-size: 0.85em;
  color: var(--accent-ai);
}

code {
  font-family: var(--mono);
  font-size: 0.9em;
}

@media (max-width: 768px) {
  .stats-bar { gap: 1.5rem; }
  .repo-grid { grid-template-columns: 1fr; }
  .scroll-hint { display: none; }
}

/* --- View variants (hub / grid / list) --- */
.variant-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.65rem;
  align-items: center;
  padding: 0.75rem 1rem;
  background: rgba(10, 10, 12, 0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  font-family: var(--mono);
  font-size: 0.62rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.variant-nav a {
  color: var(--accent-ai);
  text-decoration: none;
}

.variant-nav a:hover {
  color: var(--text);
}

.variant-sep {
  color: var(--text-dim);
  user-select: none;
}

.variant-current {
  color: var(--text);
}

/* Variant 3 — compact list */
body.compact-variant .hero-compact {
  min-height: auto;
  padding-top: 2rem;
}

.compact-section {
  padding-top: 1rem;
}

.compact-list {
  list-style: none;
  margin: 0;
  padding: 0;
  border: 1px solid var(--border);
  background: var(--bg);
}

.dir-row {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border);
  align-items: baseline;
}

.dir-row:last-child {
  border-bottom: 0;
}

.dir-row:hover {
  background: var(--surface-hover);
}

.dir-link {
  color: var(--text);
  text-decoration: none;
  font-family: var(--display);
  font-weight: 700;
  font-size: 0.95rem;
  flex: 1;
  text-align: left;
}

.dir-link:hover {
  color: var(--accent-ai);
}

.dir-meta {
  font-family: var(--mono);
  font-size: 0.62rem;
  color: var(--text-dim);
  white-space: nowrap;
}

/* Per-notebook variants */
.page-v2 .episode-grid {
  background: transparent;
  border: 0;
  gap: 10px;
}

.page-v2 .episode {
  border: 1px solid var(--border);
  padding: 1rem;
}

.page-v2 .episode-title {
  font-size: 1rem;
}

.page-v3 .episode {
  background:
    linear-gradient(160deg, rgba(0, 255, 157, 0.06), transparent 35%),
    linear-gradient(340deg, rgba(255, 107, 203, 0.05), transparent 50%),
    var(--surface);
  padding: 1.9rem;
}

.page-v3 .episode-title {
  font-size: 1.25rem;
}
"""
    write_text(SITE / "styles.css", css)

    write_versions_catalog(VERSIONS_ROOT, build_id)
    update_latest_symlink(SITE_ROOT, build_id)

    print(f"Build {build_id}: wrote {SITE / 'index.html'}")
    print(f"Build {build_id}: wrote {SITE / 'index-compact.html'}")
    print(f"Build {build_id}: wrote {SITE / 'styles.css'}")
    notebook_page_count = len(list(PAGES.glob("*.html")))
    print(f"Build {build_id}: wrote {notebook_page_count} pages under {PAGES}")
    print(f"Catalog: {VERSIONS_ROOT / 'index.html'}")
    print(f"Latest symlink: {SITE_ROOT / 'latest'} -> versions/{build_id}")


if __name__ == "__main__":
    main()
