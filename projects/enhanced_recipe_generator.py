#!/usr/bin/env python3
"""
Enhanced AI Recipe Generator - Production-Ready Version
High-engagement content system for $10K+ through SEO, affiliate marketing, and return visitors

IMPROVEMENTS:
- Enhanced error handling and logging
- Better API rate limiting
- Improved data validation
- Production-ready configuration
- Better affiliate link management
- Enhanced SEO optimization
"""

import os
import json
import sqlite3
import datetime
import random
import time
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from openai import OpenAI
import logging
from pathlib import Path
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enhanced logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/recipe_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class Recipe:
    """Enhanced recipe with better validation"""
    id: str
    title: str
    description: str
    ingredients: List[str]
    instructions: List[str]
    prep_time: str
    cook_time: str
    servings: int
    difficulty: str
    category: str
    tags: List[str]
    nutrition_info: Dict[str, Any]
    seo_keywords: List[str]
    affiliate_links: List[Dict[str, str]]
    image_prompt: str
    video_prompt: str
    created_at: str
    updated_at: str
    views: int = 0
    shares: int = 0
    affiliate_clicks: int = 0
    revenue: float = 0.0

    def __post_init__(self):
        """Validate recipe data after initialization"""
        if not self.title or len(self.title.strip()) < 3:
            raise ValueError("Recipe title must be at least 3 characters")
        if not self.ingredients or len(self.ingredients) < 2:
            raise ValueError("Recipe must have at least 2 ingredients")
        if not self.instructions or len(self.instructions) < 2:
            raise ValueError("Recipe must have at least 2 instructions")
        if self.servings < 1:
            raise ValueError("Servings must be at least 1")

class EnhancedAIRecipeGenerator:
    """Enhanced AI Recipe Generator with production-ready features"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or os.getenv('RECIPE_DB_PATH', 'databases/recipe_generator.db')
        self.openai_client = None
        self.rate_limit_delay = 1.0  # Delay between API calls
        self.last_api_call = 0
        self._init_database()
        self._load_openai_client()
        self.seasonal_themes = self._load_seasonal_themes()
        self.trending_keywords = self._load_trending_keywords()
        self.affiliate_programs = self._load_affiliate_programs()
        
    def _init_database(self):
        """Initialize database with enhanced schema"""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Enhanced recipes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recipes (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    ingredients TEXT,
                    instructions TEXT,
                    prep_time TEXT,
                    cook_time TEXT,
                    servings INTEGER,
                    difficulty TEXT,
                    category TEXT,
                    tags TEXT,
                    nutrition_info TEXT,
                    seo_keywords TEXT,
                    affiliate_links TEXT,
                    image_prompt TEXT,
                    video_prompt TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    views INTEGER DEFAULT 0,
                    shares INTEGER DEFAULT 0,
                    affiliate_clicks INTEGER DEFAULT 0,
                    revenue REAL DEFAULT 0.0
                )
            ''')
            
            # Enhanced campaigns table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS campaigns (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    theme TEXT,
                    target_keywords TEXT,
                    recipes TEXT,
                    budget REAL,
                    spent REAL DEFAULT 0.0,
                    revenue REAL DEFAULT 0.0,
                    status TEXT DEFAULT 'active',
                    created_at TEXT,
                    updated_at TEXT
                )
            ''')
            
            # Analytics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analytics (
                    id TEXT PRIMARY KEY,
                    metric_name TEXT NOT NULL,
                    metric_value REAL,
                    date TEXT,
                    recipe_id TEXT,
                    platform TEXT,
                    created_at TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    def _load_openai_client(self):
        """Load OpenAI client with better error handling"""
        try:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                # Try to load from the old location
                env_file = Path.home() / '.env.d' / 'llm-apis.env'
                if env_file.exists():
                    load_dotenv(env_file)
                    api_key = os.getenv('OPENAI_API_KEY')
            
            if not api_key:
                raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in .env file")
            
            self.openai_client = OpenAI(api_key=api_key)
            logger.info("OpenAI client loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load OpenAI client: {e}")
            raise
    
    def _rate_limit(self):
        """Implement rate limiting for API calls"""
        current_time = time.time()
        time_since_last_call = current_time - self.last_api_call
        
        if time_since_last_call < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last_call
            logger.info(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_api_call = time.time()
    
    def generate_recipe(self, theme: str = None, category: str = None, 
                       difficulty: str = "easy", servings: int = 4) -> Recipe:
        """Generate a recipe with enhanced error handling and validation"""
        try:
            self._rate_limit()
            
            # Generate theme if not provided
            if not theme:
                theme = random.choice(list(self.seasonal_themes.keys()))
            
            # Generate category if not provided
            if not category:
                category = random.choice(['breakfast', 'lunch', 'dinner', 'dessert', 'snack'])
            
            # Create enhanced prompt
            prompt = self._create_enhanced_prompt(theme, category, difficulty, servings)
            
            # Call OpenAI API
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
            )
            
            # Parse response with better error handling
            recipe_data = self._parse_recipe_response(response.choices[0].message.content)
            
            # Create and validate recipe
            recipe = Recipe(
                id=f"recipe_{int(time.time())}_{random.randint(1000, 9999)}",
                title=recipe_data.get('title', 'Untitled Recipe'),
                description=recipe_data.get('description', ''),
                ingredients=recipe_data.get('ingredients', []),
                instructions=recipe_data.get('instructions', []),
                prep_time=recipe_data.get('prep_time', '15 minutes'),
                cook_time=recipe_data.get('cook_time', '30 minutes'),
                servings=recipe_data.get('servings', servings),
                difficulty=recipe_data.get('difficulty', difficulty),
                category=recipe_data.get('category', category),
                tags=recipe_data.get('tags', []),
                nutrition_info=recipe_data.get('nutrition_info', {}),
                seo_keywords=recipe_data.get('seo_keywords', []),
                affiliate_links=recipe_data.get('affiliate_links', []),
                image_prompt=recipe_data.get('image_prompt', ''),
                video_prompt=recipe_data.get('video_prompt', ''),
                created_at=datetime.datetime.now().isoformat(),
                updated_at=datetime.datetime.now().isoformat()
            )
            
            # Save to database
            if self._save_recipe(recipe):
                logger.info(f"Recipe generated successfully: {recipe.title}")
                return recipe
            else:
                raise Exception("Failed to save recipe to database")
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            # Return a fallback recipe
            return self._create_fallback_recipe(theme, category, difficulty, servings)
        except Exception as e:
            logger.error(f"Recipe generation failed: {e}")
            return self._create_fallback_recipe(theme, category, difficulty, servings)
    
    def _create_enhanced_prompt(self, theme: str, category: str, difficulty: str, servings: int) -> str:
        """Create an enhanced prompt for better recipe generation"""
        return f"""
Generate a detailed recipe for a {difficulty} {category} dish that serves {servings} people, themed around {theme}.

The recipe should be:
- SEO-optimized with relevant keywords
- Include affiliate marketing opportunities
- Have clear, step-by-step instructions
- Include nutritional information
- Be engaging and shareable

Please respond with a JSON object containing:
{{
    "title": "Recipe title (SEO-optimized)",
    "description": "Appetizing description (2-3 sentences)",
    "ingredients": ["ingredient 1", "ingredient 2", ...],
    "instructions": ["step 1", "step 2", ...],
    "prep_time": "X minutes",
    "cook_time": "X minutes",
    "servings": {servings},
    "difficulty": "{difficulty}",
    "category": "{category}",
    "tags": ["tag1", "tag2", ...],
    "nutrition_info": {{
        "calories": "X per serving",
        "protein": "Xg",
        "carbs": "Xg",
        "fat": "Xg"
    }},
    "seo_keywords": ["keyword1", "keyword2", ...],
    "affiliate_links": [
        {{"product": "product name", "url": "affiliate_url", "description": "why recommend"}}
    ],
    "image_prompt": "Detailed prompt for DALL-E image generation",
    "video_prompt": "Detailed prompt for video content creation"
}}

Make sure the JSON is valid and complete.
"""
    
    def _parse_recipe_response(self, response: str) -> Dict[str, Any]:
        """Parse recipe response with better error handling"""
        try:
            # Clean the response
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            logger.error(f"Response content: {response[:500]}...")
            raise
    
    def _create_fallback_recipe(self, theme: str, category: str, difficulty: str, servings: int) -> Recipe:
        """Create a fallback recipe when AI generation fails"""
        logger.warning("Creating fallback recipe due to generation failure")
        
        return Recipe(
            id=f"fallback_recipe_{int(time.time())}",
            title=f"Simple {category.title()} Recipe",
            description=f"A delicious {difficulty} {category} perfect for {theme} season.",
            ingredients=["2 cups main ingredient", "1 cup secondary ingredient", "Salt and pepper to taste"],
            instructions=["Prepare ingredients", "Cook according to package directions", "Season and serve"],
            prep_time="10 minutes",
            cook_time="20 minutes",
            servings=servings,
            difficulty=difficulty,
            category=category,
            tags=[theme, category, difficulty],
            nutrition_info={"calories": "200 per serving", "protein": "10g", "carbs": "25g", "fat": "5g"},
            seo_keywords=[f"{category} recipe", f"{difficulty} cooking", theme],
            affiliate_links=[],
            image_prompt=f"Delicious {category} dish, {theme} theme, food photography",
            video_prompt=f"Quick {difficulty} {category} recipe tutorial",
            created_at=datetime.datetime.now().isoformat(),
            updated_at=datetime.datetime.now().isoformat()
        )
    
    def _save_recipe(self, recipe: Recipe) -> bool:
        """Save recipe to database with better error handling"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO recipes 
                (id, title, description, ingredients, instructions, prep_time, cook_time, 
                 servings, difficulty, category, tags, nutrition_info, seo_keywords, 
                 affiliate_links, image_prompt, video_prompt, created_at, updated_at, 
                 views, shares, affiliate_clicks, revenue)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                recipe.id, recipe.title, recipe.description,
                json.dumps(recipe.ingredients), json.dumps(recipe.instructions),
                recipe.prep_time, recipe.cook_time, recipe.servings,
                recipe.difficulty, recipe.category, json.dumps(recipe.tags),
                json.dumps(recipe.nutrition_info), json.dumps(recipe.seo_keywords),
                json.dumps(recipe.affiliate_links), recipe.image_prompt, recipe.video_prompt,
                recipe.created_at, recipe.updated_at, recipe.views, recipe.shares,
                recipe.affiliate_clicks, recipe.revenue
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Failed to save recipe: {e}")
            return False
    
    def _load_seasonal_themes(self) -> Dict[str, List[str]]:
        """Load seasonal themes with more variety"""
        return {
            "January": ["comfort food", "warm soups", "hearty stews", "winter vegetables"],
            "February": ["romantic dinners", "chocolate desserts", "valentine's treats"],
            "March": ["spring vegetables", "light meals", "fresh herbs", "green recipes"],
            "April": ["easter recipes", "spring cleaning", "fresh salads", "asparagus"],
            "May": ["mother's day", "spring flowers", "light desserts", "fresh fruits"],
            "June": ["summer grilling", "fresh berries", "picnic foods", "cold soups"],
            "July": ["4th of july", "summer bbq", "cold desserts", "refreshing drinks"],
            "August": ["back to school", "quick meals", "summer vegetables", "easy dinners"],
            "September": ["fall flavors", "apple recipes", "harvest foods", "comfort meals"],
            "October": ["halloween treats", "pumpkin recipes", "fall soups", "spooky foods"],
            "November": ["thanksgiving", "turkey recipes", "fall desserts", "comfort food"],
            "December": ["christmas cookies", "holiday meals", "winter treats", "festive foods"]
        }
    
    def _load_trending_keywords(self) -> List[str]:
        """Load trending SEO keywords"""
        return [
            "easy recipes", "quick meals", "healthy cooking", "meal prep",
            "budget recipes", "family dinners", "comfort food", "quick breakfast",
            "one pot meals", "sheet pan dinners", "instant pot recipes",
            "air fryer recipes", "keto recipes", "vegan recipes", "gluten free",
            "low carb", "high protein", "meal planning", "cooking tips"
        ]
    
    def _load_affiliate_programs(self) -> List[Dict[str, str]]:
        """Load affiliate programs with better management"""
        return [
            {
                "name": "Amazon Kitchen",
                "base_url": "https://amazon.com/dp/",
                "tag": os.getenv('AFFILIATE_AMAZON_TAG', 'your-amazon-tag'),
                "commission": "4-8%"
            },
            {
                "name": "HelloFresh",
                "base_url": "https://hellofresh.com/",
                "code": os.getenv('AFFILIATE_HELLOFRESH_CODE', 'your-hellofresh-code'),
                "commission": "$40-60 per signup"
            },
            {
                "name": "Vitamix",
                "base_url": "https://vitamix.com/",
                "code": os.getenv('AFFILIATE_VITAMIX_CODE', 'your-vitamix-code'),
                "commission": "5-10%"
            }
        ]

def main():
    """Enhanced main function with better error handling"""
    try:
        print("🍳 Enhanced AI Recipe Generator - Production Ready")
        print("=" * 50)
        
        generator = EnhancedAIRecipeGenerator()
        
        # Generate a sample recipe
        print("Generating sample recipe...")
        recipe = generator.generate_recipe(
            theme="comfort food",
            category="dinner",
            difficulty="easy",
            servings=4
        )
        
        print(f"✅ Recipe generated: {recipe.title}")
        print(f"📝 Description: {recipe.description}")
        print(f"⏱️  Prep time: {recipe.prep_time}, Cook time: {recipe.cook_time}")
        print(f"👥 Serves: {recipe.servings}")
        print(f"🏷️  Tags: {', '.join(recipe.tags)}")
        print(f"🔗 Affiliate links: {len(recipe.affiliate_links)}")
        
    except Exception as e:
        logger.error(f"Main function failed: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()