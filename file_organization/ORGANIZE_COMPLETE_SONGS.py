#!/usr/bin/env python3
"""from pathlib import Path
import re
import shutil

from difflib import SequenceMatcher
Organize the 100 complete songs into album folders:
SongName/
??? files/       (audio)
??? prompts/     (transcripts)
??? analysis/    (analysis files)
??? metadata/
"""


NOCTURNE = Path("/Users/steven/Music/nocTurneMeLoDieS")
TRANSCRIPTS = NOCTURNE / "SUNO_CONTENT_FROM_VOLUMES" / "transcripts"
ANALYSIS_DIR = NOCTURNE / "SUNO_CONTENT_FROM_VOLUMES" / "analysis"


def clean_song_name(name):
    """Clean for folder name"""
    name = re.sub(r"-\d{2,4}$", "", name)
    name = re.sub(r"_\d{2,4}$", "", name)
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"\s+", "_", name)
    return name.strip("_")


print("=" * 80)
print("?? ORGANIZE 100 COMPLETE SONGS")
print("=" * 80)
print()

# Get all transcripts
trans_files = list(TRANSCRIPTS.glob("*.txt"))
analysis_files = list(ANALYSIS_DIR.glob("*.txt"))

# Group by song
songs = {}

for trans in trans_files:
    name = trans.stem.replace("_transcript", "").replace("_transcription", "")
    name = clean_song_name(name)

    if name not in songs:
        songs[name] = {"transcripts": [], "analysis": [], "audio": None}
    songs[name]["transcripts"].append(trans)

for anal in analysis_files:
    name = anal.stem.replace("_analysis", "")
    name = clean_song_name(name)

    if name not in songs:
        songs[name] = {"transcripts": [], "analysis": [], "audio": None}
    songs[name]["analysis"].append(anal)

# Find complete songs (have both)
complete = {
    name: data
    for name, data in songs.items()
    if data["transcripts"] and data["analysis"]
}

print(f"? {len(complete)} complete songs")
print()

# Try to find matching audio files
print("?? Finding matching audio files...")
audio_files = []
for ext in ["*.mp3", "*.m4a"]:
    audio_files.extend(NOCTURNE.rglob(ext))

audio_files = [
    f
    for f in audio_files
    if not any(x in str(f) for x in ["/DATA/", "/DOCS/", "/SCRIPTS/", "/SUNO_CONTENT"])
]

for song_name in complete:
    song_clean = clean_song_name(song_name).lower()

    # Try to find audio file
    for audio in audio_files:
        audio_clean = clean_song_name(audio.stem).lower()

        score = SequenceMatcher(None, song_clean, audio_clean).ratio()
        if score > 0.7:
            complete[song_name]["audio"] = audio
            break

matched = sum(1 for s in complete.values() if s["audio"])
print(f"? Matched {matched}/{len(complete)} to audio files")
print()

# Show samples
print("Sample complete bundles:")
for name, data in list(complete.items())[:10]:
    print(f"  ?? {name}")
    print(f"     Audio: {'?' if data['audio'] else '?'}")
    print(f"     Transcripts: {len(data['transcripts'])}")
    print(f"     Analysis: {len(data['analysis'])}")
print()

DRY_RUN = True

if DRY_RUN:
    print("=" * 80)
    print("?? DRY RUN")
    print("=" * 80)
    print()
    print(f"Would create {len(complete)} album folders:")
    print()
    print("  SongName/")
    print("    ??? files/       (audio file)")
    print("    ??? prompts/     (transcript with lyrics)")
    print("    ??? analysis/    (theme/emotion analysis)")
    print("    ??? metadata/    (song info)")
    print()
    print("Set DRY_RUN = False to execute")
    print()
else:
    print("=" * 80)
    print("??  CREATING ALBUM FOLDERS")
    print("=" * 80)
    print()

    created = 0

    for song_name, data in complete.items():
        # Create album folder
        album_dir = NOCTURNE / song_name
        (album_dir / "files").mkdir(parents=True, exist_ok=True)
        (album_dir / "prompts").mkdir(parents=True, exist_ok=True)
        (album_dir / "analysis").mkdir(parents=True, exist_ok=True)
        (album_dir / "metadata").mkdir(parents=True, exist_ok=True)

        # Move audio
        if data["audio"]:
            target = album_dir / "files" / data["audio"].name
            if not target.exists():
                shutil.move(str(data["audio"]), str(target))

        # Copy transcripts to prompts/
        for trans in data["transcripts"]:
            target = album_dir / "prompts" / trans.name
            if not target.exists():
                shutil.copy2(str(trans), str(target))

        # Copy analysis
        for anal in data["analysis"]:
            target = album_dir / "analysis" / anal.name
            if not target.exists():
                shutil.copy2(str(anal), str(target))

        created += 1
        if created % 10 == 0:
            print(f"  Created {created} albums...")

    print()
    print(f"? Created {created} album folders!")
    print()
