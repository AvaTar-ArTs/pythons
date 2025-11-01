
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_033 = 033
CONSTANT_116 = 116
CONSTANT_120 = 120
CONSTANT_300 = 300
CONSTANT_2000 = 2000

#!/usr/bin/env python3
"""
🏷️ INTELLIGENT CONTENT-AWARE RENAMING TOOL
===========================================
AI-Powered Deep Analysis and Smart File Renaming System

Features:
✨ Deep content analysis with AST parsing
✨ AI-powered purpose detection
✨ Semantic understanding of code functionality
✨ Intelligent naming conventions
✨ Context-aware categorization
✨ Safe renaming with backups
✨ Batch processing with preview
"""

import ast
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# Color codes
class Colors:
    HEADER = '\CONSTANT_033[95m'
    BLUE = '\CONSTANT_033[94m'
    CYAN = '\CONSTANT_033[96m'
    GREEN = '\CONSTANT_033[92m'
    YELLOW = '\CONSTANT_033[93m'
    RED = '\CONSTANT_033[91m'
    MAGENTA = '\CONSTANT_033[35m'
    END = '\CONSTANT_033[0m'
    BOLD = '\CONSTANT_033[1m'

# Emojis
class Emojis:
    RENAME = "🏷️"
    BRAIN = "🧠"
    SPARKLES = "✨"
    CHECK = "✅"
    WARNING = "⚠️"
    FIRE = "🔥"
    FOLDER = "📁"
    FILE = "📄"
    ROCKET = "🚀"
    MICROSCOPE = "🔬"
    MAGIC = "🪄"


class IntelligentRenamer:
    """AI-Powered Intelligent File Renaming System"""

    # Category-based organization (inspired by existing folder structure)
    CATEGORIES = {
        '01_core_tools': ['manager', 'organizer', 'analyzer', 'explorer', 'consolidator'],
        '02_youtube_automation': ['youtube', 'video', 'shorts', 'reddit', 'tiktok'],
        '03_ai_creative_tools': ['ai', 'image', 'leonardo', 'dalle', 'comic', 'generator'],
        '04_web_scraping': ['scraper', 'crawler', 'downloader', 'api_client'],
        '05_automation': ['bot', 'automation', 'scheduler', 'workflow'],
        '06_data_processing': ['processor', 'converter', 'transformer', 'parser'],
        '07_media_tools': ['audio', 'video', 'image', 'upscaler', 'converter'],
        '08_utilities': ['utility', 'helper', 'tool', 'script'],
    }

    # Naming patterns based on user's preferred style
    # Examples: openai_file_categorizer, open_source_mp3_pipeline, pip_build_environment
    NAMING_PATTERNS = {
        'automation': '{platform}_{task}_automation',
        'scraper': '{platform}_{content_type}_scraper',
        'api_client': '{service}_api_client',
        'bot': '{platform}_{purpose}_bot',
        'analyzer': '{subject}_content_analyzer',
        'generator': '{platform}_{content_type}_generator',
        'processor': '{source}_{format}_processor',
        'pipeline': '{source}_{format}_pipeline',
        'downloader': '{platform}_{content}_downloader',
        'uploader': '{platform}_{content}_uploader',
        'converter': '{input_format}_to_{output_format}_converter',
        'categorizer': '{service}_{target}_categorizer',
        'manager': '{resource}_content_manager',
        'handler': '{event}_request_handler',
        'service': '{platform}_{purpose}_service',
        'tool': '{function}_{target}_tool',
        'utility': '{purpose}_utility',
        'helper': '{domain}_helper',
        'script': '{task}_automation_script',
        'organizer': '{target}_file_organizer',
        'explorer': '{subject}_file_explorer',
        'environment': '{tool}_build_environment',
        'prompter': '{domain}_ai_prompter',
        'upscaler': '{platform}_image_upscaler',
    }

    def __init__(self, target_dir: str, dry_run: bool = True,
                 interactive: bool = True, use_ai: bool = True,
                 categorize: bool = False):
        self.target_dir = Path(target_dir)
        self.dry_run = dry_run
        self.interactive = interactive
        self.use_ai = use_ai
        self.categorize = categorize  # Move files to category folders

        # Load API keys (inspired by envctl.py patterns)
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.rename_log_file = self.target_dir / f"RENAME_LOG_{timestamp}.json"
        self.undo_script = self.target_dir / f"UNDO_RENAMES_{timestamp}.sh"

        self.stats = {
            'files_analyzed': 0,
            'files_renamed': 0,
            'files_skipped': 0,
            'ai_suggestions': 0,
            'pattern_matches': 0,
            'files_categorized': 0,
            'ambiguous_names': 0
        }

        self.rename_plan = []
        self.skipped_files = []
        self.undo_commands = []  # For rollback capability

    def print_header(self, text: str, color=Colors.CYAN, emoji=""):
        """Print fancy headers"""
        logger.info(f"\n{color}{Colors.BOLD}{'='*80}")
        logger.info(f"{emoji} {text}")
        logger.info(f"{'='*80}{Colors.END}\n")

    def deep_analyze_file(self, filepath: Path) -> Dict[str, Any]:
        """Deep content analysis of Python file"""

        analysis = {
            'path': str(filepath),
            'original_name': filepath.name,
            'size': filepath.stat().st_size,
            'functions': [],
            'classes': [],
            'imports': [],
            'main_purpose': None,
            'docstring': None,
            'patterns': [],
            'keywords': [],
            'suggested_name': None,
            'confidence': 0.0
        }

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # AST Analysis
            tree = ast.parse(content)
            analysis['docstring'] = ast.get_docstring(tree)

            # Extract functions and classes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis['functions'].append(node.name)
                elif isinstance(node, ast.ClassDef):
                    analysis['classes'].append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        analysis['imports'].append(node.module)

            # Detect patterns from imports and functions
            analysis['patterns'] = self.detect_patterns(analysis)

            # Extract keywords from docstring and function names
            analysis['keywords'] = self.extract_keywords(analysis, content)

            # Generate suggested name
            if self.use_ai and (self.openai_key or self.gemini_key or self.anthropic_key):
                ai_suggestion = self.get_ai_suggestion(filepath, analysis, content[:CONSTANT_2000])
                if ai_suggestion:
                    analysis.update(ai_suggestion)
                    self.stats['ai_suggestions'] += 1

            # Fallback to pattern-based naming
            if not analysis['suggested_name']:
                analysis['suggested_name'] = self.generate_pattern_name(analysis)
                self.stats['pattern_matches'] += 1

            # Clean up the name
            if analysis['suggested_name']:
                analysis['suggested_name'] = self.clean_filename(analysis['suggested_name'])

        except Exception as e:
            analysis['error'] = str(e)

        return analysis

    def detect_patterns(self, analysis: Dict) -> List[str]:
        """Detect code patterns from imports and structure (enhanced from intelligent_consolidator.py)"""
        patterns = []
        imports = [imp.lower() for imp in analysis['imports']]
        functions = [f.lower() for f in analysis['functions']]
        all_text = ' '.join(functions + imports).lower()

        # YouTube/Video (from aliases.sh insights)
        if any(lib in all_text for lib in ['youtube', 'pytube', 'yt-dlp', 'moviepy']):
            patterns.append('youtube_automation')

        # Instagram/Social Media
        if any(lib in all_text for lib in ['instagram', 'instapy', 'discord', 'telegram', 'tweepy']):
            patterns.append('bot')

        # Web scraping (enhanced)
        if any(lib in imports for lib in ['beautifulsoup', 'bs4', 'selenium', 'scrapy', 'playwright']):
            patterns.append('scraper')

        # API clients (enhanced)
        if any(lib in imports for lib in ['requests', 'httpx', 'aiohttp']):
            if any('api' in f or 'client' in f for f in functions):
                patterns.append('api_client')

        # AI/ML tools (from existing AI tools)
        if any(lib in all_text for lib in ['openai', 'anthropic', 'leonardo', 'dalle', 'stable_diffusion']):
            patterns.append('ai_tool')

        # Data processing (enhanced)
        if any(lib in imports for lib in ['pandas', 'numpy', 'polars']):
            patterns.append('processor')

        # Image processing (enhanced from leonardo/dalle patterns)
        if any(lib in imports for lib in ['pil', 'pillow', 'opencv', 'cv2']):
            if 'upscale' in all_text:
                patterns.append('upscaler')
            else:
                patterns.append('image_processor')

        # Video processing
        if any(lib in imports for lib in ['moviepy', 'ffmpeg-python']):
            patterns.append('video_processor')

        # File operations (enhanced)
        if any(word in all_text for word in ['download', 'fetch', 'pull']):
            patterns.append('downloader')
        if any(word in all_text for word in ['upload', 'push', 'publish']):
            patterns.append('uploader')

        # Analysis tools (enhanced)
        if any(word in all_text for word in ['analyze', 'analyse', 'inspect', 'audit']):
            patterns.append('analyzer')

        # Generators (enhanced)
        if any(word in all_text for word in ['generate', 'create', 'build', 'make']):
            patterns.append('generator')

        # Organizers/Managers (from existing tools)
        if any(word in all_text for word in ['organize', 'sort', 'categorize']):
            patterns.append('organizer')
        if any(word in all_text for word in ['manage', 'handle', 'control']):
            patterns.append('manager')

        # Automation (enhanced)
        if any(lib in imports for lib in ['schedule', 'cron', 'apscheduler']):
            patterns.append('automation')

        # Explorers (from simple_python_explorer pattern)
        if any(word in all_text for word in ['explore', 'browse', 'navigate']):
            patterns.append('explorer')

        return patterns

    def extract_keywords(self, analysis: Dict, content: str) -> List[str]:
        """Extract meaningful keywords from content (FIXED - skip shebangs/imports!)"""
        keywords = []

        # From docstring (first priority)
        if analysis['docstring']:
            # Extract meaningful nouns and verbs from docstring
            words = re.findall(r'\b[a-z]{4,}\b', analysis['docstring'].lower())
            keywords.extend(words[:8])

        # From class names (high priority - usually descriptive)
        for cls in analysis['classes'][:5]:
            # Skip generic class names
            if cls.lower() not in ['base', 'main', 'config', 'utils']:
                keywords.extend(re.findall(r'[a-z]+', cls.lower()))

        # From function names (moderate priority)
        for func in analysis['functions'][:10]:
            # Skip dunder methods and generic names
            if not func.startswith('__') and func.lower() not in ['main', 'run', 'init']:
                keywords.extend(re.findall(r'[a-z]+', func.lower()))

        # Platform/service detection (from imports)
        services = ['youtube', 'instagram', 'facebook', 'twitter', 'reddit',
                   'discord', 'telegram', 'leonardo', 'openai', 'dalle',
                   'elevenlabs', 'whisper', 'tiktok', 'twitch']
        for service in services:
            if service in ' '.join(analysis['imports']).lower():
                keywords.insert(0, service)  # High priority

        # Content type detection
        content_types = ['image', 'video', 'audio', 'text', 'file', 'data',
                        'mp3', 'mp4', 'csv', 'json', 'pdf']
        for ctype in content_types:
            if ctype in content.lower():
                keywords.append(ctype)

        # Action words (from function names)
        actions = ['upload', 'download', 'analyze', 'generate', 'process',
                  'convert', 'scrape', 'organize', 'manage', 'create']
        for action in actions:
            if action in ' '.join(analysis['functions']).lower():
                keywords.append(action)

        # Remove common noise words
        noise = ['usr', 'bin', 'env', 'python', 'python3', 'import', 'from', 'abc',
                're', 'os', 'sys', 'path', 'typing', 'abstractmethod']
        keywords = [k for k in keywords if k not in noise and len(k) > 2]

        return list(dict.fromkeys(keywords))[:10]  # Unique, top 10

    def get_ai_suggestion(self, filepath: Path, analysis: Dict, content_preview: str) -> Optional[Dict]:
        """Use AI to suggest intelligent file name"""

        prompt = f"""Analyze this Python file and suggest a clear, descriptive filename.

Original name: {filepath.name}
Functions: {', '.join(analysis['functions'][:10])}
Classes: {', '.join(analysis['classes'][:5])}
Imports: {', '.join(analysis['imports'][:10])}
Patterns detected: {', '.join(analysis['patterns'])}

Code preview:
```python
{content_preview}
```

Provide a JSON response with:
{{
    "suggested_name": "descriptive_snake_case_name.py",
    "main_purpose": "brief description of what this file does",
    "confidence": 0.0-1.0
}}

Use clear, descriptive names following these patterns:
- {"{service}"}_api_client.py for API clients
- {"{platform}"}_bot.py for bots
- {"{subject}"}_analyzer.py for analyzers
- {"{output}"}_generator.py for generators
- {"{task}"}_automation.py for automation scripts
"""

        try:
            if self.openai_key:
                return self._query_openai(prompt)
            elif self.gemini_key:
                return self._query_gemini(prompt)
            elif self.anthropic_key:
                return self._query_anthropic(prompt)
        except Exception as e:
            logger.info(f"{Colors.YELLOW}AI suggestion failed: {e}{Colors.END}")

        return None

    def _query_openai(self, prompt: str) -> Optional[Dict]:
        """Query OpenAI for name suggestion"""
        try:
            import openai
            openai.api_key = self.openai_key

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert at naming Python files based on their functionality. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=CONSTANT_300
            )

            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            return None

    def _query_gemini(self, prompt: str) -> Optional[Dict]:
        """Query Gemini for name suggestion"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_key)

            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)

            # Extract JSON from response
            text = response.text
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            return None

        return None

    def _query_anthropic(self, prompt: str) -> Optional[Dict]:
        """Query Claude for name suggestion"""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.anthropic_key)

            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=CONSTANT_300,
                messages=[{"role": "user", "content": prompt}]
            )

            return json.loads(response.content[0].text)
        except Exception as e:
            return None

    def generate_pattern_name(self, analysis: Dict) -> str:
        """Generate name based on detected patterns (user's preferred descriptive style)"""

        # If original name is already good (descriptive, clear), keep it!
        original = analysis['original_name'].lower()
        if len(original) >= 15 and ('_' in original or '-' in original):
            # Check if it's already descriptive
            if not any(bad in original for bad in ['temp', 'test', 'old', 'backup', 'copy',
                                                    '2', '-.py', '..py', 'untitled']):
                # Original name is good, just clean it up
                return self.clean_filename(analysis['original_name'])

        if not analysis['patterns']:
            # Use keywords - be descriptive
            if len(analysis['keywords']) >= 2:
                return f"{analysis['keywords'][0]}_{analysis['keywords'][1]}_tool.py"
            elif analysis['keywords']:
                return f"{analysis['keywords'][0]}_utility.py"
            if analysis['functions'] and len(analysis['functions']) > 0:
                # Use main function if descriptive
                main_func = analysis['functions'][0]
                if len(main_func) > 5 and main_func not in ['main', 'init', 'setup']:
                    return f"{main_func}_script.py"
            # Keep original if nothing better found
            return analysis['original_name']

        pattern = analysis['patterns'][0]
        keywords = analysis['keywords']

        # Build descriptive names matching user's style
        # Examples: openai_file_categorizer, open_source_mp3_pipeline

        if pattern == 'youtube_automation':
            platform = 'youtube'
            content = keywords[1] if len(keywords) > 1 else 'video'
            return f"{platform}_{content}_automation.py"

        elif pattern == 'scraper':
            source = keywords[0] if keywords else 'web'
            content_type = keywords[1] if len(keywords) > 1 else 'content'
            return f"{source}_{content_type}_scraper.py"

        elif pattern == 'bot':
            platform = keywords[0] if keywords else 'social'
            purpose = keywords[1] if len(keywords) > 1 else 'automation'
            return f"{platform}_{purpose}_bot.py"

        elif pattern == 'api_client':
            service = keywords[0] if keywords else 'api'
            return f"{service}_api_client.py"

        elif pattern == 'ai_tool':
            service = keywords[0] if keywords and keywords[0] in ['openai', 'leonardo', 'dalle'] else 'ai'
            purpose = keywords[1] if len(keywords) > 1 else 'generator'
            return f"{service}_{purpose}_tool.py"

        elif pattern == 'analyzer':
            subject = keywords[0] if keywords else 'data'
            return f"{subject}_content_analyzer.py"

        elif pattern == 'generator':
            content_type = keywords[0] if keywords else 'content'
            style = keywords[1] if len(keywords) > 1 else 'ai'
            return f"{style}_{content_type}_generator.py"

        elif pattern == 'processor':
            input_type = keywords[0] if keywords else 'file'
            operation = keywords[1] if len(keywords) > 1 else 'processor'
            return f"{input_type}_{operation}_processor.py"

        elif pattern == 'upscaler':
            source = keywords[0] if keywords else 'image'
            return f"{source}_image_upscaler.py"

        elif pattern == 'downloader':
            platform = keywords[0] if keywords else 'web'
            content = keywords[1] if len(keywords) > 1 else 'file'
            return f"{platform}_{content}_downloader.py"

        elif pattern == 'uploader':
            platform = keywords[0] if keywords else 'cloud'
            content = keywords[1] if len(keywords) > 1 else 'file'
            return f"{platform}_{content}_uploader.py"

        elif pattern == 'organizer':
            target = keywords[0] if keywords else 'file'
            return f"{target}_file_organizer.py"

        elif pattern == 'manager':
            resource = keywords[0] if keywords else 'resource'
            return f"{resource}_content_manager.py"

        elif pattern == 'explorer':
            subject = keywords[0] if keywords else 'file'
            return f"{subject}_file_explorer.py"

        elif pattern == 'automation':
            platform = keywords[0] if keywords else 'task'
            action = keywords[1] if len(keywords) > 1 else 'automation'
            return f"{platform}_{action}_automation.py"

        # Default: descriptive pattern_keyword_tool format
        keyword = keywords[0] if keywords else 'content'
        return f"{keyword}_{pattern}_tool.py"

    def clean_filename(self, name: str) -> str:
        """Clean and validate filename (user's examples: YouTubeBot, content_analyzer_v2, deep_organizer)"""

        # Preserve original case for proper nouns (YouTubeBot, WhisperTranscriber)
        has_capitals = any(c.isupper() for c in name)

        # Remove redundant words (based on user examples)
        redundant_words = ['enhanced_', 'simple_', 'comprehensive_', 'fixed_',
                          'direct_', '_read_', '_deep_read']
        for word in redundant_words:
            name = name.replace(word, '')

        # Clean up version numbers: _1.py → .py or _v1.py
        name = re.sub(r'_(\d+)\.py$', r'_v\1.py', name)

        # If it has proper case (like YouTubeBot), preserve it
        if has_capitals and not name.startswith(('usr-', 'from-', 'import-')):
            # Just clean special chars
            name = re.sub(r'[^\w\-.]', '_', name)
        else:
            # Convert to lowercase
            name = name.lower()
            # Preserve hyphens and underscores, replace other special chars
            name = re.sub(r'[^\w\-.]', '_', name)

        # Remove multiple underscores/hyphens
        name = re.sub(r'_+', '_', name)
        name = re.sub(r'\-+', '-', name)

        # Remove leading/trailing underscores/hyphens
        name = name.strip('_').strip('-')

        # Ensure .py extension
        if not name.endswith('.py'):
            name += '.py'

        # User prefers descriptive names
        if len(name) > CONSTANT_120:
            name = name[:CONSTANT_116] + '.py'

        return name

    def scan_and_analyze(self) -> List[Dict]:
        """Scan directory and analyze files for renaming"""

        self.print_header("SCANNING AND ANALYZING FILES", Colors.CYAN, Emojis.MICROSCOPE)

        python_files = []

        for root, dirs, files in os.walk(self.target_dir):
            # Skip certain directories
            dirs[:] = [d for d in dirs if not d.startswith(('.', '__pycache__', 'node_modules',
                                                           'merge_backup_', 'merge_analysis_',
                                                           'dedup_backup', 'ai_diff_reports_'))]

            for filename in files:
                if filename.endswith('.py') and not filename.startswith('.'):
                    filepath = Path(root) / filename
                    python_files.append(filepath)

        logger.info(f"{Colors.GREEN}Found {len(python_files)} Python files{Colors.END}\n")

        # Analyze each file
        analyses = []
        for idx, filepath in enumerate(python_files, 1):
            if idx % 10 == 0:
                logger.info(f"{Colors.YELLOW}Analyzing: {idx}/{len(python_files)}...{Colors.END}", end='\r')

            analysis = self.deep_analyze_file(filepath)
            self.stats['files_analyzed'] += 1

            # Only suggest rename if name would change
            if analysis['suggested_name'] and \
               analysis['suggested_name'] != analysis['original_name']:
                analyses.append(analysis)

        logger.info(f"\n{Colors.GREEN}Analysis complete! Found {len(analyses)} files to rename{Colors.END}")

        return analyses

    def determine_category(self, patterns: List[str]) -> Optional[str]:
        """Determine which category folder a file belongs to"""
        for category, keywords in self.CATEGORIES.items():
            for pattern in patterns:
                if any(keyword in pattern for keyword in keywords):
                    return category
        return None

    def create_rename_plan(self, analyses: List[Dict]) -> None:
        """Create intelligent rename plan with category awareness"""

        self.print_header("CREATING INTELLIGENT RENAME PLAN", Colors.YELLOW, Emojis.BRAIN)

        for analysis in analyses:
            old_path = Path(analysis['path'])
            new_name = analysis['suggested_name']

            # Detect BAD automated names (like usr-bin-env-python3.py!)
            if any(bad in new_name for bad in ['usr-bin', 'import-', 'from-', 'for-the']):
                # Skip terrible auto-generated names - keep original
                logger.info(f"{Colors.RED}❌ BAD AUTO-NAME: {new_name} → keeping original {analysis['original_name']}{Colors.END}")
                continue

            # Detect ambiguous names (user prefers descriptive names like openai_file_categorizer)
            # Should be at least 10 chars and have underscores/hyphens (unless ProperCase like YouTubeBot)
            has_capitals = any(c.isupper() for c in new_name)
            if not has_capitals and (len(new_name) < 10 or (new_name.count('_') == 0 and new_name.count('-') == 0)):
                self.stats['ambiguous_names'] += 1
                logger.info(f"{Colors.YELLOW}⚠️  Ambiguous: {new_name} (from {analysis['original_name']}){Colors.END}")

            # Determine category if categorization enabled
            parent_dir = old_path.parent
            if self.categorize and analysis['patterns']:
                category = self.determine_category(analysis['patterns'])
                if category:
                    category_path = self.target_dir / category
                    # Only move if not already in correct category
                    if category not in str(old_path.parent):
                        parent_dir = category_path
                        self.stats['files_categorized'] += 1

            new_path = parent_dir / new_name

            # Check if target already exists
            if new_path.exists() and new_path != old_path:
                # Add suffix to avoid collision
                base = new_name[:-3]  # Remove .py
                counter = 2
                while (parent_dir / f"{base}_v{counter}.py").exists():
                    counter += 1
                new_name = f"{base}_v{counter}.py"
                new_path = parent_dir / new_name

            self.rename_plan.append({
                'old_path': old_path,
                'new_path': new_path,
                'old_name': analysis['original_name'],
                'new_name': new_name,
                'purpose': analysis.get('main_purpose', 'No description'),
                'confidence': analysis.get('confidence', 0.5),
                'patterns': analysis['patterns'],
                'category': self.determine_category(analysis['patterns']) if analysis['patterns'] else None,
                'parent_dir': str(old_path.parent.relative_to(self.target_dir))
            })

    def execute_rename_plan(self) -> None:
        """Execute the rename plan"""

        self.print_header("EXECUTING RENAME PLAN", Colors.GREEN, Emojis.MAGIC)

        logger.info(f"{Colors.YELLOW}Total renames: {len(self.rename_plan)}{Colors.END}")
        logger.info(f"{Colors.CYAN}Mode: {'DRY RUN' if self.dry_run else 'LIVE RENAME'}{Colors.END}\n")

        # Sort by confidence (high confidence first)
        sorted_plan = sorted(self.rename_plan, key=lambda x: x['confidence'], reverse=True)

        for idx, item in enumerate(sorted_plan, 1):
            logger.info(f"\n{Colors.BOLD}[{idx}/{len(sorted_plan)}]{Colors.END}")
            logger.info(f"Old: {Colors.RED}{item['old_name']}{Colors.END}")
            logger.info(f"New: {Colors.GREEN}{item['new_name']}{Colors.END}")
            if item['parent_dir'] and item['parent_dir'] != '.':
                logger.info(f"Dir: {Colors.CYAN}{item['parent_dir']}/{Colors.END}")
            logger.info(f"Purpose: {item['purpose']}")
            logger.info(f"Confidence: {Colors.YELLOW}{item['confidence']:.2f}{Colors.END}")
            if item['patterns']:
                logger.info(f"Patterns: {', '.join(item['patterns'])}")

            # Interactive confirmation
            if self.interactive:
                logger.info(f"\n{Colors.CYAN}Options:{Colors.END}")
                logger.info("  [y] Yes, rename")
                logger.info("  [n] No, skip")
                logger.info("  [e] Edit name")
                logger.info("  [q] Quit")

                choice = input(f"\n{Colors.BOLD}Choice: {Colors.END}").lower().strip()

                if choice == 'q':
                    logger.info(f"{Colors.YELLOW}Renaming aborted{Colors.END}")
                    return
                elif choice == 'n':
                    logger.info(f"{Colors.YELLOW}Skipped{Colors.END}")
                    self.skipped_files.append(item)
                    self.stats['files_skipped'] += 1
                    continue
                elif choice == 'e':
                    new_name = input(f"Enter new name: ").strip()
                    if new_name:
                        item['new_name'] = self.clean_filename(new_name)
                        item['new_path'] = item['old_path'].parent / item['new_name']

            # Perform rename
            try:
                if not self.dry_run:
                    # Ensure target directory exists
                    item['new_path'].parent.mkdir(parents=True, exist_ok=True)

                    # Generate undo command
                    self.undo_commands.append(
                        f"mv '{item['new_path']}' '{item['old_path']}'"
                    )

                    # Perform rename
                    item['old_path'].rename(item['new_path'])
                    logger.info(f"{Colors.GREEN}{Emojis.CHECK} Renamed successfully{Colors.END}")

                    if item.get('category'):
                        logger.info(f"{Colors.CYAN}  → Categorized to: {item['category']}{Colors.END}")
                else:
                    logger.info(f"{Colors.YELLOW}[DRY RUN] Would rename{Colors.END}")
                    if item.get('category'):
                        logger.info(f"{Colors.YELLOW}[DRY RUN] Would move to: {item['category']}{Colors.END}")

                self.stats['files_renamed'] += 1

            except Exception as e:
                logger.info(f"{Colors.RED}{Emojis.WARNING} Error: {e}{Colors.END}")
                self.skipped_files.append(item)
                self.stats['files_skipped'] += 1

    def generate_report(self) -> str:
        """Generate rename report"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.target_dir / f"RENAME_REPORT_{timestamp}.md"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 🏷️ INTELLIGENT RENAME REPORT\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mode:** {'DRY RUN' if self.dry_run else 'LIVE RENAME'}\n\n")
            f.write("---\n\n")

            # Statistics
            f.write("## 📊 STATISTICS\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| **Files Analyzed** | {self.stats['files_analyzed']:,} |\n")
            f.write(f"| **Files Renamed** | {self.stats['files_renamed']:,} |\n")
            f.write(f"| **Files Skipped** | {self.stats['files_skipped']:,} |\n")
            f.write(f"| **AI Suggestions** | {self.stats['ai_suggestions']:,} |\n")
            f.write(f"| **Pattern Matches** | {self.stats['pattern_matches']:,} |\n\n")

            # Renamed files grouped by directory
            f.write("## ✅ RENAMED FILES\n\n")
            by_dir = defaultdict(list)
            for item in self.rename_plan:
                if item not in self.skipped_files:
                    by_dir[item['parent_dir']].append(item)

            for directory in sorted(by_dir.keys()):
                items = by_dir[directory]
                f.write(f"### 📁 {directory or '(root)'}\n\n")
                for item in items:
                    f.write(f"- `{item['old_name']}` → `{item['new_name']}`\n")
                    f.write(f"  - Purpose: {item['purpose']}\n")
                    f.write(f"  - Confidence: {item['confidence']:.2f}\n\n")

            # Skipped files
            if self.skipped_files:
                f.write("## ⏭️ SKIPPED FILES\n\n")
                for item in self.skipped_files:
                    f.write(f"- `{item['old_name']}`\n")
                    f.write(f"  - Suggested: `{item['new_name']}`\n\n")

        # Save JSON log
        with open(self.rename_log_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'stats': self.stats,
                'rename_plan': [{**item, 'old_path': str(item['old_path']),
                               'new_path': str(item['new_path'])}
                              for item in self.rename_plan]
            }, f, indent=2)

        # Generate undo script (inspired by git safety patterns)
        if self.undo_commands and not self.dry_run:
            with open(self.undo_script, 'w', encoding='utf-8') as f:
                f.write("#!/bin/bash\n")
                f.write("# Undo script for intelligent renaming\n")
                f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("echo '🔄 Undoing file renames...'\n\n")
                for cmd in reversed(self.undo_commands):  # Reverse order for undo
                    f.write(f"{cmd}\n")
                f.write("\necho '✅ Undo complete!'\n")

            # Make executable
            self.undo_script.chmod(0o755)
            logger.info(f"\n{Colors.GREEN}✅ Undo script created: {self.undo_script}{Colors.END}")

        return str(report_file)

    def run(self) -> None:
        """Run the intelligent renaming process"""

        # Banner
        logger.info(f"{Colors.BOLD}{Colors.MAGENTA}")
        logger.info("╔═══════════════════════════════════════════════════════════════════════════════╗")
        logger.info("║                                                                               ║")
        logger.info("║              🏷️  INTELLIGENT CONTENT-AWARE RENAMER 🧠                        ║")
        logger.info("║                                                                               ║")
        logger.info("║           AI-Powered Deep Analysis and Smart File Renaming                   ║")
        logger.info("║                                                                               ║")
        logger.info("╚═══════════════════════════════════════════════════════════════════════════════╝")
        logger.info(f"{Colors.END}\n")

        logger.info(f"{Colors.CYAN}{Emojis.FOLDER} Target: {self.target_dir}{Colors.END}")
        logger.info(f"{Colors.CYAN}AI Enabled: {'Yes' if self.use_ai else 'No'}{Colors.END}")

        if self.dry_run:
            logger.info(f"{Colors.YELLOW}{Emojis.WARNING} MODE: DRY RUN (no files will be renamed){Colors.END}")
        else:
            logger.info(f"{Colors.RED}{Emojis.WARNING} MODE: LIVE RENAME (files will be renamed!){Colors.END}")

        logger.info(f"{Colors.CYAN}Interactive: {'Yes' if self.interactive else 'No'}{Colors.END}\n")

        # Analyze files
        analyses = self.scan_and_analyze()

        if not analyses:
            logger.info(f"{Colors.GREEN}{Emojis.CHECK} All files already have good names!{Colors.END}")
            return

        # Create rename plan
        self.create_rename_plan(analyses)

        # Execute renames
        self.execute_rename_plan()

        # Generate report
        self.print_header("GENERATING REPORT", Colors.BLUE, Emojis.SPARKLES)
        report_file = self.generate_report()

        # Final summary
        self.print_header("RENAMING COMPLETE!", Colors.GREEN, Emojis.ROCKET)

        logger.info(f"{Colors.BOLD}📊 FINAL STATISTICS:{Colors.END}\n")
        logger.info(f"  {Emojis.MICROSCOPE} Analyzed: {Colors.CYAN}{self.stats['files_analyzed']:,}{Colors.END}")
        logger.info(f"  {Emojis.RENAME} Renamed: {Colors.CYAN}{self.stats['files_renamed']:,}{Colors.END}")
        logger.info(f"  {Emojis.BRAIN} AI Suggestions: {Colors.CYAN}{self.stats['ai_suggestions']:,}{Colors.END}")
        logger.info(f"  {Emojis.FIRE} Pattern Matches: {Colors.CYAN}{self.stats['pattern_matches']:,}{Colors.END}")
        logger.info(f"  📁 Categorized: {Colors.CYAN}{self.stats['files_categorized']:,}{Colors.END}")
        logger.info(f"  ⚠️  Ambiguous: {Colors.CYAN}{self.stats['ambiguous_names']:,}{Colors.END}")
        logger.info(f"  ⏭️  Skipped: {Colors.CYAN}{self.stats['files_skipped']:,}{Colors.END}\n")

        logger.info(f"{Colors.BOLD}📝 OUTPUTS:{Colors.END}\n")
        logger.info(f"  {Emojis.FILE} Report: {Colors.BLUE}{report_file}{Colors.END}")
        logger.info(f"  {Emojis.FILE} JSON Log: {Colors.BLUE}{self.rename_log_file}{Colors.END}")
        if self.undo_script.exists():
            logger.info(f"  🔄 Undo Script: {Colors.BLUE}{self.undo_script}{Colors.END}")
        print()

        if self.dry_run:
            logger.info(f"{Colors.YELLOW}{Emojis.WARNING} This was a DRY RUN. Use --live to actually rename files.{Colors.END}\n")
        else:
            logger.info(f"{Colors.GREEN}{Emojis.CHECK} Renaming complete!{Colors.END}\n")


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(
        description="🏷️ Intelligent Content-Aware Renamer - AI-Powered Smart File Renaming",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--target', type=str, default=Path("/Users/steven/Documents/python"),
                       help='Target directory (default: ~/Documents/python)')
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Dry run mode (default, safe)')
    parser.add_argument('--live', action='store_true',
                       help='Live mode (actually renames files)')
    parser.add_argument('--interactive', action='store_true', default=True,
                       help='Interactive mode (asks for confirmation)')
    parser.add_argument('--batch', action='store_true',
                       help='Batch mode (no confirmation)')
    parser.add_argument('--no-ai', action='store_true',
                       help='Disable AI suggestions (pattern-based only)')
    parser.add_argument('--categorize', action='store_true',
                       help='Move files to category folders (01_core_tools/, etc.)')

    args = parser.parse_args()

    # Load environment
    env_file = Path("/Users/steven/.env.d/MASTER_CONSOLIDATED.env")
    if Path(env_file).exists():
        for line in open(env_file):
            if line.startswith('export '):
                line = line.replace('export ', '').strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    value = value.strip('"').strip("'").split('#')[0].strip()
                    os.environ[key] = value

    dry_run = not args.live
    interactive = not args.batch
    use_ai = not args.no_ai

    renamer = IntelligentRenamer(
        target_dir=args.target,
        dry_run=dry_run,
        interactive=interactive,
        use_ai=use_ai,
        categorize=args.categorize
    )

    renamer.run()


if __name__ == "__main__":
    main()
