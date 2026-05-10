#!/usr/bin/env python3
"""
find_scattered_pythons.py
Finds Python files scattered outside ~/pythons/ and categorizes them
for potential consolidation.

Usage:
    python find_scattered_pythons.py                    # Full scan with report
    python find_scattered_pythons.py --csv output.csv   # Export to CSV
    python find_scattered_pythons.py --move-candidates  # Show files safe to move
"""

import argparse
import csv
import os
from pathlib import Path
from datetime import datetime

HOME = Path.home()
PYTHONS_DIR = HOME / "pythons"

# Directories to skip entirely (framework installs, venvs, system)
SKIP_PATTERNS = {
    ".venv", "venv", "__pycache__", ".git", "node_modules",
    "site-packages", "google-cloud-sdk", ".local", ".pyenv",
    ".Trash", ".cache", "Library", ".harbor", ".claude",
    ".npm", ".cargo", ".bun",
}

# Known project directories (have their own structure, don't consolidate)
PROJECT_DIRS = {
    "AutoTagger",       # Complete project with versions
    "maigret",          # Third-party tool
    "IntelliHub",       # Standalone project
    "AVATARARTS_ENTERPRISE",
}

# Directories with cloned repos (not user scripts)
CLONED_REPO_INDICATORS = {
    "setup.py", "setup.cfg", "pyproject.toml", ".github",
    "LICENSE", "MANIFEST.in",
}


def should_skip(path: Path) -> bool:
    """Check if path should be excluded from results."""
    parts = set(path.parts)
    return bool(parts & SKIP_PATTERNS)


def is_cloned_repo(dirpath: Path) -> bool:
    """Check if a directory appears to be a cloned GitHub repo."""
    if not dirpath.is_dir():
        return False
    contents = {p.name for p in dirpath.iterdir()}
    return len(contents & CLONED_REPO_INDICATORS) >= 2


def classify_file(filepath: Path) -> str:
    """Classify a Python file into a category."""
    rel = filepath.relative_to(HOME)
    parts = rel.parts

    if len(parts) == 1:
        return "home-root"

    top_dir = parts[0]

    if top_dir in PROJECT_DIRS:
        return f"project:{top_dir}"

    if top_dir == "AVATARARTS":
        sub = parts[1] if len(parts) > 1 else ""
        if sub == "TEMP_CLEANUP":
            return "avatararts:temp-cleanup"
        if sub == "Automations":
            return "avatararts:automations"
        if sub == "pythons":
            return "avatararts:pythons-copy"
        return f"avatararts:{sub or 'root'}"

    if top_dir in ("Documents", "Downloads", "Movies", "Pictures", "Music"):
        return f"media-docs:{top_dir}"

    if top_dir == ".env.d":
        return "env-utils"

    if top_dir == "clean":
        return "cleanup-scripts"

    return f"other:{top_dir}"


def get_file_purpose(filepath: Path) -> str:
    """Read first few lines to determine purpose."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= 15:
                    break
                lines.append(line)

        text = "".join(lines)

        # Check for docstring
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('"""') or stripped.startswith("'''"):
                return stripped.strip("\"' \n")[:80]
            if stripped.startswith("#") and len(stripped) > 5 and not stripped.startswith("#!"):
                return stripped.lstrip("# ").strip()[:80]

        # Fall back to filename-based description
        name = filepath.stem.replace("_", " ").replace("-", " ")
        return f"({name})"

    except Exception:
        return "(unreadable)"


def scan_home(max_depth: int = 7) -> list[dict]:
    """Scan home directory for Python files outside ~/pythons/."""
    results = []

    for root, dirs, files in os.walk(HOME):
        root_path = Path(root)

        # Respect max depth
        depth = len(root_path.relative_to(HOME).parts)
        if depth > max_depth:
            dirs.clear()
            continue

        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in SKIP_PATTERNS]

        # Skip pythons directory itself
        if root_path == PYTHONS_DIR or PYTHONS_DIR in root_path.parents:
            dirs.clear()
            continue

        for fname in files:
            if not fname.endswith(".py"):
                continue

            filepath = root_path / fname
            if should_skip(filepath):
                continue

            try:
                stat = filepath.stat()
            except (OSError, FileNotFoundError):
                continue

            category = classify_file(filepath)

            results.append({
                "path": str(filepath),
                "relative": str(filepath.relative_to(HOME)),
                "name": fname,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d"),
                "category": category,
                "purpose": get_file_purpose(filepath),
            })

    return results


def print_report(results: list[dict]):
    """Print organized report of findings."""
    print("=" * 72)
    print("SCATTERED PYTHON FILES REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Total found: {len(results)} files outside ~/pythons/")
    print("=" * 72)

    # Group by category
    categories: dict[str, list[dict]] = {}
    for r in results:
        categories.setdefault(r["category"], []).append(r)

    # Sort categories by count
    for cat in sorted(categories, key=lambda c: len(categories[c]), reverse=True):
        items = categories[cat]
        print(f"\n--- {cat} ({len(items)} files) ---")

        # Determine if this is a cloned repo / project
        if cat.startswith("project:") or cat == "avatararts:automations":
            print(f"  [Project/repo -- not recommended to move]")
            continue

        for item in sorted(items, key=lambda x: x["name"])[:15]:
            size_kb = item["size"] / 1024
            print(f"  {item['relative']}")
            print(f"    {size_kb:.0f}KB | {item['modified']} | {item['purpose']}")

        if len(items) > 15:
            print(f"  ... and {len(items) - 15} more")


def print_move_candidates(results: list[dict]):
    """Show files that are good candidates to move to ~/pythons/."""
    print("=" * 72)
    print("MOVE CANDIDATES -- Files likely belonging in ~/pythons/")
    print("=" * 72)

    # Good candidates: home root, cleanup scripts, env utils, loose scripts
    safe_categories = {"home-root", "cleanup-scripts", "env-utils"}

    candidates = [r for r in results if r["category"] in safe_categories]
    candidates.sort(key=lambda x: x["category"])

    current_cat = ""
    for c in candidates:
        if c["category"] != current_cat:
            current_cat = c["category"]
            print(f"\n--- {current_cat} ---")
        print(f"  {c['relative']}")
        print(f"    {c['purpose']}")

    print(f"\nTotal move candidates: {len(candidates)}")
    print("Review before moving -- some may depend on relative paths.")


def main():
    parser = argparse.ArgumentParser(description="Find scattered Python files")
    parser.add_argument("--csv", type=Path, help="Export results to CSV")
    parser.add_argument("--move-candidates", action="store_true",
                        help="Show files safe to move to ~/pythons/")
    parser.add_argument("--max-depth", type=int, default=7,
                        help="Max directory depth to scan (default: 7)")
    args = parser.parse_args()

    print("Scanning... (this may take a moment)")
    results = scan_home(max_depth=args.max_depth)

    if args.move_candidates:
        print_move_candidates(results)
    else:
        print_report(results)

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["path", "relative", "name",
                                                     "size", "modified", "category", "purpose"])
            writer.writeheader()
            writer.writerows(results)
        print(f"\nCSV exported to {args.csv}")


if __name__ == "__main__":
    main()
