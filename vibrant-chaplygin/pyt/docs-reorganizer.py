#!/usr/bin/env python3
"""
Documentation Reorganizer
Create intelligent, narrative-driven documentation with better structure
"""

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class DocsReorganizer:
    """Reorganize documentation into coherent narrative structure"""
    
    def __init__(self):
        self.base_dir = Path("/Users/steven/Documents/pythons")
        self.index_file = self.base_dir / "scripts_ai_index.json"
        self.data = self.load_data()
        
    def load_data(self):
        """Load existing analysis data"""
        with open(self.index_file) as f:
            return json.load(f)
    
    def create_smart_categories(self):
        """Create intelligent category groupings"""
        categories = {
            '?? AI & Machine Learning': {
                'keywords': ['openai', 'claude', 'anthropic', 'gemini', 'ai-', 'gpt', 'llm', 'groq'],
                'scripts': []
            },
            '?? Instagram Automation': {
                'keywords': ['instagram'],
                'scripts': []
            },
            '?? Image Generation & Processing': {
                'keywords': ['leonardo', 'image-', 'stability', 'dalle', 'art-', 'vision'],
                'scripts': []
            },
            '?? Audio & Music': {
                'keywords': ['suno', 'audio', 'music', 'sound', 'elevenlabs', 'tts', 'speech', 'whisper', 'transcribe'],
                'scripts': []
            },
            '?? Video Processing': {
                'keywords': ['video', 'youtube', 'clip', 'ffmpeg', 'movie'],
                'scripts': []
            },
            '?? Data Analysis & Processing': {
                'keywords': ['analyze', 'csv', 'json', 'database', 'parse', 'extract'],
                'scripts': []
            },
            '??? File Management & Organization': {
                'keywords': ['organize', 'clean', 'rename', 'consolidate', 'flatten', 'sort'],
                'scripts': []
            },
            '?? Content Creation Pipelines': {
                'keywords': ['content-', 'pipeline', 'generator', 'creator', 'builder'],
                'scripts': []
            },
            '?? Automation & Workflows': {
                'keywords': ['automation', 'bot-', 'batch-', 'process-'],
                'scripts': []
            },
            '?? Social Media Tools': {
                'keywords': ['reddit', 'telegram', 'twitter', 'social'],
                'scripts': []
            },
            '?? Utilities & Helpers': {
                'keywords': ['util', 'helper', 'tool', 'check', 'validate', 'verify'],
                'scripts': []
            },
        }
        
        # Categorize scripts
        for script in self.data['scripts']:
            filename = script['filename'].lower()
            categorized = False
            
            for category, info in categories.items():
                if categorized:
                    break
                for keyword in info['keywords']:
                    if keyword in filename:
                        info['scripts'].append(script)
                        categorized = True
                        break
            
            # Uncategorized goes to utilities
            if not categorized:
                categories['?? Utilities & Helpers']['scripts'].append(script)
        
        return categories
    
    def generate_enhanced_docs(self):
        """Generate beautifully organized documentation"""
        categories = self.create_smart_categories()
        
        doc = f"""# ?? Python Automation Arsenal
## Comprehensive Documentation & Script Reference

> **Last Updated**: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}  
> **Total Scripts**: {len(self.data['scripts'])}  
> **Intelligent Categories**: {len([c for c in categories.values() if c['scripts']])}

---

## ?? Table of Contents

"""
        # Generate TOC
        for i, (category, info) in enumerate(categories.items(), 1):
            if info['scripts']:
                anchor = category.lower().replace(' ', '-').replace('&', 'and').replace('??', '').replace('??', '').replace('??', '').replace('??', '').replace('??', '').replace('??', '').replace('???', '').replace('??', '').replace('??', '').replace('??', '').replace('??', '').strip()
                doc += f"{i}. [{category}](#{anchor}) - {len(info['scripts'])} scripts\n"
        
        doc += "\n---\n\n"
        
        # Add overview statistics
        doc += self.generate_overview()
        
        # Add each category with narrative
        for category, info in categories.items():
            if info['scripts']:
                doc += self.generate_category_section(category, info['scripts'])
        
        # Add appendices
        doc += self.generate_appendices()
        
        return doc
    
    def generate_overview(self):
        """Generate engaging overview section"""
        total = len(self.data['scripts'])
        
        return f"""
## ?? Overview

Welcome to your **Python Automation Arsenal** - a comprehensive collection of {total}+ production-ready scripts designed for content creation, social media automation, AI integration, and digital workflow optimization.

### ?? What Makes This Collection Special

**?? AI-First Design**
- Integrated with 26+ AI services (OpenAI, Claude, Gemini, etc.)
- Intelligent content generation and analysis
- Multi-modal capabilities (text, image, audio, video)

**?? Production-Ready**
- Battle-tested in real-world workflows
- Comprehensive error handling
- Extensive API integrations

**?? Creative Automation**
- End-to-end content pipelines
- Social media management at scale
- Automated asset generation and processing

### ?? Quick Stats

| Metric | Count |
|--------|-------|
| Total Scripts | {total} |
| Instagram Tools | {len([s for s in self.data['scripts'] if 'instagram' in s['filename'].lower()])} |
| Leonardo AI Tools | {len([s for s in self.data['scripts'] if 'leonardo' in s['filename'].lower()])} |
| Audio/Music Tools | {len([s for s in self.data['scripts'] if any(x in s['filename'].lower() for x in ['audio', 'music', 'suno'])])} |
| AI/LLM Integration | {len([s for s in self.data['scripts'] if any(x in s['filename'].lower() for x in ['openai', 'claude', 'ai-', 'gpt'])])} |

---

"""
    
    def generate_category_section(self, category, scripts):
        """Generate narrative-driven category section"""
        section = f"\n## {category}\n\n"
        
        # Add category narrative
        narratives = {
            '?? AI & Machine Learning': "Harness the power of cutting-edge AI models for intelligent automation, content analysis, and creative generation. These tools integrate seamlessly with OpenAI, Claude, Gemini, and other leading AI platforms.",
            
            '?? Instagram Automation': "Complete Instagram management suite with 79+ specialized scripts. From strategic follower growth to content scheduling, analytics tracking, and engagement automation - everything you need to dominate Instagram.",
            
            '?? Image Generation & Processing': "Professional-grade image workflows powered by Leonardo AI, Stable Diffusion, and DALL-E. Generate, upscale, process, and organize visual content at scale.",
            
            '?? Audio & Music': "End-to-end audio production tools featuring Suno music generation, ElevenLabs voice synthesis, transcription services, and audio processing automation.",
            
            '?? Video Processing': "Comprehensive video automation including YouTube management, ffmpeg operations, clip editing, and automated video generation workflows.",
            
            '?? Data Analysis & Processing': "Powerful data manipulation and analysis tools. Parse, transform, analyze, and visualize data across multiple formats (CSV, JSON, databases).",
            
            '??? File Management & Organization': "Intelligent file organization, renaming, deduplication, and cleanup utilities. Keep your digital workspace pristine and organized.",
            
            '?? Content Creation Pipelines': "Complete end-to-end content generation workflows. Orchestrate multiple AI services, processing steps, and distribution channels.",
            
            '?? Automation & Workflows': "Batch processing, scheduled automation, and workflow orchestration tools. Set it and forget it automation for repetitive tasks.",
            
            '?? Social Media Tools': "Multi-platform social media automation beyond Instagram. Reddit scraping, Telegram bots, and cross-platform content distribution.",
            
            '?? Utilities & Helpers': "Essential utility scripts for validation, checking, testing, and general-purpose automation tasks.",
        }
        
        section += f"_{narratives.get(category, 'Specialized tools for specific automation needs.')}_\n\n"
        section += f"**Scripts in this category**: {len(scripts)}\n\n"
        
        # Group scripts by complexity
        by_complexity = defaultdict(list)
        for script in sorted(scripts, key=lambda x: x['filename']):
            complexity = script.get('complexity', 'Intermediate')
            by_complexity[complexity].append(script)
        
        # Show scripts by complexity
        for complexity in ['Beginner', 'Intermediate', 'Advanced', 'Expert']:
            if complexity in by_complexity:
                section += f"\n### {self.get_complexity_emoji(complexity)} {complexity} Level\n\n"
                for script in by_complexity[complexity]:
                    section += self.format_script_compact(script)
        
        section += "\n---\n"
        return section
    
    def get_complexity_emoji(self, complexity):
        """Get emoji for complexity level"""
        return {
            'Beginner': '??',
            'Intermediate': '??',
            'Advanced': '??',
            'Expert': '??'
        }.get(complexity, '?')
    
    def format_script_compact(self, script):
        """Format script in compact, scannable format"""
        entry = f"\n#### ?? {script.get('title', script['filename'])}\n\n"
        entry += f"**`{script['filename']}`**\n\n"
        
        if script.get('purpose'):
            entry += f"{script['purpose']}\n\n"
        
        # Compact feature list
        if script.get('key_features'):
            entry += "**Features**: " + " ? ".join(script['key_features'][:3]) + "\n\n"
        
        # Metadata
        meta = []
        if script.get('size_kb'):
            meta.append(f"{script['size_kb']:.1f} KB")
        if script.get('lines'):
            meta.append(f"{script['lines']} lines")
        if script.get('related_services'):
            meta.append(f"Uses: {', '.join(script['related_services'][:2])}")
        
        if meta:
            entry += f"_{' | '.join(meta)}_\n\n"
        
        return entry
    
    def generate_appendices(self):
        """Generate helpful appendices"""
        return """
---

## ?? Appendices

### A. Quick Start Guide

1. **Set up your environment**
   ```bash
   # Activate environment
   mamba activate sales-empire
   
   # Install dependencies
   pip install -r requirements-py.txt
   ```

2. **Configure API keys**
   - Keys are loaded from `~/.env.d/MASTER_CONSOLIDATED.env`
   - Contains 100+ API keys across 26+ services
   - No need to manage individual .env files

3. **Run a script**
   ```bash
   python instagram-analyze-stats.py
   python leonardo-api.py
   python openai-content-analyzer.py
   ```

### B. API Services Available

Your environment has access to:

**?? AI/LLM Services** (26 providers)
- OpenAI (GPT-4, DALL-E, Whisper)
- Anthropic (Claude)
- Google (Gemini)
- Mistral, Perplexity, DeepSeek, Groq, Cohere

**?? Image Generation** (8 services)
- Leonardo AI, Stability AI, Replicate, Runway, FAL, Pika

**?? Audio/Music** (6 services)
- Suno, ElevenLabs, AssemblyAI, Deepgram, Murf, Rev.ai

**?? Cloud Storage** (4 providers)
- AWS, Cloudflare R2, Supabase, Google Cloud

**??? Vector Databases** (4 services)
- Pinecone, Qdrant, ChromaDB, Zep

### C. Best Practices

**?? Security**
- Never commit API keys to git
- Use environment variables exclusively
- Rotate keys periodically

**? Performance**
- Use batch scripts for bulk operations
- Enable caching where available
- Monitor API quotas

**?? Development**
- Follow existing naming conventions
- Add docstrings and comments
- Test before deploying to production

### D. Common Workflows

**Instagram Content Campaign**
```bash
# Morning routine
python instagram-analyze-stats.py
python instagram-follow-user-followers.py --target competitor
python instagram-like-hashtags.py --hashtags art,design

# Content posting
python instagram-upload.py --image content.jpg --caption "..."
```

**AI Art Production**
```bash
# Generate artwork
python leonardo-api.py --prompt "cyberpunk city" --batch 10

# Upscale and organize
python leonardo-upscale-loop.py
python image-organize-by-date.py
```

**Music Production Pipeline**
```bash
# Generate tracks
python suno-generator.py --prompts music_ideas.txt

# Organize library
python suno-music-catalog.py
python audio-normalize.py
```

---

## ?? Support

**Documentation Issues**: Check scripts for inline documentation  
**API Questions**: Refer to `~/.env.d/API_KEY_INVENTORY_COMPLETE_20251105_075949.csv`  
**Environment Setup**: See `STANDARD-ENV-LOADER.py`

---

_Built with ?? for automation enthusiasts ? Last updated {datetime.now().strftime('%B %Y')}_
"""

def main():
    """Generate reorganized documentation"""
    print("?? Documentation Reorganizer")
    print("=" * 80)
    
    reorganizer = DocsReorganizer()
    
    print("?? Generating enhanced documentation...")
    enhanced_docs = reorganizer.generate_enhanced_docs()
    
    # Save to file
    output_file = reorganizer.base_dir / "DOCUMENTATION.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(enhanced_docs)
    
    print(f"? Enhanced documentation saved: {output_file}")
    print(f"?? File size: {output_file.stat().st_size / 1024:.1f} KB")
    print(f"?? Total scripts documented: {len(reorganizer.data['scripts'])}")

if __name__ == "__main__":
    main()
