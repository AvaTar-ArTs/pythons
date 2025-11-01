
# Constants
CONSTANT_200 = 200

#!/usr/bin/env python3
"""
Content Research Agent - Intelligent Content Analysis and Framework Builder
========================================================================

This agent intelligently reads and analyzes content from your document libraries
to build better prompts, frameworks, and content strategies.

Features:
- Deep content analysis across markD, HTML, and PDF files
- Pattern recognition for effective prompts and frameworks
- Content-aware prompt generation
- Framework extraction and optimization
- Knowledge base building for AI agent

Usage:
    python content_research_agent.py
"""

import os
import json
import logging
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import subprocess
import requests
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import pickle

# Load environment variables
from env_d_loader import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ContentPattern:
    """Represents a discovered content pattern"""
    pattern_type: str  # 'prompt', 'framework', 'template', 'structure'
    content: str
    source_file: str
    confidence: float
    usage_count: int = 0
    effectiveness_score: float = 0.0
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ContentAnalysis:
    """Results of content analysis"""
    file_path: str
    file_type: str
    content_length: int
    patterns_found: List[ContentPattern]
    key_topics: List[str]
    writing_style: str
    complexity_score: float
    prompt_potential: float
    framework_elements: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

class ContentResearchAgent:
    """Intelligent content research and analysis agent"""
    
    def __init__(self):
        self.base_path = Path(Path("/Users/steven/Documents"))
        self.markd_path = self.base_path / "markD"
        self.html_path = self.base_path / "HTML"
        self.pdf_path = self.base_path / "PDF"
        
        self.knowledge_base = self._load_knowledge_base()
        self.pattern_database = self._load_pattern_database()
        self.content_index = self._load_content_index()
        
        # Analysis patterns
        self.prompt_patterns = [
            r"prompt[s]?[:=]\s*['\"](.*?)['\"]",
            r"create\s+.*?prompt[s]?",
            r"generate\s+.*?using\s+.*?prompt[s]?",
            r"write\s+a\s+prompt\s+for",
            r"prompt\s+template[s]?",
            r"prompt\s+framework[s]?",
            r"prompt\s+structure[s]?",
            r"prompt\s+pattern[s]?",
            r"prompt\s+example[s]?",
            r"prompt\s+guide[s]?",
            r"prompt\s+best\s+practices",
            r"prompt\s+optimization",
            r"prompt\s+engineering",
            r"prompt\s+design",
            r"prompt\s+crafting"
        ]
        
        self.framework_patterns = [
            r"framework[s]?[:=]\s*['\"](.*?)['\"]",
            r"methodology[s]?[:=]\s*['\"](.*?)['\"]",
            r"approach[s]?[:=]\s*['\"](.*?)['\"]",
            r"strategy[s]?[:=]\s*['\"](.*?)['\"]",
            r"system[s]?[:=]\s*['\"](.*?)['\"]",
            r"process[s]?[:=]\s*['\"](.*?)['\"]",
            r"workflow[s]?[:=]\s*['\"](.*?)['\"]",
            r"template[s]?[:=]\s*['\"](.*?)['\"]",
            r"structure[s]?[:=]\s*['\"](.*?)['\"]",
            r"pattern[s]?[:=]\s*['\"](.*?)['\"]",
            r"model[s]?[:=]\s*['\"](.*?)['\"]",
            r"method[s]?[:=]\s*['\"](.*?)['\"]",
            r"technique[s]?[:=]\s*['\"](.*?)['\"]",
            r"principle[s]?[:=]\s*['\"](.*?)['\"]",
            r"guideline[s]?[:=]\s*['\"](.*?)['\"]"
        ]
        
        self.content_quality_indicators = [
            "detailed", "comprehensive", "thorough", "in-depth", "extensive",
            "structured", "organized", "systematic", "methodical", "logical",
            "clear", "concise", "precise", "specific", "actionable",
            "innovative", "creative", "original", "unique", "novel",
            "effective", "efficient", "optimized", "streamlined", "refined"
        ]
    
    def _load_knowledge_base(self) -> Dict:
        """Load the agent's knowledge base"""
        kb_file = Path(Path("/Users/steven/content_research_knowledge.json"))
        if kb_file.exists():
            with open(kb_file, 'r') as f:
                return json.load(f)
        return {
            "content_types": {},
            "prompt_templates": {},
            "framework_library": {},
            "effectiveness_scores": {},
            "usage_patterns": {},
            "last_updated": None
        }
    
    def _save_knowledge_base(self):
        """Save the agent's knowledge base"""
        kb_file = Path(Path("/Users/steven/content_research_knowledge.json"))
        self.knowledge_base["last_updated"] = datetime.now().isoformat()
        with open(kb_file, 'w') as f:
            json.dump(self.knowledge_base, f, indent=2)
    
    def _load_pattern_database(self) -> Dict:
        """Load the pattern database"""
        pattern_file = Path(Path("/Users/steven/content_patterns.json"))
        if pattern_file.exists():
            with open(pattern_file, 'r') as f:
                return json.load(f)
        return {
            "prompt_patterns": [],
            "framework_patterns": [],
            "template_patterns": [],
            "structure_patterns": []
        }
    
    def _save_pattern_database(self):
        """Save the pattern database"""
        pattern_file = Path(Path("/Users/steven/content_patterns.json"))
        with open(pattern_file, 'w') as f:
            json.dump(self.pattern_database, f, indent=2)
    
    def _load_content_index(self) -> Dict:
        """Load the content index"""
        index_file = Path(Path("/Users/steven/content_index.json"))
        if index_file.exists():
            with open(index_file, 'r') as f:
                return json.load(f)
        return {
            "files_analyzed": [],
            "last_analysis": None,
            "file_hashes": {},
            "analysis_cache": {}
        }
    
    def _save_content_index(self):
        """Save the content index"""
        index_file = Path(Path("/Users/steven/content_index.json"))
        with open(index_file, 'w') as f:
            json.dump(self.content_index, f, indent=2)
    
    def analyze_content_libraries(self) -> Dict[str, List[ContentAnalysis]]:
        """Analyze all content libraries for patterns and frameworks"""
        logger.info("🔍 Starting comprehensive content analysis...")
        
        results = {
            "markd": [],
            "html": [],
            "pdf": []
        }
        
        # Analyze markD files
        logger.info("📝 Analyzing markD files...")
        results["markd"] = self._analyze_directory(self.markd_path, "markdown")
        
        # Analyze HTML files
        logger.info("🌐 Analyzing HTML files...")
        results["html"] = self._analyze_directory(self.html_path, "html")
        
        # Analyze PDF files
        logger.info("📄 Analyzing PDF files...")
        results["pdf"] = self._analyze_directory(self.pdf_path, "pdf")
        
        # Update knowledge base
        self._update_knowledge_base(results)
        
        logger.info("✅ Content analysis complete!")
        return results
    
    def _analyze_directory(self, directory: Path, file_type: str) -> List[ContentAnalysis]:
        """Analyze all files in a directory"""
        analyses = []
        
        if not directory.exists():
            logger.warning(f"Directory not found: {directory}")
            return analyses
        
        files = list(directory.rglob("*"))
        files = [f for f in files if f.is_file() and not f.name.startswith('.')]
        
        for file_path in files[:50]:  # Limit to first 50 files for performance
            try:
                # Check if file has been analyzed recently
                file_hash = self._get_file_hash(file_path)
                if file_hash in self.content_index.get("analysis_cache", {}):
                    cached_analysis = self.content_index["analysis_cache"][file_hash]
                    analyses.append(ContentAnalysis(**cached_analysis))
                    continue
                
                # Analyze file
                analysis = self._analyze_file(file_path, file_type)
                if analysis:
                    analyses.append(analysis)
                    
                    # Cache analysis
                    self.content_index["analysis_cache"][file_hash] = {
                        "file_path": str(analysis.file_path),
                        "file_type": analysis.file_type,
                        "content_length": analysis.content_length,
                        "patterns_found": [self._pattern_to_dict(p) for p in analysis.patterns_found],
                        "key_topics": analysis.key_topics,
                        "writing_style": analysis.writing_style,
                        "complexity_score": analysis.complexity_score,
                        "prompt_potential": analysis.prompt_potential,
                        "framework_elements": analysis.framework_elements,
                        "metadata": analysis.metadata
                    }
                
            except Exception as e:
                logger.error(f"Error analyzing {file_path}: {e}")
                continue
        
        return analyses
    
    def _analyze_file(self, file_path: Path, file_type: str) -> Optional[ContentAnalysis]:
        """Analyze a single file for patterns and frameworks"""
        try:
            # Read file content
            content = self._read_file_content(file_path, file_type)
            if not content:
                return None
            
            # Extract patterns
            patterns = self._extract_patterns(content, str(file_path))
            
            # Analyze content characteristics
            key_topics = self._extract_key_topics(content)
            writing_style = self._analyze_writing_style(content)
            complexity_score = self._calculate_complexity_score(content)
            prompt_potential = self._assess_prompt_potential(content)
            framework_elements = self._extract_framework_elements(content)
            
            return ContentAnalysis(
                file_path=str(file_path),
                file_type=file_type,
                content_length=len(content),
                patterns_found=patterns,
                key_topics=key_topics,
                writing_style=writing_style,
                complexity_score=complexity_score,
                prompt_potential=prompt_potential,
                framework_elements=framework_elements,
                metadata={
                    "file_size": file_path.stat().st_size,
                    "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    "analysis_timestamp": datetime.now().isoformat()
                }
            })
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            return None
    
    def _read_file_content(self, file_path: Path, file_type: str) -> Optional[str]:
        """Read file content based on file type"""
        try:
            if file_type == "pdf":
                return self._extract_pdf_text(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None
    
    def _extract_pdf_text(self, file_path: Path) -> Optional[str]:
        """Extract text from PDF file"""
        try:
            # Try using pdfplumber if available
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                return text
        except ImportError:
            logger.warning("pdfplumber not available, using basic PDF extraction")
            # Fallback to basic extraction
            try:
                import PyPDF2
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()
                    return text
            except ImportError:
                logger.warning("PDF extraction libraries not available")
                return None
        except Exception as e:
            logger.error(f"Error extracting PDF text: {e}")
            return None
    
    def _extract_patterns(self, content: str, source_file: str) -> List[ContentPattern]:
        """Extract patterns from content"""
        patterns = []
        
        # Extract prompt patterns
        for pattern_regex in self.prompt_patterns:
            matches = re.finditer(pattern_regex, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                pattern = ContentPattern(
                    pattern_type="prompt",
                    content=match.group(1) if match.groups() else match.group(0),
                    source_file=source_file,
                    confidence=self._calculate_pattern_confidence(match.group(0)),
                    tags=self._extract_pattern_tags(match.group(0)),
                    metadata={"regex_used": pattern_regex}
                )
                patterns.append(pattern)
        
        # Extract framework patterns
        for pattern_regex in self.framework_patterns:
            matches = re.finditer(pattern_regex, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                pattern = ContentPattern(
                    pattern_type="framework",
                    content=match.group(1) if match.groups() else match.group(0),
                    source_file=source_file,
                    confidence=self._calculate_pattern_confidence(match.group(0)),
                    tags=self._extract_pattern_tags(match.group(0)),
                    metadata={"regex_used": pattern_regex}
                )
                patterns.append(pattern)
        
        return patterns
    
    def _extract_key_topics(self, content: str) -> List[str]:
        """Extract key topics from content"""
        # Simple keyword extraction
        words = re.findall(r'\b[a-zA-Z]{4,}\b', content.lower())
        word_freq = Counter(words)
        
        # Filter out common words
        common_words = {'this', 'that', 'with', 'from', 'they', 'have', 'been', 'were', 'said', 'each', 'which', 'their', 'time', 'will', 'about', 'there', 'could', 'other', 'after', 'first', 'well', 'also', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'among', 'under', 'over', 'around', 'near', 'far', 'here', 'there', 'where', 'when', 'why', 'how', 'what', 'who', 'which', 'whose', 'whom'}
        
        filtered_words = {word: count for word, count in word_freq.items() if word not in common_words}
        return [word for word, count in sorted(filtered_words.items(), key=lambda x: x[1], reverse=True)[:20]]
    
    def _analyze_writing_style(self, content: str) -> str:
        """Analyze writing style characteristics"""
        style_indicators = {
            "technical": ["function", "method", "algorithm", "implementation", "code", "system", "process"],
            "creative": ["imagine", "create", "design", "artistic", "visual", "story", "narrative"],
            "academic": ["research", "study", "analysis", "theory", "hypothesis", "conclusion", "evidence"],
            "business": ["strategy", "marketing", "sales", "revenue", "growth", "customer", "market"],
            "casual": ["hey", "cool", "awesome", "amazing", "incredible", "fantastic", "wow"]
        }
        
        content_lower = content.lower()
        style_scores = {}
        
        for style, indicators in style_indicators.items():
            score = sum(1 for indicator in indicators if indicator in content_lower)
            style_scores[style] = score
        
        return max(style_scores, key=style_scores.get) if style_scores else "neutral"
    
    def _calculate_complexity_score(self, content: str) -> float:
        """Calculate content complexity score (0-10)"""
        # Simple complexity metrics
        sentences = re.split(r'[.!?]+', content)
        words = content.split()
        
        if not sentences or not words:
            return 0.0
        
        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Normalize to 0-10 scale
        complexity = (avg_sentence_length / 20) * 5 + (avg_word_length / 10) * 5
        return min(10.0, complexity)
    
    def _assess_prompt_potential(self, content: str) -> float:
        """Assess how well content could be used for prompt generation (0-10)"""
        prompt_indicators = [
            "prompt", "template", "framework", "structure", "pattern",
            "create", "generate", "write", "design", "build",
            "step", "process", "method", "approach", "strategy"
        ]
        
        content_lower = content.lower()
        indicator_count = sum(1 for indicator in prompt_indicators if indicator in content_lower)
        
        # Normalize to 0-10 scale
        return min(10.0, (indicator_count / len(prompt_indicators)) * 10)
    
    def _extract_framework_elements(self, content: str) -> List[str]:
        """Extract framework elements from content"""
        framework_elements = []
        
        # Look for numbered lists, bullet points, and structured content
        numbered_items = re.findall(r'^\d+\.\s+(.+)$', content, re.MULTILINE)
        bullet_items = re.findall(r'^[-*]\s+(.+)$', content, re.MULTILINE)
        
        framework_elements.extend(numbered_items)
        framework_elements.extend(bullet_items)
        
        # Look for section headers
        headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        framework_elements.extend(headers)
        
        return framework_elements[:20]  # Limit to first 20 elements
    
    def _calculate_pattern_confidence(self, pattern_text: str) -> float:
        """Calculate confidence score for a pattern (0-1)"""
        confidence = 0.5  # Base confidence
        
        # Increase confidence for longer patterns
        if len(pattern_text) > 50:
            confidence += 0.2
        
        # Increase confidence for quality indicators
        quality_indicators = self.content_quality_indicators
        for indicator in quality_indicators:
            if indicator in pattern_text.lower():
                confidence += 0.1
        
        # Increase confidence for structured content
        if any(char in pattern_text for char in ['-', '*', '1.', '2.', '3.']):
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _extract_pattern_tags(self, pattern_text: str) -> List[str]:
        """Extract tags for a pattern"""
        tags = []
        
        # Content type tags
        if any(word in pattern_text.lower() for word in ['image', 'visual', 'picture', 'photo']):
            tags.append('visual')
        if any(word in pattern_text.lower() for word in ['audio', 'sound', 'voice', 'music']):
            tags.append('audio')
        if any(word in pattern_text.lower() for word in ['video', 'movie', 'film', 'animation']):
            tags.append('video')
        if any(word in pattern_text.lower() for word in ['text', 'writing', 'content', 'article']):
            tags.append('text')
        
        # Complexity tags
        if len(pattern_text) > CONSTANT_200:
            tags.append('detailed')
        if len(pattern_text) < 50:
            tags.append('simple')
        
        # Style tags
        if any(word in pattern_text.lower() for word in ['creative', 'artistic', 'design']):
            tags.append('creative')
        if any(word in pattern_text.lower() for word in ['technical', 'system', 'process']):
            tags.append('technical')
        
        return tags
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Get file hash for caching"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return str(file_path.stat().st_mtime)
    
    def _pattern_to_dict(self, pattern: ContentPattern) -> Dict:
        """Convert ContentPattern to dictionary"""
        return {
            "pattern_type": pattern.pattern_type,
            "content": pattern.content,
            "source_file": pattern.source_file,
            "confidence": pattern.confidence,
            "usage_count": pattern.usage_count,
            "effectiveness_score": pattern.effectiveness_score,
            "tags": pattern.tags,
            "metadata": pattern.metadata
        }
    
    def _update_knowledge_base(self, results: Dict[str, List[ContentAnalysis]]):
        """Update knowledge base with analysis results"""
        logger.info("🧠 Updating knowledge base...")
        
        # Update content types
        for content_type, analyses in results.items():
            if content_type not in self.knowledge_base["content_types"]:
                self.knowledge_base["content_types"][content_type] = {
                    "total_files": 0,
                    "total_patterns": 0,
                    "avg_complexity": 0.0,
                    "common_topics": [],
                    "writing_styles": {}
                }
            
            content_type_data = self.knowledge_base["content_types"][content_type]
            content_type_data["total_files"] += len(analyses)
            
            all_patterns = []
            all_topics = []
            style_counts = Counter()
            
            for analysis in analyses:
                all_patterns.extend(analysis.patterns_found)
                all_topics.extend(analysis.key_topics)
                style_counts[analysis.writing_style] += 1
            
            content_type_data["total_patterns"] += len(all_patterns)
            content_type_data["avg_complexity"] = sum(a.complexity_score for a in analyses) / len(analyses) if analyses else 0
            content_type_data["common_topics"] = [topic for topic, count in Counter(all_topics).most_common(10)]
            content_type_data["writing_styles"] = dict(style_counts)
        
        # Update prompt templates
        all_prompt_patterns = []
        for analyses in results.values():
            for analysis in analyses:
                for pattern in analysis.patterns_found:
                    if pattern.pattern_type == "prompt":
                        all_prompt_patterns.append(pattern)
        
        # Group similar prompt patterns
        prompt_groups = defaultdict(list)
        for pattern in all_prompt_patterns:
            # Simple grouping by first few words
            key = ' '.join(pattern.content.split()[:3]).lower()
            prompt_groups[key].append(pattern)
        
        # Create prompt templates
        for key, patterns in prompt_groups.items():
            if len(patterns) > 1:  # Only include patterns that appear multiple times
                template = {
                    "base_pattern": patterns[0].content,
                    "variations": [p.content for p in patterns[1:]],
                    "confidence": sum(p.confidence for p in patterns) / len(patterns),
                    "usage_count": sum(p.usage_count for p in patterns),
                    "tags": list(set(tag for p in patterns for tag in p.tags)),
                    "source_files": list(set(p.source_file for p in patterns))
                }
                self.knowledge_base["prompt_templates"][key] = template
        
        # Save updated knowledge base
        self._save_knowledge_base()
        self._save_pattern_database()
        self._save_content_index()
        
        logger.info("✅ Knowledge base updated!")
    
    def generate_prompt_frameworks(self, content_type: str = None) -> Dict[str, Any]:
        """Generate prompt frameworks based on analyzed content"""
        logger.info("🎯 Generating prompt frameworks...")
        
        frameworks = {
            "content_generation": {},
            "image_generation": {},
            "audio_generation": {},
            "video_generation": {},
            "research": {},
            "analysis": {}
        }
        
        # Extract frameworks from knowledge base
        for template_key, template_data in self.knowledge_base["prompt_templates"].items():
            # Categorize by content type
            if any(tag in template_data["tags"] for tag in ["visual", "image", "picture"]):
                frameworks["image_generation"][template_key] = template_data
            elif any(tag in template_data["tags"] for tag in ["audio", "sound", "voice"]):
                frameworks["audio_generation"][template_key] = template_data
            elif any(tag in template_data["tags"] for tag in ["video", "movie", "film"]):
                frameworks["video_generation"][template_key] = template_data
            elif any(tag in template_data["tags"] for tag in ["text", "writing", "content"]):
                frameworks["content_generation"][template_key] = template_data
            elif any(tag in template_data["tags"] for tag in ["research", "analysis", "study"]):
                frameworks["research"][template_key] = template_data
        
        # Generate optimized frameworks
        optimized_frameworks = {}
        for category, templates in frameworks.items():
            if templates:
                optimized_frameworks[category] = self._optimize_framework_category(category, templates)
        
        return optimized_frameworks
    
    def _optimize_framework_category(self, category: str, templates: Dict) -> Dict:
        """Optimize frameworks for a specific category"""
        optimized = {
            "primary_framework": None,
            "alternative_frameworks": [],
            "best_practices": [],
            "common_patterns": [],
            "optimization_tips": []
        }
        
        if not templates:
            return optimized
        
        # Find the best primary framework
        best_template = max(templates.items(), key=lambda x: x[1]["confidence"] * x[1]["usage_count"])
        optimized["primary_framework"] = {
            "pattern": best_template[1]["base_pattern"],
            "confidence": best_template[1]["confidence"],
            "usage_count": best_template[1]["usage_count"],
            "tags": best_template[1]["tags"]
        }
        
        # Add alternative frameworks
        for key, template in templates.items():
            if key != best_template[0]:
                optimized["alternative_frameworks"].append({
                    "pattern": template["base_pattern"],
                    "confidence": template["confidence"],
                    "usage_count": template["usage_count"],
                    "tags": template["tags"]
                })
        
        # Generate best practices based on patterns
        optimized["best_practices"] = self._generate_best_practices(category, templates)
        optimized["common_patterns"] = self._extract_common_patterns(templates)
        optimized["optimization_tips"] = self._generate_optimization_tips(category, templates)
        
        return optimized
    
    def _generate_best_practices(self, category: str, templates: Dict) -> List[str]:
        """Generate best practices for a category"""
        practices = []
        
        # Analyze common elements across templates
        all_tags = []
        for template in templates.values():
            all_tags.extend(template["tags"])
        
        tag_counts = Counter(all_tags)
        common_tags = [tag for tag, count in tag_counts.most_common(5)]
        
        if "detailed" in common_tags:
            practices.append("Use detailed, specific descriptions for better results")
        if "creative" in common_tags:
            practices.append("Incorporate creative and artistic elements")
        if "technical" in common_tags:
            practices.append("Include technical specifications when relevant")
        if "structured" in common_tags:
            practices.append("Use clear structure and organization")
        
        # Category-specific practices
        if category == "image_generation":
            practices.extend([
                "Include style, mood, and composition details",
                "Specify lighting and color preferences",
                "Add technical specifications (resolution, format)"
            ])
        elif category == "content_generation":
            practices.extend([
                "Define target audience and tone clearly",
                "Include specific requirements and constraints",
                "Provide context and background information"
            ])
        
        return practices
    
    def _extract_common_patterns(self, templates: Dict) -> List[str]:
        """Extract common patterns from templates"""
        patterns = []
        
        # Look for common structural elements
        all_patterns = [template["base_pattern"] for template in templates.values()]
        
        # Find common words/phrases
        all_words = []
        for pattern in all_patterns:
            words = re.findall(r'\b[a-zA-Z]{3,}\b', pattern.lower())
            all_words.extend(words)
        
        word_counts = Counter(all_words)
        common_words = [word for word, count in word_counts.most_common(10) if count > 1]
        
        patterns.extend(common_words)
        
        # Find common structural patterns
        structural_patterns = [
            r'create\s+.*?for',
            r'generate\s+.*?using',
            r'write\s+a\s+.*?about',
            r'design\s+.*?with',
            r'build\s+.*?that'
        ]
        
        for pattern_regex in structural_patterns:
            matches = sum(1 for pattern in all_patterns if re.search(pattern_regex, pattern, re.IGNORECASE))
            if matches > len(all_patterns) * 0.3:  # If pattern appears in 30%+ of templates
                patterns.append(pattern_regex)
        
        return patterns
    
    def _generate_optimization_tips(self, category: str, templates: Dict) -> List[str]:
        """Generate optimization tips for a category"""
        tips = []
        
        # Analyze confidence scores
        avg_confidence = sum(template["confidence"] for template in templates.values()) / len(templates)
        
        if avg_confidence < 0.7:
            tips.append("Focus on improving pattern clarity and specificity")
        
        # Analyze usage counts
        total_usage = sum(template["usage_count"] for template in templates.values())
        if total_usage < 10:
            tips.append("Consider testing patterns more frequently to improve effectiveness")
        
        # Category-specific tips
        if category == "image_generation":
            tips.extend([
                "Include specific artistic styles and techniques",
                "Specify lighting conditions and mood",
                "Add composition and framing details"
            ])
        elif category == "content_generation":
            tips.extend([
                "Define clear objectives and success criteria",
                "Include target audience characteristics",
                "Specify tone, style, and format requirements"
            ])
        
        return tips
    
    def get_content_recommendations(self, request_type: str, requirements: Dict) -> Dict[str, Any]:
        """Get content recommendations based on request type and requirements"""
        logger.info(f"🎯 Generating recommendations for {request_type}...")
        
        recommendations = {
            "prompt_templates": [],
            "framework_suggestions": [],
            "content_examples": [],
            "optimization_tips": [],
            "related_patterns": []
        }
        
        # Find relevant patterns from knowledge base
        relevant_patterns = []
        for template_key, template_data in self.knowledge_base["prompt_templates"].items():
            if self._is_relevant_pattern(template_data, request_type, requirements):
                relevant_patterns.append((template_key, template_data))
        
        # Sort by relevance and confidence
        relevant_patterns.sort(key=lambda x: x[1]["confidence"] * x[1]["usage_count"], reverse=True)
        
        # Generate recommendations
        for pattern_key, pattern_data in relevant_patterns[:10]:  # Top 10
            recommendations["prompt_templates"].append({
                "pattern": pattern_data["base_pattern"],
                "confidence": pattern_data["confidence"],
                "tags": pattern_data["tags"],
                "variations": pattern_data.get("variations", [])
            })
        
        # Generate framework suggestions
        frameworks = self.generate_prompt_frameworks()
        if request_type in frameworks:
            recommendations["framework_suggestions"] = frameworks[request_type]
        
        # Generate optimization tips
        recommendations["optimization_tips"] = self._generate_optimization_tips(request_type, {})
        
        return recommendations
    
    def _is_relevant_pattern(self, pattern_data: Dict, request_type: str, requirements: Dict) -> bool:
        """Check if a pattern is relevant to the request"""
        # Check tags
        pattern_tags = set(pattern_data.get("tags", []))
        request_tags = set(requirements.get("tags", []))
        
        if pattern_tags & request_tags:  # If there's any overlap
            return True
        
        # Check content type
        if request_type in pattern_data.get("tags", []):
            return True
        
        # Check confidence threshold
        if pattern_data.get("confidence", 0) > 0.6:
            return True
        
        return False

def main():
    """Main function to run the content research agent"""
    logger.info("🔍 Content Research Agent - Intelligent Content Analysis")
    logger.info("=" * 60)
    
    agent = ContentResearchAgent()
    
    # Analyze content libraries
    logger.info("📚 Analyzing content libraries...")
    results = agent.analyze_content_libraries()
    
    # Print summary
    logger.info("\n📊 Analysis Summary:")
    logger.info("-" * 30)
    for content_type, analyses in results.items():
        logger.info(f"{content_type.upper()}: {len(analyses)} files analyzed")
        total_patterns = sum(len(a.patterns_found) for a in analyses)
        logger.info(f"  - {total_patterns} patterns found")
        avg_complexity = sum(a.complexity_score for a in analyses) / len(analyses) if analyses else 0
        logger.info(f"  - Average complexity: {avg_complexity:.2f}/10")
        logger.info(f"  - Average prompt potential: {sum(a.prompt_potential for a in analyses) / len(analyses) if analyses else 0:.2f}/10")
    
    # Generate frameworks
    logger.info("\n🎯 Generating prompt frameworks...")
    frameworks = agent.generate_prompt_frameworks()
    
    logger.info("\n📋 Available Frameworks:")
    for category, framework_data in frameworks.items():
        if framework_data:
            logger.info(f"  - {category}: {len(framework_data.get('alternative_frameworks', []))} alternatives")
    
    # Save results
    output_file = Path(Path("/Users/steven/content_research_results.json"))
    with open(output_file, 'w') as f:
        json.dump({
            "analysis_results": {
                content_type: [
                    {
                        "file_path": analysis.file_path,
                        "file_type": analysis.file_type,
                        "content_length": analysis.content_length,
                        "patterns_found": len(analysis.patterns_found),
                        "key_topics": analysis.key_topics[:10],
                        "writing_style": analysis.writing_style,
                        "complexity_score": analysis.complexity_score,
                        "prompt_potential": analysis.prompt_potential,
                        "framework_elements": analysis.framework_elements[:5]
                    }
                    for analysis in analyses
                ]
                for content_type, analyses in results.items()
            },
            "frameworks": frameworks,
            "knowledge_base_summary": {
                "content_types": agent.knowledge_base["content_types"],
                "prompt_templates_count": len(agent.knowledge_base["prompt_templates"]),
                "last_updated": agent.knowledge_base["last_updated"]
            }
        }, f, indent=2)
    
    logger.info(f"\n💾 Results saved to: {output_file}")
    logger.info("✅ Content research complete!")

if __name__ == "__main__":
    main()