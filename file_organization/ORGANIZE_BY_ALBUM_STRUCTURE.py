#!/usr/bin/env python3
"""from pathlib import Path
import re
import shutil

from mutagen import File as MutagenFile
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
Organize nocTurneMeLoDieS by album with subdirectories
Structure: albumname/files/, albumname/prompts/, etc.
"""


NOCTURNE = Path("/Users/steven/Music/nocTurneMeLoDieS")
DRY_RUN = False


def sanitize_name(name):
    """Clean name for folder"""
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    name = re.sub(r"\s+", "_", name)
    return name.strip("._")


print("=" * 80)
print("?? ORGANIZE BY ALBUM WITH SUBDIRECTORIES")
print("=" * 80)
print()

# Scan all audio files
print("Scanning audio files...")
audio_files = []
for ext in ["*.mp3", "*.m4a", "*.wav"]:
    audio_files.extend(NOCTURNE.rglob(ext))

print(f"Found {len(audio_files)} audio files")
print()

# Group by album
albums = {}
no_album = []

print("Reading metadata and grouping by album...")
for audio_file in audio_files:  # Process ALL files
    try:
        audio = MP3(audio_file, ID3=EasyID3)
        album = audio.get("album", [None])[0]
        artist = audio.get("artist", [None])[0]
    except:
        try:
            audio = MutagenFile(audio_file, easy=True)
            album = (
                audio.get("album", [None])[0] if audio and audio.get("album") else None
            )
            artist = (
                audio.get("artist", [None])[0]
                if audio and audio.get("artist")
                else None
            )
        except:
            album = None
            artist = None

    if album and album not in ["Bin", "Trashycd", "Unknown"]:
        album_clean = sanitize_name(album)
        if album_clean not in albums:
            albums[album_clean] = {
                "original_name": album,
                "files": [],
                "artist": artist,
            }
        albums[album_clean]["files"].append(audio_file)
    else:
        no_album.append(audio_file)

print(f"Found {len(albums)} albums")
print(f"Found {len(no_album)} files without album")
print()

print("=" * 80)
print("?? ALBUMS (sample):")
print("-" * 80)
for i, (album_key, data) in enumerate(sorted(albums.items())[:15]):
    print(f"{data['original_name']:50s} {len(data['files'])} files")

print()
print("=" * 80)
print("?? PROPOSED STRUCTURE")
print("=" * 80)
print()
print("nocTurneMeLoDieS/")
for album_key in sorted(albums.keys())[:5]:
    album_data = albums[album_key]
    print(f"  ??? {album_key}/")
    print(f"  ?   ??? files/           ({len(album_data['files'])} audio files)")
    print("  ?   ??? prompts/         (lyrics, Suno prompts)")
    print("  ?   ??? images/          (album art)")
    print("  ?   ??? metadata/        (CSVs, info)")
print(f"  ... and {len(albums) - 5} more albums")
print()
print("  ??? Uncategorized/")
print(f"  ?   ??? files/           ({len(no_album)} files)")
print()
print("  ??? _DATA/               (all CSVs, scripts)")
print("  ??? _DOCS/               (documentation)")
print("  ??? _ARCHIVES/           (old structures)")
print()

if DRY_RUN:
    print("=" * 80)
    print("?? DRY RUN")
    print("=" * 80)
    print()
    print("This will create album folders with subdirectories:")
    print("  ? files/     - audio files")
    print("  ? prompts/   - lyrics, Suno prompts")
    print("  ? images/    - album art")
    print("  ? metadata/  - info files")
    print()
    print("Set DRY_RUN = False to execute")
    print()
else:
    print("=" * 80)
    print("??  EXECUTING ORGANIZATION")
    print("=" * 80)
    print()

    moved = 0

    # Create album structures
    for album_key, album_data in albums.items():
        album_dir = NOCTURNE / album_key

        # Create subdirectories
        (album_dir / "files").mkdir(parents=True, exist_ok=True)
        (album_dir / "prompts").mkdir(parents=True, exist_ok=True)
        (album_dir / "images").mkdir(parents=True, exist_ok=True)
        (album_dir / "metadata").mkdir(parents=True, exist_ok=True)

        # Move audio files to files/
        for audio_file in album_data["files"]:
            target = album_dir / "files" / audio_file.name
            if not target.exists():
                try:
                    shutil.move(str(audio_file), str(target))
                    moved += 1
                    if moved % 50 == 0:
                        print(f"  Moved {moved} files...")
                except Exception as e:
                    print(f"  Error: {audio_file.name}: {e}")

        # Create README
        readme = album_dir / "README.md"
        readme.write_text(
            f"""# {album_data['original_name']}

**Artist:** {album_data['artist'] or 'Steven Chaplinski'}  
**Tracks:** {len(album_data['files'])}

## Structure

- `files/` - Audio files ({len(album_data['files'])} tracks)
- `prompts/` - Suno prompts and lyrics
- `images/` - Album artwork
- `metadata/` - Additional metadata and info
""",
        )

    # Handle uncategorized
    if no_album:
        uncat_dir = NOCTURNE / "Uncategorized"
        (uncat_dir / "files").mkdir(parents=True, exist_ok=True)

        for audio_file in no_album:
            target = uncat_dir / "files" / audio_file.name
            if not target.exists():
                try:
                    shutil.move(str(audio_file), str(target))
                    moved += 1
                except Exception as e:
                    print(f"  Error: {audio_file.name}: {e}")

    print()
    print("=" * 80)
    print("? ORGANIZATION COMPLETE!")
    print("=" * 80)
    print()
    print(f"Organized {moved} files")
    print(f"Created {len(albums)} album folders")
    print()
    print("Each album now has:")
    print("  ? files/     - audio files")
    print("  ? prompts/   - ready for lyrics/prompts")
    print("  ? images/    - ready for artwork")
    print("  ? metadata/  - ready for info")
    print()
