
import os
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class Config:
    """Configuration management."""
    def __init__(self):
        """__init__ function."""
        self._config = {}
        self._load_from_env()

    def _load_from_env(self):
        """Load configuration from environment variables."""
        for key, value in os.environ.items():
            if key.startswith('APP_'):
                self._config[key[4:].lower()] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config[key] = value

config = Config()
# TODO: Resolve circular dependencies by restructuring imports

# String constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"


# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_PORT = 8080

# TODO: Consider extracting methods from long functions
# TODO: Consider breaking down this class into smaller, focused classes

from functools import wraps

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @wraps(func)
        """wrapper function."""
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def retry_decorator(max_retries = 3):
    """decorator function."""
    """Decorator to retry function on failure."""
        """wrapper function."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
            return None
        return wrapper
    return decorator

#!/usr/bin/env python3
"""
Focused Quality Analyzer
========================

Analyzes only the original Python files in the main directory structure, 
excluding backup directories and generated files.

Author: Enhanced by Claude
Version: 1.0
"""

import os
import sys
import ast
import re
import logging
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import argparse

# Configure logging
logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class FileAnalysis:
    """Analysis results for a single Python file."""
    file_path: str
    lines_of_code: int
    functions: int
    classes: int
    imports: int
    has_docstrings: bool
    has_type_hints: bool
    has_error_handling: bool
    has_logging: bool
    complexity_score: int
    quality_score: int
    issues: List[str]
    recommendations: List[str]

@dataclass
class CodebaseMetrics:
    """Overall codebase metrics."""
    total_files: int
    total_lines: int
    total_functions: int
    total_classes: int
    files_with_docstrings: int
    files_with_type_hints: int
    files_with_error_handling: int
    files_with_logging: int
    average_complexity: float
    average_quality: float
    common_issues: List[Tuple[str, int]]
    improvement_priorities: List[str]

class FocusedQualityAnalyzer:
    """__init__ function."""
    """Focused analyzer for original Python files only."""

    def __init__(self, base_path: str, max_depth: int = 3):
        self.base_path = Path(base_path)
        self.max_depth = max_depth
        self.analysis_results: List[FileAnalysis] = []
        self.metrics: Optional[CodebaseMetrics] = None

        # Directories to exclude
        self.excluded_dirs = {
            'backup_before_fixes', 
            'backup_before_quality_improvements', 
            'backup_advanced_enhancements', 
            'backup_batch_improvements', 
            '__pycache__', 
            '.git', 
            '.pytest_cache', 
            'venv', 
            'env', 
            '.venv', 
            '.env', 
            'node_modules', 
            'tests', 
            'test_', 
            'generated_', 
            'temp_', 
            'tmp_'
        }

    def get_original_python_files(self) -> List[Path]:
        """Get only the original Python files, excluding backups and generated files."""
        python_files = []

        for root, dirs, files in os.walk(self.base_path):
            # Calculate depth
            depth = root.replace(str(self.base_path), '').count(os.sep)

            # Skip if too deep
            if depth > self.max_depth:
                continue

            # Remove excluded directories from dirs list to prevent walking into them
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]

            # Check if this directory should be excluded
            if any(excluded in root for excluded in self.excluded_dirs):
                continue

            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    python_files.append(file_path)

        return python_files

    def analyze_file(self, file_path: Path) -> FileAnalysis:
        """Analyze a single Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse AST
            try:
                tree = ast.parse(content)
            except SyntaxError:
                return FileAnalysis(
                    file_path = str(file_path), 
                    lines_of_code = len(content.splitlines()), 
                    functions = 0, 
                    classes = 0, 
                    imports = 0, 
                    has_docstrings = False, 
                    has_type_hints = False, 
                    has_error_handling = False, 
                    has_logging = False, 
                    complexity_score = 0, 
                    quality_score = 0, 
                    issues=["Syntax Error"], 
                    recommendations=["Fix syntax errors"]
                )

            # Count basic metrics
            lines_of_code = len([line for line in content.splitlines() if line.strip()])
            functions = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
            classes = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
            imports = len([node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))])

            # Check for docstrings
            has_docstrings = self._has_docstrings(tree)

            # Check for type hints
            has_type_hints = self._has_type_hints(content)

            # Check for error handling
            has_error_handling = self._has_error_handling(tree)

            # Check for logging
            has_logging = 'logging' in content.lower() or 'logger.' in content

            # Calculate complexity score
            complexity_score = self._calculate_complexity(tree)

            # Identify issues
            issues = self._identify_issues(content, tree)

            # Generate recommendations
            recommendations = self._generate_recommendations(issues, has_docstrings, has_type_hints, has_error_handling, has_logging)

            # Calculate quality score
            quality_score = self._calculate_quality_score(
                has_docstrings, has_type_hints, has_error_handling, has_logging, 
                complexity_score, len(issues)
            )

            return FileAnalysis(
                file_path = str(file_path), 
                lines_of_code = lines_of_code, 
                functions = functions, 
                classes = classes, 
                imports = imports, 
                has_docstrings = has_docstrings, 
                has_type_hints = has_type_hints, 
                has_error_handling = has_error_handling, 
                has_logging = has_logging, 
                complexity_score = complexity_score, 
                quality_score = quality_score, 
                issues = issues, 
                recommendations = recommendations
            )

        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            return FileAnalysis(
                file_path = str(file_path), 
                lines_of_code = 0, 
                functions = 0, 
                classes = 0, 
                imports = 0, 
                has_docstrings = False, 
                has_type_hints = False, 
                has_error_handling = False, 
                has_logging = False, 
                complexity_score = 0, 
                quality_score = 0, 
                issues=[f"Analysis Error: {e}"], 
                recommendations=["Fix analysis errors"]
            )

    def _has_docstrings(self, tree: ast.AST) -> bool:
        """Check if file has docstrings."""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                if (node.body and isinstance(node.body[0], ast.Expr) and
                    isinstance(node.body[0].value, ast.Constant) and
                    isinstance(node.body[0].value.value, str)):
                    return True
        return False

    def _has_type_hints(self, content: str) -> bool:
        """Check if file has type hints."""
        type_hint_patterns = [
            r'def\s+\w+\([^)]*:\s*\w+', 
            r'->\s*\w+', 
            r':\s*List\[', 
            r':\s*Dict\[', 
            r':\s*Optional\[', 
            r':\s*Union\[', 
            r':\s*Tuple\['
        ]
        return any(re.search(pattern, content) for pattern in type_hint_patterns)

    def _has_error_handling(self, tree: ast.AST) -> bool:
        """Check if file has error handling."""
        for node in ast.walk(tree):
            if isinstance(node, (ast.Try, ast.ExceptHandler)):
                return True
        return False

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1  # Base complexity

        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, (ast.And, ast.Or)):
                complexity += 1

        return complexity

    def _identify_issues(self, content: str, tree: ast.AST) -> List[str]:
        """Identify common code issues."""
        issues = []

        # Check for hardcoded values
        if re.search(r'["\']/[^"\']*["\']', content):
            issues.append("Hardcoded file paths")

        # Check for print statements
        if 'print(' in content and 'logging' not in content.lower():
            issues.append("Using print instead of logging")

        # Check for bare except
        if re.search(r'except\s*:', content):
            issues.append("Bare except clauses")

        # Check for long functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.body) > 20:
                    issues.append("Long function detected")

        # Check for missing docstrings
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not (node.body and isinstance(node.body[0], ast.Expr) and
                       isinstance(node.body[0].value, ast.Constant) and
                       isinstance(node.body[0].value.value, str)):
                    issues.append("Missing docstring")

        # Check for global variables
        if re.search(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*=', content, re.MULTILINE):
            issues.append("Global variables detected")

        # Check for magic numbers
        if re.search(r'\b\d{3, }\b', content):
            issues.append("Magic numbers detected")

        return issues

    def _generate_recommendations(self, issues: List[str], has_docstrings: bool, 
                                has_type_hints: bool, has_error_handling: bool, 
                                has_logging: bool) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []

        if not has_docstrings:
            recommendations.append("Add docstrings to functions and classes")

        if not has_type_hints:
            recommendations.append("Add type hints for better code clarity")

        if not has_error_handling:
            recommendations.append("Add proper error handling with try-except blocks")

        if not has_logging:
            recommendations.append("Replace print statements with proper logging")

        if "Hardcoded file paths" in issues:
            recommendations.append("Use configuration files for file paths")

        if "Bare except clauses" in issues:
            recommendations.append("Specify exception types in except clauses")

        if "Long function detected" in issues:
            recommendations.append("Break down long functions into smaller ones")

        if "Global variables detected" in issues:
            recommendations.append("Avoid global variables, use classes or functions")

        if "Magic numbers detected" in issues:
            recommendations.append("Replace magic numbers with named constants")

        return recommendations

    def _calculate_quality_score(self, has_docstrings: bool, has_type_hints: bool, 
                               has_error_handling: bool, has_logging: bool, 
                               complexity_score: int, issue_count: int) -> int:
        """Calculate overall quality score (0-100)."""
        score = 0

        # Base score for having code
        score += 20

        # Documentation
        if has_docstrings:
            score += 15

        # Type safety
        if has_type_hints:
            score += 15

        # Error handling
        if has_error_handling:
            score += 15

        # Logging
        if has_logging:
            score += 10

        # Complexity penalty
        if complexity_score > 10:
            score -= min(20, (complexity_score - 10) * 2)

        # Issue penalty
        score -= min(25, issue_count * 2)

        return max(0, min(100, score))

    def analyze_codebase(self) -> CodebaseMetrics:
        """Analyze the focused codebase."""
        logger.info(f"Analyzing focused codebase at: {self.base_path}")

        # Get only original Python files
        python_files = self.get_original_python_files()
        logger.info(f"Found {len(python_files)} original Python files")

        # Analyze each file
        for i, file_path in enumerate(python_files):
            if i % 100 == 0:
                logger.info(f"Analyzed {i}/{len(python_files)} files")

            analysis = self.analyze_file(file_path)
            self.analysis_results.append(analysis)

        # Calculate overall metrics
        self.metrics = self._calculate_metrics()

        logger.info("Focused analysis complete!")
        return self.metrics

    def _calculate_metrics(self) -> CodebaseMetrics:
        """Calculate overall codebase metrics."""
        total_files = len(self.analysis_results)
        total_lines = sum(r.lines_of_code for r in self.analysis_results)
        total_functions = sum(r.functions for r in self.analysis_results)
        total_classes = sum(r.classes for r in self.analysis_results)

        files_with_docstrings = sum(1 for r in self.analysis_results if r.has_docstrings)
        files_with_type_hints = sum(1 for r in self.analysis_results if r.has_type_hints)
        files_with_error_handling = sum(1 for r in self.analysis_results if r.has_error_handling)
        files_with_logging = sum(1 for r in self.analysis_results if r.has_logging)

        average_complexity = sum(r.complexity_score for r in self.analysis_results) / total_files if total_files > 0 else 0
        average_quality = sum(r.quality_score for r in self.analysis_results) / total_files if total_files > 0 else 0

        # Count common issues
        all_issues = []
        for result in self.analysis_results:
            all_issues.extend(result.issues)

        from collections import Counter
        issue_counts = Counter(all_issues)
        common_issues = issue_counts.most_common(10)

        # Generate improvement priorities
        improvement_priorities = self._generate_improvement_priorities()

        return CodebaseMetrics(
            total_files = total_files, 
            total_lines = total_lines, 
            total_functions = total_functions, 
            total_classes = total_classes, 
            files_with_docstrings = files_with_docstrings, 
            files_with_type_hints = files_with_type_hints, 
            files_with_error_handling = files_with_error_handling, 
            files_with_logging = files_with_logging, 
            average_complexity = average_complexity, 
            average_quality = average_quality, 
            common_issues = common_issues, 
            improvement_priorities = improvement_priorities
        )

    def _generate_improvement_priorities(self) -> List[str]:
        """Generate improvement priorities based on analysis."""
        priorities = []

        # Calculate percentages
        total_files = len(self.analysis_results)
        if total_files == 0:
            return priorities

        docstring_pct = sum(1 for r in self.analysis_results if r.has_docstrings) / total_files * 100
        type_hint_pct = sum(1 for r in self.analysis_results if r.has_type_hints) / total_files * 100
        error_handling_pct = sum(1 for r in self.analysis_results if r.has_error_handling) / total_files * 100
        logging_pct = sum(1 for r in self.analysis_results if r.has_logging) / total_files * 100

        if docstring_pct < 50:
            priorities.append("HIGH: Add documentation - only {:.1f}% of files have docstrings".format(docstring_pct))

        if type_hint_pct < 20:
            priorities.append("HIGH: Add type hints - only {:.1f}% of files have type hints".format(type_hint_pct))

        if error_handling_pct < 60:
            priorities.append("MEDIUM: Improve error handling - only {:.1f}% of files have error handling".format(error_handling_pct))

        if logging_pct < 30:
            priorities.append("MEDIUM: Add logging - only {:.1f}% of files use logging".format(logging_pct))

        # Check for common issues
        all_issues = []
        for result in self.analysis_results:
            all_issues.extend(result.issues)

        from collections import Counter
        issue_counts = Counter(all_issues)
        if issue_counts.get("Hardcoded file paths", 0) > total_files * 0.3:
            priorities.append("HIGH: Replace hardcoded paths with configuration")

        if issue_counts.get("Using print instead of logging", 0) > total_files * 0.4:
            priorities.append("MEDIUM: Replace print statements with logging")

        return priorities

    def generate_report(self, output_dir: str = "focused_analysis_output"):
        """Generate focused analysis report."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok = True)

        # Generate CSV report
        self._generate_csv_report(output_path)

        # Generate JSON report
        self._generate_json_report(output_path)

        # Generate markdown report
        self._generate_markdown_report(output_path)

        logger.info(f"Focused reports generated in: {output_path}")

    def _generate_csv_report(self, output_path: Path):
        """Generate CSV report of file analysis."""
        csv_file = output_path / "focused_file_analysis.csv"

        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            import csv
            writer = csv.writer(f)
            writer.writerow([
                'File Path', 'Lines of Code', 'Functions', 'Classes', 'Imports', 
                'Has Docstrings', 'Has Type Hints', 'Has Error Handling', 'Has Logging', 
                'Complexity Score', 'Quality Score', 'Issues Count', 'Issues', 'Recommendations'
            ])

            for result in self.analysis_results:
                writer.writerow([
                    result.file_path, 
                    result.lines_of_code, 
                    result.functions, 
                    result.classes, 
                    result.imports, 
                    result.has_docstrings, 
                    result.has_type_hints, 
                    result.has_error_handling, 
                    result.has_logging, 
                    result.complexity_score, 
                    result.quality_score, 
                    len(result.issues), 
                    '; '.join(result.issues), 
                    '; '.join(result.recommendations)
                ])

    def _generate_json_report(self, output_path: Path):
        """Generate JSON report of analysis results."""
        json_file = output_path / "focused_analysis_results.json"

        report_data = {
            'timestamp': datetime.now().isoformat(), 
            'metrics': asdict(self.metrics), 
            'file_analysis': [asdict(result) for result in self.analysis_results]
        }

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent = 2, ensure_ascii = False)

    def _generate_markdown_report(self, output_path: Path):
        """Generate markdown report."""
        md_file = output_path / "focused_analysis_report.md"

        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("# Focused Python Codebase Analysis Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Overview
            f.write("## Overview\n\n")
            f.write(f"- **Total Files:** {self.metrics.total_files:, }\n")
            f.write(f"- **Total Lines of Code:** {self.metrics.total_lines:, }\n")
            f.write(f"- **Total Functions:** {self.metrics.total_functions:, }\n")
            f.write(f"- **Total Classes:** {self.metrics.total_classes:, }\n\n")

            # Quality Metrics
            f.write("## Quality Metrics\n\n")
            f.write(f"- **Files with Docstrings:** {self.metrics.files_with_docstrings:, } ({self.metrics.files_with_docstrings/self.metrics.total_files*100:.1f}%)\n")
            f.write(f"- **Files with Type Hints:** {self.metrics.files_with_type_hints:, } ({self.metrics.files_with_type_hints/self.metrics.total_files*100:.1f}%)\n")
            f.write(f"- **Files with Error Handling:** {self.metrics.files_with_error_handling:, } ({self.metrics.files_with_error_handling/self.metrics.total_files*100:.1f}%)\n")
            f.write(f"- **Files with Logging:** {self.metrics.files_with_logging:, } ({self.metrics.files_with_logging/self.metrics.total_files*100:.1f}%)\n")
            f.write(f"- **Average Complexity:** {self.metrics.average_complexity:.1f}\n")
            f.write(f"- **Average Quality Score:** {self.metrics.average_quality:.1f}/100\n\n")

            # Common Issues
            f.write("## Common Issues\n\n")
            for issue, count in self.metrics.common_issues:
                f.write(f"- **{issue}:** {count:, } files\n")
            f.write("\n")

            # Improvement Priorities
            f.write("## Improvement Priorities\n\n")
            for i, priority in enumerate(self.metrics.improvement_priorities, 1):
                f.write(f"{i}. {priority}\n")
            f.write("\n")

            # Top Quality Files
            f.write("## Top Quality Files\n\n")
            top_files = sorted(self.analysis_results, key = lambda x: x.quality_score, reverse = True)[:10]
            for i, result in enumerate(top_files, 1):
                f.write(f"{i}. **{Path(result.file_path).name}** (Score: {result.quality_score}/100)\n")
            f.write("\n")

            # Files Needing Most Improvement
            f.write("## Files Needing Most Improvement\n\n")
            bottom_files = sorted(self.analysis_results, key = lambda x: x.quality_score)[:10]
            for i, result in enumerate(bottom_files, 1):
                f.write(f"{i}. **{Path(result.file_path).name}** (Score: {result.quality_score}/100)\n")
                if result.issues:
                    f.write(f"   - Issues: {', '.join(result.issues[:3])}\n")
                if result.recommendations:
                    f.write(f"   - Recommendations: {', '.join(result.recommendations[:3])}\n")
            f.write("\n")

def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python focused_quality_analyzer.py <path_to_python_directory>")
        sys.exit(1)

    base_path = sys.argv[1]

    if not os.path.exists(base_path):
        print(f"Error: Path {base_path} does not exist")
        sys.exit(1)

    # Create analyzer
    analyzer = FocusedQualityAnalyzer(base_path)

    # Analyze codebase
    metrics = analyzer.analyze_codebase()

    # Print summary
    print("\n" + "="*60)
    print("FOCUSED CODEBASE ANALYSIS SUMMARY")
    print("="*60)
    print(f"Total Files: {metrics.total_files:, }")
    print(f"Total Lines: {metrics.total_lines:, }")
    print(f"Total Functions: {metrics.total_functions:, }")
    print(f"Total Classes: {metrics.total_classes:, }")
    print(f"Average Quality Score: {metrics.average_quality:.1f}/100")
    print(f"Files with Docstrings: {metrics.files_with_docstrings:, } ({metrics.files_with_docstrings/metrics.total_files*100:.1f}%)")
    print(f"Files with Type Hints: {metrics.files_with_type_hints:, } ({metrics.files_with_type_hints/metrics.total_files*100:.1f}%)")
    print(f"Files with Error Handling: {metrics.files_with_error_handling:, } ({metrics.files_with_error_handling/metrics.total_files*100:.1f}%)")
    print(f"Files with Logging: {metrics.files_with_logging:, } ({metrics.files_with_logging/metrics.total_files*100:.1f}%)")

    print("\nTop Issues:")
    for issue, count in metrics.common_issues[:5]:
        print(f"  - {issue}: {count:, } files")

    print("\nImprovement Priorities:")
    for i, priority in enumerate(metrics.improvement_priorities[:5], 1):
        print(f"  {i}. {priority}")

    # Generate reports
    analyzer.generate_report()

    print(f"\nDetailed reports generated in: focused_analysis_output/")

if __name__ == "__main__":
    main()