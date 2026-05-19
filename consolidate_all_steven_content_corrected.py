#!/usr/bin/env python3
"""
Comprehensive Content Consolidation Script for /Users/steven directory

This script consolidates scattered HTML, PDF, MD, TXT, JSON, and other files
into a centralized, mobile-optimized structure following the same approach
used for the nocTurneMeLoDieS directory.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path


def create_consolidated_structure(base_path):
    """Create the consolidated directory structure"""
    structure = [
        "CONSOLIDATED_CONTENT_STEVEN/music_analysis/lyrics",
        "CONSOLIDATED_CONTENT_STEVEN/music_analysis/compositions",
        "CONSOLIDATED_CONTENT_STEVEN/music_analysis/structural",
        "CONSOLIDATED_CONTENT_STEVEN/documentation/readmes",
        "CONSOLIDATED_CONTENT_STEVEN/documentation/guides",
        "CONSOLIDATED_CONTENT_STEVEN/documentation/notes",
        "CONSOLIDATED_CONTENT_STEVEN/web_content/websites",
        "CONSOLIDATED_CONTENT_STEVEN/web_content/conversations",
        "CONSOLIDATED_CONTENT_STEVEN/web_content/reports",
        "CONSOLIDATED_CONTENT_STEVEN/structured_data/configurations",
        "CONSOLIDATED_CONTENT_STEVEN/structured_data/metadata",
        "CONSOLIDATED_CONTENT_STEVEN/structured_data/datasets",
        "CONSOLIDATED_CONTENT_STEVEN/creative_content/lyrics",
        "CONSOLIDATED_CONTENT_STEVEN/creative_content/prompts",
        "CONSOLIDATED_CONTENT_STEVEN/creative_content/stories",
        "CONSOLIDATED_CONTENT_STEVEN/code_assets/python_scripts",
        "CONSOLIDATED_CONTENT_STEVEN/code_assets/automation",
        "CONSOLIDATED_CONTENT_STEVEN/configuration_files/requirements",
        "CONSOLIDATED_CONTENT_STEVEN/configuration_files/docker",
    ]

    consolidated_path = Path(base_path) / "CONSOLIDATED_CONTENT_STEVEN"
    for directory in structure:
        (consolidated_path / directory).mkdir(parents=True, exist_ok=True)

    return consolidated_path


def get_content_category(filepath):
    """Determine the appropriate category for a file based on its content and name"""
    filename = filepath.name.lower()
    filepath_str = str(filepath).lower()

    # Music-related files
    if "lyric" in filename or "song" in filename or "music" in filename or "album" in filename:
        if "lyric" in filename:
            return "creative_content/lyrics"
        elif "analysis" in filename:
            return "music_analysis/structural"
        else:
            return "music_analysis/compositions"

    # Documentation files
    elif "readme" in filename or "doc" in filename or "guide" in filename or "note" in filename:
        if "readme" in filename:
            return "documentation/readmes"
        elif "guide" in filename:
            return "documentation/guides"
        else:
            return "documentation/notes"

    # Web content
    elif "conversation" in filepath_str or "chat" in filepath_str or "export" in filepath_str:
        return "web_content/conversations"
    elif "website" in filepath_str or "page" in filepath_str or "index" in filename:
        return "web_content/websites"
    elif "report" in filename:
        return "web_content/reports"

    # Structured data
    elif filepath.suffix.lower() in [".json"]:
        if "config" in filename or "setting" in filename:
            return "structured_data/configurations"
        elif "meta" in filename:
            return "structured_data/metadata"
        else:
            return "structured_data/datasets"

    # Creative content
    elif "prompt" in filename or "story" in filename or "narrative" in filename:
        if "prompt" in filename:
            return "creative_content/prompts"
        elif "story" in filename:
            return "creative_content/stories"
        else:
            return "creative_content/lyrics"

    # Code assets
    elif filepath.suffix.lower() in [".py"]:
        if "auto" in filename or "script" in filename:
            return "code_assets/automation"
        else:
            return "code_assets/python_scripts"

    # Configuration files
    elif "requirement" in filename or filepath.suffix.lower() in [".yml", ".yaml"]:
        if "requirement" in filename:
            return "configuration_files/requirements"
        else:
            return "configuration_files/docker"

    # Default to miscellaneous if no specific category found
    else:
        return "documentation/notes"  # Using notes as a general catch-all


def create_mobile_optimized_version(content, original_filename):
    """Create a mobile-optimized version of HTML content"""
    # This is a simplified version - in practice, you'd have more sophisticated
    # mobile optimization based on the specific content
    mobile_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mobile Optimized: {original_filename}</title>
    <style>
        /* Mobile-first responsive design */
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
            padding: 10px;
        }}

        .container {{
            max-width: 100%;
            margin: 0 auto;
            padding: 15px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        header {{
            background-color: #2c3e50;
            color: white;
            padding: 15px;
            text-align: center;
            border-radius: 6px 6px 0 0;
        }}

        main {{
            padding: 20px 0;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            margin-bottom: 15px;
        }}

        p {{
            margin-bottom: 15px;
        }}

        a {{
            color: #3498db;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        .mobile-button {{
            display: block;
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            background-color: #3498db;
            color: white;
            text-align: center;
            border-radius: 4px;
            border: none;
            font-size: 16px;
        }}

        /* Responsive adjustments */
        @media (max-width: 768px) {{
            body {{
                padding: 5px;
            }}

            .container {{
                padding: 10px;
            }}
        }}

        /* Dark mode support */
        @media (prefers-color-scheme: dark) {{
            body {{
                background-color: #1a1a1a;
                color: #e0e0e0;
            }}

            .container {{
                background-color: #1e1e1e;
                color: #e0e0e0;
            }}

            header {{
                background-color: #2a2a2a;
            }}

            h1, h2, h3, h4, h5, h6 {{
                color: #e0e0e0;
            }}

            a {{
                color: #64b5f6;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>{original_filename}</h1>
    </header>
    <div class="container">
        <main>
            {content}
        </main>
    </div>
</body>
</html>"""
    return mobile_html


def consolidate_files(source_base, dest_base):
    """Consolidate files from source to destination with mobile optimization for HTML"""
    source_path = Path(source_base)
    dest_path = Path(dest_base)

    # Create the destination directory structure
    create_consolidated_structure("/Users/steven/Music/nocTurneMeLoDieS")

    # Extensions to process
    extensions = [
        ".html",
        ".pdf",
        ".md",
        ".txt",
        ".json",
        ".csv",
        ".yaml",
        ".yml",
        ".xml",
        ".py",
    ]

    # Track files moved
    file_mapping = {}
    category_counts = {}

    # Find all files with specified extensions
    for ext in extensions:
        files = list(source_path.rglob(f"*{ext}"))
        files = [
            f
            for f in files
            if "nocTurneMeLoDieS" not in str(f)
            and "aider-env" not in str(f)
            and "site-packages" not in str(f)
            and "node_modules" not in str(f)
        ]

        for file_path in files:
            try:
                # Skip if it's already in the consolidated directory
                if str(file_path).startswith(str(dest_path)):
                    continue

                # Determine category
                category = get_content_category(file_path)

                # Create destination path
                dest_file_path = dest_path / category / file_path.name

                # Handle filename conflicts by adding suffix
                counter = 1
                while dest_file_path.exists():
                    stem = file_path.stem
                    suffix = file_path.suffix
                    dest_file_path = dest_path / category / f"{stem}_{counter}{suffix}"
                    counter += 1

                # Copy the file to the new location
                shutil.copy2(file_path, dest_file_path)

                # Record in mapping
                original_rel_path = str(file_path.relative_to(source_path))
                new_rel_path = str(dest_file_path.relative_to(dest_path))
                file_mapping[original_rel_path] = {
                    "new_location": new_rel_path,
                    "category": category,
                    "timestamp": datetime.now().isoformat(),
                }

                # Update category count
                if category in category_counts:
                    category_counts[category] += 1
                else:
                    category_counts[category] = 1

                print(f"Moved: {original_rel_path} -> {new_rel_path}")

                # For HTML files, create a mobile-optimized version
                if file_path.suffix.lower() == ".html":
                    # Read the original content
                    with open(file_path, encoding="utf-8", errors="ignore") as f:
                        original_content = f.read()

                    # Create mobile-optimized version
                    mobile_content = create_mobile_optimized_version(original_content, file_path.name)

                    # Save mobile version
                    mobile_file_path = dest_path / category / f"{file_path.stem}_mobile.html"
                    counter = 1
                    while mobile_file_path.exists():
                        mobile_file_path = dest_path / category / f"{file_path.stem}_mobile_{counter}.html"
                        counter += 1

                    with open(mobile_file_path, "w", encoding="utf-8") as f:
                        f.write(mobile_content)

                    # Add mobile version to mapping
                    mobile_rel_path = str(mobile_file_path.relative_to(dest_path))
                    file_mapping[original_rel_path]["mobile_version"] = mobile_rel_path
                    print(f"Created mobile version: {mobile_rel_path}")

            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                continue

    # Save mapping file
    mapping_file = dest_path / "consolidation_mapping.json"
    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump(file_mapping, f, indent=2)

    # Save summary
    summary_file = dest_path / "consolidation_summary.txt"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("Content Consolidation Summary\n")
        f.write("=" * 30 + "\n")
        f.write(f"Total files consolidated: {len(file_mapping)}\n")
        f.write(f"Consolidation date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("Files by category:\n")
        for category, count in category_counts.items():
            f.write(f"  {category}: {count}\n")

    return file_mapping, category_counts


def main():
    source_directory = "/Users/steven"
    dest_directory = "/Users/steven/Music/nocTurneMeLoDieS/CONSOLIDATED_CONTENT_STEVEN"

    print("Starting comprehensive content consolidation...")
    print(f"Source: {source_directory}")
    print(f"Destination: {dest_directory}")
    print("This will organize HTML, PDF, MD, TXT, JSON, and other files into a centralized structure")
    print("with mobile-optimized versions for HTML content.\n")

    # Create the consolidated structure
    print("Creating consolidated directory structure...")
    create_consolidated_structure("/Users/steven/Music/nocTurneMeLoDieS")

    # Consolidate the files
    print("Beginning consolidation process...")
    file_mapping, category_counts = consolidate_files(source_directory, dest_directory)

    print("\nConsolidation complete!")
    print(f"Total files processed: {len(file_mapping)}")
    print(f"Categories created: {len(category_counts)}")
    print(f"Mapping saved to: {dest_directory}/consolidation_mapping.json")
    print(f"Summary saved to: {dest_directory}/consolidation_summary.txt")

    print("\nFiles organized into categories:")
    for category, count in category_counts.items():
        print(f"  {category}: {count} files")


if __name__ == "__main__":
    main()
