#!/usr/bin/env python3
"""
Production Configuration - Optimized settings for maximum revenue
Production-ready configuration for all passive income systems
"""

import os
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class ProductionConfig:
    """Production configuration for all systems"""
    
    # API Configuration
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_MAX_TOKENS: int = 2000
    OPENAI_TEMPERATURE: float = 0.7
    
    # Rate Limiting
    API_RATE_LIMIT: float = 1.0  # seconds between API calls
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 5.0
    
    # Database Configuration
    RECIPE_DB_PATH: str = os.getenv('RECIPE_DB_PATH', 'databases/recipe_generator.db')
    RECEPTIONIST_DB_PATH: str = os.getenv('RECEPTIONIST_DB_PATH', 'databases/ai_receptionist.db')
    REVENUE_DB_PATH: str = os.getenv('REVENUE_DB_PATH', 'databases/revenue_dashboard.db')
    
    # Content Generation
    DAILY_RECIPE_COUNT: int = int(os.getenv('DAILY_RECIPE_COUNT', '3'))
    MAX_RECIPES_PER_CAMPAIGN: int = int(os.getenv('MAX_RECIPES_PER_CAMPAIGN', '10'))
    CONTENT_QUALITY_LEVEL: str = os.getenv('CONTENT_QUALITY_LEVEL', 'high')
    
    # Revenue Goals
    MONTHLY_REVENUE_GOAL: float = float(os.getenv('MONTHLY_REVENUE_GOAL', '10000'))
    DAILY_REVENUE_GOAL: float = float(os.getenv('DAILY_REVENUE_GOAL', '350'))
    WEEKLY_REVENUE_GOAL: float = float(os.getenv('WEEKLY_REVENUE_GOAL', '2500'))
    
    # Affiliate Programs
    AFFILIATE_AMAZON_TAG: str = os.getenv('AFFILIATE_AMAZON_TAG', 'your-amazon-tag')
    AFFILIATE_HELLOFRESH_CODE: str = os.getenv('AFFILIATE_HELLOFRESH_CODE', 'your-hellofresh-code')
    AFFILIATE_VITAMIX_CODE: str = os.getenv('AFFILIATE_VITAMIX_CODE', 'your-vitamix-code')
    
    # Social Media
    INSTAGRAM_API_KEY: str = os.getenv('INSTAGRAM_API_KEY', '')
    PINTEREST_API_KEY: str = os.getenv('PINTEREST_API_KEY', '')
    TIKTOK_API_KEY: str = os.getenv('TIKTOK_API_KEY', '')
    
    # SEO Configuration
    SEO_KEYWORDS_PER_RECIPE: int = 10
    SEO_DESCRIPTION_LENGTH: int = 160
    SEO_TITLE_LENGTH: int = 60
    
    # Content Optimization
    MIN_INGREDIENTS: int = 3
    MAX_INGREDIENTS: int = 15
    MIN_INSTRUCTIONS: int = 3
    MAX_INSTRUCTIONS: int = 10
    
    # Analytics
    ANALYTICS_RETENTION_DAYS: int = 365
    DAILY_ANALYTICS_REPORT: bool = True
    WEEKLY_OPTIMIZATION_REVIEW: bool = True
    
    # Error Handling
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = 'logs/passive_income_empire.log'
    ERROR_NOTIFICATION_EMAIL: str = os.getenv('ERROR_NOTIFICATION_EMAIL', '')
    
    # Performance
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600  # 1 hour
    MAX_CONCURRENT_REQUESTS: int = 5
    
    # Security
    ENCRYPT_DATABASE: bool = True
    BACKUP_ENABLED: bool = True
    BACKUP_FREQUENCY: str = 'daily'
    
    def validate(self) -> bool:
        """Validate configuration"""
        required_fields = [
            'OPENAI_API_KEY',
            'RECIPE_DB_PATH',
            'RECEPTIONIST_DB_PATH'
        ]
        
        for field in required_fields:
            if not getattr(self, field):
                print(f"❌ Missing required configuration: {field}")
                return False
        
        return True
    
    def get_affiliate_config(self) -> Dict[str, Any]:
        """Get affiliate program configuration"""
        return {
            "amazon": {
                "base_url": "https://amazon.com/dp/",
                "tag": self.AFFILIATE_AMAZON_TAG,
                "commission": "4-8%",
                "enabled": bool(self.AFFILIATE_AMAZON_TAG)
            },
            "hellofresh": {
                "base_url": "https://hellofresh.com/",
                "code": self.AFFILIATE_HELLOFRESH_CODE,
                "commission": "$40-60 per signup",
                "enabled": bool(self.AFFILIATE_HELLOFRESH_CODE)
            },
            "vitamix": {
                "base_url": "https://vitamix.com/",
                "code": self.AFFILIATE_VITAMIX_CODE,
                "commission": "5-10%",
                "enabled": bool(self.AFFILIATE_VITAMIX_CODE)
            }
        }
    
    def get_seo_config(self) -> Dict[str, Any]:
        """Get SEO configuration"""
        return {
            "keywords_per_recipe": self.SEO_KEYWORDS_PER_RECIPE,
            "description_length": self.SEO_DESCRIPTION_LENGTH,
            "title_length": self.SEO_TITLE_LENGTH,
            "meta_robots": "index, follow",
            "canonical_url": True,
            "structured_data": True
        }
    
    def get_content_config(self) -> Dict[str, Any]:
        """Get content generation configuration"""
        return {
            "daily_recipe_count": self.DAILY_RECIPE_COUNT,
            "max_recipes_per_campaign": self.MAX_RECIPES_PER_CAMPAIGN,
            "quality_level": self.CONTENT_QUALITY_LEVEL,
            "min_ingredients": self.MIN_INGREDIENTS,
            "max_ingredients": self.MAX_INGREDIENTS,
            "min_instructions": self.MIN_INSTRUCTIONS,
            "max_instructions": self.MAX_INSTRUCTIONS
        }

# Global configuration instance
config = ProductionConfig()

def get_config() -> ProductionConfig:
    """Get the global configuration instance"""
    return config

def validate_config() -> bool:
    """Validate the global configuration"""
    return config.validate()

if __name__ == "__main__":
    """Test configuration"""
    print("🔧 Production Configuration Test")
    print("=" * 40)
    
    if validate_config():
        print("✅ Configuration is valid")
        print(f"📊 Monthly Revenue Goal: ${config.MONTHLY_REVENUE_GOAL:,.2f}")
        print(f"🍳 Daily Recipe Count: {config.DAILY_RECIPE_COUNT}")
        print(f"🔗 Affiliate Programs: {len([k for k, v in config.get_affiliate_config().items() if v['enabled']])}")
    else:
        print("❌ Configuration is invalid")
        print("Please check your .env file and required settings")