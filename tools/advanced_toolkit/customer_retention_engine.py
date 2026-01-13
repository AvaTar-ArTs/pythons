#!/usr/bin/env python3
"""
💰 CUSTOMER RETENTION ENGINE
Advanced content-aware customer retention and revenue optimization system

Features:
- Tracks customer interactions across all revenue streams
- AI-powered personalization using multi-LLM orchestration
- Predictive churn analysis
- Automated re-engagement campaigns
- Cross-sell opportunity identification
- Lifetime value calculation and optimization
"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
import sys

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from config_manager import get_config
    from file_intelligence import FileAnalyzer
except ImportError:
    print("Warning: Some dependencies not available")


@dataclass
class Customer:
    """Customer profile with comprehensive tracking"""
    id: str
    email: str
    name: str
    first_purchase_date: datetime
    last_interaction_date: datetime
    total_spent: float
    purchase_count: int
    revenue_streams: List[str] = field(default_factory=list)
    preferences: Dict[str, any] = field(default_factory=dict)
    churn_risk_score: float = 0.0
    lifetime_value: float = 0.0
    tags: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class RetentionAction:
    """Automated retention action"""
    customer_id: str
    action_type: str  # "email", "offer", "check_in", "upsell"
    content: str
    priority: int  # 1-10, 10 being highest
    estimated_roi: float
    ai_generated: bool = True


class CustomerRetentionEngine:
    """Advanced customer retention and revenue optimization"""
    
    def __init__(self, db_path: Path = None):
        self.db_path = db_path or Path.home() / '.customer_intelligence.db'
        self.config = get_config() if 'get_config' in sys.modules else None
        self._init_database()
        self.customers: Dict[str, Customer] = {}
    
    def _init_database(self):
        """Initialize customer intelligence database"""
        conn = sqlite3.connect(str(self.db_path))
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS customers (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                name TEXT,
                first_purchase_date REAL,
                last_interaction_date REAL,
                total_spent REAL DEFAULT 0,
                purchase_count INTEGER DEFAULT 0,
                revenue_streams TEXT,  -- JSON array
                preferences TEXT,      -- JSON object
                churn_risk_score REAL DEFAULT 0,
                lifetime_value REAL DEFAULT 0,
                tags TEXT,             -- JSON array
                notes TEXT
            );
            
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT,
                interaction_type TEXT,  -- purchase, email_open, click, support
                revenue_stream TEXT,
                timestamp REAL,
                value REAL DEFAULT 0,
                metadata TEXT,          -- JSON object
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            );
            
            CREATE TABLE IF NOT EXISTS retention_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT,
                action_type TEXT,
                content TEXT,
                priority INTEGER,
                estimated_roi REAL,
                status TEXT DEFAULT 'pending',  -- pending, sent, completed, failed
                created_at REAL,
                executed_at REAL,
                result TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            );
            
            CREATE INDEX IF NOT EXISTS idx_customer_email ON customers(email);
            CREATE INDEX IF NOT EXISTS idx_interactions_customer ON interactions(customer_id);
            CREATE INDEX IF NOT EXISTS idx_interactions_timestamp ON interactions(timestamp);
            CREATE INDEX IF NOT EXISTS idx_actions_customer ON retention_actions(customer_id);
            CREATE INDEX IF NOT EXISTS idx_actions_status ON retention_actions(status);
        """)
        conn.commit()
        conn.close()
    
    def add_customer(self, customer: Customer):
        """Add or update customer"""
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            INSERT OR REPLACE INTO customers 
            (id, email, name, first_purchase_date, last_interaction_date, 
             total_spent, purchase_count, revenue_streams, preferences,
             churn_risk_score, lifetime_value, tags, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            customer.id,
            customer.email,
            customer.name,
            customer.first_purchase_date.timestamp(),
            customer.last_interaction_date.timestamp(),
            customer.total_spent,
            customer.purchase_count,
            json.dumps(customer.revenue_streams),
            json.dumps(customer.preferences),
            customer.churn_risk_score,
            customer.lifetime_value,
            json.dumps(customer.tags),
            customer.notes
        ))
        conn.commit()
        conn.close()
        self.customers[customer.id] = customer
    
    def record_interaction(self, customer_id: str, interaction_type: str, 
                          revenue_stream: str, value: float = 0.0, 
                          metadata: Dict = None):
        """Record customer interaction"""
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            INSERT INTO interactions 
            (customer_id, interaction_type, revenue_stream, timestamp, value, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            customer_id,
            interaction_type,
            revenue_stream,
            datetime.now().timestamp(),
            value,
            json.dumps(metadata or {})
        ))
        
        # Update customer stats
        if interaction_type == 'purchase':
            conn.execute("""
                UPDATE customers 
                SET total_spent = total_spent + ?,
                    purchase_count = purchase_count + 1,
                    last_interaction_date = ?
                WHERE id = ?
            """, (value, datetime.now().timestamp(), customer_id))
        
        conn.commit()
        conn.close()
    
    def calculate_churn_risk(self, customer_id: str) -> float:
        """Calculate churn risk score (0-1, higher = more risk)"""
        conn = sqlite3.connect(str(self.db_path))
        
        # Get customer data
        cursor = conn.execute("""
            SELECT first_purchase_date, last_interaction_date, purchase_count, total_spent
            FROM customers WHERE id = ?
        """, (customer_id,))
        row = cursor.fetchone()
        
        if not row:
            return 0.5  # Default risk
        
        first_purchase, last_interaction, purchase_count, total_spent = row
        
        # Calculate days since last interaction
        days_since = (datetime.now().timestamp() - last_interaction) / 86400
        
        # Risk factors
        risk = 0.0
        
        # Time-based risk
        if days_since > 90:
            risk += 0.4
        elif days_since > 60:
            risk += 0.3
        elif days_since > 30:
            risk += 0.2
        
        # Purchase frequency risk
        if purchase_count == 1 and days_since > 30:
            risk += 0.3  # One-time buyer, long time ago
        elif purchase_count > 1:
            avg_days_between = (last_interaction - first_purchase) / (purchase_count - 1) / 86400
            if days_since > avg_days_between * 2:
                risk += 0.2
        
        # Value-based risk (high-value customers less likely to churn)
        if total_spent > 500:
            risk -= 0.2
        elif total_spent > 200:
            risk -= 0.1
        
        return min(1.0, max(0.0, risk))
    
    def calculate_lifetime_value(self, customer_id: str) -> float:
        """Calculate predicted customer lifetime value"""
        conn = sqlite3.connect(str(self.db_path))
        
        cursor = conn.execute("""
            SELECT total_spent, purchase_count, first_purchase_date
            FROM customers WHERE id = ?
        """, (customer_id,))
        row = cursor.fetchone()
        
        if not row:
            return 0.0
        
        total_spent, purchase_count, first_purchase = row
        
        if purchase_count == 0:
            return 0.0
        
        # Calculate average purchase value
        avg_purchase = total_spent / purchase_count
        
        # Calculate purchase frequency
        days_active = (datetime.now().timestamp() - first_purchase) / 86400
        if days_active > 0:
            purchases_per_month = (purchase_count / days_active) * 30
        else:
            purchases_per_month = 0
        
        # Predict future value (assuming 12 months retention)
        months_remaining = 12
        predicted_value = avg_purchase * purchases_per_month * months_remaining
        
        # Add current value
        lifetime_value = total_spent + predicted_value
        
        return lifetime_value
    
    def identify_retention_actions(self, customer_id: str) -> List[RetentionAction]:
        """Identify automated retention actions for customer"""
        actions = []
        
        churn_risk = self.calculate_churn_risk(customer_id)
        lifetime_value = self.calculate_lifetime_value(customer_id)
        
        # High churn risk actions
        if churn_risk > 0.6:
            actions.append(RetentionAction(
                customer_id=customer_id,
                action_type="re_engagement_email",
                content="We miss you! Here's a special offer...",
                priority=10,
                estimated_roi=lifetime_value * 0.1,  # 10% of LTV
                ai_generated=True
            ))
        
        # Cross-sell opportunities
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.execute("""
            SELECT revenue_streams FROM customers WHERE id = ?
        """, (customer_id,))
        row = cursor.fetchone()
        
        if row:
            revenue_streams = json.loads(row[0] or '[]')
            
            # If customer only in one stream, suggest others
            if len(revenue_streams) == 1:
                stream = revenue_streams[0]
                if stream == 'music':
                    actions.append(RetentionAction(
                        customer_id=customer_id,
                        action_type="cross_sell",
                        content="Love our music? Check out our art gallery!",
                        priority=7,
                        estimated_roi=50.0,
                        ai_generated=True
                    ))
                elif stream == 'art':
                    actions.append(RetentionAction(
                        customer_id=customer_id,
                        action_type="cross_sell",
                        content="Complete your collection with our music!",
                        priority=7,
                        estimated_roi=30.0,
                        ai_generated=True
                    ))
        
        # Upsell opportunities for high-value customers
        if lifetime_value > 500:
            actions.append(RetentionAction(
                customer_id=customer_id,
                action_type="upsell",
                content="Upgrade to premium for exclusive benefits!",
                priority=8,
                estimated_roi=100.0,
                ai_generated=True
            ))
        
        return actions
    
    def generate_personalized_content(self, customer_id: str, action_type: str) -> str:
        """Generate AI-powered personalized content"""
        # This would use multi-llm-orchestrator in production
        # For now, return template-based content
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.execute("""
            SELECT name, preferences, revenue_streams, total_spent
            FROM customers WHERE id = ?
        """, (customer_id,))
        row = cursor.fetchone()
        
        if not row:
            return "Hello! We have something special for you..."
        
        name, preferences_json, streams_json, total_spent = row
        preferences = json.loads(preferences_json or '{}')
        streams = json.loads(streams_json or '[]')
        
        if action_type == "re_engagement_email":
            return f"""
Hi {name or 'there'}!

We noticed you haven't been around lately, and we wanted to check in. 
We've got some new content that matches your preferences: {', '.join(preferences.get('genres', ['various styles']))}

As a valued customer (you've spent ${total_spent:.2f} with us!), 
here's a special 20% off code: WELCOMEBACK20

Come see what's new!
"""
        
        elif action_type == "cross_sell":
            if 'music' in streams:
                return f"Hi {name}! Since you love our music, you might enjoy our art gallery featuring album artwork and prints!"
            elif 'art' in streams:
                return f"Hi {name}! Complete your collection with our music - perfect background for your art displays!"
        
        elif action_type == "upsell":
            return f"""
Hi {name}!

As one of our top customers (${total_spent:.2f} spent!), you're eligible for our Premium membership.

Benefits:
- Exclusive content access
- 30% off all purchases
- Early access to new releases
- Priority support

Upgrade now for just $99/month (normally $149)!
"""
        
        return "Hello! We have something special for you..."
    
    def execute_retention_action(self, action: RetentionAction) -> bool:
        """Execute a retention action"""
        # Generate personalized content
        content = self.generate_personalized_content(action.customer_id, action.action_type)
        
        # Store action
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            INSERT INTO retention_actions
            (customer_id, action_type, content, priority, estimated_roi, status, created_at)
            VALUES (?, ?, ?, ?, ?, 'sent', ?)
        """, (
            action.customer_id,
            action.action_type,
            content,
            action.priority,
            action.estimated_roi,
            datetime.now().timestamp()
        ))
        conn.commit()
        conn.close()
        
        # In production, this would:
        # - Send email via SendGrid/Mailchimp
        # - Create task in CRM
        # - Trigger webhook
        # - Log to analytics
        
        print(f"✅ Executed {action.action_type} for customer {action.customer_id}")
        print(f"   Content: {content[:100]}...")
        
        return True
    
    def process_retention_queue(self, limit: int = 50):
        """Process pending retention actions"""
        conn = sqlite3.connect(str(self.db_path))
        
        # Get high-priority pending actions
        cursor = conn.execute("""
            SELECT customer_id, action_type, content, priority, estimated_roi
            FROM retention_actions
            WHERE status = 'pending'
            ORDER BY priority DESC, estimated_roi DESC
            LIMIT ?
        """, (limit,))
        
        actions = []
        for row in cursor:
            actions.append(RetentionAction(
                customer_id=row[0],
                action_type=row[1],
                content=row[2],
                priority=row[3],
                estimated_roi=row[4]
            ))
        
        conn.close()
        
        # Execute actions
        for action in actions:
            self.execute_retention_action(action)
    
    def generate_retention_report(self) -> str:
        """Generate comprehensive retention report"""
        conn = sqlite3.connect(str(self.db_path))
        
        # Customer statistics
        cursor = conn.execute("""
            SELECT 
                COUNT(*) as total_customers,
                SUM(total_spent) as total_revenue,
                AVG(total_spent) as avg_customer_value,
                AVG(purchase_count) as avg_purchases,
                COUNT(CASE WHEN churn_risk_score > 0.6 THEN 1 END) as high_risk_customers
            FROM customers
        """)
        stats = cursor.fetchone()
        
        # Recent interactions
        cursor = conn.execute("""
            SELECT COUNT(*) 
            FROM interactions 
            WHERE timestamp > ?
        """, ((datetime.now() - timedelta(days=30)).timestamp(),))
        recent_interactions = cursor.fetchone()[0]
        
        # Pending actions
        cursor = conn.execute("""
            SELECT COUNT(*) 
            FROM retention_actions 
            WHERE status = 'pending'
        """)
        pending_actions = cursor.fetchone()[0]
        
        conn.close()
        
        report = f"""
💰 CUSTOMER RETENTION REPORT
{'='*60}

📊 CUSTOMER STATISTICS
Total Customers: {stats[0]}
Total Revenue: ${stats[1]:,.2f}
Average Customer Value: ${stats[2]:,.2f}
Average Purchases per Customer: {stats[3]:.1f}

⚠️  CHURN RISK
High Risk Customers (>60%): {stats[4]}

📈 ACTIVITY (Last 30 Days)
Recent Interactions: {recent_interactions}

🎯 RETENTION ACTIONS
Pending Actions: {pending_actions}

💡 RECOMMENDATIONS
1. Process {pending_actions} pending retention actions
2. Focus on {stats[4]} high-risk customers
3. Target customers with LTV > $500 for upsells
4. Cross-sell to single-stream customers
"""
        
        return report


def main():
    """Demo of customer retention engine"""
    print("💰 CUSTOMER RETENTION ENGINE")
    print("="*60)
    print()
    
    engine = CustomerRetentionEngine()
    
    # Example: Add a customer
    customer = Customer(
        id="cust_001",
        email="example@email.com",
        name="John Doe",
        first_purchase_date=datetime.now() - timedelta(days=60),
        last_interaction_date=datetime.now() - timedelta(days=45),
        total_spent=250.0,
        purchase_count=3,
        revenue_streams=["music", "art"],
        preferences={"genres": ["cinematic", "ambient"], "styles": ["dark", "moody"]}
    )
    
    engine.add_customer(customer)
    
    # Record interactions
    engine.record_interaction("cust_001", "purchase", "music", 99.0)
    engine.record_interaction("cust_001", "email_open", "art", 0.0)
    
    # Calculate metrics
    churn_risk = engine.calculate_churn_risk("cust_001")
    ltv = engine.calculate_lifetime_value("cust_001")
    
    print(f"Customer: {customer.name}")
    print(f"Churn Risk: {churn_risk:.1%}")
    print(f"Lifetime Value: ${ltv:.2f}")
    print()
    
    # Identify retention actions
    actions = engine.identify_retention_actions("cust_001")
    print(f"Identified {len(actions)} retention actions:")
    for action in actions:
        print(f"  - {action.action_type} (Priority: {action.priority}, ROI: ${action.estimated_roi:.2f})")
    print()
    
    # Generate report
    report = engine.generate_retention_report()
    print(report)


if __name__ == '__main__':
    main()

