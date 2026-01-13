#!/usr/bin/env python3
"""
Test Twilio Connection with Live Credentials
Heavenly Hands Cleaning Service
"""

import os
import sys
from pathlib import Path
from twilio.rest import Client
from twilio.base.exceptions import TwilioException

def test_twilio_connection():
    """Test Twilio connection with live credentials"""

    print("🔍 Testing Twilio Connection with Live Credentials")
    print("=" * 60)

    # Load environment variables from the live credentials file
    env_file = Path(__file__).parent / "heavenly-hands-live.env"

    if not env_file.exists():
        print("❌ Environment file not found: heavenly-hands-live.env")
        return False

    # Load environment variables
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

    # Get Twilio credentials
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    phone_number = os.getenv('TWILIO_PHONE_NUMBER')

    print(f"📞 Account SID: {account_sid}")
    print(f"🔑 Auth Token: {auth_token[:8]}...{auth_token[-8:] if auth_token else 'None'}")
    print(f"📱 Phone Number: {phone_number}")
    print()

    if not all([account_sid, auth_token, phone_number]):
        print("❌ Missing Twilio credentials")
        return False

    try:
        # Initialize Twilio client
        print("🔌 Initializing Twilio client...")
        client = Client(account_sid, auth_token)

        # Test account access
        print("📊 Testing account access...")
        account = client.api.accounts(account_sid).fetch()
        print(f"✅ Account Status: {account.status}")
        print(f"✅ Account Name: {account.friendly_name}")
        print(f"✅ Account Type: {account.type}")

        # Test phone number access
        print("\n📱 Testing phone number access...")
        incoming_numbers = client.incoming_phone_numbers.list(limit=5)

        if incoming_numbers:
            print(f"✅ Found {len(incoming_numbers)} phone number(s):")
            for number in incoming_numbers:
                print(f"   📞 {number.phone_number} - {number.friendly_name}")
        else:
            print("⚠️  No phone numbers found")

        # Test messaging capability
        print("\n💬 Testing messaging capability...")
        try:
            # Just test if we can access messaging (don't actually send)
            messages = client.messages.list(limit=1)
            print("✅ Messaging API accessible")
        except Exception as e:
            print(f"⚠️  Messaging API issue: {e}")

        # Test voice capability
        print("\n🎙️ Testing voice capability...")
        try:
            # Test if we can access calls (don't actually make a call)
            calls = client.calls.list(limit=1)
            print("✅ Voice API accessible")
        except Exception as e:
            print(f"⚠️  Voice API issue: {e}")

        print("\n🎉 Twilio connection test completed successfully!")
        print("\n📋 Next Steps:")
        print("1. Update your webhook URLs in Twilio console")
        print("2. Configure phone number settings")
        print("3. Test incoming/outgoing calls")
        print("4. Deploy to avatararts.org")

        return True

    except TwilioException as e:
        print(f"❌ Twilio Error: {e}")
        print(f"   Error Code: {e.code}")
        print(f"   Error Message: {e.msg}")
        return False

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    success = test_twilio_connection()
    sys.exit(0 if success else 1)
