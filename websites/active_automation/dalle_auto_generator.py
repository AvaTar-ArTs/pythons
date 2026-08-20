#!/usr/bin/env python3
"""DALL-E Auto Generator - Create images on autopilot"""
import os, sys, json, requests
from pathlib import Path
from datetime import datetime

# Load API keys
sys.path.insert(0, str(Path.home() / '.env.d'))
try:
    from loader import load_env
    load_env()
except:
    import subprocess
    result = subprocess.run(['bash', '-c', 'source ~/.env.d/loader.sh && env'],
                          capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if '=' in line:
            key, val = line.split('=', 1)
            os.environ[key] = val

OUTPUT_DIR = Path(__file__).parent / 'output' / 'images'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_dalle_image(prompt, size="1024x1024", quality="standard", n=1):
    """Generate image using DALL-E 3"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        print(f"🎨 Generating image: {prompt[:60]}...")

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            n=n
        )

        image_url = response.data[0].url
        revised_prompt = response.data[0].revised_prompt

        # Download image
        img_data = requests.get(image_url).content

        return {
            'url': image_url,
            'revised_prompt': revised_prompt,
            'data': img_data
        }
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def generate_themed_series(theme, count=5, style="vibrant digital art"):
    """Generate a series of themed images"""

    prompts = [
        f"{theme} - {style}, concept 1",
        f"{theme} - {style}, concept 2",
        f"{theme} - {style}, concept 3",
        f"{theme} - {style}, concept 4",
        f"{theme} - {style}, concept 5"
    ][:count]

    results = []

    for i, prompt in enumerate(prompts, 1):
        print(f"\n[{i}/{count}] Generating...")

        result = generate_dalle_image(prompt)
        if result:
            # Save image
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{theme.replace(' ', '_')}_{i}_{timestamp}.png"
            filepath = OUTPUT_DIR / filename
            filepath.write_bytes(result['data'])

            results.append({
                'number': i,
                'prompt': prompt,
                'revised_prompt': result['revised_prompt'],
                'filepath': str(filepath),
                'url': result['url']
            })

            print(f"✅ Saved: {filename}")
        else:
            print(f"❌ Failed to generate image {i}")

    return results

def generate_daily_art(theme=None):
    """Generate daily AI art for content"""
    if theme is None:
        # Auto-generate theme
        themes = [
            "cosmic dreams and nebulas",
            "cyberpunk city at night",
            "fantasy forest with magical creatures",
            "abstract geometric patterns",
            "surreal landscape",
            "futuristic technology",
            "nature and technology fusion",
            "ethereal portrait",
            "minimalist modern design",
            "vibrant street art"
        ]
        import random
        theme = random.choice(themes)

    prompt = f"{theme}, stunning composition, professional digital art, 4K quality, trending on artstation"

    result = generate_dalle_image(prompt, size="1024x1024", quality="hd")

    if result:
        # Save
        date_str = datetime.now().strftime('%Y%m%d')
        filename = f"daily_art_{date_str}.png"
        filepath = OUTPUT_DIR / filename
        filepath.write_bytes(result['data'])

        # Create markdown
        md_content = f"""# Daily AI Art - {datetime.now().strftime('%B %d, %Y')}

## Theme: {theme}

![{theme}]({filename})

**Original Prompt:**
{prompt}

**Revised Prompt (DALL-E 3):**
{result['revised_prompt']}

---

*Generated automatically for AvaTarArTs*
*Available for prints and products*
"""

        md_file = OUTPUT_DIR / f"daily_art_{date_str}.md"
        md_file.write_text(md_content)

        print(f"\n✅ Daily art generated!")
        print(f"🖼️  Image: {filepath}")
        print(f"📄 Details: {md_file}")

        return {
            'theme': theme,
            'image': str(filepath),
            'markdown': str(md_file),
            'revised_prompt': result['revised_prompt']
        }

    return None

def generate_product_mockups(design_theme, products=None):
    """Generate product mockup images"""
    if products is None:
        products = ['t-shirt', 'poster', 'mug', 'phone case', 'tote bag']

    results = []

    for product in products:
        prompt = f"Professional product mockup: {design_theme} design on a {product}, clean white background, studio lighting, commercial photography"

        result = generate_dalle_image(prompt)
        if result:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"mockup_{product.replace(' ', '_')}_{timestamp}.png"
            filepath = OUTPUT_DIR / filename
            filepath.write_bytes(result['data'])

            results.append({
                'product': product,
                'filepath': str(filepath)
            })

            print(f"✅ {product} mockup created")

    return results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("""DALL-E Auto Generator

Usage: dalle_auto_generator.py <command> [args]

Commands:
  daily                    - Generate daily AI art (auto theme)
  daily <theme>            - Generate daily AI art with specific theme
  series <theme> <count>   - Generate series of themed images
  mockup <theme>           - Generate product mockups
  custom <prompt>          - Generate from custom prompt

Examples:
  dalle_auto_generator.py daily
  dalle_auto_generator.py daily "cyberpunk raccoon"
  dalle_auto_generator.py series "fantasy landscapes" 5
  dalle_auto_generator.py mockup "geometric patterns"
  dalle_auto_generator.py custom "vibrant abstract art with neon colors"
""")
        sys.exit(1)

    command = sys.argv[1]

    if command == "daily":
        theme = sys.argv[2] if len(sys.argv) > 2 else None
        generate_daily_art(theme)

    elif command == "series":
        if len(sys.argv) < 3:
            print("Usage: dalle_auto_generator.py series <theme> [count]")
            sys.exit(1)
        theme = sys.argv[2]
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 5

        results = generate_themed_series(theme, count)

        # Save manifest
        manifest_file = OUTPUT_DIR / f"series_{theme.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json"
        manifest_file.write_text(json.dumps(results, indent=2))

        print(f"\n✅ Generated {len(results)} images")
        print(f"📄 Manifest: {manifest_file}")

    elif command == "mockup":
        if len(sys.argv) < 3:
            print("Usage: dalle_auto_generator.py mockup <design_theme>")
            sys.exit(1)
        theme = sys.argv[2]

        results = generate_product_mockups(theme)
        print(f"\n✅ Generated {len(results)} mockups")

    elif command == "custom":
        if len(sys.argv) < 3:
            print("Usage: dalle_auto_generator.py custom <prompt>")
            sys.exit(1)
        prompt = ' '.join(sys.argv[2:])

        result = generate_dalle_image(prompt, quality="hd")
        if result:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"custom_{timestamp}.png"
            filepath = OUTPUT_DIR / filename
            filepath.write_bytes(result['data'])

            print(f"\n✅ Image generated!")
            print(f"🖼️  Saved to: {filepath}")

    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)
