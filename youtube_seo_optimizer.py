#!/usr/bin/env python3
"""
🎬 YOUTUBE SEO OPTIMIZER
Content-aware SEO optimization for YouTube videos

Integrates with:
- content-orchestrator.py (YouTube content generation)
- multi-llm-orchestrator.py (AI routing)
- content_classifier.py (Asset matching)
- customer_retention_engine.py (Viewer retention)
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from content_orchestrator import UnifiedContentOrchestrator
    from multi_llm_orchestrator import AIOrchestrator, TaskType
except ImportError:
    print("Warning: Some dependencies not available")
    UnifiedContentOrchestrator = None
    AIOrchestrator = None


@dataclass
class YouTubeVideo:
    """YouTube video with SEO optimization"""
    title: str
    description: str
    tags: List[str]
    category: str
    thumbnail_path: Optional[str] = None
    script: Optional[str] = None
    timestamps: List[Dict[str, str]] = field(default_factory=list)
    seo_score: float = 0.0
    estimated_ctr: float = 0.0
    target_keywords: List[str] = field(default_factory=list)


@dataclass
class SEOAnalysis:
    """SEO analysis results"""
    keyword_density: Dict[str, float]
    title_optimization: Dict[str, Any]
    description_optimization: Dict[str, Any]
    tag_recommendations: List[str]
    competitor_analysis: Dict[str, Any]
    trending_keywords: List[str]
    seo_score: float
    recommendations: List[str]


class YouTubeSEOOptimizer:
    """Advanced YouTube SEO optimization system"""
    
    def __init__(self):
        self.orchestrator = UnifiedContentOrchestrator() if UnifiedContentOrchestrator else None
        self.ai_orchestrator = AIOrchestrator() if AIOrchestrator else None
        self.videos: Dict[str, YouTubeVideo] = {}
    
    def generate_seo_optimized_video(
        self,
        topic: str,
        keywords: str,
        content_type: str = "music",  # music, art, tutorial, case_study
        generate_script: bool = True,
        generate_thumbnail: bool = True
    ) -> YouTubeVideo:
        """Generate complete SEO-optimized YouTube video package"""
        
        print(f"🎬 Generating SEO-optimized video package for: {topic}")
        print("="*70)
        
        # Step 1: Keyword Research
        print("\n1️⃣  Researching keywords...")
        target_keywords = self._research_keywords(topic, keywords)
        
        # Step 2: Generate Optimized Title
        print("\n2️⃣  Generating optimized title...")
        title = self._generate_optimized_title(topic, target_keywords, content_type)
        
        # Step 3: Generate Description
        print("\n3️⃣  Generating SEO-optimized description...")
        description_data = self._generate_description(topic, title, target_keywords, content_type)
        
        # Step 4: Generate Tags
        print("\n4️⃣  Generating optimized tags...")
        tags = self._generate_tags(topic, target_keywords, content_type)
        
        # Step 5: Generate Timestamps
        print("\n5️⃣  Generating timestamps/chapters...")
        timestamps = self._generate_timestamps(description_data.get('outline', ''))
        
        # Step 6: Generate Script (if requested)
        script = None
        if generate_script:
            print("\n6️⃣  Generating video script...")
            script = self._generate_script(topic, description_data.get('outline', ''), content_type)
        
        # Step 7: Generate Thumbnail (if requested)
        thumbnail_path = None
        if generate_thumbnail:
            print("\n7️⃣  Generating thumbnail...")
            thumbnail_path = self._generate_thumbnail(topic, title, content_type)
        
        # Step 8: Calculate SEO Score
        print("\n8️⃣  Calculating SEO score...")
        seo_score = self._calculate_seo_score(title, description_data['description'], tags, target_keywords)
        estimated_ctr = self._estimate_ctr(title, description_data['description'])
        
        video = YouTubeVideo(
            title=title,
            description=description_data['description'],
            tags=tags,
            category=content_type,
            thumbnail_path=thumbnail_path,
            script=script,
            timestamps=timestamps,
            seo_score=seo_score,
            estimated_ctr=estimated_ctr,
            target_keywords=target_keywords
        )
        
        print(f"\n✅ SEO Score: {seo_score:.1f}/100")
        print(f"✅ Estimated CTR: {estimated_ctr:.1f}%")
        print(f"✅ Title: {title}")
        print(f"✅ Tags: {len(tags)} tags generated")
        
        return video
    
    def _research_keywords(self, topic: str, provided_keywords: str) -> List[str]:
        """Research and optimize keywords"""
        if self.ai_orchestrator:
            # Use Grok for real-time trending keywords
            prompt = f"""Research SEO keywords for YouTube video about: {topic}

Provided keywords: {provided_keywords}

Provide:
1. Primary keyword (most important)
2. 5-7 secondary keywords (related, high search volume)
3. 3-5 long-tail keywords (specific, lower competition)
4. 2-3 trending keywords (current interest)

Output as JSON: {{"primary": "...", "secondary": [...], "long_tail": [...], "trending": [...]}}"""
            
            try:
                # Use Groq for fast keyword research
                if hasattr(self.ai_orchestrator, 'select_best_model'):
                    model_key = self.ai_orchestrator.select_best_model(
                        TaskType.RESEARCH,
                        priority="speed"
                    )
                    # Would use async in production
                    # For now, return provided keywords + variations
                    pass
            except:
                pass
        
        # Fallback: Use provided keywords + generate variations
        keywords = [k.strip() for k in provided_keywords.split(',')]
        
        # Add variations
        variations = []
        for keyword in keywords:
            variations.append(keyword)
            variations.append(f"{keyword} 2025")
            variations.append(f"best {keyword}")
            variations.append(f"{keyword} tutorial")
        
        return list(set(variations))[:15]  # Limit to 15
    
    def _generate_optimized_title(self, topic: str, keywords: List[str], content_type: str) -> str:
        """Generate SEO-optimized title"""
        if self.orchestrator:
            try:
                # Use content orchestrator's YouTube pipeline
                result = self.orchestrator.generate_youtube_content(
                    title=topic,
                    keywords=', '.join(keywords[:5]),
                    image_descriptions=f"{content_type} content thumbnail"
                )
                return result.get('title', topic)
            except:
                pass
        
        # Fallback: Create optimized title manually
        primary_keyword = keywords[0] if keywords else topic
        
        # Title templates by content type
        templates = {
            "music": f"{primary_keyword} | {keywords[1] if len(keywords) > 1 else 'Background Music'}",
            "art": f"{primary_keyword} Art Print | {keywords[1] if len(keywords) > 1 else 'Wall Art'}",
            "tutorial": f"How to {topic} | {keywords[1] if len(keywords) > 1 else 'Complete Guide'}",
            "case_study": f"{topic} Results | {keywords[1] if len(keywords) > 1 else 'Real Numbers'}"
        }
        
        title = templates.get(content_type, f"{primary_keyword} | {topic}")
        
        # Ensure title is 60 characters or less (optimal for YouTube)
        if len(title) > 60:
            title = title[:57] + "..."
        
        return title
    
    def _generate_description(self, topic: str, title: str, keywords: List[str], content_type: str) -> Dict[str, Any]:
        """Generate SEO-optimized description"""
        if self.orchestrator:
            try:
                result = self.orchestrator.generate_youtube_content(
                    title=title,
                    keywords=', '.join(keywords[:5]),
                    image_descriptions=f"{content_type} content"
                )
                return {
                    'description': result.get('description', ''),
                    'outline': result.get('outline', '')
                }
            except:
                pass
        
        # Fallback: Generate basic description
        primary_keyword = keywords[0] if keywords else topic
        
        description = f"""
{title}

🎵 {primary_keyword} - Perfect for {keywords[1] if len(keywords) > 1 else 'your projects'}!

In this video, we explore {topic} and how it can help you {keywords[2] if len(keywords) > 2 else 'achieve your goals'}.

📌 What You'll Learn:
• {keywords[0] if keywords else topic}
• {keywords[1] if len(keywords) > 1 else 'Key insights'}
• {keywords[2] if len(keywords) > 2 else 'Practical tips'}

🔔 Subscribe for more {content_type} content!

📱 Connect with us:
• Website: [Your website]
• Instagram: [Your Instagram]
• Twitter: [Your Twitter]

#{" #".join(keywords[:10])}
"""
        
        return {
            'description': description.strip(),
            'outline': f"Video about {topic} covering {', '.join(keywords[:3])}"
        }
    
    def _generate_tags(self, topic: str, keywords: List[str], content_type: str) -> List[str]:
        """Generate optimized tags"""
        tags = keywords.copy()
        
        # Add content-type specific tags
        type_tags = {
            "music": ["music", "background music", "royalty free", "no copyright"],
            "art": ["art", "digital art", "print on demand", "wall art"],
            "tutorial": ["tutorial", "how to", "guide", "tips"],
            "case_study": ["results", "case study", "success story", "review"]
        }
        
        tags.extend(type_tags.get(content_type, []))
        
        # Add year tag
        tags.append("2025")
        
        # Limit to 15 tags (YouTube recommendation)
        return list(set(tags))[:15]
    
    def _generate_timestamps(self, outline: str) -> List[Dict[str, str]]:
        """Generate video timestamps/chapters"""
        if self.orchestrator:
            try:
                result = self.orchestrator.generate_youtube_content(
                    title="Video",
                    keywords="",
                    image_descriptions=""
                )
                return result.get('timestamps', [])
            except:
                pass
        
        # Fallback: Generate basic timestamps
        return [
            {"time": "0:00", "title": "Introduction"},
            {"time": "1:00", "title": "Main Content"},
            {"time": "3:00", "title": "Key Points"},
            {"time": "5:00", "title": "Conclusion"}
        ]
    
    def _generate_script(self, topic: str, outline: str, content_type: str) -> str:
        """Generate video script"""
        if self.orchestrator and self.ai_orchestrator:
            try:
                # Use Claude for script generation (best quality)
                model_key = self.ai_orchestrator.select_best_model(
                    TaskType.CREATIVE_WRITING,
                    priority="quality"
                )
                # Would generate script here
                pass
            except:
                pass
        
        # Fallback: Basic script template
        return f"""
[INTRO - 0:00-0:15]
Welcome to the channel! Today we're exploring {topic}.

[MAIN CONTENT - 0:15-4:00]
{outline or f"Let's dive into {topic} and discover what makes it special."}

[KEY POINTS - 4:00-5:30]
Here are the key takeaways:
1. {topic} is important because...
2. You can use it to...
3. The best approach is...

[CONCLUSION - 5:30-6:00]
Thanks for watching! Don't forget to like and subscribe for more {content_type} content.
"""
    
    def _generate_thumbnail(self, topic: str, title: str, content_type: str) -> Optional[str]:
        """Generate thumbnail"""
        if self.orchestrator:
            try:
                result = self.orchestrator.generate_youtube_content(
                    title=title,
                    keywords=topic,
                    image_descriptions=f"{content_type} thumbnail, eye-catching, bold text"
                )
                thumbnails = result.get('thumbnails', [])
                if thumbnails:
                    return thumbnails[0]  # Return first thumbnail URL
            except:
                pass
        
        # Fallback: Use existing art gallery
        art_dir = Path.home() / 'workspace/avatararts-complete/DaLL-E'
        if art_dir.exists():
            # Find matching image (would use content_classifier in production)
            images = list(art_dir.glob('*.jpg'))[:1]
            if images:
                return str(images[0])
        
        return None
    
    def _calculate_seo_score(self, title: str, description: str, tags: List[str], keywords: List[str]) -> float:
        """Calculate SEO optimization score (0-100)"""
        score = 0.0
        
        # Title optimization (30 points)
        primary_keyword = keywords[0] if keywords else ""
        if primary_keyword.lower() in title.lower():
            score += 20
        if len(title) <= 60:
            score += 10
        
        # Description optimization (40 points)
        description_lower = description.lower()
        keyword_count = sum(1 for kw in keywords[:5] if kw.lower() in description_lower)
        score += min(30, keyword_count * 6)  # Up to 30 points for keyword usage
        if len(description) >= 200:
            score += 10  # Minimum length
        
        # Tags optimization (20 points)
        if len(tags) >= 10:
            score += 10
        if len(tags) <= 15:
            score += 10
        
        # Keyword coverage (10 points)
        if len(keywords) >= 5:
            score += 10
        
        return min(100, score)
    
    def _estimate_ctr(self, title: str, description: str) -> float:
        """Estimate click-through rate"""
        ctr = 3.0  # Base CTR
        
        # Title factors
        if any(word in title.lower() for word in ['how to', 'best', 'top', 'ultimate']):
            ctr += 1.0
        if any(char in title for char in ['|', ':', '?']):
            ctr += 0.5
        
        # Description factors
        if len(description) > 500:
            ctr += 0.5
        
        return min(10.0, ctr)  # Cap at 10%
    
    def analyze_seo(self, video: YouTubeVideo) -> SEOAnalysis:
        """Analyze and optimize SEO"""
        # Keyword density analysis
        all_text = f"{video.title} {video.description}".lower()
        keyword_density = {}
        for keyword in video.target_keywords:
            count = all_text.count(keyword.lower())
            density = (count / len(all_text.split())) * 100 if all_text else 0
            keyword_density[keyword] = density
        
        # Title optimization
        title_optimization = {
            'length': len(video.title),
            'optimal': len(video.title) <= 60,
            'has_primary_keyword': video.target_keywords[0].lower() in video.title.lower() if video.target_keywords else False,
            'has_power_words': any(word in video.title.lower() for word in ['best', 'ultimate', 'complete', 'guide'])
        }
        
        # Description optimization
        description_optimization = {
            'length': len(video.description),
            'optimal': len(video.description) >= 200,
            'has_timestamps': any('0:00' in line or '00:00' in line for line in video.description.split('\n')),
            'has_cta': any(phrase in video.description.lower() for phrase in ['subscribe', 'like', 'comment'])
        }
        
        # Recommendations
        recommendations = []
        if not title_optimization['optimal']:
            recommendations.append("Title should be 60 characters or less")
        if not title_optimization['has_primary_keyword']:
            recommendations.append(f"Include primary keyword '{video.target_keywords[0]}' in title")
        if not description_optimization['optimal']:
            recommendations.append("Description should be at least 200 characters")
        if not description_optimization['has_timestamps']:
            recommendations.append("Add timestamps/chapters to description")
        if len(video.tags) < 10:
            recommendations.append("Add more tags (target 10-15)")
        
        return SEOAnalysis(
            keyword_density=keyword_density,
            title_optimization=title_optimization,
            description_optimization=description_optimization,
            tag_recommendations=video.tags,
            competitor_analysis={},  # Would be populated in production
            trending_keywords=video.target_keywords[:3],
            seo_score=video.seo_score,
            recommendations=recommendations
        )
    
    def save_video_package(self, video: YouTubeVideo, output_dir: Path):
        """Save complete video package to files"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Sanitize filename
        safe_title = "".join(c for c in video.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')[:50]
        
        # Save description
        desc_file = output_dir / f"{safe_title}_description.txt"
        with open(desc_file, 'w') as f:
            f.write(video.description)
        
        # Save metadata
        metadata = {
            'title': video.title,
            'tags': video.tags,
            'category': video.category,
            'seo_score': video.seo_score,
            'estimated_ctr': video.estimated_ctr,
            'target_keywords': video.target_keywords,
            'timestamps': video.timestamps
        }
        
        metadata_file = output_dir / f"{safe_title}_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Save script if available
        if video.script:
            script_file = output_dir / f"{safe_title}_script.txt"
            with open(script_file, 'w') as f:
                f.write(video.script)
        
        print(f"\n💾 Video package saved to: {output_dir}")
        print(f"   - Description: {desc_file.name}")
        print(f"   - Metadata: {metadata_file.name}")
        if video.script:
            print(f"   - Script: {script_file.name}")


def main():
    """Demo of YouTube SEO Optimizer"""
    import argparse
    
    parser = argparse.ArgumentParser(description='YouTube SEO Optimizer')
    parser.add_argument('--topic', required=True, help='Video topic')
    parser.add_argument('--keywords', required=True, help='Comma-separated keywords')
    parser.add_argument('--type', default='music', choices=['music', 'art', 'tutorial', 'case_study'],
                       help='Content type')
    parser.add_argument('--output', default='~/youtube_content', help='Output directory')
    parser.add_argument('--script', action='store_true', help='Generate script')
    parser.add_argument('--thumbnail', action='store_true', help='Generate thumbnail')
    
    args = parser.parse_args()
    
    optimizer = YouTubeSEOOptimizer()
    
    # Generate video package
    video = optimizer.generate_seo_optimized_video(
        topic=args.topic,
        keywords=args.keywords,
        content_type=args.type,
        generate_script=args.script,
        generate_thumbnail=args.thumbnail
    )
    
    # Analyze SEO
    analysis = optimizer.analyze_seo(video)
    
    # Print analysis
    print("\n" + "="*70)
    print("📊 SEO ANALYSIS")
    print("="*70)
    print(f"\nSEO Score: {analysis.seo_score:.1f}/100")
    print("\nTitle Optimization:")
    for key, value in analysis.title_optimization.items():
        print(f"  {key}: {value}")
    
    print("\nDescription Optimization:")
    for key, value in analysis.description_optimization.items():
        print(f"  {key}: {value}")
    
    if analysis.recommendations:
        print("\n💡 Recommendations:")
        for rec in analysis.recommendations:
            print(f"  - {rec}")
    
    # Save package
    output_dir = Path(args.output).expanduser()
    optimizer.save_video_package(video, output_dir)
    
    print("\n✅ Complete!")


if __name__ == '__main__':
    main()

