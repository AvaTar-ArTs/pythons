"""
Youtube Is Section Header

This module provides functionality for youtube is section header.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_130 = 130

#!/usr/bin/env python3
"""
env_wizard.py — Interactive .env builder with sections & per-entry save

Enhancements vs classic version:
- **Per-entry save**: after each variable, we write+flush to the output file (crash-safe).
- **Section-aware**: detects comment "sections" and lets you skip/process per section.
- **Backups**: backs up an existing output file before writing.
- **Resume options**: --start-from VAR keeps prior behavior. New: --assume-yes to skip section prompts.

Expected template line format:
  VAR_NAME=                # https://example.com/keys-or-docs
Comments & blank lines are preserved verbatim.

Usage:
  python3 env_wizard.py --template .env.template --out .env
Common flags:
  -t / --template     Path to the .env template (default: .env.template)
  -o / --out          Path to write the resulting .env (default: .env)
  -s / --start-from   Start from this VAR_NAME (skip preceding vars)
  -n / --dry-run      Preview only; do not write output
  --no-open           Do not offer to open URLs in a browser
  --force             Re-prompt even if a value exists
  --assume-yes        Auto-accept all section prompts (process all sections)
"""
import argparse
import datetime as dt
import os
import re
import sys
import shutil
import webbrowser
from getpass import getpass
from pathlib import Path
from typing import Optional, Tuple

VAR_LINE_RE = re.compile(r'^([A-Z0-9_]+)\s*=\s*(.*?)\s*(?:#\s*(\S.*))?$')

def is_section_header(line: str) -> bool:
    s = line.strip()
    if not s.startswith('#'):
        return False
    # Treat any comment line with 5 or more '=' as a section delimiter,
    # or containing emoji bullets like 🌐 🖼️ 🎵 🤖 📈 ☁️ 🔔 🗂️ 💼 🛠️ etc.
    return ('=====' in s) or any(em in s for em in ['🌐','🖼️','🎵','🤖','📈','☁️','🔔','🗂️','💼','🛠️'])
def section_name_from_header(line: str) -> str:
    s = line.strip('# ').strip()
    # Extract between emojis or after the hashes; keep as-is if simple
    return s
def mask_value(v: str, show=2) -> str:
    if not v:
        return ''
    if len(v) <= show*2:
        return '*'*len(v)
    return v[:show] + '*'*(len(v)-2*show) + v[-show:]

def normalize_value(v: str) -> str:
    v = v.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        v = v[1:-1]
    return v
def needs_quoting(v: str) -> bool:
    return any(c in v for c in [' ', '#', '\t', '\n', '\r'])
def serialize_value(v: str) -> str:
    v_escaped = v.replace("'", r"'\''")
    return f"'{v_escaped}'" if needs_quoting(v) else v

def parse_line(line: str) -> Optional[Tuple[str, str, str]]:
    m = VAR_LINE_RE.match(line.strip())
    if not m:
        return None
    var, val, comment = m.group(1).strip(), m.group(2).strip(), (m.group(3) or '').strip()
    return var, normalize_value(val), comment

def prompt_yes_no(prompt: str, default: bool = False) -> bool:
    default_str = 'Y/n' if default else 'y/N'
    while True:
        ans = input(f"{prompt} [{default_str}]: ").strip().lower()
        if ans == '' and default is not None:
            return default
        if ans in ('y', 'yes'):
            return True
        if ans in ('n', 'no'):
            return False
        logger.info("Please answer y/n.")

def prompt_secret(var: str, existing: Optional[str]=None) -> str:
    logger.info(f"Enter value for {var} (input hidden).")
    if existing:
        logger.info(f"Press ENTER to keep current value ({mask_value(existing)}).")
    while True:
        val = getpass(f"{var} = ")
        if val == '' and existing is not None:
            return existing
        if val != '':
            return val
        logger.info("Empty value. Enter a value, or CTRL+C to abort.")

def open_url(url: str):
    try:
        webbrowser.open(url)
    except Exception as e:
        logger.info(f"Could not open browser: {e}")

def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument('--template', '-t', default='.env.template')
    ap.add_argument('--out', '-o', default='.env')
    ap.add_argument('--start-from', '-s', default=None, dest='start_from')
    ap.add_argument('--dry-run', '-n', action='store_true', dest='dry_run')
    ap.add_argument('--no-open', action='store_true', dest='no_open')
    ap.add_argument('--force', action='store_true', dest='force')
    ap.add_argument('--assume-yes', action='store_true', dest='assume_yes')
    ap.add_argument('--help', '-h', action='help')
    args = ap.parse_args()

    template_path = Path(args.template)
    out_path = Path(args.out)

    if not template_path.exists():
        logger.info(f"Template not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    lines = template_path.read_text(encoding='utf-8').splitlines(keepends=False)

    logger.info(f"Using template: {template_path}")
    logger.info(f"Output file:    {out_path} {'(dry-run)' if args.dry_run else ''}")
    logger.info("-"*60)

    # Prepare writer
    fout = None
    if not args.dry_run:
        # Backup if exists
        if out_path.exists():
            ts = dt.datetime.now().strftime('%Y%m%d-%H%M%S')
            backup = out_path.with_suffix(out_path.suffix + f'.bak-{ts}')
            shutil.copyfile(out_path, backup)
            logger.info(f"Existing {out_path} backed up to {backup}")
        # Truncate/create
        fout = open(out_path, 'w', encoding='utf-8')

    started = args.start_from is None
    current_section = None

    def write_line(line: str):
        """Write a single line immediately and flush/sync for safety."""
        if args.dry_run:
            return
        fout.write(line + '\n')
        fout.flush()
        os.fsync(fout.fileno())

    i = 0
    while i < len(lines):
        orig_line = lines[i]
        stripped = orig_line.strip()

        # Section detection / header passthrough
        if stripped.startswith('#'):
            if is_section_header(orig_line):
                current_section = section_name_from_header(orig_line)
                # print header and ask if we process this section (unless assume-yes)
                logger.info(Path("\n") + stripped)
                if not args.assume_yes:
                    if not prompt_yes_no(f"Process section: {current_section}?", default=True):
                        # If skipping, we still write the header and pass through all lines
                        # until the next section or EOF without prompts.
                        write_line(orig_line)
                        i += 1
                        while i < len(lines):
                            nxt = lines[i]
                            write_line(nxt)
                            if nxt.strip().startswith('#') and is_section_header(nxt):
                                # We'll re-handle this header on next loop iteration
                                break
                            i += 1
                        continue
            # Write comment lines verbatim
            write_line(orig_line)
            i += 1
            continue

        # Preserve blank lines
        if stripped == '':
            write_line(orig_line)
            i += 1
            continue

        parsed = parse_line(orig_line)
        if not parsed:
            # Unknown line structure; write as-is
            write_line(orig_line)
            i += 1
            continue

        var, val, comment = parsed

        if not started:
            if var == args.start_from:
                started = True
            else:
                # before start point
                write_line(orig_line)
                i += 1
                continue

        url = ''
        if comment:
            url = comment.split()[0]

        logger.info(f"\n== {var} ==")
        if val and not args.force:
            logger.info(f"Current value: {mask_value(val)}")
            # Keep existing?
            keep = prompt_yes_no("Keep existing value?", default=True)
            if keep:
                line = f"{var}={serialize_value(val)}" + (f"  # {comment}" if comment else "")
                write_line(line)
                i += 1
                continue

        if not val:
            logger.info("No value set.")
        if url and not args.no_open:
            if prompt_yes_no(f"Open link to manage this key? {url}", default=False):
                open_url(url)

        # Prompt user
        new_val = prompt_secret(var, existing=val if (val and not args.force) else None)
        line = f"{var}={serialize_value(new_val)}" + (f"  # {comment}" if comment else "")
        write_line(line)
        i += 1

    if not args.dry_run and fout:
        fout.close()
        logger.info(f"\nSaved {out_path}. All entries were written as you went.")
        logger.info("Done.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nAborted by user.")
        sys.exit(CONSTANT_130)
