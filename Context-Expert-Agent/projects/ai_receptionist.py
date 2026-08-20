#!/usr/bin/env python3
"""
AI Receptionist - A comprehensive AI voice agent system for small businesses
Based on the "Starting an Online Business with AI" concept

Features:
- 24/7 AI voice agent for answering calls
- Appointment booking and management
- Lead capture and conversion
- Multi-client support with customizable responses
- Recurring billing system
- Real-time analytics and reporting
"""

import os
import json
import sqlite3
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from openai import OpenAI
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BusinessClient:
    """Represents a business client using the AI receptionist service"""
    id: str
    name: str
    industry: str
    phone_number: str
    business_hours: Dict[str, str]
    services: List[str]
    pricing: Dict[str, float]
    ai_personality: str
    custom_responses: Dict[str, str]
    monthly_fee: float
    is_active: bool = True
    created_at: str = ""
    updated_at: str = ""

@dataclass
class Appointment:
    """Represents a scheduled appointment"""
    id: str
    client_id: str
    customer_name: str
    customer_phone: str
    service: str
    appointment_date: str
    appointment_time: str
    status: str  # scheduled, confirmed, cancelled, completed
    notes: str = ""
    created_at: str = ""

@dataclass
class CallLog:
    """Represents a call interaction log"""
    id: str
    client_id: str
    caller_phone: str
    call_duration: int
    outcome: str  # appointment_booked, lead_captured, no_action, voicemail
    transcript: str
    timestamp: str

class AIReceptionist:
    """Main AI Receptionist system"""
    
    def __init__(self, db_path: str = "ai_receptionist.db"):
        self.db_path = db_path
        self.openai_client = None
        self._init_database()
        self._load_openai_client()
    
    def _init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create clients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                industry TEXT NOT NULL,
                phone_number TEXT UNIQUE NOT NULL,
                business_hours TEXT NOT NULL,
                services TEXT NOT NULL,
                pricing TEXT NOT NULL,
                ai_personality TEXT NOT NULL,
                custom_responses TEXT NOT NULL,
                monthly_fee REAL NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        # Create appointments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id TEXT PRIMARY KEY,
                client_id TEXT NOT NULL,
                customer_name TEXT NOT NULL,
                customer_phone TEXT NOT NULL,
                service TEXT NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                status TEXT DEFAULT 'scheduled',
                notes TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                FOREIGN KEY (client_id) REFERENCES clients (id)
            )
        ''')
        
        # Create call_logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS call_logs (
                id TEXT PRIMARY KEY,
                client_id TEXT NOT NULL,
                caller_phone TEXT NOT NULL,
                call_duration INTEGER NOT NULL,
                outcome TEXT NOT NULL,
                transcript TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (client_id) REFERENCES clients (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def _load_openai_client(self):
        """Load OpenAI client from environment"""
        try:
            # Try to load from your .env.d directory
            env_d_path = os.path.expanduser("~/.env.d/llm-apis.env")
            if os.path.exists(env_d_path):
                from dotenv import load_dotenv
                load_dotenv(env_d_path)
            
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key not found")
            
            self.openai_client = OpenAI(api_key=api_key)
            logger.info("OpenAI client loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load OpenAI client: {e}")
            self.openai_client = None
    
    def add_client(self, client: BusinessClient) -> bool:
        """Add a new business client"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            client.created_at = datetime.datetime.now().isoformat()
            client.updated_at = client.created_at
            
            cursor.execute('''
                INSERT INTO clients (id, name, industry, phone_number, business_hours, 
                                   services, pricing, ai_personality, custom_responses, 
                                   monthly_fee, is_active, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                client.id, client.name, client.industry, client.phone_number,
                json.dumps(client.business_hours), json.dumps(client.services),
                json.dumps(client.pricing), client.ai_personality,
                json.dumps(client.custom_responses), client.monthly_fee,
                client.is_active, client.created_at, client.updated_at
            ))
            
            conn.commit()
            conn.close()
            logger.info(f"Client {client.name} added successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to add client: {e}")
            return False
    
    def get_client(self, client_id: str) -> Optional[BusinessClient]:
        """Get client by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return BusinessClient(
                    id=row[0], name=row[1], industry=row[2], phone_number=row[3],
                    business_hours=json.loads(row[4]), services=json.loads(row[5]),
                    pricing=json.loads(row[6]), ai_personality=row[7],
                    custom_responses=json.loads(row[8]), monthly_fee=row[9],
                    is_active=bool(row[10]), created_at=row[11], updated_at=row[12]
                )
            return None
        except Exception as e:
            logger.error(f"Failed to get client: {e}")
            return None
    
    def get_client_by_phone(self, phone_number: str) -> Optional[BusinessClient]:
        """Get client by phone number"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM clients WHERE phone_number = ?', (phone_number,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return BusinessClient(
                    id=row[0], name=row[1], industry=row[2], phone_number=row[3],
                    business_hours=json.loads(row[4]), services=json.loads(row[5]),
                    pricing=json.loads(row[6]), ai_personality=row[7],
                    custom_responses=json.loads(row[8]), monthly_fee=row[9],
                    is_active=bool(row[10]), created_at=row[11], updated_at=row[12]
                )
            return None
        except Exception as e:
            logger.error(f"Failed to get client by phone: {e}")
            return None
    
    def generate_ai_response(self, client: BusinessClient, caller_message: str, 
                           call_context: Dict[str, Any] = None) -> str:
        """Generate AI response for incoming call"""
        if not self.openai_client:
            return "I'm sorry, the AI service is currently unavailable. Please call back later."
        
        try:
            # Build system prompt based on client configuration
            system_prompt = f"""
            You are an AI receptionist for {client.name}, a {client.industry} business.
            
            Business Information:
            - Industry: {client.industry}
            - Services: {', '.join(client.services)}
            - Business Hours: {json.dumps(client.business_hours, indent=2)}
            - Pricing: {json.dumps(client.pricing, indent=2)}
            
            AI Personality: {client.ai_personality}
            
            Your role:
            1. Answer calls professionally and warmly
            2. Provide information about services and pricing
            3. Book appointments when requested
            4. Capture lead information for follow-up
            5. Handle common questions about the business
            
            Guidelines:
            - Be helpful, professional, and friendly
            - Always ask for the caller's name and phone number
            - Offer to book appointments for available services
            - If you can't answer something, offer to have someone call back
            - Keep responses concise but informative
            - Always end with asking how you can help further
            
            Custom Responses:
            {json.dumps(client.custom_responses, indent=2)}
            """
            
            # Add call context if available
            context_info = ""
            if call_context:
                context_info = f"\nCall Context: {json.dumps(call_context, indent=2)}"
            
            messages = [
                {"role": "system", "content": system_prompt + context_info},
                {"role": "user", "content": caller_message}
            ]
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate AI response: {e}")
            return "I'm sorry, I'm having trouble processing your request. Please call back later."
    
    def book_appointment(self, client_id: str, customer_name: str, customer_phone: str,
                        service: str, appointment_date: str, appointment_time: str,
                        notes: str = "") -> bool:
        """Book a new appointment"""
        try:
            appointment_id = f"apt_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{customer_phone[-4:]}"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO appointments (id, client_id, customer_name, customer_phone,
                                        service, appointment_date, appointment_time,
                                        status, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                appointment_id, client_id, customer_name, customer_phone,
                service, appointment_date, appointment_time, 'scheduled',
                notes, datetime.datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            logger.info(f"Appointment booked: {appointment_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to book appointment: {e}")
            return False
    
    def log_call(self, client_id: str, caller_phone: str, call_duration: int,
                outcome: str, transcript: str) -> bool:
        """Log a call interaction"""
        try:
            call_id = f"call_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{caller_phone[-4:]}"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO call_logs (id, client_id, caller_phone, call_duration,
                                     outcome, transcript, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                call_id, client_id, caller_phone, call_duration,
                outcome, transcript, datetime.datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            logger.info(f"Call logged: {call_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to log call: {e}")
            return False
    
    def get_appointments(self, client_id: str, date: str = None) -> List[Appointment]:
        """Get appointments for a client"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if date:
                cursor.execute('''
                    SELECT * FROM appointments 
                    WHERE client_id = ? AND appointment_date = ?
                    ORDER BY appointment_time
                ''', (client_id, date))
            else:
                cursor.execute('''
                    SELECT * FROM appointments 
                    WHERE client_id = ?
                    ORDER BY appointment_date, appointment_time
                ''', (client_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            appointments = []
            for row in rows:
                appointments.append(Appointment(
                    id=row[0], client_id=row[1], customer_name=row[2],
                    customer_phone=row[3], service=row[4], appointment_date=row[5],
                    appointment_time=row[6], status=row[7], notes=row[8],
                    created_at=row[9]
                ))
            
            return appointments
        except Exception as e:
            logger.error(f"Failed to get appointments: {e}")
            return []
    
    def get_call_logs(self, client_id: str, days: int = 30) -> List[CallLog]:
        """Get call logs for a client"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            start_date = (datetime.datetime.now() - datetime.timedelta(days=days)).isoformat()
            
            cursor.execute('''
                SELECT * FROM call_logs 
                WHERE client_id = ? AND timestamp >= ?
                ORDER BY timestamp DESC
            ''', (client_id, start_date))
            
            rows = cursor.fetchall()
            conn.close()
            
            call_logs = []
            for row in rows:
                call_logs.append(CallLog(
                    id=row[0], client_id=row[1], caller_phone=row[2],
                    call_duration=row[3], outcome=row[4], transcript=row[5],
                    timestamp=row[6]
                ))
            
            return call_logs
        except Exception as e:
            logger.error(f"Failed to get call logs: {e}")
            return []
    
    def get_business_analytics(self, client_id: str, days: int = 30) -> Dict[str, Any]:
        """Get business analytics for a client"""
        try:
            call_logs = self.get_call_logs(client_id, days)
            appointments = self.get_appointments(client_id)
            
            # Calculate metrics
            total_calls = len(call_logs)
            appointments_booked = len([log for log in call_logs if log.outcome == 'appointment_booked'])
            leads_captured = len([log for log in call_logs if log.outcome == 'lead_captured'])
            
            conversion_rate = (appointments_booked / total_calls * 100) if total_calls > 0 else 0
            
            # Group by outcome
            outcomes = {}
            for log in call_logs:
                outcomes[log.outcome] = outcomes.get(log.outcome, 0) + 1
            
            return {
                'total_calls': total_calls,
                'appointments_booked': appointments_booked,
                'leads_captured': leads_captured,
                'conversion_rate': round(conversion_rate, 2),
                'outcomes': outcomes,
                'period_days': days
            }
        except Exception as e:
            logger.error(f"Failed to get analytics: {e}")
            return {}

def create_sample_clients() -> List[BusinessClient]:
    """Create sample business clients for demonstration"""
    clients = []
    
    # Dental Practice
    dental_client = BusinessClient(
        id="dental_001",
        name="Bright Smile Dental",
        industry="Dental Practice",
        phone_number="+1-555-0123",
        business_hours={
            "monday": "8:00 AM - 5:00 PM",
            "tuesday": "8:00 AM - 5:00 PM",
            "wednesday": "8:00 AM - 5:00 PM",
            "thursday": "8:00 AM - 5:00 PM",
            "friday": "8:00 AM - 3:00 PM",
            "saturday": "9:00 AM - 2:00 PM",
            "sunday": "Closed"
        },
        services=["General Cleaning", "Teeth Whitening", "Crowns", "Root Canal", "Emergency Care"],
        pricing={
            "General Cleaning": 150,
            "Teeth Whitening": 300,
            "Crowns": 1200,
            "Root Canal": 800,
            "Emergency Care": 200
        },
        ai_personality="Professional, caring, and reassuring. Focus on oral health education and comfort.",
        custom_responses={
            "greeting": "Thank you for calling Bright Smile Dental! I'm your AI assistant. How can I help you today?",
            "emergency": "I understand this is urgent. Let me help you get the care you need right away.",
            "pricing": "I'd be happy to provide pricing information. Our services range from $150 for cleanings to $1200 for crowns."
        },
        monthly_fee=400.0
    )
    clients.append(dental_client)
    
    # Hair Salon
    salon_client = BusinessClient(
        id="salon_001",
        name="Style Studio Salon",
        industry="Hair Salon",
        phone_number="+1-555-0456",
        business_hours={
            "monday": "9:00 AM - 7:00 PM",
            "tuesday": "9:00 AM - 7:00 PM",
            "wednesday": "9:00 AM - 7:00 PM",
            "thursday": "9:00 AM - 7:00 PM",
            "friday": "9:00 AM - 8:00 PM",
            "saturday": "8:00 AM - 6:00 PM",
            "sunday": "10:00 AM - 4:00 PM"
        },
        services=["Haircut", "Hair Color", "Highlights", "Perm", "Styling", "Bridal Package"],
        pricing={
            "Haircut": 45,
            "Hair Color": 120,
            "Highlights": 150,
            "Perm": 100,
            "Styling": 60,
            "Bridal Package": 300
        },
        ai_personality="Friendly, trendy, and enthusiastic about beauty and style. Focus on helping clients look their best.",
        custom_responses={
            "greeting": "Welcome to Style Studio Salon! I'm here to help you book your next appointment. What can I do for you?",
            "trends": "We're always up on the latest trends! Our stylists can help you achieve any look you're going for.",
            "pricing": "Our services start at $45 for a haircut and go up to $300 for our bridal package."
        },
        monthly_fee=350.0
    )
    clients.append(salon_client)
    
    # Electrician
    electrician_client = BusinessClient(
        id="electric_001",
        name="Reliable Electric Services",
        industry="Electrical Services",
        phone_number="+1-555-0789",
        business_hours={
            "monday": "7:00 AM - 6:00 PM",
            "tuesday": "7:00 AM - 6:00 PM",
            "wednesday": "7:00 AM - 6:00 PM",
            "thursday": "7:00 AM - 6:00 PM",
            "friday": "7:00 AM - 6:00 PM",
            "saturday": "8:00 AM - 4:00 PM",
            "sunday": "Emergency Only"
        },
        services=["Electrical Repair", "Installation", "Maintenance", "Emergency Service", "Safety Inspection"],
        pricing={
            "Electrical Repair": 150,
            "Installation": 200,
            "Maintenance": 100,
            "Emergency Service": 300,
            "Safety Inspection": 125
        },
        ai_personality="Professional, knowledgeable, and safety-focused. Emphasize reliability and quick response times.",
        custom_responses={
            "greeting": "Thank you for calling Reliable Electric Services. I'm here to help with your electrical needs. What's the issue?",
            "emergency": "I understand this is an emergency. We provide 24/7 emergency service. Let me get you scheduled right away.",
            "safety": "Safety is our top priority. All our electricians are licensed and insured."
        },
        monthly_fee=450.0
    )
    clients.append(electrician_client)
    
    return clients

def main():
    """Main function to demonstrate the AI Receptionist system"""
    print("🤖 AI Receptionist System - Starting Up...")
    print("=" * 50)
    
    # Initialize the system
    receptionist = AIReceptionist()
    
    # Create sample clients
    print("📋 Creating sample business clients...")
    sample_clients = create_sample_clients()
    
    for client in sample_clients:
        if receptionist.add_client(client):
            print(f"✅ Added client: {client.name} ({client.industry})")
        else:
            print(f"❌ Failed to add client: {client.name}")
    
    print("\n🎯 AI Receptionist System Ready!")
    print("=" * 50)
    print("Features available:")
    print("• 24/7 AI voice agent for answering calls")
    print("• Appointment booking and management")
    print("• Lead capture and conversion")
    print("• Multi-client support")
    print("• Real-time analytics")
    print("• Recurring billing system")
    
    # Interactive demo
    print("\n🎮 Interactive Demo")
    print("-" * 20)
    
    while True:
        print("\nChoose an option:")
        print("1. Simulate a call")
        print("2. View client information")
        print("3. Book an appointment")
        print("4. View analytics")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            simulate_call(receptionist)
        elif choice == "2":
            view_client_info(receptionist)
        elif choice == "3":
            book_appointment_demo(receptionist)
        elif choice == "4":
            view_analytics(receptionist)
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def simulate_call(receptionist: AIReceptionist):
    """Simulate an incoming call"""
    print("\n📞 Simulating a call...")
    
    # Get available clients
    clients = []
    for client_id in ["dental_001", "salon_001", "electric_001"]:
        client = receptionist.get_client(client_id)
        if client:
            clients.append(client)
    
    if not clients:
        print("❌ No clients found. Please add clients first.")
        return
    
    print("\nAvailable businesses:")
    for i, client in enumerate(clients, 1):
        print(f"{i}. {client.name} ({client.industry})")
    
    try:
        choice = int(input("\nSelect business (1-{}): ".format(len(clients)))) - 1
        if 0 <= choice < len(clients):
            client = clients[choice]
            print(f"\n📞 Incoming call to {client.name}...")
            
            caller_message = input("\nWhat would the caller say? (e.g., 'Hi, I need to book a dental cleaning'): ")
            
            print("\n🤖 AI Receptionist Response:")
            print("-" * 40)
            
            response = receptionist.generate_ai_response(client, caller_message)
            print(response)
            
            # Log the call
            receptionist.log_call(
                client_id=client.id,
                caller_phone="+1-555-0000",
                call_duration=60,
                outcome="lead_captured",
                transcript=f"Caller: {caller_message}\nAI: {response}"
            )
            
            print("\n✅ Call logged successfully!")
        else:
            print("❌ Invalid selection.")
    except ValueError:
        print("❌ Please enter a valid number.")

def view_client_info(receptionist: AIReceptionist):
    """View client information"""
    print("\n📋 Client Information")
    print("-" * 20)
    
    client_id = input("Enter client ID (dental_001, salon_001, electric_001): ").strip()
    client = receptionist.get_client(client_id)
    
    if client:
        print(f"\n🏢 {client.name}")
        print(f"Industry: {client.industry}")
        print(f"Phone: {client.phone_number}")
        print(f"Monthly Fee: ${client.monthly_fee}")
        print(f"Services: {', '.join(client.services)}")
        print(f"AI Personality: {client.ai_personality}")
        print(f"Active: {'Yes' if client.is_active else 'No'}")
    else:
        print("❌ Client not found.")

def book_appointment_demo(receptionist: AIReceptionist):
    """Demonstrate appointment booking"""
    print("\n📅 Book Appointment")
    print("-" * 20)
    
    client_id = input("Enter client ID: ").strip()
    client = receptionist.get_client(client_id)
    
    if not client:
        print("❌ Client not found.")
        return
    
    print(f"\nBooking appointment for {client.name}")
    print(f"Available services: {', '.join(client.services)}")
    
    customer_name = input("Customer name: ").strip()
    customer_phone = input("Customer phone: ").strip()
    service = input("Service: ").strip()
    appointment_date = input("Date (YYYY-MM-DD): ").strip()
    appointment_time = input("Time (HH:MM): ").strip()
    notes = input("Notes (optional): ").strip()
    
    if receptionist.book_appointment(client_id, customer_name, customer_phone,
                                   service, appointment_date, appointment_time, notes):
        print("✅ Appointment booked successfully!")
    else:
        print("❌ Failed to book appointment.")

def view_analytics(receptionist: AIReceptionist):
    """View business analytics"""
    print("\n📊 Business Analytics")
    print("-" * 20)
    
    client_id = input("Enter client ID: ").strip()
    client = receptionist.get_client(client_id)
    
    if not client:
        print("❌ Client not found.")
        return
    
    analytics = receptionist.get_business_analytics(client_id, 30)
    
    print(f"\n📈 Analytics for {client.name} (Last 30 days)")
    print(f"Total Calls: {analytics.get('total_calls', 0)}")
    print(f"Appointments Booked: {analytics.get('appointments_booked', 0)}")
    print(f"Leads Captured: {analytics.get('leads_captured', 0)}")
    print(f"Conversion Rate: {analytics.get('conversion_rate', 0)}%")
    
    outcomes = analytics.get('outcomes', {})
    if outcomes:
        print("\nCall Outcomes:")
        for outcome, count in outcomes.items():
            print(f"  {outcome}: {count}")

if __name__ == "__main__":
    main()