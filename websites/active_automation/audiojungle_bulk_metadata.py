#!/usr/bin/env python3
"""AudioJungle Bulk Metadata Generator - 100+ tracks with SEO"""
import csv, json, sys
from pathlib import Path
from datetime import datetime

MUSIC_DIR = Path.home() / 'Music'
SUNO_DIRS = [
    MUSIC_DIR / 'SUNO',
    MUSIC_DIR / 'nocTurneMeLoDieS',
    MUSIC_DIR / 'mp3-bin'
]
OUTPUT_DIR = Path(__file__).parent / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)

# AudioJungle categories
CATEGORIES = {
    'ambient': ['ambient', 'chill', 'relax', 'meditation'],
    'corporate': ['corporate', 'business', 'presentation', 'upbeat'],
    'cinematic': ['cinematic', 'epic', 'drama', 'orchestral'],
    'electronic': ['electronic', 'techno', 'edm', 'synth'],
    'hip-hop': ['hip', 'hop', 'beat', 'rap'],
    'rock': ['rock', 'guitar', 'indie', 'alternative'],
    'folk': ['folk', 'acoustic', 'country', 'organic']
}

def find_tracks(limit=100):
    """Find music tracks for licensing"""
    tracks = []

    for suno_dir in SUNO_DIRS:
        if not suno_dir.exists():
            continue

        for track_path in suno_dir.rglob('*'):
            if track_path.suffix.lower() in ['.mp3', '.wav', '.flac']:
                tracks.append({
                    'path': str(track_path),
                    'name': track_path.stem,
                    'format': track_path.suffix[1:].upper(),
                    'size_mb': track_path.stat().st_size / 1024 / 1024
                })

                if len(tracks) >= limit:
                    break

        if len(tracks) >= limit:
            break

    return tracks[:limit]

def detect_category(track_name):
    """Detect category from filename"""
    name_lower = track_name.lower()

    for category, keywords in CATEGORIES.items():
        if any(kw in name_lower for kw in keywords):
            return category

    return 'ambient'  # Default

def generate_metadata(track):
    """Generate AudioJungle metadata"""
    name = track['name'].replace('_', ' ').replace('-', ' ')
    words = [w.title() for w in name.split() if len(w) > 2]

    category = detect_category(track['name'])

    title = ' '.join(words[:8])
    description = f"High-quality {category} music track. Perfect for videos, presentations, games, and multimedia projects. Professional production, royalty-free license."

    tags = words[:15] + [category, 'music', 'audio', 'background', 'production']

    return {
        'title': title[:70],
        'description': description[:500],
        'tags': ', '.join(tags[:30]),
        'category': category,
        'mood': 'various',
        'instruments': 'electronic, synth',
        'duration': 'varies',  # Requires audio analysis
        'bpm': '120',  # Default
        'price': '$19'  # Standard tier
    }

def create_upload_csv(tracks, output_path=None):
    """Create CSV for bulk metadata"""
    if output_path is None:
        output_path = OUTPUT_DIR / f'audiojungle_upload_{datetime.now().strftime("%Y%m%d_%H%M")}.csv'

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'file_path', 'title', 'description', 'tags', 'category',
            'mood', 'instruments', 'bpm', 'price'
        ])

        for track in tracks:
            meta = generate_metadata(track)
            writer.writerow([
                track['path'],
                meta['title'],
                meta['description'],
                meta['tags'],
                meta['category'],
                meta['mood'],
                meta['instruments'],
                meta['bpm'],
                meta['price']
            ])

    return output_path

def create_checklist(tracks, output_path=None):
    """Create upload checklist"""
    if output_path is None:
        output_path = OUTPUT_DIR / f'audiojungle_checklist_{datetime.now().strftime("%Y%m%d_%H%M")}.md'

    content = [
        "# AudioJungle Bulk Upload Checklist\n",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
        f"**Total Tracks:** {len(tracks)}\n",
        "---\n"
    ]

    by_category = {}
    for track in tracks:
        meta = generate_metadata(track)
        cat = meta['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append((track, meta))

    for category, items in sorted(by_category.items()):
        content.append(f"\n## {category.title()} ({len(items)} tracks)\n\n")

        for track, meta in items:
            content.append(f"### {meta['title']}\n")
            content.append(f"- **File:** `{Path(track['path']).name}`\n")
            content.append(f"- **Format:** {track['format']} ({track['size_mb']:.1f} MB)\n")
            content.append(f"- **Tags:** {meta['tags']}\n")
            content.append(f"- [ ] Uploaded\n")
            content.append(f"- [ ] Approved\n\n")

    output_path.write_text(''.join(content))
    return output_path

if __name__ == '__main__':
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    print(f"🎵 Finding top {limit} tracks for AudioJungle...")

    tracks = find_tracks(limit)

    if not tracks:
        print("❌ No tracks found")
        sys.exit(1)

    print(f"✅ Found {len(tracks)} tracks\n")

    # Create CSV
    csv_path = create_upload_csv(tracks)
    print(f"📄 CSV created: {csv_path}")

    # Create checklist
    checklist_path = create_checklist(tracks)
    print(f"📋 Checklist created: {checklist_path}")

    # Summary
    print(f"\n📊 Summary:")
    print(f"   Total tracks: {len(tracks)}")
    print(f"   Est. revenue potential: ${len(tracks) * 19 * 5}/month")  # $19 * 5 sales avg
    print(f"   Est. upload time: {len(tracks) * 5} minutes")
    print(f"\n💡 Next: Review {checklist_path} and upload via AudioJungle")
