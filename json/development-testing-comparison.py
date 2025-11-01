"""
Development Testing Comparison 1

This module provides functionality for development testing comparison 1.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_120 = 120
CONSTANT_200 = 200
CONSTANT_50000 = 50000

#!/usr/bin/env python3
"""
Content Analysis Comparison Tool
===============================
Compare original analysis vs content-aware intelligent analysis
on 3 random Python scripts to demonstrate improvements.
"""

import os
import sys
import json
import random
import re
import hashlib
import math
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
import ast
import subprocess


class ComparisonAnalyzer:
    def __init__(self, python_folder_path):
        """__init__ function."""

        self.python_folder = Path(python_folder_path)
        self.output_dir = self.python_folder / "comparison_analysis"
        self.output_dir.mkdir(exist_ok=True)

        # Find 3 random Python scripts
        self.target_scripts = self._find_random_scripts()

    def _find_random_scripts(self):
        """Find 3 random Python scripts for analysis"""
        logger.info("🎯 Finding 3 random Python scripts for comparison...")

        python_files = list(self.python_folder.rglob("*.py"))

        # Filter out very small files (less than CONSTANT_100 bytes) and very large files (over 50KB)
        filtered_files = [
            f
            for f in python_files
            if CONSTANT_100 < f.stat().st_size < CONSTANT_50000
            and not any(skip in str(f) for skip in ["__pycache__", ".git", "test_", "venv", "env"])
        ]

        if len(filtered_files) < 3:
            logger.info(f"⚠️  Only found {len(filtered_files)} suitable Python files")
            return filtered_files

        # Select 3 random files
        selected = random.sample(filtered_files, 3)

        logger.info(f"✅ Selected 3 random Python scripts:")
        for i, script in enumerate(selected, 1):
            logger.info(f"   {i}. {script.name} ({script.stat().st_size} bytes)")

        return selected

    def run_original_analysis(self, script_path):
        """Run the original basic analysis"""
        logger.info(f"\n📊 Running ORIGINAL analysis on {script_path.name}...")

        try:
            with open(script_path, "r", encoding="utf-8") as f:
                content = f.read()
        except (OSError, IOError, FileNotFoundError):
            return {"error": "Could not read file"}

        # Basic analysis (original approach)
        analysis = {
            "file_name": script_path.name,
            "file_size": script_path.stat().st_size,
            "line_count": len(content.splitlines()),
            "word_count": len(content.split()),
            "char_count": len(content),
            "function_count": len(re.findall(r"def\s+\w+", content)),
            "class_count": len(re.findall(r"class\s+\w+", content)),
            "import_count": len(re.findall(r"import\s+|from\s+", content)),
            "comment_lines": len([line for line in content.splitlines() if line.strip().startswith("#")]),
            "complexity_score": len(re.findall(r"def\s+|class\s+|if\s+|for\s+|while\s+|try\s+|except\s+", content)),
            "technologies": self._basic_tech_detection(content),
            "file_type": "python",
            "analysis_type": "original_basic",
        }

        return analysis

    def run_content_aware_analysis(self, script_path):
        """Run the improved content-aware analysis"""
        logger.info(f"🧠 Running CONTENT-AWARE analysis on {script_path.name}...")

        try:
            with open(script_path, "r", encoding="utf-8") as f:
                content = f.read()
        except (OSError, IOError, FileNotFoundError):
            return {"error": "Could not read file"}

        # Advanced content-aware analysis
        analysis = {
            "file_name": script_path.name,
            "file_size": script_path.stat().st_size,
            "line_count": len(content.splitlines()),
            "word_count": len(content.split()),
            "char_count": len(content),
            # Basic metrics (same as original)
            "function_count": len(re.findall(r"def\s+\w+", content)),
            "class_count": len(re.findall(r"class\s+\w+", content)),
            "import_count": len(re.findall(r"import\s+|from\s+", content)),
            "comment_lines": len([line for line in content.splitlines() if line.strip().startswith("#")]),
            # Advanced content-aware metrics
            "ast_analysis": self._analyze_ast_structure(content),
            "complexity_metrics": self._calculate_advanced_complexity(content),
            "code_quality": self._assess_code_quality(content),
            "project_context": self._detect_project_context(content),
            "technology_stack": self._advanced_tech_detection(content),
            "business_value": self._assess_business_value(content),
            "maintainability": self._assess_maintainability(content),
            "security_analysis": self._analyze_security(content),
            "performance_indicators": self._analyze_performance(content),
            "documentation_quality": self._assess_documentation(content),
            "error_handling": self._analyze_error_handling(content),
            "testing_coverage": self._analyze_testing(content),
            "dependencies": self._analyze_dependencies(content),
            "patterns_used": self._detect_design_patterns(content),
            "innovation_score": self._calculate_innovation_score(content),
            "scalability_potential": self._assess_scalability(content),
            "file_type": "python",
            "analysis_type": "content_aware_advanced",
        }

        return analysis

    def _basic_tech_detection(self, content):
        """Basic technology detection (original approach)"""
        tech_patterns = {
            "tensorflow": r"import tensorflow|from tensorflow",
            "pytorch": r"import torch|from torch",
            "pandas": r"import pandas|from pandas",
            "numpy": r"import numpy|from numpy",
            "flask": r"import flask|from flask",
            "django": r"import django|from django",
            "requests": r"import requests|from requests",
        }

        detected = {}
        for tech, pattern in tech_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                detected[tech] = 1

        return detected

    def _analyze_ast_structure(self, content):
        """Analyze AST structure for deeper understanding"""
        try:
            tree = ast.parse(content)

            functions = []
            classes = []
            imports = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(
                        {
                            "name": node.name,
                            "args": len(node.args.args),
                            "lines": node.end_lineno - node.lineno if hasattr(node, "end_lineno") else 0,
                            "is_async": isinstance(node, ast.AsyncFunctionDef),
                            "has_docstring": ast.get_docstring(node) is not None,
                        }
                    )
                elif isinstance(node, ast.ClassDef):
                    classes.append(
                        {
                            "name": node.name,
                            "methods": len([n for n in node.body if isinstance(n, ast.FunctionDef)]),
                            "has_docstring": ast.get_docstring(node) is not None,
                        }
                    )
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        imports.extend([alias.name for alias in node.names])
                    else:
                        imports.extend(
                            [f"{node.module}.{alias.name}" if node.module else alias.name for alias in node.names]
                        )

            return {
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "total_nodes": len(list(ast.walk(tree))),
                "max_depth": self._calculate_ast_depth(tree),
            }
        except (ImportError, ModuleNotFoundError):
            return {"error": "Could not parse AST"}

    def _calculate_ast_depth(self, node, depth=0):
        """Calculate maximum AST depth"""
        if not hasattr(node, "__iter__"):
            return depth

        max_depth = depth
        for child in ast.iter_child_nodes(node):
            max_depth = max(max_depth, self._calculate_ast_depth(child, depth + 1))

        return max_depth

    def _calculate_advanced_complexity(self, content):
        """Calculate advanced complexity metrics"""
        try:
            tree = ast.parse(content)

            complexity_metrics = {
                "cyclomatic_complexity": 0,
                "cognitive_complexity": 0,
                "nesting_depth": 0,
                "branch_count": 0,
                "loop_count": 0,
                "condition_count": 0,
            }

            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                    complexity_metrics["cyclomatic_complexity"] += 1
                    complexity_metrics["branch_count"] += 1

                if isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
                    complexity_metrics["loop_count"] += 1

                if isinstance(node, ast.If):
                    complexity_metrics["condition_count"] += 1

                # Calculate nesting depth
                depth = self._calculate_nesting_depth(node)
                complexity_metrics["nesting_depth"] = max(complexity_metrics["nesting_depth"], depth)

            # Calculate cognitive complexity (simplified)
            complexity_metrics["cognitive_complexity"] = (
                complexity_metrics["cyclomatic_complexity"] + complexity_metrics["nesting_depth"] * 2
            )

            return complexity_metrics
        except (IndexError, KeyError):
            return {"error": "Could not calculate complexity"}

    def _calculate_nesting_depth(self, node):
        """Calculate nesting depth of a node"""
        depth = 0
        current = node
        while hasattr(current, "parent"):
            depth += 1
            current = current.parent
        return depth

    def _assess_code_quality(self, content):
        """Assess code quality metrics"""
        lines = content.splitlines()

        # Calculate various quality metrics
        total_lines = len(lines)
        non_empty_lines = len([line for line in lines if line.strip()])
        comment_lines = len([line for line in lines if line.strip().startswith("#")])
        docstring_lines = len([line for line in lines if '"""' in line or "'''" in line])

        # Check for common quality issues
        long_lines = len([line for line in lines if len(line) > CONSTANT_120])
        trailing_whitespace = len([line for line in lines if line.rstrip() != line])

        # Calculate quality score
        quality_score = 0
        if comment_lines > 0:
            quality_score += min(20, (comment_lines / total_lines) * CONSTANT_100)
        if docstring_lines > 0:
            quality_score += min(20, (docstring_lines / total_lines) * CONSTANT_100)
        if long_lines == 0:
            quality_score += 20
        if trailing_whitespace == 0:
            quality_score += 20
        if non_empty_lines > 0:
            quality_score += min(20, (non_empty_lines / total_lines) * CONSTANT_100)

        return {
            "quality_score": min(CONSTANT_100, quality_score),
            "comment_ratio": (comment_lines / total_lines) * CONSTANT_100 if total_lines > 0 else 0,
            "docstring_ratio": (docstring_lines / total_lines) * CONSTANT_100 if total_lines > 0 else 0,
            "long_lines": long_lines,
            "trailing_whitespace": trailing_whitespace,
            "readability_score": self._calculate_readability(content),
        }

    def _calculate_readability(self, content):
        """Calculate readability score (simplified)"""
        lines = content.splitlines()
        words = content.split()
        sentences = len(re.findall(r"[.!?]+", content))

        if sentences == 0:
            return 0

        avg_words_per_sentence = len(words) / sentences
        avg_chars_per_word = len(content) / len(words) if words else 0

        # Simplified readability score
        readability = CONSTANT_100 - (avg_words_per_sentence * 2) - (avg_chars_per_word * 3)
        return max(0, min(CONSTANT_100, readability))

    def _detect_project_context(self, content):
        """Detect project context and purpose"""
        context_indicators = {
            "web_application": ["flask", "django", "fastapi", "app.route", "http"],
            "data_science": ["pandas", "numpy", "matplotlib", "seaborn", "data", "analysis"],
            "machine_learning": ["tensorflow", "pytorch", "sklearn", "model", "train", "predict"],
            "automation": ["schedule", "cron", "task", "workflow", "automate"],
            "api_development": ["requests", "json", "api", "endpoint", "rest"],
            "testing": ["pytest", "unittest", "test_", "assert", "mock"],
            "cli_tool": ["argparse", "click", "typer", "sys.argv", "command"],
            "scripting": ["os.", "sys.", "pathlib", "subprocess", "file"],
        }

        detected_contexts = []
        content_lower = content.lower()

        for context, indicators in context_indicators.items():
            score = sum(1 for indicator in indicators if indicator in content_lower)
            if score > 0:
                detected_contexts.append(
                    {"context": context, "confidence": min(CONSTANT_100, score * 20), "indicators_found": score}
                )

        return sorted(detected_contexts, key=lambda x: x["confidence"], reverse=True)

    def _advanced_tech_detection(self, content):
        """Advanced technology detection with confidence scores"""
        tech_patterns = {
            "tensorflow": {"pattern": r"import tensorflow|from tensorflow", "weight": 1.0},
            "pytorch": {"pattern": r"import torch|from torch", "weight": 1.0},
            "pandas": {"pattern": r"import pandas|from pandas", "weight": 0.8},
            "numpy": {"pattern": r"import numpy|from numpy", "weight": 0.8},
            "flask": {"pattern": r"import flask|from flask", "weight": 0.9},
            "django": {"pattern": r"import django|from django", "weight": 0.9},
            "fastapi": {"pattern": r"import fastapi|from fastapi", "weight": 0.9},
            "requests": {"pattern": r"import requests|from requests", "weight": 0.7},
            "sqlalchemy": {"pattern": r"import sqlalchemy|from sqlalchemy", "weight": 0.8},
            "pytest": {"pattern": r"import pytest|from pytest", "weight": 0.7},
            "asyncio": {"pattern": r"import asyncio|from asyncio", "weight": 0.6},
            "multiprocessing": {"pattern": r"import multiprocessing|from multiprocessing", "weight": 0.6},
        }

        detected_tech = {}
        for tech, config in tech_patterns.items():
            matches = len(re.findall(config["pattern"], content, re.IGNORECASE))
            if matches > 0:
                detected_tech[tech] = {
                    "confidence": min(CONSTANT_100, matches * config["weight"] * 20),
                    "usage_count": matches,
                    "weight": config["weight"],
                }

        return detected_tech

    def _assess_business_value(self, content):
        """Assess business value and impact potential"""
        business_indicators = {
            "automation_potential": ["automate", "schedule", "batch", "process"],
            "data_processing": ["data", "process", "analyze", "transform"],
            "api_integration": ["api", "request", "response", "endpoint"],
            "user_interface": ["gui", "tkinter", "streamlit", "dash"],
            "database_operations": ["sql", "database", "query", "insert", "update"],
            "file_operations": ["file", "read", "write", "process"],
            "error_handling": ["try", "except", "error", "exception"],
            "logging": ["log", "logging", "debug", "info"],
        }

        scores = {}
        content_lower = content.lower()

        for indicator, keywords in business_indicators.items():
            score = sum(1 for keyword in keywords if keyword in content_lower)
            scores[indicator] = min(CONSTANT_100, score * 15)

        # Calculate overall business value
        overall_value = sum(scores.values()) / len(scores) if scores else 0

        return {
            "overall_business_value": overall_value,
            "indicators": scores,
            "potential_impact": "high" if overall_value > 60 else "medium" if overall_value > 30 else "low",
        }

    def _assess_maintainability(self, content):
        """Assess code maintainability"""
        maintainability_factors = {
            "documentation": len(re.findall(r'""".*?"""', content, re.DOTALL))
            + len(re.findall(r"'''.*?'''", content, re.DOTALL)),
            "type_hints": len(re.findall(r":\s*\w+", content)),
            "error_handling": len(re.findall(r"try:|except|finally:", content)),
            "logging": len(re.findall(r"logging\.|logger\.", content)),
            "constants": len(re.findall(r"[A-Z_][A-Z0-9_]*\s*=", content)),
            "functions": len(re.findall(r"def\s+\w+", content)),
            "classes": len(re.findall(r"class\s+\w+", content)),
        }

        # Calculate maintainability score
        score = 0
        if maintainability_factors["documentation"] > 0:
            score += 20
        if maintainability_factors["type_hints"] > 0:
            score += 15
        if maintainability_factors["error_handling"] > 0:
            score += 15
        if maintainability_factors["logging"] > 0:
            score += 10
        if maintainability_factors["functions"] > 0:
            score += 10
        if maintainability_factors["classes"] > 0:
            score += 10
        if maintainability_factors["constants"] > 0:
            score += 10

        return {
            "maintainability_score": min(CONSTANT_100, score),
            "factors": maintainability_factors,
            "recommendations": self._generate_maintainability_recommendations(maintainability_factors),
        }

    def _generate_maintainability_recommendations(self, factors):
        """Generate maintainability recommendations"""
        recommendations = []

        if factors["documentation"] == 0:
            recommendations.append("Add docstrings to functions and classes")
        if factors["type_hints"] == 0:
            recommendations.append("Add type hints for better code clarity")
        if factors["error_handling"] == 0:
            recommendations.append("Implement proper error handling")
        if factors["logging"] == 0:
            recommendations.append("Add logging for debugging and monitoring")
        if factors["constants"] == 0:
            recommendations.append("Extract magic numbers to named constants")

        return recommendations

    def _analyze_security(self, content):
        """Analyze security aspects"""
        security_issues = {
            "hardcoded_secrets": len(
                re.findall(r'password\s*=\s*["\'][^"\']+["\']|api_key\s*=\s*["\'][^"\']+["\']', content, re.IGNORECASE)
            ),
            "sql_injection": len(re.findall(r'execute\s*\(\s*["\'].*%.*["\']', content)),
            "eval_usage": len(re.findall(r"\beval\s*\(", content)),
            "exec_usage": len(re.findall(r"\bexec\s*\(", content)),
            "subprocess_shell": len(re.findall(r"subprocess\.run.*shell\s*=\s*True", content)),
            "file_operations": len(re.findall(r"open\s*\([^)]*\)", content)),
        }

        security_score = CONSTANT_100
        for issue, count in security_issues.items():
            if count > 0:
                security_score -= count * 10

        return {
            "security_score": max(0, security_score),
            "issues": security_issues,
            "risk_level": "high" if security_score < 50 else "medium" if security_score < 80 else "low",
        }

    def _analyze_performance(self, content):
        """Analyze performance indicators"""
        performance_indicators = {
            "async_usage": len(re.findall(r"async\s+def|await\s+", content)),
            "list_comprehensions": len(re.findall(r"\[.*for.*in.*\]", content)),
            "generator_usage": len(re.findall(r"yield\s+", content)),
            "caching": len(re.findall(r"@lru_cache|@cache|memoize", content)),
            "vectorized_operations": len(re.findall(r"\.apply\(|\.map\(|\.vectorize\(", content)),
            "multiprocessing": len(re.findall(r"multiprocessing|concurrent\.futures", content)),
        }

        performance_score = sum(performance_indicators.values()) * 5

        return {
            "performance_score": min(CONSTANT_100, performance_score),
            "indicators": performance_indicators,
            "optimization_potential": (
                "high" if performance_score < 30 else "medium" if performance_score < 60 else "low"
            ),
        }

    def _assess_documentation(self, content):
        """Assess documentation quality"""
        docstring_count = len(re.findall(r'""".*?"""', content, re.DOTALL)) + len(
            re.findall(r"'''.*?'''", content, re.DOTALL)
        )
        comment_lines = len([line for line in content.splitlines() if line.strip().startswith("#")])
        total_lines = len(content.splitlines())

        doc_ratio = (comment_lines + docstring_count) / total_lines if total_lines > 0 else 0

        return {
            "documentation_score": min(CONSTANT_100, doc_ratio * CONSTANT_200),
            "docstring_count": docstring_count,
            "comment_lines": comment_lines,
            "documentation_ratio": doc_ratio,
        }

    def _analyze_error_handling(self, content):
        """Analyze error handling patterns"""
        error_patterns = {
            "try_except": len(re.findall(r"try\s*:", content)),
            "specific_exceptions": len(re.findall(r"except\s+\w+", content)),
            "finally_blocks": len(re.findall(r"finally\s*:", content)),
            "raise_statements": len(re.findall(r"raise\s+", content)),
            "logging_errors": len(re.findall(r"logging\.error|logger\.error", content)),
        }

        error_score = sum(error_patterns.values()) * 10

        return {
            "error_handling_score": min(CONSTANT_100, error_score),
            "patterns": error_patterns,
            "coverage": "comprehensive" if error_score > 50 else "basic" if error_score > 20 else "minimal",
        }

    def _analyze_testing(self, content):
        """Analyze testing coverage and patterns"""
        test_patterns = {
            "test_functions": len(re.findall(r"def\s+test_", content)),
            "assertions": len(re.findall(r"assert\s+", content)),
            "mock_usage": len(re.findall(r"@mock|Mock\(|patch\(", content)),
            "fixtures": len(re.findall(r"@pytest\.fixture|@fixture", content)),
            "parametrize": len(re.findall(r"@pytest\.mark\.parametrize|@parametrize", content)),
        }

        test_score = sum(test_patterns.values()) * 15

        return {
            "testing_score": min(CONSTANT_100, test_score),
            "patterns": test_patterns,
            "coverage": "comprehensive" if test_score > 60 else "basic" if test_score > 30 else "minimal",
        }

    def _analyze_dependencies(self, content):
        """Analyze dependencies and imports"""
        imports = re.findall(r"(?:from\s+(\w+)\s+import|import\s+(\w+))", content)
        dependencies = [imp[0] or imp[1] for imp in imports]

        # Categorize dependencies
        categories = {"standard_library": [], "third_party": [], "local": []}

        stdlib_modules = {
            "os",
            "sys",
            "json",
            "csv",
            "datetime",
            "pathlib",
            "collections",
            "itertools",
            "functools",
            "operator",
            "re",
            "math",
            "statistics",
            "random",
            "hashlib",
            "base64",
            "urllib",
            "http",
            "socket",
            "threading",
            "multiprocessing",
            "asyncio",
            "concurrent",
        }

        for dep in dependencies:
            if dep in stdlib_modules:
                categories["standard_library"].append(dep)
            elif "." in dep or dep.startswith("_"):
                categories["local"].append(dep)
            else:
                categories["third_party"].append(dep)

        return {
            "total_dependencies": len(dependencies),
            "categories": categories,
            "dependency_complexity": len(categories["third_party"]) * 2 + len(categories["local"]),
        }

    def _detect_design_patterns(self, content):
        """Detect common design patterns"""
        patterns = {
            "singleton": len(re.findall(r"__new__\s*\(", content)),
            "factory": len(re.findall(r"def\s+create_|def\s+make_", content)),
            "observer": len(re.findall(r"notify|subscribe|unsubscribe", content)),
            "decorator": len(re.findall(r"@\w+", content)),
            "context_manager": len(re.findall(r"__enter__|__exit__|with\s+", content)),
            "iterator": len(re.findall(r"__iter__|__next__|yield", content)),
        }

        detected_patterns = [pattern for pattern, count in patterns.items() if count > 0]

        return {"detected_patterns": detected_patterns, "pattern_count": len(detected_patterns), "patterns": patterns}

    def _calculate_innovation_score(self, content):
        """Calculate innovation and creativity score"""
        innovation_indicators = {
            "advanced_features": len(re.findall(r"async|await|yield|generator", content)),
            "ai_ml_usage": len(re.findall(r"tensorflow|pytorch|sklearn|neural|model", content)),
            "data_processing": len(re.findall(r"pandas|numpy|matplotlib|seaborn", content)),
            "web_technologies": len(re.findall(r"flask|django|fastapi|streamlit", content)),
            "cloud_integration": len(re.findall(r"aws|azure|gcp|docker|kubernetes", content)),
            "testing_advanced": len(re.findall(r"pytest|mock|fixture|parametrize", content)),
        }

        innovation_score = sum(innovation_indicators.values()) * 5

        return {
            "innovation_score": min(CONSTANT_100, innovation_score),
            "indicators": innovation_indicators,
            "level": "high" if innovation_score > 60 else "medium" if innovation_score > 30 else "low",
        }

    def _assess_scalability(self, content):
        """Assess scalability potential"""
        scalability_indicators = {
            "async_processing": len(re.findall(r"async|await", content)),
            "concurrent_processing": len(re.findall(r"threading|multiprocessing|concurrent", content)),
            "database_operations": len(re.findall(r"sql|database|query", content)),
            "caching": len(re.findall(r"cache|memoize|lru_cache", content)),
            "configuration": len(re.findall(r"config|settings|environment", content)),
            "logging": len(re.findall(r"logging|logger", content)),
        }

        scalability_score = sum(scalability_indicators.values()) * 8

        return {
            "scalability_score": min(CONSTANT_100, scalability_score),
            "indicators": scalability_indicators,
            "potential": "high" if scalability_score > 50 else "medium" if scalability_score > 25 else "low",
        }

    def run_comparison(self):
        """Run the complete comparison analysis"""
        logger.info("🚀 Starting Content Analysis Comparison...")
        logger.info("=" * 60)

        results = {
            "timestamp": datetime.now().isoformat(),
            "scripts_analyzed": [],
            "comparison_summary": {},
            "improvements_demonstrated": [],
        }

        for i, script_path in enumerate(self.target_scripts, 1):
            logger.info(f"\n📁 Analyzing Script {i}/3: {script_path.name}")
            logger.info("-" * 50)

            # Run both analyses
            original_analysis = self.run_original_analysis(script_path)
            content_aware_analysis = self.run_content_aware_analysis(script_path)

            # Store results
            script_results = {
                "script_name": script_path.name,
                "script_path": str(script_path),
                "original_analysis": original_analysis,
                "content_aware_analysis": content_aware_analysis,
                "improvements": self._calculate_improvements(original_analysis, content_aware_analysis),
            }

            results["scripts_analyzed"].append(script_results)

            # Print comparison
            self._print_script_comparison(script_results)

        # Generate summary
        results["comparison_summary"] = self._generate_comparison_summary(results["scripts_analyzed"])
        results["improvements_demonstrated"] = self._generate_improvements_summary(results["scripts_analyzed"])

        # Save results
        self._save_results(results)

        # Print final summary
        self._print_final_summary(results)

        return results

    def _calculate_improvements(self, original, content_aware):
        """Calculate improvements between original and content-aware analysis"""
        improvements = {
            "metrics_added": len(content_aware) - len(original),
            "analysis_depth": (
                "basic" if len(original) < 15 else "advanced" if len(content_aware) > 30 else "intermediate"
            ),
            "insights_gained": [],
            "value_added": 0,
        }

        # Calculate value added
        if "error" not in original and "error" not in content_aware:
            original_metrics = len([k for k, v in original.items() if isinstance(v, (int, float))])
            content_aware_metrics = len([k for k, v in content_aware.items() if isinstance(v, (int, float))])
            improvements["value_added"] = content_aware_metrics - original_metrics

        # Identify new insights
        new_keys = set(content_aware.keys()) - set(original.keys())
        improvements["insights_gained"] = list(new_keys)

        return improvements

    def _print_script_comparison(self, script_results):
        """Print comparison for a single script"""
        logger.info(f"\n📊 COMPARISON RESULTS for {script_results['script_name']}")
        logger.info("=" * 50)

        original = script_results["original_analysis"]
        content_aware = script_results["content_aware_analysis"]

        if "error" in original or "error" in content_aware:
            logger.info("❌ Error in analysis - skipping detailed comparison")
            return

        logger.info(f"📈 ORIGINAL ANALYSIS:")
        logger.info(f"   • Basic metrics: {len(original)} fields")
        logger.info(f"   • Functions: {original.get('function_count', 0)}")
        logger.info(f"   • Classes: {original.get('class_count', 0)}")
        logger.info(f"   • Technologies: {len(original.get('technologies', {}))}")
        logger.info(f"   • Complexity: {original.get('complexity_score', 0)}")

        logger.info(f"\n🧠 CONTENT-AWARE ANALYSIS:")
        logger.info(f"   • Advanced metrics: {len(content_aware)} fields")
        logger.info(f"   • AST functions: {len(content_aware.get('ast_analysis', {}).get('functions', []))}")
        logger.info(f"   • Code quality: {content_aware.get('code_quality', {}).get('quality_score', 0)}/100")
        logger.info(
            f"   • Business value: {content_aware.get('business_value', {}).get('overall_business_value', 0):.1f}/100"
        )
        logger.info(
            f"   • Maintainability: {content_aware.get('maintainability', {}).get('maintainability_score', 0)}/100"
        )
        logger.info(f"   • Security score: {content_aware.get('security_analysis', {}).get('security_score', 0)}/100")
        logger.info(f"   • Innovation: {content_aware.get('innovation_score', {}).get('innovation_score', 0)}/100")

        improvements = script_results["improvements"]
        logger.info(f"\n✨ IMPROVEMENTS DEMONSTRATED:")
        logger.info(f"   • Additional metrics: +{improvements['metrics_added']}")
        logger.info(f"   • Analysis depth: {improvements['analysis_depth']}")
        logger.info(f"   • New insights: {len(improvements['insights_gained'])}")
        logger.info(f"   • Value added: +{improvements['value_added']} metrics")

    def _generate_comparison_summary(self, scripts_analyzed):
        """Generate overall comparison summary"""
        total_original_metrics = sum(len(script["original_analysis"]) for script in scripts_analyzed)
        total_content_aware_metrics = sum(len(script["content_aware_analysis"]) for script in scripts_analyzed)

        return {
            "total_scripts": len(scripts_analyzed),
            "original_metrics_total": total_original_metrics,
            "content_aware_metrics_total": total_content_aware_metrics,
            "metrics_improvement": total_content_aware_metrics - total_original_metrics,
            "improvement_percentage": (
                ((total_content_aware_metrics - total_original_metrics) / total_original_metrics * CONSTANT_100)
                if total_original_metrics > 0
                else 0
            ),
        }

    def _generate_improvements_summary(self, scripts_analyzed):
        """Generate improvements summary"""
        improvements = {
            "new_analysis_capabilities": [
                "AST Structure Analysis",
                "Advanced Complexity Metrics",
                "Code Quality Assessment",
                "Project Context Detection",
                "Business Value Analysis",
                "Maintainability Assessment",
                "Security Analysis",
                "Performance Indicators",
                "Documentation Quality",
                "Error Handling Analysis",
                "Testing Coverage",
                "Dependency Analysis",
                "Design Pattern Detection",
                "Innovation Scoring",
                "Scalability Assessment",
            ],
            "intelligence_enhancements": [
                "Semantic Understanding",
                "Context-Aware Analysis",
                "Multi-dimensional Scoring",
                "Predictive Insights",
                "Recommendation Engine",
                "Risk Assessment",
                "Value Quantification",
            ],
            "practical_benefits": [
                "Better Code Understanding",
                "Improved Decision Making",
                "Enhanced Project Planning",
                "Risk Mitigation",
                "Quality Assurance",
                "Performance Optimization",
                "Security Hardening",
            ],
        }

        return improvements

    def _save_results(self, results):
        """Save comparison results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save JSON results
        json_file = self.output_dir / f"comparison_analysis_{timestamp}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, default=str)

        # Save CSV summary
        csv_file = self.output_dir / f"comparison_summary_{timestamp}.csv"
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            import csv

            writer = csv.writer(f)
            writer.writerow(["Script", "Original Metrics", "Content-Aware Metrics", "Improvement", "New Insights"])

            for script in results["scripts_analyzed"]:
                original_count = len(script["original_analysis"])
                content_aware_count = len(script["content_aware_analysis"])
                improvement = content_aware_count - original_count
                new_insights = len(script["improvements"]["insights_gained"])

                writer.writerow([script["script_name"], original_count, content_aware_count, improvement, new_insights])

        logger.info(f"\n💾 Results saved:")
        logger.info(f"   📄 JSON: {json_file}")
        logger.info(f"   📊 CSV: {csv_file}")

    def _print_final_summary(self, results):
        """Print final summary"""
        logger.info(Path("\n") + "=" * 60)
        logger.info("🎉 CONTENT ANALYSIS COMPARISON COMPLETE!")
        logger.info("=" * 60)

        summary = results["comparison_summary"]
        improvements = results["improvements_demonstrated"]

        logger.info(f"\n📊 OVERALL RESULTS:")
        logger.info(f"   • Scripts analyzed: {summary['total_scripts']}")
        logger.info(f"   • Original metrics: {summary['original_metrics_total']}")
        logger.info(f"   • Content-aware metrics: {summary['content_aware_metrics_total']}")
        logger.info(f"   • Total improvement: +{summary['metrics_improvement']} metrics")
        logger.info(f"   • Improvement percentage: {summary['improvement_percentage']:.1f}%")

        logger.info(f"\n🧠 NEW ANALYSIS CAPABILITIES:")
        for capability in improvements["new_analysis_capabilities"][:8]:
            logger.info(f"   ✅ {capability}")
        logger.info(f"   ... and {len(improvements['new_analysis_capabilities']) - 8} more")

        logger.info(f"\n✨ INTELLIGENCE ENHANCEMENTS:")
        for enhancement in improvements["intelligence_enhancements"]:
            logger.info(f"   🚀 {enhancement}")

        logger.info(f"\n💡 PRACTICAL BENEFITS:")
        for benefit in improvements["practical_benefits"]:
            logger.info(f"   📈 {benefit}")

        logger.info(f"\n🎯 CONCLUSION:")
        logger.info(f"   The content-aware analysis provides {summary['improvement_percentage']:.1f}% more")
        logger.info(f"   comprehensive insights compared to basic analysis, enabling")
        logger.info(f"   better decision-making and code understanding.")


def main():
    """Main function to run the comparison analysis"""
    python_folder = Path.home() / "Documents" / "python"

    if not python_folder.exists():
        logger.info(f"❌ Python folder not found: {python_folder}")
        return

    logger.info("🔬 Content Analysis Comparison Tool")
    logger.info("=" * 50)
    logger.info("Comparing Original vs Content-Aware Analysis")
    logger.info(f"📁 Analyzing folder: {python_folder}")

    # Create comparison analyzer
    analyzer = ComparisonAnalyzer(python_folder)

    # Run comparison
    results = analyzer.run_comparison()

    logger.info(f"\n✅ Comparison analysis complete!")
    logger.info(f"📊 Check the 'comparison_analysis' folder for detailed results")


if __name__ == "__main__":
    main()
