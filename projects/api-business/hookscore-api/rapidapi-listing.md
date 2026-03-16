# RapidAPI Listing — HookScore API

Complete copy for listing HookScore on RapidAPI Marketplace.

---

## API Name
**HookScore — Social Media Hook Scorer & Rewriter**

## Tagline
Score, classify, and rewrite viral hooks for TikTok, Instagram, YouTube, Twitter, and LinkedIn using AI.

## Short Description (for search cards)
AI-powered hook analysis tool. Score your opening lines 0-100, get rewrite suggestions, compare hooks head-to-head, classify hook types, and analyze emoji impact. Built for content creators, agencies, and SaaS tools.

---

## Full Description

### What is HookScore?

HookScore is the API that tells you exactly why your hook will (or won't) stop the scroll.

Content creators, agencies, and SaaS builders use HookScore to:
- **Stop guessing** — get a 0-100 score with specific reasoning, not vague advice
- **Write better, faster** — get 5 AI-generated rewrites in seconds
- **A/B test hooks** — compare two versions head-to-head before publishing
- **Understand hook types** — learn which psychological trigger you're using and how to sharpen it
- **Scale content testing** — batch score up to 20 hooks at once

HookScore is trained on what actually stops the scroll: curiosity gaps, pattern interrupts, specific numbers, controversy, and emotional triggers — applied platform-by-platform.

### Platforms Supported
- **TikTok** — 4-8 word optimal, controversy and curiosity gap dominate
- **Instagram** — aesthetic/aspirational, question format, up to 12 words
- **YouTube** — promise of value, specific outcome, 8-15 word sweet spot
- **Twitter/X** — punchy hot takes, under 10 words, contrarian wins
- **LinkedIn** — professional insight, specific stats, contrarian takes, 10-15 words

### Who Is This For?
- **Content creators** who want to improve their hook game before posting
- **Social media agencies** managing multiple clients and content calendars
- **SaaS founders** building content tools, Chrome extensions, or writing assistants
- **Marketers** running paid ad campaigns where the hook is everything
- **Developers** integrating hook scoring into content platforms

---

## Use Cases

1. **Content creation app** — Let users score hooks before they publish
2. **Chrome extension** — Score hooks from any social media platform in real-time
3. **Content calendar tool** — Add hook quality scores to scheduled posts
4. **Ad copywriting tool** — Score and rewrite ad hooks for better CTR
5. **YouTube title optimizer** — Score and batch-test 10+ title variations
6. **LinkedIn content assistant** — Classify and rewrite professional hooks
7. **Agency dashboard** — Batch score client content before approval

---

## Endpoint Documentation

---

### 1. POST `/score`
**Score a hook for a specific platform**

Analyzes a hook and returns a 0-100 score with grade, strengths, weaknesses, and platform fit assessment.

**Request Body:**
```json
{
  "hook": "I quit my 9-5 and made more in one week",
  "platform": "tiktok"
}
```

**Parameters:**
| Field | Type | Required | Description |
|---|---|---|---|
| `hook` | string | ✅ | The hook text to score (max 500 chars) |
| `platform` | string | ✅ | `tiktok`, `instagram`, `youtube`, `twitter`, `linkedin` |

**Example Response:**
```json
{
  "score": 82,
  "grade": "B+",
  "verdict": "Strong income claim with built-in controversy — 'quit my 9-5' is a proven pattern that triggers curiosity, but the timeframe 'one week' needs a number to hit A-tier.",
  "strengths": [
    "Triggers curiosity gap — reader needs to know HOW",
    "9-5 quit narrative is aspirational and broadly relatable",
    "Implies transformation (before/after frame)"
  ],
  "weaknesses": [
    "Missing specific number — '3x my salary' would score 12+ points higher",
    "Slightly over optimal TikTok length at 9 words — trim to 7"
  ],
  "platform_fit": "Strong TikTok fit — quit-job narrative performs extremely well, consider opening video with this as the first spoken line.",
  "word_count": 9,
  "optimal_word_count": "4-8 words"
}
```

---

### 2. POST `/suggest`
**Get 5 AI-rewritten versions of a hook**

Rewrites your hook in a specified tone with predicted scores for each version. Each rewrite uses a different hook formula.

**Request Body:**
```json
{
  "hook": "Tips for growing on Instagram",
  "platform": "instagram",
  "tone": "shocking"
}
```

**Parameters:**
| Field | Type | Required | Description |
|---|---|---|---|
| `hook` | string | ✅ | The original hook to rewrite |
| `platform` | string | ✅ | Target platform |
| `tone` | string | ✅ | `casual`, `professional`, `funny`, `shocking` |

**Example Response:**
```json
{
  "original_score": 38,
  "suggestions": [
    {
      "hook": "I studied 1,000 Instagram accounts. 3 rules separate 1M from 1K followers.",
      "predicted_score": 91,
      "why": "Specific social proof number + list format creates irresistible curiosity gap"
    },
    {
      "hook": "Your Instagram won't grow until you stop doing this one thing.",
      "predicted_score": 84,
      "why": "Fear/loss trigger with implied secret — 'this one thing' demands a click"
    },
    {
      "hook": "Nobody told me these Instagram growth rules until I had 10K followers.",
      "predicted_score": 80,
      "why": "Story hook with gatekept knowledge — relatable frustration + curiosity"
    },
    {
      "hook": "Unpopular opinion: Instagram reach isn't algorithm — it's your hook quality.",
      "predicted_score": 78,
      "why": "Controversy/hot take that challenges the algorithm blame narrative"
    },
    {
      "hook": "What if your captions are why you're stuck at 500 followers?",
      "predicted_score": 74,
      "why": "Question hook targeting specific pain point with accusatory edge"
    }
  ]
}
```

---

### 3. POST `/compare`
**Compare two hooks head-to-head**

Returns a winner with individual scores and detailed reasoning. Great for A/B testing before publishing.

**Request Body:**
```json
{
  "hook_a": "5 habits that changed my life",
  "hook_b": "The one habit billionaires share (it's not what you think)",
  "platform": "youtube"
}
```

**Example Response:**
```json
{
  "winner": "B",
  "score_a": 68,
  "score_b": 87,
  "reason": "Hook B wins by a wide margin. It combines a curiosity gap ('it's not what you think'), social proof ('billionaires'), and a specific promise ('one habit') — three proven YouTube title techniques in 9 words. Hook A is a tired list format with no specificity.",
  "audience_note": "Hook A might perform slightly better with younger audiences who prefer simple list formats, but Hook B is the stronger play for most YouTube audiences."
}
```

---

### 4. POST `/classify`
**Classify a hook's psychological type**

Identifies which of 10 hook types is being used, explains the psychology, and gives actionable improvement tips.

**Hook Types:** Curiosity Gap, Controversy/Hot Take, How-To, List Format, Story Hook, Fear/Loss, Social Proof, Challenge, Trend-Jacking, Question Hook

**Request Body:**
```json
{
  "hook": "Nobody talks about this investment strategy"
}
```

**Example Response:**
```json
{
  "type": "Curiosity Gap",
  "description": "This hook withholds critical information to create a cognitive itch the brain desperately needs to scratch. By implying others are ignoring something important, it triggers both FOMO and a need for insider knowledge.",
  "best_platforms": ["TikTok", "YouTube", "Twitter"],
  "typical_ctr_boost": "22-28% above platform average",
  "tips": [
    "Add a specific detail to the secret — 'Nobody talks about this 4% bond strategy' performs 3x better than a vague claim",
    "Pair with a social proof element — 'The investment strategy every hedge fund uses but won't tell you' creates stronger authority",
    "Consider adding a timeframe — 'Nobody talked about this until now' creates urgency alongside the curiosity gap"
  ]
}
```

---

### 5. POST `/batch`
**Rank up to 20 hooks at once**

Score and rank multiple hooks simultaneously. Perfect for content teams testing variations before publishing.

**Request Body:**
```json
{
  "hooks": [
    "Tips for better sleep",
    "I slept 8 hours for 30 days. Here's what happened.",
    "The sleep mistake doctors never mention",
    "Are you actually sleeping or just lying there?",
    "3 sleep hacks that outperform melatonin"
  ],
  "platform": "tiktok"
}
```

**Example Response:**
```json
{
  "ranked": [
    {
      "rank": 1,
      "hook": "The sleep mistake doctors never mention",
      "score": 88,
      "one_liner": "fear/loss + authority gap, tight 6 words"
    },
    {
      "rank": 2,
      "hook": "3 sleep hacks that outperform melatonin",
      "score": 84,
      "one_liner": "specific list + bold comparison claim"
    },
    {
      "rank": 3,
      "hook": "Are you actually sleeping or just lying there?",
      "score": 76,
      "one_liner": "question hook, relatable pain point"
    },
    {
      "rank": 4,
      "hook": "I slept 8 hours for 30 days. Here's what happened.",
      "score": 71,
      "one_liner": "story hook, specific, slightly long for TikTok"
    },
    {
      "rank": 5,
      "hook": "Tips for better sleep",
      "score": 24,
      "one_liner": "completely generic, zero curiosity"
    }
  ],
  "best": "The sleep mistake doctors never mention",
  "worst": "Tips for better sleep"
}
```

---

### 6. POST `/emoji-impact`
**Analyze how emojis affect hook performance**

Scores the hook with and without emojis, analyzes each emoji's impact, and provides an optimized version.

**Request Body:**
```json
{
  "hook": "🔥 This productivity hack will change your life 💯"
}
```

**Example Response:**
```json
{
  "score_with_emojis": 58,
  "score_without_emojis": 64,
  "emoji_analysis": [
    {
      "emoji": "🔥",
      "impact": "neutral",
      "reason": "Fire emoji has positive energy but is so overused it no longer adds urgency — now reads as generic hype"
    },
    {
      "emoji": "💯",
      "impact": "negative",
      "reason": "Heavily associated with low-quality content and spam — actively reduces credibility with most audiences"
    }
  ],
  "recommended_version": "This productivity hack changed everything ⚡"
}
```

---

### GET `/health`
Returns API health status. Use to verify the API is running.

**Response:** `{"status": "ok", "version": "1.0.0"}`

---

## Suggested Tags
`hooks`, `social-media`, `content-creation`, `tiktok`, `instagram`, `youtube`, `twitter`, `linkedin`, `copywriting`, `viral-content`, `ai`, `gpt`, `content-marketing`, `creator-tools`

## Suggested Category
**Social** → Content Tools / Creator Tools

## Suggested Pricing Tiers

| Plan | Requests/Day | Price/Month |
|---|---|---|
| Free | 25 | $0 |
| Basic | 500 | $9.99 |
| Pro | 5,000 | $29.99 |
| Ultra | 50,000 | $99.99 |

## Terms / Notes for Listing
- Response time: typically 1-3 seconds (GPT-4o-mini)
- All responses are JSON
- CORS enabled (works from any browser/frontend)
- No authentication needed beyond RapidAPI key
