#!/usr/bin/env python3
"""
Specific Functional Category Analyzer
Creates action-based, specific functional categories (not generic ones)
Example: "transcribe-analysis", "upscaler", "gallery-generator"
"""

import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from collections import Counter
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class SpecificFunctionalCategorizer:
    """
    Categorizes files into SPECIFIC functional action categories
    Not generic like "media-processing" but specific like "transcribe-analysis"
    """

    def __init__(self):
        """__init__ function."""

        # SPECIFIC ACTION-BASED CATEGORIES (not generic!)
        self.specific_categories = {
            # Audio/Video Specific Actions
            "transcribe-analysis": {
                "keywords": [
                    "transcribe",
                    "whisper",
                    "speech",
                    "stt",
                    "speech_to_text",
                    "mp3",
                    "mp4",
                    "audio_to_text",
                ],
                "imports": ["whisper", "speech_recognition", "openai.audio"],
                "functions": ["transcribe", "speech_to_text", "audio_transcription"],
                "description": "MP3/MP4 transcription and speech-to-text analysis",
            },
            "upscaler": {
                "keywords": [
                    "upscale",
                    "enhance",
                    "resolution",
                    "super_resolution",
                    "enlarge",
                    "upscaling",
                ],
                "imports": ["cv2", "PIL", "waifu2x", "esrgan"],
                "functions": ["upscale", "enhance", "increase_resolution"],
                "description": "Image/video upscaling and resolution enhancement",
            },
            "gallery-generator": {
                "keywords": [
                    "gallery",
                    "album",
                    "portfolio",
                    "photo_grid",
                    "image_gallery",
                    "html_gallery",
                ],
                "imports": ["jinja2", "pillow"],
                "functions": ["generate_gallery", "create_album", "build_portfolio"],
                "description": "HTML gallery and photo album generation",
            },
            "youtube-downloader": {
                "keywords": [
                    "youtube",
                    "yt-dlp",
                    "pytube",
                    "download_video",
                    "youtube_dl",
                ],
                "imports": ["yt_dlp", "pytube", "youtube_dl"],
                "functions": ["download_youtube", "get_video", "fetch_youtube"],
                "description": "YouTube video and audio downloading",
            },
            "instagram-bot": {
                "keywords": [
                    "instagram",
                    "instabot",
                    "instapy",
                    "ig_bot",
                    "like",
                    "follow",
                    "unfollow",
                ],
                "imports": ["instabot", "instapy", "instagram_private_api"],
                "functions": ["like_posts", "follow_user", "unfollow", "post_photo"],
                "description": "Instagram automation and bot functionality",
            },
            "telegram-bot": {
                "keywords": ["telegram", "telebot", "telegram_bot", "bot.send"],
                "imports": ["telebot", "telegram", "python-telegram-bot"],
                "functions": ["send_message", "handle_command", "bot_handler"],
                "description": "Telegram bot automation",
            },
            "twitter-bot": {
                "keywords": ["twitter", "tweepy", "tweet", "twitter_api"],
                "imports": ["tweepy", "twitter"],
                "functions": ["post_tweet", "retweet", "follow"],
                "description": "Twitter/X automation and bot functionality",
            },
            "reddit-scraper": {
                "keywords": ["reddit", "praw", "subreddit", "reddit_api"],
                "imports": ["praw"],
                "functions": ["scrape_reddit", "get_posts", "fetch_comments"],
                "description": "Reddit content scraping and data extraction",
            },
            "tiktok-downloader": {
                "keywords": ["tiktok", "tiktok_download", "tt_download"],
                "imports": ["TikTokApi"],
                "functions": ["download_tiktok", "get_video"],
                "description": "TikTok video downloading",
            },
            "web-scraper": {
                "keywords": ["scrape", "beautifulsoup", "selenium", "crawl", "spider"],
                "imports": ["beautifulsoup4", "bs4", "selenium", "scrapy"],
                "functions": ["scrape", "crawl", "extract"],
                "description": "General web scraping and data extraction",
            },
            "thumbnail-creator": {
                "keywords": ["thumbnail", "preview", "thumb", "generate_thumbnail"],
                "imports": ["PIL", "pillow"],
                "functions": ["create_thumbnail", "generate_preview", "make_thumb"],
                "description": "Thumbnail and preview image generation",
            },
            "video-editor": {
                "keywords": [
                    "edit_video",
                    "ffmpeg",
                    "moviepy",
                    "video_edit",
                    "cut",
                    "trim",
                ],
                "imports": ["moviepy", "ffmpeg"],
                "functions": ["cut_video", "trim", "concat_videos", "add_audio"],
                "description": "Video editing and manipulation",
            },
            "subtitle-handler": {
                "keywords": ["subtitle", "srt", "vtt", "caption", "subtitles"],
                "imports": ["pysrt", "webvtt"],
                "functions": ["parse_srt", "generate_subtitles", "sync_subtitles"],
                "description": "Subtitle file processing and synchronization",
            },
            "text-to-speech": {
                "keywords": ["tts", "text_to_speech", "gtts", "pyttsx", "synthesize"],
                "imports": ["gtts", "pyttsx3", "elevenlabs"],
                "functions": ["text_to_speech", "synthesize", "generate_audio"],
                "description": "Text-to-speech conversion and voice synthesis",
            },
            "image-converter": {
                "keywords": ["convert_image", "png_to_jpg", "webp", "format_convert"],
                "imports": ["PIL", "pillow"],
                "functions": ["convert_format", "png_to_jpg", "to_webp"],
                "description": "Image format conversion (PNG, JPG, WEBP, etc.)",
            },
            "video-converter": {
                "keywords": [
                    "convert_video",
                    "mp4_to_avi",
                    "transcode",
                    "format_video",
                ],
                "imports": ["ffmpeg", "moviepy"],
                "functions": ["convert_video", "transcode", "change_format"],
                "description": "Video format conversion and transcoding",
            },
            "audio-converter": {
                "keywords": ["convert_audio", "mp3_to_wav", "audio_format"],
                "imports": ["pydub", "ffmpeg"],
                "functions": ["convert_audio", "mp3_to_wav", "wav_to_mp3"],
                "description": "Audio format conversion",
            },
            "ai-image-generator": {
                "keywords": [
                    "dalle",
                    "stable_diffusion",
                    "midjourney",
                    "generate_image",
                    "text_to_image",
                ],
                "imports": ["openai", "stability_sdk", "diffusers"],
                "functions": ["generate_image", "text_to_image", "create_art"],
                "description": "AI-powered image generation using ML models",
            },
            "ai-video-generator": {
                "keywords": ["video_generation", "text_to_video", "ai_video"],
                "imports": ["runway", "synthesia"],
                "functions": ["generate_video", "text_to_video"],
                "description": "AI-powered video generation",
            },
            "image-compressor": {
                "keywords": ["compress", "optimize", "reduce_size", "tinify"],
                "imports": ["pillow", "tinify"],
                "functions": ["compress_image", "optimize", "reduce_size"],
                "description": "Image compression and optimization",
            },
            "pdf-generator": {
                "keywords": ["pdf", "reportlab", "fpdf", "generate_pdf"],
                "imports": ["reportlab", "fpdf", "pdfkit"],
                "functions": ["generate_pdf", "create_pdf", "html_to_pdf"],
                "description": "PDF generation and creation",
            },
            "excel-processor": {
                "keywords": ["excel", "xlsx", "openpyxl", "xlrd", "spreadsheet"],
                "imports": ["openpyxl", "xlrd", "xlsxwriter"],
                "functions": ["read_excel", "write_excel", "parse_xlsx"],
                "description": "Excel file processing and manipulation",
            },
            "csv-processor": {
                "keywords": ["csv", "parse_csv", "read_csv", "write_csv"],
                "imports": ["csv", "pandas"],
                "functions": ["read_csv", "write_csv", "parse_csv"],
                "description": "CSV file processing and data manipulation",
            },
            "json-processor": {
                "keywords": ["json", "parse_json", "json_dump"],
                "imports": ["json", "jsonschema"],
                "functions": ["parse_json", "dump_json", "validate_json"],
                "description": "JSON file processing and validation",
            },
            "xml-processor": {
                "keywords": ["xml", "parse_xml", "etree", "lxml"],
                "imports": ["xml.etree", "lxml"],
                "functions": ["parse_xml", "xml_to_dict"],
                "description": "XML file processing and parsing",
            },
            "api-client": {
                "keywords": ["api", "requests", "http_client", "rest_api", "api_call"],
                "imports": ["requests", "httpx", "aiohttp"],
                "functions": ["make_request", "api_call", "fetch_data"],
                "description": "API client and REST integration",
            },
            "database-manager": {
                "keywords": ["database", "sql", "mongodb", "postgres", "mysql"],
                "imports": ["sqlalchemy", "pymongo", "psycopg2", "mysql.connector"],
                "functions": ["query", "insert", "update", "delete"],
                "description": "Database operations and management",
            },
            "file-organizer": {
                "keywords": ["organize", "sort_files", "categorize", "file_manager"],
                "imports": ["os", "shutil", "pathlib"],
                "functions": ["organize_files", "sort", "categorize"],
                "description": "File organization and management",
            },
            "backup-manager": {
                "keywords": ["backup", "restore", "archive", "snapshot"],
                "imports": ["tarfile", "zipfile"],
                "functions": ["backup", "restore", "create_archive"],
                "description": "Backup creation and restoration",
            },
            "email-sender": {
                "keywords": ["email", "smtp", "send_email", "mail"],
                "imports": ["smtplib", "email"],
                "functions": ["send_email", "send_mail"],
                "description": "Email sending and automation",
            },
            "seo-optimizer": {
                "keywords": ["seo", "meta", "keywords", "optimize_seo"],
                "imports": ["beautifulsoup4"],
                "functions": ["optimize_seo", "generate_meta", "analyze_keywords"],
                "description": "SEO optimization and meta tag generation",
            },
            "markdown-converter": {
                "keywords": ["markdown", "md_to_html", "markdown_parser"],
                "imports": ["markdown", "mistune"],
                "functions": ["markdown_to_html", "parse_markdown"],
                "description": "Markdown to HTML conversion",
            },
            "code-formatter": {
                "keywords": ["format", "black", "autopep8", "prettier"],
                "imports": ["black", "autopep8"],
                "functions": ["format_code", "beautify"],
                "description": "Code formatting and beautification",
            },
            "test-runner": {
                "keywords": ["test", "pytest", "unittest", "test_"],
                "imports": ["pytest", "unittest"],
                "functions": ["test_", "setUp", "tearDown"],
                "description": "Test execution and automation",
            },
            "log-analyzer": {
                "keywords": ["log", "parse_log", "analyze_log", "logging"],
                "imports": ["logging"],
                "functions": ["parse_log", "analyze_logs"],
                "description": "Log file parsing and analysis",
            },
            "monitoring-dashboard": {
                "keywords": [
                    "monitor",
                    "dashboard",
                    "metrics",
                    "prometheus",
                    "grafana",
                ],
                "imports": ["prometheus", "flask"],
                "functions": ["collect_metrics", "monitor"],
                "description": "System monitoring and metrics dashboard",
            },
            "scheduler": {
                "keywords": ["schedule", "cron", "periodic", "scheduled_task"],
                "imports": ["schedule", "apscheduler"],
                "functions": ["schedule_task", "run_periodic"],
                "description": "Task scheduling and cron jobs",
            },
            "notification-sender": {
                "keywords": ["notify", "alert", "notification", "push"],
                "imports": ["pushbullet", "twilio"],
                "functions": ["send_notification", "alert"],
                "description": "Notification and alert sending",
            },
            "qr-generator": {
                "keywords": ["qr", "qrcode", "generate_qr"],
                "imports": ["qrcode"],
                "functions": ["generate_qr", "create_qrcode"],
                "description": "QR code generation",
            },
            "barcode-scanner": {
                "keywords": ["barcode", "scan_barcode", "read_barcode"],
                "imports": ["pyzbar"],
                "functions": ["scan_barcode", "read_barcode"],
                "description": "Barcode scanning and recognition",
            },
            "face-detector": {
                "keywords": ["face", "face_detection", "opencv", "facial_recognition"],
                "imports": ["cv2", "face_recognition"],
                "functions": ["detect_face", "recognize_face"],
                "description": "Face detection and recognition",
            },
            "ocr-processor": {
                "keywords": ["ocr", "tesseract", "text_recognition", "image_to_text"],
                "imports": ["pytesseract", "easyocr"],
                "functions": ["extract_text", "image_to_text"],
                "description": "Optical character recognition (OCR)",
            },
            "encryption-tool": {
                "keywords": ["encrypt", "decrypt", "aes", "rsa", "cryptography"],
                "imports": ["cryptography", "pycryptodome"],
                "functions": ["encrypt", "decrypt"],
                "description": "File encryption and decryption",
            },
            "password-generator": {
                "keywords": ["password", "generate_password", "random_password"],
                "imports": ["secrets", "random"],
                "functions": ["generate_password", "create_password"],
                "description": "Secure password generation",
            },
        }

    def analyze_file(self, filepath: Path) -> Optional[str]:
        """Determine specific functional category for a file"""
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")

            # Parse AST
            imports = []
            functions = []
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name.lower())
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module.lower())
                    elif isinstance(node, ast.FunctionDef):
                        functions.append(node.name.lower())
            except (ImportError, ModuleNotFoundError):
                pass

            # Convert content to lowercase for matching
            content_lower = content.lower()
            filename_lower = filepath.name.lower()

            # Score each category
            scores = {}
            for category, patterns in self.specific_categories.items():
                score = 0

                # Check keywords in content (weight: 1)
                for keyword in patterns["keywords"]:
                    if keyword.lower() in content_lower:
                        score += 1
                    if keyword.lower() in filename_lower:
                        score += 2  # Filename match is stronger

                # Check imports (weight: 3)
                for imp in patterns["imports"]:
                    if any(imp.lower() in imported for imported in imports):
                        score += 3

                # Check functions (weight: 2)
                for func in patterns["functions"]:
                    if any(func.lower() in fn for fn in functions):
                        score += 2

                if score > 0:
                    scores[category] = score

            # Return category with highest score
            if scores:
                best_category = max(scores.items(), key=lambda x: x[1])
                if best_category[1] >= 2:  # Minimum confidence threshold
                    return best_category[0]

            return None

        except Exception as e:
            return None

    def categorize_project(self, project_path: Path) -> Dict:
        """Categorize all Python files in project"""
        logger.info("🔍 Analyzing files for SPECIFIC functional categories...")

        python_files = list(project_path.rglob("*.py"))
        logger.info(f"📁 Found {len(python_files)} Python files\n")

        categorized = {}
        uncategorized = []

        for filepath in python_files:
            # Skip hidden and git files
            if any(part.startswith(".") for part in filepath.parts):
                continue

            category = self.analyze_file(filepath)

            if category:
                if category not in categorized:
                    categorized[category] = []
                categorized[category].append(str(filepath))
            else:
                uncategorized.append(str(filepath))

        # Sort by count
        categorized = dict(
            sorted(categorized.items(), key=lambda x: len(x[1]), reverse=True)
        )

        # Print results
        logger.info("📊 SPECIFIC FUNCTIONAL CATEGORIES:\n")
        for i, (category, files) in enumerate(categorized.items(), 1):
            desc = self.specific_categories[category]["description"]
            logger.info(f"{i:2d}. {category:30s} - {len(files):4d} files")
            logger.info(f"    {desc}")
            logger.info("")

        logger.info(f"❓ Uncategorized: {len(uncategorized)} files\n")

        return {
            "categorized": categorized,
            "uncategorized": uncategorized,
            "category_descriptions": {
                k: v["description"] for k, v in self.specific_categories.items()
            },
        }


def main():
    """main function."""

    project_root = Path(str(Path.home()) + "/Documents/python")

    categorizer = SpecificFunctionalCategorizer()
    results = categorizer.categorize_project(project_root)

    # Save results
    output_file = project_root / "specific_functional_categories.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    logger.info(f"✅ Results saved to: {output_file}")


if __name__ == "__main__":
    main()
