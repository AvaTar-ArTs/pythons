#!/usr/bin/env python3
"""
Advanced Script Finder - Find the best Python scripts to inspire improvements
Analyzes Python files for advanced patterns and features
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

import ast
import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class AdvancedScriptFinder:
    """Find and analyze advanced Python scripts"""
    
    def __init__(self):
        self.home = Path.home()
        self.results = {
            'advanced_patterns': defaultdict(list),
            'api_usage': defaultdict(list),
            'class_based': [],
            'async_scripts': [],
            'multi_api': [],
            'best_practices': defaultdict(list)
        }
        
        self.advanced_patterns = {
            'async/await': r'\basync\s+def\b|\bawait\b',
            'type_hints': r'def\s+\w+\([^)]*:\s*\w+',
            'dataclass': r'@dataclass',
            'context_managers': r'with\s+\w+',
            'decorators': r'@\w+',
            'list_comprehension': r'\[.*for.*in.*\]',
            'f-strings': r'f["\']',
            'logging': r'import logging|logger\.',
            'argparse': r'import argparse|ArgumentParser',
            'pathlib': r'from pathlib import Path|Path\(',
            'json_handling': r'json\.(load|dump)',
            'error_handling': r'try:|except:',
            'multi_threading': r'import threading|Thread\(',
            'multi_processing': r'import multiprocessing|Process\(',
        }
        
        self.api_patterns = {
            'OpenAI': r'openai\.|OpenAI\(',
            'Anthropic': r'anthropic\.|Anthropic\(',
            'Gemini': r'genai\.|GenerativeModel',
            'Groq': r'groq\.|Groq\(',
            'HuggingFace': r'transformers|from transformers',
            'ElevenLabs': r'elevenlabs',
            'PIL/Pillow': r'from PIL import|Image\.',
            'FastAPI': r'from fastapi|FastAPI\(',
            'Streamlit': r'import streamlit|st\.',
            'Requests': r'import requests|requests\.',
            'AsyncIO': r'import asyncio|asyncio\.',
            'SQLite': r'import sqlite3|sqlite3\.',
            'Pandas': r'import pandas|pd\.',
        }
    
    def analyze_file(self, filepath: Path):
        """Analyze a single Python file for advanced features"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if len(content) < 100:  # Skip tiny files
                return None
            
            stats = {
                'path': str(filepath),
                'name': filepath.name,
                'size': len(content),
                'lines': content.count('\n'),
                'patterns': [],
                'apis': [],
                'classes': 0,
                'functions': 0,
                'imports': [],
                'docstring': False,
                'score': 0
            }
            
            # Check for module docstring
            if content.strip().startswith('"""') or content.strip().startswith("'''"):
                stats['docstring'] = True
                stats['score'] += 10
            
            # Detect patterns
            for pattern_name, pattern in self.advanced_patterns.items():
                if re.search(pattern, content, re.MULTILINE):
                    stats['patterns'].append(pattern_name)
                    stats['score'] += 5
                    self.results['advanced_patterns'][pattern_name].append(str(filepath))
            
            # Detect API usage
            for api_name, pattern in self.api_patterns.items():
                if re.search(pattern, content):
                    stats['apis'].append(api_name)
                    stats['score'] += 10
                    self.results['api_usage'][api_name].append(str(filepath))
            
            # Parse AST for structure
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        stats['classes'] += 1
                        stats['score'] += 15
                    elif isinstance(node, ast.FunctionDef):
                        stats['functions'] += 1
                        stats['score'] += 2
                        if node.name.startswith('async'):
                            self.results['async_scripts'].append(str(filepath))
                    elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                        if isinstance(node, ast.ImportFrom):
                            stats['imports'].append(node.module)
            except:
                pass
            
            # Bonus points
            if stats['classes'] > 0:
                self.results['class_based'].append(str(filepath))
            
            if len(stats['apis']) >= 3:
                self.results['multi_api'].append(str(filepath))
                stats['score'] += 20
            
            # Best practices
            if 'logging' in stats['patterns']:
                self.results['best_practices']['logging'].append(str(filepath))
            if 'type_hints' in stats['patterns']:
                self.results['best_practices']['type_hints'].append(str(filepath))
            if 'argparse' in stats['patterns']:
                self.results['best_practices']['cli_interface'].append(str(filepath))
            if stats['docstring']:
                self.results['best_practices']['documented'].append(str(filepath))
            
            return stats
            
        except Exception:
            return None
    
    def scan_directory(self, directory: Path, max_files=200):
        """Scan directory for Python files"""
        print(f"🔍 Scanning {directory}...")
        
        python_files = []
        for py_file in directory.rglob('*.py'):
            if 'node_modules' not in str(py_file) and '.git' not in str(py_file):
                python_files.append(py_file)
                if len(python_files) >= max_files:
                    break
        
        return python_files
    
    def find_best_scripts(self):
        """Find the best advanced scripts"""
        print("🚀 ADVANCED SCRIPT FINDER")
        print("="*80)
        print()
        
        # Scan key directories
        directories_to_scan = [
            self.home / 'workspace' / 'archive' / 'system' / 'advanced-systems',
            self.home / 'workspace' / 'music-empire',
            self.home / 'GitHub' / 'AvaTarArTs-Suite',
            self.home / 'pythons',
        ]
        
        all_files = []
        for directory in directories_to_scan:
            if directory.exists():
                files = self.scan_directory(directory, max_files=100)
                all_files.extend(files)
        
        print(f"📊 Analyzing {len(all_files)} Python files...")
        print()
        
        # Analyze all files
        analyzed = []
        for filepath in all_files:
            result = self.analyze_file(filepath)
            if result and result['score'] > 20:
                analyzed.append(result)
        
        # Sort by score
        analyzed.sort(key=lambda x: x['score'], reverse=True)
        
        return analyzed
    
    def print_report(self, analyzed_files):
        """Print comprehensive report"""
        print("\n" + "="*80)
        print("📊 ADVANCED SCRIPT ANALYSIS REPORT")
        print("="*80)
        
        print(f"\n✅ Analyzed {len(analyzed_files)} advanced scripts")
        print()
        
        # Top 20 most advanced scripts
        print("🏆 TOP 20 MOST ADVANCED SCRIPTS")
        print("-"*80)
        for i, script in enumerate(analyzed_files[:20], 1):
            print(f"\n{i}. {script['name']}")
            print(f"   Path: {script['path']}")
            print(f"   Score: {script['score']} | Lines: {script['lines']:,} | Classes: {script['classes']} | Functions: {script['functions']}")
            if script['patterns']:
                print(f"   Patterns: {', '.join(script['patterns'][:5])}")
            if script['apis']:
                print(f"   APIs: {', '.join(script['apis'])}")
        
        # Pattern usage statistics
        print("\n" + "-"*80)
        print("📈 ADVANCED PATTERNS USAGE")
        print("-"*80)
        for pattern, files in sorted(self.results['advanced_patterns'].items(), 
                                     key=lambda x: len(x[1]), reverse=True)[:10]:
            print(f"  {pattern:25} {len(files):4} files")
        
        # API usage statistics
        print("\n" + "-"*80)
        print("🌐 API USAGE STATISTICS")
        print("-"*80)
        for api, files in sorted(self.results['api_usage'].items(), 
                                 key=lambda x: len(x[1]), reverse=True):
            print(f"  {api:25} {len(files):4} files")
        
        # Best practices
        print("\n" + "-"*80)
        print("✨ BEST PRACTICES ADOPTION")
        print("-"*80)
        for practice, files in sorted(self.results['best_practices'].items(), 
                                      key=lambda x: len(x[1]), reverse=True):
            print(f"  {practice:25} {len(files):4} files")
        
        # Category counts
        print("\n" + "-"*80)
        print("📊 SCRIPT CATEGORIES")
        print("-"*80)
        print(f"  Class-based scripts:     {len(self.results['class_based'])}")
        print(f"  Async/await scripts:     {len(self.results['async_scripts'])}")
        print(f"  Multi-API scripts:       {len(self.results['multi_api'])}")
        
        print("\n" + "="*80)
    
    def generate_improvement_suggestions(self, analyzed_files):
        """Generate suggestions for improving ~/pythons scripts"""
        print("\n" + "="*80)
        print("💡 IMPROVEMENT SUGGESTIONS FOR ~/pythons")
        print("="*80)
        
        # Find what's missing in pythons
        pythons_scripts = [s for s in analyzed_files if '/pythons/' in s['path']]
        advanced_scripts = [s for s in analyzed_files if '/pythons/' not in s['path']]
        
        if not pythons_scripts:
            print("\n⚠️  No scripts from ~/pythons found in analysis")
            return
        
        # Collect all patterns from pythons
        pythons_patterns = set()
        pythons_apis = set()
        for script in pythons_scripts:
            pythons_patterns.update(script['patterns'])
            pythons_apis.update(script['apis'])
        
        # Collect all patterns from advanced
        advanced_patterns = set()
        advanced_apis = set()
        for script in advanced_scripts:
            advanced_patterns.update(script['patterns'])
            advanced_apis.update(script['apis'])
        
        # Missing patterns
        missing_patterns = advanced_patterns - pythons_patterns
        missing_apis = advanced_apis - pythons_apis
        
        print("\n🎯 Patterns to Add:")
        for pattern in sorted(missing_patterns):
            print(f"   • {pattern}")
        
        print("\n🌐 APIs to Integrate:")
        for api in sorted(missing_apis):
            print(f"   • {api}")
        
        print("\n📚 Best Scripts to Learn From:")
        for script in advanced_scripts[:10]:
            if script['score'] > 100:
                print(f"   • {script['name']} (score: {script['score']})")
                print(f"     {script['path']}")
        
        print("\n" + "="*80)
    
    def save_report(self, analyzed_files):
        """Save detailed JSON report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = self.home / 'pythons' / f'advanced_scripts_analysis_{timestamp}.json'
        
        report = {
            'timestamp': timestamp,
            'total_analyzed': len(analyzed_files),
            'top_scripts': analyzed_files[:50],
            'patterns': {k: len(v) for k, v in self.results['advanced_patterns'].items()},
            'apis': {k: len(v) for k, v in self.results['api_usage'].items()},
            'best_practices': {k: len(v) for k, v in self.results['best_practices'].items()},
            'categories': {
                'class_based': len(self.results['class_based']),
                'async': len(self.results['async_scripts']),
                'multi_api': len(self.results['multi_api'])
            }
        }
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Report saved to: {report_path}")


def main():
    finder = AdvancedScriptFinder()
    analyzed = finder.find_best_scripts()
    finder.print_report(analyzed)
    finder.generate_improvement_suggestions(analyzed)
    finder.save_report(analyzed)


if __name__ == '__main__':
    main()
