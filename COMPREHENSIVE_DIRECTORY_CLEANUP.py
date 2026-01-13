#!/usr/bin/env python3
"""
🧹 COMPREHENSIVE DIRECTORY CLEANUP
Fix ~/pythons/ at the DIRECTORY level - consolidate, organize, clean
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class DirectoryOrganizer:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)
        self.actions = []

        # Define consolidation rules
        self.consolidation_map = {
            # YouTube/Video projects → AUTOMATION_BOTS/youtube_bots/
            'AUTOMATION_BOTS/youtube_bots': [
                'Auto-YouTube', 'automated-yt-channel', 'AutomatedYoutubeShorts',
                'Automatic-Video-Generator-for-youtube', 'youtube'
            ],

            # Blog/Content automation → content_creation/
            'content_creation/blog_automation': [
                'autoblog', 'autoblog using the ChatGPT'
            ],

            # Transcription tools → audio_transcription/
            'audio_transcription/tools': [
                'AutoTranscribe'
            ],

            # Gallery/HTML tools → MEDIA_PROCESSING/galleries/
            'MEDIA_PROCESSING/galleries': [
                'Auto-html-gallery-scripts', 'simplegallery', 'simplegallery1', 'simplegallery2'
            ],

            # Cloned projects → _cloned_projects/ (for review)
            '_cloned_projects': [
                'ai-comic-factory-main', 'axolotl-main', 'remove-bg-cli',
                'suno-scraper-typescript', 'Twitch-Streamer-GPT-main',
                'TG-MegaBot', 'botty'
            ],

            # Docs → documentation/
            'documentation': [
                'Comprehensive-setup-docs', 'md'
            ],

            # Adobe/Image tools → MEDIA_PROCESSING/image_tools/
            'MEDIA_PROCESSING/image_tools': [
                'Adobe Python Scripts'
            ],

            # Lyrics/Typography → content_creation/
            'content_creation/typography': [
                'AutoTypographyh - lyrics'
            ],

            # Colab notebooks → _notebooks/
            '_notebooks': [
                'colab'
            ]
        }

        # Directories to DELETE (stale cleanup attempts)
        self.to_delete = [
            'clean', 'clean-organizer', 'clean_1 2',
            '_consolidation_logs', '__pycache__'
        ]

        # Directories to KEEP as-is (already organized)
        self.keep = [
            'AI_CONTENT', 'AUTOMATION_BOTS', 'DATA_UTILITIES',
            'MEDIA_PROCESSING', 'audio_generation', 'audio_transcription',
            'audio_video_conversion', 'code_analysis', 'content_creation',
            'data_processing', 'dev_tools', 'documentation',
            'file_organization', 'image_analysis', 'image_generation',
            'social_media', 'streamlit_apps', 'utilities',
            'youtube', 'Instagram-Bot', 'Python', 'Python-organize',
            '_archive', '2T-Xx-python'
        ]

    def analyze_directories(self):
        """Analyze all directories and plan actions"""
        print("🔍 Analyzing ~/pythons/ directories...\n")

        all_dirs = [d for d in self.pythons_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]

        stats = {
            'total': len(all_dirs),
            'keep': 0,
            'consolidate': 0,
            'delete': 0,
            'unknown': 0
        }

        print(f"📂 Found {len(all_dirs)} directories\n")

        for dir_path in sorted(all_dirs):
            dir_name = dir_path.name

            # Check if it's a keeper
            if dir_name in self.keep:
                stats['keep'] += 1
                continue

            # Check if it should be deleted
            if dir_name in self.to_delete:
                self.actions.append({
                    'action': 'delete',
                    'source': dir_path,
                    'target': None,
                    'reason': 'Stale cleanup attempt'
                })
                stats['delete'] += 1
                continue

            # Check if it should be consolidated
            found = False
            for target, sources in self.consolidation_map.items():
                if dir_name in sources:
                    target_path = self.pythons_dir / target
                    self.actions.append({
                        'action': 'move',
                        'source': dir_path,
                        'target': target_path,
                        'reason': f'Consolidate to {target}'
                    })
                    stats['consolidate'] += 1
                    found = True
                    break

            if not found:
                self.actions.append({
                    'action': 'review',
                    'source': dir_path,
                    'target': None,
                    'reason': 'Unknown purpose - needs manual review'
                })
                stats['unknown'] += 1

        return stats

    def print_plan(self, stats):
        """Print the cleanup plan"""
        print("=" * 70)
        print("📋 DIRECTORY CLEANUP PLAN")
        print("=" * 70)
        print(f"Total directories:     {stats['total']}")
        print(f"Keep as-is:            {stats['keep']} ✅")
        print(f"Consolidate/Move:      {stats['consolidate']} 🔄")
        print(f"Delete (stale):        {stats['delete']} 🗑️")
        print(f"Review needed:         {stats['unknown']} ⚠️")
        print("=" * 70 + "\n")

        # Group by action
        by_action = defaultdict(list)
        for action in self.actions:
            by_action[action['action']].append(action)

        # Print moves
        if by_action['move']:
            print("🔄 CONSOLIDATIONS/MOVES:")
            for action in by_action['move']:
                print(f"\n  {action['source'].name}")
                print(f"  → {action['target']}")
                print(f"     Reason: {action['reason']}")

        # Print deletes
        if by_action['delete']:
            print("\n🗑️  DELETIONS (stale cleanup attempts):")
            for action in by_action['delete']:
                print(f"  • {action['source'].name}")
                print(f"     Reason: {action['reason']}")

        # Print reviews
        if by_action['review']:
            print("\n⚠️  NEEDS MANUAL REVIEW:")
            for action in by_action['review']:
                size = sum(f.stat().st_size for f in action['source'].rglob('*') if f.is_file()) / (1024*1024)
                file_count = len(list(action['source'].rglob('*')))
                print(f"  • {action['source'].name} ({size:.1f} MB, {file_count} files)")

    def execute(self, dry_run=True):
        """Execute the cleanup"""
        if dry_run:
            print("\n🔍 DRY RUN - No changes will be made\n")
            return

        print("\n⚠️  EXECUTING CLEANUP\n")

        # Create timestamp for archive
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_dir = self.pythons_dir / '_archive' / f'directory-cleanup-{timestamp}'
        archive_dir.mkdir(parents=True, exist_ok=True)

        stats = {'moved': 0, 'deleted': 0, 'errors': []}

        for action in self.actions:
            if action['action'] == 'review':
                continue  # Skip manual review items

            try:
                if action['action'] == 'move':
                    # Create target directory
                    action['target'].mkdir(parents=True, exist_ok=True)

                    # Move directory
                    final_target = action['target'] / action['source'].name
                    if final_target.exists():
                        print(f"⚠️  Skip (exists): {action['source'].name}")
                        continue

                    shutil.move(str(action['source']), str(final_target))
                    print(f"✅ Moved: {action['source'].name} → {action['target']}")
                    stats['moved'] += 1

                elif action['action'] == 'delete':
                    # Archive before delete
                    archive_path = archive_dir / action['source'].name
                    shutil.move(str(action['source']), str(archive_path))
                    print(f"🗑️  Deleted: {action['source'].name} (archived)")
                    stats['deleted'] += 1

            except Exception as e:
                error_msg = f"{action['source'].name}: {e}"
                stats['errors'].append(error_msg)
                print(f"❌ Error: {error_msg}")

        print("\n" + "=" * 70)
        print("📊 EXECUTION SUMMARY")
        print("=" * 70)
        print(f"Moved:     {stats['moved']}")
        print(f"Deleted:   {stats['deleted']}")
        print(f"Errors:    {len(stats['errors'])}")
        print("=" * 70)

        if not dry_run:
            print(f"\n📦 Archive: {archive_dir}")

    def organize_root_files(self):
        """Organize the 77 loose Python files in root"""
        print("\n" + "=" * 70)
        print("📝 ORGANIZING ROOT FILES")
        print("=" * 70)

        root_files = [f for f in self.pythons_dir.glob('*.py') if f.is_file()]
        print(f"\nFound {len(root_files)} Python files in root")

        # Simple categorization
        categories = defaultdict(list)

        for f in root_files:
            name = f.name.lower()

            # Skip our new scripts
            if name.startswith('deep_') or name.startswith('intelligent_') or \
               name.startswith('smart_') or name.startswith('cleanup_') or \
               name.startswith('comprehensive_'):
                continue

            # Categorize
            if 'analyze' in name or 'analyzer' in name:
                categories['DATA_UTILITIES/data_analyzers'].append(f)
            elif 'audio' in name or 'transcribe' in name or 'tts' in name:
                categories['audio_generation'].append(f)
            elif 'api' in name or 'client' in name:
                categories['utilities'].append(f)
            elif 'bot' in name or 'automat' in name:
                categories['AUTOMATION_BOTS'].append(f)
            elif 'business' in name or 'discovery' in name:
                categories['utilities'].append(f)
            else:
                categories['utilities'].append(f)

        print(f"\nCategorization:")
        for cat, files in sorted(categories.items()):
            print(f"  {cat}: {len(files)} files")

        return categories


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║        🧹 COMPREHENSIVE DIRECTORY CLEANUP                         ║
║        Fix ~/pythons/ at the DIRECTORY level                     ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    organizer = DirectoryOrganizer()

    # Analyze
    stats = organizer.analyze_directories()

    # Print plan
    organizer.print_plan(stats)

    # Analyze root files
    categories = organizer.organize_root_files()

    print("\n" + "=" * 70)
    print("🎯 EXPECTED RESULT")
    print("=" * 70)
    print(f"BEFORE:  131 directories + 77 root files (MESS!)")
    print(f"AFTER:   ~30 clean directories + ~10 root files")
    print(f"         Everything organized and consolidated!")
    print("=" * 70)

    # Ask to execute
    import sys
    if '--execute' in sys.argv:
        confirm = input("\nType 'CLEANUP' to execute: ")
        if confirm == 'CLEANUP':
            organizer.execute(dry_run=False)
        else:
            print("❌ Cancelled")
    else:
        print("\n🎯 To execute:")
        print("   python3 COMPREHENSIVE_DIRECTORY_CLEANUP.py --execute")


if __name__ == "__main__":
    main()

