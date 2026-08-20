#!/usr/bin/env python3
"""
🎯 FUNCTIONAL DUPLICATE SCANNER
Find files that do the SAME THING (same functionality/purpose)
Even if code is different
"""

import ast
import re
from pathlib import Path
from collections import defaultdict
import shutil
from datetime import datetime

class FunctionalDuplicateScanner:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)
        self.file_purposes = []

    def analyze_file_purpose(self, filepath):
        """Determine what a file DOES (its purpose/functionality)"""
        purpose = {
            'path': filepath,
            'name': filepath.name,
            'actions': set(),  # What it does (download, upload, convert, etc.)
            'targets': set(),  # What it works with (youtube, image, audio, etc.)
            'apis': set(),  # What APIs it uses
            'operations': set(),  # Specific operations
            'purpose_signature': ''
        }

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            content_lower = content.lower()
            filename = filepath.name.lower()

            # Parse AST for function names (reveal intent)
            try:
                tree = ast.parse(content)
                func_names = [node.name.lower() for node in ast.walk(tree)
                             if isinstance(node, ast.FunctionDef)]

                # Detect actions from function names
                action_keywords = {
                    'download': ['download', 'fetch', 'get', 'retrieve', 'pull'],
                    'upload': ['upload', 'post', 'publish', 'push', 'send'],
                    'convert': ['convert', 'transform', 'change', 'transcode'],
                    'generate': ['generate', 'create', 'make', 'build', 'produce'],
                    'analyze': ['analyze', 'parse', 'process', 'scan', 'inspect'],
                    'organize': ['organize', 'sort', 'categorize', 'arrange'],
                    'rename': ['rename', 'move', 'relocate'],
                    'delete': ['delete', 'remove', 'clean', 'purge'],
                    'resize': ['resize', 'scale', 'crop'],
                    'compress': ['compress', 'optimize', 'reduce'],
                    'transcribe': ['transcribe', 'speech_to_text', 'stt'],
                    'synthesize': ['synthesize', 'text_to_speech', 'tts', 'speak'],
                    'scrape': ['scrape', 'crawl', 'extract', 'spider'],
                }

                func_text = ' '.join(func_names)

                for action, keywords in action_keywords.items():
                    if any(kw in func_text for kw in keywords):
                        purpose['actions'].add(action)

            except:
                pass

            # Detect targets (what it works with)
            target_keywords = {
                'youtube': ['youtube', 'yt', 'ytdl'],
                'instagram': ['instagram', 'insta', 'ig'],
                'reddit': ['reddit', 'praw'],
                'twitter': ['twitter', 'tweet'],
                'tiktok': ['tiktok'],
                'image': ['image', 'photo', 'picture', 'img', 'jpg', 'png'],
                'video': ['video', 'mp4', 'movie', 'clip', 'avi'],
                'audio': ['audio', 'sound', 'music', 'mp3', 'wav'],
                'csv': ['csv', 'spreadsheet', 'dataframe'],
                'pdf': ['pdf', 'document'],
                'text': ['text', 'txt', 'string'],
            }

            text = filename + ' ' + content_lower

            for target, keywords in target_keywords.items():
                if any(kw in text for kw in keywords):
                    purpose['targets'].add(target)

            # Detect APIs
            api_keywords = {
                'openai': ['openai', 'gpt', 'chatgpt'],
                'anthropic': ['anthropic', 'claude'],
                'elevenlabs': ['elevenlabs', 'eleven'],
                'whisper': ['whisper'],
                'leonardo': ['leonardo'],
                'suno': ['suno'],
                'selenium': ['selenium'],
                'ffmpeg': ['ffmpeg'],
            }

            for api, keywords in api_keywords.items():
                if any(kw in text for kw in keywords):
                    purpose['apis'].add(api)

            # Detect specific operations from filename
            filename_operations = {
                'thumbnail': 'make_thumbnail',
                'upscale': 'upscale_image',
                'compress': 'compress_file',
                'batch': 'batch_process',
                'automated': 'automation',
                'bot': 'bot_automation',
                'scraper': 'web_scraping',
                'crawler': 'web_crawling',
            }

            for keyword, operation in filename_operations.items():
                if keyword in filename:
                    purpose['operations'].add(operation)

            # Create purpose signature
            actions_str = ','.join(sorted(purpose['actions']))
            targets_str = ','.join(sorted(purpose['targets']))
            apis_str = ','.join(sorted(purpose['apis']))
            ops_str = ','.join(sorted(purpose['operations']))

            purpose['purpose_signature'] = f"{actions_str}|{targets_str}|{apis_str}|{ops_str}"

        except Exception as e:
            purpose['error'] = str(e)

        return purpose

    def scan_all_files(self):
        """Scan all files for their purpose"""
        print("🎯 FUNCTIONAL DUPLICATE SCAN - Analyzing what each file DOES...\n")

        files = [f for f in self.pythons_dir.rglob('*.py')
                 if '_archive' not in str(f) and '2T-Xx-python' not in str(f)
                 and '.venv' not in str(f) and '.history' not in str(f)]

        print(f"📂 Analyzing {len(files)} files for functionality...\n")

        for i, f in enumerate(files, 1):
            # Skip cleanup scripts
            if any(f.name.startswith(x) for x in ['DEEP_', 'INTELLIGENT_', 'SMART_',
                                                    'CLEANUP_', 'COMPREHENSIVE_',
                                                    'AGGRESSIVE_', 'RECURSIVE_', 'FINAL_',
                                                    'FIND_', 'SUB_', 'STRUCTURAL_', 'FAST_',
                                                    'ULTRA_', 'REMOVE_', 'FIX_', 'CONTENT_',
                                                    'FUNCTIONAL_']):
                continue

            purpose = self.analyze_file_purpose(f)
            self.file_purposes.append(purpose)

            if i % 500 == 0:
                print(f"   ... analyzed {i} files")

        print(f"\n✅ Analyzed {len(self.file_purposes)} files\n")
        return len(self.file_purposes)

    def find_functional_duplicates(self):
        """Find files with same functionality"""
        print("🔍 Finding files with same functionality...\n")

        # Group by purpose signature
        by_purpose = defaultdict(list)

        for purpose in self.file_purposes:
            if purpose['purpose_signature'] and purpose['purpose_signature'] != '|||':
                by_purpose[purpose['purpose_signature']].append(purpose)

        # Find groups with multiple files
        functional_dupes = []

        for sig, group in by_purpose.items():
            if len(group) >= 3:  # 3+ files doing same thing
                functional_dupes.append({
                    'signature': sig,
                    'count': len(group),
                    'files': group,
                    'actions': group[0]['actions'],
                    'targets': group[0]['targets'],
                    'apis': group[0]['apis']
                })

        # Sort by count
        functional_dupes.sort(key=lambda x: x['count'], reverse=True)

        print(f"Found {len(functional_dupes)} functional duplicate groups\n")

        return functional_dupes

    def print_summary(self, functional_dupes):
        """Print summary of functional duplicates"""
        print("=" * 70)
        print("📊 FUNCTIONAL DUPLICATE SUMMARY")
        print("=" * 70)
        print(f"Groups found:            {len(functional_dupes)}")

        total_dupes = sum(group['count'] - 1 for group in functional_dupes)
        print(f"Files to review:         {total_dupes}")
        print("=" * 70)

        if functional_dupes:
            print("\n🔥 TOP 30 FUNCTIONAL DUPLICATE GROUPS:\n")

            for i, group in enumerate(functional_dupes[:30], 1):
                actions_str = ', '.join(group['actions']) if group['actions'] else 'no specific action'
                targets_str = ', '.join(group['targets']) if group['targets'] else 'general'
                apis_str = ', '.join(group['apis']) if group['apis'] else 'no API'

                print(f"{i:2}. {group['count']} files doing: {actions_str}")
                print(f"    Target: {targets_str}")
                print(f"    APIs: {apis_str}")

                for purpose in group['files'][:4]:
                    print(f"      • {purpose['name']}")

                if len(group['files']) > 4:
                    print(f"      ... and {len(group['files']) - 4} more")
                print()

    def remove_functional_duplicates(self, functional_dupes):
        """Remove functional duplicates keeping best version"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_dir = self.pythons_dir / '_archive' / f'functional-dupes-{timestamp}'
        archive_dir.mkdir(parents=True, exist_ok=True)

        print("🗑️  Removing functional duplicates (keeping best)...\n")

        removed = 0

        for group in functional_dupes:
            # Score each file
            scored = []

            for purpose in group['files']:
                score = 0

                # Size
                try:
                    score += purpose['path'].stat().st_size / 100
                except:
                    pass

                # Prefer clean names
                name = purpose['name']
                if '_from_' not in name and 'DOCS_PYTHON_' not in name:
                    score += 100
                if 'duplicate' not in name and 'copy' not in name:
                    score += 50

                # Prefer files with more descriptive names
                score += len(name) / 10

                scored.append((purpose, score))

            # Keep best
            scored.sort(key=lambda x: x[1], reverse=True)

            keep = scored[0][0]
            to_remove = [p for p, _ in scored[1:]]

            # Remove duplicates
            for purpose in to_remove:
                try:
                    rel = purpose['path'].relative_to(self.pythons_dir)
                    archive_path = archive_dir / rel
                    archive_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(purpose['path'], archive_path)

                    purpose['path'].unlink()
                    removed += 1

                    if removed % 50 == 0:
                        print(f"   ... removed {removed} files")
                except:
                    pass

        print(f"\n✅ Removed {removed} functional duplicates")
        print(f"📦 Archived to: {archive_dir}\n")

        return removed


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     🎯 FUNCTIONAL DUPLICATE SCANNER                               ║
║     Find files that DO THE SAME THING (same purpose/function)    ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    scanner = FunctionalDuplicateScanner()

    # Scan all files
    count = scanner.scan_all_files()

    # Find functional duplicates
    functional_dupes = scanner.find_functional_duplicates()

    # Print summary
    scanner.print_summary(functional_dupes)

    if functional_dupes:
        confirm = input("\nType 'FUNCTIONAL' to remove duplicate functionality: ")

        if confirm == 'FUNCTIONAL':
            removed = scanner.remove_functional_duplicates(functional_dupes)

            # Final count
            final = len([f for f in scanner.pythons_dir.rglob('*.py')
                        if '_archive' not in str(f) and '2T-Xx-python' not in str(f)
                        and '.venv' not in str(f) and '.history' not in str(f)])

            print(f"🎉 Removed {removed} functional duplicates!")
            print(f"🎯 Files remaining: {final}")
            print(f"   Original: 8,723")
            print(f"   Reduction: {100*(8723-final)/8723:.1f}%")
        else:
            print("\n❌ Cancelled")
    else:
        print("\n✅ No functional duplicates found!")


if __name__ == "__main__":
    main()

