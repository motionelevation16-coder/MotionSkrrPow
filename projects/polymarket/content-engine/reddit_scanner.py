#!/usr/bin/env python3
"""
Reddit Scanner for Polymarket Content
Scrapes r/polymarket and related subs for trending discussions
No API key needed - uses public JSON endpoints
"""

import json
import requests
from datetime import datetime
from pathlib import Path

SUBREDDITS = [
    "polymarket",
    "PredictionMarket", 
    "wallstreetbets",  # Sometimes discusses prediction markets
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def get_subreddit_posts(subreddit: str, sort: str = "hot", limit: int = 25) -> list:
    """Fetch posts from a subreddit using public JSON API"""
    try:
        url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}"
        r = requests.get(url, headers=HEADERS, timeout=15)
        
        if r.status_code == 200:
            data = r.json()
            posts = []
            
            for child in data.get('data', {}).get('children', []):
                post = child.get('data', {})
                posts.append({
                    'title': post.get('title'),
                    'selftext': post.get('selftext', '')[:500],
                    'score': post.get('score', 0),
                    'num_comments': post.get('num_comments', 0),
                    'url': f"https://reddit.com{post.get('permalink', '')}",
                    'created_utc': post.get('created_utc'),
                    'subreddit': subreddit,
                    'author': post.get('author'),
                    'upvote_ratio': post.get('upvote_ratio', 0),
                })
            
            return posts
        else:
            print(f"  Error fetching r/{subreddit}: {r.status_code}")
            return []
    except Exception as e:
        print(f"  Error: {e}")
        return []


def search_reddit(query: str, limit: int = 25) -> list:
    """Search Reddit for a query"""
    try:
        url = f"https://www.reddit.com/search.json?q={query}&limit={limit}&sort=relevance&t=week"
        r = requests.get(url, headers=HEADERS, timeout=15)
        
        if r.status_code == 200:
            data = r.json()
            posts = []
            
            for child in data.get('data', {}).get('children', []):
                post = child.get('data', {})
                posts.append({
                    'title': post.get('title'),
                    'selftext': post.get('selftext', '')[:500],
                    'score': post.get('score', 0),
                    'num_comments': post.get('num_comments', 0),
                    'url': f"https://reddit.com{post.get('permalink', '')}",
                    'subreddit': post.get('subreddit'),
                })
            
            return posts
    except Exception as e:
        print(f"  Search error: {e}")
    return []


def analyze_post(post: dict) -> dict:
    """Analyze a post for content potential"""
    score = 0
    angles = []
    
    title_lower = post.get('title', '').lower()
    
    # Engagement scoring
    upvotes = post.get('score', 0)
    comments = post.get('num_comments', 0)
    
    if upvotes > 500:
        score += 30
        angles.append("🔥 HIGH UPVOTES")
    elif upvotes > 100:
        score += 15
        angles.append("📈 Good engagement")
    
    if comments > 100:
        score += 20
        angles.append("💬 HEATED DISCUSSION")
    elif comments > 30:
        score += 10
    
    # Topic scoring
    if any(word in title_lower for word in ['trump', 'biden', 'election']):
        score += 15
        angles.append("🏛️ Political")
    
    if any(word in title_lower for word in ['elon', 'musk']):
        score += 15
        angles.append("🚀 Elon")
    
    if any(word in title_lower for word in ['whale', 'million', 'bet big']):
        score += 20
        angles.append("🐋 WHALE ACTIVITY")
    
    if any(word in title_lower for word in ['wrong', 'lost', 'rekt', 'liquidat']):
        score += 20
        angles.append("💀 L CONTENT")
    
    if any(word in title_lower for word in ['called it', 'win', 'profit', 'gains']):
        score += 15
        angles.append("🎉 W CONTENT")
    
    post['content_score'] = score
    post['content_angles'] = angles
    
    return post


def scan_all() -> dict:
    """Scan all sources"""
    results = {
        'scan_time': datetime.now().isoformat(),
        'subreddits': {},
        'search_results': {},
        'top_content': []
    }
    
    all_posts = []
    
    # Scan subreddits
    print("📡 Scanning subreddits...")
    for sub in SUBREDDITS:
        print(f"  → r/{sub}")
        posts = get_subreddit_posts(sub, sort="hot", limit=25)
        results['subreddits'][sub] = posts
        all_posts.extend(posts)
    
    # Search for polymarket mentions
    print("🔍 Searching for polymarket discussions...")
    search_posts = search_reddit("polymarket", limit=25)
    results['search_results']['polymarket'] = search_posts
    all_posts.extend(search_posts)
    
    # Analyze and rank
    print("📊 Analyzing posts...")
    analyzed = [analyze_post(p) for p in all_posts]
    analyzed = [p for p in analyzed if p.get('content_score', 0) > 0]
    analyzed.sort(key=lambda x: x.get('content_score', 0), reverse=True)
    
    # Dedupe by URL
    seen = set()
    unique = []
    for p in analyzed:
        if p['url'] not in seen:
            seen.add(p['url'])
            unique.append(p)
    
    results['top_content'] = unique[:10]
    
    return results


def generate_alert(results: dict) -> str:
    """Generate alert message"""
    alert = "📢 **REDDIT CONTENT ALERT** 📢\n"
    alert += f"*Scanned: {results['scan_time'][:16]}*\n\n"
    
    for i, post in enumerate(results.get('top_content', [])[:5], 1):
        alert += f"**{i}. {post['title'][:70]}**\n"
        alert += f"   📊 {post.get('score', 0)} upvotes | {post.get('num_comments', 0)} comments\n"
        alert += f"   📍 r/{post.get('subreddit', 'unknown')}\n"
        if post.get('content_angles'):
            alert += f"   🎯 {' '.join(post['content_angles'][:2])}\n"
        alert += f"   🔗 {post['url']}\n\n"
    
    return alert


def save_results(results: dict, output_dir: str = "output"):
    """Save results"""
    Path(output_dir).mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    
    json_path = f"{output_dir}/reddit_scan_{timestamp}.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    alert = generate_alert(results)
    alert_path = f"{output_dir}/reddit_alert_{timestamp}.md"
    with open(alert_path, 'w') as f:
        f.write(alert)
    
    print(f"\n📁 Saved: {json_path}")
    return alert


def main():
    print("🐋 Reddit Content Scanner")
    print("=" * 40)
    
    results = scan_all()
    alert = save_results(results)
    
    print("\n" + alert)
    print(f"✅ Found {len(results.get('top_content', []))} content opportunities!")


if __name__ == '__main__':
    main()
