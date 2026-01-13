#!/usr/bin/env python3
"""
Complete Testing Suite
Tests all platforms and APIs before launch
"""
import os
import sys
from pathlib import Path

def load_apis():
    """Load API keys from master env"""
    master = Path.home() / ".env.d" / "MASTER_CONSOLIDATED.env"
    if master.exists():
        with open(master) as f:
            for line in f:
                if '=' in line and 'export' in line:
                    key, val = line.replace('export ', '').strip().split('=', 1)
                    os.environ[key] = val.strip('"').strip("'")
        return True
    return False

def test_api_keys():
    """Test all required API keys exist"""
    print("?? Testing API Keys...")
    
    required = {
        'OPENAI_API_KEY': 'Required for AI conversations',
        'TWILIO_ACCOUNT_SID': 'Required for calls/SMS',
        'TWILIO_AUTH_TOKEN': 'Required for Twilio auth',
        'TWILIO_PHONE_NUMBER': 'Required for outbound calls'
    }
    
    recommended = {
        'ANTHROPIC_API_KEY': 'Better empathetic responses',
        'GOOGLE_API_KEY': 'Cheap research (Gemini)',
        'GROQ_API_KEY': 'Blazing fast (free!)',
        'ELEVENLABS_API_KEY': 'Realistic voice AI'
    }
    
    all_required_found = True
    
    for key, description in required.items():
        value = os.getenv(key)
        if value and 'changeme' not in value.lower():
            print(f"   ? {key}")
        else:
            print(f"   ? {key} - {description}")
            all_required_found = False
    
    print()
    print("Recommended (optional):")
    for key, description in recommended.items():
        value = os.getenv(key)
        if value and 'changeme' not in value.lower():
            print(f"   ? {key}")
        else:
            print(f"   ??  {key} - {description}")
    
    print()
    return all_required_found

def test_openai():
    """Test OpenAI connection"""
    print("?? Testing OpenAI...")
    try:
        import openai
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Respond with just 'OK'"}],
            max_tokens=5
        )
        result = response.choices[0].message.content
        print(f"   ? OpenAI working: {result}")
        return True
    except Exception as e:
        print(f"   ? OpenAI error: {str(e)[:100]}")
        return False

def test_twilio():
    """Test Twilio connection"""
    print("?? Testing Twilio...")
    try:
        from twilio.rest import Client
        client = Client(
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN')
        )
        account = client.api.accounts(os.getenv('TWILIO_ACCOUNT_SID')).fetch()
        print(f"   ? Twilio connected: {account.friendly_name}")
        return True
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg:
            print(f"   ? Twilio auth failed - Check credentials")
        elif "403" in error_msg:
            print(f"   ??  Twilio test credentials - Upgrade to production")
        else:
            print(f"   ? Twilio error: {error_msg[:100]}")
        return False

def test_platform_files():
    """Test platform files exist"""
    print("?? Testing Platform Files...")
    
    files = {
        'Universal Empire': 'work/universal-sales-empire/MEGA_SALES_PLATFORM.py',
        'CleanConnect Pro': 'work/cleanconnect-pro/automated_sales_caller.py',
        'HeavenlyHands': 'work/heavenlyhands/heavenlyhands/heavenly_hands_web.py'
    }
    
    all_found = True
    for name, path in files.items():
        full_path = Path.home() / 'workspace' / path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"   ? {name} ({size:,} bytes)")
        else:
            print(f"   ? {name} - File not found")
            all_found = False
    
    print()
    return all_found

def test_dependencies():
    """Test required Python packages"""
    print("?? Testing Dependencies...")
    
    packages = {
        'openai': 'OpenAI SDK',
        'twilio': 'Twilio SDK',
        'anthropic': 'Anthropic SDK (optional)',
        'google.generativeai': 'Google Gemini (optional)',
    }
    
    for package, description in packages.items():
        try:
            __import__(package)
            print(f"   ? {description}")
        except ImportError:
            if 'optional' in description:
                print(f"   ??  {description} - Not installed")
            else:
                print(f"   ? {description} - REQUIRED")
    
    print()

def main():
    print()
    print("=" * 70)
    print("              ?? COMPLETE TESTING SUITE")
    print("=" * 70)
    print()
    
    # Load environment
    print("?? Loading environment variables...")
    if load_apis():
        print("   ? Loaded from ~/.env.d/MASTER_CONSOLIDATED.env")
    else:
        print("   ??  Master env not found - run: bash ~/.env.d/rebuild_master.sh")
    print()
    
    # Run all tests
    keys_ok = test_api_keys()
    openai_ok = test_openai() if os.getenv('OPENAI_API_KEY') else False
    twilio_ok = test_twilio() if os.getenv('TWILIO_ACCOUNT_SID') else False
    files_ok = test_platform_files()
    test_dependencies()
    
    # Summary
    print("=" * 70)
    print("                    RESULTS")
    print("=" * 70)
    print()
    
    if keys_ok and openai_ok and twilio_ok and files_ok:
        print("              ? ALL TESTS PASSED - READY TO LAUNCH!")
        print()
        print("Next steps:")
        print("  1. cd ~/workspace/work/universal-sales-empire/")
        print("  2. cat ACTION_PLAN.md")
        print("  3. LAUNCH your first campaign!")
    else:
        print("              ??  SOME TESTS FAILED")
        print()
        print("Fix these issues:")
        if not keys_ok:
            print("  ? Add missing API keys to ~/.env.d/")
        if not openai_ok:
            print("  ? Fix OpenAI connection")
        if not twilio_ok:
            print("  ? Fix Twilio connection")
        if not files_ok:
            print("  ? Check platform files exist")
        print()
        print("Then run this test again: python ~/workspace/test_everything.py")
    
    print("=" * 70)
    print()

if __name__ == "__main__":
    main()
