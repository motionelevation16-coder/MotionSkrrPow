# 🧠 AI Business Research — Two Tracks
*Compiled by Motion 🐋 | March 7, 2026*

---

## TL;DR

Both tracks are real, both have proven blueprints. The question is which one fits **your situation** (no coding background, student, wants quick passive income). Verdict at the bottom.

---

## TRACK 1: AI App (The "Wrapper" Model)

### What it actually is

An AI wrapper is software that calls an AI (like OpenAI, Replicate, Stable Diffusion) to do a task — then sells access to that task with a nice interface. The app doesn't do anything technically novel. It just *wraps* an existing AI in a product with a clear value prop and a subscription price.

### Why it works

Most people don't know how to use ChatGPT, Midjourney, or Stable Diffusion directly. They *do* know how to pay $19/month for a simple tool that does the thing they want. You're selling simplicity, not technology.

### 📊 Real Numbers (Verified)

| Product | What it does | Revenue | Team |
|---|---|---|---|
| **PhotoAI** | AI photographer — pro photos from your face | $132K/mo ($1.6M ARR) | Solo founder |
| **Chatbase** | Chat widget for websites powered by GPT | $70K/mo | Small team |
| **InteriorAI** | AI room redesign | $53K/mo | Solo |
| **PDF.ai** | Chat with any PDF | $500K+/year | Solo |
| **Jenni AI** | AI writing for students/researchers | $150K/mo (from $2K in 18 months) | Small team |
| **Midjourney** | AI image generation | $42M/mo | 40 people, $0 raised |

### 🔑 The Success Formula (The Copy-Paste Template)

**Step 1 — Pick an expensive, annoying real-world service**
- Professional photography → $250–1,500 per shoot
- Interior design consultation → $500–2,000
- Resume writing → $100–500
- Video editing → $50–200/hour
- Legal document drafting → $200–500/page

**Step 2 — Find an AI that can do it for pennies**
- Image generation: Stable Diffusion via Replicate.com (~$0.01/image)
- GPT-4/Claude: via OpenAI/Anthropic API (~$0.003/1K tokens)
- Video: RunwayML, Pika Labs
- Voice: ElevenLabs

**Step 3 — Make the value proposition brutally simple**
> "A professional photoshoot costs $500. We do it for $29/month, unlimited photos."

**Step 4 — Pricing**
- Starter: $9–19/mo (entry hook)
- Pro: $29–49/mo (most features, most popular)
- Premium: $99–199/mo (power users)
- Annual plans with 20-40% discount (locks in cash)

**Step 5 — Ship it fast with minimal tech**
Pieter Levels (PhotoAI, $1.6M ARR) built his with:
- Vanilla HTML/CSS/JS
- Plain PHP backend
- SQLite database
- Single $40/mo VPS
- NO React, TypeScript, frameworks, or complex infra

Your equivalent: Use **Bubble.io**, **Glide**, or **Softr** (no-code) + **Replicate** or **OpenAI API**.

**Step 6 — AI handles the compute**
You don't run models. You pay-as-you-go via APIs:
- **Replicate.com** — pay per second of GPU use (~$0.01–0.10 per generation)
- **OpenAI API** — pay per token
- **ElevenLabs** — pay per character
- Your margins can be 80%+ because you price at 10x your API cost

### ⚡ "Our Tweak" Angle — What Makes It Original

The formula already works. Your twist can be:
- **Niche** — don't do "AI photos for everyone," do "AI photos for LinkedIn profiles" or "AI headshots for Airbnb hosts"
- **Geography** — build it in German/Bulgarian. Most wrappers are English-only. Huge untapped market.
- **Combo** — pair two tools together in a way nobody has (AI photo + AI caption generator for Instagram)
- **Audience** — target a community you understand (prediction market traders, university students, fitness influencers)

### 🚀 Time to First Revenue: 2–6 weeks (if you ship it)

### 💰 Realistic Income: $500–5,000/mo by month 3 (if you get distribution right)

---

## TRACK 2: API Provider Business

### What it actually is

You build an API — a service that other developers (or no-coders via tools like Zapier/Make) send requests to and get data/results back. You sell access on a per-call or subscription basis.

### Why it works

- API economy was worth $6.2 trillion in 2024
- Developers need building blocks — they'd rather pay for a working API than build it themselves
- Truly passive once set up (automated billing, automated delivery, no manual work)
- B2B buyers pay more reliably and churn less than consumers

### 📊 Real Numbers

| Product | What it does | Revenue |
|---|---|---|
| **Anthropic** | AI API (Claude) | $417M/month (70%+ from API) |
| **Mistral AI** | Open AI API access | $50M/month |
| Small niche APIs on RapidAPI | Varies (QR, OCR, scraping, etc.) | $200–5,000/mo |
| Niche stock/finance API | Analysis, data | Some hit $1K–10K/mo bootstrapped |

### 🔑 The Success Formula

**Step 1 — Find a gap in what exists**
Go to RapidAPI.com, browse the marketplace. Look for:
- APIs with 1,000+ subscribers but 2-star reviews (they're bad, you can build better)
- APIs people are asking for in Reddit/forums but don't exist
- Things that exist as software (not APIs) — wrap them as an API

**Step 2 — Build it (MVP)**
You don't need to write it from scratch. AI (Claude/Cursor) can build:
- A Python/Flask or Node.js API in hours
- Deployed to Railway.app or Render.com (free tier to start)
- Authentication via API keys (simple to add)

**Step 3 — Sell it in 3 places**
1. **RapidAPI** — 40K+ APIs, built-in audience, 20-30% commission (fine to start)
2. **Your own site** — Stripe + simple landing page, better margins
3. **AWS Marketplace** — enterprise buyers, higher prices

**Step 4 — Pricing model**
- Freemium: 100 free calls/month → $9/mo for 1,000 calls → $49/mo for unlimited
- Per-call: $0.001–0.01 per request (scales automatically)
- Subscription: flat monthly for a set quota

**Step 5 — Distribution**
- Post in r/SaaS, r/webdev, r/APIdev
- Write a blog post "How I built [X] API and what it does"
- List on ProductHunt
- Share in Discord communities of developers

### ⚡ Profitable API Niches Right Now (2026)

| Niche | Why it works |
|---|---|
| **AI text/content processing** (summarize, classify, extract) | Generic and always in demand |
| **Language detection + translation** | Underserved in Eastern European languages |
| **Social media scraping** (Instagram, TikTok public data) | High demand, gray area = high prices |
| **Prediction market data aggregation** (Polymarket, Kalshi) | Lyubo knows this space! |
| **SEO/SERP data** | Always in demand, existing providers are expensive |
| **Email/phone verification** | Boring but businesses need it → recurring revenue |
| **Financial data for niche markets** | Crypto, prediction markets, alternative assets |
| **AI image analysis** (classify, describe, moderate) | Wrap OpenAI Vision API with a cleaner interface |

### 🚀 Time to First Revenue: 1–4 weeks (API, no marketing needed if listed on RapidAPI)

### 💰 Realistic Income: $200–2,000/mo within 60 days (if niche has demand)

---

## 🥊 Head-to-Head Comparison

| | AI App | API Provider |
|---|---|---|
| **Target users** | Consumers, businesses | Developers, builders |
| **Revenue ceiling** | Very high (PhotoAI = $1.6M ARR) | Medium-high ($1K–$100K/mo) |
| **Speed to first $** | Slower (need marketing) | Faster (RapidAPI has organic traffic) |
| **Technical difficulty** | Low-Medium (no-code possible) | Medium (need basic code or AI-generated) |
| **Maintenance** | Medium (users have expectations) | Low (it just works or it doesn't) |
| **Competition** | High in generic niches | Lower in specific niches |
| **Passive-ness** | Medium (need to handle users) | High (truly passive once running) |

---

## 🎯 My Recommendation

**Do both, but in sequence:**

**Month 1–2 → Build a niche API first**
- Lower effort, truly passive, teaches you the fundamentals of how AI APIs work
- Start with something you understand: a Polymarket data API, a prediction market summarizer, a simple text tool
- List on RapidAPI and your own site
- Target: $200–500/mo passive

**Month 2–4 → Use that knowledge to build the AI App**
- You'll have learned pricing, deployment, billing, and what users want
- Build the wrapper app with a clear niche
- Build an audience first if possible (social media, content)
- Target: $1,000–5,000/mo

**The materials you want to send me:**
Send anything about:
- Specific niches you've been researching
- AI apps you've seen and thought "I could build that"
- Data/APIs you already use (Polymarket etc.) — could become products
- Any tools you've paid for that disappointed you (= opportunity)

---

## 📁 Sources
- IndieHackers: PhotoAI case study ($0 → $132K MRR)
- AIJourn: AI Wrappers Market Report 2025
- MktClarity: Top 35 AI Startups 2025
- CashwiseAI: 7 Realistic AI Passive Income Ideas
- JuheAPI: Top 5 API Marketplaces 2025
- Reddit r/SaaS: RapidAPI seller community

---

*Next step: Lyubo sends research materials → we narrow to 1 idea → build it.*
*🐋 Motion*
