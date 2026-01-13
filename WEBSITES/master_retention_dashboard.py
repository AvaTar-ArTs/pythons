#!/usr/bin/env python3
"""
🎯 Master Retention Dashboard
Comprehensive retention and return visit management system
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('retention_dashboard.log'),
        logging.StreamHandler()
    ]
)

@dataclass
class RetentionMetrics:
    """Retention metrics data structure"""
    daily_active_users: int
    monthly_active_users: int
    retention_rate_1d: float
    retention_rate_7d: float
    retention_rate_30d: float
    churn_rate: float
    lifetime_value: float
    revenue_per_user: float
    engagement_score: float
    content_creation_rate: float
    social_sharing_rate: float
    premium_conversion_rate: float

class MasterRetentionDashboard:
    """Master retention dashboard for all retention products"""
    
    def __init__(self):
        self.base_path = Path("/Users/steven/ai-sites/retention-products-suite")
        self.db_path = self.base_path / "retention_analytics.db"
        self.setup_database()
        
    def setup_database(self):
        """Set up retention analytics database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create retention metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS retention_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                date DATE NOT NULL,
                daily_active_users INTEGER,
                monthly_active_users INTEGER,
                retention_rate_1d REAL,
                retention_rate_7d REAL,
                retention_rate_30d REAL,
                churn_rate REAL,
                lifetime_value REAL,
                revenue_per_user REAL,
                engagement_score REAL,
                content_creation_rate REAL,
                social_sharing_rate REAL,
                premium_conversion_rate REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create user behavior table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_behavior (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                product_name TEXT NOT NULL,
                action_type TEXT NOT NULL,
                action_value REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create retention campaigns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS retention_campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_name TEXT NOT NULL,
                product_name TEXT NOT NULL,
                campaign_type TEXT NOT NULL,
                target_audience TEXT,
                start_date DATE,
                end_date DATE,
                budget REAL,
                expected_roi REAL,
                actual_roi REAL,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
    def track_user_action(self, user_id: str, product_name: str, action_type: str, action_value: float = 0.0):
        """Track user action for retention analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO user_behavior (user_id, product_name, action_type, action_value)
            VALUES (?, ?, ?, ?)
        """, (user_id, product_name, action_type, action_value))
        
        conn.commit()
        conn.close()
        
    def calculate_retention_metrics(self, product_name: str, date: datetime) -> RetentionMetrics:
        """Calculate retention metrics for a specific product and date"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Calculate daily active users
        cursor.execute("""
            SELECT COUNT(DISTINCT user_id) 
            FROM user_behavior 
            WHERE product_name = ? AND DATE(timestamp) = ?
        """, (product_name, date.date()))
        daily_active_users = cursor.fetchone()[0] or 0
        
        # Calculate monthly active users
        month_start = date.replace(day=1)
        cursor.execute("""
            SELECT COUNT(DISTINCT user_id) 
            FROM user_behavior 
            WHERE product_name = ? AND DATE(timestamp) >= ?
        """, (product_name, month_start.date()))
        monthly_active_users = cursor.fetchone()[0] or 0
        
        # Calculate retention rates
        retention_1d = self.calculate_retention_rate(product_name, date, 1)
        retention_7d = self.calculate_retention_rate(product_name, date, 7)
        retention_30d = self.calculate_retention_rate(product_name, date, 30)
        
        # Calculate churn rate
        churn_rate = 1 - retention_30d
        
        # Calculate lifetime value (simplified)
        cursor.execute("""
            SELECT AVG(action_value) 
            FROM user_behavior 
            WHERE product_name = ? AND action_type = 'revenue'
        """, (product_name,))
        lifetime_value = cursor.fetchone()[0] or 0.0
        
        # Calculate revenue per user
        cursor.execute("""
            SELECT SUM(action_value) / COUNT(DISTINCT user_id)
            FROM user_behavior 
            WHERE product_name = ? AND action_type = 'revenue' AND DATE(timestamp) = ?
        """, (product_name, date.date()))
        revenue_per_user = cursor.fetchone()[0] or 0.0
        
        # Calculate engagement score
        engagement_score = self.calculate_engagement_score(product_name, date)
        
        # Calculate content creation rate
        content_creation_rate = self.calculate_content_creation_rate(product_name, date)
        
        # Calculate social sharing rate
        social_sharing_rate = self.calculate_social_sharing_rate(product_name, date)
        
        # Calculate premium conversion rate
        premium_conversion_rate = self.calculate_premium_conversion_rate(product_name, date)
        
        conn.close()
        
        return RetentionMetrics(
            daily_active_users=daily_active_users,
            monthly_active_users=monthly_active_users,
            retention_rate_1d=retention_1d,
            retention_rate_7d=retention_7d,
            retention_rate_30d=retention_30d,
            churn_rate=churn_rate,
            lifetime_value=lifetime_value,
            revenue_per_user=revenue_per_user,
            engagement_score=engagement_score,
            content_creation_rate=content_creation_rate,
            social_sharing_rate=social_sharing_rate,
            premium_conversion_rate=premium_conversion_rate
        )
    
    def calculate_retention_rate(self, product_name: str, date: datetime, days: int) -> float:
        """Calculate retention rate for a specific period"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get users who were active on the target date
        cursor.execute("""
            SELECT DISTINCT user_id 
            FROM user_behavior 
            WHERE product_name = ? AND DATE(timestamp) = ?
        """, (product_name, date.date()))
        target_users = set(row[0] for row in cursor.fetchall())
        
        if not target_users:
            conn.close()
            return 0.0
        
        # Get users who were active days later
        target_date = date + timedelta(days=days)
        cursor.execute("""
            SELECT DISTINCT user_id 
            FROM user_behavior 
            WHERE product_name = ? AND DATE(timestamp) = ?
        """, (product_name, target_date.date()))
        retained_users = set(row[0] for row in cursor.fetchall())
        
        conn.close()
        
        return len(retained_users & target_users) / len(target_users) if target_users else 0.0
    
    def calculate_engagement_score(self, product_name: str, date: datetime) -> float:
        """Calculate engagement score based on user actions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get user actions for the date
        cursor.execute("""
            SELECT user_id, action_type, COUNT(*) as action_count
            FROM user_behavior 
            WHERE product_name = ? AND DATE(timestamp) = ?
            GROUP BY user_id, action_type
        """, (product_name, date.date()))
        
        user_actions = {}
        for user_id, action_type, count in cursor.fetchall():
            if user_id not in user_actions:
                user_actions[user_id] = {}
            user_actions[user_id][action_type] = count
        
        conn.close()
        
        if not user_actions:
            return 0.0
        
        # Calculate engagement score (weighted by action importance)
        action_weights = {
            'login': 1.0,
            'content_creation': 3.0,
            'social_sharing': 2.0,
            'premium_upgrade': 5.0,
            'community_participation': 2.5,
            'challenge_completion': 2.0
        }
        
        total_score = 0
        for user_id, actions in user_actions.items():
            user_score = sum(
                actions.get(action_type, 0) * weight 
                for action_type, weight in action_weights.items()
            )
            total_score += user_score
        
        return total_score / len(user_actions)
    
    def calculate_content_creation_rate(self, product_name: str, date: datetime) -> float:
        """Calculate content creation rate"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM user_behavior 
            WHERE product_name = ? AND action_type = 'content_creation' AND DATE(timestamp) = ?
        """, (product_name, date.date()))
        content_creations = cursor.fetchone()[0] or 0
        
        cursor.execute("""
            SELECT COUNT(DISTINCT user_id) 
            FROM user_behavior 
            WHERE product_name = ? AND DATE(timestamp) = ?
        """, (product_name, date.date()))
        active_users = cursor.fetchone()[0] or 1
        
        conn.close()
        
        return content_creations / active_users
    
    def calculate_social_sharing_rate(self, product_name: str, date: datetime) -> float:
        """Calculate social sharing rate"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM user_behavior 
            WHERE product_name = ? AND action_type = 'social_sharing' AND DATE(timestamp) = ?
        """, (product_name, date.date()))
        social_shares = cursor.fetchone()[0] or 0
        
        cursor.execute("""
            SELECT COUNT(DISTINCT user_id) 
            FROM user_behavior 
            WHERE product_name = ? AND DATE(timestamp) = ?
        """, (product_name, date.date()))
        active_users = cursor.fetchone()[0] or 1
        
        conn.close()
        
        return social_shares / active_users
    
    def calculate_premium_conversion_rate(self, product_name: str, date: datetime) -> float:
        """Calculate premium conversion rate"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM user_behavior 
            WHERE product_name = ? AND action_type = 'premium_upgrade' AND DATE(timestamp) = ?
        """, (product_name, date.date()))
        premium_upgrades = cursor.fetchone()[0] or 0
        
        cursor.execute("""
            SELECT COUNT(DISTINCT user_id) 
            FROM user_behavior 
            WHERE product_name = ? AND DATE(timestamp) = ?
        """, (product_name, date.date()))
        active_users = cursor.fetchone()[0] or 1
        
        conn.close()
        
        return premium_upgrades / active_users
    
    def generate_retention_report(self, product_name: str = None) -> Dict:
        """Generate comprehensive retention report"""
        today = datetime.now()
        
        if product_name:
            products = [product_name]
        else:
            products = [
                "digital-products", "saas-applications", "mobile-apps",
                "engagement-tools", "templates-marketplace", "community-platforms",
                "gamification-systems", "analytics-tracking"
            ]
        
        report = {
            "report_date": today.isoformat(),
            "products": {},
            "overall_metrics": {},
            "recommendations": []
        }
        
        total_dau = 0
        total_mau = 0
        total_revenue = 0.0
        
        for product in products:
            try:
                metrics = self.calculate_retention_metrics(product, today)
                report["products"][product] = {
                    "daily_active_users": metrics.daily_active_users,
                    "monthly_active_users": metrics.monthly_active_users,
                    "retention_rate_1d": round(metrics.retention_rate_1d * 100, 2),
                    "retention_rate_7d": round(metrics.retention_rate_7d * 100, 2),
                    "retention_rate_30d": round(metrics.retention_rate_30d * 100, 2),
                    "churn_rate": round(metrics.churn_rate * 100, 2),
                    "lifetime_value": round(metrics.lifetime_value, 2),
                    "revenue_per_user": round(metrics.revenue_per_user, 2),
                    "engagement_score": round(metrics.engagement_score, 2),
                    "content_creation_rate": round(metrics.content_creation_rate, 2),
                    "social_sharing_rate": round(metrics.social_sharing_rate, 2),
                    "premium_conversion_rate": round(metrics.premium_conversion_rate * 100, 2)
                }
                
                total_dau += metrics.daily_active_users
                total_mau += metrics.monthly_active_users
                total_revenue += metrics.revenue_per_user * metrics.daily_active_users
                
            except Exception as e:
                logging.error(f"Error calculating metrics for {product}: {e}")
                report["products"][product] = {"error": str(e)}
        
        # Calculate overall metrics
        report["overall_metrics"] = {
            "total_daily_active_users": total_dau,
            "total_monthly_active_users": total_mau,
            "total_daily_revenue": round(total_revenue, 2),
            "average_retention_rate_30d": round(
                sum(
                    report["products"][p].get("retention_rate_30d", 0) 
                    for p in products if "retention_rate_30d" in report["products"].get(p, {})
                ) / len(products), 2
            ),
            "average_engagement_score": round(
                sum(
                    report["products"][p].get("engagement_score", 0) 
                    for p in products if "engagement_score" in report["products"].get(p, {})
                ) / len(products), 2
            )
        }
        
        # Generate recommendations
        report["recommendations"] = self.generate_recommendations(report)
        
        return report
    
    def generate_recommendations(self, report: Dict) -> List[str]:
        """Generate retention improvement recommendations"""
        recommendations = []
        
        overall_metrics = report.get("overall_metrics", {})
        avg_retention = overall_metrics.get("average_retention_rate_30d", 0)
        avg_engagement = overall_metrics.get("average_engagement_score", 0)
        
        if avg_retention < 20:
            recommendations.append("🚨 CRITICAL: 30-day retention rate is below 20%. Implement immediate re-engagement campaigns.")
        elif avg_retention < 40:
            recommendations.append("⚠️ WARNING: 30-day retention rate is below 40%. Focus on improving user onboarding and early engagement.")
        
        if avg_engagement < 10:
            recommendations.append("🎯 Focus on increasing user engagement through gamification and social features.")
        
        # Product-specific recommendations
        for product, metrics in report.get("products", {}).items():
            if isinstance(metrics, dict) and "error" not in metrics:
                retention_30d = metrics.get("retention_rate_30d", 0)
                engagement = metrics.get("engagement_score", 0)
                churn = metrics.get("churn_rate", 0)
                
                if retention_30d < 30:
                    recommendations.append(f"📊 {product}: Low retention rate ({retention_30d}%). Implement retention campaigns.")
                
                if churn > 50:
                    recommendations.append(f"🔄 {product}: High churn rate ({churn}%). Focus on churn prevention.")
                
                if engagement < 5:
                    recommendations.append(f"🎮 {product}: Low engagement ({engagement}). Add gamification elements.")
        
        if not recommendations:
            recommendations.append("✅ All retention metrics are performing well. Continue current strategies and monitor for optimization opportunities.")
        
        return recommendations
    
    def save_retention_metrics(self, product_name: str, metrics: RetentionMetrics):
        """Save retention metrics to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO retention_metrics (
                product_name, date, daily_active_users, monthly_active_users,
                retention_rate_1d, retention_rate_7d, retention_rate_30d,
                churn_rate, lifetime_value, revenue_per_user, engagement_score,
                content_creation_rate, social_sharing_rate, premium_conversion_rate
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            product_name, datetime.now().date(),
            metrics.daily_active_users, metrics.monthly_active_users,
            metrics.retention_rate_1d, metrics.retention_rate_7d, metrics.retention_rate_30d,
            metrics.churn_rate, metrics.lifetime_value, metrics.revenue_per_user,
            metrics.engagement_score, metrics.content_creation_rate,
            metrics.social_sharing_rate, metrics.premium_conversion_rate
        ))
        
        conn.commit()
        conn.close()
    
    def display_dashboard(self):
        """Display the retention dashboard"""
        print("🎯 Master Retention Dashboard")
        print("=" * 50)
        print(f"📅 Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Generate and display report
        report = self.generate_retention_report()
        
        # Display overall metrics
        overall = report["overall_metrics"]
        print("📊 Overall Metrics:")
        print(f"   Daily Active Users: {overall['total_daily_active_users']:,}")
        print(f"   Monthly Active Users: {overall['total_monthly_active_users']:,}")
        print(f"   Daily Revenue: ${overall['total_daily_revenue']:,.2f}")
        print(f"   Average 30-day Retention: {overall['average_retention_rate_30d']}%")
        print(f"   Average Engagement Score: {overall['average_engagement_score']}")
        print()
        
        # Display product metrics
        print("📈 Product Performance:")
        for product, metrics in report["products"].items():
            if isinstance(metrics, dict) and "error" not in metrics:
                print(f"   {product}:")
                print(f"     DAU: {metrics['daily_active_users']:,}")
                print(f"     MAU: {metrics['monthly_active_users']:,}")
                print(f"     30-day Retention: {metrics['retention_rate_30d']}%")
                print(f"     Engagement Score: {metrics['engagement_score']}")
                print(f"     Revenue per User: ${metrics['revenue_per_user']:.2f}")
                print()
        
        # Display recommendations
        print("💡 Recommendations:")
        for i, rec in enumerate(report["recommendations"], 1):
            print(f"   {i}. {rec}")
        print()
        
        # Save report
        report_path = self.base_path / "reports" / f"retention_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Report saved to: {report_path}")

def main():
    """Main function to run the retention dashboard"""
    dashboard = MasterRetentionDashboard()
    dashboard.display_dashboard()

if __name__ == "__main__":
    main()