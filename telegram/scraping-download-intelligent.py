"""
Web Scraping Download Intelligent 10

This module provides functionality for web scraping download intelligent 10.

Author: Auto-generated
Date: 2025-11-01
"""

# Constants
CONSTANT_123 = 123

#!/usr/bin/env python3
"""
Intelligent Content-Aware File Renamer
Analyzes file content to suggest better, more descriptive names
"""

import os
import re
import ast
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import Counter
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class IntelligentFileRenamer:
    """Analyzes file content and suggests intelligent renames"""

    def __init__(self, project_root: Path):
        """__init__ function."""

        self.project_root = project_root
        self.rename_suggestions = []

        # Patterns for better naming
        self.function_patterns = {
            "test": ["test_", "unittest", "pytest"],
            "api": ["api", "endpoint", "route", "flask", "fastapi"],
            "cli": ["argparse", "click", "sys.argv", "main"],
            "config": ["config", "settings", "env", "dotenv"],
            "database": ["sqlalchemy", "pymongo", "psycopg2", "database"],
            "scraper": ["beautifulsoup", "selenium", "scrapy", "requests"],
            "bot": ["telegram", "discord", "slack", "bot"],
            "analyzer": ["analyze", "analysis", "metrics"],
            "generator": ["generate", "create", "build"],
            "processor": ["process", "transform", "convert"],
            "downloader": ["download", "fetch", "retrieve"],
            "uploader": ["upload", "push", "send"],
            "monitor": ["monitor", "watch", "observe"],
            "scheduler": ["schedule", "cron", "timer"],
            "validator": ["validate", "verify", "check"],
        }

        # Bad naming patterns to fix
        self.bad_patterns = [
            r"^test\d+\.py$",  # test1.py, test2.py
            r"^main\d+\.py$",  # main1.py, main2.py
            r"^script\d*\.py$",  # script.py, script1.py
            r"^temp\d*\.py$",  # temp.py, temp1.py
            r"^new\d*\.py$",  # new.py, new1.py
            r"^old\d*\.py$",  # old.py, old1.py
            r"^untitled\d*\.py$",  # untitled.py
            r"^[a-z]\.py$",  # a.py, b.py, c.py
            r"^[a-z]\d\.py$",  # a1.py, b2.py
            r"^\d+\.py$",  # 1.py, CONSTANT_123.py
            r"_\d+\.py$",  # something_1.py (with just number)
            r"^copy.*\.py$",  # copy.py, copy_of_x.py
            r".*\s+copy.*\.py$",  # file copy.py
            r".*\s+\d+\.py$",  # file 1.py
        ]

    def is_badly_named(self, filename: str) -> bool:
        """Check if filename matches bad naming patterns"""
        for pattern in self.bad_patterns:
            if re.match(pattern, filename, re.IGNORECASE):
                return True
        return False

    def analyze_file_content(self, filepath: Path) -> Dict:
        """Analyze file content to understand its purpose"""
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")

            analysis = {
                "imports": [],
                "functions": [],
                "classes": [],
                "docstring": None,
                "main_purpose": None,
                "keywords": [],
            }

            # Parse AST
            try:
                tree = ast.parse(content)

                # Get docstring
                if isinstance(tree.body[0], ast.Expr) and isinstance(
                    tree.body[0].value, ast.Constant
                ):
                    analysis["docstring"] = tree.body[0].value.value

                # Get imports
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            analysis["imports"].append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            analysis["imports"].append(node.module)
                    elif isinstance(node, ast.FunctionDef):
                        analysis["functions"].append(node.name)
                    elif isinstance(node, ast.ClassDef):
                        analysis["classes"].append(node.name)
            except (ImportError, ModuleNotFoundError):
                pass

            # Extract keywords from content
            keywords = re.findall(r"\b[a-z_]{3,}\b", content.lower())
            keyword_counts = Counter(keywords)
            analysis["keywords"] = [k for k, v in keyword_counts.most_common(20)]

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing {filepath}: {e}")
            return {}

    def suggest_better_name(self, filepath: Path, analysis: Dict) -> Optional[str]:
        """Suggest a better filename based on content analysis"""
        current_name = filepath.stem  # without extension

        # Don't rename if already well-named
        if not self.is_badly_named(filepath.name):
            return None

        # Try to determine purpose from analysis
        purpose_indicators = []

        # Check imports
        for imp in analysis.get("imports", []):
            for purpose, keywords in self.function_patterns.items():
                if any(kw in imp.lower() for kw in keywords):
                    purpose_indicators.append(purpose)

        # Check functions
        for func in analysis.get("functions", []):
            for purpose, keywords in self.function_patterns.items():
                if any(kw in func.lower() for kw in keywords):
                    purpose_indicators.append(purpose)

        # Check classes
        for cls in analysis.get("classes", []):
            class_lower = cls.lower()
            for purpose, keywords in self.function_patterns.items():
                if any(kw in class_lower for kw in keywords):
                    purpose_indicators.append(purpose)
            # Use class name as base if it's descriptive
            if len(cls) > 4 and cls not in ["Base", "Main", "App"]:
                # Convert CamelCase to snake_case
                snake = re.sub(r"(?<!^)(?=[A-Z])", "_", cls).lower()
                purpose_indicators.append(snake)

        # Check docstring
        if analysis.get("docstring"):
            doc = analysis["docstring"].lower()
            for purpose, keywords in self.function_patterns.items():
                if any(kw in doc for kw in keywords):
                    purpose_indicators.append(purpose)

        # Check keywords
        for keyword in analysis.get("keywords", [])[:10]:
            if keyword in ["youtube", "instagram", "twitter", "facebook"]:
                purpose_indicators.append(keyword)
            elif keyword in ["image", "video", "audio", "text"]:
                purpose_indicators.append(keyword)

        if not purpose_indicators:
            return None

        # Count most common indicators
        indicator_counts = Counter(purpose_indicators)
        top_indicators = [ind for ind, _ in indicator_counts.most_common(3)]

        # Build new name
        new_name_parts = []
        for ind in top_indicators[:2]:  # Use top 2 indicators
            if ind not in new_name_parts:
                new_name_parts.append(ind)

        if not new_name_parts:
            return None

        # Create final name
        new_name = "_".join(new_name_parts)

        # Add suffix if needed to make unique
        new_filepath = filepath.parent / f"{new_name}.py"
        counter = 1
        while new_filepath.exists() and new_filepath != filepath:
            new_filepath = filepath.parent / f"{new_name}_{counter}.py"
            counter += 1

        return new_filepath.name

    def analyze_project(self, dry_run: bool = True) -> List[Dict]:
        """Analyze all Python files and suggest renames"""
        logger.info("🔍 Analyzing Python files for intelligent renaming...")

        python_files = list(self.project_root.rglob("*.py"))
        logger.info(f"📁 Found {len(python_files)} Python files")

        suggestions = []
        badly_named_count = 0

        for filepath in python_files:
            # Skip hidden and git files
            if any(part.startswith(".") for part in filepath.parts):
                continue

            # Check if badly named
            if self.is_badly_named(filepath.name):
                badly_named_count += 1

                # Analyze content
                analysis = self.analyze_file_content(filepath)

                # Suggest better name
                new_name = self.suggest_better_name(filepath, analysis)

                if new_name and new_name != filepath.name:
                    suggestions.append(
                        {
                            "current_path": str(filepath),
                            "current_name": filepath.name,
                            "suggested_name": new_name,
                            "reason": f"Content suggests: {', '.join(analysis.get('keywords', [])[:3])}",
                            "classes": analysis.get("classes", []),
                            "main_imports": analysis.get("imports", [])[:5],
                        }
                    )

        logger.info(f"\n📊 Found {badly_named_count} badly named files")
        logger.info(f"💡 Generated {len(suggestions)} rename suggestions\n")

        return suggestions

    def apply_renames(self, suggestions: List[Dict], auto_approve: bool = False):
        """Apply suggested renames"""
        if not suggestions:
            logger.info("✅ No renames needed!")
            return

        logger.info(f"📝 Rename Suggestions ({len(suggestions)} files):\n")

        applied = 0
        for i, suggestion in enumerate(suggestions, 1):
            current = Path(suggestion["current_path"])
            suggested = current.parent / suggestion["suggested_name"]

            logger.info(
                f"{i}. {suggestion['current_name']} → {suggestion['suggested_name']}"
            )
            logger.info(f"   Reason: {suggestion['reason']}")

            if not auto_approve:
                continue

            try:
                # Check if git tracked
                result = subprocess.run(
                    ["git", "ls-files", "--error-unmatch", str(current)],
                    capture_output=True,
                )
                is_tracked = result.returncode == 0

                if is_tracked:
                    subprocess.run(
                        ["git", "mv", str(current), str(suggested)], check=True
                    )
                    logger.info(f"   ✅ Renamed (git tracked)")
                else:
                    current.rename(suggested)
                    logger.info(f"   ✅ Renamed")
                applied += 1
            except Exception as e:
                logger.error(f"   ❌ Error: {e}")

            logger.info("")

        if auto_approve:
            logger.info(f"✅ Successfully renamed {applied}/{len(suggestions)} files")
        else:
            logger.info(f"\n💡 To apply renames, run with --apply flag")


def main():
    """main function."""

    import argparse

    parser = argparse.ArgumentParser(
        description="Intelligent content-aware file renamer"
    )
    parser.add_argument(
        "path",
        type=Path,
        nargs="?",
        default=Path.cwd(),
        help="Project directory to analyze",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually apply the renames (default: dry-run only)",
    )
    parser.add_argument("--output", type=Path, help="Save suggestions to JSON file")

    args = parser.parse_args()

    renamer = IntelligentFileRenamer(args.path)
    suggestions = renamer.analyze_project()

    if args.output:
        args.output.write_text(json.dumps(suggestions, indent=2))
        logger.info(f"📄 Saved suggestions to {args.output}")

    renamer.apply_renames(suggestions, auto_approve=args.apply)


if __name__ == "__main__":
    main()
