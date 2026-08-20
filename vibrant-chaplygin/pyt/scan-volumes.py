#!/usr/bin/env python3
"""
Scan External Volumes - Find Python scripts on external drives
"""

import os
import ast
import re
import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

class VolumeScriptScanner:
    """Scan external volumes for Python scripts"""
    
    def __init__(self, volumes_path="/Volumes"):
        self.volumes_path = Path(volumes_path)
        self.results = {
            'volumes_scanned': [],
            'total_files': 0,
            'advanced_scripts': [],
            'by_volume': defaultdict(list),
            'patterns': defaultdict(int),
            'apis': defaultdict(int)
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
            'class_based': r'\bclass\s+\w+',
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
            'NumPy': r'import numpy|np\.',
            'TensorFlow': r'import tensorflow|tf\.',
            'PyTorch': r'import torch',
        }
    
    def analyze_file(self, filepath: Path, volume_name: str):
        """Analyze a single Python file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if len(content) < 100:  # Skip tiny files
                return None
            
            stats = {
                'volume': volume_name,
                'path': str(filepath),
                'name': filepath.name,
                'size': len(content),
                'lines': content.count('\n'),
                'patterns': [],
                'apis': [],
                'classes': 0,
                'functions': 0,
                'score': 0
            }
            
            # Check for module docstring
            if content.strip().startswith('"""') or content.strip().startswith("'''"):
                stats['score'] += 10
            
            # Detect patterns
            for pattern_name, pattern in self.advanced_patterns.items():
                if re.search(pattern, content, re.MULTILINE):
                    stats['patterns'].append(pattern_name)
                    stats['score'] += 5
                    self.results['patterns'][pattern_name] += 1
            
            # Detect API usage
            for api_name, pattern in self.api_patterns.items():
                if re.search(pattern, content):
                    stats['apis'].append(api_name)
                    stats['score'] += 10
                    self.results['apis'][api_name] += 1
            
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
            except:
                pass
            
            # Bonus for multi-API
            if len(stats['apis']) >= 3:
                stats['score'] += 20
            
            return stats
            
        except Exception as e:
            return None
    
    def scan_volume(self, volume_path: Path, max_files=500):
        """Scan a single volume for Python files"""
        volume_name = volume_path.name
        
        print(f"\n🔍 Scanning volume: {volume_name}")
        
        python_files = []
        skip_dirs = {'.Spotlight-V100', '.Trashes', '.fseventsd', 'node_modules', '.git'}
        
        try:
            for root, dirs, files in os.walk(volume_path):
                # Skip system directories
                dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]
                
                for filename in files:
                    if filename.endswith('.py'):
                        filepath = Path(root) / filename
                        python_files.append(filepath)
                        
                        if len(python_files) >= max_files:
                            break
                
                if len(python_files) >= max_files:
                    break
                    
        except PermissionError:
            pass
        
        print(f"   Found {len(python_files)} Python files")
        
        return python_files
    
    def scan_all_volumes(self):
        """Scan all available volumes"""
        print("🚀 VOLUME SCRIPT SCANNER")
        print("="*80)
        print()
        
        if not self.volumes_path.exists():
            print(f"❌ {self.volumes_path} does not exist")
            return
        
        # Get all volumes
        volumes = [v for v in self.volumes_path.iterdir() 
                   if v.is_dir() and v.name != 'Macintosh HD']
        
        if not volumes:
            print("❌ No external volumes found")
            return
        
        print(f"📊 Found {len(volumes)} external volumes:")
        for vol in volumes:
            print(f"   • {vol.name}")
        print()
        
        # Scan each volume
        all_files = []
        for volume in volumes:
            try:
                files = self.scan_volume(volume, max_files=500)
                all_files.extend([(f, volume.name) for f in files])
                self.results['volumes_scanned'].append(volume.name)
            except Exception as e:
                print(f"   ⚠️  Error scanning {volume.name}: {e}")
        
        self.results['total_files'] = len(all_files)
        
        print(f"\n📊 Analyzing {len(all_files)} Python files...")
        print()
        
        # Analyze all files
        for filepath, volume_name in all_files:
            result = self.analyze_file(filepath, volume_name)
            if result and result['score'] > 20:
                self.results['advanced_scripts'].append(result)
                self.results['by_volume'][volume_name].append(result)
        
        # Sort by score
        self.results['advanced_scripts'].sort(key=lambda x: x['score'], reverse=True)
    
    def print_report(self):
        """Print comprehensive report"""
        print("\n" + "="*80)
        print("📊 VOLUME SCAN REPORT")
        print("="*80)
        
        print(f"\n📁 Volumes Scanned: {', '.join(self.results['volumes_scanned'])}")
        print(f"📄 Total Python Files: {self.results['total_files']:,}")
        print(f"⭐ Advanced Scripts Found: {len(self.results['advanced_scripts'])}")
        print()
        
        # By volume breakdown
        print("-"*80)
        print("📊 BY VOLUME")
        print("-"*80)
        for volume, scripts in sorted(self.results['by_volume'].items(), 
                                      key=lambda x: len(x[1]), reverse=True):
            print(f"\n{volume}:")
            print(f"   Advanced scripts: {len(scripts)}")
            if scripts:
                avg_score = sum(s['score'] for s in scripts) / len(scripts)
                print(f"   Average score: {avg_score:.1f}")
                print(f"   Top script: {scripts[0]['name']} (score: {scripts[0]['score']})")
        
        # Top 30 scripts
        print("\n" + "-"*80)
        print("🏆 TOP 30 ADVANCED SCRIPTS")
        print("-"*80)
        for i, script in enumerate(self.results['advanced_scripts'][:30], 1):
            print(f"\n{i}. {script['name']}")
            print(f"   Volume: {script['volume']}")
            print(f"   Path: {script['path'][:100]}")
            print(f"   Score: {script['score']} | Lines: {script['lines']:,} | Classes: {script['classes']} | Functions: {script['functions']}")
            if script['patterns']:
                print(f"   Patterns: {', '.join(script['patterns'][:5])}")
            if script['apis']:
                print(f"   APIs: {', '.join(script['apis'])}")
        
        # Pattern statistics
        print("\n" + "-"*80)
        print("📈 PATTERN USAGE")
        print("-"*80)
        for pattern, count in sorted(self.results['patterns'].items(), 
                                     key=lambda x: x[1], reverse=True)[:15]:
            print(f"  {pattern:25} {count:4} occurrences")
        
        # API statistics
        print("\n" + "-"*80)
        print("🌐 API USAGE")
        print("-"*80)
        for api, count in sorted(self.results['apis'].items(), 
                                 key=lambda x: x[1], reverse=True):
            if count > 0:
                print(f"  {api:25} {count:4} occurrences")
        
        print("\n" + "="*80)
    
    def save_report(self):
        """Save detailed JSON report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = Path.home() / 'pythons' / f'volumes_scan_{timestamp}.json'
        
        report = {
            'timestamp': timestamp,
            'volumes_scanned': self.results['volumes_scanned'],
            'total_files': self.results['total_files'],
            'advanced_scripts_count': len(self.results['advanced_scripts']),
            'top_scripts': self.results['advanced_scripts'][:100],
            'by_volume': {k: len(v) for k, v in self.results['by_volume'].items()},
            'patterns': dict(self.results['patterns']),
            'apis': dict(self.results['apis'])
        }
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Report saved to: {report_path}")
        
        return report_path


def main():
    scanner = VolumeScriptScanner()
    scanner.scan_all_volumes()
    scanner.print_report()
    scanner.save_report()


if __name__ == '__main__':
    main()
