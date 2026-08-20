#!/usr/bin/env python3
"""
Heavenly Hands Call Tracking - Complete Setup Script
Sets up the production-ready call tracking system
"""

import os
import sys
import subprocess
from pathlib import Path

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")

    packages = [
        'django>=4.2.0',
        'twilio>=8.0.0',
        'phonenumber_field>=7.0.0',
        'python-dotenv>=1.0.0',
        'requests>=2.31.0',
        'openai>=1.0.0',
        'numpy>=1.24.0',
        'pandas>=2.0.0',
        'matplotlib>=3.7.0',
        'seaborn>=0.12.0',
        'plotly>=5.15.0',
        'scikit-learn>=1.3.0',
        'spacy>=3.6.0',
        'networkx>=3.1.0',
        'sentence-transformers>=2.2.0',
        'chromadb>=0.4.0',
        'faiss-cpu>=1.7.0',
        'appium-python-client>=3.0.0',
        'boto3>=1.28.0',
        'google-cloud-storage>=2.10.0',
        'google-cloud-compute>=1.14.0'
    ]

    try:
        for package in packages:
            print(f"   Installing {package}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', package],
                         check=True, capture_output=True)

        print("✅ All dependencies installed successfully")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_django_project():
    """Set up Django project structure"""
    print("\n🏗️  Setting up Django project...")

    project_dir = Path('/Users/steven/ai-sites/heavenlyHands')

    # Create Django project structure
    django_structure = {
        'manage.py': '''#!/usr/bin/env python
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
''',

        'wsgi.py': '''"""
WSGI config for heavenly_hands_call_tracking project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application = get_wsgi_application()
''',

        'asgi.py': '''"""
ASGI config for heavenly_hands_call_tracking project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application = get_asgi_application()
''',

        'urls.py': '''"""
URL configuration for heavenly_hands_call_tracking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse('''
    <h1>Heavenly Hands Call Tracking System</h1>
    <p>Production-ready call tracking for Heavenly Hands Cleaning Service</p>
    <ul>
        <li><a href="/admin/">Admin Panel</a></li>
        <li><a href="/api/leads-by-source/">Leads by Source API</a></li>
        <li><a href="/api/leads-by-city/">Leads by City API</a></li>
        <li><a href="/api/conversion-rates/">Conversion Rates API</a></li>
        <li><a href="/api/recent-leads/">Recent Leads API</a></li>
    </ul>
    ''')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('webhook/', include('heavenly_hands_call_tracking.urls')),
    path('api/', include('heavenly_hands_call_tracking.urls')),
]
''',

        'heavenly_hands_call_tracking/__init__.py': '',
        'heavenly_hands_call_tracking/apps.py': '''from django.apps import AppConfig

class HeavenlyHandsCallTrackingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'heavenly_hands_call_tracking'
''',

        'heavenly_hands_call_tracking/urls.py': '''from django.urls import path
from . import views

urlpatterns = [
    path('webhook/voice/<str:lead_source_name>/', views.webhook_voice, name='webhook_voice'),
    path('api/leads-by-source/', views.api_leads_by_source, name='api_leads_by_source'),
    path('api/leads-by-city/', views.api_leads_by_city, name='api_leads_by_city'),
    path('api/conversion-rates/', views.api_conversion_rates, name='api_conversion_rates'),
    path('api/recent-leads/', views.api_recent_leads, name='api_recent_leads'),
    path('api/analytics/', views.api_analytics, name='api_analytics'),
]
''',

        'heavenly_hands_call_tracking/models.py': '''from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class HeavenlyHandsLeadSourceManager(models.Manager):
    """Custom manager for Heavenly Hands lead sources"""

    def get_leads_per_source(self):
        """Get the number of leads for each lead source"""
        from django.db.models import Count
        queryset = self.all().annotate(Count("lead")).order_by("name")
        data = list(queryset.values("name", "lead__count"))
        return data

    def get_conversion_rates(self):
        """Get conversion rates for each lead source"""
        from django.db.models import Count, Q
        queryset = self.all().annotate(
            total_leads=Count("lead"),
            successful_bookings=Count("lead", filter=Q(lead__booking_made=True)),
        )

        data = []
        for source in queryset:
            conversion_rate = 0
            if source.total_leads > 0:
                conversion_rate = (
                    source.successful_bookings / source.total_leads
                ) * 100

            data.append(
                {
                    "name": source.name,
                    "total_leads": source.total_leads,
                    "successful_bookings": source.successful_bookings,
                    "conversion_rate": round(conversion_rate, 2),
                }
            )

        return data

class HeavenlyHandsLeadSource(models.Model):
    """Lead source model for Heavenly Hands cleaning service"""

    name = models.CharField(
        max_length=100,
        blank=True,
        help_text='E.g. "Google Ads Gainesville", "Facebook Ocala", "Yelp Reviews"',
    )
    incoming_number = PhoneNumberField(
        unique=True,
        help_text="A phone number purchased through Twilio for this lead source",
    )
    forwarding_number = PhoneNumberField(
        help_text="Heavenly Hands main number: +13525811245"
    )
    campaign_type = models.CharField(
        max_length=50,
        choices=[
            ("google_ads", "Google Ads"),
            ("facebook", "Facebook"),
            ("yelp", "Yelp"),
            ("referral", "Referral"),
            ("direct", "Direct"),
            ("other", "Other"),
        ],
        default="other",
    )
    service_area = models.CharField(
        max_length=50,
        choices=[
            ("gainesville", "Gainesville"),
            ("ocala", "Ocala"),
            ("alachua", "Alachua"),
            ("high_springs", "High Springs"),
            ("newberry", "Newberry"),
            ("micanopy", "Micanopy"),
            ("all", "All Areas"),
        ],
        default="gainesville",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = HeavenlyHandsLeadSourceManager()

    def __str__(self):
        if self.name:
            return f"{self.name} - {self.incoming_number}"
        else:
            return f"(not yet named) - {self.incoming_number}"

class HeavenlyHandsLeadManager(models.Manager):
    """Custom manager for Heavenly Hands leads"""

    def get_leads_per_city(self):
        """Get the number of leads for each city"""
        from django.db.models import Count
        queryset = self.all().values("city").annotate(Count("id")).order_by("city")
        data = list(queryset.values("city", "id__count"))
        return data

    def get_leads_per_service_type(self):
        """Get leads by service type"""
        from django.db.models import Count
        queryset = (
            self.all()
            .values("service_type")
            .annotate(Count("id"))
            .order_by("service_type")
        )
        data = list(queryset.values("service_type", "id__count"))
        return data

    def get_booking_conversions(self):
        """Get booking conversion statistics"""
        total_leads = self.count()
        successful_bookings = self.filter(booking_made=True).count()
        conversion_rate = (
            (successful_bookings / total_leads * 100) if total_leads > 0 else 0
        )

        return {
            "total_leads": total_leads,
            "successful_bookings": successful_bookings,
            "conversion_rate": round(conversion_rate, 2),
        }

class HeavenlyHandsLead(models.Model):
    """Lead model for Heavenly Hands cleaning service"""

    source = models.ForeignKey(HeavenlyHandsLeadSource, on_delete=models.CASCADE)
    phone_number = PhoneNumberField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # Customer information
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, default="FL")
    customer_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)

    # Service information
    service_type = models.CharField(
        max_length=50,
        choices=[
            ("residential", "Residential Cleaning"),
            ("commercial", "Commercial Cleaning"),
            ("airbnb", "Airbnb Turnover"),
            ("move_in_out", "Move-in/Move-out"),
            ("deep_clean", "Deep Cleaning"),
            ("recurring", "Recurring Service"),
            ("one_time", "One-time Service"),
        ],
        default="residential",
    )

    # Call outcome
    call_duration = models.IntegerField(default=0)  # in seconds
    call_outcome = models.CharField(
        max_length=50,
        choices=[
            ("interested", "Interested"),
            ("not_interested", "Not Interested"),
            ("callback_requested", "Callback Requested"),
            ("price_too_high", "Price Too High"),
            ("already_has_service", "Already Has Service"),
            ("no_answer", "No Answer"),
            ("busy", "Busy"),
        ],
        default="interested",
    )

    # Booking information
    booking_made = models.BooleanField(default=False)
    booking_date = models.DateTimeField(null=True, blank=True)
    estimated_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    # Follow-up information
    follow_up_needed = models.BooleanField(default=False)
    follow_up_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    objects = HeavenlyHandsLeadManager()

    def __str__(self):
        return f'{self.customer_name or "Unknown"} - {self.city}, {self.state} at {self.timestamp}'
''',

        'heavenly_hands_call_tracking/admin.py': '''from django.contrib import admin
from .models import HeavenlyHandsLeadSource, HeavenlyHandsLead

@admin.register(HeavenlyHandsLeadSource)
class HeavenlyHandsLeadSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'incoming_number', 'forwarding_number', 'campaign_type', 'service_area', 'is_active']
    list_filter = ['campaign_type', 'service_area', 'is_active']
    search_fields = ['name', 'incoming_number']
    ordering = ['-created_at']

@admin.register(HeavenlyHandsLead)
class HeavenlyHandsLeadAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'phone_number', 'city', 'service_type', 'call_outcome', 'booking_made', 'timestamp']
    list_filter = ['service_type', 'call_outcome', 'booking_made', 'source']
    search_fields = ['customer_name', 'phone_number', 'city']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp']
''',

        'heavenly_hands_call_tracking/views.py': '''import os
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import requests
from django.db import models
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from phonenumber_field.modelfields import PhoneNumberField
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import models
from .models import HeavenlyHandsLeadSource, HeavenlyHandsLead

class HeavenlyHandsCallTracker:
    """Main call tracking system for Heavenly Hands"""

    def __init__(self):
        self.twilio_client = Client(
            os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN")
        )
        self.main_number = "+13525811245"  # Heavenly Hands main number

    def handle_incoming_call(
        self, lead_source_name: str, from_number: str, city: str, state: str
    ) -> HttpResponse:
        """Handle incoming call and create lead"""
        try:
            # Find the lead source
            lead_source = HeavenlyHandsLeadSource.objects.get(
                name__icontains=lead_source_name.replace("_", " ")
            )

            # Create lead record
            lead = HeavenlyHandsLead.objects.create(
                source=lead_source, phone_number=from_number, city=city, state=state
            )

            logger.info(f"Created lead {lead.id} from {lead_source.name}")

            # Forward call to Heavenly Hands main number
            response = VoiceResponse()
            response.say(
                "Thank you for calling Heavenly Hands Cleaning Service. "
                "Please hold while we connect you to our team.",
                voice="Polly.Joanna",
            )
            response.dial(lead_source.forwarding_number)

            return HttpResponse(str(response), content_type="text/xml")

        except HeavenlyHandsLeadSource.DoesNotExist:
            logger.error(f"Lead source not found: {lead_source_name}")
            response = VoiceResponse()
            response.say("Thank you for calling Heavenly Hands Cleaning Service.")
            response.dial(self.main_number)
            return HttpResponse(str(response), content_type="text/xml")

        except Exception as e:
            logger.error(f"Error handling incoming call: {e}")
            response = VoiceResponse()
            response.say("Thank you for calling Heavenly Hands Cleaning Service.")
            response.dial(self.main_number)
            return HttpResponse(str(response), content_type="text/xml")

# Django Views
@csrf_exempt
def webhook_voice(request, lead_source_name):
    """Handle incoming voice calls"""
    from_number = request.POST.get("From")
    city = request.POST.get("FromCity", "Unknown")
    state = request.POST.get("FromState", "FL")

    tracker = HeavenlyHandsCallTracker()
    return tracker.handle_incoming_call(lead_source_name, from_number, city, state)

def api_leads_by_source(request):
    """API endpoint for leads by source"""
    data = HeavenlyHandsLeadSource.objects.get_leads_per_source()
    return JsonResponse(data, safe=False)

def api_leads_by_city(request):
    """API endpoint for leads by city"""
    data = HeavenlyHandsLead.objects.get_leads_per_city()
    return JsonResponse(data, safe=False)

def api_conversion_rates(request):
    """API endpoint for conversion rates"""
    data = HeavenlyHandsLeadSource.objects.get_conversion_rates()
    return JsonResponse(data, safe=False)

def api_recent_leads(request):
    """API endpoint for recent leads"""
    recent_leads = HeavenlyHandsLead.objects.select_related("source").order_by(
        "-timestamp"
    )[:20]
    data = []
    for lead in recent_leads:
        data.append(
            {
                "id": lead.id,
                "customer_name": lead.customer_name or "Unknown",
                "phone_number": str(lead.phone_number),
                "city": lead.city,
                "service_type": lead.service_type,
                "source_name": lead.source.name,
                "timestamp": lead.timestamp.isoformat(),
                "booking_made": lead.booking_made,
                "call_outcome": lead.call_outcome,
            }
        )
    return JsonResponse(data, safe=False)

def api_analytics(request):
    """API endpoint for comprehensive analytics"""
    try:
        # Lead source statistics
        leads_per_source = HeavenlyHandsLeadSource.objects.get_leads_per_source()
        conversion_rates = HeavenlyHandsLeadSource.objects.get_conversion_rates()

        # Lead statistics
        leads_per_city = HeavenlyHandsLead.objects.get_leads_per_city()
        leads_per_service = HeavenlyHandsLead.objects.get_leads_per_service_type()
        booking_conversions = HeavenlyHandsLead.objects.get_booking_conversions()

        # Recent leads
        recent_leads = HeavenlyHandsLead.objects.select_related("source").order_by(
            "-timestamp"
        )[:10]
        recent_leads_data = []
        for lead in recent_leads:
            recent_leads_data.append(
                {
                    "id": lead.id,
                    "customer_name": lead.customer_name or "Unknown",
                    "phone_number": str(lead.phone_number),
                    "city": lead.city,
                    "service_type": lead.service_type,
                    "source_name": lead.source.name,
                    "timestamp": lead.timestamp.isoformat(),
                    "booking_made": lead.booking_made,
                    "call_outcome": lead.call_outcome,
                }
            )

        return JsonResponse({
            "leads_per_source": leads_per_source,
            "conversion_rates": conversion_rates,
            "leads_per_city": leads_per_city,
            "leads_per_service": leads_per_service,
            "booking_conversions": booking_conversions,
            "recent_leads": recent_leads_data,
        })

    except Exception as e:
        logger.error(f"Error getting analytics data: {e}")
        return JsonResponse({"error": str(e)}, status=500)
''',

        'heavenly_hands_call_tracking/migrations/__init__.py': '',
    }

    try:
        for file_path, content in django_structure.items():
            full_path = project_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)

            with open(full_path, 'w') as f:
                f.write(content)

            # Make manage.py executable
            if file_path == 'manage.py':
                os.chmod(full_path, 0o755)

        print("✅ Django project structure created")
        return True

    except Exception as e:
        print(f"❌ Failed to create Django project: {e}")
        return False

def run_django_setup():
    """Run Django setup commands"""
    print("\n🚀 Running Django setup...")

    project_dir = Path('/Users/steven/ai-sites/heavenlyHands')

    try:
        # Change to project directory
        os.chdir(project_dir)

        # Run migrations
        print("   Running migrations...")
        subprocess.run([sys.executable, 'manage.py', 'makemigrations'],
                     check=True, capture_output=True)
        subprocess.run([sys.executable, 'manage.py', 'migrate'],
                     check=True, capture_output=True)

        # Create superuser (optional)
        print("   Creating superuser...")
        subprocess.run([
            sys.executable, 'manage.py', 'createsuperuser',
            '--username', 'admin',
            '--email', 'admin@heavenlyhands.com',
            '--noinput'
        ], check=True, capture_output=True)

        print("✅ Django setup completed")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Django setup failed: {e}")
        return False

def create_sample_data():
    """Create sample data for testing"""
    print("\n📝 Creating sample data...")

    sample_data_script = '''
import os
import sys
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
sys.path.append("/Users/steven/ai-sites/heavenlyHands")
django.setup()

from heavenly_hands_call_tracking.models import HeavenlyHandsLeadSource, HeavenlyHandsLead

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
        print(f"Created lead source: {source.name}")

# Create sample leads
sample_leads = [
    {
        "source": HeavenlyHandsLeadSource.objects.get(name="Google Ads Gainesville"),
        "phone_number": "+13525551237",
        "city": "Gainesville",
        "state": "FL",
        "customer_name": "John Smith",
        "service_type": "residential",
        "call_outcome": "interested",
        "booking_made": True,
    },
    {
        "source": HeavenlyHandsLeadSource.objects.get(name="Facebook Ocala"),
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
        print(f"Created lead: {lead.customer_name}")

print("Sample data created successfully!")
'''

    try:
        with open('/tmp/create_sample_data.py', 'w') as f:
            f.write(sample_data_script)

        subprocess.run([sys.executable, '/tmp/create_sample_data.py'],
                      check=True, capture_output=True)

        print("✅ Sample data created")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Sample data creation failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🏠 Heavenly Hands Call Tracking - Complete Setup")
    print("=" * 60)

    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        return False

    # Setup Django project
    if not setup_django_project():
        print("❌ Setup failed at Django project creation")
        return False

    # Run Django setup
    if not run_django_setup():
        print("❌ Setup failed at Django setup")
        return False

    # Create sample data
    if not create_sample_data():
        print("❌ Setup failed at sample data creation")
        return False

    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Source your environment: source ~/.env.d/loader.sh")
    print("2. Test Twilio connection: python test_twilio_connection.py")
    print("3. Start development server: python manage.py runserver")
    print("4. Access admin panel: http://localhost:8000/admin/")
    print("5. View API endpoints: http://localhost:8000/")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
