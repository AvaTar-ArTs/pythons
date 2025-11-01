#!/usr/bin/env python3
"""
Simple Flat Category Organizer

Creates simple category folders and moves all related scripts there.
NO subfolders - completely flat within each category.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class SimpleFlatOrganizer:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Folders to preserve (don't flatten)
        self.preserve_folders = {
            'scripts',
            '_data',
            '_docs',
            '_backups',
            '_reports',
            '_scripts',
            '_media'
        }

        # Simple categories
        self.categories = {
            'youtube': ['youtube', 'yt-', 'ytube', 'playlist', 'shorts', 'video'],
            'instagram': ['instagram', 'insta', 'igbot'],
            'tiktok': ['tiktok'],
            'reddit': ['reddit'],
            'twitter': ['twitter', 'tweet'],
            'telegram': ['telegram', 'tg-'],
            'facebook': ['facebook', 'fb-'],
            'twitch': ['twitch'],
            'ai': ['openai', 'gpt', 'claude', 'gemini', 'groq', 'xai', 'mistral', 'llm', 'ai-', 'anthropic', 'deepseek'],
            'leonardo': ['leonardo', 'leo-', 'leodown', 'leoup'],
            'dalle': ['dalle'],
            'image': ['image', 'img', 'photo', 'picture', 'upscale', 'resize'],
            'video': ['video', 'mp4', 'ffmpeg', 'moviepy'],
            'audio': ['audio', 'mp3', 'sound', 'music', 'whisper', 'transcribe', 'tts'],
            'scraper': ['scrape', 'spider', 'crawler'],
            'seo': ['seo', 'backlink'],
            'csv': ['csv'],
            'json': ['json'],
            'pdf': ['pdf'],
            'file': ['file-', 'folder-'],
            'analyze': ['analyze', 'analyzer', 'analysis'],
            'bot': ['bot-', 'botdraw', 'botstories'],
            'api': ['api-'],
            'etsy': ['etsy'],
            'redbubble': ['redbubble'],
            'quiz': ['quiz'],
            'suno': ['suno'],
            'backup': ['backup', 'rsync', 'migrate'],
            'utils': []  # Catch-all
        }

        # Folders to exclude from processing
        self.exclude_patterns = [
            '_ARCHIVED_BACKUPS',
            'dedup_backup',
            'bare_except_backup',
            'deep_rename_backup',
            'automated_fixes_backup',
            'merge_backup',
            '__pycache__',
            '.git',
            'node_modules',
            'myenv',
            'venv',
            'site-packages'
        ]

        self.stats = {'files_moved': 0, 'folders_removed': 0, 'errors': 0}

    def should_exclude(self, path: Path) -> bool:
        """Check if should exclude path."""
        return any(pattern in str(path) for pattern in self.exclude_patterns)

    def categorize_file(self, file_path: Path) -> str:
        """Determine category for a file."""
        name = file_path.name.lower()

        # Check filename keywords
        for category, keywords in self.categories.items():
            if category == 'utils':
                continue

            if any(keyword in name for keyword in keywords):
                return category

        # Try reading content (first 2000 chars)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(2000).lower()

            for category, keywords in self.categories.items():
                if category == 'utils':
                    continue

                if any(keyword in content for keyword in keywords):
                    return category
        except:
            pass

        return 'utils'

    def find_all_files(self):
        """Find all Python files to flatten."""
        print("\n🔍 Finding all Python files in subdirectories...\n")

        files_to_move = []

        for root, dirs, files in os.walk(self.target_dir):
            root_path = Path(root)

            # Skip excluded
            if self.should_exclude(root_path):
                dirs.clear()
                continue

            # Skip if in root
            if root_path == self.target_dir:
                continue

            # Skip preserved folders
            if root_path.name in self.preserve_folders:
                dirs.clear()
                continue

            # Collect Python files
            for file in files:
                if file.endswith('.py'):
                    files_to_move.append(root_path / file)

        return files_to_move

    def run(self, dry_run=True):
        """Run super flattening."""
        print(f"\n{'='*80}")
        print("🚀 SUPER FLAT ORGANIZER")
        print(f"{'='*80}\n")
        print(f"Target: {self.target_dir}")
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}\n")

        # Find all files
        files_to_move = self.find_all_files()
        print(f"✅ Found {len(files_to_move)} files to organize\n")

        # Categorize and count
        categorized = {}
        for category in self.categories.keys():
            categorized[category] = []

        for file_path in files_to_move:
            category = self.categorize_file(file_path)
            categorized[category].append(file_path)

        # Show summary
        print("📊 CATEGORIZATION:\n")
        for category, files in sorted(categorized.items(), key=lambda x: len(x[1]), reverse=True):
            if files:
                print(f"  {category}/: {len(files)} scripts")

        # Create category folders and move files
        print(f"\n{'='*80}")
        print(f"🚀 MOVING FILES - {'' if not dry_run else 'DRY RUN'}")
        print(f"{'='*80}\n")

        for category, files in categorized.items():
            if not files:
                continue

            category_dir = self.target_dir / category

            if not dry_run:
                category_dir.mkdir(exist_ok=True)

            print(f"\n📁 {category}/ ({len(files)} files)")

            for file_path in files:
                target = category_dir / file_path.name

                # Handle duplicates
                counter = 1
                original_target = target
                while target.exists():
                    stem = original_target.stem
                    ext = original_target.suffix
                    target = category_dir / f"{stem}-{counter}{ext}"
                    counter += 1

                if not dry_run:
                    try:
                        shutil.move(str(file_path), str(target))
                        self.stats['files_moved'] += 1
                    except Exception as e:
                        self.stats['errors'] += 1

                # Show sample
                if categorized[category].index(file_path) < 3:
                    print(f"  ✅ {file_path.name}")

            if len(files) > 3:
                print(f"  ... and {len(files) - 3} more")

        # Remove empty folders
        if not dry_run:
            print(f"\n🗑️ Removing empty folders...")
            self.remove_empty_folders()

        # Final summary
        print(f"\n{'='*80}")
        print("✅ COMPLETE!")
        print(f"{'='*80}\n")
        print(f"Files Organized: {len(files_to_move)}")
        if not dry_run:
            print(f"Files Moved: {self.stats['files_moved']}")
            print(f"Empty Folders Removed: {self.stats['folders_removed']}")
            if self.stats['errors'] > 0:
                print(f"Errors: {self.stats['errors']}")
        print()

    def remove_empty_folders(self):
        """Remove all empty folders."""
        # Bottom-up removal
        for root, dirs, files in os.walk(self.target_dir, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name

                # Skip preserved
                if dir_name in self.preserve_folders:
                    continue

                # Skip excluded
                if self.should_exclude(dir_path):
                    continue

                # Try to remove if empty
                try:
                    if not list(dir_path.iterdir()):
                        dir_path.rmdir()
                        self.stats['folders_removed'] = self.stats.get('folders_removed', 0) + 1
                except:
                    pass

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Simple Flat Organizer')
    parser.add_argument('--target', default='.', help='Target directory')
    parser.add_argument('--live', action='store_true', help='Execute flattening')

    args = parser.parse_args()

    organizer = SimpleFlatOrganizer(args.target)
    organizer.run(dry_run=not args.live)

if __name__ == "__main__":
    main()
