"""
advanced_content_analyzer.py
=================================

This module provides a content‑aware analyser for Python projects.  It is
designed to parse a directory of Python files, build an abstract syntax
tree (AST) for each file and extract rich metadata from the code.  In
addition to simple metrics such as the number of functions or classes, it
detects semantic patterns (recursion, loops, async functions), infers
high‑level domains based on imported modules, estimates confidence
scores for its recommendations and heuristically identifies common
design patterns like Singleton, Factory, Observer, Strategy, Decorator and
Context Manager.

The goal of this analyser is to demonstrate how AST‑based static
analysis and lightweight heuristics can be used to derive insights about a
codebase without executing it.  The techniques here are inspired by
research on static analysis pipelines【325992834055423†L242-L258】 and SAST
architecture【685514891648643†L684-L723】, as well as studies showing that
large language models often struggle to infer deeper semantics from code
【535380912601047†L130-L148】.  By combining structural analysis with
domain‑specific heuristics, we can provide meaningful suggestions and
confidence estimates for code improvements.

Usage
-----

Run this script directly to analyse a directory:

    python advanced_content_analyzer.py /path/to/python/project

The analyser will traverse the directory, parse all ``*.py`` files and
write a JSON report to ``analysis_report.json`` in the current working
directory.  The report contains per‑file metrics, inferred domains,
detected patterns, suggestions and confidence scores.

Limitations
-----------

This analyser uses heuristic rules and built‑in libraries only.  It
cannot detect every possible design pattern or semantic nuance, and it
does not perform data‑flow or taint analysis.  It is intended as a
starting point for deeper analysis rather than a complete SAST engine.
"""

from __future__ import annotations

import ast
import os
import json
from typing import Dict, List, Tuple, Optional, Union


class FileMetrics:
    """Container for metrics collected from a Python source file."""

    def __init__(self) -> None:
        self.num_functions: int = 0
        self.num_classes: int = 0
        self.num_imports: int = 0
        self.num_lines: int = 0
        self.num_loops: int = 0
        self.num_async_funcs: int = 0
        self.num_recursive_funcs: int = 0
        self.num_try_blocks: int = 0
        self.has_type_hints: bool = False
        self.has_docstrings: bool = False

        # Collections for further analysis
        self.imported_modules: List[str] = []
        self.function_names: List[str] = []
        self.class_names: List[str] = []
        self.called_functions: Dict[str, List[str]] = {}

    def to_dict(self) -> Dict[str, Union[int, bool, List[str], Dict[str, List[str]]]]:
        """Convert the metrics to a serialisable dictionary."""
        return {
            "num_functions": self.num_functions,
            "num_classes": self.num_classes,
            "num_imports": self.num_imports,
            "num_lines": self.num_lines,
            "num_loops": self.num_loops,
            "num_async_funcs": self.num_async_funcs,
            "num_recursive_funcs": self.num_recursive_funcs,
            "num_try_blocks": self.num_try_blocks,
            "has_type_hints": self.has_type_hints,
            "has_docstrings": self.has_docstrings,
            "imported_modules": self.imported_modules,
            "function_names": self.function_names,
            "class_names": self.class_names,
            "called_functions": self.called_functions,
        }


class ASTAnalyzer(ast.NodeVisitor):
    """AST visitor that collects metrics and detects patterns."""

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.metrics = FileMetrics()
        self.current_function_stack: List[str] = []

    def generic_visit(self, node: ast.AST) -> None:
        # Count loops
        if isinstance(node, (ast.For, ast.While)):  # includes async for
            self.metrics.num_loops += 1
        # Count try/except blocks
        if isinstance(node, ast.Try):
            self.metrics.num_try_blocks += 1
        super().generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        self.metrics.num_imports += 1
        for alias in node.names:
            self.metrics.imported_modules.append(alias.name.split(".")[0])
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        self.metrics.num_imports += 1
        module = node.module or ""
        self.metrics.imported_modules.append(module.split(".")[0])
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.metrics.num_functions += 1
        self.metrics.function_names.append(node.name)
        self.current_function_stack.append(node.name)
        # Docstring
        if ast.get_docstring(node):
            self.metrics.has_docstrings = True
        # Type hints
        if node.returns or any(arg.annotation for arg in node.args.args):
            self.metrics.has_type_hints = True
        # Check for async functions
        if isinstance(node, ast.AsyncFunctionDef):
            self.metrics.num_async_funcs += 1
        # Visit the body to detect recursion and calls
        self.generic_visit(node)
        self.current_function_stack.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        # Reuse FunctionDef logic
        self.visit_FunctionDef(node)  # type: ignore[func-returns-value]

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.metrics.num_classes += 1
        self.metrics.class_names.append(node.name)
        # Docstring for classes
        if ast.get_docstring(node):
            self.metrics.has_docstrings = True
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        # Record function calls for call graph
        caller = (
            self.current_function_stack[-1]
            if self.current_function_stack
            else "<module>"
        )
        func_name = self._get_call_name(node)
        if func_name:
            self.metrics.called_functions.setdefault(caller, []).append(func_name)
        # Check for recursion
        if func_name and func_name in self.current_function_stack:
            self.metrics.num_recursive_funcs += 1
        self.generic_visit(node)

    @staticmethod
    def _get_call_name(node: ast.Call) -> Optional[str]:
        """Resolve the name of the called function if possible."""
        # Handle simple calls like foo()
        if isinstance(node.func, ast.Name):
            return node.func.id
        # Handle method calls like obj.method()
        if isinstance(node.func, ast.Attribute):
            return node.func.attr
        return None


def detect_design_patterns(metrics: FileMetrics) -> List[str]:
    """
    Detect simple design patterns using heuristic rules based on collected
    metrics and naming conventions.  Returns a list of detected pattern names.
    """
    patterns: List[str] = []
    # Singleton: class with a static get_instance or instance attribute
    for cls in metrics.class_names:
        for func_name in metrics.function_names:
            if func_name.lower() in {"get_instance", "instance", "getinstance"}:
                patterns.append("Singleton")
                break
        # Another heuristic: class name ends with Singleton
        if cls.lower().endswith("singleton"):
            patterns.append("Singleton")
            break
    # Factory: presence of functions starting with 'create_' or 'get_' returning classes
    for func in metrics.function_names:
        if func.startswith("create_") or func.startswith("make_"):
            patterns.append("Factory")
            break
    # Observer: functions named 'register', 'unregister', 'notify'
    if {"register", "unregister", "notify"}.intersection(set(metrics.function_names)):
        patterns.append("Observer")
    # Strategy: functions or classes named 'strategy' or containing 'strategy'
    for name in metrics.function_names + metrics.class_names:
        if "strategy" in name.lower():
            patterns.append("Strategy")
            break
    # Decorator: functions whose first argument is a function and return a wrapper
    # We approximate by searching for functions ending with '_decorator'
    for func in metrics.function_names:
        if func.endswith("_decorator") or func.startswith("decorate_"):
            patterns.append("Decorator")
            break
    # Context Manager: presence of classes with __enter__ and __exit__ methods
    # We can't introspect methods easily here, so approximate by class names containing 'context'
    for cls in metrics.class_names:
        if "context" in cls.lower():
            patterns.append("Context Manager")
            break
    return list(set(patterns))


def infer_domain(imports: List[str]) -> Tuple[str, List[str]]:
    """
    Infer a high‑level domain based on imported modules.  Returns a
    tuple of (domain_label, tags).  Domains are intentionally broad and
    based on common Python ecosystems.
    """
    domain = "General"
    tags: List[str] = []
    imp = set(i.lower() for i in imports)
    # Data analysis
    if {"pandas", "numpy", "matplotlib", "scipy", "sklearn"}.intersection(imp):
        domain = "Data Analysis"
        tags.extend(["data-analysis", "data-processing"])
    # Web scraping / networking
    if {"requests", "beautifulsoup", "bs4", "selenium", "scrapy", "lxml"}.intersection(
        imp
    ):
        domain = "Web Scraping"
        tags.extend(["web-scraping", "networking"])
    # API development
    if {"flask", "fastapi", "django", "falcon", "bottle"}.intersection(imp):
        domain = "API Development"
        tags.extend(["api", "web-framework"])
    # Machine learning
    if {"tensorflow", "torch", "keras", "sklearn", "xgboost"}.intersection(imp):
        domain = "Machine Learning"
        tags.extend(["machine-learning", "ai"])
    # Database
    if {"sqlite3", "psycopg2", "mysql", "sqlalchemy"}.intersection(imp):
        domain = "Database"
        tags.extend(["database", "sql"])
    # Image processing
    if {"pillow", "pil", "cv2", "opencv", "skimage"}.intersection(imp):
        domain = "Image Processing"
        tags.extend(["image-processing", "media"])
    # Automation / scripting
    if {"os", "subprocess", "sys", "pathlib", "shutil"}.intersection(
        imp
    ) and domain == "General":
        domain = "Automation"
        tags.extend(["automation", "scripting"])
    if not tags:
        tags.append("general")
    return domain, list(set(tags))


def compute_confidence(metrics: FileMetrics, patterns: List[str], domain: str) -> float:
    '\''
    Compute a confidence score (0.0–1.0) for the analyser's
    recommendations.  The score is based on the presence of docstrings,
    type hints, complexity indicators and detected patterns.  The goal
    is to convey how confident we are that our classification and
    suggestions are appropriate; more well‑structured code tends to
    produce higher confidence.
    """
    score = 0.5
    # Reward presence of documentation and type hints
    if metrics.has_docstrings:
        score += 0.1
    if metrics.has_type_hints:
        score += 0.1
    # Penalise many recursive functions – could indicate complexity
    if metrics.num_recursive_funcs > 0:
        score -= 0.1
    # Reward detection of design patterns (indicates thoughtful design)
    if patterns:
        score += 0.1
    # Reward when domain is not general (clear purpose)
    if domain != "General":
        score += 0.05
    # Bound score between 0 and 1
    return max(0.0, min(1.0, score))


def analyse_python_file(:
    filepath: str,
) -> Dict[
    str,
    Union[
        str,
        Dict[str, Union[int, bool, List[str], Dict[str, List[str]]]],
        float,
        List[str],
    ],
]:
    """
    Analyse a single Python file and return a dictionary with metrics,
    inferred domain, tags, detected patterns, confidence score and
    suggestions for improvement.
    '\''
    metrics = FileMetrics()
    try:
        # Try reading the source file in UTF-8.  If decoding fails,
        # fall back to a permissive encoding.  Some legacy scripts in
        # user repositories may not use UTF-8, so ignoring errors or
        # using latin-1 prevents crashes during analysis.
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                source = f.read()
        except UnicodeDecodeError:
            # Try latin-1 as a fallback and ignore undecodable bytes
            with open(filepath, "r", encoding="latin-1", errors="ignore") as f:
                source = f.read()
        num_lines = len(source.splitlines())
        tree = ast.parse(source, filename=filepath)
        analyzer = ASTAnalyzer(filepath)
        analyzer.visit(tree)
        # Use the metrics collected by the AST analyzer
        metrics = analyzer.metrics
        # Preserve the line count measured earlier.  The AST analyzer
        # does not count lines, so we assign it here to avoid losing the
        # value when replacing the metrics instance.  Without this
        # assignment, num_lines would remain zero in the report.
        metrics.num_lines = num_lines
    except SyntaxError as e:
        # If file can't be parsed, mark as syntax error
        return {
            "file": filepath,
            "error": f"SyntaxError: {e}",  # indicates file needs syntax fix
        }
    # Infer domain and tags
    domain, tags = infer_domain(metrics.imported_modules)
    # Detect design patterns
    patterns = detect_design_patterns(metrics)
    # Compute confidence
    confidence = compute_confidence(metrics, patterns, domain)
    # Generate suggestions
    suggestions: List[str] = []
    # Suggest adding docstrings
    if not metrics.has_docstrings:
        suggestions.append(
            "Add docstrings to functions and classes for better documentation."
        )
    # Suggest adding type hints
    if not metrics.has_type_hints:
        suggestions.append(
            "Add type annotations to function signatures to improve type safety."
        )
    # Suggest refactoring recursive functions if many
    if metrics.num_recursive_funcs > 1:
        suggestions.append(
            "Consider refactoring recursive functions to iterative implementations if possible to reduce complexity."
        )
    # Suggest implementing design patterns if none detected but there are many classes
    if not patterns and metrics.num_classes > 3:
        suggestions.append(
            "Consider applying appropriate design patterns (e.g., Factory, Strategy) to organise classes."
        )
    # Suggest adding error handling
    if metrics.num_try_blocks == 0:
        suggestions.append("Add try/except blocks for robust error handling.")
    # Suggest reducing loops if there are many loops
    if metrics.num_loops > 5:
        suggestions.append(
            "Reduce the number of loops by using comprehensions or vectorised operations where possible."
        )

    return {
        "file": filepath,
        "metrics": metrics.to_dict(),
        "domain": domain,
        "tags": tags,
        "patterns": patterns,
        "confidence": round(confidence, 3),
        "suggestions": suggestions,
    }


def analyse_directory(:
    root_dir: str,
) -> List[
    Dict[
        str,
        Union[
            str,
            float,
            Dict[str, Union[int, bool, List[str], Dict[str, List[str]]]],
            List[str],
        ],
    ]
]:
    """
    Walk through the given directory and analyse all Python files.
    Returns a list of per‑file analysis dictionaries.
    """
    results: List[
        Dict[
            str,
            Union[
                str,
                float,
                Dict[str, Union[int, bool, List[str], Dict[str, List[str]]]],
                List[str],
            ],
        ]
    ] = []
    for dirpath, _, filenames in os.walk(root_dir):
        for name in filenames:
            if name.endswith(".py"):
                filepath = os.path.join(dirpath, name)
                analysis = analyse_python_file(filepath)
                results.append(analysis)
    return results


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyse a Python project for content‑aware metrics and suggestions."
    )
    parser.add_argument(
        "directory", help="Path to the root directory of the Python project"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="analysis_report.json",
        help="Path to write the JSON report",
    )
    args = parser.parse_args()
    results = analyse_directory(args.directory)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Analysis complete. Report written to {args.output}")


if __name__ == "__main__":
    main()
