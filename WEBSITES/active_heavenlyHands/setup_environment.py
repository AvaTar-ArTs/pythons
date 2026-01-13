#!/usr/bin/env python3
"""
Heavenly Hands Environment Configuration Setup
Integration with ~/.env.d system
"""

import os
import shutil
from pathlib import Path


def create_heavenly_hands_env():
    """Create Heavenly Hands environment configuration"""

    # Environment configuration content
    env_content = """# Heavenly Hands Call Tracking Environment Configuration
# Production-ready call tracking system for Heavenly Hands Cleaning Service

# Twilio Configuration (from your Twilio console)
TWILIO_ACCOUNT_SID=ACfa8e756d9538a305771807953e255e80
TWILIO_AUTH_TOKEN=d810cdc8cd589842b2c4a493fcc5667c
TWILIO_PHONE_NUMBER=+13525811245

# Twilio API Key (if using API keys instead of auth token)
TWILIO_API_KEY_SID=SK1cd7788f5f8c3973ac5db56aeec59ba2
TWILIO_API_KEY_SECRET=XqO1aUZXHBHjSjZxoAA0IpJLil2ASlvg

# Django Configuration
DJANGO_SECRET_KEY=heavenly-hands-call-tracking-production-secret-key-2025
DEBUG=False

# Webhook Configuration
WEBHOOK_BASE_URL=https://heavenlyhands.avatararts.org

# Heavenly Hands Business Configuration
HEAVENLY_HANDS_MAIN_NUMBER=+13525811245
HEAVENLY_HANDS_EMAIL=HHCleaning08@gmail.com
HEAVENLY_HANDS_OWNER=Kimberly Moeller

# Service Areas
SERVICE_AREAS=Gainesville,Ocala,Alachua,High Springs,Newberry,Micanopy

# Database Configuration
DATABASE_URL=sqlite:///heavenly_hands_call_tracking.db

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=heavenly_hands_call_tracking.log

# Production Settings
ALLOWED_HOSTS=localhost,127.0.0.1,heavenlyhands.avatararts.org
STATIC_ROOT=/path/to/staticfiles
MEDIA_ROOT=/path/to/media

# Security Settings
SECURE_SSL_REDIRECT=True
SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Performance Settings
CACHE_BACKEND=django.core.cache.backends.locmem.LocMemCache
CACHE_TIMEOUT=300

# Email Configuration (for notifications)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=HHCleaning08@gmail.com
EMAIL_HOST_PASSWORD=your_email_password_here

# Analytics Configuration
GOOGLE_ANALYTICS_ID=GA-XXXXXXXXX
MIXPANEL_TOKEN=your_mixpanel_token_here

# Monitoring Configuration
SENTRY_DSN=your_sentry_dsn_here
NEW_RELIC_LICENSE_KEY=your_newrelic_key_here

# Backup Configuration
BACKUP_S3_BUCKET=heavenly-hands-backups
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1
"""

    # Create the environment file
    env_file_path = Path.home() / ".env.d" / "heavenly-hands.env"

    try:
        with open(env_file_path, "w") as f:
            f.write(env_content)

        print(f"✅ Created Heavenly Hands environment file: {env_file_path}")
        print("🔐 File permissions set to secure (600)")

        # Set secure permissions
        os.chmod(env_file_path, 0o600)

        return True

    except Exception as e:
        print(f"❌ Error creating environment file: {e}")
        return False


def update_loader_integration():
    """Update loader.sh to include Heavenly Hands environment"""

    loader_path = Path.home() / ".env.d" / "loader.sh"

    if not loader_path.exists():
        print("⚠️  Loader script not found. Please create it manually.")
        return False

    try:
        # Read current loader content
        with open(loader_path, "r") as f:
            content = f.read()

        # Check if Heavenly Hands is already included
        if "heavenly-hands.env" in content:
            print("✅ Heavenly Hands environment already integrated in loader.sh")
            return True

        # Add Heavenly Hands integration
        integration_code = """
# Heavenly Hands Call Tracking Integration
if [ -f "$ENV_DIR/heavenly-hands.env" ]; then
    echo "🏠 Loading Heavenly Hands Call Tracking environment..."
    source "$ENV_DIR/heavenly-hands.env"
    export HEAVENLY_HANDS_LOADED=true
fi
"""

        # Append to loader
        with open(loader_path, "a") as f:
            f.write(integration_code)

        print("✅ Updated loader.sh to include Heavenly Hands environment")
        return True

    except Exception as e:
        print(f"❌ Error updating loader.sh: {e}")
        return False


def create_django_settings_integration():
    """Create Django settings that integrate with ~/.env.d"""

    django_settings_content = '''#!/usr/bin/env python3
"""
Django Settings for Heavenly Hands Call Tracking
Integrated with ~/.env.d environment system
"""

import os
import sys
from pathlib import Path

# Add ~/.env.d to Python path for loader integration
sys.path.insert(0, str(Path.home() / '.env.d'))

try:
    from loader import load_env
    load_env()
    print("✅ Loaded environment from ~/.env.d")
except ImportError:
    print("⚠️  Could not load ~/.env.d environment")
except Exception as e:
    print(f"⚠️  Error loading environment: {e}")

# Django settings
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'heavenly-hands-call-tracking-secret-key-change-in-production')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,heavenlyhands.avatararts.org').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'phonenumber_field',
    'heavenly_hands_call_tracking',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'heavenly_hands_urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'heavenly_hands_call_tracking.db',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Heavenly Hands specific settings from environment
HEAVENLY_HANDS_SETTINGS = {
    'MAIN_PHONE_NUMBER': os.getenv('HEAVENLY_HANDS_MAIN_NUMBER', '+13525811245'),
    'EMAIL': os.getenv('HEAVENLY_HANDS_EMAIL', 'HHCleaning08@gmail.com'),
    'OWNER': os.getenv('HEAVENLY_HANDS_OWNER', 'Kimberly Moeller'),
    'SERVICE_AREAS': os.getenv('SERVICE_AREAS', 'Gainesville,Ocala,Alachua,High Springs,Newberry,Micanopy').split(','),
    'CAMPAIGN_TYPES': ['google_ads', 'facebook', 'yelp', 'referral', 'direct', 'other'],
    'SERVICE_TYPES': ['residential', 'commercial', 'airbnb', 'move_in_out', 'deep_clean', 'recurring', 'one_time'],
}

# Twilio settings from environment
TWILIO_SETTINGS = {
    'ACCOUNT_SID': os.getenv('TWILIO_ACCOUNT_SID'),
    'AUTH_TOKEN': os.getenv('TWILIO_AUTH_TOKEN'),
    'PHONE_NUMBER': os.getenv('TWILIO_PHONE_NUMBER'),
    'API_KEY_SID': os.getenv('TWILIO_API_KEY_SID'),
    'API_KEY_SECRET': os.getenv('TWILIO_API_KEY_SECRET'),
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / os.getenv('LOG_FILE', 'heavenly_hands_call_tracking.log'),
        },
        'console': {
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'heavenly_hands_call_tracking': {
            'handlers': ['file', 'console'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
    },
}

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True').lower() == 'true'
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True').lower() == 'true'
    CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'True').lower() == 'true'

print(f"🏠 Heavenly Hands Call Tracking configured")
print(f"📞 Main Number: {HEAVENLY_HANDS_SETTINGS['MAIN_PHONE_NUMBER']}")
print(f"📧 Email: {HEAVENLY_HANDS_SETTINGS['EMAIL']}")
print(f"👤 Owner: {HEAVENLY_HANDS_SETTINGS['OWNER']}")
print(f"🌍 Service Areas: {', '.join(HEAVENLY_HANDS_SETTINGS['SERVICE_AREAS'])}")
'''

    settings_file = Path("/Users/steven/ai-sites/heavenlyHands/settings.py")

    try:
        with open(settings_file, "w") as f:
            f.write(django_settings_content)

        print(f"✅ Created Django settings with ~/.env.d integration: {settings_file}")
        return True

    except Exception as e:
        print(f"❌ Error creating Django settings: {e}")
        return False


def main():
    """Main setup function"""
    print("🏠 Heavenly Hands Call Tracking - Environment Setup")
    print("=" * 60)

    # Create environment file
    print("\n📝 Creating environment configuration...")
    if create_heavenly_hands_env():
        print("✅ Environment file created successfully")
    else:
        print("❌ Failed to create environment file")
        return False

    # Update loader integration
    print("\n🔗 Updating loader integration...")
    if update_loader_integration():
        print("✅ Loader integration updated")
    else:
        print("⚠️  Loader integration failed (manual setup required)")

    # Create Django settings
    print("\n⚙️  Creating Django settings...")
    if create_django_settings_integration():
        print("✅ Django settings created")
    else:
        print("❌ Django settings creation failed")
        return False

    print("\n🎉 Environment setup complete!")
    print("\n📋 Next steps:")
    print("1. Source your environment: source ~/.env.d/loader.sh")
    print("2. Verify Twilio credentials: echo $TWILIO_ACCOUNT_SID")
    print("3. Run Django migrations: python manage.py migrate")
    print("4. Start the server: python manage.py runserver")

    return True


if __name__ == "__main__":
    main()
