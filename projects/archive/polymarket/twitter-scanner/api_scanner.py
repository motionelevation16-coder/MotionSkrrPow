#!/usr/bin/env python3
"""
Twitter API Scanner (requires API key)
Uses official Twitter API v2
$100/month for Basic tier: https://developer.twitter.com/en/portal/products

Set TWITTER_BEARER_TOKEN environment variable or create .env file
"""

import json
import os
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Try to load from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "User-Agent": "PolymarketScanner/1.0"
}

BASE_URL = "https://api.twitter.com/2"


def load_config(config_path: str = "config.json") -> dict:
    with open(config_path, 'r') as f:
        return json.load(f)


def check_auth() -> bool:
    """Verify API access"""
    if not BEARER_TOKEN:
        print("❌ No TWITTER_BEARER_TOKEN found!")
        print("   Set it via environment variable or create .env file:")
        print("   TWITTER_BEARER_TOKEN=your_token_here")
        print("\n   Get your token: https://developer.twitter.com/en/portal/products")
        return False
    
    try:
        r = requests.get(
            f"{BASE_URL}/users/me",
            headers=HEADERS,
            timeout=10
        )
        if r.status_code == 401:
            print("❌ Invalid or expired token!")
            return False
        return True
    except Exception as e:
        print(f"❌ Auth check failed: {e}")
        return False


def get_user_id(username: str) -> Optional[str]:
    """Get user ID from username"""
    try:
        r = requests.get(
            f"{BASE_URL}/users/by/username/{username}",
            headers=HEADERS,
            timeout=10
        )
        if r.status_code == 200:
            return r.json().get('data', {}).get('id')
    except:
        pass
    return None


def get_user_tweets(user_id: str, max_results: int = 10) -> list:
    """Get recent tweets from a user"""
    try:
        params = {
            "max_results": max_results,
            "tweet.fields": "created_at,public_metrics,entities",
            "expansions": "author_id",
            "user.fields": "username,public_metrics"
        }
        r = requests.get(
            f"{BASE_URL}/users/{user_id}/tweets",
            headers=HEADERS,
            params=params,
            timeout=15
        )
        if r.status_code == 200:
            data = r.json()
            return data.get('data', [])
    except Exception as e:
        print(f"  Error: {e}")
    return []


def search_tweets(query: str, max_results: int = 50) -> list:
    """Search recent tweets (last 7 days)"""
    try:
        params = {
            "query": query,
            "max_results": max_results,
            "tweet.fields": "created_at,public_metrics,entities",
            "expansions": "author_id",
            "user.fields": "username,public_metrics"
        }
        r = requests.get(
            f"{BASE_URL}/tweets/search/recent",
            headers=HEADERS,
            params=params,
            timeout=15
        )
        if r.status_code == 200:
            data = r.json()
            return data.get('data', [])
        elif r.status_code == 429:
            print("  ⚠️ Rate limited - waiting 60s...")
            import time
            time.sleep(60)
            return search_tweets(query, max_results)
    except Exception as e:
        print(f"  Error: {e}")
    return []


def extract_tweet_data(tweet: dict, username: str = None) -> dict:
    """Extract relevant data from API response"""
    metrics = tweet.get('public_metrics', {})
    return {
        'id': tweet.get('id'),
        'url': f"https://twitter.com/{username or 'i'}/status/{tweet.get('id')}",
        'date': tweet.get('created_at'),
        'user': username,
        'content': tweet.get('text', ''),
        'likes': metrics.get('like_count', 0),
        'retweets': metrics.get('retweet_count', 0),
        'replies': metrics.get('reply_count', 0),
        'engagement': (metrics.get('like_count', 0) +
                      metrics.get('retweet_count', 0) * 2 +
                      metrics.get('reply_count', 0) * 3),
        'source': 'twitter_api'
    }


def scan_all(config: dict) -> dict:
    """Run full scan via API"""
    results = {
        'scan_time': datetime.now().isoformat(),
        'method': 'twitter_api',
        'accounts': {},
        'hashtags': {},
        'keywords': {},
        'viral_posts': [],
        'all_tweets': []
    }
    
    # Scan accounts
    print("\n📡 Scanning accounts...")
    for category, accounts in config.get('accounts', {}).items():
        results['accounts'][category] = []
        for username in accounts:
            print(f"  → @{username}")
            user_id = get_user_id(username)
            if user_id:
                tweets = get_user_tweets(user_id, max_results=5)
                for tweet in tweets:
                    data = extract_tweet_data(tweet, username)
                    data['category'] = category
                    results['accounts'][category].append(data)
                    results['all_tweets'].append(data)
    
    # Search hashtags
    print("\n#️⃣ Searching hashtags...")
    for hashtag in config.get('hashtags', []):
        print(f"  → #{hashtag}")
        tweets = search_tweets(f"#{hashtag}", max_results=20)
        results['hashtags'][hashtag] = []
        for tweet in tweets:
            data = extract_tweet_data(tweet)
            data['hashtag'] = hashtag
            results['hashtags'][hashtag].append(data)
            results['all_tweets'].append(data)
    
    # Search keywords
    print("\n🔑 Searching keywords...")
    for keyword in config.get('keywords', []):
        print(f"  → \"{keyword}\"")
        tweets = search_tweets(f'"{keyword}"', max_results=20)
        results['keywords'][keyword] = []
        for tweet in tweets:
            data = extract_tweet_data(tweet)
            data['keyword'] = keyword
            results['keywords'][keyword].append(data)
            results['all_tweets'].append(data)
    
    # Find viral posts
    viral_threshold = config.get('viral_threshold', {}).get('min_likes', 100)
    results['viral_posts'] = [
        t for t in results['all_tweets'] 
        if t.get('engagement', 0) >= viral_threshold
    ]
    results['viral_posts'].sort(key=lambda x: x.get('engagement', 0), reverse=True)
    
    return results


def save_results(results: dict, output_dir: str = "output"):
    """Save results"""
    Path(output_dir).mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    
    json_path = f"{output_dir}/api_scan_{timestamp}.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    md_path = f"{output_dir}/api_summary_{timestamp}.md"
    with open(md_path, 'w') as f:
        f.write(f"# Twitter API Scan Summary\n")
        f.write(f"*Scanned: {results['scan_time']}*\n\n")
        
        f.write(f"## Stats\n")
        f.write(f"- Total tweets: {len(results.get('all_tweets', []))}\n")
        f.write(f"- Viral posts: {len(results.get('viral_posts', []))}\n\n")
        
        f.write("## 🔥 Top Viral\n\n")
        for tweet in results.get('viral_posts', [])[:10]:
            f.write(f"**@{tweet['user']}** ({tweet['engagement']} engagement)\n")
            f.write(f"{tweet['content'][:200]}\n")
            f.write(f"[Link]({tweet['url']})\n\n---\n\n")
    
    print(f"\n📁 {json_path}")
    print(f"📝 {md_path}")


def main():
    print("🐋 Twitter API Scanner")
    print("=" * 40)
    
    if not check_auth():
        return
    
    print("✓ API access verified!")
    
    config = load_config()
    results = scan_all(config)
    save_results(results)
    
    print(f"\n✅ Found {len(results['all_tweets'])} tweets!")
    print(f"🔥 {len(results['viral_posts'])} viral posts!")


if __name__ == '__main__':
    main()
