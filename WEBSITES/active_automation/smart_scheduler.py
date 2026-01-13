#!/usr/bin/env python3
"""Smart Scheduler - AI-driven optimal posting times"""
import json, sys, csv
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

SCHEDULER_DIR = Path(__file__).parent
DATA_DIR = SCHEDULER_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

# Optimal posting times by platform (default - will be ML-optimized)
DEFAULT_TIMES = {
    'instagram': [
        {'time': '09:00', 'days': ['Mon', 'Wed', 'Fri'], 'score': 8},
        {'time': '12:00', 'days': ['Tue', 'Thu'], 'score': 7},
        {'time': '18:00', 'days': ['Mon', 'Wed', 'Fri'], 'score': 9}
    ],
    'tiktok': [
        {'time': '06:00', 'days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], 'score': 7},
        {'time': '18:00', 'days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], 'score': 9},
        {'time': '21:00', 'days': ['Fri', 'Sat'], 'score': 10}
    ],
    'youtube': [
        {'time': '14:00', 'days': ['Wed', 'Sat'], 'score': 9},
        {'time': '17:00', 'days': ['Sun'], 'score': 8}
    ],
    'twitter': [
        {'time': '09:00', 'days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], 'score': 7},
        {'time': '12:00', 'days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], 'score': 8},
        {'time': '17:00', 'days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], 'score': 7}
    ],
    'pinterest': [
        {'time': '20:00', 'days': ['Sat', 'Sun'], 'score': 9},
        {'time': '21:00', 'days': ['Wed', 'Fri'], 'score': 8}
    ]
}

def analyze_past_performance(platform, days=90):
    """Analyze past performance to find optimal times"""
    csv_path = DATA_DIR / f'{platform}_analytics.csv'

    if not csv_path.exists():
        return DEFAULT_TIMES.get(platform, [])

    hourly_performance = defaultdict(lambda: {'views': 0, 'engagement': 0, 'count': 0})

    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                post_time = datetime.fromisoformat(row['posted_at'])
                hour = post_time.hour
                views = int(row.get('views', 0))
                engagement = float(row.get('engagement_rate', 0))

                hourly_performance[hour]['views'] += views
                hourly_performance[hour]['engagement'] += engagement
                hourly_performance[hour]['count'] += 1
            except (ValueError, KeyError):
                continue

    # Calculate average performance by hour
    optimal_hours = []
    for hour, stats in hourly_performance.items():
        if stats['count'] > 0:
            avg_views = stats['views'] / stats['count']
            avg_engagement = stats['engagement'] / stats['count']
            score = (avg_views / 1000) + (avg_engagement * 10)  # Weighted score

            if score > 5:  # Only include high-performing hours
                optimal_hours.append({
                    'time': f"{hour:02d}:00",
                    'score': min(10, int(score)),
                    'avg_views': int(avg_views),
                    'avg_engagement': round(avg_engagement, 2)
                })

    return sorted(optimal_hours, key=lambda x: x['score'], reverse=True)[:5]

def generate_schedule(platforms, days_ahead=7):
    """Generate optimal posting schedule"""
    schedule = {}

    for platform in platforms:
        optimal_times = analyze_past_performance(platform)
        if not optimal_times:
            optimal_times = DEFAULT_TIMES.get(platform, [])

        platform_schedule = []
        start_date = datetime.now()

        for day_offset in range(days_ahead):
            date = start_date + timedelta(days=day_offset)
            day_name = date.strftime('%a')

            for time_slot in optimal_times:
                if 'days' not in time_slot or day_name in time_slot['days']:
                    post_datetime = datetime.combine(
                        date.date(),
                        datetime.strptime(time_slot['time'], '%H:%M').time()
                    )

                    platform_schedule.append({
                        'datetime': post_datetime.isoformat(),
                        'day': day_name,
                        'time': time_slot['time'],
                        'score': time_slot['score'],
                        'reason': f"High engagement window ({time_slot['score']}/10)"
                    })

        schedule[platform] = sorted(platform_schedule, key=lambda x: x['datetime'])

    return schedule

def export_to_buffer(schedule, output_path=None):
    """Export schedule in Buffer-compatible CSV format"""
    if output_path is None:
        output_path = SCHEDULER_DIR / f'buffer_schedule_{datetime.now().strftime("%Y%m%d")}.csv'

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['platform', 'datetime', 'content', 'media', 'link'])

        for platform, posts in schedule.items():
            for post in posts:
                writer.writerow([
                    platform,
                    post['datetime'],
                    f"[CONTENT PLACEHOLDER - Score: {post['score']}/10]",
                    '',
                    'https://avatararts.org'
                ])

    return output_path

def print_schedule(schedule):
    """Print formatted schedule"""
    print("📅 Smart Posting Schedule")
    print("=" * 60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    for platform, posts in schedule.items():
        print(f"\n🔷 {platform.upper()}")
        print("-" * 60)

        for post in posts[:10]:  # Show next 10 posts
            dt = datetime.fromisoformat(post['datetime'])
            print(f"  {dt.strftime('%a %b %d, %H:%M')}  |  Score: {post['score']}/10")

        if len(posts) > 10:
            print(f"  ... and {len(posts) - 10} more")

    print("\n" + "=" * 60)
    print("💡 Tip: Higher scores = better engagement expected")

def log_post_performance(platform, posted_at, views, engagement_rate):
    """Log post performance for ML optimization"""
    csv_path = DATA_DIR / f'{platform}_analytics.csv'
    is_new = not csv_path.exists()

    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(['posted_at', 'views', 'engagement_rate', 'logged_at'])

        writer.writerow([
            posted_at,
            views,
            engagement_rate,
            datetime.now().isoformat()
        ])

if __name__ == '__main__':
    if '--log' in sys.argv:
        # Log performance data
        if len(sys.argv) < 5:
            print("Usage: smart_scheduler.py --log <platform> <posted_at> <views> <engagement_rate>")
            sys.exit(1)

        platform = sys.argv[2]
        posted_at = sys.argv[3]
        views = int(sys.argv[4])
        engagement = float(sys.argv[5])

        log_post_performance(platform, posted_at, views, engagement)
        print(f"✅ Logged performance for {platform}")

    else:
        # Generate schedule
        platforms = sys.argv[1:] if len(sys.argv) > 1 else ['instagram', 'tiktok', 'youtube', 'twitter']
        days = 7

        print(f"🤖 Analyzing optimal posting times for: {', '.join(platforms)}")
        print("=" * 60)

        schedule = generate_schedule(platforms, days)
        print_schedule(schedule)

        # Export to CSV
        csv_path = export_to_buffer(schedule)
        print(f"\n📄 Buffer-compatible CSV: {csv_path}")

        # Save JSON
        json_path = SCHEDULER_DIR / f'schedule_{datetime.now().strftime("%Y%m%d")}.json'
        json_path.write_text(json.dumps(schedule, indent=2))
        print(f"📋 JSON schedule: {json_path}")
