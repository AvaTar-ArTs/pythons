#!/usr/bin/env python3
"""from collections import Counter
from datetime import datetime
from pathlib import Path
from pathlib import Path as PathLib
import os

from dotenv import load_dotenv
Rich Documentation Generator for Script Renames
Creates engaging, narrative documentation with detailed descriptions
Outputs: Detailed Markdown, Interactive HTML, CSV, and JSON
"""

# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)


def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            line = line.removeprefix("export ")
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")


load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass


class RichDocGenerator:
    """Generate rich, narrative documentation"""

    def __init__(self):
        self.renames = []
        self.output_dir = Path.home() / "pythons" / "_docs"
        self.output_dir.mkdir(exist_ok=True)

    def add_rename(
        self,
        current_name: str,
        description: str,
        new_name: str,
        action: str = "RENAME",
        category: str = "",
        why_rename: str = "",
        impact: str = "",
        apis_used: list = None,
    ):
        """Add a rename entry with rich metadata"""
        self.renames.append(
            {
                "current_name": current_name,
                "description": description,
                "new_name": new_name,
                "action": action,
                "category": category,
                "why_rename": why_rename,
                "impact": impact,
                "apis_used": apis_used or [],
            },
        )

    def generate_rich_markdown(self):
        """Generate detailed, narrative Markdown documentation"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"rename_documentation_{timestamp}.md"

        # Calculate statistics
        total_files = len(self.renames)
        by_action = Counter(item["action"] for item in self.renames)
        by_category = {}
        for item in self.renames:
            cat = item.get("category", "Uncategorized")
            by_category.setdefault(cat, []).append(item)

        with open(output_path, "w") as f:
            # Header
            f.write("# 🎯 Python Scripts Renaming Documentation\n\n")
            f.write("**A Comprehensive Guide to Organizing Your Python Toolkit**\n\n")
            f.write(
                f"*Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*\n\n",
            )
            f.write("---\n\n")

            # Executive Summary
            f.write("## 📊 Executive Summary\n\n")
            f.write(
                f"This document details the renaming of **{total_files} Python scripts** ",
            )
            f.write(
                "to create a more intuitive, organized, and maintainable codebase. ",
            )
            f.write(
                "Each rename reflects what the script **actually does** rather than vague or technical naming.\n\n",
            )

            f.write("### Quick Stats\n\n")
            f.write(
                f"- 🏷️ **{by_action.get('RENAME', 0)} files** being renamed for clarity\n",
            )
            f.write(
                f"- 🗑️ **{by_action.get('DELETE', 0)} files** marked for deletion (duplicates, library code)\n",
            )
            f.write(
                f"- ✅ **{by_action.get('KEEP', 0)} files** already have perfect names\n",
            )
            f.write(
                f"- 📦 **{by_action.get('MOVE', 0)} files** being moved to appropriate directories\n",
            )
            f.write(
                f"- 📂 **{len(by_category)} categories** identified for better organization\n\n",
            )

            f.write("---\n\n")

            # Renaming Philosophy
            f.write("## 💡 Renaming Philosophy\n\n")
            f.write("### Why These Changes Matter\n\n")
            f.write(
                "The goal is to create **self-documenting filenames** that immediately ",
            )
            f.write("communicate purpose and functionality. Instead of:\n\n")
            f.write("- ❌ `analyze-metadata.py` (vague - analyze what metadata?)\n")
            f.write(
                "- ✅ `transcript-to-image-prompts.py` (clear - converts transcripts to image prompts)\n\n",
            )
            f.write("### Naming Principles Applied\n\n")
            f.write(
                "1. **Action-First Naming** - Use verbs that describe the core action\n",
            )
            f.write(
                "2. **Input-Output Clarity** - Show what goes in and what comes out\n",
            )
            f.write(
                "3. **Technology Transparency** - Indicate key technologies used (GPT, Claude, etc.)\n",
            )
            f.write(
                "4. **Purpose Over Implementation** - Focus on WHAT it does, not HOW\n\n",
            )
            f.write("---\n\n")

            # By Category
            f.write("## 📂 Detailed Renaming Plan by Category\n\n")

            for category in sorted(by_category.keys()):
                items = by_category[category]
                if not items:
                    continue

                # Category header with icon
                cat_icons = {
                    "Image Analysis": "🖼️",
                    "Image Generation": "🎨",
                    "Audio Generation": "🎵",
                    "Code Analysis": "🔍",
                    "AI Tools": "🤖",
                    "Documentation": "📚",
                    "File Organization": "📁",
                    "Media Organization": "🎬",
                    "File Analysis": "📊",
                    "Cleanup": "🧹",
                    "Web Scraping": "🕸️",
                    "Social Media": "📱",
                }
                icon = cat_icons.get(category, "📌")

                f.write(f"### {icon} {category}\n\n")
                f.write(f"*{len(items)} file(s) in this category*\n\n")

                for i, item in enumerate(
                    sorted(items, key=lambda x: x["current_name"]),
                    1,
                ):
                    action = item["action"]

                    if action == "DELETE":
                        f.write(
                            f"#### {i}. ~~`{item['current_name']}`~~ → 🗑️ DELETE\n\n",
                        )
                        f.write(f"**Why Delete:** {item['description']}\n\n")
                    elif action == "KEEP":
                        f.write(f"#### {i}. `{item['current_name']}` → ✅ KEEP\n\n")
                        f.write(f"**Why Keep:** {item['description']}\n\n")
                    else:
                        f.write(
                            f"#### {i}. `{item['current_name']}` → `{item['new_name']}`\n\n",
                        )

                        f.write(f"**What It Does:** {item['description']}\n\n")

                        if item.get("why_rename"):
                            f.write(f"**Why Rename:** {item['why_rename']}\n\n")

                        if item.get("impact"):
                            f.write(f"**Impact:** {item['impact']}\n\n")

                        if item.get("apis_used"):
                            apis = ", ".join(item["apis_used"])
                            f.write(f"**Technologies:** {apis}\n\n")

                    f.write("---\n\n")

            # Quick Reference Table
            f.write("## 📋 Quick Reference Table\n\n")
            f.write("| Current Name | New Name | Category | Action |\n")
            f.write("|--------------|----------|----------|--------|\n")

            for item in sorted(self.renames, key=lambda x: x["current_name"]):
                current = item["current_name"]
                new = (
                    item["new_name"]
                    if item["action"] == "RENAME"
                    else f"**{item['action']}**"
                )
                cat = item.get("category", "")
                action = item["action"]

                action_emoji = {
                    "RENAME": "🏷️",
                    "DELETE": "🗑️",
                    "KEEP": "✅",
                    "MOVE": "📦",
                }.get(action, "📌")

                f.write(
                    f"| `{current}` | `{new}` | {cat} | {action_emoji} {action} |\n",
                )

            f.write("\n---\n\n")

            # Implementation Guide
            f.write("## 🚀 Implementation Guide\n\n")
            f.write("### Step 1: Backup Current State\n\n")
            f.write("```bash\n")
            f.write("# Create backup\n")
            f.write("tar -czf ~/pythons_backup_$(date +%Y%m%d).tar.gz ~/pythons\n")
            f.write("```\n\n")

            f.write("### Step 2: Execute Renames\n\n")
            f.write("```bash\n")
            f.write("cd ~/pythons\n\n")

            for item in self.renames:
                if item["action"] == "RENAME":
                    f.write(f"mv {item['current_name']} {item['new_name']}\n")
                elif item["action"] == "DELETE":
                    f.write(
                        f"rm {item['current_name']}  # {item['description'][:50]}\n",
                    )

            f.write("```\n\n")

            f.write("### Step 3: Update Documentation\n\n")
            f.write(
                "Update any README files or documentation that reference the old filenames.\n\n",
            )

            f.write("---\n\n")

            # Footer
            f.write("## 📝 Notes\n\n")
            f.write("- All renames preserve functionality - only filenames change\n")
            f.write(
                "- This reorganization makes your toolkit more professional and maintainable\n",
            )
            f.write("- Consider creating a `README.md` in each category folder\n")
            f.write("- Future scripts should follow these naming conventions\n\n")

            f.write("---\n\n")
            f.write(
                f"*Documentation generated by Rich Doc Generator on {datetime.now().strftime('%B %d, %Y')}*\n",
            )

        return output_path

    def generate_html(self):
        """Generate beautiful interactive HTML documentation"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"rename_documentation_{timestamp}.html"

        # Calculate statistics
        by_category = {}
        for item in self.renames:
            cat = item.get("category", "Uncategorized")
            by_category.setdefault(cat, []).append(item)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Scripts Renaming Documentation</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .category {{
            margin-bottom: 40px;
        }}
        
        .category-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .category-header h2 {{
            font-size: 1.5em;
        }}
        
        .rename-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
        }}
        
        .rename-card.delete {{
            border-left-color: #dc3545;
            background: #fff5f5;
        }}
        
        .rename-card.keep {{
            border-left-color: #28a745;
            background: #f0fff4;
        }}
        
        .file-name {{
            font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
            background: white;
            padding: 5px 10px;
            border-radius: 4px;
            display: inline-block;
            margin: 5px 0;
            font-size: 0.9em;
        }}
        
        .arrow {{
            color: #667eea;
            font-size: 1.5em;
            margin: 0 10px;
        }}
        
        .description {{
            margin: 10px 0;
            color: #555;
        }}
        
        .tag {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            margin: 5px 5px 5px 0;
        }}
        
        .search-box {{
            width: 100%;
            padding: 15px;
            font-size: 1.1em;
            border: 2px solid #667eea;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        
        footer {{
            background: #333;
            color: white;
            text-align: center;
            padding: 20px;
        }}
        
        @media (max-width: 768px) {{
            header h1 {{
                font-size: 1.8em;
            }}
            
            .stats {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎯 Python Scripts Renaming Documentation</h1>
            <p>A Comprehensive Guide to Organizing Your Python Toolkit</p>
            <p><small>Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</small></p>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(self.renames)}</div>
                <div class="stat-label">Total Files</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{sum(1 for i in self.renames if i['action'] == 'RENAME')}</div>
                <div class="stat-label">Renamed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(by_category)}</div>
                <div class="stat-label">Categories</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{sum(1 for i in self.renames if i['action'] == 'DELETE')}</div>
                <div class="stat-label">Deleted</div>
            </div>
        </div>
        
        <div class="content">
            <input type="text" class="search-box" id="searchBox" placeholder="🔍 Search for scripts..." onkeyup="searchScripts()">
"""

        # Add categories
        for category in sorted(by_category.keys()):
            items = by_category[category]
            if not items:
                continue

            cat_icons = {
                "Image Analysis": "🖼️",
                "Image Generation": "🎨",
                "Audio Generation": "🎵",
                "Code Analysis": "🔍",
                "AI Tools": "🤖",
                "Documentation": "📚",
                "File Organization": "📁",
                "Media Organization": "🎬",
                "File Analysis": "📊",
                "Cleanup": "🧹",
            }
            icon = cat_icons.get(category, "📌")

            html += f"""
            <div class="category">
                <div class="category-header">
                    <span style="font-size: 1.5em;">{icon}</span>
                    <h2>{category}</h2>
                    <span style="margin-left: auto;">({len(items)} files)</span>
                </div>
"""

            for item in sorted(items, key=lambda x: x["current_name"]):
                action_class = item["action"].lower()

                html += f"""
                <div class="rename-card {action_class}" data-searchable="{item['current_name']} {item.get('new_name', '')} {item['description']}">
"""

                if item["action"] == "DELETE":
                    html += f"""
                    <div><span class="file-name">~~{item['current_name']}~~</span> <span class="arrow">→</span> <span class="tag" style="background: #dc3545;">DELETE</span></div>
                    <div class="description">{item['description']}</div>
"""
                elif item["action"] == "KEEP":
                    html += f"""
                    <div><span class="file-name">{item['current_name']}</span> <span class="tag" style="background: #28a745;">✅ KEEP</span></div>
                    <div class="description">{item['description']}</div>
"""
                else:
                    html += f"""
                    <div><span class="file-name">{item['current_name']}</span> <span class="arrow">→</span> <span class="file-name">{item['new_name']}</span></div>
                    <div class="description"><strong>What it does:</strong> {item['description']}</div>
"""

                    if item.get("apis_used"):
                        html += "<div>"
                        for api in item["apis_used"]:
                            html += f'<span class="tag">{api}</span>'
                        html += "</div>"

                html += """
                </div>
"""

            html += """
            </div>
"""

        html += """
        </div>
        
        <footer>
            <p>Documentation generated by Rich Doc Generator</p>
            <p><small>All renames preserve functionality - only filenames change for clarity</small></p>
        </footer>
    </div>
    
    <script>
        function searchScripts() {
            const searchTerm = document.getElementById('searchBox').value.toLowerCase();
            const cards = document.querySelectorAll('.rename-card');
            
            cards.forEach(card => {
                const searchableText = card.getAttribute('data-searchable').toLowerCase();
                if (searchableText.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>"""

        with open(output_path, "w") as f:
            f.write(html)

        return output_path

    def generate_all(self):
        """Generate all documentation formats"""
        md_path = self.generate_rich_markdown()
        html_path = self.generate_html()

        print("✅ Generated rich documentation:")
        print(f"   📄 Markdown: {md_path}")
        print(f"   🌐 HTML:     {html_path}")
        print("\n💡 Open HTML in browser:")
        print(f"   open {html_path}")

        return md_path, html_path


# Current batch with rich metadata
def generate_current_batch():
    """Generate docs for current batch with detailed information"""
    gen = RichDocGenerator()

    # Image Analysis category
    gen.add_rename(
        "analyze-prompt.py",
        "Takes an existing CSV file with image paths and enriches it by calling GPT-4 Vision API to add AI-generated metadata like SEO titles, product suggestions, tags, and emotional analysis for each image.",
        "gpt-vision-csv-enricher.py",
        "RENAME",
        "Image Analysis",
        "Original name doesn't indicate it works with CSVs or uses GPT Vision",
        "Makes it immediately clear this enriches CSV data using GPT Vision",
        ["GPT-4 Vision", "OpenAI", "CSV"],
    )

    gen.add_rename(
        "analyze-reader.py",
        "Scans a folder of images and uses GPT-4 Vision to analyze each image for print-on-demand products, generating comprehensive metadata including subject, style, color palette, suggested products, SEO-optimized titles and descriptions.",
        "gpt-vision-image-analyzer.py",
        "RENAME",
        "Image Analysis",
        'Name "analyze-reader" is too generic and doesn\'t convey GPT Vision usage',
        "Clear indication of GPT Vision analysis for images",
        ["GPT-4 Vision", "OpenAI", "Print-on-Demand"],
    )

    gen.add_rename(
        "analyze-json-writer.py",
        "Shared helper utilities library for GPT-based image metadata enrichment. Provides reusable functions for discovering images, extracting EXIF data, calling GPT Vision API, and building source tags.",
        "image-metadata-helpers.py",
        "RENAME",
        "Image Analysis",
        "Name suggests JSON writing, but it's actually a utilities library for image metadata",
        "Accurately describes its role as a helper library for image metadata operations",
        ["GPT-4 Vision", "PIL/Pillow", "EXIF"],
    )

    # Image Generation category
    gen.add_rename(
        "analyze-metadata.py",
        "Reads timestamped transcript files and generates detailed, cinematic image prompts for AI image generation. Creates transition images, main narrative images, and typography overlays with mood detection, style hints, and color themes.",
        "transcript-to-image-prompts.py",
        "RENAME",
        "Image Generation",
        '"analyze-metadata" is vague - this specifically converts transcripts to image generation prompts',
        "Self-documenting name showing input (transcript) → output (image prompts)",
        ["Midjourney", "DALL-E", "Stable Diffusion"],
    )

    # Audio Generation category
    gen.add_rename(
        "alchemy-quiz.py",
        'Reads quiz data from a CSV file and automatically generates MP3 audio files using OpenAI\'s Text-to-Speech API with the "shimmer" voice. Calculates audio duration and creates quiz question audio files.',
        "csv-to-audio-quiz.py",
        "RENAME",
        "Audio Generation",
        "Project-specific name doesn't describe functionality",
        "Clear description: CSV input → Audio quiz output",
        ["OpenAI TTS", "pydub"],
    )

    # Code Analysis category
    gen.add_rename(
        "ai-stability-code.py",
        "Comprehensive code quality analyzer with intelligent pattern detection. Analyzes Python code for security vulnerabilities, performance issues, code style, documentation quality, and provides confidence-scored insights with actionable suggestions.",
        "code-quality-analyzer.py",
        "RENAME",
        "Code Analysis",
        '"ai-stability-code" is unclear - references internal project name',
        "Standard, recognizable name for code quality analysis",
        ["AST", "Static Analysis"],
    )

    gen.add_rename(
        "analyze-code-complexity.py",
        "Analyzes Python code complexity using Radon and Pylint. Generates cyclomatic complexity scores, maintainability index, and creates visual network graphs of code dependencies and relationships.",
        "python-complexity-analyzer.py",
        "RENAME",
        "Code Analysis",
        'Generic "analyze" prefix when it\'s specifically Python complexity',
        "Immediately identifies language (Python) and metric (complexity)",
        ["Radon", "Pylint", "NetworkX"],
    )

    gen.add_rename(
        "ai-deep-analyzer.py",
        "Advanced AI-powered code analyzer combining AST parsing, semantic understanding from multiple LLMs (OpenAI/Gemini/Claude), vector embeddings for similarity detection, and architectural pattern recognition with confidence scoring.",
        "ai-deep-analyzer.py",
        "KEEP",
        "Code Analysis",
        "Name is already clear and descriptive - indicates AI-powered deep analysis",
    )

    # AI Tools category
    gen.add_rename(
        "AI_ORCHESTRATOR_ULTIMATE.py",
        "Intelligent multi-model AI orchestrator that routes tasks to the optimal AI service among 12 different APIs (GPT-5, Claude, Grok, Groq, Gemini, Perplexity, DeepSeek, Mistral, Cohere, OpenRouter, Together AI, Cerebras). Selects models based on task type, supports multi-AI consensus, parallel processing, and automatic quality scoring.",
        "multi-llm-orchestrator.py",
        "RENAME",
        "AI Tools",
        'ALL_CAPS with "ULTIMATE" is too hyperbolic',
        "Professional naming that describes functionality: orchestrates multiple LLMs",
        ["OpenAI", "Anthropic", "Groq", "Gemini", "Perplexity"],
    )

    gen.add_rename(
        "AI_SETUP_VERIFICATION.py",
        "Verification tool that checks the installation and configuration of all AI service SDKs and API keys. Tests Python packages (openai, anthropic, groq, etc.) and validates environment variables, displaying colored status reports.",
        "check-ai-sdks.py",
        "RENAME",
        "AI Tools",
        "ALL_CAPS naming style doesn't fit with rest of codebase",
        "Consistent lowercase naming with clear verb (check) + target (AI SDKs)",
        ["Package Management"],
    )

    # Documentation category
    gen.add_rename(
        "ADVANCED_SYSTEMS_CATALOG.py",
        "Comprehensive project discovery and cataloging system. Scans ~/pythons, ~/workspace, ~/GitHub, and ~/Documents to discover all projects, analyze tech stacks, identify frontend/backend/database components, assess deployment readiness, and generate catalog documentation.",
        "project-catalog-generator.py",
        "RENAME",
        "Documentation",
        'ALL_CAPS and "ADVANCED_SYSTEMS" is vague about what it catalogs',
        "Clear purpose: generates project catalog documentation",
        ["Sphinx"],
    )

    gen.add_rename(
        "ai-docs-generator.py",
        "AI-powered documentation generator that uses GPT-4 and Claude to intelligently analyze Python scripts and create comprehensive documentation including purpose, features, dependencies, use cases, and complexity ratings.",
        "ai-docs-generator.py",
        "KEEP",
        "Documentation",
        "Name is already clear: AI-powered documentation generator",
    )

    # File Organization category
    gen.add_rename(
        "album-sorting.py",
        "Media file organizer that sorts MP3, MP4, and TXT files by album name into organized directory structures. Processes media files from a source directory and organizes them into album-based folders.",
        "sort-media-by-album.py",
        "RENAME",
        "Media Organization",
        '"album-sorting" sounds passive - doesn\'t indicate it actively organizes files',
        "Action verb (sort) + what it sorts (media) + how it sorts (by album)",
        ["pydub"],
    )

    gen.add_rename(
        "analyze-file-migration.py",
        "Migration planning tool that analyzes current directory structure and shows what files will be migrated to which category folders (youtube_projects, ai_creative, web_scraping, etc.) before actually executing the migration.",
        "migration-planner.py",
        "RENAME",
        "File Organization",
        '"analyze-file-migration" is too long and focuses on analysis vs. planning',
        "Concise name indicating it plans migrations",
        [],
    )

    gen.add_rename(
        "analyze-file-versions.py",
        "Version detection tool that finds all versioned scripts (script-v1.py, script_2.py, etc.), compares file sizes and modification dates, and recommends which version to keep based on the newest and largest file.",
        "find-script-versions.py",
        "RENAME",
        "File Organization",
        '"analyze" prefix when the core action is finding/detecting versions',
        "Clear action: finds script versions for cleanup",
        [],
    )

    # File Analysis category
    gen.add_rename(
        "analyze-files-comprehensive.py",
        "Master orchestrator that runs ALL 14 production analysis tools plus 8 different AI models to perform complete, comprehensive file analysis. Coordinates multiple analysis scripts and aggregates results into unified reports.",
        "master-file-analyzer.py",
        "RENAME",
        "File Analysis",
        'Long name with generic "comprehensive" modifier',
        "Clear hierarchy: master analyzer that orchestrates others",
        ["Multi-tool orchestration"],
    )

    # Cleanup category
    gen.add_rename(
        "_RefreshThread.py",
        "This is internal Rich library code for terminal UI threading - not user-created code. Part of the Rich text rendering library for Python terminal displays.",
        "",
        "DELETE",
        "Cleanup",
        "Not user code - belongs to Rich library",
        "Removes non-user code from directory",
        [],
    )

    gen.add_rename(
        "alchemyapi-audio-demo-generator.py",
        'Highly project-specific tool for creating emotional audio demos for the AlchemyAPI project. Creates complex audio patterns with mood profiles like "epic_heroic", "mystical_wisdom" using synthesized tones and harmonics.',
        "",
        "DELETE",
        "Cleanup",
        "Too project-specific for general toolkit",
        "Removes overly specific code not useful for general purposes",
        ["pydub", "Audio Synthesis"],
    )

    return gen


if __name__ == "__main__":
    gen = generate_current_batch()
    md_path, html_path = gen.generate_all()

    print("\n📖 View documentation:")
    print(f"   cat {md_path}")
    print(f"   open {html_path}")
