#!/usr/bin/env python3
"""Local-first monetization audit for a macOS creative/automation archive.

Stdlib only. It writes reports, never uploads files, and never copies file contents.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


DEFAULT_EXCLUDES = {
    ".git", ".hg", ".svn", "node_modules", "__pycache__", ".venv", "venv",
    "env", "dist", "build", ".next", "coverage", "Library", "Applications",
    "Library/Developer", "Movies/iMovie Library.imovielibrary",
}

MACOS_LIBRARY_SKIP = {"Caches", "Developer", "Containers", "Logs", "Saved Application State"}
IMPORTANT_HIDDEN_DIRS = {
    ".agent-skills", ".agents", ".book_of_memory", ".autotagger-lite", ".mcp-central",
    ".memory", ".music-vault", ".notebooklm", ".hermes", ".file-tracker",
}

EXTENSIONS = {
    "audio": {".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg", ".aiff"},
    "video": {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v"},
    "image": {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".tif", ".tiff", ".psd"},
    "code": {".py", ".js", ".ts", ".tsx", ".jsx", ".sh", ".bash", ".zsh", ".go", ".rs", ".java", ".php", ".rb"},
    "document": {".md", ".txt", ".rtf", ".docx", ".pdf", ".pages", ".odt"},
    "data": {".csv", ".json", ".jsonl", ".parquet", ".xlsx", ".xls", ".sqlite", ".db"},
    "web": {".html", ".htm", ".css", ".scss", ".xml"},
    "archive": {".zip", ".tar", ".gz", ".7z", ".rar"},
    "design": {".fig", ".sketch", ".blend", ".fbx", ".obj", ".glb", ".gltf"},
}

CHANNELS = {
    "digital_product": "Lemon Squeezy / direct download",
    "fiverr": "Fiverr implementation or custom service",
    "github": "GitHub proof / open-core / Sponsors",
    "apify": "Apify Actor or data product",
    "huggingface": "Hugging Face demo or model wrapper",
    "mcp": "MCP server / agent tool",
    "notion": "Notion template or workspace",
    "canva": "Canva template, element, or music creator",
    "stock": "Adobe Stock / Pond5 / asset licensing",
    "envato": "Envato-style code, media, or template license",
    "api": "Hosted API / RapidAPI / private endpoint",
    "n8n": "n8n workflow / template / implementation",
    "subscription": "Membership, maintenance, or recurring catalog",
    "streaming": "Music release / streaming catalog",
    "licensing": "Direct sync, soundtrack, white-label, or OEM license",
}

KEYWORDS = {
    "agent": {"mcp", "agent", "skill", "claude", "cursor", "codex", "hermes", "tool", "router", "memory"},
    "automation": {"automation", "workflow", "pipeline", "etl", "scrape", "crawler", "scheduler", "orchestr"},
    "media": {"media", "metadata", "audio", "music", "suno", "tts", "transcri", "video", "image", "gallery"},
    "creative": {"avatar", "trashcat", "heartbreak", "lore", "comic", "prompt", "character", "art", "design", "brand"},
    "research": {"research", "seo", "geo", "aeo", "notebook", "evidence", "citation", "knowledge", "brief"},
    "product": {"readme", "docs", "template", "starter", "pack", "kit", "demo", "app", "site", "dashboard"},
}

RISK_PATTERNS = {
    "possible_secret_filename": re.compile(r"(^|[._-])(secret|token|credential|password|passwd|apikey|api_key|private|ssh_key)([._-]|$)", re.I),
    "possible_secret_content": re.compile(r"(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY)", re.I),
    "rights_review": re.compile(r"(suno|udio|ai[-_ ]generated|generated[-_ ]ai|sample|copyright|license|royalt|content.?id|voice|likeness)", re.I),
    "unfinished": re.compile(r"(todo|wip|draft|prototype|scratch|test|old|backup|copy)($|[._ -])", re.I),
}


def classify(path: Path) -> str:
    suffix = path.suffix.lower()
    for kind, exts in EXTENSIONS.items():
        if suffix in exts:
            return kind
    return "other"


def keyword_groups(path: Path) -> list[str]:
    text = path.as_posix().lower().replace("_", " ").replace("-", " ")
    return sorted(group for group, words in KEYWORDS.items() if any(word in text for word in words))


def channels_for(kind: str, groups: list[str], name: str) -> list[str]:
    channels: set[str] = set()
    if kind == "audio":
        channels.update({"streaming", "licensing", "stock", "canva", "subscription"})
    elif kind == "image":
        channels.update({"stock", "canva", "digital_product", "licensing"})
    elif kind == "video":
        channels.update({"stock", "digital_product", "licensing", "huggingface"})
    elif kind == "code":
        channels.update({"github", "digital_product", "fiverr", "api"})
    elif kind in {"data", "document"}:
        channels.update({"digital_product", "fiverr", "notion"})
    elif kind in {"web", "design"}:
        channels.update({"digital_product", "envato", "fiverr", "canva"})
    if "agent" in groups:
        channels.update({"mcp", "github", "huggingface", "subscription"})
    if "automation" in groups:
        channels.update({"apify", "api", "fiverr", "n8n"})
    if "research" in groups:
        channels.update({"notion", "digital_product", "subscription", "fiverr"})
    if "creative" in groups:
        channels.update({"canva", "stock", "licensing", "digital_product"})
    if any(term in name.lower() for term in ("etsy", "printify", "listing", "seo")):
        channels.update({"fiverr", "digital_product", "api"})
    return sorted(channels)


def score(kind: str, groups: list[str], size: int, channels: list[str], risks: list[str]) -> int:
    value = {"audio": 24, "video": 23, "image": 20, "code": 24, "data": 18, "document": 15, "web": 17, "design": 21}.get(kind, 8)
    value += min(len(groups) * 7, 28) + min(len(channels) * 3, 18)
    if size > 10_000:
        value += 5
    if "possible_secret_content" in risks:
        value -= 35
    if "unfinished" in risks:
        value -= 8
    if "rights_review" in risks:
        value -= 3
    return max(0, min(100, value))


def hash_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def content_risks(path: Path, max_bytes: int, scan_content: bool) -> list[str]:
    risks: list[str] = []
    if RISK_PATTERNS["possible_secret_filename"].search(path.name):
        risks.append("possible_secret_filename")
    if RISK_PATTERNS["unfinished"].search(path.name):
        risks.append("unfinished")
    if RISK_PATTERNS["rights_review"].search(path.name):
        risks.append("rights_review")
    if scan_content and path.suffix.lower() in {".py", ".js", ".ts", ".sh", ".env", ".json", ".yaml", ".yml", ".md", ".txt"}:
        try:
            raw = path.read_bytes()[:max_bytes]
            text = raw.decode("utf-8", errors="ignore")
            if RISK_PATTERNS["possible_secret_content"].search(text):
                risks.append("possible_secret_content")
            if RISK_PATTERNS["rights_review"].search(text):
                risks.append("rights_review")
        except (OSError, PermissionError):
            risks.append("unreadable")
    return sorted(set(risks))


def iter_files(root: Path, excludes: set[str], include_hidden: bool, include_library: bool) -> Iterable[Path]:
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        relative = current_path.relative_to(root).as_posix()
        in_library = "Library" in current_path.relative_to(root).parts
        dirs[:] = [
            d for d in dirs
            if (d not in excludes or (include_library and d == "Library"))
            and d != ".DS_Store"
            and f"{relative}/{d}" not in excludes
            and not (in_library and d in MACOS_LIBRARY_SKIP)
            and (include_hidden or not d.startswith(".") or d in IMPORTANT_HIDDEN_DIRS)
            and (include_library or d != "Library")
        ]
        for filename in files:
            path = current_path / filename
            try:
                if not path.is_symlink() and path.is_file():
                    yield path
            except OSError:
                continue


def audit(root: Path, output: Path, do_hash: bool, max_content_bytes: int, scan_content: bool, excludes: set[str], include_hidden: bool, include_library: bool, progress_seconds: float = 2.0) -> tuple[list[dict], bool]:
    records: list[dict] = []
    started = time.monotonic()
    last_progress = started
    kind_counts: Counter = Counter()
    risk_count = 0
    candidate_count = 0
    interrupted = False
    print(f"Starting audit: {root}", flush=True)
    print(f"Mode: {'hashes ' if do_hash else ''}{'content scan' if scan_content else 'metadata-first'}", flush=True)
    try:
        for path in iter_files(root, excludes, include_hidden, include_library):
            try:
                stat = path.stat()
            except (OSError, PermissionError):
                continue
            kind = classify(path)
            groups = keyword_groups(path)
            risks = content_risks(path, max_content_bytes, scan_content)
            channels = channels_for(kind, groups, path.name)
            record = {
                "path": str(path),
                "relative_path": os.path.relpath(os.fspath(path), os.fspath(root)),
                "name": path.name,
                "extension": path.suffix.lower(),
                "kind": kind,
                "size_bytes": stat.st_size,
                "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                "keyword_groups": groups,
                "monetization_channels": channels,
                "monetization_score": score(kind, groups, stat.st_size, channels, risks),
                "risk_flags": risks,
                "sha256": hash_file(path) if do_hash else None,
            }
            records.append(record)
            kind_counts[kind] += 1
            risk_count += len(risks)
            candidate_count += record["monetization_score"] >= 45
            now = time.monotonic()
            if progress_seconds > 0 and now - last_progress >= progress_seconds:
                elapsed = max(now - started, 0.001)
                rate = len(records) / elapsed
                top_kind = kind_counts.most_common(1)[0][0] if kind_counts else "—"
                print(
                    f"\rIndexed {len(records):,} files | {rate:,.1f}/s | candidates {candidate_count:,} | risks {risk_count:,} | top type {top_kind} | {path.name[:70]}",
                    end="",
                    flush=True,
                )
                last_progress = now
    except KeyboardInterrupt:
        interrupted = True
        print("\n\nInterrupted by user; writing partial reports...", flush=True)
    elapsed = max(time.monotonic() - started, 0.001)
    print(
        f"\n{'Partial ' if interrupted else ''}audit summary: {len(records):,} files | {len(records) / elapsed:,.1f}/s | {elapsed:,.1f}s | candidates {candidate_count:,} | risks {risk_count:,}",
        flush=True,
    )
    return records, interrupted


def write_reports(records: list[dict], root: Path, output: Path, top_n: int) -> None:
    output.mkdir(parents=True, exist_ok=True)
    ranked = sorted(records, key=lambda item: (item["monetization_score"], item["size_bytes"]), reverse=True)
    with (output / "assets.json").open("w", encoding="utf-8") as handle:
        json.dump({"root": str(root), "generated_utc": datetime.now(timezone.utc).isoformat(), "assets": records}, handle, indent=2)
    fields = list(records[0].keys()) if records else ["path"]
    with (output / "assets.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            row = dict(record)
            row["keyword_groups"] = ";".join(row["keyword_groups"])
            row["monetization_channels"] = ";".join(row["monetization_channels"])
            row["risk_flags"] = ";".join(row["risk_flags"])
            writer.writerow(row)
    by_kind = Counter(item["kind"] for item in records)
    by_channel = Counter(channel for item in records for channel in item["monetization_channels"])
    risks = Counter(flag for item in records for flag in item["risk_flags"])
    duplicate_groups = defaultdict(list)
    for item in records:
        if item.get("sha256"):
            duplicate_groups[item["sha256"]].append(item["relative_path"])
    duplicate_groups = {digest: paths for digest, paths in duplicate_groups.items() if len(paths) > 1}
    with (output / "duplicates.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["sha256", "duplicate_count", "paths"])
        for digest, paths in duplicate_groups.items():
            writer.writerow([digest, len(paths), " | ".join(paths)])
    lines = [
        "# Avatar-Arts Monetization Audit", "",
        f"Root: `{root}`", f"Generated: `{datetime.now().isoformat(timespec='seconds')}`", "",
        f"Files indexed: **{len(records):,}**", "",
        "## Highest-priority candidates", "",
        "| Score | Kind | Asset | Channels | Risks |", "|---:|---|---|---|---|",
    ]
    for item in ranked[:top_n]:
        lines.append(f"| {item['monetization_score']} | {item['kind']} | `{item['relative_path']}` | {', '.join(item['monetization_channels'])} | {', '.join(item['risk_flags']) or '—'} |")
    lines += ["", "## Inventory by kind", ""] + [f"- **{key}:** {value:,}" for key, value in by_kind.most_common()]
    lines += ["", "## Channel opportunity counts", ""] + [f"- **{CHANNELS.get(key, key)}:** {value:,} candidate files" for key, value in by_channel.most_common()]
    lines += ["", "## Risk review", ""] + [f"- **{key}:** {value:,}" for key, value in risks.most_common()] if risks else lines + ["", "No risk flags detected by the configured heuristics."]
    lines += ["", "## Duplicate review", "", f"Hash duplicate groups found: **{len(duplicate_groups):,}**", "", "See `duplicates.csv` for paths. Duplicate files should be consolidated before packaging or licensing."]
    lines += ["", "## Interpretation", "", "This is a prioritization aid, not a legal ownership determination or a promise that every file is commercially usable.", "", "Recommended first filters: highest score, clear provenance, no secret flags, no unresolved third-party rights, and a coherent collection of related assets.", ""]
    (output / "monetization-report.md").write_text("\n".join(lines), encoding="utf-8")
    rows = []
    for item in ranked[:top_n]:
        rows.append("<tr>" + "".join(f"<td>{html.escape(str(item[field]))}</td>" for field in ("monetization_score", "kind", "relative_path", "monetization_channels", "risk_flags")) + "</tr>")
    page = "<html><meta charset='utf-8'><title>Avatar-Arts Monetization Audit</title><style>body{font:14px system-ui;margin:2rem;background:#111;color:#eee}table{border-collapse:collapse;width:100%}td,th{border:1px solid #444;padding:.5rem;text-align:left}th{background:#26364a}td{vertical-align:top}</style><h1>Avatar-Arts Monetization Audit</h1><p>Root: " + html.escape(str(root)) + f" · {len(records):,} files</p><table><tr><th>Score</th><th>Kind</th><th>Asset</th><th>Channels</th><th>Risks</th></tr>{''.join(rows)}</table></html>"
    (output / "monetization-report.html").write_text(page, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a local folder for monetizable Avatar-Arts assets.")
    parser.add_argument("root", nargs="?", default="/Users/steven", help="Folder to scan; defaults to /Users/steven")
    parser.add_argument("--output", default="./avatar-arts-audit", help="Report directory")
    parser.add_argument("--hash", action="store_true", help="Compute SHA-256 hashes; slower on large archives")
    parser.add_argument("--content-scan", action="store_true", help="Inspect limited text contents for secret/rights patterns; slower")
    parser.add_argument("--include-hidden", action="store_true", help="Scan all hidden directories; default preserves only known asset folders")
    parser.add_argument("--include-library", action="store_true", help="Scan macOS ~/Library; usually run it separately because it is very large")
    parser.add_argument("--progress-seconds", type=float, default=2.0, help="Seconds between live progress updates; use 0 to disable")
    parser.add_argument("--content-bytes", type=int, default=256_000, help="Maximum text bytes inspected per file")
    parser.add_argument("--top", type=int, default=250, help="Number of ranked candidates in reports")
    parser.add_argument("--exclude", action="append", default=[], help="Additional directory or relative path to skip")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"Root is not a readable directory: {root}", file=sys.stderr)
        return 2
    excludes = set(DEFAULT_EXCLUDES) | set(args.exclude)
    records, interrupted = audit(root, Path(args.output).expanduser().resolve(), args.hash, args.content_bytes, args.content_scan, excludes, args.include_hidden, args.include_library, args.progress_seconds)
    write_reports(records, root, Path(args.output).expanduser().resolve(), args.top)
    print(f"Reports written to {Path(args.output).expanduser().resolve()}")
    return 130 if interrupted else 0


if __name__ == "__main__":
    raise SystemExit(main())
