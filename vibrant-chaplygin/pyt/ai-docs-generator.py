#!/usr/bin/env python3
"""
AI-Powered Documentation Generator
Uses OpenAI GPT-4 to intelligently analyze and document Python scripts
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import anthropic
from openai import OpenAI
import json
from collections import defaultdict

# Load environment from master consolidated
load_dotenv("/Users/steven/.env.d/MASTER_CONSOLIDATED.env")

class IntelligentDocGenerator:
    """Generate intelligent documentation using AI analysis"""
    
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_client = OpenAI(api_key=self.openai_key) if self.openai_key else None
        self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_key) if self.anthropic_key else None
        
    def analyze_script_with_ai(self, filepath: Path) -> dict:
        """Use AI to deeply understand a script's purpose and capabilities"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read(4000)  # First 4000 chars
                
            prompt = f"""Analyze this Python script and provide:
1. Primary Purpose (1 sentence, engaging and descriptive)
2. Category (choose: Instagram, AI/ML, Content Creation, Image Processing, Audio/Video, Data Processing, Social Media, Automation, Utilities)
3. Key Features (3-5 bullet points)
4. Dependencies (list main imports)
5. Use Case Example (practical scenario)
6. Complexity Level (Beginner/Intermediate/Advanced/Expert)

Filename: {filepath.name}

Code:
```python
{code}
```

Return JSON format:
{{
    "title": "Human-Readable Title",
    "purpose": "One engaging sentence",
    "category": "Category",
    "features": ["feature1", "feature2"],
    "dependencies": ["dep1", "dep2"],
    "use_case": "Practical example",
    "complexity": "Level",
    "tags": ["tag1", "tag2"]
}}
"""
            
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",  # Faster and cheaper for analysis
                    messages=[
                        {"role": "system", "content": "You are an expert Python code analyst. Provide clear, engaging, and accurate analysis."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.3
                )
                
                result = json.loads(response.choices[0].message.content)
                result['filename'] = filepath.name
                result['analyzed_by'] = 'openai-gpt4'
                return result
                
        except Exception as e:
            print(f"Error analyzing {filepath.name}: {e}")
            return self._fallback_analysis(filepath)
    
    def _fallback_analysis(self, filepath: Path) -> dict:
        """Basic analysis when AI fails"""
        name_parts = filepath.stem.split('-')
        service = name_parts[0] if name_parts else 'utility'
        
        return {
            'filename': filepath.name,
            'title': filepath.stem.replace('-', ' ').title(),
            'purpose': f'Python automation script for {service} operations',
            'category': service.title(),
            'features': ['Automated processing', 'Error handling'],
            'dependencies': ['Unknown'],
            'use_case': f'Run to execute {service} automation tasks',
            'complexity': 'Intermediate',
            'tags': [service],
            'analyzed_by': 'fallback'
        }
    
    def analyze_relationships(self, scripts: list) -> dict:
        """Use Claude to understand relationships between scripts"""
        if not self.anthropic_client:
            return {}
            
        script_summary = "\n".join([
            f"- {s['filename']}: {s.get('purpose', 'Unknown')}"
            for s in scripts[:50]  # First 50 for context
        ])
        
        prompt = f"""Analyze these Python automation scripts and identify:
1. Common workflows (which scripts work together)
2. Dependencies between scripts
3. Recommended execution order for common tasks
4. Script families (groups of related functionality)

Scripts:
{script_summary}

Provide a structured analysis of how these scripts relate to each other.
"""
        
        try:
            message = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                'relationships': message.content[0].text,
                'analyzed_by': 'claude-sonnet'
            }
        except Exception as e:
            print(f"Error in relationship analysis: {e}")
            return {}
    
    def generate_comprehensive_docs(self, base_dir: Path):
        """Generate full documentation with AI insights"""
        print("?? Starting AI-Powered Documentation Generation...")
        print(f"?? Analyzing: {base_dir}")
        
        # Collect all Python scripts
        scripts = []
        py_files = list(base_dir.glob("*.py"))
        total = len(py_files)
        
        print(f"\n?? Found {total} Python scripts to analyze\n")
        
        # Analyze each script
        for i, filepath in enumerate(py_files[:100], 1):  # First 100 scripts
            print(f"  [{i}/{min(100, total)}] Analyzing {filepath.name}...")
            analysis = self.analyze_script_with_ai(filepath)
            scripts.append(analysis)
            
            if i % 10 == 0:
                print(f"  ? Completed {i} scripts")
        
        # Group by category
        by_category = defaultdict(list)
        for script in scripts:
            category = script.get('category', 'Utilities')
            by_category[category].append(script)
        
        # Generate markdown documentation
        docs = self._generate_markdown(scripts, by_category)
        
        # Save documentation
        docs_path = base_dir / "INTELLIGENT_DOCUMENTATION.md"
        with open(docs_path, 'w') as f:
            f.write(docs)
        
        print(f"\n? Documentation generated: {docs_path}")
        
        # Generate JSON index
        index_path = base_dir / "scripts_index.json"
        with open(index_path, 'w') as f:
            json.dump({
                'total_scripts': len(scripts),
                'categories': {cat: len(items) for cat, items in by_category.items()},
                'scripts': scripts
            }, f, indent=2)
        
        print(f"?? Index generated: {index_path}")
        
        return scripts, by_category
    
    def _generate_markdown(self, scripts: list, by_category: dict) -> str:
        """Generate beautiful markdown documentation"""
        md = """# ?? AI-Analyzed Python Automation Arsenal

> **Intelligent Documentation** - Generated using GPT-4 and Claude for deep code understanding

## ?? Overview

This repository contains **{total}** Python automation scripts, intelligently categorized and analyzed for optimal discovery and usage.

### ?? Categories at a Glance

{category_summary}

---

## ?? Detailed Script Catalog

""".format(
            total=len(scripts),
            category_summary=self._format_category_summary(by_category)
        )
        
        # Add each category
        for category, items in sorted(by_category.items()):
            md += f"\n### ?? {category} ({len(items)} scripts)\n\n"
            
            for script in sorted(items, key=lambda x: x['filename']):
                md += self._format_script_entry(script)
        
        return md
    
    def _format_category_summary(self, by_category: dict) -> str:
        """Format category summary table"""
        lines = []
        for cat, items in sorted(by_category.items(), key=lambda x: -len(x[1])):
            emoji = self._get_category_emoji(cat)
            lines.append(f"- **{emoji} {cat}**: {len(items)} scripts")
        return "\n".join(lines)
    
    def _get_category_emoji(self, category: str) -> str:
        """Get emoji for category"""
        emojis = {
            'Instagram': '??',
            'AI/ML': '??',
            'Content Creation': '??',
            'Image Processing': '???',
            'Audio/Video': '??',
            'Data Processing': '??',
            'Social Media': '??',
            'Automation': '??',
            'Utilities': '???',
            'Leonardo': '??',
            'OpenAI': '??',
            'Suno': '??',
        }
        return emojis.get(category, '??')
    
    def _format_script_entry(self, script: dict) -> str:
        """Format individual script entry"""
        complexity_badge = {
            'Beginner': '??',
            'Intermediate': '??',
            'Advanced': '??',
            'Expert': '??'
        }.get(script.get('complexity', 'Intermediate'), '?')
        
        entry = f"""
#### {script.get('title', script['filename'])}

**File**: `{script['filename']}` {complexity_badge} *{script.get('complexity', 'Intermediate')}*

**Purpose**: {script.get('purpose', 'N/A')}

**Key Features**:
{self._format_features(script.get('features', []))}

**Use Case**: _{script.get('use_case', 'See documentation')}_

**Tags**: {', '.join(f'`{tag}`' for tag in script.get('tags', []))}

---

"""
        return entry
    
    def _format_features(self, features: list) -> str:
        """Format feature list"""
        if not features:
            return "- No features documented"
        return "\n".join(f"- {feat}" for feat in features)


def main():
    """Main execution"""
    base_dir = Path("/Users/steven/Documents/pythons")
    
    generator = IntelligentDocGenerator()
    
    if not generator.openai_client and not generator.anthropic_client:
        print("??  Warning: No AI API keys found. Using fallback analysis.")
        print("Set OPENAI_API_KEY or ANTHROPIC_API_KEY for intelligent analysis.")
    
    scripts, categories = generator.generate_comprehensive_docs(base_dir)
    
    print(f"\n?? Complete! Analyzed {len(scripts)} scripts across {len(categories)} categories")
    print("\nTop Categories:")
    for cat, items in sorted(categories.items(), key=lambda x: -len(x[1]))[:5]:
        print(f"  ? {cat}: {len(items)} scripts")


if __name__ == "__main__":
    main()
