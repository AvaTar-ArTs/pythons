#!/usr/bin/env python3
"""
Comprehensive Rename & Cleaner
Re-analyzes all files, identifies third-party code, and provides accurate renames
"""

import csv
import re
import ast
from pathlib import Path
from datetime import datetime

class ComprehensiveRenameCleaner:
    """Smart analysis with third-party detection and accurate renames"""
    
    def __init__(self, pythons_dir):
        self.pythons_dir = Path(pythons_dir)
        self.results = []
        
        # Known third-party/library code patterns
        self.third_party_indicators = [
            'from .compat import',
            'from .resources import',
            'from .util import',
            'from .types import',
            '# Copyright (c)',
            'IPython Development Team',
            'Snoop Project',
            'distlib',
            'instabot example',  # Example files
            'sys.path.append(os.path.join(sys.path[0], "../"))',  # Library examples
        ]
        
    def is_third_party_code(self, filepath):
        """Detect if file is third-party/library code"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                first_100_lines = ''.join(f.readlines()[:100])
            
            # Check for third-party indicators
            for indicator in self.third_party_indicators:
                if indicator in first_100_lines:
                    return True, indicator
            
            # Check if it's an example file
            if 'example' in first_100_lines.lower() and len(first_100_lines) < 2000:
                return True, "Example file"
            
            return False, ""
            
        except:
            return False, ""
    
    def read_and_understand(self, filepath):
        """Read file and understand what it does"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract docstring
            docstring = ""
            try:
                tree = ast.parse(content)
                docstring = ast.get_docstring(tree) or ""
            except:
                # Fallback: look for """
                match = re.search(r'"""(.+?)"""', content, re.DOTALL)
                if match:
                    docstring = match.group(1).strip()
            
            # Get first meaningful line if no docstring
            if not docstring or len(docstring) < 10:
                for line in content.split('\n')[:30]:
                    if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('import'):
                        if 'def ' in line or 'class ' in line:
                            docstring = line.strip()
                            break
            
            # Analyze what it does from code
            purpose = self.infer_purpose_from_code(content, filepath.name)
            
            return {
                'docstring': docstring[:200],
                'purpose': purpose,
                'content_sample': content[:1000]
            }
            
        except:
            return {'docstring': '', 'purpose': 'Unknown', 'content_sample': ''}
    
    def infer_purpose_from_code(self, content, filename):
        """Infer purpose from code patterns"""
        content_lower = content.lower()
        
        # Specific patterns
        patterns = {
            'shuffle-csv-rows.py': ('shuffle_csv' in content and 'random.shuffle' in content),
            'gpt-script-categorizer.py': ('get_openai_category' in content and 'script_content' in content),
            'spotify-track-model.py': ('spotify_data' in content and 'class Track' in content),
            'backup-documents-csv.py': ('~/documents' in content_lower and 'csv' in content_lower and 'backup' in content_lower),
            'reddit-comment-formatter.py': ('reddit' in content_lower and 'html' in content_lower and 'comment' in content_lower),
            'instagram-bot-core.py': (filename == 'instagram.py' and len(content) < 3000),
            'shuffle-csv-from-url.py': ('requests.get(url)' in content and 'shuffle' in content and 'csv' in content),
            'telegram-file-downloader.py': ('telegram' in content_lower and 'download' in content_lower),
            'snoop-osint-tool.py': ('snoop' in content_lower and 'osint' in content_lower),
            'xml-assembly-manifest.py': ('<?xml' in content and 'assembly' in content),
        }
        
        for purpose_name, condition in patterns.items():
            if condition:
                return purpose_name
        
        return 'Unknown'
    
    def suggest_accurate_name(self, filepath, info, current_name):
        """Suggest accurate name based on deep understanding"""
        
        # Use inferred purpose if available
        if info['purpose'] != 'Unknown' and info['purpose'].endswith('.py'):
            return info['purpose'], f"Analyzed from code functionality"
        
        # Specific file mappings based on actual content
        specific_renames = {
            'sufflecsv.py': ('shuffle-csv-from-url.py', 'Downloads CSV from URL and shuffles rows'),
            'categorizer.py': ('gpt-script-categorizer.py', 'Categorizes scripts using GPT-3.5'),
            'documents.py': ('backup-documents-to-csv.py', 'Backs up ~/documents to CSV'),
            'reddit.py': ('reddit-to-html-formatter.py', 'Formats Reddit comments to HTML'),
            'instagram.py': ('instagram-bot-module.py', 'Generic Instagram bot module'),
            'askredditbot.py': ('askreddit-auto-poster.py', 'Posts to r/AskReddit'),
            'compile.py': ('compile-image-info-csv.py', 'Compiles image info to master CSV'),
            'converts.py': ('batch-convert-upscale-images.py', 'Converts and upscales images in batch'),
            'convertupscale.py': ('convert-upscale-images.py', 'Single convert + upscale operation'),
            'createimages.py': ('dalle-batch-generator.py', 'Batch generates images with DALL-E'),
            'csvsort.py': ('csv-download-sort-images.py', 'Downloads images from CSV and sorts'),
            'denoiser.py': ('ffdnet-image-denoiser.py', 'Denoises images using FFDNet'),
            'lexica.py': ('lexica-art-downloader.py', 'Downloads images from Lexica.art'),
            'mydesigner.py': ('batch-process-images.py', 'Batch processes and downloads images'),
            'nativetypes.py': ('jinja2-native-types.py', 'Jinja2 native type converter'),
            'organizer.py': ('sort-images-by-format.py', 'Sorts images by file format'),
            'parse.py': ('parse-onedrive-urls.py', 'Parses OneDrive photo URLs'),
            'setuptools.py': ('python-setuptools-bootstrap.py', 'Setuptools bootstrap script'),
            'upscalecreateimages.py': ('dalle-generate-upscale.py', 'Generates with DALL-E and upscales'),
            'cover.py': ('dalle-typography-generator.py', 'Creates typography covers with DALL-E'),
            'vision.py': ('gpt-vision-describer.py', 'Describes images with GPT-4 Vision'),
            'textgenerator.py': ('gpt-text-generator.py', 'Generates text with GPT'),
            'smart.py': ('generate-organization-plan.py', 'Generates smart organization plan'),
            'sorts.py': ('sort-images-exclude-patterns.py', 'Sorts images with exclusion patterns'),
            'rename.py': ('batch-rename-images.py', 'Batch renames image files'),
            'renamer.py': ('intelligent-script-renamer.py', 'Renames Python scripts intelligently'),
            'scrape.py': ('reddit-scraper-cleaner.py', 'Scrapes Reddit and cleans text'),
            'organize.py': ('ai-outputs-organizer.py', 'Organizes AI output files'),
            'implement.py': ('execute-organization-plan.py', 'Executes smart organization system'),
            'pyorganize.py': ('extract-functions-classes.py', 'Extracts top-level functions/classes'),
            'pytables.py': ('test-pytables-pandas.py', 'Tests Pandas HDF5 tables'),
        }
        
        if current_name in specific_renames:
            return specific_renames[current_name]
        
        # Snake_case to kebab-case
        if '_' in current_name and not current_name.startswith('_'):
            kebab = current_name.replace('_', '-')
            return kebab, "Converted snake_case to kebab-case"
        
        # ALL_CAPS to lowercase
        if current_name.isupper() or (current_name.replace('_', '').replace('.py', '').isupper()):
            lowercase = current_name.lower().replace('_', '-')
            return lowercase, "Converted ALL_CAPS to lowercase"
        
        return current_name, "Needs manual review"
    
    def analyze_all_files(self):
        """Comprehensively analyze all Python files"""
        print("🔍 Comprehensive Analysis of ~/pythons")
        print("="*80)
        
        py_files = sorted([f for f in self.pythons_dir.glob('*.py') if f.is_file()])
        
        print(f"📊 Found {len(py_files)} Python files")
        print("🧹 Identifying third-party code...")
        print("🏷️ Suggesting accurate renames...\n")
        
        for i, filepath in enumerate(py_files, 1):
            if i % 50 == 0:
                print(f"   Progress: {i}/{len(py_files)}")
            
            current_name = filepath.name
            
            # Check if third-party
            is_third_party, indicator = self.is_third_party_code(filepath)
            
            if is_third_party:
                self.results.append({
                    'current_name': current_name,
                    'suggested_name': '',
                    'action': 'DELETE',
                    'reason': f'Third-party code: {indicator}',
                    'category': 'Cleanup',
                    'description': indicator,
                    'lines': self.count_lines(filepath),
                    'size_kb': round(filepath.stat().st_size / 1024, 2)
                })
                continue
            
            # Read and understand
            info = self.read_and_understand(filepath)
            
            # Get accurate rename suggestion
            suggested_name, reason = self.suggest_accurate_name(filepath, info, current_name)
            
            # Determine action
            if suggested_name == current_name:
                if 'manual review' in reason.lower():
                    action = 'REVIEW'
                else:
                    action = 'KEEP'
            else:
                action = 'RENAME'
            
            # Categorize
            category = self.smart_categorize(current_name, info, filepath)
            
            self.results.append({
                'current_name': current_name,
                'suggested_name': suggested_name,
                'action': action,
                'reason': reason,
                'category': category,
                'description': info['docstring'] or 'No description',
                'lines': self.count_lines(filepath),
                'size_kb': round(filepath.stat().st_size / 1024, 2)
            })
        
        print(f"\n✅ Analysis complete!")
    
    def smart_categorize(self, filename, info, filepath):
        """Smart categorization"""
        name_lower = filename.lower()
        desc_lower = info['docstring'].lower() + info['purpose'].lower()
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(2000).lower()
        except:
            content = ""
        
        if 'instagram' in name_lower or 'instagram' in content:
            return 'Social Media - Instagram'
        elif 'youtube' in name_lower or 'youtube' in content:
            return 'Social Media - YouTube'
        elif 'reddit' in name_lower or 'reddit' in content:
            return 'Social Media - Reddit'
        elif 'gpt' in content or 'vision' in content or 'image' in name_lower:
            if 'vision' in content or 'image' in desc_lower:
                return 'Image Analysis'
            return 'AI Tools'
        elif 'audio' in name_lower or 'tts' in name_lower or 'mp3' in content:
            return 'Audio Tools'
        elif 'video' in name_lower or 'mp4' in content:
            return 'Video Tools'
        elif 'csv' in name_lower or 'csv' in desc_lower:
            return 'Data Processing'
        elif 'organize' in name_lower or 'rename' in name_lower or 'sort' in name_lower:
            return 'File Organization'
        elif 'code' in desc_lower or 'ast' in content or 'complexity' in name_lower:
            return 'Code Analysis'
        
        return 'Utilities'
    
    def count_lines(self, filepath):
        """Count lines"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return len(f.readlines())
        except:
            return 0
    
    def save_clean_csv(self):
        """Save clean, organized CSV"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = self.pythons_dir / f'RENAME_PLAN_{timestamp}.csv'
        
        fieldnames = [
            'action',
            'current_name',
            'suggested_name',
            'reason',
            'category',
            'description',
            'lines',
            'size_kb'
        ]
        
        # Sort by action priority, then category
        def sort_key(x):
            priority = {'DELETE': 0, 'RENAME': 1, 'KEEP': 2, 'REVIEW': 3}
            return (priority.get(x['action'], 4), x['category'], x['current_name'])
        
        sorted_results = sorted(self.results, key=sort_key)
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_results)
        
        return output_path
    
    def print_summary(self):
        """Print comprehensive summary"""
        by_action = {}
        by_category = {}
        
        for item in self.results:
            action = item['action']
            by_action[action] = by_action.get(action, 0) + 1
            
            cat = item['category']
            by_category[cat] = by_category.get(cat, 0) + 1
        
        print("\n" + "="*80)
        print("📊 COMPREHENSIVE RENAME & CLEANUP SUMMARY")
        print("="*80)
        
        print(f"\n🎯 By Action:")
        for action in ['DELETE', 'RENAME', 'KEEP', 'REVIEW']:
            count = by_action.get(action, 0)
            emoji = {'DELETE': '🗑️', 'RENAME': '🏷️', 'KEEP': '✅', 'REVIEW': '📝'}[action]
            print(f"   {emoji} {action:10} {count:4} files")
        
        print(f"\n📂 By Category:")
        for cat, count in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
            print(f"   {cat:35} {count:4} files")
        
        # Show deletions
        deletions = [r for r in self.results if r['action'] == 'DELETE']
        if deletions:
            print(f"\n🗑️ Files to DELETE ({len(deletions)}):")
            for item in deletions[:10]:
                print(f"   • {item['current_name']:40} - {item['reason']}")
            if len(deletions) > 10:
                print(f"   ... and {len(deletions) - 10} more")
        
        # Show key renames
        renames = [r for r in self.results if r['action'] == 'RENAME']
        if renames:
            print(f"\n🏷️ Sample Renames ({len(renames)} total):")
            for item in renames[:15]:
                if item['current_name'] != item['suggested_name']:
                    print(f"   {item['current_name']}")
                    print(f"   → {item['suggested_name']}")
                    print(f"      {item['reason']}\n")


def main():
    pythons_dir = Path.home() / 'pythons'
    
    cleaner = ComprehensiveRenameCleaner(pythons_dir)
    
    print("🚀 Starting comprehensive re-analysis...")
    cleaner.analyze_all_files()
    
    output_csv = cleaner.save_clean_csv()
    cleaner.print_summary()
    
    print(f"\n{'='*80}")
    print(f"💾 Clean rename plan saved to:")
    print(f"   {output_csv}")
    print(f"\n✨ This CSV is:")
    print(f"   • Sorted by action (DELETE first, then RENAME)")
    print(f"   • Categorized properly")
    print(f"   • Has accurate rename suggestions")
    print(f"   • Identifies third-party code to remove")


if __name__ == '__main__':
    main()
