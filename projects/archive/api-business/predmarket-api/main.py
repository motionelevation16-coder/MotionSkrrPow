"""
MarketPulse API — Enriched Prediction Market Intelligence
FastAPI app serving enriched Polymarket data with AI-powered insights.
"""

import os
import json
import time
import math
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Literal
from functools import lru_cache

import httpx
from fastapi import FastAPI, HTTPException, Query, Path, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import AsyncOpenAI

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────

POLYMARKET_GAMMA = "https://gamma-api.polymarket.com"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
API_KEY = os.getenv("MARKETPULSE_API_KEY", "dev-key-12345")  # Override in prod
CACHE_TTL_SECONDS = 300  # 5 minutes

openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# ─────────────────────────────────────────────
# Simple in-memory cache
# ─────────────────────────────────────────────

_cache: dict = {}

def cache_get(key: str):
    entry = _cache.get(key)
    if entry and time.time() - entry["ts"] < CACHE_TTL_SECONDS:
        return entry["data"]
    return None

def cache_set(key: str, data):
    _cache[key] = {"data": data, "ts": time.time()}

# ─────────────────────────────────────────────
# App
# ─────────────────────────────────────────────

app = FastAPI(
    title="MarketPulse API",
    description="Enriched prediction market data with AI insights. Clean data, trending scores, and bot-ready alerts.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# Auth
# ─────────────────────────────────────────────

async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Simple API key auth. In production, check against a database."""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key

# ─────────────────────────────────────────────
# Pydantic Models
# ─────────────────────────────────────────────

class MarketSummary(BaseModel):
    id: str
    title: str
    slug: str
    url: str
    current_yes_probability: float
    current_no_probability: float
    volume_24h: float
    total_volume: float
    liquidity: float
    days_until_resolution: Optional[int]
    end_date: Optional[str]
    category: str
    trending_score: float = Field(description="0–10 momentum score based on volume acceleration")
    liquidity_rating: Literal["low", "medium", "high"]
    price_change_24h: Optional[float]
    price_change_7d: Optional[float]


class MarketDetail(MarketSummary):
    sentiment_label: Literal["Strong YES", "Leaning YES", "Toss-up", "Leaning NO", "Strong NO"]
    ai_summary: str
    price_history: List[dict]


class ScoreRequest(BaseModel):
    title: str = Field(..., description="Market title or description")
    current_yes_prob: float = Field(..., ge=0, le=1, description="Current YES probability (0–1)")


class ScoreResponse(BaseModel):
    title: str
    current_yes_prob: float
    info_efficiency: int = Field(description="How well-priced this market likely is (1–10)")
    volatility_expectation: Literal["low", "medium", "high"]
    trade_attractiveness: int = Field(description="Overall score for a potential trade (1–10)")
    reasoning: str
    suggested_research: List[str]


class SentimentRequest(BaseModel):
    topic: str = Field(..., description="A prediction market topic or question")


class SentimentResponse(BaseModel):
    topic: str
    sentiment_score: float = Field(description="-1.0 (very bearish) to 1.0 (very bullish)")
    sentiment_label: Literal["bullish", "bearish", "neutral"]
    key_factors: List[str]
    confidence: Literal["low", "medium", "high"]
    summary: str


class CategoryItem(BaseModel):
    slug: str
    label: str
    active_market_count: int


class CategoriesResponse(BaseModel):
    categories: List[CategoryItem]
    total_active_markets: int
    updated_at: str


class AlertRequest(BaseModel):
    market_title: str
    condition: Literal["above_70", "below_30", "crossed_50"]
    threshold: float = Field(..., ge=0, le=1)


class AlertResponse(BaseModel):
    market_title: str
    condition: str
    threshold: float
    short_alert: str
    detailed_alert: str
    telegram_format: str
    generated_at: str


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def compute_sentiment_label(yes_prob: float) -> str:
    if yes_prob >= 0.80:
        return "Strong YES"
    elif yes_prob >= 0.60:
        return "Leaning YES"
    elif yes_prob >= 0.40:
        return "Toss-up"
    elif yes_prob >= 0.20:
        return "Leaning NO"
    else:
        return "Strong NO"


def compute_liquidity_rating(liquidity: float) -> str:
    if liquidity >= 10_000:
        return "high"
    elif liquidity >= 1_000:
        return "medium"
    else:
        return "low"


def compute_trending_score(volume_24h: float, volume_7d: float) -> float:
    """
    Trending score (0–10) based on volume acceleration.
    Compares 24h volume vs the expected daily average from 7d volume.
    Score > 5 means above-average activity today.
    """
    if volume_7d <= 0:
        return round(min(volume_24h / 1000, 10.0), 2)

    daily_avg = volume_7d / 7.0
    if daily_avg <= 0:
        return 0.0

    ratio = volume_24h / daily_avg
    # ratio=1 → average day → score ~5; ratio=3 → very hot → score ~9
    score = min(10.0, 5.0 * math.log1p(ratio) / math.log1p(2))
    return round(max(0.0, score), 2)


def compute_days_until_resolution(end_date_str: Optional[str]) -> Optional[int]:
    if not end_date_str:
        return None
    try:
        end_dt = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        delta = end_dt - now
        return max(0, delta.days)
    except Exception:
        return None


def extract_category(market: dict) -> str:
    """Extract a clean category label from market tags/events."""
    events = market.get("events", [])
    for event in events:
        tags = event.get("tags", [])
        # Prefer tags that look like categories (not too specific)
        for tag in tags:
            label = tag.get("label", "")
            slug = tag.get("slug", "")
            # Skip very specific tags (MicroStrategy, individual names etc)
            if len(label) > 2 and slug in [
                "politics", "crypto", "sports", "finance", "tech", "world",
                "science", "economy", "business", "entertainment", "culture",
                "elections", "geopolitics", "ai", "health", "weather",
                "featured", "2025-predictions", "2026-predictions"
            ]:
                return slug
    # Fallback: first tag
    for event in events:
        tags = event.get("tags", [])
        if tags:
            return tags[0].get("slug", "other")
    return "other"


def parse_outcome_prices(market: dict) -> tuple[float, float]:
    """Parse outcomePrices from Polymarket's string-encoded JSON array."""
    prices_raw = market.get("outcomePrices", "[]")
    try:
        prices = json.loads(prices_raw) if isinstance(prices_raw, str) else prices_raw
        if len(prices) >= 2:
            return float(prices[0]), float(prices[1])
    except Exception:
        pass
    # Fallback to lastTradePrice
    ltp = float(market.get("lastTradePrice", 0.5))
    return ltp, 1.0 - ltp


def enrich_market(market: dict) -> dict:
    """Transform raw Polymarket market record into enriched MarketPulse format."""
    yes_prob, no_prob = parse_outcome_prices(market)
    volume_24h = float(market.get("volume24hr", 0) or 0)
    volume_7d = float(market.get("volume1wk", 0) or 0)
    total_volume = float(market.get("volumeNum", 0) or 0)
    liquidity = float(market.get("liquidityNum", 0) or 0)
    end_date = market.get("endDate") or market.get("endDateIso")
    slug = market.get("slug", "")
    question = market.get("question", market.get("title", "Unknown"))

    return {
        "id": str(market.get("id", "")),
        "title": question,
        "slug": slug,
        "url": f"https://polymarket.com/event/{slug}",
        "current_yes_probability": round(yes_prob, 4),
        "current_no_probability": round(no_prob, 4),
        "volume_24h": round(volume_24h, 2),
        "total_volume": round(total_volume, 2),
        "liquidity": round(liquidity, 2),
        "days_until_resolution": compute_days_until_resolution(end_date),
        "end_date": end_date,
        "category": extract_category(market),
        "trending_score": compute_trending_score(volume_24h, volume_7d),
        "liquidity_rating": compute_liquidity_rating(liquidity),
        "price_change_24h": round(float(market.get("oneDayPriceChange", 0) or 0), 4),
        "price_change_7d": round(float(market.get("oneWeekPriceChange", 0) or 0), 4),
    }


async def fetch_polymarket_markets(
    limit: int = 50,
    offset: int = 0,
    tag_slug: Optional[str] = None,
) -> List[dict]:
    """Fetch active markets from Polymarket Gamma API."""
    params = {
        "active": "true",
        "closed": "false",
        "limit": min(limit, 100),
        "offset": offset,
        "_c": "volume24hr",
        "order": "DESC",
    }
    if tag_slug:
        params["tag_slug"] = tag_slug

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(f"{POLYMARKET_GAMMA}/markets", params=params)
        resp.raise_for_status()
        return resp.json()


async def fetch_market_by_slug(slug: str) -> Optional[dict]:
    """Fetch a single market by slug."""
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(f"{POLYMARKET_GAMMA}/markets", params={"slug": slug, "limit": 1})
        resp.raise_for_status()
        data = resp.json()
        return data[0] if data else None


async def fetch_categories_with_counts() -> List[dict]:
    """Fetch all active events and aggregate by tag."""
    cache_key = "categories"
    cached = cache_get(cache_key)
    if cached:
        return cached

    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.get(
            f"{POLYMARKET_GAMMA}/events",
            params={"active": "true", "closed": "false", "limit": 100},
        )
        resp.raise_for_status()
        events = resp.json()

    category_counts: dict = {}
    for event in events:
        tags = event.get("tags", [])
        for tag in tags:
            slug = tag.get("slug", "")
            label = tag.get("label", "")
            if slug and label:
                if slug not in category_counts:
                    category_counts[slug] = {"label": label, "count": 0}
                markets = event.get("markets", [])
                category_counts[slug]["count"] += len(markets) if isinstance(markets, list) else 1

    # Sort by count desc, keep top 15
    sorted_cats = sorted(category_counts.items(), key=lambda x: -x[1]["count"])[:15]
    result = [
        {"slug": slug, "label": info["label"], "active_market_count": info["count"]}
        for slug, info in sorted_cats
        if info["count"] > 0
    ]

    cache_set(cache_key, result)
    return result


def build_price_history(market: dict) -> List[dict]:
    """
    Build a synthetic 7-point price history using available delta fields.
    Polymarket doesn't expose a simple historical series without CLOB token IDs.
    We reconstruct approximate history from price change fields.
    """
    current = float((json.loads(market.get("outcomePrices", "[0.5]")) or [0.5])[0])
    delta_24h = float(market.get("oneDayPriceChange", 0) or 0)
    delta_7d = float(market.get("oneWeekPriceChange", 0) or 0)

    # Reconstruct: price 7 days ago ≈ current - delta_7d
    # price 1 day ago ≈ current - delta_24h
    # interpolate linearly between them
    price_7d_ago = max(0.01, min(0.99, current - delta_7d))
    price_1d_ago = max(0.01, min(0.99, current - delta_24h))

    history = []
    today = datetime.now(timezone.utc).date()
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        if i == 0:
            price = current
        elif i == 1:
            price = price_1d_ago
        else:
            # Linear interpolation from 7d_ago to 1d_ago
            t = (i - 1) / 5.0
            price = price_7d_ago + (price_1d_ago - price_7d_ago) * (1 - t)
            price = round(max(0.01, min(0.99, price)), 4)
        history.append({"date": str(date), "yes_price": round(price, 4)})

    return history


# ─────────────────────────────────────────────
# AI Helpers
# ─────────────────────────────────────────────

async def ai_market_summary(title: str, description: str, yes_prob: float, category: str) -> str:
    """Generate a plain-English summary of what this market is about and what drives the odds."""
    prompt = f"""You are a prediction market analyst. Write ONE clear paragraph (3-4 sentences) explaining:
1. What this prediction market is asking
2. What the current probability ({yes_prob*100:.0f}% YES) reflects about market consensus
3. What key factors are likely driving the current odds

Market title: {title}
Category: {category}
Description: {description[:500] if description else 'Not provided'}
Current YES probability: {yes_prob*100:.1f}%

Return ONLY the paragraph, no preamble. Be specific and informative."""

    response = await openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.4,
    )
    return response.choices[0].message.content.strip()


async def ai_score_market(title: str, yes_prob: float) -> dict:
    """AI scoring of a prediction market."""
    prompt = f"""You are an expert prediction market analyst. Score this market and return valid JSON.

Market: "{title}"
Current YES probability: {yes_prob*100:.1f}%

Return this exact JSON structure:
{{
  "info_efficiency": <integer 1-10, how well-priced this likely is>,
  "volatility_expectation": "<low|medium|high>",
  "trade_attractiveness": <integer 1-10, overall score for a potential trade>,
  "reasoning": "<2-3 sentence explanation>",
  "suggested_research": ["<thing 1>", "<thing 2>", "<thing 3>"]
}}

Scoring guide:
- info_efficiency: 10 = very liquid, all public info priced in. 1 = obscure market, likely mispriced.
- volatility_expectation: how likely are odds to move significantly before resolution?
- trade_attractiveness: 10 = compelling opportunity. 1 = low edge, avoid.
- suggested_research: specific, actionable things to check before trading."""

    response = await openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        max_tokens=400,
        temperature=0.3,
    )
    return json.loads(response.choices[0].message.content)


async def ai_sentiment_analyze(topic: str) -> dict:
    """AI sentiment analysis for a prediction market topic."""
    prompt = f"""You are a prediction market sentiment analyst. Analyze the current market sentiment around this topic and return valid JSON.

Topic: "{topic}"

Return this exact JSON structure:
{{
  "sentiment_score": <float from -1.0 (very bearish) to 1.0 (very bullish)>,
  "sentiment_label": "<bullish|bearish|neutral>",
  "key_factors": ["<factor 1>", "<factor 2>", "<factor 3>"],
  "confidence": "<low|medium|high>",
  "summary": "<2 sentences: current sentiment state and what it means>"
}}

Key factors should be specific, current forces driving sentiment (not generic platitudes).
Base your analysis on what you know about this topic as of your training cutoff."""

    response = await openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        max_tokens=400,
        temperature=0.4,
    )
    return json.loads(response.choices[0].message.content)


async def ai_draft_alert(market_title: str, condition: str, threshold: float) -> dict:
    """Generate Discord/Telegram alert message drafts."""
    condition_text = {
        "above_70": f"YES probability crossed above {threshold*100:.0f}%",
        "below_30": f"YES probability dropped below {threshold*100:.0f}%",
        "crossed_50": f"YES probability crossed the 50% threshold",
    }.get(condition, f"probability threshold crossed at {threshold*100:.0f}%")

    emoji_map = {
        "above_70": "🔺",
        "below_30": "🔻",
        "crossed_50": "⚖️",
    }
    emoji = emoji_map.get(condition, "📊")

    prompt = f"""You are writing alert messages for a prediction market notification bot.

Market: "{market_title}"
Event: {condition_text}
Threshold: {threshold*100:.0f}%

Generate alert messages and return valid JSON:
{{
  "short_alert": "<one-line Discord message with emoji, bold market name, signal — max 120 chars>",
  "detailed_alert": "<multi-line Discord markdown message with market name, signal explanation, brief insight, and a note about doing own research — use **bold** and newlines>",
  "telegram_format": "<same detailed alert but using Telegram HTML: <b>bold</b>, no markdown asterisks>"
}}

The short_alert should start with 🔔 and be punchy.
The detailed_alert should be informative but not overwhelming (5-7 lines max).
Keep it professional but conversational."""

    response = await openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        max_tokens=500,
        temperature=0.5,
    )
    return json.loads(response.choices[0].message.content)


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@app.get("/", include_in_schema=False)
async def root():
    return {
        "name": "MarketPulse API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational",
    }


@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get(
    "/v1/markets/active",
    response_model=dict,
    summary="Get active prediction markets",
    description="Returns enriched active prediction markets from Polymarket with computed trending scores, liquidity ratings, and clean data.",
    dependencies=[Depends(verify_api_key)],
)
async def get_active_markets(
    category: Optional[str] = Query(None, description="Filter by category slug (e.g. crypto, politics, sports)"),
    min_volume: Optional[float] = Query(None, description="Minimum 24h volume in USD"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return"),
    sort_by: Literal["trending", "volume", "closing_soon"] = Query("trending", description="Sort order"),
):
    cache_key = f"markets:{category}:{min_volume}:{limit}:{sort_by}"
    cached = cache_get(cache_key)
    if cached:
        return cached

    # Fetch more than needed to allow filtering
    fetch_limit = min(limit * 3, 100)
    raw_markets = await fetch_polymarket_markets(limit=fetch_limit, tag_slug=category)

    # Enrich
    markets = [enrich_market(m) for m in raw_markets if m.get("outcomePrices")]

    # Filter: skip markets where prices are both 0 (unresolved/broken)
    markets = [m for m in markets if m["current_yes_probability"] > 0 or m["current_no_probability"] > 0]

    # Filter by min_volume
    if min_volume is not None:
        markets = [m for m in markets if m["volume_24h"] >= min_volume]

    # Sort
    if sort_by == "trending":
        markets.sort(key=lambda m: -m["trending_score"])
    elif sort_by == "volume":
        markets.sort(key=lambda m: -m["volume_24h"])
    elif sort_by == "closing_soon":
        markets.sort(key=lambda m: (
            m["days_until_resolution"] if m["days_until_resolution"] is not None else 99999
        ))

    markets = markets[:limit]

    result = {
        "markets": markets,
        "total": len(markets),
        "limit": limit,
        "sort_by": sort_by,
        "cached_until": (datetime.now(timezone.utc) + timedelta(seconds=CACHE_TTL_SECONDS)).isoformat(),
    }
    cache_set(cache_key, result)
    return result


@app.get(
    "/v1/markets/{slug}/summary",
    response_model=dict,
    summary="Get enriched market summary with AI insight",
    description="Returns a single market with AI-generated summary, price history, and sentiment label.",
    dependencies=[Depends(verify_api_key)],
)
async def get_market_summary(
    slug: str = Path(..., description="Market slug from Polymarket"),
):
    cache_key = f"summary:{slug}"
    cached = cache_get(cache_key)
    if cached:
        return cached

    raw = await fetch_market_by_slug(slug)
    if not raw:
        raise HTTPException(status_code=404, detail=f"Market '{slug}' not found")

    enriched = enrich_market(raw)

    # AI summary (async, runs concurrently with price history build)
    description = raw.get("description", "")
    ai_summary = await ai_market_summary(
        title=enriched["title"],
        description=description,
        yes_prob=enriched["current_yes_probability"],
        category=enriched["category"],
    )

    price_history = build_price_history(raw)
    sentiment_label = compute_sentiment_label(enriched["current_yes_probability"])

    result = {
        **enriched,
        "sentiment_label": sentiment_label,
        "ai_summary": ai_summary,
        "price_history": price_history,
    }

    # Shorter cache for individual market summaries (AI content)
    _cache[cache_key] = {"data": result, "ts": time.time()}
    return result


@app.get(
    "/v1/categories",
    response_model=dict,
    summary="Get market categories with counts",
    description="Returns available prediction market categories with active market counts.",
    dependencies=[Depends(verify_api_key)],
)
async def get_categories():
    categories = await fetch_categories_with_counts()
    total = sum(c["active_market_count"] for c in categories)

    return {
        "categories": categories,
        "total_active_markets": total,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


@app.post(
    "/v1/markets/score",
    response_model=dict,
    summary="AI-score a prediction market",
    description="Score any market on information efficiency, volatility expectation, and trade attractiveness.",
    dependencies=[Depends(verify_api_key)],
)
async def score_market(request: ScoreRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=503, detail="AI scoring unavailable: OPENAI_API_KEY not configured")

    try:
        scores = await ai_score_market(request.title, request.current_yes_prob)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI scoring failed: {str(e)}")

    # Validate and normalize response
    info_eff = max(1, min(10, int(scores.get("info_efficiency", 5))))
    trade_att = max(1, min(10, int(scores.get("trade_attractiveness", 5))))
    vol_exp = scores.get("volatility_expectation", "medium")
    if vol_exp not in ("low", "medium", "high"):
        vol_exp = "medium"

    return {
        "title": request.title,
        "current_yes_prob": request.current_yes_prob,
        "info_efficiency": info_eff,
        "volatility_expectation": vol_exp,
        "trade_attractiveness": trade_att,
        "reasoning": scores.get("reasoning", ""),
        "suggested_research": scores.get("suggested_research", [])[:3],
    }


@app.post(
    "/v1/sentiment/analyze",
    response_model=dict,
    summary="AI sentiment analysis for a topic",
    description="Analyze market sentiment for any prediction market topic.",
    dependencies=[Depends(verify_api_key)],
)
async def analyze_sentiment(request: SentimentRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=503, detail="AI analysis unavailable: OPENAI_API_KEY not configured")

    try:
        sentiment = await ai_sentiment_analyze(request.topic)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Sentiment analysis failed: {str(e)}")

    # Validate
    score = float(sentiment.get("sentiment_score", 0))
    score = max(-1.0, min(1.0, score))
    label = sentiment.get("sentiment_label", "neutral")
    if label not in ("bullish", "bearish", "neutral"):
        label = "neutral"
    confidence = sentiment.get("confidence", "medium")
    if confidence not in ("low", "medium", "high"):
        confidence = "medium"

    return {
        "topic": request.topic,
        "sentiment_score": round(score, 3),
        "sentiment_label": label,
        "key_factors": sentiment.get("key_factors", [])[:3],
        "confidence": confidence,
        "summary": sentiment.get("summary", ""),
    }


@app.post(
    "/v1/alert/draft",
    response_model=dict,
    summary="Draft Discord/Telegram alert messages",
    description="Generate ready-to-send alert messages for Discord and Telegram bots.",
    dependencies=[Depends(verify_api_key)],
)
async def draft_alert(request: AlertRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=503, detail="AI unavailable: OPENAI_API_KEY not configured")

    try:
        alerts = await ai_draft_alert(request.market_title, request.condition, request.threshold)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Alert generation failed: {str(e)}")

    return {
        "market_title": request.market_title,
        "condition": request.condition,
        "threshold": request.threshold,
        "short_alert": alerts.get("short_alert", ""),
        "detailed_alert": alerts.get("detailed_alert", ""),
        "telegram_format": alerts.get("telegram_format", ""),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
