# n8n Workflow Design — Faceless Video Channel Automation

> Human-readable workflow specification. A developer can implement this directly in n8n.
> Last updated: March 2026

---

## Overview

This workflow takes a topic as input and outputs a ready-to-upload video file + thumbnail. It is triggered either manually (Webhook trigger) or on a schedule (CRON trigger reading from a topic queue).

**Estimated run time:** 15–45 minutes per video (most time is AI video generation)

---

## Workflow Architecture

```
[TRIGGER] → [TOPIC INPUT] → [SCRIPT] → [VOICEOVER] → [VISUALS] → [ASSEMBLY] → [CAPTIONS] → [THUMBNAIL] → [UPLOAD]
                                              ↓
                                    [ERROR HANDLER + NOTIFICATION]
```

The workflow has two parallel branches after script generation:
- **Branch A:** Audio (voiceover → captions)
- **Branch B:** Visuals (clip generation/search)

Both branches converge at Assembly.

---

## Node-by-Node Design

---

### NODE 1: Trigger
**Type:** Webhook (Manual) OR Schedule (CRON)

**What it does:**
- Webhook mode: Lyubo sends a POST request with `{ "topic": "...", "niche": "...", "duration_minutes": 5 }` and the workflow starts immediately.
- CRON mode: Runs daily at 9:00 AM, reads the first "pending" row from a Google Sheet (topic queue), marks it as "in progress."

**Input:** `{ topic, niche, duration_minutes, style_notes? }`

**Output:** Passes topic data to all downstream nodes.

**Google Sheet columns for queue:**
- Topic | Niche | Duration | Status | Video URL | Created At

---

### NODE 2: Set Workflow Variables
**Type:** Set

**What it does:**
Defines variables used throughout the workflow to avoid repetition. Central config.

**Variables set:**
```
video_title = {{ $json.topic }}
niche = {{ $json.niche }}
duration_min = {{ $json.duration_minutes }}
word_count = {{ $json.duration_minutes * 160 }}  // 160 words/min
timestamp = {{ Date.now() }}
job_id = {{ 'job_' + Date.now() }}
output_folder = /videos/{{ $vars.job_id }}/
```

---

### NODE 3: Script Generator
**Type:** HTTP Request (POST to Claude API) OR OpenAI node

**What it does:**
Calls Claude API with a detailed prompt. Returns a structured script with [VISUAL] cues.

**API Call:**
- URL: `https://api.anthropic.com/v1/messages`
- Method: POST
- Headers: `x-api-key: YOUR_KEY`, `anthropic-version: 2023-06-01`
- Body:
```json
{
  "model": "claude-sonnet-4-5",
  "max_tokens": 4000,
  "messages": [{
    "role": "user",
    "content": "Write a YouTube script for: [TOPIC]. Niche: [NICHE]. Target length: [WORD_COUNT] words. Include [VISUAL: brief scene description] cues every 100-150 words. Return JSON: { title, description, tags: [], script_with_cues, script_clean (no cues), visual_cues: [{timestamp_approx, description}] }"
  }]
}
```

**Output:**
```json
{
  "title": "...",
  "description": "...",
  "tags": ["tag1", "tag2"],
  "script_clean": "full voiceover text...",
  "visual_cues": [
    {"index": 0, "description": "aerial view of city skyline"},
    {"index": 1, "description": "close-up of stock chart going up"},
    ...
  ]
}
```

**Error handling:** If API fails, retry once after 30 seconds. If fails again, send Telegram notification and stop.

---

### NODE 4: Parse Script Output
**Type:** Code (JavaScript)

**What it does:**
Parses Claude's JSON response. Extracts the clean script for TTS and the visual cues list for video generation. Also counts characters for TTS cost estimate.

**Code:**
```javascript
const response = JSON.parse(items[0].json.content[0].text);
return [{
  json: {
    script_clean: response.script_clean,
    visual_cues: response.visual_cues,
    title: response.title,
    description: response.description,
    tags: response.tags,
    char_count: response.script_clean.length
  }
}];
```

---

### NODE 5: Split into Parallel Branches
**Type:** Split in Batches (or just duplicate data)

Passes the same data into two parallel paths:
- **Path A → Voiceover generation**
- **Path B → Video clip generation**

Both run simultaneously to save time.

---

## BRANCH A: Audio Pipeline

---

### NODE A1: Generate Voiceover
**Type:** HTTP Request (POST to ElevenLabs API)

**What it does:**
Converts the clean script to MP3 using ElevenLabs TTS.

**API Call:**
- URL: `https://api.elevenlabs.io/v1/text-to-speech/VOICE_ID`
- Method: POST
- Headers: `xi-api-key: YOUR_KEY`, `Content-Type: application/json`
- Body:
```json
{
  "text": "{{ $json.script_clean }}",
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.4,
    "use_speaker_boost": true
  }
}
```
- Response type: Binary (MP3 file)

**Output:** Binary MP3 data → save to `output_folder/voiceover.mp3`

**Save file:** Use "Write Binary File" node to save to disk.

---

### NODE A2: Generate Captions (Whisper)
**Type:** HTTP Request (POST to OpenAI Whisper API)

**What it does:**
Transcribes the voiceover MP3 to get accurate timestamps. Returns SRT file.

**API Call:**
- URL: `https://api.openai.com/v1/audio/transcriptions`
- Method: POST (multipart/form-data)
- Body:
  - `file`: voiceover.mp3
  - `model`: whisper-1
  - `response_format`: srt
  - `language`: en

**Output:** SRT file content (text) → save to `output_folder/captions.srt`

---

## BRANCH B: Visuals Pipeline

---

### NODE B1: Expand Visual Cues
**Type:** Code (JavaScript)

**What it does:**
Takes the `visual_cues` array from the script. For each cue, decides whether to use stock footage (Pexels) or AI generation (Kling). Decision logic:
- If cue contains "character", "person", "host" → Kling AI
- Otherwise → Pexels API first (free), Kling as fallback

Also generates enhanced prompts for Kling.

**Output:** Array of tasks:
```json
[
  {"index": 0, "source": "pexels", "query": "city skyline aerial", "duration": 5},
  {"index": 1, "source": "kling", "prompt": "close-up of stock chart, bullish green candles, cinematic...", "duration": 5},
  ...
]
```

---

### NODE B2: Fetch Stock Footage (Pexels)
**Type:** HTTP Request → runs for items where source = "pexels"

**What it does:**
Queries Pexels API for each visual cue, downloads the best matching video clip.

**API Call:**
- URL: `https://api.pexels.com/videos/search?query={{ $json.query }}&per_page=3&orientation=landscape`
- Method: GET
- Headers: `Authorization: YOUR_PEXELS_KEY`

**Logic:**
- Take the first result with duration ≥ 5 seconds
- Download MP4 to `output_folder/clips/pexels_{{ index }}.mp4`

---

### NODE B3: Generate AI Video Clips (Kling)
**Type:** HTTP Request → runs for items where source = "kling"

**What it does:**
Calls Kling API to generate video clips from text prompts.

**API Call (submit job):**
- URL: `https://api.klingai.com/v1/videos/text2video`
- Method: POST
- Headers: `Authorization: Bearer YOUR_KLING_KEY`
- Body:
```json
{
  "model_name": "kling-v1-6",
  "prompt": "{{ $json.prompt }}, cinematic, 4K, [CHANNEL_STYLE]",
  "negative_prompt": "blurry, text, watermark, low quality",
  "cfg_scale": 0.5,
  "mode": "std",
  "duration": "5"
}
```

**Response:** Returns a `task_id`

---

### NODE B4: Wait for Kling Jobs
**Type:** Wait + Loop (HTTP Request polling)

**What it does:**
Polls Kling API every 30 seconds until all jobs complete (status = "succeed").

**API Call (check status):**
- URL: `https://api.klingai.com/v1/videos/text2video/{{ task_id }}`
- Method: GET

**Logic:**
- If status = "processing" → wait 30 seconds, retry
- If status = "succeed" → download MP4 from `data.task_result.videos[0].url`
- If status = "failed" → fall back to Pexels for that clip

**Max wait:** 15 minutes per job. Timeout = skip clip + use Pexels fallback.

---

### NODE B5: Download Kling Clips
**Type:** HTTP Request (GET, binary)

Downloads each completed Kling video to `output_folder/clips/kling_{{ index }}.mp4`

---

## MERGE: Combine A + B

---

### NODE 6: Wait for Both Branches
**Type:** Merge (Wait for all inputs)

Waits until both audio pipeline (A2 done) and visual pipeline (B5 done) complete.

**Output:** Passes combined data:
- Path to `voiceover.mp3`
- Path to `captions.srt`
- Array of clip paths in order
- Title, description, tags

---

### NODE 7: Generate Clips Manifest
**Type:** Code (JavaScript)

**What it does:**
Creates the FFmpeg concat manifest file. Orders clips by visual_cue index. Calculates how many times to loop/trim each clip to match the voiceover duration.

**Output:** Creates `output_folder/clips_list.txt`:
```
file '/videos/job_123/clips/pexels_0.mp4'
duration 5
file '/videos/job_123/clips/kling_1.mp4'
duration 5
...
```

Also calculates total clip duration vs voiceover duration and adjusts (trim last clip or add padding).

---

### NODE 8: Assemble Video (FFmpeg)
**Type:** Execute Command

**What it does:**
Runs FFmpeg to combine everything into the final video.

**Commands (run in sequence):**

```bash
# Step 1: Concatenate clips
ffmpeg -f concat -safe 0 -i /videos/{{ job_id }}/clips_list.txt \
  -c:v libx264 -crf 23 -preset fast \
  /videos/{{ job_id }}/raw_video.mp4

# Step 2: Mix audio (voiceover + background music)
ffmpeg -i /videos/{{ job_id }}/raw_video.mp4 \
  -i /videos/{{ job_id }}/voiceover.mp3 \
  -i /assets/bgmusic/{{ niche }}_music.mp3 \
  -filter_complex "[2:a]volume=0.12[bg];[1:a][bg]amix=inputs=2:duration=first[audio]" \
  -map 0:v -map "[audio]" \
  -shortest \
  /videos/{{ job_id }}/with_audio.mp4

# Step 3: Burn subtitles
ffmpeg -i /videos/{{ job_id }}/with_audio.mp4 \
  -vf "subtitles=/videos/{{ job_id }}/captions.srt:force_style='FontName=Montserrat,FontSize=24,Bold=1,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,Outline=2,Alignment=2'" \
  /videos/{{ job_id }}/final.mp4
```

**Output:** `final.mp4` ready to upload.

---

### NODE 9: Generate Thumbnail
**Type:** HTTP Request (POST to OpenAI DALL-E 3 or Ideogram)

**What it does:**
Creates a thumbnail image based on the video title.

**API Call (DALL-E 3):**
- URL: `https://api.openai.com/v1/images/generations`
- Method: POST
- Body:
```json
{
  "model": "dall-e-3",
  "prompt": "YouTube thumbnail for video titled '{{ title }}'. Dramatic, high contrast, cinematic style. No text in image. [NICHE_STYLE_GUIDE]. Professional, 4K quality.",
  "size": "1792x1024",
  "quality": "hd",
  "n": 1
}
```

**Output:** Download image → `output_folder/thumbnail.jpg`

---

### NODE 10: Upload to YouTube
**Type:** YouTube (native n8n node)

**What it does:**
Uploads the final video and sets all metadata.

**Action:** Upload Video
**Credentials:** YouTube OAuth2 (pre-configured in n8n)

**Parameters:**
```
title: {{ $json.title }}
description: {{ $json.description }}
tags: {{ $json.tags }}
categoryId: 22 (People & Blogs) — adjust per niche
privacyStatus: private (then schedule or publish manually)
publishAt: {{ calculated_publish_time }}
```

Then second YouTube node:
**Action:** Set Thumbnail
Upload `thumbnail.jpg` to the just-uploaded video.

---

### NODE 11: Update Status Sheet
**Type:** Google Sheets (Update Row)

**What it does:**
Marks the topic in the queue as "completed" and writes the YouTube video URL.

**Updates:**
- Status: "completed"
- Video URL: `https://youtube.com/watch?v={{ video_id }}`
- Completed At: timestamp
- Cost (calculated): estimated API cost for this run

---

### NODE 12: Send Notification
**Type:** Telegram (or Email)

**What it does:**
Sends Lyubo a Telegram message: "✅ New video ready: [TITLE] — [YouTube URL]"

**Message template:**
```
✅ Video production complete!

📹 Title: {{ title }}
🎯 Niche: {{ niche }}
🔗 YouTube: {{ youtube_url }}
💰 Est. cost: ~${{ cost }}
⏱ Production time: {{ minutes }} minutes

Status: Scheduled for {{ publish_time }}
```

---

### NODE E: Error Handler
**Type:** Error Trigger (separate workflow or error branch)

**Catches:** Any node failure
**Actions:**
1. Save error log to Google Sheet
2. Send Telegram alert: "❌ Video production FAILED for: [TOPIC]. Error: [message]"
3. Mark topic as "failed" in queue

---

## Complete Workflow Visual Map

```
[CRON/Webhook Trigger]
         │
    [Read Topic Queue]
         │
    [Set Variables]
         │
    [Generate Script — Claude API]
         │
    [Parse Script JSON]
         │
    ┌────┴────┐
    │         │
[BRANCH A]  [BRANCH B]
    │         │
[Voiceover] [Expand Visual Cues]
[ElevenLabs]    │
    │       ┌──┴──┐
[Captions] [Pexels] [Kling AI]
[Whisper]  [Fetch]  [Generate]
    │           │       │
    │       [Wait for Kling]
    │           │
    └─────[MERGE]
              │
      [Build Clips Manifest]
              │
      [FFmpeg Assembly]
              │
      [Generate Thumbnail]
              │
      [Upload to YouTube]
              │
      [Set Thumbnail]
              │
      [Update Status Sheet]
              │
      [Telegram Notification]
```

---

## Required Credentials in n8n

| Credential | Type | Where to get |
|---|---|---|
| Claude API Key | HTTP Header Auth | console.anthropic.com |
| ElevenLabs API Key | HTTP Header Auth | elevenlabs.io/api |
| OpenAI API Key | HTTP Header Auth | platform.openai.com |
| Pexels API Key | HTTP Header Auth | pexels.com/api |
| Kling AI API Key | Bearer Token | klingai.com developer |
| YouTube OAuth2 | OAuth2 | Google Cloud Console |
| Google Sheets | OAuth2 | Google Cloud Console |
| Telegram Bot | Bot Token | @BotFather on Telegram |

---

## n8n Server Requirements

Since you already have n8n running:
- Ensure the n8n server has FFmpeg installed: `sudo apt install ffmpeg`
- Create the output directory: `mkdir -p /videos && chmod 755 /videos`
- Install background music assets to `/assets/bgmusic/` organized by niche

---

*See `system-blueprint.md` for tool rationale and `cost-calculator.md` for per-video cost breakdown.*
