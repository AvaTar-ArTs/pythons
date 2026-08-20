#!/usr/bin/env python3
"""
Intelligent Rename Analyzer
Analyzes files that need renaming and provides smart, context-aware suggestions
Handles: ALL_CAPS, generic analyze-, and missing documentation
"""

import csv
import ast
from pathlib import Path
from datetime import datetime

class IntelligentRenameAnalyzer:
    """Smart rename suggestions based on code analysis"""
    
    def __init__(self, needs_renaming_csv):
        self.csv_path = Path(needs_renaming_csv)
        self.pythons_dir = Path.home() / 'pythons'
        self.scripts = []
        self.smart_suggestions = []
        
    def load_csv(self):
        """Load the needs_renaming CSV"""
        with open(self.csv_path, 'r') as f:
            reader = csv.DictReader(f)
            self.scripts = list(reader)
        print(f"✅ Loaded {len(self.scripts)} files needing rename")
    
    def read_file_deeply(self, filename):
        """Read file and extract purpose from code"""
        try:
            filepath = self.pythons_dir / filename
            if not filepath.exists():
                return None
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract imports to understand what it does
            imports = []
            for line in content.split('\n')[:50]:
                if line.strip().startswith(('import ', 'from ')):
                    imports.append(line.strip())
            
            # Look for main function or class names
            try:
                tree = ast.parse(content)
                classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)][:10]
            except:
                classes = []
                functions = []
            
            # Look for key patterns in code
            patterns = {
                'tts': 'text-to-speech' in content.lower() or 'tts' in content.lower(),
                'download': 'download' in content.lower(),
                'upload': 'upload' in content.lower(),
                'scrape': 'scrap' in content.lower() or 'crawl' in content.lower(),
                'analyze': 'analyz' in content.lower(),
                'generate': 'generat' in content.lower(),
                'convert': 'convert' in content.lower(),
                'organize': 'organiz' in content.lower() or 'sort' in content.lower(),
            }
            
            return {
                'imports': imports,
                'classes': classes,
                'functions': functions,
                'patterns': [k for k, v in patterns.items() if v],
                'content_sample': content[:500]
            }
            
        except:
            return None
    
    def suggest_for_all_caps(self, script):
        """Handle ALL_CAPS filenames intelligently"""
        current = script['current_name']
        desc = script['description']
        
        # Extract the meaningful part
        base = current.replace('.py', '')
        
        # Common ALL_CAPS patterns and their better names
        all_caps_mapping = {
            'AI_ORCHESTRATOR_ULTIMATE': 'multi-llm-orchestrator',
            'AI_SETUP_VERIFICATION': 'check-ai-sdks',
            'ADVANCED_SYSTEMS_CATALOG': 'project-catalog-generator',
            'DEEP_CONTENT_ANALYZER_ULTIMATE': 'deep-content-analyzer',
            'COMPLETE_MEDIA_PROMPT_ANALYZER': 'media-prompt-analyzer',
            'INTELLIGENT_WORKFLOW_BUILDER': 'workflow-builder',
            'PROMPT_HUNTER_ULTIMATE': 'prompt-hunter',
            'PROMPT_CSV_ANALYZER_ULTIMATE': 'csv-prompt-analyzer',
            'UNIFIED_CONTENT_ORCHESTRATOR': 'content-orchestrator',
            'PROCESS_BATCH_RENAMES': 'batch-rename-processor',
        }
        
        if base in all_caps_mapping:
            return all_caps_mapping[base] + '.py', "Converted ALL_CAPS to meaningful lowercase"
        
        # Generic conversion: remove ULTIMATE, convert to lowercase with hyphens
        better_name = base.replace('_ULTIMATE', '').replace('_FINAL', '').replace('_MASTER', '')
        better_name = better_name.replace('_', '-').lower()
        
        # Add context from description
        if 'orchestrat' in desc.lower():
            if 'llm' in desc.lower() or 'multi' in desc.lower():
                better_name = 'multi-llm-orchestrator'
            elif 'content' in desc.lower():
                better_name = 'content-orchestrator'
        elif 'catalog' in desc.lower():
            if 'project' in desc.lower():
                better_name = 'project-catalog-generator'
            elif 'system' in desc.lower():
                better_name = 'systems-catalog-generator'
        elif 'analyzer' in desc.lower():
            if 'content' in desc.lower():
                better_name = 'content-analyzer'
            elif 'media' in desc.lower():
                better_name = 'media-analyzer'
            elif 'prompt' in desc.lower():
                better_name = 'prompt-analyzer'
        
        return better_name + '.py', f"Converted from ALL_CAPS: {base}"
    
    def suggest_for_analyze_prefix(self, script):
        """Handle generic analyze- prefix files"""
        current = script['current_name']
        desc = script['description'].lower()
        
        # Read the file to understand what it does
        code_info = self.read_file_deeply(current)
        
        base = current.replace('analyze-', '').replace('.py', '')
        
        # Specific mappings based on actual functionality
        if 'metadata' in current:
            if 'image prompt' in desc or 'transcript' in desc:
                return 'transcript-to-image-prompts.py', "Generates image prompts from transcripts"
            elif 'image' in desc or 'photo' in desc:
                return 'extract-image-metadata.py', "Extracts metadata from images"
        
        elif 'prompt' in current:
            if code_info and 'gpt' in str(code_info['imports']).lower():
                if 'csv' in desc or 'enrich' in desc:
                    return 'gpt-vision-csv-enricher.py', "Enriches CSV with GPT Vision"
                else:
                    return 'gpt-vision-prompt-generator.py', "Generates prompts with GPT Vision"
        
        elif 'reader' in current:
            if code_info and 'image' in str(code_info).lower():
                return 'gpt-vision-image-analyzer.py', "Analyzes images with GPT Vision"
            else:
                return f'read-{base}.py', f"Reads {base} data"
        
        elif 'writer' in current:
            if 'json' in current and 'image' in desc:
                return 'image-metadata-helpers.py', "Helper utilities for image metadata"
            else:
                return f'write-{base}.py', f"Writes {base} data"
        
        elif 'code' in current:
            if 'complexity' in current:
                return 'python-complexity-analyzer.py', "Analyzes Python code complexity"
            elif 'quality' in desc:
                return 'code-quality-analyzer.py', "Checks code quality"
        
        elif 'file' in current:
            if 'migration' in current:
                return 'migration-planner.py', "Plans file migrations"
            elif 'version' in current:
                return 'find-script-versions.py', "Finds versioned scripts"
            elif 'comprehensive' in current:
                return 'master-file-analyzer.py', "Master file analysis orchestrator"
        
        # Default: convert analyze-X to X-analyzer
        return f'{base}-analyzer.py', "Converted from generic analyze- prefix"
    
    def suggest_for_missing_docs(self, script):
        """Handle files with no documentation"""
        current = script['current_name']
        
        # Read file to understand it
        code_info = self.read_file_deeply(current)
        
        if not code_info:
            return current, "REVIEW", "Could not read file - manual review needed"
        
        # Analyze imports to guess purpose
        imports_str = ' '.join(code_info['imports']).lower()
        functions_str = ' '.join(code_info['functions']).lower()
        
        # Instagram patterns
        if 'instagram' in current or 'instabot' in imports_str:
            if 'whisper' in current:
                return 'instagram-whisper-captions.py', "Adds captions using Whisper"
            elif 'combiner' in current:
                return 'instagram-content-combiner.py', "Combines Instagram content"
            elif 'processor' in current:
                return 'instagram-media-processor.py', "Processes Instagram media"
            elif 'library' in current:
                return 'instagram-bot-library.py', "KEEP", "Library file - keep as-is"
        
        # Audio/TTS
        if 'polly' in current or 'tts' in imports_str:
            return 'aws-polly-tts.py', "KEEP", "Already clear - AWS Polly TTS"
        
        if 'audio' in current and 'extract' in current:
            if 'news' in current:
                return 'news-to-audio.py', "Converts news articles to audio"
            else:
                return 'extract-audio.py', "Extracts audio from media"
        
        # Video
        if 'video' in current:
            if 'thumbnail' in functions_str or 'thumb' in current:
                return 'video-thumbnail-generator.py', "Generates video thumbnails"
            elif 'clip' in current or 'editor' in current:
                return 'video-clip-editor.py', "KEEP", "Name is clear"
            elif 'compress' in current:
                return 'video-compressor.py', "KEEP", "Name is clear"
        
        # Scrapers
        if 'scrap' in current or 'crawl' in current:
            if 'news' in current:
                return 'news-scraper.py', "Scrapes news articles"
            elif 'pexels' in current:
                return 'pexels-video-downloader.py', "KEEP", "Name is clear"
            else:
                return 'web-scraper.py', "Generic web scraper"
        
        # CSV/Data processing  
        if 'csv' in current:
            if 'doc' in current:
                return 'csv-to-docs.py', "Converts CSV to documentation"
            elif 'catalog' in current:
                return 'generate-csv-catalog.py', "Generates CSV catalog"
        
        # Documents
        if 'retrieve' in current and 'docs' in current:
            return 'download-documents.py', "Downloads/retrieves documents"
        
        # Conversions
        if 'convert' in current and 'conversation' in current:
            return 'conversations-to-csv.py', "Exports conversations to CSV"
        
        # Generic single words
        single_word_map = {
            'brand.py': 'load-brand-data.py',
            'crawl.py': 'web-crawler.py',
            'scraper.py': 'video-downloader.py',
            'categorizer.py': 'file-categorizer.py',
            'vision.py': 'gpt-vision-describer.py',
            'cover.py': 'dalle-cover-generator.py',
        }
        
        if current in single_word_map:
            return single_word_map[current], f"Descriptive name for {current}"
        
        return current, "REVIEW", "Needs manual review - unclear purpose"
    
    def analyze_and_suggest(self):
        """Analyze all scripts and provide intelligent suggestions"""
        print("\n🧠 Intelligently analyzing all 398 files...")
        print("="*80)
        
        for i, script in enumerate(self.scripts, 1):
            if i % 50 == 0:
                print(f"   Progress: {i}/{len(self.scripts)}")
            
            current = script['current_name']
            reason = script.get('bad_name_reason', '')
            
            suggested_name = current
            suggestion_reason = ""
            action = "RENAME"
            
            # Route to appropriate handler
            if 'ALL_CAPS' in reason or current.isupper() or '_' in current and current.replace('_', '').replace('.py', '').isupper():
                suggested_name, suggestion_reason = self.suggest_for_all_caps(script)
            
            elif 'analyze-' in reason or current.startswith('analyze-'):
                result = self.suggest_for_analyze_prefix(script)
                if len(result) == 2:
                    suggested_name, suggestion_reason = result
                else:
                    suggested_name, action, suggestion_reason = result
            
            elif 'Missing documentation' in reason:
                result = self.suggest_for_missing_docs(script)
                if len(result) == 2:
                    suggested_name, suggestion_reason = result
                else:
                    suggested_name, action, suggestion_reason = result
            
            else:
                # Other issues
                suggested_name = current
                action = "REVIEW"
                suggestion_reason = reason
            
            self.smart_suggestions.append({
                'current_name': current,
                'suggested_name': suggested_name,
                'action': action,
                'category': script['category'],
                'description': script['description'],
                'original_issue': reason,
                'suggestion_reason': suggestion_reason,
                'apis_used': script.get('apis_used', ''),
                'lines': script.get('lines', ''),
                'size_kb': script.get('size_kb', '')
            })
        
        print("✅ Generated suggestions for all files\n")
    
    def print_suggestions_by_category(self, limit_per_cat=15):
        """Print suggestions organized by category"""
        
        by_category = {}
        for item in self.smart_suggestions:
            cat = item['category']
            by_category.setdefault(cat, []).append(item)
        
        # Sort by number of files
        sorted_cats = sorted(by_category.items(), key=lambda x: len(x[1]), reverse=True)
        
        for category, scripts in sorted_cats[:8]:  # Top 8 categories
            print(f"\n{'='*80}")
            print(f"📂 {category.upper()} ({len(scripts)} files)")
            print('='*80)
            
            # Show only files that are being renamed (not KEEP or REVIEW)
            renames = [s for s in scripts if s['action'] == 'RENAME' and s['current_name'] != s['suggested_name']]
            keeps = [s for s in scripts if s['action'] == 'KEEP']
            reviews = [s for s in scripts if s['action'] == 'REVIEW']
            
            if renames:
                print(f"\n🏷️ RENAME ({len(renames)} files):\n")
                for i, script in enumerate(sorted(renames, key=lambda x: x['current_name'])[:limit_per_cat], 1):
                    print(f"{i}. {script['current_name']}")
                    print(f"   → {script['suggested_name']}")
                    print(f"   Why: {script['suggestion_reason']}")
                    if script['description'] != 'No description found':
                        print(f"   Does: {script['description'][:80]}")
                    if script['apis_used']:
                        print(f"   APIs: {script['apis_used']}")
                    print()
                
                if len(renames) > limit_per_cat:
                    print(f"   ... and {len(renames) - limit_per_cat} more\n")
            
            if keeps:
                print(f"✅ KEEP ({len(keeps)} files already have good names)")
            
            if reviews:
                print(f"📝 NEEDS MANUAL REVIEW ({len(reviews)} files)")
    
    def save_suggestions_csv(self):
        """Save smart suggestions to CSV"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = self.pythons_dir / f'_smart_rename_suggestions_{timestamp}.csv'
        
        fieldnames = [
            'current_name',
            'suggested_name',
            'action',
            'category',
            'description',
            'original_issue',
            'suggestion_reason',
            'apis_used',
            'lines',
            'size_kb'
        ]
        
        # Sort by action (RENAME first), then category
        def sort_key(x):
            action_priority = {'RENAME': 0, 'DELETE': 1, 'KEEP': 2, 'REVIEW': 3}
            return (action_priority.get(x['action'], 4), x['category'], x['current_name'])
        
        sorted_suggestions = sorted(self.smart_suggestions, key=sort_key)
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_suggestions)
        
        return output_path
    
    def generate_summary(self):
        """Generate summary statistics"""
        by_action = {}
        by_category = {}
        
        for item in self.smart_suggestions:
            action = item['action']
            by_action[action] = by_action.get(action, 0) + 1
            
            cat = item['category']
            by_category[cat] = by_category.get(cat, 0) + 1
        
        print("\n" + "="*80)
        print("📊 INTELLIGENT RENAME SUMMARY")
        print("="*80)
        
        print("\n🎯 By Action:")
        for action in ['RENAME', 'KEEP', 'REVIEW', 'DELETE']:
            count = by_action.get(action, 0)
            emoji = {'RENAME': '🏷️', 'KEEP': '✅', 'REVIEW': '📝', 'DELETE': '🗑️'}.get(action, '📌')
            print(f"   {emoji} {action:10} {count:3} files")
        
        print("\n📂 Top Categories Needing Attention:")
        for cat, count in sorted(by_category.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {cat:30} {count:3} files")
        
        # Calculate renames that are different
        actual_renames = [s for s in self.smart_suggestions 
                         if s['action'] == 'RENAME' and s['current_name'] != s['suggested_name']]
        
        print("\n✨ Actual Changes:")
        print(f"   {len(actual_renames)} files will get new names")
        print(f"   {by_action.get('DELETE', 0)} files will be deleted")
        print(f"   {by_action.get('KEEP', 0)} files already perfect")


def main():
    needs_csv = Path.home() / 'pythons' / '_needs_renaming_20251106_133157.csv'
    
    analyzer = IntelligentRenameAnalyzer(needs_csv)
    analyzer.load_csv()
    analyzer.analyze_and_suggest()
    analyzer.print_suggestions_by_category()
    
    output_csv = analyzer.save_suggestions_csv()
    analyzer.generate_summary()
    
    print(f"\n{'='*80}")
    print("💾 Smart suggestions saved to:")
    print(f"   {output_csv}")
    print("\n💡 Review the suggestions and update as needed!")
    print("   Then run the batch rename script to execute")


if __name__ == '__main__':
    main()
