#!/usr/bin/env python3
"""Vapi.ai Demo Agent Generator - Create demo AI receptionists"""
import os, sys, json, requests
from pathlib import Path

# Load API key
sys.path.insert(0, str(Path.home() / '.env.d'))
try:
    from loader import load_env
    load_env()
except:
    pass

VAPI_API_KEY = os.getenv('VAPI_API_KEY', '')

# Demo agent templates by industry
DEMO_TEMPLATES = {
    'dentist': {
        'name': 'Dental Office AI Receptionist',
        'first_message': "Thank you for calling! How can I help you today?",
        'system_prompt': """You are a friendly AI receptionist for a dental office. Your role is to:
1. Answer common questions about services (cleanings, fillings, whitening, emergencies)
2. Provide office hours and location
3. Book appointments
4. Handle emergency calls (transfer immediately)

Services & Pricing:
- Regular Cleaning: $150
- Exam + X-rays: $200
- Fillings: $200-400
- Whitening: $500
- Emergency: Same-day available

Hours: Mon-Fri 8am-6pm, Sat 9am-2pm
Location: 123 Main St, Downtown

Be warm, professional, and efficient. Always confirm appointment details.""",
        'voice': 'jennifer',
        'functions': ['book_appointment', 'transfer_call']
    },

    'plumber': {
        'name': 'Plumbing Service AI Receptionist',
        'first_message': "Thanks for calling! Do you have a plumbing emergency or need to schedule service?",
        'system_prompt': """You are an AI receptionist for a plumbing company. Your role is to:
1. Determine urgency (emergency vs routine)
2. Describe services (repairs, installations, drain cleaning, water heaters)
3. Provide pricing estimates
4. Book appointments or dispatch emergency service

Services:
- Emergency Service: Available 24/7, $150 service call
- Drain Cleaning: $150-300
- Water Heater: $800-1500 installed
- Pipe Repairs: $200-800
- Installations: Custom quote

For emergencies, get address and transfer immediately.
For routine, book next available slot.

Be helpful and understand their stress level.""",
        'voice': 'mark',
        'functions': ['book_appointment', 'transfer_call', 'send_text']
    },

    'salon': {
        'name': 'Hair Salon AI Receptionist',
        'first_message': "Hi! Thanks for calling the salon. What service are you interested in today?",
        'system_prompt': """You are a friendly AI receptionist for a hair salon. Your role is to:
1. Book appointments for various services
2. Recommend services based on needs
3. Provide pricing
4. Mention current promotions

Services & Time:
- Haircut (Women): $60, 60min
- Haircut (Men): $35, 30min
- Color: $120+, 90-120min
- Highlights: $150+, 120min
- Blowout: $45, 45min
- Extensions: $300+, 180min

Hours: Tue-Sat 9am-7pm, Sun 10am-5pm
Stylists: Sarah (color specialist), Mike (cuts), Lisa (extensions)

Be bubbly, friendly, and enthusiastic about their beauty goals!""",
        'voice': 'jennifer',
        'functions': ['book_appointment']
    }
}

def create_vapi_agent(template_name):
    """Create a Vapi.ai agent from template"""

    if not VAPI_API_KEY:
        print("⚠️  Vapi API key not found")
        print("   Get one at: https://vapi.ai")
        print("   Add to ~/.env.d/automation-agents.env: VAPI_API_KEY=your_key")
        return None

    if template_name not in DEMO_TEMPLATES:
        print(f"❌ Template '{template_name}' not found")
        print(f"Available: {', '.join(DEMO_TEMPLATES.keys())}")
        return None

    template = DEMO_TEMPLATES[template_name]

    # Create agent via Vapi API
    url = "https://api.vapi.ai/assistant"
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": template['name'],
        "firstMessage": template['first_message'],
        "model": {
            "provider": "openai",
            "model": "gpt-4",
            "temperature": 0.7,
            "systemPrompt": template['system_prompt']
        },
        "voice": {
            "provider": "11labs",
            "voiceId": template['voice']
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        agent_data = response.json()

        return {
            'id': agent_data.get('id'),
            'name': agent_data.get('name'),
            'template': template_name,
            'created': True
        }

    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Response: {e.response.text}")
        return None

def generate_demo_script(industry):
    """Generate a demo call script"""
    scripts = {
        'dentist': """
🎙️ Demo Call Script - Dentist

YOU: "Hi, I'd like to schedule a cleaning"

AI: "I'd be happy to help you schedule a cleaning. Have you been to our office before?"

YOU: "No, first time"

AI: "Great! A new patient cleaning with exam and x-rays is $350 total. We have availability this week. Are you available Tuesday at 2pm or Thursday at 10am?"

YOU: "Thursday works"

AI: "Perfect! I'll book you for Thursday at 10am. Can I get your full name and phone number?"

YOU: "John Smith, 555-123-4567"

AI: "Thanks John! You're all set for Thursday at 10am. You'll receive a confirmation text shortly. Is there anything else I can help with today?"

💡 Key Points:
- Natural conversation flow
- Provides pricing upfront
- Offers specific time slots
- Captures contact info
- Sends confirmation
- Professional and warm tone
""",

        'plumber': """
🎙️ Demo Call Script - Plumber

YOU: "I have a leaking pipe under my kitchen sink"

AI: "I understand, a leaking pipe needs attention. Is this currently flooding or just dripping?"

YOU: "It's dripping pretty steadily"

AI: "Okay, we can get someone out today. Our emergency service call is $150 plus parts and labor. Your address?"

YOU: "123 Oak Street"

AI: "Got it. I can have a plumber there within 2 hours, or would you prefer to schedule for tomorrow morning at a lower rate?"

YOU: "Today is fine"

AI: "Perfect. You'll get a text when the plumber is 15 minutes away. His name is Mike and he's been with us for 10 years. Anything else?"

💡 Key Points:
- Assesses urgency
- Provides pricing
- Offers options
- Gets address
- Sets expectations
- Builds trust (experienced plumber)
""",

        'salon': """
🎙️ Demo Call Script - Salon

YOU: "I need a haircut for Saturday"

AI: "I'd love to help! Are you looking for a cut and style, or any color services?"

YOU: "Just a cut and style"

AI: "Perfect! That's $60 and takes about an hour. For Saturday, I have Sarah available at 11am or Lisa at 2pm. Both are amazing!"

YOU: "2pm with Lisa sounds great"

AI: "Excellent choice! Lisa is wonderful. Can I get your name and phone number?"

YOU: "Mary Johnson, 555-987-6543"

AI: "Thanks Mary! You're booked for Saturday at 2pm with Lisa. You'll get a reminder text the day before. So excited for you!"

💡 Key Points:
- Enthusiastic and friendly
- Clarifies services
- Gives pricing
- Offers stylist options
- Creates excitement
- Sends reminder
"""
    }

    return scripts.get(industry, "No script available for this industry")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("""Vapi.ai Demo Agent Generator

Usage: vapi_demo_generator.py <command> [industry]

Commands:
  list          - Show available demo templates
  create        - Create a demo agent
  script        - Generate demo call script

Industries: dentist, plumber, salon

Examples:
  vapi_demo_generator.py list
  vapi_demo_generator.py create dentist
  vapi_demo_generator.py script dentist

Setup:
  1. Sign up at vapi.ai
  2. Get your API key
  3. Add to ~/.env.d/automation-agents.env:
     VAPI_API_KEY=your_key_here
""")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'list':
        print("📋 Available Demo Templates:\n")
        for name, template in DEMO_TEMPLATES.items():
            print(f"🎙️  {name.upper()}")
            print(f"   Name: {template['name']}")
            print(f"   First Message: {template['first_message']}")
            print(f"   Voice: {template['voice']}")
            print()

    elif command == 'create':
        if len(sys.argv) < 3:
            print("Usage: vapi_demo_generator.py create <industry>")
            print(f"Industries: {', '.join(DEMO_TEMPLATES.keys())}")
            sys.exit(1)

        industry = sys.argv[2]
        print(f"🤖 Creating {industry} demo agent...")

        result = create_vapi_agent(industry)

        if result:
            print(f"✅ Agent created successfully!")
            print(f"   ID: {result['id']}")
            print(f"   Name: {result['name']}")
            print(f"\n💡 Next: Go to vapi.ai dashboard to test and configure phone number")

    elif command == 'script':
        if len(sys.argv) < 3:
            print("Usage: vapi_demo_generator.py script <industry>")
            print(f"Industries: {', '.join(DEMO_TEMPLATES.keys())}")
            sys.exit(1)

        industry = sys.argv[2]
        script = generate_demo_script(industry)
        print(script)

    else:
        print(f"❌ Unknown command: {command}")
        print("Available: list, create, script")
        sys.exit(1)
