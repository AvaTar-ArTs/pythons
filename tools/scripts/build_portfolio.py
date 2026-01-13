#!/usr/bin/env python3
"""
AvatarArts Portfolio Auto-Builder
Scans repository for Python projects and generates portfolio pages
"""

import os
import sys
import csv
import json
import ast
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Category keywords for intelligent classification
CATEGORIES = {
    "AI & Machine Learning": [
        "ai", "ml", "machine learning", "neural", "deep learning", "tensorflow",
        "pytorch", "sklearn", "model", "training", "inference", "llm", "gpt",
        "openai", "anthropic", "claude", "embeddings", "transformers"
    ],
    "Automation & Workflows": [
        "automation", "workflow", "pipeline", "orchestration", "airflow",
        "celery", "task", "scheduler", "cron", "batch", "etl", "data pipeline"
    ],
    "Web Scraping & Data Collection": [
        "scrape", "scraper", "crawl", "crawler", "beautifulsoup", "selenium",
        "requests", "scrapy", "web scraping", "data collection", "api client"
    ],
    "Data Analysis & Visualization": [
        "analysis", "analytics", "visualization", "pandas", "numpy", "matplotlib",
        "seaborn", "plotly", "dashboard", "chart", "graph", "statistics", "metrics"
    ],
    "Music & Audio": [
        "music", "audio", "sound", "mp3", "wav", "suno", "discography",
        "playlist", "track", "album", "spotify", "bandcamp"
    ],
    "SEO & Marketing": [
        "seo", "marketing", "keyword", "analytics", "google analytics",
        "meta", "sitemap", "backlink", "rank", "optimization"
    ],
    "Web Development": [
        "flask", "django", "fastapi", "web", "api", "rest", "graphql",
        "server", "backend", "frontend", "html", "css", "javascript"
    ],
    "Database & Storage": [
        "database", "sql", "sqlite", "postgresql", "mysql", "mongodb",
        "redis", "storage", "query", "orm", "sqlalchemy"
    ],
    "File Processing": [
        "file", "csv", "json", "xml", "parser", "converter", "transform",
        "import", "export", "format"
    ],
    "Utilities & Tools": [
        "utility", "tool", "helper", "cli", "command line", "script"
    ]
}

class PortfolioBuilder:
    def __init__(self, root_dir="."):
        self.root = Path(root_dir).resolve()
        self.projects = []
        self.stats = {
            'total_files': 0,
            'total_lines': 0,
            'by_category': defaultdict(int),
            'languages': defaultdict(int)
        }

    def analyze_python_file(self, filepath):
        """Extract information from Python file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Count lines
            lines = len([l for l in content.split('\n') if l.strip()])

            # Try to parse AST for docstrings
            try:
                tree = ast.parse(content)
                docstring = ast.get_docstring(tree) or ""
            except:
                docstring = ""

            # Extract imports
            imports = []
            try:
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module)
            except:
                pass

            return {
                'lines': lines,
                'docstring': docstring,
                'imports': imports,
                'content_preview': content[:500]
            }
        except Exception as e:
            return {'lines': 0, 'docstring': '', 'imports': [], 'content_preview': ''}

    def categorize_project(self, name, description, imports, filepath):
        """Intelligently categorize project based on multiple signals"""
        text = f"{name} {description} {' '.join(imports)} {filepath}".lower()

        scores = {}
        for category, keywords in CATEGORIES.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scores[category] = score

        if scores:
            return max(scores, key=scores.get)
        return "Utilities & Tools"

    def scan_directory(self):
        """Scan directory for Python projects"""
        print(f"🔍 Scanning {self.root} for Python projects...")

        # Patterns to ignore
        ignore_patterns = {
            '.venv', 'venv', 'node_modules', '__pycache__',
            '.git', '.github', 'dist', 'build', 'egg-info'
        }

        python_files = []
        for root, dirs, files in os.walk(self.root):
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_patterns]

            for file in files:
                if file.endswith('.py') and not file.startswith('_'):
                    filepath = Path(root) / file
                    python_files.append(filepath)

        print(f"   Found {len(python_files)} Python files")

        # Group by project (directory)
        projects_dict = defaultdict(list)
        for filepath in python_files:
            # Get project name (parent directory or filename)
            if filepath.parent != self.root:
                project_name = filepath.parent.name
            else:
                project_name = filepath.stem

            projects_dict[project_name].append(filepath)

        # Analyze each project
        for project_name, files in projects_dict.items():
            # Skip if only __init__.py
            if len(files) == 1 and files[0].name == '__init__.py':
                continue

            # Analyze main file (largest or most relevant)
            main_file = max(files, key=lambda f: f.stat().st_size)
            analysis = self.analyze_python_file(main_file)

            # Build description
            description = analysis['docstring'].split('\n')[0] if analysis['docstring'] else ""
            if not description:
                # Try to infer from filename
                description = f"Python script for {project_name.replace('_', ' ').replace('-', ' ')}"

            # Get category
            category = self.categorize_project(
                project_name,
                description,
                analysis['imports'],
                str(main_file)
            )

            # Detect technologies
            tech_stack = []
            imports_set = set(analysis['imports'])

            tech_mappings = {
                'pandas': 'Pandas', 'numpy': 'NumPy', 'matplotlib': 'Matplotlib',
                'flask': 'Flask', 'django': 'Django', 'fastapi': 'FastAPI',
                'tensorflow': 'TensorFlow', 'torch': 'PyTorch', 'sklearn': 'scikit-learn',
                'beautifulsoup4': 'BeautifulSoup', 'selenium': 'Selenium',
                'requests': 'Requests', 'sqlalchemy': 'SQLAlchemy',
                'openai': 'OpenAI API', 'anthropic': 'Claude API'
            }

            for imp in imports_set:
                for key, value in tech_mappings.items():
                    if key in imp.lower():
                        tech_stack.append(value)

            if not tech_stack:
                tech_stack = ['Python 3']

            # Calculate total lines
            total_lines = sum(self.analyze_python_file(f)['lines'] for f in files)

            project = {
                'name': project_name,
                'description': description[:200],
                'category': category,
                'tech_stack': ', '.join(sorted(set(tech_stack))),
                'files': len(files),
                'lines': total_lines,
                'path': str(main_file.relative_to(self.root))
            }

            self.projects.append(project)
            self.stats['by_category'][category] += 1
            self.stats['total_files'] += len(files)
            self.stats['total_lines'] += total_lines

        # Sort by lines (most substantial first)
        self.projects.sort(key=lambda x: x['lines'], reverse=True)

        print(f"   Identified {len(self.projects)} projects")
        print(f"   Total lines: {self.stats['total_lines']:,}")

    def generate_csv(self, output_path="portfolio/portfolio_descriptions.csv"):
        """Generate CSV file for portfolio data"""
        output = self.root / output_path
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Project Name', 'Description', 'Category',
                'Tech Stack', 'Files', 'Lines of Code', 'Path'
            ])

            for project in self.projects:
                writer.writerow([
                    project['name'],
                    project['description'],
                    project['category'],
                    project['tech_stack'],
                    project['files'],
                    project['lines'],
                    project['path']
                ])

        print(f"✅ Generated {output}")
        return output

    def generate_markdown(self, output_path="content/python_portfolio.md"):
        """Generate Markdown portfolio page"""
        output = self.root / output_path
        output.parent.mkdir(parents=True, exist_ok=True)

        md = f"""# Python Portfolio

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Projects:** {len(self.projects)}
**Total Lines of Code:** {self.stats['total_lines']:,}

---

## Projects by Category

"""

        # Group by category
        by_category = defaultdict(list)
        for project in self.projects:
            by_category[project['category']].append(project)

        for category in sorted(by_category.keys()):
            md += f"\n### {category} ({len(by_category[category])} projects)\n\n"

            for proj in by_category[category]:
                md += f"""
#### {proj['name']}

**Description:** {proj['description']}

**Tech Stack:** {proj['tech_stack']}
**Scale:** {proj['files']} files, {proj['lines']:,} lines

**Path:** `{proj['path']}`

---

"""

        # Add statistics
        md += f"""
## Portfolio Statistics

| Metric | Value |
|--------|------:|
| Total Projects | {len(self.projects)} |
| Total Files | {self.stats['total_files']:,} |
| Total Lines of Code | {self.stats['total_lines']:,} |

### Projects by Category

| Category | Count |
|----------|------:|
"""

        for cat in sorted(self.stats['by_category'].keys()):
            md += f"| {cat} | {self.stats['by_category'][cat]} |\n"

        md += "\n---\n\n*Auto-generated by Portfolio Builder*\n"

        output.write_text(md, encoding='utf-8')
        print(f"✅ Generated {output}")
        return output

    def generate_case_studies(self, output_path="content/alchemy_case_studies.md"):
        """Generate case study highlights for top projects"""
        output = self.root / output_path
        output.parent.mkdir(parents=True, exist_ok=True)

        # Select top 10 projects by significance
        top_projects = self.projects[:10]

        md = f"""# Case Studies - Top Projects

**Auto-generated:** {datetime.now().strftime('%Y-%m-%d')}

> Paste this section at the top of your `alchemy.md` page for instant portfolio showcase.

---

"""

        for i, proj in enumerate(top_projects, 1):
            # Create compelling case study format
            md += f"""
## Case Study #{i}: {proj['name'].replace('_', ' ').title()}

**Challenge:** {self._generate_challenge(proj)}

**Solution:** {proj['description']}

**Technologies:** {proj['tech_stack']}

**Impact:** Implemented in {proj['files']} modular files spanning {proj['lines']:,} lines of production-ready Python code.

**Category:** {proj['category']}

---

"""

        output.write_text(md, encoding='utf-8')
        print(f"✅ Generated {output}")
        return output

    def _generate_challenge(self, project):
        """Generate challenge statement based on category"""
        challenges = {
            "AI & Machine Learning": "Automate complex AI workflows and integrate cutting-edge language models",
            "Automation & Workflows": "Streamline repetitive tasks and build scalable automation pipelines",
            "Web Scraping & Data Collection": "Extract and process data from diverse web sources efficiently",
            "Data Analysis & Visualization": "Transform raw data into actionable insights with visual clarity",
            "Music & Audio": "Manage and distribute large-scale music catalog with metadata automation",
            "SEO & Marketing": "Optimize content discoverability and track performance metrics",
            "Web Development": "Build robust web applications with modern Python frameworks",
            "Database & Storage": "Design efficient data storage and retrieval systems",
            "File Processing": "Process and transform files at scale with reliability",
            "Utilities & Tools": "Create developer tools that improve productivity"
        }
        return challenges.get(project['category'], "Build efficient solution for complex technical problem")

    def build_all(self):
        """Build complete portfolio package"""
        print("=" * 60)
        print("AVATARARTS PORTFOLIO AUTO-BUILDER")
        print("=" * 60)
        print()

        self.scan_directory()
        print()

        print("📝 Generating output files...")
        csv_path = self.generate_csv()
        md_path = self.generate_markdown()
        case_studies_path = self.generate_case_studies()

        print()
        print("=" * 60)
        print("✅ BUILD COMPLETE")
        print("=" * 60)
        print(f"\nGenerated files:")
        print(f"  - {csv_path}")
        print(f"  - {md_path}")
        print(f"  - {case_studies_path}")
        print()
        print("Next steps:")
        print("  1. Review generated case studies")
        print("  2. Copy case studies to alchemy.md")
        print("  3. Deploy python.html to your site")
        print()

def main():
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        root_dir = "."

    builder = PortfolioBuilder(root_dir)
    builder.build_all()

if __name__ == "__main__":
    main()
