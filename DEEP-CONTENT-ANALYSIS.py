#!/usr/bin/env python3
"""
DEEP CONTENT-AWARE ANALYSIS
Analyze what each file REALLY does based on:
- Actual code content
- Imports (what APIs/services used)
- Functions (what operations performed)
- Classes (what objects created)
- Comments and docstrings
"""

import re
import ast
from pathlib import Path
import csv
import json
from collections import defaultdict

class DeepContentAnalyzer:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)

    def deep_analyze_file(self, filepath):
        """Deep analysis of one file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            info = {
                'filename': filepath.name,
                'size_kb': len(content) / 1024,
                'lines': len(content.split('\n')),
            }

            # Extract docstring (real purpose)
            docstrings = re.findall(r'"""(.*?)"""', content, re.DOTALL)
            if docstrings:
                first_doc = docstrings[0].strip()
                info['purpose'] = first_doc.split('\n')[0][:150]
                info['full_docstring'] = first_doc[:500]
            else:
                info['purpose'] = 'No docstring'
                info['full_docstring'] = 'No docstring'

            # Parse AST
            try:
                tree = ast.parse(content)

                # Get classes
                classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                info['classes'] = ', '.join(classes[:5]) if classes else ''
                info['class_count'] = len(classes)

                # Get functions
                functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                info['function_count'] = len(functions)
                info['has_main'] = 'main' in functions

                # Get imports
                imports = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module)

                info['imports'] = ', '.join(list(set(imports))[:15])

            except:
                info['classes'] = 'Parse error'
                info['class_count'] = 0
                info['function_count'] = 0
                info['has_main'] = False
                info['imports'] = 'Parse error'

            # Detect API services from content
            services = self.detect_services(content)
            info['services'] = ', '.join(services) if services else ''

            # Detect operations
            operations = self.detect_operations(content, filepath.name)
            info['operations'] = ', '.join(operations) if operations else ''

            # Detect file type/category
            category = self.categorize_file(info, content)
            info['category'] = category

            # Uses ~/.env.d?
            info['uses_env_d'] = '.env.d' in content or 'env.d' in content

            return info

        except Exception as e:
            return {'filename': filepath.name, 'error': str(e)}

    def detect_services(self, content):
        """Detect which API services are used"""
        services = []
        content_lower = content.lower()

        service_patterns = {
            'OpenAI': ['openai', 'gpt-4', 'gpt-3', 'dall-e'],
            'Anthropic': ['anthropic', 'claude'],
            'Instagram': ['instagram', 'instabot'],
            'YouTube': ['youtube', 'pytube', 'yt-dlp'],
            'Reddit': ['praw', 'reddit'],
            'Telegram': ['telegram', 'pyrogram'],
            'Discord': ['discord.py', 'discord'],
            'Whisper': ['whisper', 'openai.audio'],
            'ElevenLabs': ['elevenlabs', 'eleven'],
            'Suno': ['suno'],
            'Leonardo': ['leonardo'],
            'Stability': ['stability'],
            'AWS': ['boto3', 'aws'],
            'Supabase': ['supabase'],
            'Pinecone': ['pinecone'],
        }

        for service, keywords in service_patterns.items():
            if any(kw in content_lower for kw in keywords):
                services.append(service)

        return services

    def detect_operations(self, content, filename):
        """Detect what operations the file performs"""
        ops = []
        content_lower = content.lower()
        filename_lower = filename.lower()

        op_patterns = {
            'upload': ['upload', 'post', 'publish'],
            'download': ['download', 'fetch', 'scrape'],
            'transcribe': ['transcribe', 'speech_to_text', 'whisper'],
            'generate': ['generate', 'create', 'synthesize'],
            'analyze': ['analyze', 'process', 'parse'],
            'organize': ['organize', 'rename', 'sort', 'cleanup'],
            'merge': ['merge', 'combine', 'consolidate'],
            'convert': ['convert', 'transform'],
            'upscale': ['upscale', 'resize', 'enlarge'],
            'gallery': ['gallery', 'html'],
        }

        for op, keywords in op_patterns.items():
            if any(kw in content_lower or kw in filename_lower for kw in keywords):
                ops.append(op)

        return ops

    def categorize_file(self, info, content):
        """Categorize what type of file this is"""

        services = info.get('services', '').lower()
        ops = info.get('operations', '').lower()
        purpose = info.get('purpose', '').lower()

        # Platform-specific
        if 'instagram' in services: return 'Instagram Automation'
        if 'youtube' in services: return 'YouTube Automation'
        if 'reddit' in services: return 'Reddit Automation'
        if 'telegram' in services: return 'Telegram Bot'

        # AI/Content
        if 'openai' in services or 'anthropic' in services:
            if 'generate' in ops: return 'AI Content Generation'
            if 'transcribe' in ops: return 'AI Transcription'
            return 'AI Tool'

        # Media processing
        if 'upscale' in ops or 'resize' in ops: return 'Image Processing'
        if 'transcribe' in ops: return 'Audio Transcription'
        if 'gallery' in ops: return 'Gallery Generation'

        # File operations
        if 'organize' in ops or 'rename' in ops: return 'File Management'
        if 'merge' in ops: return 'Data Merging'

        # Data
        if 'csv' in content.lower(): return 'CSV Processing'
        if 'pandas' in content.lower(): return 'Data Analysis'

        # Suno
        if 'suno' in services or 'suno' in purpose: return 'Suno Music'

        return 'General Utility'

    def analyze_all(self):
        """Analyze all files"""
        print("🔍 Deep content-aware analysis of all files...\n")

        files = sorted(self.root_dir.glob('*.py'))
        files = [f for f in files if '_BROKEN_' not in f.name and
                 not any(x in f.name for x in ['DEEP_CONTENT', 'STANDARD_ENV'])]

        print(f"Analyzing {len(files)} files\n")

        results = []
        for i, file in enumerate(files, 1):
            if i % 100 == 0:
                print(f"Progress: {i}/{len(files)}")

            analysis = self.deep_analyze_file(file)
            results.append(analysis)

        return results

    def save_reports(self, results):
        """Save comprehensive reports"""

        # CSV report
        csv_path = self.root_dir / "DEEP_CONTENT_ANALYSIS.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['filename', 'category', 'purpose', 'services', 'operations',
                         'classes', 'class_count', 'function_count', 'has_main',
                         'uses_env_d', 'size_kb', 'lines']
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows([r for r in results if not r.get('error')])

        # Category summary
        by_category = defaultdict(list)
        for r in results:
            if not r.get('error'):
                by_category[r.get('category', 'Unknown')].append(r)

        summary_path = self.root_dir / "CATEGORY_SUMMARY.txt"
        with open(summary_path, 'w') as f:
            f.write("FILE CATEGORIZATION SUMMARY\n")
            f.write("=" * 70 + "\n\n")

            for category, files in sorted(by_category.items(), key=lambda x: len(x[1]), reverse=True):
                f.write(f"{category}: {len(files)} files\n")
                for file in sorted(files, key=lambda x: x['filename'])[:10]:
                    f.write(f"  - {file['filename']}\n")
                if len(files) > 10:
                    f.write(f"  ... and {len(files) - 10} more\n")
                f.write("\n")

        return csv_path, summary_path

if __name__ == "__main__":
    root = Path("/Users/steven/Documents/pythons")

    analyzer = DeepContentAnalyzer(root)

    print("=" * 70)
    print("DEEP CONTENT-AWARE ANALYSIS")
    print("=" * 70)
    print()

    results = analyzer.analyze_all()

    print(f"\n📝 Saving reports...")
    csv_path, summary_path = analyzer.save_reports(results)

    print(f"\n✅ Analysis complete!")
    print(f"📄 CSV: {csv_path}")
    print(f"📄 Summary: {summary_path}")

    # Show quick summary
    by_cat = defaultdict(int)
    for r in results:
        if not r.get('error'):
            by_cat[r.get('category', 'Unknown')] += 1

    print(f"\n📊 TOP CATEGORIES:")
    for cat, count in sorted(by_cat.items(), key=lambda x: x[1], reverse=True)[:15]:
        print(f"  {count:3d} files | {cat}")
