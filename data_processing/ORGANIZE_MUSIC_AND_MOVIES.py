#!/usr/bin/env python3
"""
Organize Music and Movies directories
Analyzes structure and organizes loose files
"""

from pathlib import Path
import shutil
from datetime import datetime
from collections import defaultdict

music_dir = Path.home() / "Music"
movies_dir = Path.home() / "Movies"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

print("=" * 100)
print("🎵🎬 ORGANIZING MUSIC AND MOVIES DIRECTORIES")
print("=" * 100)
print()

# Analyze Music directory
print("=" * 100)
print("🎵 MUSIC DIRECTORY ANALYSIS")
print("=" * 100)
print()

music_files = defaultdict(list)
music_folders = []
loose_mp3s = []
loose_other = []

# Scan Music directory
for item in music_dir.iterdir():
    if item.is_file():
        if item.suffix.lower() == ".mp3":
            loose_mp3s.append(item)
        elif item.name.startswith("."):
            continue  # Skip hidden files
        elif item.suffix.lower() in [".py", ".txt", ".md"]:
            loose_other.append(item)
        else:
            loose_other.append(item)
    elif item.is_dir() and not item.name.startswith("."):
        music_folders.append(item)

print(f"Organized folders: {len(music_folders)}")
for folder in music_folders:
    try:
        file_count = sum(1 for _ in folder.rglob("*") if _.is_file())
        size_mb = sum(f.stat().st_size for f in folder.rglob("*") if f.is_file()) / (
            1024 * 1024
        )
        print(f"  📁 {folder.name}: {file_count:,} files, {size_mb:.1f} MB")
    except:
        print(f"  📁 {folder.name}: (error reading)")

print()
print(f"Loose MP3 files in root: {len(loose_mp3s)}")
print(f"Loose other files in root: {len(loose_other)}")
print()

# Analyze Movies directory
print("=" * 100)
print("🎬 MOVIES DIRECTORY ANALYSIS")
print("=" * 100)
print()

movie_folders = []
loose_videos = []
loose_audio = []
loose_images = []
loose_other_movies = []

# Scan Movies directory
for item in movies_dir.iterdir():
    if item.is_file():
        ext = item.suffix.lower()
        if ext in [".mp4", ".mov", ".avi", ".mkv", ".m4v"]:
            loose_videos.append(item)
        elif ext in [".mp3", ".wav", ".m4a", ".aac"]:
            loose_audio.append(item)
        elif ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
            loose_images.append(item)
        elif not item.name.startswith("."):
            loose_other_movies.append(item)
    elif item.is_dir() and not item.name.startswith("."):
        movie_folders.append(item)

print(f"Organized folders: {len(movie_folders)}")
for folder in movie_folders:
    try:
        file_count = sum(1 for _ in folder.rglob("*") if _.is_file())
        size_mb = sum(f.stat().st_size for f in folder.rglob("*") if f.is_file()) / (
            1024 * 1024
        )
        print(f"  📁 {folder.name}: {file_count:,} files, {size_mb:.1f} MB")
    except:
        print(f"  📁 {folder.name}: (error reading)")

print()
print(f"Loose video files: {len(loose_videos)}")
print(f"Loose audio files: {len(loose_audio)}")
print(f"Loose image files: {len(loose_images)}")
print(f"Loose other files: {len(loose_other_movies)}")
print()

# Organization plan
print("=" * 100)
print("📋 ORGANIZATION PLAN")
print("=" * 100)
print()

# Music organization
if loose_mp3s:
    print("🎵 MUSIC:")
    print(f"  - Create 'Loose_MP3s/' folder for {len(loose_mp3s)} loose MP3 files")
    print("  - Move analysis scripts to '_scripts/' folder")
    print()

# Movies organization
if loose_videos or loose_audio or loose_images:
    print("🎬 MOVIES:")
    if loose_videos:
        print(f"  - Create 'Loose_Videos/' folder for {len(loose_videos)} video files")
    if loose_audio:
        print(f"  - Create 'Loose_Audio/' folder for {len(loose_audio)} audio files")
    if loose_images:
        print(f"  - Create 'Loose_Images/' folder for {len(loose_images)} image files")
    if loose_other_movies:
        print(
            f"  - Create 'Loose_Files/' folder for {len(loose_other_movies)} other files"
        )
    print()

# Ask for confirmation
import sys

if "--organize" in sys.argv:
    print("=" * 100)
    print("🔄 ORGANIZING FILES...")
    print("=" * 100)
    print()

    backup_log = Path.home() / "Documents" / f"MUSIC_MOVIES_ORG_LOG_{timestamp}.csv"
    with open(backup_log, "w") as log:
        log.write("original_path,new_path,file_type,moved_at\n")

    moved_count = 0

    # Organize Music
    if loose_mp3s:
        loose_mp3_dir = music_dir / "Loose_MP3s"
        loose_mp3_dir.mkdir(exist_ok=True)
        print(f"📁 Creating {loose_mp3_dir.name}/...")

        for mp3 in loose_mp3s:
            try:
                new_path = loose_mp3_dir / mp3.name
                # Handle conflicts
                counter = 1
                while new_path.exists():
                    stem = mp3.stem
                    suffix = mp3.suffix
                    new_path = loose_mp3_dir / f"{stem}_{counter}{suffix}"
                    counter += 1

                shutil.move(str(mp3), str(new_path))
                with open(backup_log, "a") as log:
                    log.write(f"{mp3},{new_path},mp3,{datetime.now().isoformat()}\n")
                moved_count += 1
            except Exception as e:
                print(f"   ⚠️  Error moving {mp3.name}: {e}")

        print(f"   ✅ Moved {moved_count} MP3 files")
        moved_count = 0

    # Move Music scripts
    if loose_other:
        scripts_dir = music_dir / "_scripts"
        scripts_dir.mkdir(exist_ok=True)
        print(f"📁 Creating {scripts_dir.name}/...")

        for script in loose_other:
            if script.suffix.lower() in [".py", ".txt", ".md"]:
                try:
                    new_path = scripts_dir / script.name
                    if new_path.exists():
                        new_path = (
                            scripts_dir / f"{script.stem}_{timestamp}{script.suffix}"
                        )
                    shutil.move(str(script), str(new_path))
                    with open(backup_log, "a") as log:
                        log.write(
                            f"{script},{new_path},script,{datetime.now().isoformat()}\n"
                        )
                    moved_count += 1
                except Exception as e:
                    print(f"   ⚠️  Error moving {script.name}: {e}")

        if moved_count > 0:
            print(f"   ✅ Moved {moved_count} script files")

    # Organize Movies
    if loose_videos:
        videos_dir = movies_dir / "Loose_Videos"
        videos_dir.mkdir(exist_ok=True)
        print(f"📁 Creating {videos_dir.name}/...")

        for video in loose_videos:
            try:
                new_path = videos_dir / video.name
                counter = 1
                while new_path.exists():
                    stem = video.stem
                    suffix = video.suffix
                    new_path = videos_dir / f"{stem}_{counter}{suffix}"
                    counter += 1

                shutil.move(str(video), str(new_path))
                with open(backup_log, "a") as log:
                    log.write(
                        f"{video},{new_path},video,{datetime.now().isoformat()}\n"
                    )
                moved_count += 1
            except Exception as e:
                print(f"   ⚠️  Error moving {video.name}: {e}")

        print(f"   ✅ Moved {moved_count} video files")
        moved_count = 0

    if loose_audio:
        audio_dir = movies_dir / "Loose_Audio"
        audio_dir.mkdir(exist_ok=True)
        print(f"📁 Creating {audio_dir.name}/...")

        for audio in loose_audio:
            try:
                new_path = audio_dir / audio.name
                counter = 1
                while new_path.exists():
                    stem = audio.stem
                    suffix = audio.suffix
                    new_path = audio_dir / f"{stem}_{counter}{suffix}"
                    counter += 1

                shutil.move(str(audio), str(new_path))
                with open(backup_log, "a") as log:
                    log.write(
                        f"{audio},{new_path},audio,{datetime.now().isoformat()}\n"
                    )
                moved_count += 1
            except Exception as e:
                print(f"   ⚠️  Error moving {audio.name}: {e}")

        print(f"   ✅ Moved {moved_count} audio files")
        moved_count = 0

    if loose_images:
        images_dir = movies_dir / "Loose_Images"
        images_dir.mkdir(exist_ok=True)
        print(f"📁 Creating {images_dir.name}/...")

        for img in loose_images:
            try:
                new_path = images_dir / img.name
                counter = 1
                while new_path.exists():
                    stem = img.stem
                    suffix = img.suffix
                    new_path = images_dir / f"{stem}_{counter}{suffix}"
                    counter += 1

                shutil.move(str(img), str(new_path))
                with open(backup_log, "a") as log:
                    log.write(f"{img},{new_path},image,{datetime.now().isoformat()}\n")
                moved_count += 1
            except Exception as e:
                print(f"   ⚠️  Error moving {img.name}: {e}")

        print(f"   ✅ Moved {moved_count} image files")
        moved_count = 0

    if loose_other_movies:
        other_dir = movies_dir / "Loose_Files"
        other_dir.mkdir(exist_ok=True)
        print(f"📁 Creating {other_dir.name}/...")

        for other in loose_other_movies:
            try:
                new_path = other_dir / other.name
                counter = 1
                while new_path.exists():
                    stem = other.stem
                    suffix = other.suffix
                    new_path = other_dir / f"{stem}_{counter}{suffix}"
                    counter += 1

                shutil.move(str(other), str(new_path))
                with open(backup_log, "a") as log:
                    log.write(
                        f"{other},{new_path},other,{datetime.now().isoformat()}\n"
                    )
                moved_count += 1
            except Exception as e:
                print(f"   ⚠️  Error moving {other.name}: {e}")

        print(f"   ✅ Moved {moved_count} other files")

    print()
    print(f"📄 Backup log: {backup_log.name}")
    print()
    print("=" * 100)
    print("✅ ORGANIZATION COMPLETE")
    print("=" * 100)
else:
    print("💡 Run with --organize to actually organize the files")
    print("   Example: python3 ORGANIZE_MUSIC_AND_MOVIES.py --organize")
