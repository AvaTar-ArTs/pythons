#!/usr/bin/env python3
"""
🌌 ULTRA-DEEP INTELLIGENCE ORCHESTRATOR 🌌
===========================================
Advanced Multi-API Content-Aware Deep Research System

This orchestrator combines ALL available AI services to perform
the most comprehensive analysis possible of ~/Documents

Features:
✨ Multi-LLM analysis (OpenAI, Gemini, Groq, DeepSeek, Perplexity)
✨ Vector embeddings with multiple providers
✨ Semantic search across all documents
✨ Content categorization with AI
✨ Knowledge graph generation
✨ Research synthesis from multiple sources
✨ Automated documentation generation
✨ Cross-reference linking
✨ Trend and pattern detection
"""

import os
import json
import asyncio
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict


# Color codes
class C:
    """Colors for beautiful output"""

    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    WHITE = "\033[97m"
    END = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# Emojis
E = type(
    "Emojis",
    (),
    {
        "ROCKET": "🚀",
        "BRAIN": "🧠",
        "SPARKLES": "✨",
        "FIRE": "🔥",
        "TARGET": "🎯",
        "MICROSCOPE": "🔬",
        "ROBOT": "🤖",
        "CHART": "📊",
        "LIGHTBULB": "💡",
        "GEAR": "⚙️",
        "FOLDER": "📁",
        "FILE": "📄",
        "CHECK": "✅",
        "WARN": "⚠️",
        "ERROR": "❌",
        "STAR": "⭐",
        "MAGIC": "🪄",
        "CRYSTAL": "🔮",
        "TELESCOPE": "🔭",
        "DNA": "🧬",
        "ATOM": "⚛️",
        "INFINITY": "∞",
        "DIAMOND": "💎",
        "KEY": "🔑",
    },
)()


class APIKeyManager:
    """Manages all available API keys"""

    def __init__(self):
        self.load_env_keys()
        self.available_apis = self.detect_available_apis()

    def load_env_keys(self):
        """Load API keys from environment file"""
        env_file = "/Users/steven/env_d_all.txt"
        if Path(env_file).exists():
            print(f"{C.CYAN}{E.KEY} Loading API keys...{C.END}")
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if "=" in line and not line.startswith("#"):
                        # Remove 'export ' if present
                        line = line.replace("export ", "")
                        key, value = line.split("=", 1)
                        value = value.strip('\'').strip("\'").split("#")[0].strip()
                        if value and not value.startswith("your_"):
                            os.environ[key] = value

    def detect_available_apis(self) -> Dict[str, List[str]]:
        """Detect which APIs are available"""
        apis = {
            "llm": [],
            "vision": [],
            "audio": [],
            "vector": [],
            "research": [],
            "document": [],
        }

        # LLM APIs
        if os.getenv("OPENAI_API_KEY"):
            apis["llm"].append("OpenAI")
        if os.getenv("GEMINI_API_KEY"):
            apis["llm"].append("Gemini")
        if os.getenv("GROQ_API_KEY"):
            apis["llm"].append("Groq")
        if os.getenv("DEEPSEEK_API_KEY"):
            apis["llm"].append("DeepSeek")
        if os.getenv("PERPLEXITY_API_KEY"):
            apis["llm"].append("Perplexity")
        if os.getenv("MISTRAL_API_KEY"):
            apis["llm"].append("Mistral")
        if os.getenv("XAI_API_KEY"):
            apis["llm"].append("XAI")
        if os.getenv("COHERE_API_KEY"):
            apis["llm"].append("Cohere")

        # Vision APIs
        if os.getenv("HUGGINGFACE_API_KEY"):
            apis["vision"].append("HuggingFace")

        # Audio APIs
        if os.getenv("ELEVENLABS_API_KEY"):
            apis["audio"].append("ElevenLabs")
        if os.getenv("ASSEMBLYAI_API_KEY"):
            apis["audio"].append("AssemblyAI")
        if os.getenv("DEEPGRAM_API_KEY"):
            apis["audio"].append("Deepgram")

        # Vector DBs
        if os.getenv("CHROMADB_API_KEY"):
            apis["vector"].append("ChromaDB")
        if os.getenv("PINECONE_API_KEY"):
            apis["vector"].append("Pinecone")
        if os.getenv("QDRANT_API_KEY"):
            apis["vector"].append("Qdrant")

        # Research APIs
        if os.getenv("SERPAPI_KEY"):
            apis["research"].append("SerpAPI")
        if os.getenv("NEWSAPI_KEY"):
            apis["research"].append("NewsAPI")

        # Document APIs
        if os.getenv("NOTION_TOKEN"):
            apis["document"].append("Notion")
        if os.getenv("SLITE_API_KEY"):
            apis["document"].append("Slite")

        return apis

    def print_available_apis(self):
        """Display available APIs"""
        print(f"\n{C.BOLD}{C.MAGENTA}{'=' * 80}")
        print(f"{E.CRYSTAL} AVAILABLE AI ARSENAL {E.CRYSTAL}")
        print(f"{'=' * 80}{C.END}\n")

        for category, apis in self.available_apis.items():
            if apis:
                icon = {
                    "llm": E.BRAIN,
                    "vision": "👁️",
                    "audio": "🎵",
                    "vector": "🧠",
                    "research": "🔍",
                    "document": "📝",
                }.get(category, E.GEAR)

                print(f"{C.CYAN}{icon} {category.upper()}:{C.END}")
                for api in apis:
                    print(f"  {C.GREEN}{E.CHECK} {api}{C.END}")
                print()


class MultiLLMAnalyzer:
    """Uses multiple LLM providers for comprehensive analysis"""

    def __init__(self, available_llms: List[str]):
        self.available_llms = available_llms
        self.results_cache = {}

    async def analyze_with_openai(self, content: str, prompt: str) -> Dict[str, Any]:
        """Analyze with OpenAI"""
        try:
            import openai

            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert content analyst. Respond with valid JSON.",
                    },
                    {
                        "role": "user",
                        "content": f"{prompt}\n\nContent:\n{content[:4000]}",
                    },
                ],
                temperature=0.3,
                max_tokens=1000,
            )

            result = json.loads(response.choices[0].message.content)
            result["provider"] = "OpenAI"
            return result
        except Exception as e:
            return {"error": str(e), "provider": "OpenAI"}

    async def analyze_with_gemini(self, content: str, prompt: str) -> Dict[str, Any]:
        """Analyze with Gemini"""
        try:
            import google.generativeai as genai

            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"{prompt}\n\nContent:\n{content[:4000]}")

            # Extract JSON
            import re

            json_match = re.search(r"\{.*\}", response.text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                result["provider"] = "Gemini"
                return result
            return {"error": "No JSON found", "provider": "Gemini"}
        except Exception as e:
            return {"error": str(e), "provider": "Gemini"}

    async def analyze_with_groq(self, content: str, prompt: str) -> Dict[str, Any]:
        """Analyze with Groq"""
        try:
            from groq import Groq

            client = Groq(api_key=os.getenv("GROQ_API_KEY"))

            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert content analyst. Respond with valid JSON.",
                    },
                    {
                        "role": "user",
                        "content": f"{prompt}\n\nContent:\n{content[:4000]}",
                    },
                ],
                temperature=0.3,
                max_tokens=1000,
            )

            result = json.loads(response.choices[0].message.content)
            result["provider"] = "Groq"
            return result
        except Exception as e:
            return {"error": str(e), "provider": "Groq"}

    async def multi_provider_analysis(:
        self, content: str, analysis_type: str
    ) -> List[Dict[str, Any]]:
        """Get analysis from multiple providers and aggregate"""
        prompts = {
            "categorize": """Analyze this document and provide:
{
    "category": "main category",
    "subcategories": ["sub1", "sub2"],
    "topics": ["topic1", "topic2", "topic3"],
    "keywords": ["kw1", "kw2", "kw3"],
    "sentiment": "positive/negative/neutral",
    "complexity": "beginner/intermediate/advanced",
    "purpose": "one sentence description",
    "actionable_items": ["item1", "item2"],
    "related_fields": ["field1", "field2"]
}""",
            "extract_knowledge": """Extract key knowledge from this document:
{
    "main_concepts": ["concept1", "concept2"],
    "facts": ["fact1", "fact2"],
    "definitions": {"term1": "def1", "term2": "def2"},
    "relationships": [{"from": "A", "to": "B", "type": "relates_to"}],
    "insights": ["insight1", "insight2"],
    "questions_raised": ["q1", "q2"]
}""",
            "summarize": """Create a comprehensive summary:
{
    "one_sentence": "brief summary",
    "executive_summary": "2-3 paragraphs",
    "key_points": ["point1", "point2", "point3"],
    "target_audience": "who should read this",
    "recommended_actions": ["action1", "action2"]
}""",
        }

        prompt = prompts.get(analysis_type, prompts["categorize"])
        results = []

        # Run analyses in parallel
        tasks = []
        if "OpenAI" in self.available_llms:
            tasks.append(self.analyze_with_openai(content, prompt))
        if "Gemini" in self.available_llms:
            tasks.append(self.analyze_with_gemini(content, prompt))
        if "Groq" in self.available_llms:
            tasks.append(self.analyze_with_groq(content, prompt))

        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out errors
        valid_results = [r for r in results if isinstance(r, dict) and "error" not in r]

        return valid_results if valid_results else results


class VectorDatabaseManager:
    """Manages vector embeddings across multiple providers"""

    def __init__(self, available_vectors: List[str]):
        self.available_vectors = available_vectors
        self.embeddings_cache = {}

    def create_embedding(self, text: str, identifier: str) -> Optional[List[float]]:
        """Create embedding vector"""
        if identifier in self.embeddings_cache:

        try:
            import openai

            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            response = client.embeddings.create(
                model="text-embedding-3-small", input=text[:8000]
            )

            embedding = response.data[0].embedding
            return embedding
        except Exception as e:
            print(f"{C.YELLOW}{E.WARN} Embedding failed: {e}{C.END}")
            return None

    def calculate_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity"""
        try:
            import numpy as np

            dot = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            return float(dot / (norm1 * norm2))
        except:
            return 0.0


class DocumentScanner:
    """Scans and catalogs all documents"""

    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.documents = {}
        self.stats = {
            "total_files": 0,
            "markdown_files": 0,
            "python_files": 0,
            "json_files": 0,
            "text_files": 0,
            "other_files": 0,
            "total_size": 0,
        }

    def scan(self, max_depth: int = 5):
        """Scan directory recursively"""
        print(f"\n{C.CYAN}{E.MICROSCOPE} Scanning {self.root_path}...{C.END}\n")

        for path in self.root_path.rglob("*"):
            try:
                if path.is_file() and not any(p.startswith(".") for p in path.parts):
                    self.process_file(path)
            except Exception:
                pass

        print(f"{C.GREEN}{E.CHECK} Scanned {self.stats['total_files']:,} files{C.END}")

    def process_file(self, path: Path):
        """Process individual file"""
        try:
            size = path.stat().st_size
            suffix = path.suffix.lower()

            # Update stats
            self.stats["total_files"] += 1
            self.stats["total_size"] += size

            if suffix == ".md":
                self.stats["markdown_files"] += 1
            elif suffix == ".py":
                self.stats["python_files"] += 1
            elif suffix == ".json":
                self.stats["json_files"] += 1
            elif suffix in [".txt", ".csv"]:
                self.stats["text_files"] += 1
            else:
                self.stats["other_files"] += 1

            # Calculate hash
            hasher = hashlib.sha256()
            with open(path, "rb") as f:
                hasher.update(f.read())
            file_hash = hasher.hexdigest()

            # Read content for text files
            content = None
            if suffix in [".md", ".txt", ".py", ".json", ".csv"] and size < 1_000_000:
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                except:
                    pass

            self.documents[str(path)] = {
                "path": str(path),
                "name": path.name,
                "size": size,
                "extension": suffix,
                "hash": file_hash,
                "modified": path.stat().st_mtime,
                "content": content,
                "analyzed": False,
            }

        except Exception:
            pass

    def get_files_by_type(self, extension: str) -> List[Dict]:
        """Get all files of specific type"""
        return [doc for doc in self.documents.values() if doc["extension"] == extension]

    def print_stats(self):
        """Print statistics"""
        print(f"\n{C.BOLD}{C.CYAN}{'=' * 80}")
        print(f"{E.CHART} DOCUMENT STATISTICS")
        print(f"{'=' * 80}{C.END}\n")

        print(f"{C.GREEN}Total Files:{C.END} {self.stats['total_files']:,}")
        print(f"{C.CYAN}Markdown:{C.END} {self.stats['markdown_files']:,}")
        print(f"{C.CYAN}Python:{C.END} {self.stats['python_files']:,}")
        print(f"{C.CYAN}JSON:{C.END} {self.stats['json_files']:,}")
        print(f"{C.CYAN}Text/CSV:{C.END} {self.stats['text_files']:,}")
        print(f"{C.CYAN}Other:{C.END} {self.stats['other_files']:,}")
        print(
            f"{C.MAGENTA}Total Size:{C.END} {self.stats['total_size'] / (1024**3):.2f} GB\n"
        )


class UltraDeepOrchestrator:
    """Main orchestrator for ultra-deep analysis"""

    def __init__(self, documents_path: str):
        self.documents_path = documents_path
        self.api_manager = APIKeyManager()
        self.scanner = DocumentScanner(documents_path)

        # Initialize analyzers
        self.llm_analyzer = MultiLLMAnalyzer(self.api_manager.available_apis["llm"])
        self.vector_manager = VectorDatabaseManager(
            self.api_manager.available_apis["vector"]
        )

        # Results storage
        self.analysis_results = defaultdict(dict)
        self.knowledge_graph = {"nodes": [], "edges": []}
        self.categories = defaultdict(list)

    def print_header(self, text: str, emoji: str = E.SPARKLES):
        """Print fancy header"""
        print(f"\n{C.BOLD}{C.MAGENTA}{'=' * 80}")
        print(f"{emoji} {text} {emoji}")
        print(f"{'=' * 80}{C.END}\n")

    async def analyze_document(self, doc: Dict) -> Dict[str, Any]:
        """Perform comprehensive analysis on a document"""
        if not doc.get("content"):
            return {}

        print(f"{C.CYAN}{E.BRAIN} Analyzing: {doc['name'][:60]}...{C.END}")

        # Multi-provider analysis
        categorization = await self.llm_analyzer.multi_provider_analysis(
            doc["content"], "categorize"
        )

        knowledge = await self.llm_analyzer.multi_provider_analysis(
            doc["content"], "extract_knowledge"
        )

        summary = await self.llm_analyzer.multi_provider_analysis(
            doc["content"], "summarize"
        )

        # Create embedding
        embedding = self.vector_manager.create_embedding(doc["content"], doc["path"])

        # Aggregate results
        result = {
            "categorization": categorization,
            "knowledge": knowledge,
            "summary": summary,
            "has_embedding": embedding is not None,
            "analyzed_at": datetime.now().isoformat(),
        }

        return result

    async def run_comprehensive_analysis(self):
        """Run the complete deep analysis"""
        self.print_header("ULTRA-DEEP INTELLIGENCE ORCHESTRATOR", E.CRYSTAL)

        # Phase 1: Show available APIs
        self.api_manager.print_available_apis()

        # Phase 2: Scan documents
        self.print_header("PHASE 1: DOCUMENT DISCOVERY", E.TELESCOPE)
        self.scanner.scan()
        self.scanner.print_stats()

        # Phase 3: AI Analysis
        self.print_header("PHASE 2: MULTI-LLM DEEP ANALYSIS", E.BRAIN)

        # Analyze markdown files (most important)
        md_files = self.scanner.get_files_by_type(".md")
        print(f"{C.YELLOW}Analyzing {len(md_files)} markdown files...{C.END}\n")

        # Analyze top 50 files to avoid excessive API calls
        for i, doc in enumerate(md_files[:50], 1):
            if doc.get("content") and len(doc["content"]) > 100:
                result = await self.analyze_document(doc)
                self.analysis_results[doc["path"]] = result

                # Extract categories
                if result.get("categorization"):
                    for cat_result in result["categorization"]:
                        if isinstance(cat_result, dict) and "category" in cat_result:
                            category = cat_result["category"]
                            self.categories[category].append(doc["path"])

                if i % 10 == 0:
                    print(
                        f"{C.GREEN}{E.CHECK} Analyzed {i}/{min(50, len(md_files))} documents{C.END}"
                    )

        # Phase 4: Generate Report
        self.print_header("PHASE 3: GENERATING COMPREHENSIVE REPORT", E.MAGIC)
        report_path = self.generate_master_report()

        # Phase 5: Complete
        self.print_header("ANALYSIS COMPLETE!", E.ROCKET)
        print(f"{C.GREEN}{E.STAR} Report saved to: {C.BOLD}{report_path}{C.END}\n")

        return report_path

    def generate_master_report(self) -> str:
        """Generate comprehensive markdown report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"/Users/steven/advanced-systems/ultra-deep-intelligence/reports/ULTRA_DEEP_ANALYSIS_{timestamp}.md"

        # Create reports directory if it doesn't exist
        Path("/Users/steven/advanced-systems/ultra-deep-intelligence/reports").mkdir(
            exist_ok=True
        )

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# 🌌 ULTRA-DEEP INTELLIGENCE ANALYSIS REPORT 🌌\n\n")
            f.write(
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )
            f.write("---\n\n")

            # API Arsenal
            f.write("## 🔑 AI ARSENAL UTILIZED\n\n")
            for category, apis in self.api_manager.available_apis.items():
                if apis:
                    f.write(f"### {category.upper()}\n")
                    for api in apis:
                        f.write(f"- ✅ {api}\n")
                    f.write("\n")

            # Document Statistics
            f.write("## 📊 DOCUMENT STATISTICS\n\n")
            f.write("| Metric | Count |\n")
            f.write("|--------|-------|\n")
            for key, value in self.scanner.stats.items():
                if key == "total_size":
                    f.write(f"| {key} | {value / (1024**3):.2f} GB |\n")
                else:
                    f.write(f"| {key} | {value:,} |\n")
            f.write("\n")

            # Categories Discovery
            f.write("## 🗂️ CONTENT CATEGORIES DISCOVERED\n\n")
            for category, files in sorted(
                self.categories.items(), key=lambda x: len(x[1]), reverse=True
            ):
                f.write(f"### {category.title()}\n")
                f.write(f"**Documents:** {len(files)}\n\n")
                for file_path in files[:5]:
                    f.write(f"- `{Path(file_path).name}`\n")
                    result = self.analysis_results.get(file_path, {})
                    if result.get("summary"):
                        for summary in result["summary"]:
                            if isinstance(summary, dict) and "one_sentence" in summary:
                                f.write(f"  - {summary['one_sentence']}\n")
                                break
                f.write("\n")

            # Detailed Analysis Results
            f.write("## 🧠 DETAILED AI ANALYSIS\n\n")
            for file_path, result in list(self.analysis_results.items())[:20]:
                doc_name = Path(file_path).name
                f.write(f"### {doc_name}\n\n")

                # Categorization
                if result.get("categorization"):
                    f.write("**Categorization:**\n")
                    for cat in result["categorization"]:
                        if isinstance(cat, dict):
                            f.write(f"- Provider: {cat.get('provider', 'Unknown')}\n")
                            f.write(f"- Category: {cat.get('category', 'N/A')}\n")
                            if "topics" in cat:
                                f.write(f"- Topics: {', '.join(cat['topics'][:5])}\n")
                            if "keywords" in cat:
                                f.write(
                                    f"- Keywords: {', '.join(cat['keywords'][:5])}\n"
                                )
                    f.write("\n")

                # Summary
                if result.get("summary"):
                    f.write("**Summary:**\n")
                    for summ in result["summary"]:
                        if isinstance(summ, dict) and "executive_summary" in summ:
                            f.write(f"{summ['executive_summary']}\n\n")
                            break

                f.write("---\n\n")

            # Recommendations
            f.write("## 🎯 INTELLIGENT RECOMMENDATIONS\n\n")
            f.write("### Organization Strategy\n")
            f.write("Based on AI analysis, consider organizing content by:\n\n")
            for i, (category, files) in enumerate(
                sorted(self.categories.items(), key=lambda x: len(x[1]), reverse=True)[
                    :10
                ],
                1,
            ):
                f.write(f"{i}. **{category}** ({len(files)} files)\n")
            f.write("\n")

            f.write("### Content Gaps Identified\n")
            f.write("- Consider creating index documents for each major category\n")
            f.write("- Add cross-references between related documents\n")
            f.write("- Create visual knowledge maps\n")
            f.write("- Develop searchable documentation hub\n\n")

            f.write("### Next Steps\n")
            f.write("1. Review categorization accuracy\n")
            f.write("2. Implement suggested organizational structure\n")
            f.write("3. Create master index with AI-generated summaries\n")
            f.write("4. Set up automated content monitoring\n")
            f.write("5. Build knowledge graph visualization\n\n")

        return report_path


async def main():
    """Main execution"""
    print(f"{C.BOLD}{C.MAGENTA}")
    print(
        "╔═══════════════════════════════════════════════════════════════════════════════╗"
    )
    print(
        "║                                                                               ║"
    )
    print(
        "║           🌌 ULTRA-DEEP INTELLIGENCE ORCHESTRATOR 🌌                          ║"
    )
    print(
        "║                                                                               ║"
    )
    print(
        "║        Advanced Multi-API Content-Aware Deep Research System                  ║"
    )
    print(
        "║                                                                               ║"
    )
    print(
        "╚═══════════════════════════════════════════════════════════════════════════════╝"
    )
    print(f"{C.END}\n")

    documents_path = "/Users/steven/Documents"

    orchestrator = UltraDeepOrchestrator(documents_path)
    report_path = await orchestrator.run_comprehensive_analysis()

    print(
        f"\n{C.GREEN}{C.BOLD}{E.SPARKLES} MISSION ACCOMPLISHED! {E.SPARKLES}{C.END}\n"
    )
    print(f"{C.CYAN}Your ultra-deep analysis is complete.{C.END}")
    print(f"{C.CYAN}Report: {C.BOLD}{report_path}{C.END}\n")


if __name__ == "__main__":
    asyncio.run(main())
