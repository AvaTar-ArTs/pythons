#!/usr/bin/env python3
import csv, json, os
from pathlib import Path

MUSIC_DIR = Path.home() / 'Music'
SOURCES_CFG = Path(__file__).parent.parent / 'music-sources.json'
SUNO_CSV = None
for p in MUSIC_DIR.rglob('*.csv'):
    if 'suno' in p.name.lower():
        SUNO_CSV = p; break

OUTPUT_DIR = Path(__file__).parent

def scan_mp3_sources(limit=15):
    results = []
    try:
        cfg = json.loads(SOURCES_CFG.read_text()) if SOURCES_CFG.exists() else {}
        dirs = [Path(p) for p in cfg.get('music_sources', [])]
    except Exception:
        dirs = []
    exts = {'.mp3', '.wav', '.flac', '.m4a'}
    for d in dirs:
        if not d.exists():
            continue
        for root, _, files in os.walk(d):
            for f in files:
                if Path(f).suffix.lower() in exts:
                    name = Path(f).stem
                    results.append({'title': name, 'genre': '', 'mood': ''})
                    if len(results) >= limit:
                        return results
    return results

def read_tracks(limit=15):
    # Prefer SUNO CSV when available
    tracks = []
    if SUNO_CSV and SUNO_CSV.exists():
        with open(SUNO_CSV, newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                tracks.append({
                    'title': row.get('title') or row.get('name') or 'Untitled',
                    'genre': row.get('genre') or row.get('style') or '',
                    'mood': row.get('mood') or row.get('tags') or ''
                })
                if len(tracks) >= limit:
                    break
    if len(tracks) < limit:
        tracks += scan_mp3_sources(limit - len(tracks))
    return tracks

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tracks = read_tracks()
    md = ["# Weekly Music Sampler", "", "Preview 15 tracks. License on AudioJungle.", ""]
    for i, t in enumerate(tracks, 1):
        md.append(f"{i}. {t['title']} — {t['genre']} — {t['mood']}")
    (OUTPUT_DIR / 'weekly-music.md').write_text('\n'.join(md))
    (OUTPUT_DIR / 'weekly-music.json').write_text(json.dumps(tracks, indent=2))
    print("✅ Generated weekly sampler")

if __name__ == '__main__':
    main()
