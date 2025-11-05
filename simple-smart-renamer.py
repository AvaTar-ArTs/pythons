#!/usr/bin/env python3
"""
Simple Smart Renamer - NO AI, Just Logic!

Rules:
1. If filename has service (stability, mistral, ygpt) → KEEP IT!
2. Read actual imports to detect service
3. Simple cleanup: remove numbers, fix formatting
4. Pattern: [service]-[what-it-does]
"""

import ast
import re
from pathlib import Path
import shutil


class SimpleSmartRenamer:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.stats = {"renamed": 0}

    def detect_service(self, file_path: Path) -> str:
        """Simple service detection."""
        filename = file_path.stem.lower()

        # 1. Check filename first (most reliable!)
        services = {
            "instagram": ["instagram", "insta-", "igbot"],
            "youtube": ["youtube", "yt-", "ytube"],
            "stability": ["stability", "stable-diff", "stablediff"],
            "leonardo": ["leonardo", "leo-"],
            "openai": ["openai", "gpt-", "chatgpt"],
            "mistral": ["mistral"],
            "gemini": ["gemini"],
            "claude": ["claude", "anthropic"],
            "elevenlabs": ["elevenlabs", "eleven"],
            "ygpt": ["ygpt"],
            "replicate": ["replicate"],
            "midjourney": ["midjourney"],
            "reddit": ["reddit"],
            "telegram": ["telegram", "tg-"],
            "tiktok": ["tiktok"],
        }

        for service, patterns in services.items():
            if any(p in filename for p in patterns):
                return service

        # 2. Check imports
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read(5000)  # First 5000 chars

            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    mod = (node.module or "").lower()
                    if "instabot" in mod or "instaclient" in mod:
                        return "instagram"
                    if "pytube" in mod or "yt_dlp" in mod:
                        return "youtube"
                    if "openai" in mod:
                        return "openai"
                    if "anthropic" in mod:
                        return "claude"
        except Exception:
            pass

        return None

    def simplify_name(self, filename: str, service: str) -> str:
        """Simplify filename keeping service prefix."""
        stem = filename.replace(".py", "")

        # Already has service prefix in good format?
        if stem.startswith(f"{service}-"):
            return stem

        # Remove service prefix variations and re-add cleanly
        for prefix in [f"{service}_", f"{service}-", service]:
            if stem.lower().startswith(prefix.lower()):
                rest = stem[len(prefix) :].lstrip("-_")
                return f"{service}-{rest}" if rest else service

        # Add service prefix
        return f"{service}-{stem}"

    def clean_filename(self, filename: str) -> str:
        """Clean up filename formatting."""
        # Remove version numbers at end like _v1, _1, -1
        filename = re.sub(r"[-_]v?\d+$", "", filename)

        # Fix double separators
        filename = re.sub(r"[-_]{2,}", "-", filename)

        # Convert underscores to hyphens for consistency
        filename = filename.replace("_", "-")

        return filename

    def process_all(self, dry_run=True):
        """Process all folders."""
        print(f"\n{'='*80}")
        print("🎯 SIMPLE SMART RENAMER")
        print(f"{'='*80}\n")
        print(f"Mode: {'DRY RUN 👀' if dry_run else 'LIVE 🔥'}\n")

        folders = sorted(
            [
                f
                for f in self.target_dir.iterdir()
                if f.is_dir() and not f.name.startswith((".", "_"))
            ]
        )

        for folder in folders:
            py_files = list(folder.glob("*.py"))
            if not py_files:
                continue

            print(f"\n📁 {folder.name}/ ({len(py_files)} files)")
            renamed = 0

            for file_path in py_files:
                service = self.detect_service(file_path)

                if service:
                    # Simplify and add service prefix
                    new_stem = self.simplify_name(file_path.stem, service)
                    new_stem = self.clean_filename(new_stem)

                    if new_stem != file_path.stem:
                        target = folder / f"{new_stem}.py"

                        # Handle conflicts
                        counter = 1
                        orig = target
                        while target.exists() and target != file_path:
                            target = folder / f"{new_stem}-{counter}.py"
                            counter += 1

                        if renamed < 3:
                            print(f"  ✨ {file_path.name}")
                            print(f"     → {target.name}")

                        if not dry_run:
                            try:
                                shutil.move(str(file_path), str(target))
                                self.stats["renamed"] += 1
                            except Exception as e:
                                print(f"  ❌ {e}")

                        renamed += 1

            if renamed > 3:
                print(f"  ... and {renamed - 3} more")
            elif renamed == 0:
                print(f"  ✅ All good!")

        print(f"\n{'='*80}")
        print(
            f"✅ Total renamed: {self.stats['renamed'] if not dry_run else 'DRY RUN'}"
        )
        print(f"{'='*80}\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default=".")
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()

    renamer = SimpleSmartRenamer(args.target)
    renamer.process_all(dry_run=not args.live)
