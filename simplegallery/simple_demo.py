#!/usr/bin/env python3
"""
Simple Demo: Enhanced Content Analysis Improvements

This script demonstrates the improvements made to the content analysis system
without requiring external dependencies.
"""

import csv
from collections import Counter
from pathlib import Path


def load_csv_data(csv_path):
    """Load CSV data and return as list of dictionaries."""
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        print(f"Error loading {csv_path}: {e}")
        return None

def compare_analysis_coverage(original_data, enhanced_data):
    """Compare analysis coverage between original and enhanced versions."""
    print("📊 ANALYSIS COVERAGE COMPARISON")
    print("=" * 50)
    
    original_analyzed = sum(1 for row in original_data if row.get('has_analysis') == 'True')
    enhanced_analyzed = sum(1 for row in enhanced_data if row.get('has_analysis') == 'True')
    total_files = len(enhanced_data)
    
    print(f"Total Files: {total_files}")
    print(f"Original Analysis Coverage: {original_analyzed} files ({original_analyzed/total_files*100:.1f}%)")
    print(f"Enhanced Analysis Coverage: {enhanced_analyzed} files ({enhanced_analyzed/total_files*100:.1f}%)")
    print(f"Improvement: +{enhanced_analyzed - original_analyzed} files")
    print()

def compare_content_classification(original_data, enhanced_data):
    """Compare content classification improvements."""
    print("🏷️  CONTENT CLASSIFICATION IMPROVEMENTS")
    print("=" * 50)
    
    # Original classification
    original_types = Counter(row.get('content_type', 'unknown') for row in original_data)
    print("Original Classification:")
    for content_type, count in original_types.most_common():
        percentage = count / len(original_data) * 100
        print(f"  {content_type}: {count} files ({percentage:.1f}%)")
    
    print("\nEnhanced Classification:")
    enhanced_types = Counter(row.get('content_type', 'unknown') for row in enhanced_data)
    for content_type, count in enhanced_types.most_common():
        percentage = count / len(enhanced_data) * 100
        print(f"  {content_type}: {count} files ({percentage:.1f}%)")
    
    print(f"\nClassification Improvement: {len(enhanced_types)} vs {len(original_types)} categories")
    print()

def analyze_enhanced_features(enhanced_data):
    """Analyze the new enhanced features."""
    print("🚀 ENHANCED FEATURES ANALYSIS")
    print("=" * 50)
    
    # Sentiment analysis
    sentiment_dist = Counter(row.get('primary_sentiment', 'unknown') for row in enhanced_data)
    print("Sentiment Distribution:")
    for sentiment, count in sentiment_dist.most_common():
        percentage = count / len(enhanced_data) * 100
        print(f"  {sentiment}: {count} files ({percentage:.1f}%)")
    
    # Visual style analysis
    visual_style_dist = Counter(row.get('primary_visual_style', 'unknown') for row in enhanced_data)
    print("\nVisual Style Distribution:")
    for style, count in visual_style_dist.most_common():
        percentage = count / len(enhanced_data) * 100
        print(f"  {style}: {count} files ({percentage:.1f}%)")
    
    # Quality analysis
    quality_scores = [float(row.get('quality_score', 0)) for row in enhanced_data if row.get('quality_score')]
    if quality_scores:
        avg_quality = sum(quality_scores) / len(quality_scores)
        high_quality = sum(1 for score in quality_scores if score > 0.7)
        medium_quality = sum(1 for score in quality_scores if 0.3 <= score <= 0.7)
        low_quality = sum(1 for score in quality_scores if score < 0.3)
        
        print("\nQuality Score Analysis:")
        print(f"  Average Quality: {avg_quality:.3f}/1.0")
        print(f"  High Quality (>0.7): {high_quality} files")
        print(f"  Medium Quality (0.3-0.7): {medium_quality} files")
        print(f"  Low Quality (<0.3): {low_quality} files")
    
    # Engagement potential
    engagement_scores = [float(row.get('engagement_potential', 0)) for row in enhanced_data if row.get('engagement_potential')]
    if engagement_scores:
        avg_engagement = sum(engagement_scores) / len(engagement_scores)
        high_engagement = sum(1 for score in engagement_scores if score > 0.7)
        medium_engagement = sum(1 for score in engagement_scores if 0.3 <= score <= 0.7)
        low_engagement = sum(1 for score in engagement_scores if score < 0.3)
        
        print("\nEngagement Potential Analysis:")
        print(f"  Average Engagement: {avg_engagement:.3f}/1.0")
        print(f"  High Engagement (>0.7): {high_engagement} files")
        print(f"  Medium Engagement (0.3-0.7): {medium_engagement} files")
        print(f"  Low Engagement (<0.3): {low_engagement} files")
    
    print()

def analyze_resolution_distribution(enhanced_data):
    """Analyze resolution distribution."""
    print("📺 RESOLUTION DISTRIBUTION")
    print("=" * 50)
    
    resolution_dist = Counter(row.get('resolution_category', 'unknown') for row in enhanced_data)
    for resolution, count in resolution_dist.most_common():
        percentage = count / len(enhanced_data) * 100
        print(f"  {resolution}: {count} files ({percentage:.1f}%)")
    print()

def generate_top_content_recommendations(enhanced_data, n=10):
    """Generate top content recommendations based on engagement potential."""
    print("⭐ TOP CONTENT RECOMMENDATIONS")
    print("=" * 50)
    
    # Filter for files with analysis and sort by engagement potential
    analyzed_data = [row for row in enhanced_data if row.get('has_analysis') == 'True']
    if not analyzed_data:
        print("No analyzed content found for recommendations.")
        return
    
    # Sort by engagement potential
    analyzed_data.sort(key=lambda x: float(x.get('engagement_potential', 0)), reverse=True)
    top_content = analyzed_data[:n]
    
    for i, row in enumerate(top_content, 1):
        print(f"{i}. {row.get('filename', 'Unknown')}")
        print(f"   Content Type: {row.get('content_type', 'Unknown')}")
        engagement = row.get('engagement_potential', '0')
        quality = row.get('quality_score', '0')
        try:
            print(f"   Engagement: {float(engagement):.3f}")
            print(f"   Quality: {float(quality):.3f}")
        except ValueError:
            print(f"   Engagement: {engagement}")
            print(f"   Quality: {quality}")
        print(f"   Sentiment: {row.get('primary_sentiment', 'Unknown')}")
        print(f"   Visual Style: {row.get('primary_visual_style', 'Unknown')}")
        themes = row.get('themes', '')
        if themes:
            theme_list = themes.split(';')[:3]  # Top 3 themes
            print(f"   Themes: {', '.join(theme_list)}")
        print()

def generate_improvements_summary():
    """Generate a summary of the improvements made."""
    print("🔧 IMPROVEMENTS IMPLEMENTED")
    print("=" * 50)
    
    improvements = [
        "Enhanced Content Classification: 7 new content types (ai_generated, gaming, music, creative, political, educational, entertainment)",
        "Multi-dimensional Sentiment Analysis: 5 sentiment categories (positive, negative, neutral, energetic, calm)",
        "Visual Style Detection: 6 visual styles (cinematic, minimalist, colorful, dark, retro, futuristic)",
        "Quality Scoring: Technical quality assessment based on resolution, bitrate, and audio quality",
        "Complexity Analysis: 5 complexity dimensions (overall, text, duration, theme, technical)",
        "Engagement Prediction: Multi-factor engagement potential scoring",
        "Enhanced Metadata: Aspect ratio, resolution categories, audio/video presence detection",
        "Theme Extraction: Advanced pattern matching for theme identification",
        "Cross-modal Analysis: Integration of visual, audio, and text analysis",
        "Intelligent Organization: Smart categorization and content discovery"
    ]
    
    for i, improvement in enumerate(improvements, 1):
        print(f"{i}. {improvement}")
    
    print()

def main():
    """Main function to run the demo."""
    movies_dir = Path("/Users/steven/Movies")
    
    # Load the CSV files
    original_csv = movies_dir / "enhanced_content_analysis.csv"
    enhanced_csv = movies_dir / "enhanced_analysis" / "enhanced_content_analysis_improved.csv"
    
    print("🔍 ENHANCED CONTENT ANALYSIS DEMO")
    print("=" * 60)
    print()
    
    # Load data
    original_data = load_csv_data(original_csv)
    enhanced_data = load_csv_data(enhanced_csv)
    
    if original_data is None or enhanced_data is None:
        print("❌ Could not load CSV files. Please run the analyzers first.")
        return
    
    # Run comparisons and analysis
    generate_improvements_summary()
    compare_analysis_coverage(original_data, enhanced_data)
    compare_content_classification(original_data, enhanced_data)
    analyze_enhanced_features(enhanced_data)
    analyze_resolution_distribution(enhanced_data)
    generate_top_content_recommendations(enhanced_data)
    
    print("✅ Demo completed! Check the enhanced_analysis/ directory for detailed results.")
    print("\n📁 Generated Files:")
    print("  - enhanced_content_analysis_improved.csv (Enhanced CSV with all improvements)")
    print("  - enhanced_analysis_summary.txt (Detailed statistics)")
    print("  - deep_read_analysis_report.md (Comprehensive analysis report)")

if __name__ == "__main__":
    main()