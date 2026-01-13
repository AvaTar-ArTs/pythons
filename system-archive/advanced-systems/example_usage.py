#!/usr/bin/env python3
"""
🎯 Quick Usage Examples for Advanced Content Intelligence Pipeline
===================================================================
Demonstrates the most common use cases and features.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import the pipeline (assuming advanced-new.py is renamed or imported correctly)
# For direct usage, copy the AdvancedContentPipeline class here or import it

# Uncomment if you've made advanced-new.py importable:
# from advanced_new import AdvancedContentPipeline


# ============================================================================
# EXAMPLE 1: Basic Content Generation with Intelligence
# ============================================================================
async def example_basic_generation():
    """Generate content with automatic analysis and suggestions"""
    print("\n" + "="*80)
    print("📝 EXAMPLE 1: Basic Content Generation with Intelligence")
    print("="*80)

    pipeline = AdvancedContentPipeline()

    result = await pipeline.generate_content(
        prompt="Write a guide about starting a podcast in 2025",
        content_type="blog_post",
        analyze=True,
        suggest=True
    )

    print(f"\n✅ Generated: {len(result['text_content'])} characters")
    print(f"📊 Analysis: {result.get('analysis', {})}")
    print(f"💡 Suggestions: {result.get('suggestions', [])[:3]}")


# ============================================================================
# EXAMPLE 2: Content Quality Scoring
# ============================================================================
async def example_quality_scoring():
    """Score content quality across multiple dimensions"""
    print("\n" + "="*80)
    print("🎯 EXAMPLE 2: Content Quality Scoring")
    print("="*80)

    pipeline = AdvancedContentPipeline()

    # Sample content to score
    content = """
    Discover the power of AI in content creation. Modern tools transform
    how we write, edit, and optimize content for maximum impact.

    Are you ready to revolutionize your content strategy? With AI-powered
    tools, you can create engaging content faster than ever before.

    Join thousands of creators who have already transformed their workflow.
    Start your journey today!
    """

    score = await pipeline.generate_content_score(content, "blog_post")

    print(f"\n📊 Quality Score: {score['total_score']}/100")
    print(f"🏆 Grade: {score['grade']}")
    print(f"📈 Breakdown:")
    for dimension, value in score['breakdown'].items():
        print(f"   - {dimension.title()}: {value}/25")
    print(f"💬 Recommendation: {score['recommendation']}")


# ============================================================================
# EXAMPLE 3: Multi-Platform Optimization
# ============================================================================
async def example_platform_optimization():
    """Optimize content for different social media platforms"""
    print("\n" + "="*80)
    print("📱 EXAMPLE 3: Multi-Platform Optimization")
    print("="*80)

    pipeline = AdvancedContentPipeline()

    original_content = """
    Exciting news! We've just launched our new AI-powered content creation
    tool that helps you create amazing content in minutes. Whether you're
    a blogger, marketer, or creator, this tool will transform your workflow.
    """

    platforms = ['twitter', 'linkedin', 'instagram']

    print("\n🔄 Optimizing for platforms:")
    for platform in platforms:
        optimized = await pipeline.optimize_for_platform(original_content, platform)
        print(f"\n📍 {platform.upper()}:")
        print(f"   Length: {optimized['optimized_length']} chars")
        print(f"   Preview: {optimized['optimized_content'][:100]}...")


# ============================================================================
# EXAMPLE 4: SEO Optimization
# ============================================================================
async def example_seo_optimization():
    """Generate SEO metadata for content"""
    print("\n" + "="*80)
    print("🔍 EXAMPLE 4: SEO Optimization")
    print("="*80)

    pipeline = AdvancedContentPipeline()

    content = """
    Machine learning and artificial intelligence are revolutionizing content
    creation. This comprehensive guide explores how AI tools can help content
    creators, marketers, and businesses streamline their workflow and create
    better content faster. Learn about the latest AI-powered writing
    assistants, image generators, and optimization tools.
    """

    # Extract keywords
    keywords = await pipeline.extract_keywords(content, count=5)
    print(f"\n🔑 Top Keywords:")
    for keyword, freq in keywords:
        print(f"   - {keyword}: {freq} occurrences")

    # Generate SEO metadata
    seo = await pipeline.generate_seo_metadata(content)
    print(f"\n🌐 SEO Metadata:")
    print(f"   Title Options:")
    for i, title in enumerate(seo.get('title_options', [])[:3], 1):
        print(f"     {i}. {title}")
    print(f"\n   Meta Description: {seo.get('meta_description', 'N/A')[:100]}...")
    print(f"   Recommended Slug: {seo.get('recommended_slug', 'N/A')}")


# ============================================================================
# EXAMPLE 5: A/B Testing Variants
# ============================================================================
async def example_ab_testing():
    """Generate multiple content variants for A/B testing"""
    print("\n" + "="*80)
    print("🔬 EXAMPLE 5: A/B Testing Variants")
    print("="*80)

    pipeline = AdvancedContentPipeline()

    original = "Transform your content strategy with AI-powered tools today!"

    variants = await pipeline.generate_ab_test_variants(original, variations=3)

    print(f"\n📊 Generated {len(variants)} variants for A/B testing:")
    print(f"\nOriginal: {original}")

    for i, variant in enumerate(variants, 1):
        print(f"\nVariant {i}:")
        print(f"   {variant['content'][:150]}...")
        print(f"   Modifications: {variant['modifications']}")


# ============================================================================
# EXAMPLE 6: Audience Targeting
# ============================================================================
async def example_audience_targeting():
    """Analyze content fit for different target audiences"""
    print("\n" + "="*80)
    print("👥 EXAMPLE 6: Audience Targeting Analysis")
    print("="*80)

    pipeline = AdvancedContentPipeline()

    content = """
    Leverage cutting-edge AI/ML algorithms to optimize your content
    generation workflow. Our enterprise-grade solution provides scalable,
    cloud-native infrastructure for high-performance content creation.
    """

    audiences = [
        'technical developers',
        'marketing professionals',
        'general consumers'
    ]

    print("\n🎯 Analyzing audience fit:")
    for audience in audiences:
        fit = await pipeline.analyze_audience_fit(content, audience)
        score = fit.get('overall_fit_score', 'N/A')
        recommendation = fit.get('recommendation', 'N/A')
        print(f"\n   {audience.title()}: {score}/10 - {recommendation}")


# ============================================================================
# EXAMPLE 7: Complete Content Campaign
# ============================================================================
async def example_complete_campaign():
    """Full content campaign workflow from generation to optimization"""
    print("\n" + "="*80)
    print("🚀 EXAMPLE 7: Complete Content Campaign")
    print("="*80)

    pipeline = AdvancedContentPipeline()

    print("\n📝 Step 1: Generate initial content...")
    result = await pipeline.generate_content(
        prompt="Write about sustainable living tips for beginners",
        content_type="blog_post",
        analyze=True
    )

    content = result['text_content']
    print(f"   ✅ Generated {len(content)} characters")

    print("\n🎯 Step 2: Quality check...")
    score = await pipeline.generate_content_score(content, "blog_post")
    print(f"   Score: {score['total_score']}/100 - {score['grade']}")

    print("\n🔍 Step 3: SEO optimization...")
    seo = await pipeline.generate_seo_metadata(content)
    print(f"   ✅ Generated title options and metadata")

    print("\n📱 Step 4: Platform optimization...")
    twitter = await pipeline.optimize_for_platform(content, 'twitter')
    linkedin = await pipeline.optimize_for_platform(content, 'linkedin')
    print(f"   ✅ Optimized for Twitter and LinkedIn")

    print("\n🔬 Step 5: Create A/B variants...")
    variants = await pipeline.generate_ab_test_variants(content[:300], variations=2)
    print(f"   ✅ Created {len(variants)} test variants")

    print("\n👥 Step 6: Audience fit analysis...")
    fit = await pipeline.analyze_audience_fit(content, "eco-conscious millennials")
    print(f"   ✅ Audience fit score: {fit.get('overall_fit_score', 'N/A')}/10")

    print("\n🎉 Campaign ready for deployment!")


# ============================================================================
# EXAMPLE 8: Quick Content Evaluation
# ============================================================================
async def example_quick_evaluation():
    """Quick evaluation of existing content"""
    print("\n" + "="*80)
    print("⚡ EXAMPLE 8: Quick Content Evaluation")
    print("="*80)

    pipeline = AdvancedContentPipeline()

    existing_content = """
    Are you struggling with content creation? Our revolutionary AI tool
    changes everything! Create amazing blog posts, social media content,
    and marketing copy in seconds.

    Join over 10,000 satisfied creators who've transformed their workflow.
    Try it free today - no credit card required!

    Start creating better content now: www.example.com
    """

    print("\n🔍 Analyzing existing content...")

    # Quick analysis
    analysis = await pipeline.analyze_content(existing_content)
    print(f"\n📊 Basic Metrics:")
    print(f"   Word count: {analysis['word_count']}")
    print(f"   Reading level: {analysis['reading_level']}")
    print(f"   Sentiment: {analysis['sentiment']}")

    # Quality score
    score = await pipeline.generate_content_score(existing_content, "marketing_copy")
    print(f"\n🎯 Quality Score: {score['total_score']}/100")
    print(f"   Grade: {score['grade']}")

    # Improvement suggestions
    suggestions = await pipeline.suggest_improvements(existing_content)
    print(f"\n💡 Top Suggestions:")
    for i, suggestion in enumerate(suggestions[:3], 1):
        print(f"   {i}. {suggestion}")


# ============================================================================
# RUN ALL EXAMPLES
# ============================================================================
async def run_all_examples():
    """Run all examples in sequence"""
    print("\n" + "🎨"*40)
    print("ADVANCED CONTENT INTELLIGENCE PIPELINE - USAGE EXAMPLES")
    print("🎨"*40)

    examples = [
        ("Basic Generation", example_basic_generation),
        ("Quality Scoring", example_quality_scoring),
        ("Platform Optimization", example_platform_optimization),
        ("SEO Optimization", example_seo_optimization),
        ("A/B Testing", example_ab_testing),
        ("Audience Targeting", example_audience_targeting),
        ("Complete Campaign", example_complete_campaign),
        ("Quick Evaluation", example_quick_evaluation),
    ]

    for name, example_func in examples:
        try:
            await example_func()
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")

        # Add delay between examples
        await asyncio.sleep(1)

    print("\n" + "="*80)
    print("✅ All examples completed!")
    print("="*80)


# ============================================================================
# INTERACTIVE MODE
# ============================================================================
async def interactive_mode():
    """Interactive CLI for testing features"""
    print("\n" + "🎮"*40)
    print("INTERACTIVE MODE")
    print("🎮"*40)

    print("\nAvailable examples:")
    print("1. Basic Generation")
    print("2. Quality Scoring")
    print("3. Platform Optimization")
    print("4. SEO Optimization")
    print("5. A/B Testing")
    print("6. Audience Targeting")
    print("7. Complete Campaign")
    print("8. Quick Evaluation")
    print("9. Run All Examples")
    print("0. Exit")

    choice = input("\nSelect an example (0-9): ").strip()

    examples = {
        '1': example_basic_generation,
        '2': example_quality_scoring,
        '3': example_platform_optimization,
        '4': example_seo_optimization,
        '5': example_ab_testing,
        '6': example_audience_targeting,
        '7': example_complete_campaign,
        '8': example_quick_evaluation,
        '9': run_all_examples,
    }

    if choice in examples:
        await examples[choice]()
    elif choice == '0':
        print("\n👋 Goodbye!")
    else:
        print("\n❌ Invalid choice!")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    import sys

    # Check if AdvancedContentPipeline is available
    try:
        from advanced_new import AdvancedContentPipeline
    except ImportError:
        print("❌ Error: Could not import AdvancedContentPipeline")
        print("💡 Make sure advanced-new.py is in the same directory")
        print("💡 Or rename it to advanced_new.py (no dash)")
        sys.exit(1)

    # Run examples
    if len(sys.argv) > 1:
        if sys.argv[1] == '--all':
            asyncio.run(run_all_examples())
        elif sys.argv[1] == '--interactive':
            asyncio.run(interactive_mode())
        else:
            print("Usage:")
            print("  python example_usage.py --all         # Run all examples")
            print("  python example_usage.py --interactive # Interactive mode")
    else:
        print("\n🚀 Running all examples...")
        asyncio.run(run_all_examples())
