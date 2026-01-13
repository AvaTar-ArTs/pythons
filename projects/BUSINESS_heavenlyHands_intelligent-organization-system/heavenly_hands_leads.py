#!/usr/bin/env python3
"""
Heavenly Hands Lead Generation Script
=====================================

Automated lead generation and phone outreach for Heavenly Hands Cleaning Service
"""

import os
import json
from enhanced_creative_automation import EnhancedIntelligentOrganizationSystem
from dotenv import load_dotenv

load_dotenv()

def main():
    """Main lead generation function"""
    print("🏠 Heavenly Hands Lead Generation System")
    print("=" * 50)
    
    # Initialize enhanced system
    system = EnhancedIntelligentOrganizationSystem()
    
    # Sample lead data (in production, this would come from CRM, website forms, etc.)
    leads = [
        {
            'name': 'John Smith',
            'phone': '+1234567890',
            'email': 'john@example.com',
            'service_interest': 'residential cleaning',
            'source': 'website_form',
            'notes': 'Interested in weekly cleaning for 3-bedroom home'
        },
        {
            'name': 'Sarah Johnson',
            'phone': '+1234567891',
            'email': 'sarah@example.com',
            'service_interest': 'commercial cleaning',
            'source': 'google_ads',
            'notes': 'Office building, 5000 sq ft, needs daily cleaning'
        },
        {
            'name': 'Mike Davis',
            'phone': '+1234567892',
            'email': 'mike@example.com',
            'service_interest': 'move-in cleaning',
            'source': 'referral',
            'notes': 'Moving into new house next week'
        }
    ]
    
    print(f"📋 Processing {len(leads)} leads...")
    
    # Create phone campaign
    phone_numbers = [lead['phone'] for lead in leads]
    campaign_id = system.creative_automation.create_phone_campaign(
        "Heavenly Hands Lead Generation Campaign",
        phone_numbers
    )
    
    print(f"✅ Phone campaign created: {campaign_id}")
    
    # Store leads in database
    for lead in leads:
        system.creative_automation._save_lead(lead)
    
    print("✅ Leads stored in database")
    
    # Create follow-up workflow
    workflow_id = system.agentic_workflows.create_creative_workflow(
        "Heavenly Hands Customer Follow-up",
        {
            'business_type': 'cleaning_service',
            'leads': leads,
            'follow_up_sequence': [
                'initial_call',
                'email_sequence',
                'social_media_engagement',
                'scheduling_consultation'
            ]
        }
    )
    
    print(f"✅ Follow-up workflow created: {workflow_id}")
    
    print("\n🎯 Next Steps:")
    print("1. Update Twilio credentials in .env file")
    print("2. Start the webhook server: python heavenly_hands_webhook.py")
    print("3. Execute the phone campaign")
    print("4. Monitor results and optimize")

if __name__ == "__main__":
    main()
