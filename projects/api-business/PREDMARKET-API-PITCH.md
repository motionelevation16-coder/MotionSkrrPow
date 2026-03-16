# Polymarket Real-Time API — Product Pitch & Course Outline

> Internal doc for RapidAPI listing prep + cousin review
> Last updated: 2026-03-08

---

# SECTION 1: API ONE-PAGER

## What It Does

**Plain English:**
Polymarket's public data is slow, incomplete, and annoying to query at scale. This API fixes that. It gives you clean, real-time access to live market odds, order book movements, event resolution, and historical price data — all through a single REST/WebSocket interface designed for bots, not browsers.

**Technical:**
The API wraps Polymarket's CLOB (Central Limit Order Book) and gamma endpoints, normalizes the data, and serves it via:
- **REST** for on-demand queries (market lookup, historical data, snapshots)
- **WebSocket** for event-driven streaming (live odds changes, trade activity, market settlements)

No scraping. No rate-limit wrestling with Polymarket directly. No building your own normalizer. You get structured JSON, ready to feed a strategy engine.

---

## Key Endpoints

### REST

| Endpoint | Description |
|---|---|
| `GET /markets` | List active markets. Filter by category, volume, end date, status. |
| `GET /markets/{marketId}` | Full market snapshot — current odds, spread, volume, open interest. |
| `GET /markets/{marketId}/history` | Historical odds series. Supports `from`, `to`, `interval` params (1m, 5m, 1h, 1d). |
| `GET /markets/search?q=` | Search markets by keyword/topic. Returns ranked results with live odds. |
| `GET /events/{eventId}` | Event-level data — all child markets, resolution status, deadline. |
| `GET /events/resolved` | Recently resolved events with final outcome and settlement price. |

### WebSocket

| Channel | Description |
|---|---|
| `ws://stream/odds` | Real-time odds tick stream. Subscribe to specific markets or all active. |
| `ws://stream/trades` | Live trade feed — price, size, side, timestamp. |
| `ws://stream/settlements` | Fires immediately on market resolution. Includes outcome + final value. |

**Sample REST response — `/markets/{id}`:**
```json
{
  "id": "will-trump-win-2024",
  "question": "Will Trump win the 2024 election?",
  "yes_price": 0.61,
  "no_price": 0.39,
  "spread": 0.02,
  "volume_24h": 142500,
  "open_interest": 980000,
  "resolution_date": "2024-11-06T00:00:00Z",
  "status": "active",
  "last_updated": "2026-03-08T15:43:22Z"
}
```

---

## Why Bots Need This Specifically

Bots are latency-sensitive. A bot acting on 30-second-old data isn't trading — it's donating.

Here's what happens without a reliable real-time feed:

- **Stale odds = bad fills.** Your bot calculates EV on odds that have already moved. You execute, you lose edge.
- **Missed resolutions.** If your bot doesn't know a market settled, it keeps watching a dead market instead of redeploying capital.
- **Crawling public endpoints at scale = bans.** Polymarket rate-limits aggressive direct queries. Your bot gets throttled or blocked.
- **No historical baseline.** Without historical price series, you can't backtest strategies or identify mean-reversion setups.

This API solves all four. WebSocket for sub-second odds updates. Settlement push events for instant redeployment signals. Managed rate-limiting so you never get blocked. Historical endpoint for backtesting.

**The math is simple:** One bad trade from stale data costs more than a month of Pro tier.

---

## Pricing Tiers

| Tier | Price | REST Calls/day | WebSocket | History | Support |
|---|---|---|---|---|---|
| **Free** | $0 | 500 | ❌ | 7 days | Community |
| **Starter** | $29/mo | 10,000 | ✅ (5 markets) | 30 days | Email |
| **Pro** | $99/mo | 100,000 | ✅ (unlimited) | 365 days | Priority |
| **Enterprise** | Custom | Unlimited | ✅ + dedicated | Full | SLA + Slack |

> Free tier is intentionally limited enough that running a bot on it is painful — but good enough to test and build. Starter is the natural first upgrade for anyone serious. Pro is where real bots live.

---

## Use Cases

**1. Arbitrage Bot**
Monitor the same real-world event across Polymarket and another prediction market (Manifold, Kalshi). When odds diverge beyond spread, execute on the cheaper side. Requires sub-second odds updates → WebSocket stream.

**2. News-Triggered Trading Bot**
Hook into a news API. When a relevant headline fires, hit `/markets/search?q=` to find matching markets, check current odds vs expected post-news fair value, and trade before the market reprices. Speed matters — REST + low latency.

**3. Mean Reversion Strategy**
Pull 30-day historical odds via `/markets/{id}/history`. Identify markets that tend to oscillate (e.g., recurring event types). Trade the reversion when odds hit statistical extremes. Historical endpoint + backtesting pipeline.

**4. Portfolio Monitor / Alert System**
No trading, just intelligence. Bot watches a basket of markets via WebSocket and pings you (Telegram, Discord, email) when odds shift >5% in an hour, or when a market resolves. Starter tier covers this easily.

**5. Resolution Harvester**
Listen to `ws://stream/settlements`. The instant a market resolves, check for any open positions that should be closed or capital that can be redeployed. Critical for multi-market bots managing position lifecycle.

---

## Tech Stack Notes

- **Protocol:** REST (HTTPS) + WebSocket (WSS)
- **Auth:** API key via `X-API-Key` header
- **Response format:** JSON throughout. Consistent schema, no surprise nulls.
- **WebSocket:** Standard `ws` protocol. Subscription model — send a JSON subscribe message, receive event stream. Reconnect-safe (last-event-id support).
- **Rate limiting:** HTTP 429 with `Retry-After` header on REST. WebSocket connections are per-key, not per-connection.
- **SDKs (planned):** Python client (ships with course). Node.js wrapper.
- **Uptime target:** 99.9% SLA on Pro+. Backed by CloudFront + multi-region origin.

---

# SECTION 2: COURSE OUTLINE

## "Build Your First Polymarket Bot"

**Tagline:** *From Python basics to a live trading bot in 6 weeks.*

---

### Who This Is For

- Knows basic Python (loops, functions, requests library — that's enough)
- Has heard of Polymarket, maybe traded manually
- Wants to automate their edge, not just theorize about it
- Not a quant. Not a CS grad. Just someone who's figured out markets are beatable and wants to act faster than humans can.

### What They'll Have at the End

A working Python bot that:
- Connects to real-time market data via the API
- Scores markets for mispricings against a configurable baseline
- Executes trades via Polymarket's API
- Sends alerts to Telegram when it acts
- Has a basic risk management layer (max position size, daily loss limit)

---

## Module Structure

---

### Module 1 — Prediction Markets 101 *(Foundation)*
**Goal:** Understand what you're actually trading before touching code.

- **Lesson 1.1** — What is a prediction market? How Polymarket works (CLOB, USDC, shares)
- **Lesson 1.2** — Reading odds like a trader, not a gambler. EV, implied probability, overround.
- **Lesson 1.3** — What makes a market mispriced? Recency bias, news lag, low liquidity traps.
- **Lesson 1.4** — The bot's edge: speed + consistency. What humans can't do, bots can.

> *No code yet. Pure market understanding. Skippable for students who already trade.*

---

### Module 2 — Your Dev Environment *(Setup)*
**Goal:** Get the toolchain working before writing a single strategy line.

- **Lesson 2.1** — Python environment setup: venv, pip, recommended packages (`requests`, `websockets`, `python-dotenv`, `pandas`)
- **Lesson 2.2** — Polymarket account setup + API key (for trade execution). What permissions you need.
- **Lesson 2.3** — Getting your API key for this course. Free tier walkthrough — what you can and can't do on it.
- **Lesson 2.4** — First API call: fetch a live market, print the odds. "Hello, Polymarket."

> *Students get a **free-tier API key** here. It's enough to follow along, but rate-limited enough that they'll feel the ceiling. Upgrade pitch is organic.*

---

### Module 3 — Real-Time Data Pipeline *(Core Infrastructure)*
**Goal:** Build the data layer your bot runs on. This is the heart of the course.

- **Lesson 3.1** — REST vs WebSocket: when to use each. Polling is dead.
- **Lesson 3.2** — Building a market snapshot fetcher. Scheduled REST pulls with caching.
- **Lesson 3.3** — Connecting to the WebSocket odds stream. Handling reconnects, dropped connections, stale data.
- **Lesson 3.4** — Structuring incoming data: pandas DataFrames, in-memory state, simple SQLite store.
- **Lesson 3.5** — Why this matters: live demo of stale-data vs real-time bot behavior on historical replay.

> *This is where the API earns its keep. Free-tier students hit rate limits here — natural upsell to Starter ($29/mo) for WebSocket access.*

---

### Module 4 — Strategy Engine *(The Brain)*
**Goal:** Teach the bot when to trade.

- **Lesson 4.1** — Defining "mispriced": building a simple fair value model (baseline odds from aggregate sources)
- **Lesson 4.2** — Signal generation: threshold-based triggers (e.g., current odds deviate >8% from fair value)
- **Lesson 4.3** — Filtering noise: minimum volume, minimum time-to-resolution, liquidity checks
- **Lesson 4.4** — Backtesting your strategy on historical odds data (using the `/history` endpoint + Starter/Pro API)
- **Lesson 4.5** — Logging signals: every potential trade captured with timestamp, odds, reason. Your audit trail.

---

### Module 5 — Trade Execution *(The Hands)*
**Goal:** Make the bot actually do something.

- **Lesson 5.1** — Polymarket's trade API: authentication, signing transactions, order types
- **Lesson 5.2** — Placing a limit order vs market order. Slippage, spread, partial fills.
- **Lesson 5.3** — Position tracking: knowing what you own, at what price, with what exposure
- **Lesson 5.4** — Paper trading mode: execute the full logic but log instead of submit. Test before live.
- **Lesson 5.5** — Going live: checklist before your first real trade. Starting small.

---

### Module 6 — Risk Management & Monitoring *(Keeping the Bot Alive)*
**Goal:** The bot should never blow up your account.

- **Lesson 6.1** — Position sizing: Kelly criterion lite. Why flat-betting is safer than it sounds to start.
- **Lesson 6.2** — Daily loss limits: auto-shutdown if the bot loses X USDC in a session
- **Lesson 6.3** — Telegram alerts: instant notifications on trade execution, errors, and market settlements
- **Lesson 6.4** — Logging and debugging: structured logs, error handling, graceful restarts
- **Lesson 6.5** — What to watch: a simple dashboard (Streamlit) to monitor bot health and P&L in real-time

---

### Module 7 — Scaling Up *(Where the Real Money Is)*
**Goal:** Go from one market to many, from simple signals to smarter ones.

- **Lesson 7.1** — Multi-market scanning: watch 50+ markets simultaneously (requires Pro API tier)
- **Lesson 7.2** — Portfolio thinking: correlation between markets, avoiding overexposure to one event type
- **Lesson 7.3** — Smarter signals: incorporating news APIs, social sentiment, resolution calendars
- **Lesson 7.4** — Scheduling and uptime: running the bot 24/7 on a cheap VPS (DigitalOcean, Hetzner)
- **Lesson 7.5** — What's next: more complex strategies, multi-exchange arbitrage, when to go fully automated vs human-in-the-loop

---

## Pricing

| Option | Price | What You Get |
|---|---|---|
| **Course Only** | $149 one-time | All 7 modules, code repo, free API key (limited) |
| **Course + Starter API** | $149 + $29/mo | Course + full WebSocket access from day one |
| **Bundle Deal** | $249 first 3 months | Course + Pro API for 3 months — run it, prove it, then decide |

> One-time purchase keeps the friction low for impulse buys. The subscription is the real business — course is the funnel.

---

## Upsell Path

```
Free API key (course)
    → Hit rate limits in Module 3
        → Upgrade to Starter ($29/mo) to unlock WebSocket
            → Module 7 requires multi-market scanning
                → Upgrade to Pro ($99/mo)
                    → Running a real bot at scale
                        → Enterprise conversation
```

The course is engineered so the API limits become friction points exactly when the student is most motivated. Module 3 (WebSocket) and Module 7 (multi-market) are the two natural upgrade moments — students who make it that far are already committed.

**Additional upsell surface:**
- Strategy library (paid add-on): pre-built signal modules students can drop in
- Bot-as-a-service: "don't want to run your own VPS? We'll host it" — future product
- Discord community (included with Pro tier): peer signal sharing, strategy discussion

---

*Document owner: Lyubo | Status: Draft for cousin review*
