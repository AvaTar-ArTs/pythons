#!/usr/bin/env python3
"""
Heavenly Hands Twilio Connection Test
Test the Twilio API connection with your credentials
"""

import os
import sys
from pathlib import Path

# Add ~/.env.d to Python path for loader integration
sys.path.insert(0, str(Path.home() / ".env.d"))

try:
    from loader import load_env

    load_env()
    print("✅ Loaded environment from ~/.env.d")
except ImportError:
    print("⚠️  Could not load ~/.env.d environment")
except Exception as e:
    print(f"⚠️  Error loading environment: {e}")


def test_twilio_connection():
    """Test Twilio API connection"""
    try:
        from twilio.rest import Client

        # Get credentials from environment
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")

        if not account_sid or not auth_token:
            print("❌ Missing Twilio credentials")
            return False

        print(f"🔑 Testing Twilio connection...")
        print(f"   Account SID: {account_sid}")
        print(f"   Auth Token: {auth_token[:8]}...")

        # Initialize Twilio client
        client = Client(account_sid, auth_token)

        # Test connection by fetching account info
        account = client.api.accounts(account_sid).fetch()

        print(f"✅ Twilio connection successful!")
        print(f"   Account Name: {account.friendly_name}")
        print(f"   Account Status: {account.status}")
        print(f"   Account Type: {account.type}")

        # List available phone numbers
        print(f"\n📞 Available Phone Numbers:")
        incoming_numbers = client.incoming_phone_numbers.list(limit=5)

        if incoming_numbers:
            for number in incoming_numbers:
                print(f"   {number.phone_number} - {number.friendly_name or 'Unnamed'}")
        else:
            print("   No phone numbers found")

        return True

    except Exception as e:
        print(f"❌ Twilio connection failed: {e}")
        return False


def test_heavenly_hands_config():
    """Test Heavenly Hands configuration"""
    print(f"\n🏠 Heavenly Hands Configuration:")
    print(f"   Main Number: {os.getenv('HEAVENLY_HANDS_MAIN_NUMBER')}")
    print(f"   Email: {os.getenv('HEAVENLY_HANDS_EMAIL')}")
    print(f"   Owner: {os.getenv('HEAVENLY_HANDS_OWNER')}")
    print(f"   Service Areas: {os.getenv('SERVICE_AREAS')}")
    print(f"   Webhook URL: {os.getenv('WEBHOOK_BASE_URL')}")


def main():
    """Main test function"""
    print("🏠 Heavenly Hands Call Tracking - Twilio Connection Test")
    print("=" * 60)

    # Test Twilio connection
    twilio_success = test_twilio_connection()

    # Test Heavenly Hands configuration
    test_heavenly_hands_config()

    print(f"\n📋 Test Results:")
    if twilio_success:
        print("✅ All tests passed! Ready for production deployment")
        print("\n🚀 Next steps:")
        print("1. Run Django migrations: python manage.py migrate")
        print("2. Create sample data: python manage.py create_sample_data")
        print("3. Start development server: python manage.py runserver")
        print("4. Deploy to production: Follow CALL_TRACKING_DEPLOYMENT_GUIDE.md")
    else:
        print("❌ Tests failed. Please check your Twilio credentials")
        print("\n🔧 Troubleshooting:")
        print("1. Verify TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN")
        print("2. Check Twilio account status")
        print("3. Ensure sufficient account balance")

    return twilio_success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
