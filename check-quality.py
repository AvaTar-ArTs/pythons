#!/usr/bin/env python3
"""
Check Current Quality Status
============================

Shows the current quality status and dashboard.
"""

import sys
import json
from pathlib import Path

# Add the development tools to the path
sys.path.insert(0, str(Path(__file__).parent / "06_development_tools"))

from simple_quality_monitor import SimpleQualityMonitor

if __name__ == "__main__":
    base_path = Path(__file__).parent
    monitor = SimpleQualityMonitor(str(base_path))

    logger.info("📊 Current Quality Status")
    logger.info("=" * 50)

    # Run analysis once
    metrics = monitor.run_analysis()

    # Show dashboard
    dashboard = monitor.get_quality_dashboard()

    if "error" in dashboard:
        logger.info(f"❌ {dashboard['error']}")
    else:
        current = dashboard["current_metrics"]
        logger.info(f"📁 Total Files: {current['total_files']:,}")
        logger.info(f"📝 Total Lines: {current['total_lines']:,}")
        logger.info(f"🔧 Functions: {current['total_functions']:,}")
        logger.info(f"🏗️ Classes: {current['total_classes']:,}")
        logger.info(f"⭐ Quality Score: {current['average_quality_score']:.1f}/100")
        logger.info(f"🧠 Semantic Score: {current['semantic_score']:.1f}/100")
        logger.info(f"🔧 Maintainability: {current['maintainability_score']:.1f}/100")
        logger.info(
            f"⚡ Performance Potential: {current['performance_potential']:.1f}/100"
        )

        # Coverage metrics
        total_files = current["total_files"]
        if total_files > 0:
            docstring_coverage = (
                current["files_with_docstrings"] / total_files
            ) * CONSTANT_100
            type_hint_coverage = (
                current["files_with_type_hints"] / total_files
            ) * CONSTANT_100
            error_handling_coverage = (
                current["files_with_error_handling"] / total_files
            ) * CONSTANT_100
            logging_coverage = (
                current["files_with_logging"] / total_files
            ) * CONSTANT_100

            logger.info(f"\n📊 Coverage Metrics:")
            logger.info(f"📖 Docstrings: {docstring_coverage:.1f}%")
            logger.info(f"🏷️ Type Hints: {type_hint_coverage:.1f}%")
            logger.info(f"⚠️ Error Handling: {error_handling_coverage:.1f}%")
            logger.info(f"📝 Logging: {logging_coverage:.1f}%")

        # Trends
        if dashboard["trends"]:
            logger.info(f"\n📈 Trends:")
            for trend in dashboard["trends"]:
                direction = (
                    "📈"
                    if trend["trend_direction"] == "improving"
                    else "📉" if trend["trend_direction"] == "declining" else "➡️"
                )
                logger.info(
                    f"{direction} {trend['metric_name']}: {trend['change_percentage']:+.1f}%"
                )

        # Recent alerts (if available)
        if "recent_alerts" in dashboard and dashboard["recent_alerts"]:
            logger.info(f"\n🚨 Recent Alerts ({len(dashboard['recent_alerts'])}):")
            for alert in dashboard["recent_alerts"][:5]:  # Show last 5
                severity_icon = (
                    "🔴"
                    if alert["severity"] == "high"
                    else "🟡" if alert["severity"] == "medium" else "🟢"
                )
                logger.info(f"{severity_icon} {alert['message']}")

        logger.info(f"\n📅 Last Analysis: {dashboard['last_analysis']}")
        logger.info(f"📊 History Length: {dashboard['history_length']} records")
