#!/usr/bin/env python3
"""Quick revenue logger - add entries from command line"""
import csv, sys
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent / 'data'
DATA_DIR.mkdir(exist_ok=True)

SOURCES = ['redbubble', 'audiojungle', 'distrokid', 'ai-voice-agents', 'cleanconnect', 'etsy', 'youtube', 'patreon', 'custom']

def log_revenue(source, amount, description=''):
    """Log a revenue entry"""
    if source not in SOURCES:
        print(f"❌ Unknown source: {source}")
        print(f"Available: {', '.join(SOURCES)}")
        return False

    csv_path = DATA_DIR / f'{source}.csv'
    is_new = not csv_path.exists()

    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(['date', 'amount', 'description'])

        writer.writerow([
            datetime.now().isoformat(),
            f"{amount:.2f}",
            description
        ])

    print(f"✅ Logged ${amount:.2f} to {source}")
    print(f"   {description}")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: log_revenue.py <source> <amount> [description]")
        print(f"Sources: {', '.join(SOURCES)}")
        print("\nExample: log_revenue.py redbubble 42.50 'Raccoon t-shirt sale'")
        sys.exit(1)

    source = sys.argv[1]
    amount = float(sys.argv[2])
    description = ' '.join(sys.argv[3:]) if len(sys.argv) > 3 else ''

    log_revenue(source, amount, description)
