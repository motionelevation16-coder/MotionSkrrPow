"""
mock_data.py — Realistic mock market data for PredMarket API

These markets are realistic representations of what Polymarket and Kalshi offer.
When integrating real APIs, replace the MOCK_MARKETS list with live API calls.

See main.py for WHERE to plug in real API calls.
"""

from datetime import datetime, date

# Reference date for days_remaining calculations
REFERENCE_DATE = date(2026, 3, 7)

MOCK_MARKETS = [
    # ── POLITICS ──────────────────────────────────────────────────────────────
    {
        "id": "us-midterms-dem-house-2026",
        "platform": "polymarket",
        "question": "Will Democrats win the House in the 2026 midterms?",
        "category": "politics",
        "yes_probability": 0.41,
        "no_probability": 0.59,
        "volume_24h": 284000,
        "total_volume": 4_120_000,
        "resolution_date": "2026-11-10",
        "days_remaining": 248,
        "status": "active",
        "url": "https://polymarket.com/event/democrats-win-house-2026",
        "tags": ["US politics", "midterms", "Congress"],
    },
    {
        "id": "trump-approval-above-50-q2-2026",
        "platform": "kalshi",
        "question": "Will Trump's approval rating exceed 50% in Q2 2026?",
        "category": "politics",
        "yes_probability": 0.22,
        "no_probability": 0.78,
        "volume_24h": 47500,
        "total_volume": 612_000,
        "resolution_date": "2026-06-30",
        "days_remaining": 115,
        "status": "active",
        "url": "https://kalshi.com/markets/TRUMP-APPROVE-50",
        "tags": ["Trump", "approval", "polls"],
    },
    {
        "id": "france-snap-election-2026",
        "platform": "polymarket",
        "question": "Will France hold a snap election before July 2026?",
        "category": "politics",
        "yes_probability": 0.31,
        "no_probability": 0.69,
        "volume_24h": 18900,
        "total_volume": 245_000,
        "resolution_date": "2026-07-01",
        "days_remaining": 116,
        "status": "active",
        "url": "https://polymarket.com/event/france-snap-election-2026",
        "tags": ["France", "Europe", "elections"],
    },
    {
        "id": "ukraine-ceasefire-june-2026",
        "platform": "polymarket",
        "question": "Will a Ukraine ceasefire agreement be signed by June 2026?",
        "category": "politics",
        "yes_probability": 0.58,
        "no_probability": 0.42,
        "volume_24h": 392_000,
        "total_volume": 8_750_000,
        "resolution_date": "2026-06-30",
        "days_remaining": 115,
        "status": "active",
        "url": "https://polymarket.com/event/ukraine-ceasefire-2026",
        "tags": ["Ukraine", "war", "Russia", "geopolitics"],
    },
    {
        "id": "us-tariffs-china-above-30",
        "platform": "kalshi",
        "question": "Will US tariffs on Chinese goods exceed 30% in 2026?",
        "category": "politics",
        "yes_probability": 0.47,
        "no_probability": 0.53,
        "volume_24h": 63_200,
        "total_volume": 1_050_000,
        "resolution_date": "2026-12-31",
        "days_remaining": 299,
        "status": "active",
        "url": "https://kalshi.com/markets/US-TARIFF-CHINA-30",
        "tags": ["tariffs", "trade war", "China", "Trump"],
    },

    # ── CRYPTO ────────────────────────────────────────────────────────────────
    {
        "id": "bitcoin-above-100k-june-2026",
        "platform": "polymarket",
        "question": "Will Bitcoin be above $100,000 on June 30, 2026?",
        "category": "crypto",
        "yes_probability": 0.63,
        "no_probability": 0.37,
        "volume_24h": 531_000,
        "total_volume": 12_400_000,
        "resolution_date": "2026-06-30",
        "days_remaining": 115,
        "status": "active",
        "url": "https://polymarket.com/event/bitcoin-100k-june-2026",
        "tags": ["Bitcoin", "BTC", "crypto price"],
    },
    {
        "id": "eth-etf-net-positive-q2-2026",
        "platform": "kalshi",
        "question": "Will Ethereum ETFs see net positive inflows in Q2 2026?",
        "category": "crypto",
        "yes_probability": 0.71,
        "no_probability": 0.29,
        "volume_24h": 88_700,
        "total_volume": 1_980_000,
        "resolution_date": "2026-06-30",
        "days_remaining": 115,
        "status": "active",
        "url": "https://kalshi.com/markets/ETH-ETF-Q2-INFLOW",
        "tags": ["Ethereum", "ETH", "ETF", "institutional"],
    },
    {
        "id": "solana-above-200-march-2026",
        "platform": "polymarket",
        "question": "Will Solana (SOL) be above $200 at end of March 2026?",
        "category": "crypto",
        "yes_probability": 0.38,
        "no_probability": 0.62,
        "volume_24h": 142_000,
        "total_volume": 3_200_000,
        "resolution_date": "2026-03-31",
        "days_remaining": 24,
        "status": "active",
        "url": "https://polymarket.com/event/solana-200-march-2026",
        "tags": ["Solana", "SOL", "altcoin"],
    },
    {
        "id": "us-crypto-reserve-bill-2026",
        "platform": "kalshi",
        "question": "Will the US Strategic Crypto Reserve bill pass in 2026?",
        "category": "crypto",
        "yes_probability": 0.29,
        "no_probability": 0.71,
        "volume_24h": 205_000,
        "total_volume": 5_640_000,
        "resolution_date": "2026-12-31",
        "days_remaining": 299,
        "status": "active",
        "url": "https://kalshi.com/markets/US-CRYPTO-RESERVE-2026",
        "tags": ["regulation", "crypto", "US policy", "Bitcoin reserve"],
    },
    {
        "id": "bitcoin-ath-q1-2026",
        "platform": "polymarket",
        "question": "Will Bitcoin set a new all-time high in Q1 2026?",
        "category": "crypto",
        "yes_probability": 0.44,
        "no_probability": 0.56,
        "volume_24h": 317_000,
        "total_volume": 7_100_000,
        "resolution_date": "2026-03-31",
        "days_remaining": 24,
        "status": "active",
        "url": "https://polymarket.com/event/bitcoin-ath-q1-2026",
        "tags": ["Bitcoin", "ATH", "price"],
    },

    # ── SPORTS ────────────────────────────────────────────────────────────────
    {
        "id": "nba-lakers-championship-2026",
        "platform": "kalshi",
        "question": "Will the LA Lakers win the 2026 NBA Championship?",
        "category": "sports",
        "yes_probability": 0.12,
        "no_probability": 0.88,
        "volume_24h": 38_400,
        "total_volume": 892_000,
        "resolution_date": "2026-06-25",
        "days_remaining": 110,
        "status": "active",
        "url": "https://kalshi.com/markets/NBA-LAKERS-CHAMP-2026",
        "tags": ["NBA", "Lakers", "basketball"],
    },
    {
        "id": "world-cup-2026-brazil-winner",
        "platform": "polymarket",
        "question": "Will Brazil win the 2026 FIFA World Cup?",
        "category": "sports",
        "yes_probability": 0.17,
        "no_probability": 0.83,
        "volume_24h": 75_600,
        "total_volume": 2_340_000,
        "resolution_date": "2026-07-19",
        "days_remaining": 134,
        "status": "active",
        "url": "https://polymarket.com/event/world-cup-2026-winner",
        "tags": ["FIFA", "World Cup", "soccer", "football"],
    },
    {
        "id": "nfl-super-bowl-lxi-winner",
        "platform": "kalshi",
        "question": "Will the Kansas City Chiefs win Super Bowl LXI?",
        "category": "sports",
        "yes_probability": 0.23,
        "no_probability": 0.77,
        "volume_24h": 121_000,
        "total_volume": 3_450_000,
        "resolution_date": "2027-02-07",
        "days_remaining": 337,
        "status": "active",
        "url": "https://kalshi.com/markets/NFL-SB-LXI-KC",
        "tags": ["NFL", "Super Bowl", "Chiefs", "football"],
    },

    # ── ECONOMICS ─────────────────────────────────────────────────────────────
    {
        "id": "fed-rate-cut-may-2026",
        "platform": "kalshi",
        "question": "Will the Fed cut interest rates at the May 2026 FOMC meeting?",
        "category": "economics",
        "yes_probability": 0.34,
        "no_probability": 0.66,
        "volume_24h": 198_000,
        "total_volume": 6_200_000,
        "resolution_date": "2026-05-07",
        "days_remaining": 61,
        "status": "active",
        "url": "https://kalshi.com/markets/FED-RATE-CUT-MAY-2026",
        "tags": ["Fed", "interest rates", "FOMC", "monetary policy"],
    },
    {
        "id": "us-recession-2026",
        "platform": "polymarket",
        "question": "Will the US enter a recession in 2026?",
        "category": "economics",
        "yes_probability": 0.39,
        "no_probability": 0.61,
        "volume_24h": 267_000,
        "total_volume": 9_800_000,
        "resolution_date": "2026-12-31",
        "days_remaining": 299,
        "status": "active",
        "url": "https://polymarket.com/event/us-recession-2026",
        "tags": ["recession", "GDP", "economy", "US"],
    },
    {
        "id": "sp500-above-6000-q2-2026",
        "platform": "kalshi",
        "question": "Will the S&P 500 close above 6,000 at end of Q2 2026?",
        "category": "economics",
        "yes_probability": 0.55,
        "no_probability": 0.45,
        "volume_24h": 89_400,
        "total_volume": 2_150_000,
        "resolution_date": "2026-06-30",
        "days_remaining": 115,
        "status": "active",
        "url": "https://kalshi.com/markets/SP500-6000-Q2-2026",
        "tags": ["S&P 500", "stocks", "equities"],
    },
    {
        "id": "us-cpi-above-3-april-2026",
        "platform": "kalshi",
        "question": "Will US CPI (YoY) be above 3% in the April 2026 report?",
        "category": "economics",
        "yes_probability": 0.48,
        "no_probability": 0.52,
        "volume_24h": 54_200,
        "total_volume": 1_120_000,
        "resolution_date": "2026-04-15",
        "days_remaining": 39,
        "status": "active",
        "url": "https://kalshi.com/markets/CPI-3PCT-APR-2026",
        "tags": ["inflation", "CPI", "Fed", "economy"],
    },

    # ── SCIENCE & TECH ────────────────────────────────────────────────────────
    {
        "id": "openai-gpt5-release-2026",
        "platform": "polymarket",
        "question": "Will OpenAI release GPT-5 before December 2026?",
        "category": "science",
        "yes_probability": 0.78,
        "no_probability": 0.22,
        "volume_24h": 93_100,
        "total_volume": 2_780_000,
        "resolution_date": "2026-12-01",
        "days_remaining": 269,
        "status": "active",
        "url": "https://polymarket.com/event/openai-gpt5-2026",
        "tags": ["AI", "OpenAI", "GPT", "tech"],
    },
    {
        "id": "spacex-starship-orbit-2026",
        "platform": "polymarket",
        "question": "Will SpaceX Starship complete a full orbital mission by mid-2026?",
        "category": "science",
        "yes_probability": 0.69,
        "no_probability": 0.31,
        "volume_24h": 41_800,
        "total_volume": 1_340_000,
        "resolution_date": "2026-06-30",
        "days_remaining": 115,
        "status": "active",
        "url": "https://polymarket.com/event/spacex-starship-orbit-2026",
        "tags": ["SpaceX", "Starship", "space", "Musk"],
    },
    {
        "id": "tesla-robotaxi-launch-2026",
        "platform": "kalshi",
        "question": "Will Tesla launch a commercial robotaxi service in the US by end of 2026?",
        "category": "science",
        "yes_probability": 0.52,
        "no_probability": 0.48,
        "volume_24h": 68_300,
        "total_volume": 1_890_000,
        "resolution_date": "2026-12-31",
        "days_remaining": 299,
        "status": "active",
        "url": "https://kalshi.com/markets/TESLA-ROBOTAXI-2026",
        "tags": ["Tesla", "autonomous vehicles", "Musk", "EV"],
    },

    # ── RESOLVED (examples) ──────────────────────────────────────────────────
    {
        "id": "trump-inauguration-jan-2025",
        "platform": "polymarket",
        "question": "Will Trump be inaugurated as US President in January 2025?",
        "category": "politics",
        "yes_probability": 1.0,
        "no_probability": 0.0,
        "volume_24h": 0,
        "total_volume": 48_200_000,
        "resolution_date": "2025-01-20",
        "days_remaining": 0,
        "status": "resolved",
        "url": "https://polymarket.com/event/trump-inauguration-2025",
        "tags": ["Trump", "US politics", "president"],
    },
    {
        "id": "bitcoin-above-50k-2024",
        "platform": "polymarket",
        "question": "Will Bitcoin close above $50,000 at any point in 2024?",
        "category": "crypto",
        "yes_probability": 1.0,
        "no_probability": 0.0,
        "volume_24h": 0,
        "total_volume": 21_500_000,
        "resolution_date": "2024-12-31",
        "days_remaining": 0,
        "status": "resolved",
        "url": "https://polymarket.com/event/bitcoin-50k-2024",
        "tags": ["Bitcoin", "BTC", "price"],
    },
]


def get_market_by_id(market_id: str) -> dict | None:
    """Look up a market by its slug ID."""
    for market in MOCK_MARKETS:
        if market["id"] == market_id:
            return market
    return None


def filter_markets(
    platform: str = "both",
    category: str = "all",
    status: str = "active",
    limit: int = 20,
) -> list[dict]:
    """
    Filter mock markets by platform, category, and status.

    ── REAL API INTEGRATION POINT ────────────────────────────────────────────
    Replace this function body with real API calls:

    POLYMARKET:
        Gamma Markets API: https://gamma-api.polymarket.com/markets
        Docs: https://docs.polymarket.com
        Params: active=true, limit=100, offset=0
        Auth: No auth needed for public data

    KALSHI:
        REST API: https://api.elections.kalshi.com/trade-api/v2/markets
        Docs: https://trading-api.kalshi.com/docs
        Auth: Bearer token (API key required)

    Then normalize the response to match the Market schema in main.py.
    ──────────────────────────────────────────────────────────────────────────
    """
    results = MOCK_MARKETS.copy()

    # Filter by platform
    if platform != "both":
        results = [m for m in results if m["platform"] == platform]

    # Filter by category
    if category != "all":
        results = [m for m in results if m["category"] == category]

    # Filter by status
    if status != "all":
        results = [m for m in results if m["status"] == status]

    # Apply limit
    return results[:limit]
