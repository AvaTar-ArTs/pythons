
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_365 = 365
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Deep Analysis and Content-Aware Document System for ~/
Analyzes, categorizes, and optimizes file organization with intelligent sorting
"""

import os
import json
import hashlib
import mimetypes
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional
import re
import subprocess
from dataclasses import dataclass
from collections import defaultdict, Counter

@dataclass
class FileAnalysis:
    """Comprehensive file analysis data"""
    path: str
    name: str
    size: int
    size_formatted: str
    extension: str
    mime_type: str
    created: datetime
    modified: datetime
    accessed: datetime
    file_hash: str
    content_type: str
    category: str
    subcategory: str
    importance_score: float
    usage_frequency: str
    content_analysis: Dict[str, Any]
    optimization_suggestions: List[str]
    sorting_priority: int
    tags: List[str]
    relationships: List[str]
    duplicates: List[str]
    quality_score: float
    accessibility_score: float
    security_risk: str
    backup_priority: str

class ContentAnalyzer:
    """Deep content analysis for files"""
    
    def __init__(self):
        self.content_patterns = {
            'code': {
                'extensions': ['.py', '.js', '.html', '.css', '.php', '.java', '.cpp', '.c', '.go', '.rs', '.swift', '.kt'],
                'keywords': ['function', 'class', 'import', 'def', 'var', 'let', 'const', 'if', 'else', 'for', 'while'],
                'patterns': [r'def\s+\w+', r'class\s+\w+', r'function\s+\w+', r'import\s+\w+']
            },
            'document': {
                'extensions': ['.pdf', '.doc', '.docx', '.txt', '.md', '.rtf', '.odt'],
                'keywords': ['abstract', 'introduction', 'conclusion', 'chapter', 'section', 'figure', 'table'],
                'patterns': [r'#+\s+', r'\\chapter', r'\\section', r'\\subsection']
            },
            'data': {
                'extensions': ['.csv', '.json', '.xml', '.yaml', '.yml', '.sql', '.db', '.sqlite'],
                'keywords': ['data', 'record', 'field', 'column', 'row', 'table', 'database'],
                'patterns': [r'\\d+,\\d+', r'\\{[^}]+\\}', r'<[^>]+>', r'SELECT\\s+', r'INSERT\\s+']
            },
            'media': {
                'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.avi', '.mov', '.mp3', '.wav'],
                'keywords': ['image', 'video', 'audio', 'photo', 'picture', 'movie', 'song'],
                'patterns': [r'\\d+x\\d+', r'\\d+\\s*[kK]?[bB]', r'\\d+\\s*fps']
            },
            'config': {
                'extensions': ['.conf', '.ini', '.cfg', '.yaml', '.yml', '.toml', '.env'],
                'keywords': ['config', 'setting', 'option', 'parameter', 'value', 'key'],
                'patterns': [r'\\w+\\s*=\\s*\\w+', r'\\[\\w+\\]', r'\\w+:\\s*\\w+']
            }
        }
        
        self.importance_keywords = {
            'high': ['important', 'critical', 'urgent', 'priority', 'main', 'core', 'essential'],
            'medium': ['secondary', 'backup', 'archive', 'temp', 'draft', 'work'],
            'low': ['old', 'unused', 'deprecated', 'legacy', 'test', 'debug', 'trash']
        }
        
        self.security_patterns = {
            'sensitive': [r'password', r'secret', r'key', r'token', r'api', r'credential'],
            'personal': [r'personal', r'private', r'confidential', r'proprietary'],
            'financial': [r'bank', r'credit', r'payment', r'financial', r'tax', r'invoice']
        }
    
    def analyze_file_content(self, file_path: Path) -> Dict[str, Any]:
        """Analyze file content for deep insights"""
        analysis = {
            'content_type': 'unknown',
            'language': 'unknown',
            'complexity': 'low',
            'keywords': [],
            'patterns': [],
            'structure': 'unstructured',
            'quality_indicators': [],
            'security_flags': [],
            'readability_score': 0.0,
            'maintenance_score': 0.0
        }
        
        try:
            # Read file content (limit size for analysis)
            max_size = CONSTANT_1024 * CONSTANT_1024  # 1MB limit
            if file_path.stat().st_size > max_size:
                with open(file_path, 'rb') as f:
                    content = f.read(max_size).decode('utf-8', errors='ignore')
            else:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            
            # Analyze content type
            analysis['content_type'] = self._determine_content_type(file_path, content)
            
            # Extract keywords
            analysis['keywords'] = self._extract_keywords(content)
            
            # Detect patterns
            analysis['patterns'] = self._detect_patterns(content)
            
            # Analyze structure
            analysis['structure'] = self._analyze_structure(content)
            
            # Quality indicators
            analysis['quality_indicators'] = self._assess_quality(content)
            
            # Security analysis
            analysis['security_flags'] = self._check_security(content)
            
            # Calculate scores
            analysis['readability_score'] = self._calculate_readability(content)
            analysis['maintenance_score'] = self._calculate_maintenance(content)
            
        except Exception as e:
            analysis['error'] = str(e)
        
        return analysis
    
    def _determine_content_type(self, file_path: Path, content: str) -> str:
        """Determine detailed content type"""
        ext = file_path.suffix.lower()
        
        for content_type, patterns in self.content_patterns.items():
            if ext in patterns['extensions']:
                return content_type
        
        # Analyze content for additional clues
        if any(keyword in content.lower() for keyword in ['function', 'class', 'import']):
            return 'code'
        elif any(keyword in content.lower() for keyword in ['chapter', 'section', 'abstract']):
            return 'document'
        elif any(keyword in content.lower() for keyword in ['data', 'record', 'field']):
            return 'data'
        
        return 'unknown'
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract important keywords from content"""
        # Simple keyword extraction
        words = re.findall(r'\b[a-zA-Z]{3,}\b', content.lower())
        word_freq = Counter(words)
        
        # Filter out common words
        common_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'}
        
        keywords = [word for word, freq in word_freq.most_common(20) 
                   if word not in common_words and freq > 1]
        
        return keywords[:10]  # Top 10 keywords
    
    def _detect_patterns(self, content: str) -> List[str]:
        """Detect patterns in content"""
        patterns = []
        
        for content_type, pattern_info in self.content_patterns.items():
            for pattern in pattern_info['patterns']:
                if re.search(pattern, content, re.IGNORECASE):
                    patterns.append(f"{content_type}_{pattern}")
        
        return patterns
    
    def _analyze_structure(self, content: str) -> str:
        """Analyze content structure"""
        lines = content.split('\n')
        
        if len(lines) < 10:
            return 'minimal'
        elif any(line.strip().startswith('#') for line in lines[:20]):
            return 'document'
        elif any(line.strip().startswith('def ') or line.strip().startswith('class ') for line in lines):
            return 'code'
        elif any(line.strip().startswith('[') or line.strip().startswith('{') for line in lines):
            return 'data'
        else:
            return 'unstructured'
    
    def _assess_quality(self, content: str) -> List[str]:
        """Assess content quality indicators"""
        indicators = []
        
        # Check for documentation
        if any(word in content.lower() for word in ['readme', 'documentation', 'comment', 'explain']):
            indicators.append('documented')
        
        # Check for version control
        if any(word in content.lower() for word in ['version', 'v1', 'v2', 'changelog', 'update']):
            indicators.append('versioned')
        
        # Check for error handling
        if any(word in content.lower() for word in ['try', 'catch', 'except', 'error', 'handle']):
            indicators.append('error_handling')
        
        # Check for testing
        if any(word in content.lower() for word in ['test', 'spec', 'assert', 'check']):
            indicators.append('tested')
        
        return indicators
    
    def _check_security(self, content: str) -> List[str]:
        """Check for security-related content"""
        flags = []
        
        for category, patterns in self.security_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    flags.append(category)
        
        return flags
    
    def _calculate_readability(self, content: str) -> float:
        """Calculate readability score (0-1)"""
        # Simple readability calculation
        sentences = len(re.findall(r'[.!?]+', content))
        words = len(content.split())
        
        if sentences == 0:
            return 0.0
        
        avg_words_per_sentence = words / sentences
        readability = max(0, 1 - (avg_words_per_sentence - 10) / 20)
        
        return min(1.0, max(0.0, readability))
    
    def _calculate_maintenance(self, content: str) -> float:
        """Calculate maintenance score (0-1)"""
        score = 0.0
        
        # Check for comments
        comment_lines = len([line for line in content.split('\n') if line.strip().startswith('#') or line.strip().startswith('//')])
        total_lines = len([line for line in content.split('\n') if line.strip()])
        
        if total_lines > 0:
            comment_ratio = comment_lines / total_lines
            score += comment_ratio * 0.3
        
        # Check for documentation
        if any(word in content.lower() for word in ['readme', 'doc', 'help', 'guide']):
            score += 0.2
        
        # Check for structure
        if any(word in content.lower() for word in ['function', 'class', 'module', 'component']):
            score += 0.2
        
        # Check for error handling
        if any(word in content.lower() for word in ['try', 'catch', 'except', 'error']):
            score += 0.2
        
        # Check for testing
        if any(word in content.lower() for word in ['test', 'spec', 'assert']):
            score += 0.1
        
        return min(1.0, score)

class FileSystemAnalyzer:
    """Analyzes file system structure and relationships"""
    
    def __init__(self):
        self.analyzer = ContentAnalyzer()
        self.file_hashes = {}
        self.duplicate_groups = defaultdict(list)
        self.relationship_map = defaultdict(list)
    
    def analyze_directory(self, root_path: str, max_depth: int = 10) -> List[FileAnalysis]:
        """Perform deep analysis of directory structure"""
        logger.info(f"🔍 Starting deep analysis of {root_path}...")
        
        root = Path(root_path)
        analyses = []
        processed = 0
        
        for file_path in root.rglob('*'):
            if file_path.is_file() and not self._should_skip_file(file_path):
                try:
                    analysis = self._analyze_single_file(file_path)
                    analyses.append(analysis)
                    processed += 1
                    
                    if processed % CONSTANT_100 == 0:
                        logger.info(f"  Processed {processed} files...")
                        
                except Exception as e:
                    logger.info(f"⚠️  Error analyzing {file_path}: {e}")
                    continue
        
        logger.info(f"✅ Analysis complete: {len(analyses)} files analyzed")
        return analyses
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """Determine if file should be skipped"""
        skip_patterns = [
            '.git', '.DS_Store', '.Trash', '.cache', '.tmp',
            'node_modules', '.venv', '__pycache__', '.pytest_cache',
            'Library/Caches', 'Library/Logs', 'Library/Application Support'
        ]
        
        return any(pattern in str(file_path) for pattern in skip_patterns)
    
    def _analyze_single_file(self, file_path: Path) -> FileAnalysis:
        """Analyze a single file comprehensively"""
        stat = file_path.stat()
        
        # Basic file info
        name = file_path.name
        size = stat.st_size
        extension = file_path.suffix.lower()
        mime_type = mimetypes.guess_type(str(file_path))[0] or 'unknown'
        
        # Timestamps
        created = datetime.fromtimestamp(stat.st_birthtime)
        modified = datetime.fromtimestamp(stat.st_mtime)
        accessed = datetime.fromtimestamp(stat.st_atime)
        
        # File hash for duplicate detection
        file_hash = self._calculate_file_hash(file_path)
        self.file_hashes[file_hash] = file_path
        self.duplicate_groups[file_hash].append(str(file_path))
        
        # Content analysis
        content_analysis = self.analyzer.analyze_file_content(file_path)
        
        # Determine category and subcategory
        category, subcategory = self._categorize_file(file_path, content_analysis)
        
        # Calculate importance score
        importance_score = self._calculate_importance(file_path, content_analysis)
        
        # Determine usage frequency
        usage_frequency = self._determine_usage_frequency(modified, accessed)
        
        # Generate optimization suggestions
        optimization_suggestions = self._generate_optimization_suggestions(file_path, content_analysis)
        
        # Calculate sorting priority
        sorting_priority = self._calculate_sorting_priority(file_path, content_analysis, importance_score)
        
        # Generate tags
        tags = self._generate_tags(file_path, content_analysis)
        
        # Find relationships
        relationships = self._find_relationships(file_path, content_analysis)
        
        # Find duplicates
        duplicates = [p for p in self.duplicate_groups[file_hash] if p != str(file_path)]
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(content_analysis)
        
        # Calculate accessibility score
        accessibility_score = self._calculate_accessibility_score(file_path, content_analysis)
        
        # Assess security risk
        security_risk = self._assess_security_risk(content_analysis)
        
        # Determine backup priority
        backup_priority = self._determine_backup_priority(importance_score, security_risk, modified)
        
        return FileAnalysis(
            path=str(file_path),
            name=name,
            size=size,
            size_formatted=self._format_size(size),
            extension=extension,
            mime_type=mime_type,
            created=created,
            modified=modified,
            accessed=accessed,
            file_hash=file_hash,
            content_type=content_analysis.get('content_type', 'unknown'),
            category=category,
            subcategory=subcategory,
            importance_score=importance_score,
            usage_frequency=usage_frequency,
            content_analysis=content_analysis,
            optimization_suggestions=optimization_suggestions,
            sorting_priority=sorting_priority,
            tags=tags,
            relationships=relationships,
            duplicates=duplicates,
            quality_score=quality_score,
            accessibility_score=accessibility_score,
            security_risk=security_risk,
            backup_priority=backup_priority
        )
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate file hash for duplicate detection"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except (OSError, IOError, FileNotFoundError):
            return str(file_path.stat().st_size)  # Fallback to size
    
    def _categorize_file(self, file_path: Path, content_analysis: Dict) -> Tuple[str, str]:
        """Categorize file based on path and content"""
        path_str = str(file_path).lower()
        content_type = content_analysis.get('content_type', 'unknown')
        
        # Determine main category
        if 'desktop' in path_str or 'documents' in path_str:
            category = 'personal'
        elif 'downloads' in path_str:
            category = 'downloads'
        elif 'pictures' in path_str or 'photos' in path_str:
            category = 'media'
        elif 'music' in path_str or 'audio' in path_str:
            category = 'media'
        elif 'movies' in path_str or 'videos' in path_str:
            category = 'media'
        elif 'applications' in path_str or '.app' in path_str:
            category = 'applications'
        elif 'library' in path_str:
            category = 'system'
        elif content_type == 'code':
            category = 'development'
        elif content_type == 'document':
            category = 'documents'
        elif content_type == 'data':
            category = 'data'
        else:
            category = 'other'
        
        # Determine subcategory
        if content_type == 'code':
            subcategory = 'source_code'
        elif content_type == 'document':
            subcategory = 'text_documents'
        elif content_type == 'data':
            subcategory = 'data_files'
        elif content_type == 'media':
            subcategory = 'multimedia'
        elif content_type == 'config':
            subcategory = 'configuration'
        else:
            subcategory = 'general'
        
        return category, subcategory
    
    def _calculate_importance(self, file_path: Path, content_analysis: Dict) -> float:
        """Calculate importance score (0-1)"""
        score = 0.0
        
        # Path-based importance
        path_str = str(file_path).lower()
        if any(word in path_str for word in ['important', 'critical', 'main', 'core']):
            score += 0.3
        elif any(word in path_str for word in ['backup', 'archive', 'old', 'temp']):
            score -= 0.2
        
        # Content-based importance
        keywords = content_analysis.get('keywords', [])
        for keyword in keywords:
            if keyword in self.analyzer.importance_keywords['high']:
                score += 0.2
            elif keyword in self.analyzer.importance_keywords['low']:
                score -= 0.1
        
        # File type importance
        if content_analysis.get('content_type') == 'code':
            score += 0.1
        elif content_analysis.get('content_type') == 'document':
            score += 0.05
        
        # Quality indicators
        quality_indicators = content_analysis.get('quality_indicators', [])
        score += len(quality_indicators) * 0.05
        
        return max(0.0, min(1.0, score))
    
    def _determine_usage_frequency(self, modified: datetime, accessed: datetime) -> str:
        """Determine usage frequency based on timestamps"""
        now = datetime.now()
        days_since_modified = (now - modified).days
        days_since_accessed = (now - accessed).days
        
        if days_since_accessed < 7:
            return 'frequent'
        elif days_since_accessed < 30:
            return 'regular'
        elif days_since_accessed < 90:
            return 'occasional'
        else:
            return 'rare'
    
    def _generate_optimization_suggestions(self, file_path: Path, content_analysis: Dict) -> List[str]:
        """Generate optimization suggestions for file"""
        suggestions = []
        
        # Size-based suggestions
        if file_path.stat().st_size > CONSTANT_100 * CONSTANT_1024 * CONSTANT_1024:  # 100MB
            suggestions.append("Consider compressing or archiving large file")
        
        # Content-based suggestions
        if content_analysis.get('content_type') == 'code':
            if 'documented' not in content_analysis.get('quality_indicators', []):
                suggestions.append("Add documentation and comments")
            if 'tested' not in content_analysis.get('quality_indicators', []):
                suggestions.append("Add unit tests")
        
        # Security suggestions
        security_flags = content_analysis.get('security_flags', [])
        if security_flags:
            suggestions.append(f"Review for sensitive information: {', '.join(security_flags)}")
        
        # Structure suggestions
        if content_analysis.get('structure') == 'unstructured':
            suggestions.append("Consider organizing content with clear structure")
        
        return suggestions
    
    def _calculate_sorting_priority(self, file_path: Path, content_analysis: Dict, importance_score: float) -> int:
        """Calculate sorting priority (1-10, higher = more important)"""
        priority = 5  # Base priority
        
        # Adjust based on importance
        priority += int(importance_score * 3)
        
        # Adjust based on content type
        content_type = content_analysis.get('content_type', 'unknown')
        if content_type == 'code':
            priority += 2
        elif content_type == 'document':
            priority += 1
        
        # Adjust based on usage frequency
        usage_frequency = self._determine_usage_frequency(
            datetime.fromtimestamp(file_path.stat().st_mtime),
            datetime.fromtimestamp(file_path.stat().st_atime)
        )
        if usage_frequency == 'frequent':
            priority += 2
        elif usage_frequency == 'rare':
            priority -= 1
        
        return max(1, min(10, priority))
    
    def _generate_tags(self, file_path: Path, content_analysis: Dict) -> List[str]:
        """Generate tags for file"""
        tags = []
        
        # Content type tags
        content_type = content_analysis.get('content_type', 'unknown')
        tags.append(content_type)
        
        # Quality tags
        quality_indicators = content_analysis.get('quality_indicators', [])
        tags.extend(quality_indicators)
        
        # Security tags
        security_flags = content_analysis.get('security_flags', [])
        tags.extend(security_flags)
        
        # Keyword tags
        keywords = content_analysis.get('keywords', [])[:5]  # Top 5 keywords
        tags.extend(keywords)
        
        return list(set(tags))  # Remove duplicates
    
    def _find_relationships(self, file_path: Path, content_analysis: Dict) -> List[str]:
        """Find related files"""
        relationships = []
        
        # Find files with similar names
        parent_dir = file_path.parent
        base_name = file_path.stem
        
        for other_file in parent_dir.iterdir():
            if other_file.is_file() and other_file != file_path:
                if base_name in other_file.stem or other_file.stem in base_name:
                    relationships.append(str(other_file))
        
        return relationships[:5]  # Limit to 5 relationships
    
    def _calculate_quality_score(self, content_analysis: Dict) -> float:
        """Calculate overall quality score (0-1)"""
        score = 0.0
        
        # Readability score
        score += content_analysis.get('readability_score', 0) * 0.3
        
        # Maintenance score
        score += content_analysis.get('maintenance_score', 0) * 0.3
        
        # Quality indicators
        quality_indicators = content_analysis.get('quality_indicators', [])
        score += len(quality_indicators) * 0.1
        
        # Structure score
        structure = content_analysis.get('structure', 'unstructured')
        if structure == 'code':
            score += 0.2
        elif structure == 'document':
            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_accessibility_score(self, file_path: Path, content_analysis: Dict) -> float:
        """Calculate accessibility score (0-1)"""
        score = 0.5  # Base score
        
        # File type accessibility
        extension = file_path.suffix.lower()
        accessible_extensions = ['.txt', '.md', '.html', '.pdf', '.doc', '.docx']
        if extension in accessible_extensions:
            score += 0.3
        
        # Content structure
        structure = content_analysis.get('structure', 'unstructured')
        if structure in ['document', 'code']:
            score += 0.2
        
        return min(1.0, score)
    
    def _assess_security_risk(self, content_analysis: Dict) -> str:
        """Assess security risk level"""
        security_flags = content_analysis.get('security_flags', [])
        
        if 'sensitive' in security_flags or 'financial' in security_flags:
            return 'high'
        elif 'personal' in security_flags:
            return 'medium'
        else:
            return 'low'
    
    def _determine_backup_priority(self, importance_score: float, security_risk: str, modified: datetime) -> str:
        """Determine backup priority"""
        if security_risk == 'high' or importance_score > 0.8:
            return 'critical'
        elif security_risk == 'medium' or importance_score > 0.6:
            return 'high'
        elif importance_score > 0.4:
            return 'medium'
        else:
            return 'low'
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= CONSTANT_1024 and i < len(size_names) - 1:
            size_bytes /= CONSTANT_1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"

class OptimizationEngine:
    """Generates optimization recommendations and sorting improvements"""
    
    def __init__(self, analyses: List[FileAnalysis]):
        self.analyses = analyses
        self.categories = defaultdict(list)
        self.duplicates = defaultdict(list)
        self.relationships = defaultdict(list)
        
        # Organize data
        for analysis in analyses:
            self.categories[analysis.category].append(analysis)
            if analysis.duplicates:
                self.duplicates[analysis.file_hash].extend(analysis.duplicates)
            for rel in analysis.relationships:
                self.relationships[analysis.path].append(rel)
    
    def generate_optimization_report(self) -> Dict[str, Any]:
        """Generate comprehensive optimization report"""
        logger.info("📊 Generating optimization report...")
        
        report = {
            'summary': self._generate_summary(),
            'categories': self._analyze_categories(),
            'duplicates': self._analyze_duplicates(),
            'optimization_suggestions': self._generate_optimization_suggestions(),
            'sorting_recommendations': self._generate_sorting_recommendations(),
            'security_analysis': self._analyze_security(),
            'quality_analysis': self._analyze_quality(),
            'backup_recommendations': self._generate_backup_recommendations(),
            'file_organization': self._generate_organization_plan()
        }
        
        return report
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics"""
        total_files = len(self.analyses)
        total_size = sum(a.size for a in self.analyses)
        
        categories = Counter(a.category for a in self.analyses)
        content_types = Counter(a.content_type for a in self.analyses)
        usage_frequencies = Counter(a.usage_frequency for a in self.analyses)
        
        return {
            'total_files': total_files,
            'total_size': total_size,
            'total_size_formatted': self._format_size(total_size),
            'categories': dict(categories),
            'content_types': dict(content_types),
            'usage_frequencies': dict(usage_frequencies),
            'average_importance': sum(a.importance_score for a in self.analyses) / total_files,
            'average_quality': sum(a.quality_score for a in self.analyses) / total_files
        }
    
    def _analyze_categories(self) -> Dict[str, Any]:
        """Analyze file categories"""
        category_analysis = {}
        
        for category, files in self.categories.items():
            total_size = sum(f.size for f in files)
            avg_importance = sum(f.importance_score for f in files) / len(files)
            avg_quality = sum(f.quality_score for f in files) / len(files)
            
            category_analysis[category] = {
                'file_count': len(files),
                'total_size': total_size,
                'total_size_formatted': self._format_size(total_size),
                'average_importance': avg_importance,
                'average_quality': avg_quality,
                'top_files': sorted(files, key=lambda x: x.importance_score, reverse=True)[:5]
            }
        
        return category_analysis
    
    def _analyze_duplicates(self) -> Dict[str, Any]:
        """Analyze duplicate files"""
        duplicate_analysis = {
            'total_duplicates': len(self.duplicates),
            'total_wasted_space': 0,
            'duplicate_groups': []
        }
        
        for file_hash, duplicate_paths in self.duplicates.items():
            if len(duplicate_paths) > 1:
                # Find the original file
                original = next((a for a in self.analyses if a.file_hash == file_hash), None)
                if original:
                    wasted_space = original.size * (len(duplicate_paths) - 1)
                    duplicate_analysis['total_wasted_space'] += wasted_space
                    
                    duplicate_analysis['duplicate_groups'].append({
                        'file_hash': file_hash,
                        'original_path': original.path,
                        'duplicate_paths': duplicate_paths[1:],
                        'file_size': original.size,
                        'wasted_space': wasted_space,
                        'wasted_space_formatted': self._format_size(wasted_space)
                    })
        
        duplicate_analysis['total_wasted_space_formatted'] = self._format_size(duplicate_analysis['total_wasted_space'])
        
        return duplicate_analysis
    
    def _generate_optimization_suggestions(self) -> List[Dict[str, Any]]:
        """Generate optimization suggestions"""
        suggestions = []
        
        # Duplicate removal
        if self.duplicates:
            suggestions.append({
                'type': 'duplicate_removal',
                'priority': 'high',
                'title': 'Remove Duplicate Files',
                'description': f'Found {len(self.duplicates)} duplicate file groups',
                'potential_savings': self._format_size(sum(original.size * (len(dups) - 1) for original, dups in [(next((a for a in self.analyses if a.file_hash == h), None), paths) for h, paths in self.duplicates.items()] if original and len(paths) > 1)),
                'action': 'Review and remove duplicate files'
            })
        
        # Large file optimization
        large_files = [a for a in self.analyses if a.size > CONSTANT_100 * CONSTANT_1024 * CONSTANT_1024]  # 100MB
        if large_files:
            suggestions.append({
                'type': 'large_file_optimization',
                'priority': 'medium',
                'title': 'Optimize Large Files',
                'description': f'Found {len(large_files)} files larger than 100MB',
                'files': [{'path': f.path, 'size': f.size_formatted} for f in large_files[:10]],
                'action': 'Consider compressing or archiving large files'
            })
        
        # Low quality files
        low_quality_files = [a for a in self.analyses if a.quality_score < 0.3]
        if low_quality_files:
            suggestions.append({
                'type': 'quality_improvement',
                'priority': 'low',
                'title': 'Improve File Quality',
                'description': f'Found {len(low_quality_files)} files with low quality scores',
                'action': 'Review and improve file content and structure'
            })
        
        return suggestions
    
    def _generate_sorting_recommendations(self) -> Dict[str, Any]:
        """Generate sorting and organization recommendations"""
        # Sort files by priority
        sorted_files = sorted(self.analyses, key=lambda x: x.sorting_priority, reverse=True)
        
        # Group by category and priority
        organized_files = defaultdict(list)
        for file_analysis in sorted_files:
            organized_files[file_analysis.category].append(file_analysis)
        
        # Generate recommendations
        recommendations = {
            'high_priority_files': [f for f in sorted_files if f.sorting_priority >= 8][:20],
            'category_organization': {},
            'access_patterns': self._analyze_access_patterns(),
            'storage_optimization': self._generate_storage_optimization()
        }
        
        # Category-specific organization
        for category, files in organized_files.items():
            recommendations['category_organization'][category] = {
                'total_files': len(files),
                'high_priority': [f for f in files if f.sorting_priority >= 8],
                'medium_priority': [f for f in files if 5 <= f.sorting_priority < 8],
                'low_priority': [f for f in files if f.sorting_priority < 5]
            }
        
        return recommendations
    
    def _analyze_access_patterns(self) -> Dict[str, Any]:
        """Analyze file access patterns"""
        now = datetime.now()
        
        recent_files = [a for a in self.analyses if (now - a.accessed).days < 7]
        frequent_files = [a for a in self.analyses if a.usage_frequency == 'frequent']
        rare_files = [a for a in self.analyses if a.usage_frequency == 'rare']
        
        return {
            'recently_accessed': len(recent_files),
            'frequently_used': len(frequent_files),
            'rarely_used': len(rare_files),
            'recent_files': recent_files[:10],
            'frequent_files': frequent_files[:10],
            'rare_files': rare_files[:10]
        }
    
    def _generate_storage_optimization(self) -> Dict[str, Any]:
        """Generate storage optimization recommendations"""
        # Calculate storage by category
        storage_by_category = {}
        for category, files in self.categories.items():
            total_size = sum(f.size for f in files)
            storage_by_category[category] = {
                'size': total_size,
                'size_formatted': self._format_size(total_size),
                'file_count': len(files)
            }
        
        # Find largest files
        largest_files = sorted(self.analyses, key=lambda x: x.size, reverse=True)[:20]
        
        return {
            'storage_by_category': storage_by_category,
            'largest_files': [{'path': f.path, 'size': f.size_formatted, 'category': f.category} for f in largest_files],
            'optimization_opportunities': self._find_optimization_opportunities()
        }
    
    def _find_optimization_opportunities(self) -> List[Dict[str, Any]]:
        """Find specific optimization opportunities"""
        opportunities = []
        
        # Find files that could be archived
        old_files = [a for a in self.analyses if (datetime.now() - a.modified).days > CONSTANT_365 and a.usage_frequency == 'rare']
        if old_files:
            total_size = sum(f.size for f in old_files)
            opportunities.append({
                'type': 'archive_old_files',
                'description': f'Archive {len(old_files)} old, rarely used files',
                'potential_savings': self._format_size(total_size),
                'files': old_files[:10]
            })
        
        # Find temporary files
        temp_files = [a for a in self.analyses if any(word in a.name.lower() for word in ['temp', 'tmp', 'cache', 'log'])]
        if temp_files:
            total_size = sum(f.size for f in temp_files)
            opportunities.append({
                'type': 'cleanup_temp_files',
                'description': f'Clean up {len(temp_files)} temporary files',
                'potential_savings': self._format_size(total_size),
                'files': temp_files[:10]
            })
        
        return opportunities
    
    def _analyze_security(self) -> Dict[str, Any]:
        """Analyze security aspects"""
        high_risk_files = [a for a in self.analyses if a.security_risk == 'high']
        medium_risk_files = [a for a in self.analyses if a.security_risk == 'medium']
        
        return {
            'high_risk_files': len(high_risk_files),
            'medium_risk_files': len(medium_risk_files),
            'high_risk_list': [{'path': f.path, 'tags': f.tags} for f in high_risk_files],
            'medium_risk_list': [{'path': f.path, 'tags': f.tags} for f in medium_risk_files],
            'recommendations': self._generate_security_recommendations(high_risk_files, medium_risk_files)
        }
    
    def _generate_security_recommendations(self, high_risk: List[FileAnalysis], medium_risk: List[FileAnalysis]) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        if high_risk:
            recommendations.append(f"Review {len(high_risk)} high-risk files for sensitive information")
        
        if medium_risk:
            recommendations.append(f"Consider encrypting {len(medium_risk)} medium-risk files")
        
        recommendations.append("Implement regular security audits")
        recommendations.append("Consider using encrypted storage for sensitive files")
        
        return recommendations
    
    def _analyze_quality(self) -> Dict[str, Any]:
        """Analyze file quality"""
        quality_scores = [a.quality_score for a in self.analyses]
        high_quality = [a for a in self.analyses if a.quality_score > 0.8]
        low_quality = [a for a in self.analyses if a.quality_score < 0.3]
        
        return {
            'average_quality': sum(quality_scores) / len(quality_scores),
            'high_quality_files': len(high_quality),
            'low_quality_files': len(low_quality),
            'quality_distribution': {
                'excellent': len([a for a in self.analyses if a.quality_score > 0.8]),
                'good': len([a for a in self.analyses if 0.6 <= a.quality_score <= 0.8]),
                'fair': len([a for a in self.analyses if 0.4 <= a.quality_score < 0.6]),
                'poor': len([a for a in self.analyses if a.quality_score < 0.4])
            }
        }
    
    def _generate_backup_recommendations(self) -> Dict[str, Any]:
        """Generate backup recommendations"""
        critical_files = [a for a in self.analyses if a.backup_priority == 'critical']
        high_priority_files = [a for a in self.analyses if a.backup_priority == 'high']
        
        return {
            'critical_files': len(critical_files),
            'high_priority_files': len(high_priority_files),
            'backup_priorities': {
                'critical': [{'path': f.path, 'size': f.size_formatted} for f in critical_files],
                'high': [{'path': f.path, 'size': f.size_formatted} for f in high_priority_files]
            },
            'recommendations': [
                f"Backup {len(critical_files)} critical files immediately",
                f"Schedule regular backups for {len(high_priority_files)} high-priority files",
                "Implement automated backup system",
                "Test backup restoration procedures"
            ]
        }
    
    def _generate_organization_plan(self) -> Dict[str, Any]:
        """Generate file organization plan"""
        # Create organization structure
        organization_plan = {
            'recommended_structure': {
                'high_priority': 'Files with sorting_priority >= 8',
                'medium_priority': 'Files with sorting_priority 5-7',
                'low_priority': 'Files with sorting_priority < 5',
                'archives': 'Old, rarely used files',
                'temp_cleanup': 'Temporary and cache files'
            },
            'category_organization': {},
            'action_plan': []
        }
        
        # Category-specific organization
        for category, files in self.categories.items():
            organization_plan['category_organization'][category] = {
                'recommended_location': f"~/Documents/{category.title()}",
                'file_count': len(files),
                'total_size': self._format_size(sum(f.size for f in files)),
                'subcategories': list(set(f.subcategory for f in files))
            }
        
        # Generate action plan
        action_plan = [
            "1. Review and remove duplicate files",
            "2. Organize files by category and priority",
            "3. Archive old, rarely used files",
            "4. Clean up temporary and cache files",
            "5. Implement regular maintenance schedule",
            "6. Set up automated backup system"
        ]
        
        organization_plan['action_plan'] = action_plan
        
        return organization_plan
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= CONSTANT_1024 and i < len(size_names) - 1:
            size_bytes /= CONSTANT_1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"

def main():
    """Main function"""
    logger.info("🚀 Starting Deep Analysis and Content-Aware Document System...")
    
    # Initialize analyzer
    analyzer = FileSystemAnalyzer()
    
    # Analyze home directory
    analyses = analyzer.analyze_directory(str(Path.home()))
    
    # Generate optimization report
    optimizer = OptimizationEngine(analyses)
    report = optimizer.generate_optimization_report()
    
    # Save report
    report_file = Path(Path("/Users/steven/deep_analysis_report.json"))
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    # Save detailed analyses
    analyses_file = Path(Path("/Users/steven/file_analyses.json"))
    with open(analyses_file, 'w') as f:
        json.dump([{
            'path': a.path,
            'name': a.name,
            'size': a.size,
            'size_formatted': a.size_formatted,
            'extension': a.extension,
            'mime_type': a.mime_type,
            'created': a.created.isoformat(),
            'modified': a.modified.isoformat(),
            'accessed': a.accessed.isoformat(),
            'content_type': a.content_type,
            'category': a.category,
            'subcategory': a.subcategory,
            'importance_score': a.importance_score,
            'usage_frequency': a.usage_frequency,
            'sorting_priority': a.sorting_priority,
            'tags': a.tags,
            'quality_score': a.quality_score,
            'accessibility_score': a.accessibility_score,
            'security_risk': a.security_risk,
            'backup_priority': a.backup_priority,
            'optimization_suggestions': a.optimization_suggestions
        } for a in analyses], f, indent=2)
    
    logger.info(f"\n🎉 Deep Analysis Complete!")
    logger.info(f"📊 Files Analyzed: {len(analyses)}")
    logger.info(f"📁 Report Saved: {report_file}")
    logger.info(f"📄 Detailed Data: {analyses_file}")
    logger.info(f"\n📈 Summary:")
    logger.info(f"  Total Size: {report['summary']['total_size_formatted']}")
    logger.info(f"  Categories: {len(report['summary']['categories'])}")
    logger.info(f"  Duplicates: {report['duplicates']['total_duplicates']}")
    logger.info(f"  Wasted Space: {report['duplicates']['total_wasted_space_formatted']}")

if __name__ == "__main__":
    main()