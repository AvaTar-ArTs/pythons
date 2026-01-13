#!/usr/bin/env python3
"""
Heavenly Hands Django Settings and URL Configuration
Production-ready Django setup for call tracking
"""

# settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY", "heavenly-hands-call-tracking-secret-key-change-in-production"
)

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "heavenlyhands.avatararts.org"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "phonenumber_field",
    "heavenly_hands_call_tracking",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "heavenly_hands_urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "heavenly_hands_call_tracking.db",
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Heavenly Hands specific settings
HEAVENLY_HANDS_SETTINGS = {
    "MAIN_PHONE_NUMBER": "+13525811245",
    "SERVICE_AREAS": [
        "Gainesville",
        "Ocala",
        "Alachua",
        "High Springs",
        "Newberry",
        "Micanopy",
    ],
    "CAMPAIGN_TYPES": ["google_ads", "facebook", "yelp", "referral", "direct", "other"],
    "SERVICE_TYPES": [
        "residential",
        "commercial",
        "airbnb",
        "move_in_out",
        "deep_clean",
        "recurring",
        "one_time",
    ],
}

# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "heavenly_hands_call_tracking.log",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "heavenly_hands_call_tracking": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

# URL Configuration (urls.py)
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.analytics_dashboard, name="dashboard"),
    path(
        "webhook/voice/<str:lead_source_name>/",
        views.webhook_voice,
        name="webhook_voice",
    ),
    path("api/leads-by-source/", views.api_leads_by_source, name="api_leads_by_source"),
    path("api/leads-by-city/", views.api_leads_by_city, name="api_leads_by_city"),
    path(
        "api/conversion-rates/", views.api_conversion_rates, name="api_conversion_rates"
    ),
    path("api/recent-leads/", views.api_recent_leads, name="api_recent_leads"),
    path("api/analytics/", views.api_analytics, name="api_analytics"),
]


# Management commands
def create_sample_data():
    """Create sample data for testing"""
    from django.core.management.base import BaseCommand

    from heavenly_hands_call_tracking.models import (
        HeavenlyHandsLead,
        HeavenlyHandsLeadSource,
    )

    class Command(BaseCommand):
        help = "Create sample data for Heavenly Hands call tracking"

        def handle(self, *args, **options):
            # Create sample lead sources
            sources = [
                {
                    "name": "Google Ads Gainesville",
                    "incoming_number": "+13525551234",
                    "forwarding_number": "+13525811245",
                    "campaign_type": "google_ads",
                    "service_area": "gainesville",
                },
                {
                    "name": "Facebook Ocala",
                    "incoming_number": "+13525551235",
                    "forwarding_number": "+13525811245",
                    "campaign_type": "facebook",
                    "service_area": "ocala",
                },
                {
                    "name": "Yelp Reviews",
                    "incoming_number": "+13525551236",
                    "forwarding_number": "+13525811245",
                    "campaign_type": "yelp",
                    "service_area": "all",
                },
            ]

            for source_data in sources:
                source, created = HeavenlyHandsLeadSource.objects.get_or_create(
                    name=source_data["name"], defaults=source_data
                )
                if created:
                    self.stdout.write(f"Created lead source: {source.name}")

            # Create sample leads
            sample_leads = [
                {
                    "source": HeavenlyHandsLeadSource.objects.get(
                        name="Google Ads Gainesville"
                    ),
                    "phone_number": "+13525551237",
                    "city": "Gainesville",
                    "state": "FL",
                    "customer_name": "John Smith",
                    "service_type": "residential",
                    "call_outcome": "interested",
                    "booking_made": True,
                },
                {
                    "source": HeavenlyHandsLeadSource.objects.get(
                        name="Facebook Ocala"
                    ),
                    "phone_number": "+13525551238",
                    "city": "Ocala",
                    "state": "FL",
                    "customer_name": "Sarah Johnson",
                    "service_type": "commercial",
                    "call_outcome": "interested",
                    "booking_made": False,
                },
                {
                    "source": HeavenlyHandsLeadSource.objects.get(name="Yelp Reviews"),
                    "phone_number": "+13525551239",
                    "city": "Gainesville",
                    "state": "FL",
                    "customer_name": "Mike Davis",
                    "service_type": "airbnb",
                    "call_outcome": "interested",
                    "booking_made": True,
                },
            ]

            for lead_data in sample_leads:
                lead, created = HeavenlyHandsLead.objects.get_or_create(
                    phone_number=lead_data["phone_number"], defaults=lead_data
                )
                if created:
                    self.stdout.write(f"Created lead: {lead.customer_name}")

            self.stdout.write(self.style.SUCCESS("Sample data created successfully!"))


# Production deployment script
def deploy_to_production():
    """Deploy Heavenly Hands call tracking to production"""
    import os
    import subprocess

    print("🚀 Deploying Heavenly Hands Call Tracking to Production")
    print("=" * 60)

    # Check environment variables
    required_vars = ["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_PHONE_NUMBER"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False

    print("✅ Environment variables configured")

    # Run Django migrations
    print("📊 Running database migrations...")
    try:
        subprocess.run(["python", "manage.py", "migrate"], check=True)
        print("✅ Database migrations completed")
    except subprocess.CalledProcessError:
        print("❌ Database migration failed")
        return False

    # Collect static files
    print("📁 Collecting static files...")
    try:
        subprocess.run(
            ["python", "manage.py", "collectstatic", "--noinput"], check=True
        )
        print("✅ Static files collected")
    except subprocess.CalledProcessError:
        print("❌ Static file collection failed")
        return False

    # Create sample data
    print("📝 Creating sample data...")
    try:
        subprocess.run(["python", "manage.py", "create_sample_data"], check=True)
        print("✅ Sample data created")
    except subprocess.CalledProcessError:
        print("⚠️  Sample data creation failed (optional)")

    print("\n🎉 Deployment completed successfully!")
    print("📞 Call tracking system is ready for production")
    print("🌐 Dashboard available at: https://heavenlyhands.avatararts.org")
    print("📊 Admin panel: https://heavenlyhands.avatararts.org/admin")

    return True


if __name__ == "__main__":
    deploy_to_production()
