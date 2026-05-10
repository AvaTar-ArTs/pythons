#!/usr/bin/env python3
"""
🧠 SMART SUB-CATEGORIZER
Use AST analysis and content intelligence to properly categorize the "misc" folders
"""

import ast
import re
from pathlib import Path
from collections import defaultdict
import shutil


class SmartSubCategorizer:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)

    def analyze_file_deeply(self, filepath):
        """Deep analysis using AST and content"""
        score = defaultdict(int)

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            content_lower = content.lower()
            filename = filepath.name.lower()

            # Parse AST for imports
            try:
                tree = ast.parse(content)
                imports = []

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name.split(".")[0])
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module.split(".")[0])

                # Score based on imports
                import_scores = {
                    "openai": {"ai_llm": 20, "chatgpt": 15},
                    "anthropic": {"ai_llm": 20, "claude": 15},
                    "streamlit": {"web_apps": 20, "dashboards": 15},
                    "flask": {"web_apps": 15, "api": 10},
                    "fastapi": {"web_apps": 15, "api": 15},
                    "selenium": {"web_automation": 20, "scraping": 15},
                    "playwright": {"web_automation": 20, "scraping": 15},
                    "beautifulsoup": {"scraping": 20, "web_parsing": 15},
                    "requests": {"api_clients": 10, "web": 5},
                    "pandas": {"data_analysis": 15, "csv_tools": 10},
                    "numpy": {"data_analysis": 10, "scientific": 10},
                    "PIL": {"image_processing": 20, "graphics": 10},
                    "cv2": {"image_processing": 20, "computer_vision": 15},
                    "moviepy": {"video_editing": 20, "video_tools": 15},
                    "pydub": {"audio_editing": 20, "audio_tools": 15},
                    "whisper": {"transcription": 20, "audio_to_text": 15},
                    "elevenlabs": {"tts": 20, "voice_synthesis": 15},
                    "instapy": {"instagram": 20, "social_media": 10},
                    "tweepy": {"twitter": 20, "social_media": 10},
                    "praw": {"reddit": 20, "social_media": 10},
                }

                for imp in imports:
                    if imp in import_scores:
                        for category, points in import_scores[imp].items():
                            score[category] += points

            except:
                pass

            # Score based on filename patterns
            filename_patterns = {
                "openai|gpt|chatgpt": {"ai_llm": 15, "chatgpt": 10},
                "claude|anthropic": {"ai_llm": 15, "claude": 10},
                "instagram|insta": {"instagram": 15, "social_media": 10},
                "youtube|yt": {"youtube": 15, "video_tools": 10},
                "reddit": {"reddit": 15, "social_media": 10},
                "twitter|tweet": {"twitter": 15, "social_media": 10},
                "tiktok": {"tiktok": 15, "social_media": 10},
                "image|photo|picture": {"image_processing": 10},
                "video|mp4|movie": {"video_tools": 10},
                "audio|sound|mp3|music": {"audio_tools": 10},
                "scrape|crawl": {"scraping": 15, "web_automation": 10},
                "bot|automat": {"automation": 10, "bots": 5},
                "csv|json|data": {"data_tools": 10, "data_analysis": 5},
                "api|client|request": {"api_clients": 10},
                "analyze|report|stats": {"analysis": 10, "reporting": 5},
                "organize|rename|sort": {"file_management": 10},
                "generate|create|make": {"generators": 10},
                "tts|text.to.speech": {"tts": 15, "voice_synthesis": 10},
                "transcribe|speech.to.text": {"transcription": 15},
                "streamlit|dashboard": {"web_apps": 15, "dashboards": 10},
            }

            for pattern, categories in filename_patterns.items():
                if re.search(pattern, filename):
                    for category, points in categories.items():
                        score[category] += points

            # Score based on content keywords
            content_patterns = {
                "openai.ChatCompletion|openai.Completion": {"chatgpt": 20},
                "claude-|anthropic.Anthropic": {"claude": 20},
                "streamlit.": {"web_apps": 15},
                "selenium.webdriver": {"web_automation": 15},
                "BeautifulSoup": {"scraping": 15},
                "pd.read_csv|pd.DataFrame": {"csv_tools": 15},
                "PIL.Image|Image.open": {"image_processing": 15},
                "moviepy|VideoFileClip": {"video_editing": 15},
            }

            for pattern, categories in content_patterns.items():
                if re.search(pattern, content, re.IGNORECASE):
                    for category, points in categories.items():
                        score[category] += points

        except:
            pass

        # Get best category
        if score:
            best_category = max(score.items(), key=lambda x: x[1])
            if best_category[1] >= 10:  # Threshold
                return best_category[0]

        return "general"

    def recategorize_misc_folders(self):
        '\''Re-categorize the 'misc', 'helpers', 'other' folders"""
        print("\n🧠 SMART RE-CATEGORIZATION OF MISC FOLDERS")
        print("=" * 70 + "\n")

        folders_to_fix = [
            ("content_creation/misc", "content_creation"),
            ("utilities/helpers", "utilities"),
            ("audio_video_conversion/other", "audio_video_conversion"),
        ]

        total_recategorized = 0

        for misc_path, parent in folders_to_fix:
            full_path = self.pythons_dir / misc_path

            if not full_path.exists():
                continue

            files = [f for f in full_path.glob("*.py") if f.is_file()]
            print(f"📁 {misc_path}/ ({len(files)} files)\n")

            # Re-categorize each file
            new_categories = defaultdict(list)

            for f in files:
                category = self.analyze_file_deeply(f)
                new_categories[category].append(f)

            # Show distribution
            print("  New distribution:")
            for cat, file_list in sorted(
                new_categories.items(), key=lambda x: len(x[1]), reverse=True
            ):
                print(f"    {cat:30} {len(file_list):4} files")

            # Move files
            parent_path = self.pythons_dir / parent
            for cat, file_list in new_categories.items():
                cat_path = parent_path / cat
                cat_path.mkdir(exist_ok=True)

                for f in file_list:
                    target = cat_path / f.name
                    if not target.exists():
                        try:
                            shutil.move(str(f), str(target))
                            total_recategorized += 1
                        except Exception:
                            pass

            # Remove misc folder if empty
            try:
                remaining = list(full_path.glob("*.py"))
                if not remaining:
                    full_path.rmdir()
                    print(f"  ✅ Removed empty {misc_path}/")
            except:
                pass

            print()

        print(f"✅ Re-categorized {total_recategorized} files from misc folders\n")
        return total_recategorized


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     🧠 SMART SUB-CATEGORIZER                                      ║
║     Intelligent re-categorization using AST analysis             ║
╚═══════════════════════════════════════════════════════════════════╝
'\'')

    categorizer = SmartSubCategorizer()

    print("This will intelligently re-categorize:")
    print("  • content_creation/misc/ (1,186 files)")
    print("  • utilities/helpers/ (789 files)")
    print("  • audio_video_conversion/other/ (437 files)")
    print("\nUsing AST analysis to detect:")
    print("  - Import statements")
    print("  - API usage patterns")
    print("  - Content analysis")
    print()

    confirm = input("Type 'SMART' to execute: ")

    if confirm == "SMART":
        total = categorizer.recategorize_misc_folders()
        print(f"✅ Smart re-categorization complete! {total} files organized.")
    else:
        print("\n❌ Cancelled")


if __name__ == "__main__":
    main()
