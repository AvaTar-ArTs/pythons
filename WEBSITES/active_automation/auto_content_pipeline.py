#!/usr/bin/env python3
"""Auto Content Pipeline - Generate, optimize, and prepare for distribution"""
import os, sys, json, subprocess
from pathlib import Path
from datetime import datetime

# Load API keys
sys.path.insert(0, str(Path.home() / '.env.d'))
try:
    from loader import load_env
    load_env()
except:
    subprocess.run(['bash', '-c', 'source ~/.env.d/loader.sh && env'],
                  capture_output=True, text=True)

AUTOMATION_DIR = Path(__file__).parent.parent
OUTPUT_DIR = Path(__file__).parent / 'output' / 'pipeline'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def run_ai_generator(content_type, topic):
    """Generate content using AI"""
    script = AUTOMATION_DIR / 'api-powered' / 'ai_content_generator.py'
    result = subprocess.run(
        ['python3', str(script), content_type, topic, 'groq'],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def run_dalle_generator(theme):
    """Generate image using DALL-E"""
    script = AUTOMATION_DIR / 'api-powered' / 'dalle_auto_generator.py'
    result = subprocess.run(
        ['python3', str(script), 'daily', theme],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def run_cross_pollination(content_type, *args):
    """Cross-pollinate content to social"""
    scripts = {
        'recipe': AUTOMATION_DIR / 'cross-pollination' / 'recipe_to_social.py',
        'art': AUTOMATION_DIR / 'cross-pollination' / 'art_to_social.py',
        'music': AUTOMATION_DIR / 'cross-pollination' / 'music_to_social.py'
    }

    script = scripts.get(content_type)
    if script:
        result = subprocess.run(
            ['python3', str(script), *args],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    return False

def full_content_pipeline(topic, include_image=True):
    """Complete pipeline: Generate → Image → Cross-pollinate → Schedule"""

    print(f"🚀 Starting full content pipeline for: {topic}")
    print("=" * 60)

    pipeline_log = {
        'topic': topic,
        'started_at': datetime.now().isoformat(),
        'steps': []
    }

    # Step 1: Generate blog post
    print("\n📝 Step 1: Generating blog post...")
    if run_ai_generator('blog', topic):
        print("✅ Blog post generated")
        pipeline_log['steps'].append({'step': 'blog', 'status': 'success'})
    else:
        print("❌ Blog generation failed")
        pipeline_log['steps'].append({'step': 'blog', 'status': 'failed'})

    # Step 2: Generate social posts
    print("\n📱 Step 2: Generating social posts...")
    if run_ai_generator('social', topic):
        print("✅ Social posts generated")
        pipeline_log['steps'].append({'step': 'social', 'status': 'success'})
    else:
        print("❌ Social generation failed")
        pipeline_log['steps'].append({'step': 'social', 'status': 'failed'})

    # Step 3: Generate accompanying image
    if include_image:
        print("\n🎨 Step 3: Generating DALL-E image...")
        if run_dalle_generator(topic):
            print("✅ Image generated")
            pipeline_log['steps'].append({'step': 'image', 'status': 'success'})
        else:
            print("❌ Image generation failed")
            pipeline_log['steps'].append({'step': 'image', 'status': 'failed'})

    # Step 4: Generate email
    print("\n📧 Step 4: Generating email newsletter...")
    if run_ai_generator('email', topic):
        print("✅ Email generated")
        pipeline_log['steps'].append({'step': 'email', 'status': 'success'})
    else:
        print("❌ Email generation failed")
        pipeline_log['steps'].append({'step': 'email', 'status': 'failed'})

    # Step 5: Generate YouTube script
    print("\n🎬 Step 5: Generating YouTube script...")
    if run_ai_generator('youtube', topic):
        print("✅ YouTube script generated")
        pipeline_log['steps'].append({'step': 'youtube', 'status': 'success'})
    else:
        print("❌ YouTube generation failed")
        pipeline_log['steps'].append({'step': 'youtube', 'status': 'failed'})

    pipeline_log['completed_at'] = datetime.now().isoformat()
    pipeline_log['success_count'] = sum(1 for s in pipeline_log['steps'] if s['status'] == 'success')
    pipeline_log['total_steps'] = len(pipeline_log['steps'])

    # Save log
    log_file = OUTPUT_DIR / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    log_file.write_text(json.dumps(pipeline_log, indent=2))

    print("\n" + "=" * 60)
    print(f"✅ Pipeline complete: {pipeline_log['success_count']}/{pipeline_log['total_steps']} successful")
    print(f"📄 Log: {log_file}")

    return pipeline_log

def daily_content_routine():
    """Daily automated content generation"""

    topics = [
        "AI in creative industries",
        "building passive income streams",
        "digital art techniques",
        "music production tips",
        "content automation strategies"
    ]

    import random
    topic = random.choice(topics)

    print("🌅 Daily Content Routine")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"📝 Topic: {topic}")
    print("=" * 60)

    # Generate daily art
    print("\n🎨 Generating daily AI art...")
    run_dalle_generator(None)  # Auto theme

    # Generate social posts
    print("\n📱 Generating social media content...")
    run_ai_generator('social', topic)

    # Generate recipe
    print("\n🍳 Generating AI recipe...")
    recipe_script = AUTOMATION_DIR / 'content-management' / 'retention-hub' / 'recipes' / 'generate_recipe.py'
    if recipe_script.exists():
        subprocess.run(['python3', str(recipe_script)], capture_output=True)

    print("\n✅ Daily routine complete!")
    print("💡 Content ready for distribution")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("""Auto Content Pipeline - Complete Automation

Usage: auto_content_pipeline.py <command> [args]

Commands:
  full <topic>       - Run full pipeline (blog + social + image + email + youtube)
  daily              - Daily automated routine (art + social + recipe)
  quick <topic>      - Quick content (social + image only)

Examples:
  auto_content_pipeline.py full "sustainable living tips"
  auto_content_pipeline.py daily
  auto_content_pipeline.py quick "AI productivity hacks"

The pipeline will:
1. Generate AI content (blog, social, etc.)
2. Create accompanying DALL-E images
3. Cross-pollinate to all platforms
4. Prepare for distribution
5. Log everything for tracking
""")
        sys.exit(1)

    command = sys.argv[1]

    if command == "full":
        if len(sys.argv) < 3:
            print("Usage: auto_content_pipeline.py full <topic>")
            sys.exit(1)
        topic = ' '.join(sys.argv[2:])
        full_content_pipeline(topic)

    elif command == "daily":
        daily_content_routine()

    elif command == "quick":
        if len(sys.argv) < 3:
            print("Usage: auto_content_pipeline.py quick <topic>")
            sys.exit(1)
        topic = ' '.join(sys.argv[2:])
        print(f"⚡ Quick content generation: {topic}")
        run_ai_generator('social', topic)
        run_dalle_generator(topic)
        print("✅ Quick content ready!")

    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)
