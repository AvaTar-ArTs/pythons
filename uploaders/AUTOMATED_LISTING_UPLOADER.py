#!/usr/bin/env python3
"""
PYTHON MARKETPLACE EMPIRE - AUTOMATED LISTING UPLOADER
======================================================
Automates creating and uploading product listings to:
- Gumroad (digital products)
- Upwork (project catalog)
- Fiverr (gigs)
- Codester (scripts & code)
- CodeCanyon (scripts)

Features:
- Auto-generates titles, descriptions, tags
- Sets pricing based on category/value
- Creates product packages (ZIP files)
- Uploads via API where available
- Generates listing preview files for manual upload
- Tracks all listings in database
- Supports batch processing
"""

import os
import csv
import json
import zipfile
import hashlib
import sqlite3
import random
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("⚠️  requests library not found. Install with: pip install requests")

# ============================================================
# Configuration
# ============================================================

EMPIRE_BASE = Path("/Users/steven/PYTHON_MARKETPLACE_EMPIRE")
INVENTORY_CSV = EMPIRE_BASE / "DOCUMENTATION" / "MASTER_INVENTORY.csv"
COPIED_INDEX_CSV = EMPIRE_BASE / "COPIED_FILES_INDEX.csv"
OUTPUT_DIR = EMPIRE_BASE / "AUTO_LISTINGS"
DATABASE_PATH = EMPIRE_BASE / "DOCUMENTATION" / "listings_database.db"

# Marketplace API Configs (set your keys here or in environment)
GUMROAD_ACCESS_TOKEN = os.getenv("GUMROAD_ACCESS_TOKEN", "")
UPWORK_API_KEY = os.getenv("UPWORK_API_KEY", "")
UPWORK_API_SECRET = os.getenv("UPWORK_API_SECRET", "")
FIVERR_API_KEY = os.getenv("FIVERR_API_KEY", "")
CODESTER_API_KEY = os.getenv("CODESTER_API_KEY", "")

# ============================================================
# Data Classes
# ============================================================

@dataclass
class ProductListing:
    """Represents a product listing for marketplaces."""
    # Core info
    product_id: str = ""
    title: str = ""
    description: str = ""
    short_description: str = ""
    category: str = ""
    subcategory: str = ""
    
    # Pricing
    price_basic: float = 0.0
    price_standard: float = 0.0
    price_premium: float = 0.0
    
    # Files
    files_included: List[str] = field(default_factory=list)
    file_count: int = 0
    package_size_mb: float = 0.0
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    features: List[str] = field(default_factory=list)
    use_cases: List[str] = field(default_factory=list)
    
    # Marketplace status
    gumroad_url: str = ""
    upwork_url: str = ""
    fiverr_url: str = ""
    codester_url: str = ""
    
    # Tracking
    created_date: str = ""
    status: str = "draft"  # draft, ready, uploaded, sold
    revenue: float = 0.0
    views: int = 0
    sales: int = 0
    
    # Source
    source_files: List[str] = field(default_factory=list)
    original_paths: List[str] = field(default_factory=list)


@dataclass
class MarketplaceConfig:
    """Configuration for a marketplace platform."""
    name: str
    api_endpoint: str
    requires_api: bool
    listing_type: str  # digital_product, service, gig
    max_title_length: int
    max_description_length: int
    max_tags: int
    fee_percentage: float
    payout_schedule: str


# ============================================================
# Marketplace Configurations
# ============================================================

MARKETPLACES = {
    "gumroad": MarketplaceConfig(
        name="Gumroad",
        api_endpoint="https://api.gumroad.com/v2/products",
        requires_api=True,
        listing_type="digital_product",
        max_title_length=255,
        max_description_length=100000,
        max_tags=20,
        fee_percentage=10.0,
        payout_schedule="weekly"
    ),
    "upwork": MarketplaceConfig(
        name="Upwork",
        api_endpoint="https://api.upwork.com/jobs",
        requires_api=True,
        listing_type="service",
        max_title_length=80,
        max_description_length=5000,
        max_tags=15,
        fee_percentage=20.0,
        payout_schedule="biweekly"
    ),
    "fiverr": MarketplaceConfig(
        name="Fiverr",
        api_endpoint="https://api.fiverr.com/gigs",
        requires_api=False,  # Manual upload via web
        listing_type="gig",
        max_title_length=80,
        max_description_length=1200,
        max_tags=5,
        fee_percentage=20.0,
        payout_schedule="14days"
    ),
    "codester": MarketplaceConfig(
        name="Codester",
        api_endpoint="https://www.codester.com/api/items",
        requires_api=True,
        listing_type="digital_product",
        max_title_length=100,
        max_description_length=10000,
        max_tags=20,
        fee_percentage=30.0,
        payout_schedule="monthly"
    ),
}

# ============================================================
# Pricing Engine
# ============================================================

class PricingEngine:
    """Calculate optimal pricing for scripts and bundles."""
    
    CATEGORY_PRICING = {
        "01_AI_LLM_TOOLS": {
            "basic": 99, "standard": 299, "premium": 799,
            "per_script": 49, "bundle_discount": 0.2
        },
        "02_AUTOMATION_BOTS": {
            "basic": 79, "standard": 199, "premium": 499,
            "per_script": 39, "bundle_discount": 0.2
        },
        "03_MEDIA_PROCESSING": {
            "basic": 59, "standard": 149, "premium": 399,
            "per_script": 29, "bundle_discount": 0.25
        },
        "04_BUSINESS_TOOLS": {
            "basic": 99, "standard": 299, "premium": 799,
            "per_script": 49, "bundle_discount": 0.15
        },
        "05_WEB_DEVELOPMENT": {
            "basic": 69, "standard": 179, "premium": 449,
            "per_script": 35, "bundle_discount": 0.2
        },
        "06_DATA_ANALYSIS": {
            "basic": 49, "standard": 129, "premium": 349,
            "per_script": 25, "bundle_discount": 0.25
        },
        "07_MARKETING_SEO": {
            "basic": 59, "standard": 149, "premium": 399,
            "per_script": 29, "bundle_discount": 0.2
        },
        "08_UTILITIES_SCRIPTS": {
            "basic": 29, "standard": 79, "premium": 199,
            "per_script": 15, "bundle_discount": 0.3
        },
    }
    
    @classmethod
    def calculate_bundle_price(cls, category: str, script_count: int, tier: str = "standard") -> float:
        """Calculate price for a bundle of scripts."""
        pricing = cls.CATEGORY_PRICING.get(category, cls.CATEGORY_PRICING["08_UTILITIES_SCRIPTS"])
        
        if tier == "basic":
            base_price = pricing["basic"]
        elif tier == "premium":
            base_price = pricing["premium"]
        else:
            base_price = pricing["standard"]
        
        # Scale with script count
        multiplier = 1 + (script_count - 1) * 0.3
        price = base_price * multiplier
        
        # Apply bundle discount for large bundles
        if script_count >= 10:
            price *= (1 - pricing["bundle_discount"])
        
        return round(price, -1)  # Round to nearest 10
    
    @classmethod
    def get_recommended_pricing(cls, category: str, script_count: int) -> Dict:
        """Get recommended pricing for all tiers."""
        return {
            "basic": cls.calculate_bundle_price(category, script_count, "basic"),
            "standard": cls.calculate_bundle_price(category, script_count, "standard"),
            "premium": cls.calculate_bundle_price(category, script_count, "premium"),
        }


# ============================================================
# Content Generator
# ============================================================

class ContentGenerator:
    """Generate listing titles, descriptions, tags, etc."""
    
    # Category-specific keywords and descriptions
    CATEGORY_INFO = {
        "01_AI_LLM_TOOLS": {
            "keywords": ["AI", "LLM", "GPT", "Machine Learning", "Neural Network", "Deep Learning", 
                        "ChatGPT", "LangChain", "OpenAI", "Anthropic", "AI Agent", "Automation"],
            "description_template": "Professional {count} Python AI/LLM scripts for {purpose}. "
                                   "Includes {features}. Perfect for {audience}.",
            "purposes": ["artificial intelligence development", "LLM fine-tuning", "AI agent creation",
                        "multi-LLM orchestration", "content generation", "voice processing"],
            "audiences": ["AI developers", "data scientists", "tech startups", "enterprise teams"]
        },
        "02_AUTOMATION_BOTS": {
            "keywords": ["Automation", "Bot", "Scraper", "Instagram", "YouTube", "Social Media",
                        "Web Scraping", "Data Extraction", "API", "Crawler"],
            "description_template": "Complete {count} Python automation scripts for {purpose}. "
                                   "Automate {tasks}. Save hours of manual work.",
            "purposes": ["social media management", "web scraping", "data collection",
                        "content automation", "competitor analysis"],
            "audiences": ["social media managers", "marketing agencies", "content creators", "business owners"],
            "tasks": ["posting and engagement", "data extraction", "content scheduling",
                     "analytics tracking", "follower growth"]
        },
        "03_MEDIA_PROCESSING": {
            "keywords": ["Media", "Audio", "Video", "Image", "Processing", "Transcription",
                        "Upscaling", "Gallery", "Conversion", "Editing"],
            "description_template": "Professional {count} Python media processing tools for {purpose}. "
                                   "Includes {features}. Production-ready code.",
            "purposes": ["audio transcription", "video editing", "image processing",
                        "gallery creation", "media conversion"],
            "audiences": ["content creators", "media professionals", "photographers", "video editors"],
            "features": ["batch processing", "AI-powered analysis", "multiple format support",
                        "cloud integration", "automated workflows"]
        },
        "04_BUSINESS_TOOLS": {
            "keywords": ["Business", "CRM", "Analytics", "Dashboard", "Lead Generation",
                        "Revenue Tracking", "Reporting", "Intelligence"],
            "description_template": "Complete {count} Python business tools for {purpose}. "
                                   "Streamline your {tasks}. Enterprise-grade quality.",
            "purposes": ["customer management", "business intelligence", "sales tracking",
                        "performance analytics", "revenue optimization"],
            "audiences": ["business owners", "sales teams", "managers", "entrepreneurs"],
            "tasks": ["client relationships", "data analysis", "reporting", "forecasting"]
        },
        "05_WEB_DEVELOPMENT": {
            "keywords": ["Web", "API", "FastAPI", "Flask", "Django", "Website", "Backend",
                        "REST", "Authentication", "Database"],
            "description_template": "Professional {count} Python web development scripts for {purpose}. "
                                   "Build {features} quickly and efficiently.",
            "purposes": ["web application development", "API creation", "website generation",
                        "backend services", "ecommerce integration"],
            "audiences": ["web developers", "startups", "agencies", "freelancers"],
            "features": ["RESTful APIs", "authentication systems", "database integrations",
                        "cloud deployment", "scalable architecture"]
        },
        "06_DATA_ANALYSIS": {
            "keywords": ["Data", "Analysis", "CSV", "Processing", "Cleaning", "Visualization",
                        "Pandas", "Analytics", "Reporting"],
            "description_template": "Complete {count} Python data analysis tools for {purpose}. "
                                   "Transform raw data into {outcomes}.",
            "purposes": ["data cleaning", "CSV processing", "statistical analysis",
                        "data visualization", "automated reporting"],
            "audiences": ["data analysts", "researchers", "business analysts", "data scientists"],
            "outcomes": ["actionable insights", "clean datasets", "visual reports",
                        "automated pipelines"]
        },
        "07_MARKETING_SEO": {
            "keywords": ["SEO", "Marketing", "Content", "Analytics", "Ranking", "Backlinks",
                        "Social Media", "Campaign", "Optimization"],
            "description_template": "Professional {count} Python marketing and SEO tools for {purpose}. "
                                   "Boost your {metrics} with automation.",
            "purposes": ["SEO optimization", "content marketing", "social media management",
                        "campaign tracking", "competitor analysis"],
            "audiences": ["marketers", "SEO specialists", "content creators", "agencies"],
            "metrics": ["search rankings", "organic traffic", "engagement rates", "conversion rates"]
        },
        "08_UTILITIES_SCRIPTS": {
            "keywords": ["Utility", "Automation", "File Management", "Batch Processing", "Converter",
                        "System", "Tools", "Productivity"],
            "description_template": "Essential {count} Python utility scripts for {purpose}. "
                                   "Automate {tasks} and save time.",
            "purposes": ["file management", "system automation", "batch processing",
                        "data conversion", "workflow optimization"],
            "audiences": ["developers", "system administrators", "power users", "IT professionals"],
            "tasks": ["file organization", "format conversion", "system maintenance", "data processing"]
        }
    }
    
    @classmethod
    def generate_title(cls, category: str, subcategory: str, script_count: int) -> str:
        """Generate an optimized product title."""
        
        # Clean category name
        clean_cat = category.replace("01_", "").replace("02_", "").replace("03_", "")
        clean_cat = clean_cat.replace("04_", "").replace("05_", "").replace("06_", "")
        clean_cat = clean_cat.replace("07_", "").replace("08_", "").replace("_", " ")
        
        # Clean subcategory
        clean_sub = subcategory.replace("_", " ").title()
        
        # Generate title variants
        titles = [
            f"{script_count}+ Python {clean_cat} Scripts - {clean_sub} Automation Bundle",
            f"Professional {clean_cat} Toolkit - {script_count} Python Scripts for {clean_sub}",
            f"Complete {clean_cat} Package - {script_count} Production-Ready Python Scripts",
            f"Python {clean_sub} Bundle - {script_count} Scripts for {clean_cat}",
            f"Ultimate {clean_cat} Collection - {script_count} Python Scripts + Documentation",
        ]
        
        # Pick best title based on script count
        if script_count >= 50:
            return titles[2]  # "Complete" for large bundles
        elif script_count >= 20:
            return titles[0]  # Count-focused for medium bundles
        else:
            return titles[1]  # "Professional" for small bundles
    
    @classmethod
    def generate_description(cls, category: str, script_count: int, features: List[str]) -> str:
        """Generate a comprehensive product description."""
        cat_info = cls.CATEGORY_INFO.get(category, cls.CATEGORY_INFO["08_UTILITIES_SCRIPTS"])
        
        purpose = random.choice(cat_info["purposes"])
        audience = random.choice(cat_info["audiences"])
        
        # Main description
        description = f"""# Professional Python {category.replace('_', ' ')} Bundle

## 📦 What's Included

This comprehensive package includes **{script_count} production-ready Python scripts** designed for {purpose}.

### ✨ Key Features

"""
        # Add features
        for i, feature in enumerate(features[:8], 1):
            description += f"{i}. **{feature}**\n"
        
        description += f"""
### 🎯 Perfect For

- {audience}
- Developers looking for production-ready code
- Teams wanting to accelerate development
- Businesses automating workflows

### 📋 What You Get

✅ **{script_count} Python Scripts** - Production-ready, well-documented code
✅ **Complete Documentation** - Setup guides and usage instructions
✅ **Example Usage** - Real-world implementation examples
✅ **Email Support** - Get help when you need it
✅ **Free Updates** - Lifetime access to improvements

### 🚀 Quick Start

1. Download and extract the package
2. Review the documentation
3. Install required dependencies (`pip install -r requirements.txt`)
4. Run the scripts with your data
5. Customize as needed for your use case

### 💼 Licensing

- **Personal Use:** Use in your own projects
- **Commercial Use:** Deploy in client projects
- **Resale Rights:** Cannot resell the scripts as-is

### 📞 Support

Need help? Contact us for:
- Installation assistance
- Customization guidance
- Bug fixes and updates
- Feature requests

---

**Category:** {category.replace('_', ' ')}
**Scripts:** {script_count}
**Format:** Python 3.x
**Support:** Email support included
"""
        
        return description
    
    @classmethod
    def generate_tags(cls, category: str, subcategory: str, max_tags: int = 15) -> List[str]:
        """Generate optimized tags for the listing."""
        cat_info = cls.CATEGORY_INFO.get(category, cls.CATEGORY_INFO["08_UTILITIES_SCRIPTS"])
        
        tags = []
        
        # Add category keywords
        tags.extend(cat_info["keywords"][:8])
        
        # Add subcategory-specific tags
        sub_tags = subcategory.replace("_", " ").split()
        tags.extend(sub_tags)
        
        # Add general tags
        tags.extend(["Python", "Automation", "Scripts", "Production-Ready"])
        
        # Remove duplicates and limit
        unique_tags = list(dict.fromkeys(tags))  # Preserve order
        return unique_tags[:max_tags]
    
    @classmethod
    def generate_requirements(cls, category: str) -> List[str]:
        """Generate list of requirements for the product."""
        base_requirements = [
            "Python 3.8 or higher",
            "pip package manager",
            "Basic Python knowledge",
        ]
        
        category_specific = {
            "01_AI_LLM_TOOLS": ["openai", "langchain", "transformers", "torch", "numpy"],
            "02_AUTOMATION_BOTS": ["requests", "selenium", "beautifulsoup4", "pandas"],
            "03_MEDIA_PROCESSING": ["Pillow", "opencv-python", "moviepy", "librosa"],
            "04_BUSINESS_TOOLS": ["pandas", "matplotlib", "plotly", "streamlit"],
            "05_WEB_DEVELOPMENT": ["fastapi", "uvicorn", "sqlalchemy", "pydantic"],
            "06_DATA_ANALYSIS": ["pandas", "numpy", "matplotlib", "seaborn"],
            "07_MARKETING_SEO": ["requests", "beautifulsoup4", "pandas", "matplotlib"],
            "08_UTILITIES_SCRIPTS": ["pathlib", "shutil", "os", "sys"],
        }
        
        return base_requirements + category_specific.get(category, [])


# ============================================================
# Package Creator
# ============================================================

class PackageCreator:
    """Create ZIP packages of scripts for upload."""
    
    @classmethod
    def create_package(cls, category: str, subcategory: str, 
                      scripts: List[Dict], output_dir: Path) -> Tuple[Path, float]:
        """Create a ZIP package of scripts."""
        
        # Generate package name
        clean_cat = category.replace("01_", "").replace("02_", "").replace("03_", "")
        clean_cat = clean_cat.replace("04_", "").replace("05_", "").replace("06_", "")
        clean_cat = clean_cat.replace("07_", "").replace("08_", "").replace("_", "-").lower()
        clean_sub = subcategory.replace("_", "-").lower()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        package_name = f"{clean_cat}-{clean_sub}-{len(scripts)}scripts-{timestamp}.zip"
        package_path = output_dir / package_name
        
        # Create ZIP
        total_size = 0
        with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add README
            readme_content = cls.generate_package_readme(category, subcategory, scripts)
            zipf.writestr("README.md", readme_content)
            
            # Add requirements.txt
            requirements = ContentGenerator.generate_requirements(category)
            zipf.writestr("requirements.txt", "\n".join(requirements))
            
            # Add scripts
            for script in scripts:
                src_path = Path(script['full_path'])
                if src_path.exists():
                    arcname = f"scripts/{script['file_name']}"
                    zipf.write(src_path, arcname)
                    total_size += src_path.stat().st_size
            
            # Add license
            license_content = cls.generate_license()
            zipf.writestr("LICENSE.txt", license_content)
        
        package_size_mb = package_path.stat().st_size / (1024 * 1024)
        return package_path, package_size_mb
    
    @classmethod
    def generate_package_readme(cls, category: str, subcategory: str, scripts: List[Dict]) -> str:
        """Generate README for the package."""
        return f"""# {category.replace('_', ' ')} - {subcategory.replace('_', ' ').title()}

## Overview

This package contains {len(scripts)} Python scripts for {subcategory.replace('_', ' ')}.

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

Browse the `scripts/` folder and choose the scripts you need.
Each script is documented with comments.

## Scripts Included

""" + "\n".join(f"- `{s['file_name']}`" for s in scripts[:20]) + f"""

{'... and more!' if len(scripts) > 20 else ''}

## Support

For questions or issues, please contact support.

## License

See LICENSE.txt for licensing information.
"""
    
    @classmethod
    def generate_license(cls) -> str:
        """Generate standard license."""
        return """PERSONAL & COMMERCIAL USE LICENSE

This license allows you to:
- Use the scripts in personal projects
- Use the scripts in commercial/client projects
- Modify and customize the scripts
- Deploy the scripts in production

This license does NOT allow you to:
- Resell or redistribute the scripts as-is
- Share the scripts publicly
- Include the scripts in open-source repositories
- Claim ownership of the original code

For extended licensing, please contact us.
"""


# ============================================================
# Database Manager
# ============================================================

class DatabaseManager:
    """SQLite database for tracking listings."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
    
    def create_tables(self):
        """Create database tables."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS listings (
                product_id TEXT PRIMARY KEY,
                title TEXT,
                description TEXT,
                category TEXT,
                subcategory TEXT,
                price_basic REAL,
                price_standard REAL,
                price_premium REAL,
                file_count INTEGER,
                package_path TEXT,
                package_size_mb REAL,
                tags TEXT,
                status TEXT DEFAULT 'draft',
                gumroad_url TEXT,
                upwork_url TEXT,
                fiverr_url TEXT,
                codester_url TEXT,
                created_date TEXT,
                views INTEGER DEFAULT 0,
                sales INTEGER DEFAULT 0,
                revenue REAL DEFAULT 0.0
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT,
                marketplace TEXT,
                sale_date TEXT,
                amount REAL,
                FOREIGN KEY (product_id) REFERENCES listings(product_id)
            )
        """)
        
        self.conn.commit()
    
    def save_listing(self, listing: ProductListing):
        """Save or update a listing."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO listings 
            (product_id, title, description, category, subcategory,
             price_basic, price_standard, price_premium, file_count,
             package_path, package_size_mb, tags, status,
             gumroad_url, upwork_url, fiverr_url, codester_url,
             created_date, views, sales, revenue)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            listing.product_id,
            listing.title,
            listing.description,
            listing.category,
            listing.subcategory,
            listing.price_basic,
            listing.price_standard,
            listing.price_premium,
            listing.file_count,
            listing.package_path,
            listing.package_size_mb,
            json.dumps(listing.tags),
            listing.status,
            listing.gumroad_url,
            listing.upwork_url,
            listing.fiverr_url,
            listing.codester_url,
            listing.created_date,
            listing.views,
            listing.sales,
            listing.revenue
        ))
        
        self.conn.commit()
    
    def get_all_listings(self) -> List[sqlite3.Row]:
        """Get all listings."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM listings ORDER BY created_date DESC")
        return cursor.fetchall()
    
    def get_stats(self) -> Dict:
        """Get listing statistics."""
        cursor = self.conn.cursor()
        
        stats = {}
        
        cursor.execute("SELECT COUNT(*) as count FROM listings")
        stats['total_listings'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM listings WHERE status = 'draft'")
        stats['drafts'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM listings WHERE status = 'uploaded'")
        stats['uploaded'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT SUM(sales) as total FROM listings")
        stats['total_sales'] = cursor.fetchone()['total'] or 0
        
        cursor.execute("SELECT SUM(revenue) as total FROM listings")
        stats['total_revenue'] = cursor.fetchone()['total'] or 0
        
        return stats
    
    def close(self):
        """Close database connection."""
        self.conn.close()


# ============================================================
# Marketplace Uploaders
# ============================================================

class GumroadUploader:
    """Upload products to Gumroad via API."""
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.gumroad.com/v2"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    
    def create_product(self, listing: ProductListing, package_path: Path) -> Dict:
        """Create a product on Gumroad."""
        if not self.access_token:
            return {"error": "No Gumroad access token configured"}
        
        url = f"{self.base_url}/products"
        
        # Prepare form data
        data = {
            "name": listing.title[:255],
            "description": listing.description,
            "price": int(listing.price_standard * 100),  # Gumroad uses cents
            "custom_permalink": listing.product_id,
            "custom_receipt": "Thank you for your purchase! Check your email for download links.",
            "custom_summary": listing.short_description[:255],
            "custom_fields": json.dumps([
                {"name": "Use Case", "tooltip": "What will you use this for?"}
            ]),
            "customizable_price": 1,
            "require_shipping": False,
            "published": False,  # Start as draft
            "file_info[]": str(package_path),
        }
        
        try:
            response = requests.post(url, headers=self.headers, data=data,
                                   files={"file": open(package_path, 'rb')})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def update_product(self, product_id: str, updates: Dict) -> Dict:
        """Update an existing product."""
        url = f"{self.base_url}/products/{product_id}"
        
        try:
            response = requests.put(url, headers=self.headers, data=updates)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}


class UpworkUploader:
    """Create project catalog listings on Upwork."""
    
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
    
    def create_project(self, listing: ProductListing) -> Dict:
        """Create a project catalog listing."""
        # Upwork requires manual creation via web interface
        # This generates the data needed for manual upload
        return {
            "title": listing.title[:80],
            "description": listing.description[:5000],
            "category": "Web, Mobile & Software Dev",
            "subcategory": "Scripts & Utilities",
            "pricing": {
                "basic": {"name": "Basic", "price": listing.price_basic,
                         "description": "Single script with documentation"},
                "standard": {"name": "Standard", "price": listing.price_standard,
                            "description": "5 scripts + documentation + support"},
                "premium": {"name": "Premium", "price": listing.price_premium,
                           "description": "Full package + customization + priority support"},
            },
            "tags": listing.tags[:15],
            "delivery_time": "3-7 days",
            "revisions": 2,
        }


class FiverrUploader:
    """Create gig listings on Fiverr."""
    
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
    
    def create_gig_data(self, listing: ProductListing) -> Dict:
        """Generate gig data for manual Fiverr upload."""
        return {
            "title": f"I will {listing.title.lower()[:80]}",
            "category": "Programming & Tech",
            "subcategory": "Scripts & Utilities",
            "description": listing.description[:1200],
            "packages": {
                "basic": {
                    "name": "Basic Package",
                    "description": "1-3 Python scripts with documentation",
                    "price": listing.price_basic,
                    "delivery_days": 3,
                    "revisions": 1,
                },
                "standard": {
                    "name": "Standard Package",
                    "description": "5-10 scripts + documentation + email support",
                    "price": listing.price_standard,
                    "delivery_days": 5,
                    "revisions": 2,
                },
                "premium": {
                    "name": "Premium Package",
                    "description": "Full package + customization + priority support",
                    "price": listing.price_premium,
                    "delivery_days": 7,
                    "revisions": 3,
                },
            },
            "tags": listing.tags[:5],  # Fiverr allows max 5 tags
            "requirements": "Please describe your use case and any specific requirements.",
        }


class CodesterUploader:
    """Upload items to Codester."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def create_item(self, listing: ProductListing, package_path: Path) -> Dict:
        """Create an item on Codester."""
        # Codester requires manual upload via web
        # This generates the listing data
        return {
            "name": listing.title[:100],
            "description": listing.description[:10000],
            "category": "Scripts & Code",
            "price": listing.price_standard,
            "tags": ",".join(listing.tags[:20]),
            "version": "1.0",
            "last_update": datetime.now().strftime("%Y-%m-%d"),
            "compatible_with": "Python 3.8+",
            "files_included": listing.files_included,
        }


# ============================================================
# Main Automation Engine
# ============================================================

class MarketplaceAutomationEngine:
    """Main engine for automating marketplace uploads."""
    
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.packages_dir = self.output_dir / "PACKAGES"
        self.listings_dir = self.output_dir / "LISTING_DATA"
        self.reports_dir = self.output_dir / "REPORTS"
        
        # Create directories
        for dir_path in [self.output_dir, self.packages_dir, self.listings_dir, self.reports_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self.db = DatabaseManager(DATABASE_PATH)
        
        # Initialize uploaders
        self.gumroad = GumroadUploader(GUMROAD_ACCESS_TOKEN)
        self.upwork = UpworkUploader(UPWORK_API_KEY, UPWORK_API_SECRET)
        self.fiverr = FiverrUploader(FIVERR_API_KEY)
        self.codester = CodesterUploader(CODESTER_API_KEY)
        
        # Load inventory
        self.inventory = self.load_inventory()
        
        print("✅ Automation engine initialized")
        print(f"   📦 Inventory loaded: {len(self.inventory)} scripts")
        print(f"   💾 Database: {DATABASE_PATH}")
    
    def load_inventory(self) -> List[Dict]:
        """Load inventory from CSV."""
        inventory = []
        
        # Try copied index first, then master inventory
        csv_files = [COPIED_INDEX_CSV, INVENTORY_CSV]
        
        for csv_file in csv_files:
            if csv_file.exists():
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        inventory.append(row)
                print(f"📊 Loaded {len(inventory)} scripts from {csv_file.name}")
                break
        
        return inventory
    
    def create_listings_for_category(self, category: str, subcategory: str = None,
                                     batch_size: int = 10) -> List[ProductListing]:
        """Create product listings for a category/subcategory."""
        
        print(f"\n🎯 Creating listings for {category}")
        if subcategory:
            print(f"   Subcategory: {subcategory}")
        
        # Filter scripts
        scripts = [s for s in self.inventory if s.get('assigned_category') == category]
        
        if subcategory:
            scripts = [s for s in scripts if s.get('assigned_subcategory') == subcategory]
        
        if not scripts:
            print(f"   ⚠️  No scripts found for {category}/{subcategory}")
            return []
        
        print(f"   📊 Found {len(scripts)} scripts")
        
        # Group into batches
        listings = []
        for i in range(0, len(scripts), batch_size):
            batch = scripts[i:i + batch_size]
            
            # Create listing
            listing = self.create_listing(category, subcategory or "mixed", batch)
            listings.append(listing)
            
            # Create package
            package_path, package_size = PackageCreator.create_package(
                category, subcategory or "mixed", batch, self.packages_dir
            )
            
            listing.package_path = str(package_path)
            listing.package_size_mb = package_size
            listing.file_count = len(batch)
            
            # Save to database
            self.db.save_listing(listing)
            
            # Generate listing data files
            self.save_listing_data(listing)
            
            print(f"   ✅ Created listing {len(listings)}: {listing.title[:60]}...")
        
        print(f"\n✅ Created {len(listings)} listings for {category}")
        return listings
    
    def create_listing(self, category: str, subcategory: str, 
                      scripts: List[Dict]) -> ProductListing:
        """Create a single product listing."""
        
        # Generate product ID
        product_id = hashlib.md5(
            f"{category}_{subcategory}_{len(scripts)}_{datetime.now()}".encode()
        ).hexdigest()[:12]
        
        # Generate content
        title = ContentGenerator.generate_title(category, subcategory, len(scripts))
        description = ContentGenerator.generate_description(
            category, len(scripts),
            [s.get('description', '') for s in scripts if s.get('description')]
        )
        tags = ContentGenerator.generate_tags(category, subcategory)
        pricing = PricingEngine.get_recommended_pricing(category, len(scripts))
        
        # Create listing
        listing = ProductListing(
            product_id=product_id,
            title=title,
            description=description,
            short_description=description[:200],
            category=category,
            subcategory=subcategory,
            price_basic=pricing['basic'],
            price_standard=pricing['standard'],
            price_premium=pricing['premium'],
            tags=tags,
            requirements=ContentGenerator.generate_requirements(category),
            features=[s.get('description', '') for s in scripts[:5] if s.get('description')],
            use_cases=[f"Use case {i+1}" for i in range(3)],
            source_files=[s['file_name'] for s in scripts],
            original_paths=[s['full_path'] for s in scripts],
            created_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status="ready"
        )
        
        return listing
    
    def save_listing_data(self, listing: ProductListing):
        """Save listing data to JSON files for manual upload."""
        
        # Gumroad listing
        gumroad_data = {
            "platform": "Gumroad",
            "title": listing.title,
            "description": listing.description,
            "price": listing.price_standard,
            "custom_permalink": listing.product_id,
            "tags": listing.tags,
            "file": listing.package_path,
            "published": False,
        }
        
        with open(self.listings_dir / f"gumroad_{listing.product_id}.json", 'w') as f:
            json.dump(gumroad_data, f, indent=2)
        
        # Fiverr listing
        fiverr_data = self.fiverr.create_gig_data(listing)
        fiverr_data["platform"] = "Fiverr"
        
        with open(self.listings_dir / f"fiverr_{listing.product_id}.json", 'w') as f:
            json.dump(fiverr_data, f, indent=2)
        
        # Upwork listing
        upwork_data = self.upwork.create_project(listing)
        upwork_data["platform"] = "Upwork"
        
        with open(self.listings_dir / f"upwork_{listing.product_id}.json", 'w') as f:
            json.dump(upwork_data, f, indent=2)
        
        # Codester listing
        codester_data = self.codester.create_item(listing, Path(listing.package_path))
        codester_data["platform"] = "Codester"
        
        with open(self.listings_dir / f"codester_{listing.product_id}.json", 'w') as f:
            json.dump(codester_data, f, indent=2)
    
    def upload_to_gumroad(self, listing: ProductListing) -> Dict:
        """Upload a listing to Gumroad."""
        print(f"\n📤 Uploading to Gumroad: {listing.title[:60]}...")
        
        if not listing.package_path:
            return {"error": "No package file found"}
        
        result = self.gumroad.create_product(listing, Path(listing.package_path))
        
        if "error" not in result:
            listing.gumroad_url = result.get("product", {}).get("url", "")
            listing.status = "uploaded"
            self.db.save_listing(listing)
            print(f"   ✅ Uploaded! URL: {listing.gumroad_url}")
        else:
            print(f"   ❌ Error: {result['error']}")
        
        return result
    
    def generate_upload_report(self, listings: List[ProductListing]) -> Path:
        """Generate a comprehensive upload report."""
        
        report_path = self.reports_dir / f"upload_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 📤 Marketplace Upload Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Listings:** {len(listings)}\n\n")
            
            f.write("## Summary\n\n")
            f.write("| Metric | Value |\n")
            f.write("|--------|-------|\n")
            f.write(f"| **Total Listings** | {len(listings)} |\n")
            
            ready = sum(1 for item in listings if item.status == "ready")
            uploaded = sum(1 for item in listings if item.status == "uploaded")
            f.write(f"| **Ready to Upload** | {ready} |\n")
            f.write(f"| **Uploaded** | {uploaded} |\n")
            
            total_value = sum(item.price_standard for item in listings)
            f.write(f"| **Total Value** | ${total_value:,.0f} |\n\n")
            
            f.write("## Listings\n\n")
            f.write("| Title | Category | Price | Status | Package |\n")
            f.write("|-------|----------|-------|--------|---------|\n")
            
            for listing in listings:
                status_emoji = "✅" if listing.status == "uploaded" else "📝"
                f.write(f"| {listing.title[:50]}... | {listing.category} | ")
                f.write(f"${listing.price_standard:.0f} | {status_emoji} {listing.status} | ")
                f.write(f"{listing.package_path} |\n")
            
            f.write("\n## Next Steps\n\n")
            f.write("1. Review the listing data files in `LISTING_DATA/`\n")
            f.write("2. Upload to marketplaces using the JSON files\n")
            f.write("3. Update URLs in the database\n")
            f.write("4. Monitor sales and views\n\n")
            
            f.write("---\n\n")
            f.write("**Generated by:** Python Marketplace Empire Automation\n")
        
        print(f"\n📄 Report saved: {report_path}")
        return report_path
    
    def run_full_automation(self, categories: List[str] = None, batch_size: int = 10):
        """Run full automation for all categories."""
        
        if categories is None:
            categories = list(set(s.get('assigned_category', '') for s in self.inventory))
        
        print("="*70)
        print("🚀 RUNNING FULL MARKETPLACE AUTOMATION")
        print("="*70)
        
        all_listings = []
        
        for category in sorted(categories):
            if not category:
                continue
            
            listings = self.create_listings_for_category(category, batch_size=batch_size)
            all_listings.extend(listings)
        
        # Generate report
        if all_listings:
            self.generate_upload_report(all_listings)
        
        # Print summary
        print("\n" + "="*70)
        print("✅ AUTOMATION COMPLETE!")
        print("="*70)
        print("\n📊 Summary:")
        print(f"   Total Listings Created: {len(all_listings)}")
        print(f"   Packages Created: {len(all_listings)}")
        print(f"   Database Updated: {DATABASE_PATH}")
        
        stats = self.db.get_stats()
        print("\n💾 Database Stats:")
        print(f"   Total Listings: {stats['total_listings']}")
        print(f"   Drafts: {stats['drafts']}")
        print(f"   Ready: {stats['total_listings'] - stats['drafts']}")
        
        print(f"\n📁 Output Directory: {self.output_dir}")
        print(f"   📦 Packages: {self.packages_dir}")
        print(f"   📝 Listing Data: {self.listings_dir}")
        print(f"   📊 Reports: {self.reports_dir}")
        
        print("\n🎯 Next Steps:")
        print("   1. Review listing data in LISTING_DATA/")
        print("   2. Upload to marketplaces (manual or API)")
        print("   3. Update URLs in database")
        print("   4. Monitor sales!")
        print("="*70)
    
    def close(self):
        """Clean up resources."""
        self.db.close()


# ============================================================
# CLI Interface
# ============================================================

def main():
    """Main CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Python Marketplace Empire - Automated Listing Uploader",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create listings for all categories
  python marketplace_uploader.py --run-all

  # Create listings for specific category
  python marketplace_uploader.py --category 01_AI_LLM_TOOLS

  # Create listings with custom batch size
  python marketplace_uploader.py --category 01_AI_LLM_TOOLS --batch-size 20

  # Upload to Gumroad (requires API token)
  python marketplace_uploader.py --upload-gumroad --product-id abc123

  # View database stats
  python marketplace_uploader.py --stats
        """
    )
    
    parser.add_argument("--run-all", action="store_true",
                       help="Run full automation for all categories")
    parser.add_argument("--category", type=str,
                       help="Process specific category (e.g., 01_AI_LLM_TOOLS)")
    parser.add_argument("--subcategory", type=str,
                       help="Process specific subcategory")
    parser.add_argument("--batch-size", type=int, default=10,
                       help="Number of scripts per listing (default: 10)")
    parser.add_argument("--upload-gumroad", action="store_true",
                       help="Upload to Gumroad (requires API token)")
    parser.add_argument("--product-id", type=str,
                       help="Product ID for upload operations")
    parser.add_argument("--stats", action="store_true",
                       help="Show database statistics")
    parser.add_argument("--export-csv", action="store_true",
                       help="Export listings to CSV")
    
    args = parser.parse_args()
    
    # Initialize engine
    engine = MarketplaceAutomationEngine()
    
    try:
        if args.stats:
            # Show stats
            stats = engine.db.get_stats()
            print("\n📊 Database Statistics:")
            print(f"   Total Listings: {stats['total_listings']}")
            print(f"   Drafts: {stats['drafts']}")
            print(f"   Uploaded: {stats['uploaded']}")
            print(f"   Total Sales: {stats['total_sales']}")
            print(f"   Total Revenue: ${stats['total_revenue']:,.0f}")
        
        elif args.upload_gumroad and args.product_id:
            # Upload specific product to Gumroad
            listings = engine.db.get_all_listings()
            listing = next((item for item in listings if item['product_id'] == args.product_id), None)
            
            if listing:
                # Convert to ProductListing
                product = ProductListing(**dict(listing))
                engine.upload_to_gumroad(product)
            else:
                print(f"❌ Product {args.product_id} not found")
        
        elif args.category:
            # Process specific category
            listings = engine.create_listings_for_category(
                args.category, args.subcategory, args.batch_size
            )
            engine.generate_upload_report(listings)
        
        elif args.run_all:
            # Run full automation
            engine.run_full_automation(batch_size=args.batch_size)
        
        elif args.export_csv:
            # Export to CSV
            listings = engine.db.get_all_listings()
            if listings:
                output_path = engine.reports_dir / "all_listings.csv"
                with open(output_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=listings[0].keys())
                    writer.writeheader()
                    for listing in listings:
                        writer.writerow(dict(listing))
                print(f"✅ Exported {len(listings)} listings to {output_path}")
            else:
                print("⚠️  No listings to export")
        
        else:
            parser.print_help()
    
    finally:
        engine.close()


if __name__ == "__main__":
    main()
