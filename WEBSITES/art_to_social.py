import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""Cross-Pollination Engine - Daily Art → All Social Platforms"""

import sys
import json
from pathlib import Path
from datetime import datetime

CONTENT_DIR = (
    Path.home() / "ai-sites" / "content-management" / "retention-hub" / "daily-art"
)
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_social_posts(art_title, art_theme):
    """Generate social posts for art drop"""

    posts = {}

    # Instagram
    posts["instagram"] = {
        "caption": f"""🎨 Daily AI Art Drop: {art_title}

{art_theme}

Created with cutting-edge AI art generation. Prints available!

#aiart #digitalart #generativeart #abstract #modernart #artoftheday #dailyart #contemporaryart #artwork #creative""",
        "hashtags": 10,
    }

    # Twitter/X
    posts["twitter"] = {
        "tweet": f"🎨 {art_title}\n\n{art_theme}\n\nDaily AI art drop!\n\n#AIArt #DigitalArt #GenerativeArt\n\n🖼️ Prints: avatararts.org",
        "chars": len(f"{art_title} {art_theme}") + 60,
    }

    # Reddit
    posts["reddit"] = {
        "title": f"[OC] {art_title} - Daily AI Art",
        "body": f"**{art_title}**\n\nTheme: {art_theme}\n\nGenerated using AI art tools. Part of my daily art series.\n\nMore at avatararts.org",
        "subreddits": ["r/aiArt", "r/MediaSynthesis", "r/generative", "r/Art"],
    }

    # Facebook
    posts["facebook"] = {
        "post": f"🎨 Today's AI Art: {art_title}\n\n{art_theme}\n\nNew art every day! Follow for more.\n\nPrints and merch available at AvaTarArTs.org"
    }

    return posts


try:
        art_title = sys.argv[1] if len(sys.argv) > 1 else "Cosmic Dreams"
        art_theme = (
            sys.argv[2]
            if len(sys.argv) > 2
            else "Exploring the intersection of technology and nature"
        )
        posts = generate_social_posts(art_title, art_theme)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        output_file = OUTPUT_DIR / f"art_social_{timestamp}.json"
        output_file.write_text(json.dumps(posts, indent=2))
        print(f"✅ Generated social posts for: {art_title}")
        print(f"📄 Saved to: {output_file}")
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)