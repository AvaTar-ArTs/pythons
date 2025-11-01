"""
Fluid Document Sweep

This module provides functionality for fluid document sweep.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Fluid Document Sweep - Find Interesting Python Scripts and Utilities
Analyzes ~/Documents directory to identify valuable scripts for reference repository
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Set, Optional
import re


@dataclass
class ScriptInfo:
    """Information about a discovered script"""

    path: str
    name: str
    extension: str
    size: int
    lines: int
    last_modified: str
    category: str
    complexity_score: int
    has_docstring: bool
    has_imports: bool
    has_functions: bool
    has_classes: bool
    has_main: bool
    dependencies: List[str]
    description: str
    tags: List[str]
    quality_score: int
    is_standalone: bool
    is_utility: bool
    is_automation: bool
    is_analysis: bool
    is_web: bool
    is_data: bool
    is_ai_ml: bool


class FluidDocumentSweeper:
    """Main class for analyzing documents and finding interesting scripts"""

    def __init__(self, root_dir: str = Path(str(Path.home()) + "/Documents")):
        """__init__ function."""

        self.root_dir = Path(root_dir)
        self.scripts: List[ScriptInfo] = []
        self.categories = {
            "python": [".py"],
            "shell": [".sh", ".bash", ".zsh"],
            "javascript": [".js", ".mjs", ".ts", ".tsx"],
            "html": [".html", ".htm"],
            "css": [".css", ".scss", ".sass"],
            "json": [".json"],
            "yaml": [".yml", ".yaml"],
            "markdown": [".md", ".rst"],
            "config": [".conf", ".cfg", ".ini", ".toml"],
            "data": [".csv", ".tsv", ".xml", ".sql"],
            "other": [],
        }

        # Quality indicators
        self.quality_keywords = {
            "high": [
                "class",
                "def",
                "import",
                "try",
                "except",
                "async",
                "await",
                "type",
                "dataclass",
            ],
            "medium": ["if", "for", "while", "return", "print", "main"],
            "low": ["pass", "TODO", "FIXME", "XXX"],
        }

        # Utility patterns
        self.utility_patterns = [
            r"organize",
            r"sort",
            r"clean",
            r"process",
            r"convert",
            r"generate",
            r"analyze",
            r"parse",
            r"extract",
            r"merge",
            r"split",
            r"filter",
            r"backup",
            r"sync",
            r"upload",
            r"download",
            r"install",
            r"setup",
        ]

        # AI/ML patterns
        self.ai_ml_patterns = [
            r"ml",
            r"machine.learning",
            r"neural",
            r"tensorflow",
            r"pytorch",
            r"scikit",
            r"pandas",
            r"numpy",
            r"matplotlib",
            r"seaborn",
            r"openai",
            r"huggingface",
            r"transformers",
            r"llm",
            r"gpt",
            r"claude",
            r"gemini",
            r"embedding",
            r"vector",
            r"prompt",
        ]

    def analyze_file(self, file_path: Path) -> Optional[ScriptInfo]:
        """Analyze a single file and extract metadata"""
        try:
            # Basic file info
            stat = file_path.stat()
            size = stat.st_size
            last_modified = datetime.fromtimestamp(stat.st_mtime).isoformat()

            # Determine category
            extension = file_path.suffix.lower()
            category = "other"
            for cat, exts in self.categories.items():
                if extension in exts:
                    category = cat
                    break

            # Read file content for analysis
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                lines = len(content.splitlines())
            except (OSError, IOError, FileNotFoundError):
                content = ""
                lines = 0

            # Analyze content for Python files
            if extension == ".py":
                return self._analyze_python_file(
                    file_path, content, size, last_modified, category
                )
            else:
                return self._analyze_other_file(
                    file_path, content, size, last_modified, category, extension
                )

        except Exception as e:
            logger.info(f"Error analyzing {file_path}: {e}")
            return None

    def _analyze_python_file(
        self,
        file_path: Path,
        content: str,
        size: int,
        last_modified: str,
        category: str,
    ) -> ScriptInfo:
        """Analyze Python file specifically"""
        lines = len(content.splitlines())

        # Count code elements
        has_docstring = '"""' in content or "'''" in content
        has_imports = bool(re.search(r"^(import|from)\s+", content, re.MULTILINE))
        has_functions = bool(re.search(r"^def\s+", content, re.MULTILINE))
        has_classes = bool(re.search(r"^class\s+", content, re.MULTILINE))
        has_main = 'if __name__ == "__main__"' in content

        # Extract dependencies
        imports = re.findall(r"^(import|from)\s+([^\s]+)", content, re.MULTILINE)
        dependencies = [imp[1].split(".")[0] for imp in imports]

        # Calculate complexity score
        complexity_score = self._calculate_complexity(content)

        # Determine script type
        is_standalone = has_main and not has_classes
        is_utility = any(
            re.search(pattern, file_path.name.lower())
            for pattern in self.utility_patterns
        )
        is_automation = any(
            word in content.lower()
            for word in ["automate", "schedule", "cron", "bot", "script"]
        )
        is_analysis = any(
            word in content.lower()
            for word in ["analyze", "analysis", "data", "statistics", "plot", "chart"]
        )
        is_web = any(
            word in content.lower()
            for word in ["flask", "django", "fastapi", "requests", "http", "api", "web"]
        )
        is_data = any(
            word in content.lower()
            for word in ["pandas", "numpy", "csv", "json", "sql", "database"]
        )
        is_ai_ml = any(
            re.search(pattern, content.lower()) for pattern in self.ai_ml_patterns
        )

        # Generate description
        description = self._generate_description(
            file_path, content, is_utility, is_automation, is_analysis
        )

        # Generate tags
        tags = self._generate_tags(
            file_path,
            content,
            is_utility,
            is_automation,
            is_analysis,
            is_web,
            is_data,
            is_ai_ml,
        )

        # Calculate quality score
        quality_score = self._calculate_quality_score(
            content, has_docstring, has_imports, has_functions, has_classes, has_main
        )

        return ScriptInfo(
            path=str(file_path),
            name=file_path.name,
            extension=file_path.suffix,
            size=size,
            lines=lines,
            last_modified=last_modified,
            category=category,
            complexity_score=complexity_score,
            has_docstring=has_docstring,
            has_imports=has_imports,
            has_functions=has_functions,
            has_classes=has_classes,
            has_main=has_main,
            dependencies=dependencies,
            description=description,
            tags=tags,
            quality_score=quality_score,
            is_standalone=is_standalone,
            is_utility=is_utility,
            is_automation=is_automation,
            is_analysis=is_analysis,
            is_web=is_web,
            is_data=is_data,
            is_ai_ml=is_ai_ml,
        )

    def _analyze_other_file(
        self,
        file_path: Path,
        content: str,
        size: int,
        last_modified: str,
        category: str,
        extension: str,
    ) -> Optional[ScriptInfo]:
        """Analyze non-Python files"""
        lines = len(content.splitlines())

        # Basic analysis for other file types
        is_utility = any(
            re.search(pattern, file_path.name.lower())
            for pattern in self.utility_patterns
        )
        is_automation = any(
            word in content.lower()
            for word in ["automate", "schedule", "cron", "bot", "script"]
        )
        is_analysis = any(
            word in content.lower()
            for word in ["analyze", "analysis", "data", "statistics"]
        )
        is_web = any(
            word in content.lower()
            for word in ["html", "css", "javascript", "web", "api"]
        )
        is_data = any(
            word in content.lower()
            for word in ["csv", "json", "xml", "sql", "database"]
        )
        is_ai_ml = any(
            re.search(pattern, content.lower()) for pattern in self.ai_ml_patterns
        )

        description = self._generate_description(
            file_path, content, is_utility, is_automation, is_analysis
        )
        tags = self._generate_tags(
            file_path,
            content,
            is_utility,
            is_automation,
            is_analysis,
            is_web,
            is_data,
            is_ai_ml,
        )

        return ScriptInfo(
            path=str(file_path),
            name=file_path.name,
            extension=extension,
            size=size,
            lines=lines,
            last_modified=last_modified,
            category=category,
            complexity_score=0,
            has_docstring=False,
            has_imports=False,
            has_functions=False,
            has_classes=False,
            has_main=False,
            dependencies=[],
            description=description,
            tags=tags,
            quality_score=50,  # Default for non-Python files
            is_standalone=True,
            is_utility=is_utility,
            is_automation=is_automation,
            is_analysis=is_analysis,
            is_web=is_web,
            is_data=is_data,
            is_ai_ml=is_ai_ml,
        )

    def _calculate_complexity(self, content: str) -> int:
        """Calculate a simple complexity score"""
        score = 0
        score += content.count("def ") * 2
        score += content.count("class ") * 3
        score += content.count("if ") * 1
        score += content.count("for ") * 1
        score += content.count("while ") * 1
        score += content.count("try:") * 1
        score += content.count("except") * 1
        score += content.count("import ") * 1
        return min(score, CONSTANT_100)  # Cap at CONSTANT_100

    def _calculate_quality_score(
        self,
        content: str,
        has_docstring: bool,
        has_imports: bool,
        has_functions: bool,
        has_classes: bool,
        has_main: bool,
    ) -> int:
        """Calculate quality score based on code structure"""
        score = 0
        if has_docstring:
            score += 20
        if has_imports:
            score += 10
        if has_functions:
            score += 15
        if has_classes:
            score += 20
        if has_main:
            score += 10

        # Check for good practices
        if 'if __name__ == "__main__"' in content:
            score += 10
        if "try:" in content and "except" in content:
            score += 10
        if "def main(" in content:
            score += 5

        # Check for bad practices
        if "print(" in content and "logging" not in content:
            score -= 5
        if "TODO" in content:
            score -= 5
        if "FIXME" in content:
            score -= 5

        return max(0, min(score, CONSTANT_100))

    def _generate_description(
        self,
        file_path: Path,
        content: str,
        is_utility: bool,
        is_automation: bool,
        is_analysis: bool,
    ) -> str:
        """Generate a description for the script"""
        name = file_path.stem.lower()

        if is_utility:
            return f"Utility script for {name.replace('_', ' ').replace('-', ' ')}"
        elif is_automation:
            return f"Automation script for {name.replace('_', ' ').replace('-', ' ')}"
        elif is_analysis:
            return f"Analysis tool for {name.replace('_', ' ').replace('-', ' ')}"
        else:
            return f"Script: {name.replace('_', ' ').replace('-', ' ')}"

    def _generate_tags(
        self,
        file_path: Path,
        content: str,
        is_utility: bool,
        is_automation: bool,
        is_analysis: bool,
        is_web: bool,
        is_data: bool,
        is_ai_ml: bool,
    ) -> List[str]:
        """Generate tags for the script"""
        tags = []

        if is_utility:
            tags.append("utility")
        if is_automation:
            tags.append("automation")
        if is_analysis:
            tags.append("analysis")
        if is_web:
            tags.append("web")
        if is_data:
            tags.append("data")
        if is_ai_ml:
            tags.append("ai-ml")

        # Add extension-based tags
        ext = file_path.suffix.lower()
        if ext == ".py":
            tags.append("python")
        elif ext in [".sh", ".bash"]:
            tags.append("shell")
        elif ext in [".js", ".ts"]:
            tags.append("javascript")
        elif ext == ".html":
            tags.append("html")
        elif ext == ".css":
            tags.append("css")
        elif ext == ".json":
            tags.append("json")
        elif ext == ".md":
            tags.append("markdown")

        return tags

    def sweep_documents(self, max_depth: int = 6) -> List[ScriptInfo]:
        """Perform the fluid sweep of documents directory"""
        logger.info(
            f"🔍 Starting fluid sweep of {self.root_dir} (max depth: {max_depth})"
        )

        interesting_files = []
        total_files = 0

        for root, dirs, files in os.walk(self.root_dir):
            # Calculate current depth
            depth = root.replace(str(self.root_dir), "").count(os.sep)
            if depth >= max_depth:
                dirs[:] = []  # Don't go deeper
                continue

            for file in files:
                file_path = Path(root) / file
                total_files += 1

                if total_files % CONSTANT_1000 == 0:
                    logger.info(f"📊 Processed {total_files} files...")

                # Skip certain files
                if self._should_skip_file(file_path):
                    continue

                script_info = self.analyze_file(file_path)
                if script_info and self._is_interesting(script_info):
                    interesting_files.append(script_info)

        logger.info(
            f"✅ Sweep complete! Found {len(interesting_files)} interesting files out of {total_files} total"
        )
        return interesting_files

    def _should_skip_file(self, file_path: Path) -> bool:
        """Determine if file should be skipped"""
        skip_patterns = [
            ".git",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            "node_modules",
            ".DS_Store",
            "Thumbs.db",
            ".pyc",
            ".log",
            ".tmp",
            ".temp",
            ".bak",
            ".backup",
        ]

        name = file_path.name.lower()
        return any(pattern in name for pattern in skip_patterns)

    def _is_interesting(self, script_info: ScriptInfo) -> bool:
        """Determine if a script is interesting enough for reference repo"""
        # Must have some minimum quality
        if script_info.quality_score < 30:
            return False

        # Must be a reasonable size (not too small, not too large)
        if (
            script_info.size < CONSTANT_100
            or script_info.size > 10 * CONSTANT_1024 * CONSTANT_1024
        ):  # CONSTANT_100 bytes to 10MB
            return False

        # Must have some content
        if script_info.lines < 5:
            return False

        # Must be one of the interesting types
        return any(
            [
                script_info.is_utility,
                script_info.is_automation,
                script_info.is_analysis,
                script_info.is_web,
                script_info.is_data,
                script_info.is_ai_ml,
                script_info.quality_score > 70,
            ]
        )

    def generate_report(self, scripts: List[ScriptInfo]) -> str:
        """Generate a comprehensive report"""
        report = []
        report.append("# 🔍 Fluid Document Sweep Report")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Total interesting files found:** {len(scripts)}")
        report.append("")

        # Summary by category
        by_category = {}
        for script in scripts:
            cat = script.category
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(script)

        report.append("## 📊 Summary by Category")
        for cat, scripts_list in sorted(by_category.items()):
            report.append(f"- **{cat.title()}:** {len(scripts_list)} files")
        report.append("")

        # Top quality scripts
        top_scripts = sorted(scripts, key=lambda x: x.quality_score, reverse=True)[:20]
        report.append("## ⭐ Top Quality Scripts")
        for i, script in enumerate(top_scripts, 1):
            report.append(f"{i:2d}. **{script.name}** (Score: {script.quality_score})")
            report.append(f"    - {script.description}")
            report.append(f"    - Tags: {', '.join(script.tags)}")
            report.append(f"    - Path: `{script.path}`")
            report.append("")

        # Scripts by type
        report.append("## 🏷️ Scripts by Type")
        types = ["utility", "automation", "analysis", "web", "data", "ai-ml"]
        for script_type in types:
            type_scripts = [s for s in scripts if script_type in s.tags]
            if type_scripts:
                report.append(f"### {script_type.title()} ({len(type_scripts)} files)")
                for script in sorted(
                    type_scripts, key=lambda x: x.quality_score, reverse=True
                )[:10]:
                    report.append(f"- **{script.name}** - {script.description}")
                report.append("")

        return Path("\n").join(report)

    def save_results(
        self, scripts: List[ScriptInfo], output_dir: str = Path("/Users/steven")
    ):
        """Save results to various formats"""
        output_path = Path(output_dir)

        # Save as JSON
        json_path = output_path / "fluid_sweep_results.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump([asdict(script) for script in scripts], f, indent=2)
        logger.info(f"📄 JSON results saved: {json_path}")

        # Save report
        report = self.generate_report(scripts)
        report_path = output_path / "FLUID_SWEEP_REPORT.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        logger.info(f"📄 Report saved: {report_path}")

        # Save CSV for easy filtering
        csv_path = output_path / "fluid_sweep_results.csv"
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write(
                "name,path,extension,size,lines,quality_score,category,tags,description,is_utility,is_automation,is_analysis,is_web,is_data,is_ai_ml\n"
            )
            for script in scripts:
                tags_str = ";".join(script.tags)
                f.write(
                    f'"{script.name}","{script.path}","{script.extension}",{script.size},{script.lines},{script.quality_score},"{script.category}","{tags_str}","{script.description}",{script.is_utility},{script.is_automation},{script.is_analysis},{script.is_web},{script.is_data},{script.is_ai_ml}\n'
                )
        logger.info(f"📄 CSV results saved: {csv_path}")


def main():
    """Main function"""
    logger.info("🚀 Starting Fluid Document Sweep...")

    sweeper = FluidDocumentSweeper()
    scripts = sweeper.sweep_documents(max_depth=6)

    if scripts:
        logger.info(f"\n🎯 Found {len(scripts)} interesting scripts!")
        sweeper.save_results(scripts)

        # Show top 10
        logger.info("\n🏆 Top 10 Most Interesting Scripts:")
        top_10 = sorted(scripts, key=lambda x: x.quality_score, reverse=True)[:10]
        for i, script in enumerate(top_10, 1):
            logger.info(
                f"{i:2d}. {script.name} (Score: {script.quality_score}) - {script.description}"
            )
    else:
        logger.info("😔 No interesting scripts found. Try adjusting the criteria.")


if __name__ == "__main__":
    main()
