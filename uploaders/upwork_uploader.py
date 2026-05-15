#!/usr/bin/env python3
"""
UPWORK AUTOMATED LISTING CREATOR
=================================
Creates professional Upwork Project Catalog listings.

Note: Upwork doesn't have a public API for Project Catalog,
so this generates complete listing data for manual upload.

Features:
- Auto-generates titles, descriptions, tags
- Creates 3-tier pricing (Basic/Standard/Premium)
- Generates project requirements
- Creates listing preview files
- Tracks all listings in database

Usage:
  python3 upwork_uploader.py --run-all
  python3 upwork_uploader.py --category 01_AI_LLM_TOOLS
  python3 upwork_uploader.py --stats
  python3 upwork_uploader.py --export-csv
"""

import csv
import json
import sqlite3
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
OUTPUT_DIR = EMPIRE_BASE / "UPWORK_LISTINGS"
LISTINGS_DIR = OUTPUT_DIR / "LISTING_DATA"
REPORTS_DIR = OUTPUT_DIR / "REPORTS"
DATABASE_PATH = EMPIRE_BASE / "DOCUMENTATION" / "upwork_database.db"

# ============================================================
# Data Classes
# ============================================================

@dataclass
class UpworkListing:
    """Represents an Upwork Project Catalog listing."""
    listing_id: str = ""
    title: str = ""
    description: str = ""
    category: str = ""
    subcategory: str = ""
    
    # 3-Tier Pricing
    basic_name: str = "Basic"
    basic_description: str = ""
    basic_price: float = 0.0
    basic_delivery_days: int = 3
    basic_revisions: int = 1
    
    standard_name: str = "Standard"
    standard_description: str = ""
    standard_price: float = 0.0
    standard_delivery_days: int = 5
    standard_revisions: int = 2
    
    premium_name: str = "Premium"
    premium_description: str = ""
    premium_price: float = 0.0
    premium_delivery_days: int = 7
    premium_revisions: int = 3
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    requirements: str = ""
    features: List[str] = field(default_factory=list)
    file_count: int = 0
    source_files: List[str] = field(default_factory=list)
    
    # Tracking
    status: str = "draft"
    created_date: str = ""
    upwork_url: str = ""


# ============================================================
# Pricing Engine
# ============================================================

class UpworkPricing:
    """Calculate Upwork 3-tier pricing."""
    
    CATEGORY_PRICING = {
        "01_AI_LLM_TOOLS": {"basic": 500, "standard": 1500, "premium": 3000},
        "02_AUTOMATION_BOTS": {"basic": 300, "standard": 1000, "premium": 2500},
        "03_MEDIA_PROCESSING": {"basic": 250, "standard": 800, "premium": 2000},
        "04_BUSINESS_TOOLS": {"basic": 500, "standard": 1500, "premium": 3500},
        "05_WEB_DEVELOPMENT": {"basic": 400, "standard": 1200, "premium": 2800},
        "06_DATA_ANALYSIS": {"basic": 200, "standard": 700, "premium": 1800},
        "07_MARKETING_SEO": {"basic": 300, "standard": 900, "premium": 2200},
        "08_UTILITIES_SCRIPTS": {"basic": 150, "standard": 500, "premium": 1200},
    }
    
    @classmethod
    def get_pricing(cls, category: str, script_count: int) -> Dict:
        """Get 3-tier pricing."""
        pricing = cls.CATEGORY_PRICING.get(category, cls.CATEGORY_PRICING["08_UTILITIES_SCRIPTS"])
        
        # Scale with script count
        multiplier = 1 + (script_count - 1) * 0.2
        
        return {
            "basic": round(pricing["basic"] * multiplier, -1),
            "standard": round(pricing["standard"] * multiplier, -1),
            "premium": round(pricing["premium"] * multiplier, -1),
        }


# ============================================================
# Content Generator
# ============================================================

class UpworkContentGenerator:
    """Generate Upwork listing content."""
    
    CATEGORY_INFO = {
        "01_AI_LLM_TOOLS": {
            "title_prefix": "AI & LLM Development",
            "description": "Professional AI and LLM development services",
            "tags": ["AI", "Machine Learning", "LLM", "GPT", "Python", "OpenAI", "Automation"],
        },
        "02_AUTOMATION_BOTS": {
            "title_prefix": "Automation & Bot Development",
            "description": "Custom automation scripts and bot development",
            "tags": ["Automation", "Bot", "Scraper", "Python", "Social Media", "Web Scraping"],
        },
        "03_MEDIA_PROCESSING": {
            "title_prefix": "Media Processing Solutions",
            "description": "Audio, video, and image processing services",
            "tags": ["Media", "Audio", "Video", "Image", "Processing", "Python"],
        },
        "04_BUSINESS_TOOLS": {
            "title_prefix": "Business Tools & CRM",
            "description": "Custom business tools and CRM development",
            "tags": ["Business", "CRM", "Analytics", "Dashboard", "Python"],
        },
        "05_WEB_DEVELOPMENT": {
            "title_prefix": "Web Development & APIs",
            "description": "Professional web development and API creation",
            "tags": ["Web", "API", "FastAPI", "Flask", "Python", "Backend"],
        },
        "06_DATA_ANALYSIS": {
            "title_prefix": "Data Analysis & Processing",
            "description": "Expert data analysis and processing services",
            "tags": ["Data", "Analysis", "CSV", "Python", "Analytics"],
        },
        "07_MARKETING_SEO": {
            "title_prefix": "Marketing & SEO Automation",
            "description": "Marketing automation and SEO optimization",
            "tags": ["SEO", "Marketing", "Content", "Analytics", "Python"],
        },
        "08_UTILITIES_SCRIPTS": {
            "title_prefix": "Python Utilities & Scripts",
            "description": "Custom Python utilities and automation scripts",
            "tags": ["Python", "Utilities", "Automation", "Scripts", "Tools"],
        }
    }
    
    @classmethod
    def generate_title(cls, category: str, subcategory: str, script_count: int) -> str:
        """Generate Upwork title (max 80 chars)."""
        cat_info = cls.CATEGORY_INFO.get(category, cls.CATEGORY_INFO["08_UTILITIES_SCRIPTS"])
        clean_sub = subcategory.replace("_", " ").title()
        
        title = f"{cat_info['title_prefix']} - {clean_sub}"
        
        if len(title) > 75:
            title = title[:75] + "..."
        
        return title
    
    @classmethod
    def generate_description(cls, category: str, script_count: int) -> str:
        """Generate Upwork description."""
        cat_info = cls.CATEGORY_INFO.get(category, cls.CATEGORY_INFO["08_UTILITIES_SCRIPTS"])
        
        return f"""# {cat_info['description']}

## Overview

I offer professional Python development services with {script_count}+ production-ready scripts available for immediate delivery.

## What I Provide

✅ **Production-Ready Code** - Well-documented, tested scripts
✅ **Custom Development** - Tailored to your specific needs
✅ **Integration Support** - Help with system integration
✅ **Documentation** - Complete setup and usage guides
✅ **Ongoing Support** - Post-delivery assistance

## My Expertise

- Python 3.x development
- AI/ML integration
- API development
- Automation solutions
- Data processing pipelines
- Web applications

## Why Choose Me

- **Fast Delivery** - Pre-built scripts ready to customize
- **Quality Code** - Production-ready, well-documented
- **Expert Support** - Ongoing assistance included
- **Proven Track Record** - 1000s of scripts delivered

## Process

1. **Consultation** - Discuss your requirements
2. **Selection** - Choose from existing scripts or custom develop
3. **Customization** - Adapt to your needs
4. **Delivery** - Complete package with documentation
5. **Support** - Ongoing assistance

Ready to accelerate your project? Let's talk!
"""
    
    @classmethod
    def generate_tags(cls, category: str) -> List[str]:
        """Generate Upwork tags (max 15)."""
        cat_info = cls.CATEGORY_INFO.get(category, cls.CATEGORY_INFO["08_UTILITIES_SCRIPTS"])
        return cat_info["tags"][:15]
    
    @classmethod
    def generate_requirements(cls) -> str:
        """Generate project requirements text."""
        return """Please provide:
1. Detailed description of your requirements
2. Any specific features or functionality needed
3. Integration requirements with existing systems
4. Timeline and deadline expectations
5. Budget range for the project"""


# ============================================================
# Database Manager
# ============================================================

class UpworkDatabase:
    """SQLite database for Upwork listings."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
    
    def create_tables(self):
        """Create tables."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS listings (
                listing_id TEXT PRIMARY KEY,
                title TEXT,
                description TEXT,
                category TEXT,
                subcategory TEXT,
                basic_name TEXT,
                basic_description TEXT,
                basic_price REAL,
                basic_delivery_days INTEGER,
                basic_revisions INTEGER,
                standard_name TEXT,
                standard_description TEXT,
                standard_price REAL,
                standard_delivery_days INTEGER,
                standard_revisions INTEGER,
                premium_name TEXT,
                premium_description TEXT,
                premium_price REAL,
                premium_delivery_days INTEGER,
                premium_revisions INTEGER,
                tags TEXT,
                requirements TEXT,
                features TEXT,
                file_count INTEGER,
                status TEXT DEFAULT 'draft',
                created_date TEXT,
                upwork_url TEXT
            )
        """)
        self.conn.commit()
    
    def save_listing(self, listing: UpworkListing):
        """Save listing."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO listings 
            (listing_id, title, description, category, subcategory,
             basic_name, basic_description, basic_price, basic_delivery_days, basic_revisions,
             standard_name, standard_description, standard_price, standard_delivery_days, standard_revisions,
             premium_name, premium_description, premium_price, premium_delivery_days, premium_revisions,
             tags, requirements, features, file_count, status, created_date, upwork_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            listing.listing_id, listing.title, listing.description,
            listing.category, listing.subcategory,
            listing.basic_name, listing.basic_description, listing.basic_price,
            listing.basic_delivery_days, listing.basic_revisions,
            listing.standard_name, listing.standard_description, listing.standard_price,
            listing.standard_delivery_days, listing.standard_revisions,
            listing.premium_name, listing.premium_description, listing.premium_price,
            listing.premium_delivery_days, listing.premium_revisions,
            json.dumps(listing.tags), listing.requirements,
            json.dumps(listing.features), listing.file_count,
            listing.status, listing.created_date, listing.upwork_url
        ))
        self.conn.commit()
    
    def get_stats(self) -> Dict:
        """Get statistics."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM listings")
        total = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM listings WHERE status = 'ready'")
        ready = cursor.fetchone()['count']
        
        return {'total': total, 'ready': ready}
    
    def close(self):
        """Close connection."""
        self.conn.close()


# ============================================================
# Main Automation Engine
# ============================================================

class UpworkAutomationEngine:
    """Main Upwork automation engine."""
    
    def __init__(self):
        for dir_path in [OUTPUT_DIR, LISTINGS_DIR, REPORTS_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        self.db = UpworkDatabase(DATABASE_PATH)
        self.inventory = self.load_inventory()
        
        print("✅ Upwork Automation Engine initialized")
        print(f"   📦 Inventory: {len(self.inventory)} scripts")
        print(f"   💾 Database: {DATABASE_PATH}")
    
    def load_inventory(self) -> List[Dict]:
        """Load inventory."""
        if not INVENTORY_CSV.exists():
            return []
        
        with open(INVENTORY_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    def create_listings(self, category: str, batch_size: int = 10) -> List[UpworkListing]:
        """Create listings for a category."""
        print(f"\n🎯 Processing {category}")
        
        scripts = [s for s in self.inventory if s.get('assigned_category') == category]
        if not scripts:
            print("   ⚠️  No scripts found")
            return []
        
        print(f"   📊 Found {len(scripts)} scripts")
        
        listings = []
        for i in range(0, len(scripts), batch_size):
            batch = scripts[i:i + batch_size]
            subcategory = batch[0].get('assigned_subcategory', 'mixed')
            
            # Generate content
            listing_id = hashlib.md5(f"upwork_{category}_{i}_{datetime.now()}".encode()).hexdigest()[:12]
            title = UpworkContentGenerator.generate_title(category, subcategory, len(batch))
            description = UpworkContentGenerator.generate_description(category, len(batch))
            tags = UpworkContentGenerator.generate_tags(category)
            pricing = UpworkPricing.get_pricing(category, len(batch))
            
            # Create listing
            listing = UpworkListing(
                listing_id=listing_id,
                title=title,
                description=description,
                category=category,
                subcategory=subcategory,
                basic_name="Basic Package",
                basic_description=f"{min(3, len(batch))} Python scripts with documentation",
                basic_price=pricing['basic'],
                basic_delivery_days=3,
                basic_revisions=1,
                standard_name="Standard Package",
                standard_description=f"{min(10, len(batch))} Python scripts + documentation + email support",
                standard_price=pricing['standard'],
                standard_delivery_days=5,
                standard_revisions=2,
                premium_name="Premium Package",
                premium_description=f"All {len(batch)} scripts + customization + priority support",
                premium_price=pricing['premium'],
                premium_delivery_days=7,
                premium_revisions=3,
                tags=tags,
                requirements=UpworkContentGenerator.generate_requirements(),
                features=[f"{len(batch)} production-ready scripts", "Complete documentation", "Email support"],
                file_count=len(batch),
                source_files=[s['file_name'] for s in batch],
                created_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                status="ready"
            )
            
            # Save to database
            self.db.save_listing(listing)
            
            # Save JSON listing
            listing_data = {
                "platform": "Upwork",
                "listing_id": listing_id,
                "title": title,
                "description": description,
                "category": "Web, Mobile & Software Dev",
                "subcategory": "Scripts & Utilities",
                "pricing": {
                    "basic": {
                        "name": listing.basic_name,
                        "description": listing.basic_description,
                        "price": listing.basic_price,
                        "delivery_days": listing.basic_delivery_days,
                        "revisions": listing.basic_revisions,
                    },
                    "standard": {
                        "name": listing.standard_name,
                        "description": listing.standard_description,
                        "price": listing.standard_price,
                        "delivery_days": listing.standard_delivery_days,
                        "revisions": listing.standard_revisions,
                    },
                    "premium": {
                        "name": listing.premium_name,
                        "description": listing.premium_description,
                        "price": listing.premium_price,
                        "delivery_days": listing.premium_delivery_days,
                        "revisions": listing.premium_revisions,
                    },
                },
                "tags": tags,
                "requirements": listing.requirements,
            }
            
            with open(LISTINGS_DIR / f"{listing_id}.json", 'w') as f:
                json.dump(listing_data, f, indent=2)
            
            listings.append(listing)
            print(f"   ✅ Created listing {len(listings)}: {title[:60]}...")
        
        print(f"\n✅ Created {len(listings)} listings for {category}")
        return listings
    
    def run_full_automation(self, batch_size: int = 10):
        """Run full automation."""
        print("="*70)
        print("🚀 UPWORK FULL AUTOMATION")
        print("="*70)
        
        categories = list(set(s.get('assigned_category', '') for s in self.inventory if s.get('assigned_category')))
        
        all_listings = []
        for category in sorted(categories):
            listings = self.create_listings(category, batch_size)
            all_listings.extend(listings)
        
        # Generate report
        self.generate_report(all_listings)
        
        print("\n" + "="*70)
        print("✅ UPWORK AUTOMATION COMPLETE!")
        print("="*70)
        print("\n📊 Summary:")
        print(f"   Total Listings: {len(all_listings)}")
        
        stats = self.db.get_stats()
        print("\n💾 Database:")
        print(f"   Total: {stats['total']}")
        print(f"   Ready: {stats['ready']}")
        
        print(f"\n📁 Output: {OUTPUT_DIR}")
        print("\n📝 Next Steps:")
        print("   1. Review listings in LISTING_DATA/")
        print("   2. Go to Upwork Project Catalog")
        print("   3. Create new projects using JSON data")
        print("="*70)
    
    def generate_report(self, listings: List[UpworkListing]):
        """Generate report."""
        report_path = REPORTS_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(report_path, 'w') as f:
            f.write("# Upwork Project Catalog Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Listings:** {len(listings)}\n\n")
            
            f.write("| Title | Category | Basic | Standard | Premium | Status |\n")
            f.write("|-------|----------|-------|----------|---------|--------|\n")
            
            for listing in listings:
                status = "✅" if listing.status == "ready" else "📝"
                f.write(f"| {listing.title[:40]}... | {listing.category} | ")
                f.write(f"${listing.basic_price:.0f} | ${listing.standard_price:.0f} | ${listing.premium_price:.0f} | ")
                f.write(f"{status} |\n")
        
        print(f"\n📄 Report: {report_path}")
    
    def close(self):
        """Close resources."""
        self.db.close()


# ============================================================
# CLI
# ============================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Upwork Project Catalog Creator")
    parser.add_argument("--run-all", action="store_true", help="Run full automation")
    parser.add_argument("--category", type=str, help="Specific category")
    parser.add_argument("--batch-size", type=int, default=10, help="Scripts per listing")
    parser.add_argument("--stats", action="store_true", help="Show stats")
    parser.add_argument("--export-csv", action="store_true", help="Export to CSV")
    
    args = parser.parse_args()
    
    engine = UpworkAutomationEngine()
    
    try:
        if args.stats:
            stats = engine.db.get_stats()
            print("\n📊 Upwork Database Stats:")
            print(f"   Total Listings: {stats['total']}")
            print(f"   Ready to Upload: {stats['ready']}")
        
        elif args.category:
            listings = engine.create_listings(args.category, args.batch_size)
            engine.generate_report(listings)
        
        elif args.run_all:
            engine.run_full_automation(args.batch_size)
        
        elif args.export_csv:
            cursor = engine.db.conn.cursor()
            cursor.execute("SELECT * FROM listings")
            rows = cursor.fetchall()
            if rows:
                output_path = REPORTS_DIR / "listings.csv"
                with open(output_path, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                    writer.writeheader()
                    for row in rows:
                        writer.writerow(dict(row))
                print(f"✅ Exported {len(rows)} listings to {output_path}")
        
        else:
            parser.print_help()
    
    finally:
        engine.close()


if __name__ == "__main__":
    main()
