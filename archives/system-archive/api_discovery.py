#!/usr/bin/env python3
"""
🔍 API DISCOVERY ENGINE
=======================
Auto-discovers all available APIs from ~/.env.d/ and intelligently routes requests.
"""

import os
import logging
from pathlib import Path
from typing import Dict, List
from collections import defaultdict
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class APIDiscoveryEngine:
    """
    Discovers and categorizes all available API services
    """

    def __init__(self, env_directory: Path = None):
        if env_directory is None:
            env_directory = Path.home() / ".env.d"

        self.env_directory = env_directory
        self.available_apis: Dict[str, Dict] = {}
        self.api_categories: Dict[str, List[str]] = defaultdict(list)
        self.loaded_env_files: List[Path] = []

    def discover_all_apis(self) -> Dict[str, Dict]:
        """
        Scan ~/.env.d/ and categorize all available APIs
        Returns dict of API configurations
        """
        logger.info("🔍 Discovering APIs from ~/.env.d/...")

        if not self.env_directory.exists():
            logger.warning(f"⚠️  {self.env_directory} not found")
            return {}

        # Load all .env files
        env_files = sorted(self.env_directory.glob("*.env"))

        for env_file in env_files:
            try:
                load_dotenv(env_file)
                self.loaded_env_files.append(env_file)
                logger.info(f"   ✅ Loaded: {env_file.name}")
            except Exception as e:
                logger.error(f"   ❌ Failed to load {env_file.name}: {e}")

        # Categorize APIs
        self._categorize_discovered_apis()

        # Log summary
        logger.info("\n📊 Discovery Summary:")
        logger.info(f"   Total APIs: {len(self.available_apis)}")
        logger.info(f"   Categories: {len(self.api_categories)}")

        for category, apis in sorted(self.api_categories.items()):
            if apis:
                logger.info(f"   {category.title()}: {len(apis)}")

        return self.available_apis

    def _categorize_discovered_apis(self):
        """Categorize all discovered APIs by function"""

        # Category patterns
        categories = {
            "llm": [
                "OPENAI",
                "ANTHROPIC",
                "GOOGLE",
                "GEMINI",
                "DEEPSEEK",
                "MISTRAL",
                "GROQ",
                "CEREBRAS",
                "COHERE",
                "FIREWORKS",
                "TOGETHER",
                "PERPLEXITY",
                "OPENROUTER",
                "CLAUDE",
            ],
            "image": [
                "LEONARDO",
                "STABILITY",
                "REPLICATE",
                "FAL",
                "RUNWAY",
                "IMAGGA",
                "REMOVEBG",
                "VANCEAI",
                "DALLE",
                "MIDJOURNEY",
            ],
            "audio": [
                "ELEVENLABS",
                "DEEPGRAM",
                "ASSEMBLYAI",
                "MURF",
                "RESEMBLE",
                "REVAI",
                "DESCRIPT",
                "WHISPER",
                "SUNO",
                "UDIO",
            ],
            "video": [
                "RUNWAY",
                "SORA",
                "HEYGEN",
                "STABLE_VIDEO_DIFFUSION",
                "PIKA",
                "SYNTHESIA",
            ],
            "analytics": [
                "NEWSAPI",
                "SERPAPI",
                "SCRAPINGBEE",
                "SCRAPINGBOT",
                "BRIGHTDATA",
                "APIFY",
            ],
            "automation": ["ZAPIER", "MAKE", "N8N", "INTEGROMAT"],
            "vector_db": [
                "PINECONE",
                "QDRANT",
                "CHROMADB",
                "ZEP",
                "LLAMAINDEX",
                "WEAVIATE",
                "MILVUS",
            ],
            "monitoring": ["BETTERUPTIME", "LANGSMITH", "SENTRY", "DATADOG"],
            "cloud": ["AWS", "AZURE", "GCP", "CLOUDFLARE", "VERCEL", "NETLIFY"],
            "search": ["ALGOLIA", "ELASTICSEARCH", "MEILISEARCH"],
            "storage": ["S3", "CLOUDINARY", "UPLOADCARE", "FILESTACK"],
        }

        # Scan all environment variables
        for key, value in os.environ.items():
            if not value or value == "":
                continue

            # Check for API keys
            if "API_KEY" in key or "KEY" in key or "TOKEN" in key:
                api_name = (
                    key.replace("_API_KEY", "")
                    .replace("_KEY", "")
                    .replace("_TOKEN", "")
                    .replace("_SECRET", "")
                )

                self.available_apis[api_name] = {
                    "key_name": key,
                    "available": True,
                    "value_length": len(value),
                    "categories": [],
                }

                # Categorize
                for category, patterns in categories.items():
                    if any(pattern in api_name.upper() for pattern in patterns):
                        self.api_categories[category].append(api_name)
                        self.available_apis[api_name]["categories"].append(category)

                # If no category found, add to 'other'
                if not self.available_apis[api_name]["categories"]:
                    self.api_categories["other"].append(api_name)
                    self.available_apis[api_name]["categories"].append("other")

    def get_apis_for_category(self, category: str) -> List[str]:
        """Get all APIs in a specific category"""
        return self.api_categories.get(category, [])

    def is_api_available(self, api_name: str) -> bool:
        """Check if specific API is available"""
        return api_name in self.available_apis

    def get_best_api_for_task(:
        self, category: str, preferences: List[str] = None
    ) -> Optional[str]:
        """
        Get best available API for a task based on preferences
        """
        available = self.get_apis_for_category(category)

        if not available:
            return None

        # Check preferences first
        if preferences:
            for pref in preferences:
                for api in available:
                    if pref.upper() in api.upper():
                        return api

        # Return first available
        return available[0]

    def generate_capabilities_report(self) -> str:
        """Generate comprehensive capabilities report"""
        lines = []
        lines.append("=" * 80)
        lines.append("🔍 API DISCOVERY REPORT")
        lines.append("=" * 80)
        lines.append("")

        lines.append(f"📊 Total APIs Discovered: {len(self.available_apis)}")
        lines.append(f"📁 Loaded .env files: {len(self.loaded_env_files)}")
        lines.append("")

        lines.append("🎯 APIs by Category:")
        lines.append("")

        for category, apis in sorted(self.api_categories.items()):
            if apis:
                lines.append(f"  {category.upper()} ({len(apis)}):")
                for api in sorted(apis):
                    lines.append(f"    ✅ {api}")
                lines.append("")

        return "\n".join(lines)
