#!/usr/bin/env python3
"""
Create an organized HTML list from ~/pythons directory,
inspired by the structure of avatararts.org pages.
"""

import os
from pathlib import Path
from datetime import datetime
import json

TARGET_DIR = "/Users/steven/pythons"
OUTPUT_FILE = "/Users/steven/pythons/pythons_list.html"

def categorize_file(filepath):
    """Categorize a file based on its name/path."""
    name = filepath.lower()

    # Cleanup/organization scripts
    if any(x in name for x in ['cleanup', 'clean', 'organize', 'merge', 'dedupe', 'remove']):
        return 'Organization & Cleanup'

    # Analysis scripts
    if any(x in name for x in ['analyze', 'analysis', 'scan', 'index', 'find']):
        return 'Analysis & Scanning'

    # Automation/Bots
    if any(x in name for x in ['bot', 'automation', 'auto', 'platform']):
        return 'Automation & Bots'

    # Social media
    if any(x in name for x in ['instagram', 'twitter', 'youtube', 'social', 'file-organizer']):
        return 'Social Media Tools'

    # AI/ML
    if any(x in name for x in ['ai', 'gpt', 'llm', 'model', 'transcribe', 'transcription']):
        return 'AI & Machine Learning'

    # Media processing
    if any(x in name for x in ['video', 'audio', 'image', 'media', 'gallery']):
        return 'Media Processing'

    # E-commerce
    if any(x in name for x in ['etsy', 'printify', 'redbubble', 'revenue']):
        return 'E-commerce'

    # SEO/Marketing
    if any(x in name for x in ['seo', 'marketing', 'optimize']):
        return 'SEO & Marketing'

    # Web/Websites
    if any(x in name for x in ['website', 'web', 'html', 'app']):
        return 'Web Development'

    # Data/CSV
    if any(x in name for x in ['csv', 'data', 'json', 'export']):
        return 'Data Processing'

    return 'Other'

def get_directory_info(dirpath):
    """Get information about a directory."""
    try:
        py_files = list(dirpath.rglob('*.py'))
        subdirs = [d for d in dirpath.iterdir() if d.is_dir() and not d.name.startswith('.')]
        total_size = sum(f.stat().st_size for f in py_files if f.exists())

        return {
            'py_file_count': len(py_files),
            'subdirectory_count': len(subdirs),
            'total_size_mb': total_size / (1024 * 1024)
        }
    except:
        return {'py_file_count': 0, 'subdirectory_count': 0, 'total_size_mb': 0}

def create_html_list():
    """Create an organized HTML list from the pythons directory."""
    base = Path(TARGET_DIR)

    # Collect all items
    items_by_category = {}
    directories = []
    files = []

    for item in sorted(base.iterdir()):
        if item.name.startswith('.') or item.name in ['__pycache__', 'custom_code_analysis', 'duplicate_comparison', 'function_analysis']:
            continue

        if item.is_file():
            if item.suffix == '.py':
                category = categorize_file(item.name)
                if category not in items_by_category:
                    items_by_category[category] = []
                items_by_category[category].append({
                    'name': item.name,
                    'path': str(item.relative_to(base)),
                    'type': 'file'
                })
        elif item.is_dir():
            info = get_directory_info(item)
            category = categorize_file(item.name)
            if category not in items_by_category:
                items_by_category[category] = []
            items_by_category[category].append({
                'name': item.name,
                'path': str(item.relative_to(base)),
                'type': 'directory',
                **info
            })

    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Projects Directory - AvatarArts</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 40px;
        }}
        h1 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        .subtitle {{
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-card h3 {{
            font-size: 2em;
            margin-bottom: 5px;
        }}
        .stat-card p {{
            opacity: 0.9;
        }}
        .category {{
            margin-bottom: 40px;
        }}
        .category-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 8px 8px 0 0;
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 0;
        }}
        .category-content {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 0 0 8px 8px;
            border: 1px solid #e0e0e0;
        }}
        .item-list {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
        }}
        .item {{
            background: white;
            padding: 15px;
            border-radius: 6px;
            border: 1px solid #ddd;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .item.directory {{
            border-left: 4px solid #667eea;
        }}
        .item.file {{
            border-left: 4px solid #48bb78;
        }}
        .item-name {{
            font-weight: bold;
            color: #333;
            margin-bottom: 8px;
            word-break: break-word;
        }}
        .item-path {{
            font-size: 0.85em;
            color: #666;
            font-family: 'Monaco', 'Courier New', monospace;
            margin-bottom: 5px;
        }}
        .item-meta {{
            font-size: 0.8em;
            color: #888;
            margin-top: 8px;
        }}
        .badge {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.75em;
            margin-right: 5px;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🐍 Python Projects Directory</h1>
        <p class="subtitle">Comprehensive collection of Python scripts, tools, and projects</p>

        <div class="stats">
"""

    # Add stats
    total_files = sum(len(items) for items in items_by_category.values())
    total_dirs = sum(1 for cat in items_by_category.values() for item in cat if item['type'] == 'directory')
    total_py_files = sum(1 for cat in items_by_category.values() for item in cat if item['type'] == 'file')

    html += f"""
            <div class="stat-card">
                <h3>{len(items_by_category)}</h3>
                <p>Categories</p>
            </div>
            <div class="stat-card">
                <h3>{total_files}</h3>
                <p>Total Items</p>
            </div>
            <div class="stat-card">
                <h3>{total_dirs}</h3>
                <p>Directories</p>
            </div>
            <div class="stat-card">
                <h3>{total_py_files}</h3>
                <p>Python Files</p>
            </div>
        </div>
"""

    # Add categories
    for category in sorted(items_by_category.keys()):
        items = sorted(items_by_category[category], key=lambda x: x['name'])
        html += f"""
        <div class="category">
            <div class="category-header">{category}</div>
            <div class="category-content">
                <div class="item-list">
"""

        for item in items:
            item_class = 'directory' if item['type'] == 'directory' else 'file'
            html += f"""
                    <div class="item {item_class}">
                        <div class="item-name">{item['name']}</div>
                        <div class="item-path">{item['path']}</div>
"""
            if item['type'] == 'directory':
                html += f"""
                        <div class="item-meta">
                            <span class="badge">{item.get('py_file_count', 0)} .py files</span>
                            <span class="badge">{item.get('subdirectory_count', 0)} subdirs</span>
                        </div>
"""
            html += """
                    </div>
"""

        html += """
                </div>
            </div>
        </div>
"""

    html += f"""
        <div class="footer">
            <p>Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            <p>Total: {total_files} items across {len(items_by_category)} categories</p>
        </div>
    </div>
</body>
</html>
"""

    # Write to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ HTML list created: {OUTPUT_FILE}")
    print(f"   Categories: {len(items_by_category)}")
    print(f"   Total items: {total_files}")

    return OUTPUT_FILE

if __name__ == "__main__":
    try:
        create_html_list()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
