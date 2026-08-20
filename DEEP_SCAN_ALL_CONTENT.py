#!/usr/bin/env python3
"""
🔍 DEEP SCAN ALL CONTENT - COMPREHENSIVE ANALYSIS
Full scan of entire Python ecosystem with detailed CSV output

Analyzes:
- File metadata (size, lines, location)
- Imports and dependencies
- Functions and classes
- API integrations detected
- Complexity metrics
- Purpose inference from content
- Category suggestions
"""

import ast
import os
import re
from pathlib import Path
from datetime import datetime
import csv
import hashlib
from collections import defaultdict

class DeepContentScanner:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)
        self.results = []
        self.stats = defaultdict(int)

        # API detection patterns
        self.api_patterns = {
            'openai': r'openai|gpt-4|gpt-3|chatgpt|dall-e',
            'anthropic': r'anthropic|claude',
            'google_ai': r'google\.generativeai|gemini|palm',
            'groq': r'groq',
            'elevenlabs': r'elevenlabs|eleven',
            'assemblyai': r'assemblyai',
            'deepgram': r'deepgram',
            'whisper': r'whisper',
            'leonardo': r'leonardo',
            'stability': r'stability\.ai|stable.diffusion',
            'midjourney': r'midjourney',
            'suno': r'suno',
            'streamlit': r'streamlit',
            'selenium': r'selenium',
            'playwright': r'playwright',
            'beautifulsoup': r'beautifulsoup|bs4',
            'instagram': r'instagram|instabot',
            'youtube': r'youtube|pytube',
            'reddit': r'reddit|praw',
            'twitter': r'twitter|tweepy',
            'facebook': r'facebook',
            'tiktok': r'tiktok',
            'aws': r'boto3|aws',
            'firebase': r'firebase',
            'mongodb': r'mongodb|pymongo',
            'postgresql': r'postgresql|psycopg',
            'mysql': r'mysql',
            'ffmpeg': r'ffmpeg',
            'pillow': r'PIL|pillow',
            'opencv': r'cv2|opencv',
            'pandas': r'pandas',
            'numpy': r'numpy',
            'requests': r'requests',
            'flask': r'flask',
            'fastapi': r'fastapi',
            'django': r'django',
        }

        # Purpose inference patterns
        self.purpose_patterns = {
            'audio_generation': r'text.to.speech|tts|audio.generat|speech.synth',
            'audio_transcription': r'transcribe|speech.to.text|audio.to.text',
            'image_generation': r'image.generat|dall.?e|leonardo|create.image',
            'image_processing': r'image.process|resize|upscale|compress|convert',
            'video_processing': r'video.process|ffmpeg|video.edit|compress',
            'web_scraping': r'scrap|crawl|extract|fetch|download',
            'social_media': r'instagram|twitter|facebook|tiktok|social',
            'automation': r'automat|bot|schedul',
            'data_analysis': r'analyz|analis|report|statistic',
            'file_organization': r'organiz|sort|categoriz|rename|clean',
            'api_client': r'api.client|endpoint|request',
            'content_generation': r'content.generat|creat.content|write',
            'gallery': r'gallery|album|catalog',
        }

    def scan_file(self, filepath):
        """Deep scan a single Python file"""
        result = {
            'filename': filepath.name,
            'full_path': str(filepath),
            'relative_path': str(filepath.relative_to(self.pythons_dir)),
            'parent_folder': filepath.parent.name,
            'size_bytes': 0,
            'size_kb': 0,
            'lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0,
            'imports': [],
            'import_count': 0,
            'functions': [],
            'function_count': 0,
            'classes': [],
            'class_count': 0,
            'has_main': False,
            'has_docstring': False,
            'has_type_hints': False,
            'error_handling': 0,
            'apis_used': [],
            'inferred_purpose': [],
            'complexity_score': 0,
            'file_hash': '',
            'last_modified': '',
            'parse_error': None
        }

        try:
            # File metadata
            stats = filepath.stat()
            result['size_bytes'] = stats.st_size
            result['size_kb'] = round(stats.st_size / 1024, 2)
            result['last_modified'] = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

            # Read content
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # File hash
            result['file_hash'] = hashlib.md5(content.encode()).hexdigest()

            # Line counts
            lines = content.splitlines()
            result['lines'] = len(lines)

            for line in lines:
                stripped = line.strip()
                if not stripped:
                    result['blank_lines'] += 1
                elif stripped.startswith('#'):
                    result['comment_lines'] += 1
                else:
                    result['code_lines'] += 1

            # Parse AST
            try:
                tree = ast.parse(content)
                ast_results = self._analyze_ast(tree)
                result.update(ast_results)
            except SyntaxError as e:
                result['parse_error'] = f"Syntax error: {str(e)}"
            except Exception as e:
                result['parse_error'] = f"Parse error: {str(e)}"

            # Detect APIs
            result['apis_used'] = self._detect_apis(content)

            # Infer purpose
            result['inferred_purpose'] = self._infer_purpose(content, filepath.name)

            # Calculate complexity
            result['complexity_score'] = self._calculate_complexity(result)

        except Exception as e:
            result['parse_error'] = f"File error: {str(e)}"

        return result

    def _analyze_ast(self, tree):
        """Analyze Python AST"""
        result = {
            'imports': [],
            'functions': [],
            'classes': [],
            'has_main': False,
            'has_docstring': False,
            'has_type_hints': False,
            'error_handling': 0
        }

        # Module docstring
        result['has_docstring'] = bool(ast.get_docstring(tree))

        for node in ast.walk(tree):
            # Imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    result['imports'].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                result['imports'].append(module)

            # Functions
            elif isinstance(node, ast.FunctionDef):
                func_name = node.name
                result['functions'].append(func_name)

                # Check for main
                if func_name == 'main':
                    result['has_main'] = True

                # Check for type hints
                if node.returns or any(arg.annotation for arg in node.args.args):
                    result['has_type_hints'] = True

            # Classes
            elif isinstance(node, ast.ClassDef):
                result['classes'].append(node.name)

            # Error handling
            elif isinstance(node, (ast.Try, ast.ExceptHandler)):
                result['error_handling'] += 1

        result['import_count'] = len(result['imports'])
        result['function_count'] = len(result['functions'])
        result['class_count'] = len(result['classes'])

        return result

    def _detect_apis(self, content):
        """Detect API integrations"""
        apis = []
        content_lower = content.lower()

        for api, pattern in self.api_patterns.items():
            if re.search(pattern, content_lower):
                apis.append(api)

        return apis

    def _infer_purpose(self, content, filename):
        """Infer file purpose from content and filename"""
        purposes = []
        text = (content + ' ' + filename).lower()

        for purpose, pattern in self.purpose_patterns.items():
            if re.search(pattern, text):
                purposes.append(purpose)

        return purposes

    def _calculate_complexity(self, result):
        """Calculate complexity score"""
        score = 0

        # Size factors
        score += min(result['code_lines'] / 10, 50)
        score += result['function_count'] * 2
        score += result['class_count'] * 5
        score += result['import_count'] * 1

        # Quality factors
        if result['has_docstring']:
            score += 10
        if result['has_main']:
            score += 5
        if result['has_type_hints']:
            score += 10
        score += result['error_handling'] * 3

        # API integration
        score += len(result['apis_used']) * 5

        return round(score, 2)

    def scan_all_files(self):
        """Scan all Python files in the ecosystem"""
        print("🔍 Starting deep scan of entire Python ecosystem...\n")

        # Find all .py files
        all_files = list(self.pythons_dir.rglob('*.py'))
        total = len(all_files)

        print(f"📂 Found {total} Python files to scan\n")
        print("⏳ This will take a few minutes for deep analysis...\n")

        for i, filepath in enumerate(all_files, 1):
            result = self.scan_file(filepath)
            self.results.append(result)

            # Update stats
            self.stats['total_scanned'] += 1
            self.stats['total_size'] += result['size_bytes']
            self.stats['total_lines'] += result['lines']
            self.stats['total_functions'] += result['function_count']
            self.stats['total_classes'] += result['class_count']

            if result['parse_error']:
                self.stats['parse_errors'] += 1

            # Progress indicator
            if i % 100 == 0:
                print(f"   ... scanned {i}/{total} files ({i*100//total}%)")

        print(f"\n✅ Scan complete! Analyzed {total} files\n")
        return len(self.results)

    def save_detailed_csv(self):
        """Save detailed CSV report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_file = self.pythons_dir / f'DEEP_SCAN_DETAILED_{timestamp}.csv'

        print(f"💾 Saving detailed CSV report...\n")

        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'filename', 'full_path', 'relative_path', 'parent_folder',
                'size_kb', 'lines', 'code_lines', 'comment_lines', 'blank_lines',
                'function_count', 'class_count', 'import_count',
                'has_main', 'has_docstring', 'has_type_hints', 'error_handling',
                'complexity_score', 'apis_used', 'inferred_purpose',
                'imports', 'functions', 'classes',
                'file_hash', 'last_modified', 'parse_error'
            ]

            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()

            for result in self.results:
                # Convert lists to strings
                row = result.copy()
                row['apis_used'] = ', '.join(result['apis_used'])
                row['inferred_purpose'] = ', '.join(result['inferred_purpose'])
                row['imports'] = ', '.join(result['imports'][:10])  # First 10 imports
                row['functions'] = ', '.join(result['functions'][:10])  # First 10 functions
                row['classes'] = ', '.join(result['classes'][:10])  # First 10 classes

                writer.writerow(row)

        print(f"✅ Detailed CSV saved: {csv_file.name}\n")
        return csv_file

    def save_summary_csv(self):
        """Save summary CSV by category"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_file = self.pythons_dir / f'DEEP_SCAN_SUMMARY_{timestamp}.csv'

        print(f"📊 Creating summary CSV...\n")

        # Group by parent folder
        by_folder = defaultdict(lambda: {
            'file_count': 0,
            'total_lines': 0,
            'total_functions': 0,
            'total_classes': 0,
            'total_size_kb': 0,
            'apis': set(),
            'purposes': set()
        })

        for result in self.results:
            folder = result['parent_folder']
            by_folder[folder]['file_count'] += 1
            by_folder[folder]['total_lines'] += result['lines']
            by_folder[folder]['total_functions'] += result['function_count']
            by_folder[folder]['total_classes'] += result['class_count']
            by_folder[folder]['total_size_kb'] += result['size_kb']
            by_folder[folder]['apis'].update(result['apis_used'])
            by_folder[folder]['purposes'].update(result['inferred_purpose'])

        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Parent Folder', 'File Count', 'Total Lines', 'Total Functions',
                'Total Classes', 'Total Size (KB)', 'APIs Used', 'Purposes'
            ])

            for folder in sorted(by_folder.keys()):
                data = by_folder[folder]
                writer.writerow([
                    folder,
                    data['file_count'],
                    data['total_lines'],
                    data['total_functions'],
                    data['total_classes'],
                    round(data['total_size_kb'], 2),
                    ', '.join(sorted(data['apis']))[:100],
                    ', '.join(sorted(data['purposes']))[:100]
                ])

        print(f"✅ Summary CSV saved: {csv_file.name}\n")
        return csv_file

    def save_api_usage_csv(self):
        """Save API usage analysis"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_file = self.pythons_dir / f'DEEP_SCAN_API_USAGE_{timestamp}.csv'

        print(f"🔌 Creating API usage CSV...\n")

        # Count API usage
        api_counts = defaultdict(list)
        for result in self.results:
            for api in result['apis_used']:
                api_counts[api].append(result['filename'])

        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['API', 'Usage Count', 'Sample Files'])

            for api in sorted(api_counts.keys(), key=lambda x: len(api_counts[x]), reverse=True):
                files = api_counts[api]
                sample_files = ', '.join(files[:5])
                writer.writerow([api, len(files), sample_files])

        print(f"✅ API usage CSV saved: {csv_file.name}\n")
        return csv_file

    def print_statistics(self):
        """Print scan statistics"""
        print("=" * 70)
        print("📊 DEEP SCAN STATISTICS")
        print("=" * 70)
        print(f"  Total files scanned:    {self.stats['total_scanned']}")
        print(f"  Total size:             {self.stats['total_size'] / (1024*1024):.2f} MB")
        print(f"  Total lines of code:    {self.stats['total_lines']:,}")
        print(f"  Total functions:        {self.stats['total_functions']:,}")
        print(f"  Total classes:          {self.stats['total_classes']:,}")
        print(f"  Parse errors:           {self.stats['parse_errors']}")
        print("=" * 70 + "\n")

        # Top APIs
        api_counts = defaultdict(int)
        for result in self.results:
            for api in result['apis_used']:
                api_counts[api] += 1

        if api_counts:
            print("🔥 TOP 10 API INTEGRATIONS:")
            for api, count in sorted(api_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"   {api:20} {count:4} files")
            print()


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║        🔍 DEEP SCAN ALL CONTENT - COMPREHENSIVE ANALYSIS         ║
║        Full ecosystem scan with detailed CSV output              ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    scanner = DeepContentScanner()

    # Scan all files
    count = scanner.scan_all_files()

    # Print statistics
    scanner.print_statistics()

    # Save reports
    detailed_csv = scanner.save_detailed_csv()
    summary_csv = scanner.save_summary_csv()
    api_csv = scanner.save_api_usage_csv()

    print("=" * 70)
    print("✨ DEEP SCAN COMPLETE!")
    print("=" * 70)
    print(f"📄 Detailed report: {detailed_csv.name}")
    print(f"📊 Summary report:  {summary_csv.name}")
    print(f"🔌 API usage:       {api_csv.name}")
    print("=" * 70)
    print("\nAll CSVs are ready for analysis in Excel, Pandas, or any CSV tool!")


if __name__ == "__main__":
    main()

