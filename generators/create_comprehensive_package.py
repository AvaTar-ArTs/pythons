#!/usr/bin/env python3
"""
Create comprehensive Python scripts marketplace package.
Organizes, documents, and prepares all user-created scripts for selling.
"""

import csv
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ============================================================
# Configuration
# ============================================================

SOURCE_CSV = "/Users/steven/python-marketplace-inventory/YOUR_PYTHON_SCRIPTS.csv"
TOP_CSV = "/Users/steven/python-marketplace-inventory/TOP_MARKETABLE_SCRIPTS.csv"
OUTPUT_BASE = "/Users/steven/PYTHON_MARKETPLACE_EMPIRE"

# ============================================================
# Directory Structure to Create
# ============================================================

FOLDER_STRUCTURE = {
    "01_AI_LLM_TOOLS": {
        "description": "AI and LLM-powered tools, agents, and frameworks",
        "subcategories": [
            "ai_agents",
            "llm_orchestration",
            "content_generation",
            "voice_speech",
            "fine_tuning",
            "chatbots",
            "multi_llm_systems",
        ]
    },
    "02_AUTOMATION_BOTS": {
        "description": "Social media automation, web scrapers, and bots",
        "subcategories": [
            "instagram_automation",
            "youtube_automation",
            "tiktok_automation",
            "twitter_automation",
            "web_scrapers",
            "data_extractors",
        ]
    },
    "03_MEDIA_PROCESSING": {
        "description": "Audio, video, and image processing tools",
        "subcategories": [
            "audio_transcription",
            "video_editing",
            "image_processing",
            "image_upscaling",
            "gallery_systems",
        ]
    },
    "04_BUSINESS_TOOLS": {
        "description": "CRM, analytics, dashboards, and business intelligence",
        "subcategories": [
            "crm_systems",
            "analytics_dashboards",
            "lead_generation",
            "revenue_tracking",
            "reporting_tools",
        ]
    },
    "05_WEB_DEVELOPMENT": {
        "description": "Web applications, APIs, and website tools",
        "subcategories": [
            "web_apps",
            "api_services",
            "website_generators",
            "ecommerce_tools",
        ]
    },
    "06_DATA_ANALYSIS": {
        "description": "Data processing, CSV tools, and analysis scripts",
        "subcategories": [
            "csv_tools",
            "data_cleaners",
            "analysis_engines",
            "file_organizers",
        ]
    },
    "07_MARKETING_SEO": {
        "description": "SEO tools, content analyzers, and marketing automation",
        "subcategories": [
            "seo_tools",
            "content_analyzers",
            "marketing_automation",
            "social_media_tools",
        ]
    },
    "08_UTILITIES_SCRIPTS": {
        "description": "System utilities, file organizers, and automation scripts",
        "subcategories": [
            "file_utilities",
            "system_tools",
            "converters",
            "batch_processors",
        ]
    },
    "DOCUMENTATION": {
        "description": "Complete documentation, guides, and marketing materials",
        "subcategories": []
    },
    "MARKETPLACE_LISTINGS": {
        "description": "Ready-to-use listings for Upwork, Fiverr, Gumroad",
        "subcategories": []
    },
}

# ============================================================
# Categorization Logic
# ============================================================

def categorize_script(filepath: str, filename: str, category: str, description: str) -> tuple:
    """
    Determine the best category and subcategory for a script.
    Returns: (main_category, subcategory)
    """
    
    text = f"{filepath} {filename} {description}".lower()
    
    # AI/LLM Tools
    if any(x in text for x in ['llm', 'gpt', 'openai', 'anthropic', 'chat', 'agent', 'ai_', 'ai_tools', 'grok', 'claude']):
        if any(x in text for x in ['agent', 'autonomous']):
            return ("01_AI_LLM_TOOLS", "ai_agents")
        elif any(x in text for x in ['orchestrat', 'multi_llm', 'router']):
            return ("01_AI_LLM_TOOLS", "llm_orchestration")
        elif any(x in text for x in ['content.*generat', 'text.*generat', 'write']):
            return ("01_AI_LLM_TOOLS", "content_generation")
        elif any(x in text for x in ['voice', 'speech', 'tts', 'transcrib', 'whisper']):
            return ("01_AI_LLM_TOOLS", "voice_speech")
        elif any(x in text for x in ['fine.*tun', 'train', 'lora', 'qlora', 'axolotl']):
            return ("01_AI_LLM_TOOLS", "fine_tuning")
        elif any(x in text for x in ['chatbot', 'chat_bot']):
            return ("01_AI_LLM_TOOLS", "chatbots")
        else:
            return ("01_AI_LLM_TOOLS", "multi_llm_systems")
    
    # Automation & Bots
    if any(x in text for x in ['bot', 'automation', 'automat', 'scraper', 'scrap', 'crawler', 'crawl']):
        if any(x in text for x in ['instagram', 'insta']):
            return ("02_AUTOMATION_BOTS", "instagram_automation")
        elif any(x in text for x in ['youtube', 'yt_', 'ytube']):
            return ("02_AUTOMATION_BOTS", "youtube_automation")
        elif any(x in text for x in ['tiktok', 'tik_tok']):
            return ("02_AUTOMATION_BOTS", "tiktok_automation")
        elif any(x in text for x in ['twitter', 'tweet']):
            return ("02_AUTOMATION_BOTS", "twitter_automation")
        elif any(x in text for x in ['scraper', 'scrap', 'crawler', 'crawl']):
            return ("02_AUTOMATION_BOTS", "web_scrapers")
        else:
            return ("02_AUTOMATION_BOTS", "data_extractors")
    
    # Media Processing
    if any(x in text for x in ['audio', 'video', 'image', 'photo', 'media', 'gallery', 'upscale', 'transcrib']):
        if any(x in text for x in ['audio', 'mp3', 'wav', 'transcrib', 'whisper']):
            return ("03_MEDIA_PROCESSING", "audio_transcription")
        elif any(x in text for x in ['video', 'mp4', 'youtube.*edit', 'clip']):
            return ("03_MEDIA_PROCESSING", "video_editing")
        elif any(x in text for x in ['image', 'photo', 'png', 'jpeg', 'resize']):
            return ("03_MEDIA_PROCESSING", "image_processing")
        elif any(x in text for x in ['upscale', 'super.*res']):
            return ("03_MEDIA_PROCESSING", "image_upscaling")
        elif any(x in text for x in ['gallery', 'portfolio']):
            return ("03_MEDIA_PROCESSING", "gallery_systems")
        else:
            return ("03_MEDIA_PROCESSING", "image_processing")
    
    # Business Tools
    if any(x in text for x in ['crm', 'lead', 'revenue', 'business.*intel', 'dashboard', 'analytics']):
        if any(x in text for x in ['crm']):
            return ("04_BUSINESS_TOOLS", "crm_systems")
        elif any(x in text for x in ['dashboard', 'analytics']):
            return ("04_BUSINESS_TOOLS", "analytics_dashboards")
        elif any(x in text for x in ['lead', 'prospect']):
            return ("04_BUSINESS_TOOLS", "lead_generation")
        elif any(x in text for x in ['revenue', 'sales', 'income']):
            return ("04_BUSINESS_TOOLS", "revenue_tracking")
        else:
            return ("04_BUSINESS_TOOLS", "reporting_tools")
    
    # Web Development
    if any(x in text for x in ['web.*app', 'api', 'fastapi', 'flask', 'django', 'website', 'ecommerce']):
        if any(x in text for x in ['web.*app', 'streamlit', 'gradio']):
            return ("05_WEB_DEVELOPMENT", "web_apps")
        elif any(x in text for x in ['api', 'endpoint', 'fastapi', 'flask']):
            return ("05_WEB_DEVELOPMENT", "api_services")
        elif any(x in text for x in ['website', 'site.*generat', 'landing']):
            return ("05_WEB_DEVELOPMENT", "website_generators")
        elif any(x in text for x in ['ecommerce', 'shop', 'store', 'product']):
            return ("05_WEB_DEVELOPMENT", "ecommerce_tools")
        else:
            return ("05_WEB_DEVELOPMENT", "web_apps")
    
    # Data Analysis
    if any(x in text for x in ['csv', 'data.*analy', 'data.*process', 'file.*organ', 'dedupe', 'duplicate']):
        if any(x in text for x in ['csv']):
            return ("06_DATA_ANALYSIS", "csv_tools")
        elif any(x in text for x in ['clean', 'dedupe', 'duplicate']):
            return ("06_DATA_ANALYSIS", "data_cleaners")
        elif any(x in text for x in ['analy', 'process']):
            return ("06_DATA_ANALYSIS", "analysis_engines")
        elif any(x in text for x in ['organ', 'sort', 'categor']):
            return ("06_DATA_ANALYSIS", "file_organizers")
        else:
            return ("06_DATA_ANALYSIS", "analysis_engines")
    
    # Marketing & SEO
    if any(x in text for x in ['seo', 'marketing', 'content.*analy', 'social.*media', 'rank', 'backlink']):
        if any(x in text for x in ['seo']):
            return ("07_MARKETING_SEO", "seo_tools")
        elif any(x in text for x in ['content.*analy']):
            return ("07_MARKETING_SEO", "content_analyzers")
        elif any(x in text for x in ['marketing', 'campaign']):
            return ("07_MARKETING_SEO", "marketing_automation")
        elif any(x in text for x in ['social.*media']):
            return ("07_MARKETING_SEO", "social_media_tools")
        else:
            return ("07_MARKETING_SEO", "seo_tools")
    
    # Default to Utilities
    return ("08_UTILITIES_SCRIPTS", "file_utilities")


# ============================================================
# Main Creation Function
# ============================================================

def create_comprehensive_package():
    """Create the comprehensive marketplace package."""
    
    print("="*70)
    print("🚀 CREATING COMPREHENSIVE PYTHON MARKETPLACE PACKAGE")
    print("="*70)
    
    base_path = Path(OUTPUT_BASE)
    
    # Create main directory
    if base_path.exists():
        print(f"\n⚠️  Removing existing directory: {base_path}")
        shutil.rmtree(base_path)
    
    base_path.mkdir(parents=True)
    print(f"\n✅ Created: {base_path}")
    
    # Create folder structure
    print("\n📁 Creating folder structure...")
    for main_cat, cat_info in FOLDER_STRUCTURE.items():
        cat_path = base_path / main_cat
        cat_path.mkdir(exist_ok=True)
        
        for subcat in cat_info['subcategories']:
            (cat_path / subcat).mkdir(exist_ok=True)
        
        print(f"   ✓ {main_cat}/")
        for subcat in cat_info['subcategories']:
            print(f"      ✓ {subcat}/")
    
    # Read and categorize scripts
    print("\n📊 Reading and categorizing scripts...")
    
    scripts_by_category = defaultdict(list)
    all_scripts = []
    
    with open(SOURCE_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_scripts.append(row)
            
            main_cat, subcat = categorize_script(
                row['full_path'],
                row['file_name'],
                row.get('category', ''),
                row.get('description', '')
            )
            
            row['assigned_category'] = main_cat
            row['assigned_subcategory'] = subcat
            
            scripts_by_category[main_cat].append(row)
    
    print(f"   Total scripts categorized: {len(all_scripts):,}")
    
    # Create category manifests
    print("\n📝 Creating category manifests...")
    for main_cat, scripts in scripts_by_category.items():
        manifest_path = base_path / main_cat / "CATEGORY_MANIFEST.md"
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(f"# {main_cat.replace('_', ' ')}\n\n")
            f.write(f"**Description:** {FOLDER_STRUCTURE[main_cat]['description']}\n\n")
            f.write(f"**Total Scripts:** {len(scripts):,}\n\n")
            
            # Subcategory breakdown
            subcats = defaultdict(int)
            for script in scripts:
                subcats[script['assigned_subcategory']] += 1
            
            f.write("## Subcategories\n\n")
            f.write("| Subcategory | Count |\n")
            f.write("|-------------|-------|\n")
            for subcat, count in sorted(subcats.items(), key=lambda x: x[1], reverse=True):
                f.write(f"| {subcat} | {count:,} |\n")
            
            f.write("\n## Marketplace Readiness\n\n")
            ready = sum(1 for s in scripts if s.get('marketplace_ready', '').lower() == 'yes')
            f.write(f"- **Ready to Sell:** {ready:,} ({ready/len(scripts)*100:.1f}%)\n")
            f.write(f"- **Needs Work:** {len(scripts)-ready:,}\n")
            
            f.write("\n## Estimated Value\n\n")
            value_ranges = defaultdict(int)
            for script in scripts:
                value_ranges[script.get('estimated_value_range', 'Unknown')] += 1
            
            f.write("| Value Range | Count |\n")
            f.write("|-------------|-------|\n")
            for value, count in sorted(value_ranges.items(), key=lambda x: x[1], reverse=True):
                f.write(f"| {value} | {count:,} |\n")
        
        print(f"   ✓ {main_cat}/CATEGORY_MANIFEST.md")
    
    # Create master inventory
    print("\n📋 Creating master inventory...")
    
    master_inventory_path = base_path / "DOCUMENTATION" / "MASTER_INVENTORY.csv"
    with open(master_inventory_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = list(all_scripts[0].keys()) if all_scripts else []
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_scripts)
    
    print(f"   ✓ MASTER_INVENTORY.csv ({len(all_scripts):,} scripts)")
    
    # Create comprehensive README
    print("\n📖 Creating comprehensive README...")
    create_master_readme(base_path, all_scripts, scripts_by_category)
    
    # Create marketplace listings
    print("\n🏪 Creating marketplace listings...")
    create_marketplace_listings(base_path, scripts_by_category)
    
    # Create pricing guide
    print("\n💰 Creating pricing guide...")
    create_pricing_guide(base_path, scripts_by_category)
    
    # Create selling strategy
    print("\n🎯 Creating selling strategy...")
    create_selling_strategy(base_path, scripts_by_category)
    
    # Create quick start guide
    print("\n🚀 Creating quick start guide...")
    create_quick_start(base_path)
    
    # Create statistics report
    print("\n📊 Creating statistics report...")
    create_statistics_report(base_path, all_scripts, scripts_by_category)
    
    # Summary
    print("\n" + "="*70)
    print("✅ PACKAGE CREATION COMPLETE!")
    print("="*70)
    print(f"\n📁 Location: {base_path}")
    print("\n📊 Summary:")
    print(f"   Total Scripts: {len(all_scripts):,}")
    print(f"   Categories: {len(scripts_by_category)}")
    print("   Documentation Files: 8+")
    
    total_value_low = 0
    total_value_high = 0
    for scripts in scripts_by_category.values():
        for script in scripts:
            value = script.get('estimated_value_range', '$0-$0')
            if '-' in value:
                try:
                    low, high = value.replace('$', '').replace(',', '').split('-')
                    total_value_low += int(low)
                    total_value_high += int(high)
                except (ValueError, IndexError):
                    pass
    
    print("\n💰 Estimated Total Value:")
    print(f"   Low: ${total_value_low:,}")
    print(f"   High: ${total_value_high:,}")
    
    print("\n🎯 Next Steps:")
    print(f"   1. Review: {base_path}/README.md")
    print(f"   2. Check: {base_path}/DOCUMENTATION/MASTER_INVENTORY.csv")
    print(f"   3. Start: {base_path}/QUICK_START.md")
    print("="*70)


def create_master_readme(base_path, all_scripts, scripts_by_category):
    """Create comprehensive README.md"""
    
    readme_path = base_path / "README.md"
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("# 🚀 Python Scripts Marketplace Empire\n\n")
        f.write(f"**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Scripts:** {len(all_scripts):,}\n")
        f.write(f"**Categories:** {len(scripts_by_category)}\n\n")
        
        f.write("---\n\n")
        f.write("## 📦 What's Inside\n\n")
        f.write("This is a comprehensive, production-ready package of ")
        f.write(f"{len(all_scripts):,} original Python scripts organized and documented ")
        f.write("for selling on freelance marketplaces (Upwork, Fiverr, Gumroad, Codester, etc.)\n\n")
        
        f.write("## 📁 Directory Structure\n\n")
        f.write("```\n")
        for main_cat in sorted(FOLDER_STRUCTURE.keys()):
            f.write(f"📁 {main_cat}/\n")
            if main_cat in scripts_by_category:
                subcats = set(s['assigned_subcategory'] for s in scripts_by_category[main_cat])
                for subcat in sorted(subcats)[:5]:  # Show first 5
                    f.write(f"   📁 {subcat}/\n")
                if len(subcats) > 5:
                    f.write(f"   ... (+{len(subcats)-5} more)\n")
        f.write("📁 DOCUMENTATION/\n")
        f.write("📁 MARKETPLACE_LISTINGS/\n")
        f.write("```\n\n")
        
        f.write("## 📊 Category Breakdown\n\n")
        f.write("| Category | Scripts | Ready | Est. Value |\n")
        f.write("|----------|---------|-------|------------|\n")
        
        for cat_name in sorted(FOLDER_STRUCTURE.keys()):
            if cat_name in scripts_by_category:
                scripts = scripts_by_category[cat_name]
                count = len(scripts)
                ready = sum(1 for s in scripts if s.get('marketplace_ready', '').lower() == 'yes')
                
                # Calculate value
                value_low = 0
                value_high = 0
                for s in scripts:
                    val = s.get('estimated_value_range', '$0-$0')
                    if '-' in val:
                        try:
                            lo, hi = val.replace('$', '').replace(',', '').split('-')
                            value_low += int(lo)
                            value_high += int(hi)
                        except (ValueError, IndexError):
                            pass
                
                f.write(f"| {cat_name.replace('_', ' ')} | {count:,} | {ready:,} | ${value_low:,}-${value_high:,} |\n")
        
        f.write("\n## 🎯 Quick Start\n\n")
        f.write("1. **Read** [QUICK_START.md](QUICK_START.md) - Get started in 5 minutes\n")
        f.write("2. **Browse** [MASTER_INVENTORY.csv](DOCUMENTATION/MASTER_INVENTORY.csv) - All scripts\n")
        f.write("3. **Choose** a category and review its `CATEGORY_MANIFEST.md`\n")
        f.write("4. **List** using templates in `MARKETPLACE_LISTINGS/`\n")
        f.write("5. **Sell** on Upwork, Fiverr, Gumroad!\n\n")
        
        f.write("## 💰 Monetization Strategy\n\n")
        f.write("### Immediate Revenue (Week 1)\n")
        f.write("- List top 10 scripts on Gumroad ($29-$99 each)\n")
        f.write("- Create Upwork gigs for automation services ($200-$2,000)\n")
        f.write("- Offer AI/LLM consulting ($100-$300/hour)\n\n")
        
        f.write("### Short-Term (30 Days)\n")
        f.write("- Package bundles by category\n")
        f.write("- Create demo videos and screenshots\n")
        f.write("- Build portfolio website\n\n")
        
        f.write("### Long-Term (90+ Days)\n")
        f.write("- Launch SaaS products from best tools\n")
        f.write("- Create online courses\n")
        f.write("- Offer enterprise consulting\n\n")
        
        f.write("## 📈 Estimated Total Value\n\n")
        
        total_low = 0
        total_high = 0
        for scripts in scripts_by_category.values():
            for s in scripts:
                val = s.get('estimated_value_range', '$0-$0')
                if '-' in val:
                    try:
                        lo, hi = val.replace('$', '').replace(',', '').split('-')
                        total_low += int(lo)
                        total_high += int(hi)
                    except (ValueError, IndexError):
                        pass
        
        f.write("| Metric | Value |\n")
        f.write("|--------|-------|\n")
        f.write(f"| **Total Scripts** | {len(all_scripts):,} |\n")
        f.write(f"| **Marketplace Ready** | {sum(1 for s in all_scripts if s.get('marketplace_ready', '').lower() == 'yes'):,} |\n")
        f.write(f"| **Estimated Value (Low)** | ${total_low:,} |\n")
        f.write(f"| **Estimated Value (High)** | ${total_high:,} |\n\n")
        
        f.write("---\n\n")
        f.write("## 📞 Support & Updates\n\n")
        f.write("All filtering and categorization scripts are included for re-use.\n\n")
        f.write("**Generated by:** Advanced Content & Context Analysis System\n")
        f.write("**Date:** April 10, 2026\n")


def create_marketplace_listings(base_path, scripts_by_category):
    """Create ready-to-use marketplace listings."""
    
    listings_path = base_path / "MARKETPLACE_LISTINGS"
    
    platforms = {
        "UPWORK": {
            "type": "Service-based",
            "pricing": "Per project or hourly",
            "best_for": "Custom development, consulting",
        },
        "FIVERR": {
            "type": "Gig-based",
            "pricing": "Fixed price packages",
            "best_for": "Quick deliveries, specific tasks",
        },
        "GUMROAD": {
            "type": "Digital products",
            "pricing": "One-time purchase",
            "best_for": "Script bundles, tools, frameworks",
        },
    }
    
    for platform, info in platforms.items():
        listing_path = listings_path / f"{platform}_LISTINGS.md"
        
        with open(listing_path, 'w', encoding='utf-8') as f:
            f.write(f"# {platform} Marketplace Listings\n\n")
            f.write(f"**Type:** {info['type']}\n")
            f.write(f"**Pricing:** {info['pricing']}\n")
            f.write(f"**Best For:** {info['best_for']}\n\n")
            f.write("---\n\n")
            
            # Create listings for top categories
            for cat_name in ['01_AI_LLM_TOOLS', '02_AUTOMATION_BOTS', '03_MEDIA_PROCESSING']:
                if cat_name not in scripts_by_category:
                    continue
                
                scripts = scripts_by_category[cat_name]
                
                f.write(f"## {cat_name.replace('_', ' ')}\n\n")
                f.write(f"**Available Scripts:** {len(scripts):,}\n\n")
                
                if platform == "UPWORK":
                    f.write("### Service Listing Template\n\n")
                    f.write(f"**Title:** Expert {cat_name.replace('_', ' ').replace('01 ', '').replace('02 ', '').replace('03 ', '')} Development\n\n")
                    f.write("**Description:**\n\n")
                    f.write(f"I offer professional {cat_name.lower().replace('_', ' ')} development services. ")
                    f.write(f"With {len(scripts):,} production-ready scripts, I can deliver custom solutions for your needs.\n\n")
                    f.write("**What I Offer:**\n")
                    f.write("- Custom script development\n")
                    f.write("- Integration with your systems\n")
                    f.write("- Ongoing support and maintenance\n")
                    f.write("- Documentation and training\n\n")
                    f.write("**Starting at:** $500-$5,000 per project\n\n")
                
                elif platform == "FIVERR":
                    f.write("### Gig Template\n\n")
                    f.write(f"**Gig Title:** I will develop custom {cat_name.lower().replace('_', ' ')} scripts\n\n")
                    f.write("**Packages:**\n\n")
                    f.write("| Package | Price | Delivery |\n")
                    f.write("|---------|-------|----------|\n")
                    f.write("| Basic | $99 | 3 days |\n")
                    f.write("| Standard | $299 | 5 days |\n")
                    f.write("| Premium | $799 | 7 days |\n\n")
                
                elif platform == "GUMROAD":
                    f.write("### Product Listing Template\n\n")
                    f.write(f"**Product:** {cat_name.replace('_', ' ')} Bundle\n\n")
                    f.write("**Price:** $49-$199\n\n")
                    f.write("**Includes:**\n")
                    f.write(f"- {min(10, len(scripts))}+ production-ready Python scripts\n")
                    f.write("- Complete documentation\n")
                    f.write("- Setup instructions\n")
                    f.write("- Email support\n\n")
                
                f.write("---\n\n")
    
    print(f"   ✓ Created listings for: {', '.join(platforms.keys())}")


def create_pricing_guide(base_path, scripts_by_category):
    """Create comprehensive pricing guide."""
    
    pricing_path = base_path / "DOCUMENTATION" / "PRICING_GUIDE.md"
    
    with open(pricing_path, 'w', encoding='utf-8') as f:
        f.write("# 💰 Pricing Guide for Python Scripts\n\n")
        f.write("Complete pricing strategy for all categories and platforms.\n\n")
        f.write("---\n\n")
        
        f.write("## 📊 Pricing by Category\n\n")
        
        pricing_tiers = {
            "01_AI_LLM_TOOLS": {
                "basic": "$299-$999",
                "standard": "$1,000-$3,000",
                "premium": "$3,000-$10,000",
                "hourly": "$100-$300/hour",
            },
            "02_AUTOMATION_BOTS": {
                "basic": "$199-$499",
                "standard": "$500-$1,500",
                "premium": "$1,500-$5,000",
                "hourly": "$75-$200/hour",
            },
            "03_MEDIA_PROCESSING": {
                "basic": "$149-$399",
                "standard": "$400-$1,200",
                "premium": "$1,200-$4,000",
                "hourly": "$50-$150/hour",
            },
            "04_BUSINESS_TOOLS": {
                "basic": "$299-$799",
                "standard": "$800-$2,500",
                "premium": "$2,500-$8,000",
                "hourly": "$100-$250/hour",
            },
            "05_WEB_DEVELOPMENT": {
                "basic": "$199-$599",
                "standard": "$600-$2,000",
                "premium": "$2,000-$6,000",
                "hourly": "$75-$200/hour",
            },
            "06_DATA_ANALYSIS": {
                "basic": "$99-$299",
                "standard": "$300-$999",
                "premium": "$1,000-$3,000",
                "hourly": "$50-$150/hour",
            },
            "07_MARKETING_SEO": {
                "basic": "$149-$399",
                "standard": "$400-$1,200",
                "premium": "$1,200-$4,000",
                "hourly": "$75-$200/hour",
            },
            "08_UTILITIES_SCRIPTS": {
                "basic": "$49-$149",
                "standard": "$150-$499",
                "premium": "$500-$1,500",
                "hourly": "$50-$125/hour",
            },
        }
        
        f.write("| Category | Basic | Standard | Premium | Hourly |\n")
        f.write("|----------|-------|----------|---------|--------|\n")
        
        for cat_name, prices in pricing_tiers.items():
            f.write(f"| {cat_name.replace('_', ' ')} | ")
            f.write(f"{prices['basic']} | {prices['standard']} | ")
            f.write(f"{prices['premium']} | {prices['hourly']} |\n")
        
        f.write("\n## 🎯 Platform-Specific Pricing\n\n")
        
        f.write("### Upwork\n")
        f.write("- **Fixed Price Projects:** Use Standard/Premium tiers\n")
        f.write("- **Hourly Contracts:** Use Hourly rates\n")
        f.write("- **Retainers:** 2-3x hourly rate for ongoing work\n\n")
        
        f.write("### Fiverr\n")
        f.write("- **Basic Gig:** 0.5x Basic tier\n")
        f.write("- **Standard Gig:** 1x Standard tier\n")
        f.write("- **Premium Gig:** 1.5x Premium tier\n\n")
        
        f.write("### Gumroad\n")
        f.write("- **Single Script:** $29-$99\n")
        f.write("- **Small Bundle (5-10):** $49-$199\n")
        f.write("- **Large Bundle (10+):** $99-$499\n")
        f.write("- **Complete Category:** $199-$999\n\n")
        
        f.write("## 💡 Pricing Tips\n\n")
        f.write("1. **Start lower** to build reviews, then increase\n")
        f.write("2. **Offer packages** for better value\n")
        f.write("3. **Charge more** for custom work vs. templates\n")
        f.write("4. **Include support** in premium tiers\n")
        f.write("5. **Upsell** maintenance and updates\n\n")


def create_selling_strategy(base_path, scripts_by_category):
    """Create comprehensive selling strategy."""
    
    strategy_path = base_path / "DOCUMENTATION" / "SELLING_STRATEGY.md"
    
    with open(strategy_path, 'w', encoding='utf-8') as f:
        f.write("# 🎯 Comprehensive Selling Strategy\n\n")
        f.write("Step-by-step plan to monetize your Python script empire.\n\n")
        f.write("---\n\n")
        
        f.write("## 📅 Phase 1: Quick Wins (Week 1-2)\n\n")
        f.write("### Goals\n")
        f.write("- Generate first revenue\n")
        f.write("- Build marketplace presence\n")
        f.write("- Get initial reviews\n\n")
        
        f.write("### Actions\n")
        f.write("1. **Gumroad Setup** (Day 1-2)\n")
        f.write("   - Create account\n")
        f.write("   - List top 10 scripts as individual products\n")
        f.write("   - Price: $29-$99 each\n")
        f.write("   - Create simple product pages\n\n")
        
        f.write("2. **Upwork Profile** (Day 2-3)\n")
        f.write("   - Complete profile with AI/automation expertise\n")
        f.write("   - Create 3-5 specialized gigs\n")
        f.write("   - Set competitive rates\n\n")
        
        f.write("3. **Fiverr Gigs** (Day 3-4)\n")
        f.write("   - Create 5 gigs in different categories\n")
        f.write("   - Use 3-tier pricing\n")
        f.write("   - Add portfolio samples\n\n")
        
        f.write("4. **Social Promotion** (Day 5-7)\n")
        f.write("   - Share on Twitter/LinkedIn\n")
        f.write("   - Join relevant communities\n")
        f.write("   - Offer launch discounts\n\n")
        
        f.write("### Expected Revenue: $500-$2,000\n\n")
        f.write("---\n\n")
        
        f.write("## 📅 Phase 2: Build Momentum (Month 1)\n\n")
        f.write("### Goals\n")
        f.write("- Establish consistent revenue\n")
        f.write("- Build client base\n")
        f.write("- Create bundles and packages\n\n")
        
        f.write("### Actions\n")
        f.write("1. **Create Bundles**\n")
        f.write("   - Package scripts by category\n")
        f.write("   - Price: $99-$499 per bundle\n")
        f.write("   - Add documentation and support\n\n")
        
        f.write("2. **Content Marketing**\n")
        f.write("   - Write blog posts showcasing tools\n")
        f.write("   - Create YouTube demos\n")
        f.write("   - Share case studies\n\n")
        
        f.write("3. **Client Outreach**\n")
        f.write("   - Propose to relevant Upwork jobs\n")
        f.write("   - Offer free consultations\n")
        f.write("   - Build long-term relationships\n\n")
        
        f.write("### Expected Revenue: $2,000-$5,000/month\n\n")
        f.write("---\n\n")
        
        f.write("## 📅 Phase 3: Scale Up (Month 2-3)\n\n")
        f.write("### Goals\n")
        f.write("- Launch SaaS products\n")
        f.write("- Create online courses\n")
        f.write("- Build team/contractors\n\n")
        
        f.write("### Actions\n")
        f.write("1. **SaaS Development**\n")
        f.write("   - Convert best tools to web apps\n")
        f.write("   - Add user management\n")
        f.write("   - Implement subscription billing\n\n")
        
        f.write("2. **Course Creation**\n")
        f.write("   - Record AI/automation courses\n")
        f.write("   - Sell on Udemy/Teachable\n")
        f.write("   - Price: $49-$299 per course\n\n")
        
        f.write("3. **Team Building**\n")
        f.write("   - Hire VA for admin tasks\n")
        f.write("   - Partner with other developers\n")
        f.write("   - Outsource non-core work\n\n")
        
        f.write("### Expected Revenue: $5,000-$15,000/month\n\n")
        f.write("---\n\n")
        
        f.write("## 📅 Phase 4: Empire Building (Month 6+)\n\n")
        f.write("### Goals\n")
        f.write("- Multiple revenue streams\n")
        f.write("- Passive income focus\n")
        f.write("- Brand recognition\n\n")
        
        f.write("### Revenue Streams\n")
        f.write("1. **Script Sales:** $2,000-$5,000/month\n")
        f.write("2. **SaaS Subscriptions:** $5,000-$20,000/month\n")
        f.write("3. **Consulting:** $3,000-$10,000/month\n")
        f.write("4. **Courses:** $2,000-$8,000/month\n")
        f.write("5. **Affiliate/Referrals:** $1,000-$3,000/month\n\n")
        
        f.write("### Total Expected Revenue: $13,000-$46,000/month\n\n")


def create_quick_start(base_path):
    """Create quick start guide."""
    
    quick_start_path = base_path / "QUICK_START.md"
    
    with open(quick_start_path, 'w', encoding='utf-8') as f:
        f.write("# 🚀 Quick Start Guide - Sell Your Python Scripts in 5 Minutes\n\n")
        
        f.write("## ⚡ Fastest Path to First Sale\n\n")
        
        f.write("### Step 1: Choose Your Best Scripts (2 minutes)\n")
        f.write("1. Open `DOCUMENTATION/MASTER_INVENTORY.csv`\n")
        f.write("2. Sort by `marketability_score` (highest first)\n")
        f.write("3. Pick top 5-10 scripts\n")
        f.write("4. Focus on categories:\n")
        f.write("   - AI/LLM Tools (highest value)\n")
        f.write("   - Automation Bots (high demand)\n")
        f.write("   - Media Processing (easy to demo)\n\n")
        
        f.write("### Step 2: Create Gumroad Account (1 minute)\n")
        f.write("1. Go to [gumroad.com](https://gumroad.com)\n")
        f.write("2. Sign up (free)\n")
        f.write("3. Connect PayPal/Stripe\n\n")
        
        f.write("### Step 3: List Your First Product (2 minutes)\n")
        f.write("1. Click \"Products\" → \"New Product\"\n")
        f.write("2. Use this template:\n\n")
        f.write("```\n")
        f.write("Title: [Script Name] - Python Automation Tool\n\n")
        f.write("Description:\n")
        f.write("Professional Python script for [purpose].\n\n")
        f.write("Features:\n")
        f.write("- Feature 1\n")
        f.write("- Feature 2\n")
        f.write("- Feature 3\n\n")
        f.write("Includes:\n")
        f.write("- ✅ Production-ready Python script\n")
        f.write("- ✅ Setup instructions\n")
        f.write("- ✅ Documentation\n")
        f.write("- ✅ Email support\n\n")
        f.write("Price: $49-$99\n")
        f.write("```\n\n")
        
        f.write("3. Upload script file(s)\n")
        f.write("4. Publish!\n\n")
        
        f.write("## 🎯 Next Steps (After First Listing)\n\n")
        f.write("1. **Create Upwork Profile** - Offer services using your scripts\n")
        f.write("2. **Make Fiverr Gigs** - Package as fixed-price offerings\n")
        f.write("3. **Share on Social Media** - Twitter, LinkedIn, Reddit\n")
        f.write("4. **Join Communities** - Indie Hackers, Product Hunt\n")
        f.write("5. **List More Products** - Aim for 10+ listings\n\n")
        
        f.write("## 💰 Pricing Cheat Sheet\n\n")
        f.write("| Script Type | Gumroad | Upwork | Fiverr |\n")
        f.write("|-------------|---------|--------|--------|\n")
        f.write("| Simple Utility | $29 | $100-$300 | $49-$99 |\n")
        f.write("| Automation Tool | $49-$99 | $300-$1,000 | $99-$299 |\n")
        f.write("| AI/LLM Tool | $99-$199 | $1,000-$5,000 | $199-$499 |\n")
        f.write("| Complete System | $199-$499 | $5,000-$15,000 | $499-$999 |\n\n")
        
        f.write("## 📞 Need Help?\n\n")
        f.write("- **Full Documentation:** See `README.md`\n")
        f.write("- **Pricing Guide:** See `DOCUMENTATION/PRICING_GUIDE.md`\n")
        f.write("- **Selling Strategy:** See `DOCUMENTATION/SELLING_STRATEGY.md`\n")
        f.write("- **Complete Inventory:** See `DOCUMENTATION/MASTER_INVENTORY.csv`\n\n")
        
        f.write("---\n\n")
        f.write("**You're ready to start selling! 🚀**\n")


def create_statistics_report(base_path, all_scripts, scripts_by_category):
    """Create detailed statistics report."""
    
    stats_path = base_path / "DOCUMENTATION" / "STATISTICS_REPORT.md"
    
    with open(stats_path, 'w', encoding='utf-8') as f:
        f.write("# 📊 Comprehensive Statistics Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        f.write("## 📈 Overall Metrics\n\n")
        f.write("| Metric | Value |\n")
        f.write("|--------|-------|\n")
        f.write(f"| **Total Scripts** | {len(all_scripts):,} |\n")
        
        marketplace_ready = sum(1 for s in all_scripts if s.get('marketplace_ready', '').lower() == 'yes')
        f.write(f"| **Marketplace Ready** | {marketplace_ready:,} ({marketplace_ready/len(all_scripts)*100:.1f}%) |\n")
        
        avg_size = sum(float(s.get('file_size_kb', 0)) for s in all_scripts) / len(all_scripts)
        f.write(f"| **Average File Size** | {avg_size:.1f} KB |\n")
        
        avg_confidence = sum(int(s.get('confidence_score', 0)) for s in all_scripts) / len(all_scripts)
        f.write(f"| **Average Confidence** | {avg_confidence:.1f}/100 |\n\n")
        
        f.write("## 📂 Category Statistics\n\n")
        
        for cat_name in sorted(scripts_by_category.keys()):
            scripts = scripts_by_category[cat_name]
            
            f.write(f"### {cat_name.replace('_', ' ')}\n\n")
            f.write(f"- **Total Scripts:** {len(scripts):,}\n")
            
            ready = sum(1 for s in scripts if s.get('marketplace_ready', '').lower() == 'yes')
            f.write(f"- **Marketplace Ready:** {ready:,} ({ready/len(scripts)*100:.1f}%)\n")
            
            # Subcategory breakdown
            subcats = defaultdict(int)
            for s in scripts:
                subcats[s['assigned_subcategory']] += 1
            
            f.write(f"- **Subcategories:** {len(subcats)}\n")
            
            # Top 5 subcategories
            f.write("- **Top Subcategories:**\n")
            for subcat, count in sorted(subcats.items(), key=lambda x: x[1], reverse=True)[:5]:
                f.write(f"  - {subcat}: {count:,}\n")
            
            # File size stats
            sizes = [float(s.get('file_size_kb', 0)) for s in scripts]
            if sizes:
                f.write("- **File Sizes:**\n")
                f.write(f"  - Min: {min(sizes):.1f} KB\n")
                f.write(f"  - Max: {max(sizes):.1f} KB\n")
                f.write(f"  - Avg: {sum(sizes)/len(sizes):.1f} KB\n")
            
            f.write("\n")
        
        f.write("## 💰 Value Analysis\n\n")
        
        value_ranges = defaultdict(int)
        for s in all_scripts:
            value_ranges[s.get('estimated_value_range', 'Unknown')] += 1
        
        f.write("| Value Range | Count | Percentage |\n")
        f.write("|-------------|-------|------------|\n")
        for value, count in sorted(value_ranges.items(), key=lambda x: x[1], reverse=True):
            pct = count / len(all_scripts) * 100
            f.write(f"| {value} | {count:,} | {pct:.1f}% |\n")
        
        f.write("\n## 📁 Source Directory Breakdown\n\n")
        
        source_dirs = defaultdict(int)
        for s in all_scripts:
            path = s['full_path']
            parts = path.replace("/Users/steven/", "").split("/")
            if len(parts) > 1:
                source_dirs[parts[0]] += 1
        
        f.write("| Directory | Scripts | Percentage |\n")
        f.write("|-----------|---------|------------|\n")
        for dir_name, count in sorted(source_dirs.items(), key=lambda x: x[1], reverse=True)[:15]:
            pct = count / len(all_scripts) * 100
            f.write(f"| {dir_name} | {count:,} | {pct:.1f}% |\n")


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    create_comprehensive_package()
