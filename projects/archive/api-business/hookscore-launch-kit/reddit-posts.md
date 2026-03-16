# Reddit Posts — HookScore API

---

## r/SaaS

**Title:** I built a hook scoring API — here's what I learned about short-form content

**Body:**

Background: I've been spending way too much time on TikTok and YouTube Shorts. Not as a consumer — as someone obsessed with *why* certain videos blow up.

The hook is everything. First 3 seconds. But nobody was actually measuring hook quality in a systematic way. Creators just... guess. Post. Wait. Repeat.

So I built HookScore — an API that scores hooks on a 0–100 scale, suggests improvements, compares two hooks against each other, and classifies by type (curiosity, fear, authority, etc.).

The interesting part was building the /compare endpoint. You throw two hooks at it and it tells you which one wins and why. Here's a real example:

```
Hook A: "This morning routine changed my life"
Hook B: "I woke up at 4am for 30 days. Here's what actually happened."

Result:
- Hook B wins (84 vs 61)
- Hook A: generic, no specificity, overused phrase
- Hook B: specific timeframe, implied journey, curiosity gap
```

The reasoning output has been the most useful part. It's not just a score — it explains *why* something lands or doesn't, which is what actually helps you improve.

Tech-wise: FastAPI, GPT-4o-mini, Railway. Nothing exotic. Built it in a few days of focused work.

It's live on RapidAPI now with a free tier (30 calls/month, no credit card). Paid plans start at $3.99.

A few things I learned:

1. Specificity kills vagueness every time. "I did X for 30 days" > "this changed my life"
2. Curiosity gaps are overused but still work when they're earned, not faked
3. LinkedIn hooks are genuinely different from TikTok — the API had to learn this too

Honest question for this community: is there an audience for this? I see tool fatigue everywhere. But I'm not finding anything that does this specific thing well. Maybe I'm wrong.

Happy to answer questions or hear what you'd do differently.

---

## r/webdev

**Title:** Built a FastAPI hook analyzer in an afternoon — free tier on RapidAPI

**Body:**

Quick share because I think some people here might find this useful or at least interesting from a build perspective.

I wanted to score short-form content hooks (TikTok, YouTube, etc.) automatically — think of it like a linter for your first sentence. Ended up building it as a REST API over a weekend.

**Stack:**
- FastAPI (Python) — fast to prototype, async-friendly, auto-docs out of the box
- GPT-4o-mini — cheap enough to run at scale, surprisingly good at structured JSON output
- Railway for deploy — zero config, just push and it works
- RapidAPI for distribution/monetization

**The 6 endpoints:**

- `/score` — single hook, returns score (0–100) + breakdown
- `/suggest` — rewrites a weak hook into something better
- `/compare` — A/B comparison of two hooks
- `/classify` — returns hook type (curiosity, fear, authority, social proof, etc.)
- `/batch` — score up to 10 hooks in one call
- `/emoji-impact` — scores whether emoji usage helps or hurts the hook

The `/batch` endpoint is probably the most practically useful. Example:

```json
POST /batch
{
  "hooks": [
    "5 foods that are secretly making you fat",
    "I tried every productivity app for a month",
    "This is why you're always tired"
  ],
  "platform": "tiktok"
}

Response:
[
  { "hook": "5 foods...", "score": 78, "grade": "B" },
  { "hook": "I tried every...", "score": 85, "grade": "A" },
  { "hook": "This is why...", "score": 52, "grade": "D" }
]
```

Getting GPT-4o-mini to return consistent JSON with a scoring rubric took a few iterations of prompt engineering. Happy to share what worked if anyone's curious.

Free tier is 30 calls/month — no card required. Listed on RapidAPI.

Not trying to sell anything here, just thought the build approach might be useful to someone. Open to feedback on the architecture if you'd do something different.

---

## r/TikTokCreators

**Title:** I got tired of guessing which hook would perform — so I built an API

**Body:**

Real talk: I spent way too long A/B testing hooks by just... posting them and seeing which one did better. Which is basically science if you're patient and have weeks to waste.

I'm a developer so I figured I'd automate the guessing part. Built an API that scores hooks before you post them.

Here's a real before/after that I actually ran:

```
Before: "This morning routine changed my life"
Score: 58/100 — Grade: D

After (using /compare endpoint):
"I woke up at 4am for 30 days. Here's what nobody tells you."
Score: 87/100 — Grade: A
```

The difference? Specificity. The API tells you *exactly* why your hook is weak — not just "make it better." It'll say things like "lacks time specificity," "no implied contrast," "curiosity gap is too vague to create tension."

The /compare endpoint is the one I use most. I write two versions of a hook, throw them both at it, and it tells me which one wins and why. Saves me the week of waiting to find out from actual data.

It works across platforms — TikTok, Instagram, YouTube, Twitter, LinkedIn. The scoring is different for each because what hooks on LinkedIn is genuinely different from what hooks on TikTok (no surprise there).

It's on RapidAPI. Free tier is 30 calls/month, no credit card. That's enough to test a few videos a week. Paid plans if you need more.

If you create a lot of content and feel like hook-writing is more vibes than science — this is the tool I built for that problem.

Drop your worst hook in the comments. I'll run it and post the score.

---

## r/entrepreneur

**Title:** Shipped my second product: an API that scores your content hooks — lessons from launch

**Body:**

Quick debrief on something I just shipped, in case the process is useful to anyone here.

**The gap I found:**

Short-form content lives or dies by the hook — the first 3 seconds. Creators know this. But there's no real tooling for measuring hook quality before you post. It's all guesswork and gut feeling.

I'd seen tools for headline scoring (CoSchedule, etc.) but nothing built specifically for the vocabulary and patterns of TikTok/Instagram/YouTube hooks. Different medium, different rules.

**What I built:**

HookScore — an API with 6 endpoints for scoring, rewriting, comparing, classifying, and batch-processing hooks. Listed on RapidAPI.

**Pricing decisions:**

This took me the longest. I landed on:
- Free: 30 calls/month
- $3.99 / $7.99 / $14.99 / $29.99/mo

The free tier was intentional — I want people to actually try it, not bounce at a paywall. The low entry point ($3.99) is for solo creators who want a little more. The higher tiers are for agencies and automation workflows.

**What I'd do differently:**

Honestly, I should've gotten 5 people to try it before launching. I built it in a focused sprint and launched before getting any external feedback. The product works, but I don't yet know what the actual pain point is for the customer — which is a gap.

**What's next:**

Watching to see who actually subscribes and why. Planning to reach out to early users directly.

If you've shipped API products before — what's your actual customer acquisition approach? Content marketing feels like the obvious play but it's slow.

---

## r/n8n

**Title:** Built a hook scoring API for automation workflows — free tier + example workflow

**Body:**

Hey everyone, built something that slots nicely into content automation workflows and thought this community might find it useful.

HookScore API — scores, rewrites, compares, and classifies short-form content hooks across TikTok, Instagram, YouTube, Twitter, LinkedIn. Available on RapidAPI.

Here's a workflow I'm using myself:

**"Auto-improve weak hooks before posting"**

```
Trigger: New draft saved in Notion (or Airtable)
  ↓
HTTP Request → POST hookscore-api/score
  Body: { "hook": "{{draft_hook}}", "platform": "twitter" }
  ↓
IF score < 70
  ↓ YES
  HTTP Request → POST hookscore-api/suggest
    Body: { "hook": "{{draft_hook}}", "platform": "twitter" }
  ↓
  Update Notion item: improved_hook = {{suggestion}}
  ↓
  Send Telegram notification: "Weak hook detected. Improved version ready."
  ↓ NO (score ≥ 70)
  Continue to post workflow
```

The API returns clean JSON — score, grade, strengths, weaknesses, and suggested rewrites. Easy to map into any workflow.

The `/batch` endpoint is also useful if you're generating multiple hooks at once (e.g., from a GPT step that outputs 5 variations). One API call instead of five.

Endpoints available:
- `/score` — single hook score
- `/suggest` — rewrite suggestion
- `/compare` — A/B winner + reasoning
- `/classify` — hook type (curiosity, fear, authority, etc.)
- `/batch` — up to 10 hooks in one call
- `/emoji-impact` — does the emoji help or hurt?

Free tier is 30 calls/month on RapidAPI, no card needed. Paid plans from $3.99 if you need more volume.

Happy to help anyone wire up a specific workflow — just drop what you're trying to automate and I'll sketch the nodes.
