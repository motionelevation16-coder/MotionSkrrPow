# PredMarket API — RapidAPI Listing

## Short Description (160 chars)
Clean, enriched prediction market data from Polymarket + Kalshi. AI summaries, market scoring, sentiment analysis, and opportunity detection.

## Long Description

**The prediction market data layer you've been waiting for.**

Polymarket and Kalshi have raw APIs — but they're not built for developers who want enriched, analysis-ready data. PredMarket API bridges that gap.

### What you get:
- ✅ **Unified data** — Polymarket + Kalshi in one clean response format
- ✅ **AI-generated summaries** — natural language analysis of any market
- ✅ **Market quality scoring** — grade any question before trading it
- ✅ **Topic sentiment** — AI-powered directional bias for any topic
- ✅ **Opportunity detection** — mispricings, momentum plays, near-resolution alerts
- ✅ **Computed fields** — days_remaining, volume ratios, probability formatting

### Perfect for:
- Prediction market traders who want analysis at scale
- Bot builders automating trading strategies
- Researchers studying market efficiency
- Dashboard builders and aggregators
- Journalists tracking prediction market signals

### Free tier available — get started in 60 seconds.

---

## Category
Finance → Financial Data

## Tags
prediction markets, polymarket, kalshi, AI, trading, financial data, sentiment analysis, forecasting

---

## Endpoints

---

### 1. GET /markets

**Browse prediction markets with filters**

Returns a list of markets from Polymarket and/or Kalshi, with clean computed fields.

**Query Parameters:**
| Parameter | Type | Default | Options |
|---|---|---|---|
| platform | string | both | polymarket, kalshi, both |
| category | string | all | politics, crypto, sports, economics, science, all |
| status | string | active | active, resolved, all |
| limit | integer | 20 | 1–100 |

**Example Request:**
```
GET /markets?platform=polymarket&category=crypto&limit=5
```

**Example Response:**
```json
{
  "count": 5,
  "markets": [
    {
      "id": "bitcoin-above-100k-june-2026",
      "platform": "polymarket",
      "question": "Will Bitcoin be above $100,000 on June 30, 2026?",
      "category": "crypto",
      "yes_probability": 0.63,
      "no_probability": 0.37,
      "volume_24h": 531000,
      "total_volume": 12400000,
      "resolution_date": "2026-06-30",
      "days_remaining": 115,
      "status": "active",
      "url": "https://polymarket.com/event/bitcoin-100k-june-2026",
      "tags": ["Bitcoin", "BTC", "crypto price"]
    },
    {
      "id": "eth-etf-net-positive-q2-2026",
      "platform": "kalshi",
      "question": "Will Ethereum ETFs see net positive inflows in Q2 2026?",
      "category": "crypto",
      "yes_probability": 0.71,
      "no_probability": 0.29,
      "volume_24h": 88700,
      "total_volume": 1980000,
      "resolution_date": "2026-06-30",
      "days_remaining": 115,
      "status": "active",
      "url": "https://kalshi.com/markets/ETH-ETF-Q2-INFLOW",
      "tags": ["Ethereum", "ETH", "ETF", "institutional"]
    }
  ],
  "filters_applied": {
    "platform": "polymarket",
    "category": "crypto",
    "status": "active",
    "limit": 5
  },
  "data_source": "live"
}
```

---

### 2. GET /markets/{market_id}/summary

**AI-generated market summary and analysis**

Returns natural language analysis, trend direction, momentum score, and confidence level.

**Path Parameters:**
| Parameter | Type | Description |
|---|---|---|
| market_id | string | Market slug ID from /markets |

**Example Request:**
```
GET /markets/ukraine-ceasefire-june-2026/summary
```

**Example Response:**
```json
{
  "market_id": "ukraine-ceasefire-june-2026",
  "question": "Will a Ukraine ceasefire agreement be signed by June 2026?",
  "platform": "polymarket",
  "current_odds": {
    "yes": 0.58,
    "no": 0.42
  },
  "ai_summary": "This market is currently trading at 58% YES probability, reflecting cautious optimism following recent diplomatic signals from both the US and European mediators. The market has seen a 6-point YES increase over the past two weeks, driven by reported backchannel negotiations and US pressure on both sides. Key risk factors: stalled frontline positions could derail talks, and domestic political opposition in both countries remains a significant wildcard.",
  "trend": "rising_yes",
  "momentum_score": 68,
  "confidence": "medium",
  "generated_at": "2026-03-07T14:23:11Z"
}
```

---

### 3. POST /markets/score

**Score a prediction market question for quality**

AI-powered evaluation of any market question. Graded on clarity, tradability, resolution criteria, and potential issues.

**Request Body:**
```json
{
  "question": "Will Tesla stock be above $300 by Dec 31, 2026?",
  "context": "Tesla Q4 earnings beat expectations, new model launch in Q2"
}
```

**Example Response:**
```json
{
  "question": "Will Tesla stock be above $300 by Dec 31, 2026?",
  "quality_score": 87,
  "grade": "A-",
  "clarity": "High — unambiguous resolution criteria with a specific price level and exact date",
  "tradability": "High — liquid underlying asset with clear catalysts and institutional participation",
  "issues": [
    "Year-end resolution may cause liquidity concentration near December, widening spreads",
    "Stock price can gap significantly on earnings or macro events, making late positioning risky"
  ],
  "verdict": "Well-structured market with clear, measurable resolution criteria and a meaningful timeframe. The specific price threshold and deadline make this highly tradable. Minor concern around year-end liquidity compression.",
  "similar_markets": [
    "Will Tesla stock exceed $400 by end of 2026?",
    "Will Tesla Model Y remain the best-selling EV in 2026?",
    "Will Tesla achieve profitability in Q4 2026?"
  ]
}
```

---

### 4. POST /sentiment

**AI sentiment analysis for a prediction market topic**

Returns directional bias, sentiment score (-100 to +100), reasoning, and a recommended position.

**Request Body:**
```json
{
  "topic": "Trump tariffs on China",
  "context": "prediction market"
}
```

**Example Response:**
```json
{
  "topic": "Trump tariffs on China",
  "sentiment": "bullish_yes",
  "sentiment_score": 34,
  "reasoning": "Recent executive orders and public statements suggest Trump is committed to escalating tariffs as a negotiating tool. Market signals on related trade policy markets have drifted higher YES over the past 30 days. However, the risk of a negotiated deal caps strong upside, keeping sentiment moderately positive rather than strongly bullish.",
  "keywords": ["tariffs", "trade war", "executive order", "China relations", "Section 301"],
  "recommended_position": "Lean YES with position sizing — uncertainty remains elevated",
  "confidence": "medium",
  "disclaimer": "Not financial advice. For research and entertainment purposes only."
}
```

---

### 5. GET /opportunities

**AI-identified trading opportunities**

Scans all active markets for mispricings, high momentum plays, near-resolution opportunities, and contrarian signals.

**Example Request:**
```
GET /opportunities
```

**Example Response:**
```json
{
  "count": 4,
  "opportunities": [
    {
      "market_id": "solana-above-200-march-2026",
      "question": "Will Solana (SOL) be above $200 at end of March 2026?",
      "platform": "polymarket",
      "type": "near_resolution",
      "description": "This market resolves in 24 days with SOL at 38% YES. High 24h volume ($142K) suggests active repositioning near expiry — typical for near-resolution markets where the final price move can be decisive.",
      "urgency": "high",
      "days_remaining": 24,
      "yes_probability": 0.38
    },
    {
      "market_id": "ukraine-ceasefire-june-2026",
      "question": "Will a Ukraine ceasefire agreement be signed by June 2026?",
      "platform": "polymarket",
      "type": "high_momentum",
      "description": "With $392K in 24h volume (highest in the dataset) and 58% YES probability, this market is seeing exceptional engagement. The volume spike suggests significant new information or institutional positioning.",
      "urgency": "medium",
      "days_remaining": 115,
      "yes_probability": 0.58
    },
    {
      "market_id": "us-cpi-above-3-april-2026",
      "question": "Will US CPI (YoY) be above 3% in the April 2026 report?",
      "platform": "kalshi",
      "type": "mispriced",
      "description": "At 48% YES, this market is nearly coin-flip while recent CPI data suggests persistence above 3% is more likely than below. Comparable inflation markets on other platforms price this at 55-60% YES.",
      "urgency": "medium",
      "days_remaining": 39,
      "yes_probability": 0.48
    },
    {
      "market_id": "bitcoin-ath-q1-2026",
      "question": "Will Bitcoin set a new all-time high in Q1 2026?",
      "platform": "polymarket",
      "type": "contrarian",
      "description": "44% YES with only 24 days remaining. With BTC needing to exceed its ATH in a very short window, YES appears crowded relative to the remaining time. NO at 56% may be undervalued given the tight timeline.",
      "urgency": "high",
      "days_remaining": 24,
      "yes_probability": 0.44
    }
  ],
  "analysis_note": "Current market conditions show elevated activity in geopolitical and crypto markets. Near-resolution markets in crypto present the highest time-sensitive opportunities this week.",
  "generated_at": "2026-03-07T14:23:11Z"
}
```

---

### 6. GET /health

**API health check**

**Example Response:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "ai_enabled": true,
  "data_source": "live",
  "timestamp": "2026-03-07T14:23:11Z"
}
```

---

## Pricing Tiers

| Plan | Price | Calls/month | Endpoints |
|---|---|---|---|
| Free | $0 | 50 | /markets, /markets/{id}/summary |
| Basic | $4.99 | 1,000 | All endpoints |
| Pro | $12.99 | 5,000 | All endpoints |
| Ultra | $24.99 | 20,000 | All endpoints + priority support |

---

## Authentication

All requests require your RapidAPI key in the header:
```
X-RapidAPI-Key: YOUR_KEY_HERE
X-RapidAPI-Host: predmarket-api.p.rapidapi.com
```

---

## Error Codes

| Code | Meaning |
|---|---|
| 400 | Bad request — invalid parameter |
| 404 | Market not found |
| 503 | AI service temporarily unavailable |
| 429 | Rate limit exceeded — upgrade your plan |
