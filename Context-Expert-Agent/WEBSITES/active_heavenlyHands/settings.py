#!/usr/bin/env python3
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
