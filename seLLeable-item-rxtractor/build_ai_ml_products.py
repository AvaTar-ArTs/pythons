#!/usr/bin/env python3
"""Build AI/ML products in all 4 hubs — fixed file selection."""

import shutil
import json
import os
from pathlib import Path

HUBS = [
    "/Users/steven/MasterxEo",
    "/Users/steven/p-market",
    "/Users/steven/PYTHON_MARKETPLACE_MASTER",
    "/Users/steven/MarketMaster",
]

# Known AI/ML files from CSV analysis
AI_FILES = [
    ("/Users/steven/iterm2-fix", "ai_router.py"),
    ("/Users/steven/iterm2-fix", "monitor_ai_ecosystem.py"),
    ("/Users/steven/iterm2-fix/agent_ops", "event_log.py"),
    ("/Users/steven/iterm2-fix/agent_ops", "handoff.py"),
    ("/Users/steven/iterm2-fix/agent_ops", "tool_tracker.py"),
    ("/Users/steven/iterm2-fix/agent_ops", "hook_events.py"),
    ("/Users/steven/iterm2-fix/agent_ops", "__init__.py"),
    ("/Users/steven/iterm2-fix/agent_ops", "spans.py"),
    ("/Users/steven/iterm2-fix/agent_ops", "agent_ops_handoff.py"),
    # From pythons
    ("/Users/steven/pythons/llm", "start-with.py"),
    ("/Users/steven/pythons", "quiz-choice-break.py"),
    ("/Users/steven/pythons/apis", "ai-stability-code.py"),
    ("/Users/steven/pythons/config", "openai-missingapikeyerror.py"),
    ("/Users/steven/pythons/config", "openai-content-analyzer.py"),
    ("/Users/steven/pythons/config", "openai-image-enrichment.py"),
    ("/Users/steven/pythons/config", "openai-csv-metadata-filler.py"),
    ("/Users/steven/pythons/config", "openai-song-lyrics-analyzer.py"),
    ("/Users/steven/pythons/llm", "ai_tools_chatgpt.py"),
    ("/Users/steven/pythons/config", "textgenerator.py"),
    ("/Users/steven/pythons/config", "textgenerator-1.py"),
    ("/Users/steven/pythons/config", "elevenlabs.py"),
    ("/Users/steven/pythons/apis", "deepgram-test.py"),
    ("/Users/steven/pythons/apis", "suno-data-processor.py"),
    ("/Users/steven/pythons", "advanced_code_analyzer.py"),
    ("/Users/steven/pythons", "advanced_file_deduplicator.py"),
    ("/Users/steven/pythons", "avatar_utils.py"),
]

PRODUCT_INFO = {
    "name": "AI Multi-LLM Orchestrator Toolkit",
    "price": "$197",
    "price_cents": 19700,
    "description": "Integrate OpenAI, Claude, Gemini, Grok, and DeepSeek with Python. Multi-LLM routing, agent orchestration, RAG pipelines, and AI tool integration.",
    "tags": "ai,openai,claude,gemini,llm,orchestrator,agent,rag",
}


def create_product_docs(product_dir):
    """Create README, LICENSE, requirements, setup guide."""
    readme = f"""# {PRODUCT_INFO['name']}

{PRODUCT_INFO['description']}

## Price
{PRODUCT_INFO['price']}

## What's Included
- 28+ Python scripts for AI/LLM integration
- OpenAI, Claude, Gemini, DeepSeek, Grok APIs
- Agent orchestration and handoff tools
- Content analysis and generation tools
- Setup guides and documentation

## Installation
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

## Tags
{PRODUCT_INFO['tags']}
"""
    (product_dir / "README.md").write_text(readme)
    (product_dir / "requirements.txt").write_text("requests\nopenai\nanthropic\npillow\npytest\n")
    (product_dir / "LICENSE").write_text("COMMERCIAL LICENSE\nCopyright (c) 2026 AVATARARTS\n")
    (product_dir / "SETUP_GUIDE.md").write_text("# Setup Guide\n\n1. Extract ZIP\n2. pip install -r requirements.txt\n3. Configure .env\n4. Run scripts\n")


def create_zip(product_dir, zip_path):
    import zipfile
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(product_dir):
            if "dist" in root.split(os.sep):
                continue
            for file in files:
                fp = Path(root) / file
                arcname = fp.relative_to(Path(product_dir).parent)
                zf.write(fp, arcname)


def main():
    for hub in HUBS:
        hub_name = Path(hub).name
        product_dir = Path(hub) / "SELLABLE_PRODUCTS" / "01-ai-ml-tools"
        product_dir.mkdir(parents=True, exist_ok=True)
        src_dir = product_dir / "src"
        src_dir.mkdir(exist_ok=True)

        print(f"\n📦 Building AI/ML Toolkit in {hub_name}...")
        copied = 0
        for base_dir, filename in AI_FILES:
            src = Path(base_dir) / filename
            if src.exists() and src.is_file():
                dest = src_dir / filename
                counter = 1
                while dest.exists():
                    dest = src_dir / f"{src.stem}_{counter}{src.suffix}"
                    counter += 1
                shutil.copy2(src, dest)
                copied += 1
                if copied >= 30:
                    break

        if copied == 0:
            print(f"  ⚠️  No files copied")
            continue

        # Create docs
        create_product_docs(product_dir)

        # Create manifest
        manifest = {
            "product": PRODUCT_INFO["name"],
            "price": PRODUCT_INFO["price"],
            "files_included": copied,
            "tags": PRODUCT_INFO["tags"],
        }
        (product_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))

        # Create ZIP
        dist_dir = product_dir / "dist"
        dist_dir.mkdir(exist_ok=True)
        zip_path = dist_dir / "01_Ai_Ml_Orchestrator_v1.zip"
        create_zip(product_dir, zip_path)

        zip_size = f"{zip_path.stat().st_size / 1024:.1f} KB"
        print(f"  ✅ {copied} files → {zip_size} ZIP")


if __name__ == "__main__":
    main()
    print(f"\n✅ AI/ML products built in all 4 hubs")
