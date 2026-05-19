#!/usr/bin/env python3
"""
Revenue Dashboard - Real-time Revenue Tracking and Optimization
Track and optimize revenue across all passive income systems

Features:
- Real-time revenue tracking
- Performance analytics
- Goal tracking
- Optimization recommendations
- Multi-system management
"""

import os
import sqlite3
import datetime
from typing import Dict, List, Any
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class RevenueGoal:
    """Represents a revenue goal"""

    id: str
    name: str
    target_amount: float
    current_amount: float
    deadline: str
    system: str
    status: str  # active, completed, failed


@dataclass
class RevenueMetric:
    """Represents a revenue metric"""

    id: str
    metric_name: str
    value: float
    date: str
    system: str
    platform: str


class RevenueDashboard:
    """Revenue tracking and optimization dashboard"""

    def __init__(self, db_path: str = "databases/revenue_dashboard.db"):
        self.db_path = db_path
        self._init_database()
        self.systems = {
            "ai_recipe_generator": "AI Recipe Generator",
            "ai_receptionist": "AI Receptionist",
            "music_licensing": "Music Licensing",
            "print_on_demand": "Print on Demand",
            "cleanconnect_leads": "CleanConnect Leads",
        }

    def _init_database(self):
        """Initialize revenue dashboard database"""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Revenue goals table
            cursor.execute('\''
                CREATE TABLE IF NOT EXISTS revenue_goals (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    target_amount REAL NOT NULL,
                    current_amount REAL DEFAULT 0.0,
                    deadline TEXT,
                    system TEXT,
                    status TEXT DEFAULT 'active',
                    created_at TEXT,
                    updated_at TEXT
                )
            """)

            # Revenue metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS revenue_metrics (
                    id TEXT PRIMARY KEY,
                    metric_name TEXT NOT NULL,
                    value REAL NOT NULL,
                    date TEXT,
                    system TEXT,
                    platform TEXT,
                    created_at TEXT
                )
            """)

            # System performance table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_performance (
                    id TEXT PRIMARY KEY,
                    system TEXT NOT NULL,
                    metric_name TEXT NOT NULL,
                    value REAL NOT NULL,
                    date TEXT,
                    created_at TEXT
                )
            """)

            conn.commit()
            conn.close()
            logger.info("Revenue dashboard database initialized")

        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    def add_revenue_goal(:
        self, name: str, target_amount: float, deadline: str, system: str
    ) -> str:
        """Add a new revenue goal"""
        goal_id = f"goal_{int(datetime.datetime.now().timestamp())}"

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO revenue_goals 
                (id, name, target_amount, current_amount, deadline, system, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    goal_id,
                    name,
                    target_amount,
                    0.0,
                    deadline,
                    system,
                    datetime.datetime.now().isoformat(),
                    datetime.datetime.now().isoformat(),
                ),
            )

            conn.commit()
            conn.close()

            logger.info(f"Revenue goal added: {name} - ${target_amount} by {deadline}")
            return goal_id

        except Exception as e:
            logger.error(f"Failed to add revenue goal: {e}")
            return None

    def update_revenue(:
        self, system: str, amount: float, platform: str = "direct"
    ) -> bool:
        """Update revenue for a system"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Add revenue metric
            metric_id = f"metric_{int(datetime.datetime.now().timestamp())}"
            cursor.execute(
                """
                INSERT INTO revenue_metrics 
                (id, metric_name, value, date, system, platform, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    metric_id,
                    "revenue",
                    amount,
                    datetime.datetime.now().date().isoformat(),
                    system,
                    platform,
                    datetime.datetime.now().isoformat(),
                ),
            )

            # Update active goals
            cursor.execute(
                """
                UPDATE revenue_goals 
                SET current_amount = current_amount + ?, updated_at = ?
                WHERE system = ? AND status = 'active'
            """,
                (amount, datetime.datetime.now().isoformat(), system),
            )

            conn.commit()
            conn.close()

            logger.info(f"Revenue updated: ${amount} for {system} via {platform}")
            return True

        except Exception as e:
            logger.error(f"Failed to update revenue: {e}")
            return False

    def get_revenue_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive revenue summary"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get total revenue by system
            cursor.execute(
                """
                SELECT system, SUM(value) as total_revenue
                FROM revenue_metrics 
                WHERE date >= date('now', '-{} days')
                GROUP BY system
            """.format(days)
            )

            system_revenue = dict(cursor.fetchall())

            # Get daily revenue trend
            cursor.execute(
                """
                SELECT date, SUM(value) as daily_revenue
                FROM revenue_metrics 
                WHERE date >= date('now', '-{} days')
                GROUP BY date
                ORDER BY date
            """.format(days)
            )

            daily_trend = dict(cursor.fetchall())

            # Get platform breakdown
            cursor.execute(
                """
                SELECT platform, SUM(value) as platform_revenue
                FROM revenue_metrics 
                WHERE date >= date('now', '-{} days')
                GROUP BY platform
            """.format(days)
            )

            platform_revenue = dict(cursor.fetchall())

            # Get active goals
            cursor.execute("""
                SELECT name, target_amount, current_amount, deadline, system
                FROM revenue_goals 
                WHERE status = 'active'
            """)

            active_goals = [
                {
                    "name": row[0],
                    "target": row[1],
                    "current": row[2],
                    "deadline": row[3],
                    "system": row[4],
                    "progress": (row[2] / row[1] * 100) if row[1] > 0 else 0,
                }
                for row in cursor.fetchall()
            ]

            conn.close()

            total_revenue = sum(system_revenue.values())

            return {
                "total_revenue": total_revenue,
                "system_revenue": system_revenue,
                "daily_trend": daily_trend,
                "platform_revenue": platform_revenue,
                "active_goals": active_goals,
                "period_days": days,
            }

        except Exception as e:
            logger.error(f"Failed to get revenue summary: {e}")
            return {}

    def get_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Get revenue optimization recommendations'\''
        recommendations = []

        try:
            summary = self.get_revenue_summary(30)

            # Check for underperforming systems
            total_revenue = summary.get("total_revenue", 0)
            if total_revenue > 0:
                for system, revenue in summary.get("system_revenue", {}).items():
                    percentage = (revenue / total_revenue) * 100
                    if percentage < 10:  # Less than 10% of total revenue
                        recommendations.append(
                            {
                                "type": "underperforming_system",
                                "system": system,
                                "revenue": revenue,
                                "percentage": percentage,
                                "recommendation": f"Focus on optimizing {system} - only contributing {percentage:.1f}% of revenue",
                            }
                        )

            # Check for goal progress
            for goal in summary.get("active_goals", []):
                if goal["progress"] < 50:  # Less than 50% progress
                    recommendations.append(
                        {
                            "type": "goal_optimization",
                            "goal": goal["name"],
                            "progress": goal["progress"],
                            "recommendation": f"Goal '{goal['name']}' is only {goal['progress']:.1f}% complete - consider increasing efforts",
                        }
                    )

            # Check for platform optimization
            platform_revenue = summary.get("platform_revenue", {})
            if platform_revenue:
                best_platform = max(platform_revenue.items(), key=lambda x: x[1])
                recommendations.append(
                    {
                        "type": "platform_optimization",
                        "platform": best_platform[0],
                        "revenue": best_platform[1],
                        "recommendation": f"Focus on {best_platform[0]} - your highest performing platform (${best_platform[1]:.2f})",
                    }
                )

        except Exception as e:
            logger.error(f"Failed to get optimization recommendations: {e}")

        return recommendations

    def generate_revenue_report(self, days: int = 30) -> str:
        """Generate a comprehensive revenue report"""
        try:
            summary = self.get_revenue_summary(days)
            recommendations = self.get_optimization_recommendations()

            report = f"""
# 💰 Revenue Dashboard Report - {datetime.datetime.now().strftime("%Y-%m-%d")}

## 📊 Revenue Summary ({days} days)
- **Total Revenue**: ${summary.get("total_revenue", 0):,.2f}
- **Daily Average**: ${summary.get("total_revenue", 0) / days:,.2f}
- **Projected Monthly**: ${summary.get("total_revenue", 0) * 30 / days:,.2f}

## 🏢 Revenue by System
"""

            for system, revenue in summary.get("system_revenue", {}).items():
                system_name = self.systems.get(system, system)
                percentage = (revenue / summary.get("total_revenue", 1)) * 100
                report += f"- **{system_name}**: ${revenue:,.2f} ({percentage:.1f}%)\n"

            report += """
## 🎯 Active Goals
"""

            for goal in summary.get("active_goals", []):
                report += f"- **{goal['name']}**: ${goal['current']:,.2f} / ${goal['target']:,.2f} ({goal['progress']:.1f}%)\n"

            report += """
## 🚀 Optimization Recommendations
"""

            for rec in recommendations:
                report += f"- **{rec['type'].replace('_', ' ').title()}**: {rec['recommendation']}\n"

            report += """
## 📈 Next Steps
1. Focus on highest-performing systems
2. Optimize underperforming platforms
3. Set realistic daily revenue targets
4. Track progress weekly
5. Scale successful strategies

---
*Generated by Passive Income Empire Revenue Dashboard*
"""

            return report

        except Exception as e:
            logger.error(f"Failed to generate revenue report: {e}")
            return f"Error generating report: {e}"


def main():
    """Main function for revenue dashboard"""
    try:
        print("💰 Revenue Dashboard - Passive Income Empire")
        print("=" * 50)

        dashboard = RevenueDashboard()

        # Add sample goals
        dashboard.add_revenue_goal(
            "Monthly $10K", 10000, "2024-12-31", "ai_recipe_generator"
        )
        dashboard.add_revenue_goal(
            "Weekly $2.5K", 2500, "2024-12-31", "ai_receptionist"
        )

        # Add sample revenue
        dashboard.update_revenue("ai_recipe_generator", 1500, "affiliate")
        dashboard.update_revenue("ai_receptionist", 800, "direct")

        # Generate report
        report = dashboard.generate_revenue_report()
        print(report)

        # Save report
        with open("revenue_report.md", "w") as f:
            f.write(report)

        print("✅ Revenue report saved to revenue_report.md")

    except Exception as e:
        logger.error(f"Main function failed: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
