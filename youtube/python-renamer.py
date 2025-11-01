#!/usr/bin/env python3
"""
Simple Python Renamer for ~/Documents/python
Follows Steven's preferred naming style: simple, hyphenated, descriptive
Examples: analyze-mp3-transcript-prompts_from_transcribe-analysis.py
"""

import ast
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Set
from collections import Counter
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class SimplePythonRenamer:
    """Simplified renamer for ~/Documents/python following Steven's style"""

    def __init__(self, project_root: Path):
        """__init__ function."""

        self.project_root = project_root
        self.rename_suggestions = []

        # Steven's preferred naming patterns
        self.action_words = {
            "analyze": ["analyze", "analysis", "analytics"],
            "transcribe": ["transcribe", "transcript", "whisper"],
            "batch": ["batch", "bulk", "process"],
            "archive": ["archive", "backup", "compress"],
            "download": ["download", "fetch", "get"],
            "upload": ["upload", "send", "post"],
            "convert": ["convert", "transform", "change"],
            "generate": ["generate", "create", "make"],
            "extract": ["extract", "parse", "pull"],
            "compress": ["compress", "zip", "pack"],
            "resize": ["resize", "scale", "crop"],
            "merge": ["merge", "combine", "join"],
            "split": ["split", "divide", "separate"],
            "clean": ["clean", "sanitize", "fix"],
            "validate": ["validate", "check", "verify"],
        }

        self.subject_words = {
            "mp3": ["mp3", "audio", "sound", "music"],
            "video": ["video", "mp4", "avi", "mov"],
            "image": ["image", "img", "jpg", "png", "photo"],
            "text": ["text", "txt", "content", "data"],
            "csv": ["csv", "spreadsheet", "data"],
            "json": ["json", "api", "response"],
            "pdf": ["pdf", "document"],
            "prompt": ["prompt", "template", "instruction"],
            "transcript": ["transcript", "transcription", "whisper"],
            "file": ["file", "files"],
            "folder": ["folder", "directory", "dir"],
            "url": ["url", "link", "web"],
            "email": ["email", "mail"],
            "youtube": ["youtube", "yt", "video"],
            "instagram": ["instagram", "ig", "social"],
        }

        # Bad patterns to fix
        self.bad_patterns = [
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
            r"^yt_.*\.py$",  # Remove yt_ prefix
            r"^ig_.*\.py$",  # Remove ig_ prefix
        ]

    def is_badly_named(self, filename: str) -> bool:
        """Check if filename matches bad naming patterns"""
        for pattern in self.bad_patterns:
            if re.match(pattern, filename, re.IGNORECASE):
                return True
        return False

    def analyze_file_content(self, filepath: Path) -> Dict:
        """Analyze file content to understand its purpose"""
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")

            analysis = {
                "imports": [],
                "functions": [],
                "classes": [],
                "docstring": None,
                "keywords": [],
                "file_operations": [],
                "api_services": [],
            }

            # Parse AST
            try:
                tree = ast.parse(content)

                # Get docstring
                if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant):
                    analysis["docstring"] = tree.body[0].value.value

                # Get imports and functions
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
            except (ImportError, ModuleNotFoundError):
                pass

            # Extract keywords from content
            keywords = re.findall(r"\b[a-z_]{3,}\b", content.lower())
            keyword_counts = Counter(keywords)
            analysis["keywords"] = [k for k, v in keyword_counts.most_common(20)]

            # Detect file operations
            analysis["file_operations"] = self._detect_file_operations(content)

            # Detect API services
            analysis["api_services"] = self._detect_api_services(content)

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing {filepath}: {e}")
            return {}

    def _detect_file_operations(self, content: str) -> List[str]:
        """Detect file operations from content"""
        ops = []
        content_lower = content.lower()

        if "open(" in content_lower and "read" in content_lower:
            ops.append("read")
        if "open(" in content_lower and "write" in content_lower:
            ops.append("write")
        if "os.rename" in content_lower or "rename" in content_lower:
            ops.append("rename")
        if "os.remove" in content_lower or "delete" in content_lower:
            ops.append("delete")
        if "shutil.copy" in content_lower or "copy" in content_lower:
            ops.append("copy")
        if "move" in content_lower:
            ops.append("move")

        return ops

    def _detect_api_services(self, content: str) -> List[str]:
        """Detect API services from content"""
        services = []
        content_lower = content.lower()

        if "openai" in content_lower or "whisper" in content_lower:
            services.append("openai")
        if "youtube" in content_lower or "yt-dlp" in content_lower:
            services.append("youtube")
        if "instagram" in content_lower or "instabot" in content_lower:
            services.append("instagram")
        if "requests" in content_lower:
            services.append("requests")
        if "pandas" in content_lower:
            services.append("pandas")
        if "pillow" in content_lower or "pil" in content_lower:
            services.append("pillow")

        return services

    def suggest_simple_name(self, filepath: Path, analysis: Dict) -> Optional[str]:
        """Suggest a simple name following Steven's style"""
        current_name = filepath.stem

        # Don't rename if already well-named
        if not self.is_badly_named(filepath.name):
            return None

        # Extract action and subject from analysis
        action = self._extract_action(analysis)
        subject = self._extract_subject(analysis)

        # Build name parts
        name_parts = []

        # Add action if found
        if action:
            name_parts.append(action)

        # Add subject if found
        if subject:
            name_parts.append(subject)

        # Add additional context from keywords
        context = self._extract_context(analysis)
        if context and context not in name_parts:
            name_parts.append(context)

        # If no clear action/subject, try to infer from filename
        if not name_parts:
            name_parts = self._infer_from_filename(current_name)

        if not name_parts:
            return None

        # Build final name with hyphens
        new_name = "-".join(name_parts) + ".py"

        # Clean up the name
        new_name = re.sub(r"[^a-zA-Z0-9\-\.]", "", new_name)
        new_name = re.sub(r"-+", "-", new_name)
        new_name = new_name.strip("-")

        # Check if different from current
        if new_name == filepath.name:
            return None

        # Check if target exists
        target = filepath.parent / new_name
        if target.exists() and target != filepath:
            # Add counter
            counter = 2
            base_name = new_name.rsplit(".", 1)[0]
            while (filepath.parent / f"{base_name}-{counter}.py").exists():
                counter += 1
            new_name = f"{base_name}-{counter}.py"

        return new_name

    def _extract_action(self, analysis: Dict) -> Optional[str]:
        """Extract action word from analysis"""
        # Check functions
        for func in analysis.get("functions", []):
            for action, patterns in self.action_words.items():
                if any(pattern in func.lower() for pattern in patterns):
                    return action

        # Check keywords
        for keyword in analysis.get("keywords", [])[:10]:
            for action, patterns in self.action_words.items():
                if any(pattern in keyword for pattern in patterns):
                    return action

        # Check docstring
        if analysis.get("docstring"):
            doc_lower = analysis["docstring"].lower()
            for action, patterns in self.action_words.items():
                if any(pattern in doc_lower for pattern in patterns):
                    return action

        return None

    def _extract_subject(self, analysis: Dict) -> Optional[str]:
        """Extract subject word from analysis"""
        # Check keywords
        for keyword in analysis.get("keywords", [])[:10]:
            for subject, patterns in self.subject_words.items():
                if any(pattern in keyword for pattern in patterns):
                    return subject

        # Check imports
        for imp in analysis.get("imports", []):
            for subject, patterns in self.subject_words.items():
                if any(pattern in imp.lower() for pattern in patterns):
                    return subject

        # Check docstring
        if analysis.get("docstring"):
            doc_lower = analysis["docstring"].lower()
            for subject, patterns in self.subject_words.items():
                if any(pattern in doc_lower for pattern in patterns):
                    return subject

        return None

    def _extract_context(self, analysis: Dict) -> Optional[str]:
        """Extract additional context from analysis"""
        # Look for specific patterns in keywords
        context_keywords = ["prompt", "template", "config", "settings", "util", "helper"]

        for keyword in analysis.get("keywords", [])[:10]:
            if keyword in context_keywords:
                return keyword

        # Check for specific file operations
        if "read" in analysis.get("file_operations", []):
            return "reader"
        if "write" in analysis.get("file_operations", []):
            return "writer"

        return None

    def _infer_from_filename(self, filename: str) -> List[str]:
        """Infer name parts from current filename"""
        # Remove common prefixes
        clean_name = re.sub(r"^(yt_|ig_|test_|main_|script_|temp_|new_|old_)", "", filename.lower())

        # Split by common separators
        parts = re.split(r"[_\-\s]+", clean_name)

        # Filter out numbers and short words
        filtered_parts = [part for part in parts if len(part) > 2 and not part.isdigit()]

        return filtered_parts[:3]  # Max 3 parts

    def analyze_project(self) -> List[Dict]:
        """Analyze all Python files and suggest renames"""
        logger.info("🔍 Analyzing Python files for simple renaming...")

        python_files = list(self.project_root.glob("*.py"))
        logger.info(f"📁 Found {len(python_files)} Python files")

        suggestions = []
        badly_named_count = 0

        for filepath in python_files:
            # Skip hidden files
            if filepath.name.startswith("."):
                continue

            # Check if badly named
            if self.is_badly_named(filepath.name):
                badly_named_count += 1

                # Analyze content
                analysis = self.analyze_file_content(filepath)

                # Suggest better name
                new_name = self.suggest_simple_name(filepath, analysis)

                if new_name and new_name != filepath.name:
                    suggestions.append(
                        {
                            "current_path": str(filepath),
                            "current_name": filepath.name,
                            "suggested_name": new_name,
                            "reason": self._generate_reason(analysis),
                            "action": self._extract_action(analysis),
                            "subject": self._extract_subject(analysis),
                        }
                    )

        logger.info(f"\n📊 Found {badly_named_count} badly named files")
        logger.info(f"💡 Generated {len(suggestions)} rename suggestions\n")

        return suggestions

    def _generate_reason(self, analysis: Dict) -> str:
        """Generate human-readable reason for rename suggestion"""
        reasons = []

        action = self._extract_action(analysis)
        if action:
            reasons.append(f"Action: {action}")

        subject = self._extract_subject(analysis)
        if subject:
            reasons.append(f"Subject: {subject}")

        if analysis.get("api_services"):
            reasons.append(f"APIs: {', '.join(analysis['api_services'][:2])}")

        return "; ".join(reasons) if reasons else "Content analysis"

    def apply_renames(self, suggestions: List[Dict], auto_approve: bool = False):
        """Apply suggested renames"""
        if not suggestions:
            logger.info("✅ No renames needed!")
            return

        logger.info(f"📝 Rename Suggestions ({len(suggestions)} files):\n")

        applied = 0
        for i, suggestion in enumerate(suggestions, 1):
            current = Path(suggestion["current_path"])
            suggested = current.parent / suggestion["suggested_name"]

            logger.info(f"{i:3d}. {suggestion['current_name']}")
            logger.info(f"     → {suggestion['suggested_name']}")
            logger.info(f"     Reason: {suggestion['reason']}")
            logger.info("")

            if not auto_approve:
                continue

            try:
                # Check if git tracked
                result = subprocess.run(["git", "ls-files", "--error-unmatch", str(current)], capture_output=True)
                is_tracked = result.returncode == 0

                if is_tracked:
                    subprocess.run(["git", "mv", str(current), str(suggested)], check=True)
                    logger.info(f"     ✅ Renamed (git tracked)")
                else:
                    current.rename(suggested)
                    logger.info(f"     ✅ Renamed")
                applied += 1
            except Exception as e:
                logger.error(f"     ❌ Error: {e}")

            logger.info("")

        if auto_approve:
            logger.info(f"✅ Successfully renamed {applied}/{len(suggestions)} files")
        else:
            logger.info(f"\n💡 To apply renames, run with --apply flag")


def main():
    """main function."""

    import argparse

    parser = argparse.ArgumentParser(description="Simple Python Renamer for ~/Documents/python")
    parser.add_argument(
        "path",
        type=Path,
        nargs="?",
        default=Path.home() / "Documents" / "python",
        help="Python directory to analyze (default: ~/Documents/python)",
    )
    parser.add_argument("--apply", action="store_true", help="Actually apply the renames (default: dry-run only)")
    parser.add_argument("--output", type=Path, help="Save suggestions to JSON file")

    args = parser.parse_args()

    renamer = SimplePythonRenamer(args.path)
    suggestions = renamer.analyze_project()

    if args.output:
        import json

        args.output.write_text(json.dumps(suggestions, indent=2))
        logger.info(f"📄 Saved suggestions to {args.output}")

    renamer.apply_renames(suggestions, auto_approve=args.apply)


if __name__ == "__main__":
    main()
