#!/usr/bin/env python3
"""
DEEP MULTI-VOLUME CONTENT-AWARE ANALYZER
Intelligently reads and analyzes actual file contents across multiple folder depths
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
import json
import ast
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict
import mimetypes

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import subprocess
    FFPROBE_AVAILABLE = True
except ImportError:
    FFPROBE_AVAILABLE = False


class DeepContentAnalyzer:
    """Analyzes actual file contents, not just filenames"""
    
    def __init__(self, max_depth: int = 5, max_file_size: int = 10 * 1024 * 1024):
        self.max_depth = max_depth
        self.max_file_size = max_file_size
        self.stats = {
            'files_analyzed': 0,
            'python_files': 0,
            'html_files': 0,
            'json_files': 0,
            'markdown_files': 0,
            'image_files': 0,
            'audio_files': 0,
            'video_files': 0,
            'errors': []
        }
        self.findings = {
            'projects': [],
            'apis_integrated': set(),
            'technologies': set(),
            'content_types': defaultdict(int),
            'business_opportunities': [],
            'automation_potential': [],
            'security_issues': [],
            'code_patterns': defaultdict(int),
        }
    
    def analyze_file(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """Analyze a single file's actual content"""
        try:
            if not filepath.exists() or not filepath.is_file():
                return None
            
            # Skip system files
            if filepath.name.startswith('.') or filepath.name.startswith('__'):
                return None
            
            # Check file size
            size = filepath.stat().st_size
            if size > self.max_file_size:
                return {'path': str(filepath), 'error': 'File too large', 'size': size}
            
            if size == 0:
                return None
            
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(str(filepath))
            
            # Analyze based on extension/content
            ext = filepath.suffix.lower()
            analysis = {
                'path': str(filepath),
                'size': size,
                'mime_type': mime_type,
                'extension': ext,
                'depth': len(filepath.parts) - len(Path(filepath.parts[0]).parts),
            }
            
            # Python files - AST analysis
            if ext == '.py':
                analysis.update(self._analyze_python(filepath))
                self.stats['python_files'] += 1
            
            # HTML files - parse structure
            elif ext in ['.html', '.htm']:
                analysis.update(self._analyze_html(filepath))
                self.stats['html_files'] += 1
            
            # JSON files - parse structure
            elif ext == '.json':
                analysis.update(self._analyze_json(filepath))
                self.stats['json_files'] += 1
            
            # Markdown files - extract content
            elif ext in ['.md', '.markdown']:
                analysis.update(self._analyze_markdown(filepath))
                self.stats['markdown_files'] += 1
            
            # Image files - metadata
            elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
                analysis.update(self._analyze_image(filepath))
                self.stats['image_files'] += 1
            
            # Audio files - metadata
            elif ext in ['.mp3', '.wav', '.flac', '.m4a', '.ogg']:
                analysis.update(self._analyze_audio(filepath))
                self.stats['audio_files'] += 1
            
            # Video files - metadata
            elif ext in ['.mp4', '.mov', '.avi', '.mkv', '.webm']:
                analysis.update(self._analyze_video(filepath))
                self.stats['video_files'] += 1
            
            # Config files
            elif ext in ['.yml', '.yaml', '.toml', '.ini', '.conf', '.env']:
                analysis.update(self._analyze_config(filepath))
            
            # JavaScript/TypeScript
            elif ext in ['.js', '.ts', '.jsx', '.tsx']:
                analysis.update(self._analyze_javascript(filepath))
            
            # CSS
            elif ext in ['.css', '.scss', '.sass']:
                analysis.update(self._analyze_css(filepath))
            
            # Text files - read first lines
            elif mime_type and mime_type.startswith('text/'):
                analysis.update(self._analyze_text(filepath))
            
            self.stats['files_analyzed'] += 1
            return analysis
            
        except Exception as e:
            self.stats['errors'].append({
                'file': str(filepath),
                'error': str(e)
            })
            return None
    
    def _analyze_python(self, filepath: Path) -> Dict[str, Any]:
        """Deep Python file analysis using AST"""
        result = {
            'type': 'python',
            'classes': [],
            'functions': [],
            'imports': [],
            'apis_used': [],
            'technologies': [],
            'purpose': 'unknown',
            'complexity': 'low',
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # AST parsing
            try:
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    # Classes
                    if isinstance(node, ast.ClassDef):
                        result['classes'].append({
                            'name': node.name,
                            'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                            'bases': [self._ast_to_string(b) for b in node.bases],
                        })
                    
                    # Functions
                    elif isinstance(node, ast.FunctionDef):
                        result['functions'].append({
                            'name': node.name,
                            'args': [arg.arg for arg in node.args.args],
                            'decorators': [self._ast_to_string(d) for d in node.decorator_list],
                        })
                    
                    # Imports
                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            result['imports'].append(alias.name)
                            self._extract_technologies(alias.name, result)
                    
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            result['imports'].append(node.module)
                            self._extract_technologies(node.module, result)
                
                # Extract APIs from imports and strings
                api_patterns = {
                    'openai': 'OpenAI',
                    'anthropic': 'Anthropic Claude',
                    'google.generativeai': 'Google Gemini',
                    'groq': 'Groq',
                    'xai': 'Grok/XAI',
                    'perplexity': 'Perplexity',
                    'deepseek': 'DeepSeek',
                    'mistral': 'Mistral',
                    'cohere': 'Cohere',
                    'together': 'Together AI',
                    'cerebras': 'Cerebras',
                    'elevenlabs': 'ElevenLabs',
                    'stability': 'Stability AI',
                    'selenium': 'Selenium',
                    'requests': 'HTTP Requests',
                    'beautifulsoup': 'BeautifulSoup',
                    'pandas': 'Pandas',
                    'numpy': 'NumPy',
                    'pillow': 'PIL/Pillow',
                    'ffmpeg': 'FFmpeg',
                }
                
                for imp in result['imports']:
                    for pattern, api_name in api_patterns.items():
                        if pattern in imp.lower():
                            result['apis_used'].append(api_name)
                            self.findings['apis_integrated'].add(api_name)
                
                # Determine purpose from content
                content_lower = content.lower()
                if any(word in content_lower for word in ['trend', 'seo', 'optimize', 'keyword']):
                    result['purpose'] = 'SEO/Content Optimization'
                elif any(word in content_lower for word in ['extract', 'scrape', 'grab', 'download']):
                    result['purpose'] = 'Content Extraction'
                elif any(word in content_lower for word in ['orchestrat', 'route', 'multi', 'llm']):
                    result['purpose'] = 'AI Orchestration'
                elif any(word in content_lower for word in ['audio', 'music', 'transcribe', 'whisper']):
                    result['purpose'] = 'Audio Processing'
                elif any(word in content_lower for word in ['image', 'photo', 'gallery', 'visual']):
                    result['purpose'] = 'Image Processing'
                elif any(word in content_lower for word in ['automate', 'workflow', 'pipeline']):
                    result['purpose'] = 'Automation'
                elif any(word in content_lower for word in ['customer', 'retention', 'churn', 'lifetime']):
                    result['purpose'] = 'CRM/Customer Management'
                elif any(word in content_lower for word in ['analyze', 'analyze', 'intelligence', 'insight']):
                    result['purpose'] = 'Analysis/Intelligence'
                elif any(word in content_lower for word in ['youtube', 'video', 'description', 'tags']):
                    result['purpose'] = 'YouTube/Video Content'
                
                # Complexity estimation
                total_elements = len(result['classes']) + len(result['functions'])
                if total_elements > 20:
                    result['complexity'] = 'high'
                elif total_elements > 10:
                    result['complexity'] = 'medium'
                
            except SyntaxError:
                result['error'] = 'Syntax error in Python file'
        
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _analyze_html(self, filepath: Path) -> Dict[str, Any]:
        """Analyze HTML structure and content"""
        result = {
            'type': 'html',
            'title': None,
            'meta_tags': {},
            'scripts': [],
            'stylesheets': [],
            'links': [],
            'is_landing_page': False,
            'is_gallery': False,
            'has_forms': False,
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract title
            title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if title_match:
                result['title'] = title_match.group(1).strip()
            
            # Meta tags
            meta_matches = re.findall(r'<meta[^>]+>', content, re.IGNORECASE)
            for meta in meta_matches:
                name_match = re.search(r'name=["\']([^"\']+)["\']', meta)
                content_match = re.search(r'content=["\']([^"\']+)["\']', meta)
                if name_match and content_match:
                    result['meta_tags'][name_match.group(1)] = content_match.group(1)
            
            # Scripts
            script_matches = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', content, re.IGNORECASE)
            result['scripts'] = script_matches
            
            # Stylesheets
            style_matches = re.findall(r'<link[^>]*rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\']', content, re.IGNORECASE)
            result['stylesheets'] = style_matches
            
            # Links
            link_matches = re.findall(r'<a[^>]*href=["\']([^"\']+)["\']', content, re.IGNORECASE)
            result['links'] = link_matches[:20]  # Limit
            
            # Detect page type
            content_lower = content.lower()
            if any(word in content_lower for word in ['gallery', 'image', 'photo', 'portfolio']):
                result['is_gallery'] = True
            if any(word in content_lower for word in ['landing', 'hero', 'cta', 'sign up']):
                result['is_landing_page'] = True
            if '<form' in content_lower:
                result['has_forms'] = True
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _analyze_json(self, filepath: Path) -> Dict[str, Any]:
        """Analyze JSON structure"""
        result = {
            'type': 'json',
            'structure': 'unknown',
            'keys': [],
            'size_estimate': 'small',
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                data = json.load(f)
            
            if isinstance(data, dict):
                result['structure'] = 'object'
                result['keys'] = list(data.keys())[:20]
            elif isinstance(data, list):
                result['structure'] = 'array'
                if len(data) > 0 and isinstance(data[0], dict):
                    result['keys'] = list(data[0].keys())[:20]
            
            # Detect type
            json_str = json.dumps(data).lower()
            if 'api' in json_str or 'endpoint' in json_str:
                result['purpose'] = 'API Configuration'
            elif 'workflow' in json_str or 'blueprint' in json_str:
                result['purpose'] = 'Workflow/Blueprint'
            elif 'package' in json_str or 'dependencies' in json_str:
                result['purpose'] = 'Package Configuration'
        
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _analyze_markdown(self, filepath: Path) -> Dict[str, Any]:
        """Analyze Markdown content"""
        result = {
            'type': 'markdown',
            'headings': [],
            'code_blocks': 0,
            'links': [],
            'word_count': 0,
            'topics': [],
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Headings
            heading_matches = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
            result['headings'] = heading_matches[:20]
            
            # Code blocks
            result['code_blocks'] = len(re.findall(r'```', content)) // 2
            
            # Links
            link_matches = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
            result['links'] = link_matches[:20]
            
            # Word count
            words = re.findall(r'\b\w+\b', content)
            result['word_count'] = len(words)
            
            # Topics (from headings and content)
            content_lower = content.lower()
            topics = []
            if any(word in content_lower for word in ['seo', 'optimize', 'keyword']):
                topics.append('SEO')
            if any(word in content_lower for word in ['ai', 'machine learning', 'llm']):
                topics.append('AI/ML')
            if any(word in content_lower for word in ['trend', 'trending', 'hot']):
                topics.append('Trending Content')
            if any(word in content_lower for word in ['youtube', 'video', 'content']):
                topics.append('Video Content')
            result['topics'] = topics
        
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _analyze_image(self, filepath: Path) -> Dict[str, Any]:
        """Analyze image metadata"""
        result = {
            'type': 'image',
            'width': None,
            'height': None,
            'format': None,
            'size_kb': 0,
        }
        
        try:
            if PIL_AVAILABLE:
                with Image.open(filepath) as img:
                    result['width'] = img.width
                    result['height'] = img.height
                    result['format'] = img.format
                    result['size_kb'] = filepath.stat().st_size / 1024
            else:
                result['size_kb'] = filepath.stat().st_size / 1024
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _analyze_audio(self, filepath: Path) -> Dict[str, Any]:
        """Analyze audio metadata using ffprobe"""
        result = {
            'type': 'audio',
            'duration': None,
            'bitrate': None,
            'sample_rate': None,
            'format': None,
        }
        
        if FFPROBE_AVAILABLE:
            try:
                cmd = [
                    'ffprobe', '-v', 'quiet', '-print_format', 'json',
                    '-show_format', '-show_streams', str(filepath)
                ]
                output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
                data = json.loads(output)
                
                if 'format' in data:
                    fmt = data['format']
                    result['duration'] = float(fmt.get('duration', 0))
                    result['bitrate'] = int(fmt.get('bit_rate', 0))
                    result['format'] = fmt.get('format_name', '')
                
                if 'streams' in data and len(data['streams']) > 0:
                    stream = data['streams'][0]
                    result['sample_rate'] = int(stream.get('sample_rate', 0))
            except:
                pass
        
        return result
    
    def _analyze_video(self, filepath: Path) -> Dict[str, Any]:
        """Analyze video metadata"""
        result = {
            'type': 'video',
            'duration': None,
            'width': None,
            'height': None,
            'bitrate': None,
            'format': None,
        }
        
        if FFPROBE_AVAILABLE:
            try:
                cmd = [
                    'ffprobe', '-v', 'quiet', '-print_format', 'json',
                    '-show_format', '-show_streams', str(filepath)
                ]
                output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
                data = json.loads(output)
                
                if 'format' in data:
                    fmt = data['format']
                    result['duration'] = float(fmt.get('duration', 0))
                    result['bitrate'] = int(fmt.get('bit_rate', 0))
                    result['format'] = fmt.get('format_name', '')
                
                if 'streams' in data:
                    for stream in data['streams']:
                        if stream.get('codec_type') == 'video':
                            result['width'] = int(stream.get('width', 0))
                            result['height'] = int(stream.get('height', 0))
                            break
            except:
                pass
        
        return result
    
    def _analyze_config(self, filepath: Path) -> Dict[str, Any]:
        """Analyze configuration files"""
        result = {
            'type': 'config',
            'keys': [],
            'has_secrets': False,
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check for secrets
            secret_patterns = ['api_key', 'password', 'secret', 'token', 'auth']
            content_lower = content.lower()
            for pattern in secret_patterns:
                if pattern in content_lower:
                    result['has_secrets'] = True
                    break
            
            # Extract keys (simple)
            if filepath.suffix in ['.env', '.ini', '.conf']:
                lines = content.split('\n')
                for line in lines[:50]:
                    if '=' in line:
                        key = line.split('=')[0].strip()
                        if key and not key.startswith('#'):
                            result['keys'].append(key)
        
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _analyze_javascript(self, filepath: Path) -> Dict[str, Any]:
        """Analyze JavaScript/TypeScript files"""
        result = {
            'type': 'javascript',
            'functions': [],
            'apis_used': [],
            'is_browser_script': False,
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Function detection (simple regex)
            func_matches = re.findall(r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\(|(\w+)\s*:\s*(?:async\s*)?\()', content)
            result['functions'] = [f[0] or f[1] or f[2] for f in func_matches[:20]]
            
            # Browser detection
            if any(word in content for word in ['document.', 'window.', 'navigator.', 'console.']):
                result['is_browser_script'] = True
            
            # API detection
            api_patterns = {
                'fetch': 'Fetch API',
                'axios': 'Axios',
                'chrome.runtime': 'Chrome Extension',
                'browser.runtime': 'Browser Extension',
            }
            for pattern, api_name in api_patterns.items():
                if pattern in content:
                    result['apis_used'].append(api_name)
        
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _analyze_css(self, filepath: Path) -> Dict[str, Any]:
        """Analyze CSS files"""
        result = {
            'type': 'css',
            'selectors': [],
            'has_animations': False,
            'has_responsive': False,
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Selectors (simple)
            selector_matches = re.findall(r'([.#]?[\w-]+)\s*\{', content)
            result['selectors'] = list(set(selector_matches))[:30]
            
            # Animations
            if '@keyframes' in content or 'animation:' in content:
                result['has_animations'] = True
            
            # Responsive
            if '@media' in content:
                result['has_responsive'] = True
        
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _analyze_text(self, filepath: Path) -> Dict[str, Any]:
        """Analyze text files"""
        result = {
            'type': 'text',
            'first_lines': [],
            'word_count': 0,
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()[:10]
                result['first_lines'] = [line.strip() for line in lines if line.strip()]
                content = ''.join(lines)
                words = re.findall(r'\b\w+\b', content)
                result['word_count'] = len(words)
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
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
    
    def _extract_technologies(self, module_name: str, result: Dict):
        """Extract technologies from module names"""
        tech_map = {
            'selenium': 'Selenium',
            'requests': 'HTTP Requests',
            'beautifulsoup': 'Web Scraping',
            'pandas': 'Data Analysis',
            'numpy': 'Numerical Computing',
            'pillow': 'Image Processing',
            'ffmpeg': 'Media Processing',
            'openai': 'OpenAI',
            'anthropic': 'Anthropic',
            'groq': 'Groq',
        }
        
        for key, tech in tech_map.items():
            if key in module_name.lower():
                result['technologies'].append(tech)
                self.findings['technologies'].add(tech)


class MultiVolumeDeepAnalyzer:
    """Analyzes multiple volumes with deep content awareness"""
    
    def __init__(self, volumes: List[str], max_depth: int = 5):
        self.volumes = volumes
        self.analyzer = DeepContentAnalyzer(max_depth=max_depth)
        self.results = {
            'volumes': {},
            'summary': {},
            'projects': [],
            'opportunities': [],
        }
    
    def analyze(self) -> Dict[str, Any]:
        """Perform deep analysis of all volumes"""
        print("🔍 Starting deep multi-volume content-aware analysis...")
        
        for volume_path in self.volumes:
            volume = Path(volume_path)
            if not volume.exists():
                print(f"⚠️  Volume not found: {volume_path}")
                continue
            
            print(f"\n📦 Analyzing: {volume_path}")
            volume_results = self._analyze_volume(volume)
            self.results['volumes'][volume_path] = volume_results
        
        # Generate summary
        self.results['summary'] = self._generate_summary()
        
        return self.results
    
    def _analyze_volume(self, volume: Path) -> Dict[str, Any]:
        """Analyze a single volume"""
        volume_data = {
            'path': str(volume),
            'directories': {},
            'files': [],
            'projects': [],
            'total_files': 0,
            'total_size': 0,
        }
        
        # Analyze key directories
        key_dirs = self._identify_key_directories(volume)
        
        for dir_path in key_dirs[:50]:  # Limit to top 50 directories
            dir_analysis = self._analyze_directory(dir_path, max_files=100)
            if dir_analysis:
                rel_path = str(dir_path.relative_to(volume))
                volume_data['directories'][rel_path] = dir_analysis
        
        # Collect file statistics
        for root, dirs, files in os.walk(volume):
            # Limit depth
            depth = len(Path(root).relative_to(volume).parts)
            if depth > self.analyzer.max_depth:
                dirs.clear()
                continue
            
            for file in files[:1000]:  # Limit per directory
                filepath = Path(root) / file
                try:
                    volume_data['total_files'] += 1
                    volume_data['total_size'] += filepath.stat().st_size
                except:
                    pass
        
        return volume_data
    
    def _identify_key_directories(self, volume: Path) -> List[Path]:
        """Identify important directories to analyze"""
        key_dirs = []
        
        # Look for common project patterns
        patterns = [
            '**/ai-sites/**',
            '**/steven/**',
            '**/projects/**',
            '**/code/**',
            '**/scripts/**',
            '**/content/**',
            '**/gallery/**',
            '**/music/**',
            '**/images/**',
            '**/archives/**',
        ]
        
        for pattern in patterns:
            try:
                matches = list(volume.glob(pattern))
                key_dirs.extend(matches[:10])  # Limit per pattern
            except:
                pass
        
        # Remove duplicates and sort
        key_dirs = sorted(set(key_dirs), key=lambda x: str(x))
        
        return key_dirs
    
    def _analyze_directory(self, dir_path: Path, max_files: int = 100) -> Optional[Dict[str, Any]]:
        """Analyze a directory's contents"""
        if not dir_path.exists() or not dir_path.is_dir():
            return None
        
        dir_analysis = {
            'path': str(dir_path),
            'files': [],
            'subdirectories': [],
            'project_type': None,
            'technologies': [],
            'purpose': None,
        }
        
        # Analyze files in directory
        files_analyzed = 0
        for item in dir_path.iterdir():
            if files_analyzed >= max_files:
                break
            
            if item.is_file():
                analysis = self.analyzer.analyze_file(item)
                if analysis:
                    dir_analysis['files'].append(analysis)
                    files_analyzed += 1
                    
                    # Extract technologies
                    if 'technologies' in analysis:
                        dir_analysis['technologies'].extend(analysis['technologies'])
                    
                    # Determine project type
                    if analysis.get('type') == 'python':
                        if not dir_analysis['project_type']:
                            dir_analysis['project_type'] = 'Python Project'
                        if analysis.get('purpose'):
                            dir_analysis['purpose'] = analysis['purpose']
            
            elif item.is_dir() and not item.name.startswith('.'):
                dir_analysis['subdirectories'].append(item.name)
        
        # Deduplicate technologies
        dir_analysis['technologies'] = list(set(dir_analysis['technologies']))
        
        return dir_analysis
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate comprehensive summary"""
        summary = {
            'total_volumes': len(self.results['volumes']),
            'total_files_analyzed': self.analyzer.stats['files_analyzed'],
            'file_types': {
                'python': self.analyzer.stats['python_files'],
                'html': self.analyzer.stats['html_files'],
                'json': self.analyzer.stats['json_files'],
                'markdown': self.analyzer.stats['markdown_files'],
                'images': self.analyzer.stats['image_files'],
                'audio': self.analyzer.stats['audio_files'],
                'video': self.analyzer.stats['video_files'],
            },
            'apis_integrated': sorted(list(self.analyzer.findings['apis_integrated'])),
            'technologies': sorted(list(self.analyzer.findings['technologies'])),
            'errors': len(self.analyzer.stats['errors']),
        }
        
        return summary


def main():
    """Main execution"""
    volumes = [
        '/Volumes/2T-Xx',
        '/Volumes/DeVonDaTa',
    ]
    
    analyzer = MultiVolumeDeepAnalyzer(volumes, max_depth=5)
    results = analyzer.analyze()
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = Path.home() / f'DEEP_VOLUMES_ANALYSIS_{timestamp}.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    print("\n✅ Analysis complete!")
    print(f"📄 Results saved to: {output_file}")
    print("\n📊 Summary:")
    print(f"   Files analyzed: {results['summary']['total_files_analyzed']}")
    print(f"   APIs found: {len(results['summary']['apis_integrated'])}")
    print(f"   Technologies: {len(results['summary']['technologies'])}")
    
    # Generate markdown report
    report_file = Path.home() / f'DEEP_VOLUMES_ANALYSIS_{timestamp}.md'
    generate_markdown_report(results, report_file)
    print(f"📝 Markdown report: {report_file}")


def generate_markdown_report(results: Dict, output_file: Path):
    """Generate comprehensive markdown report"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 🔍 DEEP MULTI-VOLUME CONTENT-AWARE ANALYSIS\n\n")
        f.write(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Summary
        f.write("## 📊 Executive Summary\n\n")
        summary = results['summary']
        f.write(f"- **Volumes Analyzed:** {summary['total_volumes']}\n")
        f.write(f"- **Files Analyzed:** {summary['total_files_analyzed']}\n")
        f.write(f"- **APIs Integrated:** {len(summary['apis_integrated'])}\n")
        f.write(f"- **Technologies:** {len(summary['technologies'])}\n\n")
        
        # File types
        f.write("### File Types\n\n")
        for file_type, count in summary['file_types'].items():
            if count > 0:
                f.write(f"- **{file_type.title()}:** {count}\n")
        f.write("\n")
        
        # APIs
        f.write("### APIs Integrated\n\n")
        for api in summary['apis_integrated']:
            f.write(f"- {api}\n")
        f.write("\n")
        
        # Technologies
        f.write("### Technologies Used\n\n")
        for tech in summary['technologies']:
            f.write(f"- {tech}\n")
        f.write("\n")
        
        # Volume details
        f.write("## 📦 Volume Details\n\n")
        for volume_path, volume_data in results['volumes'].items():
            f.write(f"### {volume_path}\n\n")
            f.write(f"- **Total Files:** {volume_data['total_files']:,}\n")
            f.write(f"- **Total Size:** {volume_data['total_size'] / (1024**3):.2f} GB\n")
            f.write(f"- **Key Directories:** {len(volume_data['directories'])}\n\n")
            
            # Key directories
            f.write("#### Key Directories\n\n")
            for dir_path, dir_info in list(volume_data['directories'].items())[:20]:
                f.write(f"**{dir_path}**\n")
                if dir_info.get('project_type'):
                    f.write(f"- Type: {dir_info['project_type']}\n")
                if dir_info.get('purpose'):
                    f.write(f"- Purpose: {dir_info['purpose']}\n")
                if dir_info.get('technologies'):
                    f.write(f"- Technologies: {', '.join(dir_info['technologies'][:5])}\n")
                f.write(f"- Files analyzed: {len(dir_info['files'])}\n\n")


if __name__ == '__main__':
    main()

