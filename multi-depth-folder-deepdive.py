#!/usr/bin/env python3
"""
Multi-Depth Folder Deep Dive Scanner
Comprehensive analysis of ~/pythons directory structure, patterns, and organization
"""

import os
# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)
from pathlib import Path as PathLib

def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")

load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass

import json
import csv
import hashlib
import re
import time
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import ast

# AI API imports
try:
    from openai import OpenAI
    HAVE_OPENAI = True
except ImportError:
    HAVE_OPENAI = False

try:
    from anthropic import Anthropic
    HAVE_ANTHROPIC = True
except ImportError:
    HAVE_ANTHROPIC = False

try:
    import google.generativeai as genai
    HAVE_GEMINI = True
except ImportError:
    HAVE_GEMINI = False


class MultiDepthFolderDeepDive:
    """Comprehensive multi-depth folder analysis"""
    
    def __init__(self, root_path: Path):
        self.root_path = Path(root_path).expanduser().resolve()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = {
            "scan_metadata": {
                "root_path": str(self.root_path),
                "timestamp": self.timestamp,
                "scanner_version": "1.0"
            },
            "directory_structure": {},
            "file_analysis": {},
            "code_patterns": {},
            "duplicates": {},
            "organization_issues": {},
            "statistics": {}
        }
        
        # Exclude patterns
        self.exclude_patterns = [
            ".git", ".ruff_cache", ".claude", ".context7", 
            ".aider.tags.cache.v4", "__pycache__", ".DS_Store",
            "node_modules", "site", "axolotl-main"
        ]
        
        # Initialize AI clients
        self.ai_clients = self._initialize_ai_clients()
        self.ai_enabled = any(self.ai_clients.values())
        
        # AI analysis cache
        self.ai_analysis_cache = {}
        
    def _initialize_ai_clients(self) -> Dict[str, any]:
        """Initialize available AI clients"""
        clients = {
            "openai": None,
            "anthropic": None,
            "gemini": None
        }
        
        # OpenAI
        if HAVE_OPENAI and os.getenv("OPENAI_API_KEY"):
            try:
                clients["openai"] = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                print("   ✓ OpenAI API initialized")
            except Exception as e:
                print(f"   ⚠️  OpenAI init failed: {e}")
        
        # Anthropic
        if HAVE_ANTHROPIC and os.getenv("ANTHROPIC_API_KEY"):
            try:
                clients["anthropic"] = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
                print("   ✓ Anthropic API initialized")
            except Exception as e:
                print(f"   ⚠️  Anthropic init failed: {e}")
        
        # Gemini
        if HAVE_GEMINI and os.getenv("GEMINI_API_KEY"):
            try:
                genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
                clients["gemini"] = genai.GenerativeModel("gemini-pro")
                print("   ✓ Gemini API initialized")
            except Exception as e:
                print(f"   ⚠️  Gemini init failed: {e}")
        
        return clients
    
    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded"""
        path_str = str(path)
        return any(exclude in path_str for exclude in self.exclude_patterns)
    
    def analyze_code_with_ai(self, file_path: Path, code_sample: str) -> Optional[Dict]:
        """Use AI to analyze code purpose, category, and patterns"""
        if not self.ai_enabled:
            return None
        
        # Check cache
        cache_key = str(file_path)
        if cache_key in self.ai_analysis_cache:
            return self.ai_analysis_cache[cache_key]
        
        try:
            # Try OpenAI first
            if self.ai_clients["openai"]:
                return self._analyze_with_openai(file_path, code_sample)
            # Then Anthropic
            elif self.ai_clients["anthropic"]:
                return self._analyze_with_anthropic(file_path, code_sample)
            # Then Gemini
            elif self.ai_clients["gemini"]:
                return self._analyze_with_gemini(file_path, code_sample)
        except Exception as e:
            print(f"   ⚠️  AI analysis failed for {file_path.name}: {e}")
            return None
    
    def _analyze_with_openai(self, file_path: Path, code_sample: str) -> Optional[Dict]:
        """Analyze code using OpenAI"""
        prompt = f"""Analyze this Python file and provide JSON response:

Filename: {file_path.name}
Path: {file_path.parent.name}

Code sample (first 2000 chars):
```python
{code_sample[:2000]}
```

Provide JSON:
{{
    "purpose": "One sentence describing primary purpose",
    "category": "One of: automation, ai-ml, content-creation, image-processing, audio-video, data-processing, social-media, web-scraping, utilities, api-integration, other",
    "key_features": ["feature1", "feature2", "feature3"],
    "technologies": ["tech1", "tech2"],
    "complexity": "beginner|intermediate|advanced|expert",
    "consolidation_candidate": true/false,
    "quality_score": 0.0-1.0,
    "suggestions": ["suggestion1", "suggestion2"]
}}"""
        
        response = self.ai_clients["openai"].chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert code analyzer. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        result = json.loads(response.choices[0].message.content)
        self.ai_analysis_cache[str(file_path)] = result
        return result
    
    def _analyze_with_anthropic(self, file_path: Path, code_sample: str) -> Optional[Dict]:
        """Analyze code using Anthropic Claude"""
        prompt = f"""Analyze this Python file and provide JSON response:

Filename: {file_path.name}
Path: {file_path.parent.name}

Code sample (first 2000 chars):
```python
{code_sample[:2000]}
```

Provide JSON:
{{
    "purpose": "One sentence describing primary purpose",
    "category": "One of: automation, ai-ml, content-creation, image-processing, audio-video, data-processing, social-media, web-scraping, utilities, api-integration, other",
    "key_features": ["feature1", "feature2", "feature3"],
    "technologies": ["tech1", "tech2"],
    "complexity": "beginner|intermediate|advanced|expert",
    "consolidation_candidate": true/false,
    "quality_score": 0.0-1.0,
    "suggestions": ["suggestion1", "suggestion2"]
}}"""
        
        response = self.ai_clients["anthropic"].messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = json.loads(response.content[0].text)
        self.ai_analysis_cache[str(file_path)] = result
        return result
    
    def _analyze_with_gemini(self, file_path: Path, code_sample: str) -> Optional[Dict]:
        """Analyze code using Google Gemini"""
        prompt = f"""Analyze this Python file and provide JSON response:

Filename: {file_path.name}
Path: {file_path.parent.name}

Code sample (first 2000 chars):
```python
{code_sample[:2000]}
```

Provide JSON:
{{
    "purpose": "One sentence describing primary purpose",
    "category": "One of: automation, ai-ml, content-creation, image-processing, audio-video, data-processing, social-media, web-scraping, utilities, api-integration, other",
    "key_features": ["feature1", "feature2", "feature3"],
    "technologies": ["tech1", "tech2"],
    "complexity": "beginner|intermediate|advanced|expert",
    "consolidation_candidate": true/false,
    "quality_score": 0.0-1.0,
    "suggestions": ["suggestion1", "suggestion2"]
}}"""
        
        response = self.ai_clients["gemini"].generate_content(prompt)
        result = json.loads(response.text)
        self.ai_analysis_cache[str(file_path)] = result
        return result
    
    def scan_directory_structure(self, max_depth: int = 10):
        """Scan directory structure at multiple depths"""
        print("📁 Scanning directory structure...")
        
        structure = {
            "by_depth": defaultdict(list),
            "by_type": defaultdict(int),
            "largest_dirs": [],
            "deepest_paths": []
        }
        
        total_files = 0
        total_dirs = 0
        depth_stats = defaultdict(int)
        
        for root, dirs, files in os.walk(self.root_path):
            root_path = Path(root)
            
            if self.should_exclude(root_path):
                continue
            
            # Calculate depth
            depth = len(root_path.relative_to(self.root_path).parts)
            if depth > max_depth:
                continue
            
            depth_stats[depth] += 1
            total_dirs += 1
            
            # Track by depth
            structure["by_depth"][depth].append({
                "path": str(root_path.relative_to(self.root_path)),
                "file_count": len(files),
                "dir_count": len(dirs),
                "size": sum((root_path / f).stat().st_size for f in files if (root_path / f).exists())
            })
            
            # Count file types
            for file in files:
                if self.should_exclude(root_path / file):
                    continue
                ext = Path(file).suffix.lower() or "no_extension"
                structure["by_type"][ext] += 1
                total_files += 1
        
        # Find largest directories
        dir_sizes = []
        for depth, dirs in structure["by_depth"].items():
            for dir_info in dirs:
                dir_sizes.append((dir_info["path"], dir_info["size"], depth))
        
        structure["largest_dirs"] = sorted(dir_sizes, key=lambda x: x[1], reverse=True)[:20]
        
        # Find deepest paths
        all_paths = []
        for depth, dirs in structure["by_depth"].items():
            for dir_info in dirs:
                all_paths.append((dir_info["path"], depth))
        structure["deepest_paths"] = sorted(all_paths, key=lambda x: x[1], reverse=True)[:20]
        
        structure["statistics"] = {
            "total_files": total_files,
            "total_dirs": total_dirs,
            "max_depth": max(depth_stats.keys()) if depth_stats else 0,
            "depth_distribution": dict(depth_stats)
        }
        
        self.results["directory_structure"] = structure
        print(f"   ✓ Found {total_files} files in {total_dirs} directories")
    
    def analyze_python_files(self):
        """Deep analysis of Python files"""
        print("🐍 Analyzing Python files...")
        
        analysis = {
            "file_count": 0,
            "total_lines": 0,
            "total_size": 0,
            "by_directory": defaultdict(lambda: {"count": 0, "lines": 0, "size": 0}),
            "imports": Counter(),
            "patterns": {
                "has_env_loading": 0,
                "has_constants": 0,
                "has_todos": 0,
                "has_docstrings": 0,
                "has_type_hints": 0,
                "has_logging": 0,
                "has_main": 0
            },
            "largest_files": [],
            "most_imports": [],
            "complexity_scores": [],
            "ai_analysis": {
                "analyzed_count": 0,
                "by_category": defaultdict(int),
                "consolidation_candidates": [],
                "quality_scores": [],
                "suggestions": defaultdict(list)
            }
        }
        
        python_files = []
        for root, dirs, files in os.walk(self.root_path):
            root_path = Path(root)
            if self.should_exclude(root_path):
                continue
            
            for file in files:
                if not file.endswith(".py"):
                    continue
                
                file_path = root_path / file
                if self.should_exclude(file_path):
                    continue
                
                python_files.append(file_path)
        
        print(f"   Processing {len(python_files)} Python files...")
        
        # AI analysis batch (sample top files)
        files_to_analyze = python_files[:100] if len(python_files) > 100 else python_files
        if self.ai_enabled:
            print(f"   🤖 AI analyzing {len(files_to_analyze)} files...")
        
        ai_results = {}
        if self.ai_enabled and files_to_analyze:
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {}
                for file_path in files_to_analyze:
                    try:
                        content = file_path.read_text(encoding="utf-8", errors="ignore")
                        future = executor.submit(self.analyze_code_with_ai, file_path, content)
                        futures[future] = file_path
                    except:
                        pass
                
                completed = 0
                for future in as_completed(futures):
                    file_path = futures[future]
                    try:
                        result = future.result()
                        if result:
                            ai_results[str(file_path)] = result
                            completed += 1
                            if completed % 10 == 0:
                                print(f"      Analyzed {completed}/{len(files_to_analyze)} files...")
                        time.sleep(0.1)  # Rate limiting
                    except Exception as e:
                        pass
                print(f"   ✓ AI analyzed {completed} files")
        
        for file_path in python_files:
            try:
                rel_path = str(file_path.relative_to(self.root_path))
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                lines = content.splitlines()
                line_count = len(lines)
                file_size = file_path.stat().st_size
                
                analysis["file_count"] += 1
                analysis["total_lines"] += line_count
                analysis["total_size"] += file_size
                
                # Directory stats
                dir_name = str(file_path.parent.relative_to(self.root_path)) or "root"
                analysis["by_directory"][dir_name]["count"] += 1
                analysis["by_directory"][dir_name]["lines"] += line_count
                analysis["by_directory"][dir_name]["size"] += file_size
                
                # Pattern detection
                if "load_env_d" in content or ".env.d" in content:
                    analysis["patterns"]["has_env_loading"] += 1
                if "CONSTANT_" in content:
                    analysis["patterns"]["has_constants"] += 1
                if "TODO" in content or "FIXME" in content:
                    analysis["patterns"]["has_todos"] += 1
                if '"""' in content or "'''" in content:
                    analysis["patterns"]["has_docstrings"] += 1
                if "->" in content or ": int" in content or ": str" in content:
                    analysis["patterns"]["has_type_hints"] += 1
                if "import logging" in content or "from logging" in content:
                    analysis["patterns"]["has_logging"] += 1
                if "__main__" in content or 'if __name__ == "__main__"' in content:
                    analysis["patterns"]["has_main"] += 1
                
                # Extract imports
                import_pattern = r'^(?:from\s+(\S+)|import\s+(\S+))'
                for line in lines:
                    match = re.match(import_pattern, line.strip())
                    if match:
                        module = match.group(1) or match.group(2)
                        if module:
                            analysis["imports"][module.split(".")[0]] += 1
                
                # Track largest files
                analysis["largest_files"].append((rel_path, line_count, file_size))
                
                # Add AI analysis if available
                if str(file_path) in ai_results:
                    ai_data = ai_results[str(file_path)]
                    analysis["ai_analysis"]["analyzed_count"] += 1
                    analysis["ai_analysis"]["by_category"][ai_data.get("category", "other")] += 1
                    
                    if ai_data.get("consolidation_candidate", False):
                        analysis["ai_analysis"]["consolidation_candidates"].append({
                            "file": rel_path,
                            "purpose": ai_data.get("purpose", ""),
                            "category": ai_data.get("category", "other")
                        })
                    
                    quality = ai_data.get("quality_score", 0.5)
                    analysis["ai_analysis"]["quality_scores"].append(quality)
                    
                    for suggestion in ai_data.get("suggestions", []):
                        analysis["ai_analysis"]["suggestions"][suggestion].append(rel_path)
                
            except Exception as e:
                print(f"   ⚠️  Error analyzing {file_path}: {e}")
        
        # Sort and limit
        analysis["largest_files"] = sorted(analysis["largest_files"], key=lambda x: x[2], reverse=True)[:30]
        analysis["most_imports"] = analysis["imports"].most_common(30)
        
        # Convert defaultdict to dict
        analysis["by_directory"] = dict(sorted(
            analysis["by_directory"].items(),
            key=lambda x: x[1]["count"],
            reverse=True
        )[:30])
        
        # Process AI analysis results
        if analysis["ai_analysis"]["analyzed_count"] > 0:
            analysis["ai_analysis"]["by_category"] = dict(analysis["ai_analysis"]["by_category"])
            analysis["ai_analysis"]["avg_quality"] = sum(analysis["ai_analysis"]["quality_scores"]) / len(analysis["ai_analysis"]["quality_scores"]) if analysis["ai_analysis"]["quality_scores"] else 0
            analysis["ai_analysis"]["suggestions"] = dict(analysis["ai_analysis"]["suggestions"])
        
        self.results["file_analysis"] = analysis
        ai_msg = f" (🤖 AI analyzed {analysis['ai_analysis']['analyzed_count']})" if analysis['ai_analysis']['analyzed_count'] > 0 else ""
        print(f"   ✓ Analyzed {analysis['file_count']} Python files ({analysis['total_lines']:,} lines){ai_msg}")
    
    def find_duplicates(self):
        """Find duplicate and similar files"""
        print("🔍 Finding duplicates and similar files...")
        
        duplicates = {
            "exact_duplicates": [],
            "similar_names": defaultdict(list),
            "similar_content": []
        }
        
        file_hashes = defaultdict(list)
        file_names = defaultdict(list)
        
        for root, dirs, files in os.walk(self.root_path):
            root_path = Path(root)
            if self.should_exclude(root_path):
                continue
            
            for file in files:
                file_path = root_path / file
                if self.should_exclude(file_path) or not file_path.is_file():
                    continue
                
                try:
                    # Hash file content
                    file_hash = hashlib.md5(file_path.read_bytes()).hexdigest()
                    rel_path = str(file_path.relative_to(self.root_path))
                    
                    file_hashes[file_hash].append(rel_path)
                    
                    # Group by similar names
                    base_name = file.lower().replace("_", "").replace("-", "")
                    file_names[base_name].append(rel_path)
                    
                except Exception as e:
                    pass
        
        # Find exact duplicates
        for file_hash, paths in file_hashes.items():
            if len(paths) > 1:
                duplicates["exact_duplicates"].append({
                    "hash": file_hash,
                    "files": paths,
                    "count": len(paths)
                })
        
        # Find similar names
        for base_name, paths in file_names.items():
            if len(paths) > 1:
                duplicates["similar_names"][base_name] = paths
        
        # Sort by count
        duplicates["exact_duplicates"] = sorted(
            duplicates["exact_duplicates"],
            key=lambda x: x["count"],
            reverse=True
        )[:20]
        
        duplicates["similar_names"] = {
            k: v for k, v in sorted(
                duplicates["similar_names"].items(),
                key=lambda x: len(x[1]),
                reverse=True
            )[:30] if len(v) > 1
        }
        
        self.results["duplicates"] = duplicates
        print(f"   ✓ Found {len(duplicates['exact_duplicates'])} duplicate groups")
    
    def identify_organization_issues(self):
        """Identify organization and structure issues"""
        print("🔧 Identifying organization issues...")
        
        issues = {
            "root_level_clutter": [],
            "deeply_nested": [],
            "inconsistent_naming": [],
            "orphaned_files": [],
            "potential_consolidation": []
        }
        
        # Root level files
        root_files = [f.name for f in self.root_path.iterdir() if f.is_file() and f.suffix == ".py"]
        if len(root_files) > 50:
            issues["root_level_clutter"] = {
                "count": len(root_files),
                "files": sorted(root_files)[:20]
            }
        
        # Deeply nested files
        for root, dirs, files in os.walk(self.root_path):
            root_path = Path(root)
            if self.should_exclude(root_path):
                continue
            
            depth = len(root_path.relative_to(self.root_path).parts)
            if depth > 5:
                for file in files:
                    if file.endswith(".py"):
                        issues["deeply_nested"].append({
                            "path": str((root_path / file).relative_to(self.root_path)),
                            "depth": depth
                        })
        
        issues["deeply_nested"] = sorted(issues["deeply_nested"], key=lambda x: x["depth"], reverse=True)[:20]
        
        # Find similar files that could be consolidated
        transcribe_files = []
        for root, dirs, files in os.walk(self.root_path / "transcribe"):
            root_path = Path(root)
            if self.should_exclude(root_path):
                continue
            for file in files:
                if file.endswith(".py") and file not in ["audio_transcriber.py", "transcript_analyzer.py", "batch_processor.py"]:
                    transcribe_files.append(str((root_path / file).relative_to(self.root_path)))
        
        if len(transcribe_files) > 10:
            issues["potential_consolidation"].append({
                "directory": "transcribe",
                "files": transcribe_files,
                "consolidated": ["audio_transcriber.py", "transcript_analyzer.py", "batch_processor.py"],
                "recommendation": "Archive redundant files"
            })
        
        self.results["organization_issues"] = issues
        print(f"   ✓ Identified {len(issues['root_level_clutter'])} organization issues")
    
    def generate_statistics(self):
        """Generate overall statistics"""
        print("📊 Generating statistics...")
        
        stats = {
            "total_files": 0,
            "total_dirs": 0,
            "total_size": 0,
            "python_files": self.results["file_analysis"].get("file_count", 0),
            "python_lines": self.results["file_analysis"].get("total_lines", 0),
            "file_types": {},
            "directory_distribution": {},
            "patterns_summary": self.results["file_analysis"].get("patterns", {}),
            "top_imports": [{"module": k, "count": v} for k, v in self.results["file_analysis"].get("most_imports", [])[:10]]
        }
        
        # Count all files
        for root, dirs, files in os.walk(self.root_path):
            root_path = Path(root)
            if self.should_exclude(root_path):
                continue
            
            stats["total_dirs"] += 1
            for file in files:
                file_path = root_path / file
                if self.should_exclude(file_path):
                    continue
                
                stats["total_files"] += 1
                try:
                    stats["total_size"] += file_path.stat().st_size
                    ext = file_path.suffix.lower() or "no_extension"
                    stats["file_types"][ext] = stats["file_types"].get(ext, 0) + 1
                except:
                    pass
        
        self.results["statistics"] = stats
        print(f"   ✓ Generated statistics")
    
    def save_results(self):
        """Save results to JSON and CSV"""
        print("💾 Saving results...")
        
        output_dir = self.root_path / f"MULTI_DEPTH_ANALYSIS_{self.timestamp}"
        output_dir.mkdir(exist_ok=True)
        
        # Save JSON
        json_path = output_dir / "DEEP_DIVE_ANALYSIS.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, default=str)
        
        # Save CSV summaries
        # Directory structure
        csv_path = output_dir / "DIRECTORY_STRUCTURE.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Depth", "Path", "File Count", "Dir Count", "Size (bytes)"])
            for depth, dirs in self.results["directory_structure"]["by_depth"].items():
                for dir_info in dirs[:50]:  # Limit rows
                    writer.writerow([
                        depth,
                        dir_info["path"],
                        dir_info["file_count"],
                        dir_info["dir_count"],
                        dir_info["size"]
                    ])
        
        # File analysis
        csv_path = output_dir / "FILE_ANALYSIS.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Directory", "File Count", "Total Lines", "Total Size (bytes)"])
            for dir_name, stats in list(self.results["file_analysis"]["by_directory"].items())[:50]:
                writer.writerow([dir_name, stats["count"], stats["lines"], stats["size"]])
        
        # Duplicates
        csv_path = output_dir / "DUPLICATES.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Type", "Hash/Pattern", "Files", "Count"])
            for dup in self.results["duplicates"]["exact_duplicates"][:20]:
                writer.writerow(["exact", dup["hash"], "; ".join(dup["files"]), dup["count"]])
        
        # Generate summary report
        self.generate_summary_report(output_dir)
        
        print(f"   ✓ Results saved to {output_dir}")
        return output_dir
    
    def generate_summary_report(self, output_dir: Path):
        """Generate human-readable summary report"""
        report_path = output_dir / "SUMMARY_REPORT.md"
        
        stats = self.results["statistics"]
        file_analysis = self.results["file_analysis"]
        dir_structure = self.results["directory_structure"]
        duplicates = self.results["duplicates"]
        issues = self.results["organization_issues"]
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# Multi-Depth Folder Deep Dive Report\n\n")
            f.write(f"**Generated:** {self.timestamp}\n")
            f.write(f"**Root Path:** {self.root_path}\n\n")
            
            f.write("## 📊 Overall Statistics\n\n")
            f.write(f"- **Total Files:** {stats['total_files']:,}\n")
            f.write(f"- **Total Directories:** {stats['total_dirs']:,}\n")
            f.write(f"- **Total Size:** {stats['total_size'] / (1024*1024):.2f} MB\n")
            f.write(f"- **Python Files:** {stats['python_files']:,}\n")
            f.write(f"- **Python Lines:** {stats['python_lines']:,}\n")
            f.write(f"- **Max Depth:** {dir_structure['statistics']['max_depth']}\n\n")
            
            f.write("## 🐍 Python File Analysis\n\n")
            f.write(f"- **Files with Environment Loading:** {file_analysis['patterns']['has_env_loading']}\n")
            f.write(f"- **Files with CONSTANT_ placeholders:** {file_analysis['patterns']['has_constants']}\n")
            f.write(f"- **Files with TODO/FIXME:** {file_analysis['patterns']['has_todos']}\n")
            f.write(f"- **Files with Docstrings:** {file_analysis['patterns']['has_docstrings']}\n")
            f.write(f"- **Files with Type Hints:** {file_analysis['patterns']['has_type_hints']}\n")
            f.write(f"- **Files with Logging:** {file_analysis['patterns']['has_logging']}\n")
            f.write(f"- **Files with __main__:** {file_analysis['patterns']['has_main']}\n\n")
            
            f.write("## 📁 Top Directories by File Count\n\n")
            for dir_name, dir_stats in list(file_analysis["by_directory"].items())[:10]:
                f.write(f"- **{dir_name}:** {dir_stats['count']} files, {dir_stats['lines']:,} lines\n")
            
            f.write("\n## 🔍 Top Imports\n\n")
            for imp in file_analysis["most_imports"][:15]:
                f.write(f"- `{imp[0]}`: {imp[1]} files\n")
            
            f.write("\n## 📦 Largest Python Files\n\n")
            for file_path, lines, size in file_analysis["largest_files"][:15]:
                f.write(f"- **{file_path}:** {lines:,} lines, {size / 1024:.1f} KB\n")
            
            f.write("\n## 🔄 Duplicates Found\n\n")
            f.write(f"- **Exact Duplicates:** {len(duplicates['exact_duplicates'])} groups\n")
            if duplicates['exact_duplicates']:
                f.write("\nTop duplicate groups:\n")
                for dup in duplicates['exact_duplicates'][:5]:
                    f.write(f"- {dup['count']} copies: {', '.join(dup['files'][:3])}\n")
            
            f.write("\n## ⚠️ Organization Issues\n\n")
            if issues.get("root_level_clutter"):
                f.write(f"- **Root Level Clutter:** {issues['root_level_clutter']['count']} Python files in root\n")
            if issues.get("deeply_nested"):
                f.write(f"- **Deeply Nested Files:** {len(issues['deeply_nested'])} files at depth > 5\n")
            if issues.get("potential_consolidation"):
                for consol in issues['potential_consolidation']:
                    f.write(f"- **{consol['directory']}:** {len(consol['files'])} files could be archived\n")
            
            f.write("\n## 📈 Depth Distribution\n\n")
            for depth, count in sorted(dir_structure['statistics']['depth_distribution'].items()):
                f.write(f"- **Depth {depth}:** {count} directories\n")
    
    def run_full_scan(self):
        """Run complete deep dive scan"""
        print("🚀 Starting Multi-Depth Folder Deep Dive Scan")
        print("=" * 60)
        print(f"Root: {self.root_path}\n")
        
        if self.ai_enabled:
            print("🤖 AI-Powered Analysis: ENABLED")
            print(f"   Available APIs: {', '.join([k for k, v in self.ai_clients.items() if v])}\n")
        else:
            print("⚠️  AI-Powered Analysis: DISABLED (no API keys found)\n")
        
        self.scan_directory_structure(max_depth=15)
        self.analyze_python_files()
        self.find_duplicates()
        self.identify_organization_issues()
        self.generate_statistics()
        
        output_dir = self.save_results()
        
        print("\n" + "=" * 60)
        print("✅ Deep Dive Scan Complete!")
        print(f"📁 Results saved to: {output_dir}")
        if self.ai_enabled:
            ai_count = self.results["file_analysis"].get("ai_analysis", {}).get("analyzed_count", 0)
            print(f"🤖 AI analyzed {ai_count} files")
        print("=" * 60)
        
        return output_dir


if __name__ == "__main__":
    scanner = MultiDepthFolderDeepDive("~/pythons")
    scanner.run_full_scan()
