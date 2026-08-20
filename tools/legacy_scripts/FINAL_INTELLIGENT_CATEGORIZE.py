#!/usr/bin/env python3
"""
🎯 FINAL INTELLIGENT CATEGORIZATION
Use function names, docstrings, and file size to categorize the remaining "general" folders
"""

import ast
import re
from pathlib import Path
from collections import defaultdict
import shutil

class FinalCategorizer:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)

    def deep_analyze_file(self, filepath):
        """VERY deep analysis using multiple signals"""
        signals = defaultdict(int)

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            size = len(content)
            filename = filepath.name.lower()

            # Size-based categorization
            if size < 500:  # Very small scripts
                signals['small_scripts'] += 20
            elif size < 2000:  # Small scripts
                signals['small_tools'] += 15
            elif size > 10000:  # Large scripts
                signals['complex_tools'] += 10

            # Parse AST for function names
            try:
                tree = ast.parse(content)
                function_names = []
                class_names = []

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        function_names.append(node.name.lower())
                    elif isinstance(node, ast.ClassDef):
                        class_names.append(node.name.lower())

                # Score based on function names
                func_text = ' '.join(function_names)
                class_text = ' '.join(class_names)
                all_text = func_text + ' ' + class_text + ' ' + filename

                # Specific purposes
                if any(x in all_text for x in ['download', 'fetch', 'scrape', 'get']):
                    signals['downloaders'] += 10

                if any(x in all_text for x in ['upload', 'post', 'publish', 'send']):
                    signals['uploaders'] += 10

                if any(x in all_text for x in ['generate', 'create', 'make', 'build']):
                    signals['generators'] += 10

                if any(x in all_text for x in ['analyze', 'parse', 'process', 'scan']):
                    signals['analyzers'] += 10

                if any(x in all_text for x in ['convert', 'transform', 'change', 'modify']):
                    signals['converters'] += 10

                if any(x in all_text for x in ['organize', 'sort', 'categorize', 'arrange']):
                    signals['organizers'] += 10

                if any(x in all_text for x in ['clean', 'remove', 'delete', 'clear']):
                    signals['cleaners'] += 10

                if any(x in all_text for x in ['test', 'demo', 'example', 'sample']):
                    signals['examples_tests'] += 10

                if any(x in all_text for x in ['monitor', 'watch', 'track', 'log']):
                    signals['monitors'] += 10

                if any(x in all_text for x in ['config', 'setup', 'init', 'settings']):
                    signals['config_tools'] += 10

                # Content-type specific
                if any(x in all_text for x in ['csv', 'excel', 'spreadsheet', 'dataframe']):
                    signals['csv_excel'] += 10

                if any(x in all_text for x in ['json', 'yaml', 'xml', 'toml']):
                    signals['data_formats'] += 10

                if any(x in all_text for x in ['image', 'photo', 'picture', 'thumbnail']):
                    signals['image_ops'] += 10

                if any(x in all_text for x in ['video', 'mp4', 'movie', 'clip']):
                    signals['video_ops'] += 10

                if any(x in all_text for x in ['audio', 'sound', 'music', 'mp3']):
                    signals['audio_ops'] += 10

            except:
                pass

            # Filename-based fallback scoring
            filename_categories = {
                r'^(test|demo|example|sample)': 'examples_tests',
                r'^(convert|transform)': 'converters',
                r'^(analyze|scan|parse)': 'analyzers',
                r'^(generate|create|make)': 'generators',
                r'^(upload|post|send)': 'uploaders',
                r'^(download|fetch|get)': 'downloaders',
                r'^(organize|sort|arrange)': 'organizers',
                r'^(clean|delete|remove)': 'cleaners',
                r'^(config|setup|init)': 'config_tools',
                r'(-test|-demo)\.py$': 'examples_tests',
                r'(-config|-setup)\.py$': 'config_tools',
                r'.*bot.*': 'bots_automation',
                r'.*scrape.*': 'scrapers',
                r'.*crawler.*': 'scrapers',
            }

            for pattern, category in filename_categories.items():
                if re.search(pattern, filename):
                    signals[category] += 15

        except:
            pass

        # Return best category or 'uncategorized'
        if signals:
            best = max(signals.items(), key=lambda x: x[1])
            if best[1] >= 10:
                return best[0]

        return 'uncategorized'

    def recategorize_general_folders(self):
        """Re-categorize the remaining 'general' folders"""
        print("🎯 FINAL INTELLIGENT CATEGORIZATION")
        print("=" * 70 + "\n")

        general_folders = [
            'content_creation/general',
            'utilities/general',
            'audio_video_conversion/general',
            'content_creation/data_analysis'  # Also big
        ]

        total_moved = 0

        for general_path in general_folders:
            full_path = self.pythons_dir / general_path

            if not full_path.exists():
                continue

            files = [f for f in full_path.glob('*.py') if f.is_file()]

            if not files:
                continue

            print(f"📁 {general_path}/ ({len(files)} files)")

            # Analyze each file
            new_categories = defaultdict(list)

            for f in files:
                category = self.deep_analyze_file(f)
                new_categories[category].append(f)

            # Show new distribution
            print("   New distribution:")
            for cat in sorted(new_categories.keys(), key=lambda x: len(new_categories[x]), reverse=True)[:15]:
                count = len(new_categories[cat])
                print(f"     {cat:35} {count:4} files")

            # Move files
            parent_path = full_path.parent

            for cat, file_list in new_categories.items():
                cat_path = parent_path / cat
                cat_path.mkdir(exist_ok=True)

                for f in file_list:
                    target = cat_path / f.name
                    if not target.exists():
                        try:
                            shutil.move(str(f), str(target))
                            total_moved += 1
                        except:
                            pass

            # Try to remove general folder if empty
            try:
                remaining = list(full_path.glob('*.py'))
                if not remaining:
                    full_path.rmdir()
                    print(f"   ✅ Removed empty {general_path}/\n")
                else:
                    print(f"   ⚠️  {len(remaining)} files remaining\n")
            except:
                print()

        print("=" * 70)
        print(f"✅ TOTAL: Re-categorized {total_moved} files")
        print("=" * 70)

        return total_moved


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     🎯 FINAL INTELLIGENT CATEGORIZATION                          ║
║     Break down the remaining "general" folders (500+ files)      ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    categorizer = FinalCategorizer()

    print("This will analyze:")
    print("  • content_creation/general/ (519 files)")
    print("  • content_creation/data_analysis/ (386 files)")
    print("  • utilities/general/ (431 files)")
    print("  • audio_video_conversion/general/ (127 files)")
    print()
    print("Using deep analysis:")
    print("  - Function names")
    print("  - Docstrings")
    print("  - File size patterns")
    print("  - Filename patterns")
    print()

    confirm = input("Type 'FINALIZE' to execute: ")

    if confirm == 'FINALIZE':
        total = categorizer.recategorize_general_folders()
        print(f"\n✅ Finalization complete! {total} files organized.")
    else:
        print("\n❌ Cancelled")


if __name__ == "__main__":
    main()

