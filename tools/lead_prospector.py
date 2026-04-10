"""
Jaybird Automations — Lead Prospector
Finds local businesses using Google Places API that might need AI services.

SETUP:
1. Get a Google Cloud account: https://console.cloud.google.com
2. Enable the "Places API" (new) or "Places API (Legacy)"
3. Create an API key: APIs & Services → Credentials → Create Credentials → API Key
4. Set your key below or as environment variable: GOOGLE_PLACES_API_KEY

USAGE:
  python lead_prospector.py --category "law firm" --city "Las Vegas" --state "NV"
  python lead_prospector.py --category "restaurant" --city "Las Vegas" --state "NV" --radius 20000
  python lead_prospector.py --all-categories --city "Las Vegas" --state "NV"

OUTPUT:
  Creates an Excel file in the output/ folder with all found businesses.
"""

import os
import sys
import time
import json
import argparse
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

# Load .env file automatically
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / '.env')
except ImportError:
    pass

# ─── CONFIG ───────────────────────────────────────────────────────────
API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY', '')

# Default target categories for AI services prospecting
DEFAULT_CATEGORIES = [
    "law firm",
    "restaurant",
    "dental office",
    "medical office",
    "contractor",
    "hair salon",
    "real estate agent",
    "auto repair",
    "accounting firm",
    "insurance agency",
    "veterinarian",
    "gym fitness",
    "spa massage",
    "plumber",
    "electrician",
    "roofing contractor",
    "landscaping",
    "chiropractic",
    "optometrist",
    "pharmacy",
]

# City coordinates for geocoding
CITY_COORDS = {
    "las vegas": {"lat": 36.1699, "lng": -115.1398},
    "henderson": {"lat": 36.0395, "lng": -114.9817},
    "north las vegas": {"lat": 36.1989, "lng": -115.1175},
    "reno": {"lat": 39.5296, "lng": -119.8138},
}

BASE_URL = "https://maps.googleapis.com/maps/api/place"


def search_nearby(query, lat, lng, radius=30000):
    """Search for businesses using Google Places Text Search API."""
    url = f"{BASE_URL}/textsearch/json"
    all_results = []
    params = {
        "query": query,
        "location": f"{lat},{lng}",
        "radius": radius,
        "key": API_KEY,
    }

    while True:
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()

        if data.get("status") not in ("OK", "ZERO_RESULTS"):
            print(f"  API error: {data.get('status')} — {data.get('error_message', '')}")
            break

        all_results.extend(data.get("results", []))
        print(f"  Found {len(data.get('results', []))} results (total: {len(all_results)})")

        # Check for next page
        next_token = data.get("next_page_token")
        if not next_token:
            break

        # Google requires a short delay before using next_page_token
        time.sleep(2)
        params = {"pagetoken": next_token, "key": API_KEY}

    return all_results


def get_place_details(place_id):
    """Get detailed info for a specific place."""
    url = f"{BASE_URL}/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,formatted_phone_number,website,rating,user_ratings_total,types,business_status,opening_hours",
        "key": API_KEY,
    }
    resp = requests.get(url, params=params, timeout=15)
    data = resp.json()
    if data.get("status") == "OK":
        return data.get("result", {})
    return {}


def prospect(categories, city, state, radius=30000):
    """Run prospecting for given categories in a city."""
    city_key = city.lower()
    coords = CITY_COORDS.get(city_key)
    if not coords:
        # Try geocoding with Google
        print(f"City '{city}' not in defaults, using Google Geocoding...")
        geo_url = "https://maps.googleapis.com/maps/api/geocode/json"
        geo_resp = requests.get(geo_url, params={"address": f"{city}, {state}", "key": API_KEY}, timeout=10)
        geo_data = geo_resp.json()
        if geo_data.get("results"):
            loc = geo_data["results"][0]["geometry"]["location"]
            coords = {"lat": loc["lat"], "lng": loc["lng"]}
        else:
            print(f"ERROR: Could not geocode '{city}, {state}'")
            sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  JAYBIRD LEAD PROSPECTOR")
    print(f"  Target: {city}, {state}")
    print(f"  Categories: {len(categories)}")
    print(f"  Radius: {radius/1000:.0f} km")
    print(f"{'='*60}\n")

    all_leads = []
    seen_place_ids = set()

    for category in categories:
        query = f"{category} {city} {state}"
        print(f"\nSearching: {query}")
        results = search_nearby(query, coords["lat"], coords["lng"], radius)

        for place in results:
            pid = place.get("place_id")
            if pid in seen_place_ids:
                continue
            seen_place_ids.add(pid)

            lead = {
                "business_name": place.get("name", ""),
                "industry": category,
                "address": place.get("formatted_address", ""),
                "rating": place.get("rating", 0),
                "review_count": place.get("user_ratings_total", 0),
                "place_id": pid,
                "lat": place.get("geometry", {}).get("location", {}).get("lat", ""),
                "lng": place.get("geometry", {}).get("location", {}).get("lng", ""),
                "business_status": place.get("business_status", ""),
            }

            # Get detailed info (phone, website)
            time.sleep(0.1)  # Be respectful with API calls
            details = get_place_details(pid)
            if details:
                lead["phone"] = details.get("formatted_phone_number", "")
                lead["website"] = details.get("website", "")
                lead["types"] = ", ".join(details.get("types", []))

            all_leads.append(lead)

        # Pause between categories to be respectful
        time.sleep(1)

    return all_leads


def score_lead(lead):
    """Score a lead 1-10 on how likely they need AI services."""
    score = 5  # Base score

    # No website = huge opportunity
    if not lead.get("website"):
        score += 3

    # Low rating = might need help
    rating = lead.get("rating", 0)
    if rating > 0 and rating < 3.5:
        score += 1
    elif rating >= 4.5:
        score -= 1  # They're doing well, harder sell

    # Few reviews = needs visibility
    reviews = lead.get("review_count", 0)
    if reviews < 10:
        score += 1
    elif reviews > 100:
        score -= 1  # Already established

    # Certain industries are better targets
    high_value = ["law firm", "dental office", "medical office", "real estate agent", "accounting firm"]
    if lead.get("industry") in high_value:
        score += 1

    return max(1, min(10, score))


def save_results(leads, city, state, categories=None):
    """Save leads to Excel file."""
    if not leads:
        print("\nNo leads found!")
        return

    # Add lead scores
    for lead in leads:
        lead["lead_score"] = score_lead(lead)

    # Sort by lead score (highest first)
    leads.sort(key=lambda x: x["lead_score"], reverse=True)

    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(output_dir, exist_ok=True)

    # Create DataFrame
    df = pd.DataFrame(leads)

    # Reorder columns
    columns = [
        "lead_score", "business_name", "industry", "phone", "website",
        "address", "rating", "review_count", "business_status", "types",
        "place_id", "lat", "lng"
    ]
    # Only include columns that exist
    columns = [c for c in columns if c in df.columns]
    df = df[columns]

    # Save — build a human-readable filename
    city_clean = city.replace(' ', '_')
    if not categories or len(categories) >= len(DEFAULT_CATEGORIES):
        category_label = "All_Businesses"
    elif len(categories) == 1:
        category_label = categories[0].replace(' ', '_').title()
    else:
        category_label = "_and_".join(c.replace(' ', '_').title() for c in categories[:2])
        if len(categories) > 2:
            category_label += f"_and_{len(categories)-2}_more"

    filename = f"{category_label}_Leads_{city_clean}_{state.upper()}.xlsx"
    filepath = os.path.join(output_dir, filename)

    df.to_excel(filepath, index=False, sheet_name="Leads")
    print(f"\n{'='*60}")
    print(f"  RESULTS SAVED!")
    print(f"  Total leads: {len(leads)}")
    print(f"  High priority (score 7+): {len([l for l in leads if l['lead_score'] >= 7])}")
    print(f"  File: {filepath}")
    print(f"{'='*60}")

    return filepath


def main():
    parser = argparse.ArgumentParser(description="Jaybird Lead Prospector — Find businesses that need AI services")
    parser.add_argument("--category", type=str, help="Business category to search (e.g., 'law firm')")
    parser.add_argument("--all-categories", action="store_true", help="Search all default categories")
    parser.add_argument("--city", type=str, default="Las Vegas", help="Target city (default: Las Vegas)")
    parser.add_argument("--state", type=str, default="NV", help="Target state (default: NV)")
    parser.add_argument("--radius", type=int, default=30000, help="Search radius in meters (default: 30000)")
    args = parser.parse_args()

    if API_KEY == "YOUR_API_KEY_HERE":
        print("ERROR: Set your Google Places API key!")
        print("  Option 1: Set environment variable GOOGLE_PLACES_API_KEY")
        print("  Option 2: Edit the API_KEY variable in this script")
        print("\nGet a free key at: https://console.cloud.google.com")
        print("  1. Enable 'Places API'")
        print("  2. Create an API key under 'Credentials'")
        print("  3. Google gives $200/month free credit!")
        sys.exit(1)

    if args.all_categories:
        categories = DEFAULT_CATEGORIES
    elif args.category:
        categories = [args.category]
    else:
        print("ERROR: Specify --category 'law firm' or --all-categories")
        sys.exit(1)

    leads = prospect(categories, args.city, args.state, args.radius)
    save_results(leads, args.city, args.state, categories)


if __name__ == "__main__":
    main()
