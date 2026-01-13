#!/usr/bin/env python3
"""
Auto-Categorize Root Scripts
Automatically categorizes and moves root-level Python scripts to appropriate directories.

Usage:
    python categorize_root_scripts.py [--dry-run] [--execute]
"""

import argparse
import shutil
from pathlib import Path
from collections import defaultdict

# Mapping of keywords to target directories
CATEGORY_MAPPING = {
    'organize': 'file_organization',
    'cleanup': 'file_organization',
    'dedup': 'file_organization',
    'duplicate': 'file_organization',
    'remove': 'file_organization',
    'merge': 'file_organization',
    'sort': 'file_organization',
    'analyze': 'code_analysis',
    'analyzer': 'code_analysis',
    'scanner': 'code_analysis',
    'csv': 'DATA_UTILITIES',
    'json': 'DATA_UTILITIES',
    'data': 'DATA_UTILITIES',
    'audio': 'audio_generation',
    'music': 'audio_generation',
    'video': 'MEDIA_PROCESSING',
    'image': 'MEDIA_PROCESSING',
    'media': 'MEDIA_PROCESSING',
    'transcription': 'audio_transcription',
    'transcribe': 'audio_transcription',
    'whisper': 'audio_transcription',
    'tts': 'audio_generation',
    'text_to_speech': 'audio_generation',
    'ai': 'AI_CONTENT',
    'gpt': 'AI_CONTENT',
    'claude': 'AI_CONTENT',
    'llm': 'AI_CONTENT',
    'openai': 'AI_CONTENT',
    'anthropic': 'AI_CONTENT',
    'content': 'content_creation',
    'seo': 'AEO_SEO_Content_Optimization',
    'bot': 'AUTOMATION_BOTS',
    'automation': 'AUTOMATION_BOTS',
    'instagram': 'AUTOMATION_BOTS',
    'youtube': 'AUTOMATION_BOTS',
    'reddit': 'AUTOMATION_BOTS',
    'utility': 'utilities',
    'util': 'utilities',
    'helper': 'utilities',
    'convert': 'audio_video_conversion',
    'download': 'utilities',
    'upload': 'utilities',
}

# Scripts to keep in root (essential scripts)
KEEP_IN_ROOT = {
    'categorize_root_scripts.py',
    'cli.py',
    'main.py',
    '__init__.py',
}


def categorize_script(script_path, dry_run=True):
    """
    Categorize a script based on its name.
    Returns (category, should_move)
    """
    name_lower = script_path.name.lower()

    # Check if should be kept in root
    if script_path.name in KEEP_IN_ROOT:
        return None, False

    # Find matching category
    for keyword, category in CATEGORY_MAPPING.items():
        if keyword in name_lower:
            return category, True

    # Default to utilities if no match
    return 'utilities', True


def main():
    parser = argparse.ArgumentParser(
        description='Categorize and move root-level Python scripts'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        default=True,
        help='Preview changes without moving files (default: True)'
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Actually move files (overrides --dry-run)'
    )
    parser.add_argument(
        '--root',
        type=str,
        default='/Users/steven/pythons',
        help='Root directory to process (default: /Users/steven/pythons)'
    )

    args = parser.parse_args()
    dry_run = not args.execute

    root_path = Path(args.root)
    if not root_path.exists():
        print(f"Error: Root directory {root_path} does not exist")
        return 1

    # Collect all Python scripts in root
    root_scripts = [f for f in root_path.glob('*.py') if f.is_file()]

    if not root_scripts:
        print(f"No Python scripts found in {root_path}")
        return 0

    print(f"Found {len(root_scripts)} Python scripts in root directory\n")

    # Categorize scripts
    categorized = defaultdict(list)
    kept_in_root = []

    for script in root_scripts:
        category, should_move = categorize_script(script)
        if should_move and category:
            categorized[category].append(script)
        else:
            kept_in_root.append(script)

    # Display results
    print("=" * 60)
    print("CATEGORIZATION PLAN")
    print("=" * 60)

    total_to_move = 0
    for category, scripts in sorted(categorized.items()):
        print(f"\n{category}/ ({len(scripts)} scripts):")
        for script in sorted(scripts):
            print(f"  → {script.name}")
            total_to_move += 1

    if kept_in_root:
        print(f"\nKept in root ({len(kept_in_root)} scripts):")
        for script in sorted(kept_in_root):
            print(f"  • {script.name}")

    print("\n" + "=" * 60)
    print(f"Summary: {total_to_move} scripts to move, {len(kept_in_root)} to keep in root")
    print("=" * 60)

    if dry_run:
        print("\n[DRY RUN] No files were moved. Use --execute to actually move files.")
        return 0

    # Execute moves
    print("\nExecuting moves...")
    moved = 0
    errors = 0

    for category, scripts in categorized.items():
        target_dir = root_path / category
        target_dir.mkdir(parents=True, exist_ok=True)

        for script in scripts:
            try:
                target_path = target_dir / script.name
                if target_path.exists():
                    print(f"  ⚠️  Skipping {script.name} (already exists in {category}/)")
                    errors += 1
                else:
                    shutil.move(str(script), str(target_path))
                    print(f"  ✓ Moved {script.name} → {category}/")
                    moved += 1
            except Exception as e:
                print(f"  ✗ Error moving {script.name}: {e}")
                errors += 1

    print(f"\n✓ Moved {moved} scripts")
    if errors > 0:
        print(f"⚠️  {errors} errors encountered")

    return 0


if __name__ == '__main__':
    exit(main())

