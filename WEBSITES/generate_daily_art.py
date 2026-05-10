import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Summary of generate_daily_art.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import os
import random
from pathlib import Path

PICTURES_DIR = Path.home() / "Pictures"
OUTPUT_DIR = Path(__file__).parent

CATEGORIES = ["raccoon", "krampus", "dark", "goth", "neon", "typography", "eso"]


def find_images():
    imgs = []
    exts = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    for root, dirs, files in os.walk(PICTURES_DIR):
        for f in files:
            if Path(f).suffix.lower() in exts:
                p = Path(root) / f
                imgs.append(p)
    return imgs


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    images = find_images()
    random.shuffle(images)
    pick = images[:9]
    cats = ", ".join(random.sample(CATEGORIES, k=3))

    md = [
        f"# Daily Art Drop — {cats}",
        "",
        "A curated 3x3 drop from the AvaTarArTs vault.",
        "",
    ]
    for p in pick:
        md.append(f"![]({p})")
    md.append(
        "\nLinks: [/disco.html](/disco.html) · [/dalle.html](/dalle.html) · [/python.html](/python.html)"
    )

    outfile = OUTPUT_DIR / "daily-art.md"
    outfile.write_text("\n".join(md))
    print(f"✅ Generated: {outfile}")


try:
        main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)