# n8n Automation Design — Faceless Channel System
*Descriptive node-by-node design. Implement this in n8n's visual editor.*

---

## Prerequisites

Before building these workflows, set up:
- n8n instance (cloud at n8n.cloud or self-hosted on Hetzner VPS ~€6/month)
- Google Sheets API connected (via Google OAuth2 credential in n8n)
- OpenAI API key (or Anthropic API key for Claude)
- ElevenLabs API key
- YouTube Data API v3 credentials (Google Cloud Console)
- Telegram Bot (created via @BotFather, get bot token + your chat ID)
- Google Drive connected via OAuth2

---

## Workflow 1: "Script to Published" Pipeline

**Trigger:** New row in Google Sheets column A has value (not empty)

**Google Sheets schema:**
| Column | Field | Example |
|--------|-------|---------|
| A | Status | `PENDING` / `IN_PROGRESS` / `DONE` |
| B | Channel | `AIProductivityPro` |
| C | Topic | `How to automate your email with AI` |
| D | Platform | `YouTube` / `TikTok` / `Both` |
| E | Style | `informative` / `storytelling` / `listicle` |
| F | Script | *(auto-filled by workflow)* |
| G | AudioURL | *(auto-filled)* |
| H | VideoFile | *(manual or auto-filled)* |
| I | ThumbnailURL | *(auto-filled)* |
| J | ScheduleTime | *(auto-filled or manual)* |
| K | YouTubeID | *(auto-filled after upload)* |

---

### Node 0: Trigger — Google Sheets

**Node type:** `n8n-nodes-base.googleSheets` (Trigger mode)

**Configuration:**
- Operation: Watch rows
- Spreadsheet: [Your spreadsheet ID]
- Sheet: `Pipeline`
- Trigger on: Row added
- Poll interval: Every 5 minutes

**Output:** Full row data as JSON object
```json
{
  "Status": "PENDING",
  "Channel": "AIProductivityPro",
  "Topic": "How to automate email with AI in 2026",
  "Platform": "YouTube",
  "Style": "informative"
}
```

**First action:** Immediately update row Status to `IN_PROGRESS` using a Google Sheets node (Update operation, set Status column to "IN_PROGRESS") to prevent duplicate processing.

---

### Node 1: OpenAI — Generate Script

**Node type:** `n8n-nodes-base.openAi` (Chat Message operation)

**Inputs from trigger:** `Topic`, `Style`, `Channel` fields

**Configuration:**
- Model: `gpt-4o` (or use HTTP Request node to hit Claude API directly)
- Max tokens: 2000 (long-form) / 500 (short-form)
- Temperature: 0.7

**System prompt (set as static value):**
```
You are a YouTube script writer for faceless channels. Write engaging, 
punchy scripts optimized for AI voiceover narration. Include [SCENE: description] 
tags every 30 seconds. Start with a hook, no intro, end with soft CTA. 
No filler words. Short sentences. [PAUSE] markers where natural.
```

**User message (dynamic, built from trigger data):**
```
Channel: {{$json["Channel"]}}
Topic: {{$json["Topic"]}}
Style: {{$json["Style"]}}
Format: Long-form 8-10 minutes
Audience: Tech-savvy adults interested in productivity and AI tools

Write the complete script now.
```

**Output:** Script text string saved to variable `{{script}}`

**Post-node action:** Update Google Sheets row column F (Script) with the generated script.

---

### Node 2: ElevenLabs — Convert Script to Audio

**Node type:** `n8n-nodes-base.httpRequest`

*(ElevenLabs doesn't have a native n8n node yet — use HTTP Request)*

**Configuration:**
- Method: POST
- URL: `https://api.elevenlabs.io/v1/text-to-speech/{{voiceId}}`
  - Replace `{{voiceId}}` with your chosen voice ID (get from ElevenLabs dashboard)
  - Example Adam voice ID: `pNInz6obpgDQGcFmaJgB`
- Authentication: Header Auth → Header name: `xi-api-key`, Value: `{{$credentials.elevenLabsApiKey}}`
- Body (JSON):
```json
{
  "text": "{{$node['OpenAI'].json['message']['content']}}",
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
    "stability": 0.60,
    "similarity_boost": 0.85,
    "style": 0.25,
    "use_speaker_boost": true
  }
}
```
- Response format: Binary (audio/mpeg)

**Output:** Binary MP3 data

**Next step:** Save to Google Drive using Google Drive node:
- Operation: Upload file
- File name: `{{$json["Channel"]}}_{{$json["Topic"].slice(0,30)}}_{{$now.format('YYYYMMDD')}}.mp3`
- Parent folder: `/faceless-channel/audio/pending/`
- Returns: File URL / Drive file ID

**Post-node action:** Update Google Sheets column G (AudioURL) with the Drive file link.

---

### Node 3: Google Drive Storage + Webhook Trigger (Visuals)

**Node type:** `n8n-nodes-base.googleDrive` + Optional webhook to external tool

**What this node does:**
This node serves as the bridge between audio generation and visual assembly. Two paths:

**Path A — Stock footage model (no external tool):**
- Create a Google Drive folder: `/faceless-channel/pending-assembly/{{Channel}}/{{date}}/`
- Upload the audio file there
- Write a `METADATA.json` file to the folder:
```json
{
  "channel": "{{Channel}}",
  "topic": "{{Topic}}",
  "style": "{{Style}}",
  "audioFile": "{{audioURL}}",
  "sceneTimestamps": "{{extractedFromScript}}",
  "status": "AWAITING_VISUALS"
}
```
- This signals to you (or a VA) that audio is ready and visuals need to be assembled

**Path B — AI video tool webhook:**
- If your video assembly tool (Pictory, etc.) has a webhook/API:
- Send HTTP POST to tool's API with script text + audio URL
- Tool auto-generates video and returns video URL
- Continue to Node 6

---

### Node 4: Generate Thumbnail Prompt → DALL-E

**Node type:** `n8n-nodes-base.openAi` (Image operation)

**Inputs:** Topic, Channel, Script summary

**First:** Generate a thumbnail prompt via OpenAI Chat:
```
Based on this video topic: "{{Topic}}"
Write a DALL-E image generation prompt for a YouTube thumbnail background.
Requirements: dramatic, high contrast, cinematic, 16:9, no text, 
attention-grabbing, relevant to the topic, professional quality.
Return ONLY the image prompt, nothing else.
```

**Then:** Second OpenAI node (Images operation):
- Model: `dall-e-3`
- Size: `1792x1024` (closest to 16:9)
- Quality: `hd`
- Prompt: `{{outputFromPreviousStep}}`

**Output:** Image URL from DALL-E

**Save to Drive:** Upload to `/faceless-channel/thumbnails/raw/`
**Update Sheets:** Column I (ThumbnailURL) with Drive link

**Note on Midjourney:** Midjourney doesn't have an official API. You can trigger it via Discord webhook using an unofficial wrapper, but DALL-E 3 via OpenAI API is the reliable, integrable option. For better quality, generate thumbnails in Midjourney manually using the prompt from this node.

---

### Node 5: Wait for Video File

**Node type:** `n8n-nodes-base.wait` (Webhook resume) + `n8n-nodes-base.googleDrive` (watch folder)

**Two approaches:**

**Approach A — Manual wait (recommended for start):**
- Pause workflow execution using Wait node configured for "webhook" resume
- When you finish assembling the video, you upload it to a specific Google Drive folder
- A separate Google Drive trigger watches that folder
- When a new file appears, it resumes the paused workflow via webhook URL
- Timeout: 48 hours (if no video uploaded in 48h, send Telegram reminder and fail gracefully)

**Approach B — Pictory/automated assembly:**
- Skip the wait entirely if using an auto-assembly tool
- Node 3 sends script + audio to Pictory API
- Poll Pictory status endpoint every 2 minutes until status = "completed"
- Retrieve video URL and continue

---

### Node 6: YouTube Data API — Schedule Upload

**Node type:** `n8n-nodes-base.youTube`

*(Or HTTP Request to YouTube Data API v3 directly if n8n's YouTube node is limited)*

**Configuration:**
- Operation: Upload Video
- Video file: Binary from Google Drive download (fetch video file by ID)

**Video metadata (dynamically generated):**

First, generate title/description/tags using OpenAI node:
```
Based on this script topic: "{{Topic}}" and channel: "{{Channel}}"
Generate:
1. YouTube title (60 chars max, clickbait but accurate, include power words)
2. Description (150 words, include 2 paragraphs + "Chapters:" section + "🔗 Links:" section with placeholder [AFFILIATE_LINK_1])
3. Tags (15 comma-separated tags, mix broad and specific)
Return as JSON: {"title": "", "description": "", "tags": []}
```

**YouTube upload settings:**
```json
{
  "snippet": {
    "title": "{{generatedTitle}}",
    "description": "{{generatedDescription}}",
    "tags": ["{{tag1}}", "{{tag2}}", "..."],
    "categoryId": "22",
    "defaultLanguage": "en"
  },
  "status": {
    "privacyStatus": "private",
    "publishAt": "{{scheduleTime}}",
    "selfDeclaredMadeForKids": false
  }
}
```

**Schedule time logic:**
- Check a "Schedule Calendar" tab in Google Sheets
- Find next available upload slot for the channel (e.g., Mon/Wed/Fri at 14:00 UTC)
- Fill in the next empty slot

**After upload:** Call `thumbnails.set` API endpoint to attach thumbnail image.

**Output:** YouTube video ID

**Update Sheets:** Column K (YouTubeID) with video URL, Column A (Status) to "DONE"

---

### Node 7: Telegram Notification

**Node type:** `n8n-nodes-base.telegram`

**Configuration:**
- Credential: Your Telegram bot token
- Chat ID: Your personal Telegram chat ID (get via @userinfobot)
- Operation: Send message
- Text (formatted):

```
✅ *Video Scheduled*

📺 *Title:* {{generatedTitle}}
📢 *Channel:* {{Channel}}
🕐 *Publish Time:* {{scheduleTime}}
🔗 *YouTube:* https://youtube.com/watch?v={{youTubeVideoId}}

🎵 Audio: Ready
🖼️ Thumbnail: Ready
📊 Status: Scheduled

Next step: Review video quality before publish time.
```

- Parse mode: Markdown

---

## Workflow 2: "Topic Finder" (Daily Cron)

This runs every morning and populates your content pipeline automatically.

---

### Node 0: Cron Trigger

**Node type:** `n8n-nodes-base.cron`

**Configuration:**
- Mode: Every Day
- Hour: 9
- Minute: 0
- Timezone: Europe/Berlin (or your local timezone)

---

### Node 1: Fetch YouTube Trending via RapidAPI

**Node type:** `n8n-nodes-base.httpRequest`

**Configuration:**
- Method: GET
- URL: `https://youtube-v31.p.rapidapi.com/videos?part=snippet%2CcontentDetails%2Cstatistics&chart=mostPopular&regionCode=US&videoCategoryId=28&maxResults=20`
  - CategoryId 28 = Science & Technology (adjust for your niche)
  - Use `hl=en` for English results
- Headers:
  - `X-RapidAPI-Key`: your RapidAPI key
  - `X-RapidAPI-Host`: `youtube-v31.p.rapidapi.com`

**Cost:** RapidAPI YouTube API has a free tier (500 req/month). Paid plans start at $10/month for more.

**Output:** Array of 20 trending videos with title, view count, published time

---

### Node 2: Fetch Google Trends (Alternative / Additional)

**Node type:** `n8n-nodes-base.httpRequest`

**Tool:** Use the `serpapi.com` Google Trends endpoint (SerpAPI has a free tier: 100 searches/month)

- URL: `https://serpapi.com/search.json?engine=google_trends&q={{nicheKeyword}}&data_type=TIMESERIES&api_key={{serpApiKey}}`

**Output:** Trend data for your niche keyword — rising topics, breakout searches

---

### Node 3: Filter by Niche Keywords

**Node type:** `n8n-nodes-base.code` (JavaScript)

**What it does:** Takes raw trending topics and filters them to your niche.

```javascript
const trendingVideos = $input.all();
const nicheKeywords = ['AI', 'artificial intelligence', 'automation', 'ChatGPT', 
                        'productivity', 'tool', 'software', 'tech']; // customize per channel

const filtered = trendingVideos
  .filter(item => {
    const title = item.json.snippet?.title?.toLowerCase() || '';
    return nicheKeywords.some(kw => title.includes(kw.toLowerCase()));
  })
  .map(item => ({
    title: item.json.snippet.title,
    viewCount: item.json.statistics.viewCount,
    publishedAt: item.json.snippet.publishedAt,
    videoId: item.json.id,
    channelTitle: item.json.snippet.channelTitle
  }))
  .sort((a, b) => b.viewCount - a.viewCount)
  .slice(0, 5); // top 5 matching topics

return filtered.map(item => ({ json: item }));
```

**Output:** Array of top 5 filtered trending topics

---

### Node 4: Append to Google Sheets

**Node type:** `n8n-nodes-base.googleSheets`

**Configuration:**
- Operation: Append rows
- Spreadsheet: Your pipeline spreadsheet
- Sheet: `Pipeline`
- Columns to fill:
  - Status: `PENDING`
  - Channel: `{{targetChannel}}` (set as static based on which channel this cron runs for)
  - Topic: `{{title}}` from filtered results
  - Platform: `YouTube`
  - Style: `informative`

**Note:** This adds one row per trending topic. If 5 topics matched, 5 rows get added. You then manually flag which ones to actually produce (change Status to PENDING → IN_QUEUE or just delete the ones you don't want).

---

### Node 5: Telegram Notification — Top 3 Topics

**Node type:** `n8n-nodes-base.telegram`

**Configuration:**
- Operation: Send message
- Text:

```
🔥 *Daily Topic Report — {{$now.format('ddd DD MMM')}}*

Top trending topics for *{{channelName}}*:

1️⃣ {{topic1.title}}
   👁️ {{topic1.viewCount}} views | {{topic1.channelTitle}}

2️⃣ {{topic2.title}}
   👁️ {{topic2.viewCount}} views | {{topic2.channelTitle}}

3️⃣ {{topic3.title}}
   👁️ {{topic3.viewCount}} views | {{topic3.channelTitle}}

📋 All 5 topics added to pipeline sheet.
Reply with topic number to auto-approve for production.
```

**Optional enhancement:** Add inline buttons to the Telegram message (Telegram bot API supports this) so you can reply "1", "2", or "3" and a webhook triggers a status update in Google Sheets automatically.

---

## Implementation Notes

### Self-Hosting n8n (Recommended)

1. Get a Hetzner VPS: CX22 (€5.77/month, 2 vCPU, 4GB RAM)
2. Install n8n via Docker:
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=yourpassword \
  n8nio/n8n
```
3. Set up Nginx reverse proxy + SSL (Certbot)
4. Access your n8n at `https://yourdomain.com`

### Error Handling

Add error handler nodes after each critical step:
- If OpenAI fails: retry once, then send Telegram error notification
- If ElevenLabs fails: check character count (may have exceeded plan limit)
- If YouTube upload fails: check file size (<128GB), check OAuth token expiry

### Credentials to Set Up in n8n

1. Google Sheets (OAuth2)
2. Google Drive (OAuth2)  
3. YouTube (OAuth2) — needs `youtube.upload` scope
4. OpenAI (API key)
5. Telegram (Bot token + chat ID)
6. HTTP Header Auth for ElevenLabs
7. HTTP Header Auth for RapidAPI

All credentials stored in n8n's encrypted credential store — never in workflow nodes directly.
