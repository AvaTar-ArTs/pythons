"""
Data Processing Json Page 1

This module provides functionality for data processing json page 1.

Author: Auto-generated
Date: 2025-11-01
"""


# Constants
CONSTANT_160 = 160
CONSTANT_220 = 220
CONSTANT_404 = 404
CONSTANT_2822 = 2822

#!/usr/bin/env python3
"""
Page Maker v3 — a lean static generator with good defaults.
Fixes, improvements, and creative formatting include:
- Robust asset handling (copied into output/assets).
- Canonical tags only when site_url is set.
- RFC CONSTANT_2822 pubDate in RSS; sitemap with lastmod.
- Tag pages, year archives, and home pagination.
- Client-side search + index generator.
- Sticky TOC, copy buttons on code, autolinked headings.
- Reading time + word count; open-graph defaults; robots.txt + CONSTANT_404.html.
- Config via CLI flags or a config.yml next to page_maker.py.
"""

import argparse, datetime, json, os, re, sys, math, itertools, yaml
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, field

# Third-party
from jinja2 import Environment, FileSystemLoader, select_autoescape

# ---------------- Utilities ----------------

def slugify(text: str) -> str:
    text = (text or "").strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "-", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-") or "page"
def summarize_text(text: str, length: int = CONSTANT_160) -> str:
    clean = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", text or "")).strip()
    return (clean[:length] + "…") if len(clean) > length else clean
def guess_date(meta: Dict[str, Any], default=None) -> str:
    dt = meta.get("date") or default
    if not dt:
        return datetime.date.today().isoformat()
    if isinstance(dt, (int, float)):
        return datetime.datetime.fromtimestamp(dt).date().isoformat()
    for fmt in ("%Y-%m-%d","%Y/%m/%d","%m/%d/%Y","%Y-%m-%d %H:%M","%Y-%m-%dT%H:%M:%S","%Y-%m-%dT%H:%M:%S%z"):
        try:
            return datetime.datetime.strptime(str(dt), fmt).date().isoformat()
        except Exception:
            pass
    return str(dt)

def reading_time_words(text: str) -> Tuple[int, int]:
    words = len(re.findall(r"\w+", text or ""))
    minutes = max(1, math.ceil(words / CONSTANT_220)) if words else 1
    return words, minutes
def read_text(p: Path) -> str:
    with p.open("r", encoding="utf-8") as f:
        return f.read()
def write_text(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        f.write(s)

def load_yaml_config(path: Path) -> Dict[str, Any]:
    if path.exists():
        try:
            return yaml.safe_load(read_text(path)) or {}
        except Exception:
            return {}
    return {}

# ---------------- Markdown ----------------
import markdown as md

def md_to_html(markdown_text: str, enable_toc: bool) -> Tuple[str, Dict[str, Any]]:
    extensions = ["extra", "admonition", "sane_lists", "tables", "fenced_code", "codehilite"]
    for ext in ["toc", "footnotes", "attr_list", "def_list"]:
        try:
            __import__("markdown.extensions."+ext)
            extensions.append(ext)
        except Exception:
            pass
    extension_configs = {"codehilite": {"guess_lang": True, "noclasses": False}}
    if "toc" in extensions and enable_toc:
        extension_configs["toc"] = {"title": "Contents", "permalink": True, "anchorlink": True, "baselevel": 2}
    conv = md.Markdown(extensions=extensions, extension_configs=extension_configs, output_format="html5")
    html_out = conv.convert(markdown_text or "")
    meta = {"toc_html": getattr(conv, "toc", "")}
    return html_out, meta

# ---------------- Data Model ----------------

@dataclass
class Page:
    title: str
    slug: str
    body_md: str
    description: str = ""
    tags: List[str] = field(default_factory=list)
    author: str = ""
    date: str = field(default_factory=lambda: datetime.date.today().isoformat())
    updated: str = field(default_factory=lambda: datetime.datetime.now().isoformat(timespec="seconds"))
    draft: bool = False
    toc: bool = True
    words: int = 0
    minutes: int = 1
    extras: Dict[str, Any] = field(default_factory=dict)

    def fm(self) -> str:
        data = {
            "title": self.title, "slug": self.slug, "description": self.description,
            "tags": self.tags, "author": self.author, "date": self.date,
            "updated": self.updated, "draft": self.draft, "toc": self.toc,
            "words": self.words, "reading_minutes": self.minutes, **self.extras
        }
        return "---\n" + yaml.safe_dump({k:v for k,v in data.items() if v is not None}, sort_keys=False, allow_unicode=True).strip() + Path("\n---\n\n")

# ---------------- Parsing ----------------

def parse_front_matter(raw: str) -> Tuple[Dict[str, Any], str]:
    if raw.startswith("---"):
        parts = raw.split(Path("\n"))
        try:
            end = next(i for i, line in enumerate(parts[1:], start=1) if line.strip() == "---")
            fm = yaml.safe_load(Path("\n").join(parts[1:end])) or {}
            body = Path("\n").join(parts[end+1:])
            return fm, body
        except StopIteration:
            pass
    return {}, raw

def extract_title(body: str) -> Optional[str]:
    for line in (body or "").splitlines():
        m = re.match(r"^#\s+(.+)", line.strip())
        if m: return m.group(1).strip()
    return None

def load_pages(input_dir: Path) -> List[Page]:
    pages: List[Page] = []
    for path in sorted(input_dir.rglob("*")):
        if path.is_dir(): continue
        ext = path.suffix.lower()
        try:
            raw = read_text(path)
        except Exception:
            continue

        if ext in [".md",".markdown"]:
            meta, body = parse_front_matter(raw)
            title = meta.get("title") or extract_title(body) or path.stem.replace("-", " ").title()
            slug = meta.get("slug") or slugify(title)
            desc = meta.get("description") or summarize_text(body)
            tags = [str(t) for t in (meta.get("tags") or [])]
            author = meta.get("author") or ""
            date = guess_date(meta)
            draft = bool(meta.get("draft", False))
            toc = bool(meta.get("toc", True))
            words, minutes = reading_time_words(body)
            updated = meta.get("updated") or datetime.datetime.now().isoformat(timespec="seconds")
            extras = {k:v for k,v in meta.items() if k not in {"title","slug","description","tags","author","date","draft","toc","updated","words","reading_minutes"}}
            pages.append(Page(title, slug, body, desc, tags, author, date, updated, draft, toc, words, minutes, extras))

        elif ext in [".json",".yml",".yaml"]:
            try:
                meta = json.loads(raw) if ext == ".json" else yaml.safe_load(raw)
                body = meta.get("content","")
                title = meta.get("title") or path.stem.replace("-", " ").title()
                slug = meta.get("slug") or slugify(title)
                desc = meta.get("description") or summarize_text(body)
                tags = [str(t) for t in (meta.get("tags") or [])]
                author = meta.get("author") or ""
                date = guess_date(meta)
                draft = bool(meta.get("draft", False))
                toc = bool(meta.get("toc", True))
                words, minutes = reading_time_words(body)
                updated = meta.get("updated") or datetime.datetime.now().isoformat(timespec="seconds")
                extras = {k:v for k,v in meta.items() if k not in {"title","slug","description","tags","author","date","draft","toc","updated","words","reading_minutes","content"}}
                pages.append(Page(title, slug, body, desc, tags, author, date, updated, draft, toc, words, minutes, extras))
            except Exception:
                continue
    return [p for p in pages if not p.draft]

# ---------------- Jinja ----------------

def build_env(templates_dir: Path):
    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html","xml"]),
        trim_blocks=True,
        lstrip_blocks=True)
    env.filters["datefmt"] = lambda s, fmt="%b %d, %Y": datetime.datetime.fromisoformat(str(s).replace("Z","").replace(" ","T")).strftime(fmt) if s else ""
    env.filters["rfc822"] = lambda s: datetime.datetime.fromisoformat(str(s).replace("Z","").replace(" ","T")).strftime("%a, %d %b %Y %H:%M:%S %z") if s else ""
    env.filters["slug"] = lambda t: re.sub(r"-+", "-", re.sub(r"[^a-z0-9-]", "-", (t or "").lower())).strip("-")
    env.filters["json"]  = lambda obj: json.dumps(obj, ensure_ascii=False)
    env.globals["now"] = datetime.datetime.now().isoformat(timespec="seconds")
    return env

# ---------------- Build ----------------

def paginate(items: List[Any], size: int):
    for i in range(0, len(items), size):
        yield (i//size)+1, items[i:i+size]

def article_jsonld(site: Dict[str, Any], p: Page) -> Dict[str, Any]:
    base = site.get("site_url","").rstrip("/")
    url = f"{base}/{p.slug}.html" if base else ""
    return {
        "@context":"https://schema.org",
        "@type":"Article",
        "headline": p.title,
        "description": p.description,
        "author": {"@type":"Person","name": (p.author or site.get("author",""))},
        "datePublished": p.date,
        "dateModified": p.updated,
        "wordCount": p.words,
        "url": url,
        "keywords": ", ".join(p.tags)
    }

def build_site(input_dir: Path, output_dir: Path, templates_dir: Path, site: Dict[str, Any], out_format: str="both"):
    env = build_env(templates_dir)
    pages = load_pages(input_dir)
    pages_sorted = sorted(pages, key=lambda x: (x.date, x.updated), reverse=True)

    # Collect tags and archives
    tags: Dict[str, List[Page]] = {}
    archives: Dict[str, List[Page]] = {}
    for p in pages_sorted:
        for t in p.tags: tags.setdefault(t, []).append(p)
        year = str(p.date)[:4]
        archives.setdefault(year, []).append(p)

    # Render pages
    for idx, p in enumerate(pages_sorted):
        body_html, meta = md_to_html(p.body_md, p.toc)
        prevp = pages_sorted[idx-1] if idx-1 >= 0 else None
        nextp = pages_sorted[idx+1] if idx+1 < len(pages_sorted) else None

        if out_format in ("both","html"):
            html = env.get_template("base.html").render(
                site=site, page=p, body=body_html, toc_html=meta.get("toc_html",""),
                prev_page=prevp, next_page=nextp, json_ld=article_jsonld(site,p)
            )
            write_text(output_dir / f"{p.slug}.html", html)
        if out_format in ("both","md"):
            body = p.body_md if re.search(r"^#\s+", p.body_md, flags=re.M) else f"# {p.title}\n\n{p.body_md}"
            write_text(output_dir / f"{p.slug}.md", p.fm() + body.strip() + Path("\n"))

    # Index with pagination (10 per page)
    if out_format in ("both","html"):
        per_page = 10
        for page_num, chunk in paginate(pages_sorted, per_page):
            html = env.get_template("index.html").render(site=site, pages=chunk, page_num=page_num, total=len(pages_sorted))
            name = "index.html" if page_num == 1 else f"page/{page_num}.html"
            write_text(output_dir / name, html)

        # Tag pages
        tag_t = env.get_template("tag.html")
        for tag, plist in sorted(tags.items()):
            html = tag_t.render(site=site, tag=tag, pages=sorted(plist, key=lambda x: (x.date, x.updated), reverse=True))
            write_text(output_dir / f"tag-{slugify(tag)}.html", html)

        # Archives
        arch_t = env.get_template("archive.html")
        for year, plist in sorted(archives.items(), reverse=True):
            html = arch_t.render(site=site, year=year, pages=sorted(plist, key=lambda x: (x.date, x.updated), reverse=True))
            write_text(output_dir / f"archive-{year}.html", html)

        # Search index + page
        idx = [{"title":p.title,"slug":p.slug,"description":p.description,"tags":p.tags,"date":p.date} for p in pages_sorted]
        write_text(output_dir / "search_index.json", json.dumps(idx, ensure_ascii=False, indent=2))
        write_text(output_dir / "search.html", env.get_template("search.html").render(site=site))
        # RSS + sitemap + robots + CONSTANT_404
        write_text(output_dir / "rss.xml", env.get_template("rss.xml").render(site=site, pages=pages_sorted))
        write_text(output_dir / "sitemap.xml", env.get_template("sitemap.xml").render(site=site, pages=pages_sorted))
        write_text(output_dir / "robots.txt", env.get_template("robots.txt").render(site=site))
        write_text(output_dir / "CONSTANT_404.html", env.get_template("CONSTANT_404.html").render(site=site))

    # Copy assets
    assets_src = templates_dir / "assets"
    assets_dst = output_dir / "assets"
    if assets_src.exists():
        import shutil
        if assets_dst.exists(): shutil.rmtree(assets_dst)
        shutil.copytree(assets_src, assets_dst)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input","-i",default="content")
    ap.add_argument("--output","-o",default="output")
    ap.add_argument("--templates","-t",default="templates")
    ap.add_argument("--site-title",default=None)
    ap.add_argument("--site-description",default=None)
    ap.add_argument("--site-url",default=None)
    ap.add_argument("--author",default=None)
    ap.add_argument("--format",choices=["html","md","both"],default="both")
    ap.add_argument("--config",default="config.yml", help="Optional YAML config file")
    args = ap.parse_args()

    cfg = load_yaml_config(Path(args.config)).get("site", {})
    site = {
        "title": args.site_title or cfg.get("title","My Site"),
        "description": args.site_description or cfg.get("description","Clean pages, zero fuss."),
        "site_url": (args.site_url or cfg.get("site_url","")).rstrip("/"),
        "author": args.author or cfg.get("author",""),
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "og_image": cfg.get("og_image",""),
    }
    build_site(Path(args.input), Path(args.output), Path(args.templates), site, out_format=args.format)

if __name__ == "__main__":
    main()
