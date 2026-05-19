#!/usr/bin/env python3
"""Cross-Pollination Engine - Music Release → All Social Platforms"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_music_release_posts(track_title, genre="electronic", release_date=None):
    """Generate comprehensive social media campaign for music release"""

    if release_date is None:
        release_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

    posts = {}

    # Instagram Posts
    posts["instagram"] = {
        "pre_save": {
            "caption": f"""🎵 NEW MUSIC DROPPING {release_date}!

"{track_title}" is coming to all platforms.

Pre-save now (link in bio) and be the first to hear it!

What vibe are you expecting from the title? Drop your guess below! 👇

#NewMusic #ComingSoon #IndieArtist #{genre.title()} #MusicProduction #IndependentMusic #NewRelease #PreSave #StreamingNow #MusicIsLife""",
            "image_prompt": f"Album artwork for '{track_title}', {genre} music style, vibrant colors, modern design, 3000x3000px square format, professional music cover art",
        },
        "release_day": {
            "caption": f"""🚀 OUT NOW ON ALL PLATFORMS!

"{track_title}" is officially live!

Stream it now:
🎧 Spotify
🍎 Apple Music
🎵 Amazon Music
🎬 YouTube Music

+ More (link in bio)

Add it to your playlists and let me know what you think! 💭

#NewMusicFriday #OutNow #IndieMusic #{genre.title()} #StreamingNow #NewRelease #MusicLover #PlaylistReady #AvaTarArTs""",
            "image_prompt": f"Music release announcement for '{track_title}', bold 'OUT NOW' text, streaming platform icons, vibrant {genre} themed colors, 1080x1080px",
        },
        "snippet": {
            "caption": f'\''🎶 Here's a taste of "{track_title}"

Full track out now on all platforms (link in bio)

Turn up the volume 🔊

#MusicSnippet #{genre.title()}Music #NewMusic #IndieArtist #MusicProducer""",
            "video": "30-second snippet (hook/drop/best section)",
        },
    }

    # TikTok/Instagram Reels Scripts
    posts["tiktok_reels"] = {
        "pre_save_hype": {
            "script": f"""[0-3s] Hook: "New music dropping in [X] days..."
[3-8s] Show creation process / visualizer
[8-15s] Play snippet (10-15 sec best part)
[15-20s] "Pre-save link in bio! 🔗"
[20-30s] Outro with release date overlay

Text Overlays:
- "{track_title}"
- "OUT {release_date}"
- "Pre-save now 🎵"

Hashtags: #newmusic #comingsoon #musicproducer #{genre}music #independentartist #presave #musicrelease""",
            "duration": "30 seconds",
        },
        "release_announcement": {
            "script": f"""[0-2s] "IT'S FINALLY HERE!"
[2-5s] Album artwork reveal
[5-25s] Best 20-second section of track
[25-28s] "Out now on all platforms!"
[28-30s] CTA: "Link in bio"

Text Overlays:
- "OUT NOW 🚀"
- "{track_title}"
- "Stream it now!"

Hashtags: #newmusicfriday #outnow #{genre} #musicrelease #independentartist #streamingn now""",
            "duration": "30 seconds",
        },
        "behind_the_scenes": {
            "script": f"""[0-5s] "How I made '{track_title}'..."
[5-15s] Show DAW, plugins, creative process
[15-25s] Play preview with process overlay
[25-30s] "Full track out now!"

Style: Raw, authentic, educational

Hashtags: #musicproduction #producerlife #beatmaking #studioflow #{genre}producer #musicproducer""",
            "duration": "30-60 seconds",
        },
    }

    # YouTube Posts
    posts["youtube"] = {
        "audio_upload": {
            "title": f"{track_title} - AvaTarArTs | {genre.title()} Music",
            "description": f"""Stream "{track_title}" now:
🎧 Spotify: [LINK]
🍎 Apple Music: [LINK]
🎵 All Platforms: [LINK]

{genre.title()} track by AvaTarArTs. Perfect for playlists, background music, study sessions, workouts, and more.

📱 Follow me:
Instagram: @avatararts
TikTok: @avatararts
Twitter: @avatararts

Support independent music! Like, subscribe, and add to your playlists.

© {datetime.now().year} AvaTarArTs. All rights reserved.

#newmusic #{genre} #independentartist #musicproducer'\'',
            "tags": [
                track_title,
                genre,
                "new music",
                "independent artist",
                "music producer",
                "instrumental",
                "background music",
                "streaming",
                f"{genre} music",
            ],
            "thumbnail_prompt": f"YouTube thumbnail for '{track_title}', bold text, {genre} aesthetic, vibrant colors, 1280x720px, eye-catching",
        },
        "visualizer": {
            "title": f"{track_title} (Official Visualizer) - AvaTarArTs",
            "description": f"""Official visualizer for "{track_title}"

{genre.title()} music by AvaTarArTs. Stream now on all platforms.

🎧 Listen: [LINK]

Visual design matches the energy and mood of the track.

Subscribe for more music + visualizers!

#visualizer #musicvideo #{genre}music""",
            "video_style": f"Audio reactive visualizer, {genre} themed colors and effects, mesmerizing patterns",
        },
    }

    # Twitter/X Posts
    posts["twitter"] = {
        "announcement": f'🎵 NEW MUSIC\n\n"{track_title}" out {release_date}\n\nPre-save: [LINK]\n\n#{genre.title()}Music #NewRelease',
        "release_day": f'🚀 OUT NOW\n\n"{track_title}" is live on all platforms!\n\nStream: [LINK]\n\nAdd to your playlists! 🎧\n\n#NewMusicFriday #OutNow',
        "milestone": f'🎉 "{track_title}" just hit [X] streams!\n\nThanks for the support! 🙏\n\nKeep streaming: [LINK]\n\n#IndieMusic',
    }

    # Spotify Canvas Script
    posts["spotify_canvas"] = {
        "specs": "9:16 aspect ratio, 3-8 seconds, looping, no audio",
        "concept": f"Abstract {genre} themed visuals, synchronized to beat/rhythm, looping seamlessly",
        "examples": [
            "Pulsing geometric shapes synced to beat",
            "Color gradient waves flowing with melody",
            "Particle effects following rhythm",
            "Abstract 3D shapes rotating/morphing",
        ],
    }

    # Email Newsletter
    posts["email"] = {
        "subject": f"🎵 New Track: {track_title} - Out {release_date}!",
        "html": f'\''<div style="max-width: 600px; font-family: Arial; text-align: center;">
<h1 style="color: #1DB954;">🎵 New Music Alert!</h1>

<h2>{track_title}</h2>

<p>I'm excited to share my latest {genre} track with you.</p>

<p><strong>Release Date:</strong> {release_date}</p>

<a href="[PRE_SAVE_LINK]" style="background: #1DB954; color: white; padding: 15px 30px; text-decoration: none; border-radius: 30px; display: inline-block; margin: 20px 0; font-weight: bold;">Pre-Save Now</a>

<p>Be the first to hear it when it drops!</p>

<p style="color: #7f8c8d; font-size: 0.9em;">Available on Spotify, Apple Music, Amazon Music, YouTube Music, and more.</p>

<hr style="margin: 30px 0;">

<p style="font-size: 0.85em; color: #999;">AvaTarArTs • Independent Music</p>
</div>""",
        "plain": f"""New Music: {track_title}

Out {release_date} on all platforms!

Pre-save now: [LINK]

Thanks for your support!
- AvaTarArTs'\'',
    }

    # Playlist Pitch (for Spotify editorial)
    posts["spotify_pitch"] = {
        "title": track_title,
        "genre": genre,
        "mood": f"Energetic, uplifting, perfect for {genre} playlists",
        "style": f"Modern {genre} with electronic elements",
        "description": f"AI-generated {genre} track with professional production quality. Perfect for workout, study, focus, or chill playlists.",
        "similar_artists": "Independent electronic artists, AI music producers",
        "story": f"Created using cutting-edge AI music generation, refined and produced by AvaTarArTs. Part of a larger collection exploring {genre} soundscapes.",
    }

    # Reddit Posts
    posts["reddit"] = {
        "subreddits": [
            "r/IndieMusic",
            "r/ThisIsOurMusic",
            "r/MusicPromotion",
            f"r/{genre}",
        ],
        "title": f"[{genre.title()}] Just released '{track_title}' - would love your feedback!",
        "body": f"""Hey everyone! I just released my latest {genre} track and would really appreciate some feedback.

**Title:** {track_title}
**Genre:** {genre.title()}
**Streaming:** [All platforms link]

What I was going for: [Brief description of the vibe/inspiration]

Let me know what you think! Always looking to improve.

Thanks for listening! 🎧""",
    }

    return posts


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: music_to_social.py '<track_title>' [genre] [release_date]")
        print("\nExample: music_to_social.py 'Neon Dreams' electronic 2025-11-01")
        sys.exit(1)

    track_title = sys.argv[1]
    genre = sys.argv[2] if len(sys.argv) > 2 else "electronic"
    release_date = sys.argv[3] if len(sys.argv) > 3 else None

    print(f"🎵 Generating social campaign for: {track_title}")
    print(f"   Genre: {genre}")
    print("=" * 60)

    posts = generate_music_release_posts(track_title, genre, release_date)

    # Save JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    json_file = OUTPUT_DIR / f"music_social_{timestamp}.json"
    json_file.write_text(json.dumps(posts, indent=2))

    # Save Markdown
    md_file = OUTPUT_DIR / f"music_social_{timestamp}.md"
    md_lines = [
        f"# Music Release Campaign: {track_title}",
        f"**Genre:** {genre.title()}",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "---",
        "",
    ]

    for platform, content in posts.items():
        md_lines.append(f"## {platform.upper().replace('_', ' ')}")
        md_lines.append("")
        md_lines.append(f"```json\n{json.dumps(content, indent=2)}\n```")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

    md_file.write_text("\n".join(md_lines))

    print("\n✅ Generated complete release campaign!")
    print(f"📄 JSON: {json_file}")
    print(f"📋 Markdown: {md_file}")
    print("\n📊 Campaign includes:")
    print("   • Instagram (3 post types)")
    print("   • TikTok/Reels (3 scripts)")
    print("   • YouTube (2 upload types)")
    print("   • Twitter (3 posts)")
    print("   • Spotify Canvas specs")
    print("   • Email newsletter")
    print("   • Spotify editorial pitch")
    print("   • Reddit posts")
    print("\n💡 Total reach: 10,000-50,000+ impressions across all platforms")
