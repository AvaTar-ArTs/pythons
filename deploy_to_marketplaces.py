#!/usr/bin/env python3
"""
Marketplace Deployment Automation Script
Prepares and deploys Python script bundles to multiple marketplaces

Supported marketplaces:
- CodeCanyon
- Gumroad
- Payhip
- Sellfy

Usage:
    python deploy_to_marketplaces.py --bundle all --dry-run
    python deploy_to_marketplaces.py --bundle code-quality --deploy gumroad
    python deploy_to_marketplaces.py --list-bundles
"""

import sys
import shutil
import zipfile
import argparse
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add parent directory to path for avatar_utils
sys.path.insert(0, str(Path(__file__).parent))
try:
    from avatar_utils import load_env_d, print_header
except ImportError:

    def load_env_d():
        pass

    def print_header(text):
        print(f"\n{'=' * 80}\n{text.center(80)}\n{'=' * 80}\n")


load_env_d()

# Configuration
PRODUCTS_DIR = Path(__file__).parent / "products"
DEPLOY_DIR = Path(__file__).parent / "deploy"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# Marketplace configurations
MARKETPLACES = {
    "gumroad": {
        "name": "Gumroad",
        "url": "https://gumroad.com",
        "fee_percentage": 10,
        "supports_bundles": True,
        "max_file_size_mb": 5000,
    },
    "codecanyon": {
        "name": "CodeCanyon",
        "url": "https://codecanyon.net",
        "fee_percentage": 30,
        "supports_bundles": False,
        "max_file_size_mb": 512,
    },
    "payhip": {
        "name": "Payhip",
        "url": "https://payhip.com",
        "fee_percentage": 5,
        "supports_bundles": True,
        "max_file_size_mb": 2000,
    },
    "sellfy": {
        "name": "Sellfy",
        "url": "https://sellfy.com",
        "fee_percentage": 0,
        "supports_bundles": True,
        "max_file_size_mb": 10000,
    },
}

# Bundle configurations
BUNDLES = {
    "code-quality": {
        "name": "Python Code Quality Toolkit",
        "price": 97,
        "description": "Professional Python code analysis, deduplication, and optimization tools",
        "category": "Development Tools",
        "tags": ["python", "code-quality", "analyzer", "deduplication", "automation"],
        "source_files": [
            "advanced_code_analyzer.py",
            "advanced_file_deduplicator.py",
            "avatar_utils.py",
        ],
        "marketplaces": ["gumroad", "codecanyon", "payhip"],
    },
    "social-media": {
        "name": "Social Media Automation Suite",
        "price": 147,
        "description": "Automate Instagram, YouTube, Twitter, and other social platforms",
        "category": "Marketing Tools",
        "tags": [
            "social-media",
            "automation",
            "instagram",
            "youtube",
            "twitter",
            "marketing",
        ],
        "source_pattern": "media_processing/",
        "marketplaces": ["gumroad", "payhip", "sellfy"],
    },
    "ai-toolkit": {
        "name": "AI Integration Toolkit",
        "price": 197,
        "description": "Integrate OpenAI, Leonardo AI, AssemblyAI, and more with Python",
        "category": "AI & Machine Learning",
        "tags": ["ai", "openai", "machine-learning", "automation", "api"],
        "source_pattern": "apis/",
        "marketplaces": ["gumroad", "payhip", "sellfy"],
    },
}


def list_bundles():
    """List all available bundles with details."""
    print_header("Available Product Bundles")

    for bundle_id, bundle in BUNDLES.items():
        print(f"\n📦 {bundle['name']}")
        print(f"   ID: {bundle_id}")
        print(f"   Price: ${bundle['price']}")
        print(f"   Category: {bundle['category']}")
        print(f"   Marketplaces: {', '.join(bundle['marketplaces'])}")
        print(f"   Tags: {', '.join(bundle['tags'][:5])}")

    print(f"\n{'=' * 80}\n")


def create_bundle_zip(bundle_id: str, dry_run: bool = False) -> Optional[Path]:
    """Create a ZIP file for a bundle."""
    bundle = BUNDLES.get(bundle_id)
    if not bundle:
        print(f"❌ Bundle not found: {bundle_id}")
        return None

    print_header(f"Creating Bundle: {bundle['name']}")

    # Create deploy directory
    bundle_dir = DEPLOY_DIR / f"{bundle_id}_{TIMESTAMP}"
    bundle_dir.mkdir(parents=True, exist_ok=True)

    # Copy product bundle if exists
    product_bundle = (
        PRODUCTS_DIR / f"bundle-1-{bundle_id}"
        if bundle_id == "code-quality"
        else (
            PRODUCTS_DIR / f"bundle-2-{bundle_id}"
            if bundle_id == "social-media"
            else PRODUCTS_DIR / f"bundle-3-{bundle_id}"
        )
    )

    if product_bundle.exists():
        print(f"✅ Found product bundle: {product_bundle}")
        shutil.copytree(product_bundle, bundle_dir / "product", dirs_exist_ok=True)
    else:
        print("⚠️  Product bundle not found, creating from source files...")
        (bundle_dir / "product").mkdir(exist_ok=True)

    # Copy source files
    print("\n📁 Collecting source files...")
    files_copied = 0

    if "source_files" in bundle:
        for file_name in bundle["source_files"]:
            source = Path(__file__).parent / file_name
            if source.exists():
                dest = bundle_dir / "product" / file_name
                if not dry_run:
                    shutil.copy2(source, dest)
                files_copied += 1
                print(f"   ✅ {file_name}")

    if "source_pattern" in bundle:
        pattern_dir = Path(__file__).parent / bundle["source_pattern"]
        if pattern_dir.exists():
            py_files = list(pattern_dir.glob("*.py"))[:20]  # Limit to 20 files
            for source in py_files:
                dest = bundle_dir / "product" / source.name
                if not dry_run:
                    shutil.copy2(source, dest)
                files_copied += 1
                if files_copied <= 10:  # Only print first 10
                    print(f"   ✅ {source.name}")

    if files_copied > 10:
        print(f"   ... and {files_copied - 10} more files")

    # Create README if not exists
    readme_path = bundle_dir / "product" / "README.md"
    if not readme_path.exists() and not dry_run:
        readme_path.write_text(
            f"""# {bundle['name']}

{bundle['description']}

## Price
${bundle['price']}

## Category
{bundle['category']}

## Installation
1. Extract the ZIP file
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables: `cp .env.example .env`
4. Run scripts: `python <script_name>.py`

## Support
Contact: support@yourdomain.com

## License
Commercial License - See LICENSE file
"""
        )

    # Create LICENSE file
    license_path = bundle_dir / "product" / "LICENSE"
    if not license_path.exists() and not dry_run:
        license_path.write_text(
            f"""COMMERCIAL LICENSE

Copyright (c) {datetime.now().year} AVATARARTS

This product is licensed for commercial use on digital marketplaces.
 redistribution without purchase is strictly prohibited.
"""
        )

    # Create ZIP archive
    zip_path = DEPLOY_DIR / f"{bundle_id}_{TIMESTAMP}.zip"
    if not dry_run:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in bundle_dir.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(bundle_dir)
                    zipf.write(file_path, arcname)
        print(f"\n📦 Created ZIP: {zip_path}")
        print(f"   Size: {zip_path.stat().st_size / 1024 / 1024:.2f} MB")

    # Calculate file hash for verification
    if zip_path.exists():
        md5 = hashlib.md5(zip_path.read_bytes()).hexdigest()
        print(f"   MD5: {md5}")

    return zip_path


def generate_marketplace_listing(bundle_id: str, marketplace: str):
    """Generate marketplace-specific listing."""
    bundle = BUNDLES.get(bundle_id)
    mp = MARKETPLACES.get(marketplace)

    if not bundle or not mp:
        print("❌ Invalid bundle or marketplace")
        return

    print_header(f"{mp['name']} Listing: {bundle['name']}")

    # Calculate final price after fees
    fee_amount = bundle["price"] * (mp["fee_percentage"] / 100)
    you_earn = bundle["price"] - fee_amount

    print(f"\n📝 Product Title: {bundle['name']}")
    print(f"💰 Price: ${bundle['price']}")
    print(f"📊 Category: {bundle['category']}")
    print(f"🏷️  Tags: {', '.join(bundle['tags'])}")
    print(f"\n💵 Marketplace Fee: {mp['fee_percentage']}% (${fee_amount:.2f})")
    print(f"✅ You Earn: ${you_earn:.2f} per sale")

    print("\n📄 Short Description:")
    print(f"   {bundle['description'][:150]}...")

    print("\n📋 Long Description:")
    print(
        f"""
{bundle['name']}

{bundle['description']}

✨ Features:
- Professional Python automation scripts
- Well-documented and tested
- Easy to customize and extend
- Production-ready code
- Comprehensive examples included

📦 What's Included:
- Multiple Python scripts for {bundle['category'].lower()}
- Detailed documentation
- Requirements file for easy setup
- Environment variable templates
- Usage examples

🚀 Perfect For:
- Developers looking to automate workflows
- Teams wanting to improve code quality
- Anyone working with {bundle['category'].lower()}

💡 Requirements:
- Python 3.8+
- Basic Python knowledge
- API keys for external services (documented)

📞 Support:
- Email: support@yourdomain.com
- Response time: 24-48 hours
"""
    )

    print(f"\n{'=' * 80}\n")


def deploy_all(dry_run: bool = False):
    """Deploy all bundles to all configured marketplaces."""
    print_header("Marketplace Deployment Automation")

    if dry_run:
        print("🔍 DRY RUN MODE - No files will be uploaded\n")

    for bundle_id, bundle in BUNDLES.items():
        print(f"\n{'─' * 80}")
        print(f"📦 Processing: {bundle['name']}")
        print(f"{'─' * 80}")

        # Create bundle ZIP
        create_bundle_zip(bundle_id, dry_run=dry_run)

        # Generate listings for each marketplace
        for marketplace in bundle["marketplaces"]:
            generate_marketplace_listing(bundle_id, marketplace)

    print_header("Deployment Summary")
    print("\n✅ All bundles processed!")
    print(f"📁 Deploy files located in: {DEPLOY_DIR}")
    print("\n🚀 Next Steps:")
    print("   1. Review generated listings")
    print("   2. Add screenshots to product pages")
    print("   3. Upload ZIP files to marketplaces")
    print("   4. Set up payment information")
    print("   5. Publish products!")
    print("\n💡 Tip: Start with Gumroad for fastest deployment")
    print(f"\n{'=' * 80}\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Deploy Python script bundles to multiple marketplaces",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list-bundles                    # List all available bundles
  %(prog)s --bundle code-quality --dry-run   # Test bundle creation
  %(prog)s --bundle all --deploy gumroad     # Deploy all to Gumroad
  %(prog)s --bundle ai-toolkit --dry-run     # Test AI toolkit bundle
        """,
    )

    parser.add_argument(
        "--bundle",
        "-b",
        choices=list(BUNDLES.keys()) + ["all"],
        help="Bundle to process",
    )
    parser.add_argument(
        "--marketplace",
        "-m",
        choices=list(MARKETPLACES.keys()),
        help="Target marketplace",
    )
    parser.add_argument(
        "--deploy",
        action="store_true",
        help="Deploy to marketplace (requires API credentials)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Test mode - don't actually upload"
    )
    parser.add_argument(
        "--list-bundles", action="store_true", help="List all available bundles"
    )

    args = parser.parse_args()

    if args.list_bundles:
        list_bundles()
        return

    if args.bundle:
        if args.bundle == "all":
            deploy_all(dry_run=args.dry_run)
        else:
            if args.dry_run:
                create_bundle_zip(args.bundle, dry_run=True)
            elif args.deploy and args.marketplace:
                generate_marketplace_listing(args.bundle, args.marketplace)
            else:
                create_bundle_zip(args.bundle, dry_run=False)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
