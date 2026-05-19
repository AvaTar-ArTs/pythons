#!/usr/bin/env python3
"""
Ultra-Specific Functional Categorizer
Creates action-based categories like "transcribe-analysis", "upscaler", "gallery-generator"
NOT broad categories like "image-processing" or "video-processing"
"""

import json
from datetime import datetime
from pathlib import Path

# Ultra-specific functional patterns
# Format: category_name -> (keywords, file_patterns, priority)
ULTRA_SPECIFIC_FUNCTIONS = {
    # Image-specific actions
    "upscaler": (
        ["upscale", "upscaler", "enlarge", "enhance", "super-resolution", "esrgan"],
        ["*upscale*", "*upscaler*"],
        10,
    ),
    "image-resizer": (
        ["resize", "downsize", "thumbnail", "scale", "dimension"],
        ["*resize*", "*downsize*", "*scale*"],
        9,
    ),
    "image-converter": (
        ["convert", "img2img", "format-convert", "webp", "png", "jpg"],
        ["*img2img*", "*convert*"],
        8,
    ),
    "gallery-generator": (
        ["gallery", "album", "grid", "collage", "photo-grid"],
        ["*gallery*", "*grid*", "*album*"],
        10,
    ),
    "pdf-converter": (["pdf", "pdf2img", "img2pdf", "pdf-to-image"], ["*pdf*"], 9),
    "watermark-tool": (
        ["watermark", "overlay", "logo"],
        ["*watermark*", "*overlay*"],
        8,
    ),
    # Video-specific actions
    "transcribe-analysis": (
        ["transcribe", "transcription", "whisper", "speech-to-text", "subtitle"],
        ["*transcribe*", "*whisper*", "*subtitle*"],
        10,
    ),
    "video-downloader": (
        ["download", "yt-dlp", "youtube-dl", "ytdl"],
        ["*download*", "*ytdl*", "*yt-dlp*"],
        10,
    ),
    "video-editor": (
        ["edit", "trim", "cut", "merge", "moviepy"],
        ["*edit*", "*trim*", "*cut*"],
        8,
    ),
    "video-converter": (
        ["ffmpeg", "convert", "encode", "transcode"],
        ["*ffmpeg*", "*convert*", "*encode*"],
        8,
    ),
    "thumbnail-generator": (
        ["thumbnail", "preview", "poster"],
        ["*thumbnail*", "*preview*"],
        9,
    ),
    # Audio-specific actions
    "audio-transcriber": (
        ["transcribe", "whisper", "speech"],
        ["*transcribe*", "*whisper*"],
        10,
    ),
    "audio-converter": (
        ["mp3", "wav", "audio-convert"],
        ["*audio*", "*mp3*", "*wav*"],
        8,
    ),
    "text-to-speech": (
        ["tts", "text-to-speech", "synthesize"],
        ["*tts*", "*text-to-speech*"],
        9,
    ),
    # Web-specific actions
    "web-scraper": (
        ["scrape", "scraper", "beautifulsoup", "selenium"],
        ["*scrape*", "*scraper*"],
        10,
    ),
    "api-client": (["api", "client", "request", "endpoint"], ["*api*", "*client*"], 7),
    "bot-automation": (
        ["bot", "instagram", "twitter", "facebook", "telegram"],
        ["*bot*", "*insta*", "*twitter*"],
        9,
    ),
    "html-generator": (["html", "generator", "web-page"], ["*html*", "*web*"], 8),
    # Data-specific actions
    "csv-processor": (
        ["csv", "excel", "xlsx", "spreadsheet"],
        ["*csv*", "*excel*", "*xlsx*"],
        9,
    ),
    "json-processor": (["json", "json-parser"], ["*json*"], 7),
    "database-migrator": (
        ["migrate", "migration", "sql"],
        ["*migrate*", "*migration*"],
        9,
    ),
    "data-analyzer": (
        ["analyze", "analysis", "pandas", "stats"],
        ["*analyze*", "*analysis*"],
        8,
    ),
    # Automation-specific actions
    "file-organizer": (
        ["organize", "organizer", "sort", "cleanup"],
        ["*organize*", "*organizer*", "*cleanup*"],
        9,
    ),
    "batch-processor": (["batch", "bulk", "mass-process"], ["*batch*", "*bulk*"], 8),
    "backup-tool": (["backup", "archive", "snapshot"], ["*backup*", "*archive*"], 9),
    "sync-tool": (["sync", "synchronize", "mirror"], ["*sync*", "*mirror*"], 8),
    # AI/ML-specific actions
    "ai-image-generator": (
        ["dall-e", "stable-diffusion", "midjourney", "ai-image"],
        ["*dall*", "*stable*", "*ai-image*"],
        10,
    ),
    "ai-text-generator": (
        ["gpt", "llm", "openai", "claude"],
        ["*gpt*", "*llm*", "*openai*"],
        9,
    ),
    "ai-chatbot": (["chatbot", "chat", "conversation"], ["*chatbot*", "*chat*"], 9),
    # System utilities
    "monitor-tool": (["monitor", "watch", "track"], ["*monitor*", "*watch*"], 7),
    "notification-sender": (
        ["notify", "notification", "alert"],
        ["*notify*", "*alert*"],
        8,
    ),
    "scheduler": (["schedule", "cron", "timer"], ["*schedule*", "*cron*"], 8),
}


class UltraSpecificCategorizer:
    """Categorize files by ultra-specific functional actions"""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.categorized = {}
        self.uncategorized = []

    def analyze_file(self, file_path: Path) -> str:
        """Determine ultra-specific functional category for a file"""

        filename_lower = file_path.name.lower()
        content_keywords = self._extract_keywords_from_file(file_path)

        best_match = None
        best_score = 0

        for category, (
            keywords,
            patterns,
            priority,
        ) in ULTRA_SPECIFIC_FUNCTIONS.items():
            score = 0

            # Check filename patterns
            for pattern in patterns:
                pattern_clean = pattern.replace("*", "")
                if pattern_clean in filename_lower:
                    score += priority * 2  # Filename match is strong signal

            # Check keywords in filename and content
            for keyword in keywords:
                if keyword in filename_lower:
                    score += priority
                if keyword in content_keywords:
                    score += priority * 0.5

            if score > best_score:
                best_score = score
                best_match = category

        # Require minimum confidence
        if best_score < 5:
            return None

        return best_match

    def _extract_keywords_from_file(self, file_path: Path) -> str:
        """Extract keywords from file content (first 50 lines)"""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = [f.readline() for _ in range(50)]
                return "\n".join(lines).lower()
        except:
            return ""

    def categorize_directory(self):
        """Categorize all Python files in base directory"""

        print(f"🔍 Analyzing {self.base_dir} for ultra-specific functions...")
        print()

        # Find all Python files (not in subdirectories of projects)
        python_files = []

        # Get files from broad categories we created
        broad_categories = [
            "api-development",
            "automation",
            "youtube-automation",
            "image-processing",
            "video-processing",
            "audio-processing",
            "social-media-automation",
            "content-generation",
            "data-analysis",
            "web-scraping",
            "file-utilities",
            "database",
            "utilities",
            "general-scripts",
        ]

        for category in broad_categories:
            category_path = self.base_dir / category
            if category_path.exists():
                python_files.extend(list(category_path.glob("*.py")))

        print(f"📊 Found {len(python_files)} files in broad categories")
        print()

        # Categorize each file
        for file_path in python_files:
            category = self.analyze_file(file_path)

            if category:
                if category not in self.categorized:
                    self.categorized[category] = []
                self.categorized[category].append(
                    str(file_path.relative_to(self.base_dir))
                )
            else:
                self.uncategorized.append(str(file_path.relative_to(self.base_dir)))

        # Display results
        print("✅ Categorization complete!\n")
        print(f"📁 Ultra-Specific Categories Found: {len(self.categorized)}")
        print(
            f"📄 Files Categorized: {sum(len(files) for files in self.categorized.values())}"
        )
        print(f"❓ Uncategorized: {len(self.uncategorized)}")
        print()

        # Show categories
        for category, files in sorted(
            self.categorized.items(), key=lambda x: len(x[1]), reverse=True
        ):
            print(f"   {category:<25} ({len(files)} files)")

        return self.categorized, self.uncategorized

    def save_analysis(self):
        """Save analysis to JSON file"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.base_dir / f"ultra_specific_analysis_{timestamp}.json"

        analysis = {
            "timestamp": timestamp,
            "directory": str(self.base_dir),
            "total_categories": len(self.categorized),
            "total_files_categorized": sum(
                len(files) for files in self.categorized.values()
            ),
            "uncategorized_count": len(self.uncategorized),
            "categories": {
                cat: {"files": files, "count": len(files)}
                for cat, files in self.categorized.items()
            },
            "uncategorized": self.uncategorized,
        }

        with open(output_file, "w") as f:
            json.dump(analysis, f, indent=2)

        print(f"\n💾 Saved analysis to: {output_file.name}")
        return output_file


def main():
    base_dir = Path.cwd()
    categorizer = UltraSpecificCategorizer(base_dir)

    categorized, uncategorized = categorizer.categorize_directory()
    categorizer.save_analysis()

    print("\n🎯 Ultra-Specific Functional Categories")
    print("=" * 60)
    print("\nThese are ACTION-BASED categories, not broad domains:")
    print("✅ 'upscaler' not 'image-processing'")
    print("✅ 'transcribe-analysis' not 'audio-processing'")
    print("✅ 'gallery-generator' not 'web-development'")
    print("\nThis is the ultimate context-fluid categorization!")


if __name__ == "__main__":
    main()
