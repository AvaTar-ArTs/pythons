#!/usr/bin/env python3
"""
Estimate tokens (and rough USD) for a batch of prompts before calling an API.
Unique SKU: buyers fear runaway LLM bills; few sell a tiny CLI focused on *budget*.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

# Default $ per 1M tokens (adjust for your listing / current OpenAI pricing)
DEFAULT_PRICES = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
}


def rough_tokens(text: str) -> int:
    """Fallback when tiktoken unavailable: ~4 chars per token (rough)."""
    if not text:
        return 0
    return max(1, int(len(text) / 4))


def count_tokens_tiktoken(text: str, model_hint: str = "gpt-4o-mini") -> int:
    try:
        import tiktoken

        enc = tiktoken.encoding_for_model(model_hint)
    except Exception:
        try:
            import tiktoken

            enc = tiktoken.get_encoding("cl100k_base")
        except Exception:
            return rough_tokens(text)
    return len(enc.encode(text))


def load_prompts(path: Path) -> list[str]:
    suf = path.suffix.lower()
    if suf == ".jsonl":
        out: list[str] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            p = obj.get("prompt") or obj.get("text") or ""
            if p:
                out.append(str(p))
        return out
    return [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Estimate input tokens per prompt and rough cost across models."
    )
    p.add_argument("prompts_file", type=Path, help=".txt (one prompt per line) or .jsonl")
    p.add_argument(
        "-m",
        "--model-hint",
        default="gpt-4o-mini",
        help="Model name for tiktoken encoding hint",
    )
    p.add_argument(
        "--output-ratio",
        type=float,
        default=0.25,
        help="Assume output tokens = input * ratio for cost estimate (default 0.25)",
    )
    p.add_argument("-o", "--csv-out", type=Path, help="Write per-row estimates CSV")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if not args.prompts_file.is_file():
        print(f"Not found: {args.prompts_file}", file=sys.stderr)
        return 1

    prompts = load_prompts(args.prompts_file)
    rows: list[dict[str, object]] = []
    total_in = 0
    for i, pr in enumerate(prompts):
        toks = count_tokens_tiktoken(pr, args.model_hint)
        total_in += toks
        rows.append({"index": i, "input_tokens": toks, "preview": pr[:120]})

    ratio = args.output_ratio
    print(f"Prompts: {len(prompts)}  Total input tokens (est.): {total_in}")
    print(f"Assumed output tokens: {int(total_in * ratio)} (input × {ratio})")
    print()
    for model, rates in DEFAULT_PRICES.items():
        tin_m = total_in / 1_000_000
        tout_m = (total_in * ratio) / 1_000_000
        usd = tin_m * rates["input"] + tout_m * rates["output"]
        print(f"  {model}: ~${usd:.4f} USD (table defaults; verify current API pricing)")

    if args.csv_out:
        args.csv_out.parent.mkdir(parents=True, exist_ok=True)
        with args.csv_out.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(
                fh, fieldnames=["index", "input_tokens", "preview"]
            )
            w.writeheader()
            w.writerows(rows)
        print(f"\nWrote {args.csv_out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
