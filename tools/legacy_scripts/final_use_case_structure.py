#!/usr/bin/env python3
"""
Final USE-CASE Optimized Structure
Organize by what you want to DO, not what files ARE
"""
import shutil
from pathlib import Path

base_dir = Path("/Users/steven/Documents/python")

# USE-CASE based organization map
USE_CASE_STRUCTURE = {
    'AI_CONTENT': {
        'text_generation': ['prompt', 'gpt', 'claude', 'completion', 'chat'],
        'image_generation': ['dalle', 'midjourney', 'leonardo', 'img_gen'],
        'voice_synthesis': ['tts', 'elevenlabs', 'voice', 'speech', 'audio_synthesis'],
        'ai_tools': ['ollama', 'ai_chat', 'ai_core_tools', 'format_converters']
    },
    'AUTOMATION_BOTS': {
        'instagram_bots': ['instagram', 'insta', 'ig_'],
        'youtube_bots': ['youtube', 'yt_', 'shorts'],
        'reddit_bots': ['reddit', 'askreddit', 'praw'],
        'twitter_bots': ['twitter', 'tweet', 'tweepy'],
        'web_scrapers': ['scrape', 'crawl', 'selenium', 'playwright'],
        'bot_tools': ['bot_frameworks', 'uploader', 'web_tools']
    },
    'MEDIA_PROCESSING': {
        'video_tools': ['video', 'mp4', 'moviepy', 'ffmpeg', 'video_editor'],
        'audio_tools': ['audio', 'mp3', 'wav', 'pydub', 'audio_processing'],
        'image_tools': ['image', 'photo', 'jpg', 'png', 'pillow'],
        'transcription': ['transcribe', 'whisper', 'subtitle', 'speech_to_text'],
        'converters': ['convert', 'transform', 'encode'],
        'enhancers': ['upscale', 'enhance', 'improve'],
        'galleries': ['gallery', 'album', 'slideshow']
    },
    'DATA_UTILITIES': {
        'spreadsheet_tools': ['csv', 'excel', 'pandas', 'spreadsheet_tools'],
        'json_tools': ['json', 'parse', 'json_tools'],
        'document_tools': ['pdf', 'doc', 'document_processors'],
        'file_organizers': ['organize', 'sort', 'file_organization'],
        'data_analyzers': ['analyze', 'analysis', 'data_analysis'],
        'downloaders': ['download', 'fetch', 'downloader'],
        'dev_tools': ['editor', 'development', 'clipboard', 'utilities']
    }
}

def get_best_use_case(dir_name: str, parent_category: str) -> str:
    """Determine best use case for a directory"""
    dir_lower = dir_name.lower()

    if parent_category not in USE_CASE_STRUCTURE:
        return None

    use_cases = USE_CASE_STRUCTURE[parent_category]

    # Score each use case
    scores = {}
    for use_case, keywords in use_cases.items():
        score = sum(10 if kw in dir_lower else 0 for kw in keywords)
        scores[use_case] = score

    # Return best match if score > 0
    best_use_case = max(scores, key=scores.get)
    return best_use_case if scores[best_use_case] > 0 else None

def main():
    print("="*70)
    print("🎯 FINAL USE-CASE OPTIMIZATION")
    print("="*70)
    print()

    moves = []

    # Scan each main category
    for category in ['AI_CONTENT', 'AUTOMATION_BOTS', 'MEDIA_PROCESSING', 'DATA_UTILITIES']:
        cat_path = base_dir / category
        if not cat_path.exists():
            continue

        # Get immediate subdirectories
        for subdir in cat_path.iterdir():
            if not subdir.is_dir():
                continue

            # Skip if already in use-case format
            if subdir.name in USE_CASE_STRUCTURE[category]:
                continue

            # Determine best use case
            use_case = get_best_use_case(subdir.name, category)
            if use_case and use_case != subdir.name:
                target = cat_path / use_case / subdir.name
                moves.append((subdir, target, category, use_case))

    print(f"Found {len(moves)} optimizations")
    print()

    # Group by category
    by_category = {}
    for source, target, category, use_case in moves:
        if category not in by_category:
            by_category[category] = []
        by_category[category].append((source, target, use_case))

    # Show plan
    for category, items in sorted(by_category.items()):
        print(f"📁 {category}")
        for source, target, use_case in items[:5]:
            rel_s = source.relative_to(base_dir)
            rel_t = target.relative_to(base_dir)
            print(f"   {rel_s}")
            print(f"   → {rel_t}")
        if len(items) > 5:
            print(f"   ... and {len(items)-5} more")
        print()

    # Execute
    if moves:
        print("🚀 Executing optimizations...")
        success = 0
        for source, target, category, use_case in moves:
            try:
                target.parent.mkdir(parents=True, exist_ok=True)

                if target.exists():
                    # Merge
                    for item in source.rglob('*'):
                        if item.is_file():
                            rel = item.relative_to(source)
                            dest = target / rel
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            if not dest.exists():
                                shutil.move(str(item), str(dest))
                    try:
                        shutil.rmtree(source)
                    except:
                        pass
                else:
                    shutil.move(str(source), str(target))

                success += 1
            except Exception as e:
                print(f"   ❌ Error: {str(e)[:50]}")

        print()
        print(f"✅ Optimized {success}/{len(moves)} directories")
    else:
        print("✅ Structure is already optimal!")

    print("="*70)

if __name__ == '__main__':
    main()
