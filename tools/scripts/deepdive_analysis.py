#!/usr/bin/env python3
"""
Deep Dive Income Opportunities Analysis
Advanced analysis with ROI, risk assessment, growth rates, and improvement recommendations
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

def load_data():
    """Load the income opportunities CSV"""
    csv_path = Path(__file__).parent / "INCOME_OPPORTUNITIES.csv"

    if not csv_path.exists():
        print(f"Error: {csv_path} not found")
        sys.exit(1)

    try:
        df = pd.read_csv(csv_path, on_bad_lines='skip', engine='python')
    except:
        df = pd.read_csv(csv_path, quoting=1)

    return df

def calculate_metrics(df):
    """Calculate advanced metrics"""
    df = df.copy()

    # Growth rates
    df['Y1_Y2_Growth'] = ((df['Potential Revenue (Year 2)'] - df['Potential Revenue (Year 1)']) /
                          df['Potential Revenue (Year 1)'].replace(0, 1)) * 100
    df['Y2_Y3_Growth'] = ((df['Potential Revenue (Year 3)'] - df['Potential Revenue (Year 2)']) /
                          df['Potential Revenue (Year 2)'].replace(0, 1)) * 100
    df['Y1_Y3_CAGR'] = (((df['Potential Revenue (Year 3)'] / df['Potential Revenue (Year 1)'].replace(0, 1)) ** (1/2)) - 1) * 100

    # ROI Score (simplified: revenue potential / implementation difficulty)
    # Implementation difficulty: Ready=1, Active=1, Available=2, In Development=3, Not Found=5
    difficulty_map = {
        'Ready': 1,
        'Active': 1,
        'Available': 2,
        'Partially Explored': 2,
        'In Development': 3,
        'Not Found': 5
    }
    df['Implementation_Difficulty'] = df['Status'].map(difficulty_map).fillna(3)
    df['ROI_Score'] = df['Potential Revenue (Year 3)'] / df['Implementation_Difficulty']

    # Quick Win Score (Year 1 revenue potential * ease of implementation)
    df['Quick_Win_Score'] = df['Potential Revenue (Year 1)'] / df['Implementation_Difficulty']

    # Revenue Concentration (top opportunities)
    total_y3 = df['Potential Revenue (Year 3)'].sum()
    df['Revenue_Contribution_Pct'] = (df['Potential Revenue (Year 3)'] / total_y3) * 100

    # Risk Score (inverse of status readiness)
    df['Risk_Score'] = df['Implementation_Difficulty'] * (df['Priority'].map({'High': 1, 'Medium': 2, 'Low': 3}).fillna(2))

    return df

def print_section_header(title):
    """Print formatted section header"""
    print("\n" + "="*100)
    print(f"  {title}")
    print("="*100)

def analyze_quick_wins(df):
    """Identify quick win opportunities"""
    print_section_header("🚀 QUICK WINS (High Year 1 Revenue + Easy Implementation)")

    quick_wins = df.nlargest(15, 'Quick_Win_Score')[
        ['Revenue Stream', 'Status', 'Priority', 'Type',
         'Potential Revenue (Year 1)', 'Quick_Win_Score', 'Implementation_Difficulty']
    ].sort_values('Quick_Win_Score', ascending=False)

    print(f"\nTop {len(quick_wins)} Quick Win Opportunities:")
    print(quick_wins.to_string(index=False))

    return quick_wins

def analyze_roi_leaders(df):
    """Analyze highest ROI opportunities"""
    print_section_header("💰 TOP ROI OPPORTUNITIES (Best Return on Implementation Effort)")

    roi_leaders = df.nlargest(20, 'ROI_Score')[
        ['Revenue Stream', 'Status', 'Priority', 'Type',
         'Potential Revenue (Year 3)', 'ROI_Score', 'Implementation_Difficulty']
    ].sort_values('ROI_Score', ascending=False)

    print(f"\nTop {len(roi_leaders)} ROI Opportunities:")
    print(roi_leaders.to_string(index=False))

    return roi_leaders

def analyze_growth_leaders(df):
    """Analyze fastest growing opportunities"""
    print_section_header("📈 FASTEST GROWING OPPORTUNITIES")

    # Filter out opportunities with no Year 1 revenue for meaningful growth calculation
    growing = df[df['Potential Revenue (Year 1)'] > 0].nlargest(20, 'Y1_Y3_CAGR')[
        ['Revenue Stream', 'Status', 'Priority',
         'Potential Revenue (Year 1)', 'Potential Revenue (Year 2)', 'Potential Revenue (Year 3)',
         'Y1_Y2_Growth', 'Y2_Y3_Growth', 'Y1_Y3_CAGR']
    ].sort_values('Y1_Y3_CAGR', ascending=False)

    print(f"\nTop {len(growing)} Fastest Growing Opportunities (with Year 1 revenue):")
    print(growing.to_string(index=False))

    return growing

def analyze_revenue_concentration(df):
    """Analyze revenue concentration"""
    print_section_header("🎯 REVENUE CONCENTRATION ANALYSIS")

    # Top 10 contribution
    top_10 = df.nlargest(10, 'Potential Revenue (Year 3)')
    top_10_pct = top_10['Revenue_Contribution_Pct'].sum()

    # Top 5 contribution
    top_5 = df.nlargest(5, 'Potential Revenue (Year 3)')
    top_5_pct = top_5['Revenue_Contribution_Pct'].sum()

    print(f"\nRevenue Concentration:")
    print(f"  Top 5 opportunities: {top_5_pct:.1f}% of total Year 3 revenue")
    print(f"  Top 10 opportunities: {top_10_pct:.1f}% of total Year 3 revenue")

    print(f"\nTop 10 Revenue Contributors:")
    top_10_display = top_10[['Revenue Stream', 'Status', 'Priority', 'Potential Revenue (Year 3)', 'Revenue_Contribution_Pct']]
    print(top_10_display.to_string(index=False))

    return top_10

def analyze_risk_profile(df):
    """Analyze risk profile"""
    print_section_header("⚠️  RISK ANALYSIS (Low Risk = Ready/Active + High Priority)")

    # Low risk opportunities
    low_risk = df[(df['Status'].isin(['Ready', 'Active'])) & (df['Priority'] == 'High')].sort_values(
        'Potential Revenue (Year 3)', ascending=False
    )[
        ['Revenue Stream', 'Status', 'Priority', 'Type', 'Potential Revenue (Year 3)', 'Risk_Score']
    ]

    print(f"\nLow Risk, High Reward Opportunities ({len(low_risk)} total):")
    print(low_risk.to_string(index=False))

    # High risk opportunities
    high_risk = df[df['Risk_Score'] >= 10].sort_values('Potential Revenue (Year 3)', ascending=False)[
        ['Revenue Stream', 'Status', 'Priority', 'Potential Revenue (Year 3)', 'Risk_Score']
    ]

    print(f"\nHigh Risk Opportunities (Status: Not Found/In Development + Lower Priority):")
    print(high_risk.to_string(index=False))

    return low_risk, high_risk

def analyze_by_implementation_readiness(df):
    """Analyze opportunities sorted by implementation readiness"""
    print_section_header("⚙️  IMPLEMENTATION READINESS SORTED VIEW")

    # Define implementation order
    status_order = {
        'Ready': 1,
        'Active': 2,
        'Available': 3,
        'Partially Explored': 4,
        'In Development': 5,
        'Not Found': 6
    }

    df['Status_Order'] = df['Status'].map(status_order)

    ready_sorted = df.sort_values(['Status_Order', 'Potential Revenue (Year 3)'], ascending=[True, False])[
        ['Revenue Stream', 'Status', 'Priority', 'Type',
         'Potential Revenue (Year 1)', 'Potential Revenue (Year 2)', 'Potential Revenue (Year 3)',
         'Implementation_Difficulty']
    ]

    print(f"\nAll Opportunities Sorted by Implementation Readiness:")
    print(ready_sorted.to_string(index=False))

    return ready_sorted

def analyze_passive_income_breakdown(df):
    """Deep dive into passive income opportunities"""
    print_section_header("💤 PASSIVE INCOME DEEP DIVE")

    passive = df[df['Type'] == 'Passive'].sort_values('Potential Revenue (Year 3)', ascending=False)

    print(f"\nTotal Passive Income Opportunities: {len(passive)}")
    print(f"Year 1 Total: ${passive['Potential Revenue (Year 1)'].sum():,.0f}")
    print(f"Year 2 Total: ${passive['Potential Revenue (Year 2)'].sum():,.0f}")
    print(f"Year 3 Total: ${passive['Potential Revenue (Year 3)'].sum():,.0f}")

    # Passive by status
    print(f"\nPassive Income by Status:")
    passive_status = passive.groupby('Status').agg({
        'Potential Revenue (Year 3)': ['sum', 'count']
    })
    print(passive_status.to_string())

    # Ready passive opportunities
    ready_passive = passive[passive['Status'].isin(['Ready', 'Active'])].head(20)[
        ['Revenue Stream', 'Status', 'Priority', 'Potential Revenue (Year 3)']
    ]

    print(f"\nTop Ready/Active Passive Income Opportunities:")
    print(ready_passive.to_string(index=False))

    return passive

def generate_improvement_recommendations(df):
    """Generate actionable improvement recommendations"""
    print_section_header("💡 IMPROVEMENT RECOMMENDATIONS")

    recommendations = []

    # 1. Focus on Ready High-Priority
    ready_high = df[(df['Status'] == 'Ready') & (df['Priority'] == 'High')]
    if len(ready_high) > 0:
        total_potential = ready_high['Potential Revenue (Year 3)'].sum()
        recommendations.append({
            'Category': 'Immediate Focus',
            'Action': f'Prioritize {len(ready_high)} Ready + High Priority opportunities',
            'Potential': f'${total_potential:,.0f} Year 3 revenue',
            'Priority': 'CRITICAL'
        })

    # 2. Develop In-Development High-Priority
    dev_high = df[(df['Status'] == 'In Development') & (df['Priority'] == 'High')]
    if len(dev_high) > 0:
        total_potential = dev_high['Potential Revenue (Year 3)'].sum()
        recommendations.append({
            'Category': 'Development Focus',
            'Action': f'Complete {len(dev_high)} In-Development High Priority projects',
            'Potential': f'${total_potential:,.0f} Year 3 revenue',
            'Priority': 'HIGH'
        })

    # 3. Explore Not Found Medium/High Priority
    missing_priority = df[(df['Status'] == 'Not Found') & (df['Priority'].isin(['High', 'Medium']))]
    if len(missing_priority) > 0:
        total_potential = missing_priority['Potential Revenue (Year 3)'].sum()
        recommendations.append({
            'Category': 'Exploration',
            'Action': f'Explore {len(missing_priority)} Not Found Medium/High Priority opportunities',
            'Potential': f'${total_potential:,.0f} Year 3 revenue',
            'Priority': 'MEDIUM'
        })

    # 4. Package Available opportunities
    available_high = df[(df['Status'] == 'Available') & (df['Priority'].isin(['High', 'Medium']))]
    if len(available_high) > 0:
        total_potential = available_high['Potential Revenue (Year 3)'].sum()
        recommendations.append({
            'Category': 'Packaging',
            'Action': f'Package {len(available_high)} Available opportunities for monetization',
            'Potential': f'${total_potential:,.0f} Year 3 revenue',
            'Priority': 'HIGH'
        })

    # 5. Revenue concentration risk
    top_5_pct = df.nlargest(5, 'Potential Revenue (Year 3)')['Revenue_Contribution_Pct'].sum()
    if top_5_pct > 70:
        recommendations.append({
            'Category': 'Risk Mitigation',
            'Action': 'Diversify revenue streams - Top 5 opportunities represent >70% of revenue',
            'Potential': 'Reduce concentration risk',
            'Priority': 'MEDIUM'
        })

    # 6. Quick wins
    quick_wins = df.nlargest(5, 'Quick_Win_Score')
    if len(quick_wins) > 0:
        total_y1 = quick_wins['Potential Revenue (Year 1)'].sum()
        recommendations.append({
            'Category': 'Quick Wins',
            'Action': f'Implement top 5 quick win opportunities',
            'Potential': f'${total_y1:,.0f} Year 1 revenue',
            'Priority': 'HIGH'
        })

    print("\n" + pd.DataFrame(recommendations).to_string(index=False))

    return recommendations

def generate_prioritized_action_plan(df):
    """Generate prioritized action plan"""
    print_section_header("📋 PRIORITIZED ACTION PLAN")

    # Phase 1: Quick Wins (0-3 months)
    phase1 = df[df['Status'].isin(['Ready', 'Active'])].nlargest(10, 'Quick_Win_Score')[
        ['Revenue Stream', 'Status', 'Potential Revenue (Year 1)', 'Quick_Win_Score']
    ]

    print("\n🚀 PHASE 1: QUICK WINS (0-3 months)")
    print(f"Focus: Immediate revenue from ready opportunities")
    print(f"Target: ${phase1['Potential Revenue (Year 1)'].sum():,.0f} Year 1 revenue")
    print(phase1.to_string(index=False))

    # Phase 2: High ROI Development (3-6 months)
    phase2 = df[df['Status'].isin(['In Development', 'Available'])].nlargest(10, 'ROI_Score')[
        ['Revenue Stream', 'Status', 'Potential Revenue (Year 3)', 'ROI_Score']
    ]

    print("\n⚡ PHASE 2: HIGH ROI DEVELOPMENT (3-6 months)")
    print(f"Focus: Complete high-value in-development projects")
    print(f"Target: ${phase2['Potential Revenue (Year 3)'].sum():,.0f} Year 3 revenue")
    print(phase2.to_string(index=False))

    # Phase 3: Exploration & Diversification (6-12 months)
    phase3 = df[df['Status'] == 'Not Found'].nlargest(10, 'Potential Revenue (Year 3)')[
        ['Revenue Stream', 'Priority', 'Potential Revenue (Year 3)']
    ]

    print("\n🔍 PHASE 3: EXPLORATION & DIVERSIFICATION (6-12 months)")
    print(f"Focus: Explore untapped opportunities")
    print(f"Target: ${phase3['Potential Revenue (Year 3)'].sum():,.0f} Year 3 revenue potential")
    print(phase3.to_string(index=False))

    return phase1, phase2, phase3

def run_analysis():
    """Run the complete analysis"""
    print("="*100)
    print("  DEEP DIVE INCOME OPPORTUNITIES ANALYSIS")
    print("  Advanced Metrics, ROI, Risk Assessment & Improvement Recommendations")
    print("="*100)

    # Load and calculate metrics
    df = load_data()
    df = calculate_metrics(df)

    # Overall summary
    total_y1 = df['Potential Revenue (Year 1)'].sum()
    total_y2 = df['Potential Revenue (Year 2)'].sum()
    total_y3 = df['Potential Revenue (Year 3)'].sum()

    print_section_header("📊 EXECUTIVE SUMMARY")
    print(f"\nTotal Revenue Streams: {len(df)}")
    print(f"Total Potential Revenue:")
    print(f"  Year 1: ${total_y1:,.0f}")
    print(f"  Year 2: ${total_y2:,.0f}")
    print(f"  Year 3: ${total_y3:,.0f}")

    ready_active_y3 = df[df['Status'].isin(['Ready', 'Active'])]['Potential Revenue (Year 3)'].sum()
    print(f"\nReady/Active Opportunities: ${ready_active_y3:,.0f} Year 3 ({ready_active_y3/total_y3*100:.1f}%)")

    # Run all analyses
    quick_wins = analyze_quick_wins(df)
    roi_leaders = analyze_roi_leaders(df)
    growth_leaders = analyze_growth_leaders(df)
    revenue_concentration = analyze_revenue_concentration(df)
    low_risk, high_risk = analyze_risk_profile(df)
    passive_breakdown = analyze_passive_income_breakdown(df)
    implementation_readiness = analyze_by_implementation_readiness(df)
    recommendations = generate_improvement_recommendations(df)
    phase1, phase2, phase3 = generate_prioritized_action_plan(df)

    print_section_header("✅ ANALYSIS COMPLETE")
    print("\nNext Steps:")
    print("1. Review Quick Wins - Start implementing immediately")
    print("2. Focus on High ROI opportunities - Best return on effort")
    print("3. Follow Prioritized Action Plan - Phased approach")
    print("4. Monitor Growth Leaders - Fastest scaling opportunities")
    print("5. Diversify revenue - Reduce concentration risk")
    print()

    return df

if __name__ == "__main__":
    # Capture output for both display and file
    import io
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()

    try:
        run_analysis()
    finally:
        output = buffer.getvalue()
        sys.stdout = old_stdout
        print(output)

        # Save to file
        output_file = Path(__file__).parent / "deepdive_analysis_output.txt"
        with open(output_file, 'w') as f:
            f.write(output)

        print(f"\n📄 Detailed analysis saved to: {output_file}")

