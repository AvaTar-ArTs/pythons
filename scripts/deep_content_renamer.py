
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_033 = 033
CONSTANT_100 = 100
CONSTANT_500 = 500

#!/usr/bin/env python3
"""
🧠 DEEP CONTENT-AWARE INTELLIGENT RENAMER
=========================================
Truly understands what code does by analyzing:
- Imports (what APIs/services used)
- Functions (what operations performed)
- Classes (what objects/patterns)
- Docstrings (stated purpose)
- Code flow (workflow understanding)
- Parent folder context

Then generates meaningful names that reflect ACTUAL functionality.

Examples:
- leonardo API + image download → leonardo-image-downloader.py
- instagram + post upload → instagram-post-uploader.py
- youtube + video process + audio → youtube-video-audio-processor.py
"""

import os
import ast
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Set
import csv

# Colors
class Colors:
    CYAN = "\CONSTANT_033[96m"
    GREEN = "\CONSTANT_033[92m"
    YELLOW = "\CONSTANT_033[93m"
    RED = "\CONSTANT_033[91m"
    MAGENTA = "\CONSTANT_033[35m"
    BOLD = "\CONSTANT_033[1m"
    END = "\CONSTANT_033[0m"


class DeepCodeAnalyzer:
    """Deep analysis of what code actually does"""

    # API/Service detection
    SERVICES = {
        'leonardo': ['leonardo', 'leonardo.ai', 'leonardo_api'],
        'openai': ['openai', 'gpt', 'chatgpt'],
        'anthropic': ['anthropic', 'claude'],
        'gemini': ['gemini', 'google.generativeai', 'genai'],
        'instagram': ['instagram', 'instapy', 'instagrapi'],
        'youtube': ['youtube', 'pytube', 'yt-dlp', 'googleapiclient'],
        'reddit': ['praw', 'reddit'],
        'twitter': ['tweepy', 'twitter'],
        'tiktok': ['tiktok'],
        'telegram': ['telegram', 'telethon'],
        'discord': ['discord'],
        'elevenlabs': ['elevenlabs', 'eleven'],
        'stability': ['stability', 'stablediffusion'],
        'replicate': ['replicate'],
        'selenium': ['selenium'],
        'beautifulsoup': ['beautifulsoup', 'bs4'],
        'requests': ['requests'],
        'flask': ['flask'],
        'fastapi': ['fastapi'],
        'pandas': ['pandas'],
        'opencv': ['cv2', 'opencv'],
        'pillow': ['PIL', 'pillow'],
        'moviepy': ['moviepy'],
        'ffmpeg': ['ffmpeg'],
    }

    # Action/Operation detection
    ACTIONS = {
        'download': ['download', 'fetch', 'get', 'pull', 'retrieve'],
        'upload': ['upload', 'post', 'push', 'publish', 'send'],
        'generate': ['generate', 'create', 'make', 'produce', 'build'],
        'process': ['process', 'transform', 'modify', 'edit'],
        'analyze': ['analyze', 'analyse', 'inspect', 'scan', 'check'],
        'scrape': ['scrape', 'crawl', 'extract'],
        'convert': ['convert', 'transform', 'encode', 'decode'],
        'organize': ['organize', 'sort', 'categorize', 'classify'],
        'automate': ['automate', 'bot', 'scheduler'],
        'transcribe': ['transcribe', 'speech_to_text', 'stt'],
        'synthesize': ['synthesize', 'tts', 'text_to_speech'],
    }

    # Content type detection
    CONTENT_TYPES = {
        'image': ['image', 'img', 'photo', 'picture', 'png', 'jpg'],
        'video': ['video', 'mp4', 'clip', 'movie'],
        'audio': ['audio', 'sound', 'music', 'voice', 'mp3'],
        'text': ['text', 'txt', 'document', 'content'],
        'data': ['data', 'dataset', 'csv', 'json'],
        'file': ['file', 'files'],
    }

    def __init__(self):
        pass

    def deep_analyze(self, filepath: Path) -> Dict:
        """Deep analysis of code functionality"""

        analysis = {
            'services': set(),
            'actions': set(),
            'content_types': set(),
            'functions': [],
            'classes': [],
            'imports': [],
            'docstring': None,
            'main_purpose': None,
            'workflow': [],
            'is_class_based': False,
        }

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Parse AST
            tree = ast.parse(content)

            # Get docstring
            analysis['docstring'] = ast.get_docstring(tree)

            # Extract all identifiers
            all_names = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis['functions'].append(node.name)
                    all_names.append(node.name.lower())

                elif isinstance(node, ast.ClassDef):
                    analysis['classes'].append(node.name)
                    all_names.append(node.name.lower())
                    analysis['is_class_based'] = True

                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis['imports'].append(alias.name)
                        all_names.append(alias.name.lower())

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        analysis['imports'].append(node.module)
                        all_names.append(node.module.lower())

            # Combine all text for analysis
            all_text = ' '.join(all_names)
            if analysis['docstring']:
                all_text += ' ' + analysis['docstring'].lower()
            all_text += ' ' + filepath.stem.lower()

            # Detect services/APIs
            for service, keywords in self.SERVICES.items():
                if any(kw in all_text for kw in keywords):
                    analysis['services'].add(service)

            # Detect actions
            for action, keywords in self.ACTIONS.items():
                if any(kw in all_text for kw in keywords):
                    analysis['actions'].add(action)

            # Detect content types
            for ctype, keywords in self.CONTENT_TYPES.items():
                if any(kw in all_text for kw in keywords):
                    analysis['content_types'].add(ctype)

            # Determine main purpose from docstring or function names
            if analysis['docstring']:
                first_sentence = analysis['docstring'].split('.')[0].lower()
                analysis['main_purpose'] = first_sentence[:CONSTANT_100]
            elif analysis['functions']:
                # Use most descriptive function name
                main_func = max(analysis['functions'], key=len)
                analysis['main_purpose'] = main_func.replace('_', ' ')

            # Detect workflow (download → process → upload)
            if 'download' in analysis['actions'] and 'upload' in analysis['actions']:
                analysis['workflow'] = ['download', 'process', 'upload']
            elif 'scrape' in analysis['actions'] and 'process' in analysis['actions']:
                analysis['workflow'] = ['scrape', 'process']
            elif 'generate' in analysis['actions'] and 'upload' in analysis['actions']:
                analysis['workflow'] = ['generate', 'upload']

        except Exception as e:
            analysis['error'] = str(e)

        return analysis

    def build_intelligent_name(self, filepath: Path, analysis: Dict) -> str:
        """Build name that reflects actual functionality"""

        original = filepath.stem

        # If ProperCase class-based file, preserve it
        if analysis['is_class_based'] and re.search(r'^[A-Z][a-z]+[A-Z]', original):
            # Clean but preserve case
            clean = re.sub(r'[_\s-](\d+)$', r'_v\1', original)
            clean = re.sub(r'[^\w]', '', clean)
            return clean

        # Build name from analysis
        parts = []

        # 1. Service/Platform (most important context)
        if analysis['services']:
            # Prioritize social media, then AI services
            priority_services = ['instagram', 'youtube', 'reddit', 'twitter', 'tiktok']
            for service in priority_services:
                if service in analysis['services']:
                    parts.append(service)
                    break
            else:
                # Use first service found
                parts.append(list(analysis['services'])[0])

        # 2. Content type (what it works with)
        if analysis['content_types']:
            # Prioritize specific types
            priority_types = ['video', 'image', 'audio']
            for ctype in priority_types:
                if ctype in analysis['content_types']:
                    parts.append(ctype)
                    break
            else:
                if 'data' not in parts:  # Skip generic 'data'
                    ctype = list(analysis['content_types'])[0]
                    if ctype not in ['file', 'data', 'text']:
                        parts.append(ctype)

        # 3. Action (what it does)
        if analysis['actions']:
            # Prioritize specific actions
            priority_actions = ['download', 'upload', 'generate', 'scrape', 'analyze']
            for action in priority_actions:
                if action in analysis['actions']:
                    parts.append(action + ('r' if action != 'analyze' else 'r'))  # downloader, analyzer
                    break
            else:
                action = list(analysis['actions'])[0]
                parts.append(action + 'r')

        # If we found meaningful parts, use them
        if len(parts) >= 2:
            name = '-'.join(parts[:3])  # Max 3 parts
        else:
            # Fall back to cleaning original name
            # Remove redundant prefixes
            clean = original
            for prefix in ['enhanced_', 'simple_', 'basic_', 'fixed_', 'new_', 'improved_']:
                clean = clean.replace(prefix, '')

            # Extract meaningful words
            words = re.findall(r'[a-zA-Z]+', clean)
            meaningful = [w for w in words if len(w) > 2][:3]

            if meaningful:
                name = '-'.join(meaningful).lower()
            else:
                name = clean.lower()

        # Clean up
        name = re.sub(r'[^\w\-]', '-', name)
        name = re.sub(r'-+', '-', name)
        name = name.strip('-')

        # Limit length
        if len(name) > 60:
            parts = name.split('-')
            name = '-'.join(parts[:3])

        return name


class DeepContentRenamer:
    """Intelligent renamer with deep content understanding"""

    def __init__(self, target_dir: str, dry_run: bool = True, limit: int = CONSTANT_500):
        self.target_dir = Path(target_dir)
        self.dry_run = dry_run
        self.limit = limit  # Limit renames for safety

        self.analyzer = DeepCodeAnalyzer()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = self.target_dir / f"deep_rename_backup_{timestamp}"
        self.undo_script = self.target_dir / f"UNDO_DEEP_RENAME_{timestamp}.sh"

        self.stats = {
            'analyzed': 0,
            'renamed': 0,
            'skipped': 0,
        }

        self.rename_plan = []
        self.undo_commands = []

    def should_rename(self, filepath: Path) -> bool:
        """Check if file needs renaming"""
        name = filepath.stem

        # Needs renaming if:
        problems = [
            bool(re.search(r'\s\d+$', name)),  # Ends with " 2", " 3"
            'copy' in name.lower(),
            bool(re.search(r'\(\d+\)', name)),  # Has (1), (2)
            bool(re.search(r'--', name)),  # Has double dashes
            bool(re.search(r'__', name)),  # Has double underscores
            name.count('_') > 5,  # Too many underscores
            len(name) > 60,  # Too long
            bool(re.search(r'_\d{8,}', name)),  # Has timestamp
        ]

        return any(problems)

    def scan_and_analyze(self):
        """Deep scan with content understanding"""

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"🔬 DEEP CONTENT ANALYSIS")
        logger.info(f"{'='*80}{Colors.END}\n")

        python_files = list(self.target_dir.rglob("*.py"))

        # Skip backups
        skip = ['backup', '.git', '__pycache__']
        python_files = [f for f in python_files if not any(s in str(f) for s in skip)]

        logger.info(f"{Colors.GREEN}Analyzing {len(python_files)} Python files...{Colors.END}\n")

        needs_rename = [f for f in python_files if self.should_rename(f)]

        logger.info(f"{Colors.YELLOW}Files needing better names: {len(needs_rename)}{Colors.END}\n")

        # Deep analyze each file
        for idx, filepath in enumerate(needs_rename[:self.limit], 1):
            if idx % 50 == 0:
                logger.info(f"{Colors.YELLOW}Analyzing: {idx}/{min(len(needs_rename), self.limit)}...{Colors.END}", end='\r')

            self.stats['analyzed'] += 1

            # Deep analysis
            analysis = self.analyzer.deep_analyze(filepath)

            # Generate intelligent name
            new_base = self.analyzer.build_intelligent_name(filepath, analysis)
            new_name = f"{new_base}.py"

            # Only add if different
            if new_name != filepath.name:
                self.rename_plan.append({
                    'old_path': filepath,
                    'old_name': filepath.name,
                    'new_name': new_name,
                    'services': list(analysis['services'])[:3],
                    'actions': list(analysis['actions'])[:2],
                    'content_types': list(analysis['content_types'])[:2],
                    'purpose': analysis.get('main_purpose', 'Script'),
                    'parent': filepath.parent.name,
                })

        logger.info(f"\n{Colors.GREEN}✅ Deep analysis complete!{Colors.END}")
        logger.info(f"{Colors.CYAN}Files to rename: {len(self.rename_plan)}{Colors.END}")

    def execute_renames(self):
        """Execute the rename plan"""

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"🏷️ EXECUTING INTELLIGENT RENAMES")
        logger.info(f"{'='*80}{Colors.END}\n")

        logger.info(f"{Colors.YELLOW}Total: {len(self.rename_plan)}{Colors.END}")
        logger.info(f"{Colors.CYAN}Mode: {'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}\n")

        # Show examples grouped by service
        by_service = defaultdict(list)
        for item in self.rename_plan:
            if item['services']:
                service = item['services'][0]
            else:
                service = 'other'
            by_service[service].append(item)

        for service in sorted(by_service.keys())[:10]:
            items = by_service[service]
            logger.info(f"\n{Colors.BOLD}🔧 {service.upper()} Files ({len(items)} renames){Colors.END}")

            for item in items[:5]:
                logger.info(f"  {Colors.RED}{item['old_name']}{Colors.END}")
                logger.info(f"  → {Colors.GREEN}{item['new_name']}{Colors.END}")

                # Show what it does
                desc = []
                if item['actions']:
                    desc.append(f"Actions: {', '.join(item['actions'])}")
                if item['content_types']:
                    desc.append(f"Type: {', '.join(item['content_types'])}")
                if desc:
                    logger.info(f"     ({'; '.join(desc)})")

                # Execute
                if not self.dry_run:
                    try:
                        new_path = item['old_path'].parent / item['new_name']

                        # Handle collision
                        if new_path.exists() and new_path != item['old_path']:
                            base = Path(item['new_name']).stem
                            counter = 2
                            while (item['old_path'].parent / f"{base}-v{counter}.py").exists():
                                counter += 1
                            new_path = item['old_path'].parent / f"{base}-v{counter}.py"

                        # Backup
                        backup_path = self.backup_dir / item['old_path'].relative_to(self.target_dir)
                        backup_path.parent.mkdir(parents=True, exist_ok=True)
                        import shutil
                        shutil.copy2(item['old_path'], backup_path)

                        # Rename
                        item['old_path'].rename(new_path)

                        self.undo_commands.append(f"mv '{new_path}' '{item['old_path']}'")
                        self.stats['renamed'] += 1

                    except Exception as e:
                        logger.info(f"    {Colors.RED}Error: {e}{Colors.END}")
                        self.stats['skipped'] += 1

            if len(items) > 5:
                logger.info(f"  ... and {len(items) - 5} more")

    def generate_report(self):
        """Generate comprehensive report"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.target_dir / f"DEEP_RENAME_REPORT_{timestamp}.md"
        csv_file = self.target_dir / f"deep_rename_mapping_{timestamp}.csv"

        # Markdown
        with open(report_file, 'w') as f:
            f.write("# 🧠 DEEP CONTENT-AWARE RENAME REPORT\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## 📊 SUMMARY\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Analyzed | {self.stats['analyzed']:,} |\n")
            f.write(f"| Renamed | {self.stats['renamed']:,} |\n")
            f.write(f"| Skipped | {self.stats['skipped']:,} |\n\n")

            # By service
            f.write("## 🔧 RENAMES BY SERVICE\n\n")
            by_service = defaultdict(list)
            for item in self.rename_plan:
                service = item['services'][0] if item['services'] else 'other'
                by_service[service].append(item)

            for service in sorted(by_service.keys()):
                items = by_service[service]
                f.write(f"### {service.title()} ({len(items)} files)\n\n")

                for item in items[:20]:
                    f.write(f"- `{item['old_name']}` → `{item['new_name']}`\n")
                    if item['purpose']:
                        f.write(f"  - Purpose: {item['purpose'][:80]}\n")
                f.write(Path("\n"))

        # CSV
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Old Name', 'New Name', 'Services', 'Actions',
                           'Content Types', 'Purpose', 'Parent', 'Path'])

            for item in self.rename_plan:
                writer.writerow([
                    item['old_name'],
                    item['new_name'],
                    ', '.join(item['services']),
                    ', '.join(item['actions']),
                    ', '.join(item['content_types']),
                    item['purpose'][:CONSTANT_100] if item['purpose'] else '',
                    item['parent'],
                    str(item['old_path'].relative_to(self.target_dir)),
                ])

        # Undo script
        if self.undo_commands and not self.dry_run:
            with open(self.undo_script, 'w') as f:
                f.write("#!/bin/bash\n")
                f.write("# Undo deep content-aware renaming\n\n")
                for cmd in reversed(self.undo_commands):
                    f.write(f"{cmd}\n")
            self.undo_script.chmod(0o755)

        logger.info(f"{Colors.GREEN}✅ Report: {report_file}{Colors.END}")
        logger.info(f"{Colors.GREEN}✅ CSV: {csv_file}{Colors.END}")

    def run(self):
        """Run deep content-aware renamer"""

        logger.info(f"{Colors.MAGENTA}{Colors.BOLD}")
        logger.info("╔═══════════════════════════════════════════════════════════════════════════════╗")
        logger.info("║                                                                               ║")
        logger.info("║           🧠 DEEP CONTENT-AWARE INTELLIGENT RENAMER 🚀                       ║")
        logger.info("║                                                                               ║")
        logger.info("║     Understands What Code Does Before Renaming                               ║")
        logger.info("║                                                                               ║")
        logger.info("╚═══════════════════════════════════════════════════════════════════════════════╝")
        logger.info(f"{Colors.END}\n")

        logger.info(f"{Colors.CYAN}Target: {self.target_dir}{Colors.END}")
        logger.info(f"{Colors.CYAN}Limit: {self.limit} files (for safety){Colors.END}")

        if self.dry_run:
            logger.info(f"{Colors.YELLOW}MODE: DRY RUN{Colors.END}\n")
        else:
            logger.info(f"{Colors.RED}MODE: LIVE RENAME{Colors.END}\n")

        self.scan_and_analyze()
        self.execute_renames()
        self.generate_report()

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"✅ COMPLETE!")
        logger.info(f"{'='*80}{Colors.END}\n")

        logger.info(f"{Colors.BOLD}📊 STATS:{Colors.END}\n")
        logger.info(f"  Analyzed: {Colors.CYAN}{self.stats['analyzed']:,}{Colors.END}")
        logger.info(f"  To Rename: {Colors.CYAN}{len(self.rename_plan):,}{Colors.END}")
        logger.info(f"  Renamed: {Colors.CYAN}{self.stats['renamed']:,}{Colors.END}\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="🧠 Deep Content-Aware Intelligent Renamer"
    )

    parser.add_argument('--target', type=str, required=True, help='Target directory')
    parser.add_argument('--dry-run', action='store_true', default=True, help='Dry run')
    parser.add_argument('--live', action='store_true', help='Apply renames')
    parser.add_argument('--limit', type=int, default=CONSTANT_500, help='Max files to rename')

    args = parser.parse_args()

    renamer = DeepContentRenamer(
        target_dir=args.target,
        dry_run=not args.live,
        limit=args.limit
    )

    renamer.run()


if __name__ == "__main__":
    main()
