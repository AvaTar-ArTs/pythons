#!/usr/bin/env python3
"""Cross-Pollination Engine - Recipe → All Social Platforms"""
import sys, json
from pathlib import Path
from datetime import datetime

CONTENT_DIR = Path.home() / 'ai-sites' / 'content-management' / 'retention-hub'
OUTPUT_DIR = Path(__file__).parent / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)

def load_latest_recipe():
    """Load the most recent recipe"""
    recipe_dir = CONTENT_DIR / 'recipes' / 'output'
    if not recipe_dir.exists():
        return None

    recipes = sorted(recipe_dir.glob('*.md'), key=lambda p: p.stat().st_mtime, reverse=True)
    if not recipes:
        return None

    return recipes[0].read_text()

def extract_recipe_data(recipe_text):
    """Extract key data from recipe markdown"""
    lines = recipe_text.split('\n')
    title = next((l.strip('# ') for l in lines if l.startswith('# ')), 'AI Recipe')

    # Extract ingredients and steps
    in_ingredients = False
    in_instructions = False
    ingredients = []
    instructions = []

    for line in lines:
        if '## Ingredients' in line:
            in_ingredients = True
            in_instructions = False
        elif '## Instructions' in line:
            in_ingredients = False
            in_instructions = True
        elif line.startswith('## '):
            in_ingredients = False
            in_instructions = False
        elif in_ingredients and line.strip().startswith('-'):
            ingredients.append(line.strip('- '))
        elif in_instructions and line.strip().startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9')):
            instructions.append(line.strip())

    return {
        'title': title,
        'ingredients': ingredients,
        'instructions': instructions
    }

def generate_instagram_post(recipe_data):
    """Generate Instagram post (image + caption)"""
    caption = f"""🍳 {recipe_data['title']}

Try this delicious AI-generated recipe! Perfect for any occasion.

✨ Key ingredients:
{chr(10).join(f"• {ing}" for ing in recipe_data['ingredients'][:5])}

👉 Full recipe on AvaTarArTs.org

#recipe #cooking #foodie #airecipes #homemade #delicious #foodporn #instafood #yummy #tasty
"""

    # Image prompt for DALL-E
    image_prompt = f"Vibrant food photography of {recipe_data['title']}, professional food styling, appetizing presentation, natural lighting, shallow depth of field, 4K quality"

    return {
        'platform': 'instagram',
        'type': 'post',
        'caption': caption.strip(),
        'image_prompt': image_prompt,
        'hashtags': 10,
        'estimated_reach': '500-2000'
    }

def generate_tiktok_script(recipe_data):
    """Generate TikTok video script (30-60 sec)"""
    script = f"""🎬 TikTok Script: {recipe_data['title']}

[HOOK - 0:00-0:03]
Text overlay: "AI just created the PERFECT recipe 🤯"
Visual: Swipe through ingredient photos

[SETUP - 0:03-0:15]
Voiceover: "Here's what you'll need..."
Text overlay: Key ingredients (animated list)
Visual: Ingredient lineup, fast-paced

[PAYOFF - 0:15-0:30]
Voiceover: "And in just [X] minutes, you'll have..."
Text overlay: Final dish reveal
Visual: Completed dish, money shot

[CTA - 0:30-0:35]
Text overlay: "Full recipe link in bio!"
Visual: AvaTarArTs.org logo

MUSIC: Upbeat trending audio
HASHTAGS: #recipe #cooking #ai #fyp #foryou #food #easy
"""

    return {
        'platform': 'tiktok',
        'type': 'video_script',
        'script': script.strip(),
        'duration': '30-35 seconds',
        'estimated_views': '1000-5000'
    }

def generate_pinterest_pin(recipe_data):
    """Generate Pinterest pin (optimized for search)"""
    title = f"{recipe_data['title']} - Easy & Delicious!"
    description = f"""Discover this amazing AI-generated recipe for {recipe_data['title']}!

Perfect for:
• Quick weeknight dinners
• Meal prep
• Special occasions

Ingredients: {', '.join(recipe_data['ingredients'][:5])}...

Click for full recipe & more AI cooking inspiration! #recipe #cooking #AI #foodie #easy #delicious"""

    image_prompt = f"Vertical Pinterest pin design (2:3 ratio), {recipe_data['title']}, bold text overlay '{recipe_data['title']}', step-by-step photo collage, bright colors, professional food photography"

    return {
        'platform': 'pinterest',
        'type': 'pin',
        'title': title,
        'description': description.strip(),
        'image_prompt': image_prompt,
        'aspect_ratio': '2:3 (1000x1500px)',
        'estimated_saves': '50-200'
    }

def generate_youtube_short(recipe_data):
    """Generate YouTube Shorts script (60 sec)"""
    script = f"""📹 YouTube Short: {recipe_data['title']}

[0:00-0:05] HOOK
"I asked AI to create a recipe... and it's AMAZING!"
Visual: Dramatic reveal of finished dish

[0:05-0:20] INGREDIENTS
Fast-paced text overlays with ingredients
B-roll of each ingredient

[0:20-0:45] QUICK STEPS
{chr(10).join(f"Step {i+1}: {inst[:50]}..." for i, inst in enumerate(recipe_data['instructions'][:3]))}

[0:45-0:55] RESULT
Money shot of final dish
"Would YOU try this?"

[0:55-0:60] CTA
"Recipe in description! Subscribe for more AI recipes!"

TAGS: recipe, cooking, AI, shorts, food, quick recipe
"""

    return {
        'platform': 'youtube_shorts',
        'type': 'video_script',
        'script': script.strip(),
        'duration': '60 seconds',
        'estimated_views': '500-2500'
    }

def generate_email_newsletter(recipe_data):
    """Generate email newsletter snippet"""
    html = f"""<div style="max-width: 600px; font-family: Arial, sans-serif;">
    <h2 style="color: #2c3e50;">🍳 This Week's AI Recipe: {recipe_data['title']}</h2>

    <p>Our AI chef has created something special for you this week!</p>

    <h3>What You'll Need:</h3>
    <ul>
    {''.join(f"<li>{ing}</li>" for ing in recipe_data['ingredients'])}
    </ul>

    <p><a href="https://avatararts.org/recipe" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Get Full Recipe →</a></p>

    <p style="color: #7f8c8d; font-size: 0.9em;">New AI recipes every week! Never miss one.</p>
</div>"""

    return {
        'platform': 'email',
        'type': 'newsletter_snippet',
        'html': html,
        'subject': f"🍳 Try This Week's AI Recipe: {recipe_data['title']}",
        'estimated_open_rate': '25-35%'
    }

def cross_pollinate(recipe_path=None):
    """Generate all social content from one recipe"""
    if recipe_path is None:
        recipe_text = load_latest_recipe()
        if not recipe_text:
            print("❌ No recipe found")
            return None
    else:
        recipe_text = Path(recipe_path).read_text()

    recipe_data = extract_recipe_data(recipe_text)

    # Generate for all platforms
    outputs = {
        'instagram': generate_instagram_post(recipe_data),
        'tiktok': generate_tiktok_script(recipe_data),
        'pinterest': generate_pinterest_pin(recipe_data),
        'youtube_shorts': generate_youtube_short(recipe_data),
        'email': generate_email_newsletter(recipe_data)
    }

    # Save to files
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    output_file = OUTPUT_DIR / f'social_content_{timestamp}.json'
    output_file.write_text(json.dumps(outputs, indent=2))

    # Create markdown summary
    md_file = OUTPUT_DIR / f'social_content_{timestamp}.md'
    md_lines = [
        f"# Social Content: {recipe_data['title']}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "---",
        ""
    ]

    for platform, content in outputs.items():
        md_lines.append(f"## {platform.upper().replace('_', ' ')}")
        md_lines.append("")
        for key, value in content.items():
            if isinstance(value, str) and len(value) > 100:
                md_lines.append(f"**{key}:**")
                md_lines.append(f"```\n{value}\n```")
            else:
                md_lines.append(f"- **{key}:** {value}")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

    md_file.write_text('\n'.join(md_lines))

    return output_file, md_file

if __name__ == '__main__':
    recipe_path = sys.argv[1] if len(sys.argv) > 1 else None

    print("🌐 Cross-Pollination Engine: Recipe → Social")
    print("=" * 50)

    result = cross_pollinate(recipe_path)

    if result:
        json_file, md_file = result
        print(f"\n✅ Generated social content for all platforms!")
        print(f"📄 JSON: {json_file}")
        print(f"📋 Markdown: {md_file}")
        print(f"\n📊 Platforms: Instagram, TikTok, Pinterest, YouTube, Email")
        print(f"💡 Estimated total reach: 2000-10000 impressions")
