"""
Data Processing Pandas Demo 3

This module provides functionality for data processing pandas demo 3.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100

#!/usr/bin/env python3
"""
Demo Script: Enhanced Content Analysis Improvements

This script demonstrates the improvements made to the content analysis system
and generates comparison reports between the original and enhanced versions.
"""

import pandas as pd
import os
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import json


def load_csv_data(csv_path):
    """Load CSV data and return as DataFrame."""
    try:
        return pd.read_csv(csv_path)
    except Exception as e:
        logger.info(f"Error loading {csv_path}: {e}")
        return None


def compare_analysis_coverage(original_df, enhanced_df):
    """Compare analysis coverage between original and enhanced versions."""
    logger.info("📊 ANALYSIS COVERAGE COMPARISON")
    logger.info("=" * 50)

    original_analyzed = original_df["has_analysis"].sum()
    enhanced_analyzed = enhanced_df["has_analysis"].sum()
    total_files = len(enhanced_df)

    logger.info(f"Total Files: {total_files}")
    logger.info(
        f"Original Analysis Coverage: {original_analyzed} files ({original_analyzed/total_files*CONSTANT_100:.1f}%)"
    )
    logger.info(
        f"Enhanced Analysis Coverage: {enhanced_analyzed} files ({enhanced_analyzed/total_files*CONSTANT_100:.1f}%)"
    )
    logger.info(f"Improvement: +{enhanced_analyzed - original_analyzed} files")
    print()


def compare_content_classification(original_df, enhanced_df):
    """Compare content classification improvements."""
    logger.info("🏷️  CONTENT CLASSIFICATION IMPROVEMENTS")
    logger.info("=" * 50)

    # Original classification
    original_types = Counter(original_df["content_type"])
    logger.info("Original Classification:")
    for content_type, count in original_types.most_common():
        percentage = count / len(original_df) * CONSTANT_100
        logger.info(f"  {content_type}: {count} files ({percentage:.1f}%)")

    logger.info("\nEnhanced Classification:")
    enhanced_types = Counter(enhanced_df["content_type"])
    for content_type, count in enhanced_types.most_common():
        percentage = count / len(enhanced_df) * CONSTANT_100
        logger.info(f"  {content_type}: {count} files ({percentage:.1f}%)")

    logger.info(f"\nClassification Improvement: {len(enhanced_types)} vs {len(original_types)} categories")
    print()


def analyze_enhanced_features(enhanced_df):
    """Analyze the new enhanced features."""
    logger.info("🚀 ENHANCED FEATURES ANALYSIS")
    logger.info("=" * 50)

    # Sentiment analysis
    sentiment_dist = Counter(enhanced_df["primary_sentiment"])
    logger.info("Sentiment Distribution:")
    for sentiment, count in sentiment_dist.most_common():
        percentage = count / len(enhanced_df) * CONSTANT_100
        logger.info(f"  {sentiment}: {count} files ({percentage:.1f}%)")

    # Visual style analysis
    visual_style_dist = Counter(enhanced_df["primary_visual_style"])
    logger.info(f"\nVisual Style Distribution:")
    for style, count in visual_style_dist.most_common():
        percentage = count / len(enhanced_df) * CONSTANT_100
        logger.info(f"  {style}: {count} files ({percentage:.1f}%)")

    # Quality analysis
    quality_scores = enhanced_df["quality_score"].dropna()
    if len(quality_scores) > 0:
        logger.info(f"\nQuality Score Analysis:")
        logger.info(f"  Average Quality: {quality_scores.mean():.3f}/1.0")
        logger.info(f"  High Quality (>0.7): {(quality_scores > 0.7).sum()} files")
        logger.info(f"  Medium Quality (0.3-0.7): {((quality_scores >= 0.3) & (quality_scores <= 0.7)).sum()} files")
        logger.info(f"  Low Quality (<0.3): {(quality_scores < 0.3).sum()} files")

    # Engagement potential
    engagement_scores = enhanced_df["engagement_potential"].dropna()
    if len(engagement_scores) > 0:
        logger.info(f"\nEngagement Potential Analysis:")
        logger.info(f"  Average Engagement: {engagement_scores.mean():.3f}/1.0")
        logger.info(f"  High Engagement (>0.7): {(engagement_scores > 0.7).sum()} files")
        logger.info(
            f"  Medium Engagement (0.3-0.7): {((engagement_scores >= 0.3) & (engagement_scores <= 0.7)).sum()} files"
        )
        logger.info(f"  Low Engagement (<0.3): {(engagement_scores < 0.3).sum()} files")

    print()


def analyze_complexity_metrics(enhanced_df):
    """Analyze complexity metrics."""
    logger.info("🧠 COMPLEXITY ANALYSIS")
    logger.info("=" * 50)

    complexity_cols = [
        "overall_complexity",
        "text_complexity",
        "duration_complexity",
        "theme_complexity",
        "technical_complexity",
    ]

    for col in complexity_cols:
        if col in enhanced_df.columns:
            values = enhanced_df[col].dropna()
            if len(values) > 0:
                logger.info(f"{col.replace('_', ' ').title()}:")
                logger.info(f"  Average: {values.mean():.2f}")
                logger.info(f"  Range: {values.min():.2f} - {values.max():.2f}")
                logger.info(f"  High Complexity (>5): {(values > 5).sum()} files")
                print()


def generate_top_content_recommendations(enhanced_df, n=10):
    """Generate top content recommendations based on engagement potential."""
    logger.info("⭐ TOP CONTENT RECOMMENDATIONS")
    logger.info("=" * 50)

    # Filter for files with analysis and sort by engagement potential
    analyzed_df = enhanced_df[enhanced_df["has_analysis"] == True].copy()
    if len(analyzed_df) == 0:
        logger.info("No analyzed content found for recommendations.")
        return

    top_content = analyzed_df.nlargest(n, "engagement_potential")

    for i, (_, row) in enumerate(top_content.iterrows(), 1):
        logger.info(f"{i}. {row['filename']}")
        logger.info(f"   Content Type: {row['content_type']}")
        logger.info(f"   Engagement: {row['engagement_potential']:.3f}")
        logger.info(f"   Quality: {row['quality_score']:.3f}")
        logger.info(f"   Sentiment: {row['primary_sentiment']}")
        logger.info(f"   Visual Style: {row['primary_visual_style']}")
        if pd.notna(row["themes"]) and row["themes"]:
            themes = row["themes"].split(";")[:3]  # Top 3 themes
            logger.info(f"   Themes: {', '.join(themes)}")
        print()


def generate_insights_report(enhanced_df):
    """Generate comprehensive insights report."""
    logger.info("📈 COMPREHENSIVE INSIGHTS REPORT")
    logger.info("=" * 60)

    total_files = len(enhanced_df)
    analyzed_files = enhanced_df["has_analysis"].sum()

    logger.info(f"Dataset Overview:")
    logger.info(f"  Total Files: {total_files}")
    logger.info(f"  Analyzed Files: {analyzed_files} ({analyzed_files/total_files*CONSTANT_100:.1f}%)")
    logger.info(f"  File Types: {enhanced_df['file_extension'].nunique()} different extensions")
    logger.info(f"  Content Categories: {enhanced_df['content_type'].nunique()} different types")
    print()

    # Content type insights
    logger.info("Content Type Insights:")
    content_dist = enhanced_df["content_type"].value_counts()
    for content_type, count in content_dist.head(5).items():
        percentage = count / total_files * CONSTANT_100
        avg_engagement = enhanced_df[enhanced_df["content_type"] == content_type]["engagement_potential"].mean()
        logger.info(f"  {content_type}: {count} files ({percentage:.1f}%) - Avg Engagement: {avg_engagement:.3f}")
    print()

    # Quality insights
    quality_data = enhanced_df["quality_score"].dropna()
    if len(quality_data) > 0:
        logger.info("Quality Insights:")
        logger.info(f"  Average Quality Score: {quality_data.mean():.3f}/1.0")
        logger.info(
            f"  High Quality Files: {(quality_data > 0.7).sum()} ({(quality_data > 0.7).sum()/len(quality_data)*CONSTANT_100:.1f}%)"
        )
        logger.info(f"  Quality Range: {quality_data.min():.3f} - {quality_data.max():.3f}")
        print()

    # Engagement insights
    engagement_data = enhanced_df["engagement_potential"].dropna()
    if len(engagement_data) > 0:
        logger.info("Engagement Insights:")
        logger.info(f"  Average Engagement: {engagement_data.mean():.3f}/1.0")
        logger.info(
            f"  High Engagement Files: {(engagement_data > 0.7).sum()} ({(engagement_data > 0.7).sum()/len(engagement_data)*CONSTANT_100:.1f}%)"
        )
        logger.info(f"  Engagement Range: {engagement_data.min():.3f} - {engagement_data.max():.3f}")
        print()

    # Resolution insights
    resolution_dist = enhanced_df["resolution_category"].value_counts()
    logger.info("Resolution Distribution:")
    for resolution, count in resolution_dist.items():
        percentage = count / total_files * CONSTANT_100
        logger.info(f"  {resolution}: {count} files ({percentage:.1f}%)")
    print()


def main():
    """Main function to run the demo."""
    movies_dir = Path(Path("/Users/steven/Movies"))

    # Load the CSV files
    original_csv = movies_dir / "enhanced_content_analysis.csv"
    enhanced_csv = movies_dir / "enhanced_analysis" / "enhanced_content_analysis_improved.csv"

    logger.info("🔍 ENHANCED CONTENT ANALYSIS DEMO")
    logger.info("=" * 60)
    print()

    # Load data
    original_df = load_csv_data(original_csv)
    enhanced_df = load_csv_data(enhanced_csv)

    if original_df is None or enhanced_df is None:
        logger.info("❌ Could not load CSV files. Please run the analyzers first.")
        return

    # Run comparisons and analysis
    compare_analysis_coverage(original_df, enhanced_df)
    compare_content_classification(original_df, enhanced_df)
    analyze_enhanced_features(enhanced_df)
    analyze_complexity_metrics(enhanced_df)
    generate_top_content_recommendations(enhanced_df)
    generate_insights_report(enhanced_df)

    logger.info("✅ Demo completed! Check the enhanced_analysis/ directory for detailed results.")


if __name__ == "__main__":
    main()
