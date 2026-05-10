#!/usr/bin/env python3
"""
Image Selector for Print-on-Demand
Analyzes Pictures directory and selects best designs for Redbubble/Etsy

Usage: python3 image-selector.py
"""

import os
import json
from pathlib import Path
from collections import defaultdict
import shutil

# Configuration
PICTURES_DIR = Path.home() / "Pictures"
OUTPUT_DIR = Path(__file__).parent / "selected-designs"
CATEGORIES = {
    "raccoon": ["raccoon", "trash", "punk", "alley", "urban"],
    "holiday": ["krampus", "christmas", "halloween", "holiday", "beetlejuice"],
    "typography": ["avatararts", "typography", "neon", "HTML Juice"],
    "gaming": ["eso", "guild", "orc", "fantasy"],
    "political": ["project 2025", "liberty", "statue"],
    "dark_art": ["dark", "gothic", "skull", "demon"],
}

def analyze_directory():
    """Analyze Pictures directory and categorize images"""
    print("🔍 Analyzing Pictures directory...")
    print(f"📁 Location: {PICTURES_DIR}")

    categorized = defaultdict(list)
    total_files = 0

    # Supported image formats
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}

    for root, dirs, files in os.walk(PICTURES_DIR):
        for file in files:
            file_lower = file.lower()
            ext = Path(file).suffix.lower()

            if ext in image_extensions:
                total_files += 1
                file_path = Path(root) / file

                # Categorize based on filename
                for category, keywords in CATEGORIES.items():
                    if any(keyword.lower() in file_lower for keyword in keywords):
                        categorized[category].append({
                            'path': str(file_path),
                            'name': file,
                            'size': file_path.stat().st_size if file_path.exists() else 0
                        })
                        break
                else:
                    categorized['other'].append({
                        'path': str(file_path),
                        'name': file,
                        'size': file_path.stat().st_size if file_path.exists() else 0
                    })

    print(f"\n📊 Analysis Complete!")
    print(f"Total images: {total_files:,}")
    print("\n📂 Categorization:")
    for category, files in sorted(categorized.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {category}: {len(files)} images")

    return categorized

def select_top_designs(categorized, top_n=10):
    """Select top N designs from each category"""
    print(f"\n🎨 Selecting top {top_n} designs per category...")

    selected = {}
    for category, files in categorized.items():
        if category == 'other':
            continue

        # Sort by file size (larger = higher quality)
        sorted_files = sorted(files, key=lambda x: x['size'], reverse=True)
        selected[category] = sorted_files[:top_n]

        print(f"  ✅ {category}: Selected {len(selected[category])} designs")

    return selected

def copy_selected_designs(selected):
    """Copy selected designs to output directory"""
    print(f"\n📦 Copying selected designs to: {OUTPUT_DIR}")

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total_copied = 0
    for category, files in selected.items():
        category_dir = OUTPUT_DIR / category
        category_dir.mkdir(exist_ok=True)

        for file_info in files:
            src = Path(file_info['path'])
            if src.exists():
                dst = category_dir / src.name
                try:
                    shutil.copy2(src, dst)
                    total_copied += 1
                except Exception as e:
                    print(f"  ⚠️  Error copying {src.name}: {e}")

    print(f"  ✅ Copied {total_copied} files")
    return total_copied

def generate_report(categorized, selected):
    """Generate JSON report of analysis"""
    report_path = OUTPUT_DIR / "analysis-report.json"

    report = {
        "total_images": sum(len(files) for files in categorized.values()),
        "categories": {cat: len(files) for cat, files in categorized.items()},
        "selected": {cat: len(files) for cat, files in selected.items()},
        "recommendations": []
    }

    # Add recommendations
    if len(categorized.get('raccoon', [])) > 20:
        report['recommendations'].append(
            "🦝 Raccoon theme is strong! Consider 'RaccoonPunkArt' as Redbubble username"
        )
    if len(categorized.get('holiday', [])) > 15:
        report['recommendations'].append(
            "🎃 Holiday content ready for seasonal launches (Krampus for Christmas!)"
        )
    if len(categorized.get('typography', [])) > 10:
        report['recommendations'].append(
            "✨ Typography designs perfect for minimalist products"
        )

    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n📄 Report saved: {report_path}")
    return report

def print_next_steps(report):
    """Print actionable next steps"""
    print("\n" + "="*50)
    print("🚀 NEXT STEPS")
    print("="*50)

    print("\n1️⃣  Review selected designs:")
    print(f"   open {OUTPUT_DIR}")

    print("\n2️⃣  Redbubble Username Suggestions:")
    if report['categories'].get('raccoon', 0) > 20:
        print("   • RaccoonPunkArt (matches your signature theme)")
        print("   • TrashPandaDesigns")
        print("   • UrbanRaccoonCo")
    print("   • KrampusVibes (for holiday niche)")
    print("   • DarkFantasyArt (broad appeal)")

    print("\n3️⃣  Redbubble Setup:")
    print("   1. Go to https://www.redbubble.com/signup")
    print("   2. Choose username from suggestions above")
    print("   3. Upload first 10 raccoon designs")
    print("   4. Use SEO keywords in titles/tags")

    print("\n4️⃣  Etsy Setup:")
    print("   1. Go to https://www.etsy.com/sell")
    print("   2. Create shop: 'AvatarArts Prints' or similar")
    print("   3. Upload as DIGITAL DOWNLOADS (instant delivery)")
    print("   4. Price: $3-10 per design")

    print("\n5️⃣  SEO Keywords (from your research):")
    top_keywords = [
        "raccoon punk art",
        "krampus christmas",
        "dark fantasy gothic",
        "urban alley art",
        "typography neon",
    ]
    for keyword in top_keywords:
        print(f"   • {keyword}")

    print("\n6️⃣  Pricing Strategy:")
    print("   Redbubble: Let them handle pricing (you get 20-25%)")
    print("   Etsy: $5-15 for digital, $15-50 for physical prints")

    print("\n7️⃣  Read the complete guide:")
    print("   open ~/ai-sites/passive-income-empire/print-on-demand/redbubble-setup.md")

    print("\n" + "="*50)

def main():
    print("🎨 PRINT-ON-DEMAND IMAGE SELECTOR")
    print("=" * 50)

    # Step 1: Analyze
    categorized = analyze_directory()

    # Step 2: Select top designs
    selected = select_top_designs(categorized, top_n=10)

    # Step 3: Copy files
    total_copied = copy_selected_designs(selected)

    # Step 4: Generate report
    report = generate_report(categorized, selected)

    # Step 5: Show recommendations
    print("\n💡 RECOMMENDATIONS:")
    for rec in report['recommendations']:
        print(f"  {rec}")

    # Step 6: Next steps
    print_next_steps(report)

    print("\n✅ Analysis complete! Ready to launch print-on-demand business.")

if __name__ == "__main__":
    main()
