#!/usr/bin/env python3
"""Python Repository Analyzer & Portfolio Generator
Analyzes Python scripts, categorizes them with GPT-4, and generates portfolio-ready outputs
"""

import csv
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import pandas as pd
    from dotenv import load_dotenv
    from openai import OpenAI

    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    print("Missing dependencies. Install with: pip install openai python-dotenv pandas")


class PythonRepoAnalyzer:
    def __init__(self, openai_api_key: str | None = None):
        self.load_environment()
        self.client = None
        if DEPENDENCIES_AVAILABLE and (openai_api_key or os.getenv("OPENAI_API_KEY")):
            self.client = OpenAI(api_key=openai_api_key or os.getenv("OPENAI_API_KEY"))

        # Your main Python directories
        self.root_directories = [
            "/Users/steven/Documents/Python",
        ]

        # Exclusion patterns (refined from your original)
        self.excluded_patterns = [
            r"^.*\/\..*",  # Hidden files/dirs
            r".*/(venv|\.venv|env|\.env|lib|\.lib|my_global_venv|\.my_global_venv)/.*",
            r".*/(Library|\.config|\.spicetify|\.gem|\.zprofile)/.*",
            r".*/(node|miniconda3)/.*",
            r".*/(simplegallery|avatararts|github|gitHub)/.*",
            r".*/__pycache__/.*",
            r".*\.pyc$",
            r".*\.pyo$",
        ]

        self.script_data = []
        self.categories = {
            "Audio & Music": [],
            "Image Processing": [],
            "YouTube & Video": [],
            "AI & GPT Tools": [],
            "File Management": [],
            "Web Scraping": [],
            "Data Processing": [],
            "Automation": [],
            "Utilities": [],
            "Other": [],
        }

    def load_environment(self):
        """Load environment variables from .env file"""
        env_paths = ["/Users/steven/.env", os.path.expanduser("~/.env"), ".env"]
        for path in env_paths:
            if os.path.exists(path):
                if DEPENDENCIES_AVAILABLE:
                    load_dotenv(dotenv_path=path)
                break

    def is_excluded(self, file_path: str) -> bool:
        """Check if file path matches exclusion patterns"""
        for pattern in self.excluded_patterns:
            if re.search(pattern, file_path):
                return True
        return False

    def extract_imports(self, content: str) -> list[str]:
        """Extract import statements from Python code"""
        import_pattern = r"^(?:from\s+(\S+)\s+import|import\s+(\S+))"
        imports = []
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith(("import ", "from ")):
                match = re.match(import_pattern, line)
                if match:
                    module = match.group(1) or match.group(2)
                    if module:
                        imports.append(module.split(".")[0])
        return list(set(imports))

    def analyze_script_content(self, file_path: str, content: str) -> dict[str, Any]:
        """Analyze a single Python script"""
        try:
            lines = content.split("\n")
            non_empty_lines = [
                line
                for line in lines
                if line.strip() and not line.strip().startswith("#")
            ]

            # Basic metrics
            metrics = {
                "file_name": os.path.basename(file_path),
                "file_path": file_path,
                "relative_path": file_path.replace("/Users/steven/", "~/"),
                "size_kb": (
                    os.path.getsize(file_path) // 1024
                    if os.path.exists(file_path)
                    else 0
                ),
                "lines_total": len(lines),
                "lines_code": len(non_empty_lines),
                "imports": self.extract_imports(content),
                "functions": len(re.findall(r"^def\s+\w+", content, re.MULTILINE)),
                "classes": len(re.findall(r"^class\s+\w+", content, re.MULTILINE)),
                "docstrings": len(re.findall(r'""".*?"""', content, re.DOTALL)),
                "created_date": (
                    datetime.fromtimestamp(os.path.getctime(file_path)).strftime(
                        "%Y-%m-%d",
                    )
                    if os.path.exists(file_path)
                    else "Unknown"
                ),
                "modified_date": (
                    datetime.fromtimestamp(os.path.getmtime(file_path)).strftime(
                        "%Y-%m-%d",
                    )
                    if os.path.exists(file_path)
                    else "Unknown"
                ),
            }

            # Determine category based on filename and content
            metrics["category"] = self.categorize_script(
                file_path, content, metrics["imports"],
            )

            return metrics

        except Exception as e:
            return {"error": str(e), "file_path": file_path}

    def categorize_script(
        self, file_path: str, content: str, imports: list[str],
    ) -> str:
        """Categorize script based on filename, content, and imports"""
        filename = os.path.basename(file_path).lower()
        content_lower = content.lower()

        # Audio & Music
        if any(
            keyword in filename
            for keyword in [
                "audio",
                "mp3",
                "wav",
                "music",
                "sound",
                "whisper",
                "transcrib",
            ]
        ):
            return "Audio & Music"
        if any(imp in imports for imp in ["pydub", "librosa", "soundfile", "wave"]):
            return "Audio & Music"
        if "whisper" in content_lower or "transcrib" in content_lower:
            return "Audio & Music"

        # Image Processing
        if any(
            keyword in filename
            for keyword in ["image", "img", "photo", "resize", "pil", "opencv"]
        ):
            return "Image Processing"
        if any(imp in imports for imp in ["PIL", "cv2", "pillow", "skimage"]):
            return "Image Processing"
        if "dalle" in content_lower or "image" in content_lower:
            return "Image Processing"

        # YouTube & Video
        if any(keyword in filename for keyword in ["youtube", "yt", "video", "mp4"]):
            return "YouTube & Video"
        if any(imp in imports for imp in ["youtube_dl", "pytube", "yt_dlp"]):
            return "YouTube & Video"

        # AI & GPT Tools
        if any(keyword in filename for keyword in ["gpt", "openai", "ai", "chat"]):
            return "AI & GPT Tools"
        if any(imp in imports for imp in ["openai", "transformers", "torch"]):
            return "AI & GPT Tools"
        if "openai" in content_lower or "gpt" in content_lower:
            return "AI & GPT Tools"

        # File Management
        if any(
            keyword in filename
            for keyword in ["file", "sort", "organize", "rename", "move"]
        ):
            return "File Management"
        if "os.rename" in content or "shutil" in imports:
            return "File Management"

        # Web Scraping
        if any(
            imp in imports
            for imp in ["requests", "beautifulsoup4", "scrapy", "selenium"]
        ):
            return "Web Scraping"

        # Data Processing
        if any(imp in imports for imp in ["pandas", "numpy", "csv"]):
            return "Data Processing"
        if any(
            keyword in filename for keyword in ["csv", "data", "process", "analyze"]
        ):
            return "Data Processing"

        # Automation
        if any(
            keyword in filename for keyword in ["auto", "script", "batch", "process"]
        ):
            return "Automation"

        # Utilities
        if any(keyword in filename for keyword in ["util", "helper", "tool"]):
            return "Utilities"

        return "Other"

    def analyze_with_gpt(self, file_path: str, content: str) -> dict[str, str]:
        """Use GPT-4 to analyze script purpose and generate descriptions"""
        if not self.client:
            return {
                "gpt_category": "N/A (No API)",
                "description": "GPT analysis unavailable - no API key configured",
                "use_case": "Manual analysis required",
                "target_audience": "General",
                "complexity": "Unknown",
            }

        try:
            # Truncate content for API limits
            content_sample = content[:3000] if len(content) > 3000 else content

            prompt = f"""
Analyze this Python script and provide a structured response in JSON format:

Filename: {os.path.basename(file_path)}
Code sample:
```python
{content_sample}
```

Please provide:
1. A concise description (1-2 sentences) of what this script does
2. Primary use case or purpose
3. Target audience (e.g., "Digital Artists", "Musicians", "Content Creators", "Developers")
4. Complexity level (Beginner/Intermediate/Advanced)
5. Category (choose one: Audio & Music, Image Processing, YouTube & Video, AI & GPT Tools, File Management, Web Scraping, Data Processing, Automation, Utilities, Other)

Respond only with valid JSON in this format:
{{
    "description": "Brief description here",
    "use_case": "Primary use case",
    "target_audience": "Target audience",
    "complexity": "Complexity level",
    "category": "Category name"
}}
"""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3,
            )

            result_text = response.choices[0].message.content.strip()
            # Clean up any markdown formatting
            result_text = result_text.replace("```json", "").replace("```", "").strip()

            result = json.loads(result_text)
            return {
                "gpt_category": result.get("category", "Other"),
                "description": result.get("description", "No description available"),
                "use_case": result.get("use_case", "General purpose"),
                "target_audience": result.get("target_audience", "General"),
                "complexity": result.get("complexity", "Unknown"),
            }

        except Exception as e:
            return {
                "gpt_category": "Analysis Error",
                "description": f"GPT analysis failed: {e!s}",
                "use_case": "Manual analysis required",
                "target_audience": "General",
                "complexity": "Unknown",
            }

    def scan_repositories(self) -> list[dict[str, Any]]:
        """Scan all Python files in specified directories"""
        all_scripts = []

        print("Starting repository scan...")

        for root_dir in self.root_directories:
            if not os.path.exists(root_dir):
                print(f"Directory not found: {root_dir}")
                continue

            print(f"Scanning: {root_dir}")

            for root, dirs, files in os.walk(root_dir):
                # Skip excluded directories
                dirs[:] = [
                    d for d in dirs if not self.is_excluded(os.path.join(root, d))
                ]

                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)

                        if self.is_excluded(file_path):
                            continue

                        try:
                            with open(
                                file_path, encoding="utf-8", errors="ignore",
                            ) as f:
                                content = f.read()

                            # Basic analysis
                            script_info = self.analyze_script_content(
                                file_path, content,
                            )

                            # GPT analysis (if available)
                            if (
                                len(content.strip()) > 50
                            ):  # Only analyze substantial scripts
                                gpt_analysis = self.analyze_with_gpt(file_path, content)
                                script_info.update(gpt_analysis)
                            else:
                                script_info.update(
                                    {
                                        "gpt_category": "Too Small",
                                        "description": "Script too small for detailed analysis",
                                        "use_case": "Utility/Fragment",
                                        "target_audience": "Developers",
                                        "complexity": "Beginner",
                                    },
                                )

                            all_scripts.append(script_info)
                            print(f"  Analyzed: {script_info['file_name']}")

                        except Exception as e:
                            print(f"  Error analyzing {file_path}: {e}")
                            continue

        return all_scripts

    def generate_csv_report(self, scripts: list[dict[str, Any]], output_path: str):
        """Generate CSV report of analyzed scripts"""
        if not scripts:
            print("No scripts to export")
            return

        # Prepare data for CSV
        csv_data = []
        for script in scripts:
            if "error" in script:
                continue

            row = {
                "Script Name": script.get("file_name", "Unknown"),
                "Category (Auto)": script.get("category", "Other"),
                "Category (GPT)": script.get("gpt_category", "N/A"),
                "Description": script.get("description", "No description"),
                "Use Case": script.get("use_case", "General"),
                "Target Audience": script.get("target_audience", "General"),
                "Complexity": script.get("complexity", "Unknown"),
                "File Size (KB)": script.get("size_kb", 0),
                "Lines of Code": script.get("lines_code", 0),
                "Functions": script.get("functions", 0),
                "Classes": script.get("classes", 0),
                "Key Imports": ", ".join(
                    script.get("imports", [])[:5],
                ),  # Top 5 imports
                "File Path": script.get(
                    "relative_path", script.get("file_path", "Unknown"),
                ),
                "Created": script.get("created_date", "Unknown"),
                "Modified": script.get("modified_date", "Unknown"),
                "GitHub URL": (
                    f"https://github.com/ichoake/python/blob/main/{script.get('file_name', '')}"
                    if script.get("file_name")
                    else ""
                ),
                "Portfolio URL": (
                    f"https://avatararts.org/python.html#{script.get('file_name', '').replace('.py', '')}"
                    if script.get("file_name")
                    else ""
                ),
            }
            csv_data.append(row)

        # Write CSV
        if DEPENDENCIES_AVAILABLE:
            df = pd.DataFrame(csv_data)
            df.to_csv(output_path, index=False)
        else:
            with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
                if csv_data:
                    fieldnames = csv_data[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(csv_data)

        print(f"CSV report saved to: {output_path}")

    def generate_html_portfolio(self, scripts: list[dict[str, Any]], output_path: str):
        """Generate HTML portfolio page"""
        # Group scripts by category
        categorized = {}
        for script in scripts:
            if "error" in script:
                continue
            category = script.get("gpt_category", script.get("category", "Other"))
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(script)

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Steven's Python Portfolio - Creative Tech Engineer</title>
    <style>
        body {{
            font-family: 'SF Pro Display', system-ui, -apple-system, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #1e1e2e 0%, #2d2d3a 100%);
            color: #e0e0e0;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        header {{
            text-align: center;
            padding: 60px 0;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            margin-bottom: 40px;
            border-radius: 20px;
        }}
        h1 {{
            font-size: 3rem;
            margin: 0 0 10px 0;
            font-weight: 700;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
        .subtitle {{
            font-size: 1.3rem;
            opacity: 0.9;
            margin: 0;
        }}
        .category-section {{
            margin-bottom: 50px;
        }}
        .category-title {{
            font-size: 2rem;
            color: #6366f1;
            border-bottom: 2px solid #6366f1;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        .script-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 25px;
        }}
        .script-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }}
        .script-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
        }}
        .script-title {{
            font-size: 1.4rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 10px;
        }}
        .script-description {{
            color: #b0b0b0;
            margin-bottom: 15px;
            font-size: 0.95rem;
        }}
        .script-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 15px;
        }}
        .meta-badge {{
            background: rgba(99, 102, 241, 0.2);
            color: #a5b4fc;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }}
        .script-links {{
            display: flex;
            gap: 10px;
        }}
        .btn {{
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.85rem;
            transition: all 0.2s ease;
        }}
        .btn-primary {{
            background: #6366f1;
            color: white;
        }}
        .btn-secondary {{
            background: rgba(255,255,255,0.1);
            color: #e0e0e0;
        }}
        .btn:hover {{
            transform: translateY(-2px);
            filter: brightness(1.1);
        }}
        .stats {{
            text-align: center;
            padding: 30px;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            margin-bottom: 40px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .stat-item {{
            padding: 20px;
            background: rgba(99, 102, 241, 0.1);
            border-radius: 10px;
        }}
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #6366f1;
        }}
        .stat-label {{
            color: #b0b0b0;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Python Portfolio</h1>
            <p class="subtitle">Creative Tech Engineer • AI-Powered Tools for Artists & Musicians</p>
        </header>
        
        <div class="stats">
            <h2>Portfolio Statistics</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number">{len([s for s in scripts if 'error' not in s])}</div>
                    <div class="stat-label">Total Scripts</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{len(categorized)}</div>
                    <div class="stat-label">Categories</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{sum(s.get('lines_code', 0) for s in scripts if 'error' not in s):,}</div>
                    <div class="stat-label">Lines of Code</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{sum(s.get('functions', 0) for s in scripts if 'error' not in s)}</div>
                    <div class="stat-label">Functions</div>
                </div>
            </div>
        </div>
"""

        # Generate category sections
        for category, category_scripts in sorted(categorized.items()):
            html_content += f"""
        <div class="category-section">
            <h2 class="category-title">{category}</h2>
            <div class="script-grid">
"""

            for script in category_scripts:
                imports_str = ", ".join(script.get("imports", [])[:3])  # Top 3 imports
                github_url = f"https://github.com/ichoake/python/blob/main/{script.get('file_name', '')}"
                portfolio_url = f"https://avatararts.org/python.html#{script.get('file_name', '').replace('.py', '')}"

                html_content += f"""
                <div class="script-card" id="{script.get('file_name', '').replace('.py', '')}">
                    <div class="script-title">{script.get('file_name', 'Unknown')}</div>
                    <div class="script-description">{script.get('description', 'No description available')}</div>
                    <div class="script-meta">
                        <span class="meta-badge">{script.get('target_audience', 'General')}</span>
                        <span class="meta-badge">{script.get('complexity', 'Unknown')}</span>
                        <span class="meta-badge">{script.get('lines_code', 0)} lines</span>
                        {f'<span class="meta-badge">{imports_str}</span>' if imports_str else ''}
                    </div>
                    <div class="script-links">
                        <a href="{github_url}" class="btn btn-primary" target="_blank">View Code</a>
                        <a href="{portfolio_url}" class="btn btn-secondary">Portfolio Link</a>
                    </div>
                </div>
"""

            html_content += """
            </div>
        </div>
"""

        html_content += """
    </div>
</body>
</html>"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"HTML portfolio saved to: {output_path}")

    def run_analysis(self):
        """Main analysis runner"""
        print("Python Repository Analyzer & Portfolio Generator")
        print("=" * 50)

        # Scan repositories
        scripts = self.scan_repositories()

        if not scripts:
            print("No Python scripts found to analyze")
            return

        print(f"\nAnalyzed {len(scripts)} Python scripts")

        # Create output directory
        output_dir = "/Users/steven/Documents/Python_Analysis"
        os.makedirs(output_dir, exist_ok=True)

        # Generate timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Generate CSV report
        csv_path = os.path.join(
            output_dir, f"python_portfolio_analysis_{timestamp}.csv",
        )
        self.generate_csv_report(scripts, csv_path)

        # Generate HTML portfolio
        html_path = os.path.join(output_dir, f"python_portfolio_{timestamp}.html")
        self.generate_html_portfolio(scripts, html_path)

        # Category summary
        categories = {}
        for script in scripts:
            if "error" in script:
                continue
            cat = script.get("gpt_category", script.get("category", "Other"))
            categories[cat] = categories.get(cat, 0) + 1

        print("\nCategory Summary:")
        for category, count in sorted(categories.items()):
            print(f"  {category}: {count} scripts")

        print(f"\nOutput files saved to: {output_dir}")
        print(
            "Ready to pair with avatararts.org/python.html and github.com/ichoake/python",
        )


if __name__ == "__main__":
    # Check dependencies
    if not DEPENDENCIES_AVAILABLE:
        print("Warning: Some dependencies are missing. Install with:")
        print("pip install openai python-dotenv pandas")
        print("\nContinuing with limited functionality...")

    # Initialize analyzer
    analyzer = PythonRepoAnalyzer()

    # Run analysis
    analyzer.run_analysis()
