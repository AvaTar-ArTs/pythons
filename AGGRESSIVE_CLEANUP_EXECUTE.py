#!/usr/bin/env python3
"""
🧹 AGGRESSIVE CLEANUP - FIX EVERYTHING
Consolidate 131 directories → ~25 clean directories
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class AggressiveCleanup:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)
        self.moved = 0
        self.deleted = 0
        self.errors = []

        # Comprehensive consolidation map
        self.moves = {
            # YOUTUBE (20+ directories!)
            'AUTOMATION_BOTS/youtube_bots': [
                'Auto-YouTube', 'automated-yt-channel', 'AutomatedYoutubeShorts',
                'Automatic-Video-Generator-for-youtube', 'YT-Comment-Bot-master',
                'YT-detail-info-Story', 'YTube', 'YouTube-Viewer',
                'YouTube-shorts-generator', 'Youtube-Gmail-Account-Generator',
                'youtube-bulk-upload-main', 'youtube-gpt-content-maker',
                'youtube-shorts-reddit-scraper', 'youtube-upload',
                'youtube-uploader-main', 'youtubegen', 'ytdl',
                'scrape-youtube-channel-videos-url'
            ],

            # REDDIT
            'AUTOMATION_BOTS/reddit_bots': [
                'reddit-text-extract', 'redditSentiment', 'redditVideoGenerator',
                'reddit_video_maker', 'RedditVideoMakerBot-master'
            ],

            # TWITCH
            'AUTOMATION_BOTS/twitch_bots': [
                'Twitch-Best-Of', 'Twitch-TikTok-Youtube-Viewbot',
                'TwitchCompilationCreator', 'twitchtube'
            ],

            # SUNO/MUSIC
            'audio_generation/suno': [
                'suno-analytics', 'suno-analytics-jupyter', 'suno-to-google-sheets'
            ],

            # TRANSCRIPTION
            'audio_transcription': [
                'transcribe', 'transcribe-keywords', 'AutoTranscribe'
            ],

            # GALLERIES/HTML
            'MEDIA_PROCESSING/galleries': [
                'Auto-html-gallery-scripts', 'simplegallery-MY-TEMPLATE 2',
                'simplegallery-bin', 'htmlsve'
            ],

            # VIDEO PROCESSING
            'MEDIA_PROCESSING/video_tools': [
                'videoGenerator', 'video_processing'
            ],

            # DATA/DOCS
            'DATA_UTILITIES': [
                'data', 'data-analyzer', 'doc-generator'
            ],

            # SCRAPERS/WEB
            'AUTOMATION_BOTS/web_scrapers': [
                'fiverr-scraping-api', 'scrapers', 'web_scraping'
            ],

            # SOCIAL MEDIA
            'AUTOMATION_BOTS/social_media_automation': [
                'instagram-follower-scraper', 'instapy-quickstart',
                'Redbubble-Auto-Uploader-stickers', 'redbubble_1.group'
            ],

            # CONTENT CREATION
            'content_creation/blog_automation': [
                'autoblog', 'autoblog using the ChatGPT'
            ],
            'content_creation/typography': [
                'AutoTypographyh - lyrics'
            ],
            'content_creation/quiz': [
                'quiz-talk'
            ],

            # IMAGE TOOLS
            'MEDIA_PROCESSING/image_tools': [
                'Adobe Python Scripts', 'leonardo', 'upscale-python',
                'photoshop-mockup-automation', 'cross-stitch-pattern-maker'
            ],

            # AUDIO TOOLS
            'audio_generation/spotify': [
                'savify', 'SpotifyMP3'
            ],
            'audio_generation/tts': [
                'tts_engines'
            ],

            # DOCUMENTATION
            'documentation': [
                'Comprehensive-setup-docs', 'md', 'MDs',
                'LLM-Engineers-Handbook-main', 'LLM_Course_Engineers_Handbook_Cover',
                'Python Automation Arsenal', 'prompt_engineering',
                'medium-articles', 'medium_articles'
            ],

            # UTILITIES
            'utilities': [
                'Drive-image-link-converter', 'HTML-Embed-youtube-videos-on-webpage',
                'download-all-the-gifs', 'sorting', 'ygpt', 'fdupes',
                'lyrics-keys-indo', 'sora-video-generator'
            ],

            # CLONED PROJECTS
            '_cloned_projects': [
                'ai-comic-factory-main', 'axolotl-main', 'remove-bg-cli',
                'suno-scraper-typescript', 'Twitch-Streamer-GPT-main',
                'TG-MegaBot', 'botty', 'Python-and-OpenAI-main',
                'spicetify-themes'
            ],

            # NOTEBOOKS
            '_notebooks': [
                'colab'
            ],

            # ARTICLES/CONTENT
            'content_creation/articles': [
                'intelligent_articles'
            ]
        }

        # DELETE (temp/stale/unclear)
        self.delete = [
            '__pycache__', '_consolidation_logs', 'clean', 'clean-organizer', 'clean_1 2',
            'ENV_D_ANALYSIS_20251201_054751', 'ENV_D_ZSHRC_COMPARISON_20251201_055039',
            'MULTI_DEPTH_ANALYSIS_20251201_050441', 'MULTI_DEPTH_ANALYSIS_20251201_050647',
            'MULTI_DEPTH_ANALYSIS_20251201_070022', 'env_backups', 'site', 'zip',
            'POD-auto', 'Sort', 'ai_tools', 'tui.editor', 'PRINTIFY_API_MUG'
        ]

    def execute_cleanup(self):
        """Execute the comprehensive cleanup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_dir = self.pythons_dir / '_archive' / f'aggressive-cleanup-{timestamp}'
        archive_dir.mkdir(parents=True, exist_ok=True)

        print("\n🧹 EXECUTING AGGRESSIVE CLEANUP")
        print("=" * 70)
        print(f"📦 Backup archive: {archive_dir}\n")

        # PHASE 1: CONSOLIDATIONS
        print("🔄 PHASE 1: CONSOLIDATING DIRECTORIES\n")

        for target, sources in self.moves.items():
            target_path = self.pythons_dir / target
            target_path.mkdir(parents=True, exist_ok=True)

            for source_name in sources:
                source_path = self.pythons_dir / source_name

                if not source_path.exists():
                    continue

                try:
                    final_target = target_path / source_name

                    if final_target.exists():
                        print(f"⚠️  Skip (exists): {source_name} → {target}")
                        continue

                    shutil.move(str(source_path), str(final_target))
                    self.moved += 1
                    print(f"✅ {source_name} → {target}")

                except Exception as e:
                    self.errors.append(f"{source_name}: {e}")
                    print(f"❌ Error: {source_name} - {e}")

        # PHASE 2: DELETIONS
        print(f"\n🗑️  PHASE 2: DELETING STALE DIRECTORIES\n")

        for dir_name in self.delete:
            dir_path = self.pythons_dir / dir_name

            if not dir_path.exists():
                continue

            try:
                # Archive before delete
                archive_path = archive_dir / dir_name
                shutil.move(str(dir_path), str(archive_path))
                self.deleted += 1
                print(f"🗑️  Deleted: {dir_name} (archived)")

            except Exception as e:
                self.errors.append(f"{dir_name}: {e}")
                print(f"❌ Error: {dir_name} - {e}")

        # PHASE 3: ORGANIZE ROOT FILES
        print(f"\n📝 PHASE 3: ORGANIZING ROOT FILES\n")

        root_files = [f for f in self.pythons_dir.glob('*.py') if f.is_file()]
        organized = 0

        for f in root_files:
            name = f.name.lower()

            # Skip our cleanup scripts
            if any(name.startswith(x) for x in ['deep_', 'intelligent_', 'smart_',
                                                  'cleanup_', 'comprehensive_', 'aggressive_']):
                continue

            # Categorize and move
            target = None
            if 'analyze' in name or 'analyzer' in name:
                target = self.pythons_dir / 'DATA_UTILITIES' / 'data_analyzers'
            elif 'audio' in name or 'transcribe' in name or 'tts' in name:
                target = self.pythons_dir / 'audio_generation'
            elif 'bot' in name or 'automat' in name:
                target = self.pythons_dir / 'AUTOMATION_BOTS'
            else:
                target = self.pythons_dir / 'utilities'

            try:
                target.mkdir(parents=True, exist_ok=True)
                final_path = target / f.name

                if final_path.exists():
                    print(f"⚠️  Skip: {f.name}")
                    continue

                shutil.move(str(f), str(final_path))
                organized += 1

                if organized % 10 == 0:
                    print(f"   ... organized {organized} files")

            except Exception as e:
                self.errors.append(f"{f.name}: {e}")

        if organized > 0:
            print(f"✅ Organized {organized} root files\n")

        # SUMMARY
        print("=" * 70)
        print("📊 CLEANUP SUMMARY")
        print("=" * 70)
        print(f"Directories moved:      {self.moved}")
        print(f"Directories deleted:    {self.deleted}")
        print(f"Root files organized:   {organized}")
        print(f"Errors:                 {len(self.errors)}")
        print("=" * 70)

        if self.errors:
            print("\n⚠️  ERRORS:")
            for error in self.errors[:10]:
                print(f"  - {error}")
            if len(self.errors) > 10:
                print(f"  ... and {len(self.errors) - 10} more")

        print(f"\n📦 Backup saved: {archive_dir}")

        # Count remaining
        remaining_dirs = len([d for d in self.pythons_dir.iterdir()
                             if d.is_dir() and not d.name.startswith('.')])
        remaining_files = len(list(self.pythons_dir.glob('*.py')))

        print(f"\n🎯 RESULT:")
        print(f"  Directories remaining: {remaining_dirs} (was 131!)")
        print(f"  Root files remaining:  {remaining_files} (was 77!)")
        print("\n✨ ~/pythons/ is now CLEAN! ✨")


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║        🧹 AGGRESSIVE CLEANUP - FIX EVERYTHING                     ║
║        131 directories → ~25 clean directories                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    print("⚠️  This will:")
    print("  • Consolidate 80+ directories")
    print("  • Delete 15+ stale directories")
    print("  • Organize 77 root files")
    print("  • Create backup archive")
    print()

    confirm = input("Type 'FIX IT' to execute: ")

    if confirm == 'FIX IT':
        cleanup = AggressiveCleanup()
        cleanup.execute_cleanup()
    else:
        print("\n❌ Cancelled")


if __name__ == "__main__":
    main()

