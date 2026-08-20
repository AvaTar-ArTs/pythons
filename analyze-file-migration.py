#!/usr/bin/env python3
"""
Analyze current structure and show what will be migrated where
"""

from pathlib import Path


def analyze_current_structure():
    """Analyze the current directory structure."""
    base_path = Path(Path(str(Path.home()) + "/Documents/python"))

    # Categories for analysis
    categories = {
        "analysis_scripts": [],
        "youtube_projects": [],
        "ai_creative": [],
        "web_scraping": [],
        "audio_video": [],
        "utilities": [],
        "duplicates": [],
        "backups": [],
        "other": [],
    }

    # Analysis patterns
    analysis_patterns = ["analyze", "analyzer"]
    youtube_patterns = ["youtube", "yt", "shorts", "reddit"]
    ai_patterns = ["ai", "dalle", "comic", "pattern", "typography"]
    scraping_patterns = ["scraping", "scraper", "backlink", "fiverr", "fb-script"]
    av_patterns = ["audio", "video", "transcribe", "convert", "tts", "quiz"]
    utility_patterns = ["clean", "sort", "organize", "duplicate", "batch", "fdupes"]
    backup_patterns = ["backup", "old", "copy", " (1)", " (2)"]

    logger.info("🔍 Analyzing current structure...")
    logger.info("=" * 50)

    # Scan directories
    for item in base_path.iterdir():
        if item.is_dir():
            name_lower = item.name.lower()

            # Categorize directories
            if any(pattern in name_lower for pattern in backup_patterns):
                categories["backups"].append(item.name)
            elif any(pattern in name_lower for pattern in youtube_patterns):
                categories["youtube_projects"].append(item.name)
            elif any(pattern in name_lower for pattern in ai_patterns):
                categories["ai_creative"].append(item.name)
            elif any(pattern in name_lower for pattern in scraping_patterns):
                categories["web_scraping"].append(item.name)
            elif any(pattern in name_lower for pattern in av_patterns):
                categories["audio_video"].append(item.name)
            elif any(pattern in name_lower for pattern in utility_patterns):
                categories["utilities"].append(item.name)
            else:
                categories["other"].append(item.name)

        elif item.is_file() and item.suffix == ".py":
            name_lower = item.name.lower()

            if any(pattern in name_lower for pattern in analysis_patterns):
                categories["analysis_scripts"].append(item.name)
            elif any(pattern in name_lower for pattern in backup_patterns):
                categories["duplicates"].append(item.name)
            else:
                categories["other"].append(item.name)

    return categories


def show_migration_plan(categories):
    """Show the migration plan."""
    logger.info("\n📋 MIGRATION PLAN")
    logger.info("=" * 50)

    # Analysis Scripts
    logger.info(f"\n🔍 ANALYSIS SCRIPTS ({len(categories['analysis_scripts'])} files)")
    logger.info("-" * 30)
    logger.info("→ 01_core_tools/content_analyzer/")
    for script in sorted(categories["analysis_scripts"])[:10]:  # Show first 10
        logger.info(f"  • {script}")
    if len(categories["analysis_scripts"]) > 10:
        logger.info(f"  ... and {len(categories['analysis_scripts']) - 10} more")

    # YouTube Projects
    logger.info(
        f"\n📺 YOUTUBE PROJECTS ({len(categories['youtube_projects'])} directories)"
    )
    logger.info("-" * 30)
    logger.info("→ 02_youtube_automation/")
    for project in sorted(categories["youtube_projects"]):
        logger.info(f"  • {project}")

    # AI Creative
    logger.info(
        f"\n🎨 AI CREATIVE TOOLS ({len(categories['ai_creative'])} directories)"
    )
    logger.info("-" * 30)
    logger.info("→ 03_ai_creative_tools/")
    for project in sorted(categories["ai_creative"]):
        logger.info(f"  • {project}")

    # Web Scraping
    logger.info(f"\n🕷️  WEB SCRAPING ({len(categories['web_scraping'])} directories)")
    logger.info("-" * 30)
    logger.info("→ 04_web_scraping/")
    for project in sorted(categories["web_scraping"]):
        logger.info(f"  • {project}")

    # Audio/Video
    logger.info(f"\n🎵 AUDIO/VIDEO ({len(categories['audio_video'])} directories)")
    logger.info("-" * 30)
    logger.info("→ 05_audio_video/")
    for project in sorted(categories["audio_video"]):
        logger.info(f"  • {project}")

    # Utilities
    logger.info(f"\n🔧 UTILITIES ({len(categories['utilities'])} directories)")
    logger.info("-" * 30)
    logger.info("→ 06_utilities/")
    for project in sorted(categories["utilities"]):
        logger.info(f"  • {project}")

    # Duplicates
    logger.info(f"\n📄 DUPLICATES ({len(categories['duplicates'])} files)")
    logger.info("-" * 30)
    logger.info("→ 08_archived/old_versions/")
    for dup in sorted(categories["duplicates"])[:10]:  # Show first 10
        logger.info(f"  • {dup}")
    if len(categories["duplicates"]) > 10:
        logger.info(f"  ... and {len(categories['duplicates']) - 10} more")

    # Backups
    logger.info(f"\n📦 BACKUPS ({len(categories['backups'])} directories)")
    logger.info("-" * 30)
    logger.info("→ 08_archived/backups/")
    for backup in sorted(categories["backups"]):
        logger.info(f"  • {backup}")

    # Other
    logger.info(f"\n❓ OTHER ({len(categories['other'])} items)")
    logger.info("-" * 30)
    logger.info("→ 07_experimental/ or 08_archived/")
    for item in sorted(categories["other"])[:15]:  # Show first 15
        logger.info(f"  • {item}")
    if len(categories["other"]) > 15:
        logger.info(f"  ... and {len(categories['other']) - 15} more")


def show_benefits():
    """Show the benefits of reorganization."""
    logger.info("\n🎯 EXPECTED BENEFITS")
    logger.info("=" * 50)

    benefits = [
        "📁 90% reduction in duplicate files",
        "🔍 Easy navigation with numbered categories",
        "📚 Shared libraries reduce code duplication",
        "🔧 Consistent naming conventions",
        "📝 Clear documentation for each category",
        "🚀 Faster project discovery and development",
        "🧹 Clean, maintainable structure",
        "📊 Better organization for CONSTANT_144+ directories",
    ]

    for benefit in benefits:
        logger.info(f"  {benefit}")


def show_risks_and_mitigation():
    """Show risks and mitigation strategies."""
    logger.info("\n⚠️  RISKS & MITIGATION")
    logger.info("=" * 50)

    risks = [
        ("🔄 Import errors", "✅ Automated import updates"),
        ("💔 Broken scripts", "✅ Full backup before migration"),
        ("🔍 Lost files", "✅ Detailed migration log"),
        ("⏱️  Downtime", "✅ Incremental migration"),
        ("🔄 Rollback needed", "✅ Complete backup + rollback plan"),
    ]

    for risk, mitigation in risks:
        logger.info(f"  {risk}: {mitigation}")


def main():
    """Main analysis function."""
    logger.info("🔍 PYTHON PROJECTS MIGRATION ANALYSIS")
    logger.info("=" * 50)

    # Analyze current structure
    categories = analyze_current_structure()

    # Show migration plan
    show_migration_plan(categories)

    # Show benefits
    show_benefits()

    # Show risks
    show_risks_and_mitigation()

    # Summary
    total_items = sum(len(items) for items in categories.values())
    logger.info("\n📊 SUMMARY")
    logger.info("=" * 50)
    logger.info(f"Total items to migrate: {total_items}")
    logger.info(f"Analysis scripts: {len(categories['analysis_scripts'])}")
    logger.info(
        f"Project directories: {len(categories['youtube_projects']) + len(categories['ai_creative']) + len(categories['web_scraping']) + len(categories['audio_video']) + len(categories['utilities'])}"
    )
    logger.info(f"Duplicates to clean: {len(categories['duplicates'])}")
    logger.info(f"Backups to archive: {len(categories['backups'])}")

    logger.info("\n🚀 Ready to migrate? Run: python migrate_projects.py")


if __name__ == "__main__":
    main()
