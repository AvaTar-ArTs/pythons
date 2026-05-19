#!/usr/bin/env python3
"""
EcoSystem Management Agent - Advanced Agent for Managing Steven's Expanded Automation Ecosystem
=============================================================================================

This agent serves as the central nervous system for Steven's expanded automation ecosystem,
managing 20+ business verticals, 758+ Python scripts, 2,500+ automation tools,
AI integrations, and revenue-generating assets across the complete technology stack.

Features:
- Asset management with business value scoring
- Business vertical coordination
- Revenue forecasting engine
- Workflow optimization suggestions
- Dashboard metrics generation
- Safe asset execution capabilities
- Comprehensive reporting features
"""

import os
import sys
import json
import sqlite3
import hashlib
import subprocess
import importlib.util
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
import logging
import csv
import yaml
import requests
from urllib.parse import urlparse
import re
import time
import threading
from collections import defaultdict, Counter
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Asset:
    """Represents a single asset in the ecosystem"""
    id: str
    name: str
    path: str
    type: str
    business_vertical: str
    business_value_score: float
    revenue_potential: float
    usage_count: int
    last_used: Optional[datetime]
    created_at: datetime
    tags: List[str]
    dependencies: List[str]
    status: str  # active, deprecated, experimental, archived

class EcoSystemOrchestrator:
    """
    Advanced agent for managing Steven's expanded automation ecosystem
    Coordinates across 20+ business verticals, 758+ Python scripts, and 2,500+ automation tools
    """
    
    def __init__(self, db_path: str = "/Users/steven/ecosystem_assets.db"):
        self.db_path = db_path
        self.assets_db = None
        self.business_verticals = {
            'AI_Automation_Services': {'revenue_potential': 150000, 'active': True},
            'Creative_Content_Generation': {'revenue_potential': 125000, 'active': True},
            'Digital_Product_Sales': {'revenue_potential': 100000, 'active': True},
            'AI_Consultation_Training': {'revenue_potential': 125000, 'active': True},
            'Music_Production_Licensing': {'revenue_potential': 75000, 'active': True},
            'Forensic_Technology_Solutions': {'revenue_potential': 200000, 'active': True},
            'Ecommerce_Print_on_Demand': {'revenue_potential': 50000, 'active': True},
            'AI_Voice_Agents': {'revenue_potential': 100000, 'active': True},
            'Knowledge_Management_Systems': {'revenue_potential': 75000, 'active': True},
            'AI_Research_Development': {'revenue_potential': 150000, 'active': True},
            'Content_Curation_Analytics': {'revenue_potential': 60000, 'active': True},
            'Ethical_Hacking_Education': {'revenue_potential': 40000, 'active': True},
            'Narrative_AI_Engine': {'revenue_potential': 80000, 'active': True},
            'NotebookLM_Publishing': {'revenue_potential': 50000, 'active': True},
            'Affiliate_Marketing': {'revenue_potential': 35000, 'active': True},
            'Video_Marketing': {'revenue_potential': 45000, 'active': True},
            'Visual_Product_Libraries': {'revenue_potential': 60000, 'active': True},
            'SaaS_Retention_Solutions': {'revenue_potential': 200000, 'active': True},
            'OSINT_Services': {'revenue_potential': 75000, 'active': True},
            'Swarm_Orchestration': {'revenue_potential': 100000, 'active': True}
        }
        
        self.setup_database()
        self.load_assets()
        
    def setup_database(self):
        """Initialize the assets database with proper schema"""
        self.assets_db = sqlite3.connect(self.db_path)
        cursor = self.assets_db.cursor()
        
        # Create assets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                type TEXT,
                business_vertical TEXT,
                business_value_score REAL,
                revenue_potential REAL,
                usage_count INTEGER DEFAULT 0,
                last_used TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tags TEXT,
                dependencies TEXT,
                status TEXT DEFAULT 'active',
                UNIQUE(path)
            )
        ''')
        
        # Create business verticals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS business_verticals (
                name TEXT PRIMARY KEY,
                revenue_potential REAL,
                active BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create asset_usage_log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS asset_usage_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id TEXT,
                action TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (asset_id) REFERENCES assets (id)
            )
        ''')
        
        # Create indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_assets_type ON assets(type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_assets_vertical ON assets(business_vertical)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_assets_value ON assets(business_value_score)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_assets_status ON assets(status)')
        
        # Insert business verticals if not exists
        for vertical, data in self.business_verticals.items():
            cursor.execute('''
                INSERT OR IGNORE INTO business_verticals (name, revenue_potential, active)
                VALUES (?, ?, ?)
            ''', (vertical, data['revenue_potential'], data['active']))
        
        self.assets_db.commit()
        logger.info(f"Database initialized at {self.db_path}")
    
    def calculate_business_value_score(self, asset_path: str, asset_type: str, business_vertical: str) -> float:
        """
        Calculate business value score based on multiple factors
        """
        score = 0.0
        
        # Base score based on asset type
        type_weights = {
            'python_script': 8.0,
            'ai_model': 9.0,
            'automation_tool': 8.5,
            'api_integration': 7.5,
            'data_pipeline': 8.0,
            'ml_model': 9.0,
            'web_application': 7.0,
            'configuration': 6.0,
            'documentation': 5.0,
            'utility': 6.5,
            'workflow': 7.5,
            'music_track': 6.0,
            'design_asset': 5.5,
            'research_note': 4.5
        }
        
        score += type_weights.get(asset_type, 5.0)
        
        # Boost for high-value business verticals
        high_value_verticals = [
            'Forensic_Technology_Solutions', 'SaaS_Retention_Solutions',
            'AI_Automation_Services', 'AI_Research_Development'
        ]
        
        if business_vertical in high_value_verticals:
            score += 2.0
            
        # Boost for automation and AI tools
        path_lower = asset_path.lower()
        if any(keyword in path_lower for keyword in ['automation', 'ai', 'ml', 'intelligent', 'smart', 'advanced']):
            score += 1.5
            
        # Boost for revenue-generating potential
        if any(keyword in path_lower for keyword in ['revenue', 'monetization', 'sales', 'profit', 'business']):
            score += 1.0
            
        # Cap at 10.0
        return min(score, 10.0)
    
    def scan_directory(self, directory: str, excluded_dirs: set = None) -> List[Dict]:
        """Scan directory recursively and identify assets"""
        if excluded_dirs is None:
            excluded_dirs = {
                '.git', 'node_modules', '__pycache__', '.vscode', '.idea',
                'dist', 'build', '.pytest_cache', '.tox', 'venv',
                'env', '.env', '__MACOSX', '.svn', '.hg', 'target',
                'tmp', 'temp', 'logs', 'cache', '.next', 'coverage',
                '.github', '.gitlab', '.circleci', '.travis', 'vendor',
                'Pods', '.bundle', 'bower_components', '.meteor'
            }
        
        assets = []
        directory_path = Path(directory)
        
        for root, dirs, files in os.walk(directory_path):
            # Remove excluded directories from walk
            dirs[:] = [d for d in dirs if d not in excluded_dirs and not d.startswith('.')]
            
            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(directory_path)
                
                # Determine asset type based on extension
                ext = file_path.suffix.lower()
                asset_type = self._classify_asset_type(ext, file_path)
                
                # Skip temporary and system files
                if self._is_temp_or_system_file(file_path):
                    continue
                
                # Determine business vertical based on path
                business_vertical = self._determine_business_vertical(rel_path)
                
                # Calculate business value score
                business_value = self.calculate_business_value_score(str(file_path), asset_type, business_vertical)
                
                # Calculate revenue potential based on business value and vertical
                vertical_data = self.business_verticals.get(business_vertical, {'revenue_potential': 50000})
                revenue_potential = vertical_data['revenue_potential'] * (business_value / 10.0)
                
                asset = {
                    'id': hashlib.md5(str(file_path).encode()).hexdigest(),
                    'name': file_path.name,
                    'path': str(file_path),
                    'type': asset_type,
                    'business_vertical': business_vertical,
                    'business_value_score': business_value,
                    'revenue_potential': revenue_potential,
                    'usage_count': 0,
                    'last_used': None,
                    'created_at': datetime.now(),
                    'tags': self._extract_tags(str(file_path)),
                    'dependencies': self._extract_dependencies(str(file_path)),
                    'status': 'active'
                }
                
                assets.append(asset)
                
        logger.info(f"Scanned {len(assets)} assets from {directory}")
        return assets
    
    def _classify_asset_type(self, extension: str, file_path: Path) -> str:
        """Classify asset type based on extension and content"""
        # Mapping of extensions to asset types
        extension_map = {
            '.py': 'python_script',
            '.js': 'javascript_script',
            '.ts': 'typescript_script',
            '.json': 'json_config',
            '.yaml': 'yaml_config',
            '.yml': 'yaml_config',
            '.toml': 'toml_config',
            '.ini': 'ini_config',
            '.cfg': 'config',
            '.conf': 'config',
            '.xml': 'xml_config',
            '.html': 'web_page',
            '.css': 'stylesheet',
            '.md': 'documentation',
            '.txt': 'text_document',
            '.csv': 'data_file',
            '.xlsx': 'spreadsheet',
            '.pdf': 'document',
            '.mp3': 'audio_file',
            '.wav': 'audio_file',
            '.flac': 'audio_file',
            '.mp4': 'video_file',
            '.mov': 'video_file',
            '.avi': 'video_file',
            '.jpg': 'image_file',
            '.jpeg': 'image_file',
            '.png': 'image_file',
            '.gif': 'image_file',
            '.svg': 'vector_image',
            '.pyc': 'compiled_python',
            '.db': 'database',
            '.sqlite': 'database',
            '.sqlite3': 'database',
            '.sql': 'sql_file',
            '.sh': 'shell_script',
            '.bash': 'shell_script',
            '.zsh': 'shell_script',
            '.pl': 'perl_script',
            '.rb': 'ruby_script',
            '.php': 'php_script',
            '.java': 'java_script',
            '.cpp': 'cpp_script',
            '.c': 'c_script',
            '.go': 'go_script',
            '.rs': 'rust_script',
            '.swift': 'swift_script',
            '.kt': 'kotlin_script'
        }
        
        if extension in extension_map:
            return extension_map[extension]
        
        # For files without extensions, try to determine type from content
        if extension == '':
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(1024)  # Read first 1KB
                    
                    if any(keyword in content.lower() for keyword in ['import', 'def', 'class', 'print']):
                        return 'python_script'
                    elif any(keyword in content.lower() for keyword in ['function', 'const', 'var', 'let']):
                        return 'javascript_script'
                    elif any(keyword in content.lower() for keyword in ['<!doctype', '<html', '<head', '<body']):
                        return 'web_page'
                    elif any(keyword in content.lower() for keyword in ['api', 'endpoint', 'route', 'server']):
                        return 'api_definition'
                    else:
                        return 'text_document'
            except:
                return 'unknown'
        
        return 'unknown'
    
    def _is_temp_or_system_file(self, file_path: Path) -> bool:
        """Check if file is a temporary or system file that should be excluded"""
        filename = file_path.name.lower()
        
        # Temporary file patterns
        temp_patterns = [
            '.tmp', '.temp', '.bak', '.backup', '.swp', '.lock',
            '~', '.cache', '.log', '.pid', '.sock', '.out', '.err',
            '.DS_Store', 'Thumbs.db', '.Spotlight-V100', '.Trashes'
        ]
        
        for pattern in temp_patterns:
            if pattern in filename:
                return True
                
        # Check for common temp/temporary in path
        path_str = str(file_path).lower()
        if any(keyword in path_str for keyword in ['temp', 'tmp', 'cache', 'log']):
            # But don't exclude important temp directories that might contain valuable assets
            if not any(allowed in path_str for allowed in ['automation', 'scripts', 'tools']):
                return True
        
        return False
    
    def _determine_business_vertical(self, relative_path: Path) -> str:
        """Determine business vertical based on file path"""
        path_str = str(relative_path).lower()
        
        # Map path keywords to business verticals
        vertical_keywords = {
            'ai': 'AI_Automation_Services',
            'automation': 'AI_Automation_Services',
            'music': 'Music_Production_Licensing',
            'audio': 'Music_Production_Licensing',
            'forensic': 'Forensic_Technology_Solutions',
            'dna': 'Forensic_Technology_Solutions',
            'research': 'AI_Research_Development',
            'ml': 'AI_Research_Development',
            'machine_learning': 'AI_Research_Development',
            'consult': 'AI_Consultation_Training',
            'train': 'AI_Consultation_Training',
            'course': 'AI_Consultation_Training',
            'ecommerce': 'Ecommerce_Print_on_Demand',
            'shop': 'Ecommerce_Print_on_Demand',
            'store': 'Ecommerce_Print_on_Demand',
            'voice': 'AI_Voice_Agents',
            'speech': 'AI_Voice_Agents',
            'tts': 'AI_Voice_Agents',
            'knowledge': 'Knowledge_Management_Systems',
            'wiki': 'Knowledge_Management_Systems',
            'docs': 'Knowledge_Management_Systems',
            'content': 'Creative_Content_Generation',
            'media': 'Creative_Content_Generation',
            'video': 'Video_Marketing',
            'youtube': 'Video_Marketing',
            'affiliate': 'Affiliate_Marketing',
            'marketing': 'Affiliate_Marketing',
            'product': 'Digital_Product_Sales',
            'sale': 'Digital_Product_Sales',
            'gumroad': 'Digital_Product_Sales',
            'codecanyon': 'Digital_Product_Sales',
            'osint': 'OSINT_Services',
            'intelligence': 'OSINT_Services',
            'investigate': 'OSINT_Services',
            'swarm': 'Swarm_Orchestration',
            'orchestrate': 'Swarm_Orchestration',
            'n8n': 'Swarm_Orchestration',
            'workflow': 'Swarm_Orchestration',
            'retention': 'SaaS_Retention_Solutions',
            'saas': 'SaaS_Retention_Solutions',
            'software': 'SaaS_Retention_Solutions',
            'ethical': 'Ethical_Hacking_Education',
            'hacking': 'Ethical_Hacking_Education',
            'security': 'Ethical_Hacking_Education',
            'narrative': 'Narrative_AI_Engine',
            'story': 'Narrative_AI_Engine',
            'writing': 'Narrative_AI_Engine',
            'notebook': 'NotebookLM_Publishing',
            'publish': 'NotebookLM_Publishing',
            'book': 'NotebookLM_Publishing',
            'library': 'Visual_Product_Libraries',
            'asset': 'Visual_Product_Libraries',
            'design': 'Visual_Product_Libraries',
            'curat': 'Content_Curation_Analytics',
            'analytic': 'Content_Curation_Analytics',
            'data': 'Content_Curation_Analytics'
        }
        
        # Check for keywords in path
        for keyword, vertical in vertical_keywords.items():
            if keyword in path_str:
                return vertical
        
        # Default to a general vertical if no specific match
        return 'AI_Automation_Services'  # Most common business vertical
    
    def _extract_tags(self, file_path: str) -> List[str]:
        """Extract tags from file path and name"""
        tags = []
        path_lower = file_path.lower()
        
        # Extract tags based on path structure
        path_parts = path_lower.split('/')
        
        for part in path_parts:
            if len(part) > 2:  # Avoid short directory names
                # Add meaningful directory names as tags
                if any(keyword in part for keyword in [
                    'api', 'web', 'mobile', 'desktop', 'cli', 'ui', 'ux',
                    'backend', 'frontend', 'devops', 'testing', 'docs',
                    'config', 'data', 'ml', 'ai', 'automation', 'tools',
                    'scripts', 'utils', 'lib', 'src', 'test', 'prod',
                    'dev', 'staging', 'api', 'service', 'microservice'
                ]):
                    tags.append(part)
        
        # Add file-specific tags
        if '.py' in path_lower:
            tags.append('python')
        if 'api' in path_lower:
            tags.append('api')
        if 'automation' in path_lower:
            tags.append('automation')
        if 'ai' in path_lower or 'ml' in path_lower:
            tags.extend(['ai', 'ml'])
        
        return list(set(tags))  # Remove duplicates
    
    def _extract_dependencies(self, file_path: str) -> List[str]:
        """Extract dependencies from code files"""
        dependencies = []
        
        try:
            ext = Path(file_path).suffix.lower()
            
            if ext == '.py':  # Python dependencies
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Find import statements
                    import_matches = re.findall(r'import\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
                    from_matches = re.findall(r'from\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+import', content)
                    
                    dependencies.extend(import_matches)
                    dependencies.extend(from_matches)
                    
                    # Remove duplicates and common built-ins
                    builtin_modules = {
                        'os', 'sys', 'json', 're', 'datetime', 'pathlib', 'typing',
                        'collections', 'itertools', 'functools', 'operator', 'math',
                        'random', 'statistics', 'decimal', 'fractions', 'numbers',
                        'copy', 'pprint', 'reprlib', 'enum', 'dataclasses', 'abc',
                        'io', 'tempfile', 'glob', 'fnmatch', 'linecache', 'pickle',
                        'shelve', 'shutil', 'zipfile', 'tarfile', 'csv', 'xml',
                        'html', 'urllib', 'http', 'ftplib', 'poplib', 'imaplib',
                        'smtplib', 'uuid', 'socket', 'ssl', 'ipaddress', 'cgi',
                        'cgitb', 'wsgiref', 'urllib', 'http', 'webbrowser',
                        'cgi', 'werkzeug', 'jinja2', 'markupsafe', 'babel',
                        'pytz', 'dateutil', 'requests', 'urllib3', 'charset_normalizer',
                        'idna', 'certifi', 'click', 'colorama', 'tqdm', 'numpy',
                        'pandas', 'matplotlib', 'seaborn', 'scipy', 'sklearn',
                        'tensorflow', 'torch', 'opencv', 'pillow', 'sqlalchemy',
                        'psycopg2', 'pymysql', 'sqlite3', 'asyncio', 'concurrent',
                        'multiprocessing', 'threading', 'queue', 'sched', 'signal',
                        'time', 'logging', 'warnings', 'weakref', 'gc', 'inspect',
                        'site', 'user', 'code', 'codeop', 'compileall', 'py_compile',
                        'zipimport', 'pkgutil', 'modulefinder', 'runpy', 'importlib',
                        'ast', 'symtable', 'tokenize', 'token', 'keyword', 'literal_eval',
                        'repr', 'ascii', 'ord', 'chr', 'len', 'str', 'int', 'float',
                        'bool', 'list', 'tuple', 'dict', 'set', 'frozenset', 'slice',
                        'property', 'super', 'isinstance', 'issubclass', 'hasattr',
                        'getattr', 'setattr', 'delattr', 'call', 'vars', 'locals',
                        'globals', 'exec', 'eval', 'compile', 'open', 'file', 'input',
                        'print', 'format', 'sorted', 'any', 'all', 'sum', 'max', 'min',
                        'abs', 'round', 'pow', 'divmod', 'range', 'enumerate', 'zip',
                        'filter', 'map', 'reduce', 'next', 'iter', 'bytes', 'bytearray',
                        'memoryview', 'complex', 'float', 'int', 'bool', 'str', 'list',
                        'tuple', 'dict', 'set', 'frozenset', 'type', 'object', 'class',
                        'def', 'lambda', 'if', 'elif', 'else', 'for', 'while', 'break',
                        'continue', 'pass', 'return', 'yield', 'with', 'as', 'try',
                        'except', 'finally', 'raise', 'assert', 'del', 'global', 'nonlocal',
                        'async', 'await', 'class', 'self', 'cls', 'staticmethod',
                        'classmethod', 'property', 'slots', 'metaclass', 'new', 'init',
                        'str', 'repr', 'add', 'sub', 'mul', 'div', 'mod', 'pow', 'and',
                        'or', 'xor', 'lshift', 'rshift', 'neg', 'pos', 'abs', 'invert',
                        'eq', 'ne', 'lt', 'le', 'gt', 'ge', 'len', 'getitem', 'setitem',
                        'delitem', 'contains', 'iter', 'next', 'enter', 'exit'
                    }
                    
                    dependencies = [dep for dep in dependencies if dep not in builtin_modules]
                    
            elif ext in ['.js', '.ts']:  # JavaScript/TypeScript dependencies
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Find import/require statements
                    import_matches = re.findall(r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]', content)
                    require_matches = re.findall(r'require\s*\(\s*[\'"](.+?)[\'"]\s*\)', content)
                    
                    dependencies.extend(import_matches)
                    dependencies.extend(require_matches)
        
        except Exception as e:
            logger.warning(f"Could not extract dependencies from {file_path}: {e}")
        
        return list(set(dependencies))
    
    def load_assets(self):
        """Load assets from the file system and update the database"""
        logger.info("Starting asset loading process...")
        
        # Scan key directories in the ecosystem
        scan_directories = [
            "/Users/steven",
            "/Users/steven/pythons",
            "/Users/steven/scripts",
            "/Users/steven/tools",
            "/Users/steven/automation_ecosystem",
            "/Users/steven/AVATARARTS",
            "/Users/steven/agents",
            "/Users/steven/nocTurneMeLoDieS",
            "/Users/steven/DNA_COLD_CASE_AI_PROGRAM",
            "/Users/steven/upwork_automation",
            "/Users/steven/n8n",
            "/Users/steven/.env.d"
        ]
        
        all_assets = []
        
        for directory in scan_directories:
            if os.path.exists(directory):
                logger.info(f"Scanning directory: {directory}")
                assets = self.scan_directory(directory)
                all_assets.extend(assets)
                logger.info(f"Found {len(assets)} assets in {directory}")
        
        logger.info(f"Total assets found: {len(all_assets)}")
        
        # Insert or update assets in database
        cursor = self.assets_db.cursor()
        
        for asset in all_assets:
            cursor.execute('''
                INSERT OR REPLACE INTO assets 
                (id, name, path, type, business_vertical, business_value_score, 
                 revenue_potential, usage_count, last_used, created_at, tags, dependencies, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                asset['id'], asset['name'], asset['path'], asset['type'],
                asset['business_vertical'], asset['business_value_score'],
                asset['revenue_potential'], asset['usage_count'],
                asset['last_used'], asset['created_at'],
                json.dumps(asset['tags']), json.dumps(asset['dependencies']), asset['status']
            ))
        
        self.assets_db.commit()
        logger.info(f"Successfully loaded {len(all_assets)} assets into database")
    
    def get_assets_by_business_value(self, min_value: float = 0, max_value: float = 10, limit: int = 100) -> List[Dict]:
        """Get assets filtered by business value score"""
        cursor = self.assets_db.cursor()
        cursor.execute('''
            SELECT * FROM assets 
            WHERE business_value_score BETWEEN ? AND ?
            ORDER BY business_value_score DESC
            LIMIT ?
        ''', (min_value, max_value, limit))
        
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        assets = []
        for row in rows:
            asset_dict = dict(zip(columns, row))
            # Parse JSON fields
            asset_dict['tags'] = json.loads(asset_dict['tags']) if asset_dict['tags'] else []
            asset_dict['dependencies'] = json.loads(asset_dict['dependencies']) if asset_dict['dependencies'] else []
            assets.append(asset_dict)
        
        return assets
    
    def get_assets_by_vertical(self, business_vertical: str) -> List[Dict]:
        """Get assets for a specific business vertical"""
        cursor = self.assets_db.cursor()
        cursor.execute('''
            SELECT * FROM assets 
            WHERE business_vertical = ?
            ORDER BY business_value_score DESC
        ''', (business_vertical,))
        
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        assets = []
        for row in rows:
            asset_dict = dict(zip(columns, row))
            # Parse JSON fields
            asset_dict['tags'] = json.loads(asset_dict['tags']) if asset_dict['tags'] else []
            asset_dict['dependencies'] = json.loads(asset_dict['dependencies']) if asset_dict['dependencies'] else []
            assets.append(asset_dict)
        
        return assets
    
    def get_top_revenue_assets(self, limit: int = 50) -> List[Dict]:
        """Get top assets by revenue potential"""
        cursor = self.assets_db.cursor()
        cursor.execute('''
            SELECT * FROM assets 
            ORDER BY revenue_potential DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        assets = []
        for row in rows:
            asset_dict = dict(zip(columns, row))
            # Parse JSON fields
            asset_dict['tags'] = json.loads(asset_dict['tags']) if asset_dict['tags'] else []
            asset_dict['dependencies'] = json.loads(asset_dict['dependencies']) if asset_dict['dependencies'] else []
            assets.append(asset_dict)
        
        return assets
    
    def get_dashboard_metrics(self) -> Dict[str, Any]:
        """Generate comprehensive dashboard metrics"""
        cursor = self.assets_db.cursor()
        
        # Total assets
        cursor.execute('SELECT COUNT(*) FROM assets')
        total_assets = cursor.fetchone()[0]
        
        # Assets by type
        cursor.execute('SELECT type, COUNT(*) FROM assets GROUP BY type ORDER BY COUNT(*) DESC')
        assets_by_type = dict(cursor.fetchall())
        
        # Assets by business vertical
        cursor.execute('SELECT business_vertical, COUNT(*) FROM assets GROUP BY business_vertical ORDER BY COUNT(*) DESC')
        assets_by_vertical = dict(cursor.fetchall())
        
        # Average business value by vertical
        cursor.execute('SELECT business_vertical, AVG(business_value_score) FROM assets GROUP BY business_vertical ORDER BY AVG(business_value_score) DESC')
        avg_value_by_vertical = dict(cursor.fetchall())
        
        # Total revenue potential
        cursor.execute('SELECT SUM(revenue_potential) FROM assets')
        total_revenue_potential = cursor.fetchone()[0] or 0
        
        # Assets by status
        cursor.execute('SELECT status, COUNT(*) FROM assets GROUP BY status')
        assets_by_status = dict(cursor.fetchall())
        
        # High value assets (business value >= 7.0)
        cursor.execute('SELECT COUNT(*) FROM assets WHERE business_value_score >= 7.0')
        high_value_assets = cursor.fetchone()[0]
        
        # Recently added assets (last 30 days)
        cursor.execute("SELECT COUNT(*) FROM assets WHERE created_at > datetime('now', '-30 days')")
        recent_assets = cursor.fetchone()[0]
        
        metrics = {
            'total_assets': total_assets,
            'assets_by_type': assets_by_type,
            'assets_by_vertical': assets_by_vertical,
            'avg_value_by_vertical': avg_value_by_vertical,
            'total_revenue_potential': total_revenue_potential,
            'assets_by_status': assets_by_status,
            'high_value_assets': high_value_assets,
            'recent_assets': recent_assets,
            'business_verticals_summary': {
                vertical: {
                    'count': count,
                    'avg_value': avg_value_by_vertical.get(vertical, 0),
                    'revenue_potential': sum(
                        cursor.execute('SELECT revenue_potential FROM assets WHERE business_vertical = ?', (vertical,)).fetchall()
                    ) if count > 0 else 0
                }
                for vertical, count in assets_by_vertical.items()
            }
        }
        
        return metrics
    
    def generate_business_report(self) -> str:
        """Generate a comprehensive business report"""
        metrics = self.get_dashboard_metrics()
        
        report = []
        report.append("# Steven's Automation Ecosystem - Business Report")
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        report.append("## Executive Summary")
        report.append(f"- Total Assets: {metrics['total_assets']:,}")
        report.append(f"- Total Revenue Potential: ${metrics['total_revenue_potential']:,.2f}/year")
        report.append(f"- High-Value Assets (≥7.0): {metrics['high_value_assets']:,}")
        report.append(f"- Recent Additions (30 days): {metrics['recent_assets']:,}")
        report.append("")
        
        report.append("## Business Verticals Performance")
        for vertical, data in sorted(metrics['business_verticals_summary'].items(), 
                                     key=lambda x: x[1]['revenue_potential'], reverse=True)[:10]:
            report.append(f"- **{vertical}**: {data['count']} assets, "
                         f"Avg Value: {data['avg_value']:.2f}, "
                         f"Revenue Potential: ${data['revenue_potential']:,.2f}")
        report.append("")
        
        report.append("## Asset Types Distribution")
        for asset_type, count in sorted(metrics['assets_by_type'].items(), 
                                        key=lambda x: x[1], reverse=True)[:10]:
            report.append(f"- **{asset_type}**: {count:,} assets")
        report.append("")
        
        report.append("## Asset Status")
        for status, count in metrics['assets_by_status'].items():
            report.append(f"- **{status}**: {count:,} assets")
        report.append("")
        
        report.append("## Top Revenue-Generating Opportunities")
        top_revenue_assets = self.get_top_revenue_assets(10)
        for i, asset in enumerate(top_revenue_assets, 1):
            report.append(f"{i}. **{asset['name']}** (${asset['revenue_potential']:,.2f}) - "
                         f"{asset['business_vertical']} | {asset['type']}")
        report.append("")
        
        return "\n".join(report)
    
    def execute_asset_safely(self, asset_id: str) -> Dict[str, Any]:
        """Safely execute an asset with proper validation and error handling"""
        cursor = self.assets_db.cursor()
        cursor.execute('SELECT * FROM assets WHERE id = ?', (asset_id,))
        asset_row = cursor.fetchone()
        
        if not asset_row:
            return {'success': False, 'error': f'Asset with ID {asset_id} not found'}
        
        # Parse the asset data
        columns = [description[0] for description in cursor.description]
        asset = dict(zip(columns, asset_row))
        asset['tags'] = json.loads(asset['tags']) if asset['tags'] else []
        asset['dependencies'] = json.loads(asset['dependencies']) if asset['dependencies'] else []
        
        # Log the execution attempt
        cursor.execute('''
            INSERT INTO asset_usage_log (asset_id, action) 
            VALUES (?, ?)
        ''', (asset_id, 'execution_attempt'))
        
        # Update asset usage statistics
        cursor.execute('''
            UPDATE assets 
            SET usage_count = usage_count + 1, last_used = CURRENT_TIMESTAMP 
            WHERE id = ?
        ''', (asset_id,))
        
        self.assets_db.commit()
        
        try:
            file_path = asset['path']
            file_ext = Path(file_path).suffix.lower()
            
            # Validate file type for safe execution
            allowed_extensions = ['.py', '.sh', '.js', '.ts', '.pl', '.rb', '.php']
            if file_ext not in allowed_extensions:
                return {
                    'success': False, 
                    'error': f'Execution not allowed for file type: {file_ext}',
                    'asset_info': asset
                }
            
            # For Python files, use subprocess to run safely
            if file_ext == '.py':
                result = subprocess.run(
                    [sys.executable, file_path],
                    capture_output=True,
                    text=True,
                    timeout=30,  # 30-second timeout
                    cwd=os.path.dirname(file_path)
                )
                
                execution_result = {
                    'success': result.returncode == 0,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'return_code': result.returncode,
                    'execution_time': 'N/A'  # subprocess doesn't provide execution time directly
                }
            
            # For shell scripts
            elif file_ext in ['.sh', '.bash', '.zsh']:
                result = subprocess.run(
                    ['bash', file_path],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=os.path.dirname(file_path)
                )
                
                execution_result = {
                    'success': result.returncode == 0,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'return_code': result.returncode
                }
            
            # For other script types, return not implemented
            else:
                return {
                    'success': False,
                    'error': f'Execution not yet implemented for file type: {file_ext}',
                    'asset_info': asset
                }
            
            # Log successful execution
            cursor.execute('''
                INSERT INTO asset_usage_log (asset_id, action) 
                VALUES (?, ?)
            ''', (asset_id, 'execution_success' if execution_result['success'] else 'execution_failed'))
            
            self.assets_db.commit()
            
            execution_result['asset_info'] = asset
            return execution_result
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Execution timed out after 30 seconds',
                'asset_info': asset
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'asset_info': asset
            }
    
    def get_optimization_suggestions(self) -> List[Dict[str, str]]:
        """Generate optimization suggestions for the ecosystem"""
        suggestions = []
        
        # Find high-value assets that aren't being used much
        cursor = self.assets_db.cursor()
        cursor.execute('''
            SELECT name, path, business_value_score, usage_count, business_vertical
            FROM assets 
            WHERE business_value_score >= 7.0 AND usage_count < 5
            ORDER BY business_value_score DESC
        ''')
        
        high_value_low_usage = cursor.fetchall()
        
        for asset in high_value_low_usage[:5]:  # Top 5 suggestions
            suggestions.append({
                'type': 'underutilized_asset',
                'title': f'Underutilized High-Value Asset: {asset[0]}',
                'description': f"'{asset[0]}' has high business value ({asset[2]:.1f}) but low usage ({asset[3]} times). Consider promoting this asset in {asset[4]}.",
                'path': asset[1]
            })
        
        # Find assets with high revenue potential
        cursor.execute('''
            SELECT name, path, revenue_potential, business_vertical
            FROM assets 
            WHERE revenue_potential > 10000
            ORDER BY revenue_potential DESC
        ''')
        
        high_revenue_assets = cursor.fetchall()
        
        for asset in high_revenue_assets[:5]:  # Top 5 suggestions
            suggestions.append({
                'type': 'revenue_opportunity',
                'title': f'High Revenue Opportunity: {asset[0]}',
                'description': f"'{asset[0]}' has revenue potential of ${asset[2]:,.2f}. Focus on monetizing this asset in {asset[3]}.",
                'path': asset[1]
            })
        
        # Find duplicate or similar assets that could be consolidated
        cursor.execute('''
            SELECT name, path, type, business_vertical, COUNT(*) as count
            FROM assets 
            GROUP BY name, type, business_vertical
            HAVING COUNT(*) > 1
        ''')
        
        duplicates = cursor.fetchall()
        
        for asset in duplicates[:5]:  # Top 5 suggestions
            suggestions.append({
                'type': 'consolidation_opportunity',
                'title': f'Potential Consolidation: {asset[0]}',
                'description': f"There are {asset[4]} versions of '{asset[0]}' in {asset[3]}. Consider consolidating to reduce redundancy.",
                'path': asset[1]
            })
        
        return suggestions
    
    def export_assets_to_csv(self, filepath: str, filters: Dict = None):
        """Export assets to CSV with optional filters"""
        cursor = self.assets_db.cursor()
        
        query = "SELECT * FROM assets"
        params = []
        
        if filters:
            conditions = []
            for key, value in filters.items():
                if key in ['type', 'business_vertical', 'status']:
                    conditions.append(f"{key} = ?")
                    params.append(value)
                elif key == 'min_business_value':
                    conditions.append("business_value_score >= ?")
                    params.append(value)
                elif key == 'max_business_value':
                    conditions.append("business_value_score <= ?")
                    params.append(value)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY business_value_score DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(columns)  # Header
            
            for row in rows:
                # Process JSON fields for CSV export
                processed_row = []
                for i, val in enumerate(row):
                    if columns[i] in ['tags', 'dependencies'] and val:
                        try:
                            val = json.loads(val)
                            val = ', '.join(val) if isinstance(val, list) else str(val)
                        except:
                            val = str(val)
                    processed_row.append(val)
                
                writer.writerow(processed_row)
    
    def close(self):
        """Close the database connection"""
        if self.assets_db:
            self.assets_db.close()
            logger.info("Database connection closed")


def main():
    """Main function to demonstrate the EcoSystem Orchestrator"""
    print("Initializing Steven's EcoSystem Orchestrator...")
    
    # Create the orchestrator instance
    orchestrator = EcoSystemOrchestrator()
    
    print("\n📊 Generating Dashboard Metrics...")
    metrics = orchestrator.get_dashboard_metrics()
    
    print(f"Total Assets: {metrics['total_assets']:,}")
    print(f"Total Revenue Potential: ${metrics['total_revenue_potential']:,.2f}/year")
    print(f"High-Value Assets (≥7.0): {metrics['high_value_assets']:,}")
    
    print("\n🏢 Business Verticals Summary:")
    for vertical, data in sorted(metrics['business_verticals_summary'].items(), 
                                 key=lambda x: x[1]['revenue_potential'], reverse=True)[:5]:
        print(f"  • {vertical}: {data['count']} assets, ${data['revenue_potential']:,.2f} potential")
    
    print("\n🔍 Top 5 High-Value Assets:")
    high_value_assets = orchestrator.get_assets_by_business_value(min_value=8.0, limit=5)
    for i, asset in enumerate(high_value_assets, 1):
        print(f"  {i}. {asset['name']} ({asset['business_value_score']:.1f}/10.0) - {asset['business_vertical']}")
    
    print("\n💡 Optimization Suggestions:")
    suggestions = orchestrator.get_optimization_suggestions()
    for suggestion in suggestions[:3]:
        print(f"  • {suggestion['title']}")
        print(f"    {suggestion['description']}")
    
    print("\n📈 Generating Business Report...")
    report = orchestrator.generate_business_report()
    
    # Save report to file
    report_path = "/Users/steven/ecosystem_business_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Business report saved to: {report_path}")
    
    print("\n📦 Exporting assets to CSV...")
    csv_path = "/Users/steven/ecosystem_assets_inventory.csv"
    orchestrator.export_assets_to_csv(csv_path)
    print(f"Assets inventory exported to: {csv_path}")
    
    print("\n✅ EcoSystem Orchestrator initialization complete!")
    print(f"The system has cataloged {metrics['total_assets']:,} assets")
    print(f"With a total revenue potential of ${metrics['total_revenue_potential']:,.2f}/year")
    print("Ready to manage your expanded automation ecosystem!")
    
    # Keep the orchestrator alive for potential use
    try:
        while True:
            command = input("\nEnter command (metrics/report/suggestions/export/quit): ").strip().lower()
            
            if command == 'metrics':
                metrics = orchestrator.get_dashboard_metrics()
                print(f"\n📊 Dashboard Metrics:")
                print(f"Total Assets: {metrics['total_assets']:,}")
                print(f"Revenue Potential: ${metrics['total_revenue_potential']:,.2f}/year")
                print(f"High-Value Assets: {metrics['high_value_assets']:,}")
                
            elif command == 'report':
                report = orchestrator.generate_business_report()
                print(f"\n📄 Business Report Preview:")
                print(report[:1000] + "..." if len(report) > 1000 else report)
                
            elif command == 'suggestions':
                suggestions = orchestrator.get_optimization_suggestions()
                print(f"\n💡 Optimization Suggestions:")
                for suggestion in suggestions[:5]:
                    print(f"  • {suggestion['title']}")
                    print(f"    {suggestion['description']}")
                    
            elif command == 'export':
                csv_path = f"/Users/steven/ecosystem_assets_export_{int(time.time())}.csv"
                orchestrator.export_assets_to_csv(csv_path)
                print(f"\📦 Assets exported to: {csv_path}")
                
            elif command == 'quit':
                break
            else:
                print("Unknown command. Available: metrics, report, suggestions, export, quit")
    
    except KeyboardInterrupt:
        print("\n\nShutting down EcoSystem Orchestrator...")
    finally:
        orchestrator.close()


if __name__ == "__main__":
    main()