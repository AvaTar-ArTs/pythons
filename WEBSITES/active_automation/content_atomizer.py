#!/usr/bin/env python3
"""Content Atomizer - Break 1 piece into 10+ pieces"""
import sys, json
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)

def atomize_blog_post(blog_text, title="Blog Post"):
    """Break blog post into atomic content pieces"""

    atoms = {}

    # 10 Twitter threads
    paragraphs = [p.strip() for p in blog_text.split('\n\n') if p.strip()]
    atoms['twitter_threads'] = []
    for i, para in enumerate(paragraphs[:10]):
        thread = {
            'number': i + 1,
            'hook': para[:100] + '...',
            'thread': f"🧵 Thread {i+1}/10 on {title}\n\n{para}\n\n#thread #tips",
            'length': len(para)
        }
        atoms['twitter_threads'].append(thread)

    # 5 LinkedIn posts
    atoms['linkedin_posts'] = []
    for i in range(min(5, len(paragraphs))):
        atoms['linkedin_posts'].append({
            'number': i + 1,
            'content': f"""💼 {title} - Key Insight #{i+1}

{paragraphs[i]}

What's your experience with this?

#business #professional #insights""",
            'cta': 'engagement'
        })

    # 2 YouTube scripts
    atoms['youtube_scripts'] = [
        {
            'title': f"{title} - Part 1",
            'script': format_as_video(paragraphs[:len(paragraphs)//2]),
            'duration': '5-8 minutes'
        },
        {
            'title': f"{title} - Part 2",
            'script': format_as_video(paragraphs[len(paragraphs)//2:]),
            'duration': '5-8 minutes'
        }
    ]

    # Quote cards
    sentences = [s.strip() for s in blog_text.split('.') if len(s.strip()) > 20]
    atoms['quote_cards'] = []
    for i in range(min(10, len(sentences))):
        atoms['quote_cards'].append({
            'number': i + 1,
            'quote': sentences[i] + '.',
            'design': f"Bold text on gradient background, {title} attribution",
            'platforms': ['Instagram', 'Pinterest', 'Twitter']
        })

    # Infographic sections
    atoms['infographic_data'] = {
        'title': f"{title} - Visual Guide",
        'sections': [
            {'number': i+1, 'content': para[:100]}
            for i, para in enumerate(paragraphs[:5])
        ],
        'style': 'modern, clean, branded'
    }

    # Email series (3 parts)
    third = len(paragraphs) // 3
    atoms['email_series'] = [
        {
            'email': 1,
            'subject': f"{title} - Part 1: Introduction",
            'body': '\n\n'.join(paragraphs[:third])
        },
        {
            'email': 2,
            'subject': f"{title} - Part 2: Deep Dive",
            'body': '\n\n'.join(paragraphs[third:third*2])
        },
        {
            'email': 3,
            'subject': f"{title} - Part 3: Conclusion",
            'body': '\n\n'.join(paragraphs[third*2:])
        }
    ]

    return atoms

def atomize_song(song_title, lyrics):
    """Break song into TikTok clips"""

    atoms = {}

    # Split by verse/chorus
    sections = lyrics.split('\n\n')

    atoms['tiktok_clips'] = []
    for i, section in enumerate(sections):
        atoms['tiktok_clips'].append({
            'clip': i + 1,
            'duration': '15-30 seconds',
            'lyrics': section,
            'visual': f"Lyric typography on dynamic background",
            'music': f"{song_title} - Clip {i+1}"
        })

    # Instagram Reels (same structure)
    atoms['instagram_reels'] = atoms['tiktok_clips'].copy()

    # Audio quotes
    atoms['audio_quotes'] = [
        {
            'number': i + 1,
            'lyric': section.split('\n')[0],
            'duration': '10 seconds',
            'use': 'Instagram Stories, Snapchat'
        }
        for i, section in enumerate(sections[:5])
    ]

    return atoms

def atomize_artwork(art_title, art_description):
    """Break artwork into product mockups"""

    products = [
        'T-Shirt', 'Hoodie', 'Poster', 'Canvas Print', 'Framed Print',
        'Sticker', 'Phone Case', 'Laptop Sleeve', 'Tote Bag', 'Mug',
        'Pillow', 'Duvet Cover', 'Shower Curtain', 'Notebook', 'Greeting Card'
    ]

    atoms = {
        'product_mockups': []
    }

    for product in products:
        atoms['product_mockups'].append({
            'product': product,
            'title': f"{art_title} - {product}",
            'description': f"{art_description} Available as high-quality {product}.",
            'mockup_style': f"{product} mockup on lifestyle background",
            'price_range': get_price_range(product)
        })

    return atoms

def format_as_video(paragraphs):
    """Format paragraphs as video script"""
    script = []
    for i, para in enumerate(paragraphs):
        timestamp = f"{i*30}s"
        script.append(f"[{timestamp}] {para}")
    return '\n\n'.join(script)

def get_price_range(product):
    """Get typical price range"""
    prices = {
        'T-Shirt': '$19-29', 'Hoodie': '$35-45', 'Poster': '$12-20',
        'Sticker': '$2-5', 'Phone Case': '$15-25', 'Mug': '$12-18'
    }
    return prices.get(product, '$15-30')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: content_atomizer.py <type> <content_file>")
        print("Types: blog, song, art")
        print("\nExample: content_atomizer.py blog my_post.txt")
        sys.exit(1)

    content_type = sys.argv[1]
    content_file = Path(sys.argv[2])

    if not content_file.exists():
        print(f"❌ File not found: {content_file}")
        sys.exit(1)

    content = content_file.read_text()
    title = content_file.stem

    print(f"⚛️ Atomizing {content_type}: {title}")
    print("=" * 50)

    if content_type == 'blog':
        atoms = atomize_blog_post(content, title)
    elif content_type == 'song':
        atoms = atomize_song(title, content)
    elif content_type == 'art':
        atoms = atomize_artwork(title, content)
    else:
        print(f"❌ Unknown type: {content_type}")
        sys.exit(1)

    # Save atoms
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    output_file = OUTPUT_DIR / f'atoms_{content_type}_{timestamp}.json'
    output_file.write_text(json.dumps(atoms, indent=2))

    print(f"\n✅ Atomized into {sum(len(v) if isinstance(v, list) else 1 for v in atoms.values())} pieces")
    print(f"📄 Saved to: {output_file}")

    # Print summary
    print(f"\n📊 Breakdown:")
    for atom_type, atom_data in atoms.items():
        count = len(atom_data) if isinstance(atom_data, list) else 1
        print(f"   {atom_type}: {count}")

    print(f"\n💡 1 {content_type} → {sum(len(v) if isinstance(v, list) else 1 for v in atoms.values())}+ content pieces!")
