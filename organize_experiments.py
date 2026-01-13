#!/usr/bin/env python3
"""
Organize Experiments Directory
Apply intelligent categorization to experiments/ contents
"""

import shutil
from pathlib import Path


class ExperimentsOrganizer:
    """Organize experiments directory with intelligent categorization"""

    def __init__(self, experiments_dir: Path):
        self.experiments_dir = experiments_dir

        # Intelligent categorization map
        self.category_map = {
            # Test files → testing/
            'testing/bot_tests': [
                'test_bot_comment.py', 'test_bot_follow.py', 'test_bot_get.py',
                'test_bot_like.py', 'test_bot_support.py', 'test_bot_unlike.py',
                'test_bot.py', 'test_automation.py'
            ],
            'testing/gallery_tests': [
                'test_gallery_build.py', 'test_gallery_init.py', 'test_gallery_logic.py',
                'test_gallery_upload.py', 'test_google_gallery_logic.py',
                'test_onedrive_gallery_logic.py', 'test_file_gallery_logic.py'
            ],
            'testing/uploader_tests': [
                'test_aws_uploader.py', 'test_netlify_uploader.py',
                'test_uploader_factory.py'
            ],
            'testing/misc_tests': [
                'test_savify.py', 'test.py', 'testing2.py', 'testing3.py',
                'isatty_test.py', 'initialise_test.py'
            ],

            # Gallery/Media tools → media_tools/
            'media_tools/gallery': [
                'gallery_init_20241204123258.py', 'gallery_init_20241204123453.py',
                'parse_vid.py'
            ],
            'media_tools/video': [
                'download_vid.py', 'gen_vid.py', 'convert_file.py'
            ],
            'media_tools/image': [
                'image.py', 'logo.py'
            ],

            # Paste/Clipboard tools → clipboard_tools/
            'clipboard_tools': [
                'diagnose_paste_blob.py', 'extract_paste_history.py',
                'split_paste_history.py', 'try_compression_formats.py'
            ],

            # Agent/AI tools → ai_agents/
            'ai_agents': [
                'chatgpt_agent.py', 'setup_agent.py', 'test_agent.py'
            ],

            # Download tools → download_tools/
            'download_tools': [
                'download_json.py', 'fetch_file.py', 'leodown_20250102105149.py'
            ],

            # Utility/Helper → utilities/
            'utilities': [
                'colors.py', 'console.py', 'credentials.py', 'debug.py',
                'docs.py', 'playwright.py', 'processor_cli.py', 'log_file.py'
            ],

            # Backup/Old files → old_versions/
            'old_versions': [
                'bak.py', 'main_20221230223427.py'
            ],

            # Keep reorganization tools in existing folder
            # (they're already in reorganization_tools, but some are loose)
            'reorganization_tools': [
                'adaptive_content_analyzer.py', 'adaptive_recategorizer.py',
                'context_fluid_organizer.py', 'next_gen_content_analyzer.py',
                'ultimate_content_organizer.py', 'intelligent_script_reorganizer.py',
                'execute_context_fluid_reorganization.py',
                'execute_improved_reorganization.py', 'execute_reorganization.py',
                'execute_script_reorganization.py', 'execute_ultimate_reorganization.py'
            ]
        }

    def execute(self, dry_run=True):
        """Execute experiments organization"""

        print("=" * 70)
        print(f"🧪 ORGANIZE EXPERIMENTS {'(DRY RUN)' if dry_run else '(LIVE)'}")
        print("=" * 70)
        print()

        moved_count = 0
        error_count = 0
        already_organized = 0

        # Process each category
        for category, files in sorted(self.category_map.items()):
            target_dir = self.experiments_dir / category
            files_to_move = []

            # Check which files exist and need moving
            for filename in files:
                source = self.experiments_dir / filename
                if source.exists() and source.is_file():
                    # Skip if already in correct location
                    if source.parent != target_dir:
                        files_to_move.append(filename)
                    else:
                        already_organized += 1

            if not files_to_move:
                continue

            print(f"📂 {category}/")

            if not dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)

            for filename in files_to_move:
                source = self.experiments_dir / filename
                target = target_dir / filename

                if dry_run:
                    print(f"   [DRY RUN] {filename}")
                else:
                    try:
                        # Handle conflicts
                        if target.exists():
                            from datetime import datetime
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            new_name = f"{source.stem}_{timestamp}{source.suffix}"
                            target = target_dir / new_name

                        shutil.move(str(source), str(target))
                        print(f"   ✅ {filename}")
                        moved_count += 1
                    except Exception as e:
                        print(f"   ❌ {filename} - ERROR: {str(e)[:40]}")
                        error_count += 1

            print()

        print("=" * 70)
        print(f"{'Simulation' if dry_run else 'Organization'} complete!")
        print(f"   Files {'would be' if dry_run else ''} moved: {moved_count}")
        if already_organized > 0:
            print(f"   Already organized: {already_organized}")
        if error_count > 0:
            print(f"   Errors: {error_count}")
        print("=" * 70)

        if not dry_run:
            print()
            print("✨ Experiments directory organized!")
            print()
            print("📊 New structure:")
            print("   experiments/")
            print("   ├── ai_agents/           AI agent scripts")
            print("   ├── clipboard_tools/     Paste/clipboard utilities")
            print("   ├── download_tools/      Download utilities")
            print("   ├── media_tools/         Gallery, video, image tools")
            print("   ├── reorganization_tools/ Organization scripts")
            print("   ├── testing/             All test files")
            print("   ├── utilities/           Helper scripts")
            print("   ├── old_versions/        Backup/old files")
            print("   ├── analysis_artifacts/  Analysis outputs")
            print("   ├── setup_tools/         Setup scripts")
            print("   ├── test_data/           Test data")
            print("   └── archived_items/      Archived experimental items")
            print()

        if dry_run:
            print("\n💡 To execute, run:")
            print("   python3 organize_experiments.py --execute")

def main():
    import sys

    base_dir = Path("/Users/steven/Documents/python")
    experiments_dir = base_dir / "experiments"

    dry_run = '--execute' not in sys.argv

    organizer = ExperimentsOrganizer(experiments_dir)
    organizer.execute(dry_run=dry_run)

if __name__ == '__main__':
    main()
