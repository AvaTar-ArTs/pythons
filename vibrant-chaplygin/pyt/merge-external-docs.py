#!/usr/bin/env python3
"""
Merge External Volume Documentation into Home Directory
Intelligently organize content from /Volumes into ~/
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class ExternalDocsMerger:
    """Merge external volume docs into home directory"""
    
    def __init__(self):
        self.home = Path.home()
        self.volumes = {
            '2T-Xx': Path('/Volumes/2T-Xx'),
            'DeVonDaTa': Path('/Volumes/DeVonDaTa')
        }
        self.merge_plan = {
            'api_docs': self.home / 'Documents' / 'api-documentation',
            'ai_projects': self.home / 'workspace',
            'scripts': self.home / 'Documents' / 'pythons' / '_library',
            'seo_docs': self.home / 'Documents' / 'seo-strategy',
        }
        
    def analyze_external_content(self):
        """Analyze what's on external volumes"""
        print("?? Analyzing External Volumes...")
        print("=" * 80)
        
        analysis = {}
        
        for vol_name, vol_path in self.volumes.items():
            if not vol_path.exists():
                print(f"??  {vol_name} not mounted")
                continue
                
            print(f"\n?? {vol_name} ({vol_path})")
            
            # Key files to merge
            key_files = {
                'API Docs': list(vol_path.glob('*API*.md')),
                'Ecosystem Docs': list(vol_path.glob('*ECOSYSTEM*.md')),
                'Quick References': list(vol_path.glob('*QUICK*.md')),
                'Guides': list(vol_path.glob('*GUIDE*.md')),
                'Python Scripts': list(vol_path.glob('*.py')),
            }
            
            for category, files in key_files.items():
                if files:
                    print(f"  {category}: {len(files)} files")
                    analysis[f"{vol_name}_{category}"] = files
        
        return analysis
    
    def create_merge_plan(self):
        """Create intelligent merge plan"""
        plan = {
            'API Documentation': {
                'source_patterns': ['*API*.md', '*api*.md'],
                'destination': self.home / 'Documents' / 'api-documentation',
                'action': 'merge'
            },
            'AI Ecosystem Docs': {
                'source_patterns': ['*ECOSYSTEM*.md', '*AI_*.md'],
                'destination': self.home / 'Documents' / 'ai-ecosystem',
                'action': 'merge'
            },
            'Quick References': {
                'source_patterns': ['*QUICK*.md', '*REFERENCE*.md'],
                'destination': self.home / '.config' / 'quick-refs',
                'action': 'link'  # Symlink for quick access
            },
            'Python Library': {
                'source_patterns': ['*.py'],
                'destination': self.home / 'Documents' / 'pythons' / '_library',
                'action': 'selective'  # Only unique/useful ones
            },
            'SEO Strategy': {
                'source_patterns': ['*SEO*.md', '*seo*.md'],
                'destination': self.home / 'Documents' / 'seo-strategy',
                'action': 'merge'
            },
            'Project Docs': {
                'source_patterns': ['README.md', 'GUIDE.md'],
                'destination': self.home / 'Documents' / 'project-docs',
                'action': 'catalog'  # Create index
            }
        }
        
        return plan
    
    def merge_api_docs(self):
        """Merge API documentation"""
        print("\n?? Merging API Documentation...")
        dest = self.home / 'Documents' / 'api-documentation'
        dest.mkdir(parents=True, exist_ok=True)
        
        files_copied = []
        
        # Find all API docs
        for vol_name, vol_path in self.volumes.items():
            if not vol_path.exists():
                continue
                
            for pattern in ['*API*.md', '*api*.md']:
                for file in vol_path.glob(pattern):
                    new_name = f"{vol_name}_{file.name}"
                    dest_file = dest / new_name
                    
                    if not dest_file.exists():
                        shutil.copy2(file, dest_file)
                        files_copied.append(new_name)
                        print(f"  ? {file.name} ? {new_name}")
        
        # Create master index
        self.create_api_index(dest, files_copied)
        
        return len(files_copied)
    
    def create_api_index(self, dest_dir, files):
        """Create master API documentation index"""
        index_path = dest_dir / 'API_MASTER_INDEX.md'
        
        content = f"""# ?? API Master Documentation Index

> **Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
> **Total API Docs**: {len(files)}

## ?? Available Documentation

"""
        for filename in sorted(files):
            title = filename.replace('_', ' ').replace('.md', '').title()
            content += f"- [{title}]({filename})\n"
        
        content += """

## ?? Quick Links

### By Category

**AI/LLM Services**
- OpenAI (GPT-4, DALL-E, Whisper)
- Anthropic (Claude)
- Groq, DeepSeek, Gemini

**Image/Video Generation**
- Leonardo AI
- Stability AI
- Runway ML

**Audio/Music**
- Suno, ElevenLabs
- AssemblyAI, Deepgram

**Automation**
- LangChain, CrewAI
- Pinecone, Qdrant

**SEO/Analytics**
- SerpAPI, NewsAPI
- Google Analytics

## ?? Usage

All APIs are pre-configured in `~/.env.d/`

```bash
# Load specific category
source ~/.env.d/llm-apis.env

# Or load all
for f in ~/.env.d/*.env; do source "$f"; done
```
"""
        
        with open(index_path, 'w') as f:
            f.write(content)
        
        print(f"\n  ?? Created: {index_path}")
    
    def create_quick_links(self):
        """Create quick access links in ~/.config"""
        print("\n?? Creating Quick Reference Links...")
        
        config_dir = self.home / '.config' / 'quick-refs'
        config_dir.mkdir(parents=True, exist_ok=True)
        
        links_created = 0
        
        # Find and link quick reference docs
        for vol_name, vol_path in self.volumes.items():
            if not vol_path.exists():
                continue
                
            for pattern in ['*QUICK*.md', '*REFERENCE*.md']:
                for file in vol_path.glob(pattern):
                    link_name = config_dir / f"{vol_name}_{file.name}"
                    
                    if not link_name.exists():
                        link_name.symlink_to(file)
                        links_created += 1
                        print(f"  ?? {file.name}")
        
        return links_created
    
    def catalog_projects(self):
        """Create catalog of projects on external drives"""
        print("\n?? Cataloging Projects...")
        
        catalog_path = self.home / 'Documents' / 'EXTERNAL_PROJECTS_CATALOG.md'
        
        content = f"""# ?? External Projects Catalog

> **Last Scanned**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## ?? Projects by Volume

"""
        
        # Scan ai-sites on 2T-Xx
        ai_sites = Path('/Volumes/2T-Xx/ai-sites')
        if ai_sites.exists():
            content += "\n### ?? AI Sites (2T-Xx)\n\n"
            projects = [d for d in ai_sites.iterdir() if d.is_dir() and not d.name.startswith('.')]
            
            for proj in sorted(projects)[:30]:  # First 30
                readme = proj / 'README.md'
                desc = "No description"
                
                if readme.exists():
                    try:
                        with open(readme) as f:
                            lines = f.readlines()
                            # Get first non-empty line
                            for line in lines[:10]:
                                if line.strip() and not line.startswith('#'):
                                    desc = line.strip()[:100]
                                    break
                    except:
                        pass
                
                content += f"- **{proj.name}**\n"
                content += f"  - Path: `{proj}`\n"
                content += f"  - {desc}\n\n"
        
        content += """

## ?? Key Projects to Integrate

### High Priority
1. **automation** - Core automation scripts
2. **content-management** - Content workflows
3. **ai-content-studio** - AI content generation
4. **AvaTarArTs** - Main art portfolio system

### Medium Priority
5. **seo-optimized-content** - SEO strategies
6. **passive-income-empire** - Business automation
7. **quantumforgelabs** - Personal brand

## ?? Next Steps

1. Review each project's README
2. Decide which to move to `~/workspace`
3. Archive outdated projects
4. Update documentation links
"""
        
        with open(catalog_path, 'w') as f:
            f.write(content)
        
        print(f"  ?? Catalog created: {catalog_path}")
        
        return catalog_path
    
    def run(self):
        """Execute merge operation"""
        print("?? External Docs Merger")
        print("=" * 80)
        
        # Analyze
        analysis = self.analyze_external_content()
        
        # Merge API docs
        api_count = self.merge_api_docs()
        
        # Create quick links
        link_count = self.create_quick_links()
        
        # Catalog projects
        catalog = self.catalog_projects()
        
        print("\n" + "=" * 80)
        print("? Merge Complete!")
        print("=" * 80)
        print(f"\n?? Summary:")
        print(f"  ? API Docs merged: {api_count}")
        print(f"  ? Quick links created: {link_count}")
        print(f"  ? Project catalog: {catalog}")
        
        print(f"\n?? New Locations:")
        print(f"  ? API Docs: ~/Documents/api-documentation/")
        print(f"  ? Quick Refs: ~/.config/quick-refs/")
        print(f"  ? Catalog: ~/Documents/EXTERNAL_PROJECTS_CATALOG.md")

def main():
    merger = ExternalDocsMerger()
    merger.run()

if __name__ == "__main__":
    main()
