#!/usr/bin/env python3
"""Email revenue summary - daily/weekly digest"""
import smtplib, sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

# Import dashboard
sys.path.insert(0, str(Path(__file__).parent))
from dashboard import aggregate_revenue

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = "your-email@gmail.com"  # Update this
TO_EMAIL = "your-email@gmail.com"    # Update this
PASSWORD = "your-app-password"        # Use app-specific password

def generate_summary(days=7):
    """Generate HTML summary"""
    totals, daily = aggregate_revenue(days)
    grand_total = sum(totals.values())
    avg_daily = grand_total / days if days > 0 else 0

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; }}
            h1 {{ color: #2c3e50; }}
            .total {{ font-size: 2em; color: #27ae60; font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f8f9fa; }}
            .footer {{ color: #7f8c8d; font-size: 0.9em; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <h1>💰 Revenue Summary ({days} days)</h1>
        <p>Period: {datetime.now().strftime('%Y-%m-%d')}</p>

        <div class="total">${grand_total:,.2f}</div>

        <h2>By Source</h2>
        <table>
            <tr><th>Source</th><th>Amount</th><th>%</th></tr>
    """

    for source in sorted(totals.keys(), key=lambda s: totals[s], reverse=True):
        amount = totals[source]
        if amount > 0:
            pct = (amount / grand_total * 100) if grand_total > 0 else 0
            html += f"<tr><td>{source.title()}</td><td>${amount:,.2f}</td><td>{pct:.1f}%</td></tr>\n"

    html += f"""
        </table>

        <h2>Projections</h2>
        <ul>
            <li>Daily Average: ${avg_daily:,.2f}</li>
            <li>Monthly (30d): ${avg_daily * 30:,.2f}</li>
            <li>Yearly (365d): ${avg_daily * 365:,.2f}</li>
        </ul>

        <div class="footer">
            <p>AvaTarArTs Revenue Dashboard</p>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
    </body>
    </html>
    """

    return html

def send_email(subject, html_content):
    """Send email via SMTP"""
    if PASSWORD == "your-app-password":
        print("⚠️ Email not configured. Update credentials in email_summary.py")
        return False

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL

    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(FROM_EMAIL, PASSWORD)
            server.send_message(msg)

        print(f"✅ Email sent to {TO_EMAIL}")
        return True
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False

if __name__ == '__main__':
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    period = "Weekly" if days == 7 else f"{days}-Day"

    html = generate_summary(days)

    # Save to file
    output = Path(__file__).parent / f'summary_{datetime.now().strftime("%Y%m%d")}.html'
    output.write_text(html)
    print(f"✅ Summary saved: {output}")

    # Send email if configured
    if '--send' in sys.argv:
        send_email(f"💰 {period} Revenue Summary", html)
