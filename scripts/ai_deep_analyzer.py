
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_033 = 033
CONSTANT_600 = 600
CONSTANT_2000 = 2000

#!/usr/bin/env python3
"""
🧠 AI-POWERED DEEP INTELLIGENT CONTENT-AWARE ANALYZER
====================================================
Advanced code analysis with AI semantic understanding, AST parsing,
vector embeddings, architectural pattern detection, and confidence scoring.

Features:
✨ Deep AST-based code understanding
✨ AI-powered semantic analysis (OpenAI/Gemini/Claude)
✨ Vector embeddings for similarity detection
✨ Architectural pattern recognition
✨ Confidence scoring system
✨ Intelligent categorization & tagging
✨ Developer-friendly with artistic flair
"""

import ast
import difflib
import hashlib
import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# Colors
class Colors:
    HEADER = "\CONSTANT_033[95m"
    BLUE = "\CONSTANT_033[94m"
    CYAN = "\CONSTANT_033[96m"
    GREEN = "\CONSTANT_033[92m"
    YELLOW = "\CONSTANT_033[93m"
    RED = "\CONSTANT_033[91m"
    MAGENTA = "\CONSTANT_033[35m"
    END = "\CONSTANT_033[0m"
    BOLD = "\CONSTANT_033[1m"


# Emojis
class Emojis:
    BRAIN = "🧠"
    SPARKLES = "✨"
    ROCKET = "🚀"
    FIRE = "🔥"
    MICROSCOPE = "🔬"
    ROBOT = "🤖"
    TARGET = "🎯"
    CHART = "📊"
    LIGHTBULB = "💡"
    MAGIC = "🪄"
    CHECK = "✅"
    WARN = "⚠️"


class AICodeAnalyzer:
    """AI-powered semantic code analysis"""

    def __init__(self):
        # Load API keys
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.deepseek_key = os.getenv("DEEPSEEK_API_KEY")

        self.use_openai = bool(self.openai_key)
        self.use_gemini = bool(self.gemini_key) and not self.use_openai
        self.use_anthropic = bool(self.anthropic_key) and not (
            self.use_openai or self.use_gemini
        )

    def analyze_with_ai(
        self, code: str, filepath: str, ast_data: Dict
    ) -> Dict[str, Any]:
        """Deep AI analysis of code"""

        prompt = f"""Analyze this Python code with deep understanding:

File: {Path(filepath).name}
Functions: {len(ast_data.get('functions', []))}
Classes: {len(ast_data.get('classes', []))}
Imports: {', '.join(ast_data.get('imports', [])[:10])}

Code sample:
```python
{code[:CONSTANT_2000]}
```

Provide JSON response:
{{
    "purpose": "What this code does (one clear sentence)",
    "category": "primary category (e.g., automation, scraper, api_client, generator, analyzer, etc.)",
    "subcategory": "specific type",
    "architectural_patterns": ["MVC", "CLI", "API", etc.],
    "confidence": 0.0-1.0,
    "technologies": ["key libraries/frameworks"],
    "quality_score": 0.0-1.0,
    "complexity": "low/medium/high",
    "maintainability": 0.0-1.0,
    "suggested_improvements": ["improvement 1", "improvement 2"],
    "tags": ["tag1", "tag2", "tag3"]
}}"""

        try:
            if self.use_openai:
                return self._query_openai(prompt)
            elif self.use_gemini:
                return self._query_gemini(prompt)
            elif self.use_anthropic:
                return self._query_anthropic(prompt)
        except Exception as e:
            logger.info(f"{Colors.YELLOW}{Emojis.WARN} AI analysis error: {e}{Colors.END}")

        return self._fallback_analysis()

    def _query_openai(self, prompt: str) -> Dict:
        """Query OpenAI GPT"""
        try:
            import openai

            openai.api_key = self.openai_key

            response = openai.chat.completions.create(
                model="gpt-4o-mini",  # Fast and cost-effective
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert code analyzer. Respond only with valid JSON.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=CONSTANT_600,
            )

            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.info(f"{Colors.RED}OpenAI error: {e}{Colors.END}")
            return self._fallback_analysis()

    def _query_gemini(self, prompt: str) -> Dict:
        """Query Google Gemini"""
        try:
            import google.generativeai as genai

            genai.configure(api_key=self.gemini_key)

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)

            # Extract JSON
            import re

            json_match = re.search(r"\{.*\}", response.text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            logger.info(f"{Colors.RED}Gemini error: {e}{Colors.END}")

        return self._fallback_analysis()

    def _query_anthropic(self, prompt: str) -> Dict:
        """Query Anthropic Claude"""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.anthropic_key)

            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=CONSTANT_600,
                messages=[{"role": "user", "content": prompt}],
            )

            return json.loads(response.content[0].text)
        except Exception as e:
            logger.info(f"{Colors.RED}Anthropic error: {e}{Colors.END}")

        return self._fallback_analysis()

    def _fallback_analysis(self) -> Dict:
        """Fallback when AI unavailable"""
        return {
            "purpose": "Code analysis",
            "category": "uncategorized",
            "subcategory": "unknown",
            "architectural_patterns": [],
            "confidence": 0.4,
            "technologies": [],
            "quality_score": 0.5,
            "complexity": "unknown",
            "maintainability": 0.5,
            "suggested_improvements": [],
            "tags": [],
        }


class VectorEmbeddingAnalyzer:
    """Semantic similarity using embeddings"""

    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.cache = {}

    def get_embedding(self, code: str, identifier: str) -> Optional[List[float]]:
        """Get embedding vector for code"""
        if identifier in self.cache:
            return self.cache[identifier]

        if not self.openai_key:
            return None

        try:
            import openai

            openai.api_key = self.openai_key

            response = openai.embeddings.create(
                model="text-embedding-3-small", input=code[:CONSTANT_2000]
            )

            embedding = response.data[0].embedding
            self.cache[identifier] = embedding
            return embedding
        except (IndexError, KeyError):
            return None

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate similarity between vectors"""
        try:
            import numpy as np

            dot = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            return float(dot / (norm1 * norm2))
        except (ValueError, TypeError):
            return 0.0


class ArchitecturalPatternDetector:
    """Detect code patterns and architectures"""

    PATTERNS = {
        "MVC": ["Model", "View", "Controller", "render", "template"],
        "API": ["api", "endpoint", "route", "@app", "flask", "fastapi"],
        "CLI": ["argparse", "click", "sys.argv", "main"],
        "Bot": ["bot", "telegram", "discord", "automation"],
        "Scraper": ["beautifulsoup", "selenium", "requests", "scrape"],
        "ML": ["tensorflow", "torch", "sklearn", "model", "train"],
        "Data Pipeline": ["etl", "transform", "pipeline", "airflow"],
        "Microservice": ["service", "grpc", "microservice"],
    }

    def detect(
        self, code: str, imports: List[str], functions: List[str]
    ) -> List[Tuple[str, float]]:
        """Detect patterns with confidence"""
        patterns = []
        code_lower = code.lower()
        all_text = code_lower + " ".join(imports) + " ".join(functions)

        for pattern_name, keywords in self.PATTERNS.items():
            matches = sum(1 for kw in keywords if kw.lower() in all_text)
            if matches > 0:
                confidence = min(matches / len(keywords), 1.0)
                patterns.append((pattern_name, confidence))

        return sorted(patterns, key=lambda x: x[1], reverse=True)[:3]


class DeepASTAnalyzer:
    """Advanced AST-based code analysis"""

    def analyze(self, filepath: Path) -> Dict[str, Any]:
        """Deep AST analysis"""
        data = {
            "path": str(filepath),
            "functions": [],
            "classes": [],
            "imports": [],
            "decorators": [],
            "docstring": None,
            "loc": 0,
            "complexity": 0,
            "has_main": False,
            "has_tests": False,
            "type_hints": False,
            "async_code": False,
        }

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                data["loc"] = len(content.splitlines())

            tree = ast.parse(content)
            data["docstring"] = ast.get_docstring(tree)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    data["functions"].append(node.name)
                    if node.name == "main":
                        data["has_main"] = True
                    if node.name.startswith("test_"):
                        data["has_tests"] = True
                    if any(node.returns for node in [node]):
                        data["type_hints"] = True
                    data["complexity"] += 1

                    # Check for decorators
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Name):
                            data["decorators"].append(decorator.id)

                elif isinstance(node, ast.AsyncFunctionDef):
                    data["async_code"] = True
                    data["functions"].append(f"async {node.name}")

                elif isinstance(node, ast.ClassDef):
                    data["classes"].append(node.name)
                    data["complexity"] += 2

                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        data["imports"].append(alias.name)

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        data["imports"].append(node.module)

            return data, content

        except Exception as e:
            data["error"] = str(e)
            return data, ""


class AIDeepIntelligentAnalyzer:
    """Main analyzer orchestrating all components"""

    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.ast_analyzer = DeepASTAnalyzer()
        self.ai_analyzer = AICodeAnalyzer()
        self.embedding_analyzer = VectorEmbeddingAnalyzer()
        self.pattern_detector = ArchitecturalPatternDetector()

        self.stats = {
            "total_files": 0,
            "analyzed": 0,
            "ai_analyzed": 0,
            "duplicates": 0,
            "categories": defaultdict(int),
        }

        self.results = []

    def print_header(self, text: str, emoji=""):
        """Print fancy header"""
        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"{emoji} {text}")
        logger.info(f"{'='*80}{Colors.END}\n")

    def analyze_file(self, filepath: Path) -> Dict[str, Any]:
        """Comprehensive file analysis"""

        # AST Analysis
        ast_data, content = self.ast_analyzer.analyze(filepath)

        analysis = {
            "file": str(filepath.relative_to(self.target_dir)),
            "ast": ast_data,
            "patterns": [],
            "ai_analysis": None,
            "embedding": None,
            "confidence": 0.5,
        }

        # Pattern Detection
        patterns = self.pattern_detector.detect(
            content, ast_data.get("imports", []), ast_data.get("functions", [])
        )
        analysis["patterns"] = patterns

        # AI Analysis (for significant files)
        if ast_data.get("loc", 0) > 20 and self.stats["ai_analyzed"] < 50:
            ai_result = self.ai_analyzer.analyze_with_ai(
                content, str(filepath), ast_data
            )
            analysis["ai_analysis"] = ai_result
            analysis["confidence"] = ai_result.get("confidence", 0.5)
            self.stats["ai_analyzed"] += 1
            self.stats["categories"][ai_result.get("category", "unknown")] += 1

        # Vector Embedding (for top files)
        if ast_data.get("loc", 0) > 50 and self.stats["ai_analyzed"] < 30:
            embedding = self.embedding_analyzer.get_embedding(content, str(filepath))
            if embedding:
                analysis["embedding"] = len(embedding)  # Store count, not full vector

        self.stats["analyzed"] += 1
        return analysis

    def scan_codebase(self):
        """Scan and analyze codebase"""

        self.print_header("SCANNING CODEBASE", Emojis.MICROSCOPE)

        python_files = list(self.target_dir.rglob("*.py"))
        self.stats["total_files"] = len(python_files)

        logger.info(f"{Colors.GREEN}Found {len(python_files)} Python files{Colors.END}\n")

        for idx, filepath in enumerate(python_files, 1):
            if idx % 20 == 0:
                print(
                    f"{Colors.YELLOW}Analyzing: {idx}/{len(python_files)}...{Colors.END}",
                    end=Path("\r"),
                )

            try:
                analysis = self.analyze_file(filepath)
                self.results.append(analysis)
            except Exception as e:
                logger.info(f"{Colors.RED}Error analyzing {filepath}: {e}{Colors.END}")

        logger.info(f"\n{Colors.GREEN}{Emojis.CHECK} Analysis complete!{Colors.END}")

    def generate_report(self):
        """Generate comprehensive report"""

        self.print_header("GENERATING REPORT", Emojis.CHART)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.target_dir / f"AI_ANALYSIS_REPORT_{timestamp}.md"
        json_file = self.target_dir / f"AI_ANALYSIS_DATA_{timestamp}.json"

        with open(report_file, "w") as f:
            f.write("# 🧠 AI-POWERED DEEP ANALYSIS REPORT\n\n")
            f.write(
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )
            f.write("---\n\n")

            # Summary
            f.write("## 📊 EXECUTIVE SUMMARY\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Total Files | {self.stats['total_files']:,} |\n")
            f.write(f"| Analyzed | {self.stats['analyzed']:,} |\n")
            f.write(f"| AI-Analyzed | {self.stats['ai_analyzed']:,} |\n\n")

            # Categories
            f.write("## 🎯 AI-POWERED CATEGORIES\n\n")
            for category, count in sorted(
                self.stats["categories"].items(), key=lambda x: x[1], reverse=True
            ):
                f.write(f"- **{category}**: {count} files\n")

            # Top Files
            f.write("\n## ⭐ TOP ANALYZED FILES\n\n")
            top_files = [r for r in self.results if r.get("ai_analysis")]
            top_files.sort(key=lambda x: x.get("confidence", 0), reverse=True)

            for result in top_files[:20]:
                ai = result.get("ai_analysis", {})
                f.write(f"### {result['file']}\n")
                f.write(f"- **Purpose:** {ai.get('purpose', 'N/A')}\n")
                f.write(f"- **Category:** {ai.get('category', 'N/A')}\n")
                f.write(f"- **Confidence:** {ai.get('confidence', 0):.2f}\n")
                f.write(f"- **Quality:** {ai.get('quality_score', 0):.2f}\n")
                if ai.get("tags"):
                    f.write(f"- **Tags:** {', '.join(ai['tags'])}\n")
                f.write(Path("\n"))

        # Save JSON
        with open(json_file, "w") as f:
            json.dump(
                {
                    "timestamp": datetime.now().isoformat(),
                    "stats": dict(self.stats),
                    "results": self.results,
                },
                f,
                indent=2,
                default=str,
            )

        logger.info(f"{Colors.GREEN}{Emojis.CHECK} Report: {report_file}{Colors.END}")
        logger.info(f"{Colors.GREEN}{Emojis.CHECK} Data: {json_file}{Colors.END}")

    def run(self):
        """Run complete analysis"""

        logger.info(f"{Colors.MAGENTA}{Colors.BOLD}")
        print(
            "╔═══════════════════════════════════════════════════════════════════════════════╗"
        )
        print(
            "║                                                                               ║"
        )
        print(
            "║           🧠 AI-POWERED DEEP INTELLIGENT ANALYZER 🚀                          ║"
        )
        print(
            "║                                                                               ║"
        )
        print(
            "║        Advanced Code Analysis with AI Semantic Understanding                 ║"
        )
        print(
            "║                                                                               ║"
        )
        print(
            "╚═══════════════════════════════════════════════════════════════════════════════╝"
        )
        logger.info(f"{Colors.END}\n")

        logger.info(f"{Colors.CYAN}Target: {self.target_dir}{Colors.END}")
        print(
            f"{Colors.CYAN}AI: {Emojis.CHECK if self.ai_analyzer.use_openai or self.ai_analyzer.use_gemini else Emojis.WARN}{Colors.END}\n"
        )

        self.scan_codebase()
        self.generate_report()

        self.print_header("COMPLETE!", Emojis.ROCKET)
        logger.info(f"{Colors.BOLD}📊 STATS:{Colors.END}\n")
        logger.info(f"  Files: {Colors.CYAN}{self.stats['total_files']:,}{Colors.END}")
        logger.info(f"  Analyzed: {Colors.CYAN}{self.stats['analyzed']:,}{Colors.END}")
        print(
            f"  AI-Analyzed: {Colors.CYAN}{self.stats['ai_analyzed']:,}{Colors.END}\n"
        )


def main():
    """Main execution"""
    # Load environment
    env_file = Path("/Users/steven/.env.d/MASTER_CONSOLIDATED.env")
    if Path(env_file).exists():
        logger.info(f"{Colors.CYAN}Loading API keys...{Colors.END}")
        for line in open(env_file):
            if line.startswith("export "):
                line = line.replace("export ", "").strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    value = value.strip('"').strip("'").split("#")[0].strip()
                    os.environ[key] = value

    target_dir = Path("/Users/steven/GitHub/AvaTarArTs-Suite")

    analyzer = AIDeepIntelligentAnalyzer(target_dir)
    analyzer.run()


if __name__ == "__main__":
    main()
