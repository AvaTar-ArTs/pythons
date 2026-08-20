#!/usr/bin/env python3
"""
Second Migration Pass - Organize Remaining Python Files (Fixed Version)
"""

import shutil
from pathlib import Path


def create_additional_directories():
    """Create additional directories for remaining files."""
    base_path = Path("/Users/steven/Documents/python")
    
    additional_dirs = [
        "01_core_tools/text_processors",
        "05_audio_video/image_processors", 
        "05_audio_video/audio_processors/quiz_tts",
        "06_utilities/converters",
        "06_utilities/data_processors",
        "07_experimental/web_tools",
        "07_experimental/misc",
        "07_experimental/testing",
        "02_youtube_automation/youtube_tools",
        "02_youtube_automation/reddit_tools",
        "04_web_scraping/social_media/instagram",
        "04_web_scraping/social_media/tiktok",
        "03_ai_creative_tools/image_generation/leonardo",
        "03_ai_creative_tools/image_generation/upscaler",
        "03_ai_creative_tools/image_generation/background_removal",
        "03_ai_creative_tools/image_generation/photoshop",
        "05_audio_video/video_editors/generator",
        "05_audio_video/video_editors/sora",
        "05_audio_video/video_editors/twitch",
        "06_utilities/file_organizers/sort",
        "06_utilities/file_organizers/sorting",
        "06_utilities/file_organizers/organize",
        "06_utilities/file_organizers/python_organize",
        "06_utilities/data_processors/table_contents",
        "07_experimental/bots",
        "07_experimental/automation",
        "07_experimental/games",
        "07_experimental/ai_tools",
        "07_experimental/audio_tools",
        "07_experimental/libraries",
        "07_experimental/backup_tools",
        "07_experimental/ecommerce",
        "07_experimental/analysis_tools",
        "08_archived/backups/youtube_tools",
        "08_archived/backups/social_media",
        "08_archived/backups/ai_tools",
        "08_archived/backups/audio_tools",
        "08_archived/backups/utilities",
        "08_archived/backups/web_tools",
        "08_archived/backups/misc"
    ]
    
    for dir_path in additional_dirs:
        full_path = base_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"Created: {dir_path}")

def migrate_remaining_files():
    """Migrate remaining Python files."""
    base_path = Path("/Users/steven/Documents/python")
    
    # File mappings - only process files that exist
    file_mappings = [
        # Image Processing
        ("imgconvert_colab.py", "05_audio_video/image_processors/"),
        ("scan_images_individual.py", "05_audio_video/image_processors/"),
        ("categorize_html.py", "05_audio_video/image_processors/"),
        ("auto-image-gallery.py", "05_audio_video/image_processors/"),
        ("base_gallery_logic.py", "05_audio_video/image_processors/"),
        
        # Quiz/TTS
        ("quiz-.py", "05_audio_video/audio_processors/quiz_tts/"),
        ("quiz-tts.py", "05_audio_video/audio_processors/quiz_tts/"),
        ("tts-doc.py", "05_audio_video/audio_processors/quiz_tts/"),
        ("audio.py", "05_audio_video/audio_processors/quiz_tts/"),
        
        # Conversion Tools
        ("convert copy.py", "06_utilities/converters/"),
        ("up-down-old.py", "06_utilities/converters/"),
        ("serialize.py", "06_utilities/converters/"),
        ("convert.py", "06_utilities/converters/"),
        ("converts.py", "06_utilities/converters/"),
        
        # Gallery/HTML
        ("test_google_gallery_logic.py", "07_experimental/web_tools/"),
        ("alphabet-html-gall.py", "07_experimental/web_tools/"),
        ("htmlouts.py", "07_experimental/web_tools/"),
        
        # CSV/Data
        ("csv-output.py", "06_utilities/data_processors/"),
        ("backupcsv.py", "06_utilities/data_processors/"),
        ("csv2.py", "06_utilities/data_processors/"),
        
        # OCR Processing
        ("ocr_gpt_renamer.py", "01_core_tools/text_processors/"),
        ("text.py", "01_core_tools/text_processors/"),
        ("textgenerator.py", "01_core_tools/text_processors/"),
        
        # Cleanup
        ("cleanups.py", "06_utilities/system_tools/"),
        ("autofixer.py", "06_utilities/system_tools/"),
        ("organize.py", "06_utilities/system_tools/"),
        ("fixer.py", "06_utilities/system_tools/"),
        
        # Test Scripts
        ("trek 2.py", "07_experimental/testing/"),
        ("test.py", "07_experimental/testing/"),
        ("debug.py", "07_experimental/testing/"),
        
        # Misc
        ("y--.py", "07_experimental/misc/"),
        ("vance.py", "07_experimental/misc/"),
        ("outs.py", "07_experimental/misc/"),
        ("pythoncatorgize.py", "07_experimental/misc/")
    ]
    
    for old_name, new_dir in file_mappings:
        old_file = base_path / old_name
        new_file = base_path / new_dir / old_name
        
        if old_file.exists():
            new_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_file), str(new_file))
            print(f"Moved: {old_name} → {new_dir}")

def migrate_remaining_directories():
    """Migrate remaining directories."""
    base_path = Path("/Users/steven/Documents/python")
    
    # Directory mappings - only process directories that exist
    dir_mappings = [
        # YouTube/Video projects
        ("Youtube", "02_youtube_automation/youtube_tools/"),
        ("YTube", "02_youtube_automation/youtube_tools/"),
        ("YouTube-Bot", "02_youtube_automation/youtube_tools/"),
        ("YouTube-Viewer", "02_youtube_automation/youtube_tools/"),
        ("YouTube-Livestream-Botter", "02_youtube_automation/youtube_tools/"),
        ("youtube-uploader-main", "02_youtube_automation/youtube_tools/"),
        ("youtube_channel_downloader", "02_youtube_automation/youtube_tools/"),
        ("youtube-shorts-reddit-scraper", "02_youtube_automation/youtube_tools/"),
        ("YoutubeBot", "02_youtube_automation/youtube_tools/"),
        ("AutomatedYoutubeShorts", "02_youtube_automation/youtube_tools/"),
        ("shorts_service_mvp_v1", "02_youtube_automation/youtube_tools/"),
        
        # Social Media
        ("Instagram-Bot", "04_web_scraping/social_media/instagram/"),
        ("instagram-follower-scraper", "04_web_scraping/social_media/instagram/"),
        ("Instagram-Mass-report", "04_web_scraping/social_media/instagram/"),
        ("Instagram-mass-reporter", "04_web_scraping/social_media/instagram/"),
        ("InstagramReportBot", "04_web_scraping/social_media/instagram/"),
        ("instapy-quickstart", "04_web_scraping/social_media/instagram/"),
        ("igbot", "04_web_scraping/social_media/instagram/"),
        
        # TikTok
        ("Tiktok-Trending-Data-Scraper", "04_web_scraping/social_media/tiktok/"),
        ("tiktok-comment-liker", "04_web_scraping/social_media/tiktok/"),
        ("tiktok-generator", "04_web_scraping/social_media/tiktok/"),
        ("TikTok-Compilation-Video-Generator", "04_web_scraping/social_media/tiktok/"),
        ("tiktok-video-downloader", "04_web_scraping/social_media/tiktok/"),
        
        # Reddit
        ("reddit_video_maker", "02_youtube_automation/reddit_tools/"),
        ("reddit-text-extract", "02_youtube_automation/reddit_tools/"),
        ("reddit-to-instagram-bot", "02_youtube_automation/reddit_tools/"),
        ("redditSentiment", "02_youtube_automation/reddit_tools/"),
        ("redditVideoGenerator", "02_youtube_automation/reddit_tools/"),
        ("RedditVideoMakerBot-master", "02_youtube_automation/reddit_tools/"),
        ("Reddit-Tiktok-Video-Bot", "02_youtube_automation/reddit_tools/"),
        
        # AI/Creative
        ("leonardo", "03_ai_creative_tools/image_generation/leonardo/"),
        ("upscale-python", "03_ai_creative_tools/image_generation/upscaler/"),
        ("upscale", "03_ai_creative_tools/image_generation/upscaler/"),
        ("remove-bg-cli", "03_ai_creative_tools/image_generation/background_removal/"),
        ("photoshop-mockup-automation", "03_ai_creative_tools/image_generation/photoshop/"),
        
        # Audio/Video
        ("transcribe", "05_audio_video/transcription_tools/transcribe/"),
        ("transcribe-keywords", "05_audio_video/transcription_tools/keywords/"),
        ("videoGenerator", "05_audio_video/video_editors/generator/"),
        ("sora-video-generator", "05_audio_video/video_editors/sora/"),
        ("sora-storyboard", "05_audio_video/video_editors/sora/"),
        ("TwitchClipGenerator-main", "05_audio_video/video_editors/twitch/"),
        ("Twitch-Best-Of", "05_audio_video/video_editors/twitch/"),
        ("TwitchCompilationCreator", "05_audio_video/video_editors/twitch/"),
        ("Twitch-TikTok-Youtube-Viewbot", "05_audio_video/video_editors/twitch/"),
        ("twitchtube", "05_audio_video/video_editors/twitch/"),
        
        # Utilities
        ("Sort", "06_utilities/file_organizers/sort/"),
        ("sorting", "06_utilities/file_organizers/sorting/"),
        ("organize", "06_utilities/file_organizers/organize/"),
        ("Python-organize", "06_utilities/file_organizers/python_organize/"),
        ("tablecontentspython", "06_utilities/data_processors/table_contents/"),
        
        # Web Tools
        ("HTML-Embed-youtube-videos-on-webpage", "07_experimental/web_tools/html_embed/"),
        ("Auto-html-gallery-scripts", "07_experimental/web_tools/gallery_scripts/"),
        ("Drive-image-link-converter", "07_experimental/web_tools/drive_converter/"),
        ("download-all-the-gifs", "07_experimental/web_tools/gif_downloader/"),
        ("telegraph-image-downloader", "07_experimental/web_tools/telegraph/"),
        
        # Misc/Experimental
        ("botty", "07_experimental/bots/botty/"),
        ("007spam-BOT", "07_experimental/bots/spam_bot/"),
        ("TG-MegaBot", "07_experimental/bots/telegram/"),
        ("POD-auto", "07_experimental/automation/podcast/"),
        ("Riddle-Game", "07_experimental/games/riddle/"),
        ("prompt_pipeline", "07_experimental/ai_tools/prompt_pipeline/"),
        ("lyrics-keys-indo", "07_experimental/ai_tools/lyrics/"),
        ("ollama_gui", "07_experimental/ai_tools/ollama/"),
        ("opus_clip_open_clone", "07_experimental/ai_tools/opus_clip/"),
        ("opus_clip_v0_2_1_auto_style_NEW", "07_experimental/ai_tools/opus_clip/"),
        ("savify", "07_experimental/audio_tools/savify/"),
        ("SpotifyMP3", "07_experimental/audio_tools/spotify/"),
        ("spicetify-themes", "07_experimental/audio_tools/spicetify/"),
        ("spidy", "07_experimental/audio_tools/spidy/"),
        ("FOSS-Voice-Assistant", "07_experimental/ai_tools/voice_assistant/"),
        ("Manual Library", "07_experimental/libraries/manual/"),
        ("MDs", "07_experimental/libraries/markdown/"),
        ("docs", "09_documentation/project_docs/"),
        ("scripts", "07_experimental/scripts/"),
        ("colab", "07_experimental/colab/"),
        ("zip", "07_experimental/archives/zip/"),
        ("trashy-python", "07_experimental/misc/trashy/"),
        ("simplegallery-bin", "07_experimental/misc/simple_gallery/"),
        ("tui.editor", "07_experimental/misc/tui_editor/"),
        ("Untitled", "07_experimental/misc/untitled/"),
        
        # Archive old/backup projects
        ("env_backups", "08_archived/backups/env_backups/"),
        ("Recents", "08_archived/backups/recents/"),
        ("analysis", "08_archived/backups/analysis/"),
        ("transcript", "08_archived/backups/transcript/"),
        ("intro-typography-ShareAE.com", "08_archived/backups/typography/"),
        ("LLM-Engineers-Handbook-main", "08_archived/backups/llm_handbook/"),
        ("LLM-engineer-handbook-main", "08_archived/backups/llm_handbook_v2/"),
        ("llm-course-main", "08_archived/backups/llm_course/"),
        ("Python-and-OpenAI-main", "08_archived/backups/python_openai/"),
        ("autoblog using the ChatGPT", "08_archived/backups/autoblog/"),
        ("(Template) 600+ ChatGPT Prompts for Data Science", "08_archived/backups/chatgpt_prompts/"),
        ("Adobe Python Scripts", "08_archived/backups/adobe_scripts/"),
        ("SEO-Link-Building-Rank-in-Google-with-EDU-and-GOV-Backlinks", "08_archived/backups/seo_tools/"),
        ("rsnapshot", "08_archived/backups/rsnapshot/"),
        ("rsync-downloader", "08_archived/backups/rsync/"),
        ("rsync-macos-utility", "08_archived/backups/rsync/"),
        ("Nice-seemingly-macOS-backup-utility-based-on-rsync-called-grsyncx", "08_archived/backups/grsyncx/"),
        ("Redbubble-Auto-Uploader-stickers", "08_archived/backups/redbubble/"),
        ("redbubble.group", "08_archived/backups/redbubble/"),
        ("PrNdOwN", "08_archived/backups/prndown/"),
        ("Carbons", "08_archived/backups/carbons/"),
        ("CarbonCards", "08_archived/backups/carbons/"),
        ("fancy", "08_archived/backups/fancy/"),
        ("fancybox", "08_archived/backups/fancybox/"),
        ("htmlsve", "08_archived/backups/htmlsve/"),
        ("platypus", "08_archived/backups/platypus/"),
        ("mediasim", "08_archived/backups/mediasim/")
    ]
    
    for old_name, new_path in dir_mappings:
        old_dir = base_path / old_name
        new_dir = base_path / new_path
        
        if old_dir.exists():
            new_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_dir), str(new_dir))
            print(f"Moved: {old_name} → {new_path}")

def archive_remaining_duplicates():
    """Archive remaining duplicate files."""
    base_path = Path("/Users/steven/Documents/python")
    
    # Find and move remaining duplicate files
    duplicate_patterns = [" (1).py", " (2).py", " copy.py", " copy 2.py", " backup.py"]
    
    for pattern in duplicate_patterns:
        for file_path in base_path.glob(f"*{pattern}"):
            if file_path.is_file():
                new_path = base_path / "08_archived/old_versions" / file_path.name
                new_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(new_path))
                print(f"Archived: {file_path.name}")

def main():
    """Run second migration."""
    print("🚀 Starting Second Migration Pass")
    print("=" * 50)
    
    create_additional_directories()
    migrate_remaining_files()
    migrate_remaining_directories()
    archive_remaining_duplicates()
    
    print("\n✅ Second migration completed!")

if __name__ == "__main__":
    main()