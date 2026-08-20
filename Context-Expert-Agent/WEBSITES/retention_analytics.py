#!/usr/bin/env python3
"""
📊 Retention Analytics - User Behavior Intelligence
Comprehensive analytics system for user retention optimization
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import logging
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class UserSession:
    """User session data structure"""
    session_id: str
    user_id: str
    start_time: datetime
    end_time: Optional[datetime]
    duration_minutes: int
    page_views: int
    actions: int
    device_type: str
    browser: str
    location: str

@dataclass
class RetentionMetrics:
    """Retention metrics data structure"""
    date: str
    cohort_size: int
    day_1_retention: float
    day_7_retention: float
    day_30_retention: float
    churn_rate: float
    lifetime_value: float
    engagement_score: float

class RetentionAnalytics:
    """Main retention analytics system"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or "/Users/steven/ai-sites/retention-products-suite/analytics-tracking/retention_analytics.db"
        self.setup_database()
        
    def setup_database(self):
        """Set up analytics database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User sessions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP,
                duration_minutes INTEGER DEFAULT 0,
                page_views INTEGER DEFAULT 0,
                actions INTEGER DEFAULT 0,
                device_type TEXT,
                browser TEXT,
                location TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # User actions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                session_id TEXT,
                action_type TEXT NOT NULL,
                action_value REAL DEFAULT 0,
                page_url TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT  -- JSON data
            )
        """)
        
        # User events
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                event_data TEXT,  -- JSON data
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Cohort data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_cohorts (
                user_id TEXT PRIMARY KEY,
                cohort_date DATE NOT NULL,
                first_action_date DATE NOT NULL,
                last_action_date DATE,
                total_sessions INTEGER DEFAULT 0,
                total_actions INTEGER DEFAULT 0,
                total_revenue REAL DEFAULT 0,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        
        # Retention metrics
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS retention_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                cohort_date DATE NOT NULL,
                day_number INTEGER NOT NULL,
                users_retained INTEGER DEFAULT 0,
                retention_rate REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Feature usage
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feature_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                feature_name TEXT NOT NULL,
                usage_count INTEGER DEFAULT 1,
                first_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_time_minutes INTEGER DEFAULT 0
            )
        """)
        
        # Conversion funnels
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversion_funnels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                funnel_name TEXT NOT NULL,
                step_number INTEGER NOT NULL,
                step_name TEXT NOT NULL,
                users_entered INTEGER DEFAULT 0,
                users_completed INTEGER DEFAULT 0,
                conversion_rate REAL DEFAULT 0,
                date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def track_session(self, session_id: str, user_id: str, start_time: datetime, 
                     device_type: str = "desktop", browser: str = "chrome", 
                     location: str = "unknown") -> bool:
        """Track user session start"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO user_sessions 
                (session_id, user_id, start_time, device_type, browser, location)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (session_id, user_id, start_time, device_type, browser, location))
            
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error tracking session {session_id}: {e}")
            return False
        finally:
            conn.close()
    
    def end_session(self, session_id: str, end_time: datetime = None) -> bool:
        """End user session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            if end_time is None:
                end_time = datetime.now()
            
            # Calculate duration
            cursor.execute("SELECT start_time FROM user_sessions WHERE session_id = ?", (session_id,))
            start_time = cursor.fetchone()
            
            if not start_time:
                return False
            
            start_time = datetime.fromisoformat(start_time[0])
            duration = (end_time - start_time).total_seconds() / 60
            
            # Get session stats
            cursor.execute("""
                SELECT COUNT(*) FROM user_actions WHERE session_id = ?
            """, (session_id,))
            actions = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(DISTINCT page_url) FROM user_actions WHERE session_id = ?
            """, (session_id,))
            page_views = cursor.fetchone()[0]
            
            # Update session
            cursor.execute("""
                UPDATE user_sessions 
                SET end_time = ?, duration_minutes = ?, actions = ?, page_views = ?
                WHERE session_id = ?
            """, (end_time, duration, actions, page_views, session_id))
            
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error ending session {session_id}: {e}")
            return False
        finally:
            conn.close()
    
    def track_action(self, user_id: str, action_type: str, action_value: float = 0, 
                    session_id: str = None, page_url: str = None, metadata: Dict = None) -> bool:
        """Track user action"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            metadata_json = json.dumps(metadata) if metadata else None
            
            cursor.execute("""
                INSERT INTO user_actions 
                (user_id, session_id, action_type, action_value, page_url, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, session_id, action_type, action_value, page_url, metadata_json))
            
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error tracking action for user {user_id}: {e}")
            return False
        finally:
            conn.close()
    
    def track_event(self, user_id: str, event_type: str, event_data: Dict = None) -> bool:
        """Track user event"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            event_data_json = json.dumps(event_data) if event_data else None
            
            cursor.execute("""
                INSERT INTO user_events (user_id, event_type, event_data)
                VALUES (?, ?, ?)
            """, (user_id, event_type, event_data_json))
            
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error tracking event for user {user_id}: {e}")
            return False
        finally:
            conn.close()
    
    def calculate_retention_metrics(self, start_date: datetime, end_date: datetime) -> List[RetentionMetrics]:
        """Calculate retention metrics for a date range"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get cohort data
        cursor.execute("""
            SELECT cohort_date, COUNT(*) as cohort_size
            FROM user_cohorts
            WHERE cohort_date BETWEEN ? AND ?
            GROUP BY cohort_date
            ORDER BY cohort_date
        """, (start_date.date(), end_date.date()))
        
        cohorts = cursor.fetchall()
        retention_metrics = []
        
        for cohort_date, cohort_size in cohorts:
            # Calculate day 1 retention
            day_1_retention = self._calculate_retention_rate(cohort_date, 1)
            
            # Calculate day 7 retention
            day_7_retention = self._calculate_retention_rate(cohort_date, 7)
            
            # Calculate day 30 retention
            day_30_retention = self._calculate_retention_rate(cohort_date, 30)
            
            # Calculate churn rate
            churn_rate = 1 - day_30_retention
            
            # Calculate lifetime value
            lifetime_value = self._calculate_lifetime_value(cohort_date)
            
            # Calculate engagement score
            engagement_score = self._calculate_engagement_score(cohort_date)
            
            retention_metrics.append(RetentionMetrics(
                date=cohort_date.isoformat(),
                cohort_size=cohort_size,
                day_1_retention=day_1_retention,
                day_7_retention=day_7_retention,
                day_30_retention=day_30_retention,
                churn_rate=churn_rate,
                lifetime_value=lifetime_value,
                engagement_score=engagement_score
            ))
        
        conn.close()
        return retention_metrics
    
    def _calculate_retention_rate(self, cohort_date: datetime, days: int) -> float:
        """Calculate retention rate for a specific cohort and day"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get users who were active on the target day
        target_date = cohort_date + timedelta(days=days)
        
        cursor.execute("""
            SELECT COUNT(DISTINCT user_id)
            FROM user_actions
            WHERE DATE(timestamp) = ?
        """, (target_date.date(),))
        
        active_users = cursor.fetchone()[0]
        
        # Get cohort size
        cursor.execute("""
            SELECT COUNT(*) FROM user_cohorts WHERE cohort_date = ?
        """, (cohort_date.date(),))
        
        cohort_size = cursor.fetchone()[0]
        
        conn.close()
        
        return active_users / cohort_size if cohort_size > 0 else 0.0
    
    def _calculate_lifetime_value(self, cohort_date: datetime) -> float:
        """Calculate average lifetime value for a cohort"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT AVG(total_revenue)
            FROM user_cohorts
            WHERE cohort_date = ?
        """, (cohort_date.date(),))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result[0] else 0.0
    
    def _calculate_engagement_score(self, cohort_date: datetime) -> float:
        """Calculate engagement score for a cohort"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get average actions per user
        cursor.execute("""
            SELECT AVG(total_actions)
            FROM user_cohorts
            WHERE cohort_date = ?
        """, (cohort_date.date(),))
        
        avg_actions = cursor.fetchone()[0] or 0
        
        # Get average sessions per user
        cursor.execute("""
            SELECT AVG(total_sessions)
            FROM user_cohorts
            WHERE cohort_date = ?
        """, (cohort_date.date(),))
        
        avg_sessions = cursor.fetchone()[0] or 0
        
        conn.close()
        
        # Calculate engagement score (weighted combination)
        engagement_score = (avg_actions * 0.7) + (avg_sessions * 0.3)
        return engagement_score
    
    def get_user_journey(self, user_id: str) -> List[Dict]:
        """Get user journey data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT action_type, action_value, page_url, timestamp, metadata
            FROM user_actions
            WHERE user_id = ?
            ORDER BY timestamp
        """, (user_id,))
        
        actions = cursor.fetchall()
        conn.close()
        
        journey = []
        for action in actions:
            journey.append({
                'action_type': action[0],
                'action_value': action[1],
                'page_url': action[2],
                'timestamp': action[3],
                'metadata': json.loads(action[4]) if action[4] else {}
            })
        
        return journey
    
    def get_conversion_funnel(self, funnel_name: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get conversion funnel data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT step_number, step_name, users_entered, users_completed, conversion_rate
            FROM conversion_funnels
            WHERE funnel_name = ? AND date BETWEEN ? AND ?
            ORDER BY step_number
        """, (funnel_name, start_date.date(), end_date.date()))
        
        funnel_data = cursor.fetchall()
        conn.close()
        
        return [{
            'step_number': step[0],
            'step_name': step[1],
            'users_entered': step[2],
            'users_completed': step[3],
            'conversion_rate': step[4]
        } for step in funnel_data]
    
    def get_feature_usage(self, feature_name: str = None, start_date: datetime = None, end_date: datetime = None) -> List[Dict]:
        """Get feature usage analytics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT feature_name, COUNT(*) as users, SUM(usage_count) as total_usage, AVG(usage_count) as avg_usage FROM feature_usage WHERE 1=1"
        params = []
        
        if feature_name:
            query += " AND feature_name = ?"
            params.append(feature_name)
        
        if start_date:
            query += " AND first_used >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND first_used <= ?"
            params.append(end_date)
        
        query += " GROUP BY feature_name ORDER BY total_usage DESC"
        
        cursor.execute(query, params)
        usage_data = cursor.fetchall()
        conn.close()
        
        return [{
            'feature_name': usage[0],
            'users': usage[1],
            'total_usage': usage[2],
            'avg_usage': usage[3]
        } for usage in usage_data]
    
    def get_churn_prediction(self, user_id: str) -> Dict:
        """Predict churn probability for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get user activity data
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT DATE(timestamp)) as active_days,
                COUNT(*) as total_actions,
                MAX(timestamp) as last_activity,
                AVG(CASE WHEN action_type = 'session_duration' THEN action_value ELSE 0 END) as avg_session_duration
            FROM user_actions
            WHERE user_id = ? AND timestamp >= date('now', '-30 days')
        """, (user_id,))
        
        activity_data = cursor.fetchone()
        
        if not activity_data:
            conn.close()
            return {'churn_probability': 0.5, 'risk_factors': ['No recent activity']}
        
        active_days, total_actions, last_activity, avg_session_duration = activity_data
        
        # Calculate days since last activity
        if last_activity:
            last_activity = datetime.fromisoformat(last_activity)
            days_since_activity = (datetime.now() - last_activity).days
        else:
            days_since_activity = 30
        
        # Simple churn prediction model
        churn_score = 0
        
        # Risk factors
        risk_factors = []
        
        if days_since_activity > 7:
            churn_score += 0.3
            risk_factors.append('No activity for 7+ days')
        
        if active_days < 5:
            churn_score += 0.2
            risk_factors.append('Low activity days')
        
        if total_actions < 10:
            churn_score += 0.2
            risk_factors.append('Low total actions')
        
        if avg_session_duration and avg_session_duration < 2:
            churn_score += 0.1
            risk_factors.append('Short session duration')
        
        # Normalize to 0-1 probability
        churn_probability = min(churn_score, 1.0)
        
        conn.close()
        
        return {
            'churn_probability': churn_probability,
            'risk_factors': risk_factors,
            'activity_score': {
                'active_days': active_days,
                'total_actions': total_actions,
                'days_since_activity': days_since_activity,
                'avg_session_duration': avg_session_duration
            }
        }
    
    def generate_retention_report(self, start_date: datetime, end_date: datetime) -> Dict:
        """Generate comprehensive retention report"""
        retention_metrics = self.calculate_retention_metrics(start_date, end_date)
        
        # Calculate averages
        avg_day_1_retention = np.mean([m.day_1_retention for m in retention_metrics])
        avg_day_7_retention = np.mean([m.day_7_retention for m in retention_metrics])
        avg_day_30_retention = np.mean([m.day_30_retention for m in retention_metrics])
        avg_churn_rate = np.mean([m.churn_rate for m in retention_metrics])
        avg_lifetime_value = np.mean([m.lifetime_value for m in retention_metrics])
        avg_engagement_score = np.mean([m.engagement_score for m in retention_metrics])
        
        # Get feature usage
        feature_usage = self.get_feature_usage(start_date=start_date, end_date=end_date)
        
        # Get top features
        top_features = sorted(feature_usage, key=lambda x: x['total_usage'], reverse=True)[:5]
        
        # Generate recommendations
        recommendations = self._generate_recommendations(retention_metrics, feature_usage)
        
        report = {
            'report_period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            },
            'retention_metrics': {
                'average_day_1_retention': round(avg_day_1_retention * 100, 2),
                'average_day_7_retention': round(avg_day_7_retention * 100, 2),
                'average_day_30_retention': round(avg_day_30_retention * 100, 2),
                'average_churn_rate': round(avg_churn_rate * 100, 2),
                'average_lifetime_value': round(avg_lifetime_value, 2),
                'average_engagement_score': round(avg_engagement_score, 2)
            },
            'feature_usage': {
                'top_features': top_features,
                'total_features_used': len(feature_usage)
            },
            'recommendations': recommendations,
            'detailed_metrics': [
                {
                    'date': m.date,
                    'cohort_size': m.cohort_size,
                    'day_1_retention': round(m.day_1_retention * 100, 2),
                    'day_7_retention': round(m.day_7_retention * 100, 2),
                    'day_30_retention': round(m.day_30_retention * 100, 2),
                    'churn_rate': round(m.churn_rate * 100, 2),
                    'lifetime_value': round(m.lifetime_value, 2),
                    'engagement_score': round(m.engagement_score, 2)
                }
                for m in retention_metrics
            ]
        }
        
        return report
    
    def _generate_recommendations(self, retention_metrics: List[RetentionMetrics], feature_usage: List[Dict]) -> List[str]:
        """Generate retention improvement recommendations"""
        recommendations = []
        
        # Analyze retention metrics
        avg_day_1_retention = np.mean([m.day_1_retention for m in retention_metrics])
        avg_day_7_retention = np.mean([m.day_7_retention for m in retention_metrics])
        avg_day_30_retention = np.mean([m.day_30_retention for m in retention_metrics])
        
        if avg_day_1_retention < 0.3:
            recommendations.append("🚨 CRITICAL: Day 1 retention is below 30%. Focus on improving onboarding experience and first-time user value.")
        elif avg_day_1_retention < 0.5:
            recommendations.append("⚠️ WARNING: Day 1 retention is below 50%. Consider improving welcome flow and immediate value delivery.")
        
        if avg_day_7_retention < 0.2:
            recommendations.append("📈 Focus on improving Day 7 retention through engagement campaigns and habit formation.")
        
        if avg_day_30_retention < 0.1:
            recommendations.append("🎯 Implement long-term retention strategies including community features and advanced functionality.")
        
        # Analyze feature usage
        if feature_usage:
            underused_features = [f for f in feature_usage if f['users'] < 10]
            if underused_features:
                recommendations.append(f"🔧 Consider promoting or improving {len(underused_features)} underused features.")
        
        if not recommendations:
            recommendations.append("✅ Retention metrics are performing well. Continue current strategies and monitor for optimization opportunities.")
        
        return recommendations

def main():
    """Main function to test retention analytics"""
    analytics = RetentionAnalytics()
    
    print("📊 Retention Analytics - User Behavior Intelligence")
    print("=" * 60)
    
    # Test session tracking
    session_id = "test_session_123"
    user_id = "test_user_123"
    start_time = datetime.now()
    
    analytics.track_session(session_id, user_id, start_time)
    print(f"✅ Session tracked: {session_id}")
    
    # Test action tracking
    analytics.track_action(user_id, "page_view", 1, session_id, "/dashboard")
    analytics.track_action(user_id, "button_click", 1, session_id, "/dashboard")
    print(f"✅ Actions tracked for user: {user_id}")
    
    # End session
    analytics.end_session(session_id)
    print(f"✅ Session ended: {session_id}")
    
    # Generate report
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    report = analytics.generate_retention_report(start_date, end_date)
    print(f"✅ Retention report generated")
    print(f"   - Average Day 1 Retention: {report['retention_metrics']['average_day_1_retention']}%")
    print(f"   - Average Day 7 Retention: {report['retention_metrics']['average_day_7_retention']}%")
    print(f"   - Average Day 30 Retention: {report['retention_metrics']['average_day_30_retention']}%")
    
    print("\n🎉 Retention analytics system is ready!")

if __name__ == "__main__":
    main()