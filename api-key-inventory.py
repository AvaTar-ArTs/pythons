#!/usr/bin/env python3
"""
🔑 API KEY INVENTORY SCANNER
=============================
Scan all .env files and create inventory without exposing actual keys

Features:
✨ Scan all .env files in ~/.env.d
✨ Identify which API keys are present/missing
✨ Check for common APIs (OpenAI, Claude, Perplexity, etc.)
✨ Never expose actual key values
✨ Generate CSV report with status
"""

import os
import re
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Tuple

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    END = "\033[0m"

class APIKeyInventory:
    """Inventory API keys without exposing values"""
    
    # Common API key patterns to check for
    COMMON_APIS = {
        # AI/LLM
        'OPENAI_API_KEY': 'OpenAI (GPT, DALL-E, Whisper)',
        'ANTHROPIC_API_KEY': 'Anthropic (Claude)',
        'PERPLEXITY_API_KEY': 'Perplexity AI',
        'GEMINI_API_KEY': 'Google Gemini',
        'GOOGLE_API_KEY': 'Google AI',
        'GROQ_API_KEY': 'Groq',
        'DEEPSEEK_API_KEY': 'DeepSeek',
        'MISTRAL_API_KEY': 'Mistral AI',
        'COHERE_API_KEY': 'Cohere',
        
        # Image/Video
        'STABILITY_API_KEY': 'Stability AI (Stable Diffusion)',
        'LEONARDO_API_KEY': 'Leonardo.ai',
        'MIDJOURNEY_API_KEY': 'Midjourney',
        'RUNWAY_API_KEY': 'Runway ML',
        'REPLICATE_API_TOKEN': 'Replicate',
        
        # Audio/Music
        'ELEVENLABS_API_KEY': 'ElevenLabs (TTS)',
        'SUNO_API_KEY': 'Suno AI',
        'MUBERT_API_KEY': 'Mubert',
        'PLAY_HT_API_KEY': 'Play.ht',
        
        # Social/Content
        'INSTAGRAM_USERNAME': 'Instagram',
        'INSTAGRAM_PASSWORD': 'Instagram',
        'YOUTUBE_API_KEY': 'YouTube Data API',
        'REDDIT_CLIENT_ID': 'Reddit API',
        'TIKTOK_API_KEY': 'TikTok',
        'TWITTER_API_KEY': 'Twitter/X',
        'TELEGRAM_BOT_TOKEN': 'Telegram Bot',
        
        # Cloud/Storage
        'AWS_ACCESS_KEY_ID': 'AWS',
        'AWS_SECRET_ACCESS_KEY': 'AWS',
        'GOOGLE_CLOUD_PROJECT': 'Google Cloud',
        'AZURE_API_KEY': 'Azure',
        'DROPBOX_ACCESS_TOKEN': 'Dropbox',
        'GITHUB_TOKEN': 'GitHub',
        
        # Other
        'HUGGINGFACE_API_KEY': 'HuggingFace',
        'PINECONE_API_KEY': 'Pinecone (Vector DB)',
        'SUPABASE_URL': 'Supabase',
        'AIRTABLE_API_KEY': 'Airtable',
        'NOTION_API_KEY': 'Notion',
    }
    
    def __init__(self):
        self.env_dir = Path.home() / ".env.d"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_file = self.env_dir / f"API_KEY_INVENTORY_{self.timestamp}.csv"
        
        self.found_keys = {}  # key_name -> {file, status, preview}
        self.missing_keys = []
    
    def print_header(self, text: str, color=Colors.CYAN):
        """Print fancy header"""
        print(f"\n{color}{Colors.BOLD}{'='*80}")
        print(f"{text}")
        print(f"{'='*80}{Colors.END}\n")
    
    def get_key_status(self, value: str) -> Tuple[str, str]:
        """Get key status and signifier without exposing actual key"""
        if not value:
            return "NOT_SET", "❌ Not configured"
        
        # Check for placeholder values
        placeholder_patterns = [
            'your_key_here', 'xxx', 'placeholder', 'replace_me',
            'changeme', 'enter_key', 'add_key_here', 'sk-xxx'
        ]
        
        value_lower = value.lower()
        if any(pattern in value_lower for pattern in placeholder_patterns):
            return "PLACEHOLDER", "⚠️ Needs real key"
        
        # Empty or very short
        if len(value) < 8:
            return "INVALID", "⚠️ Too short - check value"
        
        # Valid key
        return "CONFIGURED", f"✅ Active ({len(value)} chars)"
    
    def scan_env_file(self, env_file: Path):
        """Scan a single .env file"""
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse KEY=VALUE
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Remove quotes
                        value = value.strip('"').strip("'")
                        
                        # Determine status
                        status, preview = self.get_key_status(value)
                        
                        # Store (only if not already found or if this one is CONFIGURED)
                        if key not in self.found_keys or status == "CONFIGURED":
                            self.found_keys[key] = {
                                'file': env_file.name,
                                'status': status,
                                'preview': preview,
                                'service': self.COMMON_APIS.get(key, 'Custom/Other')
                            }
        
        except Exception as e:
            print(f"{Colors.RED}Error reading {env_file.name}: {e}{Colors.END}")
    
    def scan_all_env_files(self):
        """Scan all .env files"""
        self.print_header("🔍 SCANNING ALL .env FILES")
        
        env_files = list(self.env_dir.glob("*.env"))
        
        print(f"Found {len(env_files)} .env file(s)\n")
        
        for env_file in sorted(env_files):
            print(f"{Colors.CYAN}Scanning: {env_file.name}{Colors.END}")
            self.scan_env_file(env_file)
        
        print(f"\n{Colors.GREEN}✅ Scanned {len(env_files)} files{Colors.END}")
        print(f"{Colors.GREEN}✅ Found {len(self.found_keys)} unique API keys{Colors.END}\n")
    
    def check_missing_common_apis(self):
        """Check which common APIs are missing"""
        self.print_header("🔍 CHECKING FOR MISSING COMMON APIS")
        
        for key_name, service_name in self.COMMON_APIS.items():
            if key_name not in self.found_keys:
                self.missing_keys.append({
                    'key_name': key_name,
                    'service': service_name,
                    'status': 'MISSING'
                })
        
        print(f"{Colors.YELLOW}Found {len(self.missing_keys)} missing common API keys{Colors.END}\n")
        
        # Group by category
        missing_by_category = defaultdict(list)
        
        for missing in self.missing_keys:
            service = missing['service']
            
            if 'AI' in service or 'GPT' in service or 'Claude' in service:
                category = 'AI/LLM'
            elif 'Image' in service or 'Stable' in service or 'DALL-E' in service:
                category = 'Image Generation'
            elif 'Audio' in service or 'TTS' in service or 'Music' in service:
                category = 'Audio/Music'
            elif 'Instagram' in service or 'YouTube' in service or 'Reddit' in service:
                category = 'Social Media'
            elif 'AWS' in service or 'Google Cloud' in service or 'Azure' in service:
                category = 'Cloud/Storage'
            else:
                category = 'Other'
            
            missing_by_category[category].append(missing)
        
        print("Missing APIs by category:\n")
        for category, keys in sorted(missing_by_category.items()):
            print(f"{Colors.BOLD}{category}:{Colors.END}")
            for key in keys:
                print(f"  • {key['service']}")
            print()
    
    def generate_report(self):
        """Generate CSV report"""
        self.print_header("💾 GENERATING INVENTORY REPORT")
        
        with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Key_Name', 'Service', 'Status', 'Preview', 
                'Found_In_File', 'Category'
            ])
            
            # Add found keys
            for key_name, info in sorted(self.found_keys.items()):
                # Categorize
                service = info['service']
                
                if any(x in service for x in ['AI', 'GPT', 'Claude', 'Gemini', 'Groq']):
                    category = 'AI/LLM'
                elif any(x in service for x in ['Image', 'Stability', 'DALL-E', 'Leonardo']):
                    category = 'Image Generation'
                elif any(x in service for x in ['Audio', 'TTS', 'Music', 'Eleven', 'Suno']):
                    category = 'Audio/Music'
                elif any(x in service for x in ['Instagram', 'YouTube', 'Reddit', 'Twitter', 'TikTok']):
                    category = 'Social Media'
                elif any(x in service for x in ['AWS', 'Google Cloud', 'Azure', 'Storage']):
                    category = 'Cloud/Storage'
                else:
                    category = 'Other'
                
                writer.writerow([
                    key_name,
                    service,
                    info['status'],
                    info['preview'],
                    info['file'],
                    category
                ])
            
            # Add missing keys
            for missing in sorted(self.missing_keys, key=lambda x: x['service']):
                service = missing['service']
                
                if any(x in service for x in ['AI', 'GPT', 'Claude', 'Gemini', 'Groq']):
                    category = 'AI/LLM'
                elif any(x in service for x in ['Image', 'Stability', 'DALL-E', 'Leonardo']):
                    category = 'Image Generation'
                elif any(x in service for x in ['Audio', 'TTS', 'Music', 'Eleven', 'Suno']):
                    category = 'Audio/Music'
                elif any(x in service for x in ['Instagram', 'YouTube', 'Reddit', 'Twitter', 'TikTok']):
                    category = 'Social Media'
                elif any(x in service for x in ['AWS', 'Google Cloud', 'Azure', 'Storage']):
                    category = 'Cloud/Storage'
                else:
                    category = 'Other'
                
                writer.writerow([
                    missing['key_name'],
                    service,
                    'MISSING',
                    'Not configured',
                    'N/A',
                    category
                ])
        
        print(f"{Colors.GREEN}✅ Report saved: {self.output_file.name}{Colors.END}\n")
    
    def display_summary(self):
        """Display summary statistics"""
        self.print_header("📊 SUMMARY", Colors.GREEN)
        
        # Count by status
        status_counts = defaultdict(int)
        for info in self.found_keys.values():
            status_counts[info['status']] += 1
        status_counts['MISSING'] = len(self.missing_keys)
        
        print(f"{Colors.BOLD}API Key Status:{Colors.END}\n")
        print(f"  {Colors.GREEN}CONFIGURED:{Colors.END}   {status_counts['CONFIGURED']} keys (ready to use)")
        print(f"  {Colors.YELLOW}PLACEHOLDER:{Colors.END}  {status_counts['PLACEHOLDER']} keys (need real values)")
        print(f"  {Colors.YELLOW}NOT_SET:{Colors.END}      {status_counts['NOT_SET']} keys (empty)")
        print(f"  {Colors.YELLOW}INVALID:{Colors.END}      {status_counts['INVALID']} keys (check format)")
        print(f"  {Colors.RED}MISSING:{Colors.END}      {status_counts['MISSING']} keys (not in any .env)")
        print(f"\n  {Colors.BOLD}TOTAL:{Colors.END}        {len(self.found_keys) + len(self.missing_keys)} keys tracked\n")
        
        # Show important missing ones
        important_missing = [
            m for m in self.missing_keys 
            if any(x in m['service'] for x in ['Perplexity', 'Claude', 'Suno', 'Leonardo'])
        ]
        
        if important_missing:
            print(f"{Colors.BOLD}Notable Missing APIs:{Colors.END}\n")
            for missing in important_missing:
                print(f"  ⚠️  {missing['service']}")
            print()
        
        print(f"{Colors.CYAN}Full report: {self.output_file}{Colors.END}\n")
    
    def run(self):
        """Run inventory"""
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║                🔑 API KEY INVENTORY SCANNER 🔑                                ║")
        print("║                                                                               ║")
        print("║                  Secure Key Status Check (No Exposure)                       ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        print(f"Scanning: {self.env_dir}\n")
        
        # 1. Scan all env files
        self.scan_all_env_files()
        
        # 2. Check for missing common APIs
        self.check_missing_common_apis()
        
        # 3. Generate report
        self.generate_report()
        
        # 4. Display summary
        self.display_summary()


def main():
    inventory = APIKeyInventory()
    inventory.run()


if __name__ == "__main__":
    main()
