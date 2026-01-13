#!/usr/bin/env python3
"""
CRM System - Client Relationship Management
Manages client relationships, projects, and communications
"""

import os
import json
import sqlite3
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Client:
    """Client data structure"""
    id: str
    name: str
    email: str
    company: str
    phone: str
    industry: str
    budget_range: str
    status: str  # lead, prospect, client, inactive
    source: str
    created_at: str
    last_contact: str
    notes: str
    tags: List[str]

@dataclass
class Project:
    """Project data structure"""
    id: str
    client_id: str
    name: str
    description: str
    service_type: str
    status: str  # planning, active, review, completed, cancelled
    priority: str  # low, medium, high, urgent
    budget: float
    start_date: str
    due_date: str
    team_members: List[str]
    deliverables: List[str]
    progress: int  # 0-100
    created_at: str
    updated_at: str

@dataclass
class Communication:
    """Communication record"""
    id: str
    client_id: str
    project_id: Optional[str]
    type: str  # email, call, meeting, message
    subject: str
    content: str
    direction: str  # inbound, outbound
    timestamp: str
    status: str  # sent, delivered, read, replied

class CRMSystem:
    """Client Relationship Management System"""
    
    def __init__(self, db_path: str = "databases/agency.db"):
        self.db_path = db_path
        self._init_database()
        
    def _init_database(self):
        """Initialize CRM database"""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Clients table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    company TEXT,
                    phone TEXT,
                    industry TEXT,
                    budget_range TEXT,
                    status TEXT DEFAULT 'lead',
                    source TEXT,
                    created_at TEXT,
                    last_contact TEXT,
                    notes TEXT,
                    tags TEXT
                )
            ''')
            
            # Projects table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id TEXT PRIMARY KEY,
                    client_id TEXT,
                    name TEXT NOT NULL,
                    description TEXT,
                    service_type TEXT,
                    status TEXT DEFAULT 'planning',
                    priority TEXT DEFAULT 'medium',
                    budget REAL,
                    start_date TEXT,
                    due_date TEXT,
                    team_members TEXT,
                    deliverables TEXT,
                    progress INTEGER DEFAULT 0,
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY (client_id) REFERENCES clients (id)
                )
            ''')
            
            # Communications table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS communications (
                    id TEXT PRIMARY KEY,
                    client_id TEXT,
                    project_id TEXT,
                    type TEXT,
                    subject TEXT,
                    content TEXT,
                    direction TEXT,
                    timestamp TEXT,
                    status TEXT,
                    FOREIGN KEY (client_id) REFERENCES clients (id),
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("CRM database initialized")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    def add_client(self, client_data: Dict[str, Any]) -> str:
        """Add new client to CRM"""
        try:
            client_id = f"client_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            client = Client(
                id=client_id,
                name=client_data["name"],
                email=client_data["email"],
                company=client_data.get("company", ""),
                phone=client_data.get("phone", ""),
                industry=client_data.get("industry", ""),
                budget_range=client_data.get("budget_range", ""),
                status=client_data.get("status", "lead"),
                source=client_data.get("source", "direct"),
                created_at=datetime.now().isoformat(),
                last_contact=datetime.now().isoformat(),
                notes=client_data.get("notes", ""),
                tags=client_data.get("tags", [])
            )
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO clients 
                (id, name, email, company, phone, industry, budget_range, 
                 status, source, created_at, last_contact, notes, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                client.id, client.name, client.email, client.company,
                client.phone, client.industry, client.budget_range,
                client.status, client.source, client.created_at,
                client.last_contact, client.notes, json.dumps(client.tags)
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Client {client.name} added to CRM")
            return client_id
            
        except Exception as e:
            logger.error(f"Failed to add client: {e}")
            return None
    
    def create_project(self, project_data: Dict[str, Any]) -> str:
        """Create new project"""
        try:
            project_id = f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            project = Project(
                id=project_id,
                client_id=project_data["client_id"],
                name=project_data["name"],
                description=project_data["description"],
                service_type=project_data["service_type"],
                status=project_data.get("status", "planning"),
                priority=project_data.get("priority", "medium"),
                budget=project_data.get("budget", 0.0),
                start_date=project_data.get("start_date", datetime.now().isoformat()),
                due_date=project_data.get("due_date", ""),
                team_members=project_data.get("team_members", []),
                deliverables=project_data.get("deliverables", []),
                progress=0,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO projects 
                (id, client_id, name, description, service_type, status, priority,
                 budget, start_date, due_date, team_members, deliverables,
                 progress, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                project.id, project.client_id, project.name, project.description,
                project.service_type, project.status, project.priority,
                project.budget, project.start_date, project.due_date,
                json.dumps(project.team_members), json.dumps(project.deliverables),
                project.progress, project.created_at, project.updated_at
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Project {project.name} created")
            return project_id
            
        except Exception as e:
            logger.error(f"Failed to create project: {e}")
            return None
    
    def log_communication(self, communication_data: Dict[str, Any]) -> str:
        """Log communication with client"""
        try:
            comm_id = f"comm_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            communication = Communication(
                id=comm_id,
                client_id=communication_data["client_id"],
                project_id=communication_data.get("project_id"),
                type=communication_data["type"],
                subject=communication_data["subject"],
                content=communication_data["content"],
                direction=communication_data["direction"],
                timestamp=datetime.now().isoformat(),
                status=communication_data.get("status", "sent")
            )
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO communications 
                (id, client_id, project_id, type, subject, content, 
                 direction, timestamp, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                communication.id, communication.client_id, communication.project_id,
                communication.type, communication.subject, communication.content,
                communication.direction, communication.timestamp, communication.status
            ))
            
            # Update client last contact
            cursor.execute('''
                UPDATE clients 
                SET last_contact = ? 
                WHERE id = ?
            ''', (communication.timestamp, communication.client_id))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Communication logged for client {communication.client_id}")
            return comm_id
            
        except Exception as e:
            logger.error(f"Failed to log communication: {e}")
            return None
    
    def get_client(self, client_id: str) -> Optional[Client]:
        """Get client by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
            row = cursor.fetchone()
            
            if row:
                client = Client(
                    id=row[0],
                    name=row[1],
                    email=row[2],
                    company=row[3],
                    phone=row[4],
                    industry=row[5],
                    budget_range=row[6],
                    status=row[7],
                    source=row[8],
                    created_at=row[9],
                    last_contact=row[10],
                    notes=row[11],
                    tags=json.loads(row[12]) if row[12] else []
                )
                conn.close()
                return client
            
            conn.close()
            return None
            
        except Exception as e:
            logger.error(f"Failed to get client: {e}")
            return None
    
    def get_client_projects(self, client_id: str) -> List[Project]:
        """Get all projects for a client"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM projects 
                WHERE client_id = ? 
                ORDER BY created_at DESC
            ''', (client_id,))
            
            projects = []
            for row in cursor.fetchall():
                project = Project(
                    id=row[0],
                    client_id=row[1],
                    name=row[2],
                    description=row[3],
                    service_type=row[4],
                    status=row[5],
                    priority=row[6],
                    budget=row[7],
                    start_date=row[8],
                    due_date=row[9],
                    team_members=json.loads(row[10]) if row[10] else [],
                    deliverables=json.loads(row[11]) if row[11] else [],
                    progress=row[12],
                    created_at=row[13],
                    updated_at=row[14]
                )
                projects.append(project)
            
            conn.close()
            return projects
            
        except Exception as e:
            logger.error(f"Failed to get client projects: {e}")
            return []
    
    def update_project_progress(self, project_id: str, progress: int) -> bool:
        """Update project progress"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE projects 
                SET progress = ?, updated_at = ? 
                WHERE id = ?
            ''', (progress, datetime.now().isoformat(), project_id))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Project {project_id} progress updated to {progress}%")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update project progress: {e}")
            return False
    
    def get_client_dashboard_data(self, client_id: str) -> Dict[str, Any]:
        """Get dashboard data for client"""
        try:
            client = self.get_client(client_id)
            if not client:
                return {}
            
            projects = self.get_client_projects(client_id)
            
            # Calculate project statistics
            total_projects = len(projects)
            active_projects = len([p for p in projects if p.status == "active"])
            completed_projects = len([p for p in projects if p.status == "completed"])
            total_budget = sum(p.budget for p in projects)
            
            # Get recent communications
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM communications 
                WHERE client_id = ? 
                ORDER BY timestamp DESC 
                LIMIT 10
            ''', (client_id,))
            
            recent_communications = []
            for row in cursor.fetchall():
                recent_communications.append({
                    "id": row[0],
                    "type": row[3],
                    "subject": row[4],
                    "direction": row[6],
                    "timestamp": row[7],
                    "status": row[8]
                })
            
            conn.close()
            
            return {
                "client": client.__dict__,
                "projects": [p.__dict__ for p in projects],
                "statistics": {
                    "total_projects": total_projects,
                    "active_projects": active_projects,
                    "completed_projects": completed_projects,
                    "total_budget": total_budget
                },
                "recent_communications": recent_communications
            }
            
        except Exception as e:
            logger.error(f"Failed to get dashboard data: {e}")
            return {}
    
    def generate_client_report(self, client_id: str, period: str = "monthly") -> str:
        """Generate client report"""
        try:
            dashboard_data = self.get_client_dashboard_data(client_id)
            if not dashboard_data:
                return "Client not found"
            
            client = dashboard_data["client"]
            projects = dashboard_data["projects"]
            stats = dashboard_data["statistics"]
            
            report = f"""
# Client Report - {client['name']}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Period: {period.title()}

## Client Information
- **Company**: {client['company']}
- **Industry**: {client['industry']}
- **Status**: {client['status'].title()}
- **Budget Range**: {client['budget_range']}

## Project Statistics
- **Total Projects**: {stats['total_projects']}
- **Active Projects**: {stats['active_projects']}
- **Completed Projects**: {stats['completed_projects']}
- **Total Budget**: ${stats['total_budget']:,.2f}

## Recent Projects
"""
            
            for project in projects[:5]:  # Show last 5 projects
                report += f"""
### {project['name']}
- **Status**: {project['status'].title()}
- **Progress**: {project['progress']}%
- **Budget**: ${project['budget']:,.2f}
- **Due Date**: {project['due_date']}
"""
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate client report: {e}")
            return f"Error generating report: {e}"

# Example usage
def main():
    """Example usage of CRM System"""
    crm = CRMSystem()
    
    # Add a client
    client_data = {
        "name": "Tech Startup Inc",
        "email": "contact@techstartup.com",
        "company": "Tech Startup Inc",
        "phone": "+1-555-0123",
        "industry": "Technology",
        "budget_range": "$10K-50K",
        "status": "prospect",
        "source": "referral",
        "notes": "Interested in AI content creation",
        "tags": ["tech", "startup", "ai"]
    }
    
    client_id = crm.add_client(client_data)
    if client_id:
        print(f"Client added: {client_id}")
        
        # Create a project
        project_data = {
            "client_id": client_id,
            "name": "AI Content Creation Campaign",
            "description": "Create AI-generated content for marketing campaign",
            "service_type": "Content Creation",
            "budget": 15000.0,
            "due_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "team_members": ["AI Content Creator", "Project Manager"],
            "deliverables": ["Blog posts", "Social media content", "Video scripts"]
        }
        
        project_id = crm.create_project(project_data)
        if project_id:
            print(f"Project created: {project_id}")
            
            # Generate client report
            report = crm.generate_client_report(client_id)
            print("\nClient Report:")
            print(report)

if __name__ == "__main__":
    main()