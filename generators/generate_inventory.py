#!/usr/bin/env python3
"""
Generate comprehensive marketplace inventory from all Python and CSV files
found across the user's home directory.
"""

import os
import csv
import datetime
from collections import defaultdict

# All temp files containing file lists
TEMP_FILES = [
    "/tmp/pythons_files.txt",
    "/tmp/MasterxEo_files.txt",
    "/tmp/MarketMaster_files.txt",
    "/tmp/scripts_files.txt",
    "/tmp/Development_files.txt",
    "/tmp/github_files.txt",
    "/tmp/my_crew_files.txt",
    "/tmp/Epstein_files.txt",
    "/tmp/AutoTagger_files.txt",
    "/tmp/autotagger-lite_files.txt",
    "/tmp/file-tracker_files.txt",
    "/tmp/sora-remover_files.txt",
    "/tmp/mcPHooker_files.txt",
    "/tmp/mcphooker-lite_files.txt",
    "/tmp/agent_forge_files.txt",
    "/tmp/ai_merge_auto_files.txt",
    "/tmp/grok_files.txt",
    "/tmp/my-simple_files.txt",
    "/tmp/uv-demo_files.txt",
    "/tmp/zombot-simple-gallery_files.txt",
    "/tmp/Downloads_Compressed_files.txt",
    "/tmp/Documents_files.txt",
    "/tmp/iterm2_files.txt",
    "/tmp/ice-tracker_files.txt",
    "/tmp/AutoTag_files.txt",
    "/tmp/claudemarketplaces_files.txt",
    "/tmp/Sora_files.txt",
    "/tmp/nocTurneMeLoDieS_files.txt",
    "/tmp/Miniforge_Mamba_Analysis_files.txt",
    "/tmp/codex-upgrades_files.txt",
    "/tmp/Fixes_files.txt",
    "/tmp/fuzzy-finder_files.txt",
    "/tmp/git-ai_files.txt",
    "/tmp/kimi_files.txt",
    "/tmp/tester_files.txt",
    "/tmp/tools_files.txt",
    "/tmp/userscripts_files.txt",
    "/tmp/agent-transcripts_files.txt",
    "/tmp/AI_Chats_files.txt",
    "/tmp/icloud_files.txt",
]

# Category mapping based on directory and filename patterns
CATEGORY_RULES = {
    # Directory-based rules
    "pythons/projects/frameworks/axolotl": ("ai_llm", "llm_training_framework", "Axolotl LLM fine-tuning framework"),
    "pythons/projects/frameworks": ("ai_llm", "ml_framework", "ML/AI framework code"),
    "pythons/projects/vibrant-chaplygin": ("ai_llm", "multi_purpose_ai", "Multi-purpose AI toolkit with transcription, image gen, content analysis"),
    "pythons/projects/botty": ("ecommerce", "product_management", "Product information and CSV management"),
    "pythons/projects/avatararts": ("media_processing", "image_gallery", "Avatar art gallery management"),
    "pythons/projects": ("ai_llm", "ai_project", "AI/ML project"),
    "pythons": ("ai_llm", "ai_collection", "Python AI/ML script collection"),

    "MasterxEo": ("ai_llm", "ai_platform", "MasterxEo AI platform"),
    "MarketMaster": ("business", "market_analysis", "Market analysis and trading tools"),
    "scripts": ("automation", "utility_scripts", "Utility and automation scripts"),
    "Development": ("development", "dev_tools", "Development tools and utilities"),
    "github": ("development", "github_repo", "GitHub repository code"),
    "my_crew": ("ai_llm", "crew_ai", "CrewAI multi-agent framework"),
    "Epstein": ("data_analysis", "research", "Epstein research/data analysis"),
    "AutoTagger": ("media_processing", "auto_tagging", "Automatic media tagging system"),
    "autotagger-lite": ("media_processing", "auto_tagging", "Lightweight auto tagging tool"),
    "file-tracker": ("automation", "file_management", "File tracking utility"),
    "sora-remover": ("media_processing", "video_editing", "Sora video content removal tool"),
    "mcPHooker": ("development", "mcp_protocol", "MCP (Model Context Protocol) hook implementation"),
    "mcphooker-lite": ("development", "mcp_protocol", "Lightweight MCP hook implementation"),
    "agent_forge": ("ai_llm", "agent_framework", "AI agent building framework"),
    "ai_merge_auto": ("ai_llm", "ai_merge", "AI-powered merge automation"),
    "grok": ("ai_llm", "grok_integration", "Grok AI integration"),
    "my-simple": ("automation", "simple_scripts", "Simple utility scripts"),
    "uv-demo": ("development", "uv_tool", "UV package manager demo"),
    "zombot-simple-gallery": ("media_processing", "image_gallery", "Simple image gallery viewer"),
    "Downloads/Compressed": ("misc", "archived_project", "Archived/compressed project files"),
    "Documents": ("misc", "document_files", "Document-related Python/CSV files"),
    "iterm2": ("development", "terminal_tools", "iTerm2 terminal integration scripts"),
}

# Filename pattern-based category rules
FILENAME_PATTERNS = {
    # AI/LLM patterns
    "openai": ("ai_llm", "openai_integration", "OpenAI API integration"),
    "gpt": ("ai_llm", "gpt_integration", "GPT model integration"),
    "llm": ("ai_llm", "llm_tool", "LLM-based tool"),
    "llama": ("ai_llm", "llama_model", "Llama model integration"),
    "claude": ("ai_llm", "claude_integration", "Claude AI integration"),
    "anthropic": ("ai_llm", "anthropic_api", "Anthropic API integration"),
    "groq": ("ai_llm", "groq_api", "Groq API integration"),
    "gemini": ("ai_llm", "gemini_model", "Gemini model integration"),
    "deepseek": ("ai_llm", "deepseek_model", "DeepSeek model integration"),
    "mistral": ("ai_llm", "mistral_model", "Mistral model integration"),
    "qwen": ("ai_llm", "qwen_model", "Qwen model integration"),
    "chatgpt": ("ai_llm", "chatgpt", "ChatGPT integration"),
    "transcri": ("ai_llm", "transcription", "Audio transcription tool"),
    "whisper": ("ai_llm", "whisper", "Whisper speech-to-text"),
    "deepgram": ("ai_llm", "deepgram", "Deepgram transcription"),
    "assemblyai": ("ai_llm", "assemblyai", "AssemblyAI transcription"),
    "elevenlabs": ("ai_llm", "text_to_speech", "ElevenLabs TTS"),
    "tts": ("ai_llm", "text_to_speech", "Text-to-speech tool"),
    "speech": ("ai_llm", "speech_processing", "Speech processing tool"),
    "audio": ("media_processing", "audio_processing", "Audio processing tool"),
    "leonardo": ("media_processing", "image_generation", "Leonardo AI image generation"),
    "dalle": ("media_processing", "image_generation", "DALL-E image generation"),
    "midjourney": ("media_processing", "image_generation", "Midjourney integration"),
    "image": ("media_processing", "image_processing", "Image processing tool"),
    "vision": ("ai_llm", "vision_ai", "Vision AI analysis"),
    "suno": ("media_processing", "music_generation", "Suno music generation"),
    "music": ("media_processing", "music_generation", "Music generation tool"),
    "song": ("media_processing", "music_analysis", "Song/music analysis"),

    # Media processing
    "video": ("media_processing", "video_processing", "Video processing tool"),
    "youtube": ("media_processing", "youtube", "YouTube download/processing"),
    "mp3": ("media_processing", "audio_processing", "MP3 processing"),
    "mp4": ("media_processing", "video_processing", "MP4 processing"),
    "media": ("media_processing", "media_processing", "Media processing tool"),
    "gallery": ("media_processing", "gallery", "Image gallery tool"),
    "thumbnail": ("media_processing", "image_processing", "Thumbnail generation"),
    "resize": ("media_processing", "image_processing", "Image resizing"),
    "convert": ("media_processing", "format_conversion", "Format conversion tool"),
    "background": ("media_processing", "background_removal", "Background removal tool"),
    "upscale": ("media_processing", "image_enhancement", "Image upscaling"),

    # Automation
    "automat": ("automation", "automation", "Automation tool"),
    "batch": ("automation", "batch_processing", "Batch processing tool"),
    "schedule": ("automation", "scheduling", "Scheduling tool"),
    "cron": ("automation", "scheduling", "Cron job management"),
    "workflow": ("automation", "workflow", "Workflow automation"),
    "pipeline": ("automation", "pipeline", "Data pipeline"),
    "orchestrat": ("automation", "orchestration", "Orchestration tool"),

    # Web scraping
    "scrap": ("web_scraping", "web_scraping", "Web scraping tool"),
    "crawl": ("web_scraping", "web_crawling", "Web crawling tool"),
    "fetch": ("web_scraping", "data_fetching", "Data fetching tool"),
    "selenium": ("web_scraping", "browser_automation", "Selenium browser automation"),
    "playwright": ("web_scraping", "browser_automation", "Playwright browser automation"),
    "beautifulsoup": ("web_scraping", "html_parsing", "HTML parsing with BeautifulSoup"),
    "request": ("web_scraping", "http_requests", "HTTP request handling"),

    # Business/E-commerce
    "etsy": ("ecommerce", "etsy", "Etsy listing/management"),
    "shopify": ("ecommerce", "shopify", "Shopify integration"),
    "printify": ("ecommerce", "print_on_demand", "Printify print-on-demand"),
    "product": ("ecommerce", "product_management", "Product management"),
    "listing": ("ecommerce", "listing_management", "Listing management"),
    "revenue": ("business", "revenue_tracking", "Revenue tracking"),
    "market": ("business", "market_analysis", "Market analysis"),
    "trading": ("business", "trading", "Trading tool"),
    "stock": ("business", "stock_analysis", "Stock analysis"),
    "crypto": ("business", "crypto", "Cryptocurrency tool"),
    "blockchain": ("business", "blockchain", "Blockchain tool"),
    "invoice": ("business", "invoicing", "Invoicing tool"),

    # Social media
    "instagram": ("social_media", "instagram", "Instagram automation/management"),
    "twitter": ("social_media", "twitter", "Twitter/X automation"),
    "tiktok": ("social_media", "tiktok", "TikTok automation"),
    "reddit": ("social_media", "reddit", "Reddit automation/analysis"),
    "social": ("social_media", "social_media", "Social media tool"),
    "content": ("social_media", "content_creation", "Content creation tool"),
    "shorts": ("social_media", "youtube_shorts", "YouTube Shorts creation"),
    "podcast": ("social_media", "podcast", "Podcast production"),

    # Data analysis
    "analyz": ("data_analysis", "data_analysis", "Data analysis tool"),
    "analysis": ("data_analysis", "data_analysis", "Data analysis tool"),
    "report": ("data_analysis", "reporting", "Report generation"),
    "dashboard": ("data_analysis", "dashboard", "Dashboard tool"),
    "chart": ("data_analysis", "visualization", "Chart/visualization"),
    "plot": ("data_analysis", "visualization", "Plotting tool"),
    "statistic": ("data_analysis", "statistics", "Statistical analysis"),
    "pandas": ("data_analysis", "data_manipulation", "Pandas data manipulation"),
    "numpy": ("data_analysis", "numerical_computing", "NumPy numerical computing"),
    "dataframe": ("data_analysis", "data_manipulation", "DataFrame operations"),
    "csv": ("data_analysis", "csv_processing", "CSV file processing"),

    # Development tools
    "test": ("development", "testing", "Testing code"),
    "config": ("development", "configuration", "Configuration management"),
    "setup": ("development", "setup", "Project setup"),
    "deploy": ("development", "deployment", "Deployment tool"),
    "docker": ("development", "containerization", "Docker containerization"),
    "ci": ("development", "ci_cd", "CI/CD pipeline"),
    "git": ("development", "git_tools", "Git integration tool"),
    "lint": ("development", "code_quality", "Code linting"),
    "format": ("development", "code_formatting", "Code formatting"),
    "debug": ("development", "debugging", "Debugging tool"),
    "profile": ("development", "profiling", "Performance profiling"),
    "benchmark": ("development", "benchmarking", "Benchmarking tool"),

    # File management
    "rename": ("file_management", "file_renaming", "File renaming tool"),
    "organize": ("file_management", "file_organization", "File organization"),
    "dedup": ("file_management", "deduplication", "File deduplication"),
    "backup": ("file_management", "backup", "Backup tool"),
    "sync": ("file_management", "file_sync", "File synchronization"),
    "clean": ("file_management", "cleanup", "File cleanup"),
    "move": ("file_management", "file_management", "File moving tool"),
    "copy": ("file_management", "file_management", "File copying tool"),
    "sort": ("file_management", "file_sorting", "File sorting tool"),
    "filter": ("file_management", "file_filtering", "File filtering tool"),

    # API/Integration
    "api": ("api_integration", "api", "API integration"),
    "webhook": ("api_integration", "webhook", "Webhook handler"),
    "rest": ("api_integration", "rest_api", "REST API tool"),
    "graphql": ("api_integration", "graphql", "GraphQL integration"),
    "aws": ("cloud", "aws", "AWS integration"),
    "gcp": ("cloud", "gcp", "Google Cloud integration"),
    "azure": ("cloud", "azure", "Azure integration"),
    "cloud": ("cloud", "cloud_service", "Cloud service integration"),

    # Security
    "auth": ("security", "authentication", "Authentication tool"),
    "encrypt": ("security", "encryption", "Encryption tool"),
    "password": ("security", "password_management", "Password management"),
    "security": ("security", "security", "Security tool"),
    "scan": ("security", "scanning", "Security scanning"),

    # Documentation
    "doc": ("documentation", "documentation", "Documentation tool"),
    "readme": ("documentation", "readme", "README generation"),
    "wiki": ("documentation", "wiki", "Wiki generation"),

    # Utility
    "util": ("utility", "utility", "Utility function"),
    "helper": ("utility", "helper", "Helper function"),
    "common": ("utility", "common", "Common/shared code"),
    "base": ("utility", "base_classes", "Base classes"),
    "model": ("utility", "data_models", "Data models"),
    "schema": ("utility", "data_schema", "Data schema"),
}

# Directories to exclude (dependency/system files)
EXCLUDE_DIRS = {
    '.venv', '.venv_dev', 'node_modules', '.cache', 'site-packages',
    'Library', '.vscode', 'google-cloud-sdk', '.npm', '.nvm', '.cargo',
    '.rustup', '__pycache__', '.git', 'dist', 'build', 'egg-info',
    '.mypy_cache', '.pytest_cache', '.tox', '.eggs',
}

# Files that are likely not user-created (generic names in framework dirs)
GENERIC_FRAMEWORK_FILES = {
    '__init__.py', 'setup.py', 'conftest.py', 'constants.py', 'config.py',
    'exceptions.py', 'models.py', 'schemas.py', 'utils.py', 'helpers.py',
    'base.py', 'types.py', 'typing.py', 'version.py',
}


def get_category_from_path(filepath):
    """Determine category based on file path and name."""
    filepath_lower = filepath.lower()
    filename_lower = os.path.basename(filepath).lower()
    filename_no_ext = os.path.splitext(filename_lower)[0].lower()

    # Check directory-based rules first
    for dir_pattern, (category, subcategory, description) in CATEGORY_RULES.items():
        if dir_pattern.lower() in filepath_lower:
            # For framework test files, mark as lower value
            if 'test' in filepath_lower and 'axolotl' in filepath_lower:
                return ("development", "testing", "Framework test file")
            if 'src/axolotl' in filepath_lower or 'src/setuptools' in filepath_lower:
                return ("ai_llm", "llm_framework", "Axolotl framework source code")
            return (category, subcategory, description)

    # Check filename patterns
    for pattern, (category, subcategory, description) in FILENAME_PATTERNS.items():
        if pattern in filename_no_ext or pattern in filename_lower:
            return (category, subcategory, description)

    # Default categorization based on file extension
    if filepath_lower.endswith('.csv'):
        return ("data_analysis", "csv_data", "CSV data file")

    # Generic Python file
    return ("development", "python_module", "Python module/script")


def estimate_value(category, subcategory, filepath, file_size_kb):
    """Estimate the marketplace value of a file/project."""
    filepath_lower = filepath.lower()

    # High-value categories
    high_value_patterns = [
        ('ai_llm', 'llm_training_framework', '$5000-$15000'),
        ('ai_llm', 'multi_purpose_ai', '$2000-$8000'),
        ('ai_llm', 'agent_framework', '$3000-$10000'),
        ('automation', 'orchestration', '$1500-$5000'),
        ('ecommerce', 'etsy', '$500-$2000'),
        ('ecommerce', 'print_on_demand', '$500-$2000'),
        ('media_processing', 'image_generation', '$1000-$4000'),
        ('media_processing', 'video_processing', '$1000-$3000'),
        ('media_processing', 'youtube', '$500-$2000'),
        ('social_media', 'instagram', '$500-$2000'),
        ('social_media', 'content_creation', '$500-$2000'),
        ('business', 'market_analysis', '$1000-$5000'),
        ('business', 'trading', '$1000-$5000'),
        ('web_scraping', 'web_scraping', '$500-$3000'),
        ('api_integration', 'api', '$300-$1500'),
        ('development', 'mcp_protocol', '$1000-$4000'),
        ('ai_llm', 'transcription', '$500-$2000'),
        ('ai_llm', 'text_to_speech', '$500-$2000'),
        ('media_processing', 'auto_tagging', '$500-$2000'),
        ('file_management', 'file_renaming', '$200-$800'),
        ('file_management', 'file_organization', '$200-$800'),
        ('ai_llm', 'crew_ai', '$1000-$4000'),
        ('ai_llm', 'llm_framework', '$3000-$10000'),
    ]

    for cat, sub, value in high_value_patterns:
        if category == cat and subcategory == sub:
            return value

    # Medium value
    medium_value_patterns = [
        ('ai_llm', '$300-$1500'),
        ('automation', '$200-$1000'),
        ('media_processing', '$200-$1000'),
        ('ecommerce', '$200-$1000'),
        ('business', '$200-$1000'),
        ('web_scraping', '$200-$1000'),
        ('social_media', '$200-$800'),
        ('data_analysis', '$100-$500'),
        ('api_integration', '$100-$500'),
        ('development', '$100-$500'),
        ('file_management', '$100-$500'),
        ('cloud', '$100-$500'),
    ]

    for cat, value in medium_value_patterns:
        if category == cat:
            return value

    # Low value for test files, generic utilities
    if 'test' in filepath_lower:
        return "$50-$200"
    if file_size_kb < 5:
        return "$50-$200"

    return "$100-$500"


def is_marketplace_ready(category, subcategory, filepath, file_size_kb):
    """Determine if a file is ready for marketplace sale."""
    filepath_lower = filepath.lower()
    filename = os.path.basename(filepath).lower()

    # Not ready: test files, very small files, generic framework internals
    if 'test' in filepath_lower and '/tests/' in filepath_lower:
        return "no"
    if file_size_kb < 1:
        return "no"
    if filename in GENERIC_FRAMEWORK_FILES and 'src/' in filepath_lower:
        return "no"
    if '__pycache__' in filepath_lower:
        return "no"

    # Ready: standalone scripts, complete projects
    ready_categories = {
        'ai_llm', 'automation', 'media_processing', 'ecommerce',
        'business', 'web_scraping', 'social_media', 'api_integration',
        'development', 'file_management', 'cloud', 'data_analysis'
    }

    if category in ready_categories and file_size_kb >= 2:
        return "yes"

    return "no"


def get_project_name(filepath):
    """Extract project name from file path."""
    parts = filepath.split('/')
    # Find the project-level directory
    for i, part in enumerate(parts):
        if part == 'pythons' and i + 2 < len(parts):
            return parts[i + 2]  # projects/<project_name>/
        if part == 'github' and i + 1 < len(parts):
            return parts[i + 1]
        if part in ['MasterxEo', 'MarketMaster', 'AutoTagger', 'mcPHooker',
                     'agent_forge', 'ai_merge_auto', 'zombot-simple-gallery',
                     'my_crew', 'Epstein', 'Development', 'scripts', 'grok',
                     'my-simple', 'uv-demo', 'autotagger-lite', 'file-tracker',
                     'sora-remover', 'mcphooker-lite', 'agent_forge']:
            return part
    return parts[-2] if len(parts) > 1 else 'unknown'


def get_file_metadata(filepath):
    """Get file size and modification date."""
    try:
        st = os.stat(filepath)
        size_kb = round(st.st_size / 1024, 1)
        mtime = datetime.datetime.fromtimestamp(st.st_mtime)
        return size_kb, mtime.strftime('%Y-%m-%d %H:%M:%S')
    except (OSError, FileNotFoundError):
        return 0, 'unknown'


def collect_all_files():
    """Read all file lists from temp files."""
    all_files = []
    for temp_file in TEMP_FILES:
        if os.path.exists(temp_file):
            with open(temp_file, 'r') as f:
                for line in f:
                    filepath = line.strip()
                    if filepath and os.path.exists(filepath):
                        all_files.append(filepath)
    return all_files


def filter_user_created_files(all_files):
    """Filter out likely dependency/framework files, keeping user-created ones."""
    filtered = []
    for filepath in all_files:
        filepath_lower = filepath.lower()

        # Skip deep framework test files (but keep user test files)
        if '/tests/' in filepath_lower and ('axolotl' in filepath_lower or 'framework' in filepath_lower):
            # Still include some framework files but mark them
            pass

        # Skip __pycache__
        if '__pycache__' in filepath_lower:
            continue

        # Skip .git directories
        if '/.git/' in filepath_lower:
            continue

        filtered.append(filepath)

    return filtered


def generate_inventory():
    """Main function to generate the inventory."""
    print("Collecting all files...")
    all_files = collect_all_files()
    print(f"Found {len(all_files)} total files")

    print("Filtering user-created files...")
    user_files = filter_user_created_files(all_files)
    print(f"Filtered to {len(user_files)} user-created files")

    # Process files
    inventory = []
    category_counts = defaultdict(int)
    category_files = defaultdict(list)

    print("Processing files and collecting metadata...")
    for i, filepath in enumerate(user_files):
        if i % 1000 == 0:
            print(f"  Processing file {i}/{len(user_files)}...")

        filename = os.path.basename(filepath)
        file_size_kb, last_modified = get_file_metadata(filepath)
        category, subcategory, description = get_category_from_path(filepath)
        project = get_project_name(filepath)
        value_range = estimate_value(category, subcategory, filepath, file_size_kb)
        marketplace_ready = is_marketplace_ready(category, subcategory, filepath, file_size_kb)

        inventory.append({
            'file_name': filename,
            'full_path': filepath,
            'file_size_kb': file_size_kb,
            'last_modified': last_modified,
            'category': category,
            'subcategory': subcategory,
            'description': description,
            'project': project,
            'marketplace_ready': marketplace_ready,
            'estimated_value_range': value_range,
        })

        category_counts[category] += 1
        if marketplace_ready == "yes":
            category_files[category].append({
                'path': filepath,
                'value': value_range,
                'size': file_size_kb,
            })

    # Sort inventory by estimated value (high to low)
    value_order = {
        '$5000-$15000': 0, '$3000-$10000': 1, '$2000-$8000': 2,
        '$1500-$5000': 3, '$1000-$5000': 4, '$1000-$4000': 5,
        '$1000-$3000': 6, '$500-$3000': 7, '$500-$2000': 8,
        '$300-$1500': 9, '$200-$1000': 10, '$200-$800': 11,
        '$100-$500': 12, '$50-$200': 13,
    }

    inventory.sort(key=lambda x: value_order.get(x['estimated_value_range'], 99))

    # Write CSV
    csv_path = '/Users/steven/python-marketplace-inventory/marketplace_inventory.csv'
    print(f"\nWriting CSV to {csv_path}...")

    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'file_name', 'full_path', 'file_size_kb', 'last_modified',
            'category', 'subcategory', 'description', 'marketplace_ready',
            'estimated_value_range'
        ])
        writer.writeheader()
        for item in inventory:
            writer.writerow({k: item[k] for k in [
                'file_name', 'full_path', 'file_size_kb', 'last_modified',
                'category', 'subcategory', 'description', 'marketplace_ready',
                'estimated_value_range'
            ]})

    print(f"CSV written with {len(inventory)} entries")

    # Generate summary
    generate_summary(inventory, category_counts, category_files)

    return inventory, category_counts


def generate_summary(inventory, category_counts, category_files):
    """Generate the Markdown summary report."""
    total_files = len(inventory)
    py_files = sum(1 for f in inventory if f['full_path'].endswith('.py'))
    csv_files = sum(1 for f in inventory if f['full_path'].endswith('.csv'))
    ready_files = sum(1 for f in inventory if f['marketplace_ready'] == 'yes')

    # Top projects by value (placeholder for future use)
    _top_projects = []
    project_values = defaultdict(lambda: {'count': 0, 'files': [], 'categories': set()})
    for item in inventory:
        if item['marketplace_ready'] == 'yes':
            proj = item['project']
            project_values[proj]['count'] += 1
            project_values[proj]['files'].append(item)
            project_values[proj]['categories'].add(item['category'])

    # Sort projects by file count (proxy for project size/value)
    sorted_projects = sorted(project_values.items(), key=lambda x: x[1]['count'], reverse=True)

    # Category breakdown
    category_breakdown = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)

    # Ready files by category
    ready_by_category = defaultdict(int)
    for item in inventory:
        if item['marketplace_ready'] == 'yes':
            ready_by_category[item['category']] += 1

    summary_path = '/Users/steven/python-marketplace-inventory/MARKETPLACE_SUMMARY.md'
    print(f"Writing summary to {summary_path}...")

    with open(summary_path, 'w') as f:
        f.write("# Python & CSV Marketplace Inventory Summary\n\n")
        f.write(f"**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## Overview\n\n")
        f.write("| Metric | Count |\n")
        f.write("|--------|-------|\n")
        f.write(f"| **Total Files** | {total_files:,} |\n")
        f.write(f"| **Python Files (.py)** | {py_files:,} |\n")
        f.write(f"| **CSV Files (.csv)** | {csv_files:,} |\n")
        f.write(f"| **Marketplace Ready** | {ready_files:,} |\n")
        f.write("| **Directories Scanned** | 39 |\n\n")

        f.write("## Category Breakdown\n\n")
        f.write("| Category | File Count | Marketplace Ready |\n")
        f.write("|----------|-----------|--------------------|\n")
        for cat, count in category_breakdown:
            ready = ready_by_category.get(cat, 0)
            f.write(f"| {cat} | {count:,} | {ready:,} |\n")
        f.write("\n")

        f.write("## Subcategory Breakdown\n\n")
        subcategory_counts = defaultdict(int)
        for item in inventory:
            subcategory_counts[item['subcategory']] += 1
        sorted_subcats = sorted(subcategory_counts.items(), key=lambda x: x[1], reverse=True)
        f.write("| Subcategory | File Count |\n")
        f.write("|------------|-----------|\n")
        for subcat, count in sorted_subcats[:30]:
            f.write(f"| {subcat} | {count:,} |\n")
        f.write("\n")

        f.write("## Top 50 Most Valuable Projects\n\n")
        f.write("| Rank | Project | Files | Categories | Est. Value Range |\n")
        f.write("|------|---------|-------|------------|------------------|\n")
        for i, (proj, data) in enumerate(sorted_projects[:50], 1):
            cats = ', '.join(sorted(data['categories']))
            # Get value range from first file
            value_range = data['files'][0]['estimated_value_range'] if data['files'] else 'N/A'
            f.write(f"| {i} | {proj} | {data['count']} | {cats} | {value_range} |\n")
        f.write("\n")

        f.write("## Directory Source Breakdown\n\n")
        dir_counts = defaultdict(int)
        for item in inventory:
            # Extract the project-level directory from the path
            path = item['full_path']
            parts = path.split('/')
            # /Users/steven/<project>/...
            if len(parts) >= 4 and parts[2] == 'steven':
                top_dir = parts[3]
                # For pythons, get the sub-project
                if top_dir == 'pythons' and len(parts) >= 6 and parts[4] == 'projects':
                    top_dir = f"pythons/{parts[5]}"
                dir_counts[top_dir] += 1
            elif len(parts) >= 3:
                dir_counts[parts[2]] += 1
        sorted_dirs = sorted(dir_counts.items(), key=lambda x: x[1], reverse=True)
        f.write("| Directory | File Count |\n")
        f.write("|-----------|-----------|\n")
        for d, count in sorted_dirs:
            f.write(f"| {d} | {count:,} |\n")
        f.write("\n")

        f.write("## Recommended Organization Structure\n\n")
        f.write("```\n")
        f.write("python-marketplace/\n")
        f.write("├── ai-llm-tools/\n")
        f.write("│   ├── llm-training-frameworks/     # Axolotl, fine-tuning tools\n")
        f.write("│   ├── multi-purpose-ai/            # Vibrant-chaplygin toolkit\n")
        f.write("│   ├── agent-frameworks/            # CrewAI, agent_forge\n")
        f.write("│   ├── transcription-speech/        # Whisper, Deepgram, AssemblyAI\n")
        f.write("│   ├── text-to-speech/              # ElevenLabs, TTS tools\n")
        f.write("│   └── ai-integrations/             # OpenAI, Claude, Groq, etc.\n")
        f.write("├── media-processing/\n")
        f.write("│   ├── image-generation/            # Leonardo, DALL-E, Midjourney\n")
        f.write("│   ├── image-processing/            # Resize, upscale, tagging\n")
        f.write("│   ├── video-processing/            # YouTube, video editing\n")
        f.write("│   ├── audio-processing/            # Audio analysis, MP3 tools\n")
        f.write("│   └── music-generation/            # Suno, song analysis\n")
        f.write("├── automation-workflows/\n")
        f.write("│   ├── batch-processing/            # Batch tools, pipelines\n")
        f.write("│   ├── workflow-orchestration/      # Multi-step workflows\n")
        f.write("│   └── scheduling/                  # Cron, scheduled tasks\n")
        f.write("├── ecommerce-business/\n")
        f.write("│   ├── etsy-tools/                  # Etsy listing generators\n")
        f.write("│   ├── print-on-demand/             # Printify integration\n")
        f.write("│   ├── market-analysis/             # MarketMaster, trading\n")
        f.write("│   └── product-management/          # Product CSV tools\n")
        f.write("├── social-media/\n")
        f.write("│   ├── instagram/                   # Instagram automation\n")
        f.write("│   ├── content-creation/            # YouTube, shorts, podcasts\n")
        f.write("│   └── reddit/                      # Reddit analysis/automation\n")
        f.write("├── web-scraping/\n")
        f.write("│   ├── scrapers/                    # Web scraping tools\n")
        f.write("│   └── browser-automation/          # Selenium, Playwright\n")
        f.write("├── development-tools/\n")
        f.write("│   ├── mcp-protocol/                # mcPHooker implementations\n")
        f.write("│   ├── git-tools/                   # Git integrations\n")
        f.write("│   └── testing/                     # Test frameworks\n")
        f.write("├── file-management/\n")
        f.write("│   ├── file-renaming/               # Smart renamers\n")
        f.write("│   ├── file-organization/           # Organizers, dedup\n")
        f.write("│   └── gallery-viewers/             # Image galleries\n")
        f.write("├── data-analysis/\n")
        f.write("│   ├── data-processing/             # Pandas, NumPy tools\n")
        f.write("│   ├── visualization/               # Charts, dashboards\n")
        f.write("│   └── csv-data/                    # CSV data files\n")
        f.write("└── api-integrations/\n")
        f.write("    ├── cloud-services/              # AWS, GCP, Azure\n")
        f.write("    └── rest-apis/                   # API wrappers\n")
        f.write("```\n\n")

        f.write("## Next Steps\n\n")
        f.write("1. **Prioritize High-Value Projects**: Focus on AI/LLM frameworks, multi-purpose AI toolkits, and automation platforms first\n")
        f.write("2. **Clean and Document**: Add README files, requirements.txt, and usage examples to top projects\n")
        f.write("3. **Package for Sale**: Create clean ZIP archives with documentation for marketplace listings\n")
        f.write("4. **Test and Validate**: Ensure all marketplace-ready scripts run correctly\n")
        f.write("5. **Price Strategically**: Use estimated value ranges as starting points, adjust based on market demand\n")
        f.write("6. **List on Marketplaces**: Consider Gumroad, CodeCanyon, GitHub Sponsors, or direct sales\n")

    print(f"Summary written to {summary_path}")


if __name__ == '__main__':
    inventory, category_counts = generate_inventory()
    print(f"\nDone! Processed {len(inventory)} files across {len(category_counts)} categories.")
    print("CSV: /Users/steven/python-marketplace-inventory/marketplace_inventory.csv")
    print("Summary: /Users/steven/python-marketplace-inventory/MARKETPLACE_SUMMARY.md")
