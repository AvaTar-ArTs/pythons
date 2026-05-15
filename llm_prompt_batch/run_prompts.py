#!/usr/bin/env python3
"""
Batch-run prompts from a file (one prompt per line, or JSONL with \"prompt\" field).
Gap: many want \"run many OpenAI prompts from file\"—market is fragmented tutorials.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def load_prompts(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lines = [ln.strip() for ln in text.splitlines()]
    # Skip empty lines
    return [ln for ln in lines if ln]


def load_jsonl(path: Path) -> list[str]:
    out: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        p = obj.get("prompt") or obj.get("text")
        if not p:
            raise ValueError(f"JSONL row missing 'prompt' or 'text': {line[:80]}")
        out.append(str(p))
    return out


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Batch LLM prompts from a file.")
    p.add_argument(
        "input_file",
        type=Path,
        help=".txt (one prompt per line) or .jsonl ({\"prompt\": \"...\"})",
    )
    p.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("batch_results.jsonl"),
        help="Append JSONL results here",
    )
    p.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="OpenAI model id",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not call API; print planned prompts only",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if not args.input_file.is_file():
        print(f"Not found: {args.input_file}", file=sys.stderr)
        return 1

    suffix = args.input_file.suffix.lower()
    if suffix == ".jsonl":
        prompts = load_jsonl(args.input_file)
    else:
        prompts = load_prompts(args.input_file)

    if args.dry_run:
        for i, pr in enumerate(prompts):
            print(f"[{i}] {pr[:120]}{'...' if len(pr) > 120 else ''}")
        print(f"Dry run: {len(prompts)} prompts (no API calls)")
        return 0

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Set OPENAI_API_KEY or use --dry-run", file=sys.stderr)
        return 2

    try:
        from openai import OpenAI
    except ImportError:
        print("pip install openai", file=sys.stderr)
        return 3

    client = OpenAI(api_key=api_key)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("a", encoding="utf-8") as fh:
        for i, prompt in enumerate(prompts):
            resp = client.chat.completions.create(
                model=args.model,
                messages=[{"role": "user", "content": prompt}],
            )
            text = resp.choices[0].message.content or ""
            row = {"index": i, "prompt": prompt, "response": text, "model": args.model}
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(f"OK [{i+1}/{len(prompts)}]")

    print(f"Appended -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
