"""
File Management Organize Markdown 2

This module provides functionality for file management organize markdown 2.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_000 = 000
CONSTANT_100 = 100
CONSTANT_111 = 111
CONSTANT_200 = 200
CONSTANT_333 = 333
CONSTANT_521 = 521
CONSTANT_999 = 999
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Markdown Content Organizer & Display System
Organize and display your CONSTANT_521 markdown files with intelligent categorization
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
import argparse
from collections import defaultdict, Counter


class MarkdownOrganizer:
    def __init__(self, directory_path):
        """__init__ function."""

        self.directory_path = Path(directory_path)
        self.files_data = []
        self.categories = defaultdict(list)
        self.tags = Counter()
        self.keywords = Counter()

    def analyze_file(self, file_path):
        """Analyze a markdown file and extract metadata"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Get file stats
            stat = file_path.stat()

            # Extract title (first # heading or filename)
            title = self.extract_title(content, file_path.name)

            # Extract categories based on filename patterns
            categories = self.categorize_file(file_path.name, content)

            # Extract tags from content
            tags = self.extract_tags(content)

            # Extract keywords
            keywords = self.extract_keywords(content)

            # Determine content type
            content_type = self.determine_content_type(file_path.name, content)

            # Extract summary (first paragraph or description)
            summary = self.extract_summary(content)

            # Count sections
            sections = len(re.findall(r"^#+\s", content, re.MULTILINE))

            # Count code blocks
            code_blocks = len(re.findall(r"```", content))

            # Count links
            links = len(re.findall(r"\[.*?\]\(.*?\)", content))

            # Count images
            images = len(re.findall(r"!\[.*?\]\(.*?\)", content))

            file_data = {
                "name": file_path.name,
                "path": str(file_path.relative_to(self.directory_path)),
                "title": title,
                "size": stat.st_size,
                "size_mb": round(stat.st_size / (CONSTANT_1024 * CONSTANT_1024), 2),
                "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M"),
                "categories": categories,
                "tags": tags,
                "keywords": keywords,
                "content_type": content_type,
                "summary": summary,
                "sections": sections,
                "code_blocks": code_blocks,
                "links": links,
                "images": images,
                "word_count": len(content.split()),
                "line_count": len(content.split("\n")),
            }

            return file_data

        except Exception as e:
            logger.info(f"Error analyzing {file_path}: {e}")
            return None

    def extract_title(self, content, filename):
        """Extract title from content or use filename"""
        # Look for first # heading
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()

        # Look for ## heading
        title_match = re.search(r"^##\s+(.+)$", content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()

        # Use filename as fallback
        return filename.replace(".md", "").replace("_", " ").replace("-", " ")

    def categorize_file(self, filename, content):
        """Categorize file based on filename and content patterns"""
        categories = []
        filename_lower = filename.lower()
        content_lower = content.lower()

        # Business & Strategy
        if any(word in filename_lower for word in ["strategy", "brand", "seo", "analytics", "domain"]):
            categories.append("Business Strategy")
        if any(word in content_lower for word in ["business", "strategy", "brand", "marketing", "seo"]):
            categories.append("Business Strategy")

        # AI & Automation
        if any(word in filename_lower for word in ["ai", "automation", "python", "script", "gpt"]):
            categories.append("AI & Automation")
        if any(
            word in content_lower for word in ["artificial intelligence", "machine learning", "automation", "python"]
        ):
            categories.append("AI & Automation")

        # Technical Documentation
        if any(word in filename_lower for word in ["api", "code", "script", "technical", "analysis"]):
            categories.append("Technical Documentation")
        if any(word in content_lower for word in ["api", "code", "function", "class", "import"]):
            categories.append("Technical Documentation")

        # Creative Projects
        if any(word in filename_lower for word in ["avatar", "art", "music", "video", "creative", "storyboard"]):
            categories.append("Creative Projects")
        if any(word in content_lower for word in ["art", "music", "video", "creative", "design", "visual"]):
            categories.append("Creative Projects")

        # Quantum Forge Labs
        if any(word in filename_lower for word in ["quantum", "forge", "labs"]):
            categories.append("Quantum Forge Labs")

        # Avatar Arts
        if any(word in filename_lower for word in ["avatar", "arts"]):
            categories.append("Avatar Arts")

        # GPTJunkie
        if any(word in filename_lower for word in ["gpt", "junkie"]):
            categories.append("GPTJunkie")

        # Tutorials & Guides
        if any(word in filename_lower for word in ["guide", "tutorial", "how", "setup", "course"]):
            categories.append("Tutorials & Guides")
        if any(word in content_lower for word in ["tutorial", "guide", "how to", "step by step"]):
            categories.append("Tutorials & Guides")

        # Templates
        if any(word in filename_lower for word in ["template", "refund", "policy"]):
            categories.append("Templates & Policies")

        # Default category
        if not categories:
            categories.append("General")

        return categories

    def extract_tags(self, content):
        """Extract tags from content"""
        tags = set()

        # Look for #hashtags
        hashtags = re.findall(r"#(\w+)", content)
        tags.update(hashtags)

        # Look for common technical terms
        tech_terms = ["python", "ai", "automation", "api", "seo", "marketing", "business", "creative", "music", "video"]
        content_lower = content.lower()
        for term in tech_terms:
            if term in content_lower:
                tags.add(term)

        return list(tags)

    def extract_keywords(self, content):
        """Extract important keywords from content"""
        # Simple keyword extraction (can be enhanced with NLP)
        words = re.findall(r"\b[a-zA-Z]{4,}\b", content.lower())

        # Filter out common words
        stop_words = {
            "this",
            "that",
            "with",
            "have",
            "will",
            "from",
            "they",
            "know",
            "want",
            "been",
            "good",
            "much",
            "some",
            "time",
            "very",
            "when",
            "come",
            "here",
            "just",
            "like",
            "long",
            "make",
            "many",
            "over",
            "such",
            "take",
            "than",
            "them",
            "well",
            "were",
            "what",
            "your",
            "said",
            "each",
            "which",
            "their",
            "would",
            "there",
            "could",
            "other",
            "after",
            "first",
            "never",
            "these",
            "think",
            "where",
            "being",
            "every",
            "great",
            "might",
            "shall",
            "still",
            "those",
            "under",
            "while",
            "years",
            "before",
            "found",
            "going",
            "heard",
            "large",
            "place",
            "right",
            "small",
            "sound",
            "still",
            "three",
            "water",
            "world",
            "write",
            "young",
        }

        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        return keywords[:20]  # Top 20 keywords

    def determine_content_type(self, filename, content):
        """Determine the type of content"""
        filename_lower = filename.lower()
        content_lower = content.lower()

        if "script" in filename_lower or "code" in filename_lower:
            return "Code/Script"
        elif "guide" in filename_lower or "tutorial" in filename_lower:
            return "Tutorial/Guide"
        elif "strategy" in filename_lower or "business" in filename_lower:
            return "Business Strategy"
        elif "analysis" in filename_lower or "analytics" in filename_lower:
            return "Analysis/Report"
        elif "template" in filename_lower:
            return "Template"
        elif "course" in filename_lower or "plan" in filename_lower:
            return "Course/Plan"
        elif "storyboard" in filename_lower or "creative" in filename_lower:
            return "Creative Content"
        else:
            return "Documentation"

    def extract_summary(self, content):
        """Extract a summary from the content"""
        # Get first paragraph that's not a heading
        lines = content.split("\n")
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("```") and not line.startswith("---"):
                # Limit to CONSTANT_200 characters
                return line[:CONSTANT_200] + "..." if len(line) > CONSTANT_200 else line

        return "No summary available"

    def scan_directory(self):
        """Scan the directory and analyze all markdown files"""
        logger.info("🔍 Scanning markdown files...")

        md_files = list(self.directory_path.glob("*.md"))
        logger.info(f"Found {len(md_files)} markdown files")

        for i, file_path in enumerate(md_files, 1):
            logger.info(f"Analyzing {i}/{len(md_files)}: {file_path.name}")
            file_data = self.analyze_file(file_path)
            if file_data:
                self.files_data.append(file_data)

                # Update categories
                for category in file_data["categories"]:
                    self.categories[category].append(file_data)

                # Update tags
                for tag in file_data["tags"]:
                    self.tags[tag] += 1

                # Update keywords
                for keyword in file_data["keywords"]:
                    self.keywords[keyword] += 1

        logger.info(f"✅ Analysis complete! Processed {len(self.files_data)} files")

    def generate_html_dashboard(self):
        """Generate an HTML dashboard for the markdown files"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown Content Dashboard - Steven Chaplinski</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background: #CONSTANT_000;
            color: #fff;
            line-height: 1.6;
        }}
        
        .header {{
            background: linear-gradient(135deg, #dc2626, #991b1b);
            padding: 2rem;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .header p {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 3rem;
        }}
        
        .stat-card {{
            background: #CONSTANT_111;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #dc2626;
        }}
        
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #dc2626;
        }}
        
        .stat-label {{
            color: #ccc;
            margin-top: 0.5rem;
        }}
        
        .categories {{
            margin-bottom: 3rem;
        }}
        
        .category {{
            margin-bottom: 2rem;
        }}
        
        .category h2 {{
            color: #dc2626;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #dc2626;
        }}
        
        .files-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1rem;
        }}
        
        .file-card {{
            background: #CONSTANT_111;
            border: 1px solid #CONSTANT_333;
            border-radius: 8px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }}
        
        .file-card:hover {{
            border-color: #dc2626;
            transform: translateY(-2px);
        }}
        
        .file-title {{
            font-size: 1.1rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: #fff;
        }}
        
        .file-meta {{
            font-size: 0.9rem;
            color: #CONSTANT_999;
            margin-bottom: 1rem;
        }}
        
        .file-summary {{
            color: #ccc;
            margin-bottom: 1rem;
        }}
        
        .file-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}
        
        .tag {{
            background: #dc2626;
            color: #fff;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
        }}
        
        .search-box {{
            width: CONSTANT_100%;
            padding: 1rem;
            background: #CONSTANT_111;
            border: 1px solid #CONSTANT_333;
            border-radius: 8px;
            color: #fff;
            font-size: 1rem;
            margin-bottom: 2rem;
        }}
        
        .search-box:focus {{
            outline: none;
            border-color: #dc2626;
        }}
        
        .filters {{
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }}
        
        .filter-btn {{
            background: #CONSTANT_111;
            border: 1px solid #CONSTANT_333;
            color: #fff;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .filter-btn:hover,
        .filter-btn.active {{
            background: #dc2626;
            border-color: #dc2626;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 Markdown Content Dashboard</h1>
        <p>Steven Chaplinski's Knowledge Base - {len(self.files_data)} Files Organized</p>
    </div>
    
    <div class="container">
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(self.files_data)}</div>
                <div class="stat-label">Total Files</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(self.categories)}</div>
                <div class="stat-label">Categories</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{sum(f['size'] for f in self.files_data) // (CONSTANT_1024*CONSTANT_1024)}</div>
                <div class="stat-label">Total Size (MB)</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(self.tags)}</div>
                <div class="stat-label">Unique Tags</div>
            </div>
        </div>
        
        <input type="text" class="search-box" placeholder="🔍 Search files, tags, or content..." id="searchBox">
        
        <div class="filters">
            <button class="filter-btn active" data-category="all">All Files</button>
            {''.join(f'<button class="filter-btn" data-category="{cat}">{cat}</button>' for cat in self.categories.keys())}
        </div>
        
        <div class="categories">
            {self.generate_category_html()}
        </div>
    </div>
    
    <script>
        // Search functionality
        document.getElementById('searchBox').addEventListener('input', function(e) {{
            const searchTerm = e.target.value.toLowerCase();
            const fileCards = document.querySelectorAll('.file-card');
            
            fileCards.forEach(card => {{
                const title = card.querySelector('.file-title').textContent.toLowerCase();
                const summary = card.querySelector('.file-summary').textContent.toLowerCase();
                const tags = Array.from(card.querySelectorAll('.tag')).map(tag => tag.textContent.toLowerCase());
                
                const matches = title.includes(searchTerm) || 
                              summary.includes(searchTerm) || 
                              tags.some(tag => tag.includes(searchTerm));
                
                card.style.display = matches ? 'block' : 'none';
            }});
        }});
        
        // Filter functionality
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                // Remove active class from all buttons
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                // Add active class to clicked button
                this.classList.add('active');
                
                const category = this.dataset.category;
                const fileCards = document.querySelectorAll('.file-card');
                
                fileCards.forEach(card => {{
                    if (category === 'all') {{
                        card.style.display = 'block';
                    }} else {{
                        const cardCategory = card.dataset.category;
                        card.style.display = cardCategory === category ? 'block' : 'none';
                    }}
                }});
            }});
        }});
    </script>
</body>
</html>
"""

        return html_content

    def generate_category_html(self):
        """Generate HTML for each category"""
        html = ""
        for category, files in self.categories.items():
            html += f"""
            <div class="category">
                <h2>{category} ({len(files)} files)</h2>
                <div class="files-grid">
            """

            for file_data in files:
                tags_html = "".join(f'<span class="tag">{tag}</span>' for tag in file_data["tags"][:5])

                html += f"""
                    <div class="file-card" data-category="{category}">
                        <div class="file-title">{file_data['title']}</div>
                        <div class="file-meta">
                            {file_data['size_mb']} MB • {file_data['modified']} • {file_data['sections']} sections
                        </div>
                        <div class="file-summary">{file_data['summary']}</div>
                        <div class="file-tags">{tags_html}</div>
                    </div>
                """

            html += """
                </div>
            </div>
            """

        return html

    def generate_json_export(self):
        """Generate JSON export of all data"""
        export_data = {
            "metadata": {
                "total_files": len(self.files_data),
                "total_categories": len(self.categories),
                "total_tags": len(self.tags),
                "scan_date": datetime.now().isoformat(),
                "directory": str(self.directory_path),
            },
            "categories": dict(self.categories),
            "top_tags": dict(self.tags.most_common(20)),
            "top_keywords": dict(self.keywords.most_common(20)),
            "files": self.files_data,
        }

        return json.dumps(export_data, indent=2)

    def run(self):
        """Run the complete analysis and generation"""
        logger.info("🚀 Starting Markdown Content Organizer...")

        # Scan directory
        self.scan_directory()

        # Generate HTML dashboard
        logger.info("📊 Generating HTML dashboard...")
        html_content = self.generate_html_dashboard()

        # Save HTML dashboard
        dashboard_path = self.directory_path / "markdown_dashboard.html"
        with open(dashboard_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Generate JSON export
        logger.info("💾 Generating JSON export...")
        json_content = self.generate_json_export()

        # Save JSON export
        json_path = self.directory_path / "markdown_data.json"
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(json_content)

        # Print summary
        logger.info(Path("\n") + "=" * 60)
        logger.info("📊 ANALYSIS COMPLETE!")
        logger.info("=" * 60)
        logger.info(f"📁 Total Files: {len(self.files_data)}")
        logger.info(f"📂 Categories: {len(self.categories)}")
        logger.info(f"🏷️  Unique Tags: {len(self.tags)}")
        logger.info(f"📄 Total Size: {sum(f['size'] for f in self.files_data) // (CONSTANT_1024*CONSTANT_1024)} MB")
        logger.info("\n📊 Top Categories:")
        for category, files in sorted(self.categories.items(), key=lambda x: len(x[1]), reverse=True):
            logger.info(f"   {category}: {len(files)} files")

        logger.info("\n🏷️  Top Tags:")
        for tag, count in self.tags.most_common(10):
            logger.info(f"   {tag}: {count}")

        logger.info(f"\n📄 Files Generated:")
        logger.info(f"   📊 Dashboard: {dashboard_path}")
        logger.info(f"   💾 Data Export: {json_path}")

        logger.info("\n🌐 Open the dashboard in your browser to explore your content!")


def main():
    """main function."""

    parser = argparse.ArgumentParser(description="Organize and display markdown files")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to scan (default: current directory)")

    args = parser.parse_args()

    organizer = MarkdownOrganizer(args.directory)
    organizer.run()


if __name__ == "__main__":
    main()
