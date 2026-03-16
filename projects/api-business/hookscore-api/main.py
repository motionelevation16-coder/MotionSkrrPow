"""
HookScore API — Score, classify, rewrite, and compare social media hooks.
Powered by OpenAI GPT-4o-mini.
"""

import os
import json
import re
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ─── OpenAI client ────────────────────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

client = OpenAI(api_key=OPENAI_API_KEY)
MODEL = "gpt-4o-mini"

# ─── App setup ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="HookScore API",
    description=(
        "Score, classify, rewrite, and compare short-form content hooks for "
        "TikTok, Instagram, YouTube, Twitter/X, and LinkedIn. "
        "Powered by GPT-4o-mini."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Platform config (used in prompts) ────────────────────────────────────────
PLATFORM_RULES = {
    "tiktok": (
        "TikTok: Optimal length is 4-8 words. The hook must work in the first "
        "1-2 seconds of a video caption or opening line. Controversy, curiosity "
        "gaps, and pattern interrupts dominate. Slang and bold claims work well. "
        "Anything over 10 words loses significant impact."
    ),
    "instagram": (
        "Instagram: Up to 12 words is acceptable. Aesthetic, aspirational, and "
        "question-format hooks perform well. The first line of a caption must "
        "stop the scroll before the 'more' cutoff. Emotional resonance and "
        "relatable scenarios outperform pure shock value."
    ),
    "youtube": (
        "YouTube: 8-15 words is the sweet spot for titles and video hooks. "
        "Promise a specific outcome or value ('How I made $10k in 30 days' > "
        "'How I made money'). Numbers, specificity, and clear benefit statements "
        "are critical. The viewer needs to know exactly what they'll get."
    ),
    "twitter": (
        "Twitter/X: Under 10 words for maximum impact. Hot takes, contrarian "
        "opinions, and punchy controversial statements dominate. The hook must "
        "provoke a reaction (agree, disagree, or 'wait, what?'). Generic "
        "observations get ignored — specific and bold wins."
    ),
    "linkedin": (
        "LinkedIn: 10-15 words is acceptable. Professional insight, a specific "
        "stat, or a contrarian professional take performs best. The first line "
        "must challenge a common belief or promise career/business value. "
        "Storytelling openers ('I was fired. Best thing that happened.') also "
        "work extremely well."
    ),
}

PLATFORM_OPTIMAL_WORDS = {
    "tiktok": "4-8 words",
    "instagram": "6-12 words",
    "youtube": "8-15 words",
    "twitter": "5-10 words",
    "linkedin": "10-15 words",
}

HOOK_TYPES = [
    "Curiosity Gap",
    "Controversy/Hot Take",
    "How-To",
    "List Format",
    "Story Hook",
    "Fear/Loss",
    "Social Proof",
    "Challenge",
    "Trend-Jacking",
    "Question Hook",
]

# ─── Helper: call GPT and parse JSON ──────────────────────────────────────────
def gpt_json(system_prompt: str, user_prompt: str) -> dict:
    """
    Call GPT-4o-mini with JSON mode. Returns parsed dict.
    Raises HTTPException on failure.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )
        raw = response.choices[0].message.content
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse AI response as JSON: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}")


def normalize_platform(platform: str) -> str:
    """Normalize platform name to lowercase key."""
    p = platform.lower().strip()
    if p in ("x", "twitter/x", "twitter"):
        return "twitter"
    if p not in PLATFORM_RULES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown platform '{platform}'. Valid: tiktok, instagram, youtube, twitter, linkedin",
        )
    return p


# ─── Request / Response models ────────────────────────────────────────────────

class ScoreRequest(BaseModel):
    hook: str = Field(..., min_length=1, max_length=500, description="The hook text to score")
    platform: str = Field(..., description="Platform: tiktok|instagram|youtube|twitter|linkedin")

class EmojiAnalysisItem(BaseModel):
    emoji: str
    impact: str  # positive | negative | neutral
    reason: str

class ScoreResponse(BaseModel):
    score: int
    grade: str
    verdict: str
    strengths: List[str]
    weaknesses: List[str]
    platform_fit: str
    word_count: int
    optimal_word_count: str


class SuggestRequest(BaseModel):
    hook: str = Field(..., min_length=1, max_length=500)
    platform: str
    tone: str = Field(..., description="casual|professional|funny|shocking")

    @validator("tone")
    def validate_tone(cls, v):
        valid = {"casual", "professional", "funny", "shocking"}
        if v.lower() not in valid:
            raise ValueError(f"tone must be one of: {', '.join(valid)}")
        return v.lower()

class SuggestionItem(BaseModel):
    hook: str
    predicted_score: int
    why: str

class SuggestResponse(BaseModel):
    original_score: int
    suggestions: List[SuggestionItem]


class CompareRequest(BaseModel):
    hook_a: str = Field(..., min_length=1, max_length=500)
    hook_b: str = Field(..., min_length=1, max_length=500)
    platform: str

class CompareResponse(BaseModel):
    winner: str  # "A" or "B"
    score_a: int
    score_b: int
    reason: str
    audience_note: str


class ClassifyRequest(BaseModel):
    hook: str = Field(..., min_length=1, max_length=500)

class ClassifyResponse(BaseModel):
    type: str
    description: str
    best_platforms: List[str]
    typical_ctr_boost: str
    tips: List[str]


class BatchRequest(BaseModel):
    hooks: List[str] = Field(..., min_items=1, max_items=20)
    platform: str

class RankedHook(BaseModel):
    rank: int
    hook: str
    score: int
    one_liner: str

class BatchResponse(BaseModel):
    ranked: List[RankedHook]
    best: str
    worst: str


class EmojiImpactRequest(BaseModel):
    hook: str = Field(..., min_length=1, max_length=500)

class EmojiImpactResponse(BaseModel):
    score_with_emojis: int
    score_without_emojis: int
    emoji_analysis: List[EmojiAnalysisItem]
    recommended_version: str


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/", tags=["Meta"])
def root():
    """API info and endpoint listing."""
    return {
        "name": "HookScore API",
        "version": "1.0.0",
        "description": "Score, classify, rewrite, and compare social media hooks using AI.",
        "endpoints": {
            "POST /score": "Score a hook on a specific platform (0-100 with grade, strengths, weaknesses)",
            "POST /suggest": "Get 5 improved rewrites of a hook with predicted scores",
            "POST /compare": "Compare two hooks head-to-head and get a winner with reasoning",
            "POST /classify": "Classify a hook into one of 10 types with tips",
            "POST /batch": "Rank up to 20 hooks at once for a platform",
            "POST /emoji-impact": "Analyze how emojis affect a hook's score",
            "GET /health": "Health check",
            "GET /docs": "Interactive API documentation (Swagger UI)",
        },
    }


@app.get("/health", tags=["Meta"])
def health():
    """Health check endpoint."""
    return {"status": "ok", "version": "1.0.0"}


@app.post("/score", response_model=ScoreResponse, tags=["Hooks"])
def score_hook(req: ScoreRequest):
    """
    Score a hook on a scale of 0-100 for a specific platform.
    Returns a grade, verdict, strengths, weaknesses, and platform fit analysis.
    """
    platform = normalize_platform(req.platform)
    platform_rules = PLATFORM_RULES[platform]
    optimal = PLATFORM_OPTIMAL_WORDS[platform]
    word_count = len(req.hook.split())

    system_prompt = f"""You are a world-class social media strategist and copywriting expert.
Your specialty is analyzing hooks — the first line or caption of short-form content —
and telling creators exactly how likely they are to stop the scroll.

You understand the psychology of attention: curiosity gaps, pattern interrupts, 
specific numbers, urgency, controversy, and emotional triggers.

Platform context for this evaluation:
{platform_rules}

SCORING RUBRIC:
- 90-100: Extremely strong — opens a loop the brain has to close. Uses a number or 
  specific claim. Under optimal word count. Creates immediate "I need to know more."
- 80-89: Very strong — missing one small element. Good curiosity or controversy 
  but slightly too long, or lacks specificity.
- 70-79: Solid foundation — missing one key element. Usually: no urgency, 
  too generic, or buried the interesting part.
- 60-69: Below average — some potential but mostly forgettable. Could be improved 
  with specificity or a stronger emotional trigger.
- 50-59: Weak hook — too generic, no specific promise, or the interesting part 
  is buried. Most readers will scroll past.
- Below 50: Won't stop the scroll — no hook, no promise, no curiosity. 
  Reads like a statement, not a pull.

Be honest and direct. Don't sugarcoat weak hooks. 
Give specific, actionable feedback.

Respond ONLY with valid JSON matching this exact schema:
{{
  "score": <integer 0-100>,
  "grade": "<letter grade: A+, A, A-, B+, B, B-, C+, C, C-, D, F>",
  "verdict": "<one punchy sentence about this hook — be specific, not generic>",
  "strengths": ["<specific strength>", "<specific strength>"],
  "weaknesses": ["<specific weakness with fix>", "<specific weakness with fix>"],
  "platform_fit": "<one sentence about how well this fits the platform>",
  "word_count": <integer>,
  "optimal_word_count": "<range like '4-8 words for TikTok'>"
}}

Grade scale: A+(97-100), A(93-96), A-(90-92), B+(87-89), B(83-86), B-(80-82),
C+(77-79), C(73-76), C-(70-72), D+(67-69), D(60-66), F(below 60)"""

    user_prompt = f"""Score this hook for {platform.upper()}:

"{req.hook}"

Word count: {word_count} words
Optimal for {platform}: {optimal}"""

    result = gpt_json(system_prompt, user_prompt)

    # Ensure word_count is accurate (override AI's count with real count)
    result["word_count"] = word_count
    result["optimal_word_count"] = optimal

    # Validate score is in range
    result["score"] = max(0, min(100, int(result.get("score", 50))))

    return result


@app.post("/suggest", response_model=SuggestResponse, tags=["Hooks"])
def suggest_rewrites(req: SuggestRequest):
    """
    Generate 5 improved rewrites of a hook with predicted scores.
    Specify tone: casual, professional, funny, or shocking.
    """
    platform = normalize_platform(req.platform)
    platform_rules = PLATFORM_RULES[platform]
    optimal = PLATFORM_OPTIMAL_WORDS[platform]

    tone_guidance = {
        "casual": "conversational, relatable, feels like a friend talking — slang ok",
        "professional": "credible, authoritative, backed by expertise — no fluff",
        "funny": "unexpected humor, wit, self-aware, or absurdist — must be genuinely funny not just 'lol'",
        "shocking": "bold, unexpected, challenges assumptions, may be slightly controversial — stops the scroll",
    }

    system_prompt = f"""You are an elite hook copywriter. You've written viral content 
for accounts with millions of followers across all major platforms.

You specialize in transforming mediocre hooks into scroll-stopping openers.

Platform: {platform.upper()}
{platform_rules}

Requested tone: {req.tone} — {tone_guidance[req.tone]}

Your rewrites must:
1. Stay true to the core topic/message of the original
2. Match the requested tone authentically
3. Follow platform-specific length and style rules
4. Use proven hook formulas: curiosity gaps, specific numbers, controversy, 
   pattern interrupts, before/after frames, or bold claims
5. Each rewrite should use a DIFFERENT formula — don't just rephrase

SCORING RUBRIC for predicted_score:
- 90+: Extremely strong — opens a loop, specific, optimal length, stops scroll
- 80-89: Very strong — solid hook, minor improvement possible
- 70-79: Good — works, but missing one power element
- 60-69: Decent — better than average but needs more punch

Always give honest scores. Don't inflate predicted_score.

Respond ONLY with valid JSON:
{{
  "original_score": <integer, honest score of the original hook>,
  "suggestions": [
    {{"hook": "<rewritten hook>", "predicted_score": <integer>, "why": "<one sentence explaining the specific technique used>"}},
    {{"hook": "<rewritten hook>", "predicted_score": <integer>, "why": "<one sentence>"}},
    {{"hook": "<rewritten hook>", "predicted_score": <integer>, "why": "<one sentence>"}},
    {{"hook": "<rewritten hook>", "predicted_score": <integer>, "why": "<one sentence>"}},
    {{"hook": "<rewritten hook>", "predicted_score": <integer>, "why": "<one sentence>"}}
  ]
}}"""

    user_prompt = f"""Rewrite this hook for {platform.upper()} in a {req.tone} tone:

Original: "{req.hook}"

Optimal word count: {optimal}
Generate 5 improved versions, each using a different hook formula."""

    result = gpt_json(system_prompt, user_prompt)
    result["original_score"] = max(0, min(100, int(result.get("original_score", 50))))

    # Clamp all predicted scores
    for s in result.get("suggestions", []):
        s["predicted_score"] = max(0, min(100, int(s.get("predicted_score", 70))))

    return result


@app.post("/compare", response_model=CompareResponse, tags=["Hooks"])
def compare_hooks(req: CompareRequest):
    """
    Compare two hooks head-to-head for a specific platform.
    Returns a winner, individual scores, and detailed reasoning.
    """
    platform = normalize_platform(req.platform)
    platform_rules = PLATFORM_RULES[platform]

    system_prompt = f"""You are a senior content strategist who A/B tests hooks for 
a living. You've analyzed thousands of head-to-head hook comparisons and understand 
exactly what separates viral content from forgettable content.

Platform: {platform.upper()}
{platform_rules}

Evaluate both hooks on:
- Curiosity gap strength (does it open a loop that demands closing?)
- Specificity (numbers, names, concrete details beat vague claims)
- Emotional trigger (fear, excitement, FOMO, surprise)
- Word economy (every word should earn its place)
- Pattern interrupt (does it disrupt the scroll autopilot?)
- Platform fit (does it match the platform's style and optimal length?)

Be decisive. Pick a clear winner. If it's close, still pick one and explain why.

Respond ONLY with valid JSON:
{{
  "winner": "<A or B>",
  "score_a": <integer 0-100>,
  "score_b": <integer 0-100>,
  "reason": "<2-3 sentences explaining why the winner wins — be specific about what techniques make it stronger>",
  "audience_note": "<optional note about whether the loser might work better for a specific sub-audience or context>"
}}"""

    user_prompt = f"""Compare these two hooks for {platform.upper()}:

Hook A: "{req.hook_a}"
Hook B: "{req.hook_b}"

Which one wins? Why?"""

    result = gpt_json(system_prompt, user_prompt)
    result["score_a"] = max(0, min(100, int(result.get("score_a", 50))))
    result["score_b"] = max(0, min(100, int(result.get("score_b", 50))))

    # Ensure winner matches the actual scores
    winner = result.get("winner", "A").upper()
    if winner not in ("A", "B"):
        winner = "A" if result["score_a"] >= result["score_b"] else "B"
    result["winner"] = winner

    return result


@app.post("/classify", response_model=ClassifyResponse, tags=["Hooks"])
def classify_hook(req: ClassifyRequest):
    """
    Classify a hook into one of 10 types and get actionable improvement tips.
    Types: Curiosity Gap, Controversy/Hot Take, How-To, List Format, Story Hook,
    Fear/Loss, Social Proof, Challenge, Trend-Jacking, Question Hook.
    """
    types_list = ", ".join(HOOK_TYPES)

    system_prompt = f"""You are a content psychology expert who studies why hooks work.
You classify hooks into psychological categories and explain the mechanisms behind them.

Available hook types (you MUST pick one of these exactly):
{types_list}

For each type, you know:
- Curiosity Gap: Withholds information to create cognitive itch ("What happened next changed everything")
- Controversy/Hot Take: Challenges consensus to provoke reaction ("Unpopular opinion: gym culture is toxic")
- How-To: Promises a skill or outcome ("How I learned Spanish in 3 months")
- List Format: Sets a specific expectation of value ("5 things rich people never say")
- Story Hook: Opens a narrative loop ("I lost everything at 28. Here's what I learned.")
- Fear/Loss: Triggers loss aversion or fear of missing out ("Stop doing this before it's too late")
- Social Proof: Uses credibility signals ("I interviewed 100 CEOs — here's what they all said")
- Challenge: Dares the reader or sets a challenge ("Try this for 7 days. You won't regret it.")
- Trend-Jacking: Hijacks a current trend or cultural moment ("POV: you just discovered X")
- Question Hook: Opens with a question that demands an answer ("Are you actually smart or just lucky?")

CTR boost estimates are approximate benchmarks based on content performance data.

Respond ONLY with valid JSON:
{{
  "type": "<exact type name from the list>",
  "description": "<2-3 sentences explaining what this hook type is and why it works psychologically>",
  "best_platforms": ["<platform>", "<platform>"],
  "typical_ctr_boost": "<percentage or relative descriptor vs average, e.g. '18-24% above average'>",
  "tips": [
    "<specific, actionable tip to make this type of hook stronger>",
    "<tip 2>",
    "<tip 3>"
  ]
}}"""

    user_prompt = f"""Classify this hook and provide improvement tips:

"{req.hook}"

Pick the single best matching type from the list. Be specific in your tips."""

    return gpt_json(system_prompt, user_prompt)


@app.post("/batch", response_model=BatchResponse, tags=["Hooks"])
def batch_score(req: BatchRequest):
    """
    Score and rank up to 20 hooks at once for a platform.
    Returns hooks ranked from best to worst with a one-liner for each.
    """
    if len(req.hooks) > 20:
        raise HTTPException(status_code=400, detail="Maximum 20 hooks per batch request.")

    platform = normalize_platform(req.platform)
    platform_rules = PLATFORM_RULES[platform]

    hooks_formatted = "\n".join([f"{i+1}. \"{h}\"" for i, h in enumerate(req.hooks)])

    system_prompt = f"""You are a content performance analyst. You batch-score hooks 
for social media creators who are A/B testing their opening lines.

Platform: {platform.upper()}
{platform_rules}

Score each hook honestly on a 0-100 scale using these benchmarks:
- 90+: Extremely strong — pattern interrupt + curiosity + optimal length
- 80-89: Very strong — most elements present, minor gap
- 70-79: Solid — works, missing one power element  
- 60-69: Below average — some potential, needs work
- 50-59: Weak — generic, no real hook
- Below 50: Won't stop the scroll

For one_liner: be specific and concise (max 8 words). Name the exact technique or flaw.
Examples: "strong curiosity gap, perfect length", "too vague, no specific promise",
"controversy hook, slightly too long", "question format, lacks urgency"

Return hooks sorted by score (highest first). Include the original hook text exactly.

Respond ONLY with valid JSON:
{{
  "ranked": [
    {{"rank": 1, "hook": "<exact original text>", "score": <int>, "one_liner": "<specific 2-6 word critique>"}},
    ...
  ],
  "best": "<exact text of highest scoring hook>",
  "worst": "<exact text of lowest scoring hook>"
}}"""

    user_prompt = f"""Score and rank these {len(req.hooks)} hooks for {platform.upper()}:

{hooks_formatted}

Return them sorted from best to worst score."""

    result = gpt_json(system_prompt, user_prompt)

    # Validate and clamp scores
    for item in result.get("ranked", []):
        item["score"] = max(0, min(100, int(item.get("score", 50))))

    return result


@app.post("/emoji-impact", response_model=EmojiImpactResponse, tags=["Hooks"])
def emoji_impact(req: EmojiImpactRequest):
    """
    Analyze how emojis affect a hook's scroll-stopping power.
    Returns scores with/without emojis, per-emoji analysis, and an optimized version.
    """
    # Extract emojis from the hook for context
    emoji_pattern = re.compile(
        "[\U00010000-\U0010FFFF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F300-\U0001F5FF"
        "\U0001F600-\U0001F64F"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "]+",
        flags=re.UNICODE,
    )
    found_emojis = emoji_pattern.findall(req.hook)

    system_prompt = """You are a social media optimization expert who specializes in 
the psychology of visual elements in content hooks.

You understand how emojis affect reader perception:

POSITIVE emoji uses:
- 🔥 🚨 ⚡ ✅ — add urgency, energy, or validation
- Emojis that reinforce the message content
- 1-2 emojis max, placed strategically (start or end)
- Emojis that replace words (more efficient)

NEGATIVE emoji uses:
- 💯 🙌 👇 — overused, signal low-quality content or desperation
- Emoji spam (3+ emojis) — reduces credibility
- Emojis that contradict or distract from the message
- Using emojis where text alone would be stronger (professional platforms)

Scoring impact:
- Good emojis can add +3 to +8 points by adding visual breaks and energy
- Bad emojis can subtract -5 to -15 points by signaling spam or low quality
- No emojis is often better than bad emojis

For recommended_version: provide the optimal version of the hook 
(keep good emojis, remove bad ones, may suggest better placement).

Respond ONLY with valid JSON:
{
  "score_with_emojis": <integer 0-100, score of the hook exactly as written>,
  "score_without_emojis": <integer 0-100, estimated score with all emojis removed>,
  "emoji_analysis": [
    {"emoji": "<the emoji>", "impact": "<positive|negative|neutral>", "reason": "<specific reason>"},
    ...one entry per unique emoji
  ],
  "recommended_version": "<optimized hook — keep good emojis, fix/remove bad ones>"
}

If there are no emojis in the hook, still return the structure but with empty emoji_analysis 
and explain in recommended_version that adding a strategic emoji could help."""

    user_prompt = f"""Analyze the emoji impact in this hook:

"{req.hook}"

Emojis detected: {found_emojis if found_emojis else 'none'}

Score it with emojis (as written) and without emojis (estimated).
Analyze each emoji's impact and provide the optimal version."""

    result = gpt_json(system_prompt, user_prompt)
    result["score_with_emojis"] = max(0, min(100, int(result.get("score_with_emojis", 50))))
    result["score_without_emojis"] = max(0, min(100, int(result.get("score_without_emojis", 50))))

    return result
