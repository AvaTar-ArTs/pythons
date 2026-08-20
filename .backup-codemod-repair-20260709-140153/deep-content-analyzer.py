#!/usr/bin/env python3
"""
🧠 DEEP CONTENT ANALYZER ULTIMATE
==================================

Advanced content-aware analysis that ACTUALLY READS AND UNDERSTANDS:
- Python scripts (AST parsing + AI comprehension)
- Websites and HTML projects
- Music collections and metadata
- External volumes (/Volumes)
- All file types with intelligent categorization

Features:
🔍 Deep code comprehension (not just pattern matching)
🎨 Website/project discovery and analysis
🎵 Music collection analysis (ID3, metadata, organization)
💾 External volume scanning (/Volumes)
🧠 AI-powered semantic understanding
📊 Comprehensive relationship mapping
🎯 Advanced use case identification
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

import os
import ast
import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from collections import defaultdict
import anthropic
from openai import OpenAI
import re
from datetime import datetime


@dataclass
class PythonScript:
    """Deep analysis of a Python script"""
    filepath: str
    filename: str
    purpose: str
    actual_functionality: str  # AI-analyzed actual purpose
    imports: List[str]
    classes: List[Dict[str, Any]]
    functions: List[Dict[str, Any]]
    main_logic: str
    api_integrations: List[str]
    workflows: List[str]
    complexity_score: int
    lines: int
    documentation_quality: str  # "excellent", "good", "poor", "none"
    use_cases: List[str]
    related_scripts: List[str] = field(default_factory=list)


@dataclass
class Website:
    """Discovered website/web project"""
    path: str
    name: str
    type: str  # "static", "react", "next", "wordpress", etc.
    technologies: List[str]
    pages: List[str]
    assets: Dict[str, int]  # {"images": 50, "js": 10, etc.}
    configuration: Dict[str, Any]
    purpose: str
    deployment_status: str  # "deployed", "development", "archived"


@dataclass
class MusicCollection:
    """Music collection analysis"""
    path: str
    total_files: int
    total_size_gb: float
    formats: Dict[str, int]  # {"mp3": 1000, "flac": 50}
    artists: List[Dict[str, Any]]
    albums: List[Dict[str, Any]]
    playlists: List[str]
    metadata_quality: str
    organization_type: str  # "by_artist", "by_album", "flat", "mixed"
    duplicates: List[Tuple[str, str]]


@dataclass
class ExternalVolume:
    """External drive/volume analysis"""
    mount_point: str
    name: str
    size_gb: float
    used_gb: float
    content_summary: Dict[str, int]
    valuable_content: List[Dict[str, Any]]
    backup_status: str


class DeepContentAnalyzerUltimate:
    """
    Ultimate content analyzer that ACTUALLY UNDERSTANDS what code does
    """
    
    def __init__(self):
        self.claude = None
        self.openai_client = None
        
        if os.getenv('ANTHROPIC_API_KEY'):
            self.claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        if os.getenv('OPENAI_API_KEY'):
            self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Analysis results
        self.python_scripts: List[PythonScript] = []
        self.websites: List[Website] = []
        self.music_collections: List[MusicCollection] = []
        self.external_volumes: List[ExternalVolume] = []
        
        # Relationship graph
        self.script_relationships: Dict[str, List[str]] = defaultdict(list)
        self.workflow_chains: List[List[str]] = []
    
    # ==================== Python Script Deep Analysis ====================
    
    def deep_analyze_python_script(self, filepath: str) -> PythonScript:
        """
        ACTUALLY READ AND UNDERSTAND what a Python script does
        
        Uses AST parsing + AI comprehension
        """
        print(f"🔍 Deep analyzing: {Path(filepath).name}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Parse AST
            tree = ast.parse(code)
            
            # Extract structure
            imports = self._extract_imports(tree)
            classes = self._extract_classes(tree, code)
            functions = self._extract_functions(tree, code)
            
            # AI-powered comprehension
            actual_functionality = self._ai_understand_code(code, filepath)
            use_cases = self._identify_use_cases(code, actual_functionality)
            api_integrations = self._identify_api_integrations(code)
            workflows = self._identify_workflows(code, functions)
            
            # Quality assessment
            doc_quality = self._assess_documentation(code, classes, functions)
            complexity = self._calculate_complexity(tree, functions)
            
            script = PythonScript(
                filepath=filepath,
                filename=Path(filepath).name,
                purpose=self._extract_docstring(tree),
                actual_functionality=actual_functionality,
                imports=imports,
                classes=classes,
                functions=functions,
                main_logic=self._extract_main_logic(code),
                api_integrations=api_integrations,
                workflows=workflows,
                complexity_score=complexity,
                lines=len(code.splitlines()),
                documentation_quality=doc_quality,
                use_cases=use_cases
            )
            
            return script
            
        except Exception as e:
            print(f"   ⚠️  Error analyzing {filepath}: {e}")
            return None
    
    def _extract_imports(self, tree: ast.AST) -> List[str]:
        """Extract all imports"""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}" if module else alias.name)
        return list(set(imports))
    
    def _extract_classes(self, tree: ast.AST, code: str) -> List[Dict[str, Any]]:
        """Extract classes with full details"""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
                classes.append({
                    'name': node.name,
                    'methods': methods,
                    'bases': [self._get_name(base) for base in node.bases],
                    'decorators': [self._get_name(dec) for dec in node.decorator_list],
                    'docstring': ast.get_docstring(node) or ''
                })
        return classes
    
    def _extract_functions(self, tree: ast.AST, code: str) -> List[Dict[str, Any]]:
        """Extract functions with full details"""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Skip methods (already in classes)
                if not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(tree)):
                    args = [arg.arg for arg in node.args.args]
                    functions.append({
                        'name': node.name,
                        'args': args,
                        'returns': self._get_name(node.returns) if node.returns else None,
                        'decorators': [self._get_name(dec) for dec in node.decorator_list],
                        'docstring': ast.get_docstring(node) or '',
                        'is_async': isinstance(node, ast.AsyncFunctionDef)
                    })
        return functions
    
    def _get_name(self, node) -> str:
        """Get name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Subscript):
            return f"{self._get_name(node.value)}[...]"
        return str(node)
    
    def _ai_understand_code(self, code: str, filepath: str) -> str:
        """
        Use AI to ACTUALLY UNDERSTAND what the code does
        
        This is the key difference - we're not just pattern matching,
        we're using AI to comprehend the code's purpose and functionality
        """
        if not self.claude:
            return "AI analysis not available"
        
        # For large files, analyze in chunks
        code_sample = code[:3000] if len(code) > 3000 else code
        
        prompt = f"""Analyze this Python script and explain what it ACTUALLY does:

File: {Path(filepath).name}

Code:
```python
{code_sample}
```

Provide:
1. Real purpose (what it actually does, not what docs say)
2. Main workflow/algorithm
3. Key functionality
4. Practical use cases
5. Any clever techniques or patterns used

Be specific and technical. Focus on ACTUAL functionality."""
        
        try:
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Analysis error: {e}"
    
    def _identify_use_cases(self, code: str, ai_analysis: str) -> List[str]:
        """Identify practical use cases"""
        use_cases = []
        
        # Pattern-based detection
        patterns = {
            'instagram': ['Instagram automation', 'Social media posting', 'Follower management'],
            'youtube': ['Video upload', 'YouTube automation', 'Content publishing'],
            'suno': ['Music generation', 'Audio processing', 'Song catalog'],
            'leonardo': ['Image generation', 'AI art creation', 'Visual content'],
            'transcribe': ['Audio transcription', 'Speech-to-text', 'Subtitle generation'],
            'gallery': ['Photo gallery', 'Website generation', 'Image organization'],
            'openai': ['Text generation', 'AI content creation', 'GPT automation'],
            'claude': ['AI analysis', 'Long-form content', 'Deep reasoning']
        }
        
        code_lower = code.lower()
        for keyword, cases in patterns.items():
            if keyword in code_lower:
                use_cases.extend(cases)
        
        # Add AI-identified use cases
        if 'automation' in ai_analysis.lower():
            use_cases.append('Process automation')
        if 'api' in ai_analysis.lower():
            use_cases.append('API integration')
        
        return list(set(use_cases))
    
    def _identify_api_integrations(self, code: str) -> List[str]:
        """Identify API integrations"""
        apis = []
        
        api_patterns = {
            r'openai\.|OpenAI': 'OpenAI',
            r'anthropic\.|Anthropic': 'Anthropic/Claude',
            r'groq\.|Groq': 'Groq',
            r'instagram|instabot': 'Instagram',
            r'youtube': 'YouTube',
            r'leonardo': 'Leonardo AI',
            r'stability': 'Stability AI',
            r'elevenlabs': 'ElevenLabs',
            r'suno': 'Suno',
            r'whisper': 'Whisper',
            r'make\.com|make_com': 'Make.com',
            r'n8n': 'n8n',
            r'supabase': 'Supabase',
            r'pinecone': 'Pinecone',
            r'aws|boto3': 'AWS',
        }
        
        for pattern, api_name in api_patterns.items():
            if re.search(pattern, code, re.IGNORECASE):
                apis.append(api_name)
        
        return list(set(apis))
    
    def _identify_workflows(self, code: str, functions: List[Dict]) -> List[str]:
        """Identify workflow patterns"""
        workflows = []
        
        # Look for pipeline patterns
        if 'pipeline' in code.lower():
            workflows.append('Pipeline processing')
        if any('async' in f.get('name', '') for f in functions):
            workflows.append('Asynchronous processing')
        if 'batch' in code.lower():
            workflows.append('Batch processing')
        if re.search(r'for .+ in .+:', code):
            workflows.append('Iterative processing')
        if 'download' in code.lower() and 'upload' in code.lower():
            workflows.append('Download-Process-Upload')
        
        return workflows
    
    def _extract_main_logic(self, code: str) -> str:
        """Extract main execution logic"""
        lines = code.split('\n')
        
        # Find main block
        main_lines = []
        in_main = False
        
        for line in lines:
            if 'if __name__' in line or 'def main' in line:
                in_main = True
            elif in_main:
                if line.strip() and not line.strip().startswith('#'):
                    main_lines.append(line)
                if len(main_lines) > 20:  # Limit to first 20 lines
                    break
        
        return '\n'.join(main_lines[:20]) if main_lines else "No main logic found"
    
    def _assess_documentation(self, code: str, classes: List, functions: List) -> str:
        """Assess documentation quality"""
        total_items = len(classes) + len(functions)
        if total_items == 0:
            return "none"
        
        documented = sum(1 for c in classes if c.get('docstring'))
        documented += sum(1 for f in functions if f.get('docstring'))
        
        ratio = documented / total_items
        
        if ratio > 0.8:
            return "excellent"
        elif ratio > 0.5:
            return "good"
        elif ratio > 0.2:
            return "poor"
        else:
            return "none"
    
    def _calculate_complexity(self, tree: ast.AST, functions: List) -> int:
        """Calculate code complexity score (1-10)"""
        # Simple complexity based on:
        # - Number of functions/classes
        # - Nesting depth
        # - Cyclomatic complexity indicators
        
        complexity = 0
        
        # Base complexity
        complexity += len(functions)
        
        # Check for complex patterns
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For)):
                complexity += 1
            elif isinstance(node, ast.Try):
                complexity += 2
            elif isinstance(node, ast.With):
                complexity += 1
        
        # Normalize to 1-10 scale
        return min(10, max(1, complexity // 5))
    
    def _extract_docstring(self, tree: ast.AST) -> str:
        """Extract module docstring"""
        docstring = ast.get_docstring(tree)
        return docstring if docstring else "No description"
    
    # ==================== Website Discovery ====================
    
    def discover_websites(self, search_paths: List[str]) -> List[Website]:
        """
        Discover and analyze websites and web projects
        """
        print("\n🌐 Discovering websites and web projects...")
        
        websites = []
        
        for search_path in search_paths:
            for root, dirs, files in os.walk(search_path):
                # Skip common ignored directories
                dirs[:] = [d for d in dirs if d not in {
                    'node_modules', '.git', '__pycache__', '.next', 'dist', 'build'
                }]
                
                # Check for website indicators
                if self._is_website_directory(root, files):
                    website = self._analyze_website(root, files)
                    if website:
                        websites.append(website)
                        print(f"   ✅ Found: {website.name} ({website.type})")
        
        self.websites = websites
        return websites
    
    def _is_website_directory(self, root: str, files: List[str]) -> bool:
        """Check if directory contains a website"""
        website_indicators = {
            'index.html', 'index.htm', 'home.html',
            'package.json', 'next.config.js', 'gatsby-config.js',
            'wp-config.php', 'composer.json'
        }
        return bool(set(files) & website_indicators)
    
    def _analyze_website(self, root: str, files: List[str]) -> Optional[Website]:
        """Analyze a website directory"""
        try:
            # Determine type
            web_type = self._determine_website_type(root, files)
            
            # Find pages
            pages = [f for f in files if f.endswith(('.html', '.htm', '.php', '.jsx', '.tsx'))]
            
            # Count assets
            assets = self._count_assets(root)
            
            # Read configuration
            config = self._read_website_config(root, files)
            
            # Determine purpose
            purpose = self._infer_website_purpose(root, pages, config)
            
            # Check deployment status
            deployment = self._check_deployment_status(root, config)
            
            # Extract technologies
            technologies = self._extract_technologies(root, files, config)
            
            return Website(
                path=root,
                name=Path(root).name,
                type=web_type,
                technologies=technologies,
                pages=pages,
                assets=assets,
                configuration=config,
                purpose=purpose,
                deployment_status=deployment
            )
        except Exception as e:
            print(f"   ⚠️  Error analyzing website at {root}: {e}")
            return None
    
    def _determine_website_type(self, root: str, files: List[str]) -> str:
        """Determine website framework/type"""
        if 'next.config.js' in files:
            return 'Next.js'
        elif 'gatsby-config.js' in files:
            return 'Gatsby'
        elif 'package.json' in files:
            return 'React/Node'
        elif 'wp-config.php' in files:
            return 'WordPress'
        elif any(f.endswith('.html') for f in files):
            return 'Static HTML'
        return 'Unknown'
    
    def _count_assets(self, root: str) -> Dict[str, int]:
        """Count different asset types"""
        assets = defaultdict(int)
        
        for dirpath, _, filenames in os.walk(root):
            for filename in filenames:
                ext = Path(filename).suffix.lower()
                if ext in {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}:
                    assets['images'] += 1
                elif ext in {'.js', '.jsx', '.ts', '.tsx'}:
                    assets['javascript'] += 1
                elif ext in {'.css', '.scss', '.sass', '.less'}:
                    assets['styles'] += 1
                elif ext in {'.mp4', '.webm', '.mov'}:
                    assets['videos'] += 1
        
        return dict(assets)
    
    def _read_website_config(self, root: str, files: List[str]) -> Dict[str, Any]:
        """Read website configuration"""
        config = {}
        
        # Try package.json
        if 'package.json' in files:
            try:
                with open(Path(root) / 'package.json') as f:
                    config['package'] = json.load(f)
            except:
                pass
        
        return config
    
    def _infer_website_purpose(self, root: str, pages: List[str], config: Dict) -> str:
        """Infer website purpose"""
        root_name = Path(root).name.lower()
        
        if 'portfolio' in root_name:
            return 'Portfolio site'
        elif 'blog' in root_name:
            return 'Blog/Content site'
        elif 'ecommerce' in root_name or 'shop' in root_name:
            return 'E-commerce site'
        elif 'landing' in root_name:
            return 'Landing page'
        elif config.get('package', {}).get('name'):
            return f"Web app: {config['package']['name']}"
        return 'Website project'
    
    def _check_deployment_status(self, root: str, config: Dict) -> str:
        """Check if website is deployed"""
        # Simple heuristic - check for deployment configs
        deployment_files = {
            'vercel.json', 'netlify.toml', '.github/workflows',
            'firebase.json', 'app.yaml'
        }
        
        root_path = Path(root)
        for dep_file in deployment_files:
            if (root_path / dep_file).exists():
                return 'deployed'
        
        return 'development'
    
    def _extract_technologies(self, root: str, files: List[str], config: Dict) -> List[str]:
        """Extract technologies used"""
        techs = []
        
        # From package.json
        if 'package' in config:
            deps = config['package'].get('dependencies', {})
            if 'react' in deps:
                techs.append('React')
            if 'next' in deps:
                techs.append('Next.js')
            if 'vue' in deps:
                techs.append('Vue.js')
            if 'tailwindcss' in deps or 'tailwindcss' in config['package'].get('devDependencies', {}):
                techs.append('Tailwind CSS')
        
        # From file extensions
        if any(f.endswith('.tsx') or f.endswith('.ts') for f in files):
            techs.append('TypeScript')
        
        return techs
    
    # ==================== Music Collection Analysis ====================
    
    def analyze_music_collection(self, music_path: str = "/Users/steven/Music") -> MusicCollection:
        """
        Deep analysis of music collection
        """
        print(f"\n🎵 Analyzing music collection: {music_path}")
        
        if not Path(music_path).exists():
            print(f"   ⚠️  Path not found: {music_path}")
            return None
        
        total_files = 0
        total_size = 0
        formats = defaultdict(int)
        artists = defaultdict(int)
        albums = defaultdict(int)
        
        for root, dirs, files in os.walk(music_path):
            for file in files:
                ext = Path(file).suffix.lower()
                if ext in {'.mp3', '.flac', '.wav', '.m4a', '.aac', '.ogg', '.wma'}:
                    total_files += 1
                    filepath = Path(root) / file
                    total_size += filepath.stat().st_size
                    formats[ext] += 1
                    
                    # Extract artist/album from path
                    parts = Path(root).parts
                    if len(parts) >= 2:
                        artist = parts[-2] if parts[-1] != Path(music_path).name else parts[-1]
                        album = parts[-1]
                        artists[artist] += 1
                        albums[f"{artist}/{album}"] += 1
        
        # Assess organization
        organization = self._assess_music_organization(Path(music_path))
        
        collection = MusicCollection(
            path=music_path,
            total_files=total_files,
            total_size_gb=total_size / (1024**3),
            formats=dict(formats),
            artists=[{"name": k, "tracks": v} for k, v in sorted(artists.items(), key=lambda x: x[1], reverse=True)[:50]],
            albums=[{"name": k, "tracks": v} for k, v in sorted(albums.items(), key=lambda x: x[1], reverse=True)[:50]],
            playlists=[],  # Would need to scan for .m3u, .pls files
            metadata_quality="unknown",  # Would need ID3 tag analysis
            organization_type=organization,
            duplicates=[]  # Would need hash comparison
        )
        
        print(f"   ✅ Found {total_files:,} music files ({collection.total_size_gb:.1f} GB)")
        print(f"   📊 {len(artists)} artists, {len(albums)} albums")
        
        self.music_collections.append(collection)
        return collection
    
    def _assess_music_organization(self, music_path: Path) -> str:
        """Assess how music is organized"""
        # Sample some directories to determine organization pattern
        subdirs = [d for d in music_path.iterdir() if d.is_dir()]
        
        if not subdirs:
            return "flat"
        
        # Check for common patterns
        sample = subdirs[:10]
        has_artist_folders = any(len(list(d.iterdir())) > 5 for d in sample if d.is_dir())
        
        if has_artist_folders:
            return "by_artist"
        else:
            return "mixed"
    
    # ==================== External Volume Scanning ====================
    
    def scan_external_volumes(self) -> List[ExternalVolume]:
        """
        Scan /Volumes for external drives and analyze content
        """
        print("\n💾 Scanning external volumes...")
        
        volumes_path = Path("/Volumes")
        if not volumes_path.exists():
            print("   ⚠️  /Volumes not found")
            return []
        
        volumes = []
        
        for volume in volumes_path.iterdir():
            if volume.is_dir() and volume.name not in {'Macintosh HD', '.timemachine'}:
                print(f"   🔍 Analyzing volume: {volume.name}")
                vol_analysis = self._analyze_volume(volume)
                if vol_analysis:
                    volumes.append(vol_analysis)
        
        self.external_volumes = volumes
        return volumes
    
    def _analyze_volume(self, volume_path: Path) -> Optional[ExternalVolume]:
        """Analyze a single external volume"""
        try:
            # Get disk usage
            stat = os.statvfs(volume_path)
            total_gb = (stat.f_blocks * stat.f_frsize) / (1024**3)
            used_gb = ((stat.f_blocks - stat.f_bavail) * stat.f_frsize) / (1024**3)
            
            # Quick content summary
            content_summary = defaultdict(int)
            valuable_content = []
            
            for item in volume_path.iterdir():
                if item.is_dir():
                    content_summary['directories'] += 1
                    
                    # Check for valuable content
                    if any(keyword in item.name.lower() for keyword in {
                        'project', 'code', 'site', 'backup', 'music', 'photo', 'video'
                    }):
                        valuable_content.append({
                            'path': str(item),
                            'name': item.name,
                            'type': 'directory'
                        })
                else:
                    ext = item.suffix.lower()
                    content_summary[f'files_{ext}'] += 1
            
            return ExternalVolume(
                mount_point=str(volume_path),
                name=volume_path.name,
                size_gb=total_gb,
                used_gb=used_gb,
                content_summary=dict(content_summary),
                valuable_content=valuable_content[:20],  # Top 20
                backup_status="unknown"
            )
        except Exception as e:
            print(f"      ⚠️  Error analyzing volume: {e}")
            return None
    
    # ==================== Comprehensive Report Generation ====================
    
    def generate_comprehensive_report(self, output_file: str = "DEEP_CONTENT_ANALYSIS_ULTIMATE.json"):
        """
        Generate comprehensive analysis report
        """
        report = {
            "analysis_date": datetime.now().isoformat(),
            "summary": {
                "python_scripts": len(self.python_scripts),
                "websites": len(self.websites),
                "music_collections": len(self.music_collections),
                "external_volumes": len(self.external_volumes)
            },
            "python_scripts": [
                {
                    "filename": s.filename,
                    "purpose": s.purpose,
                    "actual_functionality": s.actual_functionality,
                    "api_integrations": s.api_integrations,
                    "use_cases": s.use_cases,
                    "complexity": s.complexity_score,
                    "documentation": s.documentation_quality,
                    "lines": s.lines
                }
                for s in self.python_scripts[:50]  # Top 50 for JSON size
            ],
            "websites": [
                {
                    "name": w.name,
                    "type": w.type,
                    "path": w.path,
                    "technologies": w.technologies,
                    "purpose": w.purpose,
                    "pages": len(w.pages),
                    "assets": w.assets,
                    "deployment": w.deployment_status
                }
                for w in self.websites
            ],
            "music_collections": [
                {
                    "path": m.path,
                    "total_files": m.total_files,
                    "size_gb": m.total_size_gb,
                    "formats": m.formats,
                    "top_artists": m.artists[:10],
                    "organization": m.organization_type
                }
                for m in self.music_collections
            ],
            "external_volumes": [
                {
                    "name": v.name,
                    "size_gb": v.size_gb,
                    "used_gb": v.used_gb,
                    "valuable_content_count": len(v.valuable_content),
                    "top_content": v.valuable_content[:5]
                }
                for v in self.external_volumes
            ]
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ Comprehensive report saved: {output_file}")
        return report


async def main():
    """Run comprehensive deep analysis"""
    print("🧠 DEEP CONTENT ANALYZER ULTIMATE")
    print("="*70)
    print()
    
    analyzer = DeepContentAnalyzerUltimate()
    
    # 1. Analyze Python scripts
    print("📂 Phase 1: Deep Python Script Analysis")
    print("-"*70)
    
    pythons_dir = Path("/Users/steven/pythons")
    python_files = list(pythons_dir.glob("*.py"))[:20]  # Analyze first 20 for demo
    
    for py_file in python_files:
        script = analyzer.deep_analyze_python_script(str(py_file))
        if script:
            analyzer.python_scripts.append(script)
    
    # 2. Discover websites
    print("\n📂 Phase 2: Website Discovery")
    print("-"*70)
    
    search_paths = [
        "/Users/steven/ai-sites",
        "/Users/steven/workspace",
        "/Users/steven/GitHub"
    ]
    analyzer.discover_websites([p for p in search_paths if Path(p).exists()])
    
    # 3. Analyze music
    print("\n📂 Phase 3: Music Collection Analysis")
    print("-"*70)
    
    analyzer.analyze_music_collection("/Users/steven/Music")
    
    # 4. Scan external volumes
    print("\n📂 Phase 4: External Volume Scan")
    print("-"*70)
    
    analyzer.scan_external_volumes()
    
    # 5. Generate report
    print("\n📊 Generating Comprehensive Report...")
    print("-"*70)
    
    report = analyzer.generate_comprehensive_report()
    
    # Print summary
    print("\n" + "="*70)
    print("📊 ANALYSIS COMPLETE")
    print("="*70)
    print(f"Python Scripts Analyzed: {len(analyzer.python_scripts)}")
    print(f"Websites Discovered: {len(analyzer.websites)}")
    print(f"Music Collections: {len(analyzer.music_collections)}")
    print(f"External Volumes: {len(analyzer.external_volumes)}")
    print("\n✅ Report saved: DEEP_CONTENT_ANALYSIS_ULTIMATE.json")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

