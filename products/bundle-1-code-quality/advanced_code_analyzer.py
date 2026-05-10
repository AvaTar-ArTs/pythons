#!/usr/bin/env python3
"""
Advanced Python Code Analyzer and Quality Tool
Analyzes Python code for quality, complexity, security, and best practices

Features:
- Code complexity analysis
- Security vulnerability detection
- Best practices checking
- Documentation quality assessment
- Performance optimization suggestions
- Automated refactoring recommendations
"""

import os
import sys
import ast
import json
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
import re
from concurrent.futures import ThreadPoolExecutor, as_completed


def setup_logging(log_file: str = "code_analyzer.log"):
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
    )
    return logging.getLogger(__name__)


@dataclass
class AnalysisConfig:
    """Configuration for code analysis."""

    include_patterns: List[str] = None
    exclude_patterns: List[str] = None
    max_line_length: int = 88
    check_security: bool = True
    check_complexity: bool = True
    check_style: bool = True
    check_documentation: bool = True
    check_performance: bool = True
    max_complexity: int = 10
    min_coverage: float = 0.0
    output_format: str = "json"  # json, text, html

    def __post_init__(self):
        if self.include_patterns is None:
            self.include_patterns = ["*.py"]
        if self.exclude_patterns is None:
            self.exclude_patterns = [
                "node_modules",
                ".git",
                "__pycache__",
                ".venv",
                "venv",
                ".env",
                "build",
                "dist",
                "*.egg-info",
                ".tox",
            ]


class SecurityChecker:
    """Checks for security vulnerabilities in Python code."""

    SECURITY_PATTERNS = {
        "eval_usage": r"\beval\s*\(",
        "exec_usage": r"\bexec\s*\(",
        "pickle_load": r"\bpickle\.loads?\s*\(",
        "shell_injection": r"(os\.system|subprocess\.(call|run|Popen))\s*\([^,]*\+",
        "hardcoded_password": r"[Pp]assword\s*=",
        "hardcoded_secret": r"[Ss]ecret|[_]?[Aa]pi[_]?[Kk]ey|[_]?[Tt]oken",
        "insecure_ssl": r"ssl\.create_default_context\(\)|ssl\.PROTOCOL_SSLv\d+",
        "unsafe_deserialization": r"yaml\.load\s*\(",
    }

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def check_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Check a file for security issues."""
        issues = []

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            for issue_type, pattern in self.SECURITY_PATTERNS.items():
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    line_no = content[: match.start()].count("\n") + 1
                    issues.append(
                        {
                            "type": issue_type,
                            "severity": (
                                "high"
                                if issue_type
                                in ["eval_usage", "exec_usage", "shell_injection"]
                                else "medium"
                            ),
                            "line": line_no,
                            "column": match.start()
                            - content.rfind("\n", 0, match.start())
                            - 1,
                            "message": f"Potential security issue: {issue_type}",
                            "code": (
                                content.split("\n")[line_no - 1].strip()
                                if line_no <= len(content.split("\n"))
                                else ""
                            ),
                        }
                    )
        except Exception as e:
            self.logger.warning(f"Could not analyze {file_path} for security: {e}")

        return issues


class ComplexityAnalyzer:
    """Analyzes code complexity using AST."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity of a node."""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):  # and/or expressions
                complexity += len(child.values) - 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1

        return complexity

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze complexity of a Python file."""
        results = {
            "file": str(file_path),
            "overall_complexity": 0,
            "function_complexities": [],
            "class_complexities": [],
            "issues": [],
        }

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            # Calculate overall complexity
            results["overall_complexity"] = self.calculate_complexity(tree)

            # Analyze functions and classes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    complexity = self.calculate_complexity(node)
                    results["function_complexities"].append(
                        {
                            "name": node.name,
                            "complexity": complexity,
                            "line_start": node.lineno,
                            "line_end": getattr(node, "end_lineno", node.lineno),
                        }
                    )

                    if complexity > 10:  # High complexity threshold
                        results["issues"].append(
                            {
                                "type": "high_complexity_function",
                                "severity": "medium",
                                "function": node.name,
                                "complexity": complexity,
                                "message": (
                                    f"Function {node.name} has high complexity ({complexity})"
                                ),
                                "line": node.lineno,
                            }
                        )

                elif isinstance(node, ast.AsyncFunctionDef):
                    complexity = self.calculate_complexity(node)
                    results["function_complexities"].append(
                        {
                            "name": node.name,
                            "complexity": complexity,
                            "line_start": node.lineno,
                            "line_end": getattr(node, "end_lineno", node.lineno),
                        }
                    )

                    if complexity > 10:
                        results["issues"].append(
                            {
                                "type": "high_complexity_function",
                                "severity": "medium",
                                "function": node.name,
                                "complexity": complexity,
                                "message": (
                                    f"Async function {node.name} has high complexity ({complexity})"
                                ),
                                "line": node.lineno,
                            }
                        )

                elif isinstance(node, ast.ClassDef):
                    class_complexity = 1  # Base complexity for class
                    method_count = 0
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            class_complexity += self.calculate_complexity(item)
                            method_count += 1

                    results["class_complexities"].append(
                        {
                            "name": node.name,
                            "complexity": class_complexity,
                            "methods": method_count,
                            "line_start": node.lineno,
                            "line_end": getattr(node, "end_lineno", node.lineno),
                        }
                    )

                    if class_complexity > 50:  # High class complexity threshold
                        results["issues"].append(
                            {
                                "type": "high_complexity_class",
                                "severity": "medium",
                                "class": node.name,
                                "complexity": class_complexity,
                                "message": (
                                    f"Class {node.name} has high complexity ({class_complexity})"
                                ),
                                "line": node.lineno,
                            }
                        )

        except SyntaxError as e:
            results["issues"].append(
                {
                    "type": "syntax_error",
                    "severity": "high",
                    "message": f"Syntax error: {e.msg}",
                    "line": e.lineno or 0,
                }
            )
        except Exception as e:
            self.logger.warning(f"Could not analyze complexity of {file_path}: {e}")

        return results


class StyleChecker:
    """Checks code style and formatting."""

    def __init__(self, logger: logging.Logger, max_line_length: int = 88):
        self.logger = logger
        self.max_line_length = max_line_length

    def check_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Check style issues in a file."""
        issues = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for i, line in enumerate(lines, 1):
                stripped = line.rstrip("\n\r")

                # Check line length
                if len(stripped) > self.max_line_length:
                    issues.append(
                        {
                            "type": "line_too_long",
                            "severity": "low",
                            "line": i,
                            "column": self.max_line_length + 1,
                            "message": f"Line too long ({len(stripped)} > {self.max_line_length})",
                            "code": (
                                stripped[:50] + "..."
                                if len(stripped) > 50
                                else stripped
                            ),
                        }
                    )

                # Check for trailing whitespace
                if line != line.rstrip():
                    issues.append(
                        {
                            "type": "trailing_whitespace",
                            "severity": "low",
                            "line": i,
                            "column": len(line.rstrip()) + 1,
                            "message": "Trailing whitespace",
                            "code": line.rstrip(),
                        }
                    )

                # Check for tabs vs spaces
                if "\t" in line:
                    issues.append(
                        {
                            "type": "tab_character",
                            "severity": "low",
                            "line": i,
                            "column": line.index("\t") + 1,
                            "message": "Tab character found (use spaces instead)",
                            "code": (
                                stripped[:50] + "..."
                                if len(stripped) > 50
                                else stripped
                            ),
                        }
                    )

        except Exception as e:
            self.logger.warning(f"Could not analyze style of {file_path}: {e}")

        return issues


class DocumentationChecker:
    """Checks documentation quality."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze documentation in a file."""
        results = {
            "file": str(file_path),
            "has_module_docstring": False,
            "function_docstrings": [],
            "missing_docstrings": [],
            "docstring_issues": [],
        }

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            # Check for module docstring
            if (
                tree.body
                and isinstance(tree.body[0], ast.Expr)
                and isinstance(tree.body[0].value, ast.Str)
            ):
                results["has_module_docstring"] = True

            # Check functions and classes for docstrings
            for node in ast.walk(tree):
                if isinstance(
                    node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
                ):
                    has_docstring = False
                    if (
                        len(node.body) > 0
                        and isinstance(node.body[0], ast.Expr)
                        and isinstance(node.body[0].value, ast.Str)
                    ):
                        has_docstring = True

                    item_info = {
                        "name": node.name,
                        "type": type(node).__name__.lower().replace("def", ""),
                        "has_docstring": has_docstring,
                        "line": node.lineno,
                    }

                    if node.name.startswith("__") and node.name.endswith("__"):
                        # Skip magic methods
                        continue

                    if has_docstring:
                        results["function_docstrings"].append(item_info)
                    else:
                        results["missing_docstrings"].append(item_info)
                        results["docstring_issues"].append(
                            {
                                "type": "missing_docstring",
                                "severity": "medium",
                                "item": node.name,
                                "item_type": type(node)
                                .__name__.lower()
                                .replace("def", ""),
                                "message": (
                                    "Missing docstring for "
                                    f'{type(node).__name__.lower().replace("def", "")} '
                                    f"{node.name}"
                                ),
                                "line": node.lineno,
                            }
                        )

        except Exception as e:
            self.logger.warning(f"Could not analyze documentation of {file_path}: {e}")

        return results


class PerformanceChecker:
    """Checks for performance issues."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def check_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Check performance issues in a file."""
        issues = []

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Check for inefficient patterns
            patterns = {
                "inefficient_loop": r"for.*in.*range\(len\(",
                "inefficient_list_creation": r"\[\]\s*=\s*\[\]",
                "inefficient_string_concat": r's \+=\s*[\'"].*[\'"]',
                "inefficient_import_in_loop": r"for.*:\s*import|for.*:\s*from.*import",
                "inefficient_dict_access": r"\[.*\]\s*=\s*\[.*\].*\[.*\].*if.*\[.*\]",
            }

            for issue_type, pattern in patterns.items():
                matches = re.finditer(pattern, content, re.MULTILINE)
                for match in matches:
                    line_no = content[: match.start()].count("\n") + 1
                    issues.append(
                        {
                            "type": issue_type,
                            "severity": "medium",
                            "line": line_no,
                            "column": match.start()
                            - content.rfind("\n", 0, match.start())
                            - 1,
                            "message": f"Potential performance issue: {issue_type}",
                            "code": (
                                content.split("\n")[line_no - 1].strip()
                                if line_no <= len(content.split("\n"))
                                else ""
                            ),
                        }
                    )

        except Exception as e:
            self.logger.warning(f"Could not analyze performance of {file_path}: {e}")

        return issues


class AdvancedCodeAnalyzer:
    """Main class that combines all analysis tools."""

    def __init__(self, config: AnalysisConfig = None):
        self.config = config or AnalysisConfig()
        self.logger = setup_logging()
        self.security_checker = SecurityChecker(self.logger)
        self.complexity_analyzer = ComplexityAnalyzer(self.logger)
        self.style_checker = StyleChecker(self.logger, self.config.max_line_length)
        self.documentation_checker = DocumentationChecker(self.logger)
        self.performance_checker = PerformanceChecker(self.logger)

    def matches_pattern(self, path: Path, patterns: List[str]) -> bool:
        """Check if path matches any of the given patterns."""
        path_str = str(path)
        for pattern in patterns:
            if "*" in pattern or "?" in pattern or "[" in pattern:
                if Path(path_str).match(pattern):
                    return True
            elif pattern in path_str:
                return True
        return False

    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        return self.matches_pattern(path, self.config.exclude_patterns)

    def should_include(self, path: Path) -> bool:
        """Check if path should be included."""
        return self.matches_pattern(path, self.config.include_patterns)

    def find_python_files(self, root_path: Path) -> List[Path]:
        """Find all Python files in the directory tree."""
        python_files = []

        for root, dirs, files in os.walk(root_path):
            # Prune directories that match exclude patterns
            dirs[:] = [d for d in dirs if not self.should_exclude(Path(root) / d)]

            for file in files:
                file_path = Path(root) / file

                if self.should_exclude(file_path):
                    continue

                if self.should_include(file_path):
                    python_files.append(file_path)

        return python_files

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single file for all aspects."""
        results = {
            "file": str(file_path),
            "security_issues": [],
            "complexity_analysis": {},
            "style_issues": [],
            "documentation_analysis": {},
            "performance_issues": [],
        }

        # Run all checks
        if self.config.check_security:
            results["security_issues"] = self.security_checker.check_file(file_path)

        if self.config.check_complexity:
            results["complexity_analysis"] = self.complexity_analyzer.analyze_file(
                file_path
            )

        if self.config.check_style:
            results["style_issues"] = self.style_checker.check_file(file_path)

        if self.config.check_documentation:
            results["documentation_analysis"] = self.documentation_checker.analyze_file(
                file_path
            )

        if self.config.check_performance:
            results["performance_issues"] = self.performance_checker.check_file(
                file_path
            )

        return results

    def analyze_directory(self, root_path: Path) -> Dict[str, Any]:
        """Analyze all Python files in a directory."""
        python_files = self.find_python_files(root_path)

        self.logger.info(f"Found {len(python_files)} Python files to analyze")

        # Analyze files in parallel
        all_results = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_path = {
                executor.submit(self.analyze_file, file_path): file_path
                for file_path in python_files
            }

            for future in as_completed(future_to_path):
                file_path = future_to_path[future]
                try:
                    result = future.result()
                    all_results.append(result)

                    if len(all_results) % 10 == 0:
                        self.logger.info(
                            f"Analyzed {len(all_results)}/{len(python_files)} files..."
                        )

                except Exception as e:
                    self.logger.error(f"Error analyzing {file_path}: {e}")

        # Compile overall statistics
        stats = self.compile_statistics(all_results)

        final_results = {
            "timestamp": str(datetime.now()),
            "directory": str(root_path),
            "config": self.config.__dict__,
            "files_analyzed": len(all_results),
            "statistics": stats,
            "details": all_results,
        }

        return final_results

    def compile_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compile statistics from all analysis results."""
        stats = {
            "total_files": len(results),
            "security_issues": 0,
            "style_issues": 0,
            "performance_issues": 0,
            "missing_docstrings": 0,
            "high_complexity_functions": 0,
            "high_complexity_classes": 0,
            "total_complexity": 0,
            "avg_complexity": 0,
            "severe_issues": 0,
            "high_issues": 0,
            "medium_issues": 0,
            "low_issues": 0,
        }

        severity_counts = {"high": 0, "medium": 0, "low": 0}

        for result in results:
            # Count security issues
            stats["security_issues"] += len(result.get("security_issues", []))

            # Count style issues
            stats["style_issues"] += len(result.get("style_issues", []))

            # Count performance issues
            stats["performance_issues"] += len(result.get("performance_issues", []))

            # Count documentation issues
            doc_analysis = result.get("documentation_analysis", {})
            missing_docs = doc_analysis.get("missing_docstrings", [])
            stats["missing_docstrings"] += len(missing_docs)

            # Count complexity issues
            complexity_analysis = result.get("complexity_analysis", {})
            func_complexities = complexity_analysis.get("function_complexities", [])
            class_complexities = complexity_analysis.get("class_complexities", [])

            for func in func_complexities:
                if func["complexity"] > 10:
                    stats["high_complexity_functions"] += 1

            for cls in class_complexities:
                if cls["complexity"] > 50:
                    stats["high_complexity_classes"] += 1

            stats["total_complexity"] += complexity_analysis.get(
                "overall_complexity", 0
            )

            # Count severity levels
            for issue_list in [
                result.get("security_issues", []),
                result.get("style_issues", []),
                result.get("performance_issues", []),
            ]:
                for issue in issue_list:
                    severity = issue.get("severity", "low")
                    if severity in severity_counts:
                        severity_counts[severity] += 1

        if stats["total_files"] > 0:
            stats["avg_complexity"] = stats["total_complexity"] / stats["total_files"]

        stats.update(severity_counts)
        stats["severe_issues"] = severity_counts["high"]

        return stats

    def generate_report(self, results: Dict[str, Any], output_path: Path = None):
        """Generate a report in the specified format."""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = Path(f"code_analysis_report_{timestamp}.json")

        if self.config.output_format == "json":
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, default=str)
        elif self.config.output_format == "text":
            self._generate_text_report(results, output_path)
        elif self.config.output_format == "html":
            self._generate_html_report(results, output_path)

        self.logger.info(f"Analysis report saved to: {output_path}")

    def _generate_text_report(self, results: Dict[str, Any], output_path: Path):
        """Generate a text report."""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("Python Code Analysis Report\n")
            f.write("=" * 50 + "\n\n")

            stats = results["statistics"]
            f.write(f"Directory: {results['directory']}\n")
            f.write(f"Files analyzed: {stats['total_files']}\n")
            f.write(f"Timestamp: {results['timestamp']}\n\n")

            f.write("Statistics:\n")
            f.write(f"  Security issues: {stats['security_issues']}\n")
            f.write(f"  Style issues: {stats['style_issues']}\n")
            f.write(f"  Performance issues: {stats['performance_issues']}\n")
            f.write(f"  Missing docstrings: {stats['missing_docstrings']}\n")
            f.write(
                f"  High complexity functions: {stats['high_complexity_functions']}\n"
            )
            f.write(f"  High complexity classes: {stats['high_complexity_classes']}\n")
            f.write(f"  Average complexity: {stats['avg_complexity']:.2f}\n\n")

            f.write("Severity breakdown:\n")
            f.write(f"  High: {stats['high']}\n")
            f.write(f"  Medium: {stats['medium']}\n")
            f.write(f"  Low: {stats['low']}\n\n")


def main():
    """Main entry point with command-line interface."""
    parser = argparse.ArgumentParser(
        description="Advanced Python Code Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python advanced_code_analyzer.py /path/to/project              # Analyze project
  python advanced_code_analyzer.py /path/to/project --security   # Security-focused analysis
  python advanced_code_analyzer.py /path/to/project --format html # HTML report
  python advanced_code_analyzer.py /path/to/project --max-complexity 5 # Strict complexity
        """,
    )

    parser.add_argument("directory", help="Directory to analyze")
    parser.add_argument(
        "--security", action="store_true", help="Check for security issues"
    )
    parser.add_argument(
        "--complexity", action="store_true", help="Check code complexity"
    )
    parser.add_argument("--style", action="store_true", help="Check code style")
    parser.add_argument(
        "--documentation", action="store_true", help="Check documentation"
    )
    parser.add_argument(
        "--performance", action="store_true", help="Check performance issues"
    )
    parser.add_argument(
        "--max-complexity", type=int, default=10, help="Maximum complexity threshold"
    )
    parser.add_argument(
        "--line-length", type=int, default=88, help="Maximum line length"
    )
    parser.add_argument(
        "--format",
        choices=["json", "text", "html"],
        default="json",
        help="Output format",
    )
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--include", action="append", help="Include pattern")
    parser.add_argument("--exclude", action="append", help="Exclude pattern")

    args = parser.parse_args()

    # Create configuration
    config = AnalysisConfig(
        include_patterns=args.include,
        exclude_patterns=args.exclude,
        max_line_length=args.line_length,
        check_security=args.security
        or not any([args.complexity, args.style, args.documentation, args.performance]),
        check_complexity=args.complexity
        or not any([args.security, args.style, args.documentation, args.performance]),
        check_style=args.style
        or not any(
            [args.security, args.complexity, args.documentation, args.performance]
        ),
        check_documentation=args.documentation
        or not any([args.security, args.complexity, args.style, args.performance]),
        check_performance=args.performance
        or not any([args.security, args.complexity, args.style, args.documentation]),
        max_complexity=args.max_complexity,
        output_format=args.format,
    )

    # Run analysis
    analyzer = AdvancedCodeAnalyzer(config)

    try:
        results = analyzer.analyze_directory(Path(args.directory))

        # Generate report
        output_path = Path(args.output) if args.output else None
        analyzer.generate_report(results, output_path)

        # Print summary
        stats = results["statistics"]
        print("\n📊 Code Analysis Summary:")
        print(f"   Files analyzed: {stats['total_files']:,}")
        print(f"   Security issues: {stats['security_issues']:,}")
        print(f"   Style issues: {stats['style_issues']:,}")
        print(f"   Performance issues: {stats['performance_issues']:,}")
        print(f"   Missing docstrings: {stats['missing_docstrings']:,}")
        print(f"   Average complexity: {stats['avg_complexity']:.2f}")
        print(f"   High severity issues: {stats['high']:,}")

        report_name = output_path or (
            f"code_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        print(f"\n✅ Analysis completed! Report saved to: {report_name}")

    except KeyboardInterrupt:
        print("\n⚠️  Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    from datetime import datetime

    main()
