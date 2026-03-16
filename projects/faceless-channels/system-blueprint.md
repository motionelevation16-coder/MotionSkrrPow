# Faceless Video Channel Automation System — System Blueprint

> **Core promise:** Topic in → Upload-ready video out. Zero face, minimum human.
> Last updated: March 2026

---

## Overview

This system is an 8-step pipeline that transforms a topic or niche idea into a fully produced, ready-to-upload video. The operator's only jobs are: (1) pick a topic, (2) press go, (3) hit upload.

Everything between those two points is automated.

```
[TOPIC INPUT]
     │
     ▼
[1. Topic Discovery] → trending topic + angle
     │
     ▼
[2. Script Generation] → 800–2000 word script
     │
     ▼
[3. Voiceover] → MP3 audio file
     │
     ▼
[4. Visuals] → video clips (AI-generated or stock)
     │
     ▼
[5. Assembly] → combined video + audio
     │
     ▼
[6. Captions] → burned-in subtitles
     │
     ▼
[7. Thumbnail] → JPG thumbnail image
     │
     ▼
[8. Upload + Schedule] → live on YouTube/TikTok
```

---

## Step 1: Topic/Niche Selection

### Goal
Find topics that are currently trending, have high search demand, and are easy to produce as AI video.

### Recommended Tool: **YouTube Data API v3 + Google Trends API**
- **Cost:** Free
- **How:** Query YouTube for most-viewed videos in your niche in the last 7–30 days. Cross-reference with Google Trends to confirm search spike.
- **Automation angle:** n8n runs a daily job that scrapes the top 10 rising topics in your niche and drops them into a queue.

### Secondary Signal Sources
| Source | What to extract | Cost |
|---|---|---|
| YouTube Data API | Video titles with 100K+ views, <30 days old | Free |
| Google Trends RSS | Trending searches in your country | Free |
| Reddit (subreddit top posts) | What people are asking about | Free |
| Twitter/X search API | Viral threads in your niche | Free tier limited |
| Exploding Topics | Early trend detection | $39/mo paid tier |

### The Prompt-Based Fallback (cheapest)
Feed Claude or GPT-4 a prompt like:
```
You are a YouTube content strategist. Given the niche [FINANCE], 
give me 10 video titles that are currently trending and easy to 
explain with AI-generated visuals. Focus on evergreen topics with 
high search demand. Format: title | angle | hook (first 10 seconds).
```

### Best pick for 2026
**Free approach:** YouTube Data API + Google Trends, automated via n8n daily cron. Store topics in a Google Sheet or Airtable queue. Operator reviews queue weekly, approves topics for production.

---

## Step 2: Script Generation

### Goal
A well-structured, engaging script optimized for the voiceover format. 150–200 words per minute → 1-min script ≈ 170 words, 10-min script ≈ 1,700 words.

### Recommended Tool: **Claude API (claude-sonnet-4 or claude-opus)**
- **Cost:** ~$0.003–$0.015 per 1,000 tokens (Sonnet). A 1,500-word script ≈ 2,000 tokens = **~$0.006 per script**.
- **Why Claude over GPT/Gemini:** Produces better narrative structure, more natural spoken-word rhythm, and avoids AI-sounding filler phrases. Better at following custom style prompts ("sound like a human, not a textbook").

### Script Template Prompt
```
You are a professional YouTube scriptwriter for a [NICHE] channel.

Write a script for: "[TOPIC TITLE]"

Format:
- Hook (15 seconds, question or shocking stat)
- Section 1: [Context]
- Section 2: [Main insight]
- Section 3: [Deeper detail]
- Outro (CTA: subscribe, comment)

Rules:
- Conversational tone. Short sentences. No jargon.
- No "In conclusion" or "As we can see"
- Written to be read aloud — use em dashes, not commas
- Include [PAUSE] markers where the voiceover should pause
- Include [VISUAL: brief description] cues for the video editor

Length: ~[X] words for [Y] minute video
```

### Alternatives
| Tool | Best for | Cost |
|---|---|---|
| **Claude Sonnet 4** | Long-form, natural narrative | ~$0.006/script |
| **GPT-4o** | Good all-rounder, faster | ~$0.006/script |
| **Gemini 1.5 Pro** | Cheapest at scale | ~$0.002/script |
| **Llama 3.3 (self-hosted)** | Zero API cost if you have a GPU | $0 after setup |

### Best pick for 2026
**Claude Sonnet 4** via API — best quality/cost ratio. The difference in script quality over cheaper models is visible in viewer retention. For high-volume production (30+ videos/month), consider Gemini 1.5 Pro to reduce costs.

---

## Step 3: Voiceover (TTS)

### Goal
A natural, engaging voice that doesn't sound robotic. This is the #2 most important quality signal after visuals.

### Recommended Tool: **ElevenLabs**
- **Cost:** 
  - Free: 10,000 characters/month (~8 min of audio)
  - Starter ($5/mo): 30,000 characters (~25 min)
  - Creator ($22/mo): 100,000 characters (~80 min) + voice cloning
  - Pro ($99/mo): 500,000 characters + API access
- **Why:** Best voice naturalness in 2026. Handles pacing, emotion, emphasis. The clone-your-own-voice feature lets you build a consistent channel voice.
- **API:** Yes, full API. POST request with text → returns MP3. Easy to integrate in n8n.

### Voice Strategy
For a faceless channel, you have 3 options:
1. **Pre-made ElevenLabs voices** (Adam, Brian, etc.) — fast, no setup
2. **Clone a voice** (your own or a hired voice actor's, with consent) — max consistency, creates a channel brand
3. **Use OpenAI TTS** for budget — decent quality, half the price

### Alternatives
| Tool | Quality | Cost (per 1K chars) | API? |
|---|---|---|---|
| **ElevenLabs** | ⭐⭐⭐⭐⭐ | ~$0.22 (Creator plan) | Yes |
| **OpenAI TTS-1-HD** | ⭐⭐⭐⭐ | ~$0.015/1K chars | Yes |
| **PlayHT** | ⭐⭐⭐⭐ | $0.008–$0.02/1K chars | Yes |
| **Murf AI** | ⭐⭐⭐ | $26/mo flat | Limited |
| **Google TTS (WaveNet)** | ⭐⭐⭐ | $0.016/1K chars | Yes |

### Best pick for 2026
- **Budget:** OpenAI TTS-1-HD. ~$0.015/1K chars, good quality, simple API.
- **Quality:** ElevenLabs Creator at $22/mo. Use the same custom voice every video = channel brand.
- **Scale (50+ vids/month):** ElevenLabs Pro API at $99/mo for volume.

**Key tip:** A 10-minute script is ~1,700 words ≈ 10,000 characters. So ElevenLabs Creator plan covers ~10 videos/month. Budget accordingly.

---

## Step 4: Visuals

### The Core Choice: AI-Generated Video vs. Stock Footage

This is the biggest cost and quality decision. Two valid paths:

---

### Path A: Stock Footage (Budget)
**Tool: Pexels API (free) + Pixabay API (free)**
- Zero cost. Unlimited downloads.
- Works well for: finance, history (archive footage look), nature/ambient, motivation
- Weakness: footage must match script topics, limited unique assets
- Automation: n8n pulls clips using keyword search from script's [VISUAL] cues

**Storyblocks API** — $149/year unlimited for commercial use. Much larger library.

---

### Path B: AI-Generated Video (Mid/Premium)

#### Recommended Tool: **Kling AI 3.0**
- **Cost:** 
  - Standard 5s clips: ~$0.09/clip (at volume)
  - Professional 10s clips: ~$0.62/clip
  - API: ~$0.07–$0.14/second of video
- **Why Kling in 2026:** 
  - "Elements" feature: combine up to 4 reference images to maintain character consistency across clips (huge for faceless channels with a recurring character)
  - Best-in-class motion quality for the price
  - Handles cinematic camera movements
  - Image-to-video from a reference image = style consistency

#### Alternatives
| Tool | Quality | Cost | Character Consistency |
|---|---|---|---|
| **Kling AI 3.0** | ⭐⭐⭐⭐⭐ | $0.09–$0.62/clip | ✅ Elements feature |
| **Runway Gen-3 Alpha** | ⭐⭐⭐⭐⭐ | $0.05–$0.10/second | ❌ Limited |
| **Pika 2.2** | ⭐⭐⭐⭐ | $0.08/credit | ❌ Limited |
| **Hailuo/MiniMax** | ⭐⭐⭐⭐ | ~$0.05/clip | ⚠️ Moderate |
| **Luma Dream Machine** | ⭐⭐⭐⭐ | $0.03–$0.05/clip | ❌ No |

### Visual Style Strategy
For a 10-minute video, you need roughly 30–60 clips (5–10 seconds each). The math:
- Budget (Pexels): $0
- Mid (Kling Standard): 40 clips × $0.09 = **~$3.60**
- Premium (Kling Pro): 40 clips × $0.40 = **~$16**

**Recommended approach:** Use stock footage for background scenes + AI-generated clips for character moments/hero shots. Hybrid cuts costs by 60–70%.

### Best pick for 2026
- **Budget:** Pexels API + Pixabay API for stock footage, automated by keyword.
- **Quality/Consistency:** Kling AI 3.0 with Elements feature for character-driven channels.
- **Scale:** Mix Kling (for key scenes) + Pexels (for B-roll), saving budget for what viewers actually focus on.

---

## Step 5: Assembly

### Goal
Combine voiceover + video clips in exact sync, add music, add branding.

### Recommended Tool: **FFmpeg (free, open-source)**
- **Cost:** $0
- **Why:** The industry standard for programmatic video editing. Works entirely from command line/API. No GUI needed. Handles:
  - Concatenating clips
  - Syncing audio to video
  - Adding background music with volume ducking
  - Adding intro/outro bumpers
  - Applying color grading filters
  - Burning in subtitles (SRT format)
- **Automation:** n8n runs FFmpeg commands via Execute Command node.

### Assembly Workflow
```bash
# Step 1: Concatenate video clips
ffmpeg -f concat -safe 0 -i clips_list.txt -c copy raw_video.mp4

# Step 2: Add voiceover + background music (ducked at -18dB)
ffmpeg -i raw_video.mp4 -i voiceover.mp3 -i bgmusic.mp3 \
  -filter_complex "[2:a]volume=0.15[music];[1:a][music]amix=inputs=2[audio]" \
  -map 0:v -map "[audio]" assembled.mp4

# Step 3: Add subtitles
ffmpeg -i assembled.mp4 -vf subtitles=captions.srt final.mp4
```

### Alternatives
| Tool | Automation-Friendly | Cost |
|---|---|---|
| **FFmpeg** | ✅ 100% CLI | Free |
| **Remotion** | ✅ React/JS-based | Free (OSS) |
| **Creatomate** | ✅ REST API | $59/mo |
| **JSON2Video** | ✅ REST API | $20/mo |
| **CapCut API** | ❌ No public API | N/A |

### Best pick for 2026
**FFmpeg** for total control + zero cost. If you want a more developer-friendly API layer, **Creatomate** is excellent (you send JSON, get back an MP4). For an n8n workflow, both work.

---

## Step 6: Captions / Subtitles

### Goal
Auto-generate accurate captions, burn them into the video OR deliver as SRT file.

### Recommended Tool: **OpenAI Whisper API**
- **Cost:** $0.006/minute of audio (extremely cheap)
- **Why:** Best transcription accuracy. Returns timestamped segments which become the SRT file. Direct API call.
- **Flow:** voiceover.mp3 → Whisper → SRT file → FFmpeg burns into video

### Alternatives
| Tool | Accuracy | Cost | API |
|---|---|---|---|
| **OpenAI Whisper API** | ⭐⭐⭐⭐⭐ | $0.006/min | Yes |
| **AssemblyAI** | ⭐⭐⭐⭐⭐ | $0.009/min | Yes |
| **Whisper (self-hosted)** | ⭐⭐⭐⭐⭐ | $0 (GPU cost) | Local |
| **Deepgram** | ⭐⭐⭐⭐ | $0.0043/min | Yes |
| **Google Speech-to-Text** | ⭐⭐⭐⭐ | $0.006/min | Yes |

### Caption Styling
Viral caption style (big centered text, one phrase at a time) significantly increases watch time. Use FFmpeg's `drawtext` filter or burn in styled SRT.
- Font: Montserrat Bold, white with black outline
- Size: ~60px for 1080p
- Highlight the current word in yellow (requires word-level timestamps from AssemblyAI or Whisper)

### Best pick for 2026
**OpenAI Whisper API** for standard captions. **AssemblyAI** if you want word-level timestamps for the viral "highlighted word" caption style.

---

## Step 7: Thumbnail Generation

### Goal
A compelling thumbnail that gets clicked. This is arguably the most important part of a YouTube video's success.

### Recommended Tool: **DALL-E 3 API (via OpenAI)**
- **Cost:** $0.040 per image (1024×1024), $0.080 for HD
- **Why:** Fast, API-accessible, good at text rendering since late 2024. Can follow brand style guidelines via prompt.

### Thumbnail Formula
1. Generate 3–5 candidate images via DALL-E 3 using a prompt based on the video title
2. Layer the title text using FFmpeg or a Canva template
3. (Optional) A/B test thumbnails via YouTube's built-in test feature

### Alternatives
| Tool | Quality | Cost | API? |
|---|---|---|---|
| **DALL-E 3** | ⭐⭐⭐⭐ | $0.04–$0.08/img | Yes |
| **Ideogram 2.0** | ⭐⭐⭐⭐⭐ | $0.08/img | Yes |
| **Leonardo AI** | ⭐⭐⭐⭐ | $0.02/img | Yes |
| **Midjourney** | ⭐⭐⭐⭐⭐ | $10/mo (no API) | ❌ No API |
| **Flux 1.1 Pro** | ⭐⭐⭐⭐⭐ | $0.04/img | Yes |

### Best pick for 2026
**Ideogram 2.0** or **Flux 1.1 Pro** via API for quality. **DALL-E 3** for simplicity (already in OpenAI account). For non-character thumbnails (text + abstract), Ideogram is the best for text accuracy in images.

---

## Step 8: Upload + Scheduling

### Goal
Automatically upload the finished video to YouTube (and optionally TikTok/Instagram Reels) with metadata: title, description, tags, category, thumbnail.

### Recommended Tool: **YouTube Data API v3**
- **Cost:** Free
- **Quota:** 10,000 units/day. One video upload = ~1,600 units. So ~6 uploads/day free.
- **What you can automate:**
  - Upload video file
  - Set title, description, tags
  - Set thumbnail
  - Set publish time (schedule)
  - Set category + audience settings

### n8n Integration
n8n has a native **YouTube node** that handles OAuth and all upload actions without custom code.

Workflow:
1. n8n YouTube node: `Upload Video` action
2. Pass: video file path, title (from script generator), description (auto-generated), tags (from topic), publish time (scheduled)
3. n8n YouTube node: `Set Thumbnail` action — upload generated thumbnail JPG

### Multi-Platform
| Platform | Method | Notes |
|---|---|---|
| **YouTube** | YouTube Data API v3 | Full automation, native n8n node |
| **TikTok** | TikTok Content Posting API | OAuth2, some manual steps still |
| **Instagram Reels** | Meta Graph API | Works for Reels, requires Business account |
| **Facebook** | Meta Graph API | Easy once Meta app set up |

### Scheduling Strategy
- Post YouTube: Tuesday–Thursday, 12pm–3pm in target audience's timezone
- Post TikTok: Same-day for short cuts, different account branding
- Use n8n CRON trigger to schedule uploads weekly

### Best pick for 2026
**YouTube Data API v3** via n8n's native YouTube node. Zero cost, full control. Add TikTok API for cross-posting the short-form version (60–90 second cut).

---

## Complete Pipeline Summary

| Step | Tool | Monthly Cost (50 videos) | Automation Level |
|---|---|---|---|
| Topic Discovery | YouTube API + Claude | ~$5 | ✅ Full |
| Script | Claude Sonnet 4 API | ~$2 | ✅ Full |
| Voiceover | ElevenLabs Creator | $22 | ✅ Full |
| Visuals | Pexels API (free) | $0 | ✅ Full |
| Assembly | FFmpeg | $0 | ✅ Full |
| Captions | Whisper API | ~$3 | ✅ Full |
| Thumbnail | DALL-E 3 API | ~$4 | ✅ Full |
| Upload | YouTube API v3 | $0 | ✅ Full |
| **TOTAL (Budget)** | | **~$36/month** | |

---

## The Character Consistency Problem

The #1 pain point for AI video channels: generating a character that looks the same across 40 different clips in a video.

### Current Best Solutions (2026)

**Option 1: Kling AI "Elements" Feature**
- Upload 1–4 reference images of your character
- Every generation uses these as consistency anchors
- Best quality/ease ratio right now
- Limitation: ~80–85% consistency, occasional drift

**Option 2: Stable Diffusion + LoRA (self-hosted)**
- Train a LoRA on 20–30 images of your character
- 95%+ consistency
- Requires GPU (or Runpod ~$0.44/hr)
- Technical setup: 2–4 hours initial, then automated

**Option 3: HeyGen Custom Avatar**
- Record 2 minutes of yourself (or hire talent)
- HeyGen clones the avatar
- 100% consistent — it's always the same avatar
- Cost: starts at $29/month
- Best for: talking-head style channels

**Recommended path for faceless channels:** 
→ See `character-consistency.md` for the full deep dive.

---

*Next: See `n8n-workflow-design.md` for how to implement this in n8n.*
