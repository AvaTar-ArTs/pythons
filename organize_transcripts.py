#!/usr/bin/env python3
"""One-time organizer for ~/agent-transcripts: flat dated layout + YAML headers."""

from __future__ import annotations

import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/Users/steven/agent-transcripts")
SESSIONS = ROOT / "sessions"
LEGACY_GLOBS = ["agent-transcripts", "agent-transcripts *"]


def is_legacy_transcript_path(p: Path) -> bool:
    rel = p.relative_to(ROOT)
    parts = rel.parts
    if len(parts) < 2:
        return False
    parent = parts[0]
    if parent == "sessions" or parent == "tools":
        return False
    return parent == "agent-transcripts" or parent.startswith("agent-transcripts ")


def format_header(
    *,
    session_id: str,
    source_relative: str,
    mtime_iso: str,
    size_bytes: int,
) -> str:
    return (
        "---\n"
        f'agent_transcript: true\n'
        f'session_id: "{session_id}"\n'
        f"organized_utc: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n"
        f'source_path: "{source_relative}"\n'
        f"file_mtime_utc: {mtime_iso}\n"
        f"size_bytes: {size_bytes}\n"
        "---\n\n"
    )


def month_key(st: os.stat_result) -> str:
    dt = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
    return dt.strftime("%Y-%m")


def main() -> int:
    ROOT.mkdir(parents=True, exist_ok=True)
    SESSIONS.mkdir(parents=True, exist_ok=True)

    sources = [
        p
        for p in ROOT.rglob("*.txt")
        if p.is_file() and is_legacy_transcript_path(p)
    ]
    sources.sort(key=lambda p: str(p))

    moved: list[tuple[str, str, int]] = []
    for src in sources:
        st = src.stat()
        body = src.read_text(encoding="utf-8", errors="replace")
        if body.startswith("---\n") and "agent_transcript:" in body[:400]:
            # Already formatted; still move if in legacy folder
            header = ""
            rest = body
        else:
            m = re.match(
                r"^([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
                src.stem,
                re.I,
            )
            session_id = m.group(1) if m else src.stem
            mtime_iso = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
            rel_old = str(src.relative_to(ROOT))
            header = format_header(
                session_id=session_id,
                source_relative=rel_old,
                mtime_iso=mtime_iso,
                size_bytes=st.st_size,
            )
            rest = body
            if not rest.endswith("\n"):
                rest += "\n"
        mk = month_key(st)
        dest_dir = SESSIONS / mk
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / src.name
        if dest.exists():
            if dest.stat().st_size == len((header + rest).encode("utf-8")) or (
                header == "" and dest.stat().st_size == st.st_size
            ):
                src.unlink(missing_ok=True)
                continue
        out = header + rest if header else body
        dest.write_text(out, encoding="utf-8", newline="\n")
        if dest.stat().st_size < 10:
            raise SystemExit(f"Write failed short: {dest}")
        src.unlink()
        moved.append((str(src.relative_to(ROOT)), str(dest.relative_to(ROOT)), st.st_size))

    # Remove empty legacy dirs
    for pattern in LEGACY_GLOBS:
        for d in ROOT.glob(pattern):
            if not d.is_dir():
                continue
            for sub in sorted(d.rglob("*"), reverse=True):
                if sub.is_file():
                    continue
                try:
                    sub.rmdir()
                except OSError:
                    pass
            try:
                d.rmdir()
            except OSError:
                pass

    # INDEX.md
    index_lines = [
        "# Agent transcripts index",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "Layout: `sessions/YYYY-MM/<session-uuid>.txt`",
        "",
        "| Month | File | Size (bytes) |",
        "|-------|------|--------------|",
    ]
    for p in sorted(SESSIONS.rglob("*.txt")):
        rel = p.relative_to(ROOT)
        sz = p.stat().st_size
        index_lines.append(f"| `{rel.parts[1]}` | `{p.name}` | {sz} |")
    index_lines.append("")
    (ROOT / "INDEX.md").write_text("\n".join(index_lines), encoding="utf-8")

    readme = """# agent-transcripts

Exported Cursor (and similar) agent sessions.

## Layout

- `sessions/YYYY-MM/<uuid>.txt` — one file per session, sorted by **file modification time** month (UTC).
- Each transcript starts with **YAML front matter** (`agent_transcript`, `session_id`, `source_path`, etc.).
- `INDEX.md` — table of all files.
- `tools/organize_transcripts.py` — re-run if you add legacy `agent-transcripts N/` folders again.

## Legacy folders

Older batches (`agent-transcripts/`, `agent-transcripts 2/`, …) were collapsed into `sessions/`; names are unchanged (`<uuid>.txt`).
"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")

    print(f"Processed legacy sources: {len(sources)}")
    print(f"Moved/rewrote: {len(moved)}")
    print(f"INDEX.md and README.md updated under {ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
