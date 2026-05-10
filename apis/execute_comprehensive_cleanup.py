#!/usr/bin/env python3
"""
Comprehensive Cleanup and Consolidation
1. Archive terrible (meaningless) directories
2. Consolidate redundant directory groups
3. Organize loose root files
"""

import shutil
from pathlib import Path


class ComprehensiveCleanup:
    """Execute comprehensive directory cleanup"""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.archive_dir = base_dir / "_archived_cleanup"
        self.loose_files_dir = base_dir / "_organized_root_files"

        # Consolidation mappings
        self.consolidations = {
            "video-downloader": [
                "youtube-downloader",
                "tiktok-video-downloader",
                "Auto-YouTube",
                "youtube-python",
                "scrape-youtube-channel-videos-url",
            ],
            "video-generator": [
                "videoGenerator",
                "Automatic-Video-Generator-for-youtube",
                "reddit_video_maker",
                "RedditVideoMakerBot-master",
                "redditVideoGenerator",
                "TikTok-Compilation-Video-Generator",
                "tiktok-generator",
            ],
            "bot-automation": [
                "instagram-follower-scraper",
                "InstagramReportBot",
                "InstaReport",
                "Instagram-Mass-report",
                "botty",
                "FB-Script-Auto-Post-All-Group",
            ],
            "gallery-generator": [
                "simplegallery",
                "simplegallery-bin",
                "netlify-gallery-deployer",
            ],
            "web-scraper": [
                "web-scraping",
                "web_scraping",
                "selenium-image-scraper",
                "fiverr-scraping-api",
            ],
            "transcribe-analysis": ["transcription_analyzer", "audio-transcriber"],
            "upscaler": ["upscale-python"],
            "file-organizer": ["Python-organize", "clean-organizer"],
            "backup-tool": ["archive-utility"],
            "thumbnail-generator": ["thumbnail-creator"],
            "ai-text-generator": ["Python-and-OpenAI-main"],
            "ai-image-generator": ["ai-comic-factory"],
            "seo-optimizer": [
                "SEO-Link-Building-Rank-in-Google-with-EDU-and-GOV-Backlinks"
            ],
        }

        # Terrible directories to archive
        self.terrible_dirs = [
            "af",
            "b2",
            "b6",
            "b8",
            "ba",
            "bb",
            "bd",
            "bf",
            "c2",
            "c4",
            "c7",
            "c8",
            "cb",
            "d0",
            "d5",
            "d6",
            "d8",
            "dd",
            "e0",
            "e2",
            "e6",
            "e7",
            "e9",
            "ea",
            "f1",
            "f2",
            "f3",
            "f6",
            "f7",
            "f8",
            "f9",
            "fb",
            "fc",
            "fd",
            "fe",
        ]

    def archive_terrible_directories(self, dry_run=True):
        """Archive meaningless 2-character directories"""

        print("🗑️  Archiving Terrible Directories...")
        print()

        archived = 0
        skipped = 0

        for dir_name in self.terrible_dirs:
            dir_path = self.base_dir / dir_name

            if not dir_path.exists():
                skipped += 1
                continue

            # Check if empty or has files
            has_content = any(dir_path.iterdir())

            if dry_run:
                status = "HAS CONTENT" if has_content else "EMPTY"
                print(f"   [DRY RUN] Would archive: {dir_name:<10} ({status})")
            else:
                self.archive_dir.mkdir(exist_ok=True)
                dest = self.archive_dir / dir_name
                shutil.move(str(dir_path), str(dest))
                print(f"   ✅ Archived: {dir_name}")

            archived += 1

        print(
            f"\n   Total: {archived} directories {'would be' if dry_run else ''} archived"
        )
        print(f"   Skipped: {skipped} (not found)")
        print()

    def consolidate_redundant_groups(self, dry_run=True):
        """Consolidate redundant directory groups"""

        print("🔄 Consolidating Redundant Directory Groups...")
        print()

        total_consolidated = 0

        for target_dir, source_dirs in self.consolidations.items():
            target_path = self.base_dir / target_dir

            # Check which source directories actually exist
            existing_sources = [d for d in source_dirs if (self.base_dir / d).exists()]

            if not existing_sources:
                continue

            print(f"📁 {target_dir}/ ← {len(existing_sources)} directories")

            if not dry_run and not target_path.exists():
                target_path.mkdir(parents=True)

            for source_dir in existing_sources:
                source_path = self.base_dir / source_dir

                if dry_run:
                    file_count = len(list(source_path.rglob("*")))
                    print(
                        f"   [DRY RUN] Would merge: {source_dir} ({file_count} items)"
                    )
                else:
                    # Move all contents to target
                    for item in source_path.iterdir():
                        dest = target_path / item.name
                        if not dest.exists():
                            shutil.move(str(item), str(dest))
                        else:
                            # Handle conflict
                            new_name = f"{item.stem}_from_{source_dir}{item.suffix}"
                            shutil.move(str(item), str(target_path / new_name))

                    # Remove empty source directory
                    try:
                        source_path.rmdir()
                        print(f"   ✅ Merged and removed: {source_dir}")
                    except:
                        print(f"   ⚠️  Merged (dir not empty): {source_dir}")

                total_consolidated += 1

            print()

        print(
            f"   Total: {total_consolidated} directories {'would be' if dry_run else ''} consolidated"
        )
        print()

    def organize_loose_files(self, dry_run=True):
        """Organize loose files in root by type"""

        print("📄 Organizing Loose Root Files...")
        print()

        # File type mappings
        type_mappings = {
            "documentation": [".md", ".txt"],
            "data": [".csv", ".json"],
            "config": [".toml", ".yml", ".yaml", ".ini", ".xml", ".plist"],
            "scripts": [".py", ".sh", ".pl", ".bat"],
            "notebooks": [".ipynb"],
            "web": [".html", ".css", ".js", ".jsx"],
            "images": [".png", ".jpg", ".jpeg", ".svg"],
            "archives": [".zip", ".tar", ".gz"],
            "logs": [".log"],
            "backups": [".bak", ".py-bak", ".seo_backup"],
            "other": [],
        }

        organized = 0
        by_type = {}

        for item in self.base_dir.iterdir():
            if not item.is_file() or item.name.startswith("."):
                continue

            # Determine type
            ext = item.suffix.lower()
            file_type = "other"

            for type_name, extensions in type_mappings.items():
                if ext in extensions:
                    file_type = type_name
                    break

            if file_type not in by_type:
                by_type[file_type] = []
            by_type[file_type].append(item.name)

        # Organize by type
        for file_type, files in sorted(by_type.items()):
            if not files:
                continue

            type_dir = self.loose_files_dir / file_type
            print(f"   {file_type}/{'':<20} {len(files)} files")

            if not dry_run:
                type_dir.mkdir(parents=True, exist_ok=True)

                for filename in files:
                    source = self.base_dir / filename
                    dest = type_dir / filename

                    if not dest.exists():
                        shutil.move(str(source), str(dest))

            organized += len(files)

        print(
            f"\n   Total: {organized} files {'would be' if dry_run else ''} organized"
        )
        print()

    def execute(self, dry_run=True):
        """Execute full cleanup"""

        print("=" * 70)
        print(f"🚀 COMPREHENSIVE CLEANUP {'(DRY RUN)' if dry_run else '(LIVE)'}")
        print("=" * 70)
        print()

        self.archive_terrible_directories(dry_run)
        self.consolidate_redundant_groups(dry_run)
        self.organize_loose_files(dry_run)

        print("=" * 70)
        print(f"✅ Cleanup {'simulation' if dry_run else 'execution'} complete!")
        print("=" * 70)
        print()

        if dry_run:
            print("💡 To execute for real, run:")
            print("   python3 execute_comprehensive_cleanup.py --execute")


def main():
    import sys

    base_dir = Path("/Users/steven/Documents/python")
    dry_run = "--execute" not in sys.argv

    cleanup = ComprehensiveCleanup(base_dir)
    cleanup.execute(dry_run=dry_run)


if __name__ == "__main__":
    main()
