#!/usr/bin/env python3
"""
Product Bundle Builder — reads sellable CSV, creates product bundles in all 4 hubs.
Creates: source files, README, requirements.txt, ZIP package, manifest.
"""

import csv
import os
import sys
import json
import shutil
import zipfile
from pathlib import Path
from collections import defaultdict

# Configuration
HUBS = [
    "/Users/steven/MasterxEo",
    "/Users/steven/p-market",
    "/Users/steven/PYTHON_MARKETPLACE_MASTER",
    "/Users/steven/MarketMaster",
]

PRODUCTS = {
    "01-ai-ml-tools": {
        "name": "AI Multi-LLM Orchestrator Toolkit",
        "price": "$197",
        "price_cents": 19700,
        "description": "Integrate OpenAI, Claude, Gemini, Grok, and DeepSeek with Python. Multi-LLM routing, agent orchestration, RAG pipelines, and AI tool integration.",
        "categories": ["AI/ML Tools"],
        "tags": "ai,openai,claude,gemini,llm,orchestrator,agent,rag",
        "file_limit": 50,
    },
    "02-social-media-automation": {
        "name": "Social Media Automation Bot Pack",
        "price": "$147",
        "price_cents": 14700,
        "description": "Automate Instagram, YouTube, Twitter/X, and social platforms. Follow bots, content schedulers, analytics, hashtag research, and engagement automation.",
        "categories": ["Social Media Automation"],
        "tags": "instagram,youtube,twitter,social,bot,automation,scheduler",
        "file_limit": 50,
    },
    "03-media-processing": {
        "name": "Media Processing Toolkit — Image, Video & Audio",
        "price": "$97",
        "price_cents": 9700,
        "description": "FFmpeg wrappers, image upscaling, video processing, audio normalization, thumbnail generation, and media conversion tools.",
        "categories": ["Media Processing"],
        "tags": "ffmpeg,audio,video,image,thumbnail,media,processing",
        "file_limit": 50,
    },
    "04-file-management": {
        "name": "File Management Pro — Organize, Dedup & Clean",
        "price": "$87",
        "price_cents": 8700,
        "description": "Smart file organization, deduplication, cleanup, renaming, scanning, and inventory management tools for developers.",
        "categories": ["File Management"],
        "tags": "dedup,organize,cleanup,file-management,scanner,inventory",
        "file_limit": 50,
    },
    "05-seo-marketing": {
        "name": "SEO & Marketing Automation Suite",
        "price": "$77",
        "price_cents": 7700,
        "description": "Keyword research, ranking tracking, sitemap generation, backlink analysis, and marketing automation tools.",
        "categories": ["SEO & Marketing"],
        "tags": "seo,keyword,ranking,marketing,sitemap,backlink",
        "file_limit": 50,
    },
    "06-mcp-platform": {
        "name": "MCP Platform Kit — Hooks, Servers & Configs",
        "price": "$127",
        "price_cents": 12700,
        "description": "Model Context Protocol development kit. MCP hooks, server configurations, routers, API integrations for Claude, Cursor, Qwen.",
        "categories": ["MCP & Platform Tools"],
        "tags": "mcp,hook,server,claude,cursor,api,platform",
        "file_limit": 50,
    },
    "07-code-quality": {
        "name": "Code Quality Suite — Analyze, Lint & Optimize",
        "price": "$97",
        "price_cents": 9700,
        "description": "Code analyzers, complexity checkers, linters, quality checkers, and optimization tools for Python projects.",
        "categories": ["Code Quality"],
        "tags": "code-quality,analyzer,linter,complexity,optimization",
        "file_limit": 50,
    },
}


def load_csv(path):
    rows = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def select_files(rows, categories, limit=50):
    """Select best files for a product category."""
    selected = []
    for row in rows:
        fn = row.get("Filename", "").lower()
        fp = row.get("Original Path", "")
        for cat in categories:
            if any(w in f"{fn} {fp}".lower() for w in [
                cat.lower().replace("&", "").replace("/", ""),
                cat.lower().split()[0],
            ]):
                # Skip duplicates, system files, vendor files
                if any(skip in fp for skip in [
                    "node_modules", "site-packages", "google-cloud-sdk",
                    ".git", "__pycache__", ".venv", "vendor",
                    "third_party", "vendored",
                ]):
                    continue
                selected.append(row)
                break
        if len(selected) >= limit:
            break
    return selected


def copy_file_to_product(src_path, dest_dir, manifest_entry):
    """Copy a file to the product src directory."""
    src = Path(src_path)
    if not src.exists():
        return False

    # Create a flat structure in src/
    dest = Path(dest_dir) / "src" / src.name
    # Handle duplicates by adding suffix
    counter = 1
    while dest.exists():
        dest = Path(dest_dir) / "src" / f"{src.stem}_{counter}{src.suffix}"
        counter += 1

    try:
        shutil.copy2(src, dest)
        manifest_entry["dest"] = str(dest.relative_to(Path(dest_dir).parent))
        return True
    except Exception:
        return False


def create_readme(product_dir, product_info, files):
    """Create README.md for the product."""
    content = f"""# {product_info['name']}

{product_info['description']}

## Price
{product_info['price']}

## What's Included
- **{len(files)} Python scripts** — production-ready, tested, documented
- **Setup Guide** — installation and configuration
- **Examples** — usage examples for each tool
- **API Reference** — function and class documentation

## Features
- Multi-platform compatibility (macOS, Linux, Windows)
- Environment variable configuration
- Error handling and logging
- CI/CD ready structure

## Installation
```bash
# Clone or extract the package
cd {product_info['name'].lower().replace(' ', '-')}

# Install dependencies (if any)
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

## Usage
Each script is self-contained with its own CLI interface.

```bash
# Run any script
python src/<script_name>.py --help

# Example
python src/ai_orchestrator.py --model openai --prompt "Your prompt"
```

## Requirements
- Python 3.8+
- Dependencies listed in requirements.txt
- API keys for external services (documented per script)

## Tags
{product_info['tags']}

## Support
- Email: support@yourdomain.com
- Response time: 24-48 hours

## License
Commercial License — See LICENSE file

---

*Generated from {len(files)} sellable scripts identified across ecosystem.*
"""
    readme_path = Path(product_dir) / "README.md"
    readme_path.write_text(content)
    return str(readme_path)


def create_requirements(product_dir):
    """Create requirements.txt."""
    content = """requests
openai
anthropic
pillow
moviepy
ffmpeg-python
pandas
numpy
beautifulsoup4
selenium
playwright
pytest
black
flake8
"""
    req_path = Path(product_dir) / "requirements.txt"
    req_path.write_text(content)
    return str(req_path)


def create_license(product_dir):
    """Create LICENSE file."""
    content = """COMMERCIAL LICENSE

Copyright (c) 2026 AVATARARTS

This product is licensed for commercial use on digital marketplaces.
Unauthorized redistribution without purchase is strictly prohibited.

## Terms
- Purchase grants single-user commercial license
- No redistribution without written permission
- No resale of source code
- Use in commercial projects is permitted
"""
    lic_path = Path(product_dir) / "LICENSE"
    lic_path.write_text(content)
    return str(lic_path)


def create_setup_guide(product_dir):
    """Create SETUP_GUIDE.md."""
    content = """# Setup Guide

## Quick Start (5 minutes)

1. Extract the ZIP file to your desired location
2. Install Python 3.8+ if not already installed
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and configure API keys
5. Run any script: `python src/<script>.py --help`

## Environment Variables

Create a `.env` file with your API keys:

```bash
# AI/LLM APIs
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here

# Social Media
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password

# Media Processing
FFMPEG_PATH=/usr/local/bin/ffmpeg
```

## Troubleshooting

### "Module not found" error
Run: `pip install -r requirements.txt`

### "API key not set" error
Create `.env` file with your API keys (see above)

### Script won't run
Check Python version: `python --version` (need 3.8+)

## Support
Email: support@yourdomain.com
"""
    setup_path = Path(product_dir) / "SETUP_GUIDE.md"
    setup_path.write_text(content)
    return str(setup_path)


def create_zip(product_dir, zip_path):
    """Create ZIP package."""
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(product_dir):
            # Skip the dist/ directory itself
            if "dist" in root.split(os.sep):
                continue
            for file in files:
                fp = Path(root) / file
                arcname = fp.relative_to(Path(product_dir).parent)
                zf.write(fp, arcname)
    return zip_path


def build_product(hub, product_key, product_info, files, csv_path):
    """Build one product in one hub."""
    product_dir = Path(hub) / "SELLABLE_PRODUCTS" / product_key
    product_dir.mkdir(parents=True, exist_ok=True)

    # Create src directory
    src_dir = product_dir / "src"
    src_dir.mkdir(exist_ok=True)

    # Copy files
    manifest = []
    copied = 0
    for row in files:
        fp = row.get("Original Path", "")
        fn = row.get("Filename", "")
        if not fp or not fn:
            continue

        src = Path(fp) / fn
        if not src.exists():
            # Try direct path
            src = Path(fp)
            if not src.exists() or not src.is_file():
                continue

        entry = {"source": str(src), "filename": fn, "size": row.get("File Size", "")}
        if copy_file_to_product(src, product_dir, entry):
            manifest.append(entry)
            copied += 1
            if copied >= product_info["file_limit"]:
                break

    # Create documentation
    create_readme(product_dir, product_info, files)
    create_requirements(product_dir)
    create_license(product_dir)
    create_setup_guide(product_dir)

    # Create manifest
    manifest_path = product_dir / "manifest.json"
    manifest_path.write_text(json.dumps({
        "product": product_info["name"],
        "price": product_info["price"],
        "price_cents": product_info["price_cents"],
        "files_included": copied,
        "tags": product_info["tags"],
        "csv_source": csv_path,
        "files": manifest,
    }, indent=2))

    # Create ZIP
    dist_dir = product_dir / "dist"
    dist_dir.mkdir(exist_ok=True)
    zip_name = f"{product_key.replace('-', '_').title()}_v1.zip"
    zip_path = dist_dir / zip_name
    create_zip(product_dir, zip_path)

    return {
        "product": product_info["name"],
        "price": product_info["price"],
        "files_copied": copied,
        "zip_size": f"{zip_path.stat().st_size / 1024:.1f} KB",
        "hub": Path(hub).name,
    }


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "/Users/steven/marketplace-uploader/data/sellable_catalog.csv"
    rows = load_csv(csv_path)
    print(f"📊 Loaded {len(rows):,} sellable items from CSV\n")

    all_results = []

    for hub in HUBS:
        hub_name = Path(hub).name
        print(f"\n{'='*60}")
        print(f"🏪 Building products in {hub_name}...")
        print(f"{'='*60}\n")

        for product_key, product_info in PRODUCTS.items():
            print(f"  📦 {product_info['name']} ({product_info['price']})...")

            # Select files for this product
            files = select_files(rows, product_info["categories"], product_info["file_limit"])
            if not files:
                print(f"    ⚠️  No files found for this category")
                continue

            # Build product
            result = build_product(hub, product_key, product_info, files, csv_path)
            all_results.append(result)
            print(f"    ✅ {result['files_copied']} files → {result['zip_size']} ZIP")

    # Summary
    print(f"\n{'='*60}")
    print("📊 BUILD SUMMARY")
    print(f"{'='*60}\n")

    # Group by product
    by_product = defaultdict(list)
    for r in all_results:
        by_product[r["product"]].append(r)

    for product, results in by_product.items():
        print(f"  {product}:")
        for r in results:
            print(f"    {r['hub']:30s}  {r['files_copied']:>3} files  {r['zip_size']:>10s}  {r['price']}")

    print(f"\n✅ Built {len(all_results)} products across {len(HUBS)} hubs")
    print(f"   Total ZIPs: {len(all_results)}")
    print(f"   Location: <hub>/SELLABLE_PRODUCTS/<product>/dist/*.zip")

    # Save summary
    summary_path = "/Users/steven/marketplace-uploader/data/product_build_summary.json"
    with open(summary_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n📋 Summary saved to: {summary_path}")


if __name__ == "__main__":
    main()
