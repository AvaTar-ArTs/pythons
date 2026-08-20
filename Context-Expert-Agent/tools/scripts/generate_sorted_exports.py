#!/usr/bin/env python3
"""
Generate sorted CSV exports for easy analysis
"""

import pandas as pd
from pathlib import Path

def load_data():
    """Load the income opportunities CSV"""
    csv_path = Path(__file__).parent / "INCOME_OPPORTUNITIES.csv"
    df = pd.read_csv(csv_path, on_bad_lines='skip', engine='python')
    return df

def calculate_metrics(df):
    """Calculate advanced metrics"""
    df = df.copy()

    # Implementation difficulty
    difficulty_map = {
        'Ready': 1, 'Active': 1, 'Available': 2,
        'Partially Explored': 2, 'In Development': 3, 'Not Found': 5
    }
    df['Implementation_Difficulty'] = df['Status'].map(difficulty_map).fillna(3)
    df['ROI_Score'] = df['Potential Revenue (Year 3)'] / df['Implementation_Difficulty']
    df['Quick_Win_Score'] = df['Potential Revenue (Year 1)'] / df['Implementation_Difficulty']

    # Growth rates
    df['Y1_Y3_CAGR'] = (((df['Potential Revenue (Year 3)'] / df['Potential Revenue (Year 1)'].replace(0, 1)) ** (1/2)) - 1) * 100

    # Revenue contribution
    total_y3 = df['Potential Revenue (Year 3)'].sum()
    df['Revenue_Contribution_Pct'] = (df['Potential Revenue (Year 3)'] / total_y3) * 100

    return df

def main():
    df = load_data()
    df = calculate_metrics(df)

    base_dir = Path(__file__).parent

    # 1. Sorted by Quick Win Score
    quick_wins = df.nlargest(62, 'Quick_Win_Score')[
        ['Revenue Stream', 'Status', 'Priority', 'Type', 'Category',
         'Potential Revenue (Year 1)', 'Potential Revenue (Year 2)',
         'Potential Revenue (Year 3)', 'Quick_Win_Score', 'Implementation_Difficulty']
    ].sort_values('Quick_Win_Score', ascending=False)
    quick_wins.to_csv(base_dir / 'SORTED_QUICK_WINS.csv', index=False)

    # 2. Sorted by ROI Score
    roi_sorted = df.nlargest(62, 'ROI_Score')[
        ['Revenue Stream', 'Status', 'Priority', 'Type', 'Category',
         'Potential Revenue (Year 3)', 'ROI_Score', 'Implementation_Difficulty']
    ].sort_values('ROI_Score', ascending=False)
    roi_sorted.to_csv(base_dir / 'SORTED_BY_ROI.csv', index=False)

    # 3. Sorted by Year 3 Revenue
    revenue_sorted = df.nlargest(62, 'Potential Revenue (Year 3)')[
        ['Revenue Stream', 'Status', 'Priority', 'Type', 'Category',
         'Potential Revenue (Year 1)', 'Potential Revenue (Year 2)',
         'Potential Revenue (Year 3)', 'Revenue_Contribution_Pct']
    ].sort_values('Potential Revenue (Year 3)', ascending=False)
    revenue_sorted.to_csv(base_dir / 'SORTED_BY_REVENUE.csv', index=False)

    # 4. Sorted by Implementation Readiness
    status_order = {'Ready': 1, 'Active': 2, 'Available': 3,
                   'Partially Explored': 4, 'In Development': 5, 'Not Found': 6}
    df['Status_Order'] = df['Status'].map(status_order)
    readiness_sorted = df.sort_values(['Status_Order', 'Potential Revenue (Year 3)'],
                                     ascending=[True, False])[
        ['Revenue Stream', 'Status', 'Priority', 'Type', 'Category',
         'Potential Revenue (Year 1)', 'Potential Revenue (Year 2)',
         'Potential Revenue (Year 3)', 'Implementation_Difficulty']
    ]
    readiness_sorted.to_csv(base_dir / 'SORTED_BY_READINESS.csv', index=False)

    # 5. Ready to Implement Only
    ready_only = df[df['Status'].isin(['Ready', 'Active'])].sort_values(
        'Potential Revenue (Year 3)', ascending=False
    )[
        ['Revenue Stream', 'Status', 'Priority', 'Type', 'Category',
         'Potential Revenue (Year 1)', 'Potential Revenue (Year 2)',
         'Potential Revenue (Year 3)', 'Implementation Status']
    ]
    ready_only.to_csv(base_dir / 'READY_TO_IMPLEMENT.csv', index=False)

    # 6. By Category Summary
    category_summary = df.groupby('Category').agg({
        'Potential Revenue (Year 1)': 'sum',
        'Potential Revenue (Year 2)': 'sum',
        'Potential Revenue (Year 3)': 'sum',
        'Revenue Stream': 'count'
    }).round(0)
    category_summary.columns = ['Year 1 Total', 'Year 2 Total', 'Year 3 Total', 'Count']
    category_summary = category_summary.sort_values('Year 3 Total', ascending=False)
    category_summary.to_csv(base_dir / 'SUMMARY_BY_CATEGORY.csv')

    # 7. By Status Summary
    status_summary = df.groupby('Status').agg({
        'Potential Revenue (Year 1)': 'sum',
        'Potential Revenue (Year 2)': 'sum',
        'Potential Revenue (Year 3)': 'sum',
        'Revenue Stream': 'count'
    }).round(0)
    status_summary.columns = ['Year 1 Total', 'Year 2 Total', 'Year 3 Total', 'Count']
    status_summary = status_summary.sort_values('Year 3 Total', ascending=False)
    status_summary.to_csv(base_dir / 'SUMMARY_BY_STATUS.csv')

    print("✅ Generated sorted CSV exports:")
    print("  - SORTED_QUICK_WINS.csv")
    print("  - SORTED_BY_ROI.csv")
    print("  - SORTED_BY_REVENUE.csv")
    print("  - SORTED_BY_READINESS.csv")
    print("  - READY_TO_IMPLEMENT.csv")
    print("  - SUMMARY_BY_CATEGORY.csv")
    print("  - SUMMARY_BY_STATUS.csv")

if __name__ == "__main__":
    main()

