#!/usr/bin/env python3
"""
AI Recipe Generator - High-Engagement Content System
Path to $10K+ through SEO, affiliate marketing, and return visitors

Features:
- AI-powered recipe generation
- SEO-optimized content
- Affiliate link integration
- Seasonal content strategy
- Social media optimization
- Analytics and tracking
"""

import os
import json
import sqlite3
import datetime
import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from openai import OpenAI
import logging
from pathlib import Path
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Recipe:
    """Represents a generated recipe"""
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
    views: int = 0
    shares: int = 0
    affiliate_clicks: int = 0

@dataclass
class ContentCampaign:
    """Represents a content marketing campaign"""
    id: str
    name: str
    theme: str
    target_keywords: List[str]
    recipes: List[str]
    start_date: str
    end_date: str
    budget: float
    expected_revenue: float
    status: str

class AIRecipeGenerator:
    """Main AI Recipe Generator system"""
    
    def __init__(self, db_path: str = "recipe_generator.db"):
        self.db_path = db_path
        self.openai_client = None
        self._init_database()
        self._load_openai_client()
        
        # Content strategies
        self.seasonal_themes = self._load_seasonal_themes()
        self.trending_keywords = self._load_trending_keywords()
        self.affiliate_programs = self._load_affiliate_programs()
    
    def _init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create recipes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL,
                prep_time TEXT NOT NULL,
                cook_time TEXT NOT NULL,
                servings INTEGER NOT NULL,
                difficulty TEXT NOT NULL,
                category TEXT NOT NULL,
                tags TEXT NOT NULL,
                nutrition_info TEXT NOT NULL,
                seo_keywords TEXT NOT NULL,
                affiliate_links TEXT NOT NULL,
                image_prompt TEXT NOT NULL,
                video_prompt TEXT NOT NULL,
                created_at TEXT NOT NULL,
                views INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                affiliate_clicks INTEGER DEFAULT 0
            )
        ''')
        
        # Create campaigns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaigns (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                theme TEXT NOT NULL,
                target_keywords TEXT NOT NULL,
                recipes TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                budget REAL NOT NULL,
                expected_revenue REAL NOT NULL,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Create analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id TEXT PRIMARY KEY,
                recipe_id TEXT NOT NULL,
                metric_type TEXT NOT NULL,
                metric_value REAL NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (recipe_id) REFERENCES recipes (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def _load_openai_client(self):
        """Load OpenAI client"""
        try:
            # Try to load from your .env.d directory
            env_d_path = os.path.expanduser("~/.env.d/llm-apis.env")
            if os.path.exists(env_d_path):
                from dotenv import load_dotenv
                load_dotenv(env_d_path)
            
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key not found")
            
            self.openai_client = OpenAI(api_key=api_key)
            logger.info("OpenAI client loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load OpenAI client: {e}")
            self.openai_client = None
    
    def _load_seasonal_themes(self) -> Dict[str, List[str]]:
        """Load seasonal content themes"""
        return {
            "january": ["New Year healthy recipes", "Detox smoothies", "Winter comfort food"],
            "february": ["Valentine's Day treats", "Romantic dinners", "Chocolate desserts"],
            "march": ["St. Patrick's Day", "Spring cleaning detox", "Easter preparations"],
            "april": ["Easter recipes", "Spring vegetables", "Light and fresh meals"],
            "may": ["Mother's Day brunch", "Spring salads", "Outdoor grilling prep"],
            "june": ["Summer BBQ", "Father's Day", "Graduation parties"],
            "july": ["4th of July", "Summer picnics", "Cooling drinks"],
            "august": ["Back to school", "End of summer", "Harvest recipes"],
            "september": ["Fall comfort food", "Apple recipes", "School lunches"],
            "october": ["Halloween treats", "Pumpkin everything", "Cozy soups"],
            "november": ["Thanksgiving", "Fall flavors", "Holiday prep"],
            "december": ["Christmas recipes", "Holiday parties", "New Year prep"]
        }
    
    def _load_trending_keywords(self) -> List[str]:
        """Load trending SEO keywords"""
        return [
            "easy recipes for beginners",
            "healthy meal prep",
            "quick dinner ideas",
            "keto recipes",
            "vegan recipes",
            "gluten-free recipes",
            "air fryer recipes",
            "instant pot recipes",
            "one-pot meals",
            "meal prep recipes",
            "budget-friendly meals",
            "family dinner ideas",
            "comfort food recipes",
            "healthy snacks",
            "dessert recipes"
        ]
    
    def _load_affiliate_programs(self) -> List[Dict[str, str]]:
        """Load affiliate program information"""
        return [
            {
                "name": "Amazon Kitchen Tools",
                "category": "kitchen_equipment",
                "commission": "4-8%",
                "keywords": ["kitchen tools", "cooking equipment", "bakeware"]
            },
            {
                "name": "HelloFresh",
                "category": "meal_kits",
                "commission": "$5-15 per signup",
                "keywords": ["meal prep", "ingredients", "cooking kits"]
            },
            {
                "name": "Vitamix",
                "category": "appliances",
                "commission": "5-10%",
                "keywords": ["smoothies", "blending", "healthy drinks"]
            },
            {
                "name": "Instant Pot",
                "category": "appliances",
                "commission": "3-7%",
                "keywords": ["pressure cooking", "quick meals", "one-pot"]
            },
            {
                "name": "Spice Companies",
                "category": "ingredients",
                "commission": "5-15%",
                "keywords": ["seasonings", "spices", "flavor"]
            }
        ]
    
    def generate_recipe(self, theme: str = None, category: str = None, 
                       difficulty: str = "easy", servings: int = 4) -> Recipe:
        """Generate a new recipe using AI"""
        if not self.openai_client:
            raise ValueError("OpenAI client not available")
        
        try:
            # Determine theme and category
            if not theme:
                current_month = datetime.datetime.now().strftime("%B").lower()
                theme = random.choice(self.seasonal_themes.get(current_month, ["comfort food"]))
            
            if not category:
                categories = ["breakfast", "lunch", "dinner", "dessert", "snack", "beverage"]
                category = random.choice(categories)
            
            # Generate recipe using AI
            prompt = f"""
            Create a detailed recipe with the following specifications:
            - Theme: {theme}
            - Category: {category}
            - Difficulty: {difficulty}
            - Servings: {servings}
            
            Please provide:
            1. A catchy, SEO-friendly title
            2. A compelling description (2-3 sentences)
            3. List of ingredients with measurements
            4. Step-by-step cooking instructions
            5. Prep time and cook time
            6. Difficulty level
            7. Relevant tags for SEO
            8. Basic nutrition information
            9. SEO keywords that people would search for
            10. Affiliate product suggestions with descriptions
            
            Format as JSON with the following structure:
            {{
                "title": "Recipe Title",
                "description": "Recipe description",
                "ingredients": ["ingredient 1", "ingredient 2"],
                "instructions": ["step 1", "step 2"],
                "prep_time": "15 minutes",
                "cook_time": "30 minutes",
                "servings": 4,
                "difficulty": "easy",
                "category": "dinner",
                "tags": ["tag1", "tag2"],
                "nutrition": {{"calories": 300, "protein": 25, "carbs": 30, "fat": 10}},
                "seo_keywords": ["keyword1", "keyword2"],
                "affiliate_products": [
                    {{"name": "Product Name", "description": "Why you need this", "category": "kitchen_equipment"}}
                ]
            }}
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=1500
            )
            
            # Parse AI response
            try:
                recipe_data = json.loads(response.choices[0].message.content)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response as JSON: {e}")
                # Fallback: create a basic recipe structure
                recipe_data = {
                    "title": f"Quick {category} Recipe",
                    "description": f"A delicious and easy {category} recipe perfect for any occasion.",
                    "ingredients": ["2 cups main ingredient", "1 tbsp seasoning", "Salt and pepper to taste"],
                    "instructions": ["Prepare ingredients", "Cook according to package directions", "Season to taste", "Serve hot"],
                    "prep_time": "10 minutes",
                    "cook_time": "20 minutes",
                    "servings": 4,
                    "difficulty": difficulty,
                    "category": category,
                    "tags": [category, "easy", "quick"],
                    "nutrition": {"calories": 300, "protein": 15, "carbs": 30, "fat": 10},
                    "seo_keywords": [f"{category} recipe", "easy recipe", "quick meal"],
                    "affiliate_products": [{"name": "Kitchen Essentials", "description": "Essential cooking tools", "category": "kitchen_equipment"}]
                }
            
            # Create Recipe object
            recipe_id = f"recipe_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
            
            recipe = Recipe(
                id=recipe_id,
                title=recipe_data["title"],
                description=recipe_data["description"],
                ingredients=recipe_data["ingredients"],
                instructions=recipe_data["instructions"],
                prep_time=recipe_data["prep_time"],
                cook_time=recipe_data["cook_time"],
                servings=recipe_data["servings"],
                difficulty=recipe_data["difficulty"],
                category=recipe_data["category"],
                tags=recipe_data["tags"],
                nutrition_info=recipe_data["nutrition"],
                seo_keywords=recipe_data["seo_keywords"],
                affiliate_links=recipe_data["affiliate_products"],
                image_prompt=f"Professional food photography of {recipe_data['title']}, appetizing, well-lit, restaurant quality",
                video_prompt=f"Step-by-step cooking video of {recipe_data['title']}, clear instructions, engaging presentation",
                created_at=datetime.datetime.now().isoformat()
            )
            
            # Save to database
            self._save_recipe(recipe)
            
            logger.info(f"Generated recipe: {recipe.title}")
            return recipe
            
        except Exception as e:
            logger.error(f"Failed to generate recipe: {e}")
            raise
    
    def _save_recipe(self, recipe: Recipe) -> bool:
        """Save recipe to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO recipes (id, title, description, ingredients, instructions,
                                   prep_time, cook_time, servings, difficulty, category,
                                   tags, nutrition_info, seo_keywords, affiliate_links,
                                   image_prompt, video_prompt, created_at, views, shares, affiliate_clicks)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                recipe.id, recipe.title, recipe.description,
                json.dumps(recipe.ingredients), json.dumps(recipe.instructions),
                recipe.prep_time, recipe.cook_time, recipe.servings,
                recipe.difficulty, recipe.category, json.dumps(recipe.tags),
                json.dumps(recipe.nutrition_info), json.dumps(recipe.seo_keywords),
                json.dumps(recipe.affiliate_links), recipe.image_prompt,
                recipe.video_prompt, recipe.created_at, recipe.views,
                recipe.shares, recipe.affiliate_clicks
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Failed to save recipe: {e}")
            return False
    
    def generate_seasonal_campaign(self, month: str, budget: float = 1000.0) -> ContentCampaign:
        """Generate a seasonal content campaign"""
        themes = self.seasonal_themes.get(month.lower(), ["comfort food"])
        theme = random.choice(themes)
        
        # Generate target keywords for the theme
        target_keywords = self._generate_keywords_for_theme(theme)
        
        # Create campaign
        campaign_id = f"campaign_{month}_{datetime.datetime.now().strftime('%Y%m%d')}"
        
        campaign = ContentCampaign(
            id=campaign_id,
            name=f"{month.title()} {theme} Campaign",
            theme=theme,
            target_keywords=target_keywords,
            recipes=[],
            start_date=datetime.datetime.now().isoformat(),
            end_date=(datetime.datetime.now() + datetime.timedelta(days=30)).isoformat(),
            budget=budget,
            expected_revenue=budget * 3,  # 3x ROI target
            status="active"
        )
        
        # Generate recipes for the campaign
        for _ in range(10):  # 10 recipes per campaign
            try:
                recipe = self.generate_recipe(theme=theme)
                campaign.recipes.append(recipe.id)
            except Exception as e:
                logger.error(f"Failed to generate recipe for campaign: {e}")
                # Continue with next recipe instead of failing entire campaign
        
        # Save campaign
        self._save_campaign(campaign)
        
        return campaign
    
    def _generate_keywords_for_theme(self, theme: str) -> List[str]:
        """Generate SEO keywords for a theme"""
        if not self.openai_client:
            return self.trending_keywords[:5]
        
        try:
            prompt = f"""
            Generate 10 high-value SEO keywords for the recipe theme: "{theme}"
            
            Focus on:
            - Long-tail keywords with commercial intent
            - Keywords people actually search for
            - Keywords with good search volume
            - Keywords that convert to affiliate sales
            
            Return as a JSON array of strings.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            
            keywords = json.loads(response.choices[0].message.content)
            return keywords if isinstance(keywords, list) else self.trending_keywords[:5]
            
        except Exception as e:
            logger.error(f"Failed to generate keywords: {e}")
            return self.trending_keywords[:5]
    
    def _save_campaign(self, campaign: ContentCampaign) -> bool:
        """Save campaign to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO campaigns (id, name, theme, target_keywords, recipes,
                                     start_date, end_date, budget, expected_revenue, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                campaign.id, campaign.name, campaign.theme,
                json.dumps(campaign.target_keywords), json.dumps(campaign.recipes),
                campaign.start_date, campaign.end_date, campaign.budget,
                campaign.expected_revenue, campaign.status
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Failed to save campaign: {e}")
            return False
    
    def get_recipe(self, recipe_id: str) -> Optional[Recipe]:
        """Get recipe by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return Recipe(
                    id=row[0], title=row[1], description=row[2],
                    ingredients=json.loads(row[3]), instructions=json.loads(row[4]),
                    prep_time=row[5], cook_time=row[6], servings=row[7],
                    difficulty=row[8], category=row[9], tags=json.loads(row[10]),
                    nutrition_info=json.loads(row[11]), seo_keywords=json.loads(row[12]),
                    affiliate_links=json.loads(row[13]), image_prompt=row[14],
                    video_prompt=row[15], created_at=row[16], views=row[17],
                    shares=row[18], affiliate_clicks=row[19]
                )
            return None
        except Exception as e:
            logger.error(f"Failed to get recipe: {e}")
            return None
    
    def get_recipes_by_category(self, category: str, limit: int = 10) -> List[Recipe]:
        """Get recipes by category"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM recipes 
                WHERE category = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (category, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            recipes = []
            for row in rows:
                recipes.append(Recipe(
                    id=row[0], title=row[1], description=row[2],
                    ingredients=json.loads(row[3]), instructions=json.loads(row[4]),
                    prep_time=row[5], cook_time=row[6], servings=row[7],
                    difficulty=row[8], category=row[9], tags=json.loads(row[10]),
                    nutrition_info=json.loads(row[11]), seo_keywords=json.loads(row[12]),
                    affiliate_links=json.loads(row[13]), image_prompt=row[14],
                    video_prompt=row[15], created_at=row[16], views=row[17],
                    shares=row[18], affiliate_clicks=row[19]
                ))
            
            return recipes
        except Exception as e:
            logger.error(f"Failed to get recipes by category: {e}")
            return []
    
    def generate_seo_content(self, recipe: Recipe) -> str:
        """Generate SEO-optimized content for a recipe"""
        content = f"""
# {recipe.title}

{recipe.description}

## Ingredients
{chr(10).join([f"- {ingredient}" for ingredient in recipe.ingredients])}

## Instructions
{chr(10).join([f"{i+1}. {instruction}" for i, instruction in enumerate(recipe.instructions)])}

## Nutrition Information
- **Calories:** {recipe.nutrition_info.get('calories', 'N/A')}
- **Protein:** {recipe.nutrition_info.get('protein', 'N/A')}g
- **Carbohydrates:** {recipe.nutrition_info.get('carbs', 'N/A')}g
- **Fat:** {recipe.nutrition_info.get('fat', 'N/A')}g

## Recipe Details
- **Prep Time:** {recipe.prep_time}
- **Cook Time:** {recipe.cook_time}
- **Servings:** {recipe.servings}
- **Difficulty:** {recipe.difficulty.title()}

## Recommended Products
{chr(10).join([f"- **{product['name']}:** {product['description']}" for product in recipe.affiliate_links])}

## Tags
{', '.join(recipe.tags)}

---
*Keywords: {', '.join(recipe.seo_keywords)}*
"""
        return content
    
    def get_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get analytics for the recipe generator"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get total recipes
            cursor.execute('SELECT COUNT(*) FROM recipes')
            total_recipes = cursor.fetchone()[0]
            
            # Get total views
            cursor.execute('SELECT SUM(views) FROM recipes')
            total_views = cursor.fetchone()[0] or 0
            
            # Get total shares
            cursor.execute('SELECT SUM(shares) FROM recipes')
            total_shares = cursor.fetchone()[0] or 0
            
            # Get total affiliate clicks
            cursor.execute('SELECT SUM(affiliate_clicks) FROM recipes')
            total_clicks = cursor.fetchone()[0] or 0
            
            # Get top performing recipes
            cursor.execute('''
                SELECT title, views, shares, affiliate_clicks 
                FROM recipes 
                ORDER BY views DESC 
                LIMIT 5
            ''')
            top_recipes = cursor.fetchall()
            
            conn.close()
            
            return {
                'total_recipes': total_recipes,
                'total_views': total_views,
                'total_shares': total_shares,
                'total_affiliate_clicks': total_clicks,
                'top_recipes': top_recipes,
                'period_days': days
            }
        except Exception as e:
            logger.error(f"Failed to get analytics: {e}")
            return {}

def main():
    """Main function to demonstrate the AI Recipe Generator"""
    print("🍳 AI Recipe Generator - High-Engagement Content System")
    print("=" * 60)
    print("Path to $10K+ through SEO, affiliate marketing, and return visitors")
    print()
    
    # Initialize the system
    generator = AIRecipeGenerator()
    
    print("🚀 Generating sample recipes...")
    
    # Generate sample recipes
    sample_recipes = []
    categories = ["breakfast", "lunch", "dinner", "dessert", "snack"]
    
    for category in categories:
        try:
            recipe = generator.generate_recipe(category=category)
            sample_recipes.append(recipe)
            print(f"✅ Generated: {recipe.title}")
        except Exception as e:
            print(f"❌ Failed to generate {category} recipe: {e}")
    
    print(f"\n📊 Generated {len(sample_recipes)} recipes successfully!")
    
    # Show analytics
    analytics = generator.get_analytics()
    print(f"\n📈 System Analytics:")
    print(f"Total Recipes: {analytics.get('total_recipes', 0)}")
    print(f"Total Views: {analytics.get('total_views', 0)}")
    print(f"Total Shares: {analytics.get('total_shares', 0)}")
    print(f"Affiliate Clicks: {analytics.get('total_affiliate_clicks', 0)}")
    
    # Generate seasonal campaign
    print(f"\n🎯 Generating seasonal campaign...")
    current_month = datetime.datetime.now().strftime("%B")
    campaign = generator.generate_seasonal_campaign(current_month, budget=1000.0)
    print(f"✅ Created campaign: {campaign.name}")
    print(f"   Theme: {campaign.theme}")
    print(f"   Budget: ${campaign.budget}")
    print(f"   Expected Revenue: ${campaign.expected_revenue}")
    print(f"   Recipes Generated: {len(campaign.recipes)}")
    
    print(f"\n🎉 AI Recipe Generator is ready to generate revenue!")
    print(f"💡 Next steps:")
    print(f"   1. Set up affiliate programs")
    print(f"   2. Create website/blog")
    print(f"   3. Generate content daily")
    print(f"   4. Optimize for SEO")
    print(f"   5. Scale to $10K+ monthly!")

if __name__ == "__main__":
    main()