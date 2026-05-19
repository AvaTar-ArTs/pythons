#!/usr/bin/env python3
"""
CODESTER AUTOMATED LISTING CREATOR
===================================
Creates professional Codester item listings.

Note: Codester has limited API access,
so this generates complete listing data for manual upload.

Features:
- Auto-generates titles, descriptions, tags
- Sets pricing based on category/value
- Creates version info and compatibility
- Generates listing preview files
- Tracks all listings in database

Usage:
  python3 codester_uploader.py --run-all
  python3 codester_uploader.py --category 01_AI_LLM_TOOLS
  python3 codester_uploader.py --stats
  python3 codester_uploader.py --export-csv
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
OUTPUT_DIR = EMPIRE_BASE / "CODESTER_LISTINGS"
LISTINGS_DIR = OUTPUT_DIR / "ITEM_DATA"
REPORTS_DIR = OUTPUT_DIR / "REPORTS"
DATABASE_PATH = EMPIRE_BASE / "DOCUMENTATION" / "codester_database.db"

# ============================================================
# Data Classes
# ============================================================

@dataclass
class CodesterItem:
    """Represents a Codester item listing."""
    item_id: str = ""
    name: str = ""
    description: str = ""
    short_description: str = ""
    category: str = ""
    subcategory: str = ""
    
    # Pricing
    price: float = 0.0
    extended_license_price: float = 0.0
    
    # Version & Compatibility
    version: str = "1.0"
    last_update: str = ""
    compatible_with: str = "Python 3.8+"
    files_included: List[str] = field(default_factory=list)
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    features: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    file_count: int = 0
    source_files: List[str] = field(default_factory=list)
    
    # Tracking
    status: str = "draft"
    created_date: str = ""
    codester_url: str = ""


# ============================================================
# Pricing Engine
# ============================================================

class CodesterPricing:
    """Calculate Codester pricing."""
    
    CATEGORY_PRICING = {
        "01_AI_LLM_TOOLS": {"base": 49, "per_script": 5, "min": 29, "max": 299},
        "02_AUTOMATION_BOTS": {"base": 39, "per_script": 4, "min": 19, "max": 199},
        "03_MEDIA_PROCESSING": {"base": 29, "per_script": 3, "min": 15, "max": 149},
        "04_BUSINESS_TOOLS": {"base": 49, "per_script": 5, "min": 29, "max": 249},
        "05_WEB_DEVELOPMENT": {"base": 39, "per_script": 4, "min": 19, "max": 199},
        "06_DATA_ANALYSIS": {"base": 25, "per_script": 3, "min": 12, "max": 129},
        "07_MARKETING_SEO": {"base": 29, "per_script": 3, "min": 15, "max": 149},
        "08_UTILITIES_SCRIPTS": {"base": 15, "per_script": 2, "min": 9, "max": 99},
    }
    
    @classmethod
    def calculate_price(cls, category: str, script_count: int) -> float:
        """Calculate item price."""
        pricing = cls.CATEGORY_PRICING.get(category, cls.CATEGORY_PRICING["08_UTILITIES_SCRIPTS"])
        
        price = pricing["base"] + (script_count - 1) * pricing["per_script"]
        
        # Bundle discount
        if script_count >= 10:
            price *= 0.75
        elif script_count >= 5:
            price *= 0.85
        
        price = max(pricing["min"], min(pricing["max"], price))
        return round(price, -1)
    
    @classmethod
    def get_extended_license_price(cls, base_price: float) -> float:
        """Calculate extended license price (typically 2-3x base)."""
        return round(base_price * 2.5, -1)


# ============================================================
# Content Generator
# ============================================================

class CodesterContentGenerator:
    """Generate Codester item content."""
    
    CATEGORY_INFO = {
        "01_AI_LLM_TOOLS": {
            "name_prefix": "AI & LLM Python Scripts",
            "category": "Scripts & Code",
            "subcategory": "Python",
            "tags": ["AI", "LLM", "GPT", "Machine Learning", "Python", "OpenAI", "Automation", "ChatGPT"],
        },
        "02_AUTOMATION_BOTS": {
            "name_prefix": "Automation Scripts & Bots",
            "category": "Scripts & Code",
            "subcategory": "Python",
            "tags": ["Automation", "Bot", "Scraper", "Python", "Social Media", "Web Scraping"],
        },
        "03_MEDIA_PROCESSING": {
            "name_prefix": "Media Processing Scripts",
            "category": "Scripts & Code",
            "subcategory": "Python",
            "tags": ["Media", "Audio", "Video", "Image", "Processing", "Python"],
        },
        "04_BUSINESS_TOOLS": {
            "name_prefix": "Business Tools & CRM",
            "category": "Scripts & Code",
            "subcategory": "PHP",
            "tags": ["Business", "CRM", "Analytics", "Dashboard", "PHP", "Python"],
        },
        "05_WEB_DEVELOPMENT": {
            "name_prefix": "Web Development Scripts",
            "category": "Scripts & Code",
            "subcategory": "PHP",
            "tags": ["Web", "API", "PHP", "Python", "FastAPI", "Backend"],
        },
        "06_DATA_ANALYSIS": {
            "name_prefix": "Data Analysis Scripts",
            "category": "Scripts & Code",
            "subcategory": "Python",
            "tags": ["Data", "Analysis", "CSV", "Python", "Analytics"],
        },
        "07_MARKETING_SEO": {
            "name_prefix": "Marketing & SEO Scripts",
            "category": "Scripts & Code",
            "subcategory": "PHP",
            "tags": ["SEO", "Marketing", "Content", "Analytics", "PHP", "Python"],
        },
        "08_UTILITIES_SCRIPTS": {
            "name_prefix": "Utility Scripts & Tools",
            "category": "Scripts & Code",
            "subcategory": "Python",
            "tags": ["Utility", "Automation", "Python", "Scripts", "Tools"],
        }
    }
    
    @classmethod
    def generate_name(cls, category: str, subcategory: str, script_count: int) -> str:
        """Generate item name."""
        cat_info = cls.CATEGORY_INFO.get(category, cls.CATEGORY_INFO["08_UTILITIES_SCRIPTS"])
        clean_sub = subcategory.replace("_", " ").title()
        
        return f"{cat_info['name_prefix']} - {clean_sub} ({script_count} Scripts)"
    
    @classmethod
    def generate_description(cls, category: str, script_count: int, features: List[str]) -> str:
        """Generate item description."""
        
        return f"""<h2>Professional Python Scripts for {category.replace('_', ' ')}</h2>

<p>This package includes <strong>{script_count} production-ready Python scripts</strong> designed for professional use.</p>

<h3>Features</h3>
<ul>
""" + "\n".join(f"<li>✅ {f}</li>" for f in features[:10] if f) + f"""
</ul>

<h3>What's Included</h3>
<ul>
<li>✅ {script_count} Python Scripts - Production-ready code</li>
<li>✅ Complete Documentation - Setup and usage guides</li>
<li>✅ Example Usage - Real-world examples</li>
<li>✅ Email Support - Get help when needed</li>
<li>✅ Free Updates - Lifetime improvements</li>
</ul>

<h3>Requirements</h3>
<ul>
<li>Python 3.8 or higher</li>
<li>pip package manager</li>
<li>Basic Python knowledge</li>
</ul>

<h3>Support</h3>
<p>For questions or issues, please contact us through the support form.</p>
"""
    
    @classmethod
    def generate_tags(cls, category: str) -> List[str]:
        """Generate tags."""
        cat_info = cls.CATEGORY_INFO.get(category, cls.CATEGORY_INFO["08_UTILITIES_SCRIPTS"])
        return cat_info["tags"][:20]


# ============================================================
# Database Manager
# ============================================================

class CodesterDatabase:
    """SQLite database for Codester items."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
    
    def create_tables(self):
        """Create tables."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                item_id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                short_description TEXT,
                category TEXT,
                subcategory TEXT,
                price REAL,
                extended_license_price REAL,
                version TEXT,
                last_update TEXT,
                compatible_with TEXT,
                files_included TEXT,
                tags TEXT,
                features TEXT,
                requirements TEXT,
                file_count INTEGER,
                status TEXT DEFAULT 'draft',
                created_date TEXT,
                codester_url TEXT
            )
        """)
        self.conn.commit()
    
    def save_item(self, item: CodesterItem):
        """Save item."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO items 
            (item_id, name, description, short_description, category, subcategory,
             price, extended_license_price, version, last_update, compatible_with,
             files_included, tags, features, requirements, file_count, status, created_date, codester_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.item_id, item.name, item.description, item.short_description,
            item.category, item.subcategory, item.price, item.extended_license_price,
            item.version, item.last_update, item.compatible_with,
            json.dumps(item.files_included), json.dumps(item.tags),
            json.dumps(item.features), json.dumps(item.requirements),
            item.file_count, item.status, item.created_date, item.codester_url
        ))
        self.conn.commit()
    
    def get_stats(self) -> Dict:
        """Get statistics."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM items")
        total = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM items WHERE status = 'ready'")
        ready = cursor.fetchone()['count']
        
        return {'total': total, 'ready': ready}
    
    def close(self):
        """Close connection."""
        self.conn.close()


# ============================================================
# Main Automation Engine
# ============================================================

class CodesterAutomationEngine:
    """Main Codester automation engine."""
    
    def __init__(self):
        for dir_path in [OUTPUT_DIR, LISTINGS_DIR, REPORTS_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        self.db = CodesterDatabase(DATABASE_PATH)
        self.inventory = self.load_inventory()
        
        print("✅ Codester Automation Engine initialized")
        print(f"   📦 Inventory: {len(self.inventory)} scripts")
        print(f"   💾 Database: {DATABASE_PATH}")
    
    def load_inventory(self) -> List[Dict]:
        """Load inventory."""
        if not INVENTORY_CSV.exists():
            return []
        
        with open(INVENTORY_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    def create_items(self, category: str, batch_size: int = 15) -> List[CodesterItem]:
        """Create items for a category."""
        print(f"\n🎯 Processing {category}")
        
        scripts = [s for s in self.inventory if s.get('assigned_category') == category]
        if not scripts:
            print("   ⚠️  No scripts found")
            return []
        
        print(f"   📊 Found {len(scripts)} scripts")
        
        items = []
        for i in range(0, len(scripts), batch_size):
            batch = scripts[i:i + batch_size]
            subcategory = batch[0].get('assigned_subcategory', 'mixed')
            
            # Generate content
            item_id = hashlib.md5(f"codester_{category}_{i}_{datetime.now()}".encode()).hexdigest()[:12]
            name = CodesterContentGenerator.generate_name(category, subcategory, len(batch))
            description = CodesterContentGenerator.generate_description(category, len(batch), [])
            tags = CodesterContentGenerator.generate_tags(category)
            price = CodesterPricing.calculate_price(category, len(batch))
            extended_price = CodesterPricing.get_extended_license_price(price)
            
            cat_info = CodesterContentGenerator.CATEGORY_INFO.get(category, {})
            
            # Create item
            item = CodesterItem(
                item_id=item_id,
                name=name,
                description=description,
                short_description=description[:200],
                category=category,
                subcategory=subcategory,
                price=price,
                extended_license_price=extended_price,
                version="1.0",
                last_update=datetime.now().strftime("%Y-%m-%d"),
                compatible_with="Python 3.8+",
                files_included=["Python Scripts", "Documentation", "Requirements"],
                tags=tags,
                features=[f"{len(batch)} production-ready scripts", "Complete documentation", "Email support"],
                requirements=["Python 3.8+", "pip", "Basic Python knowledge"],
                file_count=len(batch),
                source_files=[s['file_name'] for s in batch],
                created_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                status="ready"
            )
            
            # Save to database
            self.db.save_item(item)
            
            # Save JSON item data
            item_data = {
                "platform": "Codester",
                "item_id": item_id,
                "name": name,
                "description": description,
                "category": cat_info.get("category", "Scripts & Code"),
                "subcategory": cat_info.get("subcategory", "Python"),
                "price": price,
                "extended_license_price": extended_price,
                "version": "1.0",
                "last_update": item.last_update,
                "compatible_with": item.compatible_with,
                "tags": tags,
                "features": item.features,
                "requirements": item.requirements,
            }
            
            with open(LISTINGS_DIR / f"{item_id}.json", 'w') as f:
                json.dump(item_data, f, indent=2)
            
            items.append(item)
            print(f"   ✅ Created item {len(items)}: {name[:60]}...")
        
        print(f"\n✅ Created {len(items)} items for {category}")
        return items
    
    def run_full_automation(self, batch_size: int = 15):
        """Run full automation."""
        print("="*70)
        print("🚀 CODESTER FULL AUTOMATION")
        print("="*70)
        
        categories = list(set(s.get('assigned_category', '') for s in self.inventory if s.get('assigned_category')))
        
        all_items = []
        for category in sorted(categories):
            items = self.create_items(category, batch_size)
            all_items.extend(items)
        
        # Generate report
        self.generate_report(all_items)
        
        print("\n" + "="*70)
        print("✅ CODESTER AUTOMATION COMPLETE!")
        print("="*70)
        print("\n📊 Summary:")
        print(f"   Total Items: {len(all_items)}")
        
        stats = self.db.get_stats()
        print("\n💾 Database:")
        print(f"   Total: {stats['total']}")
        print(f"   Ready: {stats['ready']}")
        
        print(f"\n📁 Output: {OUTPUT_DIR}")
        print("\n📝 Next Steps:")
        print("   1. Review item data in ITEM_DATA/")
        print("   2. Go to Codester.com")
        print("   3. Submit new items using JSON data")
        print("="*70)
    
    def generate_report(self, items: List[CodesterItem]):
        """Generate report."""
        report_path = REPORTS_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(report_path, 'w') as f:
            f.write("# Codester Item Submission Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Items:** {len(items)}\n\n")
            
            f.write("| Name | Category | Price | Extended | Status |\n")
            f.write("|------|----------|-------|----------|--------|\n")
            
            for it in items:
                status = "✅" if it.status == "ready" else "📝"
                f.write(f"| {it.name[:40]}... | {it.category} | ")
                f.write(f"${it.price:.0f} | ${it.extended_license_price:.0f} | {status} |\n")
        
        print(f"\n📄 Report: {report_path}")
    
    def close(self):
        """Close resources."""
        self.db.close()


# ============================================================
# CLI
# ============================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Codester Item Creator")
    parser.add_argument("--run-all", action="store_true", help="Run full automation")
    parser.add_argument("--category", type=str, help="Specific category")
    parser.add_argument("--batch-size", type=int, default=15, help="Scripts per item")
    parser.add_argument("--stats", action="store_true", help="Show stats")
    parser.add_argument("--export-csv", action="store_true", help="Export to CSV")
    
    args = parser.parse_args()
    
    engine = CodesterAutomationEngine()
    
    try:
        if args.stats:
            stats = engine.db.get_stats()
            print("\n📊 Codester Database Stats:")
            print(f"   Total Items: {stats['total']}")
            print(f"   Ready to Submit: {stats['ready']}")
        
        elif args.category:
            items = engine.create_items(args.category, args.batch_size)
            engine.generate_report(items)
        
        elif args.run_all:
            engine.run_full_automation(args.batch_size)
        
        elif args.export_csv:
            cursor = engine.db.conn.cursor()
            cursor.execute("SELECT * FROM items")
            rows = cursor.fetchall()
            if rows:
                output_path = REPORTS_DIR / "items.csv"
                with open(output_path, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                    writer.writeheader()
                    for row in rows:
                        writer.writerow(dict(row))
                print(f"✅ Exported {len(rows)} items to {output_path}")
        
        else:
            parser.print_help()
    
    finally:
        engine.close()


if __name__ == "__main__":
    main()
