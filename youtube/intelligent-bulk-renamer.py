"""
Intelligent Bulk Renamer

This module provides functionality for intelligent bulk renamer.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100

#!/usr/bin/env python3
"""
Intelligent Bulk File Renamer
Analyzes Python files and suggests content-aware names based on:
- Docstrings
- Comments
- Import patterns
- Code structure
- File content

Usage:
    python intelligent_bulk_renamer.py --pattern "script_*.py" --output renames.csv --dry-run
    python intelligent_bulk_renamer.py --pattern "main_*.py" --output renames.csv --apply
"""

import ast
import re
import csv
import argparse
from pathlib import Path
from collections import Counter
import hashlib

# Key patterns to detect functionality
PATTERNS = {
    "openai_chat": ["openai", "chat.completions", "gpt-"],
    "openai_whisper": ["whisper", "transcribe", "audio.transcriptions"],
    "openai_tts": ["audio.speech", "tts-", "text-to-speech"],
    "openai_vision": ["gpt-4o", "gpt-4-vision", "image_url"],
    "youtube": ["youtube", "yt-dlp", "pytube"],
    "instagram": ["instabot", "instagram", "instaloader"],
    "tiktok": ["tiktok", "tiktokapipy"],
    "reddit": ["praw", "reddit", "subreddit"],
    "twitter": ["tweepy", "twitter"],
    "image_processing": ["PIL", "Pillow", "opencv", "cv2"],
    "video_processing": ["moviepy", "ffmpeg", "VideoFileClip"],
    "web_scraping": ["beautifulsoup", "bs4", "selenium"],
    "csv_processing": ["csv.", "pandas", "DataFrame"],
    "html_generation": ["<!DOCTYPE", "<html", "html_content"],
    "upscaling": ["upscale", "sips", "resize"],
    "transcription": ["transcribe", "transcript", "whisper"],
    "database": ["sqlite3", "mysql", "pymongo", "sqlalchemy"],
    "api_client": ["requests.", "api_key", "headers ="],
}


def extract_docstring(content):
    """Extract module docstring"""
    try:
        tree = ast.parse(content)
        return ast.get_docstring(tree)
    except Exception:
        return None


def extract_first_comment(content):
    """Extract first meaningful comment"""
    for line in content.split("\n")[:30]:
        stripped = line.strip()
        if stripped.startswith("#") and len(stripped) > 10:
            comment = stripped.lstrip("#").strip()
            if not comment.startswith(("!", "-", "=", "*")):
                return comment
    return None


def extract_imports(content):
    """Extract import statements"""
    imports = []
    for line in content.split("\n")[:CONSTANT_100]:
        stripped = line.strip()
        if stripped.startswith(("import ", "from ")):
            imports.append(stripped)
    return imports


def detect_patterns(content):
    """Detect functionality patterns in code"""
    content_lower = content.lower()
    detected = []
    for pattern_name, keywords in PATTERNS.items():
        if any(kw.lower() in content_lower for kw in keywords):
            detected.append(pattern_name)
    return detected


def extract_main_function_name(content):
    """Try to find meaningful function names"""
    try:
        tree = ast.parse(content)
        func_names = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                name = node.name
                if not name.startswith("_") and name not in ["main", "run", "execute"]:
                    func_names.append(name)
        return func_names[:3]
    except (IndexError, KeyError):
        return []


def suggest_name(filepath, analysis):
    """Suggest a descriptive name based on analysis"""

    # Priority 1: Use docstring if descriptive
    if analysis.get("docstring"):
        doc = analysis["docstring"]
        # Extract first sentence
        first_sentence = doc.split(".")[0].split("\n")[0].strip()
        if len(first_sentence) > 15 and len(first_sentence) < 80:
            # Convert to snake_case
            name = re.sub(r"[^\w\s-]", "", first_sentence.lower())
            name = re.sub(r"[-\s]+", "_", name)
            if len(name) > 10:
                return name[:50] + ".py"

    # Priority 2: Use first comment
    if analysis.get("first_comment"):
        comment = analysis["first_comment"]
        if len(comment) > 15 and len(comment) < 80:
            name = re.sub(r"[^\w\s-]", "", comment.lower())
            name = re.sub(r"[-\s]+", "_", name)
            if len(name) > 10:
                return name[:50] + ".py"

    # Priority 3: Infer from patterns
    patterns = analysis.get("patterns", [])
    if patterns:
        # Combine top 2-3 patterns
        pattern_str = "_".join(patterns[:2])
        return f"{pattern_str}_tool.py"

    # Priority 4: Use function names
    func_names = analysis.get("func_names", [])
    if func_names:
        return f"{func_names[0]}_script.py"

    # Fallback: Keep original
    return None


def analyze_file(filepath):
    """Comprehensive file analysis"""
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")

        analysis = {
            "docstring": extract_docstring(content),
            "first_comment": extract_first_comment(content),
            "imports": extract_imports(content),
            "patterns": detect_patterns(content),
            "func_names": extract_main_function_name(content),
            "size": len(content),
            "lines": content.count("\n"),
            "hash": hashlib.sha256(content.encode()).hexdigest()[:16],
        }

        suggested_name = suggest_name(filepath, analysis)
        analysis["suggested_name"] = suggested_name

        return analysis
    except Exception as e:
        return {"error": str(e)}


def main():
    """main function."""

    parser = argparse.ArgumentParser(description="Intelligent bulk file renamer")
    parser.add_argument("--pattern", required=True, help='Glob pattern (e.g., "script_*.py")')
    parser.add_argument("--output", default="rename_plan.csv", help="Output CSV file")
    parser.add_argument("--dry-run", action="store_true", help="Generate plan without applying")
    parser.add_argument("--apply", action="store_true", help="Apply renames from CSV")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of files to process")

    args = parser.parse_args()

    root = Path("/Users/steven/Documents/python")
    files = sorted(root.glob(args.pattern))

    if args.limit:
        files = files[: args.limit]

    logger.info(f"?? Analyzing {len(files)} files matching '{args.pattern}'...")
    print()

    results = []
    for i, filepath in enumerate(files, 1):
        if i % 50 == 0:
            logger.info(f"  Progress: {i}/{len(files)}...")

        analysis = analyze_file(filepath)

        results.append(
            {
                "original": filepath.name,
                "suggested": analysis.get("suggested_name", ""),
                "docstring": (analysis.get("docstring", "")[:CONSTANT_100] if analysis.get("docstring") else ""),
                "comment": analysis.get("first_comment", "")[:CONSTANT_100] if analysis.get("first_comment") else "",
                "patterns": ",".join(analysis.get("patterns", [])),
                "lines": analysis.get("lines", 0),
                "hash": analysis.get("hash", ""),
            }
        )

    # Write CSV
    output_path = root / args.output
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["original", "suggested", "docstring", "comment", "patterns", "lines", "hash"]
        )
        writer.writeheader()
        writer.writerows(results)

    logger.info(f"\n? Analysis complete!")
    logger.info(f"?? Results saved to: {output_path}")
    logger.info(f"\n?? Summary:")
    logger.info(f"   Total analyzed: {len(results)}")
    suggestions = sum(1 for r in results if r["suggested"])
    logger.info(f"   Suggestions generated: {suggestions} ({suggestions/len(results)*CONSTANT_100:.1f}%)")
    logger.info(f"   Needs manual review: {len(results) - suggestions}")

    if args.apply:
        logger.info("\n??  --apply not yet implemented. Review CSV first, then use master-rename-utility.py")


if __name__ == "__main__":
    main()
