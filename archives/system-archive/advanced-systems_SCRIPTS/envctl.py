import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""Environment orchestrator for the ~/.env.d ecosystem.

This CLI scans *.env files, validates keys, surfaces potential issues, and
can emit an updated MASTER_CONSOLIDATED.env file. It consolidates logic that
was previously spread across shell snippets.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


ENV_ROOT = Path.home() / ".env.d"
MASTER_FILENAME = "MASTER_CONSOLIDATED.env"
_ENV_LINE = re.compile(r"^(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(.*)$")
_PLACEHOLDER_PATTERNS = ("changeme", "todo", "your_", "placeholder", "xxxxx")


@dataclass
class EnvVariable:
    key: str
    value: str
    raw: str
    path: Path


@dataclass
class EnvFile:
    path: Path
    variables: List[EnvVariable]

    @property
    def name(self) -> str:
        return self.path.stem


def discover_env_files(root: Path) -> List[Path]:
    if not root.exists():
        raise SystemExit(f"Environment directory not found: {root}")
    files = []
    for path in root.glob("*.env"):
        if not path.is_file():
            continue
        if path.name == MASTER_FILENAME:
            # Skip the consolidated file; treat only source env files by default.
            continue
        files.append(path)
    return sorted(files)


def parse_env_file(path: Path) -> EnvFile:
    variables: List[EnvVariable] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = _ENV_LINE.match(stripped)
        if not match:
            continue
        key, value = match.groups()
        value = value.strip()
        if (
            value.startswith(("'", "'"))
            and value.endswith(("'", "'"))
            and len(value) >= 2
        ):
            value = value[1:-1]
        variables.append(EnvVariable(key=key, value=value, raw=stripped, path=path))
    return EnvFile(path=path, variables=variables)


def load_all_env_files(root: Path) -> List[EnvFile]:
    return [parse_env_file(path) for path in discover_env_files(root)]


def format_table(rows: Sequence[Sequence[str]], headers: Sequence[str]) -> str:
    widths = [len(header) for header in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            widths[idx] = max(widths[idx], len(cell))

    def fmt_row(row: Sequence[str]) -> str:
        return " | ".join(cell.ljust(widths[idx]) for idx, cell in enumerate(row))

    separator = "-+-".join("-" * width for width in widths)
    lines = [fmt_row(headers), separator]
    lines.extend(fmt_row(row) for row in rows)
    return "\n".join(lines)


def command_list(args: argparse.Namespace) -> None:
    env_files = load_all_env_files(args.root)
    if args.format == "names":
        for env_file in env_files:
            print(env_file.name)
        return

    rows: List[List[str]] = []
    for env_file in env_files:
        placeholder_count = sum(
            1
            for var in env_file.variables
            if any(token in var.value.lower() for token in _PLACEHOLDER_PATTERNS)
        )
        rows.append(
            [
                env_file.name,
                str(len(env_file.variables)),
                str(placeholder_count),
                str(env_file.path.relative_to(args.root)),
            ]
        )

    if rows:
        print(format_table(rows, headers=("File", "Vars", "Placeholders", "Path")))
    else:
        print("No .env files found in", args.root)


def command_show(args: argparse.Namespace) -> None:
    target = resolve_env_file(args.root, args.identifier)
    env_file = parse_env_file(target)
    print(f"# {target}")
    for var in env_file.variables:
        print(f"{var.key}={var.value}")


def resolve_env_file(root: Path, identifier: str) -> Path:
    candidate = root / identifier
    if candidate.is_file():
        return candidate
    if not identifier.endswith(".env"):
        candidate = root / f"{identifier}.env"
        if candidate.is_file():
            return candidate
    raise SystemExit(f"Could not resolve env file for identifier: {identifier}")


def command_validate(args: argparse.Namespace) -> None:
    env_files = load_all_env_files(args.root)
    issues: List[str] = []
    key_map: Dict[str, List[EnvVariable]] = {}

    for env_file in env_files:
        for var in env_file.variables:
            key_map.setdefault(var.key, []).append(var)
            if not re.fullmatch(r"[A-Z_][A-Z0-9_]*", var.key):
                issues.append(f"Non-standard key '{var.key}' in {env_file.path.name}")
            if any(token in var.value.lower() for token in _PLACEHOLDER_PATTERNS):
                issues.append(
                    f"Placeholder-like value for '{var.key}' in {env_file.path.name}: {var.value}"
                )

    for key, occurrences in key_map.items():
        if len(occurrences) > 1:
            files = ", ".join(var.path.name for var in occurrences)
            issues.append(f"Duplicate key '{key}' in files: {files}")

    if issues:
        print("Validation issues found:\n")
        for issue in issues:
            print(f"- {issue}")
        sys.exit(1)
    print("All environment files passed validation.")


def build_master(env_files: Iterable[EnvFile], output: Path) -> None:
    combined: Dict[str, EnvVariable] = {}
    duplicates: Dict[str, List[Path]] = {}

    for env_file in env_files:
        for var in env_file.variables:
            if var.key in combined:
                duplicates.setdefault(var.key, []).append(env_file.path)
            combined[var.key] = var

    timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines: List[str] = [
        "#!/bin/bash",
        "#",
        "# AUTO-GENERATED BY envctl.py",
        f"# Generated: {timestamp}",
        f"# Source: {ENV_ROOT}",
        "#",
    ]

    if duplicates:
        lines.append("# WARNING: Duplicate keys detected during build")
        for key, paths in duplicates.items():
            joined = ", ".join(str(path.name) for path in paths)
            lines.append(f"#   {key} -> {joined}")
        lines.append("#")

    for key in sorted(combined.keys()):
        value = combined[key].value
        escaped = value.replace("\\", "\\\\").replace("'", '\\"')
        lines.append(f'export {key}="{escaped}"')

    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def command_build(args: argparse.Namespace) -> None:
    env_files = load_all_env_files(args.root)
    output = args.output or (args.root / MASTER_FILENAME)
    if output.exists() and not args.force:
        raise SystemExit(
            f"Output file already exists: {output}\nUse --force to overwrite."
        )
    build_master(env_files, output)
    print(f"Master environment written to {output}")


def command_search(args: argparse.Namespace) -> None:
    env_files = load_all_env_files(args.root)
    results: List[str] = []
    query = args.query.lower()
    for env_file in env_files:
        for var in env_file.variables:
            if query in var.key.lower() or query in var.value.lower():
                results.append(f"{env_file.path.name}: {var.key}={var.value}")
    if results:
        print("\n".join(results))
    else:
        print(f"No matches found for '{args.query}'.")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Environment orchestrator CLI")
    parser.add_argument(
        "--root",
        type=Path,
        default=ENV_ROOT,
        help=f"Root directory of env files (default: {ENV_ROOT})",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List env files and stats")
    list_parser.add_argument(
        "--format",
        choices=("table", "names"),
        default="table",
        help="Output format (default: table)",
    )
    list_parser.set_defaults(func=command_list)

    show_parser = subparsers.add_parser("show", help="Show variables in a file")
    show_parser.add_argument("identifier", help="File name or stem (e.g., gemini)")
    show_parser.set_defaults(func=command_show)

    validate_parser = subparsers.add_parser("validate", help="Validate env files")
    validate_parser.set_defaults(func=command_validate)

    build_parser = subparsers.add_parser(
        "build", help="Generate MASTER_CONSOLIDATED.env"
    )
    build_parser.add_argument(
        "--output",
        type=Path,
        help="Alternative output path (defaults to MASTER_CONSOLIDATED.env)",
    )
    build_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing output file",
    )
    build_parser.set_defaults(func=command_build)

    search_parser = subparsers.add_parser("search", help="Search keys or values")
    search_parser.add_argument("query", help="Substring to search for")
    search_parser.set_defaults(func=command_search)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


try:
        raise SystemExit(main())
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)