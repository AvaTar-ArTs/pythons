
import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
API Key Setup Assistant
Automatically opens registration pages for missing API keys in ~/.env
"""

import os
import re
import webbrowser
import time
from typing import Dict, List, Tuple

class APIKeySetup:
    def __init__(self):
        self.env_file = os.path.expanduser("~/.env.d/"  # Using organized system)
        self.api_services = {
            # LLMs / TEXT / RESEARCH
            "PERPLEXITY_API_KEY": {
                "name": "Perplexity AI",
                "url": "https://www.perplexity.ai/settings/api",
                "description": "AI-powered search and research"
            },
            "GEMINI_API_KEY": {
                "name": "Google Gemini",
                "url": "https://makersuite.google.com/app/apikey",
                "description": "Google's AI model"
            },
            "XAI_API_KEY": {
                "name": "xAI (Grok)",
                "url": "https://console.x.ai/",
                "description": "Elon Musk's AI company (Grok models)"
            },
            "HUGGINGFACE_API_KEY": {
                "name": "Hugging Face",
                "url": "https://huggingface.co/settings/tokens",
                "description": "Open source AI models and datasets"
            },
            
            # ART / VISION / IMAGE
            "LEONARDO_API_KEY": {
                "name": "Leonardo AI",
                "url": "https://leonardo.ai/",
                "description": "AI image generation"
            },
            "IMAGGA_API_KEY": {
                "name": "Imagga",
                "url": "https://imagga.com/profile/signup",
                "description": "Image analysis and tagging"
            },
            "STABILITY_API_KEY": {
                "name": "Stability AI",
                "url": "https://platform.stability.ai/account/keys",
                "description": "Stable Diffusion and other AI models"
            },
            "REPLICATE_API_TOKEN": {
                "name": "Replicate",
                "url": "https://replicate.com/account/api-tokens",
                "description": "Run AI models in the cloud"
            },
            "RUNWAY_API_KEY": {
                "name": "Runway ML",
                "url": "https://runwayml.com/",
                "description": "AI video and image generation"
            },
            "IDEOGRAM_API_KEY": {
                "name": "Ideogram",
                "url": "https://ideogram.ai/",
                "description": "AI image generation with text"
            },
            "KAIBER_API_KEY": {
                "name": "Kaiber",
                "url": "https://kaiber.ai/",
                "description": "AI music video generation"
            },
            "PIKA_API_KEY": {
                "name": "Pika Labs",
                "url": "https://pika.art/",
                "description": "AI video generation"
            },
            
            # AUDIO / MUSIC / VIDEO
            "SUNO_API_KEY": {
                "name": "Suno AI",
                "url": "https://suno.ai/",
                "description": "AI music generation"
            },
            "ELEVENLABS_API_KEY": {
                "name": "ElevenLabs",
                "url": "https://elevenlabs.io/app/settings/api-keys",
                "description": "AI voice synthesis"
            },
            "ASSEMBLYAI_API_KEY": {
                "name": "AssemblyAI",
                "url": "https://www.assemblyai.com/dashboard/signup",
                "description": "Speech-to-text API"
            },
            "DEEPGRAM_API_KEY": {
                "name": "Deepgram",
                "url": "https://console.deepgram.com/signup",
                "description": "Speech recognition and understanding"
            },
            "INVIDEO_API_KEY": {
                "name": "InVideo",
                "url": "https://invideo.io/",
                "description": "AI video creation"
            },
            "SORAI_API_KEY": {
                "name": "Sora AI",
                "url": "https://openai.com/sora",
                "description": "OpenAI's video generation"
            },
            
            # AUTOMATION / AGENTS / VECTOR DB
            "COHERE_API_KEY": {
                "name": "Cohere",
                "url": "https://dashboard.cohere.ai/",
                "description": "Language AI platform"
            },
            "FIREWORKS_API_KEY": {
                "name": "Fireworks AI",
                "url": "https://fireworks.ai/",
                "description": "Fast inference for open source models"
            },
            "PINECONE_API_KEY": {
                "name": "Pinecone",
                "url": "https://app.pinecone.io/",
                "description": "Vector database for AI"
            },
            "SUPABASE_KEY": {
                "name": "Supabase",
                "url": "https://supabase.com/dashboard",
                "description": "Open source Firebase alternative"
            },
            "QDRANT_API_KEY": {
                "name": "Qdrant",
                "url": "https://cloud.qdrant.io/",
                "description": "Vector database and similarity search"
            },
            "OPENROUTER_API_KEY": {
                "name": "OpenRouter",
                "url": "https://openrouter.ai/",
                "description": "Universal API for LLMs"
            },
            "LANGSMITH_API_KEY": {
                "name": "LangSmith",
                "url": "https://smith.langchain.com/",
                "description": "LangChain's debugging and monitoring"
            },
            
            # SEO / SCRAPING / ANALYTICS
            "SERPAPI_KEY": {
                "name": "SerpAPI",
                "url": "https://serpapi.com/",
                "description": "Google search results API"
            },
            "NEWSAPI_KEY": {
                "name": "NewsAPI",
                "url": "https://newsapi.org/register",
                "description": "News headlines API"
            },
            
            # CLOUD / INFRASTRUCTURE
            "AZURE_OPENAI_KEY": {
                "name": "Azure OpenAI",
                "url": "https://portal.azure.com/",
                "description": "Microsoft's OpenAI service"
            },
            
            # NOTIFICATIONS / AUTOMATION
            "TWILIO_ACCOUNT_SID": {
                "name": "Twilio",
                "url": "https://console.twilio.com/",
                "description": "Communication platform (SMS, voice, etc.)"
            },
            "ZAPIER_API_KEY": {
                "name": "Zapier",
                "url": "https://zapier.com/app/settings/integrations",
                "description": "Workflow automation"
            },
            "MAKE_API_KEY": {
                "name": "Make (Integromat)",
                "url": "https://www.make.com/",
                "description": "Visual automation platform"
            },
            
            # DOCUMENTS / KNOWLEDGE
            "NOTION_TOKEN": {
                "name": "Notion",
                "url": "https://www.notion.so/my-integrations",
                "description": "All-in-one workspace"
            },
            "SLITE_API_KEY": {
                "name": "Slite",
                "url": "https://slite.com/",
                "description": "Team knowledge base"
            },
            
            # VECTOR / MEMORY
            "CHROMADB_API_KEY": {
                "name": "Chroma",
                "url": "https://www.trychroma.com/",
                "description": "Open source vector database"
            },
            "ZEP_API_KEY": {
                "name": "Zep",
                "url": "https://www.getzep.com/",
                "description": "Long-term memory for AI applications"
            },
            
            # OTHER
            "MOONVALLEY_API_KEY": {
                "name": "Moonvalley",
                "url": "https://moonvalley.ai/",
                "description": "AI video generation"
            },
            "ARCGIS_API_KEY": {
                "name": "ArcGIS",
                "url": "https://developers.arcgis.com/",
                "description": "Mapping and location services"
            },
            "SUPERNORMAL_API_KEY": {
                "name": "Supernormal",
                "url": "https://supernormal.com/",
                "description": "AI meeting notes"
            },
            "DESCRIPT_API_KEY": {
                "name": "Descript",
                "url": "https://www.descript.com/",
                "description": "AI video and audio editing"
            },
            "SONIX_API_KEY": {
                "name": "Sonix",
                "url": "https://sonix.ai/",
                "description": "AI transcription service"
            },
            "REVAI_API_KEY": {
                "name": "Rev.ai",
                "url": "https://www.rev.ai/",
                "description": "Speech-to-text API"
            },
            "SPEECHMATICS_API_KEY": {
                "name": "Speechmatics",
                "url": "https://www.speechmatics.com/",
                "description": "Speech recognition API"
            }
        }
    
    def load_env_file(self) -> List[str]:
        """Load the .env file and return lines"""
        if not os.path.exists(self.env_file):
            logger.info(f"❌ Error: {self.env_file} not found")
            return []
        
        with open(self.env_file, 'r') as f:
            return f.readlines()
    
    def find_missing_keys(self) -> List[Tuple[str, Dict]]:
        """Find API keys that are missing or have placeholder values"""
        lines = self.load_env_file()
        missing_keys = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if '=' in line:
                key, value = line.split('=', 1)
                value = value.strip()
                
                # Check if key is missing or has placeholder value
                if (not value or 
                    value in ['your_key_here', 'your_xai_api_key_here', 'your_secret_here', 'your_token_here'] or
                    value.startswith('your_') or
                    value == ''):
                    
                    if key in self.api_services:
                        missing_keys.append((key, self.api_services[key]))
        
        return missing_keys
    
    def open_registration_page(self, key: str, service_info: Dict) -> None:
        """Open the registration page for a service"""
        logger.info(f"\n🌐 Opening {service_info['name']} registration page...")
        logger.info(f"   📝 {service_info['description']}")
        logger.info(f"   🔗 {service_info['url']}")
        
        try:
            webbrowser.open(service_info['url'])
            logger.info(f"   ✅ Page opened in browser")
        except Exception as e:
            logger.info(f"   ❌ Error opening page: {e}")
    
    def update_env_file(self, key: str, new_value: str) -> bool:
        """Update a specific API key in the .env file"""
        lines = self.load_env_file()
        updated = False
        
        for i, line in enumerate(lines):
            if line.strip().startswith(f"{key}="):
                lines[i] = f"{key}={new_value}\n"
                updated = True
                break
        
        if updated:
            with open(self.env_file, 'w') as f:
                f.writelines(lines)
            return True
        return False
    
    def interactive_setup(self) -> None:
        """Interactive setup process"""
        missing_keys = self.find_missing_keys()
        
        if not missing_keys:
            logger.info("🎉 All API keys are configured!")
            return
        
        logger.info(f"🔍 Found {len(missing_keys)} missing API keys:")
        logger.info("=" * 50)
        
        for i, (key, service_info) in enumerate(missing_keys, 1):
            logger.info(f"\n{i}. {key}")
            logger.info(f"   Service: {service_info['name']}")
            logger.info(f"   Description: {service_info['description']}")
        
        logger.info(f"\n🚀 Starting interactive setup...")
        logger.info("=" * 50)
        
        for i, (key, service_info) in enumerate(missing_keys, 1):
            logger.info(f"\n📍 Step {i}/{len(missing_keys)}: {service_info['name']}")
            logger.info(f"   Key: {key}")
            logger.info(f"   Description: {service_info['description']}")
            
            # Open registration page
            self.open_registration_page(key, service_info)
            
            # Wait for user to get the key
            logger.info(f"\n⏳ Please get your API key from the opened page...")
            logger.info("   (The page should have opened in your browser)")
            
            while True:
                response = input(f"\n💡 Enter your {service_info['name']} API key (or 'skip' to skip, 'quit' to exit): ").strip()
                
                if response.lower() == 'quit':
                    logger.info("👋 Setup cancelled. You can run this script again later.")
                    return
                elif response.lower() == 'skip':
                    logger.info(f"⏭️  Skipped {service_info['name']}")
                    break
                elif response:
                    # Update the .env file
                    if self.update_env_file(key, response):
                        logger.info(f"✅ Updated {key} in ~/.env")
                        break
                    else:
                        logger.info(f"❌ Error updating {key}. Please try again.")
                else:
                    logger.info("❌ Please enter a valid API key or 'skip'")
            
            # Ask if user wants to continue
            if i < len(missing_keys):
                continue_setup = input(f"\n🔄 Continue to next API key? (y/n): ").strip().lower()
                if continue_setup not in ['y', 'yes', '']:
                    logger.info("👋 Setup paused. You can run this script again later.")
                    return
        
        logger.info(f"\n🎉 Setup complete! All API keys have been processed.")
        logger.info("💡 You can run this script again anytime to set up additional keys.")
    
    def list_missing_keys(self) -> None:
        """List all missing API keys without interactive setup"""
        missing_keys = self.find_missing_keys()
        
        if not missing_keys:
            logger.info("🎉 All API keys are configured!")
            return
        
        logger.info(f"🔍 Found {len(missing_keys)} missing API keys:")
        logger.info("=" * 60)
        
        for i, (key, service_info) in enumerate(missing_keys, 1):
            logger.info(f"\n{i}. {key}")
            logger.info(f"   Service: {service_info['name']}")
            logger.info(f"   Description: {service_info['description']}")
            logger.info(f"   URL: {service_info['url']}")
        
        logger.info(f"\n💡 Run with --interactive to set up these keys automatically:")
        logger.info(f"   python3 ~/api-key-setup.py --interactive")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='API Key Setup Assistant')
    parser.add_argument('--interactive', '-i', action='store_true', 
                       help='Start interactive setup process')
    parser.add_argument('--list', '-l', action='store_true', 
                       help='List missing API keys')
    
    args = parser.parse_args()
    
    setup = APIKeySetup()
    
    if args.list:
        setup.list_missing_keys()
    elif args.interactive:
        setup.interactive_setup()
    else:
        logger.info("🔧 API Key Setup Assistant")
        logger.info("=" * 30)
        logger.info("Usage:")
        logger.info("  python3 ~/api-key-setup.py --list        # List missing keys")
        logger.info("  python3 ~/api-key-setup.py --interactive # Interactive setup")
        logger.info("\n💡 This will help you set up all missing API keys in your ~/.env file")

if __name__ == "__main__":
    main()