#!/usr/bin/env python3
"""
Migrate Old Directories to Context-Fluid Structure
Move remaining old category directories into new adaptive structure
"""

import shutil
from pathlib import Path


class OldDirectoryMigrator:
    """Migrate old directories to context-fluid structure"""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

        # Map old directories to new context-fluid locations
        self.migrations = {
            # Keep these protected
            "experiments": None,
            "tests": None,
            "notebooks": None,
            "AI_CONTENT": None,
            "AUTOMATION_BOTS": None,
            "DATA_UTILITIES": None,
            "MEDIA_PROCESSING": None,
            "DOCUMENTATION": None,
            # Archive old structure
            "_archived_cleanup": None,  # Keep as archive
            "_organized_root_files": None,  # Keep as archive
            # Old AI categories → AI_CONTENT
            "ai-chatbot": "AI_CONTENT/legacy_categories/ai-chatbot",
            "ai-image-generator": "AI_CONTENT/legacy_categories/ai-image-generator",
            "ai-text-generator": "AI_CONTENT/legacy_categories/ai-text-generator",
            # Old automation → AUTOMATION_BOTS
            "bot-automation": "AUTOMATION_BOTS/legacy_categories/bot-automation",
            "instagram-automation": "AUTOMATION_BOTS/legacy_categories/instagram-automation",
            "reddit-automation": "AUTOMATION_BOTS/legacy_categories/reddit-automation",
            "automation": "AUTOMATION_BOTS/legacy_categories/automation",
            # Old media → MEDIA_PROCESSING
            "audio-converter": "MEDIA_PROCESSING/legacy_categories/audio-converter",
            "audio-mixer": "MEDIA_PROCESSING/legacy_categories/audio-mixer",
            "audio-transcription": "MEDIA_PROCESSING/legacy_categories/audio-transcription",
            "video-transcription": "MEDIA_PROCESSING/legacy_categories/video-transcription",
            "video-converter": "MEDIA_PROCESSING/legacy_categories/video-converter",
            "video-downloader": "MEDIA_PROCESSING/legacy_categories/video-downloader",
            "video-editor": "MEDIA_PROCESSING/legacy_categories/video-editor",
            "video-effects": "MEDIA_PROCESSING/legacy_categories/video-effects",
            "video-generator": "MEDIA_PROCESSING/legacy_categories/video-generator",
            "video-analyzer": "MEDIA_PROCESSING/legacy_categories/video-analyzer",
            "image-converter": "MEDIA_PROCESSING/legacy_categories/image-converter",
            "image-format-converter": "MEDIA_PROCESSING/legacy_categories/image-format-converter",
            "image-resizer": "MEDIA_PROCESSING/legacy_categories/image-resizer",
            "image-upscaler": "MEDIA_PROCESSING/legacy_categories/image-upscaler",
            "upscaler": "MEDIA_PROCESSING/legacy_categories/upscaler",
            "background-remover": "MEDIA_PROCESSING/legacy_categories/background-remover",
            "face-processor": "MEDIA_PROCESSING/legacy_categories/face-processor",
            "watermark-tool": "MEDIA_PROCESSING/legacy_categories/watermark-tool",
            "thumbnail-generator": "MEDIA_PROCESSING/legacy_categories/thumbnail-generator",
            "gallery-generator": "MEDIA_PROCESSING/legacy_categories/gallery-generator",
            "text-to-speech": "MEDIA_PROCESSING/legacy_categories/text-to-speech",
            "transcribe-analysis": "MEDIA_PROCESSING/legacy_categories/transcribe-analysis",
            "subtitle-generator": "MEDIA_PROCESSING/legacy_categories/subtitle-generator",
            "ocr-extractor": "MEDIA_PROCESSING/legacy_categories/ocr-extractor",
            # Old data → DATA_UTILITIES
            "csv-processor": "DATA_UTILITIES/legacy_categories/csv-processor",
            "json-processor": "DATA_UTILITIES/legacy_categories/json-processor",
            "excel-processor": "DATA_UTILITIES/legacy_categories/excel-processor",
            "pdf-processor": "DATA_UTILITIES/legacy_categories/pdf-processor",
            "pdf-converter": "DATA_UTILITIES/legacy_categories/pdf-converter",
            "data-analyzer": "DATA_UTILITIES/legacy_categories/data-analyzer",
            "data-extractor": "DATA_UTILITIES/legacy_categories/data-extractor",
            "file-organizer": "DATA_UTILITIES/legacy_categories/file-organizer",
            "file-downloader": "DATA_UTILITIES/legacy_categories/file-downloader",
            "backup-tool": "DATA_UTILITIES/legacy_categories/backup-tool",
            "batch-processor": "DATA_UTILITIES/legacy_categories/batch-processor",
            "monitor-tool": "DATA_UTILITIES/legacy_categories/monitor-tool",
            "scheduler": "DATA_UTILITIES/legacy_categories/scheduler",
            "database": "DATA_UTILITIES/legacy_categories/database",
            "database-tool": "DATA_UTILITIES/legacy_categories/database-tool",
            # Web/API → AUTOMATION_BOTS
            "web-scraper": "AUTOMATION_BOTS/legacy_categories/web-scraper",
            "web-development": "AUTOMATION_BOTS/legacy_categories/web-development",
            "api-client": "AUTOMATION_BOTS/legacy_categories/api-client",
            "api-development": "AUTOMATION_BOTS/legacy_categories/api-development",
            "html-generator": "AUTOMATION_BOTS/legacy_categories/html-generator",
            "youtube-downloader": "AUTOMATION_BOTS/legacy_categories/youtube-downloader",
            "tiktok-downloader": "AUTOMATION_BOTS/legacy_categories/tiktok-downloader",
            "youtube-automation": "AUTOMATION_BOTS/legacy_categories/youtube-automation",
            "telegram-bot": "AUTOMATION_BOTS/legacy_categories/telegram-bot",
            "twitter-automation": "AUTOMATION_BOTS/legacy_categories/twitter-automation",
            # ML → AI_CONTENT
            "ml-trainer": "AI_CONTENT/legacy_categories/ml-trainer",
            "machine-learning": "AI_CONTENT/legacy_categories/machine-learning",
            # Misc → DATA_UTILITIES
            "general-scripts": "DATA_UTILITIES/legacy_categories/general-scripts",
            "utilities": "DATA_UTILITIES/legacy_categories/utilities",
            "cli-tool": "DATA_UTILITIES/legacy_categories/cli-tool",
            "email-automation": "DATA_UTILITIES/legacy_categories/email-automation",
            "seo-optimizer": "DATA_UTILITIES/legacy_categories/seo-optimizer",
            "doc-generator": "DOCUMENTATION/legacy_categories/doc-generator",
            "documentation": "DOCUMENTATION/legacy_categories/documentation",
            # Apps/config → DATA_UTILITIES
            "apps": "DATA_UTILITIES/legacy_categories/apps",
            "configuration": "DATA_UTILITIES/legacy_categories/configuration",
            "alfred_workflow": "DATA_UTILITIES/legacy_categories/alfred_workflow",
            "shared_libraries": "DATA_UTILITIES/legacy_categories/shared_libraries",
            "development_tools": "DATA_UTILITIES/legacy_categories/development_tools",
            "playlist-manager": "DATA_UTILITIES/legacy_categories/playlist-manager",
            # Archive misc
            "content-generation": "_archived_cleanup/content-generation",
            "cross-stitch-pattern-maker": "_archived_cleanup/cross-stitch-pattern-maker",
            "examples": "_archived_cleanup/examples",
            "experimental": "_archived_cleanup/experimental",
            "As-a-Man-Thinketh": "_archived_cleanup/As-a-Man-Thinketh",
            "download-all-the-gifs": "_archived_cleanup/download-all-the-gifs",
            "Drive-image-link-converter": "_archived_cleanup/Drive-image-link-converter",
        }

    def execute(self, dry_run=True):
        """Execute directory migration"""

        print("=" * 70)
        print(f"🔄 MIGRATE OLD DIRECTORIES {'(DRY RUN)' if dry_run else '(LIVE)'}")
        print("=" * 70)
        print()

        moved_count = 0
        skipped_count = 0

        for old_dir, new_location in sorted(self.migrations.items()):
            # Skip protected directories
            if new_location is None:
                continue

            source = self.base_dir / old_dir

            if not source.exists() or not source.is_dir():
                continue

            target = self.base_dir / new_location

            # Count files
            try:
                file_count = len(list(source.rglob("*")))
            except:
                file_count = 0

            if dry_run:
                print(f"📦 {old_dir:<40} → {new_location}")
                print(f"   [DRY RUN] Would move {file_count} items")
            else:
                # Create target parent
                target.parent.mkdir(parents=True, exist_ok=True)

                # Move directory
                try:
                    shutil.move(str(source), str(target))
                    print(f"✅ {old_dir:<40} → {new_location}")
                    print(f"   Moved {file_count} items")
                    moved_count += 1
                except Exception as e:
                    print(f"❌ {old_dir:<40} ERROR: {e}")
                    skipped_count += 1

            print()

        print("=" * 70)
        print(f"{'Simulation' if dry_run else 'Migration'} complete!")
        print(f"   Directories {'would be' if dry_run else ''} moved: {moved_count}")
        if skipped_count > 0:
            print(f"   Errors: {skipped_count}")
        print("=" * 70)

        if dry_run:
            print("\n💡 To execute, run:")
            print("   python3 migrate_old_dirs.py --execute")


def main():
    import sys

    base_dir = Path("/Users/steven/Documents/python")
    dry_run = "--execute" not in sys.argv

    migrator = OldDirectoryMigrator(base_dir)
    migrator.execute(dry_run=dry_run)


if __name__ == "__main__":
    main()
