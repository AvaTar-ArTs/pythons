#!/usr/bin/env python3
"""
Reorganize by SERVICE instead of FILE TYPE

Moves files from generic folders (json/, file/, csv/) to service folders
based on what they ACTUALLY do (youtube/, instagram/, ai/, etc.)
"""

import ast
from pathlib import Path
import shutil


class ServiceReorganizer:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.moves = []

    def detect_service(self, file_path: Path) -> str:
        """Detect which service a script actually uses."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read(5000)  # First 5000 chars

            content_lower = content.lower()
            filename_lower = file_path.stem.lower()

            # Check filename first (most reliable)
            if any(x in filename_lower for x in ["youtube", "yt-", "ytube", "ytcsv"]):
                return "youtube"
            if any(x in filename_lower for x in ["instagram", "insta-", "ig-"]):
                return "instagram"
            if "leonardo" in filename_lower:
                return "leonardo"
            if any(x in filename_lower for x in ["reddit", "askreddit"]):
                return "reddit"
            if "telegram" in filename_lower or "tg-" in filename_lower:
                return "telegram"
            if "tiktok" in filename_lower:
                return "tiktok"
            if any(
                x in filename_lower
                for x in ["openai", "gpt-", "chatgpt", "claude", "anthropic"]
            ):
                return "ai"
            if any(
                x in filename_lower for x in ["audio", "mp3", "whisper", "transcrib"]
            ):
                return "audio"
            if any(x in filename_lower for x in ["video", "mp4", "ffmpeg"]):
                return "video"
            if any(
                x in filename_lower
                for x in ["dalle", "midjourney", "stable-diff", "stability"]
            ):
                return "image"

            # Check imports
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom):
                        mod = (node.module or "").lower()
                        if "pytube" in mod or "yt_dlp" in mod:
                            return "youtube"
                        if "instabot" in mod or "instaclient" in mod:
                            return "instagram"
                        if "openai" in mod:
                            return "ai"
                        if "anthropic" in mod:
                            return "ai"
                        if "leonardo" in mod:
                            return "leonardo"
                        if "praw" in mod:  # Reddit
                            return "reddit"
                        if "telegram" in mod or "telethon" in mod:
                            return "telegram"
            except Exception:
                pass

            # Check content
            if "youtube" in content_lower or "pytube" in content_lower:
                return "youtube"
            if "instagram" in content_lower or "instabot" in content_lower:
                return "instagram"

            # Generic data processing -> utils
            if any(
                x in filename_lower
                for x in ["analyze", "process", "reader", "writer", "batch"]
            ):
                return "utils"

            return "utils"  # Default fallback

        except Exception as e:
            return "utils"

    def reorganize(self, dry_run=True):
        """Reorganize files from generic folders to service folders."""
        print(f"\n{'='*80}")
        print("🔄 REORGANIZING BY SERVICE (NOT FILE TYPE)")
        print(f"{'='*80}\n")
        print(f"Mode: {'DRY RUN 👀' if dry_run else 'LIVE 🔥'}\n")

        generic_folders = ["json", "file", "csv"]

        for folder_name in generic_folders:
            folder = self.target_dir / folder_name
            if not folder.exists():
                continue

            print(f"\n📁 Processing {folder_name}/...")

            py_files = list(folder.glob("*.py"))

            for file_path in py_files:
                service = self.detect_service(file_path)
                target_folder = self.target_dir / service
                target_path = target_folder / file_path.name

                # Handle conflicts
                counter = 1
                orig_target = target_path
                while target_path.exists() and target_path != file_path:
                    target_path = target_folder / f"{file_path.stem}-{counter}.py"
                    counter += 1

                self.moves.append(
                    {
                        "file": file_path,
                        "from": folder_name,
                        "to": service,
                        "target": target_path,
                    }
                )

        # Group by target service
        by_service = {}
        for move in self.moves:
            service = move["to"]
            by_service.setdefault(service, []).append(move)

        # Show summary
        print(f"\n{'='*80}")
        print("📊 REORGANIZATION PLAN:")
        print(f"{'='*80}\n")

        for service, moves in sorted(by_service.items()):
            print(f"  → {service}/:  {len(moves)} files")

        print(f"\n  Total files to move: {len(self.moves)}")

        # Execute moves
        if not dry_run:
            print(f"\n🔥 EXECUTING MOVES...\n")

            for move in self.moves:
                target_folder = move["target"].parent
                target_folder.mkdir(exist_ok=True)

                try:
                    shutil.move(str(move["file"]), str(move["target"]))
                    print(f"  ✅ {move['file'].name} → {move['to']}/")
                except Exception as e:
                    print(f"  ❌ Error moving {move['file'].name}: {e}")

            # Remove empty folders
            for folder_name in generic_folders:
                folder = self.target_dir / folder_name
                if folder.exists():
                    py_files = list(folder.glob("*.py"))
                    if len(py_files) == 0:
                        import shutil

                        shutil.rmtree(folder)
                        print(f"\n  🗑️  Removed empty folder: {folder_name}/")

        print(f"\n{'='*80}")
        print(f"✅ {'DRY RUN COMPLETE' if dry_run else 'REORGANIZATION COMPLETE!'}")
        print("=" * 80 + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default=".")
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()

    reorganizer = ServiceReorganizer(args.target)
    reorganizer.reorganize(dry_run=not args.live)
