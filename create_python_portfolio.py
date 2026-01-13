#!/usr/bin/env python3
"""
Create a Python portfolio HTML page matching the format of avatararts.org/python.html
"""

import os
from pathlib import Path
from datetime import datetime
import json

TARGET_DIR = "/Users/steven/pythons"
OUTPUT_FILE = "/Users/steven/pythons/python.html"

def categorize_project(name, path):
    """Categorize a project based on its name and path."""
    name_lower = name.lower()
    path_lower = str(path).lower()

    # AI-Powered Media Processing
    if any(x in name_lower for x in ['transcribe', 'transcription', 'whisper', 'audio', 'video']):
        if any(x in name_lower for x in ['ai', 'gpt', 'openai']):
            return 'AI-Powered Media Processing'

    # YouTube Automation & Video Generation
    if any(x in name_lower for x in ['youtube', 'yt-', 'yt_', 'youtube-', 'youtube_']):
        return 'YouTube Automation & Video Generation'

    # Twitch & Streaming Tools
    if any(x in name_lower for x in ['twitch', 'stream']):
        return 'Twitch & Streaming Tools'

    # Social Media Bots
    if any(x in name_lower for x in ['instagram', 'tiktok', 'facebook', 'twitter', 'social']):
        return 'Social Media Bots (Instagram, TikTok, Facebook)'

    # E-commerce & Web Automation
    if any(x in name_lower for x in ['etsy', 'redbubble', 'printify', 'fiverr', 'ecommerce', 'e-commerce', 'pod-']):
        return 'E-commerce & Web Automation'

    # Creative Tools & Generative AI
    if any(x in name_lower for x in ['dalle', 'leonardo', 'comic', 'lyrics', 'typography', 'image-gpt', 'ai-art']):
        return 'Creative Tools & Generative AI'

    # Web & Gallery Generators
    if any(x in name_lower for x in ['gallery', 'html', 'website', 'web']):
        if any(x in name_lower for x in ['gallery', 'album']):
            return 'Web & Gallery Generators'

    # Utility & File Management
    if any(x in name_lower for x in ['organize', 'cleanup', 'sort', 'remove', 'merge', 'dedupe', 'file', 'download', 'convert']):
        return 'Utility & File Management Scripts'

    # Adobe Automation
    if any(x in name_lower for x in ['photoshop', 'adobe', 'mockup', 'grid']):
        return 'Adobe Automation Scripts'

    # Miscellaneous
    return 'Miscellaneous & Experimental'

def get_project_info(filepath):
    """Extract basic info about a project."""
    info = {
        'name': filepath.stem,
        'path': str(filepath.relative_to(Path(TARGET_DIR))),
        'size_kb': filepath.stat().st_size / 1024 if filepath.exists() else 0
    }

    # Try to get first few lines for description
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()[:30]
            content = ''.join(lines)
            info['preview'] = content[:500]
    except:
        info['preview'] = ''

    return info

def generate_description(name, category, path):
    """Generate a description for a project based on its name and category."""
    name_lower = name.lower()

    descriptions = {
        'YouTube Automation & Video Generation': {
            'default': f"An **automated YouTube tool** for creating and managing video content. This project focuses on streamlining YouTube workflows through automation and AI integration.",
        },
        'AI-Powered Media Processing': {
            'default': f"An **AI-powered media processing pipeline** that uses machine learning and automation to process audio and video content.",
        },
        'Social Media Bots': {
            'default': f"A **social media automation tool** for managing and automating interactions across various platforms.",
        },
        'E-commerce & Web Automation': {
            'default': f"An **e-commerce automation tool** for streamlining online business operations and product management.",
        },
        'Creative Tools & Generative AI': {
            'default': f"A **creative AI tool** that combines generative models with artistic workflows to produce unique content.",
        },
        'Web & Gallery Generators': {
            'default': f"A **web and gallery generation tool** for creating and managing visual content displays.",
        },
        'Utility & File Management': {
            'default': f"A **utility script** for organizing, cleaning, and managing files and directories.",
        },
    }

    # Return a generic description
    return f"A **Python automation tool** that streamlines workflows and processes. Part of the AI Alchemy project portfolio, this script exemplifies the fusion of code and creativity to transform complex tasks into automated solutions."

def get_tags(name, category):
    """Generate tags for a project."""
    name_lower = name.lower()
    tags = ['Python']

    if 'youtube' in name_lower:
        tags.extend(['YouTube API', 'Automation', 'Video'])
    if 'ai' in name_lower or 'gpt' in name_lower:
        tags.extend(['AI', 'OpenAI', 'Automation'])
    if 'instagram' in name_lower or 'social' in name_lower:
        tags.extend(['Social Media', 'Automation'])
    if 'cleanup' in name_lower or 'organize' in name_lower:
        tags.extend(['File Management', 'Automation'])
    if 'gallery' in name_lower:
        tags.extend(['Web', 'HTML', 'Gallery'])

    return tags

def create_portfolio_html():
    """Create the portfolio HTML matching avatararts.org/python.html format."""
    base = Path(TARGET_DIR)

    # Collect all projects
    projects_by_category = {}
    all_items = []

    # Get top-level Python files
    for item in sorted(base.iterdir()):
        if item.name.startswith('.') or item.name in ['__pycache__', 'custom_code_analysis', 'duplicate_comparison', 'function_analysis']:
            continue

        if item.is_file() and item.suffix == '.py':
            info = get_project_info(item)
            category = categorize_project(item.name, item)
            if category not in projects_by_category:
                projects_by_category[category] = []
            projects_by_category[category].append(info)
            all_items.append(info)
        elif item.is_dir():
            # Check for Python files in directory
            py_files = list(item.rglob('*.py'))
            if py_files:
                # Use directory as project
                info = {
                    'name': item.name,
                    'path': str(item.relative_to(base)),
                    'is_directory': True,
                    'py_file_count': len(py_files)
                }
                category = categorize_project(item.name, item)
                if category not in projects_by_category:
                    projects_by_category[category] = []
                projects_by_category[category].append(info)
                all_items.append(info)

    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Alchemy Project Portfolio - AvatarArts</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.7;
            color: #1a1a1a;
            background: #f8f9fa;
            padding: 0;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
            background: white;
        }}
        h1 {{
            font-size: 2.5em;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 10px;
            line-height: 1.2;
        }}
        .subtitle {{
            font-size: 1.2em;
            color: #666;
            font-style: italic;
            margin-bottom: 40px;
        }}
        .intro {{
            font-size: 1.05em;
            color: #333;
            margin-bottom: 50px;
            line-height: 1.8;
        }}
        .intro strong {{
            color: #1a1a1a;
            font-weight: 600;
        }}
        h2 {{
            font-size: 1.8em;
            font-weight: 600;
            color: #1a1a1a;
            margin-top: 50px;
            margin-bottom: 20px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
        }}
        h2:first-of-type {{
            border-top: none;
            padding-top: 0;
            margin-top: 0;
        }}
        h3 {{
            font-size: 1.4em;
            font-weight: 600;
            color: #1a1a1a;
            margin-top: 35px;
            margin-bottom: 15px;
        }}
        h4 {{
            font-size: 1.2em;
            font-weight: 600;
            color: #1a1a1a;
            margin-top: 25px;
            margin-bottom: 10px;
        }}
        p {{
            margin-bottom: 15px;
            color: #333;
        }}
        .toc {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 25px 30px;
            margin: 40px 0;
            border-radius: 4px;
        }}
        .toc h2 {{
            font-size: 1.5em;
            margin: 0 0 20px 0;
            padding: 0;
            border: none;
        }}
        .toc ul {{
            list-style: none;
            padding-left: 0;
        }}
        .toc > ul > li {{
            margin-bottom: 15px;
        }}
        .toc ul ul {{
            padding-left: 25px;
            margin-top: 8px;
        }}
        .toc ul ul li {{
            margin-bottom: 6px;
        }}
        .toc a {{
            color: #667eea;
            text-decoration: none;
        }}
        .toc a:hover {{
            text-decoration: underline;
        }}
        .project {{
            margin-bottom: 40px;
        }}
        .project-name {{
            font-size: 1.3em;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 10px;
        }}
        .project-description {{
            margin-bottom: 12px;
            color: #333;
        }}
        .project-description strong {{
            color: #1a1a1a;
            font-weight: 600;
        }}
        .tags {{
            margin-top: 10px;
            font-size: 0.9em;
            color: #666;
        }}
        .tags strong {{
            font-weight: 600;
            color: #555;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            color: #d63384;
        }}
        pre {{
            background: #f8f9fa;
            border: 1px solid #e0e0e0;
            border-left: 4px solid #667eea;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            margin: 15px 0;
        }}
        pre code {{
            background: none;
            padding: 0;
            color: #333;
        }}
        .footer {{
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
            color: #666;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>**AI Alchemy Project Portfolio**</h1>
        <p class="subtitle">_Transforming chaos into creativity through coded rituals_</p>

        <div class="intro">
            <p>This portfolio is a compendium of projects and scripts (our **"technical rituals"**) that merge automation with artistry. The catalog is organized for easy visual browsing and search, with each project summarized and tagged. From **AI-powered media pipelines** to **social media bots** and **creative generative tools**, each entry reflects a blend of technical skill and creative chaos. Use the **Table of Contents** below to navigate through these projects, and click on any entry to jump to its description.</p>
        </div>

        <div class="toc">
            <h2>**Table of Contents**</h2>
            <ul>
"""

    # Add TOC
    category_order = [
        'AI-Powered Media Processing',
        'YouTube Automation & Video Generation',
        'Twitch & Streaming Tools',
        'Social Media Bots (Instagram, TikTok, Facebook)',
        'E-commerce & Web Automation',
        'Creative Tools & Generative AI',
        'Web & Gallery Generators',
        'Utility & File Management Scripts',
        'Adobe Automation Scripts',
        'Miscellaneous & Experimental'
    ]

    for category in category_order:
        if category in projects_by_category:
            cat_id = category.lower().replace(' ', '-').replace('(', '').replace(')', '').replace(',', '')
            html += f'                <li><strong>{category}</strong>\n                    <ul>\n'
            for project in projects_by_category[category][:15]:  # Limit to 15 per category in TOC
                project_id = project['name'].lower().replace(' ', '-').replace('_', '-')
                html += f'                        <li><a href="#{project_id}">{project["name"]}</a></li>\n'
            html += '                    </ul>\n                </li>\n'

    html += """
            </ul>
        </div>
"""

    # Add projects by category
    for category in category_order:
        if category not in projects_by_category:
            continue

        html += f'\n        <hr style="margin: 50px 0; border: none; border-top: 2px solid #e0e0e0;">\n\n        <h2>**{category}**</h2>\n\n'

        for project in sorted(projects_by_category[category], key=lambda x: x['name']):
            project_id = project['name'].lower().replace(' ', '-').replace('_', '-')
            tags = get_tags(project['name'], category)
            description = generate_description(project['name'], category, project['path'])

            html += f'        <div class="project" id="{project_id}">\n'
            html += f'            <h3 class="project-name">**{project["name"]}**</h3>\n'
            html += f'            <div class="project-description">\n                <p>{description}</p>\n'

            if project.get('is_directory'):
                html += f'                <p>This directory contains <strong>{project.get("py_file_count", 0)} Python files</strong>, making it a comprehensive collection of related scripts and tools.</p>\n'

            html += f'            </div>\n'
            html += f'            <div class="tags"><strong>Tags:</strong> {", ".join(tags)}</div>\n'
            html += f'        </div>\n\n'

    html += f"""
        <div class="footer">
            <p>Each project in this catalog is a testament to an overarching ethos: <strong>technology as creative empowerment</strong>. From automating tedious tasks to weaving AI into art, these scripts and tools form an ecosystem – an **"AI Alchemy" lab** – where code transfigures chaos into order and imagination into reality. Whether it's a social media spell, a data ritual, or an artistic incantation, this portfolio embodies a fusion of <strong>poetic automation</strong> and practical innovation, true to the unique creative-technical brand. Welcome to the hub of <strong>Chaos Automation</strong>, where every script is both a tool and a story.</p>
            <p style="margin-top: 20px; text-align: right; color: #999;">Generated: {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
    </div>
</body>
</html>
"""

    # Write to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Portfolio HTML created: {OUTPUT_FILE}")
    print(f"   Categories: {len(projects_by_category)}")
    print(f"   Total projects: {len(all_items)}")

    return OUTPUT_FILE

if __name__ == "__main__":
    try:
        create_portfolio_html()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
