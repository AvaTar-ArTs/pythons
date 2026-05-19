#!/usr/bin/env python3
"""
Truly Intelligent Renamer
Actually reads code and understands what it does to suggest perfect names
"""

import os
# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)
from pathlib import Path as PathLib

def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")

load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass

import csv
import re
from pathlib import Path
from datetime import datetime

class TrulyIntelligentRenamer:
    """Actually intelligent - reads code and understands purpose"""
    
    def __init__(self, needs_csv):
        self.csv_path = Path(needs_csv)
        self.pythons_dir = Path.home() / 'pythons'
        self.scripts = []
        self.final_suggestions = []
        
    def load_csv(self):
        """Load needs_renaming CSV"""
        with open(self.csv_path, 'r') as f:
            reader = csv.DictReader(f)
            self.scripts = list(reader)
        print(f"✅ Loaded {len(self.scripts)} files")
    
    def deep_code_analysis(self, filename):
        """Deeply analyze code to understand what it does"""
        try:
            filepath = self.pythons_dir / filename
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            analysis = {
                'main_action': None,
                'target': None,
                'technology': None,
                'input_type': None,
                'output_type': None
            }
            
            # Parse imports
            imports = []
            for line in content.split('\n')[:100]:
                if re.match(r'^\s*(import|from)\s+', line):
                    imports.append(line.strip())
            
            imports_str = ' '.join(imports).lower()
            content_lower = content.lower()
            
            # Detect main action
            if 'def download' in content_lower or 'download(' in content_lower:
                analysis['main_action'] = 'download'
            elif 'def upload' in content_lower or '.upload(' in content_lower:
                analysis['main_action'] = 'upload'
            elif 'def generate' in content_lower or 'generat' in content_lower:
                analysis['main_action'] = 'generate'
            elif 'def convert' in content_lower or 'convert' in content_lower:
                analysis['main_action'] = 'convert'
            elif 'def analyze' in content_lower or 'analyz' in content_lower:
                analysis['main_action'] = 'analyze'
            elif 'def organize' in content_lower or 'organiz' in content_lower:
                analysis['main_action'] = 'organize'
            elif 'def scrape' in content_lower or 'scrap' in content_lower:
                analysis['main_action'] = 'scrape'
            elif 'def sort' in content_lower or 'sorting' in content_lower:
                analysis['main_action'] = 'sort'
            elif 'def shuffle' in content_lower or 'shuffle' in content_lower:
                analysis['main_action'] = 'shuffle'
            elif 'def track' in content_lower or 'tracking' in content_lower:
                analysis['main_action'] = 'track'
            elif 'def check' in content_lower or 'verify' in content_lower:
                analysis['main_action'] = 'check'
            
            # Detect target/subject
            if 'instagram' in imports_str or 'instabot' in imports_str:
                analysis['target'] = 'instagram'
            elif 'reddit' in imports_str or 'praw' in imports_str:
                analysis['target'] = 'reddit'
            elif 'youtube' in imports_str or 'pytube' in imports_str:
                analysis['target'] = 'youtube'
            elif 'spotify' in imports_str or 'spotipy' in imports_str:
                analysis['target'] = 'spotify'
            
            # Detect technology
            if 'openai' in imports_str:
                if 'vision' in content_lower or 'gpt-4v' in content_lower:
                    analysis['technology'] = 'gpt-vision'
                elif 'tts' in content_lower or 'text_to_speech' in content_lower:
                    analysis['technology'] = 'openai-tts'
                elif 'whisper' in imports_str:
                    analysis['technology'] = 'whisper'
                else:
                    analysis['technology'] = 'gpt'
            elif 'anthropic' in imports_str:
                analysis['technology'] = 'claude'
            elif 'gemini' in imports_str or 'generativeai' in imports_str:
                analysis['technology'] = 'gemini'
            elif 'groq' in imports_str:
                analysis['technology'] = 'groq'
            elif 'elevenlabs' in imports_str:
                analysis['technology'] = 'elevenlabs'
            elif 'whisper' in imports_str:
                analysis['technology'] = 'whisper'
            elif 'pil' in imports_str or 'image' in imports_str:
                analysis['technology'] = 'pil'
            
            # Detect input/output types
            if 'csv' in content_lower:
                if '.read_csv' in content or 'csv.reader' in content:
                    analysis['input_type'] = 'csv'
                if '.to_csv' in content or 'csv.writer' in content:
                    analysis['output_type'] = 'csv'
            
            if 'json.load' in content or 'json.loads' in content:
                analysis['input_type'] = 'json'
            if 'json.dump' in content or 'json.dumps' in content:
                analysis['output_type'] = 'json'
            
            if re.search(r'\.(mp3|wav|m4a|flac)', content_lower):
                if 'AudioSegment.from' in content:
                    analysis['input_type'] = 'audio'
                if '.export(' in content and 'audio' in content_lower:
                    analysis['output_type'] = 'audio'
            
            if re.search(r'\.(jpg|jpeg|png|gif|webp)', content_lower):
                if 'Image.open' in content:
                    analysis['input_type'] = 'image'
                if 'image.save' in content or '.save(' in content:
                    analysis['output_type'] = 'image'
            
            return analysis
            
        except Exception:
            return None
    
    def build_name_from_analysis(self, analysis, current_name, desc):
        """Build intelligent name from code analysis"""
        parts = []
        
        # Add target platform if specific
        if analysis['target']:
            parts.append(analysis['target'])
        
        # Add main action
        if analysis['main_action']:
            parts.append(analysis['main_action'])
        elif 'orchestrat' in desc.lower():
            parts.append('orchestrator')
        elif 'builder' in desc.lower():
            parts.append('builder')
        elif 'hunter' in desc.lower():
            parts.append('hunter')
        
        # Add input-output if conversion
        if analysis['main_action'] == 'convert':
            if analysis['input_type'] and analysis['output_type']:
                return f"{analysis['input_type']}-to-{analysis['output_type']}.py"
        
        # Add subject/technology
        if analysis['technology']:
            # Special handling for specific tech
            if analysis['technology'] == 'gpt-vision':
                if analysis['main_action'] == 'analyze' and 'image' in desc.lower():
                    return 'gpt-vision-image-analyzer.py'
                elif 'csv' in desc.lower():
                    return 'gpt-vision-csv-enricher.py'
            elif analysis['technology'] in ['whisper', 'openai-tts', 'elevenlabs']:
                if analysis['target']:
                    parts.append(analysis['technology'])
                else:
                    # Put technology first for standalone tools
                    parts = [analysis['technology']] + parts
        
        # Add object if we know it
        if 'image' in desc.lower() and 'image' not in parts:
            parts.append('images')
        elif 'audio' in desc.lower() and 'audio' not in parts:
            parts.append('audio')
        elif 'video' in desc.lower() and 'video' not in parts:
            parts.append('video')
        elif 'file' in desc.lower() and len(parts) < 2:
            parts.append('files')
        
        if parts:
            return '-'.join(parts) + '.py'
        
        return None
    
    def suggest_intelligent_rename(self, script):
        """Provide truly intelligent suggestion"""
        current = script['current_name']
        desc = script['description']
        category = script['category']
        
        # Skip already good names
        good_name_patterns = [
            'instagram-follow-user-followers',
            'instagram-delete-posts',
            'instagram-collect-stats',
            'convert-aiff-to-mp3',
            'aws-polly-tts',
            'youtube-auto-uploader',
        ]
        
        for pattern in good_name_patterns:
            if pattern in current:
                return current, "KEEP", "Already has descriptive name"
        
        # Deep code analysis
        analysis = self.deep_code_analysis(current)
        
        if not analysis:
            return current, "REVIEW", "Could not analyze - needs manual review"
        
        # Build intelligent name
        suggested = self.build_name_from_analysis(analysis, current, desc)
        
        # Specific fixes for known files
        specific_fixes = {
            'scripts.py': ('xml-assembly-manifest.py', 'XML assembly manifest file'),
            'snoopplugins.py': ('snoop-plugins.py', 'Snoop Project plugins'),
            'sufflecsv.py': ('shuffle-csv-rows.py', 'Shuffles CSV rows'),
            'track.py': ('spotify-track-handler.py', 'Handles Spotify track data'),
            'categorizer.py': ('gpt-file-categorizer.py', 'Categorizes files using GPT'),
            'documents.py': ('backup-documents-csv.py', 'Backs up documents to CSV'),
            'implement.py': ('smart-file-organizer.py', 'Smart file organization system'),
            'organize.py': ('ai-output-organizer.py', 'Organizes AI outputs'),
            'rename.py': ('image-batch-renamer.py', 'Batch renames images'),
            'renamer.py': ('python-script-renamer.py', 'Renames Python scripts'),
            'scrape.py': ('reddit-content-scraper.py', 'Scrapes Reddit content'),
            'smart.py': ('smart-organization-planner.py', 'Plans smart organization'),
            'sorts.py': ('image-file-sorter.py', 'Sorts image files'),
            'textgenerator.py': ('gpt-text-generator.py', 'Generates text with GPT'),
            'translation.py': ('telegram-downloader-bot.py', 'Telegram file downloader bot'),
            'reddit.py': ('reddit-comment-formatter.py', 'Formats Reddit comments to HTML'),
            'askredditbot.py': ('reddit-auto-poster.py', 'Posts to Reddit automatically'),
            'instagram.py': ('instagram-bot-core.py', 'Core Instagram bot module'),
            'compile.py': ('compile-image-catalog-csv.py', 'Compiles image catalog to CSV'),
            'converts.py': ('convert-upscale-images.py', 'Converts and upscales images'),
            'convertupscale.py': ('image-format-upscaler.py', 'Converts format and upscales'),
            'createimages.py': ('dalle-image-generator.py', 'Generates images with DALL-E'),
            'csvsort.py': ('download-sort-images-csv.py', 'Downloads and sorts images from CSV'),
            'denoiser.py': ('ffdnet-image-denoiser.py', 'Denoises images with FFDNet'),
            'lexica.py': ('lexica-image-downloader.py', 'Downloads images from Lexica.art'),
            'mydesigner.py': ('image-processor-pipeline.py', 'Processes images pipeline'),
            'nativetypes.py': ('jinja-native-types.py', 'Jinja2 native type handling'),
            'organizer.py': ('sort-images-by-type.py', 'Sorts images by file type'),
            'parse.py': ('onedrive-photo-parser.py', 'Parses OneDrive photo URLs'),
            'setuptools.py': ('setuptools-bootstrap.py', 'Setuptools bootstrap script'),
            'upscalecreateimages.py': ('generate-upscale-images.py', 'Generates and upscales images'),
            'cover.py': ('dalle-typography-cover.py', 'Generates typography covers with DALL-E'),
            'vision.py': ('gpt-vision-image-describer.py', 'Describes images with GPT Vision'),
        }
        
        if current in specific_fixes:
            suggested, reason = specific_fixes[current]
            return suggested, "RENAME", reason
        
        # Use analyzed suggestion if good
        if suggested and suggested != current:
            return suggested, "RENAME", f"Analyzed from code: {analysis['main_action']} {analysis['target'] or ''}"
        
        # Default for single-word generic names
        if current in ['scripts.py', 'tools.py', 'main.py', 'run.py', 'test.py']:
            return current, "REVIEW", "Generic single-word name - read file to rename properly"
        
        return current, "REVIEW", "Needs manual analysis"
    
    def analyze_all_intelligently(self):
        """Analyze with intelligence"""
        print("\n🧠 TRULY INTELLIGENT ANALYSIS")
        print("="*80)
        print("Reading actual code to understand purpose...\n")
        
        for i, script in enumerate(self.scripts, 1):
            if i % 50 == 0:
                print(f"   Progress: {i}/{len(self.scripts)}")
            
            suggested_name, action, reason = self.suggest_intelligent_rename(script)
            
            self.final_suggestions.append({
                'current_name': script['current_name'],
                'suggested_name': suggested_name,
                'action': action,
                'category': script['category'],
                'description': script['description'][:150],
                'suggestion_reason': reason,
                'apis_used': script.get('apis_used', ''),
                'lines': script.get('lines', ''),
                'original_issue': script.get('bad_name_reason', '')
            })
        
        print("\n✅ Intelligent analysis complete!")
    
    def save_csv(self):
        """Save final suggestions"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output = self.pythons_dir / f'_final_rename_plan_{timestamp}.csv'
        
        fieldnames = [
            'current_name',
            'suggested_name',
            'action',
            'category',
            'description',
            'suggestion_reason',
            'apis_used',
            'lines',
            'original_issue'
        ]
        
        # Sort: RENAME with changes first
        def sort_key(x):
            if x['action'] == 'RENAME' and x['current_name'] != x['suggested_name']:
                return (0, x['category'], x['current_name'])
            elif x['action'] == 'DELETE':
                return (1, x['category'], x['current_name'])
            elif x['action'] == 'KEEP':
                return (2, x['category'], x['current_name'])
            else:  # REVIEW
                return (3, x['category'], x['current_name'])
        
        sorted_suggestions = sorted(self.final_suggestions, key=sort_key)
        
        with open(output, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_suggestions)
        
        return output
    
    def print_summary(self):
        """Print summary with actual changes"""
        renames = [s for s in self.final_suggestions 
                   if s['action'] == 'RENAME' and s['current_name'] != s['suggested_name']]
        keeps = [s for s in self.final_suggestions if s['action'] == 'KEEP']
        reviews = [s for s in self.final_suggestions if s['action'] == 'REVIEW']
        deletes = [s for s in self.final_suggestions if s['action'] == 'DELETE']
        
        print("\n" + "="*80)
        print("📊 INTELLIGENT RENAME SUMMARY")
        print("="*80)
        
        print("\n✨ Results:")
        print(f"   🏷️ {len(renames)} files getting better names")
        print(f"   ✅ {len(keeps)} files already perfect")
        print(f"   🗑️ {len(deletes)} files to delete")
        print(f"   📝 {len(reviews)} files need manual review")
        
        # Show top renames by category
        by_cat = {}
        for r in renames:
            cat = r['category']
            by_cat.setdefault(cat, []).append(r)
        
        print("\n📂 Top Renames by Category:")
        for cat in sorted(by_cat.keys(), key=lambda x: len(by_cat[x]), reverse=True)[:5]:
            print(f"\n   {cat} ({len(by_cat[cat])} renames):")
            for item in by_cat[cat][:3]:
                print(f"      {item['current_name']}")
                print(f"      → {item['suggested_name']}")


def main():
    needs_csv = Path.home() / 'pythons' / '_needs_renaming_20251106_133157.csv'
    
    renamer = TrulyIntelligentRenamer(needs_csv)
    renamer.load_csv()
    renamer.analyze_all_intelligently()
    
    output_csv = renamer.save_csv()
    renamer.print_summary()
    
    print(f"\n{'='*80}")
    print("💾 Final rename plan saved to:")
    print(f"   {output_csv}")
    print("\n🎯 This CSV has ACTUAL intelligent suggestions!")
    print("   Review and execute the renames")


if __name__ == '__main__':
    main()
