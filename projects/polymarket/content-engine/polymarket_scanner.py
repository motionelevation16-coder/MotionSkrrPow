#!/usr/bin/env python3
"""
Polymarket Content Engine
Scans for viral content opportunities: big moves, weird markets, controversies
For Peter Griffin Predictions persona
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import argparse

# Polymarket API endpoints
GAMMA_API = "https://gamma-api.polymarket.com"
CLOB_API = "https://clob.polymarket.com"

def get_markets(limit: int = 100, active: bool = True) -> list:
    """Fetch markets from Polymarket API"""
    try:
        params = {
            "limit": limit,
            "active": str(active).lower(),
            "closed": "false"
        }
        r = requests.get(f"{GAMMA_API}/markets", params=params, timeout=30)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"API Error: {r.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching markets: {e}")
        return []


def get_trending_markets(limit: int = 20) -> list:
    """Get markets sorted by volume/activity"""
    markets = get_markets(limit=200)
    
    # Sort by volume (liquidity as proxy)
    sorted_markets = sorted(
        markets,
        key=lambda x: float(x.get('volume', 0) or 0),
        reverse=True
    )
    
    return sorted_markets[:limit]


def get_market_details(condition_id: str) -> Optional[dict]:
    """Get detailed market info"""
    try:
        r = requests.get(f"{GAMMA_API}/markets/{condition_id}", timeout=15)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None


def analyze_market(market: dict) -> dict:
    """Analyze a market for content potential"""
    analysis = {
        'id': market.get('id'),
        'condition_id': market.get('conditionId'),
        'question': market.get('question', 'Unknown'),
        'slug': market.get('slug'),
        'url': f"https://polymarket.com/event/{market.get('slug', '')}",
        'volume': float(market.get('volume', 0) or 0),
        'liquidity': float(market.get('liquidity', 0) or 0),
        'outcomes': [],
        'content_score': 0,
        'content_angles': [],
        'category': 'general'
    }
    
    # Parse outcomes and probabilities
    outcomes_str = market.get('outcomes', '[]')
    if isinstance(outcomes_str, str):
        try:
            outcomes = json.loads(outcomes_str)
        except:
            outcomes = []
    else:
        outcomes = outcomes_str or []
    
    prices_str = market.get('outcomePrices', '[]')
    if isinstance(prices_str, str):
        try:
            prices = json.loads(prices_str)
        except:
            prices = []
    else:
        prices = prices_str or []
    
    for i, outcome in enumerate(outcomes):
        price = float(prices[i]) if i < len(prices) else 0
        analysis['outcomes'].append({
            'name': outcome,
            'probability': round(price * 100, 1)
        })
    
    # Calculate content score based on various factors
    score = 0
    angles = []
    question = analysis['question'].lower()
    
    # High volume = trending
    if analysis['volume'] > 1000000:
        score += 30
        angles.append("🔥 HIGH VOLUME - People are betting big")
    elif analysis['volume'] > 100000:
        score += 15
        angles.append("📈 Decent volume - Active market")
    
    # Close odds = controversial/uncertain
    if analysis['outcomes']:
        probs = [o['probability'] for o in analysis['outcomes']]
        if probs and max(probs) < 70 and max(probs) > 30:
            score += 25
            angles.append("⚔️ CLOSE ODDS - Nobody knows!")
    
    # Extreme odds = potential upset content
    if analysis['outcomes']:
        probs = [o['probability'] for o in analysis['outcomes']]
        if probs and (min(probs) < 10 or max(probs) > 90):
            score += 15
            angles.append("🎰 EXTREME ODDS - Upset potential?")
    
    # Topic-based scoring
    if any(word in question for word in ['trump', 'biden', 'election', 'president']):
        score += 20
        analysis['category'] = 'politics'
        angles.append("🏛️ POLITICS - Always viral")
    
    if any(word in question for word in ['elon', 'musk', 'tesla', 'twitter', 'x ']):
        score += 20
        analysis['category'] = 'tech'
        angles.append("🚀 ELON - Guaranteed engagement")
    
    if any(word in question for word in ['war', 'russia', 'ukraine', 'china', 'military']):
        score += 15
        analysis['category'] = 'geopolitics'
        angles.append("⚔️ GEOPOLITICS - High stakes")
    
    if any(word in question for word in ['bitcoin', 'crypto', 'eth', 'btc']):
        score += 15
        analysis['category'] = 'crypto'
        angles.append("₿ CRYPTO - Degen territory")
    
    if any(word in question for word in ['ai', 'chatgpt', 'openai', 'artificial']):
        score += 15
        analysis['category'] = 'ai'
        angles.append("🤖 AI - Hot topic")
    
    # Weird/funny markets
    if any(word in question for word in ['alien', 'ufo', 'celebrity', 'kanye', 'kardashian']):
        score += 25
        analysis['category'] = 'weird'
        angles.append("🛸 WEIRD/FUNNY - Meme potential")
    
    analysis['content_score'] = score
    analysis['content_angles'] = angles
    
    return analysis


def find_holy_shit_content(limit: int = 10) -> list:
    """Find the best content opportunities"""
    print("🔍 Scanning Polymarket for content...")
    
    markets = get_markets(limit=200)
    print(f"   Found {len(markets)} active markets")
    
    analyzed = []
    for market in markets:
        analysis = analyze_market(market)
        if analysis['content_score'] > 0:
            analyzed.append(analysis)
    
    # Sort by content score
    analyzed.sort(key=lambda x: x['content_score'], reverse=True)
    
    return analyzed[:limit]


def generate_alert(markets: list) -> str:
    """Generate a content alert message"""
    alert = "🚨 **POLYMARKET CONTENT ALERT** 🚨\n"
    alert += f"*Scanned: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
    
    for i, m in enumerate(markets[:5], 1):
        alert += f"**{i}. {m['question'][:80]}**\n"
        
        # Show odds
        if m['outcomes']:
            odds = " | ".join([f"{o['name']}: {o['probability']}%" for o in m['outcomes'][:2]])
            alert += f"   📊 {odds}\n"
        
        # Show volume
        vol = m['volume']
        if vol > 1000000:
            vol_str = f"${vol/1000000:.1f}M"
        elif vol > 1000:
            vol_str = f"${vol/1000:.0f}K"
        else:
            vol_str = f"${vol:.0f}"
        alert += f"   💰 Volume: {vol_str}\n"
        
        # Show angles
        if m['content_angles']:
            alert += f"   🎯 {' '.join(m['content_angles'][:2])}\n"
        
        alert += f"   🔗 {m['url']}\n\n"
    
    return alert


def generate_script_prompt(market: dict) -> str:
    """Generate a script prompt for the selected market"""
    outcomes_str = ""
    if market['outcomes']:
        outcomes_str = ", ".join([f"{o['name']} at {o['probability']}%" for o in market['outcomes']])
    
    prompt = f"""You are my viral script ghostwriter.
Your job is to create Family Guy styled short-form video scripts (Reels / Shorts / TikTok) that maximize hook, retention, and payoff.

🎭 Characters:
- 🧱 Peter = Main analyst (cold, logical, shocking, always knows the truth about the bets)
- 👶 Stewie = Zoomer (sarcastic, meme-slang, half-awake but witty)

⚡️ Script Structure:
1. Hook (0–3 sec): Shocking paradox / absurd question about this prediction
2. Conflict & Escalation (3–45 sec): Peter and Stewie debate the odds, roast the bettors
3. Payoff (45–60 sec): Cold, viral conclusion about what this bet reveals

🔥 Must include:
- The actual odds/probabilities
- Why this bet is insane/genius/controversial
- Meme-style humor (NPC, degen, regards, etc.)
- A "holy shit" moment

👉 Output: Dialogue script ONLY with emojis before names.

🎯 Topic:
"{market['question']}"

Current odds: {outcomes_str}
Volume: ${market['volume']:,.0f}
Category: {market['category']}
"""
    return prompt


def save_results(markets: list, output_dir: str = "output"):
    """Save scan results"""
    Path(output_dir).mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    
    # Save JSON
    json_path = f"{output_dir}/polymarket_scan_{timestamp}.json"
    with open(json_path, 'w') as f:
        json.dump(markets, f, indent=2)
    
    # Save alert
    alert = generate_alert(markets)
    alert_path = f"{output_dir}/alert_{timestamp}.md"
    with open(alert_path, 'w') as f:
        f.write(alert)
    
    # Save latest
    with open(f"{output_dir}/latest_alert.md", 'w') as f:
        f.write(alert)
    
    # Save script prompts for top 3
    for i, m in enumerate(markets[:3], 1):
        prompt = generate_script_prompt(m)
        prompt_path = f"{output_dir}/script_prompt_{i}_{timestamp}.txt"
        with open(prompt_path, 'w') as f:
            f.write(prompt)
    
    print(f"\n📁 Saved to: {output_dir}/")
    print(f"   - {json_path}")
    print(f"   - {alert_path}")
    print(f"   - Script prompts for top 3 markets")
    
    return alert


def main():
    parser = argparse.ArgumentParser(description='Polymarket Content Scanner')
    parser.add_argument('--limit', '-l', type=int, default=10, help='Number of top markets to return')
    parser.add_argument('--output', '-o', default='output', help='Output directory')
    parser.add_argument('--alert', '-a', action='store_true', help='Print alert to console')
    args = parser.parse_args()
    
    print("🐋 Polymarket Content Engine")
    print("=" * 40)
    
    markets = find_holy_shit_content(limit=args.limit)
    
    if not markets:
        print("❌ No markets found!")
        return
    
    alert = save_results(markets, args.output)
    
    if args.alert:
        print("\n" + alert)
    
    print(f"\n✅ Found {len(markets)} content opportunities!")
    print(f"🔥 Top pick: {markets[0]['question'][:60]}...")


if __name__ == '__main__':
    main()
