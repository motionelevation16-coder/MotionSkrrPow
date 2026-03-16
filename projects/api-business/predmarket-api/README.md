# PredMarket API

**Prediction market intelligence — Polymarket + Kalshi in one API.**

Clean data, AI-generated summaries, market scoring, sentiment analysis, and opportunity detection. Built for traders, bot builders, and researchers.

---

## Features

| Endpoint | What it does |
|---|---|
| `GET /markets` | Browse active/resolved markets with platform + category filters |
| `GET /markets/{id}/summary` | AI-generated market analysis with trend + momentum |
| `POST /markets/score` | Score any market question for quality (clarity, tradability) |
| `POST /sentiment` | AI sentiment for any prediction market topic |
| `GET /opportunities` | AI-identified trading opportunities across all markets |

---

## Quick Start

### 1. Clone & install

```bash
git clone https://github.com/your-username/predmarket-api
cd predmarket-api
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — add your OPENAI_API_KEY
```

### 3. Run locally

```bash
uvicorn main:app --reload --port 8000
```

Visit: http://localhost:8000/docs

---

## Deploy to Railway (recommended)

1. Push to GitHub
2. Create new project on [Railway](https://railway.app)
3. Connect your repo
4. Add `OPENAI_API_KEY` in Railway environment variables
5. Railway auto-detects `railway.json` and deploys

Done. Your API is live at `https://your-app.railway.app`

---

## API Examples

### Get active politics markets
```bash
curl "https://your-app.railway.app/markets?platform=polymarket&category=politics&limit=10"
```

### Get market summary
```bash
curl "https://your-app.railway.app/markets/ukraine-ceasefire-june-2026/summary"
```

### Score a market question
```bash
curl -X POST "https://your-app.railway.app/markets/score" \
  -H "Content-Type: application/json" \
  -d '{"question": "Will Tesla stock be above $300 by Dec 31, 2026?"}'
```

### Get topic sentiment
```bash
curl -X POST "https://your-app.railway.app/sentiment" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Trump tariffs", "context": "prediction market"}'
```

### Get opportunities
```bash
curl "https://your-app.railway.app/opportunities"
```

---

## Switching from Mock to Real API Data

The API ships with realistic mock data (22 markets). Plugging in real data takes ~10 minutes:

### Polymarket (free, no auth needed)

In `mock_data.py`, find the `filter_markets()` function and replace its body:

```python
import httpx

def filter_markets(platform="both", category="all", status="active", limit=20):
    markets = []

    if platform in ("polymarket", "both"):
        r = httpx.get(
            "https://gamma-api.polymarket.com/markets",
            params={"active": True, "limit": 100},
            timeout=10
        )
        for m in r.json():
            markets.append({
                "id": m["slug"],
                "platform": "polymarket",
                "question": m["question"],
                "category": categorize(m.get("tags", [])),  # write a category mapper
                "yes_probability": float(m.get("outcomePrices", [0.5])[0]),
                "no_probability": 1 - float(m.get("outcomePrices", [0.5])[0]),
                "volume_24h": float(m.get("volume24hr", 0)),
                "total_volume": float(m.get("volume", 0)),
                "resolution_date": m.get("endDate", ""),
                "days_remaining": calc_days(m.get("endDate")),
                "status": "active" if m.get("active") else "resolved",
                "url": f"https://polymarket.com/event/{m['slug']}",
                "tags": m.get("tags", []),
            })

    # Filter + return
    if category != "all":
        markets = [m for m in markets if m["category"] == category]
    return markets[:limit]
```

### Kalshi (requires API key)

```python
import httpx

KALSHI_API_KEY = os.getenv("KALSHI_API_KEY")

def fetch_kalshi_markets(limit=100):
    r = httpx.get(
        "https://api.elections.kalshi.com/trade-api/v2/markets",
        headers={"Authorization": f"Bearer {KALSHI_API_KEY}"},
        params={"limit": limit, "status": "open"},
        timeout=10
    )
    markets = []
    for m in r.json().get("markets", []):
        markets.append({
            "id": m["ticker"],
            "platform": "kalshi",
            "question": m["title"],
            "category": map_kalshi_category(m.get("category", "")),
            "yes_probability": float(m.get("last_price", 0.5)),
            "no_probability": 1 - float(m.get("last_price", 0.5)),
            "volume_24h": float(m.get("dollar_recent_volume", 0)),
            "total_volume": float(m.get("dollar_volume", 0)),
            "resolution_date": m.get("close_time", "")[:10],
            "days_remaining": calc_days(m.get("close_time")),
            "status": "active",
            "url": f"https://kalshi.com/markets/{m['ticker']}",
            "tags": [],
        })
    return markets
```

---

## Architecture

```
predmarket-api/
├── main.py          — FastAPI app, all endpoints, OpenAI calls
├── mock_data.py     — 22 realistic mock markets + filter logic
├── requirements.txt
├── railway.json     — Railway deployment config
├── Procfile         — Heroku/Render compatible
├── .env.example     — Environment variable template
├── README.md        — This file
├── rapidapi-listing.md  — RapidAPI marketplace copy
└── blueprint.md     — Business strategy + competitive analysis
```

---

## Tech Stack

- **FastAPI** — async Python web framework
- **Pydantic v2** — request/response validation
- **OpenAI GPT-4o-mini** — AI features (JSON mode enforced)
- **httpx** — async HTTP client for real API calls (when enabled)
- **Railway** — recommended deployment platform

---

## License

MIT
