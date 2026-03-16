# Week 1 Action Plan — Launch Your First Faceless Channel
*Day-by-day. No fluff. Do exactly this.*

---

## Before You Start: The One Decision

**Pick ONE niche. Right now. Don't second-guess it.**

Based on your interests (prediction markets, AI tools, content creation):
- **Best bet:** AI Tools & Productivity (easiest to automate, highest affiliate income)
- **Second best:** Prediction Markets (your existing knowledge = better content)

The niche doesn't matter as much as picking one and going. You can always pivot at video 20. You cannot pivot if you never start.

**Chosen niche: _____________** (fill this in before Day 1)

---

## Day 1: Niche Selection + Tool Setup

### Morning (2-3 hours)

**9:00 — Confirm your niche and first 10 video topics**

Open a Google Doc. Write 10 video topic ideas in your niche. Don't filter them — just brainstorm. Example for AI Tools:
1. "5 AI Tools That Replace Virtual Assistants in 2026"
2. "This Free AI Tool Writes Better Than ChatGPT"
3. "I Automated My Entire Week With These 3 AI Apps"
4. "The AI Tool That Made Me €500 in One Week"
5. "AI vs Human: Who Writes Better Emails?"

These become your first 10 videos. Add them to a Google Sheet with columns: Status, Channel, Topic, Platform, Style.

**10:00 — Set up free tools (today's tools are all free)**

1. **ElevenLabs** — Sign up: [elevenlabs.io](https://elevenlabs.io)
   - Free tier: 10,000 characters/month
   - Go to Voices → browse pre-made voices → test "Adam" and "Rachel" → pick one
   - Test: paste 200 words from any article → generate → listen to quality
   - **If stuck:** The voice list is overwhelming. Just pick Adam (male) or Rachel (female) and move on.

2. **Canva** — Sign up: [canva.com](https://canva.com)
   - Free tier: generous, enough for thumbnails
   - Create a Canva "Brand Kit" with your channel colors (pick 2 colors only: a bright accent + dark background)
   - **If stuck:** Use black background + yellow text. It works. Don't overthink branding on Day 1.

3. **CapCut Desktop** — Download: [capcut.com/download](https://www.capcut.com/download)
   - Free tier: almost fully featured
   - Open it, create a new project in 1920x1080 (YouTube) ratio
   - Spend 15 min clicking around — get familiar with the interface
   - **If stuck:** YouTube "CapCut beginner tutorial 2025" — watch 10 min

4. **Claude.ai or ChatGPT** — You likely have one already
   - Claude: [claude.ai](https://claude.ai) (free tier available)
   - Set up an account if you don't have one
   - **Which one:** Use Claude for scripts. It writes more natural-sounding narration.

**12:00 — Set up your Google Sheet pipeline tracker**

Create a new Google Sheet called "Channel Pipeline — [YourChannelName]"

Sheet 1: Pipeline
| Status | Channel | Topic | Platform | Style | Script | AudioURL | VideoFile | ThumbnailURL | Published |
|--------|---------|-------|----------|-------|--------|----------|-----------|--------------|-----------|

Sheet 2: Schedule
| Date | Time | Title | Status | YouTube ID |
|------|------|-------|--------|-----------|

Add your 10 video topics to Sheet 1, Status = "IDEA"

### Afternoon (1 hour)

**14:00 — Research your niche for 1 hour, then stop**

Go to YouTube. Search your niche keyword. Watch the top 5 videos. Note:
- How long are they? (This is your target length)
- What do the thumbnails look like? (Screenshot 5 good ones)
- What topics do well vs poorly? (Look at view counts)
- What's the comment section asking about? (These become future video ideas)

Create a folder in Google Drive: `/FacelessChannel/[ChannelName]/`
Subfolders: `scripts/`, `audio/`, `visuals/`, `finals/`, `thumbnails/`

**STOP researching after 1 hour.** Research is procrastination in disguise. You now know enough to make video 1.

---

## Day 2: First Script + Voiceover

### Morning (1.5-2 hours)

**9:00 — Pick your first topic**

From your list of 10, pick the one you're most excited about. Not the "safest" — the most interesting to you. Your enthusiasm comes through even in AI-narrated content.

**9:15 — Generate the script**

Open Claude. Use this exact prompt (fill in the brackets):

```
You are a YouTube script writer for a faceless channel about [YOUR NICHE].

Write a script for this video: [YOUR TOPIC]

Channel style: Informative, direct, confident. No fluff. Short punchy sentences.
Format: Long-form, target 9-10 minutes narration.
Audience: [Describe your target viewer in one sentence]

Requirements:
- Hook in first 3 seconds — shocking stat or bold claim, no "hey guys"
- Add [PAUSE] markers after each major point
- Add [SCENE: description] every 30-40 seconds for B-roll
- Add [EMPHASIS] on key phrases
- End with soft CTA to subscribe
- Target word count: 1,400-1,500 words
- No filler words: basically, essentially, literally, actually

Write the complete script now.
```

**Review the script (15-20 min):**
- Read it aloud in your head. Does it flow naturally?
- Edit anything that sounds robotic or unnatural
- Make sure the hook is genuinely compelling
- Save to Google Drive: `/scripts/[topic-slug].md`

**10:30 — Generate the voiceover**

Go to ElevenLabs:
1. Speech Synthesis → paste your script
2. Voice: your chosen voice (Adam/Rachel)
3. Settings: Stability 0.60, Clarity 0.85, Style 0.25
4. Remove all `[SCENE]`, `[PAUSE]`, `[EMPHASIS]` markers from the text before pasting (leave the `[PAUSE]` as literal `...` or line breaks for natural pauses)
5. Generate → Download MP3
6. Save to `/audio/[topic-slug].mp3`

**Listen to the full audio file.** If it sounds bad in any section, go back and edit that script section, regenerate.

**If ElevenLabs free tier runs out:**
- Free tier = 10,000 chars (~1,500 words = one long-form script, barely)
- Upgrade to Starter ($5/month: 30,000 chars) if you hit the limit
- Alternative: Use [TTS.Monster](https://tts.monster) (has free tier with different voices)

---

## Day 3: First Video Assembled

### Full day (3-4 hours with learning curve, 1.5-2h by video 5)

**9:00 — Source visuals**

Go through your script. Find every `[SCENE: description]` tag. You need footage for each one.

For each scene:
1. Go to [pexels.com/videos](https://www.pexels.com/videos/) 
2. Search the scene description keywords
3. Download the best matching clip (HD or better)
4. Save to `/visuals/scene01_description.mp4`, `scene02_...`, etc.

**What if you can't find matching footage?**
- Try broader keywords ("business meeting" instead of "CEO signing contract")
- Use a visual metaphor (talking about AI? → "robot", "circuit board", "data center")
- Generate a clip with Kling AI (free tier: limited generations per day)
  - Go to [klingai.com](https://klingai.com)
  - Text to Video → write prompt → generate → download
  - Takes 3-5 min per clip

**11:00 — Assembly in CapCut**

1. Open CapCut → New Project → 1920x1080
2. Import your audio MP3 as the base audio track
3. Listen to the first 30 seconds → find what scene plays at 0:00-0:30
4. Import that scene's footage → drag to video track
5. Trim footage to match audio length (hold edge of clip → drag)
6. Repeat for all scenes
7. **For gaps:** duplicate the previous clip or use a transition
8. **Music:** Import tab → Search "ambient" → pick a royalty-free track → drag under everything at -25dB volume
9. **Auto-captions:** Tools → Auto Captions → Generate → style the font (size 70-80, white, black outline, centered bottom third)
10. **Export:** Share → 1080p → Export

**If CapCut feels overwhelming:**
- Watch: "CapCut desktop tutorial for beginners" on YouTube (15 min)
- Or use Pictory instead: paste script → auto-generates with stock footage → minimal editing
  - Pictory: [pictory.ai](https://pictory.ai) — 3 free projects, then $25/month
  - Quality is lower but time is much faster (10 min vs 1 hour)

**14:00 — Create thumbnail**

1. Go to Canva → Create design → Custom (1280×720 pixels)
2. Set background to black or dark gradient
3. Add a royalty-free image from Pexels relevant to your topic
4. Text: Main title in yellow or white, 80pt font, bold, max 5 words
5. Add a number or statistic if your topic has one ("$5B", "2030", "#1")
6. Download as PNG

**Thumbnail checklist:**
- [ ] Can you read the text in thumbnail preview (tiny size)?
- [ ] Does it make you curious to click?
- [ ] Is it different from the other thumbnails on your niche search page?

---

## Day 4: Channel Setup + Branding

### Morning (2-3 hours)

**9:00 — Create the YouTube channel**

If you don't have one:
1. Google.com → Sign in → YouTube → Click your profile → Create Channel
2. Channel name: Think SEO + clarity. Examples: "AIToolsDaily", "PredictedMarket", "TheFutureReport"
3. **Rules for channel names:**
   - Easy to spell and remember
   - Contains a keyword from your niche
   - Doesn't limit you too much if you expand later
   - Available as a handle (@channelname) — check this

**10:00 — Brand the channel**

**Profile picture:**
- Option A: Go to Canva → use a simple logo template → your initials or icon
- Option B: Use DallE-3 or Midjourney to generate a logo icon
- Size: 800x800, circular crop safe zone

**Channel banner:**
- Canva → YouTube Channel Art template (2560x1440)
- Simple: your channel name + tagline + upload schedule ("New videos every Tuesday & Thursday")
- Download → Upload to YouTube Studio

**Channel description:**
```
[Channel Name] — [what you cover in one sentence].

New videos every [schedule]. Subscribe to stay ahead of [benefit for viewer].

Topics covered: [list 5-8 keywords naturally in sentences]

Business inquiries: [your email]
```

**11:00 — Set up the channel properly**

In YouTube Studio → Settings:
- **Upload defaults:**
  - Category: Science & Technology (or relevant category)
  - License: Standard YouTube
  - Tags: add your 10 core niche tags here (they auto-apply to every video)
  - Comments: Allow all (engagement matters for algorithm)
- **Channel → Basic Info:**
  - Description ✓
  - Links: Add your Telegram/social if applicable
- **Monetization:** Apply if you have 500+ subs and 3,000 watch hours (new 2024 threshold for basic monetization). Otherwise, just track where you stand.

**12:00 — Set up affiliate links (do this now, not later)**

Based on your niche, sign up for 2-3 affiliate programs today:
- **AI Tools niche:**
  - ElevenLabs affiliate: [elevenlabs.io/affiliate](https://elevenlabs.io/affiliate) (22% recurring)
  - Jasper AI: [jasper.ai/affiliate](https://www.jasper.ai/affiliate) (30% recurring)
  - Notion: via Creator Fund (varies)
- **Prediction Markets / Finance niche:**
  - Trading212: [trading212.com/promote](https://www.trading212.com/promote) (~€30 CPA)
  - eToro: available via CJ Affiliate (up to €200 CPA)
  - Degiro: check their affiliate page
- **Any niche:**
  - Amazon Associates: [affiliate-program.amazon.com](https://affiliate-program.amazon.com) (easy approval, low rates but covers everything)

Create a template description with your affiliate links already formatted. Paste this in every video's description.

---

## Day 5: First Upload

### Morning (1-2 hours)

**9:00 — Final quality check on your video**

Watch your assembled video with fresh eyes. Check:
- [ ] Hook is strong — would you keep watching?
- [ ] Audio is clear throughout, no weird pronunciation
- [ ] Captions are accurate (spot check 5 random moments)
- [ ] Footage matches what's being said
- [ ] Music isn't too loud or distracting
- [ ] Thumbnail reads clearly at small size

Fix anything that bothers you. Don't aim for perfect — aim for "good enough to publish."

**10:30 — Upload to YouTube**

1. YouTube Studio → Create → Upload video
2. Upload your MP4
3. While uploading, fill in metadata:

**Title formula:** `[Number/Power word] + [Topic] + [Year/Benefit]`
Examples:
- "5 AI Tools That Will Replace Your Entire Team in 2026"
- "The Prediction Market Nobody Is Watching (Yet)"
- "This AI Tool Writes Better Than Me — I Tested It"

**Description template:**
```
[2-3 sentence summary of what the video covers and why it matters]

In this video:
0:00 - Intro
[timestamps for each major section]

🔗 Resources Mentioned:
→ [Tool/Link 1] — [affiliate link]
→ [Tool/Link 2] — [affiliate link]

📺 More videos like this:
[link to playlist when you have one]

---
#[niche] #[keyword2] #[keyword3]
```

**Tags:** 10-15 tags: mix exact match keywords + broad category keywords

**Thumbnail:** Upload your Canva-designed thumbnail

**End screen:** Add end screen to last 20 seconds (YouTube Studio → End Screen → add "Subscribe" button + "Video" card)

**Schedule or publish?**
- If it's before noon on a Tuesday/Thursday/Saturday: publish now
- Otherwise: schedule for the next Tuesday/Thursday at 14:00 your local time

**After publishing:**
- Share the video link to your personal accounts (even if you have 5 followers — it signals initial engagement to YouTube)
- Drop it in any relevant Reddit community (r/AItools, r/productivity, etc.) — NOT as spam, as genuine contribution with a comment like "I made a video about this"

---

## Days 6-7: Batch Produce 3 More Videos

### The Goal
By end of Day 7: 4 videos published or scheduled. This proves the pipeline works and gives YouTube enough content to understand your channel.

**Day 6 Schedule:**
- 9:00-10:30: Script 2 (Claude prompt → review → save)
- 10:30-11:00: Voiceover 2 (ElevenLabs → download)
- 11:00-12:30: Script 3 (Claude prompt → review → save)
- 12:30-13:00: Lunch break
- 13:00-13:30: Voiceover 3 (ElevenLabs → download)
- 13:30-15:30: Assemble Video 2 (CapCut)
- 15:30-16:30: Thumbnail 2 (Canva)
- 16:30-17:00: Upload Video 2 (schedule for Day 9 or 10)

**Day 7 Schedule:**
- 9:00-11:00: Assemble Video 3 (CapCut — faster now that you know the process)
- 11:00-11:30: Thumbnail 3
- 11:30-12:00: Upload Video 3 (schedule for Day 11 or 12)
- 12:00-13:00: Script 4
- 13:00-13:30: Voiceover 4
- 13:30-15:00: Assemble Video 4
- 15:00-15:30: Thumbnail 4
- 15:30-16:00: Upload Video 4 (schedule for Day 14)
- **16:00-17:00: Review week. What worked? What was slow? Write it down.**

---

## If Something Doesn't Work

| Problem | Solution |
|---------|----------|
| ElevenLabs free tier runs out | Upgrade to $5 Starter OR use [TTS.Monster](https://tts.monster) free tier |
| Can't find matching stock footage | Use Kling AI free tier to generate 1-2 key scenes |
| CapCut won't export | Check storage space. Try exporting at 720p first to test. |
| Script sounds robotic | Rewrite the worst sentences manually. Rule: if you wouldn't say it out loud, fix it. |
| YouTube upload rejected | File must be MP4/MOV, under 128GB, at least 720p |
| Can't think of a thumbnail design | Copy the layout of a competitor thumbnail, swap the text and colors |
| Zero views after 48h | Normal. YouTube takes 72h to index a new channel. Check back after 5 days. |
| View count stuck at 50 | Your thumbnail or title isn't compelling enough. A/B test a different title. |

---

## Week 2+ Strategy

After Week 1, you should have:
- ✅ 4 videos published
- ✅ Channel fully branded
- ✅ Pipeline understood
- ✅ Affiliate links in place

**Week 2 goals:**
- Publish 3-5 more videos
- Check analytics on first 4 videos — which has best CTR? Best watch time? Make more of that.
- Start testing Shorts: take 45-second clips from your long videos → upload as Shorts
- Set up n8n for topic finding (see n8n-workflow-design.md)

**First monetization milestone (not AdSense):**
When you hit 500 subscribers, you're eligible for YouTube's expanded partner program. But before that — check if your affiliate links are generating any clicks. Even 2-3 clicks/week means you're on track.

**When to scale to a second channel:**
- Channel 1 has 1,000+ subscribers
- You can produce a video in under 45 minutes
- Your average video gets 500+ views in first week

Then, and only then, start Channel 2 in a related but different niche.

---

## Your Week 1 Checklist

**Day 1:**
- [ ] Picked niche
- [ ] 10 video topics in Google Sheet
- [ ] ElevenLabs account created
- [ ] CapCut installed
- [ ] Canva account created
- [ ] Google Drive folders set up

**Day 2:**
- [ ] Script 1 written and reviewed
- [ ] Voiceover 1 generated and downloaded

**Day 3:**
- [ ] Footage sourced for all scenes
- [ ] Video assembled in CapCut
- [ ] Captions added
- [ ] Thumbnail created

**Day 4:**
- [ ] YouTube channel created
- [ ] Profile picture uploaded
- [ ] Channel banner uploaded
- [ ] Channel description written
- [ ] Affiliate programs joined (2-3)

**Day 5:**
- [ ] Video 1 quality checked
- [ ] Metadata written (title, description, tags)
- [ ] Video 1 uploaded and scheduled

**Days 6-7:**
- [ ] Scripts 2-4 written
- [ ] Voiceovers 2-4 generated
- [ ] Videos 2-4 assembled
- [ ] Thumbnails 2-4 created
- [ ] Videos 2-4 uploaded and scheduled
- [ ] Week reviewed — bottlenecks identified

**You now have a functioning faceless channel operation. The next 20 videos will be 2x faster than these first 4.**
