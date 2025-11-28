#!/usr/bin/env python3
"""
🔥 HOT TRENDING CONTENT ENGINE
Discovers top 1-5% hot rising trends and generates SEO-optimized content

Features:
- Real-time trend discovery (Grok for Twitter/X, Perplexity for search)
- Rising keyword identification (before they peak)
- Content generation optimized for hot trends
- Multi-platform intelligence (YouTube, Google, Twitter, Reddit)
- Predictive trend analysis (what's about to blow up)
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import subprocess

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from openai import OpenAI
    import groq
    import anthropic
    import google.generativeai as genai
except ImportError:
    print("Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "openai", "groq", "anthropic", "google-generativeai"])
    from openai import OpenAI
    import groq
    import anthropic
    import google.generativeai as genai


@dataclass
class HotTrend:
    """Hot trending topic with intelligence"""
    keyword: str
    trend_score: float  # 0-100, higher = hotter
    growth_rate: float  # % growth in last 24-48 hours
    competition: str  # "low", "medium", "high"
    search_volume: int
    platforms: List[str]  # Where it's trending
    related_keywords: List[str]
    content_opportunity: str
    estimated_peak_time: Optional[datetime] = None
    seo_potential: float = 0.0  # 0-100
    content_ideas: List[str] = field(default_factory=list)


@dataclass
class TrendingContentPackage:
    """Complete AEO/SEO-optimized content package for hot trend"""
    trend: HotTrend
    title: str
    description: str
    tags: List[str]
    hashtags: str  # Hashtag string for description
    script_outline: str
    thumbnail_concept: str
    publish_timing: str
    seo_score: float
    aeo_score: float  # Answer Engine Optimization score
    estimated_performance: Dict[str, float]
    keyword_density: Dict[str, float]  # Keyword usage analysis
    related_keywords: List[str]  # Semantic keywords for AEO


class HotTrendingContentEngine:
    """Discovers and generates content for hot trending topics"""
    
    def __init__(self):
        # Initialize AI clients
        self.grok_client = None
        self.groq_client = None
        self.claude = None
        self.gemini = None
        self.perplexity = None
        
        if os.getenv('XAI_API_KEY'):
            self.grok_client = OpenAI(
                api_key=os.getenv('XAI_API_KEY'),
                base_url="https://api.x.ai/v1"
            )
        
        if os.getenv('GROQ_API_KEY'):
            self.groq_client = groq.Groq(api_key=os.getenv('GROQ_API_KEY'))
        
        if os.getenv('ANTHROPIC_API_KEY'):
            self.claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        if os.getenv('GEMINI_API_KEY'):
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            self.gemini = genai
        
        # Cache for trending data
        self.trend_cache: Dict[str, Dict] = {}
        self.last_update = None
    
    def discover_hot_trends(
        self,
        niche: str = "content creation, AI, music, art, automation",
        min_trend_score: float = 75.0,
        max_results: int = 10
    ) -> List[HotTrend]:
        """Discover hot trending topics across multiple platforms"""
        
        print("🔥 DISCOVERING HOT TRENDING TOPICS")
        print("="*70)
        print(f"Niches: {niche}")
        print(f"Minimum Trend Score: {min_trend_score}")
        print()
        
        trends = []
        
        # 1. Real-time Twitter/X trends (Grok)
        print("1️⃣  Analyzing Twitter/X trends (Grok)...")
        twitter_trends = self._get_twitter_trends(niche)
        
        # 2. Google Search trends (Perplexity/Gemini)
        print("2️⃣  Analyzing Google Search trends...")
        google_trends = self._get_google_trends(niche)
        
        # 3. YouTube trending (Gemini/Groq)
        print("3️⃣  Analyzing YouTube trends...")
        youtube_trends = self._get_youtube_trends(niche)
        
        # 4. Reddit rising (Groq)
        print("4️⃣  Analyzing Reddit rising topics...")
        reddit_trends = self._get_reddit_trends(niche)
        
        # Combine and score all trends
        print("\n5️⃣  Scoring and ranking trends...")
        all_trends = self._combine_and_score_trends(
            twitter_trends, google_trends, youtube_trends, reddit_trends
        )
        
        # Filter by minimum score
        hot_trends = [t for t in all_trends if t.trend_score >= min_trend_score]
        
        # Sort by trend score
        hot_trends.sort(key=lambda x: x.trend_score, reverse=True)
        
        # Limit results
        hot_trends = hot_trends[:max_results]
        
        print(f"\n✅ Found {len(hot_trends)} hot trending topics (score >= {min_trend_score})")
        print()
        
        return hot_trends
    
    def _get_twitter_trends(self, niche: str) -> List[Dict[str, Any]]:
        """Get real-time Twitter/X trends using Grok"""
        if not self.grok_client:
            return []
        
        try:
            prompt = f"""Analyze current Twitter/X trends related to: {niche}

Identify:
1. Hot trending topics (last 24 hours)
2. Rising keywords (growing fast)
3. Viral content themes
4. Emerging discussions

For each trend, provide:
- Keyword/phrase
- Growth rate estimate (%)
- Why it's trending
- Content opportunity

Output as JSON array: [{{"keyword": "...", "growth": 85, "reason": "...", "opportunity": "..."}}]"""
            
            response = self.grok_client.chat.completions.create(
                model="grok-beta",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            
            # Extract JSON
            try:
                # Try to parse as JSON
                if '```json' in content:
                    json_start = content.find('```json') + 7
                    json_end = content.find('```', json_start)
                    content = content[json_start:json_end].strip()
                elif '```' in content:
                    json_start = content.find('```') + 3
                    json_end = content.find('```', json_start)
                    content = content[json_start:json_end].strip()
                
                trends = json.loads(content)
                return trends if isinstance(trends, list) else []
            except:
                # Fallback: parse manually
                return self._parse_trends_from_text(content)
        except Exception as e:
            print(f"   ⚠️  Grok error: {e}")
            return []
    
    def _get_google_trends(self, niche: str) -> List[Dict[str, Any]]:
        """Get Google Search trends using Gemini/Perplexity"""
        trends = []
        
        # Try Gemini first
        if self.gemini:
            try:
                model = self.gemini.GenerativeModel('gemini-2.0-flash-exp')
                prompt = f"""What are the hottest rising search trends on Google right now related to: {niche}

Focus on:
- Topics with rapid growth (last 48 hours)
- Low competition keywords
- Emerging search queries
- Seasonal trends

Output as JSON: [{{"keyword": "...", "growth": 90, "competition": "low", "volume": 10000}}]"""
                
                response = model.generate_content(prompt)
                content = response.text
                
                try:
                    if '```json' in content:
                        json_start = content.find('```json') + 7
                        json_end = content.find('```', json_start)
                        content = content[json_start:json_end].strip()
                    
                    trends = json.loads(content)
                    if not isinstance(trends, list):
                        trends = []
                except:
                    trends = self._parse_trends_from_text(content)
            except Exception as e:
                print(f"   ⚠️  Gemini error: {e}")
        
        # Fallback to Groq
        if not trends and self.groq_client:
            try:
                prompt = f"""What are hot Google search trends for: {niche}

Output JSON: [{{"keyword": "...", "growth": 80, "competition": "low"}}]"""
                
                response = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                
                content = response.choices[0].message.content
                trends = self._parse_trends_from_text(content)
            except:
                pass
        
        return trends
    
    def _get_youtube_trends(self, niche: str) -> List[Dict[str, Any]]:
        """Get YouTube trending topics"""
        if not self.groq_client:
            return []
        
        try:
            prompt = f"""What are hot trending topics on YouTube right now related to: {niche}

Focus on:
- Videos with rapid view growth
- Topics with low competition
- Emerging content categories
- Viral video themes

Output JSON: [{{"keyword": "...", "growth": 85, "views_trend": "rising"}}]"""
            
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return self._parse_trends_from_text(content)
        except:
            return []
    
    def _get_reddit_trends(self, niche: str) -> List[Dict[str, Any]]:
        """Get Reddit rising topics"""
        if not self.groq_client:
            return []
        
        try:
            prompt = f"""What are hot rising topics on Reddit related to: {niche}

Focus on:
- Posts with rapid upvote growth
- Topics gaining traction
- Emerging discussions
- Viral content themes

Output JSON: [{{"keyword": "...", "growth": 80, "upvotes_trend": "rising"}}]"""
            
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return self._parse_trends_from_text(content)
        except:
            return []
    
    def _parse_trends_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Parse trends from AI response text"""
        trends = []
        
        # Try to extract structured data
        lines = text.split('\n')
        current_trend = {}
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Look for keyword patterns
            if 'keyword' in line.lower() or 'topic' in line.lower():
                # Extract keyword
                if ':' in line:
                    keyword = line.split(':', 1)[1].strip().strip('"\'')
                    if keyword:
                        if current_trend:
                            trends.append(current_trend)
                        current_trend = {'keyword': keyword}
            
            # Look for growth/score
            if 'growth' in line.lower() or 'score' in line.lower():
                if ':' in line:
                    try:
                        value = float(line.split(':', 1)[1].strip().rstrip('%'))
                        current_trend['growth'] = value
                    except:
                        pass
        
        if current_trend:
            trends.append(current_trend)
        
        # If no structured data, extract keywords from text
        if not trends:
            # Look for quoted phrases or capitalized words
            import re
            keywords = re.findall(r'"([^"]+)"', text)
            keywords.extend(re.findall(r"'([^']+)'", text))
            
            for keyword in keywords[:10]:  # Limit to 10
                if len(keyword) > 3 and len(keyword) < 50:
                    trends.append({
                        'keyword': keyword,
                        'growth': 75.0,  # Default
                        'competition': 'medium'
                    })
        
        return trends
    
    def _combine_and_score_trends(
        self,
        twitter: List[Dict],
        google: List[Dict],
        youtube: List[Dict],
        reddit: List[Dict]
    ) -> List[HotTrend]:
        """Combine trends from all platforms and calculate scores"""
        
        # Count occurrences across platforms
        keyword_data = defaultdict(lambda: {
            'platforms': [],
            'growth_rates': [],
            'competition': 'medium',
            'search_volume': 0,
            'mentions': 0
        })
        
        # Process Twitter trends
        for trend in twitter:
            keyword = trend.get('keyword', '').lower().strip()
            if keyword:
                keyword_data[keyword]['platforms'].append('twitter')
                keyword_data[keyword]['growth_rates'].append(trend.get('growth', 75))
                keyword_data[keyword]['mentions'] += 1
        
        # Process Google trends
        for trend in google:
            keyword = trend.get('keyword', '').lower().strip()
            if keyword:
                keyword_data[keyword]['platforms'].append('google')
                keyword_data[keyword]['growth_rates'].append(trend.get('growth', 75))
                keyword_data[keyword]['competition'] = trend.get('competition', 'medium')
                keyword_data[keyword]['search_volume'] = trend.get('volume', 0)
                keyword_data[keyword]['mentions'] += 1
        
        # Process YouTube trends
        for trend in youtube:
            keyword = trend.get('keyword', '').lower().strip()
            if keyword:
                keyword_data[keyword]['platforms'].append('youtube')
                keyword_data[keyword]['growth_rates'].append(trend.get('growth', 75))
                keyword_data[keyword]['mentions'] += 1
        
        # Process Reddit trends
        for trend in reddit:
            keyword = trend.get('keyword', '').lower().strip()
            if keyword:
                keyword_data[keyword]['platforms'].append('reddit')
                keyword_data[keyword]['growth_rates'].append(trend.get('growth', 75))
                keyword_data[keyword]['mentions'] += 1
        
        # Convert to HotTrend objects
        hot_trends = []
        
        for keyword, data in keyword_data.items():
            # Calculate trend score
            # Base score from average growth
            avg_growth = sum(data['growth_rates']) / len(data['growth_rates']) if data['growth_rates'] else 50
            
            # Multi-platform bonus (trending on multiple platforms = hotter)
            platform_bonus = len(set(data['platforms'])) * 5
            
            # Mention bonus (mentioned multiple times = hotter)
            mention_bonus = min(data['mentions'] * 3, 15)
            
            # Competition penalty (high competition = harder to rank)
            competition_penalty = {
                'low': 0,
                'medium': -5,
                'high': -15
            }.get(data['competition'], -5)
            
            # Calculate final score
            trend_score = avg_growth + platform_bonus + mention_bonus + competition_penalty
            trend_score = min(100, max(0, trend_score))
            
            # Only include if score is significant
            if trend_score >= 60:
                hot_trend = HotTrend(
                    keyword=keyword.title(),
                    trend_score=trend_score,
                    growth_rate=avg_growth,
                    competition=data['competition'],
                    search_volume=data['search_volume'],
                    platforms=list(set(data['platforms'])),
                    related_keywords=[],
                    content_opportunity=f"Hot trending on {', '.join(set(data['platforms']))}",
                    seo_potential=self._calculate_seo_potential(keyword, data)
                )
                
                hot_trends.append(hot_trend)
        
        return hot_trends
    
    def _calculate_seo_potential(self, keyword: str, data: Dict) -> float:
        """Calculate SEO ranking potential (0-100)"""
        score = 50.0  # Base score
        
        # Competition factor
        if data['competition'] == 'low':
            score += 30
        elif data['competition'] == 'medium':
            score += 15
        
        # Multi-platform factor (trending everywhere = easier to rank)
        if len(set(data['platforms'])) >= 3:
            score += 20
        
        # Search volume factor
        if data['search_volume'] > 10000:
            score += 10
        elif data['search_volume'] > 5000:
            score += 5
        
        return min(100, score)
    
    def generate_trending_content(
        self,
        trend: HotTrend,
        content_type: str = "youtube",
        use_assets: bool = True
    ) -> TrendingContentPackage:
        """Generate complete content package for hot trend"""
        
        print(f"\n🎬 GENERATING CONTENT FOR: {trend.keyword}")
        print(f"   Trend Score: {trend.trend_score:.1f}/100")
        print(f"   Growth Rate: {trend.growth_rate:.1f}%")
        print(f"   Platforms: {', '.join(trend.platforms)}")
        print()
        
        # Generate optimized title
        title = self._generate_trending_title(trend, content_type)
        
        # Generate description
        description = self._generate_trending_description(trend, title, content_type)
        
        # Generate tags (AEO/SEO optimized)
        tags = self._generate_trending_tags(trend, content_type)
        
        # Generate hashtags
        hashtags = self._generate_hashtags(trend, content_type)
        
        # Generate script outline (engaging + AEO optimized)
        script_outline = self._generate_script_outline(trend, content_type)
        
        # Generate thumbnail concept (CTR optimized)
        thumbnail_concept = self._generate_thumbnail_concept(trend, content_type)
        
        # Determine publish timing
        publish_timing = self._determine_publish_timing(trend)
        
        # Calculate SEO score
        seo_score = self._calculate_content_seo_score(title, description, tags, trend)
        
        # Calculate AEO score (Answer Engine Optimization)
        aeo_score = self._calculate_aeo_score(title, description, trend)
        
        # Analyze keyword density
        keyword_density = self._analyze_keyword_density(description, trend)
        
        # Generate related keywords for AEO
        related_keywords = self._generate_related_keywords(trend, content_type)
        
        # Estimate performance (with AEO)
        estimated_performance = self._estimate_performance(trend, seo_score, aeo_score)
        
        package = TrendingContentPackage(
            trend=trend,
            title=title,
            description=description,
            tags=tags,
            hashtags=hashtags,
            script_outline=script_outline,
            thumbnail_concept=thumbnail_concept,
            publish_timing=publish_timing,
            seo_score=seo_score,
            aeo_score=aeo_score,
            estimated_performance=estimated_performance,
            keyword_density=keyword_density,
            related_keywords=related_keywords
        )
        
        return package
    
    def _generate_trending_title(self, trend: HotTrend, content_type: str) -> str:
        """Generate AEO/SEO-optimized, engaging, entertaining title for hot trend"""
        
        keyword = trend.keyword.lower()
        
        # Power words for maximum engagement
        power_words = [
            "EXPLAINED", "ULTIMATE", "COMPLETE", "BEST", "TOP", "INSANE", "MIND-BLOWING",
            "GAME-CHANGING", "REVOLUTIONARY", "BREAKTHROUGH", "SECRET", "HIDDEN",
            "SHOCKING", "UNBELIEVABLE", "INCREDIBLE", "AMAZING", "EPIC", "LEGENDARY"
        ]
        
        # Emotional triggers
        emotional_words = [
            "You NEED to See This", "This Will Change Everything", "You Won't Believe",
            "This is INSANE", "Watch This NOW", "Don't Miss This", "This is HUGE"
        ]
        
        # Trending indicators
        trending_indicators = [
            "🔥 HOT TRENDING", "📈 RISING FAST", "⚡ GOING VIRAL", "🚀 EXPLODING",
            "💥 BLOWING UP", "✨ TRENDING NOW", "🎯 HOT RIGHT NOW"
        ]
        
        # Use AI to generate best title with AEO/SEO optimization
        if self.groq_client:
            try:
                prompt = f"""Create a VIRAL, ENGAGING, ENTERTAINING YouTube title for hot trending topic: {trend.keyword}

CRITICAL REQUIREMENTS:
1. AEO/SEO OPTIMIZED:
   - Primary keyword "{trend.keyword}" in first 40 characters
   - Include 2-3 related trending keywords
   - Answer-focused (what, why, how questions)
   - Long-tail keyword variations

2. MAXIMUM ENGAGEMENT:
   - Use power words: {', '.join(power_words[:5])}
   - Include emotional triggers: {', '.join(emotional_words[:3])}
   - Add trending indicators: {', '.join(trending_indicators[:2])}
   - Create curiosity gap (make them click)

3. ENTERTAINING & CLICK-WORTHY:
   - Numbers/specificity (if applicable)
   - Questions that demand answers
   - Bold claims (but accurate)
   - Urgency (NOW, TODAY, 2025)

4. TECHNICAL:
   - Exactly 55-60 characters (optimal for YouTube)
   - Primary keyword in first 40 chars
   - Include trending year: 2025
   - Use | or : for separation

Trend Intelligence:
- Growth rate: {trend.growth_rate:.1f}% (EXTREMELY HOT)
- Platforms: {', '.join(trend.platforms)}
- Competition: {trend.competition}
- SEO Potential: {trend.seo_potential:.1f}/100

Generate 3 title options, then pick the BEST one. Output ONLY the final title."""
                
                response = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.9,  # Higher creativity for engaging titles
                    max_tokens=150
                )
                
                ai_title = response.choices[0].message.content.strip().strip('"\'')
                
                # Clean up if multiple options provided
                if '\n' in ai_title:
                    lines = [l.strip() for l in ai_title.split('\n') if l.strip()]
                    ai_title = lines[-1]  # Take last one (usually the selected)
                
                # Validate
                if len(ai_title) <= 60 and trend.keyword.lower() in ai_title.lower():
                    return ai_title
            except Exception as e:
                print(f"   ⚠️  AI title generation error: {e}")
        
        # Fallback: Generate optimized title manually
        import random
        
        # Select power word
        power_word = random.choice(power_words)
        
        # Select emotional trigger
        emotional = random.choice(emotional_words)
        
        # Select trending indicator
        trending = random.choice(trending_indicators)
        
        # Generate title variations
        templates = [
            f"{trending} {trend.keyword} {power_word} | {emotional}",
            f"{trend.keyword} {power_word} 2025 | {emotional}",
            f"{emotional}: {trend.keyword} {power_word}",
            f"{trend.keyword} | {power_word} Guide {trending}",
            f"Why {trend.keyword} is {power_word} RIGHT NOW"
        ]
        
        title = random.choice(templates)
        
        # Ensure optimal length
        if len(title) > 60:
            # Try shorter version
            title = f"{trend.keyword} {power_word} 2025 | {emotional[:20]}"
            if len(title) > 60:
                title = f"{trend.keyword} {power_word} | {trending}"
        
        # Final length check
        if len(title) > 60:
            title = title[:57] + "..."
        
        return title
    
    def _generate_trending_description(self, trend: HotTrend, title: str, content_type: str) -> str:
        """Generate AEO/SEO-optimized, engaging description with hashtags"""
        
        if self.groq_client:
            try:
                prompt = f"""Create a VIRAL, ENGAGING, SEO/AEO-optimized YouTube description for hot trending topic: {trend.keyword}

Title: {title}

CRITICAL REQUIREMENTS:

1. HOOK (First 125 characters - visible in search):
   - Must include primary keyword "{trend.keyword}"
   - Create immediate curiosity/urgency
   - Use emotional trigger
   - Answer "what is this?" immediately

2. AEO/SEO OPTIMIZATION:
   - Primary keyword: 5-7 times naturally
   - Related trending keywords: 3-5 times
   - Long-tail variations: 2-3 times
   - Answer common questions (what, why, how, when, where)
   - Include semantic keywords (related terms)
   - Keyword density: 3-5% (natural, not stuffed)

3. ENGAGING CONTENT (300-500 words):
   - Tell a story or create narrative
   - Use power words and emotional triggers
   - Include specific numbers/data
   - Create FOMO (fear of missing out)
   - Build excitement and urgency

4. STRUCTURE:
   - Hook paragraph (125 chars)
   - Value proposition (2-3 sentences)
   - Detailed explanation (3-4 paragraphs)
   - Key takeaways/bullet points
   - Timestamps/chapters (5-8 timestamps)
   - Call-to-action (subscribe, like, comment)
   - Links (playlists, related videos, social)

5. HASHTAGS (15-20 trending hashtags):
   - Primary keyword as hashtag
   - Trending year: #2025
   - Platform hashtags: #YouTube, #Trending
   - Niche hashtags (3-5)
   - Broad hashtags (2-3)
   - Trending topic hashtags (2-3)
   - Format: #KeywordNoSpaces

6. TRENDING OPTIMIZATION:
   - Growth rate: {trend.growth_rate:.1f}% (mention this!)
   - Platforms: {', '.join(trend.platforms)}
   - Competition: {trend.competition}
   - Include "trending now", "hot", "viral" naturally

Trend Intelligence:
- This is a TOP 1-5% hot trend
- Growing {trend.growth_rate:.1f}% daily
- Low competition: {trend.competition == 'low'}
- SEO potential: {trend.seo_potential:.1f}/100

Make it ENTERTAINING, ENGAGING, and SEO-PERFECT!"""
                
                response = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8,  # Creative but focused
                    max_tokens=1500
                )
                
                description = response.choices[0].message.content.strip()
                
                # Ensure hashtags are included
                if '#' not in description:
                    description += self._generate_hashtags(trend, content_type)
                
                return description
            except Exception as e:
                print(f"   ⚠️  AI description generation error: {e}")
        
        # Fallback: Generate optimized description manually
        hashtags = self._generate_hashtags(trend, content_type)
        
        description = f"""
{title}

🔥 {trend.keyword} is EXPLODING right now with {trend.growth_rate:.1f}% daily growth! This is a TOP 1-5% hot trending topic that's going viral across {', '.join(trend.platforms)}. Don't miss this - it's trending NOW!

📊 Why {trend.keyword} is HOT TRENDING:
• Growing {trend.growth_rate:.1f}% daily (extremely fast growth)
• Low competition ({trend.competition}) = easier to rank
• Multi-platform trending = massive opportunity
• Perfect timing to create content

🎯 What You'll Learn in This Video:
✅ What {trend.keyword} actually is (complete explanation)
✅ Why it's trending RIGHT NOW (the real reasons)
✅ How to leverage this trend (practical strategies)
✅ Key insights you need to know (expert analysis)
✅ Real examples and case studies (proof it works)

💡 Key Takeaways:
• {trend.keyword} is revolutionizing the industry
• Early adopters are seeing massive results
• This trend is here to stay (not just a fad)
• You can start using it today

⏱️ TIMESTAMPS / CHAPTERS:
0:00 - 🔥 Introduction: Why {trend.keyword} is HOT
0:30 - What is {trend.keyword}? (Complete Breakdown)
2:00 - Why It's Trending NOW (The Real Reasons)
4:00 - How {trend.keyword} Works (Deep Dive)
6:00 - Real Examples & Case Studies
8:00 - How to Use {trend.keyword} (Step-by-Step)
10:00 - Key Insights & Takeaways
11:30 - Conclusion & Next Steps

🎬 Related Videos:
• [Playlist: Hot Trending Topics 2025]
• [Video: How to Find Trending Topics]
• [Video: SEO Optimization Guide]

🔔 SUBSCRIBE for more hot trending content!
👍 LIKE if this helped you!
💬 COMMENT with your thoughts on {trend.keyword}!

📱 Connect With Us:
• Website: [Your website]
• Instagram: [Your Instagram]  
• Twitter: [Your Twitter]
• TikTok: [Your TikTok]

{hashtags}

---
⚠️ This content is about {trend.keyword}, a hot trending topic in 2025. Information is current as of {datetime.now().strftime('%B %d, %Y')}.
"""
        
        return description.strip()
    
    def _generate_hashtags(self, trend: HotTrend, content_type: str) -> List[str]:
        """Generate trending hashtags optimized for AEO/SEO"""
        hashtags = []
        
        # Primary keyword hashtag
        primary_hashtag = trend.keyword.replace(" ", "").replace("-", "")
        hashtags.append(f"#{primary_hashtag}")
        
        # Year hashtag (trending)
        hashtags.append("#2025")
        
        # Trending indicators
        hashtags.extend(["#Trending", "#TrendingNow", "#HotTrending", "#Viral", "#GoingViral"])
        
        # Platform hashtags
        if 'youtube' in trend.platforms:
            hashtags.append("#YouTube")
        if 'twitter' in trend.platforms:
            hashtags.extend(["#Twitter", "#X"])
        if 'reddit' in trend.platforms:
            hashtags.append("#Reddit")
        
        # Content type hashtags
        type_hashtags = {
            "music": ["#Music", "#NewMusic", "#Music2025", "#BackgroundMusic"],
            "art": ["#Art", "#DigitalArt", "#ArtPrint", "#WallArt"],
            "tutorial": ["#Tutorial", "#HowTo", "#Guide", "#Tips"],
            "case_study": ["#Results", "#CaseStudy", "#Success", "#Review"]
        }
        hashtags.extend(type_hashtags.get(content_type, ["#Content", "#Video"]))
        
        # Related keyword hashtags
        for related in trend.related_keywords[:5]:
            hashtag = related.replace(" ", "").replace("-", "")[:20]  # Limit length
            if hashtag:
                hashtags.append(f"#{hashtag}")
        
        # Broad trending hashtags
        hashtags.extend(["#TrendingTopic", "#HotRightNow", "#MustWatch", "#DontMiss"])
        
        # SEO hashtags (answer-focused)
        hashtags.extend(["#Explained", "#CompleteGuide", "#EverythingYouNeed"])
        
        # Remove duplicates and limit to 20
        unique_hashtags = list(dict.fromkeys(hashtags))[:20]
        
        return " ".join(unique_hashtags)
    
    def _generate_trending_tags(self, trend: HotTrend, content_type: str) -> List[str]:
        """Generate AEO/SEO-optimized tags for hot trend"""
        tags = []
        
        # PRIMARY KEYWORD (exact match - highest priority)
        tags.append(trend.keyword)
        
        # PRIMARY VARIATIONS (high priority)
        tags.append(f"{trend.keyword} 2025")
        tags.append(f"trending {trend.keyword}")
        tags.append(f"hot {trend.keyword}")
        tags.append(f"{trend.keyword} explained")
        tags.append(f"what is {trend.keyword}")
        tags.append(f"why {trend.keyword}")
        tags.append(f"how to {trend.keyword}")
        
        # LONG-TAIL KEYWORDS (AEO optimization - answer-focused)
        tags.append(f"{trend.keyword} complete guide")
        tags.append(f"{trend.keyword} tutorial")
        tags.append(f"{trend.keyword} review")
        tags.append(f"best {trend.keyword}")
        tags.append(f"{trend.keyword} tips")
        
        # TRENDING INDICATORS (trending optimization)
        tags.append("trending now")
        tags.append("hot trending")
        tags.append("viral trend")
        tags.append("trending 2025")
        tags.append("going viral")
        
        # PLATFORM-SPECIFIC (where it's trending)
        if 'youtube' in trend.platforms:
            tags.append("youtube trending")
            tags.append("youtube viral")
        if 'twitter' in trend.platforms:
            tags.append("twitter trending")
            tags.append("x trending")
        if 'google' in trend.platforms:
            tags.append("google trending")
            tags.append("search trending")
        if 'reddit' in trend.platforms:
            tags.append("reddit trending")
            tags.append("reddit viral")
        
        # CONTENT TYPE TAGS (niche-specific)
        type_tags = {
            "music": ["background music", "royalty free music", "cinematic music", "ambient music", "music 2025"],
            "art": ["digital art", "art print", "wall art", "modern art", "art 2025"],
            "tutorial": ["how to", "tutorial", "guide", "tips", "tutorial 2025"],
            "case_study": ["results", "case study", "success story", "review", "test"]
        }
        tags.extend(type_tags.get(content_type, ["content", "video", "trending content"]))
        
        # RELATED KEYWORDS (semantic SEO)
        tags.extend(trend.related_keywords[:5])
        
        # BROAD TRENDING TAGS (reach expansion)
        tags.extend(["trending topic", "viral content", "hot trend", "trending video"])
        
        # ANSWER-FOCUSED TAGS (AEO optimization)
        tags.extend([
            f"what is {trend.keyword}",
            f"why is {trend.keyword} trending",
            f"how does {trend.keyword} work",
            f"{trend.keyword} explained simply"
        ])
        
        # Remove duplicates, prioritize, and limit to 15 (YouTube optimal)
        unique_tags = []
        seen = set()
        
        # Priority order: primary > variations > long-tail > trending > broad
        priority_tags = [
            trend.keyword,  # Must include
            f"{trend.keyword} 2025",
            f"trending {trend.keyword}",
            f"hot {trend.keyword}",
            f"{trend.keyword} explained"
        ]
        
        for tag in priority_tags:
            if tag.lower() not in seen and len(tag) <= 30:  # YouTube tag limit
                unique_tags.append(tag)
                seen.add(tag.lower())
        
        # Add remaining tags
        for tag in tags:
            tag_lower = tag.lower()
            if tag_lower not in seen and len(tag) <= 30 and len(unique_tags) < 15:
                unique_tags.append(tag)
                seen.add(tag_lower)
        
        return unique_tags[:15]
    
    def _generate_script_outline(self, trend: HotTrend, content_type: str) -> str:
        """Generate engaging, entertaining script outline optimized for AEO/SEO"""
        
        if self.groq_client:
            try:
                prompt = f"""Create an ENTERTAINING, ENGAGING video script outline for hot trending topic: {trend.keyword}

CRITICAL REQUIREMENTS:

1. HOOK (0-15 seconds) - MUST BE CAPTIVATING:
   - Start with shocking/interesting fact about {trend.keyword}
   - Create immediate curiosity
   - Use emotional trigger
   - Mention it's trending NOW
   - Example: "You won't believe what's happening with {trend.keyword} right now..."

2. AEO/SEO OPTIMIZATION (Answer Engine Optimization):
   - Answer "What is {trend.keyword}?" clearly
   - Answer "Why is it trending?" with data
   - Answer "How does it work?" step-by-step
   - Answer "When should you use it?" with timing
   - Answer "Where is it used?" with examples

3. ENGAGING STRUCTURE:
   - Hook (0-15s) - Grab attention
   - What (15s-2min) - Clear explanation
   - Why Trending (2-4min) - The real reasons
   - How It Works (4-6min) - Deep dive
   - Examples (6-8min) - Real cases
   - How to Use (8-10min) - Practical steps
   - Key Takeaways (10-11min) - Summary
   - Conclusion (11-12min) - CTA

4. ENTERTAINMENT FACTORS:
   - Use storytelling
   - Include surprising facts
   - Add humor where appropriate
   - Create emotional connection
   - Build suspense

5. TRENDING OPTIMIZATION:
   - Emphasize it's HOT RIGHT NOW
   - Mention growth rate: {trend.growth_rate:.1f}%
   - Reference platforms: {', '.join(trend.platforms)}
   - Create urgency (don't miss this)

Trend Intelligence:
- Trend Score: {trend.trend_score:.1f}/100 (TOP 1-5%)
- Competition: {trend.competition}
- SEO Potential: {trend.seo_potential:.1f}/100

Make it VIRAL-WORTHY and SEO-PERFECT!"""
                
                response = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8,  # Creative but structured
                    max_tokens=1200
                )
                
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"   ⚠️  Script generation error: {e}")
        
        # Fallback: Enhanced outline
        return f"""
[🔥 HOOK - 0:00-0:15]
{trend.keyword} is EXPLODING with {trend.growth_rate:.1f}% daily growth! This is a TOP 1-5% hot trend that's going viral RIGHT NOW. You need to see this!

[📖 WHAT IS IT - 0:15-2:00]
Complete breakdown: What {trend.keyword} actually is, in simple terms. No fluff, just the facts.

[🚀 WHY TRENDING - 2:00-4:30]
The REAL reasons {trend.keyword} is blowing up:
• Factor 1: [Specific reason]
• Factor 2: [Specific reason]
• Factor 3: [Specific reason]
Data and proof included!

[⚙️ HOW IT WORKS - 4:30-7:00]
Deep dive into how {trend.keyword} actually works. Step-by-step explanation with examples.

[💡 REAL EXAMPLES - 7:00-9:00]
Case studies and real-world examples of {trend.keyword} in action. Proof it works!

[🎯 HOW TO USE - 9:00-11:00]
Practical step-by-step guide on how YOU can leverage {trend.keyword} right now.

[✅ KEY TAKEAWAYS - 11:00-11:30]
The 5 most important things you need to remember about {trend.keyword}.

[🎬 CONCLUSION - 11:30-12:00]
Don't miss out on this hot trend! Subscribe for more trending content, like if this helped, and comment your thoughts!
"""
    
    def _generate_thumbnail_concept(self, trend: HotTrend, content_type: str) -> str:
        """Generate engaging thumbnail concept optimized for CTR"""
        
        if self.groq_client:
            try:
                prompt = f"""Create a VIRAL thumbnail concept for hot trending topic: {trend.keyword}

Requirements:
- Eye-catching and click-worthy
- Bold, readable text (even at small size)
- Trending indicators (fire emoji, arrows, badges)
- Emotional trigger (shock, curiosity, excitement)
- Vibrant, high-contrast colors
- Trending year: 2025
- Platform: YouTube (16:9 aspect ratio)

Trend context:
- Growth: {trend.growth_rate:.1f}% (extremely hot)
- Competition: {trend.competition}
- Platforms: {', '.join(trend.platforms)}

Output detailed thumbnail concept description."""
                
                response = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8,
                    max_tokens=200
                )
                
                return response.choices[0].message.content.strip()
            except:
                pass
        
        # Fallback: Enhanced concept
        return f"""
THUMBNAIL CONCEPT for {trend.keyword}:

LAYOUT:
- Background: Vibrant gradient (hot colors - red/orange/yellow)
- Foreground: High-contrast text on semi-transparent dark overlay

TEXT ELEMENTS:
- Main text: "{trend.keyword}" in BOLD, large font (60% of thumbnail)
- Subtext: "HOT TRENDING 2025" in smaller bold font
- Badge: "🔥 #1 TRENDING" in top-right corner

VISUAL ELEMENTS:
- Trending arrow pointing up (green/red, animated feel)
- Fire emoji or flame graphics
- "NEW" or "2025" badge
- Eye-catching border or glow effect

COLORS:
- Primary: Hot red/orange gradient
- Text: White or bright yellow (high contrast)
- Accents: Green for "trending up" indicators

STYLE:
- Modern, clean, professional
- High contrast for mobile visibility
- Emotional trigger: Excitement, urgency, curiosity
- Optimized for 16:9 YouTube aspect ratio

DESIGN PRINCIPLES:
- Text readable at thumbnail size
- Single focal point (the keyword)
- Trending indicators clearly visible
- Creates "must-click" feeling
"""
    
    def _determine_publish_timing(self, trend: HotTrend) -> str:
        """Determine optimal publish timing"""
        # If growing fast, publish ASAP
        if trend.growth_rate > 85:
            return "PUBLISH IMMEDIATELY - Peak trending now!"
        elif trend.growth_rate > 75:
            return "Publish within 24 hours - Still rising"
        else:
            return "Publish within 48 hours - Good opportunity"
    
    def _calculate_content_seo_score(self, title: str, description: str, tags: List[str], trend: HotTrend) -> float:
        """Calculate AEO/SEO score for generated content"""
        score = 0.0
        
        keyword = trend.keyword.lower()
        title_lower = title.lower()
        desc_lower = description.lower()
        
        # TITLE OPTIMIZATION (35 points)
        # Primary keyword in title
        if keyword in title_lower:
            score += 20
            # In first 40 characters (optimal)
            if keyword in title_lower[:40]:
                score += 5
        
        # Optimal length (55-60 chars)
        if 55 <= len(title) <= 60:
            score += 10
        elif 50 <= len(title) < 55:
            score += 7
        elif len(title) < 50:
            score += 5
        
        # Power words
        power_words = ['explained', 'ultimate', 'complete', 'best', 'top', 'insane', 'secret']
        if any(pw in title_lower for pw in power_words):
            score += 5
        
        # DESCRIPTION OPTIMIZATION (45 points)
        # Keyword density (3-5% optimal)
        word_count = len(desc_lower.split())
        keyword_count = desc_lower.count(keyword)
        if word_count > 0:
            density = (keyword_count / word_count) * 100
            if 3 <= density <= 5:
                score += 15  # Perfect density
            elif 2 <= density < 3 or 5 < density <= 7:
                score += 10  # Good density
            elif density >= 1:
                score += 5  # Minimum
        
        # Keyword placement
        if keyword in desc_lower[:125]:  # First 125 chars (visible in search)
            score += 10
        
        # Length (300-500 words optimal)
        if 300 <= word_count <= 500:
            score += 10
        elif 200 <= word_count < 300:
            score += 7
        elif word_count >= 200:
            score += 5
        
        # AEO factors (answer-focused)
        question_words = ['what', 'why', 'how', 'when', 'where', 'who']
        if any(qw in desc_lower[:200] for qw in question_words):
            score += 5  # Answer-focused
        
        # Timestamps (engagement + SEO)
        if '0:00' in description or '00:00' in description:
            score += 5
        
        # TAGS OPTIMIZATION (15 points)
        tags_lower = [t.lower() for t in tags]
        
        # Primary keyword in tags
        if keyword in tags_lower:
            score += 5
        
        # Optimal count (10-15 tags)
        if 10 <= len(tags) <= 15:
            score += 5
        elif 8 <= len(tags) < 10:
            score += 3
        
        # Long-tail keywords in tags
        long_tail_count = sum(1 for t in tags if len(t.split()) >= 3)
        if long_tail_count >= 3:
            score += 5
        
        # TRENDING OPTIMIZATION (5 points)
        # Trend score factor
        score += min(5, trend.trend_score / 20)
        
        return min(100, score)
    
    def _calculate_aeo_score(self, title: str, description: str, trend: HotTrend) -> float:
        """Calculate Answer Engine Optimization score (0-100)"""
        score = 0.0
        
        keyword = trend.keyword.lower()
        desc_lower = description.lower()
        
        # ANSWER-FOCUSED CONTENT (40 points)
        # Question words present
        question_words = ['what', 'why', 'how', 'when', 'where', 'who']
        question_count = sum(1 for qw in question_words if qw in desc_lower[:500])
        score += min(20, question_count * 4)  # Up to 20 points
        
        # Direct answers to questions
        answer_phrases = [
            f"{keyword} is", f"{keyword} means", f"{keyword} works",
            f"because {keyword}", f"to {keyword}", f"with {keyword}"
        ]
        answer_count = sum(1 for phrase in answer_phrases if phrase in desc_lower)
        score += min(20, answer_count * 5)  # Up to 20 points
        
        # STRUCTURED INFORMATION (30 points)
        # Lists/bullet points (easy to parse)
        if '•' in description or '-' in description or any(str(i) in desc_lower for i in range(1, 10)):
            score += 10
        
        # Timestamps (structured content)
        if '0:00' in description or '00:00' in description:
            score += 10
        
        # Headers/sections
        if any(marker in description for marker in ['📌', '✅', '🎯', '💡', '⏱️']):
            score += 10
        
        # SEMANTIC KEYWORDS (20 points)
        # Related terms present
        related_terms = trend.related_keywords[:10]
        related_count = sum(1 for term in related_terms if term.lower() in desc_lower)
        score += min(20, related_count * 3)  # Up to 20 points
        
        # COMPREHENSIVENESS (10 points)
        # Length (comprehensive answers)
        word_count = len(desc_lower.split())
        if word_count >= 400:
            score += 10
        elif word_count >= 300:
            score += 7
        elif word_count >= 200:
            score += 5
        
        return min(100, score)
    
    def _analyze_keyword_density(self, description: str, trend: HotTrend) -> Dict[str, float]:
        """Analyze keyword density for SEO optimization"""
        desc_lower = description.lower()
        words = desc_lower.split()
        total_words = len(words)
        
        if total_words == 0:
            return {}
        
        keyword = trend.keyword.lower()
        keyword_count = desc_lower.count(keyword)
        keyword_density = (keyword_count / total_words) * 100
        
        # Analyze related keywords
        related_density = {}
        for related in trend.related_keywords[:5]:
            related_lower = related.lower()
            count = desc_lower.count(related_lower)
            if count > 0:
                related_density[related] = (count / total_words) * 100
        
        return {
            'primary_keyword': keyword_density,
            'primary_keyword_count': keyword_count,
            'total_words': total_words,
            'optimal_range': '3-5%',
            'related_keywords': related_density
        }
    
    def _generate_related_keywords(self, trend: HotTrend, content_type: str) -> List[str]:
        """Generate semantic/related keywords for AEO"""
        related = []
        
        keyword = trend.keyword.lower()
        
        # Generate semantic variations
        semantic_patterns = [
            f"what is {keyword}",
            f"why {keyword}",
            f"how {keyword}",
            f"{keyword} meaning",
            f"{keyword} definition",
            f"{keyword} explained",
            f"{keyword} tutorial",
            f"{keyword} guide",
            f"{keyword} review",
            f"best {keyword}",
            f"{keyword} vs",
            f"{keyword} alternatives",
            f"{keyword} examples",
            f"{keyword} benefits",
            f"{keyword} uses"
        ]
        
        related.extend(semantic_patterns)
        
        # Add trend-specific related terms
        related.extend(trend.related_keywords)
        
        # Add content-type specific
        type_related = {
            "music": ["background music", "royalty free", "cinematic", "ambient", "soundtrack"],
            "art": ["digital art", "art print", "wall art", "decor", "design"],
            "tutorial": ["how to", "guide", "tutorial", "tips", "tricks"],
            "case_study": ["results", "review", "test", "comparison", "analysis"]
        }
        related.extend(type_related.get(content_type, []))
        
        return list(set(related))[:20]  # Limit to 20
    
    def _estimate_performance(self, trend: HotTrend, seo_score: float, aeo_score: float) -> Dict[str, float]:
        """Estimate content performance with AEO/SEO optimization"""
        # Base estimates
        base_views = 1000
        
        # Trend score multiplier
        trend_multiplier = trend.trend_score / 50  # 1.0 to 2.0
        
        # SEO score multiplier
        seo_multiplier = seo_score / 50  # 1.0 to 2.0
        
        # AEO score multiplier (Answer Engine Optimization boosts discovery)
        aeo_multiplier = 1.0 + (aeo_score / 100)  # 1.0 to 2.0
        
        # Competition factor
        competition_factor = {
            'low': 1.5,
            'medium': 1.0,
            'high': 0.7
        }.get(trend.competition, 1.0)
        
        # Calculate estimated views (AEO helps with voice search and featured snippets)
        estimated_views = base_views * trend_multiplier * seo_multiplier * aeo_multiplier * competition_factor
        
        # Estimate CTR (higher for trending + optimized content)
        base_ctr = 5.0
        trend_ctr_boost = trend.trend_score / 20  # Up to 5%
        seo_ctr_boost = (seo_score - 70) / 10 if seo_score > 70 else 0  # Bonus for excellent SEO
        estimated_ctr = base_ctr + trend_ctr_boost + seo_ctr_boost
        estimated_ctr = min(12.0, estimated_ctr)  # Cap at 12%
        
        # Estimate watch time (trending + engaging content has higher retention)
        base_retention = 55.0
        trend_retention_boost = trend.trend_score / 4  # Up to 25%
        aeo_retention_boost = aeo_score / 5 if aeo_score > 70 else 0  # AEO content is more engaging
        estimated_retention = base_retention + trend_retention_boost + aeo_retention_boost
        estimated_retention = min(85.0, estimated_retention)  # Cap at 85%
        
        # Ranking potential (combined SEO + AEO)
        combined_score = (seo_score * 0.6) + (aeo_score * 0.4)  # Weighted average
        ranking_potential = (combined_score / 100) * trend.seo_potential
        
        return {
            'estimated_views_30d': estimated_views,
            'estimated_ctr': estimated_ctr,
            'estimated_retention': estimated_retention,
            'ranking_potential': ranking_potential,
            'seo_score': seo_score,
            'aeo_score': aeo_score,
            'combined_score': combined_score
        }
    
    def save_content_package(self, package: TrendingContentPackage, output_dir: Path):
        """Save complete content package"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Sanitize filename
        safe_keyword = "".join(c for c in package.trend.keyword if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_keyword = safe_keyword.replace(' ', '_')[:40]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save description
        desc_file = output_dir / f"{safe_keyword}_{timestamp}_description.txt"
        with open(desc_file, 'w') as f:
            f.write(package.description)
        
        # Save metadata
        metadata = {
            'trend': {
                'keyword': package.trend.keyword,
                'trend_score': package.trend.trend_score,
                'growth_rate': package.trend.growth_rate,
                'competition': package.trend.competition,
                'platforms': package.trend.platforms,
                'seo_potential': package.trend.seo_potential
            },
            'content': {
                'title': package.title,
                'tags': package.tags,
                'hashtags': package.hashtags,
                'seo_score': package.seo_score,
                'aeo_score': package.aeo_score,
                'combined_score': package.estimated_performance['combined_score'],
                'publish_timing': package.publish_timing
            },
            'optimization': {
                'keyword_density': package.keyword_density,
                'related_keywords': package.related_keywords,
                'seo_analysis': {
                    'title_length': len(package.title),
                    'description_length': len(package.description),
                    'tag_count': len(package.tags),
                    'hashtag_count': len(package.hashtags.split())
                }
            },
            'performance': package.estimated_performance,
            'script_outline': package.script_outline,
            'thumbnail_concept': package.thumbnail_concept
        }
        
        metadata_file = output_dir / f"{safe_keyword}_{timestamp}_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print("\n💾 Content package saved:")
        print(f"   - Description: {desc_file.name}")
        print(f"   - Metadata: {metadata_file.name}")


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Hot Trending Content Engine')
    parser.add_argument('--niche', default='content creation, AI, music, art, automation, technology',
                       help='Content niche to analyze')
    parser.add_argument('--min-score', type=float, default=75.0,
                       help='Minimum trend score (0-100)')
    parser.add_argument('--max-results', type=int, default=5,
                       help='Maximum number of trends to return')
    parser.add_argument('--generate', action='store_true',
                       help='Generate content packages for top trends')
    parser.add_argument('--output', default='~/hot_trending_content',
                       help='Output directory for content packages')
    
    args = parser.parse_args()
    
    engine = HotTrendingContentEngine()
    
    # Discover hot trends
    trends = engine.discover_hot_trends(
        niche=args.niche,
        min_trend_score=args.min_score,
        max_results=args.max_results
    )
    
    if not trends:
        print("\n⚠️  No hot trends found matching criteria.")
        print("   Try lowering --min-score or expanding --niche")
        return
    
    # Display trends
    print("\n" + "="*70)
    print("🔥 TOP HOT TRENDING TOPICS")
    print("="*70)
    print()
    
    for i, trend in enumerate(trends, 1):
        print(f"{i}. {trend.keyword}")
        print(f"   Trend Score: {trend.trend_score:.1f}/100")
        print(f"   Growth Rate: {trend.growth_rate:.1f}%")
        print(f"   Competition: {trend.competition.upper()}")
        print(f"   Platforms: {', '.join(trend.platforms)}")
        print(f"   SEO Potential: {trend.seo_potential:.1f}/100")
        print()
    
    # Generate content packages if requested
    if args.generate:
        print("\n" + "="*70)
        print("🎬 GENERATING CONTENT PACKAGES")
        print("="*70)
        print()
        
        output_dir = Path(args.output).expanduser()
        
        for trend in trends[:3]:  # Generate for top 3
            package = engine.generate_trending_content(trend)
            
            print(f"\n✅ Generated package for: {trend.keyword}")
            print(f"   SEO Score: {package.seo_score:.1f}/100")
            print(f"   AEO Score: {package.aeo_score:.1f}/100")
            print(f"   Combined Score: {package.estimated_performance['combined_score']:.1f}/100")
            print(f"   Estimated Views (30d): {package.estimated_performance['estimated_views_30d']:,.0f}")
            print(f"   Estimated CTR: {package.estimated_performance['estimated_ctr']:.1f}%")
            print(f"   Estimated Retention: {package.estimated_performance['estimated_retention']:.1f}%")
            print(f"   Keyword Density: {package.keyword_density.get('primary_keyword', 0):.2f}%")
            print(f"   Publish Timing: {package.publish_timing}")
            
            engine.save_content_package(package, output_dir)
            print()


if __name__ == '__main__':
    main()

