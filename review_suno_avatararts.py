#!/usr/bin/env python3
"""
Review script for suno.com and avatararts connections
This script analyzes the relationship between your content and these platforms
"""

import os
from datetime import datetime
from pathlib import Path


def analyze_suno_avatararts_connections():
    """Analyze connections between your content and suno.com/avatararts.org"""

    print("Analyzing connections between your content and suno.com/avatararts.org...")
    print("=" * 70)

    # Look for files that mention suno or avatararts
    suno_related_files = []
    avatararts_related_files = []

    # Search in the main directories
    search_dirs = [
        "/Users/steven/Music/nocTurneMeLoDieS",
        "/Users/steven/Music/analysis",
        "/Users/steven/WEB_ASSETS",
        "/Users/steven/DATA",
    ]

    for search_dir in search_dirs:
        if Path(search_dir).exists():
            # Find files mentioning suno
            for root, dirs, files in os.walk(search_dir):
                for file in files:
                    if file.endswith((".txt", ".html", ".md", ".json", ".py")):
                        filepath = Path(root) / file
                        try:
                            with open(filepath, encoding="utf-8", errors="ignore") as f:
                                content = f.read().lower()

                                if "suno" in content:
                                    suno_related_files.append(str(filepath))

                                if "avatararts" in content or "avatar art" in content:
                                    avatararts_related_files.append(str(filepath))
                        except OSError:
                            continue

    print(f"Found {len(suno_related_files)} files mentioning 'suno'")
    print(f"Found {len(avatararts_related_files)} files mentioning 'avatararts'")

    # Analyze content patterns
    print("\nSuno-related content patterns:")
    print("-" * 30)

    suno_analysis = {
        "suno_ai_music": 0,
        "suno_prompts": 0,
        "suno_exports": 0,
        "suno_workflows": 0,
    }

    for file_path in suno_related_files[:10]:  # Sample first 10 files
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                content = f.read().lower()

                if "ai music" in content or "artificial intelligence" in content:
                    suno_analysis["suno_ai_music"] += 1
                if "prompt" in content:
                    suno_analysis["suno_prompts"] += 1
                if "export" in content or "download" in content:
                    suno_analysis["suno_exports"] += 1
                if "workflow" in content or "process" in content:
                    suno_analysis["suno_workflows"] += 1
        except OSError:
            continue

    for key, value in suno_analysis.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")

    print("\nAvatarArts-related content patterns:")
    print("-" * 35)

    avatararts_analysis = {
        "avatar_creation": 0,
        "avatar_design": 0,
        "avatar_workflow": 0,
        "avatar_branding": 0,
    }

    for file_path in avatararts_related_files[:10]:  # Sample first 10 files
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                content = f.read().lower()

                if "creation" in content or "generate" in content:
                    avatararts_analysis["avatar_creation"] += 1
                if "design" in content or "art" in content:
                    avatararts_analysis["avatar_design"] += 1
                if "workflow" in content or "process" in content:
                    avatararts_analysis["avatar_workflow"] += 1
                if "brand" in content or "identity" in content:
                    avatararts_analysis["avatar_branding"] += 1
        except OSError:
            continue

    for key, value in avatararts_analysis.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")

    # Create a summary report
    summary = f"""
Suno.com and AvatarArts Connection Analysis Report
====================================================

Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Overview:
- Total Suno-related files found: {len(suno_related_files)}
- Total AvatarArts-related files found: {len(avatararts_related_files)}

Suno.com Connection:
- Platform for AI-generated music
- Integration with your music generation workflows
- Export and processing of Suno-generated content
- Prompt engineering for music generation

AvatarArts Connection:
- Creative identity and branding
- Digital art and avatar creation
- Workflow integration with AI tools
- Brand representation across platforms

Recommendations:
1. Ensure all Suno-generated content is properly categorized in your consolidated structure
2. Integrate AvatarArts branding consistently across all platforms
3. Optimize Suno content for mobile viewing
4. Create dedicated sections for Suno and AvatarArts content in your web structure
"""

    # Save the analysis
    with open(
        "/Users/steven/Music/nocTurneMeLoDieS/SUNO_AVATARARTS_CONNECTION_ANALYSIS.md",
        "w",
    ) as f:
        f.write(summary)

    print(
        "\nAnalysis complete! Report saved to: /Users/steven/Music/nocTurneMeLoDieS/SUNO_AVATARARTS_CONNECTION_ANALYSIS.md"
    )

    return suno_related_files, avatararts_related_files


if __name__ == "__main__":
    suno_files, avatar_files = analyze_suno_avatararts_connections()
