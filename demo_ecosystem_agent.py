import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Quick Demo of EcoSystem Agent Manager
This script demonstrates the agent's functionality on a smaller subset of the ecosystem
"""

import os
from ecosystem_agent_manager import EcoSystemAgentManager

def demo_ecosystem_agent():
    print("🚀 Starting Quick Demo of EcoSystem Agent Manager...")
    print(" ")
    
    # Initialize the agent manager
    manager = EcoSystemAgentManager(db_path="./demo_ecosystem_agent.db")
    
    # Scan a smaller directory for demonstration purposes
    print("🔍 Scanning AVATARARTS directory (smaller subset)...")
    assets = manager.scan_system("/Users/steven/AVATARARTS")
    
    print(f"📊 Found {len(assets)} assets in AVATARARTS directory")
    
    # Register assets
    print("📦 Registering assets in database...")
    manager.register_assets(assets)
    
    # Detect duplicates
    print("🔍 Detecting duplicates...")
    duplicates = manager.detect_duplicates()
    print(f"📋 Found {len(duplicates)} duplicate groups")
    
    # Generate report
    print("📝 Generating report...")
    report = manager.generate_comprehensive_report()
    
    # Save report
    with open("demo_ecosystem_report.md", "w") as f:
        f.write(report)
    print("💾 Report saved to demo_ecosystem_report.md")
    
    # Show high-value assets
    print(f"\n💎 High-Value Assets (8.0+) in AVATARARTS:")
    high_value_assets = manager.get_high_value_assets(min_value=8.0)
    for asset in high_value_assets[:5]:  # Show top 5
        print(f"   • {asset.name} ({asset.business_value_score}) - {asset.business_vertical}")
    
    # Show revenue forecast
    print(f"\n💰 Revenue Forecast for AVATARARTS:")
    revenue_forecast = manager.get_revenue_forecast()
    for vertical, forecast in list(revenue_forecast.items())[:3]:
        print(f"   • {vertical}: ${forecast:,.2f}/month (estimated)")
    
    # Export to CSV
    print("📊 Exporting assets to CSV...")
    manager.export_to_csv("demo_ecosystem_assets.csv")
    print("💾 Assets exported to demo_ecosystem_assets.csv")
    
    # Close the manager
    manager.close()
    print(" ")
    print("✅ Quick Demo completed successfully!")
    print("📄 Check demo_ecosystem_report.md for detailed analysis")
    print("📊 Check demo_ecosystem_assets.csv for structured data")
    print("💾 Check demo_ecosystem_agent.db for database records")

try:
        demo_ecosystem_agent()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)