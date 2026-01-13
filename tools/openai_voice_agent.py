#!/usr/bin/env python3
"""OpenAI-Powered Voice Agent - Streaming + Embeddings for Business Knowledge"""
import os, sys, json, requests
from pathlib import Path
from openai import OpenAI

# Load API keys
sys.path.insert(0, str(Path.home() / '.env.d'))
try:
    from loader import load_env
    load_env()
except:
    pass

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class VoiceAgent:
    """Custom voice agent using OpenAI"""

    def __init__(self, business_name, business_type, knowledge_base=None):
        self.business_name = business_name
        self.business_type = business_type
        self.knowledge_base = knowledge_base or {}
        self.conversation_history = []

    def create_system_prompt(self):
        """Generate system prompt with embedded knowledge"""

        base_prompt = f"""You are a professional AI receptionist for {self.business_name}, a {self.business_type} in the Gainesville/Ocala, Florida area.

Your role is to:
1. Answer questions about services, hours, and location
2. Book appointments directly into the calendar
3. Qualify leads and capture contact information
4. Transfer urgent calls to staff when needed
5. Be warm, professional, and efficient

Business Information:
"""

        # Add embedded knowledge
        for key, value in self.knowledge_base.items():
            base_prompt += f"\n{key}: {value}"

        base_prompt += """

Always:
- Be friendly but professional
- Confirm appointment details
- Capture name and phone number
- Ask if there's anything else you can help with
- Never make up information you don't have

If you don't know something, say "Let me transfer you to someone who can help with that specific question."
"""

        return base_prompt

    def chat(self, user_message):
        """Process a conversation turn"""

        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        messages = [
            {"role": "system", "content": self.create_system_prompt()}
        ] + self.conversation_history

        # Use GPT-4 for best quality (or gpt-3.5-turbo for cost savings)
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Fast and cheap
            messages=messages,
            temperature=0.7,
            max_tokens=200
        )

        assistant_message = response.choices[0].message.content

        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def text_to_speech(self, text):
        """Convert text to speech using OpenAI TTS"""

        response = client.audio.speech.create(
            model="tts-1",  # or tts-1-hd for higher quality
            voice="alloy",  # alloy, echo, fable, onyx, nova, shimmer
            input=text
        )

        return response.content

    def speech_to_text(self, audio_file_path):
        """Convert speech to text using Whisper"""

        with open(audio_file_path, 'rb') as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        return transcript.text

    def create_embedding(self, text):
        """Create embedding for knowledge base search"""

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        return response.data[0].embedding

    def add_knowledge_from_website(self, url):
        """Scrape website and add to knowledge base"""

        try:
            import requests
            from bs4 import BeautifulSoup

            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract text
            text = soup.get_text(separator=' ', strip=True)

            # Create embedding
            embedding = self.create_embedding(text[:8000])  # Limit to 8k chars

            self.knowledge_base['website_content'] = text[:2000]  # Store snippet
            self.knowledge_base['website_embedding'] = embedding

            return True

        except Exception as e:
            print(f"Error scraping website: {e}")
            return False


# Pre-configured templates for Gainesville/Ocala businesses
GAINESVILLE_OCALA_TEMPLATES = {
    'dentist_gainesville': {
        'business_name': 'Gainesville Family Dentistry',
        'business_type': 'dental office',
        'knowledge_base': {
            'Services': 'Regular cleanings ($150), Exams ($200), Fillings ($200-400), Whitening ($500), Crowns ($1200), Root canals ($800-1500), Emergencies (same-day)',
            'Hours': 'Monday-Friday 8am-6pm, Saturday 9am-2pm',
            'Location': 'Gainesville, FL 32601',
            'Parking': 'Free parking available',
            'Insurance': 'We accept most major insurance plans',
            'Emergency': 'Same-day emergency appointments available',
            'New Patients': 'New patient special: $99 exam, cleaning, and x-rays (regular $350)'
        }
    },

    'plumber_ocala': {
        'business_name': 'Ocala Plumbing Pros',
        'business_type': 'plumbing service',
        'knowledge_base': {
            'Services': 'Emergency repairs, Drain cleaning, Water heaters, Pipe repairs, Installations, Leak detection, Sewer line work',
            'Pricing': 'Emergency service call: $150, Drain cleaning: $150-300, Water heater install: $800-1500, Hourly rate: $125',
            'Hours': '24/7 Emergency Service, Regular hours: Mon-Fri 7am-6pm, Sat 8am-4pm',
            'Location': 'Serving all of Ocala and Marion County',
            'Service_Area': 'Ocala, Silver Springs, Belleview, Dunnellon, and surrounding areas',
            'Response_Time': 'Emergency calls: 1-2 hours, Regular service: Same or next day',
            'Licensed': 'Licensed, bonded, and insured. FL License #CFC1234567'
        }
    },

    'salon_gainesville': {
        'business_name': 'Gainesville Glam Salon',
        'business_type': 'hair salon',
        'knowledge_base': {
            'Services': 'Haircuts, Color, Highlights, Balayage, Extensions, Treatments, Styling, Makeup',
            'Pricing': "Women's cut: $60, Men's cut: $35, Color: $120+, Highlights: $150+, Extensions: $300+, Blowout: $45",
            'Hours': 'Tuesday-Saturday 9am-7pm, Sunday 10am-5pm, Closed Monday',
            'Location': 'Near UF Campus, Gainesville FL',
            'Stylists': 'Sarah (color specialist), Mike (precision cuts), Lisa (extensions expert)',
            'Booking': 'Walk-ins welcome, but appointments preferred',
            'First_Visit': '20% off first visit for new clients'
        }
    },

    'hvac_gainesville': {
        'business_name': 'Gainesville AC & Heating',
        'business_type': 'HVAC service',
        'knowledge_base': {
            'Services': 'AC repair, AC installation, Heating repair, Maintenance, Emergency service, Duct cleaning, Air quality',
            'Pricing': 'Diagnostic: $89, Service call: $125, New AC unit: $3500-8000, Maintenance plan: $199/year',
            'Hours': '24/7 Emergency Service, Regular: Mon-Sat 7am-7pm',
            'Location': 'Serving Gainesville and Alachua County',
            'Service_Area': 'Gainesville, Alachua, Newberry, High Springs, Archer',
            'Emergency': 'Same-day service for AC emergencies (Florida heat is no joke!)',
            'Financing': 'Flexible financing available on new systems',
            'Licensed': 'Licensed and insured. CAC1234567'
        }
    },

    'lawyer_ocala': {
        'business_name': 'Ocala Legal Group',
        'business_type': 'law firm',
        'knowledge_base': {
            'Practice_Areas': 'Personal injury, Car accidents, Workers comp, Family law, Estate planning, Criminal defense',
            'Consultation': 'Free initial consultation for personal injury and car accident cases',
            'Hours': 'Monday-Friday 8am-6pm, Evening and weekend by appointment',
            'Location': 'Downtown Ocala, FL',
            'Fees': 'Personal injury: Contingency (no fee unless we win), Family law: $250/hour, Estate planning: Flat fees starting at $500',
            'Languages': 'English and Spanish speaking attorneys',
            'Experience': '25+ years combined experience serving Marion County'
        }
    }
}


def create_demo_agent(template_name='dentist_gainesville'):
    """Create a demo agent from template"""

    if template_name not in GAINESVILLE_OCALA_TEMPLATES:
        print(f"Template '{template_name}' not found")
        print(f"Available: {', '.join(GAINESVILLE_OCALA_TEMPLATES.keys())}")
        return None

    template = GAINESVILLE_OCALA_TEMPLATES[template_name]

    agent = VoiceAgent(
        business_name=template['business_name'],
        business_type=template['business_type'],
        knowledge_base=template['knowledge_base']
    )

    return agent


def interactive_demo():
    """Interactive demo of voice agent"""

    print("🎙️ OpenAI Voice Agent Demo")
    print("=" * 60)
    print("\nAvailable templates:")
    for i, name in enumerate(GAINESVILLE_OCALA_TEMPLATES.keys(), 1):
        template = GAINESVILLE_OCALA_TEMPLATES[name]
        print(f"{i}. {template['business_name']} ({template['business_type']})")

    choice = input("\nSelect template (1-5): ").strip()
    template_name = list(GAINESVILLE_OCALA_TEMPLATES.keys())[int(choice) - 1]

    agent = create_demo_agent(template_name)
    template = GAINESVILLE_OCALA_TEMPLATES[template_name]

    print(f"\n✅ Created agent for: {template['business_name']}")
    print("\nType your messages (or 'quit' to exit):")
    print("-" * 60)

    # First message from AI
    first_msg = f"Thank you for calling {template['business_name']}! How can I help you today?"
    print(f"\nAI: {first_msg}\n")
    agent.conversation_history.append({"role": "assistant", "content": first_msg})

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Thanks for testing! Goodbye.")
            break

        if not user_input:
            continue

        response = agent.chat(user_input)
        print(f"\nAI: {response}\n")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        interactive_demo()
    else:
        print("""OpenAI Voice Agent - Custom Built for Gainesville/Ocala

Usage:
  python3 openai_voice_agent.py demo     # Interactive demo

Cost Analysis:
  - GPT-4o-mini: $0.15/1M input tokens, $0.60/1M output tokens
  - Whisper STT: $0.006/minute
  - TTS: $15/1M characters

  Average call (5 min):
  - Transcription: $0.03
  - GPT: $0.02
  - TTS: $0.10
  - Total: ~$0.15/call

  vs Vapi: $0.05-0.09/min = $0.25-0.45/call

  Savings: 40-67% lower cost!

Templates available:
  - dentist_gainesville
  - plumber_ocala
  - salon_gainesville
  - hvac_gainesville
  - lawyer_ocala

Next: Integrate with Twilio for real phone calls
""")
