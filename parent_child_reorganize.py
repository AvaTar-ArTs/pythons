#!/usr/bin/env python3
"""
Reorganize for better parent-child awareness.

Current issue: Scripts organized by type (organization, consolidation) but
should be organized by feature/workflow to keep related scripts together.

New structure:
- scripts/core/ — Main workflows (organize, consolidate, transcribe)
- scripts/uuid/ — All UUID-related scripts
- scripts/album/ — Album-specific operations
- scripts/data/ — Data processing and mapping
- scripts/web/ — Web-related scripts
- scripts/backup/ — All backup/preservation scripts
- scripts/specialized/ — One-off utilities

This keeps parent-child relationships: scripts that work together stay together.
"""

import shutil
from pathlib import Path

PROJECT = Path(__file__).parent
SCRIPTS_DIR = PROJECT / "scripts"

# Feature-based organization (better parent-child awareness)
FEATURE_MAPPING = {
    # Core workflows
    "core": [
        "organize_albums.py",
        "consolidate_song_variations.py",
        "transcribe_unmapped.py",
        "transcribe_albums_missing.py",
    ],
    # UUID handling (all related scripts together)
    "uuid": [
        "fix_untitled_uuid_folders.py",
        "rename_unmapped_to_titles.py",
        "move_unmapped_to_albums.py",
        "rename_downloads_uuid_to_title.py",
        "organized_uuid_renamer.py",
        "parse_and_rename_uuids.py",
        "focused_uuid_renamer.py",
        "accurate_uuid_renamer.py",
        "precise_uuid_renamer.py",
        "final_uuid_renamer.py",
        "debug_uuid_renamer.py",
    ],
    # Album operations
    "album": [
        "album_organization_clean.py",
        "album_organization_final.py",
        "album_organization_fixed.py",
        "album_based_organization_fixed.py",
        "album_based_organization.py",
        "focused_album_organization.py",
        "final_album_organization.py",
        "simple_album_organizer_fixed.py",
        "simple_album_organizer.py",
        "fixed_album_organizer.py",
        "implement_album_organization.py",
        "simple_music_organizer_fixed.py",
        "simple_music_organizer.py",
        "focused_music_organization.py",
        "focused_organization_fixer.py",
        "consolidate_nested_albums.py",
        "specific_organization_fixes.py",
        "final_cleanup_and_organization.py",
    ],
    # Data processing
    "data": [
        "csv_song_mapping.py",
        "build_song_variations_map.py",
        "download_suno_exports.py",
        "apply_knowledge_enhancements.py",
        "enhanced_collection_organizer.py",
        "knowledge_manager.py",
        "nocturnemelodies_knowledge_manager.py",
        "analyze_duplicate_consolidation.py",
        "dry_run_with_deduplication.py",
        "remove_duplicate_mp3s.py",
        "create_duplicate_report.py",
        "create_comprehensive_inventory.py",
        "compare_mp3s_to_csv.py",
        "mp3_similarity_analyzer.py",
        "music_content_analysis.py",  # if exists
    ],
    # Image/music file handling
    "media": [
        "analyze_and_move_music_images_from_pictures.py",
        "move_music_images_from_pictures_final.py",
        "analyze_cursor_chats.py",
        "compare_downloads_with_albums.py",
        "integrate_downloads_into_albums.py",
        "move_external_volume_music.py",
        "move_external_volume_music_optimized.py",
        "move_volume_music_to_albums.py",
        "sync_collections_final.py",
        "sync_collections.py",
    ],
    # Web/HTML processing
    "web": [
        "convert_html_mobile.py",
        "create_avatararts_website.py",
        "create_avatararts_website_final.py",
        "create_nocturnemelodies_web_structure.py",
        "create_nocturnemelodies_v2.py",
        "create_nocturnemelodies_v3.py",
        "create_final_nocturnemelodies_organization.py",
    ],
    # Backup and preservation
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
        "final_preservation_summary.py",
        "final_preservation_script.py",
        "create_preservation_backup.py",
        "backup_nocturnemelodies_organization.py",
        "create_comprehensive_backup.py",
        "nocturnemelodies_collection_backup.py",
        "create_music_collection_backup.py",
    ],
    # Verification and reporting
    "verify": [
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
    # Specialized/one-off
    "specialized": [
        "fix_loose_and_emoji.py",
        "fix_nonascii_albums.py",
        "rename_files_using_csv_metadata_final.py",
        "rename_files_using_csv_metadata.py",
        "rename_files_to_match_dir.py",
        "final_mp3_rename_from_csv.py",
        "organize_zip_folder.py",
        "organize_zip_folder_fixed.py",
        "organize_zip_directory_fixed.py",
        "organize_zip_directory.py",
        "organize_zip_directory_corrected.py",
        "comprehensive_review.py",
        "test_uuid_matching.py",
        "analyze_cursor_chats.py",
        "sync_icloud_collection_auto.py",
        "sync_icloud_collection.py",
        "restore_icloud_collection.py",
        "create_icloud_backup_mapping.py",
        "compare_collections.py",
        "compare_avatararts_with_other_dirs.py",
        "review_suno_avatararts.py",
        "review_all_work_done.py",
        "find_duplicates.py",
        "create_project_inventory.py",
        "create_comprehensive_review.py",
    ],
    # Apply/Knowledge scripts (keep together as they're related)
    "apply": [
        "APPLY_COMPLETE_ORGANIZATION_PLAN_CORRECTED.py",
        "APPLY_COMPLETE_ORGANIZATION_FROM_CSV.py",
        "APPLY_COMPLETE_ORGANIZATION_FROM_CSV_CORRECTED.py",
        "APPLY_COMPLETE_ORGANIZATION_PLAN.py",
        "APPLY_KNOWLEDGE_LEARNINGS.py",
    ],
}


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Parent-child aware reorganization")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be moved")
    parser.add_argument("--apply", action="store_true", help="Execute the reorganization")
    args = parser.parse_args()

    if not (args.dry_run or args.apply):
        print("Use --dry-run or --apply")
        return

    print("Parent-Child Aware Reorganization")
    print("=" * 45)
    print("Grouping by feature/workflow instead of type...")

    moved = 0

    for feature, scripts in FEATURE_MAPPING.items():
        feature_dir = SCRIPTS_DIR / feature
        if args.apply:
            feature_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n{feature.upper()}:")
        print(f"  Feature: {feature}")
        print(f"  Scripts: {len(scripts)}")
        print(f"  Target: scripts/{feature}/")

        # Move scripts from current locations to feature-based locations
        for script in scripts:
            # Find script in any current location
            found = False
            for current_dir in SCRIPTS_DIR.iterdir():
                if current_dir.is_dir():
                    src = current_dir / script
                    if src.exists():
                        dst = feature_dir / script
                        if args.dry_run:
                            print(f"    [move] scripts/{current_dir.name}/{script} → scripts/{feature}/")
                        else:
                            shutil.move(str(src), str(dst))
                            print(f"    Moved {script} → scripts/{feature}/")
                            moved += 1
                        found = True
                        break

            if not found:
                # Script not found in current structure
                src = PROJECT / script
                if src.exists():
                    dst = feature_dir / script
                    if args.dry_run:
                        print(f"    [move] {script} → scripts/{feature}/")
                    else:
                        shutil.move(str(src), str(dst))
                        print(f"    Moved {script} → scripts/{feature}/")
                        moved += 1

    print("\nSummary:")
    print(f"  Scripts reorganized: {moved}")
    print("  New feature-based structure created")


if __name__ == "__main__":
    main()
