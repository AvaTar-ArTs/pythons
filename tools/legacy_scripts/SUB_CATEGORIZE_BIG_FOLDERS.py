#!/usr/bin/env python3
"""
🗂️  SUB-CATEGORIZE BIG FOLDERS
Break down folders with 500+ direct files into logical subcategories
"""

import re
import shutil
from pathlib import Path
from collections import defaultdict

class SubCategorizer:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)
        self.moves = defaultdict(list)

    def categorize_content_creation(self):
        """Sub-categorize content_creation/ (1,555 direct files!)"""
        print("📝 ANALYZING content_creation/ (1,555 files)...\n")

        folder = self.pythons_dir / 'content_creation'
        files = [f for f in folder.glob('*.py') if f.is_file()]

        categories = defaultdict(list)

        for f in files:
            name = f.name.lower()

            # AI/LLM
            if any(x in name for x in ['gpt', 'claude', 'openai', 'anthropic', 'llm', 'ai-', 'gemini']):
                categories['ai_tools'].append(f)
            # Text/Writing
            elif any(x in name for x in ['text', 'write', 'article', 'blog', 'content', 'seo']):
                categories['text_tools'].append(f)
            # Image
            elif any(x in name for x in ['image', 'photo', 'img', 'picture', 'vision', 'dalle', 'leonardo']):
                categories['image_tools'].append(f)
            # Video
            elif any(x in name for x in ['video', 'mp4', 'movie', 'youtube', 'shorts']):
                categories['video_tools'].append(f)
            # Audio
            elif any(x in name for x in ['audio', 'sound', 'music', 'tts', 'speech']):
                categories['audio_tools'].append(f)
            # Social Media
            elif any(x in name for x in ['instagram', 'twitter', 'facebook', 'reddit', 'social', 'tiktok']):
                categories['social_media'].append(f)
            # Automation/Bots
            elif any(x in name for x in ['bot', 'automat', 'schedule', 'workflow']):
                categories['automation'].append(f)
            # Data/Analysis
            elif any(x in name for x in ['data', 'csv', 'json', 'analyze', 'report']):
                categories['data_tools'].append(f)
            # Web/API
            elif any(x in name for x in ['api', 'web', 'scrape', 'crawl', 'request']):
                categories['web_tools'].append(f)
            # Misc
            else:
                categories['misc'].append(f)

        self.moves['content_creation'] = categories

        print("  Sub-categories:")
        for cat, files in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"    {cat:25} {len(files):4} files")

        return categories

    def categorize_utilities(self):
        """Sub-categorize utilities/ (986 direct files!)"""
        print("\n🛠️  ANALYZING utilities/ (986 files)...\n")

        folder = self.pythons_dir / 'utilities'
        files = [f for f in folder.glob('*.py') if f.is_file()]

        categories = defaultdict(list)

        for f in files:
            name = f.name.lower()

            # File operations
            if any(x in name for x in ['file', 'rename', 'move', 'copy', 'delete', 'organize', 'sort']):
                categories['file_ops'].append(f)
            # Data/CSV
            elif any(x in name for x in ['csv', 'json', 'xml', 'data', 'parse']):
                categories['data_ops'].append(f)
            # API/Web
            elif any(x in name for x in ['api', 'request', 'client', 'http', 'web']):
                categories['api_clients'].append(f)
            # Text processing
            elif any(x in name for x in ['text', 'string', 'regex', 'format']):
                categories['text_utils'].append(f)
            # Media
            elif any(x in name for x in ['image', 'video', 'audio', 'media', 'convert']):
                categories['media_utils'].append(f)
            # System
            elif any(x in name for x in ['system', 'process', 'monitor', 'backup', 'config']):
                categories['system_utils'].append(f)
            # Development
            elif any(x in name for x in ['test', 'debug', 'lint', 'check', 'validate']):
                categories['dev_utils'].append(f)
            # Helpers
            else:
                categories['helpers'].append(f)

        self.moves['utilities'] = categories

        print("  Sub-categories:")
        for cat, files in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"    {cat:25} {len(files):4} files")

        return categories

    def categorize_audio_video_conversion(self):
        """Sub-categorize audio_video_conversion/ (510 direct files!)"""
        print("\n🎬 ANALYZING audio_video_conversion/ (510 files)...\n")

        folder = self.pythons_dir / 'audio_video_conversion'
        files = [f for f in folder.glob('*.py') if f.is_file()]

        categories = defaultdict(list)

        for f in files:
            name = f.name.lower()

            # Audio conversion
            if any(x in name for x in ['mp3', 'wav', 'audio', 'sound', 'music']):
                if 'to' in name or 'convert' in name:
                    categories['audio_converters'].append(f)
                else:
                    categories['audio_tools'].append(f)
            # Video conversion
            elif any(x in name for x in ['mp4', 'video', 'mov', 'avi']):
                if 'to' in name or 'convert' in name:
                    categories['video_converters'].append(f)
                else:
                    categories['video_tools'].append(f)
            # FFmpeg
            elif 'ffmpeg' in name:
                categories['ffmpeg_tools'].append(f)
            # Transcoding
            elif any(x in name for x in ['transcode', 'encode', 'compress']):
                categories['transcoders'].append(f)
            # Misc
            else:
                categories['other'].append(f)

        self.moves['audio_video_conversion'] = categories

        print("  Sub-categories:")
        for cat, files in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"    {cat:25} {len(files):4} files")

        return categories

    def execute_subcategorization(self):
        """Execute the sub-categorization"""
        print("\n" + "=" * 70)
        print("🚀 EXECUTING SUB-CATEGORIZATION")
        print("=" * 70 + "\n")

        total_moved = 0

        for main_folder, categories in self.moves.items():
            main_path = self.pythons_dir / main_folder

            print(f"📁 {main_folder}/")

            for subcat, files in categories.items():
                if not files:
                    continue

                # Create subcategory
                subcat_path = main_path / subcat
                subcat_path.mkdir(exist_ok=True)

                moved = 0
                for f in files:
                    target = subcat_path / f.name

                    if target.exists():
                        continue

                    try:
                        shutil.move(str(f), str(target))
                        moved += 1
                    except Exception as e:
                        print(f"   ❌ Error: {f.name} - {e}")

                if moved > 0:
                    print(f"   ✅ {subcat:30} {moved:4} files")
                    total_moved += moved

            print()

        print("=" * 70)
        print(f"✅ TOTAL: Moved {total_moved} files into subcategories")
        print("=" * 70)

        return total_moved


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     🗂️  SUB-CATEGORIZE BIG FOLDERS                               ║
║     Break down 500-2000 file folders into logical groups         ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    sub = SubCategorizer()

    # Analyze each big folder
    sub.categorize_content_creation()
    sub.categorize_utilities()
    sub.categorize_audio_video_conversion()

    print("\n" + "=" * 70)
    print("📊 EXPECTED RESULT")
    print("=" * 70)
    print("\nBEFORE:")
    print("  content_creation/        1,555 direct files (CHAOS!)")
    print("  utilities/                 986 direct files (MESS!)")
    print("  audio_video_conversion/    510 direct files (TOO MANY!)")
    print("\nAFTER:")
    print("  content_creation/")
    print("    ├── ai_tools/           ~300 files")
    print("    ├── text_tools/         ~400 files")
    print("    ├── image_tools/        ~200 files")
    print("    ├── video_tools/        ~200 files")
    print("    └── [8 more subcategories]")
    print("\n  utilities/")
    print("    ├── file_ops/           ~250 files")
    print("    ├── data_ops/           ~200 files")
    print("    ├── api_clients/        ~150 files")
    print("    └── [5 more subcategories]")
    print("\n  audio_video_conversion/")
    print("    ├── audio_converters/   ~200 files")
    print("    ├── video_converters/   ~150 files")
    print("    └── [3 more subcategories]")
    print("=" * 70)

    confirm = input("\nType 'SUBCATEGORIZE' to execute: ")

    if confirm == 'SUBCATEGORIZE':
        sub.execute_subcategorization()
        print("\n✅ Sub-categorization complete!")
    else:
        print("\n❌ Cancelled")


if __name__ == "__main__":
    main()

