#!/usr/bin/env python3
import os, random
from pathlib import Path

PICTURES_DIR = Path.home() / 'Pictures'
OUTPUT_DIR = Path(__file__).parent

CATEGORIES = ['raccoon','krampus','dark','goth','neon','typography','eso']

def find_images():
    imgs = []
    exts = {'.jpg','.jpeg','.png','.webp','.gif'}
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
    cats = ', '.join(random.sample(CATEGORIES, k=3))

    md = [
        f"# Daily Art Drop — {cats}",
        "",
        "A curated 3x3 drop from the AvaTarArTs vault.",
        "",
    ]
    for p in pick:
        md.append(f"![]({p})")
    md.append("\nLinks: [/disco.html](/disco.html) · [/dalle.html](/dalle.html) · [/python.html](/python.html)")

    outfile = OUTPUT_DIR / 'daily-art.md'
    outfile.write_text('\n'.join(md))
    print(f"✅ Generated: {outfile}")

if __name__ == '__main__':
    main()
