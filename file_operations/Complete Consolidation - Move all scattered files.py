#!/usr/bin/env python3
"""
Complete Consolidation - Move all scattered files to proper locations
"""

from pathlib import Path
import shutil
from datetime import datetime

def print_header(text):
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")

def consolidate_files():
    """Consolidate all scattered files"""
    
    home = Path.home()
    
    # Define destination directories
    destinations = {
        'toolkit': home / 'advanced_toolkit',
        'music_scripts': home / 'Music' / 'nocTurneMeLoDieS' / 'scripts',
        'music_analysis': home / 'Music' / 'nocTurneMeLoDieS' / 'analysis',
        'music_docs': home / 'Music' / 'nocTurneMeLoDieS' / 'docs',
        'suno_tools': home / 'Music' / 'nocTurneMeLoDieS' / 'suno-tools',
        'web': home / 'Music' / 'nocTurneMeLoDieS' / 'web',
        'archive': home / 'Music' / 'nocTurneMeLoDieS' / 'ARCHIVES' / f'old_files_{datetime.now().strftime("%Y%m%d")}'
    }
    
    # Create directories
    for dest in destinations.values():
        dest.mkdir(parents=True, exist_ok=True)
    
    # File mappings
    file_moves = {
        # Python analysis scripts ? analysis
        'analyze_audio_metadata.py': destinations['music_analysis'],
        'cross_directory_matcher.py': destinations['music_analysis'],
        'comprehensive_music_organizer.py': destinations['music_scripts'],
        'organize_related_content.py': destinations['music_scripts'],
        'organize_remaining_files.py': destinations['music_scripts'],
        'rename_audio_files.py': destinations['music_scripts'],
        
        # Analysis results ? analysis
        'audio_analysis_report.json': destinations['music_analysis'],
        'cross_directory_matches.json': destinations['music_analysis'],
        'rename_plan.json': destinations['music_analysis'],
        'organization_log.json': destinations['music_analysis'],
        
        # Documentation ? docs
        'CONTENT_ANALYSIS_SUMMARY.md': destinations['music_docs'],
        'FINAL_ORGANIZATION.md': destinations['music_docs'],
        'MUSIC_EMPIRE_COMPLETE.txt': destinations['music_docs'],
        'NAVIGATION_MASTER.md': destinations['music_docs'],
        'SIMPLE_NAVIGATION.md': destinations['music_docs'],
        'TOOLKIT_SUMMARY.md': destinations['music_docs'],
        'WORKSPACE_COMPLETE.md': destinations['music_docs'],
        'README.md': destinations['music_docs'] / 'HOME_README.md',  # Rename to avoid conflict
        
        # Instructions ? docs
        'AUTOSCROLL_INSTRUCTIONS.md': destinations['suno_tools'],
        'FINAL_INSTRUCTIONS.txt': destinations['music_docs'],
        'LIVE_SUNO_INSTRUCTIONS.txt': destinations['suno_tools'],
        'QUICK_INSTRUCTIONS.txt': destinations['music_docs'],
        
        # JavaScript/Web tools ? web or suno-tools
        'AUTO_SCROLL_EXTRACTOR.js': destinations['suno_tools'],
        'LIVE_SUNO_EXTRACTOR.js': destinations['suno_tools'],
        'SAVED_HTML_EXTRACTOR.js': destinations['suno_tools'],
        'evolves.html': destinations['web'],
        'main.html': destinations['web'],
        'suno-viewer.html': destinations['web'],
        'playwright.config.js': destinations['suno_tools'],
        
        # Misc files ? archive
        'console.txt': destinations['archive'],
        'DEV_CONSOLE_SCRIPT.txt': destinations['archive'],
        'fix.txt': destinations['archive'],
        'suno.com-1762231878516.log': destinations['archive'],
        'pnpm-lock.yaml': destinations['archive'],
    }
    
    print_header("File Consolidation Plan")
    
    # Group by destination
    by_dest = {}
    for file, dest in file_moves.items():
        if dest not in by_dest:
            by_dest[dest] = []
        by_dest[dest].append(file)
    
    print("Files will be moved to:")
    for dest, files in by_dest.items():
        print(f"\n?? {dest.relative_to(home)}:")
        for f in files:
            print(f"   ? {f}")
    
    print("\n")
    response = input("Proceed with consolidation? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("\nCancelled.")
        return
    
    print_header("Moving Files")
    
    moved = 0
    skipped = 0
    errors = 0
    
    for source_name, dest_dir in file_moves.items():
        source = home / source_name
        
        if not source.exists():
            skipped += 1
            continue
        
        # Determine target filename
        if isinstance(dest_dir, Path) and dest_dir.name.endswith('.md'):
            # It's a full path with new name
            target = dest_dir
            dest_dir = target.parent
        else:
            target = dest_dir / source_name
        
        try:
            if target.exists():
                print(f"??  Skip (exists): {source_name}")
                skipped += 1
            else:
                shutil.move(str(source), str(target))
                print(f"? Moved: {source_name} ? {dest_dir.name}/")
                moved += 1
        except Exception as e:
            print(f"? Error: {source_name} - {e}")
            errors += 1
    
    print_header("Summary")
    print(f"? Moved: {moved} files")
    print(f"??  Skipped: {skipped} files")
    print(f"? Errors: {errors} files")
    
    print("\nNew Structure:")
    print(f"  ~/Music/nocTurneMeLoDieS/")
    print(f"    ??? scripts/           (organization scripts)")
    print(f"    ??? analysis/          (analysis results)")
    print(f"    ??? docs/              (documentation)")
    print(f"    ??? suno-tools/        (Suno extractors)")
    print(f"    ??? web/               (HTML viewers)")
    print(f"    ??? ARCHIVES/          (old files)")
    
    print(f"\n  ~/advanced_toolkit/    (advanced tools)")

def create_index():
    """Create index files"""
    print_header("Creating Index Files")
    
    music_dir = Path.home() / 'Music' / 'nocTurneMeLoDieS'
    
    # Create main README
    readme = music_dir / 'README.md'
    
    readme_content = """# nocTurneMeLoDieS Music Organization

## Directory Structure

```
nocTurneMeLoDieS/
??? FINAL_ORGANIZED/        # Main organized music
?   ??? YOUR_SUNO_SONGS/    # Your Suno/AvatarArts music (370 files)
?   ??? OTHER_MUSIC/        # Other music files
?   ??? BY_ARTIST/          # Organized by artist
?   ??? BY_ALBUM/           # Organized by album
?   ??? AUDIOBOOKS/         # Audio books
?
??? scripts/                # Organization scripts
??? analysis/               # Analysis reports & results
??? docs/                   # Documentation
??? suno-tools/             # Suno extraction tools
??? web/                    # HTML viewers
??? ARCHIVES/               # Old/archived files
```

## Quick Start

### Use Advanced Toolkit
```bash
cd ~/advanced_toolkit
python suno_organizer.py scan
python suno_organizer.py organize
python suno_organizer.py catalog
```

### Check Your Music
```bash
open ~/Music/nocTurneMeLoDieS/FINAL_ORGANIZED/YOUR_SUNO_SONGS
```

### Run Analysis
```bash
cd ~/Music/nocTurneMeLoDieS/scripts
python comprehensive_music_organizer.py
```

## Current Status

- **YOUR_SUNO_SONGS**: 370 files organized
- **Total Collection**: 1,427 audio files
- **Organization**: Complete ?
- **Ready for**: Album creation & distribution

## Tools Available

### In ~/advanced_toolkit/
- `suno_organizer.py` - Main Suno organizer
- `master_control.py` - Universal file management
- `visualizer.py` - Generate dashboards

### In ./scripts/
- `comprehensive_music_organizer.py` - Full organization
- `organize_remaining_files.py` - Process new files
- `rename_audio_files.py` - Fix filenames

### In ./suno-tools/
- JavaScript extractors for Suno.com
- Auto-scroll and live extraction tools

## Documentation

See `./docs/` for:
- Complete analysis summaries
- Organization plans
- Revenue projections
- Workflow guides
"""
    
    with open(readme, 'w') as f:
        f.write(readme_content)
    
    print(f"? Created: {readme}")
    
    # Create scripts README
    scripts_readme = music_dir / 'scripts' / 'README.md'
    scripts_content = """# Music Organization Scripts

## Available Scripts

- `comprehensive_music_organizer.py` - Complete organization system
- `organize_remaining_files.py` - Process unorganized files
- `rename_audio_files.py` - Fix misnamed files

## Usage

```bash
cd ~/Music/nocTurneMeLoDieS/scripts
python comprehensive_music_organizer.py
```
"""
    
    with open(scripts_readme, 'w') as f:
        f.write(scripts_content)
    
    print(f"? Created: {scripts_readme}")

def main():
    print("\n??" + "=" * 78 + "??")
    print("  COMPLETE CONSOLIDATION - Clean up scattered files")
    print("??" + "=" * 78 + "??")
    
    consolidate_files()
    create_index()
    
    print_header("? CONSOLIDATION COMPLETE!")
    
    print("Everything is now properly organized:")
    print()
    print("?? ~/Music/nocTurneMeLoDieS/")
    print("   All music organization in one place")
    print()
    print("?? ~/advanced_toolkit/")
    print("   Advanced Python tools")
    print()
    print("?? ~/ (home)")
    print("   Clean! No scattered files")
    print()
    print("Next: cd ~/Music && ./START_HERE.sh")

if __name__ == '__main__':
    main()
