#!/usr/bin/env python3
"""Comprehensive Directory Analyzer
Analyzes ALL directories and files in ~/Documents/python
Identifies well-named vs poorly-named directories
Suggests consolidations and reorganization
"""

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple


class ComprehensiveAnalyzer:
    """Analyze entire python directory structure"""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.directories = []
        self.loose_files = []
        self.well_named = []  # Already action-based directories
        self.poorly_named = []  # Generic or unclear directories
        self.redundant_groups = defaultdict(list)  # Similar directories to consolidate

        # Ultra-specific action patterns
        self.action_patterns = {
            "upscaler",
            "upscale",
            "transcribe",
            "transcription",
            "downloader",
            "download",
            "converter",
            "convert",
            "generator",
            "generate",
            "editor",
            "edit",
            "analyzer",
            "analyze",
            "processor",
            "process",
            "scraper",
            "scrape",
            "organizer",
            "organize",
            "automation",
            "automate",
            "creator",
            "create",
            "maker",
            "make",
            "builder",
            "build",
        }

        # Generic/poor names to avoid
        self.generic_patterns = {
            "tools",
            "utils",
            "utilities",
            "scripts",
            "apps",
            "projects",
            "misc",
            "other",
            "temp",
            "test",
            "experimental",
            "examples",
            "archive",
            "backup",
            "old",
            "new",
            "stuff",
        }

    def analyze_directory_name(self, dir_name: str) -> tuple[str, str]:
        """Classify directory name quality

        Returns:
            (quality, reason) where quality is 'excellent', 'good', 'poor', or 'terrible'
        """
        name_lower = dir_name.lower()

        # Terrible: single character, numbers only, or generic trash
        if len(dir_name) <= 2 or dir_name.isdigit():
            return ("terrible", "Single char or numeric directory")

        # Check for generic patterns
        for generic in self.generic_patterns:
            if generic in name_lower:
                return ("poor", f"Contains generic term: {generic}")

        # Excellent: Contains specific action verb
        for action in self.action_patterns:
            if action in name_lower:
                return ("excellent", f'Action-based: contains "{action}"')

        # Good: Descriptive, specific purpose
        if "-" in dir_name or "_" in dir_name:
            parts = dir_name.replace("_", "-").split("-")
            if len(parts) >= 2:
                return ("good", "Multi-part descriptive name")

        # Poor: Single word without clear action
        if "-" not in dir_name and "_" not in dir_name:
            return ("poor", "Single word, no clear action")

        return ("good", "Descriptive name")

    def find_redundant_directories(self):
        """Find directories that could be consolidated"""
        # Group by functional similarity
        function_groups = {
            "video-download": [
                "youtube-downloader",
                "video-downloader",
                "tiktok-video-downloader",
                "Auto-YouTube",
                "youtube-python",
                "scrape-youtube-channel-videos-url",
            ],
            "image-upscale": ["upscaler", "upscale-python"],
            "video-generate": [
                "video-generator",
                "videoGenerator",
                "Automatic-Video-Generator-for-youtube",
                "reddit_video_maker",
                "RedditVideoMakerBot-master",
                "redditVideoGenerator",
                "TikTok-Compilation-Video-Generator",
                "tiktok-generator",
            ],
            "bot-social": [
                "Instagram-Bot",
                "instagram-follower-scraper",
                "InstagramReportBot",
                "InstaReport",
                "Instagram-Mass-report",
                "botty",
                "FB-Script-Auto-Post-All-Group",
            ],
            "transcription": [
                "transcribe-analysis",
                "transcription_analyzer",
                "audio-transcriber",
            ],
            "gallery": [
                "gallery-generator",
                "simplegallery",
                "simplegallery-bin",
                "netlify-gallery-deployer",
            ],
            "ai-text": ["ai-text-generator", "Python-and-OpenAI-main"],
            "ai-image": ["ai-image-generator", "ai-comic-factory"],
            "file-organize": ["file-organizer", "Python-organize", "clean-organizer"],
            "backup": ["backup-tool", "archive-utility"],
            "thumbnail": ["thumbnail-generator", "thumbnail-creator"],
            "web-scrape": [
                "web-scraper",
                "web-scraping",
                "web_scraping",
                "selenium-image-scraper",
                "fiverr-scraping-api",
            ],
            "reddit": [
                "reddit_video_maker",
                "reddit-text-extract",
                "Reddit-Tiktok-Video-Bot",
                "reddit-to-instagram-bot",
            ],
            "podcast": ["podcast_to_video_v2"],
            "redbubble": [
                "Redbubble-Auto-Uploader-stickers",
                "redbubble.group",
                "POD-auto",
            ],
            "seo": [
                "seo-optimizer",
                "SEO-Link-Building-Rank-in-Google-with-EDU-and-GOV-Backlinks",
            ],
        }

        return function_groups

    def scan_directory(self):
        """Scan entire directory structure"""
        print("🔍 Scanning ~/Documents/python directory structure...")
        print()

        # Get all subdirectories
        for item in self.base_dir.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                self.directories.append(item.name)

        # Get all loose files in root
        for item in self.base_dir.iterdir():
            if item.is_file() and not item.name.startswith("."):
                self.loose_files.append(item.name)

        print(f"📁 Found {len(self.directories)} directories")
        print(f"📄 Found {len(self.loose_files)} loose files in root")
        print()

    def classify_directories(self):
        """Classify all directories by name quality"""
        print("📊 Classifying directory names...")
        print()

        excellent = []
        good = []
        poor = []
        terrible = []

        for dir_name in sorted(self.directories):
            quality, reason = self.analyze_directory_name(dir_name)

            if quality == "excellent":
                excellent.append((dir_name, reason))
            elif quality == "good":
                good.append((dir_name, reason))
            elif quality == "poor":
                poor.append((dir_name, reason))
            else:  # terrible
                terrible.append((dir_name, reason))

        self.well_named = excellent + good
        self.poorly_named = poor + terrible

        print(f"✅ Excellent (action-based): {len(excellent)}")
        print(f"👍 Good (descriptive): {len(good)}")
        print(f"⚠️  Poor (generic/unclear): {len(poor)}")
        print(f"❌ Terrible (meaningless): {len(terrible)}")
        print()

        return {
            "excellent": excellent,
            "good": good,
            "poor": poor,
            "terrible": terrible,
        }

    def generate_report(self):
        """Generate comprehensive analysis report"""
        self.scan_directory()
        classification = self.classify_directories()
        redundant_groups = self.find_redundant_directories()

        print("=" * 70)
        print("📋 COMPREHENSIVE DIRECTORY ANALYSIS REPORT")
        print("=" * 70)
        print()

        # Excellent directories
        if classification["excellent"]:
            print("✅ EXCELLENT - Action-Based Directories (Keep as-is)")
            print("-" * 70)
            for dir_name, reason in classification["excellent"][:20]:
                print(f"   {dir_name:<50} {reason}")
            if len(classification["excellent"]) > 20:
                print(f"   ... and {len(classification['excellent']) - 20} more")
            print()

        # Terrible directories (to remove/rename)
        if classification["terrible"]:
            print("❌ TERRIBLE - Meaningless Directories (Remove or Rename)")
            print("-" * 70)
            for dir_name, reason in classification["terrible"]:
                print(f"   {dir_name:<50} {reason}")
            print()

        # Poor directories
        if classification["poor"]:
            print("⚠️  POOR - Generic/Unclear Directories (Consider Renaming)")
            print("-" * 70)
            for dir_name, reason in classification["poor"][:15]:
                print(f"   {dir_name:<50} {reason}")
            if len(classification["poor"]) > 15:
                print(f"   ... and {len(classification['poor']) - 15} more")
            print()

        # Redundant groups
        print("🔄 REDUNDANT DIRECTORIES - Candidates for Consolidation")
        print("-" * 70)
        for group_name, dirs in redundant_groups.items():
            existing_dirs = [d for d in dirs if d in self.directories]
            if len(existing_dirs) > 1:
                print(f"\n   {group_name.upper()}:")
                for dir_name in existing_dirs:
                    print(f"      → {dir_name}")
        print()

        # Loose files summary
        print("📄 LOOSE FILES IN ROOT")
        print("-" * 70)

        by_extension = defaultdict(int)
        for filename in self.loose_files:
            ext = Path(filename).suffix or "no-extension"
            by_extension[ext] += 1

        for ext, count in sorted(
            by_extension.items(), key=lambda x: x[1], reverse=True,
        ):
            print(f"   {ext:<20} {count:>3} files")
        print(f"\n   TOTAL: {len(self.loose_files)} loose files")
        print()

        return {
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "total_directories": len(self.directories),
            "total_loose_files": len(self.loose_files),
            "classification": classification,
            "redundant_groups": {
                k: v
                for k, v in redundant_groups.items()
                if len([d for d in v if d in self.directories]) > 1
            },
            "loose_files_by_type": dict(by_extension),
        }

    def save_report(self, report_data: dict):
        """Save report to JSON"""
        timestamp = report_data["timestamp"]
        output_file = self.base_dir / f"comprehensive_analysis_{timestamp}.json"

        with open(output_file, "w") as f:
            json.dump(report_data, f, indent=2)

        print(f"💾 Saved detailed report to: {output_file.name}")
        return output_file


def main():
    base_dir = Path("/Users/steven/Documents/python")

    analyzer = ComprehensiveAnalyzer(base_dir)
    report_data = analyzer.generate_report()
    analyzer.save_report(report_data)

    print()
    print("=" * 70)
    print("🎯 SUMMARY")
    print("=" * 70)
    print(f"   Total directories: {report_data['total_directories']}")
    print(
        f"   Excellent/Good: {len(report_data['classification']['excellent']) + len(report_data['classification']['good'])}",
    )
    print(f"   Poor: {len(report_data['classification']['poor'])}")
    print(f"   Terrible: {len(report_data['classification']['terrible'])}")
    print(f"   Redundant groups: {len(report_data['redundant_groups'])}")
    print(f"   Loose files: {report_data['total_loose_files']}")
    print()
    print("Next steps:")
    print("1. Review terrible directories - remove or rename")
    print("2. Consolidate redundant directory groups")
    print("3. Organize loose root files")
    print("4. Consider renaming poor directories")


if __name__ == "__main__":
    main()
