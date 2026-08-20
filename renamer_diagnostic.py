#!/usr/bin/env python3
"""Non-destructive diagnostic runner for content_aware_renamer.py.

Examples:
    python renamer_diagnostic.py ./upload
    python renamer_diagnostic.py ~/Pictures --output renamer-diagnostic.log
    python renamer_diagnostic.py ./assets --json renamer-diagnostic.json
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List


SCRIPT_DIR = Path(__file__).resolve().parent
RENAMER_PATH = SCRIPT_DIR / "content_aware_renamer.py"


def load_renamer():
    spec = importlib.util.spec_from_file_location("content_aware_renamer", RENAMER_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load {RENAMER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dependency_status() -> Dict[str, bool]:
    names = {"PIL": "Pillow", "imagehash": "imagehash", "mutagen": "mutagen", "PyPDF2": "PyPDF2"}
    result: Dict[str, bool] = {}
    for import_name, display_name in names.items():
        try:
            importlib.import_module(import_name)
            result[display_name] = True
        except ImportError:
            result[display_name] = False
    return result


def run_fixture_tests(ContentAwareRenamer) -> Dict[str, Any]:
    results: Dict[str, Any] = {}
    with tempfile.TemporaryDirectory(prefix="renamer-diagnostic-") as temp:
        root = Path(temp)
        (root / "first.md").write_text("# Same Title\nA", encoding="utf-8")
        (root / "second.md").write_text("# Same Title\nB", encoding="utf-8")
        excluded = root / "excluded"
        excluded.mkdir()
        (excluded / "should-not-scan.txt").write_text("# Hidden", encoding="utf-8")

        renamer = ContentAwareRenamer(root, exclude_paths=[excluded])
        renamer.scan_and_plan()
        names = [Path(item["new_path"]).name for item in renamer.manifest]
        results["collision_names"] = names
        results["collision_unique"] = len(names) == len(set(names))
        results["excluded_directory_skipped"] = not any(
            "should-not-scan" in item["original_path"] for item in renamer.manifest
        )

        renamer.dry_run = False
        renamer.execute_renames()
        results["transaction_success"] = all(
            item["status"] == "success" for item in renamer.manifest
        )
        results["content_preserved"] = (
            (root / "SameTitle.md").read_text(encoding="utf-8") == "# Same Title\nA"
            and (root / "SameTitle_1.md").read_text(encoding="utf-8") == "# Same Title\nB"
        )
    return results


def scan_root(ContentAwareRenamer, root: Path, sample_limit: int) -> Dict[str, Any]:
    renamer = ContentAwareRenamer(root)
    renamer.scan_and_plan()
    records = renamer.manifest
    by_extension: Dict[str, int] = {}
    for record in records:
        suffix = Path(record["original_path"]).suffix.lower() or "[none]"
        by_extension[suffix] = by_extension.get(suffix, 0) + 1
    return {
        "root": str(root),
        "file_count_planned": len(records),
        "by_extension": dict(sorted(by_extension.items())),
        "sample_manifest": records[:sample_limit],
        "unchanged_count": sum(item["status"] == "unchanged" for item in records),
        "collision_target_count": len(records) - len({item["new_path"] for item in records}),
    }


def style_examples(ContentAwareRenamer) -> Dict[str, str]:
    return {
        style: ContentAwareRenamer(".", naming_style=style).format_name("SEO Top Showcase")
        for style in ["pascal", "camel", "snake", "kebab", "human", "structured"]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run non-destructive renamer diagnostics")
    parser.add_argument("root", help="Directory to inspect")
    parser.add_argument("--output", help="Write human-readable log to this file")
    parser.add_argument("--json", dest="json_output", help="Write machine-readable report to this file")
    parser.add_argument("--sample-limit", type=int, default=12)
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    report: Dict[str, Any] = {
        "diagnostic_version": "1.0",
        "python": sys.version,
        "platform": platform.platform(),
        "renamer_path": str(RENAMER_PATH),
        "root_exists": root.exists(),
        "dependencies": dependency_status(),
    }

    lines: List[str] = []
    try:
        module = load_renamer()
        ContentAwareRenamer = module.ContentAwareRenamer
        report["style_examples"] = style_examples(ContentAwareRenamer)
        report["fixture_tests"] = run_fixture_tests(ContentAwareRenamer)
        if root.exists() and root.is_dir():
            report["scan"] = scan_root(ContentAwareRenamer, root, max(0, args.sample_limit))
        else:
            report["scan_error"] = "Root is missing or is not a directory"
    except Exception as exc:  # Diagnostics should report failures, not hide them.
        report["fatal_error"] = f"{type(exc).__name__}: {exc}"

    lines.append("Content-Aware Renamer Diagnostic")
    lines.append("=================================")
    lines.append(f"Root: {root}")
    lines.append(f"Renamer: {RENAMER_PATH}")
    lines.append(f"Python: {sys.version.split()[0]}")
    lines.append(f"Platform: {platform.platform()}")
    lines.append(f"Dependencies: {report['dependencies']}")
    lines.append(f"Style examples: {report.get('style_examples', {})}")
    lines.append(f"Fixture tests: {report.get('fixture_tests', {})}")
    if "scan" in report:
        scan = report["scan"]
        lines.append(f"Planned records: {scan['file_count_planned']}")
        lines.append(f"By extension: {scan['by_extension']}")
        lines.append(f"Unchanged: {scan['unchanged_count']}")
        lines.append(f"Duplicate targets: {scan['collision_target_count']}")
        lines.append("Sample manifest:")
        lines.append(json.dumps(scan["sample_manifest"], indent=2))
    if "scan_error" in report:
        lines.append(f"Scan error: {report['scan_error']}")
    if "fatal_error" in report:
        lines.append(f"Fatal error: {report['fatal_error']}")

    output = "\n".join(lines) + "\n"
    print(output, end="")
    if args.output:
        Path(args.output).expanduser().write_text(output, encoding="utf-8")
    if args.json_output:
        Path(args.json_output).expanduser().write_text(
            json.dumps(report, indent=2), encoding="utf-8"
        )
    return 0 if "fatal_error" not in report else 1


if __name__ == "__main__":
    raise SystemExit(main())
