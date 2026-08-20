#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

HOME = Path.home()
OUT_DIR = HOME / "avatararts-revenue-pages"
OUT_CSV = OUT_DIR / "HOME_REVENUE_AUDIT.csv"
OUT_MD = OUT_DIR / "HOME_REVENUE_AUDIT.md"

SKIP_DIRS = {
    ".git",
    ".cache",
    ".npm",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    "Library",
    "Applications",
    "Movies",
    "Music",
    "Pictures",
    ".Trash",
    ".local",
    ".cargo",
    ".rustup",
    ".pyenv",
}

TEXT_EXTS = {
    ".md",
    ".txt",
    ".html",
    ".htm",
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".json",
    ".yaml",
    ".yml",
    ".csv",
    ".sh",
}

HIGH_VALUE_TERMS = {
    "gumroad": 8,
    "payhip": 8,
    "stripe": 8,
    "paypal": 7,
    "ko-fi": 7,
    "kofi": 7,
    "buy me a coffee": 7,
    "patreon": 7,
    "etsy": 7,
    "printify": 7,
    "shopify": 7,
    "revenue": 6,
    "monetization": 6,
    "pricing": 5,
    "launch": 5,
    "product": 4,
    "offer": 4,
    "package": 4,
    "bundle": 4,
    "course": 5,
    "template": 4,
    "subscription": 6,
    "affiliate": 5,
    "adsense": 4,
    "client": 3,
    "service": 3,
    "consult": 4,
    "automation": 3,
    "agent": 3,
    "workflow": 3,
    "download": 2,
}

PATH_TERMS = {
    "avatararts": 8,
    "revenue": 8,
    "monetization": 8,
    "business": 6,
    "product": 5,
    "gumroad": 8,
    "payhip": 8,
    "shop": 5,
    "etsy": 7,
    "printify": 7,
    "soul-blueprint": 8,
    "gpt-to-claude": 5,
    "coh-taku": 4,
    "cox": 3,
    "avatararts.org": 6,
    "digitaldive": 6,
    "digita": 5,
    "agent": 3,
    "agents": 3,
    "course": 5,
    "template": 4,
}

READINESS_FILES = {
    "README.md": 3,
    "CHANGELOG.md": 2,
    "LICENSE": 1,
    "package.json": 3,
    "pyproject.toml": 3,
    "requirements.txt": 2,
    "Dockerfile": 3,
    "index.html": 3,
    "landing.html": 3,
    "privacy.html": 2,
    "terms.html": 2,
    "stripe.json": 6,
    "gumroad.md": 8,
}


@dataclass
class Candidate:
    root: Path
    score: int = 0
    files: int = 0
    dirs: int = 0
    size_bytes: int = 0
    ext_counts: Counter = field(default_factory=Counter)
    hits: Counter = field(default_factory=Counter)
    notable_files: list[str] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)

    @property
    def category(self) -> str:
        path = str(self.root).lower()
        if any(x in path for x in ["soul-blueprint", "avatararts-revenue-pages"]):
            return "Digital product"
        if any(x in path for x in ["avatararts.org", "website", "public_html"]):
            return "Website/funnel"
        if any(x in path for x in ["agent", "automation", "workflow", "gpt-to-claude"]):
            return "Automation/service"
        if any(x in path for x in ["coh", "cox", "mod"]):
            return "Community/tooling"
        if any(x in path for x in ["media", "music", "photo", "art", "image"]):
            return "Media/IP"
        return "Mixed asset"

    @property
    def readiness(self) -> str:
        if self.score >= 80:
            return "Launch candidate"
        if self.score >= 45:
            return "Package next"
        if self.score >= 25:
            return "Needs positioning"
        return "Low signal"


def is_skipped_dir(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & SKIP_DIRS)


def top_level_roots() -> list[Path]:
    roots = []
    for child in HOME.iterdir():
        if child.name in SKIP_DIRS:
            continue
        if child.name.startswith(".") and child.name not in {".agent-skills", ".codex", ".gemini"}:
            continue
        if child.is_dir():
            roots.append(child)
    return sorted(roots, key=lambda p: p.name.lower())


def text_preview(path: Path, max_bytes: int = 24000) -> str:
    try:
        data = path.read_bytes()[:max_bytes]
        return data.decode("utf-8", errors="ignore").lower()
    except Exception:
        return ""


def scan_root(root: Path, max_files: int | None = 1800) -> Candidate:
    c = Candidate(root=root)
    path_lower = str(root.relative_to(HOME)).lower()
    for term, weight in PATH_TERMS.items():
        if term in path_lower:
            c.score += weight
            c.hits[f"path:{term}"] += 1

    seen_files = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dpath = Path(dirpath)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        if is_skipped_dir(dpath):
            dirnames[:] = []
            continue
        c.dirs += 1
        for filename in filenames:
            seen_files += 1
            if max_files is not None and seen_files > max_files:
                c.hits["truncated:file_limit"] += 1
                return c
            f = dpath / filename
            rel = str(f.relative_to(root))
            suffix = f.suffix.lower()
            c.files += 1
            c.ext_counts[suffix or "[none]"] += 1
            try:
                c.size_bytes += f.stat().st_size
            except OSError:
                pass
            base_weight = READINESS_FILES.get(filename, 0)
            if base_weight:
                c.score += base_weight
                c.hits[f"file:{filename}"] += 1
                if len(c.notable_files) < 12:
                    c.notable_files.append(rel)
            name_lower = filename.lower()
            for term, weight in PATH_TERMS.items():
                if term in name_lower:
                    c.score += max(1, weight // 2)
                    c.hits[f"name:{term}"] += 1
                    if len(c.notable_files) < 12:
                        c.notable_files.append(rel)
            if suffix in TEXT_EXTS and f.stat().st_size < 1_000_000:
                body = text_preview(f)
                for term, weight in HIGH_VALUE_TERMS.items():
                    if term in body:
                        count = min(body.count(term), 4)
                        c.score += weight * count
                        c.hits[f"text:{term}"] += count
                        if len(c.examples) < 8:
                            c.examples.append(rel)
    return c


def fmt_size(n: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    value = float(n)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{n} B"


def write_outputs(candidates: list[Candidate]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    candidates = sorted(candidates, key=lambda c: c.score, reverse=True)
    with OUT_CSV.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Rank",
            "Score",
            "Readiness",
            "Category",
            "Path",
            "Files",
            "Dirs",
            "ApproxSize",
            "TopSignals",
            "NotableFiles",
        ])
        for idx, c in enumerate(candidates, 1):
            writer.writerow([
                idx,
                c.score,
                c.readiness,
                c.category,
                str(c.root),
                c.files,
                c.dirs,
                fmt_size(c.size_bytes),
                "; ".join(f"{k}={v}" for k, v in c.hits.most_common(8)),
                "; ".join(dict.fromkeys(c.notable_files[:10])),
            ])

    top = candidates[:30]
    launch = [c for c in candidates if c.readiness == "Launch candidate"][:15]
    package = [c for c in candidates if c.readiness == "Package next"][:15]
    lines = [
        "# Home Revenue Audit",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Scope: `{HOME}` excluding OS/cache/noisy development dependency folders.",
        "",
        "## Executive Summary",
        "",
        f"- Scanned top-level project/workspace directories: **{len(candidates)}**",
        f"- Launch candidates: **{len([c for c in candidates if c.readiness == 'Launch candidate'])}**",
        f"- Package-next candidates: **{len([c for c in candidates if c.readiness == 'Package next'])}**",
        "",
        "## Top Revenue Candidates",
        "",
        "| Rank | Score | Readiness | Category | Path | Signals |",
        "|---:|---:|---|---|---|---|",
    ]
    for idx, c in enumerate(top, 1):
        signals = ", ".join(k.replace("text:", "").replace("path:", "").replace("file:", "") for k, _ in c.hits.most_common(5))
        lines.append(f"| {idx} | {c.score} | {c.readiness} | {c.category} | `{c.root}` | {signals} |")

    lines += [
        "",
        "## Immediate Launch Candidates",
        "",
    ]
    for c in launch:
        lines += [
            f"### {c.root.name}",
            f"- Path: `{c.root}`",
            f"- Category: {c.category}",
            f"- Score: {c.score}",
            f"- Notable files: {', '.join(dict.fromkeys(c.notable_files[:8])) or 'none'}",
            f"- Signals: {', '.join(f'{k}={v}' for k, v in c.hits.most_common(8))}",
            "",
        ]

    lines += [
        "## Package Next",
        "",
    ]
    for c in package:
        lines += [
            f"- `{c.root}` — {c.category}, score {c.score}, signals: {', '.join(k for k, _ in c.hits.most_common(5))}",
        ]

    lines += [
        "",
        "## Suggested Revenue Stack",
        "",
        "1. **Direct digital products:** package existing engines, guides, and templates as Gumroad/Payhip downloads.",
        "2. **Support/donation:** use community tools and free guides as the trust-builder, then add Ko-fi/Buy Me a Coffee.",
        "3. **Services:** sell creative automation, AI handoff systems, and asset cataloging from the strongest existing workflows.",
        "4. **Merch/prints:** route visual art and symbolic products into Etsy/Printify instead of relying on ad revenue.",
        "",
        "## CSV Export",
        "",
        f"- `{OUT_CSV}`",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit home-directory projects for revenue potential.")
    parser.add_argument(
        "--max-files",
        type=int,
        default=1800,
        help="Maximum files to inspect per top-level root. Use 0 for no file cap. Folder depth is always unlimited.",
    )
    args = parser.parse_args()
    max_files = None if args.max_files == 0 else args.max_files

    roots = top_level_roots()
    candidates = [scan_root(root, max_files=max_files) for root in roots]
    candidates = [c for c in candidates if c.score > 0 or c.files > 20]
    write_outputs(candidates)
    print(OUT_MD)
    print(OUT_CSV)
    for c in sorted(candidates, key=lambda c: c.score, reverse=True)[:12]:
        print(f"{c.score:4d} {c.readiness:16s} {c.category:18s} {c.root}")


if __name__ == "__main__":
    main()
