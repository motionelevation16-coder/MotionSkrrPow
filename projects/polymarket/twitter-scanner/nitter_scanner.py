#!/usr/bin/env python3
"""
Nitter-based Twitter Scanner (fallback)
Uses Nitter RSS feeds when snscrape gets blocked
"""

import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Optional
import requests
import re
import time

# List of public Nitter instances (some may be down)
NITTER_INSTANCES = [
    "https://nitter.privacydev.net",
    "https://nitter.poast.org", 
    "https://nitter.cz",
    "https://nitter.1d4.us",
]

def load_config(config_path: str = "config.json") -> dict:
    with open(config_path, 'r') as f:
        return json.load(f)


def get_working_instance() -> Optional[str]:
    """Find a working Nitter instance"""
    for instance in NITTER_INSTANCES:
        try:
            r = requests.get(f"{instance}/Polymarket/rss", timeout=10)
            if r.status_code == 200:
                print(f"✓ Using: {instance}")
                return instance
        except:
            continue
    return None


def fetch_user_feed(instance: str, username: str) -> list:
    """Fetch RSS feed for a user"""
    try:
        url = f"{instance}/{username}/rss"
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            return []
        
        # Parse RSS XML
        root = ET.fromstring(r.content)
        tweets = []
        
        for item in root.findall('.//item'):
            title = item.find('title')
            link = item.find('link')
            pubDate = item.find('pubDate')
            description = item.find('description')
            
            if title is not None and link is not None:
                # Extract engagement from description if available
                desc_text = description.text if description is not None else ""
                
                tweet = {
                    'user': username,
                    'content': title.text or "",
                    'url': (link.text or "").replace(instance, "https://twitter.com"),
                    'date': pubDate.text if pubDate is not None else "",
                    'description': desc_text,
                    'source': 'nitter'
                }
                tweets.append(tweet)
        
        return tweets
    except Exception as e:
        print(f"  Error fetching @{username}: {e}")
        return []


def fetch_search(instance: str, query: str) -> list:
    """Search via Nitter (limited support)"""
    try:
        url = f"{instance}/search/rss?f=tweets&q={query}"
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            return []
        
        root = ET.fromstring(r.content)
        tweets = []
        
        for item in root.findall('.//item'):
            title = item.find('title')
            link = item.find('link')
            pubDate = item.find('pubDate')
            
            if title is not None and link is not None:
                # Try to extract username from link
                link_text = link.text or ""
                username = "unknown"
                match = re.search(r'twitter\.com/(\w+)/status', link_text.replace(instance, "twitter.com"))
                if match:
                    username = match.group(1)
                
                tweet = {
                    'user': username,
                    'content': title.text or "",
                    'url': link_text.replace(instance, "https://twitter.com"),
                    'date': pubDate.text if pubDate is not None else "",
                    'source': 'nitter_search'
                }
                tweets.append(tweet)
        
        return tweets
    except Exception as e:
        print(f"  Error searching '{query}': {e}")
        return []


def scan_all(config: dict) -> dict:
    """Run scan using Nitter"""
    results = {
        'scan_time': datetime.now().isoformat(),
        'method': 'nitter',
        'accounts': {},
        'searches': {},
        'all_tweets': []
    }
    
    # Find working instance
    print("🔍 Finding working Nitter instance...")
    instance = get_working_instance()
    
    if not instance:
        print("❌ No working Nitter instance found!")
        print("   All public instances may be down.")
        print("   Try again later or use Twitter API.")
        return results
    
    results['instance'] = instance
    
    # Scan accounts
    print("\n📡 Scanning accounts...")
    for category, accounts in config.get('accounts', {}).items():
        results['accounts'][category] = []
        for username in accounts:
            print(f"  → @{username}")
            tweets = fetch_user_feed(instance, username)
            results['accounts'][category].extend(tweets)
            results['all_tweets'].extend(tweets)
            time.sleep(0.5)  # Be nice to the instance
    
    # Search hashtags
    print("\n#️⃣ Searching hashtags...")
    for hashtag in config.get('hashtags', []):
        print(f"  → #{hashtag}")
        tweets = fetch_search(instance, f"%23{hashtag}")
        results['searches'][f"#{hashtag}"] = tweets
        results['all_tweets'].extend(tweets)
        time.sleep(0.5)
    
    # Search keywords
    print("\n🔑 Searching keywords...")
    for keyword in config.get('keywords', []):
        print(f"  → \"{keyword}\"")
        tweets = fetch_search(instance, keyword.replace(" ", "%20"))
        results['searches'][keyword] = tweets
        results['all_tweets'].extend(tweets)
        time.sleep(0.5)
    
    return results


def save_results(results: dict, output_dir: str = "output"):
    """Save results to files"""
    Path(output_dir).mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    
    # Save JSON
    json_path = f"{output_dir}/nitter_scan_{timestamp}.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    # Save summary
    md_path = f"{output_dir}/nitter_summary_{timestamp}.md"
    with open(md_path, 'w') as f:
        f.write(f"# Nitter Scan Summary\n")
        f.write(f"*Scanned: {results['scan_time']}*\n")
        f.write(f"*Instance: {results.get('instance', 'N/A')}*\n\n")
        
        f.write(f"## Stats\n")
        f.write(f"- Total tweets: {len(results.get('all_tweets', []))}\n\n")
        
        f.write("## Recent Tweets\n\n")
        for tweet in results.get('all_tweets', [])[:20]:
            f.write(f"**@{tweet['user']}**\n")
            f.write(f"{tweet['content'][:200]}\n")
            f.write(f"[Link]({tweet['url']})\n\n---\n\n")
    
    print(f"\n📁 Saved: {json_path}")
    print(f"📝 Saved: {md_path}")
    
    return json_path, md_path


def main():
    print("🐋 Nitter-based Twitter Scanner")
    print("=" * 40)
    
    config = load_config()
    results = scan_all(config)
    
    if results.get('all_tweets'):
        save_results(results)
        print(f"\n✅ Found {len(results['all_tweets'])} tweets!")
    else:
        print("\n⚠️ No tweets found. Nitter instances may be down.")
    
    print("\n💡 Tip: If Nitter fails often, consider Twitter API ($100/mo)")


if __name__ == '__main__':
    main()
