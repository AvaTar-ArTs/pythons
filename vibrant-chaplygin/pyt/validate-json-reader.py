import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_33 = 33

#!/usr/bin/env python3
"""
API Key Manager - Interactive Script for Managing Environment Variables
=====================================================================

This script helps you:
1. Scan all .env files in ~/.env.d/ for missing API keys
2. Open browser links to create missing API keys
3. Guide you through filling in the keys
4. Validate and save the keys securely

Usage: python3 api_key_manager.py [options]
"""

import os
import re
import webbrowser
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import subprocess
import sys


# Color codes for terminal output
class Colors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    WHITE = "\033[1;37m"
    NC = "\033[0m"  # No Color


# API service information with creation links
API_SERVICES = {
    # LLM APIs
    "OPENAI_API_KEY": {
        "name": "OpenAI",
        "url": "https://platform.openai.com/api-keys",
        "description": "GPT models, embeddings, and more",
        "pattern": r"^sk-proj-",
        "required": True,
    },
    "ANTHROPIC_API_KEY": {
        "name": "Anthropic Claude",
        "url": "https://console.anthropic.com/",
        "description": "Claude AI models",
        "pattern": r"^sk-ant-",
        "required": True,
    },
    "GROQ_API_KEY": {
        "name": "Groq",
        "url": "https://console.groq.com/keys",
        "description": "Fast LLM inference",
        "pattern": r"^gsk_",
        "required": True,
    },
    "GROK_API_KEY": {
        "name": "Grok (xAI)",
        "url": "https://console.x.ai/",
        "description": "xAI Grok models",
        "pattern": r"^xai-",
        "required": False,
    },
    "XAI_API_KEY": {
        "name": "xAI",
        "url": "https://console.x.ai/",
        "description": "xAI models and tools",
        "pattern": r"^xai-",
        "required": False,
    },
    "DEEPSEEK_API_KEY": {
        "name": "DeepSeek",
        "url": "https://platform.deepseek.com/api_keys",
        "description": "DeepSeek AI models",
        "pattern": r"^sk-",
        "required": False,
    },
    "PERPLEXITY_API_KEY": {
        "name": "Perplexity",
        "url": "https://www.perplexity.ai/settings/api",
        "description": "Perplexity AI search",
        "pattern": r"^pplx-",
        "required": False,
    },
    "GEMINI_API_KEY": {
        "name": "Google Gemini",
        "url": "https://makersuite.google.com/app/apikey",
        "description": "Google Gemini models",
        "pattern": r"^AIza",
        "required": False,
    },
    "HUGGINGFACE_API_KEY": {
        "name": "Hugging Face",
        "url": "https://huggingface.co/settings/tokens",
        "description": "Hugging Face models and datasets",
        "pattern": r"^hf_",
        "required": False,
    },
    # Art & Vision APIs
    "STABILITY_API_KEY": {
        "name": "Stability AI",
        "url": "https://platform.stability.ai/account/keys",
        "description": "Stable Diffusion and image generation",
        "pattern": r"^sk-",
        "required": False,
    },
    "REPLICATE_API_TOKEN": {
        "name": "Replicate",
        "url": "https://replicate.com/account/api-tokens",
        "description": "AI model hosting and inference",
        "pattern": r"^r8_",
        "required": False,
    },
    "RUNWAY_API_KEY": {
        "name": "Runway ML",
        "url": "https://app.runwayml.com/account/settings",
        "description": "AI video and image generation",
        "pattern": r"^[a-zA-Z0-9]{32,}",
        "required": False,
    },
    "LEONARDO_API_KEY": {
        "name": "Leonardo AI",
        "url": "https://leonardo.ai/",
        "description": "AI art generation",
        "pattern": r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}",
        "required": False,
    },
    "IDEOGRAM_API_KEY": {
        "name": "Ideogram",
        "url": "https://ideogram.ai/",
        "description": "AI image generation with text",
        "pattern": r"^[a-zA-Z0-9]{32,}",
        "required": False,
    },
    "KAIBER_API_KEY": {
        "name": "Kaiber",
        "url": "https://kaiber.ai/",
        "description": "AI music video generation",
        "pattern": r"^[a-zA-Z0-9]{32,}",
        "required": False,
    },
    "PIKA_API_KEY": {
        "name": "Pika Labs",
        "url": "https://pika.art/",
        "description": "AI video generation",
        "pattern": r"^[a-zA-Z0-9]{32,}",
        "required": False,
    },
    # Audio & Music APIs
    "SUNO_API_KEY": {
        "name": "Suno AI",
        "url": "https://suno.ai/",
        "description": "AI music generation",
        "pattern": r"^[a-zA-Z0-9]{32,}",
        "required": False,
    },
    "ELEVENLABS_API_KEY": {
        "name": "ElevenLabs",
        "url": "https://elevenlabs.io/app/settings/api-keys",
        "description": "AI voice synthesis",
        "pattern": r"^[a-f0-9]{32,}",
        "required": False,
    },
    "ASSEMBLYAI_API_KEY": {
        "name": "AssemblyAI",
        "url": "https://www.assemblyai.com/dashboard/signup",
        "description": "Speech-to-text transcription",
        "pattern": r"^[a-f0-9]{32,}",
        "required": False,
    },
    "DEEPGRAM_API_KEY": {
        "name": "Deepgram",
        "url": "https://console.deepgram.com/",
        "description": "Speech-to-text and audio intelligence",
        "pattern": r"^[a-f0-9]{32,}",
        "required": False,
    },
    "INVIDEO_API_KEY": {
        "name": "InVideo",
        "url": "https://invideo.io/",
        "description": "AI video creation",
        "pattern": r"^[a-zA-Z0-9]{32,}",
        "required": False,
    },
    "SORAI_API_KEY": {
        "name": "Sora AI",
        "url": "https://openai.com/sora",
        "description": "AI video generation (OpenAI)",
        "pattern": r"^sk-",
        "required": False,
    },
    # Automation & Agents
    "COHERE_API_KEY": {
        "name": "Cohere",
        "url": "https://dashboard.cohere.ai/api-keys",
        "description": "Language AI and embeddings",
        "pattern": r"^[a-zA-Z0-9]{32,}",
        "required": False,
    },
    "FIREWORKS_API_KEY": {
        "name": "Fireworks AI",
        "url": "https://fireworks.ai/",
        "description": "Open source LLM inference",
        "pattern": r"^[a-zA-Z0-9]{32,}",
        "required": False,
    },
    "PINECONE_API_KEY": {
        "name": "Pinecone",
        "url": "https://app.pinecone.io/organizations/-/api-keys",
        "description": "Vector database for embeddings",
        "pattern": r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}",
        "required": False,
    },
    "SUPABASE_KEY": {
        "name": "Supabase",
        "url": "https://supabase.com/dashboard/project/_/settings/api",
        "description": "Backend-as-a-Service and database",
        "pattern": r"^[a-zA-Z0-9]{32,}",
        "required": False,
    },
    "QDRANT_API_KEY": {
        "name": "Qdrant",
        "url": "https://cloud.qdrant.io/",
        "description": "Vector database and search",
        "pattern": r"^[a-zA-Z0-9]{32,}",
        "required": False,
    },
    "OPENROUTER_API_KEY": {
        "name": "OpenRouter",
        "url": "https://openrouter.ai/keys",
        "description": "Unified API for multiple LLMs",
        "pattern": r"^sk-or-",
        "required": False,
    },
    "LANGSMITH_API_KEY": {
        "name": "LangSmith",
        "url": "https://smith.langchain.com/",
        "description": "LangChain observability platform",
        "pattern": r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}",
        "required": False,
    },
    # SEO & Analytics
    "SERPAPI_KEY": {
        "name": "SERP API",
        "url": "https://serpapi.com/manage-api-key",
        "description": "Google search results API",
        "pattern": r"^[a-f0-9]{64,}",
        "required": False,
    },
    "NEWSAPI_KEY": {
        "name": "News API",
        "url": "https://newsapi.org/register",
        "description": "News headlines and articles",
        "pattern": r"^[a-f0-9]{32,}",
        "required": False,
    },
    # Notifications
    "TWILIO_ACCOUNT_SID": {
        "name": "Twilio Account SID",
        "url": "https://console.twilio.com/us1/develop/api-keys",
        "description": "SMS and voice communications",
        "pattern": r"^AC[a-f0-9]{32}",
        "required": False,
    },
    "TWILIO_AUTH_TOKEN": {
        "name": "Twilio Auth Token",
        "url": "https://console.twilio.com/us1/develop/api-keys",
        "description": "SMS and voice communications",
        "pattern": r"^[a-f0-9]{32}",
        "required": False,
    },
    "ZAPIER_API_KEY": {
        "name": "Zapier",
        "url": "https://zapier.com/app/settings/integrations",
        "description": "Workflow automation",
        "pattern": r"^[a-zA-Z0-9]{32,}",
        "required": False,
    },
    "MAKE_API_KEY": {
        "name": "Make (Integromat)",
        "url": "https://www.make.com/en/help/api-keys",
        "description": "Workflow automation platform",
        "pattern": r"^[a-zA-Z0-9]{32,}",
        "required": False,
    },
    # Other Tools
    "MOONVALLEY_API_KEY": {
        "name": "Moonvalley",
        "url": "https://moonvalley.ai/",
        "description": "AI video generation",
        "pattern": r"^[a-zA-Z0-9]{32,}",
        "required": False,
    },
    "ARCGIS_API_KEY": {
        "name": "ArcGIS",
        "url": "https://developers.arcgis.com/",
        "description": "Mapping and geospatial services",
        "pattern": r"^[a-zA-Z0-9]{32,}",
        "required": False,
    },
    "SUPERNORMAL_API_KEY": {
        "name": "Supernormal",
        "url": "https://supernormal.com/",
        "description": "AI meeting transcription",
        "pattern": r"^[a-zA-Z0-9]{32,}",
        "required": False,
    },
    "DESCRIPT_API_KEY": {
        "name": "Descript",
        "url": "https://www.descript.com/",
        "description": "Audio/video editing and transcription",
        "pattern": r"^[a-zA-Z0-9]{32,}",
        "required": False,
    },
    "SONIX_API_KEY": {
        "name": "Sonix",
        "url": "https://sonix.ai/",
        "description": "AI transcription service",
        "pattern": r"^[a-zA-Z0-9]{32,}",
        "required": False,
    },
    "REVAI_API_KEY": {
        "name": "Rev.ai",
        "url": "https://www.rev.ai/",
        "description": "Speech-to-text API",
        "pattern": r"^[a-zA-Z0-9]{32,}",
        "required": False,
    },
    "SPEECHMATICS_API_KEY": {
        "name": "Speechmatics",
        "url": "https://www.speechmatics.com/",
        "description": "Speech-to-text and audio intelligence",
        "pattern": r"^[a-zA-Z0-9]{32,}",
        "required": False,
    },
    # Cloud Infrastructure
    "AWS_ACCESS_KEY_ID": {
        "name": "AWS Access Key ID",
        "url": "https://console.aws.amazon.com/iam/home#/security_credentials",
        "description": "Amazon Web Services",
        "pattern": r"^AKIA[0-9A-Z]{16}",
        "required": False,
    },
    "AWS_SECRET_ACCESS_KEY": {
        "name": "AWS Secret Access Key",
        "url": "https://console.aws.amazon.com/iam/home#/security_credentials",
        "description": "Amazon Web Services",
        "pattern": r"^[a-zA-Z0-9+/]{40}",
        "required": False,
    },
    "AZURE_OPENAI_KEY": {
        "name": "Azure OpenAI",
        "url": "https://portal.azure.com/",
        "description": "Microsoft Azure OpenAI Service",
        "pattern": r"^[a-f0-9]{32,}",
        "required": False,
    },
}


class APIKeyManager:
    def __init__(self, env_dir: str = "~/.env.d"):
        self.env_dir = Path(env_dir).expanduser()
        self.missing_keys = []
        self.invalid_keys = []
        self.valid_keys = []

    def print_header(self, title: str):
        """Print a formatted header"""
        logger.info(f"\n{Colors.CYAN}{'='*60}{Colors.NC}")
        logger.info(f"{Colors.WHITE}{title:^60}{Colors.NC}")
        logger.info(f"{Colors.CYAN}{'='*60}{Colors.NC}\n")

    def print_success(self, message: str):
        """Print success message"""
        logger.info(f"{Colors.GREEN}✅ {message}{Colors.NC}")

    def print_warning(self, message: str):
        """Print warning message"""
        logger.info(f"{Colors.YELLOW}⚠️  {message}{Colors.NC}")

    def print_error(self, message: str):
        """Print error message"""
        logger.info(f"{Colors.RED}❌ {message}{Colors.NC}")

    def print_info(self, message: str):
        """Print info message"""
        logger.info(f"{Colors.BLUE}ℹ️  {message}{Colors.NC}")

    def scan_env_files(self) -> Dict[str, List[Tuple[str, str, str]]]:
        """Scan all .env files and categorize API keys"""
        results = {}

        if not self.env_dir.exists():
            self.print_error(f"Environment directory not found: {self.env_dir}")
            return results

        for env_file in self.env_dir.glob("*.env"):
            if env_file.name == "loader.sh":
                continue

            category = env_file.stem.replace("-", " ").title()
            results[category] = []

            try:
                with open(env_file, "r") as f:
                    for line_num, line in enumerate(f, 1):
                        line = line.strip()

                        # Skip comments and empty lines
                        if not line or line.startswith("#"):
                            continue

                        # Extract API key variable
                        if "=" in line:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip()

                            # Remove inline comments
                            if "#" in value:
                                value = value.split("#")[0].strip()

                            # Check if it's an API key
                            if (
                                key.endswith("_API_KEY")
                                or key.endswith("_TOKEN")
                                or key.endswith("_SID")
                                or key.endswith("_SECRET")
                            ):
                                results[category].append((key, value, f"{env_file.name}:{line_num}"))

            except Exception as e:
                self.print_error(f"Error reading {env_file}: {e}")

        return results

    def validate_api_key(self, key: str, value: str) -> bool:
        """Validate an API key format"""
        if not value or value in ["your_key_here", "your_secret_here", ""]:
            return False

        if key in API_SERVICES:
            pattern = API_SERVICES[key]["pattern"]
            return bool(re.match(pattern, value))

        return True  # Unknown format, assume valid

    def categorize_keys(self, all_keys: Dict[str, List[Tuple[str, str, str]]]):
        """Categorize keys into missing, invalid, and valid"""
        for category, keys in all_keys.items():
            for key, value, location in keys:
                if not value or value in ["your_key_here", "your_secret_here", ""]:
                    self.missing_keys.append((key, category, location))
                elif not self.validate_api_key(key, value):
                    self.invalid_keys.append((key, value, category, location))
                else:
                    self.valid_keys.append((key, category, location))

    def display_summary(self):
        """Display summary of API key status"""
        self.print_header("API Key Status Summary")

        logger.info(f"{Colors.GREEN}Valid Keys: {len(self.valid_keys)}{Colors.NC}")
        logger.info(f"{Colors.YELLOW}Missing Keys: {len(self.missing_keys)}{Colors.NC}")
        logger.info(f"{Colors.RED}Invalid Keys: {len(self.invalid_keys)}{Colors.NC}")

        if self.valid_keys:
            logger.info(f"\n{Colors.GREEN}✅ Working API Keys:{Colors.NC}")
            for key, category, location in self.valid_keys:
                service_name = API_SERVICES.get(key, {}).get("name", key)
                logger.info(f"  • {service_name} ({category}) - {location}")

        if self.missing_keys:
            logger.info(f"\n{Colors.YELLOW}⚠️  Missing API Keys:{Colors.NC}")
            for key, category, location in self.missing_keys:
                service_name = API_SERVICES.get(key, {}).get("name", key)
                logger.info(f"  • {service_name} ({category}) - {location}")

        if self.invalid_keys:
            logger.info(f"\n{Colors.RED}❌ Invalid API Keys:{Colors.NC}")
            for key, value, category, location in self.invalid_keys:
                service_name = API_SERVICES.get(key, {}).get("name", key)
                logger.info(f"  • {service_name} ({category}) - {location}")
                logger.info(f"    Current value: {value[:20]}{'...' if len(value) > 20 else ''}")

    def interactive_setup(self):
        """Interactive setup for missing API keys"""
        if not self.missing_keys:
            self.print_success("No missing API keys found!")
            return

        self.print_header("Interactive API Key Setup")
        logger.info("I'll help you set up missing API keys one by one.")
        logger.info("For each key, I'll open the creation page and wait for you to fill it in.\n")

        for i, (key, category, location) in enumerate(self.missing_keys, 1):
            service_info = API_SERVICES.get(key, {})
            service_name = service_info.get("name", key)
            service_url = service_info.get("url", "")
            description = service_info.get("description", "")
            is_required = service_info.get("required", False)

            logger.info(f"{Colors.CYAN}[{i}/{len(self.missing_keys)}] Setting up {service_name}{Colors.NC}")
            logger.info(f"Description: {description}")
            logger.info(f"Category: {category}")
            logger.info(f"Location: {location}")

            if is_required:
                logger.info(f"{Colors.YELLOW}This is a REQUIRED key for core functionality{Colors.NC}")

            if service_url:
                logger.info(f"\n{Colors.BLUE}Opening {service_url} in your browser...{Colors.NC}")
                try:
                    webbrowser.open(service_url)
                except Exception as e:
                    self.print_error(f"Could not open browser: {e}")
                    logger.info(f"Please manually visit: {service_url}")
            else:
                logger.info(
                    f"{Colors.YELLOW}No direct URL available. Please search for '{service_name} API key' in your browser.{Colors.NC}"
                )

            # Get user input
            while True:
                api_key = input(
                    f"\n{Colors.WHITE}Enter your {service_name} API key (or 'skip' to skip, 'quit' to exit): {Colors.NC}"
                ).strip()

                if api_key.lower() == "quit":
                    logger.info(f"\n{Colors.YELLOW}Setup interrupted by user.{Colors.NC}")
                    return
                elif api_key.lower() == "skip":
                    logger.info(f"{Colors.YELLOW}Skipped {service_name}{Colors.NC}")
                    break
                elif not api_key:
                    logger.info(f"{Colors.RED}Please enter a valid API key or 'skip'{Colors.NC}")
                    continue

                # Validate the key
                if self.validate_api_key(key, api_key):
                    # Update the environment file
                    if self.update_env_file(key, api_key, location):
                        self.print_success(f"Successfully saved {service_name} API key!")
                        break
                    else:
                        logger.info(f"{Colors.RED}Failed to save API key. Please try again.{Colors.NC}")
                else:
                    logger.info(f"{Colors.RED}Invalid API key format. Please check and try again.{Colors.NC}")
                    if key in API_SERVICES:
                        pattern = API_SERVICES[key]["pattern"]
                        logger.info(f"Expected format: {pattern}")

            logger.info(f"{Colors.CYAN}{'─'*60}{Colors.NC}")

    def update_env_file(self, key: str, value: str, location: str) -> bool:
        """Update an API key in the appropriate .env file"""
        try:
            file_path, line_num = location.split(":")
            file_path = self.env_dir / file_path
            line_num = int(line_num) - 1  # Convert to 0-based index

            # Read the file
            with open(file_path, "r") as f:
                lines = f.readlines()

            # Update the specific line
            if 0 <= line_num < len(lines):
                line = lines[line_num]
                if "=" in line:
                    # Preserve comments
                    if "#" in line:
                        comment_part = line[line.find("#") :]
                        lines[line_num] = f"{key}={value} {comment_part}"
                    else:
                        lines[line_num] = f"{key}={value}\n"

                    # Write back to file
                    with open(file_path, "w") as f:
                        f.writelines(lines)

                    # Set secure permissions
                    os.chmod(file_path, 0o600)
                    return True

            return False

        except Exception as e:
            self.print_error(f"Error updating file: {e}")
            return False

    def fix_invalid_keys(self):
        """Interactive fix for invalid API keys"""
        if not self.invalid_keys:
            self.print_success("No invalid API keys found!")
            return

        self.print_header("Fix Invalid API Keys")
        logger.info("I found some API keys that appear to be invalid or placeholder values.")
        logger.info("Let's fix them one by one.\n")

        for i, (key, value, category, location) in enumerate(self.invalid_keys, 1):
            service_info = API_SERVICES.get(key, {})
            service_name = service_info.get("name", key)
            service_url = service_info.get("url", "")
            description = service_info.get("description", "")

            logger.info(f"{Colors.CYAN}[{i}/{len(self.invalid_keys)}] Fixing {service_name}{Colors.NC}")
            logger.info(f"Description: {description}")
            logger.info(f"Category: {category}")
            logger.info(f"Current value: {value[:30]}{'...' if len(value) > 30 else ''}")

            if service_url:
                logger.info(f"\n{Colors.BLUE}Opening {service_url} in your browser...{Colors.NC}")
                try:
                    webbrowser.open(service_url)
                except Exception as e:
                    self.print_error(f"Could not open browser: {e}")
                    logger.info(f"Please manually visit: {service_url}")

            while True:
                new_key = input(
                    f"\n{Colors.WHITE}Enter the correct {service_name} API key (or 'skip' to skip): {Colors.NC}"
                ).strip()

                if new_key.lower() == "skip":
                    logger.info(f"{Colors.YELLOW}Skipped {service_name}{Colors.NC}")
                    break
                elif not new_key:
                    logger.info(f"{Colors.RED}Please enter a valid API key or 'skip'{Colors.NC}")
                    continue

                if self.validate_api_key(key, new_key):
                    if self.update_env_file(key, new_key, location):
                        self.print_success(f"Successfully updated {service_name} API key!")
                        break
                    else:
                        logger.info(f"{Colors.RED}Failed to update API key. Please try again.{Colors.NC}")
                else:
                    logger.info(f"{Colors.RED}Invalid API key format. Please check and try again.{Colors.NC}")

            logger.info(f"{Colors.CYAN}{'─'*60}{Colors.NC}")

    def generate_report(self):
        """Generate a detailed report of all API keys"""
        report_file = self.env_dir.parent / "api_keys_report.md"

        with open(report_file, "w") as f:
            f.write("# API Keys Status Report\n\n")
            f.write(f"Generated on: {subprocess.check_output(['date']).decode().strip()}\n\n")

            f.write("## Summary\n\n")
            f.write(f"- **Valid Keys**: {len(self.valid_keys)}\n")
            f.write(f"- **Missing Keys**: {len(self.missing_keys)}\n")
            f.write(f"- **Invalid Keys**: {len(self.invalid_keys)}\n\n")

            if self.valid_keys:
                f.write("## ✅ Working API Keys\n\n")
                for key, category, location in self.valid_keys:
                    service_name = API_SERVICES.get(key, {}).get("name", key)
                    f.write(f"- **{service_name}** ({category}) - `{location}`\n")
                f.write(Path("\n"))

            if self.missing_keys:
                f.write("## ⚠️ Missing API Keys\n\n")
                for key, category, location in self.missing_keys:
                    service_info = API_SERVICES.get(key, {})
                    service_name = service_info.get("name", key)
                    service_url = service_info.get("url", "")
                    is_required = service_info.get("required", False)

                    f.write(f"- **{service_name}** ({category}) - `{location}`")
                    if is_required:
                        f.write(" **[REQUIRED]**")
                    f.write(f"\n  - URL: {service_url}\n")
                f.write(Path("\n"))

            if self.invalid_keys:
                f.write("## ❌ Invalid API Keys\n\n")
                for key, value, category, location in self.invalid_keys:
                    service_name = API_SERVICES.get(key, {}).get("name", key)
                    f.write(f"- **{service_name}** ({category}) - `{location}`\n")
                    f.write(f"  - Current value: `{value[:50]}{'...' if len(value) > 50 else ''}`\n")
                f.write(Path("\n"))

        self.print_success(f"Detailed report saved to: {report_file}")

    def run(self, interactive: bool = True, fix_invalid: bool = True, generate_report: bool = True):
        """Main execution method"""
        self.print_header("API Key Manager")

        # Scan environment files
        self.print_info("Scanning environment files...")
        all_keys = self.scan_env_files()

        if not all_keys:
            self.print_error("No environment files found or accessible.")
            return

        # Categorize keys
        self.categorize_keys(all_keys)

        # Display summary
        self.display_summary()

        # Interactive setup for missing keys
        if interactive and self.missing_keys:
            self.interactive_setup()

        # Fix invalid keys
        if fix_invalid and self.invalid_keys:
            self.fix_invalid_keys()

        # Generate report
        if generate_report:
            self.generate_report()

        self.print_header("Setup Complete!")
        self.print_success("API key management completed successfully!")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="API Key Manager - Interactive script for managing environment variables"
    )
    parser.add_argument("--no-interactive", action="store_true", help="Skip interactive setup")
    parser.add_argument("--no-fix", action="store_true", help="Skip fixing invalid keys")
    parser.add_argument("--no-report", action="store_true", help="Skip generating report")
    parser.add_argument("--env-dir", default="~/.env.d", help="Environment directory path")

    args = parser.parse_args()

    manager = APIKeyManager(args.env_dir)
    manager.run(interactive=not args.no_interactive, fix_invalid=not args.no_fix, generate_report=not args.no_report)


if __name__ == "__main__":
    main()
