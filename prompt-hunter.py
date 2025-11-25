#!/usr/bin/env python3
"""
🔎 PROMPT HUNTER ULTIMATE
=========================

Hunts for valuable prompts across your entire system:
- Sora prompts (video generation)
- Music prompts (especially Nocturnemelodies)
- AI generation prompts (DALL-E, Midjourney, Leonardo)
- Make.com/n8n workflow prompts
- Any prompt templates and instructions

Searches in: HTML, MD, PDF, CSV, TXT, JSON, Python, JS
Locations: ~/pythons, ~/Music, ~/sites, ~/workspace, ~/Documents
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import PyPDF2


@dataclass
class PromptDiscovery:
    """A discovered prompt"""
    filepath: str
    prompt_type: str  # 'sora', 'music', 'image', 'text', 'workflow'
    content: str
    context: str
    related_to: List[str] = field(default_factory=list)
    quality_score: int = 0  # 1-10


@dataclass
class NocturneMelodiesContent:
    """Content related to Nocturnemelodies"""
    filepath: str
    content_type: str  # 'prompt', 'lyrics', 'description', 'metadata'
    content: str
    tags: List[str] = field(default_factory=list)


class PromptHunterUltimate:
    """
    Advanced prompt discovery system
    """
    
    def __init__(self):
        self.prompts: List[PromptDiscovery] = []
        self.nocturne_content: List[NocturneMelodiesContent] = []
        self.sites_found: Dict[str, Dict] = {}
        
        # Prompt patterns
        self.prompt_indicators = {
            'sora': ['sora', 'video prompt', 'video generation', 'openai video'],
            'music': ['music prompt', 'suno', 'song generation', 'lyrics', 'nocturne'],
            'image': ['dall-e', 'dalle', 'midjourney', 'leonardo', 'stable diffusion', 'image prompt'],
            'text': ['gpt prompt', 'chat prompt', 'system prompt', 'instruction'],
            'workflow': ['make.com', 'n8n', 'workflow', 'automation prompt']
        }
    
    def hunt_all(self, base_paths: List[str]) -> Dict[str, Any]:
        """
        Hunt for prompts across all specified paths
        """
        print("🔎 PROMPT HUNTER ULTIMATE - Starting Deep Scan")
        print("="*70)
        
        results = {
            'prompts_found': 0,
            'nocturne_content': 0,
            'sites_analyzed': 0,
            'files_scanned': 0
        }
        
        for base_path in base_paths:
            if not Path(base_path).exists():
                print(f"⚠️  Path not found: {base_path}")
                continue
            
            print(f"\n📂 Scanning: {base_path}")
            self._scan_directory(base_path, results)
        
        return results
    
    def _scan_directory(self, directory: str, results: Dict):
        """Scan a directory for prompts"""
        target_extensions = {'.html', '.md', '.pdf', '.csv', '.txt', '.json', '.py', '.js', '.jsx', '.tsx'}
        
        for root, dirs, files in os.walk(directory):
            # Skip common ignore directories
            dirs[:] = [d for d in dirs if d not in {
                'node_modules', '.git', '__pycache__', 'venv', '.venv', 
                'dist', 'build', '.next', 'Library', 'Applications'
            }]
            
            for file in files:
                filepath = Path(root) / file
                
                if filepath.suffix.lower() in target_extensions:
                    results['files_scanned'] += 1
                    self._analyze_file(filepath)
    
    def _analyze_file(self, filepath: Path):
        """Analyze a single file for prompts"""
        try:
            # Read file based on type
            if filepath.suffix == '.pdf':
                content = self._read_pdf(filepath)
            else:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            
            if not content:
                return
            
            # Check for Nocturnemelodies content
            if 'nocturne' in content.lower():
                self._extract_nocturne_content(filepath, content)
            
            # Hunt for prompts
            self._hunt_prompts(filepath, content)
            
            # Check if it's a website/project
            if filepath.name in {'index.html', 'package.json', 'README.md'}:
                self._analyze_site(filepath, content)
                
        except Exception as e:
            # Silent fail for unreadable files
            pass
    
    def _read_pdf(self, filepath: Path) -> str:
        """Read PDF file"""
        try:
            with open(filepath, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)
                text = ''
                for page in pdf.pages[:10]:  # Limit to first 10 pages
                    text += page.extract_text()
                return text
        except:
            return ''
    
    def _extract_nocturne_content(self, filepath: Path, content: str):
        """Extract Nocturnemelodies-related content"""
        # Find context around "nocturne"
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if 'nocturne' in line.lower():
                # Get context (5 lines before and after)
                start = max(0, i - 5)
                end = min(len(lines), i + 6)
                context = '\n'.join(lines[start:end])
                
                # Determine content type
                content_type = 'prompt'
                if 'lyric' in context.lower():
                    content_type = 'lyrics'
                elif 'description' in context.lower() or 'about' in context.lower():
                    content_type = 'description'
                elif 'metadata' in context.lower() or 'tag' in context.lower():
                    content_type = 'metadata'
                
                # Extract tags
                tags = self._extract_tags(context)
                
                nocturne_item = NocturneMelodiesContent(
                    filepath=str(filepath),
                    content_type=content_type,
                    content=context,
                    tags=tags
                )
                
                self.nocturne_content.append(nocturne_item)
                print(f"   🎵 Found Nocturne content in: {filepath.name}")
    
    def _hunt_prompts(self, filepath: Path, content: str):
        """Hunt for valuable prompts"""
        content_lower = content.lower()
        
        # Check each prompt type
        for prompt_type, indicators in self.prompt_indicators.items():
            if any(indicator in content_lower for indicator in indicators):
                # Extract the actual prompt
                prompts = self._extract_prompts(content, prompt_type)
                
                for prompt_text in prompts:
                    prompt = PromptDiscovery(
                        filepath=str(filepath),
                        prompt_type=prompt_type,
                        content=prompt_text,
                        context=self._get_context(content, prompt_text),
                        related_to=self._find_related_terms(prompt_text),
                        quality_score=self._score_prompt(prompt_text)
                    )
                    
                    self.prompts.append(prompt)
                    
                    if prompt.quality_score >= 7:  # High-quality prompt
                        print(f"   ✨ Found {prompt_type} prompt in: {filepath.name}")
    
    def _extract_prompts(self, content: str, prompt_type: str) -> List[str]:
        """Extract actual prompt text"""
        prompts = []
        
        # Common prompt patterns
        patterns = [
            r'prompt[:\s]+["\'](.+?)["\']',  # prompt: "text"
            r'prompt[:\s]+(.+?)(?:\n|$)',     # prompt: text
            r'system[:\s]+["\'](.+?)["\']',   # system: "text"
            r'instruction[:\s]+(.+?)(?:\n|$)', # instruction: text
            r'```(.+?)```',                    # Code blocks with prompts
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                prompt_text = match.group(1).strip()
                if len(prompt_text) > 20 and len(prompt_text) < 2000:  # Reasonable length
                    prompts.append(prompt_text)
        
        # Special handling for JSON prompts
        if '{' in content and '"prompt"' in content.lower():
            try:
                json_data = json.loads(content)
                if isinstance(json_data, dict):
                    prompts.extend(self._extract_from_json(json_data))
                elif isinstance(json_data, list):
                    for item in json_data:
                        if isinstance(item, dict):
                            prompts.extend(self._extract_from_json(item))
            except:
                pass
        
        return prompts[:10]  # Limit to top 10 per file
    
    def _extract_from_json(self, data: Dict) -> List[str]:
        """Extract prompts from JSON data"""
        prompts = []
        
        for key, value in data.items():
            if 'prompt' in key.lower() and isinstance(value, str):
                prompts.append(value)
            elif isinstance(value, dict):
                prompts.extend(self._extract_from_json(value))
        
        return prompts
    
    def _get_context(self, content: str, prompt_text: str) -> str:
        """Get context around a prompt"""
        # Find where prompt appears
        idx = content.find(prompt_text)
        if idx == -1:
            return ""
        
        # Get 200 chars before and after
        start = max(0, idx - 200)
        end = min(len(content), idx + len(prompt_text) + 200)
        
        return content[start:end]
    
    def _find_related_terms(self, text: str) -> List[str]:
        """Find related terms in prompt"""
        related = []
        
        terms = {
            'nocturne': ['nocturne', 'night music', 'evening'],
            'sora': ['sora', 'video', 'openai'],
            'suno': ['suno', 'music', 'song'],
            'leonardo': ['leonardo', 'image', 'art'],
            'make.com': ['make', 'automation', 'workflow']
        }
        
        text_lower = text.lower()
        for key, keywords in terms.items():
            if any(kw in text_lower for kw in keywords):
                related.append(key)
        
        return related
    
    def _score_prompt(self, prompt_text: str) -> int:
        """Score prompt quality (1-10)"""
        score = 5  # Base score
        
        # Length bonus
        if 100 < len(prompt_text) < 1000:
            score += 2
        
        # Detail indicators
        detail_words = ['detailed', 'specific', 'professional', 'high quality', 'cinematic']
        score += sum(1 for word in detail_words if word in prompt_text.lower())
        
        # Structure bonus
        if any(marker in prompt_text for marker in ['1.', '2.', '-', '*']):
            score += 1
        
        return min(10, score)
    
    def _extract_tags(self, text: str) -> List[str]:
        """Extract tags from text"""
        tags = []
        
        # Common tag patterns
        tag_patterns = [
            r'#(\w+)',           # Hashtags
            r'tag[s]?:\s*(.+)',  # tags: ...
            r'\[(.+?)\]',        # [tag]
        ]
        
        for pattern in tag_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            tags.extend(matches)
        
        return list(set(tags))[:10]  # Limit to 10 unique tags
    
    def _analyze_site(self, filepath: Path, content: str):
        """Analyze a website/project"""
        site_info = {
            'path': str(filepath.parent),
            'name': filepath.parent.name,
            'type': 'unknown',
            'technologies': [],
            'has_prompts': False
        }
        
        # Determine type
        if filepath.name == 'package.json':
            try:
                data = json.loads(content)
                site_info['type'] = 'Node/React project'
                site_info['technologies'] = list(data.get('dependencies', {}).keys())[:10]
            except:
                pass
        elif filepath.name == 'index.html':
            site_info['type'] = 'Static website'
            # Check for frameworks
            if 'react' in content.lower():
                site_info['technologies'].append('React')
            if 'vue' in content.lower():
                site_info['technologies'].append('Vue')
        
        # Check if site contains prompts
        if any(ind in content.lower() for indicators in self.prompt_indicators.values() for ind in indicators):
            site_info['has_prompts'] = True
        
        self.sites_found[str(filepath.parent)] = site_info
    
    def generate_report(self) -> str:
        """Generate comprehensive report"""
        report = []
        report.append("="*70)
        report.append("🔎 PROMPT HUNTER ULTIMATE - COMPLETE REPORT")
        report.append("="*70)
        report.append("")
        
        # Summary
        report.append("📊 SUMMARY")
        report.append("-"*70)
        report.append(f"Total Prompts Found: {len(self.prompts)}")
        report.append(f"Nocturnemelodies Content: {len(self.nocturne_content)}")
        report.append(f"Sites with Prompts: {sum(1 for s in self.sites_found.values() if s['has_prompts'])}")
        report.append("")
        
        # Nocturnemelodies Content
        if self.nocturne_content:
            report.append("\n🎵 NOCTURNEMELODIES CONTENT")
            report.append("-"*70)
            
            for item in self.nocturne_content[:20]:  # Top 20
                report.append(f"\nFile: {Path(item.filepath).name}")
                report.append(f"Type: {item.content_type}")
                if item.tags:
                    report.append(f"Tags: {', '.join(item.tags)}")
                report.append(f"Content Preview:\n{item.content[:200]}...")
                report.append("")
        
        # High-Quality Prompts
        high_quality = [p for p in self.prompts if p.quality_score >= 7]
        if high_quality:
            report.append("\n✨ HIGH-QUALITY PROMPTS")
            report.append("-"*70)
            
            for prompt in high_quality[:30]:  # Top 30
                report.append(f"\nType: {prompt.prompt_type.upper()}")
                report.append(f"File: {Path(prompt.filepath).name}")
                report.append(f"Quality Score: {prompt.quality_score}/10")
                if prompt.related_to:
                    report.append(f"Related to: {', '.join(prompt.related_to)}")
                report.append(f"Prompt:\n{prompt.content[:300]}...")
                report.append("")
        
        # Prompts by Type
        report.append("\n📂 PROMPTS BY TYPE")
        report.append("-"*70)
        
        by_type = defaultdict(list)
        for prompt in self.prompts:
            by_type[prompt.prompt_type].append(prompt)
        
        for prompt_type, prompts in sorted(by_type.items(), key=lambda x: len(x[1]), reverse=True):
            report.append(f"\n{prompt_type.upper()}: {len(prompts)} prompts")
            for p in prompts[:5]:  # Top 5 per type
                report.append(f"  • {Path(p.filepath).name} (score: {p.quality_score}/10)")
        
        report.append("")
        
        # Sites with Prompts
        sites_with_prompts = {k: v for k, v in self.sites_found.items() if v['has_prompts']}
        if sites_with_prompts:
            report.append("\n🌐 SITES WITH PROMPTS")
            report.append("-"*70)
            
            for site_path, info in list(sites_with_prompts.items())[:20]:
                report.append(f"\n{info['name']}")
                report.append(f"  Path: {site_path}")
                report.append(f"  Type: {info['type']}")
                if info['technologies']:
                    report.append(f"  Tech: {', '.join(info['technologies'][:5])}")
        
        return '\n'.join(report)
    
    def export_prompts_json(self, filepath: str = "PROMPTS_DISCOVERED.json"):
        """Export all prompts to JSON"""
        data = {
            'summary': {
                'total_prompts': len(self.prompts),
                'nocturne_content': len(self.nocturne_content),
                'sites_found': len(self.sites_found)
            },
            'nocturnemelodies': [
                {
                    'file': item.filepath,
                    'type': item.content_type,
                    'content': item.content,
                    'tags': item.tags
                }
                for item in self.nocturne_content
            ],
            'prompts': [
                {
                    'file': p.filepath,
                    'type': p.prompt_type,
                    'content': p.content,
                    'quality_score': p.quality_score,
                    'related_to': p.related_to
                }
                for p in self.prompts
            ],
            'sites': self.sites_found
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n✅ Exported prompts to: {filepath}")


def main():
    """Run the prompt hunter"""
    print("🔎 PROMPT HUNTER ULTIMATE")
    print("="*70)
    print()
    
    hunter = PromptHunterUltimate()
    
    # Define search paths
    search_paths = [
        "/Users/steven/pythons",
        "/Users/steven/Music",
        "/Users/steven/workspace",
        "/Users/steven/ai-sites",
        "/Users/steven/Documents",
        "/Users/steven/Downloads",
        "/Users/steven/GitHub"
    ]
    
    print("📂 Search Paths:")
    for path in search_paths:
        if Path(path).exists():
            print(f"   ✅ {path}")
        else:
            print(f"   ⚠️  {path} (not found)")
    
    print("\n" + "="*70)
    print("🔍 Starting Deep Scan...")
    print("="*70 + "\n")
    
    # Hunt for prompts
    results = hunter.hunt_all(search_paths)
    
    # Generate report
    print("\n" + "="*70)
    print("📊 Generating Report...")
    print("="*70)
    
    report = hunter.generate_report()
    print(report)
    
    # Export to JSON
    hunter.export_prompts_json()
    
    # Save report
    with open("PROMPT_HUNTER_REPORT.md", 'w') as f:
        f.write(report)
    
    print("\n✅ Report saved: PROMPT_HUNTER_REPORT.md")
    print(f"\n📊 FINAL STATS:")
    print(f"   Files Scanned: {results['files_scanned']:,}")
    print(f"   Prompts Found: {len(hunter.prompts)}")
    print(f"   Nocturne Content: {len(hunter.nocturne_content)}")
    print(f"   Sites Analyzed: {len(hunter.sites_found)}")


if __name__ == "__main__":
    main()

