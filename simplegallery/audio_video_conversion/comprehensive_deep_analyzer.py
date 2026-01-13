#!/usr/bin/env python3
"""Comprehensive Deep Analyzer for Steven Chaplinski's Complete Portfolio
Content-aware analysis of all directories with detailed HTML generation
"""

import os
import json
import shutil
import hashlib
import mimetypes
from datetime import datetime
from pathlib import Path
import re
from collections import defaultdict, Counter


class ComprehensiveDeepAnalyzer:
    def __init__(self):
        self.directories = [
            "/Users/steven/AvaTarArTs",
            "/Users/steven/clean",
            "/Users/steven/Documents",
            "/Users/steven/Downloads",
            "/Users/steven/Movies",
            "/Users/steven/Music",
            "/Users/steven/Pictures",
            "/Users/steven/python-docs",
            "/Users/steven/seo-win",
            "/Users/steven/SUNO",
            "/Users/steven/tehSiTes",
            "/Users/steven/my-empire",
        ]
        self.output_dir = "/Users/steven/Optimized"
        self.html_dir = os.path.join(self.output_dir, "html_analysis")
        self.data_dir = os.path.join(self.output_dir, "data")

        # Content analysis patterns
        self.skill_patterns = {
            "python": [r"\.py$", r"python", r"pandas", r"numpy", r"flask", r"django"],
            "web_dev": [r"\.html?$", r"\.css$", r"\.js$", r"react", r"vue", r"angular"],
            "ai_ml": [
                r"ai",
                r"machine.?learning",
                r"neural",
                r"tensorflow",
                r"pytorch",
                r"openai",
            ],
            "automation": [
                r"automation",
                r"script",
                r"workflow",
                r"pipeline",
                r"batch",
            ],
            "media": [
                r"\.mp4$",
                r"\.mp3$",
                r"\.jpg$",
                r"\.png$",
                r"video",
                r"audio",
                r"image",
            ],
            "data": [
                r"\.csv$",
                r"\.json$",
                r"\.sql$",
                r"data",
                r"analysis",
                r"analytics",
            ],
            "devops": [
                r"docker",
                r"kubernetes",
                r"ci/cd",
                r"deployment",
                r"infrastructure",
            ],
            "content": [
                r"\.md$",
                r"\.txt$",
                r"content",
                r"blog",
                r"writing",
                r"documentation",
            ],
        }

        self.project_patterns = {
            "ai_art": [
                r"avatar",
                r"art",
                r"dalle",
                r"midjourney",
                r"stable.?diffusion",
            ],
            "music": [r"music", r"suno", r"audio", r"song", r"lyrics", r"discography"],
            "video": [r"video", r"mp4", r"capcut", r"editing", r"production"],
            "automation": [r"automation", r"script", r"workflow", r"pipeline"],
            "web": [r"website", r"html", r"css", r"javascript", r"frontend"],
            "data": [r"analysis", r"csv", r"data", r"analytics", r"report"],
        }

    def deep_scan_directory(self, directory):
        """Perform deep content-aware analysis of a directory"""
        if not os.path.exists(directory):
            return None

        analysis = {
            "path": directory,
            "name": os.path.basename(directory),
            "scan_time": datetime.now().isoformat(),
            "file_count": 0,
            "total_size": 0,
            "file_types": Counter(),
            "skill_indicators": defaultdict(int),
            "project_indicators": defaultdict(int),
            "key_files": [],
            "subdirectories": [],
            "content_analysis": {
                "ai_art_projects": [],
                "music_projects": [],
                "video_projects": [],
                "automation_scripts": [],
                "web_projects": [],
                "data_analysis": [],
                "documentation": [],
            },
            "complexity_score": 0,
            "innovation_score": 0,
        }

        try:
            for root, dirs, files in os.walk(directory):
                # Add subdirectories
                for subdir in dirs:
                    subdir_path = os.path.join(root, subdir)
                    rel_path = os.path.relpath(subdir_path, directory)
                    analysis["subdirectories"].append(rel_path)

                # Analyze files
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, directory)

                    try:
                        file_size = os.path.getsize(file_path)
                        file_ext = os.path.splitext(file)[1].lower()

                        analysis["file_count"] += 1
                        analysis["total_size"] += file_size
                        analysis["file_types"][file_ext] += 1

                        # Content-aware analysis
                        self._analyze_file_content(file_path, file, analysis)

                        # Identify key files
                        if self._is_key_file(file, file_ext, file_size):
                            analysis["key_files"].append(
                                {
                                    "name": file,
                                    "path": rel_path,
                                    "size": file_size,
                                    "extension": file_ext,
                                    "mime_type": mimetypes.guess_type(file_path)[0],
                                },
                            )

                    except (OSError, UnicodeDecodeError):
                        continue

        except OSError:
            pass

        # Calculate complexity and innovation scores
        analysis["complexity_score"] = self._calculate_complexity_score(analysis)
        analysis["innovation_score"] = self._calculate_innovation_score(analysis)

        return analysis

    def _analyze_file_content(self, file_path, filename, analysis):
        """Analyze file content for skills and project indicators"""
        try:
            # Read file content for analysis
            if (
                os.path.getsize(file_path) < 10 * 1024 * 1024
            ):  # Skip files larger than 10MB
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read(50000)  # Read first 50KB

                    # Check for skill indicators
                    for skill, patterns in self.skill_patterns.items():
                        for pattern in patterns:
                            if re.search(pattern, content, re.IGNORECASE):
                                analysis["skill_indicators"][skill] += 1

                    # Check for project indicators
                    for project, patterns in self.project_patterns.items():
                        for pattern in patterns:
                            if re.search(pattern, content, re.IGNORECASE):
                                analysis["project_indicators"][project] += 1

                    # Categorize content
                    self._categorize_content(file_path, filename, content, analysis)

        except (OSError, UnicodeDecodeError):
            pass

    def _categorize_content(self, file_path, filename, content, analysis):
        """Categorize content into specific project types"""
        file_lower = filename.lower()
        content_lower = content.lower()

        # AI Art projects
        if any(
            keyword in file_lower
            for keyword in ["avatar", "art", "dalle", "midjourney", "stable"]
        ):
            analysis["content_analysis"]["ai_art_projects"].append(
                {
                    "file": filename,
                    "path": file_path,
                    "indicators": self._extract_keywords(
                        content_lower, ["ai", "art", "image", "generation", "prompt"],
                    ),
                },
            )

        # Music projects
        if any(
            keyword in file_lower
            for keyword in ["music", "suno", "audio", "song", "mp3"]
        ):
            analysis["content_analysis"]["music_projects"].append(
                {
                    "file": filename,
                    "path": file_path,
                    "indicators": self._extract_keywords(
                        content_lower, ["music", "audio", "song", "lyrics", "suno"],
                    ),
                },
            )

        # Video projects
        if any(
            keyword in file_lower for keyword in ["video", "mp4", "capcut", "editing"]
        ):
            analysis["content_analysis"]["video_projects"].append(
                {
                    "file": filename,
                    "path": file_path,
                    "indicators": self._extract_keywords(
                        content_lower, ["video", "editing", "production", "capcut"],
                    ),
                },
            )

        # Automation scripts
        if any(
            keyword in file_lower
            for keyword in ["script", "automation", "workflow", "pipeline"]
        ):
            analysis["content_analysis"]["automation_scripts"].append(
                {
                    "file": filename,
                    "path": file_path,
                    "indicators": self._extract_keywords(
                        content_lower, ["automation", "script", "workflow", "pipeline"],
                    ),
                },
            )

        # Web projects
        if any(
            keyword in file_lower for keyword in ["html", "css", "js", "website", "web"]
        ):
            analysis["content_analysis"]["web_projects"].append(
                {
                    "file": filename,
                    "path": file_path,
                    "indicators": self._extract_keywords(
                        content_lower, ["html", "css", "javascript", "website", "web"],
                    ),
                },
            )

        # Data analysis
        if any(
            keyword in file_lower
            for keyword in ["csv", "data", "analysis", "analytics"]
        ):
            analysis["content_analysis"]["data_analysis"].append(
                {
                    "file": filename,
                    "path": file_path,
                    "indicators": self._extract_keywords(
                        content_lower, ["data", "analysis", "csv", "analytics"],
                    ),
                },
            )

        # Documentation
        if any(
            keyword in file_lower for keyword in ["readme", "doc", "guide", "manual"]
        ):
            analysis["content_analysis"]["documentation"].append(
                {
                    "file": filename,
                    "path": file_path,
                    "indicators": self._extract_keywords(
                        content_lower, ["documentation", "guide", "manual", "readme"],
                    ),
                },
            )

    def _extract_keywords(self, content, keywords):
        """Extract keyword frequencies from content"""
        return {
            keyword: content.count(keyword)
            for keyword in keywords
            if keyword in content
        }

    def _is_key_file(self, filename, extension, size):
        """Identify key files based on name, extension, and size"""
        key_patterns = [
            r"index\.html?",
            r"README\.md",
            r"package\.json",
            r"config\.",
            r"portfolio",
            r"resume",
            r"cv",
            r"analysis",
            r"strategy",
            r"documentation",
            r"main\.py",
            r"app\.py",
            r"setup\.py",
        ]

        key_extensions = [".html", ".md", ".json", ".py", ".js", ".css", ".csv"]

        # Check filename patterns
        for pattern in key_patterns:
            if re.search(pattern, filename, re.IGNORECASE):
                return True

        # Check extensions
        if extension in key_extensions:
            return True

        # Check size (important files are usually not too large)
        if 1000 <= size <= 1000000:  # 1KB to 1MB
            return True

        return False

    def _calculate_complexity_score(self, analysis):
        """Calculate complexity score based on file diversity and content"""
        score = 0

        # File type diversity
        score += len(analysis["file_types"]) * 2

        # File count
        score += min(analysis["file_count"] / 100, 50)

        # Skill indicators
        score += sum(analysis["skill_indicators"].values()) * 0.5

        # Project diversity
        score += len(analysis["content_analysis"]) * 5

        return min(score, 100)

    def _calculate_innovation_score(self, analysis):
        """Calculate innovation score based on cutting-edge technologies"""
        score = 0

        # AI/ML indicators
        score += analysis["skill_indicators"]["ai_ml"] * 3

        # Automation indicators
        score += analysis["skill_indicators"]["automation"] * 2

        # Media processing
        score += analysis["skill_indicators"]["media"] * 1.5

        # Data analysis
        score += analysis["skill_indicators"]["data"] * 2

        # Project innovation
        for project_type, projects in analysis["content_analysis"].items():
            if projects:
                score += len(projects) * 2

        return min(score, 100)

    def generate_comprehensive_html(self, all_analyses):
        """Generate comprehensive HTML analysis"""
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Steven Chaplinski - Comprehensive Deep Analysis</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            text-align: center;
        }}
        
        .header h1 {{
            color: #2c3e50;
            font-size: 3.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .stat-label {{
            color: #7f8c8d;
            font-size: 1.1em;
        }}
        
        .directory-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }}
        
        .directory-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }}
        
        .directory-title {{
            color: #2c3e50;
            font-size: 1.8em;
            margin-bottom: 15px;
            font-weight: bold;
        }}
        
        .directory-path {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 20px;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .metric-card {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }}
        
        .metric-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .metric-label {{
            font-size: 0.8em;
            color: #7f8c8d;
        }}
        
        .skill-section {{
            margin-bottom: 20px;
        }}
        
        .skill-title {{
            color: #2c3e50;
            font-size: 1.2em;
            margin-bottom: 10px;
            font-weight: bold;
        }}
        
        .skill-bars {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .skill-bar {{
            background: #e9ecef;
            border-radius: 20px;
            padding: 5px 15px;
            font-size: 0.9em;
            color: #2c3e50;
        }}
        
        .skill-bar.high {{
            background: #d4edda;
            color: #155724;
        }}
        
        .skill-bar.medium {{
            background: #fff3cd;
            color: #856404;
        }}
        
        .project-section {{
            margin-bottom: 20px;
        }}
        
        .project-title {{
            color: #2c3e50;
            font-size: 1.2em;
            margin-bottom: 10px;
            font-weight: bold;
        }}
        
        .project-list {{
            list-style: none;
            padding: 0;
        }}
        
        .project-item {{
            background: #f8f9fa;
            margin: 5px 0;
            padding: 10px;
            border-radius: 5px;
            border-left: 3px solid #27ae60;
        }}
        
        .project-name {{
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .project-count {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        
        .scores {{
            display: flex;
            gap: 20px;
            margin-top: 20px;
        }}
        
        .score-card {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            flex: 1;
        }}
        
        .score-value {{
            font-size: 2em;
            font-weight: bold;
            color: #27ae60;
        }}
        
        .score-label {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            color: white;
            font-size: 1.1em;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            
            .header h1 {{
                font-size: 2.5em;
            }}
            
            .directory-grid {{
                grid-template-columns: 1fr;
            }}
            
            .metrics-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Steven Chaplinski</h1>
            <div style="color: #7f8c8d; font-size: 1.3em; margin-bottom: 20px;">
                Comprehensive Deep Analysis - Complete Portfolio
            </div>
            <div style="color: #7f8c8d; font-size: 0.9em;">
                Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </div>
        </div>"""

        # Calculate overall statistics
        total_files = sum(
            analysis["file_count"] for analysis in all_analyses.values() if analysis
        )
        total_size = sum(
            analysis["total_size"] for analysis in all_analyses.values() if analysis
        )
        total_directories = len([a for a in all_analyses.values() if a])

        html_content += f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_files:,}</div>
                <div class="stat-label">Total Files Analyzed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_directories}</div>
                <div class="stat-label">Directories Analyzed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{self._format_size(total_size)}</div>
                <div class="stat-label">Total Content Size</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(set().union(*[list(analysis['file_types'].keys()) for analysis in all_analyses.values() if analysis]))}</div>
                <div class="stat-label">File Types</div>
            </div>
        </div>"""

        # Generate directory cards
        for dir_name, analysis in all_analyses.items():
            if not analysis:
                continue

            html_content += f"""
        <div class="directory-card">
            <div class="directory-title">📁 {analysis['name']}</div>
            <div class="directory-path">{analysis['path']}</div>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">{analysis['file_count']:,}</div>
                    <div class="metric-label">Files</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{self._format_size(analysis['total_size'])}</div>
                    <div class="metric-label">Size</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{len(analysis['subdirectories'])}</div>
                    <div class="metric-label">Subdirs</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{len(analysis['file_types'])}</div>
                    <div class="metric-label">File Types</div>
                </div>
            </div>
            
            <div class="skill-section">
                <div class="skill-title">⚡ Skill Indicators</div>
                <div class="skill-bars">"""

            # Add skill bars
            for skill, count in sorted(
                analysis["skill_indicators"].items(), key=lambda x: x[1], reverse=True,
            ):
                if count > 0:
                    level = "high" if count > 10 else "medium" if count > 5 else ""
                    html_content += f'<span class="skill-bar {level}">{skill.title()}: {count}</span>'

            html_content += """
                </div>
            </div>
            
            <div class="project-section">
                <div class="project-title">🔧 Project Categories</div>
                <ul class="project-list">"""

            # Add project categories
            for category, projects in analysis["content_analysis"].items():
                if projects:
                    html_content += f"""
                    <li class="project-item">
                        <div class="project-name">{category.replace('_', ' ').title()}</div>
                        <div class="project-count">{len(projects)} projects</div>
                    </li>"""

            html_content += """
                </ul>
            </div>
            
            <div class="scores">
                <div class="score-card">
                    <div class="score-value">{analysis['complexity_score']:.0f}</div>
                    <div class="score-label">Complexity Score</div>
                </div>
                <div class="score-card">
                    <div class="score-value">{analysis['innovation_score']:.0f}</div>
                    <div class="score-label">Innovation Score</div>
                </div>
            </div>
        </div>"""

        html_content += """
        <div class="footer">
            <p>🚀 <strong>Comprehensive Deep Analysis Complete!</strong></p>
            <p>Content-aware analysis of complete portfolio with skill indicators and project categorization</p>
        </div>
    </div>
</body>
</html>"""

        return html_content

    def _format_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"

        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1

        return f"{size_bytes:.1f} {size_names[i]}"

    def run_comprehensive_analysis(self):
        """Run the complete comprehensive analysis"""
        print("🔍 Starting comprehensive deep analysis...")

        # Create output directories
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.html_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)

        # Analyze all directories
        all_analyses = {}
        for directory in self.directories:
            print(f"📁 Analyzing {directory}...")
            analysis = self.deep_scan_directory(directory)
            if analysis:
                all_analyses[directory] = analysis

        # Generate comprehensive HTML
        print("🌐 Generating comprehensive HTML analysis...")
        html_content = self.generate_comprehensive_html(all_analyses)

        # Save HTML file
        html_file = os.path.join(self.html_dir, "comprehensive_deep_analysis.html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Save JSON data
        json_file = os.path.join(self.data_dir, "comprehensive_analysis.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(all_analyses, f, indent=2, default=str)

        # Generate summary report
        self._generate_summary_report(all_analyses)

        print("✅ Comprehensive analysis complete!")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"🌐 HTML analysis: {html_file}")
        print(f"📊 JSON data: {json_file}")

        return all_analyses

    def _generate_summary_report(self, all_analyses):
        """Generate a summary report"""
        summary = {
            "analysis_date": datetime.now().isoformat(),
            "total_directories": len(all_analyses),
            "total_files": sum(
                analysis["file_count"] for analysis in all_analyses.values()
            ),
            "total_size": sum(
                analysis["total_size"] for analysis in all_analyses.values()
            ),
            "top_skills": Counter(),
            "top_projects": Counter(),
            "directory_summary": {},
        }

        # Aggregate skills and projects
        for analysis in all_analyses.values():
            for skill, count in analysis["skill_indicators"].items():
                summary["top_skills"][skill] += count

            for project, count in analysis["project_indicators"].items():
                summary["top_projects"][project] += count

            summary["directory_summary"][analysis["name"]] = {
                "files": analysis["file_count"],
                "size": analysis["total_size"],
                "complexity": analysis["complexity_score"],
                "innovation": analysis["innovation_score"],
            }

        # Save summary
        summary_file = os.path.join(self.data_dir, "analysis_summary.json")
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, default=str)

        print(f"📋 Summary report: {summary_file}")


def main():
    analyzer = ComprehensiveDeepAnalyzer()
    all_analyses = analyzer.run_comprehensive_analysis()

    print("\n🎯 Analysis Summary:")
    for dir_name, analysis in all_analyses.items():
        if analysis:
            print(
                f"  {analysis['name']}: {analysis['file_count']:,} files, {analyzer._format_size(analysis['total_size'])}, Complexity: {analysis['complexity_score']:.0f}, Innovation: {analysis['innovation_score']:.0f}",
            )


if __name__ == "__main__":
    main()
