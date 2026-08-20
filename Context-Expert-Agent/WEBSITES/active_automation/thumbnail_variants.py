#!/usr/bin/env python3
"""Thumbnail A/B Variant Generator - 5 optimized versions"""
import sys, json
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent / 'output' / 'thumbnails'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# CTR-optimized thumbnail strategies
VARIANTS = {
    'high_contrast': {
        'description': 'Boosted contrast, vibrant colors',
        'adjustments': 'brightness +20%, saturation +30%, contrast +40%'
    },
    'text_overlay': {
        'description': 'Bold text overlay with drop shadow',
        'adjustments': 'Add title text, 72pt bold, yellow/white, shadow'
    },
    'close_crop': {
        'description': 'Tight crop on focal point',
        'adjustments': 'Crop to 120% center, scale up'
    },
    'emotion_face': {
        'description': 'Emphasize emotional element',
        'adjustments': 'Circle/arrow to face or key object, boost that area'
    },
    'border_frame': {
        'description': 'Colorful border/frame',
        'adjustments': 'Add 10px bright border, subtle vignette'
    }
}

def generate_variant_specs(image_path):
    """Generate specifications for 5 thumbnail variants"""
    variants = []

    for variant_name, config in VARIANTS.items():
        variants.append({
            'original': str(image_path),
            'variant': variant_name,
            'description': config['description'],
            'adjustments': config['adjustments'],
            'output': str(OUTPUT_DIR / f"{image_path.stem}_{variant_name}{image_path.suffix}")
        })

    return variants

def create_variant_script(image_path, output_path=None):
    """Create ImageMagick script to generate variants"""
    if output_path is None:
        output_path = OUTPUT_DIR / f'generate_{image_path.stem}.sh'

    specs = generate_variant_specs(image_path)

    script = [
        "#!/bin/bash",
        "# Thumbnail variant generator",
        f"# Source: {image_path}",
        "set -euo pipefail",
        ""
    ]

    for spec in specs:
        variant = spec['variant']
        output = spec['output']

        if variant == 'high_contrast':
            script.append(f"# High contrast variant")
            script.append(f"convert '{image_path}' -brightness-contrast 20x40 -modulate 100,130,100 '{output}'")

        elif variant == 'text_overlay':
            script.append(f"# Text overlay variant")
            script.append(f"convert '{image_path}' -pointsize 72 -fill white -stroke black -strokewidth 3 -gravity north -annotate +0+50 'CLICK ME' '{output}'")

        elif variant == 'close_crop':
            script.append(f"# Close crop variant")
            script.append(f"convert '{image_path}' -gravity center -crop 80%x80%+0+0 +repage -resize 1280x720! '{output}'")

        elif variant == 'emotion_face':
            script.append(f"# Emotion emphasis (manual edit recommended)")
            script.append(f"convert '{image_path}' -fill none -stroke yellow -strokewidth 8 -draw 'circle 640,360 640,450' '{output}'")

        elif variant == 'border_frame':
            script.append(f"# Border frame variant")
            script.append(f"convert '{image_path}' -bordercolor '#FF6B6B' -border 15 -vignette 0x2 '{output}'")

        script.append("")

    script.append("echo '✅ Generated 5 thumbnail variants'")
    script.append(f"ls -lh {OUTPUT_DIR}")

    output_path.write_text('\n'.join(script))
    output_path.chmod(0o755)

    return output_path

def create_json_spec(image_path, output_path=None):
    """Create JSON spec for programmatic variant generation"""
    if output_path is None:
        output_path = OUTPUT_DIR / f'{image_path.stem}_variants.json'

    specs = generate_variant_specs(image_path)

    data = {
        'original': str(image_path),
        'generated': datetime.now().isoformat(),
        'variants': specs,
        'ctr_tips': [
            'Test all 5 variants with A/B testing',
            'High contrast performs best for mobile',
            'Text overlay increases CTR by 20-30%',
            'Emotion/face emphasis drives engagement',
            'Borders make thumbnails stand out in grid'
        ]
    }

    output_path.write_text(json.dumps(data, indent=2))
    return output_path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: thumbnail_variants.py <image_path>")
        print("\nGenerates 5 CTR-optimized thumbnail variants")
        sys.exit(1)

    image_path = Path(sys.argv[1])

    if not image_path.exists():
        print(f"❌ Image not found: {image_path}")
        sys.exit(1)

    print(f"🎨 Generating 5 thumbnail variants for: {image_path.name}")

    # Create ImageMagick script
    script_path = create_variant_script(image_path)
    print(f"📄 Script created: {script_path}")

    # Create JSON spec
    json_path = create_json_spec(image_path)
    print(f"📋 JSON spec: {json_path}")

    print(f"\n💡 Run: {script_path}")
    print(f"   (Requires ImageMagick: brew install imagemagick)")
