# Faceless Channel — Step-by-Step Automation Pipeline
*One video, start to finish. Copy this workflow exactly.*

---

## Overview

| Phase | What | Time | Automation Level |
|-------|------|------|-----------------|
| 1. Topic & Script | Find topic, write script | 5 min | 90% automated |
| 2. Voiceover | Generate audio | 2 min | 100% automated |
| 3. Visuals | Footage or AI clips | 10-20 min | 50-80% automated |
| 4. Assembly & Editing | Combine everything | 10 min | 70% automated |
| 5. Publishing | Upload, schedule | 2 min | 95% automated |
| **Total** | | **~30-40 min** | **~80% automated** |

At full pipeline maturity (templates set, n8n running), this drops to **15-20 min of actual human attention** per video.

---

## Phase 1 — Topic & Script (5 min, mostly automated)

### Step 1.1: Find Trending Topics Automatically

**Method 1: Google Trends (free, manual check)**
- Go to trends.google.com → "Trending Now" → filter by category
- Look for topics in your niche with "Breakout" status (spike in searches)
- Copy 3 candidates to your Google Sheet

**Method 2: n8n Daily Topic Finder (automated — see n8n-workflow-design.md)**
- Runs daily at 9AM
- Pulls YouTube trending + Google Trends via RapidAPI
- Filters by your niche keywords
- Appends to Google Sheet
- Sends Telegram notification with top 3 topics

**Method 3: YouTube Search (2 min manual)**
- Search your niche keyword on YouTube
- Sort by "This week"
- Look at videos with 50k-500k views from channels with <100k subscribers (that means the topic is trending, not the channel)
- Write down the topic

**Method 4: Reddit + Twitter/X (2 min scan)**
- r/investing, r/AItools, r/todayilearned depending on niche
- What's being discussed = what people want to watch

---

### Step 1.2: Generate the Script

**The Master Script Prompt (copy-paste this into Claude):**

```
You are a faceless YouTube channel script writer. Write a script for the following video:

TOPIC: [paste topic here]
CHANNEL STYLE: [informative/storytelling/listicle/explainer]
FORMAT: [short-form 60s / long-form 8-10 min]
TONE: [confident, direct, slightly conversational — no filler words]
AUDIENCE: [describe target viewer]

Script requirements:
- Start with a HOOK in the first 3 seconds (question, shocking stat, or bold statement)
- NO intro ("Hey guys, welcome back to...") — jump straight into the content
- Write in short punchy sentences optimized for voiceover
- Add [PAUSE] markers where natural breath would occur
- Add [EMPHASIS] markers on key words
- Add [SCENE: description] tags every 20-30 seconds for the video editor
- End with a soft CTA: "If you want [outcome], [subscribe/check description]"
- Do NOT use filler words: "essentially", "basically", "literally", "actually"

[For short-form] Target word count: 130-150 words (= ~60 seconds at average TTS pace)
[For long-form] Target word count: 1,400-1,600 words (= ~9-10 minutes)
```

**Example output structure:**

```
[SCENE: Close-up of stock ticker screen, red numbers falling]
The stock market just lost 2 trillion dollars in 48 hours. [PAUSE]
[EMPHASIS]And most people have no idea why.[EMPHASIS] [PAUSE]

[SCENE: World map with flashing geopolitical markers]
Here's what actually happened — and what it means for your money.
...
```

---

### Script Structure: Short-Form (60 seconds)

```
0:00-0:03  HOOK — shocking stat, question, or bold claim
0:03-0:10  SETUP — context for why this matters
0:10-0:45  CONTENT — 3-4 key points, one sentence each
0:45-0:55  PAYOFF — the answer/conclusion
0:55-1:00  CTA — subscribe, check description, follow
```

Word count target: **130-150 words**

---

### Script Structure: Long-Form (8-12 min)

```
0:00-0:30   HOOK — most compelling moment from the video
0:30-1:00   PREMISE — what we're covering and why you should care
1:00-2:30   SECTION 1 — first major point with evidence/example
2:30-4:00   SECTION 2 — second major point, builds on first
4:00-5:30   SECTION 3 — third major point, adds complexity
5:30-7:00   SECTION 4 — fourth major point or counterargument
7:00-8:30   SYNTHESIS — connecting the dots
8:30-9:30   IMPLICATIONS — what this means for the viewer
9:30-10:00  CTA — subscribe, affiliate mention, next video tease
```

Word count target: **1,400-1,600 words**

---

## Phase 2 — Voiceover (2 min, fully automated)

### ElevenLabs Workflow

**Voice Settings for YouTube Narration:**
- Go to elevenlabs.io → Speech Synthesis
- **Voice:** Adam (male, authoritative), Rachel (female, warm), or Bella (female, conversational)
- **Stability:** 0.50-0.65 (lower = more expressive, higher = more consistent)
- **Clarity + Similarity:** 0.80-0.85
- **Style Exaggeration:** 0.20-0.35 (too high sounds unnatural)
- **Speaker Boost:** ON

**How to Structure Script for Natural Pauses:**
- Use `...` for short pauses (0.3s)
- Use `[pause]` or a line break for longer pauses (0.7-1s)
- Commas already generate natural micro-pauses
- Questions naturally get upward inflection — write them as questions
- Avoid run-on sentences — each sentence should be speakable in one breath

**Batch Processing Multiple Scripts:**

Option A (Manual): 
1. Open ElevenLabs
2. Paste script → Generate → Download
3. Name file: `[channel-name]_[date]_[topic-slug].mp3`
4. Save to Google Drive folder: `/voiceovers/pending/`

Option B (API via n8n — fully automated):
- n8n receives script text from OpenAI node
- Sends POST request to ElevenLabs API: `https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`
- Body: `{ "text": "{{script}}", "voice_settings": { "stability": 0.6, "similarity_boost": 0.85 } }`
- Response contains audio binary → save to Google Drive
- Estimated generation time: 30-90 seconds for a full 10-minute script

**ElevenLabs API Rate Limits:** Creator plan allows 2 concurrent requests. For batch jobs, queue them with a 2-second delay between requests.

---

## Phase 3 — Visuals (10-20 min, semi-automated)

### Model A: Stock Footage (Fastest)

**Tool:** Pexels.com + Storyblocks

**Search Strategy:**
1. Look at each `[SCENE: description]` tag in your script
2. Extract 3-4 keyword candidates per scene
3. Search from most specific to most general:
   - "stock market crash 2025" → "stock market red" → "financial charts" → "money"
4. Download 3 candidates per scene (you'll only use 1, but options save time later)
5. Naming convention: `scene01_financial-charts.mp4`, `scene02_world-map.mp4`

**Time saving tip:** Build a personal footage library. Every time you download a clip, tag it with keywords. After 10 videos, you'll have 80% of what you need without searching.

**Footage duration matching:**
- Listen to voiceover while noting timestamp of each `[SCENE]` marker
- Each scene needs footage equal to that scene's duration + 10% buffer
- For 30-second scenes: minimum 35-second clip, or cut between 2-3 clips

---

### Model B: AI Video Generation (Best Quality)

**Tool:** Kling AI (primary) + Runway Gen-4 (secondary)

**Kling Workflow:**
1. Go to klingai.com → Image/Video → Text to Video
2. Mode: Professional (5s or 10s clips)
3. Write your prompt using this structure:

```
[Camera movement] [Subject description] [Action] [Setting] [Lighting] [Style] [Quality tags]

Example:
"Slow dolly-in shot, photorealistic close-up of a stock market trading screen showing red declining numbers, 
tense atmosphere, dramatic blue-tinted office lighting, cinematic 4K quality, 
film grain, shallow depth of field"
```

**Maintaining Scene Consistency:**
- Create a "style bible" document: "All videos use cinematic 4K, cold blue color grade, corporate setting"
- Use the same style suffix on every prompt: `"cinematic 4K, blue-tinted color grade, film grain, photorealistic"`
- For character consistency (if showing a person): use Kling's "Image to Video" feature — generate a character image in Midjourney first, then animate it consistently
- Generate 3 variations per scene, pick best

**Runway Gen-4 Workflow:**
- Better for abstract visuals: "AI brain network", "data streams", "futuristic city"
- Use "Reference image" feature for style consistency — upload your style reference once
- Camera controls: Zoom in/out, pan left/right, orbit — use these to add motion to otherwise static scenes

**Batch generation strategy:** 
Queue all 8-10 scene prompts at once. Each takes 2-5 min to generate. By the time you finish writing all prompts, your first clips are ready.

---

### Model C: AI Avatar (HeyGen Workflow)

1. **Go to HeyGen.com → Create Video → Instant Avatar or Stock Avatar**
2. **Select avatar:** Choose one and stick with it — consistency builds recognition
3. **Paste script** into the text box
4. **Select voice:** Use ElevenLabs integration (HeyGen allows custom voices) OR use HeyGen's built-in voices
5. **Set background:** Green screen (replace later in editing) or a pre-made set background
6. **Generate** — takes 5-15 min for 10-minute video
7. **Download** the MP4

**Post-HeyGen workflow:**
- Import avatar video into CapCut
- Replace background if using green screen
- Add B-roll cutaways (stock footage or AI clips) for visual variety every 30-45 seconds
- The avatar should NOT be on screen 100% of the time — cut away to relevant footage

---

## Phase 4 — Assembly & Editing (10 min)

### CapCut Workflow (Batch Editing)

**Setup (do once):**
1. Create a CapCut template for your channel:
   - Aspect ratio: 16:9 (YouTube) or 9:16 (Shorts/TikTok)
   - Color grade: apply your channel's LUT or color filter
   - Intro/outro: 2-3 second branded bumper
   - Music track: lo-fi background, volume at -25db under voiceover
   - Font style for captions: set as default

**Assembly sequence:**
1. Import voiceover MP3 as base track
2. Add footage/clips to timeline, match to voiceover timestamps
3. Trim clips to match scene durations
4. Add background music (CapCut's royalty-free library: search "corporate", "ambient", "motivational")
5. Apply color grade (one-click with preset)
6. Add auto-captions (see below)
7. Add lower thirds or text overlays for key stats/names
8. Export: 1080p minimum, 4K if clips are 4K source

**CapCut batch editing for multiple videos:**
- Create a Project Folder per channel
- Use "Templates" feature — set up your standard format once, apply it to new projects in 2 clicks
- If producing the same format repeatedly (e.g., daily 60-second news shorts), CapCut templates save 70% of assembly time

---

### Auto-Captions

**Tool: CapCut built-in captions (free)**
1. In CapCut: Tools → Auto Captions → Generate
2. Review generated text (usually 95%+ accurate with clean ElevenLabs audio)
3. Style: Large font, centered, with slight background shadow
4. For TikTok style: Use "Impact" or "Anton" font, white with black outline, centered lower-third position

**Alternative: Submagic.co** ($20/month)
- More stylized caption options (animated, gradient, emoji auto-suggest)
- Better for viral short-form content where captions are a visual element themselves

---

### Thumbnail Creation

**Workflow (10-12 min):**

1. **Generate background image in Midjourney:**
```
Prompt: "Dramatic thumbnail background for YouTube video about [topic], 
highly contrasted, bold colors, cinematic, [relevant visual], 
no text, 16:9 ratio, designed to grab attention in feed --ar 16:9 --v 6"
```

2. **Open Canva → Custom Size → 1280x720**
3. Import Midjourney image as background
4. Add text:
   - Main title: 72-90pt bold, high contrast color (yellow, red, or white with black stroke)
   - Max 5 words in main title
   - Optional: number or statistic in large font ("$2 TRILLION LOST")
5. Add arrow or circle pointing to key visual element (optional but effective for CTR)
6. Export PNG

**Thumbnail Rules that Drive CTR:**
- Face (even AI avatar face) + big emotion = 40% higher CTR than no face
- Question or controversy outperforms statement ("Is AI killing jobs?" vs "AI Kills Jobs")
- 3 colors maximum
- Test 2 thumbnails per video using TubeBuddy A/B testing

---

## Phase 5 — Publishing (2 min, fully automated)

### YouTube Auto-Schedule via n8n

*Full workflow in n8n-workflow-design.md. Summary here:*

1. Video file uploaded to Google Drive folder `/ready-to-upload/[channel-name]/`
2. n8n detects new file (Google Drive trigger)
3. n8n calls YouTube Data API v3: `videos.insert` endpoint
4. Metadata auto-populated from Google Sheets row:
   - Title (AI-generated from script topic)
   - Description (AI-generated: summary + affiliate links + chapters + CTA)
   - Tags (extracted from script keywords)
   - Category, Playlist, Made for Kids: No
   - Schedule time: next open slot in channel schedule
5. Thumbnail uploaded separately via `thumbnails.set` API call
6. Telegram notification sent: "✅ Video scheduled: [title] on [channel] at [time]"

**YouTube scheduling strategy:**
- Publish Tuesday, Thursday, Saturday for general audiences
- Finance: Monday, Wednesday, Friday (market week)
- Don't publish every day at start — 3x/week is sustainable and gives algorithm time to test each video

---

### TikTok Auto-Post Options

**Option A: TikTok API (direct)** — requires TikTok Developer account + approval process (takes 1-2 weeks). Once approved, fully automated.

**Option B: Buffer** ($6/month for 1 channel) — connect TikTok, schedule posts. Not 100% API — still requires mobile notification confirm on first post.

**Option C: Later.com** ($18/month) — best cross-posting tool. Auto-post to TikTok, Instagram Reels, YouTube Shorts from one upload.

**✅ Recommendation:** Use **Later** ($18/month) for TikTok/Instagram Reels cross-posting. For YouTube, use direct API via n8n.

---

### Cross-Posting Strategy

**The "One Video, Three Platforms" system:**

1. **Long-form (YouTube):** Full 8-10 min video as main content
2. **Short-form clip (YouTube Shorts / TikTok / Reels):** Extract the 45-60 second most interesting segment
   - Use CapCut's crop tool to reframe 16:9 → 9:16 (vertical)
   - Add captions if not already present
3. **Quote card (Instagram / Twitter):** Pull most quotable line → Canva graphic

**Time added:** 10-15 min extra per video to create short-form version. Worth it — each short can drive subscribers back to your main channel.

---

## Total Time Per Video (Realistic Estimate)

### First 10 videos (learning curve):
- Phase 1: 15-20 min (finding topics, editing scripts)
- Phase 2: 5-10 min (ElevenLabs, manual steps)
- Phase 3: 30-45 min (sourcing footage, generating AI clips)
- Phase 4: 30-45 min (assembly, captions, thumbnail)
- Phase 5: 10-15 min (manual upload, scheduling)
- **Total: 1.5-2.5 hours per video**

### Videos 20-50 (pipeline dialed in):
- Phase 1: 5 min (n8n finds topic, Claude writes script)
- Phase 2: 2 min (n8n auto-generates audio)
- Phase 3: 15-20 min (footage sourcing, some AI generation)
- Phase 4: 15-20 min (CapCut template, captions, thumbnail)
- Phase 5: 2 min (drag to Drive folder, n8n does the rest)
- **Total: 40-50 min per video**

### Full automation (50+ videos, templates locked in):
- **Total human time: 15-25 min per video**
- Most of that is quality checking, not doing

The goal is to reach the 15-25 min level per video by video 50. That means you can produce 20-25 videos/week as a solo operator across multiple channels.
