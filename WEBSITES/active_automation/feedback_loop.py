#!/usr/bin/env python3
"""Performance Feedback Loop - Track, analyze, optimize"""
import json, csv, sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

PERF_DIR = Path(__file__).parent
DATA_DIR = PERF_DIR / 'data'
REPORTS_DIR = PERF_DIR / 'reports'
DATA_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Performance tracking
def track_content_performance(content_id, content_type, platform, metrics):
    """Track performance of a piece of content"""
    csv_path = DATA_DIR / 'performance_log.csv'
    is_new = not csv_path.exists()

    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow([
                'timestamp', 'content_id', 'content_type', 'platform',
                'views', 'likes', 'shares', 'comments', 'ctr', 'conversions',
                'revenue'
            ])

        writer.writerow([
            datetime.now().isoformat(),
            content_id,
            content_type,
            platform,
            metrics.get('views', 0),
            metrics.get('likes', 0),
            metrics.get('shares', 0),
            metrics.get('comments', 0),
            metrics.get('ctr', 0.0),
            metrics.get('conversions', 0),
            metrics.get('revenue', 0.0)
        ])

def analyze_performance(days=30):
    """Analyze performance and identify patterns"""
    csv_path = DATA_DIR / 'performance_log.csv'

    if not csv_path.exists():
        return {
            'top_content_types': [],
            'top_platforms': [],
            'best_keywords': [],
            'recommendations': ['No data yet - start tracking performance!']
        }

    # Aggregate by content type
    by_type = defaultdict(lambda: {'views': 0, 'engagement': 0, 'revenue': 0, 'count': 0})
    by_platform = defaultdict(lambda: {'views': 0, 'engagement': 0, 'revenue': 0, 'count': 0})

    cutoff = datetime.now() - timedelta(days=days)

    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                timestamp = datetime.fromisoformat(row['timestamp'])
                if timestamp < cutoff:
                    continue

                content_type = row['content_type']
                platform = row['platform']
                views = int(row.get('views', 0))
                engagement = int(row.get('likes', 0)) + int(row.get('shares', 0)) + int(row.get('comments', 0))
                revenue = float(row.get('revenue', 0))

                by_type[content_type]['views'] += views
                by_type[content_type]['engagement'] += engagement
                by_type[content_type]['revenue'] += revenue
                by_type[content_type]['count'] += 1

                by_platform[platform]['views'] += views
                by_platform[platform]['engagement'] += engagement
                by_platform[platform]['revenue'] += revenue
                by_platform[platform]['count'] += 1

            except (ValueError, KeyError):
                continue

    # Calculate scores
    top_types = []
    for ctype, stats in by_type.items():
        if stats['count'] > 0:
            score = (stats['views'] / 100) + (stats['engagement'] / 10) + stats['revenue']
            top_types.append({
                'type': ctype,
                'score': round(score, 2),
                'avg_views': stats['views'] // stats['count'],
                'avg_engagement': stats['engagement'] // stats['count'],
                'total_revenue': round(stats['revenue'], 2),
                'count': stats['count']
            })

    top_types.sort(key=lambda x: x['score'], reverse=True)

    top_platforms = []
    for platform, stats in by_platform.items():
        if stats['count'] > 0:
            score = (stats['views'] / 100) + (stats['engagement'] / 10) + stats['revenue']
            top_platforms.append({
                'platform': platform,
                'score': round(score, 2),
                'avg_views': stats['views'] // stats['count'],
                'avg_engagement': stats['engagement'] // stats['count'],
                'total_revenue': round(stats['revenue'], 2),
                'count': stats['count']
            })

    top_platforms.sort(key=lambda x: x['score'], reverse=True)

    # Generate recommendations
    recommendations = []

    if top_types:
        best_type = top_types[0]
        recommendations.append(f"✅ Focus on {best_type['type']} (score: {best_type['score']}) - it's your top performer")

    if top_platforms:
        best_platform = top_platforms[0]
        recommendations.append(f"✅ Prioritize {best_platform['platform']} - highest engagement and revenue")

    if len(top_types) > 1:
        worst_type = top_types[-1]
        if worst_type['score'] < best_type['score'] * 0.3:
            recommendations.append(f"⚠️ Consider reducing {worst_type['type']} - underperforming")

    # Revenue optimization
    total_revenue = sum(p['total_revenue'] for p in top_platforms)
    if total_revenue > 0:
        recommendations.append(f"💰 Total revenue tracked: ${total_revenue:.2f}")
        top_revenue_platform = max(top_platforms, key=lambda x: x['total_revenue'])
        recommendations.append(f"💎 Best revenue source: {top_revenue_platform['platform']} (${top_revenue_platform['total_revenue']:.2f})")

    return {
        'period_days': days,
        'top_content_types': top_types[:5],
        'top_platforms': top_platforms[:5],
        'recommendations': recommendations
    }

def generate_report(days=30, output_path=None):
    """Generate performance report"""
    if output_path is None:
        output_path = REPORTS_DIR / f'performance_report_{datetime.now().strftime("%Y%m%d")}.md'

    analysis = analyze_performance(days)

    report = [
        f"# Performance Report ({days} days)",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "---",
        "",
        "## 🏆 Top Content Types",
        ""
    ]

    if analysis['top_content_types']:
        for item in analysis['top_content_types']:
            report.append(f"### {item['type'].title()}")
            report.append(f"- **Score:** {item['score']}")
            report.append(f"- **Avg Views:** {item['avg_views']:,}")
            report.append(f"- **Avg Engagement:** {item['avg_engagement']:,}")
            report.append(f"- **Total Revenue:** ${item['total_revenue']:.2f}")
            report.append(f"- **Posts:** {item['count']}")
            report.append("")
    else:
        report.append("*No data yet*\n")

    report.extend([
        "## 📱 Top Platforms",
        ""
    ])

    if analysis['top_platforms']:
        for item in analysis['top_platforms']:
            report.append(f"### {item['platform'].title()}")
            report.append(f"- **Score:** {item['score']}")
            report.append(f"- **Avg Views:** {item['avg_views']:,}")
            report.append(f"- **Avg Engagement:** {item['avg_engagement']:,}")
            report.append(f"- **Total Revenue:** ${item['total_revenue']:.2f}")
            report.append(f"- **Posts:** {item['count']}")
            report.append("")
    else:
        report.append("*No data yet*\n")

    report.extend([
        "## 💡 Recommendations",
        ""
    ])

    for rec in analysis['recommendations']:
        report.append(f"- {rec}")

    report.extend([
        "",
        "---",
        "",
        "## 🔄 Next Actions",
        "",
        "1. **Create more** of what works (top content types)",
        "2. **Optimize** underperforming content",
        "3. **Focus** on highest-revenue platforms",
        "4. **Test** variations of successful content",
        "5. **Track** everything for continuous improvement",
        "",
        "---",
        f"*Data: {DATA_DIR / 'performance_log.csv'}*"
    ])

    output_path.write_text('\n'.join(report))
    return output_path

def print_analysis(days=30):
    """Print performance analysis"""
    analysis = analyze_performance(days)

    print(f"📊 Performance Analysis ({days} days)")
    print("=" * 60)

    print("\n🏆 Top Content Types:")
    for item in analysis['top_content_types'][:3]:
        print(f"  {item['type']:20s}  Score: {item['score']:6.1f}  Views: {item['avg_views']:6,}  Revenue: ${item['total_revenue']:6.2f}")

    print("\n📱 Top Platforms:")
    for item in analysis['top_platforms'][:3]:
        print(f"  {item['platform']:20s}  Score: {item['score']:6.1f}  Views: {item['avg_views']:6,}  Revenue: ${item['total_revenue']:6.2f}")

    print("\n💡 Recommendations:")
    for rec in analysis['recommendations']:
        print(f"  • {rec}")

    print("\n" + "=" * 60)

if __name__ == '__main__':
    if '--track' in sys.argv:
        # Track performance
        if len(sys.argv) < 5:
            print("Usage: feedback_loop.py --track <content_id> <type> <platform> <views> [likes] [shares] [revenue]")
            print("\nExample: feedback_loop.py --track recipe_001 recipe instagram 1250 85 12 0")
            sys.exit(1)

        content_id = sys.argv[2]
        content_type = sys.argv[3]
        platform = sys.argv[4]

        metrics = {
            'views': int(sys.argv[5]) if len(sys.argv) > 5 else 0,
            'likes': int(sys.argv[6]) if len(sys.argv) > 6 else 0,
            'shares': int(sys.argv[7]) if len(sys.argv) > 7 else 0,
            'revenue': float(sys.argv[8]) if len(sys.argv) > 8 else 0.0
        }

        track_content_performance(content_id, content_type, platform, metrics)
        print(f"✅ Tracked: {content_id} on {platform}")

    elif '--report' in sys.argv:
        # Generate report
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        report_path = generate_report(days)
        print(f"✅ Report generated: {report_path}")

    else:
        # Print analysis
        days = int(sys.argv[1]) if len(sys.argv) > 1 else 30
        print_analysis(days)
