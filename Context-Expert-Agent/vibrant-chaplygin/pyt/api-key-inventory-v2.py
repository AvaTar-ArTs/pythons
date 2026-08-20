#!/usr/bin/env python3
"""
🔑 API KEY INVENTORY V2
========================
Show ACTUAL keys you have, then check for truly missing ones

Features:
✨ Show all keys found in .env files
✨ Group by category/service
✨ Only flag truly missing important keys
✨ Never expose actual values
"""

import os
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

class APIKeyInventoryV2:
    """Show what you actually have"""
    
    def __init__(self):
        self.env_dir = Path.home() / ".env.d"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_file = self.env_dir / f"API_KEY_INVENTORY_COMPLETE_{self.timestamp}.csv"
        
        self.all_keys = {}  # key_name -> info
    
    def print_header(self, text: str, color=Colors.CYAN):
        """Print fancy header"""
        print(f"\n{color}{Colors.BOLD}{'='*80}")
        print(f"{text}")
        print(f"{'='*80}{Colors.END}\n")
    
    def get_key_status(self, value: str) -> Tuple[str, str]:
        """Get status signifier without exposing key"""
        if not value:
            return "NOT_SET", "❌ Empty"
        
        # Placeholder values
        placeholder_patterns = ['your_key_here', 'xxx', 'placeholder', 'replace', 
                               'changeme', 'enter_key', 'sk-xxx', 'add_key']
        
        value_lower = value.lower()
        if any(p in value_lower for p in placeholder_patterns):
            return "PLACEHOLDER", "⚠️ Placeholder"
        
        # Very short (likely config, not API key)
        if len(value) < 8:
            return "CONFIG", f"⚙️ Config ({len(value)} chars)"
        
        # Valid API key
        return "ACTIVE", f"✅ Active ({len(value)} chars)"
    
    def categorize_key(self, key_name: str) -> str:
        """Categorize key by name pattern"""
        key_lower = key_name.lower()
        
        # AI/LLM
        if any(x in key_lower for x in ['openai', 'anthropic', 'claude', 'gemini', 'gpt', 
                                         'perplexity', 'groq', 'deepseek', 'cohere', 'mistral',
                                         'cerebras', 'together', 'fireworks']):
            return '🤖 AI/LLM'
        
        # Image/Video
        if any(x in key_lower for x in ['stability', 'leonardo', 'replicate', 'midjourney',
                                         'runway', 'dall', 'image', 'fal', 'clipdrop']):
            return '🎨 Image/Video Generation'
        
        # Audio/Music
        if any(x in key_lower for x in ['elevenlabs', 'suno', 'mubert', 'play', 'audio',
                                         'assemblyai', 'deepgram', 'whisper', 'speech']):
            return '🎵 Audio/Music'
        
        # Social Media
        if any(x in key_lower for x in ['instagram', 'youtube', 'reddit', 'tiktok', 
                                         'twitter', 'telegram', 'discord']):
            return '📱 Social Media'
        
        # Cloud/Storage
        if any(x in key_lower for x in ['aws', 'azure', 'gcp', 'google_cloud', 'cloudflare',
                                         'supabase', 'firebase', 'r2', 's3', 'storage']):
            return '☁️ Cloud/Storage'
        
        # Database/Vector
        if any(x in key_lower for x in ['pinecone', 'chroma', 'weaviate', 'qdrant', 
                                         'postgres', 'mongodb', 'redis', 'database']):
            return '🗄️ Database/Vector'
        
        # Analytics/SEO
        if any(x in key_lower for x in ['analytics', 'seo', 'mixpanel', 'plausible',
                                         'posthog', 'heap', 'segment']):
            return '📊 Analytics/SEO'
        
        # Automation/Tools
        if any(x in key_lower for x in ['n8n', 'zapier', 'make', 'airtable', 'notion',
                                         'slack', 'webhook', 'monitor']):
            return '⚙️ Automation/Tools'
        
        # Development
        if any(x in key_lower for x in ['github', 'gitlab', 'vercel', 'netlify']):
            return '💻 Development'
        
        return '📦 Other/Config'
    
    def scan_all_env_files(self):
        """Scan all .env files"""
        self.print_header("🔍 SCANNING ALL .env FILES")
        
        env_files = list(self.env_dir.glob("*.env"))
        print(f"Found {len(env_files)} .env file(s)\n")
        
        for env_file in sorted(env_files):
            print(f"{Colors.CYAN}Scanning: {env_file.name}{Colors.END}")
            
            keys_in_file = 0
            
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        
                        if not line or line.startswith('#'):
                            continue
                        
                        if '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            
                            status, signifier = self.get_key_status(value)
                            category = self.categorize_key(key)
                            
                            # Store (prefer ACTIVE over others)
                            if key not in self.all_keys or status == "ACTIVE":
                                self.all_keys[key] = {
                                    'file': env_file.name,
                                    'status': status,
                                    'signifier': signifier,
                                    'category': category,
                                    'value_length': len(value)
                                }
                                keys_in_file += 1
                
                print(f"  Found {keys_in_file} keys\n")
                
            except Exception as e:
                print(f"{Colors.RED}  Error: {e}{Colors.END}\n")
        
        print(f"{Colors.GREEN}✅ Total unique keys found: {len(self.all_keys)}{Colors.END}\n")
    
    def display_by_category(self):
        """Display keys grouped by category"""
        self.print_header("📋 KEYS BY CATEGORY")
        
        by_category = defaultdict(list)
        for key_name, info in self.all_keys.items():
            by_category[info['category']].append((key_name, info))
        
        for category in sorted(by_category.keys()):
            keys = by_category[category]
            active_count = sum(1 for _, info in keys if info['status'] == 'ACTIVE')
            
            print(f"{Colors.BOLD}{category}{Colors.END} ({active_count}/{len(keys)} active)")
            
            for key_name, info in sorted(keys):
                status_color = Colors.GREEN if info['status'] == 'ACTIVE' else Colors.YELLOW
                print(f"  {status_color}{info['signifier']}{Colors.END} {key_name}")
            print()
    
    def check_specific_missing(self):
        """Check for specific important keys that might be missing"""
        self.print_header("🔍 CHECKING SPECIFIC SERVICES")
        
        # Check for specific services
        checks = {
            'Perplexity': ['PERPLEXITY_API_KEY', 'PERPLEXITY_KEY'],
            'Suno': ['SUNO_API_KEY', 'SUNO_KEY', 'SUNO_SESSION', 'SUNO_TOKEN'],
            'Instagram': ['INSTAGRAM_USERNAME', 'INSTAGRAM_PASSWORD', 'IG_USERNAME', 'IG_PASSWORD'],
            'YouTube': ['YOUTUBE_API_KEY', 'YOUTUBE_KEY', 'GOOGLE_YOUTUBE_API_KEY'],
        }
        
        results = {}
        
        for service, possible_keys in checks.items():
            found = False
            found_key = None
            
            for possible_key in possible_keys:
                if possible_key in self.all_keys:
                    if self.all_keys[possible_key]['status'] == 'ACTIVE':
                        found = True
                        found_key = possible_key
                        break
            
            if found:
                print(f"{Colors.GREEN}✅ {service:15} {found_key}{Colors.END}")
                results[service] = 'FOUND'
            else:
                print(f"{Colors.RED}❌ {service:15} Not found{Colors.END}")
                results[service] = 'MISSING'
        
        print()
        return results
    
    def save_report(self):
        """Save CSV report"""
        self.print_header("💾 SAVING REPORT")
        
        with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Key_Name', 'Category', 'Status', 'Signifier', 
                'Found_In', 'Key_Length'
            ])
            
            for key_name, info in sorted(self.all_keys.items()):
                writer.writerow([
                    key_name,
                    info['category'],
                    info['status'],
                    info['signifier'],
                    info['file'],
                    info['value_length']
                ])
        
        print(f"{Colors.GREEN}✅ Report: {self.output_file.name}{Colors.END}\n")
    
    def run(self):
        """Run inventory"""
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║              🔑 API KEY INVENTORY (SECURE - NO EXPOSURE) 🔑                   ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        # 1. Scan all files
        self.scan_all_env_files()
        
        # 2. Display by category
        self.display_by_category()
        
        # 3. Check specific services
        check_results = self.check_specific_missing()
        
        # 4. Save report
        self.save_report()
        
        # Summary
        self.print_header("📊 SUMMARY", Colors.GREEN)
        
        status_counts = defaultdict(int)
        for info in self.all_keys.values():
            status_counts[info['status']] += 1
        
        print(f"{Colors.BOLD}Total Keys: {len(self.all_keys)}{Colors.END}\n")
        print(f"  {Colors.GREEN}ACTIVE:{Colors.END}       {status_counts['ACTIVE']} (ready to use)")
        print(f"  {Colors.CYAN}CONFIG:{Colors.END}       {status_counts['CONFIG']} (config values)")
        print(f"  {Colors.YELLOW}PLACEHOLDER:{Colors.END}  {status_counts['PLACEHOLDER']} (need real keys)")
        print(f"  {Colors.RED}NOT_SET:{Colors.END}      {status_counts['NOT_SET']} (empty)\n")
        
        print(f"{Colors.CYAN}Full inventory: {self.output_file}{Colors.END}\n")


def main():
    inventory = APIKeyInventoryV2()
    inventory.run()


if __name__ == "__main__":
    main()
