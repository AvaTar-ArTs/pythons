#!/usr/bin/env python3
"""
🧠 CONTENT-AWARE INTELLIGENT ORGANIZER 🧠
==========================================
Organizes files based on ACTUAL CONTENT and PURPOSE
using AI to understand what each file is about

- Reads file content
- AI determines purpose/category
- Groups by meaning, not just extension
- Smart folder naming
"""

import os
import sys
import asyncio
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
from ULTRA_DEEP_INTELLIGENCE_ORCHESTRATOR import (
    C, E, APIKeyManager, MultiLLMAnalyzer
)


class ContentAwareOrganizer:
    """AI-powered content-aware organization"""

    def __init__(self, dry_run: bool = True):
        self.docs_path = Path("/Users/steven/Documents")
        self.dry_run = dry_run
        self.api_manager = APIKeyManager()
        self.llm_analyzer = MultiLLMAnalyzer(self.api_manager.available_apis['llm'])

        # Content-based categories
        self.content_categories = defaultdict(list)
        self.move_plan = []

        self.stats = {
            'files_analyzed': 0,
            'files_organized': 0,
            'categories_created': 0
        }

    def print_header(self, text: str, emoji: str = E.SPARKLES):
        print(f"\n{C.BOLD}{C.MAGENTA}{'='*80}")
        print(f"{emoji} {text} {emoji}")
        print(f"{'='*80}{C.END}\n")

    async def analyze_file_content(self, file_path: Path) -> dict:
        """Use AI to understand file content"""
        try:
            # Only analyze text-based files
            if file_path.suffix not in ['.md', '.txt', '.py', '.js', '.html', '.json', '.csv']:
                return {'category': f'{file_path.suffix[1:]}_files', 'confidence': 0.5}

            # Skip very large files
            if file_path.stat().st_size > 500000:
                return {'category': f'large_{file_path.suffix[1:]}_files', 'confidence': 0.5}

            # Read content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(3000)  # First 3000 chars

            if len(content) < 50:
                return {'category': 'small_files', 'confidence': 0.3}

            # AI analysis
            prompt = f"""Analyze this file and categorize it. Respond with JSON:
{{
    "category": "choose ONE: business, technical, creative, personal, reference, tutorial, code, data, design, archive",
    "subcategory": "specific topic",
    "confidence": 0.0-1.0
}}

Filename: {file_path.name}
Content preview:
{content[:1000]}
"""

            # Use one LLM for speed
            if 'OpenAI' in self.api_manager.available_apis['llm']:
                result = await self.llm_analyzer.analyze_with_openai(content, prompt)
                if isinstance(result, dict) and 'category' in result:
                    return result

            # Fallback: simple keyword matching
            content_lower = content.lower()
            if any(word in content_lower for word in ['api', 'code', 'function', 'class']):
                return {'category': 'technical', 'confidence': 0.6}
            elif any(word in content_lower for word in ['business', 'price', 'service', 'client']):
                return {'category': 'business', 'confidence': 0.6}
            elif any(word in content_lower for word in ['story', 'creative', 'art', 'design']):
                return {'category': 'creative', 'confidence': 0.6}
            else:
                return {'category': 'reference', 'confidence': 0.4}

        except Exception as e:
            return {'category': 'uncategorized', 'confidence': 0.0}

    async def analyze_loose_files(self):
        """Analyze all loose files in Documents root"""
        self.print_header("ANALYZING FILE CONTENTS", E.BRAIN)

        loose_files = [f for f in self.docs_path.iterdir() if f.is_file()]

        print(f"{C.CYAN}🔍 Found {len(loose_files)} loose files{C.END}")
        print(f"{C.CYAN}🧠 Using AI to understand content...{C.END}\n")

        for i, file in enumerate(loose_files, 1):
            print(f"{C.CYAN}  [{i}/{len(loose_files)}] {file.name[:60]}...{C.END}")

            analysis = await self.analyze_file_content(file)
            category = analysis.get('category', 'uncategorized')

            self.content_categories[category].append({
                'file': file,
                'analysis': analysis
            })

            self.stats['files_analyzed'] += 1

            if i % 10 == 0:
                print(f"{C.GREEN}  ✅ Analyzed {i} files{C.END}")

        print(f"\n{C.GREEN}✅ Content analysis complete!{C.END}\n")

    def create_organization_plan(self):
        """Create smart organization plan"""
        self.print_header("CREATING ORGANIZATION PLAN", E.LIGHTBULB)

        # Map content categories to folder names
        folder_mapping = {
            'business': 'Business',
            'technical': 'Technical',
            'creative': 'Creative',
            'personal': 'Personal',
            'reference': 'Reference',
            'tutorial': 'Tutorials',
            'code': 'Code',
            'data': 'Data',
            'design': 'Design',
            'archive': 'Archives',
            'md_files': 'markD',
            'html_files': 'HTML',
            'py_files': 'pythons',
            'json_files': 'json',
            'csv_files': 'CsV',
            'txt_files': 'text',
            'sh_files': 'script'
        }

        for category, files in self.content_categories.items():
            target_folder = folder_mapping.get(category, category)

            print(f"{C.CYAN}📂 {target_folder}: {len(files)} files{C.END}")

            for file_info in files:
                self.move_plan.append({
                    'file': file_info['file'],
                    'target_folder': target_folder,
                    'confidence': file_info['analysis'].get('confidence', 0.5)
                })

        print()

    def execute_plan(self):
        """Execute the organization plan"""
        self.print_header("ORGANIZING FILES", E.FOLDER)

        if self.dry_run:
            print(f"{C.YELLOW}⚠️  DRY RUN - Showing moves:{C.END}\n")

        for item in self.move_plan:
            file = item['file']
            target_folder = item['target_folder']
            confidence = item['confidence']

            target_path = self.docs_path / target_folder

            # Create folder if needed
            if not target_path.exists():
                if not self.dry_run:
                    target_path.mkdir(exist_ok=True)
                self.stats['categories_created'] += 1

            dest = target_path / file.name
            conf_emoji = "🎯" if confidence > 0.7 else "📌" if confidence > 0.5 else "❓"

            print(f"{C.CYAN}  {conf_emoji} {file.name[:50]:.<50} → {target_folder}/{C.END}")

            if not self.dry_run:
                try:
                    # If file exists, add number
                    if dest.exists():
                        base = dest.stem
                        ext = dest.suffix
                        counter = 1
                        while dest.exists():
                            dest = target_path / f"{base}_{counter}{ext}"
                            counter += 1

                    shutil.move(str(file), str(dest))
                    self.stats['files_organized'] += 1
                except Exception as e:
                    print(f"{C.RED}     ❌ Error: {e}{C.END}")

        print(f"\n{C.GREEN}✅ Organized {self.stats['files_organized']} files{C.END}\n")

    async def run(self):
        """Run content-aware organization"""
        print(f"{C.BOLD}{C.MAGENTA}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║           🧠 CONTENT-AWARE INTELLIGENT ORGANIZER 🧠                          ║")
        print("║                                                                               ║")
        print("║        AI Reads Content to Understand Purpose, Not Just File Type             ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{C.END}\n")

        # Phase 1: Analyze content
        await self.analyze_loose_files()

        # Phase 2: Create plan
        self.create_organization_plan()

        # Phase 3: Execute
        self.execute_plan()

        # Summary
        self.print_header("COMPLETE!", E.ROCKET)
        print(f"{C.GREEN}✅ Content-aware organization summary:{C.END}")
        print(f"  🧠 Files analyzed: {C.BOLD}{self.stats['files_analyzed']}{C.END}")
        print(f"  📁 Files organized: {C.BOLD}{self.stats['files_organized']}{C.END}")
        print(f"  🗂️  Categories created: {C.BOLD}{self.stats['categories_created']}{C.END}\n")

        if self.dry_run:
            print(f"{C.YELLOW}⚠️  To execute, run:{C.END}")
            print(f"{C.CYAN}   python CONTENT_AWARE_ORGANIZER.py --execute{C.END}\n")


async def main():
    import sys
    execute = '--execute' in sys.argv

    organizer = ContentAwareOrganizer(dry_run=not execute)
    await organizer.run()

    print(f"{C.GREEN}{C.BOLD}{E.SPARKLES} DONE! {E.SPARKLES}{C.END}\n")


if __name__ == "__main__":
    asyncio.run(main())
