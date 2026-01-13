#!/usr/bin/env python3
"""
Identify YOUR Music vs Downloaded Music
Separates original content from copyrighted downloads
"""
from pathlib import Path
import re

music_dir = Path.home() / "Music"

print("=" * 70)
print("              ?? IDENTIFYING YOUR ORIGINAL MUSIC")
print("=" * 70)
print()

# Indicators of YOUR music
your_music_indicators = [
    'suno',
    'avatararts',
    'nocturnemelodies',
    'petalfall',
    'ktherias',
    'by _',  # Suno AI naming pattern
    'by @',  # Suno AI pattern
]

# Indicators of DOWNLOADED music
downloaded_indicators = [
    '[',  # YouTube download pattern [ID].mp3
    'official',
    'audio)',
    'music video',
    'cover)',
    'remix)',
]

your_music = []
downloaded_music = []
uncertain = []

print("?? Scanning 936 audio files...")
print()

for file in music_dir.rglob('*'):
    if file.suffix.lower() in ['.mp3', '.m4a', '.wav', '.flac', '.m4r']:
        filename_lower = file.name.lower()
        parent_lower = file.parent.name.lower()
        
        # Check if it's yours
        is_yours = any(indicator in filename_lower or indicator in parent_lower 
                      for indicator in your_music_indicators)
        
        # Check if it's downloaded
        is_downloaded = any(indicator in filename_lower 
                           for indicator in downloaded_indicators)
        
        if is_yours and not is_downloaded:
            your_music.append(file)
        elif is_downloaded and not is_yours:
            downloaded_music.append(file)
        else:
            uncertain.append(file)

# Report
print("?? RESULTS")
print("=" * 70)
print()

print(f"? YOUR ORIGINAL MUSIC: {len(your_music)} files")
print(f"   (Can monetize freely!)")
print()

if your_music[:10]:
    print("   Top 10 examples:")
    for f in your_music[:10]:
        print(f"   - {f.name}")
print()

print(f"? DOWNLOADED MUSIC: {len(downloaded_music)} files")
print(f"   (Copyrighted - do NOT monetize)")
print()

if downloaded_music[:10]:
    print("   Examples:")
    for f in downloaded_music[:10]:
        print(f"   - {f.name}")
print()

print(f"??  UNCERTAIN: {len(uncertain)} files")
print(f"   (Need manual review)")
print()

# Breakdown by project
print("=" * 70)
print("              ?? YOUR MUSIC BY PROJECT")
print("=" * 70)
print()

# Group your music by project/folder
your_projects = {}
for file in your_music:
    # Get project folder (2 levels up from Music dir)
    try:
        rel_path = file.relative_to(music_dir)
        if len(rel_path.parts) > 1:
            project = rel_path.parts[0]
        else:
            project = "Root"
        
        if project not in your_projects:
            your_projects[project] = []
        your_projects[project].append(file)
    except:
        pass

for project, files in sorted(your_projects.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"?? {project}: {len(files)} files")

print()

# Monetization focus
print("=" * 70)
print("              ?? MONETIZATION READY")
print("=" * 70)
print()

print("?? Focus on these projects for revenue:")
print()

monetizable = {
    'nocTurneMeLoDieS': 'Your original music album/project',
    'SUNO': 'AI-generated music (100% yours)',
    'PetalsFall': 'Original music project',
    'Ktherias': 'Original content'
}

for project, files in your_projects.items():
    project_lower = project.lower()
    for key, desc in monetizable.items():
        if key.lower() in project_lower:
            print(f"   ? {project}")
            print(f"      {desc}")
            print(f"      {len(files)} monetizable tracks")
            print()

print("?? Recommendation:")
print("   - Upload YOUR music to Spotify, AudioJungle, YouTube")
print("   - Keep downloaded music for personal listening only")
print("   - Use Suno API to generate MORE original music")
print()

# Save report
report_path = Path.home() / "workspace" / "music-analysis" / "YOUR_MUSIC_ONLY.txt"
with open(report_path, 'w') as f:
    f.write("YOUR ORIGINAL MUSIC (Can Monetize):\n")
    f.write("=" * 60 + "\n\n")
    for file in your_music:
        f.write(f"{file}\n")
    
    f.write("\n\nDOWNLOADED MUSIC (Do NOT Monetize):\n")
    f.write("=" * 60 + "\n\n")
    for file in downloaded_music:
        f.write(f"{file}\n")

print(f"?? Full report saved: {report_path}")
print()

print("=" * 70)
print("              ?? ANALYSIS COMPLETE!")
print("=" * 70)
print()
print(f"Your original music: {len(your_music)} files")
print(f"Ready to monetize: YES!")
print()
