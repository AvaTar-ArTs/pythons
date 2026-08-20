#!/usr/bin/env python3
"""
Deep Content-Aware File Renamer
Reads entire file content to generate VERY SPECIFIC names
Based on the advanced yt_deep_content_renamer.py
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import Counter
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class DeepContentRenamer:
    """Deep analysis of file content to suggest specific, descriptive names"""

    def analyze_file_deeply(self, filepath: Path) -> Dict:
        """Deep content analysis - read everything"""
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
                "suggested_name": None,
            }

            # Parse AST for structure
            try:
                tree = ast.parse(content)

                # Get module docstring
                if (
                    tree.body
                    and isinstance(tree.body[0], ast.Expr)
                    and isinstance(tree.body[0].value, ast.Constant)
                ):
                    analysis["docstring"] = tree.body[0].value.value

                # Collect all imports
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

                # Identify main imports (most significant ones)
                significant_imports = []
                for imp in analysis["imports"]:
                    base = imp.split(".")[0]
                    # Skip standard library
                    if base not in [
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
                    ]:
                        significant_imports.append(base)

                analysis["main_imports"] = list(set(significant_imports))[:5]

                # Identify main functions (not test_, not __)
                main_funcs = [
                    f
                    for f in analysis["functions"]
                    if not f.startswith("test_") and not f.startswith("_")
                ]
                analysis["main_functions"] = main_funcs[:5]

            except Exception as e:
                logger.debug(f"AST parse error for {filepath}: {e}")

            # Extract action verbs from function names and content
            verbs = self._extract_verbs(analysis["functions"], content)
            analysis["main_verbs"] = verbs[:3]

            # Extract nouns (what it operates on)
            nouns = self._extract_nouns(content, analysis["main_imports"])
            analysis["main_nouns"] = nouns[:3]

            # Detect API services
            analysis["api_services"] = self._detect_api_services(
                content, analysis["imports"]
            )

            # Detect file operations
            analysis["file_operations"] = self._detect_file_operations(content)

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing {filepath}: {e}")
            return {}

    def _extract_verbs(self, functions: List[str], content: str) -> List[str]:
        """Extract action verbs from function names"""
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

        return found_verbs

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
                    if count >= 3:  # Must appear at least 3 times
                        found_nouns.append(noun)
                        break

        return list(set(found_nouns))

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

        if "upload" in content.lower():
            ops.append("upload")
        if "download" in content.lower():
            ops.append("download")
        if "compress" in content.lower():
            ops.append("compress")
        if "convert" in content.lower() or "transform" in content.lower():
            ops.append("convert")
        if "parse" in content.lower():
            ops.append("parse")
        if "generate" in content.lower() or "create" in content.lower():
            ops.append("generate")

        return ops

    def suggest_specific_name(self, filepath: Path, analysis: Dict) -> Optional[str]:
        """Generate concise, specific name based on deep analysis"""

        # Don't rename if already well-named (specific enough)
        current_name = filepath.stem

        # Skip if it's already specific
        if (
            len(current_name) > 15
            and "_" in current_name
            and not any(
                bad in current_name.lower()
                for bad in ["copy", "old", "new", "temp", "1", "2", "3"]
            )
        ):
            return None

        # Abbreviations for common terms
        abbreviations = {
            "youtube": "yt",
            "video": "vid",
            "image": "img",
            "audio": "aud",
            "database": "db",
            "gallery": "gal",
            "thumbnail": "thumb",
            "generate": "gen",
            "process": "proc",
            "analyze": "analyze",  # keep this one
            "transcribe": "transcribe",  # keep this one
        }

        # Build concise name (max 2-3 parts)
        name_parts = []

        # Strategy: action_subject or subject_action pattern
        main_action = None
        main_subject = None

        # Get primary action
        if analysis["main_verbs"]:
            action = analysis["main_verbs"][0]
            main_action = abbreviations.get(action, action)

        # Get primary subject (what it works with)
        if analysis["main_nouns"]:
            subject = analysis["main_nouns"][0]
            main_subject = abbreviations.get(subject, subject)

        # Special handling for specific combinations
        # For downloads: {platform}_download or download_{thing}
        if main_action in ["download", "fetch", "get", "retrieve"]:
            if "youtube" in analysis["api_services"]:
                return "yt_video_downloader.py"
            elif "instagram" in analysis["api_services"]:
                return "ig_downloader.py"
            elif main_subject:
                name_parts = [main_action, main_subject]

        # For uploads: upload_{platform} or {thing}_uploader
        elif main_action in ["upload", "post", "send"]:
            if main_subject:
                name_parts = [main_action, main_subject]
            else:
                name_parts = [main_action]

        # For transcription: {format}_transcribe
        elif main_action == "transcribe":
            if "audio" in analysis["main_nouns"] or "video" in analysis["main_nouns"]:
                fmt = (
                    "mp4"
                    if "video" in analysis["main_nouns"]
                    or "mp4" in str(filepath).lower()
                    else "mp3"
                )
                return f"{fmt}_transcribe.py"
            else:
                return "transcribe.py"

        # For generation: gen_{what} or generate_{what}
        elif main_action in ["generate", "create", "make", "build"]:
            if main_subject:
                subject_abbr = abbreviations.get(main_subject, main_subject)
                name_parts = ["gen", subject_abbr]
            elif "video" in analysis["main_nouns"] and "text" in analysis["main_nouns"]:
                return "gen_vid_text.py"

        # For upscaling: upscale_{what}
        elif main_action in ["upscale", "enhance", "resize"]:
            if main_subject:
                name_parts = [
                    main_action,
                    abbreviations.get(main_subject, main_subject),
                ]
            else:
                name_parts = [main_action]

        # For analysis: analyze_{what}
        elif main_action in ["analyze", "parse", "process"]:
            if main_subject:
                name_parts = [
                    main_action,
                    abbreviations.get(main_subject, main_subject),
                ]

        # Default: action_subject
        else:
            if main_action and main_subject:
                name_parts = [
                    main_action,
                    abbreviations.get(main_subject, main_subject),
                ]
            elif main_action:
                name_parts = [main_action]
            elif main_subject:
                name_parts = [abbreviations.get(main_subject, main_subject)]

        if not name_parts:
            return None

        # Keep it concise - max 2 parts usually
        name_parts = name_parts[:2]

        # Build final name
        new_name = "_".join(name_parts) + ".py"

        # Check if different from current
        if new_name == filepath.name:
            return None

        # Check if target exists
        target = filepath.parent / new_name
        if target.exists() and target != filepath:
            # Add counter
            counter = 2
            while (filepath.parent / f"{new_name[:-3]}_{counter}.py").exists():
                counter += 1
            new_name = f"{new_name[:-3]}_{counter}.py"

        return new_name

    def analyze_and_rename(self, project_root: Path, apply: bool = False):
        """Analyze all files and suggest renames"""
        logger.info("🔍 Deep content analysis for specific renaming...\n")

        python_files = list(project_root.rglob("*.py"))
        suggestions = []

        for filepath in python_files:
            # Skip hidden and system files
            if any(part.startswith(".") for part in filepath.parts):
                continue

            # Skip well-named files
            if not any(
                bad in filepath.name.lower()
                for bad in [
                    "copy",
                    "old",
                    "new",
                    "temp",
                    "_1",
                    "_2",
                    "_3",
                    "_4",
                    " 1",
                    " 2",
                    " 3",
                    " 4",
                    "untitled",
                ]
            ):
                continue

            # Deep analysis
            analysis = self.analyze_file_deeply(filepath)

            # Generate specific name
            new_name = self.suggest_specific_name(filepath, analysis)

            if new_name:
                suggestions.append(
                    {
                        "current": str(filepath),
                        "current_name": filepath.name,
                        "new_name": new_name,
                        "verbs": analysis["main_verbs"],
                        "nouns": analysis["main_nouns"],
                        "apis": analysis["api_services"],
                        "imports": analysis["main_imports"][:3],
                    }
                )

        # Display suggestions
        logger.info(f"📝 Found {len(suggestions)} files to rename:\n")

        for i, sug in enumerate(suggestions, 1):
            logger.info(f"{i:3d}. {sug['current_name']}")
            logger.info(f"     → {sug['new_name']}")
            logger.info(f"     Actions: {', '.join(sug['verbs'][:2])}")
            logger.info(f"     Operates on: {', '.join(sug['nouns'][:2])}")
            if sug["apis"]:
                logger.info(f"     APIs: {', '.join(sug['apis'][:2])}")
            logger.info("")

        if apply:
            logger.info("Applying renames...\n")
            applied = 0
            for sug in suggestions:
                try:
                    current = Path(sug["current"])
                    new_path = current.parent / sug["new_name"]

                    # Check if git tracked
                    result = subprocess.run(
                        ["git", "ls-files", "--error-unmatch", str(current)],
                        capture_output=True,
                    )
                    is_tracked = result.returncode == 0

                    if is_tracked:
                        subprocess.run(
                            ["git", "mv", str(current), str(new_path)], check=True
                        )
                        logger.info(f"✅ {sug['current_name']} → {sug['new_name']}")
                    else:
                        current.rename(new_path)
                        logger.info(f"✅ {sug['current_name']} → {sug['new_name']}")

                    applied += 1
                except Exception as e:
                    logger.error(f"❌ Error renaming {sug['current_name']}: {e}")

            logger.info(f"\n✅ Successfully renamed {applied}/{len(suggestions)} files")
        else:
            logger.info("💡 Run with --apply to execute renames")


def main():
    """main function."""

    import argparse

    parser = argparse.ArgumentParser(description="Deep content-aware file renamer")
    parser.add_argument("path", type=Path, nargs="?", default=Path.cwd())
    parser.add_argument("--apply", action="store_true", help="Apply renames")

    args = parser.parse_args()

    renamer = DeepContentRenamer()
    renamer.analyze_and_rename(args.path, apply=args.apply)


if __name__ == "__main__":
    main()
