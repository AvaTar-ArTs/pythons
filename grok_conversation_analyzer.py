#!/usr/bin/env python3
"""
grok_conversation_analyzer.py
Analyze and summarize Grok AI conversation exports (.json format).

Usage:
    python grok_conversation_analyzer.py /path/to/grok/conversations/
    python grok_conversation_analyzer.py /path/to/single-export.json
    python grok_conversation_analyzer.py /path/to/folder --find-duplicates
"""

import argparse
import json
import hashlib
from pathlib import Path
from collections import Counter
from datetime import datetime


def load_export(filepath: Path) -> dict:
    """Load a Grok JSON export file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def content_hash(filepath: Path) -> str:
    """SHA256 hash of file content for deduplication."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def analyze_single(filepath: Path) -> dict:
    """Analyze a single Grok conversation export."""
    data = load_export(filepath)

    messages = data.get("conversation", [])
    stats = data.get("statistics", {})

    # Grok exports use "speaker" field with values "Human"/"Grok"
    # Also support "role" field for other export formats
    def get_speaker(m):
        return m.get("speaker", m.get("role", "")).lower()

    human_msgs = [m for m in messages if get_speaker(m) in ("human", "user")]
    grok_msgs = [m for m in messages if get_speaker(m) in ("grok", "assistant")]

    # Extract word counts
    human_words = sum(len(m.get("content", "").split()) for m in human_msgs)
    grok_words = sum(len(m.get("content", "").split()) for m in grok_msgs)

    # Extract code blocks from Grok responses
    code_blocks = 0
    for m in grok_msgs:
        content = m.get("content", "")
        code_blocks += content.count("```")
    code_blocks //= 2  # pairs of ```

    # Extract unique topics from human messages (first 50 words of each)
    prompts = []
    for m in human_msgs:
        text = m.get("content", "").strip()
        if text:
            prompts.append(text[:200])

    return {
        "file": filepath.name,
        "url": data.get("url", ""),
        "export_date": data.get("exportDate", ""),
        "message_count": data.get("messageCount", len(messages)),
        "human_messages": len(human_msgs),
        "grok_messages": len(grok_msgs),
        "human_words": human_words,
        "grok_words": grok_words,
        "code_blocks": code_blocks,
        "prompts": prompts,
    }


def find_duplicates(folder: Path) -> list[tuple[Path, Path]]:
    """Find duplicate files by content hash."""
    hashes: dict[str, list[Path]] = {}
    for f in folder.rglob("*.json"):
        h = content_hash(f)
        hashes.setdefault(h, []).append(f)

    duplicates = []
    for h, files in hashes.items():
        if len(files) > 1:
            for f in files[1:]:
                duplicates.append((files[0], f))
    return duplicates


def find_url_duplicates(folder: Path) -> list[tuple[str, list[Path]]]:
    """Find exports from the same conversation URL (different timestamps)."""
    url_map: dict[str, list[Path]] = {}
    for f in folder.rglob("*.json"):
        try:
            data = load_export(f)
            url = data.get("url", "").split("?")[0]  # strip rid param
            if url:
                url_map.setdefault(url, []).append(f)
        except (json.JSONDecodeError, KeyError):
            continue

    return [(url, files) for url, files in url_map.items() if len(files) > 1]


def print_report(analyses: list[dict]):
    """Print a formatted summary report."""
    print("=" * 72)
    print("GROK CONVERSATION ANALYSIS REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 72)

    total_msgs = sum(a["message_count"] for a in analyses)
    total_words = sum(a["human_words"] + a["grok_words"] for a in analyses)

    print(f"\nTotal conversations: {len(analyses)}")
    print(f"Total messages: {total_msgs}")
    print(f"Total words: {total_words:,}")
    print()

    for i, a in enumerate(analyses, 1):
        print(f"--- Conversation {i}: {a['file']} ---")
        print(f"  URL: {a['url']}")
        print(f"  Exported: {a['export_date']}")
        print(f"  Messages: {a['message_count']} ({a['human_messages']} human, {a['grok_messages']} grok)")
        print(f"  Words: {a['human_words']:,} human / {a['grok_words']:,} grok")
        print(f"  Code blocks: {a['code_blocks']}")
        print(f"  User prompts:")
        for p in a["prompts"][:5]:
            print(f"    - {p[:100]}{'...' if len(p) > 100 else ''}")
        if len(a["prompts"]) > 5:
            print(f"    ... and {len(a['prompts']) - 5} more")
        print()


def main():
    parser = argparse.ArgumentParser(description="Analyze Grok conversation exports")
    parser.add_argument("path", type=Path, help="JSON file or directory of exports")
    parser.add_argument("--find-duplicates", action="store_true", help="Find duplicate exports")
    parser.add_argument("--json-output", type=Path, help="Write analysis as JSON to file")
    args = parser.parse_args()

    if args.find_duplicates and args.path.is_dir():
        print("Content-identical files:")
        for original, dup in find_duplicates(args.path):
            print(f"  {dup.name} == {original.name}")

        print("\nSame-conversation exports (different timestamps):")
        for url, files in find_url_duplicates(args.path):
            print(f"  URL: {url}")
            for f in files:
                print(f"    - {f.name}")
        return

    files = []
    if args.path.is_dir():
        files = sorted(args.path.rglob("*.json"))
        md_files = sorted(args.path.rglob("*.md"))
    elif args.path.is_file():
        files = [args.path] if args.path.suffix == ".json" else []
        md_files = [args.path] if args.path.suffix == ".md" else []
    else:
        print(f"Error: {args.path} not found")
        return

    analyses = []
    for f in files:
        try:
            data = load_export(f)
            if "conversation" in data:
                analyses.append(analyze_single(f))
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Skipping {f.name}: {e}")

    if not analyses:
        print("No valid Grok conversation exports found.")
        return

    # Also analyze MD files for human prompt extraction
    md_stats = {}
    for mf in md_files:
        try:
            text = mf.read_text(encoding="utf-8")
            # Count ## Human and ## Grok sections
            human_sections = text.count("\n## Human\n") + text.count("\n## Grok\n")
            # Extract human prompts from MD
            prompts = []
            lines = text.split("\n")
            in_human = False
            current_prompt = []
            for line in lines:
                if line.strip() == "## Human":
                    if current_prompt:
                        prompts.append(" ".join(current_prompt).strip()[:200])
                    current_prompt = []
                    in_human = True
                elif line.startswith("## Grok") or line.startswith("## "):
                    if in_human and current_prompt:
                        prompts.append(" ".join(current_prompt).strip()[:200])
                    current_prompt = []
                    in_human = False
                elif in_human:
                    current_prompt.append(line.strip())
            if in_human and current_prompt:
                prompts.append(" ".join(current_prompt).strip()[:200])
            md_stats[mf.stem] = {
                "prompts": [p for p in prompts if p],
                "total_words": len(text.split()),
                "total_lines": len(lines),
            }
        except Exception:
            continue

    # Merge MD prompt data into JSON analyses where stems match
    for a in analyses:
        json_stem = Path(a["file"]).stem
        for md_stem, md_data in md_stats.items():
            if json_stem == md_stem:
                if md_data["prompts"] and len(md_data["prompts"]) > len(a["prompts"]):
                    a["prompts"] = md_data["prompts"]
                    a["human_messages"] = len(md_data["prompts"])
                a["total_lines"] = md_data["total_lines"]

    analyses.sort(key=lambda a: a["message_count"], reverse=True)
    print_report(analyses)

    if args.json_output:
        with open(args.json_output, "w", encoding="utf-8") as f:
            json.dump(analyses, f, indent=2, default=str)
        print(f"JSON output written to {args.json_output}")


if __name__ == "__main__":
    main()
