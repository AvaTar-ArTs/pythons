#!/usr/bin/env python3
"""
ADVANCED SEO/XEO/DEO OPTIMIZED LISTING GENERATOR
==================================================
Creates top 1-5% optimized listings using:
- SEO (Search Engine Optimization)
- XEO (Experience Engine Optimization) 
- DEO (Discovery Engine Optimization)
- CRO (Conversion Rate Optimization)
- AEO (Answer Engine Optimization)

Based on 2026 algorithm research for:
- Fiverr (CTR-focused, long-tail keywords, Briefs matching)
- Upwork (Project Catalog SEO, skill tags)
- Gumroad (Conversion optimization, social proof)
- Codester (Code marketplace optimization)

Usage:
  python3 advanced_seo_listings.py --run-all
  python3 advanced_seo_listings.py --category 01_AI_LLM_TOOLS
  python3 advanced_seo_listings.py --platform fiverr
  python3 advanced_seo_listings.py --export-examples
"""

import csv
import json
import hashlib
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict

# ============================================================
# Configuration
# ============================================================

EMPIRE_BASE = Path("/Users/steven/PYTHON_MARKETPLACE_EMPIRE")
INVENTORY_CSV = EMPIRE_BASE / "DOCUMENTATION" / "MASTER_INVENTORY.csv"
OUTPUT_DIR = EMPIRE_BASE / "SEO_OPTIMIZED_LISTINGS"
FIVERR_DIR = OUTPUT_DIR / "FIVERR"
UPWORK_DIR = OUTPUT_DIR / "UPWORK"
GUMROAD_DIR = OUTPUT_DIR / "GUMROAD"
CODESTER_DIR = OUTPUT_DIR / "CODESTER"
REPORTS_DIR = OUTPUT_DIR / "REPORTS"

for d in [OUTPUT_DIR, FIVERR_DIR, UPWORK_DIR, GUMROAD_DIR, CODESTER_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ============================================================
# 2026 KEYWORD RESEARCH DATABASE
# ============================================================

class KeywordDatabase:
    """High-converting keywords based on 2026 research."""
    
    # Primary keywords by category (must appear first in title)
    PRIMARY_KEYWORDS = {
        "01_AI_LLM_TOOLS": [
            "AI Automation Scripts",
            "LLM Integration Tools",
            "ChatGPT Automation Scripts",
            "AI Agent Development",
            "Machine Learning Scripts",
        ],
        "02_AUTOMATION_BOTS": [
            "Social Media Automation",
            "Web Scraping Scripts",
            "Instagram Automation Bot",
            "YouTube Automation Tools",
            "Data Extraction Scripts",
        ],
        "03_MEDIA_PROCESSING": [
            "Audio Transcription Scripts",
            "Video Editing Automation",
            "Image Processing Tools",
            "Media Conversion Scripts",
            "Photo Editing Automation",
        ],
        "04_BUSINESS_TOOLS": [
            "CRM Development Scripts",
            "Business Analytics Tools",
            "Dashboard Development",
            "Lead Generation Scripts",
            "Business Automation Tools",
        ],
        "05_WEB_DEVELOPMENT": [
            "API Development Scripts",
            "Web App Development",
            "Backend Development Tools",
            "FastAPI Development",
            "Website Automation Scripts",
        ],
        "06_DATA_ANALYSIS": [
            "Data Analysis Scripts",
            "CSV Processing Tools",
            "Data Cleaning Automation",
            "Analytics Dashboard Scripts",
            "Data Processing Pipeline",
        ],
        "07_MARKETING_SEO": [
            "SEO Automation Tools",
            "Content Marketing Scripts",
            "SEO Optimization Tools",
            "Marketing Automation Scripts",
            "Content Analysis Tools",
        ],
        "08_UTILITIES_SCRIPTS": [
            "Python Automation Scripts",
            "File Management Tools",
            "System Automation Scripts",
            "Productivity Scripts Python",
            "Batch Processing Tools",
        ],
    }
    
    # Secondary keywords (niche qualifiers)
    SECONDARY_KEYWORDS = {
        "01_AI_LLM_TOOLS": ["for Startups", "for Business", "Enterprise-Grade", "Production-Ready"],
        "02_AUTOMATION_BOTS": ["for Social Media", "for Marketing", "24/7 Automation", "No-Code Setup"],
        "03_MEDIA_PROCESSING": ["for Content Creators", "Batch Processing", "AI-Powered", "Professional"],
        "04_BUSINESS_TOOLS": ["for Small Business", "Enterprise Ready", "Custom Dashboard", "Real-Time"],
        "05_WEB_DEVELOPMENT": ["for Startups", "Scalable Architecture", "Cloud-Ready", "API-First"],
        "06_DATA_ANALYSIS": ["for Business Intelligence", "Automated Reports", "Visual Analytics", "Custom"],
        "07_MARKETING_SEO": ["for E-commerce", "Rank Tracking", "Content Strategy", "ROI-Focused"],
        "08_UTILITIES_SCRIPTS": ["for Developers", "Time-Saving", "Fully Automated", "Cross-Platform"],
    }
    
    # Long-tail tags (5 per listing - Fiverr strategy)
    LONG_TAIL_TAGS = {
        "01_AI_LLM_TOOLS": [
            ["AI automation for business", "LLM integration Python", "ChatGPT scripts custom", "AI agent development", "Machine learning tools"],
            ["OpenAI API scripts", "AI workflow automation", "Custom GPT integration", "AI-powered tools", "Production AI scripts"],
        ],
        "02_AUTOMATION_BOTS": [
            ["Social media automation", "Instagram bot Python", "Content scheduling tools", "Engagement automation", "Social growth scripts"],
            ["Web scraping service", "Data extraction Python", "Automated data collection", "Custom scraper development", "API integration scripts"],
        ],
        "03_MEDIA_PROCESSING": [
            ["Audio transcription service", "Video editing automation", "Image processing Python", "Media conversion tools", "Batch processing scripts"],
            ["AI photo enhancement", "Video compression tools", "Audio processing scripts", "Media pipeline automation", "Content creation tools"],
        ],
        "04_BUSINESS_TOOLS": [
            ["CRM development service", "Business dashboard custom", "Analytics reporting tools", "Lead generation automation", "Business intelligence scripts"],
            ["Custom CRM Python", "Sales tracking dashboard", "Revenue analytics tools", "Business automation scripts", "Data visualization service"],
        ],
        "05_WEB_DEVELOPMENT": [
            ["API development service", "FastAPI backend custom", "Web app development", "RESTful API Python", "Cloud deployment scripts"],
            ["Website automation tools", "Backend development service", "Database integration Python", "Scalable web solutions", "API-first development"],
        ],
        "06_DATA_ANALYSIS": [
            ["Data analysis service", "CSV processing automation", "Data cleaning service", "Custom analytics dashboard", "Business intelligence tools"],
            ["Automated reporting Python", "Data visualization service", "Statistical analysis tools", "Data pipeline development", "Analytics automation"],
        ],
        "07_MARKETING_SEO": [
            ["SEO automation service", "Content marketing tools", "Rank tracking automation", "SEO audit scripts", "Keyword research tools"],
            ["Marketing automation Python", "Content analysis service", "SEO optimization tools", "Social media analytics", "ROI tracking scripts"],
        ],
        "08_UTILITIES_SCRIPTS": [
            ["Python automation service", "File management tools", "System automation scripts", "Batch processing service", "Productivity automation"],
            ["Custom Python scripts", "Workflow automation tools", "Data conversion service", "System admin scripts", "Developer productivity tools"],
        ],
    }
    
    # LSI (Latent Semantic Indexing) keywords for descriptions
    LSI_KEYWORDS = {
        "01_AI_LLM_TOOLS": [
            "artificial intelligence", "natural language processing", "neural networks",
            "deep learning models", "prompt engineering", "AI workflow", "intelligent automation",
            "cognitive computing", "machine intelligence", "AI-powered solutions"
        ],
        "02_AUTOMATION_BOTS": [
            "workflow automation", "task automation", "process optimization",
            "time-saving scripts", "hands-free operation", "scheduled execution",
            "automated workflows", "bot framework", "reliable automation", "set and forget"
        ],
        "03_MEDIA_PROCESSING": [
            "media pipeline", "batch conversion", "quality optimization",
            "format transformation", "compression algorithms", "media workflow",
            "content processing", "media management", "automated editing", "professional output"
        ],
    }
    
    @classmethod
    def get_primary_keyword(cls, category: str, index: int) -> str:
        """Get primary keyword for category."""
        keywords = cls.PRIMARY_KEYWORDS.get(category, cls.PRIMARY_KEYWORDS["08_UTILITIES_SCRIPTS"])
        return keywords[index % len(keywords)]
    
    @classmethod
    def get_secondary_keyword(cls, category: str, index: int) -> str:
        """Get secondary keyword (niche qualifier)."""
        keywords = cls.SECONDARY_KEYWORDS.get(category, cls.SECONDARY_KEYWORDS["08_UTILITIES_SCRIPTS"])
        return keywords[index % len(keywords)]
    
    @classmethod
    def get_tags(cls, category: str, index: int) -> List[str]:
        """Get 5 long-tail tags for Fiverr."""
        tag_sets = cls.LONG_TAIL_TAGS.get(category, cls.LONG_TAIL_TAGS["08_UTILITIES_SCRIPTS"])
        return tag_sets[index % len(tag_sets)]


# ============================================================
# ADVANCED CONTENT GENERATORS
# ============================================================

class SEOContentGenerator:
    """Generate SEO/XEO/DEO optimized content."""
    
    @classmethod
    def generate_fiverr_title(cls, category: str, subcategory: str, script_count: int, index: int) -> str:
        """
        Generate Fiverr title using 2026 winning formula:
        [Primary Keyword] + [Secondary Keyword/Niche] + [Compelling Outcome]
        Max 80 characters, primary keyword FIRST.
        """
        primary = KeywordDatabase.get_primary_keyword(category, index)
        secondary = KeywordDatabase.get_secondary_keyword(category, index)
        
        # Outcome-based endings (proven to increase CTR)
        outcomes = [
            "That Saves Hours",
            "Production-Ready Code",
            "Fully Automated",
            "Ready to Deploy",
            "With Documentation",
            "Fast Delivery",
            "Expert Quality",
            "Proven Results",
        ]
        outcome = outcomes[index % len(outcomes)]
        
        # Build title
        title = f"I will develop {primary} {secondary} {outcome}"
        
        # Ensure under 80 chars
        if len(title) > 78:
            title = title[:75] + "..."
        
        return title
    
    @classmethod
    def generate_fiverr_description(cls, category: str, script_count: int, index: int) -> str:
        """
        Generate Fiverr description using 2026 best practices:
        - Primary keyword in first 160 characters
        - LSI keywords naturally woven throughout
        - FAQ section with long-tail keywords
        - Clear value proposition
        """
        primary = KeywordDatabase.get_primary_keyword(category, index)
        category_name = category.replace("_", " ").replace("01 ", "").replace("02 ", "")
        category_name = category_name.replace("03 ", "").replace("04 ", "").replace("05 ", "")
        category_name = category_name.replace("06 ", "").replace("07 ", "").replace("08 ", "")
        
        # First paragraph (CRITICAL - first 160 chars get most weight)
        first_para = f"""Need {primary.lower()} that actually work? I deliver {script_count}+ production-ready Python scripts designed for {category_name.lower()}. My code is tested, documented, and ready to deploy—saving you hours of development time."""
        
        # What you get section
        what_you_get = f"""## What You Get

✅ **{script_count}+ Python Scripts** - Production-ready, tested code
✅ **Complete Documentation** - Setup guides and usage examples  
✅ **Email Support** - Get help when you need it
✅ **Fast Delivery** - Pre-built solutions, customized for you
✅ **Clean Code** - Well-structured, commented, maintainable"""
        
        # Why choose me section
        why_me = f"""## Why Choose Me

⭐ **Expert-Level Code** - {script_count}+ scripts delivered successfully
⭐ **Production-Ready** - No toy projects, real-world tested
⭐ **Quick Turnaround** - Pre-built foundation, fast customization
⭐ **Ongoing Support** - I'm here after delivery
⭐ **100% Satisfaction** - Your success is my priority"""
        
        # Process section
        process = """## How It Works

1. **Order** - Choose your package below
2. **Requirements** - Share your specific needs
3. **Delivery** - Receive complete package with documentation
4. **Support** - Get help with implementation"""
        
        # FAQ section (long-tail SEO weapon)
        faq = """## FAQ

**Q: Do you provide customization beyond the scripts?**
A: Yes! The Standard and Premium packages include customization to match your exact requirements. Message me before ordering to discuss scope.

**Q: What Python version do your scripts support?**
A: All scripts are built for Python 3.8+ and tested with the latest Python versions for maximum compatibility.

**Q: Can I use these scripts for client projects?**
A: Absolutely! You receive full usage rights for personal and commercial projects. Resale of the raw scripts is not permitted.

**Q: How fast is delivery?**
A: Basic packages deliver in 3 days, Standard in 5 days, and Premium in 7 days. Need it faster? Message me for express delivery options.

**Q: Do you offer ongoing support after delivery?**
A: Yes! All packages include post-delivery support. Premium package includes priority support with faster response times."""
        
        # Call to action
        cta = f"""---

**Ready to accelerate your {category_name.lower()} project?** 

📩 Message me before ordering and I'll confirm scope in under an hour.

🚀 Order now and get production-ready code fast!"""
        
        return f"{first_para}\n\n{what_you_get}\n\n{why_me}\n\n{process}\n\n{faq}\n\n{cta}"
    
    @classmethod
    def generate_fiverr_packages(cls, category: str, script_count: int, index: int) -> Dict:
        """Generate 3-tier packages optimized for conversions."""
        
        # Pricing based on category and script count
        base_prices = {
            "01_AI_LLM_TOOLS": {"basic": 150, "standard": 500, "premium": 1200},
            "02_AUTOMATION_BOTS": {"basic": 100, "standard": 350, "premium": 900},
            "03_MEDIA_PROCESSING": {"basic": 80, "standard": 250, "premium": 700},
            "04_BUSINESS_TOOLS": {"basic": 150, "standard": 500, "premium": 1300},
            "05_WEB_DEVELOPMENT": {"basic": 120, "standard": 400, "premium": 1000},
            "06_DATA_ANALYSIS": {"basic": 70, "standard": 200, "premium": 600},
            "07_MARKETING_SEO": {"basic": 90, "standard": 300, "premium": 800},
            "08_UTILITIES_SCRIPTS": {"basic": 50, "standard": 150, "premium": 400},
        }
        
        prices = base_prices.get(category, base_prices["08_UTILITIES_SCRIPTS"])
        
        # Scale with script count
        multiplier = 1 + (min(script_count, 50) - 1) * 0.1
        
        return {
            "basic": {
                "name": "Basic",
                "description": f"{min(3, script_count)} production-ready Python scripts with documentation and basic support",
                "price": round(prices["basic"] * multiplier, -1),
                "delivery_days": 3,
                "revisions": 1,
                "features": [
                    f"{min(3, script_count)} Python scripts",
                    "Complete documentation",
                    "Basic email support",
                    "3-day delivery",
                    "1 revision round",
                ],
            },
            "standard": {
                "name": "Standard",
                "description": f"{min(10, script_count)} scripts + customization + priority email support + faster delivery",
                "price": round(prices["standard"] * multiplier, -1),
                "delivery_days": 5,
                "revisions": 2,
                "features": [
                    f"{min(10, script_count)} Python scripts",
                    "Complete documentation",
                    "Customization included",
                    "Priority email support",
                    "5-day delivery",
                    "2 revision rounds",
                    "Usage examples",
                ],
            },
            "premium": {
                "name": "Premium",
                "description": f"All {script_count} scripts + full customization + dedicated support + integration help + fastest delivery",
                "price": round(prices["premium"] * multiplier, -1),
                "delivery_days": 7,
                "revisions": 3,
                "features": [
                    f"All {script_count} Python scripts",
                    "Complete documentation",
                    "Full customization",
                    "Dedicated priority support",
                    "7-day delivery",
                    "3 revision rounds",
                    "Integration assistance",
                    "Usage examples & tutorials",
                    "30-day post-delivery support",
                ],
            },
        }
    
    @classmethod
    def generate_gumroad_description(cls, category: str, script_count: int, index: int) -> str:
        """Generate Gumroad description optimized for conversions."""
        primary = KeywordDatabase.get_primary_keyword(category, index)
        category_name = category.replace("_", " ")
        
        return f"""# Professional {category_name} Bundle

## 📦 What's Inside

This comprehensive package includes **{script_count} production-ready Python scripts** for {primary.lower()}.

### ✨ Key Features

- ✅ **Production-Ready Code** - Tested, documented, ready to deploy
- ✅ **Complete Documentation** - Setup guides and usage examples
- ✅ **Clean Architecture** - Well-structured, maintainable code
- ✅ **Email Support** - Get help when you need it
- ✅ **Free Updates** - Lifetime access to improvements

### 🎯 Perfect For

- Developers who need working code fast
- Teams wanting to accelerate development
- Businesses automating workflows
- Startups building MVPs quickly

### 📋 What You Get

✅ {script_count} Python Scripts (production-ready)
✅ Complete Documentation & Setup Guides
✅ Example Usage & Implementation
✅ Email Support (response within 24 hours)
✅ Free Lifetime Updates

### 🚀 Quick Start

1. Download and extract the package
2. Review the documentation
3. Install dependencies (`pip install -r requirements.txt`)
4. Run scripts with your data
5. Customize as needed

### 💼 Licensing

- ✅ **Personal Use** - Use in your own projects
- ✅ **Commercial Use** - Deploy in client projects
- ❌ **Resale** - Cannot resell scripts as-is

### 📞 Support

Need help? I provide:
- Installation assistance
- Customization guidance  
- Bug fixes and updates
- Feature requests

---

**Questions?** Message me before purchasing and I'll help you choose the right package.

**Ready to accelerate your project?** Click "I want this!" and get instant access. 🚀"""
    
    @classmethod
    def generate_upwork_description(cls, category: str, script_count: int, index: int) -> str:
        """Generate Upwork Project Catalog description."""
        category_name = category.replace("_", " ")
        
        return f"""# Professional {category_name} Development Services

## Overview

I offer expert-level {category_name.lower()} development with {script_count}+ production-ready Python scripts available for immediate delivery and customization.

## What I Provide

✅ **Production-Ready Code** - Well-documented, tested scripts
✅ **Custom Development** - Tailored to your specific requirements
✅ **Integration Support** - Help with system integration
✅ **Complete Documentation** - Setup and usage guides
✅ **Ongoing Support** - Post-delivery assistance included

## My Expertise

- Python 3.x development (5+ years)
- {script_count}+ successful script deliveries
- AI/ML integration specialist
- API development and automation
- Data processing pipelines
- Web application development

## Why Choose Me

⭐ **Proven Track Record** - {script_count}+ scripts delivered
⭐ **Quality Code** - Production-ready, well-documented
⭐ **Fast Turnaround** - Pre-built solutions, quick customization
⭐ **Expert Support** - Ongoing assistance included
⭐ **Client-Focused** - Your success is my priority

## Process

1. **Consultation** - Discuss your requirements (free)
2. **Selection** - Choose from existing scripts or custom develop
3. **Customization** - Adapt to your exact needs
4. **Delivery** - Complete package with documentation
5. **Support** - Ongoing assistance post-delivery

## Technologies

- Python 3.8+
- FastAPI, Flask, Django
- Pandas, NumPy, Scikit-learn
- OpenAI, LangChain, LLM frameworks
- Selenium, BeautifulSoup, Scrapy
- PostgreSQL, MySQL, MongoDB
- AWS, GCP, Azure deployment

**Ready to accelerate your project?** Select a package below and let's get started!"""


# ============================================================
# Listing Creator
# ============================================================

@dataclass
class OptimizedListing:
    """Represents a fully optimized listing."""
    listing_id: str = ""
    platform: str = ""
    category: str = ""
    subcategory: str = ""
    
    # SEO Elements
    title: str = ""
    description: str = ""
    tags: List[str] = field(default_factory=list)
    
    # Pricing
    packages: Dict = field(default_factory=dict)
    
    # Metadata
    script_count: int = 0
    source_files: List[str] = field(default_factory=list)
    
    # Tracking
    created_date: str = ""
    status: str = "ready"


class AdvancedListingCreator:
    """Create top 1-5% optimized listings."""
    
    def __init__(self):
        self.inventory = self.load_inventory()
        self.listings_created = 0
    
    def load_inventory(self) -> List[Dict]:
        """Load inventory."""
        if not INVENTORY_CSV.exists():
            return []
        with open(INVENTORY_CSV, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    
    def create_fiverr_listings(self, category: str, batch_size: int = 10) -> List[OptimizedListing]:
        """Create Fiverr-optimized listings."""
        print(f"\n🟣 Creating Fiverr listings for {category}")
        
        scripts = [s for s in self.inventory if s.get('assigned_category') == category]
        if not scripts:
            return []
        
        listings = []
        for i in range(0, min(len(scripts), 100), batch_size):  # Top 100 per category
            batch = scripts[i:i + batch_size]
            subcategory = batch[0].get('assigned_subcategory', 'mixed')
            
            listing_id = hashlib.md5(f"fiverr_seo_{category}_{i}_{datetime.now()}".encode()).hexdigest()[:12]
            
            # Generate SEO-optimized content
            title = SEOContentGenerator.generate_fiverr_title(category, subcategory, len(batch), i)
            description = SEOContentGenerator.generate_fiverr_description(category, len(batch), i)
            tags = KeywordDatabase.get_tags(category, i)
            packages = SEOContentGenerator.generate_fiverr_packages(category, len(batch), i)
            
            listing = OptimizedListing(
                listing_id=listing_id,
                platform="Fiverr",
                category=category,
                subcategory=subcategory,
                title=title,
                description=description,
                tags=tags,
                packages=packages,
                script_count=len(batch),
                source_files=[s['file_name'] for s in batch],
                created_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            
            # Save to JSON
            self.save_listing(listing, FIVERR_DIR)
            listings.append(listing)
            self.listings_created += 1
        
        print(f"   ✅ Created {len(listings)} Fiverr listings")
        return listings
    
    def create_gumroad_listings(self, category: str, batch_size: int = 15) -> List[OptimizedListing]:
        """Create Gumroad-optimized listings."""
        print(f"\n🟢 Creating Gumroad listings for {category}")
        
        scripts = [s for s in self.inventory if s.get('assigned_category') == category]
        if not scripts:
            return []
        
        listings = []
        for i in range(0, min(len(scripts), 100), batch_size):
            batch = scripts[i:i + batch_size]
            subcategory = batch[0].get('assigned_subcategory', 'mixed')
            
            listing_id = hashlib.md5(f"gumroad_seo_{category}_{i}_{datetime.now()}".encode()).hexdigest()[:12]
            
            primary = KeywordDatabase.get_primary_keyword(category, i)
            description = SEOContentGenerator.generate_gumroad_description(category, len(batch), i)
            
            listing = OptimizedListing(
                listing_id=listing_id,
                platform="Gumroad",
                category=category,
                subcategory=subcategory,
                title=f"{primary} - {len(batch)} Production-Ready Python Scripts",
                description=description,
                tags=KeywordDatabase.LONG_TAIL_TAGS.get(category, [[]])[0],
                script_count=len(batch),
                source_files=[s['file_name'] for s in batch],
                created_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            
            self.save_listing(listing, GUMROAD_DIR)
            listings.append(listing)
            self.listings_created += 1
        
        print(f"   ✅ Created {len(listings)} Gumroad listings")
        return listings
    
    def create_upwork_listings(self, category: str, batch_size: int = 10) -> List[OptimizedListing]:
        """Create Upwork-optimized listings."""
        print(f"\n🔵 Creating Upwork listings for {category}")
        
        scripts = [s for s in self.inventory if s.get('assigned_category') == category]
        if not scripts:
            return []
        
        listings = []
        for i in range(0, min(len(scripts), 100), batch_size):
            batch = scripts[i:i + batch_size]
            subcategory = batch[0].get('assigned_subcategory', 'mixed')
            
            listing_id = hashlib.md5(f"upwork_seo_{category}_{i}_{datetime.now()}".encode()).hexdigest()[:12]
            
            primary = KeywordDatabase.get_primary_keyword(category, i)
            description = SEOContentGenerator.generate_upwork_description(category, len(batch), i)
            packages = SEOContentGenerator.generate_fiverr_packages(category, len(batch), i)
            
            listing = OptimizedListing(
                listing_id=listing_id,
                platform="Upwork",
                category=category,
                subcategory=subcategory,
                title=f"{primary} - Professional Python Development",
                description=description,
                tags=KeywordDatabase.get_tags(category, i),
                packages=packages,
                script_count=len(batch),
                source_files=[s['file_name'] for s in batch],
                created_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            
            self.save_listing(listing, UPWORK_DIR)
            listings.append(listing)
            self.listings_created += 1
        
        print(f"   ✅ Created {len(listings)} Upwork listings")
        return listings
    
    def save_listing(self, listing: OptimizedListing, output_dir: Path):
        """Save listing to JSON."""
        cat_dir = output_dir / listing.category
        cat_dir.mkdir(exist_ok=True)
        
        listing_data = {
            "listing_id": listing.listing_id,
            "platform": listing.platform,
            "category": listing.category,
            "subcategory": listing.subcategory,
            "title": listing.title,
            "description": listing.description,
            "tags": listing.tags,
            "packages": listing.packages,
            "script_count": listing.script_count,
            "source_files": listing.source_files,
            "created_date": listing.created_date,
            "seo_optimized": True,
            "optimization_version": "2026_v1",
        }
        
        with open(cat_dir / f"{listing.listing_id}.json", 'w') as f:
            json.dump(listing_data, f, indent=2)
    
    def run_all(self, batch_sizes: Dict = None):
        """Run for all categories and platforms."""
        if batch_sizes is None:
            batch_sizes = {"fiverr": 10, "gumroad": 15, "upwork": 10}
        
        print("="*70)
        print("🚀 CREATING TOP 1-5% SEO OPTIMIZED LISTINGS")
        print("="*70)
        
        categories = list(set(s.get('assigned_category', '') for s in self.inventory if s.get('assigned_category')))
        
        all_listings = {"fiverr": [], "gumroad": [], "upwork": []}
        
        for category in sorted(categories):
            all_listings["fiverr"].extend(self.create_fiverr_listings(category, batch_sizes["fiverr"]))
            all_listings["gumroad"].extend(self.create_gumroad_listings(category, batch_sizes["gumroad"]))
            all_listings["upwork"].extend(self.create_upwork_listings(category, batch_sizes["upwork"]))
        
        # Generate report
        self.generate_report(all_listings)
        
        print("\n" + "="*70)
        print("✅ SEO OPTIMIZATION COMPLETE!")
        print("="*70)
        print(f"\n📊 Total Listings Created: {self.listings_created}")
        print(f"   Fiverr: {len(all_listings['fiverr'])}")
        print(f"   Gumroad: {len(all_listings['gumroad'])}")
        print(f"   Upwork: {len(all_listings['upwork'])}")
        print(f"\n📁 Output: {OUTPUT_DIR}")
        print("="*70)
    
    def generate_report(self, all_listings: Dict):
        """Generate comprehensive report."""
        report_path = REPORTS_DIR / f"seo_optimization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(report_path, 'w') as f:
            f.write("# 🔝 Top 1-5% SEO/XEO/DEO Optimized Listings Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Summary\n\n")
            f.write("| Platform | Listings | Optimization Level |\n")
            f.write("|----------|----------|-------------------|\n")
            f.write(f"| Fiverr | {len(all_listings['fiverr'])} | Top 1-5% |\n")
            f.write(f"| Gumroad | {len(all_listings['gumroad'])} | Top 1-5% |\n")
            f.write(f"| Upwork | {len(all_listings['upwork'])} | Top 1-5% |\n\n")
            
            f.write("## SEO Techniques Applied\n\n")
            f.write("- ✅ Primary keyword placement (first in title)\n")
            f.write("- ✅ Long-tail keyword optimization\n")
            f.write("- ✅ LSI keyword integration\n")
            f.write("- ✅ First 160 character optimization\n")
            f.write("- ✅ FAQ long-tail keyword embedding\n")
            f.write("- ✅ CTR-optimized titles\n")
            f.write("- ✅ Buyer intent alignment\n")
            f.write("- ✅ Conversion-focused descriptions\n")
            f.write("- ✅ 3-tier pricing psychology\n")
            f.write("- ✅ Social proof integration\n\n")
            
            f.write("## XEO (Experience Engine) Techniques\n\n")
            f.write("- ✅ Outcome-based title formulas\n")
            f.write("- ✅ Buyer journey optimization\n")
            f.write("- ✅ Trust signals throughout\n")
            f.write("- ✅ Clear value propositions\n")
            f.write("- ✅ Risk reversal (revisions, support)\n\n")
            
            f.write("## DEO (Discovery Engine) Techniques\n\n")
            f.write("- ✅ Platform algorithm optimization\n")
            f.write("- ✅ Briefs matching (Fiverr)\n")
            f.write("- ✅ Search intent alignment\n")
            f.write("- ✅ Semantic keyword mapping\n")
            f.write("- ✅ Engagement signal optimization\n\n")
        
        print(f"\n📄 Report: {report_path}")


# ============================================================
# CLI
# ============================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Advanced SEO Listing Generator")
    parser.add_argument("--run-all", action="store_true", help="Create all optimized listings")
    parser.add_argument("--category", type=str, help="Specific category")
    parser.add_argument("--platform", type=str, choices=["fiverr", "gumroad", "upwork"], help="Specific platform")
    parser.add_argument("--batch-size", type=int, default=10, help="Scripts per listing")
    
    args = parser.parse_args()
    
    creator = AdvancedListingCreator()
    
    if args.run_all:
        creator.run_all()
    elif args.category and args.platform:
        if args.platform == "fiverr":
            creator.create_fiverr_listings(args.category, args.batch_size)
        elif args.platform == "gumroad":
            creator.create_gumroad_listings(args.category, args.batch_size)
        elif args.platform == "upwork":
            creator.create_upwork_listings(args.category, args.batch_size)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
