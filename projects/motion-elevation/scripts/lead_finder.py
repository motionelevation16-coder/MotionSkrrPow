#!/usr/bin/env python3
"""
Free Lead Finder
================

Finds potential leads from free sources:
- Google Maps (local businesses)
- Google Search (industry + location)
- Social media profile extraction

No API keys needed for basic operation.
Gemini/Groq API optional for AI enrichment.

Usage:
    python lead_finder.py --source google_maps --query "HVAC" --location "Austin, TX"
    python lead_finder.py --source creators --niche "fitness" --platform instagram
"""

import os
import re
import csv
import json
import argparse
from datetime import datetime
from urllib.parse import quote_plus

# Optional imports
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False


# ============================================
# LEAD TEMPLATES
# ============================================

SEARCH_QUERIES = {
    "local_services": [
        "{service} {location}",
        "{service} near me {location}",
        "best {service} {location}",
    ],
    "creators": [
        "site:instagram.com {niche} creator",
        "site:twitter.com {niche} influencer",
        "site:tiktok.com/@* {niche}",
    ],
    "ecommerce": [
        "site:myshopify.com {niche}",
        "site:etsy.com/shop {niche}",
        "powered by shopify {niche}",
    ],
    "agencies": [
        "{type} agency {location}",
        "site:clutch.co {type} agency",
        "{type} agency for hire",
    ],
}

# ============================================
# FREE EMAIL FINDER (Pattern-based)
# ============================================

def guess_email_patterns(name: str, domain: str) -> list:
    """Generate common email patterns to try"""
    if not name or not domain:
        return []
    
    # Clean name
    parts = name.lower().strip().split()
    if len(parts) < 2:
        first = parts[0] if parts else "info"
        last = ""
    else:
        first = parts[0]
        last = parts[-1]
    
    patterns = [
        f"{first}@{domain}",
        f"{first}.{last}@{domain}",
        f"{first}{last}@{domain}",
        f"{first[0]}{last}@{domain}",
        f"{first}_{last}@{domain}",
        f"info@{domain}",
        f"contact@{domain}",
        f"hello@{domain}",
        f"team@{domain}",
    ]
    
    return list(set(patterns))

def extract_domain_from_url(url: str) -> str:
    """Extract domain from URL"""
    url = url.lower()
    url = re.sub(r'^https?://', '', url)
    url = re.sub(r'^www\.', '', url)
    url = url.split('/')[0]
    return url

# ============================================
# GOOGLE MAPS MANUAL WORKFLOW
# ============================================

def generate_google_maps_search_url(query: str, location: str) -> str:
    """Generate Google Maps search URL for manual extraction"""
    search_term = f"{query} in {location}"
    return f"https://www.google.com/maps/search/{quote_plus(search_term)}"

def google_maps_workflow(query: str, location: str):
    """Print instructions for manual Google Maps lead extraction"""
    
    search_url = generate_google_maps_search_url(query, location)
    
    print("\n" + "="*60)
    print("📍 GOOGLE MAPS LEAD FINDER")
    print("="*60)
    print(f"\n🔍 Search: {query} in {location}")
    print(f"\n🔗 Open this URL:\n{search_url}")
    print("""
MANUAL EXTRACTION STEPS:
1. Open the URL above in your browser
2. Scroll through results to load more businesses
3. For each business you want:
   - Click on it to see details
   - Note: Name, Phone, Website, Address
   - Look for email on their website

QUICK COPY FORMAT:
Name | Phone | Website | Address

TIPS:
- Filter by "Open now" if you want active businesses
- Check reviews for business size/quality indicators
- Look for businesses with websites (easier to contact)
- Skip chains/franchises (harder to sell to)
""")
    
    # Create a template CSV
    csv_template = f"google_maps_leads_{datetime.now().strftime('%Y%m%d')}.csv"
    with open(csv_template, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "business_name", "phone", "website", "address", 
            "rating", "reviews", "email_guess", "notes"
        ])
    
    print(f"📝 Created template: {csv_template}")
    print("   Fill this in as you browse!")

# ============================================
# INSTAGRAM/TIKTOK CREATOR FINDER
# ============================================

def creator_workflow(niche: str, platform: str = "instagram"):
    """Print instructions for finding creators"""
    
    search_queries = [
        f"{niche} creator",
        f"{niche} influencer",
        f"{niche} coach",
        f"{niche} tips",
        f"{niche} expert",
    ]
    
    print("\n" + "="*60)
    print(f"👤 {platform.upper()} CREATOR FINDER")
    print("="*60)
    print(f"\n🎯 Niche: {niche}")
    
    if platform == "instagram":
        print("""
SEARCH STRATEGY:
1. Go to Instagram.com/explore
2. Search these hashtags and find active creators:""")
        
        hashtags = [
            f"#{niche.replace(' ', '')}",
            f"#{niche.replace(' ', '')}tips",
            f"#{niche.replace(' ', '')}coach",
            f"#{niche.replace(' ', '')}creator",
            f"#{niche.replace(' ', '')}content",
        ]
        for h in hashtags:
            print(f"   {h}")
        
        print("""
3. Look for creators with:
   - 10k-500k followers (sweet spot)
   - Active posting (last 7 days)
   - Business/creator account (contact button)
   - Email in bio

CAPTURE:
- Username
- Follower count  
- Email (if in bio)
- DM open? (check for message button)
- Content style notes
""")
    
    elif platform == "tiktok":
        print("""
SEARCH STRATEGY:
1. Go to TikTok.com
2. Search these terms:""")
        for q in search_queries:
            print(f"   "{q}"")
        
        print("""
3. Filter by "Accounts" not "Videos"
4. Look for creators with:
   - 10k-1M followers
   - Consistent posting
   - Business/creator in bio

CAPTURE:
- Username
- Follower count
- Bio link (often Linktree with email)
- Content niche verification
""")
    
    # Create template
    csv_template = f"{platform}_creators_{datetime.now().strftime('%Y%m%d')}.csv"
    with open(csv_template, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "username", "platform", "followers", "email", 
            "bio_link", "niche", "engagement_notes", "contacted"
        ])
    
    print(f"\n📝 Created template: {csv_template}")

# ============================================
# WEBSITE SCRAPER (for emails)
# ============================================

def find_email_on_website(url: str) -> list:
    """Try to find email addresses on a website"""
    
    if not REQUESTS_AVAILABLE or not BS4_AVAILABLE:
        print("⚠️  Install requests and beautifulsoup4 for web scraping:")
        print("   pip install requests beautifulsoup4")
        return []
    
    emails = []
    pages_to_check = [
        url,
        url.rstrip("/") + "/contact",
        url.rstrip("/") + "/about",
        url.rstrip("/") + "/contact-us",
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; LeadFinder/1.0)"
    }
    
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    for page in pages_to_check:
        try:
            response = requests.get(page, headers=headers, timeout=5)
            if response.status_code == 200:
                # Find emails in page content
                found = re.findall(email_pattern, response.text)
                # Filter out common false positives
                for email in found:
                    if not any(x in email.lower() for x in [
                        "example.com", "email.com", "domain.com",
                        "sentry.io", "wixpress", "cloudflare"
                    ]):
                        emails.append(email)
        except:
            continue
    
    return list(set(emails))

# ============================================
# MAIN
# ============================================

def main():
    parser = argparse.ArgumentParser(description="Free Lead Finder")
    parser.add_argument("--source", "-s", 
                       choices=["google_maps", "creators", "email_find"],
                       required=True, help="Lead source")
    parser.add_argument("--query", "-q", help="Search query (service type, niche)")
    parser.add_argument("--location", "-l", help="Location (for local searches)")
    parser.add_argument("--platform", "-p", default="instagram",
                       help="Platform for creator search")
    parser.add_argument("--website", "-w", help="Website to find email on")
    
    args = parser.parse_args()
    
    if args.source == "google_maps":
        if not args.query or not args.location:
            print("Error: --query and --location required for google_maps")
            return
        google_maps_workflow(args.query, args.location)
    
    elif args.source == "creators":
        if not args.query:
            print("Error: --query (niche) required for creators")
            return
        creator_workflow(args.query, args.platform)
    
    elif args.source == "email_find":
        if not args.website:
            print("Error: --website required for email_find")
            return
        print(f"\n🔍 Searching for emails on {args.website}...")
        emails = find_email_on_website(args.website)
        if emails:
            print(f"\n📧 Found emails:")
            for email in emails:
                print(f"   {email}")
        else:
            print("\n❌ No emails found. Try:")
            domain = extract_domain_from_url(args.website)
            guesses = guess_email_patterns("contact", domain)[:5]
            print("   Common patterns to try:")
            for g in guesses:
                print(f"   {g}")

if __name__ == "__main__":
    main()
