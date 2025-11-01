"""
Adaptive Content Awareness

This module provides functionality for adaptive content awareness.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_256 = 256
CONSTANT_500 = 500
CONSTANT_512 = 512
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024
CONSTANT_5000 = 5000

#!/usr/bin/env python3
"""
Adaptive Content-Aware Analysis System
Dynamically adjusts analysis approach based on file content, context, and patterns
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import mimetypes


class ContextDetector:
    """Detects content type, language, framework, and context"""

    # Programming language patterns
    LANGUAGE_PATTERNS = {
        "python": [r"def\s+\w+\(", r"import\s+\w+", r"class\s+\w+:", r"__init__", r"\.py$"],
        "javascript": [r"function\s+\w+\(", r"const\s+\w+\s*=", r"\.js$", r"=>", r"require\("],
        "typescript": [r"interface\s+\w+", r"type\s+\w+\s*=", r"\.ts$", r"\.tsx$"],
        "shell": [r"^#!/bin/(bash|sh)", r"\.sh$", r"^\s*#", r"\$\{"],
        "yaml": [r"\.ya?ml$", r"^\s*\w+:", r"^\s*-\s+\w+"],
        "json": [r"\.json$", r"^\s*[\{\[]", r'"[\w-]+":\s*'],
        "markdown": [r"\.md$", r"^#+\s+", r"^\s*[-*]\s+", r"\[.*\]\(.*\)"],
        "html": [r"<!DOCTYPE", r"<html", r"<div", r"\.html$"],
        "css": [r"\.css$", r"\{[^}]*:[^}]*\}", r"@media"],
        "go": [r"func\s+\w+\(", r"package\s+\w+", r"\.go$"],
        "rust": [r"fn\s+\w+\(", r"let\s+mut", r"\.rs$"],
        "ruby": [r"def\s+\w+", r"\.rb$", r"require\s+"],
    }

    # Framework detection patterns
    FRAMEWORK_PATTERNS = {
        "react": [r'import.*from\s+[\'"]react', r"useState", r"useEffect", r"jsx"],
        "vue": [r"<template>", r"<script.*setup>", r"Vue\."],
        "django": [r"from django", r"models\.Model", r"urls\.py"],
        "flask": [r"from flask", r"@app\.route", r"Flask\("],
        "fastapi": [r"from fastapi", r"@app\.(get|post)", r"FastAPI\("],
        "express": [r"express\(\)", r"app\.(get|post)", r"require.*express"],
        "nextjs": [r"next/.*", r"getServerSideProps", r"getStaticProps"],
        "alfred": [r"info\.plist", r"alfred", r"workflow", r"script filter"],
        "github-action": [r"action\.yml", r"steps:", r"uses:", r"github"],
    }

    # Content purpose patterns
    PURPOSE_PATTERNS = {
        "configuration": [r"config", r"settings", r"\.json$", r"\.yaml$", r"\.toml$"],
        "documentation": [r"readme", r"\.md$", r"docs?/", r"# ", r"## "],
        "test": [r"test_", r"_test\.", r"\.test\.", r"\.spec\.", r"describe\("],
        "build": [r"build\.", r"webpack", r"rollup", r"Makefile", r"CMakeLists"],
        "deployment": [r"deploy", r"docker", r"k8s", r"terraform", r"ansible"],
        "data": [r"\.csv$", r"\.json$", r"\.xml$", r"\.sql$"],
        "script": [r"\.sh$", r"\.py$", r"#!/", r"automation"],
        "library": [r"lib/", r"package", r"module", r"export"],
        "application": [r"main\.", r"app\.", r"index\.", r"server\."],
    }

    @staticmethod
    def detect_language(content: str, filepath: str) -> Optional[str]:
        """Detect programming language with confidence score"""
        scores = Counter()

        for lang, patterns in ContextDetector.LANGUAGE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                    scores[lang] += 1
                if re.search(pattern, filepath, re.IGNORECASE):
                    scores[lang] += 2  # Filename match is stronger

        return scores.most_common(1)[0][0] if scores else None

    @staticmethod
    def detect_framework(content: str) -> List[str]:
        """Detect frameworks used"""
        frameworks = []

        for framework, patterns in ContextDetector.FRAMEWORK_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    frameworks.append(framework)
                    break

        return frameworks

    @staticmethod
    def detect_purpose(content: str, filepath: str) -> str:
        """Detect file purpose"""
        scores = Counter()

        combined = content + " " + filepath
        for purpose, patterns in ContextDetector.PURPOSE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, combined, re.IGNORECASE):
                    scores[purpose] += 1

        return scores.most_common(1)[0][0] if scores else "general"

    @staticmethod
    def analyze_complexity(content: str) -> Dict[str, Any]:
        """Analyze code complexity"""
        lines = content.split("\n")
        code_lines = [l for l in lines if l.strip() and not l.strip().startswith("#")]

        return {
            "total_lines": len(lines),
            "code_lines": len(code_lines),
            "blank_lines": len(lines) - len(code_lines),
            "functions": len(re.findall(r"(def|function|func)\s+\w+", content)),
            "classes": len(re.findall(r"class\s+\w+", content)),
            "imports": len(re.findall(r"^(import|from|require|use)", content, re.MULTILINE)),
            "comments": len(re.findall(r"(#|//|/\*)", content)),
            "todos": len(re.findall(r"TODO|FIXME|XXX|HACK", content, re.IGNORECASE)),
        }


class AdaptiveStrategy:
    """Determines appropriate analysis strategy based on content"""

    @staticmethod
    def choose_strategy(filepath: Path, content: str, context: Dict) -> str:
        """Choose analysis depth: quick, medium, or deep"""

        # Quick analysis for small, simple files
        if len(content) < CONSTANT_500:
            return "quick"

        # Deep analysis for complex code files
        if context.get("language") in ["python", "javascript", "typescript"]:
            complexity = context.get("complexity", {})
            if complexity.get("functions", 0) > 10 or complexity.get("classes", 0) > 3:
                return "deep"

        # Deep analysis for configuration files
        if context.get("purpose") == "configuration":
            return "deep"

        # Deep analysis for documentation
        if context.get("purpose") == "documentation":
            if len(content) > CONSTANT_5000:
                return "deep"

        # Medium for everything else
        return "medium"

    @staticmethod
    def select_analyzers(strategy: str, context: Dict) -> List[str]:
        """Select which analyzers to run based on strategy"""

        analyzers = ["basic"]  # Always run basic

        if strategy in ["medium", "deep"]:
            analyzers.extend(["structure", "quality"])

        if strategy == "deep":
            analyzers.extend(["security", "performance", "best_practices"])

        # Add context-specific analyzers
        if context.get("language") == "python":
            analyzers.append("python_specific")

        if context.get("purpose") == "test":
            analyzers.append("test_coverage")

        if context.get("frameworks"):
            analyzers.append("framework_patterns")

        return list(set(analyzers))


class DynamicInsights:
    """Generates context-aware insights and recommendations"""

    @staticmethod
    def generate_insights(filepath: Path, content: str, context: Dict, analysis: Dict) -> List[Dict]:
        """Generate dynamic insights based on analysis"""

        insights = []

        # Language-specific insights
        if context["language"] == "python":
            insights.extend(DynamicInsights._python_insights(content, context))
        elif context["language"] == "javascript":
            insights.extend(DynamicInsights._javascript_insights(content, context))

        # Purpose-specific insights
        if context["purpose"] == "configuration":
            insights.extend(DynamicInsights._config_insights(content, context))
        elif context["purpose"] == "documentation":
            insights.extend(DynamicInsights._docs_insights(content, context))

        # Complexity insights
        insights.extend(DynamicInsights._complexity_insights(context.get("complexity", {})))

        # Security insights
        insights.extend(DynamicInsights._security_insights(content, context))

        # Best practices
        insights.extend(DynamicInsights._best_practices(content, context))

        return insights

    @staticmethod
    def _python_insights(content: str, context: Dict) -> List[Dict]:
        """Python-specific insights"""
        insights = []

        # Check for type hints
        if not re.search(r":\s*\w+\s*(->|,|\))", content):
            insights.append(
                {
                    "type": "enhancement",
                    "priority": "medium",
                    "title": "Add Type Hints",
                    "message": "Consider adding type hints for better code documentation and IDE support",
                    "impact": "Improves code maintainability and catches type errors early",
                }
            )

        # Check for docstrings
        functions = re.findall(r"def\s+\w+\([^)]*\):", content)
        docstrings = re.findall(r'"""[^"]*"""', content)
        if len(functions) > len(docstrings) / 2:
            insights.append(
                {
                    "type": "documentation",
                    "priority": "medium",
                    "title": "Add Docstrings",
                    "message": f"{len(functions)} functions found, but only ~{len(docstrings)} docstrings",
                    "impact": "Improves code documentation and IDE help",
                }
            )

        # Check for error handling
        try_blocks = len(re.findall(r"\btry:", content))
        if try_blocks == 0 and "open(" in content:
            insights.append(
                {
                    "type": "robustness",
                    "priority": "high",
                    "title": "Add Error Handling",
                    "message": "File operations found without try/except blocks",
                    "impact": "Prevents crashes from IO errors",
                }
            )

        return insights

    @staticmethod
    def _javascript_insights(content: str, context: Dict) -> List[Dict]:
        """JavaScript-specific insights"""
        insights = []

        # Check for const/let vs var
        if "var " in content:
            insights.append(
                {
                    "type": "modernization",
                    "priority": "medium",
                    "title": "Use const/let Instead of var",
                    "message": "Found var declarations, consider using const/let",
                    "impact": "Prevents scope-related bugs",
                }
            )

        # Check for async/await vs promises
        if ".then(" in content and "async " not in content:
            insights.append(
                {
                    "type": "modernization",
                    "priority": "low",
                    "title": "Consider async/await",
                    "message": "Promise chains could be simplified with async/await",
                    "impact": "Improves code readability",
                }
            )

        return insights

    @staticmethod
    def _config_insights(content: str, context: Dict) -> List[Dict]:
        """Configuration file insights"""
        insights = []

        # Check for sensitive data
        sensitive_patterns = [
            r"password\s*[=:]",
            r"api[_-]?key\s*[=:]",
            r"secret\s*[=:]",
            r"token\s*[=:]",
        ]

        for pattern in sensitive_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                insights.append(
                    {
                        "type": "security",
                        "priority": "critical",
                        "title": "Potential Secrets in Config",
                        "message": "Found potential sensitive data in configuration file",
                        "impact": "Security risk if committed to version control",
                        "action": "Use environment variables or secrets management",
                    }
                )
                break

        return insights

    @staticmethod
    def _docs_insights(content: str, context: Dict) -> List[Dict]:
        """Documentation insights"""
        insights = []

        # Check for outdated dates
        current_year = datetime.now().year
        old_years = re.findall(r"\b(20\d{2})\b", content)
        if old_years and int(min(old_years)) < current_year - 2:
            insights.append(
                {
                    "type": "maintenance",
                    "priority": "low",
                    "title": "Documentation May Be Outdated",
                    "message": f"References dates from {min(old_years)}, may need updating",
                    "impact": "Users may follow outdated instructions",
                }
            )

        # Check for broken links (basic)
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
        if len(links) > 5:
            insights.append(
                {
                    "type": "maintenance",
                    "priority": "low",
                    "title": "Many Links Present",
                    "message": f"{len(links)} links found - consider periodic link checking",
                    "impact": "Broken links hurt user experience",
                }
            )

        return insights

    @staticmethod
    def _complexity_insights(complexity: Dict) -> List[Dict]:
        """Complexity-based insights"""
        insights = []

        # Large files
        if complexity.get("code_lines", 0) > CONSTANT_500:
            insights.append(
                {
                    "type": "refactoring",
                    "priority": "medium",
                    "title": "Large File",
                    "message": f'{complexity["code_lines"]} lines of code - consider splitting',
                    "impact": "Improves maintainability and testability",
                }
            )

        # Many functions/classes
        if complexity.get("functions", 0) > 20:
            insights.append(
                {
                    "type": "organization",
                    "priority": "medium",
                    "title": "Many Functions",
                    "message": f'{complexity["functions"]} functions - consider organizing into classes/modules',
                    "impact": "Improves code organization",
                }
            )

        # TODOs
        if complexity.get("todos", 0) > 5:
            insights.append(
                {
                    "type": "maintenance",
                    "priority": "low",
                    "title": "Many TODOs",
                    "message": f'{complexity["todos"]} TODO/FIXME comments found',
                    "impact": "Technical debt tracking",
                }
            )

        return insights

    @staticmethod
    def _security_insights(content: str, context: Dict) -> List[Dict]:
        """Security-focused insights"""
        insights = []

        # SQL injection risk
        if re.search(r'execute\([^)]*%s|format\(|f["\']', content):
            if "sql" in content.lower() or "query" in content.lower():
                insights.append(
                    {
                        "type": "security",
                        "priority": "high",
                        "title": "Potential SQL Injection Risk",
                        "message": "String formatting used with SQL queries",
                        "impact": "Critical security vulnerability",
                        "action": "Use parameterized queries",
                    }
                )

        # Hardcoded credentials
        if re.search(r'(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']', content, re.IGNORECASE):
            insights.append(
                {
                    "type": "security",
                    "priority": "critical",
                    "title": "Hardcoded Credentials",
                    "message": "Found hardcoded password in source code",
                    "impact": "Critical security risk",
                    "action": "Use environment variables or secrets management",
                }
            )

        return insights

    @staticmethod
    def _best_practices(content: str, context: Dict) -> List[Dict]:
        """General best practices"""
        insights = []

        # Magic numbers
        if context.get("language") in ["python", "javascript"]:
            magic_numbers = re.findall(
                r"\b(CONSTANT_100|CONSTANT_1000|CONSTANT_256|CONSTANT_512|CONSTANT_1024)\b", content
            )
            if len(magic_numbers) > 5:
                insights.append(
                    {
                        "type": "best_practice",
                        "priority": "low",
                        "title": "Magic Numbers",
                        "message": "Found several numeric literals - consider using named constants",
                        "impact": "Improves code readability and maintainability",
                    }
                )

        return insights


class AdaptiveAnalyzer:
    """Main adaptive analysis system"""

    def __init__(self, target_path: str):
        """__init__ function."""

        self.target = Path(target_path)
        self.results = {
            "files_analyzed": 0,
            "strategies_used": Counter(),
            "insights_generated": [],
            "contexts": {},
            "summary": {},
        }

    def analyze(self, thoroughness: str = "adaptive") -> Dict:
        """
        Analyze target with adaptive strategies
        thoroughness: 'quick', 'adaptive' (default), 'deep'
        """

        if self.target.is_file():
            result = self._analyze_file(self.target, thoroughness)
            # Generate summary for single file
            self.results["summary"] = self._generate_summary()
            return result
        elif self.target.is_dir():
            return self._analyze_directory(self.target, thoroughness)
        else:
            return {"error": "Target not found"}

    def _analyze_file(self, filepath: Path, thoroughness: str) -> Dict:
        """Analyze single file with adaptive strategy"""

        try:
            # Read content
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Detect context
            context = {
                "language": ContextDetector.detect_language(content, str(filepath)),
                "frameworks": ContextDetector.detect_framework(content),
                "purpose": ContextDetector.detect_purpose(content, str(filepath)),
                "complexity": ContextDetector.analyze_complexity(content),
                "size": len(content),
                "filepath": str(filepath),
            }

            # Choose strategy
            if thoroughness == "adaptive":
                strategy = AdaptiveStrategy.choose_strategy(filepath, content, context)
            else:
                strategy = thoroughness

            self.results["strategies_used"][strategy] += 1

            # Generate insights
            insights = DynamicInsights.generate_insights(filepath, content, context, {})

            # Store results
            self.results["files_analyzed"] += 1
            self.results["contexts"][str(filepath)] = context
            self.results["insights_generated"].extend(insights)

            return {
                "file": str(filepath),
                "context": context,
                "strategy": strategy,
                "insights": insights,
                "summary": self._summarize_insights(insights),
            }

        except Exception as e:
            return {"file": str(filepath), "error": str(e)}

    def _analyze_directory(self, dirpath: Path, thoroughness: str) -> Dict:
        """Analyze directory with adaptive strategies"""

        # Get all relevant files
        files = [f for f in dirpath.rglob("*") if f.is_file() and not self._should_skip(f)]

        logger.info(f"Analyzing {len(files)} files...")

        # Analyze each file
        file_results = []
        for i, filepath in enumerate(files[:CONSTANT_100]):  # Limit to CONSTANT_100 files
            if i % 10 == 0:
                logger.info(f"Progress: {i}/{min(len(files), CONSTANT_100)}")

            result = self._analyze_file(filepath, thoroughness)
            if "error" not in result:
                file_results.append(result)

        # Aggregate results
        self.results["file_results"] = file_results
        self.results["summary"] = self._generate_summary()

        return self.results

    def _should_skip(self, filepath: Path) -> bool:
        """Determine if file should be skipped"""

        skip_patterns = [
            r"\.git/",
            r"node_modules/",
            r"__pycache__/",
            r"\.pyc$",
            r"\.class$",
            r"\.o$",
            r"\.so$",
            r"\.dylib$",
            r"\.egg-info/",
            r"\.DS_Store$",
        ]

        for pattern in skip_patterns:
            if re.search(pattern, str(filepath)):
                return True

        return False

    def _summarize_insights(self, insights: List[Dict]) -> Dict:
        """Summarize insights for a file"""

        return {
            "total": len(insights),
            "critical": len([i for i in insights if i.get("priority") == "critical"]),
            "high": len([i for i in insights if i.get("priority") == "high"]),
            "medium": len([i for i in insights if i.get("priority") == "medium"]),
            "low": len([i for i in insights if i.get("priority") == "low"]),
            "types": Counter([i["type"] for i in insights]),
        }

    def _generate_summary(self) -> Dict:
        """Generate overall summary"""

        all_insights = self.results["insights_generated"]

        return {
            "files_analyzed": self.results["files_analyzed"],
            "strategies": dict(self.results["strategies_used"]),
            "total_insights": len(all_insights),
            "by_priority": {
                "critical": len([i for i in all_insights if i.get("priority") == "critical"]),
                "high": len([i for i in all_insights if i.get("priority") == "high"]),
                "medium": len([i for i in all_insights if i.get("priority") == "medium"]),
                "low": len([i for i in all_insights if i.get("priority") == "low"]),
            },
            "by_type": dict(Counter([i["type"] for i in all_insights])),
            "languages_detected": list(
                set([ctx.get("language") for ctx in self.results["contexts"].values() if ctx.get("language")])
            ),
            "frameworks_detected": list(
                set([fw for ctx in self.results["contexts"].values() for fw in ctx.get("frameworks", [])])
            ),
        }

    def print_report(self):
        """Print formatted analysis report"""

        logger.info(Path("\n") + "=" * 80)
        logger.info("ADAPTIVE CONTENT-AWARE ANALYSIS REPORT")
        logger.info("=" * 80)

        summary = self.results.get("summary", {})

        logger.info(f"\n📊 Overview:")
        logger.info(f"  Files Analyzed: {summary.get('files_analyzed', 0)}")
        logger.info(f"  Total Insights: {summary.get('total_insights', 0)}")

        logger.info(f"\n🎯 Strategies Used:")
        for strategy, count in summary.get("strategies", {}).items():
            logger.info(f"  {strategy}: {count} files")

        logger.info(f"\n⚠️  Insights by Priority:")
        for priority, count in summary.get("by_priority", {}).items():
            logger.info(f"  {priority}: {count}")

        logger.info(f"\n📋 Insights by Type:")
        for itype, count in summary.get("by_type", {}).items():
            logger.info(f"  {itype}: {count}")

        logger.info(f"\n💻 Languages Detected:")
        for lang in summary.get("languages_detected", []):
            logger.info(f"  - {lang}")

        if summary.get("frameworks_detected"):
            logger.info(f"\n🔧 Frameworks Detected:")
            for fw in summary.get("frameworks_detected", []):
                logger.info(f"  - {fw}")

        # Show critical insights
        critical = [i for i in self.results["insights_generated"] if i.get("priority") == "critical"]
        if critical:
            logger.info(f"\n🔴 CRITICAL Issues:")
            for insight in critical[:5]:
                logger.info(f"\n  {insight['title']}")
                logger.info(f"    {insight['message']}")
                if "action" in insight:
                    logger.info(f"    Action: {insight['action']}")

        logger.info(Path("\n") + "=" * 80)


def main():
    """main function."""

    import sys

    if len(sys.argv) < 2:
        logger.info("Usage: adaptive_analyzer.py <path> [quick|adaptive|deep]")
        logger.info("\nExample:")
        logger.info("  adaptive_analyzer.py /path/to/file.py")
        logger.info("  adaptive_analyzer.py /path/to/directory deep")
        sys.exit(1)

    target = sys.argv[1]
    thoroughness = sys.argv[2] if len(sys.argv) > 2 else "adaptive"

    analyzer = AdaptiveAnalyzer(target)
    results = analyzer.analyze(thoroughness)
    analyzer.print_report()

    # Save results
    output_file = Path("analysis_results.json")
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2, default=str)

    logger.info(f"\n💾 Full results saved to: {output_file}")


if __name__ == "__main__":
    main()
