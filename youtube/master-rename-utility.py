"""
Master Rename Utility

This module provides functionality for master rename utility.

Author: Auto-generated
Date: 2025-11-01
"""

# Constants
CONSTANT_100 = 100
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Master Rename Utility - Advanced Python File Renaming System
Combines all advanced renaming capabilities into a unified interface
"""

import ast
import os
import re
import json
import csv
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set, Any, Union
from collections import Counter, defaultdict
from datetime import datetime
import hashlib

# Optional imports for advanced features
try:
    import openai
    from env_d_loader import load_dotenv

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import cv2
    import pytesseract
    from PIL import Image, ImageOps

    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class MasterRenamer:
    """
    Master rename utility that combines all advanced renaming capabilities
    """

    def __init__(self, project_root: Path, config: Optional[Dict] = None):
        """__init__ function."""

        self.project_root = Path(project_root)
        self.config = config or self._default_config()
        self.rename_log = []
        self.files_processed = 0
        self.files_renamed = 0
        self.duplicates_found = 0

        # Initialize OpenAI if available
        if OPENAI_AVAILABLE:
            self._setup_openai()

    def _default_config(self) -> Dict:
        """Default configuration for the renamer"""
        return {
            "dry_run": True,
            "backup": True,
            "recursive": True,
            "file_types": [".py", ".md", ".txt", ".json", ".csv"],
            "image_types": [".jpg", ".jpeg", ".png", ".webp", ".tiff"],
            "video_types": [".mp4", ".webm", ".mov", ".mkv"],
            "min_file_size": CONSTANT_100,  # bytes
            "max_file_size": CONSTANT_100 * CONSTANT_1024 * CONSTANT_1024,  # 100MB
            "exclude_patterns": [r"^\.", r"__pycache__", r"\.git", r"\.DS_Store", r"node_modules"],
            "bad_naming_patterns": [
                r"^test\d+\.py$",
                r"^main\d+\.py$",
                r"^script\d*\.py$",
                r"^temp\d*\.py$",
                r"^new\d*\.py$",
                r"^old\d*\.py$",
                r"^untitled\d*\.py$",
                r"^[a-z]\.py$",
                r"^[a-z]\d\.py$",
                r"^\d+\.py$",
                r"_\d+\.py$",
                r"^copy.*\.py$",
                r".*\s+copy.*\.py$",
                r".*\s+\d+\.py$",
            ],
            "function_patterns": {
                "test": ["test_", "unittest", "pytest"],
                "api": ["api", "endpoint", "route", "flask", "fastapi"],
                "cli": ["argparse", "click", "sys.argv", "main"],
                "config": ["config", "settings", "env", "dotenv"],
                "database": ["sqlalchemy", "pymongo", "psycopg2", "database"],
                "scraper": ["beautifulsoup", "selenium", "scrapy", "requests"],
                "bot": ["telegram", "discord", "slack", "bot"],
                "analyzer": ["analyze", "analysis", "metrics"],
                "generator": ["generate", "create", "build"],
                "processor": ["process", "transform", "convert"],
                "downloader": ["download", "fetch", "retrieve"],
                "uploader": ["upload", "push", "send"],
                "monitor": ["monitor", "watch", "observe"],
                "scheduler": ["schedule", "cron", "timer"],
                "validator": ["validate", "verify", "check"],
            },
            "theme_patterns": {
                "youtube": ["youtube", "yt_", "video", "download", "playlist"],
                "ai": ["whisper", "openai", "dalle", "gpt", "ai_", "transcribe"],
                "data": ["csv", "data", "process", "analyze", "pandas"],
                "web": ["scrape", "requests", "beautifulsoup", "selenium"],
                "utility": ["util", "helper", "common", "base", "config"],
            },
        }

    def _setup_openai(self):
        """Setup OpenAI API if available"""
        try:
            load_dotenv()
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                openai.api_key = api_key
                logger.info("OpenAI API configured")
            else:
                logger.warning("OpenAI API key not found")
        except Exception as e:
            logger.warning(f"OpenAI setup failed: {e}")

    def is_badly_named(self, filename: str) -> bool:
        """Check if filename matches bad naming patterns"""
        for pattern in self.config["bad_naming_patterns"]:
            if re.match(pattern, filename, re.IGNORECASE):
                return True
        return False

    def should_exclude(self, filepath: Path) -> bool:
        """Check if file should be excluded from processing"""
        # Check file size
        try:
            size = filepath.stat().st_size
            if size < self.config["min_file_size"] or size > self.config["max_file_size"]:
                return True
        except OSError:
            return True

        # Check exclude patterns
        for pattern in self.config["exclude_patterns"]:
            if re.search(pattern, str(filepath)):
                return True

        return False

    def analyze_file_content(self, filepath: Path) -> Dict:
        """Comprehensive file content analysis"""
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")

            analysis = {
                "imports": [],
                "main_imports": [],
                "functions": [],
                "main_functions": [],
                "classes": [],
                "docstring": None,
                "main_verbs": [],
                "main_nouns": [],
                "api_services": [],
                "file_operations": [],
                "themes": [],
                "keywords": [],
                "complexity": 0,
                "lines_of_code": len(content.splitlines()),
                "file_type": filepath.suffix.lower(),
            }

            # Parse AST for Python files
            if filepath.suffix.lower() == ".py":
                try:
                    tree = ast.parse(content)

                    # Get module docstring
                    if (
                        tree.body
                        and isinstance(tree.body[0], ast.Expr)
                        and isinstance(tree.body[0].value, ast.Constant)
                    ):
                        analysis["docstring"] = tree.body[0].value.value

                    # Collect all imports and functions
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                analysis["imports"].append(alias.name)
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                analysis["imports"].append(node.module)
                        elif isinstance(node, ast.FunctionDef):
                            analysis["functions"].append(node.name)
                        elif isinstance(node, ast.ClassDef):
                            analysis["classes"].append(node.name)

                    # Identify main imports (non-standard library)
                    stdlib_modules = {
                        "os",
                        "sys",
                        "re",
                        "json",
                        "time",
                        "datetime",
                        "logging",
                        "pathlib",
                        "typing",
                        "collections",
                    }
                    for imp in analysis["imports"]:
                        base = imp.split(".")[0]
                        if base not in stdlib_modules:
                            analysis["main_imports"].append(base)

                    analysis["main_imports"] = list(set(analysis["main_imports"]))[:5]

                    # Identify main functions (not test_, not __)
                    main_funcs = [
                        f for f in analysis["functions"] if not f.startswith("test_") and not f.startswith("_")
                    ]
                    analysis["main_functions"] = main_funcs[:5]

                    # Calculate complexity
                    analysis["complexity"] = self._calculate_complexity(tree)

                except SyntaxError:
                    logger.debug(f"Syntax error parsing {filepath}")

            # Extract action verbs
            analysis["main_verbs"] = self._extract_verbs(analysis["functions"], content)

            # Extract nouns (what it operates on)
            analysis["main_nouns"] = self._extract_nouns(content, analysis["main_imports"])

            # Detect API services
            analysis["api_services"] = self._detect_api_services(content, analysis["imports"])

            # Detect file operations
            analysis["file_operations"] = self._detect_file_operations(content)

            # Detect themes
            analysis["themes"] = self._detect_themes(content)

            # Extract keywords
            analysis["keywords"] = self._extract_keywords(content)

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing {filepath}: {e}")
            return {}

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1

        for child in ast.walk(tree):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity

    def _extract_verbs(self, functions: List[str], content: str) -> List[str]:
        """Extract action verbs from function names and content"""
        verb_patterns = [
            "upload",
            "download",
            "fetch",
            "get",
            "retrieve",
            "send",
            "post",
            "analyze",
            "process",
            "parse",
            "transform",
            "convert",
            "generate",
            "create",
            "build",
            "make",
            "compile",
            "render",
            "scrape",
            "crawl",
            "extract",
            "collect",
            "compress",
            "decompress",
            "encode",
            "decode",
            "encrypt",
            "decrypt",
            "hash",
            "sign",
            "validate",
            "verify",
            "check",
            "test",
            "monitor",
            "watch",
            "track",
            "log",
            "schedule",
            "queue",
            "dispatch",
            "transcribe",
            "translate",
            "synthesize",
            "upscale",
            "resize",
            "crop",
            "enhance",
            "notify",
            "alert",
            "email",
            "message",
        ]

        found_verbs = []
        content_lower = content.lower()

        # Check function names
        for func in functions:
            for verb in verb_patterns:
                if verb in func.lower():
                    found_verbs.append(verb)

        # Check content frequency
        verb_counts = Counter()
        for verb in verb_patterns:
            if verb in content_lower:
                verb_counts[verb] = content_lower.count(verb)

        # Combine and rank
        for verb, count in verb_counts.most_common(5):
            if count > 2 and verb not in found_verbs:
                found_verbs.append(verb)

        return found_verbs[:3]

    def _extract_nouns(self, content: str, imports: List[str]) -> List[str]:
        """Extract key nouns (what it operates on)"""
        noun_patterns = {
            "video": ["video", "mp4", "avi", "mov"],
            "audio": ["audio", "mp3", "wav", "sound"],
            "image": ["image", "jpg", "png", "photo", "picture"],
            "pdf": ["pdf"],
            "html": ["html", "webpage"],
            "csv": ["csv", "spreadsheet"],
            "json": ["json"],
            "xml": ["xml"],
            "text": ["text", "txt"],
            "youtube": ["youtube", "yt"],
            "instagram": ["instagram", "ig"],
            "twitter": ["twitter"],
            "reddit": ["reddit"],
            "telegram": ["telegram"],
            "database": ["database", "db", "sql"],
            "api": ["api", "endpoint", "rest"],
            "file": ["file"],
            "url": ["url", "link"],
            "email": ["email", "mail"],
            "gallery": ["gallery", "album"],
            "thumbnail": ["thumbnail", "thumb"],
            "subtitle": ["subtitle", "srt", "caption"],
            "transcript": ["transcript", "transcription"],
        }

        found_nouns = []
        content_lower = content.lower()

        for noun, patterns in noun_patterns.items():
            for pattern in patterns:
                if pattern in content_lower:
                    count = content_lower.count(pattern)
                    if count >= 3:
                        found_nouns.append(noun)
                        break

        return list(set(found_nouns))[:3]

    def _detect_api_services(self, content: str, imports: List[str]) -> List[str]:
        """Detect which API services are being used"""
        services = []
        content_lower = content.lower()

        service_keywords = {
            "openai": ["openai", "gpt", "dall-e"],
            "youtube": ["youtube", "yt-dlp", "pytube"],
            "instagram": ["instagram", "instabot"],
            "twitter": ["twitter", "tweepy"],
            "reddit": ["reddit", "praw"],
            "telegram": ["telegram"],
            "aws": ["boto3", "aws", "s3"],
            "google": ["google", "google_api"],
            "stripe": ["stripe"],
            "twilio": ["twilio"],
        }

        for service, keywords in service_keywords.items():
            if any(kw in content_lower for kw in keywords):
                services.append(service)

        return services

    def _detect_file_operations(self, content: str) -> List[str]:
        """Detect what file operations are being performed"""
        ops = []
        content_lower = content.lower()

        if "upload" in content_lower:
            ops.append("upload")
        if "download" in content_lower:
            ops.append("download")
        if "compress" in content_lower:
            ops.append("compress")
        if "convert" in content_lower or "transform" in content_lower:
            ops.append("convert")
        if "parse" in content_lower:
            ops.append("parse")
        if "generate" in content_lower or "create" in content_lower:
            ops.append("generate")

        return ops

    def _detect_themes(self, content: str) -> List[str]:
        """Detect content themes"""
        themes = []
        content_lower = content.lower()

        for theme, patterns in self.config["theme_patterns"].items():
            if any(pattern in content_lower for pattern in patterns):
                themes.append(theme)

        return themes

    def _extract_keywords(self, content: str) -> List[str]:
        """Extract important keywords from content"""
        # Extract words from headers and important sections
        lines = content.split("\n")
        key_terms = []

        for line in lines[:50]:  # Look at first 50 lines
            line = line.strip()
            if line.startswith("#") or line.startswith("**") or line.startswith("-"):
                # Extract meaningful words
                words = re.findall(r"\b[A-Za-z]{3,}\b", line)
                key_terms.extend(words[:3])

        # Remove common words
        common_words = {
            "the",
            "and",
            "for",
            "with",
            "this",
            "that",
            "from",
            "into",
            "your",
            "are",
            "has",
            "have",
            "will",
            "can",
            "should",
            "project",
            "analysis",
            "generated",
            "files",
            "total",
            "size",
            "words",
            "chat",
            "id",
            "categories",
            "code",
            "blocks",
            "tool",
            "calls",
            "modified",
            "man",
            "thinketh",
            "james",
            "allen",
        }

        key_terms = [word.lower() for word in key_terms if word.lower() not in common_words]

        return key_terms[:5]

    def suggest_better_name(self, filepath: Path, analysis: Dict) -> Optional[str]:
        """Suggest a better filename based on comprehensive analysis"""
        current_name = filepath.stem

        # Don't rename if already well-named
        if not self.is_badly_named(filepath.name):
            return None

        # Build name from analysis
        name_parts = []

        # Add theme if detected
        if analysis.get("themes"):
            theme = analysis["themes"][0]
            if theme == "youtube":
                name_parts.append("yt")
            elif theme == "ai":
                name_parts.append("ai")
            elif theme == "data":
                name_parts.append("data")
            elif theme == "web":
                name_parts.append("web")
            elif theme == "utility":
                name_parts.append("util")

        # Add primary action
        if analysis.get("main_verbs"):
            action = analysis["main_verbs"][0]
            # Abbreviate common actions
            abbreviations = {
                "download": "dl",
                "upload": "ul",
                "generate": "gen",
                "process": "proc",
                "analyze": "analyze",
                "transcribe": "transcribe",
                "convert": "conv",
                "compress": "comp",
                "extract": "ext",
                "validate": "val",
            }
            name_parts.append(abbreviations.get(action, action))

        # Add primary subject
        if analysis.get("main_nouns"):
            subject = analysis["main_nouns"][0]
            # Abbreviate common subjects
            abbreviations = {
                "video": "vid",
                "image": "img",
                "audio": "aud",
                "database": "db",
                "gallery": "gal",
                "thumbnail": "thumb",
                "youtube": "yt",
                "instagram": "ig",
            }
            name_parts.append(abbreviations.get(subject, subject))

        # Add API service if significant
        if analysis.get("api_services") and not any(api in name_parts for api in ["yt", "ig"]):
            api = analysis["api_services"][0]
            if api == "youtube":
                name_parts.insert(0, "yt")
            elif api == "instagram":
                name_parts.insert(0, "ig")
            elif api == "openai":
                name_parts.insert(0, "ai")

        if not name_parts:
            return None

        # Build final name
        new_name = "_".join(name_parts[:3])  # Max 3 parts
        new_name = re.sub(r"[^a-zA-Z0-9_]", "", new_name)  # Clean filename

        # Add extension
        new_name += filepath.suffix

        # Check if different from current
        if new_name == filepath.name:
            return None

        # Check if target exists
        target = filepath.parent / new_name
        if target.exists() and target != filepath:
            # Add counter
            counter = 2
            base_name = new_name.rsplit(".", 1)[0]
            ext = new_name.rsplit(".", 1)[1] if "." in new_name else ""
            while (filepath.parent / f"{base_name}_{counter}.{ext}").exists():
                counter += 1
            new_name = f"{base_name}_{counter}.{ext}"

        return new_name

    def process_file(self, filepath: Path) -> Optional[Dict]:
        """Process a single file and suggest rename"""
        if self.should_exclude(filepath):
            return None

        # Skip if not a supported file type
        if filepath.suffix.lower() not in self.config["file_types"]:
            return None

        # Analyze file content
        analysis = self.analyze_file_content(filepath)

        # Suggest better name
        new_name = self.suggest_better_name(filepath, analysis)

        if new_name:
            return {
                "current_path": str(filepath),
                "current_name": filepath.name,
                "suggested_name": new_name,
                "analysis": analysis,
                "reason": self._generate_reason(analysis),
            }

        return None

    def _generate_reason(self, analysis: Dict) -> str:
        """Generate human-readable reason for rename suggestion"""
        reasons = []

        if analysis.get("themes"):
            reasons.append(f"Theme: {', '.join(analysis['themes'][:2])}")

        if analysis.get("main_verbs"):
            reasons.append(f"Actions: {', '.join(analysis['main_verbs'][:2])}")

        if analysis.get("main_nouns"):
            reasons.append(f"Operates on: {', '.join(analysis['main_nouns'][:2])}")

        if analysis.get("api_services"):
            reasons.append(f"APIs: {', '.join(analysis['api_services'][:2])}")

        return "; ".join(reasons) if reasons else "Content analysis"

    def analyze_project(self) -> List[Dict]:
        """Analyze entire project and suggest renames"""
        logger.info("🔍 Analyzing project for intelligent renaming...")

        suggestions = []
        python_files = []

        # Find all Python files
        if self.config["recursive"]:
            python_files = list(self.project_root.rglob("*.py"))
        else:
            python_files = list(self.project_root.glob("*.py"))

        logger.info(f"📁 Found {len(python_files)} Python files")

        for filepath in python_files:
            suggestion = self.process_file(filepath)
            if suggestion:
                suggestions.append(suggestion)
                self.files_processed += 1

        logger.info(f"💡 Generated {len(suggestions)} rename suggestions")

        return suggestions

    def apply_renames(self, suggestions: List[Dict], auto_approve: bool = False) -> int:
        """Apply suggested renames"""
        if not suggestions:
            logger.info("✅ No renames needed!")
            return 0

        logger.info(f"📝 Applying {len(suggestions)} renames...")

        applied = 0
        for suggestion in suggestions:
            current = Path(suggestion["current_path"])
            new_path = current.parent / suggestion["suggested_name"]

            if not auto_approve:
                response = input(f"Rename {current.name} → {suggestion['suggested_name']}? [y/N]: ")
                if response.lower() not in ["y", "yes"]:
                    continue

            try:
                # Check if git tracked
                result = subprocess.run(["git", "ls-files", "--error-unmatch", str(current)], capture_output=True)
                is_tracked = result.returncode == 0

                if is_tracked:
                    subprocess.run(["git", "mv", str(current), str(new_path)], check=True)
                    logger.info(f"✅ Renamed (git): {current.name} → {suggestion['suggested_name']}")
                else:
                    current.rename(new_path)
                    logger.info(f"✅ Renamed: {current.name} → {suggestion['suggested_name']}")

                # Log the rename
                self.rename_log.append(
                    {
                        "original": str(current),
                        "new": str(new_path),
                        "timestamp": datetime.now().isoformat(),
                        "reason": suggestion["reason"],
                    }
                )

                applied += 1
                self.files_renamed += 1

            except Exception as e:
                logger.error(f"❌ Error renaming {current.name}: {e}")

        logger.info(f"✅ Successfully renamed {applied}/{len(suggestions)} files")
        return applied

    def export_report(self, suggestions: List[Dict], output_path: Path):
        """Export rename suggestions to various formats"""
        output_path.mkdir(parents=True, exist_ok=True)

        # Export JSON report
        json_path = output_path / "rename_suggestions.json"
        with open(json_path, "w") as f:
            json.dump(suggestions, f, indent=2, default=str)

        # Export CSV report
        csv_path = output_path / "rename_suggestions.csv"
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Current Name", "Suggested Name", "Reason", "Themes", "Actions", "APIs"])
            for suggestion in suggestions:
                analysis = suggestion["analysis"]
                writer.writerow(
                    [
                        suggestion["current_name"],
                        suggestion["suggested_name"],
                        suggestion["reason"],
                        ", ".join(analysis.get("themes", [])),
                        ", ".join(analysis.get("main_verbs", [])),
                        ", ".join(analysis.get("api_services", [])),
                    ]
                )

        # Export summary
        summary_path = output_path / "rename_summary.txt"
        with open(summary_path, "w") as f:
            f.write(f"Rename Analysis Summary\n")
            f.write(f"======================\n\n")
            f.write(f"Project: {self.project_root}\n")
            f.write(f"Files processed: {self.files_processed}\n")
            f.write(f"Suggestions generated: {len(suggestions)}\n")
            f.write(f"Date: {datetime.now().isoformat()}\n\n")

            f.write("Suggestions:\n")
            for i, suggestion in enumerate(suggestions, 1):
                f.write(f"{i:3d}. {suggestion['current_name']} → {suggestion['suggested_name']}\n")
                f.write(f"     Reason: {suggestion['reason']}\n\n")

        logger.info(f"📄 Reports exported to {output_path}")

    def run(self, apply: bool = False, output_dir: Optional[Path] = None):
        """Main execution method"""
        logger.info("🚀 Starting Master Rename Utility")
        logger.info(f"📁 Project: {self.project_root}")
        logger.info(f"🔧 Mode: {'Apply' if apply else 'Dry Run'}")

        # Analyze project
        suggestions = self.analyze_project()

        if not suggestions:
            logger.info("✅ No files need renaming!")
            return

        # Display suggestions
        logger.info(f"\n📝 Rename Suggestions ({len(suggestions)} files):\n")
        for i, suggestion in enumerate(suggestions, 1):
            logger.info(f"{i:3d}. {suggestion['current_name']} → {suggestion['suggested_name']}")
            logger.info(f"     Reason: {suggestion['reason']}")
            logger.info("")

        # Apply renames if requested
        if apply:
            applied = self.apply_renames(suggestions, auto_approve=True)
            logger.info(f"✅ Applied {applied} renames")
        else:
            logger.info("💡 Run with --apply to execute renames")

        # Export reports
        if output_dir:
            self.export_report(suggestions, Path(output_dir))

        return suggestions


def main():
    """Command line interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Master Rename Utility - Advanced Python File Renaming System")
    parser.add_argument("path", type=Path, nargs="?", default=Path.cwd(), help="Project directory to analyze")
    parser.add_argument("--apply", action="store_true", help="Actually apply the renames (default: dry-run only)")
    parser.add_argument("--output", type=Path, help="Output directory for reports")
    parser.add_argument("--config", type=Path, help="Custom configuration file (JSON)")

    args = parser.parse_args()

    # Load custom config if provided
    config = None
    if args.config and args.config.exists():
        with open(args.config) as f:
            config = json.load(f)

    # Create renamer and run
    renamer = MasterRenamer(args.path, config)
    renamer.run(apply=args.apply, output_dir=args.output)


if __name__ == "__main__":
    main()
