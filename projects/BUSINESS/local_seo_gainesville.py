#!/usr/bin/env python3
"""Local SEO Lead Generator - Gainesville & Ocala, Florida"""
import os, sys, json, csv
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent / 'leads' / 'gainesville-ocala'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Gainesville & Ocala ZIP codes and neighborhoods
GAINESVILLE_AREAS = {
    'Downtown Gainesville': ['32601', '32602'],
    'University/UF Area': ['32603', '32611'],
    'Northwest Gainesville': ['32606', '32605'],
    'Southwest Gainesville': ['32607', '32608'],
    'Newberry': ['32669'],
    'Alachua': ['32615'],
    'High Springs': ['32643'],
    'Archer': ['32618']
}

OCALA_AREAS = {
    'Downtown Ocala': ['34470', '34471'],
    'Silver Springs': ['34488'],
    'Belleview': ['34420'],
    'Dunnellon': ['34432', '34433', '34434'],
    'The Villages (Marion)': ['32162', '32163']
}

# High-value industries for Florida market
FLORIDA_INDUSTRIES = {
    'dentist': {
        'avg_ticket': 500,
        'priority': 'high',
        'search_terms': ['dentist', 'dental office', 'family dentistry', 'cosmetic dentist'],
        'pain_points': 'New patients needed, missed calls lose $500+ appointments'
    },
    'plumber': {
        'avg_ticket': 400,
        'priority': 'high',
        'search_terms': ['plumber', 'plumbing service', 'emergency plumber'],
        'pain_points': 'Emergency calls = big revenue, can\'t afford to miss 3am calls'
    },
    'hvac': {
        'avg_ticket': 600,
        'priority': 'high',
        'search_terms': ['hvac', 'air conditioning', 'ac repair', 'heating cooling'],
        'pain_points': 'Florida heat = emergency calls, peak season overwhelm'
    },
    'roofer': {
        'avg_ticket': 1200,
        'priority': 'high',
        'search_terms': ['roofer', 'roofing contractor', 'roof repair'],
        'pain_points': 'Storm season leads, insurance claims, high-ticket jobs'
    },
    'lawn care': {
        'avg_ticket': 150,
        'priority': 'medium',
        'search_terms': ['lawn care', 'landscaping', 'lawn service', 'tree service'],
        'pain_points': 'Year-round growth in FL, recurring revenue model'
    },
    'auto repair': {
        'avg_ticket': 300,
        'priority': 'medium',
        'search_terms': ['auto repair', 'mechanic', 'car repair'],
        'pain_points': 'Appointment booking, estimates, customer communication'
    },
    'real estate': {
        'avg_ticket': 5000,
        'priority': 'high',
        'search_terms': ['real estate agent', 'realtor', 'realty'],
        'pain_points': '24/7 lead capture, buyer/seller qualification, showings'
    },
    'chiropractor': {
        'avg_ticket': 200,
        'priority': 'medium',
        'search_terms': ['chiropractor', 'chiropractic'],
        'pain_points': 'New patient booking, insurance verification'
    },
    'hair salon': {
        'avg_ticket': 80,
        'priority': 'medium',
        'search_terms': ['hair salon', 'beauty salon', 'barber shop'],
        'pain_points': 'Appointment booking, cancellations, after-hours calls'
    },
    'lawyer': {
        'avg_ticket': 1500,
        'priority': 'high',
        'search_terms': ['lawyer', 'attorney', 'law firm', 'legal'],
        'pain_points': 'Lead qualification, consultation booking, 24/7 availability'
    }
}

def generate_local_leads_manual(industry, area='gainesville', limit=20):
    """Generate leads list for manual Google Maps search"""

    industry_data = FLORIDA_INDUSTRIES.get(industry, {})
    search_terms = industry_data.get('search_terms', [industry])

    areas = GAINESVILLE_AREAS if area.lower() == 'gainesville' else OCALA_AREAS

    leads = []
    search_queries = []

    for neighborhood, zip_codes in areas.items():
        for term in search_terms[:2]:  # Top 2 search terms
            query = f"{term} {neighborhood} Florida"
            search_queries.append({
                'query': query,
                'gmaps_url': f"https://www.google.com/maps/search/{query.replace(' ', '+')}",
                'neighborhood': neighborhood,
                'zip_codes': ', '.join(zip_codes)
            })

    # Create search guide
    guide = f"""# Local Lead Generation Guide
## {industry.title()} businesses in {area.title()}, FL

### Search Queries ({len(search_queries)} total):

"""

    for i, sq in enumerate(search_queries, 1):
        guide += f"{i}. **{sq['query']}**\n"
        guide += f"   - Google Maps: {sq['gmaps_url']}\n"
        guide += f"   - Area: {sq['neighborhood']} ({sq['zip_codes']})\n\n"

    guide += """
### Manual Lead Gathering Process:

1. **Click each Google Maps link above**
2. **For each business, collect:**
   - Business name
   - Phone number
   - Website (if available)
   - Address
   - Rating (stars)
   - Number of reviews
   - Notes (hours, busy times, etc.)

3. **Scoring (Priority):**
   - ⭐⭐⭐ HIGH: Has phone + 3.0-3.8 rating + 50+ reviews
   - ⭐⭐ MEDIUM: Has phone + any rating + 20+ reviews
   - ⭐ LOW: No phone OR <3.0 rating OR <20 reviews

4. **Add to spreadsheet:**
   - Use template: leads_template.csv

5. **Generate pitches:**
   - Run: python3 generate_pitch.py leads.csv

### Why These Searches?

"""

    for neighborhood in areas.keys():
        guide += f"- **{neighborhood}:** Local market, less competition, community-focused\n"

    guide += f"""
### Industry Insights: {industry.title()}

- **Average Ticket:** ${industry_data.get('avg_ticket', 300)}
- **Pain Points:** {industry_data.get('pain_points', 'Missed calls = lost revenue')}
- **Your Pitch:** "You're losing ${industry_data.get('avg_ticket', 300) * 8}/month from just 40% missed calls"

### Next Steps:

1. **Gather 50 leads** (2-3 hours of work)
2. **Score them** (HIGH/MED/LOW priority)
3. **Generate personalized pitches**
4. **Start outreach** (email + call top 20)
5. **Close 3-5 clients** in first month

Target: 10 clients × $400 = $4,000/month recurring
"""

    return guide, search_queries


def create_pitch_template(business_name, industry, city, phone='', website='', rating='N/A', reviews=0):
    """Create personalized pitch for Gainesville/Ocala business"""

    industry_data = FLORIDA_INDUSTRIES.get(industry, {})
    avg_ticket = industry_data.get('avg_ticket', 300)
    pain_points = industry_data.get('pain_points', '')

    # Calculate potential
    calls_per_day = 12 if reviews > 50 else 8 if reviews > 20 else 5
    missed_rate = 0.4
    monthly_missed = int(calls_per_day * missed_rate * 30)
    conversion_rate = 0.2
    potential = int(monthly_missed * conversion_rate * avg_ticket)

    pitch = f"""Subject: {business_name} - Losing ${potential:,}/month in {city}?

Hi [Owner/Manager],

I found {business_name} on Google ({reviews} reviews{f', {rating} stars' if rating != 'N/A' else ''}) - great local presence in {city}!

Quick question for {industry} businesses in {city}: What happens when you can't answer the phone during busy hours?

**The Reality:**
- Most {city} {industry} businesses miss 40% of calls
- At your volume ({calls_per_day} calls/day), that's {monthly_missed} missed opportunities monthly
- Potential lost revenue: ${potential:,}/month

**The Solution:**
I help {city}/{('Ocala' if city == 'Gainesville' else 'Gainesville')} businesses capture every lead with AI receptionists that:

✓ Answer 24/7 (nights, weekends, holidays)
✓ Book appointments directly into your calendar
✓ Qualify leads while you're busy with customers
✓ Never put anyone on hold
✓ Sound natural (most callers can't tell it's AI!)

**Local Setup:**
- No setup fee (first 3 {city} businesses)
- Just $300-400/month
- Pays for itself with 1-2 extra appointments
- 7-day free trial

**Florida Focused:**
I work exclusively with {city}/Ocala businesses. I understand our local market, snowbird season, and Florida business needs.

Want to hear it in action? I can have you test our AI receptionist live - just takes 10 minutes.

Free demo?

Best,
Steven Chaplinski
AvaTarArTs AI Solutions
Based in Gainesville/Ocala area
[Phone] | avatararts.org/ai-voice

P.S. - {pain_points}
"""

    return pitch


def create_csv_template():
    """Create CSV template for manual lead entry"""

    template = OUTPUT_DIR / 'leads_template.csv'

    with open(template, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'business_name', 'industry', 'phone', 'website', 'address',
            'city', 'zip', 'rating', 'reviews', 'priority', 'notes'
        ])

        # Add example rows
        writer.writerow([
            'Example Dental', 'dentist', '352-555-1234', 'www.example.com',
            '123 Main St', 'Gainesville', '32601', '3.5', '75', 'HIGH',
            'Busy practice, could use after-hours coverage'
        ])

    return template


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("""Local SEO Lead Generator - Gainesville & Ocala, FL

Usage: local_seo_gainesville.py <industry> [area]

Industries:""")
        for industry, data in FLORIDA_INDUSTRIES.items():
            print(f"  {industry:15s} ${data['avg_ticket']:4d} avg ticket, {data['priority']:6s} priority")

        print("""
Areas: gainesville, ocala (default: gainesville)

Examples:
  local_seo_gainesville.py dentist gainesville
  local_seo_gainesville.py hvac ocala
  local_seo_gainesville.py plumber gainesville

Output:
  - Search guide with Google Maps links
  - Lead gathering instructions
  - CSV template for data entry
  - Pitch generation tools
""")
        sys.exit(1)

    industry = sys.argv[1].lower()
    area = sys.argv[2].lower() if len(sys.argv) > 2 else 'gainesville'

    if industry not in FLORIDA_INDUSTRIES:
        print(f"⚠️  '{industry}' not in pre-configured industries")
        print(f"Available: {', '.join(FLORIDA_INDUSTRIES.keys())}")
        sys.exit(1)

    if area not in ['gainesville', 'ocala']:
        print(f"⚠️  Area must be 'gainesville' or 'ocala'")
        sys.exit(1)

    print(f"🎯 Generating lead searches for {industry} in {area.title()}, FL")
    print("=" * 60)

    # Generate guide
    guide, queries = generate_local_leads_manual(industry, area)

    # Save guide
    timestamp = datetime.now().strftime('%Y%m%d')
    guide_file = OUTPUT_DIR / f'lead_guide_{industry}_{area}_{timestamp}.md'
    guide_file.write_text(guide)

    # Create CSV template
    template_file = create_csv_template()

    # Create sample pitch
    sample_pitch = create_pitch_template(
        business_name=f"{area.title()} {industry.title()} Example",
        industry=industry,
        city=area.title(),
        reviews=75,
        rating='3.8'
    )

    pitch_file = OUTPUT_DIR / f'sample_pitch_{industry}_{area}.txt'
    pitch_file.write_text(sample_pitch)

    print(f"\n✅ Generated {len(queries)} search queries")
    print(f"\n📄 Files created:")
    print(f"   1. Search Guide: {guide_file.name}")
    print(f"   2. CSV Template: {template_file.name}")
    print(f"   3. Sample Pitch: {pitch_file.name}")

    print(f"\n🎯 Next Steps:")
    print(f"   1. Open: {guide_file}")
    print(f"   2. Click Google Maps links (or search manually)")
    print(f"   3. Fill out: {template_file}")
    print(f"   4. Review pitch: {pitch_file}")
    print(f"   5. Start outreach to top 20 leads")

    print(f"\n💡 Target: 50 leads → 10 contacted → 3-5 clients → $1,200-2,000/month!")

    print(f"\n📍 Focusing on {area.title()} gives you:")
    print(f"   - Local credibility (you're nearby)")
    print(f"   - Easy meetings (drive over)")
    print(f"   - Word-of-mouth referrals")
    print(f"   - Dominate local market first")
