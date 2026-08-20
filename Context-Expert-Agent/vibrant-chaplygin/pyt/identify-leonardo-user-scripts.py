import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_200 = 200

#!/usr/bin/env python3
"""
🔍 USER SCRIPT IDENTIFIER
========================
Intelligently distinguishes between:
✅ Your actual custom scripts
❌ System/library files (pandas, numpy test files, etc.)
❌ Third-party package code
❌ Virtual environment files

Detection Methods:
✨ AST analysis for library patterns
✨ Path analysis (site-packages, venv, etc.)
✨ Import pattern detection
✨ Test file identification (from libraries vs custom tests)
✨ File content fingerprinting
"""

import os
import ast
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Set, Tuple
import csv
import json


# Colors
class Colors:
    CYAN = "\CONSTANT_033[96m"
    GREEN = "\CONSTANT_033[92m"
    YELLOW = "\CONSTANT_033[93m"
    RED = "\CONSTANT_033[91m"
    MAGENTA = "\CONSTANT_033[35m"
    BOLD = "\CONSTANT_033[1m"
    END = "\CONSTANT_033[0m"


class UserScriptIdentifier:
    """Identify user scripts vs library/system files"""

    # Library test file patterns (NOT user code!)
    LIBRARY_TEST_PATTERNS = [
        "test_pandas",
        "test_numpy",
        "test_scipy",
        "test_sklearn",
        "test_matplotlib",
        "test_torch",
        "test_tensorflow",
        "test_array",
        "test_scalar",
        "test_dtype",
        "test_indexing",
        "test_reshape",
        "test_reduction",
        "test_ufunc",
        "test_datetime",
        "test_timedelta",
        "test_timestamp",
        "test_sparse",
        "test_interval",
        "test_multiindex",
    ]

    # System/library paths to exclude
    EXCLUDE_PATHS = [
        "site-packages",
        "dist-packages",
        "lib/python",
        ".venv",
        "venv",
        "virtualenv",
        "env",
        "__pycache__",
        ".pytest_cache",
        ".tox",
        "node_modules",
        ".git",
    ]

    # Library module imports (if file ONLY imports these, it's probably library code)
    LIBRARY_ONLY_IMPORTS = {
        "pandas": ["pandas", "pd"],
        "numpy": ["numpy", "np"],
        "scipy": ["scipy"],
        "matplotlib": ["matplotlib", "plt"],
        "sklearn": ["sklearn", "scikit"],
    }

    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)

        self.categories = {
            "user_scripts": [],
            "library_tests": [],
            "library_code": [],
            "system_files": [],
            "uncertain": [],
        }

        self.stats = {
            "total_scanned": 0,
            "user_scripts": 0,
            "library_tests": 0,
            "library_code": 0,
            "system_files": 0,
            "uncertain": 0,
        }

    def is_library_test_file(self, filepath: Path) -> bool:
        """Check if file is from a library test suite"""

        name_lower = filepath.stem.lower()

        # Check against known library test patterns
        for pattern in self.LIBRARY_TEST_PATTERNS:
            if pattern in name_lower:
                return True

        # Check for pandas/numpy specific test patterns
        if name_lower.startswith("test_") and any(
            lib in name_lower
            for lib in [
                "period",
                "interval",
                "timestamp",
                "timedelta",
                "offset",
                "scalar",
                "array",
                "dtype",
                "reshape",
                "reduction",
            ]
        ):
            return True

        return False

    def is_system_or_library_path(self, filepath: Path) -> bool:
        """Check if file is in a system/library path"""

        path_str = str(filepath).lower()

        for exclude_path in self.EXCLUDE_PATHS:
            if exclude_path in path_str:
                return True

        return False

    def analyze_file_origin(self, filepath: Path) -> Tuple[str, str]:
        """Determine if file is user code or library code"""

        # First check path
        if self.is_system_or_library_path(filepath):
            return "system_files", "In system/library path"

        # Check if it's a known library test file
        if self.is_library_test_file(filepath):
            return "library_tests", "Library test file pattern"

        # Analyze content
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Parse AST
            tree = ast.parse(content)

            imports = []
            has_main = False
            has_custom_functions = False
            function_names = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
                elif isinstance(node, ast.FunctionDef):
                    function_names.append(node.name)
                    if node.name == "main":
                        has_main = True
                    if not node.name.startswith("test_"):
                        has_custom_functions = True

            # Check if it ONLY imports testing libraries
            testing_only = all(
                imp
                in [
                    "pytest",
                    "unittest",
                    "nose",
                    "hypothesis",
                    "numpy.testing",
                    "pandas.testing",
                ]
                for imp in imports
                if imp
            )

            if testing_only and filepath.stem.startswith("test_"):
                return "library_tests", "Only imports testing frameworks"

            # Check for library-specific patterns
            imports_lower = [imp.lower() for imp in imports]

            # If it imports custom packages or APIs, it's likely user code
            custom_indicators = [
                "requests",
                "instagram",
                "youtube",
                "leonardo",
                "openai",
                "anthropic",
                "gemini",
                "selenium",
                "beautifulsoup",
                "flask",
                "fastapi",
                "discord",
                "telegram",
                "tweepy",
                "tiktok",
                "elevenlabs",
                "replicate",
                "PIL",
                "cv2",
                "moviepy",
            ]

            if any(
                indicator in " ".join(imports_lower) for indicator in custom_indicators
            ):
                return "user_scripts", "Contains custom API/service imports"

            # Check for custom business logic
            custom_function_patterns = [
                "download",
                "upload",
                "scrape",
                "bot",
                "automation",
                "generate",
                "organize",
                "process",
                "leonardo",
                "instagram",
            ]

            func_text = " ".join(function_names).lower()
            if any(pattern in func_text for pattern in custom_function_patterns):
                return "user_scripts", "Has custom business logic functions"

            # Has main() = likely user script
            if has_main:
                return "user_scripts", "Has main() function"

            # If it has custom functions (not just test_*)
            if has_custom_functions:
                return "user_scripts", "Has custom functions"

            # Otherwise uncertain
            return "uncertain", "Could not determine origin"

        except SyntaxError:
            # If it has syntax errors, might be incomplete user script
            return "uncertain", "Syntax error (incomplete?)"
        except Exception as e:
            return "uncertain", f"Analysis error: {str(e)[:50]}"

    def scan_and_categorize(self):
        """Scan directory and categorize files"""

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"🔍 SCANNING AND CATEGORIZING FILES")
        logger.info(f"{'='*80}{Colors.END}\n")

        python_files = list(self.target_dir.rglob("*.py"))

        # Skip obvious backup dirs
        python_files = [
            f
            for f in python_files
            if "backup_2025" not in str(f) and "dedup_backup" not in str(f)
        ]

        logger.info(
            f"{Colors.GREEN}Scanning {len(python_files)} Python files...{Colors.END}\n"
        )

        for idx, filepath in enumerate(python_files, 1):
            if idx % CONSTANT_200 == 0:
                logger.info(
                    f"{Colors.YELLOW}Progress: {idx}/{len(python_files)}...{Colors.END}",
                    end="\r",
                )

            self.stats["total_scanned"] += 1

            category, reason = self.analyze_file_origin(filepath)

            self.categories[category].append(
                {
                    "path": filepath,
                    "rel_path": str(filepath.relative_to(self.target_dir)),
                    "name": filepath.name,
                    "size": filepath.stat().st_size,
                    "reason": reason,
                }
            )

            self.stats[category] += 1

        logger.info(f"\n{Colors.GREEN}✅ Categorization complete!{Colors.END}\n")

    def generate_report(self):
        """Generate categorization report"""

        logger.info(f"{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"📊 CATEGORIZATION RESULTS")
        logger.info(f"{'='*80}{Colors.END}\n")

        # Print stats
        logger.info(f"{Colors.BOLD}Results:{Colors.END}\n")
        logger.info(
            f"  {Colors.GREEN}✅ User Scripts:    {self.stats['user_scripts']:,}{Colors.END}"
        )
        logger.info(
            f"  {Colors.RED}❌ Library Tests:   {self.stats['library_tests']:,}{Colors.END}"
        )
        logger.info(
            f"  {Colors.RED}❌ Library Code:    {self.stats['library_code']:,}{Colors.END}"
        )
        logger.info(
            f"  {Colors.RED}❌ System Files:    {self.stats['system_files']:,}{Colors.END}"
        )
        logger.info(
            f"  {Colors.YELLOW}⚠️  Uncertain:       {self.stats['uncertain']:,}{Colors.END}\n"
        )

        # Show examples of library tests to exclude
        if self.categories["library_tests"]:
            logger.info(
                f"{Colors.RED}Examples of Library Test Files (NOT your code):{Colors.END}"
            )
            for item in self.categories["library_tests"][:10]:
                logger.info(f"  ❌ {item['name']}")
            print()

        # Show examples of user scripts
        if self.categories["user_scripts"]:
            logger.info(f"{Colors.GREEN}Examples of YOUR Scripts:{Colors.END}")
            for item in self.categories["user_scripts"][:15]:
                logger.info(f"  ✅ {item['name']}")
            print()

        # Generate reports
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.target_dir / f"USER_SCRIPTS_IDENTIFIED_{timestamp}.md"
        csv_file = self.target_dir / f"user_scripts_{timestamp}.csv"

        # Markdown report
        with open(report_file, "w") as f:
            f.write("# 🔍 USER SCRIPT IDENTIFICATION REPORT\n\n")
            f.write(
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )
            f.write("## 📊 SUMMARY\n\n")
            f.write(f"| Category | Count | Percentage |\n")
            f.write(f"|----------|-------|------------|\n")

            total = self.stats["total_scanned"]
            for category in [
                "user_scripts",
                "library_tests",
                "library_code",
                "system_files",
                "uncertain",
            ]:
                count = self.stats[category]
                pct = (count / total * CONSTANT_100) if total > 0 else 0
                f.write(
                    f"| {category.replace('_', ' ').title()} | {count:,} | {pct:.1f}% |\n"
                )
            f.write(Path("\n"))

            # List user scripts
            f.write("## ✅ YOUR ACTUAL SCRIPTS\n\n")
            f.write(f"Total: {len(self.categories['user_scripts']):,} files\n\n")

            for item in self.categories["user_scripts"][:CONSTANT_100]:
                f.write(f"- `{item['rel_path']}`\n")
                f.write(f"  - Reason: {item['reason']}\n")

            if len(self.categories["user_scripts"]) > CONSTANT_100:
                f.write(
                    f"\n... and {len(self.categories['user_scripts']) - CONSTANT_100} more\n"
                )

            # List library files to exclude
            f.write("\n## ❌ LIBRARY/SYSTEM FILES (Exclude from consolidation)\n\n")
            f.write(
                f"Total: {self.stats['library_tests'] + self.stats['library_code'] + self.stats['system_files']:,} files\n\n"
            )

            for category in ["library_tests", "library_code", "system_files"]:
                if self.categories[category]:
                    f.write(f"### {category.replace('_', ' ').title()}\n\n")
                    for item in self.categories[category][:20]:
                        f.write(f"- `{item['name']}` - {item['reason']}\n")
                    if len(self.categories[category]) > 20:
                        f.write(
                            f"- ... and {len(self.categories[category]) - 20} more\n"
                        )
                    f.write(Path("\n"))

        # CSV with user scripts only
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["File Path", "File Name", "Size (bytes)", "Category", "Reason"]
            )

            for item in self.categories["user_scripts"]:
                writer.writerow(
                    [
                        item["rel_path"],
                        item["name"],
                        item["size"],
                        "user_script",
                        item["reason"],
                    ]
                )

        logger.info(f"{Colors.GREEN}✅ Report: {report_file}{Colors.END}")
        logger.info(f"{Colors.GREEN}✅ CSV: {csv_file}{Colors.END}")

        return report_file, csv_file

    def run(self):
        """Run identification"""

        logger.info(f"{Colors.MAGENTA}{Colors.BOLD}")
        logger.info(
            "╔═══════════════════════════════════════════════════════════════════════════════╗"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "║              🔍 USER SCRIPT IDENTIFIER 🎯                                     ║"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "║     Distinguish Your Scripts from Library/System Files                       ║"
        )
        logger.info(
            "║                                                                               ║"
        )
        logger.info(
            "╚═══════════════════════════════════════════════════════════════════════════════╝"
        )
        logger.info(f"{Colors.END}\n")

        logger.info(f"{Colors.CYAN}Target: {self.target_dir}{Colors.END}\n")

        self.scan_and_categorize()
        self.generate_report()

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"✅ IDENTIFICATION COMPLETE!")
        logger.info(f"{'='*80}{Colors.END}\n")

        logger.info(
            f"{Colors.BOLD}Only work with these {self.stats['user_scripts']:,} files!{Colors.END}\n"
        )


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="🔍 Identify user scripts vs library files"
    )
    parser.add_argument("--target", type=str, required=True, help="Target directory")

    args = parser.parse_args()

    identifier = UserScriptIdentifier(args.target)
    identifier.run()


if __name__ == "__main__":
    main()
