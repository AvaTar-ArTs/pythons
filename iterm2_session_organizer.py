#!/usr/bin/env python3
"""Safe, metadata-first organizer for iTerm2 and agent session exports.

The default mode is a read-only plan. Use --apply only after reviewing the
manifest. The script never sends transcript contents anywhere and records
only bounded structural probes plus secret-pattern counts.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

ITERM_TIMESTAMP = re.compile(
    r"iTerm2 Session (?P<month>[A-Za-z]{3}) (?P<day>\d{1,2}), (?P<year>\d{4})"
    r" at (?P<hour>\d{1,2}):(?P<minute>\d{2}):(?P<second>\d{2})\s*"
    r"(?P<ampm>AM|PM)",
    re.IGNORECASE,
)
CODEX_TIMESTAMP = re.compile(r"(?P<date>20\d{6})-(?P<time>\d{6})-codex-instance-export", re.I)
SECRET_PATTERNS = {
    "openai_api_key": re.compile(r"(?i)\b(?:openai[_ -]?api[_ -]?key|sk-(?:proj-)?[A-Za-z0-9_-]{12,})\b"),
    "github_token": re.compile(r"\bgh[opsu]_[A-Za-z0-9]{12,}\b"),
    "private_key": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    "authorization": re.compile(r"(?i)authorization:\s*bearer|x-api-key|client_secret"),
}


@dataclass
class Record:
    source: str
    destination: str
    kind: str
    size_bytes: int
    sha256: str
    timestamp: str | None
    secret_pattern_counts: dict[str, int]
    status: str


def parse_export_timestamp(name: str) -> str | None:
    match = ITERM_TIMESTAMP.search(name)
    if match:
        try:
            hour = int(match.group("hour")) % 12
            if match.group("ampm").lower() == "pm":
                hour += 12
            value = datetime.strptime(
                f"{match.group('year')} {match.group('month')} {match.group('day')} "
                f"{hour:02d}:{match.group('minute')}:{match.group('second')}",
                "%Y %b %d %H:%M:%S",
            )
            return value.isoformat(timespec="seconds")
        except ValueError:
            return None
    match = CODEX_TIMESTAMP.search(name)
    if match:
        try:
            value = datetime.strptime(match.group("date") + match.group("time"), "%Y%m%d%H%M%S")
            return value.isoformat(timespec="seconds")
        except ValueError:
            return None
    return None


def classify_file(path: Path) -> str:
    name = path.name.lower()
    if "codex-instance-export" in name:
        return "codex-export"
    if name.startswith("iterm2 session ") and path.suffix.lower() == ".txt":
        return "iterm2-session"
    return "text-export" if path.suffix.lower() in {".txt", ".md", ".json", ".log"} else "file"


def short_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()[:8]


def probe_secret_patterns(path: Path, probe_bytes: int = 65536) -> dict[str, int]:
    size = path.stat().st_size
    with path.open("rb") as handle:
        head = handle.read(probe_bytes)
        tail = b""
        if size > probe_bytes:
            handle.seek(max(0, size - 16384))
            tail = handle.read(16384)
    text = (head + b"\n" + tail).decode("utf-8", errors="replace")
    return {name: len(pattern.findall(text)) for name, pattern in SECRET_PATTERNS.items()}


def sanitize_component(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-")
    return value or "Unknown"


def safe_destination_name(path: Path, kind: str, timestamp: str | None, digest: str) -> str:
    suffix = path.suffix.lower() or ".dat"
    if timestamp:
        date_part, time_part = timestamp.split("T", 1)
        time_part = time_part.replace(":", "")
        time_part = f"{time_part[:4]}-{time_part[4:]}"
        prefix = {"iterm2-session": "iTerm2-Session", "codex-export": "Codex-Instance-Export"}.get(kind, "Session-Export")
        return f"{prefix}-{date_part}-{time_part}-{digest}{suffix}"
    prefix = {"iterm2-session": "iTerm2-Session", "codex-export": "Codex-Instance-Export"}.get(kind, "Session-Export")
    return f"{prefix}-{sanitize_component(path.stem)}-{digest}{suffix}"


def allocate_destinations(items: list[tuple[Path, str]]) -> list[Path]:
    reserved: set[Path] = set()
    result: list[Path] = []
    for source, name in items:
        candidate = source.parent / name
        stem, suffix = candidate.stem, candidate.suffix
        counter = 2
        while candidate.exists() and candidate.resolve() != source.resolve() or candidate.resolve() in reserved:
            candidate = source.parent / f"{stem}-{counter:02d}{suffix}"
            counter += 1
        reserved.add(candidate.resolve())
        result.append(candidate)
    return result


def iter_files(root: Path, recursive: bool) -> Iterable[Path]:
    paths = root.rglob("*") if recursive else root.iterdir()
    for path in sorted(paths, key=lambda item: str(item).casefold()):
        if path.is_file() and not path.name.startswith("."):
            yield path


def build_plan(root: Path, recursive: bool = False) -> list[Record]:
    sources = list(iter_files(root, recursive))
    proposed: list[tuple[Path, str]] = []
    details: list[tuple[Path, str, str | None, str, dict[str, int]]] = []
    for source in sources:
        kind = classify_file(source)
        timestamp = parse_export_timestamp(source.name)
        digest = short_hash(source)
        counts = probe_secret_patterns(source)
        destination = safe_destination_name(source, kind, timestamp, digest)
        proposed.append((source, destination))
        details.append((source, kind, timestamp, digest, counts))
    destinations = allocate_destinations(proposed)
    records: list[Record] = []
    for (source, _), destination, (_, kind, timestamp, digest, counts) in zip(proposed, destinations, details):
        status = "unchanged" if destination.resolve() == source.resolve() else "planned"
        records.append(Record(str(source), str(destination), kind, source.stat().st_size, digest, timestamp, counts, status))
    return records


def write_reports(records: list[Record], manifest_path: Path, csv_path: Path, markdown_path: Path) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"schema": "iterm2-session-organizer/v1", "records": [asdict(record) for record in records]}
    manifest_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        rows = [asdict(record) for record in records]
        fieldnames = list(rows[0]) if rows else ["source", "destination", "kind", "size_bytes", "sha256", "timestamp", "secret_pattern_counts", "status"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            row["secret_pattern_counts"] = json.dumps(row["secret_pattern_counts"], sort_keys=True)
            writer.writerow(row)
    lines = ["# iTerm2 Session Organizer Plan", "", "| Status | Kind | Source | Destination | Timestamp | Size | Secret-pattern counts |", "|---|---|---|---|---|---:|---|"]
    for record in records:
        counts = ", ".join(f"{key}={value}" for key, value in record.secret_pattern_counts.items() if value) or "none detected in bounded probe"
        lines.append(f"| {record.status} | {record.kind} | `{record.source}` | `{record.destination}` | {record.timestamp or 'unknown'} | {record.size_bytes} | {counts} |")
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def apply_records(records: list[Record]) -> None:
    planned = [record for record in records if record.status == "planned"]
    staged: list[tuple[Path, Path]] = []
    try:
        for record in planned:
            source = Path(record.source)
            temporary = source.with_name(f".{source.name}.organizing-{short_hash(source)}")
            counter = 2
            while temporary.exists():
                temporary = source.with_name(f".{source.name}.organizing-{short_hash(source)}-{counter}")
                counter += 1
            source.rename(temporary)
            staged.append((temporary, source))
        for record, (temporary, source) in zip(planned, staged):
            destination = Path(record.destination)
            temporary.rename(destination)
            record.status = "applied"
    except Exception:
        for temporary, source in reversed(staged):
            if temporary.exists():
                temporary.rename(source)
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Metadata-first iTerm2 session export organizer")
    parser.add_argument("root", type=Path, help="directory containing exports")
    parser.add_argument("--recursive", action="store_true", help="scan nested directories")
    parser.add_argument("--apply", action="store_true", help="perform planned renames; default is read-only")
    parser.add_argument("--manifest", type=Path, help="JSON manifest path")
    parser.add_argument("--csv", type=Path, help="CSV report path")
    parser.add_argument("--markdown", type=Path, help="Markdown report path")
    args = parser.parse_args(argv)
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    records = build_plan(root, args.recursive)
    if args.apply:
        apply_records(records)
    if args.manifest or args.csv or args.markdown:
        prefix = args.manifest or root.parent / "iterm2-session-organizer-manifest.json"
        manifest = prefix
        csv_path = args.csv or prefix.with_suffix(".csv")
        markdown = args.markdown or prefix.with_suffix(".md")
        write_reports(records, manifest, csv_path, markdown)
        print(json.dumps({"manifest": str(manifest), "csv": str(csv_path), "markdown": str(markdown)}, indent=2))
    print(json.dumps({"root": str(root), "records": len(records), "planned": sum(r.status == 'planned' for r in records), "applied": sum(r.status == 'applied' for r in records), "mode": "apply" if args.apply else "dry-run"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
