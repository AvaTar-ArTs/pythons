#!/usr/bin/env python3
"""AI Voice Agent Lead Generator - Find local businesses via Google Maps"""
import os, sys, json, csv, requests
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent / 'leads'
OUTPUT_DIR.mkdir(exist_ok=True)

# Load API key from .env.d
sys.path.insert(0, str(Path.home() / '.env.d'))
try:
    from loader import load_env
    load_env()
except:
    pass

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')

# High-value target industries
TARGET_INDUSTRIES = {
    'dentist': {'avg_ticket': 500, 'priority': 'high'},
    'plumber': {'avg_ticket': 400, 'priority': 'high'},
    'electrician': {'avg_ticket': 350, 'priority': 'high'},
    'hvac': {'avg_ticket': 600, 'priority': 'high'},
    'hair salon': {'avg_ticket': 80, 'priority': 'medium'},
    'real estate agent': {'avg_ticket': 5000, 'priority': 'high'},
    'lawyer': {'avg_ticket': 1500, 'priority': 'high'},
    'chiropractor': {'avg_ticket': 200, 'priority': 'medium'},
    'auto repair': {'avg_ticket': 300, 'priority': 'medium'},
    'contractor': {'avg_ticket': 800, 'priority': 'high'},
    'roofing': {'avg_ticket': 1200, 'priority': 'high'},
    'landscaping': {'avg_ticket': 250, 'priority': 'medium'}
}

def search_google_maps(query, location, radius=5000, max_results=20):
    """Search Google Maps for businesses"""

    if not GOOGLE_MAPS_API_KEY:
        print("⚠️  Google Maps API key not found in .env.d/other-tools.env")
        print("   Add: GOOGLE_MAPS_API_KEY=your_key_here")
        return []

    # Geocode location first
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json"
    geocode_params = {
        'address': location,
        'key': GOOGLE_MAPS_API_KEY
    }

    try:
        response = requests.get(geocode_url, params=geocode_params)
        geo_data = response.json()

        if geo_data['status'] != 'OK':
            print(f"❌ Geocoding failed: {geo_data['status']}")
            return []

        lat = geo_data['results'][0]['geometry']['location']['lat']
        lng = geo_data['results'][0]['geometry']['location']['lng']

    except Exception as e:
        print(f"❌ Geocoding error: {e}")
        return []

    # Search nearby places
    search_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    search_params = {
        'location': f"{lat},{lng}",
        'radius': radius,
        'keyword': query,
        'key': GOOGLE_MAPS_API_KEY
    }

    results = []

    try:
        response = requests.get(search_url, params=search_params)
        data = response.json()

        if data['status'] != 'OK':
            print(f"⚠️  Search returned: {data['status']}")
            return []

        for place in data['results'][:max_results]:
            # Get place details
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                'place_id': place['place_id'],
                'fields': 'name,formatted_phone_number,website,rating,user_ratings_total,formatted_address,opening_hours',
                'key': GOOGLE_MAPS_API_KEY
            }

            details_response = requests.get(details_url, params=details_params)
            details_data = details_response.json()

            if details_data['status'] == 'OK':
                result = details_data['result']
                results.append({
                    'name': result.get('name'),
                    'phone': result.get('formatted_phone_number', 'N/A'),
                    'website': result.get('website', 'N/A'),
                    'address': result.get('formatted_address', 'N/A'),
                    'rating': result.get('rating', 'N/A'),
                    'reviews': result.get('user_ratings_total', 0),
                    'place_id': place['place_id'],
                    'lat': place['geometry']['location']['lat'],
                    'lng': place['geometry']['location']['lng']
                })

        return results

    except Exception as e:
        print(f"❌ Search error: {e}")
        return []

def score_lead(business, industry_key):
    """Score lead quality (1-10)"""
    score = 5  # Base score

    # Phone number (essential)
    if business['phone'] != 'N/A':
        score += 2
    else:
        score -= 3

    # Website (can scrape for AI training)
    if business['website'] != 'N/A':
        score += 1

    # Rating (lower = more pain, but too low = risky)
    rating = business.get('rating', 0)
    if rating == 'N/A' or rating == 0:
        score += 0
    elif 3.0 <= rating < 3.8:
        score += 2  # Sweet spot - needs help
    elif rating < 3.0:
        score -= 1  # Too risky
    else:
        score += 1  # Good but may not need help

    # Reviews (more = busier = more missed calls)
    reviews = business.get('reviews', 0)
    if reviews > 100:
        score += 2
    elif reviews > 50:
        score += 1

    # Industry priority
    industry_data = TARGET_INDUSTRIES.get(industry_key, {})
    if industry_data.get('priority') == 'high':
        score += 1

    return min(10, max(1, score))

def generate_pitch(business, industry):
    """Generate personalized pitch"""
    name = business['name']
    rating = business.get('rating', 'N/A')
    reviews = business.get('reviews', 0)

    industry_data = TARGET_INDUSTRIES.get(industry, {})
    avg_ticket = industry_data.get('avg_ticket', 300)

    # Calculate potential revenue
    estimated_calls_per_day = 10 if reviews > 50 else 5
    missed_calls = int(estimated_calls_per_day * 0.4)  # 40% miss rate
    monthly_missed = missed_calls * 30
    conversion_rate = 0.2
    potential_revenue = int(monthly_missed * conversion_rate * avg_ticket)

    pitch = f"""Subject: {name} - Are you losing ${potential_revenue:,}/month?

Hi [Owner/Manager],

I found {name} on Google Maps ({reviews} reviews, {rating} stars - nice!).

Quick question: What happens to calls when you're busy or after hours?

Most {industry} businesses miss 40% of incoming calls. At your volume, that could be ${potential_revenue:,}+ in lost revenue monthly.

I help businesses like yours capture every lead with AI receptionists that:
✓ Answer 24/7 (nights, weekends, holidays)
✓ Book appointments directly into your calendar
✓ Qualify leads while you focus on serviced
✓ Never put anyone on hold

Setup is free. Just $300-400/month.
Pays for itself with 1 extra booking.

Want to hear how it sounds? I'll call you back with our AI so you can test it live.

Interested in 15-min demo?

Best,
Steven Chaplinski
AvaTarArTs AI Solutions
[Phone] | avatararts.org"""

    return pitch, potential_revenue

def export_leads(leads, industry, location):
    """Export leads to CSV"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    csv_file = OUTPUT_DIR / f'leads_{industry.replace(" ", "_")}_{location.replace(" ", "_")}_{timestamp}.csv'

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'name', 'phone', 'website', 'address', 'rating', 'reviews',
            'score', 'potential_revenue', 'industry', 'pitch_subject',
            'contacted', 'status', 'notes'
        ])
        writer.writeheader()
        writer.writerows(leads)

    return csv_file

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("""AI Voice Agent Lead Generator

Usage: lead_generator.py <industry> <location> [radius_miles]

Industries:
""")
        for industry, data in TARGET_INDUSTRIES.items():
            print(f"  - {industry:20s} (avg ticket: ${data['avg_ticket']}, priority: {data['priority']})")

        print("""
Examples:
  lead_generator.py dentist "Austin, TX" 5
  lead_generator.py plumber "Phoenix, AZ" 10
  lead_generator.py "hair salon" "Miami, FL"

Requires: GOOGLE_MAPS_API_KEY in ~/.env.d/other-tools.env
""")
        sys.exit(1)

    industry = sys.argv[1].lower()
    location = sys.argv[2]
    radius_miles = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    radius_meters = radius_miles * 1609  # Convert to meters

    if industry not in TARGET_INDUSTRIES:
        print(f"⚠️  '{industry}' not in predefined industries, but searching anyway...")

    print(f"🔍 Searching for {industry} businesses in {location}")
    print(f"   Radius: {radius_miles} miles")
    print("=" * 60)

    # Search
    results = search_google_maps(industry, location, radius=radius_meters, max_results=20)

    if not results:
        print("❌ No results found")
        sys.exit(1)

    print(f"✅ Found {len(results)} businesses\n")

    # Score and prepare leads
    leads = []
    for business in results:
        score = score_lead(business, industry)
        pitch, potential_revenue = generate_pitch(business, industry)

        lead = {
            'name': business['name'],
            'phone': business['phone'],
            'website': business['website'],
            'address': business['address'],
            'rating': business.get('rating', 'N/A'),
            'reviews': business.get('reviews', 0),
            'score': score,
            'potential_revenue': potential_revenue,
            'industry': industry,
            'pitch_subject': pitch.split('\n')[0].replace('Subject: ', ''),
            'contacted': 'No',
            'status': 'New Lead',
            'notes': ''
        }

        leads.append(lead)

        # Print preview
        print(f"📍 {business['name']}")
        print(f"   Score: {score}/10 | Phone: {business['phone']} | Reviews: {business.get('reviews', 0)}")
        print(f"   Potential: ${potential_revenue:,}/month")
        print()

    # Sort by score
    leads.sort(key=lambda x: x['score'], reverse=True)

    # Export
    csv_file = export_leads(leads, industry, location)

    # Save pitches
    pitches_file = OUTPUT_DIR / f'pitches_{industry.replace(" ", "_")}_{datetime.now().strftime("%Y%m%d_%H%M")}.txt'
    with open(pitches_file, 'w') as f:
        for i, business in enumerate(results, 1):
            pitch, _ = generate_pitch(business, industry)
            f.write(f"=== Lead {i}: {business['name']} ===\n\n")
            f.write(pitch)
            f.write("\n\n" + "="*60 + "\n\n")

    print("=" * 60)
    print(f"✅ Generated {len(leads)} leads")
    print(f"📄 CSV: {csv_file}")
    print(f"📧 Pitches: {pitches_file}")
    print(f"\n💡 Top 3 leads:")
    for i, lead in enumerate(leads[:3], 1):
        print(f"  {i}. {lead['name']} (Score: {lead['score']}/10, ${lead['potential_revenue']:,}/mo potential)")

    print(f"\n🎯 Next: Review CSV, start outreach to top-scored leads!")
