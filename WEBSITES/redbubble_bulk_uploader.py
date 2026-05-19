import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""Redbubble Bulk Uploader - 50+ designs with SEO"""

import csv
import sys
from pathlib import Path
from datetime import datetime

PICS_DIR = Path.home() / "Pictures"
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Redbubble product types
PRODUCTS = [
    "classic-tee",
    "fitted-tee",
    "tri-blend-tee",
    "baseball-tee",
    "hoodie",
    "zip-hoodie",
    "crewneck-sweatshirt",
    "sticker",
    "magnet",
    "poster",
    "art-print",
    "canvas-print",
    "phone-case",
    "laptop-sleeve",
    "tote-bag",
    "drawstring-bag",
    "mug",
    "travel-mug",
    "water-bottle",
    "pillow",
    "duvet-cover",
    "comforter",
    "greeting-card",
    "postcard",
    "notebook",
    "spiral-notebook",
]


def find_best_images(limit=50, theme_keywords=None):
    """Find top images for print-on-demand"""
    if theme_keywords is None:
        theme_keywords = ["raccoon", "fantasy", "holiday", "gothic", "cyberpunk"]

    candidates = []

    # Search Pictures directory
    for img_path in PICS_DIR.rglob("*"):
        if img_path.suffix.lower() in [".png", ".jpg", ".jpeg"]:
            # Check size (min 2000px for Redbubble)
            if img_path.stat().st_size < 100000:  # Skip tiny files
                continue

            # Score by theme
            name_lower = img_path.stem.lower()
            score = sum(1 for kw in theme_keywords if kw in name_lower)

            if score > 0:
                candidates.append(
                    {
                        "path": str(img_path),
                        "name": img_path.stem,
                        "score": score,
                        "size_mb": img_path.stat().st_size / 1024 / 1024,
                    }
                )

    # Sort by score, take top N
    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates[:limit]


def generate_seo_metadata(image_name):
    """Generate SEO-optimized metadata"""
    # Extract keywords from filename
    words = image_name.replace("_", " ").replace("-", " ").split()
    keywords = [w for w in words if len(w) > 3][:10]

    title = " ".join(words[:8]).title()
    description = f"Unique {title} design. Perfect for gifts, home decor, and personal style. High-quality print on demand."
    tags = keywords + ["art", "design", "gift", "unique", "style"]

    return {
        "title": title[:60],  # Redbubble limit
        "description": description[:256],
        "tags": ",".join(tags[:20]),
    }


def create_upload_csv(images, output_path=None):
    """Create CSV for bulk upload"""
    if output_path is None:
        output_path = (
            OUTPUT_DIR
            / f"redbubble_upload_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        )

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "image_path",
                "title",
                "description",
                "tags",
                "products",
                "default_price_tier",
                "collection",
            ]
        )

        for img in images:
            meta = generate_seo_metadata(img["name"])
            writer.writerow(
                [
                    img["path"],
                    meta["title"],
                    meta["description"],
                    meta["tags"],
                    ";".join(PRODUCTS[:10]),  # Enable top 10 products
                    "artist_+25%",  # Markup tier
                    "AvaTarArTs Collection",
                ]
            )

    return output_path


def create_manual_checklist(images, output_path=None):
    """Create human-readable checklist"""
    if output_path is None:
        output_path = (
            OUTPUT_DIR
            / f"redbubble_checklist_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        )

    content = [
        "# Redbubble Bulk Upload Checklist\n",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
        f"**Total Designs:** {len(images)}\n",
        "---\n",
    ]

    for i, img in enumerate(images, 1):
        meta = generate_seo_metadata(img["name"])
        content.append(f"## {i}. {meta['title']}\n")
        content.append(f"- **File:** `{img['path']}`\n")
        content.append(f"- **Size:** {img['size_mb']:.1f} MB\n")
        content.append(f"- **Description:** {meta['description']}\n")
        content.append(f"- **Tags:** {meta['tags']}\n")
        content.append("- [ ] Uploaded\n")
        content.append("- [ ] Verified\n\n")

    output_path.write_text("".join(content))
    return output_path


try:
        limit = int(sys.argv[1]) if len(sys.argv) > 1 else 50
        print(f"🔍 Finding top {limit} images for Redbubble...")
        images = find_best_images(limit)
        if not images:
            print("❌ No suitable images found")
            sys.exit(1)
        print(f"✅ Found {len(images)} images\n")
        # Create CSV
        csv_path = create_upload_csv(images)
        print(f"📄 CSV created: {csv_path}")
        # Create checklist
        checklist_path = create_manual_checklist(images)
        print(f"📋 Checklist created: {checklist_path}")
        # Summary
        print("\n📊 Summary:")
        print(f"   Total images: {len(images)}")
        print(f"   Potential products: {len(images) * len(PRODUCTS[:10])} listings")
        print(f"   Est. upload time: {len(images) * 3} minutes")
        print(f"\n💡 Next: Review {checklist_path} and upload via Redbubble dashboard")
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)