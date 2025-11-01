"""
Ai Config

This module provides functionality for ai config.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
AI CLI Configuration Manager
Tab-based interface for managing API keys and settings
"""

from pathlib import Path
import os
import json
import webbrowser
import time
from typing import Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class APIService:
    name: str
    url: str
    key: str
    description: str
    priority: str
    essential: bool
    enabled: bool = False
    api_key: str = ""
    category: str = ""


class AIConfigManager:
    def __init__(self):
        """__init__ function."""

        self.config_file = os.path.expanduser("~/.ai-config.json")
        self.env_file = os.path.expanduser("~/.env")
        self.current_tab = 0
        self.tabs = [
            "🔥 Essential APIs",
            "⚡ AI/LLM Services",
            "🎨 Image Generation",
            "🎵 Audio/Video",
            "🤖 Automation",
            "📊 Data & Search",
            "☁️ Cloud Services",
            "⚙️ Settings",
        ]

        self.services = self.initialize_services()
        self.load_config()

    def initialize_services(self) -> Dict[str, APIService]:
        """Initialize all available API services"""
        return {
            # ESSENTIAL APIs
            "xai": APIService(
                name="xAI (Grok)",
                url="https://console.x.ai/",
                key="XAI_API_KEY",
                description="Elon Musk's AI company - Grok models",
                priority="HIGH",
                essential=True,
                category="essential",
            ),
            "perplexity": APIService(
                name="Perplexity AI",
                url="https://www.perplexity.ai/settings/api",
                key="PERPLEXITY_API_KEY",
                description="AI-powered search and research",
                priority="HIGH",
                essential=True,
                category="essential",
            ),
            "gemini": APIService(
                name="Google Gemini",
                url="https://makersuite.google.com/app/apikey",
                key="GEMINI_API_KEY",
                description="Google's AI model (free tier available)",
                priority="HIGH",
                essential=True,
                category="essential",
            ),
            # AI/LLM Services
            "huggingface": APIService(
                name="Hugging Face",
                url="https://huggingface.co/settings/tokens",
                key="HUGGINGFACE_API_KEY",
                description="Open source AI models and datasets",
                priority="HIGH",
                essential=False,
                category="ai_llm",
            ),
            "cohere": APIService(
                name="Cohere",
                url="https://dashboard.cohere.ai/",
                key="COHERE_API_KEY",
                description="Language AI platform",
                priority="MEDIUM",
                essential=False,
                category="ai_llm",
            ),
            "fireworks": APIService(
                name="Fireworks AI",
                url="https://fireworks.ai/",
                key="FIREWORKS_API_KEY",
                description="Fast inference for open source models",
                priority="MEDIUM",
                essential=False,
                category="ai_llm",
            ),
            "openrouter": APIService(
                name="OpenRouter",
                url="https://openrouter.ai/",
                key="OPENROUTER_API_KEY",
                description="Universal API for LLMs",
                priority="MEDIUM",
                essential=False,
                category="ai_llm",
            ),
            "langsmith": APIService(
                name="LangSmith",
                url="https://smith.langchain.com/",
                key="LANGSMITH_API_KEY",
                description="LangChain's debugging and monitoring",
                priority="LOW",
                essential=False,
                category="ai_llm",
            ),
            # IMAGE GENERATION
            "leonardo": APIService(
                name="Leonardo AI",
                url="https://leonardo.ai/",
                key="LEONARDO_API_KEY",
                description="AI image generation",
                priority="MEDIUM",
                essential=False,
                category="image",
            ),
            "stability": APIService(
                name="Stability AI",
                url="https://platform.stability.ai/account/keys",
                key="STABILITY_API_KEY",
                description="Stable Diffusion and image generation",
                priority="MEDIUM",
                essential=False,
                category="image",
            ),
            "replicate": APIService(
                name="Replicate",
                url="https://replicate.com/account/api-tokens",
                key="REPLICATE_API_TOKEN",
                description="Run AI models in the cloud",
                priority="MEDIUM",
                essential=False,
                category="image",
            ),
            "runway": APIService(
                name="Runway ML",
                url="https://runwayml.com/",
                key="RUNWAY_API_KEY",
                description="AI video and image generation",
                priority="LOW",
                essential=False,
                category="image",
            ),
            "ideogram": APIService(
                name="Ideogram",
                url="https://ideogram.ai/",
                key="IDEOGRAM_API_KEY",
                description="AI image generation with text",
                priority="LOW",
                essential=False,
                category="image",
            ),
            "kaiber": APIService(
                name="Kaiber",
                url="https://kaiber.ai/",
                key="KAIBER_API_KEY",
                description="AI music video generation",
                priority="LOW",
                essential=False,
                category="image",
            ),
            "pika": APIService(
                name="Pika Labs",
                url="https://pika.art/",
                key="PIKA_API_KEY",
                description="AI video generation",
                priority="LOW",
                essential=False,
                category="image",
            ),
            # AUDIO/VIDEO
            "suno": APIService(
                name="Suno AI",
                url="https://suno.ai/",
                key="SUNO_API_KEY",
                description="AI music generation",
                priority="MEDIUM",
                essential=False,
                category="audio_video",
            ),
            "elevenlabs": APIService(
                name="ElevenLabs",
                url="https://elevenlabs.io/app/settings/api-keys",
                key="ELEVENLABS_API_KEY",
                description="AI voice synthesis",
                priority="MEDIUM",
                essential=False,
                category="audio_video",
            ),
            "assemblyai": APIService(
                name="AssemblyAI",
                url="https://www.assemblyai.com/dashboard/signup",
                key="ASSEMBLYAI_API_KEY",
                description="Speech-to-text API",
                priority="LOW",
                essential=False,
                category="audio_video",
            ),
            "deepgram": APIService(
                name="Deepgram",
                url="https://console.deepgram.com/signup",
                key="DEEPGRAM_API_KEY",
                description="Speech recognition and understanding",
                priority="LOW",
                essential=False,
                category="audio_video",
            ),
            "invideo": APIService(
                name="InVideo",
                url="https://invideo.io/",
                key="INVIDEO_API_KEY",
                description="AI video creation",
                priority="LOW",
                essential=False,
                category="audio_video",
            ),
            "sora": APIService(
                name="Sora AI",
                url="https://openai.com/sora",
                key="SORAI_API_KEY",
                description="OpenAI's video generation",
                priority="LOW",
                essential=False,
                category="audio_video",
            ),
            # AUTOMATION
            "zapier": APIService(
                name="Zapier",
                url="https://zapier.com/app/settings/integrations",
                key="ZAPIER_API_KEY",
                description="Workflow automation",
                priority="LOW",
                essential=False,
                category="automation",
            ),
            "make": APIService(
                name="Make (Integromat)",
                url="https://www.make.com/",
                key="MAKE_API_KEY",
                description="Visual automation platform",
                priority="LOW",
                essential=False,
                category="automation",
            ),
            "twilio": APIService(
                name="Twilio",
                url="https://console.twilio.com/",
                key="TWILIO_ACCOUNT_SID",
                description="Communication platform (SMS, voice, etc.)",
                priority="LOW",
                essential=False,
                category="automation",
            ),
            # DATA & SEARCH
            "serpapi": APIService(
                name="SerpAPI",
                url="https://serpapi.com/",
                key="SERPAPI_KEY",
                description="Google search results API",
                priority="MEDIUM",
                essential=False,
                category="data_search",
            ),
            "newsapi": APIService(
                name="NewsAPI",
                url="https://newsapi.org/register",
                key="NEWSAPI_KEY",
                description="News headlines API",
                priority="LOW",
                essential=False,
                category="data_search",
            ),
            "pinecone": APIService(
                name="Pinecone",
                url="https://app.pinecone.io/",
                key="PINECONE_API_KEY",
                description="Vector database for AI",
                priority="MEDIUM",
                essential=False,
                category="data_search",
            ),
            "supabase": APIService(
                name="Supabase",
                url="https://supabase.com/dashboard",
                key="SUPABASE_KEY",
                description="Open source Firebase alternative",
                priority="LOW",
                essential=False,
                category="data_search",
            ),
            "qdrant": APIService(
                name="Qdrant",
                url="https://cloud.qdrant.io/",
                key="QDRANT_API_KEY",
                description="Vector database and similarity search",
                priority="LOW",
                essential=False,
                category="data_search",
            ),
            "chroma": APIService(
                name="Chroma",
                url="https://www.trychroma.com/",
                key="CHROMADB_API_KEY",
                description="Open source vector database",
                priority="LOW",
                essential=False,
                category="data_search",
            ),
            "zep": APIService(
                name="Zep",
                url="https://www.getzep.com/",
                key="ZEP_API_KEY",
                description="Long-term memory for AI applications",
                priority="LOW",
                essential=False,
                category="data_search",
            ),
            # CLOUD SERVICES
            "azure": APIService(
                name="Azure OpenAI",
                url="https://portal.azure.com/",
                key="AZURE_OPENAI_KEY",
                description="Microsoft's OpenAI service",
                priority="LOW",
                essential=False,
                category="cloud",
            ),
            "notion": APIService(
                name="Notion",
                url="https://www.notion.so/my-integrations",
                key="NOTION_TOKEN",
                description="All-in-one workspace",
                priority="LOW",
                essential=False,
                category="cloud",
            ),
            "slite": APIService(
                name="Slite",
                url="https://slite.com/",
                key="SLITE_API_KEY",
                description="Team knowledge base",
                priority="LOW",
                essential=False,
                category="cloud",
            ),
        }

    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                    for key, service_data in config.get("services", {}).items():
                        if key in self.services:
                            self.services[key].enabled = service_data.get("enabled", False)
                            self.services[key].api_key = service_data.get("api_key", "")
            except Exception as e:
                logger.info(f"⚠️  Error loading config: {e}")

    def save_config(self):
        """Save configuration to file"""
        config = {
            "services": {
                key: {"enabled": service.enabled, "api_key": service.api_key} for key, service in self.services.items()
            }
        }

        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)
            logger.info("✅ Configuration saved!")
        except Exception as e:
            logger.info(f"❌ Error saving config: {e}")

    def update_env_file(self):
        """Update .env file with enabled API keys"""
        if not os.path.exists(self.env_file):
            logger.info("❌ .env file not found!")
            return

        with open(self.env_file, "r") as f:
            lines = f.readlines()

        # Update existing keys
        for i, line in enumerate(lines):
            if "=" in line:
                key = line.split("=")[0].strip()
                for service in self.services.values():
                    if service.key == key and service.enabled and service.api_key:
                        lines[i] = f"{service.key}={service.api_key}\n"
                        break

        with open(self.env_file, "w") as f:
            f.writelines(lines)

        logger.info("✅ .env file updated!")

    def get_services_by_category(self, category: str) -> List[tuple]:
        """Get services filtered by category"""
        if category == "essential":
            return [(k, v) for k, v in self.services.items() if v.essential]
        elif category == "ai_llm":
            return [(k, v) for k, v in self.services.items() if v.category == "ai_llm"]
        elif category == "image":
            return [(k, v) for k, v in self.services.items() if v.category == "image"]
        elif category == "audio_video":
            return [(k, v) for k, v in self.services.items() if v.category == "audio_video"]
        elif category == "automation":
            return [(k, v) for k, v in self.services.items() if v.category == "automation"]
        elif category == "data_search":
            return [(k, v) for k, v in self.services.items() if v.category == "data_search"]
        elif category == "cloud":
            return [(k, v) for k, v in self.services.items() if v.category == "cloud"]
        return []

    def display_tab(self):
        """Display current tab content"""
        os.system("clear" if os.name == "posix" else "cls")

        # Header
        logger.info("🤖 AI CLI Configuration Manager")
        logger.info("=" * 60)

        # Tabs
        for i, tab in enumerate(self.tabs):
            if i == self.current_tab:
                logger.info(f"▶️  {tab}", end="  ")
            else:
                logger.info(f"   {tab}", end="  ")
        logger.info(Path("\n") + "=" * 60)

        # Tab content
        if self.current_tab == 0:  # Essential APIs
            self.display_essential_tab()
        elif self.current_tab == 1:  # AI/LLM Services
            self.display_ai_llm_tab()
        elif self.current_tab == 2:  # Image Generation
            self.display_image_tab()
        elif self.current_tab == 3:  # Audio/Video
            self.display_audio_video_tab()
        elif self.current_tab == 4:  # Automation
            self.display_automation_tab()
        elif self.current_tab == 5:  # Data & Search
            self.display_data_search_tab()
        elif self.current_tab == 6:  # Cloud Services
            self.display_cloud_tab()
        elif self.current_tab == 7:  # Settings
            self.display_settings_tab()

        # Footer
        logger.info(Path("\n") + "=" * 60)
        logger.info("Commands: ← → (tabs), 1-9 (toggle), o (open), s (save), q (quit)")

    def display_essential_tab(self):
        """Display essential APIs tab"""
        logger.info("🔥 Essential APIs - Core services for AI CLI")
        logger.info("-" * 50)

        services = self.get_services_by_category("essential")
        for i, (key, service) in enumerate(services, 1):
            status = "✅ ENABLED" if service.enabled else "❌ DISABLED"
            has_key = "🔑" if service.api_key else "🔓"
            essential = " ⭐" if service.essential else ""

            logger.info(f"{i}. {service.name}{essential} - {status} {has_key}")
            logger.info(f"   {service.description}")
            logger.info(f"   Key: {service.key}")
            if service.api_key:
                masked_key = service.api_key[:8] + "..." + service.api_key[-4:] if len(service.api_key) > 12 else "***"
                logger.info(f"   API Key: {masked_key}")
            print()

    def display_ai_llm_tab(self):
        """Display AI/LLM services tab"""
        logger.info("⚡ AI/LLM Services - Language models and AI platforms")
        logger.info("-" * 50)

        services = self.get_services_by_category("ai_llm")
        for i, (key, service) in enumerate(services, 1):
            status = "✅ ENABLED" if service.enabled else "❌ DISABLED"
            has_key = "🔑" if service.api_key else "🔓"
            priority = {"HIGH": "🔥", "MEDIUM": "⚡", "LOW": "📋"}[service.priority]

            logger.info(f"{i}. {priority} {service.name} - {status} {has_key}")
            logger.info(f"   {service.description}")
            logger.info(f"   Key: {service.key}")
            if service.api_key:
                masked_key = service.api_key[:8] + "..." + service.api_key[-4:] if len(service.api_key) > 12 else "***"
                logger.info(f"   API Key: {masked_key}")
            print()

    def display_image_tab(self):
        """Display image generation tab"""
        logger.info("🎨 Image Generation - AI art and visual content")
        logger.info("-" * 50)

        services = self.get_services_by_category("image")
        for i, (key, service) in enumerate(services, 1):
            status = "✅ ENABLED" if service.enabled else "❌ DISABLED"
            has_key = "🔑" if service.api_key else "🔓"
            priority = {"HIGH": "🔥", "MEDIUM": "⚡", "LOW": "📋"}[service.priority]

            logger.info(f"{i}. {priority} {service.name} - {status} {has_key}")
            logger.info(f"   {service.description}")
            logger.info(f"   Key: {service.key}")
            if service.api_key:
                masked_key = service.api_key[:8] + "..." + service.api_key[-4:] if len(service.api_key) > 12 else "***"
                logger.info(f"   API Key: {masked_key}")
            print()

    def display_audio_video_tab(self):
        """Display audio/video tab"""
        logger.info("🎵 Audio/Video - Music, voice, and video generation")
        logger.info("-" * 50)

        services = self.get_services_by_category("audio_video")
        for i, (key, service) in enumerate(services, 1):
            status = "✅ ENABLED" if service.enabled else "❌ DISABLED"
            has_key = "🔑" if service.api_key else "🔓"
            priority = {"HIGH": "🔥", "MEDIUM": "⚡", "LOW": "📋"}[service.priority]

            logger.info(f"{i}. {priority} {service.name} - {status} {has_key}")
            logger.info(f"   {service.description}")
            logger.info(f"   Key: {service.key}")
            if service.api_key:
                masked_key = service.api_key[:8] + "..." + service.api_key[-4:] if len(service.api_key) > 12 else "***"
                logger.info(f"   API Key: {masked_key}")
            print()

    def display_automation_tab(self):
        """Display automation tab"""
        logger.info("🤖 Automation - Workflow and integration tools")
        logger.info("-" * 50)

        services = self.get_services_by_category("automation")
        for i, (key, service) in enumerate(services, 1):
            status = "✅ ENABLED" if service.enabled else "❌ DISABLED"
            has_key = "🔑" if service.api_key else "🔓"
            priority = {"HIGH": "🔥", "MEDIUM": "⚡", "LOW": "📋"}[service.priority]

            logger.info(f"{i}. {priority} {service.name} - {status} {has_key}")
            logger.info(f"   {service.description}")
            logger.info(f"   Key: {service.key}")
            if service.api_key:
                masked_key = service.api_key[:8] + "..." + service.api_key[-4:] if len(service.api_key) > 12 else "***"
                logger.info(f"   API Key: {masked_key}")
            print()

    def display_data_search_tab(self):
        """Display data & search tab"""
        logger.info("📊 Data & Search - Vector databases and search APIs")
        logger.info("-" * 50)

        services = self.get_services_by_category("data_search")
        for i, (key, service) in enumerate(services, 1):
            status = "✅ ENABLED" if service.enabled else "❌ DISABLED"
            has_key = "🔑" if service.api_key else "🔓"
            priority = {"HIGH": "🔥", "MEDIUM": "⚡", "LOW": "📋"}[service.priority]

            logger.info(f"{i}. {priority} {service.name} - {status} {has_key}")
            logger.info(f"   {service.description}")
            logger.info(f"   Key: {service.key}")
            if service.api_key:
                masked_key = service.api_key[:8] + "..." + service.api_key[-4:] if len(service.api_key) > 12 else "***"
                logger.info(f"   API Key: {masked_key}")
            print()

    def display_cloud_tab(self):
        """Display cloud services tab"""
        logger.info("☁️ Cloud Services - Cloud platforms and storage")
        logger.info("-" * 50)

        services = self.get_services_by_category("cloud")
        for i, (key, service) in enumerate(services, 1):
            status = "✅ ENABLED" if service.enabled else "❌ DISABLED"
            has_key = "🔑" if service.api_key else "🔓"
            priority = {"HIGH": "🔥", "MEDIUM": "⚡", "LOW": "📋"}[service.priority]

            logger.info(f"{i}. {priority} {service.name} - {status} {has_key}")
            logger.info(f"   {service.description}")
            logger.info(f"   Key: {service.key}")
            if service.api_key:
                masked_key = service.api_key[:8] + "..." + service.api_key[-4:] if len(service.api_key) > 12 else "***"
                logger.info(f"   API Key: {masked_key}")
            print()

    def display_settings_tab(self):
        """Display settings tab"""
        logger.info("⚙️ Settings - Configuration and management")
        logger.info("-" * 50)

        enabled_count = sum(1 for s in self.services.values() if s.enabled)
        total_count = len(self.services)

        logger.info(f"📊 Statistics:")
        logger.info(f"   Total APIs: {total_count}")
        logger.info(f"   Enabled: {enabled_count}")
        logger.info(f"   Disabled: {total_count - enabled_count}")
        print()

        logger.info(f"🔧 Actions:")
        logger.info(f"   1. Save configuration")
        logger.info(f"   2. Update .env file")
        logger.info(f"   3. Open all enabled APIs")
        logger.info(f"   4. Reset all to disabled")
        logger.info(f"   5. Enable all essential APIs")
        logger.info(f"   6. Export configuration")
        logger.info(f"   7. Import configuration")
        print()

        logger.info(f"📁 Files:")
        logger.info(f"   Config: {self.config_file}")
        logger.info(f"   .env: {self.env_file}")

    def toggle_service(self, category: str, index: int):
        """Toggle a service on/off"""
        services = self.get_services_by_category(category)
        if 0 <= index < len(services):
            key, service = services[index]
            service.enabled = not service.enabled
            logger.info(f"✅ {service.name} {'enabled' if service.enabled else 'disabled'}")
        else:
            logger.info("❌ Invalid service number")

    def open_service_registration(self, category: str, index: int):
        """Open registration page for a service"""
        services = self.get_services_by_category(category)
        if 0 <= index < len(services):
            key, service = services[index]
            logger.info(f"🌐 Opening {service.name} registration page...")
            webbrowser.open(service.url)
            logger.info(f"✅ Opened {service.url}")
        else:
            logger.info("❌ Invalid service number")

    def set_api_key(self, category: str, index: int):
        """Set API key for a service"""
        services = self.get_services_by_category(category)
        if 0 <= index < len(services):
            key, service = services[index]
            logger.info(f"Enter API key for {service.name}:")
            api_key = input("API Key: ").strip()
            if api_key:
                service.api_key = api_key
                service.enabled = True
                logger.info(f"✅ API key set for {service.name}")
            else:
                logger.info("❌ No API key entered")
        else:
            logger.info("❌ Invalid service number")

    def run(self):
        """Main interactive loop"""
        while True:
            self.display_tab()

            try:
                command = input("\nCommand: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                logger.info("\n👋 Goodbye!")
                break

            if command == "q":
                logger.info("👋 Goodbye!")
                break
            elif command == "s":
                self.save_config()
                self.update_env_file()
            elif command == "←" or command == "left":
                self.current_tab = (self.current_tab - 1) % len(self.tabs)
            elif command == "→" or command == "right":
                self.current_tab = (self.current_tab + 1) % len(self.tabs)
            elif command.isdigit():
                index = int(command) - 1
                if self.current_tab == 0:  # Essential
                    self.toggle_service("essential", index)
                elif self.current_tab == 1:  # AI/LLM
                    self.toggle_service("ai_llm", index)
                elif self.current_tab == 2:  # Image
                    self.toggle_service("image", index)
                elif self.current_tab == 3:  # Audio/Video
                    self.toggle_service("audio_video", index)
                elif self.current_tab == 4:  # Automation
                    self.toggle_service("automation", index)
                elif self.current_tab == 5:  # Data & Search
                    self.toggle_service("data_search", index)
                elif self.current_tab == 6:  # Cloud
                    self.toggle_service("cloud", index)
            elif command == "o":
                # Open registration for current service
                if self.current_tab < 7:  # Not settings tab
                    index = int(input("Service number: ")) - 1
                    if self.current_tab == 0:
                        self.open_service_registration("essential", index)
                    elif self.current_tab == 1:
                        self.open_service_registration("ai_llm", index)
                    elif self.current_tab == 2:
                        self.open_service_registration("image", index)
                    elif self.current_tab == 3:
                        self.open_service_registration("audio_video", index)
                    elif self.current_tab == 4:
                        self.open_service_registration("automation", index)
                    elif self.current_tab == 5:
                        self.open_service_registration("data_search", index)
                    elif self.current_tab == 6:
                        self.open_service_registration("cloud", index)
            elif command == "k":
                # Set API key for current service
                if self.current_tab < 7:  # Not settings tab
                    index = int(input("Service number: ")) - 1
                    if self.current_tab == 0:
                        self.set_api_key("essential", index)
                    elif self.current_tab == 1:
                        self.set_api_key("ai_llm", index)
                    elif self.current_tab == 2:
                        self.set_api_key("image", index)
                    elif self.current_tab == 3:
                        self.set_api_key("audio_video", index)
                    elif self.current_tab == 4:
                        self.set_api_key("automation", index)
                    elif self.current_tab == 5:
                        self.set_api_key("data_search", index)
                    elif self.current_tab == 6:
                        self.set_api_key("cloud", index)


def main():
    """main function."""

    config_manager = AIConfigManager()
    config_manager.run()


if __name__ == "__main__":
    main()
