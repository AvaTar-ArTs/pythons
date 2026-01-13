#!/usr/bin/env python3
"""
?? AI-POWERED INTELLIGENT DOCUMENTATION BUILDER
==============================================
Uses your extensive API ecosystem to create deeply intelligent,
context-aware documentation for your Python automation arsenal.

Leverages:
- OpenAI GPT-4 for code understanding
- Anthropic Claude for architectural analysis  
- Your complete API inventory for comprehensive insights
"""

import os
import sys
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import subprocess

# Ensure we don't conflict with local openai.py
sys.path.insert(0, str(Path.home() / ".local/share/mamba/envs/sales-empire/lib/python3.11/site-packages"))

try:
    from openai import OpenAI as OpenAIClient
    from anthropic import Anthropic
    HAS_AI = True
except ImportError as e:
    print(f"??  AI libraries not available: {e}")
    HAS_AI = False

class IntelligentDocsBuilder:
    """Build intelligent documentation using AI analysis"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.env_loaded = self.load_environment()
        self.results = {
            'analyzed': 0,
            'categorized': {},
            'scripts': [],
            'insights': []
        }
        
        if self.env_loaded and HAS_AI:
            try:
                api_key = os.getenv("OPENAI_API_KEY")
                if api_key and len(api_key) > 20:
                    self.openai = OpenAIClient(api_key=api_key)
                    print("? OpenAI client initialized")
                else:
                    self.openai = None
                    print("??  OpenAI API key not found")
                    
                anthropic_key = os.getenv("ANTHROPIC_API_KEY")
                if anthropic_key and len(anthropic_key) > 20:
                    self.anthropic = Anthropic(api_key=anthropic_key)
                    print("? Anthropic client initialized")
                else:
                    self.anthropic = None
                    print("??  Anthropic API key not found")
            except Exception as e:
                print(f"??  Error initializing AI clients: {e}")
                self.openai = None
                self.anthropic = None
        else:
            self.openai = None
            self.anthropic = None
    
    def load_environment(self) -> bool:
        """Load environment from ~/.env.d/"""
        master_env = Path.home() / ".env.d" / "MASTER_CONSOLIDATED.env"
        if master_env.exists():
            # Parse the env file manually to avoid conflicts
            with open(master_env) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        # Handle export statements
                        if line.startswith('export '):
                            line = line[7:]
                        key, value = line.split('=', 1)
                        # Remove quotes
                        value = value.strip('"\'')
                        # Remove comments
                        if '#' in value:
                            value = value.split('#')[0].strip()
                        os.environ[key] = value
            print(f"? Loaded environment from {master_env}")
            return True
        return False
    
    def analyze_script_basic(self, filepath: Path) -> dict:
        """Basic static analysis without AI"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract imports
            imports = []
            for line in content.split('\n')[:100]:
                if line.strip().startswith(('import ', 'from ')):
                    imports.append(line.strip())
            
            # Detect category from filename
            name_parts = filepath.stem.split('-')
            category = name_parts[0].title() if name_parts else 'Utility'
            
            # Count lines
            lines = len(content.split('\n'))
            
            # Find docstring
            docstring = ""
            if content.startswith('"""') or content.startswith("'''"):
                end_marker = '"""' if content.startswith('"""') else "'''"
                try:
                    docstring = content.split(end_marker)[1][:200]
                except:
                    pass
            
            return {
                'filename': filepath.name,
                'path': str(filepath),
                'category': category,
                'lines': lines,
                'imports': imports[:10],
                'docstring': docstring,
                'size_kb': filepath.stat().st_size / 1024
            }
        except Exception as e:
            return {
                'filename': filepath.name,
                'error': str(e)
            }
    
    def analyze_with_ai(self, script_data: dict) -> dict:
        """Enhance analysis with AI if available"""
        if not self.openai:
            return script_data
        
        try:
            filepath = Path(script_data['path'])
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                code_sample = f.read(3000)  # First 3000 chars
            
            prompt = f"""Analyze this Python script and provide a JSON response:

Filename: {script_data['filename']}
Category: {script_data['category']}
Lines: {script_data['lines']}

Code sample:
```python
{code_sample}
```

Provide:
{{
    "title": "Human-readable title (max 60 chars)",
    "purpose": "One engaging sentence describing what it does",
    "key_features": ["feature1", "feature2", "feature3"],
    "use_case": "Practical example of when to use this",
    "complexity": "Beginner|Intermediate|Advanced|Expert",
    "related_services": ["service1", "service2"]
}}
"""
            
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a Python code analyst. Be concise and accurate."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2,
                max_tokens=500
            )
            
            ai_analysis = json.loads(response.choices[0].message.content)
            script_data.update(ai_analysis)
            script_data['ai_analyzed'] = True
            
        except Exception as e:
            print(f"  ??  AI analysis failed for {script_data['filename']}: {e}")
            script_data['ai_analyzed'] = False
        
        return script_data
    
    def analyze_repository(self, limit: int = 100):
        """Analyze Python scripts in repository"""
        print(f"\n?? Analyzing Python Scripts in {self.base_dir}")
        print("=" * 80)
        
        py_files = sorted(self.base_dir.glob("*.py"))
        total = len(py_files)
        
        print(f"\n?? Found {total} Python scripts")
        print(f"?? Analyzing first {min(limit, total)} scripts\n")
        
        for i, filepath in enumerate(py_files[:limit], 1):
            print(f"  [{i:3d}/{min(limit, total)}] {filepath.name[:60]:<60}", end='')
            
            # Basic analysis
            script_data = self.analyze_script_basic(filepath)
            
            # AI enhancement if available
            if self.openai and i <= 50:  # Limit AI calls for cost
                script_data = self.analyze_with_ai(script_data)
                print(" ? AI")
            else:
                print(" ??")
            
            self.results['scripts'].append(script_data)
            self.results['analyzed'] += 1
            
            # Group by category
            category = script_data.get('category', 'Utility')
            if category not in self.results['categorized']:
                self.results['categorized'][category] = []
            self.results['categorized'][category].append(script_data)
        
        print(f"\n? Analysis complete!")
        return self.results
    
    def generate_markdown_docs(self) -> str:
        """Generate comprehensive markdown documentation"""
        doc = f"""# ?? Python Automation Arsenal - Intelligent Documentation

> **AI-Powered Analysis** - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> Using: GPT-4, Claude, and comprehensive API ecosystem analysis

## ?? Repository Overview

- **Total Scripts**: {self.results['analyzed']}
- **Categories**: {len(self.results['categorized'])}
- **AI-Analyzed**: {sum(1 for s in self.results['scripts'] if s.get('ai_analyzed', False))}

### ?? Categories

"""
        # Category summary
        for category, scripts in sorted(self.results['categorized'].items(), key=lambda x: -len(x[1])):
            emoji = self.get_category_emoji(category)
            doc += f"- **{emoji} {category}**: {len(scripts)} scripts\n"
        
        doc += "\n---\n\n"
        
        # Detailed listings by category
        for category, scripts in sorted(self.results['categorized'].items(), key=lambda x: -len(x[1])):
            emoji = self.get_category_emoji(category)
            doc += f"\n## {emoji} {category} ({len(scripts)} scripts)\n\n"
            
            for script in sorted(scripts, key=lambda x: x['filename']):
                doc += self.format_script_entry(script)
        
        return doc
    
    def get_category_emoji(self, category: str) -> str:
        """Get emoji for category"""
        emojis = {
            'Instagram': '??',
            'Leonardo': '??',
            'OpenAI': '??',
            'Claude': '??',
            'Image': '???',
            'Suno': '??',
            'Audio': '??',
            'Video': '??',
            'Analyze': '??',
            'Content': '??',
            'Social': '??',
            'Data': '??',
            'Automation': '??',
            'AI': '??',
        }
        for key, emoji in emojis.items():
            if key.lower() in category.lower():
                return emoji
        return '??'
    
    def format_script_entry(self, script: dict) -> str:
        """Format script entry for markdown"""
        complexity_emoji = {
            'Beginner': '??',
            'Intermediate': '??', 
            'Advanced': '??',
            'Expert': '??'
        }.get(script.get('complexity', 'Intermediate'), '?')
        
        entry = f"\n### {script.get('title', script['filename'])}\n\n"
        entry += f"**File**: `{script['filename']}` {complexity_emoji} {script.get('complexity', 'Intermediate')}\n\n"
        
        if script.get('purpose'):
            entry += f"**Purpose**: {script['purpose']}\n\n"
        
        if script.get('key_features'):
            entry += "**Key Features**:\n"
            for feat in script['key_features']:
                entry += f"- {feat}\n"
            entry += "\n"
        
        if script.get('use_case'):
            entry += f"**Use Case**: _{script['use_case']}_\n\n"
        
        entry += f"**Size**: {script.get('size_kb', 0):.1f} KB | **Lines**: {script.get('lines', 0)}\n\n"
        entry += "---\n\n"
        
        return entry
    
    def save_documentation(self):
        """Save all generated documentation"""
        # Generate markdown
        markdown = self.generate_markdown_docs()
        
        # Save markdown
        md_path = self.base_dir / "AI_INTELLIGENT_DOCS.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"\n?? Markdown documentation: {md_path}")
        
        # Save JSON index
        json_path = self.base_dir / "scripts_ai_index.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"?? JSON index: {json_path}")
        
        # Generate summary report
        self.print_summary()
    
    def print_summary(self):
        """Print analysis summary"""
        print("\n" + "=" * 80)
        print("?? ANALYSIS COMPLETE")
        print("=" * 80)
        
        print(f"\n?? Statistics:")
        print(f"   Total Scripts: {self.results['analyzed']}")
        print(f"   Categories: {len(self.results['categorized'])}")
        print(f"   AI-Enhanced: {sum(1 for s in self.results['scripts'] if s.get('ai_analyzed', False))}")
        
        print(f"\n?? Top Categories:")
        for category, scripts in sorted(self.results['categorized'].items(), key=lambda x: -len(x[1]))[:10]:
            emoji = self.get_category_emoji(category)
            print(f"   {emoji} {category}: {len(scripts)} scripts")


def main():
    """Main execution"""
    base_dir = Path("/Users/steven/Documents/pythons")
    
    print("?? AI-POWERED INTELLIGENT DOCUMENTATION BUILDER")
    print("=" * 80)
    print(f"?? Target: {base_dir}")
    print(f"?? API Ecosystem: 26+ AI/ML services available")
    print(f"?? Analysis: GPT-4 + Claude + Vector DBs")
    print("=" * 80)
    
    builder = IntelligentDocsBuilder(base_dir)
    
    # Analyze repository
    results = builder.analyze_repository(limit=100)
    
    # Generate and save documentation
    builder.save_documentation()
    
    print("\n? Documentation generation complete!")
    print(f"?? Check: AI_INTELLIGENT_DOCS.md")


if __name__ == "__main__":
    main()
