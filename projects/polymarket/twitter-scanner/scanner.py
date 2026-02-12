#!/usr/bin/env python3
"""
Twitter Scanner for Polymarket Content
Scans viral posts, news accounts, and prediction market gurus
For Peter Griffin Polymarket persona content ideas
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import argparse

# Check if rich is available for pretty output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    console = None


def load_config(config_path: str = "config.json") -> dict:
    """Load scanner configuration"""
    with open(config_path, 'r') as f:
        return json.load(f)


def run_snscrape(query: str, limit: int = 50, since_hours: int = 24) -> list:
    """Run snscrape and return tweets as list of dicts"""
    since_date = (datetime.now() - timedelta(hours=since_hours)).strftime('%Y-%m-%d')
    
    cmd = [
        sys.executable, '-m', 'snscrape',
        '--jsonl',
        '--max-results', str(limit),
        'twitter-search',
        f'{query} since:{since_date}'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        tweets = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    tweets.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return tweets
    except subprocess.TimeoutExpired:
        print(f"Timeout scanning: {query}")
        return []
    except Exception as e:
        print(f"Error scanning {query}: {e}")
        return []


def get_account_tweets(username: str, limit: int = 20, since_hours: int = 24) -> list:
    """Get recent tweets from a specific account"""
    return run_snscrape(f'from:{username}', limit, since_hours)


def get_hashtag_tweets(hashtag: str, limit: int = 50, since_hours: int = 24) -> list:
    """Get recent tweets with a specific hashtag"""
    return run_snscrape(f'#{hashtag}', limit, since_hours)


def get_keyword_tweets(keyword: str, limit: int = 50, since_hours: int = 24) -> list:
    """Get recent tweets containing a keyword"""
    return run_snscrape(f'"{keyword}"', limit, since_hours)


def is_viral(tweet: dict, thresholds: dict) -> bool:
    """Check if tweet meets viral thresholds"""
    likes = tweet.get('likeCount', 0) or 0
    retweets = tweet.get('retweetCount', 0) or 0
    replies = tweet.get('replyCount', 0) or 0
    
    return (likes >= thresholds.get('min_likes', 100) or
            retweets >= thresholds.get('min_retweets', 25) or
            replies >= thresholds.get('min_replies', 10))


def extract_tweet_data(tweet: dict) -> dict:
    """Extract relevant data from a tweet"""
    return {
        'id': tweet.get('id'),
        'url': tweet.get('url'),
        'date': tweet.get('date'),
        'user': tweet.get('user', {}).get('username'),
        'user_followers': tweet.get('user', {}).get('followersCount'),
        'content': tweet.get('rawContent', tweet.get('content', '')),
        'likes': tweet.get('likeCount', 0),
        'retweets': tweet.get('retweetCount', 0),
        'replies': tweet.get('replyCount', 0),
        'engagement': (tweet.get('likeCount', 0) or 0) + 
                      (tweet.get('retweetCount', 0) or 0) * 2 +
                      (tweet.get('replyCount', 0) or 0) * 3,
        'source': 'scanner'
    }


def scan_all(config: dict) -> dict:
    """Run full scan based on config"""
    results = {
        'scan_time': datetime.now().isoformat(),
        'accounts': {},
        'hashtags': {},
        'keywords': {},
        'viral_posts': [],
        'top_content_ideas': []
    }
    
    since_hours = config.get('scan_hours', 24)
    viral_thresholds = config.get('viral_threshold', {})
    all_tweets = []
    
    # Scan accounts
    print("\n🔍 Scanning accounts...")
    for category, accounts in config.get('accounts', {}).items():
        results['accounts'][category] = []
        for username in accounts:
            print(f"  → @{username}")
            tweets = get_account_tweets(username, limit=10, since_hours=since_hours)
            for tweet in tweets:
                data = extract_tweet_data(tweet)
                data['category'] = category
                results['accounts'][category].append(data)
                all_tweets.append(data)
    
    # Scan hashtags
    print("\n#️⃣ Scanning hashtags...")
    for hashtag in config.get('hashtags', []):
        print(f"  → #{hashtag}")
        tweets = get_hashtag_tweets(hashtag, limit=30, since_hours=since_hours)
        results['hashtags'][hashtag] = []
        for tweet in tweets:
            data = extract_tweet_data(tweet)
            data['hashtag'] = hashtag
            results['hashtags'][hashtag].append(data)
            all_tweets.append(data)
    
    # Scan keywords
    print("\n🔑 Scanning keywords...")
    for keyword in config.get('keywords', []):
        print(f"  → \"{keyword}\"")
        tweets = get_keyword_tweets(keyword, limit=30, since_hours=since_hours)
        results['keywords'][keyword] = []
        for tweet in tweets:
            data = extract_tweet_data(tweet)
            data['keyword'] = keyword
            results['keywords'][keyword].append(data)
            all_tweets.append(data)
    
    # Find viral posts
    print("\n🔥 Finding viral posts...")
    seen_ids = set()
    for tweet in all_tweets:
        tweet_id = tweet.get('id')
        if tweet_id and tweet_id not in seen_ids:
            seen_ids.add(tweet_id)
            # Check if viral based on engagement
            if tweet.get('engagement', 0) >= 150:  # Simplified viral check
                results['viral_posts'].append(tweet)
    
    # Sort by engagement
    results['viral_posts'].sort(key=lambda x: x.get('engagement', 0), reverse=True)
    results['viral_posts'] = results['viral_posts'][:20]  # Top 20 viral
    
    # Generate content ideas
    print("\n💡 Generating content ideas...")
    for tweet in results['viral_posts'][:10]:
        idea = {
            'source_tweet': tweet['url'],
            'source_user': tweet['user'],
            'engagement': tweet['engagement'],
            'original_content': tweet['content'][:200],
            'peter_griffin_angle': generate_content_angle(tweet['content'])
        }
        results['top_content_ideas'].append(idea)
    
    return results


def generate_content_angle(content: str) -> str:
    """Generate a Peter Griffin style content angle"""
    # Simple keyword-based angle suggestions
    content_lower = content.lower()
    
    angles = []
    if 'trump' in content_lower or 'biden' in content_lower or 'election' in content_lower:
        angles.append("Political betting take with degen humor")
    if 'whale' in content_lower or 'million' in content_lower:
        angles.append("Whale watching commentary - 'this guy knows something'")
    if 'odds' in content_lower or '%' in content_lower:
        angles.append("Odds analysis with meme reaction")
    if 'wrong' in content_lower or 'lost' in content_lower:
        angles.append("L compilation / copium content")
    if 'win' in content_lower or 'profit' in content_lower:
        angles.append("W celebration / gains content")
    
    if not angles:
        angles.append("General Polymarket commentary - find the funny angle")
    
    return " | ".join(angles)


def save_results(results: dict, output_dir: str = "output"):
    """Save scan results to files"""
    Path(output_dir).mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    
    # Save full JSON
    json_path = f"{output_dir}/scan_{timestamp}.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n📁 Full results saved to: {json_path}")
    
    # Save readable summary
    summary_path = f"{output_dir}/summary_{timestamp}.md"
    with open(summary_path, 'w') as f:
        f.write(f"# Twitter Scan Summary\n")
        f.write(f"*Scanned: {results['scan_time']}*\n\n")
        
        f.write("## 🔥 Top Viral Posts\n\n")
        for i, tweet in enumerate(results.get('viral_posts', [])[:10], 1):
            f.write(f"### {i}. @{tweet['user']} ({tweet['engagement']} engagement)\n")
            f.write(f"{tweet['content'][:280]}\n")
            f.write(f"[Link]({tweet['url']})\n\n")
        
        f.write("## 💡 Content Ideas for Peter Griffin Polymarket\n\n")
        for i, idea in enumerate(results.get('top_content_ideas', []), 1):
            f.write(f"{i}. **Angle:** {idea['peter_griffin_angle']}\n")
            f.write(f"   - Source: @{idea['source_user']} ({idea['engagement']} engagement)\n")
            f.write(f"   - [Original Tweet]({idea['source_tweet']})\n\n")
    
    print(f"📝 Summary saved to: {summary_path}")
    
    # Save latest symlink for easy access
    latest_json = f"{output_dir}/latest.json"
    latest_md = f"{output_dir}/latest.md"
    
    # Remove old symlinks if they exist
    for link in [latest_json, latest_md]:
        if os.path.islink(link):
            os.unlink(link)
    
    # Create relative symlinks
    os.symlink(os.path.basename(json_path), latest_json)
    os.symlink(os.path.basename(summary_path), latest_md)
    
    return json_path, summary_path


def print_summary(results: dict):
    """Print a summary of the scan results"""
    if RICH_AVAILABLE:
        console.print(Panel.fit("🐋 Twitter Scan Complete", style="bold blue"))
        
        table = Table(title="📊 Scan Statistics")
        table.add_column("Category", style="cyan")
        table.add_column("Count", style="green")
        
        total_account_tweets = sum(len(tweets) for tweets in results.get('accounts', {}).values())
        total_hashtag_tweets = sum(len(tweets) for tweets in results.get('hashtags', {}).values())
        total_keyword_tweets = sum(len(tweets) for tweets in results.get('keywords', {}).values())
        
        table.add_row("Account Tweets", str(total_account_tweets))
        table.add_row("Hashtag Tweets", str(total_hashtag_tweets))
        table.add_row("Keyword Tweets", str(total_keyword_tweets))
        table.add_row("Viral Posts Found", str(len(results.get('viral_posts', []))))
        table.add_row("Content Ideas", str(len(results.get('top_content_ideas', []))))
        
        console.print(table)
        
        if results.get('viral_posts'):
            console.print("\n[bold yellow]🔥 Top 5 Viral Posts:[/bold yellow]")
            for i, tweet in enumerate(results['viral_posts'][:5], 1):
                console.print(f"  {i}. @{tweet['user']} - {tweet['engagement']} engagement")
                console.print(f"     [dim]{tweet['content'][:100]}...[/dim]")
    else:
        print("\n" + "="*50)
        print("🐋 TWITTER SCAN COMPLETE")
        print("="*50)
        print(f"\nViral Posts Found: {len(results.get('viral_posts', []))}")
        print(f"Content Ideas: {len(results.get('top_content_ideas', []))}")


def main():
    parser = argparse.ArgumentParser(description='Twitter Scanner for Polymarket Content')
    parser.add_argument('--config', '-c', default='config.json', help='Config file path')
    parser.add_argument('--hours', '-H', type=int, help='Hours to scan back (overrides config)')
    parser.add_argument('--output', '-o', help='Output directory (overrides config)')
    parser.add_argument('--quick', '-q', action='store_true', help='Quick scan (fewer results)')
    args = parser.parse_args()
    
    print("🐋 Twitter Scanner for Polymarket")
    print("=" * 40)
    
    # Load config
    config = load_config(args.config)
    
    if args.hours:
        config['scan_hours'] = args.hours
    
    output_dir = args.output or config.get('output_dir', 'output')
    
    # Run scan
    results = scan_all(config)
    
    # Save and display results
    save_results(results, output_dir)
    print_summary(results)
    
    print("\n✅ Done! Check the output folder for full results.")
    print("   Use latest.md for a quick summary.")


if __name__ == '__main__':
    main()
