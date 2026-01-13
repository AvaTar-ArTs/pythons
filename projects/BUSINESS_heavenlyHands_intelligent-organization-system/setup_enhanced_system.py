#!/usr/bin/env python3
"""
Enhanced Creative Automation System Setup
=========================================

Setup script for the enhanced Intelligent Organization System with:
- Twilio phone automation
- Enhanced semantic search
- Creative automation workflows
- Agentic AI workflows

Author: AI Assistant
Date: 2025-10-26
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def install_requirements():
    """Install enhanced requirements"""
    requirements = [
        "twilio>=8.0.0",
        "openai>=1.0.0",
        "aiohttp>=3.8.0",
        "asyncio",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
        "requests>=2.28.0",
        "sqlite3",
        "nltk>=3.8",
        "scikit-learn>=1.3.0",
        "faiss-cpu>=1.7.4",
        "selenium>=4.15.0"
    ]
    
    print("📦 Installing enhanced requirements...")
    
    for req in requirements:
        try:
            print(f"Installing {req}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
            print(f"✅ {req} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {req}: {e}")
            if req in ["twilio", "openai", "aiohttp"]:
                print(f"⚠️  {req} is required for enhanced functionality")
            else:
                print(f"⚠️  {req} is optional, continuing...")

def create_enhanced_env():
    """Create enhanced environment configuration"""
    env_content = """# Enhanced Creative Automation System Environment Variables
# ================================================================

# OpenAI API Configuration
OPENAI_API_KEY=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
OPENAI_MODEL=gpt-4o

# Twilio Configuration (Add your credentials)
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number_here

# System Configuration
SYSTEM_NAME=Enhanced Creative Automation System
SYSTEM_VERSION=2.1.0
DEBUG_MODE=true
LOG_LEVEL=INFO

# Database Configuration
DATABASE_PATH=./intelligent_org.db
AUTOMATION_DB_PATH=./creative_automation.db
AGENTIC_DB_PATH=./agentic_workflows_enhanced.db
VECTOR_DB_PATH=./enhanced_vector_search.db

# Vector Search Configuration
VECTOR_DB_TYPE=enhanced
SIMILARITY_THRESHOLD=0.3
EMBEDDING_MODEL=enhanced_semantic

# Creative Automation Configuration
MAX_CONCURRENT_TASKS=10
TASK_TIMEOUT=600
RETRY_ATTEMPTS=3
PHONE_CALL_TIMEOUT=30

# Heavenly Hands Project Configuration
HEAVENLY_HANDS_PATH=/Users/steven/ai-sites/heavenlyHands-advanced
TARGET_PAGE_LOAD_TIME=2.0
TARGET_SEO_SCORE=90
TARGET_CONVERSION_RATE=0.05
TARGET_MOBILE_SCORE=95

# Social Media Integration (Optional)
FACEBOOK_ACCESS_TOKEN=your_facebook_token_here
INSTAGRAM_ACCESS_TOKEN=your_instagram_token_here
TWITTER_API_KEY=your_twitter_api_key_here

# Email Integration (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here

# Analytics Configuration
GOOGLE_ANALYTICS_ID=your_ga_id_here
FACEBOOK_PIXEL_ID=your_pixel_id_here
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Enhanced .env file created")
    print("⚠️  Please update Twilio credentials in .env file")

def create_heavenly_hands_phone_scripts():
    """Create Heavenly Hands specific phone automation scripts"""
    
    # TwiML webhook handler
    twiml_handler = '''from flask import Flask, request
from twilio.twiml import VoiceResponse
import json

app = Flask(__name__)

@app.route('/handle_gather', methods=['POST'])
def handle_gather():
    """Handle phone keypad input"""
    response = VoiceResponse()
    digits = request.form.get('Digits', '')
    
    if digits == '1':
        response.say("Great! For residential cleaning, we offer weekly, bi-weekly, or monthly services. Our rates start at $120 for a 3-bedroom home.")
        response.say("Press 1 to schedule a free consultation, or 2 to speak with our team.")
    elif digits == '2':
        response.say("For commercial cleaning, we provide customized solutions for offices, retail spaces, and more. Our commercial rates are competitive and flexible.")
        response.say("Press 1 to schedule a free consultation, or 2 to speak with our team.")
    elif digits == '3':
        response.say("Move-in and move-out cleaning is our specialty! We ensure your new home is spotless or help you get your deposit back.")
        response.say("Press 1 to schedule a free consultation, or 2 to speak with our team.")
    elif digits == '4':
        response.say("Connecting you to our team now. Please hold while we transfer your call.")
        response.dial("+1234567890")  # Replace with actual number
    else:
        response.say("I didn't understand your selection. Please call us back at your convenience.")
    
    response.hangup()
    return str(response)

@app.route('/handle_lead_gather', methods=['POST'])
def handle_lead_gather():
    """Handle lead generation call input"""
    response = VoiceResponse()
    digits = request.form.get('Digits', '')
    
    if digits == '1':
        response.say("Perfect! We'll schedule your free consultation. Our team will call you within 24 hours to set up a convenient time.")
        response.say("Thank you for choosing Heavenly Hands Cleaning Service!")
    elif digits == '2':
        response.say("Our residential cleaning starts at $120 for a 3-bedroom home. Commercial rates vary based on size and frequency.")
        response.say("Press 1 to schedule a free consultation for a personalized quote.")
    elif digits == '3':
        response.say("Connecting you to our team now. Please hold while we transfer your call.")
        response.dial("+1234567890")  # Replace with actual number
    elif digits == '0':
        response.say("We'll remove you from our call list. Thank you for your time.")
    else:
        response.say("I didn't understand your selection. Please call us back at your convenience.")
    
    response.hangup()
    return str(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
'''
    
    with open('heavenly_hands_webhook.py', 'w') as f:
        f.write(twiml_handler)
    
    # Lead generation script
    lead_script = '''#!/usr/bin/env python3
"""
Heavenly Hands Lead Generation Script
=====================================

Automated lead generation and phone outreach for Heavenly Hands Cleaning Service
"""

import os
import json
from enhanced_creative_automation import EnhancedIntelligentOrganizationSystem
from dotenv import load_dotenv

load_dotenv()

def main():
    """Main lead generation function"""
    print("🏠 Heavenly Hands Lead Generation System")
    print("=" * 50)
    
    # Initialize enhanced system
    system = EnhancedIntelligentOrganizationSystem()
    
    # Sample lead data (in production, this would come from CRM, website forms, etc.)
    leads = [
        {
            'name': 'John Smith',
            'phone': '+1234567890',
            'email': 'john@example.com',
            'service_interest': 'residential cleaning',
            'source': 'website_form',
            'notes': 'Interested in weekly cleaning for 3-bedroom home'
        },
        {
            'name': 'Sarah Johnson',
            'phone': '+1234567891',
            'email': 'sarah@example.com',
            'service_interest': 'commercial cleaning',
            'source': 'google_ads',
            'notes': 'Office building, 5000 sq ft, needs daily cleaning'
        },
        {
            'name': 'Mike Davis',
            'phone': '+1234567892',
            'email': 'mike@example.com',
            'service_interest': 'move-in cleaning',
            'source': 'referral',
            'notes': 'Moving into new house next week'
        }
    ]
    
    print(f"📋 Processing {len(leads)} leads...")
    
    # Create phone campaign
    phone_numbers = [lead['phone'] for lead in leads]
    campaign_id = system.creative_automation.create_phone_campaign(
        "Heavenly Hands Lead Generation Campaign",
        phone_numbers
    )
    
    print(f"✅ Phone campaign created: {campaign_id}")
    
    # Store leads in database
    for lead in leads:
        system.creative_automation._save_lead(lead)
    
    print("✅ Leads stored in database")
    
    # Create follow-up workflow
    workflow_id = system.agentic_workflows.create_creative_workflow(
        "Heavenly Hands Customer Follow-up",
        {
            'business_type': 'cleaning_service',
            'leads': leads,
            'follow_up_sequence': [
                'initial_call',
                'email_sequence',
                'social_media_engagement',
                'scheduling_consultation'
            ]
        }
    )
    
    print(f"✅ Follow-up workflow created: {workflow_id}")
    
    print("\\n🎯 Next Steps:")
    print("1. Update Twilio credentials in .env file")
    print("2. Start the webhook server: python heavenly_hands_webhook.py")
    print("3. Execute the phone campaign")
    print("4. Monitor results and optimize")

if __name__ == "__main__":
    main()
'''
    
    with open('heavenly_hands_leads.py', 'w') as f:
        f.write(lead_script)
    
    print("✅ Heavenly Hands phone automation scripts created")

def create_demo_script():
    """Create comprehensive demo script"""
    demo_script = '''#!/usr/bin/env python3
"""
Enhanced Creative Automation System - Full Demo
===============================================

Comprehensive demonstration of all enhanced capabilities
"""

import os
import json
from enhanced_creative_automation import EnhancedIntelligentOrganizationSystem
from dotenv import load_dotenv

load_dotenv()

def main():
    """Main demo function"""
    print("🚀 Enhanced Creative Automation System - Full Demo")
    print("=" * 60)
    
    # Initialize system
    system = EnhancedIntelligentOrganizationSystem()
    
    # 1. System Status
    print("\\n1️⃣ System Status:")
    status = system.get_system_status()
    print(f"   📊 System: {status['system_name']} v{status['version']}")
    print(f"   🔧 Components: {status['components']}")
    print(f"   🎯 Capabilities: {len(status['capabilities'])} features enabled")
    
    # 2. Content Indexing
    print("\\n2️⃣ Enhanced Content Indexing:")
    print("   🔍 Indexing project with enhanced semantic analysis...")
    system.index_project_content()
    print("   ✅ Content indexed with advanced vector search")
    
    # 3. Semantic Search Demo
    print("\\n3️⃣ Enhanced Semantic Search:")
    queries = [
        "cleaning services pricing",
        "contact information",
        "customer testimonials",
        "service areas"
    ]
    
    for query in queries:
        results = system.search_content(query, categories=['cleaning_services'])
        print(f"   🔍 '{query}': {len(results)} results")
    
    # 4. Creative Automation
    print("\\n4️⃣ Creative Automation Platform:")
    phone_system = system.create_heavenly_hands_phone_system()
    print(f"   📞 Phone campaign: {phone_system.get('phone_campaign_id', 'Not created')}")
    print(f"   🤖 Agentic workflow: {phone_system.get('agentic_workflow_id', 'Not created')}")
    
    # 5. Agentic Workflows
    print("\\n5️⃣ Agentic Workflows:")
    workflow_id = system.agentic_workflows.create_creative_workflow(
        "Comprehensive Marketing Automation",
        {
            'business_type': 'cleaning_service',
            'goals': ['lead_generation', 'customer_retention', 'brand_awareness'],
            'channels': ['phone', 'email', 'social_media', 'website']
        }
    )
    print(f"   ✅ Created workflow: {workflow_id}")
    
    # 6. Database Statistics
    print("\\n6️⃣ Database Statistics:")
    try:
        import sqlite3
        
        # Creative automation stats
        conn = sqlite3.connect('creative_automation.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM creative_tasks")
        tasks = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM automation_workflows")
        workflows = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM leads")
        leads = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"   📊 Creative Tasks: {tasks}")
        print(f"   📊 Automation Workflows: {workflows}")
        print(f"   📊 Leads: {leads}")
        
    except Exception as e:
        print(f"   ⚠️  Could not retrieve database stats: {e}")
    
    # 7. Next Steps
    print("\\n7️⃣ Next Steps:")
    print("   🎯 Configure Twilio credentials for phone automation")
    print("   🎯 Set up webhook server for TwiML handling")
    print("   🎯 Execute phone campaigns for lead generation")
    print("   🎯 Monitor and optimize based on results")
    print("   🎯 Scale to additional creative projects")
    
    print("\\n" + "=" * 60)
    print("🎉 Enhanced Creative Automation System Ready!")
    print("=" * 60)

if __name__ == "__main__":
    main()
'''
    
    with open('demo_enhanced_system.py', 'w') as f:
        f.write(demo_script)
    
    print("✅ Enhanced demo script created")

def main():
    """Main setup function"""
    print("🚀 Setting up Enhanced Creative Automation System")
    print("=" * 60)
    
    # Install requirements
    install_requirements()
    
    # Create enhanced environment
    create_enhanced_env()
    
    # Create Heavenly Hands phone scripts
    create_heavenly_hands_phone_scripts()
    
    # Create demo script
    create_demo_script()
    
    print("\\n" + "=" * 60)
    print("🎉 Enhanced Creative Automation System Setup Complete!")
    print("=" * 60)
    print("\\n📋 Next Steps:")
    print("1. Update Twilio credentials in .env file")
    print("2. Run: python demo_enhanced_system.py")
    print("3. Run: python heavenly_hands_leads.py")
    print("4. Start webhook server: python heavenly_hands_webhook.py")
    print("\\n🔧 Files Created:")
    print("   📄 enhanced_creative_automation.py - Main system")
    print("   📄 setup_enhanced_system.py - This setup script")
    print("   📄 demo_enhanced_system.py - Comprehensive demo")
    print("   📄 heavenly_hands_leads.py - Lead generation")
    print("   📄 heavenly_hands_webhook.py - TwiML webhook handler")
    print("   📄 .env - Enhanced environment configuration")

if __name__ == "__main__":
    main()