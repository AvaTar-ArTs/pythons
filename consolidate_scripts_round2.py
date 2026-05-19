#!/usr/bin/env python3
"""
Round 2: Consolidate remaining Python scripts from root.

Adds patterns missed in first consolidation:
- focused_*, final_*, simple_* variants
- More verification scripts
- More backup scripts
- Data/analysis scripts

Usage: python consolidate_scripts_round2.py [--dry-run] [--apply]
"""

import shutil
from pathlib import Path

PROJECT = Path(__file__).parent
SCRIPTS_DIR = PROJECT / "scripts"

# Additional scripts to categorize (missed in round 1)
ADDITIONAL_SCRIPT_CATEGORIES = {
    "organization": [
        "album_organization_clean.py",
        "album_organization_final.py",
        "album_organization_fixed.py",
        "album_based_organization_fixed.py",
        "focused_album_organization.py",
        "simple_music_organizer_fixed.py",
        "final_album_organization.py",
        "focused_music_analyzer.py",
        "analyze_and_move_music_images_from_pictures.py",
        "move_music_images_from_pictures_final.py",
        "fix_loose_and_emoji.py",
        "fix_nonascii_albums.py",
        "fix_untitled_uuid_folders.py",
        "rename_unmapped_to_titles.py",
        "move_unmapped_to_albums.py",
        "rename_downloads_uuid_to_title.py",
        "integrate_downloads_into_albums.py",
        "compare_downloads_with_albums.py",
        "remove_duplicate_mp3s.py",
        "parse_and_rename_uuids.py",
        "rename_files_using_csv_metadata_final.py",
        "rename_files_using_csv_metadata.py",
        "rename_files_to_match_dir.py",
        "organized_uuid_renamer.py",
        "album_organization_clean.py",
        "album_organization_final.py",
        "album_organization_fixed.py",
        "album_based_organization_fixed.py",
        "simple_music_organizer_fixed.py",
        "simple_music_organizer.py",
        "focused_album_organization.py",
        "focused_music_analyzer.py",
        "focused_music_organization.py",
        "focused_organization_fixer.py",
        "fix_loose_and_emoji.py",
        "fix_nonascii_albums.py",
        "fix_untitled_uuid_folders.py",
        "rename_unmapped_to_titles.py",
        "move_unmapped_to_albums.py",
        "rename_downloads_uuid_to_title.py",
        "integrate_downloads_into_albums.py",
        "compare_downloads_with_albums.py",
        "remove_duplicate_mp3s.py",
        "parse_and_rename_uuids.py",
        "rename_files_using_csv_metadata_final.py",
        "rename_files_using_csv_metadata.py",
        "rename_files_to_match_dir.py",
        "album_organization_clean.py",
        "album_organization_final.py",
        "album_organization_fixed.py",
        "album_based_organization_fixed.py",
        "simple_music_organizer_fixed.py",
        "simple_music_organizer.py",
        "focused_album_organization.py",
        "focused_music_analyzer.py",
        "focused_music_organization.py",
        "focused_organization_fixer.py",
        "fix_loose_and_emoji.py",
        "fix_nonascii_albums.py",
        "fix_untitled_uuid_folders.py",
        "rename_unmapped_to_titles.py",
        "move_unmapped_to_albums.py",
        "rename_downloads_uuid_to_title.py",
        "integrate_downloads_into_albums.py",
        "compare_downloads_with_albums.py",
        "remove_duplicate_mp3s.py",
        "parse_and_rename_uuids.py",
        "rename_files_using_csv_metadata_final.py",
        "rename_files_using_csv_metadata.py",
        "rename_files_to_match_dir.py",
    ],
    "verification": [
        "verify_final_organization.py",
        "verify_title_organization_final.py",
        "verify_title_organization_final_fixed.py",
        "verify_title_organization_fixed.py",
        "verify_title_organization.py",
        "verify_consolidation_state.py",
        "final_verification_save.py",
        "final_verification_completion.py",
        "final_verification_and_save.py",
        "final_verification_and_completion.py",
        "compare_mp3s_to_csv.py",
        "create_duplicate_report.py",
        "create_comprehensive_inventory.py",
    ],
    "backup": [
        "save_final_organization_work.py",
        "final_preservation_backup.py",
        "content_preservation_backup.py",
        "preserve_organization_work.py",
        "nocturnemelodies_backup_manager.py",
        "test_backup_script.py",
        "archive_project_state.py",
        "final_archive_original_html.py",
        "archive_original_html_final.py",
        "create_preservation_package.py",
        "create_final_project_archive.py",
    ],
    "data": [
        "download_suno_exports.py",
        "apply_knowledge_enhancements.py",
        "analyze_duplicate_consolidation.py",
        "debug_uuid_renamer.py",
        "dry_run_with_deduplication.py",
        "dry_run_consolidation_analysis.py",
    ],
    "specialized": [
        "convert_html_mobile.py",
        "create_avatararts_website.py",
        "create_avatararts_website_final.py",
        "sync_collections_final.py",
        "move_external_volume_music.py",
        "move_external_volume_music_optimized.py",
        "final_mp3_rename_from_csv.py",
        "organize_zip_folder.py",
        "organize_zip_folder_fixed.py",
        "comprehensive_review.py",
        "test_uuid_matching.py",
        "analyze_cursor_chats.py",
        "sync_icloud_collection_auto.py",
        "sync_icloud_collection.py",
        "restore_icloud_collection.py",
        "create_icloud_backup_mapping.py",
    ],
}


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Round 2: Consolidate remaining scripts")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be moved")
    parser.add_argument("--apply", action="store_true", help="Execute the consolidation")
    args = parser.parse_args()

    if not (args.dry_run or args.apply):
        print("Use --dry-run or --apply")
        return

    print("Round 2: Remaining Scripts Consolidation")
    print("=" * 50)

    moved = 0
    for category, scripts in ADDITIONAL_SCRIPT_CATEGORIES.items():
        category_dir = SCRIPTS_DIR / category
        if category == "specialized":
            # Specialized scripts go in their own subdir
            category_dir = SCRIPTS_DIR / "specialized"

        print(f"\n{category.upper()}:")
        print(f"  Scripts: {len(scripts)}")
        print(f"  Target: scripts/{category_dir.name}/")

        if args.apply:
            category_dir.mkdir(parents=True, exist_ok=True)

        # Move scripts
        for script in scripts:
            src = PROJECT / script
            if not src.exists():
                continue

            dst = category_dir / script

            if args.dry_run:
                print(f"    [move] {script} → scripts/{category_dir.name}/")
            else:
                shutil.move(str(src), str(dst))
                print(f"    Moved {script} → scripts/{category_dir.name}/")
                moved += 1

    print("\nSummary:")
    print(f"  Scripts moved: {moved}")
    print("  Note: Specialized scripts moved to scripts/specialized/")


if __name__ == "__main__":
    main()
