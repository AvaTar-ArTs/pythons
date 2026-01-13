#!/usr/bin/env python3
"""DistroKid Bulk Upload Prep - Get 100+ tracks ready for distribution"""
import csv, json, sys
from pathlib import Path
from datetime import datetime

MUSIC_DIR = Path.home() / 'Music'
SUNO_DIRS = [
    MUSIC_DIR / 'SUNO',
    MUSIC_DIR / 'nocTurneMeLoDieS',
    MUSIC_DIR / 'mp3-bin',
    MUSIC_DIR / 'PetalsFall'
]
OUTPUT_DIR = Path(__file__).parent / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)

# DistroKid genres
GENRES = {
    'electronic': ['electronic', 'edm', 'techno', 'synth', 'house', 'trance'],
    'pop': ['pop', 'indie', 'alternative', 'modern'],
    'rock': ['rock', 'guitar', 'punk', 'metal'],
    'hip-hop': ['hip', 'hop', 'rap', 'beat', 'trap'],
    'ambient': ['ambient', 'chill', 'lofi', 'meditation', 'relaxing'],
    'classical': ['classical', 'orchestral', 'piano', 'strings'],
    'jazz': ['jazz', 'blues', 'swing'],
    'country': ['country', 'folk', 'acoustic', 'americana'],
    'r&b': ['r&b', 'soul', 'funk'],
    'latin': ['latin', 'reggaeton', 'salsa', 'bachata']
}

# Streaming platforms
PLATFORMS = [
    'Spotify', 'Apple Music', 'Amazon Music', 'YouTube Music',
    'Tidal', 'Deezer', 'Pandora', 'iHeartRadio',
    'Instagram/Facebook', 'TikTok', 'Snapchat'
]

def find_tracks(limit=100):
    """Find music tracks ready for distribution"""
    tracks = []

    for suno_dir in SUNO_DIRS:
        if not suno_dir.exists():
            continue

        for track_path in suno_dir.rglob('*'):
            if track_path.suffix.lower() in ['.mp3', '.wav', '.flac']:
                # Check if it's high quality enough (size check)
                size_mb = track_path.stat().st_size / 1024 / 1024
                if size_mb < 1:  # Skip low-quality tracks
                    continue

                tracks.append({
                    'path': str(track_path),
                    'filename': track_path.name,
                    'name': track_path.stem,
                    'format': track_path.suffix[1:].upper(),
                    'size_mb': round(size_mb, 2),
                    'directory': track_path.parent.name
                })

                if len(tracks) >= limit:
                    break

        if len(tracks) >= limit:
            break

    return tracks[:limit]

def detect_genre(track_name):
    """Detect genre from filename"""
    name_lower = track_name.lower()

    for genre, keywords in GENRES.items():
        if any(kw in name_lower for kw in keywords):
            return genre

    return 'electronic'  # Default

def generate_metadata(track):
    """Generate DistroKid-ready metadata"""
    name = track['name'].replace('_', ' ').replace('-', ' ')
    words = [w.title() for w in name.split() if len(w) > 1]

    # Track title (clean)
    title = ' '.join(words[:8]) if words else track['name']

    # Artist name
    artist = 'AvaTarArTs'

    # Genre
    genre = detect_genre(track['name'])

    # Album name (based on directory or date)
    album = f"{track['directory']} Collection" if track['directory'] != 'Music' else f"Singles {datetime.now().year}"

    # Release date (suggest 2 weeks out for pre-saves)
    release_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')

    # Generate description
    description = f"{title} by {artist}. {genre.title()} music created with AI. Perfect for playlists, workouts, study sessions, and more."

    # Generate lyrics placeholder
    lyrics = "[Instrumental]"

    # ISRC code placeholder
    isrc = f"PLACEHOLDER-{datetime.now().year}-{hash(track['name']) % 10000:04d}"

    return {
        'filename': track['filename'],
        'title': title[:80],  # DistroKid limit
        'artist': artist,
        'album': album[:80],
        'genre': genre,
        'release_date': release_date,
        'description': description[:500],
        'lyrics': lyrics,
        'isrc': isrc,
        'language': 'Instrumental',
        'explicit': 'No',
        'copyright': f'℗ {datetime.now().year} {artist}',
        'platforms': ', '.join(PLATFORMS[:8]),  # Top 8
        'price_tier': 'Standard'
    }

def create_upload_csv(tracks, output_path=None):
    """Create CSV for DistroKid bulk upload"""
    if output_path is None:
        output_path = OUTPUT_DIR / f'distrokid_upload_{datetime.now().strftime("%Y%m%d_%H%M")}.csv'

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'filename', 'title', 'artist', 'album', 'genre', 'release_date',
            'description', 'lyrics', 'isrc', 'language', 'explicit',
            'copyright', 'platforms'
        ])

        for track in tracks:
            meta = generate_metadata(track)
            writer.writerow([
                track['path'],
                meta['title'],
                meta['artist'],
                meta['album'],
                meta['genre'],
                meta['release_date'],
                meta['description'],
                meta['lyrics'],
                meta['isrc'],
                meta['language'],
                meta['explicit'],
                meta['copyright'],
                meta['platforms']
            ])

    return output_path

def create_release_checklist(tracks, output_path=None):
    """Create release checklist with marketing plan"""
    if output_path is None:
        output_path = OUTPUT_DIR / f'distrokid_checklist_{datetime.now().strftime("%Y%m%d_%H%M")}.md'

    # Group by genre
    by_genre = {}
    for track in tracks:
        meta = generate_metadata(track)
        genre = meta['genre']
        if genre not in by_genre:
            by_genre[genre] = []
        by_genre[genre].append((track, meta))

    content = [
        "# DistroKid Release Checklist\n",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
        f"**Total Tracks:** {len(tracks)}\n",
        f"**Artist:** AvaTarArTs\n",
        "---\n\n",
        "## 📋 Pre-Release Checklist\n",
        "- [ ] All tracks are high quality (320kbps MP3 or WAV)\n",
        "- [ ] Track metadata is accurate\n",
        "- [ ] Album artwork is ready (3000x3000px minimum)\n",
        "- [ ] ISRC codes assigned (DistroKid auto-generates)\n",
        "- [ ] Release dates set (2+ weeks out for pre-saves)\n",
        "- [ ] Social media pre-announcement scheduled\n",
        "- [ ] Playlist pitch prepared for Spotify\n",
        "- [ ] Email list notified\n\n",
        "---\n\n"
    ]

    for genre, items in sorted(by_genre.items()):
        content.append(f"## {genre.upper()} ({len(items)} tracks)\n\n")

        for track, meta in items:
            content.append(f"### {meta['title']}\n")
            content.append(f"- **File:** `{track['filename']}`\n")
            content.append(f"- **Format:** {track['format']} ({track['size_mb']} MB)\n")
            content.append(f"- **Album:** {meta['album']}\n")
            content.append(f"- **Release Date:** {meta['release_date']}\n")
            content.append(f"- **Platforms:** {meta['platforms']}\n")
            content.append(f"- [ ] Uploaded to DistroKid\n")
            content.append(f"- [ ] Artwork attached\n")
            content.append(f"- [ ] Metadata verified\n")
            content.append(f"- [ ] Pre-save link created\n")
            content.append(f"- [ ] Social posts scheduled\n\n")

    content.extend([
        "---\n\n",
        "## 🚀 Marketing Plan (Per Release)\n\n",
        "### 2 Weeks Before Release\n",
        "- [ ] Create pre-save link\n",
        "- [ ] Announce on all social media\n",
        "- [ ] Email list teaser\n",
        "- [ ] Submit to Spotify editorial playlists\n\n",
        "### 1 Week Before Release\n",
        "- [ ] Post snippets on TikTok/Instagram Reels\n",
        "- [ ] Engage with fans in comments\n",
        "- [ ] Prepare release day graphics\n",
        "- [ ] Schedule release day posts\n\n",
        "### Release Day\n",
        "- [ ] Post on all platforms (Instagram, TikTok, Twitter, Facebook)\n",
        "- [ ] Email list announcement\n",
        "- [ ] Submit to user-curated playlists\n",
        "- [ ] Engage with early listeners\n\n",
        "### Post-Release (Ongoing)\n",
        "- [ ] Monitor streaming numbers\n",
        "- [ ] Create visualizers/lyric videos\n",
        "- [ ] Submit to more playlists\n",
        "- [ ] Engage with playlist curators\n",
        "- [ ] Track revenue in dashboard\n\n",
        "---\n\n",
        "## 💰 Revenue Tracking\n\n",
        "Track DistroKid earnings:\n",
        "```bash\n",
        "python3 ~/ai-sites/automation/revenue-dashboard/log_revenue.py \\\n",
        "  distrokid <amount> \"<track_name> streams\"\n",
        "```\n\n",
        "---\n\n",
        "## 📊 Expected Revenue\n\n",
        f"- **Tracks:** {len(tracks)}\n",
        f"- **Per Track (conservative):** $5-20/month after 6 months\n",
        f"- **Total Potential:** ${len(tracks) * 5} - ${len(tracks) * 20}/month\n",
        f"- **Annual Potential:** ${len(tracks) * 5 * 12} - ${len(tracks) * 20 * 12}/year\n\n",
        "*Assumes organic growth, playlist placements, and consistent promotion*\n\n",
        "---\n\n",
        "## 🎯 Playlist Strategy\n\n",
        "### Target Playlists (by genre):\n"
    ])

    for genre in sorted(by_genre.keys()):
        content.append(f"**{genre.title()}:**\n")
        content.append(f"- Search Spotify for \"{genre} independent artists\"\n")
        content.append(f"- Submit to user-curated playlists via SubmitHub\n")
        content.append(f"- Create your own playlist featuring your {genre} tracks\n\n")

    content.extend([
        "---\n\n",
        "**💡 Tip:** Consistency is key. Release regularly and promote each track for maximum impact.\n"
    ])

    output_path.write_text(''.join(content))
    return output_path

def create_marketing_plan(tracks, output_path=None):
    """Create social media marketing plan for releases"""
    if output_path is None:
        output_path = OUTPUT_DIR / f'distrokid_marketing_{datetime.now().strftime("%Y%m%d_%H%M")}.md'

    content = [
        "# DistroKid Release Marketing Plan\n\n",
        "## 📱 Social Media Templates\n\n",
        "### Pre-Save Announcement\n",
        "```\n",
        "🎵 NEW MUSIC ALERT!\n\n",
        "\"[TRACK TITLE]\" drops on [RELEASE DATE]\n\n",
        "Pre-save now:\n",
        "🎧 Spotify: [LINK]\n",
        "🍎 Apple Music: [LINK]\n\n",
        "#NewMusic #ComingSoon #IndieArtist #[GENRE]\n",
        "```\n\n",
        "### Release Day Post\n",
        "```\n",
        "🚀 IT'S HERE!\n\n",
        "\"[TRACK TITLE]\" is now live on all platforms!\n\n",
        "Stream now:\n",
        "🎧 [LINK]\n\n",
        "Let me know what you think in the comments! 💬\n\n",
        "#NewMusicFriday #OutNow #IndieMusic #[GENRE] #StreamingNow\n",
        "```\n\n",
        "### TikTok/Reels Script\n",
        "```\n",
        "[0-3s] Hook: \"I just released this track...\"\n",
        "[3-15s] Play snippet (hook/drop/best part)\n",
        "[15-20s] \"Out now on all platforms!\"\n",
        "[20-30s] Link in bio + CTA\n\n",
        "Text overlay: \"NEW MUSIC 🎵 [TRACK TITLE]\"\n",
        "Hashtags: #newmusic #independentartist #[genre] #musicproducer\n",
        "```\n\n",
        "### Instagram Story Series\n",
        "```\n",
        "Story 1: Countdown graphic \"NEW MUSIC IN 3 DAYS\"\n",
        "Story 2: Behind-the-scenes/creation process\n",
        "Story 3: Snippet with \"Swipe up to pre-save\"\n",
        "Story 4: Release day \"OUT NOW\" + link sticker\n",
        "Story 5: Repost fan reactions\n",
        "```\n\n",
        "---\n\n",
        "## 🎨 Required Assets (Per Release)\n\n",
        "- [ ] Album artwork (3000x3000px)\n",
        "- [ ] Instagram square post (1080x1080px)\n",
        "- [ ] Instagram story template (1080x1920px)\n",
        "- [ ] TikTok/Reels video (9:16)\n",
        "- [ ] YouTube thumbnail (1280x720px)\n",
        "- [ ] Spotify Canvas (9:16 looping video)\n\n",
        "**Generate with:**\n",
        "```bash\n",
        "python3 ~/ai-sites/automation/cross-pollination/music_to_social.py \"[TRACK_TITLE]\"\n",
        "```\n\n",
        "---\n\n",
        "## 📧 Email Template\n\n",
        "**Subject:** 🎵 New Track: [TRACK TITLE] - Out Now!\n\n",
        "```html\n",
        "Hey there!\n\n",
        "I'm excited to share my latest release with you:\n\n",
        "🎵 [TRACK TITLE]\n\n",
        "This [GENRE] track is perfect for [USE CASE].\n\n",
        "Listen now:\n",
        "→ Spotify: [LINK]\n",
        "→ Apple Music: [LINK]\n",
        "→ All Platforms: [LINK]\n\n",
        "If you enjoy it, please:\n",
        "✓ Add it to your playlists\n",
        "✓ Share with friends\n",
        "✓ Leave a comment\n\n",
        "More music coming soon!\n\n",
        "- AvaTarArTs\n",
        "```\n\n",
        "---\n\n",
        "## 🎯 Automation Integration\n\n",
        "Auto-generate marketing for each release:\n",
        "```bash\n",
        "# Generate all social posts\n",
        "python3 ~/ai-sites/automation/cross-pollination/music_to_social.py \"[TRACK]\"\n\n",
        "# Schedule posts\n",
        "python3 ~/ai-sites/automation/scheduler/smart_scheduler.py spotify instagram tiktok\n\n",
        "# Track performance\n",
        "python3 ~/ai-sites/automation/performance/feedback_loop.py --track \\\n",
        "  track_001 music spotify <streams>\n",
        "```\n"
    ]

    output_path.write_text(''.join(content))
    return output_path

if __name__ == '__main__':
    from datetime import timedelta

    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    print(f"🎵 Preparing {limit} tracks for DistroKid distribution...")

    tracks = find_tracks(limit)

    if not tracks:
        print("❌ No tracks found in Music directories")
        sys.exit(1)

    print(f"✅ Found {len(tracks)} tracks\n")

    # Create CSV
    csv_path = create_upload_csv(tracks)
    print(f"📄 Upload CSV: {csv_path}")

    # Create checklist
    checklist_path = create_release_checklist(tracks)
    print(f"📋 Release checklist: {checklist_path}")

    # Create marketing plan
    marketing_path = create_marketing_plan(tracks)
    print(f"📱 Marketing plan: {marketing_path}")

    # Summary
    by_genre = {}
    for track in tracks:
        genre = detect_genre(track['name'])
        by_genre[genre] = by_genre.get(genre, 0) + 1

    print(f"\n📊 Summary:")
    print(f"   Total tracks: {len(tracks)}")
    print(f"   Genres: {', '.join(f'{g}({c})' for g, c in sorted(by_genre.items()))}")
    print(f"   Revenue potential: ${len(tracks) * 5}-${len(tracks) * 20}/month")
    print(f"   Annual potential: ${len(tracks) * 60}-${len(tracks) * 240}/year")
    print(f"\n💡 Next: Review {checklist_path} and start uploading to DistroKid!")
