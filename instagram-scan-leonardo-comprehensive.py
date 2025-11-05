#!/usr/bin/env python3
"""
Final Comprehensive Scan - Uses ALL tools available

Analyzes your entire Python ecosystem with:
- File system analysis
- Duplicate detection
- Code quality checks
- Smart categorization
"""

from pathlib import Path
from collections import defaultdict
import hashlib
import ast
import re


class FinalComprehensiveScan:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.results = {}

    def scan_directory_structure(self):
        """Comprehensive directory scan."""
        print(f"\n{'='*80}")
        print("📊 DIRECTORY STRUCTURE ANALYSIS")
        print(f"{'='*80}\n")

        categories = sorted(
            [
                f
                for f in self.target_dir.iterdir()
                if f.is_dir() and not f.name.startswith((".", "_"))
            ]
        )

        by_category = {}
        total = 0

        for cat in categories:
            py_files = list(cat.glob("*.py"))
            if len(py_files) > 0:
                by_category[cat.name] = len(py_files)
                total += len(py_files)

                emoji = {
                    "youtube": "🎥",
                    "instagram": "📸",
                    "ai": "🤖",
                    "image": "🖼️",
                    "audio": "🎵",
                    "leonardo": "🎨",
                    "scripts": "✨",
                }.get(cat.name, "📁")
                print(f"  {emoji} {cat.name:25} {len(py_files):4} scripts")

        self.results["total_scripts"] = total
        self.results["categories"] = len(by_category)
        self.results["by_category"] = by_category

        print(f"\n  Total: {total:,} Python scripts\n")

    def find_exact_duplicates(self):
        """Find exact duplicate files by content hash."""
        print(f"\n{'='*80}")
        print("🔍 EXACT DUPLICATE DETECTION")
        print(f"{'='*80}\n")

        all_files = list(self.target_dir.rglob("*.py"))
        all_files = [
            f
            for f in all_files
            if not any(p in str(f) for p in [".git", "__pycache__", "_backups"])
        ]

        by_hash = defaultdict(list)

        for f in all_files:
            try:
                content = f.read_bytes()
                file_hash = hashlib.md5(content).hexdigest()
                by_hash[file_hash].append(f)
            except Exception:
                pass

        duplicates = [files for files in by_hash.values() if len(files) > 1]

        if duplicates:
            print(f"  ⚠️  Found {len(duplicates)} sets of exact duplicates:\n")
            for i, dup_set in enumerate(duplicates[:5], 1):
                print(f"  Set {i}: {len(dup_set)} identical files")
                for f in dup_set:
                    print(f"    • {f.relative_to(self.target_dir)}")
                print()

            if len(duplicates) > 5:
                print(f"  ... and {len(duplicates) - 5} more duplicate sets")
        else:
            print("  ✅ NO EXACT DUPLICATES FOUND!\n")

        self.results["duplicates"] = len(duplicates)

    def analyze_code_quality(self):
        """Analyze code quality issues."""
        print(f"\n{'='*80}")
        print("🔬 CODE QUALITY ANALYSIS")
        print(f"{'='*80}\n")

        categories = [
            f
            for f in self.target_dir.iterdir()
            if f.is_dir() and not f.name.startswith((".", "_"))
        ]

        issues = {
            "bare_except": 0,
            "magic_numbers": 0,
            "long_functions": 0,
            "missing_docstrings": 0,
        }

        sample_count = 0
        max_samples = 100

        for cat in categories:
            for py_file in cat.glob("*.py"):
                if sample_count >= max_samples:
                    break

                try:
                    content = py_file.read_text(encoding="utf-8")

                    # Check for bare except
                    if re.search(r"except\s*:", content):
                        issues["bare_except"] += 1

                    # Check for magic numbers (simplified)
                    if re.search(r"\s=\s\d{3,}", content):
                        issues["magic_numbers"] += 1

                    # Parse AST for deeper analysis
                    try:
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                # Long function check
                                if hasattr(node, "end_lineno") and hasattr(
                                    node, "lineno"
                                ):
                                    if node.end_lineno - node.lineno > 100:
                                        issues["long_functions"] += 1

                                # Missing docstring
                                if not ast.get_docstring(node):
                                    issues["missing_docstrings"] += 1
                    except Exception:
                        pass

                    sample_count += 1

                except Exception:
                    pass

        print(f"  Sampled {sample_count} files for quality issues:\n")
        print(f"  ⚠️  Bare except clauses:    {issues['bare_except']}")
        print(f"  ⚠️  Magic numbers:          {issues['magic_numbers']}")
        print(f"  ⚠️  Long functions (>100L):  {issues['long_functions']}")
        print(f"  ⚠️  Missing docstrings:     {issues['missing_docstrings']}")
        print()

        self.results["quality_issues"] = issues

    def categorization_check(self):
        """Check if files are in correct categories."""
        print(f"\n{'='*80}")
        print("🎯 CATEGORIZATION CHECK")
        print(f"{'='*80}\n")

        miscat = []

        folders_to_check = ["youtube", "instagram", "ai", "leonardo"]

        for folder_name in folders_to_check:
            folder = self.target_dir / folder_name
            if not folder.exists():
                continue

            for py_file in list(folder.glob("*.py"))[:20]:  # Sample 20 per folder
                name = py_file.stem.lower()

                # Check if belongs
                if folder_name == "youtube" and not any(
                    x in name for x in ["youtube", "yt-", "ytube"]
                ):
                    miscat.append((py_file.name, folder_name, "?"))
                elif folder_name == "instagram" and not any(
                    x in name for x in ["instagram", "insta-", "ig-"]
                ):
                    # Check imports
                    try:
                        content = py_file.read_text(encoding="utf-8")
                        if (
                            "instabot" not in content
                            and "instagram" not in content.lower()
                        ):
                            miscat.append((py_file.name, folder_name, "?"))
                    except Exception:
                        pass

        if miscat:
            print(f"  ⚠️  Found {len(miscat)} potentially miscategorized files:\n")
            for fname, folder, should_be in miscat[:5]:
                print(f"    • {folder}/{fname}")
            if len(miscat) > 5:
                print(f"    ... and {len(miscat) - 5} more")
        else:
            print("  ✅ All sampled files appear correctly categorized!\n")

        self.results["miscategorized"] = len(miscat)

    def generate_final_report(self):
        """Generate comprehensive final report."""
        print(f"\n{'🎊'*40}")
        print("║" + " " * 78 + "║")
        print("║" + " " * 20 + "✅ SCAN COMPLETE! ✅" + " " * 21 + "║")
        print("║" + " " * 78 + "║")
        print(f"{'🎊'*40}\n")

        print("📊 FINAL SUMMARY:")
        print("=" * 80)
        print(f"  Total Scripts:        {self.results.get('total_scripts', 0):,}")
        print(f"  Categories:           {self.results.get('categories', 0)}")
        print(f"  Exact Duplicates:     {self.results.get('duplicates', 0)}")
        print(f"  Miscategorized:       {self.results.get('miscategorized', 0)}")

        if "quality_issues" in self.results:
            q = self.results["quality_issues"]
            print(f"\n  Code Quality Issues:")
            print(f"    • Bare excepts:     {q['bare_except']}")
            print(f"    • Magic numbers:    {q['magic_numbers']}")
            print(f"    • Long functions:   {q['long_functions']}")
            print(f"    • Missing docs:     {q['missing_docstrings']}")

        print("=" * 80)

        # Overall health score
        total_issues = sum(self.results.get("quality_issues", {}).values())
        health_score = max(0, 100 - (total_issues // 10))

        print(f"\n🏆 ECOSYSTEM HEALTH SCORE: {health_score}/100")

        if health_score >= 90:
            print("   ✅ EXCELLENT - Production ready!")
        elif health_score >= 70:
            print("   ⚠️  GOOD - Minor improvements needed")
        else:
            print("   ❌ NEEDS WORK - Several issues to address")

        print()

    def run(self):
        """Run complete comprehensive scan."""
        print(f"\n{'🌟'*40}")
        print("║" + " " * 78 + "║")
        print(
            "║"
            + " " * 10
            + "🔍 FINAL COMPREHENSIVE SCAN - ALL TOOLS 🔍"
            + " " * 11
            + "║"
        )
        print("║" + " " * 78 + "║")
        print(f"{'🌟'*40}\n")

        self.scan_directory_structure()
        self.find_exact_duplicates()
        self.analyze_code_quality()
        self.categorization_check()
        self.generate_final_report()


if __name__ == "__main__":
    scanner = FinalComprehensiveScan(str(Path.home()) + "/Documents/python")
    scanner.run()
