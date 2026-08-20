#!/usr/bin/env python3
"""
Income Opportunities Analysis Tool
Analyzes the INCOME_OPPORTUNITIES.csv file and generates insights
"""

import pandas as pd
import sys
from pathlib import Path

def load_data():
    """Load the income opportunities CSV"""
    csv_path = Path(__file__).parent / "INCOME_OPPORTUNITIES.csv"
    
    if not csv_path.exists():
        print(f"Error: {csv_path} not found")
        sys.exit(1)
    
    # Read CSV with proper handling of commas in fields
    try:
        df = pd.read_csv(csv_path, on_bad_lines='skip', engine='python')
    except:
        # Fallback: read with quote handling
        df = pd.read_csv(csv_path, quoting=1)  # QUOTE_ALL
    return df

def analyze_by_category(df):
    """Analyze revenue by category"""
    print("\n" + "="*80)
    print("REVENUE BY CATEGORY")
    print("="*80)
    
    category_summary = df.groupby('Category').agg({
        'Potential Revenue (Year 1)': 'sum',
        'Potential Revenue (Year 2)': 'sum',
        'Potential Revenue (Year 3)': 'sum',
        'Revenue Stream': 'count'
    }).round(0)
    
    category_summary.columns = ['Year 1 Total', 'Year 2 Total', 'Year 3 Total', 'Count']
    category_summary = category_summary.sort_values('Year 3 Total', ascending=False)
    
    print(category_summary.to_string())
    
    return category_summary

def analyze_by_status(df):
    """Analyze revenue by implementation status"""
    print("\n" + "="*80)
    print("REVENUE BY STATUS")
    print("="*80)
    
    status_summary = df.groupby('Status').agg({
        'Potential Revenue (Year 1)': 'sum',
        'Potential Revenue (Year 2)': 'sum',
        'Potential Revenue (Year 3)': 'sum',
        'Revenue Stream': 'count'
    }).round(0)
    
    status_summary.columns = ['Year 1 Total', 'Year 2 Total', 'Year 3 Total', 'Count']
    status_summary = status_summary.sort_values('Year 3 Total', ascending=False)
    
    print(status_summary.to_string())
    
    return status_summary

def analyze_by_priority(df):
    """Analyze revenue by priority"""
    print("\n" + "="*80)
    print("REVENUE BY PRIORITY")
    print("="*80)
    
    priority_summary = df.groupby('Priority').agg({
        'Potential Revenue (Year 1)': 'sum',
        'Potential Revenue (Year 2)': 'sum',
        'Potential Revenue (Year 3)': 'sum',
        'Revenue Stream': 'count'
    }).round(0)
    
    priority_summary.columns = ['Year 1 Total', 'Year 2 Total', 'Year 3 Total', 'Count']
    priority_summary = priority_summary.sort_values('Year 3 Total', ascending=False)
    
    print(priority_summary.to_string())
    
    return priority_summary

def analyze_by_type(df):
    """Analyze passive vs active income"""
    print("\n" + "="*80)
    print("PASSIVE vs ACTIVE INCOME")
    print("="*80)
    
    type_summary = df.groupby('Type').agg({
        'Potential Revenue (Year 1)': 'sum',
        'Potential Revenue (Year 2)': 'sum',
        'Potential Revenue (Year 3)': 'sum',
        'Revenue Stream': 'count'
    }).round(0)
    
    type_summary.columns = ['Year 1 Total', 'Year 2 Total', 'Year 3 Total', 'Count']
    
    print(type_summary.to_string())
    
    # Calculate percentages
    total_y3 = type_summary['Year 3 Total'].sum()
    if total_y3 > 0:
        print("\nYear 3 Percentage Breakdown:")
        for idx, row in type_summary.iterrows():
            pct = (row['Year 3 Total'] / total_y3) * 100
            print(f"  {idx}: {pct:.1f}%")
    
    return type_summary

def top_opportunities(df, n=10):
    """Show top N opportunities by Year 3 revenue"""
    print("\n" + "="*80)
    print(f"TOP {n} OPPORTUNITIES (By Year 3 Revenue)")
    print("="*80)
    
    top = df.nlargest(n, 'Potential Revenue (Year 3)')[
        ['Revenue Stream', 'Category', 'Status', 'Priority', 
         'Potential Revenue (Year 1)', 'Potential Revenue (Year 2)', 
         'Potential Revenue (Year 3)']
    ]
    
    print(top.to_string(index=False))
    
    return top

def ready_to_implement(df):
    """Show opportunities ready to implement"""
    print("\n" + "="*80)
    print("READY TO IMPLEMENT (Status: Ready or Active)")
    print("="*80)
    
    ready = df[df['Status'].isin(['Ready', 'Active'])].sort_values(
        'Potential Revenue (Year 3)', ascending=False
    )[
        ['Revenue Stream', 'Category', 'Type', 'Priority',
         'Potential Revenue (Year 1)', 'Potential Revenue (Year 2)', 
         'Potential Revenue (Year 3)', 'Implementation Status']
    ]
    
    print(f"\nTotal Ready: {len(ready)} opportunities")
    print(f"Year 1 Potential: ${ready['Potential Revenue (Year 1)'].sum():,.0f}")
    print(f"Year 2 Potential: ${ready['Potential Revenue (Year 2)'].sum():,.0f}")
    print(f"Year 3 Potential: ${ready['Potential Revenue (Year 3)'].sum():,.0f}")
    print("\n" + ready.to_string(index=False))
    
    return ready

def missing_opportunities(df):
    """Show opportunities not yet explored"""
    print("\n" + "="*80)
    print("MISSING OPPORTUNITIES (Status: Not Found)")
    print("="*80)
    
    missing = df[df['Status'] == 'Not Found'].sort_values(
        'Potential Revenue (Year 3)', ascending=False
    )[
        ['Revenue Stream', 'Category', 'Priority',
         'Potential Revenue (Year 1)', 'Potential Revenue (Year 2)', 
         'Potential Revenue (Year 3)', 'Notes']
    ]
    
    print(f"\nTotal Missing: {len(missing)} opportunities")
    print(f"Year 3 Potential (if implemented): ${missing['Potential Revenue (Year 3)'].sum():,.0f}")
    print("\n" + missing.to_string(index=False))
    
    return missing

def generate_summary_stats(df):
    """Generate overall summary statistics"""
    print("\n" + "="*80)
    print("OVERALL SUMMARY STATISTICS")
    print("="*80)
    
    total_y1 = df['Potential Revenue (Year 1)'].sum()
    total_y2 = df['Potential Revenue (Year 2)'].sum()
    total_y3 = df['Potential Revenue (Year 3)'].sum()
    
    ready_y3 = df[df['Status'].isin(['Ready', 'Active'])]['Potential Revenue (Year 3)'].sum()
    missing_y3 = df[df['Status'] == 'Not Found']['Potential Revenue (Year 3)'].sum()
    
    passive_y3 = df[df['Type'] == 'Passive']['Potential Revenue (Year 3)'].sum()
    active_y3 = df[df['Type'] == 'Active']['Potential Revenue (Year 3)'].sum()
    
    print(f"\nTotal Revenue Streams: {len(df)}")
    print(f"\nTotal Potential Revenue:")
    print(f"  Year 1: ${total_y1:,.0f}")
    print(f"  Year 2: ${total_y2:,.0f}")
    print(f"  Year 3: ${total_y3:,.0f}")
    
    print(f"\nBy Status:")
    print(f"  Ready/Active (Year 3): ${ready_y3:,.0f} ({ready_y3/total_y3*100:.1f}%)")
    print(f"  Not Found (Year 3): ${missing_y3:,.0f} ({missing_y3/total_y3*100:.1f}%)")
    
    print(f"\nBy Type:")
    print(f"  Passive (Year 3): ${passive_y3:,.0f} ({passive_y3/total_y3*100:.1f}%)")
    print(f"  Active (Year 3): ${active_y3:,.0f} ({active_y3/total_y3*100:.1f}%)")
    
    print(f"\nBy Priority:")
    high_y3 = df[df['Priority'] == 'High']['Potential Revenue (Year 3)'].sum()
    medium_y3 = df[df['Priority'] == 'Medium']['Potential Revenue (Year 3)'].sum()
    low_y3 = df[df['Priority'] == 'Low']['Potential Revenue (Year 3)'].sum()
    print(f"  High (Year 3): ${high_y3:,.0f} ({high_y3/total_y3*100:.1f}%)")
    print(f"  Medium (Year 3): ${medium_y3:,.0f} ({medium_y3/total_y3*100:.1f}%)")
    print(f"  Low (Year 3): ${low_y3:,.0f} ({low_y3/total_y3*100:.1f}%)")

def main():
    """Main analysis function"""
    print("="*80)
    print("INCOME OPPORTUNITIES ANALYSIS")
    print("="*80)
    
    df = load_data()
    
    # Run all analyses
    generate_summary_stats(df)
    top_opportunities(df, 15)
    ready_to_implement(df)
    analyze_by_category(df)
    analyze_by_status(df)
    analyze_by_priority(df)
    analyze_by_type(df)
    missing_opportunities(df)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\nNext Steps:")
    print("1. Focus on 'Ready to Implement' opportunities")
    print("2. Prioritize 'High Priority' streams")
    print("3. Explore 'Missing Opportunities' with high potential")
    print("4. Build passive income streams for long-term growth")
    print()

if __name__ == "__main__":
    main()
