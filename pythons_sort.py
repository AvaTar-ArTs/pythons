#!/usr/bin/env python3
"""List and explicitly launch standalone scripts from a pythons checkout."""
import argparse
import os
from pathlib import Path
import shlex
import subprocess
import sys

# Categories reflect the current repository, not the retired src/tools layout.
CATEGORY_PATHS = {
    "analysis": ("data_processing",),
    "cleanup": ("file_operations",),
    "dedup": ("file_operations", "data_processing"),
    "rename": ("file_organization",),
    "scanners": (".",),
}
LEGACY_COMMANDS = ("analyze", "cleanup", "dedup", "organize", "scan", "rename", "pdf")


def list_tools(repository, category):
    """List exact paths without importing scripts or traversing directory symlinks."""
    paths = set()
    for directory in CATEGORY_PATHS[category]:
        folder = repository / directory
        if folder.is_symlink():
            continue
        for script in folder.glob("*.py"):
            if script.is_symlink() or not script.is_file():
                continue
            if script.name.startswith("__"):
                continue
            if category == "scanners" and "scan" not in script.stem.lower():
                continue
            paths.add(script.relative_to(repository).as_posix())
    return sorted(paths)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="List and run standalone scripts with their own arguments.",
        prog="pythons-sort",
    )
    parser.add_argument(
        "--repository",
        default=os.environ.get("PYTHONS_REPOSITORY", str(Path(__file__).resolve().parent)),
        help="Checkout containing scripts (or set PYTHONS_REPOSITORY).",
    )
    commands = parser.add_subparsers(dest="command")
    info = commands.add_parser("info", help="List actual script paths; do not import them.")
    selection = info.add_mutually_exclusive_group()
    selection.add_argument("--category", choices=tuple(CATEGORY_PATHS))
    selection.add_argument("--all", action="store_true")

    run = commands.add_parser("run", help="Run one exact repository-relative Python script.")
    run.add_argument("--dry-run", action="store_true", help="Print the command without running it.")
    run.add_argument("script", help="Exact path from info or the repository inventory.")
    run.add_argument("script_args", nargs=argparse.REMAINDER, help="Arguments passed unchanged to the script.")

    for command in LEGACY_COMMANDS:
        legacy = commands.add_parser(command, help="Retired implicit tool dispatch; use run.")
        legacy.add_argument("legacy_args", nargs=argparse.REMAINDER)

    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 0
    if args.command in LEGACY_COMMANDS:
        parser.error(
            f"'{args.command}' used an unavailable layout and unverified argument mappings. "
            "Use 'info --all', then 'run [--dry-run] SCRIPT -- SCRIPT_ARGS'. "
            "Standalone scripts have different interfaces."
        )

    repository = Path(args.repository).expanduser().resolve()
    if not repository.is_dir():
        parser.error(f"Repository directory not found: {repository}")
    if args.command == "info":
        categories = [args.category] if args.category else list(CATEGORY_PATHS)
        total = 0
        for category in categories:
            paths = list_tools(repository, category)
            print(f"\n{category.upper()} TOOLS:")
            for path in paths:
                print(f"  {path}")
            total += len(paths)
        if total == 0:
            print("No tools found. Set --repository to a pythons checkout.", file=sys.stderr)
            return 1
        return 0

    script = (repository / args.script).resolve()
    try:
        script.relative_to(repository)
    except ValueError:
        parser.error("Script resolves outside the selected repository.")
    if not script.is_file():
        parser.error(f"Script not found: {args.script}")
    if script.suffix != ".py":
        parser.error("Select a Python (.py) script.")
    if script == Path(__file__).resolve():
        parser.error("Select a tool, not the launcher itself.")
    forwarded = args.script_args
    if forwarded[:1] == ["--"]:
        forwarded = forwarded[1:]
    command = [sys.executable, str(script), *forwarded]
    if args.dry_run:
        print(f"Preview (not executed): {shlex.join(command)}")
        return 0
    try:
        result = subprocess.run(command, check=False)
    except OSError as error:
        print(f"Unable to launch script: {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130
    return result.returncode if result.returncode >= 0 else 128 - result.returncode


if __name__ == "__main__":
    sys.exit(main())
