#!/usr/bin/env python3
"""
Suno Analytics Tools - Extracted from jupyter notebook
Useful functions for analyzing Suno music data
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict
import plotly.express as px


def analyze_sentiment(text: str) -> int:
    """
    Simple sentiment analysis based on keyword matching.
    Returns positive score for uplifting words, negative for darker themes.
    """
    positive_words = ["magic", "enchanting", "joyful", "empowerment", "serenity", 
                      "love", "hope", "bright", "beautiful", "happy"]
    negative_words = ["melancholy", "haunting", "gritty", "feral", "imperfection",
                      "dark", "shadow", "pain", "lost", "broken"]
    
    text_lower = text.lower()
    positive_score = sum(1 for word in positive_words if word in text_lower)
    negative_score = sum(1 for word in negative_words if word in text_lower)
    
    return positive_score - negative_score


def analyze_tags(df: pd.DataFrame, tag_column: str = 'Keys') -> pd.Series:
    """
    Analyze tag distribution from comma-separated tag strings.
    Returns a Series with tag counts sorted by frequency.
    """
    if tag_column not in df.columns:
        raise ValueError(f"Column '{tag_column}' not found in DataFrame")
    
    tag_counts = df[tag_column].str.split(", ").explode().value_counts()
    return tag_counts


def temporal_analysis(df: pd.DataFrame, date_column: str = 'Created time') -> pd.DataFrame:
    """
    Analyze release patterns over time.
    Returns monthly statistics with total songs and unique releases.
    """
    if date_column not in df.columns:
        raise ValueError(f"Column '{date_column}' not found in DataFrame")
    
    # Ensure date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column])
    
    df['Release Month'] = df[date_column].dt.month_name()
    
    monthly_stats = df.groupby('Release Month').agg({
        df.columns[0]: 'count',  # Assuming first column has song titles
        'Song URL': 'nunique' if 'Song URL' in df.columns else 'count'
    }).rename(columns={
        df.columns[0]: 'Total Songs',
        'Song URL': 'Unique Releases'
    })
    
    return monthly_stats


def plot_release_timeline(df: pd.DataFrame, date_column: str = 'Created time'):
    """
    Create an interactive timeline plot of daily song releases.
    """
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column])
    
    daily_counts = df.groupby(df[date_column].dt.date).size().reset_index(name='count')
    daily_counts.columns = [date_column, 'count']
    
    fig = px.line(
        daily_counts,
        x=date_column,
        y='count',
        title='Daily Song Releases Over Time',
        labels={date_column: 'Date', 'count': 'Number of Releases'}
    )
    
    return fig


def load_suno_csv(csv_path: Path) -> pd.DataFrame:
    """
    Load and validate Suno CSV data.
    """
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    df = pd.read_csv(csv_path, parse_dates=['Created time'] if 'Created time' in pd.read_csv(csv_path, nrows=1).columns else None)
    
    print(f"? Loaded {len(df)} tracks")
    if 'Created time' in df.columns:
        print(f"?? Date range: {df['Created time'].min()} to {df['Created time'].max()}")
    
    return df


def export_analysis_report(df: pd.DataFrame, output_dir: Path):
    """
    Generate comprehensive analysis report with all metrics.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Tag analysis
    if 'Keys' in df.columns:
        tag_counts = analyze_tags(df)
        tag_counts.to_csv(output_dir / 'tag_analysis.csv')
    
    # Temporal analysis
    if 'Created time' in df.columns:
        monthly_stats = temporal_analysis(df)
        monthly_stats.to_csv(output_dir / 'temporal_analysis.csv')
    
    # Sentiment analysis
    if 'Analysis' in df.columns:
        df['Sentiment Score'] = df['Analysis'].apply(analyze_sentiment)
        df[['Song Title', 'Sentiment Score']].to_csv(output_dir / 'sentiment_analysis.csv', index=False)
    
    print(f"? Analysis reports saved to: {output_dir}")


if __name__ == '__main__':
    """
    Example usage:
    
    from pathlib import Path
    import suno_analytics_tools as sat
    
    # Load data
    df = sat.load_suno_csv('/path/to/suno_data.csv')
    
    # Analyze tags
    tags = sat.analyze_tags(df)
    print(tags.head(10))
    
    # Temporal analysis
    monthly = sat.temporal_analysis(df)
    print(monthly)
    
    # Plot timeline
    fig = sat.plot_release_timeline(df)
    fig.show()
    
    # Export full report
    sat.export_analysis_report(df, Path('./suno_reports'))
    """
    print("Suno Analytics Tools loaded successfully!")
    print("Import this module to use the analysis functions.")
