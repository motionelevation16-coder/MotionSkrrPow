# MarketPulse API — Business Blueprint

> **One-liner:** The enriched prediction market API that turns raw Polymarket data into developer-ready intelligence.

---

## 1. Competitive Landscape

### Polymarket's Native APIs

Polymarket exposes three separate APIs:

| API | Base URL | Auth | Focus |
|-----|----------|------|-------|
| Gamma API | gamma-api.polymarket.com | None (public) | Market discovery, events, search |
| CLOB API | clob.polymarket.com | Required for trading | Order book, price history, trading |
| Data API | data-api.polymarket.com | None (public) | Positions, trades, leaderboards |

**What Polymarket gives you:**
- Raw market records with ~60+ fields, most irrelevant to most developers
- outcomePrices as JSON strings embedded in JSON ("[\\"0.57\\", \\"0.43\\"]")
- volume24hr, volume fields in raw form
- No computed momentum/trending scores
- No AI summaries or sentiment
- No sentiment labels ("Toss-up", "Strong YES")
- No enriched plain-English context
- Developer experience: raw JSON dumps with cryptographic IDs, Polygon blockchain references, complex nested structures
- No SDK-friendly response shapes

**Polymarket pain points for developers:**
- Category system is inconsistent (tags vs category field)
- Price history requires separate CLOB API call with token IDs
- Pagination is cursor-based but poorly documented
- No single endpoint gives you "the top 20 trending markets right now"

### Kalshi's API

Kalshi is CFTC-regulated (US only), serving event-based markets.

**What Kalshi gives you:**
- REST + WebSocket + FIX 4.4 interfaces
- Token-based auth that expires every 30 minutes (annoying for bots)
- Separate sandbox environment
- Clean endpoint structure: /markets, /events, /orders, /portfolio

**Kalshi pain points:**
- Requires auth even for market data browsing
- US-only, smaller market selection than Polymarket
- FIX protocol complexity is overkill for most developers
- No AI enrichment, no sentiment, no computed scores

### Third-Party / RapidAPI Landscape

**Findings:** As of early 2026, there are no mature prediction market data APIs on RapidAPI. The closest competitor is:

- **Dome (YC W25, domeapi.io):** A unified API for trading across Polymarket + Kalshi. Focused on *trading operations*, not enriched analytics. Targets algo traders, not content/dashboard developers. 50+ developers early. Not on RapidAPI. Positioning: "one API to trade everywhere."

**The gap Dome doesn't fill:** Analytics, AI enrichment, developer-friendly summaries, sentiment, alert drafts. Dome is a trading router. MarketPulse is an intelligence layer.

### The Gap

What developers actually want (based on Discord/Reddit/GitHub discussions):
1. ✅ Clean, pre-parsed market data (no string-encoded JSON, no crypto addresses)
2. ✅ "What's trending right now?" — computed momentum scores
3. ✅ Plain-English explanations of market context (great for news apps, Discord bots)
4. ✅ Sentiment signals before trading
5. ✅ Ready-to-send alert messages for Discord/Telegram bots
6. ✅ Market "quality" scoring — is this market worth trading?
7. ✅ One API key, one endpoint pattern, no auth complexity

---

## 2. Product: MarketPulse API

### Positioning

**"The enriched prediction market API — clean data, AI insights, and bot-ready alerts without the raw data wrangling."**

### Target Users

| User Type | What They're Building | What They Need |
|-----------|----------------------|----------------|
| Discord bot developers | Live prediction market feeds in servers | Trending markets, alert drafts |
| Dashboard builders | Market monitoring UIs | Clean data, categories, trending |
| Trading tool developers | Alpha identification | Market scoring, sentiment analysis |
| News/media apps | Prediction market context for articles | AI summaries, market context |
| Telegram bot builders | Prediction market alerts | Alert drafts, sentiment |
| Researchers / quants | Market analysis | Volume data, scoring, sentiment |

---

## 3. API Endpoints

### Base URL
```
https://api.marketpulse.dev/v1
```

### Authentication
All requests require `X-API-Key: your_key` header.

---

### Endpoint 1: GET /markets/active

Returns enriched active prediction markets.

**Query Parameters:**
| Param | Type | Description | Default |
|-------|------|-------------|---------|
| category | string | Filter by category slug (politics, crypto, sports, etc.) | all |
| min_volume | float | Minimum 24h volume in USD | 0 |
| limit | int | Number of results (1–100) | 20 |
| sort_by | enum | trending \| volume \| closing_soon | trending |

**Response Schema:**
```json
{
  "markets": [
    {
      "id": "540816",
      "title": "Russia-Ukraine Ceasefire before GTA VI?",
      "slug": "russia-ukraine-ceasefire-before-gta-vi-554",
      "url": "https://polymarket.com/event/russia-ukraine-ceasefire-before-gta-vi-554",
      "current_yes_probability": 0.575,
      "current_no_probability": 0.425,
      "volume_24h": 2298.82,
      "total_volume": 1362433.29,
      "liquidity": 64497.0,
      "days_until_resolution": 146,
      "end_date": "2026-07-31T12:00:00Z",
      "category": "politics",
      "trending_score": 7.4,
      "liquidity_rating": "high",
      "price_change_24h": -0.02,
      "price_change_7d": 0.05
    }
  ],
  "total": 847,
  "page": 1,
  "limit": 20
}
```

---

### Endpoint 2: GET /markets/{slug}/summary

Returns enriched single market with AI summary.

**Path Parameter:** slug (market slug from Polymarket)

**Response Schema:**
```json
{
  "id": "540816",
  "title": "Russia-Ukraine Ceasefire before GTA VI?",
  "slug": "russia-ukraine-ceasefire-before-gta-vi-554",
  "url": "https://polymarket.com/event/russia-ukraine-ceasefire-before-gta-vi-554",
  "current_yes_probability": 0.575,
  "current_no_probability": 0.425,
  "volume_24h": 2298.82,
  "total_volume": 1362433.29,
  "liquidity": 64497.0,
  "days_until_resolution": 146,
  "end_date": "2026-07-31T12:00:00Z",
  "category": "politics",
  "trending_score": 7.4,
  "liquidity_rating": "high",
  "price_change_24h": -0.02,
  "price_change_7d": 0.05,
  "sentiment_label": "Leaning YES",
  "ai_summary": "This market asks whether Russia and Ukraine will agree to a ceasefire before Grand Theft Auto VI releases (expected late 2026). The current 57.5% YES probability reflects cautious optimism following recent diplomatic signals from European mediators. Traders are watching ongoing US-brokered talks and the political calendar in Moscow, with the market pricing in roughly even odds given the historically low success rate of ceasefires in this conflict.",
  "price_history": [
    {"date": "2026-03-01", "yes_price": 0.55},
    {"date": "2026-03-02", "yes_price": 0.57},
    {"date": "2026-03-03", "yes_price": 0.56},
    {"date": "2026-03-04", "yes_price": 0.59},
    {"date": "2026-03-05", "yes_price": 0.61},
    {"date": "2026-03-06", "yes_price": 0.58},
    {"date": "2026-03-07", "yes_price": 0.575}
  ]
}
```

---

### Endpoint 3: POST /markets/score

AI scoring of a prediction market.

**Request Body:**
```json
{
  "title": "Will the Fed cut rates in March 2026?",
  "current_yes_prob": 0.73
}
```

**Response Schema:**
```json
{
  "title": "Will the Fed cut rates in March 2026?",
  "current_yes_prob": 0.73,
  "info_efficiency": 7,
  "volatility_expectation": "medium",
  "trade_attractiveness": 6,
  "reasoning": "At 73% YES, this market is fairly liquid and appears reasonably efficient — Fed rate decisions are heavily telegraphed and analyzed. The risk of a surprise is medium, as recent macro data has been mixed. The price has likely already absorbed most public information.",
  "suggested_research": [
    "Review the latest FOMC meeting minutes and dot plot projections",
    "Check the CME FedWatch Tool for consensus positioning vs this market",
    "Monitor upcoming CPI and jobs report releases before the FOMC meeting date"
  ]
}
```

---

### Endpoint 4: POST /sentiment/analyze

AI sentiment analysis for a prediction market topic.

**Request Body:**
```json
{
  "topic": "US presidential election outcomes 2028"
}
```

**Response Schema:**
```json
{
  "topic": "US presidential election outcomes 2028",
  "sentiment_score": 0.15,
  "sentiment_label": "neutral",
  "key_factors": [
    "High uncertainty this far from the election date",
    "No confirmed candidates from either major party yet",
    "Historical incumbency advantage if current administration runs"
  ],
  "confidence": "low",
  "summary": "Prediction market sentiment on 2028 election outcomes is broadly neutral with slight optimism for the incumbent party, though the signal is weak given the 2+ year horizon. Markets historically show low conviction on election outcomes this far in advance."
}
```

---

### Endpoint 5: GET /categories

Returns market categories with counts.

**Response Schema:**
```json
{
  "categories": [
    {"slug": "politics", "label": "Politics", "active_market_count": 142},
    {"slug": "crypto", "label": "Crypto", "active_market_count": 98},
    {"slug": "sports", "label": "Sports", "active_market_count": 87},
    {"slug": "finance", "label": "Finance", "active_market_count": 76},
    {"slug": "tech", "label": "Tech", "active_market_count": 64},
    {"slug": "world", "label": "World", "active_market_count": 58},
    {"slug": "science", "label": "Science", "active_market_count": 34},
    {"slug": "economy", "label": "Economy", "active_market_count": 29}
  ],
  "total_active_markets": 847,
  "updated_at": "2026-03-07T16:00:00Z"
}
```

---

### Endpoint 6: POST /alert/draft

Generates formatted alert messages for Discord/Telegram bots.

**Request Body:**
```json
{
  "market_title": "Will Bitcoin hit $150k in 2026?",
  "condition": "above_70",
  "threshold": 0.70
}
```

**Response Schema:**
```json
{
  "market_title": "Will Bitcoin hit $150k in 2026?",
  "condition": "above_70",
  "threshold": 0.70,
  "short_alert": "🔔 **BTC $150k 2026** — YES crossed **70%** on Polymarket",
  "detailed_alert": "📊 **Prediction Market Alert**\n\n**Market:** Will Bitcoin hit $150k in 2026?\n**Signal:** YES probability crossed above **70%** 🔺\n**Current odds:** 70% YES / 30% NO\n\n💡 *This threshold crossing may indicate building momentum. Polymarket traders appear increasingly confident in a Bitcoin surge to $150k this year.*\n\n🔗 [View on Polymarket](https://polymarket.com)",
  "telegram_format": "🔔 <b>Market Alert</b>\n\n<b>Will Bitcoin hit $150k in 2026?</b>\nYES crossed <b>70%</b> 🔺\n\n💡 Traders signaling strong confidence. Consider doing your own research before acting.",
  "generated_at": "2026-03-07T16:00:00Z"
}
```

---

## 4. Pricing Tiers

Competitive positioning: undercut any paid alternatives, match Dome's implied pricing.

| Tier | Price | Requests/month | Features |
|------|-------|----------------|----------|
| **Free** | $0 | 500 | /markets/active, /categories only. No AI endpoints. Rate limited to 10 req/min |
| **Starter** | $9/month | 5,000 | All endpoints. 30 req/min. Email support |
| **Pro** | $29/month | 25,000 | All endpoints. 100 req/min. Priority support |
| **Builder** | $79/month | 100,000 | All endpoints. 300 req/min. Webhook alerts, priority support |
| **Enterprise** | Custom | Unlimited | Custom rate limits, SLA, onboarding |

**Why this pricing works:**
- Free tier drives RapidAPI discovery and word-of-mouth
- $9 Starter is impulse-buy territory for hobbyists
- $29 Pro is casual Discord bot builder tier
- $79 Builder is for production bots doing real volume
- No existing product offers this at these price points

---

## 5. Unique Differentiators

1. **Trending Score** — computed momentum metric (volume acceleration over 24h vs 7d baseline), something neither Polymarket nor Kalshi provides
2. **AI Summaries** — plain English "what is this market about" context, perfect for news apps and Discord bots
3. **Sentiment Labels** — Strong YES / Leaning YES / Toss-up / Leaning NO / Strong NO mapping
4. **Market Scoring** — quality signal for traders: is this market worth entering?
5. **Alert Draft Generator** — copy-paste ready Discord/Telegram messages, zero formatting work
6. **Clean Data Contract** — no string-encoded JSON arrays, no blockchain addresses, consistent field names
7. **One endpoint for discovery** — no need to stitch together 3 different Polymarket APIs

---

## 6. Distribution Plan

### Phase 1: Launch (Month 1–2)
- Deploy on Railway (same as HookScore)
- List on RapidAPI (free tier first, then paid)
- GitHub README with working examples
- Post on r/algotrading, r/predictionmarkets, r/discord
- Dev.to article: "Building a Polymarket Discord Bot in 10 Minutes"

### Phase 2: Growth (Month 3–6)
- Twitter/X presence targeting prediction market community
- Polymarket community Discord — be genuinely helpful
- Cold outreach to prediction market newsletter writers
- YouTube demo: "Real-Time Prediction Market Bot"

### Phase 3: Scale (Month 6+)
- Partner with prediction market educators/influencers
- Add Kalshi data (unified layer like Dome, but enriched)
- Consider webhook/push model for Pro+

---

## 7. Revenue Timeline Estimate

| Month | Scenario | MRR |
|-------|----------|-----|
| 1 | Launch, first 10 users on free | $0 |
| 2 | 3 Starter, 1 Pro | $56 |
| 3 | 8 Starter, 3 Pro, 1 Builder | $238 |
| 6 | 20 Starter, 10 Pro, 4 Builder | $806 |
| 12 | 50 Starter, 25 Pro, 10 Builder, 2 Enterprise | $2,245+ |

Conservative path to $500 MRR: ~Month 5–7
Conservative path to $1,000 MRR: ~Month 9–12

---

## 8. Tech Stack

- **Framework:** FastAPI (Python)
- **Data source:** Polymarket Gamma API (public, no auth)
- **AI:** OpenAI GPT-4o-mini (JSON mode)
- **Deploy:** Railway
- **API keys:** Environment variable, simple header-based auth
- **Caching:** In-memory LRU cache, 5-minute TTL on market data

---

*Blueprint version 1.0 — March 2026*
