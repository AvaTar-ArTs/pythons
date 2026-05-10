#!/usr/bin/env python3
"""
Comprehensive Script Analyzer
Analyzes ALL Python files and outputs to CSV for batch renaming
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

import re
import ast
import csv
from pathlib import Path
from datetime import datetime

class ComprehensiveScriptAnalyzer:
    """Analyze all Python scripts and generate CSV report"""
    
    def __init__(self, pythons_dir):
        self.pythons_dir = Path(pythons_dir)
        self.results = []
        
    def extract_docstring(self, filepath):
        """Extract module docstring"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Try to parse AST
            try:
                tree = ast.parse(content)
                docstring = ast.get_docstring(tree)
                if docstring:
                    # Get first line or first 100 chars
                    first_line = docstring.split('\n')[0].strip()
                    return first_line[:200] if first_line else docstring[:200]
            except:
                pass
            
            # Fallback: look for """ or ''' at start
            lines = content.split('\n')
            in_docstring = False
            docstring_lines = []
            
            for line in lines[:30]:
                stripped = line.strip()
                if not stripped:
                    continue
                if stripped.startswith('#!'):
                    continue
                if '"""' in line or "'''" in line:
                    if not in_docstring:
                        in_docstring = True
                        # Get text after opening quotes
                        text = line.split('"""')[1] if '"""' in line else line.split("'''")[1]
                        if text.strip():
                            docstring_lines.append(text.strip())
                    else:
                        # Closing quotes
                        text = line.split('"""')[0] if '"""' in line else line.split("'''")[0]
                        if text.strip():
                            docstring_lines.append(text.strip())
                        break
                elif in_docstring:
                    docstring_lines.append(stripped)
            
            if docstring_lines:
                return ' '.join(docstring_lines)[:200]
            
            return "No description found"
            
        except Exception as e:
            return f"Error reading file: {e}"
    
    def detect_apis(self, filepath):
        """Detect which APIs/libraries are used"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            apis = []
            
            api_patterns = {
                'OpenAI': r'openai\.|OpenAI\(',
                'Anthropic': r'anthropic\.|Anthropic\(',
                'Gemini': r'genai\.|GenerativeModel',
                'Groq': r'groq\.|Groq\(',
                'ElevenLabs': r'elevenlabs',
                'AssemblyAI': r'assemblyai',
                'Deepgram': r'deepgram',
                'HuggingFace': r'transformers|from transformers',
                'PIL': r'from PIL|import PIL',
                'Streamlit': r'import streamlit|st\.',
                'FastAPI': r'from fastapi|FastAPI',
                'Pandas': r'import pandas|pd\.',
                'NumPy': r'import numpy|np\.',
                'PyTorch': r'import torch',
                'TensorFlow': r'tensorflow',
                'Whisper': r'import whisper',
                'pydub': r'from pydub|AudioSegment',
                'Requests': r'import requests',
                'Beautiful Soup': r'from bs4|BeautifulSoup',
                'Selenium': r'from selenium|webdriver',
                'Playwright': r'from playwright',
            }
            
            for api_name, pattern in api_patterns.items():
                if re.search(pattern, content):
                    apis.append(api_name)
            
            return ', '.join(apis) if apis else 'None'
            
        except:
            return 'Unknown'
    
    def categorize_script(self, filepath, description, apis):
        """Suggest category based on filename, description, and APIs"""
        filename_lower = filepath.name.lower()
        desc_lower = description.lower()
        apis_lower = apis.lower()
        
        # Image-related
        if any(word in filename_lower + desc_lower for word in ['image', 'photo', 'picture', 'gallery', 'vision', 'pil']):
            if 'prompt' in filename_lower or 'generat' in desc_lower:
                return 'Image Generation'
            return 'Image Analysis'
        
        # Audio-related
        if any(word in filename_lower + desc_lower for word in ['audio', 'tts', 'speech', 'music', 'mp3', 'transcribe', 'whisper']):
            if 'transcrib' in filename_lower + desc_lower:
                return 'Audio Transcription'
            return 'Audio Generation'
        
        # Video-related
        if any(word in filename_lower + desc_lower for word in ['video', 'mp4', 'movie']):
            return 'Video Processing'
        
        # Code analysis
        if any(word in filename_lower + desc_lower for word in ['code', 'complexity', 'quality', 'review', 'ast', 'lint']):
            return 'Code Analysis'
        
        # AI/LLM tools
        if any(word in filename_lower + desc_lower + apis_lower for word in ['gpt', 'claude', 'gemini', 'llm', 'orchestrat']):
            if 'orchestrat' in desc_lower or 'multi' in desc_lower:
                return 'AI Tools'
        
        # Documentation
        if any(word in filename_lower + desc_lower for word in ['docs', 'documentation', 'readme', 'catalog']):
            return 'Documentation'
        
        # File organization
        if any(word in filename_lower + desc_lower for word in ['organiz', 'sort', 'categoriz', 'rename', 'clean', 'flatten', 'migration']):
            return 'File Organization'
        
        # Web scraping
        if any(word in filename_lower + desc_lower for word in ['scrap', 'crawl', 'spider', 'selenium', 'playwright']):
            return 'Web Scraping'
        
        # Social media
        if any(word in filename_lower + desc_lower for word in ['instagram', 'youtube', 'tiktok', 'reddit', 'twitter', 'social']):
            return 'Social Media'
        
        # Data processing
        if any(word in filename_lower + desc_lower for word in ['csv', 'json', 'data', 'process', 'convert']):
            return 'Data Processing'
        
        return 'Utilities'
    
    def should_delete(self, filepath, description):
        """Determine if file should be deleted"""
        filename = filepath.name
        desc_lower = description.lower()
        
        # Library/framework code
        if any(word in filename for word in ['_RefreshThread', 'test_', '_test']):
            return True, "Library/test code - not user created"
        
        # Very specific project files
        if 'alchemyapi' in filename.lower() and 'demo' in filename.lower():
            return True, "Too project-specific"
        
        # IPython/Jupyter test files
        if 'ipython' in desc_lower and 'test' in desc_lower:
            return True, "IPython library test file"
        
        return False, ""
    
    def suggest_rename(self, filepath, description, category):
        """Suggest better filename based on description and category"""
        filename = filepath.stem
        
        # Already has good name?
        good_patterns = [
            r'^[a-z]+-[a-z]+-[a-z]+\.py$',  # kebab-case-name.py
            r'^[a-z]+_[a-z]+_[a-z]+\.py$',  # snake_case_name.py
        ]
        
        # Check if already well-named
        if any(re.match(pattern, filepath.name) for pattern in good_patterns):
            # Check if name matches purpose
            if 'deep' in filename and 'deep' in description.lower():
                return filename + '.py', "KEEP"
            if 'generator' in filename and 'generat' in description.lower():
                return filename + '.py', "KEEP"
        
        # Needs rename - this is where you'll manually review and improve
        return filename + '.py', "REVIEW"
    
    def analyze_all(self):
        """Analyze all Python files"""
        print(f"🔍 Scanning {self.pythons_dir}...")
        
        py_files = sorted([f for f in self.pythons_dir.glob('*.py') if f.is_file()])
        
        print(f"📊 Found {len(py_files)} Python files")
        print("📝 Analyzing...\n")
        
        for i, filepath in enumerate(py_files, 1):
            if i % 10 == 0:
                print(f"   Progress: {i}/{len(py_files)}")
            
            description = self.extract_docstring(filepath)
            apis = self.detect_apis(filepath)
            category = self.categorize_script(filepath, description, apis)
            
            should_del, del_reason = self.should_delete(filepath, description)
            
            if should_del:
                action = "DELETE"
                suggested_name = ""
                reason = del_reason
            else:
                suggested_name, action = self.suggest_rename(filepath, description, category)
                reason = ""
            
            self.results.append({
                'current_name': filepath.name,
                'description': description,
                'category': category,
                'apis_used': apis,
                'suggested_name': suggested_name,
                'action': action,
                'reason': reason,
                'lines': self.count_lines(filepath),
                'size_kb': filepath.stat().st_size / 1024
            })
        
        print("\n✅ Analysis complete!")
        
    def count_lines(self, filepath):
        """Count lines in file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return len(f.readlines())
        except:
            return 0
    
    def save_csv(self):
        """Save results to CSV"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = self.pythons_dir / f'_all_scripts_analysis_{timestamp}.csv'
        
        fieldnames = [
            'current_name',
            'suggested_name',
            'action',
            'category',
            'description',
            'apis_used',
            'lines',
            'size_kb',
            'reason'
        ]
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            # Sort by category, then name
            sorted_results = sorted(self.results, key=lambda x: (x['category'], x['current_name']))
            writer.writerows(sorted_results)
        
        return output_path
    
    def print_summary(self):
        """Print summary statistics"""
        by_category = {}
        by_action = {}
        
        for item in self.results:
            cat = item['category']
            by_category[cat] = by_category.get(cat, 0) + 1
            
            action = item['action']
            by_action[action] = by_action.get(action, 0) + 1
        
        print("\n" + "="*80)
        print("📊 ANALYSIS SUMMARY")
        print("="*80)
        
        print("\n📂 By Category:")
        for cat, count in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
            print(f"   {cat:30} {count:3} files")
        
        print("\n🎯 By Action:")
        for action, count in sorted(by_action.items()):
            emoji = {'DELETE': '🗑️', 'KEEP': '✅', 'REVIEW': '📝', 'RENAME': '🏷️'}.get(action, '📌')
            print(f"   {emoji} {action:10} {count:3} files")
        
        print("\n" + "="*80)


def main():
    pythons_dir = Path.home() / 'pythons'
    
    analyzer = ComprehensiveScriptAnalyzer(pythons_dir)
    analyzer.analyze_all()
    
    csv_path = analyzer.save_csv()
    analyzer.print_summary()
    
    print("\n💾 Results saved to:")
    print(f"   {csv_path}")
    print("\n💡 Next steps:")
    print(f"   1. Open CSV in spreadsheet: open {csv_path}")
    print("   2. Review and edit 'suggested_name' column")
    print("   3. Update 'action' column (RENAME/DELETE/KEEP)")
    print("   4. Run batch rename script")


if __name__ == '__main__':
    main()
