"""
Second Pass Migration Audit

This module provides functionality for second pass migration audit.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_600 = 600

#!/usr/bin/env python3
"""
Analyze remaining Python files and directories for second migration pass
"""

import os
import re
from pathlib import Path
from collections import defaultdict


def analyze_remaining_files():
    """Analyze all remaining Python files and directories."""
    base_path = Path(Path("/Users/steven/Documents/python"))

    # Categories for remaining files
    categories = {
        "image_processing": [],
        "quiz_tts": [],
        "conversion_tools": [],
        "gallery_html": [],
        "csv_data": [],
        "ocr_processing": [],
        "cleanup_utilities": [],
        "test_scripts": [],
        "misc_utilities": [],
        "duplicates": [],
        "unorganized_dirs": [],
    }

    logger.info("🔍 Analyzing remaining files and directories...")
    logger.info("=" * 60)

    # Analyze Python files
    logger.info("\n📄 PYTHON FILES ANALYSIS")
    logger.info("-" * 30)

    for py_file in base_path.glob("*.py"):
        if py_file.name.startswith("analyze_migration") or py_file.name.startswith("migrate_projects"):
            continue  # Skip our migration scripts

        name_lower = py_file.name.lower()

        # Categorize by filename patterns
        if any(pattern in name_lower for pattern in ["img", "image", "photo", "picture", "gallery"]):
            categories["image_processing"].append(py_file.name)
        elif any(pattern in name_lower for pattern in ["quiz", "tts", "speech", "audio", "voice"]):
            categories["quiz_tts"].append(py_file.name)
        elif any(pattern in name_lower for pattern in ["convert", "transform", "change", "format"]):
            categories["conversion_tools"].append(py_file.name)
        elif any(pattern in name_lower for pattern in ["html", "web", "gallery", "website"]):
            categories["gallery_html"].append(py_file.name)
        elif any(pattern in name_lower for pattern in ["csv", "data", "table", "spreadsheet"]):
            categories["csv_data"].append(py_file.name)
        elif any(pattern in name_lower for pattern in ["ocr", "text", "extract", "read"]):
            categories["ocr_processing"].append(py_file.name)
        elif any(pattern in name_lower for pattern in ["clean", "sort", "organize", "fix"]):
            categories["cleanup_utilities"].append(py_file.name)
        elif any(pattern in name_lower for pattern in ["test", "debug", "check", "verify"]):
            categories["test_scripts"].append(py_file.name)
        elif any(pattern in name_lower for pattern in ["copy", " (1)", " (2)", "backup"]):
            categories["duplicates"].append(py_file.name)
        else:
            categories["misc_utilities"].append(py_file.name)

    # Analyze remaining directories
    logger.info("\n📁 REMAINING DIRECTORIES ANALYSIS")
    logger.info("-" * 30)

    for item in base_path.iterdir():
        if item.is_dir() and not item.name.startswith((".", "0", "MIGRATION")):
            name_lower = item.name.lower()

            # Categorize directories
            if any(pattern in name_lower for pattern in ["youtube", "yt", "video", "shorts", "reddit"]):
                categories["unorganized_dirs"].append(f"{item.name} (YouTube/Video)")
            elif any(pattern in name_lower for pattern in ["instagram", "social", "fb", "facebook"]):
                categories["unorganized_dirs"].append(f"{item.name} (Social Media)")
            elif any(pattern in name_lower for pattern in ["ai", "dalle", "comic", "pattern", "creative"]):
                categories["unorganized_dirs"].append(f"{item.name} (AI/Creative)")
            elif any(pattern in name_lower for pattern in ["scraping", "scraper", "backlink", "fiverr"]):
                categories["unorganized_dirs"].append(f"{item.name} (Web Scraping)")
            elif any(pattern in name_lower for pattern in ["audio", "video", "transcribe", "tts"]):
                categories["unorganized_dirs"].append(f"{item.name} (Audio/Video)")
            elif any(pattern in name_lower for pattern in ["clean", "sort", "organize", "utility"]):
                categories["unorganized_dirs"].append(f"{item.name} (Utilities)")
            else:
                categories["unorganized_dirs"].append(f"{item.name} (Miscellaneous)")

    return categories


def show_remaining_analysis(categories):
    """Display analysis of remaining files."""
    logger.info("\n📋 REMAINING FILES MIGRATION PLAN")
    logger.info("=" * 60)

    # Image Processing
    if categories["image_processing"]:
        logger.info(f"\n🖼️  IMAGE PROCESSING ({len(categories['image_processing'])} files)")
        logger.info("-" * 40)
        logger.info("→ 05_audio_video/image_processors/")
        for file in sorted(categories["image_processing"])[:10]:
            logger.info(f"  • {file}")
        if len(categories["image_processing"]) > 10:
            logger.info(f"  ... and {len(categories['image_processing']) - 10} more")

    # Quiz/TTS
    if categories["quiz_tts"]:
        logger.info(f"\n🎤 QUIZ/TTS TOOLS ({len(categories['quiz_tts'])} files)")
        logger.info("-" * 40)
        logger.info("→ 05_audio_video/audio_processors/quiz_tts/")
        for file in sorted(categories["quiz_tts"])[:10]:
            logger.info(f"  • {file}")
        if len(categories["quiz_tts"]) > 10:
            logger.info(f"  ... and {len(categories['quiz_tts']) - 10} more")

    # Conversion Tools
    if categories["conversion_tools"]:
        logger.info(f"\n🔄 CONVERSION TOOLS ({len(categories['conversion_tools'])} files)")
        logger.info("-" * 40)
        logger.info("→ 06_utilities/converters/")
        for file in sorted(categories["conversion_tools"])[:10]:
            logger.info(f"  • {file}")
        if len(categories["conversion_tools"]) > 10:
            logger.info(f"  ... and {len(categories['conversion_tools']) - 10} more")

    # Gallery/HTML
    if categories["gallery_html"]:
        logger.info(f"\n🌐 GALLERY/HTML TOOLS ({len(categories['gallery_html'])} files)")
        logger.info("-" * 40)
        logger.info("→ 07_experimental/web_tools/")
        for file in sorted(categories["gallery_html"])[:10]:
            logger.info(f"  • {file}")
        if len(categories["gallery_html"]) > 10:
            logger.info(f"  ... and {len(categories['gallery_html']) - 10} more")

    # CSV/Data
    if categories["csv_data"]:
        logger.info(f"\n📊 CSV/DATA TOOLS ({len(categories['csv_data'])} files)")
        logger.info("-" * 40)
        logger.info("→ 06_utilities/data_processors/")
        for file in sorted(categories["csv_data"])[:10]:
            logger.info(f"  • {file}")
        if len(categories["csv_data"]) > 10:
            logger.info(f"  ... and {len(categories['csv_data']) - 10} more")

    # OCR Processing
    if categories["ocr_processing"]:
        logger.info(f"\n👁️  OCR/TEXT PROCESSING ({len(categories['ocr_processing'])} files)")
        logger.info("-" * 40)
        logger.info("→ 01_core_tools/text_processors/")
        for file in sorted(categories["ocr_processing"])[:10]:
            logger.info(f"  • {file}")
        if len(categories["ocr_processing"]) > 10:
            logger.info(f"  ... and {len(categories['ocr_processing']) - 10} more")

    # Cleanup Utilities
    if categories["cleanup_utilities"]:
        logger.info(f"\n🧹 CLEANUP UTILITIES ({len(categories['cleanup_utilities'])} files)")
        logger.info("-" * 40)
        logger.info("→ 06_utilities/system_tools/")
        for file in sorted(categories["cleanup_utilities"])[:10]:
            logger.info(f"  • {file}")
        if len(categories["cleanup_utilities"]) > 10:
            logger.info(f"  ... and {len(categories['cleanup_utilities']) - 10} more")

    # Test Scripts
    if categories["test_scripts"]:
        logger.info(f"\n🧪 TEST SCRIPTS ({len(categories['test_scripts'])} files)")
        logger.info("-" * 40)
        logger.info("→ 07_experimental/testing/")
        for file in sorted(categories["test_scripts"])[:10]:
            logger.info(f"  • {file}")
        if len(categories["test_scripts"]) > 10:
            logger.info(f"  ... and {len(categories['test_scripts']) - 10} more")

    # Duplicates
    if categories["duplicates"]:
        logger.info(f"\n📄 DUPLICATES ({len(categories['duplicates'])} files)")
        logger.info("-" * 40)
        logger.info("→ 08_archived/old_versions/")
        for file in sorted(categories["duplicates"])[:10]:
            logger.info(f"  • {file}")
        if len(categories["duplicates"]) > 10:
            logger.info(f"  ... and {len(categories['duplicates']) - 10} more")

    # Misc Utilities
    if categories["misc_utilities"]:
        logger.info(f"\n🔧 MISC UTILITIES ({len(categories['misc_utilities'])} files)")
        logger.info("-" * 40)
        logger.info("→ 07_experimental/misc/")
        for file in sorted(categories["misc_utilities"])[:15]:
            logger.info(f"  • {file}")
        if len(categories["misc_utilities"]) > 15:
            logger.info(f"  ... and {len(categories['misc_utilities']) - 15} more")

    # Unorganized Directories
    if categories["unorganized_dirs"]:
        logger.info(f"\n📁 UNORGANIZED DIRECTORIES ({len(categories['unorganized_dirs'])} directories)")
        logger.info("-" * 40)
        for item in sorted(categories["unorganized_dirs"])[:20]:
            logger.info(f"  • {item}")
        if len(categories["unorganized_dirs"]) > 20:
            logger.info(f"  ... and {len(categories['unorganized_dirs']) - 20} more")


def create_second_migration_script(categories):
    """Create a second migration script for remaining files."""
    script_content = '''#!/usr/bin/env python3
"""
Second Migration Pass - Organize Remaining Python Files
"""

import os
import shutil
from pathlib import Path

def create_additional_directories():
    """Create additional directories for remaining files."""
    base_path = Path(Path("/Users/steven/Documents/python"))
    
    additional_dirs = [
        "01_core_tools/text_processors",
        "05_audio_video/image_processors", 
        "05_audio_video/audio_processors/quiz_tts",
        "06_utilities/converters",
        "06_utilities/data_processors",
        "07_experimental/web_tools",
        "07_experimental/misc",
        "07_experimental/testing"
    ]
    
    for dir_path in additional_dirs:
        full_path = base_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created: {dir_path}")

def migrate_remaining_files():
    """Migrate remaining Python files."""
    base_path = Path(Path("/Users/steven/Documents/python"))
    
    # File mappings
    file_mappings = {
        # Image Processing
        "imgconvert_colab.py": "05_audio_video/image_processors/",
        "scan_images_individual.py": "05_audio_video/image_processors/",
        "categorize_html.py": "05_audio_video/image_processors/",
        
        # Quiz/TTS
        "quiz-.py": "05_audio_video/audio_processors/quiz_tts/",
        "quiz-tts.py": "05_audio_video/audio_processors/quiz_tts/",
        "tts-doc.py": "05_audio_video/audio_processors/quiz_tts/",
        
        # Conversion Tools
        "convert copy.py": "06_utilities/converters/",
        "up-down-old.py": "06_utilities/converters/",
        "serialize.py": "06_utilities/converters/",
        
        # Gallery/HTML
        "test_google_gallery_logic.py": "07_experimental/web_tools/",
        
        # CSV/Data
        "csv-output.py": "06_utilities/data_processors/",
        
        # OCR Processing
        "ocr_gpt_renamer.py": "01_core_tools/text_processors/",
        
        # Cleanup
        "cleanups.py": "06_utilities/system_tools/",
        "autofixer.py": "06_utilities/system_tools/",
        
        # Test Scripts
        "trek 2.py": "07_experimental/testing/",
        
        # Misc
        "y--.py": "07_experimental/misc/",
        "vance.py": "07_experimental/misc/",
        "outs.py": "07_experimental/misc/",
        "pythoncatorgize.py": "07_experimental/misc/"
    }
    
    for old_name, new_dir in file_mappings.items():
        old_file = base_path / old_name
        new_file = base_path / new_dir / old_name
        
        if old_file.exists():
            new_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_file), str(new_file))
            logger.info(f"Moved: {old_name} → {new_dir}")

def migrate_remaining_directories():
    """Migrate remaining directories."""
    base_path = Path(Path("/Users/steven/Documents/python"))
    
    # Directory mappings
    dir_mappings = {
        # YouTube/Video projects
        "Youtube": "02_youtube_automation/youtube_tools/",
        "YTube": "02_youtube_automation/youtube_tools/",
        "YouTube-Bot": "02_youtube_automation/youtube_tools/",
        "YouTube-Viewer": "02_youtube_automation/youtube_tools/",
        "YouTube-Livestream-Botter": "02_youtube_automation/youtube_tools/",
        "youtube-uploader-main": "02_youtube_automation/youtube_tools/",
        "youtube_channel_downloader": "02_youtube_automation/youtube_tools/",
        "youtube-shorts-reddit-scraper": "02_youtube_automation/youtube_tools/",
        "YoutubeBot": "02_youtube_automation/youtube_tools/",
        "AutomatedYoutubeShorts": "02_youtube_automation/youtube_tools/",
        "shorts_service_mvp_v1": "02_youtube_automation/youtube_tools/",
        
        # Social Media
        "Instagram-Bot": "04_web_scraping/social_media/instagram/",
        "instagram-follower-scraper": "04_web_scraping/social_media/instagram/",
        "Instagram-Mass-report": "04_web_scraping/social_media/instagram/",
        "Instagram-mass-reporter": "04_web_scraping/social_media/instagram/",
        "InstagramReportBot": "04_web_scraping/social_media/instagram/",
        "instapy-quickstart": "04_web_scraping/social_media/instagram/",
        "igbot": "04_web_scraping/social_media/instagram/",
        
        # TikTok
        "Tiktok-Trending-Data-Scraper": "04_web_scraping/social_media/tiktok/",
        "tiktok-comment-liker": "04_web_scraping/social_media/tiktok/",
        "tiktok-generator": "04_web_scraping/social_media/tiktok/",
        "TikTok-Compilation-Video-Generator": "04_web_scraping/social_media/tiktok/",
        "tiktok-video-downloader": "04_web_scraping/social_media/tiktok/",
        
        # Reddit
        "reddit_video_maker": "02_youtube_automation/reddit_tools/",
        "reddit-text-extract": "02_youtube_automation/reddit_tools/",
        "reddit-to-instagram-bot": "02_youtube_automation/reddit_tools/",
        "redditSentiment": "02_youtube_automation/reddit_tools/",
        "redditVideoGenerator": "02_youtube_automation/reddit_tools/",
        "RedditVideoMakerBot-master": "02_youtube_automation/reddit_tools/",
        "Reddit-Tiktok-Video-Bot": "02_youtube_automation/reddit_tools/",
        
        # AI/Creative
        "leonardo": "03_ai_creative_tools/image_generation/leonardo/",
        "upscale-python": "03_ai_creative_tools/image_generation/upscaler/",
        "upscale": "03_ai_creative_tools/image_generation/upscaler/",
        "remove-bg-cli": "03_ai_creative_tools/image_generation/background_removal/",
        "photoshop-mockup-automation": "03_ai_creative_tools/image_generation/photoshop/",
        
        # Audio/Video
        "transcribe": "05_audio_video/transcription_tools/transcribe/",
        "transcribe-keywords": "05_audio_video/transcription_tools/keywords/",
        "videoGenerator": "05_audio_video/video_editors/generator/",
        "sora-video-generator": "05_audio_video/video_editors/sora/",
        "sora-storyboard": "05_audio_video/video_editors/sora/",
        "TwitchClipGenerator-main": "05_audio_video/video_editors/twitch/",
        "Twitch-Best-Of": "05_audio_video/video_editors/twitch/",
        "TwitchCompilationCreator": "05_audio_video/video_editors/twitch/",
        "Twitch-TikTok-Youtube-Viewbot": "05_audio_video/video_editors/twitch/",
        "twitchtube": "05_audio_video/video_editors/twitch/",
        
        # Utilities
        "Sort": "06_utilities/file_organizers/sort/",
        "sorting": "06_utilities/file_organizers/sorting/",
        "organize": "06_utilities/file_organizers/organize/",
        "Python-organize": "06_utilities/file_organizers/python_organize/",
        "tablecontentspython": "06_utilities/data_processors/table_contents/",
        
        # Web Tools
        "HTML-Embed-youtube-videos-on-webpage": "07_experimental/web_tools/html_embed/",
        "Auto-html-gallery-scripts": "07_experimental/web_tools/gallery_scripts/",
        "Drive-image-link-converter": "07_experimental/web_tools/drive_converter/",
        "download-all-the-gifs": "07_experimental/web_tools/gif_downloader/",
        "telegraph-image-downloader": "07_experimental/web_tools/telegraph/",
        
        # Misc/Experimental
        "botty": "07_experimental/bots/botty/",
        "007spam-BOT": "07_experimental/bots/spam_bot/",
        "TG-MegaBot": "07_experimental/bots/telegram/",
        "POD-auto": "07_experimental/automation/podcast/",
        "Riddle-Game": "07_experimental/games/riddle/",
        "prompt_pipeline": "07_experimental/ai_tools/prompt_pipeline/",
        "lyrics-keys-indo": "07_experimental/ai_tools/lyrics/",
        "ollama_gui": "07_experimental/ai_tools/ollama/",
        "opus_clip_open_clone": "07_experimental/ai_tools/opus_clip/",
        "opus_clip_v0_2_1_auto_style_NEW": "07_experimental/ai_tools/opus_clip/",
        "savify": "07_experimental/audio_tools/savify/",
        "SpotifyMP3": "07_experimental/audio_tools/spotify/",
        "spicetify-themes": "07_experimental/audio_tools/spicetify/",
        "spidy": "07_experimental/audio_tools/spidy/",
        "FOSS-Voice-Assistant": "07_experimental/ai_tools/voice_assistant/",
        "Manual Library": "07_experimental/libraries/manual/",
        "MDs": "07_experimental/libraries/markdown/",
        "docs": "09_documentation/project_docs/",
        "scripts": "07_experimental/scripts/",
        "colab": "07_experimental/colab/",
        "zip": "07_experimental/archives/zip/",
        "trashy-python": "07_experimental/misc/trashy/",
        "simplegallery-bin": "07_experimental/misc/simple_gallery/",
        "tui.editor": "07_experimental/misc/tui_editor/",
        "Untitled": "07_experimental/misc/untitled/",
        "This script is related to processing and categorizing output from the Flake8 static code analysis tool. A suitable category for this script could be \"Static Code Analysis\"": "07_experimental/analysis_tools/flake8_analyzer/",
        "rsnapshot": "07_experimental/backup_tools/rsnapshot/",
        "rsync-downloader": "07_experimental/backup_tools/rsync/",
        "rsync-macos-utility": "07_experimental/backup_tools/rsync/",
        "Nice-seemingly-macOS-backup-utility-based-on-rsync-called-grsyncx": "07_experimental/backup_tools/grsyncx/",
        "Redbubble-Auto-Uploader-stickers": "07_experimental/ecommerce/redbubble/",
        "redbubble.group": "07_experimental/ecommerce/redbubble/",
        "PrNdOwN": "07_experimental/misc/prndown/",
        "Carbons": "07_experimental/misc/carbons/",
        "CarbonCards": "07_experimental/misc/carbons/",
        "fancy": "07_experimental/misc/fancy/",
        "fancybox": "07_experimental/misc/fancybox/",
        "htmlsve": "07_experimental/misc/htmlsve/",
        "platypus": "07_experimental/misc/platypus/",
        "mediasim": "07_experimental/misc/mediasim/",
        "env_backups": "08_archived/backups/env_backups/",
        "Recents": "08_archived/backups/recents/",
        "analysis": "08_archived/backups/analysis/",
        "transcript": "08_archived/backups/transcript/",
        "intro-typography-ShareAE.com": "08_archived/backups/typography/",
        "LLM-Engineers-Handbook-main": "08_archived/backups/llm_handbook/",
        "LLM-engineer-handbook-main": "08_archived/backups/llm_handbook_v2/",
        "llm-course-main": "08_archived/backups/llm_course/",
        "Python-and-OpenAI-main": "08_archived/backups/python_openai/",
        "autoblog using the ChatGPT": "08_archived/backups/autoblog/",
        "-(Template) CONSTANT_600+ ChatGPT Prompts for Data Science": "08_archived/backups/chatgpt_prompts/",
        "Adobe Python Scripts": "08_archived/backups/adobe_scripts/",
        "SEO-Link-Building-Rank-in-Google-with-EDU-and-GOV-Backlinks": "08_archived/backups/seo_tools/",
        "Tiktok-Trending-Data-Scraper": "08_archived/backups/tiktok_scraper/",
        "spicetify-themes": "08_archived/backups/spicetify/",
        "spidy": "08_archived/backups/spidy/",
        "SpotifyMP3": "08_archived/backups/spotify/",
        "FOSS-Voice-Assistant": "08_archived/backups/voice_assistant/",
        "Manual Library": "08_archived/backups/manual_library/",
        "MDs": "08_archived/backups/markdown/",
        "docs": "08_archived/backups/docs/",
        "scripts": "08_archived/backups/scripts/",
        "colab": "08_archived/backups/colab/",
        "zip": "08_archived/backups/zip/",
        "trashy-python": "08_archived/backups/trashy/",
        "simplegallery-bin": "08_archived/backups/simple_gallery/",
        "tui.editor": "08_archived/backups/tui_editor/",
        "Untitled": "08_archived/backups/untitled/",
        "This script is related to processing and categorizing output from the Flake8 static code analysis tool. A suitable category for this script could be \"Static Code Analysis\"": "08_archived/backups/flake8_analyzer/",
        "rsnapshot": "08_archived/backups/rsnapshot/",
        "rsync-downloader": "08_archived/backups/rsync/",
        "rsync-macos-utility": "08_archived/backups/rsync/",
        "Nice-seemingly-macOS-backup-utility-based-on-rsync-called-grsyncx": "08_archived/backups/grsyncx/",
        "Redbubble-Auto-Uploader-stickers": "08_archived/backups/redbubble/",
        "redbubble.group": "08_archived/backups/redbubble/",
        "PrNdOwN": "08_archived/backups/prndown/",
        "Carbons": "08_archived/backups/carbons/",
        "CarbonCards": "08_archived/backups/carbons/",
        "fancy": "08_archived/backups/fancy/",
        "fancybox": "08_archived/backups/fancybox/",
        "htmlsve": "08_archived/backups/htmlsve/",
        "platypus": "08_archived/backups/platypus/",
        "mediasim": "08_archived/backups/mediasim/"
    }
    
    for old_name, new_path in dir_mappings.items():
        old_dir = base_path / old_name
        new_dir = base_path / new_path
        
        if old_dir.exists():
            new_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_dir), str(new_dir))
            logger.info(f"Moved: {old_name} → {new_path}")

def main():
    """Run second migration."""
    logger.info("🚀 Starting Second Migration Pass")
    logger.info("=" * 50)
    
    create_additional_directories()
    migrate_remaining_files()
    migrate_remaining_directories()
    
    logger.info("\n✅ Second migration completed!")

if __name__ == "__main__":
    main()
'''

    with open(Path("/Users/steven/Documents/python/migrate_remaining.py"), "w") as f:
        f.write(script_content)

    logger.info(f"\n📝 Second migration script created: migrate_remaining.py")


def main():
    """Main analysis function."""
    logger.info("🔍 REMAINING FILES & DIRECTORIES ANALYSIS")
    logger.info("=" * 60)

    # Analyze remaining files
    categories = analyze_remaining_files()

    # Show analysis
    show_remaining_analysis(categories)

    # Create second migration script
    create_second_migration_script(categories)

    # Summary
    total_files = sum(len(files) for files in categories.values() if isinstance(files, list) and files)
    logger.info(f"\n📊 SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Total remaining files: {total_files}")
    logger.info(
        f"Python files: {sum(len(files) for name, files in categories.items() if 'dir' not in name and isinstance(files, list))}"
    )
    logger.info(f"Directories: {len(categories['unorganized_dirs'])}")

    logger.info(f"\n🚀 Ready for second migration? Run: python migrate_remaining.py")


if __name__ == "__main__":
    main()
