#!/usr/bin/env python3
"""
GUMROAD AUTOMATED UPLOADER
==========================
Automates creating and uploading product listings to Gumroad.

Features:
- Auto-generates titles, descriptions, tags
- Sets pricing based on category/value
- Creates product packages (ZIP files)
- Uploads via Gumroad API
- Tracks all listings in database
- Supports batch processing

Usage:
  python3 gumroad_uploader.py --run-all
  python3 gumroad_uploader.py --category 01_AI_LLM_TOOLS
  python3 gumroad_uploader.py --stats
  python3 gumroad_uploader.py --export-csv

Setup:
  export GUMROAD_ACCESS_TOKEN="your_token_here"
"""

import os
import csv
import json
import zipfile
import sqlite3
import hashlib
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
OUTPUT_DIR = EMPIRE_BASE / "GUMROAD_LISTINGS"
PACKAGES_DIR = OUTPUT_DIR / "PACKAGES"
LISTINGS_DIR = OUTPUT_DIR / "LISTING_DATA"
REPORTS_DIR = OUTPUT_DIR / "REPORTS"
DATABASE_PATH = EMPIRE_BASE / "DOCUMENTATION" / "gumroad_database.db"

GUMROAD_ACCESS_TOKEN = os.getenv("GUMROAD_ACCESS_TOKEN", "")
GUMROAD_API_URL = "https://api.gumroad.com/v2"

# ============================================================
# Data Classes
# ============================================================

@dataclass
class GumroadProduct:
    """Represents a Gumroad product listing."""
    product_id: str = ""
    name: str = ""
    description: str = ""
    custom_permalink: str = ""
    custom_summary: str = ""
    price: int = 0  # In cents
    categorized: bool = False
    category: str = ""
    subcategory: str = ""
    tags: List[str] = field(default_factory=list)
    file_count: int = 0
    package_path: str = ""
    package_size_mb: float = 0.0
    source_files: List[str] = field(default_factory=list)
    gumroad_url: str = ""
    status: str = "draft"  # draft, ready, uploaded, published
    created_date: str = ""
    views: int = 0
    sales: int = 0
    revenue: float = 0.0


# ============================================================
# Pricing Engine
# ============================================================

class GumroadPricing:
    """Calculate optimal Gumroad pricing."""
    
    CATEGORY_PRICING = {
        "01_AI_LLM_TOOLS": {"base": 299, "per_script": 49, "min": 99, "max": 999},
        "02_AUTOMATION_BOTS": {"base": 199, "per_script": 39, "min": 79, "max": 799},
        "03_MEDIA_PROCESSING": {"base": 149, "per_script": 29, "min": 59, "max": 599},
        "04_BUSINESS_TOOLS": {"base": 299, "per_script": 49, "min": 99, "max": 999},
        "05_WEB_DEVELOPMENT": {"base": 179, "per_script": 35, "min": 69, "max": 699},
        "06_DATA_ANALYSIS": {"base": 129, "per_script": 25, "min": 49, "max": 499},
        "07_MARKETING_SEO": {"base": 149, "per_script": 29, "min": 59, "max": 599},
        "08_UTILITIES_SCRIPTS": {"base": 79, "per_script": 15, "min": 29, "max": 299},
    }
    
    @classmethod
    def calculate_price(cls, category: str, script_count: int) -> int:
        """Calculate price in dollars."""
        pricing = cls.CATEGORY_PRICING.get(category, cls.CATEGORY_PRICING["08_UTILITIES_SCRIPTS"])
        
        price = pricing["base"] + (script_count - 1) * pricing["per_script"] * 0.3
        
        # Apply bundle discount for large bundles
        if script_count >= 10:
            price *= 0.8
        elif script_count >= 5:
            price *= 0.9
        
        # Clamp to min/max
        price = max(pricing["min"], min(pricing["max"], price))
        
        return round(price, -1)  # Round to nearest 10


# ============================================================
# Content Generator
# ============================================================

class GumroadContentGenerator:
    """Generate Gumroad product content."""
    
    CATEGORY_INFO = {
        "01_AI_LLM_TOOLS": {
            "keywords": ["AI", "LLM", "GPT", "Machine Learning", "Python Scripts", "Automation", "ChatGPT", "OpenAI"],
            "purpose": "artificial intelligence and LLM development",
            "audience": "AI developers and data scientists",
        },
        "02_AUTOMATION_BOTS": {
            "keywords": ["Automation", "Bot", "Scraper", "Instagram", "YouTube", "Social Media", "Python"],
            "purpose": "social media and web automation",
            "audience": "social media managers and marketers",
        },
        "03_MEDIA_PROCESSING": {
            "keywords": ["Media", "Audio", "Video", "Image", "Processing", "Transcription", "Python"],
            "purpose": "audio, video, and image processing",
            "audience": "content creators and media professionals",
        },
        "04_BUSINESS_TOOLS": {
            "keywords": ["Business", "CRM", "Analytics", "Dashboard", "Python Scripts", "Automation"],
            "purpose": "business intelligence and CRM",
            "audience": "business owners and managers",
        },
        "05_WEB_DEVELOPMENT": {
            "keywords": ["Web", "API", "FastAPI", "Flask", "Python", "Backend", "Development"],
            "purpose": "web application development",
            "audience": "web developers and startups",
        },
        "06_DATA_ANALYSIS": {
            "keywords": ["Data", "Analysis", "CSV", "Processing", "Python", "Analytics"],
            "purpose": "data analysis and processing",
            "audience": "data analysts and researchers",
        },
        "07_MARKETING_SEO": {
            "keywords": ["SEO", "Marketing", "Content", "Analytics", "Python", "Automation"],
            "purpose": "SEO and marketing automation",
            "audience": "marketers and SEO specialists",
        },
        "08_UTILITIES_SCRIPTS": {
            "keywords": ["Utility", "Automation", "File Management", "Python", "Tools", "Productivity"],
            "purpose": "file management and system automation",
            "audience": "developers and power users",
        }
    }
    
    @classmethod
    def generate_title(cls, category: str, subcategory: str, script_count: int) -> str:
        """Generate optimized Gumroad title."""
        clean_cat = category.replace("_", " ").replace("01 ", "").replace("02 ", "")
        clean_cat = clean_cat.replace("03 ", "").replace("04 ", "").replace("05 ", "")
        clean_cat = clean_cat.replace("06 ", "").replace("07 ", "").replace("08 ", "")
        clean_sub = subcategory.replace("_", " ").title()
        
        if script_count >= 50:
            return f"Ultimate {clean_cat} Bundle - {script_count}+ Python Scripts"
        elif script_count >= 20:
            return f"Complete {clean_cat} Toolkit - {script_count} Python Scripts"
        else:
            return f"Professional {clean_cat} Scripts - {clean_sub} ({script_count} Scripts)"
    
    @classmethod
    def generate_description(cls, category: str, script_count: int, features: List[str]) -> str:
        """Generate comprehensive Gumroad description."""
        cat_info = cls.CATEGORY_INFO.get(category, cls.CATEGORY_INFO["08_UTILITIES_SCRIPTS"])
        
        return f"""# Professional Python {category.replace('_', ' ')} Bundle

## 📦 What's Included

This comprehensive package includes **{script_count} production-ready Python scripts** designed for {cat_info['purpose']}.

### ✨ Key Features

""" + "\n".join(f"- ✅ **{f}**" for f in features[:10] if f) + f"""

### 🎯 Perfect For

- {cat_info['audience']}
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

Need help? Contact us for installation assistance and customization guidance.

---

**Category:** {category.replace('_', ' ')}
**Scripts:** {script_count}
**Format:** Python 3.x
**Support:** Email support included
"""
    
    @classmethod
    def generate_tags(cls, category: str, subcategory: str) -> List[str]:
        """Generate optimized Gumroad tags."""
        cat_info = cls.CATEGORY_INFO.get(category, cls.CATEGORY_INFO["08_UTILITIES_SCRIPTS"])
        
        tags = cat_info["keywords"][:]
        tags.extend(subcategory.replace("_", " ").split())
        tags.extend(["Python", "Scripts", "Automation", "Production-Ready"])
        
        # Remove duplicates and limit to 20
        return list(dict.fromkeys(tags))[:20]


# ============================================================
# Package Creator
# ============================================================

class GumroadPackageCreator:
    """Create ZIP packages for Gumroad."""
    
    @classmethod
    def create_package(cls, category: str, subcategory: str, 
                      scripts: List[Dict], output_dir: Path) -> Tuple[Path, float]:
        """Create a ZIP package."""
        
        clean_cat = category.replace("_", "-").lower()
        clean_sub = subcategory.replace("_", "-").lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        package_name = f"{clean_cat}-{clean_sub}-{len(scripts)}scripts-{timestamp}.zip"
        package_path = output_dir / package_name
        
        total_size = 0
        with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add README
            readme = cls.generate_readme(category, subcategory, scripts)
            zipf.writestr("README.md", readme)
            
            # Add requirements
            requirements = cls.generate_requirements(category)
            zipf.writestr("requirements.txt", "\n".join(requirements))
            
            # Add scripts
            for script in scripts:
                src_path = Path(script['full_path'])
                if src_path.exists():
                    arcname = f"scripts/{script['file_name']}"
                    zipf.write(src_path, arcname)
                    total_size += src_path.stat().st_size
            
            # Add license
            zipf.writestr("LICENSE.txt", cls.generate_license())
        
        package_size_mb = package_path.stat().st_size / (1024 * 1024)
        return package_path, package_size_mb
    
    @classmethod
    def generate_readme(cls, category: str, subcategory: str, scripts: List[Dict]) -> str:
        """Generate README for package."""
        return f"""# {category.replace('_', ' ')} - {subcategory.replace('_', ' ').title()}

## Overview

This package contains {len(scripts)} Python scripts for {subcategory.replace('_', ' ')}.

## Installation

```bash
pip install -r requirements.txt
```

## Scripts Included

""" + "\n".join(f"- `{s['file_name']}`" for s in scripts[:20]) + f"""

{'... and more!' if len(scripts) > 20 else ''}

## Support

For questions or issues, please contact support.
"""
    
    @classmethod
    def generate_requirements(cls, category: str) -> List[str]:
        """Generate requirements.txt."""
        return ["Python 3.8+", "pip", "See individual scripts for specific dependencies"]
    
    @classmethod
    def generate_license(cls) -> str:
        """Generate license."""
        return """PERSONAL & COMMERCIAL USE LICENSE

You can:
- Use in personal projects
- Use in commercial/client projects
- Modify and customize

You cannot:
- Resell or redistribute as-is
- Share publicly
- Include in open-source repos

For extended licensing, contact us.
"""


# ============================================================
# Database Manager
# ============================================================

class GumroadDatabase:
    """SQLite database for Gumroad listings."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
    
    def create_tables(self):
        """Create tables."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                custom_permalink TEXT,
                custom_summary TEXT,
                price INTEGER,
                category TEXT,
                subcategory TEXT,
                tags TEXT,
                file_count INTEGER,
                package_path TEXT,
                package_size_mb REAL,
                gumroad_url TEXT,
                status TEXT DEFAULT 'draft',
                created_date TEXT,
                views INTEGER DEFAULT 0,
                sales INTEGER DEFAULT 0,
                revenue REAL DEFAULT 0.0
            )
        """)
        self.conn.commit()
    
    def save_product(self, product: GumroadProduct):
        """Save product."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO products 
            (product_id, name, description, custom_permalink, custom_summary,
             price, category, subcategory, tags, file_count, package_path,
             package_size_mb, gumroad_url, status, created_date, views, sales, revenue)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            product.product_id, product.name, product.description,
            product.custom_permalink, product.custom_summary, product.price,
            product.category, product.subcategory, json.dumps(product.tags),
            product.file_count, product.package_path, product.package_size_mb,
            product.gumroad_url, product.status, product.created_date,
            product.views, product.sales, product.revenue
        ))
        self.conn.commit()
    
    def get_stats(self) -> Dict:
        """Get statistics."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM products")
        total = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM products WHERE status = 'uploaded'")
        uploaded = cursor.fetchone()['count']
        
        cursor.execute("SELECT SUM(sales) as total FROM products")
        sales = cursor.fetchone()['total'] or 0
        
        cursor.execute("SELECT SUM(revenue) as total FROM products")
        revenue = cursor.fetchone()['total'] or 0
        
        return {'total': total, 'uploaded': uploaded, 'sales': sales, 'revenue': revenue}
    
    def close(self):
        """Close connection."""
        self.conn.close()


# ============================================================
# Gumroad API Uploader
# ============================================================

class GumroadAPIUploader:
    """Upload products to Gumroad via API."""
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {"Authorization": f"Bearer {access_token}"}
    
    def upload_product(self, product: GumroadProduct) -> Dict:
        """Upload a product to Gumroad."""
        if not self.access_token:
            return {"error": "No access token. Set GUMROAD_ACCESS_TOKEN env var."}
        
        url = f"{GUMROAD_API_URL}/products"
        
        data = {
            "name": product.name[:255],
            "description": product.description,
            "price": product.price,
            "custom_permalink": product.custom_permalink,
            "custom_summary": product.custom_summary[:255],
            "customizable_price": 1,
            "require_shipping": False,
            "published": False,
        }
        
        try:
            with open(product.package_path, 'rb') as f:
                files = {"file": f}
                response = requests.post(url, headers=self.headers, data=data, files=files)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def publish_product(self, product_id: str) -> Dict:
        """Publish a product."""
        url = f"{GUMROAD_API_URL}/products/{product_id}"
        try:
            response = requests.put(url, headers=self.headers, data={"published": "true"})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}


# ============================================================
# Main Automation Engine
# ============================================================

class GumroadAutomationEngine:
    """Main Gumroad automation engine."""
    
    def __init__(self):
        # Create directories
        for dir_path in [OUTPUT_DIR, PACKAGES_DIR, LISTINGS_DIR, REPORTS_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        self.db = GumroadDatabase(DATABASE_PATH)
        self.api = GumroadAPIUploader(GUMROAD_ACCESS_TOKEN)
        self.inventory = self.load_inventory()
        
        print("✅ Gumroad Automation Engine initialized")
        print(f"   📦 Inventory: {len(self.inventory)} scripts")
        print(f"   💾 Database: {DATABASE_PATH}")
    
    def load_inventory(self) -> List[Dict]:
        """Load inventory."""
        if not INVENTORY_CSV.exists():
            print(f"❌ Inventory not found: {INVENTORY_CSV}")
            return []
        
        with open(INVENTORY_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    def create_listings(self, category: str, batch_size: int = 15) -> List[GumroadProduct]:
        """Create product listings for a category."""
        print(f"\n🎯 Processing {category}")
        
        scripts = [s for s in self.inventory if s.get('assigned_category') == category]
        if not scripts:
            print("   ⚠️  No scripts found")
            return []
        
        print(f"   📊 Found {len(scripts)} scripts")
        
        listings = []
        for i in range(0, len(scripts), batch_size):
            batch = scripts[i:i + batch_size]
            
            # Create product
            product_id = hashlib.md5(f"{category}_{i}_{datetime.now()}".encode()).hexdigest()[:12]
            subcategory = batch[0].get('assigned_subcategory', 'mixed')
            
            price = GumroadPricing.calculate_price(category, len(batch))
            title = GumroadContentGenerator.generate_title(category, subcategory, len(batch))
            description = GumroadContentGenerator.generate_description(category, len(batch), [])
            tags = GumroadContentGenerator.generate_tags(category, subcategory)
            
            # Create package
            package_path, package_size = GumroadPackageCreator.create_package(
                category, subcategory, batch, PACKAGES_DIR
            )
            
            product = GumroadProduct(
                product_id=product_id,
                name=title,
                description=description,
                custom_permalink=f"{category.lower()}-{subcategory.lower()}-{i//batch_size + 1}",
                custom_summary=description[:200],
                price=price * 100,  # Convert to cents
                category=category,
                subcategory=subcategory,
                tags=tags,
                file_count=len(batch),
                package_path=str(package_path),
                package_size_mb=package_size,
                source_files=[s['file_name'] for s in batch],
                created_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                status="ready"
            )
            
            # Save to database
            self.db.save_product(product)
            
            # Save JSON listing
            listing_data = {
                "platform": "Gumroad",
                "product_id": product_id,
                "name": title,
                "description": description,
                "price": price,
                "custom_permalink": product.custom_permalink,
                "tags": tags,
                "package": str(package_path),
                "published": False,
            }
            
            with open(LISTINGS_DIR / f"{product_id}.json", 'w') as f:
                json.dump(listing_data, f, indent=2)
            
            listings.append(product)
            print(f"   ✅ Created listing {len(listings)}: {title[:60]}...")
        
        print(f"\n✅ Created {len(listings)} listings for {category}")
        return listings
    
    def upload_to_gumroad(self, product: GumroadProduct) -> Dict:
        """Upload product to Gumroad."""
        print(f"\n📤 Uploading: {product.name[:60]}...")
        
        result = self.api.upload_product(product)
        
        if "error" not in result:
            product.gumroad_url = result.get("product", {}).get("url", "")
            product.status = "uploaded"
            self.db.save_product(product)
            print(f"   ✅ Uploaded! {product.gumroad_url}")
        else:
            print(f"   ❌ Error: {result['error']}")
        
        return result
    
    def run_full_automation(self, batch_size: int = 15):
        """Run full automation."""
        print("="*70)
        print("🚀 GUMROAD FULL AUTOMATION")
        print("="*70)
        
        categories = list(set(s.get('assigned_category', '') for s in self.inventory if s.get('assigned_category')))
        
        all_listings = []
        for category in sorted(categories):
            listings = self.create_listings(category, batch_size)
            all_listings.extend(listings)
        
        # Generate report
        self.generate_report(all_listings)
        
        print("\n" + "="*70)
        print("✅ GUMROAD AUTOMATION COMPLETE!")
        print("="*70)
        print("\n📊 Summary:")
        print(f"   Total Listings: {len(all_listings)}")
        print(f"   Packages: {len(all_listings)}")
        
        stats = self.db.get_stats()
        print("\n💾 Database:")
        print(f"   Total: {stats['total']}")
        print(f"   Uploaded: {stats['uploaded']}")
        print(f"   Sales: {stats['sales']}")
        print(f"   Revenue: ${stats['revenue']:,.0f}")
        
        print(f"\n📁 Output: {OUTPUT_DIR}")
        print("="*70)
    
    def generate_report(self, listings: List[GumroadProduct]):
        """Generate report."""
        report_path = REPORTS_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(report_path, 'w') as f:
            f.write("# Gumroad Upload Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Listings:** {len(listings)}\n\n")
            
            f.write("| Title | Category | Price | Status |\n")
            f.write("|-------|----------|-------|--------|\n")
            
            for p in listings:
                status = "✅" if p.status == "uploaded" else "📝"
                f.write(f"| {p.name[:50]}... | {p.category} | ${p.price/100:.0f} | {status} |\n")
        
        print(f"\n📄 Report: {report_path}")
    
    def close(self):
        """Close resources."""
        self.db.close()


# ============================================================
# CLI
# ============================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Gumroad Automated Uploader")
    parser.add_argument("--run-all", action="store_true", help="Run full automation")
    parser.add_argument("--category", type=str, help="Specific category")
    parser.add_argument("--batch-size", type=int, default=15, help="Scripts per package")
    parser.add_argument("--upload", action="store_true", help="Upload to Gumroad")
    parser.add_argument("--product-id", type=str, help="Product ID to upload")
    parser.add_argument("--stats", action="store_true", help="Show stats")
    parser.add_argument("--export-csv", action="store_true", help="Export to CSV")
    
    args = parser.parse_args()
    
    engine = GumroadAutomationEngine()
    
    try:
        if args.stats:
            stats = engine.db.get_stats()
            print("\n📊 Gumroad Database Stats:")
            print(f"   Total Products: {stats['total']}")
            print(f"   Uploaded: {stats['uploaded']}")
            print(f"   Sales: {stats['sales']}")
            print(f"   Revenue: ${stats['revenue']:,.0f}")
        
        elif args.upload and args.product_id:
            # Upload specific product
            cursor = engine.db.conn.cursor()
            cursor.execute("SELECT * FROM products WHERE product_id = ?", (args.product_id,))
            row = cursor.fetchone()
            if row:
                product = GumroadProduct(**dict(row))
                engine.upload_to_gumroad(product)
            else:
                print(f"❌ Product {args.product_id} not found")
        
        elif args.category:
            listings = engine.create_listings(args.category, args.batch_size)
            engine.generate_report(listings)
        
        elif args.run_all:
            engine.run_full_automation(args.batch_size)
        
        elif args.export_csv:
            cursor = engine.db.conn.cursor()
            cursor.execute("SELECT * FROM products")
            rows = cursor.fetchall()
            if rows:
                output_path = REPORTS_DIR / "products.csv"
                with open(output_path, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                    writer.writeheader()
                    for row in rows:
                        writer.writerow(dict(row))
                print(f"✅ Exported {len(rows)} products to {output_path}")
        
        else:
            parser.print_help()
    
    finally:
        engine.close()


if __name__ == "__main__":
    main()
