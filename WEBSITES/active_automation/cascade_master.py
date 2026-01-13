#!/usr/bin/env python3
"""Template Cascade - One master content → All formats"""
import sys, json
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)

def cascade_content(master_content, title="Content Piece"):
    """Cascade master content to all formats"""

    outputs = {}

    # Blog post (1200 words)
    outputs['blog_post'] = {
        'format': 'blog',
        'word_count': 1200,
        'content': f"""# {title}

## Introduction

{master_content[:200]}...

## Main Content

{master_content}

## Key Takeaways

- [Auto-generated bullet points]

## Conclusion

{master_content[-200:]}...

---
*Published: {datetime.now().strftime('%Y-%m-%d')}*
*Author: AvaTarArTs*
""",
        'seo_keywords': extract_keywords(master_content)
    }

    # YouTube script (8 min ~ 1100 words)
    outputs['youtube_script'] = {
        'format': 'video_script',
        'duration': '8 minutes',
        'content': f"""📹 YouTube Script: {title}

[INTRO - 0:00-0:30]
Hook: {master_content[:100]}...
"In this video, we'll explore..."

[MAIN CONTENT - 0:30-7:00]
{format_for_voiceover(master_content)}

[OUTRO - 7:00-8:00]
Summary: Key points recap
CTA: "Like, subscribe, comment!"
End screen: Related videos

B-ROLL SUGGESTIONS:
- [Auto-generated based on content]

MUSIC: Upbeat, energetic
""",
        'chapters': generate_chapters(master_content)
    }

    # 10 social posts
    outputs['social_posts'] = {
        'format': 'social_media',
        'count': 10,
        'posts': generate_social_snippets(master_content, title, 10)
    }

    # Email newsletter
    outputs['email_newsletter'] = {
        'format': 'email',
        'subject': f"📧 {title}",
        'html': f"""<div style="max-width: 600px; font-family: Arial;">
<h1>{title}</h1>

<p>{master_content[:300]}...</p>

<a href="https://avatararts.org" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Read More →</a>

<hr>
<p style="font-size: 0.9em; color: #7f8c8d;">AvaTarArTs • {datetime.now().year}</p>
</div>"""
    }

    # Product descriptions (for merch)
    outputs['product_descriptions'] = {
        'format': 'ecommerce',
        'count': 5,
        'descriptions': [
            f"T-Shirt: {title} - {master_content[:100]}...",
            f"Poster: {title} - {master_content[:100]}...",
            f"Sticker: {title} - {master_content[:80]}...",
            f"Mug: {title} - {master_content[:80]}...",
            f"Phone Case: {title} - {master_content[:80]}..."
        ]
    }

    # Pinterest descriptions
    outputs['pinterest_descriptions'] = {
        'format': 'pinterest',
        'pins': [
            {
                'title': f"{title} - Complete Guide",
                'description': f"{master_content[:400]}... #guide #tutorial #howto"
            },
            {
                'title': f"Everything About {title}",
                'description': f"{master_content[:400]}... #tips #advice #learn"
            }
        ]
    }

    return outputs

def extract_keywords(text, limit=10):
    """Extract key terms from text"""
    # Simple extraction - can be enhanced with NLP
    words = text.lower().split()
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
    keywords = [w.strip('.,!?') for w in words if len(w) > 4 and w not in common_words]
    return list(set(keywords))[:limit]

def format_for_voiceover(text):
    """Format text for video voiceover"""
    sentences = text.split('. ')
    formatted = []
    for i, sentence in enumerate(sentences):
        if sentence:
            formatted.append(f"[{i*10}s] {sentence}.")
    return '\n'.join(formatted)

def generate_chapters(text):
    """Generate video chapters"""
    # Simple chapter generation
    return [
        {'time': '0:00', 'title': 'Introduction'},
        {'time': '0:30', 'title': 'Main Content'},
        {'time': '7:00', 'title': 'Conclusion'}
    ]

def generate_social_snippets(text, title, count=10):
    """Generate bite-sized social posts"""
    sentences = [s.strip() for s in text.split('. ') if s.strip()]
    snippets = []

    for i in range(min(count, len(sentences))):
        snippets.append({
            'platform': 'twitter/instagram',
            'content': f"💡 {sentences[i]}.\n\n#{title.replace(' ', '')} #tips",
            'number': i + 1
        })

    return snippets

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: cascade_master.py '<master_content>' '<title>'")
        print("\nGenerates: blog post, YouTube script, 10 social posts, email, product descriptions")
        sys.exit(1)

    master_content = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else "Untitled"

    print(f"🌊 Cascading content: {title}")
    print("=" * 50)

    outputs = cascade_content(master_content, title)

    # Save all outputs
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')

    for format_name, format_data in outputs.items():
        output_file = OUTPUT_DIR / f'{format_name}_{timestamp}.json'
        output_file.write_text(json.dumps(format_data, indent=2))
        print(f"✅ {format_name}: {output_file.name}")

    # Create master index
    index_file = OUTPUT_DIR / f'cascade_index_{timestamp}.md'
    index_content = [
        f"# Content Cascade: {title}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Formats Generated:",
        "- Blog Post (1200 words)",
        "- YouTube Script (8 min)",
        "- Social Posts (10x)",
        "- Email Newsletter",
        "- Product Descriptions (5x)",
        "- Pinterest Pins (2x)",
        "",
        "## Files:",
        ""
    ]

    for format_name in outputs.keys():
        index_content.append(f"- `{format_name}_{timestamp}.json`")

    index_file.write_text('\n'.join(index_content))

    print(f"\n📋 Index: {index_file}")
    print(f"\n💡 Total formats: {len(outputs)}")
    print("   Write once, publish everywhere!")
