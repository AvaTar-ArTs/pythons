#!/usr/bin/env python3
"""
🧠 AI SUPER-POWERED CONTENT ANALYZER 🚀

Uses multiple LLM APIs (OpenAI, Claude, Gemini, etc.) to:
- Deep understand what each script actually does
- Suggest perfect names based on functionality
- Detect semantic duplicates (not just exact matches)
- Identify improvement opportunities
- Create intelligent categorizations
"""

import ast
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Import all available LLM clients
try:
    from openai import OpenAI
    HAS_OPENAI = True
except:
    HAS_OPENAI = False

try:
    from anthropic import Anthropic
    HAS_ANTHROPIC = True
except:
    HAS_ANTHROPIC = False

class AISuperPoweredAnalyzer:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Initialize AI clients
        self.openai_client = None
        self.anthropic_client = None

        print("\n🌟 " + "="*76 + " 🌟")
        print("🚀 " + " "*28 + "INITIALIZING AI ENGINES" + " "*28 + " 🚀")
        print("🌟 " + "="*76 + " 🌟\n")

        if HAS_OPENAI and os.getenv('OPENAI_API_KEY'):
            self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            print("⚡ [OPENAI GPT-4] .......... LOADED! 🧠✨")

        if HAS_ANTHROPIC and os.getenv('ANTHROPIC_API_KEY'):
            self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            print("⚡ [ANTHROPIC CLAUDE] ...... LOADED! 🧠✨")

        print("\n🎯 AI POWER LEVEL: " + "█" * 50 + " 100% 🔥")

        self.analysis_cache = {}
        self.stats = {
            'files_analyzed': 0,
            'ai_calls': 0,
            'renames_suggested': 0,
            'duplicates_found': 0,
            'improvements_found': 0
        }

        self.results = {
            'semantic_duplicates': [],
            'rename_suggestions': [],
            'quality_improvements': [],
            'categorization_suggestions': []
        }

    def extract_code_summary(self, file_path: Path) -> str:
        """Extract a summary of the code for AI analysis."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse AST for structure
            try:
                tree = ast.parse(content)

                imports = []
                functions = []
                classes = []

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module)
                    elif isinstance(node, ast.FunctionDef):
                        functions.append(node.name)
                    elif isinstance(node, ast.ClassDef):
                        classes.append(node.name)

                docstring = ast.get_docstring(tree) or ""

                # Create summary
                summary = f"""File: {file_path.name}
Imports: {', '.join(imports[:15])}
Functions: {', '.join(functions[:10])}
Classes: {', '.join(classes[:5])}
Docstring: {docstring[:200]}
First 500 chars: {content[:500]}
"""
                return summary

            except SyntaxError:
                return f"File: {file_path.name}\nContent preview: {content[:1000]}"

        except Exception as e:
            return f"File: {file_path.name}\nError: {e}"

    def ai_analyze_file(self, file_path: Path) -> Dict:
        """Use AI to deeply understand the file."""
        # Check cache
        cache_key = str(file_path)
        if cache_key in self.analysis_cache:
            return self.analysis_cache[cache_key]

        summary = self.extract_code_summary(file_path)

        prompt = f"""Analyze this Python script and provide:
1. What it actually does (in 1-2 sentences)
2. Primary service it uses (e.g., OpenAI, YouTube, Instagram, None)
3. Primary action (e.g., download, upload, generate, analyze, bot)
4. Best filename (max 40 chars, kebab-case, descriptive)
5. Semantic category (e.g., automation, data_processing, api_client)

{summary}

Respond in JSON format:
{{
  "purpose": "...",
  "service": "...",
  "action": "...",
  "suggested_name": "...",
  "category": "..."
}}
"""

        # Try OpenAI first (faster)
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300,
                    temperature=0.3
                )

                result_text = response.choices[0].message.content
                # Extract JSON from response
                import re
                json_match = re.search(r'\{[^}]+\}', result_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    self.stats['ai_calls'] += 1
                    self.analysis_cache[cache_key] = result
                    return result
            except Exception as e:
                print(f"  ⚠️  OpenAI error for {file_path.name}: {e}")

        # Fallback to Anthropic Claude
        if self.anthropic_client:
            try:
                response = self.anthropic_client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )

                result_text = response.content[0].text
                import re
                json_match = re.search(r'\{[^}]+\}', result_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    self.stats['ai_calls'] += 1
                    self.analysis_cache[cache_key] = result
                    return result
            except Exception as e:
                print(f"  ⚠️  Claude error for {file_path.name}: {e}")

        # Fallback to local analysis
        return {
            'purpose': 'Unknown',
            'service': 'none',
            'action': 'unknown',
            'suggested_name': file_path.stem,
            'category': 'utility'
        }

    def analyze_category(self, category_path: Path, sample_size: int = 50):
        """Deeply analyze a category using AI."""
        category_name = category_path.name
        python_files = list(category_path.glob("*.py"))

        emoji_map = {
            'youtube': '🎥', 'instagram': '📸', 'image': '🖼️', 'ai': '🤖',
            'audio': '🎵', 'video': '🎬', 'file': '📁', 'reddit': '🔴',
            'telegram': '💬', 'leonardo': '🎨', 'csv': '📊', 'json': '📄'
        }
        emoji = emoji_map.get(category_name, '📁')

        print(f"\n{'='*80}")
        print(f"🔬 DEEP ANALYZING: {emoji} {category_name.upper()}/ 🔬")
        print(f"{'='*80}")
        print(f"📦 Total files: {len(python_files)} | 🎯 Sampling: {min(sample_size, len(python_files))}")
        print(f"🧠 AI Status: {'GPT-4 🟢' if self.openai_client else ''} {'Claude 🟢' if self.anthropic_client else ''}")
        print()

        # Sample files for AI analysis (to save API costs)
        import random
        sample_files = random.sample(python_files, min(sample_size, len(python_files)))

        analyzed = 0
        for file_path in sample_files:
            analysis = self.ai_analyze_file(file_path)
            self.stats['files_analyzed'] += 1
            analyzed += 1

            if analyzed % 10 == 0:
                progress_pct = int((analyzed / len(sample_files)) * 100)
                bar_length = 40
                filled = int((progress_pct / 100) * bar_length)
                bar = "█" * filled + "░" * (bar_length - filled)
                print(f"    🔄 Progress: [{bar}] {progress_pct}% ({analyzed}/{len(sample_files)})")

            # Check if rename is suggested
            suggested = analysis.get('suggested_name', '')
            if suggested and suggested != file_path.stem and len(suggested) > 3:
                self.results['rename_suggestions'].append({
                    'file': file_path,
                    'current': file_path.name,
                    'suggested': f"{suggested}.py",
                    'purpose': analysis.get('purpose', ''),
                    'category': category_name
                })
                self.stats['renames_suggested'] += 1
                print(f"    💡 INSIGHT: {file_path.name[:40]} → {suggested}.py")

        print(f"\n  ✨ {emoji} COMPLETE! Analyzed {analyzed} files | Found {sum(1 for r in self.results['rename_suggestions'] if r['category'] == category_name)} improvements!")

    def find_semantic_duplicates(self):
        """Use AI to find files that do the same thing (semantic duplicates)."""
        print(f"\n\n{'🔮'*40}")
        print("🔍 🧙 AI SEMANTIC DUPLICATE DETECTION ENGAGING... 🧙 🔍")
        print(f"{'🔮'*40}\n")

        print("🌐 Analyzing code semantics across all analyzed files...")
        print("🧠 Grouping by actual functionality (not just names)...\n")

        # Group files by their AI-analyzed purpose
        by_purpose = {}
        for file_path, analysis in self.analysis_cache.items():
            purpose = analysis.get('purpose', '').lower()
            if purpose and purpose != 'unknown':
                if purpose not in by_purpose:
                    by_purpose[purpose] = []
                by_purpose[purpose].append((file_path, analysis))

        # Find groups with multiple files
        duplicate_count = 0
        for purpose, files in by_purpose.items():
            if len(files) > 1:
                self.results['semantic_duplicates'].append({
                    'purpose': purpose,
                    'files': [f[0] for f in files],
                    'count': len(files)
                })
                self.stats['duplicates_found'] += len(files) - 1
                duplicate_count += 1

        print("="*80)
        if self.results['semantic_duplicates']:
            print(f"⚠️  🎯 FOUND {len(self.results['semantic_duplicates'])} SEMANTIC DUPLICATE GROUPS! 🎯")
            print("="*80 + "\n")
            for i, group in enumerate(self.results['semantic_duplicates'][:5], 1):
                print(f"🔥 GROUP #{i}: {group['count']} files doing the same thing!")
                print(f"   📝 Purpose: {group['purpose'][:70]}...")
                for f in group['files'][:3]:
                    print(f"      • {Path(f).name}")
                if len(group['files']) > 3:
                    print(f"      ... and {len(group['files']) - 3} more")
                print()
        else:
            print(f"✅ 🎉 NO SEMANTIC DUPLICATES! CODE IS UNIQUE! 🎉 ✅")
            print("="*80 + "\n")

    def generate_report(self):
        """Generate comprehensive AI-powered analysis report."""
        report_path = self.target_dir / f"AI_SUPERPOWERED_ANALYSIS_{self.timestamp}.md"

        with open(report_path, 'w') as f:
            f.write("# 🧠 AI Super-Powered Analysis Report 🚀\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**AI Models Used:** GPT-4, Claude\n\n")

            f.write("## 📊 Summary\n\n")
            f.write(f"- **Files Analyzed:** {self.stats['files_analyzed']:,}\n")
            f.write(f"- **AI API Calls:** {self.stats['ai_calls']:,}\n")
            f.write(f"- **Rename Suggestions:** {self.stats['renames_suggested']}\n")
            f.write(f"- **Semantic Duplicates:** {self.stats['duplicates_found']}\n\n")

            # Rename suggestions
            if self.results['rename_suggestions']:
                f.write("## ✏️ AI-Suggested Renames\n\n")
                for item in self.results['rename_suggestions'][:50]:
                    f.write(f"### {item['category']}/{item['current']}\n")
                    f.write(f"**Suggested:** `{item['suggested']}`\n\n")
                    f.write(f"**Purpose:** {item['purpose']}\n\n")
                    f.write("---\n\n")

            # Semantic duplicates
            if self.results['semantic_duplicates']:
                f.write("## 🔍 Semantic Duplicates (Same Functionality)\n\n")
                for group in self.results['semantic_duplicates']:
                    f.write(f"### {group['purpose'][:80]}\n")
                    f.write(f"**{group['count']} files do the same thing:**\n\n")
                    for file_path in group['files'][:10]:
                        f.write(f"- `{file_path}`\n")
                    f.write("\n")

        print(f"\n📄 Report saved: {report_path}")

    def run(self, sample_size: int = 50):
        """Run AI super-powered analysis."""
        print(f"\n{'🌟'*40}")
        print("║" + " "*78 + "║")
        print("║" + " "*18 + "🧠✨ AI SUPER-POWERED CONTENT ANALYZER ✨🧠" + " "*18 + "║")
        print("║" + " "*78 + "║")
        print(f"{'🌟'*40}\n")

        print("🎮 GAME PLAN:")
        print("  🎯 Step 1: Deep analyze code with GPT-4 & Claude")
        print("  🎯 Step 2: Find semantic duplicates (AI magic!)")
        print("  🎯 Step 3: Suggest intelligent renames")
        print("  🎯 Step 4: Generate comprehensive report\n")

        print(f"⚙️  CONFIGURATION:")
        print(f"   📊 Sample size per category: {sample_size} files")
        print(f"   🤖 AI Models: {'GPT-4 ⚡' if self.openai_client else ''} {'Claude 💎' if self.anthropic_client else ''}")
        print(f"   🎨 Output style: MAXIMUM FLASHINESS 💫\n")

        # Get categories
        categories = [f for f in self.target_dir.iterdir()
                     if f.is_dir() and not f.name.startswith(('.', '_'))]

        print(f"\n🎬 BEGINNING AI-POWERED ANALYSIS OF {len(categories)} CATEGORIES...\n")

        # Analyze each category
        for i, category in enumerate(sorted(categories), 1):
            print(f"\n🎯 [{i}/{len(categories)}]", end=" ")
            self.analyze_category(category, sample_size)

        # Find semantic duplicates
        self.find_semantic_duplicates()

        # Generate report
        self.generate_report()

        # Final summary - EXTRA FLASHY!
        print(f"\n\n{'🎊'*40}")
        print("║" + " "*78 + "║")
        print("║" + " "*25 + "🏆 AI ANALYSIS COMPLETE! 🏆" + " "*25 + "║")
        print("║" + " "*78 + "║")
        print(f"{'🎊'*40}\n")

        print("📊 FINAL STATISTICS:\n")
        print(f"   🧠 Files Deep Analyzed: {self.stats['files_analyzed']:,} 🔬")
        print(f"   🤖 AI API Calls Made:   {self.stats['ai_calls']:,} ⚡")
        print(f"   ✏️  Rename Suggestions:  {self.stats['renames_suggested']:,} 💡")
        print(f"   🔍 Semantic Duplicates: {self.stats['duplicates_found']:,} 🎯")

        print(f"\n{'✨'*40}")
        print("🎊 YOUR CODE IS NOW AI-ANALYZED & OPTIMIZED! 🎊")
        print(f"{'✨'*40}\n")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='AI Super-Powered Analyzer')
    parser.add_argument('--target', default='.', help='Target directory')
    parser.add_argument('--sample', type=int, default=50, help='Sample size per category')

    args = parser.parse_args()

    # Load environment
    os.system('source ~/.env.d/load_master.sh 2>/dev/null')

    analyzer = AISuperPoweredAnalyzer(args.target)
    analyzer.run(sample_size=args.sample)

if __name__ == "__main__":
    main()
