
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_128 = 128
CONSTANT_255 = 255
CONSTANT_1000 = 1000
CONSTANT_1950 = 1950
CONSTANT_2000 = 2000
CONSTANT_10000 = 10000
CONSTANT_1738731384372 = 1738731384372

#!/usr/bin/env python3
"""
Advanced Content-Awareness Intelligence System
Implements deep semantic analysis, pattern recognition, and intelligent organization
using multiple AI APIs and advanced techniques.
"""

import os
import sys
import json
import ast
import re
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import hashlib
import pickle
from collections import defaultdict, Counter
import openai
import cohere
from openai import OpenAI
import anthropic

# Load environment variables
def load_env():
    """Load environment variables from ~/.env.d"""
    try:
        # Load specific environment files directly
        env_files = [
            Path.home() / ".env.d" / "llm-apis.env",
            Path.home() / ".env.d" / "automation-agents.env",
            Path.home() / ".env.d" / "vector-memory.env"
        ]
        
        for env_file in env_files:
            if env_file.exists():
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key] = value
    except Exception as e:
        logger.info(f"⚠️  Error loading environment: {e}")
        logger.info("Please set API keys manually or check ~/.env.d/ files")

@dataclass
class ContentInsight:
    """Structured insight about content"""
    content_type: str
    semantic_category: str
    complexity_score: float
    patterns: List[str]
    confidence: float
    recommendations: List[str]
    metadata: Dict[str, Any]

@dataclass
class FileAnalysis:
    """Complete analysis of a file"""
    filepath: str
    content_insights: List[ContentInsight]
    overall_score: float
    organization_suggestions: List[str]
    dependencies: List[str]
    tags: List[str]

class AdvancedContentAnalyzer:
    """Advanced content analysis using multiple AI models and techniques"""
    
    def __init__(self):
        load_env()
        
        # Initialize clients with error handling
        self.openai_client = None
        self.anthropic_client = None
        self.cohere_client = None
        
        try:
            if os.getenv('OPENAI_API_KEY'):
                self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        except Exception as e:
            logger.info(f"⚠️  OpenAI client initialization failed: {e}")
            
        try:
            if os.getenv('ANTHROPIC_API_KEY'):
                self.anthropic_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        except Exception as e:
            logger.info(f"⚠️  Anthropic client initialization failed: {e}")
            
        try:
            if os.getenv('COHERE_API_KEY'):
                self.cohere_client = cohere.Client(api_key=os.getenv('COHERE_API_KEY'))
        except Exception as e:
            logger.info(f"⚠️  Cohere client initialization failed: {e}")
        
        # Initialize vector database
        self.vector_db = {}
        self.insights_db = {}
        
        # Load existing data
        self._load_databases()
    
    def _load_databases(self):
        """Load existing vector and insights databases"""
        try:
            with open('.vector_database.pkl', 'rb') as f:
                self.vector_db = pickle.load(f)
        except FileNotFoundError:
            self.vector_db = {}
            
        try:
            with open('.insights_database.json', 'r') as f:
                self.insights_db = json.load(f)
        except FileNotFoundError:
            self.insights_db = {}
    
    def _save_databases(self):
        """Save databases to disk"""
        with open('.vector_database.pkl', 'wb') as f:
            pickle.dump(self.vector_db, f)
            
        with open('.insights_database.json', 'w') as f:
            json.dump(self.insights_db, f, indent=2)
    
    def analyze_file_content(self, filepath: str) -> FileAnalysis:
        """Perform comprehensive content analysis of a file"""
        logger.info(f"🔍 Analyzing: {filepath}")
        
        try:
            # Read file content
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Generate content hash for caching
            content_hash = hashlib.md5(content.encode()).hexdigest()
            
            # Check if we have cached analysis
            if content_hash in self.insights_db:
                logger.info(f"📋 Using cached analysis for {filepath}")
                return self._load_cached_analysis(content_hash)
            
            # Perform multi-layered analysis
            insights = []
            
            # 1. Semantic Analysis with GPT-5
            semantic_insights = self._semantic_analysis(content, filepath)
            insights.extend(semantic_insights)
            
            # 2. Pattern Recognition with Claude
            pattern_insights = self._pattern_analysis(content, filepath)
            insights.extend(pattern_insights)
            
            # 3. Code Quality Analysis (if applicable)
            if filepath.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c')):
                code_insights = self._code_quality_analysis(content, filepath)
                insights.extend(code_insights)
            
            # 4. Data Structure Analysis (for Excel/CSV files)
            if filepath.endswith(('.xlsx', '.xls', '.csv')):
                data_insights = self._data_structure_analysis(filepath)
                insights.extend(data_insights)
            
            # 5. Generate embeddings for semantic search
            embeddings = self._generate_embeddings(content)
            
            # Calculate overall score
            overall_score = self._calculate_overall_score(insights)
            
            # Generate organization suggestions
            suggestions = self._generate_organization_suggestions(insights, filepath)
            
            # Extract dependencies
            dependencies = self._extract_dependencies(content, filepath)
            
            # Generate tags
            tags = self._generate_tags(insights, filepath)
            
            # Create analysis result
            analysis = FileAnalysis(
                filepath=filepath,
                content_insights=insights,
                overall_score=overall_score,
                organization_suggestions=suggestions,
                dependencies=dependencies,
                tags=tags
            )
            
            # Cache the analysis
            self._cache_analysis(content_hash, analysis)
            
            return analysis
            
        except Exception as e:
            logger.info(f"❌ Error analyzing {filepath}: {str(e)}")
            return FileAnalysis(
                filepath=filepath,
                content_insights=[],
                overall_score=0.0,
                organization_suggestions=[f"Error analyzing file: {str(e)}"],
                dependencies=[],
                tags=["error"]
            )
    
    def _semantic_analysis(self, content: str, filepath: str) -> List[ContentInsight]:
        """Perform semantic analysis using GPT-5"""
        if not self.openai_client:
            return self._fallback_semantic_analysis(content, filepath)
            
        try:
            prompt = f"""
            Analyze the following content for semantic understanding and categorization:
            
            File: {filepath}
            Content: {content[:CONSTANT_2000]}...
            
            Provide analysis in JSON format with:
            1. content_type: Type of content (code, data, documentation, etc.)
            2. semantic_category: Main semantic category
            3. complexity_score: 0-1 complexity rating
            4. patterns: List of identified patterns
            5. confidence: 0-1 confidence in analysis
            6. recommendations: List of improvement suggestions
            7. metadata: Additional relevant information
            
            Focus on understanding the purpose, structure, and quality of the content.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=CONSTANT_1000
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return [ContentInsight(
                content_type=result.get('content_type', 'unknown'),
                semantic_category=result.get('semantic_category', 'general'),
                complexity_score=float(result.get('complexity_score', 0.5)),
                patterns=result.get('patterns', []),
                confidence=float(result.get('confidence', 0.7)),
                recommendations=result.get('recommendations', []),
                metadata=result.get('metadata', {})
            )]
            
        except Exception as e:
            logger.info(f"⚠️  Semantic analysis failed: {str(e)}")
            return self._fallback_semantic_analysis(content, filepath)
    
    def _fallback_semantic_analysis(self, content: str, filepath: str) -> List[ContentInsight]:
        """Fallback semantic analysis using heuristics"""
        # Basic content type detection
        content_type = "unknown"
        if filepath.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c')):
            content_type = "code"
        elif filepath.endswith(('.xlsx', '.xls', '.csv')):
            content_type = "data"
        elif filepath.endswith(('.md', '.txt', '.rst')):
            content_type = "documentation"
        
        # Basic complexity scoring
        lines = content.split('\n')
        complexity_score = min(len(lines) / CONSTANT_1000, 1.0)
        
        # Basic patterns
        patterns = []
        if 'function' in content.lower():
            patterns.append("functional")
        if 'class' in content.lower():
            patterns.append("object_oriented")
        if 'import' in content.lower():
            patterns.append("modular")
        
        return [ContentInsight(
            content_type=content_type,
            semantic_category="general",
            complexity_score=complexity_score,
            patterns=patterns,
            confidence=0.5,
            recommendations=[],
            metadata={"fallback": True}
        )]
    
    def _pattern_analysis(self, content: str, filepath: str) -> List[ContentInsight]:
        """Perform pattern analysis using Claude"""
        if not self.anthropic_client:
            return self._fallback_pattern_analysis(content, filepath)
            
        try:
            prompt = f"""
            Analyze the following content for design patterns, anti-patterns, and code quality:
            
            File: {filepath}
            Content: {content[:CONSTANT_2000]}...
            
            Identify:
            1. Design patterns (Singleton, Factory, Observer, etc.)
            2. Anti-patterns (code smells, bad practices)
            3. Architectural patterns (MVC, Microservices, etc.)
            4. Data patterns (normalization, relationships)
            5. Security patterns or vulnerabilities
            
            Provide analysis in JSON format with patterns found and confidence scores.
            """
            
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=CONSTANT_1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result = json.loads(response.content[0].text)
            
            return [ContentInsight(
                content_type="pattern_analysis",
                semantic_category="patterns",
                complexity_score=float(result.get('complexity_score', 0.5)),
                patterns=result.get('patterns', []),
                confidence=float(result.get('confidence', 0.7)),
                recommendations=result.get('recommendations', []),
                metadata=result.get('metadata', {})
            )]
            
        except Exception as e:
            logger.info(f"⚠️  Pattern analysis failed: {str(e)}")
            return self._fallback_pattern_analysis(content, filepath)
    
    def _fallback_pattern_analysis(self, content: str, filepath: str) -> List[ContentInsight]:
        """Fallback pattern analysis using heuristics"""
        patterns = []
        
        # Basic pattern detection
        if 'class' in content.lower() and 'def __init__' in content:
            patterns.append("object_oriented")
        if 'def ' in content and 'return' in content:
            patterns.append("functional")
        if 'import' in content and 'from' in content:
            patterns.append("modular")
        if 'try:' in content and 'except' in content:
            patterns.append("error_handling")
        
        return [ContentInsight(
            content_type="pattern_analysis",
            semantic_category="patterns",
            complexity_score=0.5,
            patterns=patterns,
            confidence=0.6,
            recommendations=[],
            metadata={"fallback": True}
        )]
    
    def _code_quality_analysis(self, content: str, filepath: str) -> List[ContentInsight]:
        """Perform code quality analysis using AST and heuristics"""
        try:
            if filepath.endswith('.py'):
                return self._python_code_analysis(content, filepath)
            else:
                return self._general_code_analysis(content, filepath)
                
        except Exception as e:
            logger.info(f"⚠️  Code quality analysis failed: {str(e)}")
            return []
    
    def _python_code_analysis(self, content: str, filepath: str) -> List[ContentInsight]:
        """Analyze Python code using AST"""
        try:
            tree = ast.parse(content)
            
            # Analyze code structure
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            imports = [node for node in ast.walk(tree) if isinstance(node, ast.Import)]
            
            # Calculate complexity metrics
            complexity_score = min(len(functions) * 0.1 + len(classes) * 0.2, 1.0)
            
            # Identify patterns
            patterns = []
            if len(classes) > 0:
                patterns.append("object_oriented")
            if len(functions) > 5:
                patterns.append("functional_heavy")
            if any(isinstance(node, ast.AsyncFunctionDef) for node in ast.walk(tree)):
                patterns.append("async_programming")
            
            # Generate recommendations
            recommendations = []
            if len(functions) > 10:
                recommendations.append("Consider breaking into smaller modules")
            if not any(isinstance(node, ast.ClassDef) for node in ast.walk(tree)) and len(functions) > 5:
                recommendations.append("Consider using classes for better organization")
            
            return [ContentInsight(
                content_type="python_code",
                semantic_category="programming",
                complexity_score=complexity_score,
                patterns=patterns,
                confidence=0.9,
                recommendations=recommendations,
                metadata={
                    "functions": len(functions),
                    "classes": len(classes),
                    "imports": len(imports),
                    "lines": len(content.split('\n'))
                }
            )]
            
        except SyntaxError:
            return [ContentInsight(
                content_type="python_code",
                semantic_category="programming",
                complexity_score=0.0,
                patterns=["syntax_error"],
                confidence=1.0,
                recommendations=["Fix syntax errors"],
                metadata={"error": "syntax_error"}
            )]
    
    def _general_code_analysis(self, content: str, filepath: str) -> List[ContentInsight]:
        """General code analysis for non-Python files"""
        lines = content.split('\n')
        
        # Basic metrics
        total_lines = len(lines)
        comment_lines = len([line for line in lines if line.strip().startswith(('//', '/*', '#', '--'))])
        empty_lines = len([line for line in lines if not line.strip()])
        
        # Calculate complexity
        complexity_score = min(total_lines / CONSTANT_1000, 1.0)
        
        # Identify patterns
        patterns = []
        if 'function' in content.lower():
            patterns.append("functional")
        if 'class' in content.lower():
            patterns.append("object_oriented")
        if 'async' in content.lower():
            patterns.append("async_programming")
        
        return [ContentInsight(
            content_type="code",
            semantic_category="programming",
            complexity_score=complexity_score,
            patterns=patterns,
            confidence=0.7,
            recommendations=[],
            metadata={
                "total_lines": total_lines,
                "comment_lines": comment_lines,
                "empty_lines": empty_lines
            }
        )]
    
    def _data_structure_analysis(self, filepath: str) -> List[ContentInsight]:
        """Analyze data structure files (Excel, CSV)"""
        try:
            if filepath.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(filepath)
            elif filepath.endswith('.csv'):
                df = pd.read_csv(filepath)
            else:
                return []
            
            # Analyze data structure
            rows, cols = df.shape
            null_percentage = (df.isnull().sum().sum() / (rows * cols)) * CONSTANT_100
            
            # Identify data types
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            text_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            # Calculate complexity
            complexity_score = min((rows * cols) / CONSTANT_10000, 1.0)
            
            # Generate patterns
            patterns = []
            if len(numeric_cols) > len(text_cols):
                patterns.append("numeric_heavy")
            if null_percentage > 20:
                patterns.append("sparse_data")
            if rows > CONSTANT_1000:
                patterns.append("large_dataset")
            
            # Generate recommendations
            recommendations = []
            if null_percentage > 20:
                recommendations.append("Consider data cleaning for null values")
            if rows > CONSTANT_10000:
                recommendations.append("Consider data partitioning or sampling")
            if len(cols) > 20:
                recommendations.append("Consider feature selection or dimensionality reduction")
            
            return [ContentInsight(
                content_type="data",
                semantic_category="dataset",
                complexity_score=complexity_score,
                patterns=patterns,
                confidence=0.9,
                recommendations=recommendations,
                metadata={
                    "rows": rows,
                    "columns": cols,
                    "null_percentage": null_percentage,
                    "numeric_columns": len(numeric_cols),
                    "text_columns": len(text_cols)
                }
            )]
            
        except Exception as e:
            logger.info(f"⚠️  Data analysis failed for {filepath}: {str(e)}")
            return []
    
    def _generate_embeddings(self, content: str) -> List[float]:
        """Generate embeddings using Cohere"""
        if not self.cohere_client:
            return self._fallback_embeddings(content)
            
        try:
            response = self.cohere_client.embed(
                texts=[content[:CONSTANT_1000]],  # Limit content for API
                model="embed-english-v3.0"
            )
            return response.embeddings[0]
        except Exception as e:
            logger.info(f"⚠️  Embedding generation failed: {str(e)}")
            return self._fallback_embeddings(content)
    
    def _fallback_embeddings(self, content: str) -> List[float]:
        """Fallback embeddings using simple hash-based vectors"""
        # Create a simple hash-based embedding
        content_hash = hashlib.md5(content.encode()).hexdigest()
        # Convert hash to CONSTANT_128-dimensional vector
        vector = []
        for i in range(0, len(content_hash), 2):
            hex_pair = content_hash[i:i+2]
            vector.append(int(hex_pair, 16) / CONSTANT_255.0)
        
        # Pad or truncate to CONSTANT_128 dimensions
        while len(vector) < CONSTANT_128:
            vector.append(0.0)
        return vector[:CONSTANT_128]
    
    def _calculate_overall_score(self, insights: List[ContentInsight]) -> float:
        """Calculate overall quality score from insights"""
        if not insights:
            return 0.0
        
        # Weight different aspects
        weights = {
            'complexity': 0.3,
            'confidence': 0.4,
            'pattern_quality': 0.3
        }
        
        scores = []
        for insight in insights:
            score = (
                insight.complexity_score * weights['complexity'] +
                insight.confidence * weights['confidence'] +
                (len(insight.patterns) / 10) * weights['pattern_quality']
            )
            scores.append(score)
        
        return sum(scores) / len(scores)
    
    def _generate_organization_suggestions(self, insights: List[ContentInsight], filepath: str) -> List[str]:
        """Generate intelligent organization suggestions"""
        suggestions = []
        
        # Analyze file path and content
        path_parts = Path(filepath).parts
        
        # Suggest based on content type
        for insight in insights:
            if insight.content_type == "python_code":
                suggestions.append("Move to code/ directory")
            elif insight.content_type == "data":
                suggestions.append("Move to data/ directory")
            elif "documentation" in insight.semantic_category:
                suggestions.append("Move to docs/ directory")
        
        # Suggest based on patterns
        for insight in insights:
            if "automation" in insight.patterns:
                suggestions.append("Consider automation/ directory")
            if "analysis" in insight.patterns:
                suggestions.append("Consider analysis/ directory")
        
        # Suggest based on complexity
        overall_complexity = sum(i.complexity_score for i in insights) / len(insights) if insights else 0
        if overall_complexity > 0.7:
            suggestions.append("High complexity - consider refactoring")
        
        return list(set(suggestions))  # Remove duplicates
    
    def _extract_dependencies(self, content: str, filepath: str) -> List[str]:
        """Extract dependencies from content"""
        dependencies = []
        
        # Python imports
        if filepath.endswith('.py'):
            import_pattern = r'^(?:from\s+(\S+)\s+)?import\s+(\S+)'
            matches = re.findall(import_pattern, content, re.MULTILINE)
            for module, name in matches:
                if module:
                    dependencies.append(module)
                else:
                    dependencies.append(name)
        
        # JavaScript/Node.js requires
        elif filepath.endswith(('.js', '.ts')):
            require_pattern = r'require\([\'"]([^\'"]+)[\'"]\)'
            matches = re.findall(require_pattern, content)
            dependencies.extend(matches)
        
        return list(set(dependencies))
    
    def _generate_tags(self, insights: List[ContentInsight], filepath: str) -> List[str]:
        """Generate intelligent tags for the file"""
        tags = []
        
        # Add file extension tag
        ext = Path(filepath).suffix[1:]
        if ext:
            tags.append(ext)
        
        # Add content type tags
        for insight in insights:
            tags.append(insight.content_type)
            tags.append(insight.semantic_category)
            tags.extend(insight.patterns)
        
        # Add complexity tag
        if insights:
            avg_complexity = sum(i.complexity_score for i in insights) / len(insights)
            if avg_complexity > 0.7:
                tags.append("complex")
            elif avg_complexity < 0.3:
                tags.append("simple")
        
        return list(set(tags))
    
    def _cache_analysis(self, content_hash: str, analysis: FileAnalysis):
        """Cache analysis results"""
        self.insights_db[content_hash] = {
            "filepath": analysis.filepath,
            "overall_score": analysis.overall_score,
            "tags": analysis.tags,
            "timestamp": datetime.now().isoformat()
        }
        self._save_databases()
    
    def _load_cached_analysis(self, content_hash: str) -> FileAnalysis:
        """Load cached analysis"""
        cached = self.insights_db[content_hash]
        return FileAnalysis(
            filepath=cached["filepath"],
            content_insights=[],
            overall_score=cached["overall_score"],
            organization_suggestions=[],
            dependencies=[],
            tags=cached["tags"]
        )
    
    def search_semantic(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search files using semantic similarity"""
        if not self.vector_db:
            return []
        
        # Generate query embedding
        query_embedding = self._generate_embeddings(query)
        if not query_embedding:
            return []
        
        # Calculate similarities
        similarities = []
        for filepath, embedding in self.vector_db.items():
            if embedding:
                similarity = np.dot(query_embedding, embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(embedding)
                )
                similarities.append((filepath, similarity))
        
        # Return top results
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [{"filepath": fp, "similarity": sim} for fp, sim in similarities[:top_k]]
    
    def generate_organization_report(self, files: List[str]) -> Dict[str, Any]:
        """Generate comprehensive organization report"""
        logger.info("📊 Generating organization report...")
        
        analyses = []
        for filepath in files:
            analysis = self.analyze_file_content(filepath)
            analyses.append(analysis)
        
        # Generate statistics
        total_files = len(analyses)
        avg_score = sum(a.overall_score for a in analyses) / total_files if analyses else 0
        
        # Categorize files
        categories = defaultdict(list)
        for analysis in analyses:
            for insight in analysis.content_insights:
                categories[insight.semantic_category].append(analysis.filepath)
        
        # Generate recommendations
        recommendations = []
        for analysis in analyses:
            recommendations.extend(analysis.organization_suggestions)
        
        # Count patterns
        all_patterns = []
        for analysis in analyses:
            for insight in analysis.content_insights:
                all_patterns.extend(insight.patterns)
        
        pattern_counts = Counter(all_patterns)
        
        return {
            "summary": {
                "total_files": total_files,
                "average_score": avg_score,
                "categories": dict(categories),
                "top_patterns": dict(pattern_counts.most_common(10))
            },
            "recommendations": list(set(recommendations)),
            "detailed_analyses": [
                {
                    "filepath": a.filepath,
                    "score": a.overall_score,
                    "tags": a.tags,
                    "suggestions": a.organization_suggestions
                }
                for a in analyses
            ]
        }

def main():
    """Main execution function"""
    logger.info("🚀 Advanced Content-Awareness Intelligence System")
    logger.info("=" * 60)
    
    # Initialize analyzer
    analyzer = AdvancedContentAnalyzer()
    
    # Example usage with Excel files
    excel_files = [
        "/Users/steven/Documents/CsV/xlsx/2b. Example 1.xlsx",
        "/Users/steven/Documents/CsV/xlsx/2b. Example.xlsx",
        "/Users/steven/Documents/CsV/xlsx/CONSTANT_1950 horror 1.xlsx",
        "/Users/steven/Documents/CsV/xlsx/CONSTANT_1950 horror.xlsx",
        "/Users/steven/Documents/CsV/xlsx/avatars 1.xlsx",
        Path("/Users/steven/Documents/CsV/xlsx/avatars.xlsx"),
        Path("/Users/steven/Documents/CsV/xlsx/Discography-v4.xlsx"),
        "/Users/steven/Documents/CsV/xlsx/Glory Shorts.xlsx",
        "/Users/steven/Documents/CsV/xlsx/gtrivia-emoji 1.xlsx",
        Path("/Users/steven/Documents/CsV/xlsx/gtrivia-emoji.xlsx"),
        "/Users/steven/Documents/CsV/xlsx/GTrivia-Grid view.xlsx",
        Path("/Users/steven/Documents/CsV/xlsx/layout.xlsx"),
        Path("/Users/steven/Documents/CsV/xlsx/NoteGPT-Flashcards-CONSTANT_1738731384372.xlsx"),
        "/Users/steven/Documents/CsV/xlsx/Obscure horror facts 1.xlsx",
        "/Users/steven/Documents/CsV/xlsx/WooLy 1.xlsx",
        Path("/Users/steven/Documents/CsV/xlsx/WooLy.xlsx")
    ]
    
    # Filter existing files
    existing_files = [f for f in excel_files if os.path.exists(f)]
    
    if not existing_files:
        logger.info("❌ No Excel files found to analyze")
        return
    
    logger.info(f"📁 Found {len(existing_files)} Excel files to analyze")
    
    # Generate organization report
    report = analyzer.generate_organization_report(existing_files)
    
    # Save report
    with open('advanced_organization_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    logger.info("\n📊 Organization Report Summary:")
    logger.info(f"Total files analyzed: {report['summary']['total_files']}")
    logger.info(f"Average quality score: {report['summary']['average_score']:.2f}")
    logger.info(f"Categories found: {len(report['summary']['categories'])}")
    logger.info(f"Top patterns: {list(report['summary']['top_patterns'].keys())[:5]}")
    
    logger.info("\n🎯 Key Recommendations:")
    for i, rec in enumerate(report['recommendations'][:10], 1):
        logger.info(f"{i}. {rec}")
    
    logger.info(f"\n📄 Full report saved to: advanced_organization_report.json")

if __name__ == "__main__":
    main()