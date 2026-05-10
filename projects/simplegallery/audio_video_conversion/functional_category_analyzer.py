#!/usr/bin/env python3
"""Functional Category Analyzer
===========================
Analyze Python scripts and categorize them by specific functional actions
rather than broad generic categories.
"""

import re
import json
import csv
import logging
import random
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Set random seed for reproducibility
random.seed(42)


class FunctionalCategoryAnalyzer:
    '\''Analyze Python scripts and categorize them by specific functional actions
    like 'transcribe-analysis', 'upscaler', 'gallery-generator', etc.
    """

    def __init__(self, python_folder_path: str):
        self.python_folder = Path(python_folder_path)
        self.output_dir = self.python_folder / "functional_analysis"
        self.output_dir.mkdir(exist_ok=True)

        # Define functional categories with specific patterns
        self.functional_categories = {
            # Audio/Video Processing
            "transcribe-analysis": {
                "patterns": [
                    r"transcrib",
                    r"whisper",
                    r"speech.*text",
                    r"audio.*text",
                    r"speech.*recognition",
                    r"voice.*text",
                    r"stt",
                    r"speech.*to.*text",
                    r"audio.*transcrib",
                    r"video.*transcrib",
                    r"mp3.*text",
                    r"mp4.*text",
                    r"subtitle.*generat",
                    r"caption.*generat",
                    r"audio.*caption",
                ],
                "keywords": [
                    "transcribe",
                    "whisper",
                    "speech",
                    "audio",
                    "voice",
                    "stt",
                    "subtitle",
                    "caption",
                ],
                "description": "Audio/video transcription and speech-to-text analysis (mp3/mp4 transcription)",
            },
            "subtitle-handler": {
                "patterns": [
                    r"subtitle.*handl",
                    r"subtitle.*process",
                    r"subtitle.*convert",
                    r"subtitle.*edit",
                    r"srt.*process",
                    r"vtt.*process",
                    r"subtitle.*sync",
                    r"subtitle.*timing",
                    r"subtitle.*extract",
                    r"subtitle.*generat",
                    r"caption.*handl",
                ],
                "keywords": ["subtitle", "srt", "vtt", "caption", "timing", "sync"],
                "description": "Subtitle file processing, conversion, and synchronization",
            },
            "youtube-downloader": {
                "patterns": [
                    r"youtube.*download",
                    r"yt.*download",
                    r"youtube.*dl",
                    r"yt.*dl",
                    r"youtube.*extract",
                    r"yt.*extract",
                    r"youtube.*grab",
                    r"yt.*grab",
                    r"youtube.*save",
                    r"yt.*save",
                    r"youtube.*get",
                    r"yt.*get",
                    r"yt-dlp",
                    r"youtube-dl",
                    r"pytube",
                    r"youtube.*api",
                ],
                "keywords": [
                    "youtube",
                    "yt",
                    "download",
                    "dl",
                    "extract",
                    "grab",
                    "yt-dlp",
                    "pytube",
                ],
                "description": "YouTube video and audio downloading",
            },
            "audio-converter": {
                "patterns": [
                    r"audio.*convert",
                    r"sound.*convert",
                    r"mp3.*convert",
                    r"wav.*convert",
                    r"audio.*transform",
                    r"sound.*transform",
                    r"audio.*chang.*format",
                    r"ffmpeg.*audio",
                    r"pydub.*convert",
                    r"audio.*format.*chang",
                ],
                "keywords": [
                    "audio",
                    "convert",
                    "mp3",
                    "wav",
                    "ffmpeg",
                    "pydub",
                    "format",
                ],
                "description": "Audio file format conversion and transformation",
            },
            "video-converter": {
                "patterns": [
                    r"video.*convert",
                    r"mp4.*convert",
                    r"avi.*convert",
                    r"mov.*convert",
                    r"video.*transform",
                    r"video.*chang.*format",
                    r"ffmpeg.*video",
                    r"opencv.*convert",
                    r"video.*format.*chang",
                    r"video.*encode",
                ],
                "keywords": [
                    "video",
                    "convert",
                    "mp4",
                    "avi",
                    "mov",
                    "ffmpeg",
                    "opencv",
                    "format",
                ],
                "description": "Video file format conversion and transformation",
            },
            # Image Processing
            "upscaler": {
                "patterns": [
                    r"upscal",
                    r"scale.*up",
                    r"enhance.*image",
                    r"super.*resolution",
                    r"image.*enlarg",
                    r"resolution.*increase",
                    r"esrgan",
                    r"real.*esrgan",
                    r"waifu2x",
                    r"image.*upscal",
                    r"photo.*upscal",
                    r"video.*upscal",
                ],
                "keywords": [
                    "upscale",
                    "enhance",
                    "resolution",
                    "esrgan",
                    "waifu2x",
                    "super-resolution",
                ],
                "description": "Image/video upscaling and resolution enhancement",
            },
            "image-converter": {
                "patterns": [
                    r"image.*convert",
                    r"photo.*convert",
                    r"jpg.*convert",
                    r"png.*convert",
                    r"image.*format.*chang",
                    r"photo.*format.*chang",
                    r"image.*transform",
                    r"pil.*convert",
                    r"opencv.*convert",
                    r"image.*chang.*format",
                ],
                "keywords": [
                    "image",
                    "convert",
                    "jpg",
                    "png",
                    "format",
                    "pil",
                    "opencv",
                ],
                "description": "Image file format conversion and transformation",
            },
            "ai-image-generator": {
                "patterns": [
                    r"ai.*image.*generat",
                    r"image.*generat.*ai",
                    r"dalle",
                    r"midjourney",
                    r"stable.*diffusion",
                    r"image.*ai",
                    r"ai.*art",
                    r"generat.*image.*ai",
                    r"diffusion.*model",
                    r"gan.*generat",
                    r"neural.*image",
                ],
                "keywords": [
                    "ai",
                    "image",
                    "generate",
                    "dalle",
                    "midjourney",
                    "stable-diffusion",
                    "gan",
                ],
                "description": "AI-powered image generation using machine learning models",
            },
            "video-generator": {
                "patterns": [
                    r"video.*generat",
                    r"generat.*video",
                    r"ai.*video",
                    r"video.*ai",
                    r"runway",
                    r"synthesia",
                    r"video.*creat.*ai",
                    r"animat.*video",
                    r"video.*synthes",
                    r"deepfake",
                    r"video.*ai.*generat",
                ],
                "keywords": [
                    "video",
                    "generate",
                    "ai",
                    "runway",
                    "synthesia",
                    "deepfake",
                    "animate",
                ],
                "description": "AI-powered video generation and animation",
            },
            "gallery-generator": {
                "patterns": [
                    r"gallery.*generat",
                    r"photo.*gallery",
                    r"image.*gallery",
                    r"web.*gallery",
                    r"html.*gallery",
                    r"thumbnails",
                    r"gallery.*html",
                    r"photo.*album",
                    r"image.*album",
                    r"gallery.*create",
                    r"html.*gallery",
                ],
                "keywords": ["gallery", "album", "thumbnails", "html", "web"],
                "description": "HTML gallery and album generation from images",
            },
            "thumbnail-creator": {
                "patterns": [
                    r"thumbnail.*creat",
                    r"thumbnail.*generat",
                    r"thumb.*creat",
                    r"thumb.*generat",
                    r"preview.*creat",
                    r"preview.*generat",
                    r"image.*thumbnail",
                    r"video.*thumbnail",
                    r"thumb.*generat",
                    r"preview.*generat",
                ],
                "keywords": ["thumbnail", "thumb", "preview", "create", "generate"],
                "description": "Thumbnail and preview creation for images and videos",
            },
            # Data Processing
            "data-analyzer": {
                "patterns": [
                    r"data.*analyz",
                    r"data.*process",
                    r"pandas.*analyz",
                    r"data.*explor",
                    r"data.*insight",
                    r"data.*visualiz",
                    r"data.*statistic",
                    r"data.*summary",
                    r"data.*report",
                    r"analyz.*data",
                ],
                "keywords": ["data", "analyze", "pandas", "numpy", "statistics"],
                "description": "Data analysis and processing",
            },
            "csv-processor": {
                "patterns": [
                    r"csv.*process",
                    r"csv.*read",
                    r"csv.*write",
                    r"csv.*convert",
                    r"csv.*analyz",
                    r"csv.*manipulat",
                    r"pandas.*csv",
                    r"csv.*export",
                    r"csv.*import",
                    r"csv.*parse",
                ],
                "keywords": ["csv", "comma", "separated"],
                "description": "CSV file processing and manipulation",
            },
            "json-processor": {
                "patterns": [
                    r"json.*process",
                    r"json.*read",
                    r"json.*write",
                    r"json.*convert",
                    r"json.*analyz",
                    r"json.*manipulat",
                    r"json.*export",
                    r"json.*import",
                    r"json.*parse",
                    r"json.*validat",
                ],
                "keywords": ["json", "javascript", "object"],
                "description": "JSON file processing and manipulation",
            },
            "excel-processor": {
                "patterns": [
                    r"excel.*process",
                    r"xlsx.*process",
                    r"xls.*process",
                    r"openpyxl",
                    r"excel.*read",
                    r"excel.*write",
                    r"excel.*convert",
                    r"spreadsheet",
                    r"workbook",
                    r"excel.*analyz",
                ],
                "keywords": ["excel", "xlsx", "xls", "openpyxl", "spreadsheet"],
                "description": "Excel file processing and manipulation",
            },
            # Web Development
            "web-scraper": {
                "patterns": [
                    r"web.*scrap",
                    r"scrap.*web",
                    r"beautifulsoup",
                    r"scrapy",
                    r"selenium",
                    r"html.*pars",
                    r"web.*crawl",
                    r"spider",
                    r"extract.*web",
                    r"web.*data",
                ],
                "keywords": ["scrape", "beautifulsoup", "scrapy", "selenium", "crawl"],
                "description": "Web scraping and data extraction",
            },
            "seo-optimizer": {
                "patterns": [
                    r"seo.*optim",
                    r"optim.*seo",
                    r"search.*engin.*optim",
                    r"seo.*analyz",
                    r"seo.*audit",
                    r"seo.*check",
                    r"seo.*score",
                    r"seo.*rank",
                    r"seo.*tool",
                    r"meta.*tag.*generat",
                    r"seo.*generat",
                    r"seo.*content",
                ],
                "keywords": ["seo", "optimize", "search", "engine", "meta", "rank"],
                "description": "SEO optimization and search engine ranking tools",
            },
            "api-client": {
                "patterns": [
                    r"api.*client",
                    r"api.*call",
                    r"requests.*api",
                    r"rest.*api",
                    r"api.*request",
                    r"api.*response",
                    r"api.*endpoint",
                    r"api.*wrapper",
                    r"api.*service",
                    r"api.*integration",
                ],
                "keywords": ["api", "rest", "requests", "endpoint", "client"],
                "description": "API client and integration",
            },
            "web-server": {
                "patterns": [
                    r"web.*server",
                    r"flask.*app",
                    r"django.*app",
                    r"fastapi.*app",
                    r"http.*server",
                    r"web.*app",
                    r"server.*app",
                    r"web.*service",
                    r"web.*endpoint",
                    r"web.*route",
                ],
                "keywords": ["flask", "django", "fastapi", "server", "http"],
                "description": "Web server and application development",
            },
            "html-generator": {
                "patterns": [
                    r"html.*generat",
                    r"html.*create",
                    r"html.*build",
                    r"html.*render",
                    r"html.*template",
                    r"html.*output",
                    r"web.*page.*generat",
                    r"html.*page",
                ],
                "keywords": ["html", "template", "render", "page"],
                "description": "HTML page and template generation",
            },
            # Machine Learning & AI
            "ml-trainer": {
                "patterns": [
                    r"model.*train",
                    r"train.*model",
                    r"machine.*learn",
                    r"ml.*train",
                    r"tensorflow.*train",
                    r"pytorch.*train",
                    r"sklearn.*train",
                    r"neural.*train",
                    r"ai.*train",
                    r"model.*fit",
                ],
                "keywords": [
                    "train",
                    "model",
                    "machine",
                    "learning",
                    "tensorflow",
                    "pytorch",
                ],
                "description": "Machine learning model training",
            },
            "ml-predictor": {
                "patterns": [
                    r"model.*predict",
                    r"predict.*model",
                    r"ml.*predict",
                    r"ai.*predict",
                    r"inference",
                    r"model.*infer",
                    r"prediction",
                    r"forecast",
                    r"model.*evaluat",
                    r"model.*test",
                ],
                "keywords": ["predict", "inference", "forecast", "evaluate"],
                "description": "Machine learning prediction and inference",
            },
            "ai-processor": {
                "patterns": [
                    r"ai.*process",
                    r"artificial.*intelligence",
                    r"neural.*network",
                    r"deep.*learn",
                    r"ai.*analyz",
                    r"ai.*generat",
                    r"ai.*classify",
                    r"ai.*recogniz",
                    r"ai.*detect",
                ],
                "keywords": ["ai", "neural", "deep", "artificial", "intelligence"],
                "description": "AI processing and analysis",
            },
            # File Management
            "file-organizer": {
                "patterns": [
                    r"file.*organiz",
                    r"organiz.*file",
                    r"file.*sort",
                    r"file.*categoriz",
                    r"file.*move",
                    r"file.*copy",
                    r"file.*rename",
                    r"file.*manag",
                    r"file.*cleanup",
                    r"file.*arrang",
                ],
                "keywords": [
                    "organize",
                    "sort",
                    "categorize",
                    "move",
                    "copy",
                    "rename",
                ],
                "description": "File organization and management",
            },
            "backup-manager": {
                "patterns": [
                    r"backup.*manag",
                    r"backup.*creat",
                    r"backup.*restor",
                    r"backup.*sync",
                    r"backup.*copy",
                    r"backup.*archiv",
                    r"backup.*compress",
                    r"backup.*store",
                ],
                "keywords": ["backup", "restore", "sync", "archive"],
                "description": "Backup creation and management",
            },
            "file-converter": {
                "patterns": [
                    r"file.*convert",
                    r"convert.*file",
                    r"format.*convert",
                    r"file.*transform",
                    r"file.*translat",
                    r"file.*chang.*format",
                    r"file.*reformat",
                ],
                "keywords": ["convert", "transform", "format", "translate"],
                "description": "File format conversion and transformation",
            },
            # Automation & Batch Processing
            "batch-processor": {
                "patterns": [
                    r"batch.*process",
                    r"process.*batch",
                    r"batch.*job",
                    r"batch.*task",
                    r"batch.*run",
                    r"batch.*execut",
                    r"batch.*autom",
                    r"batch.*workflow",
                ],
                "keywords": ["batch", "process", "job", "task", "workflow"],
                "description": "Batch processing and job automation",
            },
            "medium-automation": {
                "patterns": [
                    r"medium.*autom",
                    r"autom.*medium",
                    r"medium.*article",
                    r"medium.*post",
                    r"medium.*generat",
                    r"medium.*publish",
                    r"medium.*bot",
                    r"medium.*script",
                ],
                "keywords": ["medium", "article", "post", "publish", "automation"],
                "description": "Medium platform automation and article generation",
            },
            "instagram-bot": {
                "patterns": [
                    r"instagram.*bot",
                    r"bot.*instagram",
                    r"instagram.*autom",
                    r"instagram.*script",
                    r"instagram.*post",
                    r"instagram.*upload",
                    r"instagram.*like",
                    r"instagram.*follow",
                    r"insta.*bot",
                    r"insta.*autom",
                    r"insta.*script",
                ],
                "keywords": [
                    "instagram",
                    "insta",
                    "bot",
                    "automation",
                    "post",
                    "upload",
                ],
                "description": "Instagram automation and bot functionality",
            },
            "automation-script": {
                "patterns": [
                    r"automat",
                    r"script.*autom",
                    r"schedul.*task",
                    r"cron.*job",
                    r"task.*autom",
                    r"workflow.*autom",
                    r"process.*autom",
                    r"general.*autom",
                ],
                "keywords": ["automate", "schedule", "cron", "workflow", "general"],
                "description": "General automation and task scheduling",
            },
            # System Administration
            "system-monitor": {
                "patterns": [
                    r"system.*monitor",
                    r"monitor.*system",
                    r"system.*status",
                    r"system.*health",
                    r"system.*metric",
                    r"system.*perform",
                    r"system.*check",
                    r"system.*watch",
                ],
                "keywords": ["monitor", "status", "health", "metrics", "performance"],
                "description": "System monitoring and health checking",
            },
            "log-analyzer": {
                "patterns": [
                    r"log.*analyz",
                    r"analyz.*log",
                    r"log.*process",
                    r"log.*pars",
                    r"log.*monitor",
                    r"log.*filter",
                    r"log.*search",
                    r"log.*report",
                ],
                "keywords": ["log", "analyze", "parse", "filter", "search"],
                "description": "Log file analysis and processing",
            },
            # Database Operations
            "database-manager": {
                "patterns": [
                    r"database.*manag",
                    r"db.*manag",
                    r"sql.*manag",
                    r"database.*oper",
                    r"db.*oper",
                    r"sql.*oper",
                    r"database.*connect",
                    r"db.*connect",
                ],
                "keywords": ["database", "db", "sql", "connect", "operate"],
                "description": "Database management and operations",
            },
            "data-migrator": {
                "patterns": [
                    r"data.*migrat",
                    r"migrat.*data",
                    r"database.*migrat",
                    r"db.*migrat",
                    r"data.*transfer",
                    r"data.*mov",
                    r"data.*export.*import",
                ],
                "keywords": ["migrate", "transfer", "move", "export", "import"],
                "description": "Data migration and transfer",
            },
            # Testing & Quality
            "test-runner": {
                "patterns": [
                    r"test.*run",
                    r"run.*test",
                    r"pytest.*run",
                    r"unittest.*run",
                    r"test.*execut",
                    r"test.*autom",
                    r"test.*suite",
                    r"test.*batch",
                ],
                "keywords": ["test", "pytest", "unittest", "execute", "suite"],
                "description": "Test execution and automation",
            },
            "code-analyzer": {
                "patterns": [
                    r"code.*analyz",
                    r"analyz.*code",
                    r"code.*qualit",
                    r"code.*review",
                    r"code.*inspect",
                    r"code.*audit",
                    r"code.*check",
                    r"code.*validat",
                ],
                "keywords": ["code", "analyze", "quality", "review", "inspect"],
                "description": "Code analysis and quality assessment",
            },
            # Communication
            "email-processor": {
                "patterns": [
                    r"email.*process",
                    r"email.*send",
                    r"email.*receiv",
                    r"email.*pars",
                    r"email.*filter",
                    r"email.*analyz",
                    r"smtp",
                    r"email.*client",
                ],
                "keywords": ["email", "smtp", "mail", "message"],
                "description": "Email processing and management",
            },
            "notification-sender": {
                "patterns": [
                    r"notif.*send",
                    r"send.*notif",
                    r"alert.*send",
                    r"message.*send",
                    r"push.*notif",
                    r"slack.*notif",
                    r"discord.*notif",
                    r"webhook",
                ],
                "keywords": [
                    "notification",
                    "alert",
                    "message",
                    "push",
                    "slack",
                    "discord",
                ],
                "description": "Notification and alert sending",
            },
            # Security
            "security-scanner": {
                "patterns": [
                    r"security.*scan",
                    r"scan.*security",
                    r"vulnerabilit.*scan",
                    r"security.*check",
                    r"security.*audit",
                    r"security.*analyz",
                    r"penetration.*test",
                    r"security.*test",
                ],
                "keywords": [
                    "security",
                    "scan",
                    "vulnerability",
                    "audit",
                    "penetration",
                ],
                "description": "Security scanning and vulnerability assessment",
            },
            "encryption-tool": {
                "patterns": [
                    r"encrypt",
                    r"decrypt",
                    r"crypt",
                    r"hash",
                    r"password.*hash",
                    r"encrypt.*file",
                    r"decrypt.*file",
                    r"encrypt.*data",
                    r"decrypt.*data",
                ],
                "keywords": ["encrypt", "decrypt", "crypt", "hash", "password"],
                "description": "Encryption and decryption tools",
            },
            # Utilities
            "text-processor": {
                "patterns": [
                    r"text.*process",
                    r"process.*text",
                    r"text.*analyz",
                    r"text.*pars",
                    r"text.*clean",
                    r"text.*filter",
                    r"text.*transform",
                    r"text.*manipulat",
                ],
                "keywords": ["text", "process", "analyze", "parse", "clean"],
                "description": "Text processing and manipulation",
            },
            "url-processor": {
                "patterns": [
                    r"url.*process",
                    r"process.*url",
                    r"url.*pars",
                    r"url.*validat",
                    r"url.*shorten",
                    r"url.*expand",
                    r"url.*analyz",
                    r"url.*manipulat",
                ],
                "keywords": ["url", "link", "shorten", "expand", "validate"],
                "description": "URL processing and manipulation",
            },
            "config-manager": {
                "patterns": [
                    r"config.*manag",
                    r"manag.*config",
                    r"config.*load",
                    r"config.*save",
                    r"config.*pars",
                    r"config.*validat",
                    r"settings.*manag",
                    r"config.*file",
                ],
                "keywords": ["config", "settings", "configuration", "load", "save"],
                "description": "Configuration management and processing",
            },
        }

    def analyze_file_functionality(self, file_path: Path) -> dict:
        """Analyze a single file to determine its functional category"""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
        except (OSError, UnicodeDecodeError, PermissionError) as e:
            return {
                "error": f"Could not read file: {e!s}",
                "file_path": str(file_path),
            }

        # Basic file info
        file_info = {
            "file_path": str(file_path),
            "file_name": file_path.name,
            "file_size": file_path.stat().st_size,
            "line_count": len(content.splitlines()),
            "analysis_timestamp": datetime.now().isoformat(),
        }

        # Analyze content for functional patterns
        content_lower = content.lower()
        file_name_lower = file_path.name.lower()

        # Score each category
        category_scores = {}
        matched_patterns = {}

        for category, config in self.functional_categories.items():
            score = 0
            matched = []

            # Check patterns
            for pattern in config["patterns"]:
                try:
                    matches = re.findall(pattern, content_lower, re.IGNORECASE)
                    if matches:
                        score += len(matches) * 2  # Pattern matches are weighted higher
                        matched.extend(matches)
                except (re.error, TypeError):
                    # Skip invalid regex patterns
                    continue

            # Check keywords
            for keyword in config["keywords"]:
                if keyword in content_lower:
                    score += 1
                    matched.append(keyword)

            # Check filename
            for keyword in config["keywords"]:
                if keyword in file_name_lower:
                    score += 3  # Filename matches are weighted highest
                    matched.append(f"filename:{keyword}")

            if score > 0:
                category_scores[category] = score
                matched_patterns[category] = list(set(matched))

        # Determine primary category
        if category_scores:
            primary_category = max(category_scores, key=category_scores.get)
            primary_score = category_scores[primary_category]
        else:
            primary_category = "uncategorized"
            primary_score = 0

        # Get secondary categories (score > 1)
        secondary_categories = {
            cat: score
            for cat, score in category_scores.items()
            if cat != primary_category and score > 1
        }

        file_info.update(
            {
                "primary_category": primary_category,
                "primary_score": primary_score,
                "secondary_categories": secondary_categories,
                "matched_patterns": matched_patterns,
                "category_description": self.functional_categories.get(
                    primary_category,
                    {},
                ).get("description", "No description available"),
                "all_category_scores": category_scores,
            },
        )

        return file_info

    def analyze_python_folder(self) -> dict:
        """Analyze all Python files in the folder"""
        logger.info("🔍 Analyzing Python files for functional categories...")

        analysis_results = {
            "timestamp": datetime.now().isoformat(),
            "folder_path": str(self.python_folder),
            "analysis_type": "functional_category_analysis",
            "files_analyzed": [],
            "category_summary": {},
            "category_distribution": {},
            "insights": {},
        }

        # Find all Python files
        python_files = list(self.python_folder.rglob("*.py"))
        logger.info(f"📁 Found {len(python_files)} Python files to analyze")

        # Analyze each file
        for file_path in python_files:
            if self._should_analyze_file(file_path):
                file_analysis = self.analyze_file_functionality(file_path)
                analysis_results["files_analyzed"].append(file_analysis)

        # Generate summary statistics
        analysis_results["category_summary"] = self._generate_category_summary(
            analysis_results["files_analyzed"],
        )
        analysis_results["category_distribution"] = (
            self._generate_category_distribution(analysis_results["files_analyzed"])
        )
        analysis_results["insights"] = self._generate_insights(analysis_results)

        return analysis_results

    def _should_analyze_file(self, file_path: Path) -> bool:
        """Determine if file should be analyzed"""
        skip_patterns = ["__pycache__", ".git", "venv", "env", ".pytest_cache"]
        return not any(pattern in str(file_path) for pattern in skip_patterns)

    def _generate_category_summary(self, files_analyzed: list) -> dict:
        """Generate summary of categories found"""
        category_counts = Counter()
        category_files = defaultdict(list)

        for file_info in files_analyzed:
            if "error" not in file_info:
                primary_category = file_info.get("primary_category", "uncategorized")
                category_counts[primary_category] += 1
                category_files[primary_category].append(
                    {
                        "file_name": file_info["file_name"],
                        "file_path": file_info["file_path"],
                        "score": file_info.get("primary_score", 0),
                    },
                )

        # Sort by count
        sorted_categories = category_counts.most_common()

        summary = {}
        for category, count in sorted_categories:
            summary[category] = {
                "count": count,
                "percentage": (
                    (count / len(files_analyzed)) * 100 if files_analyzed else 0
                ),
                "description": self.functional_categories.get(category, {}).get(
                    "description",
                    "No description",
                ),
                "files": category_files[category],
            }

        return summary

    def _generate_category_distribution(self, files_analyzed: list) -> dict:
        """Generate category distribution statistics"""
        total_files = len([f for f in files_analyzed if "error" not in f])

        if total_files == 0:
            return {}

        # Count primary categories
        primary_categories = Counter()
        secondary_categories = Counter()

        for file_info in files_analyzed:
            if "error" not in file_info:
                primary_cat = file_info.get("primary_category", "uncategorized")
                primary_categories[primary_cat] += 1

                # Count secondary categories
                for sec_cat in file_info.get("secondary_categories", {}):
                    secondary_categories[sec_cat] += 1

        return {
            "total_files": total_files,
            "primary_categories": dict(primary_categories),
            "secondary_categories": dict(secondary_categories),
            "most_common_primary": (
                primary_categories.most_common(1)[0] if primary_categories else None
            ),
            "most_common_secondary": (
                secondary_categories.most_common(1)[0] if secondary_categories else None
            ),
        }

    def _generate_insights(self, analysis_results: dict) -> dict:
        """Generate insights from the analysis"""
        files_analyzed = analysis_results["files_analyzed"]
        category_summary = analysis_results["category_summary"]

        insights = {
            "total_files_analyzed": len(
                [f for f in files_analyzed if "error" not in f],
            ),
            "categories_found": len(category_summary),
            "most_common_category": (
                max(category_summary.items(), key=lambda x: x[1]["count"])
                if category_summary
                else None
            ),
            "uncategorized_files": category_summary.get("uncategorized", {}).get(
                "count",
                0,
            ),
            "high_confidence_files": len(
                [f for f in files_analyzed if f.get("primary_score", 0) > 5],
            ),
            "category_diversity": len(
                [cat for cat, data in category_summary.items() if data["count"] > 0],
            ),
            "recommendations": self._generate_recommendations(category_summary),
        }

        return insights

    def _generate_recommendations(self, category_summary: dict) -> list:
        """Generate recommendations based on analysis'\''
        recommendations = []

        # Check for uncategorized files
        uncategorized = category_summary.get("uncategorized", {}).get("count", 0)
        if uncategorized > 0:
            recommendations.append(
                f"Review {uncategorized} uncategorized files for better organization",
            )

        # Check for dominant categories
        if category_summary:
            most_common = max(category_summary.items(), key=lambda x: x[1]["count"])
            if most_common[1]["count"] > 10:
                recommendations.append(
                    f"Consider creating a dedicated folder for '{most_common[0]}' files ({most_common[1]['count']} files)",
                )

        # Check for low-confidence files
        recommendations.append(
            "Review files with low confidence scores for better categorization",
        )

        return recommendations

    def save_analysis_results(self, analysis_results: dict) -> None:
        """Save analysis results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save JSON results
        json_file = self.output_dir / f"functional_analysis_{timestamp}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(analysis_results, f, indent=2, default=str)

        # Save CSV summary
        csv_file = self.output_dir / f"functional_summary_{timestamp}.csv"
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Category", "Count", "Percentage", "Description", "Files"])

            for category, data in analysis_results["category_summary"].items():
                files_list = ", ".join(
                    [f["file_name"] for f in data["files"][:5]],
                )  # First 5 files
                if len(data["files"]) > 5:
                    files_list += f" ... and {len(data['files']) - 5} more"

                writer.writerow(
                    [
                        category,
                        data["count"],
                        f"{data['percentage']:.1f}%",
                        data["description"],
                        files_list,
                    ],
                )

        # Save detailed file analysis
        detailed_csv = self.output_dir / f"functional_files_{timestamp}.csv"
        with open(detailed_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "File Name",
                    "File Path",
                    "Primary Category",
                    "Primary Score",
                    "Secondary Categories",
                    "Matched Patterns",
                    "Description",
                ],
            )

            for file_info in analysis_results["files_analyzed"]:
                if "error" not in file_info:
                    secondary_cats = ", ".join(
                        file_info.get("secondary_categories", {}).keys(),
                    )
                    matched_patterns = ", ".join(
                        file_info.get("matched_patterns", {}).get(
                            file_info.get("primary_category", ""),
                            [],
                        )[:3],
                    )

                    writer.writerow(
                        [
                            file_info["file_name"],
                            file_info["file_path"],
                            file_info.get("primary_category", "uncategorized"),
                            file_info.get("primary_score", 0),
                            secondary_cats,
                            matched_patterns,
                            file_info.get("category_description", ""),
                        ],
                    )

        logger.info("💾 Analysis results saved:")
        logger.info(f"   📄 JSON: {json_file}")
        logger.info(f"   📊 Summary CSV: {csv_file}")
        logger.info(f"   📋 Detailed CSV: {detailed_csv}")

    def run_analysis(self) -> dict:
        """Run the complete functional category analysis"""
        logger.info("🚀 Starting Functional Category Analysis...")
        logger.info("=" * 60)

        # Perform analysis
        analysis_results = self.analyze_python_folder()

        # Save results
        self.save_analysis_results(analysis_results)

        # Print summary
        self._print_summary(analysis_results)

        return analysis_results

    def _print_summary(self, analysis_results: dict):
        """Print analysis summary"""
        logger.info("\n" + "=" * 60)
        logger.info("📊 FUNCTIONAL CATEGORY ANALYSIS SUMMARY")
        logger.info("=" * 60)

        insights = analysis_results["insights"]
        category_summary = analysis_results["category_summary"]

        logger.info(f"\n📁 Files Analyzed: {insights['total_files_analyzed']}")
        logger.info(f"🏷️  Categories Found: {insights['categories_found']}")
        logger.info(f"🎯 Category Diversity: {insights['category_diversity']}")
        logger.info(f"❓ Uncategorized Files: {insights['uncategorized_files']}")
        logger.info(f"✅ High Confidence Files: {insights['high_confidence_files']}")

        logger.info("\n🏆 TOP CATEGORIES:")
        for i, (category, data) in enumerate(list(category_summary.items())[:10], 1):
            logger.info(
                f"   {i:2d}. {category:<20} - {data['count']:3d} files "
                f"({data['percentage']:5.1f}%)",
            )
            logger.info(f"       {data['description']}")

        if insights["recommendations"]:
            logger.info("\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(insights["recommendations"], 1):
                logger.info(f"   {i}. {rec}")

        logger.info(
            "\n✅ Analysis complete! Check the 'functional_analysis' folder "
            "for detailed results.",
        )


def main():
    """Main function to run functional category analysis"""
    python_folder = Path.home() / "Documents" / "python"

    if not python_folder.exists():
        logger.error(f"❌ Python folder not found: {python_folder}")
        return

    logger.info("🏷️  Functional Category Analyzer")
    logger.info("=" * 60)
    logger.info("Categorizing Python scripts by specific functional actions")
    logger.info(f"📁 Analyzing folder: {python_folder}")

    # Create analyzer
    analyzer = FunctionalCategoryAnalyzer(str(python_folder))

    # Run analysis
    results = analyzer.run_analysis()

    logger.info("\n✅ Functional category analysis complete!")


if __name__ == "__main__":
    main()
