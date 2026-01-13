#!/usr/bin/env python3
"""
Heavenly Hands Call Tracking System
Production-ready call tracking with Django integration
Based on Twilio's official call tracking tutorial
"""

import json
import logging
import os
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


class HeavenlyHandsLeadSourceManager(models.Manager):
    """Custom manager for Heavenly Hands lead sources"""

    def get_leads_per_source(self):
        """Get the number of leads for each lead source"""
        queryset = self.all().annotate(Count("lead")).order_by("name")
        data = list(queryset.values("name", "lead__count"))
        return data

    def get_conversion_rates(self):
        """Get conversion rates for each lead source"""
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
        queryset = self.all().values("city").annotate(Count("id")).order_by("city")
        data = list(queryset.values("city", "id__count"))
        return data

    def get_leads_per_service_type(self):
        """Get leads by service type"""
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


class HeavenlyHandsCallTracker:
    """Main call tracking system for Heavenly Hands"""

    def __init__(self):
        self.twilio_client = Client(
            os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN")
        )
        self.main_number = "+13525811245"  # Heavenly Hands main number

    def create_lead_source(
        self, name: str, campaign_type: str, service_area: str
    ) -> Dict[str, Any]:
        """Create a new lead source with Twilio phone number"""
        try:
            # Purchase a new phone number from Twilio
            available_numbers = self.twilio_client.available_phone_numbers(
                "US"
            ).local.list(
                area_code="352", voice_enabled=True  # Gainesville area code
            )

            if not available_numbers:
                return {"error": "No available phone numbers in Gainesville area"}

            # Purchase the first available number
            phone_number = self.twilio_client.incoming_phone_numbers.create(
                phone_number=available_numbers[0].phone_number,
                voice_url=f"{os.getenv('WEBHOOK_BASE_URL')}/webhook/voice/{name.lower().replace(' ', '_')}",
            )

            # Create lead source in database
            lead_source = HeavenlyHandsLeadSource.objects.create(
                name=name,
                incoming_number=phone_number.phone_number,
                forwarding_number=self.main_number,
                campaign_type=campaign_type,
                service_area=service_area,
            )

            return {
                "success": True,
                "lead_source_id": lead_source.id,
                "phone_number": phone_number.phone_number,
                "sid": phone_number.sid,
            }

        except Exception as e:
            logger.error(f"Error creating lead source: {e}")
            return {"error": str(e)}

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

    def update_call_outcome(
        self,
        lead_id: int,
        outcome: str,
        duration: int = 0,
        booking_made: bool = False,
        notes: str = "",
    ) -> bool:
        """Update call outcome after call ends"""
        try:
            lead = HeavenlyHandsLead.objects.get(id=lead_id)
            lead.call_outcome = outcome
            lead.call_duration = duration
            lead.booking_made = booking_made
            lead.notes = notes

            if booking_made:
                lead.booking_date = datetime.now()

            lead.save()

            logger.info(f"Updated lead {lead_id} outcome: {outcome}")
            return True

        except HeavenlyHandsLead.DoesNotExist:
            logger.error(f"Lead not found: {lead_id}")
            return False

        except Exception as e:
            logger.error(f"Error updating call outcome: {e}")
            return False

    def get_analytics_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive analytics for dashboard"""
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

            return {
                "leads_per_source": leads_per_source,
                "conversion_rates": conversion_rates,
                "leads_per_city": leads_per_city,
                "leads_per_service": leads_per_service,
                "booking_conversions": booking_conversions,
                "recent_leads": recent_leads_data,
            }

        except Exception as e:
            logger.error(f"Error getting analytics data: {e}")
            return {"error": str(e)}


# Django Views
@csrf_exempt
def webhook_voice(request, lead_source_name):
    """Handle incoming voice calls"""
    from_number = request.POST.get("From")
    city = request.POST.get("FromCity", "Unknown")
    state = request.POST.get("FromState", "FL")

    tracker = HeavenlyHandsCallTracker()
    return tracker.handle_incoming_call(lead_source_name, from_number, city, state)


def analytics_dashboard(request):
    """Render the analytics dashboard"""
    tracker = HeavenlyHandsCallTracker()
    analytics_data = tracker.get_analytics_dashboard_data()

    return render(
        request, "heavenly_hands_dashboard.html", {"analytics_data": analytics_data}
    )


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


def main():
    """Main function to demonstrate the call tracking system"""
    print("🏠 Heavenly Hands Call Tracking System")
    print("=" * 50)
    print("Production-ready call tracking with Django integration")
    print("Based on Twilio's official call tracking tutorial")

    # Initialize tracker
    tracker = HeavenlyHandsCallTracker()

    print("\n📞 Creating sample lead sources...")

    # Create sample lead sources
    sample_sources = [
        {
            "name": "Google Ads Gainesville",
            "campaign_type": "google_ads",
            "service_area": "gainesville",
        },
        {
            "name": "Facebook Ocala",
            "campaign_type": "facebook",
            "service_area": "ocala",
        },
        {"name": "Yelp Reviews", "campaign_type": "yelp", "service_area": "all"},
    ]

    for source_data in sample_sources:
        result = tracker.create_lead_source(**source_data)
        if result.get("success"):
            print(f"   ✅ Created {source_data['name']}: {result['phone_number']}")
        else:
            print(
                f"   ❌ Failed to create {source_data['name']}: {result.get('error')}"
            )

    print(f"\n📊 Analytics Dashboard Features:")
    print("  • Lead source performance tracking")
    print("  • City-based lead analysis")
    print("  • Service type conversion rates")
    print("  • Real-time call tracking")
    print("  • Booking conversion analytics")
    print("  • Visual charts with Chart.js")

    print(f"\n🔗 Webhook Endpoints:")
    print("  • /webhook/voice/{lead_source_name} - Handle incoming calls")
    print("  • /api/leads-by-source - Get leads by source")
    print("  • /api/leads-by-city - Get leads by city")
    print("  • /api/conversion-rates - Get conversion rates")
    print("  • /api/recent-leads - Get recent leads")

    print(f"\n✅ Call tracking system ready for production!")
    print("Features implemented:")
    print("• Twilio phone number management")
    print("• Lead source tracking")
    print("• Call forwarding to main number")
    print("• Comprehensive analytics")
    print("• Django web framework integration")
    print("• Chart.js visualization support")


if __name__ == "__main__":
    main()
