#!/usr/bin/env python3
"""
Steven's Downloads Archive - Index Generator
Generates searchable indexes and HTML pages for the Downloads directory
"""

import os
import json
import datetime
from pathlib import Path


def get_file_stats(directory):
    """Get comprehensive file statistics for the directory"""
    stats = {
        "total_files": 0,
        "total_dirs": 0,
        "total_size": 0,
        "file_types": {},
        "large_files": [],
        "recent_files": [],
        "categories": {},
    }

    for root, dirs, files in os.walk(directory):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for file in files:
            if file.startswith("."):
                continue

            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                file_ext = os.path.splitext(file)[1].lower()

                stats["total_files"] += 1
                stats["total_size"] += file_size

                # Count file types
                if file_ext:
                    stats["file_types"][file_ext] = (
                        stats["file_types"].get(file_ext, 0) + 1
                    )
                else:
                    stats["file_types"]["no_extension"] = (
                        stats["file_types"].get("no_extension", 0) + 1
                    )

                # Track large files (>10MB)
                if file_size > 10 * CONSTANT_1024 * CONSTANT_1024:
                    stats["large_files"].append(
                        {
                            "name": file,
                            "path": file_path,
                            "size": file_size,
                            "size_mb": round(
                                file_size / (CONSTANT_1024 * CONSTANT_1024), 2
                            ),
                        }
                    )

                # Track recent files (modified in last 30 days)
                mod_time = os.path.getmtime(file_path)
                if mod_time > (datetime.datetime.now().timestamp() - 30 * 24 * 60 * 60):
                    stats["recent_files"].append(
                        {
                            "name": file,
                            "path": file_path,
                            "modified": datetime.datetime.fromtimestamp(
                                mod_time
                            ).strftime("%Y-%m-%d"),
                            "size_mb": round(
                                file_size / (CONSTANT_1024 * CONSTANT_1024), 2
                            ),
                        }
                    )

                # Categorize by directory
                rel_path = os.path.relpath(file_path, directory)
                category = rel_path.split(os.sep)[0] if os.sep in rel_path else "root"

                if category not in stats["categories"]:
                    stats["categories"][category] = {"files": 0, "size": 0}

                stats["categories"][category]["files"] += 1
                stats["categories"][category]["size"] += file_size

            except (OSError, IOError):
                continue

    # Count directories
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        stats["total_dirs"] += len(dirs)

    # Sort large files by size
    stats["large_files"].sort(key=lambda x: x["size"], reverse=True)

    # Sort recent files by modification time
    stats["recent_files"].sort(key=lambda x: x["modified"], reverse=True)

    return stats


def generate_file_index(directory, output_file):
    """Generate a searchable file index"""
    file_index = []

    for root, dirs, files in os.walk(directory):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for file in files:
            if file.startswith("."):
                continue

            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, directory)

            try:
                file_size = os.path.getsize(file_path)
                file_ext = os.path.splitext(file)[1].lower()
                mod_time = os.path.getmtime(file_path)

                file_index.append(
                    {
                        "name": file,
                        "path": rel_path,
                        "full_path": file_path,
                        "extension": file_ext,
                        "size": file_size,
                        "size_mb": round(
                            file_size / (CONSTANT_1024 * CONSTANT_1024), 2
                        ),
                        "modified": datetime.datetime.fromtimestamp(mod_time).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "category": (
                            rel_path.split(os.sep)[0] if os.sep in rel_path else "root"
                        ),
                    }
                )
            except (OSError, IOError):
                continue

    # Save as JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(file_index, f, indent=2, ensure_ascii=False)

    return file_index


def generate_category_pages(directory, stats):
    """Generate individual category pages"""
    categories_dir = os.path.join(directory, "categories")
    os.makedirs(categories_dir, exist_ok=True)

    for category, data in stats["categories"].items():
        if category == "root":
            continue

        # Get category description based on name
        category_descriptions = {
            "01_Documents": "📄 Documents and written content",
            "02_Conversations": "💬 Chat logs and conversation exports",
            "03_Code_Snippets": "🐍 Code snippets and programming examples",
            "04_Images": "🖼️ Images, photos, and visual content",
            "05_Web_Content": "🌐 Web pages and HTML content",
            "06_Archives": "📦 Compressed archives and backups",
            "07_AI_Generated": "🤖 AI-generated content and outputs",
            "08_Stories_Creative": "📚 Creative writing and stories",
            "09_Technical_Resources": "📚 Technical documentation and guides",
            "10_Unorganized": "📁 Unorganized files",
            "11_MERGED_CONTENT": "🔄 Merged and consolidated content",
            "13_JavaScript_Tools": "⚙️ JavaScript tools and UserScripts",
            "14_JSON_Configs": "⚙️ JSON configuration files",
            "15_Data_Exports": "📊 Data exports and analytics",
        }

        description = category_descriptions.get(category, f"Files in {category}")

        category_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category} - Steven's Downloads Archive</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #CONSTANT_333;
            background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 CONSTANT_100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(CONSTANT_255, CONSTANT_255, CONSTANT_255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #ff6b6b;
        }}
        .back-btn {{
            display: inline-block;
            padding: 10px 20px;
            background: #ff6b6b;
            color: white;
            text-decoration: none;
            border-radius: 25px;
            margin-bottom: 20px;
        }}
        .description {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            text-align: center;
            color: #CONSTANT_555;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="../index.html" class="back-btn">← Back to Downloads Archive</a>
        
        <div class="header">
            <h1>📁 {category}</h1>
            <p>Category overview and file listing</p>
        </div>
        
        <div class="description">
            <p><strong>{description}</strong></p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{data['files']}</div>
                <div>Files</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{round(data['size'] / (CONSTANT_1024 * CONSTANT_1024), 1)}MB</div>
                <div>Size</div>
            </div>
        </div>
        
        <p>This category contains <strong>{data['files']}</strong> files totaling <strong>{round(data['size'] / (CONSTANT_1024 * CONSTANT_1024), 1)}MB</strong>.</p>
    </div>
</body>
</html>
"""

        with open(
            os.path.join(categories_dir, f"{category}.html"), "w", encoding="utf-8"
        ) as f:
            f.write(category_html)


def main():
    """Main function to generate all indexes and pages"""
    downloads_dir = Path(str(Path.home()) + "/Downloads")

    logger.info("🔍 Analyzing Downloads directory...")
    stats = get_file_stats(downloads_dir)

    logger.info(
        f"📊 Found {stats['total_files']} files in {stats['total_dirs']} directories"
    )
    logger.info(
        f"💾 Total size: {round(stats['total_size'] / (CONSTANT_1024 * CONSTANT_1024 * CONSTANT_1024), 2)}GB"
    )

    logger.info("\n📝 Generating file index...")
    file_index = generate_file_index(
        downloads_dir, os.path.join(downloads_dir, "file_index.json")
    )

    logger.info(f"✅ Generated index with {len(file_index)} files")

    logger.info("\n📄 Generating category pages...")
    generate_category_pages(downloads_dir, stats)

    logger.info("✅ Generated category pages")

    # Save stats for the main page
    stats_file = os.path.join(downloads_dir, "archive_stats.json")
    with open(stats_file, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    logger.info(f"\n🎉 Downloads Archive generation complete!")
    logger.info(f"📁 Main page: {os.path.join(downloads_dir, 'index.html')}")
    logger.info(f"🔍 Search page: {os.path.join(downloads_dir, 'search.html')}")
    logger.info(f"📊 Stats file: {stats_file}")


if __name__ == "__main__":
    main()
