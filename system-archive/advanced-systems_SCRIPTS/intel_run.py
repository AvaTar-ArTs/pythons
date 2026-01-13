#!/usr/bin/env python3
"""Entry point for intelligent content-aware analysis of the clean workspace."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Iterable

from rich.console import Console

from content_intel import ContentAnalyzer, MarkdownReporter, ConsoleReporter

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def iter_python_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.py"):
        if path.name.startswith("."):
            continue
        if "__pycache__" in path.parts:
            continue
        if any(part in {".venv", "venv", ".git", "node_modules"} for part in path.parts):
            continue
        yield path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run intelligent content-aware analysis over the clean project.")
    parser.add_argument("paths", nargs="*", help="Optional specific files or directories to analyze")
    parser.add_argument("--report", default="reports", help="Directory for markdown reports")
    parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2", help="SentenceTransformer model name")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent
    targets: list[Path] = []

    if args.paths:
        for item in args.paths:
            path = Path(item).expanduser().resolve()
            if path.is_dir():
                targets.extend(iter_python_files(path))
            else:
                targets.append(path)
    else:
        targets = list(iter_python_files(project_root))

    logger.info("Analyzing %d python files", len(targets))
    analyzer = ContentAnalyzer(project_root=project_root, embedding_model=args.model)
    insights = analyzer.analyze_paths(targets)

    reporter = MarkdownReporter(Path(args.report))
    report_path = reporter.write(insights, filename="content_intel.md")
    ConsoleReporter(Console()).render(insights)
    logger.info("Markdown report written to %s", report_path)


if __name__ == "__main__":
    main()
