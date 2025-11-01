"""
Integrate Ai

This module provides functionality for integrate ai.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
AI Outputs Hub - Integration Script
Automatically saves AI assistant outputs with smart categorization
"""

import sys
import os
from auto_save_system import AIOutputsHub


def save_ai_output(content, title, category="general", tags=None, project=None):
    """
    Main function to save AI assistant outputs
    Call this whenever you want to save an output
    """
    hub = AIOutputsHub()

    # Auto-detect category based on content
    if not category or category == "general":
        category = auto_detect_category(content, title)

    # Auto-generate tags if none provided
    if not tags:
        tags = auto_generate_tags(content, title)

    result = hub.auto_save_output(
        content=content, title=title, category=category, project=project, tags=tags
    )

    logger.info(f"✅ Saved: {result['title']}")
    logger.info(f"📁 Location: {result['filepath']}")
    logger.info(f"🏷️ Category: {result['category']}")
    logger.info(f"🔖 Tags: {', '.join(tags) if tags else 'None'}")
    logger.info(f"🌐 Hub Dashboard: {hub.base_dir}/Dashboard.html")

    return result


def auto_detect_category(content, title):
    """Auto-detect category based on content and title"""
    content_lower = content.lower()
    title_lower = title.lower()

    # SEO and Keywords
    if any(
        keyword in content_lower
        for keyword in ["seo", "keyword", "trending", "optimization", "ranking"]
    ):
        return "seo_analysis"

    # Creative Automation
    if any(
        keyword in content_lower
        for keyword in ["python", "automation", "script", "ai tool", "workflow"]
    ):
        return "creative_automation"

    # Brand Strategy
    if any(
        keyword in content_lower
        for keyword in ["brand", "marketing", "strategy", "positioning", "identity"]
    ):
        return "brand_strategy"

    # Technical Documentation
    if any(
        keyword in content_lower
        for keyword in ["code", "technical", "implementation", "documentation", "api"]
    ):
        return "technical_docs"

    # Content Creation
    if any(
        keyword in content_lower
        for keyword in ["content", "article", "social media", "creative", "writing"]
    ):
        return "content_creation"

    # Business Analysis
    if any(
        keyword in content_lower
        for keyword in ["business", "analysis", "market", "competitive", "strategy"]
    ):
        return "business_analysis"

    return "general"


def auto_generate_tags(content, title):
    """Auto-generate tags based on content"""
    tags = set()
    content_lower = content.lower()

    # Common tag patterns
    tag_patterns = {
        "ai": ["ai", "artificial intelligence", "machine learning", "automation"],
        "seo": ["seo", "search engine", "keywords", "optimization", "ranking"],
        "python": ["python", "script", "automation", "programming"],
        "creative": ["creative", "art", "design", "aesthetic", "visual"],
        "marketing": ["marketing", "brand", "strategy", "promotion", "social media"],
        "technical": ["technical", "code", "implementation", "documentation", "api"],
        "trending": ["trending", "viral", "hot", "rising", "popular"],
        "analysis": ["analysis", "research", "study", "evaluation", "assessment"],
    }

    for tag, keywords in tag_patterns.items():
        if any(keyword in content_lower for keyword in keywords):
            tags.add(tag)

    # Add title-based tags
    title_words = title.lower().split()
    for word in title_words:
        if len(word) > 3 and word.isalpha():
            tags.add(word)

    return list(tags)[:10]  # Limit to 10 tags


def quick_save_seo(content, title):
    """Quick save for SEO content"""
    return save_ai_output(
        content, title, "seo_analysis", ["seo", "keywords", "trending"]
    )


def quick_save_creative(content, title):
    """Quick save for creative automation content"""
    return save_ai_output(
        content, title, "creative_automation", ["python", "automation", "ai"]
    )


def quick_save_brand(content, title):
    """Quick save for brand strategy content"""
    return save_ai_output(
        content, title, "brand_strategy", ["brand", "marketing", "strategy"]
    )


# Example usage
if __name__ == "__main__":
    # Test the integration
    test_content = """
    # Top Trending SEO Keywords
    
    ## AI Automation Keywords
    - AI automation scripts
    - Python creative automation
    - Generative AI workflow
    
    ## Creative Trends
    - Cyberpunk art
    - Vaporwave aesthetic
    - Digital glitch art
    """

    result = save_ai_output(
        content=test_content,
        title="Top Trending SEO Keywords Master List",
        category="seo_analysis",
        tags=["seo", "keywords", "trending", "ai", "automation"],
    )

    logger.info("\n🎉 Integration test complete!")
    logger.info(f"📊 Total outputs in hub: {result.get('total_outputs', 'Unknown')}")
