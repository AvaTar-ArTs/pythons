#!/usr/bin/env python3
"""
Rename by Purpose - What does the script DO?

Reads actual code to determine purpose, then names accordingly.
Pattern: [service]-[action]-[object]
"""

import ast
import re
import shutil
from pathlib import Path


class PurposeRenamer:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)

    def analyze_purpose(self, file_path: Path) -> dict:
        """Analyze what a script actually does."""
        try:
            content = file_path.read_text(encoding="utf-8")

            result = {"service": None, "action": None, "object": None}

            # Detect service from imports
            if "import openai" in content or "from openai" in content:
                result["service"] = "openai"
            elif "import anthropic" in content:
                result["service"] = "claude"
            elif "import instagram" in content or "instabot" in content:
                result["service"] = "instagram"
            elif "pytube" in content or "yt_dlp" in content:
                result["service"] = "youtube"
            elif "import leonardo" in content:
                result["service"] = "leonardo"
            elif "stability" in content.lower() and "api" in content:
                result["service"] = "stability"
            elif "elevenlabs" in content.lower():
                result["service"] = "elevenlabs"

            # Detect action from functions/code
            content_lower = content.lower()

            if "def download" in content_lower or "download(" in content_lower:
                result["action"] = "download"
            elif "def upload" in content_lower or "upload(" in content_lower:
                result["action"] = "upload"
            elif "def generate" in content_lower or "generate(" in content_lower:
                result["action"] = "generate"
            elif "def transcribe" in content_lower or "whisper" in content_lower:
                result["action"] = "transcribe"
            elif "def analyze" in content_lower or "analyze(" in content_lower:
                result["action"] = "analyze"
            elif "def convert" in content_lower or "convert(" in content_lower:
                result["action"] = "convert"
            elif "def scrape" in content_lower or "scrape(" in content_lower:
                result["action"] = "scrape"
            elif "def process" in content_lower:
                result["action"] = "process"
            elif "def cli" in content_lower or "argparse" in content:
                result["action"] = "cli"
            elif "def rerank" in content_lower or "reranking" in content_lower:
                result["action"] = "rerank"
            elif "def embed" in content_lower or "embedding" in content_lower:
                result["action"] = "embed"
            elif "def chat" in content_lower and "input" in content_lower:
                result["action"] = "chat"

            # Detect object from context
            if "video" in content_lower:
                result["object"] = "video"
            elif "audio" in content_lower or "mp3" in content_lower:
                result["object"] = "audio"
            elif "image" in content_lower or "photo" in content_lower:
                result["object"] = "image"
            elif "csv" in content_lower:
                result["object"] = "csv"
            elif "json" in content_lower:
                result["object"] = "json"
            elif "pdf" in content_lower:
                result["object"] = "pdf"
            elif "rag" in content_lower:
                result["object"] = "rag"
            elif "doc" in content_lower and "string" in content_lower:
                result["object"] = "docs"

            return result

        except:
            return {"service": None, "action": None, "object": None}

    def create_name(self, analysis: dict, current_name: str) -> str:
        """Create clean name from analysis."""
        parts = []

        if analysis["service"]:
            parts.append(analysis["service"])

        if analysis["action"]:
            parts.append(analysis["action"])

        if analysis["object"]:
            parts.append(analysis["object"])

        if len(parts) >= 2:
            return "-".join(parts)
        else:
            # Not enough info, keep simplified version of current name
            # Remove generic words
            clean = current_name
            clean = re.sub(r"_\d+$", "", clean)  # Remove trailing numbers
            clean = re.sub(r"-v\d+$", "", clean)  # Remove versions
            clean = clean.replace("utilities-misc-", "")
            clean = clean.replace("data-processing-", "")
            clean = clean.replace("file-management-", "")
            return clean

    def rename_all(self, dry_run=True):
        """Rename all files by purpose."""
        print(f"\n{'='*80}")
        print("🎯 RENAMING BY PURPOSE - WHAT DO SCRIPTS DO?")
        print(f"{'='*80}\n")
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}\n")

        py_files = list(self.target_dir.glob("*.py"))

        renamed = 0

        for f in py_files:
            analysis = self.analyze_purpose(f)
            suggested = self.create_name(analysis, f.stem)

            if suggested and suggested != f.stem:
                new_path = self.target_dir / f"{suggested}.py"

                # Handle conflicts
                counter = 1
                while new_path.exists() and new_path != f:
                    new_path = self.target_dir / f"{suggested}-{counter}.py"
                    counter += 1

                if renamed < 30:
                    action_str = f"{analysis['service'] or '?'}-{analysis['action'] or '?'}-{analysis['object'] or '?'}"
                    print(f"  {f.name[:40]:40}")
                    print(f"  → {new_path.name[:40]:40} [{action_str}]")
                    print()

                if not dry_run:
                    try:
                        shutil.move(str(f), str(new_path))
                    except:
                        pass

                renamed += 1

        if renamed > 30:
            print(f"  ... and {renamed - 30} more")

        print(f"\n{'='*80}")
        print(f"{'Would rename' if dry_run else 'Renamed'} {renamed} files")
        print("=" * 80 + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default=".")
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()

    renamer = PurposeRenamer(args.target)
    renamer.rename_all(dry_run=not args.live)
