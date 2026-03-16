# Cost Calculator — Faceless Video Channel

> Exact per-video cost breakdown across 3 production approaches.
> Last updated: March 2026. All prices in USD.

---

## Pricing Reference (March 2026)

| Service | Unit | Price |
|---|---|---|
| Claude Sonnet 4 API | per 1K tokens | ~$0.003 input / $0.015 output |
| OpenAI TTS-1-HD | per 1K characters | $0.015 |
| ElevenLabs Creator | monthly flat | $22/mo (100K chars) |
| ElevenLabs Pro | monthly flat | $99/mo (500K chars) |
| OpenAI Whisper | per minute of audio | $0.006 |
| Pexels API | per download | Free |
| Storyblocks | annual | $149/year = $12.42/mo |
| Kling AI Standard 5s | per clip | ~$0.09 |
| Kling AI Pro 10s | per clip | ~$0.62 |
| Runway Gen-3 | per second | ~$0.05 |
| DALL-E 3 HD | per image | $0.080 |
| Ideogram 2.0 | per image | ~$0.08 |
| YouTube API | per video | Free |

---

## Approach 1: Budget (Free Tools + OpenAI TTS)

**Philosophy:** Spend as little as possible. Quality is "good enough to post." Use stock footage everywhere. Great for testing a niche before investing.

### Cost Per 1-Minute Video

| Component | Tool | Calculation | Cost |
|---|---|---|---|
| Script | Claude Sonnet 4 | ~1,200 tokens total | $0.02 |
| Voiceover | OpenAI TTS-1-HD | 170 words ≈ 1,000 chars | $0.015 |
| Visuals | Pexels API | 10–12 clips | $0.00 |
| Assembly | FFmpeg | — | $0.00 |
| Captions | Whisper API | 1 minute of audio | $0.006 |
| Thumbnail | DALL-E 3 (standard) | 1 image | $0.040 |
| Upload | YouTube API | — | $0.00 |
| **TOTAL** | | | **~$0.08** |

**Yes, that's 8 cents per video.**

### Cost Per 10-Minute Video

| Component | Tool | Calculation | Cost |
|---|---|---|---|
| Script | Claude Sonnet 4 | ~8,000 tokens total | $0.12 |
| Voiceover | OpenAI TTS-1-HD | 1,700 words ≈ 10,000 chars | $0.15 |
| Visuals | Pexels API | 60–80 clips | $0.00 |
| Assembly | FFmpeg | — | $0.00 |
| Captions | Whisper API | 10 minutes of audio | $0.06 |
| Thumbnail | DALL-E 3 (standard) | 1 image | $0.040 |
| Upload | YouTube API | — | $0.00 |
| **TOTAL** | | | **~$0.37** |

### Monthly Costs at Scale

| Videos/month | Cost/video | Total API | Tool subscriptions | **Total/month** |
|---|---|---|---|---|
| 10 | $0.37 | $3.70 | $0 | **$3.70** |
| 30 | $0.37 | $11.10 | $0 | **$11.10** |
| 100 | $0.37 | $37.00 | $0 | **$37.00** |

**Limitations:** OpenAI TTS sounds noticeably AI. Stock footage won't always match your content perfectly. No character consistency. Thumbnail quality is inconsistent.

---

## Approach 2: Mid (ElevenLabs + Kling AI mix)

**Philosophy:** Professional quality that can compete on a real channel. ElevenLabs voice is near-human. Mix of AI-generated clips for key scenes and free stock for B-roll.

**Assumption:** 70% of clips from Pexels, 30% from Kling AI Standard

### Cost Per 1-Minute Video

| Component | Tool | Calculation | Cost |
|---|---|---|---|
| Script | Claude Sonnet 4 | ~1,200 tokens | $0.02 |
| Voiceover | ElevenLabs | 1,000 chars ÷ 100K/mo × $22 | $0.22 |
| Visuals | Pexels (70%) + Kling Std (30%) | 3 Kling clips × $0.09 | $0.27 |
| Assembly | FFmpeg | — | $0.00 |
| Captions | AssemblyAI | 1 min × $0.009 | $0.009 |
| Thumbnail | Ideogram 2.0 | 1 image | $0.08 |
| Upload | YouTube API | — | $0.00 |
| **TOTAL** | | | **~$0.60** |

### Cost Per 10-Minute Video

| Component | Tool | Calculation | Cost |
|---|---|---|---|
| Script | Claude Sonnet 4 | ~8,000 tokens | $0.12 |
| Voiceover | ElevenLabs | 10,000 chars ÷ 100K/mo × $22 | $2.20 |
| Visuals | Pexels (70%) + Kling Std (30%) | 18 Kling clips × $0.09 | $1.62 |
| Assembly | FFmpeg | — | $0.00 |
| Captions | AssemblyAI | 10 min × $0.009 | $0.09 |
| Thumbnail | Ideogram 2.0 | 1 image | $0.08 |
| Upload | YouTube API | — | $0.00 |
| **TOTAL** | | | **~$4.11** |

### Monthly Costs at Scale

| Videos/month | Length | API costs | ElevenLabs sub | Kling (over-plan) | **Total/month** |
|---|---|---|---|---|---|
| 10 × 10min | 10 min | $19.10 | $22 | ~$0 | **~$41** |
| 30 × 10min | 10 min | $57.30 | $22 | ~$30 overage | **~$109** |
| 4 × 10min | 10 min | $7.64 | $22 | $0 | **~$30** |

**Note:** ElevenLabs Creator gives 100K chars/mo. 10-min video = ~10K chars. That's **10 videos/month included**. Beyond that, pay overage or upgrade.

---

## Approach 3: Premium (Everything Best Quality)

**Philosophy:** Build a channel that looks better than 95% of AI channels. Kling AI Pro for all visuals, ElevenLabs Pro cloned voice, premium thumbnail generation, word-level captions.

### Cost Per 1-Minute Video

| Component | Tool | Calculation | Cost |
|---|---|---|---|
| Script | Claude Opus 4 | ~2,000 tokens | $0.06 |
| Voiceover | ElevenLabs Pro API | 1,000 chars × overage rate | $0.22 |
| Visuals | Kling Pro (all clips) | 10 clips × $0.40 | $4.00 |
| Assembly | FFmpeg + Creatomate | — | $0.08 |
| Captions | AssemblyAI (word-level) | 1 min | $0.012 |
| Thumbnail | Midjourney (manual) or Flux 1.1 | 1 image | $0.04 |
| Upload | YouTube API | — | $0.00 |
| **TOTAL** | | | **~$4.41** |

### Cost Per 10-Minute Video

| Component | Tool | Calculation | Cost |
|---|---|---|---|
| Script | Claude Opus 4 | ~15,000 tokens | $0.45 |
| Voiceover | ElevenLabs Pro API | 10,000 chars | $2.20 |
| Visuals | Kling Pro (60% clips) | 35 Kling Pro clips × $0.40 | $14.00 |
| Assembly | FFmpeg | — | $0.00 |
| Captions | AssemblyAI (word-level) | 10 min | $0.12 |
| Thumbnail | Flux 1.1 Pro | 2 candidates | $0.08 |
| Upload | YouTube API | — | $0.00 |
| **TOTAL** | | | **~$16.85** |

### Monthly Costs at Scale

| Videos/month | Length | API costs | Subscriptions | **Total/month** |
|---|---|---|---|---|
| 10 × 10min | 10 min | $168.50 | ElevenLabs Pro $99 + Claude Pro $20 | **~$287** |
| 20 × 10min | 10 min | $337.00 | Same subs | **~$456** |
| 4 × 10min | 10 min | $67.40 | ElevenLabs Creator $22 | **~$90** |

---

## Side-by-Side Comparison

| Metric | Budget | Mid | Premium |
|---|---|---|---|
| Cost per 10-min video | $0.37 | $4.11 | $16.85 |
| Voice quality | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Visual quality | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Character consistency | ❌ | ⚠️ Partial | ✅ Strong |
| Monthly cost (10 vids) | $3.70 | $41 | $287 |
| Competitive viability | Low | High | Very High |

---

## Break-Even Analysis

### How much does YouTube pay?

YouTube RPM (Revenue Per 1,000 Views) varies by niche:
| Niche | RPM Range | Average |
|---|---|---|
| Finance | $10–$21 | $15 |
| True Crime | $8–$12 | $10 |
| History | $6–$10 | $8 |
| Tech Explained | $8–$12 | $10 |
| Motivation | $5–$9 | $7 |
| Health/Wellness | $8–$14 | $11 |
| Prediction Markets | $8–$14 | $11 |

**RPM Note:** You earn RPM on ~40–60% of total views (those that get an ad). So "earned RPM" is approximately: views × 0.45 × RPM ÷ 1000

### Break-Even Calculator

**Scenario: Mid approach, Finance niche**
- Cost per 10-min video: $4.11
- RPM: $15
- Break-even views per video: `4.11 ÷ (15 × 0.45) = 4.11 ÷ 6.75 = ~609 views`

**You break even at just 609 views per video.** A finance channel with 10K subscribers should easily get 300–1,000 views per video.

---

### Revenue at 100K Subscribers

Assuming:
- 2 videos/week uploaded
- 3% of subs watch each video = 3,000 views/video
- Budget approach (cost: $0.37/video)

| Niche | RPM | Revenue/video | Cost/video | Profit/video |
|---|---|---|---|---|
| Finance | $15 | $20.25 | $0.37 | **$19.88** |
| History | $8 | $10.80 | $0.37 | **$10.43** |
| Motivation | $7 | $9.45 | $0.37 | **$9.08** |

**Monthly profit at 100K subs, 8 videos/month, Finance niche, Budget approach:**
`8 × $19.88 = ~$159/month from YouTube ads alone`

That seems low — because it is at only 3% view rate. Channels with 100K subs that post consistently + have good click-through often average 5–10% view rate.

**At 8% view rate (8,000 views/video):**
- Finance, mid approach: `8 × ($54 - $4.11) = ~$399/month`

**At 100K subs with viral potential (1 video hits 50K views):**
- Finance, mid: `50,000 × (15 × 0.45 ÷ 1000) = $337.50 from one video`

### Additional Revenue Streams (NOT counting above)

| Revenue Stream | Realistic at 100K subs | Notes |
|---|---|---|
| Affiliate marketing | $200–$2,000/mo | Finance niche: financial products pay 20–50% commission |
| Sponsorships | $500–$5,000/video | After ~50K subs with engaged audience |
| Digital products | $500–$5,000/mo | Course, ebook, template |
| Patreon/membership | $100–$1,000/mo | Loyal audience, exclusive content |
| Course sales | $1,000–$10,000/mo | High-ticket offer |

**Realistic Total Monthly Revenue at 100K Subscribers (Finance, Mid production quality):**
- YouTube AdSense: $400–$800
- Affiliate links: $300–$1,000
- Sponsorships: $500–$2,000 (1–2 per month)
- **Total: $1,200–$3,800/month**

**At this production quality and cost ($41/mo for 10 videos), you're looking at 20–90x ROI.**

---

## Recommended Starting Strategy

**Phase 1 (Months 1–3): Budget approach**
- Prove the niche works before spending more
- Test 2–3 topics per week
- Total monthly spend: under $15
- Goal: Find 1–2 video formats that break 1K views

**Phase 2 (Months 4–6): Mid approach**
- Upgrade to ElevenLabs + mixed Kling visuals
- Focus on top-performing formats
- Total monthly spend: ~$40–$80
- Goal: Hit 1K subscribers + YouTube Partner Program threshold

**Phase 3 (Month 7+): Premium on hero content**
- Use premium production for "pillar" content (longer, evergreen)
- Budget approach for short-form/frequent posts
- Add affiliate links, sponsor spots
- Goal: Replace the day job

---

*Related: See `niche-research.md` for RPM data by niche and `quick-start.md` for starting at €0.*
