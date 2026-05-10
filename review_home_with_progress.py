import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Deep-dive review of ~/ with progress (ASCII + emoji) as it runs.
"""
import os
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
EMOJI = {"pending": "⏳", "spin": "🔄", "ok": "✅", "folder": "📁", "file": "📄", "bar_fill": "█", "bar_empty": "░"}


def log(msg, icon="  "):
    print(f"{icon} {msg}", flush=True)


def run(cmd, capture=True):
    r = subprocess.run(cmd, shell=True, capture_output=capture, text=True, timeout=300)
    return (r.stdout or "").strip() if capture else r.returncode


def main():
    print("\n" + "=" * 50)
    log("Deep-dive review: " + str(HOME), EMOJI["folder"])
    print("=" * 50 + "\n")

    # 1. Count directories
    log("Counting directories (unlimited depth)...", EMOJI["pending"])
    out = run("find " + str(HOME) + " -type d 2>/dev/null | wc -l")
    n_dirs = int(out.split()[0]) if out else 0
    log(f"Directories: {n_dirs:,}", EMOJI["ok"])
    print()

    # 2. Count files
    log("Counting files (unlimited depth)...", EMOJI["pending"])
    out = run("find " + str(HOME) + " -type f 2>/dev/null | wc -l")
    n_files = int(out.split()[0]) if out else 0
    log(f"Files: {n_files:,}", EMOJI["ok"])
    print()

    # 3. Total size
    log("Computing total size...", EMOJI["pending"])
    out = run("du -sh " + str(HOME) + " 2>/dev/null")
    size_line = out.split("\n")[-1].strip() if out else "?"
    log(f"Total size: {size_line}", EMOJI["ok"])
    print()

    # 4. Top-level listing (first 80)
    log("Listing top-level children...", EMOJI["spin"])
    children = sorted(HOME.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    for p in children[:80]:
        icon = EMOJI["folder"] if p.is_dir() else EMOJI["file"]
        log(p.name, icon)
    if len(children) > 80:
        log(f"... and {len(children) - 80} more", "  ")
    print()

    # 5. Top-level sizes (one du for first 30 dirs)
    log("Top-level sizes (first 30 dirs)...", EMOJI["pending"])
    dirs_only = [str(p) for p in children if p.is_dir()][:30]
    if dirs_only:
        out = run("du -sh " + " ".join(f"'{d}'" for d in dirs_only) + " 2>/dev/null | sort -hr")
        if out:
            for line in out.split("\n"):
                log(line, EMOJI["folder"])
    print()

    log("Review complete.", EMOJI["ok"])
    print()


try:
        main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)