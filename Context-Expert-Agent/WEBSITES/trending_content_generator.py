#!/usr/bin/env python3
"""
Trending Content Generator - AI-powered SEO content creation
Generates high-ranking content for trending keywords
"""

import os
import json
import sqlite3
import requests
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import openai
from bs4 import BeautifulSoup
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TrendingKeyword:
    """Trending keyword data structure"""
    keyword: str
    search_volume: int
    difficulty: int
    cpc: float
    trend_score: float
    competition: str
    related_keywords: List[str]
    search_intent: str
    last_updated: str

@dataclass
class SEOContent:
    """SEO-optimized content structure"""
    id: str
    title: str
    meta_description: str
    content: str
    target_keyword: str
    secondary_keywords: List[str]
    word_count: int
    readability_score: float
    seo_score: float
    internal_links: List[str]
    external_links: List[str]
    images: List[str]
    schema_markup: str
    created_at: str

class TrendingContentGenerator:
    """AI-powered trending content generator"""
    
    def __init__(self, db_path: str = "databases/content.db"):
        self.db_path = db_path
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.trending_keywords = self._load_trending_keywords()
        self._init_database()
        
    def _load_trending_keywords(self) -> List[TrendingKeyword]:
        """Load trending keywords from database or API"""
        # This would typically load from a keyword research database
        # For now, we'll use hardcoded trending keywords
        return [
            TrendingKeyword(
                keyword="AI content generation",
                search_volume=2400000,
                difficulty=65,
                cpc=2.50,
                trend_score=95.0,
                competition="high",
                related_keywords=["AI writing tools", "automated content", "AI copywriting"],
                search_intent="commercial",
                last_updated=datetime.now().isoformat()
            ),
            TrendingKeyword(
                keyword="AI art generator",
                search_volume=3200000,
                difficulty=70,
                cpc=3.20,
                trend_score=98.0,
                competition="high",
                related_keywords=["AI image generator", "DALL-E", "Midjourney"],
                search_intent="commercial",
                last_updated=datetime.now().isoformat()
            ),
            TrendingKeyword(
                keyword="AI video creation",
                search_volume=1800000,
                difficulty=75,
                cpc=4.50,
                trend_score=92.0,
                competition="very high",
                related_keywords=["Sora", "Runway", "AI video editing"],
                search_intent="commercial",
                last_updated=datetime.now().isoformat()
            ),
            TrendingKeyword(
                keyword="passive income AI",
                search_volume=1400000,
                difficulty=60,
                cpc=2.80,
                trend_score=88.0,
                competition="medium",
                related_keywords=["AI side hustle", "AI business", "automated income"],
                search_intent="commercial",
                last_updated=datetime.now().isoformat()
            ),
            TrendingKeyword(
                keyword="creative AI tools",
                search_volume=1200000,
                difficulty=55,
                cpc=2.20,
                trend_score=85.0,
                competition="medium",
                related_keywords=["AI design tools", "creative automation", "AI creativity"],
                search_intent="informational",
                last_updated=datetime.now().isoformat()
            )
        ]
    
    def _init_database(self):
        """Initialize content database"""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Content table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS seo_content (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    meta_description TEXT,
                    content TEXT,
                    target_keyword TEXT,
                    secondary_keywords TEXT,
                    word_count INTEGER,
                    readability_score REAL,
                    seo_score REAL,
                    internal_links TEXT,
                    external_links TEXT,
                    images TEXT,
                    schema_markup TEXT,
                    created_at TEXT
                )
            ''')
            
            # Keywords table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trending_keywords (
                    keyword TEXT PRIMARY KEY,
                    search_volume INTEGER,
                    difficulty INTEGER,
                    cpc REAL,
                    trend_score REAL,
                    competition TEXT,
                    related_keywords TEXT,
                    search_intent TEXT,
                    last_updated TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Content database initialized")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    def generate_trending_content(self, keyword: str, content_type: str = "blog_post") -> SEOContent:
        """Generate SEO-optimized content for trending keyword"""
        try:
            # Find keyword data
            keyword_data = next((k for k in self.trending_keywords if k.keyword == keyword), None)
            if not keyword_data:
                logger.error(f"Keyword {keyword} not found in trending keywords")
                return None
            
            # Generate content based on type
            if content_type == "blog_post":
                return self._generate_blog_post(keyword_data)
            elif content_type == "article":
                return self._generate_article(keyword_data)
            elif content_type == "video_script":
                return self._generate_video_script(keyword_data)
            elif content_type == "social_media":
                return self._generate_social_content(keyword_data)
            else:
                logger.error(f"Unsupported content type: {content_type}")
                return None
                
        except Exception as e:
            logger.error(f"Content generation failed: {e}")
            return None
    
    def _generate_blog_post(self, keyword_data: TrendingKeyword) -> SEOContent:
        """Generate SEO-optimized blog post"""
        try:
            # Generate title
            title = self._generate_seo_title(keyword_data.keyword, keyword_data.related_keywords)
            
            # Generate meta description
            meta_description = self._generate_meta_description(keyword_data.keyword, title)
            
            # Generate content
            content = self._generate_blog_content(keyword_data)
            
            # Calculate metrics
            word_count = len(content.split())
            readability_score = self._calculate_readability(content)
            seo_score = self._calculate_seo_score(content, keyword_data.keyword)
            
            # Generate internal and external links
            internal_links = self._generate_internal_links(keyword_data.keyword)
            external_links = self._generate_external_links(keyword_data.keyword)
            
            # Generate images
            images = self._generate_image_suggestions(keyword_data.keyword)
            
            # Generate schema markup
            schema_markup = self._generate_schema_markup(keyword_data.keyword, title, content)
            
            content_id = f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            seo_content = SEOContent(
                id=content_id,
                title=title,
                meta_description=meta_description,
                content=content,
                target_keyword=keyword_data.keyword,
                secondary_keywords=keyword_data.related_keywords,
                word_count=word_count,
                readability_score=readability_score,
                seo_score=seo_score,
                internal_links=internal_links,
                external_links=external_links,
                images=images,
                schema_markup=schema_markup,
                created_at=datetime.now().isoformat()
            )
            
            # Save to database
            self._save_content(seo_content)
            
            return seo_content
            
        except Exception as e:
            logger.error(f"Blog post generation failed: {e}")
            return None
    
    def _generate_seo_title(self, keyword: str, related_keywords: List[str]) -> str:
        """Generate SEO-optimized title"""
        try:
            prompt = f"""
            Create an SEO-optimized title for a blog post about "{keyword}".
            Related keywords: {', '.join(related_keywords)}
            
            Requirements:
            - Include the main keyword naturally
            - 50-60 characters long
            - Compelling and click-worthy
            - Include a number or power word if relevant
            - Make it specific and valuable
            
            Generate 5 title options:
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert SEO copywriter specializing in high-converting titles."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            titles = response.choices[0].message.content.strip().split('\n')
            # Return the first title (you could implement logic to choose the best one)
            return titles[0].strip('- ').strip()
            
        except Exception as e:
            logger.error(f"Title generation failed: {e}")
            return f"The Ultimate Guide to {keyword.title()}"
    
    def _generate_meta_description(self, keyword: str, title: str) -> str:
        """Generate SEO-optimized meta description"""
        try:
            prompt = f"""
            Create an SEO-optimized meta description for a blog post.
            Title: "{title}"
            Main keyword: "{keyword}"
            
            Requirements:
            - 150-160 characters long
            - Include the main keyword naturally
            - Compelling call-to-action
            - Summarize the value proposition
            - Include a power word or emotional trigger
            
            Generate 3 meta description options:
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert SEO copywriter specializing in meta descriptions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            descriptions = response.choices[0].message.content.strip().split('\n')
            return descriptions[0].strip('- ').strip()
            
        except Exception as e:
            logger.error(f"Meta description generation failed: {e}")
            return f"Discover the best {keyword} strategies and tools. Learn how to create amazing content with AI. Read our comprehensive guide now!"
    
    def _generate_blog_content(self, keyword_data: TrendingKeyword) -> str:
        """Generate comprehensive blog post content"""
        try:
            prompt = f"""
            Write a comprehensive, SEO-optimized blog post about "{keyword_data.keyword}".
            
            Keyword data:
            - Search volume: {keyword_data.search_volume:,}
            - Difficulty: {keyword_data.difficulty}/100
            - Related keywords: {', '.join(keyword_data.related_keywords)}
            - Search intent: {keyword_data.search_intent}
            
            Requirements:
            - 2000+ words
            - Include the main keyword 8-10 times naturally
            - Include related keywords throughout
            - Use proper heading structure (H1, H2, H3)
            - Include actionable tips and examples
            - Add internal linking opportunities
            - Make it engaging and valuable
            - Include a compelling introduction and conclusion
            - Add FAQ section if relevant
            
            Structure:
            1. Compelling introduction
            2. What is [keyword]?
            3. Why is it important?
            4. How to get started
            5. Best tools and resources
            6. Common mistakes to avoid
            7. Advanced strategies
            8. FAQ section
            9. Conclusion with call-to-action
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert content writer and SEO specialist. Write engaging, informative, and SEO-optimized content that ranks well in search engines."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Content generation failed: {e}")
            return f"# {keyword_data.keyword.title()}\n\nThis is a comprehensive guide about {keyword_data.keyword}..."
    
    def _calculate_readability(self, content: str) -> float:
        """Calculate content readability score"""
        try:
            # Simple readability calculation (Flesch Reading Ease approximation)
            sentences = len(re.findall(r'[.!?]+', content))
            words = len(content.split())
            syllables = len(re.findall(r'[aeiouAEIOU]', content))
            
            if sentences == 0 or words == 0:
                return 0.0
            
            score = 206.835 - (1.015 * (words / sentences)) - (84.6 * (syllables / words))
            return max(0, min(100, score))
            
        except Exception as e:
            logger.error(f"Readability calculation failed: {e}")
            return 50.0
    
    def _calculate_seo_score(self, content: str, keyword: str) -> float:
        """Calculate SEO score for content"""
        try:
            score = 0.0
            content_lower = content.lower()
            keyword_lower = keyword.lower()
            
            # Keyword density (2-3% is optimal)
            keyword_count = content_lower.count(keyword_lower)
            word_count = len(content.split())
            density = (keyword_count / word_count) * 100
            
            if 2 <= density <= 3:
                score += 20
            elif 1 <= density < 2 or 3 < density <= 4:
                score += 15
            else:
                score += 10
            
            # Title contains keyword
            if keyword_lower in content_lower[:100]:  # First 100 characters
                score += 15
            
            # Proper heading structure
            h1_count = len(re.findall(r'<h1[^>]*>', content, re.IGNORECASE))
            h2_count = len(re.findall(r'<h2[^>]*>', content, re.IGNORECASE))
            
            if h1_count == 1:
                score += 10
            if h2_count >= 3:
                score += 15
            
            # Content length (2000+ words is good)
            if word_count >= 2000:
                score += 20
            elif word_count >= 1500:
                score += 15
            elif word_count >= 1000:
                score += 10
            
            # Internal links
            internal_links = len(re.findall(r'href=["\'](?!http)', content, re.IGNORECASE))
            if internal_links >= 3:
                score += 10
            elif internal_links >= 1:
                score += 5
            
            # External links
            external_links = len(re.findall(r'href=["\']https?://', content, re.IGNORECASE))
            if external_links >= 2:
                score += 10
            elif external_links >= 1:
                score += 5
            
            return min(100, score)
            
        except Exception as e:
            logger.error(f"SEO score calculation failed: {e}")
            return 50.0
    
    def _generate_internal_links(self, keyword: str) -> List[str]:
        """Generate internal linking suggestions"""
        # This would typically analyze your site structure
        return [
            "/ai-content-tools",
            "/content-automation-guide",
            "/ai-marketing-strategies"
        ]
    
    def _generate_external_links(self, keyword: str) -> List[str]:
        """Generate external linking suggestions"""
        # This would typically research authoritative sources
        return [
            "https://openai.com",
            "https://www.anthropic.com",
            "https://huggingface.co"
        ]
    
    def _generate_image_suggestions(self, keyword: str) -> List[str]:
        """Generate image suggestions for content"""
        return [
            f"{keyword.replace(' ', '-')}-infographic.png",
            f"{keyword.replace(' ', '-')}-workflow-diagram.png",
            f"{keyword.replace(' ', '-')}-tools-comparison.png"
        ]
    
    def _generate_schema_markup(self, keyword: str, title: str, content: str) -> str:
        """Generate schema markup for content"""
        schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": content[:200] + "...",
            "author": {
                "@type": "Organization",
                "name": "Creative AI Empire"
            },
            "publisher": {
                "@type": "Organization",
                "name": "Creative AI Empire"
            },
            "datePublished": datetime.now().isoformat(),
            "dateModified": datetime.now().isoformat(),
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"https://creativeaiempire.com/{keyword.replace(' ', '-')}"
            }
        }
        
        return json.dumps(schema, indent=2)
    
    def _save_content(self, content: SEOContent):
        """Save content to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO seo_content 
                (id, title, meta_description, content, target_keyword, secondary_keywords,
                 word_count, readability_score, seo_score, internal_links, external_links,
                 images, schema_markup, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                content.id, content.title, content.meta_description, content.content,
                content.target_keyword, json.dumps(content.secondary_keywords),
                content.word_count, content.readability_score, content.seo_score,
                json.dumps(content.internal_links), json.dumps(content.external_links),
                json.dumps(content.images), content.schema_markup, content.created_at
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Content {content.id} saved to database")
            
        except Exception as e:
            logger.error(f"Failed to save content: {e}")
    
    def batch_generate_content(self, keywords: List[str], content_type: str = "blog_post") -> List[SEOContent]:
        """Generate content for multiple keywords"""
        results = []
        
        for keyword in keywords:
            content = self.generate_trending_content(keyword, content_type)
            if content:
                results.append(content)
        
        return results
    
    def get_content_performance(self) -> Dict[str, Any]:
        """Get content performance analytics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get content statistics
            cursor.execute('SELECT COUNT(*) FROM seo_content')
            total_content = cursor.fetchone()[0]
            
            cursor.execute('SELECT AVG(seo_score) FROM seo_content')
            avg_seo_score = cursor.fetchone()[0] or 0
            
            cursor.execute('SELECT AVG(readability_score) FROM seo_content')
            avg_readability = cursor.fetchone()[0] or 0
            
            cursor.execute('SELECT AVG(word_count) FROM seo_content')
            avg_word_count = cursor.fetchone()[0] or 0
            
            conn.close()
            
            return {
                "total_content": total_content,
                "average_seo_score": round(avg_seo_score, 2),
                "average_readability": round(avg_readability, 2),
                "average_word_count": round(avg_word_count, 0)
            }
            
        except Exception as e:
            logger.error(f"Failed to get performance data: {e}")
            return {}

# Example usage
def main():
    """Example usage of Trending Content Generator"""
    generator = TrendingContentGenerator()
    
    # Generate content for trending keywords
    trending_keywords = ["AI content generation", "AI art generator", "passive income AI"]
    
    for keyword in trending_keywords:
        content = generator.generate_trending_content(keyword, "blog_post")
        if content:
            print(f"Generated content for '{keyword}':")
            print(f"  Title: {content.title}")
            print(f"  Word count: {content.word_count}")
            print(f"  SEO score: {content.seo_score}")
            print(f"  Readability: {content.readability_score}")
            print()
    
    # Get performance analytics
    performance = generator.get_content_performance()
    print("Content Performance:")
    for key, value in performance.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    main()