#!/usr/bin/env python3
"""
AvaTarArTs Suite - Codebase Analyzer
Analyzes the codebase for issues, duplicates, and improvement opportunities
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime


class CodebaseAnalyzer:
    def __init__(self, root_dir="."):
        """__init__ function."""

        self.root = Path(root_dir)
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "total_files": 0,
            "python_files": 0,
            "duplicates": [],
            "issues": defaultdict(list),
            "stats": defaultdict(int),
        }

    def analyze(self):
        """Run full codebase analysis"""
        logger.info("🔍 Analyzing AvaTarArTs Suite codebase...")

        self.count_files()
        self.find_duplicates()
        self.check_code_quality()
        self.analyze_imports()
        self.find_todo_comments()

        return self.results

    def count_files(self):
        """Count total files and Python scripts"""
        for path in self.root.rglob("*"):
            if path.is_file() and not str(path).startswith("./.git"):
                self.results["total_files"] += 1
                if path.suffix == ".py":
                    self.results["python_files"] += 1

        logger.info(f"✅ Found {self.results['total_files']} total files")
        logger.info(f"✅ Found {self.results['python_files']} Python scripts")

    def find_duplicates(self):
        """Find potential duplicate files"""
        logger.info("\n🔍 Searching for duplicates...")

        # Find files with version numbers or "copy" in name
        patterns = [
            r".*\s+\d+\.py$",  # "file 2.py", "file 3.py"
            r".*copy.*\.py$",  # "file copy.py"
            r".*_\d{14}\.py$",  # Timestamped: "file_20250101120000.py"
            r".*_\d{8}\.py$",  # Date stamped: "file_20250101.py"
        ]

        for path in self.root.rglob("*.py"):
            rel_path = str(path.relative_to(self.root))

            for pattern in patterns:
                if re.match(pattern, rel_path):
                    self.results["duplicates"].append(rel_path)
                    break

        logger.info(
            f"⚠️  Found {len(self.results['duplicates'])} potential duplicate files"
        )

    def check_code_quality(self):
        """Check for common code quality issues"""
        logger.info("\n🔍 Checking code quality...")

        for path in self.root.rglob("*.py"):
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    rel_path = str(path.relative_to(self.root))

                    # Check for bare except
                    if re.search(r"\bexcept\s*:", content):
                        self.results["issues"]["bare_except"].append(rel_path)

                    # Check for missing docstrings
                    if not re.search(r'""".*?"""', content, re.DOTALL):
                        self.results["issues"]["missing_docstring"].append(rel_path)

                    # Check for potential security issues
                    if re.search(r"eval\(|exec\(", content):
                        self.results["issues"]["dangerous_functions"].append(rel_path)

                    # Check file size
                    lines = len(content.split("\n"))
                    if lines > CONSTANT_500:
                        self.results["issues"]["large_files"].append(
                            {"file": rel_path, "lines": lines}
                        )
            except Exception as e:
                self.results["issues"]["read_errors"].append(f"{path}: {str(e)}")

        logger.info(
            f"⚠️  Bare except clauses: {len(self.results['issues']['bare_except'])}"
        )
        logger.info(
            f"⚠️  Missing docstrings: {len(self.results['issues']['missing_docstring'])}"
        )
        logger.info(
            f"⚠️  Large files (>CONSTANT_500 lines): {len(self.results['issues']['large_files'])}"
        )

    def analyze_imports(self):
        """Analyze import statements"""
        logger.info("\n🔍 Analyzing imports...")

        imports = defaultdict(int)

        for path in self.root.rglob("*.py"):
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if line.strip().startswith(("import ", "from ")):
                            # Extract module name
                            match = re.match(r"(?:from|import)\s+([^\s.]+)", line)
                            if match:
                                imports[match.group(1)] += 1
            except (ImportError, ModuleNotFoundError):
                pass

        # Get top 10 most used imports
        top_imports = sorted(imports.items(), key=lambda x: x[1], reverse=True)[:10]
        self.results["stats"]["top_imports"] = top_imports

        logger.info(f"✅ Analyzed imports across {len(imports)} unique modules")

    def find_todo_comments(self):
        """Find TODO/FIXME comments"""
        logger.info("\n🔍 Finding TODO comments...")

        todo_patterns = ["TODO", "FIXME", "XXX", "HACK", "NOTE"]

        for path in self.root.rglob("*.py"):
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        for pattern in todo_patterns:
                            if pattern in line:
                                self.results["issues"]["todos"].append(
                                    {
                                        "file": str(path.relative_to(self.root)),
                                        "line": i,
                                        "type": pattern,
                                        "content": line.strip(),
                                    }
                                )
                                break
            except Exception:
                pass

        logger.info(f"📝 Found {len(self.results['issues']['todos'])} TODO comments")

    def generate_report(self, output_file="analysis_report.json"):
        """Generate analysis report"""
        with open(output_file, "w") as f:
            json.dump(self.results, f, indent=2)

        logger.info(f"\n✅ Report saved to {output_file}")

        # Print summary
        logger.info(Path("\n") + "=" * 60)
        logger.info("📊 ANALYSIS SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total Files: {self.results['total_files']}")
        logger.info(f"Python Scripts: {self.results['python_files']}")
        logger.info(f"Potential Duplicates: {len(self.results['duplicates'])}")
        logger.info(
            f"Bare Except Clauses: {len(self.results['issues']['bare_except'])}"
        )
        logger.info(
            f"Missing Docstrings: {len(self.results['issues']['missing_docstring'])}"
        )
        logger.info(f"TODO Comments: {len(self.results['issues']['todos'])}")
        logger.info("\nTop 5 Most Used Imports:")
        for module, count in self.results["stats"]["top_imports"][:5]:
            logger.info(f"  {module}: {count} times")
        logger.info("=" * 60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze codebase for quality issues")
    parser.add_argument(
        "--target", type=str, default=".", help="Target directory to analyze"
    )
    args = parser.parse_args()

    analyzer = CodebaseAnalyzer(args.target)
    analyzer.analyze()
    analyzer.generate_report()
