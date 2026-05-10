import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
Summary of catalog_art.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import os
import csv
from pathlib import Path

# Configuration
SOURCE_DIR = Path("/Users/steven/Pictures")
OUTPUT_CSV = Path("/Users/steven/SELLABLE_ART_CATALOG.csv")

# Asset Category Mapping
CATEGORIES = {
    "Adobe": "SYSTEMS (Mockups/Workflows)",
    "etsy/SVG_Files": "VECTORS (Commercial SVG)",
    "etsy/Designs": "DESIGNS (Commercial Art)",
    "Kreature-Zombot-Brand": "IP (Brand Assets)",
    "buBBleSpider": "IP (Brand Assets)",
    "DaLLe": "AI_RAW (DALL-E)",
    "ideoGram": "AI_RAW (Ideogram)",
    "leonardo": "AI_RAW (Leonardo)",
}

def get_category(path):
    rel_path = path.relative_to(SOURCE_DIR)
    for key, cat in CATEGORIES.items():
        if str(rel_path).startswith(key):
            return cat
    return "GENERAL_ART"

def catalog_assets():
    print(f"🚀 Scanning {SOURCE_DIR} for sellable assets...")
    assets = []
    
    # Extensions that represent sellable source/output
    TARGET_EXTS = {'.psd', '.ai', '.svg', '.png', '.jpg', '.jpeg'}
    
    for root, dirs, files in os.walk(SOURCE_DIR):
        root_path = Path(root)
        
        # Skip hidden and system folders
        if any(part.startswith('.') for part in root_path.parts):
            continue
            
        category = get_category(root_path)
        
        for f in files:
            if f.startswith('.'): continue
            
            file_path = root_path / f
            ext = file_path.suffix.lower()
            
            if ext in TARGET_EXTS:
                size_mb = file_path.stat().st_size / (1024 * 1024)
                
                # Heuristic for "High Quality"
                # PSD/AI are always valuable. 
                # SVGs are always valuable for Etsy.
                # PNG/JPG must be > 1MB to be considered "Print Ready"
                is_valuable = False
                if ext in {'.psd', '.ai', '.svg'}:
                    is_valuable = True
                elif size_mb > 1.0:
                    is_valuable = True
                
                if is_valuable:
                    assets.append({
                        "Category": category,
                        "Format": ext[1:].upper(),
                        "Name": f,
                        "Size_MB": f"{size_mb:.2f}",
                        "Path": str(file_path),
                        "Folder": root_path.name
                    })

    # Sort by Category and then Size
    assets.sort(key=lambda x: (x['Category'], -float(x['Size_MB'])))

    # Write to CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Category", "Format", "Name", "Size_MB", "Folder", "Path"])
        writer.writeheader()
        writer.writerows(assets)

    print(f"✅ Catalog complete! {len(assets)} items identified.")
    print(f"📊 Saved to: {OUTPUT_CSV}")

try:
        catalog_assets()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)