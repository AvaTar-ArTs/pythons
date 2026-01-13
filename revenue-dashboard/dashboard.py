#!/usr/bin/env python3
"""Revenue Dashboard - Track all income streams in one place"""
import csv, json, sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

DASHBOARD_DIR = Path(__file__).parent
DATA_DIR = DASHBOARD_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

# Revenue sources config
SOURCES = {
    'redbubble': DATA_DIR / 'redbubble.csv',
    'audiojungle': DATA_DIR / 'audiojungle.csv',
    'distrokid': DATA_DIR / 'distrokid.csv',
    'ai-voice-agents': DATA_DIR / 'ai-voice-agents.csv',
    'cleanconnect': DATA_DIR / 'cleanconnect.csv',
    'etsy': DATA_DIR / 'etsy.csv',
    'youtube': DATA_DIR / 'youtube.csv',
    'patreon': DATA_DIR / 'patreon.csv',
    'custom': DATA_DIR / 'custom.csv'
}

def read_revenue(source_path, days=30):
    """Read revenue data from CSV"""
    if not source_path.exists():
        return []

    cutoff = datetime.now() - timedelta(days=days)
    data = []

    with open(source_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.fromisoformat(row['date'])
                if date >= cutoff:
                    data.append({
                        'date': date,
                        'amount': float(row['amount']),
                        'description': row.get('description', '')
                    })
            except (ValueError, KeyError):
                continue

    return data

def aggregate_revenue(days=30):
    """Aggregate revenue across all sources"""
    totals = defaultdict(float)
    daily = defaultdict(lambda: defaultdict(float))

    for source, path in SOURCES.items():
        data = read_revenue(path, days)
        source_total = sum(d['amount'] for d in data)
        totals[source] = source_total

        for entry in data:
            day = entry['date'].date().isoformat()
            daily[day][source] += entry['amount']

    return totals, daily

def print_dashboard(days=30):
    """Print formatted dashboard"""
    print("💰 Steven's Revenue Dashboard")
    print("=" * 60)
    print(f"Period: Last {days} days")
    print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    totals, daily = aggregate_revenue(days)

    # Total revenue
    grand_total = sum(totals.values())
    print(f"📊 TOTAL REVENUE: ${grand_total:,.2f}\n")

    # By source
    print("By Source:")
    print("-" * 60)
    for source in sorted(totals.keys(), key=lambda s: totals[s], reverse=True):
        amount = totals[source]
        if amount > 0:
            pct = (amount / grand_total * 100) if grand_total > 0 else 0
            bar = '█' * int(pct / 2)
            print(f"  {source:15s} ${amount:9,.2f}  ({pct:5.1f}%)  {bar}")
    print()

    # Recent days (last 7)
    print("Recent Activity (Last 7 Days):")
    print("-" * 60)
    recent_days = sorted(daily.keys(), reverse=True)[:7]
    for day in recent_days:
        day_total = sum(daily[day].values())
        print(f"  {day}  ${day_total:9,.2f}")
        for source, amount in sorted(daily[day].items(), key=lambda x: x[1], reverse=True):
            if amount > 0:
                print(f"    └─ {source}: ${amount:,.2f}")
    print()

    # Projections
    avg_daily = grand_total / days if days > 0 else 0
    monthly_proj = avg_daily * 30
    yearly_proj = avg_daily * 365
    print("📈 Projections:")
    print("-" * 60)
    print(f"  Daily Average:   ${avg_daily:,.2f}")
    print(f"  Monthly (30d):   ${monthly_proj:,.2f}")
    print(f"  Yearly (365d):   ${yearly_proj:,.2f}")
    print()

    print("=" * 60)
    print(f"💡 Data files: {DATA_DIR}")
    print(f"   Format: date,amount,description")

def export_json(output_path=None):
    """Export dashboard data as JSON"""
    if output_path is None:
        output_path = DASHBOARD_DIR / f'dashboard_{datetime.now().strftime("%Y%m%d")}.json'

    totals, daily = aggregate_revenue()
    data = {
        'updated': datetime.now().isoformat(),
        'totals': dict(totals),
        'daily': {day: dict(sources) for day, sources in daily.items()},
        'grand_total': sum(totals.values())
    }

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✅ Exported to {output_path}")

if __name__ == '__main__':
    if '--json' in sys.argv:
        export_json()
    else:
        days = int(sys.argv[1]) if len(sys.argv) > 1 else 30
        print_dashboard(days)
