#!/usr/bin/env python3
"""AI Content Generator - Use LLMs to generate content automatically"""
import os, sys, json
from pathlib import Path
from datetime import datetime

# Load API keys
sys.path.insert(0, str(Path.home() / '.env.d'))
try:
    from loader import load_env
    load_env()
except:
    print("⚠️  Loading .env.d manually...")
    import subprocess
    result = subprocess.run(['bash', '-c', 'source ~/.env.d/loader.sh && env'],
                          capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if '=' in line:
            key, val = line.split('=', 1)
            os.environ[key] = val

OUTPUT_DIR = Path(__file__).parent / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)

def generate_with_openai(prompt, model="gpt-4o-mini", max_tokens=2000):
    """Generate content using OpenAI"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.8
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error with OpenAI: {e}"

def generate_with_groq(prompt, model="mixtral-8x7b-32768", max_tokens=2000):
    """Generate content using Groq (fast!)"""
    try:
        from groq import Groq
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.8
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error with Groq: {e}"

def generate_content(content_type, topic, provider="groq"):
    """Generate different types of content"""

    prompts = {
        'blog': f"""Write a 1000-word blog post about: {topic}

Include:
- Catchy title
- Engaging introduction
- 3-5 main sections with headers
- Practical tips
- SEO-friendly conclusion
- Call to action

Make it conversational and valuable.""",

        'social': f"""Create 10 social media posts about: {topic}

Requirements:
- Mix of formats (questions, tips, quotes, stories)
- Include emojis
- Add relevant hashtags
- Keep under 280 characters each
- Make them engaging and shareable

Format as JSON array.""",

        'email': f"""Write an email newsletter about: {topic}

Include:
- Subject line (compelling, 50 chars max)
- Greeting
- Main content (3 paragraphs)
- Call to action
- Sign off

Tone: Friendly and professional.""",

        'product': f"""Write a product description for: {topic}

Include:
- Catchy title (60 chars)
- Description (200 chars, SEO-optimized)
- Features (5 bullet points)
- Benefits
- Keywords for SEO

Make it compelling and convert-focused.""",

        'youtube': f"""Write a YouTube video script about: {topic}

Include:
- Hook (first 15 seconds)
- Introduction
- Main content (3-5 sections)
- Transitions
- Call to action
- Outro

Estimated length: 5-8 minutes. Include [visual cues] and timestamps.""",

        'recipe': f"""Create a creative recipe inspired by: {topic}

Include:
- Recipe name
- Ingredients list
- Step-by-step instructions
- Cooking time
- Serving suggestions
- Pro tips

Make it unique and appealing!"""
    }

    prompt = prompts.get(content_type, prompts['blog'])

    print(f"🤖 Generating {content_type} content about '{topic}' using {provider}...")

    if provider == "openai":
        content = generate_with_openai(prompt)
    elif provider == "groq":
        content = generate_with_groq(prompt)
    else:
        return "Unknown provider"

    return content

def batch_generate(content_types, topics, provider="groq"):
    """Generate multiple pieces of content"""
    results = []

    for content_type in content_types:
        for topic in topics:
            print(f"\n📝 Generating {content_type}: {topic}")
            content = generate_content(content_type, topic, provider)

            result = {
                'type': content_type,
                'topic': topic,
                'content': content,
                'generated_at': datetime.now().isoformat(),
                'provider': provider
            }
            results.append(result)

            # Save individual file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{content_type}_{topic[:30].replace(' ', '_')}_{timestamp}.txt"
            output_file = OUTPUT_DIR / filename
            output_file.write_text(content)
            print(f"✅ Saved to: {filename}")

    return results

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("""AI Content Generator - Powered by OpenAI/Groq

Usage: ai_content_generator.py <type> <topic> [provider]

Types:
  blog      - 1000-word blog post
  social    - 10 social media posts
  email     - Email newsletter
  product   - Product description
  youtube   - YouTube video script
  recipe    - Creative recipe

Providers: openai, groq (default: groq - faster!)

Examples:
  ai_content_generator.py blog "AI in music production"
  ai_content_generator.py social "sustainable living tips" openai
  ai_content_generator.py youtube "beginner's guide to digital art"

Batch mode:
  ai_content_generator.py batch blog,social,email "AI art,music production,creative automation"
""")
        sys.exit(1)

    content_type = sys.argv[1]
    topic = sys.argv[2]
    provider = sys.argv[3] if len(sys.argv) > 3 else "groq"

    if content_type == "batch":
        # Batch mode: multiple types and topics
        types = topic.split(',')
        topics_str = sys.argv[3] if len(sys.argv) > 3 else "AI, creativity, automation"
        topics = [t.strip() for t in topics_str.split(',')]
        provider = sys.argv[4] if len(sys.argv) > 4 else "groq"

        results = batch_generate(types, topics, provider)

        # Save master JSON
        master_file = OUTPUT_DIR / f'batch_generation_{datetime.now().strftime("%Y%m%d_%H%M")}.json'
        master_file.write_text(json.dumps(results, indent=2))

        print(f"\n🎉 Generated {len(results)} pieces of content!")
        print(f"📄 Master file: {master_file}")
    else:
        # Single generation
        content = generate_content(content_type, topic, provider)

        # Save
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{content_type}_{topic[:30].replace(' ', '_')}_{timestamp}.txt"
        output_file = OUTPUT_DIR / filename
        output_file.write_text(content)

        print(f"\n✅ Content generated!")
        print(f"📄 Saved to: {output_file}")
        print(f"\n--- Preview ---")
        print(content[:500] + "..." if len(content) > 500 else content)
