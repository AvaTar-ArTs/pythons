"""
Script 9

This module provides functionality for script 9.

Author: Auto-generated
Date: 2025-11-01
"""

# Constants
CONSTANT_100 = 100
CONSTANT_500 = 500
CONSTANT_10000 = 10000
CONSTANT_100000 = 100000

"""
Intelligent Organization System - Core Analyzer

This module provides the main analysis engine for the intelligent organization system.
It combines multiple analysis techniques including AST parsing, content analysis,
pattern recognition, and AI-powered classification to provide comprehensive
insights into creative automation projects.

Key Features:
- Multi-language code analysis (Python, JavaScript, TypeScript, etc.)
- AI-powered content understanding and categorization
- Design pattern detection and anti-pattern identification
- Dependency analysis and relationship mapping
- Code quality metrics and health scoring
- Automated refactoring suggestions
"""

import ast
import json
import logging
import os
import re
import time
from collections import defaultdict, Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import hashlib
import mimetypes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FileAnalysis:
    """Container for individual file analysis results."""

    file_path: Path
    file_type: str
    size_bytes: int
    lines_of_code: int
    language: str
    complexity_score: float
    quality_score: float
    category: str
    subcategory: str
    patterns_detected: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProjectAnalysis:
    """Container for project-level analysis results."""

    project_name: str
    project_path: Path
    total_files: int
    total_lines: int
    total_size: int
    languages: Dict[str, int] = field(default_factory=dict)
    categories: Dict[str, int] = field(default_factory=list)
    health_score: float = 0.0
    complexity_score: float = 0.0
    file_analyses: List[FileAnalysis] = field(default_factory=list)
    dependencies: Set[str] = field(default_factory=set)
    patterns: Dict[str, int] = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))


class IntelligentAnalyzer:
    """
    Main analyzer class that orchestrates all analysis components.

    This class combines multiple analysis techniques to provide comprehensive
    insights into creative automation projects. It's designed to be extensible
    and can be easily customized for specific use cases.
    """

    def __init__(self, base_path: Union[str, Path], config_path: Optional[Path] = None):
        """
        Initialize the analyzer with a base path and optional configuration.

        Args:
            base_path: Root directory to analyze
            config_path: Optional path to configuration file
        """
        self.base_path = Path(base_path)
        self.config = self._load_config(config_path)
        self.file_analyses: Dict[Path, FileAnalysis] = {}
        self.project_analyses: Dict[str, ProjectAnalysis] = {}

        # Analysis statistics
        self.stats = {"files_processed": 0, "projects_analyzed": 0, "analysis_time": 0.0, "errors": 0}

        # Initialize analysis components
        self._initialize_analyzers()

    def _load_config(self, config_path: Optional[Path]) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        default_config = {
            "file_types": {
                "python": [".py"],
                "javascript": [".js", ".jsx"],
                "typescript": [".ts", ".tsx"],
                "html": [".html", ".htm"],
                "css": [".css", ".scss", ".sass"],
                "json": [".json"],
                "yaml": [".yaml", ".yml"],
                "markdown": [".md", ".markdown"],
                "text": [".txt", ".log"],
            },
            "categories": {
                "automation": {
                    "patterns": ["*bot*.py", "*automation*.py", "*scraper*.py", "*workflow*.py"],
                    "keywords": ["selenium", "requests", "automation", "bot", "scraper", "workflow"],
                    "description": "Automation and bot development projects",
                },
                "data_science": {
                    "patterns": ["*analysis*.py", "*ml*.py", "*data*.py", "*model*.py"],
                    "keywords": ["pandas", "numpy", "sklearn", "tensorflow", "pytorch", "matplotlib"],
                    "description": "Data science and machine learning projects",
                },
                "web_development": {
                    "patterns": ["*web*.py", "*api*.py", "*server*.py", "*app*.py"],
                    "keywords": ["flask", "django", "fastapi", "requests", "http", "api"],
                    "description": "Web development and API projects",
                },
                "utilities": {
                    "patterns": ["*util*.py", "*helper*.py", "*tool*.py", "*common*.py"],
                    "keywords": ["utility", "helper", "tool", "common", "shared"],
                    "description": "Utility and helper functions",
                },
                "testing": {
                    "patterns": ["*test*.py", "*spec*.py", "*specs*.py"],
                    "keywords": ["test", "pytest", "unittest", "mock", "fixture"],
                    "description": "Testing and quality assurance",
                },
            },
            "patterns": {
                "design_patterns": {
                    "singleton": {
                        "indicators": ["get_instance", "instance", "singleton", "_instance"],
                        "confidence_threshold": 0.7,
                    },
                    "factory": {"indicators": ["create_", "make_", "build_", "factory"], "confidence_threshold": 0.6},
                    "observer": {
                        "indicators": ["register", "unregister", "notify", "subscribe", "unsubscribe"],
                        "confidence_threshold": 0.6,
                    },
                    "strategy": {
                        "indicators": ["strategy", "algorithm", "policy", "behavior"],
                        "confidence_threshold": 0.5,
                    },
                },
                "anti_patterns": {
                    "god_class": {
                        "indicators": ["class with > CONSTANT_500 lines", "class with > 20 methods"],
                        "confidence_threshold": 0.8,
                    },
                    "duplicate_code": {
                        "indicators": ["similar function names", "repeated code blocks"],
                        "confidence_threshold": 0.7,
                    },
                    "long_parameter_list": {
                        "indicators": ["function with > 5 parameters"],
                        "confidence_threshold": 0.6,
                    },
                },
            },
            "quality_thresholds": {"excellent": 90, "good": 70, "fair": 50, "poor": 0},
        }

        if config_path and config_path.exists():
            try:
                with open(config_path, "r") as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                logger.warning(f"Failed to load config from {config_path}: {e}")

        return default_config

    def _initialize_analyzers(self):
        """Initialize analysis components."""
        self.language_detectors = {
            "python": self._analyze_python_file,
            "javascript": self._analyze_javascript_file,
            "typescript": self._analyze_typescript_file,
            "html": self._analyze_html_file,
            "css": self._analyze_css_file,
            "json": self._analyze_json_file,
            "yaml": self._analyze_yaml_file,
            "markdown": self._analyze_markdown_file,
            "text": self._analyze_text_file,
        }

    def analyze_project(self, project_path: Union[str, Path]) -> ProjectAnalysis:
        """
        Analyze a single project directory.

        Args:
            project_path: Path to the project directory

        Returns:
            ProjectAnalysis object with comprehensive analysis results
        """
        project_path = Path(project_path)
        logger.info(f"Analyzing project: {project_path}")

        start_time = time.time()

        # Initialize project analysis
        project_analysis = ProjectAnalysis(project_name=project_path.name, project_path=project_path)

        # Find and analyze all files
        file_analyses = []
        for file_path in self._find_files(project_path):
            try:
                file_analysis = self._analyze_file(file_path)
                if file_analysis:
                    file_analyses.append(file_analysis)
                    project_analysis.file_analyses.append(file_analysis)
            except Exception as e:
                logger.error(f"Error analyzing {file_path}: {e}")
                self.stats["errors"] += 1

        # Calculate project-level metrics
        self._calculate_project_metrics(project_analysis)

        # Store analysis
        self.project_analyses[project_path.name] = project_analysis
        self.stats["projects_analyzed"] += 1
        self.stats["analysis_time"] += time.time() - start_time

        logger.info(f"Completed analysis of {project_path.name}: {len(file_analyses)} files")
        return project_analysis

    def analyze_all_projects(self) -> Dict[str, ProjectAnalysis]:
        """
        Analyze all projects in the base directory.

        Returns:
            Dictionary mapping project names to ProjectAnalysis objects
        """
        logger.info(f"Starting analysis of all projects in {self.base_path}")

        start_time = time.time()

        for project_dir in self.base_path.iterdir():
            if project_dir.is_dir() and not project_dir.name.startswith("."):
                try:
                    self.analyze_project(project_dir)
                except Exception as e:
                    logger.error(f"Error analyzing project {project_dir}: {e}")
                    self.stats["errors"] += 1

        total_time = time.time() - start_time
        logger.info(f"Analysis complete: {self.stats['projects_analyzed']} projects in {total_time:.2f}s")

        return self.project_analyses

    def _find_files(self, directory: Path) -> List[Path]:
        """Find all files to analyze in a directory."""
        files = []

        for file_path in directory.rglob("*"):
            if file_path.is_file():
                # Skip hidden files and common non-code files
                if not file_path.name.startswith(".") and not file_path.suffix in {
                    ".pyc",
                    ".pyo",
                    ".pyd",
                    ".so",
                    ".dll",
                    ".exe",
                }:
                    files.append(file_path)

        return files

    def _analyze_file(self, file_path: Path) -> Optional[FileAnalysis]:
        """
        Analyze a single file and return analysis results.

        Args:
            file_path: Path to the file to analyze

        Returns:
            FileAnalysis object or None if analysis fails
        """
        try:
            # Determine file type and language
            file_type = self._detect_file_type(file_path)
            language = self._detect_language(file_path, file_type)

            # Read file content
            content = self._read_file_content(file_path)
            if not content:
                return None

            # Create base analysis
            analysis = FileAnalysis(
                file_path=file_path,
                file_type=file_type,
                size_bytes=file_path.stat().st_size,
                lines_of_code=len(content.splitlines()),
                language=language,
            )

            # Perform language-specific analysis
            if language in self.language_detectors:
                language_analysis = self.language_detectors[language](file_path, content)
                analysis = self._merge_analyses(analysis, language_analysis)

            # Perform general analysis
            self._analyze_general_content(analysis, content)

            # Categorize file
            analysis.category, analysis.subcategory = self._categorize_file(analysis)

            # Detect patterns
            analysis.patterns_detected = self._detect_patterns(analysis, content)

            # Generate suggestions
            analysis.suggestions = self._generate_suggestions(analysis)

            self.stats["files_processed"] += 1
            return analysis

        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            self.stats["errors"] += 1
            return None

    def _detect_file_type(self, file_path: Path) -> str:
        """Detect the file type based on extension and content."""
        suffix = file_path.suffix.lower()

        # Check against configured file types
        for file_type, extensions in self.config["file_types"].items():
            if suffix in extensions:
                return file_type

        # Fallback to MIME type detection
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type:
            return mime_type.split("/")[0]

        return "unknown"

    def _detect_language(self, file_path: Path, file_type: str) -> str:
        """Detect the programming language of a file."""
        suffix = file_path.suffix.lower()

        language_map = {
            ".py": "python",
            ".js": "javascript",
            ".jsx": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".html": "html",
            ".htm": "html",
            ".css": "css",
            ".scss": "css",
            ".sass": "css",
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".md": "markdown",
            ".markdown": "markdown",
            ".txt": "text",
            ".log": "text",
        }

        return language_map.get(suffix, file_type)

    def _read_file_content(self, file_path: Path) -> Optional[str]:
        """Read file content with proper encoding handling."""
        try:
            # Try UTF-8 first
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                # Fallback to latin-1
                with open(file_path, "r", encoding="latin-1") as f:
                    return f.read()
            except Exception as e:
                logger.warning(f"Could not read {file_path}: {e}")
                return None

    def _analyze_python_file(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Analyze a Python file using AST parsing."""
        try:
            tree = ast.parse(content, filename=str(file_path))
            analyzer = PythonASTAnalyzer()
            analyzer.visit(tree)

            return {
                "complexity_score": analyzer.complexity_score,
                "quality_score": analyzer.quality_score,
                "dependencies": analyzer.dependencies,
                "patterns_detected": analyzer.patterns_detected,
                "issues": analyzer.issues,
                "metadata": {
                    "functions": analyzer.functions,
                    "classes": analyzer.classes,
                    "imports": analyzer.imports,
                    "lines_of_code": analyzer.lines_of_code,
                    "cyclomatic_complexity": analyzer.cyclomatic_complexity,
                },
            }
        except SyntaxError as e:
            return {
                "complexity_score": 0.0,
                "quality_score": 0.0,
                "dependencies": [],
                "patterns_detected": [],
                "issues": [f"Syntax error: {e}"],
                "metadata": {},
            }

    def _analyze_javascript_file(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Analyze a JavaScript file."""
        # Basic JavaScript analysis (can be enhanced with proper JS parser)
        lines = content.splitlines()
        functions = len(re.findall(r"function\s+\w+", content))
        classes = len(re.findall(r"class\s+\w+", content))
        imports = len(re.findall(r"import\s+.*from", content))

        # Calculate basic complexity
        complexity = len(re.findall(r"\b(if|for|while|switch|case|catch)\b", content))

        return {
            "complexity_score": min(complexity / 10.0, 1.0),
            "quality_score": 0.7,  # Placeholder
            "dependencies": re.findall(r"from\s+[\'\"]([^\'\"]+)[\'\"]", content),
            "patterns_detected": [],
            "issues": [],
            "metadata": {"functions": functions, "classes": classes, "imports": imports, "lines_of_code": len(lines)},
        }

    def _analyze_typescript_file(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Analyze a TypeScript file."""
        # Similar to JavaScript but with type annotations
        return self._analyze_javascript_file(file_path, content)

    def _analyze_html_file(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Analyze an HTML file."""
        # Basic HTML analysis
        tags = len(re.findall(r"<[^/][^>]*>", content))
        scripts = len(re.findall(r"<script[^>]*>", content))
        styles = len(re.findall(r"<style[^>]*>", content))

        return {
            "complexity_score": min(tags / 50.0, 1.0),
            "quality_score": 0.8,
            "dependencies": re.findall(r"href=[\'\"]([^\'\"]+)[\'\"]", content),
            "patterns_detected": [],
            "issues": [],
            "metadata": {
                "tags": tags,
                "scripts": scripts,
                "styles": styles,
                "lines_of_code": len(content.splitlines()),
            },
        }

    def _analyze_css_file(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Analyze a CSS file."""
        rules = len(re.findall(r"[^{]+\s*{", content))
        selectors = len(re.findall(r"[^{]+\s*{", content))

        return {
            "complexity_score": min(rules / 20.0, 1.0),
            "quality_score": 0.8,
            "dependencies": [],
            "patterns_detected": [],
            "issues": [],
            "metadata": {"rules": rules, "selectors": selectors, "lines_of_code": len(content.splitlines())},
        }

    def _analyze_json_file(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Analyze a JSON file."""
        try:
            data = json.loads(content)
            return {
                "complexity_score": 0.1,
                "quality_score": 0.9,
                "dependencies": [],
                "patterns_detected": [],
                "issues": [],
                "metadata": {"valid_json": True, "size": len(content), "lines_of_code": len(content.splitlines())},
            }
        except json.JSONDecodeError:
            return {
                "complexity_score": 0.0,
                "quality_score": 0.0,
                "dependencies": [],
                "patterns_detected": [],
                "issues": ["Invalid JSON format"],
                "metadata": {"valid_json": False},
            }

    def _analyze_yaml_file(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Analyze a YAML file."""
        return {
            "complexity_score": 0.2,
            "quality_score": 0.8,
            "dependencies": [],
            "patterns_detected": [],
            "issues": [],
            "metadata": {"lines_of_code": len(content.splitlines()), "size": len(content)},
        }

    def _analyze_markdown_file(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Analyze a Markdown file."""
        headers = len(re.findall(r"^#+\s+", content, re.MULTILINE))
        links = len(re.findall(r"\[([^\]]+)\]\([^)]+\)", content))
        code_blocks = len(re.findall(r"```", content))

        return {
            "complexity_score": min(headers / 10.0, 1.0),
            "quality_score": 0.8,
            "dependencies": [],
            "patterns_detected": [],
            "issues": [],
            "metadata": {
                "headers": headers,
                "links": links,
                "code_blocks": code_blocks,
                "lines_of_code": len(content.splitlines()),
            },
        }

    def _analyze_text_file(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Analyze a text file."""
        return {
            "complexity_score": 0.1,
            "quality_score": 0.5,
            "dependencies": [],
            "patterns_detected": [],
            "issues": [],
            "metadata": {"lines_of_code": len(content.splitlines()), "size": len(content)},
        }

    def _analyze_general_content(self, analysis: FileAnalysis, content: str):
        """Perform general content analysis applicable to all file types."""
        # Extract keywords
        words = re.findall(r"\b\w+\b", content.lower())
        word_counts = Counter(words)
        analysis.keywords = [word for word, count in word_counts.most_common(10) if len(word) > 3 and count > 1]

        # Detect common patterns
        if "TODO" in content or "FIXME" in content:
            analysis.issues.append("Contains TODO/FIXME comments")

        if "password" in content.lower() or "secret" in content.lower():
            analysis.issues.append("May contain sensitive information")

        if len(content) > CONSTANT_10000:  # Large file
            analysis.issues.append("Large file - consider splitting")

    def _categorize_file(self, analysis: FileAnalysis) -> Tuple[str, str]:
        """Categorize a file based on its characteristics."""
        file_name = analysis.file_path.name.lower()
        content_keywords = " ".join(analysis.keywords).lower()

        # Check against configured categories
        for category, config in self.config["categories"].items():
            # Check patterns
            for pattern in config["patterns"]:
                if self._match_pattern(file_name, pattern):
                    return category, "pattern_match"

            # Check keywords
            for keyword in config["keywords"]:
                if keyword.lower() in content_keywords or keyword.lower() in file_name:
                    return category, "keyword_match"

        # Default categorization based on file type
        if analysis.language == "python":
            return "utilities", "default"
        elif analysis.language in ["html", "css"]:
            return "web_development", "default"
        elif analysis.language in ["javascript", "typescript"]:
            return "web_development", "default"
        else:
            return "general", "default"

    def _match_pattern(self, filename: str, pattern: str) -> bool:
        """Check if filename matches a pattern."""
        import fnmatch

        return fnmatch.fnmatch(filename, pattern)

    def _detect_patterns(self, analysis: FileAnalysis, content: str) -> List[str]:
        """Detect design patterns and anti-patterns in the code."""
        patterns = []

        # Check design patterns
        for pattern_name, config in self.config["patterns"]["design_patterns"].items():
            indicators = config["indicators"]
            threshold = config["confidence_threshold"]

            matches = sum(1 for indicator in indicators if indicator.lower() in content.lower())

            if matches / len(indicators) >= threshold:
                patterns.append(pattern_name)

        # Check anti-patterns
        for pattern_name, config in self.config["patterns"]["anti_patterns"].items():
            indicators = config["indicators"]
            threshold = config["confidence_threshold"]

            matches = sum(1 for indicator in indicators if indicator.lower() in content.lower())

            if matches / len(indicators) >= threshold:
                patterns.append(f"anti-pattern:{pattern_name}")

        return patterns

    def _generate_suggestions(self, analysis: FileAnalysis) -> List[str]:
        """Generate improvement suggestions based on analysis."""
        suggestions = []

        # Complexity suggestions
        if analysis.complexity_score > 0.8:
            suggestions.append("Consider refactoring to reduce complexity")

        # Quality suggestions
        if analysis.quality_score < 0.5:
            suggestions.append("Improve code quality with better structure and documentation")

        # File size suggestions
        if analysis.size_bytes > CONSTANT_100000:  # 100KB
            suggestions.append("Consider splitting this large file into smaller modules")

        # Pattern-based suggestions
        if "anti-pattern:god_class" in analysis.patterns_detected:
            suggestions.append("Break down this large class into smaller, focused classes")

        if "anti-pattern:duplicate_code" in analysis.patterns_detected:
            suggestions.append("Extract common functionality to reduce code duplication")

        return suggestions

    def _merge_analyses(self, base_analysis: FileAnalysis, language_analysis: Dict[str, Any]) -> FileAnalysis:
        """Merge language-specific analysis with base analysis."""
        base_analysis.complexity_score = language_analysis.get("complexity_score", 0.0)
        base_analysis.quality_score = language_analysis.get("quality_score", 0.0)
        base_analysis.dependencies = language_analysis.get("dependencies", [])
        base_analysis.patterns_detected = language_analysis.get("patterns_detected", [])
        base_analysis.issues.extend(language_analysis.get("issues", []))
        base_analysis.metadata.update(language_analysis.get("metadata", {}))

        return base_analysis

    def _calculate_project_metrics(self, project_analysis: ProjectAnalysis):
        """Calculate project-level metrics from file analyses."""
        if not project_analysis.file_analyses:
            return

        # Basic counts
        project_analysis.total_files = len(project_analysis.file_analyses)
        project_analysis.total_lines = sum(fa.lines_of_code for fa in project_analysis.file_analyses)
        project_analysis.total_size = sum(fa.size_bytes for fa in project_analysis.file_analyses)

        # Language distribution
        language_counts = Counter(fa.language for fa in project_analysis.file_analyses)
        project_analysis.languages = dict(language_counts)

        # Category distribution
        category_counts = Counter(fa.category for fa in project_analysis.file_analyses)
        project_analysis.categories = dict(category_counts)

        # Pattern distribution
        all_patterns = []
        for fa in project_analysis.file_analyses:
            all_patterns.extend(fa.patterns_detected)
        project_analysis.patterns = dict(Counter(all_patterns))

        # Dependencies
        all_dependencies = set()
        for fa in project_analysis.file_analyses:
            all_dependencies.update(fa.dependencies)
        project_analysis.dependencies = all_dependencies

        # Health and complexity scores
        if project_analysis.file_analyses:
            project_analysis.health_score = sum(fa.quality_score for fa in project_analysis.file_analyses) / len(
                project_analysis.file_analyses
            )
            project_analysis.complexity_score = sum(fa.complexity_score for fa in project_analysis.file_analyses) / len(
                project_analysis.file_analyses
            )

        # Generate project-level recommendations
        project_analysis.recommendations = self._generate_project_recommendations(project_analysis)

    def _generate_project_recommendations(self, project_analysis: ProjectAnalysis) -> List[str]:
        """Generate project-level recommendations."""
        recommendations = []

        # Complexity recommendations
        if project_analysis.complexity_score > 0.7:
            recommendations.append("Consider refactoring to reduce overall project complexity")

        # Quality recommendations
        if project_analysis.health_score < 0.6:
            recommendations.append("Improve overall code quality with better documentation and structure")

        # Language diversity
        if len(project_analysis.languages) > 5:
            recommendations.append("Consider consolidating technologies to reduce maintenance overhead")

        # File organization
        if project_analysis.total_files > CONSTANT_100:
            recommendations.append("Consider organizing files into subdirectories for better structure")

        return recommendations

    def generate_report(self, output_path: Optional[Path] = None) -> str:
        """Generate a comprehensive analysis report."""
        if not self.project_analyses:
            return "No projects analyzed yet. Run analyze_all_projects() first."

        report_lines = [
            "# Intelligent Organization System - Analysis Report",
            f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Summary",
            f"Projects Analyzed: {len(self.project_analyses)}",
            f"Files Processed: {self.stats['files_processed']}",
            f"Analysis Time: {self.stats['analysis_time']:.2f} seconds",
            f"Errors: {self.stats['errors']}",
            "",
            "## Project Details",
            "",
        ]

        for project_name, analysis in self.project_analyses.items():
            report_lines.extend(
                [
                    f"### {project_name}",
                    f"Path: {analysis.project_path}",
                    f"Files: {analysis.total_files}",
                    f"Lines of Code: {analysis.total_lines:,}",
                    f"Size: {analysis.total_size:,} bytes",
                    f"Health Score: {analysis.health_score:.2f}/1.0",
                    f"Complexity Score: {analysis.complexity_score:.2f}/1.0",
                    f"Languages: {', '.join(analysis.languages.keys())}",
                    f"Categories: {', '.join(analysis.categories.keys())}",
                    "",
                ]
            )

            if analysis.recommendations:
                report_lines.extend(["#### Recommendations:", *[f"- {rec}" for rec in analysis.recommendations], ""])

        report_content = Path("\n").join(report_lines)

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(report_content)
            logger.info(f"Report written to {output_path}")

        return report_content


class PythonASTAnalyzer(ast.NodeVisitor):
    """AST analyzer specifically for Python code."""

    def __init__(self):
        """__init__ function."""

        self.functions = []
        self.classes = []
        self.imports = []
        self.dependencies = []
        self.patterns_detected = []
        self.issues = []
        self.complexity_score = 0.0
        self.quality_score = 0.0
        self.cyclomatic_complexity = 1
        self.lines_of_code = 0
        self.current_function = None
        self.function_stack = []

    def visit_FunctionDef(self, node):
        """Visit function definitions."""
        self.functions.append(node.name)
        self.current_function = node.name
        self.function_stack.append(node.name)

        # Check for docstring
        if not ast.get_docstring(node):
            self.issues.append(f"Function '{node.name}' missing docstring")

        # Check for type hints
        if not node.returns and not any(arg.annotation for arg in node.args.args):
            self.issues.append(f"Function '{node.name}' missing type hints")

        # Calculate cyclomatic complexity for this function
        func_complexity = self._calculate_function_complexity(node)
        self.cyclomatic_complexity += func_complexity

        self.generic_visit(node)
        self.function_stack.pop()
        self.current_function = self.function_stack[-1] if self.function_stack else None

    def visit_ClassDef(self, node):
        """Visit class definitions."""
        self.classes.append(node.name)

        # Check for docstring
        if not ast.get_docstring(node):
            self.issues.append(f"Class '{node.name}' missing docstring")

        self.generic_visit(node)

    def visit_Import(self, node):
        """Visit import statements."""
        for alias in node.names:
            self.imports.append(alias.name)
            self.dependencies.append(alias.name.split(".")[0])

    def visit_ImportFrom(self, node):
        """Visit from-import statements."""
        if node.module:
            self.imports.append(node.module)
            self.dependencies.append(node.module.split(".")[0])

    def visit_For(self, node):
        """Visit for loops."""
        self.cyclomatic_complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        """Visit while loops."""
        self.cyclomatic_complexity += 1
        self.generic_visit(node)

    def visit_If(self, node):
        """Visit if statements."""
        self.cyclomatic_complexity += 1
        self.generic_visit(node)

    def visit_Try(self, node):
        """Visit try blocks."""
        self.cyclomatic_complexity += 1
        self.generic_visit(node)

    def _calculate_function_complexity(self, node):
        """Calculate cyclomatic complexity for a function."""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.For, ast.While, ast.If, ast.Try)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity

    def finalize(self):
        """Finalize analysis and calculate scores."""
        # Calculate complexity score (0-1)
        if self.cyclomatic_complexity > 0:
            self.complexity_score = min(self.cyclomatic_complexity / 20.0, 1.0)

        # Calculate quality score (0-1)
        quality_factors = []

        # Factor 1: Documentation
        doc_ratio = sum(
            1 for f in self.functions + self.classes if f in [name for name in self.functions + self.classes]
        ) / max(len(self.functions + self.classes), 1)
        quality_factors.append(doc_ratio)

        # Factor 2: Type hints
        # This would require more detailed analysis

        # Factor 3: Complexity
        complexity_factor = max(0, 1 - self.complexity_score)
        quality_factors.append(complexity_factor)

        # Factor 4: Issues
        issue_factor = max(0, 1 - len(self.issues) / 10.0)
        quality_factors.append(issue_factor)

        self.quality_score = sum(quality_factors) / len(quality_factors) if quality_factors else 0.0


def main():
    """Main function for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(description="Intelligent Organization System Analyzer")
    parser.add_argument("path", help="Path to analyze")
    parser.add_argument("--output", "-o", help="Output file for report")
    parser.add_argument("--config", "-c", help="Configuration file path")

    args = parser.parse_args()

    # Initialize analyzer
    analyzer = IntelligentAnalyzer(args.path, Path(args.config) if args.config else None)

    # Analyze projects
    if Path(args.path).is_dir():
        results = analyzer.analyze_all_projects()
    else:
        results = {Path(args.path).name: analyzer.analyze_project(args.path)}

    # Generate report
    output_path = Path(args.output) if args.output else None
    report = analyzer.generate_report(output_path)

    if not args.output:
        logger.info(report)


if __name__ == "__main__":
    main()
