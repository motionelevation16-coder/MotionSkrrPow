# 🎣 HookScore API — Full Blueprint
*Motion 🐋 | March 7, 2026*

---

## 🔍 Competition Analysis

### What exists right now:

| Competitor | Type | Price | Users | Weakness |
|---|---|---|---|---|
| **Apify TikTok Hook Analyzer** | API (barely) | $5/mo + usage | 2 total users, 1 active | TikTok only, 0 reviews, basically dead |
| **TLinky Caption Analyzer** | Web tool only | Free | No API — unusable for devs | Not an API at all |
| **ap0t.com Hook Analyzer** | Web tool only | Free | No API | Not an API at all |
| **HookMafia** | Web app | Free (for now) | Script generator only | Not an API, no scoring |

### 🟢 Verdict: The market is WIDE OPEN

There is NO real, well-built hook scoring API on RapidAPI right now. The only one has 2 users and 0 reviews. We walk in as the first serious product in this space.

---

## 💡 What We Build — HookScore API

**One-liner:** *The developer API that scores, compares, classifies, and rewrites short-form content hooks for TikTok, Instagram, YouTube, Twitter, and LinkedIn.*

The difference from what exists: we go **multi-platform, multi-endpoint, multi-use-case** — not just "score my TikTok caption."

---

## 🔧 Endpoints (What the API Does)

### 1. `/score` — Core Endpoint
**Input:** hook text + platform (tiktok/instagram/youtube/twitter/linkedin)
**Output:**
```json
{
  "score": 78,
  "grade": "B+",
  "verdict": "Strong curiosity gap but weak CTA. Missing urgency.",
  "strengths": ["Opens with a question", "Specific number included"],
  "weaknesses": ["No CTA", "Too long for TikTok (optimal: under 8 words)"],
  "platform_fit": "Medium — this style performs better on Instagram than TikTok"
}
```

### 2. `/suggest` — Rewrite Engine
**Input:** hook text + platform + tone (casual/professional/funny/shocking)
**Output:** 5 improved versions with predicted scores for each

### 3. `/compare` — A/B Tester
**Input:** hook_a + hook_b + platform
**Output:** winner, score difference, reason, which audience each performs better for

### 4. `/classify` — Hook Type Identifier
**Input:** hook text
**Output:**
```json
{
  "type": "Curiosity Gap",
  "description": "Teases information without revealing it",
  "best_platforms": ["TikTok", "YouTube"],
  "tips": ["Add a number", "Use 'This is why...' format for higher CTR"]
}
```
Hook types covered: Curiosity Gap, Controversy/Hot Take, How-To, List Format, Story Hook, Fear/Loss, Social Proof, Challenge, Trend-Jacking

### 5. `/batch` — Bulk Scorer (Paid tiers only)
**Input:** array of up to 20 hooks + platform
**Output:** ranked list, best to worst, with scores and one-line feedback each

### 6. `/emoji-impact` — Emoji Analyzer
**Input:** hook with emojis
**Output:** which emojis help, which hurt, optimized version with/without

---

## 🎯 Our Tweak (What Makes It "Us")

Three things no competitor does:

**1. Platform-specific scoring**
A hook that kills on TikTok is dead on LinkedIn. We score against each platform's actual algorithm behavior and audience expectation. Not generic — platform-aware.

**2. The A/B Compare endpoint**
Content creators and marketers constantly have 2 versions and don't know which to post. Nobody offers this as an API call. We make it a one-liner.

**3. Hook Type Classification + Coaching**
Don't just tell them the score — tell them *what kind of hook* they wrote and how to get better at that type. Educational value = retention.

---

## 💰 Pricing (Undercutting the Only Competition)

Apify charges $5/mo + usage for an inferior product with 2 users. We go lower to vacuum up their potential market.

| Tier | Price | Calls/month | Endpoints | Target |
|---|---|---|---|---|
| **FREE** | $0 | 30/mo | /score only | Testing + discovery |
| **Starter** | $3.99/mo | 500/mo | /score + /classify | Hobbyists, students |
| **Creator** | $7.99/mo | 2,000/mo | All except /batch | Solo content creators |
| **Pro** | $14.99/mo | 8,000/mo | All endpoints | Agencies, tools builders |
| **Ultra** | $29.99/mo | 30,000/mo | All endpoints + priority | SaaS builders, power users |

**Per-call overage:** $0.005 per extra call above limit (very competitive)

### Why this pricing works:
- Free tier = discovery on RapidAPI (more signups = more visibility in algorithm)
- $3.99 = impulse buy (less than a coffee, easy yes)
- Pro tier is where we make money ($14.99 × 100 users = $1,499/mo)

---

## 👥 Who Buys This (Target Users)

| User Type | Use Case | Tier |
|---|---|---|
| Solo content creators | Test hooks before posting | Starter |
| Social media agencies | Batch test 10+ hooks per client | Pro |
| SaaS builders | Embed hook scoring in their own tool | Ultra |
| n8n/Make automation builders | Automate content pipeline scoring | Creator |
| Course creators | Validate email subject lines + video titles | Creator |
| Marketers | A/B test ad copy hooks | Pro |

---

## 🛠️ How to Build It (Non-Coder Path)

**Tech stack:**
- Python + FastAPI (AI can write 100% of this)
- OpenAI API (GPT-4o-mini — cheap: ~$0.0001 per call = margins of 97%+)
- Deployed on Railway.app (free tier to start, $5/mo when you scale)
- API key management → handled by RapidAPI automatically

**Step-by-step build:**
1. Open Cursor or Claude.ai
2. Paste: *"Build me a FastAPI Python API with these 6 endpoints: [list]. Each endpoint calls OpenAI GPT-4o-mini with a scoring prompt. Return JSON."*
3. AI writes the whole thing (~200 lines of code)
4. Deploy to Railway.app (free, takes 10 minutes with a guide)
5. Connect to RapidAPI (paste your Railway URL, set pricing tiers)
6. Done.

**Cost to run:**
- Railway.app: Free (until $5/mo threshold)
- OpenAI API: ~$0.0001 per call → 8,000 calls = $0.80 in API costs
- You charge $14.99/mo for 8,000 calls
- **Margin: ~95%**

---

## 📢 How to Get First Users

1. **RapidAPI listing** → organic traffic from day 1 (developers browse by category)
2. **Post in r/SaaS, r/webdev, r/TikTokCreators** → "I built a hook scoring API, free tier available"
3. **ProductHunt launch** → one post, can generate 100+ signups in 24h
4. **Content creators on Twitter/X** → "Rate your TikTok hooks with our API" — visual demo of the output
5. **n8n/Make communities** → devs who build automation workflows will embed this immediately

---

## 📅 Timeline

| Week | Action |
|---|---|
| Week 1 | Build the API (Cursor + AI, one afternoon session) |
| Week 1 | Deploy to Railway.app |
| Week 1 | List on RapidAPI with free tier |
| Week 2 | Post on Reddit, ProductHunt |
| Week 3 | First paying users (target: 10 users = ~$40/mo) |
| Month 2 | Iterate based on feedback, add endpoints |
| Month 3 | Target: 50-100 users = $200-1,000/mo passive |

---

## 🎯 Summary

- **Gap confirmed:** No real hook API exists on RapidAPI
- **Our edge:** Multi-platform + A/B compare + classification (nobody else does this combo)
- **Price:** Undercuts the only competitor ($3.99 vs $5+ usage)
- **Effort:** 1 afternoon to build with AI assistance
- **Margins:** 95%+
- **Passive-ness:** 100% once running (RapidAPI handles everything)
- **Month 3 target:** €200-1,000/mo

---

*Next: Lyubo reviews, we build the API together (1 session with Cursor). 🐋*
