#!/usr/bin/env python3
"""
Quick Connection Test - Test all API connections
"""
import os
from pathlib import Path

# Load environment
master_env = Path.home() / ".env.d" / "MASTER_CONSOLIDATED.env"
if master_env.exists():
    with open(master_env) as f:
        for line in f:
            if 'export ' in line and '=' in line:
                line = line.replace('export ', '').strip()
                if line and not line.startswith('#'):
                    key, val = line.split('=', 1)
                    os.environ[key] = val.strip('"').strip("'")

print("=" * 70)
print("              ?? API CONNECTION TESTS")
print("=" * 70)
print()

# Test 1: OpenAI
print("1?? Testing OpenAI...")
try:
    import openai
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Reply with just: OK"}],
        max_tokens=5
    )
    result = response.choices[0].message.content
    print(f"   ? OpenAI CONNECTED: {result}")
    print(f"   Model: gpt-3.5-turbo")
except Exception as e:
    error_msg = str(e)
    if "401" in error_msg or "Incorrect API key" in error_msg:
        print(f"   ? OpenAI: Invalid API key")
    elif "quota" in error_msg.lower():
        print(f"   ??  OpenAI: No credits (add billing)")
    else:
        print(f"   ? OpenAI: {error_msg[:80]}")
print()

# Test 2: Anthropic/Claude
print("2?? Testing Anthropic/Claude...")
try:
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=10,
        messages=[{"role": "user", "content": "Say: OK"}]
    )
    result = message.content[0].text
    print(f"   ? Claude CONNECTED: {result}")
    print(f"   Model: claude-3-5-sonnet")
except Exception as e:
    error_msg = str(e)
    if "401" in error_msg or "authentication" in error_msg.lower():
        print(f"   ? Claude: Invalid API key")
    else:
        print(f"   ? Claude: {error_msg[:80]}")
print()

# Test 3: Groq
print("3?? Testing Groq...")
try:
    import groq
    client = groq.Groq(api_key=os.getenv('GROQ_API_KEY'))
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Say: OK"}],
        max_tokens=5
    )
    result = completion.choices[0].message.content
    print(f"   ? Groq CONNECTED: {result}")
    print(f"   Model: llama-3.1-8b-instant (FREE!)")
except Exception as e:
    error_msg = str(e)
    if "401" in error_msg:
        print(f"   ? Groq: Invalid API key")
    else:
        print(f"   ? Groq: {error_msg[:80]}")
print()

# Test 4: Twilio
print("4?? Testing Twilio...")
try:
    from twilio.rest import Client
    client = Client(
        os.getenv('TWILIO_ACCOUNT_SID'),
        os.getenv('TWILIO_AUTH_TOKEN')
    )
    account = client.api.accounts(os.getenv('TWILIO_ACCOUNT_SID')).fetch()
    print(f"   ? Twilio CONNECTED")
    print(f"   Account: {account.friendly_name}")
    print(f"   Phone: {os.getenv('TWILIO_PHONE_NUMBER')}")
    print(f"   Status: {account.status}")
except Exception as e:
    error_msg = str(e)
    if "401" in error_msg or "20003" in error_msg:
        print(f"   ? Twilio: Invalid credentials")
    elif "403" in error_msg:
        print(f"   ??  Twilio: Trial account (upgrade for production)")
    else:
        print(f"   ? Twilio: {error_msg[:80]}")
print()

# Test 5: ElevenLabs
print("5?? Testing ElevenLabs...")
try:
    from elevenlabs import generate, set_api_key
    set_api_key(os.getenv('ELEVENLABS_API_KEY'))
    # Just check if we can import and set key - actual generation costs money
    print(f"   ? ElevenLabs API KEY SET")
    print(f"   Ready for voice generation")
except Exception as e:
    print(f"   ??  ElevenLabs: {str(e)[:80]}")
print()

# Test 6: Google Gemini
print("6?? Testing Google Gemini...")
try:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Say: OK")
    print(f"   ? Gemini CONNECTED: {response.text[:20]}")
    print(f"   Model: gemini-pro (FREE!)")
except Exception as e:
    error_msg = str(e)
    if "API key not valid" in error_msg:
        print(f"   ? Gemini: Invalid API key")
    else:
        print(f"   ? Gemini: {error_msg[:80]}")
print()

# Summary
print("=" * 70)
print("                    SUMMARY")
print("=" * 70)
print()
print("? = Working perfectly")
print("??  = Configured but limited (trial/credits)")
print("? = Needs attention")
print()
print("?? Cost Per Call Estimate:")
print("   OpenAI (GPT-3.5):  $0.002")
print("   Claude:            $0.015")
print("   Groq:              FREE!")
print("   Gemini:            FREE!")
print("   Twilio:            $0.01-0.02/min")
print("   ElevenLabs:        $0.10/1000 chars")
print()
print("?? Recommended Stack:")
print("   Primary AI:   Claude (best conversations)")
print("   Fast AI:      Groq (free + fast!)")
print("   Research:     Gemini (free!)")
print("   Calls:        Twilio")
print("   Voice:        ElevenLabs")
print()
print("=" * 70)
