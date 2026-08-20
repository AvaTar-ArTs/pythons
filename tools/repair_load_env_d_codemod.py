#!/usr/bin/env python3
"""Repair the bad load_env_d codemod across ~/pythons top-level scripts.

Two idempotent transforms:
  A) Ensure `import os` exists immediately after the injected anchor comment,
     so the top load_env_d() block (which uses os) doesn't crash on import.
  B) Remove the orphaned duplicate fragment the codemod left behind:
         # Load API keys from ~/.env.d/
         from pathlib import Path as PathLib

             for env_file in env_dir.glob("*.env"):
                 load_dotenv(env_file)

Usage:
    repair_codemod.py --check FILE...     # report, do not modify
    repair_codemod.py FILE...             # apply in place
"""
from __future__ import annotations

import sys

ANCHOR = "# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)"
SHORT = "# Load API keys from ~/.env.d/"


def repair(lines: list[str]) -> tuple[list[str], bool, bool]:
    """Return (new_lines, removed_fragment, inserted_import)."""
    removed_fragment = False
    inserted_import = False

    # --- Transform B: remove orphaned duplicate fragment ---
    out: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        stripped = lines[i].strip()
        if stripped == SHORT:  # short form only; full anchor won't match
            window = [l.rstrip("\n") for l in lines[i : i + 6]]
            if (
                len(window) >= 5
                and window[1].strip() == "from pathlib import Path as PathLib"
                and any("for env_file in env_dir.glob" in w for w in window[2:5])
            ):
                end = i
                for k in range(i, min(i + 6, n)):
                    if "load_dotenv(env_file)" in lines[k]:
                        end = k
                        break
                i = end + 1
                # swallow up to two trailing blank lines left behind
                blanks = 0
                while i < n and lines[i].strip() == "" and blanks < 2:
                    i += 1
                    blanks += 1
                removed_fragment = True
                continue
        out.append(lines[i])
        i += 1
    lines = out

    # --- Transform C: remove the orphaned 2-line env_dir loop variant ---
    # Some files got a bare orphan (no PathLib line):
    #     load_dotenv(Path.home() / ".env")
    #         for env_file in env_dir.glob("*.env"):   <- unexpected indent
    #             load_dotenv(env_file)
    # Guard: only strip it when the preceding non-blank line is at column 0 and
    # is NOT a block opener (doesn't end with ':'), which marks it as an orphan
    # rather than a legitimate in-function loop.
    out = []
    i = 0
    n = len(lines)
    while i < n:
        if (
            lines[i].startswith("    for env_file in env_dir.glob")
            and i + 1 < n
            and lines[i + 1].lstrip().startswith("load_dotenv(env_file)")
        ):
            prev = next((out[k] for k in range(len(out) - 1, -1, -1) if out[k].strip()), "")
            prev_s = prev.rstrip("\n")
            if prev_s and not prev_s.startswith((" ", "\t")) and not prev_s.rstrip().endswith(":"):
                i += 2
                removed_fragment = True
                continue
        out.append(lines[i])
        i += 1
    lines = out

    # --- Transform A: ensure `import os` right after the anchor comment ---
    for idx, l in enumerate(lines):
        if l.strip() == ANCHOR:
            if idx + 1 < len(lines) and lines[idx + 1].strip() == "import os":
                break  # already fixed
            lines.insert(idx + 1, "import os\n")
            inserted_import = True
            break

    return lines, removed_fragment, inserted_import


def main(argv: list[str]) -> int:
    check = False
    files = []
    for a in argv:
        if a == "--check":
            check = True
        else:
            files.append(a)

    for path in files:
        with open(path, encoding="utf-8") as f:
            original = f.readlines()
        new, rem, ins = repair(list(original))
        tag = []
        if rem:
            tag.append("removed-fragment")
        if ins:
            tag.append("inserted-import-os")
        label = ",".join(tag) if tag else "no-change"
        print(f"{path}: {label}")
        if not check and (rem or ins):
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(new)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
