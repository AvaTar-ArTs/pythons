#!/usr/bin/env python3
"""
Ultimate Content-Aware Analyzer

Deep reads every file and analyzes:
- Actual functionality (imports, functions, classes)
- API usage (OpenAI, Instagram, YouTube, etc.)
- Main purpose
- Better naming suggestions
"""

import os
import ast
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import shutil

class UltimateContentAnalyzer:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Service detection patterns
        self.service_patterns = {
            'openai': ['openai', 'gpt', 'chatgpt', 'dall-e', 'whisper'],
            'anthropic': ['anthropic', 'claude'],
            'google': ['gemini', 'bard', 'google'],
            'instagram': ['instabot', 'instaclient', 'instagram'],
            'youtube': ['pytube', 'yt-dlp', 'youtube', 'youtubeviewer'],
            'tiktok': ['tiktok'],
            'reddit': ['praw', 'reddit'],
            'telegram': ['telethon', 'telegram'],
            'twitter': ['tweepy', 'twitter'],
            'leonardo': ['leonardo'],
            'midjourney': ['midjourney'],
            'replicate': ['replicate'],
            'huggingface': ['transformers', 'diffusers', 'huggingface']
        }

        # Action patterns
        self.action_patterns = {
            'download': ['download', 'fetch', 'get', 'retrieve', 'pull'],
            'upload': ['upload', 'post', 'publish', 'push'],
            'generate': ['generate', 'create', 'make', 'build'],
            'analyze': ['analyze', 'parse', 'process', 'extract'],
            'convert': ['convert', 'transform', 'transcode'],
            'scrape': ['scrape', 'crawl', 'spider'],
            'bot': ['bot', 'automate', 'auto'],
            'transcribe': ['transcribe', 'speech', 'stt'],
            'tts': ['tts', 'text-to-speech', 'synthesize']
        }

        self.stats = {
            'files_analyzed': 0,
            'rename_suggestions': 0,
            'errors': 0
        }

        self.renaming_plan = []

    def detect_services(self, content: str, imports: list) -> list:
        """Detect which services/APIs are used."""
        content_lower = content.lower()
        services = []

        for service, patterns in self.service_patterns.items():
            if any(pattern in content_lower for pattern in patterns):
                services.append(service)

            # Check imports
            for imp in imports:
                if any(pattern in imp.lower() for pattern in patterns):
                    if service not in services:
                        services.append(service)

        return services

    def detect_actions(self, content: str, functions: list) -> list:
        """Detect what actions the script performs."""
        content_lower = content.lower()
        actions = []

        for action, patterns in self.action_patterns.items():
            if any(pattern in content_lower for pattern in patterns):
                actions.append(action)

            # Check function names
            for func in functions:
                if any(pattern in func.lower() for pattern in patterns):
                    if action not in actions:
                        actions.append(action)

        return actions

    def analyze_file_content(self, file_path: Path) -> dict:
        """Deep analysis of file content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse AST
            try:
                tree = ast.parse(content)
            except SyntaxError:
                return {'error': 'syntax_error'}

            # Extract information
            imports = []
            functions = []
            classes = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)

            # Get docstring
            docstring = ast.get_docstring(tree) or ""

            # Detect services and actions
            services = self.detect_services(content, imports)
            actions = self.detect_actions(content, functions)

            # Determine content type
            content_type = self.determine_content_type(imports, functions, classes)

            return {
                'imports': imports[:10],  # Top 10
                'functions': functions[:10],
                'classes': classes[:5],
                'services': services,
                'actions': actions,
                'content_type': content_type,
                'docstring': docstring[:200],
                'lines': len(content.split('\n'))
            }

        except Exception as e:
            return {'error': str(e)}

    def determine_content_type(self, imports, functions, classes):
        """Determine the type of script."""
        all_names = ' '.join(imports + functions + classes).lower()

        if any(x in all_names for x in ['csv', 'pandas', 'dataframe']):
            return 'data_processing'
        elif any(x in all_names for x in ['image', 'pil', 'opencv', 'pillow']):
            return 'image_processing'
        elif any(x in all_names for x in ['audio', 'mp3', 'ffmpeg', 'pydub']):
            return 'audio_processing'
        elif any(x in all_names for x in ['video', 'moviepy', 'cv2']):
            return 'video_processing'
        elif any(x in all_names for x in ['requests', 'urllib', 'httpx', 'selenium']):
            return 'web_automation'
        elif any(x in all_names for x in ['bot', 'automation']):
            return 'bot_automation'
        elif classes:
            return 'library'
        elif functions:
            return 'utility'
        else:
            return 'script'

    def suggest_better_name(self, file_path: Path, analysis: dict) -> str:
        """Suggest a better filename based on content analysis."""
        current_name = file_path.stem

        # If there's an error, keep current name
        if 'error' in analysis:
            return current_name

        services = analysis.get('services', [])
        actions = analysis.get('actions', [])
        content_type = analysis.get('content_type', '')

        # Build suggested name parts
        parts = []

        # Add primary service
        if services:
            parts.append(services[0])

        # Add primary action
        if actions:
            parts.append(actions[0])

        # Check if current name is descriptive enough
        current_lower = current_name.lower()

        # If current name has meaningful words, keep them
        meaningful_words = []
        for word in re.split(r'[-_]', current_name):
            if (len(word) > 3 and not word.isdigit() and
                word.lower() not in ['main', 'test', 'script', 'file', 'data']):
                meaningful_words.append(word)

        if meaningful_words:
            # Current name is good, just clean it up
            suggested = '-'.join(meaningful_words[:3]).lower()
        elif parts:
            # Use detected services/actions
            suggested = '-'.join(parts)
        else:
            # Keep current name
            return current_name

        return suggested

    def analyze_category(self, category_path: Path, dry_run=True):
        """Analyze all files in a category."""
        category_name = category_path.name
        python_files = list(category_path.glob("*.py"))

        print(f"\n📁 {category_name}/ ({len(python_files)} files)")

        renamed_count = 0

        for i, file_path in enumerate(python_files):
            if i % 50 == 0 and i > 0:
                print(f"  Progress: {i}/{len(python_files)}...")

            # Analyze content
            analysis = self.analyze_file_content(file_path)
            self.stats['files_analyzed'] += 1

            if 'error' in analysis:
                self.stats['errors'] += 1
                continue

            # Suggest better name
            suggested_name = self.suggest_better_name(file_path, analysis)

            if suggested_name != file_path.stem:
                target_path = category_path / f"{suggested_name}.py"

                # Handle conflicts
                counter = 1
                original_target = target_path
                while target_path.exists() and target_path != file_path:
                    target_path = category_path / f"{suggested_name}-v{counter}.py"
                    counter += 1

                # Add to renaming plan
                self.renaming_plan.append({
                    'category': category_name,
                    'old': file_path.name,
                    'new': target_path.name,
                    'services': analysis.get('services', []),
                    'actions': analysis.get('actions', []),
                    'type': analysis.get('content_type', ''),
                    'path': file_path,
                    'target': target_path
                })

                self.stats['rename_suggestions'] += 1
                renamed_count += 1

        if renamed_count > 0:
            print(f"  ✨ {renamed_count} files have better name suggestions")
        else:
            print(f"  ✅ All names are good!")

    def run(self, dry_run=True, limit_categories=None):
        """Run ultimate content analysis."""
        print(f"\n{'='*80}")
        print("🧠 ULTIMATE CONTENT-AWARE ANALYZER")
        print(f"{'='*80}\n")
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}\n")
        print("Deep reading every file to analyze content...\n")

        # Get all category folders
        categories = [f for f in self.target_dir.iterdir()
                     if f.is_dir() and not f.name.startswith(('.', '_'))]

        if limit_categories:
            categories = categories[:limit_categories]

        # Analyze each category
        for category in sorted(categories):
            self.analyze_category(category, dry_run)

        # Show renaming plan
        self.show_renaming_plan(dry_run)

        # Execute renames if live
        if not dry_run:
            self.execute_renames()

        # Generate report
        self.generate_report()

    def show_renaming_plan(self, dry_run):
        """Show the renaming plan."""
        if not self.renaming_plan:
            print(f"\n✅ All filenames are already content-aware!")
            return

        print(f"\n{'='*80}")
        print(f"📋 RENAMING PLAN ({len(self.renaming_plan)} files)")
        print(f"{'='*80}\n")

        # Group by category
        by_category = defaultdict(list)
        for item in self.renaming_plan:
            by_category[item['category']].append(item)

        for category, items in sorted(by_category.items()):
            print(f"\n{category}/ ({len(items)} renames):")
            for item in items[:5]:
                print(f"  {item['old']}")
                print(f"    → {item['new']}")
                if item['services']:
                    print(f"      Services: {', '.join(item['services'])}")
                if item['actions']:
                    print(f"      Actions: {', '.join(item['actions'])}")

            if len(items) > 5:
                print(f"  ... and {len(items) - 5} more")

    def execute_renames(self):
        """Execute the renaming plan."""
        print(f"\n🚀 Executing renames...\n")

        for item in self.renaming_plan:
            try:
                shutil.move(str(item['path']), str(item['target']))
            except Exception as e:
                print(f"❌ Error renaming {item['old']}: {e}")

    def generate_report(self):
        """Generate analysis report."""
        report_path = self.target_dir / f"ULTIMATE_CONTENT_ANALYSIS_{self.timestamp}.md"

        with open(report_path, 'w') as f:
            f.write("# 🧠 Ultimate Content-Aware Analysis Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("## Summary\n\n")
            f.write(f"- **Files Analyzed:** {self.stats['files_analyzed']:,}\n")
            f.write(f"- **Rename Suggestions:** {self.stats['rename_suggestions']}\n")
            f.write(f"- **Errors:** {self.stats['errors']}\n\n")

            if self.renaming_plan:
                f.write("## Suggested Renames\n\n")
                for item in self.renaming_plan[:100]:
                    f.write(f"### {item['category']}/{item['old']}\n")
                    f.write(f"**Suggested:** `{item['new']}`\n\n")
                    if item['services']:
                        f.write(f"- **Services:** {', '.join(item['services'])}\n")
                    if item['actions']:
                        f.write(f"- **Actions:** {', '.join(item['actions'])}\n")
                    if item['type']:
                        f.write(f"- **Type:** {item['type']}\n")
                    f.write("\n")

        print(f"\n📄 Report: {report_path}")

        # Final summary
        print(f"\n{'='*80}")
        print("✅ ANALYSIS COMPLETE!")
        print(f"{'='*80}\n")
        print(f"Files Analyzed: {self.stats['files_analyzed']:,}")
        print(f"Rename Suggestions: {self.stats['rename_suggestions']}")
        print(f"Errors: {self.stats['errors']}")
        print()

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Ultimate Content Analyzer')
    parser.add_argument('--target', default='.', help='Target directory')
    parser.add_argument('--live', action='store_true', help='Execute renames')
    parser.add_argument('--limit', type=int, help='Limit number of categories')

    args = parser.parse_args()

    analyzer = UltimateContentAnalyzer(args.target)
    analyzer.run(dry_run=not args.live, limit_categories=args.limit)

if __name__ == "__main__":
    main()
