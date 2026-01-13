from __future__ import annotations

import csv
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]

IGNORE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
}

TEXT_EXTS = {
    ".py",
    ".ipynb",
    ".md",
    ".txt",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".csv",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
}


@dataclass
class FileEntry:
    path: str
    name: str
    ext: str
    size: int
    mtime: float
    kind: str
    project: str
    tags: List[str]
    summary: str | None = None


def iter_files(base: Path) -> Iterable[Path]:
    for root, dirs, files in os.walk(base):
        # prune ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            yield Path(root) / f


def guess_project(p: Path) -> str:
    parts = p.relative_to(ROOT).parts
    if not parts:
        return "root"
    # Consider top-level directory as project if not root-level file
    return parts[0] if len(parts) > 1 else "root"


def classify(p: Path) -> str:
    ext = p.suffix.lower()
    if ext == ".py":
        return "python"
    if ext in {".md", ".txt"}:
        return "docs"
    if ext in {".ipynb"}:
        return "notebook"
    if ext in {".json", ".toml", ".yaml", ".yml", ".ini"}:
        return "config"
    if ext in {".csv"}:
        return "data"
    if ext in {".js", ".ts", ".tsx", ".jsx"}:
        return "web"
    if ext in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
        return "asset"
    return "other"


def tag_for(p: Path) -> List[str]:
    tags: List[str] = []
    name = p.name.lower()
    parent = guess_project(p).lower()
    if any(k in name for k in ["ocr", "image", "img", "resize", "mask", "webp"]):
        tags.append("images")
    if any(k in name for k in ["vid", "mp4", "youtube", "transcribe", "audio", "mp3"]):
        tags.append("media")
    if any(k in name for k in ["quiz", "quiz-talk", "quiztime"]):
        tags.append("quiz")
    if any(k in (name + parent) for k in ["instagram", "reddit", "bot"]):
        tags.append("bot")
    if p.suffix.lower() == ".py":
        tags.append("python")
    return sorted(set(tags))


def build_index() -> List[FileEntry]:
    entries: List[FileEntry] = []
    for p in iter_files(ROOT):
        rel = p.relative_to(ROOT)
        try:
            stat = p.stat()
        except OSError:
            continue
        ext = p.suffix.lower()
        kind = classify(p)
        project = guess_project(p)
        summary = None
        if ext == ".py":
            try:
                with p.open("r", encoding="utf-8", errors="ignore") as fh:
                    first = fh.readline().strip()
                    if first.startswith("#!"):
                        summary = first
                    else:
                        # Try to capture a simple first docstring line
                        # Read a bit more to find opening triple quotes
                        head = first + "\n" + fh.read(1024)
                        for quote in ("\"\"\"", "'''"):
                            if quote in head:
                                start = head.find(quote) + len(quote)
                                rest = head[start:]
                                line = rest.strip().splitlines()[0] if rest else ""
                                if line:
                                    summary = f"doc: {line[:200]}"
                                break
            except Exception:
                pass
        entry = FileEntry(
            path=str(rel),
            name=p.name,
            ext=ext,
            size=stat.st_size,
            mtime=stat.st_mtime,
            kind=kind,
            project=project,
            tags=tag_for(p),
            summary=summary,
        )
        entries.append(entry)
    return entries


def write_csv(entries: List[FileEntry], dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "path",
        "name",
        "ext",
        "size",
        "mtime",
        "kind",
        "project",
        "tags",
        "summary",
    ]
    with dest.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for e in entries:
            row: Dict[str, str] = asdict(e)
            row["tags"] = ",".join(e.tags)
            if row.get("summary") is None:
                row["summary"] = ""
            writer.writerow(row)


def write_json(entries: List[FileEntry], dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", encoding="utf-8") as f:
        json.dump([asdict(e) for e in entries], f, indent=2)


def main() -> None:
    entries = build_index()
    write_csv(entries, ROOT / "python_index.csv")
    write_json(entries, ROOT / "python_index.json")
    print(f"Indexed {len(entries)} files -> python_index.csv, python_index.json")


if __name__ == "__main__":
    main()
