#!/usr/bin/env python3
"""
ADVANCED BATCH VOLUME ANALYZER
Deep content-aware analysis using advanced APIs and Python intelligence
Integrates with advanced_toolkit and deep_env_volumes_analyzer
"""

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
                            value = value.strip().strip("'").strip("'")
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

import os
import json
import ast
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "advanced_toolkit"))

try:
    from advanced_toolkit.file_intelligence import FileAnalyzer
    from advanced_toolkit.config_manager import ConfigManager

    ADVANCED_TOOLKIT_AVAILABLE = True
except ImportError:
    FileAnalyzer = None
    ConfigManager = None
    ADVANCED_TOOLKIT_AVAILABLE = False

try:
    from PIL import Image

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class AdvancedPythonAnalyzer:
    """Advanced Python file analysis using AST and content intelligence"""

    def __init__(self):
        # API service patterns from deep_env_volumes_analyzer
        self.api_patterns = {
            "openai": ["openai", "gpt", "chatgpt", "davinci", "curie"],
            "anthropic": ["anthropic", "claude", "bedrock"],
            "google": ["google.generativeai", "gemini", "vertex", "google.ai"],
            "groq": ["groq"],
            "xai": ["xai", "grok"],
            "perplexity": ["perplexity"],
            "cohere": ["cohere"],
            "deepseek": ["deepseek"],
            "mistral": ["mistral"],
            "together": ["together"],
            "cerebras": ["cerebras"],
            "openrouter": ["openrouter"],
            "huggingface": ["huggingface", "transformers", "hf_"],
            "replicate": ["replicate"],
            "stability": ["stability", "stable_diffusion"],
            "elevenlabs": ["elevenlabs"],
            "suno": ["suno"],
            "make": ["make", "integromat"],
            "n8n": ["n8n"],
            "selenium": ["selenium", "webdriver"],
            "requests": ["requests", "httpx", "aiohttp"],
            "beautifulsoup": ["beautifulsoup", "bs4"],
            "pandas": ["pandas", "pd"],
            "numpy": ["numpy", "np"],
            "pillow": ["pillow", "pil", "image"],
            "ffmpeg": ["ffmpeg", "ffprobe"],
        }

        # Purpose detection patterns
        self.purpose_patterns = {
            "SEO/Content Optimization": [
                "seo",
                "optimize",
                "keyword",
                "trend",
                "trending",
                "aeo",
            ],
            "Content Extraction": ["extract", "scrape", "grab", "download", "crawl"],
            "AI Orchestration": ["orchestrat", "route", "multi", "llm", "model", "ai_"],
            "Audio Processing": [
                "audio",
                "music",
                "transcribe",
                "whisper",
                "ffmpeg",
                "mp3",
            ],
            "Image Processing": [
                "image",
                "photo",
                "gallery",
                "visual",
                "pil",
                "pillow",
            ],
            "Automation": ["automate", "workflow", "pipeline", "task", "job"],
            "CRM/Customer Management": [
                "customer",
                "retention",
                "churn",
                "lifetime",
                "crm",
            ],
            "Analysis/Intelligence": [
                "analyze",
                "analysis",
                "intelligence",
                "insight",
                "report",
            ],
            "YouTube/Video Content": [
                "youtube",
                "video",
                "description",
                "tags",
                "thumbnail",
            ],
            "File Management": [
                "file",
                "organize",
                "move",
                "copy",
                "rename",
                "duplicate",
            ],
            "Data Processing": ["data", "process", "transform", "clean", "merge"],
        }

    def analyze_python_file(self, filepath: Path) -> Dict[str, Any]:
        """Deep Python file analysis"""
        result = {
            "type": "python",
            "classes": [],
            "functions": [],
            "imports": [],
            "apis_used": [],
            "technologies": [],
            "purpose": [],
            "complexity": "low",
            "dependencies": [],
            "description": None,
            "main_functionality": None,
        }

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # AST parsing for structure
            try:
                tree = ast.parse(content)

                # Extract classes
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        methods = [
                            n.name for n in node.body if isinstance(n, ast.FunctionDef)
                        ]
                        result["classes"].append(
                            {
                                "name": node.name,
                                "methods": methods[:10],  # Limit
                                "bases": [self._ast_to_string(b) for b in node.bases][
                                    :5
                                ],
                            }
                        )

                    # Extract functions
                    elif isinstance(node, ast.FunctionDef):
                        args = [arg.arg for arg in node.args.args]
                        decorators = [
                            self._ast_to_string(d) for d in node.decorator_list
                        ]
                        result["functions"].append(
                            {
                                "name": node.name,
                                "args": args[:10],
                                "decorators": decorators[:5],
                            }
                        )

                    # Extract imports
                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            module = alias.name.split(".")[0]
                            result["imports"].append(module)
                            self._detect_api(module, result)
                            self._detect_technology(module, result)

                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            module = node.module.split(".")[0]
                            result["imports"].append(module)
                            self._detect_api(module, result)
                            self._detect_technology(module, result)

                # Extract docstrings for description
                if (
                    tree.body
                    and isinstance(tree.body[0], ast.Expr)
                    and isinstance(tree.body[0].value, ast.Str)
                ):
                    result["description"] = tree.body[0].value.s[:500]
                elif (
                    tree.body
                    and isinstance(tree.body[0], ast.Expr)
                    and isinstance(tree.body[0].value, ast.Constant)
                ):
                    result["description"] = str(tree.body[0].value.value)[:500]

            except SyntaxError:
                result["syntax_error"] = True

            # Content-based analysis
            content_lower = content.lower()

            # Detect purpose
            for purpose, patterns in self.purpose_patterns.items():
                if any(pattern in content_lower for pattern in patterns):
                    if purpose not in result["purpose"]:
                        result["purpose"].append(purpose)

            # Detect main functionality from function names
            main_functions = [
                f["name"]
                for f in result["functions"]
                if any(
                    keyword in f["name"].lower()
                    for keyword in [
                        "main",
                        "run",
                        "execute",
                        "process",
                        "analyze",
                        "generate",
                    ]
                )
            ]
            if main_functions:
                result["main_functionality"] = main_functions[0]

            # Complexity estimation
            total_elements = len(result["classes"]) + len(result["functions"])
            if total_elements > 20:
                result["complexity"] = "high"
            elif total_elements > 10:
                result["complexity"] = "medium"

            # Deduplicate
            result["imports"] = sorted(list(set(result["imports"])))
            result["apis_used"] = sorted(list(set(result["apis_used"])))
            result["technologies"] = sorted(list(set(result["technologies"])))
            result["purpose"] = result["purpose"] if result["purpose"] else ["unknown"]

        except Exception as e:
            result["error"] = str(e)

        return result

    def _detect_api(self, module: str, result: Dict):
        """Detect API services from module names"""
        module_lower = module.lower()
        for api_name, patterns in self.api_patterns.items():
            if any(pattern in module_lower for pattern in patterns):
                api_display = api_name.replace("_", " ").title()
                if api_display not in result["apis_used"]:
                    result["apis_used"].append(api_display)
                break

    def _detect_technology(self, module: str, result: Dict):
        """Detect technologies from module names"""
        tech_map = {
            "selenium": "Selenium (Browser Automation)",
            "requests": "HTTP Requests",
            "beautifulsoup": "Web Scraping",
            "pandas": "Data Analysis",
            "numpy": "Numerical Computing",
            "pillow": "Image Processing",
            "ffmpeg": "Media Processing",
        }

        module_lower = module.lower()
        for key, tech in tech_map.items():
            if key in module_lower:
                if tech not in result["technologies"]:
                    result["technologies"].append(tech)
                break

    def _ast_to_string(self, node) -> str:
        """Convert AST node to string"""
        try:
            if isinstance(node, ast.Name):
                return node.id
            elif isinstance(node, ast.Attribute):
                return f"{self._ast_to_string(node.value)}.{node.attr}"
            return str(node)
        except:
            return str(node)


class AdvancedBatchVolumeAnalyzer:
    """Advanced batch analyzer with deep content intelligence"""

    def __init__(self, max_files_per_dir: int = 100):
        self.max_files_per_dir = max_files_per_dir
        self.python_analyzer = AdvancedPythonAnalyzer()
        self.config_manager = ConfigManager() if ConfigManager else None

        # Statistics
        self.stats = {
            "files_analyzed": 0,
            "python_files": 0,
            "python_scripts_analyzed": 0,
            "apis_found": set(),
            "technologies_found": set(),
            "projects_found": [],
        }

        # Results
        self.results = {
            "volumes": {},
            "summary": {},
        }

    def analyze_volume(self, volume_path: str, max_depth: int = 5) -> Dict[str, Any]:
        """Analyze a single volume with advanced intelligence"""
        volume = Path(volume_path)

        if not volume.exists():
            return {"error": f"Volume not found: {volume_path}"}

        print(f"\n{'=' * 70}")
        print(f"🔍 ADVANCED ANALYSIS: {volume_path}")
        print(f"{'=' * 70}\n")

        volume_data = {
            "path": str(volume),
            "name": volume.name,
            "directories": {},
            "python_scripts": [],
            "projects": [],
            "apis_integrated": set(),
            "technologies": set(),
            "total_files": 0,
            "total_size": 0,
            "file_types": defaultdict(int),
            "intelligence": {},
        }

        # Step 1: Find all Python scripts recursively
        print("🔍 Step 1: Discovering Python scripts...")
        python_scripts = self._find_python_scripts(volume, max_depth)
        print(f"   Found {len(python_scripts)} Python scripts\n")

        # Step 2: Deep analyze Python scripts
        print("🔍 Step 2: Deep analyzing Python scripts...")
        for i, script_path in enumerate(
            python_scripts[:200], 1
        ):  # Limit to 200 scripts
            if i % 20 == 0:
                print(
                    f"   Progress: {i}/{min(200, len(python_scripts))} scripts analyzed..."
                )

            analysis = self.python_analyzer.analyze_python_file(script_path)
            if analysis:
                rel_path = str(script_path.relative_to(volume))
                script_info = {
                    "path": rel_path,
                    "name": script_path.name,
                    "analysis": analysis,
                }
                volume_data["python_scripts"].append(script_info)

                # Collect APIs and technologies
                if analysis.get("apis_used"):
                    volume_data["apis_integrated"].update(analysis["apis_used"])
                    self.stats["apis_found"].update(analysis["apis_used"])

                if analysis.get("technologies"):
                    volume_data["technologies"].update(analysis["technologies"])
                    self.stats["technologies_found"].update(analysis["technologies"])

                # Identify projects
                if analysis.get("purpose") and analysis["purpose"] != ["unknown"]:
                    volume_data["projects"].append(
                        {
                            "path": rel_path,
                            "name": script_path.name,
                            "purpose": analysis["purpose"],
                            "apis": analysis.get("apis_used", []),
                            "complexity": analysis.get("complexity", "low"),
                        }
                    )

        print(f"   ✅ Analyzed {len(volume_data['python_scripts'])} scripts\n")

        # Step 3: Analyze key directories
        print("🔍 Step 3: Analyzing key directories...")
        key_dirs = self._find_key_directories(volume, max_depth)
        print(f"   Found {len(key_dirs)} key directories\n")

        for i, dir_path in enumerate(key_dirs[:50], 1):
            rel_path = str(dir_path.relative_to(volume))
            print(f"   [{i}/{min(50, len(key_dirs))}] {rel_path[:60]}...")

            dir_analysis = self._analyze_directory(dir_path)
            if dir_analysis:
                volume_data["directories"][rel_path] = dir_analysis

        # Step 4: File statistics
        print("\n📊 Step 4: Collecting file statistics...")
        for root, dirs, files in os.walk(volume):
            depth = len(Path(root).relative_to(volume).parts)
            if depth > max_depth:
                dirs.clear()
                continue

            for file in files:
                filepath = Path(root) / file
                try:
                    volume_data["total_files"] += 1
                    volume_data["total_size"] += filepath.stat().st_size
                    ext = filepath.suffix.lower()
                    if ext:
                        volume_data["file_types"][ext] += 1
                except:
                    pass

        # Convert sets to lists
        volume_data["apis_integrated"] = sorted(list(volume_data["apis_integrated"]))
        volume_data["technologies"] = sorted(list(volume_data["technologies"]))

        # Intelligence summary
        volume_data["intelligence"] = {
            "total_python_scripts": len(volume_data["python_scripts"]),
            "unique_apis": len(volume_data["apis_integrated"]),
            "unique_technologies": len(volume_data["technologies"]),
            "projects_identified": len(volume_data["projects"]),
            "top_purposes": self._get_top_purposes(volume_data["python_scripts"]),
        }

        print("\n✅ Volume analysis complete!")
        print(f"   Total files: {volume_data['total_files']:,}")
        print(f"   Total size: {volume_data['total_size'] / (1024**3):.2f} GB")
        print(f"   Python scripts: {len(volume_data['python_scripts'])}")
        print(f"   APIs found: {len(volume_data['apis_integrated'])}")
        print(f"   Technologies: {len(volume_data['technologies'])}")
        print(f"   Projects: {len(volume_data['projects'])}")

        return volume_data

    def _find_python_scripts(self, volume: Path, max_depth: int) -> List[Path]:
        """Find all Python scripts recursively"""
        python_scripts = []

        for root, dirs, files in os.walk(volume):
            depth = len(Path(root).relative_to(volume).parts)
            if depth > max_depth:
                dirs.clear()
                continue

            # Skip common non-code directories
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".")
                and d not in ["__pycache__", "node_modules", ".git", "venv", "env"]
            ]

            for file in files:
                if file.endswith(".py"):
                    filepath = Path(root) / file
                    try:
                        if (
                            filepath.stat().st_size > 0
                            and filepath.stat().st_size < 5 * 1024 * 1024
                        ):  # < 5MB
                            python_scripts.append(filepath)
                    except:
                        pass

        return sorted(python_scripts)

    def _find_key_directories(self, volume: Path, max_depth: int) -> List[Path]:
        """Find important directories in home directory"""
        key_dirs = []

        priority_patterns = [
            ("**/pythons/**", 20),
            ("**/advanced_toolkit/**", 15),
            ("**/organize/**", 10),
            ("**/clean/**", 10),
            ("**/projects/**", 10),
            ("**/code/**", 8),
            ("**/scripts/**", 8),
            ("**/content/**", 8),
            ("**/docs*/**", 5),
            ("**/Documents/**", 5),
            ("**/Downloads/**", 3),
            ("**/Pictures/**", 3),
            ("**/Music/**", 3),
        ]

        for pattern, limit in priority_patterns:
            try:
                matches = list(volume.glob(pattern))
                key_dirs.extend(matches[:limit])
            except:
                pass

        # Also get top-level directories
        try:
            for item in volume.iterdir():
                if item.is_dir() and not item.name.startswith("."):
                    if item not in key_dirs:
                        key_dirs.append(item)
        except:
            pass

        return sorted(set(key_dirs), key=lambda x: str(x))[:100]

    def _analyze_directory(self, dir_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze directory contents"""
        if not dir_path.exists() or not dir_path.is_dir():
            return None

        dir_analysis = {
            "path": str(dir_path),
            "files": [],
            "python_files": [],
            "file_count": 0,
            "project_type": None,
            "technologies": [],
            "apis": [],
        }

        files_analyzed = 0
        for item in dir_path.iterdir():
            if files_analyzed >= self.max_files_per_dir:
                break

            if item.is_file():
                if item.suffix == ".py":
                    analysis = self.python_analyzer.analyze_python_file(item)
                    if analysis:
                        dir_analysis["python_files"].append(
                            {
                                "name": item.name,
                                "analysis": analysis,
                            }
                        )
                        if analysis.get("technologies"):
                            dir_analysis["technologies"].extend(
                                analysis["technologies"]
                            )
                        if analysis.get("apis_used"):
                            dir_analysis["apis"].extend(analysis["apis_used"])
                        if not dir_analysis["project_type"] and analysis.get("purpose"):
                            dir_analysis["project_type"] = analysis["purpose"][0]

                dir_analysis["files"].append(item.name)
                dir_analysis["file_count"] += 1
                files_analyzed += 1

        dir_analysis["technologies"] = sorted(list(set(dir_analysis["technologies"])))
        dir_analysis["apis"] = sorted(list(set(dir_analysis["apis"])))

        return dir_analysis

    def _get_top_purposes(self, python_scripts: List[Dict]) -> List[str]:
        """Get top purposes from Python scripts"""
        purpose_counts = defaultdict(int)
        for script in python_scripts:
            purposes = script.get("analysis", {}).get("purpose", [])
            for purpose in purposes:
                if purpose != "unknown":
                    purpose_counts[purpose] += 1

        return sorted(purpose_counts.items(), key=lambda x: x[1], reverse=True)[:10]


def main():
    """Main execution - analyze home directory in batches"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Advanced Batch Home Directory Analyzer"
    )
    parser.add_argument(
        "--target", default="~", help="Target directory to analyze (default: ~)"
    )
    parser.add_argument(
        "--max-scripts", type=int, default=200, help="Max Python scripts to analyze"
    )
    parser.add_argument("--max-depth", type=int, default=4, help="Max directory depth")
    parser.add_argument(
        "--files-per-dir", type=int, default=50, help="Max files per directory"
    )
    parser.add_argument(
        "--batch-size", type=int, default=10, help="Number of directories per batch"
    )

    args = parser.parse_args()

    # Expand target path
    target_path = Path(args.target).expanduser()

    if not target_path.exists():
        print(f"❌ Target directory not found: {target_path}")
        return

    print(f"🎯 Analyzing: {target_path}")
    print(f"   Max depth: {args.max_depth}")
    print(f"   Max scripts: {args.max_scripts}")
    print(f"   Files per dir: {args.files_per_dir}")
    print()

    analyzer = AdvancedBatchVolumeAnalyzer(max_files_per_dir=args.files_per_dir)

    try:
        # Limit Python scripts
        original_find = analyzer._find_python_scripts

        def limited_find(volume, max_depth):
            scripts = original_find(volume, max_depth)
            return scripts[: args.max_scripts]

        analyzer._find_python_scripts = limited_find

        # Analyze home directory
        home_data = analyzer.analyze_volume(str(target_path), max_depth=args.max_depth)

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = Path.home() / f"ADVANCED_HOME_ANALYSIS_{timestamp}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(home_data, f, indent=2, default=str)

        print(f"\n💾 Analysis saved: {output_file}")

        # Generate markdown report
        report_file = Path.home() / f"ADVANCED_HOME_REPORT_{timestamp}.md"
        generate_report({"home": home_data}, report_file, analyzer.stats)

        print(f"📝 Report saved: {report_file}")
        print("\n✅ Analysis complete!")

    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()


def generate_report(results: Dict, output_file: Path, stats: Dict):
    """Generate comprehensive markdown report"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 🔍 ADVANCED MULTI-VOLUME CONTENT-AWARE ANALYSIS\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## 📊 Executive Summary\n\n")
        f.write(f"- **Volumes Analyzed:** {len(results)}\n")
        f.write(
            f"- **Python Scripts Analyzed:** {stats.get('python_scripts_analyzed', 0)}\n"
        )
        f.write(f"- **Unique APIs Found:** {len(stats.get('apis_found', set()))}\n")
        f.write(
            f"- **Unique Technologies:** {len(stats.get('technologies_found', set()))}\n\n"
        )

        # Volume details
        f.write("## 📦 Volume Analysis\n\n")
        for volume_path, volume_data in results.items():
            if "error" in volume_data:
                f.write(f"### {volume_path}\n\n")
                f.write(f"❌ Error: {volume_data['error']}\n\n")
                continue

            f.write(f"### {volume_data.get('name', Path(volume_path).name)}\n\n")
            f.write(f"**Path:** `{volume_path}`\n\n")
            f.write(f"- **Total Files:** {volume_data.get('total_files', 0):,}\n")
            f.write(
                f"- **Total Size:** {volume_data.get('total_size', 0) / (1024**3):.2f} GB\n"
            )
            f.write(
                f"- **Python Scripts:** {len(volume_data.get('python_scripts', []))}\n"
            )
            f.write(
                f"- **APIs Integrated:** {len(volume_data.get('apis_integrated', []))}\n"
            )
            f.write(f"- **Technologies:** {len(volume_data.get('technologies', []))}\n")
            f.write(f"- **Projects:** {len(volume_data.get('projects', []))}\n\n")

            # APIs
            if volume_data.get("apis_integrated"):
                f.write("#### 🔌 APIs Integrated\n\n")
                for api in volume_data["apis_integrated"][:30]:
                    f.write(f"- {api}\n")
                f.write("\n")

            # Technologies
            if volume_data.get("technologies"):
                f.write("#### 🔧 Technologies\n\n")
                for tech in volume_data["technologies"][:30]:
                    f.write(f"- {tech}\n")
                f.write("\n")

            # Top Python Scripts
            if volume_data.get("python_scripts"):
                f.write("#### 🐍 Key Python Scripts\n\n")
                for script in volume_data["python_scripts"][:20]:
                    analysis = script.get("analysis", {})
                    f.write(f"**{script['name']}**\n")
                    f.write(f"- Path: `{script['path']}`\n")
                    if analysis.get("purpose"):
                        f.write(f"- Purpose: {', '.join(analysis['purpose'])}\n")
                    if analysis.get("apis_used"):
                        f.write(f"- APIs: {', '.join(analysis['apis_used'][:5])}\n")
                    if analysis.get("description"):
                        f.write(f"- Description: {analysis['description'][:200]}...\n")
                    f.write("\n")

            # Projects
            if volume_data.get("projects"):
                f.write("#### 🎯 Projects Identified\n\n")
                for proj in volume_data["projects"][:15]:
                    f.write(f"**{proj['name']}**\n")
                    f.write(f"- Path: `{proj['path']}`\n")
                    f.write(f"- Purpose: {', '.join(proj['purpose'])}\n")
                    if proj.get("apis"):
                        f.write(f"- APIs: {', '.join(proj['apis'][:5])}\n")
                    f.write(f"- Complexity: {proj.get('complexity', 'unknown')}\n\n")


if __name__ == "__main__":
    main()
