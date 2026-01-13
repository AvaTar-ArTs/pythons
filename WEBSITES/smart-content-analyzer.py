#!/usr/bin/env python3
"""
Smart Content Analyzer with Deep Research Intelligence
====================================================
Intelligently analyzes, deduplicates, and organizes content using AI
"""

import os
import json
import hashlib
import difflib
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from collections import defaultdict
import re

@dataclass
class ContentItem:
    """Represents a piece of content with metadata"""
    path: str
    content: str
    hash: str
    size: int
    type: str
    title: str
    topics: List[str]
    complexity: float
    duplicates: List[str]
    similar: List[str]
    quality_score: float
    last_modified: str

class SmartContentAnalyzer:
    """Intelligent content analysis and organization system"""
    
    def __init__(self, base_path: str = "/Users/steven"):
        self.base_path = Path(base_path)
        self.content_items = {}
        self.duplicate_groups = defaultdict(list)
        self.similar_groups = defaultdict(list)
        self.topic_index = defaultdict(list)
        self.quality_scores = {}
        
    def analyze_directory(self, directory: str) -> Dict[str, Any]:
        """Analyze a directory for content intelligence"""
        print(f"🔍 Analyzing directory: {directory}")
        
        target_path = self.base_path / directory
        if not target_path.exists():
            print(f"❌ Directory not found: {target_path}")
            return {}
        
        # Find all content files
        content_files = self._find_content_files(target_path)
        print(f"📁 Found {len(content_files)} content files")
        
        # Analyze each file
        for file_path in content_files:
            self._analyze_file(file_path)
        
        # Perform intelligent analysis
        self._detect_duplicates()
        self._detect_similar_content()
        self._build_topic_index()
        self._calculate_quality_scores()
        
        return self._generate_report()
    
    def _find_content_files(self, path: Path) -> List[Path]:
        """Find all content files in directory"""
        content_extensions = {
            '.md', '.txt', '.html', '.htm', '.pdf', '.doc', '.docx',
            '.json', '.yaml', '.yml', '.xml', '.csv', '.log'
        }
        
        files = []
        for ext in content_extensions:
            files.extend(path.rglob(f"*{ext}"))
        
        return files
    
    def _analyze_file(self, file_path: Path):
        """Analyze a single file for content intelligence"""
        try:
            # Read file content
            if file_path.suffix.lower() in ['.pdf']:
                content = self._read_pdf(file_path)
            else:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Calculate hash
            content_hash = hashlib.md5(content.encode()).hexdigest()
            
            # Extract metadata
            title = self._extract_title(content, file_path)
            topics = self._extract_topics(content)
            complexity = self._calculate_complexity(content)
            
            # Create content item
            item = ContentItem(
                path=str(file_path),
                content=content,
                hash=content_hash,
                size=len(content),
                type=file_path.suffix.lower(),
                title=title,
                topics=topics,
                complexity=complexity,
                duplicates=[],
                similar=[],
                quality_score=0.0,
                last_modified=str(file_path.stat().st_mtime)
            )
            
            self.content_items[str(file_path)] = item
            
        except Exception as e:
            print(f"⚠️  Error analyzing {file_path}: {e}")
    
    def _read_pdf(self, file_path: Path) -> str:
        """Read PDF content (simplified)"""
        try:
            import PyPDF2
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                return text
        except:
            return f"[PDF content from {file_path.name}]"
    
    def _extract_title(self, content: str, file_path: Path) -> str:
        """Extract title from content"""
        lines = content.split('\n')[:10]
        
        # Look for markdown headers
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
            elif line.startswith('## '):
                return line[3:].strip()
        
        # Look for HTML titles
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        if title_match:
            return title_match.group(1).strip()
        
        # Use filename
        return file_path.stem.replace('_', ' ').replace('-', ' ').title()
    
    def _extract_topics(self, content: str) -> List[str]:
        """Extract topics from content using intelligent analysis"""
        topics = []
        
        # Common AI/tech topics
        ai_topics = [
            'artificial intelligence', 'machine learning', 'deep learning',
            'neural networks', 'nlp', 'computer vision', 'automation',
            'api', 'docker', 'python', 'javascript', 'react', 'node',
            'database', 'sql', 'mongodb', 'redis', 'kubernetes',
            'aws', 'azure', 'gcp', 'cloud', 'devops', 'ci/cd'
        ]
        
        content_lower = content.lower()
        for topic in ai_topics:
            if topic in content_lower:
                topics.append(topic)
        
        # Extract from headers
        headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        topics.extend([h.strip().lower() for h in headers[:5]])
        
        return list(set(topics))[:10]
    
    def _calculate_complexity(self, content: str) -> float:
        """Calculate content complexity score"""
        lines = len(content.split('\n'))
        words = len(content.split())
        chars = len(content)
        
        # Simple complexity calculation
        complexity = (lines * 0.1 + words * 0.01 + chars * 0.001) / 100
        return min(complexity, 1.0)
    
    def _detect_duplicates(self):
        """Detect exact duplicate content"""
        hash_groups = defaultdict(list)
        
        for path, item in self.content_items.items():
            hash_groups[item.hash].append(path)
        
        for content_hash, paths in hash_groups.items():
            if len(paths) > 1:
                self.duplicate_groups[content_hash] = paths
                for path in paths:
                    self.content_items[path].duplicates = [p for p in paths if p != path]
    
    def _detect_similar_content(self):
        """Detect similar content using intelligent comparison"""
        paths = list(self.content_items.keys())
        
        for i, path1 in enumerate(paths):
            for path2 in paths[i+1:]:
                similarity = self._calculate_similarity(
                    self.content_items[path1].content,
                    self.content_items[path2].content
                )
                
                if similarity > 0.7:  # 70% similarity threshold
                    self.similar_groups[f"{path1}~{path2}"] = [path1, path2]
                    self.content_items[path1].similar.append(path2)
                    self.content_items[path2].similar.append(path1)
    
    def _calculate_similarity(self, content1: str, content2: str) -> float:
        """Calculate similarity between two content pieces"""
        # Use difflib for similarity
        matcher = difflib.SequenceMatcher(None, content1, content2)
        return matcher.ratio()
    
    def _build_topic_index(self):
        """Build topic-based index for navigation"""
        for path, item in self.content_items.items():
            for topic in item.topics:
                self.topic_index[topic].append(path)
    
    def _calculate_quality_scores(self):
        """Calculate quality scores for content"""
        for path, item in self.content_items.items():
            score = 0.0
            
            # Length factor
            if item.size > 1000:
                score += 0.2
            elif item.size > 500:
                score += 0.1
            
            # Complexity factor
            score += item.complexity * 0.3
            
            # Topic richness
            score += min(len(item.topics) * 0.1, 0.3)
            
            # File type factor
            if item.type in ['.md', '.txt']:
                score += 0.1
            elif item.type in ['.html', '.json']:
                score += 0.05
            
            item.quality_score = min(score, 1.0)
            self.quality_scores[path] = item.quality_score
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive analysis report"""
        total_files = len(self.content_items)
        duplicate_files = sum(len(group) for group in self.duplicate_groups.values())
        similar_pairs = len(self.similar_groups)
        
        # Top topics
        top_topics = sorted(
            self.topic_index.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )[:10]
        
        # Quality distribution
        quality_distribution = {
            'high': sum(1 for score in self.quality_scores.values() if score > 0.7),
            'medium': sum(1 for score in self.quality_scores.values() if 0.4 <= score <= 0.7),
            'low': sum(1 for score in self.quality_scores.values() if score < 0.4)
        }
        
        return {
            'summary': {
                'total_files': total_files,
                'duplicate_files': duplicate_files,
                'similar_pairs': similar_pairs,
                'unique_files': total_files - duplicate_files,
                'topics_found': len(self.topic_index)
            },
            'duplicates': dict(self.duplicate_groups),
            'similar_content': dict(self.similar_groups),
            'top_topics': top_topics,
            'quality_distribution': quality_distribution,
            'content_items': {
                path: {
                    'title': item.title,
                    'topics': item.topics,
                    'complexity': item.complexity,
                    'quality_score': item.quality_score,
                    'size': item.size,
                    'type': item.type
                }
                for path, item in self.content_items.items()
            }
        }
    
    def suggest_actions(self) -> List[Dict[str, Any]]:
        """Suggest intelligent actions based on analysis"""
        actions = []
        
        # Duplicate handling
        for content_hash, paths in self.duplicate_groups.items():
            if len(paths) > 1:
                actions.append({
                    'type': 'merge_duplicates',
                    'priority': 'high',
                    'description': f'Merge {len(paths)} duplicate files',
                    'files': paths,
                    'suggestion': 'Keep the most recent or highest quality version'
                })
        
        # Similar content handling
        for pair, paths in self.similar_groups.items():
            actions.append({
                'type': 'review_similar',
                'priority': 'medium',
                'description': f'Review similar content: {len(paths)} files',
                'files': paths,
                'suggestion': 'Consider merging or clearly differentiating content'
            })
        
        # Topic organization
        for topic, paths in self.topic_index.items():
            if len(paths) > 3:
                actions.append({
                    'type': 'organize_by_topic',
                    'priority': 'low',
                    'description': f'Organize {len(paths)} files about "{topic}"',
                    'files': paths,
                    'suggestion': f'Create topic folder: {topic.replace(" ", "_")}/'
                })
        
        return actions

def main():
    """Main function for content analysis"""
    print("🧠 Smart Content Analyzer")
    print("========================")
    
    analyzer = SmartContentAnalyzer()
    
    # Analyze key directories
    directories = [
        "Documents",
        "ai-sites",
        "claude",
        "reports"
    ]
    
    all_results = {}
    
    for directory in directories:
        print(f"\n📁 Analyzing {directory}...")
        results = analyzer.analyze_directory(directory)
        all_results[directory] = results
        
        if results:
            summary = results['summary']
            print(f"  📊 Files: {summary['total_files']}")
            print(f"  🔄 Duplicates: {summary['duplicate_files']}")
            print(f"  🔗 Similar: {summary['similar_pairs']}")
            print(f"  🏷️  Topics: {summary['topics_found']}")
    
    # Generate overall report
    print(f"\n📋 Overall Analysis Report")
    print("=" * 30)
    
    total_files = sum(r['summary']['total_files'] for r in all_results.values())
    total_duplicates = sum(r['summary']['duplicate_files'] for r in all_results.values())
    total_similar = sum(r['summary']['similar_pairs'] for r in all_results.values())
    
    print(f"📁 Total files analyzed: {total_files}")
    print(f"🔄 Total duplicates found: {total_duplicates}")
    print(f"🔗 Total similar pairs: {total_similar}")
    print(f"✅ Unique content: {total_files - total_duplicates}")
    
    # Suggest actions
    print(f"\n🎯 Suggested Actions")
    print("=" * 20)
    
    actions = analyzer.suggest_actions()
    for i, action in enumerate(actions[:10], 1):  # Show top 10 actions
        priority_emoji = "🔴" if action['priority'] == 'high' else "🟡" if action['priority'] == 'medium' else "🟢"
        print(f"{i}. {priority_emoji} {action['description']}")
        print(f"   💡 {action['suggestion']}")
        print(f"   📁 Files: {len(action['files'])}")
        print()
    
    # Save detailed report
    report_file = Path("/Users/steven/ai-sites/n8n/content-analysis-report.json")
    with open(report_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"💾 Detailed report saved to: {report_file}")
    print(f"\n🎉 Content analysis complete!")

if __name__ == "__main__":
    main()