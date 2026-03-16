# dev.to Article — HookScore API

---

## Title
**I built a hook scoring API with FastAPI and GPT-4o-mini — here's how**

### Alt Titles
1. "Why I built a content hook analyzer instead of just using ChatGPT directly"
2. "FastAPI + GPT-4o-mini + Railway: my weekend API build — from idea to RapidAPI listing"
3. "Scoring TikTok hooks with AI: the build, the rubric, and what I learned"

---

## Article

---

### The problem nobody's tooling for

If you've spent any time in short-form content, you know the hook is everything. First 3 seconds on TikTok. First line on Twitter. First sentence on LinkedIn. Get it wrong and it doesn't matter how good the rest is — nobody sees it.

What surprised me is how few tools exist specifically for hook quality. There are headline analyzers (CoSchedule, etc.) built for blog posts. There are general "content quality" tools. But nothing that understood the vocabulary and patterns of short-form hooks — the difference between a curiosity gap that works and one that feels desperate, or why "I did this for 30 days" beats "this changed my life" every single time.

So I built one.

---

### The tech stack

**FastAPI** was the obvious choice for a Python dev building a REST API quickly. Auto-generates OpenAPI docs, async-native, minimal boilerplate. I had a working prototype in about two hours.

**GPT-4o-mini** for the AI layer. I went back and forth on this — I considered Claude for the nuanced reasoning, but GPT-4o-mini is cheap, fast, and surprisingly good at returning structured JSON when you prompt it correctly. For a scoring API where every call costs money, the price point matters.

**Railway** for deployment. Zero config. Push to GitHub, it deploys. For a side project API, I don't want to manage infrastructure. Railway just works.

**RapidAPI** for distribution and monetization. I didn't want to build my own billing system. RapidAPI handles the API keys, rate limiting, and Stripe integration. It's not perfect but it's functional.

---

### What I built

HookScore has 6 endpoints:

- `/score` — takes a hook + platform, returns score (0–100), letter grade, strengths, weaknesses
- `/suggest` — takes a weak hook, returns 3 improved versions
- `/compare` — takes two hooks, returns the winner + reasoning
- `/classify` — returns the hook's psychological type (curiosity, fear, authority, social proof, transformation, controversy)
- `/batch` — score up to 10 hooks in one call
- `/emoji-impact` — evaluates whether emoji usage helps or hurts the hook

Platform-aware scoring for TikTok, Instagram Reels, YouTube Shorts, Twitter/X, and LinkedIn.

---

### Deep dive: the /compare endpoint

The compare endpoint is the one I personally find most useful. Here's the core logic:

```python
@router.post("/compare")
async def compare_hooks(request: CompareRequest):
    hook_a = request.hook_a
    hook_b = request.hook_b
    platform = request.platform or "general"

    prompt = f"""
    You are a short-form content expert evaluating hooks for {platform}.

    Compare these two hooks:
    Hook A: "{hook_a}"
    Hook B: "{hook_b}"

    Score each hook from 0-100 based on:
    - Specificity (0-25): Does it use concrete details, numbers, timeframes?
    - Curiosity gap (0-25): Does it create genuine tension without being clickbait?
    - Relevance (0-25): Is it immediately clear what this is about?
    - Emotional resonance (0-25): Does it tap into a real feeling or desire?

    Return a JSON object with this exact structure:
    {{
      "winner": "A" or "B",
      "hook_a_score": integer,
      "hook_b_score": integer,
      "hook_a_grade": letter grade,
      "hook_b_grade": letter grade,
      "winner_reasons": [list of 2-3 reasons why the winner is better],
      "loser_weaknesses": [list of 1-2 specific weaknesses of the loser]
    }}
    """

    response = await openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.3
    )

    result = json.loads(response.choices[0].message.content)
    return CompareResponse(**result)
```

A few things worth noting here:

**Low temperature (0.3):** Scoring should be consistent, not creative. Lower temperature means more deterministic outputs. I tried 0.7 early on and the same hook could score 65 one run and 80 the next. 0.3 stabilized it significantly.

**`response_format: json_object`:** GPT-4o-mini supports a JSON mode that forces structured output. Without this, you'd be parsing free-text which breaks constantly. This was a game-changer for reliability.

**Rubric in the prompt:** I spent probably 30% of my development time on the scoring rubric. Getting the four dimensions right (specificity, curiosity gap, relevance, emotional resonance) was more important than any engineering decision.

---

### Sample outputs

**TikTok — Fitness niche**

```json
{
  "hook": "I ate one meal a day for 90 days — here's what my bloodwork showed",
  "platform": "tiktok",
  "score": 91,
  "grade": "A+",
  "strengths": [
    "Extreme specificity: 90 days + bloodwork implies verified data",
    "High curiosity gap: reader wants the unexpected result"
  ],
  "weaknesses": [
    "Niche audience — might underperform with general fitness crowd"
  ]
}
```

**LinkedIn — Productivity niche**

```json
{
  "hook": "I stopped using to-do lists 6 months ago. Here's what replaced them.",
  "platform": "linkedin",
  "score": 83,
  "grade": "A",
  "strengths": [
    "Contrarian angle works well on LinkedIn professional audience",
    "Specific timeframe adds credibility"
  ],
  "weaknesses": [
    "Slightly overused structure on LinkedIn — 'I stopped doing X' pattern is common"
  ]
}
```

---

### What I learned

**Prompt engineering is most of the work.** The FastAPI boilerplate took a few hours. The Railway deploy was 20 minutes. Getting the scoring rubric right, getting consistent JSON output, handling edge cases in prompts — that was 60% of the project.

**GPT-4o-mini is better than I expected.** I assumed I'd need GPT-4 for nuanced content evaluation. GPT-4o-mini handles it well at a fraction of the cost. For a per-call API, this matters a lot.

**Launch before you're ready.** I kept wanting to add features before shipping. The product is never "done." I had 6 working endpoints and a free tier — that's enough to see if anyone wants it.

**RapidAPI takes time to get traction.** You don't just list your API and watch the subscriptions roll in. Distribution is a second job. That's why I'm writing this.

---

### Where to find it

HookScore is listed on RapidAPI: **[INSERT RAPIDAPI LINK]**

Free tier: 30 calls/month, no credit card required.

If you build something with it, or use it in an n8n workflow, I'd genuinely love to hear about it. Reach out on Twitter: **[INSERT HANDLE]**

---

*Stack: FastAPI · GPT-4o-mini · Railway · RapidAPI*
*Tags: #python #fastapi #openai #api #contentcreation*
