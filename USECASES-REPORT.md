# Motion Elevation — Use Cases & Tools Report
_Generated: 2026-03-04_

---

## 1. Tool Installation Results

### Scrapling
**Status: FAILED ❌**

`pip` and `pip3` are not installed on this server. Python3 exists (`/usr/bin/python3`) but has no `pip` module. Cannot install Scrapling without first installing pip.

**Fix needed (Lyubo must approve):**
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && sudo python3 get-pip.py
pip install scrapling
python3 -c "from scrapling import Scraper; print('Scrapling OK')"
```
Scrapling is a smart web scraper with anti-detection features — good for scraping competitor sites or prediction market data. Not urgent to install now; APITap covers similar ground better.

---

### APITap
**Status: INSTALLED ✅ (partially)**

- Cloned to: `/home/ubuntu/.openclaw/workspace/tools/apitap`
- `npm install` ran successfully — 101 packages, 0 vulnerabilities
- The core library is ready

**What APITap does:** Turns any website into an API. It intercepts the real API calls a website makes internally (e.g., Polymarket, Reddit, YouTube) and lets you replay them directly — no browser needed, 20-100x less token cost than scraping HTML.

**What still needs to be done to use it:**
1. **Install globally:** `npm install -g @apitap/core` (or use from the local clone)
2. **Optional (for `capture` + `browse` commands):** `npx playwright install chromium` — installs a full browser (~300MB). Required only to *capture* new sites. The `read`, `peek`, `discover` commands work without it.
3. **Wire to OpenClaw MCP:** `claude mcp add -s user apitap -- apitap-mcp`

**Especially useful for Polymarket** — APITap already has a tested Polymarket skill file (3 endpoints, green tier, 200 OK replay). This means it can fetch market data without a browser.

---

## 2. Use Case Assessments

### 🟢 multi-channel-customer-service.md
**What it does:** Unifies WhatsApp, Instagram DMs, Gmail, and Google Reviews into one AI-powered inbox. Auto-replies to FAQs, escalates complex issues to humans. Deployable for client businesses.

**Relevance to Motion Elevation:** HIGH — this is a sellable product. One client = recurring revenue. Lyubo can pitch this to local businesses (restaurants, salons, clinics) and charge €100–500/month setup + monthly retainer.

**What's needed:**
- WhatsApp Business API (via 360dialog or Meta directly — requires business verification)
- Instagram Graph API (Meta Business Suite)
- Gmail OAuth (`gog` CLI)
- Google Business Profile API (for reviews)
- A client willing to be the first test case

**Difficulty:** Medium-Hard (API setup is bureaucratic but not technically complex)

**Lyubo must provide:**
- Decision: which local businesses to target first
- Client contact to pilot it with
- Business Facebook/Meta account for API access

---

### 🟢 n8n-workflow-orchestration.md
**What it does:** Routes all external API calls through n8n visual workflows. OpenClaw never touches credentials — it just calls webhooks. Gives full visibility into what's running, with a lock-after-test safety step.

**Relevance to Motion Elevation:** HIGH — this is the backbone pattern for running an automation business. Every client workflow Lyubo builds should run through n8n. Reduces risk, looks professional, easy to demo.

**What's needed:**
- Docker installed (or use cloud n8n)
- Clone and run `openclaw-n8n-stack` (one command: `docker-compose up -d`)
- Anthropic API key in `.env`

**Difficulty:** Easy (Docker + one repo clone)

**Lyubo must provide:**
- Decision to use Docker on this server or a separate VPS
- Anthropic API key (already have it presumably)

**Recommended:** Set this up first. It makes every other use case more secure and professional.

---

### 🟡 youtube-content-pipeline.md
**What it does:** Automated content scouting for YouTube. Hourly cron scans web + Twitter for AI news, pitches video ideas to Telegram, deduplicates against past videos using embeddings, creates Asana cards with outlines when Lyubo shares a link.

**Relevance to Motion Elevation:** MEDIUM-HIGH — directly supports "Predictions Peter" channel. Saves hours of research per week. But requires Lyubo to actually be creating content consistently first.

**What's needed:**
- `x-research-v2` skill from ClawhHub
- `knowledge-base` skill (RAG)
- YouTube Analytics access via `gog` CLI
- SQLite database (already available on server)
- Asana account (or swap for Todoist)
- Telegram topic for video ideas

**Difficulty:** Medium

**Lyubo must provide:**
- Decision: is Predictions Peter active and posting regularly?
- YouTube channel connected to `gog`
- List of subreddits/topics to track
- Asana or Todoist account

---

### 🟢 polymarket-autopilot.md
**What it does:** Paper trading bot for Polymarket. Runs every 15 minutes, analyzes markets, simulates trades using TAIL/BONDING/SPREAD strategies, logs everything to a database, posts daily P&L summaries to Discord. No real money.

**Relevance to Motion Elevation:** HIGH — directly relevant to Predictions Peter and Lyubo's interest in prediction markets. Low risk (paper trading), high learning value. Can later inform real trading strategy.

**What's needed:**
- Polymarket API access (public, no auth needed for market data)
- SQLite database (already available)
- Discord server + channel for reports
- APITap already has Polymarket skill — can use it for data fetching

**Difficulty:** Easy-Medium (database setup + cron + Discord webhook)

**Lyubo must provide:**
- Discord server (or create one for Motion Elevation)
- Starting strategy parameters (or use defaults from the use case)

**Note:** APITap's existing Polymarket skill makes this easier — market data is already mapped.

---

### 🟡 autonomous-project-management.md
**What it does:** Decentralized project management using STATE.yaml files. Subagents work in parallel on tasks, update shared state, no central bottleneck. CEO pattern — main agent does strategy only.

**Relevance to Motion Elevation:** MEDIUM — useful once Lyubo has multiple clients or projects running in parallel. Too early right now if Motion Elevation is still in early stages.

**What's needed:**
- Just file system + subagent spawning (already available)
- Git repo for state versioning
- AGENTS.md configuration update

**Difficulty:** Easy (it's a pattern, not an installation)

**Lyubo must provide:**
- List of active projects to track
- Decision on which project to use as first test

---

### 🟢 daily-reddit-digest.md
**What it does:** Daily digest of top posts from specified subreddits, delivered at a set time. Learns preferences over time (no memes, no reposts, etc.). Read-only, no auth needed.

**Relevance to Motion Elevation:** HIGH — easy win. Useful for market research, prediction market trends, content ideas. Can be running in 30 minutes.

**What's needed:**
- `reddit-readonly` skill from ClawhHub (`clawhub install reddit-readonly`)
- List of subreddits to track
- Scheduled cron (or heartbeat)

**Difficulty:** Easy

**Lyubo must provide:**
- List of subreddits (e.g., r/PredictionMarkets, r/Polymarket, r/SideHustle, r/entrepreneur)
- Preferred delivery time

---

### 🟡 x-account-analysis.md
**What it does:** Qualitative analysis of Twitter/X account. Finds patterns in viral posts, identifies what topics drive engagement, explains why some posts flop. Uses the Bird skill (pre-bundled).

**Relevance to Motion Elevation:** MEDIUM-HIGH — very useful for Predictions Peter Twitter account. But requires Lyubo to have an active X account with enough tweet history to analyze.

**What's needed:**
- Bird skill (pre-bundled with OpenClaw)
- X account login in Chrome/Brave
- Cookie extraction: `auth-token` and `ct0` values from browser DevTools

**Difficulty:** Easy (once cookies are extracted)

**Lyubo must provide:**
- X/Twitter account login
- `auth-token` and `ct0` cookie values (from browser DevTools → Application → Cookies → twitter.com)
- Decision: use personal account or Predictions Peter account

---

### 🟡 overnight-mini-app-builder.md (game dev check)
**What it does:** Asks OpenClaw to autonomously build a mini MVP app overnight based on Lyubo's goals and interests. Wakes up to a surprise app each morning.

**Game dev relevance:** No game dev specific file found. This is the closest — it can build any kind of mini app, including simple browser games if instructed.

**Relevance to Motion Elevation:** LOW-MEDIUM — fun experiment, not a revenue driver directly. Could occasionally produce something useful or worth launching.

**Difficulty:** Easy (just a prompting pattern)

---

## 3. Priority Order — What to Implement First

### 🥇 Priority 1: n8n Workflow Orchestration
**Why:** Foundation layer. Set this up first and every other workflow runs through it safely. One Docker command away. Makes Motion Elevation look professional to clients.

### 🥈 Priority 2: Polymarket Autopilot
**Why:** Low setup effort, directly relevant to Lyubo's interests, no real money at risk, generates daily data and insights. APITap already has the Polymarket skill ready. Great learning tool for trading strategy.

### 🥉 Priority 3: Daily Reddit Digest
**Why:** Easiest win. Running in 30 minutes. Useful for market research, content ideas, and staying informed — all relevant to Predictions Peter and automation research.

### 🏅 Priority 4: Multi-Channel Customer Service
**Why:** Highest revenue potential. Takes more setup but is the core product Motion Elevation can sell. Start building this once n8n is running, then pitch to first client.

---

## 4. What Lyubo Needs to Provide

| Use Case | Needs from Lyubo |
|---|---|
| **Scrapling** | Approval to install pip (`sudo`) |
| **APITap** | Decision: install Playwright (300MB) for capture? |
| **n8n** | Docker on this server or separate VPS? Anthropic API key. |
| **Polymarket Autopilot** | Discord server/channel for reports |
| **Reddit Digest** | List of subreddits to track + preferred delivery time |
| **X Account Analysis** | X login cookies (`auth-token`, `ct0`). Which account? |
| **YouTube Pipeline** | Is Predictions Peter active? YouTube + Asana/Todoist account |
| **Customer Service** | First client to pilot with. Meta Business account for WhatsApp/Instagram API |
| **Autonomous PM** | List of active projects to track |

---

## 5. Quick Wins This Week

1. `clawhub install reddit-readonly` → set up Reddit digest (30 min)
2. Set up Polymarket Autopilot with SQLite + Discord (2-3 hours)  
3. Clone and run `openclaw-n8n-stack` via Docker (1 hour)
4. Extract X cookies → run account analysis on Predictions Peter (30 min)

Scrapling is blocked until pip is installed. APITap is installed and ready; Playwright is optional.
