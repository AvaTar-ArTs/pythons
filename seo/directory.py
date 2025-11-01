
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_255 = 255
CONSTANT_333 = 333
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Directory Merger & Organizer for Steven Chaplinski's Portfolio
Merges content from seo-win, MySiTes, python-docs, and blog-versions
Creates comprehensive HTML-based organization system
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
import re

class DirectoryMergerOrganizer:
    def __init__(self):
        self.base_directories = [
            Path("/Users/steven/seo-win"),
            Path("/Users/steven/MySiTes"), 
            Path("/Users/steven/python-docs"),
            Path("/Users/steven/blog-versions")
        ]
        self.output_dir = Path("/Users/steven/Documents/python/merged_portfolio")
        self.html_output_dir = Path("/Users/steven/Documents/python/html_portfolio")
        
    def scan_directories(self):
        """Scan all directories and catalog content"""
        content_catalog = {
            "timestamp": datetime.now().isoformat(),
            "directories": {},
            "file_types": {},
            "total_files": 0,
            "total_size": 0
        }
        
        for directory in self.base_directories:
            if os.path.exists(directory):
                dir_info = self._scan_directory(directory)
                content_catalog["directories"][directory] = dir_info
                content_catalog["total_files"] += dir_info["file_count"]
                content_catalog["total_size"] += dir_info["total_size"]
                
                # Count file types
                for file_type, count in dir_info["file_types"].items():
                    if file_type not in content_catalog["file_types"]:
                        content_catalog["file_types"][file_type] = 0
                    content_catalog["file_types"][file_type] += count
        
        return content_catalog
    
    def _scan_directory(self, directory):
        """Scan individual directory and return info"""
        dir_info = {
            "path": directory,
            "name": os.path.basename(directory),
            "file_count": 0,
            "total_size": 0,
            "file_types": {},
            "subdirectories": [],
            "key_files": []
        }
        
        for root, dirs, files in os.walk(directory):
            # Add subdirectories
            for subdir in dirs:
                subdir_path = os.path.join(root, subdir)
                rel_path = os.path.relpath(subdir_path, directory)
                dir_info["subdirectories"].append(rel_path)
            
            # Process files
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, directory)
                
                # Get file info
                try:
                    file_size = os.path.getsize(file_path)
                    file_ext = os.path.splitext(file)[1].lower()
                    
                    dir_info["file_count"] += 1
                    dir_info["total_size"] += file_size
                    
                    # Count file types
                    if file_ext:
                        if file_ext not in dir_info["file_types"]:
                            dir_info["file_types"][file_ext] = 0
                        dir_info["file_types"][file_ext] += 1
                    
                    # Identify key files
                    if self._is_key_file(file, file_ext):
                        dir_info["key_files"].append({
                            "name": file,
                            "path": rel_path,
                            "size": file_size,
                            "extension": file_ext
                        })
                        
                except (OSError, IOError):
                    continue
        
        return dir_info
    
    def _is_key_file(self, filename, extension):
        """Identify key files based on name and extension"""
        key_patterns = [
            r'index\.html?',
            r'README\.md',
            r'package\.json',
            r'config\.',
            r'portfolio',
            r'resume',
            r'cv',
            r'analysis',
            r'strategy',
            r'documentation'
        ]
        
        key_extensions = ['.html', '.md', '.json', '.py', '.js', '.css']
        
        # Check filename patterns
        for pattern in key_patterns:
            if re.search(pattern, filename, re.IGNORECASE):
                return True
        
        # Check extensions
        if extension in key_extensions:
            return True
            
        return False
    
    def create_merged_structure(self, content_catalog):
        """Create merged directory structure"""
        # Create output directories
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.html_output_dir, exist_ok=True)
        
        # Create organized structure
        structure = {
            "portfolio": {
                "seo_analysis": [],
                "websites": [],
                "documentation": [],
                "blog_versions": [],
                "assets": []
            }
        }
        
        # Organize content by type
        for dir_path, dir_info in content_catalog["directories"].items():
            dir_name = dir_info["name"]
            
            if "seo-win" in dir_path:
                structure["portfolio"]["seo_analysis"].extend(dir_info["key_files"])
            elif "MySiTes" in dir_path:
                structure["portfolio"]["websites"].extend(dir_info["key_files"])
            elif "python-docs" in dir_path:
                structure["portfolio"]["documentation"].extend(dir_info["key_files"])
            elif "blog-versions" in dir_path:
                structure["portfolio"]["blog_versions"].extend(dir_info["key_files"])
        
        return structure
    
    def generate_html_portfolio(self, content_catalog, structure):
        """Generate comprehensive HTML portfolio"""
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Steven Chaplinski - Merged Portfolio & Content Hub</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #CONSTANT_333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 CONSTANT_100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: rgba(CONSTANT_255, CONSTANT_255, CONSTANT_255, 0.95);
            border-radius: 15px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            text-align: center;
        }}
        
        .header h1 {{
            color: #2c3e50;
            font-size: 3em;
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
            background: rgba(CONSTANT_255, CONSTANT_255, CONSTANT_255, 0.95);
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
        
        .section {{
            background: rgba(CONSTANT_255, CONSTANT_255, CONSTANT_255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }}
        
        .section h2 {{
            color: #2c3e50;
            font-size: 1.8em;
            margin-bottom: 20px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .directory-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .directory-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            border-left: 5px solid #667eea;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }}
        
        .directory-title {{
            color: #2c3e50;
            font-size: 1.3em;
            margin-bottom: 10px;
            font-weight: bold;
        }}
        
        .directory-path {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 15px;
        }}
        
        .directory-stats {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 1.2em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-desc {{
            font-size: 0.8em;
            color: #7f8c8d;
        }}
        
        .file-list {{
            list-style: none;
            padding: 0;
        }}
        
        .file-item {{
            background: white;
            margin: 5px 0;
            padding: 10px;
            border-radius: 5px;
            border-left: 3px solid #27ae60;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        
        .file-name {{
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .file-size {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        
        .file-extension {{
            color: #667eea;
            font-weight: bold;
        }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            color: white;
            font-size: 1.1em;
        }}
        
        .timestamp {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-top: 10px;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            
            .header h1 {{
                font-size: 2.5em;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .directory-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Steven Chaplinski</h1>
            <div style="color: #7f8c8d; font-size: 1.3em; margin-bottom: 20px;">
                Merged Portfolio & Content Hub
            </div>
            <div class="timestamp">Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{content_catalog['total_files']:,}</div>
                <div class="stat-label">Total Files Analyzed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(content_catalog['directories'])}</div>
                <div class="stat-label">Directories Merged</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(content_catalog['file_types'])}</div>
                <div class="stat-label">File Types</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{self._format_size(content_catalog['total_size'])}</div>
                <div class="stat-label">Total Size</div>
            </div>
        </div>"""
        
        # Add directory sections
        for dir_path, dir_info in content_catalog["directories"].items():
            dir_name = dir_info["name"]
            html_content += f"""
        <div class="section">
            <h2>📁 {dir_name}</h2>
            <div class="directory-card">
                <div class="directory-title">{dir_name}</div>
                <div class="directory-path">{dir_path}</div>
                <div class="directory-stats">
                    <div class="stat-item">
                        <div class="stat-value">{dir_info['file_count']:,}</div>
                        <div class="stat-desc">Files</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{self._format_size(dir_info['total_size'])}</div>
                        <div class="stat-desc">Size</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{len(dir_info['subdirectories'])}</div>
                        <div class="stat-desc">Subdirs</div>
                    </div>
                </div>
                <h4>Key Files:</h4>
                <ul class="file-list">"""
            
            for file_info in dir_info["key_files"][:10]:  # Show top 10 files
                html_content += f"""
                    <li class="file-item">
                        <div class="file-name">{file_info['name']}</div>
                        <div class="file-size">{self._format_size(file_info['size'])} • <span class="file-extension">{file_info['extension']}</span></div>
                    </li>"""
            
            if len(dir_info["key_files"]) > 10:
                html_content += f"""
                    <li class="file-item">
                        <div class="file-name">... and {len(dir_info['key_files']) - 10} more files</div>
                    </li>"""
            
            html_content += """
                </ul>
            </div>
        </div>"""
        
        html_content += """
        <div class="footer">
            <p>🚀 <strong>Merged Portfolio Complete!</strong></p>
            <p>All directories analyzed and organized into comprehensive HTML portfolio</p>
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
        while size_bytes >= CONSTANT_1024 and i < len(size_names) - 1:
            size_bytes /= CONSTANT_1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def copy_key_files(self, content_catalog):
        """Copy key files to merged directory"""
        for dir_path, dir_info in content_catalog["directories"].items():
            dir_name = dir_info["name"]
            target_dir = os.path.join(self.output_dir, dir_name)
            os.makedirs(target_dir, exist_ok=True)
            
            # Copy key files
            for file_info in dir_info["key_files"]:
                source_path = os.path.join(dir_path, file_info["path"])
                target_path = os.path.join(target_dir, file_info["name"])
                
                try:
                    # Create target directory if needed
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    shutil.copy2(source_path, target_path)
                except (OSError, IOError) as e:
                    logger.info(f"Error copying {source_path}: {e}")
    
    def generate_file_type_analysis(self, content_catalog):
        """Generate file type analysis HTML"""
        file_types = content_catalog["file_types"]
        sorted_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Type Analysis - Steven Chaplinski Portfolio</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #CONSTANT_333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 CONSTANT_100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            background: rgba(CONSTANT_255, CONSTANT_255, CONSTANT_255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            text-align: center;
        }}
        
        .header h1 {{
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .file-type-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }}
        
        .file-type-card {{
            background: rgba(CONSTANT_255, CONSTANT_255, CONSTANT_255, 0.95);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }}
        
        .file-extension {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .file-count {{
            font-size: 1.5em;
            font-weight: bold;
            color: #27ae60;
            margin-bottom: 5px;
        }}
        
        .file-percentage {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 File Type Analysis</h1>
            <p>Distribution of file types across all directories</p>
        </div>
        
        <div class="file-type-grid">"""
        
        total_files = sum(file_types.values())
        for ext, count in sorted_types:
            percentage = (count / total_files) * CONSTANT_100
            html_content += f"""
            <div class="file-type-card">
                <div class="file-extension">{ext or 'No Extension'}</div>
                <div class="file-count">{count:,}</div>
                <div class="file-percentage">{percentage:.1f}%</div>
            </div>"""
        
        html_content += """
        </div>
    </div>
</body>
</html>"""
        
        return html_content
    
    def run_merge_organization(self):
        """Run the complete merge and organization process"""
        logger.info("🔍 Scanning directories...")
        content_catalog = self.scan_directories()
        
        logger.info("📁 Creating merged structure...")
        structure = self.create_merged_structure(content_catalog)
        
        logger.info("🌐 Generating HTML portfolio...")
        html_content = self.generate_html_portfolio(content_catalog, structure)
        
        logger.info("📊 Generating file type analysis...")
        file_type_html = self.generate_file_type_analysis(content_catalog)
        
        logger.info("📋 Copying key files...")
        self.copy_key_files(content_catalog)
        
        # Save HTML files
        with open(os.path.join(self.html_output_dir, "merged_portfolio.html"), "w", encoding="utf-8") as f:
            f.write(html_content)
        
        with open(os.path.join(self.html_output_dir, "file_type_analysis.html"), "w", encoding="utf-8") as f:
            f.write(file_type_html)
        
        # Save JSON catalog
        with open(os.path.join(self.output_dir, "content_catalog.json"), "w", encoding="utf-8") as f:
            json.dump(content_catalog, f, indent=2)
        
        logger.info(f"✅ Merge complete!")
        logger.info(f"📁 Merged files: {self.output_dir}")
        logger.info(f"🌐 HTML portfolio: {self.html_output_dir}")
        logger.info(f"📊 Total files processed: {content_catalog['total_files']:,}")
        logger.info(f"📈 Total size: {self._format_size(content_catalog['total_size'])}")
        
        return content_catalog, structure

def main():
    merger = DirectoryMergerOrganizer()
    content_catalog, structure = merger.run_merge_organization()
    
    logger.info("\n🎯 Key Statistics:")
    for dir_path, dir_info in content_catalog["directories"].items():
        logger.info(f"  {dir_info['name']}: {dir_info['file_count']:,} files, {merger._format_size(dir_info['total_size'])}")
    
    logger.info(f"\n📈 Top file types:")
    sorted_types = sorted(content_catalog["file_types"].items(), key=lambda x: x[1], reverse=True)
    for ext, count in sorted_types[:10]:
        logger.info(f"  {ext or 'No Extension'}: {count:,} files")

if __name__ == "__main__":
    main()