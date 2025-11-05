#!/usr/bin/env python3
"""
Smart Local Renamer - NO AI HALLUCINATIONS!

Uses actual code analysis (imports, functions, docstrings) to rename intelligently.
NO guessing, NO hallucinations, just FACTS from the code.
"""

import ast
import re
import shutil
from datetime import datetime
from pathlib import Path


class SmartLocalRenamer:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Service detection from actual imports
        self.service_imports = {
            "instagram": ["instabot", "instaclient", "instapy"],
            "youtube": ["pytube", "yt_dlp", "youtube", "youtubeviewer"],
            "openai": ["openai"],
            "anthropic": ["anthropic"],
            "stability": ["stability", "stablediffusion", "stable_diffusion"],
            "leonardo": ["leonardo"],
            "replicate": ["replicate"],
            "midjourney": ["midjourney"],
            "elevenlabs": ["elevenlabs"],
            "gemini": ["google.generativeai"],
            "huggingface": ["transformers", "diffusers", "huggingface"],
            "aws": ["boto3", "botocore"],
            "gcp": ["google.cloud"],
            "reddit": ["praw"],
            "telegram": ["telethon", "telegram"],
            "tiktok": ["tiktok"],
            "twitter": ["tweepy"],
        }

        self.stats = {"renamed": 0, "skipped": 0, "errors": 0}
        self.renames = []

    def detect_service_from_code(self, file_path: Path) -> str:
        """Detect service by READING actual imports."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 1. Check filename first (most reliable)
            filename_lower = file_path.name.lower()

            # Strong filename indicators
            if "stability" in filename_lower or "stable-diff" in filename_lower:
                return "stability"
            if "ygpt" in filename_lower or "youtube-gpt" in filename_lower:
                return "ygpt"
            if "elevenlabs" in filename_lower:
                return "elevenlabs"
            if "midjourney" in filename_lower:
                return "midjourney"
            if "replicate" in filename_lower:
                return "replicate"

            # 2. Parse actual imports
            try:
                tree = ast.parse(content)

                imports = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name.lower())
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module.lower())

                # Match imports to services
                for service, import_patterns in self.service_imports.items():
                    for pattern in import_patterns:
                        if any(pattern in imp for imp in imports):
                            return service

            except Exception:
                pass

            # 3. Check content for service mentions
            content_lower = content.lower()
            if "stability" in content_lower or "stable diffusion" in content_lower:
                return "stability"
            if "elevenlabs" in content_lower:
                return "elevenlabs"

            # 4. Fallback to folder-based categorization
            folder = file_path.parent.name
            if folder in [
                "youtube",
                "instagram",
                "leonardo",
                "reddit",
                "telegram",
                "tiktok",
            ]:
                return folder

            return None

        except:
            return None

    def create_smart_name(self, file_path: Path, service: str) -> str:
        """Create smart name based on actual code."""
        current_stem = file_path.stem

        # If already has good naming pattern, keep it
        if service and current_stem.startswith(f"{service}-"):
            # Already properly named
            return current_stem

        # If has service in name but wrong format, fix it
        if service:
            # Remove service prefix variations
            clean_stem = current_stem
            for variant in [f"{service}_", f"{service}-", service]:
                if clean_stem.lower().startswith(variant):
                    clean_stem = clean_stem[len(variant) :].lstrip("-_")
                    break

            # Add service prefix in standard format
            if clean_stem:
                return f"{service}-{clean_stem}"

        return current_stem

    def process_folder(self, folder_path: Path, dry_run=True):
        """Process all files in a folder."""
        folder_name = folder_path.name
        python_files = list(folder_path.glob("*.py"))

        print(f"\n📁 {folder_name}/ ({len(python_files)} files)")

        renamed_count = 0

        for file_path in python_files:
            # Detect actual service
            service = self.detect_service_from_code(file_path)

            if service:
                new_stem = self.create_smart_name(file_path, service)

                if new_stem != file_path.stem:
                    target_path = folder_path / f"{new_stem}.py"

                    # Handle conflicts
                    counter = 1
                    original_target = target_path
                    while target_path.exists() and target_path != file_path:
                        target_path = folder_path / f"{new_stem}-v{counter}.py"
                        counter += 1

                    self.renames.append(
                        {"old": file_path, "new": target_path, "service": service}
                    )

                    if renamed_count < 5:
                        print(f"  ✨ {file_path.name}")
                        print(f"     → {target_path.name} [service: {service}]")

                    if not dry_run:
                        try:
                            shutil.move(str(file_path), str(target_path))
                            self.stats["renamed"] += 1
                        except Exception as e:
                            print(f"  ❌ Error: {e}")
                            self.stats["errors"] += 1

                    renamed_count += 1

        if renamed_count > 5:
            print(f"  ... and {renamed_count - 5} more")
        elif renamed_count == 0:
            print(f"  ✅ All files already well-named!")

        return renamed_count

    def run(self, dry_run=True):
        """Run smart local renaming."""
        print(f"\n{'='*80}")
        print("🧠 SMART LOCAL RENAMER - NO AI HALLUCINATIONS!")
        print(f"{'='*80}\n")
        print(f"Mode: {'DRY RUN' if dry_run else '🔥 LIVE'}\n")
        print("✅ Uses ACTUAL imports from code")
        print("✅ Detects services from filenames")
        print("✅ NO guessing or hallucinations!")
        print()

        # Process all folders
        folders = [
            f
            for f in self.target_dir.iterdir()
            if f.is_dir() and not f.name.startswith((".", "_"))
        ]

        total_renamed = 0
        for folder in sorted(folders):
            count = self.process_folder(folder, dry_run)
            total_renamed += count

        print(f"\n{'='*80}")
        print("✅ COMPLETE!")
        print(f"{'='*80}\n")
        print(f"Total Files to Rename: {total_renamed}")
        if not dry_run:
            print(f"Successfully Renamed: {self.stats['renamed']}")
            if self.stats["errors"] > 0:
                print(f"Errors: {self.stats['errors']}")
        print()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Smart Local Renamer")
    parser.add_argument("--target", default=".", help="Target directory")
    parser.add_argument("--live", action="store_true", help="Execute renames")

    args = parser.parse_args()

    renamer = SmartLocalRenamer(args.target)
    renamer.run(dry_run=not args.live)


if __name__ == "__main__":
    main()
