#!/usr/bin/env python3
"""
Heavenly Hands Call Tracking - Simple Setup Script
Sets up the production-ready call tracking system
"""

import os
import subprocess
import sys
from pathlib import Path


def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")

    packages = [
        "django>=4.2.0",
        "twilio>=8.0.0",
        "phonenumber_field>=7.0.0",
        "python-dotenv>=1.0.0",
    ]

    try:
        for package in packages:
            print(f"   Installing {package}...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                check=True,
                capture_output=True,
            )

        print("✅ All dependencies installed successfully")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def create_manage_py():
    """Create manage.py file"""
    manage_py_content = '''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
'''

    try:
        with open("manage.py", "w") as f:
            f.write(manage_py_content)

        # Make executable
        os.chmod("manage.py", 0o755)
        print("✅ Created manage.py")
        return True

    except Exception as e:
        print(f"❌ Failed to create manage.py: {e}")
        return False


def create_django_app():
    """Create Django app structure"""
    print("🏗️  Creating Django app...")

    try:
        # Create app directory
        app_dir = Path("heavenly_hands_call_tracking")
        app_dir.mkdir(exist_ok=True)

        # Create __init__.py
        (app_dir / "__init__.py").touch()

        # Create apps.py
        apps_py_content = """from django.apps import AppConfig

class HeavenlyHandsCallTrackingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'heavenly_hands_call_tracking'
"""
        with open(app_dir / "apps.py", "w") as f:
            f.write(apps_py_content)

        # Create migrations directory
        migrations_dir = app_dir / "migrations"
        migrations_dir.mkdir(exist_ok=True)
        (migrations_dir / "__init__.py").touch()

        print("✅ Django app created")
        return True

    except Exception as e:
        print(f"❌ Failed to create Django app: {e}")
        return False


def run_django_commands():
    """Run Django setup commands"""
    print("🚀 Running Django commands...")

    try:
        # Make migrations
        print("   Making migrations...")
        subprocess.run(
            [sys.executable, "manage.py", "makemigrations"],
            check=True,
            capture_output=True,
        )

        # Run migrations
        print("   Running migrations...")
        subprocess.run(
            [sys.executable, "manage.py", "migrate"], check=True, capture_output=True
        )

        print("✅ Django commands completed")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Django commands failed: {e}")
        return False


def test_twilio():
    """Test Twilio connection"""
    print("📞 Testing Twilio connection...")

    try:
        from twilio.rest import Client

        # Get credentials from environment
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")

        if not account_sid or not auth_token:
            print("❌ Missing Twilio credentials")
            return False

        # Initialize Twilio client
        client = Client(account_sid, auth_token)

        # Test connection
        account = client.api.accounts(account_sid).fetch()

        print(f"✅ Twilio connection successful!")
        print(f"   Account Name: {account.friendly_name}")
        print(f"   Account Status: {account.status}")

        return True

    except Exception as e:
        print(f"❌ Twilio connection failed: {e}")
        return False


def main():
    """Main setup function"""
    print("🏠 Heavenly Hands Call Tracking - Simple Setup")
    print("=" * 60)

    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        return False

    # Create manage.py
    if not create_manage_py():
        print("❌ Setup failed at manage.py creation")
        return False

    # Create Django app
    if not create_django_app():
        print("❌ Setup failed at Django app creation")
        return False

    # Run Django commands
    if not run_django_commands():
        print("❌ Setup failed at Django commands")
        return False

    # Test Twilio
    if not test_twilio():
        print("❌ Setup failed at Twilio test")
        return False

    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Source your environment: source ~/.env.d/loader.sh")
    print("2. Start development server: python manage.py runserver")
    print("3. Access admin panel: http://localhost:8000/admin/")
    print("4. View API endpoints: http://localhost:8000/")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
